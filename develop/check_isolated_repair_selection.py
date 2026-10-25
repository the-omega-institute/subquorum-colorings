"""Exact isolated-selection repair oracle, full beta-entry model and weighted choice.

Written proofs: docs/ISOLATED_SELECTION_REPAIR_MATROID.md. Standard resource
matroid contraction and min-cost flow are used, not claimed as new theorems.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_selection_maximum_singleton import compile_even_width,cropped
from check_forced_mates_and_adjacent_maxima import configuration
from check_crossing_matching_ports import rectangle,compile_partition
from check_frozen_beta_support_fork import fixture as beta_fixture
from check_frozen_tip_slot_obstruction import fixture as tip_fixture
from check_whole_support_fork_flow import fork_flow,normalize_beta_paths
from check_whole_support_fork_normal_form import canonical,evaluate
from check_interface_reserve_reoptimization import subsets,constrained_primitive
from check_promotion_cores import frozen_certificate

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def available(data,pool):
    return (*data[:3],{o:js&pool for o,js in data[3].items()},set(pool))


def paid_sources(data,flow):
    _,A,_,_=owner_data(*data[:2])
    return set().union(set(),*(set(c['owners'])&A for c in flow['certificates']))


def repair_flow(data,candidates,weights,protected):
    """Max value, then retain protected sources, then min deletions/weight/links.

    Lexicographic integral costs avoid arbitrary large scalar rewards.
    Actual mixed and BOTH beta BP entry gates are retained.
    """
    owner,A,B,X=owner_data(*data[:2]);assert protected<=A and candidates<=data[4]
    assert set(weights)==candidates and all(isinstance(w,int) and w>=0 for w in weights.values())
    source=('source',);sink=('sink',);edges=[];adj=defaultdict(list);zero=(0,0,0,0)
    plus=lambda a,b:tuple(x+y for x,y in zip(a,b))
    def add(u,v,cap,cost=zero,tag=None):
        i=len(edges)
        edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
                      dict(u=v,v=u,cap=0,initial=0,cost=tuple(-x for x in cost),tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    exit=lambda o:('alpha',o) if o in A else ('out',o) if o in X else ('beta',o)
    for a in sorted(A):add(source,exit(a),1,(-int(a in protected),0,0,0),('source',a))
    for x in sorted(X):add(('in',x),exit(x),1,tag=('mixed',x))
    for b in sorted(B):
        for tip in data[1][b]:add(('tip',tip),exit(b),1,tag=('tip',tip))
        add(exit(b),sink,1,tag=('beta',b))
    for j in sorted(data[4]):
        cost=(0,1,weights[j],0) if j in candidates else zero
        add(('interval',j),sink,1,cost,('interval',j))
    large=len(A)+1
    for a,b in sorted(set(data[2])):
        assert data[0][a]=='TP' and data[0][b]=='BP'
        if owner[a]==owner[b]:continue
        incoming=('tip',b) if owner[b] in B else ('in',owner[b])
        add(exit(owner[a]),incoming,large,(0,0,0,1),('link',a,b))
    for o,js in data[3].items():
        for j in sorted(js):add(exit(o),('interval',j),large,tag=('access',o,j))
    nodes=set(adj)|{source,sink};value=0;total=zero
    while True:
        distances={source:zero};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in distances:
                    candidate=plus(distances[e['u']],e['cost'])
                    if e['v'] not in distances or candidate<distances[e['v']]:
                        distances[e['v']]=candidate;parent[e['v']]=i;changed=True
            if not changed:break
        assert all(not e['cap'] or e['u'] not in distances or
            e['v'] not in distances or distances[e['v']]<=plus(distances[e['u']],e['cost']) for e in edges)
        if sink not in distances:break
        v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v);i=parent[v]
            edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1;total=plus(total,distances[sink])
    remaining={i:e['initial']-e['cap'] for i,e in enumerate(edges) if i%2==0}
    paths=[]
    for i in adj[source]:
        if i%2 or not remaining[i]:continue
        u=source;tags=[];seen=set()
        while u!=sink:
            assert u not in seen;seen.add(u)
            j=next(j for j in adj[u] if j%2==0 and remaining[j]>0)
            remaining[j]-=1;e=edges[j];tags.append(e['tag']);u=e['v']
        betas=[owner[t[1]] for t in tags if t[0]=='tip'];assert len(betas)<=1
        paths.append(dict(source=tags[0][1],resource=tags[-1],beta=betas[0] if betas else None,
            links=[(t[1],t[2]) for t in tags if t[0]=='link']))
    assert not any(remaining.values())
    for b in B:
        ps=[p for p in paths if p['beta']==b]
        if ps:normalize_beta_paths(b,ps)
    paid={p['source'] for p in paths};chosen=[e for p in paths for e in p['links']]
    terminals=[p['resource'] for p in paths]
    used_new={tag[1] for tag in terminals if tag[0]=='interval' and tag[1] in candidates}
    assert len(terminals)==len(set(terminals))==value
    assert len({v for e in chosen for v in e})==2*len(chosen)
    assert total==(-len(paid&protected),len(used_new),sum(weights[j] for j in used_new),len(chosen))
    assert evaluate(*data[:2],chosen,*data[3:])['value']==value
    return dict(value=value,paid=paid,used_new=used_new,weight=total[2],links=chosen,cost=total[3],paths=paths)


def rank_checks(data,candidates,totals,independent=False):
    candidates=set(candidates);Q0=data[4]-candidates
    base=available(data,Q0);old=fork_flow(*base);p=old['value'];protected=paid_sources(base,old)
    totals['baseline_fork_models']+=any(c['kind']=='fork' for c in old['certificates'])
    ground=sorted(candidates);pool_list=list(subsets(ground));rank={};flows={}
    for C in pool_list:
        f=fork_flow(*available(data,Q0|C));key=frozenset(C);flows[key]=f;rank[key]=f['value']-p
        assert 0<=rank[key]<=len(C)
        totals['candidate_pool_flows_with_forks']+=any(c['kind']=='fork' for c in f['certificates'])
        totals['resource_subsets']+=1
        if independent and len(C)<=2:
            primitive=constrained_primitive(available(data,Q0|C),protected)
            # Source protection can cost extra links; its value must agree.
            assert primitive[0]==f['value']
            totals['independent_protected_primitive_values']+=1
    r=rank[frozenset(candidates)]
    for C in pool_list:
        for D in pool_list:
            cc,dd=frozenset(C),frozenset(D)
            assert rank[cc]+rank[dd]>=rank[cc|dd]+rank[cc&dd]
            if C<=D:assert rank[cc]<=rank[dd]
            totals['rank_submodular_pairs']+=1
        if all(rank[frozenset(C|{j})]==rank[frozenset(C)] for j in candidates-C):
            assert rank[frozenset(C)]==r
            totals['exact_zero_marginal_stopping_certificates']+=1
    bases=[C for C in pool_list if rank[frozenset(C)]==len(C)==r]
    assert bases and min(len(C) for C in pool_list if rank[frozenset(C)]==r)==r
    for b in range(len(ground)+1):
        assert max(rank[frozenset(C)] for C in pool_list if len(C)<=b)==min(b,r)
        totals['exact_deletion_budget_frontier_entries']+=1
    rng=random.Random(7000+len(data[1])*100+len(ground))
    for _ in range(3):
        weights={j:rng.randrange(5) for j in ground};chosen=set()
        for j in sorted(ground,key=lambda j:(weights[j],j)):
            if rank[frozenset(chosen|{j})]>len(chosen):chosen.add(j)
        opt_weight=min(sum(weights[j] for j in C) for C in bases)
        assert len(chosen)==r and sum(weights[j] for j in chosen)==opt_weight
        answer=repair_flow(data,candidates,weights,protected)
        assert answer['value']==p+r and protected<=answer['paid']
        assert len(answer['used_new'])==r and answer['weight']==opt_weight
        # Exhaustive independent source-protected link optimum over every
        # minimum-count, minimum-weight repair set, using the prior oracle.
        if independent:
            cheapest=min(constrained_primitive(available(data,Q0|C),protected)[1]
                for C in bases if sum(weights[j] for j in C)==opt_weight)
            assert answer['cost']==cheapest
            totals['independent_lexicographic_repair_optima']+=1
        totals['weighted_greedy_and_joint_flow_profiles']+=1
    totals['models']+=1
    return dict(old_value=p,maximum=p+r,minimum_repairs=r,protected=sorted(protected),bases=len(bases))


def isolated(cur):
    R,C,T,M=cur;occupied=T|{v for e in M for v in e}
    return sorted(v for v in T if all((v[0]+dr,v[1]+dc) not in occupied
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]))


def physical(cur,label,totals,limit=5,save=False,regions=None):
    def compile_cur(board):
        if regions is None:return compile_even_width(board)
        summary,data=compile_partition(board,regions)
        return data,summary
    old,old_meta=compile_cur(cur);possible=isolated(cur)
    old_flow=fork_flow(*old)
    # Spread deterministic representatives across both boundaries/interior.
    chosen=possible if len(possible)<=limit else [possible[i*(len(possible)-1)//(limit-1)] for i in range(limit)]
    # For the maximum adjacent boards include left reserve and both shared seams.
    if label.startswith(('adjacent','mixed')):
        useful=[v for v in [(0,1),(0,11),(cur[0]-1,11),(0,21),(cur[0]-1,21)] if v in possible]
        chosen=list(dict.fromkeys(useful+chosen))[:limit]
    assert len(set(chosen))==len(chosen)
    if regions is None:
        column_units={v:(r//2,c,c) for r in range(0,cur[0],2) for c in range(cur[1]) for v in [(r,c),(r+1,c)]}
    else:
        bands=[band for region in regions for band in region['bands']]
        column_units={v:(b,c,c) for b,band in enumerate(bands) for c,pair in enumerate(band) for v in pair}
    unit=lambda v:column_units[v]
    pool={unit(v) for v in chosen};assert len(pool)==len(chosen) and not pool&old[4]
    fullcur=(*cur[:2],cur[2]-set(chosen),cur[3]);full,_=compile_cur(fullcur)
    assert full[:3]==old[:3] and full[4]==old[4]|pool
    oldfrozen=frozen_certificate(cur)[0];P={v for e in cur[3] for v in e}
    for D in subsets(chosen):
        changed=(*cur[:2],cur[2]-D,cur[3]);data,meta=compile_cur(changed)
        C={unit(v) for v in D}
        assert data==available(full,old[4]|C)
        assert meta['slack']==cur[0]*cur[1]//2-len(cur[2])-len(cur[3])+len(D)
        assert frozen_certificate(changed)[0]==oldfrozen
        new_flow=fork_flow(*data);gain=new_flow['value']-old_flow['value']
        assert meta['slack']+new_flow['deficit']==old_meta['slack']+old_flow['deficit']+len(D)-gain
        totals['physical_commuting_deletion_subsets']+=1
        totals['fully_frozen_deletion_subsets']+=int(oldfrozen==P)
        if regions is not None:
            totals['mixed_partition_commuting_subsets']+=1
            totals['mixed_partition_actual_crossing_edge_checks']+=len(meta['crossing_edges'])
    result=rank_checks(full,pool,totals,independent=len(full[1])<=20)
    result.update(label=label,shape=cur[:2],isolated_candidates=len(possible),tested_candidates=len(chosen),frozen=oldfrozen==P)
    if save:
        fixture=dict(label=label,shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],deleted_candidates=chosen,
            candidate_units=sorted(pool),old_units=sorted(old[4]),full_units=sorted(full[4]),pairs=full[1],
            owner_links=sorted({(owner_data(*full[:2])[0][u],owner_data(*full[:2])[0][v]) for u,v in full[2]}),
            support=[(o,sorted(js)) for o,js in full[3].items()],result=result)
        (Path(__file__).parent/'fixtures/isolated_selection_repair.json').write_text(json.dumps(fixture,indent=2)+'\n')
    return result


def all_candidate_adjacent(w,k,totals):
    cur=configuration(w,k);X=set(isolated(cur));old,_=compile_even_width(cur)
    changed=(*cur[:2],cur[2]-X,cur[3]);data,_=compile_even_width(changed)
    E={(r//2,c,c) for r,c in X}
    assert data[:3]==old[:3] and data[4]==old[4]|E and not old[4]&E
    assert frozen_certificate(changed)[0]=={v for e in cur[3] for v in e}
    own,A,B,_=owner_data(*data[:2]);assert len(A)==k and not B
    assert all(not data[3][a] for a in A)
    answer=repair_flow(data,E,{j:1 for j in E},set())
    assert (answer['value'],len(answer['used_new']),answer['cost'])==(k,k,k)
    # A closed-form optimal choice for all W,k, independently of the solver.
    points={(0,10*a+1) for a in range(k)};assert points<=X
    explicit,_=compile_even_width((*cur[:2],cur[2]-points,cur[3]))
    links=[((1,10*a+5),(1,10*a+4)) for a in range(k)]
    assert all(link in explicit[2] for link in links)
    assert evaluate(*explicit[:2],links,*explicit[3:])['value']==k
    totals['all_candidate_global_optimal_adjacent_controls']+=1
    return dict(W=w,k=k,candidates=len(X),minimum_deletions=k,minimum_links=k)


def nonisolated_negative_control(totals):
    old=(2,4,{(0,1),(1,1)},[]);new=(2,4,{(1,1)},[])
    before,_=compile_even_width(old);after,_=compile_even_width(new)
    assert before[4]=={(0,0,2),(0,3,3)}
    assert after[4]=={(0,0,0),(0,2,2),(0,3,3)}
    assert len(after[4])==len(before[4])+1 and not before[4]<=after[4]
    totals['nonisolated_TT_identity_failure_controls']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();records=[];rng=random.Random(20261025)
    kinds,pairs,_=canonical('AAB')
    rank_checks((kinds,pairs,[(0,4),(2,5)],{0:set(),1:set(),2:{0}},{0}),{0},totals,independent=True)
    totals['explicit_two_entry_beta_repair_models']+=1
    for index in range(90):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,5)))
        kinds,pairs,possible=canonical(types);rng.shuffle(possible)
        links=possible[:rng.randrange(min(9,len(possible))+1)]
        Q=set(range(rng.randrange(1,6)));cand={j for j in Q if rng.randrange(3)}
        support={o:{j for j in Q if rng.randrange(2)} for o in range(len(pairs))}
        data=(kinds,pairs,links,support,Q)
        result=rank_checks(data,cand,totals,independent=index<24)
        totals['abstract_models']+=1
        if index<8:records.append(dict(label='abstract-'+str(index),**result))
    for w,k in itertools.product((8,10,20),(1,2,3)):
        records.append(physical(configuration(w,k),'adjacent-'+str(w)+'-'+str(k),totals,save=(w,k)==(8,2)))
    for w in (8,10,20):records.append(physical(cropped(w),'raw-singleton-'+str(w),totals))
    records.append(physical(beta_fixture()[0],'beta-fork',totals))
    records.append(physical(tip_fixture(),'tip-slot',totals))
    for w,k in itertools.product((8,10),(1,2)):
        cur=configuration(w,k);R,C=cur[:2]
        regions=[rectangle(0,2,0,C,True),rectangle(2,R,0,C)]
        records.append(physical(cur,'mixed-crossing-'+str(w)+'-'+str(k),totals,regions=regions))
    for w in (8,10):
        cur=cropped(w);R,C=cur[:2]
        regions=[rectangle(0,R,0,14),rectangle(0,R,14,C,True)]
        records.append(physical(cur,'mixed-singleton-'+str(w),totals,regions=regions))
    optimal=[all_candidate_adjacent(w,k,totals) for w,k in itertools.product((8,20,64),(1,2,4,8))]
    nonisolated_negative_control(totals)
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,all_candidate_adjacent=optimal,
        scope='General isolated-deletion physical adapter; normalized candidate repair rank, arbitrary mixed/BP/beta flow; exact deletion frontier, weighted greedy, source-protected joint lexicographic selection and links.',
        limits=['General proofs are written; enumeration corroborates.',
                'Full compensation is conditional on all candidate resources paying all alpha sources.',
                'Only isolated selections are deleted; no arbitrary candidate-removal identity claim.',
                'No universal5over6 improvement or change of auxiliary partition.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
