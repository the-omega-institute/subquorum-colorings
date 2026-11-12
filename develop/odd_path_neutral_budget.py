"""Shared odd-path neutral budgets with explicit final-cover repair.

This optimizes the isolated-addition, outside-independent-cover candidate
class, not arbitrary exchanges or unrestricted all-helper optimization.
"""
from collections import Counter


def ordered_components(vertices, edges):
    vertices=set(vertices);adj={v:set() for v in vertices}
    for a,b in edges:
        if a in vertices and b in vertices:adj[a].add(b);adj[b].add(a)
    if any(len(ns)>2 for ns in adj.values()):raise ValueError('Initial induced maximum degree at most two required')
    unseen=set(vertices);answer=[]
    while unseen:
        block={min(unseen)};todo=list(block)
        while todo:
            for v in adj[todo.pop()]-block:block.add(v);todo.append(v)
        ends=sorted(v for v in block if len(adj[v])<2);cyclic=not ends
        v=ends[0] if ends else min(block);previous=None;order=[];visited=set()
        while v not in visited:
            visited.add(v);order.append(v);options=sorted(adj[v]-({previous} if previous is not None else set()))
            if not options:break
            previous,v=v,options[0]
        assert set(order)==block
        answer.append((order,cyclic));unseen-=block
    return answer


def compile_budget(n,edges,U,cover,matching,operations):
    """Validate tight independent C,M0; compile exact final-isolation conditions."""
    if not isinstance(n,int) or isinstance(n,bool) or n<0:raise ValueError('Nonnegative indexed order required')
    V=set(range(n));U=set(U);C=set(cover);E=sorted({tuple(sorted(e)) for e in edges});M=[tuple(sorted(e)) for e in matching]
    operations=[tuple(op) for op in operations]
    if not C<=U<=V or any(a==b or a not in V or b not in V for a,b in E):raise ValueError('Simple graph and C subset U required')
    if any((a in C)==(b in C) for a,b in E if a in U and b in U):raise ValueError('Independent vertex cover required')
    if len(M)!=len(C) or len({v for e in M for v in e})!=2*len(M) or any(e not in E or not set(e)<=U for e in M):raise ValueError('Tight initial matching required')
    if len({x for x,y in operations})!=len(operations) or len({y for x,y in operations})!=len(operations):raise ValueError('Distinct removal and addition points required')
    if any(x not in U-C or y not in V-U for x,y in operations):raise ValueError('Remove outside C; add outside U')
    components=ordered_components(U,E);which={v:j for j,(K,_) in enumerate(components) for v in K};odd=set()
    for j,(K,cyclic) in enumerate(components):
        delta=len(set(K)-C)-len(set(K)&C)
        if delta not in (0,1) or (cyclic and delta):raise ValueError('Tight independent cover on paths/even cycles required')
        if delta:odd.add(j)
    removal={x:i for i,(x,y) in enumerate(operations)};addition={y:i for i,(x,y) in enumerate(operations)}
    dependencies=set();conflicts=set();blocked=set();evidence=[]
    for a,b in E:
        if a in addition and b in addition:conflicts.add(tuple(sorted((addition[a],addition[b]))))
        for y,v in ((a,b),(b,a)):
            if y not in addition or v not in U:continue
            i=addition[y]
            if v in removal:dependencies.add((i,removal[v]))
            else:blocked.add(i);evidence.append(dict(candidate=i,edge=[a,b],unavailable_removal=v))
    return dict(groups=[which[x] if which[x] in odd else None for x,y in operations],dependencies=[list(e) for e in sorted(dependencies)],
                conflicts=[list(e) for e in sorted(conflicts)],blocked=sorted(blocked),blocker_evidence=evidence,
                initial_components=[dict(vertices=K,cyclic=cyclic,odd=j in odd) for j,(K,cyclic) in enumerate(components)],
                operations=[list(e) for e in operations])


def budget_value(groups,selected):
    selected=set(selected)
    return len(selected)-len({groups[i] for i in selected if groups[i] is not None})


def grouped_optimum(groups,dependencies=(),conflicts=(),blocked=(),vertex_cover=None):
    """Maximize shared budget, then minimize selected labels, in 2^|K| poly.

    K is a supplied conflict vertex cover, or endpoints of a greedy maximal
    conflict matching. A fixed K-assignment has a unique smallest optimum.
    """
    groups=list(groups);V=set(range(len(groups)));D=sorted(set(map(tuple,dependencies)));F=sorted({tuple(sorted(e)) for e in conflicts});blocked=set(blocked)
    if not blocked<=V or any(a not in V or b not in V for a,b in D+F) or any(a==b for a,b in F):raise ValueError('Indexed implications and loop-free conflicts required')
    K=set() if vertex_cover is None else set(vertex_cover)
    if vertex_cover is None:
        for a,b in F:
            if a not in K and b not in K:K|={a,b}
    if not K<=V or any(a not in K and b not in K for a,b in F):raise ValueError('Conflict vertex cover required')
    K=sorted(K);forward=[set() for _ in V];reverse=[set() for _ in V];adj=[set() for _ in V]
    for a,b in D:forward[a].add(b);reverse[b].add(a)
    for a,b in F:adj[a].add(b);adj[b].add(a)
    best=None;assignments=0
    for mask in range(1<<len(K)):
        chosen={v for j,v in enumerate(K) if mask>>j&1}
        if any(a in chosen and b in chosen for a,b in F):continue
        excluded=blocked|(set(K)-chosen)|{v for i in chosen for v in adj[i]};todo=list(excluded)
        while todo:
            j=todo.pop()
            for i in reverse[j]-excluded:excluded.add(i);todo.append(i)
        if chosen&excluded:continue
        greatest=V-excluded;mult=Counter(groups[i] for i in greatest if groups[i] is not None)
        roots=chosen|{i for i in greatest if groups[i] is None or mult[groups[i]]>=2};selected=set(roots);todo=list(roots)
        while todo:
            i=todo.pop()
            for j in forward[i]-selected:selected.add(j);todo.append(j)
        value=budget_value(groups,greatest);assert budget_value(groups,selected)==value and selected<=greatest
        assignments+=1
        trial=dict(credit=value,selected=sorted(selected),roots=sorted(roots),greatest_for_assignment=sorted(greatest),chosen_cover_labels=sorted(chosen))
        if best is None or (value,-len(selected))>(best['credit'],-len(best['selected'])):best=trial
    assert best is not None
    return dict(vertex_cover=K,assignments=1<<len(K),feasible_assignments=assignments,**best)


def repair_batch(n,edges,U,cover,matching,operations,selected):
    """Construct a tight final cover/matching by consecutive path pairing.

    No final matching optimizer. One different original matching edge is
    charged per vertex-disjoint final C-heavy odd repair component.
    """
    compiled=compile_budget(n,edges,U,cover,matching,operations);selected=set(selected);V=set(range(len(operations)))
    if not selected<=V or selected&set(compiled['blocked']) or any(a in selected and b not in selected for a,b in compiled['dependencies']) or any(a in selected and b in selected for a,b in compiled['conflicts']):raise ValueError('Feasible isolated-addition batch required')
    U=set(U);C=set(cover);X={operations[i][0] for i in selected};Y={operations[i][1] for i in selected};final=(U-X)|Y
    repaired=set();M=[];regions=[]
    for K,cyclic in ordered_components(U-X,edges):
        KC=set(K)&C;KI=set(K)-C
        if len(KC)>len(KI):
            assert not cyclic and len(KC)==len(KI)+1
            choices=sorted(tuple(sorted(e)) for e in matching if set(e)&KC and set(e)&X)
            assert choices
            regions.append(dict(vertices=K,old_cover=sorted(KC),new_cover=sorted(KI),charged_initial_edge=list(choices[0])))
            repaired|=KI
        else:repaired|=KC
        M.extend([K[j],K[j+1]] for j in range(0,len(K)-1,2))
    credit=budget_value(compiled['groups'],selected)
    assert len(regions)==credit and len(M)==len(repaired)==len(C)-credit
    charges=[r['charged_initial_edge'] for r in regions];assert len({tuple(e) for e in charges})==len(charges)
    return dict(initial_cost=len(C),actual_cost=len(M),credit=credit,selected_candidates=sorted(selected),removed=sorted(X),added=sorted(Y),U=sorted(final),
                cover=sorted(repaired),matching=M,repair_regions=regions,charged_edges=charges)


def physical_budget_batch(b,P,Q,B,colour,U,operations,cover,matching,conflict_cover=None):
    from owner_matching_certificate import prepare
    data=prepare(b,P,Q,B,colour);n=2*b;U=set(U);used=set();ops=[tuple(e) for e in operations]
    V=set(range(n));owner_degree=Counter(v for a,c in data['B'] if a not in U and c not in U for v in (a,c))
    if not U<=V or max(owner_degree.values(),default=0)>1:raise ValueError('Permitted omission required')
    local_edges=[[] for _ in data['owner_components']];owner_of={v:i for i,(K,_) in enumerate(data['owner_components']) for v in K}
    for edge in data['B']:local_edges[owner_of[edge[0]]].append(edge)
    for i,x,y in ops:
        if i not in range(len(data['owner_components'])) or i in used:raise ValueError('Distinct owners required')
        K=set(data['owner_components'][i][0]);used.add(i)
        local=(K-U)|{x};local.discard(y)
        degree=Counter(v for a,c in local_edges[i] if a in local and c in local for v in (a,c))
        if x not in U&K or y not in K-U or max(degree.values(),default=0)>1:raise ValueError('Permitted within-owner replacement required')
    pairs=[(x,y) for _,x,y in ops];compiled=compile_budget(n,data['P']+data['Q'],U,cover,matching,pairs)
    opt=grouped_optimum(compiled['groups'],compiled['dependencies'],compiled['conflicts'],compiled['blocked'],conflict_cover)
    out=repair_batch(n,data['P']+data['Q'],U,cover,matching,pairs,opt['selected']);assert out['credit']==opt['credit']
    out.update(witnesses=sorted(set(out['U'])-set(out['cover'])),owners=sorted(set(range(n))-set(out['U'])),beta_I_lower=3*b-out['actual_cost'])
    return dict(constraints=compiled,optimization=opt,certificate=out)


def shared_path_family(r):
    """Every integer r>=3: inherited cost2r-2; repaired fixed-list optimum r-1."""
    if not isinstance(r,int) or isinstance(r,bool) or r<3:raise ValueError('Integer r>=3 required')
    from owner_matching_certificate import prepare
    n=8*r;b=4*r;colour=[(v//2)%2 for v in range(n)];U=set(range(1,4*r-2))|{4*r,4*r+4,4*r+8}
    X=[4*j+1 for j in range(r)];Y=[4*r+2+4*j for j in range(r)]
    remainingU=U-set(X);outside=set(range(n))-U-set(Y);pairs=[]
    for c in (0,1):
        left=sorted(v for v in remainingU if colour[v]==c);right=sorted(v for v in outside if colour[v]!=c)
        assert len(left)==len(right);pairs.extend(zip(left,right))
    squares=[]
    for j,(u,z) in enumerate(pairs[:r]):squares.append([X[j],Y[j],u,z] if colour[u]==0 else [X[j],Y[j],z,u])
    for k in range(r,3*r,2):
        e,f=pairs[k:k+2];squares.append(sorted(e,key=lambda v:colour[v])+sorted(f,key=lambda v:colour[v]))
    P=[(v,v+1) for v in range(0,n,2)];Q=[(v,(v+1)%n) for v in range(1,n,2)];B=[e for K in squares for e in zip(K,K[1:]+K[:1])]
    data=prepare(b,P,Q,B,colour);ids={frozenset(K):i for i,(K,_) in enumerate(data['owner_components'])}
    ops=[[ids[frozenset(squares[j])],X[j],Y[j]] for j in range(r)]
    return dict(r=r,b=b,P=P,Q=Q,B=B,colour=colour,initial_U=sorted(U),cover=list(range(2,4*r-3,2)),
                matching=[(v,v+1) for v in range(1,4*r-4,2)],operations=ops,squares=squares)
