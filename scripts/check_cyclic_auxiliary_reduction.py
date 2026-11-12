"""Independent physical completion and certificate-transfer checks."""
from pathlib import Path
from itertools import combinations, product
from collections import Counter
from functools import lru_cache
import argparse, hashlib, json, random, sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from cyclic_auxiliary_reduction import cyclic_completion,transfer_certificate
from auxiliary_square_forest import abstract_certificate
if not __debug__:raise RuntimeError('Assertions required')
counts=Counter();digest=hashlib.sha256();rng=random.Random(131126)


def matching(n,E,U):
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


def blocks(n,E):
    adj=[set() for _ in range(n)]
    for a,b in E:adj[a].add(b);adj[b].add(a)
    unseen=set(range(n));answer=[]
    while unseen:
        root=min(unseen);K={root};stack=[root]
        while stack:
            for v in adj[stack.pop()]-K:K.add(v);stack.append(v)
        answer.append((K,all(len(adj[v])==2 for v in K)));unseen-=K
    return answer


def permitted(n,B,U):
    S=set(range(n))-set(U)
    return all(sum(v in e and set(e)<=S for e in B)<=1 for v in S)


def physical(x,owners,witnesses):
    b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
    def add(a,c):G[a].add(c);G[c].add(a)
    for j,(a,c) in enumerate(x['P']):add(j,b+a);add(j,b+c)
    for v in range(n):add(b+v,3*b+v)
    for a,c in x['Q']:add(b+a,b+c)
    for a,c in x['B']:add(3*b+a,3*b+c)
    colours=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
    assert all(colours[v]!=colours[w] for v in range(5*b) for w in G[v])
    assert max(map(len,G),default=0)<=3
    D=set(range(b))|{b+v for v in witnesses}|{3*b+v for v in owners}
    assert all(len(G[v]&D)<=1 for v in D)
    if x.get('close_owners') and b:
        assert set(map(len,G))=={2,3} and min(map(len,G))==2
    counts['literal_physical_graph_checks']+=1
    return len(D)


def transfer(x,U,close,target=False):
    rec=transfer_certificate(**x,completed_U=U,close_owners=close,require_target=target)
    c=4 if close else 2;n=2*x['b'];hat=rec['completion']
    assert rec['sum_original_costs']<=rec['completed_cost']
    assert rec['cost']==min(y['cost'] for y in rec['all_copies'])<=rec['completed_cost']//c
    for y in rec['all_copies']:
        assert permitted(n,x['B'],y['U'])
        assert physical(x,y['owners'],y['witnesses'])==y['beta_I_lower']==3*x['b']-y['cost']
        T=set(y['witnesses']);V=set(y['U']);EE=x['P']+x['Q'];cover=V-T;M=y['matching']
        assert T<=V and len(cover)==len(M)==y['cost']
        assert len({v for e in M for v in e})==2*len(M)
        assert all(tuple(sorted(e)) in {tuple(sorted(f)) for f in EE} and set(e)<=V for e in M)
        assert all(a in cover or b in cover for a,b in EE if a in V and b in V)
        if n<=12:assert matching(n,EE,V)==y['cost'];counts['independent_original_matching_checks']+=1
    if c*n<=16:
        assert matching(c*n,hat['P']+hat['Q'],U)==rec['completed_cost'];counts['independent_completed_matching_checks']+=1
    if rec['completed_cost']<=rec['completed_bound']:
        assert rec['cost']<=n//6 and rec['meets_target'];counts['target_transfer_checks']+=1
    counts['transfer_certificates']+=1
    digest.update(json.dumps(rec,sort_keys=True).encode())
    return rec


def inspect(x,thorough=False):
    n=2*x['b'];E=x['P']+x['Q']
    for close in (False,True):
        c=4 if close else 2;hat=cyclic_completion(**x,close_owners=close);nn=c*n
        assert hat['b']==c*x['b'] and len(hat['colour'])==nn
        assert sorted(v for e in hat['P'] for v in e)==list(range(nn))
        assert sorted(v for e in hat['Q'] for v in e)==list(range(nn))
        assert all(a!=b and hat['colour'][a]!=hat['colour'][b] for a,b in hat['Q']+hat['B'])
        assert all(hat['colour'][a]==hat['colour'][b] for a,b in hat['P'])
        assert all(cyclic and len(K)%4==0 for K,cyclic in blocks(nn,hat['P']+hat['Q']))
        assert all(not cyclic or len(K)%2==0 for K,cyclic in blocks(nn,hat['B']))
        assert all(sum(v in e for e in hat['B'])==2 for v in range(nn)) if close else True
        for j in range(c):
            for old,key in ((x['P'],'P'),(x['Q'],'Q'),(x['B'],'B')):
                assert {tuple(sorted((a+n*j,b+n*j))) for a,b in old}<=set(hat[key])
        assert all(a//n!=b//n for a,b in hat['added_B']) if n else not hat['added_B']
        physical(hat,[],[])
        counts['completed_templates']+=1
        for K,cyclic in blocks(n,E):counts['original_auxiliary_'+('cycle' if cyclic else 'path')+'_'+str(len(K))]+=1
        if close:
            for K,cyclic in blocks(n,x['B']):
                if not cyclic:counts['owner_path_closures_'+str(len(K))]+=1
        # Literal all permitted completed omissions on the smallest instances;
        # sampled omissions otherwise (the target is not assumed for samples).
        masks=range(1<<nn) if thorough and nn<=8 else [0,(1<<nn)-1]+[rng.getrandbits(nn) for _ in range(4)]
        for mask in masks:
            U={v for v in range(nn) if mask>>v&1}
            if permitted(nn,hat['B'],U):transfer(x,U,close)
        # In the short class, obtain an actual target certificate by the
        # square forest, then use the independent physical-copy transfer.
        if all(cyclic and len(K)==4 for K,cyclic in blocks(nn,hat['P']+hat['Q'])):
            square=abstract_certificate(nn,hat['P']+hat['Q'],hat['B'])
            U=set(range(nn))-set(square['owners']);rec=transfer(x,U,close,True)
            if not close:
                R=sum(len(K)%3 for K,cyclic in blocks(n,x['B']) if not cyclic)
                assert rec['cost']<=(n-R)//6;counts['two_copy_path_surplus_checks']+=1
            counts['square_target_constructions']+=1
    counts['original_models']+=1


# Exhaust every physical P,Q,B,colour choice for canonical P through four
# indices. Relabellings of P do not change these tested properties.
for b in (0,1,2):
    n=2*b;P=[(2*j,2*j+1) for j in range(b)]
    for bits in product(range(2),repeat=b):
        colour=[v for bit in bits for v in (bit,bit)]
        possible=[e for e in combinations(range(n),2) if colour[e[0]]!=colour[e[1]]]
        qs=[];bs=[]
        for mask in range(1<<len(possible)):
            F=[e for j,e in enumerate(possible) if mask>>j&1]
            degrees=Counter(v for e in F for v in e)
            if max(degrees.values(),default=0)<=1:qs.append(F)
            if max(degrees.values(),default=0)<=2:bs.append(F)
        for Q in qs:
            for B in bs:inspect(dict(b=b,P=P,Q=Q,B=B,colour=colour),True);counts['exhaustive_small_physical_models']+=1


for trial in range(240):
    n=rng.choice([2,4,6,8,10,12,16,20,24,32,48,64,96]);P=[];Q=[];col=[];off=0
    while off<n:
        k=rng.choice(list(range(2,min(24,n-off)+1,2)));K=list(range(off,off+k));off+=k
        P.extend(zip(K[::2],K[1::2]));Q.extend((K[j],K[j+1]) for j in range(1,k-1,2))
        first=rng.randrange(2);col.extend(first^((j//2)%2) for j in range(k))
        if k%4==0 and rng.randrange(2):Q.append((K[-1],K[0]))
    B=[];remaining=set(range(n))
    while remaining:
        v=rng.choice(sorted(remaining));K=[v];remaining.remove(v)
        for _ in range(rng.randrange(12)):
            choices=sorted(w for w in remaining if col[w]!=col[K[-1]])
            if not choices:break
            w=rng.choice(choices);K.append(w);remaining.remove(w)
        B.extend(zip(K,K[1:]))
        if len(K)>=4 and len(K)%2==0 and rng.randrange(2):B.append((K[-1],K[0]))
    inspect(dict(b=n//2,P=P,Q=Q,B=B,colour=col));counts['seeded_crossing_models']+=1


# Every path congruence and existing C4/C8/C12/C16, with isolates, even and
# odd owner paths; these controls also cover colour imbalance and zero order.
for k in range(2,34,2):
    P=[(j,j+1) for j in range(0,k,2)];Q=[(j,j+1) for j in range(1,k-1,2)];col=[(j//2)%2 for j in range(k)]
    inspect(dict(b=k//2,P=P,Q=Q,B=[],colour=col));counts['path_congruence_controls']+=1
    if k%4==0:
        inspect(dict(b=k//2,P=P,Q=Q+[(k-1,0)],B=[],colour=col));counts['cycle_congruence_controls']+=1

for n in range(0,1002,2):
    for c in (2,4):assert (c*n//6)//c==n//6;counts['nested_floor_controls']+=1
x=dict(b=1,P=[(0,1)],Q=[],B=[],colour=[0,0])
for kw in (dict(completed_U={4}),dict(completed_U={True}),dict(completed_U={0,1,2,3},require_target=True)):
    try:transfer_certificate(**x,**kw)
    except ValueError:counts['rejected_invalid_transfer_controls']+=1
    else:raise AssertionError('Invalid transfer accepted')
x2=dict(b=2,P=[(0,1),(2,3)],Q=[],B=[(0,2),(1,2)],colour=[0,0,1,1])
try:transfer_certificate(**x2,completed_U=set(),require_target=False)
except ValueError:counts['rejected_invalid_transfer_controls']+=1
else:raise AssertionError('Nonpermitted omission accepted')
report=dict(theorem='Physical two-/four-copy cyclic completion and exact transfer; universal cyclic case conditional',
            counts=dict(sorted(counts.items())),certificate_digest=digest.hexdigest(),
            scope='No proof of the mixed cyclic target, exact large optimum, Lean, or novelty/priority claim')
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/cyclic-auxiliary-reduction-check.json');args=parser.parse_args()
args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(json.dumps(report,sort_keys=True))
