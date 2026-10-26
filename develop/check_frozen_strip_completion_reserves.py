"""Sharp all-selection bound and physical no-reuse reserves for frozen D4 strips.

The written proof is a disjoint geometric cover, not finite enumeration.
"""
import argparse
from collections import Counter
import itertools
import json
import random
from pathlib import Path

from check_occupied_strip_degree_four_budget import family,check_ranks,unique_by_leaves,inspect_budget
from check_occupied_strip_export_cancellation import complete_fixed_strip,frozen_check
from check_cooperative_promotion import neighbors
from check_even_bridge_support_completion import endpoints_of,tiles_of
from check_component_receivers import vertices_of
from check_residual_corridors import direct_check,transformed
from check_neutral_portal_strip_compensation import image_map

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

MODULE_P={(1,1),(1,2),(1,3),(2,2),(2,3),(3,2),(3,3),(3,4)}
MODULE_FORBIDDEN={(2,1),(2,4)}
MODULE_FACES=[(0,4),(4,0),(4,4)]
MODULE_PAIRS=[((3,1),(3,0)),((4,3),(5,3)),((0,3),(0,2)),
              ((0,1),(0,0)),((1,0),(2,0)),((3,5),(2,5)),((4,2),(5,2))]
CAP_P={(1,1),(2,1)}
CAP_FACES=[(0,2),(2,2),(4,0),(4,2)]
CAP_PAIRS=[((0,1),(0,0)),((3,1),(3,0)),((1,0),(2,0))]


def face(r,c):return {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}


def check_cover(P,forbidden,faces,pairs,width):
    cells=set(itertools.product(range(6),range(width)));seen=set(P)|set(forbidden)
    assert len(seen)==len(P)+len(forbidden)
    for v in forbidden:assert len(set(neighbors(v))&P)>=2
    for r,c in faces:
        F=face(r,c);assert not seen&F;seen|=F
        # Any three square corners contain a vertex with two neighbours.
        for triple in itertools.combinations(F,3):
            assert any(len(set(neighbors(v))&set(triple))==2 for v in triple)
    for a,b in pairs:
        assert b in neighbors(a) and set(neighbors(a))&P
        assert not seen&{a,b};seen|={a,b}
    assert seen==cells
    return 2*len(faces)+len(pairs)


def completion(k):
    cur,region,ranks,forced=family(k)
    w=cur[1]
    T={(0,c) for c in range(1,w,2)}|{(1,2)}
    T|={(1,c) for i in range(k) for c in (4+6*i,8+6*i)}
    T|={(2,0),(2,3),(3,1),(3,3)}
    T|={(3,c) for i in range(k) for c in (5+6*i,9+6*i)}
    T|={(4,c) for c in range(0,w,2)}|{(5,0)}|{(5,c) for c in range(3,w,2)}
    assert cur[2]<=T
    return (*cur[:2],T,cur[3]),region,ranks,forced


def upper_certificate(cur):
    """Check the local cover against an arbitrary feasible selected set."""
    h,w,T,M=cur;assert h==6 and (w-4)%6==0;k=(w-4)//6
    direct_check(*cur);P=endpoints_of(cur);seen=set();upper=0
    for start,width,footprint,forbidden,faces,pairs in [
        (0,4,CAP_P,set(),CAP_FACES,CAP_PAIRS)]+[
        (4+6*i,6,MODULE_P,MODULE_FORBIDDEN,MODULE_FACES,MODULE_PAIRS) for i in range(k)]:
        shift=lambda v:(v[0],v[1]+start)
        cells={(r,c+start) for r,c in itertools.product(range(6),range(width))}
        assert not seen&cells;seen|=cells
        assert P&cells=={shift(v) for v in footprint}
        assert not T&{shift(v) for v in forbidden}
        local=0
        for r,c in faces:
            z={shift(v) for v in face(r,c)};assert len(T&z)<=2;local+=2
        for a,b in pairs:
            assert len(T&{shift(a),shift(b)})<=1;local+=1
        assert len(T&cells)<=local;upper+=local
    assert seen==set(itertools.product(range(h),range(w))) and upper==13*k+11
    assert len(T)<=upper
    return upper


def check_retained_extension(cur,k,counts):
    old,region,ranks,forced=family(k)
    assert cur[:2]==old[:2] and cur[3]==old[3] and old[2]<=cur[2]
    direct_check(*cur);check_ranks(cur,ranks);upper_certificate(cur)
    P=endpoints_of(cur);T=cur[2];U={v for col in region for v in col}
    assert T&U==old[2]&U
    outside=set(itertools.product(range(3),range(cur[1]//2)))-tiles_of(U)
    Q=tiles_of(P);raw={q:4-2*len(T&vertices_of({q}))-len(P&vertices_of({q})) for q in outside&Q}
    assert raw=={(1,0):-1,**{(1,3+3*i):0 for i in range(k)},**{(1,4+3*i):1 for i in range(k)}}
    donors={(1,2+3*i) for i in range(k)}
    free=outside-Q;assert donors<=free
    deficit={q:2-len(T&vertices_of({q})) for q in free}
    assert all(c>=0 for c in deficit.values()) and all(deficit[q]>=1 for q in donors)
    assert sum(deficit.values())>=k
    assert cur[0]*cur[1]//2-len(T)-len(cur[3])==sum(deficit.values())
    counts['retained_extension_models']+=1;counts['retained_rank_events']+=len(P)


def retained_controls(counts):
    for k in (0,1,2,4,8):
        base=family(k)[0];P=endpoints_of(base);maxT=completion(k)[0][2]
        for seed in range(8):
            rng=random.Random(7100+31*k+seed)
            partial=base[2]|{v for v in sorted(maxT-base[2]) if rng.randrange(2)}
            check_retained_extension((*base[:2],partial,base[3]),k,counts)
            chosen=set(base[2]);candidates=sorted(set(itertools.product(range(6),range(base[1])))-P-chosen)
            rng.shuffle(candidates)
            for v in candidates:
                trial=chosen|{v};O=trial|P
                if all(len(set(neighbors(t))&O)<=1 for t in trial):chosen.add(v)
            check_retained_extension((*base[:2],chosen,base[3]),k,counts)


def inspect(k,counts):
    cur,region,ranks,forced=completion(k);P=endpoints_of(cur);T=cur[2]
    direct_check(*cur);check_ranks(cur,ranks);unique_by_leaves(cur,forced)
    frozen_check(cur,counts);joint=inspect_budget(cur,[region],counts)
    upper=upper_certificate(cur);assert len(T)==upper==13*k+11
    assert joint['surplus_twice']==1-k and joint['degree_four_budget']==dict(
        boundary_ends=1,unported_degree_four_TP=k,ported_exports=1,unused_forest_end_slots=0,bound_surplus_twice=1-k)
    assert joint['unused_BP']==0 and len(cur[3])==4*k+1
    U={v for col in region for v in col};Q=tiles_of(P)
    alltiles=set(itertools.product(range(3),range(cur[1]//2)))
    outside=alltiles-tiles_of(U);free=outside-Q
    deficit={q:2-len(T&vertices_of({q})) for q in free}
    donors={(1,2+3*i) for i in range(k)}
    assert {q for q,c in deficit.items() if c>0}==donors
    assert all(deficit[q]==1 for q in donors) and sum(deficit.values())==k
    # Exact endpoint-bearing outside pieces: one half unit per D4, and
    # one half-unit boundary demand paid from the internal b=1 budget.
    raw={q:4-2*len(T&vertices_of({q}))-len(P&vertices_of({q})) for q in outside&Q}
    rebates={(1,4+3*i) for i in range(k)}
    assert raw=={(1,0):-1,**{(1,3+3*i):0 for i in range(k)},**{q:1 for q in rebates}}
    assert donors.isdisjoint(rebates) and len(donors)==len(rebates)==k
    assert cur[0]*cur[1]//2-len(T)-len(cur[3])==k
    assert joint['surplus_twice']+sum(raw.values())+2*sum(deficit.values())==2*k
    counts['sharp_all_k_models']+=1
    counts['distinct_physical_unit_reserves']+=k
    if k<=5:
        # Independently optimize both all reselections and retained extensions.
        for retain in (False,True):
            base=family(k)[0] if retain else (*cur[:2],set(),cur[3])
            optimal,value=complete_fixed_strip(base,0,6,0,cur[1],set())
            assert value==upper
            upper_certificate(optimal);counts['independent_column_DP_optima']+=1
    return cur,region,ranks,dict(k=k,shape=cur[:2],selected=len(T),matching=len(cur[3]),
        endpoints=len(P),maximum_T_over_all_feasible_reselections=upper,
        whole_surplus=k,regional_surplus_twice=1-k,internal_half_unit_budget=1,D4=k,
        outside_boundary_half_unit_demand=1,distinct_core_half_unit_rebates=k,
        distinct_endpoint_free_unit_reserves=k,
        selected_region=len(T&U),endpoint_region=len(P&U))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--write-fixture',action='store_true');a=p.parse_args()
    assert check_cover(MODULE_P,MODULE_FORBIDDEN,MODULE_FACES,MODULE_PAIRS,6)==13
    assert check_cover(CAP_P,set(),CAP_FACES,CAP_PAIRS,4)==11
    counts=Counter();samples=[]
    retained_controls(counts)
    for k in (*range(17),32,64,128):
        cur,region,ranks,report=inspect(k,counts)
        if k in (0,1,2,4,16,128):samples.append(report)
        if k in (0,2,4):
            for sym in itertools.product((False,True),repeat=3):
                shape,T,M=transformed(*cur,*sym);f=image_map(*cur[:2],sym)
                image=(*shape,T,M);reg=[tuple(f(v) for v in col) for col in region]
                z=inspect_budget(image,[reg],counts);frozen_check(image,counts)
                assert z['surplus_twice']==1-k
                counts['isometry_controls']+=1
    cur,region,ranks,report=inspect(2,counts)
    fixture=dict(scope='k=2 sharp global T optimum for the fixed actual endpoint footprint: 37T/9M/18P, all frozen, negative occupied strip surplus -1/2, two distinct exterior half rebates pay D4 and boundary budget pays its demand, two distinct full-unit endpoint-free reserves remain.',
        k=2,shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],region=region,strict_rank_witnesses=ranks,report=report)
    fp=Path('develop/fixtures/frozen_strip_sharp_maximum_k2.json')
    if a.write_fixture:fp.write_text(json.dumps(fixture,indent=2)+'\n')
    assert json.loads(fp.read_text())==json.loads(json.dumps(fixture))
    out=dict(status='PASS',counts=dict(counts),samples=samples,
        scope='General written disjoint cell cover gives T<=13k+11 for EVERY feasible reselected T with this fixed P, with no freezing/retained-T hypothesis for the upper bound. Explicit all-k completion retains old T and freezing and attains the bound, keeps regional2S=1-k, gives exact distinct physical compensation plus k unused whole units. General grid coverage and universal5/6 improvement remain open.')
    a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__=='__main__':main()
