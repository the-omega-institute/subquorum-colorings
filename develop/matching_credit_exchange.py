"""Matching-owned credits, neutral deletions, dependencies and conflicts.

Fix an initial matching/cover pair of equal size. Removals are outside the
cover; each matched removal retires its distinct cover mate and earns one
credit. Unmatched removals earn zero. The surviving matching and inherited
cover certify exact final cost when the compiled conditions hold.
"""
from all_helper_optimization import score
from owner_matching_certificate import prepare
from mixed_owner_bridges import _permitted


def credit_constraints(n,edges,U,cover,matching,operations):
    """Compile exact conditions for the inherited cover after specified swaps.

    Generic indexed graph, supplied tight matching/cover certificates on U.
    Operations are distinct removals outside the cover and additions outside U.
    No bipartiteness is needed beyond the supplied matching/cover equality.
    """
    if not isinstance(n,int) or n<0:raise ValueError('Use a nonnegative indexed order')
    V=set(range(n));U=set(U);C=set(cover);E=sorted({tuple(sorted(e)) for e in edges})
    M=[tuple(sorted(e)) for e in matching];operations=[tuple(op) for op in operations]
    if not C<=U<=V or any(a not in V or b not in V or a==b for a,b in E):
        raise ValueError('Use a simple indexed graph and cover subset U')
    if len(M)!=len(C) or len({v for e in M for v in e})!=2*len(M) or any(e not in E or not set(e)<=U for e in M):
        raise ValueError('Supply a matching on U of the same size as the cover')
    if any(a not in C and b not in C for a,b in E if a in U and b in U):
        raise ValueError('Supplied cover misses an initial edge')
    assert all(len(set(e)&C)==1 for e in M)
    mate={v:w for a,b in M for v,w in ((a,b),(b,a))}
    if len({x for x,y in operations})!=len(operations) or len({y for x,y in operations})!=len(operations):
        raise ValueError('Removal and addition points must each be distinct')
    if any(x not in U-C or y not in V-U for x,y in operations):
        raise ValueError('Remove outside the initial cover; add outside U')
    removal={x:i for i,(x,y) in enumerate(operations)};addition={y:i for i,(x,y) in enumerate(operations)}
    trigger={mate[x]:i for i,(x,y) in enumerate(operations) if x in mate}
    weights=[int(x in mate) for x,y in operations];dependencies=set();conflicts=set();blockers=[]
    def require(i,v,edge):
        if v in removal:dependencies.add((i,removal[v]))
        else:blockers.append(dict(candidate=i,kind='required removal unavailable',edge=list(edge),vertex=v))
    def conflict(i,j,edge):
        if i==j:blockers.append(dict(candidate=i,kind='self conflict',edge=list(edge)))
        else:conflicts.add(tuple(sorted((i,j))))
    for a,b in E:
        if a in U and b in U:
            if a in C and b in C:
                if a in trigger and b in trigger:conflict(trigger[a],trigger[b],(a,b))
            elif a in C:
                if a in trigger:require(trigger[a],b,(a,b))
            else:
                assert b in C
                if b in trigger:require(trigger[b],a,(a,b))
        elif a in addition and b in addition:
            conflict(addition[a],addition[b],(a,b))
        else:
            for y,v in ((a,b),(b,a)):
                if y not in addition or v not in U:continue
                i=addition[y]
                if v in C:
                    if v in trigger:conflict(i,trigger[v],(a,b))
                else:require(i,v,(a,b))
    return dict(weights=weights,dependencies=[list(e) for e in sorted(dependencies)],
                conflicts=[list(e) for e in sorted(conflicts)],
                blocked=sorted({r['candidate'] for r in blockers}),blocker_evidence=blockers,
                retirement_triggers=[[c,trigger[c]] for c in sorted(trigger)],
                operations=[list(op) for op in operations])


def closed_conflict_optimum(weights,dependencies,conflicts,blocked=(),vertex_cover=None):
    """Maximum nonnegative credit, then fewest operations, in a closed batch.

    Enumerate the chosen part of a conflict-graph vertex cover K, 2^|K| cases.
    Outside K there are no conflicts. Exclude forced conflicts and blockers,
    propagate exclusion backwards, then trim to the dependency closure of all
    positive-credit surviving labels and the chosen K labels. No MIS oracle.
    """
    weights=list(weights);n=len(weights);V=set(range(n));D=sorted(set(map(tuple,dependencies)))
    F=sorted({tuple(sorted(e)) for e in conflicts});blocked=set(blocked)
    if any(not isinstance(w,int) or w<0 for w in weights):raise ValueError('Credits must be nonnegative integers')
    if not blocked<=V or any(a not in V or b not in V for a,b in D+F) or any(a==b for a,b in F):
        raise ValueError('Use indexed implications and loop-free conflicts')
    if vertex_cover is None:
        K=set()
        for a,b in F:
            if a not in K and b not in K:K|={a,b}
    else:K=set(vertex_cover)
    if not K<=V or any(a not in K and b not in K for a,b in F):
        raise ValueError('Supply a vertex cover of the conflict graph')
    K=sorted(K);forward=[set() for _ in V];reverse=[set() for _ in V];adj=[set() for _ in V]
    for a,b in D:forward[a].add(b);reverse[b].add(a)
    for a,b in F:adj[a].add(b);adj[b].add(a)
    best=None;feasible=0
    for mask in range(1<<len(K)):
        chosen={v for i,v in enumerate(K) if mask>>i&1}
        if any(a in chosen and b in chosen for a,b in F):continue
        excluded=blocked|(set(K)-chosen)|{v for i in chosen for v in adj[i]};todo=sorted(excluded)
        while todo:
            j=todo.pop()
            for i in sorted(reverse[j]-excluded):excluded.add(i);todo.append(i)
        if chosen&excluded:continue
        greatest=V-excluded;value=sum(weights[i] for i in greatest);feasible+=1
        selected=chosen|{i for i in greatest if weights[i]>0};todo=sorted(selected)
        while todo:
            i=todo.pop()
            for j in sorted(forward[i]-selected):selected.add(j);todo.append(j)
        assert selected<=greatest and not selected&blocked
        assert all(a not in selected or b in selected for a,b in D)
        assert not any(a in selected and b in selected for a,b in F)
        assert sum(weights[i] for i in selected)==value
        if best is None or value>best['credit'] or (value==best['credit'] and len(selected)<len(best['selected'])):
            best=dict(credit=value,selected=sorted(selected),greatest_for_assignment=sorted(greatest),chosen_cover_labels=sorted(chosen))
    assert best is not None
    return dict(vertex_cover=K,assignments=1<<len(K),feasible_assignments=feasible,**best)


def matching_credit_batch(b,P,Q,B,colour,U,operations,cover=None,matching=None,conflict_cover=None):
    """Exact best inherited-cover certificate for a fixed physical candidate list.

    Each owner appears at most once, each local replacement is permitted,
    and every removal lies outside C. Additional points may have conflicts
    and need not be isolated finally. Neutral deletions have zero credit.
    """
    data=prepare(b,P,Q,B,colour);n=2*b;V=set(range(n));U=set(U);E=data['P']+data['Q']
    if not U<=V or not _permitted(n,data['B'],U):raise ValueError('Initial omission must be permitted')
    operations=[tuple(op) for op in operations];owners=data['owner_components'];used=set()
    for i,x,y in operations:
        if i not in range(len(owners)) or i in used:raise ValueError('Use distinct owner components')
        K=set(owners[i][0])
        if x not in U&K or y not in K-U or not _permitted(n,data['B'],(U-{x})|{y}):
            raise ValueError('Each local replacement must be permitted within its owner')
        used.add(i)
    if cover is None or matching is None:
        T,M=score(n,data['P'],data['Q'],U)
        if cover is None:cover=U-T
        if matching is None:matching=M
    C=set(cover);M=[tuple(sorted(e)) for e in matching]
    constraints=credit_constraints(n,E,U,C,M,[(x,y) for i,x,y in operations])
    result=closed_conflict_optimum(constraints['weights'],constraints['dependencies'],constraints['conflicts'],constraints['blocked'],conflict_cover)
    selected=[operations[i] for i in result['selected']];X={x for i,x,y in selected};Y={y for i,x,y in selected};new=(U-X)|Y
    mate={v:w for a,c in M for v,w in ((a,c),(c,a))};R={mate[x] for x in X if x in mate};final_cover=C-R
    charges=[dict(candidate=i,removed=operations[i][1],edge=sorted((operations[i][1],mate[operations[i][1]]))) for i in result['selected'] if operations[i][1] in mate]
    remaining=[list(e) for e in M if not set(e)&X];cost=len(C)-result['credit'];T=new-final_cover
    assert len(R)==len(charges)==result['credit'] and len({tuple(r['edge']) for r in charges})==len(charges)
    assert len(remaining)==len(final_cover)==cost and final_cover<=new
    assert all(a in final_cover or c in final_cover for a,c in E if a in new and c in new)
    assert _permitted(n,data['B'],new) and len(new)==len(U)
    certificate=dict(initial_U=sorted(U),initial_cover=sorted(C),initial_matching=[list(e) for e in M],initial_cost=len(C),
                     selected_candidates=result['selected'],operations=[list(op) for op in selected],removed=sorted(X),added=sorted(Y),
                     retired_cover=sorted(R),charged_edges=charges,matching=remaining,cover=sorted(final_cover),U=sorted(new),
                     witnesses=sorted(T),owners=sorted(V-new),actual_cost=cost,beta_I_lower=3*b-cost,
                     neutral_removals=sorted(x for x in X if x not in mate))
    return dict(constraints=constraints,optimization=result,certificate=certificate)


def neutral_plateau_family(m):
    """Every m>=1: prior strict-descent plateau, now solved by one batch."""
    if not isinstance(m,int) or isinstance(m,bool) or m<1:raise ValueError('Use integer m>=1')
    n=8*m;P=[(v,v+1) for v in range(0,n,2)];Q=[(v,(v+1)%n) for v in range(1,n,2)]
    Cs=[]
    for j in range(m):
        a=8*j;Cs += [[a,a+6,a+1,a+7],[a+2,a+4,a+3,a+5]]
    B=[e for K in Cs for e in zip(K,K[1:]+K[:1])];colour=[(v//2)%2 for v in range(n)]
    data=prepare(4*m,P,Q,B,colour);ids={frozenset(K):i for i,(K,_) in enumerate(data['owner_components'])}
    operations=[]
    for j in range(m):
        a=8*j;operations += [[ids[frozenset(Cs[2*j])],a+1,a],[ids[frozenset(Cs[2*j+1])],a+3,a+4]]
    return dict(b=4*m,P=P,Q=Q,B=B,colour=colour,m=m,initial_U=[8*j+t for j in range(m) for t in (1,2,3,6)],
                cover=[8*j+2 for j in range(m)],matching=[(8*j+1,8*j+2) for j in range(m)],operations=operations)


def odd_path_escape_family(r):
    """Even r>=4: full cost-zero escape with one unmatched neutral removal."""
    from cover_saturated_exchange import shared_odd_path_family
    x=shared_odd_path_family(r);data=prepare(*(x[k] for k in ('b','P','Q','B','colour')))
    ids={v:i for i,(K,_) in enumerate(data['owner_components']) for v in K}
    route=[(1,0),(3,2*r)]+[(2*i+1,2*r+2*(i^1)) for i in range(2,r)]
    x['operations']=[[ids[a],a,c] for a,c in route];x['matching']=[(v,v+1) for v in range(1,2*r-2,2)]
    return x
