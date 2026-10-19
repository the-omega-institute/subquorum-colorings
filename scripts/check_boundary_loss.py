"""Independent small-graph controls for exported private-clause ownership."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from check_bare_heawood_ports import PHASE, FULL_WITNESS
from check_long_core_words import translate, word_control
from check_starforming_gap import forms
from explore_long_core_SF import clauses, graph


def private_owners(adjacency, selected):
    owners = set()
    for clause in clauses(adjacency):
        intersection = clause & selected
        if len(intersection) == 1:
            owners |= intersection
    return owners


def export_control(adjacency, selected, inside, core, ports):
    restricted = selected & core
    unsupported = restricted - ports - private_owners(inside, restricted)
    outside_owners = {}
    certificates = {}
    for owner in sorted(unsupported):
        candidates = []
        for boundary in restricted & ports:
            if inside[boundary] & restricted != {owner}:
                continue
            for outside in adjacency[boundary] - inside[boundary]:
                if outside in selected or adjacency[outside] & selected != {boundary}:
                    continue
                candidates.append((boundary, outside))
                if outside in outside_owners:
                    assert outside_owners[outside] == owner
                outside_owners[outside] = owner
        assert candidates, (sorted(selected), sorted(core), owner)
        certificates[owner] = sorted(candidates)
    assert len(unsupported) <= len(outside_owners)
    return certificates


def small_controls():
    totals = Counter()
    example = None
    for order in range(6):
        vertices = set(range(order))
        edges = list(combinations(range(order), 2))
        for edge_mask in range(1 << len(edges)):
            adjacency = [set() for vertex in vertices]
            for index, (first, second) in enumerate(edges):
                if edge_mask >> index & 1:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
            totals['graphs'] += 1
            minimal_sets = []
            for selection_mask in range(1 << order):
                selected = {vertex for vertex in vertices if selection_mask >> vertex & 1}
                if forms(adjacency, selected) and all(not forms(adjacency, selected - {vertex})
                                                      for vertex in selected):
                    minimal_sets.append(selected)
            totals['minimal_sets'] += len(minimal_sets)
            for core_mask in range(1 << order):
                core = {vertex for vertex in vertices if core_mask >> vertex & 1}
                inside = [neighbors & core if vertex in core else set()
                          for vertex, neighbors in enumerate(adjacency)]
                ports = {vertex for vertex in core if adjacency[vertex] - core}
                for selected in minimal_sets:
                    certificates = export_control(adjacency, selected, inside, core, ports)
                    totals['core_selection_instances'] += 1
                    totals['exported_owners'] += len(certificates)
                    if certificates and example is None:
                        example = dict(adjacency=[sorted(neighbors) for neighbors in adjacency],
                                       selected=sorted(selected), core=sorted(core),
                                       ports=sorted(ports), exports=certificates)
    assert totals['graphs'] == 1100 and example is not None
    return dict(totals=totals, first_nonvacuous_example=example,
                scope='All simple labeled graphs of order at most five, every induced core and every inclusion-minimal forming selection. The general proof also permits added port-to-port edges; this finite family does not exhaust those internal edge omissions.')


def fixed_private_budget():
    adjacency, pairs, _, _ = word_control('B')
    port_mask = sum(1 << vertex for pair in pairs for vertex in pair)
    clause_masks = [sum(1 << vertex for vertex in clause) for clause in clauses(adjacency)]
    maximum = -1
    example = None
    for selection in range(1 << 20):
        if selection.bit_count() <= maximum:
            continue
        owners = 0
        for clause in clause_masks:
            intersection = selection & clause
            if intersection and not intersection & (intersection - 1):
                owners |= intersection
        score = ((owners | port_mask) & selection).bit_count()
        if score > maximum:
            maximum, example = score, selection
    assert maximum == 12
    return dict(k=1, conceptual_subsets=1 << 20,
                maximum_selected_ports_plus_private_nonports=maximum,
                attaining_selected=[vertex for vertex in range(20) if example >> vertex & 1],
                pruning='Selections of cardinality at most current maximum cannot improve the score.',
                all_k_extension='Refuted at k2, even with an internally forming core; see output/bare-port-only-obstruction.json.',
                scope='Finite discovery only. No all-k partial private-owner cap is inferred.')


def long_core_control():
    adjacency, _ = graph(2)
    inside_core, pairs, _, _ = word_control('BB')
    inside = inside_core + [set() for vertex in range(84)]
    ports = {vertex for pair in pairs for vertex in pair}
    chosen = {translate(2, block, local) for block in range(2) for local in PHASE[block]}
    assert FULL_WITNESS & set(range(40)) == chosen
    exports = export_control(adjacency, FULL_WITNESS, inside, set(range(40)), ports)
    assert set(exports) == {22}
    return dict(order=124, selected_size=62, core_size=25, exports=exports)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED', small_graphs=small_controls(),
                  fixed_core_private_budget=fixed_private_budget(),
                  nonvacuous_long_core=long_core_control(),
                  scope='Finite independent controls of the general written and Lean export and unique-ownership theorems. The k1 core budget is only a discovery lead.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], small_graphs=report['small_graphs']['totals'],
                         fixed_core_budget=report['fixed_core_private_budget']['maximum_selected_ports_plus_private_nonports'],
                         long_core_exports=report['nonvacuous_long_core']['exports'])))


if __name__ == '__main__':
    main()
