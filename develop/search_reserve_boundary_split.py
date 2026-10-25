"""Optional Z3 discovery; no finite UNSAT result is a general theorem.

Saved fixture has independent solver-free and Lean freezing verification.
"""
import sys,itertools,json,time,argparse
sys.path.insert(0,'develop')
import z3
from check_merger_matching_rigidity import *
from check_whole_support_fork_normal_form import whole_support_data
from check_whole_support_fork_flow import fork_flow
from check_compensation_flow_normal_form import owner_data
from check_residual_corridors import direct_check
ap=argparse.ArgumentParser();ap.add_argument('mode',choices=['split','split_alpha','terminals']);ap.add_argument('--seconds',type=int,default=35);ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
_,cur=load();rows,cols,T0,M0=cur;P0={v for e in M0 for v in e};points=list(itertools.product(range(rows),range(cols)));universe=set(points)
N={v:sorted(set(neighbors(v))&universe) for v in points};E=sorted({tuple(sorted((v,w))) for v in points for w in N[v]});inc={v:[e for e in E if v in e] for v in points}
t={v:z3.Bool('t_%d_%d'%v) for v in points};p={v:z3.Bool('p_%d_%d'%v) for v in points};m={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in E};rank={v:z3.Int('r_%d_%d'%v) for v in points}
owner={v:z3.Int('o_%d_%d'%v) for v in points};dist={v:z3.Int('d_%d_%d'%v) for v in points}
ct=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs]);solver=z3.Solver();solver.set(timeout=1000*args.seconds)
roots={(5,12):1,((3,15) if args.mode=='terminals' else (4,15)):2}
for v in points:
 solver.add(z3.Not(z3.And(t[v],p[v])),ct(m[e] for e in inc[v])==z3.If(p[v],1,0),rank[v]>=0,rank[v]<len(points))
 solver.add(z3.Implies(t[v],ct(z3.Or(t[w],p[w]) for w in N[v])<=1))
 retained=[z3.Or(t[w],z3.Or([z3.And(m[e],rank[next(x for x in e if x!=w)]<rank[v]) for e in inc[w]])) for w in N[v]]
 solver.add(z3.Implies(p[v],ct(retained)>=2))
 if v in T0:solver.add(t[v])
 if v in P0:solver.add(p[v])
 if v[1]==0:solver.add(z3.Not(t[v]),z3.Not(p[v]))
 partner=(v[0]^1,v[1]);solver.add(owner[v]>=0,owner[v]<=2,dist[v]>=0,dist[v]<len(points))
 solver.add(z3.Implies(z3.And(p[v],p[partner]),owner[v]==owner[partner]))
 if v in roots:solver.add(owner[v]==roots[v],dist[v]==0)
 else:
  descent=[z3.And(z3.Or(m[tuple(sorted((v,w)))],z3.And(w==partner,p[v],p[w])),owner[v]==owner[w],dist[w]<dist[v]) for w in N[v]]
  solver.add(z3.Implies(z3.And(p[v],owner[v]>0),z3.Or(descent)))
for e in E:solver.add(z3.Implies(m[e],owner[e[0]]==owner[e[1]]))
for r in range(0,rows,2):solver.add(z3.Or(z3.And(z3.Not(t[r,cols-1]),z3.Not(p[r,cols-1])),z3.And(z3.Not(t[r+1,cols-1]),z3.Not(p[r+1,cols-1]))))
if args.mode=='split_alpha':
 for label in (1,2):
  solver.add(ct(z3.And(p[v],owner[v]==label,t[v[0]^1,v[1]]) for v in points)==2)
  solver.add(ct(z3.And(p[v],owner[v]==label,z3.Not(p[v[0]^1,v[1]]),z3.Not(t[v[0]^1,v[1]])) for v in points)==0)
for budget in (4,8,12,20,40,190):
 solver.push();solver.add(ct(p[v] for v in points if v not in P0)<=budget)
 start=time.monotonic();ans=solver.check();print(args.mode,budget,str(ans),'seconds',time.monotonic()-start,flush=True)
 if ans==z3.sat:
  model=solver.model();T={v for v in points if z3.is_true(model.eval(t[v]))};M=[e for e in E if z3.is_true(model.eval(m[e]))];ext=rows,cols,T,M
  direct_check(*ext);assert frozen(ext);Q={v for e in M for v in e};d,meta,_=whole_support_data(ext,whole_bands(ext));o,aa,bb,mm=owner_data(*d[:2]);flow=fork_flow(*d)
  record=dict(shape=(rows,cols),selected=sorted(T),matching=M,newT=sorted(T-T0),newP=sorted(Q-P0),removed=sorted(canonical(M0)-canonical(M)),added=sorted(canonical(M)-canonical(M0)),k=len(aa),b=len(bb),I=len(d[4]),value=flow['value'],cost=flow['cost'],mode=args.mode,budget=budget)
  args.output.write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k not in ('selected','matching')}),flush=True);break
 solver.pop()
