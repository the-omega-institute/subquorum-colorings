"""Exact contact-pool coverage and physical two-colour cost controls.

Proofs for every finite pool are in CONTACT_FLOW_CUT_AND_EXACT_COST.md.
The cost control enumerates RED arc assignments on tiny instances, not
contact subsets, and solves the complementary blue min-cost flow.
"""
from collections import deque
from itertools import product
from pathlib import Path
import json
import random

from check_mixed_terminal_compensation import decompose, edge, grid, selected_feasible
from check_ordered_th_relay import all_gates, family as relay_family, wrong_order_control
from check_shared_th_star import family as star_family
from check_contact_cycle_ledger import row_family, same_order_witness
from check_five_contact_barrier import family as five_family, path_builder

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')
ROOT=Path(__file__).resolve().parents[1]


class Network:
    """Each path is (black_is_T,white_is_T,ordered_contact_ids,weights)."""
    def __init__(self, paths):
        self.paths=paths; self.arcs=[];self.incoming={};self.outgoing={}
        self.starts=[];self.ends=[]
        for i,(bt,wt,order,weights) in enumerate(paths):
            assert len(weights)==len(order)+1 and min(weights)>=0
            assert len(set(order))==len(order)
            nodes=[('b',i)]+[('g',g) for g in order]+[('w',i)]
            self.starts.append(len(self.arcs))
            for u,v,w in zip(nodes,nodes[1:],weights):
                j=len(self.arcs);self.arcs.append((u,v,w,i))
                self.outgoing.setdefault(u,[]).append(j)
                self.incoming.setdefault(v,[]).append(j)
            self.ends.append(len(self.arcs)-1)
        self.gates=sorted(v for v in self.incoming if v[0]=='g')
        for g in self.gates:
            assert len(self.incoming[g])==len(self.outgoing[g])==2
            assert len({self.arcs[j][3] for j in self.incoming[g]})==2
        self.BT=sum(p[0] for p in paths);self.WT=sum(p[1] for p in paths)

    def switches(self, colours):
        result=set()
        for g in self.gates:
            ins=sorted(self.incoming[g],key=lambda j:self.arcs[j][3])
            outs=sorted(self.outgoing[g],key=lambda j:self.arcs[j][3])
            a,b=[colours[j] for j in ins];c,d=[colours[j] for j in outs]
            if (a,b)==(c,d):continue
            assert (a,b)==(d,c),(g,a,b,c,d)
            result.add(g[1])
        return result

    def route(self, switches):
        nxt={}
        for g in self.gates:
            ins=sorted(self.incoming[g],key=lambda j:self.arcs[j][3])
            outs=sorted(self.outgoing[g],key=lambda j:self.arcs[j][3])
            if g[1] in switches:outs.reverse()
            nxt.update(zip(ins,outs))
        used=set();counts=[0,0,0];paid=set();red=set();blue=set();endpoints=[]
        for i,start in enumerate(self.starts):
            j=start;part=set()
            while True:
                assert j not in used;used.add(j);part.add(j)
                v=self.arcs[j][1]
                if v[0]=='w':break
                j=nxt[j]
            bt=self.paths[i][0];wt=self.paths[v[1]][1]
            counts[0 if bt and wt else 1 if not bt and not wt else 2]+=1
            endpoints.append((i,v[1]))
            if bt!=wt:
                paid|=part
                (red if bt else blue).update(part)
        cycles=[]
        for first in range(len(self.arcs)):
            if first in used:continue
            j=first;part=set()
            while j not in used:
                used.add(j);part.add(j);j=nxt[j]
            assert j==first;cycles.append(part)
        assert len(used)==len(self.arcs) and not red&blue
        return dict(counts=tuple(counts),paid=paid,red=red,blue=blue,cycles=cycles,
                    cost=sum(self.arcs[j][2] for j in paid),endpoints=endpoints)

    def flow(self, colour='red', banned=frozenset(), priced=False):
        """Successive residual shortest augmentations; costs include reverse arcs."""
        graph={};refs={};S=('S',0);Z=('Z',0)
        def add(u,v,cap,cost=0):
            graph.setdefault(u,[]);graph.setdefault(v,[])
            a=[v,len(graph[v])+(u==v),cap,cost];b=[u,len(graph[u]),0,-cost]
            graph[u].append(a);graph[v].append(b);return a
        for j,(u,v,w,_) in enumerate(self.arcs):
            if j not in banned:refs[j]=add(u,v,1,w if priced else 0)
        for i,(bt,wt,_,_) in enumerate(self.paths):
            if (bt if colour=='red' else not bt):add(S,('b',i),1)
            if (not wt if colour=='red' else wt):add(('w',i),Z,1)
        graph.setdefault(S,[]);graph.setdefault(Z,[])
        value=cost=0
        while True:
            dist={S:0};prev={};todo=deque([S]);queued={S}
            while todo:
                u=todo.popleft();queued.remove(u)
                for k,a in enumerate(graph[u]):
                    v,_,cap,c=a
                    if cap and (v not in dist or dist[v]>dist[u]+c):
                        dist[v]=dist[u]+c;prev[v]=(u,k)
                        if v not in queued:todo.append(v);queued.add(v)
            if Z not in dist:break
            v=Z
            while v!=S:
                u,k=prev[v];a=graph[u][k];a[2]-=1;graph[v][a[1]][2]+=1;v=u
            value+=1;cost+=dist[Z]
        reachable={S};todo=[S]
        while todo:
            for v,_,cap,_ in graph[todo.pop()]:
                if cap and v not in reachable:reachable.add(v);todo.append(v)
        return value,{j for j,a in refs.items() if a[2]==0},cost,reachable

    def coverage(self):
        value,used,_,reach=self.flow();sw=self.switches([int(j in used) for j in range(len(self.arcs))])
        result=self.route(sw);delta=self.BT-value;assert result['counts'][0]==delta
        U={g[1] for g in self.gates if g in reach}
        cut=self.cut(U);assert cut==delta
        return dict(delta=delta,flow=value,switches=sw,cut=U,route=result)

    def cut(self,U):
        iso=sum(bt and wt and not order for bt,wt,order,_ in self.paths)
        source=sum(bt and bool(order) and order[0] in U for bt,_,order,_ in self.paths)
        sink=sum(not wt and bool(order) and order[-1] in U for _,wt,order,_ in self.paths)
        out=sum(u[0]==v[0]=='g' and u[1] in U and v[1] not in U for u,v,_,_ in self.arcs)
        return iso+source-sink-out

    def cost_model(self,red_priority=False):
        """Independent exact tiny solver for the written two-colour binary model."""
        forced=set();forbidden=set()
        for i,(bt,wt,_,_) in enumerate(self.paths):
            (forced if bt else forbidden).add(self.starts[i])
            if wt:forbidden.add(self.ends[i])
        if forced&forbidden:return None
        free=[j for j in range(len(self.arcs)) if j not in forced|forbidden]
        assert len(free)<=16,'Tiny validation solver only'
        best=None
        for bits in range(1<<len(free)):
            red=forced|{j for k,j in enumerate(free) if bits>>k&1}
            if any(sum(j in red for j in self.incoming[g])!=sum(j in red for j in self.outgoing[g]) for g in self.gates):continue
            rcost=sum(self.arcs[j][2] for j in red)
            if best is not None and rcost>(best['red_cost'] if red_priority else best['cost']):continue
            value,blue,bcost,_=self.flow('blue',red,True)
            if value!=self.WT:continue
            assert not red&blue
            total=rcost+bcost
            key=(rcost,total) if red_priority else (total,rcost)
            if best is None or key<best['key']:
                colours=[1 if j in red else 2 if j in blue else 0 for j in range(len(self.arcs))]
                sw=self.switches(colours);r=self.route(sw)
                assert r['counts'][0]==0 and r['cost']<=total
                best=dict(cost=total,red_cost=rcost,key=key,switches=sw,route=r,red=red,blue=blue)
        if best is not None:assert best['route']['cost']==best['cost']
        return best


def physical(h,w,m,n,t,gates):
    m,n,t=set(m),set(n),set(t);board=grid(h,w);d=decompose(board,m,n,t)
    assert selected_feasible(d['P'],t)
    used=set();relevant={i for g in gates for i in g['ids']}
    relevant|={i for i,p in enumerate(d['paths']) if p['kind']!='HH'}
    for g in gates:
        assert not used&g['vertices'];used|=g['vertices']
        assert g['old']<=n and not (g['old']|g['new'])&m
    rows=[];resources=[];vertices=[]
    for i in sorted(relevant):
        pv=d['paths'][i]['vertices']
        if sum(pv[0])%2:pv=pv[::-1]
        positions={edge(a,b):j for j,(a,b) in enumerate(zip(pv,pv[1:]))}
        cuts=sorted((positions[g['cut'][i]],j) for j,g in enumerate(gates) if i in g['ids'])
        assert all(p%2==0 for p,_ in cuts)
        parts=[pv[a:b+1] for a,b in zip([0]+[p+1 for p,_ in cuts],[p for p,_ in cuts]+[len(pv)-1])]
        rs=[{edge(a,b) for a,b in zip(p,p[1:]) if edge(a,b) in m} for p in parts]
        rows.append((pv[0] in t,pv[-1] in t,[j for _,j in cuts],list(map(len,rs))))
        resources+=rs;vertices+=[set(p) for p in parts]
    net=Network(rows);net.resources=resources
    assert sum(map(len,resources))==len(set().union(set(),*resources))
    assert sum(map(len,vertices))==len(set().union(set(),*vertices))
    def actual(sw):
        nn=set(n)
        for j in sw:nn=nn-gates[j]['old']|gates[j]['new']
        after=decompose(board,m,nn,t);r=net.route(sw)
        assert r['counts'][0]==after['counts'][0]
        assert r['counts'][2]==after['counts'][2]
        paid=set().union(set(),*(p['M'] for p in after['paths'] if p['kind']=='TH'))
        assert paid==set().union(set(),*(resources[j] for j in r['paid']))
        assert len(paid)==r['cost'];return after['counts'],len(paid)
    return net,actual


def specified_gates(h,w,m,n,t,squares):
    """Read only prescribed squares, avoiding an all-square search on large boards."""
    data=decompose(grid(h,w),m,n,set(t));owner={e:i for i,p in enumerate(data['paths']) for e in p['N']}
    n=set(n);gates=[]
    for r,c in squares:
        a,b,z,d=(r,c),(r,c+1),(r+1,c+1),(r+1,c)
        pair=[{edge(a,b),edge(d,z)},{edge(a,d),edge(b,z)}]
        old,new=pair if pair[0]<=n else pair[::-1]
        assert old<=n and old<=owner.keys()
        ids={owner[e] for e in old};assert len(ids)==2
        gates.append(dict(square=(r,c),old=old,new=new,ids=ids,
                          cut={owner[e]:e for e in old},vertices={a,b,z,d}))
    return gates


def greedy_family(L,d):
    """Narrow A's old width-d serpentine to width ONE; keep B and all margins."""
    h,w,_,n,t,_,bv,squares,_,_=five_family(L,d)
    c4=d+13;c5=2*d+14
    a,to=path_builder((0,0));to((c4,0));to((c4,2))
    for row in range(2,L):
        to((c4+1 if row%2==0 else c4,row));to((a[-1][0],row+1))
    to((c5,L));to((c5,0));to((c5+4,0))
    def domino(q):
        i,j=q;left=(j+4,2*i+6);right=(j+4,2*i+7)
        return (left,right) if j%2==0 else (right,left)
    av=[v for q in a for v in domino(q)]
    m={edge(p[j],p[j+1]) for p in [av,bv] for j in range(1,len(p)-1,2)}
    assert len(m)==(L+5)*d+7*L+80
    return h,w,m,n,t,[squares[j] for j in [1,2,3]]


def control(net,actual=None,exhaust=True,weighted=False):
    r=net.coverage()
    if actual:actual(r['switches'])
    if exhaust:
        rows=[net.route({g[1] for k,g in enumerate(net.gates) if b>>k&1}) for b in range(1<<len(net.gates))]
        assert min(x['counts'][0] for x in rows)==r['delta']
        assert max(net.cut({g[1] for k,g in enumerate(net.gates) if b>>k&1}) for b in range(1<<len(net.gates)))==r['delta']
        if weighted:
            costs=[x['cost'] for x in rows if x['counts'][0]==0]
            opt=net.cost_model();assert (opt is None)==(not costs)
            if opt is not None:
                assert opt['cost']==min(costs)
                if actual:actual(opt['switches'])
    return r


def main():
    rng=random.Random(271027);abstract=weighted=0
    for case in range(360):
        n=rng.randrange(2,7);e=rng.randrange(0,8);orders=[[] for _ in range(n)]
        for j in range(e):
            for i in rng.sample(range(n),2):orders[i].append(j)
        rows=[]
        for order in orders:
            rng.shuffle(order);rows.append((bool(rng.randrange(2)),bool(rng.randrange(2)),order,[rng.randrange(10) for _ in range(len(order)+1)]))
        use=e<=4;control(Network(rows),weighted=use);abstract+=1;weighted+=use
    physical_cases=0;physical_exhaust=0
    for h,w in [(4,4),(4,6),(4,8),(6,4),(6,6),(6,8)]:
        for selection in ['TT','TH']:
            m,n,t,allg=row_family(h,w,selection)
            for _ in range(8):
                pool=[];seen=set();candidates=list(allg);rng.shuffle(candidates)
                for g in candidates:
                    if not seen&g['vertices'] and len(pool)<5 and rng.random()<.7:
                        pool.append(g);seen|=g['vertices']
                net,actual=physical(h,w,m,n,t,pool);control(net,actual,weighted=True)
                # Physical surgery for EVERY subset, separately from compressed routing.
                for bits in range(1<<len(pool)):
                    actual({j for j in range(len(pool)) if bits>>j&1});physical_exhaust+=1
                physical_cases+=1
    stars=star_subsets=0
    for k in range(1,6):
        for word in product('HT',repeat=k):
            d=star_family(''.join(word));h,w=d['h'],d['w'];m,n,t=d['M'],d['N'],d['T']
            before=decompose(grid(h,w),m,n,t);by={g['square']:g for g in all_gates(h,w,n,before)}
            net,actual=physical(h,w,m,n,t,[by[s] for s in d['squares']])
            control(net,actual,weighted=k<=3)
            for bits in range(1<<k):actual({j for j in range(k) if bits>>j&1});star_subsets+=1
            stars+=1
    long_stars=[]
    for s in range(1,25):
        for good,word in [(True,'HT'*s),(False,'H'*s+'T'*s)]:
            d=star_family(word);h,w=d['h'],d['w'];m,n,t=d['M'],d['N'],d['T']
            before=decompose(grid(h,w),m,n,t);by={g['square']:g for g in all_gates(h,w,n,before)}
            net,actual=physical(h,w,m,n,t,[by[z] for z in d['squares']])
            r=control(net,actual,False);assert r['delta']==(0 if good else s-1)
            if not good:
                U={j for j,c in enumerate(word) if c=='T'};assert net.cut(U)==s-1
            long_stars.append(dict(s=s,alternating=good,delta=r['delta'],flow=r['flow']))
    fixtures=[]
    for f in [same_order_witness(),wrong_order_control()]:
        h,w=f.get('h',f.get('height')),f.get('w',f.get('width'));m,n,t=f['M'],f['N'],set(f['T'])
        squares=f.get('squares',f.get('witness_squares'));before=decompose(grid(h,w),m,n,t)
        pool=[g for g in all_gates(h,w,n,before) if g['square'] in squares]
        net,actual=physical(h,w,m,n,t,pool);r=control(net,actual,weighted=True)
        fixtures.append(dict(board=[h,w],minimum_TT=r['delta'],flow=r['flow'],cut=sorted(r['cut'])))
    five=[]
    for L,d in [(12,12),(20,11),(20,20)]:
        h,w,m,n,t,_,_,squares,_,_=five_family(L,d);before=decompose(grid(h,w),m,n,t)
        by={g['square']:g for g in all_gates(h,w,n,before)}
        net,actual=physical(h,w,m,n,t,[by[s] for s in squares]);control(net,actual,weighted=True)
        opt=net.cost_model();assert opt['switches']==set(range(5));assert opt['cost']==2*L+3*d+78
        five.append(dict(L=L,d=d,cost=opt['cost'],contacts=sorted(opt['switches'])))
    shortcuts=[]
    for W in range(4,42,2):
        m,n,t,gates=row_family(4,W);pool=[g for g in gates if g['square'] in [(1,0),(1,W-2)]]
        net,actual=physical(4,W,m,n,t,pool);opt=net.cost_model();assert opt['cost']==0
        single=[(j,net.route({j})) for j in range(2)]
        j,r=next((j,r) for j,r in single if sum(net.arcs[a][2] for a in r['red'])==0)
        assert r['cost']==W-2;actual({j});actual(opt['switches'])
        shortcuts.append(dict(W=W,red_cost=0,decoded_total=r['cost'],joint_optimum=0,
                              zero_red_single_square=pool[j]['square']))
    greedy=[]
    for L in [4,6,8,12,20,40]:
        d=L;h,w,m,n,t,squares=greedy_family(L,d)
        pool=specified_gates(h,w,m,n,t,squares)
        assert all(g['vertices']<={v for e in m for v in e} for g in pool)
        net,actual=physical(h,w,m,n,t,pool);control(net,actual,weighted=True)
        joint=net.cost_model();lex=net.cost_model(True)
        assert joint['cost']==5*d+5*L+78 and joint['switches']=={0,1}
        assert lex['cost']==len(m) and lex['red_cost']==2*d+42 and lex['switches']=={2}
        actual(joint['switches']);actual(lex['switches'])
        for bits in range(8):actual({j for j in range(3) if bits>>j&1})
        greedy.append(dict(L=L,d=d,board=[h,w],M=len(m),all_contacts_internal=True,
            joint_cost=joint['cost'],joint_red_cost=joint['red_cost'],joint_contacts=sorted(joint['switches']),
            red_first_then_optimal_blue=lex['cost'],minimum_red_cost=lex['red_cost'],greedy_contacts=sorted(lex['switches'])))
    out=dict(status='PASS',abstract_networks=abstract,abstract_weighted_models=weighted,
        actual_row_pools=physical_cases,actual_row_subset_surgeries=physical_exhaust,
        actual_short_stars=stars,actual_star_subset_surgeries=star_subsets,
        actual_long_star_families=long_stars,fixtures=fixtures,
        five_contact_weighted_models=five,one_colour_shortcut=shortcuts,three_contact_greedy_barrier=greedy,
        scope='General maximum-flow/TT and complete cut identities, plus exact two-colour integer-cost equivalence, proved in note. Tiny independent red-variable enumeration plus blue min-cost flow checks cost model against contact-subset enumeration. Physical controls reconstruct actual N and unique M resources. No universal grid coverage, weighted polynomial-time claim, LP integrality, or end-to-end Lean.')
    (ROOT/'output/contact-flow-cut.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['actual_long_star_families','one_colour_shortcut','scope']}))


if __name__=='__main__':main()
