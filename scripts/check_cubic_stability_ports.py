"""Independent witnesses and small-instance controls for the port construction."""

import argparse
from itertools import combinations
import json
from pathlib import Path

from check_cubic_starforming import SELECTED, base, dissociation
from check_regular_starforming import bipartition, covered, star_lists
from check_starforming_gap import connected


def construction(copies):
    size = 6 * copies
    adjacency = base() + [set() for vertex in range(20 * copies)]
    high = [14 + position for position in range(size)]
    leaves = [14 + size + position for position in range(size)]
    private = [14 + 2 * size + position for position in range(size)]
    full = [14 + 3 * size + position for position in range(2 * copies)]
    edges = []
    for position in range(size):
        following = (position + 1) % size
        edges.extend([(high[position], high[following]),
                      (private[position], private[following]),
                      (high[position], leaves[position]),
                      (leaves[position], private[position]),
                      (leaves[position], full[2 * (position // 6) + position % 2])])
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    for first, second in [(0, 8), (private[0], private[1])]:
        adjacency[first].remove(second)
        adjacency[second].remove(first)
    for first, second in [(0, private[1]), (8, private[0])]:
        adjacency[first].add(second)
        adjacency[second].add(first)
    selected = SELECTED | set(high) | set(leaves)
    attaining = set(range(7)) | set(leaves) | set(high[1::2]) | set(private[::2])
    return adjacency, selected, attaining


def heawood_control():
    adjacency = base()
    cycle = [0, 7, 4, 11, 1, 8, 5, 12, 2, 9, 6, 13, 3, 10]
    assert all(cycle[(position + 1) % 14] in adjacency[vertex]
               for position, vertex in enumerate(cycle))
    adjacency[0].remove(8)
    adjacency[8].remove(0)
    largest = 0
    saturated = []
    budgets = 0
    for mask in range(1 << 14):
        selected = {vertex for vertex in range(14) if mask >> vertex & 1}
        if not dissociation(adjacency, selected):
            continue
        ports = len(selected & {0, 8})
        assert 5 * len(selected) <= 40 + 2 * ports
        budgets += 1
        largest = max(largest, len(selected))
        if len(selected) == 8:
            assert {0, 8} <= selected
            assert all(len(adjacency[port] & selected) == 1 for port in (0, 8))
            saturated.append(sorted(selected))
    assert largest == 8 and len(saturated) == 4
    return dict(subsets=1 << 14, dissociation_budgets=budgets,
                beta=largest, saturated_eight_sets=saturated)


def milp_control(adjacency):
    import numpy as np
    import scipy
    from scipy.optimize import Bounds, LinearConstraint, milp
    from scipy.sparse import csr_matrix

    triples = sorted({tuple(sorted((center, first, second)))
                      for center, neighbors in enumerate(adjacency)
                      for first, second in combinations(neighbors, 2)})
    matrix = np.zeros((len(triples), len(adjacency)))
    for row, triple in enumerate(triples):
        matrix[row, list(triple)] = 1
    result = milp(-np.ones(len(adjacency)), integrality=np.ones(len(adjacency)),
                  bounds=Bounds(np.zeros(len(adjacency)), np.ones(len(adjacency))),
                  constraints=LinearConstraint(csr_matrix(matrix), -np.inf, 2),
                  options={'time_limit': 45, 'mip_rel_gap': 0})
    assert result.status == 0, str(result)
    selected = {vertex for vertex, value in enumerate(result.x) if value > 0.5}
    assert dissociation(adjacency, selected)
    assert abs(result.fun + len(selected)) < 1e-6
    return dict(beta=len(selected), witness=sorted(selected), scipy=scipy.__version__,
                solver_status=int(result.status), gap=float(result.mip_gap))


def family_control(copies, use_milp):
    adjacency, selected, attaining = construction(copies)
    order = len(adjacency)
    assert order == 14 + 20 * copies
    assert all(len(neighbors) == 3 and vertex not in neighbors and
               all(vertex in adjacency[neighbor] for neighbor in neighbors)
               for vertex, neighbors in enumerate(adjacency))
    assert bipartition(adjacency) is not None
    assert connected(adjacency)
    assert all(connected(adjacency, removed) for removed in range(order))
    stars = star_lists(adjacency)
    selection = sum(1 << vertex for vertex in selected)
    assert all(covered(stars, selection, outside)
               for outside in set(range(order)) - selected)
    witnesses = {}
    for deleted in sorted(selected):
        smaller = selection ^ (1 << deleted)
        failures = [outside for outside in range(order) if not smaller >> outside & 1
                    and not covered(stars, smaller, outside)]
        assert failures
        witnesses[deleted] = failures[0]
    assert len(selected) == 8 + 12 * copies == 3 * order // 5
    assert dissociation(adjacency, attaining)
    assert len(attaining) == 7 + 12 * copies
    assert 7 * len(selected) == 3 * order + 2 * len(attaining)
    assert 7 * len(selected) - 4 * order == 4 * copies
    result = dict(k=copies, order=order, cubic=True, bipartite=True, two_connected=True,
                  minimal_star_set=sorted(selected), deletion_witnesses=witnesses,
                  dissociation_witness=sorted(attaining), SF_by_written_upper_bound=len(selected),
                  beta_by_written_port_proof=len(attaining), regular_defect=2,
                  candidate_stability_equality=True)
    if copies <= 3 and use_milp:
        result['independent_milp'] = milp_control(adjacency)
        assert result['independent_milp']['beta'] == len(attaining)
    if copies == 1:
        result['edges'] = [[vertex, neighbor] for vertex, neighbors in enumerate(adjacency)
                           for neighbor in sorted(neighbors) if vertex < neighbor]
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--milp', action='store_true')
    arguments = parser.parse_args()
    report = dict(scope='Finite controls; general parameters require the written proof',
                  heawood=heawood_control(), families=[])
    for copies in range(1, 9):
        result = family_control(copies, arguments.milp)
        report['families'].append(result)
        print(json.dumps({key: result[key] for key in ['k', 'order', 'SF_by_written_upper_bound',
                                                      'beta_by_written_port_proof']}), flush=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
