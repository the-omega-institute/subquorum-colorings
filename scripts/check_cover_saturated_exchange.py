"""Independent finite checks of cover saturation and coordinated physical batches."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from cover_saturated_exchange import forced_minimum_cover,coordinated_exchange,dependency_batch,cyclic_dependency_family,shared_odd_path_family
from omission_conflict_graph import conflict_data
from owner_matching_certificate import prepare
from all_helper_optimization import score
if not __debug__:raise RuntimeError('Assertions must be enabled')
counts=Counter();rng=random.Random(13112608);digest=hashlib.sha256();examples=[]


def subsets(S):
    S=sorted(S)
    for mask in range(1<<len(S)):yield {v for i,v in enumerate(S) if mask>>i&1}


def literal_matching(U,E):
    U=set(U);memo={};adj={v:set() for v in U}
    for a,b in E:
        if a in U and b in U:adj[a].add(b);adj[b].add(a)
    def rec(S):
        if not S:return 0
        key=tuple(sorted(S))
        if key in memo:return memo[key]
        v=min(S);best=rec(S-{v})
        for u in adj[v]&S:best=max(best,1+rec(S-{v,u}))
        memo[key]=best;return best
    return rec(U)


def permitted(n,B,U):
    S=set(range(n))-set(U);degree={v:0 for v in S}
    for a,b in B:
        if a in S and b in S:degree[a]+=1;degree[b]+=1
    return all(v<=1 for v in degree.values())


def isolation(U,X,Y,E):
    new=(set(U)-set(X))|set(Y)
    return not any((a in Y and b in new) or (b in Y and a in new) for a,b in E)


def abstract(n,E,U):
    U=set(U);nu=literal_matching(U,E)
    covers=[C for C in subsets(U) if all(a in C or b in C for a,b in E if a in U and b in U)]
    tau=min(map(len,covers));mins=[C for C in covers if len(C)==tau];assert tau==nu
    for X in subsets(U):
        exact=literal_matching(U-X,E);contains=any(X<=C for C in mins)
        rec=forced_minimum_cover(n,iter(E),U,X)
        assert rec['applicable']==contains==(exact==nu-len(X))
        assert rec['initial_cost']==nu and rec['deletion_cost']==exact
        if contains:
            C=set(rec['cover']);assert C in mins and X<=C
            for Y in subsets(set(range(n))-U):
                if len(X)!=len(Y) or not isolation(U,X,Y,E):continue
                assert literal_matching((U-X)|Y,E)==nu-len(X)
                counts['literal_final_isolation_replacements']+=1
        counts['literal_cover_deletion_equivalences']+=1
    counts['bipartite_graph_induced_set_models']+=1


# All crossing-edge subgraphs on the fixed balanced split, every U and X, n<=5.
# n=6: all512 crossing-edge graphs, U=V and every X. No all-labelled-graph claim.
for n in range(7):
    p=n//2;possible=list(product(range(p),range(p,n)))
    for mask in range(1<<len(possible)):
        E=[e for i,e in enumerate(possible) if mask>>i&1]
        Us=[set(range(n))] if n==6 else subsets(range(n))
        for U in Us:abstract(n,E,U)


def physical(x,z,connectivity=False):
    b=x['b'];n=2*b;E=x['P']+x['Q'];U=set(z['U']);C=set(z['cover']);M=z['matching'];T=set(z['witnesses'])
    old=set(z['initial_U']);oldC=set(z['initial_cover']);oldM=z['initial_matching']
    edge_set={tuple(sorted(e)) for e in E}
    assert oldC<=old and len(oldC)==len(oldM)==z['initial_cost']
    assert len({v for e in oldM for v in e})==2*len(oldM)
    assert all(set(e)<=old and tuple(sorted(e)) in edge_set for e in oldM)
    assert all(a in oldC or c in oldC for a,c in E if a in old and c in old)
    assert permitted(n,x['B'],U) and len(U)==len(z['initial_U'])
    assert all(set(e)<=U for e in M) and len({v for e in M for v in e})==2*len(M)
    assert all(tuple(sorted(e)) in edge_set for e in M)
    assert len(M)==len(C)==z['actual_cost']
    assert C<=U and all(a in C or c in C for a,c in E if a in U and c in U)
    assert T==U-C and not any(a in T and c in T for a,c in E)
    charges=z['charged_edges'];initial={tuple(sorted(e)) for e in z['initial_matching']}
    assert len(charges)==z['saved_matching_edges'] and len({tuple(r['edge']) for r in charges})==len(charges)
    assert all(tuple(r['edge']) in initial and r['removed'] in r['edge'] for r in charges)
    if n<=16:assert literal_matching(U,E)==z['actual_cost'];counts['literal_matching_physical_controls']+=1
    G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
    assert all(colour[v]!=colour[u] for v in range(5*b) for u in G[v])
    assert max(map(len,G),default=0)<=3
    D=set(range(b))|{b+v for v in T}|{3*b+v for v in z['owners']}
    assert len(D)==z['beta_I_lower']==3*b-z['actual_cost'] and all(len(G[v]&D)<=1 for v in D)
    if connectivity:
        assert min(map(len,G))==2 and max(map(len,G))==3
        for removed in range(5*b):
            V=set(range(5*b))-{removed};seen={min(V)};todo=list(seen)
            while todo:
                for u in (G[todo.pop()]&V)-seen:seen.add(u);todo.append(u)
            assert seen==V;counts['physical_vertex_deletion_connectivity_checks']+=1
        counts['two_connected_family_models']+=1
    digest.update(json.dumps([x,z],sort_keys=True).encode());counts['physical_primal_dual_certificates']+=1


def alpha(V,E):
    return max(len(S) for S in subsets(V) if not any(a in S and b in S for a,b in E))


for r in list(range(3,33))+[48,64,96,128,256]:
    x=cyclic_dependency_family(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    ops=x['operations'];U=set(x['initial_U']);E=x['P']+x['Q']
    out=dependency_batch(*args,U,ops,x['cover']);z=out['certificate']
    assert out['selected_candidates']==list(range(r)) and not out['permanent_blockers']
    assert out['dependencies']==[[i,(i+1)%r] for i in range(r)]
    assert z['initial_cost']==r and z['actual_cost']==0 and z['beta_I_lower']==6*r
    assert set(z['U'])==set(range(0,4*r,2))
    physical(x,z,r<=32)
    auto=coordinated_exchange(*args,U,ops)
    assert auto['actual_cost']==0;physical(x,auto)
    if r<=10:
        for S in subsets(range(r)):
            X={ops[i][1] for i in S};Y={ops[i][2] for i in S}
            assert permitted(4*r,x['B'],(U-X)|Y)
            assert isolation(U,X,Y,E)==(len(S) in (0,r))
            counts['literal_cyclic_batch_subsets']+=1
    if r<=32:
        for missing in range(r):
            cropped=[op for i,op in enumerate(ops) if i!=missing]
            broken=dependency_batch(*args,U,cropped,x['cover'])
            assert not broken['selected_candidates'] and len(broken['excluded_candidates'])==r-1
            counts['cyclic_permanent_blocker_propagations']+=1
    if r<=64:
        d=conflict_data(*args,U=U);assert len(d['good'])==r and d['initial_cost']==r
        natural={frozenset(C):i for i,C in enumerate(x['natural_owner_sets'])}
        ids={i:natural[frozenset(c['vertices'])] for i,c in enumerate(d['candidates'])}
        actual={tuple(sorted((ids[i],ids[j]))) for i,j in d['conflicts']}
        expected={(i,j) for i in range(r) for j in range(i+1,r) if min(j-i,r-j+i)<=2}
        assert actual==expected
        if r<=12:assert alpha(range(r),actual)==r//3;counts['literal_cycle_square_independence_optima']+=1
        assert r-r//3==(2*r+2)//3;counts['cycle_square_conflict_models']+=1
    if r in (3,6):examples.append(dict(name='cyclic dependency r='+str(r),model=x,batch=out,exact_beta_I=6*r))
    counts['cyclic_dependency_family_scales']+=1


for r in list(range(4,65,2))+[96,128]:
    x=shared_odd_path_family(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    z=coordinated_exchange(*args,x['initial_U'],x['operations'],x['cover'])
    assert z['initial_cost']==r-1 and z['actual_cost']==1 and z['saved_matching_edges']==r-2
    physical(x,z)
    d=conflict_data(*args,U=x['initial_U']);assert not d['good'] and d['initial_cost']==r-1
    for t in range(len(x['operations'])+1):
        partial=coordinated_exchange(*args,x['initial_U'],x['operations'][:t],x['cover'])
        assert partial['actual_cost']==r-1-t
        counts['shared_odd_path_prefix_exact_costs']+=1
    if r==6:examples.append(dict(name='shared odd path r=6',model=x,certificate=z))
    counts['shared_odd_path_family_scales']+=1


def random_model(n):
    L=list(range(0,n,2));R=list(range(1,n,2));rng.shuffle(L);rng.shuffle(R)
    P=list(zip(L[::2],L[1::2]))+list(zip(R[::2],R[1::2]));rng.shuffle(R)
    k=rng.randrange(n//2+1);Q=list(zip(L[:k],R[:k]));order=[v for pair in zip(L,R) for v in pair]
    B=[];off=0
    while off<n:
        size=min(n-off,rng.choice([4,4,6,8]));K=order[off:off+size];off+=size
        B+=list(zip(K,K[1:]+K[:1])) if size>=4 and size%2==0 else list(zip(K,K[1:]))
    return dict(b=n//2,P=P,Q=Q,B=B,colour=[v%2 for v in range(n)])


for n in (8,12,16,24,32,64):
    for trial in range(40):
        x=random_model(n);args=[x[k] for k in ('b','P','Q','B','colour')];d=prepare(*args);U=set()
        # Choose a local maximum owner dissociation set by literal enumeration
        # for these <=8-vertex owner components, independently of production.
        for K,_ in d['owner_components']:
            omit=min((S for S in subsets(K) if permitted(n,x['B'],S|(set(range(n))-set(K)))),key=lambda S:(len(S),sorted(S)))
            U|=omit
        if trial%3==0:U|={v for v in range(n) if rng.randrange(5)==0}
        T,M=score(n,x['P'],x['Q'],U);C=U-T;ops=[];Y=set();E=x['P']+x['Q']
        for i,(K,_) in enumerate(d['owner_components']):
            choices=[(a,c) for a in sorted(set(K)&C) for c in sorted(set(K)-U) if permitted(n,x['B'],(U-{a})|{c}) and not any((v==c and w in Y) or (w==c and v in Y) for v,w in E)]
            if choices:
                a,c=rng.choice(choices);ops.append([i,a,c]);Y.add(c)
        # Exhaustive subset comparison is for the first at most8 candidates.
        ops=ops[:8]
        out=dependency_batch(*args,U,ops,C);z=out['certificate'];physical(x,z)
        selected=set(out['selected_candidates']);all_feasible=[]
        for S in subsets(range(len(ops))):
            X={ops[i][1] for i in S};Y={ops[i][2] for i in S}
            if not isolation(U,X,Y,E):continue
            assert S<=selected
            rec=coordinated_exchange(*args,U,[ops[i] for i in sorted(S)],C)
            assert rec['applicable'] and rec['actual_cost']==len(M)-len(S)
            assert permitted(n,x['B'],(U-X)|Y)
            all_feasible.append(S);counts['literal_dependency_feasible_subsets']+=1
        assert selected in all_feasible and max(map(len,all_feasible))==len(selected)
        assert set().union(*all_feasible)==selected
        counts['literal_largest_dependency_batch_optima']+=1
        counts['nonempty_random_batches']+=bool(selected)


# Hypotheses really matter. These distinguish failure of a rule from its target.
assert literal_matching({0,1,2},[(0,1),(1,2)])==literal_matching({1,2},[(0,1),(1,2)])==1
assert forced_minimum_cover(4,[(0,1),(1,2),(2,3)],range(4),{1,2})['applicable']
assert not forced_minimum_cover(4,[(0,1),(1,2),(2,3)],range(4),{0,1})['applicable']
x=dict(b=2,P=[(0,1),(2,3)],Q=[(1,2)],B=[(0,2),(2,1),(1,3),(3,0)],colour=[0,0,1,1])
z=coordinated_exchange(*(x[k] for k in ('b','P','Q','B','colour')),{0,1},[[0,0,2]],{0})
assert not z['applicable'] and 'isolated' in z['reason']
B=[(i,(i+1)%8) for i in range(8)];U={0,2,5}
assert permitted(8,B,U) and permitted(8,B,{7,2,5}) and permitted(8,B,{0,3,5}) and not permitted(8,B,{7,3,5})
try:forced_minimum_cover(3,[(0,1),(1,2),(2,0)],range(3),{0})
except ValueError:pass
else:raise AssertionError('Nonbipartite input must be rejected')
counts['necessity_controls']=6

report=dict(scope='Exact general proof checked by small fixed-bipartition enumeration; physical certificates, cyclic dependencies, shared odd components and fixed-candidate closure optimum. No universal optimum from enumeration, no Lean.',
            counts=dict(sorted(counts.items())),certificate_digest=digest.hexdigest(),examples=examples)
parser=argparse.ArgumentParser();parser.add_argument('--output',default=str(ROOT/'output/cover-saturated-exchange-check.json'));opt=parser.parse_args()
Path(opt.output).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
print(json.dumps(dict(counts=report['counts'],certificate_digest=report['certificate_digest']),sort_keys=True))
