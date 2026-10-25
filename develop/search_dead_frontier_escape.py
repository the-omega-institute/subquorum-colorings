"""Optional bounded discovery of a vertical fork with a dead forced H escape.

SAT boards require independent verification. UNSAT/UNKNOWN is not a theorem.
"""
import argparse,itertools,json,time
from pathlib import Path
import z3
from check_cooperative_promotion import neighbors
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_whole_support_fork_normal_form import whole_support_data
from check_compensation_flow_normal_form import owner_data


def search(rows,cols,seconds,typed,rich_gate=False,double_dead=False):
    assert rows >= 14 and rows % 2 == 0 and cols >= (24 if double_dead else 18)
    assert seconds > 0 and (typed or not rich_gate)
    shift=8 if double_dead else 0
    mv=lambda v:(v[0],v[1]+shift)
    U=set(itertools.product(range(rows),range(cols)));points=sorted(U)
    adj={v:sorted(set(neighbors(v))&U) for v in points};edges=sorted({tuple(sorted((v,w))) for v in points for w in adj[v]});inc={v:[e for e in edges if v in e] for v in points}
    T={v:z3.Bool('t%d_%d'%v) for v in points};P={v:z3.Bool('p%d_%d'%v) for v in points};M={e:z3.Bool('m%d_%d_%d_%d'%(*e[0],*e[1])) for e in edges};rank={v:z3.Int('r%d_%d'%v) for v in points}
    count=lambda xs:z3.Sum([z3.If(x,1,0) for x in xs]);blank=lambda v:z3.And(z3.Not(T[v]),z3.Not(P[v]))
    S=z3.Solver();S.set(timeout=seconds*1000)
    for v in points:
        S.add(z3.Not(z3.And(T[v],P[v])),count(M[e] for e in inc[v])==z3.If(P[v],1,0),rank[v]>=0,rank[v]<len(points))
        S.add(z3.Implies(T[v],count(z3.Or(T[w],P[w]) for w in adj[v])<=1))
        retained=[z3.Or(T[w],z3.Or([z3.And(M[e],rank[next(x for x in e if x!=w)]<rank[v]) for e in inc[w]])) for w in adj[v]]
        S.add(z3.Implies(P[v],count(retained)>=2))
        if v[0] in (0,rows-1) or v[1] in (0,cols-1):S.add(blank(v))
    # t=(5,7), central vertical BP b=(5,6), other TP u=(5,5).
    # Forced H root=(5,8), TP=(5,9); its two-BT gap ends at opposite-row BP.
    for v in [(4,5),(4,7),(4,9),(5,10),(4,11)]:S.add(T[mv(v)])
    for v in [(4,6),(4,8),(4,10),(5,11),(5,12)]:S.add(blank(mv(v)))
    for v in [(5,5),(5,6),(5,7),(5,8),(5,9),(4,12)]:S.add(P[mv(v)])
    for e in [((5,7),(6,7)),((5,6),(6,6)),((5,8),(5,9))]:S.add(M[tuple(sorted(map(mv,e)))])
    if typed:
        roots={mv(v):i for v,i in {(5,6):1,(5,7):2,(5,5):3,(5,8):4}.items()};own={v:z3.Int('o%d_%d'%v) for v in points};dist={v:z3.Int('d%d_%d'%v) for v in points}
        for v in points:
            partner=(v[0]^1,v[1]);S.add(own[v]>=0,own[v]<=4,dist[v]>=0,dist[v]<len(points))
            S.add(z3.Implies(z3.And(P[v],P[partner]),own[v]==own[partner]))
            if v in roots:S.add(own[v]==roots[v],dist[v]==0)
            else:
                S.add(z3.Implies(z3.And(P[v],own[v]>0),z3.Or([z3.And(z3.Or(M[tuple(sorted((v,w)))],z3.And(w==partner,P[v],P[w])),own[w]==own[v],dist[w]<dist[v]) for w in adj[v]])))
        for u,v in edges:S.add(z3.Implies(M[u,v],own[u]==own[v]))
        for label,ntp,nbp in [(1,1,1),(2,2,0),(3,2,0),(4,1,1)]:
            S.add(count(z3.And(P[v],own[v]==label,T[v[0]^1,v[1]]) for v in points)==ntp)
            S.add(count(z3.And(P[v],own[v]==label,blank((v[0]^1,v[1]))) for v in points)==nbp)
    if rich_gate:
        assert typed
        S.add(P[mv((10,4))],own[mv((10,4))]==1,T[mv((11,4))],T[mv((10,6))],blank(mv((11,6))))
        for c in (5,7):S.add(blank(mv((10,c))),blank(mv((11,c))))
    if double_dead:
        for v in [(4,11),(5,10),(4,9)]:S.add(T[v])
        for v in [(4,12),(4,10),(5,9),(5,8)]:S.add(blank(v))
        for v in [(5,12),(5,11),(4,8)]:S.add(P[v])
        S.add(M[((5,11),(5,12))])
    start=time.monotonic();status=S.check();out=dict(status=str(status),shape=[rows,cols],elapsed_seconds=time.monotonic()-start,reason=S.reason_unknown(),typed=typed,rich_gate=rich_gate,double_dead=double_dead,coordinate_shift=shift,scope='Bounded discovery; no general inference from UNSAT/UNKNOWN.')
    if status==z3.sat:
        model=S.model();ts={v for v in points if z3.is_true(model.eval(T[v]))};ms=[e for e in edges if z3.is_true(model.eval(M[e]))];cur=rows,cols,ts,ms
        direct_check(*cur);F,layers=frozen_certificate(cur);assert len(F)==2*len(ms)
        data,meta,_=whole_support_data(cur,whole_bands(cur));o,A,B,MM=owner_data(*data[:2]);dead=o[mv((5,8))]
        assert dead in MM and set(data[1][dead])=={mv((5,8)),mv((5,9))} and not data[3][dead]
        assert [e for e in data[2] if e[0]==mv((5,9))]==[(mv((5,9)),mv((5,8)))]
        if typed:assert o[mv((5,6))] in MM and o[mv((5,7))] in A and o[mv((5,5))] in A and o[mv((5,7))]!=o[mv((5,5))]
        if rich_gate:assert len(data[3][o[mv((5,6))]])>=2
        if double_dead:
            left=o[5,12]
            assert left in MM and not data[3][left] and set(data[1][left])=={(5,11),(5,12)}
        out.update(selected=sorted(ts),matching=ms,freezing_layers=[[w['endpoint'] for w in layer] for layer in layers],endpoints=len(F),selected_count=len(ts),fork_owners=[o[mv((5,5))],o[mv((5,6))],o[mv((5,7))]],dead_owner=dead)
    return out
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--rows',type=int,default=14);ap.add_argument('--columns',type=int,default=18);ap.add_argument('--seconds',type=int,default=40);ap.add_argument('--typed',action='store_true');ap.add_argument('--rich-gate',action='store_true');ap.add_argument('--double-dead',action='store_true');ap.add_argument('--output',type=Path,required=True);a=ap.parse_args();r=search(a.rows,a.columns,a.seconds,a.typed,a.rich_gate,a.double_dead);a.output.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps({k:v for k,v in r.items() if k not in ['selected','matching','freezing_layers']}))
