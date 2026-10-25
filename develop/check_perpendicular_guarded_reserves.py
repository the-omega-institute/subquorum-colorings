"""Perpendicular compensation for every T; joint maximality of attaining boards.

General proofs: PERPENDICULAR_GUARDED_RESERVES_AND_JOINT_MAXIMALITY.md.
Finite controls test those proofs; they do not establish the quantified claims.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_forced_mates_and_adjacent_maxima import configuration, uniform_freezing
from check_selection_maximum_singleton import compile_even_width
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize
from check_residual_corridors import direct_check
from check_frozen_shared_mixed_gate import check_rank_certificate

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def transpose(cur):
    """Bookkeeping for vertical bands on the SAME board, not a new placement."""
    return cur[1],cur[0],{(c,r) for r,c in cur[2]},[tuple((c,r) for r,c in e) for e in cur[3]]


def neighbourhoods(R,C):
    return {(r,c):{(a,b) for a,b in ((r-1,c),(r+1,c),(r,c-1),(r,c+1))
                   if 0<=a<R and 0<=b<C} for r in range(R) for c in range(C)}


def arbitrary_selection(base,seed,force=()):
    R,C,_,edges=base;P={v for e in edges for v in e};T=set();N=neighbourhoods(R,C)
    rng=random.Random(seed);order=list(N);rng.shuffle(order);order=list(force)+order
    for v in order:
        if v in P|T:continue
        if len(N[v]&(P|T))>1 or any(len(N[u]&(P|T))>=1 for u in N[v]&T):continue
        if v not in force and rng.random()<.25:continue
        T.add(v)
    assert set(force)<=T
    return R,C,T,edges


def endpoint_hull(cur):
    R,C,T,edges=cur;P={v for e in edges for v in e};N=neighbourhoods(R,C)
    return {v for v in N if v not in T|P and
            all(not N[t]&(T|P) for t in N[v]&T)}


def hull_formula(w,q):
    Q={(4,10*i+9) for i in range(q)}
    if w>=10:Q.add((4,1))
    for r in range(6,w-3,2):
        Q|={(r,10*i+c) for i in range(q) for c in (9,11)}
        if r<w-4:Q.add((r,1))
    for r in range(5,w-2,2):
        Q|={(r,10*i) for i in range(1,q+1)}
        if r<=w-7:Q.add((r,0))
    Q|={(w-2,10*i+11) for i in range(q)}
    Q|={(w-1,10*i+9) for i in range(q)}|{(w-1,10*i+3) for i in range(1,q)}
    return Q


def extendable(P,extra):
    """Independent bipartite augmenting-matching check, only small controls."""
    vertices=P|set(extra);left={v for v in vertices if sum(v)%2==0}
    if len(left)*2!=len(vertices):return False
    N={v:{u for u in vertices if sum(abs(x-y) for x,y in zip(v,u))==1} for v in left}
    mates={}
    def augment(v,seen):
        for u in N[v]-seen:
            seen.add(u)
            if u not in mates or augment(mates[u],seen):mates[u]=v;return True
        return False
    return all(augment(v,set()) for v in sorted(left))


def verify_direction(w,q,cur,totals,all_pools=False):
    direct_check(*cur);vertical=transpose(cur);data,meta=compile_even_width(vertical)
    kinds,pairs,links,S,Q=data;owner,A,B,M=owner_data(kinds,pairs)
    expected=[]
    for i in range(q):
        expected.append(frozenset(((10*i+3,1),(10*i+3,w))))
        expected.extend(frozenset(((10*i+6,r),(10*i+6,r+1))) for r in range(2,w-3,2))
        expected.append(frozenset(((10*i+6,w-2),(10*i+8,w-1))))
    assert {frozenset(e) for e in pairs}==set(expected) and len(pairs)==q*w//2
    expectedA={owner[(10*i+3,1)] for i in range(q)
               if (1,10*i+2) in cur[2] and (w,10*i+2) in cur[2]}
    assert A==expectedA
    reserves={}
    for a in A:
        tip=next(v for v in pairs[a] if v[1]==1);i=(tip[0]-3)//10
        upper,lower=(5*i+1,2,2),(5*i+1,w-1,w-1)
        assert {upper,lower}<=S[a]
        assert not any(owner[x]==a for x,y in links)
        assert all(not S[a]&S[o] for o in S if o!=a)
        reserves[a]=(upper,lower)
    assert len({j for values in reserves.values() for j in values})==2*len(A)
    flow=fork_flow(*data);assert (flow['value'],flow['cost'],flow['deficit'])==(len(A),0,0)
    pools=[set(),Q,Q-{v[0] for v in reserves.values()},Q-{v[1] for v in reserves.values()}]
    pools+=[Q-S[a] for a in sorted(A)]
    rng=random.Random(w*100+q+len(cur[2]));pools+=[{j for j in sorted(Q) if rng.random()<.5} for _ in range(3)]
    if all_pools:
        assert len(Q)<=6
        pools=[{j for b,j in zip(bits,sorted(Q)) if b} for bits in itertools.product((0,1),repeat=len(Q))]
    for F in pools:
        restricted=(kinds,pairs,links,{o:s&F for o,s in S.items()},F)
        expected_value=sum(bool(S[a]&F) for a in A)
        guarded={j for js in reserves.values() for j in js}
        assert 2*(len(A)-expected_value)<=len(guarded-F)
        result=fork_flow(*restricted)
        assert (result['value'],result['cost'])==(expected_value,0)
        independent=optimize(*restricted)
        assert (independent['value'],independent['cost'])==(expected_value,0)
        totals['available_pool_flow_and_independent_pack_comparisons']+=1
    totals['arbitrary_T_direction_boards']+=1;totals['forced_distinct_reserve_pairs']+=len(A)
    totals['balanced_boundary_chains_observed']+=len(meta['balanced_chains'])
    return data,meta,reserves


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();records=[];fixture=None
    for w,q in itertools.product((8,10,12,20,40,64),(1,2,3,7)):
        cur=configuration(w,q);data,meta,reserves=verify_direction(w,q,cur,totals,all_pools=q<=3)
        _,A,B,M=owner_data(*data[:2]);assert (len(A),len(B),len(M),meta['raw'])==(q,q,q*(w//2-2),2*q)
        N=neighbourhoods(*cur[:2]);P={v for e in cur[3] for v in e};Q=endpoint_hull(cur)
        assert Q==hull_formula(w,q)
        attached={(w-1,10*i+9) for i in range(q)}|{(w-1,10*i+3) for i in range(1,q)}
        assert {v for v in Q if N[v]&P}==attached
        assert all(sum(v)%2==0 for v in attached)
        assert all(not N[v]&(P|Q) for v in Q-attached)
        assert sum(sum(v)%2==0 for v in P)*2==len(P)
        totals['attaining_board_exact_endpoint_hulls']+=1;totals['isolated_new_endpoint_candidates']+=len(Q-attached)
        if w==8 and q<=2:
            ordered=sorted(Q)
            for bits in itertools.product((0,1),repeat=len(ordered)):
                extra={v for v,b in zip(ordered,bits) if b}
                assert extendable(P,extra)==(not extra)
                totals['independent_endpoint_extension_matching_controls']+=1
        if w<=20 and q<=3:
            for seed in range(24):
                forced=[(r,10*i+2) for i in range(q) for r in (1,w)] if seed%2 else []
                other=arbitrary_selection(cur,seed,forced)
                verify_direction(w,q,other,totals)
        record=dict(w=w,q=q,vertical_alpha=q,vertical_beta=q,vertical_mixed=q*(w//2-2),
                    vertical_raw=2*q,payment=q,cost=0,slack=2*q,endpoint_hull_size=len(Q),
                    attachable_candidate_count=len(attached),isolated_candidates=len(Q-attached))
        records.append(record)
        if (w,q)==(8,1):
            _,layers=uniform_freezing(w,q,cur)
            trans_layers=[[(c,r) for r,c in layer] for layer in layers]
            witnesses=check_rank_certificate(transpose(cur),trans_layers)
            fixture=dict(**record,original_shape=cur[:2],original_T=sorted(cur[2]),original_M=cur[3],
                transposed_T=sorted(transpose(cur)[2]),transposed_M=transpose(cur)[3],
                strict_freezing_witnesses=witnesses,endpoint_hull=sorted(Q),
                attachable_candidates=sorted(attached),vertical_labels=meta['labels'],
                strand_pairs=data[1],reserves=[dict(owner=a,units=js) for a,js in reserves.items()])
    (Path(__file__).parent/'fixtures/perpendicular_guarded_reserves_and_joint_maximality.json').write_text(json.dumps(fixture,indent=2)+'\n')
    report=dict(status='PASS',totals=dict(totals),records=records,
        scope='Written all-W/q theorem for EVERY feasible T with module P: vertical alphas have two private forced singleton reserves; all-pool value equals number of alphas with surviving support, cost0. For displayed fixed-P selection maxima, no monotone endpoint enlargement exists even with arbitrary rematching, by complete candidate hull isolation and bipartite balance.',
        limits=['No change of band phase or boundary crop is silently included.',
                'Joint maximality is inclusion maximality, not a global maximum over replacements of T/P.',
                'General grid coefficient-one or improved5over6 bound remains open.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
