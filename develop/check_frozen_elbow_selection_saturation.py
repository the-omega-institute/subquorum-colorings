"""Selected-extension stability and exact 184/186 bounds; standard library.

General proofs: docs/FROZEN_ELBOW_SELECTION_SATURATION.md.
No optimizer or enumeration of full-board selections is used for the bounds.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_fully_frozen_elbow_withdrawal import configuration_one, stack
from check_canonical_band_coarsening import canonical_bands, forests
from check_crossing_matching_ports import rectangle, band_resources
from check_degree_changing_bent_completions import compile_model
from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_selection_maximum_singleton import candidates, feasible
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def neighbors(v):
    r,c=v
    return {(r-1,c),(r+1,c),(r,c-1),(r,c+1)}


def blocker(cur, extra):
    """A physical degree-two certificate, not a solver infeasibility claim."""
    T=cur[2]|set(extra);P={v for edge in cur[3] for v in edge}
    assert not T&P
    for v in sorted(T):
        witnesses=sorted(neighbors(v)&(P|T))
        if len(witnesses)>=2:
            return dict(selected=v,occupied_neighbors=witnesses[:2])
    raise AssertionError('No forbidden degree-two selection')


def tile_cover(cur,hull):
    """Analytic square cap2, improved to cap1 by pairwise degree witnesses.

    Any three vertices of a 2x2 square give a selected vertex two selected
    neighbors. Thus cap2 is universal. No feasible-subset search is needed.
    """
    rows=[];certs=[]
    for r in range(0,cur[0],2):
        row=[]
        for c in range(0,cur[1],2):
            xs=sorted(hull&{(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)})
            if not xs:cap=0
            elif all(not feasible(cur,pair) for pair in itertools.combinations(xs,2)):
                cap=1
                certs.extend(dict(tile=[r,c],pair=pair,**blocker(cur,pair))
                             for pair in itertools.combinations(xs,2))
            else:cap=2
            row.append(cap)
        rows.append(row)
    return rows,certs


def regions(cur,bits,E,F):
    bits=dict(bits)
    for i in E:bits[16*i+10,16]=False
    for i in F:bits[16*i+2,12]=bits[16*i+4,12]=True
    return canonical_bands(*cur[:2],[rectangle(r,r+2,c,c+2,v) for (r,c),v in bits.items()])


def protection(cur,bits,hull,E,F):
    """Complete BP and body-boundary gap certificates for the general proof."""
    regs=regions(cur,bits,E,F);d,cl,N=compile_model(cur,regs)
    own,A,B,X=owner_data(*d[:2]);q=cur[0]//16
    core=A|{own[16*i+5,15] for i in range(q)}
    body_owner={v:o for o,x in enumerate(cl) for v in x['body']}
    P={v for edge in cur[3] for v in edge};bp=[]
    for v,k in sorted(d[0].items()):
        if k!='BP':continue
        x=N[v];witnesses=sorted(neighbors(x)&(P|cur[2]))
        assert x not in hull and len(witnesses)>=2
        bp.append(dict(tip=v,blank_partner=x,occupied_neighbors=witnesses[:2]))
    bands=[band for reg in regs for band in reg['bands']]
    _,gaps,_=band_resources(P,cur[2],bands);protected=[]
    for b,first,end,units in gaps:
        users={body_owner[v] for k in (first-1,end) if 0<=k<len(bands[b])
               for v in bands[b][k] if v in body_owner}
        if not users&core:continue
        cells={v for pair in bands[b][first:end] for v in pair}
        assert not cells&hull
        # Every blank excluded site has an explicit baseline obstruction.
        certs=[dict(site=v,**blocker(cur,{v})) for v in sorted(cells-cur[2])]
        protected.append(dict(cells=sorted(cells),owners=sorted(users),capacity=len(units),blockers=certs))
    tips=[]
    for a in sorted(A):
        for v in d[1][a]:
            assert len(neighbors(v)&(P|cur[2]))==3
            for x in sorted(neighbors(v)-(P|cur[2])):
                ws=sorted(neighbors(x)&(P|cur[2]));assert len(ws)>=2
                tips.append(dict(alpha_tip=v,blank_neighbor=x,occupied_neighbors=ws[:2]))
    return dict(empty_actions=sorted(E),elbow_actions=sorted(F),BP=bp,gaps=protected,
                degree_three_tip_protection=tips)


def profile(base,cur,bits,ranks,E,F,counts,independent=False):
    direct_check(*cur);assert base[2]<=cur[2] and base[3]==cur[3]
    q=cur[0]//16
    counts['strict_rank_events']+=len(check_rank_certificate(cur,ranks))
    assert frozen_certificate(cur)[0]=={v for edge in cur[3] for v in edge}
    regs=regions(cur,bits,E,F)
    old,oc,_=compile_model(base,regs);d,cl,_=compile_model(cur,regs)
    assert d[:2]==old[:2] and set(d[2])==set(old[2])
    assert [x['body'] for x in cl]==[x['body'] for x in oc]
    own,A,B,X=owner_data(*d[:2]);assert (len(A),len(B),len(X))==(2*q,2*q,5*q)
    P={v for edge in cur[3] for v in edge}
    assert all(len(neighbors(v)&(P|cur[2]))==3 for a in A for v in d[1][a])
    of,cf=forests(base,regs),forests(cur,regs)
    core=A|{own[16*i+5,15] for i in range(q)}
    for o in core:
        assert {of[j][1] for j in old[3][o]}=={cf[j][1] for j in d[3][o]}
    assert len(d[4])==cur[0]*cur[1]//2-len(cur[2])-len(cur[3])
    answer=fork_flow(*d);expected=(q+len(E-F),q-len(F))
    assert (answer['value'],answer['cost'])==expected
    if independent:
        alt=optimize(*d)
        assert (alt['value'],alt['cost'])==expected
        counts['independent_primitive_optima']+=1
    counts['extension_action_profiles']+=1
    return dict(selected=len(cur[2]),raw=len(d[4]),value=answer['value'],cost=answer['cost'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    base,bits,ranks=configuration_one();R,C,T,M=base
    fixture=json.loads((Path(__file__).parent/'fixtures/frozen_elbow_selection_saturation.json').read_text())
    assert fixture['shape']==[R,C] and [tuple(map(tuple,e)) for e in fixture['matching']]==M
    hull=candidates(base);assert len(hull)==181
    extcaps,paircerts=tile_cover(base,hull);assert sum(map(sum,extcaps))==101
    ext=R,C,set(map(tuple,fixture['extension_maximum_selected'])),M
    direct_check(*ext);assert T<=ext[2] and len(ext[2])==184 and not candidates(ext)
    # Every cover inequality is attained, certifying the exact extension maximum.
    for r in range(0,R,2):
        for c in range(0,C,2):
            cells={(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}
            assert len((ext[2]-T)&cells)==extcaps[r//2][c//2]
    empty=R,C,set(),M;allhull=candidates(empty)
    globalcaps,globalpairs=tile_cover(empty,allhull)
    assert globalcaps==fixture['unrestricted_tile_caps'] and sum(map(sum,globalcaps))==189
    patches=[];covered=set()
    for r,c in fixture['patch_origins']:
        cells={(r+i,c+j) for i in range(4) for j in range(2)}
        assert not cells&covered;covered|=cells
        xs=allhull&cells
        # The six candidates are partitioned into three forbidden pairs.
        ends=[sorted(xs&{(r+i,c),(r+i,c+1)}) for i in (0,3)]
        middle=sorted(xs-{v for pair in ends for v in pair});pairs=ends+[middle]
        assert len(xs)==6 and all(len(pair)==2 for pair in pairs)
        assert set().union(*map(set,pairs))==xs
        assert all(not feasible(empty,pair) for pair in pairs)
        P={v for edge in M for v in edge}
        assert all(any(neighbors(v)&P for v in pair) for pair in pairs)
        assert globalcaps[r//2][c//2]+globalcaps[r//2+1][c//2]==4
        patches.append(dict(origin=[r,c],capacity=3,candidates=sorted(xs),
                            forbidden_pairs=[dict(pair=pair,**blocker(empty,pair)) for pair in pairs]))
    glob=R,C,set(map(tuple,fixture['unrestricted_maximum_selected'])),M
    direct_check(*glob);assert len(glob[2])==186==189-len(patches)
    counts=Counter();certificates=[];maxprofiles=[]
    for e,f in itertools.product((False,True),repeat=2):
        E={0} if e else set();F={0} if f else set()
        certificates.append(protection(base,bits,hull,E,F))
        maxprofiles.append(dict(empty=e,elbow=f,**profile(base,ext,bits,ranks,E,F,counts,True)))
    rng=random.Random(20261026184)
    # Check every single addition, then independently generated maximal completions.
    for v in sorted(hull):
        cur=R,C,T|{v},M
        for e,f in itertools.product((False,True),repeat=2):
            profile(base,cur,bits,ranks,{0} if e else set(),{0} if f else set(),counts)
        counts['single_addition_boards']+=1
    for q in (1,2,3,7):
        b,bb,_,rr=stack(q);H=candidates(b)
        for e,f in ((set(),set()),(set(range(q)),set()),(set(range(q)),set(range(q))),
                    (set(range(0,q,2)),set(range(1,q,2)))):
            protection(b,bb,H,e,f)
            counts['stack_protection_profiles']+=1
        for trial in range(4):
            order=sorted(H);rng.shuffle(order);cur=b
            for v in order:
                if feasible(cur,{v}):cur=(*cur[:2],cur[2]|{v},cur[3])
            assert not candidates(cur)
            counts['inclusion_maximal_boards']+=1
            for e,f in ((set(),set()),(set(range(q)),set()),(set(range(q)),set(range(q))),
                        (set(range(0,q,2)),set(range(1,q,2)))):
                profile(b,cur,bb,rr,e,f,counts,q<=2)
    # Scope control: the unrestricted attainer is not completely frozen.
    frozen,_=frozen_certificate(glob);assert len(frozen)==45
    report=dict(status='PASS',counts=dict(counts),candidate_hull_size=len(hull),
        extension_upper_bound=dict(base_selected=83,additional_cap=101,maximum=184,
            tile_caps=extcaps,cap1_pair_obstructions=paircerts),
        unrestricted_upper_bound=dict(tile_sum=189,disjoint_patch_savings=3,maximum=186,
            tile_caps=globalcaps,cap1_pair_obstructions=globalpairs,patches=patches),
        all_extension_protection=certificates,maximum_extension_profiles=maxprofiles,
        unrestricted_attainer_control=dict(selected=186,frozen_endpoints=45,required_for_full_freezing=70),
        theorem='Every feasible extension retaining baseline selections preserves all owner types/links and the complete source-reachable supports in every E/F state. Exact arbitrary-q value q+|E\\F| and cost q-|F| survive all such extensions. One-copy retained maximum184, raw/slack5; unrestricted fixed-P maximum186.',
        limits=['General proofs establish arbitrary extensions; samples are regression checks only.',
            'No assertion that the unrestricted maximum has a fully frozen elbow obstruction.',
            'No additive184q/186q formula: saturated boundary witnesses cannot simply be stacked.',
            'No optimized-N or numerical target counterexample; universal5/6 remains open.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts),retained_maximum=184,unrestricted_maximum=186),indent=2))


if __name__=='__main__':main()
