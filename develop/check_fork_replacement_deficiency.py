"""Controls for exact fixed-arm value, tree defects and beta-retaining cost.

The arbitrary-size arguments are written in FORK_REPLACEMENT_DEFICIENCY.md.
Finite matching, ordinary terminal flow and packing are independent comparisons.
All generated systems are abstract, with separately labelled physical lifts.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_fork_arm_replacement import model
from check_one_sided_interval_allocation import allocate,independent_maximum
from check_whole_support_fork_normal_form import (
    ordinary_flow,optimize,canonical,evaluate,
)
from check_compensation_flow_normal_form import owner_data
from check_frozen_missing_port_bp_injection import inspect as inject
from check_terminal_cancellation_and_stranded_demand import terminal_data
from check_frozen_beta_support_fork import stacked,A,C,B,restrict
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_whole_support_fork_normal_form import whole_support_data

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def incidence(neighbors):
    return {j:{f for f,n in enumerate(neighbors) if j in n}
            for j in set().union(set(),*neighbors)}


def hall_deficiency(neighbors):
    best=0;witness=[]
    for mask in range(1<<len(neighbors)):
        chosen=[f for f in range(len(neighbors)) if mask>>f&1]
        neighborhood=set().union(set(),*(neighbors[f] for f in chosen))
        d=len(chosen)-len(neighborhood)
        if d>best:best=d;witness=chosen
    return best,witness


def assignment_cost(weights):
    @lru_cache(None)
    def visit(f,used):
        if f==len(weights):return 0
        used=set(used);candidates=[]
        for j,cost in weights[f].items():
            if j in used:continue
            tail=visit(f+1,tuple(sorted(used|{j})))
            if tail is not None:candidates.append(cost+tail)
        return min(candidates) if candidates else None
    return visit(0,())


def beta_retaining_brute(q,lengths,choices,preused):
    # Independently enumerate side, prefix and interval for each fork; this
    # does not consume the edge weights passed to assignment_cost.
    options=[]
    for f in range(q):
        local=[]
        for side in range(2):
            other=lengths[2*f+1-side]+1
            for prefix in range(lengths[2*f+side]+1):
                for j in choices[f,side,prefix]-preused:local.append((j,prefix+other))
        options.append(local)
    best=None
    for selected in itertools.product(*options):
        if len({j for j,c in selected})!=q:continue
        cost=sum(c for j,c in selected)
        if best is None or cost<best:best=cost
    return best


def check(q,lengths,choices,preused,totals):
    data,neighbors,fork_links=model(q,lengths,choices,preused)
    inc=incidence(neighbors);mu=independent_maximum(q,inc)
    delta,witness=hall_deficiency(neighbors)
    assert delta==q-mu
    ordinary=ordinary_flow(*data)
    assert ordinary['value']==q+mu==2*q-delta
    totals['systems']+=1;totals['positive_defects']+=bool(delta)
    totals['defect_sum']+=delta
    if all(len(owners)<=2 for owners in inc.values()):
        tree=allocate(q,inc)
        assert len(tree['deficient'])==delta and len(tree['assignment'])==mu
        totals['two_owner_tree_systems']+=1
        totals['deficient_tree_components']+=len(tree['deficient'])
    # Full replacement with exactly one whole beta per fork has an exact
    # assignment cost. General ordinary flow may use two interval stems.
    weights=[]
    for f in range(q):
        weights.append({j:min(p+lengths[2*f+1-s]+1
            for s in range(2) for p in range(lengths[2*f+s]+1)
            if j in choices[f,s,p]-preused) for j in neighbors[f]})
    cost=assignment_cost(weights)
    assert (cost is None)==bool(delta)
    if not delta:
        assert cost<=fork_links-q
        assert ordinary['cost']<=cost
        totals['beta_retaining_assignments']+=1
        totals['cheaper_unrestricted_ordinary_costs']+=ordinary['cost']<cost
    if q<=3 and sum(len(c) for c in choices.values())<=12:
        assert cost==beta_retaining_brute(q,lengths,choices,preused)
        totals['independent_prefix_cost_enumerations']+=1
    return delta


def optimal_pack_structure(data,full,totals):
    certs=full['certificates'];forks=[i for i,p in enumerate(certs) if p['kind']=='fork']
    owner_cert={o:i for i,p in enumerate(certs) for o in p['owners']}
    used={p['interval']:i for i,p in enumerate(certs) if p['interval'] is not None}
    edges={i:set() for i in forks}
    degree_two=all(sum(j in w for w in data[3].values())<=2 for j in data[4])
    for i in forks:
        f=certs[i];arm=set().union(*(data[3][o] for o in f['owners'] if o!=f['beta']))
        # A free pre-beta unit would replace this fork and lower link cost.
        assert arm<=set(used) and all(used[j]!=i for j in arm)
        edges[i]={used[j] for j in arm if used[j] in forks}
        if degree_two:
            external=[]
            for j in arm:
                outside={o for o,w in data[3].items() if j in w and o not in f['owners']}
                assert len(outside)==1
                o=next(iter(outside));assert owner_cert[o]==used[j]
                external.append(o)
            assert len(external)==len(set(external))
            totals['two_owner_optimal_fork_injections']+=1
    # A directed cycle provides a simultaneous old-fork-interval swap,
    # replacing every cycle fork while preserving the other certificates.
    todo=set(forks)
    while todo:
        sinks={i for i in todo if not edges[i]&todo}
        assert sinks
        todo-=sinks
    if forks:
        sinks={i for i in forks if not edges[i]}
        assert sinks
        ordinary_used={j for j,i in used.items() if i not in forks}
        for i in sinks:
            f=certs[i]
            arm=set().union(*(data[3][o] for o in f['owners'] if o!=f['beta']))
            assert arm<=ordinary_used
        totals['optimal_fork_DAGs']+=1
        totals['ordinary_blocked_sink_forks']+=len(sinks)


def fixed_pack_bound(data,totals):
    full=optimize(*data);ordinary=ordinary_flow(*data)
    optimal_pack_structure(data,full,totals)
    fs=[p for p in full['certificates'] if p['kind']=='fork']
    ks=[p for p in full['certificates'] if p['kind']!='fork']
    used={p['interval'] for p in ks if p['interval'] is not None}
    neighbors=[set().union(*(data[3][o] for o in f['owners'] if o!=f['beta']))-used for f in fs]
    delta,_=hall_deficiency(neighbors)
    assert full['value']-ordinary['value']<=delta
    if delta==0 and fs:
        # Such a packing can preserve value and strictly lower link cost;
        # it cannot be the lexicographic whole-support optimum.
        raise AssertionError('Minimum-link maximum packing has an eliminable fork pack')
    totals['whole_network_pack_bounds']+=1
    totals['whole_network_optima_with_forks']+=bool(fs)
    totals['strict_unrestricted_gaps']+=full['value']>ordinary['value']
    totals['positive_fixed_pack_bound_but_no_value_gap']+=delta>0 and full['value']==ordinary['value']


def direct_token_bounds(current,bands,data,meta,chosen,totals):
    # Original-alpha injection only; no C0 or mixed internal arms accepted.
    original,_,_,interval_owner,kinds,pairs,ports=terminal_data(current,bands)
    injection=dict(inject(current,bands,Counter(),True)['assignment'])
    owner,alphas,betas,mixed=owner_data(kinds,pairs)
    token_rows=[]
    for a,c,b in chosen:
        row=[]
        for source in (a,c):
            assert source in alphas
            for tip in pairs[source]:
                if ports[tip]:
                    js={interval_owner[p] for p in ports[tip]}
                    j=min(js,key=lambda j:(j in meta['boundary'],j))
                    kind='mark' if j in meta['boundary'] else 'interval'
                    assert kind=='mark' or j in data[3][source]
                    row.append((kind,j))
                else:
                    bp=injection[tip];o=owner[bp]
                    row.append(('beta' if o in betas else 'mixed',o))
        assert len(row)==4;token_rows.append(row)
    counts=Counter(d for row in token_rows for d in row)
    assert all(n<=(2 if k in ('interval','beta') else 1) for (k,j),n in counts.items())
    arm_units=set().union(*(data[3][a]|data[3][c] for a,c,b in chosen))
    policies=[set(),set(arm_units),{j for j in arm_units if j%2==0}]
    for blocked in policies:
        for mask in range(1,1<<len(chosen)):
            selected=[i for i in range(len(chosen)) if mask>>i&1]
            internal_beta={chosen[i][2] for i in selected}
            n=set().union(*(data[3][chosen[i][0]]|data[3][chosen[i][1]] for i in selected))-blocked
            ds={d for i in selected for d in token_rows[i]}
            bo={j for k,j in ds if k=='beta' and j not in internal_beta}
            used={j for k,j in ds if k=='interval' and j in blocked}
            mix={j for k,j in ds if k=='mixed'};marks={j for k,j in ds if k=='mark'}
            assert 2*(len(selected)-len(n))<=2*len(bo)+2*len(used)+len(mix)+len(marks)
            totals['direct_fork_physical_token_inequalities']+=1
            totals['positive_direct_fork_blocked_defects']+=len(selected)>len(n)


def physical(q,totals):
    current=stacked(q);data,meta,_=whole_support_data(current,whole_bands(current))
    owners,_,_,mixed=owner_data(*data[:2]);allowed=set(mixed);units=set();neighbors=[];chosen=[]
    for i in range(q):
        move=lambda v:(v[0]+16*i,v[1])
        a,c,b=(owners[move(v[0])] for v in (A,C,B))
        chosen.append((a,c,b))
        allowed|={a,c,b};units.add(meta['owner'][4+8*i,7])
        neighbors.append(data[3][a]|data[3][c])
    inc=incidence(neighbors);mu=independent_maximum(q,inc)
    assert mu==q and hall_deficiency(neighbors)[0]==0
    assert len(allocate(q,inc)['deficient'])==0
    reserved=restrict(data,allowed,units)
    reserved_neighbors=[n&units for n in neighbors]
    assert hall_deficiency(reserved_neighbors)[0]==q
    assert ordinary_flow(*reserved)['value']==q
    assert ordinary_flow(*data)['value']==3*q
    direct_token_bounds(current,whole_bands(current),data,meta,chosen,totals)
    totals['physical_stack_lifts']+=1
    return dict(copies=q,full_arm_matching=mu,full_arm_defect=0,
                reserved_arm_matching=0,reserved_arm_defect=q)


def blocking_chain(q,totals):
    kinds,pairs,_=canonical('AAB'*q+'A');links=[]
    support={o:set() for o in range(3*q+1)};resources=set(range(q+1))
    for i in range(q):
        links.extend([(6*i,6*i+4),(6*i+2,6*i+5)])
        support[3*i+2]={i}
        support[3*i]={i+1}  # Last arm sees interval q, used by outside D.
    support[3*q]={q}
    data=(kinds,pairs,links,support,resources)
    ordinary=ordinary_flow(*data)
    assert (ordinary['value'],ordinary['cost'])==(2*q,q)
    # Explicit all-fork+outside-interval certificate meets the source bound.
    assert evaluate(*data)['value']==2*q+1
    if q<=6:
        full=optimize(*data)
        assert (full['value'],full['cost'])==(2*q+1,2*q)
        assert len([p for p in full['certificates'] if p['kind']=='fork'])==q
        optimal_pack_structure(data,full,totals)
        totals['independent_chain_optima']+=1
    totals['abstract_blocking_chains']+=1
    return dict(forks=q,ordinary_value=2*q,ordinary_min_links=q,
                full_value=2*q+1,full_min_links=2*q,global_gap=1)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter()
    for q,r in [(1,3),(2,2),(3,1)]:
        for mask in range(1<<(2*q*r)):
            choices={(f,s,0):{j for j in range(r) if mask>>(r*(2*f+s)+j)&1}
                     for f in range(q) for s in range(2)}
            check(q,[0]*(2*q),choices,set(),totals)
    rng=random.Random(20261026)
    for _ in range(600):
        q=rng.randrange(1,5);r=rng.randrange(1,6)
        lengths=[rng.randrange(3) for _ in range(2*q)]
        # Include beta-body units of other forks as arm candidates. Those
        # identities are released simultaneously, not only one fork at a time.
        pool=list(range(r))+list(range(-q,0))
        choices={(f,s,p):{j for j in pool if rng.randrange(6)==0}
                 for f in range(q) for s in range(2) for p in range(lengths[2*f+s]+1)}
        preused={j for j in range(r) if rng.randrange(4)==0}
        check(q,lengths,choices,preused,totals)
    # Distinct representatives can swap old fork intervals across forks.
    swapped={(f,s,0):({-2 if f==0 else -1} if s==0 else set())
             for f in range(2) for s in range(2)}
    assert check(2,[0]*4,swapped,set(),totals)==0
    # A full-network optimum need not be forced into the chosen fork routes.
    for _ in range(250):
        types=['A','A','B']+[rng.choice(['A','B','M']) for _ in range(rng.randrange(3))]
        kinds,pairs,links=canonical(types)
        links=[e for e in links if rng.randrange(3)==0]
        resources=set(range(rng.randrange(1,5)))
        support={o:{j for j in resources if rng.randrange(4)==0} for o in range(len(pairs))}
        fixed_pack_bound((kinds,pairs,links,support,resources),totals)
    # Hall failure for fixed arms can coexist with full-network value equality.
    kinds,pairs,_=canonical('AABMM')
    cost_only=(kinds,pairs,[(0,4),(2,5),(3,6),(7,8)],
               {0:set(),1:set(),2:{0},3:set(),4:{0}},{0})
    fixed_pack_bound(cost_only,totals)
    assert optimize(*cost_only)['value']==ordinary_flow(*cost_only)['value']==2
    assert (optimize(*cost_only)['cost'],ordinary_flow(*cost_only)['cost'])==(2,3)
    # A pre-beta gap with >=2 units sharing one other original owner
    # always leaves a substitute after that owner's single interval payment.
    for m in range(2,14):
        kinds,pairs,_=canonical('AAAB');units=set(range(m))
        data=(kinds,pairs,[(0,6),(2,7)],
              {0:units,1:set(),2:units,3:{m}},units|{m})
        full=optimize(*data);old=ordinary_flow(*data)
        assert (full['value'],full['cost'])==(3,1)
        assert (old['value'],old['cost'])==(3,1)
        assert not any(p['kind']=='fork' for p in full['certificates'])
        totals['capacity_two_or_larger_exclusions']+=1
    # A one-unit PRIVATE arm gap also prevents a minimum-cost optimal fork.
    kinds,pairs,_=canonical('AAB')
    data=(kinds,pairs,[(0,4),(2,5)],{0:{0},1:set(),2:{1}},{0,1})
    full=optimize(*data)
    assert (full['value'],full['cost'])==(2,1)
    assert not any(p['kind']=='fork' for p in full['certificates'])
    totals['private_arm_unit_exclusions']+=1
    # Two independent interval stems beat every beta-retaining replacement
    # in link cost, despite agreeing in maximum payment count.
    choices={(0,0,0):{0},(0,1,0):{1}}
    data,_,_=model(1,[0,0],choices,set())
    assert ordinary_flow(*data)['cost']==0
    assert beta_retaining_brute(1,[0,0],choices,set())==1
    chains=[blocking_chain(q,totals) for q in range(1,13)]
    lifts=[physical(q,totals) for q in range(1,9)]
    result=dict(status='PASS',totals=dict(totals),physical_lifts=lifts,abstract_blocking_chains=chains,
        old_fork_interval_swap_control='PASS_twoForks_reuseReleasedIdentitiesInjectively',
        cost_scope_control=dict(ordinary_value=2,ordinary_min_links=0,beta_retaining_min_links=1),
        scope='General exact fixed-arm deficit and two-owner tree proof written; '
              'beta-retaining full-replacement assignment cost only, not unrestricted mincost. '
              'Whole-network bound, optimal fork DAG and unique external-owner blocking injection tested on maximum-value minimum-link packings. '
              'Physical frozen copies checked in full and declared reserved interfaces; '
              'no unrestricted physical strict gain or general5of6 improvement claimed.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
