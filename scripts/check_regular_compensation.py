"""Literal-star controls for general bipartite compensation and sharp families."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random

from check_regular_starforming import bipartition, covered, graph_from_edges, masks, star_lists


def exchange_control(adjacency, selected, totals, exact_beta=None):
    vertices = set(range(len(adjacency)))
    outside = vertices - selected
    colors = bipartition(adjacency)
    assert colors is not None
    stars = star_lists(adjacency)
    selection = sum(1 << vertex for vertex in selected)
    assert all(covered(stars, selection, vertex) for vertex in outside)
    failures = {deleted: {vertex for vertex in vertices - (selected - {deleted})
                          if not covered(stars, selection ^ (1 << deleted), vertex)}
                for deleted in selected}
    assert all(failures.values())
    counts = [len(neighbors & selected) for neighbors in adjacency]
    isolated = {vertex for vertex in selected if counts[vertex] == 0}
    high = {vertex for vertex in selected if counts[vertex] >= 2}
    leaves = {vertex for vertex in selected if counts[vertex] == 1 and adjacency[vertex] & high}
    high_failures = {vertex: failures[vertex] & outside for vertex in high}
    assert all(high_failures.values())
    for first, second in combinations(high, 2):
        assert not high_failures[first] & high_failures[second]
    witnesses = {vertex: min(candidates) for vertex, candidates in high_failures.items()}
    good = set()
    for vertex, image in witnesses.items():
        assert counts[image] in (1, 2)
        if image not in adjacency[vertex]:
            good.add(vertex)
            assert counts[image] == 1 and colors[image] == colors[vertex]
            leaf = next(iter(adjacency[image] & selected))
            assert leaf in leaves and adjacency[leaf] & selected == {vertex}
        elif counts[image] == 2:
            assert len(adjacency[image] & isolated) == 1
    leaf_witnesses = {leaf: min(failures[leaf] & outside) for leaf in leaves}
    assert len(set(leaf_witnesses.values())) == len(leaves)
    for leaf, image in leaf_witnesses.items():
        assert image in adjacency[leaf] and counts[image] in (1, 2)
        if counts[image] == 2:
            assert len(adjacency[image] & isolated) == 1 and image not in witnesses.values()
        elif image in witnesses.values():
            owner = next(vertex for vertex, witness in witnesses.items() if witness == image)
            assert owner in good and adjacency[leaf] & selected == {owner}
    unused = outside - set(witnesses.values())
    residual_one = sum(counts[vertex] == 1 for vertex in unused)
    residual_two = sum(counts[vertex] == 2 for vertex in unused)
    leaf_loss = len(leaves) - len(good)
    assert 0 <= leaf_loss <= residual_one + residual_two
    candidates = []
    for color in (0, 1):
        candidate = selected - isolated - high
        candidate |= {vertex for vertex in isolated if colors[vertex] != color}
        candidate |= {vertex for vertex in high if colors[vertex] == color}
        candidate |= {image for image in witnesses.values() if colors[image] != color}
        for vertex in high:
            if colors[vertex] == color:
                ordered = sorted(adjacency[vertex] & leaves)
                candidate -= set(ordered[1:] if vertex in good else ordered)
        assert all(len(adjacency[vertex] & candidate) <= 1 for vertex in candidate)
        candidates.append(candidate)
    assert sum(map(len, candidates)) == 2 * len(selected) - len(isolated) - leaf_loss
    maximum = max(3, max(map(len, adjacency), default=0))
    weighted_base = sum(len(adjacency[vertex]) + maximum - 1 for vertex in selected)
    defect = maximum * len(vertices) - weighted_base
    surplus = sum(maximum - counts[image] - counts[vertex] + 1
                  for vertex, image in witnesses.items())
    assert all(maximum - counts[image] >= counts[vertex] - 1
               for vertex, image in witnesses.items())
    assert defect == len(isolated) + surplus + sum(maximum - counts[vertex] for vertex in unused)
    assert defect >= len(isolated) + (maximum - 1) * residual_one + (maximum - 2) * residual_two
    assert 2 * (len(selected) - max(map(len, candidates))) <= defect
    if exact_beta is not None:
        assert weighted_base + 2 * len(selected) <= maximum * len(vertices) + 2 * exact_beta
    totals['minimal_selections'] += 1
    totals['exchanges'] += 2
    totals['high_witnesses'] += len(high)
    totals['leaf_witnesses'] += len(leaves)
    totals['selections_with_isolates'] += bool(isolated)
    return dict(size=len(selected), isolates=len(isolated), leaf_loss=leaf_loss,
                defect=defect, exchange_sizes=list(map(len, candidates)))


def exhaustive_graph(adjacency, totals):
    order = len(adjacency)
    stars = star_lists(adjacency)
    adjacency_masks = masks(adjacency)
    forming = []
    proper_forming = []
    beta = 0
    minimal = []
    for selection in range(1 << order):
        selected = {vertex for vertex in range(order) if selection >> vertex & 1}
        forming.append(all(covered(stars, selection, vertex) for vertex in range(order)
                           if not selection >> vertex & 1))
        proper_forming.append(any(forming[selection ^ (1 << vertex)] or
                                  proper_forming[selection ^ (1 << vertex)] for vertex in selected))
        if all((adjacency_masks[vertex] & selection).bit_count() <= 1 for vertex in selected):
            beta = max(beta, len(selected))
        if forming[-1] and not proper_forming[-1]:
            minimal.append(selected)
    for selected in minimal:
        exchange_control(adjacency, selected, totals, beta)
    star_value = max(map(len, minimal))
    degrees = list(map(len, adjacency))
    if degrees and min(degrees) == max(degrees) and degrees[0] >= 3:
        degree = degrees[0]
        assert (2 * degree + 1) * star_value <= degree * order + 2 * beta
        assert (4 * degree + 2) * (star_value - beta) <= order
    totals['graphs'] += 1
    totals['subsets'] += 1 << order
    return dict(order=order, beta=beta, SF=star_value, minimal_count=len(minimal))


def sharp_family(degree):
    edges = [(first, degree + second) for first in range(degree)
             for second in range(degree) if first != second]
    for index in range(degree):
        edges += [(index, 3 * degree + index), (degree + index, 2 * degree + index),
                  (4 * degree, 3 * degree + index), (4 * degree + 1, 2 * degree + index)]
    edges += [(2 * degree + first, 3 * degree + second)
              for first in range(degree) for second in range(degree)
              if (second - first) % degree not in (1, 2)]
    return graph_from_edges(4 * degree + 2, edges), set(range(2 * degree)) | {4 * degree, 4 * degree + 1}


def connected_after_deletion(adjacency, deleted):
    remaining = set(range(len(adjacency))) - {deleted}
    reached = {min(remaining)}
    frontier = list(reached)
    while frontier:
        vertex = frontier.pop()
        added = (adjacency[vertex] & remaining) - reached
        reached |= added
        frontier.extend(added)
    return reached == remaining


def family_control(degree, totals):
    adjacency, selected = sharp_family(degree)
    assert all(len(neighbors) == degree for neighbors in adjacency)
    colors = bipartition(adjacency)
    assert colors is not None
    lower = {vertex for vertex in range(len(adjacency)) if colors[vertex] == 0}
    assert len(lower) == 2 * degree + 1
    for deleted in range(len(adjacency)):
        assert connected_after_deletion(adjacency, deleted)
        totals['vertex_connectivity_checks'] += 1
    result = exchange_control(adjacency, selected, totals)
    assert sorted(result['exchange_sizes']) == [2 * degree + 1, 2 * degree + 1]
    result.update(degree=degree, order=len(adjacency), selected=sorted(selected),
                  edges=[[vertex, neighbor] for vertex, neighbors in enumerate(adjacency)
                         for neighbor in sorted(neighbors) if vertex < neighbor])
    if degree <= 5:
        target = 2 * degree + 2
        adjacency_masks = masks(adjacency)
        tested = 0
        for chosen in combinations(range(len(adjacency)), target):
            selection = sum(1 << vertex for vertex in chosen)
            assert any((adjacency_masks[vertex] & selection).bit_count() >= 2 for vertex in chosen)
            tested += 1
        totals['family_forbidden_size_subsets'] += tested
        result['independent_beta_exact'] = 2 * degree + 1
        result['forbidden_size_subsets'] = tested
    if degree == 3:
        assert all(len(adjacency[first] & adjacency[second]) <= 1
                   for first, second in combinations(lower, 2))
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    for left, right in [(1, 1), (1, 4), (2, 3), (2, 4), (3, 3)]:
        possibilities = [(first, left + second) for first in range(left) for second in range(right)]
        for edge_mask in range(1 << len(possibilities)):
            edges = [edge for position, edge in enumerate(possibilities) if edge_mask >> position & 1]
            exhaustive_graph(graph_from_edges(left + right, edges), totals)
    generator = random.Random(2026101905)
    samples = []
    for left, right in [(3, 5), (4, 4), (4, 5), (5, 5), (5, 6), (6, 6)]:
        for density in (0.2, 0.5, 0.8):
            for trial in range(3):
                edges = [(first, left + second) for first in range(left) for second in range(right)
                         if generator.random() < density]
                samples.append(exhaustive_graph(graph_from_edges(left + right, edges), totals))
    families = [family_control(degree, totals) for degree in range(3, 17)]
    exact_families = []
    for degree in (3, 4):
        adjacency, selected = sharp_family(degree)
        exact_families.append(exhaustive_graph(adjacency, totals))
    report = dict(scope='Literal-star all-subset controls of arbitrary bipartite weighted compensation; sharp-family deletion, connectivity and independently exhaustive dissociation controls. General theorems have separate written proofs.',
                  seed=2026101905, totals=dict(totals), sampled_graphs=samples,
                  exact_families=exact_families, families=families)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['totals']))


if __name__ == '__main__':
    main()
