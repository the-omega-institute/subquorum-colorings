"""Independent original-graph checks for short-component completion theorem."""
from pathlib import Path
from itertools import combinations,product
from collections import Counter
from functools import lru_cache
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from short_auxiliary_completion import complete_short_auxiliary,certificate
from owner_matching_certificate import components,prepare,materialize
from mixed_owner_bridges import cardinality_bridge
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();rng=random.Random(151126)


def literal_matching(n,E,U):
    adj=[0]*n
    for a,b in E:adj[a]|=1<<b;adj[b]|=1<<a
    @lru_cache(None)
    def f(mask):
        if not mask:return 0
        bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit;best=f(rest);W=adj[v]&rest
        while W:
            w=W&-W;W^=w;best=max(best,1+f(rest^w))
        return best
    return f(sum(1<<v for v in U))


def inspect(n,A,B,exact=False):
    rec=complete_short_auxiliary(n,A,B);S=set(rec['owners']);U=set(rec['U']);T=set(rec['witnesses']);M=rec['matching']
    R=sum(len(K)%3 for K,c in components(n,B) if not c)
    assert R==rec['path_remainder'] and rec['cost_bound']==(n-R)//6
    assert S==set(range(n))-U and T<=U and all(not set(e)<=T for e in A)
    assert all(sum(v in e and set(e)<=S for e in B)<=1 for v in S)
    assert len(T)==len(U)-len(M) and len(M)==rec['cost']<=rec['cost_bound']
    EE={tuple(sorted(e)) for e in A};cover=U-T
    assert len(cover)==len(M) and len({v for e in M for v in e})==2*len(M)
    assert all(tuple(sorted(e)) in EE and set(e)<=U for e in M)
    assert all(a in cover or b in cover for a,b in A if a in U and b in U)
    AA=A+[tuple(e) for e in rec['added_auxiliary_edges']]
    assert all(c and len(K)==4 for K,c in components(rec['completed_order'],AA))
    square=rec['square_certificate'];SS=set(square['owners']);nn=rec['completed_order']
    RR=R+2*bool(rec['ghost_vertices'])
    assert 6*len(SS)>=2*nn+RR
    if rec['ghost_vertices']:counts['odd_P2_ghost_models']+=1
    if R:counts['positive_owner_path_remainder_models']+=1
    if n<=12:
        assert literal_matching(n,A,U)==len(M);counts['independent_matching_controls']+=1
    if exact:
        best=n
        for mask in range(1<<n):
            owners={v for v in range(n) if mask>>v&1}
            if any(sum(v in e and set(e)<=owners for e in B)>1 for v in owners):continue
            cost=literal_matching(n,A,set(range(n))-owners);best=min(best,cost);counts['literal_permitted_omission_models']+=1
        assert best<=rec['cost']<=rec['cost_bound'];counts['exact_small_optimum_controls']+=1
    counts['abstract_certificates']+=1
    digest.update(json.dumps([n,A,B,rec],sort_keys=True).encode())
    return rec


def physical(x,rec,connect=False):
    b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    col=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-c for c in x['colour']]
    assert all(col[v]!=col[w] for v in range(5*b) for w in G[v])
    assert max(map(len,G),default=0)<=3
    D=set(range(b))|{b+v for v in rec['witnesses']}|{3*b+v for v in rec['owners']}
    assert len(D)==rec['beta_I_lower']==3*b-rec['cost']
    assert len(D)>=(16*b+rec['path_remainder']+5)//6
    assert all(len(G[v]&D)<=1 for v in D)
    counts['physical_certificates']+=1
    for a,c in rec['added_auxiliary_edges']:
        if a<n and c<n and x['colour'][a]==x['colour'][c]:counts['nonphysical_completion_edge_controls']+=1
    if connect:
        seen={0};stack=[0]
        while stack:
            for w in G[stack.pop()]-seen:seen.add(w);stack.append(w)
        assert len(seen)==5*b and min(map(len,G))==2 and max(map(len,G))==3
        counts['connected_min2_max3_fixture_controls']+=1


# Every valid abstract pair A,B through4 indices, no prescribed physical colour.
for n in (0,2,4):
    poss=list(combinations(range(n),2));short=[];owners=[]
    for mask in range(1<<len(poss)):
        E=[e for i,e in enumerate(poss) if mask>>i&1]
        if max(Counter(v for e in E for v in e).values(),default=0)>2:continue
        cs=components(n,E)
        if all(not c or len(K)%2==0 for K,c in cs):owners.append(E)
        if all((c and len(K)==4) or (not c and len(K) in (2,4)) for K,c in cs):short.append(E)
    for A in short:
        for B in owners:inspect(n,A,B,exact=True)
    counts['complete_small_graph_pairs']+=len(short)*len(owners)


# Arbitrary crossing owner paths/even cycles, all short auxiliary mixtures.
for trial in range(540):
    n=rng.choice([2,4,6,8,10,12,14,16,20,24,32,48,64,96,128])
    A=[];P=[];Q=[];col=[];off=0
    while off<n:
        k=2 if n-off==2 or rng.randrange(3)==0 else 4
        if k==2:
            P.append((off,off+1));col.extend([rng.randrange(2)]*2)
        else:
            P.extend([(off,off+1),(off+2,off+3)]);Q.append((off+1,off+2));c=rng.randrange(2);col.extend([c,c,1-c,1-c])
            if rng.randrange(2):Q.append((off+3,off))
        off+=k
    A=P+Q
    # Abstract B independently permuted, including nonphysical colour cases.
    order=list(range(n));rng.shuffle(order);B=[];off=0
    while off<n:
        k=rng.randrange(1,min(n-off,12)+1);K=order[off:off+k];off+=k;B.extend(zip(K,K[1:]))
        if k>=4 and k%2==0 and rng.randrange(2):B.append((K[-1],K[0]))
    inspect(n,A,B,exact=n<=8)
    # A separate physical B: alternating-colour paths, with some closed cycles.
    remaining=set(range(n));physicalB=[]
    while remaining:
        v=min(remaining);remaining.remove(v);K=[v]
        for _ in range(rng.randrange(1,14)):
            choices=sorted(w for w in remaining if col[w]!=col[K[-1]])
            if not choices:break
            w=rng.choice(choices);remaining.remove(w);K.append(w)
        physicalB.extend(zip(K,K[1:]))
        if len(K)>=4 and len(K)%2==0 and rng.randrange(2):physicalB.append((K[-1],K[0]))
    x=dict(b=n//2,P=P,Q=Q,B=physicalB,colour=col);rec=certificate(*(x[k] for k in ('b','P','Q','B','colour')));assert rec['applicable'];physical(x,rec)
    counts['seeded_crossing_abstract_models']+=1

# Actual physical same-colour P2 joins and all odd ghost residues.
for pairs in (1,2,3,5,7,9,15):
    n=2*pairs;x=dict(b=pairs,P=[(v,v+1) for v in range(0,n,2)],Q=[],B=[],colour=[0]*n)
    rec=certificate(*(x[k] for k in ('b','P','Q','B','colour')));physical(x,rec);assert rec['cost']==0 and rec['beta_I_lower']==3*pairs
    counts['monochromatic_padding_controls']+=1

x=json.loads((ROOT/'develop/fixtures/short-auxiliary-completion.json').read_text());args=[x[k] for k in ('b','P','Q','B','colour')]
rec=certificate(*args);physical(x,rec,connect=True);assert rec['cost']==9 and rec['beta_I_lower']==111
data=prepare(*args);phasecounts=[len(materialize(data,s)['K4']) for s in product((0,1),repeat=len(data['choices']))]
assert len(phasecounts)==512 and min(phasecounts)==2 and not cardinality_bridge(*args)['applicable']
assert sorted(len(K) for K,c in data['owner_components'])==[8]*8+[16]
assert Counter((len(K),c) for K,c in components(80,x['P']+x['Q']))==Counter({(4,True):18,(4,False):2})
counts['fixture_owner_matching_phase_controls']+=len(phasecounts)

# Iterator-safe entry points and precise exclusions (not target counterexamples).
A=[(0,1),(1,2),(2,3),(4,5)];B=[(v,v+1) for v in range(5)]
assert complete_short_auxiliary(6,iter(A),iter(B))==complete_short_auxiliary(6,A,B);counts['one_shot_controls']+=1
for n,A,B in [(6,[(v,v+1) for v in range(5)],[]),(8,[(v,(v+1)%8) for v in range(8)],[]),(4,[(0,1),(2,3)],[(0,1),(1,2),(2,0)]),(3,[],[])]:
    try:complete_short_auxiliary(n,A,B)
    except ValueError:counts['excluded_input_controls']+=1
    else:raise AssertionError('Excluded graph accepted')
report=dict(scope='General short auxiliaryP2/P4/C4 target with arbitrary owner paths/even cycles; sharp inherited8b/3 coefficient and path remainder refinement. Colour-free completions with ghostpair use original physical certificates only; longer auxiliary paths/cycles and universalgraph/grid goals remain open.',counts=dict(sorted(counts.items())),digest=digest.hexdigest(),connected_mixed_fixture=dict(input=x,certificate=rec,owner_phase_count=len(phasecounts),minimum_K4_count=min(phasecounts)))
p=argparse.ArgumentParser();p.add_argument('--output',default=str(ROOT/'output/short-auxiliary-completion-check.json'));dest=Path(p.parse_args().output);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report['counts'],sort_keys=True))
