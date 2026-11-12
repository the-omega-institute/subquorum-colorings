"""Literal all-matching choice equivalence, all-cover optimization and Hall barrier."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from matching_choice_exchange import choose_matching,saturate,best_initial_pair_batch,common_neighbour_barrier,mixed_path_escape
from matching_credit_exchange import credit_constraints,closed_conflict_optimum
from cover_choice_exchange import minimum_covers
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();examples=[]

def subsets(V):
 V=sorted(V)
 for mask in range(1<<len(V)):yield {v for i,v in enumerate(V) if mask>>i&1}

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

def check(n,E,U,C,Ms,X,Y,mixed=False):
 out=choose_matching(n,E,U,C,Ms[0],X,Y,mixed);final=(U-X)|Y;expected=False
 for M in Ms:
  mate={v:w for a,b in M for v,w in ((a,b),(b,a))};R={c for c in C if c in X or mate[c] in X};kept=C-R
  good=all(a in kept or b in kept for a,b in E if a in final and b in final)
  if good:
   expected=True;assert R==set(out['forced_retired']);counts['literal_feasible_initial_pair_certificates']+=1
 assert out['applicable']==expected
 if expected:
  chosen=out['initial_matching'];kept=set(out['cover']);rem=out['matching']
  assert len({v for e in chosen for v in e})==2*len(C)==2*len(chosen)
  assert all(set(e)<=U and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in chosen)
  assert len(rem)==len(kept)==len(maximum(final,E)[0])==out['actual_cost']
  assert len(out['charged_edges'])==out['credit'] and not any(set(e)&X for e in rem)
  counts['literal_successful_reconstructions']+=1
 elif out['reason']=='constrained initial matching cannot saturate cover':
  h=out['hall'];L=set(h['hall_left']);R=set(h['hall_neighbours']);I=U-C;kept=set(out['cover'])
  allowed=[(a,b) for a,b in E if not ((a in kept and b in X) or (b in kept and a in X))]
  N={b for a,b in allowed if a in L and b in I}|{a for a,b in allowed if b in L and a in I}
  assert N==R and len(L)>len(R);counts['literal_Hall_failures']+=1
 else:
  e=out['uncovered_edge'];assert set(e)<=final and not set(e)&set(out['cover']);counts['literal_cover_failures']+=1
 digest.update(json.dumps([n,E,sorted(U),sorted(C),sorted(X),sorted(Y),out],sort_keys=True).encode())
 counts['literal_batch_models']+=1

for n in range(5):
 possible=list(combinations(range(n),2))
 for Es in subsets(range(len(possible))):
  E=[e for i,e in enumerate(possible) if i in Es]
  for U in subsets(range(n)):
   Ms=maximum(U,E);nu=len(Ms[0])
   for C in subsets(U):
    if len(C)!=nu or any(a not in C and b not in C for a,b in E if a in U and b in U):continue
    counts['literal_tight_cover_models']+=1
    for X in subsets(U):
     for Y in subsets(set(range(n))-U):
      if len(X)==len(Y):
       check(n,E,U,C,Ms,X,Y,True)
       if not X&C:check(n,E,U,C,Ms,X,Y)

# Arbitrary supplied cross graphs: literal optimum and returned Hall witness.
for l in range(4):
 for r in range(4):
  L=set(range(l));R=set(range(l,l+r));possible=[(a,b) for a in sorted(L) for b in sorted(R)]
  for Es in subsets(range(len(possible))):
   E=[e for i,e in enumerate(possible) if i in Es];z=saturate(L,R,E);assert z['saturated']==(len(maximum(L|R,E)[0])==l)
   if not z['saturated']:
    S=set(z['hall_left']);N={b for a,b in E if a in S};assert N==set(z['hall_neighbours']) and len(S)>len(N)
   counts['literal_cross_graphs']+=1

rng=random.Random(13112631)
for k in range(1,5):
 for trial in range(30):
  C=set(range(k));I=set(range(k,2*k+rng.randrange(3)));U=C|I;n=len(U)+3;outside=set(range(len(U),n))
  E={(c,k+c) for c in C}
  E|={(c,i) for c in C for i in I if rng.randrange(3)==0}
  E|={(a,b) for a,b in combinations(sorted(C),2) if rng.randrange(3)==0}
  E|={(a,b) for a,b in combinations(range(n),2) if (a in outside or b in outside) and rng.randrange(5)==0}
  E=sorted(E);Ms=maximum(U,E);assert len(Ms[0])==k
  X={i for i in I if rng.randrange(2)==0};X=set(sorted(X)[:3]);Y=set(sorted(outside)[:len(X)])
  check(n,E,U,C,Ms,X,Y);counts['seeded_larger_batch_models']+=1

# Initial matching choice can rescue a zero-credit prerequisite of a saving.
E=[(0,1),(1,2),(2,3),(3,4),(6,7),(0,9)];U={0,1,2,3,4,6,7};C={1,3,6};bad=[(0,1),(2,3),(6,7)];ops=[(0,8),(7,9)]
z=credit_constraints(10,E,U,C,bad,ops);old=closed_conflict_optimum(z['weights'],z['dependencies'],z['conflicts'],z['blocked']);assert old['credit']==0
new=choose_matching(10,E,U,C,bad,{0,7},{8,9});assert new['applicable'] and new['credit']==1
check(10,E,U,C,maximum(U,E),{0,7},{8,9});examples.append(dict(name='matching choice rescues a zero-credit prerequisite',edges=E,U=sorted(U),cover=sorted(C),bad_matching=bad,operations=ops,result=new))
counts['positive_matching_choice_controls']=1


def physical(x,U,C,M):
 b=x['b'];n=2*b;U=set(U);C=set(C);E=x['P']+x['Q'];S=set(range(n))-U;T=U-C
 assert C<=U and len(M)==len(C) and len({v for e in M for v in e})==2*len(M)
 assert all(set(e)<=U and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in M)
 assert all(a in C or c in C for a,c in E if a in U and c in U)
 deg={v:0 for v in S}
 for a,c in x['B']:
  if a in S and c in S:deg[a]+=1;deg[c]+=1
 assert all(v<=1 for v in deg.values())
 G=[set() for _ in range(5*b)]
 def edge(a,c):G[a].add(c);G[c].add(a)
 for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
 for v in range(n):edge(b+v,3*b+v)
 for a,c in x['Q']:edge(b+a,b+c)
 for a,c in x['B']:edge(3*b+a,3*b+c)
 colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
 assert all(colour[v]!=colour[w] for v in range(5*b) for w in G[v])
 D=set(range(b))|{b+v for v in T}|{3*b+v for v in S}
 assert len(D)==3*b-len(C) and all(len(G[v]&D)<=1 for v in D)
 counts['physical_dissociation_certificates']+=1
 return G

for m in list(range(1,13))+[16,32,64,128]:
 x=common_neighbour_barrier(m);U=set(x['initial_U']);E=x['P']+x['Q'];X={12*j+t for j in range(m) for t in (1,5)};Y={12*j+t for j in range(m) for t in (7,11)}
 final=(U-X)|Y;Cfinal={12*j+3 for j in range(m)};Mfinal=[(12*j+2,12*j+3) for j in range(m)]
 G=physical(x,final,Cfinal,Mfinal);assert min(map(len,G))==2 and max(map(len,G))==3
 z=choose_matching(12*m,E,U,x['cover'],x['matching'],X,Y);assert not z['applicable'] and z['reason']=='constrained initial matching cannot saturate cover'
 assert z['hall']['hall_left']==[2,4] and z['hall']['hall_neighbours']==[3]
 for v in (range(len(G)) if m<=4 else [0,1,len(G)//2,len(G)-1]):
  root=next(w for w in range(len(G)) if w!=v);seen={root};todo=[root]
  while todo:
   for w in G[todo.pop()]-seen-{v}:seen.add(w);todo.append(w)
  assert len(seen)==len(G)-1;counts['physical_connectivity_deletions']+=1
 if m<=4:
  a=[x[k] for k in ('b','P','Q','B','colour')];best=best_initial_pair_batch(*a,U,x['operations']);assert best['minimum_covers_tested']==1 and best['certificate']['actual_cost']==2*m
  for S in subsets(range(2*m)):
   XX={x['operations'][i][1] for i in S};YY={x['operations'][i][2] for i in S};V=(U-XX)|YY
   # Independent path-component calculation, not the algorithm under test.
   adj={v:set() for v in V}
   for a,b in E:
    if a in V and b in V:adj[a].add(b);adj[b].add(a)
   unseen=set(V);cost=0
   while unseen:
    K={min(unseen)};todo=list(K)
    while todo:
     for v in adj[todo.pop()]-K:K.add(v);todo.append(v)
    cost+=len(K)//2;unseen-=K
   expected=2*m-sum(2*j in S and 2*j+1 in S for j in range(m));assert cost==expected
   out=choose_matching(12*m,E,U,x['cover'],x['matching'],XX,YY)
   assert out['applicable']==all(not (2*j in S and 2*j+1 in S) for j in range(m))
   counts['barrier_candidate_subsets']+=1
  counts['all_pair_family_optima']+=1
 counts['barrier_family_scales']+=1
 if m==1:examples.append(dict(name='all initial pairs miss a joint saving',model=x,result=z,final_U=sorted(final),final_cover=sorted(Cfinal),final_matching=Mfinal))

# Both endpoints of an original edge are charged once, not twice.
z=choose_matching(4,[(0,1)],{0,1},{0},[(0,1)],{0,1},{2,3},True)
assert z['applicable'] and z['credit']==1 and z['actual_cost']==0 and len(z['charged_edges'])==1
check(4,[(0,1)],{0,1},{0},[[(0,1)]],{0,1},{2,3},True)
counts['double_endpoint_single_charge_controls']=1

for m in list(range(1,13))+[16,32,64,128]:
 x=mixed_path_escape(m);U=set(x['initial_U']);E=x['P']+x['Q'];X={o[1] for o in x['operations']};Y={o[2] for o in x['operations']}
 z=choose_matching(12*m,E,U,x['cover'],x['matching'],X,Y,True);assert z['applicable'] and z['credit']==2*m and z['actual_cost']==0
 assert set(z['U'])==set(range(0,12*m,2));G=physical(x,z['U'],z['cover'],z['matching'])
 if m<=3:
  a=[x[k] for k in ('b','P','Q','B','colour')]
  old=best_initial_pair_batch(*a,U,x['operations']);new=best_initial_pair_batch(*a,U,x['operations'],True)
  assert old['minimum_covers_tested']==new['minimum_covers_tested']==1
  assert old['certificate']['actual_cost']==m and new['certificate']['actual_cost']==0
  counts['mixed_family_all_pair_optima']+=1
  for S in subsets(range(3*m)):
   XX={x['operations'][i][1] for i in S};YY={x['operations'][i][2] for i in S};final=(U-XX)|YY
   expected=sum(not (3*j in S and 3*j+1 in S) for j in range(m))+sum(3*j+2 not in S for j in range(m))
   from all_helper_optimization import score
   assert len(score(12*m,x['P'],x['Q'],final)[1])==expected
   counts['mixed_family_candidate_subsets']+=1
 counts['mixed_family_scales']+=1
 if m==1:examples.append(dict(name='both one-sided rules miss zero, mixed transfer reaches it',model=x,result=z))

# All14 stored previous gaps; endpoint costs safely prune impossible improvements.
from all_helper_optimization import score
from matching_credit_exchange import matching_credit_batch
rows=json.loads((ROOT/'develop/fixtures/matching-choice-seeded-gaps.json').read_text());benchmark=[]
for x in rows:
 args=x['args'];n=x['n'];E=args[1]+args[2];U=set(x['U']);ops=x['operations'];C=set(x['cover'])
 old=matching_credit_batch(*args,U,ops,C,x['matching']);assert old['certificate']['actual_cost']==x['old_cost']
 covers=list(minimum_covers(n,E,U));assert len(covers)==x['covers']
 actual=x['old_cost'];improvers=[]
 for S in subsets(range(len(ops))):
  XX={ops[i][1] for i in S};YY={ops[i][2] for i in S};cost=len(score(n,args[1],args[2],(U-XX)|YY)[1]);actual=min(actual,cost)
  if cost<x['old_cost']:improvers.append((S,XX,YY,cost))
  counts['stored_gap_candidate_subsets']+=1
 assert actual==x['true_cost']==x['old_cost']-1
 mode_results=[]
 for mixed in (False,True):
  witness=None;tested=0
  for S,XX,YY,cost in improvers:
   for Ctrial in covers:
    if not mixed and XX&Ctrial:continue
    out=choose_matching(n,E,U,Ctrial,x['matching'],XX,YY,mixed);tested+=1
    if out['applicable']:
     assert out['actual_cost']==actual;witness=dict(selected=sorted(S),certificate=out);break
   if witness:break
  best=actual if witness else x['old_cost'];mode_results.append(dict(allow_mixed=mixed,best_cost=best,improvement_witness=witness,choice_checks=tested))
  counts['stored_gap_matching_choice_checks']+=tested
  if witness:counts['stored_gap_mixed_resolved' if mixed else 'stored_gap_outside_resolved']+=1
 benchmark.append(dict(n=n,trial=x['trial'],old_cost=x['old_cost'],actual_cost=actual,modes=mode_results))
 counts['stored_gap_models']+=1
examples.append(dict(name='complete stored previous gap followup',models=benchmark))

# Literal optimization over all initial tight pairs in small physical instances.
from owner_matching_certificate import prepare
rng2=random.Random(13112637)
for n in (8,12,16):
 for trial in range(15):
  L=list(range(0,n,2));R=list(range(1,n,2));rng2.shuffle(L);rng2.shuffle(R)
  P=list(zip(L[::2],L[1::2]))+list(zip(R[::2],R[1::2]));rng2.shuffle(R);q=rng2.randrange(n//2+1);Q=list(zip(L[:q],R[:q]))
  order=[v for pair in zip(L,R) for v in pair];B=[]
  for off in range(0,n,4):
   K=order[off:off+4];B+=list(zip(K,K[1:]+K[:1]))
  colour=[v%2 for v in range(n)];args=[n//2,P,Q,B,colour];data=prepare(*args);U=set();ops=[]
  for i,(K,_) in enumerate(data['owner_components']):
   initial=set(rng2.sample(list(K),2));U|=initial;x=rng2.choice(sorted(initial));y=rng2.choice(sorted(set(K)-initial));ops.append([i,x,y])
  E=P+Q;Ms=maximum(U,E);nu=len(Ms[0]);covers=[C for C in subsets(U) if len(C)==nu and all(a in C or b in C for a,b in E if a in U and b in U)]
  assert {tuple(sorted(C)) for C in covers}=={tuple(sorted(C)) for C in minimum_covers(n,E,U)}
  for mixed in (False,True):
   expected=(-1,0)
   for S in subsets(range(len(ops))):
    XX={ops[i][1] for i in S};YY={ops[i][2] for i in S};final=(U-XX)|YY
    for C in covers:
     if not mixed and XX&C:continue
     for M in Ms:
      lost=[e for e in M if set(e)&XX];retired={v for e in lost for v in e if v in C};kept=C-retired
      if all(a in kept or b in kept for a,b in E if a in final and b in final):expected=max(expected,(len(lost),-len(S)))
      counts['literal_physical_pair_batch_tests']+=1
   result=best_initial_pair_batch(*args,U,ops,mixed);cert=result['certificate'];assert (cert['credit'],-len(cert['selected_candidates']))==expected
   physical(dict(b=n//2,P=P,Q=Q,B=B,colour=colour),cert['U'],cert['cover'],cert['matching']);counts['literal_physical_all_pair_optima']+=1

report=dict(scope='Original assertion-enabled checker. Exhaustive generic graphs through4; all maximum matchings, tight covers and arbitrary removals; all cross graphs through3+3; seeded larger and nonbipartite controls; positive matching-choice example; all-parameter physical common-neighbour barrier checked at16scales, all subsets for m<=4. Mixed-removal zero-cost escape at16scales and all subsets throughm3; all14 stored prior gaps checked by exact endpoint pruning and all-cover matching choice;90 all-pair physical optima independently enumerated. No unrestricted physical optimum or new universal numerical bound.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/matching-choice-exchange-check.json'));args=p.parse_args();Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
