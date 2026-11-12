"""Independent literal controls plus actual physical certificates for bridges."""
from pathlib import Path
from collections import Counter
from itertools import combinations, product
import argparse, hashlib, json, random, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from mixed_owner_bridges import (square_six_bridge, one_exception_bridge,
    one_K4_bridge, mixed_colouring, cardinality_bridge, _exchange)
from all_helper_optimization import solve
from owner_matching_certificate import prepare, materialize
if not __debug__: raise RuntimeError('Assertions must be enabled')
rng=random.Random(131126);counts=Counter();digest=hashlib.sha256();fixtures=[]


def literal_matching(V,E):
    """No production matching code: first-vertex recurrence."""
    adj={v:set() for v in V}
    for a,b in E:
        if a in adj and b in adj:adj[a].add(b);adj[b].add(a)
    memo={}
    def rec(U):
        if not U:return 0
        key=tuple(sorted(U))
        if key in memo:return memo[key]
        a=min(U);out=rec(U-{a})
        for b in adj[a]&U:out=max(out,1+rec(U-{a,b}))
        memo[key]=out;return out
    return rec(set(V))


def physical(x,rec):
    n=len(x['colour']);b=n//2;P,Q,B=(x[k] for k in ('P','Q','B'))
    G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(P):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in Q:edge(b+a,b+c)
    for a,c in B:edge(3*b+a,3*b+c)
    col=[1-x['colour'][P[i][0]] for i in range(b)]+x['colour']+[1-c for c in x['colour']]
    assert all(col[v]!=col[u] for v in range(5*b) for u in G[v])
    assert max(map(len,G),default=0)<=3
    S=set(rec['owners']);T=set(rec['witnesses']);U=set(range(n))-S
    D=set(range(b))|{b+v for v in T}|{3*b+v for v in S}
    assert len(D)==rec['beta_I_lower']>=(8*b+2)//3
    assert not S&T and all(len(G[v]&D)<=1 for v in D)
    if n<=16:
        assert literal_matching(U,P+Q)==len(rec['matching']);counts['literal_matching_certificates']+=1
    counts['physical_certificates']+=1
    digest.update(json.dumps([x,rec],sort_keys=True).encode())


def build(spec,trial):
    """Create B first, then a physical P and a partial cross-colour matching Q."""
    n=sum(k for k,c in spec);assert n%2==0
    # Random path orientations; physical P requires even counts of both colours.
    for attempt in range(100):
        col=[];B=[];off=0
        for k,cyclic in spec:
            flip=rng.randrange(2);C=list(range(off,off+k));off+=k
            col.extend((j+flip)%2 for j in range(k))
            B+=list(zip(C,C[1:]+C[:1])) if cyclic else list(zip(C,C[1:]))
        if sum(col)%2==0:break
    else:return None
    L=[v for v in range(n) if col[v]==0];RR=[v for v in range(n) if col[v]==1]
    rng.shuffle(L);rng.shuffle(RR)
    P=list(zip(L[::2],L[1::2]))+list(zip(RR[::2],RR[1::2]))
    # Some full Q matchings, some genuinely partial ones, including no Q edges.
    length=min(len(L),len(RR));k=length if trial%4==0 else 0 if trial%4==1 else rng.randrange(length+1)
    rng.shuffle(L);rng.shuffle(RR);Q=list(zip(L[:k],RR[:k]))
    return dict(b=n//2,P=P,Q=Q,B=B,colour=col)


def check(x,kinds,exact=False):
    args=[x[k] for k in ('b','P','Q','B','colour')]
    for kind in kinds:
        f={'squares':square_six_bridge,'exception':one_exception_bridge,'K4':one_K4_bridge,'cardinality':cardinality_bridge}[kind]
        rec=f(*args)
        if not rec['applicable']:counts['inapplicable_'+kind]+=1;continue
        physical(x,rec);counts['models_'+kind]+=1
        if kind=='K4':counts['K4_'+rec['method']]+=1
        if kind=='squares':
            UI=set(v for v,c in rec['labels']);O=set(range(2*x['b']))-UI;U=set(rec['U'])
            internal=sum(a in U&UI and c in U&UI for a,c in x['P']+x['Q'])
            cross=sum((a in U&UI and c in U&O) or (c in U&UI and a in U&O) for a,c in x['P']+x['Q'])
            assert rec['twice_budget']==len(U&O)+2*internal+cross
            assert 2*len(rec['matching'])<=rec['twice_budget']
            if UI and O and any((a in UI)!=(c in UI) for a,c in x['P']+x['Q']):counts['cross_interface_models']+=1
        if kind=='exception':
            counts['exception_'+rec['method']]+=1
        if exact:
            optimum=solve(x['b'],x['P'],x['Q'],x['B'])['beta_I']
            assert optimum>=rec['beta_I_lower'];counts['original_exponential_controls']+=1
    return


# Every prescribed exchange on many cycle lengths, literal triple coverage.
for m in range(4,123,2):
    if m%6==0:continue
    C=list(range(m));B=[(v,(v+1)%m) for v in C]
    for j in C:
        X,Y=_exchange(C,j)
        assert X^Y=={j,(j+1)%m} and len(X)==len(Y)==(m+2)//3
        for U in (X,Y):
            assert all(any((v+t)%m in U for t in range(3)) for v in C)
        counts['prescribed_edge_exchange_pairs']+=1

# Exhaust every cross-colour Q matching for fixed physical P on four/eight indices.
def matchings(L,R):
    if not L:yield [];return
    a=L[0]
    yield from matchings(L[1:],R)
    for c in R:
        for rest in matchings(L[1:],[v for v in R if v!=c]):yield [(a,c)]+rest
for n in (4,8):
    col=[0]*(n//2)+[1]*(n//2);P=[(v,v+1) for v in range(0,n,2)]
    order=[v for pair in zip(range(n//2),range(n//2,n)) for v in pair]
    specs=[[(n,False)],[(4,True)]*(n//4)]
    if n==8:specs += [[(8,True)],[(4,True),(4,False)]]
    for spec in specs:
        B=[];off=0
        for k,cyclic in spec:
            C=order[off:off+k];off+=k
            B+=list(zip(C,C[1:]+C[:1])) if cyclic else list(zip(C,C[1:]))
        for Q in matchings(list(range(n//2)),list(range(n//2,n))):
            x=dict(b=n//2,P=P,Q=Q,B=B,colour=col)
            check(x,('squares','exception','K4','cardinality'),exact=n==4)
            counts['exhaustive_physical_models']+=1

# Random relabellings span every cycle congruence, odd paths, mixed A and sizes.
for n in (4,8,10,12,16,20,24,28,32,40,48,64,96,128):
    specs=[[(4,True)]*(n//4)+([(n%4,False)] if n%4 else []),[(n,False)]]
    for c in (4,6,8,10,14,16,20,22):
        if c<=n:
            rem=n-c
            specs.append([(c,True)]+([(rem,False)] if rem else []))
            if rem>=6:specs.append([(c,True),(3,False),(3,False)]+([(rem-6,False)] if rem>6 else []))
    if n>=16:specs.append([(4,True),(6,True),(6,False)]+([(n-16,False)] if n>16 else []))
    if n>=20:specs.append([(4,True),(4,True),(12,True)]+([(n-20,False)] if n>20 else []))
    for spec in specs:
        for trial in range(8):
            x=build(spec,trial)
            if x is not None:check(x,('squares','exception','K4','cardinality'),exact=n<=8)

# A stronger cardinality class: several exceptional cycles can be present.
for spec in ([ (4,True),(4,True),(12,True) ],[(4,True)]*3,[(8,True)]*2+[(4,False)]):
    for trial in range(40):
        x=build(spec,trial)
        if x is not None:
            rec=cardinality_bridge(*(x[k] for k in ('b','P','Q','B','colour')))
            if rec['applicable']:
                physical(x,rec);counts['multiple_exception_cardinality_controls']+=1

# Abstract controls permit odd auxiliary cycles and ignore physical colouring.
for n in range(1,29):
    for trial in range(14):
        order=list(range(n));rng.shuffle(order)
        A=list(zip(order,order[1:]))
        if n>=3 and trial%3==0:A.append((order[-1],order[0]))
        if n>=4 and trial%3==1:
            A=[(order[j+k],order[j+(k+1)%4]) for j in range(0,n-n%4,4) for k in range(4)]
        order=list(range(n));rng.shuffle(order)
        B=list(zip(order,order[1:]))
        if n>=4 and n%2==0 and trial%2:B.append((order[-1],order[0]))
        rec=mixed_colouring(n,A,B);c=dict(rec['colouring'])
        assert all(c[a]!=c[b] for a,b in A)
        assert all(sum(v in e and c[e[0]]==c[e[1]] for e in B)<=1 for v in range(n))
        assert len(rec['largest_class'])>=(n+2)//3
        counts['abstract_models']+=1;counts['abstract_restored_squares']+=len(rec['restored_squares'])
        digest.update(json.dumps([A,B,rec],sort_keys=True).encode())

# Strong local lemma: fix arbitrary outside omissions, not just minimum ones.
# C need not respect physical colours in these abstract bipartite-A controls.
for n in (4,6,8,10):
    graphs=[[(v,v+1) for v in range(n-1)],[(v,(v+1)%n) for v in range(n)]]
    if n>=8:graphs.append([(j+k,j+(k+1)%4) for j in range(0,n-n%4,4) for k in range(4)])
    for A in graphs:
        for m in (4,8,10):
            if m>n:continue
            for Ctuple in combinations(range(n),m):
                C=list(Ctuple);outside=sorted(set(range(n))-set(C));k=(m+2)//3
                for mask in range(1<<len(outside)):
                    U0={v for j,v in enumerate(outside) if mask>>j&1}
                    if (len(U0)+k)%2:continue
                    assert any(2*literal_matching(U0|UC,A)<len(U0)+k
                               for j in range(m) for UC in _exchange(C,j))
                    counts['arbitrary_fixed_outside_balance_controls']+=1

for x in json.loads((ROOT/'develop/fixtures/mixed-owner-bridges.json').read_text()):
    opt=solve(x['b'],x['P'],x['Q'],x['B']);assert opt['beta_I']==x['exact_beta_I']
    counts['exact_fixed_benchmarks']+=1
    check({k:x[k] for k in ('b','P','Q','B','colour')},('squares','exception','K4','cardinality'))
    if x['name']=='normalization':
        n=2*x['b'];A=x['P']+x['Q'];best=0;best_compatible=None
        for mask in range(1<<n):
            S={v for v in range(n) if mask>>v&1}
            if any(set(e)<=S for e in A):continue
            if any(sum(v in e and set(e)<=S for e in x['B'])>1 for v in S):continue
            if len(S)>best:best=len(S);best_compatible=sorted(S)
            counts['literal_compatible_subsets']+=1
        assert best==6 and opt['beta_I']==17<2*x['b']+best
        assert literal_matching(set(range(n))-set(x['threshold_size_compatible_set']),A)==3
    else:
        d=prepare(*(x[k] for k in ('b','P','Q','B','colour')));mat=materialize(d,[0]*len(d['choices']))
        assert len(mat['K4'])==1
        alpha=0
        for mask in range(1<<(2*x['b'])):
            S={v for v in range(2*x['b']) if mask>>v&1}
            if not any(set(e)<=S for e in mat['edges']):alpha=max(alpha,len(S))
        assert alpha==5 and 2*x['b']+alpha==21 and opt['beta_I']==24
        rep=one_K4_bridge(*(x[k] for k in ('b','P','Q','B','colour')))
        assert rep['method']=='one-K4 doubled-owner repair';physical(x,rep)
        counts['genuine_K4_repairs']+=1
    fixtures.append({'name':x['name'],'exact_optimum':opt})

# Empty and outside-hypothesis controls.
for f in (square_six_bridge,one_exception_bridge,one_K4_bridge):assert f(0,[],[],[],[])['beta_I_lower']==0
assert counts['cross_interface_models'] and counts['genuine_K4_repairs']
assert counts['multiple_exception_cardinality_controls'] and counts['abstract_restored_squares']
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/mixed-owner-bridges-check.json');args=parser.parse_args()
report={'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),'fixtures':fixtures,
        'scope':'General proofs are in docs/MIXED_OWNER_BRIDGES.md. Finite controls check constructions; no unrestricted physical, SF, grid or Lean result is claimed. Colouring search has no polynomial runtime claim.'}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='fixtures'}))
