"""Optional Z3 discovery for the sharp nonfrozen restricted-pool witness.
Run from repository root with z3-solver installed. The theorem and the saved
fixture are verified without Z3 by check_residual_fresh_domains.py.
"""
import argparse
import sys,json,time
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--timeout-ms',type=int,default=30000);args=ap.parse_args()
sys.path.insert(0,'develop')
import z3
from check_conditional_fresh_tip_closure import load_model,PROTECTED,partner
from check_endpoint_extension_replacement import static_certificate,FLEX
from check_cooperative_promotion import neighbors
b,*_=load_model();P0={v for e in b[3] for v in e};T=b[2]|{(16,9),(27,13)}
D=(17,9);V=(26,13);newanchors={D,V}
points={(r,c) for r in range(28) for c in range(1,23)}
allowed=P0|{v for v in points-T if not(set(neighbors(v))&b[2]) and not((set(neighbors(v))&{(16,9),(27,13)}) and v not in newanchors)}
assert P0<=allowed
es=sorted({tuple(sorted((v,w))) for v in allowed for w in set(neighbors(v))&allowed})
inc={v:[] for v in allowed};m={}
for e in es:
 m[e]=z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1]))
 for v in e:inc[v].append(m[e])
p={v:z3.Or(inc[v]) for v in allowed};mark={v:z3.Bool('a_%d_%d'%v) for v in allowed}
s=z3.Solver();s.set(timeout=args.timeout_ms)
for v in allowed:
 if inc[v]:s.add(z3.AtMost(*inc[v],1))
old,_=static_certificate(b);C=[(v,t[1]) for t,v in old.items()]+list(FLEX)
required=P0|{D,V}|{w for v,w in FLEX}
for v in required:s.add(p[v])
for e in es:s.add(z3.Implies(m[e],mark[e[0]]==mark[e[1]]))
for v in allowed:
 q=partner(v)
 if q in allowed:s.add(z3.Implies(z3.And(p[v],p[q]),mark[v]==mark[q]))
linked={v for e in C for v in e}
for a,c in C:s.add(mark[a]==mark[c])
for v in allowed-linked-{D,V}:
 q=partner(v)
 s.add(z3.Implies(z3.And(p[v],z3.Not(p[q]) if q in allowed else z3.BoolVal(True)),z3.Not(mark[v])))
s.add(mark[D],mark[V])
print('size',len(allowed),len(es),flush=True)
t=time.monotonic();r=s.check();print(r,time.monotonic()-t,flush=True)
if r==z3.sat:
 model=s.model();edges=[e for e in es if z3.is_true(model.eval(m[e]))]
 out=dict(shape=[28,24],selected=sorted(T),matching=edges,new_P=len({v for e in edges for v in e}-P0),search='SAT discovery only; verify all mathematical claims independently.')
 open(args.output,'w').write(json.dumps(out,indent=2)+'\n');print('newP',out['new_P'],flush=True)
