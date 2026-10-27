"""Independent endpoint enumeration, physical controls and symbolic witnesses.

General proofs are in docs/MULTICENTRE_HALL_BALANCE.md. Enumerations test
the implementation and the case split, not arbitrary-size mathematics.
"""
from itertools import combinations,permutations,product
from pathlib import Path
import json,random

from multicentre_hall_balance import (terminal_balance,certify_multicentre_bound,
    solve_multicentre_completion,two_cheap_centre_family,proper_root_counterexample)
from exposable_source_completion import surplus_exposure
from hall_barrier_pair_bound import complete_fixed_th_paths
from check_hall_barrier_pair_bound import check_extension_certificate
from check_two_th_path_bound import enumerate_physical_paths,check_pair
from check_mixed_terminal_compensation import all_matchings,edge,grid,mates,neighbours
from check_general_square_ports import physical_state
from check_corner_relay_shortest_path import flip_rematching
from check_unbounded_hole_relay import family
from branched_source_obstruction import branched_family

if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1]


def abstract_source_controls():
    graphs=saturated=partial_assignments=0
    for r in range(1,5):
        W=list(range(r-1));C=set(range(r));edges=list(product(W,sorted(C)))
        for mask in range(1<<len(edges)):
            adj={w:{c for j,(w1,c) in enumerate(edges) if w1==w and mask>>j&1} for w in W}
            full=[dict(zip(W,cs)) for cs in permutations(sorted(C),len(W))
                  if all(c in adj[w] for w,c in zip(W,cs))]
            got=surplus_exposure(set(W),C,adj);graphs+=1
            assert (got is None)==(not full)
            if not full:continue
            saturated+=1;J=set().union(*(C-set(x.values()) for x in full))
            assert got['exposable']==J
            for n in range(r):
                for left in combinations(W,n):
                    for right in permutations(sorted(C),n):
                        if not all(c in adj[w] for w,c in zip(left,right)):continue
                        used=set(right)
                        # Independent references: at least one maximum matching
                        # preserves every occupied right vertex, and an eligible
                        # centre is absent from the original partial matching.
                        assert any(used<=set(x.values()) for x in full)
                        assert J-used
                        partial_assignments+=1
    return dict(graphs=graphs,saturating_graphs=saturated,
                independent_partial_HH_centre_assignments=partial_assignments,
                scope='All Gamma with r=1..4, r-1 sources, and all partial matchings; eligible roots from independent permutations.')


def abstract_terminal_controls():
    cases={'U1':0,'FX':0,'FH':0};bijections=0;counts={};example=None
    for r in range(1,4):
        W=[('w',i) for i in range(r-1)];C=[('c',i) for i in range(r)]
        gamma_edges=list(product(W,C))
        for mask in range(1<<len(gamma_edges)):
            gamma={e for j,e in enumerate(gamma_edges) if mask>>j&1}
            saturated=[cs for cs in permutations(C,len(W)) if all((w,c) in gamma for w,c in zip(W,cs))]
            if not saturated:continue
            J=set().union(*(set(C)-set(cs) for cs in saturated))
            for nf in range(3):
                for ne in (1,2):
                    F=[('f',i) for i in range(nf)];E=[('e',i) for i in range(ne)]
                    D=[('d',i) for i in range(nf)];O=[('o',i) for i in range(ne-1)]
                    white=W+F+E;black=C+D+O
                    for perm in permutations(black):
                        pairs=dict(zip(white,perm))
                        if any(pairs[w] in C and (w,pairs[w]) not in gamma for w in W):continue
                        th=[(w,pairs[w]) for w in F+E if pairs[w] in C]
                        k=len(th);a=sum(pairs[w] not in D for w in F)
                        b=sum(pairs[w] in D for w in E);c=sum(pairs[w] in D for w in W)
                        outside=sum(pairs[w] not in C for w in W)
                        assert k>=1 and a==b+c and outside==k-1 and c<=k-1
                        assert any(z in J for w,z in th)
                        if all(w in F for w,z in th):assert a>=k and b>=1
                        if any(w in E and z in J for w,z in th):kind='U1'
                        elif any(w in E and z not in J for w,z in th):
                            kind='FX';assert any(w in F and z in J for w,z in th)
                            if example is None and b==0:
                                example=dict(r=r,gamma=sorted(gamma),eligible=sorted(J),pairs=sorted(pairs.items()),a=a,b=b,c=c,k=k)
                        else:
                            kind='FH'
                            assert any(w in F and z in J for w,z in th)
                            assert any(pairs[w] in D for w in E)
                        cases[kind]+=1;bijections+=1;counts[k]=counts.get(k,0)+1
    assert all(cases.values()) and example is not None
    return dict(terminal_bijections=bijections,classification=cases,TH_centre_histogram=counts,
                proper_J_FX_endpoint_countermodel=example,
                scope='All Gamma r=1..3 admitting saturation, F size0..2,E size1..2, all endpoint bijections consistent with HH-centre incidence. No grid realizability is assumed for this abstract check.')


def balance_numbers(value):
    return {k:value[k] for k in ['a','b','c','k','HH_outside_centres','all_TH_centre_sources_in_F']}


def small_full_N_controls():
    board=grid(4,4);p0={(0,1),(0,2),(1,0),(2,0)}
    m0={edge((0,1),(0,2)),edge((1,0),(2,0))}
    full=[set(n) for n in all_matchings(board)];checks=0
    rows=[]
    for values in [(0,0),(0,1),(1,0),(1,1),(2,7),(10**400,3)]:
        t={v for v in board-p0 if sum(v)%2};weights=dict(zip(sorted(m0),values))
        got=solve_multicentre_completion(board,m0,t,[p0],[(0,0)],weights);fees=[]
        for n in full:
            state=physical_state(board,m0,n,t);fee=sum(weights[e] for e in state['paid']);fees.append(fee)
            assert fee>=got['lower_bound'];checks+=1
            bal=terminal_balance(board,m0,n,t,[(0,0)],got['barrier'])
            assert bal['k']==1
        assert got['global_optimum_certified'] and got['minimum_TH_fee']==min(fees)
        rows.append(dict(weights=list(values),optimum=min(fees),BM=got['lower_bound']))
    return dict(full_N_matchings=len(full),full_N_comparisons=checks,weight_controls=rows)


def proper_root_controls():
    f=family(1);board=grid(6,14);parts=[];centres=[];m=set()
    for r,c in [(0,0),(0,8)]:
        move=lambda v:(v[0]+r,v[1]+c)
        parts.append({move(v) for v in f['P']});centres.append(move(f['h']))
        m|={edge(move(a),move(b)) for a,b in f['M']}
    t={v for v in board-set(mates(board,m)) if sum(v)%2}-{(5,2)}
    weights={e:1 for e in m};got=solve_multicentre_completion(board,m,t,parts,centres,weights)
    assert got['base']['eligible_roots']=={1} and not got['all_roots_eligible']
    assert got['base']['source_adjacency']=={(5,2):{0}}
    assert got['barrier']['forbidden']=={(5,0),(5,4)}
    assert got['mixed_centre_pair']['minimum']==3 and got['minimum_TH_fee']==1
    check_pair(got['mixed_centre_pair'],board,m,t,weights,None)
    paths=enumerate_physical_paths(board,m,t,weights);F=got['barrier']['forbidden'];E=got['barrier']['exposable']
    candidates=[]
    for a,b in combinations(paths,2):
        if a[0]&b[0]:continue
        sources=[next(iter(p[0]&t)) for p in (a,b)]
        if sum(s in F for s in sources)!=1 or sum(s in E for s in sources)!=1:continue
        if {a[2],b[2]}==set(centres):candidates.append(a[3]+b[3])
    assert min(candidates)==3
    state=physical_state(board,m,got['auxiliary'],t);assert len(state['paid'])==1
    return dict(eligible_roots=[1],source_adjacency=[[[5,2],[0]]],F=sorted(F),FX=3,BM=1,optimum=1,
                independent_physical_paths=len(paths),independent_qualifying_pairs=len(candidates)),dict(
                board=sorted(board),M=sorted(m),T=sorted(t),centres=centres,parts=[sorted(p) for p in parts],
                attaining_N=sorted(got['auxiliary']),FX_paths=[p['vertices'] for p in got['mixed_centre_pair']['paths']])


def original_controls():
    rng=random.Random(27102799);f=branched_family();rows=[]
    old=json.loads((ROOT/'output/hall-barrier-pair-bound.json').read_text())['original_rematching_controls']
    for variant in range(48):
        m=flip_rematching(f['M'],f['P'],rng,80*(variant+1));weights={e:rng.randrange(12) for e in sorted(m)}
        if variant%8==0:weights={e:1 for e in m}
        elif variant%8==1:weights={e:0 for e in m}
        elif variant%8==2:weights={e:10**400+3*j for j,e in enumerate(sorted(m))}
        elif variant%8==3:weights={e:rng.randrange(1,12) for e in sorted(m)}
        got=solve_multicentre_completion(f['board'],m,f['T'],f['parts'],f['centres'],weights)
        assert got['previous']['lower_bound']==old[variant]['BH']
        assert got['global_optimum_certified'] and got['minimum_TH_fee']==old[variant]['true_optimum']
        state=physical_state(f['board'],m,got['auxiliary'],f['T'])
        assert sum(weights[e] for e in state['paid'])==got['lower_bound']
        for key in ['Hall_pair','mixed_centre_pair']:check_pair(got[key],f['board'],m,f['T'],weights,None)
        bal=terminal_balance(f['board'],m,got['auxiliary'],f['T'],f['centres'],got['barrier'])
        rows.append(dict(variant=variant,BH=old[variant]['BH'],BM=got['lower_bound'],
                         optimum=got['minimum_TH_fee'],completion=got['completion_kind'],balance=balance_numbers(bal)))
    return rows


def all_K_controls():
    A=[(1,2),(2,2),(3,2),(4,2)];B=[(5,8),(6,8),(7,8),(8,8)]
    R=[(7,4),(6,4),(5,4),(5,5)];rows=[];certificate=None
    for k in [3,7,100,10**6,10**400+17]:
        f=two_cheap_centre_family(k);board,m,t=[f[x] for x in ['board','M','T']]
        got=solve_multicentre_completion(board,m,t,f['parts'],f['centres'],f['weights'])
        assert got['all_roots_eligible'] and got['base']['rho']==[1,1,k,k,k]
        assert got['base']['source_budget']==1 and got['previous']['lower_bound']==2
        assert got['lower_bound']==got['minimum_TH_fee']==got['normal_form_upper']==k
        assert got['Hall_pair']['minimum']==k+1 and got['mixed_centre_pair']['minimum'] is None
        assert got['previous']['two_centres']['minimum']==2
        F,E,D=[got['barrier'][x] for x in ['forbidden','exposable','dark']]
        assert F==f['white_chamber'] and D==f['black_chamber']
        for e in f['cheap_edges']:
            black=next(v for v in e if sum(v)%2==0)
            assert not(neighbours(black)&E)
        assert {(8,5),(7,4)}<=E and {(1,2),(5,8)}<=F and (5,5) in D
        state=physical_state(board,m,got['auxiliary'],t)
        paid=state['paid'];assert not paid&f['cheap_edges'] and len(paid)==1
        witness=complete_fixed_th_paths(board,m,t,[A,B,R]);assert witness['feasible']
        check_extension_certificate(board,m,t,[A,B,R],witness)
        sharp=terminal_balance(board,m,witness['auxiliary'],t,f['centres'],got['barrier'])
        assert balance_numbers(sharp)==dict(a=2,b=1,c=1,k=2,HH_outside_centres=1,all_TH_centre_sources_in_F=True)
        paid2=physical_state(board,m,witness['auxiliary'],t)['paid']
        assert len(paid2&f['cheap_edges'])==2 and len(paid2-f['cheap_edges'])==1
        assert sum(f['weights'][e] for e in paid2)==k+2
        for key in ['Hall_pair','mixed_centre_pair']:check_pair(got[key],board,m,t,f['weights'],None)
        hh=[]
        for p in sharp['state']['data']['paths']:
            vs=p['vertices']
            if sum(vs[0])%2==0:vs=list(reversed(vs))
            if vs[0] in f['white_holes'] and vs[-1] in D:hh.append(vs)
        assert len(hh)==1
        rows.append(dict(K=k,BH=2,BM=k,optimum=k,U1=k,F_CC=2,F_H=k+1,F_X=None,
                         normal_paid_coefficients=[0,1],sharp_two_centre_coefficients=[2,1],
                         two_centre_balance=balance_numbers(sharp)))
        if certificate is None:
            certificate=dict(board=sorted(board),M=sorted(m),T=sorted(t),centres=f['centres'],
                parts=[sorted(p) for p in f['parts']],W=sorted(f['white_holes']),F=sorted(F),E=sorted(E),D=sorted(D),
                cheap_edges=sorted(f['cheap_edges']),symbolic_weights='1 on two cheap edges; integer K>=3 on every other M edge',
                optimum_N=sorted(got['auxiliary']),optimum_paid=sorted(paid),optimum_symbolic_coefficients=[0,1],
                cheap_centre_paths=[A,B],Hall_quota_attaining_paths=[A,R],
                sharp_two_centre_fixed_paths=[A,B,R],sharp_two_centre_N=sorted(witness['auxiliary']),
                sharp_two_centre_paid=sorted(paid2),sharp_two_centre_symbolic_coefficients=[2,1],
                sharp_two_centre_HH_to_D=hh[0],sharp_two_centre_balance=balance_numbers(sharp))
        else:
            assert sorted(got['auxiliary'])==certificate['optimum_N']
            assert sorted(witness['auxiliary'])==certificate['sharp_two_centre_N']
    return rows,certificate


def proper_root_counterexample_controls():
    A=[(5,2),(6,2),(7,2),(8,2)];B=[(5,8),(4,8),(3,8),(2,8)]
    R=[(5,6),(4,6),(3,6),(3,5)];rows=[];certificate=None
    chamber={(r,c) for r in range(6) for c in range(6)}-{(0,5),(5,5)}
    F={v for v in chamber if sum(v)%2};D=chamber-F
    assert len(F)==len(D)==17
    for k in [3,7,100,10**6,10**400+17]:
        f=proper_root_counterexample(k);board,m,t=[f[key] for key in ['board','M','T']]
        got=solve_multicentre_completion(board,m,t,f['parts'],f['centres'],f['weights'])
        assert got['base']['eligible_roots']=={1} and got['base']['source_adjacency']=={(0,5):{0}}
        assert got['base']['rho']==[1,1] and got['base']['sigma']==[1,k]
        assert got['lower_bound']==got['minimum_TH_fee']==2 and got['normal_form_upper']==k
        assert got['mixed_centre_pair']['minimum']==2 and got['Hall_pair']['minimum']==k+1
        assert got['barrier']['forbidden']==F and got['barrier']['dark']==D
        invalid=min(got['normal_form_upper'],got['Hall_pair']['minimum']);assert invalid==k>2
        fixed=complete_fixed_th_paths(board,m,t,[A,B]);assert fixed['feasible']
        check_extension_certificate(board,m,t,[A,B],fixed)
        bal=terminal_balance(board,m,fixed['auxiliary'],t,f['centres'],got['barrier'])
        assert (bal['a'],bal['b'],bal['c'],bal['k'])==(1,0,1,2)
        paid=physical_state(board,m,fixed['auxiliary'],t)['paid'];assert paid==f['cheap_edges']
        check_pair(got['mixed_centre_pair'],board,m,t,f['weights'],None)
        check_pair(got['Hall_pair'],board,m,t,f['weights'],None)
        E=got['barrier']['exposable'];assert B[0] in E and A[0] in F and R[0] in E and R[-1] in D
        hh=[]
        for p in bal['state']['data']['paths']:
            vs=p['vertices']
            if sum(vs[0])%2==0:vs=list(reversed(vs))
            if vs[0] in f['white_holes'] and vs[-1] in D:hh.append(vs)
        assert hh==[[(0,5),(0,4)]]
        rows.append(dict(K=k,eligible_roots=[1],BM=2,optimum=2,U1=k,F_X=2,F_H=k+1,
                         invalid_bound_without_F_X=k,balance=balance_numbers(bal)))
        if certificate is None:
            normal_paid=physical_state(board,m,got['base']['auxiliary'],t)['paid']
            assert len(normal_paid)==1 and not normal_paid&f['cheap_edges']
            certificate=dict(board=sorted(board),M=sorted(m),T=sorted(t),parts=[sorted(p) for p in f['parts']],
                centres=f['centres'],W=sorted(f['white_holes']),F=sorted(F),D=sorted(D),E=sorted(E),
                cheap_edges=sorted(f['cheap_edges']),fixed_paths=[A,B],attaining_N=sorted(fixed['auxiliary']),
                paid=sorted(paid),symbolic_paid_coefficients=[2,0],Hall_attaining_paths=[A,R],
                normal_N=sorted(got['base']['auxiliary']),normal_paid=sorted(normal_paid),normal_paid_coefficients=[0,1],
                HH_to_D=hh[0],balance=balance_numbers(bal),eligible_roots=[1])
        else:assert sorted(fixed['auxiliary'])==certificate['attaining_N']
    return rows,certificate


def main():
    source=abstract_source_controls();print(json.dumps(source),flush=True)
    terminal=abstract_terminal_controls();print(json.dumps(terminal),flush=True)
    small=small_full_N_controls();proper,proper_cert=proper_root_controls()
    original=original_controls();weighted,weighted_cert=all_K_controls()
    counterexample,counterexample_cert=proper_root_counterexample_controls()
    out=dict(status='PASS',source_graph_controls=source,terminal_bijection_controls=terminal,
        small_grid_full_N_controls=small,proper_root_grid=proper,original_48_controls=original,
        original_48_exact_count=len(original),all_K_controls=weighted,all_K_proper_J_counterexample=counterexample,
        scope='General balance, eligible-centre lemma and strengthened inequality have written proofs. All-K improvement is symbolic with fixed full matching witnesses. Finite enumeration checks implementations. No general exact optimizer, unit-weight 5/6 improvement or Lean claim.')
    (ROOT/'output/multicentre-hall-balance.json').write_text(json.dumps(out,indent=2)+'\n')
    (ROOT/'output/multicentre-hall-certificates.json').write_text(json.dumps(dict(all_K=weighted_cert,proper_J=proper_cert,
        proper_J_counterexample=counterexample_cert),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',original_exact=len(original),all_K_samples=len(weighted),proper_J=proper,small_grid=small)),flush=True)


if __name__=='__main__':main()
