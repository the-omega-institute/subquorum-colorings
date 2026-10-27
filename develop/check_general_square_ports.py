"""Physical-port adapter allowing same-path cuts, original cycles and retention.

All-size proofs are in GENERAL_SQUARE_PORTS_AND_TILE_CUTS.md. This verifier
compares the generalized flow model with actual matching surgery, retaining
parallel arcs, self loops, zero-M fragments and doubled matching components.
"""
from itertools import product
from collections import deque
from pathlib import Path
import json
import random

from check_contact_flow_cut import Network
from check_mixed_terminal_compensation import (
    all_matchings, decompose, edge, grid, mates, neighbours, selected_feasible,
)
from check_unique_matching_hole_barrier import family as unique_matching_family

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')
ROOT=Path(__file__).resolve().parents[1]


def all_squares(h,w,n):
    n=set(n);result=[]
    for r in range(h-1):
        for c in range(w-1):
            a,b,z,d=(r,c),(r,c+1),(r+1,c+1),(r+1,c)
            pairs=[{edge(a,b),edge(d,z)},{edge(a,d),edge(b,z)}]
            if pairs[0]<=n:old,new=pairs
            elif pairs[1]<=n:new,old=pairs
            else:continue
            result.append(dict(square=(r,c),old=old,new=new,vertices={a,b,z,d}))
    return result


def independent_pools(gates):
    for bits in range(1<<len(gates)):
        found=[];vertices=set()
        for j,g in enumerate(gates):
            if not bits>>j&1:continue
            if vertices&g['vertices']:break
            vertices|=g['vertices'];found.append(g)
        else:yield found


def physical_state(board,m,n,t):
    d=decompose(board,m,n,t);mm=mates(board,m);nm=mates(board,n,full=True)
    unseen=set(d['remainder']);cycles=[]
    while unseen:
        start=min(v for v in unseen if sum(v)%2==0);v=start;vs=set();rs=set()
        while True:
            assert v not in vs;vs.add(v);w=nm[v];assert w not in vs;vs.add(w)
            z=mm[w];rs.add(edge(w,z));v=z
            if v==start:break
        assert vs<=unseen;unseen-=vs;cycles.append((frozenset(vs),frozenset(rs)))
    paid=set().union(set(),*(p['M'] for p in d['paths'] if p['kind']=='TH'))
    bad=set().union(set(),*(p['M'] for p in d['paths'] if p['kind']!='TH'))
    free=set().union(set(),*(rs for _,rs in cycles))
    assert not paid&bad and not paid&free and not bad&free and paid|bad|free==set(m)
    return dict(data=d,cycles=cycles,paid=paid,bad=bad,free=free)


class PortNetwork(Network):
    def __init__(self,h,w,m,n,t,gates):
        self.board=grid(h,w);self.m=set(m);self.n=set(n);self.t=set(t);self.pool=gates
        mm=mates(self.board,m);nm=mates(self.board,n,full=True);q=self.board-mm.keys()
        assert selected_feasible(set(mm),self.t)
        self.old=physical_state(self.board,self.m,self.n,self.t)
        oldpaths=self.old['data']['paths'];self.paths=[];black={};white={}
        for i,p in enumerate(oldpaths):
            pv=p['vertices']
            if sum(pv[0])%2:pv=pv[::-1]
            black[pv[0]]=i;white[pv[-1]]=i
            self.paths.append((pv[0] in t,pv[-1] in t,[],[]))
        self.starts=[None]*len(self.paths);self.ends=[None]*len(self.paths)
        self.BT=sum(p[0] for p in self.paths);self.WT=sum(p[1] for p in self.paths)
        cutblack={};cutwhite={};seen=set()
        for j,g in enumerate(gates):
            assert g['old']<=self.n and not seen&g['vertices'];seen|=g['vertices']
            cuts=[]
            for e in g['old']:
                a,b=e
                if sum(a)%2:a,b=b,a
                cuts.append((a,b))
            cuts.sort()
            for p,(a,b) in enumerate(cuts):cutblack[a]=(j,p);cutwhite[b]=(j,p)
        self.arcs=[];self.resources=[];self.vertices=[];self.incoming={};self.outgoing={}
        self.inport={};self.outport={}
        sources=[(v,('b',i),None) for v,i in sorted(black.items())]
        sources += [(v,('g',g),p) for v,(g,p) in sorted(cutwhite.items(),key=lambda x:x[1])]
        for start,tail,port in sources:
            v=start;vs={v};rs=set()
            while True:
                if sum(v)%2==0:
                    if v in cutblack:
                        j,p=cutblack[v];head=('g',j);endport=p;break
                    z=nm[v]
                else:
                    if v in q:
                        head=('w',white[v]);endport=None;break
                    z=mm[v];rs.add(edge(v,z))
                assert z not in vs;vs.add(z);v=z
            k=len(self.arcs);self.arcs.append((tail,head,len(rs),k));self.resources.append(rs);self.vertices.append(vs)
            self.outgoing.setdefault(tail,[]).append(k);self.incoming.setdefault(head,[]).append(k)
            if tail[0]=='b':self.starts[tail[1]]=k
            else:self.outport[tail[1],port]=k
            if head[0]=='w':self.ends[head[1]]=k
            else:self.inport[head[1],endport]=k
        self.gates=[('g',j) for j in range(len(gates))]
        assert len(self.arcs)==len(self.paths)+2*len(gates)
        for g in self.gates:
            assert len(self.incoming[g])==len(self.outgoing[g])==2
            assert all((g[1],p) in self.inport and (g[1],p) in self.outport for p in [0,1])
        assert None not in self.starts and None not in self.ends
        assert sum(map(len,self.vertices))==len(set().union(set(),*self.vertices))
        assert sum(map(len,self.resources))==len(set().union(set(),*self.resources))
        self.covered=set().union(set(),*self.vertices)
        remaining=self.board-self.covered
        assert remaining<=mm.keys() and all(mm[v] in remaining and nm[v] in remaining for v in remaining)
        self.untouched=[(vs,rs) for vs,rs in self.old['cycles'] if vs<=remaining]

    def switches(self,colours):
        result=set()
        for _,g in self.gates:
            a,b=[colours[self.inport[g,p]] for p in [0,1]]
            c,d=[colours[self.outport[g,p]] for p in [0,1]]
            if (a,b)==(c,d):continue
            assert (a,b)==(d,c);result.add(g)
        return result

    def route(self,switches):
        nxt={self.inport[g,p]:self.outport[g,1-p if g in switches else p]
             for _,g in self.gates for p in [0,1]}
        used=set();counts=[0,0,0];paid=set();red=set();blue=set();endpoints=[];paths=[]
        for i,start in enumerate(self.starts):
            j=start;part=set()
            while True:
                assert j not in used;used.add(j);part.add(j);v=self.arcs[j][1]
                if v[0]=='w':break
                j=nxt[j]
            bt=self.paths[i][0];wt=self.paths[v[1]][1]
            kind='TT' if bt and wt else 'HH' if not bt and not wt else 'TH'
            counts[['TT','HH','TH'].index(kind)]+=1;endpoints.append((i,v[1]))
            paths.append((part,kind))
            if bt!=wt:paid|=part;(red if bt else blue).update(part)
        cycles=[]
        for first in range(len(self.arcs)):
            if first in used:continue
            j=first;part=set()
            while j not in used:used.add(j);part.add(j);j=nxt[j]
            assert j==first;cycles.append(part)
        assert len(used)==len(self.arcs) and not red&blue
        return dict(counts=tuple(counts),paid=paid,red=red,blue=blue,cycles=cycles,paths=paths,
                    cost=sum(self.arcs[j][2] for j in paid),endpoints=endpoints)

    def cut(self,U):
        def inside(v):
            kind,i=v
            if kind=='g':return i in U
            return self.paths[i][0] if kind=='b' else self.paths[i][1]
        return self.BT-sum(inside(u) and not inside(v) for u,v,_,_ in self.arcs)

    def actual(self,switches):
        nn=set(self.n)
        for j in switches:nn=nn-self.pool[j]['old']|self.pool[j]['new']
        state=physical_state(self.board,self.m,nn,self.t);r=self.route(switches)
        assert r['counts']==state['data']['counts']
        def component(part):
            return (frozenset().union(*(self.vertices[j] for j in part)),
                    frozenset().union(*(self.resources[j] for j in part)))
        predicted={(component(part),kind) for part,kind in r['paths']}
        actual={((frozenset(p['vertices']),frozenset(p['M'])),p['kind']) for p in state['data']['paths']}
        assert predicted==actual
        assert set(component(c) for c in r['cycles'])|set(self.untouched)==set(state['cycles'])
        paid=set().union(set(),*(self.resources[j] for j in r['paid']))
        assert paid==state['paid'] and len(paid)==r['cost']
        assert len(state['paid'])-len(self.old['paid'])==(
            len(self.old['bad'])-len(state['bad'])+len(self.old['free'])-len(state['free']))
        # Normalize ALL free cycles, including doubled and pre-existing ones.
        remainder=state['data']['remainder']
        normalized={e for e in nn if not set(e)<=remainder}|state['free']
        normal=physical_state(self.board,self.m,normalized,self.t)
        assert normal['data']['counts']==state['data']['counts'] and normal['paid']==state['paid']
        assert self.m&normalized==state['free']
        return state


def tiled_auxiliary(h,w,vertical=frozenset()):
    assert h%2==w%2==0
    n=set();squares=[]
    for r in range(0,h,2):
        for c in range(0,w,2):
            squares.append((r,c));a,b,z,d=(r,c),(r,c+1),(r+1,c+1),(r+1,c)
            n|={edge(a,d),edge(b,z)} if (r,c) in vertical else {edge(a,b),edge(d,z)}
    return n,squares


def debt_compensation(ids,cross_edges,defect,reserve):
    """Independent integral flow with ONE undirected capacity per actual M edge.

    Symmetric initial residual capacities encode net flow in [-1,1], not two
    separately reusable payments. Parallel physical edges retain multiplicity.
    """
    S,Z=('source',),('sink',);res={v:{} for v in [S,Z]+ids}
    def add(u,v,capacity):
        res[u][v]=res[u].get(v,0)+capacity;res[v].setdefault(u,0)
    for u,v in cross_edges:add(u,v,1);add(v,u,1)
    for v in ids:
        add(S,v,defect[v]);add(v,Z,reserve[v])
    value=0
    while True:
        prev={S:None};todo=deque([S])
        while todo and Z not in prev:
            u=todo.popleft()
            for v,capacity in res[u].items():
                if capacity>0 and v not in prev:prev[v]=u;todo.append(v)
        if Z not in prev:break
        v=Z
        while v!=S:
            u=prev[v];res[u][v]-=1;res[v][u]+=1;v=u
        value+=1
    reached={S};todo=[S]
    while todo:
        for v,capacity in res[todo.pop()].items():
            if capacity>0 and v not in reached:reached.add(v);todo.append(v)
    U=set(ids)&reached
    boundary=sum((u in U)!=(v in U) for u,v in cross_edges)
    shortage=sum(defect[v]-reserve[v] for v in U)-boundary
    assert shortage==sum(defect.values())-value
    return dict(value=value,uncompensated=shortage,cut=sorted(U))


def tile_control(h,w,m,t,enumerate_phases=True,weighted=False):
    n,squares=tiled_auxiliary(h,w);by={g['square']:g for g in all_squares(h,w,n)}
    net=PortNetwork(h,w,m,n,t,[by[s] for s in squares]);r=net.coverage();net.actual(r['switches'])
    tile={v:(v[0]//2,v[1]//2) for v in net.board};ids=[(r//2,c//2) for r,c in squares]
    maximum=0;bestU=[]
    slack={i:2-len(set(t)&{v for v in net.board if tile[v]==i})-
           sum(all(tile[v]==i for v in e) for e in m) for i in ids}
    p={v for e in m for v in e}
    charge={i:4-2*sum(v in t for v in net.board if tile[v]==i)-
            sum(v in p for v in net.board if tile[v]==i) for i in ids}
    assert min(charge.values())>=-1
    defect={i:int(charge[i]==-1) for i in ids}
    reserve={i:max(0,charge[i]) for i in ids}
    cross_edges=[(tile[a],tile[b]) for a,b in m if tile[a]!=tile[b]]
    compensation=debt_compensation(ids,cross_edges,defect,reserve)
    assert min(slack.values())>=0
    for bits in range(1<<len(squares)):
        U={ids[j] for j in range(len(ids)) if bits>>j&1};region={v for v in net.board if tile[v] in U}
        excess=len(set(t)&region)+sum(set(e)<=region for e in m)-2*len(U)
        assert excess==net.cut({j for j,i in enumerate(ids) if i in U})
        crossing=sum(set(e)<=region and tile[e[0]]!=tile[e[1]] for e in m)
        assert excess==crossing-sum(slack[i] for i in U)
        boundary=sum((a in U)!=(b in U) for a,b in cross_edges)
        assert 2*excess==sum(defect[i]-reserve[i] for i in U)-boundary
        if excess>maximum:maximum=excess;bestU=sorted(U)
    assert maximum==r['delta']
    assert compensation['uncompensated']==2*maximum
    if not any(defect.values()):assert maximum==0
    rows=[]
    if enumerate_phases:
        for bits in range(1<<len(squares)):
            sw={j for j in range(len(squares)) if bits>>j&1};state=net.actual(sw);old=net.route(sw)
            normalized=set(sw)
            for j,g in enumerate(net.pool):
                internal={e for e in m if set(e)<=g['vertices']}
                if not internal:continue
                if internal<=g['old']:normalized.discard(j)
                else:assert internal<=g['new'];normalized.add(j)
            newstate=net.actual(normalized);new=net.route(normalized)
            assert old['endpoints']==new['endpoints'] and newstate['paid']<=state['paid']
            nn=set(n)
            for j in normalized:nn=nn-net.pool[j]['old']|net.pool[j]['new']
            internal={e for e in m if tile[e[0]]==tile[e[1]]}
            assert set(m)&nn==internal
            rows.append(old)
        assert min(x['counts'][0] for x in rows)==maximum
    if weighted:
        opt=net.cost_model();costs=[x['cost'] for x in rows if not x['counts'][0]]
        assert (opt is None)==(not costs)
        if opt is not None:assert opt['cost']==min(costs);net.actual(opt['switches'])
    return dict(delta=maximum,cut_tiles=bestU,flow=r['flow'],normalization_states=len(rows),
                debt_compensation=compensation,debt_tiles=sum(defect.values()))


def cycle_relay_family(H):
    """A genuine old P-only cycle is the ONLY original neighbour of the TT path."""
    assert H>=2 and H%2==0
    h,w=H+2,6
    m={edge((0,1),(0,2)),edge((0,3),(0,4))}
    m|={edge((r,c),(r+1,c)) for c in [2,3] for r in range(1,H,2)}
    n={edge((r,c),(r,c+1)) for r in [0,H+1] for c in [0,2,4]}
    n|={edge((1,2),(1,3)),edge((H,2),(H,3))}
    n|={edge((r,c),(r+1,c)) for c in [2,3] for r in range(2,H-1,2)}
    n|={edge((r,c),(r+1,c)) for c in [0,1,4,5] for r in range(1,H,2)}
    t={(0,0),(0,5)}
    return h,w,m,n,t


def cycle_relay_control(H):
    h,w,m,n,t=cycle_relay_family(H);state=physical_state(grid(h,w),m,n,t)
    assert state['data']['counts']==(1,2*H+3,0)
    assert len(state['cycles'])==1 and len(state['free'])==H and len(state['bad'])==2
    assert not m&n
    candidates=all_squares(h,w,n)
    ttN={e for p in state['data']['paths'] if p['kind']=='TT' for e in p['N']}
    hhN={e for p in state['data']['paths'] if p['kind']=='HH' for e in p['N']}
    assert not any(g['old']&ttN and g['old']&hhN for g in candidates)
    by={g['square']:g for g in candidates};pool=[by[(0,2)],by[(H,2)]]
    assert all(g['vertices']<={v for e in m for v in e} for g in pool[:1])
    net=PortNetwork(h,w,m,n,t,pool);r=net.coverage();assert r['delta']==0 and r['switches']=={0,1}
    for sw in [set(),{0},{1},{0,1}]:
        actual=net.actual(sw)
        assert actual['data']['counts'][0]==(0 if len(sw)==2 else 1)
    opt=net.cost_model();assert opt['switches']=={0,1} and opt['cost']==H+2
    assert net.route({0,1})['counts']==(0,2*H+2,2)
    # Complete unrestricted zero-M payments, outside the prescribed two-contact class.
    for u in t:assert (1,u[1]) in state['data']['H'] and (1,u[1]) in neighbours(u)
    return dict(H=H,board=[h,w],M=len(m),old_bad_M=2,old_cycle_M=H,
        new_paid_M=opt['cost'],new_cycle_M=0,contacts=[g['square'] for g in pool],
        initially_no_TH=True,initially_no_direct_TT_HH_square=True,
        unique_covering_subset=[0,1],unrestricted_adjacent_payment_M=0)


def local_tile_controls():
    vs=[(0,0),(0,1),(1,1),(1,0)];count=debt=0
    for labels in product('HTP',repeat=4):
        p={v for v,s in zip(vs,labels) if s=='P'};t={v for v,s in zip(vs,labels) if s=='T'}
        if not selected_feasible(p,t):continue
        for m in all_matchings(set(vs),partial=True):
            if not {v for e in m for v in e}<=p:continue
            s=2-len(t)-len(m);external=len(p)-2*len(m)
            d=int(len(t)==2 and len(p)==1)
            assert s>=0 and external<=2*s+d
            if d:
                assert len(m)==0 and external==1
                assert sorted(vs.index(v) for v in t) in [[0,2],[1,3]]
            debt+=d;count+=1
    return dict(supported_feasible_local_patterns=count,debt_patterns=debt,
                complete_label_matching_space=3**4*7)


def small_controls(h,w):
    board=grid(h,w);aux=list(all_matchings(board));models=subsets=costs=0;special={k:0 for k in ['retention_removed','retention_added','same_original_component','old_cycle_contact']}
    for matching in all_matchings(board,partial=True):
        m=set(matching);p={v for e in m for v in e};q=sorted(board-p)
        for mask in range(1<<len(q)):
            t={v for i,v in enumerate(q) if mask>>i&1}
            if not selected_feasible(p,t):continue
            for n in aux:
                n=set(n);old=physical_state(board,m,n,t)
                owner={e:('p',i) for i,path in enumerate(old['data']['paths']) for e in path['N']}
                for i,(vs,_) in enumerate(old['cycles']):
                    for e in n:
                        if set(e)<=vs:owner[e]=('c',i)
                for pool in independent_pools(all_squares(h,w,n)):
                    net=PortNetwork(h,w,m,n,t,pool);r=net.coverage();net.actual(r['switches']);rows=[]
                    for bits in range(1<<len(pool)):
                        sw={j for j in range(len(pool)) if bits>>j&1};state=net.actual(sw);rows.append(net.route(sw));subsets+=1
                        newn=set(n)
                        for j in sw:newn=newn-pool[j]['old']|pool[j]['new']
                        special['retention_removed']+=bool((m&n)-newn)
                        special['retention_added']+=bool((m&newn)-n)
                    assert min(x['counts'][0] for x in rows)==r['delta']
                    assert max(net.cut({j for j in range(len(pool)) if bits>>j&1}) for bits in range(1<<len(pool)))==r['delta']
                    opt=net.cost_model();feasible=[x['cost'] for x in rows if not x['counts'][0]]
                    assert (opt is None)==(not feasible)
                    if opt is not None:assert opt['cost']==min(feasible);net.actual(opt['switches']);costs+=1
                    for g in pool:
                        ids=[owner[e] for e in g['old']]
                        special['same_original_component']+=ids[0]==ids[1]
                        special['old_cycle_contact']+=any(kind=='c' for kind,_ in ids)
                    models+=1
    return dict(board=[h,w],physical_models=models,actual_subset_surgeries=subsets,feasible_weighted_models=costs,case_coverage=special)


def small_tile_controls(h,w):
    """All feasible actual M,T; fixed tiling, all phases and both exact flows."""
    board=grid(h,w);models=debt_models=states=0
    for matching in all_matchings(board,partial=True):
        m=set(matching);p={v for e in m for v in e};q=sorted(board-p)
        for bits in range(1<<len(q)):
            t={v for j,v in enumerate(q) if bits>>j&1}
            if not selected_feasible(p,t):continue
            r=tile_control(h,w,m,t,weighted=True)
            models+=1;debt_models+=r['debt_tiles']>0;states+=r['normalization_states']
    return dict(board=[h,w],models=models,models_with_debt=debt_models,
                normalization_states=states)


def closed_tile_chain_control(w):
    """Old actual family, NEW all-product-phase obstruction via exact debt cut."""
    p,m,t,holes,pairs=unique_matching_family(w);m=set(m);n,squares=tiled_auxiliary(4,w)
    by={g['square']:g for g in all_squares(4,w,n)}
    net=PortNetwork(4,w,m,n,t,[by[s] for s in squares]);r=net.coverage();net.actual(r['switches'])
    ids=[(a//2,b//2) for a,b in squares];tile=lambda v:(v[0]//2,v[1]//2)
    U={(0,j) for j in range(w//2)}|{(1,0),(1,w//2-1)}
    region={v for v in net.board if tile(v) in U}
    charge={i:4-2*sum(v in t for v in net.board if tile(v)==i)-
            sum(v in p for v in net.board if tile(v)==i) for i in ids}
    defects={i:int(charge[i]==-1) for i in ids};reserve={i:max(0,charge[i]) for i in ids}
    cross=[(tile(a),tile(b)) for a,b in m if tile(a)!=tile(b)]
    debt=debt_compensation(ids,cross,defects,reserve)
    assert r['delta']==1 and r['route']['counts']==(1,2,w-2)
    assert sum(defects.values())==2 and debt['value']==0 and debt['uncompensated']==2
    assert all(charge[i]==0 for i in U if i[0]==0)
    assert all(charge[i]==-1 for i in U if i[0]==1)
    assert all(charge[i]>=0 for i in set(ids)-U)
    assert {tile(v) for v in p}==U
    assert len(set(t)&region)==6 and len(U)==w//2+2
    assert len(t&region)+sum(set(e)<=region for e in m)-2*len(U)==1
    assert all(a in U and b in U for a,b in cross)
    trace=[(1,0)]+[(0,j) for j in range(w//2)]+[(1,w//2-1)]
    assert {frozenset(e) for e in cross}=={frozenset(e) for e in zip(trace,trace[1:])}
    assert len(cross)==len(trace)-1
    partners={u:v for a,b in pairs for u,v in [(a,b),(b,a)]}
    image={partners[v] for v in t}
    assert len(image)==len(t) and not image&(p|t)
    assert all(partners[v] in neighbours(v) for v in t)
    # The adjacent-hole certificate extends to an actual FULL auxiliary N.
    # Keep top/side actual edges, route the two unused holes through row one.
    completion={e for e in m if not all(v[0]==1 for v in e)}
    completion|={edge(v,partners[v]) for v in t}
    completion|={edge((2,c),(1,c)) for c in [2,w-3]}
    completion|={edge((1,c),(1,c+1)) for c in range(3,w-4,2)}
    unrestricted=physical_state(grid(4,w),m,completion,t)
    assert unrestricted['data']['counts']==(0,1,w) and not unrestricted['paid']
    if w<=10:assert tile_control(4,w,m,t)['delta']==1
    return dict(width=w,debt=2,debt_flow=0,minimum_residual_TT=1,
                optimal_counts=[1,2,w-2],closed_cut_tiles=len(U),cut_T=6,cut_M=w-1,
                regional_excess=1,unrestricted_adjacent_payment_M=0,
                provenance='Actual M,T from existing unique_matching_hole_barrier; all-product-phase optimum is the new deduction.')


def column_strip_obstruction_controls():
    """All five local domino states, plus every maximal independent square pool.

    The all-size proof is the forced two-top-port connection in each strip,
    not the following finite state products or pool enumeration.
    """
    local=list(all_matchings(grid(4,2)));assert len(local)==5
    auxiliary_models=0;maximal_pools=0;counts=[]
    for w in [6,8,10]:
        _,m,t,_,_=unique_matching_family(w);minimum=99;models=0
        for choices in product(range(5),repeat=w//2):
            n={edge((a[0],a[1]+2*j),(b[0],b[1]+2*j))
               for j,k in enumerate(choices) for a,b in local[k]}
            state=physical_state(grid(4,w),m,n,t)
            assert state['data']['counts'][0]>=1
            minimum=min(minimum,state['data']['counts'][0]);models+=1
        assert minimum==1 and models==5**(w//2)
        auxiliary_models+=models;counts.append(dict(width=w,auxiliary_models=models,minimum_TT=minimum))
    for w in [6,8,10,12,14,16]:
        _,m,t,_,_=unique_matching_family(w);n,_=tiled_auxiliary(4,w)
        by={g['square']:g for g in all_squares(4,w,n)}
        assert set(by)=={(r,c) for r in range(3) for c in range(0,w,2)}
        for bits in range(1<<(w//2)):
            coords=[(r,2*j) for j in range(w//2) for r in ([1] if bits>>j&1 else [0,2])]
            net=PortNetwork(4,w,m,n,t,[by[x] for x in coords]);r=net.coverage()
            net.actual(r['switches']);assert r['delta']==1
            maximal_pools+=1
    return dict(local_domino_states=5,all_column_strip_auxiliaries=auxiliary_models,
                exact_width_controls=counts,maximal_independent_pools=maximal_pools,
                all_pool_minimum_TT=1,
                scope='Finite controls for written ALL-W no-column-crossing-N obstruction, hence ANY single independent square batch from all-horizontal N fails; unrestricted full N succeeds.')


def two_batch_repair_control(w):
    """Exact batch depth TWO; never add intermediate cycle credit twice."""
    _,m,t,_,_=unique_matching_family(w);m=set(m);n0,_=tiled_auxiliary(4,w)
    first=[(r,c) for r in [0,2] for c in range(0,w,2)]
    second=[(r,c) for r in [0,2] for c in range(1,w-1,2)]
    states=[physical_state(grid(4,w),m,n0,t)]
    n=n0
    for coords in [first,second]:
        by={g['square']:g for g in all_squares(4,w,n)}
        net=PortNetwork(4,w,m,n,t,[by[x] for x in coords])
        states.append(net.actual(set(range(len(coords)))))
        for square in coords:
            g=by[square];n=n-g['old']|g['new']
    assert [s['data']['counts'] for s in states]==[(1,2,w-2),(1,2,w-2),(0,1,w)]
    assert [len(s['paid']) for s in states]==[2,0,0]
    assert len(states[0]['bad'])==w//2-1 and len(states[0]['free'])==w//2-2
    assert len(states[1]['bad'])==w-1 and not states[1]['free']
    assert len(states[2]['bad'])==w//2 and len(states[2]['free'])==w//2-1
    top={e for e in m if all(v[0]==0 for v in e)}
    mid={e for e in m if all(v[0]==1 for v in e)}
    side=m-top-mid
    assert states[0]['paid']==side and states[0]['bad']==top and states[0]['free']==mid
    assert not states[1]['paid'] and states[1]['bad']==m and not states[1]['free']
    assert not states[2]['paid'] and states[2]['bad']==mid|side and states[2]['free']==top
    assert all(len(p['vertices'])==2 for p in states[2]['data']['paths'] if p['kind']=='TH')
    assert len(first)==w and len(second)==w-2
    return dict(width=w,minimum_independent_batches=2,
                flip_counts=[w,w-2],counts=[list(s['data']['counts']) for s in states],
                paid_M=[len(s['paid']) for s in states],
                final_T_paths_are_direct_hole_payments=True,
                scope='Upper bound is explicit; lower bound is the written all-independent-pools theorem, not finite extrapolation. Fixed actual M,T; final ledger evaluated once.')


def main():
    small=[small_controls(2,2),small_controls(2,4)]
    small_tiles=[small_tile_controls(2,2),small_tile_controls(2,4)]
    # A feasible TH path absorbs a previously retained M edge: old bad M=0.
    m={edge((0,0),(1,0))};n={edge((0,c),(1,c)) for c in range(2)};t={(0,1)}
    net=PortNetwork(2,2,m,n,t,all_squares(2,2,n));after=net.actual({0})
    assert len(net.old['paid'])==0 and len(net.old['bad'])==0 and len(net.old['free'])==1
    assert len(after['paid'])==1 and len(after['bad'])==len(after['free'])==0
    old_circle=dict(board=[2,2],M=sorted(m),N=sorted(n),T=sorted(t),old_counts=net.old['data']['counts'],new_counts=after['data']['counts'],old_paid=0,new_paid=1,old_bad_M=0,old_free_M=1,new_free_M=0)
    rng=random.Random(102727);random_cases=0;random_surgeries=0;tile_rows=[]
    for case in range(140):
        h,w=4,(4 if case<100 else 6);board=grid(h,w);m=set();p=set()
        edges=list({edge(v,z) for v in board for z in neighbours(v)&board});rng.shuffle(edges)
        for e in edges:
            if not set(e)&p and rng.random()<.42:m.add(e);p.update(e)
        q=list(board-p);rng.shuffle(q);t=set()
        for v in q:
            if rng.random()<.8 and selected_feasible(p,t|{v}):t.add(v)
        n,_=tiled_auxiliary(h,w)
        for _ in range(12):
            candidates=all_squares(h,w,n)
            if candidates:
                g=rng.choice(candidates);n=n-g['old']|g['new']
        candidates=all_squares(h,w,n);rng.shuffle(candidates);pool=[];seen=set()
        for g in candidates:
            if not seen&g['vertices'] and len(pool)<5:pool.append(g);seen|=g['vertices']
        net=PortNetwork(h,w,m,n,t,pool);r=net.coverage();net.actual(r['switches']);rows=[]
        for bits in range(1<<len(pool)):
            sw={j for j in range(len(pool)) if bits>>j&1};net.actual(sw);rows.append(net.route(sw));random_surgeries+=1
        assert min(x['counts'][0] for x in rows)==r['delta']
        tile_rows.append(tile_control(h,w,m,t,weighted=case<40));random_cases+=1
    relays=[cycle_relay_control(H) for H in range(2,82,2)]
    closed_chains=[closed_tile_chain_control(w) for w in range(6,106,2)]
    strip_obstructions=column_strip_obstruction_controls()
    two_batches=[two_batch_repair_control(w) for w in range(6,106,2)]
    out=dict(status='PASS',exhaustive_small=small,random_actual_models=random_cases,
        exhaustive_product_tiles=small_tiles,
        random_actual_subset_surgeries=random_surgeries,product_tile_models=len(tile_rows),
        product_tile_normalization_states=sum(x['normalization_states'] for x in tile_rows),
        exact_debt_flow_models=len(tile_rows),
        debt_flow_models_with_debt=sum(x['debt_tiles']>0 for x in tile_rows),
        local_tile_classification=local_tile_controls(),cycle_relay_family_controls=relays,
        closed_tile_chain_controls=closed_chains,
        column_strip_obstruction=strip_obstructions,
        two_batch_repair_controls=two_batches,
        positive_regional_cut_examples=[x for x in tile_rows if x['delta']>0],
        old_cycle_payment_witness=old_circle,
        scope='General port/flow/cost theorem, old-circle signed ledger, geometric product-tile cut identity and all-internal-M retention normalization are written proofs. Finite actual controls validate, not prove, arbitrary-size statements. No universal half-area or5/6 improvement.')
    (ROOT/'output/general-square-ports.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(out))


if __name__=='__main__':main()
