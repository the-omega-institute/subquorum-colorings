"""Optional Z3 discovery for a forced escape that belongs to a pure PP cycle.

SAT is used only to discover an explicit board. A solver-free verifier checks
every resulting geometric and freezing assertion. No UNSAT/timeout conclusion
is used as a substitute for a general proof.
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
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows',type=int,default=12)
    parser.add_argument('--columns',type=int,default=14)
    parser.add_argument('--seconds',type=int,default=45)
    parser.add_argument('--two-forks',action='store_true')
    parser.add_argument('--double-ended',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    rows,cols = args.rows,args.columns
    assert rows >= 10 and cols >= 10 and rows%2 == cols%2 == 0
    points = list(itertools.product(range(rows),range(cols)))
    universe = set(points)
    adjacent = {v:sorted(set(neighbors(v))&universe) for v in points}
    edges = sorted({tuple(sorted((v,w))) for v in points for w in adjacent[v]})
    incident = {v:[e for e in edges if v in e] for v in points}
    t = {v:z3.Bool('t_%d_%d'%v) for v in points}
    p = {v:z3.Bool('p_%d_%d'%v) for v in points}
    m = {e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in edges}
    rank = {v:z3.Int('r_%d_%d'%v) for v in points}
    owner = {v:z3.Int('o_%d_%d'%v) for v in points}
    distance = {v:z3.Int('d_%d_%d'%v) for v in points}
    blank = lambda v:z3.And(z3.Not(t[v]),z3.Not(p[v]))
    count = lambda xs:z3.Sum([z3.If(x,1,0) for x in xs])
    solver = z3.Solver()
    solver.set(timeout=args.seconds*1000)
    roots = {(5,5):1,(5,4):2,(5,3):3,(5,6):4}
    if args.two_forks:
        roots.update({(8,7):5,(8,8):6,(8,9):7,(8,6):8})
    if args.double_ended:
        assert not args.two_forks
        roots.update({(8,5):1,(8,4):2,(8,3):5,(8,6):6})
    labels = max(roots.values())
    for v in points:
        solver.add(z3.Not(z3.And(t[v],p[v])))
        solver.add(count(m[e] for e in incident[v]) == z3.If(p[v],1,0))
        solver.add(rank[v]>=0,rank[v]<len(points),owner[v]>=0,owner[v]<=labels,
                   distance[v]>=0,distance[v]<len(points))
        solver.add(z3.Implies(t[v],count(z3.Or(t[w],p[w]) for w in adjacent[v])<=1))
        retained = [z3.Or(t[w],z3.Or([z3.And(m[e],rank[next(x for x in e if x!=w)]<rank[v])
                      for e in incident[w]])) for w in adjacent[v]]
        solver.add(z3.Implies(p[v],count(retained)>=2))
        partner = (v[0]^1,v[1])
        solver.add(z3.Implies(z3.And(p[v],p[partner]),owner[v]==owner[partner]))
        if v[0] in (0,rows-1) or v[1] in (0,cols-1):
            solver.add(blank(v))
        if v in roots:
            solver.add(p[v],owner[v]==roots[v],distance[v]==0)
        else:
            descent = []
            for w in adjacent[v]:
                connection = z3.Or(m[tuple(sorted((v,w)))],z3.And(w==partner,p[v],p[w]))
                descent.append(z3.And(connection,owner[w]==owner[v],distance[w]<distance[v]))
            solver.add(z3.Implies(z3.And(p[v],owner[v]>0),z3.Or(descent)))
    for x,y in edges:
        solver.add(z3.Implies(m[x,y],owner[x]==owner[y]))
    types = {1:(2,0),2:(0,2),3:(1,1),4:(1,1)}
    if args.two_forks:
        types.update({5:(2,0),6:(0,2),7:(1,1),8:(1,1)})
    if args.double_ended:
        types.update({5:(1,1),6:(1,1)})
    for label,(tp,bp) in types.items():
        solver.add(count(z3.And(p[v],owner[v]==label,t[v[0]^1,v[1]]) for v in points)==tp)
        solver.add(count(z3.And(p[v],owner[v]==label,blank((v[0]^1,v[1]))) for v in points)==bp)
    for v in ((4,3),(4,5)):
        solver.add(t[v])
    for v in ((4,4),(4,6)):
        solver.add(blank(v))
    # The diagonal escape is forced to be a two-vertex PP/M pure cycle.
    solver.add(m[((6,6),(7,6))],owner[6,6]==0,owner[7,6]==0)
    # The right BP begins a longer mixed strand, rather than a one-edge
    # self-link. Its mandatory outward mate and following PP column are real.
    solver.add(m[((5,6),(5,7))],p[4,7],owner[4,7]==4)
    if args.two_forks:
        for v in ((9,7),(9,9)):
            solver.add(t[v])
        for v in ((9,6),(9,8)):
            solver.add(blank(v))
        solver.add(m[((8,5),(8,6))],p[9,5],owner[9,5]==8)
    if args.double_ended:
        for v in ((9,3),(9,5)):
            solver.add(t[v])
        for v in ((9,4),(9,6)):
            solver.add(blank(v))
        solver.add(m[((8,6),(8,7))],p[9,7],owner[9,7]==6)
    start = time.monotonic()
    status = solver.check()
    report = dict(status=str(status),seconds=time.monotonic()-start,shape=[rows,cols],
        reason_unknown=solver.reason_unknown(),two_forks=args.two_forks,double_ended=args.double_ended,scope='Fixed local beta/alpha/mixed terminal motif '
        'with diagonal pure PP cycle and longer outward mixed branch; no global nonexistence inference.')
    if status == z3.sat:
        model = solver.model()
        selected = {v for v in points if z3.is_true(model.eval(t[v]))}
        matching = [e for e in edges if z3.is_true(model.eval(m[e]))]
        current = rows,cols,selected,matching
        direct_check(*current)
        frozen,layers = frozen_certificate(current)
        assert len(frozen)==2*len(matching)
        report.update(selected=sorted(selected),matching=matching,freezing_layers=layers,
                      solver_ranks=[dict(point=v,rank=model.eval(rank[v]).as_long())
                                    for v in sorted(frozen)])
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in {'selected','matching','freezing_layers','solver_ranks'}}))


if __name__ == '__main__':
    main()
