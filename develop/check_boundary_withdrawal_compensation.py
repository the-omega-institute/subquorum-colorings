"""Standard-library controls for the all-length boundary-state proof.

The written weighted identities and state induction are the proof; finite
models check them. No numerical optimizer is used by this verifier.
"""
import argparse
from collections import Counter,deque
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_endpoint_invasion_sharp_strips import POCKET,endpoints,edge_key,free_vertices
from check_occupied_strip_degree_four_budget import family
from check_residual_corridors import direct_check
from check_promotion_cores import frozen_certificate
from check_selection_withdrawal_sharp_strips import attaining
from check_connected_band_integer_compensation import ROWS as OLDROWS,module,weight

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')

A=set(POCKET);Q=(4,5);LAST=(5,5);AP=A|{Q}
# weight, list of (kind,site,coefficient), right side.
ROWS=[
 (1,[('o',(2,3),1)],1),
 (4,[('t',(3,3),1),('o',(2,3),1),('o',(3,4),1)],2),
 (1,[('t',(3,3),2),('o',(2,3),1),('o',(3,4),1),('o',(4,3),1)],3),
 (4,[('t',(3,5),1),('o',(2,5),1)],1),
 (2,[('t',(3,5),1),('o',(2,5),1),('o',Q,1)],2),
 (2,[('o',(4,2),1)],1),
 (2,[('t',(4,2),1),('o',(4,3),1),('o',(5,2),1)],2),
 (3,[('t',(4,4),1),('o',Q,1),('o',(5,4),1)],2),
 (1,[('t',(4,4),3),('o',(3,4),1),('o',(4,3),1),('o',Q,1),('o',(5,4),1)],4),
 (6,[('t',(5,0),1),('o',(4,0),1),('o',(5,1),1)],2),
 (2,[('t',(5,2),1),('o',(4,2),1),('o',(5,3),1)],2),
 (2,[('t',(5,3),2),('o',(4,3),1),('o',(5,2),1),('o',(5,4),1)],3)]
HC={edge_key(e):w for w,e in [(4,((4,2),(4,3))),(2,((4,2),(5,2))),
     (2,((4,3),(5,3))),(4,((5,1),(5,2))),(2,((5,3),(5,4))) ]}
PORTS=[((2,5),(1,5)),((2,5),(2,6)),((3,5),(3,6)),(Q,(4,6)),(LAST,(5,6))]
INTERNAL=sorted({edge_key((v,u)) for v in AP for u in set(neighbors(v))&AP})
POSSIBLE=INTERNAL+list(map(edge_key,PORTS))


def evaluate(rows,T,P):
    O=T|P;lhs=0
    for w,terms,b in rows:
        val=sum(q*int(v in (T if kind=='t' else O)) for kind,v,q in terms)
        assert val<=b;lhs+=w*val
    return lhs


def symbolic_coefficients(counts):
    for rows,S,scale,isnew in [(OLDROWS,A,4,False),(ROWS,AP,6,True)]:
        lhs=Counter()
        for w,terms,b in rows:
            for kind,v,q in terms:
                lhs['t',v]+=w*q
                if kind=='o':
                    for e in POSSIBLE:
                        if v in e:lhs['e',e]+=w*q
        for v in S:assert lhs['t',v]+(6 if isnew and v==LAST else 0)==scale
        for e in POSSIBLE:
            target=scale*sum(sum(v)%2 for v in set(e)&S)
            if isnew:assert lhs['e',e]==target+HC.get(e,0)
            else:assert lhs['e',e]>=target
        assert sum(w*b for w,_,b in rows)==(58 if isnew else 39)
        counts['symbolic_pocket_identities']+=1


def pocket_bound(T,P,M,counts):
    T=T&AP;P=P&AP;O=T|P
    meet=[edge_key(e) for e in M if set(e)&AP]
    assert set(meet)<=set(POSSIBLE)
    old=evaluate(OLDROWS,T&A,P&A);oldW=weight(A,T,P)
    assert 4*oldW<=old<=39 and oldW<=9
    lhs=evaluate(ROWS,T,P);W=weight(AP,T,P);r=int(LAST in T)
    H=sum(HC.get(e,0) for e in meet)
    assert lhs+6*r==6*W+H and lhs<=58
    assert W<=9+r and W<=9+int(Q in O)<=10
    if W==10:
        assert LAST in T and Q in O
        counts['pocket_maximum_boundary_states']+=1
    counts['pocket_controls']+=1
    return W


def all_pocket_controls(counts):
    P0=endpoints(family(3)[0][3]);es=INTERNAL+list(map(edge_key,[PORTS[0],*PORTS[2:]]))
    best=-1;maxpatterns=0
    def visit(i,M,used):
        nonlocal best,maxpatterns
        if i==len(es):
            P=set(used);rest=sorted(AP-P)
            for bits in itertools.product((0,1),repeat=len(rest)):
                T={v for v,b in zip(rest,bits) if b};O=T|P|P0
                if any(len(set(neighbors(t))&O)>1 for t in T):continue
                W=pocket_bound(T,P,M,counts);best=max(best,W)
                maxpatterns+=W==10
                counts['independent_partial_pocket_models']+=1
            return
        visit(i+1,M,used);a,b=es[i]
        if not {a,b}&used:visit(i+1,M+[es[i]],used|{a,b})
    visit(0,[],set());assert best==10 and maxpatterns
    counts['pocket_capacity_ten_models']=maxpatterns


def all_local_states(counts):
    equality=[]
    for q in itertools.product((0,1),repeat=13):
        x,y,z,u,v,w,A,B,C,D,E,F,G=q
        if x and not A==D==1 or y and not A==B==E==1:continue
        if z and B+C+F+G<3 or u and A+D+E<2 or v and B+E+F<2 or w and C+F<1:continue
        W=sum(q[:6])+7-sum(q[6:]);assert W<=7
        counts['thirteen_site_models']+=1
        if x==0 and D==1:
            counts['input_state_models']+=1
            if W==7:equality.append(q)
    assert equality==[(0,0,0,1,1,1,0,0,0,1,1,1,0)]
    for q in itertools.product((0,1),repeat=7):
        x,y,u,w,A,B,C=q
        if x and not A==B==1 or y and not A==C==1 or u and A+B+C<2:continue
        W=x+y+u+w+3-A-B-C;assert W<=4
        if x==0 and B==1:assert W<=3
        counts['right_end_models']+=1


def domain(m):
    old=family(m+1)[0];P0=endpoints(old[3])
    R=old[2]-{(3,9+6*i) for i in range(m)}-{v for v in old[2] if v[0]==4}
    U=free_vertices((*old[:2],R,old[3]));return old,R,P0,U


def geometry(m,counts):
    old,R,P0,U=domain(m)
    pairs=[{(2,c),(3,c)} for i in range(m) for c in (9+6*i,11+6*i)]
    blocks=[set(sum(module(a),[])) for a in range(6,6*m+1,6)]
    end={(4,6*m+c) for c in (6,7,8)}|{(5,6*m+c) for c in (6,7,8,9)}
    cover=Counter(v for S in [AP,*pairs,*blocks,end] for v in S)
    assert set(cover)==U and set(cover.values())=={1} and len(U)==17*m+23
    assert len(R)==5*m+11 and sum(sum(v)%2 for v in P0)==4*m+5
    assert all(not set(neighbors(v))&R for v in U)
    forced={0:set(range(0,6*m+10,2)),1:{0}|{3+6*j for j in range(m+2)},
            2:{2,6*m+9}|{c+6*j for j in range(m+1) for c in (4,8)},
            3:{0,2},4:{1,6*m+9},5:set()}
    blanks={(r,c) for r,cols in forced.items() for c in cols}
    assert blanks==set(itertools.product(range(6),range(6*m+10)))-(R|P0|U)
    anchored={v for v in R if set(neighbors(v))&P0}
    assert all(set(neighbors(v))&anchored for v in blanks)
    counts['disjoint_finite_board_partitions']+=1
    return old,R,P0,U,pairs,blocks,end


def random_model(m,seed):
    old,R,P0,U=domain(m);rng=random.Random(seed);possible=U|P0
    mate={v:u for e in old[3] for v,u in (e,e[::-1])};starts=sorted(U);rng.shuffle(starts)
    for start in starts[:rng.randrange(len(starts)+1)]:
        if start in mate:continue
        parent={start:None};queue=deque([start]);end=None
        while queue and end is None:
            v=queue.popleft();ns=sorted(set(neighbors(v))&possible);rng.shuffle(ns)
            for u in ns:
                if mate.get(v)==u or u in parent:continue
                parent[u]=v
                if u not in mate:end=u;break
                w=mate[u]
                if w not in parent:parent[w]=u;queue.append(w)
        if end is None:continue
        path=[end]
        while parent[path[-1]] is not None:path.append(parent[path[-1]])
        path.reverse()
        for v in path:mate.pop(v,None)
        for a,b in zip(path[::2],path[1::2]):mate[a]=b;mate[b]=a
    M=sorted({edge_key((v,u)) for v,u in mate.items()});T=set(R);choices=sorted(U-set(mate));rng.shuffle(choices)
    for v in choices:
        if rng.randrange(5)==0:continue
        trial=T|{v};O=trial|set(mate)
        if all(len(set(neighbors(t))&O)<=1 for t in trial):T=trial
    return (*old[:2],T,M)


def left_gain_model(m):
    old,R,P0,U=domain(m)
    T=R|{(2,3),(3,4),(4,0),(4,2),(4,5),(5,0),(5,3),(5,5)}
    removed={edge_key(e) for e in [((2,6),(3,6)),((3,7),(3,8))]}
    M=[e for e in old[3] if edge_key(e) not in removed]
    M += [((2,5),(2,6)),((3,6),(3,7)),((3,8),(4,8)),((3,3),(4,3))]
    return (*old[:2],T,M)


def board_control(m,cur,counts,sharp=False):
    old,R,P0,U,pairs,blocks,end=geometry(m,counts);T,M=cur[2:];P=endpoints(M)
    direct_check(*cur);assert R<=T and P0<=P and ((T-R)|(P-P0))<=U
    nt=T-R;np=P-P0;O=nt|np
    for pair in pairs:assert weight(pair,nt,np)<=1
    L=pocket_bound(nt,np,M,counts);vals=[];state=(L==10);paid=None
    for a,S in zip(range(6,6*m+1,6),blocks):
        V=weight(S,nt,np);assert V<=7;vals.append(V)
        if state:
            assert (4,a) not in nt and (5,a) not in O
            if V<7:paid=('block',a);state=False
            else:
                B,W=module(a);q=tuple(int(v in nt) for v in B)+tuple(int(v not in O) for v in W)
                assert q==(0,0,0,1,1,1,0,0,0,1,1,1,0)
                assert (4,a+6) not in nt and (5,a+6) not in O
                counts['saturated_state_transmissions']+=1
    endW=weight(end,nt,np);assert endW<=4
    if state:assert endW<=3;paid=('right',6*m+6)
    if L==10:assert paid is not None;counts['actual_left_extra_unit_compensated']+=1
    potentials=[int((4,a) not in nt and (5,a) not in O) for a in range(6,6*m+7,6)]
    assert L<=9+potentials[0]
    assert all(val+potentials[i]<=7+potentials[i+1] for i,val in enumerate(vals))
    assert endW+potentials[-1]<=4
    assert sum(vals)+potentials[0]<=7*m+potentials[-1]
    counts['telescoping_potential_controls']+=1
    WU=weight(U,nt,np);J=len(T)+len(M)
    assert WU==L+sum(weight(S,nt,np) for S in pairs)+sum(vals)+endW<=9*m+13
    assert J==9*m+16+WU<=18*m+29
    pos=[];neg=[];strip=0
    for r in (0,2,4):
        for c in range(0,6*m+10,2):
            S={(r+i,c+j) for i in (0,1) for j in (0,1)};charge=4-2*len(T&S)-len(P&S)
            if r==0:strip+=charge;continue
            pos += [((r,c),j) for j in range(max(charge,0))]
            neg += [((r,c),j) for j in range(max(-charge,0))]
    assert strip==-m and len(pos)>=len(neg)+m+2
    paidtokens=pos[:len(neg)+m];reserve=pos[len(neg)+m:]
    assert len(set(paidtokens))==len(paidtokens) and set(paidtokens).isdisjoint(reserve)
    counts['physical_token_controls']+=1
    if sharp:assert J==18*m+29 and frozen_certificate(cur)[0]==P;counts['frozen_sharp_attainers']+=1
    else:
        counts['actual_rematching_models']+=1
        counts['models_changing_old_edges']+=not set(map(edge_key,old[3]))<=set(map(edge_key,M))
        missing=sum(v not in T for v in [(4,6),(4,6*m+6),(4,6*m+8)])
        counts['actual_boundary_guard_deletions']+=missing
        counts['all_three_boundary_guards_absent']+=missing==3


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();counts=Counter()
    symbolic_coefficients(counts);all_local_states(counts);all_pocket_controls(counts)
    fixture=json.loads((Path(__file__).parent/'fixtures/boundary_withdrawal_attainer_m2.json').read_text())
    cur=(6,22,set(map(tuple,fixture['T'])),[tuple(map(tuple,e)) for e in fixture['M']])
    board_control(2,cur,counts);assert len(cur[2])+len(cur[3])==65
    assert all(v not in cur[2] for v in [(4,6),(4,18),(4,20)])
    propagation=json.loads((Path(__file__).parent/'fixtures/boundary_state_propagation_models.json').read_text())
    for d in propagation['models']:
        m=d['m'];cur=(6,6*m+10,set(map(tuple,d['T'])),[tuple(map(tuple,e)) for e in d['M']])
        before=counts['saturated_state_transmissions']
        board_control(m,cur,counts)
        assert counts['saturated_state_transmissions']-before==m
        assert len(cur[2])+len(cur[3])==18*m+29
        counts['actual_full_chain_transmission_models']+=1
    for m in list(range(2,15))+[18,24,32,64,100]:
        geometry(m,counts);board_control(m,attaining(m+1,set(range(m))),counts,True)
        gain=left_gain_model(m);board_control(m,gain,counts)
        nt=gain[2]-domain(m)[1];np=endpoints(gain[3])-domain(m)[2]
        assert weight(AP,nt,np)==10 and len(gain[2])+len(gain[3])==9*m+26
        counts['all_length_formula_left_gain_controls']+=1
        if m<=32:
            for seed in range(10):board_control(m,random_model(m,seed),counts)
    assert counts['all_three_boundary_guards_absent'] and counts['models_changing_old_edges']
    result=dict(status='PASS',theorem='All m>=2: exact maximum 18m+29 with every old row-four selection optional; written weighted certificates and boundary-state induction are primary.',counts=dict(counts),scope='Finite controls of universal written proof. Lean audits formalize algebra and abstract state induction, not the complete graph reduction.')
    a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))

if __name__=='__main__':main()
