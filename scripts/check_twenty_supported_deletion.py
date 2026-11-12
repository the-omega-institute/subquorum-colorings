#!/usr/bin/env python3
"""Independent local rules, explicit proof choices, and literal ambient stars."""
from pathlib import Path
from itertools import combinations
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from supported_local_deletion import supported
from twenty_supported_deletion import choose,thirteen_choice,ready_owners
from twenty_vertex_subcubic import block,cyclic_family
if not __debug__:raise RuntimeError('Assertions must be enabled')
A={12,13,16,19};B={14,15,17,18};H=set(range(4));X=set(range(4,12));P={4,12}
M={4:11,11:4,5:9,9:5,6:8,8:6,7:10,10:7}
COMP={4:5,5:4,6:7,7:6,8:9,9:8,10:11,11:10}
counts=Counter();branches=Counter();digest=hashlib.sha256()


def independent_block():
 g=[set() for _ in range(20)];cycle=[0,4,11,3,10,7,1,6,8,2,9,5]
 for v,u in zip(cycle,cycle[1:]+cycle[:1]):g[v].add(u);g[u].add(v)
 for x in range(5,12):g[x].add(x+8);g[x+8].add(x)
 for L,R in (({12,13},{16,19}),({14,15},{17,18})):
  for v in L:
   for u in R:g[v].add(u);g[u].add(v)
 return g


def literal_supported(g,C,v):
 # Deliberately separate the three tests; record activity before deleting v.
 if v not in C-P:return False
 ns=sorted(g[v]&C)
 if not ns:return False
 for u in ns:
  if len(g[u]&C)<=1:return False
 for x in g[v]-C:
  remaining=(g[x]&C)-{v}
  if len(remaining)>=2:continue
  if len(remaining)!=1:return False
  u=next(iter(remaining))
  if not g[u]&C:return False
 return True


def forms(g,S):
 return all(any(x in {c,a,b} and len({c,a,b}&S)==2
       for c in {x}|g[x] for a,b in combinations(g[c],2))
       for x in set(range(len(g)))-S)


def main():
 g=independent_block();assert g==block()[0]
 for C in map(set,combinations(range(20),13)):
  ready=ready_owners(g,C);D=X-C;h=len(C&H)
  for v in C-P:
   assert literal_supported(g,C,v)==supported(g,C,P,v)
   counts['independent_vertex_tests']+=1
  # Ready-owner matching-pair budget and helper obstruction counting.
  if not any(literal_supported(g,C,v) for v in ready):
   assert len(D)>=len(ready);counts['ready_budget_cases']+=1
   for v in ready:
    x=v-8;mate=M[x]
    if (x in D)+(mate in D)==1:
     assert (x-4)//2 not in C
     if x in D:assert not g[mate]&C
     counts['single_omission_rules']+=1
    if h==3:
     j=next(iter(H-C));ob={mate} if (x-4)//2==j else {x,COMP[x],mate}
     assert ob<=D;counts['three_helper_owner_obstructions']+=1
    if h==4:
     assert not C&{x,COMP[x],mate};counts['four_helper_owner_obstructions']+=1
  if not any(literal_supported(g,C,v) for v in C&H):
   active=sum(bool(g[v]&C) for v in C&H)
   assert active<=len(D);counts['helper_budget_cases']+=1
   if h==3 and len(D)==2:
    j=next(iter(H-C));assert D==({6,7},{4,5},{10,11},{8,9})[j]
   if h==4 and len(D)==3:
    assert D in ({4,5,8},{4,5,10},{6,7,11},{6,7,9},
                 {7,8,9},{4,8,9},{6,10,11},{5,10,11})
  v,branch=thirteen_choice(g,C);assert literal_supported(g,C,v)
  branches[branch]+=1;counts['thirteen_sets']+=1
  for x in set(range(20))-C:
   assert literal_supported(g,C|{x},v);counts['single_addition_steps']+=1
  digest.update(bytes([v]));digest.update(branch.encode()+b'\n')
 # Check the expanded analytic implications under their weaker local hypotheses,
 # without assuming the globally impossible absence of every supported vertex.
 def case_check(C,v):
  assert len(C)==13 and literal_supported(g,C,v)
  counts['expanded_analytic_branch_controls']+=1
  digest.update(json.dumps([sorted(C),v]).encode()+b'\n')
 for a in (16,19):
  selected_A=A-{a}
  for pair in combinations(B,2):
   for z in (4,6,7,8,10,11):
    v=1 if z in (4,7,11) else 3
    # D={5,z}, failure at ready13 forces17omitted and helpers1,3 selected.
    if 17 not in pair:
     case_check({1,3}|(X-{5,z})|selected_A|set(pair),v)
    # D={9,z} with helper2omitted is excluded by exactly the same table.
    case_check({1,3}|(X-{9,z})|selected_A|set(pair),v)
   if a==16:case_check({1,2}|(X-{6,9})|selected_A|set(pair),1)
   if 14 not in pair:
    case_check({1,2}|(X-{8,9})|selected_A|set(pair),18 if 18 in pair else 17)
 # Three-helper branch: B omits17or18 and has ready owners14,15.
 for pair in combinations(A,2):
  for omitted in (17,18):
   for z in (4,5,6,7,9,11):
    C={0,2,3}|(X-{8,10,z})|set(pair)|(B-{omitted})
    case_check(C,2 if z in (4,7,11) else 3)
 # Explicit obstruction-union tables, using only specified pair maps.
 types={'AL':{16,19},'AR':{13},'BL':{17,18},'BR':{14,15}}
 def union(owners,j):
  return set().union(*({M[v-8]} if (v-12)//2==j else
                   {v-8,COMP[v-8],M[v-8]} for v in owners))
 assert [len(union({13,16,19},j)) for j in range(4)]==[6,7,6,5]
 assert [len(union(B,j)) for j in range(4)]==[7,6,6,6]
 table=[]
 for a,b,expected in (('AL','BL',[8,8,6,6]),('AL','BR',[7,6,6,6]),
                       ('AR','BL',[6,7,6,5]),('AR','BR',[5,5,7,7])):
  row=[len(union(types[a]|types[b],j)) for j in range(4)]
  assert row==expected;table.append(row)
 counts['forced_union_table_entries']=24
 rng=random.Random(12211126)
 for j in range(3000):
  n=rng.randrange(9);ambient=[set(row) for row in g]+[set() for _ in range(n)]
  for a,b in combinations(range(20,20+n),2):
   if rng.randrange(2):ambient[a].add(b);ambient[b].add(a)
  for p in P:
   for u in range(20,20+n):
    if rng.randrange(2):ambient[p].add(u);ambient[u].add(p)
  if j%2:ambient[4].add(12);ambient[12].add(4)
  C=set(rng.sample(range(20),rng.randrange(13,21)))
  S=C|{u for u in range(20,20+n) if rng.randrange(2)}
  v,branch=choose(g,C);assert literal_supported(g,C,v)
  if forms(ambient,S):
   assert forms(ambient,S-{v});counts['literal_ambient_safe_deletions']+=1
  counts['arbitrary_ambient_models']+=1
 # The lower certificates and local cap simultaneously apply on large cycles.
 for r in list(range(1,17))+[32,64,128,256]:
  model=cyclic_family(r);S=model['selected'];physical=model['g']
  assert len(S)==12*r
  for i in range(r):
   C=set(rng.sample(range(20),13));v,branch=choose(g,C)
   assert 20*i+v not in {20*i+4,20*i+12}
   assert all(physical[20*i+u]=={20*i+w for w in g[u]}
              for u in range(20) if u not in P)
   counts['cyclic_block_neighbourhood_checks']+=1
  counts['cyclic_family_certificates']+=1
 parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/twenty-supported-deletion-check.json');args=parser.parse_args()
 report={'counts':dict(sorted(counts.items())),'proof_branches':dict(sorted(branches.items())),
  'deterministic_sha256':digest.hexdigest(),
  'scope':'Written local case proof establishes the13set lemma; supported deletion and upward closure give an all-ambient cap12, hence exact SF(G_r)=12r. This checker independently scores the local rules and explicit case choices and literal stars in seeded ambient extensions. No unrestricted large exact-SF solver or Lean execution.'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(report)
if __name__=='__main__':main()
