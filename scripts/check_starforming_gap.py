"""Independent finite checks of the written star-forming gap theorems."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path


MATRIX = ['11001', '11010', '00011', '01111', '10111']
SELECTED = {0, 1, 2, 5, 6, 7}
WITNESSES = {0: 9, 1: 8, 2: 2, 5: 4, 6: 3, 7: 7}


def graph(copies, cyclic=True):
    adjacency = [set() for vertex in range(10 * copies)]
    for block in range(copies):
        for row, entries in enumerate(MATRIX):
            for column, value in enumerate(entries):
                if value == '1':
                    first, second = 10 * block + row, 10 * block + 5 + column
                    adjacency[first].add(second)
                    adjacency[second].add(first)
    if copies > 1:
        for block in range(copies if cyclic else copies - 1):
            first = 10 * block + 5
            second = 10 * ((block + 1) % copies)
            adjacency[first].add(second)
            adjacency[second].add(first)
    return adjacency


def local_condition(adjacency, selected, outside):
    neighbors = adjacency[outside] & selected
    return len(neighbors) >= 2 or any(adjacency[center] & selected for center in neighbors)


def literal_condition(adjacency, selected, outside):
    available = selected | {outside}
    for center in available:
        for leaves in combinations(available - {center}, 2):
            if outside in {center, *leaves} and set(leaves) <= adjacency[center]:
                return True
    return False


def forms(adjacency, selected):
    return all(local_condition(adjacency, selected, outside)
               for outside in set(range(len(adjacency))) - selected)


def connected(adjacency, removed=None):
    remaining = set(range(len(adjacency))) - {removed}
    reached = {min(remaining)}
    frontier = list(reached)
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] & remaining - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    return reached == remaining


def base_checks():
    adjacency = graph(1)
    subsets = [{vertex for vertex in range(10) if mask >> vertex & 1}
               for mask in range(1024)]
    for selected in subsets:
        for outside in set(range(10)) - selected:
            assert literal_condition(adjacency, selected, outside) == local_condition(
                adjacency, selected, outside)
    star_sets = [selected for selected in subsets if forms(adjacency, selected)]
    minimal = [selected for selected in star_sets
               if not any(proper < selected for proper in star_sets)]
    dissociation = [selected for selected in subsets
                   if all(len(adjacency[vertex] & selected) <= 1 for vertex in selected)]
    assert max(map(len, dissociation)) == 5
    assert max(map(len, minimal)) == 6
    assert SELECTED in minimal
    assert Counter(map(len, minimal)) == {4: 37, 5: 48, 6: 1}
    for deleted, witness in WITNESSES.items():
        assert not local_condition(adjacency, SELECTED - {deleted}, witness)
    return dict(beta_2=5, SF_2=6, minimal_set_counts=dict(Counter(map(len, minimal))),
                literal_star_and_local_predicate_agree=True,
                all_proper_subsets_checked=True,
                deletion_witnesses=WITNESSES)


def family_checks(copies, cyclic):
    adjacency = graph(copies, cyclic)
    selected = {10 * block + vertex for block in range(copies) for vertex in SELECTED}
    assert forms(adjacency, selected)
    for block in range(copies):
        for deleted, witness in WITNESSES.items():
            reduced = selected - {10 * block + deleted}
            assert not local_condition(adjacency, reduced, 10 * block + witness)
    all_a = {10 * block + vertex for block in range(copies) for vertex in range(5)}
    assert all(not adjacency[vertex] & all_a for vertex in all_a)
    assert all((vertex % 10 < 5) != (neighbor % 10 < 5)
               for vertex in range(len(adjacency)) for neighbor in adjacency[vertex])
    assert connected(adjacency)
    if cyclic:
        assert all(connected(adjacency, vertex) for vertex in range(len(adjacency)))
    expected_edges = 16 * copies + (copies if cyclic else copies - 1)
    if copies == 1:
        expected_edges = 16
    assert sum(map(len, adjacency)) == 2 * expected_edges
    assert max(map(len, adjacency)) <= 4 and min(map(len, adjacency)) == 2
    return dict(copies=copies, cyclic=cyclic, order=10 * copies, edges=expected_edges,
                two_connected_checked=cyclic, minimal_set_size=len(selected),
                independent_witness_size=len(all_a), maximum_degree=max(map(len, adjacency)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    reports = [family_checks(copies, cyclic)
               for copies in range(2, 31) for cyclic in [False, True]]
    report = dict(status='ALL_CHECKS_PASSED', base=base_checks(), families=reports,
                  scope='Finite checks support the general written proof; no all-size conclusion from enumeration.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], families=len(reports), base=report['base'])))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; verification uses assertions.')
    main()
