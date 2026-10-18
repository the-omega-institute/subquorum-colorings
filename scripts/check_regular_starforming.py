"""Independent finite controls of the general degree-capacity theorem."""

import argparse
from collections import Counter, deque
from itertools import combinations
import json
from pathlib import Path
import random


def masks(adjacency):
    return [sum(1 << neighbor for neighbor in neighbors) for neighbors in adjacency]


def star_lists(adjacency):
    result = [set() for neighbors in adjacency]
    for center, neighbors in enumerate(adjacency):
        for first, second in combinations(neighbors, 2):
            star = (1 << center) | (1 << first) | (1 << second)
            for vertex in (center, first, second):
                result[vertex].add(star)
    return result


def covered(stars, selected, outside):
    available = selected | (1 << outside)
    return any(star & available == star for star in stars[outside])


def local(adjacency, selected, outside):
    neighbors = adjacency[outside] & selected
    if neighbors.bit_count() >= 2:
        return True
    return any(adjacency[vertex] & selected
               for vertex in range(len(adjacency)) if neighbors >> vertex & 1)


def bipartition(adjacency):
    colors = {}
    for start in range(len(adjacency)):
        if start in colors:
            continue
        colors[start] = 0
        queue = deque([start])
        while queue:
            vertex = queue.popleft()
            for neighbor in adjacency[vertex]:
                if neighbor in colors:
                    if colors[neighbor] == colors[vertex]:
                        return None
                else:
                    colors[neighbor] = 1 - colors[vertex]
                    queue.append(neighbor)
    return colors


def equality_partition(adjacency, selected, degree, colors):
    vertices = set(range(len(adjacency)))
    chosen = {vertex for vertex in vertices if selected >> vertex & 1}
    outside = vertices - chosen
    counts = [len(neighbors & chosen) for neighbors in adjacency]
    high = {vertex for vertex in chosen if counts[vertex] >= 2}
    leaves = {vertex for vertex in chosen if counts[vertex] == 1 and adjacency[vertex] & high}
    paired = chosen - high - leaves
    private = {vertex for vertex in outside if counts[vertex] == 1}
    full = outside - private
    assert all(counts[vertex] == degree for vertex in high | full)
    assert all(counts[vertex] == 1 for vertex in chosen - high)
    assert len(high) == len(leaves) == len(private)
    assert all(len(adjacency[vertex] & leaves) == 1 for vertex in high | private)
    assert all(len(adjacency[vertex] & high) == len(adjacency[vertex] & private) == 1
               for vertex in leaves)
    assert all(len(adjacency[vertex] & high) == degree - 1 for vertex in high)
    assert all(len(adjacency[vertex] & private) == degree - 1 for vertex in private)
    assert all(len(adjacency[vertex] & paired) == 1 and
               adjacency[vertex] <= paired | full for vertex in paired)
    assert all(adjacency[vertex] <= chosen for vertex in full)
    if colors is not None:
        exchanged = paired | leaves | {vertex for vertex in high if colors[vertex] == 0} | {
            vertex for vertex in private if colors[vertex] == 1}
        assert len(exchanged) == len(chosen)
        assert all(len(adjacency[vertex] & exchanged) == 1 for vertex in exchanged)
    return bool(high)


def check_graph(adjacency, totals):
    order = len(adjacency)
    adjacency_masks = masks(adjacency)
    stars = star_lists(adjacency)
    degrees = [len(neighbors) for neighbors in adjacency]
    maximum = max(degrees)
    minimum = min(degrees)
    regular = minimum == maximum
    triangle_free = not any(adjacency[first] & adjacency[second]
                            for first in range(order) for second in adjacency[first])
    colors = bipartition(adjacency)
    forming = []
    proper_forming = []
    beta = 0
    star_value = 0
    extremal_high = 0
    minimal_count = 0
    for selected in range(1 << order):
        chosen = [vertex for vertex in range(order) if selected >> vertex & 1]
        outside = [vertex for vertex in range(order) if not selected >> vertex & 1]
        for vertex in outside:
            assert covered(stars, selected, vertex) == local(adjacency_masks, selected, vertex)
            totals['literal_local_tests'] += 1
        forming.append(all(covered(stars, selected, vertex) for vertex in outside))
        proper_forming.append(any(forming[selected ^ (1 << vertex)] or
                                  proper_forming[selected ^ (1 << vertex)] for vertex in chosen))
        counts = [(neighbors & selected).bit_count() for neighbors in adjacency_masks]
        if all(counts[vertex] <= 1 for vertex in chosen):
            beta = max(beta, len(chosen))
        if not forming[selected] or proper_forming[selected]:
            continue
        minimal_count += 1
        star_value = max(star_value, len(chosen))
        isolated = sum(counts[vertex] == 0 for vertex in chosen)
        high = [vertex for vertex in chosen if counts[vertex] >= 2]
        used = set()
        for deleted in high:
            assert covered(stars, selected ^ (1 << deleted), deleted)
            witnesses = {vertex for vertex in outside
                         if not covered(stars, selected ^ (1 << deleted), vertex)}
            assert witnesses and not used & witnesses
            used |= witnesses
            for witness in witnesses:
                assert 1 <= counts[witness] <= 2
                if witness not in adjacency[deleted]:
                    assert counts[witness] == 1
                assert counts[deleted] - 1 <= maximum - counts[witness]
                totals['all_failure_witness_budgets'] += 1
        capacity = sum(maximum - counts[vertex] for vertex in outside)
        assert sum(counts[vertex] - 1 for vertex in high) <= capacity
        assert sum(degrees[vertex] - 1 for vertex in chosen) + isolated <= maximum * len(outside)
        assert (minimum + maximum - 1) * len(chosen) + isolated <= maximum * order
        if regular and maximum >= 1:
            assert (2 * maximum - 1) * len(chosen) + isolated <= maximum * order
            if triangle_free and maximum >= 2 and (2 * maximum - 1) * len(chosen) == maximum * order:
                extremal_high += equality_partition(adjacency, selected, maximum, colors)
                totals['triangle_free_equality_sets'] += 1
        totals['minimal_sets'] += 1
    if regular and maximum >= 2 and colors is not None:
        assert ((2 * maximum - 1) * star_value == maximum * order) == (
            (2 * maximum - 1) * beta == maximum * order)
        if maximum == 3 and star_value > beta:
            assert 10 * (star_value - beta) <= order - 2
    totals['graphs'] += 1
    totals['subsets'] += 1 << order
    totals['extremal_high_sets'] += extremal_high
    return dict(order=order, degree=maximum if regular else None,
                beta2=beta, SF2=star_value, minimal_sets=minimal_count)


def graph_from_edges(order, edges):
    adjacency = [set() for vertex in range(order)]
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    return adjacency


def sharp_graph(degree):
    edges = [(vertex, degree + vertex) for vertex in range(degree)]
    edges += [(vertex, 3 * degree - 1 + neighbor)
              for vertex in range(degree) for neighbor in range(degree - 1)]
    edges += [(degree + vertex, 2 * degree + neighbor)
              for vertex in range(degree) for neighbor in range(degree - 1)]
    return graph_from_edges(4 * degree - 2, edges), set(range(2 * degree))


def high_equality_example():
    edges = [(vertex, (vertex + 1) % 6) for vertex in range(6)]
    edges += [(12 + vertex, 12 + (vertex + 1) % 6) for vertex in range(6)]
    edges += [(vertex, 6 + vertex) for vertex in range(6)]
    edges += [(6 + vertex, 12 + vertex) for vertex in range(6)]
    edges += [(6 + vertex, 18 + vertex % 2) for vertex in range(6)]
    return graph_from_edges(20, edges), set(range(12))


def selected_certificate(adjacency, chosen):
    stars = star_lists(adjacency)
    selected = sum(1 << vertex for vertex in chosen)
    assert all(covered(stars, selected, vertex)
               for vertex in range(len(adjacency)) if vertex not in chosen)
    assert all(any(not covered(stars, selected ^ (1 << deleted), outside)
                   for outside in set(range(len(adjacency))) - (chosen - {deleted}))
               for deleted in chosen)
    return selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    labeled_counts = {}
    for order in range(1, 7):
        count = 0
        edges = list(combinations(range(order), 2))
        for edge_mask in range(1 << len(edges)):
            adjacency = graph_from_edges(order, [edge for position, edge in enumerate(edges)
                                                 if edge_mask >> position & 1])
            if order == 6 and len({len(neighbors) for neighbors in adjacency}) != 1:
                continue
            check_graph(adjacency, totals)
            count += 1
        labeled_counts[order] = count
    generator = random.Random(20261019)
    samples = []
    for half in (4, 5, 6, 7):
        for trial in range(4):
            adjacency = graph_from_edges(2 * half, [])
            for matching in range(3):
                permutation = list(range(half))
                generator.shuffle(permutation)
                for vertex, neighbor in enumerate(permutation):
                    adjacency[vertex].add(half + neighbor)
                    adjacency[half + neighbor].add(vertex)
            samples.append(check_graph(adjacency, totals))
    from check_cubic_starforming import base
    samples.append(check_graph(base(), totals))
    grids = []
    for rows, columns in [(rows, columns) for rows in range(2, 5) for columns in range(2, 5)] + [
            (2, 5), (2, 6), (3, 5)]:
        edges = []
        for row in range(rows):
            for column in range(columns):
                vertex = row * columns + column
                if row + 1 < rows:
                    edges.append((vertex, vertex + columns))
                if column + 1 < columns:
                    edges.append((vertex, vertex + 1))
        result = check_graph(graph_from_edges(rows * columns, edges), totals)
        assert 7 * result['SF2'] <= 4 * rows * columns + 2 * rows + 2 * columns
        grids.append(dict(rows=rows, columns=columns, **result))
    sharp = []
    for degree in range(1, 9):
        adjacency, chosen = sharp_graph(degree)
        selected = selected_certificate(adjacency, chosen)
        assert all(len(neighbors) == degree for neighbors in adjacency)
        assert bipartition(adjacency) is not None
        assert (2 * degree - 1) * len(chosen) == degree * len(adjacency)
        assert all(len(adjacency[vertex] & chosen) == 1 for vertex in chosen)
        if degree >= 2:
            equality_partition(adjacency, selected, degree, bipartition(adjacency))
        sharp.append(dict(degree=degree, order=len(adjacency), beta2=len(chosen), SF2=len(chosen)))
    adjacency, chosen = high_equality_example()
    selected = selected_certificate(adjacency, chosen)
    assert all(len(neighbors) == 3 for neighbors in adjacency)
    colors = bipartition(adjacency)
    assert colors is not None
    assert equality_partition(adjacency, selected, 3, colors)
    result = dict(status='ALL_CHECKS_PASSED', exhaustive_labeled_graphs=labeled_counts,
                  totals=dict(totals), deterministic_samples=samples, seed=20261019,
                  rectangular_grids=grids,
                  sharp_examples=sharp,
                  non_dissociation_extremal_selection=dict(order=20, SF2=12, beta2=12,
                      selected=sorted(chosen), edges=[[vertex, neighbor] for vertex, neighbors in
                          enumerate(adjacency) for neighbor in sorted(neighbors) if vertex < neighbor]),
                  scope='Literal K1,2 stars independently checked against local test. All proper-subset minimality tested dynamically for all labeled graphs through order5, all regular labeled graphs of order6,16 deterministic matching-union samples, Heawood and12 rectangular grids through4x4. Every high-vertex failure witness checked for disjointness and weighted capacity. Triangle-free equality partition and bipartite matching exchange checked. Degree1..8 sharp families and a non-dissociation 20-vertex extremal selection checked by explicit certificates, not exhaustive graph evaluation. General conclusions rely on written proofs.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(dict(status=result['status'], totals=dict(totals))))


if __name__ == '__main__':
    main()
