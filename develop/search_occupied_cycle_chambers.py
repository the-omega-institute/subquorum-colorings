"""Optional Z3 discovery; bounded UNSAT/timeout is not a general proof."""
import argparse,itertools,json,time
from pathlib import Path
import z3
from check_merger_completion_reserves import neighbors,feasible,frozen
from check_promotion_cores import frozen_certificate
from check_whole_support_fork_normal_form import whole_support_data
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_whole_support_fork_flow import fork_flow
from check_compensation_flow_normal_form import owner_data


from check_occupied_cycle_chambers import scaffold


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bottom',type=int,default=12);ap.add_argument('--right',type=int,default=10)
    ap.add_argument('--no-freeze',action='store_true');ap.add_argument('--seconds',type=int,default=30);ap.add_argument('--mixed',action='store_true');ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    T0,M0,roots,blank=scaffold(args.bottom,5,args.right)
    rows,cols=args.bottom+4,args.right+6
    if rows%2:rows+=1
    points=list(itertools.product(range(rows),range(cols)));universe=set(points)
    N={v:sorted(set(neighbors(v))&universe) for v in points}
    E=sorted({tuple(sorted((v,w))) for v in points for w in N[v]})
    inc={v:[e for e in E if v in e] for v in points}
    t={v:z3.Bool('t_%d_%d'%v) for v in points};p={v:z3.Bool('p_%d_%d'%v) for v in points}
    m={e:z3.Bool('m_%d_%d_%d_%d'%(*e[0],*e[1])) for e in E}
    rank={v:z3.Int('r_%d_%d'%v) for v in points}
    own={v:z3.Int('o_%d_%d'%v) for v in points};dist={v:z3.Int('d_%d_%d'%v) for v in points}
    count=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs])
    solver=z3.Solver();solver.set(timeout=args.seconds*1000)
    labels={v:i+1 for i,v in enumerate(roots)}
    for v in points:
        solver.add(z3.Not(z3.And(t[v],p[v])),count(m[e] for e in inc[v])==z3.If(p[v],1,0))
        solver.add(z3.Implies(t[v],count(z3.Or(t[w],p[w]) for w in N[v])<=1))
        solver.add(rank[v]>=0,rank[v]<len(points))
        retained=[z3.Or(t[w],z3.Or([z3.And(m[e],rank[next(x for x in e if x!=w)]<rank[v]) for e in inc[w]])) for w in N[v]]
        if not args.no_freeze:solver.add(z3.Implies(p[v],count(retained)>=2))
        if v in T0:solver.add(t[v])
        if v in blank or v[1] in (0,cols-1):solver.add(z3.Not(t[v]),z3.Not(p[v]))
        if args.mixed:
            q=(v[0]^1,v[1]);solver.add(own[v]>=0,own[v]<=4,dist[v]>=0,dist[v]<len(points))
            solver.add(z3.Implies(z3.And(p[v],p[q]),own[v]==own[q]))
            if v in labels:solver.add(own[v]==labels[v],dist[v]==0)
            else:
                descent=[z3.And(z3.Or(m[tuple(sorted((v,w)))],z3.And(w==q,p[w])),own[v]==own[w],dist[w]<dist[v]) for w in N[v]]
                solver.add(z3.Implies(z3.And(p[v],own[v]>0),z3.Or(descent)))
    for e in M0:solver.add(m[tuple(sorted(e))])
    if args.mixed:
        for e in E:solver.add(z3.Implies(m[e],own[e[0]]==own[e[1]]))
        for g in range(1,5):
            solver.add(count(z3.And(p[v],own[v]==g,t[v[0]^1,v[1]]) for v in points)==1)
            solver.add(count(z3.And(p[v],own[v]==g,z3.Not(p[v[0]^1,v[1]]),z3.Not(t[v[0]^1,v[1]])) for v in points)==1)
    start=time.monotonic();answer=solver.check();elapsed=time.monotonic()-start
    record=dict(status=str(answer),seconds=elapsed,bottom=args.bottom,right=args.right,mixed=args.mixed,freeze_required=not args.no_freeze)
    if answer==z3.sat:
        model=solver.model();T={v for v in points if z3.is_true(model.eval(t[v]))};M=[e for e in E if z3.is_true(model.eval(m[e]))]
        cur=(rows,cols,T,M);assert feasible(cur)
        if not args.no_freeze:assert frozen(cur)
        d,meta,_=whole_support_data(cur,whole_bands(cur));o,aa,bb,mm=owner_data(*d[:2]);flow=fork_flow(*d)
        _,layers=frozen_certificate(cur)
        record.update(shape=(rows,cols),selected=sorted(T),matching=M,freezing_layers=[[x['endpoint'] for x in layer] for layer in layers],
            gates=[dict(bp=v,owner=o[v],kind='mixed' if o[v] in mm else 'beta' if o[v] in bb else 'alpha',terminals=d[1][o[v]]) for v in roots],
            k=len(aa),b=len(bb),I=len(d[4]),value=flow['value'],cost=flow['cost'])
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps({k:v for k,v in record.items() if k not in ('matching','selected','freezing_layers')}),flush=True)

if __name__=='__main__':main()
