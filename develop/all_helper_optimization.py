"""Exact, exponential all-helper optimization through bipartite matching."""
from collections import deque


def score(n, pairs, Q, U):
    """Maximum independent set of (P union Q)[U] and a maximum matching."""
    U=set(U);adj={v:set() for v in U}
    for a,b in list(pairs)+list(Q):
        if a in U and b in U:adj[a].add(b);adj[b].add(a)
    colour={}
    for root in sorted(U):
        if root in colour:continue
        colour[root]=0;todo=[root]
        while todo:
            v=todo.pop()
            for u in sorted(adj[v]):
                if u in colour:
                    if colour[u]==colour[v]:raise ValueError('P union Q must be bipartite')
                else:colour[u]=1-colour[v];todo.append(u)
    left={v for v in U if not colour[v]};mate={}
    def aug(v,seen):
        for u in sorted(adj[v]):
            if u in seen:continue
            seen.add(u)
            if u not in mate or aug(mate[u],seen):mate[u]=v;return True
        return False
    for v in sorted(left):aug(v,set())
    inverse={v:u for u,v in mate.items()}
    reached=set(left-set(inverse));queue=deque(sorted(reached))
    while queue:
        v=queue.popleft()
        if v in left:
            for u in adj[v]:
                if inverse.get(v)!=u and u not in reached:reached.add(u);queue.append(u)
        elif v in mate and mate[v] not in reached:reached.add(mate[v]);queue.append(mate[v])
    independent=(left&reached)|((U-left)-reached)
    return independent,sorted((v,u) for u,v in mate.items())


def solve(b,pairs,Q,core):
    """Return exact beta_I plus owner/witness selections; enumerates all2^(2b) U."""
    n=2*b
    if b<0 or sorted(v for p in pairs for v in p)!=list(range(n)):
        raise ValueError('P must partition the2b witness indices')
    if any(a==c or a<0 or c<0 or a>=n or c>=n for a,c in list(Q)+list(core)):
        raise ValueError('Invalid index edge')
    if len({v for edge in Q for v in edge})!=2*len(Q):
        raise ValueError('Q must be a matching')
    best=None
    for mask in range(1<<n):
        U={v for v in range(n) if mask>>v&1};S=set(range(n))-U
        degrees={v:0 for v in S}
        for a,c in core:
            if a in S and c in S:degrees[a]+=1;degrees[c]+=1
        if any(d>1 for d in degrees.values()):continue
        T,M=score(n,pairs,Q,U)
        record={'beta_I':b+len(S)+len(T),'owners':sorted(S),'witnesses':sorted(T),'U':sorted(U),'matching':[list(e) for e in M]}
        if best is None or record['beta_I']>best['beta_I']:best=record
    return best


def path_cycle_owner_set(vertices, core):
    """Dissociation certificate for paths and cycles of length divisible by six."""
    remaining=set(vertices);adj={v:set() for v in remaining}
    for a,b in core:
        if a==b or a not in adj or b not in adj:
            raise ValueError('Use a finite simple owner graph on the given vertices')
        adj[a].add(b);adj[b].add(a)
    if any(len(ns)>2 for ns in adj.values()):
        raise ValueError('Owner components must be paths or cycles of length6k')
    selected=set();orders=[]
    while remaining:
        root=min(remaining);block={root};todo=[root]
        while todo:
            for u in adj[todo.pop()]-block:
                block.add(u);todo.append(u)
        ends=sorted(v for v in block if len(adj[v])<2)
        cyclic=not ends
        if cyclic and len(block)%6:
            raise ValueError('A cycle must have length divisible by six')
        start=ends[0] if ends else min(block)
        order=[];v=start;previous=None
        while v not in order:
            order.append(v);choices=sorted(adj[v]-({previous} if previous is not None else set()))
            if not choices:break
            previous,v=v,choices[0]
        assert set(order)==block
        selected.update(v for j,v in enumerate(order) if j%3!=2)
        orders.append({'vertices':order,'cyclic':cyclic})
        remaining-=block
    assert 3*len(selected)>=2*len(adj)
    assert all(len(adj[v]&selected)<=1 for v in selected)
    return selected,orders


def template_certificate(m):
    """Polynomial physical certificate for the hereditary path/6k owner class."""
    g,C,X,I=(m[k] for k in ('g','C','X','I'))
    order=sorted(X);index={x:j for j,x in enumerate(order)}
    inverse={c:x for x,c in m['owner'].items()}
    core=[(v,u) for v in C for u in g[v]&C if v<u]
    selected,components=path_cycle_owner_set(C,core)
    pairs=[tuple(index[x] for x in sorted(g[i]&X)) for i in sorted(I)]
    Q=[(index[x],index[y]) for x in X for y in g[x]&X if x<y]
    U={index[inverse[c]] for c in C-selected}
    witnesses,matching=score(len(X),pairs,Q,U)
    D=set(I)|selected|{order[j] for j in witnesses}
    assert len(C)==len(X)==2*len(I)
    assert all(len(g[v]&D)<=1 for v in D)
    assert len(D)>=2*len(I)+(len(selected)+1)//2 >=(8*len(I)+2)//3
    return D,dict(owner_set=selected,components=components,matching=matching)


def lift_certificate(g,S,w,beta):
    """Use the fixed witness ledger and a path/6k extracted owner core."""
    m=dict(g=g,C=w['C0'],I=w['I0'],X=w['X0'],owner=w['owner'])
    inner,data=template_certificate(m)
    retained=(w['R']-w['I0'])|{ell for c,ell,x in w['triples']}
    assert not retained&inner and all(not g[v]&inner for v in retained)
    D=inner|retained
    assert all(len(g[v]&D)<=1 for v in D) and len(D)<=beta
    p,u=len(w['triples']),len(w['pairs'])
    a,b,b3=w['a'],w['b'],w['b3'];minimum=min(a,p)
    alpha,pi=a-minimum,p-minimum
    e,r=u-a-2*b,len(w['R'])-a-b
    q,d=len(g)-len(S)-p-u,len(S)-beta
    tau=minimum+b-2*d;L,bp=len(retained),len(w['I0'])
    Z=3*beta-3*L-8*bp
    terms=[Z,5*r,12*(alpha+pi),24*tau,7*(e-b3),2*b3,5*q]
    assert all(t>=0 for t in terms) and sum(terms)==5*len(g)-51*d
    return D,dict(template=data,inner=inner,retained=retained,Z=Z,
                  d=d,bprime=bp,L=L,nonnegative_terms=terms)
