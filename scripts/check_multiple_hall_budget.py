#!/usr/bin/env python3
"""Literal terminal-bijection checks; no geometric-routing imports."""
import itertools,json,math,pathlib,random
rng=random.Random(20261111)
counts=dict(graphs=0,saturating_graphs=0,tight_sets=0,potential_choices=0,terminal_checks=0,weighted_identities=0)
for b in range(1,4):
 t=b+1
 matrices=range(1<<(b*t)) if b<=2 else sorted({rng.randrange(1<<(b*t)) for _ in range(32)}|{sum(1<<(j*t+j) for j in range(b))})
 for bits in matrices:
  counts['graphs']+=1
  ns=[{i for i in range(t) if bits>>(j*t+i)&1} for j in range(b)]
  match=next((m for m in itertools.permutations(range(t),b) if all(m[j] in ns[j] for j in range(b))),None)
  if match is None:continue
  counts['saturating_graphs']+=1
  tight=[]
  for mask in range(1,1<<b):
   D={j for j in range(b) if mask>>j&1};F=set().union(*(ns[j] for j in D))
   if len(F)==len(D):tight.append((D,F))
  counts['tight_sets']+=len(tight)
  choices=[[(i,1)] for i in range(len(tight))]
  choices += [[(i,1),(j,l)] for i in range(len(tight)) for j in range(i+1,len(tight)) for l in (1,2)]
  if len(tight)>2:choices.append([(i,1+i%3) for i in range(len(tight))])
  for choice in choices:
   pb=[sum(w for j,w in choice if v in tight[j][0]) for v in range(b)]
   pt=[sum(w for j,w in choice if v in tight[j][1]) for v in range(t)]
   mu=max(pb);assert max(pt)==mu and sum(pt)==sum(pb)
   assert all(pt[v]>=pb[j] for j in range(b) for v in ns[j])
   counts['potential_choices']+=1
   for r in (1,2,3) if b<=2 else (1,2):
    black=b+r
    for pi in itertools.permutations(range(black)):
     k=sum(v>=b for v in pi[:t]);assert k>=1
     hh=[v for v in pi[t:] if v<b];assert len(hh)==k-1
     A=B=q=R=0
     for v,dest in enumerate(pi[:t]):
      p=pb[dest] if dest<b else 0
      A+=max(0,pt[v]-p);B+=max(0,p-pt[v]);q+=p>pt[v]
      if p>pt[v]:assert dest<b and v not in ns[dest]
      if dest>=b:R+=pt[v]
     assert A-B==sum(pb[v] for v in hh)
     assert 0<=A-B<=(k-1)*mu
     assert q>=max(0,math.ceil((A-(k-1)*mu)/mu))>=max(0,math.ceil((R-(k-1)*mu)/mu))
     assert 0<=max(0,math.ceil((R-(k-1)*mu)/mu))<=1
     nontrivial=sum(dest>=b or v not in ns[dest] for v,dest in enumerate(pi[:t]))
     assert nontrivial>=k+max(0,math.ceil((A-(k-1)*mu)/mu))
     counts['terminal_checks']+=1;counts['weighted_identities']+=len(choice)
# Two distinct overlapping tight regions, one reused HH endpoint.
D=[{0,1},{1,2}];F=[{0,1},{1,2}];pi=[4,3,2,0,1];t=4;b=3
abc=[]
for d,f in zip(D,F):
 a=sum(pi[v] not in d for v in f)
 bv=sum(v not in f and pi[v] in d for v in range(t))
 c=sum(v in d for v in pi[t:]);assert a==bv+c;abc.append((a,bv,c))
assert abc==[(2,1,1),(1,0,1)]
assert sum(v[2] for v in abc)==2 and len(pi[t:])==1
# Exterior withdrawals carry information beyond centre withdrawals.
pt=[1,1,0,0];pb=[1,1,0];pi=[3,2,0,1]
A=sum(max(0,pt[t]-(pb[v] if v<3 else 0)) for t,v in enumerate(pi))
Bc=sum(max(0,(pb[v] if v<3 else 0)-pt[t]) for t,v in enumerate(pi))
assert A==Bc==2
report={'status':'PASS',**counts,'overlap_countermodel':{'region_counts':abc,'exterior_HH_paths':1,'unnormalized_inequality_false':True},'exterior_withdrawal_example':{'k':1,'A_tot':2,'B_tot':2,'strong_expense_bound':3},'scope':'Abstract endpoint bijections only; no physical grid realization asserted.'}
path=pathlib.Path('output/multiple-hall-budget-controls.json');path.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
