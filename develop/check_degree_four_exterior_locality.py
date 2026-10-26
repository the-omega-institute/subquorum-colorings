"""Arbitrary-distance D4 exterior-donor obstruction; no discovery solver required.

Written all-h proof: docs/DEGREE_FOUR_EXTERIOR_LOCALITY_OBSTRUCTION.md.
Resources are original physical tiles, shared by both selected vertical strips.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_four_outward_slab import slab, freezing_schedule
from check_component_receivers import endpoint_components
from check_occupied_strip_degree_four_budget import inspect_budget
from check_occupied_strip_export_cancellation import frozen_check
from check_promotion_cores import frozen_certificate
from check_cooperative_promotion import neighbors
from check_residual_corridors import direct_check, transformed
from check_neutral_portal_strip_compensation import image_map

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def construction(h):
    assert h >= 1
    L, _, baseT, baseM = slab(h)
    lower = lambda v: (L+2+v[0], v[1]+1)
    upper = lambda v: (L+1-v[0], v[1]+1)
    T = {f(v) for f in (lower, upper) for v in baseT}
    # These supports conflict with the lower copy across the join. Their
    # replacement witnesses are actual lower endpoints, not new selections.
    removed = {upper((0,1)), upper((0,6))}
    T -= removed
    # Saturate the added outer tile columns. The two selections at each join
    # form a selected pair; all other added selections are isolated.
    T |= {f((r,c)) for f in (lower,upper) for r in range(0,L,2) for c in (-1,8)}
    M = [tuple(f(v) for v in edge) for f in (lower,upper) for edge in baseM]
    cur = (2*L+2, 10, T, M)
    regions = [[((r,c),(r,c+1)) for r in range(cur[0])] for c in (2,6)]
    schedule = [[lower(v) for v in wave] for wave in freezing_schedule(h)]
    schedule += [[upper(v) for v in wave] for wave in freezing_schedule(h)]
    sources = [lower((0,2)), lower((0,5))]
    return cur, regions, schedule, sources


def replay_schedule(cur, schedule):
    """Replay the written nine waves twice, preserving true mate identities."""
    T=cur[2]; P={v for e in cur[3] for v in e}
    mate={v:w for e in cur[3] for v,w in (e,e[::-1])}
    seen=set(); records=[]
    for rank, wave in enumerate(schedule):
        assert len(wave)==len(set(wave)) and set(wave)<=P-seen
        for v in wave:
            retained=sorted(w for w in neighbors(v) if w!=mate[v] and
                            (w in T or w in P and mate[w] in seen))
            assert len(retained)>=2, (v,rank,retained)
            records.append((v,rank,*retained[:2]))
        seen.update(wave)
    assert seen==P
    return records


def raw_tiles(cur):
    R,C,T,M=cur;P={v for e in M for v in e}
    return {(a,b):4-2*len(T&cells)-len(P&cells)
            for a,b in itertools.product(range(R//2),range(C//2))
            for cells in [{(2*a+i,2*b+j) for i,j in itertools.product(range(2),repeat=2)}]}


def inspect(h, counts):
    cur,regions,schedule,sources=construction(h);R,C,T,M=cur
    P={v for e in M for v in e}; mate={v:w for e in M for v,w in (e,e[::-1])}
    assert (R,C,len(T),len(M),len(P))==(4*h+10,10,12*h+26,8*h+10,16*h+20)
    objective=direct_check(*cur)
    assert R*C//2-objective==14
    records=replay_schedule(cur,schedule)
    counts['written_schedule_events']+=len(records)
    frozen_check(cur,counts)
    joint=inspect_budget(cur,regions,counts)
    assert joint['degree_four_budget']==dict(boundary_ends=2,unported_degree_four_TP=2,
        ported_exports=0,unused_forest_end_slots=6,bound_surplus_twice=2)
    assert joint['surplus_twice']==8 and joint['unused_BP']==2 and joint['safe_cross']==0
    U={v for reg in regions for col in reg for v in col}
    assert len(T&U)==4*h+10 and len(P&U)==8*h+12
    assert len(endpoint_components(cur))==1
    allp=[]
    for a,b in itertools.product(range(R//2),range(C//2)):
        cells={(2*a+i,2*b+j) for i,j in itertools.product(range(2),repeat=2)}
        if cells<=P:
            allp.append(2-sum(set(e)<=cells for e in M))
    assert len(allp)==2*h+2
    assert Counter(allp)==(Counter({1:2,0:2}) if h==1 else Counter({1:6,2:2*h-4}))
    for reg in regions:
        cells={v for col in reg for v in col}
        assert len(cells)-2*len(T&cells)-len(P&cells)==4
    for v in sources:
        assert v in P and len(set(neighbors(v))&(T|P))==4 and mate[v] not in U
    raw=raw_tiles(cur);ut={(r//2,c//2) for r,c in U}
    expected={(0,b):4 for b in range(5)}
    expected.update({(1,2):4,(2*h+4,2):4,(h+2,1):2,(h+2,3):2})
    expected.update({(a,b):-1 for a in (1,2*h+4) for b in (1,3)})
    assert raw=={q:expected.get(q,0) for q in raw}
    outside_positive={q:c for q,c in raw.items() if q not in ut and c>0}
    assert outside_positive=={(0,0):4,(0,2):4,(0,4):4,(1,2):4,(2*h+4,2):4}
    assert all(c>=0 for q,c in raw.items() if q not in ut)
    assert sum(outside_positive.values())==20
    assert sum(raw.values())==28==joint['surplus_twice']+20
    distances=[]
    for v in sources:
        q=(v[0]//2,v[1]//2)
        cheb=min(max(abs(q[j]-p[j]) for j in (0,1)) for p in outside_positive)
        taxicab=min(sum(abs(q[j]-p[j]) for j in (0,1)) for p in outside_positive)
        assert cheb==h+1 and taxicab==h+2
        distances.append(dict(source=v,tile=q,nearest_chebyshev=cheb,nearest_manhattan=taxicab))
    counts['all_h_models']+=1
    counts['degree_four_sources']+=len(sources)
    return cur,regions,records,dict(h=h,shape=cur[:2],selected=len(T),matching=len(M),
        endpoints=len(P),whole_surplus=14,regional_surplus_twice=8,
        D4=2,connected_endpoint_components=1,original_all_P_tiles=len(allp),
        original_capacity_two_tiles=allp.count(2),internal_half_unit_budget=10,outside_positive_half_units=20,
        outside_positive_tiles=[dict(tile=q,half_units=c) for q,c in outside_positive.items()],
        source_distances=distances,written_freezing_waves=len(schedule))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    p.add_argument('--write-fixture',action='store_true');a=p.parse_args()
    counts=Counter();samples=[]
    for h in (*range(1,17),24,32,64,128):
        cur,regions,records,report=inspect(h,counts)
        if h in (1,2,4,16,128):samples.append(report)
        if h in (1,2,4):
            raw=raw_tiles(cur)
            for symmetry in itertools.product((False,True),repeat=3):
                shape,T,M=transformed(*cur,*symmetry);f=image_map(*cur[:2],symmetry)
                image=(*shape,T,M);newregions=[[tuple(f(v) for v in col) for col in reg] for reg in regions]
                joint=inspect_budget(image,newregions,counts);frozen_check(image,counts)
                assert joint['surplus_twice']==8 and joint['degree_four_budget']['unported_degree_four_TP']==2
                assert sorted(raw_tiles(image).values())==sorted(raw.values())
                counts['isometry_controls']+=1
    cur,regions,records,report=inspect(2,counts)
    fixture=dict(scope='All-h proof witness h=2: both actual D4 exports have no positive raw-surplus original tile outside the joint two-strip region at Chebyshev distance <=2. Complete freezing and regional internal budget10 pay both D4; this refutes unconditional pointwise radius-two exterior-donor access, not residual compensation or the grid bound.',
        h=2,shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],regions=regions,
        strict_rank_witnesses=records,report=report)
    fp=Path('develop/fixtures/frozen_degree_four_remote_exterior_h2.json')
    if a.write_fixture:fp.write_text(json.dumps(fixture,indent=2)+'\n')
    assert json.loads(fp.read_text())==json.loads(json.dumps(fixture))
    out=dict(status='PASS',counts=dict(counts),samples=samples,
        scope='All-h written construction, actual feasibility, two nine-wave freezing schedules with two true lower-endpoint replacements, exact original-tile ledger, arbitrary-distance pointwise D4 exterior access obstruction. Internal budget10 covers D4=2; no counterexample to residual-capacity routing, grid target or 5/6.')
    a.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__=='__main__':main()
