"""Joint TP/BP matching flux across disjoint occupied strips.

Proof: docs/OCCUPIED_STRIP_EXPORT_CANCELLATION.md.
Enumeration is an independent implementation/geometry check, not the proof.
"""
import argparse
from collections import Counter,defaultdict
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_occupied_strip_matching_flux import inspect as inspect_strip,physical_ledger
from check_cooperative_promotion import neighbors,occupied_degrees
from check_component_receivers import endpoint_components,vertices_of
from check_even_bridge_support_completion import endpoints_of,tiles_of
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_neutral_portal_strip_compensation import image_map

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def inspect(current,regions,counts):
    direct_check(*current)
    T=current[2];P=endpoints_of(current);mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    columns={};where={};local=[];union=set();K=delta=C=D=exports=0
    for i,region in enumerate(regions):
        # Ordered geometric two-row/two-column rectangle, allowing reversal.
        assert len(region)>=2 and all(len(c)==2 for c in region)
        a,b=region[0];across=(b[0]-a[0],b[1]-a[1])
        step=(region[1][0][0]-a[0],region[1][0][1]-a[1])
        assert abs(across[0])+abs(across[1])==1
        assert abs(step[0])+abs(step[1])==1 and across[0]*step[0]+across[1]*step[1]==0
        assert region==[tuple((a[0]+j*step[0]+k*across[0],a[1]+j*step[1]+k*across[1]) for k in range(2)) for j in range(len(region))]
        cells={v for col in region for v in col};assert not union&cells
        assert all(0<=r<current[0] and 0<=c<current[1] for r,c in cells)
        union|=cells
        z=inspect_strip(current,region,counts);local.append(z)
        K+=z['forest_components'];delta+=z['delta'];exports+=z['mixed_exports']
        for j,col in enumerate(region):
            labels=tuple(sorted(1 if v in T else 2 if v in P else 0 for v in col))
            kind='TP' if labels==(1,2) else 'BP' if labels==(0,2) else 'PP' if labels==(2,2) else 'other'
            columns[i,j]=kind
            for v in col:
                where[v]=(i,j)
                if v in P:
                    C+=kind=='TP';D+=kind=='BP'
    types=Counter();good_targets=[];safe_cross=[];bad=[]
    for edge in current[3]:
        entries=[v for v in edge if v in union and columns[where[v]]=='TP']
        if not entries:continue
        if len(entries)==2:
            types['TP_TP']+=1;bad.append(('TP_TP',edge));assert where[entries[0]][0]!=where[entries[1]][0]
            continue
        v=entries[0];w=mate[v]
        if w not in union:types['outside']+=1;bad.append(('outside',edge));continue
        kind=columns[where[w]]
        if kind=='BP':
            types['TP_BP']+=1;good_targets.append(where[w])
            if where[v][0]!=where[w][0]:
                types['safe_cross']+=1;safe_cross.append((v,w))
        else:
            assert kind=='PP';types['TP_PP']+=1;bad.append(('TP_PP',edge))
            assert where[v][0]!=where[w][0]
    assert len(set(good_targets))==len(good_targets)==types['TP_BP']
    unused=D-types['TP_BP'];assert unused>=0
    h,j,o=[types[k] for k in ('TP_TP','TP_PP','outside')]
    assert C==types['TP_BP']+2*h+j+o
    twice=sum(z['surplus_twice'] for z in local)
    assert twice==2*K+unused-2*h-j-o
    assert twice>=2*delta-2*h-j-o
    assert exports==types['safe_cross']+2*h+j+o
    assert sum(z['unused_bp'] for z in local)==unused+types['safe_cross']
    assert twice==sum(2*len(r) for r in regions)-2*len(T&union)-len(P&union)
    # Physical ledger only when the UNION consists of original whole tiles.
    tiles=tiles_of(union);tile_closed=vertices_of(tiles)==union
    ledger=None
    if tile_closed:
        deficit,raw=physical_ledger(current,tiles);assert twice==2*deficit-raw
        ledger=dict(endpoint_free_deficit=deficit,raw_receiver_charge_twice=raw)
    # Geometric refinement for parallel strips under single terminality.
    # A safe TP-to-BP transverse matching edge forces a P-square across
    # their band boundary. These are witnesses, never extra resources.
    square_witnesses={}
    if P and all(d>=3 for d in occupied_degrees(current).values()):
        for v,w in safe_cross:
            iv,jv=where[v];iw,jw=where[w]
            av,bv=regions[iv][jv];aw,bw=regions[iw][jw]
            across_v=(bv[0]-av[0],bv[1]-av[1]);across_w=(bw[0]-aw[0],bw[1]-aw[1])
            if abs(across_v[0]*across_w[0]+across_v[1]*across_w[1])!=1:continue
            d=(w[0]-v[0],w[1]-v[1]);side=(-d[1],d[0])
            assert (v[0]-d[0],v[1]-d[1]) in T
            assert (w[0]+d[0],w[1]+d[1]) not in T|P
            squares=[]
            for sign in (-1,1):
                q=frozenset((v,w,(v[0]+sign*side[0],v[1]+sign*side[1]),(w[0]+sign*side[0],w[1]+sign*side[1])))
                if q<=P:squares.append(q)
            assert squares
            square_witnesses[v,w]=min(squares,key=lambda q:sorted(q))
        multiplicity=Counter(tuple(sorted(q)) for q in square_witnesses.values())
        assert all(n<=2 for n in multiplicity.values())
        counts['parallel_safe_export_square_witnesses']+=len(square_witnesses)
    counts['joint_models']+=1
    counts['models_with_safe_cross_refund']+=bool(safe_cross)
    counts['safe_cross_matching_edges']+=len(safe_cross)
    counts['models_with_TP_TP_debit']+=bool(h)
    counts['models_with_TP_PP_debit']+=bool(j)
    counts['models_with_external_TP_debit']+=bool(o)
    return dict(surplus_twice=twice,boundary_budget=delta,forest_components=K,unused_BP=unused,
        TP_TP=h,TP_PP=j,outside=o,safe_cross=len(safe_cross),
        old_individual_export_debit=exports,new_debit_twice=2*h+j+o,
        safe_cross_edges=safe_cross,bad_edges=bad,union_tile_closed=tile_closed,physical_ledger=ledger,
        parallel_square_witnesses=[dict(edge=e,square=sorted(q)) for e,q in square_witnesses.items()])


def complete_fixed_strip(current,row0,height,first_column,length,blank_columns):
    """Exact column DP for maximizing T in a fixed P footprint.

    Uses only local selected-degree constraints, not the flux bound.
    Retains all old T and all outside occupancy. Returns an explicit optimum.
    """
    T=current[2];P=endpoints_of(current);outside=(T|P)-{(r,c) for r in range(row0,row0+height) for c in range(first_column,first_column+length)}
    pm=[];choices=[]
    for c in range(first_column,first_column+length):
        maskP=sum(1<<i for i in range(height) if (row0+i,c) in P);pm.append(maskP)
        required=sum(1<<i for i in range(height) if (row0+i,c) in T)
        choices.append([m for m in range(1<<height) if not m&maskP and m&required==required and (c not in blank_columns or m==0)])
    def valid(k,left,chosen,right):
        c=first_column+k
        occ=pm[k]|chosen
        for i in range(height):
            if not (chosen>>i&1):continue
            upper=bool(occ>>(i-1)&1) if i else (row0-1,c) in outside
            lower=bool(occ>>(i+1)&1) if i+1<height else (row0+height,c) in outside
            if upper+lower+bool(left>>i&1)+bool(right>>i&1)>1:return False
        return True
    left_out=sum(1<<i for i in range(height) if (row0+i,first_column-1) in outside)
    right_out=sum(1<<i for i in range(height) if (row0+i,first_column+length) in outside)
    @lru_cache(None)
    def best(k,left,chosen):
        if k+1==length:return (chosen.bit_count(),(chosen,)) if valid(k,left,chosen,right_out) else None
        result=None
        for nxt in choices[k+1]:
            if not valid(k,left,chosen,pm[k+1]|nxt):continue
            tail=best(k+1,pm[k]|chosen,nxt)
            if tail is None:continue
            z=chosen.bit_count()+tail[0],(chosen,)+tail[1]
            if result is None or z[0]>result[0]:result=z
        return result
    result=max((z for m in choices[0] if (z:=best(0,left_out,m)) is not None),default=None)
    assert result is not None
    selected=(T-{(r,c) for r in range(row0,row0+height) for c in range(first_column,first_column+length)})|{(row0+i,first_column+k) for k,m in enumerate(result[1]) for i in range(height) if m>>i&1}
    changed=(*current[:2],selected,current[3]);direct_check(*changed)
    return changed,result[0]


def safe_core(fill=True):
    T={(2,4),(4,3),(2,6),(3,7),(5,6),(6,5)}
    M=[((3,4),(4,4)),((3,5),(3,6)),((4,5),(5,5))]
    current=8,10,T,M
    if fill:current,_=complete_fixed_strip(current,2,4,0,10,{0,9})
    regions=[[( (r,c),(r+1,c)) for c in range(10)] for r in (2,4)]
    return current,regions


def frozen_check(current,counts):
    direct_check(*current);P=endpoints_of(current)
    assert min(occupied_degrees(current).values())>=3
    frozen,layers=frozen_certificate(current);assert frozen==P
    # Replay the actual rank witnesses independently of the constructor.
    mate={v:w for e in current[3] for v,w in (e,e[::-1])};seen=set()
    for layer in layers:
        for event in layer:
            v=event['endpoint'];ws=event['kept_neighbors'];assert len(ws)==len(set(ws))==2
            assert all(w in neighbors(v) and (w in current[2] or mate[w] in seen) for w in ws)
        seen|={e['endpoint'] for e in layer}
    assert seen==P
    counts['strict_freezing_events']+=len(P)
    return layers


def local_controls(counts):
    cur,regions=safe_core();z=inspect(cur,regions,counts);frozen_check(cur,counts)
    assert z['safe_cross']==1 and z['new_debit_twice']==0
    assert z['surplus_twice']==10 and z['boundary_budget']==4
    assert z['forest_components']==5 and z['unused_BP']==0
    # Same original endpoint component meets both strips, so the previous
    # per-strip complete-receiver closure hypothesis fails.
    components=endpoint_components(cur);assert len(components)==1
    assert all(set(components[0])&{v for col in r for v in col} for r in regions)
    assert all(not tiles_of(components[0])<=tiles_of({v for col in r for v in col}) for r in regions)
    # TP-TP: both mixed exports debit the SAME actual edge, one unit total.
    curTT=(4,3,{(0,1),(1,2),(2,0),(3,1)},[((1,1),(2,1))])
    regsTT=[[( (0,c),(1,c)) for c in range(3)],[( (2,c),(3,c)) for c in reversed(range(3))]]
    zz=inspect(curTT,regsTT,counts);frozen_check(curTT,counts)
    assert (zz['surplus_twice'],zz['boundary_budget'],zz['TP_TP'],zz['unused_BP'])==(2,2,1,0)
    assert zz['surplus_twice']<2*zz['boundary_budget']
    # TP-PP: a frozen four-endpoint vertical comb, two independent half-debits.
    curPP=(6,4,{(0,1),(1,2),(2,0),(3,2),(4,0),(5,1)},[((1,1),(2,1)),((3,1),(4,1))])
    regsPP=[[( (0,c),(1,c)) for c in range(3)],[( (2,c),(3,c)) for c in reversed(range(4))],[( (4,c),(5,c)) for c in reversed(range(3))]]
    zp=inspect(curPP,regsPP,counts);frozen_check(curPP,counts)
    assert (zp['surplus_twice'],zp['boundary_budget'],zp['TP_PP'],zp['unused_BP'])==(4,3,2,0)
    assert zp['surplus_twice']<2*zp['boundary_budget']
    half=inspect(curPP,regsPP[:2],counts)
    assert (half['surplus_twice'],half['boundary_budget'],half['TP_PP'])==(3,2,1)
    # The original single-strip fully frozen half-debit remains sharp.
    from check_occupied_strip_matching_flux import counterexample
    outside=counterexample(6,False)
    zo=inspect(outside,[[( (0,c),(1,c)) for c in range(6)]],counts)
    frozen_check(outside,counts)
    assert zo['outside']==1 and zo['surplus_twice']==1 and zo['boundary_budget']==1
    return dict(safe=(cur,regions,z),TP_TP=(curTT,regsTT,zz),TP_PP=(curPP,regsPP,zp),TP_PP_half=(curPP,regsPP[:2],half),outside=(outside,None,zo))


def save_fixture():
    cur,regions=safe_core();_,layers=frozen_certificate(cur)
    case=dict(scope='Fully frozen six-endpoint component split across two original horizontal bands; one actual TP-to-BP export refunded at its distinct BP column. Original board and matching; no rerooting or new resources.',
        shape=list(cur[:2]),selected=sorted(cur[2]),matching=cur[3],regions=regions,
        exact_regional_surplus=5,boundary_lower_budget=4,safe_cross_edge=((3,4),(4,4)),
        strict_freezing_layers=layers)
    Path('develop/fixtures/frozen_occupied_strip_export_refund.json').write_text(json.dumps(case,indent=2)+'\n')


def frozen_families(counts):
    case=json.loads(Path('develop/fixtures/frozen_occupied_strip_export_refund.json').read_text())
    base=(*case['shape'],{tuple(v) for v in case['selected']},[tuple(tuple(v) for v in e) for e in case['matching']])
    regs=[[tuple(tuple(v) for v in col) for col in region] for region in case['regions']]
    assert (base,regs)==safe_core()
    samples=[]
    for q in (1,2,3,4,8,16,32):
        move=lambda v,i:(v[0],v[1]+12*i)
        cur=(8,12*q-2,{move(v,i) for i in range(q) for v in base[2]},
             [tuple(move(v,i) for v in e) for i in range(q) for e in base[3]])
        regions=[[tuple(move(v,i) for v in col) for col in r] for i in range(q) for r in regs]
        z=inspect(cur,regions,counts);frozen_check(cur,counts)
        assert z['surplus_twice']==10*q and z['safe_cross']==q and z['boundary_budget']==4*q
        assert z['new_debit_twice']==0 and z['forest_components']==5*q and z['unused_BP']==0
        assert z['physical_ledger']==dict(endpoint_free_deficit=5*q,raw_receiver_charge_twice=0)
        assert len(cur[2])==13*q and len(cur[3])==3*q
        counts['all_q_frozen_refund_controls']+=1
        if q in (1,32):samples.append(dict(copies=q,shape=cur[:2],record=z))
        if q in (1,4):
            for symmetry in itertools.product((False,True),repeat=3):
                shape,T,M=transformed(*cur,*symmetry);f=image_map(*cur[:2],symmetry)
                regions2=[[tuple(f(v) for v in col) for col in r] for r in regions]
                im=inspect((*shape,T,M),regions2,counts);frozen_check((*shape,T,M),counts)
                assert all(im[k]==z[k] for k in ('surplus_twice','safe_cross','boundary_budget','new_debit_twice','forest_components','unused_BP'))
                counts['frozen_refund_symmetries']+=1
    # Five positive complete elbows per neutral split receiver; the exact
    # forest budget5 pays them, with the outside component ledger kept once.
    from check_elbow_sources import elbow
    from check_native_guard_compensation import charge
    root=elbow(6,4);assert charge(root)==1
    for q in (1,2,8):
        T=set();M=[];regions=[]
        for i in range(q):
            shift=112*i
            for j in range(5):
                f=lambda v:(v[0],v[1]+shift+20*j)
                T|={f(v) for v in root[2]};M.extend(tuple(f(v) for v in e) for e in root[3])
            f=lambda v:(v[0],v[1]+shift+100)
            T|={f(v) for v in base[2]};M.extend(tuple(f(v) for v in e) for e in base[3])
            regions.extend([[tuple(f(v) for v in col) for col in r] for r in regs])
        cur=12,112*q-2,T,M;z=inspect(cur,regions,counts);frozen_check(cur,counts)
        U={v for r in regions for col in r for v in col};inside=tiles_of(U)
        all_tiles=set(itertools.product(range(cur[0]//2),range(cur[1]//2)))
        outside_receivers=set();positive=negative=0;inside_count=0
        for comp in endpoint_components(cur):
            receiver=tiles_of(comp)
            if receiver&inside:
                assert receiver<=inside;inside_count+=1
            else:
                outside_receivers|=receiver
                rho2=2*len(T&vertices_of(receiver))+len(comp)-4*len(receiver)
                positive+=max(rho2,0);negative+=max(-rho2,0)
        D_out=sum(2-len(T&vertices_of({tile})) for tile in all_tiles-inside-outside_receivers)
        margin2=cur[0]*cur[1]-2*direct_check(*cur)
        assert inside_count==q and positive==10*q and negative==0
        assert margin2==z['surplus_twice']+2*D_out-positive+negative and margin2>=0
        counts['nonvacuous_five_positive_source_compensation_boards']+=1
    # Globally tile-closed, fully frozen sharp TP-TP debit: 2q copies of
    # the 4x3 module partition the 4x6q rectangle without any double use.
    for q in (1,2,4,16):
        T0={(0,1),(1,2),(2,0),(3,1)};M0=[((1,1),(2,1))]
        T={(r,c+3*i) for i in range(2*q) for r,c in T0}
        M=[tuple((r,c+3*i) for r,c in e) for i in range(2*q) for e in M0]
        regions=[]
        for i in range(2*q):
            regions.extend([[((0,c+3*i),(1,c+3*i)) for c in range(3)],
                            [((2,c+3*i),(3,c+3*i)) for c in reversed(range(3))]])
        cur=4,6*q,T,M;z=inspect(cur,regions,counts);frozen_check(cur,counts)
        assert z['TP_TP']==2*q and z['surplus_twice']==4*q and z['boundary_budget']==4*q
        assert z['union_tile_closed'] and z['surplus_twice']==2*z['boundary_budget']-2*z['TP_TP']
        assert cur[0]*cur[1]//2-direct_check(*cur)==2*q
        counts['all_q_sharp_TP_TP_debit_boards']+=1
    return samples


def exhaustive_two_strip_controls(counts):
    # All labels on the 8 non-entry cells of a 4x3 region, every internal
    # matching and every possible transverse completion into blank padding.
    cells={(r,c) for r in range(1,5) for c in range(3)}
    entry={(1,0),(2,0),(3,2),(4,2)};free=sorted(cells-entry)
    regions=[[((1,c),(2,c)) for c in range(3)],
             [((3,c),(4,c)) for c in reversed(range(3))]]
    def matchings(P):
        if not P:yield [];return
        v=min(P);left=P-{v}
        for w in sorted(set(neighbors(v))&left):
            for rest in matchings(left-{w}):yield [(v,w)]+rest
        if v[0] in (1,4):
            w=(0 if v[0]==1 else 5,v[1])
            for rest in matchings(left):yield [(v,w)]+rest
    for labels in itertools.product(range(3),repeat=len(free)):
        T={v for v,label in zip(free,labels) if label==1}
        P={v for v,label in zip(free,labels) if label==2}
        occ=T|P
        if {(1,2),(2,2)}<=occ or {(3,0),(4,0)}<=occ:continue
        if any(len(set(neighbors(v))&occ)>1 for v in T):continue
        for M in matchings(P):
            cur=6,3,T,M
            try:direct_check(*cur)
            except AssertionError:continue
            inspect(cur,regions,counts);counts['exhaustive_two_strip_matchings']+=1


def mixed_region_controls(counts):
    from check_frozen_mixed_gate_cycle import load_model
    cur=load_model()[0];P=endpoints_of(cur);occ=cur[2]|P
    candidates=[]
    for horizontal in (False,True):
        transverse=cur[0] if horizontal else cur[1]
        along=cur[1] if horizontal else cur[0]
        for r in range(transverse-1):
            for lo in range(along-1):
                for hi in range(lo+2,along+1):
                    region=[((r,c),(r+1,c)) if horizontal else ((c,r),(c,r+1)) for c in range(lo,hi)]
                    if not set(region[0])&occ and not set(region[-1])<=occ:candidates.append(region)
                    rev=region[::-1]
                    if not set(rev[0])&occ and not set(rev[-1])<=occ:candidates.append(rev)
    rng=random.Random(20261026173)
    for rep in range(80):
        pool=list(candidates);rng.shuffle(pool);used=set();regions=[]
        for region in pool:
            cells={v for col in region for v in col}
            if not cells&used:regions.append(region);used|=cells
            if len(regions)>=16:break
        inspect(cur,regions,counts);counts['mixed_direction_greedy_region_controls']+=1
    # Full original horizontal bands are an exactly tile-closed partition.
    regions=[[((r,c),(r+1,c)) for c in range(cur[1])] for r in range(0,cur[0],2)]
    z=inspect(cur,regions,counts);assert z['union_tile_closed']
    counts['complete_frozen_board_band_partition']=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();examples=local_controls(counts)
    families=frozen_families(counts);exhaustive_two_strip_controls(counts);mixed_region_controls(counts)
    report=dict(status='PASS',counts=dict(counts),families=families,
        local_controls={name:dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],record=z) for name,(cur,regs,z) in examples.items()},
        scope='Exact original-column matching-edge ledger across disjoint mixed-direction strips; safe TP-to-BP exports refund through different BP columns. Sharp TP-TP/TP-PP/exterior debit controls, fully frozen split receiver and all-q families. No universal5/6 improvement or routing-to-unused-interval claim.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts)),indent=2))


if __name__=='__main__':main()
