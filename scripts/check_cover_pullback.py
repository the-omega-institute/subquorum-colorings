"""Literal-star controls for the triangle-free covering pullback theorem."""

import argparse
from collections import Counter
import json
from pathlib import Path
import random

from check_regular_starforming import bipartition, covered, graph_from_edges, masks, star_lists
from explore_heawood_two_lifts import exact_bipartite_dissociation, lift


def control(adjacency, generator, totals):
    order = len(adjacency)
    assert not any(adjacency[first] & adjacency[second]
                   for first in range(order) for second in adjacency[first])
    stars = star_lists(adjacency)
    adjacency_masks = masks(adjacency)
    forming = []
    proper = []
    minimal = []
    beta = 0
    for selection in range(1 << order):
        selected = {vertex for vertex in range(order) if selection >> vertex & 1}
        forming.append(all(covered(stars, selection, vertex) for vertex in range(order)
                           if vertex not in selected))
        proper.append(any(forming[selection ^ (1 << vertex)] or proper[selection ^ (1 << vertex)]
                          for vertex in selected))
        if all((adjacency_masks[vertex] & selection).bit_count() <= 1 for vertex in selected):
            beta = max(beta, len(selected))
        if forming[-1] and not proper[-1]:
            minimal.append(selected)
    if bipartition(adjacency) is not None:
        assert exact_bipartite_dissociation(adjacency)['beta'] == beta
        totals['independent_formula_optima'] += 1
    edges = {(vertex, neighbor) for vertex, neighbors in enumerate(adjacency)
             for neighbor in neighbors if vertex < neighbor}
    signs = [set(), {min(edges)} if edges else set(),
             {edge for edge in sorted(edges) if generator.randrange(2)}]
    for negative in signs:
        lifted = lift(adjacency, negative)
        lifted_stars = star_lists(lifted)
        for selected in minimal:
            pulled = selected | {order + vertex for vertex in selected}
            selection = sum(1 << vertex for vertex in pulled)
            assert all(covered(lifted_stars, selection, vertex)
                       for vertex in range(2 * order) if vertex not in pulled)
            for deleted in pulled:
                assert any(not covered(lifted_stars, selection ^ (1 << deleted), outside)
                           for outside in set(range(2 * order)) - (pulled - {deleted}))
                totals['literal_lifted_deletion_tests'] += 1
            totals['pulled_back_minimal_sets'] += 1
        totals['cover_instances'] += 1
    totals['base_graphs'] += 1
    totals['base_subsets'] += 1 << order
    return dict(order=order, base_minimal_sets=len(minimal), beta=beta)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    generator = random.Random(2026101906)
    totals = Counter()
    for left, right in [(2, 3), (3, 3)]:
        possible = [(first, left + second) for first in range(left) for second in range(right)]
        for edge_mask in range(1 << len(possible)):
            edges = [edge for position, edge in enumerate(possible) if edge_mask >> position & 1]
            control(graph_from_edges(left + right, edges), generator, totals)
    odd_examples = []
    for order in (5, 7):
        adjacency = graph_from_edges(order, [(vertex, (vertex + 1) % order) for vertex in range(order)])
        odd_examples.append(control(adjacency, generator, totals))
    petersen = [(vertex, (vertex + 1) % 5) for vertex in range(5)]
    petersen += [(vertex, 5 + vertex) for vertex in range(5)]
    petersen += [(5 + vertex, 5 + (vertex + 2) % 5) for vertex in range(5)]
    odd_examples.append(control(graph_from_edges(10, petersen), generator, totals))
    report = dict(scope='Literal-star minimality pullback controls on bipartite and nonbipartite triangle-free bases; independent full-subset checks of the one-part dissociation formula on small bipartite graphs. General proofs are separate.',
                  seed=2026101906, totals=dict(totals), nonbipartite_examples=odd_examples)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['totals']))


if __name__ == '__main__':
    main()
