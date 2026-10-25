"""Frozen no-isolated-selection obstruction and exact narrow-strip direction repair.

All-parameter proof: docs/ISOLATED_COVERAGE_OBSTRUCTION_AND_STRIP_REPAIR.md.
No claim of a counterexample to the numerical grid bound or every partition.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_forced_mates_and_adjacent_maxima import configuration,uniform_freezing,forced_order,verify_forced_mates
from check_isolated_repair_selection import isolated
from check_crossing_matching_ports import rectangle,compile_partition
from check_compensation_flow_normal_form import owner_data
from check_full_pool_interface_profile import closure
from check_interface_reserve_reoptimization import constrained_primitive,subsets
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def regions_for(w,k,flips):
    R=w+2;regions=[]
    for a in range(k):
        c=10*a
        regions.extend([rectangle(0,R,c,c+2,True),rectangle(0,R,c+2,c+4,a in flips),
                        rectangle(0,R,c+4,c+10,True)])
    regions.append(rectangle(0,R,10*k,10*k+2,True))
    return regions


def inspect(w,k,removed,flips,totals,save=False):
    base=configuration(w,k);X=set(isolated(base));assert removed<=X
    assert len(X)==k*(5*w//2-9)+w-6
    P0={v for e in base[3] for v in e}
    near=Counter(r for r,c in base[2] if any((r+dr,c+dc) in P0 for dr,dc in ((0,1),(0,-1),(1,0),(-1,0))))
    assert near[0]+near[w+1]==8*k and near[1]+near[w]==4*k
    assert near[2]==k and near[3]==2*k and near[w-2]==k+1
    assert sum(near[r] for r in range(5,w-2,2))==k*(w-6)-1
    assert sum(near.values())==k*(w+10)
    cur=(*base[:2],base[2]-removed,base[3]);ranks,layers=uniform_freezing(w,k,cur)
    direct_check(*cur)
    P={v for e in cur[3] for v in e};assert frozen_certificate(cur)[0]==P
    assert set(isolated(cur))==X-removed
    rec,data=compile_partition(cur,regions_for(w,k,flips));own,A,B,M=owner_data(*data[:2])
    assert (len(A),len(B),len(M))==(k,k,k*(w//2-2))
    assert len(rec['crossing_edges'])==2*k
    assert rec['local_inventory']['CT']==2*k and rec['local_inventory']['CC']==k
    assert rec['local_inventory'].get('TT',0)==0 and rec['interface']=={'TT':k}
    assert rec['local_closed_value']==0
    assert (rec['raw'],rec['slack'])==(2*k+len(removed),2*k+len(removed))
    assert (rec['value'],rec['deficit'],rec['cost'])==(len(flips),k-len(flips),0)
    assert rec['reserved_interface_payments']==len(flips)
    roots=[];guards=[]
    # Full N[P] components and all tip types are literally unchanged by
    # flipping the narrow strips; only supports and band links can change.
    vertical_regions=regions_for(w,k,set(range(k)))
    vrec,vertical=compile_partition(cur,vertical_regions)
    assert data[:2]==vertical[:2]
    for a in range(k):
        c=10*a;root=own[(1,c+3)];assert root in A
        assert set(data[1][root])=={(1,c+3),(w,c+3)};roots.append(root)
        seen,edges=closure(data,{root});assert seen=={root} and not edges[root]
        if a not in flips:
            assert data[3][root]==set()
        else:
            b=sum(len(region['bands']) for region in regions_for(w,k,flips)[:3*a+1])
            top=(b,2,2);bottom=(b,w-1,w-1)
            assert top!=bottom and {top,bottom}<=data[3][root]
            for j in (top,bottom):
                assert {o for o,js in data[3].items() if j in js}=={root}
            guards.append((a,top,bottom))
        # All four seals are selected and adjacent to P, hence never in X.
        seals=[((0,c+3),(1,c+3)),((1,c+2),(1,c+3)),
               ((w,c+2),(w,c+3)),((w+1,c+3),(w,c+3)),
               ((0,c+5),(1,c+5)),((w+1,c+5),(w,c+5))]
        assert all(t in cur[2] and p in P and t not in X for t,p in seals)
        totals['exact_single_owner_source_closures']+=1
    assert set(roots)==A
    if w<=10 and k<=4:
        assert constrained_primitive(data,set())==(len(flips),0)
        totals['independent_primitive_value_cost_profiles']+=1
    if removed==X:
        assert len(cur[2])==k*(w+12)+8
        assert rec['slack']==k*(5*w//2-7)+w-6
        assert not isolated(cur)
        totals['fully_frozen_boards_with_no_isolated_T']+=1
    if save:
        fixture=dict(W=w,k=k,shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],
            removed=sorted(removed),all_isolated_candidates=sorted(X),flipped=sorted(flips),
            freezing_layers=layers,unique_matching_leaf_certificate=verify_forced_mates(cur,forced_order(w,k)),
            region_bounds=[dict(bounds=r['bounds'],vertical=r['vertical']) for r in regions_for(w,k,flips)],
            pairs=data[1],kinds=sorted(data[0].items()),links=data[2],
            supports=[(o,sorted(js)) for o,js in data[3].items()],resources=sorted(data[4]),
            roots=roots,owner_links=sorted({(own[u],own[v]) for u,v in data[2] if own[u]!=own[v]}),
            inventory=dict(alpha=len(A),beta=len(B),mixed=len(M),value=rec['value'],deficit=rec['deficit'],
                cost=rec['cost'],raw=rec['raw'],slack=rec['slack'],actual_crossings=len(rec['crossing_edges'])))
        (Path(__file__).parent/'fixtures/isolated_coverage_obstruction.json').write_text(json.dumps(fixture,indent=2)+'\n')
    totals['physical_partition_models']+=1;totals['strict_freezing_events']+=len(ranks)
    return dict(W=w,k=k,removed=len(removed),candidates=len(X),flips=sorted(flips),
                selected=len(cur[2]),value=rec['value'],deficit=rec['deficit'],raw=rec['raw'],slack=rec['slack'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();records=[];rng=random.Random(20261025)
    for w in (8,10):
        for k in range(1,6):
            X=set(isolated(configuration(w,k)))
            deletions=[set(),X,{x for x in X if sum(x)%2==0}]
            for removed,F in itertools.product(deletions,subsets(range(k))):
                records.append(inspect(w,k,removed,F,totals,save=(w,k,removed,F)==(8,2,X,set())))
    for w,k in itertools.product((12,20,40,64),(1,3,8,16)):
        X=set(isolated(configuration(w,k)))
        for removed in [set(),X,{x for x in X if rng.randrange(2)}]:
            for F in {frozenset(),frozenset(range(k)),frozenset(range(0,k,2))}:
                records.append(inspect(w,k,removed,set(F),totals))
    # Finite all-subset control is on an explicitly chosen small candidate
    # subset; the general all-X assertion is the written single-owner proof.
    cur=configuration(8,1);chosen=isolated(cur)[:6]
    for Y in subsets(chosen):inspect(8,1,Y,set(),totals)
    totals['exhaustive_six_candidate_subsets']=2**len(chosen)
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,
        scope='All-W/k written mixed-partition obstruction for every isolated deletion subset; no-isolated fully frozen specialization; exact arbitrary-subset direction flips at unchanged P/T/M and source identities.',
        limits=['Finite checks corroborate the general proof.',
                'Failure is in the fixed conservative local-band network; all-vertical repartition fully pays.',
                'Not a grid numerical counterexample, no new universal5over6 bound.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
