"""Exact signed support compiler for arbitrary mixed-target P-free pivots.

General proof: docs/SIGNED_MIXED_SUPPORT_COMPILER.md. The compiler uses at
most three physical snapshots. Recognition enumerates literal falsifiers,
not gate subsets; exhaustive states below are independent audits only.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_positive_capacity_handoffs import snapshot as anchored_snapshot, recognize as uniform_recognize, endpoint_trap
from check_canonical_band_coarsening import random_board
from check_uniform_zero_capacity_openings import tile_cells
from check_compensation_flow_normal_form import owner_data
from check_fully_frozen_elbow_withdrawal import configuration_one
from check_P_free_pivot_interface import family as loss_family
from check_protected_linear_corridors import frozen_board, subsets
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize
from check_old_link_batch_repair import repair

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def snapshot(cur,bits,gates,changed=frozenset()):
    at={g:i for i,g in enumerate(gates)}
    state={g:not v if at.get(g) in changed else v for g,v in bits.items()}
    return anchored_snapshot(cur,state,gates)


def compile_signed(cur,bits,gates):
    """Compile every owner's support at every state, including rejected inputs."""
    direct_check(*cur);assert len(set(gates))==len(gates)
    P={v for e in cur[3] for v in e}
    assert all(g in bits and not tile_cells(g)&P for g in gates)
    cache={}
    def get(F):
        F=frozenset(F)
        if F not in cache:cache[F]=snapshot(cur,bits,gates,F)
        return cache[F]
    old=get(set());terms=defaultdict(list);records=[]
    for axis in (False,True):
        F={i for i,g in enumerate(gates) if bits[g]!=axis}
        potential=get(F)
        assert old['data'][:2]==potential['data'][:2]
        assert set(old['data'][2])==set(potential['data'][2])
        assert old['data'][4]==potential['data'][4]
        assert [x['body'] for x in old['closed']]==[x['body'] for x in potential['closed']]
        body_owner={v:o for o,x in enumerate(old['closed']) for v in x['body']}
        b=0;placed=[];seen=[]
        for region in potential['regs']:
            for band in region['bands']:
                if region['vertical']==axis:
                    fixed=min((c if axis else r) for r,c in band[0])
                    start=min((r if axis else c) for r,c in band[0])
                    def boundary(i):
                        if not 0<=i<len(band):return None
                        users={body_owner[v] for v in band[i] if v in body_owner}
                        assert len(users)<=1
                        return next(iter(users),None)
                    pos=0
                    while pos<len(band):
                        if set(band[pos])&P:pos+=1;continue
                        first=pos
                        while pos<len(band) and not set(band[pos])&P:pos+=1
                        after=pos;L,R=boundary(first-1),boundary(after)
                        units=[uid for j,uid in potential['mapping'].items()
                            if j[0]==b and first<=j[1]<=j[2]<after]
                        gate_ids=[i for i,(r,c) in enumerate(gates)
                            if (c if axis else r)==fixed and
                            start+first<=(r if axis else c) and (r if axis else c)+1<start+after]
                        placed+=gate_ids;seen+=units
                        for uid in units:
                            coord=min((r if axis else c) for r,c in potential['anchors'][uid])
                            for side,o in ((-1,L),(1,R)):
                                if o is None:continue
                                needed=[i for i in gate_ids if
                                    (gates[i][0 if axis else 1]<=coord if side==-1 else
                                     gates[i][0 if axis else 1]+1>=coord)]
                                literals=frozenset((i,bits[gates[i]]!=axis) for i in needed)
                                terms[uid,o].append(literals)
                                records.append(dict(resource=uid,owner=o,axis=axis,side=side,
                                    literals=sorted(literals)))
                b+=1
        assert len(placed)==len(gates) and set(placed)==set(range(len(gates)))
        expected={j for j in potential['data'][4] if potential['axes'][j]==axis}
        assert len(seen)==len(expected) and set(seen)==expected
    for (j,o),ts in terms.items():
        assert len(ts)<=4
        if j[0]=='fixed':assert len(ts)<=2
        else:assert all(any(i==j[1] for i,v in t) for t in ts)
        assert all(len({i for i,v in t})==len(t) for t in ts)
    return dict(old=old,terms=dict(terms),corridor_records=records,snapshots=len(cache),
        gates=list(gates),initial_bits=dict(bits),resources=old['data'][4])


def true_term(term,F):
    return all((i in F)==v for i,v in term)


def support(compiled,F):
    W={o:set() for o in compiled['old']['data'][3]}
    for (j,o),terms in compiled['terms'].items():
        if any(true_term(t,F) for t in terms):W[o].add(j)
    return W


def model_at(compiled,F):
    assert set(F)<=set(range(len(compiled['gates'])))
    base=compiled['old']['data']
    return (*base[:3],support(compiled,F),base[4])


def loss_witness(terms,gate):
    """Find F -> F+gate with true -> false, in polynomial literal choices.

    A losing old term must contain (gate,False). Its other literals fix a
    consistent base state. Each new term must have one false literal. On
    physical compiled DNFs at most two terms remain undecided after the base.
    """
    for oldterm in terms:
        if (gate,False) not in oldterm:continue
        forced=dict(oldterm);forced[gate]=True
        clauses=[];impossible=False
        for term in terms:
            if any(i in forced and forced[i]!=v for i,v in term):continue
            free=[(i,not v) for i,v in term if i not in forced]
            if not free:impossible=True;break
            clauses.append(free)
        if impossible:continue
        assert len(clauses)<=2
        for choices in itertools.product(*clauses):
            assignment=dict(forced);consistent=True
            for i,v in choices:
                if i in assignment and assignment[i]!=v:consistent=False;break
                assignment[i]=v
            if not consistent:continue
            after={i for i,v in assignment.items() if v};before=after-{gate}
            assert any(true_term(t,before) for t in terms)
            assert not any(true_term(t,after) for t in terms)
            return dict(from_changed=sorted(before),to_changed=sorted(after),gate=gate,
                old_term=sorted(oldterm),undecided_new_terms=len(clauses))
    return None


def recognize(compiled):
    losses=[]
    for (j,o),terms in compiled['terms'].items():
        negative={i for t in terms for i,v in t if not v}
        for i in sorted(negative):
            witness=loss_witness(terms,i)
            if witness is not None:losses.append(dict(resource=j,owner=o,**witness))
    return dict(accepted=not losses,losses=losses,snapshots=compiled['snapshots'])


def positive_support(compiled,F):
    """Exact only after all-state monotonicity has been established."""
    W={o:set() for o in compiled['old']['data'][3]}
    for (j,o),terms in compiled['terms'].items():
        if any({i for i,v in term if v}<=F for term in terms):W[o].add(j)
    return W


def old_phase_birth(n,one=False):
    """Lossless mixed targets, but genuinely new support in the old phase.

    q's incidence is x_q OR AND_(i<q) x_i for every n>=2. All other old
    support is constant. Feasible bent mixed owner; no freezing claim.
    """
    cur,bits,gates=endpoint_trap(one,n);R,C,T,M=cur
    zero_tiles=gates[:-1]+[(4,2*n+2)]
    T=T|{v for r,c in zero_tiles for v in ((r,c),(r+1,c+1))}
    bits[gates[-1]]=False
    return (R,C,T,M),bits,gates


def audit(cur,bits,gates,counts,states=None,primitive=True):
    compiled=compile_signed(cur,bits,gates);recognized=recognize(compiled)
    all_states=states is None
    choices=list(subsets(range(len(gates)))) if all_states else states
    physical={};old=compiled['old'];oldpack=fork_flow(*old['data'])
    for F in choices:
        F=frozenset(F);s=snapshot(cur,bits,gates,F)
        assert s['data'][:2]==old['data'][:2] and set(s['data'][2])==set(old['data'][2])
        assert s['data'][4]==old['data'][4]
        assert support(compiled,F)==s['data'][3]
        if recognized['accepted']:
            assert positive_support(compiled,F)==s['data'][3]
            counts['accepted_positive_retraction_states']+=1
        if primitive:
            f=fork_flow(*s['data']);p=optimize(*s['data'])
            assert (f['value'],f['cost'])==(p['value'],p['cost'])
            counts['independent_physical_optima']+=1
        repaired=repair(model_at(compiled,F),oldpack)
        assert repaired['feasible']
        counts['old_pack_repair_states']+=1
        physical[F]=s
        counts['physical_support_states']+=1
        counts['capacity_two_twin_states']+=sum(2-len(tile_cells(g)&cur[2])==2 for g in gates)
    if all_states:
        monotone=True
        for F,s in physical.items():
            for i in set(range(len(gates)))-F:
                monotone &= all(S<=physical[F|{i}]['data'][3][o] for o,S in s['data'][3].items())
                counts['all_boolean_lattice_edges']+=1
        assert recognized['accepted']==monotone
        counts['exact_recognition_iff_exhaustive']+=1
    for w in recognized['losses']:
        before=snapshot(cur,bits,gates,set(w['from_changed']))
        after=snapshot(cur,bits,gates,set(w['to_changed']))
        assert w['resource'] in before['data'][3][w['owner']]
        assert w['resource'] not in after['data'][3][w['owner']]
        counts['physical_loss_certificates']+=1
        counts['max_undecided_new_terms']=max(counts['max_undecided_new_terms'],w['undecided_new_terms'])
    if all(bits[g] for g in gates):
        other=uniform_recognize(cur,bits,gates)
        assert other['accepted']==recognized['accepted']
        counts['prior_uniform_recognizer_comparisons']+=1
    counts['models']+=1;counts['accepted' if recognized['accepted'] else 'rejected']+=1
    counts['mixed_target_models']+=len({bits[g] for g in gates})==2
    counts['max_compiler_snapshots']=max(counts['max_compiler_snapshots'],compiled['snapshots'])
    counts['signed_corridor_terms']+=len(compiled['corridor_records'])
    counts['negative_literal_occurrences']+=sum(not v for r in compiled['corridor_records'] for i,v in r['literals'])
    counts['positive_literal_occurrences']+=sum(v for r in compiled['corridor_records'] for i,v in r['literals'])
    for g in gates:counts['gate_capacity_'+str(2-len(tile_cells(g)&cur[2]))]+=1
    return compiled,recognized


def logic_controls(counts):
    # Coincident global owners may provide an unconditional opposite arm;
    # rejecting each shrinking term independently would be incorrect.
    assert loss_witness([frozenset({(0,False)}),frozenset()],0) is None
    assert loss_witness([frozenset({(0,False)}),frozenset({(1,True)})],0) is not None
    # Handoff: preserving initial incidences alone misses potential old support
    # exposed only after another gate changes.
    terms=[frozenset({(0,False),(1,True)}),frozenset({(0,True),(2,True)})]
    w=loss_witness(terms,0);assert w and w['from_changed']==[1] and w['to_changed']==[0,1]
    terms=[frozenset({(0,False)}),frozenset({(0,True),(1,True)}),frozenset({(0,True),(2,True)})]
    w=loss_witness(terms,0);assert w and w['undecided_new_terms']==2
    terms=[frozenset({(0,False)}),frozenset({(0,True),(1,True)}),frozenset({(0,True),(1,False)})]
    assert loss_witness(terms,0) is None
    assert true_term(frozenset({(0,False)}),set()) and not true_term(frozenset({(0,False)}),{0})
    # Incompatible literal choices must not be merged as simultaneous offers.
    assert max(sum((i in F)==v for i,v in [(0,False),(0,True)]) for F in (set(),{0}))==1
    counts['logic_controls']=7


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();counts=Counter();rng=random.Random(2026102651);logic_controls(counts)
    for shape in ((4,4),(6,8),(8,8)):
        for index in range(28):
            raw=random_board(*shape,rng)
            if index%2:
                cur=(*raw[:2],{v for v in raw[2] if rng.random()<.4},[e for e in raw[3] if rng.random()<.4])
            else:cur=raw
            P={v for e in cur[3] for v in e}
            bits={(r,c):bool(rng.getrandbits(1)) for r in range(0,cur[0],2) for c in range(0,cur[1],2)}
            candidates=[g for g in bits if not tile_cells(g)&P];rng.shuffle(candidates)
            gates=candidates[:5]
            if index%7==0:
                for g in gates:bits[g]=True
            audit(cur,bits,gates,counts)
    controls=[]
    for one in (False,True):
        cur,bits,gates=endpoint_trap(one,4)
        bits[gates[1]]=False;bits[gates[3]]=False
        compiled,recognized=audit(cur,bits,gates,counts)
        assert not recognized['accepted']
        controls.append(dict(name='mixed-target-bent-endpoint-trap',capacity=1 if one else 2,
            accepted=False,losses=recognized['losses'][:2]))
    for n in (2,4,8):
        for one in (False,True):
            cur,bits,gates=old_phase_birth(n,one)
            compiled,recognized=audit(cur,bits,gates,counts,primitive=False)
            assert recognized['accepted']
            q=n-1;units={j for j in compiled['resources'] if j[0]=='gate' and j[1]==q}
            assert len(units)==(1 if one else 2)
            _,A,B,X=owner_data(*compiled['old']['data'][:2]);assert not A and not B and X=={0}
            assert len(cur[2])==2*n+1+one and len(cur[3])==2*n+2
            assert len(compiled['resources'])==4*n+13-one
            constant=support(compiled,set())[0]
            for F in subsets(range(n)):
                expected=q in F or set(range(q))<=F
                W=support(compiled,F)
                assert all((j in W[0])==expected for j in units)
                assert W[0]-units==constant
            # Before q switches, the earlier gates can expose support absent
            # initially. The final-direction-only offer would demand q.
            before=set(range(q));assert q not in before
            assert all(j not in support(compiled,set())[0] and j in support(compiled,before)[0] for j in units)
            assert all(j in positive_support(compiled,before)[0] for j in units)
            weights={i:1 for i in range(q)}|{q:n+1}
            fee=min(sum(weights[i] for i in F) for F in subsets(range(n))
                if next(iter(units)) in support(compiled,F)[0])
            assert fee==n-1 and fee<weights[q]
            controls.append(dict(name='lossless-old-phase-new-support',n=n,capacity=1 if one else 2,
                accepted=True,formula='x_q OR AND_(i<q) x_i',old_phase_state=sorted(before),
                true_minimum_access_fee=fee,final_phase_only_fee=weights[q],
                frozen=False,alpha=0,beta=0,mixed=1))
    for build in (lambda:loss_family(0),configuration_one):
        cur,bits,ranks=build();P={v for e in cur[3] for v in e}
        assert frozen_certificate(cur)[0]==P
        counts['strict_freezing_events']+=len(check_rank_certificate(cur,ranks))
        candidates=[g for g in bits if not tile_cells(g)&P]
        gates=[(2,16)]+[g for g in candidates if g!=(2,16)][:4]
        compiled,recognized=audit(cur,bits,gates,counts)
        assert recognized['accepted']==(len(cur[2])==83)
    # Thirty-five actual gates; all states are compiled symbolically. Only
    # selected states and every returned rejection witness are rebuilt.
    cur,bits,ranks,left,right,q=frozen_board(17,17)
    gates=left+right+[(2,16+2*q)]
    for i,g in enumerate(gates):bits[g]=bool(i%2)
    assert len(check_rank_certificate(cur,ranks))==140
    assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
    counts['strict_freezing_events']+=140
    choices=[set(),set(range(len(gates))),set(range(0,len(gates),2)),set(range(1,len(gates),2))]
    choices += [{i for i in range(len(gates)) if rng.getrandbits(1)} for _ in range(8)]
    compiled,recognized=audit(cur,bits,gates,counts,states=choices,primitive=False)
    controls.append(dict(name='frozen-35-mixed-target-gates',shape=list(cur[:2]),gates=35,
        compiler_snapshots=compiled['snapshots'],all_state_count=2**35,
        accepted=recognized['accepted'],loss_certificates=len(recognized['losses'])))
    # Production compilation must not enumerate gate subsets or optimize packs.
    with patch(__name__+'.subsets',side_effect=AssertionError('no subset enumeration')), \
         patch(__name__+'.fork_flow',side_effect=AssertionError('no flow')), \
         patch(__name__+'.optimize',side_effect=AssertionError('no pack optimization')):
        again=compile_signed(cur,bits,gates);assert recognize(again)['accepted']==recognized['accepted']
    counts['no_enumeration_api_controls']+=1
    assert counts['mixed_target_models'] and counts['gate_capacity_0'] and counts['gate_capacity_1'] and counts['gate_capacity_2']
    assert counts['positive_literal_occurrences'] and counts['negative_literal_occurrences']
    assert counts['max_compiler_snapshots']<=3
    report=dict(status='PASS',counts=dict(counts),controls=controls,
        proof='docs/SIGNED_MIXED_SUPPORT_COMPILER.md',
        scope='Exact signed support at every gate state and polynomial all-subset monotonicity recognition for arbitrary mixed-target aligned P-free tiles, capacities zero/one/two. Enumeration is audit only.',
        limitations=['No arbitrary-state joint fee optimizer.','No automatic compensation or universal 5/6 improvement.','Signed offers cannot be unioned without one consistent global gate assignment.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
