"""Physical controls for the written degree-defect/direction-interface theorem.

Standard library only. Counts original N-edges, not duplicate owner credits.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors, occupied_degrees
from check_crossing_matching_ports import rectangle, strand_parts, compile_partition
from check_compensation_flow_normal_form import owner_data
from check_four_outward_slab import slab
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_owned_donors import capacity_cross
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_normal_form import brute
from rotor_networks import chain

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def tile(v):
    return v[0]//2*2, v[1]//2*2


def cells(q):
    r,c=q
    return {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}


def fixture():
    j=json.loads((Path(__file__).parent/'fixtures/degree_three_four_outward_live_mixed.json').read_text())
    return (tuple(j['shape'])+ (set(map(tuple,j['selected'])),
            [tuple(map(tuple,e)) for e in j['matching']])),j


def inspect(cur, directions, totals):
    R,C,T,M=cur;P={v for e in M for v in e}
    mate={v:w for e in M for v,w in (e,e[::-1])}
    deg={v:sum(w in T|P for w in neighbors(v)) for v in P}
    assert min(deg.values())>=3
    regions=[rectangle(r,r+2,c,c+2,directions[r,c]) for r,c in sorted(directions)]
    parts,_=strand_parts(P,T,M,[b for x in regions for b in x['bands']])
    owner={v:k for k,x in enumerate(parts) for v in x['body']}
    J={v for v in P if deg[v]==4}
    seams=[e for e in M if directions[tile(e[0])]!=directions[tile(e[1])]]
    records=[];root_defects=[];mate_defects=[];seam_corners=[]
    for q in sorted(directions):
        Q=cells(q)
        if not Q<=P or any(mate[v] in Q for v in Q):continue
        vertical=directions[q]  # True means horizontal N, vertical bands.
        r,c=q
        wires=([((r,c),(r,c+1)),((r+1,c),(r+1,c+1))] if vertical else
               [((r,c),(r+1,c)),((r,c+1),(r+1,c+1))])
        alpha=[e for e in wires if parts[owner[e[0]]]['kind']=='TT']
        assert all(owner[u]==owner[v] for u,v in wires)
        a=Q&J;b={mate[v] for v in Q}&J
        perpendicular=lambda v: (v[0]==mate[v][0]) != vertical
        cross={v for v in Q if perpendicular(v) and directions[tile(mate[v])]!=vertical}
        all_faces=[((r,c),(r,c+1)),((r+1,c),(r+1,c+1)),
                   ((r,c),(r+1,c)),((r,c+1),(r+1,c+1))]
        double=[]
        for u,v in all_faces:
            # Equal outward displacements specify the same double-exit face.
            if (mate[u][0]-u[0],mate[u][1]-u[1]) != (mate[v][0]-v[0],mate[v][1]-v[1]):continue
            cycle={u,v,mate[u],mate[v]}
            assert len(cycle)==4
            for color in (0,1):
                assert any(x in J for x in cycle if sum(x)%2==color)
            double.append(cycle)
        assert sum(map(len,double))==len(set().union(set(),*double))
        D=len(double)
        v=sum(not any(perpendicular(x) for x in e) for e in wires)
        h=sum(any(perpendicular(x) for x in e) for e in alpha)
        i=len(alpha)
        # Check the actual injection in the two-column written proof.
        # Tags distinguish root degree defects from counted seam corners.
        charges=[]
        for e in alpha:
            horizontal=[x for x in e if perpendicular(x)]
            if not horizontal:continue
            if any(x in cross for x in horizontal):
                charges.append(('seam',min(set(horizontal)&cross)))
            elif len(horizontal)==1:
                x=horizontal[0];z=next(w for w in e if w!=x)
                dx=mate[x][0]-x[0];dy=mate[x][1]-x[1]
                companion=z[0]+dx,z[1]+dy
                assert companion in T|P and z in a
                charges.append(('defect',z))
            else:
                raise AssertionError('An alpha cannot be the coherent outside-pair cycle.')
        assert len(charges)==len(set(charges))==h
        assert v<=D and 2*D<=len(a)+len(b)
        assert h<=len(a)+len(cross) and i<=v+h
        assert 2*i<=3*len(a)+len(b)+2*len(cross)
        root_defects+=list(a);mate_defects+=list(b);seam_corners+=list(cross)
        records.append(dict(tile=q,i=i,a=len(a),b=len(b),c=len(cross),D=D,v=v,
                            owners=[parts[owner[e[0]]]['kind'] for e in wires]))
    assert len(root_defects)==len(set(root_defects))
    assert len(mate_defects)==len(set(mate_defects))
    charged_edges=[frozenset((v,mate[v])) for v in seam_corners]
    assert len(charged_edges)==len(set(charged_edges))<=len(seams)
    I=sum(x['i'] for x in records);CF=len(seam_corners)
    F={tuple(x['tile']) for x in records}
    weighted=sum(3*(tile(v) in F)+(tile(mate[v]) in F) for v in J)
    assert weighted==3*len(root_defects)+len(mate_defects)<=4*len(J)
    assert 2*I<=weighted+2*CF and I<=2*len(J)+len(seams)
    totals['partitions']+=1;totals['four_outward_tiles']+=len(records)
    totals['alpha_wire_incidences']+=I;totals['degree_four_endpoint_occurrences']+=len(J)
    totals['direction_changing_matching_edges']+=len(seams)
    return dict(I=I,J4=len(J),E_dir=len(seams),C_F=CF,weighted_defects=weighted,tiles=records)


def local_controls(totals):
    # True = perpendicular/horizontal actual mate at that corner; N vertical.
    for nw,ne,sw,se in itertools.product((False,True),repeat=4):
        v=int(not nw and not sw)+int(not ne and not se)
        D=int(not nw and not ne)+int(not sw and not se)+int(nw and sw)+int(ne and se)
        assert v<=D
        totals['local_direction_cases']+=1


def boundary(cur,j,totals):
    R,C,T,M=cur;P={v for e in M for v in e}
    dirs={q:False for q in itertools.product(range(0,R,2),range(0,C,2))}
    out={}
    for flip in (False,True):
        directions=dict(dirs)
        if flip:directions[tuple(j['flipped_tile'])]=True
        result=inspect(cur,directions,totals)
        root=next(x for x in result['tiles'] if x['tile']==tuple(j['root_tile']))
        assert result['J4']==0 and root['i']==int(flip) and root['c']==int(flip)
        assert result['E_dir']==2*int(flip)
        regions=[rectangle(r,r+2,c,c+2,directions[r,c]) for r,c in sorted(directions)]
        rec,data=compile_partition(cur,regions)
        independent,count=brute(*data)
        assert independent==(rec['value'],rec['cost'])==(1,0) and rec['deficit']==0
        assert (rec['alpha'],rec['beta'])==(1,3)
        totals['independent_terminal_matchings']+=count
        bands=[b for reg in regions for b in reg['bands']]
        parts,_=strand_parts(P,T,M,bands)
        body={v:x for x in parts for v in x['body']}
        if flip:
            assert body[4,4]['kind']=='TT'
            assert body[4,4]['ends']==[('T',(3,4)),('T',(10,2))]
        else:
            assert body[4,4]['kind']=='BT'
            owners,A,_,_=owner_data(*data[:2]);alpha=owners[5,2];gate=owners[5,3]
            assert alpha in A and ((5,2),(5,3)) in data[2]
            assert body[4,4] is body[5,3]
            units=data[3][gate]-set().union(*(data[3][a] for a in A))
            assert len(units)==1
            unit=next(iter(units));b,first,last=unit
            physical=sorted(v for pair in bands[b][first:last+1] for v in pair)
            assert physical==[(2,5),(3,5)] and not set(physical)&(T|P)
            support={o:s&units for o,s in data[3].items()}
            before,bcount=brute(*data[:3],support,units)
            free={v for o,pair in enumerate(data[1]) if o!=gate for v in pair}
            pruned=({v:k for v,k in data[0].items() if v in free},
                    [pair for o,pair in enumerate(data[1]) if o!=gate],
                    [e for e in data[2] if set(e)<=free],
                    {n:support[o] for n,o in enumerate(o for o in range(len(data[1])) if o!=gate)},units)
            after,acount=brute(*pruned)
            totals['independent_terminal_matchings']+=bcount+acount
            assert before==(1,1) and after==(0,0)
            # Repeat on a single uncut horizontal-band rectangle: the same
            # physical original unit exists before any tile-region splitting.
            whole,wd=compile_partition(cur,[rectangle(0,R,0,C)])
            assert (whole['alpha'],whole['beta'],whole['value'],whole['cost'])==(1,3,1,0)
            whole_result,wcount=brute(*wd)
            assert whole_result==(1,0)
            totals['independent_terminal_matchings']+=wcount
            wo,wA,_,_=owner_data(*wd[:2]);wg=wo[5,3];unit_whole=(1,5,5)
            assert unit_whole in wd[3][wg] and all(unit_whole not in wd[3][a] for a in wA)
            available={unit_whole};ws={o:s&available for o,s in wd[3].items()}
            wp,bc=brute(*wd[:3],ws,available)
            wf={v for o,pair in enumerate(wd[1]) if o!=wg for v in pair}
            wa,ac=brute({v:k for v,k in wd[0].items() if v in wf},
                [pair for o,pair in enumerate(wd[1]) if o!=wg],
                [e for e in wd[2] if set(e)<=wf],
                {n:ws[o] for n,o in enumerate(o for o in range(len(wd[1])) if o!=wg)},available)
            assert wp==(1,1) and wa==(0,0)
            totals['independent_terminal_matchings']+=bc+ac
            out['live_mixed']=dict(link=((5,2),(5,3)),original_resource_cells=physical,
                singleton_pool_before=before,singleton_pool_after_pruning=after,
                full_pool_before=(rec['value'],rec['cost']),
                whole_uncut_H_resource=unit_whole,whole_uncut_H_singleton_before=wp,
                whole_uncut_H_singleton_after_pruning=wa,
                scope='Only singleton-available-pool pruning fails; no full-pool loss claimed.')
        out['mixed' if flip else 'uniform']=result
    return out


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();local_controls(totals)
    cur,j=fixture();direct_check(*cur)
    assert len(cur[2])==26 and len(cur[3])==33 and set(occupied_degrees(cur).values())=={3}
    totals['independent_rank_events']+=len(check_rank_certificate(cur,
        [[tuple(v) for v in wave] for wave in j['frozen_schedule']]))
    assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
    witness=boundary(cur,j,totals)
    rng=random.Random(20261026)
    controls=[('witness',cur)]+[('slab'+str(h),slab(h)) for h in (1,2,4,8,16)]+[
        ('cross'+str(q),capacity_cross(q)[0]) for q in (1,2,4)]+[
        ('chain'+str(q),chain(q)[0]) for q in (1,2,4)]
    examples=[]
    for name,current in controls:
        direct_check(*current);P={v for e in current[3] for v in e}
        assert frozen_certificate(current)[0]==P
        totals['physical_models']+=1
        R,C,_,_=current;tiles=list(itertools.product(range(0,R,2),range(0,C,2)))
        masks=[{q:False for q in tiles},{q:True for q in tiles},
               {q:(sum(q)//2)%2==0 for q in tiles}]
        masks += [{q:bool(rng.getrandbits(1)) for q in tiles} for _ in range(32)]
        masks += [{q:q==single for q in tiles} for single in tiles if cells(single)<=P]
        for mask in masks:examples.append(dict(model=name,**inspect(current,mask,totals)))
    # Isometries verify both absolute directions and every physical face.
    for symmetry in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,*symmetry);image=(*shape,T,M)
        assert frozen_certificate(image)[0]=={v for e in M for v in e}
        totals['physical_models']+=1
        for direction in (False,True):
            inspect(image,{q:direction for q in itertools.product(range(0,shape[0],2),range(0,shape[1],2))},totals)
    summaries=[]
    for name,_ in controls:
        rows=[x for x in examples if x['model']==name]
        summaries.append(dict(model=name,partitions=len(rows),
            four_outward_tile_occurrences=sum(len(x['tiles']) for x in rows),
            alpha_wire_incidences=sum(x['I'] for x in rows),
            maximum_J4=max(x['J4'] for x in rows),maximum_E_dir=max(x['E_dir'] for x in rows),
            minimum_local_bound_slack=min((3*t['a']+t['b']+2*t['c']-2*t['i']
                for x in rows for t in x['tiles']),default=None),
            minimum_global_bound_slack=min(2*x['J4']+x['E_dir']-x['I'] for x in rows),
            uniform_vertical_N=rows[0],uniform_horizontal_N=rows[1]))
    report=dict(status='PASS',totals=dict(totals),witness=witness,controls=summaries,
        proved='Written: 2i_Q<=3a_Q+b_Q+2c_Q; exact non-reused endpoint/seam sum; I_F<=2J4+E_dir for any F. Exact degree three/uniform implies no alpha wire at four-outward tiles.',
        limitations='Localization, not donor supply or universal5/6. Mixed/beta owners not excluded. Singleton-pool pruning counterexample is not full-pool failure; witness full pool pays its one alpha at cost zero.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',**totals)))


if __name__=='__main__':main()
