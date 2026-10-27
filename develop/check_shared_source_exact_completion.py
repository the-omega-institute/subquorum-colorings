"""Whole outer completions and arbitrary-rematching weighted exactness controls."""
from collections import Counter
from pathlib import Path
import json
import random
from shared_source_exact_completion import solve_shared_source,outer_near_matching,expose_outer_white
from shared_hole_chambers import shared_hole_chambers
from check_unbounded_hole_relay import family as core_family
from check_mixed_terminal_compensation import all_matchings,neighbours,edge,mates
from check_general_square_ports import physical_state
from strip_tree_compensation import physical_state_linear
from terminal_source_budget import terminal_source_budget
from check_corner_relay_shortest_path import flip_rematching

if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def forward_distance(f,m,weights,which):
    first={v for v in f['P'] if v[1]<4*f['k']+2};p=first if which==0 else f['P']-first
    centre=f['first_centre'] if which==0 else f['second_centre']
    targets={v for v in f['T'] if neighbours(v)&p};allowed=p|targets|{centre};arcs=[]
    for a,b in sorted(m):
        if a not in p:continue
        black,white=(a,b) if sum(a)%2==0 else (b,a)
        arcs.append((black,white,weights[edge(a,b)]))
    for white in sorted(v for v in allowed if sum(v)%2):
        arcs.extend((white,black,0) for black in sorted(neighbours(white)&allowed) if edge(white,black) not in m)
    distance={v:0 for v in targets}
    for _ in range(len(allowed)-1):
        changed=False
        for a,b,cost in arcs:
            if a in distance and (b not in distance or distance[b]>distance[a]+cost):
                distance[b]=distance[a]+cost;changed=True
        if not changed:break
    assert centre in distance
    return distance[centre]


def generic_budget(f,m,weights):
    board=f['board'];p=set(mates(board,m));q=board-p;directed={v:[] for v in board};cost={}
    for a,b in sorted(m):
        black,white=(a,b) if sum(a)%2==0 else (b,a)
        directed[black].append(white);cost[black,white]=weights[edge(a,b)]
    for white in sorted(v for v in board if sum(v)%2):
        directed[white].extend(b for b in sorted(neighbours(white)&board) if edge(white,b) not in m)
    return terminal_source_budget(board,directed,f['T'],{f['white_hole']},{v for v in q if sum(v)%2==0},cost)


def outer_controls():
    rows=[]
    for k,l in [(1,1),(2,1),(2,2),(3,1),(3,2),(3,3),(4,1),(4,3)]:
        d=outer_near_matching(k,l);white=sorted(v for v in d['region'] if sum(v)%2)
        for target in white:
            matching,path=expose_outer_white(d,target)
            assert set(mates(d['region'],matching))==d['region']-{target}
            assert len(path)==len(set(path)) and len(path)%2==1
        rows.append(dict(K=k,l=l,outer_vertices=len(d['region']),all_white_deletions=len(white)))
    return rows


def exhaustive_rematchings():
    f=shared_hole_chambers(1,1);raw=[set(m) for m in all_matchings(core_family(1)['P'])]
    assert len(raw)==196
    move=lambda v:(v[0]+4,v[1]+6)
    right=[{edge(move(a),move(b)) for a,b in m} for m in raw]
    left_reference=[forward_distance(f,m,{e:1 for e in m},0) for m in raw]
    right_reference=[forward_distance(f,m,{e:1 for e in m},1) for m in right]
    fees=Counter();choices=Counter();count=0
    for i,a in enumerate(raw):
        for j,b in enumerate(right):
            m=a|b;result=solve_shared_source(1,1,m)
            reference=min(left_reference[i],right_reference[j])
            state=physical_state(f['board'],m,result['auxiliary'],f['T'])
            assert len(state['paid'])==result['minimum_TH_fee']==reference
            assert result['relay_costs']==[left_reference[i],right_reference[j]]
            assert state['paid']==result['TH_relay']['actual']
            assert state['data']['counts'][0]==0 and state['data']['counts'][1]==1
            fees[reference]+=1;choices[result['chosen_paid_core']]+=1;count+=1
        if i%49==0:print('exhaustive pairs checked',count,flush=True)
    return dict(single_core_rematchings=len(raw),all_actual_rematching_pairs=count,
                unit_optimum_histogram=dict(sorted(fees.items())),paid_core_histogram=dict(sorted(choices.items())),
                independent_forward_reference_values=2*len(raw),
                scope='ALL actual rematchings of both k=l=1 footprints, unit weights. Every returned full N rescored by older independent physical decomposition; fees compared to cached forward Bellman-Ford distances. Does not enumerate full N or all weight vectors.')


def transpose_parts(m,k):
    n=4*k+2
    def move(v):
        r,c=v
        return (c,r) if c<n else (4*k+c-n,n+r-4*k)
    return {edge(move(a),move(b)) for a,b in m}


def weighted_controls():
    rng=random.Random(27102319);rows=[]
    for k,l in [(1,1),(2,1),(2,2),(3,1),(3,2),(4,1)]:
        f=shared_hole_chambers(k,l)
        for variant in range(8):
            m=flip_rematching(f['M'],f['P'],rng,100*(variant+1))
            if variant%2:m=transpose_parts(m,k)
            weights={e:rng.randrange(20) for e in sorted(m)}
            if variant==0:weights={e:1 for e in m}
            elif variant==1:weights={e:0 for e in m}
            elif variant==2:weights={e:10**400+3*j for j,e in enumerate(sorted(m))}
            elif variant==3:weights={e:0 if e[0][1]<4*k+2 else 7 for e in m}
            elif variant==4:weights={e:1 if e[0][1]<4*k+2 else 100 for e in m}
            elif variant==5:weights={e:100 if e[0][1]<4*k+2 else 1 for e in m}
            result=solve_shared_source(k,l,m,weights)
            reference=[forward_distance(f,m,weights,i) for i in (0,1)]
            assert result['relay_costs']==reference
            budget=generic_budget(f,m,weights)
            assert budget['lower_bound']==result['minimum_TH_fee']==min(reference)
            phi=budget['potential'];assert all(c+phi[a]-phi[b]>=0 for a,b,cap,c in budget['residual_arcs'] if cap)
            state=physical_state(f['board'],m,result['auxiliary'],f['T'])
            assert sum(weights[e] for e in state['paid'])==result['minimum_TH_fee']
            assert state['paid']==result['TH_relay']['actual']
            hh=[p for p in state['data']['paths'] if p['kind']=='HH'];assert len(hh)==1
            assert f['white_hole'] in [hh[0]['vertices'][0],hh[0]['vertices'][-1]]
            assert state['data']['counts'][0]==0
            if variant in (3,4):assert result['chosen_paid_core']==0
            if variant==5:assert result['chosen_paid_core']==1
            rows.append(dict(K=k,l=l,variant=variant,changed_M=m!=f['M'],
                             rho=reference,exact_TH_fee=result['minimum_TH_fee'],
                             paid_core=result['chosen_paid_core'],budget_lower=budget['lower_bound'],
                             HH_actual_expense=sum(weights[e] for e in hh[0]['M']),
                             paid_edges=len(state['paid']),outer_exchange_edges=len(result['outer_exchange'])-1))
    return rows


def large_controls():
    rows=[]
    for k,l in [(16,1),(16,8),(32,1),(32,16)]:
        f=shared_hole_chambers(k,l);r=solve_shared_source(k,l)
        assert r['relay_costs']==[k,l] and r['minimum_TH_fee']==l
        state=physical_state_linear(f['board'],r['M'],r['auxiliary'],r['T'])
        assert len(state['paid'])==l
        rows.append(dict(K=k,l=l,height=f['height'],width=f['width'],exact_TH_fee=l))
    return rows


def main():
    outer=outer_controls();exhaustive=exhaustive_rematchings();weighted=weighted_controls();large=large_controls()
    out=dict(status='PASS',outer=outer,exhaustive=exhaustive,weighted=weighted,large=large,
             all_white_outer_deletion_checks=sum(r['all_white_deletions'] for r in outer),
             weighted_rematching_models=len(weighted),changed_weighted_matchings=sum(r['changed_M'] for r in weighted),
             generic_weighted_source_budget_comparisons=len(weighted),
             scope='All white outer deletions on eight footprints; all 196x196 actual M pairs at K=l=1 under unit weights; independent forward Bellman-Ford, old tagged decomposition and 48 weighted generic HH-budget comparisons including zero and 401-digit weights; large canonical boards.',
             proof_scope='Any-rematching, nonnegative-real-weight exactness follows from the written odd-square relay existence, whole outer deletion lemma and simultaneous physical completion. Finite checks are implementation validation. No generic shortest-path novelty, Lean or universal numerical-bound improvement.')
    (ROOT/'output/shared-source-exact-completion.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','all_white_outer_deletion_checks','weighted_rematching_models','changed_weighted_matchings','generic_weighted_source_budget_comparisons']}),flush=True)
    print(json.dumps(exhaustive),flush=True)


if __name__=='__main__':main()
