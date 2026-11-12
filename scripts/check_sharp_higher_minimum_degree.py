#!/usr/bin/env python3
"""Physical checks of the all-minimum-degree sharpness subfamily.
The exact dissociation cap is proved by cases, not solved here numerically.
"""
from itertools import combinations
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
import witness_interface_optimizer as opt
from check_sharp_minimum_two_degree import diss,literal
if not __debug__:raise RuntimeError('Assertions are required.')


def base(t,r):
    if type(t)is not int or type(r)is not int or t<2 or r<3:
        raise ValueError('Integer t>=2,r>=3 required.')
    p=t*r;old,S=opt.graph(p,p,opt.degree_adjacency(p));n=12*p+2*t
    g=[set()for _ in range(n)]
    def edge(a,b):g[a].add(b);g[b].add(a)
    for a in range(12*p):
        for b in old[a]:
            if a<b<12*p:edge(a,b)
    A=tuple(range(12*p,12*p+t));B=tuple(range(12*p+t,n))
    for first,own,other in((0,A,B),(p,B,A)):
        for j in range(p):
            c=6*(first+j)
            for s in range(t):
                edge(own[s],c+3)
                if s!=j%t:edge(own[s],c+1);edge(other[s],c)
                if s!=(j+1)%t:edge(own[s],c+2)
    Q={6*j+a for j in range(2*p)for a in((0,1,3)if j<p else(1,2,4,5))}
    return g,S,Q


def lift(t,r,k):
    if type(k)is not int or k<1:raise ValueError('Positive integer k required.')
    old,S0,Q0=base(t,r);p=t*r;n=len(old);g=[set()for _ in range(n*k)]
    for j in range(k):
        for a in range(n):
            for b in old[a]:
                if a<b and(a,b)!=(5,6*p+5):g[n*j+a].add(n*j+b);g[n*j+b].add(n*j+a)
        a,b=n*j+5,n*((j+1)%k)+6*p+5;g[a].add(b);g[b].add(a)
    return g,{n*j+x for j in range(k)for x in S0},{n*j+x for j in range(k)for x in Q0}


def physical(t,r,k,delete_port=False):
    p=t*r;n0=12*p+2*t;g,S,Q=lift(t,r,k);delta=t+1;Delta=(4*t-3)*r
    if delete_port:
        assert k==1;g[5].remove(6*p+5);g[6*p+5].remove(5)
    assert len(g)==n0*k and len(S)==8*p*k and len(Q)==7*p*k
    assert min(map(len,g))==delta and max(map(len,g))==Delta and diss(g,Q)
    col={0:0};todo=[0]
    while todo:
        a=todo.pop();assert a not in g[a]
        for b in g[a]:
            assert a in g[b]
            if b not in col:col[b]=1-col[a];todo.append(b)
            assert col[b]!=col[a]
    assert len(col)==len(g)
    for x in set(range(len(g)))-S:assert literal(g,S,x)
    for x in S:
        copy,v=divmod(x,n0);j,kind=divmod(v,6)
        failure=n0*copy+6*j+{0:4,1:4,2:5,3:3}[kind]
        assert not literal(g,S,failure,x)
    for omitted in range(len(g)):
        root=next(x for x in range(len(g))if x!=omitted);seen={root};todo=[root]
        while todo:
            for b in g[todo.pop()]:
                if b!=omitted and b not in seen:seen.add(b);todo.append(b)
        assert len(seen)==len(g)-1
    pair_coverage=single_y=0
    for copy in range(k):
        o=copy*n0;A=set(range(o+12*p,o+12*p+t));B=set(range(o+12*p+t,o+n0))
        assert all(len(g[a])==Delta for a in A|B)
        assert all(g[a]<=S for a in A|B)
        for first,own,other in((0,A,B),(p,B,A)):
            I={o+6*(first+j)+3 for j in range(p)}
            leaves={o+6*(first+j)+a for j in range(p)for a in(1,2)}
            oppositeC={o+6*((p-first)+j)for j in range(p)}
            ys={o+6*(first+j)+2 for j in range(p)}
            for a in own:
                assert I<=g[a]and len(g[a]&ys)==p-p//t
                single_y+=1
            for a,b in combinations(sorted(own),2):
                assert I|leaves|oppositeC <= g[a]|g[b]
                pair_coverage+=1
            for j in range(p):
                x,y=o+6*(first+j)+1,o+6*(first+j)+2
                assert len(own-g[x])==len(own-g[y])==1 and own-g[x]!=own-g[y]
        for j in range(p):
            L=[o+6*j+a for a in(4,5)];R=[o+6*(p+(j+1)%p)+a for a in(4,5)]
            assert all(b in g[a]for a in L for b in R)
    assert p>=2*t+2 and 6*p+4<=7*p and 6*p+2+2*t<=7*p
    assert Delta*len(g)==(12*Delta+8*delta-14)*(len(S)-len(Q))
    return {'t':t,'r':r,'p':p,'k':k,'safe_edge_deleted':delete_port,'order':len(g),
            'selected':len(S),'attaining_set_size':len(Q),'minimum_degree':delta,
            'maximum_degree':Delta,'literal_deletion_failures':len(S),
            'single_vertex_deletion_checks':len(g),'same_side_pair_coverage_checks':pair_coverage,
            'single_connector_y_checks':single_y,
            'beta_cap_source':'Analytical cases; no exhaustive large-graph solve.'}


def main():
    invalid=0
    for t,r in((1,3),(2,2),(True,3),(2,False),(2,3.0)):
        try:base(t,r)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid domain accepted.')
    models=[physical(t,r,k)for t in(2,3,4,6)for r in(3,4)for k in(1,2)]
    models +=[physical(t,3,1,True)for t in(2,3,4,6)]
    report={'status':'PASS','models':models,'invalid_domains_rejected':invalid,
            'scope':'Physical construction, literal stars/deletions, slot and connector '
                    'coverage, all vertex deletions and sharpness arithmetic. '
                    'The infinite-parameter exact beta uses the written proof.'}
    out=ROOT/'output/sharp-higher-minimum-degree-check.json'
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','physical_models':len(models),
                      'literal_deletion_failures':sum(x['literal_deletion_failures']for x in models),
                      'single_vertex_deletion_checks':sum(x['single_vertex_deletion_checks']for x in models)},sort_keys=True))


if __name__=='__main__':main()
