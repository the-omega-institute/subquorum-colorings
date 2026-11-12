#!/usr/bin/env python3
"""Exact integer base certificates and controls for the cyclic regular family.
Requires numpy. SciPy/MILP is neither imported nor needed. Assertions are required.
The infinite-family conclusion uses the general written composition proof.
"""
from itertools import combinations
import hashlib
import json
from pathlib import Path
import numpy as np

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')

def minfill_order(g):
    adj={v:set(row) for v,row in enumerate(g)}
    for v in adj:
        for a in g[v]:adj[v]|=g[a]
        adj[v].discard(v)
    order=[]
    while adj:
        v=min(adj,key=lambda v:(sum(b not in adj[a] for a in adj[v] for b in adj[v] if a<b),len(adj[v]),v))
        neighbours=adj[v]
        for a in neighbours:
            adj[a]|=neighbours-{a};adj[a].remove(v)
        order.append(v);del adj[v]
    return order

def exact_beta(g,order=None):
    n=len(g)
    if order is None:order=minfill_order(g)
    assert sorted(order)==list(range(n))
    triples=sorted({tuple(sorted((v,a,b))) for v in range(n) for a,b in combinations(g[v],2)})
    M=n+1
    assert n+M*len(triples)<2**31-1
    factors=[((v,),np.array([0,1],dtype=np.int32)) for v in range(n)]
    for triple in triples:
        f=np.zeros((2,2,2),dtype=np.int32);f[1,1,1]=-M;factors.append((triple,f))
    records=[];largest=0;entries=0
    for v in order:
        bucket=[(vs,t) for vs,t in factors if v in vs]
        factors=[(vs,t) for vs,t in factors if v not in vs]
        variables=tuple(sorted(set().union(*(set(vs) for vs,t in bucket))))
        size=len(variables);largest=max(largest,size);entries+=1<<size
        combined=np.zeros((2,)*size,dtype=np.int32)
        for vs,t in bucket:
            shape=tuple(2 if w in vs else 1 for w in variables)
            combined+=t.reshape(shape)
        value=np.max(combined,axis=variables.index(v));remaining=tuple(w for w in variables if w!=v)
        factors.append((remaining,value))
        records.append({'vertex':v,'bag':list(variables),'entries':1<<size,'message_sha256':hashlib.sha256(value.astype("<i4",copy=False).tobytes(order="C")).hexdigest()})
    assert all(not vs for vs,t in factors)
    optimum=sum(int(t) for vs,t in factors)
    return {'beta':optimum,'order':order,'maximum_bag_size':largest,'combined_assignments':entries,'messages':records,'scope':'Exact integer variable elimination over forbidden three-vertex stars. General recurrence supplies correctness; no floating optimization.'}


def graph(n,edges):
    g=[set() for _ in range(n)]
    for a,b in edges:
        assert a!=b and 0<=a<n and 0<=b<n and b not in g[a]
        g[a].add(b);g[b].add(a)
    return g


def diss(g,D):
    return all(len(g[v]&D)<=1 for v in D)


def beta_brute(g):
    return max((mask.bit_count() for mask in range(1<<len(g))
                if diss(g,{v for v in range(len(g)) if mask>>v&1})),default=0)


def small_controls():
    controls=assignments=0;digest=hashlib.sha256()
    for n,edges in [(5,list(combinations(range(5),2))),
                    (6,[(a,b) for a in range(3) for b in range(3,6)])]:
        for mask in range(1<<len(edges)):
            g=graph(n,[e for j,e in enumerate(edges) if mask>>j&1])
            actual=exact_beta(g)['beta'];expected=beta_brute(g)
            assert actual==expected
            controls+=1;assignments+=1<<n;digest.update(bytes([actual]))
    return {'graphs':controls,'literal_dissociation_subsets':assignments,'optima_sha256':digest.hexdigest(),
            'scope':'All labelled simple five-vertex graphs and fixed-part(3,3) bipartite graphs; independent full subset optima.'}


def construct_base():
    g=[set() for _ in range(68)];colour=[None]*68
    S={6*j+a for j in range(4) for a in range(4)}|set(range(24,44))
    def edge(a,b):
        assert a!=b and colour[a]!=colour[b] and b not in g[a]
        g[a].add(b);g[b].add(a)
    for j in range(4):
        side=int(j>=2)
        for a in range(6):colour[6*j+a]=side if a in (0,4,5) else 1-side
        for a,b in ((0,1),(0,2),(1,4),(2,5),(3,5)):edge(6*j+a,6*j+b)
    W=[[4,10,5,11],[16,22,17,23]]
    for i in range(4):
        for shift in (1,2):edge(W[0][i],W[1][(i+shift)%4])
        if i<2:edge(W[0][i],W[1][i])
    for a in range(24,44):colour[a]=a%2
    for a in range(24,44,2):edge(a,a+1)
    U=[list(range(44,56)),list(range(56,68))]
    for side in (0,1):
        for v in U[side]:colour[v]=side
    for side in (0,1):
        offset=0
        for v in sorted(v for v in S if colour[v]==side):
            for _ in range(4-len(g[v])):
                edge(v,U[1-side][offset%12]);offset+=1
        assert offset==48
    return g,S,colour


def literal_formed(g,S,x):
    return any((a in g[x] and b in g[x]) or (x in g[a] and b in g[a]) or
               (x in g[b] and a in g[b]) for a,b in combinations(sorted(S),2))


def forming_literal(g,S):
    return all(literal_formed(g,S,x) for x in range(len(g)) if x not in S)


def forming_fast(g,S):
    active={v for v in S if g[v]&S}
    return all(len(g[x]&S)>=2 or bool(g[x]&active) for x in range(len(g)) if x not in S)


def connected(g,omit=None):
    vertices=set(range(len(g)))-({omit} if omit is not None else set())
    if not vertices:return True
    todo=[min(vertices)];seen=set(todo)
    for v in todo:
        for w in (g[v]&vertices)-seen:seen.add(w);todo.append(w)
    return seen==vertices


def cyclic_lift(g,S,D,edge,r):
    n=len(g);a,b=edge
    edges=[(i*n+u,i*n+v) for i in range(r) for u in range(n) for v in g[u]
           if u<v and {u,v}!={a,b}]
    edges += [(i*n+a,((i+1)%r)*n+b) for i in range(r)]
    h=graph(n*r,edges)
    chosen={i*n+v for i in range(r) for v in S}
    lower={i*n+v for i in range(r) for v in D}
    return h,chosen,lower


def main():
    root=Path(__file__).resolve().parents[1]
    fixture=json.loads((root/'develop/fixtures/regular-selected-star-gap.json').read_text())
    g,S,col=construct_base();literal=graph(fixture['order'],fixture['edges'])
    assert g==literal and S==set(fixture['selected'])
    D=set(fixture['dissociation_set']);assert len(D)==35 and diss(g,D)
    assert len(S)==36 and all(len(row)==4 for row in g)
    assert all(col[a]!=col[b] for a in range(len(g)) for b in g[a])
    assert forming_literal(g,S)
    for v in S:assert not forming_literal(g,S-{v})
    selected_components=[];remaining=set(S)
    while remaining:
        todo=[min(remaining)];seen=set(todo)
        for v in todo:
            for w in (g[v]&S)-seen:seen.add(w);todo.append(w)
        remaining-=seen;degrees=sorted(len(g[v]&S) for v in seen)
        assert degrees in ([0],[1,1],[1,1,2])
        selected_components.append(degrees)
    assert selected_components.count([1,1,2])==4
    assert selected_components.count([0])==4
    assert selected_components.count([1,1])==10
    assert connected(g) and all(connected(g,v) for v in range(68))
    exact=exact_beta(g);assert exact['beta']==35
    safe=tuple(fixture['safe_port_edge']);assert not(set(safe)&S)
    deleted=[set(row) for row in g];deleted[safe[0]].remove(safe[1]);deleted[safe[1]].remove(safe[0])
    assert connected(deleted)
    safe_exact=exact_beta(deleted);assert safe_exact['beta']==35
    unsafe=tuple(fixture['unsafe_port_edge'])
    bad=[set(row) for row in g];bad[unsafe[0]].remove(unsafe[1]);bad[unsafe[1]].remove(unsafe[0])
    unsafe_exact=exact_beta(bad);assert unsafe_exact['beta']==36
    bad_D=set(fixture['unsafe_deleted_dissociation_set']);assert len(bad_D)==36 and diss(bad,bad_D) and not diss(g,bad_D)
    lifts=[]
    for r in (1,2,3,4,8,16):
        h,chosen,lower=cyclic_lift(g,S,D,safe,r)
        assert len(h)==68*r and len(chosen)==36*r and len(lower)==35*r
        assert all(len(row)==4 for row in h) and connected(h) and diss(h,lower)
        assert all(col[u%68]!=col[v%68] for u in range(len(h)) for v in h[u])
        assert forming_fast(h,chosen)
        for v in chosen:assert not forming_fast(h,chosen-{v})
        if r<=3:assert all(connected(h,v) for v in range(len(h)))
        lifts.append({'copies':r,'order':len(h),'selected_size':len(chosen),'dissociation_lower_certificate':len(lower),
                      'scope':'Regularity/connectivity/minimality and lower set checked; exact beta35r uses the general composition theorem and base certificate.'})
    report={'status':'PASS','small_controls':small_controls(),
            'base':{'order':68,'selected_size':36,'degree':4,'selected_P3_components':4,'selected_edge_components':10,'selected_isolates':4,'literal_single_deletions':36,'vertex_removals_connected':68,'exact':exact},
            'safe_edge':{'edge':list(safe),'deleted_graph_connected':True,'exact':safe_exact},
            'unsafe_edge':{'edge':list(unsafe),'exact':unsafe_exact},'lift_controls':lifts,
            'scope':'Exact integer max-sum elimination proves the finite base and port caps by the written recurrence. The all-r family and its optimal beta follow from the general cyclic outside-edge theorem, not extrapolation from the lift controls. No exact SF value or graph-sharp coefficient claim.'}
    path=root/'output/regular-selected-star-gap-check.json';path.write_text(json.dumps(report,sort_keys=True,separators=(',',':'))+'\n')
    print(json.dumps({'status':'PASS','base_beta':exact['beta'],'safe_deleted_beta':safe_exact['beta'],'unsafe_deleted_beta':unsafe_exact['beta'],'small_controls':report['small_controls'],'lift_orders':[row['order'] for row in lifts],'output':str(path)},sort_keys=True))


if __name__=='__main__':main()
