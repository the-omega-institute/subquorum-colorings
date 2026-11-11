#!/usr/bin/env python3
"""Exhaustive physical small graphs: local-safe deletion implies global safety."""
import itertools,json,pathlib

def form(adj,S,domain):
 for x in domain-S:
  ns=adj[x]&S
  if len(ns)>=2:continue
  if not ns or not any(adj[y]&S for y in ns):return False
 return True

counts=dict(block_presentations=0,ambient_presentations=0,forming_sets=0,safe_deletions=0,necessary_conditions=0)
for n in range(1,5):
 pairs=list(itertools.combinations(range(n),2))
 for bits in range(1<<len(pairs)):
  base=[set() for _ in range(n+2)]
  for j,(a,b) in enumerate(pairs):
   if bits>>j&1:base[a].add(b);base[b].add(a)
  for pm in range(1<<n):
   P={i for i in range(n) if pm>>i&1};block=set(range(n));counts['block_presentations']+=1
   ep=[(p,x) for p in P for x in range(n,n+2)]+[(n,n+1)]
   for ext in range(1<<len(ep)):
    adj=[set(v) for v in base]
    for j,(a,b) in enumerate(ep):
     if ext>>j&1:adj[a].add(b);adj[b].add(a)
    counts['ambient_presentations']+=1
    for sm in range(1<<(n+2)):
     S={i for i in range(n+2) if sm>>i&1};C=S&block
     if not form(adj,S,set(range(n+2))):continue
     counts['forming_sets']+=1
     for x in block-(C|P):
      ns=adj[x]&C
      assert len(ns)>=2 or any((adj[y]&C) or y in P for y in ns)
     counts['necessary_conditions']+=1
     for v in C-P:
      Cv=C-{v}
      if not form(adj,Cv,block):continue
      if any(adj[p]&C and not adj[p]&Cv for p in C&P):continue
      assert form(adj,S-{v},set(range(n+2)))
      counts['safe_deletions']+=1
# Explicit necessity of activity preservation.
adj=[{1,4},{0,2},{1,3},{2},{0}];block=set(range(4));S=set(range(4))
assert form(adj,S,set(range(5))) and form(adj,S-{1},block)
assert not form(adj,S-{1},set(range(5)))
# The abstract finite cap test specializes to H with cap six.
rows=['11001','11010','00011','01111','10111'];adj=[set() for _ in range(10)]
for a,row in enumerate(rows):
 for b,bit in enumerate(row,5):
  if bit=='1':adj[a].add(b);adj[b].add(a)
P={0,1,5,6};block=set(range(10));h_candidates=0;min_choices=10
for cm in range(1<<10):
 C={i for i in block if cm>>i&1}
 if len(C)<=6:continue
 A=all(len(adj[x]&C)>=2 or any((adj[y]&C) or y in P for y in adj[x]&C) for x in block-(C|P))
 if not A:continue
 choices=[v for v in C-P if form(adj,C-{v},block) and all(not adj[p]&C or adj[p]&(C-{v}) for p in C&P)]
 assert choices;h_candidates+=1;min_choices=min(min_choices,len(choices))
C={0,1,2,5,6,7}
for v in C:
 assert any(not adj[x]&(C-{v}) or (len(adj[x]&(C-{v}))==1 and all(y not in P and not adj[y]&(C-{v}) for y in adj[x]&(C-{v}))) for x in block-((C-{v})|P))
report={'status':'PASS',**counts,'five_vertex_activity_obstruction':True,'H_cap_candidates':h_candidates,'H_minimum_safe_choices':min_choices,'H_protected_deletion_witnesses':6,'scope':'All simple blocks through order four, all boundary subsets, two outside vertices and all boundary interfaces; literal formation predicates. All H selections for the cap-six test and protected witnesses.'}
pathlib.Path('output/boundary-safe-composition-controls.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
