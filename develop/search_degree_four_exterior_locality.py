"""Optional Z3 discovery only. Final all-h validator needs only standard Python.

Saved discovery used z3-solver 5.3.2.0. A bounded UNSAT result is not a
general theorem; --negative additionally asks for a negative strip and
no nearby outside donor for any actual D4 export.
"""
import sys,itertools,json,time,argparse
from pathlib import Path
import z3
sys.path.insert(0,str(Path.cwd()/'develop'))
from check_residual_corridors import direct_check
from check_promotion_cores import frozen_certificate
from check_cooperative_promotion import neighbors

def cnt(xs):return z3.Sum([z3.If(x,1,0) for x in xs])
def run(h,w,R,timeout,negative=False):
 V=list(itertools.product(range(h),range(w)));Vs=set(V);adj={v:sorted(set(neighbors(v))&Vs) for v in V};E=sorted({tuple(sorted((v,u))) for v in V for u in adj[v]})
 T={v:z3.Bool('t%d_%d'%v) for v in V};P={v:z3.Bool('p%d_%d'%v) for v in V};rank={v:z3.Int('r%d_%d'%v) for v in V};M={e:z3.Bool('m%d_%d_%d_%d'%(*e[0],*e[1])) for e in E};inc={v:[(u,M[tuple(sorted((u,v)))]) for u in adj[v]] for v in V}
 s=z3.Solver();s.set(timeout=timeout*1000)
 for v in V:
  s.add(z3.Not(z3.And(T[v],P[v])),cnt(e for u,e in inc[v])==z3.If(P[v],1,0),rank[v]>=0,rank[v]<len(V))
  s.add(z3.Implies(T[v],cnt(z3.Or(T[u],P[u]) for u in adj[v])<=1))
  retained=[z3.Or(T[u],z3.Or([z3.And(e,rank[x]<rank[v]) for x,e in inc[u]])) for u in adj[v]]
  s.add(z3.Implies(P[v],cnt(retained)>=2))
 r=3;c=w//2-1;v=(r,c);q=(r//2,c//2);U={(a,b) for a in (2,3) for b in range(w)}
 s.add(T[r-1,c],P[v],P[r,c-1],P[r,c+1],M[tuple(sorted((v,(r+1,c))))])
 for a in (2,3):s.add(z3.Not(T[a,0]),z3.Not(P[a,0]))
 s.add(z3.Or([z3.And(z3.Not(T[a,w-1]),z3.Not(P[a,w-1])) for a in (2,3)]))
 for a,b in itertools.product(range(h//2),range(w//2)):
  tile={(2*a+i,2*b+j) for i,j in itertools.product(range(2),repeat=2)}
  if tile<=U or max(abs(a-q[0]),abs(b-q[1]))>R:continue
  s.add(2*cnt(T[x] for x in tile)+cnt(P[x] for x in tile)>=4)
 if negative:
  s.add(2*cnt(T[x] for x in U)+cnt(P[x] for x in U)>len(U))
  for a,b in U:
   if b==0 or b==w-1:continue
   d4=z3.And(T[5-a,b],P[a,b],z3.Or([edge for u,edge in inc[a,b] if u not in U]),z3.Or(T[a,b-1],P[a,b-1]),z3.Or(T[a,b+1],P[a,b+1]))
   for i,j in itertools.product(range(h//2),range(w//2)):
    if i==1 or max(abs(i-a//2),abs(j-b//2))>R:continue
    tile={(2*i+x,2*j+y) for x,y in itertools.product(range(2),repeat=2)}
    s.add(z3.Implies(d4,2*cnt(T[x] for x in tile)+cnt(P[x] for x in tile)>=4))
 t=time.monotonic();status=s.check();out=dict(status=str(status),shape=[h,w],radius=R,source=v,seconds=time.monotonic()-t)
 if status==z3.sat:
  m=s.model();cur=(h,w,{x for x in V if z3.is_true(m.eval(T[x]))},[e for e in E if z3.is_true(m.eval(M[e]))]);direct_check(*cur);F,layers=frozen_certificate(cur);assert F=={x for e in cur[3] for x in e}
  out.update(selected=sorted(cur[2]),matching=cur[3],freezing_layers=layers,region=[((2,j),(3,j)) for j in range(w)])
 return out
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--shape',nargs=2,type=int,default=[10,12]);a.add_argument('--radius',type=int,default=2);a.add_argument('--timeout',type=int,default=30);a.add_argument('--output',type=Path,required=True);a.add_argument('--negative',action='store_true');p=a.parse_args();out=run(*p.shape,p.radius,p.timeout,p.negative);p.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ('selected','matching','freezing_layers','region')},indent=2))
