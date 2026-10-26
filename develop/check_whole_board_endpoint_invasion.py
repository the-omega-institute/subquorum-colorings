"""Solver-free controls for the written whole-board endpoint-invasion theorem.

The proof is the algebraic pocket lemma and disjoint all-length coordinates in
WHOLE_BOARD_ENDPOINT_INVASION.md. Finite controls do not replace that proof.
"""
import argparse
from collections import Counter, deque
import itertools
import json
import random
from pathlib import Path
from check_frozen_half_area_attainers import frozen_family
from check_neutral_occupied_envelopes import expanded
from check_endpoint_invasion_sharp_strips import endpoints
from check_promotion_cores import frozen_certificate
from check_frozen_equality_matching_rigidity import first_times
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; do not run with -O.')

BLACK=[(2,0),(3,1),(3,3),(4,0),(4,2),(4,4),(5,1),(5,3)]
WHITE=[(1,0),(3,0),(3,2),(4,1),(2,3),(3,4),(4,3),(5,0),(5,2)]

def neighbors(v,h,w):
    r,c=v
    return {u for u in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)] if 0<=u[0]<h and 0<=u[1]<w}

def local_ok(bits,blanks):
    a,b,C,d,e,f,g,h=bits;u,v,w,x,y,z,q,r,s=blanks
    return (a<=u and b<=min(v,w,x) and f<=min(z,q)
        and 3*C<=w+y+z+q and 2*d<=v+x+r
        and 3*e<=w+x+q+s and 2*g<=x+r+s and h<=q+s)

def check_cases(bits,blanks):
    a,b,C,d,e,f,g,h=bits;u,v,w,x,y,z,q,r,s=blanks
    D=d+e+g+h;k=v+w+x+y+z+q
    assert C+f<=w+y+z and C+f<=y+z+q
    if r==s==1:
        assert b+d<=v+x and e<=w+q and C+f+e<=w+y+z+q
    elif r==1:
        assert D<=max(v,x)+x+q and b+D<=v+2*x+q
    elif s==1:
        if v==0:
            assert b==d==0 and e<=w+q and C+f+e<=w+y+z+q
        else:
            assert D<=2+x and b<=w
    elif q==0:
        assert e==f==g==h==0 and b+d<=v+x
    else:
        assert D<=1+x*max(v,w)
        assert v*w+max(v,w)==v+w and x*(v+w)<=v+x
    assert b+C+f+D<=k+r+s
    assert sum(bits)<=sum(blanks)


def local_controls(counts):
    bad=[]
    for blanks in itertools.product((0,1),repeat=9):
        for bits in itertools.product((0,1),repeat=8):
            if not local_ok(bits,blanks):continue
            counts['degree_feasible_local_models']+=1
            hall=sum(bits[i] for i in (3,4,6,7))<=2+blanks[7]+blanks[8]
            if not hall:
                if sum(bits)>sum(blanks):bad.append((bits,blanks))
                continue
            check_cases(bits,blanks)
            counts['actual_capacity_local_models']+=1
            counts['pocket_equality_models']+=sum(bits)==sum(blanks)
    witness=((0,0,1,1,1,1,1,1),(0,0,1,1,0,1,1,1,0))
    joint=((0,1,1,1,1,1,0,1),(0,1,1,1,0,1,1,0,0))
    assert witness in bad and joint in bad and len(bad)>0
    counts['degree_only_deficit_models_excluded_by_actual_capacity']=len(bad)
    return dict(selected=list(witness[0]),blank=list(witness[1]),
        selected_count=6,blank_count=5,actual_matching_capacity_violation='4>3',
        joint_witness=dict(selected=list(joint[0]),blank=list(joint[1]),
            obstruction='Both occupied (5,0),(5,2) can only mate (5,1); two singleton capacities pass but their joint capacity fails.'))


def board_control(cur,counts,require_frozen=False):
    h,cplus,T,M=cur;c=cplus-1
    assert h==6 and c>=5 and c%2==1
    direct_check(*cur);P=endpoints(M);O=T|P
    board=set(itertools.product(range(h),range(cplus)));H=board-O
    tail={(5,k) for k in range(5,c+1,2)}
    L={(5,k-1) for k in range(5,c+1,2)}
    assert {v for v in T if sum(v)%2==0}<=set(BLACK)|tail
    assert {(2,1)}|{(4,k) for k in range(5,c+1,2)}<=O
    assert {(5,0),(5,2)}.isdisjoint(T)
    assert len(set(BLACK))==8 and len(set(WHITE))==9
    assert set(BLACK).isdisjoint(tail) and set(WHITE).isdisjoint(L)
    assert all(sum(v)%2==0 for v in BLACK) and all(sum(v)%2==1 for v in WHITE)
    assert neighbors((5,0),h,cplus)|neighbors((5,2),h,cplus)=={BLACK[i] for i in (3,4,6,7)}
    bits=tuple(int(v in T) for v in BLACK);blanks=tuple(int(v in H) for v in WHITE)
    assert local_ok(bits,blanks)
    occupied_pair={(5,0),(5,2)}&O
    mate={v:u for edge in M for v,u in (edge,edge[::-1])}
    actual_mates={mate[v] for v in occupied_pair}
    assert len(actual_mates)==len(occupied_pair)
    assert actual_mates<={BLACK[i] for i in (3,4,6,7)}-T
    assert sum(bits[i] for i in (3,4,6,7))<=2+blanks[7]+blanks[8]
    check_cases(bits,blanks)
    selected_tail=T&tail
    paid_tail={(5,k-1) for r,k in selected_tail}
    assert len(paid_tail)==len(selected_tail) and paid_tail<=H
    Hw={v for v in H if sum(v)%2};Tb={v for v in T if sum(v)%2==0};Ow={v for v in O if sum(v)%2}
    pocket_slack=len(H&set(WHITE))-sum(bits)
    tail_slack=len(H&L)-len(selected_tail)
    other=len(Hw-(set(WHITE)|L))
    J=len(T)+len(M)
    assert J==len(Tb)+len(Ow)
    assert min(pocket_slack,tail_slack,other)>=0
    assert h*cplus//2-J==pocket_slack+tail_slack+other
    positive=[];negative=[]
    for r in range(0,h,2):
        for col in range(0,cplus,2):
            tile={(r+i,col+j) for i in (0,1) for j in (0,1)}
            chi=4-2*len(T&tile)-len(P&tile)
            positive.extend(((r,col),i) for i in range(max(0,chi)))
            negative.extend(((r,col),i) for i in range(max(0,-chi)))
    assert len(positive)-len(negative)==h*cplus-2*J
    assert len(positive)==len(set(positive)) and len(negative)==len(set(negative))
    payment=list(zip(positive,negative))
    assert len(payment)==len(negative) and len({a for a,b in payment})==len(payment)
    counts['boards']+=1;counts['physical_tail_payments']+=len(paid_tail)
    counts['actual_pair_mate_events']+=len(actual_mates)
    counts['tile_global_payments']+=len(payment)
    if require_frozen:
        F,layers=frozen_certificate(cur)
        assert F==P and set(first_times(cur))==P
        assert J==h*cplus//2
        counts['fully_frozen_sharp_boards']+=1
    return dict(selected=len(T),matching=len(M),objective=J,pocket_slack=pocket_slack,tail_slack=tail_slack,other_holes=other)


def random_whole_board(m,seed,new_white=False):
    rng=random.Random(seed);h,w,T0,M0=frozen_family(m)
    V=set(itertools.product(range(h),range(w)))
    mate={v:u for e in M0 for v,u in (e,e[::-1])}
    starts=sorted(V-set(mate));rng.shuffle(starts)
    for start in starts[:len(starts)//2]:
        if start in mate:continue
        parent={start:None};queue=deque([start]);end=None
        while queue and end is None:
            v=queue.popleft();ns=sorted(neighbors(v,h,w));rng.shuffle(ns)
            for u in ns:
                if mate.get(v)==u or u in parent:continue
                parent[u]=v
                if u not in mate:end=u;break
                z=mate[u]
                if z not in parent:parent[z]=u;queue.append(z)
        if end is None:continue
        path=[end]
        while parent[path[-1]] is not None:path.append(parent[path[-1]])
        path.reverse();assert len(path)%2==0
        for v in path:mate.pop(v,None)
        for a,b in zip(path[::2],path[1::2]):mate[a]=b;mate[b]=a
    M=sorted({tuple(sorted((v,u))) for v,u in mate.items()})
    T=T0-set(mate)
    while True:
        bad=[v for v in sorted(T) if len(neighbors(v,h,w)&(T|set(mate)))>1]
        if not bad:break
        T.remove(rng.choice(bad))
    if new_white:
        choices=sorted(v for v in V-(T|set(mate)|{(5,0),(5,2)}) if sum(v)%2)
        rng.shuffle(choices)
        for v in choices:
            trial=T|{v};O=trial|set(mate)
            if all(len(neighbors(u,h,w)&O)<=1 for u in trial):T=trial
    assert endpoints(M0)<=endpoints(M)
    return h,w,T,M


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();obstruction=local_controls(counts);examples=[]
    for m in list(range(2,21))+[25,50,100]:
        base=frozen_family(m);T0=base[2];P0=endpoints(base[3])
        assert {v for v in T0 if sum(v)%2==0}==set(BLACK)|{(5,k) for k in range(5,6*m+10,2)}
        rec=board_control(base,counts,True);assert rec['objective']==18*m+30
        patterns=itertools.product(range(3),repeat=m) if m<=5 else [tuple(1 for _ in range(m)),tuple(2 for _ in range(m)),tuple(i%3 for i in range(m))]
        for word in patterns:
            S={j for j,x in enumerate(word) if x};A={j for j,x in enumerate(word) if x==2}
            cur=expanded(m,S,A);board_control(cur,counts,True)
        # Arbitrary selected withdrawals keep feasibility; no freezing is assumed.
        for residue in range(4):
            T={v for v in T0 if (v[0]+3*v[1])%4!=residue}
            board_control((*base[:2],T,base[3]),counts)
    for m in [2,3,8,20]:
        for seed in range(16):
            for new_white in [False,True]:
                cur=random_whole_board(m,seed,new_white)
                board_control(cur,counts)
                counts['arbitrary_whole_board_rematchings']+=1
                counts['skeleton_controls_with_new_white_selections']+=bool(cur[2]-frozen_family(m)[2])
    data=Path(__file__).resolve().parents[1]/'output/whole-board-endpoint-invasion-examples.json'
    for raw in json.loads(data.read_text()):
        m=raw['m'];base=frozen_family(m)
        T={tuple(v) for v in raw['selected']};M=[tuple(map(tuple,e)) for e in raw['matching']]
        assert T<=base[2] and endpoints(base[3])<=endpoints(M)
        rec=board_control((*base[:2],T,M),counts,raw['require_frozen'])
        assert rec['objective']==raw['J']
        examples.append(dict(m=m,discovery_status=raw['status'],frozen_required=raw['require_frozen'],**rec))
    result=dict(status='PASS',theorem='All m>=2, retained P0 and T subset T0, arbitrary whole-board new endpoints and actual rematching: exact maximum J=18m+30=area/2, attained fully frozen.',
        proof='Written algebraic four-case pocket lemma, injective two-site actual-mate capacity, and disjoint all-length bottom-hole budget. Finite checks do not replace this proof.',
        scope='Also checks the weaker occupied-anchor/black-selection skeleton. Not a universal 5/6 improvement or complete equality-footprint classification.',
        counts=dict(counts),degree_only_obstruction=obstruction,discovery_examples=examples)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))

if __name__=='__main__':main()
