"""All-cover catalogues and exact physical fixed-candidate optima, independently checked."""
from pathlib import Path
from itertools import product
from collections import Counter
import sys,json,random
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from cover_choice_exchange import minimum_covers as all_covers_indexed,best_cover_batch
from cover_saturated_exchange import dependency_batch
from owner_matching_certificate import prepare
from all_helper_optimization import score
from mixed_owner_bridges import _minimum_omission
counts=Counter();rng=random.Random(13112609)

def subsets(S):
 S=sorted(S)
 for m in range(1<<len(S)):yield {v for j,v in enumerate(S) if m>>j&1}

def all_covers(U,E):
 return all_covers_indexed(max(set(U)|{v for e in E for v in e},default=-1)+1,E,U)

def literal_matching(U,E):
 U=set(U);adj={v:set() for v in U};memo={}
 for a,b in E:
  if a in U and b in U:adj[a].add(b);adj[b].add(a)
 def rec(S):
  if not S:return 0
  key=tuple(sorted(S))
  if key in memo:return memo[key]
  v=min(S);best=rec(S-{v})
  for u in adj[v]&S:best=max(best,1+rec(S-{v,u}))
  memo[key]=best;return best
 return rec(U)

for n in range(7):
 p=n//2;possible=list(product(range(p),range(p,n)))
 for em in range(1<<len(possible)):
  E=[e for j,e in enumerate(possible) if em>>j&1]
  if any(sum(v in e for e in E)>2 for v in range(n)):continue
  for U in subsets(range(n)):
   covers=[C for C in subsets(U) if all(a in C or b in C for a,b in E if a in U and b in U)]
   tau=min(map(len,covers));expected={frozenset(C) for C in covers if len(C)==tau};actual=list(all_covers(U,E))
   assert len(actual)==len(expected) and {frozenset(C) for C in actual}==expected
   counts['literal_minimum_cover_catalogues']+=1

examples=[]
for n in (8,12,16):
 for trial in range(40):
  L=list(range(0,n,2));RR=list(range(1,n,2));rng.shuffle(L);rng.shuffle(RR)
  P=list(zip(L[::2],L[1::2]))+list(zip(RR[::2],RR[1::2]));rng.shuffle(RR)
  k=rng.randrange(n//2+1);Q=list(zip(L[:k],RR[:k]));B=[]
  order=[v for pair in zip(L,RR) for v in pair]
  for off in range(0,n,4):
   K=order[off:off+4];B+=list(zip(K,K[1:]+K[:1]))
  colour=[v%2 for v in range(n)];args=[n//2,P,Q,B,colour];d=prepare(*args)
  U=set().union(*(_minimum_omission(K,c) for K,c in d['owner_components']))
  if trial%3==0:U|={v for v in range(n) if rng.randrange(5)==0}
  def perm(S):
   retained=set(range(n))-S
   return all(sum(v in e and set(e)<=retained for e in B)<=1 for v in retained)
  E=P+Q;ops=[];Y=set()
  for i,(K,c) in enumerate(d['owner_components']):
   candidates=[(x,y) for x in sorted(set(K)&U) for y in sorted(set(K)-U) if perm((U-{x})|{y}) and not any((a==y and b in Y) or (b==y and a in Y) for a,b in E)]
   if candidates:
    x,y=rng.choice(candidates);ops.append([i,x,y]);Y.add(y)
  T,M=score(n,P,Q,U);default=U-T
  cover_list=list(all_covers(U,E));best=(-1,None,None);tested=0
  for C in cover_list:
   filtered=[op for op in ops if op[1] in C]
   out=dependency_batch(*args,U,filtered,C);saving=out['certificate']['saved_matching_edges'];tested+=1
   if saving>best[0]:best=(saving,C,out)
  initial=dependency_batch(*args,U,[op for op in ops if op[1] in default],default)
  actual=best_cover_batch(*args,U,ops)
  assert actual['minimum_covers_tested']==len(cover_list)
  assert actual['certificate']['saved_matching_edges']==best[0]
  nu=literal_matching(U,E);assert nu==len(M)
  literal=0
  for S in subsets(range(len(ops))):
   X={ops[j][1] for j in S};Y={ops[j][2] for j in S};new=(U-X)|Y
   if any((a in Y and b in new) or (b in Y and a in new) for a,b in E):continue
   if literal_matching(U-X,E)!=nu-len(S):continue
   assert perm(new) and literal_matching(new,E)==nu-len(S)
   literal=max(literal,len(S));counts['literal_all_cover_feasible_subsets']+=1
  assert best[0]==literal
  z=actual['certificate'];V=set(z['U']);C=set(z['cover']);matching=z['matching']
  assert len(C)==len(matching)==nu-literal and all(a in C or b in C for a,b in E if a in V and b in V)
  assert len({v for e in matching for v in e})==2*len(matching)
  assert all(set(e)<=V and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in matching)
  b=n//2;G=[set() for _ in range(5*b)]
  def edge(a,c):G[a].add(c);G[c].add(a)
  for i,(a,c) in enumerate(P):edge(i,b+a);edge(i,b+c)
  for v in range(n):edge(b+v,3*b+v)
  for a,c in Q:edge(b+a,b+c)
  for a,c in B:edge(3*b+a,3*b+c)
  D=set(range(b))|{b+v for v in z['witnesses']}|{3*b+v for v in z['owners']}
  assert len(D)==z['beta_I_lower']==3*b-nu+literal and all(len(G[v]&D)<=1 for v in D)
  counts['actual_physical_certificates']+=1
  old=initial['certificate']['saved_matching_edges']
  if best[0]>old:
   counts['strict_improvements_over_default_cover']+=1
   if len(examples)<4:examples.append(dict(b=n//2,P=P,Q=Q,B=B,colour=colour,U=sorted(U),operations=ops,default_cover=sorted(default),default_saving=old,best_cover=sorted(best[1]),best_saving=best[0],best=best[2],all_cover_result=actual))
  counts['physical_all_cover_optima']+=1;counts['physical_minimum_covers_tested']+=tested
assert examples[0]['b']==4 and examples[0]['U']==[0,2,3,6,7]
assert examples[0]['operations']==[[0,2,1],[1,6,4]]
assert examples[0]['default_cover']==[0,3] and examples[0]['default_saving']==0
assert examples[0]['best_cover']==[2,3] and examples[0]['best_saving']==1
assert examples[0]['all_cover_result']['certificate']['beta_I_lower']==11
counts['explicit_default_cover_physical_fixture']=1
# The exact deletion family is hereditary, but fails matroid augmentation.
E=[(0,1),(1,2),(2,3)];I={0};J={1,3};Cs=list(all_covers(range(4),E))
assert any(I<=C for C in Cs) and any(J<=C for C in Cs)
assert all(not any((I|{j})<=C for C in Cs) for j in J-I)
try:list(all_covers(range(3),[(0,1),(1,2),(2,0)]))
except ValueError:pass
else:raise AssertionError('Odd cycle accepted')
try:list(all_covers(range(4),[(0,1),(0,2),(0,3)]))
except ValueError:pass
else:raise AssertionError('Degree3 accepted')
counts['necessity_controls']=3
report=dict(scope='All fixed-balanced-bipartition graphs with degree<=2 through6 vertices, every induced U, all literal vertex covers;120 physical models with fixed distinct-owner candidates and independent additions, exact all-subset optima by independent literal matchings. General completeness uses proof; no polynomial all-cover or unrestricted exchange claim.',counts=dict(sorted(counts.items())),examples=examples)
import argparse
parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT/'output/cover-choice-exchange-check.json'));opt=parser.parse_args()
Path(opt.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(report['counts'],sort_keys=True))
