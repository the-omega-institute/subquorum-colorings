"""Exact controls for the written all-length integer compensation proof.

Standard library only. Enumeration checks identities and does not replace
any universal argument in CONNECTED_BAND_INTEGER_COMPENSATION.md.
"""
import argparse
from collections import Counter, deque
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_connected_band_fractional_matching import domain
from check_endpoint_invasion_sharp_strips import POCKET, EDGES, endpoints, edge_key
from check_occupied_strip_degree_four_budget import family
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_selection_withdrawal_sharp_strips import attaining

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

# (weight, [(kind,site,coefficient)], right side).
ROWS = [
 (1,[('o',(2,3),1)],1),
 (2,[('t',(3,3),1),('o',(2,3),1),('o',(3,4),1)],2),
 (1,[('t',(3,3),2),('o',(2,3),1),('o',(3,4),1),('o',(4,3),1)],3),
 (4,[('t',(3,5),1),('o',(2,5),1)],1),
 (1,[('t',(4,2),1),('o',(4,3),1),('o',(5,2),1)],2),
 (1,[('t',(4,4),1),('o',(3,4),1),('o',(4,3),1)],2),
 (4,[('t',(5,0),1),('o',(4,0),1),('o',(5,1),1)],2),
 (3,[('t',(5,2),1),('o',(4,2),1),('o',(5,3),1)],2),
 (1,[('t',(5,3),1),('o',(4,3),1),('o',(5,4),1)],2),
 (3,[('t',(5,4),1),('o',(4,4),1),('o',(5,5),1)],2),
 (1,[('o',(5,5),1)],1)]
H = {edge_key(e) for e in [((3,4),(4,4)),((4,2),(4,3)),
                           ((4,3),(4,4)),((4,3),(5,3))]}
E0 = {edge_key(e) for e in [((5,1),(5,2)),((5,4),(5,5))]}
PORTS = [((2,5),(1,5)),((2,5),(2,6)),((3,5),(3,6))]


def black(v): return sum(v)%2 == 0

def weight(S,T,P):
    return sum(black(v) and v in T or not black(v) and v in T|P for v in S)


def local_certificate(bits,blanks,counts,left=False):
    x,y,z,u,v,w=bits;A,B,C,D,E,F,G=blanks
    assert all(b in (0,1) for b in bits+blanks)
    assert (not x or A==D==1) and (not y or A==B==E==1)
    assert (not z or B+C+F+G>=3) and (not u or A+D+E>=2)
    assert (not v or B+E+F>=2) and (not w or C+F>=1)
    assert sum(blanks)>=sum(bits)
    if left:
        assert x==0 and A==D==1
        assert sum(blanks)>=sum(bits)+1
    counts['left_local_controls' if left else 'thirteen_site_controls']+=1


def all_local_controls(counts):
    for values in itertools.product((0,1),repeat=13):
        x,y,z,u,v,w,A,B,C,D,E,F,G=values
        if x and not A==D==1 or y and not A==B==E==1: continue
        if z and B+C+F+G<3 or u and A+D+E<2: continue
        if v and B+E+F<2 or w and C+F<1: continue
        local_certificate(values[:6],values[6:],counts)
        if not x and A==D==1: local_certificate(values[:6],values[6:],counts,True)


def pocket_coefficients(counts):
    es=EDGES+PORTS; lhs=Counter()
    for weight,terms,rhs in ROWS:
        for kind,v,q in terms:
            lhs['t',v]+=weight*q
            if kind=='o':
                for e in es:
                    if v in e: lhs['e',edge_key(e)]+=weight*q
    rhs=Counter({('t',v):4 for v in POCKET})
    for e in es:
        e=edge_key(e)
        rhs['e',e]=4*int(e in EDGES or (2,5) in e)+3*int(e in H)+int(e in E0)
    # Counter equality checks all coefficients, including zero port coefficient.
    assert lhs==rhs and sum(w*b for w,_,b in ROWS)==39
    counts['exact_symbolic_pocket_identities']+=1


def pocket_certificate(T,P,M,counts):
    S=set(POCKET);lt=T&S;lp=P&S;O=lt|lp
    inside={edge_key(e) for e in M if set(e)<=S}
    cross={edge_key(e) for e in M if len(set(e)&S)==1}
    assert cross<=set(map(edge_key,PORTS))
    xU=sum((2,5) in e for e in cross);assert xU<=1
    t=lambda v:int(v in lt);o=lambda v:int(v in O)
    lhs=0
    for w,terms,b in ROWS:
        val=sum(q*(t(v) if kind=='t' else o(v)) for kind,v,q in terms)
        assert val<=b;lhs+=w*val
    W=weight(S,lt,lp)
    assert W==len(lt)+len(inside)+xU
    assert lhs==4*W+3*len(inside&H)+len(inside&E0)<=39
    assert W<=9
    counts['pocket_certificates']+=1
    return W


def all_pocket_controls(counts):
    S=set(POCKET);P0=endpoints(family(2)[0][3])
    # The two U outside mates are indistinguishable locally; cover their
    # coefficients separately above, then enumerate one representative port.
    es=EDGES+[PORTS[0],PORTS[2]];maxima={}
    def visit(i,M,used):
        if i==len(es):
            P=set(used);rest=sorted(S-P)
            for bits in itertools.product((0,1),repeat=len(rest)):
                T={v for v,b in zip(rest,bits) if b};O=T|P|P0
                if any(len(set(neighbors(t))&O)>1 for t in T):continue
                W=pocket_certificate(T,P,M,counts)
                counts['independent_pocket_partial_matching_models']+=1
                key=str((int(PORTS[0] in M),int(PORTS[2] in M)))
                maxima[key]=max(maxima.get(key,-1),W)
            return
        visit(i+1,M,used)
        a,b=es[i]
        if not {a,b}&used:visit(i+1,M+[es[i]],used|{a,b})
    visit(0,[],set())
    assert maxima=={'(0, 0)':9,'(0, 1)':8,'(1, 0)':9,'(1, 1)':9}
    return maxima


def module(a):
    B=[(4,a),(4,a+2),(4,a+4),(5,a+1),(5,a+3),(5,a+5)]
    W=[(4,a+1),(4,a+3),(4,a+5),(5,a),(5,a+2),(5,a+4),(3,a+4)]
    return B,W


def geometry(m,counts):
    old,R,P0,U,C,es=domain(m)
    A=set(POCKET);I={(5,6*m+7),(5,6*m+9)}
    assert U==C|A|I and not (C&A or C&I or A&I)
    forced={0:set(range(0,6*m+10,2)),
            1:{0}|{3+6*j for j in range(m+2)},
            2:{2,6*m+9}|{c+6*j for j in range(m+1) for c in (4,8)},
            3:{0,2},4:{1,5,7,6*m+5,6*m+7,6*m+9},5:{6,6*m+6,6*m+8}}
    blanks={(r,c) for r,cols in forced.items() for c in cols}
    board=set(itertools.product(range(6),range(6*m+10)))
    assert blanks==board-(R|P0|U)
    anchored={v for v in R if set(neighbors(v))&P0}
    assert all(set(neighbors(v))&anchored for v in blanks)
    assert [sum(r==i for r,c in R) for i in range(6)]==[3*m+5,2*m+3,1,2,3,0]
    assert len(R)==5*m+14 and sum(not black(v) for v in P0)==4*m+5
    assert all(not set(neighbors(v))&R for v in U)
    pairs=[[(2,c),(3,c)] for i in range(m) for c in (9+6*i,11+6*i)]
    L={(3,10)}|{(4,c) for c in range(8,12)}|{(5,c) for c in range(7,12)}
    blocks=[set(B+W) for a in range(12,6*m+1,6) for B,W in [module(a)]]
    parts=[set(p) for p in pairs]+[L]+blocks
    cover=Counter(v for S in parts for v in S)
    blank=(4,6*m+5)
    assert set(cover)==C|{blank} and set(cover.values())=={1}
    assert blank not in U|R|P0
    assert (4,6) in R and {(4,7),(5,6)}.isdisjoint(U|R|P0)
    for a in range(6,6*m+1,6):
        B,W=module(a)
        x,y,z,u,v,w=B
        if a>=12:assert set(neighbors(x))&P0
        assert set(neighbors(y))&P0
        assert set(neighbors(z))>=set([W[i] for i in (1,2,5,6)])
        assert set(neighbors(u))>=set([W[i] for i in (0,3,4)])
        assert set(neighbors(v))>=set([W[i] for i in (1,4,5)])
        assert set(neighbors(w))>=set([W[i] for i in (2,5)])
    assert 2*m+6+7*(m-1)==9*m-1
    counts['disjoint_open_board_covers']+=1
    return old,R,P0,U,C,pairs,L,blocks


def random_model(m,seed):
    old,R,P0,U,C,es=domain(m);rng=random.Random(seed)
    mate={v:u for e in old[3] for v,u in (e,e[::-1])}
    starts=sorted(U);rng.shuffle(starts)
    for start in starts[:rng.randrange(len(starts)+1)]:
        if start in mate:continue
        parent={start:None};queue=deque([start]);end=None
        while queue and end is None:
            v=queue.popleft();ns=sorted(set(neighbors(v))&(U|P0));rng.shuffle(ns)
            for u in ns:
                if mate.get(v)==u or u in parent:continue
                parent[u]=v
                if u not in mate:end=u;break
                w=mate[u]
                if w not in parent:parent[w]=u;queue.append(w)
        if end is None:continue
        path=[end]
        while parent[path[-1]] is not None:path.append(parent[path[-1]])
        path.reverse();assert len(path)%2==0
        for v in path:mate.pop(v,None)
        for a,b in zip(path[::2],path[1::2]):mate[a]=b;mate[b]=a
    M=sorted({edge_key((v,u)) for v,u in mate.items()});T=set(R)
    choices=sorted(U-set(mate));rng.shuffle(choices)
    for v in choices:
        if rng.randrange(5)==0:continue
        trial=T|{v};O=trial|set(mate)
        if all(len(set(neighbors(t))&O)<=1 for t in trial):T=trial
    return (*old[:2],T,M)


def board_control(m,cur,counts,sharp=False):
    old,R,P0,U,C,pairs,L,blocks=geometry(m,counts)
    T,M=cur[2:];P=endpoints(M);direct_check(*cur)
    assert R<=T and P0<=P and (T-R)|(P-P0)<=U
    nt=T-R;np=P-P0;O=nt|np
    assert len(P)==2*len(M) and sum(not black(v) for v in P)==len(M)
    for d,g in pairs:assert int(d in O)+int(g in nt)<=1
    for a in range(12,6*m+1,6):
        B,W=module(a);bits=tuple(int(v in nt) for v in B);blanks=tuple(int(v not in O) for v in W)
        local_certificate(bits,blanks,counts)
        assert weight(set(B+W),nt,np)<=7
    B,W=module(6)
    local_certificate(tuple(int(v in nt) for v in B),tuple(int(v not in O) for v in W),counts,True)
    assert weight(L,nt,np)<=6 and weight(C,nt,np)<=9*m-1
    pocket_certificate(nt,np,M,counts)
    WU=weight(U,nt,np);J=len(T)+len(M)
    assert J==9*m+19+WU<=18*m+29
    # Tokens on the original aligned physical tiles, with exterior debts first.
    positive=[];negative=[];strip=0
    for r in range(0,6,2):
        for c in range(0,6*m+10,2):
            Q={(r+i,c+j) for i in (0,1) for j in (0,1)}
            charge=4-2*len(T&Q)-len(P&Q)
            if r==0:strip+=charge;continue
            positive += [((r,c),j) for j in range(max(charge,0))]
            negative += [('exterior',(r,c),j) for j in range(max(-charge,0))]
    assert strip==-m
    demands=negative+[('strip',j) for j in range(m)]
    assert len(positive)>=len(demands)+2
    paid=positive[:len(demands)];reserve=positive[len(demands):]
    assert len(set(paid))==len(demands) and set(paid).isdisjoint(reserve)
    counts['original_tile_token_assignments']+=1
    if sharp:
        assert J==18*m+29 and frozen_certificate(cur)[0]==P
        counts['fully_frozen_sharp_attainers']+=1
    else:
        counts['random_actual_rematchings']+=1
        counts['models_changing_old_edges']+=not set(map(edge_key,old[3]))<=set(map(edge_key,M))
        counts['h_withdrawals']+=sum((4,8+6*i) not in T for i in range(m))
        counts['f_withdrawals']+=sum((4,12+6*i) not in T for i in range(m-1))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    counts=Counter();all_local_controls(counts);pocket_coefficients(counts)
    maxima=all_pocket_controls(counts)
    for m in list(range(2,17))+[18,24,32,64,100]:
        geometry(m,counts)
        board_control(m,attaining(m+1,set(range(m))),counts,True)
        if m<=32:
            for seed in range(8):board_control(m,random_model(m,seed),counts)
    assert counts['models_changing_old_edges'] and counts['h_withdrawals'] and counts['f_withdrawals']
    result=dict(status='PASS',theorem='All m>=2: exact integer J maximum 18m+29; written general proof is primary',
                pocket_coloured_maxima=maxima,counts=dict(counts),
                scope='Local exhaustive controls and finite boards validate a general written proof; they are not its replacement.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
