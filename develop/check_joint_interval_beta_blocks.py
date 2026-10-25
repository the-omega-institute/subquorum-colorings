"""Joint source-only intervals and exclusive empty-body beta reductions.

General proofs: JOINT_INTERVAL_BETA_BLOCK_REDUCTION.md. This verifier keeps
the complete exterior mixed/BP/body/interval capacities and original IDs.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_forced_pocket_guards_and_cycle_elimination import inspect_geometry
from check_frozen_beta_support_fork import restrict
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_joint_tree_beta_compensation import min_cost_matching
from check_residual_reserve_cost_profile import Network
from check_shared_pocket_completion import fixture as loose_fixture
from check_tight_shared_pocket import fixture as tight_fixture
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical,evaluate,optimize,ordinary_flow,whole_support_data

if not __debug__:
    raise RuntimeError('Run without -O; assertions required.')


def components(vertices,incidence):
    adj=defaultdict(set)
    for users in incidence.values():
        for a in users:adj[a]|=users-{a}
    remaining=set(vertices);answer=[]
    while remaining:
        reached={min(remaining)};todo=list(reached)
        while todo:
            for a in adj[todo.pop()]-reached:reached.add(a);todo.append(a)
        remaining-=reached;answer.append(reached)
    return answer


def validate(data,blocks):
    owner,aa,bb,_=owner_data(*data[:2]);seen=set();used=set()
    for vertices,units in blocks:
        assert vertices and vertices<=aa and not vertices&seen;seen|=vertices
        for resource,users in units.items():
            assert resource not in used and users and users<=vertices and len(users)<=2
            used.add(resource);kind,index=resource
            if kind=='i':
                assert index in data[4]
                assert {o for o,w in data[3].items() if index in w}==users
            else:
                assert kind=='b' and index in bb and not data[3][index]
                incoming=[e for e in data[2] if owner[e[1]]==index]
                assert len(incoming)==2 and len({v for u,v in incoming})==2
                assert {owner[u] for u,v in incoming}==users
        assert len(components(vertices,units))==1
    return seen,{index for kind,index in used if kind=='b'},{index for kind,index in used if kind=='i'}


def local_matching(vertices,units,excluded=frozenset(),interval_only=False):
    demands=sorted(vertices-set(excluded));renumber={a:i for i,a in enumerate(demands)}
    incidence={r:{renumber[a] for a in users if a in renumber} for r,users in units.items()
               if not interval_only or r[0]=='i'}
    matched=min_cost_matching(len(demands),incidence,lambda a,r:int(r[0]=='b'))
    return {demands[a]:r for a,r in matched.items()}


def closed_blocks(data,motifs):
    _,aa,_,_=owner_data(*data[:2]);units={('b',m['beta']):set(m['ends']) for m in motifs}
    for j in data[4]:
        users={o for o,w in data[3].items() if j in w}
        if users and users<=aa:units['i',j]=users
    return [(v,{r:u for r,u in units.items() if u&v}) for v in components(aa,units)]


def saturated_elimination(data,blocks,totals,independent=False):
    validate(data,blocks);chosen=[];local={}
    for vertices,units in blocks:
        matched=local_matching(vertices,units)
        if len(matched)==len(vertices):chosen.append((vertices,units));local.update(matched)
    grouped,betas,intervals=validate(data,chosen)
    cost=sum(r[0]=='b' for r in local.values())
    interval_rank=sum(len(local_matching(v,u,interval_only=True)) for v,u in chosen)
    assert cost==len(grouped)-interval_rank
    exact=all(data[3][a]<=intervals for a in grouped)
    owner,_,_,_=owner_data(*data[:2])
    links=[next(e for e in data[2] if owner[e[0]]==a and owner[e[1]]==r[1])
           for a,r in local.items() if r[0]=='b']
    residual=restrict(data,set(range(len(data[1])))-grouped-betas,data[4]-intervals)
    for solver in (ordinary_flow,fork_flow):
        old,new=solver(*data),solver(*residual)
        assert old['value']==len(grouped)+new['value']
        assert new['cost']<=old['cost']<=cost+new['cost']
        if exact:assert old['cost']==cost+new['cost']
        lifted=links+new['links'];assert len(set(lifted))==len(lifted)
        assert len({u for u,v in lifted})==len(lifted)==len({v for u,v in lifted})
        assert evaluate(*data[:2],lifted,*data[3:])['value']==old['value']
        totals['saturated_full_residual_comparisons']+=1
    if independent:
        for model in (data,residual):
            answer=optimize(*model);flow=fork_flow(*model)
            assert (answer['value'],answer['cost'])==(flow['value'],flow['cost'])
            totals['independent_primitive_pack_comparisons']+=1
    totals['saturated_systems']+=1;totals['nonempty_saturated_eliminations']+=bool(grouped)
    totals['exact_saturated_cost_systems']+=exact
    return dict(sources=len(grouped),units=len(betas)+len(intervals),local_cost=cost,
                exact_cost_hypothesis=exact)


def block_structure(data,blocks):
    grouped,betas,intervals=validate(data,blocks);info=[]
    for vertices,units in blocks:
        zero={r:u for r,u in units.items() if r[0]=='i'}
        clusters=components(vertices,zero)
        deficient=[c for c in clusters if len(local_matching(c,{r:u for r,u in zero.items() if u&c}))<len(c)]
        assert len(local_matching(vertices,units,interval_only=True))==len(vertices)-len(deficient)
        saturated=len(local_matching(vertices,units))==len(vertices)
        if not saturated:
            assert len(units)==len(vertices)-1 and all(len(u)==2 for u in units.values())
            assert deficient==clusters
        info.append(dict(saturated=saturated,clusters=clusters,deficient=deficient,
                         basecost=len(deficient) if saturated else len(clusters)-1))
    return grouped,betas,intervals,info


def compressed(data,trees,discounted=False,respect_clusters=True):
    grouped,local_betas,local_intervals,info=block_structure(data,trees)
    owner,alphas,betas,mixed=owner_data(*data[:2]);support=data[3]
    baseline=sum(len(v)-(not d['saturated']) for (v,u),d in zip(trees,info))
    costbase=sum(d['basecost'] for d in info)
    penalty=len(set(data[2]))+costbase+1
    graph=Network();s=('s',);t=('t',);graph.nodes|={s,t}
    exit_node=lambda o:('a',o) if o in alphas else ('out',o) if o in mixed else ('b',o)
    for a in sorted(alphas-grouped):graph.add(s,exit_node(a),1,-penalty if discounted else 0,('outside',a))
    for i,(vertices,_) in enumerate(trees):
        d=info[i];g=('group',i)
        if not d['saturated']:
            graph.add(s,g,1,-penalty if discounted else 0,('first',i))
            if discounted and len(d['clusters'])>1:
                graph.add(s,g,len(d['clusters'])-1,-1,('extra',i))
        for j,cluster in enumerate(d['deficient']):
            h=('zero',i,j)
            if d['saturated']:
                if not discounted:continue
                assert respect_clusters
                graph.add(s,h,1,-1,('sat_bonus',i,j))
            elif respect_clusters:graph.add(g,h,1,0,('cluster',i,j))
            for a in sorted(cluster):graph.add(h if respect_clusters else g,exit_node(a),1,0,('choose',i,a))
    for m in sorted(mixed):graph.add(('in',m),exit_node(m),1,0,('mixed',m))
    for b in sorted(betas-local_betas):
        for tip in data[1][b]:graph.add(('tip',tip),exit_node(b),1,0,('tip',tip))
        graph.add(exit_node(b),t,1,0,('beta',b))
    for j in sorted(data[4]-local_intervals):graph.add(('j',j),t,1,0,('interval',j))
    large=len(alphas)+1
    for u,v in sorted(set(data[2])):
        if owner[u]==owner[v] or owner[v] in local_betas:continue
        entry=('tip',v) if owner[v] in betas else ('in',owner[v])
        graph.add(exit_node(owner[u]),entry,large,1,('link',u,v))
    for o in support:
        if o in local_betas:continue
        for j in sorted(support[o]-local_intervals):graph.add(exit_node(o),('j',j),large,0,('support',o,j))
    network_cost=value=0
    while True:
        before=[e['cap'] for e in graph.edges];extra=graph.augment(s,t)
        if extra is None:break
        if discounted and extra>=0:
            for e,cap in zip(graph.edges,before):e['cap']=cap
            break
        network_cost+=extra;value+=1
    balance=Counter();actual=0;roots=defaultdict(set);outside=set();first=set();bonus=0;links=[]
    for e in graph.edges[::2]:
        amount=e['initial']-e['cap'];assert 0<=amount<=e['initial']
        balance[e['u']]+=amount;balance[e['v']]-=amount;actual+=amount*e['cost']
        if not amount:continue
        tag=e['tag']
        if tag[0]=='choose':assert amount==1;roots[tag[1]].add(tag[2])
        if tag[0]=='outside':outside.add(tag[1])
        if tag[0]=='first':first.add(tag[1])
        if tag[0] in ('extra','sat_bonus'):bonus+=amount
        if tag[0]=='link':assert amount==1;links.append(tag[1:])
    assert actual==network_cost
    assert balance[s]==value and balance[t]==-value
    assert all(v in (s,t) or z==0 for v,z in balance.items())
    score=len(outside)+len(first)
    assert first=={i for i in roots if roots[i] and not info[i]['saturated']}
    expected_bonus=sum(len(roots[i]) if info[i]['saturated'] else max(0,len(roots[i])-1)
                       for i in range(len(trees)))
    assert bonus==(expected_bonus if discounted else 0)
    assert value==score+bonus
    exterior_cost=len(links);internal_intervals=set()
    for i,(vertices,units) in enumerate(trees):
        d=info[i];occupied=sum(bool(c&roots[i]) for c in d['deficient'])
        if respect_clusters:assert occupied==len(roots[i])
        local=local_matching(vertices,units,roots[i])
        assert len(local)==len(vertices)-(len(roots[i]) if d['saturated'] else max(1,len(roots[i])))
        expected_cost=(len(d['deficient'])-occupied if d['saturated']
                       else len(d['clusters'])-max(1,occupied))
        assert sum(r[0]=='b' for r in local.values())==expected_cost
        for a,r in local.items():
            if r[0]=='i':assert r[1] not in internal_intervals;internal_intervals.add(r[1])
            else:links.append(next(e for e in data[2] if owner[e[0]]==a and owner[e[1]]==r[1]))
    claimed_cost=costbase+exterior_cost-bonus
    if respect_clusters:assert len(links)==claimed_cost
    assert len({u for u,v in links})==len(links)==len({v for u,v in links})
    assert evaluate(*data[:2],links,*data[3:])['value']==baseline+score
    assert network_cost==exterior_cost-bonus-penalty*score if discounted else network_cost==exterior_cost
    if discounted:
        back=graph.add(t,s,len(alphas),0,('return',));graph.send(back,value);graph.potentials()
    else:
        side=graph.reachable(s)
        assert sum(e['initial'] for e in graph.edges[::2] if e['u'] in side and e['v'] not in side)==score
    return dict(value=baseline+score,cost=len(links),claimed_cost=claimed_cost,baseline=baseline,
                costbase=costbase,exterior_score=score,extra_clusters=bonus,
                roots={i:sorted(a) for i,a in roots.items()})


def compare_reduction(data,trees,totals,independent=False):
    original=fork_flow(*data);one=compressed(data,trees);exact=compressed(data,trees,True)
    assert original['value']==one['value']==exact['value']
    assert original['cost']==exact['cost']<=one['cost']
    grouped,_,local_intervals=validate(data,trees)
    no_external_support=all(data[3][a]<=local_intervals for a in grouped)
    if no_external_support:assert one['cost']==original['cost']
    totals['joint_reduction_systems']+=1;totals['joint_actual_pack_lifts']+=2
    totals['simple_cost_overestimates']+=one['cost']>exact['cost']
    totals['no_external_support_equalities']+=no_external_support
    totals['nonzero_component_discount_systems']+=exact['extra_clusters']>0
    if independent:
        result=optimize(*data);assert (result['value'],result['cost'])==(exact['value'],exact['cost'])
        totals['independent_primitive_pack_comparisons']+=1
    return exact


def random_tree(rng):
    sizes=[rng.randrange(1,5) for _ in range(rng.randrange(1,4))];n=sum(sizes);p=rng.randrange(3)
    edge_specs=[];cursor=nb=nj=0
    for size in sizes:
        vertices=set(range(cursor,cursor+size));units={}
        for v in range(cursor+1,cursor+size):
            users={v,rng.randrange(cursor,v)}
            if rng.randrange(2):units['b',nb]=users;nb+=1
            else:units['i',nj]=users;nj+=1
        edge_specs.append((vertices,units));cursor+=size
    ne=rng.randrange(3);nm=rng.randrange(3)
    kinds,pairs,_=canonical('A'*(n+p)+'B'*(nb+ne)+'M'*nm)
    links=[];support={o:set() for o in range(len(pairs))};trees=[]
    for vertices,units in edge_specs:
        actual={}
        for (kind,index),users in units.items():
            index=n+p+index if kind=='b' else index;actual[kind,index]=users
            if kind=='b':
                a,b=sorted(users);links.extend([(2*a,2*index),(2*b+1,2*index+1)])
            else:
                for a in users:support[a].add(index)
        trees.append((vertices,actual))
    local_betas={b for v,u in trees for k,b in u if k=='b'}
    owner,aa,bb,mm=owner_data(kinds,pairs);resources=set(range(nj+rng.randrange(5)))
    for u in kinds:
        if kinds[u]!='TP':continue
        for v in kinds:
            if kinds[v]=='BP' and owner[v] not in local_betas and rng.random()<.12:links.append((u,v))
    for o in support:
        if o in local_betas:continue
        support[o]|={j for j in resources if j>=nj and rng.random()<.3}
    return (kinds,pairs,links,support,resources),trees


def abstract_checks(totals):
    rng=random.Random(2026102505)
    for i in range(500):
        data,trees=random_tree(rng);compare_reduction(data,trees,totals,len(data[1])<=10)
        saturated_elimination(data,trees,totals)
        if i<150:
            for vertices,units in trees:
                if len(vertices)>6:continue
                clusters=components(vertices,{r:u for r,u in units.items() if r[0]=='i'})
                for mask in range(1<<len(vertices)):
                    roots={a for k,a in enumerate(sorted(vertices)) if mask>>k&1}
                    matched=local_matching(vertices,units,roots)
                    z=sum(bool(c&roots) for c in clusters)
                    assert len(matched)==len(vertices)-max(1,len(roots))
                    assert sum(r[0]=='b' for r in matched.values())==len(clusters)-max(1,z)
                    totals['arbitrary_local_root_sets']+=1
        # Give each selected tree one source-only private anchor interval.
        if i<200:
            kinds,pairs,links,support,resources=data;support={a:set(w) for a,w in support.items()}
            anchored=[];resources=set(resources)
            for vertices,units in trees:
                j=max(resources,default=-1)+1;resources.add(j);a=min(vertices);support[a].add(j)
                anchored.append((vertices,{**units,('i',j):{a}}))
            anchored_data=(kinds,pairs,links,support,resources)
            saturated_elimination(anchored_data,anchored,totals,len(pairs)<=10)
            compare_reduction(anchored_data,anchored,totals,len(pairs)<=10)
            for (vertices,units),d in zip(anchored,block_structure(anchored_data,anchored)[3]):
                for mask in range(1<<len(vertices)):
                    roots={a for k,a in enumerate(sorted(vertices)) if mask>>k&1}
                    matched=local_matching(vertices,units,roots)
                    z=sum(bool(c&roots) for c in d['deficient'])
                    assert len(matched)==len(vertices)-len(roots)
                    assert sum(r[0]=='b' for r in matched.values())==len(d['deficient'])-z
                    totals['saturated_arbitrary_root_sets']+=1
    # Wrong discount: two exterior roots lie in ONE interval component.
    kinds,pairs,_=canonical('AAABMM')
    data=(kinds,pairs,[(2,6),(5,7)],{0:{0,1},1:{0,2},2:set(),3:set(),4:{1},5:{2}},{0,1,2})
    trees=[({0,1,2},{('i',0):{0,1},('b',3):{1,2}})]
    correct=compare_reduction(data,trees,totals,True);wrong=compressed(data,trees,True,False)
    assert (correct['value'],correct['cost'])==(3,1)
    assert wrong['claimed_cost']==0 and wrong['cost']==1
    return dict(same_interval_component_discount=dict(correct=correct,invalid_flattened=wrong,
        status='Refutes counting alpha exits as independent beta savings; abstract control, not a frozen realization.'))


def local_multigraph_checks(totals):
    # Includes beta loops, parallel resources, interval anchors and cycles.
    for n in range(1,4):
        vertices=set(range(n))
        incidences=[set(c) for size in (1,2) for c in itertools.combinations(range(n),size)]
        types=[(kind,u) for kind in ('i','b') for u in incidences]
        for m in range(n+2):
            for choices in itertools.combinations_with_replacement(range(len(types)),m):
                units={(types[k][0],j):types[k][1] for j,k in enumerate(choices)}
                if len(components(vertices,units))!=1:continue
                saturated=len(local_matching(vertices,units))==n
                zero={r:u for r,u in units.items() if r[0]=='i'}
                clusters=components(vertices,zero)
                deficient=[c for c in clusters if len(local_matching(c,{r:u for r,u in zero.items() if u&c}))<len(c)]
                for mask in range(1<<n):
                    roots={a for a in vertices if mask>>a&1}
                    matched=local_matching(vertices,units,roots)
                    z=sum(bool(c&roots) for c in deficient)
                    assert len(matched)==n-(len(roots) if saturated else max(1,len(roots)))
                    assert sum(r[0]=='b' for r in matched.values())==len(deficient)-(z if saturated else max(1,z))
                    totals['exhaustive_local_multigraph_root_sets']+=1
                totals['exhaustive_local_multigraphs']+=1


def physical_checks(totals):
    records=[]
    for name,fixture in [('tight',tight_fixture),('outside',loose_fixture)]:
        for q in range(1,9):
            masks=range(1<<q) if q<=3 else [0]+[(1<<n)-1 for n in range(1,q+1)]
            for mask in masks:
                filled={i for i in range(q) if mask>>i&1};current,_=fixture(q,filled)
                data,motifs=inspect_geometry(current,whole_bands(current),totals)
                blocks=closed_blocks(data,motifs)
                result=saturated_elimination(data,blocks,totals,q<=2)
                compare_reduction(data,blocks,totals,q<=2)
                records.append(dict(family=name,copies=q,filled=sorted(filled),**result))
    # Frozen necessary-hypothesis control: internal I+beta cycle has cost1,
    # but the omitted second original interval permits full cost0.
    current,_=tight_fixture(1,set());data,motifs=inspect_geometry(current,whole_bands(current),totals)
    blocks=closed_blocks(data,motifs);vertices,units=blocks[0]
    interval=next(r for r in units if r[0]=='i');beta=next(r for r in units if r[0]=='b')
    reduced=[(vertices,{interval:units[interval],beta:units[beta]})]
    control=saturated_elimination(data,reduced,totals,True)
    assert control['local_cost']==1 and not control['exact_cost_hypothesis']
    assert fork_flow(*data)['cost']==0
    unified=compare_reduction(data,reduced,totals,True)
    assert unified['cost']==0 and unified['extra_clusters']==1
    return records,dict(local_cost=1,full_cost=0,exact_cost_hypothesis=False,
        status='Actual frozen board refutes dropping no-exterior-direct-support cost condition.')


def physical_reservations(totals):
    records=[]
    for q in range(1,5):
        current,_=tight_fixture(q,set());data,motifs=inspect_geometry(current,whole_bands(current),totals)
        _,meta,_=whole_support_data(current,whole_bands(current))
        by_coordinate={(v['band'],v['first'],v['last']):j for j,v in enumerate(meta['intervals'])}
        for counts in itertools.product(range(3),repeat=q):
            reserved={by_coordinate[4+8*i,c,c] for i,n in enumerate(counts) for c in (5,6)[:n]}
            reduced=restrict(data,set(range(len(data[1]))),data[4]-reserved)
            blocks=closed_blocks(reduced,motifs)
            saturated_elimination(reduced,blocks,totals,q<=2)
            result=compare_reduction(reduced,blocks,totals,q<=2)
            totals['physical_interval_reservation_models']+=1
            if q==1:records.append(dict(reserved=counts[0],**result))
    return records


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();controls=abstract_checks(totals)
    local_multigraph_checks(totals)
    physical,cost_control=physical_checks(totals);reservations=physical_reservations(totals)
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),controls=controls,
        physical=physical,frozen_cost_control=cost_control,physical_reservations=reservations,
        scope='Closed source-only interval and exclusive empty-body beta blocks have an exact joint reduction in the full exterior network; optional discounts retain one capacity per deficient interval component in saturated blocks and per interval component in trees. General proofs written, finite controls not a universal geometric compensation proof;5/6 open.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
