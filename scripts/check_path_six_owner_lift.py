#!/usr/bin/env python3
"""Physical owner certificates, heredity, and exact fixed-extraction ledgers."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
from functools import lru_cache
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from all_helper_optimization import path_cycle_owner_set,template_certificate,lift_certificate
from subcubic_partial_template import decompose
if not __debug__:raise RuntimeError('Assertions must be enabled')
counts=Counter();digest=hashlib.sha256()


def diss(g,S):return all(len(g[v]&S)<=1 for v in S)


def forms(g,S):
 return all(any(x in {c,a,b} and len({c,a,b}&S)==2
       for c in {x}|g[x] for a,b in combinations(g[c],2))
       for x in set(range(len(g)))-S)


def minimal(g,S):return forms(g,S) and all(not forms(g,S-{v}) for v in S)


def literal_beta(g):
 best=0
 for mask in range(1<<len(g)):
  S={v for v in range(len(g)) if mask>>v&1}
  if len(S)>best and diss(g,S):best=len(S)
 return best


def exact(g):
 adj=[sum(1<<u for u in ns) for ns in g]
 @lru_cache(None)
 def go(mask):
  if not mask:return 0
  v=max((i for i in range(len(g)) if mask>>i&1),key=lambda i:(adj[i]&mask).bit_count())
  ns=adj[v]&mask
  if not ns:return mask.bit_count()
  closed=ns|(1<<v);ans=max(go(mask&~(1<<v)),1+go(mask&~closed))
  while ns:
   bit=ns&-ns;ns-=bit;ans=max(ans,2+go(mask&~(closed|adj[bit.bit_length()-1])))
  return ans
 return go((1<<len(g))-1)


def model(b,core,Q):
 g=[set() for _ in range(5*b)];I=set(range(b));X=set(range(b,3*b));C=set(range(3*b,5*b));owner={}
 for i in range(b):
  for x in (b+2*i,b+2*i+1):
   c=x+2*b;owner[x]=c;g[i].add(x);g[x].add(i);g[x].add(c);g[c].add(x)
 for v,u in core+Q:g[v].add(u);g[u].add(v)
 return dict(g=g,I=I,X=X,C=C,owner=owner)


def check_template(m,optimize):
 g=m['g'];D,data=template_certificate(m);S=m['I']|m['C'];b=len(m['I'])
 assert diss(g,D) and len(D)>=(8*b+2)//3 and minimal(g,S)
 w=decompose(g,S)
 if optimize:
  beta=exact(g);assert beta>=len(D);counts['exact_template_optima']+=1
  lifted,rec=lift_certificate(g,S,w,beta)
  assert diss(g,lifted) and rec['bprime']<=b
  assert sum(rec['nonnegative_terms'])==5*len(g)-51*(len(S)-beta)
  counts['nonempty_template_lifts']+=bool(rec['bprime'])
  counts['proper_induced_extractions']+=rec['bprime']<b
 counts['physical_templates']+=1
 digest.update(json.dumps([len(g),sorted(D),data],sort_keys=True,default=lambda x:sorted(x)).encode()+b'\n')
 return g,S


def main():
 rng=random.Random(8611126)
 for n in range(13):
  path=[(i,i+1) for i in range(n-1)]
  for cyclic in (False,True):
   if cyclic and (not n or n%6):continue
   es=path+([(n-1,0)] if cyclic else [])
   for mask in range(1<<n):
    V={v for v in range(n) if mask>>v&1};sub=[(v,u) for v,u in es if {v,u}<=V]
    S,orders=path_cycle_owner_set(V,sub)
    assert len(S)>=(2*len(V)+2)//3 and all(sum(v in edge and bool(set(edge)-{v}&S) for edge in sub)<=1 for v in S)
    counts['induced_owner_subgraphs']+=1
 # Every small labelled subcubic bipartite graph, with every minimal set.
 for n in range(7):
  for a in range(n//2+1):
   es=list(product(range(a),range(a,n)))
   for mask in range(1<<len(es)):
    g=[set() for _ in range(n)]
    for j,(v,u) in enumerate(es):
     if mask>>j&1:g[v].add(u);g[u].add(v)
    if max(map(len,g),default=0)>3:continue
    beta=literal_beta(g);assert beta==exact(g)
    for bitset in range(1<<n):
     S={v for v in range(n) if bitset>>v&1}
     if not minimal(g,S):continue
     w=decompose(g,S)
     try:D,data=lift_certificate(g,S,w,beta)
     except ValueError:counts['nonapplicable_small_selections']+=1;continue
     assert diss(g,D) and 51*(len(S)-beta)<=5*n
     assert sum(data['nonnegative_terms'])==5*n-51*(len(S)-beta)
     counts['small_minimal_set_lifts']+=1
     counts['nonempty_retained_small_lifts']+=bool(data['retained'])
    counts['small_graphs']+=1
 # Balanced physical templates: owner colours also determine helper colours.
 for b in (2,4,6,8,16,32,64):
  side0=list(range(3*b,4*b));side1=list(range(4*b,5*b))
  for trial in range(6):
   rng.shuffle(side0);rng.shuffle(side1)
   order=[v for pair in zip(side0,side1) for v in pair]
   core=[(v,u) for v,u in zip(order,order[1:])]
   if trial%2 and b>=4:
    core=[(order[j],order[(j+1)%6]) for j in range(6)]
    core += [(order[j],order[j+1]) for j in range(6,len(order)-1)]
   wx=list(range(b,2*b));wy=list(range(2*b,3*b));rng.shuffle(wx);rng.shuffle(wy)
   Q=[(v,u) for v,u in zip(wx,wy) if rng.randrange(3)]
   m=model(b,core,Q)
   # Helpers each have two witnesses of one physical colour, since b is even.
   colours={v:0 if v in set(range(b//2))|set(range(2*b,3*b))|set(side0) else 1 for v in range(5*b)}
   assert all(colours[v]!=colours[u] for v in range(5*b) for u in m['g'][v])
   g,S=check_template(m,optimize=b<=6)
   if b==4 and trial in (1,3):
    # Retained selected edge and a genuine centre/leaf/private-witness triple.
    for tail,selected in (([{1},{0}],{0,1}),([{1},{0,2},{1,3},{2}],{0,1,3})):
     assert minimal(tail,selected)
     joined=[set(row) for row in g]+[{len(g)+u for u in row} for row in tail]
     T=S|{len(g)+v for v in selected};beta=exact(joined)
     D,data=lift_certificate(joined,T,decompose(joined,T),beta)
     assert diss(joined,D) and data['retained'] and 0<data['bprime']<=b
     assert all(not joined[v]&data['inner'] for v in data['retained'])
     counts['retained_exterior_template_lifts']+=1
 for n in (3,4,8,10):
  es=[(i,(i+1)%n) for i in range(n)]
  try:path_cycle_owner_set(range(n),es)
  except ValueError:counts['wrong_cycle_lengths_rejected']+=1
  else:raise AssertionError(n)
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/path-six-owner-lift-check.json');args=parser.parse_args()
 report={'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),
 'scope':'Path/6k owner construction, induced-subgraph heredity and physical fixed-extraction5/51 ledger. Literal optima for all small graph controls; exact recursion for templates through30vertices; larger models are actual dissociation/minimal-set certificates, not large exact optima. The general8b/3 template bound and sharp subcubic coefficient remain open.'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(report)
if __name__=='__main__':main()
