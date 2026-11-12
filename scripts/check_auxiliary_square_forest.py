from pathlib import Path
from collections import Counter,deque
from itertools import product
import sys,json,random,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from auxiliary_square_forest import certificate,rainbow_forest
from auxiliary_square_parity import certificate as prior
from all_helper_optimization import solve
from owner_matching_certificate import prepare,certificate as matching
if not __debug__:raise RuntimeError('Assertions must be enabled')
rng=random.Random(141126);counts=Counter();digest=hashlib.sha256();fixtures=[]

def rank(vertices,edges):
 adj={v:set() for v in vertices}
 for a,b in edges:adj[a].add(b);adj[b].add(a)
 unseen=set(vertices);k=0
 while unseen:
  k+=1;todo=[min(unseen)];seen=set(todo)
  while todo:
   for u in adj[todo.pop()]-seen:seen.add(u);todo.append(u)
  unseen-=seen
 return len(vertices)-k

# Independent literal optimum and all-subsets Rado rank formula on coloured
# multigraphs; parallel edges and loops are allowed in these algorithm controls.
for n in range(1,7):
 for trial in range(70):
  c=rng.randrange(1,6);m=rng.randrange(0,11)
  E=[dict(a=rng.randrange(n),b=rng.randrange(n),cycle=rng.randrange(c)) for _ in range(m)]
  x=rainbow_forest(range(n),E);best=0
  for mask in range(1<<m):
   I=[i for i in range(m) if mask>>i&1];counts['literal_coloured_edge_subsets']+=1
   if len({E[i]['cycle'] for i in I})<len(I):continue
   if rank(range(n),[(E[i]['a'],E[i]['b']) for i in I])==len(I):best=max(best,len(I))
  assert x['size']==best
  bound=c
  for mask in range(1<<c):
   J={j for j in range(c) if mask>>j&1}
   bound=min(bound,c-len(J)+rank(range(n),[(e['a'],e['b']) for e in E if e['cycle'] in J]))
   counts['literal_Rado_rank_subsets']+=1
  assert bound==best;counts['coloured_multigraphs']+=1

def check(P,Q,B,col,exact=False):
 n=len(col);b=n//2;x=certificate(b,P,Q,B,col);counts['templates']+=1
 assert x['applicable'];S=set(x['owners']);T=set(x['witnesses']);D=set(x['maximum_owner_set'])
 adj=[set() for _ in range(5*b)]
 def edge(a,z):adj[a].add(z);adj[z].add(a)
 for i,(a,z) in enumerate(P):edge(i,b+a);edge(i,b+z)
 for v in range(n):edge(b+v,3*b+v)
 for a,z in Q:edge(b+a,b+z)
 for a,z in B:edge(3*b+a,3*b+z)
 selected=set(range(b))|{b+v for v in T}|{3*b+v for v in S}
 assert len(selected)==x['beta_I_lower']>=(8*b+2)//3
 assert all(len(adj[v]&selected)<=1 for v in selected)
 assert S<=D and all(sum(v in e and set(e)<=D for e in B)<=1 for v in D)
 if n<=8:
  beta=0
  for mask in range(1<<n):
   Z={v for v in range(n) if mask>>v&1}
   if all(sum(v in e and set(e)<=Z for e in B)<=1 for v in Z):beta=max(beta,len(Z))
   counts['literal_owner_subsets']+=1
  assert len(D)==beta
 if exact:assert solve(b,P,Q,B)['beta_I']>=len(selected);counts['exact_all_helper_controls']+=1
 old=prior(b,P,Q,B,col)
 counts['beyond_prior_owner_size_criterion']+=not old['applicable']
 rf=x['rainbow_forest'];E=rf['ground'];sq=range(n//4)
 I=rf['indices'];assert len({E[i]['cycle'] for i in I})==len(I)
 assert rank(sq,[(E[i]['a'],E[i]['b']) for i in I])==len(I)
 R=set(range(len(E)))-set(rf['dual_unreachable'])
 assert rank(sq,[(E[i]['a'],E[i]['b']) for i in rf['dual_unreachable']])+len({E[i]['cycle'] for i in R})==len(I)
 # Reconstruct every projected ground edge and cycle weight from raw inputs.
 def comps(edges):
  aa=[set() for _ in range(n)]
  for a,z in edges:aa[a].add(z);aa[z].add(a)
  unseen=set(range(n));out=[]
  while unseen:
   part={min(unseen)};todo=list(part)
   while todo:
    for v in aa[todo.pop()]-part:part.add(v);todo.append(v)
   unseen-=part;out.append(part)
  return out,aa
 owner_parts,ba=comps(B);aux_parts,_=comps(P+Q)
 oi={v:i for i,C in enumerate(owner_parts) for v in C};ai={v:i for i,C in enumerate(aux_parts) for v in C}
 assert len(D)==sum((2*len(C))//3 if all(len(ba[v])==2 for v in C) else (2*len(C)+2)//3 for C in owner_parts)
 removed={v for z in x['closed_components'] for v in z['vertices']}
 exceptional={i:(2 if len(C)%6==4 else 1) for i,C in enumerate(owner_parts) if not C&removed and all(len(ba[v])==2 for v in C) and len(C)%3}
 expected={(oi[a],min(a,z),max(a,z),min(ai[a],ai[z]),max(ai[a],ai[z])) for a,z in B if oi[a] in exceptional and ai[a]!=ai[z]}
 observed={(e['cycle'],min(e['x'],e['y']),max(e['x'],e['y']),min(e['a'],e['b']),max(e['a'],e['b'])) for e in E}
 assert observed==expected and len(observed)==len(E)
 labels=sorted(exceptional);local_rng=random.Random(n+counts['templates'])
 masks=range(1<<len(labels)) if len(labels)<=8 else [local_rng.getrandbits(len(labels)) for _ in range(64)]
 for mask in masks:
  J={v for j,v in enumerate(labels) if mask>>j&1}
  assert 3*rank(sq,[(e['a'],e['b']) for e in E if e['cycle'] in J])>=sum(exceptional[v] for v in J)
  counts['physical_subset_rank_inequalities']+=1
 counts['dual_rank_cuts']+=1;counts['residual_forest_edges']+=len(I)
 counts['closed_four_components']+=sum(z['type']=='coincident C4' for z in x['closed_components'])
 counts['closed_eight_components']+=sum(z['type']=='two closed C4s' for z in x['closed_components'])
 assert 3*len(I)>=x['residual_deficit_thirds']
 counts['physical_certificates']+=1
 digest.update(json.dumps([P,Q,B,col,x],sort_keys=True).encode())
 return x

def aux(n):
 L=list(range(0,n,2));RR=list(range(1,n,2));rng.shuffle(L);rng.shuffle(RR);P=[];Q=[]
 for j in range(0,n//2,2):
  a,b=L[j:j+2];c,d=RR[j:j+2];P.extend([(a,b),(c,d)]);Q.extend([(a,c),(b,d)])
 return P,Q
for n in (4,8,12,16,20,24,28,32,64,128):
 specs=[[(n,True)],[(n,False)]]
 for k in (4,6,8,10):
  if k<n:specs.append([(k,True),(n-k,False)])
 if n>=16:specs.append([(8,True),(8,True)]+([(n-16,False)] if n>16 else []))
 specs.append([(4,True)]*(n//4))
 # Many exceptional cycles, mixtures and all-cycle deficits.
 for k in (8,10):
  if n>=k:
   t,r=divmod(n,k);specs.append([(k,True)]*t+([(r,False)] if r else []))
 for spec in specs:
  for trial in range(30):
   col=[v%2 for v in range(n)];L=list(range(0,n,2));RR=list(range(1,n,2));rng.shuffle(L);rng.shuffle(RR);order=[v for pair in zip(L,RR) for v in pair];B=[];offset=0
   for size,cyclic in spec:
    C=order[offset:offset+size];offset+=size
    B.extend(zip(C,C[1:]+C[:1]) if cyclic else zip(C,C[1:]))
   assert offset==n
   P,Q=aux(n);check(P,Q,list(B),col,exact=n<=8)
for model in json.loads((ROOT/'develop/fixtures/auxiliary-square-parity.json').read_text()):
 x=check(model['P'],model['Q'],model['B'],model['colour'],exact=True)
 fixtures.append({'name':model['name'],'certificate':x})
for model in json.loads((ROOT/'develop/fixtures/auxiliary-square-forest.json').read_text()):
 x=check(model['P'],model['Q'],model['B'],model['colour'])
 assert prior(model['b'],model['P'],model['Q'],model['B'],model['colour'])['applicable']==model['prior_owner_size']
 assert matching(prepare(model['b'],model['P'],model['Q'],model['B'],model['colour']))['feasible']==model['prior_K4_free']
 assert rank(range(2*model['b']),model['P']+model['Q']+model['B'])==2*model['b']-1
 fixtures.append({'name':model['name'],'certificate':x})
# Abstract, colour-free theorem controls. Enumerate every A-independent set;
# B is randomly relabelled with no prescribed physical colouring compatibility.
for n in (4,8,12,16):
 A=[(4*j+k,4*j+(k+1)%4) for j in range(n//4) for k in range(4)]
 patterns=[(),(0,),(1,),(2,),(3,),(0,2),(1,3)]
 for trial in range(90):
  order=list(range(n));rng.shuffle(order)
  spec=[n] if trial%3==0 else [4]*(n//4) if trial%3==1 else ([n-4,4] if n>4 else [4])
  B=[];offset=0
  for m in spec:
   C=order[offset:offset+m];offset+=m
   B.extend(zip(C,C[1:]+C[:1]) if trial%4 else zip(C,C[1:]))
  best=0
  for choices in product(patterns,repeat=n//4):
   Z={4*j+v for j,part in enumerate(choices) for v in part}
   if all(sum(v in e and set(e)<=Z for e in B)<=1 for v in Z):best=max(best,len(Z))
   counts['literal_abstract_independent_subsets']+=1
  assert best>=(n+2)//3;counts['abstract_colour_free_models']+=1
assert certificate(0,[],[],[],[])['beta_I_lower']==0
P=[(0,2),(1,3),(4,6),(5,7)];Q=[(2,1),(3,4),(6,5),(7,0)]
x=certificate(4,P,Q,[(v,v+1) for v in range(7)],[v%2 for v in range(8)])
assert not x['applicable'];counts['outside_auxiliary_criterion']=1
assert counts['beyond_prior_owner_size_criterion'] and counts['closed_four_components'] and counts['closed_eight_components'] and counts['residual_forest_edges']
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/auxiliary-square-forest-check.json');args=parser.parse_args()
report={'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),'critical_examples':fixtures,'scope':'All-owner auxiliary-square theorem, constructive physical certificates, independent literal coloured forest optima and dual rank cuts. Exact all-helper comparisons are confined to small controls; larger instances certify actual sets. General auxiliary cycles and sharp unrestricted graph coefficient remain open.'}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='critical_examples'}))
