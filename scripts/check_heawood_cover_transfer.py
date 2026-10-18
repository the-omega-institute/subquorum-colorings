"""Controls for pullback density and discovery of a binary-subspace lemma."""

import argparse
from collections import Counter
import json
from pathlib import Path

from check_heawood_matrix_certificates import CASES, STRONG_CASES, adjacent, polynomial_coefficients


def cyclic_cover(case, sheets):
    name, twisted, matched_points, matched_lines, isolated_points, isolated_lines = case
    order = 28 * sheets
    adjacency = [set() for vertex in range(order)]
    for point in range(1, 8):
        for line in range(1, 8):
            if (point & line).bit_count() % 2:
                continue
            voltage = int((point, line) in twisted)
            for sheet in range(2 * sheets):
                first = (point - 1) * (2 * sheets) + sheet
                second = (7 + line - 1) * (2 * sheets) + (sheet + voltage) % (2 * sheets)
                adjacency[first].add(second)
                adjacency[second].add(first)
    points = set(matched_points + isolated_points)
    lines = set(matched_lines + isolated_lines)
    projection = {}
    selected = set()
    for vertex in range(order):
        base, sheet = divmod(vertex, 2 * sheets)
        label = base % 7 + 1
        projection[vertex] = (base, sheet % 2)
        if 10 * label + sheet % 2 in (points if base < 7 else lines):
            selected.add(vertex)
        assert len(adjacency[vertex]) == 3
    assert set(Counter(projection.values()).values()) == {sheets}
    for vertex, neighbors in enumerate(adjacency):
        projected = {projection[neighbor] for neighbor in neighbors}
        assert len(projected) == 3
        base, sheet = projection[vertex]
        expected = set()
        for other in range(7):
            for other_sheet in (0, 1):
                point = 10 * (base % 7 + 1) + sheet if base < 7 else 10 * (other + 1) + other_sheet
                line = 10 * (other + 1) + other_sheet if base < 7 else 10 * (base % 7 + 1) + sheet
                if adjacent(point, line, set(twisted)):
                    expected.add((7 + other if base < 7 else other, other_sheet))
        assert projected == expected
    assert len(selected) == sheets * (len(points) + len(lines))
    assert all(len(adjacency[vertex] & selected) <= 1 for vertex in selected)
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in adjacency[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    assert len(reached) == order
    return dict(type=name, sheets_above_double=sheets, order=order,
                pulled_certificate_size=len(selected), connected=True,
                projection_checks=order)


def avoiding_subspaces():
    allowed = {matrix for matrix in range(512)
               if polynomial_coefficients(matrix)[1] == 0
               and polynomial_coefficients(matrix)[2:] != [1, 0]}
    spaces = {frozenset([0])}
    counts = []
    for dimension in range(1, 5):
        extended = set()
        for space in spaces:
            for matrix in allowed - space:
                shifted = {element ^ matrix for element in space}
                if shifted <= allowed:
                    extended.add(space | shifted)
        assert all(len(space) == 1 << dimension and space <= allowed for space in extended)
        counts.append(len(extended))
        spaces = extended
    assert counts == [143, 1835, 1269, 0]
    return dict(status='DISCOVERY_ONLY_NOT_A_GENERAL_PROOF', avoiding_subspace_counts=counts,
                forbidden_characteristic_polynomial='t^3+t', dimensions=[1, 2, 3, 4],
                permitted_nonzero_matrices=len(allowed) - 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = [cyclic_cover(case, sheets) for case in CASES + STRONG_CASES for sheets in range(1, 13)]
    report = dict(status='ALL_CONTROLS_PASSED', records=records,
                  total_covers=len(records), projection_checks=sum(record['projection_checks'] for record in records),
                  subspace_exploration=avoiding_subspaces(),
                  scope='Cover pullback controls support the separate general proof. '
                  'Subspace threshold remains discovery until a structural proof is supplied. '
                  'No exact higher-cover SF value is inferred.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'records'}, indent=2))


if __name__ == '__main__':
    main()
