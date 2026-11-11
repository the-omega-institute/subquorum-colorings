import itertools, random, json
stats=dict(graphs=0,minimal_sets=0,choices=0)
def check(k,l,edges):
 n=k+l; full=(1<<n)-1; A=(1<<k)-1; adj=[0]*n
 for v,w in edges: adj[v]|=1<<w; adj[w]|=1<<v
 def vs(m): return [v for v in range(n) if m>>v&1]
 def covered(x,s):
  ns=adj[x]&s
  return ns.bit_count()>=2 or any(adj[y]&s for y in vs(ns))
 def forming(s): return all(covered(x,s) for x in vs(full^s))
 def diss(s): return all((adj[x]&s).bit_count()<=1 for x in vs(s))
 forms=[forming(s) for s in range(1<<n)]
 beta=max(s.bit_count() for s in range(1<<n) if diss(s))
 for s in range(1<<n):
  if not forms[s] or any(forms[s^(1<<v)] for v in vs(s)): continue
  stats['minimal_sets']+=1
  assert 10*(s.bit_count()-beta)<=n
  # Components of size at most 2, independently found by flood fill.
  R=0; unseen=s
  while unseen:
   todo=unseen&-unseen; comp=0
   while todo:
    bit=todo&-todo; todo^=bit; v=bit.bit_length()-1; comp|=bit
    todo|=adj[v]&s&~comp
   unseen&=~comp
   if comp.bit_count()<=2:R|=comp
  C=s&~R; isolates=[v for v in vs(R) if not adj[v]&s]
  options={}
  for v in vs(C):
   actual=[x for x in vs(full^s) if not covered(x,s^(1<<v))]
   pred=[]
   for x in vs(full^s):
    ns=adj[x]&s
    typ=ns==1<<v or (ns.bit_count()==2 and ns>>v&1 and any(ns==((1<<v)|(1<<i)) for i in isolates))
    third=[z for z in vs(ns) if ns==1<<z and adj[z]&s==1<<v]
    if typ or third:pred.append(x)
   assert set(actual)==set(pred) and actual
   options[v]=[(z,x) for x in actual for z in vs(adj[x]&s) if adj[x]&s==1<<z and adj[z]&s==1<<v]
  centers=[v for v in vs(C) if options[v]]
  # Exercise every type-3 choice; residual witnesses also exhaustively varied.
  for tc in itertools.product(*(options[v] for v in centers)):
   triples=[(v,z,x) for v,(z,x) in zip(centers,tc)]
   used=[q for t in triples for q in t]; assert len(used)==len(set(used))
   U=vs(C&~sum(1<<v for v in centers)&~sum(1<<z for _,z,_ in triples))
   opts=[]
   for v in U:
    opts.append([x for x in vs(full^s) if not covered(x,s^(1<<v)) and adj[x]>>v&1])
    assert opts[-1]
   for ws in itertools.product(*opts):
    stats['choices']+=1
    assert len(set(ws)|{x for _,_,x in triples})==len(ws)+len(triples)
    h={i:sum(bool(adj[x]>>i&1) for x in ws) for i in isolates}
    a=sum(t==1 for t in h.values());b=sum(t>=2 for t in h.values());p=len(triples);u=len(U)
    assert n>=3*p+2*u+a+b and u>=a+2*b
    sizes=[[],[]]
    T=s|sum(1<<x for x in ws)|sum(1<<x for _,_,x in triples)
    for side in (A,full^A):
     D=R&~sum(1<<i for i in isolates if side>>i&1 and h[i])
     for c,z,x in triples:D|=(1<<z)|(1<<(c if side>>c&1 else x))
     for v,x in zip(U,ws):
      if side>>v&1:D|=(1<<v)|(1<<x)
     E=(T&side)|(R&~side&~sum(1<<i for i in isolates if h[i]>=2))
     assert diss(D),('first',k,l,edges,s,triples,U,ws,D)
     assert diss(E),('second',k,l,edges,s,triples,U,ws,E)
     sizes[0].append(D.bit_count());sizes[1].append(E.bit_count())
    assert sum(sizes[0])==2*s.bit_count()-a-b
    assert sum(sizes[1])==2*s.bit_count()-p-b
 stats['graphs']+=1
for n in range(1,8):
 for k in range(n//2+1):
  l=n-k; possible=list(itertools.product(range(k),range(k,n)))
  for mask in range(1<<len(possible)):
   check(k,l,[e for j,e in enumerate(possible) if mask>>j&1])
 print(n,stats,flush=True)
rng=random.Random(11011)
for _ in range(300):
 n=rng.randrange(8,12);k=rng.randrange(1,n);q=rng.random()
 check(k,n-k,[(v,w) for v in range(k) for w in range(k,n) if rng.random()<q])
print('FINAL',json.dumps(stats),flush=True)
