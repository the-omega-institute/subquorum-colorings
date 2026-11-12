"""Eliminate initial matching choice; expose its remaining Hall obstruction."""
from collections import deque
from matching_credit_exchange import credit_constraints
from cover_choice_exchange import minimum_covers
from all_helper_optimization import score
from owner_matching_certificate import prepare
from mixed_owner_bridges import _permitted


def saturate(left,right,edges):
    """Saturate left in the cross graph, or return an explicit Hall deficiency."""
    left=set(left);right=set(right)
    if left&right:raise ValueError('Disjoint matching sides required')
    adj={v:set() for v in left}
    for a,b in edges:
        if a in left and b in right:adj[a].add(b)
        if b in left and a in right:adj[b].add(a)
    lm={};rm={}
    for root in sorted(left):
        todo=deque([root]);L={root};R=set();parent={};free=None
        while todo and free is None:
            v=todo.popleft()
            for u in sorted(adj[v]-R):
                R.add(u);parent[u]=v
                if u not in rm:free=u;break
                w=rm[u]
                if w not in L:L.add(w);todo.append(w)
        if free is None:
            assert set().union(*(adj[v] for v in L))==R and len(L)>len(R)
            return dict(saturated=False,matching=[[v,lm[v]] for v in sorted(lm)],hall_left=sorted(L),hall_neighbours=sorted(R),deficiency=len(L)-len(R))
        while free is not None:
            v=parent[free];old=lm.get(v);lm[v]=free;rm[free]=v;free=old
    return dict(saturated=True,matching=[[v,lm[v]] for v in sorted(lm)])


def choose_matching(n,edges,U,cover,initial_matching,X,Y,allow_mixed=False):
    """Exact existence test over ALL tight initial matchings for this C,X,Y.

    Supply one tight pair to certify the initial graph. By default removals lie
    outside C; allow_mixed=True permits removals on both sides of the cover.
    The final cover is inherited, not arbitrary. No final matching optimization.
    """
    edges=sorted({tuple(sorted(e)) for e in edges});U=set(U);C=set(cover);X=set(X);Y=set(Y)
    M0=[tuple(sorted(e)) for e in initial_matching]
    credit_constraints(n,edges,U,C,M0,[])
    if not X<=(U if allow_mixed else U-C) or not Y<=set(range(n))-U or len(X)!=len(Y):
        raise ValueError('Equal-sized replacements with permitted removal domain required')
    I=U-C;new=(U-X)|Y
    adj={c:set() for c in C}
    for a,b in edges:
        if a in C and b in I:adj[a].add(b)
        if b in C and a in I:adj[b].add(a)
    retired=(C&X)|{c for c in C-X if not adj[c]&(I-X)};kept=C-retired
    common=dict(initial_U=sorted(U),initial_cover=sorted(C),removed=sorted(X),added=sorted(Y),U=sorted(new),forced_retired=sorted(retired),cover=sorted(kept))
    bad=next((list(e) for e in edges if set(e)<=new and not set(e)&kept),None)
    if bad is not None:return dict(applicable=False,reason='inherited cover misses final edge',uncovered_edge=bad,**common)
    allowed=[e for e in edges if not ((e[0] in kept and e[1] in X) or (e[1] in kept and e[0] in X))]
    trial=saturate(C,I,allowed)
    if not trial['saturated']:return dict(applicable=False,reason='constrained initial matching cannot saturate cover',hall=trial,**common)
    chosen=trial['matching'];lost=[e for e in chosen if set(e)&X];remaining=[e for e in chosen if not set(e)&X]
    assert len(lost)==len(retired) and all(set(e)&X for e in lost)
    assert len({v for e in chosen for v in e})==2*len(chosen)==2*len(C)
    assert len(remaining)==len(kept) and all(not set(e)&X for e in remaining)
    return dict(applicable=True,initial_matching=chosen,matching=remaining,charged_edges=lost,
                initial_cost=len(C),actual_cost=len(kept),credit=len(retired),**common)


def best_initial_pair_batch(b,P,Q,B,colour,U,operations,allow_mixed=False):
    """Exact over all initial pairs for the specified inherited transfer rule.

    Enumerates minimum covers and candidate subsets; exponential generally.
    One operation per owner, individually permitted. In the default outside-only
    mode, removals in a given cover are excluded; mixed mode allows them.
    """
    data=prepare(b,P,Q,B,colour);n=2*b;U=set(U);V=set(range(n));E=data['P']+data['Q'];ops=[tuple(e) for e in operations]
    if not U<=V or not _permitted(n,data['B'],U):raise ValueError('Permitted initial omission required')
    used=set()
    for i,x,y in ops:
        if i not in range(len(data['owner_components'])) or i in used:raise ValueError('Distinct owners required')
        K=set(data['owner_components'][i][0]);used.add(i)
        if x not in U&K or y not in K-U or not _permitted(n,data['B'],(U-{x})|{y}):raise ValueError('Permitted within-owner replacement required')
    _,M0=score(n,data['P'],data['Q'],U);best=None;covers=trials=0
    for C in minimum_covers(n,E,U):
        covers+=1;ids=[j for j,(_,x,_) in enumerate(ops) if allow_mixed or x not in C]
        for mask in range(1<<len(ids)):
            S=[j for k,j in enumerate(ids) if mask>>k&1];X={ops[j][1] for j in S};Y={ops[j][2] for j in S}
            z=choose_matching(n,E,U,C,M0,X,Y,allow_mixed);trials+=1
            if not z['applicable']:continue
            if best is None or (z['credit'],-len(S))>(best['credit'],-len(best['selected_candidates'])):
                best=dict(selected_candidates=S,operations=[list(ops[j]) for j in S],**z)
    assert best is not None
    best['witnesses']=sorted(set(best['U'])-set(best['cover']));best['owners']=sorted(V-set(best['U']));best['beta_I_lower']=3*b-best['actual_cost']
    return dict(minimum_covers_tested=covers,batch_cover_trials=trials,certificate=best)


def common_neighbour_barrier(m):
    """Every m>=1: all initial pairs return2m, actual fixed-list optimum m."""
    if not isinstance(m,int) or isinstance(m,bool) or m<1:raise ValueError('Integer m>=1 required')
    n=12*m;P=[(v,v+1) for v in range(0,n,2)];Q=[(v,(v+1)%n) for v in range(1,n,2)]
    squares=[]
    for j in range(m):
        a=12*j;squares.extend([[a+1,a+7,a,a+2],[a+5,a+11,a+8,a+3],[a+4,a+6,a+9,a+10]])
    B=[e for K in squares for e in zip(K,K[1:]+K[:1])];colour=[(v//2)%2 for v in range(n)];b=6*m
    data=prepare(b,P,Q,B,colour);ids={frozenset(K):i for i,(K,_) in enumerate(data['owner_components'])}
    operations=[]
    for j in range(m):
        a=12*j;operations.extend([[ids[frozenset(squares[3*j])],a+1,a+7],[ids[frozenset(squares[3*j+1])],a+5,a+11]])
    return dict(b=b,P=P,Q=Q,B=B,colour=colour,m=m,initial_U=[12*j+t for j in range(m) for t in (1,2,3,4,5,9)],
                cover=[12*j+t for j in range(m) for t in (2,4)],matching=[(12*j+1,12*j+2) for j in range(m)]+[(12*j+4,12*j+5) for j in range(m)],operations=operations)


def mixed_path_escape(m):
    """Every m>=1: either one-sided rule costs m, mixed transfer costs zero."""
    if not isinstance(m,int) or isinstance(m,bool) or m<1:raise ValueError('Integer m>=1 required')
    n=12*m;P=[(v,v+1) for v in range(0,n,2)];Q=[(v,(v+1)%n) for v in range(1,n,2)];squares=[]
    for j in range(m):
        a=12*j;squares.extend([[a,a+2,a+1,a+11],[a+4,a+6,a+9,a+3],[a+8,a+10,a+5,a+7]])
    B=[e for K in squares for e in zip(K,K[1:]+K[:1])];colour=[(v//2)%2 for v in range(n)];b=6*m
    data=prepare(b,P,Q,B,colour);ids={frozenset(K):i for i,(K,_) in enumerate(data['owner_components'])};ops=[]
    for j in range(m):
        a=12*j;ops.extend([[ids[frozenset(squares[3*j])],a+1,a],[ids[frozenset(squares[3*j+1])],a+3,a+4],[ids[frozenset(squares[3*j+2])],a+7,a+10]])
    return dict(b=b,P=P,Q=Q,B=B,colour=colour,m=m,initial_U=[12*j+t for j in range(m) for t in (1,2,3,6,7,8)],
                cover=[12*j+t for j in range(m) for t in (2,7)],matching=[(12*j+1,12*j+2) for j in range(m)]+[(12*j+6,12*j+7) for j in range(m)],operations=ops)
