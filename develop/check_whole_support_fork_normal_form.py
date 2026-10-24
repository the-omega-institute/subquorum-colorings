"""Exact whole-owner-support compensation normal form, including beta forks.

The all-size normalization proof is in WHOLE_SUPPORT_FORK_NORMAL_FORM.md.
Enumeration is an independent regression check, not a universal proof.
"""
import argparse
from collections import Counter, defaultdict
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_bt_corridor_ports import compile_model
from check_compensation_flow_normal_form import owner_data, solve
from check_endpoint_free_gap_compensation import gap_access
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_one_sided_interval_allocation import independent_maximum
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import all_link_matchings, cancel_pairs

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def primitive_certificates(kinds,pairs,links,support,resources):
    owners,alphas,betas,mixed=owner_data(kinds,pairs)
    assert set(support)==set(range(len(pairs)))
    assert all(set(s)<=resources for s in support.values())
    assert all(kinds[a]=='TP' and kinds[b]=='BP' for a,b in links)
    outgoing=defaultdict(list)
    for a,b in links:
        if owners[a]!=owners[b]:outgoing[owners[a]].append((a,b))
    primitives=[];arms=defaultdict(list)
    def add(kind,path_owners,path_links,interval=None,**extra):
        aa=set(path_owners)&alphas
        primitives.append(dict(kind=kind,owners=tuple(sorted(path_owners)),
            links=tuple(path_links),interval=interval,value=len(aa),**extra))
    def visit(current,path_owners,path_links):
        for j in sorted(support[current]):
            add('interval',path_owners,path_links,j,witness=current)
        for edge in outgoing[current]:
            target=owners[edge[1]]
            if target in path_owners:continue
            next_owners=path_owners|{target};next_links=path_links+[edge]
            if target in betas:
                add('beta',next_owners,next_links,beta=target)
                arms[target].append(dict(owners=next_owners,links=next_links,entry=edge[1]))
            else:
                assert target in mixed
                visit(target,next_owners,next_links)
    for a in sorted(alphas):visit(a,{a},[])
    for beta,choices in arms.items():
        for left,right in itertools.combinations(choices,2):
            if left['entry']==right['entry'] or left['owners']&right['owners']!={beta}:continue
            for j in sorted(support[beta]):
                add('fork',left['owners']|right['owners'],left['links']+right['links'],j,
                    beta=beta,entries=(left['entry'],right['entry']),witness=beta)
    return primitives


def optimize(kinds,pairs,links,support,resources,allow_forks=True):
    _,alphas,_,_=owner_data(kinds,pairs)
    primitives=primitive_certificates(kinds,pairs,links,support,resources)
    if not allow_forks:primitives=[p for p in primitives if p['kind']!='fork']
    rid={j:i for i,j in enumerate(sorted(resources))}
    masks=[(sum(1<<o for o in p['owners']),0 if p['interval'] is None else 1<<rid[p['interval']]) for p in primitives]
    by_alpha={a:[i for i,p in enumerate(primitives) if a in p['owners']] for a in alphas}
    @lru_cache(None)
    def search(occupied,used):
        left=alphas-{a for a in alphas if occupied>>a&1}
        if not left:return 0,0,()
        a=min(left);best=search(occupied|1<<a,used)
        for i in by_alpha[a]:
            om,im=masks[i]
            if om&occupied or im&used:continue
            v,c,chosen=search(occupied|om,used|im)
            proposal=(v+primitives[i]['value'],c+len(primitives[i]['links']),(i,)+chosen)
            if (proposal[0],-proposal[1])>(best[0],-best[1]):best=proposal
        return best
    value,cost,chosen=search(0,0)
    certificates=[primitives[i] for i in chosen]
    selected=[e for p in certificates for e in p['links']]
    evaluated=evaluate(kinds,pairs,selected,support,resources)
    assert (evaluated['value'],len(selected))==(value,cost)
    used_owners=[o for p in certificates for o in p['owners']]
    assert len(used_owners)==len(set(used_owners))
    used_i=[p['interval'] for p in certificates if p['interval'] is not None]
    assert len(used_i)==len(set(used_i))
    return dict(value=value,cost=cost,certificates=certificates,primitive_count=len(primitives))


def ordinary_flow(kinds,pairs,links,support,resources,removed=frozenset()):
    """Owner-support counting arcs; these are NOT physical free-tip accesses."""
    owners,_,_,_=owner_data(kinds,pairs)
    kept=[pair for o,pair in enumerate(pairs) if o not in removed]
    free={v for pair in kept for v in pair}
    access={v:support[owners[v]]&resources for v in free if kinds[v]=='TP'}
    return solve({v:kinds[v] for v in free},kept,
        [e for e in links if set(e)<=free],access,resources)


def optimize_by_forks(kinds,pairs,links,support,resources):
    forks=[p for p in primitive_certificates(kinds,pairs,links,support,resources) if p['kind']=='fork']
    best=None;packs=0
    def visit(first,used,intervals,chosen,selected):
        nonlocal best,packs
        packs+=1
        ordinary=ordinary_flow(kinds,pairs,links,support,resources-intervals,used)
        value=2*len(chosen)+ordinary['value'];cost=len(selected)+ordinary['cost']
        candidate=dict(value=value,cost=cost,forks=list(chosen),
            links=list(selected)+ordinary['links'],ordinary_value=ordinary['value'])
        if best is None or (value,-cost)>(best['value'],-best['cost']):best=candidate
        for i in range(first,len(forks)):
            f=forks[i]
            if used&set(f['owners']) or f['interval'] in intervals:continue
            visit(i+1,used|set(f['owners']),intervals|{f['interval']},chosen+[f],selected+list(f['links']))
    visit(0,set(),set(),[],[])
    assert evaluate(kinds,pairs,best['links'],support,resources)['value']==best['value']
    best['fork_packs_checked']=packs
    return best


def evaluate(kinds,pairs,selected,support,resources):
    owners,_,betas,_=owner_data(kinds,pairs)
    _,inventory,components=cancel_pairs(kinds,list(pairs),list(selected),Counter())
    alphas=[c for c in components if not c['cycle'] and c['alpha']==c['beta']+1]
    incidence={j:set() for j in resources}
    for a,component in enumerate(alphas):
        choices=set().union(*(support[o] for o in {owners[v] for v in component['vertices']}))
        for j in choices:incidence[j].add(a)
    return dict(value=len(betas)-inventory['BP','BP']+independent_maximum(len(alphas),incidence),
                remaining_beta=inventory['BP','BP'],incidence=incidence)


def brute(kinds,pairs,links,support,resources):
    best=(0,0);count=0
    for selected in all_link_matchings(links):
        count+=1;result=evaluate(kinds,pairs,selected,support,resources)
        proposal=result['value'],len(selected)
        if (proposal[0],-proposal[1])>(best[0],-best[1]):best=proposal
    return best,count


def verify(kinds,pairs,links,support,resources,totals):
    answer=optimize(kinds,pairs,links,support,resources)
    expected,count=brute(kinds,pairs,links,support,resources)
    assert (answer['value'],answer['cost'])==expected
    ordinary=optimize(kinds,pairs,links,support,resources,False)
    flow=ordinary_flow(kinds,pairs,links,support,resources)
    assert (flow['value'],flow['cost'])==(ordinary['value'],ordinary['cost'])
    compiled=optimize_by_forks(kinds,pairs,links,support,resources)
    assert (compiled['value'],compiled['cost'])==expected
    totals['fork_pack_flow_comparisons']+=1
    totals['fork_packs_checked']+=compiled['fork_packs_checked']
    _,alphas,betas,_=owner_data(kinds,pairs)
    incidence={j:{b for b in betas if j in support[b]} for j in resources}
    bid={b:i for i,b in enumerate(sorted(betas))}
    rho=independent_maximum(len(betas),{j:{bid[b] for b in bs} for j,bs in incidence.items()})
    assert 0<=answer['value']-ordinary['value']<=min(rho,len(alphas)//2)
    totals['systems']+=1;totals['independent_terminal_matchings']+=count
    totals['strict_fork_cardinality_gains']+=answer['value']>ordinary['value']
    totals['strict_fork_cost_gains']+=answer['value']==ordinary['value'] and answer['cost']<ordinary['cost']
    totals['optima_using_forks']+=any(p['kind']=='fork' for p in answer['certificates'])
    return answer


def canonical(types):
    kinds={};pairs=[]
    for o,t in enumerate(types):
        pair=(2*o,2*o+1);pairs.append(pair)
        for p,k in zip(pair,{'A':('TP','TP'),'B':('BP','BP'),'M':('BP','TP')}[t]):kinds[p]=k
    links=[(a,b) for a in kinds for b in kinds if kinds[a]=='TP' and kinds[b]=='BP']
    return kinds,pairs,links


def whole_support_data(current,bands):
    data,meta=compile_model(current,bands,Counter())
    kinds,pairs,links,_,resources=data;owners,_,_,_=owner_data(kinds,pairs)
    support={o:set() for o in range(len(pairs))};nodes={};witness={}
    for c in meta['original']['components']:
        if c['kind']==['cycle']:continue
        b,col=c['nodes'][0];tip=next(v for v in bands[b][col] if v in owners)
        for node in c['nodes']:nodes[node]=owners[tip]
    _,_,_,rr,_,_,gaps=gap_access(current,bands,Counter());assert rr==resources
    for g in gaps:
        units={j for j in resources if meta['intervals'][j]['band']==g['band'] and g['first']<=meta['intervals'][j]['first']<=g['last']}
        for col in (g['first']-1,g['last']+1):
            owner=nodes.get((g['band'],col))
            if owner is None:continue
            support[owner]|=units
            for j in units:witness[owner,j]=(g['band'],col)
    assert all(sum(j in choices for choices in support.values())<=2 for j in resources)
    return (kinds,pairs,links,support,resources),meta,witness


def contract(data,fixed):
    kinds,pairs,links,support,resources=data
    assert all(e in links for e in fixed)
    owners,_,_,_=owner_data(kinds,pairs)
    reduced,_,records=cancel_pairs(kinds,pairs,fixed,Counter())
    free={v for pair in reduced for v in pair};new_support={}
    for o,pair in enumerate(reduced):
        component=next(c for c in records if set(c['ends'])==set(pair))
        source_owners={owners[v] for v in component['vertices']}
        new_support[o]=set().union(*(support[a] for a in source_owners))
    return ({v:kinds[v] for v in free},reduced,[e for e in links if set(e)<=free],new_support,resources)


def physical_controls(totals):
    from check_compensation_flow_geometry_frontier import pad_image
    from check_even_bridge_support_completion import endpoints_of
    from check_exchange_terminal_nonunique import fixture as bent, matching_orders, graft
    from check_frozen_support_tree_reroot import fixture as tree, model_at
    from check_frozen_first_destination_allocation import fixture as unported
    from check_frozen_shared_mixed_gate import fixture as shared
    from check_whole_support_donor_collision import sealed
    from degree_three_fusion import occupied_bands
    from rotor_networks import rotor,combine,star_modules,transform_module
    base=bent()
    sources=[('bent'+str(i),(*base[:3],list(r['matching']))) for i,r in enumerate(matching_orders())]
    sources += [('graft',graft(6,4)),('occupied',occupied_bands(6)[0])]
    module=rotor();sources += [('rotor',(6,6,module['selected'],module['matching']))]
    for width in (6,10):
        net=combine([transform_module(m,(False,False,False),(width-2,width-2)) for m in star_modules(width)])
        sources += [('star'+str(width),(2*width+2,2*width+2,net['selected'],net['matching']))]
    records=[]
    def check(name,current,bands,fixed=()):
        direct_check(*current)
        assert frozen_certificate(current)[0]==endpoints_of(current)
        data,_,_=whole_support_data(current,bands);virtual=contract(data,list(fixed))
        answer=optimize_by_forks(*virtual)
        _,_,betas,_=owner_data(*virtual[:2])
        _,_,after,_,_,_=model_at(current,bands,list(fixed)+answer['links'])
        assert answer['value']==len(betas)-after['beta']+after['paid']
        if len(virtual[2])<=16:
            expected,count=brute(*virtual)
            assert (answer['value'],answer['cost'])==expected
            totals['physical_independent_terminal_matchings']+=count
            totals['physical_exhaustive_optimum_comparisons']+=1
        forks=[p for p in primitive_certificates(*virtual) if p['kind']=='fork']
        totals['physical_systems']+=1
        totals['physical_systems_with_feasible_forks']+=bool(forks)
        totals['physical_fork_value_gains']+=answer['value']>ordinary_flow(*virtual)['value']
        records.append(dict(family=name,fixed_links=len(fixed),value=answer['value'],cost=answer['cost'],feasible_forks=len(forks)))
    for (name,raw),sym,offset in itertools.product(sources,itertools.product((False,True),repeat=3),itertools.product((2,3),repeat=2)):
        current=pad_image(raw,sym,offset);check(name,current,whole_bands(current))
    for name,current in [('tree',tree()[0]),('unported',unported()[0]),('shared',shared())]:
        bands=whole_bands(current);data,_,_=whole_support_data(current,bands)
        for fixed in all_link_matchings(data[2]):check(name,current,bands,fixed)
    for width in (8,12):
        current,bands=sealed(width)
        for extra in ([],[((5,7),(5,8))],[((5,15),(5,14))],[((5,7),(5,8)),((5,15),(5,14))]):
            check('whole_support_collision'+str(width),current,bands,[((5,5),(5,6))]+extra)
    grouped=Counter((r['family'],r['fixed_links'],r['value'],r['cost'],r['feasible_forks']) for r in records)
    return [dict(family=key[0],fixed_links=key[1],value=key[2],cost=key[3],
                 feasible_forks=key[4],count=count) for key,count in sorted(grouped.items())]


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter()
    for types in ('AAB','AMB','AAM','ABB','AMM'):
        kinds,pairs,possible=canonical(types)
        for bits in range(1<<len(possible)):
            links=[e for i,e in enumerate(possible) if bits>>i&1]
            for access in range(1<<len(pairs)):
                support={o:({0} if access>>o&1 else set()) for o in range(len(pairs))}
                verify(kinds,pairs,links,support,{0},totals)
    randomizer=random.Random(20261025)
    for case in range(400):
        types='AA'+''.join(randomizer.choice('ABM') for _ in range(randomizer.randrange(1,5)))
        kinds,pairs,possible=canonical(types);randomizer.shuffle(possible)
        links=possible[:randomizer.randrange(min(len(possible),11)+1)]
        resources=set(range(randomizer.randrange(4)))
        support={o:{j for j in resources if randomizer.randrange(2)} for o in range(len(pairs))}
        verify(kinds,pairs,links,support,resources,totals)
        if case<24:
            for selected in all_link_matchings(links):
                normalized=optimize_by_forks(kinds,pairs,selected,support,resources)
                before=evaluate(kinds,pairs,selected,support,resources)['value']
                assert normalized['value']>=before
                assert set(normalized['links'])<=set(selected)
                totals['subset_normalization_checks']+=1
    # Cardinality can stay fixed while the exact minimum number of links falls.
    kinds,pairs,_=canonical('AABMM')
    support={0:set(),1:set(),2:{0},3:set(),4:{0}}
    cost_control=verify(kinds,pairs,[(0,4),(2,5),(3,6),(7,8)],support,{0},totals)
    assert (cost_control['value'],cost_control['cost'])==(2,2)
    ordinary=ordinary_flow(kinds,pairs,[(0,4),(2,5),(3,6),(7,8)],support,{0})
    assert (ordinary['value'],ordinary['cost'])==(2,3)
    # The beta supplies one consumption unit, and its support supplies one
    # DIFFERENT interval unit only when both distinct BP ports are entered.
    kinds,pairs,_=canonical('AAB');links=[(0,4),(2,5)];support={0:set(),1:set(),2:{0}}
    positive=verify(kinds,pairs,links,support,{0},totals)
    assert (positive['value'],positive['cost'])==(2,2)
    assert optimize(kinds,pairs,links,support,{0},False)['value']==1
    assert positive['certificates'][0]['kind']=='fork'
    # Both arms at the same BP are illegal; an unbacked beta-to-I transit
    # cannot turn its internal support into an alpha payment.
    for bad_links in ([(0,4)],[(0,4),(2,4)]):
        assert verify(kinds,pairs,bad_links,support,{0},totals)['value']==1
    for q in range(1,7):
        kinds,pairs,_=canonical('AAB'*q);links=[]
        support={o:set() for o in range(3*q)}
        for i in range(q):
            links.extend([(6*i,6*i+4),(6*i+2,6*i+5)])
            support[3*i+2]={i}
        result=verify(kinds,pairs,links,support,set(range(q)),totals)
        assert (result['value'],result['cost'])==(2*q,2*q)
        assert ordinary_flow(kinds,pairs,links,support,set(range(q)))['value']==q
        totals['abstract_sharp_stack_controls']+=1
    physical=physical_controls(totals)
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),physical=physical,
        minimal_abstract_fork=positive,
        minimum_cost_fork_control=cost_control,
        scope='Exact general whole-owner-support stem/fork normalization and minimum links; '
              'independent terminal-matching/allocation and fork-pack/residual-flow comparisons. '
              'Physical all-C0 lifts and frontier controls contain zero feasible forks; '
              'strict fork gains are abstract, not claimed frozen-grid realizations. '
              'General normalization and physical adapter proofs are written.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
