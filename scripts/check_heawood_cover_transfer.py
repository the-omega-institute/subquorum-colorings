"""Controls for pullback density and discovery of a binary-subspace lemma."""

import argparse
from collections import Counter
import json
from pathlib import Path

from check_heawood_matrix_certificates import CASES, STRONG_CASES, adjacent, outer, polynomial_coefficients
from explore_heawood_two_lifts import exact_bipartite_dissociation


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


def base_and_cotree():
    edges = [(point - 1, 7 + line - 1) for point in range(1, 8) for line in range(1, 8)
             if (point & line).bit_count() % 2 == 0]
    base = [set() for vertex in range(14)]
    for first, second in edges:
        base[first].add(second)
        base[second].add(first)
    reached = {0}
    frontier = [0]
    tree = set()
    while frontier:
        vertex = frontier.pop()
        for neighbor in sorted(base[vertex] - reached):
            reached.add(neighbor)
            frontier.append(neighbor)
            tree.add(tuple(sorted((vertex, neighbor))))
    cotree = sorted(set(edges) - tree)
    assert len(cotree) == 8
    return edges, cotree


def elementary_abelian_cover(rank):
    edges, cotree = base_and_cotree()
    voltages = {edge: (1 << position if position < rank else 0)
                for position, edge in enumerate(cotree)}
    chosen_character = None
    for character in range(1, 1 << rank):
        invariant = 0
        for (first, second), voltage in voltages.items():
            if (voltage & character).bit_count() % 2:
                invariant ^= outer(first + 1, second - 7 + 1)
        if polynomial_coefficients(invariant) == [1, 0, 1, 0]:
            chosen_character = character
            break
    assert chosen_character is not None
    quotient = [set() for vertex in range(28)]
    sheets = 1 << rank
    graph = [set() for vertex in range(14 * sheets)]
    for first, second in edges:
        voltage = voltages.get((first, second), 0)
        sign = (voltage & chosen_character).bit_count() % 2
        for sheet in (0, 1):
            left, right = 2 * first + sheet, 2 * second + (sheet ^ sign)
            quotient[left].add(right)
            quotient[right].add(left)
        for sheet in range(sheets):
            left, right = sheets * first + sheet, sheets * second + (sheet ^ voltage)
            graph[left].add(right)
            graph[right].add(left)
    optimum = exact_bipartite_dissociation(quotient)
    assert optimum['beta'] == 16
    witness = set(optimum['witness'])
    projection = {vertex: 2 * (vertex // sheets)
                  + ((vertex % sheets) & chosen_character).bit_count() % 2
                  for vertex in range(len(graph))}
    assert set(Counter(projection.values()).values()) == {sheets // 2}
    for vertex, neighbors in enumerate(graph):
        assert len(neighbors) == 3
        assert {projection[neighbor] for neighbor in neighbors} == quotient[projection[vertex]]
    selected = {vertex for vertex in range(len(graph)) if projection[vertex] in witness}
    assert 7 * len(selected) == 4 * len(graph)
    assert all(len(graph[vertex] & selected) <= 1 for vertex in selected)
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in graph[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    assert len(reached) == len(graph)
    return dict(rank=rank, order=len(graph), character=chosen_character,
                quotient_optimum=optimum, pulled_certificate_size=len(selected),
                characteristic_polynomial=[1, 0, 1, 0], connected=True)


def dihedral_cover(exponent, character):
    edges, cotree = base_and_cotree()
    rotation_order = 1 << (exponent - 1)
    group_order = 8 * rotation_order
    voltages = {edge: position for position, edge in enumerate(cotree[:4])}

    def binary_character(element):
        rotation = element % rotation_order
        bits = element // rotation_order
        abelianized = (rotation % 2) | (bits << 1)
        return (abelianized & character).bit_count() % 2

    def multiply_generator(element, generator):
        rotation = element % rotation_order
        bits = element // rotation_order
        if generator == 0:
            rotation = (rotation + (-1 if bits & 1 else 1)) % rotation_order
        elif generator in (1, 2, 3):
            bits ^= 1 << (generator - 1)
        return rotation + rotation_order * bits

    graph = [set() for vertex in range(14 * group_order)]
    quotient = [set() for vertex in range(28)]
    for first, second in edges:
        generator = voltages.get((first, second), -1)
        sign = binary_character(multiply_generator(0, generator))
        for sheet in (0, 1):
            left, right = 2 * first + sheet, 2 * second + (sheet ^ sign)
            quotient[left].add(right)
            quotient[right].add(left)
        for element in range(group_order):
            target = multiply_generator(element, generator)
            assert binary_character(target) == binary_character(element) ^ sign
            left, right = group_order * first + element, group_order * second + target
            graph[left].add(right)
            graph[right].add(left)
    optimum = exact_bipartite_dissociation(quotient)
    assert optimum['beta'] == 16
    projection = {vertex: 2 * (vertex // group_order) + binary_character(vertex % group_order)
                  for vertex in range(len(graph))}
    assert set(Counter(projection.values()).values()) == {group_order // 2}
    selected = {vertex for vertex in range(len(graph)) if projection[vertex] in optimum['witness']}
    assert 7 * len(selected) == 4 * len(graph)
    for vertex, neighbors in enumerate(graph):
        assert len(neighbors) == 3
        assert {projection[neighbor] for neighbor in neighbors} == quotient[projection[vertex]]
        if vertex in selected:
            assert len(neighbors & selected) <= 1
    reached = {0}
    frontier = [0]
    while frontier:
        vertex = frontier.pop()
        for neighbor in graph[vertex] - reached:
            reached.add(neighbor)
            frontier.append(neighbor)
    assert len(reached) == len(graph)
    return dict(dihedral_order=1 << exponent, deck_group_order=group_order,
                additional_binary_factors=2, binary_character_rank=4, character=character,
                order=len(graph), pulled_certificate_size=len(selected), connected=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = [cyclic_cover(case, sheets) for case in CASES + STRONG_CASES for sheets in range(1, 13)]
    elementary = [elementary_abelian_cover(rank) for rank in range(4, 9)]
    report = dict(status='ALL_CONTROLS_PASSED', records=records,
                  total_covers=len(records), projection_checks=sum(record['projection_checks'] for record in records),
                  elementary_abelian_controls=elementary,
                  nonabelian_controls=[dihedral_cover(exponent, elementary[0]['character'])
                                       for exponent in range(3, 6)],
                  subspace_exploration=avoiding_subspaces(),
                  scope='Cover pullback controls support the separate general proof. '
                  'Subspace enumeration is discovery only; the threshold now has a separate structural proof. '
                  'No exact higher-cover SF value is inferred.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {'records', 'elementary_abelian_controls'}}, indent=2))


if __name__ == '__main__':
    main()
