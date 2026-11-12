#!/usr/bin/env python3
"""Independent phase, physical-set, exact optimum and fixed-extraction controls."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from functools import lru_cache
import argparse, hashlib, json, random, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from owner_matching_certificate import prepare, materialize, certificate, sat, lift_certificate
from all_helper_optimization import solve
from subcubic_partial_template import decompose
if not __debug__:raise RuntimeError('Assertions must be enabled')
counts=Counter();digest=hashlib.sha256()

def physical(b,P,Q,B):
 g=[set() for _ in range(5*b)]
 for i,pair in enumerate(P):
  for x in pair:g[i].add(b+x);g[b+x].add(i);g[b+x].add(3*b+x);g[3*b+x].add(b+x)
 for a,c in Q:g[b+a].add(b+c);g[b+c].add(b+a)
 for a,c in B:g[3*b+a].add(3*b+c);g[3*b+c].add(3*b+a)
 return g

def diss(g,D):return all(len(g[v]&D)<=1 for v in D)

def literal(g,b):
 beta=forced=0
 for mask in range(1<<len(g)):
  D={i for i in range(len(g)) if mask>>i&1}
  if diss(g,D):
   beta=max(beta,len(D))
   if set(range(b))<=D:forced=max(forced,len(D))
 counts['literal_physical_subsets']+=1<<len(g)
 return beta,forced

def exact(g):
 a=[sum(1<<u for u in row) for row in g]
 @lru_cache(None)
 def go(M):
  if not M:return 0
  v=max((v for v in range(len(g)) if M>>v&1),key=lambda v:(a[v]&M).bit_count())
  ns=a[v]&M;closed=ns|(1<<v)
  if not ns:return M.bit_count()
  best=max(go(M&~(1<<v)),1+go(M&~closed))
  for u in range(len(g)):
   if ns>>u&1:best=max(best,2+go(M&~(closed|a[u])) )
  return best
 return go((1<<len(g))-1)

def forms(g,S):
 return all(any(x in {c,a,b} and len({c,a,b}&S)==2 for c in {x}|g[x] for a,b in combinations(g[c],2)) for x in set(range(len(g)))-S)

def matchings(V):
 if not V:yield [];return
 v,*rest=V
 yield from matchings(rest)
 for u in rest:
  for M in matchings([x for x in rest if x!=u]):yield [(v,u)]+M

def unsat_check(clauses,obstruction):
 if 'empty_clause' in obstruction:assert not clauses[obstruction['empty_clause']];return
 edges=set()
 for clause in clauses:
  if not clause:continue
  a,b=(clause*2)[:2] if len(clause)==1 else clause
  edges.add((2*a[0]+a[1],(2*b[0]+b[1])^1));edges.add((2*b[0]+b[1],(2*a[0]+a[1])^1))
 v=obstruction['variable']
 for name,start,end in [('zero_to_one',2*v,2*v+1),('one_to_zero',2*v+1,2*v)]:
  path=obstruction[name];assert path[0]==start and path[-1]==end
  assert all((a,b) in edges for a,b in zip(path,path[1:]))
 counts['unsat_path_certificates']+=1

def check(b,P,Q,B,colour,do_exact=False,do_literal=False,all_phases=True):
 data=prepare(b,P,Q,B,colour);rec=certificate(data);g=physical(b,P,Q,B)
 assert all(len(row)<=3 for row in g)
 variables=len(data['choices']);sols=0
 if all_phases:
  for values in product((0,1),repeat=variables):
   x=materialize(data,values);W=set(x['matched']);adj={v:set() for v in W}
   for a,c in x['edges']:adj[a].add(c);adj[c].add(a)
   bad={tuple(sorted({v}|adj[v])) for v in W if len(adj[v])==3 and all(adj[v]-{u}<=adj[u] for u in adj[v])}
   assert bad=={tuple(K) for K in x['K4']}
   good=not bad;formula=all(not all(values[v]==p for v,p in clause) for clause in data['clauses'])
   assert good==formula;sols+=good;counts['independent_K4_phase_checks']+=1
  assert rec['feasible']==bool(sols)
 if rec['feasible']:
  D=set(range(b))|{b+v for v in rec['witnesses']}|{3*b+v for v in rec['owners']}
  assert diss(g,D) and len(D)==rec['beta_I_lower']>=rec['bound']>=(8*b+2)//3
  colours=dict(rec['colouring']);xx=materialize(data,rec['values'])
  assert all(colours[a]!=colours[c] for a,c in xx['edges'])
  counts['physical_certificates']+=1
  counts['positive_odd_path_bonus']+=rec['bound']>(8*b+2)//3
 else:unsat_check(data['clauses'],rec['obstruction']);counts['method_unsat']+=1
 counts['binary_K4_clauses']+=sum(len(c)==2 for c in data['clauses'])
 if do_exact:
  optimum=solve(b,P,Q,B)['beta_I'];assert not rec['feasible'] or optimum>=rec['beta_I_lower']
  counts['exact_all_helper_optima']+=1
  if do_literal:
   beta,forced=literal(g,b);assert forced==optimum and beta>=forced;counts['literal_optima']+=1
 counts['templates']+=1
 digest.update(json.dumps([b,P,Q,B,colour,rec],sort_keys=True).encode()+b'\n')
 return g,rec

def main():
 rng=random.Random(3211126)
 # Every clause subset with <=2 Boolean variables, independently truth-tabled.
 for k in range(3):
  atoms=list(product(range(k),(0,1)));pool=[[]]+[[a] for a in atoms]+[[a,b] for a,b in combinations(atoms,2) if a[0]!=b[0]]
  for mask in range(1<<len(pool)):
   clauses=[c for j,c in enumerate(pool) if mask>>j&1];values,ob=sat(k,clauses)
   truth=[x for x in product((0,1),repeat=k) if all(not all(x[v]==p for v,p in c) for c in clauses)]
   assert (values is not None)==bool(truth)
   if values is None:unsat_check(clauses,ob)
   else:assert tuple(values) in truth
   counts['exhaustive_2SAT_models']+=1
 # All physical colour assignments, Q matchings and owner maxdegree2 graphs b<=2.
 for b in range(3):
  P=[(2*i,2*i+1) for i in range(b)]
  for helper_colours in product((0,1),repeat=b):
   col=[c for c in helper_colours for _ in range(2)];es=[e for e in combinations(range(2*b),2) if col[e[0]]!=col[e[1]]]
   for Q in matchings(list(range(2*b))):
    if any(col[a]==col[c] for a,c in Q):continue
    for mask in range(1<<len(es)):
     B=[e for j,e in enumerate(es) if mask>>j&1]
     if any(sum(v in e for e in B)>2 for v in range(2*b)):continue
     check(b,P,Q,B,col,True,True)
 # Random partial templates, including odd paths, duplicate Q/B occurrences and mixed cores.
 for b in range(3,9):
  P=[(2*i,2*i+1) for i in range(b)]
  for trial in range(45):
   col=[c for c in [rng.randrange(2) for _ in range(b)] for _ in (0,1)]
   left=[v for v in range(2*b) if col[v]==0];right=[v for v in range(2*b) if col[v]==1]
   rng.shuffle(left);rng.shuffle(right);Q=[(a,c) for a,c in zip(left,right) if rng.randrange(4)]
   es=[(a,c) for a in left for c in right];rng.shuffle(es);B=[];degree=Counter()
   for a,c in es:
    if degree[a]<2 and degree[c]<2 and rng.randrange(3)==0:B.append((a,c));degree[a]+=1;degree[c]+=1
   check(b,P,Q,B,col,do_exact=b<=4 and trial<18,do_literal=b==3 and trial<8)
 # Auxiliary single long cycles have no four-cycle, with arbitrary even owner cycles.
 for b in (4,6,8,10,16,32,64,128):
  n=2*b;P=[(v,v+1) for v in range(0,n,2)];col=[(v//2)%2 for v in range(n)]
  Q=[(v,(v+1)%n) for v in range(1,n,2)]
  left=[v for v in range(n) if col[v]==0];right=[v for v in range(n) if col[v]==1]
  for trial in range(6):
   rng.shuffle(left);rng.shuffle(right);order=[v for pair in zip(left,right) for v in pair]
   if trial==0:B=[(order[j],order[(j+1)%n]) for j in range(n)]
   elif trial==1:B=[(order[j],order[j+1]) for j in range(n-1)]
   elif trial==2:B=[(order[j],order[j+1]) for j in range(n-2)] # odd path plus isolate
   else:
    B=[];start=0
    for size in (4,8,10,n):
     if start>=n:break
     size=min(size,n-start)
     B +=[(order[start+j],order[start+(j+1)%size]) for j in range(size)] if size>=4 else [(order[start],order[start+1])]
     start+=size
   g,rec=check(b,P,Q,B,col,do_exact=b==4 and trial<2,all_phases=b<=16)
   assert rec['feasible'];counts['no_auxiliary_C4_certificates']+=1
   if b<=6:
    S=set(range(b))|set(range(3*b,5*b));beta=exact(g)
    assert forms(g,S) and all(not forms(g,S-{v}) for v in S)
    physical_colour={i:1-col[P[i][0]] for i in range(b)}
    physical_colour.update({b+v:col[v] for v in range(2*b)})
    physical_colour.update({3*b+v:1-col[v] for v in range(2*b)})
    D,lift=lift_certificate(g,S,decompose(g,S),beta,physical_colour)
    assert D is not None and diss(g,D)
    assert sum(lift['nonnegative_terms'])==5*len(g)-51*(len(S)-beta)
    counts['nonempty_template_lifts']+=bool(lift['bprime'])
 # Independent exact fixed obstruction and analytic eight-case table.
 fixture=json.loads((ROOT/'develop/fixtures/owner-matching-obstruction.json').read_text())
 m=fixture['model'];b=6;P=m['P'];Q=m['Q'];B=m['B'];col=[0]*6+[1]*6
 g,rec=check(b,P,Q,B,col,do_exact=True);assert not rec['feasible']
 optimum=solve(b,P,Q,B);assert optimum['beta_I']==17
 D=set(range(6))|{6+v for v in optimum['witnesses']}|{18+v for v in optimum['owners']};assert len(D)==17 and diss(g,D)
 for row in fixture['all_helper_maximal_U_table']:
  U=set().union(*(set(fixture['A_diagonals'][i][p]) for i,p in enumerate(row['phases'])))
  assert len(U)==6 and not any(set(e)<=U for e in P+Q)
  S=set(range(12))-U;a,c,z=row['owner_P3'];assert {a,c,z}<=S and {frozenset((a,c)),frozenset((c,z))}<=set(map(frozenset,B))
  counts['analytic_all_helper_obstruction_rows']+=1
 data=prepare(b,P,Q,B,col)
 for row in fixture['phases']:
  x=materialize(data,[row['phase']]);es=set(map(frozenset,x['edges']));T=set(row['independent']);K=set(x['K4'][0]);cycle=row['exterior_cycle']
  assert len(T)==4 and not any(e<=T for e in es)
  assert len(cycle)==8 and set(cycle)==set(range(12))-K
  assert all(frozenset((a,c)) in es for a,c in zip(cycle,cycle[1:]+cycle[:1]))
  for p,chord in enumerate(row['blocking_chords']):assert set(chord)<=set(cycle[p::2]) and frozenset(chord) in es
  for size in range(5,13):
   assert not any(not any(e<=set(T) for e in es) for T in combinations(range(12),size))
  counts['exact_independence_obstruction_phases']+=1
 # Physical fixed-extraction ledgers on every minimal set in small bipartite graphs.
 for n in range(7):
  for a in range(n//2+1):
   es=list(product(range(a),range(a,n)))
   for mask in range(1<<len(es)):
    g=[set() for _ in range(n)]
    for j,(v,u) in enumerate(es):
     if mask>>j&1:g[v].add(u);g[u].add(v)
    if max(map(len,g),default=0)>3:continue
    beta=exact(g);colour={v:int(v>=a) for v in range(n)}
    for M in range(1<<n):
     S={v for v in range(n) if M>>v&1}
     if not forms(g,S) or any(forms(g,S-{v}) for v in S):continue
     D,data=lift_certificate(g,S,decompose(g,S),beta,colour)
     if D is None:counts['nonapplicable_small_minimal_sets']+=1;continue
     assert diss(g,D) and sum(data['nonnegative_terms'])==5*n-51*(len(S)-beta)
     counts['small_minimal_set_lifts']+=1
    counts['small_graphs']+=1
 assert counts['binary_K4_clauses'] and counts['method_unsat'] and counts['positive_odd_path_bonus']
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/owner-matching-certificate-check.json');args=parser.parse_args()
 report={'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),'scope':'General written owner-matching/odd-path theorem and exact 2SAT criterion for its specified family. K4 avoidance is sufficient only. All-phase physical and exact small controls; larger certificates do not assert large optimality. Fixed30vertex obstruction has beta_I17 and both route independence numbers4, with an analytic eight-row upper bound. General8b/3, universal graph sharp coefficient and grid questions remainopen.'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report))
if __name__=='__main__':main()
