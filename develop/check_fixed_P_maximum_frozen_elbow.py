"""A true fixed-P maximum retaining complete freezing and elbow rank loss.

No solver dependency. Upper bound: disjoint geometric cover. Lower bound:
explicit selected vertices. General discussion: FIXED_P_MAXIMUM_FROZEN_ELBOW.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_frozen_elbow_selection_saturation import (
    neighbors, tile_cover, regions, candidates, feasible, blocker,
    compile_model, owner_data, forests, fork_flow, optimize,
    direct_check, check_rank_certificate, frozen_certificate,
)
from check_residual_corridors import transformed
from check_canonical_band_coarsening import canonical_bands
from check_crossing_matching_ports import rectangle
from check_local_elbow_resource_transfer import adapter, omit

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def fixture():
    raw=json.loads((Path(__file__).parent/'fixtures/fixed_P_maximum_fully_frozen_elbow.json').read_text())
    cur=(*raw['shape'],set(map(tuple,raw['selected'])),[tuple(map(tuple,e)) for e in raw['matching']])
    bits={(r,c):bool(v) for r,c,v in raw['tile_directions']}
    ranks=[[tuple(v) for v in layer] for layer in raw['strict_freezing_layers']]
    units={key:frozenset(map(tuple,cells)) for key,cells in raw['full_pool_units'].items()}
    return cur,bits,ranks,units


def maximum_cover(cur):
    empty=(*cur[:2],set(),cur[3]);D=candidates(empty)
    caps,paircerts=tile_cover(empty,D);assert sum(map(sum,caps))==189
    covered=set();patches=[]
    for r,c in ((2,12),(8,12),(10,16)):
        cells={(r+i,c+j) for i in range(4) for j in range(2)}
        assert not cells&covered;covered|=cells
        xs=D&cells;ends=[sorted(xs&{(r+i,c),(r+i,c+1)}) for i in (0,3)]
        mid=sorted(xs-set().union(*map(set,ends)));pairs=ends+[mid]
        assert len(xs)==6 and all(len(p)==2 and not feasible(empty,p) for p in pairs)
        assert sum(caps[i//2][c//2] for i in (r,r+2))==4
        patches.append(dict(origin=[r,c],cap=3,pairs=[dict(pair=p,**blocker(empty,p)) for p in pairs]))
    assert len(cur[2])==186==189-len(patches)
    return dict(tile_caps=caps,tile_sum=189,cap1_pair_obstructions=paircerts,
                disjoint_cap3_patches=patches,upper_bound=186,feasible_attainer=186)


def mandatory_selections(cur):
    """Two possible strict witnesses force every external one to be T.

    The actual mate of p cannot be a strict witness for p, since its own
    mate is p. Every selected external site lies in the P-only candidate
    hull by hereditary feasibility. This establishes necessity, not sufficiency.
    """
    P={v for edge in cur[3] for v in edge}
    mate={v:u for edge in cur[3] for v,u in (edge,edge[::-1])}
    D=candidates((*cur[:2],set(),cur[3]));forced=set();records=[]
    for p in sorted(P):
        possible=(neighbors(p)-{mate[p]})&(P|D)
        if len(possible)!=2:continue
        extra=possible&D;forced|=extra
        if extra:records.append(dict(endpoint=p,possible_strict_witnesses=sorted(possible),
                                     necessarily_selected=sorted(extra)))
    assert len(forced)==15 and forced<=cur[2]
    return dict(necessary_selected=sorted(forced),endpoint_obstructions=records,
                sufficient_for_freezing_claim=False)


def profile(cur,bits,ranks,units,E,F,counts):
    direct_check(*cur);P={v for e in cur[3] for v in e};assert len(P)==70
    counts['strict_freezing_events']+=len(check_rank_certificate(cur,ranks))
    assert frozen_certificate(cur)[0]==P
    regs=regions(cur,bits,{0} if E else set(),{0} if F else set())
    d,cl,N=compile_model(cur,regs);own,A,B,X=owner_data(*d[:2])
    a,b,z=own[3,12],own[5,17],own[5,15]
    assert A=={a,b} and (len(A),len(B),len(X))==(2,2,5)
    assert all(len(neighbors(v)&(P|cur[2]))==3 for o in A for v in d[1][o])
    assert len(d[4])==3==cur[0]*cur[1]//2-len(cur[2])-len(cur[3])
    fs=forests(cur,regs)
    wanted={units['R'],units['J'] if F else units['Q'],units['K'] if E else units['U']}
    assert {fs[j][1] for j in d[4]}==wanted
    supports={o:{fs[j][1] for j in W} for o,W in d[3].items()}
    assert supports[a]==({units['J']} if F else set())|({units['K']} if E else set())
    assert supports[z]==(set() if F else {units['Q']})
    assert all(not W for o,W in supports.items() if o not in (a,z))
    external={(p,t) for p,t in d[2] if own[p]!=own[t]}
    assert {(p,t) for p,t in external if own[p] in {a,b,z}}=={((5,17),(5,16))}
    assert not {a,b,z}&B
    answer=fork_flow(*d);alt=optimize(*d);expected=(1+int(E and not F),int(not F))
    assert (answer['value'],answer['cost'])==(alt['value'],alt['cost'])==expected
    # Target-deletion and actual withdrawing resource, in the OLD E state.
    if not F:
        lost={j for j in d[4] if fs[j][1]==units['Q']}
        no_target=omit(d,{a});residual=omit(d,{a},d[4]-lost)
        for model,want in ((no_target,(1,1)),(residual,(0,0))):
            ff=fork_flow(*model);aa=optimize(*model)
            assert (ff['value'],ff['cost'])==(aa['value'],aa['cost'])==want
            counts['independent_primitive_optima']+=1
    counts['independent_primitive_optima']+=1;counts['direction_profiles']+=1
    return d,cl,dict(empty_tile=E,elbow=F,value=expected[0],links=expected[1],
        raw=3,slack=3,alpha=2,beta=2,mixed=5,selected=186,frozen_endpoints=70,
        source_units={label:[sorted(cells) for cells in sorted(supports[o],key=lambda c:sorted(c))]
                      for label,o in [('a',a),('b',b),('z',z)]})


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    cur,bits,ranks,units=fixture();direct_check(*cur);assert len(ranks)==12
    cover=maximum_cover(cur);mandatory=mandatory_selections(cur)
    counts=Counter();records=[];first=None
    for E,F in itertools.product((False,True),repeat=2):
        d,cl,row=profile(cur,bits,ranks,units,E,F,counts);records.append(row)
        if first is None:first=(d,cl)
        assert d[:2]==first[0][:2] and set(d[2])==set(first[0][2])
        assert [x['body'] for x in cl]==[x['body'] for x in first[1]]
    # Normalize the reflected elbow and invoke the separately proved adapter.
    R,C=cur[:2]
    normalized=R,C,{(r,C-1-c) for r,c in cur[2]},[tuple((r,C-1-c) for r,c in e) for e in cur[3]]
    for E,essential in ((False,0),(True,1)):
        b=dict(bits)
        if E:b[10,16]=False
        regs=canonical_bands(R,C,[rectangle(r,r+2,C-c-2,C-c,v) for (r,c),v in b.items()])
        z=adapter(normalized,regs,2,14,True)
        assert (z['delta'],z['rank_loss'],z['old_essential_source'],z['old_value'],z['new_value'])==(1,1,essential,1+essential,1)
        counts['general_adapter_independent_optima']+=4
    # All eight dihedral images, all four E/F states: no orientation artifact.
    for transpose,flipr,flipc in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,transpose,flipr,flipc);image=(*shape,T,M);direct_check(*image)
        def point(v):
            r,c=v
            if flipr:r=R-1-r
            if flipc:c=C-1-c
            return (c,r) if transpose else (r,c)
        rr=[[point(v) for v in layer] for layer in ranks]
        counts['strict_freezing_events']+=len(check_rank_certificate(image,rr))
        for E,F in itertools.product((False,True),repeat=2):
            bb=dict(bits)
            if E:bb[10,16]=False
            if F:bb[2,12]=bb[4,12]=True
            regs=[]
            for (r,c),v in bb.items():
                cells=[point((r+i,c+j)) for i,j in itertools.product(range(2),repeat=2)]
                x=min(a for a,b in cells);y=min(b for a,b in cells)
                regs.append(rectangle(x,x+2,y,y+2,v!=transpose))
            data,_,_=compile_model(image,canonical_bands(*shape,regs))
            ff=fork_flow(*data);aa=optimize(*data);expect=(1+int(E and not F),int(not F))
            assert (ff['value'],ff['cost'])==(aa['value'],aa['cost'])==expect
            assert len(data[4])==3
            counts['dihedral_independent_direction_controls']+=1
    uniform=[]
    for vertical in (False,True):
        d,_,_=compile_model(cur,[rectangle(0,R,0,C,vertical)])
        own,A,B,X=owner_data(*d[:2]);ff=fork_flow(*d);aa=optimize(*d)
        assert (ff['value'],ff['cost'])==(aa['value'],aa['cost']) and ff['value']==len(A)
        uniform.append(dict(vertical=vertical,alpha=len(A),beta=len(B),raw=len(d[4]),value=ff['value'],links=ff['cost']))
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(counts),exact_maximum_cover=cover,
        records=records,uniform_direction_controls=uniform,full_freezing_necessary_selections=mandatory,
        theorem='TrueMaximumOverAllFeasibleTWithFixedPM=186_CompletelyFrozen70Endpoints12StrictWaves_AllAlphaTipsDegree3_CanonicalMixedFullPool3Units;PhysicalElbowDelta1RankLoss1_OldTargetUnpaid_NoPaymentGain;OneEmptyTilePays2ThenElbowDropsTo1_TargetEssential_e=r=1;DisprovesFixedPSelectionMaximumPlusCompleteFreezingForcesZeroWithdrawalLoss.',
        limits=['Not a numerical counterexample: slack3 remains positive.',
            'Not an optimized-N obstruction: one empty tile already pays both, and uniform directions also pay all their sources.',
            'No rectangular arbitrary-q exact-maximum assertion: saturated boundary choices are not directly stackable.',
            'Finite construction is a counterexample to a universal rule; optimum proved by a geometric cover, not solver output.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts),selected_maximum=186,fully_frozen=70,slack=3),indent=2))


if __name__=='__main__':main()
