"""Coordinate checks for the written complete two-port matching classification.
Finite enumeration checks the geometric adapter, never replaces its all-length proof.
"""
if not __debug__: raise RuntimeError('Assertions required; do not use -O.')
import argparse,json
from collections import Counter
from itertools import combinations
from pathlib import Path
from check_frozen_half_area_attainers import frozen_family
from check_endpoint_invasion_sharp_strips import edge_key,endpoints
from check_ambient_band_port_activation import local_closure,check_trap,CAP_T,CAP_M
from check_frozen_equality_matching_rigidity import first_times
from check_cooperative_promotion import neighbors
from check_residual_corridors import direct_check
from check_frozen_half_area_attainers import exact_tile_payment

def candidate(m,r,kind):
 h,w,T,original=frozen_family(m);P=endpoints(original);M=[];used=set()
 def add(a,b):
  assert a in P and b in P and a not in used and b not in used,(m,r,kind,a,b)
  M.append(edge_key((a,b)));used.update((a,b))
 add((1,1),(2,1))
 for j in range(m+1):
  s=6*j;A=(1,5+s);B=(1,6+s);C=(1,7+s);D=(2,7+s);E=(2,6+s);F=(3,6+s);U=(2,5+s);V=(3,5+s);G=(3,7+s)
  add(E,F)
  for a,b in ([(A,B),(C,D),(U,V)] if j<r else [(A,U),(B,C),(D,G)]):add(a,b)
 # R suffix backbone
 for j in range(r,m+1):add((3,8+6*j),(3,9+6*j))
 for j in range(r,m):add((3,10+6*j),(3,11+6*j))
 # Prefix, with transition modification at r-1, or terminal modifier.
 for j in range(min(r,m+1)):
  s=6*j;G=(3,7+s);H=(3,8+s);g=(3,9+s);b=(3,10+s)
  if j==r-1 and r<=m:
   v=(3,11+s)
   if kind=='V':add(G,H);add(g,b);add(v,(4,11+s))
   elif kind=='gA':add(G,H);add(g,(4,9+s));add(b,v)
   elif kind=='gB':add(G,H);add(g,(4,9+s));add(b,(4,10+s));add(v,(4,11+s))
   elif kind=='GA':add(G,(4,7+s));add(H,g);add(b,v)
   elif kind=='GB':add(G,(4,7+s));add(H,(4,8+s));add(g,(4,9+s));add(b,v)
   else:assert False,kind
  elif j==m:
   Q=(4,9+s)
   if kind=='canonical':add(G,H);add(g,Q)
   elif kind=='square':add(G,(4,7+s));add(H,(4,8+s));add(g,Q)
   elif kind=='tail':add(G,(4,7+s));add(H,g)
   else:assert False
  else:add(G,H);add(g,b)
 if r==0:add((3,5),(4,5))
 # Remaining row4 intervals have unique path perfect matching.
 remaining=sorted(P-used)
 while remaining:
  a=remaining.pop(0);b=remaining.pop(0);assert a[0]==b[0]==4 and b[1]==a[1]+1,(m,r,kind,a,b)
  add(a,b)
 assert used==P
 return h,w,T,M

def all_candidates(m):
 yield 'full',0,candidate(m,0,'V')
 for r in range(1,m+1):
  for kind in ['V','gA','gB','GA','GB']:yield kind,r,candidate(m,r,kind)
 for kind in ['canonical','square','tail']:yield kind,m+1,candidate(m,m+1,kind)


def odd_rungs(M):
 return sorted(a[1] for a,b in M if a[1]==b[1] and {a[0],b[0]}=={3,4} and a[1]%2)

def white_tail(P,x):
 S={v for v in P if sum(v)%2 and v[1]>x}
 if x%6==5:S.add((2,x))
 return S

def white_sequence(m,kind,r,cur):
 """Literal ordered waves from Section 5; no search for an activation order."""
 h,w,T,M=cur;mate={v:u for e in M for v,u in (e,e[::-1])};P=set(mate);frozen=set();rec=[]
 def take(v):
  if v in frozen:return
  assert v in P and sum(v)%2
  kept=T|{(4,w)}|{mate[z] for z in frozen}
  support=sorted(set(neighbors(v))&kept)
  assert len(support)>=2,(m,kind,r,v,support)
  rec.append((v,support[:2]));frozen.add(v)
 def core(j):
  s=6*j
  return (3,6+s),(2,5+s),(1,6+s),(2,7+s),(3,8+s)
 take((2,1));take((4,w-1));take((4,5))
 roots=odd_rungs(M);first=(roots[0]-5)//2;last=(roots[-1]-5)//2;n=3*m+2
 for l in range(first+1):take((4,5+2*l))
 for l in range(n-1,last-1,-1):take((4,5+2*l))
 if len(roots)==2:take((3,roots[0]+1))
 if r<=m:
  if r:
   j=r-1;s=6*j
   if kind=='V':take((3,10+s));take((3,8+s))
   elif kind in {'gA','gB'}:take((3,8+s));take((3,10+s))
   elif kind in {'GA','GB'}:take((3,8+s));take((3,10+s));take((3,6+s))
  for j in range(r,m+1):
   F,U,B,D,H=core(j)
   for v in [F,U,B,D,H]:take(v)
   if j<m:take((3,10+6*j))
 else:
  take((3,8+6*m))
  if kind in {'square','tail'}:take((3,6+6*m))
 for j in range(min(r-1,m),-1,-1):
  F,U,B,D,H=core(j)
  for v in [H,F,D,B,U]:take(v)
  if j:take((3,4+6*j));take((3,2+6*j))
 assert frozen=={v for v in P if sum(v)%2}
 return rec

def verify_candidate(m,kind,r,cur,stats,synchronous=False):
 h,w,T,M=cur;P=endpoints(M);old=frozen_family(m);canonical=set(map(edge_key,old[3]));assert P==endpoints(old[3]) and T==old[2]
 direct_check(*cur);stats['candidate_boards']+=1
 roots=odd_rungs(M);assert len(roots)==1 or len(roots)==2 and roots[1]-roots[0]==2
 B=set() if kind=='canonical' else {(3,w-1),(4,w-2)}
 W=set() if kind=='canonical' else white_tail(P,roots[0])
 if B:
  check_trap(T,M,B,{(4,w)});check_trap(T,M,W,{(3,w)});stats['exact_response_traps']+=2
 k=m-r+1
 d=0 if kind=='canonical' else 2 if kind=='square' else 3 if kind=='tail' else 8*m+7 if r==0 else 8*k-1 if kind=='V' else 8*k+1 if kind.startswith('g') else 8*k+3
 nw=0 if kind=='canonical' else 2 if kind in {'square','tail'} else 9*m+7 if r==0 else 9*k-2 if kind=='V' else 9*k if kind.startswith('g') else 9*k+2
 assert len(canonical-set(M))==d and len(W)==nw
 stats['white_strict_sequence_events']+=len(white_sequence(m,kind,r,cur))
 for p,q in [(False,False),(True,False),(False,True),(True,True)]:
  grants=({(3,w)} if p else set())|({(4,w)} if q else set())
  expected=P-(set() if p else B)-(set() if q else W)
  times=first_times((h,w,T|grants,M));assert set(times)==expected
  # Independent strict actual-mate certificate reconstructed from queue times.
  mate={v:u for e in M for v,u in (e,e[::-1])}
  for v,t in times.items():
   supports=[u for u in neighbors(v) if u in T|grants or u in mate and mate[u] in times and times[mate[u]]<t]
   assert len(supports)>=2
  if synchronous:
   assert local_closure(T,M,grants)[0]==expected;stats['independent_synchronous_responses']+=1
  stats['exact_interface_responses']+=1;stats['strict_rank_events']+=len(times)
 if synchronous:
  shift=lambda v:(v[0],v[1]+w)
  ambient=(h,w+6,T|{shift(v) for v in CAP_T},M+[(shift(a),shift(b)) for a,b in CAP_M])
  direct_check(*ambient);assert set(first_times(ambient))==endpoints(ambient[3]);assert len(ambient[2])+len(ambient[3])==h*(w+6)//2
  stats['fully_frozen_ambient_boards']+=1
 # Fixed T/P implies physical charges and the SAME inherited token bijection.
 if kind=='canonical':exact_tile_payment(m,cur,stats)
 return frozenset(M)

def exhaustive(m,stats):
 h,w,T,original=frozen_family(m);P=endpoints(original);c=w-1;canonical=set(map(edge_key,original))
 expected={frozenset(cur[3]) for _,_,cur in all_candidates(m)}
 forced=[((1,1),(2,1))]+[((2,6+6*j),(3,6+6*j)) for j in range(m+1)]
 vs=sorted(P-{v for e in forced for v in e});index={v:i for i,v in enumerate(vs)};adj=[sum(1<<index[u] for u in neighbors(v) if u in index) for v in vs];accepted=set();count=0
 def visit(mask,es):
  nonlocal count
  if not mask:
   M=forced+es;mate={v:u for e in M for v,u in (e,e[::-1])};roots=odd_rungs(M);assert roots
   count+=1;stats['exhaustive_reduced_matchings']+=1
   eligible=len(roots)==1 or len(roots)==2 and roots[1]-roots[0]==2
   actual=frozenset(map(edge_key,M));assert eligible==(actual in expected)
   f=set(first_times((h,w,T|{(3,w),(4,w)},M)));assert (f==P)==eligible
   if f==P:accepted.add(actual)
   for x in roots:
    if x<c:check_trap(T,M,white_tail(P,x),{(3,w)});stats['universal_tail_traps']+=1
   for x,z in combinations(roots,2):
    if z-x>=4:
     S={v for v in P if sum(v)%2 and x<v[1]<z};check_trap(T,M,S,{(3,w),(4,w)});stats['universal_interval_traps']+=1
   return
  _,i,nb=min((int.bit_count(adj[i]&mask),i,adj[i]&mask) for i in range(len(vs)) if mask>>i&1)
  while nb:
   one=nb&-nb;nb-=one;j=one.bit_length()-1;visit(mask^(1<<i)^one,es+[(vs[i],vs[j])])
 visit((1<<len(vs))-1,[]);assert accepted==expected
 return dict(m=m,reduced_matchings=count,accepted=len(accepted))

def main():
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args();stats=Counter();lengths=list(range(2,21))+[25,40]
 for m in lengths:
  generated={verify_candidate(m,kind,r,cur,stats,m<=5 or m==25) for kind,r,cur in all_candidates(m)}
  assert len(generated)==5*m+4
  print(json.dumps(dict(m=m,candidates=len(generated))),flush=True)
 ex=[exhaustive(m,stats) for m in [2,3,4]]
 result=dict(status='PASS',lengths=lengths,counts=dict(stats),exhaustive=ex,scope='Literal white wave sequence, exact four-state closures, strict actual-mate certificates, interval/tail traps for all reduced matchings m2..4, 215 candidate ambient cap unions, unchanged physical token bijections.',proof='docs/TWO_PORT_MATCHING_CLASSIFICATION.md',limits='Finite controls verify the written geometric adapter; they do not replace its arbitrary-length proof. EF-absent matchings are excluded by the written three-endpoint trap, not by the reduced enumeration.')
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
if __name__=='__main__':main()
