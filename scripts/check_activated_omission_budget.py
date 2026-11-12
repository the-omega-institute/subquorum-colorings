"""Independent physical, activation-support and small optimum controls."""
from pathlib import Path
from collections import Counter
from itertools import product
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from activated_omission_budget import activated_budget,separated_long_cycle_family
from component_omission_budget import budget_certificate,one_K4_search
from owner_matching_certificate import prepare,materialize
from mixed_owner_bridges import _minimum_omission,cardinality_bridge,square_six_bridge,one_exception_bridge
from maximum_witness_loss import instance
if not __debug__:raise RuntimeError('Assertions must be enabled')
rng=random.Random(13112603);counts=Counter();digest=hashlib.sha256();examples=[]


def raw_components(vertices,edges):
    vertices=set(vertices);adj={v:set() for v in vertices}
    for a,c in edges:
        if a in adj and c in adj:adj[a].add(c);adj[c].add(a)
    unseen=set(vertices);answer=[]
    while unseen:
        K={min(unseen)};todo=list(K)
        while todo:
            for v in adj[todo.pop()]-K:K.add(v);todo.append(v)
        unseen-=K;answer.append(K)
    return answer


def literal_matching(U,E):
    adj={v:set() for v in U};memo={}
    for a,c in E:
        if a in adj and c in adj:adj[a].add(c);adj[c].add(a)
    def rec(S):
        key=tuple(sorted(S))
        if not S:return 0
        if key in memo:return memo[key]
        v=min(S);best=rec(S-{v})
        for u in adj[v]&S:best=max(best,1+rec(S-{v,u}))
        memo[key]=best;return best
    return rec(set(U))


def check(x,z,connected=False):
    b=x['b'];n=2*b;E=x['P']+x['Q'];U0=set(z['initial_U']);U=set(z['U']);W=set(z['activated_vertices'])
    assert len(U)==len(U0) and U<=W and U0<=W
    Ks=raw_components(W,E);sizes=[len(K&U0) for K in Ks]
    assert [sorted(K) for K in Ks]==z['activated_components']
    assert sizes==z['initial_component_omissions']
    owners=raw_components(range(n),x['B']);used=set()
    for p in z['packing']:
        C=owners[p['cycle']];assert C<=W
        assert sum(set(e)<=C for e in x['B'])==len(C) and len(C)%6
        assert len(C&U0)==(len(C)+2)//3
        support={j for j,K in enumerate(Ks) if K&C}
        assert support==set(p['support']) and not support&used
        assert all(sizes[j]%2==0 for j in support);used|=support
    assert z['cost_upper_bound']==(len(U0)-sum(k%2 for k in sizes))//2-len(z['packing'])
    assert z['final_component_omissions']==[len(K&U) for K in Ks]
    assert all(len(K&U)==sizes[j] for j,K in enumerate(Ks) if j not in used)
    # A[U] consists of paths/even cycles; its exact matching size is sum floor(|K|/2).
    cost=sum(len(K)//2 for K in raw_components(U,E))
    assert cost==z['actual_cost']<=z['cost_upper_bound']
    counts['independent_path_cycle_matching_controls']+=1
    if n<=16:
        assert literal_matching(U,E)==cost;counts['literal_matching_controls']+=1
    G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    physical_colour=[1-x['colour'][a] for a,c in x['P']]+x['colour']+[1-v for v in x['colour']]
    assert all(physical_colour[v]!=physical_colour[u] for v in range(5*b) for u in G[v])
    D=set(range(b))|{b+v for v in z['witnesses']}|{3*b+v for v in z['owners']}
    assert len(D)==z['beta_I_lower']==3*b-cost
    assert all(len(G[v]&D)<=1 for v in D)
    if connected:
        assert min(map(len,G))==2 and max(map(len,G))==3
        assert len(raw_components(range(5*b),[(v,u) for v in range(5*b) for u in G[v] if v<u]))==1
        counts['connected_min2_max3_family_graphs']+=1
    counts['actual_physical_certificates']+=1
    counts['changed_individual_component_counts']+=sum(a!=c for a,c in zip(sizes,z['final_component_omissions']))
    counts['selected_cycles_crossing_activated_components']+=sum(len(p['support'])>1 for p in z['packing'])
    digest.update(json.dumps([x,z],sort_keys=True).encode())


for r in list(range(1,25))+[32,48,64]:
    x=separated_long_cycle_family(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    z=activated_budget(*args,x['chosen_cycles'],U=x['initial_U']);check(x,z,True)
    assert z['cost_upper_bound']==z['actual_cost']==3*r and z['meets_target']
    assert len(z['activated_components'])==5*r and len(z['packing'])==2*r
    old=budget_certificate(*args,U=x['initial_U'])
    assert old['cost_upper_bound']==5*r-1 and len(old['packing'])==1
    whole=activated_budget(*args,[p['cycle'] for p in old['packing']],U=x['initial_U'],W=range(24*r))
    check(x,whole);assert whole['cost_upper_bound']==old['cost_upper_bound'];counts['whole_graph_specialization_controls']+=1
    zero=activated_budget(*args,[],U=x['zero_cost_U']);check(x,zero)
    assert zero['actual_cost']==0 and zero['beta_I_lower']==36*r
    counts['explicit_zero_cost_exact_family_controls']+=1
    d=prepare(*args);phases=product(range(2),repeat=r) if r<=8 else [tuple(rng.randrange(2) for _ in range(r)) for j in range(9)]
    for v in phases:
        assert len(materialize(d,list(v))['K4'])==r;counts['specified_matching_phase_controls']+=1
    if r<=8:
        assert one_K4_search(*args)['applicable']==(r==1);counts['exact_2SAT_family_controls']+=1
    if r>=2:
        assert not old['meets_target']
        assert not cardinality_bridge(*args)['applicable'] and not square_six_bridge(*args)['applicable'] and not one_exception_bridge(*args)['applicable']
        counts['beyond_prior_global_tests_and_prescribed_U_budget']+=1
    if r in (1,2):examples.append(dict(name='mixed long cycle r='+str(r),model=x,activation=z,whole_support=old,exact_beta_I=36*r))

# Multiple separated regions inside a single original component, including zero-count singleton support.
for r in list(range(1,17))+[24,32,64]:
    x=instance(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    U={8*i+j for i in range(r) for j in (0,1,2,3)}
    chosen=list(range(0,2*r,2));z=activated_budget(*args,chosen,U=U);check(x,z)
    assert z['cost_upper_bound']==z['actual_cost']==r;counts['old_Hr_separation_controls']+=1
    if r>=2:
        try:activated_budget(*args,list(range(2*r)),U=U)
        except AssertionError:counts['inconsistent_individual_activation_rejections']+=1
        else:raise AssertionError('Overlapping common activation supports accepted')


def random_model(n):
    col=[0]*(n//2)+[1]*(n//2);L=list(range(n//2));R=list(range(n//2,n));rng.shuffle(L);rng.shuffle(R)
    P=list(zip(L[::2],L[1::2]))+list(zip(R[::2],R[1::2]))
    rng.shuffle(L);rng.shuffle(R);k=rng.randrange(n//2+1);Q=list(zip(L[:k],R[:k]))
    order=[v for pair in zip(L,R) for v in pair];B=[];off=0
    while off<n:
        left=n-off;k=left if left<=4 else min(left,rng.choice([4,6,8,10,left]))
        C=order[off:off+k];off+=k;cyclic=k>=4 and k%2==0 and rng.randrange(4)!=0
        B+=list(zip(C,C[1:]+C[:1])) if cyclic else list(zip(C,C[1:]))
    return dict(b=n//2,P=P,Q=Q,B=B,colour=col)


for n in (4,8,12,16,20,24,32,48):
    for trial in range(45):
        x=random_model(n);args=[x[k] for k in ('b','P','Q','B','colour')];d=prepare(*args)
        U=set().union(*(_minimum_omission(C,c) for C,c in d['owner_components']))
        if trial%3==0:U|={v for v in range(n) if rng.randrange(5)==0};counts['nonminimum_initial_U_models']+=1
        ids=[i for i,(C,c) in enumerate(d['owner_components']) if c and len(C)%6 and len(U&set(C))==(len(C)+2)//3]
        masks=range(1<<len(ids)) if len(ids)<=4 else [0]+[1<<j for j in range(len(ids))]
        for mask in masks:
            chosen=[i for j,i in enumerate(ids) if mask>>j&1]
            required=U|{v for i in chosen for v in d['owner_components'][i][0]}
            for mode in range(3):
                W=required if mode==0 else set(range(n)) if mode==2 else required|{v for v in range(n) if rng.randrange(2)}
                Ks=raw_components(W,x['P']+x['Q']);used=set();valid=True
                for i in chosen:
                    C=set(d['owner_components'][i][0]);support={j for j,K in enumerate(Ks) if K&C}
                    if support&used or any(len(Ks[j]&U)%2 for j in support):valid=False
                    used|=support
                if not valid:
                    try:activated_budget(*args,chosen,U=U,W=W)
                    except AssertionError:counts['literal_ineligible_support_rejections']+=1
                    else:raise AssertionError('Invalid support allocation accepted')
                    continue
                z=activated_budget(*args,chosen,U=U,W=W);check(x,z)
                counts['consistent_activation_candidate_controls']+=1
                if mode==2:
                    old=budget_certificate(*args,U=U,chosen_cycles=chosen)
                    assert z['cost_upper_bound']==old['cost_upper_bound'];counts['whole_graph_specialization_controls']+=1
        # Exhaustive independent unrestricted-U optimum, not minimum-cardinality-only.
        if n<=12 and trial<6:
            best=3*x['b']
            for mask in range(1<<n):
                UU={v for v in range(n) if mask>>v&1};S=set(range(n))-UU
                if any(sum(v in e and set(e)<=S for e in x['B'])>1 for v in S):continue
                best=min(best,literal_matching(UU,x['P']+x['Q']))
            simple=activated_budget(*args,[],U=U)
            assert best<=simple['actual_cost'];counts['literal_unrestricted_U_optimum_controls']+=1

# Missing full cycle, duplicate cycle and out-of-domain activation are rejected.
x=separated_long_cycle_family(1);args=[x[k] for k in ('b','P','Q','B','colour')];i=x['chosen_cycles'][0]
for chosen,W in [([i],x['initial_U']),([i,i],None),([],[*x['initial_U'],24])]:
    try:activated_budget(*args,chosen,U=x['initial_U'],W=W)
    except AssertionError:counts['invalid_activation_input_rejections']+=1
    else:raise AssertionError('Invalid activation input accepted')
assert activated_budget(0,[],[],[],[],[])['actual_cost']==0
assert counts['selected_cycles_crossing_activated_components']>0
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/activated-omission-budget-check.json');opt=parser.parse_args()
report=dict(counts=dict(sorted(counts.items())),deterministic_sha256=digest.hexdigest(),critical_examples=examples,
            scope='One common activation graph; all-r proofs are in the note. Finite controls check physical certificates, literal supports and matching values. Only declared n<=12 slices enumerate unrestricted U. No universal8b/3, sharp unrestricted coefficient, optimum packing or general grid claim.')
opt.output.parent.mkdir(parents=True,exist_ok=True);opt.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='critical_examples'}))
