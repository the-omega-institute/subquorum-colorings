"""Exact seam-opening extremal budget and FULL-pool source/path circuits.

All-parameter written proofs: EXTREMAL_SHARED_UNIT_BUDGET_AND_FULL_POOL_PATH_CIRCUITS.md.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path

from check_forced_mates_and_adjacent_maxima import (configuration,uniform_freezing,
    forced_order,verify_forced_mates,upper_certificate)
from check_selection_maximum_singleton import compile_even_width
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow
from check_interface_reserve_reoptimization import constrained_primitive,subsets,physical_model
from check_frozen_beta_support_fork import restrict
from check_full_pool_interface_profile import closure
from check_endpoint_component_resource_gluing import physical_groups,local
from check_crossing_matching_ports import compile_partition
from check_residual_corridors import direct_check
from check_promotion_cores import frozen_certificate

if not __debug__:raise RuntimeError('Assertions required; no -O.')


@lru_cache(None)
def upper(w,k):
    return upper_certificate(w,k,configuration(w,k))


def feasible_local(S,P):
    occupied=P|S
    return not S&P and all(sum((v[0]+dr,v[1]+dc) in occupied
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)])<=1 for v in S)


def inspect(w,k,E,totals,write_fixture=False):
    m=len(E);base=configuration(w,k);removed={(w+1,10*i+1) for i in E}
    cur=(*base[:2],base[2]-removed,base[3]);R,C,T,M=cur;P={v for e in M for v in e}
    direct_check(*cur);ranks,layers=uniform_freezing(w,k,cur)
    assert frozen_certificate(cur)[0]==P and len(P)==k*(3*w+10)
    leaf=verify_forced_mates(cur,forced_order(w,k))
    optimum=(7*k+2)*(w//2)+3*k+2
    assert len(base[2])==optimum and len(T)==optimum-m
    patches=[{(r+j,2+10*a+b) for j in range(4) for b in (0,1)}
             for r,a in itertools.product((0,w-2),range(k))]
    tiles=[]
    for i in range(1,k):
        c=10*i;G={(r,s) for r in (w,w+1) for s in (c,c+1)}
        assert not any(G&H for H in patches) and not any(G&H for H in tiles);tiles.append(G)
        assert (w,c-1) in P and (w,c) not in P and (w+1,c) not in P
        points=sorted(G);free={(w,c),(w+1,c)}
        cap=max(len(S) for S in subsets(points) if feasible_local(S,P))
        forced=max(len(S) for S in subsets(free) if feasible_local(S,P))
        assert (cap,forced)==(2,1)
        assert {(w,10*i+1),(w+1,10*i+1)}.isdisjoint(T)==(i in E)
        totals['independent_seam_tile_cap_checks']+=1
    if w<=12 and k<=5:
        certificate=upper(w,k);assert certificate['upper_bound']==optimum
        assert len(certificate['patches'])==2*k
        totals['cached_general_cover_uses']+=1
    data,meta=compile_even_width(cur);own,A,B,X=owner_data(*data[:2]);Q=data[4]
    assert (len(A),len(B),len(X),len(Q),meta['slack'])==(k,0,7*k,3*k+m,2*k+m)
    flow=fork_flow(*data);assert (flow['value'],flow['cost'],flow['deficit'])==(m,m,k-m)
    units={i:(w//2,10*i+1,10*i+1) for i in E};assert set(units.values())<=Q
    roots=[];module_tables=[]
    for a in range(k):
        shift=10*a
        ids={name:own[(r,shift+c)] for name,r,c in [('A',1,5),('U0',1,3),('U1',1,6),('U2',1,8),('L0',w,3),('L1',w,6),('L2',w,8)]}
        roots.append(ids['A']);seen,edges=closure(data,{ids['A']})
        assert len(set(ids.values()))==7 and seen==set(ids.values())
        expected={'A':{'U0','U1','L0','L1'},'U1':{'U2'},'L1':{'L2'}}
        W={'L0':({units[a]} if a in E else set()),'L2':({units[a+1]} if a+1 in E else set())}
        for name,o in ids.items():
            assert edges[o]=={ids[x] for x in expected.get(name,set())}
            assert data[3][o]==W.get(name,set())
        module_tables.append(ids);totals['exact_seven_owner_closures']+=1
    assert set(roots)==A
    seen,_=closure(data,A)
    assert len(seen)==7*k and set().union(set(),*(data[3][o] for o in seen))==set(units.values())
    for i,j in units.items():
        users={module_tables[i-1]['L2'],module_tables[i]['L0']}
        assert {o for o,js in data[3].items() if j in js}==users
        assert {x for x in Q if {o for o,js in data[3].items() if x in js}==users}=={j}
        link=((w,10*i+5),(w,10*i+4));assert link in data[2]
    groups,_=physical_groups(cur,data);assert len(groups)==k
    byroot={a:next(g for g in groups if a in g) for a in A}
    for a,root in enumerate(roots):
        assert fork_flow(*local(data,byroot[root],Q))['value']==int(a in E or a+1 in E)
    if k<=4 and w<=10:
        assert constrained_primitive(data,set())==(m,m)
        totals['independent_primitive_profiles']+=1
    is_path=k>=2 and E==set(range(1,k))
    if is_path:
        for r,root in enumerate(roots):
            kept=set(range(len(data[1])))-{root};d=restrict(data,kept,Q);f=fork_flow(*d)
            assert (f['value'],f['cost'])==(k-1,k-1+r)
            if k<=4 and w<=10:
                assert constrained_primitive(data,A-{root})==(k-1,k-1+r)
                totals['independent_primitive_profiles']+=1
            # Explicit bijection, with the cost dictated by LEFT versus
            # RIGHT incidence in the physical path, not by scalar tiles.
            assignment={a:(a+1 if a<r else a) for a in range(k) if a!=r}
            assert set(assignment.values())==set(range(1,k))
            assert sum(2 if a<r else 1 for a in assignment)==k-1+r
            totals['all_maximum_source_basis_costs']+=1
        if k<=5:
            for D in subsets(A):
                keep=set(range(len(data[1])))-(A-D)
                assert fork_flow(*restrict(data,keep,Q))['value']==min(len(D),k-1)
                totals['all_proper_source_subsets']+=int(D!=A)
        core=set(units.values());outside=Q-core;assert len(outside)==3*k
        withdrawals=list(subsets(core)) if k<=8 else [set(),core]+[core-{j} for j in sorted(core)]
        positives=[]
        for J in withdrawals:
            F=Q-J
            loss=sum(1-fork_flow(*local(data,byroot[root],F))['value'] for root in roots)
            missing_vertices=sum(all(units[i] in J for i in (a,a+1) if i in E) for a in range(k))
            assert loss==missing_vertices
            excess=loss-len(J)
            assert (excess>0)==(J==core)
            if excess>0:assert excess==1;positives.append(J)
            if k<=5:
                extra={min(outside)}
                loss_extra=sum(1-fork_flow(*local(data,byroot[root],Q-J-extra))['value'] for root in roots)
                assert loss_extra==loss and loss_extra-len(J|extra)<=0
                totals['withdrawals_with_actual_inaccessible_units']+=1
            totals['full_pool_path_withdrawals']+=1
        assert positives==[core]
        totals['full_pool_unbounded_order_path_controls']+=1
    if write_fixture:
        fixture=dict(shape=cur[:2],selected_points=sorted(T),matching_edges=M,
            freezing_layers=layers,unique_matching_leaf_certificate=leaf,
            kinds=sorted(data[0].items()),pairs=data[1],links=data[2],resources=sorted(Q),
            support=[(o,sorted(js)) for o,js in data[3].items()],roots=roots,modules=module_tables,
            owner_links=sorted({(own[u],own[v]) for u,v in data[2] if own[u]!=own[v]}),
            reachable=sorted(seen),opened_units=sorted(units.values()),
            exact_fixed_P_maximum=optimum,constrained_exact_maximum=optimum-m,
            selected=len(T),value=m,cost=m,deficit=k-m,numerical_slack=2*k+m,
            availability='FULL original pool, no reservation; inaccessible actual originals remain present.')
        (Path(__file__).parent/'fixtures/extremal_full_pool_path.json').write_text(json.dumps(fixture,indent=2)+'\n')
    totals['fully_frozen_physical_boards']+=1;totals['strict_freezing_events']+=len(ranks)
    totals['unique_matching_forced_pairs']+=len(leaf)
    return dict(W=w,k=k,opened=sorted(E),fixed_P_maximum=optimum,selected=len(T),
        exact_constrained_maximum=optimum-m,raw=len(Q),value=m,deficit=k-m,min_links=m,
        slack=meta['slack'],full_path=is_path)


def mixed(w,totals):
    b=configuration(w,2);cur=(*b[:2],b[2]-{(w+1,11)},b[3])
    data,groups,I,rs,full=physical_model(cur);summary,compiled=compile_partition(cur,rs)
    assert compiled==full
    own,A,B,X=owner_data(*full[:2]);Q=full[4]
    assert (len(A),len(B),len(X),len(Q),summary['slack'])==(2,1,w//2+5,6,5)
    old=A-I;assert len(old)==len(I)==1
    assert (summary['local_closed_value'],summary['local_closed_cost'],summary['value'],summary['cost'],summary['deficit'])==(1,2,1,0,1)
    assert fork_flow(*restrict(full,I,Q))['value']==1
    assert fork_flow(*restrict(full,set(range(len(full[1])))-I,Q))['cost']==2
    seen,_=closure(full,A);assert len(seen)==8 and not seen&B
    assert set().union(set(),*(full[3][o] for o in seen))=={(w//2,11,11)}
    assert len(cur[2])==8*w+7
    totals['one_below_maximum_full_pool_mixed_interfaces']+=1
    return dict(W=w,selected=8*w+7,unconstrained_maximum=8*w+8,
        exact_maximum_with_open_singleton=8*w+7,full_pool_units=6,
        old_value=1,standalone_interface_value=1,full_value=1,theta=0,
        min_links=0,protected_min_links=2,numerical_slack=5)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();records=[]
    for w in (8,10):
        for k in range(1,6):
            for E in subsets(range(1,k)):
                records.append(inspect(w,k,E,totals,write_fixture=(w,k,E)==(8,3,{1,2})))
    for w,k in itertools.product((12,20,40,64),(2,4,8)):
        for E in {frozenset(),frozenset(range(1,k)),frozenset(range(1,k,2))}:
            records.append(inspect(w,k,set(E),totals))
    records.append(inspect(8,16,set(range(1,16)),totals))
    mixed_records=[mixed(w,totals) for w in (8,10,12,20,40,64,128)]
    report=dict(status='PASS',totals=dict(totals),physical_records=records,mixed_records=mixed_records,
        scope='Exact arbitrary-T constrained fixed-P maximum with specified BB seams; complete original-pool path circuits on frozen attainers; every maximum paid basis exact links; unique violating full-pool withdrawal; one-below-maximum positive-local-payment mixed interface.',
        limits=['All-parameter geometric statements have written proofs; finite checks corroborate.',
                'No claim for arbitrary endpoint replacement or failure under every band partition; this P family has vertical full compensation.',
                'Not a numerical target counterexample or universal5over6 improvement.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
