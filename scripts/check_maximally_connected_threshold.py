#!/usr/bin/env python3
"""Maximally connected sharp degree-threshold family.
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
                if a<b and not(a%6==b%6==5 and a<6*p and b==a+6*p):g[n*j+a].add(n*j+b);g[n*j+b].add(n*j+a)
        for port in range(p):
            a,b=n*j+6*port+5,n*((j+1)%k)+6*(p+port)+5;g[a].add(b);g[b].add(a)
    return g,{n*j+a for j in range(k)for a in S},{n*j+a for j in range(k)for a in Q}


def physical(p,k,deleted=False):
    g,S,Q=lift(p,k);n=14*p;delta=p+1;Delta=4*p-3
    if deleted:
        assert k==1
        for port in range(p):
            a,b=6*port+5,6*(p+port)+5;g[a].remove(b);g[b].remove(a)
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
                assert len(g[c+5])==2*p+2-(1 if deleted else 0)
        assert all(len(g[a])==Delta for a in range(o+12*p,o+14*p))
    assert Delta*len(g)==(12*Delta+8*delta-14)*(len(S)-len(Q))
    return {'p':p,'k':k,'safe_edge_deleted':deleted,'n':len(g),'selected':len(S),
            'attaining_size':len(Q),'minimum_degree':delta,'maximum_degree':Delta,
            'literal_failures':len(S),'vertex_deletion_checks':len(g),
            'beta_cap':'All-p combinatorial proof, not finite optimizer inference.'}


def local_connectivity_at_least(g,source,target,bound):
    # Vertex-split augmenting paths for NONADJACENT terminal pairs.
    assert source!=target and target not in g[source]
    n=len(g);caps=[{}for _ in range(2*n)]
    def arc(a,b,c):
        caps[a][b]=c;caps[b].setdefault(a,0)
    for a in range(n):
        arc(2*a,2*a+1,bound if a in(source,target)else 1)
        for b in g[a]:arc(2*a+1,2*b,bound)
    total=0;sink=2*target;start=2*source+1
    while total<bound:
        parent={start:None};queue=[start]
        for a in queue:
            for b,c in caps[a].items():
                if c and b not in parent:parent[b]=a;queue.append(b)
            if sink in parent:break
        if sink not in parent:return total
        a=sink;amount=bound-total
        while a!=start:
            b=parent[a];amount=min(amount,caps[b][a]);a=b
        a=sink
        while a!=start:
            b=parent[a];caps[b][a]-=amount;caps[a][b]+=amount;a=b
        total+=amount
    return total


def connectivity_certificate(p,k):
    g,S,Q=lift(p,k);delta=p+1;calls=0
    roots=list(range(delta))
    for a in roots:
        for b in range(len(g)):
            if a==b or b in g[a]:continue
            assert local_connectivity_at_least(g,a,b,delta)>=delta
            calls+=1
    # Any cut of fewer than delta vertices leaves one of delta roots.
    # A component separated from that root would violate one of these flows.
    return {'p':p,'k':k,'roots':roots,'required_vertex_connectivity':delta,
            'nonadjacent_root_target_flows':calls}


def main():
    rows=[physical(p,k)for p in(3,4,5,6,7,9)for k in(1,2,3)]
    rows +=[physical(p,1,True)for p in(3,4,5,6,7,9)]
    controls=[]
    for p in(3,4):
        g,S,Q=lift(p,1)
        for port in range(p):
            a,b=6*port+5,6*(p+port)+5;g[a].remove(b);g[b].remove(a)
        result=exact(g);assert result['beta']==7*p
        controls.append({'p':p,'all_diagonal_b_edges_deleted':True,**result})
    flows=[connectivity_certificate(p,k)for p,k in((3,1),(3,2),(4,1),(4,2),(5,1),(6,2))]
    record={'status':'PASS','physical_models':rows,'small_exact_controls':controls,
            'connectivity_certificates':flows,
            'scope':'All-p proof establishes beta and connectivity. Physical controls '
                    'test parallel-port switching, literal minimality, degrees and '
                    'attainment. Standard vertex-split integer flows certify exact '
                    'minimum-degree connectivity for six finite models; two exact '
                    'recursions check all-diagonal-deleted bases p3,p4.'}
    out=ROOT/'output/maximally-connected-threshold-check.json'
    out.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','physical_models':len(rows),
        'literal_failures':sum(r['literal_failures']for r in rows),
        'vertex_deletion_checks':sum(r['vertex_deletion_checks']for r in rows),
        'connectivity_models':len(flows),
        'nonadjacent_root_target_flows':sum(x['nonadjacent_root_target_flows']for x in flows),
        'small_exact_controls':len(controls)},sort_keys=True))


if __name__=='__main__':main()
