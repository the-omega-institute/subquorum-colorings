"""Finite boundary tests for non-induced k-star formation, arbitrary k>=1."""

def validate(adj,k):
    if type(k) is not int or k<1:raise ValueError('k must be a positive integer')
    V=set(range(len(adj)))
    if any(v in adj[v] or not set(adj[v])<=V for v in V):raise ValueError('simple graph required')
    if any(v not in adj[u] for v in V for u in adj[v]):raise ValueError('undirected graph required')
    return V


def forms(adj,C,k):
    V=validate(adj,k);C=set(C)
    if not C<=V:raise ValueError('selected vertices outside graph')
    return all(len(adj[x]&C)>=k or any(len(adj[y]&C)>=k-1 for y in adj[x]&C)
               for x in V-C)


def admissible(adj,P,C,k):
    """Exactly the selected intersections realizable in some ambient extension."""
    V=validate(adj,k);P=set(P);C=set(C)
    if not P|C<=V:raise ValueError('invalid block subset')
    return all(len(adj[x]&C)>=k or any(y in P or len(adj[y]&C)>=k-1
                                      for y in adj[x]&C) for x in V-(C|P))


def signature(adj,P,C,k):
    V=validate(adj,k);P=set(P);C=set(C)
    if not P|C<=V:raise ValueError('invalid block subset')
    return {p:min(k-1,len(adj[p]&C)) for p in sorted(P&C)}


def safe_internal_deletion(adj,P,C,D,k):
    """Exact universal criterion under the explicit internal-formation premise.

    D must be selected and disjoint from P. If C-D forms the block, deletion
    is safe in every forming ambient extension iff the truncated signature
    is unchanged. This function includes that internal-formation premise.
    """
    validate(adj,k);P=set(P);C=set(C);D=set(D)
    if not D<=C-P:raise ValueError('only selected nonports may be deleted')
    return forms(adj,C-D,k) and signature(adj,P,C,k)==signature(adj,P,C-D,k)


def saturate_ports(adj,P,C,k):
    """Canonical realization with at most k shared selected external vertices."""
    V=validate(adj,k);P=set(P);C=set(C)
    if not P|C<=V:raise ValueError('invalid block subset')
    graph=[set(z) for z in adj];S=set(C);added=set()
    if P:
        added=set(range(len(graph),len(graph)+k))
        graph.extend(set(P) for _ in range(k))
        for p in P:graph[p]|=added
        S|=added
    return graph,S,dict(new_vertices=sorted(added),ports=sorted(P))


def saturate_bipartite_ports(adj,P,C,k,colour):
    """The same canonical realization within a fixed proper bipartition."""
    V=validate(adj,k);P=set(P);C=set(C)
    if len(colour)!=len(adj) or any(c not in (0,1) for c in colour):raise ValueError('binary colouring required')
    if not P|C<=V or any(colour[a]==colour[b] for a in V for b in adj[a]):raise ValueError('proper bipartition required')
    graph=[set(z) for z in adj];S=set(C);col=list(colour);added=[]
    for c in (0,1):
        ports={p for p in P if colour[p]==c}
        if not ports:continue
        new=set(range(len(graph),len(graph)+k));graph.extend(set(ports) for _ in range(k));col.extend([1-c]*k)
        for p in ports:graph[p]|=new
        S|=new;added+=sorted(new)
    return graph,S,dict(new_vertices=added,colour=col)


def protected_witnesses(adj,P,C,v,k):
    """Exactly the failures surviving EVERY forming ambient extension of C.

    The universal-essentiality equivalence requires admissible(P,C); without
    it there need not be any forming ambient extension at all.
    """
    V=validate(adj,k);P=set(P);C=set(C)
    if v not in C or not P|C<=V:raise ValueError('invalid selected vertex or ports')
    Cv=C-{v}
    return [x for x in sorted(V-(Cv|P))
            if len(adj[x]&Cv)<k and not adj[x]&Cv&P
            and all(len(adj[y]&Cv)<k-1 for y in adj[x]&Cv)]


def loss_obstruction(adj,P,C,D,k):
    """An actual ambient graph refuting safety when truncated capacity drops.

    Requires C-D to form the block and some selected port signature to drop.
    Returns a forming selection whose D-deletion fails at the new leaf x.
    """
    validate(adj,k);P=set(P);C=set(C);D=set(D)
    if not D<=C-P or not forms(adj,C-D,k):raise ValueError('internal premise required')
    before=signature(adj,P,C,k);after=signature(adj,P,C-D,k)
    p=next((p for p in sorted(before) if before[p]>after[p]),None)
    if p is None:raise ValueError('no truncated-capacity loss')
    h=max(0,k-1-len(adj[p]&C));graph=[set(z) for z in adj];S=set(C)
    for _ in range(h):
        u=len(graph);graph.append({p});graph[p].add(u);S.add(u)
    x=len(graph);graph.append({p});graph[p].add(x)
    assert forms(graph,S,k) and not forms(graph,S-D,k)
    return dict(graph=graph,selected=S,deleted=D,port=p,failure=x,selected_leaves=h,
                signature_before=before,signature_after=after)


def activity_counterexample(k):
    """For every k>=3, boolean activity survives but k-star coverage fails."""
    if type(k) is not int or k<3:raise ValueError('k>=3 required')
    n=2*k;adj=[set() for _ in range(n)];p=0;v=1;x=n-1
    edges=[(p,v),(p,x)]+[(p,a) for a in range(2,k)]+[(v,b) for b in range(k,n-1)]
    for a,b in edges:adj[a].add(b);adj[b].add(a)
    C=set(range(n-1));assert forms(adj,C,k) and not forms(adj,C-{v},k)
    block=[z-{x} for z in adj[:-1]]
    assert forms(block,C-{v},k) and adj[p]&C and adj[p]&(C-{v})
    return dict(k=k,graph=adj,block_order=n-1,ports={p},selected=C,deleted={v},failure=x)


def sharp_extension_order(k):
    """k-1 added vertices are necessary and sufficient to refute safety here."""
    if type(k) is not int or k<2:raise ValueError('k>=2 required')
    block=[set() for _ in range(k+1)]
    for u in range(k+1):
        if u!=1:block[1].add(u);block[u].add(1)
    P={0};C=set(range(k+1));D={1}
    rec=loss_obstruction(block,P,C,D,k)
    assert len(rec['graph'])-len(block)==k-1 and rec['selected_leaves']==k-2
    return dict(block=block,ports=P,selected=C,deleted=D,obstruction=rec)
