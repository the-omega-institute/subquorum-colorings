"""Finite search for the obstruction to a non-port safe deletion."""

import argparse
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

from check_long_core_words import word_control
from check_starforming_gap import local_condition
from explore_long_core_SF import clauses


def safe_deletions(adjacency, selected, ports):
    degrees = [len(neighbors & selected) for neighbors in adjacency]
    safe = set()
    for vertex in selected - ports:
        after = selected - {vertex}
        if not local_condition(adjacency, after, vertex):
            continue
        if any(degrees[port] == 1 for port in adjacency[vertex] & selected & ports):
            continue
        affected = set(adjacency[vertex])
        for center in adjacency[vertex] & selected:
            if degrees[center] == 1:
                affected |= adjacency[center]
        if all(local_condition(adjacency, after, outside) for outside in affected - selected):
            safe.add(vertex)
    return safe


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', type=int, required=True)
    parser.add_argument('--seconds', type=float, default=30)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    copies = arguments.k
    adjacency, pairs, _, _ = word_control('B' * copies)
    order = len(adjacency)
    ports = {vertex for pair in pairs for vertex in pair}
    family = [(clause, None) for clause in clauses(adjacency)]
    family += [(frozenset(adjacency[port]), port) for port in sorted(ports)]
    incident = [[] for vertex in adjacency]
    rows, columns, values, lower, upper = [], [], [], [], []

    def add(terms, minimum=-np.inf, maximum=np.inf):
        row = len(lower)
        for column, value in terms:
            rows.append(row)
            columns.append(column)
            values.append(value)
        lower.append(minimum)
        upper.append(maximum)

    for index, (clause, condition) in enumerate(family):
        marker = order + index
        terms = [(vertex, 1) for vertex in clause]
        add(terms + [(marker, -1)], minimum=0)
        add(terms + [(marker, len(clause) - 1)], maximum=len(clause))
        if condition is not None:
            add([(marker, 1), (condition, -1)], maximum=0)
        for vertex in clause:
            incident[vertex].append(marker)
    for vertex in set(range(order)) - ports:
        add([(index, 1) for index in incident[vertex]] + [(vertex, -1)], minimum=0)
    add([(vertex, 1) for vertex in range(order)], minimum=12 * copies + 1)
    matrix = coo_matrix((values, (rows, columns)),
                        shape=(len(lower), order + len(family))).tocsc()
    result = milp(np.zeros(order + len(family)), integrality=np.ones(order + len(family)),
                  bounds=Bounds(0, 1), constraints=LinearConstraint(matrix, lower, upper),
                  options=dict(time_limit=arguments.seconds, mip_rel_gap=0))
    record = dict(k=copies, solver_status=int(result.status), solver_message=result.message,
                  scope='Finite discovery of a core selection larger than12k with no non-port deletion preserving the local clauses and selected-port activity. No ambient formation or global minimality is presumed. Timeout is inconclusive.')
    if result.x is not None:
        selected = {vertex for vertex in range(order) if result.x[vertex] > 0.5}
        assert len(selected) > 12 * copies
        assert not safe_deletions(adjacency, selected, ports)
        record.update(selected=sorted(selected), selected_size=len(selected),
                      safe_deletions=[], adjacency=[sorted(neighbors) for neighbors in adjacency])
    arguments.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
