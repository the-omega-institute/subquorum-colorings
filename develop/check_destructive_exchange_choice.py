"""Exact choice of resource-replacing actions via one capacity-one token flow.

General proof: docs/DESTRUCTIVE_EXCHANGE_CHOICE.md. Standard library only.
"""
import argparse
from collections import Counter,defaultdict
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import canonical,primitive_certificates,optimize
from check_whole_support_fork_flow import fork_flow
from check_fixed_P_maximum_frozen_elbow import fixture
from check_frozen_elbow_selection_saturation import regions,compile_model,forests

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def compress(data,actions):
    kinds,pairs,links,W,Q=data;_,A,_,_=owner_data(kinds,pairs)
    used=set();resource_map={j:('old',j) for j in Q};groups=[]
    for i,action in enumerate(actions):
        withdrawn=set(action['withdraw']);assert withdrawn and withdrawn<=Q and not withdrawn&used
        assert action['target'] in A
        users={o for o,S in W.items() if S&withdrawn};assert len(users)<=1
        used|=withdrawn
        for j in withdrawn:resource_map[j]=('exchange',i)
        groups.append(dict(action=i,target=action['target'],withdrawn=sorted(withdrawn),old_users=sorted(users)))
    support={o:{resource_map[j] for j in S} for o,S in W.items()}
    resources=set(resource_map.values())
    baseline=kinds,pairs,links,support,resources
    return baseline,groups


def proxy(data,actions,enabled):
    base,groups=compress(data,actions);W={o:set(S) for o,S in base[3].items()}
    for i in enabled:W[actions[i]['target']].add(('exchange',i))
    return (*base[:3],W,base[4])


def apply(data,actions,chosen):
    """Abstract simultaneous adapter: activated sources use private units.

    Their previous supports may be discarded; private normalization proves
    that this has no effect on optimum payment or minimum physical links.
    """
    kinds,pairs,links,W,Q=data
    lost=set().union(set(),*(set(actions[i]['withdraw']) for i in chosen))
    active={actions[i]['target'] for i in chosen}
    support={o:({('old',j) for j in S-lost} if o not in active else set()) for o,S in W.items()}
    resources={('old',j) for j in Q-lost}
    for i in chosen:
        for k in range(len(actions[i]['withdraw'])):
            j=('new',i,k);resources.add(j);support[actions[i]['target']].add(j)
    return kinds,pairs,links,support,resources


def constrained_optimum(data,required=frozenset()):
    """Independent primitive-pack DP with prescribed old paid sources."""
    _,A,_,_=owner_data(*data[:2]);assert required<=A
    ps=primitive_certificates(*data);rid={j:i for i,j in enumerate(sorted(data[4]))}
    masks=[(sum(1<<o for o in p['owners']),0 if p['interval'] is None else 1<<rid[p['interval']]) for p in ps]
    by={a:[i for i,p in enumerate(ps) if a in p['owners']] for a in A}
    @lru_cache(None)
    def search(occupied,used):
        left=A-{a for a in A if occupied>>a&1}
        if not left:return (0,0)
        a=min(left);best=None if a in required else search(occupied|1<<a,used)
        for i in by[a]:
            om,im=masks[i]
            if om&occupied or im&used:continue
            rest=search(occupied|om,used|im)
            if rest is None:continue
            candidate=rest[0]+ps[i]['value'],rest[1]+len(ps[i]['links'])
            if best is None or (candidate[0],-candidate[1])>(best[0],-best[1]):best=candidate
        return best
    return search(0,0)


def token_flow(data,actions,enabled,weights,required=frozenset(),independent=True):
    """Integral min-cost max-flow, retaining both physical beta BP entries.

    An action is one parallel direct alpha->exchange-token arc. Its flow
    consumes the same capacity-one token as all old access to that group.
    """
    base,_=compress(data,actions);kinds,pairs,links,W,Q=base
    own,A,B,X=owner_data(kinds,pairs)
    assert len(weights)==len(actions) and all(isinstance(w,int) and w>=0 for w in weights)
    source=('source',);sink=('sink',);edges=[];adj=defaultdict(list)
    scale=len(pairs)+1;protect=(sum(weights)*scale+len(pairs)+1)
    def add(u,v,cap,cost=0,tag=None):
        i=len(edges);edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    exit=lambda o:('alpha',o) if o in A else ('out',o) if o in X else ('beta',o)
    for a in sorted(A):add(source,exit(a),1,-protect if a in required else 0,('source',a))
    for m in sorted(X):add(('in',m),exit(m),1,tag=('mixed',m))
    for b in sorted(B):
        for tip in pairs[b]:add(('tip',tip),exit(b),1,tag=('tip',tip))
        add(exit(b),sink,1,tag=('beta',b))
    for j in sorted(Q):add(('resource',j),sink,1,tag=('resource',j))
    large=len(A)+1
    for p,t in sorted(set(links)):
        if own[p]==own[t]:continue
        add(exit(own[p]),('tip',t) if own[t] in B else ('in',own[t]),large,1,('link',p,t))
    for o,S in W.items():
        for j in sorted(S):add(exit(o),('resource',j),large,tag=('access',o,j))
    for i in sorted(enabled):
        add(exit(actions[i]['target']),('resource',('exchange',i)),1,weights[i]*scale,('action',i))
    nodes=set(adj)|{source,sink};value=0
    while True:
        dist={source:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in dist:
                    alt=dist[e['u']]+e['cost']
                    if e['v'] not in dist or alt<dist[e['v']]:dist[e['v']]=alt;parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in dist:break
        v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v);i=parent[v];edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1
    used=[e for e in edges[::2] if e['initial']>e['cap']]
    chosen={e['tag'][1] for e in used if e['tag'][0]=='action'}
    paid={e['tag'][1] for e in used if e['tag'][0]=='source'}
    link_count=sum(e['initial']-e['cap'] for e in used if e['tag'][0]=='link')
    assert len({actions[i]['target'] for i in chosen})==len(chosen)
    assert required<=paid
    if independent:
        actual=constrained_optimum(apply(data,actions,chosen),required)
        assert actual==(value,link_count)
    return dict(value=value,action_weight=sum(weights[i] for i in chosen),links=link_count,
                chosen=sorted(chosen),paid=sorted(paid))


def subsets(items):
    items=sorted(items)
    for mask in range(1<<len(items)):yield {v for i,v in enumerate(items) if mask>>i&1}


def verify(data,actions,weights,counts):
    baseline,_=compress(data,actions);old=optimize(*data);compressed=optimize(*baseline)
    assert (old['value'],old['cost'])==(compressed['value'],compressed['cost'])
    _,A,_,_=owner_data(*data[:2]);required=set().union(set(),*(set(p['owners'])&A for p in old['certificates']))
    profiles={}
    for F in subsets(range(len(actions))):
        actual=apply(data,actions,F);answer=constrained_optimum(actual)
        protected=constrained_optimum(actual,required)
        profiles[frozenset(F)]=(answer,protected)
        counts['independent_selected_action_profiles']+=1
    records=[]
    for enabled in subsets(range(len(actions))):
        for keep in (False,True):
            B=required if keep else set()
            candidates=[]
            for F,(a,b) in profiles.items():
                if not F<=enabled:continue
                ans=b if keep else a
                if ans is not None:candidates.append((ans[0],sum(weights[i] for i in F),ans[1]))
            want=max(candidates,key=lambda x:(x[0],-x[1],-x[2]))
            result=token_flow(data,actions,enabled,weights,B)
            assert (result['value'],result['action_weight'],result['links'])==want
            if keep:assert result['value']==records[-1]['value']
            else:
                f=fork_flow(*proxy(data,actions,enabled))
                assert result['value']==f['value']
            counts['exact_enabled_and_source_preservation_profiles']+=1
            records.append(dict(enabled=sorted(enabled),preserve_old_sources=keep,**result))
    counts['models']+=1
    counts['old_optima_with_forks']+=any(p['kind']=='fork' for p in old['certificates'])
    counts['multiunit_withdrawal_groups']+=sum(len(x['withdraw'])>1 for x in actions)
    counts['repeated_target_models']+=len({a['target'] for a in actions})<len(actions)
    return records


def chain(n):
    """n actions, n sources, n tokens; only the full action set gains one."""
    assert n>=2;kinds,pairs,_=canonical('A'*n)
    W={a:({a} if a else set()) for a in range(n)}
    data=kinds,pairs,[],W,set(range(n))
    actions=[dict(target=a,withdraw={(a+1)%n}) for a in range(n)]
    return data,actions


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();rng=random.Random(2026102623);records=[]
    # A beta fork consumes just one group interval and one whole-beta sink.
    kinds,pairs,_=canonical('AAABM');data=(kinds,pairs,[(0,6),(2,7)],{0:set(),1:set(),2:set(),3:{0,1},4:set()},{0,1,2})
    actions=[dict(target=0,withdraw={2}),dict(target=2,withdraw={0,1})]
    beta_control=verify(data,actions,[1,1],counts)
    assert [constrained_optimum(apply(data,actions,F))[0] for F in (set(),{0},{1},{0,1})]==[2,2,2,3]
    same_tip=(kinds,pairs,[(0,6),(2,6)],data[3],data[4])
    verify(same_tip,actions,[1,1],counts)
    assert constrained_optimum(same_tip)[0]==1
    counts['separate_beta_BP_gate_controls']+=1
    kinds,pairs,_=canonical('AAA')
    common_witness=(kinds,pairs,[],{0:set(),1:set(),2:{0,1}},{0,1})
    alternatives=[dict(target=0,withdraw={0}),dict(target=1,withdraw={1})]
    verify(common_witness,alternatives,[1,1],counts)
    assert token_flow(common_witness,alternatives,{0,1},[1,1],{2})['value']==2
    counts['shared_old_witness_distinct_group_controls']+=1
    for _ in range(48):
        kinds,pairs,possible=canonical(rng.choice(('AAAMB','AABMM','AAABM')))
        rng.shuffle(possible);links=possible[:rng.randrange(9)]
        _,A,B,X=owner_data(kinds,pairs);m=rng.randrange(1,5);Q=set(range(2*m+2));W={o:set() for o in range(len(pairs))};acts=[];used=set()
        for i in range(m):
            group={2*i}
            if rng.randrange(2):group.add(2*i+1)
            used|=group
            if rng.randrange(4):W[rng.randrange(len(pairs))]|=group
            acts.append(dict(target=rng.choice(sorted(A)),withdraw=group))
        for j in Q-used:
            for o in W:
                if rng.randrange(4)==0:W[o].add(j)
        data=kinds,pairs,links,W,Q
        verify(data,acts,[rng.randrange(4) for _ in acts],counts)
    chain_records=[]
    for n in range(2,7):
        data,acts=chain(n);verify(data,acts,[1]*n,counts)
        for F in subsets(range(n)):
            assert (constrained_optimum(apply(data,acts,F))[0]==n)==(len(F)==n)
            assert fork_flow(*proxy(data,acts,F))['value']==(n if len(F)==n else n-1)
        ans=token_flow(data,acts,set(range(n)),[1]*n)
        assert (ans['value'],ans['action_weight'])==(n,n)
        chain_records.append(dict(actions=n,old_value=n-1,proper_enabled_subset_value=n-1,full_value=n,minimum_actions_for_gain=n))
    for n in (8,16,32,64):
        data,acts=chain(n);ans=token_flow(data,acts,set(range(n)),[1]*n,independent=False)
        assert ans['value']==ans['action_weight']==n
        counts['large_chain_flow_controls']+=1
    # Physical fixed-P maximum: E uses unsupported U, F withdraws z's Q.
    cur,bits,ranks,units=fixture();old,cl,_=compile_model(cur,regions(cur,bits,set(),set()));own,A,B,X=owner_data(*old[:2])
    fs=forests(cur,regions(cur,bits,set(),set()));a,b=own[3,12],own[5,17]
    get=lambda cells:{j for j in old[4] if fs[j][1]==cells}
    acts=[dict(target=a,withdraw=get(units['U'])),dict(target=a,withdraw=get(units['Q']))]
    physical=verify(old,acts,[1,1],counts)
    for e,f in itertools.product((False,True),repeat=2):
        F=({0} if e else set())|({1} if f else set())
        actual,cc,_=compile_model(cur,regions(cur,bits,{0} if e else set(),{0} if f else set()))
        actual_fs=forests(cur,regions(cur,bits,{0} if e else set(),{0} if f else set()))
        lost=set().union(set(),*(set(acts[i]['withdraw']) for i in F))
        old_surviving={fs[j][1] for j in old[4]-lost}
        new_units={units['K'] for i in F if i==0}|{units['J'] for i in F if i==1}
        assert {actual_fs[j][1] for j in actual[4]}==old_surviving|new_units
        assert actual[:2]==old[:2] and set(actual[2])==set(old[2])
        assert [x['body'] for x in cc]==[x['body'] for x in cl]
        for o in old[3]:
            if not F or o!=a:
                assert {actual_fs[j][1] for j in actual[3][o]}=={fs[j][1] for j in old[3][o]-lost}
        assert all({o for o,S in actual[3].items() if j in S}=={a}
                   for j in actual[4] if actual_fs[j][1] in new_units)
        real=optimize(*actual);abstract=constrained_optimum(apply(old,acts,F))
        assert (real['value'],real['cost'])==abstract
        counts['physical_adapter_profiles']+=1
    picked=token_flow(old,acts,{0,1},[1,1],{b})
    assert picked['chosen']==[0] and picked['value']==2
    # Without action cost, F-only can abandon b for cheaper links; source protection fixes this.
    loose=token_flow(old,acts,{1},[0,0]);kept=token_flow(old,acts,{1},[0,0],{b})
    assert loose['chosen']==[1] and kept['chosen']==[] and loose['value']==kept['value']==1
    # Two independently usable old units cannot be merged into one token.
    kinds,pairs,_=canonical('AAA')
    bad=(kinds,pairs,[],{0:{0},1:{1},2:set()},{0,1})
    rejected=False
    try:compress(bad,[dict(target=2,withdraw={0,1})])
    except AssertionError:rejected=True
    assert rejected and optimize(*bad)['value']==2
    counts['multi_owner_group_rejection_controls']+=1
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(counts),physical_optimum=picked,
        physical_enabled_choice_profiles=physical,beta_fork_synergy_profiles=beta_control,
        arbitrary_length_synergy_controls=chain_records,source_identity_control=dict(unprotected=loose,protected=kept),
        theorem='Under a simultaneous disjoint withdrawal/private-target adapter, each nonempty old withdrawal group has at most one old witness owner. Compress that group to one capacity-one token and add a direct target-to-token action arc. The fixed fork-capable proxy gives exactly the maximum over chosen action subsets, including repeated target alternatives. Nonnegative action weights and physical links optimize lexicographically by min-cost flow; any old maximum paid source set can be retained at maximum value. Applied actions and physical old/new pools are never unioned.',
        limits=['Does not assert that applying all enabled destructive actions attains the proxy optimum.',
            'Enabled-action gain need not be a matroid rank or submodular: arbitrary n-action complementarity exists in abstract exchange models.',
            'The arbitrary chain family is abstract, not a claimed frozen grid realization.',
            'Full physical adapter and fork normalization have written proofs; formal allocation scope separately stated. No universal5/6 improvement.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts),physical_choice=picked),indent=2))

if __name__=='__main__':main()
