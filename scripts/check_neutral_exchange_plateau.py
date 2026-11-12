"""Standalone physical/certificate audit of an unbounded neutral-exchange plateau."""
from pathlib import Path
from itertools import product,permutations
from collections import Counter
import argparse,json,random,hashlib
if not __debug__:raise RuntimeError('Assertions must be enabled')
ROOT=Path(__file__).resolve().parents[1];counts=Counter();rng=random.Random(13112611);examples=[];digest=hashlib.sha256()

def model(m):
 n=8*m;P=[(v,v+1) for v in range(0,n,2)];Q=[(v,(v+1)%n) for v in range(1,n,2)]
 Cs=[]
 for j in range(m):
  a=8*j;Cs += [[a,a+6,a+1,a+7],[a+2,a+4,a+3,a+5]]
 B=[e for K in Cs for e in zip(K,K[1:]+K[:1])]
 U={8*j+t for j in range(m) for t in (1,2,3,6)};C={8*j+2 for j in range(m)}
 return n,P,Q,Cs,B,U,C

def permitted(n,B,U):
 S=set(range(n))-U;degree={v:0 for v in S}
 for a,b in B:
  if a in S and b in S:degree[a]+=1;degree[b]+=1
 return all(d<=1 for d in degree.values())

def matching(n,U):
 missing=min(set(range(n))-U);M=[];pending=None
 for t in range(1,n+1):
  v=(missing+t)%n
  if v not in U:pending=None
  elif pending is None:pending=v
  else:M.append((pending,v));pending=None
 return M

def isolate(U,X,Y,E):
 V=(U-X)|Y
 return not any((a in Y and b in V) or (b in Y and a in V) for a,b in E)

for m in list(range(1,25))+[32,64,128]:
 n,P,Q,Cs,B,U,C=model(m);E=P+Q;M=matching(n,U);even=set(range(0,n,2));odd=set(range(1,n,2))
 assert len(U)==4*m and len(M)==len(C)==m and all(a in C or b in C for a,b in E if a in U and b in U)
 assert all(len(set(K)&U)==2 for K in Cs) and permitted(n,B,U)
 assert permitted(n,B,even) and permitted(n,B,odd) and not matching(n,even)
 assert len(U-even)==len(U-odd)==2*m
 for j in range(m):
  for a,c in [(8*j,8*j+1),(8*j+4,8*j+3),(8*j+5,8*j+6),(8*j+7,8*j+6)]:
   assert a not in U and c in U-C and tuple(sorted((a,c))) in {tuple(sorted(e)) for e in E}
   counts['persistent_addition_blockers']+=1
 local=[];swaps=[]
 for K in Cs:
  initial=U&set(K);options=[initial]
  for x in sorted(initial):
   for y in sorted(set(K)-U):
    V=(U-{x})|{y};assert permitted(n,B,V) and len(matching(n,V))>=m
    counts['legal_single_owner_nonimprovements']+=1
    options.append((initial-{x})|{y})
  local.append(options)
 for j in range(m):swaps += [(8*j+1,8*j),(8*j+3,8*j+4)]
 schedules=list(permutations(range(2*m))) if m<=3 else [tuple(range(2*m)),tuple(reversed(range(2*m)))]+[tuple(rng.sample(range(2*m),2*m)) for _ in range(8)]
 for order in schedules:
  V=set(U);cost=m;deltas=[]
  for i in order:
   x,y=swaps[i];assert x in V and y not in V;V=(V-{x})|{y};assert permitted(n,B,V)
   now=len(matching(n,V));deltas.append(now-cost);cost=now
  assert V==even and cost==0 and deltas.count(0)==deltas.count(-1)==m and deltas.count(1)==0
  counts['route_prefixes']+=2*m;counts['route_orders']+=1
 # Reconstruct actual physical graph and all-helper independent certificate.
 b=4*m;G=[set() for _ in range(5*b)]
 def edge(a,c):G[a].add(c);G[c].add(a)
 for i,(a,c) in enumerate(P):edge(i,b+a);edge(i,b+c)
 for v in range(n):edge(b+v,3*b+v)
 for a,c in Q:edge(b+a,b+c)
 for a,c in B:edge(3*b+a,3*b+c)
 colour=[1-((a//2)%2) for a,c in P]+[(v//2)%2 for v in range(n)]+[1-(v//2)%2 for v in range(n)]
 assert min(map(len,G))==2 and max(map(len,G))==3
 assert all(colour[v]!=colour[w] for v in range(5*b) for w in G[v])
 D=set(range(b))|{b+v for v in even}|{3*b+v for v in set(range(n))-even}
 assert len(D)==12*m and all(len(G[v]&D)<=1 for v in D)
 counts['physical_zero_cost_certificates']+=1
 if m<=8:
  for removed in range(5*b):
   V=set(range(5*b))-{removed};seen={min(V)};todo=list(seen)
   while todo:
    for w in (G[todo.pop()]&V)-seen:seen.add(w);todo.append(w)
   assert seen==V;counts['physical_point_deletion_connectivity']+=1
 if m<=3:
  best=4*m;rule=m;zero=0;valid=0
  for parts in product(*local):
   V=set().union(*parts);assert len(V)==len(U) and permitted(n,B,V)
   X=U-V;Y=V-U;cost=len(matching(n,V));best=min(best,cost)
   if cost==0:zero+=1;assert V in (even,odd)
   if isolate(U,X,Y,E) and len(matching(n,U-X))==m-len(X):
    assert not X and not Y;valid+=1;rule=min(rule,cost)
   counts['literal_owner_outcomes']+=1
  assert best==0 and rule==m and zero==2 and valid==1
  examples.append(dict(m=m,initial_cost=m,best_exact_deletion_cost=rule,actual_best=best,zero_outcomes=zero,route=swaps))
  counts['literal_rule_and_actual_optima']+=1
 digest.update(json.dumps([m,sorted(U),sorted(C),swaps],sort_keys=True).encode());counts['family_scales']+=1
report=dict(scope='Standalone standard library. Every local owner outcome at m1,2,3; every route permutation there, all single-owner swaps and explicit physical certificates throughm128, point-deletion connectivity throughm8. General proof distinguishes nonincreasing from arbitrary routes.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/neutral-exchange-plateau-check.json'));args=p.parse_args()
Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
