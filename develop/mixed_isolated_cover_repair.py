"""Mixed-side isolated-addition repair: exact cost, parameterized max credit,
SCC exact tie-break, and a physical minimum-operation hardness construction.
"""
from collections import Counter
from odd_path_neutral_budget import ordered_components


def path_certificate(vertices,edges):
    """Tight cover/matching of a degree-two bipartite induced graph, no optimizer."""
    components=ordered_components(vertices,edges);C=set();M=[];odd=0
    for K,cyclic in components:
        if cyclic and len(K)%2:raise ValueError('Bipartite initial graph required')
        a=K[::2];b=K[1::2];C.update(a if len(a)<=len(b) else b)
        M.extend([K[j],K[j+1]] for j in range(0,len(K)-1,2));odd+=len(K)%2
    assert len(C)==len(M)
    return dict(cover=sorted(C),matching=M,cost=len(M),odd_components=odd,
                components=[dict(vertices=K,cyclic=cyclic) for K,cyclic in components])


def compile_isolation(n,edges,U,operations):
    if not isinstance(n,int) or isinstance(n,bool) or n<0:raise ValueError('Nonnegative indexed order required')
    V=set(range(n));U=set(U);E=sorted({tuple(sorted(e)) for e in edges});ops=[tuple(e) for e in operations]
    if not U<=V or any(a==b or a not in V or b not in V for a,b in E):raise ValueError('Simple indexed graph required')
    initial=path_certificate(U,E)
    if len({x for x,y in ops})!=len(ops) or len({y for x,y in ops})!=len(ops) or any(x not in U or y not in V-U for x,y in ops):raise ValueError('Distinct removals in U and additions outside U required')
    removal={x:i for i,(x,y) in enumerate(ops)};addition={y:i for i,(x,y) in enumerate(ops)};D=set();F=set();blocked=set()
    for a,b in E:
        if a in addition and b in addition:F.add(tuple(sorted((addition[a],addition[b]))))
        for y,v in ((a,b),(b,a)):
            if y not in addition or v not in U:continue
            if v in removal:D.add((addition[y],removal[v]))
            else:blocked.add(addition[y])
    return dict(initial=initial,dependencies=[list(e) for e in sorted(D)],conflicts=[list(e) for e in sorted(F)],blocked=sorted(blocked),operations=[list(e) for e in ops])


def repair(n,edges,U,operations,selected):
    z=compile_isolation(n,edges,U,operations);S=set(selected)
    if not S<=set(range(len(operations))) or S&set(z['blocked']) or any(a in S and b not in S for a,b in z['dependencies']) or any(a in S and b in S for a,b in z['conflicts']):raise ValueError('Feasible isolated-addition batch required')
    X={operations[i][0] for i in S};Y={operations[i][1] for i in S};remaining=set(U)-X;final=remaining|Y;certificate=path_certificate(remaining,edges);initial=z['initial']
    credit=(len(X)+certificate['odd_components']-initial['odd_components'])//2
    assert 2*credit==len(X)+certificate['odd_components']-initial['odd_components'] and credit==initial['cost']-certificate['cost'] and credit>=0
    lost=[e for e in initial['matching'] if set(e)&X];assert credit<=len(lost)
    return dict(initial_cost=initial['cost'],actual_cost=certificate['cost'],credit=credit,selected_candidates=sorted(S),removed=sorted(X),added=sorted(Y),U=sorted(final),
                cover=certificate['cover'],matching=certificate['matching'],initial_odd_components=initial['odd_components'],remaining_odd_components=certificate['odd_components'],
                destroyed_initial_edges=lost,charged_edges=lost[:credit])


def maximum_credit(n,edges,U,operations,conflict_cover=None):
    """2^|K| poly exact max saving; deliberately NO minimum-operation claim."""
    z=compile_isolation(n,edges,U,operations);q=len(operations);V=set(range(q));D=z['dependencies'];F=z['conflicts'];K=set() if conflict_cover is None else set(conflict_cover)
    if conflict_cover is None:
        for a,b in F:
            if a not in K and b not in K:K|={a,b}
    if not K<=V or any(a not in K and b not in K for a,b in F):raise ValueError('Conflict vertex cover required')
    K=sorted(K);reverse=[set() for _ in V];adj=[set() for _ in V]
    for a,b in D:reverse[b].add(a)
    for a,b in F:adj[a].add(b);adj[b].add(a)
    best=None;feasible=0
    for mask in range(1<<len(K)):
        chosen={v for j,v in enumerate(K) if mask>>j&1}
        if any(a in chosen and b in chosen for a,b in F):continue
        excluded=set(z['blocked'])|(set(K)-chosen)|{v for i in chosen for v in adj[i]};todo=list(excluded)
        while todo:
            j=todo.pop()
            for i in reverse[j]-excluded:excluded.add(i);todo.append(i)
        if chosen&excluded:continue
        out=repair(n,edges,U,operations,V-excluded);feasible+=1
        if best is None or out['credit']>best['credit']:best=out
    assert best is not None
    return dict(vertex_cover=K,assignments=1<<len(K),feasible_assignments=feasible,certificate=best)


def dependency_components(q,dependencies):
    """Iterative Kosaraju, avoiding a recursion-depth assumption."""
    adj=[set() for _ in range(q)];rev=[set() for _ in range(q)]
    for a,b in dependencies:adj[a].add(b);rev[b].add(a)
    seen=set();post=[]
    for root in range(q):
        if root in seen:continue
        stack=[(root,False)]
        while stack:
            v,done=stack.pop()
            if done:post.append(v);continue
            if v in seen:continue
            seen.add(v);stack.append((v,True))
            for w in sorted(adj[v],reverse=True):
                if w not in seen:stack.append((w,False))
    seen=set();blocks=[]
    for root in reversed(post):
        if root in seen:continue
        block={root};seen.add(root);todo=[root]
        while todo:
            for w in rev[todo.pop()]-seen:seen.add(w);block.add(w);todo.append(w)
        blocks.append(sorted(block))
    return blocks


def minimum_operation_optimum(n,edges,U,operations):
    """Exact max-credit/min-operations in 2^s poly, s dependency SCCs."""
    z=compile_isolation(n,edges,U,operations);blocks=dependency_components(len(operations),z['dependencies']);best=None;feasible=0
    for mask in range(1<<len(blocks)):
        S={v for j,B in enumerate(blocks) if mask>>j&1 for v in B}
        if S&set(z['blocked']) or any(a in S and b not in S for a,b in z['dependencies']) or any(a in S and b in S for a,b in z['conflicts']):continue
        out=repair(n,edges,U,operations,S);feasible+=1
        if best is None or (out['credit'],-len(S))>(best['credit'],-len(best['selected_candidates'])):best=out
    assert best is not None
    return dict(dependency_components=blocks,assignments=1<<len(blocks),feasible_assignments=feasible,certificate=best)


def vertex_cover_physical(k,H):
    """For any simple k-vertex H, min operations to cost0 is D*tau(H).

    All final-isolation feasible batches are unions of D-label groups.
    Actual physical graph is bipartite min2/max3; connected/bridgeless H
    additionally makes it two-connected. No unrestricted all-helper hardness.
    """
    if not isinstance(k,int) or isinstance(k,bool) or k<1:raise ValueError('Positive indexed H order required')
    H=sorted({tuple(sorted(e)) for e in H});V=set(range(k))
    if any(a==b or a not in V or b not in V for a,b in H):raise ValueError('Simple indexed H required')
    deg=Counter(v for e in H for v in e);D=max(1,max(deg.values(),default=0));inc={};groups=[];labels=[];xcolour=[]
    for v in range(k):
        group=[]
        for e in H:
            if v not in e:continue
            inc[v,e]=len(labels);group.append(len(labels));labels.append([v,list(e)]);xcolour.append(int(v==e[1]))
        while len(group)<D:group.append(len(labels));labels.append([v,None]);xcolour.append(0)
        groups.append(group)
    q=len(labels);colour=xcolour+[0]*(3*q);P=[];Q=[(inc[a,e],inc[b,e]) for e in H for a,b in [e]]
    for group in groups:
        for i,j in zip(group,group[1:]+group[:1]):P.append((q+i,j));colour[q+i]=colour[j]
        different=[i for i in group if colour[i]!=colour[q+i]];assert len(different)%2==0
        split={i:int(j>=len(different)//2) for j,i in enumerate(different)}
        for i in group:
            if i in split:colour[2*q+i]=split[i];colour[3*q+i]=1-split[i]
            else:colour[2*q+i]=colour[3*q+i]=1-colour[i]
        for c in (0,1):
            Z=sorted(2*q+i for i in group if colour[2*q+i]==c);W=sorted(3*q+i for i in group if colour[3*q+i]==c);assert len(Z)==len(W);P.extend(zip(Z,W))
    squares=[]
    for i in range(q):
        block=[i,q+i,2*q+i,3*q+i];a=sorted(v for v in block if colour[v]==0);b=sorted(v for v in block if colour[v]==1);assert len(a)==len(b)==2
        squares.append([a[0],b[0],a[1],b[1]])
    B=[e for K in squares for e in zip(K,K[1:]+K[:1])]
    # Independent index-to-owner map is explicit: each square has minimum i,
    # and the standard prepare() catalogue visits these squares in i order.
    U=list(range(q))+list(range(2*q,3*q));ops=[[i,i,q+i] for i in range(q)]
    return dict(k=k,H=[list(e) for e in H],D=D,q=q,b=2*q,P=P,Q=Q,B=B,colour=colour,initial_U=U,operations=ops,groups=groups,labels=labels,squares=squares)


def bridgeless_vertex_cover_reduction(k,H):
    """Connected bridgeless J with tau(J)=2*m_apex+tau(H)+1.

    Apex + k+2 leaves forces apex, then every edge is replaced by two
    internally disjoint length-three paths. Each uncovered base edge costs
    two extra internal vertices, so an optimum always covers that edge.
    """
    if not isinstance(k,int) or isinstance(k,bool) or k<0:raise ValueError('Nonnegative indexed order required')
    H=sorted({tuple(sorted(e)) for e in H})
    if any(a==b or a not in range(k) or b not in range(k) for a,b in H):raise ValueError('Simple indexed H required')
    apex=k;leaves=list(range(k+1,2*k+3));base=H+[(apex,v) for v in range(k)]+[(apex,v) for v in leaves];J=[];paths=[];nextv=2*k+3
    for u,v in base:
        a,b,c,d=range(nextv,nextv+4);nextv+=4;J.extend([(u,a),(a,b),(b,v),(u,c),(c,d),(d,v)]);paths.append(dict(base_edge=[u,v],paths=[[u,a,b,v],[u,c,d,v]]))
    return dict(original_k=k,original_edges=[list(e) for e in H],base_k=2*k+3,base_edges=[list(e) for e in base],apex=apex,leaves=leaves,k=nextv,H=[list(e) for e in J],paths=paths,tau_additive_constant=2*len(base)+1)
