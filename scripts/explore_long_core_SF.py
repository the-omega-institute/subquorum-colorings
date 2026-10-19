"""Discovery MILP for minimal star-forming sets via private hitting clauses."""

import argparse
import json
from pathlib import Path
import time

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import coo_matrix

from check_cubic_padding_rings import core, edge
from check_cubic_starforming import SELECTED, base, star_masks
from check_starforming_gap import forms


def graph(copies):
    adjacency = core(copies)
    selected = set(range(12 * copies))
    for index in range(3 * copies):
        first, second = 12 * copies + 2 * index, 12 * copies + 2 * index + 1
        adjacency[first].remove(second)
        adjacency[second].remove(first)
        block = base()
        block[0].remove(8)
        block[8].remove(0)
        offset = len(adjacency)
        adjacency.extend({offset + neighbor for neighbor in neighbors} for neighbors in block)
        edge(adjacency, offset, second)
        edge(adjacency, offset + 8, first)
        selected |= {offset + vertex for vertex in SELECTED}
    return adjacency, selected


def clauses(adjacency):
    family = {frozenset({vertex} | neighbors) for vertex, neighbors in enumerate(adjacency)}
    family |= {frozenset({vertex} | (neighbors - {neighbor}) |
                        (adjacency[neighbor] - {vertex}))
               for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors}
    return sorted(family, key=lambda clause: (len(clause), sorted(clause)))


def verify_literal(adjacency, selected):
    stars = star_masks(adjacency)
    containing = [[] for vertex in adjacency]
    for star in stars:
        for vertex in range(len(adjacency)):
            if star >> vertex & 1:
                containing[vertex].append(star)

    def literal_forms(selection):
        chosen_mask = sum(1 << vertex for vertex in selection)
        for outside in set(range(len(adjacency))) - selection:
            available = chosen_mask | (1 << outside)
            if not any(star & available == star for star in containing[outside]):
                return False
        return True

    assert forms(adjacency, selected) and literal_forms(selected)
    assert all(not literal_forms(selected - {deleted}) for deleted in selected)
    return len(selected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', type=int, required=True)
    parser.add_argument('--seconds', type=float, default=60)
    parser.add_argument('--target', type=int)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    copies = arguments.k
    adjacency, baseline = graph(copies)
    family = clauses(adjacency)
    order, clause_count = len(adjacency), len(family)
    assert len(baseline) == 36 * copies
    assert all(clause & baseline for clause in family)
    assert all(any(clause & baseline == {vertex} for clause in family) for vertex in baseline)
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

    for index, clause in enumerate(family):
        terms = [(vertex, 1) for vertex in clause]
        add(terms, minimum=1)
        add(terms + [(order + index, len(clause) - 1)], maximum=len(clause))
        for vertex in clause:
            incident[vertex].append(order + index)
    for vertex in range(order):
        add([(index, 1) for index in incident[vertex]] + [(vertex, -1)], minimum=0)
    for block in range(3 * copies):
        add([(20 * copies + 14 * block + vertex, 1) for vertex in range(14)], maximum=8)
    target = arguments.target if arguments.target is not None else 36 * copies + 1
    add([(vertex, 1) for vertex in range(order)], minimum=target,
        maximum=36 * copies + (2 * (copies // 2)) // 7)
    matrix = coo_matrix((values, (rows, columns)),
                        shape=(len(lower), order + clause_count)).tocsc()
    objective = np.zeros(order + clause_count)
    started = time.monotonic()
    result = milp(objective, integrality=np.ones(order + clause_count),
                  bounds=Bounds(0, 1),
                  constraints=LinearConstraint(matrix, lower, upper),
                  options=dict(time_limit=arguments.seconds, mip_rel_gap=0))
    report = dict(k=copies, order=order, clauses=clause_count,
                  variables=order + clause_count, constraints=len(lower), target=target,
                  solver_status=int(result.status), solver_message=result.message,
                  seconds=round(time.monotonic() - started, 3),
                  scope='Finite discovery only; timeout is inconclusive and infeasibility is not an all-k proof. Binary x selects vertices. Binary p marks a clause with exactly one selected member. Every selected vertex must lie in a marked clause, giving a private witness. The exact general clause equivalence and minimality argument have written proofs.')
    if result.x is not None:
        selected = {vertex for vertex in range(order) if result.x[vertex] > 0.5}
        assert len(selected) >= target
        report['literal_deletion_checks'] = verify_literal(adjacency, selected)
        report['selected'] = sorted(selected)
        report['selected_size'] = len(selected)
        report['core_selected_size'] = len(selected & set(range(20 * copies)))
        report['block_sizes'] = [sum(20 * copies + 14 * block + vertex in selected
                                     for vertex in range(14)) for block in range(3 * copies)]
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
