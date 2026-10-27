"""Independent physical path enumeration and full matching controls.

The arbitrary-size dichotomy and all-K family are written proofs, not
inferences from these finite controls. The fixed fixture contains explicit M,N.
"""
from itertools import combinations
from pathlib import Path
import json
import random

from two_th_path_bound import two_path_relaxation,certify_two_path_bound
from branched_source_obstruction import branched_family,weighted_obstruction
from check_corner_relay_shortest_path import flip_rematching
from check_general_square_ports import physical_state
from check_mixed_terminal_compensation import all_matchings,edge,grid,mates,neighbours,selected_feasible

if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def enumerate_physical_paths(board,m,t,weights):
    """Independent DFS on physical alternating paths; no flow graph import."""
    mm=mates(board,m);q=board-set(mm);paths=[]
    def visit(path,actual):
        v=path[-1]
        if len(path)>1 and v in q:
            if actual:paths.append((frozenset(path),frozenset(actual),v,sum(weights[e] for e in actual)))
            return
        if sum(v)%2:
            options=[z for z in neighbours(v)&board if mm.get(v)!=z]
        else:
            options=[mm[v]] if v in mm else []
        for z in options:
            if z in path:continue
            e=edge(v,z);visit(path+[z],actual|({e} if e in m else set()))
    for start in sorted(t):visit([start],set())
    return paths


def independent_pair_minimum(paths,centres):
    costs=[a[3]+b[3] for a,b in combinations(paths,2)
           if not a[0]&b[0] and (centres is None or a[2] in centres or b[2] in centres)]
    return min(costs) if costs else None


def check_pair(result,board,m,t,weights,centres):
    occupied=set();total=0
    for path in result['paths']:
        vs=path['vertices'];assert vs[0] in t and vs[-1] not in set(mates(board,m)) and sum(vs[-1])%2==0
        assert len(vs)==len(set(vs)) and not occupied&set(vs);occupied|=set(vs)
        actual={edge(vs[i],vs[i+1]) for i in range(1,len(vs)-1,2)}
        assert actual and actual==path['actual'] and actual<=m
        assert all(b in neighbours(a) for a,b in zip(vs,vs[1:]))
        assert all(edge(vs[i],vs[i+1]) not in m for i in range(0,len(vs)-1,2))
        assert path['cost']==sum(weights[e] for e in actual);total+=path['cost']
    assert len(result['paths'])==result['value']
    if result['minimum'] is not None:
        assert result['value']==2 and total==result['minimum']
        assert centres is None or any(p['vertices'][-1] in centres for p in result['paths'])
    else:assert result['value']<2 and result['cut_capacity']==result['value']
    phi=result['potential']
    assert all(c+phi[a]-phi[b]>=0 for a,b,cap,c in result['residual_arcs'] if cap)


def small_path_controls():
    rng=random.Random(271027812);models=flow_comparisons=paths_count=infinite=quota_strict=0
    for h,w in [(2,2),(2,3),(3,4)]:
        board=grid(h,w)
        for full in all_matchings(board):
            full=sorted(full)
            masks=range(1<<len(full)) if len(full)<=3 else sorted({rng.randrange(1<<len(full)) for _ in range(12)})
            for mask in masks:
                m={e for i,e in enumerate(full) if mask>>i&1};q=board-set(mates(board,m))
                whites=sorted(v for v in q if sum(v)%2);black={v for v in q if sum(v)%2==0}
                for selection in range(3):
                    t=set(whites) if selection==0 else {v for v in whites if rng.randrange(2)}
                    weights={e:(0 if selection==1 else rng.randrange(8)) for e in sorted(m)}
                    if models%13==0:weights={e:10**400+5*i for i,e in enumerate(sorted(m))}
                    paths=enumerate_physical_paths(board,m,t,weights);paths_count+=len(paths);models+=1
                    previous=None
                    for centres in [None,set(),set(sorted(black)[:1]),black]:
                        expected=independent_pair_minimum(paths,centres)
                        got=two_path_relaxation(board,m,t,weights,centres)
                        assert got['minimum']==expected,(h,w,m,t,centres,expected,got)
                        check_pair(got,board,m,t,weights,centres);flow_comparisons+=1;infinite+=expected is None
                        if centres is None:previous=expected
                        elif previous is not None and (expected is None or expected>previous):quota_strict+=1
    return dict(physical_models=models,independent_paths=paths_count,flow_comparisons=flow_comparisons,
                infinite_pair_minima=infinite,strict_centre_quota_controls=quota_strict,
                scope='All actual submatchings of all full 2x2 and 2x3 matchings; sampled subsets of each full 3x4 matching, three source/weight variants, four centre quotas. Pair reference enumerates simple physical paths independently.')


def full_matching_controls():
    board=grid(4,4);m={edge((0,1),(0,2)),edge((1,0),(2,0))};p=set(mates(board,m))
    t={v for v in board-p if sum(v)%2};centres=[(0,0)]
    assert selected_feasible(p,t)
    full=[set(n) for n in all_matchings(board)];comparisons=0;rows=[]
    for weights in [{e:a for e,a in zip(sorted(m),values)} for values in [(0,0),(0,1),(1,0),(1,1),(2,7),(10**400,3)]]:
        result=certify_two_path_bound(board,m,t,[p],centres,weights);fees=[]
        for n in full:
            state=physical_state(board,m,n,t);fee=sum(weights[e] for e in state['paid']);fees.append(fee)
            assert result['lower_bound']<=fee;comparisons+=1
            th=[path for path in state['data']['paths'] if path['kind']=='TH' and path['M']]
            normal=(len(th)==1 and bool({th[0]['vertices'][0],th[0]['vertices'][-1]}&set(centres)))
            assert normal or len(th)>=2
        optimum=min(fees)
        assert result['normal_form_upper']>=optimum
        if result['global_optimum_certified']:assert result['minimum_TH_fee']==optimum
        rows.append(dict(weights=sorted(weights.values()),true_enumerated_optimum=optimum,certified_lower=result['lower_bound'],upper=result['normal_form_upper']))
    # Enforce the additional hypothesis instead of silently applying the theorem.
    rejected=False
    try:certify_two_path_bound(grid(2,2),set(),{(0,1),(1,0)},[set()],[(0,0)])
    except ValueError as e:rejected='no direct selected neighbour' in str(e)
    assert rejected
    return dict(all_full_matchings=len(full),weight_models=len(rows),full_N_comparisons=comparisons,
                direct_centre_hypothesis_rejected=rejected,rows=rows)


def obstruction_controls():
    rows=[]
    for k in [None,2,3,7,10**6,10**400+17]:
        f=branched_family(True) if k is None else weighted_obstruction(k)
        weights=f.get('weights',{e:1 for e in f['M']})
        result=certify_two_path_bound(f['board'],f['M'],f['T'],f['parts'],f['centres'],weights)
        assert result['global_optimum_certified']
        expected=2 if k is None else k
        assert result['minimum_TH_fee']==expected and result['two_path']['minimum']==(2 if k is None else k+1)
        check_pair(result['two_path'],f['board'],f['M'],f['T'],weights,set(f['centres']))
        state=physical_state(f['board'],f['M'],result['base']['auxiliary'],f['T'])
        assert sum(weights[e] for e in state['paid'])==expected
        rows.append(dict(K=k,source_budget=1,two_path_minimum=result['two_path']['minimum'],true_optimum=expected))
    return rows


def rematching_controls():
    rng=random.Random(27102799);rows=[];f=branched_family()
    old=json.loads((ROOT/'output/exposable-source-completion.json').read_text())['rematched_controls']
    for variant in range(48):
        m=flip_rematching(f['M'],f['P'],rng,80*(variant+1));weights={e:rng.randrange(12) for e in sorted(m)}
        if variant%8==0:weights={e:1 for e in m}
        elif variant%8==1:weights={e:0 for e in m}
        elif variant%8==2:weights={e:10**400+3*j for j,e in enumerate(sorted(m))}
        elif variant%8==3:weights={e:rng.randrange(1,12) for e in sorted(m)}
        result=certify_two_path_bound(f['board'],m,f['T'],f['parts'],f['centres'],weights)
        base=result['base'];assert base['source_budget']==old[variant]['source_budget']
        assert base['normal_form_optimum']==old[variant]['normal_form_upper']
        check_pair(result['two_path'],f['board'],m,f['T'],weights,set(f['centres']))
        state=physical_state(f['board'],m,base['auxiliary'],f['T'])
        assert sum(weights[e] for e in state['paid'])==result['normal_form_upper']
        rows.append(dict(variant=variant,old_lower=base['source_budget'],new_lower=result['lower_bound'],
                         U1=result['normal_form_upper'],F2C=result['two_path']['minimum'],
                         old_exact=base['budget_attained'],new_exact=result['global_optimum_certified']))
    assert sum(r['old_exact'] for r in rows)==39
    assert sum(r['new_exact'] for r in rows)==44
    return rows


def strict_compensation_controls():
    raw=json.loads((ROOT/'develop/fixtures/two-th-compensation.json').read_text());f=branched_family()
    m={edge(tuple(a),tuple(b)) for a,b in raw['M']};n={edge(tuple(a),tuple(b)) for a,b in raw['N']}
    cheap={edge(tuple(a),tuple(b)) for a,b in raw['cheap_edges']};state=physical_state(f['board'],m,n,f['T'])
    normal_n={edge(tuple(a),tuple(b)) for a,b in raw['normal_form_N']}
    normal_state=physical_state(f['board'],m,normal_n,f['T'])
    normal_th=[path for path in normal_state['data']['paths'] if path['kind']=='TH' and path['M']]
    assert len(normal_th)==1 and len(normal_state['paid'])==1 and not normal_state['paid']&cheap
    assert set(normal_th[0]['vertices'])==set(map(tuple,raw['normal_form_TH_path']))
    assert normal_state['data']['counts'][1]==4
    assert state['paid']==cheap and len(cheap)==2
    nontrivial=[path for path in state['data']['paths'] if path['kind']=='TH' and path['M']]
    assert len(nontrivial)==2
    assert {frozenset(path['vertices']) for path in nontrivial}=={frozenset(tuple(v) for v in path) for path in raw['nontrivial_TH_paths']}
    mm=mates(f['board'],m);one_cheap_sources=[]
    for h in f['centres']:
        sources=set()
        for e in cheap:
            a,b=e
            if sum(a)%2:a,b=b,a
            if b in neighbours(h):sources|=neighbours(a)&f['T']
        one_cheap_sources.append(sources)
    assert one_cheap_sources==[set(),{(1,2)},set(),set(),set()]
    assert (1,2) in f['white_chamber']
    assert neighbours((6,9))&set(f['centres'])==set()
    rows=[]
    for k in [3,7,100,10**6,10**400+17]:
        weights={e:1 if e in cheap else k for e in m}
        result=certify_two_path_bound(f['board'],m,f['T'],f['parts'],f['centres'],weights)
        assert result['base']['rho']==[k,1,k,k,k] and result['base']['sigma']==[k]*5
        assert result['base']['source_budget']==1 and result['normal_form_upper']==k
        assert result['two_path']['minimum']==result['lower_bound']==2
        assert sum(weights[e] for e in state['paid'])==2<k
        assert sum(weights[e] for e in normal_state['paid'])==k
        check_pair(result['two_path'],f['board'],m,f['T'],weights,set(f['centres']))
        for path in raw['exposable_single_K_centre_relays']:
            path=list(map(tuple,path));assert path[0] in result['base']['outer']['exposable']
            assert len(path)==4 and edge(path[1],path[2]) in m-cheap
            assert all(b in neighbours(a) for a,b in zip(path,path[1:]))
        # The alternative full N, rather than the normal form, attains B_2.
        rows.append(dict(K=k,Lambda=1,U1=k,F2C=2,true_optimum=2,normal_form_globally_optimal=False))
    zero={e:0 if e in cheap else 1 for e in m}
    result=certify_two_path_bound(f['board'],m,f['T'],f['parts'],f['centres'],zero)
    assert result['normal_form_upper']==1 and result['lower_bound']==0
    assert sum(zero[e] for e in state['paid'])==0
    return dict(positive_weight_family=rows,zero_weight_control=dict(U1=1,true_optimum=0),
                nontrivial_TH_paths=raw['nontrivial_TH_paths'],cheap_edges=raw['cheap_edges'],
                source_of_cheap_centre_path=[1,2],one_cheap_edge_centre_sources=[sorted(x) for x in one_cheap_sources],
                full_auxiliary_edges=len(n),actual_edges=len(m))


def main():
    small=small_path_controls();full=full_matching_controls();obstructions=obstruction_controls()
    rematched=rematching_controls();strict=strict_compensation_controls()
    out=dict(status='PASS',small_path_controls=small,full_matching_controls=full,
             existing_obstructions=obstructions,rematched_controls=rematched,
             old_exact_models=39,new_exact_models=44,newly_certified_variants=[r['variant'] for r in rematched if r['new_exact'] and not r['old_exact']],
             still_unresolved_variants=[r['variant'] for r in rematched if not r['new_exact']],
             strict_compensation=strict,
             scope='General dichotomy and all-integer-K positive-weight compensation family proved in the note. Finite checks test flow implementation, full matching accounting and explicit witnesses. No universal 5/6 or Lean claim.')
    (ROOT/'output/two-th-path-bound.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','old_exact_models','new_exact_models','newly_certified_variants','still_unresolved_variants']}),flush=True)
    print(json.dumps(small),flush=True)
    print(json.dumps({k:v for k,v in full.items() if k!='rows'}),flush=True)
    print('Positive-weight fixed-footprint family: Lambda=1, F2C=f*=2, U1=K, every integer K>=3.',flush=True)


if __name__=='__main__':main()
