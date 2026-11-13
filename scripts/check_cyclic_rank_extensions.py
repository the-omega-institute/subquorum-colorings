"""Literal controls of mixed-cycle rank extensions and exact parity obstruction."""
from pathlib import Path
from itertools import combinations,permutations
from collections import Counter
from functools import lru_cache
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from cyclic_rank_extensions import certificate,coarse_parity_obstruction
from owner_matching_certificate import prepare,components
from mixed_owner_bridges import _exchange
from all_helper_optimization import solve
if not __debug__:raise RuntimeError('Assertions required')
rng=random.Random(171126);counts=Counter();methods=Counter();digest=hashlib.sha256();examples={}


def connected(n,E):
    adj=[set() for _ in range(n)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    todo=[0] if n else [];seen=set(todo)
    for a in todo:
        for b in adj[a]-seen:seen.add(b);todo.append(b)
    return len(seen)==n


def physical(x,S,T):
    b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
    def add(a,c):G[a].add(c);G[c].add(a)
    for j,(a,c) in enumerate(x['P']):add(j,b+a);add(j,b+c)
    for v in range(n):add(b+v,3*b+v)
    for a,c in x['Q']:add(b+a,b+c)
    for a,c in x['B']:add(3*b+a,3*b+c)
    col=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-c for c in x['colour']]
    assert all(col[a]!=col[c] for a in range(5*b) for c in G[a])
    D=set(range(b))|{b+v for v in T}|{3*b+v for v in S}
    assert all(len(G[v]&D)<=1 for v in D)
    assert all(len(G[v])==2 for v in range(b)) and all(len(G[v])==3 for v in range(b,5*b))
    counts['literal_physical_certificates']+=1
    return len(D)


def brute_matching(n,E,U):
    adj=[0]*n
    for a,b in E:adj[a]|=1<<b;adj[b]|=1<<a
    @lru_cache(None)
    def f(mask):
        if not mask:return 0
        bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit;best=f(rest);W=adj[v]&rest
        while W:
            z=W&-W;W^=z;best=max(best,1+f(rest^z))
        return best
    return f(sum(1<<v for v in U))


def rank(k,E):
    adj=[set() for _ in range(k)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    seen=set();r=0
    for v in range(k):
        if v in seen:continue
        todo=[v];seen.add(v)
        for a in todo:
            for b in adj[a]-seen:seen.add(b);todo.append(b);r+=1
    return r


def inspect(x,exact=False):
    rec=certificate(**x);counts['physical_models']+=1
    if not rec['applicable']:counts['class_rejections']+=1;return rec
    n=2*x['b'];U=set(rec['U']);T=set(rec['witnesses']);M=rec['matching'];S=set(range(n))-U
    assert physical(x,S,T)==rec['beta_I_lower']==3*x['b']-len(M)>=(8*x['b']+2)//3
    A={tuple(sorted(e)) for e in x['P']+x['Q']};cover=U-T
    assert len(cover)==len(M)==rec['cost'] and len({v for e in M for v in e})==2*len(M)
    assert all(tuple(sorted(e)) in A and set(e)<=U for e in M)
    assert all(a in cover or b in cover for a,b in A if a in U and b in U)
    # Exact induced deficiency from independent literal traversal, not just
    # whole-auxiliary intersection parity.
    deg={v:set() for v in U}
    for a,b in A:
        if a in U and b in U:deg[a].add(b);deg[b].add(a)
    unseen=set(U);odd=0
    while unseen:
        K={min(unseen)};todo=list(K)
        for a in todo:
            for z in deg[a]-K:K.add(z);todo.append(z)
        unseen-=K;odd+=len(K)%2
    assert odd==len(U)-2*len(M);counts['independent_induced_deficiencies']+=1
    if n<=16:assert brute_matching(n,list(A),U)==len(M);counts['literal_matching_controls']+=1
    if exact:assert solve(x['b'],x['P'],x['Q'],x['B'])['beta_I']>=rec['beta_I_lower'];counts['exact_small_optima']+=1
    for row in rec['components']:
        rr=row['certificate'];method=rr['method'];methods[method]+=1
        if method not in examples:examples[method]=dict(model=x,certificate=rec)
        if 'forest' not in rr:continue
        K=row['vertices'];idx={v:j for j,v in enumerate(K)}
        AA=[(idx[a],idx[b]) for a,b in A if a in idx];BB=[(idx[a],idx[b]) for a,b in x['B'] if a in idx]
        aux=components(len(K),AA);owners=components(len(K),BB);of={v:i for i,(Z,_) in enumerate(aux) for v in Z}
        families=[i for i,(Z,_) in enumerate(owners) if len(Z)%6 and i!=rr['reserved_owner']]
        assert len(set(e['cycle'] for e in rr['forest']['ground']))<=len(families)
        if len(families)<=10:
            minimum=len(families)
            for mask in range(1<<len(families)):
                J={f for j,f in enumerate(families) if mask>>j&1};E=[];d=0
                for i in J:
                    Z=owners[i][0];d+=2 if len(Z)%6==4 else 1
                    E.extend((of[a],of[b]) for a,b in zip(Z,Z[1:]+Z[:1]) if of[a]!=of[b])
                r=rank(len(aux),E);eps=0 if method=='square incidence' or rr['reserved_owner'] is not None else 1
                assert 3*r>=d-eps
                minimum=min(minimum,len(families)-len(J)+r);counts['complete_owner_subset_rank_controls']+=1
            assert minimum==rr['forest']['size'];counts['independent_Rado_minmax_controls']+=1
    digest.update(json.dumps([x,rec],sort_keys=True).encode());counts['successful_models']+=1
    return rec


# Prescribed-edge minimum exchanges, full cyclic permission and cardinality.
for m in (4,8,10,14,16,20,22,26,28,32):
    Z=list(range(m))
    for j in range(m):
        U,W=_exchange(Z,j);assert U^W=={j,(j+1)%m} and len(U)==len(W)==(m+2)//3
        for X in (U,W):assert all({i,(i+1)%m,(i+2)%m}&X for i in range(m))
        counts['prescribed_owner_edge_exchanges']+=1
# Reserved-four local lemma: ALL choices of marked vertices and fixed omissions
# in C8, not merely physical examples visited by the constructor.
E8=[(i,(i+1)%8) for i in range(8)]
for marked in combinations(range(8),4):
    rest=sorted(set(range(8))-set(marked))
    for mask in range(16):
        fixed={v for j,v in enumerate(rest) if mask>>j&1};ds=[]
        for pair in combinations(marked,2):
            UU=fixed|set(pair);ds.append(len(UU)-2*brute_matching(8,E8,UU))
        assert max(ds)>=(1 if len(fixed)%2 else 2)
        counts['complete_reserved_C8_fixed_outside_controls']+=1


def template(lengths):
    n=sum(lengths);P=[];Q=[];off=0
    for m in lengths:
        Z=list(range(off,off+m));off+=m;P.extend(zip(Z[::2],Z[1::2]));Q.extend((Z[j],Z[(j+1)%m]) for j in range(1,m,2))
    return dict(b=n//2,P=P,Q=Q,colour=[(v//2)%2 for v in range(n)])


# Complete all physical 2regular owner edge sets for canonical A at order8.
for lengths in ([4,4],[8]):
    x=template(lengths);L=[v for v,c in enumerate(x['colour']) if not c];R=[v for v,c in enumerate(x['colour']) if c];seen=set()
    for p in permutations(R):
        for q in permutations(R):
            if any(a==b for a,b in zip(p,q)):continue
            B=tuple(sorted(tuple(sorted(e)) for e in list(zip(L,p))+list(zip(L,q))))
            if B in seen:continue
            seen.add(B);inspect(dict(x,B=list(B)),exact=True);counts['complete_order8_physical_graphs']+=1
# Biased oneC8 plus squares, including reserved owner squares and outside C8s.
for trial in range(520):
    lengths=[8]+[4]*rng.randrange(1,15);x=template(lengths);n=2*x['b']
    L=[v for v,c in enumerate(x['colour']) if not c];R=[v for v,c in enumerate(x['colour']) if c];rng.shuffle(L);rng.shuffle(R)
    order=[v for pair in zip(L,R) for v in pair];B=[];off=0
    if trial%3==0:
        # Put a physical ownerC4 wholly inside the unique auxiliaryC8.
        C=[0,2,1,3];B.extend(zip(C,C[1:]+C[:1]));order=[v for pair in zip([v for v in L if v not in C],[v for v in R if v not in C]) for v in pair]
    while order:
        options=list(range(4,len(order)+1,2));options=[m for m in options if len(order)-m!=2]
        m=rng.choice(options);C=order[:m];order=order[m:];B.extend(zip(C,C[1:]+C[:1]))
    rec=inspect(dict(x,B=B),exact=n<=12);assert rec['applicable'];counts['seeded_one_C8_models']+=1
# Arbitrarily long auxiliary cycles, including multiple long components.
for trial in range(440):
    lengths=[4]*rng.randrange(2,15)+[rng.choice([8,12,16,20]) for _ in range(rng.randrange(1,4))];x=template(lengths);n=2*x['b']
    L=[v for v,c in enumerate(x['colour']) if not c];R=[v for v,c in enumerate(x['colour']) if c];rng.shuffle(L);rng.shuffle(R)
    order=[v for pair in zip(L,R) for v in pair];B=[]
    while order:
        opts=[m for m in range(4,len(order)+1,2) if len(order)-m!=2];m=rng.choice(opts);C=order[:m];order=order[m:];B.extend(zip(C,C[1:]+C[:1]))
    inspect(dict(x,B=B));counts['seeded_general_long_cycle_models']+=1
# Explicit family where whole-component parity fails at unbounded scale.
large=template([1200]);large['B']=[(off+a,off+b) for off in range(0,1200,4) for a,b in ((0,2),(2,1),(1,3),(3,0))]
rec=inspect(large);assert rec['applicable'];counts['iterative_exterior_above_default_recursion_limit']+=1
family=[]
for t in (1,2,3,4,8,16,32,64):
    x,rec=coarse_parity_obstruction(t);d=prepare(**x);U=set(rec['U']);n=2*x['b'];A=x['P']+x['Q'];S=set(range(n))-U
    assert all(not set(e)<=U for e in A);assert all(sum(v in e and set(e)<=S for e in x['B'])<=1 for v in S)
    assert physical(x,S,U)==rec['exact_beta_I']==3*x['b'];assert connected(n,A+x['B'])
    aa=components(n,A);bb=components(n,x['B']);assert sorted(map(lambda z:len(z[0]),aa))==[4,4,n-8]
    m=sum((len(Z)+2)//3 for Z,_ in bb);assert m==len(U)==rec['minimum_omissions']
    intersection=sorted(len(U&set(Z)) for Z,_ in aa);assert intersection==sorted(rec['omission_intersections'])
    q=sum(len(U&set(Z))//2 for Z,_ in aa);assert q==rec['exact_min_coarse_cost']==(m-3+1)//2
    assert q-n//6==t==rec['coarse_shortfall'];assert n//6==rec['target_cost']
    of={v:i for i,(Z,_) in enumerate(aa) for v in Z};cross=[]
    for Z,_ in bb:
        es=[(of[a],of[b]) for a,b in zip(Z,Z[1:]+Z[:1]) if of[a]!=of[b]]
        if es:cross.append(es)
    assert len(cross)==1 and rank(3,cross[0])==2
    # Precisely one available family yields exactly one rainbow edge.
    counts['literal_exact_obstruction_families']+=1;family.append(dict(t=t,n=n,actual_order=5*x['b'],**{k:v for k,v in rec.items() if k!='U'}))
    digest.update(json.dumps([x,rec],sort_keys=True).encode())
# Domain rejection does not mean target failure.
x=template([8]);assert not certificate(**dict(x,B=[]))['applicable'];counts['partial_domain_rejections']+=1
for invalid in (0,-1,True,1.5):
    try:coarse_parity_obstruction(invalid)
    except ValueError:counts['invalid_parameter_rejections']+=1
    else:raise AssertionError('Invalid t accepted')
assert all(methods[k] for k in ('one C8 reserved owner square','one C8 rank deficit','square incidence'))
report=dict(counts=dict(sorted(counts.items())),methods=dict(sorted(methods.items())),examples=examples,family=family,deterministic_sha256=digest.hexdigest(),scope='Actual cyclic sufficient classes: oneC8 or squareincidence, plus exact optimized wholecomponentparity obstruction. No universal mixedcyclic or unrestricted graphparameter conclusion.')
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/cyclic-rank-extensions-check.json');a=p.parse_args();a.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps({k:v for k,v in report.items() if k!='examples'}))
