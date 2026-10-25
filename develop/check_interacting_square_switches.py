"""Actual interacting frozen rematching and arbitrary-support repair theorem.

Finite checks corroborate the general written all-Q proof. The independent
abstract route enumeration checks both identity and mixed entrance capacities.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_frozen_mixed_gate_cycle import load_model
from check_occupied_cycle_chambers import actual
from check_merger_completion_reserves import feasible,frozen,owner_data,whole_bands,whole_support_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_reserve_boundary_split import clipped,distance
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize,primitive_certificates
from check_frozen_tip_slot_obstruction import independent_strands

if not __debug__:
    raise RuntimeError('Run without -O.')
FIXTURE=Path(__file__).parent/'fixtures/frozen_double_square_switch.json'


def pair(E,F,Q):
    return any(x!=y for x in E&Q for y in F&Q)


def sdr(groups,Q):
    groups=sorted([E&Q for E in groups],key=len)
    def choose(i,used):
        return i==len(groups) or any(choose(i+1,used|{j}) for j in groups[i]-used)
    return choose(0,set())


def prediction(classes,Q):
    """Includes the one private A payment of cost1."""
    P,L,R,U,W=classes
    full=pair(L,P|R|W,Q) or pair(W,P|R,Q)
    v=2+bool(Q&(P|L|R|W))+full
    direct=P|L|R
    if v==2:
        c=0 if Q&direct else 1 if Q&(U|W) else 2
    elif v==3:
        candidates=[]
        if any(pair(E,F,Q) for E,F in [(P,L),(P,R),(L,R)]):candidates.append(0)
        if pair(U,direct,Q) or pair(W,direct,Q):candidates.append(1)
        if Q&direct or pair(U,W,Q):candidates.append(2)
        if Q&W:candidates.append(3)
        c=min(candidates)
    else:
        candidates=[]
        if sdr([P,L,R],Q):candidates.append(0)
        if any(sdr(gs,Q) for gs in [(P,L,W),(P,W,R),(U,L,R),(P,L,U)]):candidates.append(1)
        if pair(L,R,Q) or pair(P,L,Q) or any(sdr(gs,Q) for gs in [(U,L,W),(U,W,R),(P,U,W)]):candidates.append(2)
        if pair(W,L|P|R,Q):candidates.append(3)
        c=min(candidates)
    return int(v),1+c


def brute_interface(classes,Q):
    P,L,R,U,W=classes
    direct=lambda E:[(frozenset(),j,0) for j in E&Q]
    gate=lambda g,E:[(frozenset({g}),j,1) for j in E&Q]
    beta=(frozenset({'u'}),'beta',2)
    options=[direct(P)+gate('u',U)+[beta],direct(L)+gate('w',W),direct(R)+gate('u',U)+gate('w',W)+[beta]]
    best=(0,0)
    for choices in itertools.product(*[[None]+ops for ops in options]):
        chosen=[p for p in choices if p is not None]
        units=[p[1] for p in chosen]
        gates=[g for p in chosen for g in p[0]]
        if len(units)!=len(set(units)) or len(gates)!=len(set(gates)):continue
        candidate=(len(chosen),sum(p[2] for p in chosen))
        if (candidate[0],-candidate[1])>(best[0],-best[1]):best=candidate
    return 1+best[0],1+best[1]


def model():
    old,od,om,*_=load_model()
    record=json.loads(FIXTURE.read_text());cur=actual(record)
    assert feasible(cur) and frozen(cur)
    check_rank_certificate(cur,[[tuple(v) for v in layer] for layer in record['freezing_layers']])
    canon=lambda es:{tuple(sorted(e)) for e in es}
    assert cur[:3]==old[:3]
    assert {v for e in cur[3] for v in e}=={v for e in old[3] for v in e}
    removed=canon([((5,c),(6,c)) for c in (4,5,18,19)])
    added=canon([((r,c),(r,c+1)) for r,c in itertools.product((5,6),(4,18))])
    assert canon(old[3])-canon(cur[3])==removed
    assert canon(cur[3])-canon(old[3])==added
    d,meta,_=whole_support_data(cur,whole_bands(cur));o,aa,bb,mm=owner_data(*d[:2])
    assert tuple(map(len,(aa,bb,mm)))==(4,6,15)
    assert d[0]==od[0] and d[2]==od[2] and d[4]==od[4]
    for key in ('labels','intervals','boundary'):assert meta[key]==om[key]
    A,B,D,C=[o[v] for v in [(5,6),(24,19),(24,4),(24,6)]]
    u,w,beta=o[24,18],o[24,5],o[18,16]
    assert aa=={A,B,C,D} and not d[3][A]
    assert set(d[1][B])=={(24,19),(12,14)}
    assert set(d[1][D])=={(24,4),(14,11)}
    P,L,R,U,W=[d[3][i] for i in (B,D,C,u,w)]
    assert list(map(len,(P,L,R,U,W)))==[5,16,6,4,9]
    ident=lambda b,c:meta['owner'][b,c]
    coordinates=[[(5,[10,12]),(6,[12,15,16])],
        [(5,[10,12]),(6,[12]),(7,[5,6,7,9,10,13,15]),(8,[5,7,8,9,10,11])],
        [(12,[7,12,13,14,15,16])],[(7,[13,15]),(9,[13,14])],
        [(9,[8,9,10,13,14]),(10,[12,13,14,15])]]
    for group,rows in zip((P,L,R,U,W),coordinates):
        assert group=={ident(b,c) for b,cols in rows for c in cols}
    old_owner=owner_data(*od[:2])[0]
    assert L==od[3][old_owner[5,4]]|od[3][old_owner[5,5]]
    assert P==od[3][old_owner[5,19]]|od[3][old_owner[5,18]]
    assert P&L=={ident(5,10),ident(5,12),ident(6,12)}
    assert L&U=={ident(7,13),ident(7,15)}
    assert U&W=={ident(9,13),ident(9,14)}
    assert not (P&(U|W|R) or L&(W|R) or R&(U|W))
    assert U<=(L|W) and d[3][beta]<=W
    reach={a:distance(d,a) for a in aa}
    assert not set(reach[D])&bb
    assert set(reach[B])=={B,u,beta,o[24,20]}
    assert set(reach[D])=={D,w,o[24,3]}
    assert set(reach[C])=={C,u,w,beta}
    assert not d[3][o[24,20]] and not d[3][o[24,3]]
    for a,expected in [(B,{(B,u),(u,beta),(B,o[24,20])}),
                       (D,{(D,w),(D,o[24,3])}),
                       (C,{(C,u),(C,w),(u,beta)})]:
        transitions={(o[x],o[y]) for x,y in d[2] if o[x] in reach[a] and o[x]!=o[y]}
        assert transitions==expected
    private=o[5,16]
    assert ((5,17),(5,16)) in d[2] and private in bb
    assert {a for a in aa if private in reach[a]}=={A}
    assert not any(p['kind']=='fork' for p in primitive_certificates(*d))
    # Check both tail surgeries independently of the terminal-only model.
    _,old_comp=independent_strands(old,whole_bands(old))
    _,new_comp=independent_strands(cur,whole_bands(cur))
    body=lambda comps,tip:next(b for ts,b in comps if tip in ts)
    for x,y,z,root,length in [((5,4),(5,5),{(5,4),(5,5)},(24,4),40),
                             ((5,19),(5,18),{(5,19),(5,18)},(24,19),42)]:
        assert body(new_comp,root)==(body(old_comp,x)|body(old_comp,y))-z
        assert body(new_comp,x)==z and len(body(new_comp,root))==length
    return cur,d,meta,(P,L,R,U,W)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    cur,d,meta,classes=model();P,L,R,U,W=classes
    totals=Counter();rng=random.Random(2026102541)
    # All arbitrary five-support assignments on two original identities;
    # plus random three-identity systems. These do not assume physical overlap.
    for mask in range(1<<10):
        gs=[{j for j in range(2) if mask>>(2*i+j)&1} for i in range(5)]
        assert prediction(gs,{0,1})==brute_interface(gs,{0,1})
        totals['abstract_arbitrary_support_models']+=1
    for _ in range(256):
        gs=[{j for j in range(3) if rng.randrange(2)} for _ in range(5)]
        assert prediction(gs,set(range(3)))==brute_interface(gs,set(range(3)))
        totals['abstract_arbitrary_support_models']+=1
    incidence=[P-L,P&L,L-(P|U),L&U,U&W,W-U,R]
    assert list(map(len,incidence))==[2,3,11,2,2,7,6]
    choices=[[set(sorted(E)[:n]) for n in range(min(3,len(E))+1)] for E in incidence]
    pools=[set().union(set(),*parts) for parts in itertools.product(*choices)]
    pools += [set(s) for n in (0,1,2) for s in itertools.combinations(sorted(d[4]),n)]
    pools += [d[4]]+[{j for j in d[4] if rng.randrange(2)} for _ in range(160)]
    for i,Q in enumerate(pools):
        answer=fork_flow(*clipped(d,Q));expected=prediction(classes,Q)
        assert (answer['value'],answer['cost'])==expected
        if i<96 or i>=len(pools)-32:
            for forks in (False,True):
                brute=optimize(*clipped(d,Q),allow_forks=forks)
                assert (brute['value'],brute['cost'])==expected
                totals['independent_complete_ordinary_full_packs']+=1
            assert brute_interface(classes,Q)==expected
            totals['independent_abstract_route_packs']+=1
        totals['complete_original_availability_models']+=1
    ident=lambda b,c:meta['owner'][b,c]
    named={}
    for name,Q in [('empty',set()),('one_Z',{ident(5,10)}),('two_Z',{ident(5,10),ident(5,12)}),
        ('two_X',{ident(7,13),ident(7,15)}),('two_Y',{ident(9,13),ident(9,14)}),
        ('two_W_only',{ident(9,8),ident(9,9)}),('R_and_P',{ident(12,7),ident(6,15)}),
        ('L_and_R',{ident(7,5),ident(12,7)}),('L_and_W',{ident(7,5),ident(9,8)}),('all',d[4])]:
        answer=fork_flow(*clipped(d,Q));named[name]=dict(value=answer['value'],cost=answer['cost'])
        assert (answer['value'],answer['cost'])==prediction(classes,Q)
    # Relax only the actual route entrance constraints: ordinary matching
    # to individually reachable resources overstates BOTH physical controls.
    own,alphas,betas,_=owner_data(*d[:2])
    for label,Q in [('two_X',{ident(7,13),ident(7,15)}),
                    ('two_W_only',{ident(9,8),ident(9,9)})]:
        access={}
        for a in alphas:
            reach=set(distance(d,a))
            access[a]={('beta',b) for b in reach&betas}|{
                ('interval',j) for b in reach for j in d[3][b]&Q}
        assigned={}
        def augment(a,seen):
            for j in sorted(access[a]):
                if j in seen:continue
                seen.add(j)
                if j not in assigned or augment(assigned[j],seen):
                    assigned[j]=a;return True
            return False
        rank=sum(augment(a,set()) for a in sorted(alphas))
        assert rank==4 and named[label]['value']==3
        named[label]['individual_reachability_matching_value']=rank
        totals['strict_reachability_matching_overestimates']+=1
    for vr,hz in itertools.product((False,True),repeat=2):
        mv=lambda v:(27-v[0] if vr else v[0],23-v[1] if hz else v[1])
        image=(*cur[:2],{mv(v) for v in cur[2]},[tuple(mv(v) for v in e) for e in cur[3]])
        assert feasible(image) and frozen(image)
        dd,_,_=whole_support_data(image,whole_bands(image))
        assert (fork_flow(*clipped(dd,set()))['value'],fork_flow(*dd)['value'])==(2,4)
        totals['actual_frozen_reflections']+=1
    result=dict(status='PASS',shape=cur[:2],selected=49,matching=154,endpoints=308,
        freezing_layers=48,source_counts=dict(alpha=4,beta=6,mixed=15),
        class_sizes=dict(P=5,L=16,R=6,U=4,W=9,Z=3,X=2,Y=2),totals=dict(totals),named=named,
        scope='Actual two switches on SAME frozen board: beta-only V2/c3, full original V4/c1. General arbitrary-support three-source/two-gate shared-beta value and exact-cost theorem, all original Q. Different units do not suffice when beta/interval exits share U or interval routes share W. Universal rematching compensation and5over6 OPEN.')
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
