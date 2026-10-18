"""Independent literal-star and exchange controls for cubic compensation."""

import argparse
from collections import Counter
from itertools import combinations, permutations
import json
from pathlib import Path
import random

from check_cubic_starforming import SELECTED, base, dissociation
from check_cubic_stability_ports import construction
from check_regular_starforming import bipartition, covered, masks, star_lists


def selection_control(adjacency, selected, totals, exact_beta=None):
    colors = bipartition(adjacency)
    stars = star_lists(adjacency)
    vertices = set(range(len(adjacency)))
    outside = vertices - selected
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
    excess = sum(max(len(adjacency[vertex] & leaves) - 1, 0) for vertex in high)
    witness = {vertex: min(failures[vertex] & outside) for vertex in high}
    assert len(set(witness.values())) == len(high)
    bad_one = set()
    bad_two = set()
    good = set()
    for vertex, image in witness.items():
        assert 1 <= counts[image] <= 2
        if image not in adjacency[vertex]:
            assert counts[image] == 1 and colors[image] == colors[vertex]
            leaf = next(iter(adjacency[image] & selected))
            assert leaf in leaves and adjacency[leaf] & selected == {vertex}
            good.add(vertex)
        else:
            assert counts[vertex] == 2
            if counts[image] == 1:
                bad_one.add(vertex)
            else:
                assert len(adjacency[image] & isolated) == 1
                bad_two.add(vertex)
    unused = outside - set(witness.values())
    residual_one = sum(counts[vertex] == 1 for vertex in unused)
    residual_two = sum(counts[vertex] == 2 for vertex in unused)
    good_two = sum(counts[vertex] == 2 for vertex in good)
    defect = 3 * len(vertices) - 5 * len(selected)
    assert defect == len(isolated) + len(bad_one) + good_two + 2 * residual_one + residual_two
    leaf_witness = {leaf: min(failures[leaf] & outside) for leaf in leaves}
    assert len(set(leaf_witness.values())) == len(leaves)
    leaf_two = set()
    for leaf, image in leaf_witness.items():
        assert leaf in adjacency[image] and counts[image] in (1, 2)
        if counts[image] == 2:
            assert len(adjacency[image] & isolated) == 1
            assert image not in witness.values()
            leaf_two.add(image)
    assert excess <= residual_one + len(leaf_two)
    assert len(bad_two) + len(leaf_two) <= 3 * len(isolated)
    assert len(bad_one) + len(bad_two) + excess <= defect + 2 * len(isolated)
    candidates = []
    for color in range(2):
        candidate = (selected - high) | {vertex for vertex in high if colors[vertex] == color}
        candidate |= {witness[vertex] for vertex in good if colors[vertex] != color}
        removed = 0
        for vertex in high:
            if colors[vertex] != color:
                continue
            excess_leaves = sorted(adjacency[vertex] & leaves)[1:]
            candidate -= set(excess_leaves)
            removed += len(excess_leaves)
        assert dissociation(adjacency, candidate)
        missing_bad = sum(colors[vertex] != color for vertex in bad_one | bad_two)
        assert len(candidate) == len(selected) - missing_bad - removed
        candidates.append(candidate)
    assert sum(map(len, candidates)) == 2 * len(selected) - len(bad_one) - len(bad_two) - excess
    assert 2 * (len(selected) - max(map(len, candidates))) <= defect + 2 * len(isolated)
    if exact_beta is not None:
        assert 2 * (len(selected) - exact_beta) <= defect + 2 * len(isolated) <= 3 * defect
    totals['minimal_selections'] += 1
    totals['exchanges'] += 2
    totals['no_isolate_selections'] += not isolated
    totals['selected_isolates'] += len(isolated)
    totals['high_witnesses'] += len(high)
    totals['leaf_witnesses'] += len(leaves)
    return dict(order=len(vertices), selected=len(selected), isolates=len(isolated),
                defect=defect, adjacent_one=len(bad_one), adjacent_two=len(bad_two),
                leaf_excess=excess, candidate_sizes=list(map(len, candidates)),
                candidates=[sorted(candidate) for candidate in candidates])


def enumerate_graph(adjacency, totals):
    order = len(adjacency)
    stars = star_lists(adjacency)
    adjacency_masks = masks(adjacency)
    forming = []
    proper_forming = []
    minimal = []
    beta = 0
    for selection in range(1 << order):
        selected = [vertex for vertex in range(order) if selection >> vertex & 1]
        forming.append(all(covered(stars, selection, outside) for outside in range(order)
                           if not selection >> outside & 1))
        proper_forming.append(any(forming[selection ^ (1 << vertex)] or
                                  proper_forming[selection ^ (1 << vertex)] for vertex in selected))
        if all((adjacency_masks[vertex] & selection).bit_count() <= 1 for vertex in selected):
            beta = max(beta, len(selected))
        if forming[-1] and not proper_forming[-1]:
            minimal.append(set(selected))
    for selected in minimal:
        selection_control(adjacency, selected, totals, beta)
    star_value = max(map(len, minimal))
    assert 17 * star_value <= 9 * order + 2 * beta
    assert 34 * (star_value - beta) <= 3 * order
    totals['graphs'] += 1
    totals['subsets'] += 1 << order
    return dict(order=order, beta=beta, SF=star_value, minimal_count=len(minimal))


def from_permutations(permutations_used):
    half = len(permutations_used[0])
    adjacency = [set() for vertex in range(2 * half)]
    for permutation in permutations_used:
        for vertex, neighbor in enumerate(permutation):
            adjacency[vertex].add(half + neighbor)
            adjacency[half + neighbor].add(vertex)
    return adjacency


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    graphs = []
    graphs.append(from_permutations([tuple((vertex + shift) % 3 for vertex in range(3))
                                     for shift in range(3)]))
    for omitted in permutations(range(4)):
        graph = [set() for vertex in range(8)]
        for vertex in range(4):
            for neighbor in range(4):
                if neighbor != omitted[vertex]:
                    graph[vertex].add(4 + neighbor)
                    graph[4 + neighbor].add(vertex)
        graphs.append(graph)
    for half in range(5, 8):
        for first, second in combinations(range(1, half), 2):
            graphs.append(from_permutations([tuple((vertex + shift) % half for vertex in range(half))
                                             for shift in (0, first, second)]))
    generator = random.Random(20261019)
    for half in (5, 6, 7):
        for trial in range(8):
            while True:
                matchings = [generator.sample(range(half), half) for matching in range(3)]
                graph = from_permutations(matchings)
                if all(len(neighbors) == 3 for neighbors in graph):
                    break
            graphs.append(graph)
    graphs.append(base())
    report = dict(scope='Independent literal-star all-subset controls and explicit exchange witnesses',
                  graphs=[enumerate_graph(graph, totals) for graph in graphs])
    report['heawood_obstacle'] = selection_control(base(), SELECTED, totals, 7)
    assert report['heawood_obstacle']['candidate_sizes'] == [5, 5]
    report['larger_family_selections'] = []
    for copies in range(1, 9):
        graph, selected, attaining = construction(copies)
        report['larger_family_selections'].append(selection_control(graph, selected, totals, len(attaining)))
    report['totals'] = dict(totals)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['totals']))


if __name__ == '__main__':
    main()
