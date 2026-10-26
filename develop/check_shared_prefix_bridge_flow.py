"""Exact shared-reserve bridge repair by one initialized min-cost flow.

Donors are in old deficient request trees, receivers in nondeficient request
components, and candidate stem pairs are disjoint. No private-unit guard.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_private_prefix_bridge import frame_with_direct_sources, request_data, lift
from check_single_bridge_compensation import ordered_stem, switched_skeleton, bridge_batch, stem
from check_old_link_batch_repair import allocation, signature
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import canonical, optimize, primitive_certificates
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def recognize(data, frame, bridges):
    own, _, _, _ = owner_data(*data[:2]); ps = frame['certificates']
    at = {o:i for i,p in enumerate(ps) for o in p['owners']}
    assert len(at) == sum(len(p['owners']) for p in ps)
    neighbours, users = request_data(data, frame); ledger = allocation(neighbours)
    component = {d:i for i,c in enumerate(ledger['components']) for d in c['demands']}
    occupied = set(); records = []
    for k,e in enumerate(bridges):
        switched_skeleton(data, frame, e)
        a,b = at[own[e[0]]],at[own[e[1]]]
        assert not {a,b}&occupied; occupied |= {a,b}
        if not ledger['components'][component[a]]['deficient']:
            return dict(accepted=False, reason='Donor not in deficient request tree.', bridge=k)
        if ledger['components'][component[b]]['deficient']:
            return dict(accepted=False, reason='Receiver not in nondeficient request component.', bridge=k)
        bo,_ = ordered_stem(data,ps[b]); cut = bo.index(own[e[1]])
        pre = set().union(set(),*(data[3][o] for o in bo[:cut]))
        post = set().union(set(),*(data[3][o] for o in bo[cut:]))
        records.append(dict(index=k,donor=a,receiver=b,tree=component[a],pre=pre,post=post))
    return dict(accepted=True,records=records,neighbours=neighbours,users=users,
                ledger=ledger,component=component)


def receiver_flow(neighbours, records, old, fees):
    """Start with a zero-cost maximum OLD allocation; augment in one graph.

    Source-unit and baseline-sink arcs already saturated never reverse on a
    simple augmenting source-to-sink path. Thus old original unit IDs and all
    old receiver baseline demands are retained even through negative fee swaps.
    """
    source=('source',); sink=('sink',); edges=[]; adj=defaultdict(list)
    def add(u,v,cap=1,cost=0,tag=None):
        i=len(edges); edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
            dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        adj[u].append(i); adj[v].append(i+1)
        return i
    def use(i):
        assert edges[i]['cap']>0
        edges[i]['cap']-=1; edges[i^1]['cap']+=1
    byreceiver={r['receiver']:r for r in records}
    units=set().union(set(),*neighbours.values())
    unit_arcs={j:add(source,('unit',j),tag=('unit',j)) for j in sorted(units)}
    accesses={}; side_arcs={}; bases={}; extras={}
    for d,J in sorted(neighbours.items()):
        r=byreceiver.get(d); sides={'pre':r['pre'],'post':r['post']} if r else {'whole':J}
        for side,S in sides.items():
            node=('slot',d,side)
            side_arcs[d,side]=add(node,('request',d),tag=('side',d,side))
            for j in sorted(S):
                accesses[d,side,j]=add(('unit',j),node,tag=('access',d,side,j))
        bases[d]=add(('request',d),sink,tag=('base',d))
        if r:
            extras[r['index']]=add(('request',d),('tree',r['tree']),cost=fees[r['index']],
                                  tag=('bridge',r['index']))
    for t in sorted({r['tree'] for r in records}):add(('tree',t),sink,tag=('tree',t))
    for d,j in sorted(old.items()):
        assert d in neighbours and j in neighbours[d]
        side=next(s for dd,s in side_arcs if dd==d and (d,s,j) in accesses)
        for i in (unit_arcs[j],accesses[d,side,j],side_arcs[d,side],bases[d]):use(i)
    assert set(old)==set(neighbours)
    value=len(old); cost=0; augmentations=[]; nodes=set(adj)
    while True:
        distance={source:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if not e['cap'] or e['u']==sink or e['v']==source or e['u'] not in distance:continue
                candidate=distance[e['u']]+e['cost']
                if e['v'] not in distance or candidate<distance[e['v']]:
                    distance[e['v']]=candidate;parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in distance:break
        v=sink;seen=set();path=[]
        while v!=source:
            assert v not in seen;seen.add(v);i=parent[v];path.append(i);v=edges[i]['u']
        for i in path:use(i)
        value+=1;cost+=distance[sink];augmentations.append(dict(cost=distance[sink],
            reverses_bridge_fee=any(i%2 and edges[i^1]['tag'] and edges[i^1]['tag'][0]=='bridge' for i in path)))
        assert all(edges[i]['cap']==0 for i in bases.values())
        assert all(edges[unit_arcs[j]]['cap']==0 for j in old.values())
    reachable={source};pending=[source]
    while pending:
        u=pending.pop()
        for i in adj[u]:
            e=edges[i]
            if e['cap'] and e['v'] not in reachable:reachable.add(e['v']);pending.append(e['v'])
    cut=[e for e in edges[::2] if e['u'] in reachable and e['v'] not in reachable]
    assert sink not in reachable and sum(e['initial'] for e in cut)==value
    # Global residual potentials independently certify minimum cost, including
    # residual arcs incident with source/sink that augmentation never traverses.
    potential={v:0 for v in nodes}
    for _ in range(len(nodes)):
        changed=False
        for e in edges:
            if e['cap'] and potential[e['v']]>potential[e['u']]+e['cost']:
                potential[e['v']]=potential[e['u']]+e['cost'];changed=True
        if not changed:break
    assert not changed, 'Negative residual cycle: fee is not minimum.'
    assert all(e['cost']+potential[e['u']]-potential[e['v']]>=0 for e in edges if e['cap'])
    slots={}
    for (d,side,j),i in accesses.items():
        if edges[i^1]['cap']:
            assert (d,side) not in slots;slots[d,side]=j
    selected=sorted(k for k,i in extras.items() if edges[i^1]['cap'])
    assert len(selected)==value-len(old) and cost==sum(fees[k] for k in selected)
    used={j for j,i in unit_arcs.items() if edges[i^1]['cap']}
    assert len(used)==value and set(old.values())<=used
    return dict(value=value,cost=cost,slots=slots,selected=selected,used=used,
                cut_capacity=value,cut_tags=[e['tag'] for e in cut],augmentations=augmentations,
                residual_min_cost_certificate=True,potential=potential)


def solve(data,pack,bridges,fees=None,new_sources=frozenset(),baseline_matching=None):
    frame=frame_with_direct_sources(data,pack,new_sources);c=recognize(data,frame,bridges)
    if not c['accepted']:return c
    fees=dict.fromkeys(range(len(bridges)),1) if fees is None else fees
    assert set(fees)==set(range(len(bridges))) and all(isinstance(w,int) and w>=0 for w in fees.values())
    old=dict(c['ledger']['matching'] if baseline_matching is None else baseline_matching)
    assert len(old)==len(c['neighbours'])-c['ledger']['deficiency']
    assert len(set(old.values()))==len(old) and all(j in c['neighbours'][d] for d,j in old.items())
    before=lift(data,frame,old)
    nond={d for d in c['neighbours'] if not c['ledger']['components'][c['component'][d]]['deficient']}
    flow=receiver_flow({d:c['neighbours'][d] for d in nond},c['records'],
                       {d:j for d,j in old.items() if d in nond},fees)
    matching={d:j for d,j in old.items() if d not in nond};mode=frame;byindex={r['index']:r for r in c['records']}
    selected=set(flow['selected']);assert len({byindex[k]['tree'] for k in selected})==len(selected)
    for d in nond:
        slots={side:j for (dd,side),j in flow['slots'].items() if dd==d}
        r=next((r for r in c['records'] if r['receiver']==d),None)
        if r and r['index'] in selected:
            assert set(slots)=={'pre','post'}
            matching[d]=slots['pre'];matching[r['donor']]=slots['post']
        else:
            assert len(slots)==1;matching[d]=next(iter(slots.values()))
    for k in sorted(selected):
        r=byindex[k];T=set(c['ledger']['components'][r['tree']]['demands'])
        rooted=allocation({d:c['neighbours'][d] for d in T},T-{r['donor']})
        for d in T-{r['donor']}:matching[d]=rooted['matching'][d]
        mode=switched_skeleton(data,mode,bridges[k])
    n,_=request_data(data,mode)
    assert len(set(matching.values()))==len(matching) and all(j in n[d] for d,j in matching.items())
    after=lift(data,mode,matching)
    assert set(before['paid'])<=set(after['paid']) and before['used']<=after['used']
    assert after['value']==before['value']+len(selected)
    assert len(after['used']-before['used'])==len(selected)
    assert [k for k,e in enumerate(bridges) if e in after['links']]==sorted(selected)
    return dict(accepted=True,**after,old_value=before['value'],old_paid=before['paid'],old_used=before['used'],
        selected=sorted(selected),bridge_fee=flow['cost'],gain=len(selected),
        deficiency=c['ledger']['deficiency']-len(selected),flow=flow)


def check(data,pack,bridges,fees,counts,new_sources=frozenset(),all_baselines=False,primitive=True):
    frame=frame_with_direct_sources(data,pack,new_sources);c=recognize(data,frame,bridges);assert c['accepted']
    z=solve(data,pack,bridges,fees,new_sources)
    ref=bridge_batch(data,frame,bridges,fees)
    assert (z['value'],z['bridge_fee'])==(ref['value'],ref['bridge_fee']),(data,z,ref)
    counts['independent_mode_value_and_actual_fee_optima']+=1
    if primitive:
        E={e for p in frame['certificates'] for e in p['links']}|set(bridges)
        d=(*data[:2],sorted(E),data[3],data[4])
        assert optimize(*d)['value']==z['value']==fork_flow(*d)['value']
        legal={signature(p) for p in primitive_certificates(*d)}
        assert all(signature(p) in legal for p in z['certificates'])
        counts['independent_primitive_and_full_flow_values']+=1
    counts['paid_source_and_used_unit_set_retention']+=1
    counts['max_flow_cut_and_global_fee_potential_certificates']+=1
    counts['fee_reversing_augmentation_paths']+=sum(a['reverses_bridge_fee'] for a in z['flow']['augmentations'])
    if all_baselines:
        ds=sorted(c['neighbours']);size=len(ds)-c['ledger']['deficiency']
        def visit(i,m,used):
            if i==len(ds):
                if len(m)!=size:return
                r=solve(data,pack,bridges,fees,new_sources,m)
                assert (r['value'],r['bridge_fee'])==(z['value'],z['bridge_fee'])
                counts['all_maximum_baseline_retention']+=1
                return
            d=ds[i];visit(i+1,m,used)
            for j in c['neighbours'][d]-used:visit(i+1,m|{d:j},used|{j})
        visit(0,{},set())
    return z


def small_model(k,donor_shared=False):
    kinds,pairs,_=canonical('A'*(2*k)+'M'*k)
    old=[(2*(k+i),2*(2*k+i)) for i in range(k)]
    bridges=[(2*i,2*(2*k+i)) for i in range(k)]
    pack=dict(certificates=[stem((k+i,2*k+i),[old[i]]) for i in range(k)])
    W={o:set() for o in range(3*k)};Q=set()
    if donor_shared:
        for i in range(k-1):
            j=-1-i;W[i].add(j);W[i+1].add(j);Q.add(j)
    return (kinds,pairs,old+bridges,W,Q),pack,bridges,set(range(k))


def abstract_checks(counts):
    rng=random.Random(2026102693);samples=[]
    # A shared post-entry reserve gives exactly one joint gain; no private pair.
    data,pack,bridges,N=small_model(2);W=data[3];Q=data[4]
    for o,j in [(2,0),(3,1),(4,2),(5,2)]:W[o].add(j);Q.add(j)
    z=check(data,pack,bridges,{0:5,1:2},counts,N,all_baselines=True)
    assert (z['old_value'],z['value'],z['gain'],z['bridge_fee'],z['selected'])==(2,3,1,2,[1])
    samples.append(dict(name='two_receivers_one_shared_suffix_reserve',old=2,new=3,fee=2,bridges=[1]))
    # A cheap first bridge must be reversed to attain the maximum gain.
    data,pack,bridges,N=small_model(3);W,Q=data[3:5]
    for o,j in [(0,-1),(1,-1),(3,0),(4,1),(5,2),(6,3),(7,4),(8,3)]:W[o].add(j);Q.add(j)
    z=check(data,pack,bridges,{0:0,1:2,2:1},counts,N,all_baselines=True)
    assert z['gain']==2 and z['selected']==[1,2] and z['bridge_fee']==3
    assert any(a['reverses_bridge_fee'] for a in z['flow']['augmentations'])
    samples.append(dict(name='cheap_bridge_reversed_for_joint_optimum',old=z['old_value'],
                        new=z['value'],fee=z['bridge_fee'],bridges=z['selected']))
    # The old donor's assigned unit can be on the discarded donor suffix.
    kinds,pairs,_=canonical('AAAAMMMM')
    links=[(0,8),(9,10),(4,12),(6,14)];bridges=[(0,12),(2,14)]
    pack=dict(certificates=[stem((0,4,5),links[:2]),stem((2,6),[links[2]]),stem((3,7),[links[3]])])
    W={o:set() for o in range(8)}
    for o,j in [(5,0),(1,0),(2,1),(3,2),(6,3),(7,3)]:W[o].add(j)
    data=kinds,pairs,links+bridges,W,set(range(4))
    z=check(data,pack,bridges,{0:1,1:5},counts,{1},all_baselines=True)
    assert z['selected']==[0] and z['old_value']==3 and z['value']==4
    counts['discarded_donor_suffix_resource_retained']+=1
    # A fork can share the deficient donor tree; both old baseline choices survive.
    kinds,pairs,_=canonical('AAAAMB');bridges=[(0,8)]
    pack=dict(certificates=[stem((1,4),[(2,8)]),dict(kind='fork',owners=(2,3,5),
        links=((4,10),(6,11)),interval=0,value=2,beta=5,entries=(10,11),witness=5)])
    W={0:{0},1:{1},2:set(),3:set(),4:{2},5:{0}}
    data=kinds,pairs,[(2,8),(4,10),(6,11)]+bridges,W,{0,1,2}
    z=check(data,pack,bridges,{0:2},counts,{0},all_baselines=True)
    assert z['old_value']==3 and z['value']==4
    counts['fork_in_donor_tree_controls']+=1
    accepted=0
    for rep in range(320):
        k=2+int(rep%5==0);data,pack,bridges,N=small_model(k,donor_shared=bool(rep%3==0))
        W,Q=data[3:5]
        for j in range(rng.randint(k,2*k+3)):
            for o in rng.sample(list(range(k,3*k)),rng.randint(1,2)):
                W[o].add(j);Q.add(j)
        frame=frame_with_direct_sources(data,pack,N)
        if not recognize(data,frame,bridges)['accepted']:continue
        fees={i:rng.randint(0,6) for i in range(k)}
        z=check(data,pack,bridges,fees,counts,N,all_baselines=accepted<25,primitive=accepted<45)
        accepted+=1
    assert accepted>=100;counts['accepted_random_shared_support_models']=accepted
    return samples


def frozen_shared(copies,counts,production=False):
    from check_frozen_mixed_gate_cycle import load_model, FIXTURE
    from check_P_free_pivot_interface import regions
    from check_degree_changing_bent_completions import compile_model
    from check_canonical_band_coarsening import forests
    from check_frozen_shared_mixed_gate import check_rank_certificate
    from check_promotion_cores import frozen_certificate
    from check_residual_corridors import direct_check
    from check_uniform_zero_capacity_openings import tile_cells
    from check_private_prefix_bridge import recognize_private
    case=json.loads(Path('develop/fixtures/frozen_shared_prefix_bridge.json').read_text())
    assert case['base_fixture']==FIXTURE.name and case['pivot_capacity']==1
    R,C,T,M=load_model()[0];shift=lambda v,k:(v[0]+30*k,v[1])
    cur=(30*copies-2,24,{shift(v,k) for k in range(copies) for v in T},
         [tuple(shift(v,k) for v in e) for k in range(copies) for e in M])
    vertical={shift(tuple(tile),k) for k in range(copies) for tile in case['vertical_tiles']}
    bits={(r,c):(r,c) in vertical for r in range(0,cur[0],2) for c in range(0,24,2)}
    P={v for e in cur[3] for v in e}
    assert all(not tile_cells(t)&P and len(tile_cells(t)&cur[2])==1 for t in vertical)
    direct_check(*cur);data,_,_=compile_model(cur,regions(cur,bits));own,A,_,_=owner_data(*data[:2])
    raw=json.loads(FIXTURE.read_text());layers=[[shift(tuple(v),k) for k in range(copies) for v in layer] for layer in raw['freezing_layers']]
    assert len(check_rank_certificate(cur,layers))==308*copies
    assert frozen_certificate(cur)[0]==P
    counts['strict_freezing_events']+=308*copies
    fs=forests(cur,regions(cur,bits));bycells={cc:j for j,(cap,cc) in fs.items() if cap}
    ps=[];bridges=[];N=set();baseline={};shared=[]
    for k in range(copies):
        get=lambda r,c:own[shift((r,c),k)]
        unit=lambda r,c:bycells[frozenset({shift((r,c),k),shift((r+1,c),k)})]
        bottom=tuple(shift(tuple(v),k) for v in case['old_stems'][0]['links'][0])
        left=tuple(shift(tuple(v),k) for v in case['old_stems'][1]['links'][0])
        ps.extend([stem((get(24,17),get(24,18)),[bottom]),stem((get(24,4),get(24,5)),[left])])
        bridges.append(tuple(shift(tuple(v),k) for v in case['bridge']));N.add(get(24,19))
        j0,j1=[bycells[frozenset(shift(tuple(v),k) for v in cc)] for cc in case['baseline_original_units_cells']]
        assert data[3][get(24,18)]=={j0,j1}
        for j in (j0,j1):assert {o for o,S in data[3].items() if j in S}=={get(24,18),get(24,5)}
        baseline[2*k]=j0;baseline[2*k+1]=j1
        shared.append([j0,j1])
    pack=dict(certificates=ps);frame=frame_with_direct_sources(data,pack,N)
    assert not recognize_private(data,frame,bridges)['accepted']
    fees={k:1+k%3 for k in range(copies)}
    if production:
        with patch(__name__+'.bridge_batch',side_effect=AssertionError('No modes')), \
             patch(__name__+'.optimize',side_effect=AssertionError('No primitive optimization')), \
             patch(__name__+'.fork_flow',side_effect=AssertionError('No full flow')):
            z=solve(data,pack,bridges,fees,N,baseline)
        counts['production_shared_flow_without_modes_or_full_optimizer']+=1
    else:
        z=solve(data,pack,bridges,fees,N,baseline)
        ref=bridge_batch(data,frame,bridges,fees)
        assert (z['value'],z['bridge_fee'])==(ref['value'],ref['bridge_fee'])
        E={e for p in ps for e in p['links']}|set(bridges)
        restricted=(*data[:2],sorted(E),data[3],data[4])
        assert fork_flow(*restricted)['value']==z['value']
        counts['frozen_independent_mode_and_restricted_full_flow']+=1
        if copies==1:
            assert optimize(*restricted)['value']==z['value']
            check(data,pack,bridges,fees,counts,N,all_baselines=True)
            counts['frozen_independent_primitive_value']+=1
    assert z['value']==3*copies and z['old_value']==2*copies and z['gain']==copies
    assert z['old_used']==set(baseline.values()) and z['old_used']<=z['used']
    assert len(z['used']-z['old_used'])==copies and z['bridge_fee']==sum(fees.values())
    assert len(data[4])==155*copies-24
    counts['frozen_nonprivate_capacity_one_boards']+=1
    example={} if copies!=1 else dict(paid_source_ids=z['paid'],certificates=z['certificates'],
        used_original_units=[dict(id=j,cells=sorted(fs[j][1]),old=j in z['old_used']) for j in sorted(z['used'])])
    return dict(copies=copies,shape=list(cur[:2]),old_payment=z['old_value'],new_payment=z['value'],
        old_shared_used_units_retained=len(z['old_used']),fresh_units=copies,bridges=len(z['selected']),
        fee=z['bridge_fee'],old_private_guard_accepts=False,production=production,
        vertical_tiles=sorted(vertical)[:1],shared_suffix_original_units=shared[:1],
        cut_capacity=z['flow']['cut_capacity'],min_cost_potential_certificate=z['flow']['residual_min_cost_certificate'],
        example_certificate=example)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();samples=abstract_checks(counts)
    physical=[frozen_shared(q,counts,production=q==16) for q in (1,2,4,16)]
    report=dict(status='PASS',counts=dict(counts),samples=samples,physical=physical,
        proof='docs/SHARED_PREFIX_BRIDGE_FLOW.md',
        scope='One initialized receiver-slot min-cost flow: deficient donors, nondeficient receivers, disjoint candidate stem pairs. Arbitrary shared original supports. Exact unrestricted declared-link payment/actual bridge fees; all maximum-baseline paid sources and original used units retained.',
        limitations=['No shared-stem candidates or deficient receivers.','No universal geometric certificate or 5/6 improvement.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
