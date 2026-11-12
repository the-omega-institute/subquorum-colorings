from pathlib import Path
from collections import Counter
from itertools import product
import sys,json,random,hashlib,argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
from auxiliary_square_parity import certificate
from sharp_all_helper import physical
from owner_matching_certificate import prepare,certificate as previous
from all_helper_optimization import solve
if not __debug__:raise RuntimeError('Assertions must be enabled')
rng=random.Random(131126);counts=Counter();digest=hashlib.sha256();fixtures=[]
def check(P,Q,B,col,exact=False):
 n=len(col);b=n//2;x=certificate(b,P,Q,B,col);counts['templates']+=1
 if not x['applicable']:
  counts['outside_owner_size_criterion']+=1;return x
 if x['owner_beta']<(2*n)//3:
  counts['newly_admitted_below_floor_two_thirds']+=1
  counts['newly_admitted_residue_'+str(n%6)]+=1
 g,c=physical(dict(b=b,P=P,Q=Q,B=B,index_colours=col));D=set(range(b))|{b+v for v in x['witnesses']}|{3*b+v for v in x['owners']}
 assert len(D)==x['beta_I_lower']>=(8*b+2)//3 and all(len(g[v]&D)<=1 for v in D)
 dd=set(x['maximum_owner_set']);bb=[set() for _ in range(n)]
 for a,z in B:bb[a].add(z);bb[z].add(a)
 assert all(len(bb[v]&dd)<=1 for v in dd)
 if n<=8:
  best=0
  for mask in range(1<<n):
   Z={v for v in range(n) if mask>>v&1}
   if all(len(bb[v]&Z)<=1 for v in Z):best=max(best,len(Z))
   counts['literal_owner_subsets']+=1
  assert best==x['owner_beta']
 if n<=16:
  old=previous(prepare(b,P,Q,B,col));counts['beyond_K4_free_matching_criterion']+=not old['feasible']
 if exact:assert solve(b,P,Q,B)['beta_I']>=len(D);counts['exact_all_helper_controls']+=1
 counts['physical_certificates']+=1
 if x['exchange']:
  counts[x['exchange']['type']]+=1
 digest.update(json.dumps([P,Q,B,col,x],sort_keys=True).encode())
 return x

def aux(n,forced=None):
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
 for spec in specs:
  for trial in range(30):
   col=[v%2 for v in range(n)];L=list(range(0,n,2));RR=list(range(1,n,2));rng.shuffle(L);rng.shuffle(RR);order=[v for pair in zip(L,RR) for v in pair];B=[];offset=0
   for size,cyclic in spec:
    C=order[offset:offset+size];offset+=size
    B.extend(zip(C,C[1:]+C[:1]) if cyclic else zip(C,C[1:]))
   assert offset==n
   P,Q=aux(n);check(P,Q,list(B),col,exact=n<=8)
# Fixed critical examples exercise both parity repairs and prior-criterion failure.
for model in json.loads((ROOT/'develop/fixtures/auxiliary-square-parity.json').read_text()):
 x=check(model['P'],model['Q'],model['B'],model['colour'],exact='prior_K4_free' in model)
 if 'exchange_type' in model:assert x['exchange']['type']==model['exchange_type']
 if 'prior_K4_free' in model:
  assert previous(prepare(model['b'],model['P'],model['Q'],model['B'],model['colour']))['feasible']==model['prior_K4_free']
 fixtures.append({'name':model['name'],'certificate':x})
# A physical auxiliary eight-cycle is outside this sufficient class, regardless
# of its large owner dissociation number; failure is not a target refutation.
P=[(0,2),(1,3),(4,6),(5,7)];Q=[(2,1),(3,4),(6,5),(7,0)]
x=certificate(4,P,Q,[(v,v+1) for v in range(7)],[v%2 for v in range(8)])
assert not x['applicable'] and x['reason']=='auxiliary graph is not a union of squares'
counts['outside_auxiliary_criterion']=1
assert counts['newly_admitted_residue_0'] and counts['newly_admitted_residue_2']
assert certificate(0,[],[],[],[])['beta_I_lower']==0
assert counts['crossing owner edge'] and counts['coincident square'] and counts['beyond_K4_free_matching_criterion']
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/auxiliary-square-parity-check.json');args=parser.parse_args()
report={'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),'critical_examples':fixtures,
 'scope':'Written all-size parity theorem and normalization; physical construction under the explicit owner-size criterion. Exact smaller owner/forced optima; larger cases are actual certificates only. Prior K4-free criterion and this criterion are sufficient, not necessary. No universal8b/3, unrestricted coefficient or new grid claim.'}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='critical_examples'}))
