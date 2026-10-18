"""Independent literal-star controls for the exact cover-stability criterion."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random

from check_regular_starforming import covered, graph_from_edges, star_lists
from explore_heawood_two_lifts import lift


def forms(stars, selected):
    selection = sum(1 << vertex for vertex in selected)
    return all(covered(stars, selection, outside)
               for outside in range(len(stars)) if outside not in selected)


def minimal_sets(adjacency):
    stars = star_lists(adjacency)
    forming = []
    proper = []
    minimal = []
    for selection in range(1 << len(adjacency)):
        selected = {vertex for vertex in range(len(adjacency)) if selection >> vertex & 1}
        forming.append(forms(stars, selected))
        proper.append(any(forming[selection ^ (1 << vertex)] or proper[selection ^ (1 << vertex)]
                          for vertex in selected))
        if forming[-1] and not proper[-1]:
            minimal.append(selected)
    return minimal


def certificates(adjacency, selected):
    stars = star_lists(adjacency)
    selection = sum(1 << vertex for vertex in selected)
    outside = set(range(len(adjacency))) - selected
    result = {}
    for deleted in selected:
        smaller = selection ^ (1 << deleted)
        self_failure = not covered(stars, smaller, deleted)
        failures = [vertex for vertex in outside if not covered(stars, smaller, vertex)]
        safe = [vertex for vertex in failures
                if deleted not in adjacency[vertex] or
                not any(deleted in adjacency[center] for center in adjacency[vertex] & selected)]
        result[deleted] = dict(self_failure=self_failure, safe_outside=safe,
                               all_outside_failures=failures)
    return result


def check_canonical(adjacency, selected, deleted, certificate, totals):
    outside = set(range(len(adjacency))) - selected
    negative = {tuple(sorted((deleted, vertex))) for vertex in adjacency[deleted] & outside}
    lifted = lift(adjacency, negative)
    for vertex, neighbors in enumerate(lifted):
        projected = [neighbor % len(adjacency) for neighbor in neighbors]
        assert len(projected) == len(set(projected))
        assert set(projected) == adjacency[vertex % len(adjacency)]
    pulled = selected | {len(adjacency) + vertex for vertex in selected}
    assert forms(star_lists(lifted), pulled - {deleted})
    assert not certificate['self_failure'] and not certificate['safe_outside']
    assert certificate['all_outside_failures']
    for failed in certificate['all_outside_failures']:
        assert deleted in adjacency[failed]
        others = adjacency[failed] & (selected - {deleted})
        assert len(others) == 1
        support = next(iter(others))
        assert adjacency[support] & selected == {deleted}
    reached = {0}
    pending = [0]
    while pending:
        for neighbor in adjacency[pending.pop()] - reached:
            reached.add(neighbor)
            pending.append(neighbor)
    if len(reached) == len(adjacency):
        reached = {0}
        pending = [0]
        while pending:
            for neighbor in lifted[pending.pop()] - reached:
                reached.add(neighbor)
                pending.append(neighbor)
        assert len(reached) == len(lifted)
        totals['connected_countercovers'] += 1
    totals['canonical_nonminimal_pullbacks'] += 1


def graph_control(adjacency, generator, totals, exhaustive_signs=False, supplied=None):
    selections = minimal_sets(adjacency) if supplied is None else [supplied]
    stars = star_lists(adjacency)
    data = []
    for selected in selections:
        assert forms(stars, selected)
        assert all(not forms(stars, selected - {deleted}) for deleted in selected)
        certificate_map = certificates(adjacency, selected)
        unstable = [vertex for vertex, certificate in certificate_map.items()
                    if not certificate['self_failure'] and not certificate['safe_outside']]
        for vertex in unstable:
            check_canonical(adjacency, selected, vertex, certificate_map[vertex], totals)
        data.append((selected, not unstable))
        totals['minimal_selections'] += 1
        totals['certificate_stable_selections'] += not unstable
    edges = [(vertex, neighbor) for vertex, neighbors in enumerate(adjacency)
             for neighbor in sorted(neighbors) if vertex < neighbor]
    if exhaustive_signs:
        signatures = range(1 << len(edges))
    else:
        signatures = {0, generator.randrange(1 << len(edges)), generator.randrange(1 << len(edges))}
    surviving = [True] * len(data)
    for signature in signatures:
        negative = {edge for position, edge in enumerate(edges) if signature >> position & 1}
        lifted = lift(adjacency, negative)
        lifted_stars = star_lists(lifted)
        for position, (selected, stable) in enumerate(data):
            pulled = selected | {len(adjacency) + vertex for vertex in selected}
            assert forms(lifted_stars, pulled)
            minimal = all(not forms(lifted_stars, pulled - {deleted}) for deleted in pulled)
            if stable:
                assert minimal
            surviving[position] &= minimal
            totals['tested_pullbacks'] += 1
            totals['tested_nonminimal_pullbacks'] += not minimal
        totals['cover_instances'] += 1
    if exhaustive_signs:
        assert surviving == [stable for selected, stable in data]
        totals['all_signs_base_graphs'] += 1
    totals['base_graphs'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    generator = random.Random(2026101907)
    totals = Counter()
    for order in range(1, 6):
        possible = list(combinations(range(order), 2))
        for edge_mask in range(1 << len(possible)):
            edges = [edge for position, edge in enumerate(possible) if edge_mask >> position & 1]
            graph_control(graph_from_edges(order, edges), generator, totals, exhaustive_signs=order <= 4)
    for order in (7, 8, 9):
        for trial in range(30):
            edges = [edge for edge in combinations(range(order), 2) if generator.randrange(2)]
            graph_control(graph_from_edges(order, edges), generator, totals)
    obstruction_examples = []
    for leaves in range(2, 8):
        for signature in range(1, 1 << leaves):
            triangular = [vertex for vertex in range(leaves) if signature >> vertex & 1]
            isolate = leaves + 1
            private_offset = leaves + 2
            triangle_offset = 2 * leaves + 2
            edges = [(0, 1 + vertex) for vertex in range(leaves)]
            edges += [(1 + vertex, private_offset + vertex) for vertex in range(leaves)]
            edges += [(isolate, private_offset + vertex) for vertex in range(leaves)]
            edges += [(0, triangle_offset + position) for position in range(len(triangular))]
            edges += [(1 + vertex, triangle_offset + position)
                      for position, vertex in enumerate(triangular)]
            adjacency = graph_from_edges(triangle_offset + len(triangular), edges)
            selected = set(range(leaves + 2))
            graph_control(adjacency, generator, totals, supplied=selected)
            certificate_map = certificates(adjacency, selected)
            assert [vertex for vertex, certificate in certificate_map.items()
                    if not certificate['self_failure'] and not certificate['safe_outside']] == [0]
            obstruction_examples.append(dict(leaves=leaves, triangles=len(triangular), order=len(adjacency)))
    report = dict(scope='Controls only; general safe-certificate equivalence, canonical counter-cover and connectedness have separate written proofs. All graph-cover sufficiency and boundary corollaries additionally have Lean proofs.',
                  seed=2026101907, totals=dict(totals), obstruction_examples=obstruction_examples)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['totals']))


if __name__ == '__main__':
    main()
