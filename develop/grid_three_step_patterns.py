"""Complete finite type classification for a 3-edge LL path with r=1 internal tiles."""
from itertools import product
import json, collections
CORNERS=((0,0),(0,1),(1,0),(1,1))

def point(tile,corner):return (2*tile[0]+corner[0],2*tile[1]+corner[1])
def tile_of(p):return (p[0]//2,p[1]//2)
def corner_of(p):return (p[0]%2,p[1]%2)
def add(p,q):return (p[0]+q[0],p[1]+q[1])
def external_toward_blank(s,b):
 if s[0]==b[0]:return (-1 if s[0]==0 else 1,0)
 assert s[1]==b[1]
 return (0,-1 if s[1]==0 else 1)

class Conflict(Exception):pass
class Patch:
 def __init__(self):self.states={};self.mate={};self.roles={}
 def cell(self,p,s):
  if p in self.states and self.states[p]!=s:raise Conflict('state')
  self.states[p]=s
 def shape(self,t,letters,role):
  if t in self.roles and self.roles[t]!=role:raise Conflict('tile_role')
  self.roles[t]=role
  for c,s in letters.items():self.cell(point(t,c),s)
 def edge(self,u,v):
  assert abs(u[0]-v[0])+abs(u[1]-v[1])==1
  self.cell(u,'P');self.cell(v,'P')
  if u in self.mate and self.mate[u]!=v:raise Conflict('matching')
  if v in self.mate and self.mate[v]!=u:raise Conflict('matching')
  self.mate[u]=v;self.mate[v]=u
 def attachment(self,t,s,b):
  u=point(t,s);v=add(u,external_toward_blank(s,b));nt=tile_of(v);nc=corner_of(v)
  shape={c: ('P' if c==nc else 'B' if (c[0]!=nc[0] and c[1]!=nc[1]) else 'T') for c in CORNERS}
  self.shape(nt,shape,'sat');self.edge(u,v)
 def central(self,t,ports,kind):
  rest=[c for c in CORNERS if c not in ports]
  letters={c:'P' for c in ports}
  if kind=='H':
   letters.update({c:'P' for c in rest});self.shape(t,letters,'r1');self.edge(point(t,rest[0]),point(t,rest[1]));return
  st,j=kind[0],int(kind[1]);active=rest[j];blank=rest[1-j]
  letters[active]='T' if st=='T' else 'P';letters[blank]='B';self.shape(t,letters,'r1')
  if st=='S':self.attachment(t,active,blank)
 def leaf(self,u,d,kind):
  v=add(u,d);t=tile_of(v);c=corner_of(v);opp=(1-c[0],1-c[1]);adj=[x for x in CORNERS if x not in (c,opp)]
  letters={c:'P',opp:'B'}
  if kind==2:
   letters.update({x:'P' for x in adj});ss=adj
  else:
   letters[adj[kind]]='T';letters[adj[1-kind]]='P';ss=[adj[1-kind]]
  self.shape(t,letters,'leaf');self.edge(u,v)
  for s in ss:self.attachment(t,s,opp)
 def finish(self):
  for p,s in self.states.items():
   if s=='P' and p not in self.mate:raise Conflict('unmatched')
   if s=='T':
    degree=sum(self.states.get(add(p,d),'B')!='B' for d in ((1,0),(-1,0),(0,1),(0,-1)))
    if degree>1:raise Conflict('T_degree')
  # All unspecified cells can be B: these are actual finite witnesses.
  return True

def classification():
 Q=(0,0);R=(0,1);qout=(0,1);rin=(0,0)
 qtypes=[('left',(0,0),(0,-1)),('up',(0,0),(-1,0)),('down',(1,1),(1,0))]
 rtypes=[('right',(0,1),(0,1)),('up',(0,1),(-1,0)),('down',(1,0),(1,0))]
 kinds=['T0','T1','S0','S1','H'];counts=[];examples=[];all_examples=[];total=0;reasons=collections.Counter()
 for (qa,qc,qd),(ra,rc,rd) in product(qtypes,rtypes):
  tally=[0,0,0];witness=None
  for a,b,l,r in product(kinds,kinds,range(3),range(3)):
   total+=1;p=Patch()
   try:
    p.central(Q,(qout,qc),a);p.central(R,(rin,rc),b)
    p.edge(point(Q,qout),point(R,rin))
    p.leaf(point(Q,qc),qd,l);p.leaf(point(R,rc),rd,r);p.finish()
   except Conflict as e:reasons[str(e)]+=1;continue
   h=(a=='H')+(b=='H');tally[h]+=1
   if not h:raise AssertionError(('counterexample',qa,ra,a,b,l,r))
   record=dict(case=[qa,ra],types=[a,b,l,r],states=[(list(v),s) for v,s in sorted(p.states.items())],edges=[(list(v),list(w)) for v,w in p.mate.items() if v<w])
   all_examples.append(record)
   if witness is None:witness=record
  counts.append(dict(left_leaf_exit=qa,right_leaf_exit=ra,feasible_by_internal_edges=tally))
  if witness:examples.append(witness)
 return dict(total=total,table=counts,rejections=dict(reasons),examples=examples,all_examples=all_examples)
