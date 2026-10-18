"""Controls for dissociation pullback, square certificates and fiber budgets."""

import argparse
from collections import Counter
from itertools import combinations
from fractions import Fraction
import json
from pathlib import Path

from check_cubic_starforming import base
from check_regular_compensation import connected_after_deletion, sharp_family
from check_regular_starforming import covered, graph_from_edges, star_lists
from explore_heawood_two_lifts import exact_bipartite_dissociation, lift


def dissociates(adjacency, selected):
    return all(len(adjacency[vertex] & selected) <= 1 for vertex in selected)


def prism(length):
    edges = [(vertex, (vertex + 1) % length) for vertex in range(length)]
    edges += [(length + vertex, length + (vertex + 1) % length) for vertex in range(length)]
    edges += [(vertex, length + vertex) for vertex in range(length)]
    return graph_from_edges(2 * length, edges)


def owner_budget(adjacency, selected_left, right):
    counts = Counter(len(adjacency[vertex] & selected_left) for vertex in right)
    owners = {next(iter(adjacency[vertex] & selected_left))
              for vertex in right if len(adjacency[vertex] & selected_left) == 1}
    duplicates = counts[1] - len(owners)
    surplus = len(owners) - 2 * duplicates - counts[2]
    assert surplus == 3 * (len(selected_left) + counts[0] + len(owners) - len(right))
    return dict(left_size=len(selected_left), private_owners=len(owners),
                repeated_private_incidences=duplicates, right_counts=dict(counts), surplus=surplus)


def sharp_square_certificate(degree, totals):
    adjacency, selected = sharp_family(degree)
    first_class = set(range(degree))
    second_class = set(range(degree, 2 * degree))
    third_class = set(range(2 * degree, 3 * degree))
    fourth_class = set(range(3 * degree, 4 * degree))
    first_isolate, second_isolate = 4 * degree, 4 * degree + 1
    alpha = Fraction(6, degree * (degree - 1) * (degree - 2) * (degree - 3))
    eta = Fraction(2, degree * (degree - 2) * (degree - 3))
    gamma = Fraction(1, degree)
    cycles = []
    for first, second in combinations(sorted(first_class), 2):
        for third, fourth in combinations(sorted(adjacency[first] & adjacency[second] & second_class), 2):
            cycles.append(('crown', (first, third, second, fourth), alpha))
    for center in sorted(third_class):
        for first, second in combinations(sorted(adjacency[center] & fourth_class), 2):
            cycles.append(('p', (first_isolate, first, center, second), eta))
    for center in sorted(fourth_class):
        for first, second in combinations(sorted(adjacency[center] & third_class), 2):
            cycles.append(('q', (second_isolate, first, center, second), eta))
    for first in range(degree):
        for second in range(degree):
            if degree + second in adjacency[first] and 3 * degree + first in adjacency[2 * degree + second]:
                cycles.append(('mixed', (first, degree + second, 2 * degree + second, 3 * degree + first), gamma))
    incidence = {vertex: Fraction(0) for vertex in range(len(adjacency))}
    type_counts = Counter()
    for kind, cycle, weight in cycles:
        assert len(set(cycle)) == 4
        assert all(cycle[(position + 1) % 4] in adjacency[vertex]
                   for position, vertex in enumerate(cycle))
        for vertex in cycle:
            incidence[vertex] += weight
        type_counts[kind] += 1
    assert all(weight == 1 for weight in incidence.values())
    assert sum(weight for kind, cycle, weight in cycles) == Fraction(len(adjacency), 4)
    stars = star_lists(adjacency)
    selection = sum(1 << vertex for vertex in selected)
    assert all(covered(stars, selection, outside)
               for outside in range(len(adjacency)) if outside not in selected)
    for deleted in selected:
        smaller = selection ^ (1 << deleted)
        assert any(not covered(stars, smaller, outside)
                   for outside in range(len(adjacency)) if not smaller >> outside & 1)
        totals['square_gap_deletion_witnesses'] += 1
    exact = exact_bipartite_dissociation(adjacency) if degree <= 7 else None
    if exact:
        assert exact['beta'] == 2 * degree + 1
        totals['independent_square_gap_optima'] += 1
    totals['square_gap_certificate_cycles'] += len(cycles)
    return dict(degree=degree, order=len(adjacency), beta=2 * degree + 1,
                displayed_minimal_size=len(selected), alpha=str(alpha), eta=str(eta),
                gamma=str(gamma), type_counts=dict(type_counts),
                vertex_coefficients=[str(incidence[vertex]) for vertex in range(len(adjacency))],
                degree_four_cycles=[dict(kind=kind, vertices=cycle, weight=str(weight))
                                    for kind, cycle, weight in cycles] if degree == 4 else None)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    totals = Counter()
    for order in range(1, 5):
        possible = list(combinations(range(order), 2))
        for edge_mask in range(1 << len(possible)):
            edges = [edge for position, edge in enumerate(possible) if edge_mask >> position & 1]
            adjacency = graph_from_edges(order, edges)
            for signature in range(1 << len(edges)):
                negative = {edge for position, edge in enumerate(edges) if signature >> position & 1}
                lifted = lift(adjacency, negative)
                for selected_mask in range(1 << order):
                    selected = {vertex for vertex in range(order) if selected_mask >> vertex & 1}
                    pulled = selected | {order + vertex for vertex in selected}
                    assert dissociates(adjacency, selected) == dissociates(lifted, pulled)
                    totals['pullback_reflection_selections'] += 1
                totals['small_cover_instances'] += 1
            totals['small_base_graphs'] += 1
    prisms = []
    for base_length in range(4, 15, 2):
        source = prism(base_length)
        for sheets in range(1, 7):
            length = base_length * sheets
            adjacency = prism(length)
            projection = {row * length + column: row * base_length + column % base_length
                          for row in (0, 1) for column in range(length)}
            assert Counter(projection.values()) == Counter({vertex: sheets for vertex in range(2 * base_length)})
            for vertex, neighbors in enumerate(adjacency):
                projected = [projection[neighbor] for neighbor in neighbors]
                assert len(projected) == len(set(projected))
                assert set(projected) == source[projection[vertex]]
            incidence = Counter()
            for column in range(length):
                following = (column + 1) % length
                face = [column, following, length + following, length + column]
                assert len(set(face)) == 4
                assert all(face[(position + 1) % 4] in adjacency[vertex]
                           for position, vertex in enumerate(face))
                incidence.update(face)
                for mask in range(16):
                    selected = {vertex for position, vertex in enumerate(face) if mask >> position & 1}
                    assert dissociates(adjacency, selected) == (len(selected) <= 2)
                    totals['local_square_subsets'] += 1
            assert all(incidence[vertex] == 2 for vertex in range(2 * length))
            independent = {row * length + column for row in (0, 1)
                           for column in range(length) if (row + column) % 2 == 0}
            assert len(independent) == length
            assert all(not adjacency[vertex] & independent for vertex in independent)
            for deleted in range(2 * length):
                assert connected_after_deletion(adjacency, deleted)
                totals['prism_vertex_deletion_connectivity'] += 1
            exact = exact_bipartite_dissociation(adjacency) if length <= 18 else None
            if exact:
                assert exact['beta'] == length
                totals['independent_prism_optima'] += 1
            prisms.append(dict(base_length=base_length, sheets=sheets, order=2 * length,
                               beta=length, square_incidence_per_vertex=2,
                               independently_optimized=bool(exact)))
    exploration = json.loads((root / 'output/heawood-two-lift-exploration.json').read_text())
    examples = []
    for record in exploration['records']:
        adjacency = lift(base(), {tuple(edge) for edge in record['negative_edges']})
        right = set(range(7, 14)) | set(range(21, 28))
        for choice in range(128):
            selected = {vertex + (14 if choice >> vertex & 1 else 0) for vertex in range(7)}
            budget = owner_budget(adjacency, selected, right)
            assert budget['right_counts'].get(0, 0) + budget['right_counts'].get(1, 0) == 7
            assert budget['surplus'] <= 0
            totals['heawood_transversal_controls'] += 1
        if record['signature'] in (1, 10):
            optimum = exact_bipartite_dissociation(adjacency)
            assert optimum['beta'] == record['optimum']['beta']
            selected = set(optimum['witness'])
            assert dissociates(adjacency, selected)
            budget = owner_budget(adjacency, selected - right, right)
            assert budget['surplus'] == 3 * (optimum['beta'] - 14)
            examples.append(dict(signature=record['signature'], negative_edges=record['negative_edges'],
                                 optimum=optimum, budget=budget))
    square_gap_certificates = [sharp_square_certificate(degree, totals) for degree in range(4, 13)]
    report = dict(scope='Controls for general written dissociation covering and fractional-square arguments, connected zero-gain prism covers, exact owner surplus, the impossibility of a gaining full fiber transversal and the uniform fractional square certificate in sharp regular G_d. No proof of the outstanding Heawood strict-gain claim is inferred.',
                  totals=dict(totals), prism_covers=prisms, heawood_examples=examples,
                  square_gap_certificates=square_gap_certificates)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['totals']))


if __name__ == '__main__':
    main()
