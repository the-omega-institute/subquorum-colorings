"""Literal compiler semantics, weighted closed conflicts, physical neutral escapes."""
from pathlib import Path
from itertools import combinations,permutations,product
from collections import Counter
import argparse,json,random,sys,hashlib
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from matching_credit_exchange import credit_constraints,closed_conflict_optimum,matching_credit_batch,neutral_plateau_family,odd_path_escape_family
from cover_saturated_exchange import cyclic_dependency_family
from owner_matching_certificate import prepare
from all_helper_optimization import score
from mixed_owner_bridges import _minimum_omission
if not __debug__:raise RuntimeError('Assertions must be enabled')
counts=Counter();rng=random.Random(13112612);digest=hashlib.sha256();examples=[]


def subsets(S):
    S=sorted(S)
    for mask in range(1<<len(S)):yield {v for i,v in enumerate(S) if mask>>i&1}


def literal_matchings(U,E):
    U=set(U);adj={v:set() for v in U}
    for a,b in E:
        if a in U and b in U:adj[a].add(b);adj[b].add(a)
    def rec(V):
        if not V:yield [];return
        v=min(V)
        yield from rec(V-{v})
        for u in sorted(adj[v]&V):
            for M in rec(V-{v,u}):yield [(min(v,u),max(v,u))]+M
    Ms=list(rec(U));size=max(map(len,Ms),default=0)
    return [M for M in Ms if len(M)==size]


def path_cost(U,E):
    U=set(U);adj={v:set() for v in U}
    for a,b in E:
        if a in U and b in U:adj[a].add(b);adj[b].add(a)
    assert max(map(len,adj.values()),default=0)<=2
    remaining=set(U);cost=0
    while remaining:
        K={min(remaining)};todo=list(K)
        while todo:
            for v in adj[todo.pop()]-K:K.add(v);todo.append(v)
        # Every cycle in the physical A is even; all other blocks are paths.
        if all(len(adj[v])==2 for v in K):assert len(K)%2==0
        cost+=len(K)//2;remaining-=K
    return cost


def permitted(n,B,U):
    S=set(range(n))-set(U);degree={v:0 for v in S}
    for a,b in B:
        if a in S and b in S:degree[a]+=1;degree[b]+=1
    return all(d<=1 for d in degree.values())


def feasible(S,D,F,blocked):
    return not set(S)&set(blocked) and all(a not in S or b in S for a,b in D) and not any(a in S and b in S for a,b in F)


def compiler_check(n,E,U,C,M,ops):
    z=credit_constraints(n,iter(E),U,C,M,iter(ops));mate={v:w for a,b in M for v,w in ((a,b),(b,a))}
    best=(-1,0)
    for S in subsets(range(len(ops))):
        X={ops[i][0] for i in S};Y={ops[i][1] for i in S};R={mate[x] for x in X if x in mate};new=(set(U)-X)|Y;final=set(C)-R
        literal=all(a in final or b in final for a,b in E if a in new and b in new)
        compiled=feasible(S,z['dependencies'],z['conflicts'],z['blocked'])
        assert literal==compiled
        if literal:
            assert len(R)==sum(z['weights'][i] for i in S)
            assert len(literal_matchings(new,E)[0])==len(C)-len(R)
            best=max(best,(len(R),-len(S)));counts['literal_tight_matching_cover_transfers']+=1
        counts['literal_compiler_subsets']+=1
    out=closed_conflict_optimum(z['weights'],z['dependencies'],z['conflicts'],z['blocked'])
    assert (out['credit'],-len(out['selected']))==best
    counts['literal_compiler_models']+=1


# Every simple graph n<=4, every U, every tight minimum cover and maximum
# matching, every partial injection from U minus C to its complement (<=2).
for n in range(5):
    possible=list(combinations(range(n),2))
    for mask in range(1<<len(possible)):
        E=[e for i,e in enumerate(possible) if mask>>i&1]
        for U in subsets(range(n)):
            Ms=literal_matchings(U,E);nu=len(Ms[0])
            Cs=[C for C in subsets(U) if len(C)==nu and all(a in C or b in C for a,b in E if a in U and b in U)]
            for C in Cs:
                for M in Ms:
                    I=sorted(U-C);outside=sorted(set(range(n))-U)
                    for k in range(min(len(I),len(outside))+1):
                        for X in combinations(I,k):
                            for Y in permutations(outside,k):compiler_check(n,E,U,C,M,list(zip(X,Y)))


def optimization_check(weights,D,F,blocked):
    q=len(weights);states=[S for S in subsets(range(q)) if feasible(S,D,F,blocked)]
    expected=max((sum(weights[i] for i in S),-len(S)) for S in states)
    covers=[K for K in subsets(range(q)) if all(a in K or b in K for a,b in F)]
    supplied=[None,min(covers,key=lambda K:(len(K),sorted(K)))]
    if q<=2:supplied+=covers
    for K in supplied:
        z=closed_conflict_optimum(weights,D,F,blocked,K);S=set(z['selected'])
        assert feasible(S,D,F,blocked) and (z['credit'],-len(S))==expected
        assert z['assignments']==1<<len(z['vertex_cover'])
        counts['literal_weighted_optimizer_runs']+=1
    counts['literal_weighted_constraint_models']+=1


# All directed implication graphs, simple conflict graphs, blocker subsets,
# and binary credits for q<=3. Self implications are covered separately below.
for q in range(4):
    arcs=[(i,j) for i in range(q) for j in range(q) if i!=j];edges=list(combinations(range(q),2))
    for dm in range(1<<len(arcs)):
        D=[e for i,e in enumerate(arcs) if dm>>i&1]
        for fm in range(1<<len(edges)):
            F=[e for i,e in enumerate(edges) if fm>>i&1]
            for blocked in subsets(range(q)):
                for weights in product((0,1),repeat=q):optimization_check(weights,D,F,blocked)


for q in (4,5,6,8,10):
    for trial in range(45):
        D=[(i,j) for i in range(q) for j in range(q) if rng.randrange(9)==0]
        F=[(i,j) for i in range(q) for j in range(i+1,q) if rng.randrange(4)==0]
        blocked={i for i in range(q) if rng.randrange(9)==0}
        weights=[rng.choice([0,0,1,3,10**120+7]) for i in range(q)]
        optimization_check(weights,D,F,blocked)
        counts['large_integer_weight_controls']+=any(w>10**100 for w in weights)


# Each distinct constraint source and zero-credit prerequisite has a control.
controls=[
 (5,[(0,1),(1,2)],{0,1,2},{1},[(0,1)],[(0,3),(2,4)]),
 (4,[(0,1),(1,2)],{0,1,2},{1},[(0,1)],[(0,3)]),
 (6,[(0,1),(2,3),(4,5)],{0,1,2,3},{0,2},[(0,1),(2,3)],[(1,4),(3,5)]),
 (6,[(0,1),(2,3),(2,4)],{0,1,2,3},{0,2},[(0,1),(2,3)],[(1,4),(3,5)]),
 (3,[(0,1),(0,2)],{0,1},{0},[(0,1)],[(1,2)]),
 (6,[(0,1),(1,2),(2,3)],{0,1,2,3},{1,2},[(0,1),(2,3)],[(0,4),(3,5)]),
 (5,[(0,1),(2,3)],{0,1,2},{0},[(0,1)],[(1,3),(2,4)]),
]
for args in controls:compiler_check(*args);counts['constraint_source_controls']+=1
z=credit_constraints(*controls[0]);out=closed_conflict_optimum(z['weights'],z['dependencies'],z['conflicts'],z['blocked'])
assert out['credit']==1 and out['selected']==[0,1]
assert credit_constraints(*controls[4])['blocked']==[0]


def physical(x,result):
    z=result['certificate'];b=x['b'];n=2*b;E=x['P']+x['Q'];U=set(z['U']);C=set(z['cover']);M=z['matching'];T=set(z['witnesses'])
    assert len(C)==len(M)==z['actual_cost']==path_cost(U,E)
    assert len({v for e in M for v in e})==2*len(M)
    assert all(set(e)<=U and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in M)
    assert C<=U and all(a in C or c in C for a,c in E if a in U and c in U)
    assert T==U-C and permitted(n,x['B'],U)
    if n<=16:assert len(literal_matchings(U,E)[0])==z['actual_cost'];counts['literal_physical_matchings']+=1
    initial=set(z['initial_U']);oldC=set(z['initial_cover']);oldM=z['initial_matching']
    assert len(oldC)==len(oldM)==z['initial_cost'] and oldC<=initial
    assert all(a in oldC or c in oldC for a,c in E if a in initial and c in initial)
    assert len({v for e in oldM for v in e})==2*len(oldM)
    assert all(set(e)<=initial and tuple(sorted(e)) in {tuple(sorted(f)) for f in E} for e in oldM)
    charges=z['charged_edges'];assert len({tuple(r['edge']) for r in charges})==len(charges)
    assert all(r['removed'] in r['edge'] and tuple(r['edge']) in {tuple(sorted(e)) for e in oldM} for r in charges)
    G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
    assert all(colour[v]!=colour[w] for v in range(5*b) for w in G[v]) and max(map(len,G),default=0)<=3
    D=set(range(b))|{b+v for v in T}|{3*b+v for v in z['owners']}
    assert len(D)==z['beta_I_lower']==3*b-z['actual_cost'] and all(len(G[v]&D)<=1 for v in D)
    digest.update(json.dumps([x,result],sort_keys=True).encode());counts['physical_matching_cover_certificates']+=1


for m in list(range(1,25))+[32,64,128]:
    x=neutral_plateau_family(m);args=[x[k] for k in ('b','P','Q','B','colour')]
    result=matching_credit_batch(*args,x['initial_U'],x['operations'],x['cover'],x['matching']);z=result['certificate']
    assert z['actual_cost']==0 and z['beta_I_lower']==12*m and len(z['neutral_removals'])==m
    assert result['optimization']['credit']==m and len(result['optimization']['selected'])==2*m
    assert result['optimization']['assignments']==1 and not result['constraints']['conflicts']
    physical(x,result);counts['plateau_escape_family_scales']+=1
    if m in (1,2):examples.append(dict(name='unbounded plateau escape',model=x,result=result))


for r in list(range(4,49,2))+[64,96,128]:
    x=odd_path_escape_family(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    result=matching_credit_batch(*args,x['initial_U'],x['operations'],x['cover'],x['matching']);z=result['certificate']
    assert z['actual_cost']==0 and z['beta_I_lower']==6*r and len(z['neutral_removals'])==1
    assert result['optimization']['credit']==r-1 and len(result['optimization']['selected'])==r and result['optimization']['assignments']==1
    physical(x,result);counts['odd_path_escape_family_scales']+=1


for r in list(range(3,25))+[32,64,128]:
    x=cyclic_dependency_family(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    C=[4*i for i in range(r)];M=[(4*i,4*i+1) for i in range(r)]
    result=matching_credit_batch(*args,x['initial_U'],x['operations'],C,M)
    assert result['certificate']['actual_cost']==0 and result['optimization']['credit']==r and not result['certificate']['neutral_removals']
    physical(x,result);counts['cyclic_escape_family_scales']+=1


def fixed_physical(colour,Q,U,ops,C,M):
    x=dict(b=4,P=[(0,1),(2,3),(4,5),(6,7)],Q=Q,
           B=[(0,4),(4,1),(1,5),(5,0),(2,6),(6,3),(3,7),(7,2)],colour=colour)
    args=[x[k] for k in ('b','P','Q','B','colour')];result=matching_credit_batch(*args,U,ops,C,M)
    physical(x,result);examples.append(dict(name='fixed physical constraint control',model=x,initial_U=sorted(U),operations=ops,result=result))
    return result


z=fixed_physical([0,0,1,1,1,1,0,0],[(1,2)],{0,1,2,3},[[0,0,4],[1,3,6]],{1,2},[(0,1),(2,3)])
assert z['constraints']['conflicts']==[[0,1]] and z['certificate']['actual_cost']==1
counts['physical_old_cover_edge_conflicts']=1
z=fixed_physical([1,1,1,1,0,0,0,0],[(2,4)],{0,1,2,3},[[0,1,4]],{0,2},[(0,1),(2,3)])
assert z['certificate']['actual_cost']==1 and z['certificate']['added']==[4] and 2 in z['certificate']['U']
fixture=examples[-1]['model'];final=set(z['certificate']['U'])
assert any(a in final and c in final and {a,c}=={2,4} for a,c in fixture['P']+fixture['Q'])
assert 4 in z['certificate']['added'] and 2 in z['certificate']['cover']
counts['physical_nonisolated_addition_savings']=1


for n in (8,12,16,24,32,64):
    for trial in range(30):
        L=list(range(0,n,2));RR=list(range(1,n,2));rng.shuffle(L);rng.shuffle(RR)
        P=list(zip(L[::2],L[1::2]))+list(zip(RR[::2],RR[1::2]));rng.shuffle(RR);k=rng.randrange(n//2+1);Q=list(zip(L[:k],RR[:k]))
        order=[v for pair in zip(L,RR) for v in pair];B=[]
        for off in range(0,n,4):
            K=order[off:off+4];B+=list(zip(K,K[1:]+K[:1]))
        colour=[v%2 for v in range(n)];args=[n//2,P,Q,B,colour];data=prepare(*args)
        U=set().union(*(_minimum_omission(K,c) for K,c in data['owner_components']))
        if trial%3==0:U|={v for v in range(n) if rng.randrange(5)==0}
        T,M=score(n,P,Q,U);C=U-T;ops=[]
        for i,(K,_) in enumerate(data['owner_components']):
            choices=[(a,c) for a in sorted((set(K)&U)-C) for c in sorted(set(K)-U) if permitted(n,B,(U-{a})|{c})]
            if choices:
                a,c=rng.choice(choices);ops.append([i,a,c])
        ops=ops[:8];x=dict(b=n//2,P=P,Q=Q,B=B,colour=colour)
        result=matching_credit_batch(*args,U,ops,C,M);physical(x,result)
        mate={v:w for a,c in M for v,w in ((a,c),(c,a))};best=(-1,0);true_cost=len(M);true_selected=[]
        for S in subsets(range(len(ops))):
            X={ops[i][1] for i in S};Y={ops[i][2] for i in S};new=(U-X)|Y;R={mate[a] for a in X if a in mate};final=C-R
            cost=path_cost(new,P+Q)
            if cost<true_cost:true_cost=cost;true_selected=sorted(S)
            literal=all(a in final or c in final for a,c in P+Q if a in new and c in new)
            compiled=feasible(S,result['constraints']['dependencies'],result['constraints']['conflicts'],result['constraints']['blocked'])
            assert literal==compiled and permitted(n,B,new)
            if literal:
                assert path_cost(new,P+Q)==len(M)-len(R);best=max(best,(len(R),-len(S)))
            counts['physical_literal_candidate_subsets']+=1
        opt=result['optimization'];assert (opt['credit'],-len(opt['selected']))==best
        assert result['certificate']['actual_cost']>=true_cost
        if result['certificate']['actual_cost']>true_cost:
            counts['physical_rule_actual_cost_gaps']+=1
            if counts['physical_rule_actual_cost_gaps']==1:
                examples.append(dict(name='fixed inherited cover can miss the actual fixed-list optimum',
                                     model=x,initial_U=sorted(U),cover=sorted(C),matching=M,operations=ops,
                                     result=result,actual_fixed_list_optimum=true_cost,actual_selected=true_selected))
        counts['physical_rule_equals_actual_fixed_list_optimum']+=result['certificate']['actual_cost']==true_cost
        counts['physical_fixed_list_rule_optima']+=1
        counts['random_physical_nonempty_batches']+=bool(opt['selected'])
        counts['random_physical_conflict_models']+=bool(result['constraints']['conflicts'])


try:closed_conflict_optimum([1,1],[],[(0,1)],[],[])
except ValueError:pass
else:raise AssertionError('Invalid conflict vertex cover accepted')
try:closed_conflict_optimum([-1],[],[],[])
except ValueError:pass
else:raise AssertionError('Negative credits accepted')
counts['invalid_contract_controls']=2
report=dict(scope='Literal compiler equivalence over all simple graphs through4 vertices with tight matching/cover pairs and all partial injection operations; all implication/conflict/blocker/binary-credit systems through3 candidates; seeded larger integer controls; physical fixed-list optimum comparisons, nonisolated addition, old-cover conflict, and all-scale plateau/odd/cyclic escapes. No unrestricted physical optimum from generic finite enumeration; no Lean.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),examples=examples)
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/matching-credit-exchange-check.json'));args=p.parse_args()
Path(args.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report['counts'],sort_keys=True))
