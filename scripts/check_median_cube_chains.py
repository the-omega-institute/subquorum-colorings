"""Independent metric/cube controls for the structural note; standard library only."""
from collections import deque
from itertools import combinations
from pathlib import Path
import json


def make_graph(n,edges):
    g=[set() for _ in range(n)]
    for a,b in edges:
        g[a].add(b);g[b].add(a)
    return g


def distances(g):
    out=[]
    for v in range(len(g)):
        d=[-1]*len(g);d[v]=0;q=deque([v])
        while q:
            u=q.popleft()
            for w in g[u]:
                if d[w]<0:d[w]=d[u]+1;q.append(w)
        assert min(d)>=0
        out.append(d)
    return out


def intervals(d):
    return [[{x for x in range(len(d)) if d[a][x]+d[x][b]==d[a][b]}
             for b in range(len(d))] for a in range(len(d))]


def cubes(g):
    found=set()
    for v,neighbours in enumerate(g):
        for a,b,c in combinations(sorted(neighbours),3):
            mids=[]
            for u,w in ((a,b),(a,c),(b,c)):
                common=(g[u]&g[w])-{v}
                if len(common)!=1:break
                mids.append(next(iter(common)))
            if len(mids)!=3:continue
            far=g[mids[0]]&g[mids[1]]&g[mids[2]]
            for z in far:
                candidate=frozenset((v,a,b,c,*mids,z))
                if len(candidate)==8 and all(len(g[x]&candidate)==3 for x in candidate):
                    found.add(candidate)
    return sorted(found,key=lambda s:tuple(sorted(s)))


def components(g,vertices):
    unseen=set(vertices);result=[]
    while unseen:
        root=min(unseen);unseen.remove(root);comp={root};q=[root]
        for u in q:
            for v in g[u]&unseen:
                unseen.remove(v);comp.add(v);q.append(v)
        result.append(comp)
    return result


def check(g,report):
    assert max(map(len,g))<=4
    d=distances(g);iv=intervals(d)
    for a,b,c in combinations(range(len(g)),3):
        assert len(iv[a][b]&iv[a][c]&iv[b][c])==1
        report['median_triples']+=1
    for v in range(len(g)):
        assert len(components(g,set(range(len(g)))-{v}))==1
        report['vertex_deletions']+=1
    cs=cubes(g)
    cg=[{j for j in range(len(cs)) if j!=i and cs[i]&cs[j]}
        for i in range(len(cs))]
    for cc in components(cg,range(len(cs))):
        assert max(len(cg[i]) for i in cc)<=2
        assert sum(len(cg[i]) for i in cc)==2*(len(cc)-1)
        t=set().union(*(cs[i] for i in cc));r=len(cc)
        assert len(t)==4*r+4
        assert sum(len(g[v]&t) for v in t)==2*(8*r+4)
        assert all(iv[a][b]<=t for a,b in combinations(t,2))
        ends={v for v in t if len(g[v]&t)==3}
        assert len(ends)==8
        assert all(not(g[v]-t) for v in t-ends)
        assert sum(len(g[v]-t) for v in t)<=8
        if r>=2:
            end_comps=components(g,ends)
            assert sorted(map(len,end_comps))==[4,4]
            for outside in components(g,set(range(len(g)))-t):
                ports=set().union(*(g[v]&t for v in outside))
                assert len(ports)>=2 and any(ports<=end for end in end_comps)
        report['cube_components']+=1
        report['cubes']+=r
    report['models']+=1


def chain(r):
    edges=[]
    for layer in range(r+1):
        edges.extend((4*layer+j,4*layer+(j+1)%4) for j in range(4))
        if layer:edges.extend((4*(layer-1)+j,4*layer+j) for j in range(4))
    return make_graph(4*(r+1),edges)


def add_ears(g,matching):
    g=[row.copy() for row in g]
    for u,v in matching:
        assert v in g[u]
        a=len(g);b=a+1;g.extend([{u,b},{a,v}]);g[u].add(a);g[v].add(b)
    return g


def main():
    report=dict(status='PASS',models=0,cube_components=0,cubes=0,
                median_triples=0,vertex_deletions=0,subcubic_models=0,
                nonplanar_hypothesis_control=False,new_Lean=False)
    for r in range(1,7):
        g=chain(r)
        check(g,report)
        for matching in ([(0,1)],[(0,1),(4*r,4*r+1)],
                         [(0,1),(2,3),(4*r,4*r+1),(4*r+2,4*r+3)]):
            check(add_ears(g,matching),report)
    for n in range(2,17):
        edges=[(i,i+1) for i in range(n-1)]+[(n+i,n+i+1) for i in range(n-1)]
        edges += [(i,n+i) for i in range(n)]
        g=make_graph(2*n,edges);check(g,report)
        assert max(map(len,g))<=3
        report['subcubic_models']+=1
    q4=make_graph(16,[(v,v^(1<<i)) for v in range(16) for i in range(4)])
    # Q4 is median and degree four, but violates planar bipartite edge bound.
    iv=intervals(distances(q4))
    assert all(len(iv[a][b]&iv[a][c]&iv[b][c])==1
               for a,b,c in combinations(range(16),3))
    cs=cubes(q4)
    assert max(sum(bool(c&d) for d in cs if c!=d) for c in cs)>2
    assert sum(map(len,q4))//2>2*len(q4)-4
    report['nonplanar_hypothesis_control']=True
    out=Path(__file__).resolve().parents[1]/'output'
    out.mkdir(exist_ok=True)
    (out/'median-cube-chain-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__=='__main__':main()
