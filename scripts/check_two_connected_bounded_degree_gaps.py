#!/usr/bin/env python3
"""Physical controls for the all-p/all-k partition and gluing proof.
Standard library only; imports the earlier independent literal graph utilities.
"""
from itertools import combinations
import json
from pathlib import Path
import check_selected_star_general_budget as old

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')


def base(p):
    edges=[(6*j+a,6*j+b)for j in range(2*p)
           for a,b in [(0,1),(0,2),(1,4),(2,5),(3,5)]]
    edges +=[(6*i+a,6*j+b)for i in range(p)for j in range(p,2*p)
             for a in (4,5)for b in (4,5)]
    for first,u in [(0,12*p),(p,12*p+1)]:
        edges +=[(u,6*j+3)for j in range(first,first+p)]+[(u,6*first+2)]
    return old.graph(12*p+2,edges),{6*j+a for j in range(2*p)for a in range(4)}


def glue(p,k):
    g,S=base(p); n=len(g)
    edges=[(i*n+u,i*n+v)for i in range(k)for u in range(n)for v in g[u]if u<v]
    if k>=2:edges +=[(i*n+12*p,((i+1)%k)*n+12*p+1)for i in range(k)]
    return old.graph(n*k,edges),{i*n+v for i in range(k)for v in S}


def maximizer(p,k):
    n=12*p+2
    return {i*n+6*j+a for i in range(k)for j in range(2*p)
            for a in ((1,2,4,5)if j<p else(0,1,3))}


def connected_after(g,removed):
    rest=set(range(len(g)))-set(removed)
    root=min(rest); reached={root};todo=[root]
    while todo:
        x=todo.pop()
        for y in g[x]&rest-reached:reached.add(y);todo.append(y)
    return reached==rest


def blocks(p,first):
    u=12*p+(first!=0)
    return [{u,6*first+2,6*first+5,6*first+3}]+[
        {6*j,6*j+1,6*j+4}for j in range(first,first+p)]+[
        {6*j+2,6*j+5,6*j+3}for j in range(first+1,first+p)]


def audit(p,k):
    g,S=glue(p,k); col=old.colors(g); n=12*p+2
    assert len(g)==n*k and len(S)==8*p*k
    assert min(map(len,g))==2 and max(map(len,g))==2*p+2
    C,L,I=old.structure(g,S)
    assert len(C)==len(I)==2*p*k and len(L)==4*p*k
    assert all(old.local_literal(g,S,x)for x in range(len(g))if x not in S)
    failures=0
    for copy in range(k):
        for j in range(2*p):
            c=copy*n+6*j
            # Explicit failure vertices for centre,x,y,isolate deletions.
            for removed,w in [(c,c+4),(c+1,c+4),(c+2,c+5),(c+3,c+3)]:
                assert not old.local_literal(g,S-{removed},w); failures+=1
    Q=maximizer(p,k)
    assert len(Q)==7*p*k and old.diss(g,Q)
    assert all(copy*n+12*p not in Q and copy*n+12*p+1 not in Q for copy in range(k))
    if len(g)<=38:assert old.minimal(g,S)
    baseg,baseS=base(p)
    for first in (0,p):
        partition=blocks(p,first);union=set().union(*partition)
        assert len(union)==6*p+1 and sum(map(len,partition))==len(union)
        assert union==set(range(6*first,6*(first+p)))|{12*p+(first!=0)}
        for ix,block in enumerate(partition):
            assert sorted(len(baseg[x]&block)for x in block)==([2]*4 if ix==0 else[1,1,2])
            cap=max(len(D)for size in range(len(block)+1)for D in map(set,combinations(block,size))if old.diss(baseg,D))
            assert cap==2
        noW=[{6*j,6*j+1,6*j+2}for j in range(first,first+p)]
        noW +=[{12*p+(first!=0)}|{6*j+3 for j in range(first,first+p)}]
        assert set().union(*noW)==union-{6*j+a for j in range(first,first+p)for a in (4,5)}
        assert sum(map(len,noW))==len(set().union(*noW))
    if p<=8:
        assert all(connected_after(g,[v])for v in range(len(g)))
        deletions=len(g)
    else:
        assert connected_after(g,[])
        deletions=0
    return {'p':p,'k':k,'order':len(g),'selected':len(S),'certified_beta':len(Q),
            'gap':p*k,'minimum_degree':2,'maximum_degree':2*p+2,
            'literal_deletion_failures':failures,'all_single_vertex_deletions_checked':deletions,
            'beta_method':'general wing-partition upper proof plus explicit physical lower set; no large exact enumeration'}


def exact_controls():
    rows=[]
    for p in (1,2,3):
        g,S=base(p); beta,subsets=old.one_part_beta(g,old.colors(g))
        if p<=2:assert beta==old.beta_literal(g)
        assert beta==(8 if p==1 else 7*p)
        row={'p':p,'order':len(g),'selected':len(S),'exact_beta':beta,'one_part_subsets':subsets}
        if p==1:row['scope']='boundary outside theorem; beta8 exceeds7p, so p>=2 is necessary'
        rows.append(row)
    return rows


def main():
    models=[audit(p,k)for p in (2,3,4,5,8,16,32)for k in (1,2,3,7)]
    report={'status':'PASS','physical_models':models,'exact_controls':exact_controls(),
            'scope':'All-size theorem uses the written partition and gluing proof, not extrapolation. Exact small optima use independent one-part enumeration and (at p<=2) forbidden-triple recurrence. Connectivity deletion controls run only at p<=8.'}
    dest=Path(__file__).resolve().parents[1]/'output/two-connected-bounded-degree-gaps-check.json'
    dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','physical_models':len(models),'literal_deletion_failures':sum(r['literal_deletion_failures']for r in models),
                      'single_vertex_deletions':sum(r['all_single_vertex_deletions_checked']for r in models),
                      'exact_controls':len(report['exact_controls'])},sort_keys=True))


if __name__=='__main__':main()
