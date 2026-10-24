"""Two-slot sufficiency controls and a fully frozen internal Hall obstruction.

Explicit geometry, independent strict-rank/strand reconstruction, exhaustive
base terminal cancellation, and finite controls. No SAT dependency. General
proofs and the all-copy construction are in FROZEN_TIP_SLOT_OBSTRUCTION.md.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_one_sided_interval_allocation import independent_maximum
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_normal_form import (
    brute, canonical, ordinary_flow, whole_support_data,
)

if not __debug__:
    raise RuntimeError('Run without -O; verification requires assertions.')

SELECTED = {
    (1,4),(2,3),(2,6),(2,8),(3,9),(4,2),(5,3),(6,2),(6,5),
    (6,9),(7,1),(7,4),(7,6),(7,8),(7,10),(8,3),(8,10),
    (6,11),(5,12),(7,13),(8,12),
}
MATCHING = [
    ((2,4),(3,4)),((3,5),(4,5)),((3,6),(4,6)),((3,7),(3,8)),
    ((4,3),(4,4)),((4,7),(5,7)),((5,6),(6,6)),((6,7),(6,8)),
    ((7,2),(7,3)),((6,12),(7,12)),
]
LAYERS = [
    [(2,4),(3,8),(4,3),(6,6),(6,8),(6,12),(7,2),(7,3),(7,12)],
    [(3,6),(5,7)],[(4,5),(4,6),(4,7)],
    [(3,4),(3,5),(3,7),(5,6)],[(4,4),(6,7)],
]
ALPHA = [(3,6),(4,6),(5,6),(6,6)]
DEAD_MIXED = [(6,7),(6,8)]
UPPER_MIXED = [(3,7),(3,8)]
BETA = [(3,5),(4,5)]


def fixture(copies=1, extra_columns=0):
    assert copies >= 1 and extra_columns >= 0 and extra_columns % 2 == 0
    move = lambda v, i: (v[0]+10*i,v[1])
    return (10*copies,16+extra_columns,
            {move(v,i) for i in range(copies) for v in SELECTED},
            [tuple(move(v,i) for v in edge) for i in range(copies) for edge in MATCHING])


def matching(adjacency):
    """Independent augmenting matching on explicitly named target identities."""
    assigned = {}
    def augment(v,seen):
        for target in sorted(adjacency[v],key=repr):
            if target in seen:
                continue
            seen.add(target)
            if target not in assigned or augment(assigned[target],seen):
                assigned[target] = v
                return True
        return False
    for v in sorted(adjacency,key=repr):
        augment(v,set())
    return assigned


def slot_graph(data, slots=2):
    kinds,pairs,links,support,_ = data
    owner,_,_,_ = owner_data(kinds,pairs)
    return {v: {('bp',w) for u,w in links if u == v} |
               {('interval',j,k) for j in support[owner[v]] for k in range(slots)}
            for v in kinds if kinds[v] == 'TP'}


def independent_strands(current,bands):
    """Actual endpoint graph, with separate matching and PP edge identities."""
    endpoints = {v for edge in current[3] for v in edge}
    edges = list(current[3])
    for columns in bands:
        edges.extend((a,b) for a,b in columns if a in endpoints and b in endpoints)
    adjacency = defaultdict(list)
    for i,(a,b) in enumerate(edges):
        adjacency[a].append((b,i));adjacency[b].append((a,i))
    partner = {a:b for columns in bands for col in columns for a,b in (col,col[::-1])}
    kinds = {v:'TP' if partner[v] in current[2] else 'BP'
             for v in endpoints if partner[v] not in endpoints}
    unseen = set(endpoints);components = []
    while unseen:
        start = min(unseen);body = {start};pending = [start]
        while pending:
            v = pending.pop()
            assert len(adjacency[v]) in (1,2)
            for w,_ in adjacency[v]:
                if w not in body:body.add(w);pending.append(w)
        unseen -= body
        tips = frozenset(v for v in body if len(adjacency[v]) == 1)
        assert len(tips) in (0,2)
        components.append((tips,body))
    return kinds,components


def inspect(current,bands,critical_pairs,totals):
    direct_check(*current)
    kinds0,components = independent_strands(current,bands)
    data,meta,_ = whole_support_data(current,bands)
    kinds,pairs,links,support,resources = data
    assert kinds == kinds0
    assert {frozenset(p) for p in pairs} == {tips for tips,_ in components if tips}
    owner,alphas,betas,mixed = owner_data(kinds,pairs)
    graph = slot_graph(data)
    hall = {v for pair in critical_pairs for v in pair}
    targets = set().union(*(graph[v] for v in hall))
    assert len(hall) == 2*len(critical_pairs) and len(targets) == len(critical_pairs)
    assert all(target[0] == 'bp' for target in targets)
    for x,y in critical_pairs:
        assert kinds[x] == kinds[y] == 'TP' and len(graph[x]) == 1 and graph[x] == graph[y]
        assert owner[x] in alphas and owner[y] in mixed
        assert not support[owner[x]] and not support[owner[y]]
        alpha = owner[x]
        other = next(v for v in pairs[alpha] if v != x)
        assert any(u == other and owner[w] in betas for u,w in links)
        assert any(u == x and owner[w] == owner[y] for u,w in links)
    assigned = matching(graph)
    assert len(graph)-len(assigned) == len(critical_pairs)
    flow = ordinary_flow(*data)
    q = len(critical_pairs)
    assert (len(alphas),len(betas),len(mixed)) == (q,q,4*q)
    assert (flow['value'],flow['cost'],flow['deficit']) == (q,q,0)
    assert not any(support[a] for a in alphas)  # zero links cannot pay any source
    totals['physical_systems'] += 1
    return dict(alpha=q,beta=q,mixed=4*q,tp_tips=len(graph),slot_matching=len(assigned),
                tip_hall_defect=q,ordinary_payment=q,minimum_link_cost=q,
                ordinary_deficit=0,intervals=len(resources),
                balance=meta['original']['balance'],boundary_budget=meta['original']['boundary_budget'])


def physical(totals):
    base = fixture()
    rank = check_rank_certificate(base,LAYERS)
    frozen,layers = frozen_certificate(base)
    assert len(frozen) == 20 and frozen == {v for e in MATCHING for v in e}
    data,meta,_ = whole_support_data(base,whole_bands(base))
    assert brute(*data) == ((1,1),60)
    totals['independent_base_terminal_matchings'] = 60
    # All TP subsets: exact maximum Hall defect, not merely the displayed witness.
    graph = slot_graph(data);tips = list(graph);max_defect = 0
    for mask in range(1<<len(tips)):
        subset = [v for i,v in enumerate(tips) if mask>>i&1]
        targets = set().union(*(graph[v] for v in subset)) if subset else set()
        max_defect = max(max_defect,len(subset)-len(targets))
        totals['base_hall_subsets'] += 1
    assert max_defect == 1
    records = []
    for q,extra in itertools.product(range(1,17),(0,2,10)):
        current = fixture(q,extra)
        transported = [[(r+10*i,c) for r,c in layer]
                       for layer in LAYERS for i in range(q)]
        # Copies have no cross-copy occupied adjacency. Equal ranks are valid
        # across copies; the flattened rank order is also a valid certificate.
        check_rank_certificate(current,transported)
        pairs = [((6+10*i,6),(6+10*i,8)) for i in range(q)]
        result = inspect(current,whole_bands(current),pairs,totals)
        records.append(dict(copies=q,extra_columns=extra,**result))
    # Carry the two-row bands through all eight square isometries. Re-pairing
    # rows after a rotation would test a different compensation model.
    for transpose,fr,fc in itertools.product((False,True),repeat=3):
        def move(v):
            r,c = v
            r = base[0]-1-r if fr else r
            c = base[1]-1-c if fc else c
            return (c,r) if transpose else (r,c)
        shape = base[:2][::-1] if transpose else base[:2]
        current = (*shape,{move(v) for v in base[2]},[tuple(map(move,e)) for e in base[3]])
        bands = [[tuple(map(move,col)) for col in columns] for columns in whole_bands(base)]
        check_rank_certificate(current,[[move(v) for v in layer] for layer in LAYERS])
        inspect(current,bands,[(move((6,6)),move((6,8)))],totals)
        totals['carried_band_isometries'] += 1
    return dict(selected=sorted(SELECTED),matching=MATCHING,rank_witnesses=rank,
                original_inventory={k:v for k,v in meta['original'].items() if k != 'components'},
                alpha=ALPHA,mixed=DEAD_MIXED,beta=BETA,upper_mixed=UPPER_MIXED,
                records=records)


def abstract_controls(totals):
    rng = random.Random(20261025)
    families = [('A',),('M',),('A','M'),('A','B'),('A','M','M'),
                ('A','B','M'),('A','A','M'),('A','A','B'),('A','B','M','M')]
    for types in families:
        for _ in range(120):
            kinds,pairs,possible = canonical(types)
            links = [edge for edge in possible if rng.randrange(2)]
            resources = set(range(rng.randrange(3)))
            support = {i:{j for j in resources if rng.randrange(2)} for i in range(len(pairs))}
            data = kinds,pairs,links,support,resources
            graph = slot_graph(data);assignment = matching(graph)
            flow = ordinary_flow(*data)
            totals['abstract_systems'] += 1
            if len(assignment) == len(graph):
                assert flow['deficit'] == 0
                # Lift the actual tip assignment, independently checking the
                # final-alpha allocation, rather than only comparing optima.
                selected = [(v,target[1]) for target,v in assignment.items() if target[0] == 'bp']
                from check_terminal_cancellation_and_stranded_demand import cancel_pairs
                _,inventory,components = cancel_pairs(kinds,pairs,selected,Counter())
                aa = [c for c in components if not c['cycle'] and c['alpha'] == c['beta']+1]
                slot_of = {v:target for target,v in assignment.items() if target[0] == 'interval'}
                incidence = {j:set() for j in resources}
                for i,c in enumerate(aa):
                    assert len(c['ends']) == 2 and all(v in slot_of for v in c['ends'])
                    for v in c['ends']:incidence[slot_of[v][1]].add(i)
                assert independent_maximum(len(aa),incidence) == len(aa)
                _,alphas,betas,_ = owner_data(kinds,pairs)
                assert len(betas)-inventory['BP','BP']+len(aa) == len(alphas)
                totals['actual_two_slot_lifts'] += 1
            elif flow['deficit'] == 0:
                totals['ordinary_complete_without_tip_certificate'] += 1
    # Three slots are already unsound, even with at most two owners per unit.
    kinds,pairs,links = canonical(('A','A','A'))
    support = {0:{0},1:{0,1},2:{1}};data = kinds,pairs,[],support,{0,1}
    assert len(matching(slot_graph(data,3))) == 6
    assert len(matching(slot_graph(data,2))) == 4
    assert ordinary_flow(*data)['value'] == 2
    totals['three_slot_unsound_controls'] = 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args = parser.parse_args();totals = Counter()
    evidence = physical(totals);abstract_controls(totals)
    result = dict(status='PASS',totals=dict(totals),physical=evidence,
                  scope='Explicit fully frozen physical counterexample to necessity of '
                  'two-slot TP Hall, alpha-reachable and PP-sealed against blank right padding. '
                  'General sufficiency and all-copy proof are written separately. '
                  'Finite checks do not prove universal geometric compensation or improve 5/6.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__ == '__main__':main()
