"""Geometric port budget and sharp all-q frozen families; written proof is primary."""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors,occupied_degrees
from check_component_receivers import endpoint_components,vertices_of
from check_even_bridge_support_completion import endpoints_of,tiles_of
from check_neutral_portal_strip_compensation import image_map
import check_occupied_strip_export_cancellation as previous
from check_occupied_strip_export_cancellation import inspect as joint_inspect,frozen_check
from check_residual_corridors import direct_check,transformed

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

CORE_T={(0,2),(0,4),(1,1),(1,5),(4,3),(4,5),(3,6)}
CORE_M=[((1,2),(1,3)),((1,4),(2,4)),((2,3),(3,3)),((3,4),(3,5))]
CORE_WITNESSES=[
    ((1,2),0,(0,2),(1,1)),((1,4),0,(0,4),(1,5)),
    ((3,5),0,(4,5),(3,6)),((2,3),1,(1,3),(2,4)),
    ((3,3),1,(4,3),(3,4)),((2,4),2,(2,3),(3,4)),
    ((3,4),2,(3,3),(2,4)),((1,3),3,(1,4),(2,3)),
]
FORCED=[((1,2),(1,3)),((1,4),(2,4)),((3,5),(3,4)),((2,3),(3,3))]


def family(q,sealed=False):
    assert q>=0
    row0=2 if sealed else 0
    move=lambda v,i:(v[0]+row0,v[1]+3+6*i)
    T={move(v,i) for i in range(q) for v in CORE_T}
    # Isolated selections join copies WITHOUT introducing another BB column.
    T|={(row0,3+6*i) for i in range(q+1)}
    T|={(r+row0,c) for r,c in ((0,1),(1,2),(2,0),(3,1))}
    M=[tuple(move(v,i) for v in e) for i in range(q) for e in CORE_M]
    M.append(((row0+1,1),(row0+2,1)))
    n=6*q+4+2*int(sealed)
    region=[((row0,c),(row0+1,c)) for c in range(n)]
    ranks=[tuple(move(v,i) if isinstance(v,tuple) else v for v in w)
           for i in range(q) for w in CORE_WITNESSES]
    ranks.extend([((row0+1,1),0,(row0,1),(row0+1,2)),
                  ((row0+2,1),0,(row0+2,0),(row0+3,1))])
    forced=[tuple(move(v,i) for v in e) for i in range(q) for e in FORCED]
    forced.append(M[-1])
    if sealed:
        c=6*q+4
        T|={(3,c),(0,c),(1,c+1)}
        M.append(((2,c),(1,c)))
        ranks.extend([((2,c),0,(3,c),(2,c-1)),((1,c),0,(0,c),(1,c+1))])
        forced.append(M[-1])
    cur=(8 if sealed else 6,n,T,M)
    return cur,region,ranks,forced


def inspect_budget(cur,regions,counts):
    """Rebuild and allocate actual BB/TT forest END incidences, once each."""
    result=joint_inspect(cur,regions,counts)
    T=cur[2];P=endpoints_of(cur);mate={v:w for e in cur[3] for v,w in (e,e[::-1])}
    B=D4=A=V=old_unused=0
    for region in regions:
        cells={v for col in region for v in col}
        labels=[('BB' if not set(col)&(T|P) else 'TT' if set(col)<=T else 'other') for col in region]
        pending={i for i,s in enumerate(labels) if s!='other'};slots=set();K=0
        while pending:
            stack=[min(pending)];component=set()
            while stack:
                j=stack.pop()
                if j in component:continue
                component.add(j);pending.discard(j)
                stack.extend(k for k in (j-1,j+1) if k in pending and (labels[j]=='TT' or labels[k]=='TT'))
            lo,hi=min(component),max(component)
            assert labels[lo]==labels[hi]=='BB'
            slots|={(lo,-1),(hi,1)};K+=1
        b=1+int(labels[-1]=='BB')
        protected={(0,-1)}|({(len(region)-1,1)} if b==2 else set())
        assert protected<=slots and len(slots)==2*K
        allocated=set();a=d4=e=0
        for j,col in enumerate(region):
            if len(set(col)&T)!=1 or len(set(col)&P)!=1:continue
            v=next(iter(set(col)&P))
            if mate[v] in cells:continue
            e+=1
            ports=[(k,1 if k<j else -1) for k in (j-1,j+1) if 0<=k<len(region) and labels[k]=='BB']
            if ports:
                chosen=min(ports);assert chosen in slots-protected-allocated
                allocated.add(chosen);a+=1
            else:
                assert len(set(neighbors(v))&(T|P))==4
                d4+=1
        assert e==a+d4
        v=2*K-b-a;assert v==len(slots-protected-allocated)>=0
        local=previous.inspect_strip(cur,region,Counter())
        assert local['mixed_exports']==e
        assert local['surplus_twice']==b+local['unused_bp']+v-d4
        B+=b;D4+=d4;A+=a;V+=v;old_unused+=local['unused_bp']
    assert old_unused==result['safe_cross']+result['unused_BP']
    assert result['surplus_twice']==B+result['safe_cross']+result['unused_BP']+V-D4
    assert result['surplus_twice']>=B+result['safe_cross']+result['unused_BP']-D4
    counts['geometric_port_budget_models']+=1
    counts['ported_export_forest_ends_allocated']+=A
    counts['unported_degree_four_TP_exports']+=D4
    result['degree_four_budget']=dict(boundary_ends=B,unported_degree_four_TP=D4,
        ported_exports=A,unused_forest_end_slots=V,
        bound_surplus_twice=B+result['safe_cross']+result['unused_BP']-D4)
    return result


def check_ranks(cur,records):
    P=endpoints_of(cur);T=cur[2]
    mate={v:w for e in cur[3] for v,w in (e,e[::-1])}
    rank={v:k for v,k,a,b in records}
    assert set(rank)==P and len(records)==len(P)
    for v,k,a,b in records:
        assert a!=b and {a,b}<=set(neighbors(v)) and mate[v] not in (a,b)
        assert all(w in T or w in P and rank[mate[w]]<k for w in (a,b))


def unique_by_leaves(cur,order):
    """A leaf of the remaining induced P graph forces its mate in ANY matching."""
    left=endpoints_of(cur);actual={frozenset(e) for e in cur[3]}
    for v,w in order:
        assert v in left and set(neighbors(v))&left=={w}
        assert frozenset((v,w)) in actual
        left-={v,w}
    assert not left


def count_matchings(P):
    if not P:return 1
    v=min(P)
    return sum(count_matchings(P-{v,w}) for w in set(neighbors(v))&P)


def inspect(q,sealed,counts):
    cur,region,ranks,forced=family(q,sealed);z=int(sealed)
    direct_check(*cur);P=endpoints_of(cur);T=cur[2]
    b=1+z
    assert Counter(occupied_degrees(cur).values())==Counter({3:7*q+2*b,4:q})
    check_ranks(cur,ranks);unique_by_leaves(cur,forced)
    frozen_check(cur,counts)
    joint=inspect_budget(cur,[region],counts)
    U={v for col in region for v in col};Q=tiles_of(P);R=vertices_of(Q)
    comps=endpoint_components(cur)
    assert len(comps)==q+b and sorted(map(len,comps))==[2]*b+[8]*q
    assert len(T)==8*q+2+3*b and len(cur[3])==4*q+b and len(P)==8*q+2*b
    assert len(T&U)==5*q+2+b and len(P&U)==3*q+b
    assert joint['forest_components']==b and joint['boundary_budget']==b
    assert joint['outside']==q+b and joint['unused_BP']==0
    assert joint['TP_TP']==joint['TP_PP']==joint['safe_cross']==0
    assert joint['surplus_twice']==b-q
    assert joint['degree_four_budget']==dict(boundary_ends=b,unported_degree_four_TP=q,
        ported_exports=b,unused_forest_end_slots=0,bound_surplus_twice=b-q)
    assert joint['physical_ledger']==dict(endpoint_free_deficit=0,raw_receiver_charge_twice=q-b)
    assert joint['union_tile_closed']
    assert not set(region[0])&(T|P) and not set(region[-1])<=(T|P)
    assert bool(not set(region[-1])&(T|P))==sealed
    # Distinct original receiver tiles, including all negative outside pieces.
    seen=set();inside_raw=outside_raw=0;capacity_two=0
    for comp in comps:
        tiles=tiles_of(comp);cells=vertices_of(tiles)
        assert not seen&tiles;seen|=tiles
        assert len(tiles) in (2,4)
        assert 2*len(T&cells)+len(comp)-4*len(tiles)==0
        A=cells&U;B=cells-U
        ar=2*len(T&A)+len(P&A)-len(A);br=2*len(T&B)+len(P&B)-len(B)
        assert (ar,br)==((1,-1) if len(comp)==8 else (-1,1))
        inside_raw+=ar;outside_raw+=br
        capacity_two+=sum(len(P&vertices_of({tile}))==4 for tile in tiles)
    all_tiles=set(itertools.product(range(cur[0]//2),range(cur[1]//2)))
    u_tiles=tiles_of(U);out_empty=all_tiles-u_tiles-Q
    D_out=sum(2-len(T&vertices_of({tile})) for tile in out_empty)
    global_twice=cur[0]*cur[1]-2*direct_check(*cur)
    assert D_out==(12*q+14 if sealed else 6*q+6)
    assert global_twice==2*D_out
    assert global_twice==joint['surplus_twice']+2*D_out-outside_raw
    assert len(Q)==4*q+2*b and len(T&R)==4*q+3*b and capacity_two==q
    # Every complete receiver is neutral; inside/outside charges sum to zero.
    assert inside_raw==q-b and outside_raw==b-q
    counts['all_q_frozen_models']+=1
    counts['forced_unique_matching_edges']+=4*q+b
    if joint['surplus_twice']<0:counts['negative_regional_models']+=1
    if q<=2:
        assert count_matchings(P)==1;counts['independent_unique_matching_counts']+=1
    return cur,region,dict(copies=q,sealed=sealed,shape=cur[:2],T=len(T),M=len(cur[3]),
        regional_selected=len(T&U),regional_endpoints=len(P&U),
        record={k:v for k,v in joint.items() if k not in ('bad_edges','safe_cross_edges','parallel_square_witnesses')},
        complete_receiver_charge_twice=0,outside_raw_receiver_charge_twice=b-q,
        outside_endpoint_free_deficit=D_out,whole_margin_twice=global_twice)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    counts=Counter();samples=[]
    for q in (0,1,2,3,4,5,8,16,64,128):
        for sealed in (False,True):
            cur,region,record=inspect(q,sealed,counts)
            if q in (0,2,3,128):samples.append(record)
            if q in (0,2,5):
                for symmetry in itertools.product((False,True),repeat=3):
                    shape,T,M=transformed(*cur,*symmetry);f=image_map(*cur[:2],symmetry)
                    image=(*shape,T,M);new_region=[tuple(f(v) for v in col) for col in region]
                    new=inspect_budget(image,[new_region],counts);frozen_check(image,counts)
                    assert Counter(occupied_degrees(image).values())==Counter(occupied_degrees(cur).values())
                    for k in ('surplus_twice','outside','forest_components','unused_BP','boundary_budget'):
                        assert new[k]==record['record'][k]
                    counts['isometry_controls']+=1
    # Independent existing frozen, feasible, mixed-direction and exhaustive controls.
    previous.inspect=inspect_budget
    previous.local_controls(counts);previous.frozen_families(counts)
    previous.exhaustive_two_strip_controls(counts);previous.mixed_region_controls(counts)
    fixture_path=Path('develop/fixtures/frozen_strip_degree_four_sharp_q2.json')
    fixture=json.loads(fixture_path.read_text());cur,region,ranks,forced=family(2)
    assert fixture['shape']==list(cur[:2])
    assert {tuple(v) for v in fixture['selected']}==cur[2]
    assert {frozenset(map(tuple,e)) for e in fixture['matching']}=={frozenset(e) for e in cur[3]}
    assert fixture['region']==json.loads(json.dumps(region))
    check_ranks(cur,[(tuple(v),k,tuple(a),tuple(b)) for v,k,a,b in fixture['strict_rank_witnesses']])
    unique_by_leaves(cur,[tuple(map(tuple,e)) for e in fixture['forced_leaf_order']])
    assert fixture['regional_surplus_twice']==-1
    report=dict(status='PASS',counts=dict(counts),samples=samples,
        scope='General physical forest-end injection and exact occupied-strip degree-four budget; all-q sharp frozen uniquely matched constructions. Seven degree-three and one degree-four endpoint per eight-endpoint core. All full receivers neutral, all regional endpoint-free tiles saturated, one original capacity-two tile per core. Finite checks corroborate the written general proofs; no universal grid-bound improvement.')
    a.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__=='__main__':main()
