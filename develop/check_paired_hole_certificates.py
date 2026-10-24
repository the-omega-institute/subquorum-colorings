"""Exact partial-certificate defects and a frozen maximum-matching trap.

Original resources retain their identities. General arguments, as opposed to
the finite controls here, are in PAIRED_HOLES_AND_CERTIFICATE_OPTIMIZATION.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_tip_slot_obstruction import (
    fixture, LAYERS, matching, slot_graph, independent_strands,
)
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_partial_tip_compensation import components, lift, live_prune
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import (
    canonical, ordinary_flow, optimize, whole_support_data,
)

if not __debug__:
    raise RuntimeError('Run without -O; assertions are required.')


def all_assignments(graph):
    tips = sorted(graph, key=repr)
    def visit(i, assigned):
        if i == len(tips):
            yield dict(assigned)
            return
        yield from visit(i+1, assigned)
        for target in sorted(graph[tips[i]]-assigned.keys(), key=repr):
            assigned[target] = tips[i]
            yield from visit(i+1, assigned)
            del assigned[target]
    yield from visit(0, {})


def exact_check(data, assigned, totals):
    result = lift(data, assigned)
    kinds, pairs, _, _, resources = data
    selected = [(v,t[1]) for t,v in assigned.items() if t[0] == 'bp']
    _, _, records = cancel_pairs(kinds, pairs, selected, Counter())
    alphas = [c for c in records if not c['cycle'] and c['alpha'] == c['beta']+1]
    target_of = {v:t for t,v in assigned.items()}
    edges = [(('a',i),('i',target_of[v][1])) for i,c in enumerate(alphas)
             for v in c['ends'] if v in target_of]
    vertices = {('a',i) for i in range(len(alphas))}|{w for _,w in edges}
    deficit = 0
    for part in components(vertices, edges):
        aa = {i for tag,i in part if tag == 'a'}
        jj = {j for tag,j in part if tag == 'i'}
        e = sum(v in part for v,w in edges)
        h = sum(v not in target_of for i in aa for v in alphas[i]['ends'])
        assert e+h == 2*len(aa) and e <= 2*len(jj)
        assert len(aa)+len(jj) <= e+1  # connected incidence MULTIGRAPH
        assert h <= 2 and max(0,len(aa)-len(jj)) == h//2
        neighbours = {i:{w for v,w in edges if v == ('a',i)} for i in aa}
        actual = len(aa)-len(matching(neighbours))
        assert actual == h//2
        deficit += actual
        totals['exact_components'] += 1
    assert deficit == result['final_component_budget'] == result['certified_deficit']
    # Independent augmented strand model: each original interval is ONE beta
    # with two labelled BP ends, not two independently spendable resources.
    kk = {('original',v):k for v,k in kinds.items()}
    pp = [tuple(('original',v) for v in pair) for pair in pairs]
    for j in sorted(resources):
        pair = (('slot',j,0),('slot',j,1))
        pp.append(pair)
        kk.update({v:'BP' for v in pair})
    links = [(('original',v), ('original',t[1]) if t[0] == 'bp'
              else ('slot',t[1],t[2])) for t,v in assigned.items()]
    _, inventory, _ = cancel_pairs(kk, pp, links, Counter())
    assert inventory['TP','TP'] == deficit
    totals['certificates'] += 1
    return result


def packing_certificate(data):
    """Sparse certificate extracted from an independently optimized packing."""
    kinds,pairs,_,support,_ = data
    packed = optimize(*data, allow_forks=False)
    assigned = {('bp',w):v for stem in packed['certificates'] for v,w in stem['links']}
    occupied = {v for stem in packed['certificates'] for edge in stem['links'] for v in edge}
    for stem in packed['certificates']:
        if stem['kind'] == 'interval':
            witness = stem['witness']
            v = next(v for v in pairs[witness] if kinds[v] == 'TP' and v not in occupied)
            j = stem['interval']
            assert j in support[witness]
            assigned['interval',j,0] = v
    return assigned, packed


def greedy_extend(data, assigned, totals):
    assigned = dict(assigned)
    graph = slot_graph(data)
    old = exact_check(data, assigned, totals)['final_component_budget']
    for v in sorted(graph, key=repr):
        if v in assigned.values():
            continue
        free = graph[v]-assigned.keys()
        if free:
            assigned[min(free,key=repr)] = v
            new = exact_check(data, assigned, totals)['final_component_budget']
            assert new <= old
            old = new
            totals['monotone_direct_extensions'] += 1
    assert all(v in assigned.values() or graph[v] <= assigned.keys() for v in graph)
    return assigned


def abstract(totals):
    rng = random.Random(2026102542)
    families = [('A',),('A','A'),('A','M'),('A','B'),('A','A','M'),
                ('A','B','M'),('A','B','M','M'),('A','A','B','M')]
    for types in families:
        for trial in range(50):
            kinds,pairs,possible = canonical(types)
            links = [e for e in possible if rng.randrange(3) == 0]
            rr = set(range(rng.randrange(3)))
            support = {o:{j for j in rr if rng.randrange(2)} for o in range(len(pairs))}
            data = kinds,pairs,links,support,rr
            assigned, packed = packing_certificate(data)
            expected = len(owner_data(kinds,pairs)[1])-packed['value']
            assert ordinary_flow(*data)['deficit'] == expected
            assert exact_check(data,assigned,totals)['final_component_budget'] == expected
            extended = greedy_extend(data,assigned,totals)
            assert exact_check(data,extended,totals)['final_component_budget'] == expected
            exact_check(data,matching(slot_graph(data)),totals)
            if trial < 4:
                best = len(owner_data(kinds,pairs)[1])
                for candidate in all_assignments(slot_graph(data)):
                    b = exact_check(data,candidate,totals)['final_component_budget']
                    best = min(best,b)
                assert best == expected
                totals['exhaustive_certificate_systems'] += 1
            totals['abstract_systems'] += 1
    # Unique maximum terminal matching is strictly worse than a smaller one.
    kinds,pairs,_ = canonical(('A','B','M','M'))
    trap = kinds,pairs,[(0,2),(5,2),(0,6)],{i:set() for i in range(4)},set()
    assignments = list(all_assignments(slot_graph(trap)))
    maxima = [a for a in assignments if len(a) == 2]
    assert len(maxima) == 1 and maxima[0] == {('bp',2):5,('bp',6):0}
    assert exact_check(trap,maxima[0],totals)['final_component_budget'] == 1
    smaller = {('bp',2):0}
    assert exact_check(trap,smaller,totals)['final_component_budget'] == 0
    extended = greedy_extend(trap,smaller,totals)
    assert extended == smaller and ordinary_flow(*trap)['deficit'] == 0
    pruned,meta = live_prune(trap)
    assert len(meta['removed_mixed']) == 2
    assert exact_check(pruned,matching(slot_graph(pruned)),totals)['final_component_budget'] == 0
    # General q-copy gap is proved in the note; these are finite checks.
    for q in range(1,17):
        kinds,pairs,_ = canonical(('A','B','M','M')*q)
        links = [(v+8*i,w+8*i) for i in range(q) for v,w in trap[2]]
        data = kinds,pairs,links,{i:set() for i in range(4*q)},set()
        maximum = matching(slot_graph(data))
        assert len(maximum) == 2*q
        assert exact_check(data,maximum,totals)['final_component_budget'] == q
        assert ordinary_flow(*data)['deficit'] == 0
        totals['unique_maximum_trap_copies'] += 1


def paired_fixture(copies=1,width=30,padding=0):
    assert copies >= 1 and width >= 30 and width%2 == 0 and padding >= 0 and padding%2 == 0
    base = fixture()
    maps = [lambda v,i=i,reflect=reflect:
            (v[0]+10*i,width-1-v[1] if reflect else v[1])
            for i in range(copies) for reflect in (False,True)]
    current = (10*copies,width+padding,
        set().union(*({move(v) for v in base[2]} for move in maps)),
        [tuple(map(move,e)) for move in maps for e in base[3]])
    layers = [[move(v) for move in maps for v in layer] for layer in LAYERS]
    return current,layers


def physical_one(current,bands,layers,copies,width,point,totals):
    direct_check(*current)
    check_rank_certificate(current,layers)
    assert len(frozen_certificate(current)[0]) == 40*copies
    data,meta,_ = whole_support_data(current,bands)
    independent_kinds,independent = independent_strands(current,bands)
    assert independent_kinds == data[0]
    assert {frozenset(p) for p in data[1]} == {tips for tips,body in independent if tips}
    data,removed = live_prune(data)
    owner,aa,bb,mm = owner_data(*data[:2])
    assert (len(aa),len(bb),len(mm)) == (2*copies,2*copies,2*copies)
    graph = slot_graph(data)
    bad = {}; good = {}; scarce = set(); selected = []
    for i in range(copies):
        a,b = point((3+10*i,6)),point((3+10*i,width-7))
        left,right = point((3+10*i,8)),point((3+10*i,width-9))
        assert not graph[point((6+10*i,6))] and not graph[point((6+10*i,width-7))]
        shared = sorted(data[3][owner[left]] & data[3][owner[right]])
        assert len(shared) == width-20  # distinct BB units in the SAME original gap
        j,k = shared[:2]
        scarce.add(j)
        for v,w in ((a,point((3+10*i,7))),(b,point((3+10*i,width-8)))):
            assert ('bp',w) in graph[v]
            bad['bp',w] = v
            good['bp',w] = v
            selected.append((v,w))
        bad['interval',j,0] = left
        bad['interval',j,1] = right
        good['interval',j,0] = left
        good['interval',k,0] = right
    assert len(bad) == len(good) == len(matching(graph)) == 4*copies
    bad_result = exact_check(data,bad,totals)
    good_result = exact_check(data,good,totals)
    assert (bad_result['holes'],bad_result['final_component_budget']) == (2*copies,copies)
    assert bad_result['interaction_budget'] == copies
    assert good_result['final_component_budget'] == 0
    assert all(x['alpha'] == 2 and x['holes'] == 2 for x in bad_result['interactions'] if x['alpha'])
    assert ordinary_flow(*data)['value'] == 2*copies
    assert ordinary_flow(*data)['cost'] == 2*copies
    # Hold the productive A->R links fixed. Two genuinely distinct intervals
    # repair the certificate; this does not spend either whole beta.
    restricted = data[:2]+(selected,)+data[3:]
    assert ordinary_flow(*restricted)['value'] == 2*copies
    k,p,l,s,r = restricted
    scarce_data = k,p,l,{o:units&scarce for o,units in s.items()},scarce
    assert ordinary_flow(*scarce_data)['deficit'] == copies
    # Restoring ALL original links restores beta payments, even with the same
    # scarce resources. This is NOT a frozen-grid inequality counterexample.
    restored = k,p,data[2],scarce_data[3],scarce
    assert ordinary_flow(*restored)['deficit'] == 0
    totals['physical_systems'] += 1
    return dict(copies=copies,width=width,maximum_tip_matching=4*copies,
        holes=2*copies,alpha_component_holes=2,bad_certificate_deficit=copies,
        repaired_certificate_deficit=0,actual_payment=2*copies,
        minimum_links=2*copies,shared_units_per_pair=width-20,
        scarce_fixed_link_deficit=copies,restored_link_deficit=0,
        removed_mixed=len(removed['removed_mixed']))


def physical(totals):
    records = []
    for q,width,padding in itertools.product(range(1,9),(30,32,40),(0,2,10)):
        current,layers = paired_fixture(q,width,padding)
        result = physical_one(current,whole_bands(current),layers,q,width,lambda v:v,totals)
        records.append(dict(padding=padding,**result))
    base,layers = paired_fixture()
    for transpose,fr,fc in itertools.product((False,True),repeat=3):
        def point(v):
            r,c = v
            r = base[0]-1-r if fr else r
            c = base[1]-1-c if fc else c
            return (c,r) if transpose else (r,c)
        shape = base[:2][::-1] if transpose else base[:2]
        current = (*shape,{point(v) for v in base[2]},[tuple(map(point,e)) for e in base[3]])
        bands = [[tuple(map(point,col)) for col in band] for band in whole_bands(base)]
        physical_one(current,bands,[[point(v) for v in layer] for layer in layers],1,30,point,totals)
        totals['carried_band_isometries'] += 1
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args()
    totals = Counter()
    abstract(totals)
    records = physical(totals)
    result = dict(status='PASS',totals=dict(totals),physical=records,
        scope='Written general exact-budget, sparse completeness and monotone direct-extension proofs; '
        'explicit abstract unique-maximum trap and actual frozen paired-hole traps. '
        'No universal frozen-grid compensation or 5/6 improvement; no exhaustive claim beyond named small systems.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__ == '__main__':
    main()
