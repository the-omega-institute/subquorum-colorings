"""Literal mixed-repair checks and independent physical VC-reduction audit."""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from mixed_isolated_cover_repair import compile_isolation,repair,maximum_credit,minimum_operation_optimum,dependency_components,vertex_cover_physical,bridgeless_vertex_cover_reduction
from owner_matching_certificate import prepare
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();examples=[]

def subsets(V):
 V=sorted(V)
 for mask in range(1<<len(V)):yield {v for j,v in enumerate(V) if mask>>j&1}

def matchings(V,E):
 V=set(V)
 if not V:yield [];return
 v=min(V);yield from matchings(V-{v},E)
 for a,b in E:
  w=b if a==v else a if b==v else None
  if w is not None and w in V:
   for M in matchings(V-{v,w},E):yield [(v,w)]+M

def nu(V,E):return max(map(len,matchings(V,E)))

def initial_ok(U,E):
 adj={v:set() for v in U};colour={}
 for a,b in E:
  if a in U and b in U:adj[a].add(b);adj[b].add(a)
 if any(len(ns)>2 for ns in adj.values()):return False
 for root in sorted(U):
  if root in colour:continue
  colour[root]=0;todo=[root]
  while todo:
   v=todo.pop()
   for w in adj[v]:
    if w in colour:
     if colour[v]==colour[w]:return False
    else:colour[w]=1-colour[v];todo.append(w)
 return True


def verify(n,E,U,ops,S):
 out=repair(n,E,U,ops,S);V=set(out['U']);C=set(out['cover']);M=out['matching'];actual=nu(V,E)
 assert actual==out['actual_cost']==len(C)==len(M)
 assert len({v for e in M for v in e})==2*len(M) and all(set(e)<=V and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in M)
 assert all(a in C or b in C for a,b in E if a in V and b in V)
 assert all(not set(e)&set(out['added']) for e in E if set(e)<=V)
 assert len(out['charged_edges'])==out['credit'] and len({tuple(e) for e in out['charged_edges']})==out['credit']
 assert all(e in out['destroyed_initial_edges'] and set(e)&set(out['removed']) for e in out['charged_edges'])
 counts['literal_repaired_batches']+=1;digest.update(json.dumps(out,sort_keys=True).encode());return out

# All simple initial degree-two bipartite graphs through6 and all mixed
# removal subsets; additions are distinct isolates.
for k in range(7):
 poss=list(combinations(range(k),2));U=set(range(k))
 for ids in subsets(range(len(poss))):
  E=[e for j,e in enumerate(poss) if j in ids]
  if not initial_ok(U,E):continue
  ops=[(i,k+i) for i in range(k)];initial=nu(U,E)
  for S in subsets(range(k)):
   out=verify(2*k,E,U,ops,S);assert out['credit']==initial-out['actual_cost'];counts['all_mixed_initial_subsets']+=1
  best=maximum_credit(2*k,E,U,ops);tie=minimum_operation_optimum(2*k,E,U,ops);vc=min(len(S) for S in subsets(U) if all(a in S or b in S for a,b in E))
  assert best['certificate']['actual_cost']==tie['certificate']['actual_cost']==0 and len(tie['certificate']['selected_candidates'])==vc
  counts['initial_graphs']+=1

# All ambient simple graphs through4, all valid initial U, all ordered
# distinct injections X->Y of any possible length, all candidate subsets.
for n in range(5):
 possible=list(combinations(range(n),2))
 for es in subsets(range(len(possible))):
  E=[e for j,e in enumerate(possible) if j in es]
  for U in subsets(range(n)):
   if not initial_ok(U,E):continue
   outside=set(range(n))-U;initial=nu(U,E)
   for q in range(min(len(U),len(outside))+1):
    for X in combinations(sorted(U),q):
     for Y in permutations(sorted(outside),q):
      ops=list(zip(X,Y));z=compile_isolation(n,E,U,ops);feasible=[]
      for S in subsets(range(q)):
       final=(U-{ops[i][0] for i in S})|{ops[i][1] for i in S};added={ops[i][1] for i in S}
       literal=not any(set(e)<=final and set(e)&added for e in E)
       compiled=not S&set(z['blocked']) and all(a not in S or b in S for a,b in z['dependencies']) and not any(a in S and b in S for a,b in z['conflicts'])
       assert literal==compiled;counts['ambient_isolation_subsets']+=1
       if literal:
        out=verify(n,E,U,ops,S);feasible.append((initial-out['actual_cost'],-len(S)))
      best=maximum_credit(n,E,U,ops);tie=minimum_operation_optimum(n,E,U,ops);expected=max(feasible)
      assert best['certificate']['credit']==expected[0] and (tie['certificate']['credit'],-len(tie['certificate']['selected_candidates']))==expected
      allcover=maximum_credit(n,E,U,ops,range(q));assert allcover['certificate']['credit']==expected[0]
      counts['ambient_injection_systems']+=1

# Independent SCC equivalence via all-pairs reachability for every directed
# graph through4; self-loops do not change SCCs.
for q in range(5):
 possible=[e for e in product(range(q),repeat=2) if e[0]!=e[1]]
 for ids in subsets(range(len(possible))):
  D=[e for j,e in enumerate(possible) if j in ids];reach={i:{i} for i in range(q)}
  for a,b in D:reach[a].add(b)
  for t in range(q):
   for a in range(q):
    if t in reach[a]:reach[a]|=reach[t]
  expected={frozenset(j for j in range(q) if j in reach[i] and i in reach[j]) for i in range(q)}
  actual={frozenset(B) for B in dependency_components(q,D)};assert actual==expected;counts['literal_dependency_graphs']+=1

rng=random.Random(13112653)
for trial in range(160):
 k=rng.randrange(2,9);q=rng.randrange(1,min(k,6)+1);U=set(range(k));E=[(v,v+1) for v in range(k-1) if rng.randrange(3)];ops=list(zip(rng.sample(range(k),q),range(k,k+q)))
 E += [e for e in combinations(range(k+q),2) if e[1]>=k and rng.randrange(5)==0];z=compile_isolation(k+q,E,U,ops);feasible=[]
 for S in subsets(range(q)):
  final=(U-{ops[i][0] for i in S})|{ops[i][1] for i in S};added={ops[i][1] for i in S}
  if any(set(e)<=final and set(e)&added for e in E):continue
  out=verify(k+q,E,U,ops,S);feasible.append((out['credit'],-len(S)))
 best=maximum_credit(k+q,E,U,ops);tie=minimum_operation_optimum(k+q,E,U,ops);assert best['certificate']['credit']==max(feasible)[0] and (tie['certificate']['credit'],-len(tie['certificate']['selected_candidates']))==max(feasible)
 counts['seeded_mixed_systems']+=1


def vertex_covers(k,H):return [S for S in subsets(range(k)) if all(a in S or b in S for a,b in H)]
def tau(k,H):return min(map(len,vertex_covers(k,H)))
def connected(k,E,removed_vertex=None,removed_edge=None):
 V=set(range(k))-{removed_vertex}
 if not V:return True
 adj={v:set() for v in V}
 for a,b in E:
  if a in V and b in V and frozenset((a,b))!=removed_edge:adj[a].add(b);adj[b].add(a)
 seen={min(V)};todo=list(seen)
 while todo:
  for w in adj[todo.pop()]-seen:seen.add(w);todo.append(w)
 return seen==V


def physical_graph(x):
 b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
 def edge(a,c):G[a].add(c);G[c].add(a)
 for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
 for v in range(n):edge(b+v,3*b+v)
 for a,c in x['Q']:edge(b+a,b+c)
 for a,c in x['B']:edge(3*b+a,3*b+c)
 colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
 assert all(colour[v]!=colour[w] for v in range(5*b) for w in G[v]) and min(map(len,G))==2 and max(map(len,G))==3
 return G


def validate_physical(x):
 q=x['q'];n=4*q;data=prepare(x['b'],x['P'],x['Q'],x['B'],x['colour']);U=set(x['initial_U']);initial=set(map(tuple,map(sorted,x['Q'])))
 assert len(data['owner_components'])==q and all(set(data['owner_components'][i][0])=={i,q+i,2*q+i,3*q+i} for i in range(q))
 assert all(len(U&set(K))==2 for K,_ in data['owner_components'])
 assert all(len(set((U-{i})|{q+i})&set(K))==2 for i in range(q) for K,_ in data['owner_components'] if i in K)
 assert all(x['colour'][a]==x['colour'][b] for a,b in x['P']) and all(x['colour'][a]!=x['colour'][b] for a,b in x['Q']+x['B'])
 ops=[(a,b) for _,a,b in x['operations']];z=compile_isolation(n,x['P']+x['Q'],U,ops)
 expected=sorted((i,j) for G in x['groups'] for i,j in zip(G,G[1:]+G[:1]));assert sorted(map(tuple,z['dependencies']))==expected and not z['blocked'] and not z['conflicts']
 E=x['P']+x['Q'];assert {tuple(sorted(e)) for e in E if set(e)<=U}==initial
 counts['physical_models']+=1;return physical_graph(x)


def score_physical(x,G,S):
 q=x['q'];b=x['b'];U=set(x['initial_U']);XX={i for i in S};YY={q+i for i in S};final=(U-XX)|YY;E=x['P']+x['Q'];expected=[tuple(sorted(e)) for e in x['Q'] if not set(e)&XX]
 assert sorted(tuple(sorted(e)) for e in E if set(e)<=final)==sorted(expected)
 cover={a for a,c in expected};assert len(cover)==len(expected)
 owners=set(range(4*q))-final;T=final-cover
 selected=set(range(b))|{b+v for v in T}|{3*b+v for v in owners}
 assert len(selected)==3*b-len(expected) and all(len(G[v]&selected)<=1 for v in selected)
 counts['actual_dissociation_certificates']+=1
 return len(expected)

for k in range(1,5):
 possible=list(combinations(range(k),2))
 for es in subsets(range(len(possible))):
  H=[e for j,e in enumerate(possible) if j in es];x=vertex_cover_physical(k,H);G=validate_physical(x);q=x['q'];D=x['D'];E=x['P']+x['Q'];U=set(x['initial_U']);ops=[(a,b) for _,a,b in x['operations']]
  bestpair=None
  for V in subsets(range(k)):
   S={i for v in V for i in x['groups'][v]};cost=score_physical(x,G,S);assert cost==sum(a not in V and b not in V for a,b in H) and len(S)==D*len(V)
   pair=(cost,len(S));bestpair=pair if bestpair is None or pair<bestpair else bestpair;counts['physical_vertex_subsets']+=1
  result=minimum_operation_optimum(4*q,E,U,ops);cert=result['certificate'];assert cert['actual_cost']==0 and len(cert['selected_candidates'])==D*tau(k,H)==bestpair[1]
  assert {frozenset(B) for B in result['dependency_components']}=={frozenset(B) for B in x['groups']}
  if k<=3:
   for S in subsets(range(q)):
    final=(U-S)|{q+i for i in S};Y={q+i for i in S};isolated=not any(set(e)<=final and set(e)&Y for e in E)
    groupclosed=all(not set(B)&S or set(B)<=S for B in x['groups']);assert isolated==groupclosed;counts['physical_literal_candidate_subsets']+=1
  bridgeless=connected(k,H) and all(connected(k,H,removed_edge=frozenset(e)) for e in H)
  if bridgeless:
   edges=[(v,w) for v in range(len(G)) for w in G[v] if v<w]
   for v in range(len(G)):assert connected(len(G),edges,removed_vertex=v);counts['physical_single_deletion_checks']+=1
   counts['bridgeless_physical_models']+=1
  counts['physical_exact_min_operation_optima']+=1
  if k==3 and H==[(0,1),(0,2),(1,2)]:examples.append(dict(name='triangle input; true minimum-operation tie-break',model=x,result=result))

# Literal local gadget covers and the connected/bridgeless normalization.
# Each doubled length-three edge gadget costs2 if an endpoint is selected,
# costs4 if neither endpoint is selected.
localE=[(0,2),(2,3),(3,1),(0,4),(4,5),(5,1)];local_cost={}
for ends in subsets({0,1}):
 choices=[Z for Z in subsets({2,3,4,5}) if all(a in ends|Z or b in ends|Z for a,b in localE)]
 local_cost[tuple(sorted(ends))]=min(map(len,choices));assert local_cost[tuple(sorted(ends))]==(2 if ends else 4);counts['literal_edge_gadget_states']+=1

for k in range(5):
 possible=list(combinations(range(k),2))
 for es in subsets(range(len(possible))):
  H=[e for j,e in enumerate(possible) if j in es];z=bridgeless_vertex_cover_reduction(k,H);base=z['base_edges'];m=len(base)
  assert tau(z['base_k'],base)==tau(k,H)+1
  values=[]
  for S in subsets(range(z['base_k'])):
   value=len(S)
   for a,b in base:
    ends=tuple(i for i,v in enumerate((a,b)) if v in S);value+=local_cost[ends]
   values.append(value)
  assert min(values)==z['tau_additive_constant']+tau(k,H)
  assert connected(z['k'],z['H']) and all(connected(z['k'],z['H'],removed_edge=frozenset(e)) for e in z['H'])
  counts['normalized_vc_inputs']+=1

for k,H in [(0,[]),(1,[]),(2,[(0,1)]),(3,[(0,1),(0,2),(1,2)]),(4,list(combinations(range(4),2)))]:
 z=bridgeless_vertex_cover_reduction(k,H);x=vertex_cover_physical(z['k'],z['H']);G=validate_physical(x);baseS=min(vertex_covers(z['base_k'],z['base_edges']),key=lambda S:(len(S),sorted(S)));Jcover=set(baseS)
 for gadget in z['paths']:
  u,v=gadget['base_edge'];a,b=gadget['paths'][0][1:3];c,d=gadget['paths'][1][1:3];E=[(u,a),(a,b),(b,v),(u,c),(c,d),(d,v)]
  choices=[T for T in subsets({a,b,c,d}) if all(p in baseS|T or q in baseS|T for p,q in E)];Jcover|=min(choices,key=lambda T:(len(T),sorted(T)))
 assert len(Jcover)==z['tau_additive_constant']+tau(k,H) and all(a in Jcover or b in Jcover for a,b in z['H'])
 S={i for v in Jcover for i in x['groups'][v]};assert len(S)==x['D']*len(Jcover) and score_physical(x,G,S)==0
 if k==0:deletions=range(len(G))
 else:deletions=sorted(set([0,1,len(G)-1,len(G)//2]+[rng.randrange(len(G)) for _ in range(12)]))
 edges=[(v,w) for v in range(len(G)) for w in G[v] if v<w]
 for v in deletions:assert connected(len(G),edges,removed_vertex=v);counts['normalized_physical_deletions']+=1
 counts['normalized_full_physical_models']+=1
 if k==2:examples.append(dict(name='normalized connected bridgeless reduction',normalization=z,physical_summary=dict(b=x['b'],q=x['q'],D=x['D'],actual_order=len(G),selected_operations=len(S),zero_cost=0)))

# Conditional uniqueness fails even for one initial edge and no conflicts.
E=[(0,1)];ops=[(0,2),(1,3)];a=repair(4,E,{0,1},ops,{0});b=repair(4,E,{0,1},ops,{1});greatest=maximum_credit(4,E,{0,1},ops)
assert a['actual_cost']==b['actual_cost']==0 and a['credit']==b['credit']==1 and greatest['certificate']['selected_candidates']==[0,1]
assert repair(4,E,{0,1},ops,set())['actual_cost']==1
counts['conditional_uniqueness_counterexamples']=1;examples.append(dict(name='two incomparable one-operation optima; greatest batch is not min operations',left=a,right=b,greatest=greatest))
report=dict(scope='Mixed removals, degree-two bipartite initial induced graph, finally isolated additions. Exact odd-component formula, constructive covers/matchings,2^conflict-cover max credit only,2^dependency-SCC exact min-operation tie-break. Direct vertex-cover reduction including physical square owners,min2/max3; explicit connected bridgeless normalization proves two-connected physical min-operation hardness. No hardness of unrestricted all-helper or primary max credit; no universal numerical or rectangular-grid claim.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/mixed-isolated-cover-repair-check.json'));args=p.parse_args();dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report['counts'],sort_keys=True))
