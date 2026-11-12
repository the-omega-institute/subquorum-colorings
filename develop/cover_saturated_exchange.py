"""Exact cover-saturated deletion and coordinated physical owner exchanges.

The cover condition characterizes one saved matching edge per deletion.
Final isolation permits dependencies among additions and simultaneous removals.
No optimization over all owner exchanges is claimed.
"""
from all_helper_optimization import score
from owner_matching_certificate import prepare
from mixed_owner_bridges import _permitted


def forced_minimum_cover(n, edges, U, X):
    """Return a minimum cover containing X iff nu(G-X)=nu(G)-|X|.

    G is the bipartite induced graph on U. Edges may be a one-pass iterable.
    A failed criterion certifies failure of this exact deletion rule only.
    """
    edges=list(edges);U=set(U);X=set(X);V=set(range(n))
    if not X<=U<=V or any(a not in V or b not in V or a==b for a,b in edges):
        raise ValueError('Use X subset U on a simple indexed graph')
    T,M=score(n,edges,[],U)
    T0,M0=score(n,edges,[],U-X)
    nu=len(M);remaining=len(M0)
    if remaining!=nu-len(X):
        return dict(applicable=False,initial_cost=nu,deletion_cost=remaining,
                    removed=sorted(X),reason='no minimum vertex cover contains X')
    C=X|((U-X)-T0)
    assert len(C)==nu and all(a in C or b in C for a,b in edges if a in U and b in U)
    return dict(applicable=True,cover=sorted(C),initial_cost=nu,
                deletion_cost=remaining,matching=[list(e) for e in M])


def coordinated_exchange(b,P,Q,B,colour,U,operations,cover=None):
    """Construct a primal/dual physical certificate, without a final matching solve.

    An operation is (owner_component_id, removed_x, added_y). There is at most
    one per owner component. Each is locally permitted. All additions must be
    isolated in the FINAL induced graph, but may be adjacent to removed points.
    Supply any minimum cover containing all removed points, or find one exactly.
    """
    data=prepare(b,P,Q,B,colour);n=2*b;V=set(range(n));U=set(U)
    if not U<=V or not _permitted(n,data['B'],U):
        raise ValueError('Initial omission set must be permitted')
    operations=[tuple(op) for op in operations];owners=data['owner_components']
    X=set();Y=set();used=set()
    for i,x,y in operations:
        if i not in range(len(owners)) or i in used:
            return dict(applicable=False,reason='operations need distinct owner components')
        C=set(owners[i][0])
        if x not in U&C or y not in C-U:
            return dict(applicable=False,reason='operation must replace x in U by y outside U in its owner')
        if not _permitted(n,data['B'],(U-{x})|{y}):
            return dict(applicable=False,reason='individual owner replacement is not permitted')
        X.add(x);Y.add(y);used.add(i)
    E=data['P']+data['Q'];new=(U-X)|Y
    if any((a in Y and c in new) or (c in Y and a in new) for a,c in E):
        return dict(applicable=False,reason='an addition is not isolated after the batch')
    T,M=score(n,data['P'],data['Q'],U);nu=len(M)
    if cover is None:
        rec=forced_minimum_cover(n,E,U,X)
        if not rec['applicable']:return rec
        C=set(rec['cover'])
    else:C=set(cover)
    if not X<=C<=U or len(C)!=nu or any(a not in C and c not in C for a,c in E if a in U and c in U):
        return dict(applicable=False,reason='supplied cover is not a minimum cover containing X')
    # A maximum matching uses exactly one C vertex per edge and saturates C.
    assert all(len(set(e)&C)==1 for e in M)
    incident={v:tuple(sorted(e)) for e in M for v in set(e)&C}
    assert set(incident)==C
    charged=[dict(removed=x,edge=list(incident[x])) for x in sorted(X)]
    assert len({tuple(r['edge']) for r in charged})==len(X)
    remaining=[list(e) for e in M if not set(e)&X];final_cover=C-X
    witnesses=new-final_cover;actual_cost=nu-len(X)
    assert len(remaining)==len(final_cover)==actual_cost
    assert all(set(e)<=new for e in remaining)
    assert all(a in final_cover or c in final_cover for a,c in E if a in new and c in new)
    assert _permitted(n,data['B'],new) and len(new)==len(U)
    assert len(witnesses)==len(new)-actual_cost
    return dict(applicable=True,initial_U=sorted(U),initial_cost=nu,
                initial_cover=sorted(C),initial_matching=[list(e) for e in M],
                operations=[list(op) for op in operations],removed=sorted(X),added=sorted(Y),
                charged_edges=charged,U=sorted(new),matching=remaining,cover=sorted(final_cover),
                witnesses=sorted(witnesses),owners=sorted(V-new),actual_cost=actual_cost,
                beta_I_lower=3*b-actual_cost,saved_matching_edges=len(X))


def dependency_batch(b,P,Q,B,colour,U,operations,cover):
    """Largest isolation-compatible batch in a fixed-cover candidate list.

    Candidates use distinct owners, remove from the supplied minimum cover,
    are individually owner-permitted, and have pairwise nonadjacent additions.
    Dependency i->j means addition i needs removal j. A permanent blocker is
    an initial neighbour with no candidate removal. Discard blockers and every
    predecessor reaching them; all remaining candidates form the unique largest
    closed feasible batch. This is not optimization over arbitrary replacements.
    """
    data=prepare(b,P,Q,B,colour);n=2*b;U=set(U);C=set(cover)
    if not U<=set(range(n)) or not _permitted(n,data['B'],U):
        raise ValueError('Initial omission set must be permitted')
    operations=[tuple(op) for op in operations];owners=data['owner_components']
    E=data['P']+data['Q'];T,M=score(n,data['P'],data['Q'],U)
    if not C<=U or len(C)!=len(M) or any(a not in C and c not in C for a,c in E if a in U and c in U):
        raise ValueError('Supply a minimum vertex cover of the initial graph')
    used=set();removal={};Y=set()
    for j,(i,x,y) in enumerate(operations):
        if i not in range(len(owners)) or i in used:
            raise ValueError('Candidates must use distinct owner components')
        K=set(owners[i][0])
        if x not in C&K or y not in K-U or not _permitted(n,data['B'],(U-{x})|{y}):
            raise ValueError('Each candidate must be a permitted within-owner replacement from the cover')
        used.add(i);removal[x]=j;Y.add(y)
    if any(a in Y and c in Y for a,c in E):
        raise ValueError('Candidate additions must be independent')
    adj={v:set() for v in range(n)}
    for a,c in E:adj[a].add(c);adj[c].add(a)
    dependencies=[];blockers=[];reverse=[set() for _ in operations]
    for i,(_,x,y) in enumerate(operations):
        for v in sorted(adj[y]&U):
            if v in removal:
                j=removal[v];dependencies.append([i,j]);reverse[j].add(i)
            else:blockers.append([i,v])
    excluded={i for i,v in blockers};todo=sorted(excluded)
    while todo:
        j=todo.pop()
        for i in sorted(reverse[j]-excluded):excluded.add(i);todo.append(i)
    selected=sorted(set(range(len(operations)))-excluded)
    certificate=coordinated_exchange(b,P,Q,B,colour,U,[operations[i] for i in selected],C)
    assert certificate['applicable'] and certificate['saved_matching_edges']==len(selected)
    return dict(selected_candidates=selected,excluded_candidates=sorted(excluded),
                dependencies=dependencies,permanent_blockers=blockers,certificate=certificate)


def cyclic_dependency_family(r):
    """Every r>=3: one closed cyclic batch saves r, physical order10r."""
    if not isinstance(r,int) or isinstance(r,bool) or r<3:
        raise ValueError('Use integer r>=3')
    n=4*r;P=[(v,v+1) for v in range(0,n,2)]
    Q=[(v,(v+1)%n) for v in range(1,n,2)];B=[];Cs=[]
    for i in range(r):
        j=(i+1)%r;C=[4*i+1,4*j+2,4*i,4*j+3];Cs.append(C)
        B+=list(zip(C,C[1:]+C[:1]))
    colour=[(v//2)%2 for v in range(n)];b=2*r
    data=prepare(b,P,Q,B,colour)
    ids={frozenset(C):i for i,(C,_) in enumerate(data['owner_components'])}
    return dict(b=b,P=P,Q=Q,B=B,colour=colour,r=r,
                initial_U=[v for v in range(n) if v%4 in (0,1)],
                cover=[4*i+1 for i in range(r)],
                operations=[[ids[frozenset(Cs[i])],4*i+1,4*((i+1)%r)+2] for i in range(r)],
                natural_owner_sets=Cs)


def shared_odd_path_family(r):
    """Even r>=4: r-2 savings in one shared odd base component."""
    from omission_conflict_graph import shared_even_path_family
    if not isinstance(r,int) or isinstance(r,bool) or r<4 or r%2:
        raise ValueError('Use even integer r>=4')
    x=shared_even_path_family(r)
    data=prepare(*(x[k] for k in ('b','P','Q','B','colour')))
    ids={v:i for i,(C,_) in enumerate(data['owner_components']) for v in C}
    x['initial_U']=list(range(1,2*r))+[2*r+2]
    x['cover']=list(range(2,2*r,2))
    x['operations']=[[ids[2*j],2*j,2*r+2*(j^1)] for j in range(2,r)]
    return x
