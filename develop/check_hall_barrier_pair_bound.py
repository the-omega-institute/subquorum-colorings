"""Independent barriers, quota-pair enumeration and fixed-path completion.

General claims and the all-K wrong-minimum-pair obstruction have written
proofs. Small enumeration and full coordinate witnesses validate the code.
"""
from itertools import combinations,permutations
from pathlib import Path
import json,random

from hall_barrier_pair_bound import (canonical_barrier,quota_pair_relaxation,
    certify_hall_barrier_bound,complete_fixed_th_paths,solve_hall_barrier_completion)
from exposable_source_completion import surplus_exposure
from check_two_th_path_bound import enumerate_physical_paths,check_pair
from check_mixed_terminal_compensation import all_matchings,edge,grid,mates,neighbours
from check_general_square_ports import physical_state
from check_corner_relay_shortest_path import flip_rematching
from branched_source_obstruction import branched_family

if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def barrier_graph_controls():
    graphs=saturated=matchings=tight_sets=0
    for n in range(4):
        left=set(range(n));right=set(range(n+1));pairs=[(a,b) for a in sorted(left) for b in sorted(right)]
        for mask in range(1<<len(pairs)):
            adj={a:{b for j,(a1,b) in enumerate(pairs) if a1==a and mask>>j&1} for a in left}
            assignments=[dict(zip(sorted(left),image)) for image in permutations(sorted(right),n)
                         if all(b in adj[a] for a,b in zip(sorted(left),image))]
            got=surplus_exposure(left,right,adj);graphs+=1
            assert (got is None)==(not assignments)
            if got is None:continue
            saturated+=1;barrier=canonical_barrier(got)
            E=set().union(*(right-set(a.values()) for a in assignments));F=right-E
            D={b for b in left if not adj[b]&E}
            assert barrier==dict(exposable=E,forbidden=F,dark=D)
            for a in assignments:
                assert {b for b in left if a[b] in F}==D;matchings+=1
            union=set()
            for k in range(n+1):
                for S in combinations(sorted(left),k):
                    N=set().union(set(),*(adj[b] for b in S))
                    if len(S)==len(N):union|=N;tight_sets+=1
            assert union==F
    return dict(all_surplus_one_graphs=graphs,saturating_graphs=saturated,
                independent_saturating_matchings=matchings,tight_sets_checked=tight_sets,
                scope='Every bipartite graph with black size 0..3 and white surplus one; independent permutation matching and all tight subsets.')


def quota_pair_controls():
    rng=random.Random(27102831);models=compares=infinite=finite=0
    for h,w in [(2,2),(2,3),(3,4)]:
        board=grid(h,w)
        for full in all_matchings(board):
            full=sorted(full)
            masks=range(1<<len(full)) if len(full)<=3 else sorted({rng.randrange(1<<len(full)) for _ in range(12)})
            for mask in masks:
                m={e for i,e in enumerate(full) if mask>>i&1};q=board-set(mates(board,m))
                white={v for v in q if sum(v)%2};black=q-white
                for selection in range(3):
                    t=white if selection==0 else {v for v in sorted(white) if rng.randrange(2)}
                    weights={e:(0 if selection==1 else rng.randrange(9)) for e in sorted(m)}
                    if models%17==0:weights={e:10**400+3*i for i,e in enumerate(sorted(m))}
                    paths=enumerate_physical_paths(board,m,t,weights);models+=1
                    source={a:next(iter(a[0]&t)) for a in paths}
                    for variant in range(3):
                        if variant==0:
                            sg=[set(),set(t)];eg=[set(),set(black)]
                        else:
                            s0={v for v in sorted(t) if rng.randrange(2)};sg=[s0,t-s0]
                            e0=set();e1=set()
                            for v in sorted(black):
                                kind=rng.randrange(3)
                                if kind==0:e0.add(v)
                                elif kind==1:e1.add(v)
                            eg=[e0,e1]
                        costs=[]
                        for a,b in combinations(paths,2):
                            if a[0]&b[0]:continue
                            if not all(sum(source[p] in group for p in (a,b))==1 for group in sg):continue
                            if not all(sum(p[2] in group for p in (a,b))==1 for group in eg):continue
                            costs.append(a[3]+b[3])
                        expected=min(costs) if costs else None
                        got=quota_pair_relaxation(board,m,t,weights,sg,eg);assert got['minimum']==expected
                        check_pair(got,board,m,t,weights,None)
                        if expected is not None:
                            assert all(sum(p['vertices'][0] in group for p in got['paths'])==1 for group in sg)
                            assert all(sum(p['vertices'][-1] in group for p in got['paths'])==1 for group in eg)
                            finite+=1
                        else:infinite+=1
                        compares+=1
    return dict(physical_models=models,independent_quota_pair_comparisons=compares,
                finite_pair_minima=finite,infeasible_pair_minima=infinite,
                scope='All submatchings of all full 2x2/2x3 matchings, sampled subsets of each full 3x4 matching, three source/weight variants and three group assignments. Reference enumerates disjoint physical paths with both quotas independently.')


def ordered_paths(board,m,t):
    mm=mates(board,m);q=board-set(mm);out=[]
    def visit(path):
        v=path[-1]
        if len(path)>1 and v in q:
            if len(path)>=4:out.append(path)
            return
        options=(neighbours(v)&board)-({mm[v]} if v in mm else set()) if sum(v)%2 else ({mm[v]} if v in mm else set())
        for z in sorted(options):
            if z not in path:visit(path+[z])
    for start in sorted(t):visit([start])
    return out


def check_extension_certificate(board,m,t,paths,result):
    fixed_m={edge(path[i],path[i+1]) for path in paths for i in range(1,len(path)-1,2)}
    removed=set().union(set(),*(set(path) for path in paths));remaining=board-removed;p=set(mates(board,m))
    assert result['remaining']==remaining
    if result['feasible']:
        state=physical_state(board,m,result['auxiliary'],t)
        assert state['paid']==fixed_m==result['fixed_actual']
        assert all(edge(path[i],path[i+1]) in result['auxiliary'] for path in paths for i in range(0,len(path)-1,2))
        return
    S=result['Hall_black'];N=result['Hall_white']
    assert S<=remaining and all(sum(v)%2==0 for v in S)
    actual_neighbours={w for b in S for w in neighbours(b)&remaining if not(w in t and b in p)}
    assert actual_neighbours==N and len(N)<len(S)


def fixed_path_controls():
    rng=random.Random(27102832);models=specifications=success=fail=full_comparisons=0
    for h,w in [(2,2),(2,3),(3,4)]:
        board=grid(h,w);full=[set(n) for n in all_matchings(board)]
        reference=[(n,mates(board,n)) for n in full]
        for original in full:
            original=sorted(original)
            masks=range(1<<len(original)) if len(original)<=3 else sorted({rng.randrange(1<<len(original)) for _ in range(8)})
            for mask in masks:
                m={e for i,e in enumerate(original) if mask>>i&1};q=board-set(mates(board,m))
                white={v for v in q if sum(v)%2}
                for selection in range(2):
                    t=white if selection==0 else {v for v in sorted(white) if rng.randrange(2)}
                    paths=ordered_paths(board,m,t);specs=[[]]+[[path] for path in paths]
                    specs += [[a,b] for a,b in combinations(paths,2) if not set(a)&set(b)]
                    models+=1
                    for chosen in specs:
                        fixed_n={edge(path[i],path[i+1]) for path in chosen for i in range(0,len(path)-1,2)}
                        starts={path[0] for path in chosen};possible=False
                        for n,nm in reference:
                            full_comparisons+=1
                            if fixed_n<=n and all(nm[t1] in q for t1 in t-starts):possible=True
                        got=complete_fixed_th_paths(board,m,t,chosen)
                        assert got['feasible']==possible
                        check_extension_certificate(board,m,t,chosen,got);specifications+=1
                        if possible:success+=1
                        else:fail+=1
    return dict(physical_models=models,fixed_path_specifications=specifications,
                all_full_N_reference_comparisons=full_comparisons,feasible_completions=success,
                certified_Hall_failures=fail,
                scope='Empty lists, every nontrivial single path, and every disjoint pair in the sampled physical models; compare with every full N of each 2x2,2x3,3x4 board. No model sampling over N.')


def small_full_N_controls():
    board=grid(4,4);m={edge((0,1),(0,2)),edge((1,0),(2,0))};p=set(mates(board,m));t={v for v in board-p if sum(v)%2}
    full=[set(n) for n in all_matchings(board)];comparisons=0
    for values in [(0,0),(0,1),(1,0),(1,1),(2,7),(10**400,3)]:
        weights=dict(zip(sorted(m),values));got=solve_hall_barrier_completion(board,m,t,[p],[(0,0)],weights)
        fees=[]
        for n in full:
            state=physical_state(board,m,n,t);fee=sum(weights[e] for e in state['paid']);fees.append(fee)
            assert fee>=got['lower_bound'];comparisons+=1
        assert got['global_optimum_certified'] and got['minimum_TH_fee']==min(fees)
    return dict(full_auxiliary_matchings=len(full),weight_models=6,full_N_bound_comparisons=comparisons,
                empty_canonical_barrier_tested=True)


def rematching_controls():
    rng=random.Random(27102799);f=branched_family();rows=[];cert=None
    old=json.loads((ROOT/'output/two-th-path-bound.json').read_text())['rematched_controls']
    for variant in range(48):
        m=flip_rematching(f['M'],f['P'],rng,80*(variant+1));weights={e:rng.randrange(12) for e in sorted(m)}
        if variant%8==0:weights={e:1 for e in m}
        elif variant%8==1:weights={e:0 for e in m}
        elif variant%8==2:weights={e:10**400+3*j for j,e in enumerate(sorted(m))}
        elif variant%8==3:weights={e:rng.randrange(1,12) for e in sorted(m)}
        got=solve_hall_barrier_completion(f['board'],m,f['T'],f['parts'],f['centres'],weights)
        assert got['previous']['lower_bound']==old[variant]['new_lower']
        assert got['normal_form_upper']==old[variant]['U1']
        assert got['global_optimum_certified'] and got['minimum_TH_fee']==got['lower_bound']
        state=physical_state(f['board'],m,got['auxiliary'],f['T'])
        assert sum(weights[e] for e in state['paid'])==got['lower_bound']
        for key in ['two_centres','Hall_pair']:
            check_pair(got[key],f['board'],m,f['T'],weights,None)
        rows.append(dict(variant=variant,B2=old[variant]['new_lower'],BH=got['lower_bound'],
                         U1=got['normal_form_upper'],F_CC=got['two_centres']['minimum'],F_H=got['Hall_pair']['minimum'],
                         true_optimum=got['minimum_TH_fee'],completion_kind=got['completion_kind'],
                         normal_form_globally_optimal=got['normal_form_globally_optimal']))
        if variant==31:
            assert got['minimum_TH_fee']==0 and got['normal_form_upper']==2
            bad=[p['vertices'] for p in got['previous']['two_path']['paths']]
            rejected=complete_fixed_th_paths(f['board'],m,f['T'],bad);assert not rejected['feasible']
            check_extension_certificate(f['board'],m,f['T'],bad,rejected)
            cert=dict(variant=31,original_actual_matching=sorted(m),original_weights=sorted(weights.items()),
                      attaining_auxiliary=sorted(got['auxiliary']),original_weight_true_optimum=0,
                      original_weight_normal_form_optimum=2,Hall_pair_paths=[p['vertices'] for p in got['Hall_pair']['paths']],
                      rejected_pair_paths=bad,rejected_Hall_black=sorted(rejected['Hall_black']),
                      rejected_Hall_white=sorted(rejected['Hall_white']),
                      canonical_D=sorted(got['barrier']['dark']),canonical_F=sorted(got['barrier']['forbidden']))
    assert sum(r['normal_form_globally_optimal'] for r in rows)==47
    assert sum(r['completion_kind']=='Hall_pair_optimum' for r in rows)==1
    return rows,cert


def wrong_minimum_pair_controls(certificate):
    raw=json.loads((ROOT/'develop/fixtures/two-th-compensation.json').read_text());f=branched_family()
    m={edge(tuple(a),tuple(b)) for a,b in raw['M']}
    cheap={edge(tuple(a),tuple(b)) for a,b in raw['cheap_edges']}|{edge((6,6),(6,7))}
    bad=[[(1,2),(2,2),(3,2),(4,2)],[(5,6),(6,6),(6,7),(5,7)]]
    good=[[(1,2),(2,2),(3,2),(4,2)],[(6,11),(6,10),(6,9),(5,9)]]
    rejection=complete_fixed_th_paths(f['board'],m,f['T'],bad);assert not rejection['feasible']
    check_extension_certificate(f['board'],m,f['T'],bad,rejection)
    assert len(rejection['Hall_black'])==51 and len(rejection['Hall_white'])==50
    completion=complete_fixed_th_paths(f['board'],m,f['T'],good);assert completion['feasible']
    check_extension_certificate(f['board'],m,f['T'],good,completion)
    rows=[]
    for k in [3,7,100,10**6,10**400+17]:
        weights={e:1 if e in cheap else k for e in m}
        got=solve_hall_barrier_completion(f['board'],m,f['T'],f['parts'],f['centres'],weights)
        assert got['normal_form_upper']==k and got['minimum_TH_fee']==got['Hall_pair']['minimum']==2
        assert got['previous']['two_path']['minimum']==2
        bad_fee=sum(weights[edge(p[i],p[i+1])] for p in bad for i in range(1,len(p)-1,2))
        assert bad_fee==2
        assert sum(weights[e] for e in physical_state(f['board'],m,completion['auxiliary'],f['T'])['paid'])==2
        assert all(path[0] in got['barrier']['forbidden'] for path in bad)
        assert bad[1][-1] in got['barrier']['dark']
        rows.append(dict(K=k,true_optimum=2,U1=k,F2C=2,minimum_pair_A_C_extendable_at_fee=False,
                         minimum_pair_A_B_extendable_at_fee=True))
    certificate.update(three_cheap_edges=sorted(cheap),three_cheap_symbolic_weights='1 on these three edges; K on all others, every integer K>=3',
                       bad_minimum_pair_paths=bad,good_minimum_pair_paths=good,
                       bad_pair_Hall_black=sorted(rejection['Hall_black']),bad_pair_Hall_white=sorted(rejection['Hall_white']),
                       good_pair_attaining_auxiliary=sorted(completion['auxiliary']))
    return rows


def main():
    graph=barrier_graph_controls();quota=quota_pair_controls();extension=fixed_path_controls();small=small_full_N_controls()
    rows,certificate=rematching_controls();wrong=wrong_minimum_pair_controls(certificate)
    out=dict(status='PASS',canonical_barrier_controls=graph,physical_quota_controls=quota,
             fixed_path_extension_controls=extension,small_full_N_controls=small,
             original_rematching_controls=rows,old_two_path_exact_count=44,Hall_bound_normal_form_exact_count=47,
             Hall_bound_plus_extension_exact_count=48,new_normal_form_certificates=[14,23,45],
             original_variant31_true_optimum=0,all_K_wrong_minimum_pair_family=wrong,
             scope='Canonical barrier and forced compensation bound are general written proofs. Fixed-path extension criterion is an iff for the specified direct remainder only. All-K wrong-minimum-pair obstruction is proved symbolically. Enumeration tests implementation and fixed witnesses. Not a general exact optimizer or universal 5/6 result; no Lean claim.')
    (ROOT/'output/hall-barrier-pair-bound.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'output/hall-barrier-pair-certificates.json').write_text(json.dumps(certificate,indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','old_two_path_exact_count','Hall_bound_normal_form_exact_count','Hall_bound_plus_extension_exact_count','original_variant31_true_optimum']}),flush=True)
    for result in [graph,quota,extension,small]:print(json.dumps(result),flush=True)


if __name__=='__main__':main()
