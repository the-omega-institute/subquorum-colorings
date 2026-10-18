"""Independent controls for the Fano-plane proof and cubic composition."""

import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import subprocess

from check_starforming_gap import connected, forms, local_condition


SELECTED = {1, 2, 3, 5, 7, 9, 10, 11}
FAILURES = {1: 8, 2: 12, 3: 13, 5: 5, 7: 7, 9: 6, 10: 0, 11: 4}
EIGHT = {0, 1, 2, 3, 7, 8, 12, 13}
SEVEN = {1, 2, 4, 5, 7, 10, 13}
PORTS = (0, 8)


def base():
    vectors = [1, 2, 4, 5, 7, 3, 6]
    lines = {frozenset(triple) for triple in combinations(range(1, 8), 3)
             if triple[0] ^ triple[1] ^ triple[2] == 0}
    adjacency = [set() for vertex in range(14)]
    assert len(lines) == 7
    for line in range(7):
        points = {vectors[line], vectors[(line - 1) % 7], vectors[(line - 3) % 7]}
        assert frozenset(points) in lines
        for point in points:
            vertex = vectors.index(point)
            adjacency[vertex].add(7 + line)
            adjacency[7 + line].add(vertex)
    return adjacency


def dissociation(adjacency, selected):
    return all(len(adjacency[vertex] & selected) <= 1 for vertex in selected)


def star_masks(adjacency):
    return {sum(1 << vertex for vertex in [center, first, second])
            for center, neighbors in enumerate(adjacency)
            for first, second in combinations(neighbors, 2)}


def literal_stars(stars, selected, outside):
    available = sum(1 << vertex for vertex in selected | {outside})
    return any(star >> outside & 1 and star & available == star for star in stars)


def port_state(adjacency, selected):
    return tuple((port in selected, len(adjacency[port] & selected) if port in selected else 0)
                 for port in PORTS)


def base_controls():
    adjacency = base()
    assert all(len(neighbors) == 3 for neighbors in adjacency)
    assert all((vertex < 7) != (neighbor < 7)
               for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors)
    stars = star_masks(adjacency)
    subsets = [{vertex for vertex in range(14) if mask >> vertex & 1}
               for mask in range(1 << 14)]
    forming = []
    for selected in subsets:
        for outside in set(range(14)) - selected:
            assert literal_stars(stars, selected, outside) == local_condition(adjacency, selected, outside)
        forming.append(forms(adjacency, selected))
    proper_forming = []
    for mask in range(1 << 14):
        proper_forming.append(any(forming[mask ^ (1 << vertex)] or proper_forming[mask ^ (1 << vertex)]
                                  for vertex in range(14) if mask >> vertex & 1))
    minimal = [selected for mask, selected in enumerate(subsets) if forming[mask] and not proper_forming[mask]]
    assert SELECTED in minimal
    assert max(map(len, minimal)) == 8
    assert max(len(selected) for selected in subsets if dissociation(adjacency, selected)) == 7
    for deleted, outside in FAILURES.items():
        assert outside not in SELECTED - {deleted}
        assert not literal_stars(stars, SELECTED - {deleted}, outside)
    broken = [set(neighbors) for neighbors in adjacency]
    broken[0].remove(8)
    broken[8].remove(0)
    capacities = {}
    eight_sets = []
    for selected in subsets:
        if not dissociation(broken, selected):
            continue
        assert len(selected) <= 8
        if len(selected) == 8:
            assert set(PORTS) <= selected
            assert all(len(broken[port] & selected) == 1 for port in PORTS)
            eight_sets.append(sorted(selected))
        state = port_state(broken, selected)
        capacities[state] = max(capacities.get(state, 0), len(selected))
    assert len(eight_sets) == 4
    assert dissociation(broken, EIGHT) and dissociation(broken, SEVEN)
    assert not set(PORTS) & SEVEN
    return capacities, dict(order=14, beta2=7, SF2_finite_exact=8,
                            minimal_set_counts=dict(Counter(map(len, minimal))),
                            literal_local_tests=14 * (1 << 13), all_proper_subset_minimality_checked=True,
                            broken_flag_eight_sets=eight_sets,
                            port_states=[dict(state=state, maximum=value) for state, value in sorted(capacities.items())])


def compatible(first, second):
    outgoing, incoming = first[1], second[0]
    return not (outgoing[0] and incoming[0]) or outgoing[1] == incoming[1] == 0


def transfer_maximum(capacities, copies):
    best = 0
    for initial in capacities:
        scores = {initial: capacities[initial]}
        for position in range(1, copies):
            following = {}
            for current, score in scores.items():
                for candidate in capacities:
                    if compatible(current, candidate):
                        following[candidate] = max(following.get(candidate, 0), score + capacities[candidate])
            scores = following
        best = max(best, max((score for final, score in scores.items() if compatible(final, initial)), default=0))
    return best


def family(copies):
    adjacency = [set() for vertex in range(14 * copies)]
    for block in range(copies):
        for vertex, neighbors in enumerate(base()):
            adjacency[14 * block + vertex].update(14 * block + neighbor for neighbor in neighbors)
        adjacency[14 * block].remove(14 * block + 8)
        adjacency[14 * block + 8].remove(14 * block)
    for block in range(copies):
        first, second = 14 * block + 8, 14 * ((block + 1) % copies)
        adjacency[first].add(second)
        adjacency[second].add(first)
    return adjacency


def family_controls(copies, capacities):
    adjacency = family(copies)
    selected = {14 * block + vertex for block in range(copies) for vertex in SELECTED}
    assert len(selected) == 8 * copies and forms(adjacency, selected)
    for block in range(copies):
        for deleted, outside in FAILURES.items():
            assert not local_condition(adjacency, selected - {14 * block + deleted}, 14 * block + outside)
    assert all(len(neighbors) == 3 for neighbors in adjacency)
    assert all((vertex % 14 < 7) != (neighbor % 14 < 7)
               for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors)
    assert connected(adjacency)
    assert all(connected(adjacency, removed) for removed in range(len(adjacency)))
    pairs = set()
    for neighbors in adjacency:
        for pair in combinations(sorted(neighbors), 2):
            assert pair not in pairs
            pairs.add(pair)
    for block in range(copies):
        cycle = [14 * block + vertex for vertex in [1, 9, 2, 10, 3, 11]]
        assert all(cycle[(position + 1) % 6] in adjacency[vertex]
                   for position, vertex in enumerate(cycle))
    matching = [(14 * block + point, 14 * block + 7 + point)
                for block, point in product(range(copies), range(7))]
    assert all(second in adjacency[first] for first, second in matching)
    assert sorted(vertex for edge in matching for vertex in edge) == list(range(14 * copies))
    dense = {2 * position for position in range(copies // 2)}
    attaining = {14 * block + vertex for block in range(copies)
                 for vertex in (EIGHT if block in dense else SEVEN)}
    assert dissociation(adjacency, attaining)
    assert len(attaining) == transfer_maximum(capacities, copies) == 7 * copies + copies // 2
    return dict(copies=copies, order=14 * copies, cubic=True, bipartite=True,
                two_connected=True, girth=6, perfect_matching_size=len(matching),
                beta2=7 * copies + copies // 2, transfer_and_attainment_agree=True,
                minimal_star_set_size=len(selected), gap_lower_bound=(copies + 1) // 2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--cpp', type=Path)
    arguments = parser.parse_args()
    capacities, base_report = base_controls()
    report = dict(status='ALL_CHECKS_PASSED', base=base_report,
                  families=[family_controls(copies, capacities) for copies in range(1, 33)],
                  scope='Finite controls support the Fano incidence proof, saturated-port lemma and all-r composition argument. Exact SF8 is computed only for the base; the general theorem claims SF>=8r.')
    if arguments.cpp:
        independent = json.loads(subprocess.check_output(
            [str(arguments.cpp.resolve()), '--circulant', '7', '1', '3'], text=True))
        assert independent['beta'] == 7 and independent['SF'] == 8
        assert independent['adjacency'] == [sum(1 << neighbor for neighbor in neighbors) for neighbors in base()]
        report['independent_cpp_base'] = independent
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], base=base_report, families=len(report['families']))))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; verification uses assertions.')
    main()
