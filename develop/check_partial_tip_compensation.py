"""Lift partial two-slot assignments; keep original resource identities.

General proofs are in PARTIAL_TIP_COMPENSATION_AND_SAFE_PRUNING.md.
Finite controls test the lift, the component rounding and safe graph pruning.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_tip_slot_obstruction import fixture, matching, slot_graph
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import canonical, ordinary_flow, whole_support_data
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def components(vertices,edges):
    adjacency={v:set() for v in vertices}
    for v,w in edges:
        adjacency[v].add(w);adjacency[w].add(v)
    unseen=set(vertices);answer=[]
    while unseen:
        start=min(unseen,key=repr);seen={start};pending=[start]
        while pending:
            v=pending.pop()
            for w in adjacency[v]-seen:seen.add(w);pending.append(w)
        unseen-=seen;answer.append(seen)
    return answer


def interaction_components(data):
    kinds,pairs,links,support,resources=data
    owner,_,_,_=owner_data(kinds,pairs)
    vertices={('o',o) for o in support}|{('i',j) for j in resources}
    edges=[(('o',owner[v]),('o',owner[w])) for v,w in links]
    edges += [(('o',o),('i',j)) for o,units in support.items() for j in units]
    return components(vertices,edges)


def lift(data,assignment):
    kinds,pairs,links,support,resources=data
    owner,alphas,betas,_=owner_data(kinds,pairs)
    graph=slot_graph(data)
    assert len(set(assignment.values()))==len(assignment)
    assert all(target in graph[v] for target,v in assignment.items())
    selected=[(v,target[1]) for target,v in assignment.items() if target[0]=='bp']
    reduced,inventory,records=cancel_pairs(kinds,pairs,selected,Counter())
    final_alphas=[c for c in records if not c['cycle'] and c['alpha']==c['beta']+1]
    target_of={v:t for t,v in assignment.items()}
    holes={v for v in graph if v not in target_of}
    incidence={i:{target_of[v][1] for v in c['ends'] if v in target_of}
               for i,c in enumerate(final_alphas)}
    assert all(target_of[v][0]=='interval' for c in final_alphas for v in c['ends'] if v in target_of)
    # One original resource node, even when different final alphas name it.
    parts=components({('a',i) for i in incidence}|
                     {('i',j) for js in incidence.values() for j in js},
                     [(('a',i),('i',j)) for i,js in incidence.items() for j in js])
    fine_budget=0;part_records=[]
    for part in parts:
        aa={v[1] for v in part if v[0]=='a'}
        jj={v[1] for v in part if v[0]=='i'}
        h=sum(len(set(final_alphas[i]['ends'])&holes) for i in aa)
        achieved=len(matching({i:{('i',j) for j in incidence[i]} for i in aa}))
        deficit=len(aa)-achieved
        assert deficit<=h//2
        fine_budget+=h//2
        part_records.append(dict(alphas=len(aa),intervals=len(jj),holes=h,deficit=deficit,budget=h//2))
    allocated=matching({i:{('i',j) for j in js} for i,js in incidence.items()})
    assert len({t[1] for t in allocated})==len(allocated)
    # Every payment has its actual assigned free-tip owner witness.
    for target,i in allocated.items():
        assert any(v in target_of and target_of[v][1]==target[1] and
                   target[1] in support[owner[v]] for v in final_alphas[i]['ends'])
    payment=len(betas)-inventory['BP','BP']+len(allocated)
    deficit=len(alphas)-payment
    assert 0<=deficit<=fine_budget
    coarse=0;interaction_records=[]
    for part in interaction_components(data):
        oo={v[1] for v in part if v[0]=='o'}
        a=len(oo&alphas)
        h=sum(owner[v] in oo for v in holes)
        bound=min(a,h//2)
        coarse+=bound
        interaction_records.append(dict(alpha=a,holes=h,budget=bound))
    assert fine_budget<=coarse<=min(len(alphas),len(holes)//2)
    restricted=(kinds,pairs,selected,support,resources)
    ordinary=ordinary_flow(*restricted)
    assert ordinary['value']>=payment and ordinary['cost']<=len(selected)
    return dict(alpha=len(alphas),holes=len(holes),selected_links=len(selected),
                certified_payment=payment,certified_deficit=deficit,
                final_alpha_holes=sum(len(set(c['ends'])&holes) for c in final_alphas),
                final_component_budget=fine_budget,interaction_budget=coarse,
                global_budget=len(holes)//2,parts=part_records,interactions=interaction_records)


def restrict_owners(data,keep):
    kinds,pairs,links,support,resources=data
    owner,_,_,_=owner_data(kinds,pairs)
    new=[pair for o,pair in enumerate(pairs) if o in keep]
    points={v for pair in new for v in pair}
    return ({v:kinds[v] for v in points},new,[e for e in links if set(e)<=points],
            {i:set(support[owner[p[0]]]) for i,p in enumerate(new)},set(resources))


def live_prune(data):
    """Delete mixed owners off every ordinary alpha-to-resource route.

    Original alpha and beta owners and every original interval identity stay.
    This is graph pruning, not removal of any physical grid endpoint.
    """
    kinds,pairs,links,support,resources=data
    owner,alphas,betas,mixed=owner_data(kinds,pairs)
    forward=defaultdict(set);reverse=defaultdict(set)
    for v,w in links:
        a,b=owner[v],owner[w]
        if a!=b:forward[a].add(b);reverse[b].add(a)
    def closure(starts,adj):
        seen=set(starts);pending=list(starts)
        while pending:
            v=pending.pop()
            for w in adj[v]-seen:seen.add(w);pending.append(w)
        return seen
    reached=closure(alphas,forward)
    productive=closure(betas|{o for o in alphas|mixed if support[o]&resources},reverse)
    live=mixed&reached&productive
    reduced=restrict_owners(data,alphas|betas|live)
    return reduced,dict(removed_mixed=sorted(mixed-live),live_mixed=sorted(live))


def check(data,totals,exhaust_partial=False):
    graph=slot_graph(data);assigned=matching(graph)
    result=lift(data,assigned)
    ordinary=ordinary_flow(*data)
    assert ordinary['deficit']<=result['interaction_budget']
    totals['systems']+=1
    totals['partial_lifts']+=1
    totals['strict_component_rounding']+=result['interaction_budget']<result['global_budget']
    totals['strict_final_component_budget']+=result['final_component_budget']<result['interaction_budget']
    totals['complete_without_full_tip_cover']+=bool(result['holes']) and result['interaction_budget']==0
    totals['nonempty_alpha_complete_without_full_tip_cover']+=(result['alpha']>0 and
        bool(result['holes']) and result['interaction_budget']==0)
    totals['sharp_positive_budgets']+=ordinary['deficit']==result['interaction_budget']>0
    # Arbitrary partial certificates, not just maximum tip matchings.
    keys=list(assigned)
    masks=range(1<<len(keys)) if exhaust_partial else (0,(1<<len(keys))-1)
    for mask in masks:
        partial={t:assigned[t] for i,t in enumerate(keys) if mask>>i&1}
        lift(data,partial);totals['partial_lifts']+=1
    pruned,meta=live_prune(data)
    old,new=ordinary_flow(*data),ordinary_flow(*pruned)
    assert (old['value'],old['cost'])==(new['value'],new['cost'])
    # A beta-body-only fork does not need a mixed owner rejected by ordinary
    # productivity: every beta is already an ordinary private target.
    old,new=fork_flow(*data),fork_flow(*pruned)
    assert (old['value'],old['cost'])==(new['value'],new['cost'])
    assert old['deficit']==new['deficit']
    totals['pruning_comparisons']+=2
    totals['nontrivial_prunings']+=bool(meta['removed_mixed'])
    return result


def abstract(totals):
    families=[('A',),('M',),('A','M'),('A','B'),('A','A'),('A','M','M'),
              ('A','B','M'),('A','A','M'),('A','A','B'),('A','B','M','M'),
              ('A','A','B','M'),('A','A','B','B','M')]
    rng=random.Random(260925)
    for types in families:
        for trial in range(100):
            kinds,pairs,possible=canonical(types)
            links=[e for e in possible if rng.randrange(3)]
            resources=set(range(rng.randrange(4)))
            support={o:{j for j in resources if rng.randrange(2)} for o in range(len(pairs))}
            data=(kinds,pairs,links,support,resources)
            check(data,totals,trial<6)
            owner,aa,bb,mm=owner_data(kinds,pairs)
            # Preserve a specified paid-source candidate subset and arbitrary
            # deletions of interval identities before recomputing liveness.
            if trial<8:
                for rmask in range(1<<len(resources)):
                    available={j for j in resources if rmask>>j&1}
                    for mask in range(1<<len(aa)):
                        chosen={a for i,a in enumerate(sorted(aa)) if mask>>i&1}
                        restricted=restrict_owners(data,chosen|bb|mm)
                        k,p,l,s,_=restricted
                        restricted=(k,p,l,{o:w&available for o,w in s.items()},available)
                        pruned,_=live_prune(restricted)
                        for solver in (ordinary_flow,fork_flow):
                            old,new=solver(*restricted),solver(*pruned)
                            assert (old['value'],old['cost'])==(new['value'],new['cost'])
                            totals['fixed_source_resource_pruning_comparisons']+=1
                            totals['nonempty_source_pruning_comparisons']+=bool(chosen)
    # Sharp loss, with at most two original owners per resource.
    for q in range(1,21):
        kinds,pairs,_=canonical(('A',)*(2*q))
        support={i:{i//2} for i in range(2*q)}
        data=kinds,pairs,[],support,set(range(q))
        result=check(data,totals)
        assert result['holes']==2*q and result['interaction_budget']==q
        assert ordinary_flow(*data)['deficit']==q
        totals['sharp_two_owner_resource_systems']+=1
    # Maximum terminal matching can leave holes only in final mixed paths;
    # keeping those holes out of the final-alpha budget is a strict gain.
    kinds,pairs,_=canonical(('A','B','M','M'))
    data=kinds,pairs,[(0,2),(1,4),(5,4),(7,4)],{o:set() for o in range(4)},set()
    refined=check(data,totals)
    assert refined['holes']==2 and refined['interaction_budget']==1
    assert refined['final_component_budget']==0 and refined['certified_deficit']==0
    totals['strict_final_alpha_refinement_controls']=1
    # Counterexample to splitting one original resource into two local copies.
    kinds,pairs,_=canonical(('A','A'))
    shared=(kinds,pairs,[],{0:{0},1:{0}},{0})
    split=(kinds,pairs,[],{0:{0},1:{1}},{0,1})
    assert len(matching(slot_graph(shared)))==2 and ordinary_flow(*shared)['value']==1
    assert len(matching(slot_graph(split)))==4 and ordinary_flow(*split)['value']==2
    totals['shared_identity_split_counterexamples']=1


def physical(totals):
    records=[]
    for q,padding in itertools.product(range(1,17),(0,2,10)):
        current=fixture(q,padding)
        data,_,_=whole_support_data(current,whole_bands(current))
        result=check(data,totals)
        assert result['holes']==q and result['interaction_budget']==0
        pruned,meta=live_prune(data)
        after=lift(pruned,matching(slot_graph(pruned)))
        assert after['holes']==q and after['interaction_budget']==0
        owner,aa,_,mm=owner_data(*pruned[:2])
        assert len(mm)==q
        # The lower TP of every alpha has no possible target even AFTER the
        # mathematically safe pruning. Both original alpha tips remain.
        graph=slot_graph(pruned)
        assert all((6+10*i,6) in graph and not graph[6+10*i,6] for i in range(q))
        assert ordinary_flow(*pruned)['value']==q
        totals['physical_systems']+=1
        records.append(dict(copies=q,extra_columns=padding,holes=result['holes'],
            global_budget=result['global_budget'],interaction_budget=0,
            paid=result['certified_payment'],after_pruning_holes=after['holes'],
            live_mixed=len(mm),removed_mixed=len(meta['removed_mixed'])))
    return records


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter();abstract(totals);records=physical(totals)
    result=dict(status='PASS',totals=dict(totals),physical=records,
        scope='General partial-certificate/component rounding and safe source-to-resource '
        'graph pruning are written proofs, not conclusions of enumeration. '
        'Pruning preserves the fixed T/M geometry and original resource identities. '
        'No universal frozen-grid compensation theorem or 5/6 improvement.')
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
