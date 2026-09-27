#!/usr/bin/env python3
"""Exact finite regression checks, not a substitute for the written proofs."""
from __future__ import annotations
import argparse, hashlib, itertools, json, random
from pathlib import Path

def F(m,n):
 return max(((m+1)//2)*((2*n+2)//3)+(m//2)*(n//3),((n+1)//2)*((2*m+2)//3)+(n//2)*(m//3))
def bits(x):
 while x:
  b=x&-x;yield b.bit_length()-1;x^=b

def graph(m,n):
 adj=[0]*(m*n);edges=[]
 for v in range(m*n):
  i,j=divmod(v,n)
  for u in (v+1 if j+1<n else -1,v+n if i+1<m else -1):
   if u>=0:adj[v]|=1<<u;adj[u]|=1<<v;edges.append((v,u))
 return adj,edges

def feasible(adj,T,A):return all((adj[v]&A).bit_count()<=1 for v in bits(T))

def pairs(m,n):
 adj,_=graph(m,n)
 def rec(left,T,A,M):
  if not left:yield T,A,M;return
  b=left&-left;v=b.bit_length()-1;rest=left^b
  yield from rec(rest,T,A,M)
  if feasible(adj,T|b,A|b):yield from rec(rest,T|b,A|b,M)
  for u in bits(adj[v]&rest):
   ub=1<<u;nxt=A|b|ub
   if feasible(adj,T,nxt):yield from rec(rest^ub,T,nxt,M+((v,u),))
 yield from rec((1<<(m*n))-1,0,0,())

def core(m,n,T,M):
 Q=m*n//4;tile=lambda v:(v//n//2)*(n//2)+(v%n//2)
 t=[0]*Q;h=[0]*Q;s=[0]*Q;ce=[]
 for v in bits(T):t[tile(v)]+=1
 assert max(t)<=2
 for v,w in M:
  a,b=tile(v),tile(w)
  if a==b:h[a]+=1
  elif t[a]==t[b]==2:raise AssertionError('saturated-to-saturated edge')
  elif t[a]==2:s[b]+=1
  elif t[b]==2:s[a]+=1
  else:ce.append((a,b))
 residual=[2-t[i]-h[i]-s[i] for i in range(Q)];assert min(residual)>=0
 deg=[0]*Q
 for a,b in ce:
  deg[a]+=1;deg[b]+=1
  assert residual[a]+residual[b]>0,('adjacent residual-zero tiles',m,n,T,M)
 for r,d in zip(residual,deg):assert d <= (1 if r==0 else 2*r)
 bound=m*n//2;D=bound-T.bit_count();excess=T.bit_count()+len(M)-bound
 assert excess==len(ce)-sum(residual)
 assert 3*len(M)<=4*D,('three-quarter bound',m,n,T,M)
 if D<=2:assert len(M)<=D

def check_pair(m,n,T,A,M):
 P=A^T;mate={v:w for e in M for v,w in (e,e[::-1])};assert len(mate)==2*len(M)
 c=[0]*m
 for v in bits(T):c[v//n]+=1
 horizontal=True
 for v,w in M:
  if v//n==w//n:c[v//n]+=1
  else:horizontal=False
 if horizontal:
  cap=(2*n+2)//3;high=(n+1)//2
  assert max(c)<=cap
  assert all(a+b<=n or (n%2 and a==b==high) for a,b in zip(c,c[1:]))
  if n%2:assert all(c[i:i+3]!=[high]*3 for i in range(m-2))
  assert sum(c)<=F(m,n)
 for row in range(m-1):
  band=((1<<(2*n))-1)<<(row*n);tp=[];pb=[];tt=[];bb=[]
  for j in range(n):
   vs=(row*n+j,(row+1)*n+j)
   st=tuple('T' if T>>v&1 else 'P' if P>>v&1 else 'B' for v in vs)
   if st==('T','T'):tt.append(j)
   if st==('B','B'):bb.append(j)
   if set(st)=={'T','P'}:tp.append(next(v for v in vs if P>>v&1))
   if set(st)=={'P','B'}:pb.append(next(v for v in vs if P>>v&1))
  internal=[v for v in tp if band>>mate[v]&1]
  assert len({mate[v] for v in internal})==len(internal)
  assert all(mate[v] in pb for v in internal)
  ext=sum(1 for v in bits(P&band) if not(band>>mate[v]&1))
  u=len(tp)-len(internal);v=len(pb)-len(internal);R=ext-u;delta=len(bb)-len(tt)
  J=(T&band).bit_count()+sum(bool(band>>a&1) and bool(band>>b&1) for a,b in M)
  assert R>=0 and v>=0 and (R+v)%2==0
  assert n-J==delta+(R+v)//2
  if delta<0:
   assert n%2 and tt==list(range(0,n,2)) and bb==list(range(1,n,2))
   assert P&band==0 and ext==0
  if m==2:
   assert J<=n+n%2
   if n%2 and J==n+1:
    assert not M and T==sum(1<<(i*n+j) for i in range(2) for j in range(0,n,2))
 if m%2==n%2==0:core(m,n,T,M)

def orient_linear(c,k,n):
 if n<2 or n%2 or len(k)!=len(c)-1 or not c or min(c+k)<0:raise ValueError('invalid data')
 m=len(c);cap=(2*n+2)//3;S=[0];X=[0];origin=[0]
 for i in range(1,m+1):
  S.append(S[-1]+c[i-1]+(k[i-2] if i>=2 else 0))
  upper=S[i]+(k[i-1] if i<m else 0)
  opts=[(upper,i),(X[i-1]+cap,origin[i-1])]
  if i>=2:opts.append((X[i-2]+n,origin[i-2]))
  value,start=min(opts);X.append(value);origin.append(start)
  if value<S[i]:return None,(start,i-1)
 return [X[i]-X[i-1] for i in range(1,m+1)],None

def orient_independent(c,k,n):
 cap=(2*n+2)//3;states={(0,-1)}
 for i in range(len(c)):
  nxt=set();prev=k[i-1] if i else 0;after=k[i] if i<len(k) else 0
  for old,zold in states:
   for new in range(after+1):
    z=c[i]+prev-old+new
    if z<=cap and (i==0 or zold+z<=n):nxt.add((new,z))
  states=nxt
 return bool(states)

def W(c,k,a,b):return sum(c[a:b+1])+sum(k[a:b])
def L(h,n):return (h//2)*n+(h%2)*((2*n+2)//3)

def abstract_checks():
 count=0
 for n,maxm in [(2,5),(4,4),(6,3)]:
  for m in range(1,maxm+1):
   for data in itertools.product(range(n+1),repeat=2*m-1):
    c=list(data[:m]);k=list(data[m:]);z,wit=orient_linear(c,k,n)
    good=all(W(c,k,a,b)<=L(b-a+1,n) for a in range(m) for b in range(a,m))
    assert (z is not None)==good==orient_independent(c,k,n)
    if wit is not None:
     a,b=wit;assert W(c,k,a,b)>L(b-a+1,n)
    else:assert sum(z)==sum(c)+sum(k)
    count+=1
 return count

def random_checks(count):
 rng=random.Random(20260927);total=0;sizes=[(6,6),(8,10),(12,14),(20,20),(2,30),(30,2)]
 for m,n in sizes:
  adj,edges=graph(m,n)
  for _ in range(count):
   rng.shuffle(edges);A=T=0;M=[];probability=rng.random()*.7
   for v,w in edges:
    mask=(1<<v)|(1<<w)
    if not A&mask and rng.random()<probability:A|=mask;M.append((v,w))
   order=list(range(m*n));rng.shuffle(order)
   for v in order:
    b=1<<v
    if not A&b and feasible(adj,T|b,A|b):T|=b;A|=b
   check_pair(m,n,T,A,tuple(M));total+=1
 return {'seed':20260927,'sizes':sizes,'pairs':total}

def main():
 p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('grid-directional-core-verification.json'));p.add_argument('--random-per-size',type=int,default=200);a=p.parse_args()
 report={'scope':'Exact finite regression checks. Universal claims rest on written proofs; no Lean claim.','exhaustive':[]}
 for m,n in [(2,1),(2,2),(2,3),(2,4),(2,5),(2,6),(3,3),(3,4),(4,3),(4,4)]:
  count=0
  for T,A,M in pairs(m,n):check_pair(m,n,T,A,M);count+=1
  row={'m':m,'n':n,'pairs':count};report['exhaustive'].append(row);print(json.dumps(row),flush=True)
 report['abstract_even_profiles']=abstract_checks();print('ABSTRACT_PROFILES_PASSED',flush=True)
 report['random']=random_checks(a.random_per_size)
 report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();report['result']='ALL_LISTED_CHECKS_PASSED'
 a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report),flush=True)
if __name__=='__main__':main()
