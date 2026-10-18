"""Independent broken-block and connected sharp-gap controls."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix

from check_regular_compensation import connected_after_deletion, exchange_control, sharp_family


def ring(degree, copies):
    block, chosen = sharp_family(degree)
    order = len(block)
    adjacency = [set() for vertex in range(order * copies)]
    selected = set()
    for index in range(copies):
        offset = order * index
        for vertex, neighbors in enumerate(block):
            adjacency[offset + vertex] = {offset + neighbor for neighbor in neighbors}
        selected |= {offset + vertex for vertex in chosen}
        first, second = offset + 2 * degree, offset + 3 * degree
        adjacency[first].remove(second)
        adjacency[second].remove(first)
    for index in range(copies):
        first = order * index + 2 * degree
        second = order * ((index + 1) % copies) + 3 * degree
        adjacency[first].add(second)
        adjacency[second].add(first)
    return adjacency, selected


def exhaustive_forbidden_size(adjacency, target):
    adjacency_masks = [sum(1 << neighbor for neighbor in neighbors) for neighbors in adjacency]
    tested = 0
    for chosen in combinations(range(len(adjacency)), target):
        selected = sum(1 << vertex for vertex in chosen)
        assert any((adjacency_masks[vertex] & selected).bit_count() >= 2 for vertex in chosen)
        tested += 1
    return tested


def exact_dissociation(adjacency):
    triples = sorted({tuple(sorted((center, first, second)))
                      for center, neighbors in enumerate(adjacency)
                      for first, second in combinations(neighbors, 2)})
    matrix = np.zeros((len(triples), len(adjacency)))
    for row, triple in enumerate(triples):
        matrix[row, list(triple)] = 1
    result = milp(-np.ones(len(adjacency)), integrality=np.ones(len(adjacency)),
                  bounds=Bounds(np.zeros(len(adjacency)), np.ones(len(adjacency))),
                  constraints=LinearConstraint(csr_matrix(matrix), -np.inf, 2),
                  options={'time_limit': 30, 'mip_rel_gap': 0})
    assert result.status == 0 and result.mip_gap == 0
    selected = {vertex for vertex, value in enumerate(result.x) if value > 0.5}
    assert all(len(adjacency[vertex] & selected) <= 1 for vertex in selected)
    assert abs(result.fun + len(selected)) < 1e-7
    assert abs(result.mip_dual_bound - result.fun) < 1e-7
    return dict(beta=len(selected), witness=sorted(selected), solver_status=int(result.status),
                objective=float(result.fun), dual_bound=float(result.mip_dual_bound),
                relative_gap=float(result.mip_gap))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    broken = []
    for degree in range(3, 13):
        adjacency, selected = sharp_family(degree)
        first, second = 2 * degree, 3 * degree
        adjacency[first].remove(second)
        adjacency[second].remove(first)
        result = exchange_control(adjacency, selected, totals)
        result.update(degree=degree, order=len(adjacency), ports=[first, second])
        if degree == 3:
            obstruction = set(range(degree)) | set(range(3 * degree, 4 * degree)) | {first, 4 * degree + 1}
            assert len(obstruction) == 8
            assert all(len(adjacency[vertex] & obstruction) <= 1 for vertex in obstruction)
            result['cubic_obstruction'] = sorted(obstruction)
            result['forbidden_size_subsets'] = exhaustive_forbidden_size(adjacency, 9)
            result['exact_beta'] = 8
        elif degree <= 5:
            result['forbidden_size_subsets'] = exhaustive_forbidden_size(adjacency, 2 * degree + 2)
            result['exact_beta'] = 2 * degree + 1
        totals['broken_forbidden_size_subsets'] += result.get('forbidden_size_subsets', 0)
        broken.append(result)
    examples = []
    optimize = {(4, 2), (4, 3), (5, 2), (6, 2), (8, 2)}
    for degree in range(4, 9):
        for copies in range(1, 5):
            adjacency, selected = ring(degree, copies)
            assert all(len(neighbors) == degree for neighbors in adjacency)
            for deleted in range(len(adjacency)):
                assert connected_after_deletion(adjacency, deleted)
                totals['vertex_connectivity_checks'] += 1
            record = exchange_control(adjacency, selected, totals)
            record.update(degree=degree, copies=copies, order=len(adjacency),
                          theorem_SF=(2 * degree + 2) * copies,
                          theorem_beta=(2 * degree + 1) * copies)
            assert len(selected) == record['theorem_SF']
            assert record['exchange_sizes'] == [record['theorem_beta']] * 2
            if (degree, copies) in optimize:
                record['independent_optimum'] = exact_dissociation(adjacency)
                assert record['independent_optimum']['beta'] == record['theorem_beta']
                totals['exact_connected_optima'] += 1
            examples.append(record)
            print(json.dumps({key: record[key] for key in ['degree', 'copies', 'order']}), flush=True)
    report = dict(scope='Broken-block literal-star exchanges and exhaustive forbidden-size checks; connected-ring literal deletion, all vertex-removal connectivity tests and five independent exact MILP optima. General proof is separate.',
                  totals=dict(totals), broken_blocks=broken, connected_examples=examples)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report['totals']))


if __name__ == '__main__':
    main()
