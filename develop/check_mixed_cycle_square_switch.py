"""Actual frozen square switch and all-original-availability value/link cost.

General proofs: docs/FROZEN_SQUARE_SWITCH_AND_INTERVAL_REPAIR.md.
Finite computations check the proofs, not replace them. No SAT dependency.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_frozen_mixed_gate_cycle import load_model, full_prediction
from check_occupied_cycle_chambers import actual
from check_merger_completion_reserves import feasible, frozen, owner_data, whole_bands, whole_support_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_reserve_boundary_split import clipped, distance
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize, primitive_certificates

if not __debug__:
    raise RuntimeError('Run without -O.')

FIXTURE=Path(__file__).parent/'fixtures/frozen_mixed_cycle_square_switch.json'


def model():
    before,old_data,old_meta,_,_,_,old_classes,_=load_model()
    record=json.loads(FIXTURE.read_text())
    cur=actual(record)
    assert feasible(cur) and frozen(cur)
    check_rank_certificate(cur,[[tuple(v) for v in layer] for layer in record['freezing_layers']])
    canon=lambda edges:{tuple(sorted(e)) for e in edges}
    assert cur[:3]==before[:3]
    assert {v for e in cur[3] for v in e}=={v for e in before[3] for v in e}
    assert canon(before[3])-canon(cur[3])==canon([((5,4),(6,4)),((5,5),(6,5))])
    assert canon(cur[3])-canon(before[3])==canon([((5,4),(5,5)),((6,4),(6,5))])
    data,meta,_=whole_support_data(cur,whole_bands(cur))
    own,alphas,betas,mixed=owner_data(*data[:2])
    old_own,old_alphas,old_betas,old_mixed=owner_data(*old_data[:2])
    assert (len(alphas),len(betas),len(mixed))==(4,6,15)
    assert tuple(map(len,(old_alphas,old_betas,old_mixed)))==(4,6,15)
    assert data[0]==old_data[0] and set(data[2])==set(old_data[2])
    assert meta['labels']==old_meta['labels']
    assert meta['intervals']==old_meta['intervals'] and meta['boundary']==old_meta['boundary']
    assert data[4]==old_data[4]
    _,old_components=independent_strands(before,whole_bands(before))
    _,new_components=independent_strands(cur,whole_bands(cur))
    body=lambda components,tip:next(b for ts,b in components if tip in ts)
    assert body(new_components,(24,4))==(body(old_components,(5,4))|body(old_components,(5,5)))-{(5,4),(5,5)}
    assert len(body(new_components,(24,4)))==40
    assert body(new_components,(5,5))=={(5,4),(5,5)}
    A,B,C,D=[own[v] for v in [(5,6),(5,19),(24,6),(24,4)]]
    g2,g3,short=[own[v] for v in [(24,18),(24,5),(5,5)]]
    assert set((A,B,C,D))==alphas and not data[3][A] and not data[3][B]
    assert set(data[1][D])=={(24,4),(14,11)}
    assert data[3][D]==old_data[3][old_own[5,4]]|old_data[3][old_own[5,5]]
    assert not data[3][short]
    for new_o,pair in enumerate(data[1]):
        if new_o in (D,short):
            continue
        assert set(pair)==set(old_data[1][old_own[pair[0]]])
        assert data[3][new_o]==old_data[3][old_own[pair[0]]]
    L,R,U,W=data[3][D],data[3][C],data[3][g2],data[3][g3]
    assert list(map(len,(L,R,U,W)))==[16,6,4,9]
    assert not (L&W or R&(L|U|W))
    identity=lambda b,c:meta['owner'][b,c]
    assert L&U=={identity(7,13),identity(7,15)}
    assert U&W=={identity(9,13),identity(9,14)}
    reach={a:distance(data,a) for a in alphas}
    assert not set(reach[D])&betas
    assert set(reach[D])=={D,g3,own[24,3]}
    assert not data[3][own[24,3]]
    assert set(reach[C])=={C,g2,g3,own[18,16]}
    betaC=own[18,16]
    assert data[3][betaC]<=W
    # Every possible reachable transition, including zero-support branches,
    # is retained in the exact ordinary/full primitive model.
    for a in (C,D):
        transitions={(own[u],own[v]) for u,v in data[2] if own[u] in reach[a] and own[u]!=own[v]}
        expected={(C,g2),(C,g3),(g2,betaC)} if a==C else {(D,g3),(D,own[24,3])}
        assert transitions==expected
    for source,edge in [(A,((5,17),(5,16))),(B,((5,19),(5,20)))]:
        target=own[edge[1]]
        assert edge in data[2] and target in betas
        assert {a for a in alphas if target in reach[a]}=={source}
    assert not any(p['kind']=='fork' for p in primitive_certificates(*data))
    return before,cur,old_data,data,meta,(L,R,U,W),old_classes


def distinct_pair(E,F,Q):
    return any(e!=f for e in E&Q for f in F&Q)


def prediction(classes,Q):
    L,R,U,W=classes
    l,r,u,w=[bool(Q&E) for E in classes]
    if not (l or w):
        return 3,2+(0 if r else 1 if u else 2)
    if r:
        return 4,2 if l else 3
    if l:
        return 4,3 if distinct_pair(L,U|W,Q) else 4
    return 4,4 if distinct_pair(U,W,Q) else 5


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    before,cur,old_data,data,meta,classes,old_classes=model()
    totals=Counter()
    rng=random.Random(2026102533)
    L,R,U,W=classes
    incidence_classes=[L-U,L&U,U&W,W-U,R]
    assert list(map(len,incidence_classes))==[14,2,2,7,6]
    choices=[]
    for i,E in enumerate(incidence_classes):
        ids=sorted(E)
        choices.append([set(),{ids[0]},set(ids[:2])] if i in (1,2,3) else [set(),{ids[0]}])
    pools=[set().union(set(),*parts) for parts in itertools.product(*choices)]
    pools+=[set(s) for n in (0,1,2) for s in itertools.combinations(sorted(data[4]),n)]
    pools+=[data[4]]+[{j for j in data[4] if rng.randrange(2)} for _ in range(160)]
    for i,Q in enumerate(pools):
        expected=prediction(classes,Q)
        flow=fork_flow(*clipped(data,Q))
        assert (flow['value'],flow['cost'])==expected
        if i<108 or i>=len(pools)-32:
            for allow in (False,True):
                brute=optimize(*clipped(data,Q),allow_forks=allow)
                assert (brute['value'],brute['cost'])==expected
                totals['independent_complete_ordinary_full_packs']+=1
        totals['complete_original_availability_models']+=1
    identity=lambda b,c:meta['owner'][b,c]
    named={}
    for name,Q in [
        ('empty',set()),('one_X',{identity(7,13)}),('both_X',{identity(7,13),identity(7,15)}),
        ('one_Y',{identity(9,13)}),('both_Y',{identity(9,13),identity(9,14)}),
        ('two_W_only',{identity(9,8),identity(9,9)}),('all',data[4])]:
        after=fork_flow(*clipped(data,Q));old=fork_flow(*clipped(old_data,Q))
        named[name]=dict(after_value=after['value'],after_cost=after['cost'],before_value=old['value'],before_cost=old['cost'])
    # Independent reflection adapters preserve the standard band partner.
    for vertical,horizontal in itertools.product((False,True),repeat=2):
        move=lambda v:(27-v[0] if vertical else v[0],23-v[1] if horizontal else v[1])
        image=(*cur[:2],{move(v) for v in cur[2]},[tuple(move(v) for v in e) for e in cur[3]])
        assert feasible(image) and frozen(image)
        image_data,_,_=whole_support_data(image,whole_bands(image))
        assert fork_flow(*clipped(image_data,set()))['value']==3
        assert fork_flow(*image_data)['value']==4
        totals['actual_frozen_reflections']+=1
    # Every choice of switched copies in literal q=2,3 boards; all-q is
    # proved by the separated support/owner identity construction in the note.
    for q in (2,3):
        for flags in itertools.product((False,True),repeat=q):
            T=set();M=[];moves=[]
            for i,flag in enumerate(flags):
                packet=cur if flag else before
                move=lambda v,offset=32*i+2:(v[0]+offset,v[1])
                moves.append(move)
                T|={move(v) for v in packet[2]}
                M+=[tuple(move(v) for v in e) for e in packet[3]]
            joined=(32*q,24,T,M)
            assert feasible(joined) and frozen(joined)
            joined_data,info,_=whole_support_data(joined,whole_bands(joined))
            own,aa,bb,mm=owner_data(*joined_data[:2])
            assert (len(aa),len(bb),len(mm))==(4*q,6*q,15*q)
            for mode in ('empty','all','random'):
                Q=set() if mode=='empty' else joined_data[4] if mode=='all' else {j for j in joined_data[4] if rng.randrange(3)==0}
                ev=ec=0
                for i,(flag,move) in enumerate(zip(flags,moves)):
                    shift=16*i+1
                    original_id={j:info['owner'][meta['intervals'][j]['band']+shift,meta['intervals'][j]['first']]
                                 for j in data[4]}
                    local_Q={j for j,newj in original_id.items() if newj in Q}
                    v,c=prediction(classes,local_Q) if flag else full_prediction(old_classes,local_Q)
                    ev+=v;ec+=c
                flow=fork_flow(*clipped(joined_data,Q))
                assert (flow['value'],flow['cost'])==(ev,ec)
                if mode=='empty':
                    assert (ev,ec)==(4*q-sum(flags),5*q-sum(flags))
                elif mode=='all':
                    assert (ev,ec)==(4*q,2*q)
                totals['literal_frozen_copy_availability_models']+=1
    record=dict(status='PASS',shape=cur[:2],selected=len(cur[2]),matching=len(cur[3]),endpoints=2*len(cur[3]),
        counts=dict(alpha=4,beta=6,mixed=15),all_original_interval_count=len(data[4]),
        unchanged=['T','P','M_cardinality','TP_BP_sites','physical_tip_adjacencies','interval_identities','boundary_marks','alpha_beta_mixed_counts','I_plus_beta_minus_alpha'],
        class_sizes=dict(L=16,R=6,U=4,W=9,X=2,Y=2),totals=dict(totals),named=named,
        scope='Actual frozen fixed-T/P square switch defeats beta-only persistence4to3; new alpha40P has no beta path and inherits old alpha/gate intervals. All final-original Q value/cost theorem written with distinct-unit AND capacity-one gate corrections. Complete pool still4/c2; allq beta-only loss with unchanged inventory. No universal compensation/5over6 counterexample.')
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record))


if __name__=='__main__':
    main()
