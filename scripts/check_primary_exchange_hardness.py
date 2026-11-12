"""Literal matching, complete source controls and physical primary reduction."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from functools import lru_cache
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from primary_exchange_hardness import charged_vertex_cover_template,batch_ledger,batch_from_source_cover,certificate_for_batch,connected_primary_reduction,lift_normalized_cover,project_normalized_cover
from owner_matching_certificate import prepare
from component_cycle_frontier import component_frontier
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();examples=[];largest=0;rng=random.Random(13112697)


def components(n,E):
    adj=[set() for _ in range(n)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    seen=set();out=[]
    for root in range(n):
        if root in seen:continue
        seen.add(root);K={root};stack=[root]
        while stack:
            for w in adj[stack.pop()]-seen:seen.add(w);K.add(w);stack.append(w)
        out.append(K)
    return out,adj


def literal_tau(h,E):
    best=None
    for mask in range(1<<h):
        if all(mask>>a&1 or mask>>b&1 for a,b in E):
            value=(mask.bit_count(),mask)
            if best is None or value<best:best=value
    return best[0],{v for v in range(h) if best[1]>>v&1}


def branch_tau(h,E):
    """Independent exact include-v / include-N(v) cover branching."""
    adj=[0]*h
    for a,b in E:adj[a]|=1<<b;adj[b]|=1<<a
    @lru_cache(None)
    def solve(V):
        active=[v for v in range(h) if V>>v&1 and adj[v]&V]
        if not active:return 0
        v=max(active,key=lambda z:(adj[z]&V).bit_count());N=adj[v]&V
        return min(1+solve(V&~(1<<v)),N.bit_count()+solve(V&~(N|(1<<v))))
    return solve((1<<h)-1)


def matching_number(V,E):
    """Independent augmenting paths, no run-parity or ledger identity."""
    V=set(V);adj={v:set() for v in V};colour={}
    for a,b in E:
        if a in V and b in V:adj[a].add(b);adj[b].add(a)
    for root in sorted(V):
        if root in colour:continue
        colour[root]=0;stack=[root]
        while stack:
            v=stack.pop()
            for w in adj[v]:
                if w not in colour:colour[w]=1-colour[v];stack.append(w)
                else:assert colour[w]!=colour[v]
    matched={}
    def aug(v,seen):
        for w in adj[v]:
            if w in seen:continue
            seen.add(w)
            if w not in matched or aug(matched[w],seen):matched[w]=v;return True
        return False
    for v in sorted(V):
        if colour[v]==0:aug(v,set())
    return len(matched)


def articulation(G):
    """Iterative low-link reference, calibrated against literal deletions."""
    n=len(G);disc=[-1]*n;low=[-1]*n;parent=[-1]*n;children=[0]*n;timer=0;art=set();cc=0
    for root in range(n):
        if disc[root]>=0:continue
        cc+=1;disc[root]=low[root]=timer;timer+=1;stack=[(root,iter(G[root]))]
        while stack:
            v,it=stack[-1]
            try:w=next(it)
            except StopIteration:
                stack.pop();p=parent[v]
                if p>=0:
                    low[p]=min(low[p],low[v])
                    if parent[p]>=0 and low[v]>=disc[p]:art.add(p)
                elif children[v]>1:art.add(v)
                continue
            if disc[w]<0:
                parent[w]=v;children[v]+=1;disc[w]=low[w]=timer;timer+=1;stack.append((w,iter(G[w])))
            elif w!=parent[v]:low[v]=min(low[v],disc[w])
    return cc,art


def cc_after_delete(G,deleted=None):
    seen={deleted} if deleted is not None else set();cc=0
    for root in range(len(G)):
        if root in seen:continue
        cc+=1;seen.add(root);stack=[root]
        while stack:
            for w in G[stack.pop()]-seen:seen.add(w);stack.append(w)
    return cc


def source_bridgeless(h,H):
    cs,adj=components(h,H)
    if len(cs)!=1:return False
    for a,b in H:
        seen={a};stack=[a]
        while stack:
            v=stack.pop()
            for w in adj[v]-seen:
                if {v,w}=={a,b}:continue
                seen.add(w);stack.append(w)
        if len(seen)!=h:return False
    return True


def physical_graph(x):
    b=x['b'];G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(2*b):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-c for c in x['colour']]
    assert all(colour[v]!=colour[w] for v in range(len(G)) for w in G[v])
    return G


def inspect_model(x,full_deletions=False):
    global largest
    data=prepare(*[x[k] for k in ('b','P','Q','B','colour')]);n=2*x['b'];U=set(x['initial_U']);q=x['q'];h=x['h'];H=x['H']
    assert len(U)==x['b'] and all(len(K)==4 and len(U&set(K))==2 for K,_ in data['owner_components'])
    owner={v:i for i,(K,_) in enumerate(data['owner_components']) for v in K};used=set()
    for i,a,c in x['operations']:
        assert i==owner[a]==owner[c] and i not in used and a in U and c not in U;used.add(i)
        final=(U-{a})|{c};deg=Counter(v for a,b in x['B'] if a not in final and b not in final for v in (a,b));assert max(deg.values(),default=0)<=1;counts['individual_permission_controls']+=1
    cs,_=components(n,x['P']+x['Q']);assert all(len(K) in (2,4) for K in cs) and len(cs)==2*q-len(H)
    for K in cs:counts['auxiliary_P2_components' if len(K)==2 else 'auxiliary_P4_components']+=1
    own={v:i for i,K in enumerate(cs) for v in K};KE=[(own[a],own[b]) for _,a,b in x['operations']];kc,_=components(len(cs),KE);hc,_=components(h,H)
    assert q-len(cs)+len(kc)==len(H)+len(hc);counts['cycle_rank_identity_models']+=1
    G=physical_graph(x);assert len(G)==10*(q+h) and min(map(len,G))==2 and max(map(len,G))==3;largest=max(largest,len(G))
    cc,art=articulation(G);assert cc==len(hc)
    if source_bridgeless(h,H):assert cc==1 and not art;counts['two_connected_physical_models']+=1
    if full_deletions:
        base=cc_after_delete(G);assert base==cc
        actual={v for v in range(len(G)) if cc_after_delete(G,v)>base};assert actual==art;counts['literal_physical_vertex_deletions']+=len(G)
    counts['physical_models']+=1
    return G


def check_batch(x,G,S):
    q=x['q'];S=set(S);U=(set(x['initial_U'])-S)|{q+i for i in S};E=x['P']+x['Q'];cert=certificate_for_batch(x,S);ledger=cert['ledger'];cost=matching_number(U,E)
    assert set(cert['U'])==U and cert['actual_cost']==ledger['cost']==cost
    C=set(cert['cover']);M=cert['matching'];EE={tuple(sorted(e)) for e in E}
    assert len(C)==len(M)==cost and len({v for e in M for v in e})==2*len(M)
    assert all(set(e)<=U and tuple(sorted(e)) in EE for e in M) and all(a in C or b in C for a,b in EE if a in U and b in U)
    b=x['b'];chosen=set(range(b))|{b+v for v in cert['witnesses']}|{3*b+v for v in cert['owners']}
    assert len(chosen)==3*b-cost==cert['beta_I_lower'] and all(len(G[v]&chosen)<=1 for v in chosen)
    deg=Counter(v for a,b in x['B'] if a not in U and b not in U for v in (a,b));assert max(deg.values(),default=0)<=1
    Z=set(ledger['touched_groups']);R=set(ledger['rounded_candidates']);roundedU=(set(x['initial_U'])-R)|{q+i for i in R};rounded=matching_number(roundedU,E)
    expected=len(Z)+sum(a not in Z and b not in Z for a,b in x['H']);assert rounded==ledger['rounded_cost']==expected<=cost
    sourceC=set(ledger['source_cover']);assert len(sourceC)<=rounded and all(a in sourceC or b in sourceC for a,b in x['H'])
    counts['arbitrary_batch_certificates']+=1;counts['rounding_matching_controls']+=1
    digest.update(json.dumps([x['h'],x['H'],sorted(S),cost,ledger],sort_keys=True).encode())
    return cost


# All source graphs through4, with full candidate enumeration wheneverq<=12.
for h in range(1,5):
    possible=list(combinations(range(h),2))
    for emask in range(1<<len(possible)):
        H=[e for i,e in enumerate(possible) if emask>>i&1];x=charged_vertex_cover_template(h,H);q=x['q'];tau,C=literal_tau(h,H);assert branch_tau(h,H)==tau;counts['independent_cover_solver_calibrations']+=1
        G=inspect_model(x,full_deletions=source_bridgeless(h,H))
        masks=range(1<<q) if q<=12 else [rng.randrange(1<<q) for _ in range(120)]
        best=None
        for mask in masks:
            S={i for i in range(q) if mask>>i&1};cost=check_batch(x,G,S);assert cost>=tau;best=cost if best is None else min(best,cost)
        for zmask in range(1<<h):
            Z={v for v in range(h) if zmask>>v&1};S={i for v in Z for i in x['groups'][v]};cost=check_batch(x,G,S);assert cost==len(Z)+sum(a not in Z and b not in Z for a,b in H);best=min(best,cost);counts['whole_group_batches']+=1
        assert best==tau
        S=batch_from_source_cover(x,C);cert=certificate_for_batch(x,S);assert cert['actual_cost']==tau
        if q<=12:counts['exhaustive_batch_source_models']+=1
        if h<=3 or H==possible:
            out=component_frontier(2*x['b'],x['P']+x['Q'],x['initial_U'],[(a,b) for _,a,b in x['operations']]);assert out['best']['cost']==tau;counts['full_frontier_optimum_comparisons']+=1
        counts['all_small_source_graphs']+=1
        if h==3 and len(H)==3:examples.append(dict(name='triangle_unbudgeted_primary',model=x,minimum_source_cover=sorted(C),optimal_certificate=cert,initial_cost=len(H),all_selected_cost=h))

# Larger independent arbitrary-source controls and exact source covers.
for h in (5,6,8):
    for trial in range(4):
        H=[e for e in combinations(range(h),2) if rng.randrange(3)==0];x=charged_vertex_cover_template(h,H);G=inspect_model(x);tau,C=literal_tau(h,H)
        for _ in range(48):
            S={i for i in range(x['q']) if rng.randrange(2)};assert check_batch(x,G,S)>=tau
        S=batch_from_source_cover(x,C);assert check_batch(x,G,S)==tau;counts['larger_source_models']+=1

# Connected normalization: lift all F covers; decode arbitrary J covers/batches.
normalizations=[(0,[]),(1,[]),(2,[]),(2,[(0,1)]),(3,[]),(3,[(0,1),(1,2)]),(3,list(combinations(range(3),2))),(4,[]),(4,[(0,1),(1,2),(2,3)]),(4,[(i,(i+1)%4) for i in range(4)]),(4,list(combinations(range(4),2)))]
for h,F in normalizations:
    reduction=connected_primary_reduction(h,F);norm=reduction['normalization'];x=reduction['template'];G=inspect_model(x);tau,minimum=literal_tau(h,F);expected=tau+reduction['additive_offset']
    assert source_bridgeless(norm['k'],norm['H'])
    if h<=2:assert branch_tau(norm['k'],norm['H'])==expected;counts['normalized_exact_cover_comparisons']+=1
    for mask in range(1<<h):
        C={v for v in range(h) if mask>>v&1}
        if not all(a in C or b in C for a,b in F):continue
        lifted=lift_normalized_cover(norm,C);assert len(lifted)==len(C)+reduction['additive_offset'];S=batch_from_source_cover(x,lifted);cost=check_batch(x,G,S);assert cost==len(lifted)
        projected=project_normalized_cover(norm,lifted);assert len(projected)<=len(C) and all(a in projected or b in projected for a,b in F);counts['normalized_lift_projection_controls']+=1
    lifted=lift_normalized_cover(norm,minimum);assert check_batch(x,G,batch_from_source_cover(x,lifted))==expected
    _,adj=components(norm['k'],norm['H'])
    for _ in range(8):
        C=set(range(norm['k']));order=list(C);rng.shuffle(order)
        for v in order:
            if adj[v]<=C:C.remove(v)
        projected=project_normalized_cover(norm,C);assert len(projected)<=len(C)-reduction['additive_offset'] and all(a in projected or b in projected for a,b in F);counts['normalized_arbitrary_cover_projections']+=1
        S={i for i in range(x['q']) if rng.randrange(2)};cost=check_batch(x,G,S);CJ=batch_ledger(x,S)['source_cover'];CF=project_normalized_cover(norm,CJ);assert len(CF)<=cost-reduction['additive_offset'];counts['normalized_batch_to_original_cover_controls']+=1
    counts['connected_normalization_models']+=1

# Large unit source families, with explicit source lower witnesses.
for h,kind in [(16,'cycle'),(64,'cycle'),(128,'cycle'),(16,'clique'),(32,'clique')]:
    H=[(i,(i+1)%h) for i in range(h)] if kind=='cycle' else list(combinations(range(h),2));C=set(range(0,h,2)) if kind=='cycle' else set(range(h-1));tau=h//2 if kind=='cycle' else h-1
    x=charged_vertex_cover_template(h,H);G=inspect_model(x);assert check_batch(x,G,batch_from_source_cover(x,C))==tau
    for _ in range(3):assert check_batch(x,G,{i for i in range(x['q']) if rng.randrange(2)})>=tau
    counts['large_source_family_models']+=1

# One-shot APIs must not consume iterators twice.
x=charged_vertex_cover_template(3,((a,b) for a,b in combinations(range(3),2)));S={0,3,6};C={0,1};norm=connected_primary_reduction(2,iter([(0,1)]))['normalization'];Jcover=lift_normalized_cover(norm,{0})
assert x==charged_vertex_cover_template(3,list(combinations(range(3),2)));counts['one_shot_constructor_controls']+=1
for f,args,index in [(batch_ledger,[x,S],1),(certificate_for_batch,[x,S],1),(batch_from_source_cover,[x,C],1),(lift_normalized_cover,[norm,{0}],1),(project_normalized_cover,[norm,Jcover],1)]:
    expected=f(*args);once=args[:];once[index]=iter(once[index]);assert f(*once)==expected;counts['one_shot_api_controls']+=1
invalid=[(0,[]),(True,[]),(2,[(0,0)]),(2,[(0,2)]),(2,[(0,1,2)])]
for args in invalid:
    try:charged_vertex_cover_template(*args)
    except ValueError:counts['invalid_source_rejections']+=1
    else:raise AssertionError('Invalid source accepted')
for f,args in [(batch_ledger,[x,[-1]]),(batch_ledger,[x,[x['q']]]),(batch_from_source_cover,[x,[]]),(lift_normalized_cover,[norm,[]]),(project_normalized_cover,[norm,[]])]:
    try:f(*args)
    except ValueError:counts['invalid_certificate_rejections']+=1
    else:raise AssertionError('Invalid certificate accepted')

report=dict(scope='UNBUDGETED primary unit matching-cost minimization on all subsets of a fixed distinct-owner candidate list. Exact charged-group rounding and optimumtauH; connected bridgeless normalization gives NP-complete primarycost decision on two-connected bipartite physical min2/max3 graphs, minimum square omissions and auxiliaryP4/P2. NO operation budget or tie-break. Fixed-list only, not all-helper global omission, SF/beta, weightedTH or grid hardness.',counts=dict(sorted(counts.items())),largest_physical_order=largest,digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/primary-exchange-hardness-check.json'));a=p.parse_args();dest=Path(a.output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(dict(counts=report['counts'],largest_physical_order=largest),sort_keys=True))
