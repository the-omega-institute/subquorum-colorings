"""Optional Z3 discovery only; no UNSAT/timeout gives a general theorem.

The reduced saved fixture and independent solver-free verification are in
check_frozen_ear_rematching.py. Example: STATE empty --output /tmp/ear.json.
"""
import sys,itertools,json,time,argparse
sys.path.insert(0,'develop')
import z3
from check_merger_matching_rigidity import *
from check_whole_support_fork_normal_form import whole_support_data
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow
from check_residual_corridors import direct_check
ap=argparse.ArgumentParser();ap.add_argument('state',choices=['empty','selection','cycle','cycle_beta']);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--seconds',type=int,default=45);args=ap.parse_args()
_,base=load();state=next(s for s in STATES if s[0]==args.state);cur=complete(base,state)
rows,cols,T0,M0=cur;P0={v for e in M0 for v in e};points=list(itertools.product(range(rows),range(cols)));universe=set(points)
N={v:sorted(set(neighbors(v))&universe) for v in points};E=sorted({tuple(sorted((v,w))) for v in points for w in N[v]});inc={v:[e for e in E if v in e] for v in points}
t={v:z3.Bool('t_%d_%d'%v) for v in points};p={v:z3.Bool('p_%d_%d'%v) for v in points};m={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in E};rank={v:z3.Int('r_%d_%d'%v) for v in points}
ct=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs]);solver=z3.Solver();solver.set(timeout=1000*args.seconds)
for v in points:
 solver.add(z3.Not(z3.And(t[v],p[v])),ct(m[e] for e in inc[v])==z3.If(p[v],1,0),rank[v]>=0,rank[v]<len(points))
 solver.add(z3.Implies(t[v],ct(z3.Or(t[w],p[w]) for w in N[v])<=1))
 retained=[z3.Or(t[w],z3.Or([z3.And(m[e],rank[next(x for x in e if x!=w)]<rank[v]) for e in inc[w]])) for w in N[v]]
 solver.add(z3.Implies(p[v],ct(retained)>=2))
 if v in T0:solver.add(t[v])
 if v in P0:solver.add(p[v])
 if v[1]==0:solver.add(z3.Not(t[v]),z3.Not(p[v]))
for r in range(0,rows,2):solver.add(z3.Or(z3.And(z3.Not(t[r,cols-1]),z3.Not(p[r,cols-1])),z3.And(z3.Not(t[r+1,cols-1]),z3.Not(p[r+1,cols-1]))))
solver.add(z3.Or([z3.Not(m[e]) for e in canonical(M0)]))
for budget in (2,4,6,8,12,20):
 solver.push();solver.add(ct(p[v] for v in points if v not in P0)<=budget)
 start=time.monotonic();ans=solver.check();print(state[0],budget,str(ans),'seconds',time.monotonic()-start,flush=True)
 if ans==z3.sat:
  model=solver.model();T={v for v in points if z3.is_true(model.eval(t[v]))};M=[e for e in E if z3.is_true(model.eval(m[e]))];ext=rows,cols,T,M
  direct_check(*ext);assert frozen(ext);Q={v for e in M for v in e};d,meta,_=whole_support_data(ext,whole_bands(ext));o,aa,bb,mm=owner_data(*d[:2]);flow=fork_flow(*d)
  record=dict(shape=(rows,cols),selected=sorted(T),matching=M,newT=sorted(T-T0),newP=sorted(Q-P0),removed=sorted(canonical(M0)-canonical(M)),added=sorted(canonical(M)-canonical(M0)),k=len(aa),b=len(bb),I=len(d[4]),value=flow['value'],cost=flow['cost'],state=state[0],budget=budget)
  args.output.write_text(json.dumps(record,indent=2));print(json.dumps({k:v for k,v in record.items() if k not in ('selected','matching')}),flush=True);break
 solver.pop()
