"""Positive fixed-grid controls for the constrained rank-obstruction search."""

import argparse
import itertools
import json
from pathlib import Path

import z3

from search_frozen_receiver_ceiling import encoding, verify
from search_strip_coverage import exclude_certificates
from search_strip_rank_coverage import first_balanced_shape, first_mixed_shape
from check_low_charge_rank_barrier import array_records
from component_strip_certificates import mixed_component_allocation
from strip_incidence_allocation import maximum_run_allocation


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check(path):
    source = json.loads(path.read_text())
    rows, columns = source['shape']
    chosen = {tuple(point) for point in source['selected']}
    edges = {tuple(sorted(tuple(point) for point in edge)) for edge in source['matching']}
    actual_endpoints = {point for edge in edges for point in edge}
    current = rows, columns, chosen, list(edges)
    verified = verify(current)
    root = min(actual_endpoints)
    solver, selected, endpoints, matching, _, charge = encoding(
        rows, columns, 1, 10, root, require_frozen=True)
    exclude_certificates(solver, selected, endpoints, rows, columns, certificate=None)
    solver.add([variable == (point in chosen) for point, variable in selected.items()])
    solver.add([variable == (point in actual_endpoints) for point, variable in endpoints.items()])
    solver.add([variable == (edge in edges) for edge, variable in matching.items()])
    status = solver.check()
    assert status == z3.sat
    assert solver.model().eval(charge).as_long() == verified['receiver_charge']
    return dict(source=str(path), shape=[rows, columns], root=root, status=str(status),
                original_receiver_charge=verified['receiver_charge'],
                independently_frozen=verified['fully_frozen'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = [check(Path('develop')/name) for name in (
        'capacity_one_strip_obstruction.json', 'remote_deficit_frozen_obstruction.json')]
    tiles, runs = array_records(2, 3)
    shape_patterns = 0
    shape_accepted = 0
    mixed_shape_accepted = 0
    for capacities in itertools.product(range(3), repeat=len(tiles)):
        residual = dict(zip(tiles, capacities))
        chosen = {(2*row, 2*column+offset) for (row, column), capacity in residual.items()
                  for offset in range(2-capacity)}
        points = list(itertools.product(range(4), range(6)))
        selected = {point: z3.BoolVal(point in chosen) for point in points}
        endpoints = {point: z3.BoolVal(False) for point in points}
        solver = z3.Solver()
        first_balanced_shape(solver, selected, endpoints, 4, 6)
        status = solver.check()
        assert status in (z3.sat, z3.unsat)
        rank = maximum_run_allocation(runs, residual)['rank']
        assert (status == z3.sat) == (sum(capacities) == 4 and rank == 3)
        shape_patterns += 1
        shape_accepted += status == z3.sat
        mixed_solver = z3.Solver()
        first_mixed_shape(mixed_solver, selected, endpoints, 4, 6)
        mixed_status = mixed_solver.check()
        assert mixed_status in (z3.sat, z3.unsat)
        mixed = mixed_component_allocation(runs, residual)
        assert (mixed_status == z3.sat) == (5 <= sum(capacities) <= 6 and mixed['credits'] == 4)
        mixed_shape_accepted += mixed_status == z3.sat
    assert shape_accepted == 9
    assert mixed_shape_accepted == 60
    report = dict(status='PASS', z3_version=z3.get_version_string(), positive_controls=records,
                  shape_encoding_patterns=shape_patterns, accepted_resource_shapes=shape_accepted,
                  accepted_first_mixed_resource_shapes=mixed_shape_accepted,
                  scope='Both known fully frozen no-four-corner fixtures satisfy the '
                        'base SMT constraints with their exact T/P/matching labels. '
                        'The encoded charge equals the independently checked original '
                        'corrected receiver charge. This excludes vacuous negative '
                        'searches caused by rejecting these fixtures at the base level; '
                        'The direct doubled-tile shape encoding agrees with independent '
                        'rank and capacity on all729abstract patterns, accepting exactly nine. '
                        'The new first-mixed encoding agrees with the independently allocated '
                        'mixed score on those same patterns, accepting exactly60. '
                        'These patterns test resource algebra, not physical feasibility. '
                        'This does not establish full search completeness or general coverage.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
