"""Resource-first bridge repair with arbitrary sharing and beta saturation.

Proof: docs/GENERAL_BRIDGE_RETENTION_AND_DEFICIENT_RELAYS.md.
The old baseline must already use every reachable whole-beta credit.
All mixed-head additions to an old stem/fork skeleton satisfy that guard.
"""
import argparse
from collections import Counter,defaultdict
from functools import lru_cache
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_private_prefix_bridge import frame_with_direct_sources,request_data,lift
from check_old_link_batch_repair import allocation,signature
from check_single_bridge_compensation import stem
from check_whole_support_fork_normal_form import canonical,primitive_certificates,optimize
from check_whole_support_fork_flow import fork_flow
from check_compensation_flow_normal_form import owner_data

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def old_paths(data,pack):
    own,A,B,X=owner_data(*data[:2]);paths=[]
    for p in pack['certificates']:
        sources=sorted(set(p['owners'])&A)
        outgoing={own[u]:(u,v) for u,v in p['links']}
        for k,a in enumerate(sources):
            os=[a];es=[]
            while os[-1] in outgoing:
                e=outgoing[os[-1]];es.append(e);os.append(own[e[1]])
                assert len(os)==len(set(os))
            if p['kind']=='interval':resource=('interval',p['interval'])
            elif p['kind']=='beta' or k==0:resource=('beta',p['beta'])
            else:resource=('interval',p['interval'])
            if resource[0]=='interval':assert resource[1] in data[3][os[-1]]
            else:assert os[-1]==resource[1] and os[-1] in B
            paths.append(dict(source=a,owners=os,links=es,resource=resource))
    return paths


def exact_normal(data,fees,required=frozenset(),need=frozenset(),lex_links=True):
    """Independent finite primitive DP, used exclusively as a test oracle."""
    _,A,_,_=owner_data(*data[:2]);ps=primitive_certificates(*data)
    rid={j:i for i,j in enumerate(sorted(data[4]))};needed=sum(1<<rid[j] for j in need)
    masks=[(sum(1<<o for o in p['owners']),0 if p['interval'] is None else 1<<rid[p['interval']],
        sum(fees.get(e,0) for e in p['links']),sum(e in fees for e in p['links'])) for p in ps]
    by={a:[i for i,p in enumerate(ps) if a in p['owners']] for a in A}
    @lru_cache(None)
    def visit(om,rm):
        left=A-{a for a in A if om>>a&1}
        if not left:return (0,0,0,()) if rm&needed==needed else None
        a=min(left);best=None if a in required else visit(om|1<<a,rm)
        for i in by[a]:
            po,pr,pc,pn=masks[i]
            if po&om or pr&rm:continue
            z=visit(om|po,rm|pr)
            if z is None:continue
            candidate=(z[0]+ps[i]['value'],z[1]+pc,z[2]+pn,(i,)+z[3])
            key=lambda r:(r[0],-r[1],-r[2] if lex_links else 0)
            if best is None or key(candidate)>key(best):best=candidate
        return best
    z=visit(0,0)
    return None if z is None else dict(value=z[0],fee=z[1],new_links=z[2],
        certificates=[ps[i] for i in z[3]])


def solve(data,pack,added,fees=None,new_sources=frozenset(),baseline_matching=None):
    own,A,B,X=owner_data(*data[:2]);frame=frame_with_direct_sources(data,pack,new_sources)
    neighbours,_=request_data(data,frame);ledger=allocation(neighbours)
    old=dict(ledger['matching'] if baseline_matching is None else baseline_matching)
    assert len(old)==len(neighbours)-ledger['deficiency']
    assert len(set(old.values()))==len(old) and all(j in neighbours[d] for d,j in old.items())
    before=lift(data,frame,old);initial=old_paths(data,before)
    declared=set().union(set(),*(set(p['owners'])&A for p in frame['certificates']))
    E0={e for p in frame['certificates'] for e in p['links']};added=sorted(set(added))
    assert not E0&set(added) and E0|set(added)<=set(data[2])
    fees=dict.fromkeys(added,1) if fees is None else fees
    assert set(fees)==set(added) and all(isinstance(w,int) and w>=0 for w in fees.values())
    active_beta={p['resource'][1] for p in initial if p['resource'][0]=='beta'}
    assert active_beta=={p['beta'] for p in frame['certificates'] if p['kind'] in ('beta','fork')}
    out=defaultdict(list)
    for e in E0|set(added):
        assert data[0][e[0]]=='TP' and data[0][e[1]]=='BP'
        if own[e[0]]!=own[e[1]]:out[own[e[0]]].append(e)
    reached=set(declared);todo=list(declared);routes={a:[] for a in declared}
    while todo:
        o=todo.pop()
        for e in out[o]:
            target=own[e[1]]
            if target not in reached:
                reached.add(target);routes[target]=routes[o]+[e]
                if target not in B:todo.append(target)
    unsafe=(reached&B)-active_beta
    if unsafe:
        b=min(unsafe)
        return dict(accepted=False,reason='A reachable beta has no saturated old whole-beta credit.',
                    beta=b,reachability_path=routes[b],scope='Guard failure, not a routing or inequality counterexample.')
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
    while True:
        distance={s:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if not e['cap'] or e['u']==t or e['v']==s or e['u'] not in distance:continue
                d=distance[e['u']]+e['cost']
                if e['v'] not in distance or d<distance[e['v']]:
                    distance[e['v']]=d;parent[e['v']]=i;changed=True
            if not changed:break
        if t not in distance:break
        v=t;seen=set();path=[]
        while v!=s:
            assert v not in seen;seen.add(v);i=parent[v];path.append(i);v=edges[i]['u']
        for i in path:use(i)
        assert all(edges[i]['cap']==0 for i in protected)
        value+=1;combined+=distance[t]
        augmentations.append(dict(cost=distance[t],reversed_links=sum(i%2 and edges[i^1]['tag'][0]=='link' for i in path)))
    cut_side={s};todo=[s]
    while todo:
        u=todo.pop()
        for i in adj[u]:
            e=edges[i]
            if e['cap'] and e['v'] not in cut_side:cut_side.add(e['v']);todo.append(e['v'])
    cut=[e for e in edges[::2] if e['u'] in cut_side and e['v'] not in cut_side]
    assert t not in cut_side and sum(e['initial'] for e in cut)==value
    potential={v:0 for v in nodes}
    for _ in range(len(nodes)):
        changed=False
        for e in edges:
            if e['cap'] and potential[e['v']]>potential[e['u']]+e['cost']:
                potential[e['v']]=potential[e['u']]+e['cost'];changed=True
        if not changed:break
    assert not changed
    assert all(e['cost']+potential[e['u']]-potential[e['v']]>=0 for e in edges if e['cap'])
    # Source-first path extraction. Beta saturation makes normalization exact
    # without substituting any original interval by a new private beta.
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
    assert len(paid)==value and len(used)==value-len(active_beta)
    assert before['used']<=used and set(before['paid'])<=paid
    assert len(used-before['used'])==value-before['value']
    assert sum(fees[e] for e in actual_new)*scale+len(actual_new)==combined
    assert len(selected)==len(set(selected)) and len({v for e in selected for v in e})==2*len(selected)
    return dict(accepted=True,value=value,fee=sum(fees[e] for e in actual_new),new_links=len(actual_new),
        certificates=certs,paid=sorted(paid),used=used,old_value=before['value'],old_paid=before['paid'],
        old_used=before['used'],old_beta=sorted(active_beta),fresh=used-before['used'],
        selected_new=sorted(actual_new),cut_capacity=value,cut_tags=[e['tag'] for e in cut],
        cost_potential_certificate=True,augmentations=augmentations)


def compare(data,pack,added,fees,counts,N=frozenset(),all_baselines=False):
    z=solve(data,pack,added,fees,N);assert z['accepted']
    frame=frame_with_direct_sources(data,pack,N);E0={e for p in frame['certificates'] for e in p['links']}
    declared=set().union(set(),*(set(p['owners']) for p in frame['certificates']))
    _,A,_,_=owner_data(*data[:2]);allowed_sources=declared&A
    # All generated comparison cases declare every alpha.
    assert allowed_sources==A
    d=(*data[:2],sorted(E0|set(added)),data[3],data[4])
    ref=exact_normal(d,fees);assert (z['value'],z['fee'],z['new_links'])==(ref['value'],ref['fee'],ref['new_links'])
    constrained=exact_normal(d,fees,set(z['old_paid']),z['old_used'])
    assert constrained is not None and (constrained['value'],constrained['fee'],constrained['new_links'])==(z['value'],z['fee'],z['new_links'])
    legal={signature(p) for p in primitive_certificates(*d)}
    assert all(signature(p) in legal for p in z['certificates'])
    assert fork_flow(*d)['value']==z['value']
    counts['independent_lex_value_fee_new_link_optima']+=1
    counts['independent_prescribed_source_and_interval_optima']+=1
    counts['max_flow_cut_and_residual_cost_certificates']+=1
    counts['old_whole_beta_credit_models']+=int(bool(z['old_beta']))
    counts['old_fork_reference_models']+=int(any(p['kind']=='fork' for p in pack['certificates']))
    counts['augmenting_paths_with_reversed_links']+=sum(bool(a['reversed_links']) for a in z['augmentations'])
    if all_baselines:
        ns,_=request_data(data,frame);ledger=allocation(ns);size=len(ns)-ledger['deficiency'];ds=sorted(ns)
        def visit(i,m,used):
            if i==len(ds):
                if len(m)!=size:return
                r=solve(data,pack,added,fees,N,m)
                assert (r['value'],r['fee'],r['new_links'])==(z['value'],z['fee'],z['new_links'])
                counts['all_maximum_baseline_retention']+=1
                return
            d=ds[i];visit(i+1,m,used)
            for j in ns[d]-used:visit(i+1,m|{d:j},used|{j})
        visit(0,{},set())
    return z


def junction():
    # A,B,C,D,E,F alphas; X is B's empty/mixed receiver suffix; Y,Z receive C,D.
    case=json.loads(Path('develop/fixtures/deficient_tree_relay_junction.json').read_text())
    kinds,pairs,_=canonical(case['owner_types'])
    pack=dict(certificates=[stem(tuple(p['owners']),[tuple(e) for e in p['links']]) for p in case['old_stems']])
    E0=[e for p in pack['certificates'] for e in p['links']]
    W={int(o):set(S) for o,S in case['support'].items()}
    added=[tuple(e) for e in case['added_links']]
    return (kinds,pairs,E0+added,W,set(case['resources'])),pack,added,dict(zip(added,case['fees'])),set(case['new_sources'])


def transport(length):
    assert length>=1
    # A0,...,Al and X0,...,X(l-1),Y. Old stems Ai->X(i-1); Y is newly reached.
    n=length+1;kinds,pairs,_=canonical('A'*n+'M'*n);W={o:set() for o in range(2*n)}
    E0=[];ps=[]
    for i in range(1,n):
        x=n+i-1;e=(2*i,2*x);E0.append(e);os=(i,x);es=[e]
        W[i].add(i-1);W[x].add(i-1)
        ps.append(stem(os,es))
    W[2*n-1].add(length)
    added=[(2*i,2*(n+i)) for i in range(length)]+[(2*length,2*(2*n-1))]
    data=kinds,pairs,E0+added,W,set(range(n))
    return data,dict(certificates=ps),added,{e:1 for e in added},{0}


def abstract_checks(counts):
    data,pack,added,fees,N=junction();z=compare(data,pack,added,fees,counts,N,all_baselines=True)
    assert (z['old_value'],z['value'],z['new_links'])==(4,6,3)
    ns,_=request_data(data,frame_with_direct_sources(data,pack,N));ld=allocation(ns)
    assert sorted(len(c['demands']) for c in ld['components'] if c['deficient'])==[1,3]
    for e in added:
        other=[f for f in added if f!=e];r=solve(data,pack,other,{f:1 for f in other},N)
        assert r['value']==5
        counts['junction_bridge_essentiality_checks']+=1
    # The full component's two outgoing bridges and one incoming are necessary.
    samples=[dict(name='deficient_tree_transit_junction',old=4,new=6,gain=2,new_links=3,
                  tree_outgoing=2,tree_incoming=1,paid=z['paid'],certificates=z['certificates'])]
    # An added beta-head edge is safe when its whole-beta credit is saturated.
    kinds,pairs,_=canonical('AAAMB');E0=[(0,8)];added=[(4,9)]
    W={0:set(),1:{0},2:set(),3:set(),4:{1}}
    pack=dict(certificates=[dict(kind='beta',owners=(0,4),links=tuple(E0),interval=None,value=1,beta=4),stem((1,),[])])
    z=compare((kinds,pairs,E0+added,W,{0,1}),pack,added,{added[0]:3},counts,{2},all_baselines=True)
    assert z['value']==3 and z['fee']==3 and z['new_links']==1 and z['old_beta']==[4]
    counts['safe_added_beta_head_with_old_private_credit']=1
    # A previously paid beta fork retains both its private credit and interval.
    E0=[(0,8),(2,9)];added=[(4,6)];W={0:set(),1:set(),2:set(),3:{1},4:{0}}
    pack=dict(certificates=[dict(kind='fork',owners=(0,1,4),links=tuple(E0),interval=0,value=2,beta=4,witness=4)])
    z=compare((kinds,pairs,E0+added,W,{0,1}),pack,added,{added[0]:1},counts,{2},all_baselines=True)
    assert z['value']==3 and z['old_used']=={0} and any(p['kind']=='fork' for p in z['certificates'])
    for length in range(1,8):
        data,pack,added,fees,N=transport(length)
        z=compare(data,pack,added,fees,counts,N,all_baselines=length<=2)
        assert z['old_value']==length and z['value']==length+1 and z['new_links']==length+1
        assert len(z['fresh'])==1 and len(z['old_used'])==length
        for e in added:
            remaining=[f for f in added if f!=e]
            assert solve(data,pack,remaining,{f:1 for f in remaining},N)['value']==length
            counts['transport_bridge_essentiality_checks']+=1
    counts['all_length_transport_samples']=7
    rng=random.Random(20261026103);accepted=0;rejected=0
    for rep in range(320):
        kinds,pairs,all_edges=canonical('AAAMMB' if rep%2 else 'AAAAMMB')
        own,A,B,X=owner_data(kinds,pairs);pool=[e for e in all_edges if own[e[0]]!=own[e[1]]]
        W={o:set() for o in range(len(pairs))};Q=set(range(rng.randint(2,5)))
        for j in Q:
            for o in rng.sample(list(W),rng.randint(1,2)):W[o].add(j)
        old_edges=rng.sample(pool,rng.randint(0,min(5,len(pool))))
        old=optimize(kinds,pairs,old_edges,W,Q);pack=dict(certificates=old['certificates'])
        old_sources=set().union(set(),*(set(p['owners'])&A for p in old['certificates']));N=A-old_sources
        E0={e for p in pack['certificates'] for e in p['links']}
        candidates=[e for e in pool if e not in E0 and own[e[1]] in X]
        candidates=rng.sample(candidates,rng.randint(0,min(6,len(candidates))))
        fees={e:rng.randint(0,5) for e in candidates};data=kinds,pairs,sorted(E0|set(candidates)),W,Q
        z=compare(data,pack,candidates,fees,counts,N,all_baselines=accepted<18)
        accepted+=1
        if B:
            b=min(B);beta_edge=next(e for e in pool if own[e[1]]==b)
            if b not in z['old_beta'] and beta_edge not in E0:
                more=set(candidates)|{beta_edge};f={e:fees.get(e,1) for e in more}
                r=solve((*data[:2],sorted(E0|more),*data[3:]),pack,more,f,N)
                assert not r['accepted'] and r['beta']==b
                rejected+=1
    counts['random_mixed_head_models']=accepted
    counts['new_reachable_beta_guard_rejections']=rejected
    # No mode or primitive/full optimizer in the production solver.
    data,pack,added,fees,N=transport(64)
    with patch(__name__+'.exact_normal',side_effect=AssertionError('No primitive DP')), \
         patch(__name__+'.primitive_certificates',side_effect=AssertionError('No primitives')), \
         patch(__name__+'.fork_flow',side_effect=AssertionError('No original full optimizer')):
        z=solve(data,pack,added,fees,N)
    assert (z['old_value'],z['value'],z['new_links'],len(z['fresh']))==(64,65,65,1)
    counts['production_64_step_transport_no_mode_or_primitive_optimizer']=1
    return samples


def frozen_shared_stem(copies,counts,production=False):
    from check_frozen_mixed_gate_cycle import load_model,FIXTURE
    from check_P_free_pivot_interface import regions
    from check_degree_changing_bent_completions import compile_model
    from check_canonical_band_coarsening import forests
    from check_frozen_shared_mixed_gate import check_rank_certificate
    from check_promotion_cores import frozen_certificate
    from check_residual_corridors import direct_check
    case=json.loads(Path('develop/fixtures/frozen_shared_stem_bridge_synergy.json').read_text())
    R,C,T,M=load_model()[0];assert case['base_fixture']==FIXTURE.name
    shift=lambda v,k:(v[0]+30*k,v[1])
    cur=(30*copies-2,24,{shift(v,k) for k in range(copies) for v in T},
         [tuple(shift(v,k) for v in e) for k in range(copies) for e in M])
    bits={(r,c):False for r in range(0,cur[0],2) for c in range(0,24,2)}
    direct_check(*cur);data,_,_=compile_model(cur,regions(cur,bits));own,A,_,_=owner_data(*data[:2])
    raw=json.loads(FIXTURE.read_text());layers=[[shift(tuple(v),k) for k in range(copies) for v in layer] for layer in raw['freezing_layers']]
    assert len(check_rank_certificate(cur,layers))==308*copies and frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
    counts['strict_freezing_events']+=308*copies
    fs=forests(cur,regions(cur,bits));bycells={cc:j for j,(cap,cc) in fs.items() if cap}
    ps=[];added=[];N=set();baseline={};fees={}
    for k in range(copies):
        for i,p in enumerate(case['old_stems']):
            links=[tuple(shift(tuple(v),k) for v in e) for e in p['links']]
            os=[own[links[0][0]]]+[own[e[1]] for e in links]
            ps.append(stem(tuple(os),links))
            baseline[3*k+i]=bycells[frozenset(shift(tuple(v),k) for v in case['baseline_original_units_cells'][i])]
        for index,e in enumerate(case['added_links']):
            edge=tuple(shift(tuple(v),k) for v in e);added.append(edge);fees[edge]=case['fees'][index]
        N.add(own[shift(tuple(case['new_source_tip']),k)])
    pack=dict(certificates=ps)
    if production:
        with patch(__name__+'.exact_normal',side_effect=AssertionError('No primitive DP')), \
             patch(__name__+'.primitive_certificates',side_effect=AssertionError('No primitive enumeration')), \
             patch(__name__+'.fork_flow',side_effect=AssertionError('No original full optimizer')):
            z=solve(data,pack,added,fees,N,baseline)
        counts['production_frozen_shared_stems_no_independent_optimizer']=1
    else:
        z=solve(data,pack,added,fees,N,baseline)
        E0={e for p in ps for e in p['links']};restricted=(*data[:2],sorted(E0|set(added)),data[3],data[4])
        assert fork_flow(*restricted)['value']==z['value']
        counts['frozen_independent_restricted_full_flow_values']+=1
        if copies==1:
            ref=exact_normal(restricted,fees,set(z['old_paid']),z['old_used'])
            assert (ref['value'],ref['fee'],ref['new_links'])==(z['value'],z['fee'],z['new_links'])
            legal={signature(p) for p in primitive_certificates(*restricted)}
            assert all(signature(p) in legal for p in z['certificates'])
            for e in added:
                kept=[f for f in added if f!=e]
                r=solve(data,pack,kept,{f:fees[f] for f in kept},N,baseline)
                assert r['value']==3
                counts['frozen_two_bridge_joint_necessity_checks']+=1
            counts['frozen_independent_identity_prescribed_lex_optimum']=1
    assert z['value']==4*copies and z['old_value']==3*copies
    assert set(z['paid'])==A and z['new_links']==2*copies and z['fee']==sum(fees.values())
    assert len(z['old_used'])==3*copies and len(z['fresh'])==copies
    assert len(data[4])==155*copies-24
    counts['frozen_shared_stem_synergy_boards']+=1
    example={} if copies!=1 else dict(certificates=z['certificates'],
        used_units=[dict(id=j,cells=sorted(fs[j][1]),old=j in z['old_used']) for j in sorted(z['used'])])
    return dict(copies=copies,shape=list(cur[:2]),old_payment=z['old_value'],new_payment=z['value'],
        old_used_retained=len(z['old_used']),fresh_units=len(z['fresh']),new_links=z['new_links'],fee=z['fee'],
        cut_capacity=z['cut_capacity'],cost_potential_certificate=z['cost_potential_certificate'],
        production=production,example_certificate=example)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();samples=abstract_checks(counts)
    physical=[frozen_shared_stem(q,counts,production=q==16) for q in (1,2,4,16)]
    report=dict(status='PASS',counts=dict(counts),samples=samples,physical=physical,
        proof='docs/GENERAL_BRIDGE_RETENTION_AND_DEFICIENT_RELAYS.md',
        scope='Arbitrary added links with no newly reachable beta; all mixed-head additions to old normalized skeletons covered. Exact maximum payment, minimum actual new-link fee then count; retain all old paid sources and original used interval IDs. No disjoint-pair, deficient-donor or nondeficient-receiver guard.',
        limitations=['New reachable beta not already paid in baseline requires additional normalization argument.','No universal geometric 5/6 improvement.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
