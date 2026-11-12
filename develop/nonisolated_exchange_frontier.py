"""Exact operation-count frontiers for arbitrary mixed replacements on
bipartite degree-two auxiliary graphs, including nonisolated additions.

Standard finite-state frontier DP; exponential in the supplied traversal's
number of live candidate pairs, not a general polynomial algorithm.
"""
from odd_path_neutral_budget import ordered_components
from mixed_isolated_cover_repair import path_certificate


def validate(n,edges,U,operations,component_orders=None):
    if not isinstance(n,int) or isinstance(n,bool) or n<0:raise ValueError('Nonnegative indexed order required')
    V=set(range(n));U=set(U);E=sorted({tuple(sorted(e)) for e in edges});ops=[tuple(e) for e in operations]
    if not U<=V or any(a==b or a not in V or b not in V for a,b in E):raise ValueError('Simple indexed graph required')
    canonical=ordered_components(V,E)
    if any(cyclic and len(K)%2 for K,cyclic in canonical):raise ValueError('Bipartite degree-two ambient graph required')
    if len({x for x,y in ops})!=len(ops) or len({y for x,y in ops})!=len(ops) or any(x not in U or y not in V-U for x,y in ops):raise ValueError('Distinct removals in U and additions outside U required')
    if component_orders is None:components=canonical
    else:
        orders=[list(K) for K in component_orders];flat=[v for K in orders for v in K]
        if len(flat)!=n or set(flat)!=V or any(not K for K in orders):raise ValueError('Orders must partition all vertices')
        lookup={frozenset(K):cyclic for K,cyclic in canonical};components=[];edge_set=set(E)
        for K in orders:
            key=frozenset(K)
            if key not in lookup:raise ValueError('Each order must be a complete ambient component')
            cyclic=lookup[key]
            if any(tuple(sorted((a,b))) not in edge_set for a,b in zip(K,K[1:])) or (cyclic and tuple(sorted((K[-1],K[0]))) not in edge_set):raise ValueError('Consecutive vertices must follow the component')
            components.append((K,cyclic))
    vertex_op={v:(i,role) for i,(x,y) in enumerate(ops) for v,role in ((x,0),(y,1))};order=[v for K,_ in components for v in K];position={v:j for j,v in enumerate(order)}
    first={i:min(position[x],position[y]) for i,(x,y) in enumerate(ops)};last={i:max(position[x],position[y]) for i,(x,y) in enumerate(ops)}
    live=set();width=0;profile=[]
    for j,v in enumerate(order):
        if v in vertex_op:
            i,_=vertex_op[v]
            if j==first[i]:live.add(i)
            else:live.remove(i)
        width=max(width,len(live));profile.append(len(live))
    assert not live
    return dict(n=n,edges=E,U=U,operations=ops,components=components,vertex_op=vertex_op,first=first,last=last,width=width,live_profile=profile)


def endpoint(n,edges,U,operations,selected):
    d=validate(n,edges,U,operations);U=d['U'];operations=d['operations'];S=set(selected)
    if not S<=set(range(len(operations))):raise ValueError('Indexed candidate subset required')
    X={operations[i][0] for i in S};Y={operations[i][1] for i in S};final=(set(U)-X)|Y
    initial=path_certificate(U,d['edges']);out=path_certificate(final,d['edges'])
    saving=initial['cost']-out['cost'];assert 2*saving==out['odd_components']-initial['odd_components'] and abs(saving)<=len(S)
    return dict(initial_cost=initial['cost'],actual_cost=out['cost'],saving=saving,selected_candidates=sorted(S),removed=sorted(X),added=sorted(Y),U=sorted(final),cover=out['cover'],matching=out['matching'],initial_odd_components=initial['odd_components'],final_odd_components=out['odd_components'])


def exact_frontier(n,edges,U,operations,component_orders=None):
    """Min cost for EACH exact operation count; explicit candidate-mask witnesses.

    w=max live pairs at a cut of the supplied component traversal.
    At most4*(q+1)*2^w states during any component. Large integer bitsets
    and output witnesses have polynomial bit cost. No monotonicity assumed.
    """
    d=validate(n,edges,U,operations,component_orders);q=len(d['operations']);position=0;between={(0,0):(0,0)};peak=1;transitions=0
    def keep(table,key,value):
        old=table.get(key)
        if old is None or value<old:table[key]=value
    for K,cyclic in d['components']:
        states={}
        for (live,t),value in between.items():
            for h in ((0,1) if cyclic else (0,)):states[live,t,h,h]=value
        peak=max(peak,len(states))
        for v in K:
            new={}
            for (live,t,p,h),(cost,chosen) in states.items():
                if v not in d['vertex_op']:choices=[(live,t,int(v in d['U']),chosen)]
                else:
                    i,role=d['vertex_op'][v];bit=1<<i
                    if position==d['first'][i]:choices=[(live|(s*bit),t+s,s if role else 1-s,chosen|(s*bit)) for s in (0,1)]
                    else:
                        s=int(bool(live&bit));choices=[(live&~bit,t,s if role else 1-s,chosen)]
                for live2,t2,present,chosen2 in choices:
                    p2=1-p if present else 0;cost2=cost+int(bool(present and p))
                    keep(new,(live2,t2,p2,h),(cost2,chosen2));transitions+=1
            states=new;position+=1;peak=max(peak,len(states))
        between={}
        for (live,t,p,h),value in states.items():
            if not cyclic or p==h:keep(between,(live,t),value)
    assert position==n and all(live==0 for live,t in between) and set(t for live,t in between)==set(range(q+1))
    rows=[dict(operations=t,cost=between[0,t][0],selected_mask=between[0,t][1]) for t in range(q+1)]
    assert all(row['selected_mask'].bit_count()==row['operations'] for row in rows)
    best=min(rows,key=lambda r:(r['cost'],r['operations'],r['selected_mask']))
    assert peak<=4*(q+1)*(1<<d['width'])
    return dict(pair_width=d['width'],live_profile=d['live_profile'],component_orders=[K for K,_ in d['components']],peak_states=peak,transitions=transitions,frontier=rows,best=best)


def physical_frontier(b,P,Q,B,colour,U,operations,component_orders=None):
    """Exact over ALL subsets of distinct-owner individually permitted swaps."""
    from owner_matching_certificate import prepare
    from collections import Counter
    data=prepare(b,P,Q,B,colour);n=2*b;V=set(range(n));U=set(U);ops=[tuple(e) for e in operations];used=set()
    degree=Counter(v for a,c in data['B'] if a not in U and c not in U for v in (a,c))
    if not U<=V or max(degree.values(),default=0)>1:raise ValueError('Permitted initial omission required')
    owner_of={v:i for i,(K,_) in enumerate(data['owner_components']) for v in K};local=[[] for _ in data['owner_components']]
    for e in data['B']:local[owner_of[e[0]]].append(e)
    for i,x,y in ops:
        if i not in range(len(local)) or i in used:raise ValueError('Distinct owners required')
        used.add(i);K=set(data['owner_components'][i][0]);remaining=(K-U)|{x};remaining.discard(y);degree=Counter(v for a,c in local[i] if a in remaining and c in remaining for v in (a,c))
        if x not in U&K or y not in K-U or max(degree.values(),default=0)>1:raise ValueError('Permitted within-owner replacement required')
    pairs=[(x,y) for _,x,y in ops];out=exact_frontier(n,data['P']+data['Q'],U,pairs,component_orders);mask=out['best']['selected_mask'];S=[i for i in range(len(ops)) if mask>>i&1]
    cert=endpoint(n,data['P']+data['Q'],U,pairs,S);cert.update(owners=sorted(V-set(cert['U'])),witnesses=sorted(set(cert['U'])-set(cert['cover'])),beta_I_lower=3*b-cert['actual_cost'])
    return dict(**out,certificate=cert)


def cost_increase_family(r):
    """Everyr>=1, physicalorder10r,min2max3,two-connected; cost(t)=t."""
    if not isinstance(r,int) or isinstance(r,bool) or r<1:raise ValueError('Integer r>=1 required')
    n=4*r;P=[e for i in range(r) for e in ((4*i,4*i+3),(4*i+1,4*i+2))];Q=[(4*i,4*((i+1)%r)+1) for i in range(r)]
    squares=[[4*i+t for t in (0,1,3,2)] for i in range(r)];B=[e for K in squares for e in zip(K,K[1:]+K[:1])]
    return dict(r=r,b=2*r,P=P,Q=Q,B=B,colour=[c for _ in range(r) for c in (0,1,1,0)],initial_U=[4*i+t for i in range(r) for t in (0,2)],operations=[[i,4*i,4*i+1] for i in range(r)])


def free_extension_family(r):
    """Everyr>=1, physicalorder20r; unrestricted cost(t)=2r-t;
    finally-isolated-addition restriction can only use the empty batch.
    Earlier mixed inherited-cover rules can already attain the full gain.
    """
    if not isinstance(r,int) or isinstance(r,bool) or r<1:raise ValueError('Integer r>=1 required')
    n=8*r;P=[(v,v+1) for v in range(0,n,2)];Q=[(v,(v+1)%n) for v in range(1,n,2)]
    squares=[]
    for i in range(r):a=8*i;squares.extend([[a+2,a+5,a+6,a+1],[a,a+3,a+4,a+7]])
    B=[e for K in squares for e in zip(K,K[1:]+K[:1])]
    # prepare visits the second square of each tile first (its minimum is a).
    return dict(r=r,b=4*r,P=P,Q=Q,B=B,colour=[(v//2)%2 for v in range(n)],initial_U=[8*i+t for i in range(r) for t in (1,2,3,4)],operations=[[2*i+1,8*i+2,8*i+5] for i in range(r)])


def within_budget(result,budget):
    if not isinstance(budget,int) or isinstance(budget,bool) or budget<0:raise ValueError('Nonnegative operation budget required')
    return min((r for r in result['frontier'] if r['operations']<=budget),key=lambda r:(r['cost'],r['operations'],r['selected_mask']))
