"""Mixed-target zero-capacity corridors and positive-capacity parameterization.

Proof: docs/MIXED_ZERO_CORRIDOR_OPTIMIZATION.md. Production enumerates only
positive-capacity gate assignments, never zero-capacity states or packings.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_signed_mixed_support import compile_signed, recognize, model_at, snapshot, old_phase_birth
from check_protected_linear_corridors import apply, offers, corridor_flow, subsets, frozen_board
from check_uniform_zero_capacity_openings import tile_cells
from check_canonical_band_coarsening import random_board
from check_destructive_exchange_choice import constrained_optimum
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize
from check_promotion_cores import frozen_certificate
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_compensation_flow_normal_form import owner_data

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def capacity(cur,g):
    return 2-len(tile_cells(g)&cur[2])


def compile_zero(cur,bits,gates,certified_monotone=False):
    """Exact final corridors on a support-monotone zero-capacity subcube.

    certified_monotone is an internal proof premise used by solve_parameterized
    after the parent signed recognizer has certified every subcube. Public
    callers should leave it False; no endpoint-only audit is sufficient.
    """
    assert all(capacity(cur,g)==0 for g in gates)
    signed=compile_signed(cur,bits,gates)
    result=dict(accepted=True,losses=[]) if certified_monotone else recognize(signed)
    if not result['accepted']:return result
    final=snapshot(cur,bits,gates,set(range(len(gates))))
    P={v for e in cur[3] for v in e}
    body_owner={v:o for o,x in enumerate(final['closed']) for v in x['body']}
    corridors=[];placed=[];seen=[];b=0
    for region in final['regs']:
        axis=region['vertical']
        for band in region['bands']:
            fixed=min((c if axis else r) for r,c in band[0])
            start=min((r if axis else c) for r,c in band[0])
            def boundary(i):
                if not 0<=i<len(band):return None
                owners={body_owner[v] for v in band[i] if v in body_owner}
                assert len(owners)<=1
                return next(iter(owners),None)
            pos=0
            while pos<len(band):
                if set(band[pos])&P:pos+=1;continue
                first=pos
                while pos<len(band) and not set(band[pos])&P:pos+=1
                after=pos
                units=[uid for j,uid in final['mapping'].items()
                       if j[0]==b and first<=j[1]<=j[2]<after]
                coordinate=lambda uid:min((r if axis else c) for r,c in final['anchors'][uid])
                units.sort(key=coordinate)
                gg=[i for i,(r,c) in enumerate(gates) if
                    (c if axis else r)==fixed and start+first<=(r if axis else c)
                    and (r if axis else c)+1<start+after]
                assert all(bits[gates[i]]!=axis for i in gg)
                slots=[(i,sum(coordinate(uid)<gates[i][0 if axis else 1] for uid in units)) for i in gg]
                placed+=gg;seen+=units
                if units or gg:corridors.append(dict(left=boundary(first-1),right=boundary(after),
                    units=units,gates=slots,axis=axis))
            b+=1
    assert len(placed)==len(gates) and set(placed)==set(range(len(gates)))
    assert len(seen)==len(final['data'][4]) and set(seen)==final['data'][4]
    assert all(j[0]=='fixed' for j in seen)
    data=final['data'];base=(*data[:3],{o:set() for o in data[3]},data[4])
    return dict(accepted=True,losses=[],base=base,corridors=corridors,signed=signed,
                snapshots_upper_bound=signed['snapshots']+1)


def solve_zero(cur,bits,gates,weights,required=frozenset(),compiled=None):
    """required must be feasible in the initial state (or in every state)."""
    assert set(weights)==set(range(len(gates)))
    assert all(isinstance(w,int) and w>=0 for w in weights.values())
    c=compiled if compiled is not None else compile_zero(cur,bits,gates)
    if not c['accepted']:return c
    result=corridor_flow(c['base'],c['corridors'],weights,required,independent=False)
    return dict(accepted=True,**result)


def solve_parameterized(cur,bits,gates,weights,required=frozenset()):
    """Exact 2^p polynomial solver, p = positive-capacity variable gates.

    Global support monotonicity is mandatory. required must be feasible in
    the global initial state; support monotonicity preserves it in each branch.
    Branch resources are never pooled. Returned gate IDs are global IDs.
    """
    assert set(weights)==set(range(len(gates)))
    assert all(isinstance(w,int) and w>=0 for w in weights.values())
    signed=compile_signed(cur,bits,gates);recognized=recognize(signed)
    if not recognized['accepted']:return recognized
    positive=[i for i,g in enumerate(gates) if capacity(cur,g)>0]
    zero=[i for i,g in enumerate(gates) if capacity(cur,g)==0]
    best=None;branches=0
    for assignment in itertools.product((False,True),repeat=len(positive)):
        fixed={i for i,on in zip(positive,assignment) if on};bb=dict(bits)
        for i in fixed:bb[gates[i]]=not bb[gates[i]]
        cc=compile_zero(cur,bb,[gates[i] for i in zero],certified_monotone=True)
        solved=solve_zero(cur,bb,[gates[i] for i in zero],
                          {k:weights[i] for k,i in enumerate(zero)},required,compiled=cc)
        opened=fixed|{zero[k] for k in solved['opened']}
        candidate=dict(accepted=True,value=solved['value'],fee=sum(weights[i] for i in opened),
            links=solved['links'],opened=sorted(opened),paid=solved['paid'])
        if best is None or (candidate['value'],-candidate['fee'],-candidate['links'])> \
                (best['value'],-best['fee'],-best['links']):best=candidate
        branches+=1
    assert best is not None
    return dict(**best,positive_gates=len(positive),zero_gates=len(zero),branches=branches)


def audit(cur,bits,gates,counts,parameterized=True):
    signed=compile_signed(cur,bits,gates);recognition=recognize(signed)
    zero=all(capacity(cur,g)==0 for g in gates)
    compiled=compile_zero(cur,bits,gates) if zero else None
    if zero:assert compiled['accepted']==recognition['accepted']
    if not recognition['accepted']:
        counts['rejected_models']+=1
        if parameterized:assert not solve_parameterized(cur,bits,gates,dict.fromkeys(range(len(gates)),1))['accepted']
        return
    states={};old=signed['old']['data']
    for F in subsets(range(len(gates))):
        physical=snapshot(cur,bits,gates,F)['data']
        assert physical==model_at(signed,F)
        if zero:
            assert apply(compiled['base'],compiled['corridors'],F)==physical
            compressed=apply(compiled['base'],compiled['corridors'],F,True)
            assert constrained_optimum(compressed)==constrained_optimum(physical)
            counts['exact_zero_final_corridor_states']+=1
        f=fork_flow(*physical);p=optimize(*physical)
        assert (f['value'],f['cost'])==(p['value'],p['cost'])
        states[F]=physical;counts['independent_physical_optima']+=1
    for profile in range(3):
        weights={i:(0 if profile==0 else 1 if profile==1 else (i*5+2)%7) for i in range(len(gates))}
        # Independent primitive DP over all physical states, including fees
        # for unused gates. Enumeration is deliberately confined to this audit.
        for required in (frozenset(),*initial_prescriptions(old)):
            candidates=[]
            for F,data in states.items():
                pair=constrained_optimum(data,required);assert pair is not None
                candidates.append((pair[0],sum(weights[i] for i in F),pair[1]))
            expected=max(candidates,key=lambda t:(t[0],-t[1],-t[2]))
            if zero:
                solved=solve_zero(cur,bits,gates,weights,required,compiled)
                assert (solved['value'],solved['fee'],solved['links'])==expected
                counts['single_flow_lex_optima']+=1
            if parameterized:
                solved=solve_parameterized(cur,bits,gates,weights,required)
                assert solved['branches']==2**sum(capacity(cur,g)>0 for g in gates)
                assert (solved['value'],solved['fee'],solved['links'])==expected
                counts['parameterized_lex_optima']+=1
            actual=constrained_optimum(states[frozenset(solved['opened'])],required)
            assert actual==(solved['value'],solved['links'])
            assert solved['fee']==sum(weights[i] for i in solved['opened'])
            assert required<=set(solved['paid'])
            counts['nonempty_prescribed_optima']+=bool(required)
    counts['accepted_models']+=1;counts['zero_models']+=zero
    counts['mixed_target_accepted_models']+=len({bits[g] for g in gates})==2


def initial_prescriptions(data):
    # Independent feasibility oracle is audit-only, never used by production.
    _,eligible,_,_=owner_data(*data[:2])
    result=[]
    for o in sorted(eligible):
        if constrained_optimum(data,{o}) is not None:result.append(frozenset({o}))
        if len(result)==2:break
    return result


def doubled_frozen(n=2,single=False,positive=False):
    """Separated frozen board plus transpose: both target directions active."""
    cur,bits,ranks,left,right,q=frozen_board(n,n,single)
    if positive:bits[2,16+2*q]=True
    R,C,T,M=cur;offset=R+4
    trans=lambda v:(offset+v[1],v[0])
    doubled=(offset+C,C,T|set(map(trans,T)),M+[tuple(map(trans,e)) for e in M])
    bb={(r,c):False for r in range(0,doubled[0],2) for c in range(0,C,2)}
    bb.update(bits);bb.update({trans(g):not v for g,v in bits.items()})
    rr=[[v for layer in (x,list(map(trans,x))) for v in layer] for x in ranks]
    gates=left+right+list(map(trans,left+right))
    if positive:gates += [(2,16+2*q),trans((2,16+2*q))]
    return doubled,bb,rr,gates


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();counts=Counter();rng=random.Random(2026102663);controls=[]
    for R,C in ((4,4),(6,8),(8,8)):
        for rep in range(35):
            cur=random_board(R,C,rng);bits={(r,c):bool(rng.getrandbits(1)) for r in range(0,R,2) for c in range(0,C,2)}
            P={v for e in cur[3] for v in e}
            candidates=[g for g in bits if not tile_cells(g)&P]
            if rep%2==0:candidates=[g for g in candidates if capacity(cur,g)==0]
            rng.shuffle(candidates);gates=candidates[:3]
            audit(cur,bits,gates,counts)
    # Previously discovered old-phase birth has positive capacity. The zero
    # theorem must not be applied to it; parameterization remains exact.
    for n in (2,3,4):
        for one in (False,True):
            cur,bits,gates=old_phase_birth(n,one)
            audit(cur,bits,gates,counts)
            try:compile_zero(cur,bits,gates)
            except AssertionError:counts['positive_capacity_zero_adapter_rejections']+=1
            else:raise AssertionError('Positive gate silently accepted')
    for n in (1,2):
        cur,bits,ranks,gates=doubled_frozen(n)
        assert len(check_rank_certificate(cur,ranks))==280
        assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
        signed=compile_signed(cur,bits,gates);assert recognize(signed)['accepted']
        c=compile_zero(cur,bits,gates);weights={i:1+i%3 for i in range(len(gates))}
        solved=solve_zero(cur,bits,gates,weights,compiled=c)
        assert solved['value']==8 and solved['links']==4
        assert solved['fee']==sum(weights.values()) and set(solved['opened'])==set(weights)
        for F in subsets(range(len(gates))):
            actual=snapshot(cur,bits,gates,F)['data']
            assert apply(c['base'],c['corridors'],F)==actual
            f=fork_flow(*actual)
            # Each of the four independent opening chains gives one payment.
            groups=[set(range(k*n,(k+1)*n)) for k in range(4)]
            assert f['value']==4+sum(G<=F for G in groups) and f['cost']==4
            counts['frozen_mixed_target_physical_states']+=1
        counts['strict_freezing_events']+=280
        controls.append(dict(name='two-direction-frozen-payment',n=n,shape=list(cur[:2]),
            gates=len(gates),initial_payment=4,final_payment=8,**solved))
        if n==1:audit(cur,bits,gates,counts)
    for single in (False,True):
        cur,bits,ranks,gates=doubled_frozen(1,single=single,positive=True)
        audit(cur,bits,gates,counts)
        assert len(check_rank_certificate(cur,ranks))==280
        assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
        weights={i:1+i%3 for i in range(len(gates))}
        solved=solve_parameterized(cur,bits,gates,weights)
        assert solved['positive_gates']==2 and solved['branches']==4
        assert solved['value']==(6 if single else 8) and solved['links']==4
        counts['strict_freezing_events']+=280
        controls.append(dict(name='frozen-mixed-positive-branches',capacity=1 if single else 2,**solved))
    # Large zero subcube: production must neither enumerate its states nor
    # call the primitive oracle. Only 2^p positive assignments may be visited.
    cur,bits,ranks,gates=doubled_frozen(9)
    weights=dict.fromkeys(range(len(gates)),1)
    with patch(__name__+'.subsets',side_effect=AssertionError('No zero-state enumeration')), \
         patch(__name__+'.constrained_optimum',side_effect=AssertionError('No primitive DP')), \
         patch(__name__+'.optimize',side_effect=AssertionError('No primitive optimization')):
        solved=solve_parameterized(cur,bits,gates,weights)
    assert solved['value']==8 and solved['fee']==36 and solved['branches']==1
    controls.append(dict(name='36-zero-gates-one-flow',symbolic_states=2**36,**solved))
    counts['production_no_zero_state_or_pack_enumeration_controls']+=1
    assert counts['mixed_target_accepted_models'] and counts['single_flow_lex_optima']
    assert counts['nonempty_prescribed_optima']
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(counts),controls=controls,
        proof='docs/MIXED_ZERO_CORRIDOR_OPTIMIZATION.md',
        scope='All-state support-monotone aligned P-free arbitrary mixed targets. Zero capacity: one exact costed full fork flow. General capacities: 2^p flows, p positive gates. Nonnegative integer fees. Required sources initially feasible.',
        limitations=['Not an arbitrary mixed-target polynomial algorithm when p is unbounded.',
                     'No universal 5/6 improvement or automatic geometric defect-tree elimination.',
                     'Finite state and primitive enumeration are independent audits only.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts),controls=controls),indent=2))


if __name__=='__main__':main()
