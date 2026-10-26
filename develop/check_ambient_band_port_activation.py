"""Solver-free checks of the all-length ambient activation construction.

The coordinate proof, rank table, interface traps and arbitrary-stack argument
are in docs/AMBIENT_BAND_PORT_ACTIVATION.md. Enumeration checks that proof's
adapter; it does not prove the unbounded statement.
"""
if not __debug__:
    raise RuntimeError('Assertions required; do not run with -O.')

import argparse
from collections import Counter, deque
from itertools import product
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import edge_key, endpoints
from check_frozen_half_area_attainers import frozen_family, certificate
from check_frozen_equality_matching_rigidity import first_times
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed


CAP_T = {(0,1),(0,3),(0,5),(1,0),(1,4),(2,5),(3,5),
         (4,4),(5,1),(5,3),(5,5)}
CAP_M = [((1,1),(2,1)),((1,3),(1,2)),((2,2),(3,2)),
         ((2,3),(3,3)),((3,0),(3,1)),((4,0),(4,1)),((4,2),(4,3))]
CAP_NAMES = dict(C0=(1,1),D=(2,1),A=(1,3),B=(1,2),E=(2,2),F=(3,2),
                 U=(2,3),V=(3,3),p=(3,0),a=(3,1),q=(4,0),b=(4,1),
                 L=(4,2),Z=(4,3))


def mate_map(M):
    return {v:u for e in M for v,u in (e,e[::-1])}


def band(m, flip):
    h,w,T,M = frozen_family(m)
    c = w-1
    removed = {edge_key(e) for e in [((3,c-2),(3,c-1)),((4,c-2),(4,c-1))]}
    if flip:
        M = [e for e in M if edge_key(e) not in removed]
        M += [((3,c-2),(4,c-2)),((3,c-1),(4,c-1))]
    return h,w,set(T),list(M)


def ambient(m, flip):
    h,w,T,M = band(m,flip)
    shift = lambda v:(v[0],v[1]+w)
    return h,w+6,T|{shift(v) for v in CAP_T},M+[(shift(a),shift(b)) for a,b in CAP_M]


def rank_certificate(m, flip):
    c=6*m+9; n=3*m+2
    cap=lambda v:(v[0],v[1]+c+1)
    names={k:cap(v) for k,v in CAP_NAMES.items()}
    rec=[]
    for v,r,a,b in certificate(m):
        if v==(4,c): a,b=(5,c),names['q']
        elif v==(3,c): a,b=(2,c),names['p']
        elif flip and v==(4,c-1): a,b=(4,c-2),(4,c)
        elif flip and v==(3,c-1): a,b=(3,c-2),(3,c)
        rec.append((v,r,a,b))
    table=[('C0',0,(0,1),(1,0)),('A',0,(0,3),(1,4)),
           ('Z',0,(4,4),(5,3)),('E',1,'B','D'),('b',1,(5,1),'L'),
           ('a',2,'D','F'),('q',4,'p',('inside',4,c)),
           ('L',5,'F','b'),('V',6,'F','Z'),
           ('p',n+1,'q',('inside',3,c)),('F',n+2,'a','L'),
           ('D',n+3,'a','E'),('B',n+4,'C0','E'),('U',n+5,'A','E')]
    def site(s):
        if isinstance(s,str): return names[s]
        if len(s)==3: return s[1:]
        return cap(s)
    return rec+[(names[v],r,site(a),site(b)) for v,r,a,b in table]


def check_ranks(cur,rec,counts):
    T,M=cur[2:]; mate=mate_map(M); ranks={v:r for v,r,a,b in rec}
    assert len(rec)==len(ranks)==len(mate) and set(ranks)==set(mate)
    for v,r,a,b in rec:
        assert r>=0 and a!=b and mate[v] not in (a,b)
        assert all(u in neighbors(v) for u in (a,b))
        assert all(u in T or u in mate and ranks[mate[u]]<r for u in (a,b))
        counts['strict_actual_mate_rank_events']+=1
    return ranks


def local_closure(T,M,granted=frozenset()):
    """Independent synchronous local response with explicitly kept outside sites."""
    mate=mate_map(M); frozen=set(); rounds=0
    assert set(granted).isdisjoint(T|set(mate))
    while True:
        kept=T|set(granted)|{mate[v] for v in frozen}
        new={v for v in mate.keys()-frozen if len(set(neighbors(v))&kept)>=2}
        if not new: return frozen,rounds
        frozen|=new; rounds+=1


def check_trap(T,M,S,granted=frozenset()):
    mate=mate_map(M); assert S and S<=set(mate)
    possible=T|set(granted)|{v for v in mate if mate[v] not in S}
    supports={v:sorted(set(neighbors(v))&possible) for v in S}
    assert all(len(xs)<=1 for xs in supports.values()),supports
    return supports


def interface_checks(m,counts):
    c=6*m+9; old=band(m,True); T,M=old[2:]; P=endpoints(M)
    cap=lambda v:(v[0],v[1]+c+1)
    ct={cap(v) for v in CAP_T}; cm=[(cap(a),cap(b)) for a,b in CAP_M]
    names={k:cap(v) for k,v in CAP_NAMES.items()}
    white={(3,c-1),(4,c)}; black={(3,c),(4,c-1)}
    early={names[k] for k in ['C0','A','Z','E','b','a']}
    wc={names[k] for k in ['p','F','D','B','U']}
    bc={names[k] for k in ['q','L','V']}
    for a,b in product([False,True],repeat=2):
        grants=({names['p']} if a else set())|({names['q']} if b else set())
        expected=(P-(white|black))|(black if a else set())|(white if b else set())
        actual,_=local_closure(T,M,grants)
        assert actual==expected,(m,a,b,actual^expected)
        if not a: check_trap(T,M,black,grants)
        if not b: check_trap(T,M,white,grants)
        counts['exact_band_interface_responses']+=1
    for g,Q in product([False,True],repeat=2):
        grants=({(4,c)} if g else set())|({(3,c)} if Q else set())
        expected=early|(wc if Q else set())|(bc if g else set())
        actual,_=local_closure(ct,cm,grants)
        assert actual==expected,(m,g,Q,actual^expected)
        if not Q: check_trap(ct,cm,wc,grants)
        if not g: check_trap(ct,cm,bc,grants)
        counts['exact_cap_interface_responses']+=1
    assert local_closure(CAP_T,CAP_M)[0]=={CAP_NAMES[k] for k in ['C0','A','Z','E','b','a']}


def tokens(cur):
    h,w,T,M=cur; P=endpoints(M); plus=set(); minus=set(); matrix={}
    assert h%2==w%2==0
    for r in range(0,h,2):
        for c in range(0,w,2):
            tile={(r+i,c+j) for i,j in product([0,1],repeat=2)}
            charge=4-2*len(T&tile)-len(P&tile); matrix[r,c]=charge
            plus.update(((r,c),i) for i in range(max(charge,0)))
            minus.update(((r,c),i) for i in range(max(-charge,0)))
    assert len(plus)-len(minus)==h*w-2*(len(T)+len(M))
    return plus,minus,matrix


def payments(m,row=0):
    w=6*m+10
    pairs=[(((0,0),0),((0,4),0)),(((2,4),0),((2,0),0)),
           (((2,4),1),((4,4),0))]
    pairs += [(((2,4+6*j),0),((0,4+6*j),0)) for j in range(1,m+1)]
    pairs += [(((2,w),0),((0,w),0))]
    shift=lambda x:((x[0][0]+row,x[0][1]),x[1])
    return [(shift(a),shift(b)) for a,b in pairs]


def check_ledger(cur,pairs,expected,counts):
    plus,minus,matrix=tokens(cur)
    assert len(pairs)==len(plus)==len(minus)==expected
    sources=[a for a,b in pairs]; targets=[b for a,b in pairs]
    assert len(set(sources))==len(sources) and len(set(targets))==len(targets)
    assert set(sources)==plus and set(targets)==minus
    counts['literal_nonreuse_token_bijections']+=1
    return matrix


def stack(m,profile):
    q=len(profile); assert q>=1
    W=6*m+16; T=set(); M=[]; rec=[]
    for i,flip in enumerate(profile):
        cur=ambient(m,flip); shift=lambda v:(v[0]+8*i,v[1])
        T|={shift(v) for v in cur[2]}
        M += [(shift(a),shift(b)) for a,b in cur[3]]
        rec += [(shift(v),r,shift(a),shift(b)) for v,r,a,b in rank_certificate(m,flip)]
        if i+1<q: T|={(8*i+r,c) for r in (6,7) for c in range(0,W,2)}
    return (8*q-2,W,T,M),rec


def one_length(m,counts):
    originals=frozen_family(m); c=6*m+9; records=[]
    for flip in [False,True]:
        cur=ambient(m,flip); h,w,T,M=cur; P=endpoints(M)
        assert direct_check(*cur)==18*m+48==h*w//2
        assert len(T)==9*m+32 and len(M)==9*m+16
        assert {v for v in T if v[1]<=c}==originals[2]
        assert {v for v in P if v[1]<=c}==endpoints(originals[3])
        assert all((a[1]<=c)==(b[1]<=c) for a,b in M)
        cross={edge_key((v,u)) for v in T|P if v[1]==c
               for u in neighbors(v) if u[1]==c+1 and u in T|P}
        assert cross=={edge_key(((r,c),(r,c+1))) for r in (3,4)}
        actual=set(map(edge_key,M)); prescribed=set(map(edge_key,originals[3]))
        assert len(prescribed-actual)==2*int(flip)
        ranks=check_ranks(cur,rank_certificate(m,flip),counts)
        times=first_times(cur)
        assert set(times)==P and max(times.values())<=9*m+8
        assert max(ranks.values())==9*m+7
        # Independent synchronous replay cross-checks the queue and rank adapter.
        frozen,layers=frozen_certificate(cur)
        assert frozen==P and len(layers)==max(times.values())
        mat=check_ledger(cur,payments(m),m+4,counts)
        capmat=[[mat[r,k] for k in range(c+1,c+7,2)] for r in (0,2,4)]
        assert capmat==[[-1,0,0],[1,0,0],[0,0,0]]
        local=band(m,flip); locfrozen,_=local_closure(*local[2:])
        missing=endpoints(local[3])-locfrozen
        assert missing==({(3,c-1),(3,c),(4,c-1),(4,c)} if flip else set())
        counts['fully_frozen_half_area_boards']+=1
        counts['queue_synchronous_crosschecks']+=1
        records.append(dict(m=m,flip=flip,shape=[h,w],selected=len(T),matching=len(M),
                            objective=len(T)+len(M),missing_prescribed_edges=2*int(flip),
                            local_unfrozen_endpoints=len(missing),cap_unfrozen_endpoints=8,
                            observed_synchronous_rounds=len(layers),max_rank=max(ranks.values()),
                            positive_tokens=m+4,negative_demands=m+4,reserve=0))
    interface_checks(m,counts)
    return records


def stack_checks(counts):
    for m in [2,3,5]:
        for q in range(1,6):
            matchings=set();fixed=None
            for profile in product([False,True],repeat=q):
                cur,rec=stack(m,profile);h,w,T,M=cur;P=endpoints(M)
                assert direct_check(*cur)==(4*q-1)*w==h*w//2
                assert len(T)==q*(9*m+32)+(q-1)*w and len(M)==q*(9*m+16)
                assert fixed in (None,(T,P)); fixed=(T,P)
                matching=frozenset(map(edge_key,M));assert matching not in matchings;matchings.add(matching)
                canonical,_=stack(m,[False]*q)
                assert len(set(map(edge_key,canonical[3]))-matching)==2*sum(profile)
                check_ranks(cur,rec,counts);assert set(first_times(cur))==P
                mat=check_ledger(cur,[p for i in range(q) for p in payments(m,8*i)],q*(m+4),counts)
                assert all(mat[8*i+6,c]==0 for i in range(q-1) for c in range(0,w,2))
                counts['exhaustive_stack_matching_profiles']+=1
            assert len(matchings)==2**q
            counts['fixed_occupation_distinct_matching_families']+=1
    for m,q in [(2,32),(12,7),(100,3)]:
        profile=[bool(i%2) for i in range(q)]
        cur,rec=stack(m,profile);assert direct_check(*cur)==cur[0]*cur[1]//2
        check_ranks(cur,rec,counts);assert set(first_times(cur))==endpoints(cur[3])
        check_ledger(cur,[p for i in range(q) for p in payments(m,8*i)],q*(m+4),counts)
        counts['larger_stack_controls']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--max-m',type=int,default=24)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();records=[]
    lengths=sorted(set(range(2,args.max_m+1))|{40,64,100})
    for m in lengths: records+=one_length(m,counts)
    stack_checks(counts)
    for m in [2,5]:
        for flip in [False,True]:
            cur=ambient(m,flip);h,w=cur[:2]
            for tr,fi,fj in product([False,True],repeat=3):
                shape,T,M=transformed(*cur,tr,fi,fj)
                def f(v):
                    r,c=v;r=h-1-r if fi else r;c=w-1-c if fj else c
                    return (c,r) if tr else (r,c)
                rec=[(f(v),r,f(a),f(b)) for v,r,a,b in rank_certificate(m,flip)]
                new=(*shape,T,M);assert direct_check(*new)==shape[0]*shape[1]//2
                check_ranks(new,rec,counts);assert set(first_times(new))==endpoints(M)
                counts['isometry_controls']+=1
    report=dict(status='PASS',theorem='For every m>=2 a six-column zero-charge cap activates the flipped half-area band; arbitrary q stacks have at least 2^q frozen actual matchings on identical occupation with zero reserve.',
                obstruction='Global freezing and region-closed matching do not imply local freezing or the isolated-band binary reserve. The isolated theorem and global half-area target are not refuted.',
                proof='Written all-length coordinate construction, strict actual-mate ranks, exact interface traps and arbitrary-q disjoint physical token bijection; finite checks only validate adapters.',
                lengths=lengths,counts=dict(counts),records=records)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k!='records'}))


if __name__=='__main__': main()
