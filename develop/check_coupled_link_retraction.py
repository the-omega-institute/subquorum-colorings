"""Minimum full-repair retractions and serial release dependencies.

General proofs and explicit scope: docs/COUPLED_LINK_RETRACTION.md.
No optional packages or discovery solver. Finite controls do not replace proofs.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_partial_tip_compensation import live_prune
from check_terminal_cancellation_and_stranded_demand import all_link_matchings
from check_whole_support_fork_normal_form import (
    canonical, contract, evaluate, ordinary_flow, whole_support_data,
)
from check_whole_support_fork_flow import fork_flow
from check_frozen_gap_retraction import family as physical_family
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_merger_completion_reserves import feasible, frozen
from check_interval_connector_cycles_and_missing_ports import whole_bands

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def weighted_full(data, old, lexicographic=True):
    """Full-fork network, signed rewards only on original alpha-first links.

    Old arcs cannot lie on a forward cycle. All other physical links have
    positive toll in the lexicographic run; no negative cycle is introduced.
    """
    kinds, pairs, links, support, resources = data
    owner, aa, bb, mm = owner_data(kinds, pairs)
    old = set(old)
    assert old <= set(links)
    assert len({owner[u] for u,v in old}) == len(old)
    assert len({owner[v] for u,v in old}) == len(old)
    for u,v in old:
        assert owner[u] in aa and owner[v] in mm
        assert not support[owner[u]]
        assert all(x == u for x,y in links if owner[x] == owner[u])
    scale = len(aa)+len(mm)+1 if lexicographic else 1
    edges=[]; adj=defaultdict(list)
    source=('source',); sink=('sink',)
    def add(u,v,cap,toll=0,tag=None):
        i=len(edges)
        edges.extend([dict(u=u,v=v,cap=cap,initial=cap,toll=toll,tag=tag),
                      dict(u=v,v=u,cap=0,initial=0,toll=-toll,tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    def out(o):
        return ('a',o) if o in aa else ('mout',o) if o in mm else ('b',o)
    for a in sorted(aa):add(source,out(a),1)
    for m in sorted(mm):add(('min',m),out(m),1)
    for b in sorted(bb):
        for tip in pairs[b]:add(('bp',tip),out(b),1)
        add(out(b),sink,1)
    for j in sorted(resources):add(('i',j),sink,1)
    for e in sorted(set(links)):
        u,v=e
        if owner[u]==owner[v]:continue
        target=('bp',v) if owner[v] in bb else ('min',owner[v])
        toll=(1 if lexicographic else 0)-scale*(e in old)
        add(out(owner[u]),target,len(aa)+1,toll,e)
    for o in sorted(support):
        for j in sorted(support[o]):add(out(o),('i',j),len(aa)+1)
    nodes=set(adj)|{source,sink}; value=toll=0
    while value<len(aa):
        dist={source:0}; parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in dist:
                    d=dist[e['u']]+e['toll']
                    if e['v'] not in dist or d<dist[e['v']]:
                        dist[e['v']]=d;parent[e['v']]=i;changed=True
            if not changed:break
        # Bellman-Ford optimality check on every reachable residual arc.
        assert all(not e['cap'] or e['u'] not in dist or
                   (e['v'] in dist and dist[e['v']]<=dist[e['u']]+e['toll']) for e in edges)
        if sink not in dist:break
        v=sink; seen=set()
        while v!=source:
            assert v not in seen;seen.add(v)
            i=parent[v];edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1;toll+=dist[sink]
    selected=[e['tag'] for e in edges[::2] if e['tag'] is not None and e['initial']>e['cap']]
    assert len({v for e in selected for v in e})==2*len(selected)
    retained=old&set(selected)
    assert toll==(len(selected) if lexicographic else 0)-scale*len(retained)
    assert evaluate(*data[:2],selected,*data[3:])['value']==value
    return dict(value=value,retractions=len(old)-len(retained),links=len(selected),
                toll=toll,scale=scale,selected=selected,kept=sorted(retained))


def serial(n):
    assert n>=2
    kinds,pairs,_=canonical('A'*n+'M'*n+'B'*n)
    a=lambda i:pairs[i][0]
    mi=lambda i:pairs[n+i][0]
    mo=lambda i:pairs[n+i][1]
    b=lambda i:pairs[2*n+i][0]
    old=[(a(i),mi(i)) for i in range(n)]
    alternate=[(a(i),mi(i+1)) for i in range(n-1)]+[(a(n-1),b(n-1))]
    exits=[(mo(i),b(max(0,i-1))) for i in range(n)]
    links=old+alternate+exits
    support={i:set() for i in range(3*n)}
    return (kinds,pairs,links,support,set()),old


def fixed_value(data,old,released,full):
    kept=[e for i,e in enumerate(old) if i not in released]
    reduced=contract(data,kept)
    flow=fork_flow(*reduced) if full else ordinary_flow(*reduced)
    return flow['value']


def independent_full_optimum(data,old,totals):
    """All actual terminal matchings, not a path/reward restatement."""
    n=len(owner_data(*data[:2])[1]); old=set(old); best=None
    for selected in all_link_matchings(data[2]):
        totals['independent_terminal_matchings']+=1
        if evaluate(*data[:2],selected,*data[3:])['value']!=n:continue
        score=(len(old-set(selected)),len(selected))
        if best is None or score<best:best=score
    return best


def abstract_controls(totals):
    records=[]
    for n in range(2,13):
        data,old=serial(n)
        owner,aa,bb,mm=owner_data(*data[:2])
        # Degree and opposite-phase checks concern actual terminals.
        deg=Counter(v for e in data[2] for v in e)
        assert max(deg.values())<=2
        color={}
        for i,pair in enumerate(data[1]):
            bits=(0,1) if i<n else (1,0)
            color.update(zip(pair,bits))
        assert all(color[u]!=color[v] for u,v in data[1]+data[2])
        pruned,_=live_prune(data)
        assert set(pruned[0])==set(data[0]), 'Every mixed gate is live.'
        # Connected owner graph.
        adj=defaultdict(set)
        for u,v in data[2]:adj[owner[u]].add(owner[v]);adj[owner[v]].add(owner[u])
        seen={0};todo=[0]
        while todo:
            u=todo.pop()
            for v in adj[u]-seen:seen.add(v);todo.append(v)
        assert len(seen)==3*n
        totals['connected_all_live_phase_degree_controls']+=1
        masks=range(1<<n) if n<=8 else sorted({0,(1<<n)-1,(1<<n)-2}|{
            (1<<n)-2-(1<<j) for j in range(1,n)})
        outcomes={}
        for mask in masks:
            released={i for i in range(n) if mask>>i&1}
            expected=n if set(range(1,n))<=released else n-1
            values=[fixed_value(data,old,released,f) for f in (False,True)]
            assert values==[expected,expected]
            totals['fixed_subset_ordinary_full_comparisons']+=2
            outcomes[mask]=expected
        if n<=8:
            for budget in range(n+1):
                best=max(v for mask,v in outcomes.items() if mask.bit_count()<=budget)
                assert best==(n if budget>=n-1 else n-1)
                totals['exhaustive_serial_budget_optima']+=1
        full=weighted_full(data,old)
        reward=weighted_full(data,old,False)
        assert (full['value'],full['retractions'],full['links'])==(n,n-1,2*n-1)
        assert reward['value']==n and reward['retractions']==n-1
        assert full['kept']==[old[0]]
        totals['signed_full_flow_checks']+=2
        if n<=4:
            assert independent_full_optimum(data,old,totals)==(n-1,2*n-1)
            totals['independent_serial_full_optima']+=1
        records.append(dict(sources=n,initial_deficit=1,minimum_full_retractions=n-1,
            minimum_full_total_links=2*n-1,subsets_checked=len(outcomes),
            frozen_grid_realization=False))
    return records


def randomized(totals):
    rng=random.Random(20261025041); accepted=0;forked=0
    for _ in range(180):
        n=rng.randrange(1,4);m=rng.randrange(n,n+2);b=rng.randrange(1,4)
        kinds,pairs,_=canonical('A'*n+'M'*m+'B'*b)
        alpha_tips=[p[0] for p in pairs[:n]]
        tp=alpha_tips+[p[1] for p in pairs[n:n+m]]
        bp=[p[0] for p in pairs[n:n+m]]+[v for p in pairs[n+m:] for v in p]
        old=[(pairs[i][0],pairs[n+i][0]) for i in range(n)]
        available=[(u,v) for u in tp for v in bp if (u,v) not in old]
        rng.shuffle(available)
        links=old+available[:rng.randrange(0,min(6,len(available))+1)]
        W={o:set() if o<n else {j for j in range(2) if rng.random()<.28}
           for o in range(n+m+b)}
        data=(kinds,pairs,links,W,{0,1})
        full=weighted_full(data,old)
        if full['value']!=n:
            totals['random_infeasible_full_targets']+=1;continue
        accepted+=1
        expected=independent_full_optimum(data,old,totals)
        assert expected==(full['retractions'],full['links'])
        reward=weighted_full(data,old,False)
        assert reward['value']==n and reward['retractions']==full['retractions']
        subset_min=n+1
        for mask in range(1<<n):
            r={i for i in range(n) if mask>>i&1}
            if fixed_value(data,old,r,True)==n:subset_min=min(subset_min,len(r))
            totals['random_fixed_subsets']+=1
        assert subset_min==full['retractions']
        contracted=contract(data,full['kept'])
        ans=fork_flow(*contracted)
        assert ans['value']==n and ans['cost']+len(full['kept'])==full['links']
        forked+=any(p['kind']=='fork' for p in ans['certificates'])
        totals['signed_full_flow_checks']+=2
    assert accepted>=100 and forked>0
    totals['random_full_targets']=accepted
    totals['random_repaired_targets_using_beta_forks']=forked


def bundle_controls(totals):
    records=[]
    for lengths in ((2,3),(3,4),(2,4,3),(3,3,3)):
        kinds={};pairs=[];links=[];W={};old=[];tails=[]
        for n in lengths:
            d,C=serial(n);offset=len(pairs);tipoffset=2*offset
            moved=lambda e:tuple(v+tipoffset for v in e)
            kinds.update({v+tipoffset:k for v,k in d[0].items()})
            pairs.extend(map(moved,d[1]));links.extend(map(moved,d[2]))
            W.update({o+offset:set() for o in d[3]})
            start=len(old);old.extend(map(moved,C))
            tails.append(set(range(start+1,start+n)))
        data=kinds,pairs,links,W,set()
        N=sum(lengths);baseline=N-len(lengths);bybudget=defaultdict(list)
        for mask in range(1<<len(old)):
            released={i for i in range(len(old)) if mask>>i&1}
            expected=baseline+sum(t<=released for t in tails)
            assert fixed_value(data,old,released,True)==expected
            bybudget[len(released)].append(expected)
            totals['disjoint_bundle_subset_checks']+=1
        costs=sorted(n-1 for n in lengths);frontier=[]
        for budget in range(len(old)+1):
            completed=max(h for h in range(len(costs)+1) if sum(costs[:h])<=budget)
            exact=max(v for b,vs in bybudget.items() if b<=budget for v in vs)
            assert exact==baseline+completed
            totals['exhaustive_bundle_budget_optima']+=1
            frontier.append(exact)
        records.append(dict(lengths=lengths,initial_deficit=len(lengths),
                            full_retractions=sum(costs),budget_values=frontier))
    return records


def two_active_countercontrol(totals):
    kinds,pairs,_=canonical('AAMB')
    old=[(pairs[0][0],pairs[2][0])]
    alternate=(pairs[0][1],pairs[3][0])
    W={0:set(),1:{0},2:{0},3:set()}
    data=kinds,pairs,old+[alternate],W,{0}
    assert evaluate(*data[:2],old+[alternate],*data[3:])['value']==2
    assert fork_flow(*contract(data,old))['value']==2
    assert independent_full_optimum(data,old,totals)==(0,2)
    # A route using old[0] spends the sole interval on source 0, leaving
    # source 1 unpaid. Keeping old[0] as an unused arm is nevertheless legal.
    try:
        weighted_full(data,old)
    except AssertionError:
        totals['two_active_hypothesis_countercontrols']+=1
    else:
        raise AssertionError('The one-active-tip guard must reject this input.')


def physical_controls(totals):
    records=[]
    for q,c,mirror in itertools.product(range(1,4),(0,1,2),(False,True)):
        _,cur,_,layers,_,old,_=physical_family([c]*q,30,0,mirror)
        assert feasible(cur) and frozen(cur)
        check_rank_certificate(cur,layers)
        data,_,_=whole_support_data(cur,whole_bands(cur))
        # Delete only the proved exterior dead entry ARCS. In particular,
        # keep nonproductive C heads when c=0; blanket live pruning would
        # remove constrained C arcs and would be an invalid adapter here.
        owner,aa,_,_=owner_data(*data[:2])
        active={owner[u]:u for u,v in old}
        removed={e for e in data[2] if owner[e[0]] in aa and e[0]!=active[owner[e[0]]]}
        assert len(removed)==2*q
        for u,v in removed:
            dead=owner[v]
            assert not data[3][dead]
            assert all(owner[y]==dead for x,y in data[2] if owner[x]==dead)
        pruned=(*data[:2],[e for e in data[2] if e not in removed],*data[3:])
        assert set(old)<=set(pruned[2]) and pruned[4]==data[4]
        ans=weighted_full(pruned,old)
        expected=q*max(0,2-c)
        assert (ans['value'],ans['retractions'],ans['links'])==(2*q,expected,2*q)
        subset_min=2*q+1
        for mask in range(1<<(2*q)):
            released={i for i in range(2*q) if mask>>i&1}
            value=fixed_value(data,old,released,True)
            if value==2*q:subset_min=min(subset_min,len(released))
            totals['unpruned_physical_fixed_subsets']+=1
        assert subset_min==expected
        totals['physical_frozen_controls']+=1
        totals['signed_full_flow_checks']+=1
        records.append(dict(copies=q,capacity=c,mirror=mirror,sources=2*q,
                            minimum_full_retractions=expected,total_links=2*q))
    return records


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    totals=Counter()
    abstract=abstract_controls(totals)
    randomized(totals)
    bundles=bundle_controls(totals)
    two_active_countercontrol(totals)
    physical=physical_controls(totals)
    payload=dict(status='passed',scope='Signed full-repair theorem, abstract serial dependency, and previous frozen-family applications; no physical serial embedding.',
                 counts=dict(totals),serial=abstract,bundles=bundles,physical=physical)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(payload,indent=2)+'\n')
    print(json.dumps(dict(status='passed',counts=dict(totals)),indent=2))

if __name__=='__main__':main()
