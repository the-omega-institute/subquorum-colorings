"""Identity-safe admission of previously unused betas by shortest-path shortcuts.

General proof: docs/NEW_BETA_IDENTITY_SAFE_AUGMENTATION.md.
Production uses physical residual flow only; primitive DP is a test oracle.
"""
import argparse
from collections import Counter,defaultdict
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_general_bridge_retention import old_paths,exact_normal
from check_private_prefix_bridge import frame_with_direct_sources,request_data,lift
from check_old_link_batch_repair import allocation,signature
from check_single_bridge_compensation import stem
from check_whole_support_fork_normal_form import canonical,primitive_certificates,optimize
from check_compensation_flow_normal_form import owner_data

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def extend(data,before,E0,added,fees=None,declared=None):
    """Extend any normalized zero-fee baseline; all its boundary IDs persist.

    E0 must be a directed owner forest (the old reference skeleton). All new
    links are charged, even if their monetary fee is zero. The path arc-count
    tiebreak is local to each augmentation, not a fourth global objective.
    """
    own,A,B,X=owner_data(*data[:2]);E0=set(E0);added=sorted(set(added))
    declared=A if declared is None else set(declared)
    assert declared<=A and set(before['paid'])<=declared
    assert not E0&set(added) and E0|set(added)<=set(data[2])
    fees=dict.fromkeys(added,1) if fees is None else fees
    assert set(fees)==set(added) and all(isinstance(w,int) and w>=0 for w in fees.values())
    # Check old forest without enumerating primitives.
    out=defaultdict(list);indegree=Counter()
    for u,v in E0:
        assert own[u]!=own[v];out[own[u]].append(own[v]);indegree[own[v]]+=1
    remaining=set(range(len(data[1])));todo=[o for o in remaining if not indegree[o]]
    while todo:
        o=todo.pop();remaining.remove(o)
        for q in out[o]:
            indegree[q]-=1
            if not indegree[q]:todo.append(q)
    assert not remaining
    initial=old_paths(data,before)
    assert len(initial)==before['value']==len(before['paid'])
    assert {p['source'] for p in initial}==set(before['paid'])
    assert {p['resource'][1] for p in initial if p['resource'][0]=='interval'}==before['used']
    assert len({p['resource'] for p in initial})==len(initial)
    assert all(set(p['links'])<=E0 for p in initial)
    active_beta={p['resource'][1] for p in initial if p['resource'][0]=='beta'}
    # Reverse the physical alpha-to-payment network. All arcs have unit capacity.
    s=('source',);t=('sink',);edges=[];adj=defaultdict(list);tags={}
    def add(u,v,tag,cost=0):
        assert tag not in tags;i=len(edges);tags[tag]=i
        edges.extend([dict(u=u,v=v,cap=1,initial=1,cost=cost,tag=tag),
                      dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    def use(i):
        assert edges[i]['cap'];edges[i]['cap']-=1;edges[i^1]['cap']+=1
    exit=lambda o:('alpha',o) if o in A else ('out',o) if o in X else ('beta',o)
    for j in sorted(data[4]):add(s,('unit',j),('interval',j))
    for b in sorted(B):
        add(s,exit(b),('beta',b))
        for tip in data[1][b]:add(exit(b),('tip',tip),('port',tip))
    for x in sorted(X):add(exit(x),('in',x),('mixed',x))
    for a in sorted(declared):add(exit(a),t,('alpha',a))
    for o in sorted(data[3]):
        for j in sorted(data[3][o]):add(('unit',j),exit(o),('access',o,j))
    scale=len(added)+1
    for e in sorted(E0|set(added)):
        a,b=e
        if own[a]==own[b]:continue
        head=('tip',b) if own[b] in B else ('in',own[b])
        add(head,exit(own[a]),('link',a,b),fees[e]*scale+1 if e in fees else 0)
    for p in initial:
        use(tags[p['resource']]);current=p['owners'][-1]
        if p['resource'][0]=='interval':use(tags['access',current,p['resource'][1]])
        for a,b in reversed(p['links']):
            assert own[b]==current
            use(tags[('port',b) if current in B else ('mixed',current)])
            use(tags['link',a,b]);current=own[a]
        assert current==p['source'];use(tags['alpha',current])
    protected=[tags[p['resource']] for p in initial]+[tags['alpha',p['source']] for p in initial]
    value=len(initial);combined=0;nodes=set(adj)|{s,t};augmentations=[]
    def normality():
        result={}
        for b in B:
            whole=1-edges[tags['beta',b]]['cap']
            ports=sum(1-edges[tags['port',tip]]['cap'] for tip in data[1][b])
            intervals=sum(1-edges[tags['access',b,j]]['cap'] for j in data[3][b])
            assert ports==whole+intervals and ports<=2
            assert not ports or whole==1
            result[b]=whole
        return result
    def cost_audit():
        potential={v:0 for v in nodes}
        for _ in range(len(nodes)):
            changed=False
            for e in edges:
                if e['cap'] and potential[e['v']]>potential[e['u']]+e['cost']:
                    potential[e['v']]=potential[e['u']]+e['cost'];changed=True
            if not changed:break
        assert not changed, 'Negative residual cycle'
        assert all(e['cost']+potential[e['u']]-potential[e['v']]>=0 for e in edges if e['cap'])
        return True
    cost_audit();normality()
    while True:
        beta_before=normality();distance={s:(0,0)};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if not e['cap'] or e['u']==t or e['v']==s or e['u'] not in distance:continue
                d=(distance[e['u']][0]+e['cost'],distance[e['u']][1]+1)
                if e['v'] not in distance or d<distance[e['v']]:
                    distance[e['v']]=d;parent[e['v']]=i;changed=True
            if not changed:break
        if t not in distance:break
        v=t;seen=set();path=[]
        while v!=s:
            assert v not in seen;seen.add(v);i=parent[v];path.append(i);v=edges[i]['u']
        forward=list(reversed(path))
        # An unused beta must be entered directly from the private source arc.
        # Otherwise its source shortcut has <= cost and fewer residual arcs.
        for position,i in enumerate(forward):
            e=edges[i]
            if e['v'][0]=='beta' and not beta_before[e['v'][1]]:
                assert position==0 and e['tag']==('beta',e['v'][1])
        for i in path:use(i)
        assert all(edges[i]['cap']==0 for i in protected)
        value+=1;combined+=distance[t][0]
        beta_after=normality();cost_audit()
        augmentations.append(dict(cost=distance[t][0],residual_arc_count=distance[t][1],new_beta=sum(beta_after[b]-beta_before[b] for b in B),reversed_links=sum(i%2 and edges[i^1]['tag'][0]=='link' for i in path)))
    cut_side={s};todo=[s]
    while todo:
        u=todo.pop()
        for i in adj[u]:
            e=edges[i]
            if e['cap'] and e['v'] not in cut_side:cut_side.add(e['v']);todo.append(e['v'])
    cut=[e for e in edges[::2] if e['u'] in cut_side and e['v'] not in cut_side]
    assert t not in cut_side and sum(e['initial'] for e in cut)==value
    cost_audit()
    # Every used beta retains its private source credit from first activation.
    # Thus path extraction never performs an interval-releasing substitution.
    remaining={i:e['initial']-e['cap'] for i,e in enumerate(edges) if i%2==0};paths=[]
    for i in adj[s]:
        if i%2 or not remaining[i]:continue
        u=s;ptags=[];seen=set()
        while u!=t:
            assert u not in seen;seen.add(u)
            j=next(j for j in adj[u] if j%2==0 and remaining[j])
            remaining[j]-=1;e=edges[j];ptags.append(e['tag']);u=e['v']
        beta=[own[z[1]] for z in ptags if z[0]=='port'];assert len(beta)<=1
        witness=next((z[1] for z in ptags if z[0]=='access'),None)
        es=[(z[1],z[2]) for z in reversed(ptags) if z[0]=='link']
        a=ptags[-1][1];os={a}|{z[1] for z in ptags if z[0]=='mixed'}|set(beta)
        paths.append(dict(source=a,resource=ptags[0],owners=os,links=es,beta=beta[0] if beta else None,witness=witness))
    assert not any(remaining.values())
    groups=defaultdict(list);certs=[]
    for p in paths:
        if p['beta'] is None:
            assert p['resource'][0]=='interval'
            certs.append(stem(tuple(sorted(p['owners'])),p['links'],p['resource'][1],p['witness']))
        else:groups[p['beta']].append(p)
    for b,ps in groups.items():
        assert 1<=len(ps)<=2 and sum(p['resource']==('beta',b) for p in ps)==1
        interval=[p for p in ps if p['resource'][0]=='interval'];assert len(interval)==len(ps)-1
        assert all(p['witness']==b for p in interval)
        certs.append(dict(kind='fork' if interval else 'beta',owners=tuple(sorted(set().union(*(p['owners'] for p in ps)))),
            links=tuple(e for p in ps for e in p['links']),interval=interval[0]['resource'][1] if interval else None,
            value=len(ps),beta=b,**({'witness':b} if interval else {})))
    selected=[e for p in certs for e in p['links']];actual_new=set(selected)&set(added)
    used={p['interval'] for p in certs if p['interval'] is not None}
    paid=set().union(set(),*(set(p['owners'])&A for p in certs))
    used_beta=set(groups)
    assert active_beta<=used_beta
    assert len(paid)==value and len(used)==value-len(used_beta)
    assert before['used']<=used and set(before['paid'])<=paid
    assert len(used-before['used'])+len(used_beta-active_beta)==value-before['value']
    assert sum(fees[e] for e in actual_new)*scale+len(actual_new)==combined
    assert len(selected)==len(set(selected)) and len({v for e in selected for v in e})==2*len(selected)
    return dict(accepted=True,value=value,fee=sum(fees[e] for e in actual_new),new_links=len(actual_new),
        certificates=certs,paid=sorted(paid),used=used,old_value=before['value'],old_paid=before['paid'],
        old_used=before['used'],old_beta=sorted(active_beta),fresh=used-before['used'],
        used_beta=sorted(used_beta),fresh_beta=sorted(used_beta-active_beta),
        selected_new=sorted(actual_new),cut_capacity=value,cut_tags=[e['tag'] for e in cut],
        cost_potential_certificate=True,augmentations=augmentations)


def solve(data,pack,added,fees=None,new_sources=frozenset(),baseline_matching=None):
    frame=frame_with_direct_sources(data,pack,new_sources)
    neighbours,_=request_data(data,frame);ledger=allocation(neighbours)
    old=dict(ledger['matching'] if baseline_matching is None else baseline_matching)
    assert len(old)==len(neighbours)-ledger['deficiency']
    assert len(set(old.values()))==len(old) and all(j in neighbours[d] for d,j in old.items())
    before=lift(data,frame,old)
    _,A,_,_=owner_data(*data[:2])
    declared=set().union(set(),*(set(p['owners'])&A for p in frame['certificates']))
    E0={e for p in frame['certificates'] for e in p['links']}
    return extend(data,before,E0,added,fees,declared)


def compare(data,pack,added,fees,counts,new_sources=frozenset(),baseline_matching=None):
    z=solve(data,pack,added,fees,new_sources,baseline_matching)
    frame=frame_with_direct_sources(data,pack,new_sources)
    E0={e for p in frame['certificates'] for e in p['links']}
    restricted=(*data[:2],sorted(E0|set(added)),*data[3:])
    _,A,_,_=owner_data(*data[:2]);assert A==set().union(set(),*(set(p['owners'])&A for p in frame['certificates']))
    ref=exact_normal(restricted,fees)
    keep=exact_normal(restricted,fees,set(z['old_paid']),z['old_used'])
    key=lambda r:(r['value'],r['fee'],r['new_links'])
    assert key(z)==key(ref)==key(keep)
    legal={signature(p) for p in primitive_certificates(*restricted)}
    assert all(signature(p) in legal for p in z['certificates'])
    counts['independent_unrestricted_lex_optima']+=1
    counts['independent_prescribed_source_interval_lex_optima']+=1
    counts['old_beta_models']+=bool(z['old_beta'])
    counts['old_fork_models']+=any(p['kind']=='fork' for p in pack['certificates'])
    counts['models_activating_new_beta']+=bool(z['fresh_beta'])
    counts['augmentations_activating_new_beta']+=sum(a['new_beta'] for a in z['augmentations'])
    counts['new_beta_forks']+=sum(p['kind']=='fork' and p['beta'] in z['fresh_beta'] for p in z['certificates'])
    counts['augmentations_with_reverse_links']+=sum(bool(a['reversed_links']) for a in z['augmentations'])
    return z


def beta_transport(r):
    assert r>=1
    kinds,pairs,_=canonical('A'*(r+1)+'M'*r+'B');n=r+1
    W={o:set() for o in range(2*n)};E0=[];ps=[]
    for i in range(1,n):
        x=n+i-1;e=(2*i,2*x);E0.append(e)
        W[i].add(i-1);W[x].add(i-1);ps.append(stem((i,x),[e]))
    added=[(2*i,2*(n+i)) for i in range(r)]+[(2*r,2*(2*n-1))]
    return (kinds,pairs,E0+added,W,set(range(r))),dict(certificates=ps),added,dict.fromkeys(added,1),{0}


def all_baselines(data,pack,added,fees,N,counts):
    frame=frame_with_direct_sources(data,pack,N);ns,_=request_data(data,frame)
    ledger=allocation(ns);size=len(ns)-ledger['deficiency'];requests=sorted(ns)
    reference=None
    def visit(i,matching,used):
        nonlocal reference
        if i==len(requests):
            if len(matching)!=size:return
            z=solve(data,pack,added,fees,N,matching)
            key=z['value'],z['fee'],z['new_links']
            if reference is None:reference=key
            assert key==reference
            counts['all_maximum_old_baselines']+=1
            return
        d=requests[i];visit(i+1,matching,used)
        for j in ns[d]-used:visit(i+1,matching|{d:j},used|{j})
    visit(0,{},set())


def controls(counts):
    # A:u old; C empty; beta B supports u. A also has a fresh v.
    # A cost-shortest residual route s-v-A-u-B-C-t loses u upon post-hoc
    # normalization. The shorter equal-cost s-B-C-t keeps old A:u instead.
    fixture=json.loads(Path('develop/fixtures/new_beta_shortest_path_tie.json').read_text())
    kinds,pairs,_=canonical(fixture['owner_types'])
    W={int(o):set(S) for o,S in fixture['support'].items()};added=[tuple(e) for e in fixture['added_links']]
    data=kinds,pairs,added,W,set(fixture['resources']);pack=dict(certificates=[stem((0,),[])])
    fees=dict.fromkeys(added,1)
    z=compare(data,pack,added,fees,counts,{1},{0:0})
    assert z['value']==2 and z['used']=={0} and z['fresh']==set() and z['fresh_beta']==[2]
    # Independent check of both equal-cost raw flows by explicit resource routes.
    raw=[dict(source=0,resource=('interval',1),owners=[0],links=[]),
         dict(source=1,resource=('interval',0),owners=[1,2],links=added)]
    good=[dict(source=0,resource=('interval',0),owners=[0],links=[]),
          dict(source=1,resource=('beta',2),owners=[1,2],links=added)]
    for paths in (raw,good):
        assert len({p['source'] for p in paths})==2
        assert len({p['resource'] for p in paths})==2
        for p in paths:
            if p['resource'][0]=='interval':assert p['resource'][1] in W[p['owners'][-1]]
        assert sum(sum(fees[e] for e in p['links']) for p in paths)==1
    assert fixture['raw_residual_arc_count']==7 and fixture['shortcut_residual_arc_count']==4
    # Both raw flows have maximum value 2 and fee1 (C has only one route).
    # Replacing raw C:u by C:beta drops the old u. This rejects arbitrary
    # cost-only tie selection + post-hoc normalization, not the main theorem.
    counts['explicit_cost_shortest_bad_normalization_control']=1
    # A newly activated beta later receives a second arm carrying an OLD unit.
    kinds,pairs,_=canonical('AAAB');added=[(2,6),(4,7)]
    data=kinds,pairs,added,{0:{0,1},1:set(),2:set(),3:{0}},{0,1}
    pack=dict(certificates=[stem((0,),[])])
    fork=compare(data,pack,added,dict.fromkeys(added,2),counts,{1,2},{0:0})
    assert fork['value']==3 and fork['old_used']=={0} and fork['used']=={0,1}
    assert fork['fresh_beta']==[3] and any(p['kind']=='fork' and p['interval']==0 for p in fork['certificates'])
    # Two links to the SAME BP port never supply a fork.
    same=[(2,6),(4,6)]
    zsame=compare((*data[:2],same,*data[3:]),pack,same,dict.fromkeys(same,2),counts,{1,2},{0:0})
    assert zsame['value']==2 and zsame['used']=={0}
    counts['same_actual_beta_port_capacity_control']=1
    for r in range(1,8):
        d,p,es,f,N=beta_transport(r);chain=compare(d,p,es,f,counts,N)
        assert chain['value']==r+1 and chain['old_value']==r
        assert len(chain['old_used'])==r and not chain['fresh'] and len(chain['fresh_beta'])==1
        assert chain['new_links']==r+1 and chain['fee']==r+1
        for e in es:
            other=[a for a in es if a!=e]
            assert solve(d,p,other,{a:f[a] for a in other},N)['value']==r
            counts['beta_transport_bridge_deletion_controls']+=1
    d,p,es,f,N=beta_transport(64)
    with patch(__name__+'.exact_normal',side_effect=AssertionError('No primitive DP')), \
         patch(__name__+'.primitive_certificates',side_effect=AssertionError('No primitives')), \
         patch(__name__+'.optimize',side_effect=AssertionError('No independent optimizer')):
        prod=solve(d,p,es,f,N)
    assert (prod['old_value'],prod['value'],len(prod['used']),len(prod['fresh_beta']),prod['new_links'])==(64,65,64,1,65)
    counts['production_beta_transport_r64']=1
    # Core theorem does not require two-owner incidence or an old maximum.
    kinds,pairs,_=canonical('AAAABM');edges=[(2,8),(4,9)]
    W={0:{0,2},1:set(),2:set(),3:{1},4:{0},5:{0}}
    data=kinds,pairs,edges,W,{0,1,2};fees=dict.fromkeys(edges,1)
    before=dict(value=1,paid=[0],used={0},certificates=[stem((0,),[],0,0)])
    core=extend(data,before,[],edges,fees)
    assert core['value']==4 and core['old_used']=={0} and core['used']=={0,1,2}
    assert core['fresh_beta']==[4] and any(p['kind']=='fork' for p in core['certificates'])
    ref=exact_normal(data,fees,{0},{0})
    assert (core['value'],core['fee'],core['new_links'])==(ref['value'],ref['fee'],ref['new_links'])
    empty=extend(data,dict(value=0,paid=[],used=set(),certificates=[]),[],edges,fees)
    assert (empty['value'],empty['fee'],empty['new_links'])==(ref['value'],ref['fee'],ref['new_links'])
    counts['arbitrary_support_nonmaximum_and_empty_baseline_controls']=2
    return dict(tie=z,new_beta_old_interval_fork=fork,production_chain=prod,nonmaximum_core=core)


def random_checks(counts):
    rng=random.Random(20261026137)
    for rep in range(1200):
        types=['AAAMMB','AAAAMMBB','AAAMMMBB','AAAAAMMBB'][rep%4]
        kinds,pairs,all_edges=canonical(types);own,A,B,X=owner_data(kinds,pairs)
        pool=[e for e in all_edges if own[e[0]]!=own[e[1]]]
        W={o:set() for o in range(len(pairs))};Q=set(range(rng.randint(1,6)))
        for j in Q:
            for o in rng.sample(list(W),rng.randint(1,2)):W[o].add(j)
        E=rng.sample(pool,rng.randint(0,min(7,len(pool))))
        old=optimize(kinds,pairs,E,W,Q);pack=dict(certificates=old['certificates'])
        paid=set().union(set(),*(set(p['owners'])&A for p in pack['certificates']));N=A-paid
        E0={e for p in pack['certificates'] for e in p['links']}
        candidates=[e for e in pool if e not in E0]
        added=rng.sample(candidates,rng.randint(0,min(9,len(candidates))))
        # Force new beta eligibility in half the systems where possible.
        if rep%2:
            inactive=B-{p['beta'] for p in pack['certificates'] if p['kind'] in ('beta','fork')}
            eligible=[e for e in candidates if own[e[1]] in inactive]
            if eligible:added=sorted(set(added)|{rng.choice(eligible)})
        fees={e:rng.randint(0,5) for e in added};data=kinds,pairs,sorted(E0|set(added)),W,Q
        compare(data,pack,added,fees,counts,N)
        if rep<24:all_baselines(data,pack,added,fees,N,counts)
        counts['seeded_arbitrary_head_models']+=1


def physical_new_beta(q,counts):
    import check_general_bridge_retention as previous
    from check_whole_support_fork_flow import fork_flow
    captured={}
    def record(data,pack,added,fees=None,new_sources=frozenset(),baseline_matching=None):
        captured.update(data=data,pack=pack,N=new_sources,baseline=baseline_matching)
        return solve(data,pack,added,fees,new_sources,baseline_matching)
    with patch.object(previous,'solve',record):
        mixed=previous.frozen_shared_stem(q,counts,production=q==16)
    data,pack,N,baseline=[captured[k] for k in ('data','pack','N','baseline')]
    added=[((5+30*i,19),(5+30*i,20)) for i in range(q)]
    assert set(added)<=set(data[2]);fees=dict.fromkeys(added,1)
    if q==16:
        with patch(__name__+'.exact_normal',side_effect=AssertionError('No DP')), \
             patch(__name__+'.primitive_certificates',side_effect=AssertionError('No primitives')), \
             patch(__name__+'.optimize',side_effect=AssertionError('No independent optimizer')):
            z=solve(data,pack,added,fees,N,baseline)
        counts['production_frozen_new_beta_q16']=1
    else:
        z=solve(data,pack,added,fees,N,baseline)
        E0={e for p in pack['certificates'] for e in p['links']}
        restricted=(*data[:2],sorted(E0|set(added)),*data[3:])
        assert fork_flow(*restricted)['value']==z['value']
        counts['frozen_new_beta_independent_full_values']+=1
        if q==1:
            ref=exact_normal(restricted,fees,set(z['old_paid']),z['old_used'])
            assert (ref['value'],ref['fee'],ref['new_links'])==(z['value'],z['fee'],z['new_links'])
            legal={signature(p) for p in primitive_certificates(*restricted)}
            assert all(signature(p) in legal for p in z['certificates'])
            assert not previous.solve(data,pack,added,fees,N,baseline)['accepted']
            counts['physical_previous_beta_guard_removed']=1
    assert z['value']==4*q and z['old_value']==3*q
    assert len(z['used'])==3*q and not z['fresh'] and len(z['fresh_beta'])==q
    assert z['new_links']==q and z['fee']==q
    counts['frozen_new_beta_admission_boards']+=1
    return dict(copies=q,mixed_head_regression=mixed,new_beta_payment=z['value'],
        old_payment=z['old_value'],old_intervals_retained=len(z['used']),fresh_intervals=0,
        fresh_whole_betas=len(z['fresh_beta']),new_links=z['new_links'],fee=z['fee'],
        example_certificate=z['certificates'] if q==1 else None)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();examples=controls(counts);random_checks(counts)
    physical=[physical_new_beta(q,counts) for q in (1,2,4,16)]
    report=dict(status='PASS',counts=dict(counts),examples=examples,physical=physical,
        proof='docs/NEW_BETA_IDENTITY_SAFE_AUGMENTATION.md',
        scope='Arbitrary new actual links, including newly reachable beta; maximum payment/minimum actual fee/then minimum new links retain all old paid alphas, original intervals and whole-beta credits. Shortest residual paths break cost ties by residual arc count, preserving beta normality after EVERY augmentation.',
        limitations=['Full flow/normalization theorem has a general written proof, not end-to-end Lean.','New-beta transport and tie control are abstract canonical systems; physical new-beta controls instantiate the theorem on the existing frozen board, not a newly discovered unrestricted compensation improvement.','No universal geometric 5/6 improvement.'])
    args.output.write_text(json.dumps(report,indent=2,default=lambda x:sorted(x))+'\n')
    print(json.dumps(dict(status=report['status'],counts=report['counts']),indent=2))


if __name__=='__main__':main()
