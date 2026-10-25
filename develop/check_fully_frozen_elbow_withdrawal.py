"""Complete freezing does not force zero elbow withdrawal loss.

Written construction and arbitrary-copy proof:
docs/FULLY_FROZEN_ELBOW_WITHDRAWAL_OBSTRUCTION.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_physical_elbow_withdrawal import configuration_one as partial_one
from check_canonical_band_coarsening import canonical_bands, forests
from check_crossing_matching_ports import rectangle
from check_degree_changing_bent_completions import compile_model
from check_compensation_flow_normal_form import owner_data
from check_local_elbow_resource_transfer import adapter, omit
from check_promotion_cores import frozen_certificate
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def configuration_one():
    old, bits = partial_one()
    R,C,T,M = old
    shield_edges = {((2,14),(2,15)), ((11,14),(11,15))}
    M = [edge for edge in M if edge not in shield_edges]
    # One horizontal T--T pair changes the BT row phase without adding BB.
    additions = {(2,14),(2,15)} | {(2 if c%2 else 3,c) for c in range(16,C)}
    additions |= {(11,14),(10,15)}
    assert len(additions)==16 and not T & additions
    T = T | additions
    # This tile contains no P. A canonical cut here suppresses only the
    # target's old lower support. This is a legal direction change of N.
    bits[10,16] = True
    cur = (R,C,T,M)
    oldfrozen, oldlayers = frozen_certificate(old)
    P = {v for edge in M for v in edge}
    assert P == oldfrozen and len(P)==70
    ranks = [[item['endpoint'] for item in layer] for layer in oldlayers]
    assert len(ranks)==11
    # Independent strict-rank verifier, replaying the OLD partial schedule
    # unchanged on the NEW fully frozen board.
    check_rank_certificate(cur,ranks)
    return cur,bits,ranks


def stack(q):
    base,bits,ranks = configuration_one()
    assert q>=1
    R,C,T,M = base
    cur=(R*q,C,{(r+R*i,c) for i in range(q) for r,c in T},
         [tuple((r+R*i,c) for r,c in e) for i in range(q) for e in M])
    tiles={(r+R*i,c):v for i in range(q) for (r,c),v in bits.items()}
    # Replay copies in parallel waves; cross-copy ranks are irrelevant.
    layers=[[(r+R*i,c) for i in range(q) for r,c in layer] for layer in ranks]
    regions=canonical_bands(*cur[:2],[rectangle(r,r+2,c,c+2,v) for (r,c),v in tiles.items()])
    return cur,tiles,regions,layers


def check(q,actions,totals,independent=False):
    cur,bits,regs,layers=stack(q)
    direct_check(*cur)
    events=check_rank_certificate(cur,layers)
    P={v for edge in cur[3] for v in edge}
    assert len(events)==70*q and frozen_certificate(cur)[0]==P
    totals['independently_replayed_strict_freezing_events']+=len(events)
    d,cl,N=compile_model(cur,regs)
    own,A,B,X=owner_data(*d[:2])
    targets={own[16*i+3,12] for i in range(q)}
    sources={own[16*i+5,17] for i in range(q)}
    witnesses={own[16*i+5,15] for i in range(q)}
    assert A==targets|sources and len(A)==len(B)==2*q and len(X)==5*q
    assert len(d[4])==106*q and len(cur[2])==83*q and len(cur[3])==35*q
    assert cur[0]*cur[1]//2-len(cur[2])-len(cur[3])==106*q
    assert all(not d[3][a] for a in A)
    for a in A:
        for r,c in d[1][a]:
            assert len({(r+1,c),(r-1,c),(r,c+1),(r,c-1)}&(P|cur[2]))==3
    fs=forests(cur,regs)
    lost={}
    for i in range(q):
        z=own[16*i+5,15]
        assert set(cl[z]['body'])=={(16*i+5,15),(16*i+5,16)}
        lost[i]={j for j in d[4] if fs[j][1]==frozenset({(16*i+4,13),(16*i+5,13)})}
        assert len(lost[i])==1 and d[3][z]==lost[i]
        assert all({o for o,W in d[3].items() if j in W}=={z} for j in lost[i])
    external={(p,t) for p,t in d[2] if own[p]!=own[t]}
    reached=set(A)
    while True:
        extra={own[t] for p,t in external if own[p] in reached}-reached
        if not extra:break
        reached|=extra
    assert reached==A|witnesses
    assert {(p,t) for p,t in external if own[p] in reached}=={
        ((16*i+5,17),(16*i+5,16)) for i in range(q)}
    changed=dict(bits)
    for i in actions:changed[16*i+2,12]=changed[16*i+4,12]=True
    newregs=canonical_bands(*cur[:2],[rectangle(r,r+2,c,c+2,v) for (r,c),v in changed.items()])
    new,newcl,N1=compile_model(cur,newregs)
    assert new[:2]==d[:2] and set(new[2])==set(d[2])
    assert [o['body'] for o in newcl]==[o['body'] for o in cl]
    nf=forests(cur,newregs);newcells={nf[j][1] for j in new[4]}
    Q={j for j in d[4] if fs[j][1] not in newcells}
    expect=set().union(*(lost[i] for i in actions)) if actions else set()
    assert Q==expect and len(Q)==len(actions) and len(new[4])==len(d[4])
    for i in range(q):
        a,b,z=own[16*i+3,12],own[16*i+5,17],own[16*i+5,15]
        assert not new[3][b]
        assert bool(new[3][a])==(i in actions) and bool(new[3][z])==(i not in actions)
        if i in actions:
            assert len(new[3][a])==1
            j=next(iter(new[3][a]))
            assert nf[j][1]==frozenset({(16*i+4,12),(16*i+4,13)})
            assert {o for o,W in new[3].items() if j in W}=={a}
    residual=omit(d,targets,d[4]-Q)
    for model,value,cost in ((d,q,q),(omit(d,targets),q,q),
                             (residual,q-len(actions),q-len(actions)),(new,q,q-len(actions))):
        answer=fork_flow(*model)
        assert (answer['value'],answer['cost'])==(value,cost)
        if independent:
            alt=optimize(*model)
            assert (alt['value'],alt['cost'])==(value,cost)
            totals['independent_primitive_optima']+=1
    totals['fully_frozen_stack_action_profiles']+=1
    totals['fully_frozen_rank_one_transfers']+=len(actions)
    return dict(copies=q,actions=sorted(actions),old_value=q,old_cost=q,
                residual_value=q-len(actions),joint_loss=len(actions),
                new_value=q,new_cost=q-len(actions),fully_frozen=True,
                endpoints=70*q,freezing_waves=11,selected=83*q,matching_edges=35*q,
                raw=106*q,alpha=2*q,beta=2*q,mixed=5*q,slack=106*q)


def interaction(q,empty_actions,elbow_actions,totals,independent=False):
    cur,bits,regs,layers=stack(q)
    d,cl,_=compile_model(cur,regs);own,A,B,X=owner_data(*d[:2])
    oldfs=forests(cur,regs)
    for i in empty_actions:bits[16*i+10,16]=False
    for i in elbow_actions:bits[16*i+2,12]=bits[16*i+4,12]=True
    rr=canonical_bands(*cur[:2],[rectangle(r,r+2,c,c+2,v) for (r,c),v in bits.items()])
    new,newcl,_=compile_model(cur,rr);fs=forests(cur,rr)
    assert d[:2]==new[:2] and set(d[2])==set(new[2])
    assert [o['body'] for o in cl]==[o['body'] for o in newcl]
    assert len(new[4])==106*q
    oldcells={oldfs[j][1] for j in d[4]};newcells={fs[j][1] for j in new[4]}
    removed={frozenset({(16*i+11,16),(16*i+11,17)}) for i in empty_actions}
    removed|={frozenset({(16*i+4,13),(16*i+5,13)}) for i in elbow_actions}
    added={frozenset({(16*i+10,16),(16*i+11,16)}) for i in empty_actions}
    added|={frozenset({(16*i+4,12),(16*i+4,13)}) for i in elbow_actions}
    assert oldcells-newcells==removed and newcells-oldcells==added
    for i in empty_actions:
        u=next(j for j in d[4] if oldfs[j][1]==frozenset({(16*i+11,16),(16*i+11,17)}))
        assert not any(u in W for W in d[3].values())
    for o in range(len(d[1])):
        if o not in A:
            assert {oldfs[j][1] for j in d[3][o]}-removed=={fs[j][1] for j in new[3][o]}
    for i in range(q):
        a,b,z=own[16*i+3,12],own[16*i+5,17],own[16*i+5,15]
        expected=[]
        if i in empty_actions:expected.append(frozenset({(16*i+10,16),(16*i+11,16)}))
        if i in elbow_actions:expected.append(frozenset({(16*i+4,12),(16*i+4,13)}))
        assert {fs[j][1] for j in new[3][a]}==set(expected)
        assert all({o for o,W in new[3].items() if j in W}=={a} for j in new[3][a])
        assert not new[3][b]
        assert bool(new[3][z])==(i not in elbow_actions)
    f=fork_flow(*new)
    expected=(q+len(empty_actions-elbow_actions),q-len(elbow_actions))
    assert (f['value'],f['cost'])==expected
    if independent:
        alt=optimize(*new)
        assert (alt['value'],alt['cost'])==expected
        totals['interaction_independent_primitive_optima']+=1
    totals['joint_empty_tile_elbow_profiles']+=1
    return dict(copies=q,empty_tile_actions=sorted(empty_actions),elbow_actions=sorted(elbow_actions),
                value=f['value'],cost=f['cost'],deficit=2*q-f['value'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();records=[]
    for q in range(1,5):
        for mask in range(1<<q):
            records.append(check(q,{i for i in range(q) if mask>>i&1},totals,q<=3))
    for q in (8,16,32):
        for F in (set(),{0},set(range(0,q,2)),set(range(q))):
            records.append(check(q,F,totals))
    interactions=[]
    for q in range(1,4):
        for e,f in itertools.product(range(1<<q),repeat=2):
            E={i for i in range(q) if e>>i&1};F={i for i in range(q) if f>>i&1}
            interactions.append(interaction(q,E,F,totals,True))
    for q in (8,16):
        allcopies=set(range(q));even=set(range(0,q,2))
        for E,F in ((allcopies,set()),(allcopies,allcopies),(even,even),(even,allcopies-even)):
            interactions.append(interaction(q,E,F,totals))
    cur,bits,regs,layers=stack(1);R,C=cur[:2]
    normalized=(R,C,{(r,C-1-c) for r,c in cur[2]},
                [tuple((r,C-1-c) for r,c in e) for e in cur[3]])
    normregs=canonical_bands(R,C,[rectangle(r,r+2,C-c-2,C-c,v) for (r,c),v in bits.items()])
    a=adapter(normalized,normregs,2,14,True)
    assert (a['old_value'],a['minus_value'],a['rest_value'],a['new_value'],
            a['rank_loss'],a['delta'],a['old_essential_source'])==(1,1,0,1,1,1,0)
    totals['general_adapter_independent_optima']+=4
    for transpose,flipr,flipc in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,transpose,flipr,flipc)
        def point(v):
            r,c=v
            if flipr:r=R-1-r
            if flipc:c=C-1-c
            return (c,r) if transpose else (r,c)
        regions=[]
        for (r,c),v in bits.items():
            cells=[point((x,y)) for x in (r,r+1) for y in (c,c+1)]
            x=min(x for x,y in cells);y=min(y for x,y in cells)
            regions.append(rectangle(x,x+2,y,y+2,v!=transpose))
        image=(*shape,T,M);direct_check(*image)
        check_rank_certificate(image,[[point(v) for v in layer] for layer in layers])
        data,_,_=compile_model(image,canonical_bands(*shape,regions))
        f=fork_flow(*data);alt=optimize(*data)
        assert (f['value'],f['cost'])==(alt['value'],alt['cost'])==(1,1)
        totals['dihedral_fully_frozen_controls']+=1
    uniform_controls=[]
    for vertical,expected in ((False,(2,0,108,2,2)),(True,(2,2,106,2,0))):
        data,_,_=compile_model(cur,[rectangle(0,R,0,C,vertical)])
        _,A,B,_=owner_data(*data[:2]);f=fork_flow(*data);alt=optimize(*data)
        profile=(len(A),len(B),len(data[4]),f['value'],f['cost'])
        assert profile==expected and (alt['value'],alt['cost'])==profile[-2:]
        uniform_controls.append(dict(vertical=vertical,alpha=len(A),beta=len(B),
                                     raw=len(data[4]),value=f['value'],cost=f['cost']))
        totals['uniform_direction_independent_controls']+=1
    fixture=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],
                 tile_directions=[[r,c,int(v)] for (r,c),v in sorted(bits.items())],
                 strict_freezing_layers=layers,patch=dict(row=2,column=12,reflected_horizontally=True),
                 expected=records[1])
    fp=Path(__file__).parent/'fixtures/fully_frozen_elbow_rank_one.json'
    fp.write_text(json.dumps(fixture,indent=2)+'\n')
    saved=json.loads(fp.read_text());reloaded=(*saved['shape'],set(map(tuple,saved['selected'])),
                                            [tuple(map(tuple,e)) for e in saved['matching']])
    assert reloaded==cur and saved['expected']==records[1]
    check_rank_certificate(reloaded,[[tuple(v) for v in layer] for layer in saved['strict_freezing_layers']])
    report=dict(status='PASS',counts=dict(totals),records=records,uniform_controls=uniform_controls,
        empty_tile_elbow_interactions=interactions,
        theorem='FullyFrozenCanonicalFullPoolPhysicalElbowDelta1RankLoss1;All70EndpointsFrozenIn11ReplayedStrictWaves_AllAlphaTerminalsDegree3;ArbitraryQIndependentCopiesAnyActionSetF_OldValueQ_NewValueQ_JointLossAbsF_NewCostQMinusAbsF;RefutesFullFreezingImpliesZeroElbowWithdrawalLoss;ExtraEmptyTileActionE_GivesExactVQPlusAbsEMinusF_CostQMinusAbsF;SameCopyEmptyTileAlonePays2_ThenElbowDropsTo1_AllOwnersAndLinksInvariant',
        limits=['Not a numerical target-inequality counterexample: S=106 per copy.',
                'Does not refute a compensation rule allowed to alter other directions or use a larger justified interface.',
                'No end-to-end Lean claim; general freezing replay lemma formalized separately.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals)),indent=2))


if __name__=='__main__':main()
