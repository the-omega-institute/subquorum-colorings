"""Optional discovery of two horizontal short mixed tails at one physical BP.

SAT is discovery only. Every saved SAT board is solver-free checked; neither
UNSAT nor a timeout is evidence of general nonexistence.
"""
import argparse
import itertools
import json
from pathlib import Path
import time
import z3

from check_cooperative_promotion import neighbors
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_normal_form import whole_support_data
from check_short_mixed_chains import chains
from check_compensation_flow_normal_form import owner_data


def search(rows,cols,row,col,seconds,entered=False,mixed_receiver=False,rich_gate=False,sealed_escape=False,upper_sources=False):
    assert rows%2==cols%2==0 and row%2==1 and 3<=row<rows-3 and 4<=col<cols-4
    assert not mixed_receiver or entered
    assert not rich_gate or entered and mixed_receiver and row+6<rows
    assert not upper_sources or entered
    points=list(itertools.product(range(rows),range(cols)));universe=set(points)
    adjacent={v:sorted(set(neighbors(v))&universe) for v in points}
    edges=sorted({tuple(sorted((v,w))) for v in points for w in adjacent[v]})
    incident={v:[e for e in edges if v in e] for v in points}
    t={v:z3.Bool('t_%d_%d'%v) for v in points};p={v:z3.Bool('p_%d_%d'%v) for v in points}
    m={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in edges}
    rank={v:z3.Int('r_%d_%d'%v) for v in points}
    count=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs])
    blank=lambda v:z3.And(z3.Not(t[v]),z3.Not(p[v]))
    solver=z3.Solver();solver.set(timeout=seconds*1000)
    for v in points:
        solver.add(z3.Not(z3.And(t[v],p[v])))
        solver.add(count(m[e] for e in incident[v])==z3.If(p[v],1,0))
        solver.add(rank[v]>=0,rank[v]<len(points))
        solver.add(z3.Implies(t[v],count(z3.Or(t[w],p[w]) for w in adjacent[v])<=1))
        retained=[z3.Or(t[w],z3.Or([z3.And(m[e],rank[next(x for x in e if x!=w)]<rank[v])
                    for e in incident[w]])) for w in adjacent[v]]
        solver.add(z3.Implies(p[v],count(retained)>=2))
        if v[0] in (0,rows-1) or v[1] in (0,cols-1):solver.add(blank(v))
    for delta in (-2,-1,0,1,2):solver.add(p[row,col+delta])
    for delta in (-1,1):solver.add(t[row-1,col+delta])
    for delta in (-2,0,2):solver.add(blank((row-1,col+delta)))
    for a,b in [((row,col-2),(row,col-1)),((row,col+1),(row,col+2))]:
        solver.add(m[tuple(sorted((a,b)))])
    if sealed_escape:
        solver.add(m[((row+1,col-1),(row+2,col-1))])
        for rr in (row+1,row+2):
            for cc in (col-2,col):solver.add(p[rr,cc])
    if entered:
        roots={(row,col-3):1,(row,col+3):2,(row,col):3}
        owner={v:z3.Int('o_%d_%d'%v) for v in points}
        dist={v:z3.Int('d_%d_%d'%v) for v in points}
        for v in points:
            partner=(v[0]^1,v[1])
            solver.add(owner[v]>=0,owner[v]<=3,dist[v]>=0,dist[v]<len(points))
            solver.add(z3.Implies(z3.And(p[v],p[partner]),owner[v]==owner[partner]))
            if v in roots:solver.add(p[v],owner[v]==roots[v],dist[v]==0)
            else:
                descent=[z3.And(z3.Or(m[tuple(sorted((v,w)))],z3.And(w==partner,p[v],p[w])),
                               owner[w]==owner[v],dist[w]<dist[v]) for w in adjacent[v]]
                solver.add(z3.Implies(z3.And(p[v],owner[v]>0),z3.Or(descent)))
        for x,y in edges:solver.add(z3.Implies(m[x,y],owner[x]==owner[y]))
        for label in (1,2,3):
            tp_count=2 if label<3 else int(mixed_receiver)
            bp_count=0 if label<3 else 2-int(mixed_receiver)
            solver.add(count(z3.And(p[v],owner[v]==label,t[v[0]^1,v[1]]) for v in points)==tp_count)
            solver.add(count(z3.And(p[v],owner[v]==label,blank((v[0]^1,v[1]))) for v in points)==bp_count)
        solver.add(t[row-1,col-3],t[row-1,col+3])
        if upper_sources:
            for v in points:
                if v[0]>=row+3:solver.add(z3.Implies(p[v],z3.And(owner[v]!=1,owner[v]!=2)))
        if rich_gate:
            assert mixed_receiver
            v=(row+5,col);solver.add(p[v],owner[v]==3,t[v[0]^1,v[1]])
            for dc in (1,3):
                solver.add(blank((v[0],col+dc)),blank((v[0]^1,col+dc)))
            solver.add(t[v[0],col+2],blank((v[0]^1,col+2)))
    start=time.monotonic();status=solver.check()
    report=dict(status=str(status),seconds=time.monotonic()-start,shape=[rows,cols],motif_center=[row,col],
                entered=entered,mixed_receiver=mixed_receiver,rich_gate=rich_gate,sealed_escape=sealed_escape,upper_sources=upper_sources,
                reason_unknown=solver.reason_unknown(),
                scope='Fixed motif discovery only, no global impossibility inference.')
    if status==z3.sat:
        model=solver.model();selected={v for v in points if z3.is_true(model.eval(t[v]))}
        matching=[e for e in edges if z3.is_true(model.eval(m[e]))];current=rows,cols,selected,matching
        direct_check(*current);frozen,layers=frozen_certificate(current);assert len(frozen)==2*len(matching)
        data,meta,_=whole_support_data(current,whole_bands(current));rs,tp,bp,internal=chains(current,whole_bands(current),data)
        owner,aa,bb,mm=owner_data(*data[:2]);left,right=owner[row,col-1],owner[row,col+1]
        assert left!=right and left in mm and right in mm
        assert data[0][row,col]=='BP' and data[0][row,col-1]==data[0][row,col+1]=='TP'
        assert any(x[-1]==left for x in rs) and any(x[-1]==right for x in rs)
        if entered:
            assert owner[row,col-3] in aa and owner[row,col+3] in aa and owner[row,col-3]!=owner[row,col+3]
            assert owner[row,col] in (mm if mixed_receiver else bb)
        report.update(selected=sorted(selected),matching=matching,freezing_layers=layers,
            solver_ranks=[dict(point=v,rank=model.eval(rank[v]).as_long()) for v in sorted(frozen)])
    return report


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--rows',type=int,default=12);ap.add_argument('--columns',type=int,default=14)
    ap.add_argument('--row',type=int,default=5);ap.add_argument('--column',type=int,default=7)
    ap.add_argument('--seconds',type=int,default=45);ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--entered',action='store_true');ap.add_argument('--mixed-receiver',action='store_true')
    ap.add_argument('--rich-gate',action='store_true');ap.add_argument('--sealed-escape',action='store_true')
    ap.add_argument('--upper-sources',action='store_true');a=ap.parse_args()
    r=search(a.rows,a.columns,a.row,a.column,a.seconds,a.entered,a.mixed_receiver,a.rich_gate,a.sealed_escape,a.upper_sources);a.output.write_text(json.dumps(r,indent=2)+'\n')
    print(json.dumps({k:v for k,v in r.items() if k not in ('selected','matching','freezing_layers','solver_ranks')}))

if __name__=='__main__':main()
