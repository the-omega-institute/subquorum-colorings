"""Independent literal-star controls for protected-port return certificates."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random

from check_cubic_starforming import base, star_masks
from check_exact_cubic import robust_deletions
from check_saturated_heawood_transfer import templates
from explore_long_core_SF import verify_literal


def shapes(adjacency, selected, deleted, outside):
    neighbors = adjacency[outside] & selected
    if neighbors == {deleted}:
        return 'direct'
    if deleted in neighbors and len(neighbors) == 2:
        other = next(iter(neighbors - {deleted}))
        if adjacency[other] & selected <= {deleted}:
            return 'split'
    if deleted not in neighbors and len(neighbors) == 1:
        support = next(iter(neighbors))
        if adjacency[support] & selected == {deleted}:
            return 'relay'
    return None


def literal_at(containing, selected, outside):
    available = sum(1 << vertex for vertex in selected | {outside})
    return any(star & available == star for star in containing[outside])


def containing_stars(adjacency):
    stars = star_masks(adjacency)
    return [[star for star in stars if star >> vertex & 1]
            for vertex in range(len(adjacency))]


def graph_controls(adjacency, counts):
    counts['graphs'] += 1
    order = len(adjacency)
    vertices = set(range(order))
    containing = containing_stars(adjacency)
    selections = [{vertex for vertex in vertices if mask >> vertex & 1}
                  for mask in range(1 << order)]
    forming = [all(literal_at(containing, selected, outside)
                   for outside in vertices - selected) for selected in selections]
    for mask, selected in enumerate(selections):
        if not forming[mask]:
            continue
        counts['forming_selections'] += 1
        failures = {}
        for deleted in selected:
            failures[deleted] = set()
            for outside in vertices - selected:
                failure = not literal_at(containing, selected - {deleted}, outside)
                shape = shapes(adjacency, selected, deleted, outside)
                assert failure == (shape is not None)
                counts['failure_shape_comparisons'] += 1
                if failure:
                    counts['failure_' + shape] += 1
                    failures[deleted].add(outside)
        if any(forming[mask ^ (1 << vertex)] for vertex in selected):
            continue
        counts['minimal_selections'] += 1
        high = {vertex for vertex in selected if len(adjacency[vertex] & selected) >= 2}
        for first, second in combinations(high, 2):
            assert not failures[first] & failures[second]
            counts['high_failure_disjointness'] += 1
        for port in high:
            assert failures[port]
            for exit_vertex in adjacency[port]:
                core = {exit_vertex} | (adjacency[exit_vertex] - {port})
                block = vertices - core
                if port not in block or adjacency[port] - block != {exit_vertex}:
                    continue
                internal_neighbors = adjacency[port] & block
                if any(not literal_at(containing, selected - {port}, outside)
                       for outside in internal_neighbors - selected):
                    continue
                if any(not (adjacency[neighbor] & (selected - {port}))
                       for neighbor in internal_neighbors & selected):
                    continue
                assert failures[port] <= core
                for outside in failures[port]:
                    if outside != exit_vertex:
                        assert shapes(adjacency, selected, port, outside) == 'relay'
                        assert adjacency[outside] & selected == {exit_vertex}
                        assert adjacency[exit_vertex] & selected == {port}
                    counts['protected_return_witnesses'] += 1
                counts['protected_ports'] += 1


def general_controls():
    counts = Counter()
    for order in range(1, 6):
        edges = list(combinations(range(order), 2))
        for mask in range(1 << len(edges)):
            adjacency = [set() for vertex in range(order)]
            for index, (first, second) in enumerate(edges):
                if mask >> index & 1:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
            graph_controls(adjacency, counts)
    generator = random.Random(19102026)
    for order in range(6, 10):
        for sample in range(12):
            adjacency = [set() for vertex in range(order)]
            for first, second in combinations(range(order), 2):
                if generator.random() < (0.25, 0.5, 0.75)[sample % 3]:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
            graph_controls(adjacency, counts)
    return counts


def ambient_controls():
    heawood = base()
    broken = [set(neighbors) for neighbors in heawood]
    broken[0].remove(8)
    broken[8].remove(0)
    records = []
    for template in templates(heawood, broken):
        port, incoming_port = template['signal_port'], template['omitted_port']
        internal = set(template['selected'])
        assert robust_deletions(broken, internal) == {port}
        assert len(broken[port]) == 2 and broken[port] <= internal
        assert all(adjacency_other & (internal - {port})
                   for neighbor in broken[port] for adjacency_other in [broken[neighbor]])
        for kind in ('direct', 'split', 'relay'):
            order = 16 if kind == 'direct' else 17
            adjacency = [set(neighbors) for neighbors in broken]
            adjacency += [set() for vertex in range(14, order)]
            edges = [(port, 14), (incoming_port, 15)]
            if kind != 'direct':
                edges.append((14, 16))
            for first, second in edges:
                adjacency[first].add(second)
                adjacency[second].add(first)
            selected = internal | {15}
            if kind == 'split':
                selected.add(16)
            elif kind == 'relay':
                selected.add(14)
            deletion_checks = verify_literal(adjacency, selected)
            containing = containing_stars(adjacency)
            failures = {outside for outside in set(range(order)) - selected
                        if not literal_at(containing, selected - {port}, outside)}
            assert failures == ({16} if kind == 'relay' else {14})
            terminal = next(iter(failures))
            assert shapes(adjacency, selected, port, terminal) == kind
            records.append(dict(kind=kind, omitted_port=incoming_port, signal_port=port,
                                order=order, extra_edges=edges, selected=sorted(selected),
                                return_witness=terminal,
                                selected_neighbors_of_exit=sorted(adjacency[14] & selected),
                                selected_neighbors_of_witness=sorted(adjacency[terminal] & selected),
                                literal_deletion_checks=deletion_checks))
    assert len(records) == 24
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    general = general_controls()
    ambient = ambient_controls()
    report = dict(status='ALL_CHECKS_PASSED', general=general,
                  ambient_examples=ambient,
                  ambient_literal_deletions=sum(row['literal_deletion_checks'] for row in ambient),
                  scope='General failure equivalence, protected-port localization and high-port '
                        'witness uniqueness are proved in Lean for arbitrary vertex types. These '
                        'literal-star controls test all labeled graphs through order five, '
                        '48 deterministic larger samples and all eight Fano templates with '
                        'three actual minimal ambient return shapes each. The long-core '
                        'geometry and global count remain separate written deductions/open work.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], general=general,
                         ambient_examples=len(ambient),
                         ambient_literal_deletions=report['ambient_literal_deletions'])))


if __name__ == '__main__':
    main()
