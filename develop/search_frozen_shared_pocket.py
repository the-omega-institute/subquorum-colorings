"""Optional discovery: a guarded pocket whose TP boundaries have different alphas.

SAT proposes a board; the solver-free checker supplies all permanent checks.
No nonexistence claim is drawn from UNSAT, UNKNOWN or timeout.
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
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--seconds',type=int,default=60)
    parser.add_argument('--tight-support',action='store_true');args=parser.parse_args()
    rows,cols=16,14;points=list(itertools.product(range(rows),range(cols)));universe=set(points)
    adjacent={v:sorted(set(neighbors(v))&universe) for v in points}
    edges=sorted({tuple(sorted((v,w))) for v in points for w in adjacent[v]})
    incident={v:[e for e in edges if v in e] for v in points}
    t={v:z3.Bool('t_%d_%d'%v) for v in points};p={v:z3.Bool('p_%d_%d'%v) for v in points}
    m={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in edges}
    rank={v:z3.Int('rank_%d_%d'%v) for v in points}
    owner={v:z3.Int('owner_%d_%d'%v) for v in points}
    dist={v:z3.Int('dist_%d_%d'%v) for v in points}
    roots={(8,4):1,(8,7):2};count=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs])
    blank=lambda v:z3.And(z3.Not(t[v]),z3.Not(p[v]))
    solver=z3.Solver();solver.set(timeout=args.seconds*1000,random_seed=20261026)
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
    for v in ((9,4),(9,7)):solver.add(t[v])
    for v in ((8,5),(8,6),(9,5),(9,6)):solver.add(blank(v))
    for v in ((6,5),(6,6),(7,5),(7,6)):solver.add(p[v])
    if args.tight_support:
        # Discovery restriction: the only internal BB interval sites whose
        # endpoint-free gap sees either named alpha are the pocket columns.
        for band in range(rows//2):
            present={c:z3.Or(p[2*band,c],p[2*band+1,c]) for c in range(cols)}
            label={c:z3.If(p[2*band,c],owner[2*band,c],owner[2*band+1,c]) for c in range(cols)}
            left={c:z3.Int('left_%d_%d'%(band,c)) for c in range(cols)}
            right={c:z3.Int('right_%d_%d'%(band,c)) for c in range(cols)}
            for c in range(cols):
                solver.add(left[c]==z3.If(present[c],label[c],left[c-1] if c else 0))
                solver.add(right[c]==z3.If(present[c],label[c],right[c+1] if c+1<cols else 0))
                if c not in (0,cols-1) and (band,c) not in ((4,5),(4,6)):
                    solver.add(z3.Implies(z3.And(blank((2*band,c)),blank((2*band+1,c))),
                        z3.And(left[c]!=1,left[c]!=2,right[c]!=1,right[c]!=2)))
    start=time.monotonic();status=solver.check()
    report=dict(status=str(status),shape=[rows,cols],seconds=time.monotonic()-start,tight_support=args.tight_support,
        reason_unknown=solver.reason_unknown(),solver_version=z3.get_version_string(),
        scope='Fixed guarded two-column pocket with two different original alpha owners; discovery only.')
    if status==z3.sat:
        model=solver.model();selected={v for v in points if z3.is_true(model.eval(t[v]))}
        matching=[e for e in edges if z3.is_true(model.eval(m[e]))]
        current=rows,cols,selected,matching;direct_check(*current)
        frozen,layers=frozen_certificate(current);assert len(frozen)==2*len(matching)
        report.update(selected=sorted(selected),matching=matching,freezing_layers=layers)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in ('selected','matching','freezing_layers')}))


if __name__=='__main__':main()
