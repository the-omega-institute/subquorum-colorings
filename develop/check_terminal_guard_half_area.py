"""Exact controls for the written terminal-guard half-area theorem.

Standard library only. Finite controls check the proof; they do not prove its
all-length scope. The discovery optimizer is not needed to replay this file.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_boundary_withdrawal_compensation import AP,domain,pocket_bound,random_model
from check_connected_band_integer_compensation import module,weight
from check_endpoint_invasion_sharp_strips import endpoints,free_vertices
from check_cooperative_promotion import neighbors
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_selection_withdrawal_sharp_strips import attaining

if not __debug__: raise RuntimeError('Assertions required; do not use -O.')

LEFT_T = [(0, 1),
 (0, 3),
 (0, 5),
 (1, 2),
 (1, 4),
 (2, 0),
 (2, 3),
 (3, 1),
 (3, 3),
 (4, 0),
 (4, 2),
 (4, 4),
 (5, 3),
 (5, 5)]
LEFT_M = [((1, 1), (2, 1)), ((1, 5), (2, 5)), ((3, 5), (4, 5)), ((5, 1), (5, 2))]

PERIOD_T = [(0, 1), (0, 3), (0, 5), (1, 2), (1, 4), (2, 3), (5, 1), (5, 3), (5, 5)]
PERIOD_M = [((1, 0), (1, 1)),
 ((1, 5), (2, 5)),
 ((2, 0), (3, 0)),
 ((2, 1), (3, 1)),
 ((3, 2), (4, 2)),
 ((3, 3), (4, 3)),
 ((3, 4), (3, 5)),
 ((4, 0), (4, 1)),
 ((4, 4), (4, 5))]

RIGHT_T = [(0, 1),
 (0, 3),
 (0, 5),
 (0, 7),
 (0, 9),
 (1, 2),
 (1, 4),
 (1, 8),
 (2, 3),
 (2, 9),
 (5, 1),
 (5, 3),
 (5, 5),
 (5, 7),
 (5, 9)]
RIGHT_M = [((1, 0), (1, 1)),
 ((1, 5), (2, 5)),
 ((1, 6), (1, 7)),
 ((2, 0), (3, 0)),
 ((2, 1), (3, 1)),
 ((2, 6), (2, 7)),
 ((3, 2), (4, 2)),
 ((3, 3), (3, 4)),
 ((3, 5), (4, 5)),
 ((3, 6), (4, 6)),
 ((3, 7), (3, 8)),
 ((3, 9), (4, 9)),
 ((4, 0), (4, 1)),
 ((4, 3), (4, 4)),
 ((4, 7), (4, 8))]

def sharp_family(m):
    assert m>=2
    chunks=[(0,LEFT_T,LEFT_M)]+[(6+6*i,PERIOD_T,PERIOD_M) for i in range(m-1)]
    chunks+=[(6*m,RIGHT_T,RIGHT_M)]
    T={(r,c+a) for a,ts,_ in chunks for r,c in ts}
    M=[tuple((r,c+a) for r,c in e) for a,_,ms in chunks for e in ms]
    return 6,6*m+10,T,M


def terminal_models(counts):
    eq=[]
    for q in itertools.product((0,1),repeat=10):
        x,y,u,w,h,A,B,C,L,K=q
        if x and not A==B==1 or y and not A==C==L==1:continue
        if u and A+B+C<2 or w and C+L<1 or h and not K==L==1:continue
        W=sum(q[:5])+5-sum(q[5:]);assert W<=5
        counts['terminal_bit_models']+=1
        if x==0 and B==1:
            counts['terminal_input_models']+=1
            if W==5:eq.append(q)
    assert eq==[(0,0,1,1,0,0,1,1,0,0)]
    counts['unique_saturated_input_patterns']=len(eq)


def chunk_checks(counts):
    degrees={}
    chunks=[('L',6,LEFT_T,LEFT_M),('B',6,PERIOD_T,PERIOD_M),('R',10,RIGHT_T,RIGHT_M)]
    for name,width,ts,ms in chunks:
        direct_check(6,width,set(ts),ms)
        P=endpoints(ms);O=set(ts)|P
        degrees[name]=[len(set(neighbors(v))&O) for v in ts]
        counts['single_chunk_controls']+=1
    status=lambda v,T,P:'T' if v in T else 'P' if v in P else '_'
    for lname,lw,lt,lm in chunks[:2]:
        for rname,rw,rt,rm in chunks[1:]:
            assert tuple(status((r,lw-1),set(lt),endpoints(lm)) for r in range(6))==('T','P','P','P','P','T')
            assert tuple(status((r,0),set(rt),endpoints(rm)) for r in range(6))==('_','P','P','P','P','_')
            T=set(lt)|{(r,c+lw) for r,c in rt}
            M=lm+[tuple((r,c+lw) for r,c in e) for e in rm]
            direct_check(6,lw+rw,T,M)
            counts['seam_controls']+=1
    return degrees


def board_control(m,cur,counts,sharp=False):
    old,Rp,P0,Up=domain(m);c=6*m+9;R=Rp-{(3,c)}
    U=free_vertices((*old[:2],R,old[3]))
    assert U==Up|{(2,c),(3,c),(4,c)} and len(U)==17*m+26
    assert len(R)==5*m+10
    assert all(not set(neighbors(v))&R for v in U)
    direct_check(*cur);T,M=cur[2:];P=endpoints(M)
    assert R<=T and P0<=P and ((T-R)|(P-P0))<=U
    nt=T-R;np=P-P0;O=nt|np
    pairs=[{(2,z),(3,z)} for i in range(m) for z in (9+6*i,11+6*i)]
    blocks=[set(sum(module(a),[])) for a in range(6,6*m+1,6)]
    E={(4,6*m+z) for z in (6,7,8,9)}|{(5,6*m+z) for z in (6,7,8,9)}|{(2,c),(3,c)}
    cover=Counter(v for S in [AP,*pairs,*blocks,E] for v in S)
    assert set(cover)==U and set(cover.values())=={1}
    L=pocket_bound(nt,np,M,counts);pairW=sum(weight(S,nt,np) for S in pairs)
    assert all(weight(S,nt,np)<=1 for S in pairs)
    b=[weight(S,nt,np) for S in blocks];assert all(w<=7 for w in b)
    a=6*m+6
    q=tuple(int(v in nt) for v in [(4,a),(4,a+2),(5,a+1),(5,a+3),(3,a+3)])
    q+=tuple(int(v not in O) for v in [(4,a+1),(5,a),(5,a+2),(4,a+3),(2,a+3)])
    x,y,u,w,h,A,B,C,LL,K=q
    assert not x or A==B==1
    assert not y or A==C==LL==1
    assert not u or A+B+C>=2
    assert not w or C+LL>=1
    assert not h or K==LL==1
    e=weight(E,nt,np);assert e==sum(q[:5])+5-sum(q[5:])<=5
    J=len(T)+len(M);WU=weight(U,nt,np)
    assert WU==L+pairW+sum(b)+e<=9*m+15
    assert J==9*m+15+WU<=18*m+30
    if J==18*m+30:
        assert L==10 and pairW==2*m and b==[7]*m and e==5
        for a in range(6,6*m+1,6):
            assert (4,a) not in nt and (5,a) not in O
            assert (5,a+5) in nt and (4,a+5) in O
        assert q==(0,0,1,1,0,0,1,1,0,0)
        assert T&old[2]==R  # Every optional old selection is absent at equality.
        counts['all_optional_old_selections_absent_at_equality']+=1
        counts['equality_pattern_controls']+=1
    plus=[];minus=[];strip=0
    for r in (0,2,4):
        for z in range(0,cur[1],2):
            S={(r+i,z+j) for i,j in itertools.product((0,1),repeat=2)}
            charge=4-2*len(T&S)-len(P&S)
            if r==0:strip+=charge
            elif charge>0:plus.extend(((r,z),i) for i in range(charge))
            elif charge<0:minus.extend(((r,z),i) for i in range(-charge))
    assert strip==-m and len(plus)-len(minus)-m==cur[0]*cur[1]-2*J
    demands=[('exterior',v) for v in minus]+[('strip',i) for i in range(m)]
    assert len(plus)>=len(demands) and len(set(plus[:len(demands)]))==len(demands)
    counts['token_injections']+=1
    if sharp:
        assert J==18*m+30 and len(T)==9*m+20 and len(M)==9*m+10
        assert len(plus)==len(demands)
        assert (5,1) in P and set(neighbors((5,1)))&(T|P)=={(5,2)}
        frozen,_=frozen_certificate(cur);assert (5,1) not in frozen and frozen!=P
        counts['sharp_all_length_formula_controls']+=1
    if (3,c) not in T:counts['terminal_guard_actually_absent']+=1
    if not {tuple(sorted(e)) for e in old[3]}<={tuple(sorted(e)) for e in M}:
        counts['models_changing_old_matching']+=1
    counts['actual_board_controls']+=1
    return dict(m=m,J=J,pocket=L,pairs=pairW,blocks=b,terminal=e,unspent_half_tokens=len(plus)-len(demands))


def main():
    p=argparse.ArgumentParser();p.add_argument('--max-m',type=int,default=40)
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();terminal_models(counts);degrees=chunk_checks(counts)
    records=[]
    lengths=sorted(set(range(2,args.max_m+1))|{64,100})
    for m in lengths:records.append(board_control(m,sharp_family(m),counts,True))
    for m in [2,3,4,8]:
        inherited=attaining(m+1,set(range(m)))
        assert frozen_certificate(inherited)[0]==endpoints(inherited[3])
        board_control(m,inherited,counts)
        counts['inherited_frozen_attainers']+=1
        for seed in range(12):board_control(m,random_model(m,1000*m+seed),counts)
    report=dict(status='PASS',theorem='Every m>=2: exact unrestricted actual-matching maximum 18m+30=area/2 after terminal guard withdrawal.',
        proof='Written all-length terminal inequality, coordinate partition, disjoint chunk gluing and counts; enumeration checks only.',
        frozen_scope='Sharp half-area family is not completely frozen; completely frozen optimum remains one of 18m+29 and 18m+30.',
        counts=dict(counts),chunk_selected_degrees=degrees,sharp_records=records)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('sharp_records',)}))

if __name__=='__main__':main()
