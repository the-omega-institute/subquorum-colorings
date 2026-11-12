"""Independent literal checks of shared odd budgets, final repair and physical family."""
from pathlib import Path
from itertools import combinations,product,permutations
from collections import Counter
from functools import lru_cache
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from odd_path_neutral_budget import compile_budget,grouped_optimum,repair_batch,physical_budget_batch,shared_path_family
from matching_choice_exchange import choose_matching,best_initial_pair_batch
from all_helper_optimization import score
from owner_matching_certificate import prepare
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();examples=[]

def subsets(V):
 V=sorted(V)
 for mask in range(1<<len(V)):yield {v for j,v in enumerate(V) if mask>>j&1}

def matchings(V,E):
 V=set(V)
 if not V:yield [];return
 v=min(V)
 yield from matchings(V-{v},E)
 for a,b in E:
  w=b if a==v else a if b==v else None
  if w is not None and w in V:
   for M in matchings(V-{v,w},E):yield [(v,w)]+M

def maximum(V,E):
 Ms=list(matchings(V,E));k=max(map(len,Ms));return [M for M in Ms if len(M)==k]

def verify(n,E,U,C,M,ops,S):
 out=repair_batch(n,E,U,C,M,ops,S);V=set(out['U']);F=set(out['cover']);actual=maximum(V,E)[0]
 assert len(out['matching'])==len(F)==len(actual)==out['actual_cost']
 assert len({v for e in out['matching'] for v in e})==2*len(actual)
 assert all(set(e)<=V and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in out['matching'])
 assert all(a in F or b in F for a,b in E if a in V and b in V)
 assert all(not set(e)&set(out['added']) for e in E if set(e)<=V)
 seen=set();charges=set()
 for region in out['repair_regions']:
  K=set(region['vertices']);e=tuple(region['charged_initial_edge']);assert not K&seen;seen|=K
  assert len(region['old_cover'])==len(region['new_cover'])+1
  assert e in {tuple(sorted(f)) for f in M} and set(e)&K and set(e)&set(out['removed']) and e not in charges
  charges.add(e)
 assert len(charges)==out['credit']==len(C)-len(actual)
 digest.update(json.dumps(out,sort_keys=True).encode());counts['literal_repaired_batches']+=1
 return out

# Every simple degree<=2 graph through six vertices; every tight independent
# cover, every subset of its complement, all initial max matchings through4.
for k in range(7):
 poss=list(combinations(range(k),2))
 for ids in subsets(range(len(poss))):
  E=[e for j,e in enumerate(poss) if j in ids];deg=Counter(v for e in E for v in e)
  if max(deg.values(),default=0)>2:continue
  U=set(range(k));Ms=maximum(U,E);nu=len(Ms[0]);accepted=False
  for C in subsets(U):
   if len(C)!=nu or any((a in C)==(b in C) for a,b in E):continue
   accepted=True;I=sorted(U-C);ops=[(x,k+j) for j,x in enumerate(I)];n=k+len(I)
   z=compile_budget(n,E,U,C,Ms[0],ops);counts['initial_independent_tight_covers']+=1
   for S in subsets(range(len(ops))):
    for M in (Ms if k<=4 else Ms[:1]):verify(n,E,U,C,M,ops,S)
   opt=grouped_optimum(z['groups']);out=verify(n,E,U,C,Ms[0],ops,set(opt['selected']))
   expected=max((nu-len(maximum((U-{ops[i][0] for i in S})|{ops[i][1] for i in S},E)[0]),-len(S)) for S in subsets(range(len(ops))))
   assert (opt['credit'],-len(opt['selected']))==expected;counts['literal_isolated_candidate_optima']+=1
  if accepted:counts['initial_degree_two_bipartite_graphs']+=1

# Exhaustive isolation compilation: all simple initial bipartite degree-two
# graphs through3; all tight independent covers and ordered removal lists;
# all possible edges involving two new points, including addition conflicts.
for k in range(4):
 for ids in subsets(range(k*(k-1)//2)):
  poss=list(combinations(range(k),2));initial=[e for j,e in enumerate(poss) if j in ids];U=set(range(k));Ms=maximum(U,initial);nu=len(Ms[0])
  for C in subsets(U):
   if len(C)!=nu or any((a in C)==(b in C) for a,b in initial):continue
   for q in range(min(2,len(U-C))+1):
    for X in permutations(sorted(U-C),q):
     ops=list(zip(X,range(k,k+q)));extra=[e for e in combinations(range(k+q),2) if e[1]>=k]
     for es in subsets(range(len(extra))):
      E=initial+[e for j,e in enumerate(extra) if j in es];z=compile_budget(k+q,E,U,C,Ms[0],ops);feasible=[]
      for S in subsets(range(q)):
       final=(U-{ops[i][0] for i in S})|{ops[i][1] for i in S};Y={ops[i][1] for i in S}
       literal=not any(set(e)<=final and set(e)&Y for e in E)
       compiled=not S&set(z['blocked']) and all(a not in S or b in S for a,b in z['dependencies']) and not any(a in S and b in S for a,b in z['conflicts'])
       assert literal==compiled;counts['literal_isolation_subsets']+=1
       if literal:feasible.append(S);verify(k+q,E,U,C,Ms[0],ops,S)
      opt=grouped_optimum(z['groups'],z['dependencies'],z['conflicts'],z['blocked']);expected=max((nu-len(maximum((U-{ops[i][0] for i in S})|{ops[i][1] for i in S},E)[0]),-len(S)) for S in feasible)
      assert (opt['credit'],-len(opt['selected']))==expected;counts['literal_isolation_systems']+=1

# Canonical group patterns (None is an uncharged/balanced label).
def patterns(q):
 for raw in product(range(-1,q),repeat=q):
  seen={};canon=[]
  for x in raw:
   if x==-1:canon.append(None)
   else:
    if x not in seen:seen[x]=len(seen)
    canon.append(seen[x])
  if tuple(canon)==tuple(None if x==-1 else x for x in raw):yield list(canon)

def check_system(g,D,F,B,K=None):
 q=len(g);feasible=[S for S in subsets(range(q)) if not S&set(B) and all(a not in S or b in S for a,b in D) and not any(a in S and b in S for a,b in F)]
 # Independent explicit sum: each odd group of size t saves max(t-1,0).
 def value(S):
  mult=Counter(g[i] for i in S if g[i] is not None)
  return sum(g[i] is None for i in S)+sum(max(t-1,0) for t in mult.values())
 expected=max((value(S),-len(S)) for S in feasible);opt=grouped_optimum(g,D,F,B,K);S=set(opt['selected'])
 assert S in feasible and (opt['credit'],-len(S))==expected
 KK=set(opt['vertex_cover']);FF=S&KK;conditional=[T for T in feasible if T&KK==FF];v=max(map(value,conditional));maximizers=[T for T in conditional if value(T)==v]
 intersection=set.intersection(*maximizers);assert intersection==S and S in maximizers
 assert set(opt['greatest_for_assignment'])==set.union(*conditional)
 counts['grouped_optimizer_systems']+=1
 digest.update(json.dumps([g,D,F,sorted(B),opt],sort_keys=True).encode())

for q in range(4):
 ds=[e for e in product(range(q),repeat=2) if e[0]!=e[1]];fs=list(combinations(range(q),2))
 for g in patterns(q):
  for di in subsets(range(len(ds))):
   D=[e for j,e in enumerate(ds) if j in di]
   for fi in subsets(range(len(fs))):
    F=[e for j,e in enumerate(fs) if j in fi]
    for B in subsets(range(q)):check_system(g,D,F,B)

rng=random.Random(13112649)
for trial in range(600):
 q=rng.randrange(4,11);g=[rng.choice([None,None,0,1,2,3]) for _ in range(q)];D=[e for e in product(range(q),repeat=2) if rng.randrange(12)==0];F=[e for e in combinations(range(q),2) if rng.randrange(5)==0];B={i for i in range(q) if rng.randrange(10)==0}
 check_system(g,D,F,B);K=set(range(q))
 for i in rng.sample(list(K),len(K)):
  if all(a!=i or b in K-{i} for a,b in F) and all(b!=i or a in K-{i} for a,b in F):K.remove(i)
 check_system(g,D,F,B,K)
 counts['larger_seeded_grouped_models']+=1

# Physical dissociation independently scored on every edge of the actual graph.
def physical(x,out):
 b=x['b'];n=2*b;U=set(out['U']);C=set(out['cover']);M=out['matching'];S=set(range(n))-U;T=U-C
 assert len(C)==len(M) and len({v for e in M for v in e})==2*len(M)
 assert all(set(e)<=U and tuple(sorted(e)) in {tuple(sorted(f)) for f in x['P']+x['Q']} for e in M)
 assert all(a in C or c in C for a,c in x['P']+x['Q'] if a in U and c in U)
 assert all(sum(v in e and set(e)<=S for e in x['B'])<=1 for v in S)
 G=[set() for _ in range(5*b)]
 def edge(a,c):G[a].add(c);G[c].add(a)
 for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
 for v in range(n):edge(b+v,3*b+v)
 for a,c in x['Q']:edge(b+a,b+c)
 for a,c in x['B']:edge(3*b+a,3*b+c)
 colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
 assert all(colour[v]!=colour[w] for v in range(5*b) for w in G[v])
 selected=set(range(b))|{b+v for v in T}|{3*b+v for v in S}
 assert len(selected)==3*b-len(C) and all(len(G[v]&selected)<=1 for v in selected)
 counts['physical_dissociation_certificates']+=1
 return G

for r in list(range(3,15))+[16,32,64,128,512]:
 x=shared_path_family(r);E=x['P']+x['Q'];U=set(x['initial_U']);C=set(x['cover']);ops=x['operations'];a=[x[k] for k in ('b','P','Q','B','colour')]
 out=physical_budget_batch(*a,U,ops,C,x['matching']);cert=out['certificate']
 assert out['optimization']['selected']==list(range(r)) and cert['actual_cost']==r-1 and len(cert['repair_regions'])==r-1
 assert cert['cover']==[4*j+3 for j in range(r-1)] and {tuple(e) for e in cert['matching']}=={(4*j+2,4*j+3) for j in range(r-1)}
 assert cert['beta_I_lower']==11*r+1 and all(g==out['constraints']['groups'][0] for g in out['constraints']['groups'])
 assert not out['constraints']['dependencies'] and not out['constraints']['conflicts'] and not out['constraints']['blocked']
 assert len(U)==4*r and all(len(U&set(K))==2 for K in x['squares'])
 assert (2*r-2>8*r//6)==(r>=4) and r-1<=8*r//6
 G=physical(x,cert);assert min(map(len,G))==2 and max(map(len,G))==3
 for v in (range(len(G)) if r<=6 else [0,1,len(G)//2,len(G)-1]):
  root=next(w for w in range(len(G)) if w!=v);seen={root};todo=[root]
  while todo:
   for w in G[todo.pop()]-seen-{v}:seen.add(w);todo.append(w)
  assert len(seen)==len(G)-1;counts['physical_connectivity_deletions']+=1
 if r<=7:
  for S in subsets(range(r)):
   XX={ops[i][1] for i in S};YY={ops[i][2] for i in S};V=(U-XX)|YY
   assert len(score(8*r,x['P'],x['Q'],V)[1])==2*r-2-max(len(S)-1,0)
   result=repair_batch(8*r,E,U,C,x['matching'],[(x,y) for _,x,y in ops],S)
   physical(x,result);old=choose_matching(8*r,E,U,C,x['matching'],XX,YY,True)
   assert not old['forced_retired'] and (not old['applicable'] or old['actual_cost']==2*r-2)
   counts['shared_path_literal_subsets']+=1
 if r==3:
  # Unique initial minimum cover: avoid enumerating every subset of U at large r.
  covers=[CC for CC in subsets(U) if len(CC)==2*r-2 and all(a in CC or b in CC for a,b in E if a in U and b in U)]
  assert covers==[C]
  z=best_initial_pair_batch(*a,U,ops,True);assert z['minimum_covers_tested']==1 and z['certificate']['actual_cost']==2*r-2
  examples.append(dict(model=x,result=out,inherited_best=z))
 counts['shared_path_family_scales']+=1

# Random physical square owners, literal optimum within the stated isolation
# domain; covers chosen independently as the smaller side on each component.
for n in (8,12,16,24):
 for trial in range(30):
  L=list(range(0,n,2));R=list(range(1,n,2));rng.shuffle(L);rng.shuffle(R)
  P=list(zip(L[::2],L[1::2]))+list(zip(R[::2],R[1::2]));rng.shuffle(R);q=rng.randrange(n//2+1);Q=list(zip(L[:q],R[:q]));order=[v for e in zip(L,R) for v in e];B=[]
  for off in range(0,n,4):K=order[off:off+4];B+=list(zip(K,K[1:]+K[:1]))
  args=[n//2,P,Q,B,[v%2 for v in range(n)]];data=prepare(*args);U=set();ops=[]
  for i,(K,_) in enumerate(data['owner_components']):U|=set(rng.sample(list(K),2))
  # Literal cover enumeration is small (at most12 initial points).
  M=maximum(U,P+Q)[0];covers=[CC for CC in subsets(U) if len(CC)==len(M) and all((a in CC)!=(b in CC) for a,b in P+Q if a in U and b in U)];C=rng.choice(covers)
  for i,(K,_) in enumerate(data['owner_components']):
   removals=sorted((set(K)&U)-C)
   if removals:ops.append([i,rng.choice(removals),rng.choice(sorted(set(K)-U))])
  out=physical_budget_batch(*args,U,ops,C,M);feasible=[]
  for S in subsets(range(len(ops))):
   V=(U-{ops[i][1] for i in S})|{ops[i][2] for i in S};Y={ops[i][2] for i in S}
   if any(set(e)<=V and set(e)&Y for e in P+Q):continue
   cost=len(maximum(V,P+Q)[0]);feasible.append((len(C)-cost,-len(S)));counts['random_physical_literal_feasible_batches']+=1
  cert=out['certificate'];assert (cert['credit'],-len(cert['selected_candidates']))==max(feasible)
  physical(dict(b=n//2,P=P,Q=Q,B=B,colour=args[-1]),cert);counts['random_physical_optima']+=1

# Hypothesis controls: non-independent cover, odd cycle, non-tight matching,
# maximum degree three, duplicate replacements and infeasible selected batch.
invalid=[(3,[(0,1),(1,2)],{0,1,2},{0,1},[(0,1)],[]),
 (3,[(0,1),(1,2),(0,2)],{0,1,2},{0,1},[(0,1)],[]),
 (2,[(0,1)],{0,1},{0},[],[]),
 (4,[(0,1),(0,2),(0,3)],{0,1,2,3},{0},[(0,1)],[]),
 (4,[(0,1)],{0,1},{0},[(0,1)],[(1,2),(1,3)])]
for args in invalid:
 try:compile_budget(*args)
 except ValueError:counts['rejected_hypothesis_controls']+=1
 else:raise AssertionError(args)
try:repair_batch(3,[(0,1),(0,2)],{0,1},{0},[(0,1)],[(1,2)],{0})
except ValueError:counts['rejected_hypothesis_controls']+=1
else:raise AssertionError('Blocked addition accepted')
report=dict(scope='Exact shared odd-path budget with independent tight cover, removals outside it and finally isolated additions. Literal degree-two bipartite graphs through6; full isolation systems through3 and2additions; exhaustive grouped dependency/conflict/blocker/canonical-group systems through3; larger seeded systems and physical optima. Uniform connected20r family has inherited best2r-2 vs repaired fixed-list optimum r-1. No unrestricted all-helper optimum, rectangular embedding, universal8b/3 or5/6 claim.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/odd-path-neutral-budget-check.json'));args=p.parse_args();dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
