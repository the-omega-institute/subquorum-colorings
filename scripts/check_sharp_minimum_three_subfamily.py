#!/usr/bin/env python3
"""Physical controls; the large-graph dissociation cap has a general proof."""
from pathlib import Path
import json
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'develop'))
import witness_interface_optimizer as opt
from check_sharp_minimum_two_degree import diss,literal
if not __debug__:raise RuntimeError('Run with assertions enabled.')


def base(p):
    if type(p)is not int or p<6 or p%2:raise ValueError('Even integer p>=6 required.')
    old,S=opt.graph(p,p,opt.degree_adjacency(p))
    n=12*p+4;g=[set()for _ in range(n)]
    def edge(a,b):g[a].add(b);g[b].add(a)
    for a in range(12*p):
        for b in old[a]:
            if a<b<12*p:edge(a,b)
    A0,A1,B0,B1=range(12*p,n)
    for first,us,vs in((0,(A0,A1),(B0,B1)),(p,(B0,B1),(A0,A1))):
        for j in range(p):
            c=6*(first+j)
            for x in us:edge(x,c+3)
            edge(us[0],c+1);edge(us[1],c+2);edge(vs[j>=p//2],c)
    Q={6*j+a for j in range(2*p)for a in((0,1,3)if j<p else(1,2,4,5))}
    return g,S,Q


def lift(p,k):
    if type(k)is not int or k<1:raise ValueError('Positive integer lift size required.')
    g0,S0,Q0=base(p);n=len(g0);g=[set()for _ in range(n*k)];ports=(5,6*p+5)
    for j in range(k):
        for a in range(n):
            for b in g0[a]:
                if a<b and(a,b)!=ports:g[n*j+a].add(n*j+b);g[n*j+b].add(n*j+a)
        a,b=n*j+ports[0],n*((j+1)%k)+ports[1];g[a].add(b);g[b].add(a)
    return g,{n*j+x for j in range(k)for x in S0},{n*j+x for j in range(k)for x in Q0}


def connected(g,omitted):
    root=next(x for x in range(len(g))if x!=omitted);seen={root};todo=[root]
    while todo:
        for x in g[todo.pop()]:
            if x!=omitted and x not in seen:seen.add(x);todo.append(x)
    return len(seen)==len(g)-1


def physical(p,k,delete_port=False):
    g,S,Q=lift(p,k);n0=12*p+4
    if delete_port:
        assert k==1;g[5].remove(6*p+5);g[6*p+5].remove(5)
    assert len(g)==n0*k and len(S)==8*p*k and len(Q)==7*p*k
    assert min(map(len,g))==3 and max(map(len,g))==5*p//2
    col={0:0};todo=[0]
    while todo:
        a=todo.pop();assert a not in g[a]
        for b in g[a]:
            assert a in g[b]
            if b not in col:col[b]=1-col[a];todo.append(b)
            assert col[b]!=col[a]
    assert len(col)==len(g)and diss(g,Q)
    for x in set(range(len(g)))-S:assert literal(g,S,x)
    for x in S:
        copy,r=divmod(x,n0);block,kind=divmod(r,6)
        failure=n0*copy+6*block+{0:4,1:4,2:5,3:3}[kind]
        assert not literal(g,S,failure,x)
    for copy in range(k):
        for j in range(p):
            L=[n0*copy+6*j+a for a in(4,5)]
            R=[n0*copy+6*(p+(j+1)%p)+a for a in(4,5)]
            assert all(b in g[a]for a in L for b in R)
    for x in range(len(g)):assert connected(g,x)
    assert(5*p//2)*len(g)==(12*(5*p//2)+10)*(len(S)-len(Q))
    return {'p':p,'k':k,'deleted_port':delete_port,'order':len(g),'selected':len(S),
            'attaining_set_size':len(Q),'minimum_degree':3,'maximum_degree':5*p//2,
            'literal_deletion_failures':len(S),'single_vertex_deletion_checks':len(g),
            'beta_cap_source':'General case proof, not an exhaustive physical solve.'}


def kernel_controls():
    rows=[]
    for p in(2,3,4,5):
        adj=[0]*(2*p)
        for j in range(p):
            for d in(0,1):
                for e in(0,1):adj[2*j+d]|=1<<(2*((j+1)%p)+e)
            adj[2*j]|=(1<<(2*j))|(1<<(2*j+1))|(1<<(2*((j+2)%p)))
            adj[2*j+1]|=1<<(2*((j+2)%p))
        rev=[sum(1<<a for a in range(2*p)if adj[a]>>b&1)for b in range(2*p)]
        tested=valid=0
        for left in range(1<<(2*p)):
            for right in range(1<<(2*p)):
                tested+=1
                if any(left>>a&1 and(adj[a]&right).bit_count()>1 for a in range(2*p)):continue
                if any(right>>b&1 and(rev[b]&left).bit_count()>1 for b in range(2*p)):continue
                good=[]
                for w,other,rel in((left,right,adj),(right,left,rev)):
                    good.append(sum(bool(w>>(2*j)&3)and not(w>>(2*j+1)&1 and rel[2*j+1]&other)for j in range(p)))
                aL=sum(bool(left>>(2*j)&1)for j in range(p));aR=sum(bool(right>>(2*j)&1)for j in range(p))
                assert left.bit_count()+right.bit_count()<=2*p
                assert aL+good[1]<=p and aR+good[0]<=p
                valid+=1
        rows.append({'p':p,'all_witness_pairs':tested,'legal_pairs':valid})
    local=0;es=[(0,1),(0,2),(1,4),(2,5),(3,5)]
    for mask in range(64):
        Q={x for x in range(6)if mask>>x&1}
        if any(sum(y in Q for a,b in es for y in([b]if a==x else[a]if b==x else[]))>1 for x in Q):continue
        if not Q&{1,3}:assert len(Q)<=2+(4 in Q);local+=1
    return {'ranges':rows,'local_x_i_absent_checks':local,
            'scope':'Exhaustive smaller abstract witness kernels, not full physical-graph optima.'}


def main():
    invalid=0
    for p in(0,2,4,5,7,True):
        try:base(p)
        except ValueError:invalid+=1
        else:raise AssertionError('Invalid input accepted.')
    models=[physical(p,k)for p in(6,8,10,12,20)for k in(1,2,3)]
    models +=[physical(p,1,True)for p in(6,8,10,12,20)]
    report={'status':'PASS','models':models,'invalid_domains_rejected':invalid,
            'kernel_controls':kernel_controls(),
            'scope':'Physical constructions, literal witnesses, two-connectivity and attaining sets. '
                    'The arbitrary-p/k upper cap is proved analytically in the note.'}
    out=ROOT/'output/sharp-minimum-three-subfamily-check.json'
    out.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
    print(json.dumps({'status':'PASS','physical_models':len(models),
                      'literal_deletion_failures':sum(r['literal_deletion_failures']for r in models),
                      'single_vertex_deletion_checks':sum(r['single_vertex_deletion_checks']for r in models)},sort_keys=True))


if __name__=='__main__':main()
