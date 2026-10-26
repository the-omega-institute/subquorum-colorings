"""Exact affine certificates for the written retained-P0 colour-switch proof.

No optimizer is imported here. Nonnegative polynomial identities, their local
geometric premises and all-length coordinate budgets are checked exactly.
"""
from collections import defaultdict
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json

if not __debug__:raise RuntimeError('Assertions required')
B13={(0,0),(0,2),(1,3),(2,0),(2,2),(2,4),(3,1),(3,3),(4,0),(4,2),(4,4),(5,1),(5,3)}
W13={(0,1),(0,3),(1,0),(1,2),(1,4),(2,3),(3,0),(3,2),(3,4),(4,1),(4,3),(5,0),(5,2)}
B15=B13|{(0,4),(0,6)};W15=W13|{(0,5),(0,7)}
K={(0,0),(0,2),(1,3),(2,0),(2,2),(3,1),(3,3),(4,0),(4,2),(5,1),(5,3)}
Q={(0,1),(1,0),(1,2),(2,1),(3,0),(3,2),(4,1),(5,0),(5,2)}

def neighbors(v):
 r,k=v;return {(r+dr,k+dk) for dr,dk in [(1,0),(-1,0),(0,1),(0,-1)] if 0<=r+dr<6 and k+dk>=0}
def retained(m):
 c=6*m+9
 return {(r,k) for r in (1,2) for k in {1}|{5+6*j+i for j in range(m+1) for i in range(3)}}|{(r,k) for r in (3,4) for k in range(5,c+1)}
def variable(kind,v):return kind+str(v[0])+str(v[1])
def poly(*terms):
 d=defaultdict(int)
 for coef,key in terms:d[key]+=coef
 return {k:v for k,v in d.items() if v}
def add(*ps):return poly(*[(v,k) for p in ps for k,v in p.items()])
def scale(n,p):return {k:n*v for k,v in p.items() if n*v}
def const(n):return {'1':n} if n else {}
def var(kind,v):return {variable(kind,v):1}
def delta(B,W):return add(*[var('t',v) for v in B],*[scale(-1,var('h',v)) for v in W])
DB=delta(B15,W15);DW=delta(W13,B13)

def substitute(p,fix):
 return poly(*[(coef*fix[key],'1') if key in fix else (coef,key) for key,coef in p.items()])

def black_system():
 S={};eps={v:int(bool(neighbors(v)&retained(2))) for v in B15}
 assert {v for v,x in eps.items() if x}=={(0,6),(2,0),(2,2),(2,4),(3,1),(4,4)}
 holes=W15|{(5,4)}
 for v in sorted(B15):
  S['bound_'+variable('t',v)]=add(const(1),scale(-1,var('t',v)))
  ns=sorted(neighbors(v)&holes)
  for n in range(1,len(ns)+1):
   if n+eps[v]<2:continue
   for q in combinations(ns,n):
    S['degree_'+variable('t',v)+'_'+('_'.join(variable('h',w) for w in q))]=add(*[var('h',w) for w in q],scale(-(n+eps[v]-1),var('t',v)))
 S['capacity1']=add(const(4),var('h',(0,1)),*[scale(-1,var('t',v)) for v in {(0,0),(0,2),(2,0),(2,2),(3,1)}])
 S['capacity2']=add(const(2),var('h',(5,0)),var('h',(5,2)),*[scale(-1,var('t',v)) for v in {(4,0),(4,2),(5,1),(5,3)}])
 S['capacity3']=add(const(1),var('h',(5,0)),scale(-1,var('t',(4,0))),scale(-1,var('t',(5,1))))
 S['capacity4']=add(const(3),*[var('h',v) for v in Q-{(2,1)}],*[scale(-1,var('t',v)) for v in K])
 for v in sorted(holes):S['bound_'+variable('h',v)]=add(const(1),scale(-1,var('h',v)))
 for key in sorted({key for p in S.values() for key in p if key!='1'}):S['nonnegative_'+key]={key:1}
 return S

def switch_system():
 S={};nodes={(r,k) for r in range(6) for k in range(10)};p0=retained(2);fixed={variable(kind,v):0 for v in nodes&p0 for kind in ['t','h']}
 for v in sorted(nodes):
  S['occupancy_'+str(v)]=add(const(1),scale(-1,var('t',v)),scale(-1,var('h',v)))
  for kind in ['t','h']:
   key=variable(kind,v);S['nonnegative_'+key]={key:1}
   S['bound_'+key]=add(const(1),{key:-1})
  ns=sorted(neighbors(v)&nodes)
  for n in range(2,len(ns)+1):
   for q in combinations(ns,n):S['degree_'+variable('t',v)+'_'+('_'.join(variable('h',w) for w in q))]=add(*[var('h',w) for w in q],scale(-(n-1),var('t',v)))
  for u in ns:
   if (neighbors(v)&p0)-{u}:S['forced_'+variable('t',v)+'_'+variable('h',u)]=add(var('h',u),scale(-1,var('t',v)))
 for r in range(5):
  for k in range(9):
   corners={(r,k),(r+1,k),(r,k+1),(r+1,k+1)}
   S[f'square_{r}_{k}']=add(const(2),*[scale(-1,var('t',v)) for v in corners])
 S['positive_black_deficit']=add(DB,const(-1))
 return {name:substitute(p,fixed) for name,p in S.items() if substitute(p,fixed)}

BLACK_CASES=[{'t44':1},{'t44':0,'t33':0,'h41':0},{'t44':0,'t33':0,'h41':1},{'t44':0,'t33':1,'t24':0},{'t44':0,'t33':1,'t24':1,'h41':0},{'t44':0,'t33':1,'t24':1,'h41':1}]
SWITCH_CASES=[{'t32':0,'t41':0,'h00':0},{'t32':0,'t41':0,'h00':1},{'t32':0,'t41':1,'h23':0},{'t32':0,'t41':1,'h23':1},{'t32':1,'h13':0,'h03':0},{'t32':1,'h13':0,'h03':1},{'t32':1,'h13':1}]

def check_certificates(path):
 data=json.loads(Path(path).read_text());out=[]
 for group,cases,system,objective in [('black',BLACK_CASES,black_system(),add(DB,scale(-1,var('h',(5,4))))),('switch',SWITCH_CASES,switch_system(),DW)]:
  certs=data[group];assert len(certs)==len(cases)
  for case,cert in zip(cases,certs):
   assert cert['fix']==case and 0<=cert['numerator']<cert['denominator']
   terms=[]
   for name,coef in cert['terms'].items():
    assert isinstance(coef,int) and coef>0
    terms.append(scale(coef,substitute(system[name],case)))
   lhs=add(const(cert['numerator']),scale(-cert['denominator'],substitute(objective,case)))
   assert lhs==add(*terms),(group,case,lhs,add(*terms))
   out.append({'group':group,'fix':case,'bound':[cert['numerator'],cert['denominator']],'nonnegative_terms':len(terms)})
 return out


def evaluate(p,T,H):
 return sum(coef*(1 if key=='1' else int((int(key[1]),int(key[2:])) in (T if key[0]=='t' else H))) for key,coef in p.items())

def inject(left,targets,adj):
 owner={}
 def aug(v,seen):
  for u in sorted(adj(v)&targets):
   if u in seen:continue
   seen.add(u)
   if u not in owner or aug(owner[u],seen):owner[u]=v;return True
  return False
 for v in sorted(left):assert aug(v,set()),(left,targets,v)
 return {v:u for u,v in owner.items()}

def white_pocket_injection(T,H):
 targets={}
 for v,u in [((0,1),(0,2)),((1,0),(0,0)),((1,2),(1,3))]:
  if v in T:assert u in H;targets[v]=u
 rest=T&{(3,0),(3,2),(4,1),(5,0),(5,2)}
 targets.update(inject(rest,(K|{(1,1)})&H,neighbors))
 assert len(set(targets.values()))==len(targets) and set(targets)==T&Q
 return targets

def maps(m,T,H):
 c=6*m+9;Bmap={};Wmap={}
 def put(mapping,v,u):
  assert v in T and u in H and u in neighbors(v)
  assert v not in mapping and u not in mapping.values()
  mapping[v]=u
 for j in range(m+1):
  a=4+6*j
  A,B,C,D=(0,a),(0,a+2),(0,a+4),(1,a+5)
  u,v,w,x,y,z=(0,a+1),(1,a),(0,a+3),(0,a+5),(1,a+4),(2,a+5)
  if j:
   part=inject(T&{A,B},H&{u,v,w},neighbors)
   for source,target in part.items():put(Bmap,source,target)
  part=inject(T&{C,D},H&{x,y,z},neighbors)
  for source,target in part.items():put(Bmap,source,target)
  U,W,X,Y,V,Z=(0,a+1),(0,a+3),(0,a+5),(1,a+4),(1,a+6),(2,a+5)
  E,F=(2,a+4),(2,a+6)
  if U in T:put(Wmap,U,A)
  if W in T:put(Wmap,W,B)
  if D in H:
   for source,target in [(X,D),(Y,C),(V,F),(Z,E)]:
    if source in T:put(Wmap,source,target)
  else:
   assert not T&{Y,V,Z}
   if X in T:put(Wmap,X,C)
 for k in range(5,c+1,2):
  if (5,k) in T:put(Bmap,(5,k),(5,k-1))
 for k in range(6,c,2):
  if (5,k) in T:put(Wmap,(5,k),(5,k-1))
 assert set(Bmap)=={v for v in T if sum(v)%2==0}-B15
 assert set(Wmap)=={v for v in T if sum(v)%2==1}-W13-{(5,4)}
 assert not set(Bmap.values())&W15 and not set(Wmap.values())&B13
 return Bmap,Wmap

def candidate_lists(m):
 c=6*m+9
 B={(0,k) for k in range(0,c+1,2)}|{(1,k) for k in range(3,c+1,6)}|{(2,k) for k in (0,2,4)}|{(3,k) for k in (1,3)}|{(4,k) for k in (0,2,4)}|{(5,k) for k in range(1,c+1,2)}
 W={(0,k) for k in range(1,c+1,2)}|{(1,k) for k in {0,2,4}|{a+6*j for j in range(m+1) for a in (8,10)} if k<=c}|{(2,k) for k in range(3,c+1,6)}|{(3,k) for k in (0,2,4)}|{(4,k) for k in (1,3)}|{(5,k) for k in range(0,c+1,2)}
 return B,W

def control(m,cur,counts):
 from check_residual_corridors import direct_check
 h,w,T,M=cur;assert h==6 and w==6*m+10;direct_check(*cur)
 V={(r,k) for r in range(h) for k in range(w)};P={v for e in M for v in e};H=V-T-P;P0=retained(m);assert P0<=P
 B,W=candidate_lists(m)
 possible={v for v in V-P0 if len(neighbors(v)&P0)<=1}
 assert B|W==possible and T<=possible
 sb=black_system();sw=switch_system()
 assert all(evaluate(p,T,H)>=0 for p in sb.values())
 db=evaluate(DB,T,H);dw=evaluate(DW,T,H)
 assert db<=int((5,4) in H)
 if db>=1:
  assert all(evaluate(p,T,H)>=0 for p in sw.values())
  assert dw<=0;counts['positive_prefix_deficits']+=1
 # The actual injection images are respectively genuine holes and endpoints.
 sel=white_pocket_injection(T,H);mate={v:u for e in M for v,u in (e,e[::-1])}
 actual={v:mate[v] for v in P&Q};assert set(actual.values())<=P&(K|{(1,1)})
 assert len(set(actual.values()))==len(actual) and not set(sel.values())&set(actual.values())
 assert neighbors_of(Q)==K|{(1,1)}
 bm,wm=maps(m,T,H)
 tb=sum(sum(v)%2==0 for v in T);tw=len(T)-tb
 hw=sum(sum(v)%2==1 for v in H);hb=len(H)-hw
 D=len(T)+len(M)-3*w
 assert D==tb-hw==tw-hb and D<=db and D<=dw+int((5,4) in T)
 assert D<=0
 counts['boards']+=1;counts['black_payments']+=len(bm);counts['white_payments']+=len(wm)
 counts['selected_white_pocket_injections']+=len(sel);counts['actual_mate_pocket_injections']+=len(actual)
 return db,dw,D

def neighbors_of(vs):return set().union(*(neighbors(v) for v in vs))

def new_obstruction(m):
 c=6*m+9;T={(0,0),(0,2),(0,4),(1,3),(2,0),(2,2),(2,4),(3,1),(3,3),(4,0),(4,2),(4,4),(5,0),(5,2)}
 M=[((1,1),(2,1))]+[((r,k),(r+1,k)) for k in range(5,c+1) for r in (0,2,4)]
 return 6,c+1,T,M

def random_actual(m,seed):
 import random
 from check_frozen_half_area_attainers import frozen_family
 h,w,_,M=frozen_family(m);rng=random.Random(seed);M={tuple(sorted(e)) for e in M}
 squares=[((r,k),(r+1,k),(r,k+1),(r+1,k+1)) for r in range(5) for k in range(w-1)];rng.shuffle(squares)
 for a,b,c,d in squares:
  first={tuple(sorted((a,b))),tuple(sorted((c,d)))};second={tuple(sorted((a,c))),tuple(sorted((b,d)))}
  if first<=M:M=(M-first)|second
  elif second<=M:M=(M-second)|first
 P={v for e in M for v in e};V={(r,k) for r in range(h) for k in range(w)}
 # Arbitrary new endpoints, then arbitrary colours and positions of selections.
 edges=[tuple(sorted((v,u))) for v in sorted(V) for u in sorted(neighbors(v)&V) if v<u];rng.shuffle(edges)
 for e in edges:
  if not set(e)&P and rng.randrange(3)==0:M.add(e);P.update(e)
 T=set();choices=sorted(V-P);rng.shuffle(choices)
 for v in choices:
  if rng.randrange(5)==0:continue
  trial=T|{v};O=trial|P
  if all(len(neighbors(u)&O)<=1 for u in trial):T=trial
 return h,w,T,sorted(M)

def check_hall_patterns():
 # Controls for the written five-white Hall proof; not its general premise.
 sources={(3,0),(3,2),(4,1),(5,0),(5,2)};targets=neighbors_of(sources);count=0
 from itertools import product
 for bits in product((0,1),repeat=len(targets)):
  H={v for v,b in zip(sorted(targets),bits) if b}
  allowed={v for v in sources if len(neighbors(v)&H)>=len(neighbors(v))-1}
  for n in range(len(allowed)+1):
   for ss in combinations(sorted(allowed),n):inject(set(ss),H,neighbors);count+=1
 return count

def main():
 import argparse
 from collections import Counter
 from check_frozen_half_area_attainers import frozen_family
 from check_unprotected_white_pair import white_replacement,frozen_terminal_black,prefix_obstruction
 from check_promotion_cores import frozen_certificate
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();root=Path(__file__).resolve().parents[1]
 certs=check_certificates(root/'output/colour-switch-affine-certificates.json');counts=Counter();lengths=list(range(2,41))+[64,100];records=[]
 for m in lengths:
  for cur in [frozen_family(m),white_replacement(m),frozen_terminal_black(m)[0]]:
   control(m,cur,counts);assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e};counts['frozen_controls']+=1
  for cur in [new_obstruction(m),prefix_obstruction(m)]:
   db,dw,D=control(m,cur,counts);assert db==1 and dw==D==0
   expected={(2,1)} if cur[2]==new_obstruction(m)[2] else set()
   assert frozen_certificate(cur)[0]==expected;counts['all_length_prefix_obstructions']+=1
  cur=new_obstruction(m);records.append({'m':m,'J':len(cur[2])+len(cur[3]),'black_prefix_selected':12,'white_prefix_holes':11,'delta_black':1,'delta_white':0,'boundary_hole':[5,4]})
 for m in [2,3,8,20]:
  for seed in range(64):control(m,random_actual(m,seed),counts)
 counts['five_white_hall_patterns']=check_hall_patterns()
 out={'status':'PASS','theorem':'For every m>=2, retain P0, arbitrary feasible T and arbitrary actual matching: exact max J=18m+30=area/2. No freezing needed; inherited frozen equality family attains.',
      'proof':'Written actual-mate capacities, five-white Hall injection, thirteen exact nonnegative affine identities, disjoint colourwise maps and integer colour switch. Enumeration checks the proof only.',
      'counts':dict(counts),'affine_certificates':certs,'obstruction_controls':records,'scope':'Full grid adapter and actual-mate/Hall geometry are written with solver-free checks. Lean audits local algebra and global switching arithmetic separately. Universal 5/6 remains open.'}
 args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['obstruction_controls','affine_certificates']},indent=2))

if __name__=='__main__':main()
