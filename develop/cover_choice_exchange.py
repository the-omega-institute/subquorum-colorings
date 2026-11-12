"""Exact enumeration of minimum covers and the best specified exchange batch.

The cover enumeration is generally exponential. Each fixed-cover closure is
polynomial. Completeness is for the listed owner operations with independent
additions and the final-isolation, exact-deletion rule, not arbitrary exchanges.
"""
from itertools import product
from cover_saturated_exchange import dependency_batch
from owner_matching_certificate import prepare
from mixed_owner_bridges import _permitted


def minimum_covers(n,edges,U):
    """Yield every minimum cover of a bipartite maxdegree2 induced graph once."""
    U=set(U);V=set(range(n));edges=list(edges)
    if not U<=V or any(a not in V or b not in V or a==b for a,b in edges):
        raise ValueError('Use a simple indexed graph and U subset V')
    adj={v:set() for v in U}
    for a,b in edges:
        if a in U and b in U:adj[a].add(b);adj[b].add(a)
    if any(len(N)>2 for N in adj.values()):raise ValueError('Maximum induced degree must be2')
    unseen=set(U);choices=[]
    while unseen:
        root=min(unseen);K={root};todo=[root]
        while todo:
            for v in adj[todo.pop()]-K:K.add(v);todo.append(v)
        unseen-=K;ends=sorted(v for v in K if len(adj[v])<2);cyclic=not ends
        order=[];previous=None;v=ends[0] if ends else min(K)
        while v not in order:
            order.append(v);following=sorted(adj[v]-({previous} if previous is not None else set()))
            if not following:break
            previous,v=v,following[0]
        assert set(order)==K
        k=len(order)//2
        if cyclic:
            if len(order)%2:raise ValueError('Induced graph must be bipartite')
            choices.append([set(order[::2]),set(order[1::2])])
        elif len(order)%2:
            choices.append([set(order[1::2])])
        else:
            choices.append([{order[2*j+1] for j in range(t)}|{order[2*j] for j in range(t,k)} for t in range(k+1)])
    for covers in product(*choices):yield set().union(*covers)


def best_cover_batch(b,P,Q,B,colour,U,operations):
    """Best final-isolating exact-deletion batch over ALL minimum covers.

    Operations are fixed, one per owner, locally permitted; additions must
    be pairwise independent. Enumerates covers, filters removals not in each
    cover, then applies the fixed-cover dependency closure. No polynomial
    worst-case runtime claim is made for cover enumeration.
    """
    data=prepare(b,P,Q,B,colour);n=2*b;U=set(U)
    if not U<=set(range(n)) or not _permitted(n,data['B'],U):
        raise ValueError('Initial omission set must be permitted')
    operations=[tuple(op) for op in operations];owners=data['owner_components'];used=set();Y=set()
    for i,x,y in operations:
        if i not in range(len(owners)) or i in used:
            raise ValueError('Candidates must use distinct owner components')
        K=set(owners[i][0])
        if x not in U&K or y not in K-U or not _permitted(n,data['B'],(U-{x})|{y}):
            raise ValueError('Each candidate must be a permitted within-owner replacement')
        used.add(i);Y.add(y)
    E=data['P']+data['Q']
    if any(a in Y and c in Y for a,c in E):raise ValueError('Candidate additions must be independent')
    best=None;count=0
    for C in minimum_covers(n,E,U):
        ids=[i for i,(_,x,_) in enumerate(operations) if x in C]
        trial=dependency_batch(b,P,Q,B,colour,U,[operations[i] for i in ids],C);count+=1
        selected=[ids[i] for i in trial['selected_candidates']]
        if best is None or len(selected)>len(best['selected_candidates']):
            best=dict(selected_candidates=selected,cover=sorted(C),fixed_cover_result=trial,
                      certificate=trial['certificate'])
    assert best is not None
    return dict(minimum_covers_tested=count,**best)
