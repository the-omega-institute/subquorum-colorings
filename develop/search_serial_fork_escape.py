"""Optional bounded discovery of an actual nested alpha/mixed/beta fork.

SAT boards are solver-free verified. UNKNOWN/UNSAT are not general proofs.
"""
import argparse
from collections import Counter
import itertools,json,time
from pathlib import Path
import z3
from check_cooperative_promotion import neighbors
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_whole_support_fork_normal_form import whole_support_data
from check_compensation_flow_normal_form import owner_data


def search(rows,cols,seconds,nonfrozen_control=False):
    points=list(itertools.product(range(rows),range(cols)));U=set(points)
    adj={v:sorted(set(neighbors(v))&U) for v in points}
    edges=sorted({tuple(sorted((v,w))) for v in points for w in adj[v]})
    inc={v:[e for e in edges if v in e] for v in points}
    T={v:z3.Bool('t%d_%d'%v) for v in points};P={v:z3.Bool('p%d_%d'%v) for v in points}
    M={e:z3.Bool('m%d_%d_%d_%d'%(*e[0],*e[1])) for e in edges}
    rank={v:z3.Int('r%d_%d'%v) for v in points};owner={v:z3.Int('o%d_%d'%v) for v in points}
    dist={v:z3.Int('d%d_%d'%v) for v in points}
    count=lambda terms:z3.Sum([z3.If(x,1,0) for x in terms])
    blank=lambda v:z3.And(z3.Not(T[v]),z3.Not(P[v]))
    roots={(5,8):1,(5,10):2,(5,9):3,(10,10):4}
    S=z3.Solver();S.set(timeout=seconds*1000)
    for v in points:
        partner=(v[0]^1,v[1])
        S.add(z3.Not(z3.And(T[v],P[v])),count(M[e] for e in inc[v])==z3.If(P[v],1,0))
        S.add(rank[v]>=0,rank[v]<len(points),owner[v]>=0,owner[v]<=4,dist[v]>=0,dist[v]<len(points))
        S.add(z3.Implies(T[v],count(z3.Or(T[w],P[w]) for w in adj[v])<=1))
        retained=[z3.Or(T[w],z3.Or([z3.And(M[e],rank[next(x for x in e if x!=w)]<rank[v]) for e in inc[w]])) for w in adj[v]]
        if not nonfrozen_control:S.add(z3.Implies(P[v],count(retained)>=2))
        S.add(z3.Implies(z3.And(P[v],P[partner]),owner[v]==owner[partner]))
        if v[0] in (0,rows-1) or v[1] in (0,cols-1):S.add(blank(v))
        if v in roots:S.add(P[v],owner[v]==roots[v],dist[v]==0)
        else:
            descent=[z3.And(z3.Or(M[tuple(sorted((v,w)))],z3.And(w==partner,P[v],P[w])),owner[w]==owner[v],dist[w]<dist[v]) for w in adj[v]]
            S.add(z3.Implies(z3.And(P[v],owner[v]>0),z3.Or(descent)))
    for u,v in edges:S.add(z3.Implies(M[u,v],owner[u]==owner[v]))
    for label,ntp,nbp in [(1,2,0),(2,2,0),(3,1,1),(4,0,2)]:
        S.add(count(z3.And(P[v],owner[v]==label,T[v[0]^1,v[1]]) for v in points)==ntp)
        S.add(count(z3.And(P[v],owner[v]==label,blank((v[0]^1,v[1]))) for v in points)==nbp)
    for v in [(4,8),(4,10),(11,9),(11,11)]:S.add(T[v])
    for v in [(4,9),(11,10),(11,8)]:S.add(blank(v))
    S.add(T[10,8] if nonfrozen_control else blank((10,8)))
    S.add(P[10,9],owner[10,9]==3,P[10,11])
    start=time.monotonic();status=S.check()
    out=dict(status=str(status),shape=[rows,cols],elapsed_seconds=time.monotonic()-start,reason=S.reason_unknown(),scope='Bounded discovery only; no general impossibility inference.',nonfrozen_control=nonfrozen_control)
    if status==z3.sat:
        model=S.model();ts={v for v in points if z3.is_true(model.eval(T[v]))};ms=[e for e in edges if z3.is_true(model.eval(M[e]))]
        cur=rows,cols,ts,ms;direct_check(*cur);frozen,layers=frozen_certificate(cur);assert nonfrozen_control or len(frozen)==2*len(ms)
        ranks=[[tuple(w['endpoint']) for w in layer] for layer in layers]
        if not nonfrozen_control:check_rank_certificate(cur,ranks)
        d,meta,_=whole_support_data(cur,whole_bands(cur));o,A,B,MM=owner_data(*d[:2])
        assert o[5,8] in A and o[5,10] in A and o[5,8]!=o[5,10]
        assert o[5,9]==o[10,9] in MM and o[10,10] in B
        out.update(selected=sorted(ts),matching=ms,freezing_layers=ranks,head=[5,9],output=[10,9],beta_entry=[10,10],other_tp=[10,11],outer_site=[10,8],outer_is_selected=nonfrozen_control,frozen_endpoint_count=len(frozen),
                   source_owners=[o[5,8],o[5,10]],endpoints=2*len(ms),selected_count=len(ts))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rows',type=int,default=14);ap.add_argument('--columns',type=int,default=18);ap.add_argument('--seconds',type=int,default=45);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--nonfrozen-control',action='store_true');a=ap.parse_args()
    out=search(a.rows,a.columns,a.seconds,a.nonfrozen_control);a.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k not in ['selected','matching','freezing_layers']}))
