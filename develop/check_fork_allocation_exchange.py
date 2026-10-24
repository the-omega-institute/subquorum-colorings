"""Solver-free controls for fork/ordinary allocation exchange and closed trees.

General arguments: FORK_ALLOCATION_EXCHANGE_AND_CLOSED_TREES.md.
Generated counterexamples are abstract. Physical lifts retain their own scope.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_one_sided_interval_allocation import independent_maximum
from check_whole_support_fork_normal_form import (
    optimize,ordinary_flow,primitive_certificates,evaluate,canonical,whole_support_data,
)
from check_frozen_beta_support_fork import fixture,stacked,A,C,B,FORK
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_even_bridge_support_completion import endpoints_of
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def restrict_owners(data,allowed,links):
    kinds,pairs,_,support,resources=data
    kept=[(o,pair) for o,pair in enumerate(pairs) if o in allowed]
    free={v for o,pair in kept for v in pair}
    return ({v:kinds[v] for v in free},[pair for o,pair in kept],
            [e for e in links if set(e)<=free],
            {i:support[o] for i,(o,pair) in enumerate(kept)},resources)


def matching_with_baseline(access,initial):
    right={j:p for p,j in initial.items()}
    assert len(right)==len(initial)
    def augment(p,seen):
        for j in sorted(access[p]):
            if j in seen:continue
            seen.add(j);previous=right.get(j)
            if previous is None or augment(previous,seen):
                right[j]=p;return True
        return False
    for p in access:
        if p not in right.values():augment(p,set())
    matched={p:j for j,p in right.items()}
    assert len(matched)==len(right)
    assert set(initial)<=set(matched) and set(initial.values())<=set(right)
    assert all(j in access[p] for p,j in matched.items())
    inc={j:{p for p,ns in access.items() if j in ns}
         for j in set().union(set(),*access.values())}
    order={p:i for i,p in enumerate(access)}
    assert len(matched)==independent_maximum(len(access),
        {j:{order[p] for p in users} for j,users in inc.items()})
    return matched


def reachable(start,edges):
    seen=set();pending=list(edges[start])
    while pending:
        p=pending.pop()
        if p not in seen:seen.add(p);pending+=list(edges[p]-seen)
    return seen


def closure_trees(data,certs,access,forks,totals):
    used={p['interval']:i for i,p in enumerate(certs) if p['interval'] is not None}
    graph={p:{used[j] for j in ns if j in used and used[j]!=p} for p,ns in access.items()}
    free={p:ns-set(used) for p,ns in access.items()}
    for f in forks:
        rs=reachable(f,graph)
        assert f not in rs and not free[f]
        assert not any(free[p] for p in rs)
    if not all(sum(j in w for w in data[3].values())<=2 for j in data[4]):return
    incoming=Counter(q for ns in graph.values() for q in ns)
    assert all(n<=1 for n in incoming.values())
    totals['two_owner_dependency_graphs']+=1
    terminal=[f for f in forks if not (reachable(f,graph)&forks)]
    if forks:assert terminal
    # Each terminal fork plus its disjoint closed ordinary closure has one
    # Hall deficit. Match all other forks along first-next-fork paths.
    initial={p:certs[p]['interval'] for p in access if p not in forks}
    exchanged=dict(initial);path_interiors=set();path_targets=set()
    for f in sorted(forks-set(terminal)):
        pending=[(f,[f])];path=None
        while pending and path is None:
            p,route=pending.pop()
            for q in graph[p]:
                if q in forks:
                    path=route+[q];break
                pending.append((q,route+[q]))
        assert path is not None
        interior=set(path[1:-1]);target=path[-1]
        assert not interior&path_interiors and target not in path_targets
        path_interiors|=interior;path_targets.add(target)
        for p,q in zip(path,path[1:]):exchanged[p]=certs[q]['interval']
    assert set(exchanged)==set(access)-set(terminal)
    assert len(set(exchanged.values()))==len(exchanged)
    assert set(initial.values())<=set(exchanged.values())
    assert all(j in access[p] for p,j in exchanged.items())
    maximum=matching_with_baseline(access,initial)
    assert len(access)-len(maximum)==len(terminal)
    assert len(exchanged)==len(maximum)
    totals['exact_terminal_fork_defects']+=1
    totals['terminal_fork_deficit_units']+=len(terminal)
    totals['first_next_fork_exchange_paths']+=len(forks)-len(terminal)
    accounted=set()
    for f in terminal:
        closed=reachable(f,graph)
        assert not closed&forks
        assert not closed&accounted
        accounted|=closed
        assert set().union(set(),*(access[p] for p in closed))=={certs[p]['interval'] for p in closed}
        adjacency={p:set() for p in closed}
        inc={j:{p for p in closed if j in access[p]} for j in {certs[p]['interval'] for p in closed}}
        for users in inc.values():
            if len(users)==2:
                a,b=users;adjacency[a].add(b);adjacency[b].add(a)
        todo=set(closed);anchors=[]
        while todo:
            root=min(todo);comp={root};pending=[root]
            while pending:
                p=pending.pop()
                for q in adjacency[p]-comp:comp.add(q);pending.append(q)
            todo-=comp
            units={j for j,users in inc.items() if users&comp}
            private={j for j in units if len(inc[j])==1}
            entry=access[f]&units
            assert len(units)==len(comp)
            assert len(private)==len(entry)==1 and private==entry
            assert sum(len(inc[j])==2 for j in units)==len(comp)-1
            anchors+=list(entry)
            totals['closed_ordinary_trees']+=1
            totals['closed_ordinary_tree_vertices']+=len(comp)
            totals['nonsingleton_closed_ordinary_trees']+=len(comp)>1
        assert set(anchors)==access[f] and len(anchors)==len(set(anchors))
        totals['terminal_forks_with_ordinary_closure']+=bool(closed)
        totals['empty_arm_terminal_forks']+=not access[f]


def check_pack(data,pack,totals,minimum_cost=False):
    certs=pack['certificates'];forks={i for i,p in enumerate(certs) if p['kind']=='fork'}
    intervals={i for i,p in enumerate(certs) if p['kind']=='interval'}
    betas={i for i,p in enumerate(certs) if p['kind']=='beta'}
    access={i:set().union(*(data[3][o] for o in p['owners'] if p['kind']!='fork' or o!=p['beta']))
            for i,p in enumerate(certs) if i not in betas}
    initial={i:certs[i]['interval'] for i in intervals}
    u=set(initial.values());matched=matching_with_baseline(access,initial)
    h,m,t=len(forks),len(intervals),len(betas);mu=len(matched)
    delta=h+m-mu
    fixed_mu=independent_maximum(h,{j:{a for a,f in enumerate(sorted(forks)) if j in access[f]-u}
        for j in set().union(set(),*(access[f]-u for f in forks))})
    assert 0<=delta<=h-fixed_mu
    selected_links=[e for p in certs for e in p['links']]
    allowed=set().union(set(),*(set(p['owners']) for p in certs))
    restricted=restrict_owners(data,allowed,selected_links)
    ordinary=ordinary_flow(*restricted)
    assert ordinary['value']==t+h+mu
    # Build actual ordinary primitives realizing the baseline-preserving
    # matching. Witnesses may move to earlier prefixes, reducing link count.
    candidates=primitive_certificates(*data[:2],selected_links,*data[3:])
    _,alphas,_,_=owner_data(*data[:2]);chosen=[]
    for i,p in enumerate(certs):
        if i in betas:chosen.append(p);continue
        if i in intervals:
            stems=[s for s in candidates if s['kind']=='interval'
                   and s['interval']==matched[i] and set(s['owners'])<=set(p['owners'])]
            chosen.append(min(stems,key=lambda s:len(s['links'])))
        elif i in matched:
            options=[]
            for a in candidates:
                if a['kind']!='interval' or a['interval']!=matched[i] or not set(a['owners'])<=set(p['owners']):continue
                for b in candidates:
                    if b['kind']=='beta' and b['beta']==p['beta'] and set(b['owners'])<=set(p['owners']) and not set(a['owners'])&set(b['owners']):
                        options.append((a,b))
            a,b=min(options,key=lambda pair:len(pair[0]['links'])+len(pair[1]['links']))
            chosen.extend([a,b])
        else:
            stems=[s for s in candidates if s['kind']=='beta' and s['beta']==p['beta'] and set(s['owners'])<=set(p['owners'])]
            chosen.append(min(stems,key=lambda s:len(s['links'])))
    actual=[e for p in chosen for e in p['links']]
    owners=[o for p in chosen for o in p['owners']]
    js=[p['interval'] for p in chosen if p['interval'] is not None]
    assert len(owners)==len(set(owners)) and len(js)==len(set(js))
    assert u<=set(js) and len(js)==mu
    old_paid=set().union(set(),*(set(certs[i]['owners'])&alphas for i in intervals|betas))
    new_paid=set().union(set(),*(set(p['owners'])&alphas for p in chosen))
    assert old_paid<=new_paid
    assert set(actual)<=set(selected_links) and len(actual)<=len(selected_links)-h
    replay=restrict_owners(data,allowed,actual)
    assert evaluate(*replay)['value']==t+h+mu
    fullordinary=ordinary_flow(*data)
    assert pack['value']-fullordinary['value']<=delta
    if minimum_cost:
        assert not forks or delta>0
        closure_trees(data,certs,access,forks,totals)
    totals['pack_exchanges']+=1
    totals['strict_improvements_over_fixed_assignment_bound']+=delta<h-fixed_mu
    totals['old_interval_identities_preserved']+=len(u)
    totals['old_paid_sources_preserved']+=len(old_paid)
    totals['actual_subset_links_removed']+=len(selected_links)-len(actual)
    totals['partial_replacements']+=0<mu-m<h
    return dict(forks=h,ordinary_interval_stems=m,joint_matching=mu,
                fixed_assignment_defect=h-fixed_mu,joint_defect=delta,
                ordinary_route_value=t+h+mu,constructed_links=len(actual))


def ordinary_forest(n,parents,repair=False,mixed=False):
    types='AAB'+('AM' if mixed else 'A')*n
    kinds,pairs,_=canonical(types);support={o:set() for o in range(len(pairs))}
    links=[(0,4),(2,5)];support[2]={n};route=[]
    for i in range(n):
        a=3+(2 if mixed else 1)*i;w=a+1 if mixed else a;route.append((a,w))
        if mixed:links.append((pairs[a][0],pairs[w][0]))
        support[w].add(i)
        if parents[i] is None:support[0].add(i)
        else:support[route[parents[i]][1]].add(i)
    resources=set(range(n+1))
    if repair:support[route[-1][1]].add(n+1);resources.add(n+1)
    data=(kinds,pairs,links,support,resources)
    candidates=primitive_certificates(*data);certs=[]
    certs.append(next(p for p in candidates if p['kind']=='fork' and p['interval']==n))
    for i,(a,w) in enumerate(route):
        certs.append(next(p for p in candidates if p['kind']=='interval' and p['interval']==i and a in p['owners'] and set(p['owners'])<={a,w}))
    return data,dict(value=n+2,cost=sum(len(p['links']) for p in certs),certificates=certs)


def alternating_chain(q,totals):
    kinds,pairs,_=canonical('AAB'*q+'A'*q)
    support={o:set() for o in range(len(pairs))};links=[]
    for i in range(q):
        links.extend([(6*i,6*i+4),(6*i+2,6*i+5)])
        support[3*i+2]={i};support[3*i]={q+i};support[3*q+i]={q+i}
        if i<q-1:support[3*q+i].add(i+1)
    data=(kinds,pairs,links,support,set(range(2*q)))
    candidates=primitive_certificates(*data);certs=[]
    for i in range(q):
        certs.append(next(p for p in candidates if p['kind']=='fork' and p['beta']==3*i+2))
        certs.append(next(p for p in candidates if p['kind']=='interval' and p['owners']==(3*q+i,) and p['interval']==q+i))
    pack=dict(value=3*q,cost=2*q,certificates=certs)
    result=check_pack(data,pack,totals,minimum_cost=True)
    assert result['fixed_assignment_defect']==q and result['joint_defect']==1
    ordinary=ordinary_flow(*data)
    assert (ordinary['value'],ordinary['cost'])==(3*q-1,q)
    if q<=5:
        exact=optimize(*data)
        assert (exact['value'],exact['cost'])==(3*q,2*q)
        totals['independent_alternating_chain_optima']+=1
    totals['alternating_blocking_chains']+=1
    return dict(copies=q,full_value=3*q,full_min_links=2*q,
                ordinary_value=3*q-1,ordinary_min_links=q,**result)


def dependency_forest(n,shape,phase,totals):
    """Arbitrary abstract certificate trees, including branching fork DAGs.

    Every certificate keeps its own assigned resource. A parent's pre-beta
    or ordinary support additionally sees its child's resource. Resources
    have at most two original owners; only direct fork-entry links exist.
    Leaves force full-payment forks to remain forks, inductively proving
    that this all-source packing is also minimum-link.
    """
    forks={i for i in range(n) if (i+phase)%3!=1}
    types=''.join('AAB' if i in forks else 'A' for i in range(n))
    kinds,pairs,_=canonical(types);support={o:set() for o in range(len(pairs))}
    starts=[];holders=[];links=[];offset=0
    for i in range(n):
        starts.append(offset);holders.append(offset+2 if i in forks else offset)
        support[holders[-1]].add(i)
        if i in forks:
            links.extend([(pairs[offset][0],pairs[offset+2][0]),
                          (pairs[offset+1][0],pairs[offset+2][1])])
        offset+=3 if i in forks else 1
    for i in range(1,n):
        parent=(i-1 if shape=='path' else 0 if shape=='star' else
                (i-1)//2 if shape=='binary' else None if i%3==0 else i-1)
        if parent is not None:support[starts[parent]].add(i)
    data=(kinds,pairs,links,support,set(range(n)))
    candidates=primitive_certificates(*data);certs=[]
    for i in range(n):
        certs.append(next(p for p in candidates if p['interval']==i
            and (p['kind']=='fork' and p['beta']==holders[i] if i in forks
                 else p['kind']=='interval' and p['owners']==(starts[i],))))
    pack=dict(value=n+len(forks),cost=2*len(forks),certificates=certs)
    result=check_pack(data,pack,totals,minimum_cost=True)
    totals['branching_dependency_forest_controls']+=1
    return dict(vertices=n,shape=shape,phase=phase,**result)


def physical(q,padding,totals):
    current=stacked(q)
    if padding:current=(current[0],current[1]+2,current[2],current[3])
    direct_check(*current);assert frozen_certificate(current)[0]==endpoints_of(current)
    data,meta,_=whole_support_data(current,whole_bands(current));candidates=primitive_certificates(*data)
    certs=[]
    for i in range(q):
        move=lambda v:(v[0]+16*i,v[1]);fork_links={tuple(map(move,e)) for e in FORK}
        j=meta['owner'][4+8*i,7]
        certs.append(next(p for p in candidates if p['kind']=='fork' and p['interval']==j and set(p['links'])==fork_links))
        if padding:
            d=move((7,12));owner=owner_data(*data[:2])[0][d]
            certs.append(next(p for p in candidates if p['kind']=='interval' and p['owners']==(owner,) and not p['links']))
        else:
            edge=(move((7,12)),move((7,11)))
            certs.append(next(p for p in candidates if p['kind']=='beta' and p['links']==(edge,)))
    pack=dict(value=3*q,cost=sum(len(p['links']) for p in certs),certificates=certs)
    result=check_pack(data,pack,totals)
    assert result['joint_defect']==0
    totals['physical_pack_lifts']+=1
    return dict(copies=q,positive_right_padding=padding,**result)


def shielding_control(totals):
    current,_=fixture();data,meta,_=whole_support_data(current,whole_bands(current))
    # No selected-only extension can occupy any of these four cells while
    # retaining the old T/M: two new selections directly have two old P
    # neighbors; the others touch an already saturated old selected guard.
    mate={a:b for e in current[3] for a,b in (e,e[::-1])}
    assert {(12,2),(11,3)}<=set(mate) and {(12,5),(11,4)}<=set(mate)
    assert {(13,2),(13,5)}<=current[2]
    assert {(12,2),(12,5)}<=set(mate)
    occupied=current[2]|set(mate)
    adjacent=lambda v,w:abs(v[0]-w[0])+abs(v[1]-w[1])==1
    for v,neighbors in [((12,3),[(12,2),(11,3)]),((12,4),[(12,5),(11,4)])]:
        assert len(set(neighbors))==2 and all(w in occupied and adjacent(v,w) for w in neighbors)
    for guard,old_neighbor,new in [((13,2),(12,2),(13,3)),((13,5),(12,5),(13,4))]:
        assert guard in current[2] and old_neighbor in occupied
        assert adjacent(guard,old_neighbor) and adjacent(guard,new) and old_neighbor!=new
    wider=(*current[:3],current[3]+[((12,3),(12,4))])
    direct_check(*wider);assert frozen_certificate(wider)[0]==endpoints_of(wider)
    changed,_,_=whole_support_data(wider,whole_bands(wider))
    old=ordinary_flow(*data);new=ordinary_flow(*changed)
    owners,_,betas,_=owner_data(*changed[:2])
    c=owners[(12,2)];b=owners[(12,3)]
    assert b in betas and not changed[3][c]
    assert ((12,2),(12,3)) in changed[2] and ((12,5),(12,4)) in changed[2]
    assert (old['value'],old['cost'],new['value'],new['cost'])==(3,1,3,2)
    assert len(changed[4])==41 and len(betas)==3
    totals['frozen_horizontal_insertion_controls']+=1
    return dict(added_matching_edge=[[12,3],[12,4]],endpoints=68,
                available_intervals=41,beta=3,full_ordinary_value=3,min_links=2,
                selected_only_shielding='Impossible_by_four_local_feasibility_witnesses',
                scope='Fixed_original_T_and_M_selected_only_extension; insertion_adds_new_beta_credit_NOTstrict_fork_gain')


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();families=[]
    for n in range(1,9):
        for shape in ('path','star','binary','forest'):
            parents=[None]+[(i-1 if shape=='path' else 0 if shape=='star' else (i-1)//2 if shape=='binary' else None if i%3==0 else i-1) for i in range(1,n)]
            for mixed,repair in itertools.product((False,True),repeat=2):
                data,pack=ordinary_forest(n,parents,repair,mixed)
                result=check_pack(data,pack,totals,minimum_cost=not repair)
                assert result['fixed_assignment_defect']==1
                assert result['joint_defect']==(0 if repair else 1)
                optimum=optimize(*data)
                assert optimum['value']==n+2
                if not repair:assert optimum['cost']==pack['cost']
                families.append(dict(vertices=n,shape=shape,mixed_routes=mixed,free_repair=repair,**result))
    rng=random.Random(20261027)
    for _ in range(500):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,5)))
        kinds,pairs,possible=canonical(types);rng.shuffle(possible);links=possible[:rng.randrange(min(12,len(possible))+1)]
        resources=set(range(rng.randrange(1,6)));support={o:set() for o in range(len(pairs))}
        for j in resources:
            for o in rng.sample(range(len(pairs)),rng.randrange(min(2,len(pairs))+1)):support[o].add(j)
        data=(kinds,pairs,links,support,resources)
        check_pack(data,optimize(*data),totals,minimum_cost=True)
    dependency_forests=[dependency_forest(n,shape,phase,totals)
        for n in range(1,9) for shape in ('path','star','binary','forest')
        for phase in (0,1)]
    chains=[alternating_chain(q,totals) for q in range(1,11)]
    lifts=[physical(q,padding,totals) for q in range(1,7) for padding in (False,True)]
    shielding=shielding_control(totals)
    result=dict(status='PASS',totals=dict(totals),abstract_forest_families=families,
        physical_lifts=lifts,alternating_chains=chains,shielding_control=shielding,
        dependency_forests=dependency_forests,
        scope='Exact route-restricted joint matching and original allocation exchange checked '
              'by independent ordinary flow and actual subset-link replay. Closed ordinary '
              'trees, private anchors and exact terminal-fork defect use two-owner supports '
              'and minimum-link maximal packs. '
              'Frozen physical lifts have no unrestricted strict gain; abstract blocking trees '
              'not claimed physical. General proofs written; finite controls do not replace them.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
