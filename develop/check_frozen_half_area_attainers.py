"""Standard-library controls for the written all-length frozen half-area family.

The explicit construction and strict-rank templates are the proof. Optimizers
are used only in separate discovery material, never to validate this file.
"""
if not __debug__: raise RuntimeError("Assertions required; do not use -O.")

import argparse
from collections import Counter
import json
from pathlib import Path
from check_boundary_withdrawal_compensation import domain
from check_endpoint_invasion_sharp_strips import edge_key,endpoints
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_terminal_guard_half_area import board_control
from check_cooperative_promotion import neighbors
from check_selection_withdrawal_sharp_strips import attaining

def frozen_family(m):
 assert m>=2
 old,R,P0,U=domain(m);R-={(3,6*m+9)};c=6*m+9;n=3*m+2
 T=R|{(2,3),(3,3),(4,0),(4,2),(4,4),(5,1),(5,3)}|{(2,9+6*i) for i in range(m+1)}|{(5,z) for z in range(5,c+1,2)}
 M=list(old[3])+[((2,5+6*j),(3,5+6*j)) for j in range(m+1)]+[((3,9+6*i),(3,10+6*i)) for i in range(m)]+[((3,c),(4,c))]+[((4,5+2*j),(4,6+2*j)) for j in range(n)]
 return (*old[:2],T,M)

def certificate(m):
 n=3*m+2;c=6*m+9;rec=[]
 def add(v,r,a,b):rec.append((v,r,a,b))
 add((1,1),0,(0,1),(1,2));add((2,1),0,(2,0),(3,1))
 for j in range(m+1):
  s=6*j;A=(1,5+s);B=(1,6+s);C=(1,7+s);D=(2,7+s);E=(2,6+s);F=(3,6+s);G=(3,7+s);H=(3,8+s);U=(2,5+s);V=(3,5+s)
  add(A,0,(0,5+s),(1,4+s));add(C,0,(0,7+s),(1,8+s))
  add(E,1,B,D);add(G,2,D,F)
  add((3,9+s),3,(2,9+s),H)
  if j: add(V,4,(3,4+s),F)
  else:add(V,n+4,F,(4,5))
  r=n+1+6*(m-j)
  add(H,r,(3,9+s),(4,8+s));add(F,r+1,G,(4,6+s));add(D,r+2,E,G);add(B,r+3,C,E);add(U,r+4,A,E)
  if j:add((3,4+s),r+5,V,(4,4+s))
 for j in range(n):
  z=(4,5+2*j);v=(4,6+2*j)
  add(z,j,(5,5+2*j),(4,4+2*j))
  add(v,n+3-j,(3,6+2*j),(4,7+2*j))
 add((4,c),n,(5,c),(4,c-1))
 return rec



def verify_ranks(cur,rec,counts):
 T,M=cur[2:];P=endpoints(M);mate={v:u for e in M for v,u in (e,e[::-1])}
 rank={v:r for v,r,a,b in rec}
 assert len(rec)==len(rank)==len(P) and set(rank)==P
 for v,r,a,b in rec:
  assert a!=b and mate[v] not in (a,b)
  assert all(abs(v[0]-u[0])+abs(v[1]-u[1])==1 for u in (a,b))
  for u in (a,b):assert u in T or u in P and rank[mate[u]]<r
  counts['strict_rank_endpoint_events']+=1
 frozen,layers=frozen_certificate(cur);assert frozen==P
 counts['new_family_fully_frozen_board_checks']+=1
 return rank,layers



def exact_tile_payment(m,cur,counts):
 h,w,T,M=cur;P=endpoints(M);plus=set();minus=set()
 for r in (0,2,4):
  for c in range(0,w,2):
   S={(r+i,c+j) for i in (0,1) for j in (0,1)}
   charge=4-2*len(T&S)-len(P&S)
   expected=0
   if r==0:
    if c==0:expected=1
    elif c in {4+6*j for j in range(m+1)}:expected=-1
   elif r==2:
    if c==0:expected=-1
    elif c==4:expected=2
    elif c in {4+6*j for j in range(1,m+1)}:expected=1
   elif c==4:expected=-1
   assert charge==expected,(m,r,c,charge,expected)
   plus.update(((r,c),i) for i in range(max(charge,0)))
   minus.update(((r,c),i) for i in range(max(-charge,0)))
 payments=[(((0,0),0),((0,4),0)),(((2,4),0),((2,0),0)),(((2,4),1),((4,4),0))]
 payments += [(((2,4+6*j),0),((0,4+6*j),0)) for j in range(1,m+1)]
 assert len(payments)==len(plus)==len(minus)==m+3
 assert {v for v,_ in payments}==plus and {u for _,u in payments}==minus
 counts['explicit_full_tile_token_bijections']+=1



def terminal_port_controls(counts):
 c=21
 x=(4,c-3);A=(4,c-2);y=(4,c-1);Q=(4,c);g=(3,c);K=(2,c)
 G=(3,c-2);H=(3,c-1);u=(5,c-2);w=(5,c)
 F=(3,c-3);D=(2,c-2);Z=(4,c-4)
 region={x,A,y,Q,g,K,G,H};outside={F,D,Z}
 es=sorted({edge_key((v,z)) for v in region for z in set(neighbors(v))&(region|outside)})
 forced={edge_key(e) for e in [(g,Q),(A,y),(G,H),(x,Z)]}
 def visit(i,M,used):
  if i<len(es):
   visit(i+1,M,used);a,b=es[i]
   if not {a,b}&used:visit(i+1,M+[es[i]],used|{a,b})
   return
  if not {G,H}<=used:return
  T={u,w}|({A,Q,K}-used);O=T|used|outside
  if any(len(set(neighbors(v))&O)>1 for v in T):return
  counts['terminal_local_matching_models']+=1
  mate={v:z for e in M for v,z in (e,e[::-1])}
  if g not in used:trap={Q} if Q in used else {H}
  elif mate[g]==K:trap={K}
  elif mate[g]==H:trap={Q,H}
  else:
   assert mate[g]==Q and K in T
   if y not in used:trap={Q}
   elif mate[y]==H:trap={Q,H}
   else:
    assert mate[y]==A and mate[H]==G
    if x not in used:trap={A,Q,H}
    elif mate[x]==F:trap={x,G,y,g}
    else:
     assert mate[x]==Z
     trap=set()
  frozen=set();P=used&region
  while True:
   kept=T|{v for v,z in mate.items() if z not in region or z in frozen}|{v for v in outside if v not in mate or mate[v] in frozen}
   new={v for v in P-frozen if len(set(neighbors(v))&kept)>=2}
   if not new:break
   frozen|=new
  if trap:
   assert trap<=P
   optimistic=T|{v for v,z in mate.items() if z not in trap}|{v for v in outside if v not in mate}
   assert all(len(set(neighbors(v))&optimistic)<=1 for v in trap)
   assert not trap&frozen
   counts['explicit_terminal_trap_certificates']+=1
  else:
   assert frozen==P and forced<=set(M)
   counts['optimistically_frozen_terminal_patterns']+=1
 visit(0,[],set())
 assert counts['terminal_local_matching_models']==17
 assert counts['explicit_terminal_trap_certificates']==16
 assert counts['optimistically_frozen_terminal_patterns']==1


def main():
 p=argparse.ArgumentParser();p.add_argument('--max-m',type=int,default=40)
 p.add_argument('--output',type=Path,required=True);args=p.parse_args()
 counts=Counter();terminal_port_controls(counts);records=[]
 lengths=sorted(set(range(2,args.max_m+1))|{64,100})
 for m in lengths:
  cur=frozen_family(m);T,M=cur[2:];P=endpoints(M)
  direct_check(*cur);rank,layers=verify_ranks(cur,certificate(m),counts)
  old,R,P0,U=domain(m);R-={(3,6*m+9)}
  assert R<=T and T&old[2]==R and P0<=P
  assert {edge_key(e) for e in old[3]}<={edge_key(e) for e in M}
  assert len(T)==9*m+21 and len(M)==9*m+9 and len(P)==18*m+18
  cols={1}|{v+6*j for j in range(m+1) for v in (5,6,7)}
  expectedP={(r,c) for r in (1,2) for c in cols}|{(r,c) for r in (3,4) for c in range(5,6*m+10)}
  assert P==expectedP
  counts['explicit_endpoint_row_tables']+=1
  assert max(rank.values())==9*m+7
  # The certificate proves an upper bound on depth. This observed equality is
  # a finite control, not an asserted all-m minimal-depth theorem.
  assert len(layers)==9*m+8
  rec=board_control(m,cur,counts)
  exact_tile_payment(m,cur,counts)
  assert rec['J']==18*m+30 and rec['unspent_half_tokens']==0
  c=6*m+9;forced=[((3,c),(4,c)),((4,c-2),(4,c-1)),((3,c-2),(3,c-1)),((4,c-4),(4,c-3))]
  assert {edge_key(e) for e in forced}<={edge_key(e) for e in M}
  baseline=attaining(m+1,set(range(m)))
  direct_check(*baseline);assert frozen_certificate(baseline)[0]==endpoints(baseline[3])
  baseline_edges={edge_key(e) for e in baseline[3]}
  assert edge_key(((3,c),(4,c))) not in baseline_edges
  assert {edge_key(e) for e in old[3]}<=baseline_edges
  base=board_control(m,baseline,counts)
  assert base['J']==18*m+29 and base['unspent_half_tokens']==2
  counts['sharp_no_terminal_port_frozen_lengths']+=1
  counts['sharp_frozen_lengths']+=1
  records.append(dict(m=m,selected=len(T),matching=len(M),endpoints=len(P),
      objective=rec['J'],certificate_max_rank=max(rank.values()),
      observed_synchronous_layers=len(layers),unspent_half_tokens=0))
 for m in [2,3,8]:
  cur=frozen_family(m);h,w=cur[:2]
  for tr in [False,True]:
   for fi in [False,True]:
    for fj in [False,True]:
     shape,T,M=transformed(*cur,tr,fi,fj)
     def f(v):
      r,c=v;r=h-1-r if fi else r;c=w-1-c if fj else c
      return (c,r) if tr else (r,c)
     rec=[(f(v),r,f(a),f(b)) for v,r,a,b in certificate(m)]
     new=(*shape,T,M);direct_check(*new);verify_ranks(new,rec,counts)
     counts['isometry_controls']+=1
 result=dict(status='PASS',theorem='Every m>=2, completely frozen: J<=18m+29+epsilon where epsilon indicates actual terminal vertical edge. Both epsilon values have sharp M0-retaining frozen attainers. Half-area equality forces four terminal matching edges.',
   proof='Written coordinate construction, explicit two-witness strict-rank table and well-founded induction for arbitrary length. Finite controls do not substitute for this proof.',
   scope='No universal 5/6 counterexample. The certificate has maximum rank 9m+7; equality of the minimal synchronous depth is observed in finite controls only.',
   counts=dict(counts),records=records)
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({k:v for k,v in result.items() if k!='records'}))

if __name__=='__main__':main()
