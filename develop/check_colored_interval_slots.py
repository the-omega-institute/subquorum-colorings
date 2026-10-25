"""Color capacities and actual frozen same-color-hole countercontrols.

General proofs: docs/COLORED_INTERVAL_SLOTS_AND_MONOCHROMATIC_HOLES.md.
No solver, network access or optional packages are required.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_tip_slot_obstruction import (
    SELECTED, MATCHING, LAYERS, matching, slot_graph, independent_strands,
)
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_merger_completion_reserves import feasible, frozen
from check_paired_hole_certificates import all_assignments
from check_partial_tip_compensation import components, lift, live_prune
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import canonical, ordinary_flow, optimize, whole_support_data
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def analyze(data, assigned, color, totals):
    """Check every color count against the original assigned incidences."""
    kinds, pairs, links, support, resources = data
    assert all(color[x] in (0, 1) and color[x] != color[y] for x,y in pairs)
    assert all(color[v] != color[w] for v,w in links)
    graph = slot_graph(data)
    assert len(assigned) == len(set(assigned.values()))
    assert all(t in graph[v] for t,v in assigned.items())
    C = [(v,t[1]) for t,v in assigned.items() if t[0] == 'bp']
    _, inventory, records = cancel_pairs(kinds, pairs, C, Counter())
    aa = [p for p in records if not p['cycle'] and p['alpha'] == p['beta']+1]
    target = {v:t for t,v in assigned.items()}
    inc = {i:[] for i in range(len(aa))}
    for i,p in enumerate(aa):
        x,y = p['ends']
        assert color[x] != color[y]
        for v in p['ends']:
            if v in target:
                assert target[v][0] == 'interval'
                inc[i].append((target[v][1],color[v]))
    edges = [(('a',i),('i',j)) for i,js in inc.items() for j,c in js]
    vertices = {('a',i) for i in inc}|{w for _,w in edges}
    total_h = [0,0]; total_e = [0,0]; deficit = 0; summary = []
    for part in components(vertices,edges):
        alphas = {i for tag,i in part if tag == 'a'}
        units = {j for tag,j in part if tag == 'i'}
        h = [sum(v not in target and color[v] == c for i in alphas for v in aa[i]['ends'])
             for c in (0,1)]
        users = {j:[(i,c) for i in alphas for k,c in inc[i] if k == j] for j in units}
        assert all(1 <= len(uses) <= 2 for uses in users.values())
        e = [sum(len(uses) == 2 and all(bit == c for i,bit in uses) for uses in users.values())
             for c in (0,1)]
        s = [sum(len(uses) == 1 and uses[0][1] == c for uses in users.values()) for c in (0,1)]
        assert h[0]+2*e[0]+s[0] == h[1]+2*e[1]+s[1]
        assert sum(h) <= 2
        allocation = matching({i:{('i',j) for j,c in inc[i]} for i in alphas})
        loss = len(alphas)-len(allocation)
        assert loss == sum(h)//2
        for c in (0,1):
            chosen = {}
            for j,uses in users.items():
                same = [i for i,bit in uses if bit == c]
                if same: chosen[j] = min(same)
            # Actual resource->alpha map: one color-c end per alpha makes
            # chosen alpha identities distinct without a second Hall call.
            assert len(set(chosen.values())) == len(chosen)
            assert len(chosen) == len(alphas)-h[c]-e[c]
            assert loss <= h[c]+e[c]
        if sum(h) == 2:
            assert s == [0,0] and h[0]+2*e[0] == h[1]+2*e[1]
            if h[0] == 2: assert e[1] == e[0]+1
            if h[1] == 2: assert e[0] == e[1]+1
        if not e[0] and not e[1]: assert loss <= min(h)
        totals['incidence_components'] += 1
        totals['components_with_opposite_color_double_slot'] += any(
            len(uses) == 2 and uses[0][1] != uses[1][1] for uses in users.values())
        totals['same_color_two_hole_components'] += loss == 1 and max(h) == 2
        totals['components_with_color_collision'] += bool(sum(e))
        for c in (0,1): total_h[c] += h[c]; total_e[c] += e[c]
        deficit += loss
        summary.append(dict(alphas=len(alphas),units=len(units),holes=h,collisions=e,deficit=loss))
    reference = lift(data,assigned)
    assert deficit == reference['certified_deficit'] == reference['final_component_budget']
    assert deficit <= min(sum(total_h)//2,total_h[0]+total_e[0],total_h[1]+total_e[1])
    totals['certificates'] += 1
    totals['color_bound_strict_vs_global_hole_floor'] += (
        min(total_h[0]+total_e[0],total_h[1]+total_e[1]) < sum(total_h)//2)
    return dict(deficit=deficit,holes=total_h,collisions=total_e,parts=summary,
                assignments=len(assigned),links=len(C),payment=reference['certified_payment'])


def physical(q,w,padding=0,mirror=False):
    assert q >= 1 and w >= 30 and w%2 == padding%2 == 0
    width = w+padding
    def move(v,side,i):
        r,c = (v[0]+4,v[1]) if side == 0 else (9-v[0],w-1-v[1])
        return r+14*i, width-1-c if mirror else c
    cur = (14*q,width,
           {move(v,side,i) for i in range(q) for side in (0,1) for v in SELECTED},
           [tuple(move(v,side,i) for v in edge) for i in range(q) for side in (0,1) for edge in MATCHING])
    layers = [[move(v,side,i) for i in range(q) for side in (0,1) for v in layer] for layer in LAYERS]
    return cur,move,layers


def physical_checks(totals):
    named = {}
    for q in range(1,9):
        for w in (30,32,40):
            for padding in (0,2,10):
                for mirror in (False,True):
                    cur,move,layers = physical(q,w,padding,mirror)
                    assert feasible(cur) and frozen(cur)
                    check_rank_certificate(cur,layers)
                    assert len(cur[2]) == 42*q and len(cur[3]) == 20*q
                    bands = whole_bands(cur)
                    full,meta,_ = whole_support_data(cur,bands)
                    kinds,parts = independent_strands(cur,bands)
                    assert kinds == full[0]
                    assert {frozenset(p) for p in full[1]} == {tips for tips,body in parts if tips}
                    d,pruned = live_prune(full)
                    owner,alphas,betas,mixed = owner_data(*d[:2])
                    assert (len(alphas),len(betas),len(mixed)) == (2*q,2*q,2*q)
                    assert len(pruned['removed_mixed']) == 6*q
                    graph = slot_graph(d)
                    assigned = {}; repaired = {}; chosen_pool = set(); all_pairs = []
                    for i in range(q):
                        rtips = []
                        for side in (0,1):
                            av,bp,rv = (move(v,side,i) for v in ((3,6),(3,7),(3,8)))
                            assert (av,bp) in d[2]
                            assigned['bp',bp] = av; repaired['bp',bp] = av
                            rtips.append(rv)
                            hole = move((6,6),side,i)
                            assert not graph[hole] and not d[3][owner[hole]]
                        shared = d[3][owner[rtips[0]]]&d[3][owner[rtips[1]]]
                        expected = {meta['owner'][move((2,c),0,i)[0]//2,
                                                  move((2,c),0,i)[1]] for c in range(10,w-10)}
                        # L's row 2 moves to row 6, the common R gap band.
                        assert shared == expected and len(shared) == w-20
                        assert d[3][owner[rtips[0]]] == d[3][owner[rtips[1]]] == shared
                        j,k = sorted(shared)[:2]
                        assigned['interval',j,0] = rtips[0]
                        assigned['interval',j,1] = rtips[1]
                        repaired['interval',j,0] = rtips[0]
                        repaired['interval',k,0] = rtips[1]
                        chosen_pool.add(j);all_pairs.append((j,k))
                    color = {v:sum(v)%2 for v in d[0]}
                    bad = analyze(d,assigned,color,totals)
                    good = analyze(d,repaired,color,totals)
                    assert len(matching(graph)) == len(assigned) == len(repaired) == 4*q
                    c = int(mirror)
                    assert bad['holes'][c] == 2*q and bad['holes'][1-c] == 0
                    assert bad['collisions'][c] == 0 and bad['collisions'][1-c] == q
                    assert (bad['payment'],bad['deficit']) == (q,q)
                    assert good['holes'] == bad['holes'] and good['collisions'] == [0,0]
                    assert (good['payment'],good['deficit']) == (2*q,0)
                    flow = ordinary_flow(*d); fullflow = fork_flow(*d)
                    assert (flow['value'],flow['cost'],flow['deficit']) == (2*q,2*q,0)
                    assert (fullflow['value'],fullflow['cost']) == (2*q,2*q)
                    C = [(v,t[1]) for t,v in assigned.items() if t[0] == 'bp']
                    small_support = {o:js&chosen_pool for o,js in d[3].items()}
                    restricted = d[:2]+(C,small_support,chosen_pool)
                    restored = d[:3]+(small_support,chosen_pool)
                    repair_pool = {j for pair in all_pairs for j in pair}
                    distinct = d[:2]+(C,{o:js&repair_pool for o,js in d[3].items()},repair_pool)
                    for model,expected_value in ((restricted,q),(restored,2*q),(distinct,2*q)):
                        for forks in (False,True):
                            actual = fork_flow(*model) if forks else ordinary_flow(*model)
                            assert (actual['value'],actual['cost']) == (expected_value,expected_value)
                            totals['resource_link_model_flow_checks'] += 1
                            if q == 1 and w == 30 and padding == 0:
                                independent = optimize(*model,allow_forks=forks)
                                assert (independent['value'],independent['cost']) == (actual['value'],actual['cost'])
                                totals['independent_primitive_comparisons'] += 1
                    totals['physical_boards'] += 1
                    totals['strict_rank_certificates'] += 1
                    if q in (1,8) and w == 30 and padding == 0:
                        named[f'q{q}_mirror{int(mirror)}'] = dict(shape=cur[:2],endpoints=40*q,
                            selected=len(cur[2]),bad=bad,repaired=good,full_payment=flow['value'],
                            full_minimum_links=flow['cost'],shared_units_per_pair=w-20)
    return named


def abstract_checks(totals):
    rng = random.Random(20261025037)
    families = [('A',),('A','A'),('A','M'),('A','B'),('A','A','M'),
                ('A','B','M'),('A','B','M','M'),('A','A','B','M')]
    for types in families:
        for trial in range(50):
            kinds,pairs,possible = canonical(types)
            color = {}
            for pair in pairs:
                phase = rng.randrange(2);color[pair[0]] = phase;color[pair[1]] = 1-phase
            links = [e for e in possible if color[e[0]] != color[e[1]] and rng.randrange(3) == 0]
            resources = set(range(rng.randrange(4)))
            support = {o:{j for j in resources if rng.randrange(2)} for o in range(len(pairs))}
            data = kinds,pairs,links,support,resources
            graph = slot_graph(data)
            assigned = matching(graph)
            analyze(data,assigned,color,totals)
            partial = {t:v for t,v in assigned.items() if rng.randrange(2)}
            analyze(data,partial,color,totals)
            colored_graph = {v:{t for t in targets if t[0] == 'bp' or t[2] == color[v]}
                             for v,targets in graph.items()}
            result = analyze(data,matching(colored_graph),color,totals)
            assert result['collisions'] == [0,0]
            totals['abstract_systems'] += 1
            if trial < 3 and len(pairs) <= 2:
                for certificate in all_assignments(graph):
                    analyze(data,certificate,color,totals)
                    totals['exhaustively_checked_partial_certificates'] += 1
    # Two opposite-color assignments to ONE resource are legal and still
    # represent exactly ONE payment. This cannot use a one-tip certificate.
    kinds,pairs,_ = canonical(('A',))
    data = kinds,pairs,[],{0:{0}},{0}
    color = dict(zip(pairs[0],(0,1)))
    r = analyze(data,{('interval',0,0):pairs[0][0],('interval',0,1):pairs[0][1]},color,totals)
    assert (r['payment'],r['deficit'],r['holes'],r['collisions']) == (1,0,[0,0],[0,0])
    totals['opposite_color_double_slot_controls'] += 1


def main():
    ap = argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args = ap.parse_args()
    totals = Counter();abstract_checks(totals)
    print(json.dumps(dict(stage='abstract',counts=dict(totals))),flush=True)
    named = physical_checks(totals)
    assert totals['same_color_two_hole_components'] and totals['components_with_opposite_color_double_slot']
    assert totals['color_bound_strict_vs_global_hole_floor'] and totals['independent_primitive_comparisons'] == 12
    report = dict(status='PASS',counts=dict(totals),named=named,
        scope='General written colored two-slot compensation and signed collision identity; actual all-q frozen half-turn/shift same-color-hole maximum-certificate failure and distinct-unit/beta repairs. Finite controls do not establish arbitrary-grid saturation or improve universal 5/6.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals))),flush=True)


if __name__ == '__main__':main()
