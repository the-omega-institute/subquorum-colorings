"""Literal all-budget checks, cycle traces, pair-width and actual graph families."""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from nonisolated_exchange_frontier import endpoint,exact_frontier,physical_frontier,cost_increase_family,free_extension_family,within_budget
from owner_matching_certificate import prepare
from mixed_isolated_cover_repair import maximum_credit,vertex_cover_physical
from matching_choice_exchange import choose_matching
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

def allowed(n,E):
 adj=[set() for _ in range(n)];colour={}
 for a,b in E:adj[a].add(b);adj[b].add(a)
 if any(len(ns)>2 for ns in adj):return False
 for root in range(n):
  if root in colour:continue
  colour[root]=0;todo=[root]
  while todo:
   v=todo.pop()
   for w in adj[v]:
    if w in colour:
     if colour[w]==colour[v]:return False
    else:colour[w]=1-colour[v];todo.append(w)
 return True


def certificate(n,E,U,ops,S):
 out=endpoint(n,E,U,ops,S);V=set(out['U']);C=set(out['cover']);M=out['matching'];actual=nu(V,E)
 assert out['actual_cost']==actual==len(M)==len(C)
 assert len({v for e in M for v in e})==2*len(M) and all(set(e)<=V and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in M)
 assert all(a in C or b in C for a,b in E if a in V and b in V)
 assert abs(out['saving'])<=len(S);counts['literal_endpoint_certificates']+=1;return out


def check(n,E,U,ops,orders=None):
 result=exact_frontier(n,E,U,ops,orders);q=len(ops);expected={t:None for t in range(q+1)};initial=nu(U,E)
 for S in subsets(range(q)):
  final=(set(U)-{ops[i][0] for i in S})|{ops[i][1] for i in S};cost=nu(final,E);t=len(S)
  expected[t]=cost if expected[t] is None else min(expected[t],cost);counts['literal_candidate_subsets']+=1
  assert abs(initial-cost)<=t
 for row in result['frontier']:
  t=row['operations'];S={i for i in range(q) if row['selected_mask']>>i&1};assert len(S)==t and row['cost']==expected[t]
  out=certificate(n,E,U,ops,S);assert out['actual_cost']==row['cost'];counts['exact_operation_count_points']+=1
 assert all(abs(expected[t+1]-expected[t])<=1 for t in range(q))
 for budget in range(q+2):
  out=within_budget(result,budget);best=min((c,t) for t,c in expected.items() if t<=budget);assert (out['cost'],out['operations'])==best;counts['at_most_budget_optima']+=1
 flat=[v for K in result['component_orders'] for v in K];pos={v:j for j,v in enumerate(flat)}
 profile=[sum(min(pos[x],pos[y])<=cut<max(pos[x],pos[y]) for x,y in ops) for cut in range(n)]
 assert profile==result['live_profile'] and result['pair_width']==max(profile,default=0)
 assert result['peak_states']<=4*(q+1)*(1<<result['pair_width'])
 digest.update(json.dumps([n,E,sorted(U),ops,result],sort_keys=True).encode());counts['generic_frontiers']+=1;return result

# All bipartite degree-two ambient graphs through4, every initialU and every
# possible candidate injection; no addition-isolation restriction at all.
for n in range(5):
 possible=list(combinations(range(n),2))
 for ids in subsets(range(len(possible))):
  E=[e for j,e in enumerate(possible) if j in ids]
  if not allowed(n,E):continue
  for U in subsets(range(n)):
   outside=set(range(n))-U
   for q in range(min(len(U),len(outside))+1):
    for X in combinations(sorted(U),q):
     for Y in permutations(sorted(outside),q):check(n,E,U,list(zip(X,Y)))
  counts['exhaustive_ambient_graphs']+=1

# Every selected subset on each even cycle through12: no zero to break the
# trace is guaranteed. Includes the fully selected cycle and all path runs.
for n in (4,6,8,10,12):
 E=[(v,(v+1)%n) for v in range(n)]
 for U in subsets(range(n)):
  result=check(n,E,U,[]);assert result['best']['cost']==nu(U,E);counts['cycle_trace_subsets']+=1

# Larger arbitrary candidate crossings, y-before-x, rotations, reversals,
# component permutations and empty/all-selected cycles.
rng=random.Random(13112667)
for trial in range(140):
 n=rng.randrange(5,15);order=list(range(n));rng.shuffle(order);E=[(order[j],order[j+1]) for j in range(n-1) if rng.randrange(5)]
 if n%2==0 and rng.randrange(2)==0 and len(E)==n-1:E.append((order[-1],order[0]))
 U=set(rng.sample(range(n),rng.randrange(n+1)));q=rng.randrange(min(len(U),n-len(U),6)+1);ops=list(zip(rng.sample(sorted(U),q),rng.sample(sorted(set(range(n))-U),q)))
 original=check(n,E,U,ops);components=[list(K) for K in original['component_orders']];rng.shuffle(components)
 for K in components:
  if rng.randrange(2):K.reverse()
  cyclic=len(K)>=4 and sum(a in K and b in K for a,b in E)==len(K)
  if cyclic:
   off=rng.randrange(len(K));K[:]=K[off:]+K[:off]
 changed=check(n,E,U,ops,components);assert [r['cost'] for r in changed['frontier']]==[r['cost'] for r in original['frontier']];counts['traversal_invariance_pairs']+=1


def physical_graph(x):
 b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
 def edge(a,c):G[a].add(c);G[c].add(a)
 for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
 for v in range(n):edge(b+v,3*b+v)
 for a,c in x['Q']:edge(b+a,b+c)
 for a,c in x['B']:edge(3*b+a,3*b+c)
 colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
 assert all(colour[v]!=colour[w] for v in range(len(G)) for w in G[v])
 return G


def score_physical(x,G,U,C,M):
 b=x['b'];n=2*b;U=set(U);C=set(C);S=set(range(n))-U;W=U-C;E={tuple(sorted(e)) for e in x['P']+x['Q']}
 assert len(C)==len(M) and len({v for e in M for v in e})==2*len(M) and all(tuple(sorted(e)) in E and set(e)<=U for e in M)
 assert all(a in C or c in C for a,c in E if a in U and c in U)
 selected=set(range(b))|{b+v for v in W}|{3*b+v for v in S};assert len(selected)==3*b-len(C) and all(len(G[v]&selected)<=1 for v in selected)
 degree=Counter(v for a,c in x['B'] if a in S and c in S for v in (a,c));assert max(degree.values(),default=0)<=1
 counts['actual_dissociation_certificates']+=1

# Two all-parameter physical families, sharp opposite budget slopes.
for constructor in (cost_increase_family,free_extension_family):
 for r in list(range(1,17))+[32,64,128,512]:
  x=constructor(r);q=len(x['operations']);n=2*x['b'];U=set(x['initial_U']);ops=[(a,b) for _,a,b in x['operations']];E=x['P']+x['Q'];args=[x[k] for k in ('b','P','Q','B','colour')]
  data=prepare(*args);assert all(len(U&set(K))==2 for K,_ in data['owner_components'])
  out=physical_frontier(*args,U,x['operations']);G=physical_graph(x);assert min(map(len,G))==2 and max(map(len,G))==3
  expected=[t if constructor is cost_increase_family else 2*r-t for t in range(r+1)];assert [row['cost'] for row in out['frontier']]==expected
  assert out['pair_width']<=(2 if constructor is cost_increase_family else 1)
  score_physical(x,G,out['certificate']['U'],out['certificate']['cover'],out['certificate']['matching'])
  if r<=8:
   for S in subsets(range(r)):
    cert=endpoint(n,E,U,ops,S);assert cert['actual_cost']==expected[len(S)];score_physical(x,G,cert['U'],cert['cover'],cert['matching']);counts['family_literal_subsets']+=1
  if r<=6:deletions=range(len(G))
  else:deletions=sorted({0,1,len(G)//2,len(G)-1})
  for v in deletions:
   root=next(w for w in range(len(G)) if w!=v);seen={root};todo=[root]
   while todo:
    for w in G[todo.pop()]-seen-{v}:seen.add(w);todo.append(w)
   assert len(seen)==len(G)-1;counts['physical_connectivity_deletions']+=1
  if constructor is free_extension_family:
   old=maximum_credit(n,E,U,ops);assert old['certificate']['actual_cost']==2*r
   C={8*i+t for i in range(r) for t in (2,4)};M=[e for i in range(r) for e in ((8*i+1,8*i+2),(8*i+3,8*i+4))]
   inherited=choose_matching(n,E,U,C,M,{a for a,b in ops},{b for a,b in ops},True);assert inherited['applicable'] and inherited['actual_cost']==r;counts['earlier_mixed_inherited_controls']+=1
  counts['family_scales']+=1
  if r==2:examples.append(dict(name=constructor.__name__,model=x,result=out))

# General physical candidates, direct subset scoring and all budget witnesses.
for n in (8,12,16):
 for trial in range(20):
  L=list(range(0,n,2));R=list(range(1,n,2));rng.shuffle(L);rng.shuffle(R);P=list(zip(L[::2],L[1::2]))+list(zip(R[::2],R[1::2]));rng.shuffle(R);q=rng.randrange(n//2+1);Q=list(zip(L[:q],R[:q]));order=[v for e in zip(L,R) for v in e];B=[]
  for off in range(0,n,4):K=order[off:off+4];B+=list(zip(K,K[1:]+K[:1]))
  args=[n//2,P,Q,B,[v%2 for v in range(n)]];data=prepare(*args);U=set();ops=[]
  for i,(K,_) in enumerate(data['owner_components']):
   initial=set(rng.sample(list(K),2));U|=initial;ops.append([i,rng.choice(sorted(initial)),rng.choice(sorted(set(K)-initial))])
  result=physical_frontier(*args,U,ops);literal=check(n,P+Q,U,[(a,b) for _,a,b in ops]);assert [r['cost'] for r in result['frontier']]==[r['cost'] for r in literal['frontier']]
  x=dict(b=n//2,P=P,Q=Q,B=B,colour=args[-1]);G=physical_graph(x)
  for row in result['frontier']:
   S={i for i in range(len(ops)) if row['selected_mask']>>i&1};cert=endpoint(n,P+Q,U,[(a,b) for _,a,b in ops],S);score_physical(x,G,cert['U'],cert['cover'],cert['matching'])
  counts['random_physical_frontiers']+=1

# Zero-cost decision agrees with the previous physical Vertex Cover encoding;
# operation budget remains meaningful even without explicit final isolation.
for k,H in [(1,[]),(2,[(0,1)]),(3,[(0,1),(0,2),(1,2)]),(4,list(combinations(range(4),2)))]:
 x=vertex_cover_physical(k,H);out=physical_frontier(*[x[z] for z in ('b','P','Q','B','colour')],x['initial_U'],x['operations']);expected_tau=min(len(S) for S in subsets(range(k)) if all(a in S or b in S for a,b in H))
 firstzero=min(row['operations'] for row in out['frontier'] if row['cost']==0);assert firstzero==x['D']*expected_tau;counts['previous_hardness_budget_controls']+=1

# Public generic entrypoints must normalize one-shot iterables exactly once.
for n,E,U,ops,S in [(0,[],set(),[],set()),(2,[(0,1)],{0,1},[],set()),(6,[(v,(v+1)%6) for v in range(6)],{0,2,4},[(0,1),(2,3),(4,5)],{0,2})]:
 expected=endpoint(n,E,U,ops,S);dp=exact_frontier(n,E,U,ops);orders=dp['component_orders']
 for mask in range(16):
  values=[E,U,ops,S];args=[iter(v) if mask>>j&1 else v for j,v in enumerate(values)]
  assert endpoint(n,args[0],args[1],args[2],args[3])==expected;counts['one_shot_endpoint_controls']+=1
  values=[E,U,ops,orders];args=[iter(v) if mask>>j&1 else v for j,v in enumerate(values)]
  assert exact_frontier(n,args[0],args[1],args[2],args[3])==dp;counts['one_shot_frontier_controls']+=1
for constructor in (cost_increase_family,free_extension_family):
 x=constructor(2);args=[x[k] for k in ('b','P','Q','B','colour')]
 assert physical_frontier(*args,iter(x['initial_U']),iter(x['operations']))==physical_frontier(*args,x['initial_U'],x['operations']);counts['one_shot_physical_controls']+=1

report=dict(scope='All exact operation-count optima for arbitrary mixed replacements on a degree-two bipartite AMBIENT auxiliary graph, no final-isolation requirement. Pair-frontier-width DP including full cycle traces and cross-component labels; explicit witnesses and covers/matchings. Two all-scale physical opposite-slope families: cost(t)=t and cost(t)=2r-t. The latter improves isolation-only candidates, while earlier mixed inherited rule already reaches it. No universal polynomial, weightedTH, unrestricted global parameter or rectangular-grid claim.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/nonisolated-exchange-frontier-check.json'));args=p.parse_args();dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
