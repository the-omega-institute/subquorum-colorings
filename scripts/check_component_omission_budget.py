"""Physical and literal-matching audits of disjoint-support exchange budgets."""
from pathlib import Path
from itertools import product
from collections import Counter
import argparse,hashlib,json,random,sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'develop'))
from component_omission_budget import budget_certificate,coupled_family,one_K4_search
from mixed_owner_bridges import _minimum_omission,_permitted,square_six_bridge,one_exception_bridge,cardinality_bridge
from owner_matching_certificate import prepare,materialize,components
from all_helper_optimization import solve,score
from maximum_witness_loss import instance
if not __debug__:raise RuntimeError('Assertions must be enabled')
counts=Counter();digest=hashlib.sha256();rng=random.Random(13112602);examples=[]


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


def physical(x,rec,connected=False):
    b=x['b'];n=2*b;G=[set() for _ in range(5*b)]
    def edge(a,c):G[a].add(c);G[c].add(a)
    for i,(a,c) in enumerate(x['P']):edge(i,b+a);edge(i,b+c)
    for v in range(n):edge(b+v,3*b+v)
    for a,c in x['Q']:edge(b+a,b+c)
    for a,c in x['B']:edge(3*b+a,3*b+c)
    c=[1-x['colour'][a] for a,z in x['P']]+x['colour']+[1-v for v in x['colour']]
    assert all(c[v]!=c[u] for v in range(5*b) for u in G[v])
    assert max(map(len,G),default=0)<=3
    if connected:
        assert min(map(len,G))==2
        reached={0};todo=[0]
        while todo:
            for v in G[todo.pop()]-reached:reached.add(v);todo.append(v)
        assert len(reached)==5*b;counts['connected_min2_max3_physical_graphs']+=1
    D=set(range(b))|{b+v for v in rec['witnesses']}|{3*b+v for v in rec['owners']}
    assert len(D)==rec['beta_I_lower'] and all(len(G[v]&D)<=1 for v in D)
    assert rec['actual_cost']<=rec['cost_upper_bound']
    # Independently recover A components and support ownership from raw edges.
    adj=[set() for _ in range(n)]
    for a,c in x['P']+x['Q']:adj[a].add(c);adj[c].add(a)
    selected=set(rec['U']);remaining=set(selected);path_cost=0
    while remaining:
        C={min(remaining)};todo=list(C)
        while todo:
            for v in (adj[todo.pop()]&selected)-C:C.add(v);todo.append(v)
        remaining-=C;path_cost+=len(C)//2
    assert path_cost==rec['actual_cost']
    counts['independent_path_cycle_matching_controls']+=1
    blocks=[];unseen=set(range(n))
    while unseen:
        C={min(unseen)};todo=list(C)
        while todo:
            for v in adj[todo.pop()]-C:C.add(v);todo.append(v)
        unseen-=C;blocks.append(C)
    data=prepare(*(x[k] for k in ('b','P','Q','B','colour')))
    U0=set(rec['initial_U']);sizes=[len(C&U0) for C in blocks]
    assert sizes==rec['auxiliary_component_omissions']
    used=set()
    for p in rec['packing']:
        C,cyclic=data['owner_components'][p['cycle']]
        support={j for j,K in enumerate(blocks) if K&set(C)}
        assert support==set(p['support']) and not support&used
        assert cyclic and len(C)%6 and len(U0&set(C))==(len(C)+2)//3
        assert all(sizes[j]%2==0 for j in support);used|=support
    assert rec['cost_upper_bound']==(len(U0)-sum(k%2 for k in sizes))//2-len(rec['packing'])
    if n<=16:
        assert literal_matching(set(rec['U']),x['P']+x['Q'])==rec['actual_cost']
        counts['literal_matching_controls']+=1
    counts['actual_physical_certificates']+=1
    counts['cross_auxiliary_selected_cycles']+=sum(len(p['support'])>1 for p in rec['packing'])
    counts['changed_individual_component_counts']+=sum(a!=b for a,b in zip(sizes,rec['final_component_omissions']))
    digest.update(json.dumps([x,rec],sort_keys=True).encode())


for r in list(range(1,25))+[32,48,64]:
    x=coupled_family(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    direct=budget_certificate(*args,U=x['initial_U']);cross=budget_certificate(*args,U=x['initial_U'],chosen_cycles=x['crossing_cycles'])
    assert direct['cost_upper_bound']==2*r and len(direct['packing'])==2*r
    assert cross['cost_upper_bound']==3*r and len(cross['packing'])==r
    assert direct['meets_target'] and cross['meets_target']
    physical(x,direct,True);physical(x,cross)
    zU=set(x['zero_cost_U']);assert _permitted(20*r,x['B'],zU)
    assert not any(set(e)<=zU for e in x['P']+x['Q'])
    exact=budget_certificate(*args,U=zU,chosen_cycles=[])
    assert exact['actual_cost']==0 and exact['beta_I_lower']==30*r
    physical(x,exact)
    counts['explicit_zero_cost_exact_family_controls']+=1
    d=prepare(*args);minima=8*r;assert sum((len(K)+2)//3 if c else len(K)//3 for K,c in d['owner_components'])==minima
    phases=list(product(range(2),repeat=len(d['choices']))) if r<=8 else [tuple(rng.randrange(2) for _ in d['choices']) for _ in range(12)]
    for vals in phases:
        assert len(materialize(d,list(vals))['K4'])==r
        counts['specified_matching_phase_controls']+=1
    if r<=8:
        searched=one_K4_search(*args);assert searched['applicable']==(r==1)
        counts['exact_2SAT_family_controls']+=1
    if r>=2:
        assert not square_six_bridge(*args)['applicable'] and not one_exception_bridge(*args)['applicable'] and not cardinality_bridge(*args)['applicable']
        assert 12*r<2*((20*r+2)//3)-2
        counts['beyond_prior_global_tests']+=1
    if r in (1,2):examples.append({'name':'coupled r='+str(r),'model':x,'packed':direct,'crossing':cross,'exact_beta_I':30*r})


def random_model(n,trial):
    col=[0]*(n//2)+[1]*(n//2);L=list(range(n//2));RR=list(range(n//2,n));rng.shuffle(L);rng.shuffle(RR)
    P=list(zip(L[::2],L[1::2]))+list(zip(RR[::2],RR[1::2]));rng.shuffle(L);rng.shuffle(RR)
    k=rng.randrange(n//2+1);Q=list(zip(L[:k],RR[:k]));order=[v for pair in zip(L,RR) for v in pair]
    B=[];off=0
    while off<n:
        left=n-off;k=left if left<=4 else rng.choice([4,6,8,10,left])
        if k>left:k=left
        C=order[off:off+k];off+=k
        cyclic=k>=4 and k%2==0 and rng.randrange(4)!=0
        B+=list(zip(C,C[1:]+C[:1])) if cyclic else list(zip(C,C[1:]))
    return dict(b=n//2,P=P,Q=Q,B=B,colour=col)


for n in (4,8,12,16,20,24,32,48,64):
    for trial in range(70):
        x=random_model(n,trial);args=[x[k] for k in ('b','P','Q','B','colour')];data=prepare(*args)
        U=set().union(*(_minimum_omission(K,c) for K,c in data['owner_components']))
        if trial%3==0:
            U|={v for v in range(n) if rng.randrange(5)==0};counts['nonminimum_initial_U_models']+=1
        rec=budget_certificate(*args,U=U);physical(x,rec)
        E=rec['eligible_cycles']
        if len(E)<=8:
            for mask in range(1<<len(E)):
                chosen=[e for i,e in enumerate(E) if mask>>i&1];used=[]
                for e in chosen:used+=e['support']
                if len(set(used))!=len(used):continue
                other=budget_certificate(*args,U=U,chosen_cycles=[e['cycle'] for e in chosen]);physical(x,other)
                counts['literal_support_packing_controls']+=1
        if n<=16 and trial<12:
            vals=list(product(range(2),repeat=len(data['choices'])))
            minimum=min(len(materialize(data,list(v))['K4']) for v in vals)
            found=one_K4_search(*args);assert found['applicable']==(minimum<=1)
            if found['applicable']:
                assert found['certificate']['beta_I_lower']>=(8*x['b']+2)//3
            counts['literal_phase_versus_2SAT_controls']+=1

# Overlapping credits: every C4 of H_r consumes its one shared auxiliary slot.
for r in range(1,17):
    x=instance(r);args=[x[k] for k in ('b','P','Q','B','colour')]
    d=prepare(*args);U=set().union(*(_minimum_omission(K,c) for K,c in d['owner_components']))
    rec=budget_certificate(*args,U=U);assert len(rec['eligible_cycles'])==2*r and len(rec['packing'])==1
    assert rec['cost_upper_bound']==2*r-1 and x['beta_I']==12*r-(r+1)//2
    try:budget_certificate(*args,U=U,chosen_cycles=[0,1])
    except AssertionError:counts['overlap_rejections']+=1
    else:raise AssertionError('Shared auxiliary slot incorrectly spent twice')
    if r<=2:
        assert 3*x['b']-solve(x['b'],x['P'],x['Q'],x['B'])['beta_I']==(r+1)//2
        counts['exact_overcount_obstruction_controls']+=1
    physical(x,rec)

assert budget_certificate(0,[],[],[],[])['cost_upper_bound']==0
assert one_K4_search(0,[],[],[],[])['applicable']
assert counts['changed_individual_component_counts'] and counts['cross_auxiliary_selected_cycles']
parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,default=ROOT/'output/component-omission-budget-check.json');args=parser.parse_args()
report={'counts':dict(sorted(counts.items())),'deterministic_sha256':digest.hexdigest(),'critical_examples':examples,
        'scope':'General disjoint-support theorem and explicit all-r families have written proofs. Finite physical checks certify constructions; only declared small slices use literal optima. No optimal-packing, universal8b/3, unrestricted SF or general-grid result is claimed.'}
args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='critical_examples'}))
