"""Finite discovery of connected frozen receivers with prescribed charge."""

import argparse
import itertools
import json
from pathlib import Path
import time

import z3

from check_component_receivers import endpoint_components, verify_terminal
from check_cooperative_promotion import neighbors
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def count(terms):
    return z3.Sum([z3.If(term, 1, 0) for term in terms])


def encoding(rows, columns, charge, timeout, root, require_frozen=True):
    assert rows % 2 == columns % 2 == 0
    points = set(itertools.product(range(rows), range(columns)))
    assert root in points
    adjacent = {point: set(neighbors(point)) & points for point in points}
    edges = sorted({tuple(sorted((point, other))) for point in points
                    for other in adjacent[point]})
    selected = {point: z3.Bool('t_%d_%d' % point) for point in points}
    endpoints = {point: z3.Bool('p_%d_%d' % point) for point in points}
    matching = {edge: z3.Bool('m_%d_%d_%d_%d' % (*edge[0], *edge[1])) for edge in edges}
    frozen_rank = {point: z3.Int('f_%d_%d' % point) for point in points}
    distance = {point: z3.Int('d_%d_%d' % point) for point in points}
    incident = {point: [edge for edge in edges if point in edge] for point in points}
    solver = z3.Solver()
    solver.set(timeout=1000*timeout)
    solver.add(endpoints[root], distance[root] == 0)
    for point in sorted(points):
        solver.add(z3.Not(z3.And(selected[point], endpoints[point])))
        solver.add(count(matching[edge] for edge in incident[point]) == z3.If(endpoints[point], 1, 0))
        solver.add(z3.Implies(selected[point], count(z3.Or(selected[other], endpoints[other])
                                                    for other in adjacent[point]) <= 1))
        solver.add(frozen_rank[point] >= 0, frozen_rank[point] < len(points))
        retained = []
        for other in sorted(adjacent[point]):
            retained.append(z3.Or(selected[other], z3.Or([
                z3.And(matching[edge], frozen_rank[next(partner for partner in edge if partner != other)]
                       < frozen_rank[point]) for edge in incident[other]])))
        if require_frozen:
            solver.add(z3.Implies(endpoints[point], count(retained) >= 2))
        solver.add(z3.Implies(endpoints[point], count(z3.Or(selected[other], endpoints[other])
                                                     for other in adjacent[point]) >= 3))
        if point != root:
            solver.add(z3.Implies(endpoints[point], z3.And(distance[point] > 0,
                distance[point] < len(points), z3.Or([
                    z3.And(endpoints[other], distance[other] < distance[point])
                    for other in adjacent[point]]))))
    tiles = [{(2*row+local_row, 2*column+local_column)
              for local_row, local_column in itertools.product((0, 1), repeat=2)}
             for row, column in itertools.product(range(rows//2), range(columns//2))]
    used = [z3.Or([endpoints[point] for point in tile]) for tile in tiles]
    selected_inside = z3.Sum([z3.If(used[index], count(selected[point] for point in tile), 0)
                              for index, tile in enumerate(tiles)])
    total_charge = selected_inside+count(matching.values())-2*count(used)
    solver.add(total_charge >= charge)
    return solver, selected, endpoints, matching, frozen_rank, total_charge


def verify(current, require_frozen=True):
    objective = direct_check(*current)
    endpoints = endpoint_data(current)[0]
    assert endpoints and endpoint_components(current) == [endpoints]
    frozen, layers = frozen_certificate(current)
    if require_frozen:
        assert frozen == endpoints
    ledger = verify_terminal(current)
    assert len(ledger['receivers']) == 1
    receiver = ledger['receivers'][0]
    assert receiver['charge_twice'] % 2 == 0
    return dict(objective=objective, receiver_charge=receiver['charge_twice']//2,
                ledger=ledger, fully_frozen=frozen == endpoints, freezing_layers=layers)


def search(rows, columns, charge, timeout, root, require_frozen=True):
    solver, selected, endpoints, matching, frozen_rank, total_charge = encoding(
        rows, columns, charge, timeout, root, require_frozen)
    started = time.monotonic()
    status = solver.check()
    report = dict(status=str(status), shape=[rows, columns], minimum_charge=charge,
                  root=root, require_frozen=require_frozen, timeout_seconds=timeout,
                  seconds=round(time.monotonic()-started, 3),
                  scope='All feasible labeled configurations and actual grid matchings in this '
                        'fixed even rectangle, with one nonempty connected endpoint component '
                        'containing the prescribed root. Single terminality is required; '
                        'a strict finite freezing certificate is additionally required when '
                        'require_frozen is true. '
                        'Finite discovery only; unknown is not unsat.')
    if status == z3.sat:
        model = solver.model()
        actual_selected = {point for point, variable in selected.items() if z3.is_true(model.eval(variable))}
        actual_matching = [edge for edge, variable in matching.items() if z3.is_true(model.eval(variable))]
        actual_endpoints = {point for point, variable in endpoints.items() if z3.is_true(model.eval(variable))}
        current = rows, columns, actual_selected, actual_matching
        assert endpoint_data(current)[0] == actual_endpoints
        checked = verify(current, require_frozen)
        assert checked['receiver_charge'] == model.eval(total_charge).as_long() >= charge
        report.update(selected=sorted(actual_selected), matching=actual_matching,
                      ranks=[dict(point=point, rank=model.eval(frozen_rank[point]).as_long())
                             for point in sorted(actual_endpoints)], checked=checked)
    else:
        report['reason_unknown'] = solver.reason_unknown() if status == z3.unknown else None
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, required=True)
    parser.add_argument('--columns', type=int, required=True)
    parser.add_argument('--charge', type=int, default=2)
    parser.add_argument('--root', type=int, nargs=2, default=(2, 2))
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--single-terminal-only', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = search(arguments.rows, arguments.columns, arguments.charge,
                    arguments.timeout, tuple(arguments.root), not arguments.single_terminal_only)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {'selected', 'matching', 'ranks', 'checked'}}))
    if 'checked' in report:
        print(json.dumps({key: value for key, value in report['checked'].items()
                          if key != 'freezing_layers'}))


if __name__ == '__main__':
    main()
