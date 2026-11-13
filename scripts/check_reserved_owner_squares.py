"""Independent literal controls for the unique physical auxiliary C12 theorem."""
from pathlib import Path
from itertools import combinations
from collections import Counter
from functools import lru_cache
import argparse, hashlib, json, random, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from reserved_owner_squares import certificate, four_boundary
from owner_matching_certificate import prepare
from all_helper_optimization import solve
if not __debug__:raise RuntimeError('Assertions required')
rng=random.Random(134121);counts=Counter();methods=Counter();digest=hashlib.sha256()


def parts(V,E):
    adj={v:set() for v in V}
    for a,b in E:adj[a].add(b);adj[b].add(a)
    unseen=set(V);answer=[]
    while unseen:
        todo=[min(unseen)];K=set(todo)
        for a in todo:
            for b in adj[a]-K:K.add(b);todo.append(b)
        unseen-=K;answer.append(K)
    return answer


def matching_function(n,E):
    adj=[0]*n
    for a,b in E:adj[a]|=1<<b;adj[b]|=1<<a
    @lru_cache(None)
    def f(mask):
        if not mask:return 0
        bit=mask&-mask;v=bit.bit_length()-1;rest=mask^bit;best=f(rest);W=adj[v]&rest
        while W:
            z=W&-W;W^=z;best=max(best,1+f(rest^z))
        return best
    return f


def literal_physical(x,S,T):
    b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for j,(a,c) in enumerate(x['P']):edge(j,b+a);edge(j,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    col=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-c for c in x['colour']]
    assert all(col[a]!=col[c] for a in range(5*b) for c in G[a])
    D=set(range(b))|{b+v for v in T}|{3*b+v for v in S}
    assert all(len(G[v]&D)<=1 for v in D)
    assert all(len(G[v])==2 for v in range(b)) and all(len(G[v])==3 for v in range(b,5*b))
    counts['literal_physical_certificates']+=1
    return len(D)


def inspect(x,exact=False):
    rec=certificate(**x);assert rec['applicable'];n=2*x['b'];U=set(rec['U']);T=set(rec['witnesses']);M=rec['matching'];A=x['P']+x['Q'];cover=U-T
    assert literal_physical(x,set(range(n))-U,T)==rec['beta_I_lower']==3*x['b']-len(M)>=(8*x['b']+2)//3
    assert len({v for e in M for v in e})==2*len(M) and len(cover)==len(M)==rec['cost']
    es={tuple(sorted(e)) for e in A}
    assert all(tuple(sorted(e)) in es and set(e)<=U for e in M)
    assert all(a in cover or b in cover for a,b in A if a in U and b in U)
    odd=sum(len(K)%2 for K in parts(U,[e for e in A if set(e)<=U]))
    assert odd==len(U)-2*len(M);counts['independent_induced_deficiencies']+=1
    if n<=16:assert matching_function(n,A)(sum(1<<v for v in U))==len(M);counts['literal_matching_controls']+=1
    if exact:assert solve(x['b'],x['P'],x['Q'],x['B'])['beta_I']>=rec['beta_I_lower'];counts['exact_small_all_helper_optima']+=1
    for row in rec['components']:
        rr=row['certificate'];methods[rr['method']]+=1
        if 'forest' not in rr:continue
        K=row['vertices'];idx={v:j for j,v in enumerate(K)};B=[(idx[a],idx[b]) for a,b in x['B'] if a in idx]
        owners=parts(range(len(K)),B);of={v:i for i,Z in enumerate(rr['projected_auxiliary']) for v in Z}
        reserved=rr['reserved_owner_indices'];families=[i for i,C in enumerate(owners) if len(C)%6 and i not in reserved]
        if len(families)<=10:
            minimum=len(families)
            for mask in range(1<<len(families)):
                J={f for j,f in enumerate(families) if mask>>j&1};vertices=set().union(*(owners[i] for i in J)) if J else set()
                E=[(of[a],of[b]) for a,b in B if a in vertices and of[a]!=of[b]]
                rank=len(rr['projected_auxiliary'])-len(parts(range(len(rr['projected_auxiliary'])),E))
                d=sum(2 if len(owners[i])%6==4 else 1 for i in J)
                eps=rr['rank_epsilon_thirds']
                if not (eps==-1 and not J):assert 3*rank>=d-eps
                minimum=min(minimum,len(families)-len(J)+rank);counts['independent_all_subset_rank_controls']+=1
            assert minimum==rr['forest']['size'];counts['independent_Rado_minmax_controls']+=1
        if 'local' in rr:
            local=rr['local'];R={K[v] for v in local['region']};UR=U&R
            d=len(UR)-2*sum(len(C)//2 for C in parts(UR,[e for e in A if set(e)<=UR]))
            assert d==local['deficiency'];counts['independent_reserved_regional_controls']+=1
    counts['physical_models']+=1;digest.update(json.dumps([x,rec],sort_keys=True).encode());return rec


# All marked-square placements and all fixed memberships outside them on C12.
A12=[(v,(v+1)%12) for v in range(12)];f=matching_function(12,A12)
for marked in combinations(range(12),4):
    outside=sorted(set(range(12))-set(marked));pairs=[sum(1<<v for v in p) for p in combinations(marked,2)]
    for mask in range(1<<len(outside)):
        fixed=sum(1<<v for j,v in enumerate(outside) if mask>>j&1)
        best=max((fixed|p).bit_count()-2*f(fixed|p) for p in pairs)
        assert best>=(1 if mask.bit_count()%2 else 2);counts['complete_C12_marked_square_fixed_outside']+=1
# Entire abstract C8/C10 placements on C12, literal minimum permitted choices.
for m in (8,10):
    for C in combinations(range(12),m):
        opts=[]
        for U in combinations(C,(m+2)//3):
            S=set(C)-set(U)
            if all(not {C[j],C[(j+1)%m],C[(j+2)%m]}<=S for j in range(m)):
                opts.append(sum(1<<v for v in U))
        outside=sorted(set(range(12))-set(C))
        for mask in range(1<<len(outside)):
            fixed=sum(1<<v for j,v in enumerate(outside) if mask>>j&1)
            best=max((fixed|p).bit_count()-2*f(fixed|p) for p in opts)
            assert best>=(1 if (fixed.bit_count()+(m+2)//3)%2 else 2)
            counts['complete_C12_marked_C'+str(m)+'_fixed_outside']+=1


def template(lengths):
    n=sum(lengths);P=[];Q=[];off=0
    for m in lengths:
        K=list(range(off,off+m));off+=m;P.extend(zip(K[::2],K[1::2]));Q.extend((K[j],K[(j+1)%m]) for j in range(1,m,2))
    return dict(b=n//2,P=P,Q=Q,colour=[(v//2)%2 for v in range(n)])


def from_pool(x,pool,lengths):
    sides=[[v for v in sorted(pool) if x['colour'][v]==c] for c in (0,1)]
    assert len(sides[0])==len(sides[1]) and sum(lengths)==len(pool)
    for Z in sides:rng.shuffle(Z)
    B=[];off=0
    for m in lengths:
        K=[v for p in zip(sides[0][off:off+m//2],sides[1][off:off+m//2]) for v in p];off+=m//2;B.extend(zip(K,K[1:]+K[:1]))
    return B


# Four-boundary lemma, all16 prescribed F0, varied physical placements.
for k in (3,4):
    for trial in range(48):
        x=template([12]+[4]*(k-2));R=set(range(2*x['b']));colour=x['colour'];pool=[]
        for c in (0,1):
            Z=[v for v in sorted(R) if colour[v]==c];rng.shuffle(Z);pool+=Z[:2*k]
        B=from_pool(x,pool,[4]*k);F=sorted(R-set(pool));B+=from_pool(x,F,[4]);x['B']=B;data=prepare(**x)
        reserved=[i for i,(K,_) in enumerate(data['owner_components']) if set(K)<=set(pool)]
        fun=matching_function(2*x['b'],x['P']+x['Q'])
        for mask in range(16):
            F0={v for j,v in enumerate(F) if mask>>j&1};U,rec=four_boundary(data,R,reserved,F0)
            delta=len(U)-2*fun(sum(1<<v for v in U));assert delta==rec['deficiency'] and delta>=(3 if len(F0)%2 else 2)
            assert U&set(F)==F0;counts['literal_four_boundary_'+str(k)+'_controls']+=1
            digest.update(json.dumps([x,rec],sort_keys=True).encode())
# Frozen branch examples discovered before this checker, not adapted at runtime.
examples=json.loads((ROOT/'develop/fixtures/c12-reservation-examples.json').read_text())
for name,x in sorted(examples.items()):
    rec=inspect(x);assert any(row['certificate']['method']==name for row in rec['components']);counts['frozen_branch_models']+=1
# Small domain: isolated C12 and C12+C4; literal exponential all-helper optima.
for s in (0,1):
    for trial in range(14):
        x=template([12]+[4]*s);n=2*x['b'];x['B']=from_pool(x,range(n),[n]);inspect(x,exact=True)
x=template([12,4]);C=set(range(8));x['B']=from_pool(x,C,[8])+from_pool(x,set(range(16))-C,[8]);inspect(x,exact=True)
# Biased physical whole graphs, arbitrary owner even cycles.
for typ in ('random','internal4','internal44','internal8','internal10','T3','T4'):
    for trial in range(72):
        s=rng.randrange(2,16);x=template([12]+[4]*s);n=2*x['b'];B=[];used=set()
        if typ.startswith('internal'):
            lengths={'internal4':[4],'internal44':[4,4],'internal8':[8],'internal10':[10]}[typ];pool=[]
            for c in (0,1):
                Z=[v for v in range(12) if x['colour'][v]==c];rng.shuffle(Z);pool+=Z[:sum(lengths)//2]
            B=from_pool(x,pool,lengths);used=set(pool)
        elif typ in ('T3','T4'):
            k=3 if typ=='T3' else 4;R=list(range(4*(k+1)));pool=[]
            for c in (0,1):
                Z=[v for v in R if x['colour'][v]==c];rng.shuffle(Z);pool+=Z[:2*k]
            B=from_pool(x,pool,[4]*k);used=set(pool)
        pool=set(range(n))-used;m=len(pool);lengths=[]
        while m:
            opts=[j for j in range(4,m+1,2) if m-j!=2];j=rng.choice(opts) if typ=='random' else m;lengths.append(j);m-=j
        x['B']=B+from_pool(x,pool,lengths);inspect(x);counts['seeded_'+typ+'_models']+=1
# Component reassembly: exactly one C12 plus many disconnected auxiliary squares.
x=template([12]+[4]*20);x['B']=from_pool(x,range(12),[12])
for off in range(12,2*x['b'],4):x['B']+=from_pool(x,range(off,off+4),[4])
inspect(x);counts['disconnected_reassembly_models']+=1
# All integer capacity possibilities for serious root rank loss, no finite
# vertex-size assumption: x+5y+(9/2)a<=7 supplies these exact bounds.
expected={(1,3,0),(2,4,0),(1,4,0),(2,5,0),(3,6,0),(4,7,0),(1,2,1)};actual=set()
for x in range(8):
    for y in range(2):
        for a in range(2):
            for q in range(1,5):
                if 4*x+8*y+6*a<=4*q+12 and 2*x+y>=3*q+2:
                    assert a==0;actual.add((q,x,y));counts['serious_rank_integer_types']+=1
assert actual==expected
required=['unique C12 ordinary rank','unique C12 contained 4','unique C12 contained 4,4','unique C12 contained 8','unique C12 contained 10','unique C12 T3 four boundary','unique C12 T4 strict rank','at most one auxiliary square']
assert all(methods[name] for name in required)
report=dict(counts=dict(sorted(counts.items())),methods=dict(sorted(methods.items())),deterministic_sha256=digest.hexdigest(),
            scope='Written all-size theorem for A=sC4+C12, perfect Q, physical owner even cycles; literal matching/cover and original5bvertex certificates. Finite controls do not prove the theorem. General mixed cyclic and physical grid problems remain open.')
p=argparse.ArgumentParser();p.add_argument('--output',type=Path,default=ROOT/'output/reserved-owner-squares-check.json');a=p.parse_args();a.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n');print(json.dumps(report))
