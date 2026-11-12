"""Literal pair/common-activation equivalence, optimum budgets and physical controls."""
from pathlib import Path
from itertools import product,combinations
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from omission_conflict_graph import pair_conflicts,conflict_data,greedy_conflict_certificate,shared_even_path_family
from activated_omission_budget import activated_budget,separated_long_cycle_family
from owner_matching_certificate import prepare
from mixed_owner_bridges import _minimum_omission
if not __debug__:raise RuntimeError('Assertions must be enabled')
rng=random.Random(13112606);counts=Counter();digest=hashlib.sha256();examples=[]


def blocks(vertices,E):
    vertices=set(vertices);adj={v:set() for v in vertices}
    for a,b in E:
        if a in adj and b in adj:adj[a].add(b);adj[b].add(a)
    unseen=set(vertices);out=[]
    while unseen:
        root=min(unseen);K={root};todo=[root]
        while todo:
            for u in adj[todo.pop()]-K:K.add(u);todo.append(u)
        unseen-=K;out.append(K)
    return out


def path_cost(U,E):return sum(len(K)//2 for K in blocks(U,E))


def literal_matching(U,E):
    adj={v:set() for v in U};memo={}
    for a,b in E:
        if a in adj and b in adj:adj[a].add(b);adj[b].add(a)
    def rec(S):
        if not S:return 0
        key=tuple(sorted(S))
        if key in memo:return memo[key]
        v=min(S);best=rec(S-{v})
        for u in adj[v]&S:best=max(best,1+rec(S-{v,u}))
        memo[key]=best;return best
    return rec(set(U))


def independent(S,E):return not any(i in S and j in S for i,j in E)


def abstract_check(n,E,U,Cs):
    rec=pair_conflicts(n,E,U,Cs);actual=[]
    if n<=3:
        assert pair_conflicts(n,iter(E),U,Cs)==rec
        counts['one_pass_edge_iterable_controls']+=1
    for i in range(len(Cs)):
        for j in range(i+1,len(Cs)):
            if any(K&Cs[i] and K&Cs[j] for K in blocks(U|Cs[i]|Cs[j],E)):actual.append([i,j])
    assert rec['edges']==actual
    for mask in range(1<<len(Cs)):
        S={i for i in range(len(Cs)) if mask>>i&1};W=U|{v for i in S for v in Cs[i]};Ks=blocks(W,E)
        disjoint=all(sum(bool(K&Cs[i]) for i in S)<=1 for K in Ks)
        assert disjoint==independent(S,actual)
        if disjoint:
            for i in S:
                a={frozenset(K) for K in Ks if K&Cs[i]}
                b={frozenset(K) for K in blocks(U|Cs[i],E) if K&Cs[i]}
                assert a==b;counts['common_individual_component_equalities']+=1
        counts['literal_common_activation_subsets']+=1
    counts['arbitrary_graph_models']+=1


# All simple graphs, all U, and canonical disjoint-set families with up to3 sets, n<=4.
for n in range(5):
    edge_list=list(combinations(range(n),2));families=[]
    for labels in product(range(4),repeat=n):
        first=[]
        for label in labels:
            if label and label not in first:first.append(label)
        if first!=list(range(1,len(first)+1)):continue
        families.append([{v for v,a in enumerate(labels) if a==label} for label in first])
    for emask in range(1<<len(edge_list)):
        E=[e for j,e in enumerate(edge_list) if emask>>j&1]
        for umask in range(1<<n):
            U={v for v in range(n) if umask>>v&1}
            for Cs in families:abstract_check(n,E,U,Cs)


def physical(x,z,two_connected=False):
    b=x['b'];n=2*b;E=x['P']+x['Q'];U=set(z['U']);assert path_cost(U,E)==z['actual_cost']<=z['cost_upper_bound']
    if n<=16:assert literal_matching(U,E)==z['actual_cost'];counts['literal_matching_controls']+=1
    G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
    assert all(colour[v]!=colour[u] for v in range(5*b) for u in G[v])
    assert max(map(len,G),default=0)<=3
    D=set(range(b))|{b+v for v in z['witnesses']}|{3*b+v for v in z['owners']}
    assert len(D)==z['beta_I_lower']==3*b-z['actual_cost'] and all(len(G[v]&D)<=1 for v in D)
    if two_connected:
        assert min(map(len,G))==2 and max(map(len,G))==3
        for removed in [None]+list(range(5*b)):
            available=set(range(5*b))-{removed};reached={min(available)};todo=list(reached)
            while todo:
                for u in (G[todo.pop()]&available)-reached:reached.add(u);todo.append(u)
            assert reached==available;counts['physical_vertex_deletion_connectivity_controls']+=removed is not None
        counts['two_connected_min2_max3_family_graphs']+=1
    counts['actual_physical_certificates']+=1;digest.update(json.dumps([x,z],sort_keys=True).encode())


def alpha(vertices,E):
    vertices=list(vertices);best=0
    for mask in range(1<<len(vertices)):
        S={v for j,v in enumerate(vertices) if mask>>j&1}
        if independent(S,E):best=max(best,len(S))
    return best


def optimum_budget(x,data):
    n=2*x['b'];U=set(data['initial_U']);E=x['P']+x['Q'];Cs=[set(c['vertices']) for c in data['candidates']]
    best=len(U);valid=0
    for mask in range(1<<len(Cs)):
        S=[i for i in range(len(Cs)) if mask>>i&1];required=U|{v for i in S for v in Cs[i]};free=sorted(set(range(n))-required)
        for extra in range(1<<len(free)):
            W=required|{v for j,v in enumerate(free) if extra>>j&1};Ks=blocks(W,E);used=set();okay=True
            for i in S:
                support={j for j,K in enumerate(Ks) if K&Cs[i]}
                if support&used or any(len(Ks[j]&U)%2 for j in support):okay=False;break
                used|=support
            counts['literal_candidate_W_pairs']+=1
            if not okay:continue
            valid+=1;rhs=(len(U)-sum(len(K&U)%2 for K in Ks))//2-len(S);best=min(best,rhs)
    expected=data['initial_cost']-alpha(data['good'],data['conflicts'])
    assert best==expected;counts['literal_all_W_budget_optima']+=1;counts['admissible_candidate_W_pairs']+=valid


for r in list(range(1,17))+[24,32,64]:
    x=separated_long_cycle_family(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    rec=greedy_conflict_certificate(*args,U=x['initial_U']);d=rec['data'];physical(x,rec['certificate'])
    assert d['initial_cost']==5*r and len(d['good'])==4*r and len(d['conflicts'])==4*r
    assert rec['maximum_degree']==2 and len(rec['colour_classes'])==2 and len(rec['selected_candidates'])==2*r
    assert rec['certificate']['cost_upper_bound']==3*r
    G=blocks(range(4*r),d['conflicts']);assert sorted(map(len,G))==[4]*r
    if r<=2:assert alpha(d['good'],d['conflicts'])==2*r
    counts['mixed_family_automatic_selection_controls']+=1

for r in list(range(2,33,2))+[48,64,128]:
    x=shared_even_path_family(r);args=[x[k] for k in ('b','P','Q','B','colour')];rec=greedy_conflict_certificate(*args,U=x['initial_U']);d=rec['data']
    assert d['initial_cost']==r and len(d['good'])==r and len(d['conflicts'])==r*(r-1)//2
    assert rec['maximum_degree']==r-1 and len(rec['selected_candidates'])==1 and rec['certificate']['cost_upper_bound']==r-1
    physical(x,rec['certificate'],True)
    zero=activated_budget(*args,[],U=x['zero_cost_U']);assert zero['actual_cost']==0 and zero['beta_I_lower']==6*r;physical(x,zero)
    if r<=32:
        initial=set(x['initial_U'])
        for c in d['candidates']:
            C=set(c['vertices']);fixed=initial-C;costs=[]
            for UC in combinations(sorted(C),2):costs.append(path_cost(fixed|set(UC),x['P']+x['Q']))
            assert min(costs)==r-1;counts['literal_single_owner_optima']+=1
    if r<=4:optimum_budget(x,d)
    if r in (2,4):
        best=2*r;permitted=0;Cs=[set(c['vertices']) for c in d['candidates']]
        for mask in range(1<<(4*r)):
            U={v for v in range(4*r) if mask>>v&1}
            if any(len(U&C)<2 for C in Cs):continue
            permitted+=1;best=min(best,path_cost(U,x['P']+x['Q']))
        assert best==0;counts['literal_unrestricted_U_family_optima']+=1;counts['literal_permitted_U_family_states']+=permitted
        examples.append(dict(name='clique obstruction r='+str(r),model=x,selection=rec,exact_beta_I=6*r))
    counts['clique_obstruction_family_controls']+=1


def random_model(n):
    L=list(range(0,n,2));R=list(range(1,n,2));rng.shuffle(L);rng.shuffle(R)
    P=list(zip(L[::2],L[1::2]))+list(zip(R[::2],R[1::2]));rng.shuffle(R);k=rng.randrange(n//2+1);Q=list(zip(L[:k],R[:k]));order=[v for pair in zip(L,R) for v in pair]
    B=[];off=0
    while off<n:
        size=min(n-off,rng.choice([4,4,6,8,10]));C=order[off:off+size];off+=size
        cyclic=size>=4 and size%2==0 and rng.randrange(4)!=0
        B+=list(zip(C,C[1:]+C[:1])) if cyclic else list(zip(C,C[1:]))
    return dict(b=n//2,P=P,Q=Q,B=B,colour=[v%2 for v in range(n)])


for n in (4,8,12,16,20,24,32,48,64):
    for trial in range(55):
        x=random_model(n);args=[x[k] for k in ('b','P','Q','B','colour')];od=prepare(*args)
        U=set().union(*(_minimum_omission(C,c) for C,c in od['owner_components']))
        if trial%3==0:U|={v for v in range(n) if rng.randrange(5)==0};counts['nonminimum_initial_U_models']+=1
        rec=greedy_conflict_certificate(*args,U=U);d=rec['data'];physical(x,rec['certificate']);base=blocks(U,x['P']+x['Q'])
        assert d['initial_cost']==path_cost(U,x['P']+x['Q'])
        eligible=[]
        for j,c in enumerate(d['candidates']):
            C=set(c['vertices']);Ks=blocks(U|C,x['P']+x['Q']);R=set().union(*(K for K in Ks if K&C))
            penalty=sum(len(K)%2 for K in base if K&R)
            assert penalty==c['penalty_d'] and c['good']==(penalty==0)
            if c['individually_eligible']:eligible.append(j)
        masks=range(1<<len(eligible)) if len(eligible)<=7 else [0]+[1<<j for j in range(len(eligible))]
        for mask in masks:
            S={v for j,v in enumerate(eligible) if mask>>j&1}
            if not independent(S,d['conflicts']):continue
            chosen=[d['candidates'][i]['cycle'] for i in sorted(S)]
            z=activated_budget(*args,chosen,U=U);expected=d['initial_cost']+sum(d['candidates'][i]['penalty_d']//2-1 for i in S)
            assert z['cost_upper_bound']==expected;physical(x,z)
            counts['literal_parity_formula_controls']+=1
            counts['selected_positive_parity_penalties']+=sum(d['candidates'][i]['penalty_d']>0 for i in S)
        if n<=12 and trial<7:optimum_budget(x,d)

assert counts['selected_positive_parity_penalties']>0
# Reproduce the reviewer's valid long-path input beyond the default call-stack depth.
n=2048;x=dict(b=n//2,P=[(v,v+1) for v in range(0,n,2)],
              Q=[(v,v+1) for v in range(1,n-1,2)],
              B=[(0,2),(2,1),(1,3),(3,0)],colour=[(v//2)%2 for v in range(n)])
long=greedy_conflict_certificate(*(x[k] for k in ('b','P','Q','B','colour')),U=range(2,n))
assert long['data']['initial_cost']==1023 and len(long['data']['good'])==1
assert long['certificate']['cost_upper_bound']==long['certificate']['actual_cost']==1022
physical(x,long['certificate']);counts['long_augmenting_path_physical_controls']+=1
empty=greedy_conflict_certificate(0,[],[],[],[]);assert empty['certificate']['actual_cost']==0
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/omission-conflict-graph-check.json');opt=parser.parse_args()
report=dict(counts=dict(sorted(counts.items())),deterministic_sha256=digest.hexdigest(),critical_examples=examples,
            scope='Generic pair lemma exhaustive for all simple graphs/U/canonical disjoint candidate families<=3,n<=4. Declared small physical slices enumerate all S,W and compare the exact numerical-budget optimum. Physical certificates and all-r families have independent counts and written proofs. No polynomial maximum independent set, unrestricted SF coefficient, universal8b/3 or general-grid claim.')
opt.output.parent.mkdir(parents=True,exist_ok=True);opt.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='critical_examples'}))
