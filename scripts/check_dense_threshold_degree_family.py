#!/usr/bin/env python3
"""Dense witness construction at Delta=4delta-7, delta>=4.
Small exact recursion is a control, not a premise of the all-p proof.
"""
from pathlib import Path
from functools import lru_cache
import json,sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
from check_sharp_minimum_two_degree import diss,literal
if not __debug__:raise RuntimeError('Assertions required.')

def base(p):
    if type(p)is not int or p<3:raise ValueError("Integer p>=3 required.")
    n=14*p;g=[set()for _ in range(n)]
    def edge(a,b):g[a].add(b);g[b].add(a)
    for j in range(2*p):
        c=6*j
        for a,b in((0,1),(0,2),(1,4),(2,5),(3,5)):edge(c+a,c+b)
    for j in range(p):
        for a in(4,5):
            for k in range(p):
                for b in(4,5):
                    edge(6*j+a,6*(p+k)+b)
    A=range(12*p,13*p);B=range(13*p,14*p)
    for first,own,other in((0,A,B),(p,B,A)):
        for j in range(p):
            c=6*(first+j)
            for s in range(p):
                edge(own[s],c+3)
                if s!=3*j%p:edge(own[s],c+1)
                if s!=(3*j+1)%p:edge(own[s],c+2)
                if s!=(3*j+2)%p:edge(other[s],c)
    S={6*j+a for j in range(2*p)for a in range(4)}
    Q={6*j+a for j in range(2*p)for a in((0,1,3)if j<p else(1,2,4,5))}
    return g,S,Q

def exact(g):
    masks=[sum(1<<b for b in a)for a in g];calls=0
    @lru_cache(None)
    def solve(active):
        nonlocal calls
        calls+=1
        if not active:return 0,0
        # Split components before branching.
        seed=active&-active;component=seed;front=seed
        while front:
            bit=front&-front;front-=bit;a=bit.bit_length()-1
            new=masks[a]&active&~component;component|=new;front|=new
        if component!=active:
            v,w=solve(component);x,y=solve(active^component);return v+x,w|y
        vertices=[v for v in range(len(g))if active>>v&1]
        v=max(vertices,key=lambda x:(masks[x]&active).bit_count())
        neighbours=masks[v]&active;degree=neighbours.bit_count();vb=1<<v
        if degree<=1:return len(vertices),active
        # Exclude v, include v isolated, or pair v to one surviving neighbour.
        best=solve(active^vb)
        value,Q=solve(active&~(masks[v]|vb))
        if value+1>best[0]:best=value+1,Q|vb
        for u in vertices:
            if neighbours>>u&1:
                value,Q=solve(active&~(masks[v]|masks[u]|vb|(1<<u)))
                if value+2>best[0]:best=value+2,Q|vb|(1<<u)
        return best
    value,Q=solve((1<<len(g))-1)
    chosen={v for v in range(len(g))if Q>>v&1};assert diss(g,chosen)and len(chosen)==value
    return {'beta':value,'attaining':sorted(chosen),'cache':solve.cache_info()._asdict(),'calls':calls}

def lift(p,k):
    if type(k)is not int or k<1:raise ValueError('Integer k>=1 required.')
    old,S,Q=base(p);n=len(old);g=[set()for _ in range(n*k)]
    for j in range(k):
        for a in range(n):
            for b in old[a]:
                if a<b and(a,b)!=(5,6*p+5):g[n*j+a].add(n*j+b);g[n*j+b].add(n*j+a)
        a,b=n*j+5,n*((j+1)%k)+6*p+5;g[a].add(b);g[b].add(a)
    return g,{n*j+a for j in range(k)for a in S},{n*j+a for j in range(k)for a in Q}


def physical(p,k,deleted=False):
    g,S,Q=lift(p,k);n=14*p;delta=p+1;Delta=4*p-3
    if deleted:
        assert k==1;g[5].remove(6*p+5);g[6*p+5].remove(5)
    assert len(g)==n*k and len(S)==8*p*k and len(Q)==7*p*k and diss(g,Q)
    assert min(map(len,g))==delta and max(map(len,g))==Delta
    colours={0:0};todo=[0]
    while todo:
        a=todo.pop();assert a not in g[a]
        for b in g[a]:
            assert a in g[b]
            if b not in colours:colours[b]=1-colours[a];todo.append(b)
            assert colours[b]!=colours[a]
    assert len(colours)==len(g)
    for a in set(range(len(g)))-S:assert literal(g,S,a)
    for a in S:
        copy,j=divmod(a,n);block,kind=divmod(j,6)
        failure=n*copy+6*block+{0:4,1:4,2:5,3:3}[kind]
        assert not literal(g,S,failure,a)
    for omitted in range(len(g)):
        root=next(x for x in range(len(g))if x!=omitted);seen={root};todo=[root]
        while todo:
            for b in g[todo.pop()]:
                if b!=omitted and b not in seen:seen.add(b);todo.append(b)
        assert len(seen)==len(g)-1
    for copy in range(k):
        o=n*copy
        for first in(0,p):
            for j in range(p):
                c=o+6*(first+j)
                assert all(len(g[c+a])==p+1 for a in range(4))
                assert len(g[c+4])==2*p+1
                assert len(g[c+5])==2*p+2-(1 if deleted and j==0 else 0)
        assert all(len(g[a])==Delta for a in range(o+12*p,o+14*p))
    assert Delta*len(g)==(12*Delta+8*delta-14)*(len(S)-len(Q))
    return {'p':p,'k':k,'safe_edge_deleted':deleted,'n':len(g),'selected':len(S),
            'attaining_size':len(Q),'minimum_degree':delta,'maximum_degree':Delta,
            'literal_failures':len(S),'vertex_deletion_checks':len(g),
            'beta_cap':'All-p combinatorial proof, not finite optimizer inference.'}


def main():
    rows=[physical(p,k)for p in(3,4,5,6,7,9)for k in(1,2,3)]
    rows +=[physical(p,1,True)for p in(3,4,5,6,7,9)]
    controls=[]
    for p in(3,4):
        for deleted in(False,True):
            g,S,Q=base(p)
            if deleted:g[5].remove(6*p+5);g[6*p+5].remove(5)
            result=exact(g);assert result['beta']==7*p
            controls.append({'p':p,'safe_edge_deleted':deleted,**result})
    invalid=0
    for p in(0,2,True,3.5):
        try:base(p)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid p accepted.')
    for k in(0,False,1.5):
        try:lift(3,k)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid k accepted.')
    record={'status':'PASS','physical_models':rows,'small_exact_controls':controls,
            'invalid_domains_rejected':invalid,
            'scope':'General cap and all-scale theorem use written proof. Independent '
                    'exact graph recurrence controls only p3,p4 full and deleted bases. '
                    'Physical models check bipartition, degree extrema, formation, '
                    'literal minimality, attaining set and every vertex deletion.'}
    out=ROOT/'output/dense-threshold-degree-check.json';out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','physical_models':len(rows),
        'literal_failures':sum(r['literal_failures']for r in rows),
        'vertex_deletion_checks':sum(r['vertex_deletion_checks']for r in rows),
        'small_exact_controls':len(controls),'exact_recurrence_states':sum(r['calls']for r in controls)},sort_keys=True))


if __name__=='__main__':main()
