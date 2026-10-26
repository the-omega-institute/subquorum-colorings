"""Solver-free checks of the all-length proof in NEUTRAL_OCCUPIED_ENVELOPE_EXPANSION.

The written rank formulas prove the theorem for arbitrary m and S. This program
checks their literal coordinate adapters, independent closure implementations,
and physical token identities; enumeration is a control, not the proof.
"""
if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import endpoints, edge_key
from check_frozen_half_area_attainers import frozen_family
from check_frozen_equality_matching_rigidity import first_times
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check


def core(j):
    t = 6*j
    return [(r, c+t) for r, c in
            [(1,5),(1,6),(1,7),(2,7),(2,6),(3,6),(3,7),(3,8),(2,5),(3,5)]]


def envelope(j):
    t = 6*j
    # a,b,f are converted selections; d,e,w were empty black sites.
    return [(r,c+t) for r,c in [(1,8),(1,10),(2,9),(2,8),(2,10),(1,9)]]


def expanded(m, S):
    assert m >= 2 and set(S) <= set(range(m))
    h,w,T,M = frozen_family(m)
    T = set(T); M = list(M)
    for j in sorted(S):
        _,_,C,D,*_ = core(j)
        a,b,f,d,e,v = envelope(j)
        T -= {a,b,f}
        M.remove(next(edge for edge in M if set(edge) == {C,D}))
        M.extend([(C,a),(D,d),(v,b),(f,e)])
    return h,w,T,M


def rank_table(m, S):
    n = 3*m+2; c = 6*m+9; rec = []
    def add(v,r,a,b): rec.append((v,r,a,b))
    def Z(l): return 4,5+2*l
    def K(l): return 4,6+2*l
    add((1,1),0,(0,1),(1,2)); add((2,1),0,(2,0),(3,1))
    for l in range(n):
        add(Z(l),l,(5,5+2*l),(4,4) if l==0 else K(l-1))
    add((4,c),n,(5,c),K(n-1))
    for j in range(m+1):
        A,B,C,D,E,F,G,H,U,V = core(j)
        a,b,f,d,e,v = envelope(j)
        g = 3,9+6*j
        r = n+1+9*(m-j)
        add(H,r,g,K(3*j+1)); add(F,r+1,G,K(3*j))
        add(D,r+2,E,G)
        if j in S:
            add(f,r+3,g,d); add(b,r+4,core(j+1)[0],e)
            add(a,r+5,d,v)
        add(B,r+6,C,E); add(U,r+7,A,E)
        if j: add((3,4+6*j),r+8,V,K(3*j-1))
        add(A,3*j,(0,5+6*j),(1,4+6*j))
        add(C,3*j+1,(0,7+6*j),B)
        if j in S: add(v,3*j+2,(0,9+6*j),a)
        t = 3*m+2+10*(m-j)
        if j in S:
            add(e,t,b,core(j+1)[8]); add(d,t+1,a,f)
        add(E,t+2,B,D); add(G,t+3,D,F)
        add(g,t+4,(2,9+6*j),H)
        if j<m: add(K(3*j+2),t+5,(3,10+6*j),Z(3*j+3))
        add(K(3*j+1),t+6,H,Z(3*j+2) if j<m else (4,c))
        add(K(3*j),t+7,F,Z(3*j+1)); add(V,t+8,F,Z(3*j))
    return rec


def token_sets(cur):
    h,w,T,M = cur; P = endpoints(M); charges = {}; plus=set(); minus=set()
    for r in range(0,h,2):
        for c in range(0,w,2):
            tile={(r+i,c+j) for i in (0,1) for j in (0,1)}
            q=4-2*len(T&tile)-len(P&tile); charges[r,c]=q
            plus.update((((r,c),i) for i in range(max(q,0))))
            minus.update((((r,c),i) for i in range(max(-q,0))))
    return charges,plus,minus


def payment(m, S, cur, counts):
    oldq,oldp,oldn=token_sets(frozen_family(m))
    q,p,n=token_sets(cur)
    expected=dict(oldq)
    for j in S:
        assert oldq[0,10+6*j]==-1 and oldq[2,10+6*j]==1
        expected[0,10+6*j]=expected[2,10+6*j]=0
    assert q==expected
    oldpay=[(((0,0),0),((0,4),0)),(((2,4),0),((2,0),0)),
            (((2,4),1),((4,4),0))]
    oldpay += [(((2,4+6*k),0),((0,4+6*k),0)) for k in range(1,m+1)]
    removed={(((2,10+6*j),0),((0,10+6*j),0)) for j in S}
    pay=[edge for edge in oldpay if edge not in removed]
    assert {x for x,_ in oldpay}==oldp and {y for _,y in oldpay}==oldn
    assert len(pay)==len(p)==len(n)==m+3-len(S)
    assert {x for x,_ in pay}==p and {y for _,y in pay}==n
    assert oldp-p=={x for x,_ in removed} and oldn-n=={y for _,y in removed}
    assert {((2,4),0),((2,4),1)}<=p
    counts['surviving_physical_payments']+=len(pay)
    counts['literal_cancellations']+=len(S)


def check_board(m,S,counts):
    cur=expanded(m,S); h,w,T,M=cur; P=endpoints(M); s=len(S)
    assert direct_check(*cur)==h*w//2==18*m+30
    assert len(T)==9*m+21-3*s and len(M)==9*m+9+3*s
    original=frozen_family(m); oldP=endpoints(original[3])
    added=set().union(*(set(envelope(j)) for j in S))
    assert P-oldP==added
    assert oldP<=P and len(P)==18*m+18+6*s
    assert len({edge_key(e) for e in M}&{edge_key(e) for e in original[3]})==len(original[3])-s
    rec=rank_table(m,S); rank={v:r for v,r,a,b in rec}
    mate={v:u for edge in M for v,u in (edge,edge[::-1])}
    assert len(rec)==len(rank)==len(P) and set(rank)==P
    for v,r,a,b in rec:
        assert r>=0 and a!=b and mate[v] not in (a,b)
        assert a in neighbors(v) and b in neighbors(v)
        for u in (a,b):
            assert u in T or u in P and rank[mate[u]]<r,(m,S,v,r,u)
            if u in P: assert sum(v)%2==sum(mate[u])%2
    assert max(rank.values())<=13*m+10
    times=first_times(cur); assert set(times)==P and max(times.values())<=13*m+11
    # Synchronous replay is intentionally independent of the event queue.
    frozen,layers=frozen_certificate(cur); assert frozen==P
    replay={tuple(item['endpoint']):i+1 for i,layer in enumerate(layers) for item in layer}
    assert replay==times
    payment(m,S,cur,counts)
    counts['boards']+=1; counts['strict_actual_mate_rank_events']+=len(rec)
    return len(layers)


def restricted_controls(counts):
    for m in range(2,5):
        old=frozen_family(m); oldT=old[2]; oldP=endpoints(old[3])
        for bits in itertools.product((0,1,2,3),repeat=m):
            X=set(); guards=set(); private=set(); common=set()
            for j,bitsj in enumerate(bits):
                a,b,f,d,e,_=envelope(j)
                if bitsj&1: X.add(d); guards|={a,f}; private.add(a)
                if bitsj&2: X.add(e); guards|={b,f}; private.add(b)
                if bitsj: common.add(f)
            h=sum(bool(x) for x in bits)
            assert len(guards)==len(X)+h and guards==private|common
            M=list(old[3])+[(x,(1,x[1])) for x in sorted(X)]
            cur=(*old[:2],oldT-guards,M)
            assert direct_check(*cur)==18*m+30-h
            if X: assert set(first_times(cur))!=endpoints(M)
            # For every colour-balanced conversion pool, count singleton traps
            # from actual geometry before choosing any perfect matching.
            for Yt in itertools.combinations(sorted(guards),len(X)):
                Y=set(Yt); P=oldP|X|Y; T=oldT-guards
                trapped=set()
                for v in Y:
                    adj=set(neighbors(v))
                    assert not adj&T
                    if v in private: assert len(adj&P)<=2
                    if len(adj&P)<=2: trapped.add(v)
                double=sum(x==3 for x in bits)
                assert len(Y-trapped)<=double<=len(X)//2
                if X: assert trapped
                counts['restricted_conversion_pools']+=1
            counts['restricted_entry_sets']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();max_depth=0
    for m in range(2,9):
        for bits in itertools.product((False,True),repeat=m):
            max_depth=max(max_depth,check_board(m,{j for j,b in enumerate(bits) if b},counts))
    for m in (10,25,50,100):
        for S in (set(range(m)),set(range(0,m,2)),{0},{m-1}):
            max_depth=max(max_depth,check_board(m,S,counts))
    restricted_controls(counts)
    result=dict(status='PASS',counts=dict(counts),max_observed_synchronous_depth=max_depth,
                scope='All subsets for m=2..8; all/even/first/last subsets for m=10,25,50,100. Restricted entry sets and all colour-balanced shield pools for m=2..4.',
                proof='Written arbitrary-length rank formulas and token deletion; finite enumeration checks the adapter and is not a general proof.',
                not_claimed='Arbitrary enlarged footprints; global 5/6 improvement; end-to-end Lean coordinate formalization.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result))


if __name__=='__main__':main()
