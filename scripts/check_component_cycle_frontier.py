"""Independent literal matching, candidate subsets, physical and width checks."""
from pathlib import Path
from itertools import combinations, permutations, product
from collections import Counter
from functools import lru_cache
import argparse, hashlib, json, random, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from component_cycle_frontier import component_frontier, physical_component_frontier, component_star_family
from nonisolated_exchange_frontier import exact_frontier, endpoint, validate, within_budget
from owner_matching_certificate import prepare
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();examples=[]


def subsets(vertices):
    vertices=list(vertices)
    for mask in range(1<<len(vertices)):
        yield {v for i,v in enumerate(vertices) if mask>>i&1}


def graph_components(n,E):
    adj=[set() for _ in range(n)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    out=[];seen=set()
    for root in range(n):
        if root in seen:continue
        K={root};stack=[root];seen.add(root)
        while stack:
            for v in adj[stack.pop()]-seen:seen.add(v);K.add(v);stack.append(v)
        out.append(K)
    return out,adj


def allowed(n,E):
    cs,adj=graph_components(n,E)
    if any(len(v)>2 for v in adj):return False
    colour={}
    for K in cs:
        root=min(K);colour[root]=0;stack=[root]
        while stack:
            v=stack.pop()
            for w in adj[v]:
                if w in colour:
                    if colour[w]==colour[v]:return False
                else:colour[w]=1-colour[v];stack.append(w)
    return True


def literal_nu(vertices,E):
    """Enumerate matchings, decomposed only by literal physical adjacency."""
    vertices=set(vertices);adj={v:set() for v in vertices}
    for a,b in E:
        if a in vertices and b in vertices:adj[a].add(b);adj[b].add(a)
    @lru_cache(None)
    def rec(V):
        if not V:return 0
        S=set(V);v=min(S);rest=S-{v};best=rec(tuple(sorted(rest)))
        for w in adj[v]&rest:best=max(best,1+rec(tuple(sorted(rest-{w}))))
        return best
    # Components avoid taking products of independent enumeration spaces.
    result=0;seen=set()
    for root in sorted(vertices):
        if root in seen:continue
        K={root};seen.add(root);stack=[root]
        while stack:
            for w in adj[stack.pop()]-seen:seen.add(w);K.add(w);stack.append(w)
        result+=rec(tuple(sorted(K)))
    return result


def rank_reference(n,E,ops):
    cs,_=graph_components(n,E);owner={v:i for i,K in enumerate(cs) for v in K};adj=[set() for _ in cs]
    for x,y in ops:adj[owner[x]].add(owner[y]);adj[owner[y]].add(owner[x])
    seen=set();d=0
    for root in range(len(cs)):
        if root in seen:continue
        d+=1;seen.add(root);stack=[root]
        while stack:
            for w in adj[stack.pop()]-seen:seen.add(w);stack.append(w)
    return len(ops)-len(cs)+d,len(cs),d


def check(n,E,U,ops,orders=None,compare_old=True):
    result=component_frontier(n,E,U,ops,orders);q=len(ops);expected=[None]*(q+1)
    for S in subsets(range(q)):
        final=(set(U)-{ops[i][0] for i in S})|{ops[i][1] for i in S};cost=literal_nu(final,E);t=len(S)
        expected[t]=cost if expected[t] is None else min(expected[t],cost);counts['literal_candidate_subsets']+=1
    for row in result['frontier']:
        t=row['operations'];S={i for i in range(q) if row['selected_mask']>>i&1};cert=endpoint(n,E,U,ops,S)
        assert len(S)==t and row['cost']==expected[t]==cert['actual_cost']==len(cert['cover'])==len(cert['matching'])
        assert literal_nu(cert['U'],E)==row['cost'];counts['exact_budget_rows']+=1
    assert (result['cycle_rank'],result['component_count'],result['component_tree_count'])==rank_reference(n,E,ops)
    assert result['conditioned_branches']==1<<result['cycle_rank'] and result['peak_component_states']<=4*(q+1)
    assert all(abs(expected[t+1]-expected[t])<=1 for t in range(q))
    for budget in range(q+2):
        row=within_budget(result,budget);assert (row['cost'],row['operations'])==min((cost,t) for t,cost in enumerate(expected) if t<=budget);counts['at_most_budget_optima']+=1
    if compare_old:
        old=exact_frontier(n,E,U,ops,orders);assert [r['cost'] for r in old['frontier']]==expected;counts['pair_width_solver_comparisons']+=1
    try:forest=component_frontier(n,E,U,ops,orders,forest_only=True)
    except ValueError:assert result['cycle_rank']>0;counts['cyclic_forest_rejections']+=1
    else:assert result['cycle_rank']==0 and forest==result;counts['forest_models']+=1
    digest.update(json.dumps((n,E,sorted(U),ops,result),sort_keys=True).encode());counts['generic_frontiers']+=1
    return result


# Every degree2 bipartite ambient graph through4, all U and all injections.
for n in range(5):
    possible=list(combinations(range(n),2))
    for ids in subsets(range(len(possible))):
        E=[e for i,e in enumerate(possible) if i in ids]
        if not allowed(n,E):continue
        for U in subsets(range(n)):
            outside=set(range(n))-U
            for q in range(min(len(U),len(outside))+1):
                for X in combinations(sorted(U),q):
                    for Y in permutations(sorted(outside),q):check(n,E,U,list(zip(X,Y)))
        counts['exhaustive_ambient_graphs']+=1

# All circle-presence traces through10, including full cycles, with no ops.
for n in (4,6,8,10):
    E=[(v,(v+1)%n) for v in range(n)]
    for U in subsets(range(n)):check(n,E,U,[]);counts['cycle_presence_subsets']+=1

rng=random.Random(13112683)
# Random general lists include loops, parallel component edges and high rank.
for trial in range(180):
    n=rng.randrange(0,21);order=list(range(n));rng.shuffle(order)
    E=[(order[i],order[i+1]) for i in range(n-1) if rng.randrange(4)]
    if n>=4 and n%2==0 and len(E)==n-1 and rng.randrange(2):E.append((order[-1],order[0]))
    U=set(rng.sample(range(n),rng.randrange(n+1)));q=rng.randrange(min(len(U),n-len(U),8)+1)
    ops=list(zip(rng.sample(sorted(U),q),rng.sample(sorted(set(range(n))-U),q)))
    original=check(n,E,U,ops);orders=[list(K) for K in original['component_orders']];rng.shuffle(orders)
    for K in orders:
        if rng.randrange(2):K.reverse()
        if len(K)>=4 and sum(a in K and b in K for a,b in E)==len(K):
            off=rng.randrange(len(K));K[:]=K[off:]+K[:off]
    changed=check(n,E,U,ops,orders);assert [r['cost'] for r in changed['frontier']]==[r['cost'] for r in original['frontier']];counts['traversal_invariance_pairs']+=1
    perm=list(range(q));rng.shuffle(perm);reordered=component_frontier(n,E,U,[ops[i] for i in perm])
    assert [r['cost'] for r in reordered['frontier']]==[r['cost'] for r in original['frontier']]
    for row in reordered['frontier']:
        S=[perm[i] for i in range(q) if row['selected_mask']>>i&1];assert endpoint(n,E,U,ops,S)['actual_cost']==row['cost']
    counts['candidate_permutation_models']+=1

# Genuine random component forests with high-arity path/cycle component factors.
for trial in range(220):
    k=rng.randrange(1,11);components=[];E=[];n=0
    for _ in range(k):
        size=rng.randrange(1,7);cyclic=size in (4,6) and rng.randrange(2);K=list(range(n,n+size));n+=size;components.append(K);E.extend(zip(K,K[1:]))
        if cyclic:E.append((K[-1],K[0]))
    available=[K[:] for K in components];U={v for v in range(n) if rng.randrange(2)};ops=[]
    for c in range(1,k):
        choices=[a for a in range(c) if available[a]]
        if not choices or rng.randrange(4)==0:continue
        a=rng.choice(choices);x=rng.choice(available[a]);y=rng.choice(available[c]);available[a].remove(x);available[c].remove(y)
        if rng.randrange(2):x,y=y,x
        U.add(x);U.discard(y);ops.append((x,y))
    rng.shuffle(ops);out=check(n,E,U,ops);assert out['cycle_rank']==0;counts['random_component_forests']+=1

# Exact rank: one loop, parallel pair, triangle of ambient P2 components.
rank_cases=[(4,[(0,1),(1,2),(2,3)],{0,2},[(0,1),(2,3)],2),
            (4,[(0,1),(2,3)],{0,1},[(0,2),(1,3)],1),
            (6,[(0,1),(2,3),(4,5)],{0,2,4},[(0,3),(2,5),(4,1)],1)]
for n,E,U,ops,k in rank_cases:
    out=check(n,E,U,ops);assert out['cycle_rank']==k;counts['explicit_cycle_rank_cases']+=1

# Normalize every public iterable once, including nested supplied orders.
for n,E,U,ops in [(0,[],set(),[]),(6,[(i,(i+1)%6) for i in range(6)],{0,2,4},[(0,1),(2,3),(4,5)]),(8,[(0,1),(1,2),(2,3),(4,5),(5,6),(6,7)],{0,1,4,5},[(0,6),(1,7),(4,2),(5,3)])]:
    expected=component_frontier(n,E,U,ops);orders=expected['component_orders']
    for mask in range(16):
        values=[E,U,ops,orders];args=[iter(v) if mask>>i&1 else v for i,v in enumerate(values)]
        if mask&8:args[3]=(iter(K) for K in orders)
        assert component_frontier(n,*args)==expected;counts['one_shot_generic_controls']+=1


def physical_graph(x):
    b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-c for c in x['colour']]
    assert all(colour[v]!=colour[w] for v in range(len(G)) for w in G[v])
    return G


def physical_certificate(x,G,cert):
    b=x['b'];V=set(range(2*b));U=set(cert['U']);C=set(cert['cover']);M=cert['matching'];E={tuple(sorted(e)) for e in x['P']+x['Q']}
    assert len(C)==len(M)==cert['actual_cost']
    assert len({v for e in M for v in e})==2*len(M) and all(set(e)<=U and tuple(sorted(e)) in E for e in M)
    assert all(a in C or c in C for a,c in E if a in U and c in U)
    selected=set(range(b))|{b+v for v in U-C}|{3*b+v for v in V-U}
    assert len(selected)==3*b-cert['actual_cost'] and all(len(G[v]&selected)<=1 for v in selected)
    counts['actual_dissociation_certificates']+=1

# Physical high-width star, all types throughq4 and random mixed types larger.
for q in (2,4,6,8,16,32,64,128,512):
    patterns=list(product((0,1),repeat=q)) if q<=4 else [tuple(rng.randrange(2) for _ in range(q)) for _ in range(8 if q<=8 else 2 if q<=128 else 1)]
    if q%4==0:patterns.append(tuple(int(i%4>=2) for i in range(q)))
    for types in patterns:
        x=component_star_family(q,types);args=[x[k] for k in ('b','P','Q','B','colour')];U=x['initial_U'];ops=[(a,c) for _,a,c in x['operations']];n=2*x['b'];E=x['P']+x['Q'];data=prepare(*args)
        assert all(len(K)==4 and len(set(U)&set(K))==2 for K,_ in data['owner_components'])
        result=physical_component_frontier(*args,U,x['operations']);G=physical_graph(x)
        assert len(G)==10*q and min(map(len,G))==2 and max(map(len,G))==3 and result['cycle_rank']==0
        if q<=8:
            literal=check(n,E,U,ops);assert [r['cost'] for r in literal['frontier']]==[r['cost'] for r in result['frontier']]
        for row in result['frontier']:
            S=[i for i in range(q) if row['selected_mask']>>i&1];cert=endpoint(n,E,U,ops,S);assert cert['actual_cost']==row['cost'];physical_certificate(x,G,cert)
        for v in (range(len(G)) if q<=8 else sorted({0,x['b'],3*x['b'],len(G)-1})):
            root=next(z for z in range(len(G)) if z!=v);seen={root};stack=[root]
            while stack:
                for w in G[stack.pop()]-seen-{v}:seen.add(w);stack.append(w)
            assert len(seen)==len(G)-1;counts['physical_connectivity_deletions']+=1
        orders=[[2*q+2*i,2*q+2*i+1] for i in range(q//2)]+[list(range(2*q))]+[[2*q+2*i,2*q+2*i+1] for i in range(q//2,q)]
        assert validate(n,E,U,ops,orders)['width']==q//2;counts['balanced_order_width_controls']+=1
        if q%4==0 and tuple(types)==tuple(int(i%4>=2) for i in range(q)):
            r=q//4
            assert [row['cost'] for row in result['frontier']]==[max(2*r-t//2,r,t-2*r) for t in range(q+1)]
            assert (result['best']['cost'],result['best']['operations'])==(r,2*r)
            counts['periodic_family_scales']+=1;counts['periodic_exact_budget_rows']+=q+1
            if q==4:examples.append(dict(name='periodic_star_r1',model=x,result=result))
        if q<=4:
            assert physical_component_frontier(*args,iter(U),iter(x['operations']))==result;counts['one_shot_physical_controls']+=1
        counts['physical_star_models']+=1

# Width lower bound independent of component order, direction or cycle rotation.
for q in (2,4):
    x=component_star_family(q);n=4*q;E=x['P']+x['Q'];ops=[(a,c) for _,a,c in x['operations']];cs=[list(range(2*q))]+[[2*q+2*i,2*q+2*i+1] for i in range(q)]
    for perm in permutations(range(q+1)):
        for reverse_leaves in (False,True):
            for direction in (1,-1):
                base=cs[0][::direction]
                for off in range(2*q):
                    circle=base[off:]+base[:off];orders=[circle if i==0 else cs[i][::-1] if reverse_leaves else cs[i] for i in perm]
                    d=validate(n,E,x['initial_U'],ops,orders);assert d['width']>=q//2;counts['width_order_direction_rotation_controls']+=1

# Input restrictions remain checked instead of treating invalid lists as forests.
invalid=[(3,[(0,1),(1,2),(2,0)],set(),[]),(4,[(0,1),(0,2),(0,3)],{0},[(0,1)]),(4,[(0,1)],{0,2},[(0,1),(0,3)]),(4,[(0,1)],{0,2},[(0,1),(2,1)])]
for args in invalid:
    try:component_frontier(*args)
    except ValueError:counts['invalid_input_rejections']+=1
    else:raise AssertionError('Invalid ambient graph or duplicate endpoint accepted')

report=dict(scope='Exact full operation-count frontier on ambient degree2 bipartite graphs, parameterized by candidate COMPONENT MULTIGRAPH cycle rank. Direct forest messages, conditioning loops/parallel edges once, complete masks, unit matching costs. Physical star family has minimum complete-component widthq/2 and k0; periodic q4r frontier max(2r-floor(t/2),r,t-2r). Fixed-list results only; no weightedTH, universal graph coefficient or grid embedding.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/component-cycle-frontier-check.json'));args=p.parse_args();dest=Path(args.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
