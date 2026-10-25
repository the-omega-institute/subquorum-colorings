"""Optional Z3 discovery; mandatory saved-model checks need no solver.
Run from the repository root with z3-solver installed.
"""
import argparse
import sys,json,time
ap=argparse.ArgumentParser();ap.add_argument('--output',required=True);ap.add_argument('--timeout-ms',type=int,default=15000);args=ap.parse_args()
sys.path.insert(0,'develop')
import z3
from check_conditional_fresh_tip_closure import *
b,*_=load_model();initial=base_copies(b,2);O0=initial[2]|endpoints(initial)
board={(r,c) for r in range(28) for c in range(1,48)}
# Retained selected saturation forces these old blanks to remain blank.
F={v for v in board-O0 if set(neighbors(v))&initial[2]}
allowed=board-initial[2]-F
es=sorted({tuple(sorted((v,w))) for v in allowed for w in set(neighbors(v))&allowed})
m={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in es};inc={v:[] for v in allowed}
for e in es:
 for v in e:inc[v].append(m[e])
p={v:z3.Or(inc[v]) for v in allowed};t={v:z3.Bool('t_%d_%d'%v) for v in allowed-endpoints(initial)}
for v in initial[2]:t[v]=z3.BoolVal(True)
def pp(v):return p.get(v,z3.BoolVal(False))
def tt(v):return t.get(v,z3.BoolVal(False))
def occ(v):return z3.Or(pp(v),tt(v))
s=z3.Solver();s.set(timeout=args.timeout_ms)
for v in allowed:
 if inc[v]:s.add(z3.AtMost(*inc[v],1))
 s.add(z3.Not(z3.And(pp(v),tt(v))))
 s.add(z3.Implies(pp(v),z3.PbGe([(occ(w),1) for w in neighbors(v) if w in board],3)))
for v in t:
 ns=[occ(w) for w in neighbors(v) if w in board]
 s.add(z3.Implies(tt(v),z3.AtMost(*ns,1)))
for v in endpoints(initial):s.add(pp(v))
for r in range(0,28,2):s.add(z3.Not(z3.And(occ((r,47)),occ((r+1,47)))))
cases=[]
for v in [(9,23),(10,23),(11,23),(12,23),(13,23),(14,23),(21,23),(22,23),(9,24),(10,24),(11,24),(12,24),(26,23),(26,24)]:
 cases.append(('tip_'+str(v),[pp(v),tt(partner(v))]))
cases += [('noBB_seam',[pp((9,23)),tt((8,23)),tt((9,22)),pp((9,24))]),
 ('bottom_BP',[pp((26,14)),tt((27,14)),pp((26,13))]),
 ('bottom_BB13',[pp((26,14)),tt((27,14)),z3.Not(occ((26,13)))]),
 ('bottom_BT_BB12',[pp((26,14)),tt((27,14)),tt((26,13)),z3.Not(occ((27,12)))]),
 ('bottom_BT_BT_BB11',[pp((26,14)),tt((27,14)),tt((26,13)),tt((27,12))])]
cases += [
 ('mixed_bottom_colors',[pp((26,14)),tt((27,14)),pp((26,37)),tt((27,37)),m[tuple(sorted(((26,37),(25,37))))]]),
 ('two_odd_bottoms',[pp((26,13)),tt((27,13)),pp((26,15)),tt((27,15)),m[tuple(sorted(((26,13),(25,13))))]]),
 ('odd_and_seam',[pp((26,13)),tt((27,13)),pp((9,23)),tt((8,23)),m[tuple(sorted(((26,13),(25,13))))]]),
 ('double_BT_and_odd',[pp((26,14)),tt((27,14)),tt((26,13)),tt((27,12)),pp((26,39)),tt((27,39)),m[tuple(sorted(((26,39),(25,39))))]]),
 ('opposite_copies_odd',[pp((26,13)),tt((27,13)),pp((26,39)),tt((27,39)),m[tuple(sorted(((26,13),(25,13))))],m[tuple(sorted(((26,39),(25,39))))]]),
]

out=[]
for name,conditions in cases:
 s.push();s.add(*conditions);start=time.monotonic();result=s.check();print(name,result,round(time.monotonic()-start,2),flush=True)
 if result==z3.sat:
  mod=s.model();T={v for v in t if z3.is_true(mod.eval(tt(v)))};M=[e for e in es if z3.is_true(mod.eval(m[e]))]
  cur=(*initial[:2],T,M);assert feasible(cur) and endpoints(initial)<=endpoints(cur)
  assert all(len(set(neighbors(v))&(T|endpoints(cur)))>=3 for v in endpoints(cur))
  out.append(dict(name=name,shape=list(cur[:2]),selected=sorted(T),matching=M))
 s.pop()
open(args.output,'w').write(json.dumps(out,indent=2)+'\n');print('saved',len(out),flush=True)
