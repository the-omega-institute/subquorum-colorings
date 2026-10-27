"""Exact local prefix optimization and disjoint pair min-cost certificates.

The theorem is for one/two-contact repairs on a matching of ORIGINAL TT/HH
components. It does not assert optimality among general shared networks.
"""
from collections import defaultdict
from functools import lru_cache
from itertools import groupby
import json
from pathlib import Path
import random

from check_mixed_terminal_compensation import decompose, edge, grid, selected_feasible
from check_ordered_th_relay import all_gates, family, family_control
from check_contact_cycle_ledger import analyse, row_family

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def best_credit(points):
    """Return credit and original contact indices; equal x/y never invert."""
    assert points
    ys = {y:i+1 for i,y in enumerate(sorted({y for x,y in points},reverse=True))}
    tree = [None]*(len(ys)+1)
    def insert(y,value):
        i = ys[y]
        while i < len(tree):
            if tree[i] is None or value < tree[i]: tree[i] = value
            i += i & -i
    def query(y):
        i = ys[y]-1; result = None
        while i:
            if tree[i] is not None and (result is None or tree[i] < result):
                result = tree[i]
            i -= i & -i
        return result
    credit = 0; chosen = [0]
    ordered = sorted((x,y,j) for j,(x,y) in enumerate(points))
    for _,group in groupby(ordered,key=lambda item:item[0]):
        batch = list(group)
        for x,y,j in batch:
            prior = query(y)
            if prior is not None and x-y-prior[0] > credit:
                credit = x-y-prior[0]; chosen = [prior[1],j]
        for x,y,j in batch: insert(y,(x-y,j))
    return credit,chosen


def pair_options(h,w,m,n,t,available=None):
    data = decompose(grid(h,w),m,n,t)
    assert selected_feasible(data['P'],t)
    gates = all_gates(h,w,n,data) if available is None else available
    prefixes = {}
    for i,p in enumerate(data['paths']):
        pv = p['vertices']
        if sum(pv[0]) % 2: pv = list(reversed(pv))
        prefixes[i] = {edge(pv[j],pv[j+1]):j//2 for j in range(0,len(pv)-1,2)}
    grouped = defaultdict(list)
    for g in gates:
        i,j = sorted(g['ids']); kinds = [data['paths'][x]['kind'] for x in [i,j]]
        if set(kinds) != {'TT','HH'}: continue
        a,b = (i,j) if kinds[0]=='TT' else (j,i)
        grouped[a,b].append(g)
    options = {}
    for (a,b),gs in grouped.items():
        points = [(prefixes[a][g['cut'][a]],prefixes[b][g['cut'][b]]) for g in gs]
        credit,chosen = best_credit(points)
        # Independent quadratic check of the range-minimum algorithm.
        brute = max([0]+[v-x+y-z for x,y in points for v,z in points if x<v and y>z])
        assert credit == brute
        total = len(data['paths'][a]['M'])+len(data['paths'][b]['M'])
        assert 0 <= credit <= total
        selected = [gs[j] for j in chosen]
        physical = analyse(h,w,m,n,t,selected)
        assert physical['old_bad_M'] == total and physical['cycle_M'] == credit
        assert physical['new_bad_M'] == 0 and physical['new_TH_M'] == total-credit
        options[a,b] = dict(cost=total-credit,credit=credit,total=total,gates=selected)
    left = [i for i,p in enumerate(data['paths']) if p['kind']=='TT']
    right = [i for i,p in enumerate(data['paths']) if p['kind']=='HH']
    return data,left,right,options


def min_cost_matching(left,right,options):
    """Unit-capacity successive shortest augmentations; return Hall witness on failure."""
    nodes = [('s',)]+[('a',i) for i in left]+[('b',i) for i in right]+[('t',)]
    source,sink = 0,len(nodes)-1; ids = {x:i for i,x in enumerate(nodes)}
    graph = [[] for _ in nodes]
    def add(u,v,cost):
        graph[u].append([v,len(graph[v]),1,cost])
        graph[v].append([u,len(graph[u])-1,0,-cost])
        return graph[u][-1]
    for a in left: add(source,ids['a',a],0)
    for b in right: add(ids['b',b],sink,0)
    arcs = {(a,b):add(ids['a',a],ids['b',b],option['cost'])
            for (a,b),option in options.items()}
    cost = 0; flow = 0
    while True:
        dist = [None]*len(nodes); dist[source] = 0; parent = {}
        for _ in range(len(nodes)-1):
            changed = False
            for u,edges in enumerate(graph):
                if dist[u] is None: continue
                for j,(v,rev,cap,c) in enumerate(edges):
                    if cap and (dist[v] is None or dist[v] > dist[u]+c):
                        dist[v] = dist[u]+c; parent[v] = (u,j); changed = True
            if not changed: break
        if dist[sink] is None: break
        v = sink
        while v != source:
            u,j = parent[v]; arc = graph[u][j]
            arc[2] -= 1; graph[v][arc[1]][2] += 1; v = u
        cost += dist[sink]; flow += 1
    chosen = [key for key,arc in arcs.items() if arc[2]==0]
    assert len(chosen)==flow and len({a for a,b in chosen})==flow
    assert len({b for a,b in chosen})==flow
    assert cost == sum(options[key]['cost'] for key in chosen)
    hall = None
    if flow < len(left):
        reachable = {source}; todo = [source]
        while todo:
            for v,rev,cap,c in graph[todo.pop()]:
                if cap and v not in reachable: reachable.add(v); todo.append(v)
        s = {a for a in left if ids['a',a] in reachable}
        neighbours = {b for a,b in options if a in s}
        assert neighbours == {b for b in right if ids['b',b] in reachable}
        assert len(neighbours)<len(s)
        hall = dict(TT=sorted(s),HH_neighbours=sorted(neighbours),deficit=len(s)-len(neighbours))
    return dict(flow=flow,cost=cost,chosen=chosen,hall=hall)


def exhaustive_matching(left,options):
    """Independent assignment recursion: max cardinality, then min total cost."""
    @lru_cache(None)
    def solve(j,used):
        if j==len(left): return 0,0
        best = solve(j+1,used)
        for (a,b),option in options.items():
            if a != left[j] or b in used: continue
            flow,cost = solve(j+1,tuple(sorted(used+(b,))))
            candidate = (flow+1,cost+option['cost'])
            if candidate[0]>best[0] or candidate[0]==best[0] and candidate[1]<best[1]:best=candidate
        return best
    return solve(0,())


def certificate(h,w,m,n,t,available=None,exhaustive=False):
    data,left,right,options = pair_options(h,w,m,n,t,available)
    result = min_cost_matching(left,right,options)
    if exhaustive:
        assert (result['flow'],result['cost']) == exhaustive_matching(left,options)
    chosen = result['chosen']; s = len(chosen)
    if s:
        gates = [g for key in chosen for g in options[key]['gates']]
        physical = analyse(h,w,m,n,t,gates)
        a,b,th = data['counts']
        assert physical['after']==(a-s,b-s,th+2*s)
        assert physical['new_TH_M']==result['cost'] and physical['new_bad_M']==0
        assert physical['cycle_M']==sum(options[key]['credit'] for key in chosen)
        if s==len(left): assert physical['after'][0]==0
    else:
        physical = None
    return dict(TT=len(left),HH=len(right),pair_edges=len(options),flow=s,
                added_paid_M=result['cost'],credit=sum(options[key]['credit'] for key in chosen),
                original_matched_M=sum(options[key]['total'] for key in chosen),
                full=s==len(left),hall=result['hall'],physical=physical)


def packed(q,w):
    h = 4*q
    m = {edge((r,c),(r,c+1)) for j in range(q) for r in (4*j+1,4*j+2)
         for c in range(1,w-2,2)}
    n = {edge((r,c),(r,c+1)) for r in range(h) for c in range(0,w,2)}
    t = {(4*j+1,c) for j in range(q) for c in (0,w-1)}
    return h,w,m,n,t


def main():
    rng = random.Random(271027); prefix_controls = 0
    for d in range(1,41):
        for _ in range(25):
            points = [(rng.randrange(15),rng.randrange(15)) for _ in range(d)]
            credit,chosen = best_credit(points)
            brute = max([0]+[v-x+y-z for x,y in points for v,z in points if x<v and y>z])
            assert credit==brute
            if len(chosen)==2:
                (x,y),(v,z)=[points[j] for j in chosen]
                assert x<v and y>z and credit==v-x+y-z
            prefix_controls += 1
    rows = []; failures = 0; positive_cost = 0
    for h in (4,6,10):
        for w in (4,6,8):
            m,n,t,gates = row_family(h,w)
            for probability in (0,.2,.5,1):
                for _ in range(4):
                    available = [g for g in gates if rng.random()<probability]
                    result = certificate(h,w,m,n,t,available,exhaustive=True)
                    failures += not result['full']; positive_cost += result['added_paid_M']>0
                    rows.append(result)
    packings = []
    for q in range(1,13):
        for w in range(4,25,2):
            result = certificate(*packed(q,w))
            assert result['full'] and result['flow']==q and result['added_paid_M']==0
            assert result['credit']==q*(w-2)
            packings.append(result)
    relay_failures = []
    for r in range(1,21):
        result = certificate(*family(r),exhaustive=True)
        assert not result['full'] and result['flow']==result['pair_edges']==0
        assert result['hall']['deficit']==1
        relay = family_control(r)
        relay_failures.append(result)
    assert failures and positive_cost
    output = dict(status='PASS',prefix_optimizer_controls=prefix_controls,
        actual_matching_assignment_controls=len(rows),actual_restricted_pool_Hall_failures=failures,
        actual_positive_cost_batches=positive_cost,actual_zero_cost_packings=len(packings),
        all_candidate_direct_Hall_failures_with_TH_relay=len(relay_failures),
        largest_packing=packings[-1],largest_direct_class_failure=relay_failures[-1],
        scope='Fast prefix optimizer versus quadratic inversion search; residual min-cost matching versus exhaustive small assignments; chosen witnesses versus actual physical component/resource decomposition; arbitrary-qW packing and Hall-failure family have written proofs.',
        limitations='Exact optimum within original-component-disjoint one/two-contact pair class only. Not an optimum over arbitrary multi-contact/shared-component networks; no universal covering or5/6 claim.')
    (ROOT/'output/double-contact-cover.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output))


if __name__ == '__main__': main()
