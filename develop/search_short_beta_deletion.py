"""Optional discovery of frozen short-beta deletion failures.

An exposed outer alpha-tip neighbor is forced blank. Removing the short
beta then leaves this alpha endpoint only its actual mate and its selected
band partner. SAT discovers the original board; a solver-free checker must
verify all permanent conclusions. Timeout/UNSAT is not a general theorem.
"""
import argparse
import itertools
import json
from pathlib import Path
import time
import z3

from check_cooperative_promotion import neighbors
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rows',type=int,default=16)
    parser.add_argument('--columns',type=int,default=14)
    parser.add_argument('--seconds',type=int,default=45)
    parser.add_argument('--unsupported-core',action='store_true',
                        help='Seek an arbitrary nonfreezing core, with empty alpha whole support.')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    rows,cols=args.rows,args.columns
    r,s=8,5
    points=list(itertools.product(range(rows),range(cols)));universe=set(points)
    adjacent={v:sorted(set(neighbors(v))&universe) for v in points}
    edges=sorted({tuple(sorted((v,w))) for v in points for w in adjacent[v]})
    incident={v:[e for e in edges if v in e] for v in points}
    t={v:z3.Bool('t_%d_%d'%v) for v in points}
    p={v:z3.Bool('p_%d_%d'%v) for v in points}
    m={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in edges}
    rank={v:z3.Int('rank_%d_%d'%v) for v in points}
    owner={v:z3.Int('owner_%d_%d'%v) for v in points}
    dist={v:z3.Int('dist_%d_%d'%v) for v in points}
    roots={(r,s-1):1,(r,s+2):2}
    count=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs])
    blank=lambda v:z3.And(z3.Not(t[v]),z3.Not(p[v]))
    solver=z3.Solver();solver.set(timeout=args.seconds*1000,random_seed=2026102504)
    for v in points:
        partner=(v[0]^1,v[1])
        solver.add(z3.Not(z3.And(t[v],p[v])))
        solver.add(count(m[e] for e in incident[v])==z3.If(p[v],1,0))
        solver.add(rank[v]>=0,rank[v]<len(points),owner[v]>=0,owner[v]<=2,
                   dist[v]>=0,dist[v]<len(points))
        solver.add(z3.Implies(t[v],count(z3.Or(t[w],p[w]) for w in adjacent[v])<=1))
        kept=[z3.Or(t[w],z3.Or([z3.And(m[e],rank[next(x for x in e if x!=w)]<rank[v])
              for e in incident[w]])) for w in adjacent[v]]
        solver.add(z3.Implies(p[v],count(kept)>=2))
        solver.add(z3.Implies(z3.And(p[v],p[partner]),owner[v]==owner[partner]))
        if v[0] in (0,rows-1) or v[1] in (0,cols-1):solver.add(blank(v))
        if v in roots:solver.add(p[v],owner[v]==roots[v],dist[v]==0)
        else:
            descent=[]
            for w in adjacent[v]:
                connection=z3.Or(m[tuple(sorted((v,w)))],z3.And(w==partner,p[v],p[w]))
                descent.append(z3.And(connection,owner[w]==owner[v],dist[w]<dist[v]))
            solver.add(z3.Implies(z3.And(p[v],owner[v]>0),z3.Or(descent)))
    for v,w in edges:solver.add(z3.Implies(m[v,w],owner[v]==owner[w]))
    for label in (1,2):
        solver.add(count(z3.And(p[v],owner[v]==label,t[v[0]^1,v[1]]) for v in points)==2)
        solver.add(count(z3.And(p[v],owner[v]==label,blank((v[0]^1,v[1]))) for v in points)==0)
    for v in ((r+1,s-1),(r+1,s+2)):solver.add(t[v])
    for v in ((r+1,s),(r+1,s+1)):solver.add(blank(v))
    target=((r,s),(r,s+1));solver.add(m[target])
    if args.unsupported_core:
        bad={v:z3.Bool('bad_%d_%d'%v) for v in points}
        solver.add(z3.Or(list(bad.values())))
        for v in points:
            solver.add(z3.Implies(bad[v],z3.And(p[v],v not in target)))
            possible=[]
            for w in adjacent[v]:
                if w in target:continue
                possible.append(z3.Or(t[w],z3.Or([z3.And(m[e],z3.Not(bad[next(x for x in e if x!=w)]))
                    for e in incident[w]])))
            solver.add(z3.Implies(bad[v],count(possible)<=1))
        for band in range(rows//2):
            present={c:z3.Or(p[2*band,c],p[2*band+1,c]) for c in range(cols)}
            label={c:z3.If(p[2*band,c],owner[2*band,c],owner[2*band+1,c]) for c in range(cols)}
            left={c:z3.Int('left_%d_%d'%(band,c)) for c in range(cols)}
            right={c:z3.Int('right_%d_%d'%(band,c)) for c in range(cols)}
            for c in range(cols):
                solver.add(left[c]==z3.If(present[c],label[c],left[c-1] if c else 0))
                solver.add(right[c]==z3.If(present[c],label[c],right[c+1] if c+1<cols else 0))
                if c not in (0,cols-1):
                    solver.add(z3.Implies(z3.And(blank((2*band,c)),blank((2*band+1,c))),
                        z3.And(left[c]!=1,left[c]!=2,right[c]!=1,right[c]!=2)))
    else:
        solver.add(blank((r,s-2)))
    start=time.monotonic();status=solver.check()
    report=dict(status=str(status),shape=[rows,cols],seconds=time.monotonic()-start,
        reason_unknown=solver.reason_unknown(),solver_version=z3.get_version_string(),
        target=target,unsupported_core=args.unsupported_core,
        scope=('Discovery only: original frozen short beta between two distinct alpha TP tips; '
               'empty whole-support alpha owners and an arbitrary nonfreezing core after deletion.'
               if args.unsupported_core else
               'Discovery only: original frozen short beta between two distinct alpha TP tips; '
               'deletion leaves exposed alpha tip (8,4) with one occupied nonmate neighbor.'))
    if status==z3.sat:
        model=solver.model()
        selected={v for v in points if z3.is_true(model.eval(t[v]))}
        matching=[e for e in edges if z3.is_true(model.eval(m[e]))]
        current=rows,cols,selected,matching;direct_check(*current)
        frozen,layers=frozen_certificate(current);assert len(frozen)==2*len(matching)
        after=(*current[:3],[e for e in matching if e!=target])
        direct_check(*after)
        remaining,_=frozen_certificate(after)
        assert len(remaining)<2*len(after[3])
        report.update(selected=sorted(selected),matching=matching,freezing_layers=layers,
                      after_unfrozen=sorted({v for e in after[3] for v in e}-remaining))
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('selected','matching','freezing_layers','after_unfrozen')}))


if __name__=='__main__':main()
