"""Independent coordinates, all small owner outcomes and neutral exchange schedules."""
from pathlib import Path
from itertools import product,combinations,permutations
from collections import Counter
import argparse,json,random,hashlib
if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1];counts=Counter();rng=random.Random(13112610);examples=[];digest=hashlib.sha256()

def model(r):
 n=4*r;P=[(v,v+1) for v in range(0,n,2)];Q=[(v,(v+1)%n) for v in range(1,n,2)]
 Cs=[[2*i,2*r+2*(i^1),2*i+1,2*r+2*(i^1)+1] for i in range(r)]
 B=[e for K in Cs for e in zip(K,K[1:]+K[:1])];U=set(range(1,2*r))|{2*r+2}
 return n,P+Q,Cs,B,U

def permitted(n,B,U):
 S=set(range(n))-U
 return all(sum(v in e and set(e)<=S for e in B)<=1 for v in S)

def matching(n,U):
 # Break the cycle at a missing point; greedily pair consecutive points of
 # every selected run. Each run is a path, so floor(run length/2) is exact.
 missing=min(set(range(n))-U);M=[];pending=None
 for t in range(1,n+1):
  v=(missing+t)%n
  if v not in U:pending=None
  elif pending is None:pending=v
  else:M.append((pending,v));pending=None
 assert len({v for e in M for v in e})==2*len(M)
 return M

def isolated(U,X,Y,E):
 V=(U-X)|Y
 return not any((a in Y and b in V) or (b in Y and a in V) for a,b in E)

for r in list(range(4,66,2))+[96,128]:
 n,E,Cs,B,U=model(r);C=set(range(2,2*r,2));even=set(range(0,n,2));odd=set(range(1,n,2))
 assert len(U)==2*r and len(matching(n,U))==r-1 and permitted(n,B,U)
 assert len(C)==r-1 and all(a in C or b in C for a,b in E if a in U and b in U)
 assert len(U-even)==len(U-odd)==r and permitted(n,B,even) and permitted(n,B,odd)
 X=set(range(4,2*r,2));Y={2*r+2*(j^1) for j in range(2,r)};V=(U-X)|Y
 assert X<=C and isolated(U,X,Y,E) and permitted(n,B,V) and len(matching(n,V))==1
 # This is an explicit cover/matching certificate for the sharp attainable1.
 assert C-X=={2} and all(a==2 or b==2 for a,b in E if a in V and b in V)
 route=[(1,0),(3,2*r)]+[(2*i+1,2*r+2*(i^1)) for i in range(2,r)]
 assert len(route)==r and len({x for x,y in route})==r and len({y for x,y in route})==r
 assert (U-{x for x,y in route})|{y for x,y in route}==even
 schedules=list(permutations(range(r))) if r<=6 else [tuple(range(r)),tuple(reversed(range(r)))]+[tuple(rng.sample(range(r),r)) for _ in range(8)]
 for order in schedules:
  V=set(U);cost=r-1;changes=[]
  for j in order:
   x,y=route[j];assert x in V and y not in V;V=(V-{x})|{y}
   assert permitted(n,B,V);new=len(matching(n,V));changes.append(new-cost);cost=new
  assert V==even and cost==0 and changes.count(-1)==r-1 and changes.count(0)==1 and changes.count(1)==0
  counts['neutral_schedule_prefix_checks']+=r;counts['neutral_schedules']+=1
 if r in (4,6):
  options=[]
  for K in Cs:
   initial=U&set(K)
   options.append([initial]+[(initial-{x})|{y} for x in sorted(initial) for y in sorted(set(K)-U)])
  best_cost=r;best_rule=r;zero=0;valid=0
  for parts in product(*options):
   V=set().union(*parts);assert len(V)==len(U) and permitted(n,B,V)
   X=U-V;Y=V-U;cost=len(matching(n,V));best_cost=min(best_cost,cost)
   if cost==0:
    zero+=1;assert V in (even,odd) and len(X)==r
   if isolated(U,X,Y,E) and len(matching(n,U-X))==(r-1)-len(X):
    best_rule=min(best_rule,cost);valid+=1
   counts['literal_owner_batch_outcomes']+=1
  assert best_cost==0 and best_rule==1 and zero==2
  counts['literal_certificate_optima']+=1
  examples.append(dict(r=r,initial_U=sorted(U),initial_cost=r-1,unrestricted_cost=best_cost,exact_rule_cost=best_rule,zero_cost_outcomes=zero,valid_rule_outcomes=valid,route=route))
 if r==4:
  zero=[]
  for S in combinations(range(n),n//2):
   V=set(S)
   if not any(a in V and b in V for a,b in E):zero.append(V)
   counts['literal_maximum_cardinality_subsets']+=1
  assert len(zero)==2 and even in zero and odd in zero
  counts['literal_independent_cycle_optima']+=1
 digest.update(json.dumps([r,sorted(U),route,sorted(X),sorted(Y)],sort_keys=True).encode());counts['family_scales']+=1
report=dict(scope='Standard-library coordinate audit; all five local outcomes per owner at r4,6, all route permutations at those scales, literal maximum-cardinality subsets of C16, explicit primal/dual certificates and random larger route orders. General proof, not extrapolated finite enumeration.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/exact-deletion-barrier-check.json'));args=p.parse_args()
Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
