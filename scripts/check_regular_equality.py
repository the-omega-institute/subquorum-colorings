"""Independent controls for isolate-tight regular structure and equality."""

import argparse
from collections import Counter
import json
from pathlib import Path

from check_regular_compensation import exchange_control, sharp_family
from check_regular_starforming import bipartition, covered, graph_from_edges, masks, sharp_graph, star_lists


def structure_control(adjacency, selected, totals, exact_beta=None):
    degree = len(adjacency[0])
    assert degree >= 3 and all(len(neighbors) == degree for neighbors in adjacency)
    control = exchange_control(adjacency, selected, totals, exact_beta)
    colors = bipartition(adjacency)
    counts = [len(neighbors & selected) for neighbors in adjacency]
    outside = set(range(len(adjacency))) - selected
    isolated = {vertex for vertex in selected if counts[vertex] == 0}
    defect = degree * len(adjacency) - (2 * degree - 1) * len(selected)
    linear = degree * len(adjacency) + 2 * exact_beta - (2 * degree + 1) * len(selected) if exact_beta is not None else None
    if degree >= 4 and linear == 0:
        assert defect == len(isolated)
        assert control['exchange_sizes'] == [exact_beta, exact_beta]
        totals['linear_equality_selections'] += 1
    if defect != len(isolated):
        return
    high = {vertex for vertex in selected if counts[vertex] >= 2}
    leaves = {vertex for vertex in selected if counts[vertex] == 1 and adjacency[vertex] & high}
    paired = selected - isolated - high - leaves
    partial = {vertex for vertex in high if counts[vertex] == degree - 1}
    full = {vertex for vertex in high if counts[vertex] == degree}
    private = {vertex for vertex in outside if counts[vertex] == 1}
    double = {vertex for vertex in outside if counts[vertex] == 2}
    saturated = {vertex for vertex in outside if counts[vertex] == degree}
    assert high == partial | full
    assert outside == private | double | saturated
    assert len(full) == len(leaves) == len(private)
    assert len(partial) == len(double)
    assert all(len(adjacency[vertex] & high) == degree - 1 for vertex in high)
    assert all(len(adjacency[vertex] & leaves) == 1 for vertex in full | private)
    assert all(len(adjacency[vertex] & full) == len(adjacency[vertex] & private) == 1 and
               len(adjacency[vertex] & saturated) == degree - 2 for vertex in leaves)
    assert all(len(adjacency[vertex] & double) == 1 for vertex in partial)
    assert all(len(adjacency[vertex] & partial) == len(adjacency[vertex] & isolated) == 1 for vertex in double)
    assert all(adjacency[vertex] <= double | saturated for vertex in isolated)
    assert all(len(adjacency[vertex] & paired) == 1 and
               len(adjacency[vertex] & saturated) == degree - 1 for vertex in paired)
    assert all(adjacency[vertex] <= isolated | paired | leaves for vertex in saturated)
    assert all(len(adjacency[vertex] & outside) == degree - counts[vertex] for vertex in private | double)
    for high_class in (partial, full):
        assert 2 * sum(colors[vertex] == 0 for vertex in high_class) == len(high_class)
    isolate_counts = [sum(colors[vertex] == color for vertex in isolated) for color in (0, 1)]
    assert len(partial) <= 2 * degree * min(isolate_counts)
    assert sorted(control['exchange_sizes']) == sorted(len(selected) - count for count in isolate_counts)
    if exact_beta is not None:
        assert linear >= abs(isolate_counts[0] - isolate_counts[1])
        assert linear == abs(isolate_counts[0] - isolate_counts[1]) + 2 * (
            exact_beta - max(control['exchange_sizes']))
    totals['isolate_tight_selections'] += 1
    totals['tight_with_high_leaves'] += bool(full)
    totals['tight_with_matching'] += bool(paired)
    totals['tight_with_bad_highs'] += bool(partial)


def exhaustive_control(adjacency, totals):
    stars = star_lists(adjacency)
    adjacency_masks = masks(adjacency)
    order = len(adjacency)
    forming = []
    proper = []
    minimal = []
    beta = 0
    for selection in range(1 << order):
        selected = {vertex for vertex in range(order) if selection >> vertex & 1}
        forming.append(all(covered(stars, selection, vertex) for vertex in range(order)
                           if not selection >> vertex & 1))
        proper.append(any(forming[selection ^ (1 << vertex)] or
                          proper[selection ^ (1 << vertex)] for vertex in selected))
        if all((adjacency_masks[vertex] & selection).bit_count() <= 1 for vertex in selected):
            beta = max(beta, len(selected))
        if forming[-1] and not proper[-1]:
            minimal.append(selected)
    for selected in minimal:
        structure_control(adjacency, selected, totals, beta)
    totals['exact_graphs'] += 1
    totals['subsets'] += 1 << order
    return dict(order=order, degree=len(adjacency[0]), beta=beta, minimal_count=len(minimal))


def high_corona(degree):
    edges = [(first, degree + second) for first in range(degree)
             for second in range(degree) if first != second]
    edges += [(4 * degree + first, 5 * degree + second) for first in range(degree)
              for second in range(degree) if first != second]
    for vertex in range(2 * degree):
        edges += [(vertex, 2 * degree + vertex), (2 * degree + vertex, 4 * degree + vertex)]
        offset = 6 * degree if vertex < degree else 7 * degree - 2
        edges += [(2 * degree + vertex, offset + neighbor) for neighbor in range(degree - 2)]
    return graph_from_edges(8 * degree - 4, edges), set(range(4 * degree))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    graphs = []
    for degree in (3, 4):
        for builder in (sharp_graph, sharp_family):
            adjacency, selected = builder(degree)
            graphs.append(exhaustive_control(adjacency, totals))
    examples = []
    balanced_obstacles = []
    for degree in range(3, 11):
        for name, builder, beta in [('isolated_crown', sharp_family, 2 * degree + 1),
                                    ('matching_equality', sharp_graph, 2 * degree),
                                    ('high_leaf_equality', high_corona, 4 * degree)]:
            adjacency, selected = builder(degree)
            structure_control(adjacency, selected, totals, beta)
            examples.append(dict(degree=degree, family=name, order=len(adjacency), selected=len(selected)))
        edges = [(offset + first, offset + degree + second)
                 for offset in (0, 2 * degree)
                 for first in range(degree) for second in range(degree)]
        adjacency = graph_from_edges(4 * degree, edges)
        selected = set(range(degree)) | set(range(3 * degree, 4 * degree))
        structure_control(adjacency, selected, totals, 2 * degree)
        balanced_obstacles.append(dict(degree=degree, order=4 * degree,
                                       beta=2 * degree, linear_slack=2 * degree,
                                       global_isolate_imbalance=0,
                                       componentwise_isolate_imbalance=2 * degree))
    report = dict(scope='Literal-star and exact-small-instance controls for the all-degree isolate-tight partition, high-class balances, isolate imbalance margin and higher-degree linear-equality necessity. General proofs are separate.',
                  totals=dict(totals), exact_graphs=graphs, displayed_selections=examples,
                  balanced_partition_obstacles=balanced_obstacles)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['totals']))


if __name__ == '__main__':
    main()
