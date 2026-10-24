"""Exact whole-support fork flow with separate physical BP entry capacities.

The proof is in WHOLE_SUPPORT_FORK_FLOW_AND_RESOURCE_CUTS.md. Independent
primitive packing and terminal-matching enumeration are used only as checks.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import (
    canonical,optimize,optimize_by_forks,ordinary_flow,primitive_certificates,
    evaluate,brute,whole_support_data,contract,
)
from check_frozen_beta_support_fork import fixture,stacked,restrict,A,C,B
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_even_bridge_support_completion import endpoints_of
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def normalize_beta_paths(beta,paths):
    """The beta sink is private to these paths; changing one output is free."""
    assert 1<=len(paths)<=2
    changed=not any(p['resource']==('beta',beta) for p in paths)
    if changed:paths[0]['resource']=('beta',beta)
    assert sum(p['resource']==('beta',beta) for p in paths)==1
    assert sum(p['resource'][0]=='interval' for p in paths)==len(paths)-1
    return int(changed)


def fork_flow(kinds,pairs,links,support,resources,maximal_cut=False):
    owner,alphas,betas,mixed=owner_data(kinds,pairs)
    assert set(support)==set(range(len(pairs)))
    assert all(set(w)<=resources for w in support.values())
    source=('source',);sink=('sink',);edges=[];adj=defaultdict(list)
    def add(u,v,cap,cost=0,tag=None):
        i=len(edges);edges.extend([
            dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
            dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    exit=lambda o:('alpha',o) if o in alphas else ('out',o) if o in mixed else ('beta',o)
    for a in sorted(alphas):add(source,exit(a),1,tag=('source',a))
    for m in sorted(mixed):add(('in',m),exit(m),1,tag=('mixed',m))
    for b in sorted(betas):
        for tip in pairs[b]:add(('tip',tip),exit(b),1,tag=('tip',tip))
        add(exit(b),sink,1,tag=('beta',b))
    for j in sorted(resources):add(('interval',j),sink,1,tag=('interval',j))
    large=len(alphas)+1
    for a,b in sorted(set(links)):
        assert kinds[a]=='TP' and kinds[b]=='BP'
        if owner[a]==owner[b]:continue
        incoming=('tip',b) if owner[b] in betas else ('in',owner[b])
        add(exit(owner[a]),incoming,large,1,('link',a,b))
    for o in sorted(support):
        for j in sorted(support[o]):
            add(exit(o),('interval',j),large,tag=('access',o,j))
    nodes=set(adj)|{source,sink};value=cost=0
    while True:
        distance={source:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in distance:
                    candidate=distance[e['u']]+e['cost']
                    if e['v'] not in distance or candidate<distance[e['v']]:
                        distance[e['v']]=candidate;parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in distance:break
        v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v);i=parent[v]
            edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1;cost+=distance[sink]
    reachable={source};pending=[source]
    while pending:
        u=pending.pop()
        for i in adj[u]:
            e=edges[i]
            if e['cap'] and e['v'] not in reachable:reachable.add(e['v']);pending.append(e['v'])
    if maximal_cut:
        # The largest source side among all minimum cuts is the complement
        # of vertices that can reach the sink in the residual network.
        incoming=defaultdict(list)
        for e in edges:
            if e['cap']:incoming[e['v']].append(e['u'])
        sink_reachable={sink};pending=[sink]
        while pending:
            v=pending.pop()
            for u in incoming[v]:
                if u not in sink_reachable:sink_reachable.add(u);pending.append(u)
        reachable=nodes-sink_reachable
        assert source in reachable
    assert sink not in reachable
    cut=[e for e in edges[::2] if e['u'] in reachable and e['v'] not in reachable]
    assert sum(e['initial'] for e in cut)==value
    assert all(e['initial']==1 for e in cut)
    source_side={a for a in alphas if exit(a) in reachable}
    separator=[e['tag'] for e in cut if e['tag'][0]!='source']
    assert all(z[0] in ('mixed','tip','beta','interval') for z in separator)
    assert len(alphas)-value==len(source_side)-len(separator)
    # Independently delete just the mixed/tip/resource separator gates, then
    # recompute which original alpha sources have no remaining sink route.
    deleted=set(separator);forward=defaultdict(list)
    for e in edges[::2]:
        if e['tag'] not in deleted:forward[e['u']].append(e['v'])
    blocked=[]
    for a in sorted(alphas):
        seen={exit(a)};todo=[exit(a)]
        while todo:
            u=todo.pop()
            for v in forward[u]:
                if v not in seen:seen.add(v);todo.append(v)
        if sink not in seen:blocked.append(a)
    assert set(blocked)==source_side
    # A source-side beta body forces its WHOLE-beta unit and every supported
    # interval onto the resource side of this same cut, with shared I once.
    for b in betas:
        if exit(b) in reachable:
            assert ('beta',b) in deleted
            assert all(('interval',j) in deleted for j in support[b])
    # Integral forward paths. Positive link costs remove all directed cycles
    # in a minimum-cost flow. Private beta-sink normalization is free.
    remaining={i:e['initial']-e['cap'] for i,e in enumerate(edges) if i%2==0}
    paths=[]
    for i in adj[source]:
        if i%2 or not remaining[i]:continue
        u=source;tags=[];seen=set()
        while u!=sink:
            assert u not in seen;seen.add(u)
            j=next(j for j in adj[u] if j%2==0 and remaining[j]>0)
            remaining[j]-=1;e=edges[j];tags.append(e['tag']);u=e['v']
        beta=[owner[t[1]] for t in tags if t[0]=='tip']
        assert len(beta)<=1
        paths.append(dict(source=tags[0][1],owners={tags[0][1]}|
            {t[1] for t in tags if t[0]=='mixed'}|set(beta),
            links=[(t[1],t[2]) for t in tags if t[0]=='link'],
            resource=tags[-1],beta=beta[0] if beta else None,
            witness=next((t[1] for t in reversed(tags) if t[0]=='access'),None)))
    assert not any(remaining.values())
    groups=defaultdict(list);certs=[];normalizations=0
    for p in paths:
        if p['beta'] is None:
            assert p['resource'][0]=='interval'
            certs.append(dict(kind='interval',owners=tuple(sorted(p['owners'])),
                links=tuple(p['links']),interval=p['resource'][1],value=1,witness=p['witness']))
        else:groups[p['beta']].append(p)
    for b,ps in groups.items():
        assert 1<=len(ps)<=2
        assert len({p['links'][-1][1] for p in ps})==len(ps)
        normalizations+=normalize_beta_paths(b,ps)
        beta_paths=[p for p in ps if p['resource']==('beta',b)]
        interval_paths=[p for p in ps if p['resource'][0]=='interval']
        assert len(beta_paths)==1 and len(interval_paths)==len(ps)-1
        owners=set().union(*(p['owners'] for p in ps))
        chosen=tuple(e for p in ps for e in p['links'])
        certs.append(dict(kind='fork' if len(ps)==2 else 'beta',
            owners=tuple(sorted(owners)),links=chosen,
            interval=interval_paths[0]['resource'][1] if interval_paths else None,
            value=len(ps),beta=b,**({'witness':b} if interval_paths else {})))
    assigned=[p['interval'] for p in certs if p['interval'] is not None]
    allowners=[o for p in certs for o in p['owners']]
    chosen=[e for p in certs for e in p['links']]
    assert len(assigned)==len(set(assigned)) and len(allowners)==len(set(allowners))
    assert len(chosen)==cost and len({v for e in chosen for v in e})==2*len(chosen)
    assert sum(p['value'] for p in certs)==value
    assert evaluate(kinds,pairs,chosen,support,resources)['value']==value
    return dict(value=value,cost=cost,certificates=certs,links=chosen,
        beta_private_sink_normalizations=normalizations,
        cut=separator,source_side=sorted(source_side),blocked_sources=blocked,deficit=len(alphas)-value,
        source_side_betas=sorted(b for b in betas if exit(b) in reachable),
        source_side_intervals=sorted(j for j in resources if ('interval',j) in reachable),
        cut_side='largest' if maximal_cut else 'smallest',
        network_nodes=len(nodes),network_forward_arcs=len(edges)//2)


def compare(data,totals,terminal=False):
    flow=fork_flow(*data);expected=optimize(*data)
    assert (flow['value'],flow['cost'])==(expected['value'],expected['cost'])
    if terminal:
        answer,count=brute(*data)
        assert answer==(flow['value'],flow['cost']);totals['independent_terminal_matchings']+=count
    ordinary=ordinary_flow(*data)
    assert flow['value']>=ordinary['value']
    totals['models']+=1;totals['strict_value_gains']+=flow['value']>ordinary['value']
    totals['strict_cost_gains']+=flow['value']==ordinary['value'] and flow['cost']<ordinary['cost']
    totals['flows_with_forks']+=any(p['kind']=='fork' for p in flow['certificates'])
    totals['beta_private_sink_normalizations']+=flow['beta_private_sink_normalizations']
    totals['positive_deficit_cuts']+=flow['deficit']>0
    totals['cuts_with_BP_tip_gates']+=any(z[0]=='tip' for z in flow['cut'])
    return flow


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter()
    for types in ('AAB','AMB','AAM','ABB','AMM'):
        kinds,pairs,possible=canonical(types)
        for bits in range(1<<len(possible)):
            links=[e for i,e in enumerate(possible) if bits>>i&1]
            for access in range(1<<len(pairs)):
                support={o:({0} if access>>o&1 else set()) for o in range(len(pairs))}
                compare((kinds,pairs,links,support,{0}),totals,terminal=True)
    rng=random.Random(20261029)
    for i in range(800):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,6)))
        kinds,pairs,possible=canonical(types);rng.shuffle(possible)
        links=possible[:rng.randrange(min(12,len(possible))+1)]
        resources=set(range(rng.randrange(5)))
        support={o:{j for j in resources if rng.randrange(2)} for o in range(len(pairs))}
        compare((kinds,pairs,links,support,resources),totals,terminal=i<80)
    kinds,pairs,_=canonical('AAB');support={0:set(),1:set(),2:{0,1}}
    wrong_tip=compare((kinds,pairs,[(0,4),(2,4)],support,{0,1}),totals,True)
    good_tips=compare((kinds,pairs,[(0,4),(2,5)],support,{0,1}),totals,True)
    assert wrong_tip['value']==1 and good_tips['value']==2
    for before in [[('interval',0)],[('interval',0),('interval',1)],
                   [('beta',2)],[('beta',2),('interval',0)]]:
        ps=[dict(resource=r) for r in before]
        changed=normalize_beta_paths(2,ps)
        assert changed==(not any(r==('beta',2) for r in before))
        assert {p['resource'][1] for p in ps if p['resource'][0]=='interval'}<=\
               {r[1] for r in before if r[0]=='interval'}
        totals['forced_beta_normalization_controls']+=1
    kinds,pairs,_=canonical('AABMM')
    cost_data=(kinds,pairs,[(0,4),(2,5),(3,6),(7,8)],
               {0:set(),1:set(),2:{0},3:set(),4:{0}},{0})
    cost_flow=compare(cost_data,totals,True)
    assert (cost_flow['value'],cost_flow['cost'])==(2,2)
    assert (ordinary_flow(*cost_data)['value'],ordinary_flow(*cost_data)['cost'])==(2,3)
    physical=[]
    for q in range(1,9):
        for pattern in ('none','all','alternating'):
            current=stacked(q)
            added=[((12+16*i,3),(12+16*i,4)) for i in range(q)
                   if pattern=='all' or pattern=='alternating' and i%2==0]
            current=(*current[:3],current[3]+added)
            direct_check(*current);assert frozen_certificate(current)[0]==endpoints_of(current)
            data,_,_=whole_support_data(current,whole_bands(current));flow=fork_flow(*data)
            assert (flow['value'],flow['cost'])==(3*q,q+len(added))
            totals['frozen_physical_controls']+=1
            physical.append(dict(copies=q,pattern=pattern,value=flow['value'],cost=flow['cost']))
    current,_=fixture();data,meta,_=whole_support_data(current,whole_bands(current))
    owner,_,_,mixed=owner_data(*data[:2]);j=meta['owner'][4,7]
    reserved=restrict(data,{owner[x[0]] for x in (A,C,B)}|mixed,{j})
    reserved_flow=compare(reserved,totals,True)
    assert (reserved_flow['value'],reserved_flow['cost'])==(2,2)
    contractions=[]
    for fixed in ([],[((5,5),(5,6))],[((12,5),(12,6))],[((5,5),(5,6)),((12,5),(12,6))]):
        virtual=contract(data,fixed);flow=compare(virtual,totals,True)
        contractions.append(dict(fixed_links=fixed,value=flow['value'],cost=flow['cost']))
    # Exhaust ALL perfect matchings on the base fixture's fixed endpoint set.
    # This is a finite-footprint mate-surgery obstruction, not an all-grid proof.
    vertices=endpoints_of(current)
    adjacent={v:{w for w in vertices if sum(abs(a-b) for a,b in zip(v,w))==1} for v in vertices}
    def matchings(left,chosen):
        if not left:yield chosen;return
        v=min(left,key=lambda v:(len(adjacent[v]&left),v))
        for w in sorted(adjacent[v]&left):yield from matchings(left-{v,w},chosen+[(v,w)])
    surgeries=[]
    for matching in matchings(vertices,[]):
        variant=(*current[:3],matching);direct_check(*variant)
        frozen=frozen_certificate(variant)[0]==vertices
        assert frozen
        data,_,_=whole_support_data(variant,whole_bands(variant))
        flow=compare(data,totals,True);ordinary=ordinary_flow(*data)
        assert (flow['value'],flow['cost'])==(ordinary['value'],ordinary['cost'])
        surgeries.append(dict(matching=matching,value=flow['value'],cost=flow['cost'],frozen=frozen))
    assert len(surgeries)==4
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),physical=physical,
        same_BP_obstruction=wrong_tip,different_BP_fork=good_tips,
        physical_reserved_fork=reserved_flow,physical_C0=contractions,
        equal_value_lower_cost_control=cost_flow,all_fixed_endpoint_matchings=surgeries,
        scope='Exact fork-capable maximum compensation and minimum links via a single integral '
              'min-cost flow with separate BP entry capacities and private beta sink normalization. '
              'Independent primitive optimum and terminal-matching comparisons; general proof written. '
              'No physical unrestricted strict gain or universal grid bound claimed.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
