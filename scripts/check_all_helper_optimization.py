#!/usr/bin/env python3
"""Literal physical controls for the all-helper expression and sharp loss."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from functools import lru_cache
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from all_helper_optimization import solve,score
if not __debug__:raise RuntimeError('Assertions must be enabled')
counts=Counter();digest=hashlib.sha256()


def model(b,P,Q,B):
 n=5*b;g=[set() for _ in range(n)]
 def add(a,c):g[a].add(c);g[c].add(a)
 for i,pair in enumerate(P):
  for x in pair:add(i,b+x);add(b+x,3*b+x)
 for a,c in Q:add(b+a,b+c)
 for a,c in B:add(3*b+a,3*b+c)
 return g


def diss(g,D):return all(len(g[v]&D)<=1 for v in D)


def literal(g,b):
 n=len(g);adj=[sum(1<<u for u in ns) for ns in g];valid=bytearray(1<<n);valid[0]=1
 beta=forced=0;wit=0
 for mask in range(1<<n):
  if mask:
   bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit;ns=adj[v]&rest
   valid[mask]=bool(valid[rest] and ns.bit_count()<=1 and (not ns or not adj[ns.bit_length()-1]&rest))
  if valid[mask]:
   k=mask.bit_count()
   if k>beta:beta,wit=k,mask
   if mask&((1<<b)-1)==(1<<b)-1:forced=max(forced,k)
 counts['literal_physical_subsets']+=1<<n
 return beta,forced,{v for v in range(n) if wit>>v&1}


def matchings(V):
 V=list(V)
 if not V:yield [];return
 v=V[0]
 yield from matchings(V[1:])
 for j,u in enumerate(V[1:],1):
  for rest in matchings(V[1:j]+V[j+1:]):yield [(v,u)]+rest


def check(b,P,Q,B):
 g=model(b,P,Q,B);rec=solve(b,P,Q,B)
 D=set(range(b))|{b+x for x in rec['witnesses']}|{3*b+c for c in rec['owners']}
 beta,forced,opt=literal(g,b)
 assert diss(g,D) and len(D)==rec['beta_I']==forced
 assert forced==3*b-len(rec['matching'])
 assert 0<=beta-forced<=b
 replaced=set(range(b))|(opt&set(range(3*b,5*b)))
 assert diss(g,replaced) and len(replaced)>=beta-b
 counts['templates']+=1;counts['nonzero_forcing_loss']+=beta>forced;counts['forcing_loss_b_attained']+=beta-forced==b
 counts['P_Q_duplicate_models']+=bool(set(map(frozenset,P))&set(map(frozenset,Q)))
 counts['owner_degree_above_two_models']+=any(sum(v in e for e in B)>2 for v in range(2*b))
 digest.update(json.dumps([b,P,Q,B,beta,forced,rec],sort_keys=True).encode()+b'\n')


def main():
 for b in range(3):
  P=[(2*i,2*i+1) for i in range(b)];es=list(combinations(range(2*b),2))
  for mask in range(1<<len(es)):
   B=[e for j,e in enumerate(es) if mask>>j&1]
   for Q in matchings(range(2*b)):check(b,P,Q,B)
 rng=random.Random(2811126)
 for j in range(40):
  b=3;P=[(2*i,2*i+1) for i in range(b)];V=list(range(2*b));rng.shuffle(V)
  Q=[tuple(V[k:k+2]) for k in range(0,len(V),2) if rng.randrange(2)]
  B=[e for e in combinations(range(2*b),2) if rng.randrange(4)==0]
  check(b,P,Q,B)
 # The audited20vertex family base is a physical target model.
 b=4;P=[(2*i,2*i+1) for i in range(b)];Q=[(0,7),(1,5),(2,4),(3,6)]
 B=[(a,c) for L,R in (((0,1),(4,7)),((2,3),(5,6))) for a in L for c in R]
 check(b,P,Q,B)
 # Large forcing-loss witnesses: actual sets and per-P5 structural optima.
 for b in (0,1,2,3,4,8,16,32,64,128):
  P=[(2*i,2*i+1) for i in range(b)];g=model(b,P,[],[])
  D=set(range(b,5*b));F=set(range(b))|set(range(3*b,5*b))
  assert len(D)==4*b and diss(g,D) and len(F)==3*b and diss(g,F)
  counts['large_sharp_loss_certificates']+=1
 # The sufficient owner class: paths and6kcycles, scored without exponential
 # enumeration of allU. P/Q may have duplicates; the resultingA stays bipartite.
 for b in range(1,33):
  P=[(2*i,2*i+1) for i in range(b)];V=list(range(2*b));rng.shuffle(V)
  Q=[tuple(V[k:k+2]) for k in range(0,len(V),2)]
  for cyclic in (False,True):
   length=(2*b//6)*6 if cyclic else 2*b
   B=[(i,i+1) for i in range(max(0,length-1))]
   if cyclic and length:B.append((length-1,0))
   if cyclic:S={i for i in range(length) if i%3!=2}|set(range(length,2*b))
   else:S={i for i in range(2*b) if i%3!=2}
   assert len(S)>=(4*b+2)//3
   T,M=score(2*b,P,Q,set(range(2*b))-S);g=model(b,P,Q,B)
   D=set(range(b))|{b+x for x in T}|{3*b+c for c in S}
   assert diss(g,D) and len(D)>=2*b+(len(S)+1)//2 >=(8*b+2)//3
   counts['path_or_6k_cycle_certificates']+=1
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/all-helper-optimization-check.json');args=parser.parse_args()
 report={'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),'scope':'Exact literal unrestricted/all-helper optima on686models; large sharp-loss and owner-class instances are explicit physical certificates, not large unrestricted searches. General8b/3 remainsopen; helperforcingloss bound and matching identity have written proofs.'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(report)
if __name__=='__main__':main()
