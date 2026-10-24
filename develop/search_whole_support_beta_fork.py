"""Optional discovery only: frozen beta with a PP interval and two alpha entries.

SAT discovery is not used in the general normalization proof. A produced model
must pass the solver-free geometric/primitive verifier before being used.
"""
import argparse
import itertools
import json
from pathlib import Path
import time

import z3
from check_cooperative_promotion import neighbors
from check_even_bridge_support_completion import endpoints_of
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_normal_form import whole_support_data, primitive_certificates


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--rows',type=int,default=12)
    parser.add_argument('--columns',type=int,default=14);parser.add_argument('--seconds',type=int,default=60)
    parser.add_argument('--lower-side',choices=('left','right'),default='left')
    parser.add_argument('--flexible-beta',action='store_true')
    parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    rows,cols=args.rows,args.columns
    assert rows>=12 and cols>=10 and rows%2==cols%2==0
    points=list(itertools.product(range(rows),range(cols)));universe=set(points)
    adj={v:sorted(set(neighbors(v))&universe) for v in points}
    edges=sorted({tuple(sorted((v,w))) for v in points for w in adj[v]})
    incident={v:[e for e in edges if v in e] for v in points}
    selected={v:z3.Bool('t_%d_%d'%v) for v in points}
    endpoint={v:z3.Bool('p_%d_%d'%v) for v in points}
    matching={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in edges}
    rank={v:z3.Int('r_%d_%d'%v) for v in points}
    owner={v:z3.Int('o_%d_%d'%v) for v in points}
    count=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs])
    solver=z3.Solver();solver.set(timeout=args.seconds*1000)
    blank=lambda v:z3.And(z3.Not(selected[v]),z3.Not(endpoint[v]))
    for v in points:
        solver.add(z3.Not(z3.And(selected[v],endpoint[v])))
        solver.add(count(matching[e] for e in incident[v])==z3.If(endpoint[v],1,0))
        solver.add(rank[v]>=0,rank[v]<len(points),owner[v]>=0,owner[v]<=3)
        solver.add(z3.Implies(selected[v],count(z3.Or(selected[w],endpoint[w]) for w in adj[v])<=1))
        retained=[z3.Or(selected[w],z3.Or([z3.And(matching[e],rank[next(u for u in e if u!=w)]<rank[v]) for e in incident[w]])) for w in adj[v]]
        solver.add(z3.Implies(endpoint[v],count(retained)>=2))
        matecolumn=(v[0]^1,v[1])
        solver.add(z3.Implies(z3.And(endpoint[v],endpoint[matecolumn]),owner[v]==owner[matecolumn]))
        if v[0] in (0,rows-1) or v[1] in (0,cols-1):solver.add(blank(v))
    for a,b in edges:solver.add(z3.Implies(matching[a,b],owner[a]==owner[b]))
    for label in (1,2,3):
        solver.add(count(z3.And(endpoint[v],selected[v[0]^1,v[1]],owner[v]==label) for v in points)==(0 if label==3 else 2))
        solver.add(count(z3.And(endpoint[v],blank((v[0]^1,v[1])),owner[v]==label) for v in points)==(2 if label==3 else 0))
    lower_col=5 if args.lower_side=='left' else 7
    for v,label in [((5,5),1),((8,lower_col),2),((5,6),3),((8,6),3)]:solver.add(endpoint[v],owner[v]==label)
    for v in ((4,5),(9,lower_col),(5,7),(8,12-lower_col)):solver.add(selected[v])
    for v in ((4,6),(9,6),(6,7),(7,7)):solver.add(blank(v))
    if args.flexible_beta:
        for v in ((6,6),(7,6)):solver.add(endpoint[v],owner[v]==3)
    else:
        for e in [((5,6),(6,6)),((7,6),(8,6))]:solver.add(matching[e])
    started=time.monotonic();status=solver.check()
    report=dict(status=str(status),seconds=time.monotonic()-started,shape=[rows,cols],
        reason=solver.reason_unknown(),lower_side=args.lower_side,flexible_beta=args.flexible_beta,
        scope='Specified beta endpoints5,6 and8,6 with internalPP6,6/7,6 seeingBB6,7/7,7; two separate adjacent alpha entries. No universal nonexistence inference from finite failure.')
    if status==z3.sat:
        model=solver.model();tt={v for v in points if z3.is_true(model.eval(selected[v]))}
        mm=[e for e in edges if z3.is_true(model.eval(matching[e]))]
        current=rows,cols,tt,mm;direct_check(*current)
        assert frozen_certificate(current)[0]==endpoints_of(current)
        data,meta,witness=whole_support_data(current,whole_bands(current))
        forks=[p for p in primitive_certificates(*data) if p['kind']=='fork']
        desired=[p for p in forks if set(p['links'])=={((5,5),(5,6)),((8,lower_col),(8,6))}
                 and witness[p['beta'],p['interval']]==(3,6)]
        assert desired
        report.update(selected=sorted(tt),matching=mm,verified_fork=desired[0])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({k:v for k,v in report.items() if k not in ('selected','matching')},default=list))

if __name__=='__main__':main()
