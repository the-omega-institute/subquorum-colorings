"""Genuine frozen-grid coordination, including a fixed-P maximum local trap.

All-n geometric proofs are in docs/FROZEN_COORDINATED_PIVOTS.md.
Finite enumeration checks construction adapters and exact optima only.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_canonical_band_coarsening import forests, tile_refinement
from check_compensation_flow_normal_form import owner_data
from check_degree_changing_bent_completions import compile_model
from check_fixed_P_maximum_frozen_elbow import fixture, maximum_cover
from check_fully_frozen_elbow_withdrawal import configuration_one
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_P_free_pivot_interface import regions, gap_arms
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def tile_cells(tile):
    r,c=tile
    return {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}


def inventory(cur,bits,totals):
    regs=regions(cur,bits)
    data,closed,_=compile_model(cur,regs)
    fs=forests(cur,regs)
    supports={o:{fs[j][1] for j in W} for o,W in data[3].items()}
    f=fork_flow(*data);independent=optimize(*data)
    assert (f['value'],f['cost'])==(independent['value'],independent['cost'])
    totals['independent_primitive_optima']+=1
    return data,closed,{fs[j][1] for j in data[4]},supports,f


def check_kernel(cur,data,closed,supports,totals):
    own,A,B,X=owner_data(*data[:2]);a,b,z=own[3,12],own[5,17],own[5,15]
    assert A=={a,b} and (len(A),len(B),len(X))==(2,2,5)
    assert set(closed[a]['body'])=={(r,c) for r in range(3,11) for c in (10,11)}|{(3,12),(10,12)}
    assert set(data[1][a])=={(3,12),(10,12)}
    assert set(data[1][b])=={(5,17),(12,17)}
    external={(p,q) for p,q in data[2] if own[p]!=own[q]}
    assert {(p,q) for p,q in external if own[p] in {a,b,z}}=={((5,17),(5,16))}
    assert not supports[b] and supports[z]=={frozenset({(4,13),(5,13)})}
    O={v for e in cur[3] for v in e}|cur[2]
    assert all(len({(r+1,c),(r-1,c),(r,c+1),(r,c-1)}&O)==3 for o in A for r,c in data[1][o])
    totals['complete_source_kernel_checks']+=1
    return a,b,z


def family(n):
    assert isinstance(n,int) and n>=1
    q=max(n,6)
    old,oldbits,ranks=configuration_one()
    R,_,T,M=old
    C=18+2*q
    T=T|{(2 if c%2 else 3,c) for c in range(28,16+2*q)}
    cur=(R,C,T,M)
    bits={(r,c):oldbits.get((r,c),False) for r in range(0,R,2) for c in range(0,C,2)}
    gates=[(2,16+2*i) for i in range(n)]
    for tile in gates:bits[tile]=True
    return cur,bits,ranks,gates


def check_family(n,totals):
    cur,bits,ranks,gates=family(n);q=max(n,6);P={v for e in cur[3] for v in e}
    direct_check(*cur)
    assert len(cur[2])==71+2*q and len(cur[3])==35
    assert len(check_rank_certificate(cur,ranks))==70 and frozen_certificate(cur)[0]==P
    totals['family_strict_freezing_events']+=70
    for r,c in gates:
        tile=tile_cells((r,c))
        assert not tile&P and cur[2]&tile=={(r,c+1),(r+1,c)}
    first=inventory(cur,bits,totals)
    a,b,z=check_kernel(cur,first[0],first[1],first[3],totals)
    assert not first[3][a] and (first[4]['value'],first[4]['cost'])==(1,1)
    target={frozenset({(2,j),(3,j)}) for j in (16+2*q,17+2*q)}
    assert target<=first[2]
    assert all(not any(cells in W for W in first[3].values()) for cells in target)
    if n<=8:
        chosen=[{i for i in range(n) if mask>>i&1} for mask in range(1<<n)]
    else:
        allgates=set(range(n))
        chosen=[set(),allgates,set(range(0,n,2)),set(range(1,n,2))]
        chosen += [allgates-{i} for i in range(n)]
        chosen += [{i} for i in range(n)]
    states=[]
    for selected in chosen:
        changed=dict(bits)
        for i in selected:changed[gates[i]]=False
        data,closed,cells,supports,f=inventory(cur,changed,totals)
        assert data[:2]==first[0][:2] and set(data[2])==set(first[0][2])
        assert [(x['body'],x['ends']) for x in closed]==[(x['body'],x['ends']) for x in first[1]]
        assert cells==first[2] and len(cells)==38+14*q
        assert all(supports[o]==first[3][o] for o in supports if o!=a)
        full=len(selected)==n
        assert supports[a]==(target if full else set())
        assert (f['value'],f['cost'])==(1+int(full),1)
        assert all({o for o,W in supports.items() if cells in W}==({a} if full else set()) for cells in target)
        states.append(dict(selected=sorted(selected),value=f['value'],links=f['cost']))
        totals['family_joint_states']+=1
    # The long-gate lower bound concerns the declared corridor operations.
    # A separate lower corridor still permits a one-pivot global repair.
    alternate=dict(bits);assert alternate[10,16];alternate[10,16]=False
    alt=inventory(cur,alternate,totals)
    assert (alt[4]['value'],alt[4]['cost'])==(2,1)
    totals['unrestricted_alternate_single_repair_controls']+=1
    totals['family_boards']+=1
    if n<=8:totals['exhaustive_family_boards']+=1
    return dict(gates=n,q=q,shape=list(cur[:2]),selected=len(cur[2]),matching=35,frozen=70,
                raw=38+14*q,gate_tiles=gates,target_cells=[sorted(cells) for cells in sorted(target,key=lambda x:sorted(x))],
                exhaustive=n<=8,states=states,alternate_single_repair_outside_declared_gates=[10,16])


def maximum_trap(totals):
    cur,bits,ranks,units=fixture();bits[10,14]=True
    cover=maximum_cover(cur);P={v for e in cur[3] for v in e}
    assert len(check_rank_certificate(cur,ranks))==70 and frozen_certificate(cur)[0]==P
    direct_check(*cur)
    first=inventory(cur,bits,totals)
    a,b,z=check_kernel(cur,first[0],first[1],first[3],totals)
    assert not first[3][a] and (first[4]['value'],first[4]['cost'])==(1,1)
    free=[tile for tile in sorted(bits) if not tile_cells(tile)&P]
    assert len(free)==81
    candidates=[];singles=[]
    for tile in free:
        changed=dict(bits);changed[tile]=not changed[tile]
        regs=regions(cur,changed)
        data,closed,cells,supports,f=inventory(cur,changed,totals)
        assert data[:2]==first[0][:2] and set(data[2])==set(first[0][2])
        assert [x['body'] for x in closed]==[x['body'] for x in first[1]]
        assert not supports[a] and f['value']<=1
        left,right,L,R=gap_arms(cur,regs,tile,changed[tile],closed)
        if a in (L,R):
            ff=forests(cur,tile_refinement(*cur[:2],regs))
            fine=[cc for cap,cc in ff.values() if cap]
            counts=[sum(cc<=part for cc in fine) for part in (left,tile_cells(tile),right)]
            assert counts==[0,0,0]
            candidates.append(dict(tile=tile,new_vertical=changed[tile],gap_positive_counts=counts))
        singles.append(dict(tile=tile,value=f['value'],links=f['cost']))
        totals['maximum_all_P_free_single_pivots']+=1
    assert {tuple(x['tile']) for x in candidates}=={(0,10),(10,14),(12,10)}
    gates=[(10,14),(10,16)];states=[]
    for mask in range(4):
        changed=dict(bits)
        for i,tile in enumerate(gates):changed[tile]=not bool(mask>>i&1)
        data,closed,cells,supports,f=inventory(cur,changed,totals)
        assert data[:2]==first[0][:2] and set(data[2])==set(first[0][2])
        assert [x['body'] for x in closed]==[x['body'] for x in first[1]]
        assert len(cells)==3 and supports[a]==({units['K']} if mask==3 else set())
        assert all(supports[o]==first[3][o] for o in supports if o!=a)
        assert (f['value'],f['cost'])==(1+int(mask==3),1)
        states.append(dict(selected=[i for i in range(2) if mask>>i&1],value=f['value'],links=f['cost']))
    totals['maximum_gate_joint_states']+=4
    # The local-trap statement is invariant under all board symmetries.
    R,C=cur[:2]
    for tr,fr,fc in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,tr,fr,fc);image=(*shape,T,M)
        def point(v):
            r,c=v
            if fr:r=R-1-r
            if fc:c=C-1-c
            return (c,r) if tr else (r,c)
        def tile_image(tile):
            cc=list(map(point,tile_cells(tile)))
            return min(r for r,c in cc),min(c for r,c in cc)
        bb={tile_image(tile):v!=tr for tile,v in bits.items()}
        check_rank_certificate(image,[[point(v) for v in layer] for layer in ranks])
        for tile in free:
            changed=dict(bb);tt=tile_image(tile);changed[tt]=not changed[tt]
            d,_,_=compile_model(image,regions(image,changed))
            assert fork_flow(*d)['value']<=1
            totals['dihedral_maximum_single_pivots']+=1
        for tile in gates:bb[tile_image(tile)]=tr
        d,_,_=compile_model(image,regions(image,bb));assert fork_flow(*d)['value']==2
        totals['dihedral_maximum_joint_gains']+=1
    return dict(shape=list(cur[:2]),selected=186,matching=35,frozen=70,raw=3,
                fixed_P_upper_bound=cover['upper_bound'],all_P_free_single_pivots=singles,
                only_possible_new_a_boundary_gaps=candidates,gate_tiles=gates,joint_states=states)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter()
    maximum=maximum_trap(totals)
    families=[check_family(n,totals) for n in (*range(1,9),16,32,64)]
    result=dict(status='PASS',scope='Checks of independently proved all-n frozen-grid coordination and an explicit fixed-P maximum local trap. No universal bound improvement or unrestricted n-pivot lower bound.',
                counts=dict(totals),fixed_P_maximum_trap=maximum,arbitrary_gate_family=families)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(totals,sort_keys=True))


if __name__=='__main__':main()
