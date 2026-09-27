#!/usr/bin/env python3
"""Exact finite checks of the short residual-path compensation paper proof.
Finite checks are not the proof and do not settle the full grid formula.
"""
from __future__ import annotations
import argparse, collections, hashlib, itertools, json, random
from pathlib import Path

DIRECTIONS=((-1,0),(0,1),(1,0),(0,-1))
def bits(mask):
    while mask:
        bit=mask & -mask
        yield bit.bit_length()-1
        mask ^= bit

def graph(m,n):
    adj=[0]*(m*n); edges=[]
    for v in range(m*n):
        i,j=divmod(v,n)
        for w in (v+1 if j+1<n else -1,v+n if i+1<m else -1):
            if w>=0:
                adj[v]|=1<<w;adj[w]|=1<<v;edges.append((v,w))
    return adj,edges

def feasible(adj,T,M):
    A=T;used=set()
    for v,w in M:
        if v==w or not(adj[v]>>w&1) or v in used or w in used:return False
        used.update((v,w))
        if T>>v&1 or T>>w&1:return False
        A |= (1<<v)|(1<<w)
    return all((adj[v]&A).bit_count()<=1 for v in bits(T))

def pairs(m,n):
    adj,_=graph(m,n)
    def go(left,T,A,M):
        if not left:
            yield T,M
            return
        bit=left&-left;v=bit.bit_length()-1;rest=left^bit
        yield from go(rest,T,A,M)
        if (adj[v]&A).bit_count()<=1 and all((adj[w]&A).bit_count()==0 for w in bits(adj[v]&T)):
            yield from go(rest,T|bit,A|bit,M)
        for w in bits(adj[v]&rest):
            wb=1<<w;new=A|bit|wb
            if all((adj[x]&new).bit_count()<=1 for x in bits(T)):
                yield from go(rest^wb,T,new,M+((v,w),))
    yield from go((1<<(m*n))-1,0,0,())

def residual(m,n,T,M):
    assert m%2==n%2==0 and m>0 and n>0
    nr,nc=m//2,n//2;N=nr*nc
    tile=lambda v:(v//n//2)*nc+(v%n//2)
    vertices=[tuple((2*i+a)*n+2*j+b for a,b in ((0,0),(0,1),(1,0),(1,1))) for i in range(nr) for j in range(nc)]
    t=[0]*N;h=[0]*N;s=[0]*N;E=[];ends=[];A=T
    for v in bits(T):t[tile(v)]+=1
    for v,w in M:
        A|=(1<<v)|(1<<w);a,b=tile(v),tile(w)
        if a==b:h[a]+=1
        elif t[a]==t[b]==2:raise AssertionError('saturated-saturated matching')
        elif t[a]==2:s[b]+=1
        elif t[b]==2:s[a]+=1
        else:E.append((a,b));ends.append((v,w))
    r=[2-t[i]-h[i]-s[i] for i in range(N)];deg=[0]*N;neighbors=[[] for _ in range(N)]
    assert min(r)>=0 and max(t)<=2
    for e,(a,b) in enumerate(E):
        deg[a]+=1;deg[b]+=1;neighbors[a].append((b,e));neighbors[b].append((a,e))
    L={i for i in range(N) if r[i]==0 and deg[i]==1}
    for i in range(N):assert deg[i]<=(1 if r[i]==0 else 2*r[i])
    assert all(not(a in L and b in L) for a,b in E)
    return dict(m=m,n=n,nr=nr,nc=nc,N=N,T=T,M=M,A=A,vertices=vertices,t=t,h=h,s=s,r=r,E=E,ends=ends,deg=deg,neighbors=neighbors,L=L)

def check_geometry(g):
    m,n,nc=g['m'],g['n'],g['nc'];L=g['L'];r=g['r'];sources={};loads=collections.Counter()
    for Q in range(g['N']):
        leaf_edges=[(w,e) for w,e in g['neighbors'][Q] if w in L]
        assert len(leaf_edges)<=2,('three leaf neighbors',m,n,g['T'],g['M'],Q)
        # For a leaf edge, the companion corner on the same side cannot
        # itself be an endpoint of another edge leading to a zero leaf.
        entry={}
        for w,e in leaf_edges:
            a,b=g['E'][e];v,z=g['ends'][e];p=v if a==Q else z
            entry[p]=w
        for p,w in entry.items():
            qi,qj=divmod(Q,nc);wi,wj=divmod(w,nc);pi,pj=divmod(p,n)
            companion=(pi*n+(2*qj+1 if pj==2*qj else 2*qj)) if wi!=qi else ((2*qi+1 if pi==2*qi else 2*qi)*n+pj)
            assert companion not in entry,('leaf-companion conflict',Q,p,companion)
        if r[Q]!=1 or len(leaf_edges)!=2:continue
        assert g['t'][Q]==0 and g['h'][Q]==1 and g['s'][Q]==0 and g['deg'][Q]==2
        assert all(g['A']>>v&1 for v in g['vertices'][Q])
        p=list(entry);a,b=map(lambda v:divmod(v,n),p)
        qi,qj=divmod(Q,nc)
        if a[0]==b[0]:
            assert abs(a[1]-b[1])==1
            delta=(1 if a[0]==2*qi else -1,0)
        else:
            assert a[1]==b[1] and abs(a[0]-b[0])==1
            delta=(0,1 if a[1]==2*qj else -1)
        si,sj=qi+delta[0],qj+delta[1]
        assert 0<=si<g['nr'] and 0<=sj<nc
        S=si*nc+sj;sources[Q]=S;loads[S]+=1
        assert g['t'][S]==0 and g['s'][S]==0 and g['deg'][S]==0 and r[S] in (1,2)
        assert g['h'][S]==2-r[S]
        # The half of S away from Q is blank; the near half is BB or a matched PP pair.
        far=[];near=[]
        for v in g['vertices'][S]:
            vi,vj=divmod(v,n)
            isnear=(vi==(2*si if delta[0]>0 else 2*si+1)) if delta[0] else (vj==(2*sj if delta[1]>0 else 2*sj+1))
            (near if isnear else far).append(v)
        assert all(not(g['A']>>v&1) for v in far)
        occ=[bool(g['A']>>v&1) for v in near];assert occ[0]==occ[1]
        if occ[0]:assert any(set(e)==set(near) for e in g['M'])
    for S,count in loads.items():
        assert count<=r[S]
        src=[Q for Q,P in sources.items() if P==S]
        if len(src)==2:
            si,sj=divmod(S,nc);q1=divmod(src[0],nc);q2=divmod(src[1],nc)
            assert (q1[0]+q2[0],q1[1]+q2[1])==(2*si,2*sj)
            assert r[S]==2 and all(not(g['A']>>v&1) for v in g['vertices'][S])
    return sources

def route(g,rng):
    N=g['N'];local=[[] for _ in range(N)];links={};terminal={};leaf_ports=set()
    def link(a,b,w):
        links.setdefault(a,[]).append((b,w));links.setdefault(b,[]).append((a,w))
    for e,(u,v) in enumerate(g['E']):
        p=(0,e,0);q=(0,e,1);local[u].append(p);local[v].append(q);link(p,q,1)
        if u in g['L']:terminal[p]='L';leaf_ports.add(q)
        if v in g['L']:terminal[q]='L';leaf_ports.add(p)
    for v in range(N):
        rv=g['r'][v]
        if rv==0:continue
        for j in range(2*rv-g['deg'][v]):
            p=(1,v,j);local[v].append(p);terminal[p]='H'
        P=local[v];rng.shuffle(P)
        if rv==1:matching=[(P[0],P[1])]
        else:
            choices=[[(P[0],P[1]),(P[2],P[3])],[(P[0],P[2]),(P[1],P[3])],[(P[0],P[3]),(P[1],P[2])]]
            choices=[x for x in choices if all(not(a in leaf_ports and b in leaf_ports) for a,b in x)]
            assert choices
            matching=rng.choice(choices)
        for a,b in matching:link(a,b,0)
    seen=set();counts=collections.Counter();real_used=0
    for start in terminal:
        if start in seen:continue
        seen.add(start);previous=None;current=start;length=0
        while True:
            choices=[(p,w) for p,w in links[current] if p!=previous]
            assert len(choices)==1
            nxt,w=choices[0];length+=w;previous,current=current,nxt
            assert current not in seen;seen.add(current)
            if current in terminal:break
        kind=''.join(sorted((terminal[start],terminal[current])))
        counts[kind]+=1;real_used+=length
        if kind=='LL':
            assert length>=2
            if length==2:counts['short']+=1
    for start in links:
        if start in seen:continue
        todo=[start];seen.add(start);doubled=0
        while todo:
            p=todo.pop()
            for q,w in links[p]:
                doubled+=w
                if q not in seen:seen.add(q);todo.append(q)
        assert doubled%2==0;real_used+=doubled//2
    a,b,c,f=[counts[k] for k in ('LL','HH','HL','short')]
    q=len(g['E'])-sum(g['r']);D=g['m']*g['n']//2-g['T'].bit_count()
    assert real_used==len(g['E']) and q==a-b
    assert f<=b
    assert D>=4*q+5*b-f+2*c
    assert D>=4*q
    assert 5*g['T'].bit_count()+4*len(g['M'])<=5*g['m']*g['n']//2
    return counts

def normalize(m,n,T,M):
    # Each move strictly decreases the number of matched edges internal
    # to the fixed tile partition and preserves |T|+|M|.
    adj,_=graph(m,n);M=list(M);start=T.bit_count()+len(M);steps=promotions=flips=0
    while True:
        g=residual(m,n,T,tuple(M));sources=check_geometry(g)
        if not sources:break
        Q,S=next(iter(sources.items()));oldh=sum(g['h'])
        qe=next(e for e in M if set(e)<=set(g['vertices'][Q]))
        M.remove(qe)
        if g['r'][S]==2:
            candidates=[v for v in g['vertices'][S] if any(adj[v]>>u&1 for u in qe)]
            assert len(candidates)==2
            T|=1<<candidates[0];promotions+=1
        else:
            se=next(e for e in M if set(e)<=set(g['vertices'][S]));M.remove(se)
            for u in qe:
                matches=[v for v in se if adj[u]>>v&1];assert len(matches)==1
                M.append((u,matches[0]))
            flips+=1
        assert feasible(adj,T,M) and T.bit_count()+len(M)==start
        after=residual(m,n,T,tuple(M));assert sum(after['h'])<oldh
        steps+=1
    return T,tuple(M),dict(steps=steps,promotions=promotions,flips=flips)

def check(m,n,T,M,rng,normal=False):
    g=residual(m,n,T,M);sources=check_geometry(g);ct=route(g,rng)
    assert ct['short']==len(sources)
    out=dict(sources=len(sources),short=ct['short'])
    if normal:
        U,N,record=normalize(m,n,T,M)
        assert U.bit_count()>=T.bit_count() and len(N)<=len(M)
        out.update(record)
    return out

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=Path('short-path-compensation-verification.json'));p.add_argument('--random-per-size',type=int,default=100);args=p.parse_args()
    rng=random.Random(2026092705);report={'scope':'Finite exact regression checks for written lemmas, not a universal or Lean proof.','exhaustive':[]}
    total_sources=0
    for m,n in ((2,2),(2,4),(2,6),(4,4)):
        count=0;src=0
        for T,M in pairs(m,n):
            out=check(m,n,T,M,rng);src+=out['sources'];count+=1
        report['exhaustive'].append(dict(m=m,n=n,pairs=count,short_sources=src));total_sources+=src
        print(report['exhaustive'][-1],flush=True)
    sizes=((4,6),(6,6),(8,10),(12,14),(20,20));randoms=0
    for m,n in sizes:
        adj,edges=graph(m,n)
        for _ in range(args.random_per_size):
            E=edges[:];rng.shuffle(E);A=T=0;M=[];prob=rng.random()*.8
            for u,v in E:
                mask=(1<<u)|(1<<v)
                if not(A&mask) and rng.random()<prob:A|=mask;M.append((u,v))
            order=list(range(m*n));rng.shuffle(order)
            for v in order:
                bit=1<<v
                if not(A&bit) and (adj[v]&A).bit_count()<=1 and all((adj[w]&A).bit_count()==0 for w in bits(adj[v]&T)):
                    T|=bit;A|=bit
            check(m,n,T,tuple(M),rng,normal=True);randoms+=1
    # Real short-path examples with the blank and internally matched compensator.
    T=sum(1<<v for v in (0,5,12,17,19,22))
    M=((1,2),(3,4),(7,13),(10,16),(8,9))
    witnesses=[]
    for extra in ((),((14,15),)):
        edges=M+extra
        assert feasible(graph(4,6)[0],T,edges)
        out=check(4,6,T,edges,rng,normal=True)
        witnesses.append(dict(T=list(bits(T)),M=edges,result=out))
    assert witnesses[0]['result']['promotions']==1 and witnesses[1]['result']['flips']==1
    report['random']=dict(seed=2026092705,sizes=sizes,pairs=randoms)
    report['normalization_witnesses']=witnesses
    report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest();report['result']='ALL_LISTED_CHECKS_PASSED'
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report),flush=True)
if __name__=='__main__':main()
