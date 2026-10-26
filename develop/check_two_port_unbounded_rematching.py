"""Solver-free audit of the all-length two-port rematching zipper.

The theorem is the coordinate construction, strict actual-mate ranks and
explicit traps in docs/TWO_PORT_UNBOUNDED_REMATCHING.md. Finite enumeration
is used only to check the adapter, never as an all-length proof.
"""
if not __debug__:
    raise RuntimeError('Assertions required; do not run with -O.')

import argparse
from collections import Counter
from itertools import product
import json
from pathlib import Path

from check_ambient_band_port_activation import (CAP_T,CAP_M,CAP_NAMES,
    ambient,rank_certificate,check_ranks,local_closure,check_trap,
    check_ledger,payments,mate_map)
from check_frozen_half_area_attainers import frozen_family
from check_endpoint_invasion_sharp_strips import endpoints,edge_key
from check_cooperative_promotion import neighbors
from check_frozen_equality_matching_rigidity import first_times
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed


def zipper(m):
    h,w,T,_=frozen_family(m);c=w-1;n=3*m+2
    M=[((1,1),(2,1))]
    for j in range(m+1):
        s=6*j
        M += [((2,6+s),(3,6+s)),((1,5+s),(2,5+s)),
              ((1,6+s),(1,7+s)),((2,7+s),(3,7+s)),
              ((3,8+s),(3,9+s))]
    M += [((3,5),(4,5))]
    M += [((3,10+6*i),(3,11+6*i)) for i in range(m)]
    M += [((4,6+2*l),(4,7+2*l)) for l in range(n)]
    return h,w,T,M


def union(m):
    h,w,T,M=zipper(m);shift=lambda v:(v[0],v[1]+w)
    return h,w+6,T|{shift(v) for v in CAP_T},M+[(shift(a),shift(b)) for a,b in CAP_M]


def region_ranks(m):
    c=6*m+9;n=3*m+2;w=c+1;rec=[]
    def add(v,r,a,b):rec.append((v,r,a,b))
    add((1,1),0,(0,1),(1,2));add((2,1),0,(2,0),(3,1))
    for j in range(m+1):
        s=6*j;A=(1,5+s);B=(1,6+s);C=(1,7+s);D=(2,7+s)
        E=(2,6+s);F=(3,6+s);G=(3,7+s);H=(3,8+s);U=(2,5+s);V=(3,5+s)
        add(A,0,(0,5+s),(1,4+s));add(C,0,(0,7+s),(1,8+s))
        add(E,1,B,U);add(V,2,U,F)
        if j<m:
            add((3,9+s),3,(2,9+s),(3,10+s));add(G,4,F,H)
        else:
            add((3,c),3,(2,c),(3,w))
            # This witness choice remains internal even without the p input.
            add(G,n+3,F,(4,c-2))
        k=n+2+6*j
        add(F,k,V,(4,6+s));add(U,k+1,E,V)
        add(B,k+2,A,E);add(D,k+3,C,E)
        add(H,k+4,G,(4,8+s))
        if j<m:add((3,10+s),k+5,(3,9+s),(4,10+s))
    add((4,5),0,(4,4),(5,5))
    for l in range(1,n):add((4,5+2*l),n+2-l,(5,5+2*l),(4,6+2*l))
    for l in range(n):add((4,6+2*l),4+l,(3,6+2*l),(4,5+2*l))
    add((4,c),2,(5,c),(4,w))
    return rec


def union_ranks(m):
    c=6*m+9;n=3*m+2;shift=lambda v:(v[0],v[1]+c+1)
    names={k:shift(v) for k,v in CAP_NAMES.items()}
    table=[('C0',0,(0,1),(1,0)),('A',0,(0,3),(1,4)),
           ('Z',0,(4,4),(5,3)),('E',1,'B','D'),('b',1,(5,1),'L'),
           ('a',2,'D','F'),('q',n+4,'p',('inside',4,c)),
           ('L',n+5,'F','b'),('V',n+6,'F','Z'),
           ('p',9*m+9,'q',('inside',3,c)),('F',9*m+10,'a','L'),
           ('D',9*m+11,'a','E'),('B',9*m+12,'C0','E'),('U',9*m+13,'A','E')]
    def site(s):
        if isinstance(s,str):return names[s]
        return s[1:] if len(s)==3 else shift(s)
    return region_ranks(m)+[(names[v],r,site(a),site(b)) for v,r,a,b in table]


def groups(m):
    cur=zipper(m);P=endpoints(cur[3]);c=cur[1]-1
    black={(3,c),(4,c-1)}
    white={v for v in P if sum(v)%2==1}-{(2,1),(4,5)}
    return black,white,P-(black|white)


def check_partial_ranks(T,M,grants,expected,rec,counts):
    mate=mate_map(M);rank={v:r for v,r,a,b in rec if v in expected}
    assert set(rank)==expected
    for v,r,a,b in rec:
        if v not in expected:continue
        assert a!=b and mate[v] not in (a,b)
        assert all(u in neighbors(v) for u in (a,b))
        assert all(u in T|grants or u in mate and mate[u] in rank and rank[mate[u]]<r for u in (a,b))
        counts['strict_partial_interface_rank_events']+=1


def interface(m,counts):
    h,w,T,M=zipper(m);P=endpoints(M);B,W,E=groups(m)
    assert len(B)==2 and len(W)==9*m+7 and len(E)==9*m+9
    assert all(sum(v)%2==0 for v in B) and all(sum(v)%2==1 for v in W)
    assert B=={(3,w-1),(4,w-2)}
    for p,q in product([False,True],repeat=2):
        grants=({(3,w)} if p else set())|({(4,w)} if q else set())
        expected=E|(B if p else set())|(W if q else set())
        check_partial_ranks(T,M,grants,expected,region_ranks(m),counts)
        actual,_=local_closure(T,M,grants)
        assert actual==expected
        if not p:
            supports=check_trap(T,M,B,grants)
            assert supports=={(3,w-1):[(2,w-1)],(4,w-2):[(4,w-3)]}
            counts['exact_trap_support_tables']+=1
        if not q:
            supports=check_trap(T,M,W,grants)
            expected_supports={v:[] for v in W}
            for v in [(2,5),(3,6)]:expected_supports[v]=[(3,5)]
            for l in range(1,3*m+2):expected_supports[4,5+2*l]=[(5,5+2*l)]
            expected_supports[4,w-1]=[(5,w-1)]
            assert supports==expected_supports
            counts['exact_trap_support_tables']+=1
        counts['exact_two_port_interface_responses']+=1
    return dict(no_input_unfrozen=9*m+9,p_only_unfrozen=9*m+7,q_only_unfrozen=2,both_unfrozen=0)


def check_length(m,counts):
    z=zipper(m);old=frozen_family(m);cur=union(m);h,w,T,M=cur
    assert z[2]==old[2] and endpoints(z[3])==endpoints(old[3])
    assert direct_check(*z)==18*m+30 and direct_check(*cur)==18*m+48==h*w//2
    prescribed=set(map(edge_key,old[3]));actual=set(map(edge_key,z[3]))
    common={edge_key(((1,1),(2,1)))}|{edge_key(((2,6+6*j),(3,6+6*j))) for j in range(m+1)}
    assert prescribed&actual==common and len(prescribed-actual)==8*m+7
    assert len(actual-prescribed)==8*m+7 and len(z[3])==9*m+9
    assert edge_key(((1,5),(1,6))) in prescribed-actual
    assert edge_key(((1,5),(2,5))) in actual-prescribed
    cut=z[1];P=endpoints(M)
    assert all((a[1]<cut)==(b[1]<cut) for a,b in M)
    cross={edge_key((v,u)) for v in T|P if v[1]==cut-1 for u in neighbors(v) if u[1]==cut and u in T|P}
    assert cross=={edge_key(((r,cut-1),(r,cut))) for r in (3,4)}
    ranks=check_ranks(cur,union_ranks(m),counts)
    assert max(ranks.values())==9*m+13
    times=first_times(cur);frozen,layers=frozen_certificate(cur)
    assert frozen==set(times)==P and len(layers)==max(times.values())<=9*m+14
    check_ledger(cur,payments(m),m+4,counts)
    response=interface(m,counts)
    counts['fully_frozen_half_area_zipper_boards']+=1
    counts['queue_synchronous_crosschecks']+=1
    return dict(m=m,shape=[h,w],selected=len(T),matching=len(M),objective=len(T)+len(M),
                missing_prescribed_edges=8*m+7,interface_ports=2,reserve=0,
                max_rank=max(ranks.values()),observed_synchronous_rounds=len(layers),**response)


def stack(m,profile):
    q=len(profile);T=set();M=[];rec=[];w=6*m+16
    for i,zipped in enumerate(profile):
        cur=union(m) if zipped else ambient(m,False)
        ranks=union_ranks(m) if zipped else rank_certificate(m,False)
        shift=lambda v:(v[0]+8*i,v[1])
        T|={shift(v) for v in cur[2]};M += [(shift(a),shift(b)) for a,b in cur[3]]
        rec += [(shift(v),r,shift(a),shift(b)) for v,r,a,b in ranks]
        if i+1<q:T|={(8*i+r,c) for r in (6,7) for c in range(0,w,2)}
    return (8*q-2,w,T,M),rec


def main():
    p=argparse.ArgumentParser();p.add_argument('--max-m',type=int,default=32)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();lengths=sorted(set(range(2,args.max_m+1))|{64,100})
    records=[check_length(m,counts) for m in lengths]
    for m in [2,5]:
        cur=union(m);h,w=cur[:2]
        for tr,fi,fj in product([False,True],repeat=3):
            shape,T,M=transformed(*cur,tr,fi,fj)
            def f(v):
                r,c=v;r=h-1-r if fi else r;c=w-1-c if fj else c
                return (c,r) if tr else (r,c)
            new=(*shape,T,M);assert direct_check(*new)==shape[0]*shape[1]//2
            check_ranks(new,[(f(v),r,f(a),f(b)) for v,r,a,b in union_ranks(m)],counts)
            assert set(first_times(new))==endpoints(M)
            counts['isometry_controls']+=1
    for m in [2,4]:
        for q in range(1,5):
            distinct=set();occupation=None
            for profile in product([False,True],repeat=q):
                cur,rec=stack(m,profile);h,w,T,M=cur;P=endpoints(M)
                assert direct_check(*cur)==h*w//2
                assert occupation is None or occupation==(T,P);occupation=T,P
                edges=frozenset(map(edge_key,M));assert edges not in distinct;distinct.add(edges)
                canonical,_=stack(m,[False]*q)
                assert len(set(map(edge_key,canonical[3]))-edges)==sum(profile)*(8*m+7)
                check_ranks(cur,rec,counts);assert set(first_times(cur))==P
                check_ledger(cur,[p for i in range(q) for p in payments(m,8*i)],q*(m+4),counts)
                counts['exhaustive_stack_profiles']+=1
            assert len(distinct)==2**q
    cur,rec=stack(8,[bool(i%2) for i in range(16)])
    assert direct_check(*cur)==cur[0]*cur[1]//2
    check_ranks(cur,rec,counts);assert set(first_times(cur))==endpoints(cur[3])
    check_ledger(cur,[p for i in range(16) for p in payments(8,8*i)],16*12,counts)
    counts['larger_stack_controls']+=1
    out=dict(status='PASS',theorem='For every m>=2 the same two-port zero-charge cap activates a zipper missing 8m+7 prescribed edges at half-area. The exact missing sets have sizes 9m+9, 9m+7, 2, 0 for no input, p only, q only, both.',
             scope='Explicit all-length rank/trap proof, not an all-matching classification. No per-port bound on number or distance of changed edges, and no positive reserve per activated region. Original isolated theorem and global half-area target unchanged.',
             lengths=lengths,counts=dict(counts),records=records)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k!='records'}))


if __name__=='__main__':main()
