"""Bounded SAT discovery using the proved private-clause characterization."""

import argparse
from itertools import combinations
import json
from pathlib import Path
from threading import Timer
import time

from pysat.card import CardEnc, EncType
from pysat.formula import CNF, IDPool
from pysat.solvers import Solver

from check_long_core_words import word_control
from explore_long_core_deletions import safe_deletions
from explore_long_core_SF import clauses, graph, verify_literal


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--k', required=True, type=int)
    parser.add_argument('--mode', choices=['core', 'full'], required=True)
    parser.add_argument('--seconds', default=45, type=float)
    parser.add_argument('--target', type=int)
    parser.add_argument('--fixed-phase', action='store_true')
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    copies = arguments.k
    if arguments.mode == 'core':
        adjacency, pairs, _, _ = word_control('B' * copies)
        ports = {vertex for pair in pairs for vertex in pair}
        family = [(clause, None) for clause in clauses(adjacency)]
        family += [(frozenset(adjacency[port]), port) for port in sorted(ports)]
        required_owners = set(range(len(adjacency))) - ports
        target = 12 * copies + 1
    else:
        adjacency, _ = graph(copies)
        family = [(clause, None) for clause in clauses(adjacency)]
        required_owners = set(range(len(adjacency)))
        target = arguments.target if arguments.target is not None else 36 * copies + 1
    order = len(adjacency)
    pool = IDPool(start_from=order + 1)
    formula = CNF()
    incident = [[] for vertex in adjacency]
    for clause, condition in family:
        marker = pool.id()
        members = [vertex + 1 for vertex in clause]
        formula.append([-marker] + members)
        formula.extend([[-marker, -first, -second] for first, second in combinations(members, 2)])
        if condition is not None:
            formula.append([-marker, condition + 1])
        if arguments.mode == 'full':
            formula.append(members)
        for vertex in clause:
            incident[vertex].append(marker)
    for vertex in required_owners:
        formula.append([-(vertex + 1)] + incident[vertex])
    encoding = EncType.cardnetwrk
    formula.extend(CardEnc.atleast(list(range(1, order + 1)), bound=target,
                                  vpool=pool, encoding=encoding).clauses)
    if arguments.fixed_phase:
        from check_long_core_words import translate
        assert arguments.mode == 'full' and copies % 2 == 0
        patterns = [
            {0, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19},
            {1, 4, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17}]
        fixed = {translate(copies, block, local) for block in range(copies)
                 for local in patterns[block % 2]}
        for vertex in range(20 * copies):
            formula.append([vertex + 1 if vertex in fixed else -(vertex + 1)])
    if arguments.mode == 'full':
        upper = 36 * copies + (2 * (copies // 2)) // 7
        formula.extend(CardEnc.atmost(list(range(1, order + 1)), bound=upper,
                                     vpool=pool, encoding=encoding).clauses)
        for block in range(3 * copies):
            members = [20 * copies + 14 * block + vertex + 1 for vertex in range(14)]
            formula.extend(CardEnc.atmost(members, bound=8, vpool=pool, encoding=encoding).clauses)
    started = time.monotonic()
    with Solver(name='glucose4', bootstrap_with=formula.clauses) as solver:
        deadline = Timer(arguments.seconds, solver.interrupt)
        deadline.daemon = True
        deadline.start()
        try:
            result = solver.solve_limited(expect_interrupt=True)
        finally:
            deadline.cancel()
        record = dict(k=copies, mode=arguments.mode, order=order, target=target,
                      status='SAT' if result is True else 'UNSAT' if result is False else 'INTERRUPTED',
                      seconds=round(time.monotonic() - started, 3),
                      binary_variables=pool.top, clauses=len(formula.clauses),
                      solver='glucose4', fixed_phase=arguments.fixed_phase,
                      statistics=solver.accum_stats(),
                      scope='Finite discovery only. Interrupted is inconclusive. UNSAT is a finite solver report without an independently checked proof certificate, not an all-k mathematical proof.')
        if result is True:
            positive = set(solver.get_model())
            selected = {vertex for vertex in range(order) if vertex + 1 in positive}
            assert len(selected) >= target
            record['selected'] = sorted(selected)
            record['selected_size'] = len(selected)
            if arguments.mode == 'core':
                assert not safe_deletions(adjacency, selected, ports)
                record['safe_nonport_deletions'] = []
            else:
                record['literal_deletion_checks'] = verify_literal(adjacency, selected)
    arguments.output.write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
