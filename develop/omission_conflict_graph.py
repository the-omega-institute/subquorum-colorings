"""Pair conflicts and exact optimization scope of the activation budget."""
from owner_matching_certificate import prepare
from mixed_owner_bridges import _minimum_omission,_permitted
from activated_omission_budget import activated_budget


def induced_components(vertices,edges):
    vertices=set(vertices);adj={v:set() for v in vertices}
    for a,c in edges:
        if a in adj and c in adj:adj[a].add(c);adj[c].add(a)
    remaining=set(vertices);answer=[]
    while remaining:
        K={min(remaining)};todo=list(K)
        while todo:
            for v in sorted(adj[todo.pop()]-K):K.add(v);todo.append(v)
        answer.append(K);remaining-=K
    return answer


def pair_conflicts(n,edges,U,sets):
    """Exact conflict graph for disjoint candidate sets in any simple graph.

    A conflict means a component of A[U union C_i union C_j] touches both.
    Regions are computed individually; overlap or an edge between them is
    equivalent to this pair condition. No matching assumptions are used here.
    """
    edges=list(edges)
    V=set(range(n));U=set(U);sets=[set(C) for C in sets];used=set()
    assert U<=V and all(a in V and c in V and a!=c for a,c in edges)
    for C in sets:
        assert C and C<=V and not C&used;used|=C
    regions=[]
    for C in sets:
        Ks=induced_components(U|C,edges)
        regions.append(set().union(*(K for K in Ks if K&C)))
    conflicts=[]
    for i,R in enumerate(regions):
        for j in range(i+1,len(regions)):
            S=regions[j]
            if R&S or any((a in R and c in S) or (a in S and c in R) for a,c in edges):
                conflicts.append([i,j])
    return dict(regions=[sorted(R) for R in regions],edges=conflicts)


def conflict_data(b,P,Q,B,colour,U=None):
    """All initially minimum exceptional cycles, their parity penalties and graph."""
    d=prepare(b,P,Q,B,colour);n=2*b;owners=d['owner_components'];E=d['P']+d['Q']
    if U is None:U=set().union(*(_minimum_omission(C,c) for C,c in owners)) if owners else set()
    else:U=set(U)
    assert U<=set(range(n)) and _permitted(n,B,U)
    base=induced_components(U,E);nu0=sum(len(K)//2 for K in base)
    ids=[i for i,(C,c) in enumerate(owners) if c and len(C)%6 and len(U&set(C))==(len(C)+2)//3]
    sets=[set(owners[i][0]) for i in ids];g=pair_conflicts(n,E,U,sets);records=[]
    for i,C,R in zip(ids,sets,g['regions']):
        R=set(R);Ks=induced_components(U|C,E)
        odd=[j for j,K in enumerate(base) if K&R and len(K)%2]
        eligible=all(len(K&U)%2==0 for K in Ks if K&C)
        if eligible:assert len(odd)%2==0
        records.append(dict(cycle=i,vertices=sorted(C),region=sorted(R),
                            individually_eligible=eligible,odd_base_components=odd,
                            penalty_d=len(odd),good=not odd))
        assert odd or eligible
    good=[j for j,r in enumerate(records) if r['good']]
    return dict(initial_U=sorted(U),initial_cost=nu0,base_components=[sorted(K) for K in base],
                candidates=records,conflicts=g['edges'],good=good)


def greedy_conflict_certificate(b,P,Q,B,colour,U=None):
    """Polynomial (Delta+1)-colour selection, not a maximum-independent-set solver."""
    data=conflict_data(b,P,Q,B,colour,U);good=data['good'];adj={j:set() for j in good}
    for i,j in data['conflicts']:
        if i in adj and j in adj:adj[i].add(j);adj[j].add(i)
    colours={};classes=[]
    for v in good:
        unavailable={colours[u] for u in adj[v] if u in colours};c=0
        while c in unavailable:c+=1
        colours[v]=c
        while len(classes)<=c:classes.append([])
        classes[c].append(v)
    chosen=max(classes,key=len) if classes else []
    delta=max(map(len,adj.values()),default=0)
    guaranteed=(len(good)+delta)//(delta+1) if good else 0
    assert len(chosen)>=guaranteed
    cycles=[data['candidates'][j]['cycle'] for j in chosen]
    certificate=activated_budget(b,P,Q,B,colour,cycles,U=data['initial_U'])
    assert certificate['cost_upper_bound']==data['initial_cost']-len(chosen)
    return dict(data=data,colours=[[v,colours[v]] for v in good],colour_classes=classes,
                maximum_degree=delta,guaranteed_savings=guaranteed,
                selected_candidates=chosen,certificate=certificate)


def shared_even_path_family(r):
    """Even r>=2: 2-connected10r vertices, conflict K_r, true cost0."""
    assert isinstance(r,int) and not isinstance(r,bool) and r>=2 and r%2==0
    n=4*r;P=[(v,v+1) for v in range(0,n,2)]
    Q=[(v,(v+1)%n) for v in range(1,n,2)];B=[]
    for i in range(r):
        j=i^1;C=[2*i,2*r+2*j,2*i+1,2*r+2*j+1]
        B+=list(zip(C,C[1:]+C[:1]))
    return dict(b=2*r,P=P,Q=Q,B=B,colour=[(v//2)%2 for v in range(n)],r=r,
                initial_U=list(range(2*r)),zero_cost_U=list(range(0,n,2)))
