"""Beta-body promotion, surplus Hall witnesses and a finite frozen frontier.

General proofs: BETA_CUT_PROMOTION_AND_SHARED_RESERVE_OBSTRUCTION.md.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical,ordinary_flow,whole_support_data,optimize
from check_one_sided_interval_allocation import independent_maximum
from check_frozen_beta_support_fork import fixture
from check_promotion_cores import frozen_certificate
from check_even_bridge_support_completion import endpoints_of
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; do not run with -O.')


def examine(data,totals,compare_smallest=False):
    flow=fork_flow(*data,maximal_cut=True)
    if compare_smallest:
        original=fork_flow(*data)
        assert (original['value'],original['cost'])==(flow['value'],flow['cost'])
        totals['same_optimum_different_cut_controls']+=original['cut']!=flow['cut']
    owner,_,betas,_=owner_data(*data[:2])
    entered=Counter(owner[z[1]] for z in flow['cut'] if z[0]=='tip')
    receivers=sorted(entered);double={b for b,n in entered.items() if n==2}
    assert all(b not in flow['source_side_betas'] for b in receivers)
    outside=data[4]-set(flow['source_side_intervals'])
    neighborhood={b:data[3][b]&outside for b in receivers}
    # Exact cut change for simultaneous body promotion:
    # |Q| + |union W_out(Q)| - sum number_of_cut_entries.
    for bits in range(1,1<<len(receivers)):
        chosen={b for i,b in enumerate(receivers) if bits>>i&1}
        union=set().union(*(neighborhood[b] for b in chosen))
        change=len(chosen)+len(union)-sum(entered[b] for b in chosen)
        assert change>=1
        assert len(union)>=len(chosen&double)+1
        totals['strict_joint_promotion_inequalities']+=1
    ordered=sorted(double)
    inc={j:{i for i,b in enumerate(ordered) if j in neighborhood[b]} for j in outside}
    assert independent_maximum(len(ordered),inc)==len(ordered)
    for deleted in outside:
        assert independent_maximum(len(ordered),{j:ns for j,ns in inc.items() if j!=deleted})==len(ordered)
        totals['single_interval_deletion_matching_controls']+=bool(ordered)
    if double:
        totals['cuts_with_double_BP_receiver']+=1
        totals['double_BP_receivers']+=len(double)
        # Under two-owner support the surplus Hall condition is equivalent
        # to degree>=2 at every beta and no isolated pure cycle component.
        if all(len(ns)<=2 for ns in inc.values()):
            assert all(len(neighborhood[b])>=2 for b in double)
            adjacency={i:set() for i in range(len(ordered))}
            for ns in inc.values():
                if len(ns)==2:
                    a,b=ns;adjacency[a].add(b);adjacency[b].add(a)
            todo=set(adjacency)
            while todo:
                comp={min(todo)};pending=list(comp)
                while pending:
                    a=pending.pop()
                    for b in adjacency[a]-comp:comp.add(b);pending.append(b)
                todo-=comp
                units={j for j,ns in inc.items() if ns&comp}
                assert len(units)>=len(comp)+1
                totals['two_owner_surplus_components']+=1
    totals['canonical_cut_models']+=1
    return flow,dict(receivers=receivers,double_receivers=ordered,
                     far_intervals=sorted(outside),neighborhood={str(b):sorted(ns) for b,ns in neighborhood.items()})


def shared_reserve_chain(q,totals):
    kinds,pairs,_=canonical('AAB'*q);support={o:set() for o in range(3*q)};links=[]
    for i in range(q):
        support[3*i+2]={i,i+1};links.extend([(6*i,6*i+4),(6*i+2,6*i+5)])
    data=(kinds,pairs,links,support,set(range(q+1)))
    flow,cut=examine(data,totals,True);ordinary=ordinary_flow(*data)
    assert (flow['value'],flow['cost'])==(2*q,2*q)
    assert (ordinary['value'],ordinary['cost'])==(q,q)
    assert len(cut['double_receivers'])==q and len(flow['cut'])==2*q
    used={p['interval'] for p in flow['certificates'] if p['interval'] is not None}
    assert len(used)==q and len(data[4]-used)==1
    assert not flow['source_side_betas'] and not flow['source_side_intervals']
    if q<=5:
        exact=optimize(*data);assert (exact['value'],exact['cost'])==(2*q,2*q)
        totals['independent_shared_chain_optima']+=1
    totals['shared_reserve_chain_controls']+=1
    return dict(copies=q,full_value=2*q,ordinary_value=q,double_BP_receivers=q,
                far_side_intervals=q+1,used_intervals=q,globally_unused_intervals=1,
                scalar_margin=1)


def feasible(current):
    try:direct_check(*current)
    except AssertionError:return False
    return True


def finite_frontier(totals):
    base,_=fixture();vertices=endpoints_of(base)
    adjacent={v:{w for w in vertices if sum(abs(a-b) for a,b in zip(v,w))==1} for v in vertices}
    def matchings(left,chosen):
        if not left:yield chosen;return
        v=min(left,key=lambda v:(len(adjacent[v]&left),v))
        for w in sorted(adjacent[v]&left):yield from matchings(left-{v,w},chosen+[(v,w)])
    bases=list(matchings(vertices,[]));assert len(bases)==4
    blank={(r,c) for r in range(16) for c in range(1,13)}-(base[2]|vertices)
    actions=[]
    for v in sorted(blank):
        if feasible((16,14,base[2]|{v},base[3])):actions.append(('T',(v,)))
    for v in sorted(blank):
        for w in sorted(blank):
            if v<w and sum(abs(a-b) for a,b in zip(v,w))==1:
                if feasible((16,14,base[2],base[3]+[(v,w)])):actions.append(('M',(v,w)))
    assert Counter(k for k,vs in actions)=={'T':52,'M':61}
    controls=[];grouped=Counter();examples={}
    selections=[()]+[(a,) for a in actions]+list(itertools.combinations(actions,2))
    for base_index,matching in enumerate(bases):
        for chosen in selections:
            added_vertices=[v for kind,vs in chosen for v in vs]
            if len(added_vertices)!=len(set(added_vertices)):continue
            selected=base[2]|{v for kind,vs in chosen if kind=='T' for v in vs}
            edges=matching+[vs for kind,vs in chosen if kind=='M']
            current=(16,14,selected,edges);totals['frontier_disjoint_edit_sets']+=1
            if not feasible(current):continue
            totals['frontier_feasible_boards']+=1
            frozen,layers=frozen_certificate(current)
            if frozen!=endpoints_of(current):continue
            data,meta,_=whole_support_data(current,whole_bands(current))
            flow,cut=examine(data,totals);ordinary=ordinary_flow(*data)
            _,alphas,betas,_=owner_data(*data[:2])
            margin=len(data[4])+len(betas)-len(alphas)
            kind=''.join(sorted(k for k,vs in chosen)) or 'none'
            key=(base_index,kind,len(alphas),flow['deficit'],
                 flow['value']-ordinary['value'],flow['cost']-ordinary['cost'])
            if not grouped[key]:
                exact=optimize(*data)
                assert (exact['value'],exact['cost'])==(flow['value'],flow['cost'])
                totals['frontier_independent_packing_comparisons']+=1
            grouped[key]+=1
            totals['frontier_fully_frozen_boards']+=1
            totals['frontier_positive_full_deficit']+=flow['deficit']>0
            totals['frontier_strict_fork_value_gain']+=flow['value']>ordinary['value']
            totals['frontier_strict_fork_cost_gain']+=flow['value']==ordinary['value'] and flow['cost']<ordinary['cost']
            totals['frontier_solver_selected_forks']+=any(p['kind']=='fork' for p in flow['certificates'])
            totals['frontier_negative_scalar_margin']+=margin<0
            flags=[]
            if flow['deficit']>0:flags.append('positive_full_deficit')
            if flow['value']>ordinary['value']:flags.append('strict_fork_value_gain')
            if any(z[0]=='tip' for z in flow['cut']):flags.append('BP_entry_cut')
            for flag in flags:
                if flag not in examples:
                    examples[flag]=dict(shape=[16,14],selected=sorted(selected),matching=edges,
                        freezing_layers=layers,edits=chosen,base_matching=base_index,
                        full=flow,ordinary=ordinary,scalar_margin=margin,cut_analysis=cut)
        print(json.dumps(dict(frontier_base_completed=base_index,fully_frozen=totals['frontier_fully_frozen_boards'])),flush=True)
    for key,count in sorted(grouped.items()):
        controls.append(dict(base_matching=key[0],edit_types=key[1],alphas=key[2],
            full_deficit=key[3],full_minus_ordinary_value=key[4],
            full_minus_ordinary_cost=key[5],count=count))
    return dict(base_matchings=4,elementary_feasible_actions={'T':52,'M':61},
                allowed_edit_count=[0,1,2],scope='Fixed16x14_standardBlankBoundary; '
                'fourBasePerfectMatchings; retainBaseTandEachChosenBaseM; add at most '
                'two selections or new matching edges; require full freezing. '
                'All individually feasible actions suffice by monotonicity of feasibility.',
                grouped=controls,first_obstructions=examples)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();rng=random.Random(20261030)
    for i in range(1200):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,7)))
        kinds,pairs,possible=canonical(types);rng.shuffle(possible)
        links=possible[:rng.randrange(min(14,len(possible))+1)]
        resources=set(range(rng.randrange(6)));support={o:set() for o in range(len(pairs))}
        for j in resources:
            for o in rng.sample(range(len(pairs)),rng.randrange(min(2,len(pairs))+1)):support[o].add(j)
        data=(kinds,pairs,links,support,resources)
        examine(data,totals,True)
    chains=[shared_reserve_chain(q,totals) for q in range(1,17)]
    frontier=finite_frontier(totals)
    report=dict(status='PASS',totals=dict(totals),shared_reserve_chains=chains,
                physical_frontier=frontier,
                scope='General strict beta-promotion and surplus Hall proofs written; '
                'finite controls compare canonical cuts, matching after any single interval '
                'deletion and abstract shared-reserve family. Physical edit frontier is '
                'explicitly finite, not a universal compensation proof.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
