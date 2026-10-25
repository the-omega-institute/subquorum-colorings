"""Guarded direction switches, dual source rank, and frozen shared-seam stacks.

General proofs: docs/GUARDED_STRIP_SWITCHES_AND_DUAL_REPAIR.md.
Finite enumeration corroborates, and is not the general proof.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_forced_mates_and_adjacent_maxima import configuration,uniform_freezing
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_crossing_matching_ports import rectangle,compile_partition,strand_parts
from check_frozen_beta_support_fork import restrict
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical
from check_interface_reserve_reoptimization import subsets,constrained_primitive
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def source_restrict(data,S):
    _,A,_,_=owner_data(*data[:2]);assert S<=A
    return restrict(data,set(range(len(data[1])))-(A-S),data[4])


def private_payments(data,F):
    kinds,pairs,links,support,Q=data;W={o:set(js) for o,js in support.items()};Q=set(Q)
    for a in F:
        j=(-1,a,0) if not Q or isinstance(next(iter(Q)),tuple) else -a-1
        assert j not in Q;Q.add(j);W[a].add(j)
    return kinds,pairs,links,W,Q


def dual_check(data,totals,independent=False):
    _,A,_,_=owner_data(*data[:2]);A=set(A)
    profiles={frozenset(S):fork_flow(*source_restrict(data,S)) for S in subsets(A)}
    rank={S:f['value'] for S,f in profiles.items()}
    p=rank[frozenset(A)];gain={}
    old_bases=[set(S) for S,r in rank.items() if len(S)==r==p]
    for F in subsets(A):
        key=frozenset(F);predicted=len(F)+rank[frozenset(A-F)]
        result=fork_flow(*private_payments(data,F));actual=result['value'];assert actual==predicted
        assert result['cost']==profiles[frozenset(A-F)]['cost']
        totals['exact_complement_min_link_profiles']+=1
        gain[key]=actual-p;assert 0<=gain[key]<=len(F)
        assert (actual==len(A))==(rank[frozenset(A-F)]==len(A-F))
        totals['private_flip_complement_rank_profiles']+=1
        if independent:
            new=private_payments(data,F)
            assert constrained_primitive(new,set())[0]==actual
            totals['independent_primitive_values']+=1
            for B in old_bases:
                assert constrained_primitive(new,B)[0]==actual
                totals['independent_protected_old_bases']+=1
    for F,G in itertools.product(gain,repeat=2):
        assert gain[F]+gain[G]>=gain[F|G]+gain[F&G]
        totals['dual_submodular_pairs']+=1
    # Weighted independent greedy is compared with all minimum-cardinality
    # eligible repairs; links are not a greedy secondary objective.
    for E in [A,{a for i,a in enumerate(sorted(A)) if i%2==0}]:
        target=gain[frozenset(E)];weights={a:(a*7+3)%11 for a in E};chosen=set()
        for a in sorted(E,key=lambda a:(weights[a],a)):
            if gain[frozenset(chosen|{a})]>gain[frozenset(chosen)]:chosen.add(a)
        feasible=[F for F in subsets(E) if gain[frozenset(F)]==target]
        assert len(chosen)==target==min(map(len,feasible))
        assert sum(weights[a] for a in chosen)==min(sum(weights[a] for a in F) for F in feasible if len(F)==target)
        for b in range(len(E)+1):
            assert max(gain[frozenset(F)] for F in subsets(E) if len(F)<=b)==min(b,target)
            totals['exact_flip_budget_controls']+=1
        totals['weighted_greedy_controls']+=1
    totals['abstract_models']+=1
    return rank,gain


def reduced_seed_schedule(w):
    base=configuration(w,1);_,old=uniform_freezing(w,1,base)
    postponed={(r,5) for r in range(1,w,2)}|{(r,6) for r in range(2,w+1,2)}
    postponed|={(w-1,7),(w,8)}|{(r,4) for r in range(2,w+1,2)}
    first=[layer for layer in old if layer[0] not in postponed]
    tail=[[(1,5)]]
    for r in range(2,w+1,2):
        tail.append([(r,6)])
        if r<w:tail.append([(r+1,5)])
    tail += [[(w-1,7)],[(w,8)]]+ [[(r,4)] for r in range(2,w+1,2)]
    reduced=(*base[:2],base[2]-{(0,5)},base[3])
    check_rank_certificate(reduced,first+tail)
    return first+tail


def stack(w,q,opened,flips):
    assert w>=8 and w%2==0 and q>=1 and opened<=set(range(q-1)) and flips<=set(range(q))
    h=w+2;R=q*(w+4)-2;T=set();M=[];layers=[];seed=reduced_seed_schedule(w)
    for a in range(q):
        off=a*(w+4);base=configuration(w,1)
        T|={(off+r,c) for r,c in base[2]}
        M += [tuple((off+r,c) for r,c in e) for e in base[3]]
        layers += [[(off+r,c) for r,c in layer] for layer in seed]
        if a and a-1 in opened:T.remove((off,5))
        if a<q-1:
            T|=({(off+h+1,4),(off+h+1,5)} if a in opened else {(off+h,4),(off+h+1,4)})
    cur=(R,12,T,M);regions=[rectangle(0,R,0,2,True)]
    for a in range(q):
        off=a*(w+4);regions.append(rectangle(off,off+h,2,4,a in flips))
        if a<q-1:regions.append(rectangle(off+h,off+h+2,2,4,True))
    regions += [rectangle(0,R,4,10,True),rectangle(0,R,10,12,True)]
    return cur,regions,layers


def components(q,opened):
    out=[];current={0}
    for a in range(q-1):
        if a in opened:current.add(a+1)
        else:out.append(current);current={a+1}
    return out+[current]


def physical(w,q,opened,flips,totals,independent=False,save=False):
    cur,regions,layers=stack(w,q,opened,flips);direct_check(*cur)
    witnesses=check_rank_certificate(cur,layers);P={v for e in cur[3] for v in e}
    assert frozen_certificate(cur)[0]==P
    rec,data=compile_partition(cur,regions);own,A,B,X=owner_data(*data[:2]);roots=[]
    assert (len(A),len(B),len(X))==(q,q,q*(w//2-2))
    assert len(cur[2])==q*(9*w//2+5)+2*(q-1)-len(opened)
    assert rec['slack']==rec['raw']==12*q-10+len(opened)
    assert len(rec['crossing_edges'])==2*q
    comp=components(q,opened);hit=sum(bool(C&flips) for C in comp)
    assert (rec['value'],rec['deficit'],rec['cost'])==(len(opened)+hit,q-len(opened)-hit,0)
    # IDs use physical band geometry, not the incidental index that shifts
    # when an earlier strip changes from horizontal to vertical.
    band_keys=[tuple(cols) for region in regions for cols in region['bands']]
    geometric_id=lambda j:(band_keys[j[0]],j[1],j[2])
    _,old_regions,_=stack(w,q,opened,set());oldrec,olddata=compile_partition(cur,old_regions)
    old_keys=[tuple(cols) for region in old_regions for cols in region['bands']]
    old_id=lambda j:(old_keys[j[0]],j[1],j[2])
    assert data[:3]==olddata[:3]
    bands=[cols for region in regions for cols in region['bands']]
    old_bands=[cols for region in old_regions for cols in region['bands']]
    describe=lambda parts:{(frozenset(x['body']),tuple(x['ends'])) for x in parts}
    assert describe(strand_parts(P,cur[2],cur[3],bands)[0])==describe(strand_parts(P,cur[2],cur[3],old_bands)[0])
    for a in range(q):
        off=a*(w+4);root=own[(off+1,3)];roots.append(root)
        strip={(off+r,c) for r in range(w+2) for c in (2,3)}
        assert P&strip=={(off+1,3),(off+w,3)}
        assert {(off,3),(off+w+1,3),(off+1,2),(off+w,2)}<=cur[2]
        assert all((off+r,4) in P for r in range(2,w))
        assert root in A and set(data[1][root])=={(off+1,3),(off+w,3)}
        assert not any(own[u]==root for u,v in data[2])
        oldW={old_id(j) for j in olddata[3][root]};newW={geometric_id(j) for j in data[3][root]}
        assert oldW<=newW
        new_only=newW-oldW
        if a in flips:
            assert len(new_only)>=2
            for j in data[3][root]:
                if geometric_id(j) in new_only:assert {o for o,js in data[3].items() if j in js}=={root}
        else:assert not new_only
    for o in set(range(len(data[1])))-A:
        assert {geometric_id(j) for j in data[3][o]}=={old_id(j) for j in olddata[3][o]}
    assert set(roots)==A
    # Source supports in the original partition are EXACTLY path-edge units.
    for a,root in enumerate(roots):
        expected={j for j in olddata[4] if j[1] in {i*(w+4)+w+2 for i in opened&{a-1,a}} and old_keys[j[0]][0][0][1]==4}
        assert olddata[3][root]==expected
    if independent:
        assert constrained_primitive(data,set())==(rec['value'],0)
        totals['physical_independent_primitive_values']+=1
    if save:
        fixture=dict(W=w,q=q,opened=sorted(opened),flips=sorted(flips),shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],
            freezing_layers=layers,freezing_witnesses=witnesses,regions=[dict(bounds=r['bounds'],vertical=r['vertical']) for r in regions],
            roots=roots,pairs=data[1],links=data[2],supports=[(o,sorted(js)) for o,js in data[3].items()],resources=sorted(data[4]),
            value=rec['value'],deficit=rec['deficit'],slack=rec['slack'],cost=rec['cost'])
        (Path(__file__).parent/'fixtures/guarded_strip_shared_seam.json').write_text(json.dumps(fixture,indent=2)+'\n')
    totals['physical_partition_models']+=1;totals['strict_freezing_events']+=len(witnesses)
    return dict(W=w,q=q,opened=sorted(opened),flips=sorted(flips),value=rec['value'],deficit=rec['deficit'],slack=rec['slack'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();totals=Counter();records=[]
    rng=random.Random(20261025)
    # Real BP-entry bottlenecks and beta bodies remain in the source rank.
    for types in ('AA','AAA','AAB','AAAB','AAM','AAAMB','AAABMM','AAAABB'):
        for i in range(8):
            kinds,pairs,possible=canonical(types);rng.shuffle(possible);links=possible[:rng.randrange(min(9,len(possible))+1)]
            Q=set(range(rng.randrange(4)));W={o:{j for j in Q if rng.randrange(2)} for o in range(len(pairs))}
            dual_check((kinds,pairs,links,W,Q),totals,independent=i<3)
    for w in (8,10):
        for q in range(1,6):
            for E in subsets(range(q-1)):
                for F in subsets(range(q)):
                    records.append(physical(w,q,E,F,totals,independent=q<=3,save=(w,q,E,F)==(8,2,{0},set())))
    for w,q in itertools.product((12,20,40,64),(1,3,8,16)):
        for E in (set(),set(range(q-1)),set(range(0,q-1,2))):
            for F in (set(),{0},set(range(q))):
                records.append(physical(w,q,E,F,totals))
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,
        scope='General guarded-strip geometry and dual source-rank repair proved in note; frozen path-component family has exact whole-pool support and one flip per component, no point loss.',
        limits=['Finite controls corroborate written general proofs.','Source matroid duality and physical geometry are written; Lean scope separately recorded.','No universal 5/6 improvement; not all direction switches satisfy guarded hypotheses.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
