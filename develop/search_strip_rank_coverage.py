"""Finite discovery of a frozen receiver exceeding the exact strip incidence rank."""

import argparse
import itertools
import json
from pathlib import Path
import time

import z3

from check_two_leg_corner_obstruction import saturated_endpoint_donors
from component_strip_certificates import mixed_component_allocation
from local_quota_strip_allocation import local_quota_allocation
from owned_corner_witnesses import physical_donors
from sealed_strip_allocation import maximal_strips
from search_frozen_receiver_ceiling import count, encoding, verify
from search_strip_coverage import exclude_certificates
from strip_incidence_allocation import maximum_run_allocation


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def rank_cover(solver, selected, endpoints, rows, columns):
    tiles = list(itertools.product(range(rows//2), range(columns//2)))
    cells = {tile: {(2*tile[0]+first, 2*tile[1]+second)
                    for first, second in itertools.product((0, 1), repeat=2)} for tile in tiles}
    occupied = {tile: z3.Or([endpoints[point] for point in cells[tile]]) for tile in tiles}
    residual = {tile: z3.If(occupied[tile], 0, 2-count(selected[point] for point in cells[tile]))
                for tile in tiles}
    covered_by_axis = [{tile: [] for tile in tiles} for _ in range(2)]
    run_cost = []
    for axis, horizontal in enumerate((True, False)):
        bands, length = (rows//2, columns//2) if horizontal else (columns//2, rows//2)
        for band in range(bands):
            tile_at = lambda index: (band, index) if horizontal else (index, band)
            for start in range(length):
                for stop in range(start+1, length+1):
                    actual = [z3.Not(occupied[tile_at(index)]) for index in range(start, stop)]
                    if start:
                        actual.append(occupied[tile_at(start-1)])
                    if stop < length:
                        actual.append(occupied[tile_at(stop)])
                    covered = z3.Bool('covered_%d_%d_%d_%d' % (axis, band, start, stop))
                    solver.add(z3.Implies(covered, z3.And(actual)))
                    run_cost.append(covered)
                    for index in range(start, stop):
                        covered_by_axis[axis][tile_at(index)].append(covered)
    uncovered_slots = []
    for tile in tiles:
        both_runs = z3.And([z3.Or(covered_by_axis[axis][tile]) for axis in range(2)])
        uncovered_slots.append(z3.If(both_runs, 0, residual[tile]))
    return count(run_cost)+z3.Sum(uncovered_slots)


def first_balanced_shape(solver, selected, endpoints, rows, columns):
    tiles = list(itertools.product(range(rows//2), range(columns//2)))
    occupied = {}
    positive = {}
    for tile in tiles:
        cells = [(2*tile[0]+local_row, 2*tile[1]+local_column)
                 for local_row, local_column in itertools.product((0, 1), repeat=2)]
        occupied[tile] = z3.Or([endpoints[point] for point in cells])
        selected_count = count(selected[point] for point in cells)
        solver.add(z3.Or(occupied[tile], selected_count == 0, selected_count == 2))
        positive[tile] = z3.And(z3.Not(occupied[tile]), selected_count == 0)
    solver.add(count(positive.values()) == 2)
    shared = []
    for horizontal in (True, False):
        bands, length = (rows//2, columns//2) if horizontal else (columns//2, rows//2)
        for band in range(bands):
            tile_at = lambda index: (band, index) if horizontal else (index, band)
            for first in range(length):
                for second in range(first+1, length):
                    shared.append(z3.And(positive[tile_at(first)], positive[tile_at(second)],
                        z3.And([z3.Not(occupied[tile_at(index)])
                                for index in range(first, second+1)])))
    solver.add(z3.Or(shared))


def first_mixed_shape(solver, selected, endpoints, rows, columns, exclude_leaves=False):
    tiles = list(itertools.product(range(rows//2), range(columns//2)))
    occupied = {}
    capacities = {}
    for tile in tiles:
        cells = [(2*tile[0]+local_row, 2*tile[1]+local_column)
                 for local_row, local_column in itertools.product((0, 1), repeat=2)]
        occupied[tile] = z3.Or([endpoints[point] for point in cells])
        capacities[tile] = z3.If(occupied[tile], 0,
                                 2-count(selected[point] for point in cells))
    active = []
    weighted = []
    for horizontal in (True, False):
        bands, length = (rows//2, columns//2) if horizontal else (columns//2, rows//2)
        for band in range(bands):
            tile_at = lambda index: (band, index) if horizontal else (index, band)
            for start in range(length):
                for stop in range(start+1, length+1):
                    actual = [z3.Not(occupied[tile_at(index)]) for index in range(start, stop)]
                    if start:
                        actual.append(occupied[tile_at(start-1)])
                    if stop < length:
                        actual.append(occupied[tile_at(stop)])
                    maximal = z3.And(actual)
                    capacity = z3.Sum([capacities[tile_at(index)] for index in range(start, stop)])
                    if exclude_leaves:
                        solver.add(z3.Implies(maximal, capacity != 1))
                    active.append(z3.And(maximal, capacity > 0))
                    weighted.append(z3.If(maximal, capacity/2, 0))
    total = z3.Sum(list(capacities.values()))
    solver.add(total >= 5, total <= 6, count(active) == 4, z3.Sum(weighted) <= 4)


def search(rows, columns, timeout, fixed_geometry=None, require_frozen=True,
           first_balanced_obstruction=False, first_mixed_obstruction=False,
           first_local_quota_obstruction=False):
    assert sum((first_balanced_obstruction, first_mixed_obstruction,
                first_local_quota_obstruction)) <= 1
    actual_endpoints = None
    if fixed_geometry is not None:
        rows, columns = fixed_geometry['shape']
        fixed_matching = {tuple(sorted(tuple(point) for point in edge))
                          for edge in fixed_geometry['matching']}
        actual_endpoints = {point for edge in fixed_matching for point in edge}
        assert actual_endpoints
    root = min(actual_endpoints) if actual_endpoints is not None else (2, 2)
    solver, selected, endpoints, matching, _, charge = encoding(
        rows, columns, 1, timeout, root, require_frozen=require_frozen)
    if actual_endpoints is not None:
        assert actual_endpoints <= set(endpoints)
        assert fixed_matching <= set(matching)
        solver.add([variable == (point in actual_endpoints)
                    for point, variable in endpoints.items()])
        solver.add([variable == (edge in fixed_matching)
                    for edge, variable in matching.items()])
    exclude_certificates(solver, selected, endpoints, rows, columns, certificate=None)
    if first_balanced_obstruction:
        first_balanced_shape(solver, selected, endpoints, rows, columns)
        solver.add(charge == 4)
        cover = z3.IntVal(3)
    elif first_mixed_obstruction or first_local_quota_obstruction:
        first_mixed_shape(solver, selected, endpoints, rows, columns,
                          exclude_leaves=first_local_quota_obstruction)
        solver.add(charge == 5)
        cover = z3.IntVal(4)
    else:
        cover = rank_cover(solver, selected, endpoints, rows, columns)
    solver.add(cover < charge)
    started = time.monotonic()
    status = solver.check()
    report = dict(status=str(status), shape=[rows, columns], timeout_seconds=timeout,
                  fixed_endpoint_geometry=actual_endpoints is not None,
                  require_frozen=require_frozen,
                  first_balanced_obstruction=first_balanced_obstruction,
                  first_mixed_obstruction=first_mixed_obstruction,
                  first_local_quota_obstruction=first_local_quota_obstruction,
                  rank_encoding='exact_two_doubled_tiles_shape' if first_balanced_obstruction
                                else 'four_active_leaf_free_runs_shape' if first_local_quota_obstruction
                                else 'four_active_runs_odd_degree_shape' if first_mixed_obstruction
                                else 'run_slot_vertex_cover',
                  seconds=round(time.monotonic()-started, 3), z3_version=z3.get_version_string(),
                  scope='Finite discovery only. One connected single-terminal endpoint component '
                        'through the recorded root, optionally with strict retained-witness '
                        'freezing. Fixed geometry constrains endpoints and matching but leaves '
                        'all selected labels free. No four-corner donors, and a run-slot bipartite vertex '
                        'cover smaller than the original corrected receiver charge. The cover '
                        'upper-bounds exact one-unit-per-run matching rank. Unknown is not unsat.',
                  root=root)
    if status == z3.sat:
        model = solver.model()
        actual_selected = {point for point, variable in selected.items()
                           if z3.is_true(model.eval(variable))}
        actual_matching = [edge for edge, variable in matching.items()
                           if z3.is_true(model.eval(variable))]
        current = rows, columns, actual_selected, actual_matching
        checked = verify(current, require_frozen=require_frozen)
        assert not physical_donors(current, include_endpoint_guard=True)
        assert not saturated_endpoint_donors(current)
        records, _, residual = maximal_strips(current)
        rank = maximum_run_allocation(records, residual)['rank']
        cover_value = model.eval(cover).as_long()
        assert checked['receiver_charge'] == model.eval(charge).as_long()
        assert rank <= cover_value < checked['receiver_charge']
        if first_balanced_obstruction:
            assert checked['receiver_charge'] == 4 and rank == 3
            assert sum(residual.values()) == 4
            assert checked['ledger']['objective'] == rows*columns//2
            positive = [tile for tile, capacity in residual.items() if capacity]
            assert len(positive) == 2 and all(residual[tile] == 2 for tile in positive)
            assert any(set(positive) <= set(record['tiles']) for record in records)
        if first_mixed_obstruction or first_local_quota_obstruction:
            mixed = mixed_component_allocation(records, residual)
            assert checked['receiver_charge'] == 5 and rank == mixed['credits'] == 4
            assert sum(residual.values()) in (5, 6)
            assert len(mixed['components']) == 1
            assert len(mixed['components'][0]['vertices']) == 4
            report['mixed_certificate'] = mixed
            if first_local_quota_obstruction:
                local = local_quota_allocation(records, residual)
                assert local['credits'] == 4
                assert all(degree >= 2 for _, degree in local['degrees'])
                report['local_quota_certificate'] = local
        report.update(selected=sorted(actual_selected), matching=actual_matching, checked=checked,
                      exact_rank=rank, vertex_cover=cover_value)
    elif status == z3.unknown:
        report['reason_unknown'] = solver.reason_unknown()
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=8)
    parser.add_argument('--columns', type=int, default=10)
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--fixed-geometry', type=Path)
    parser.add_argument('--single-terminal-only', action='store_true')
    first_modes = parser.add_mutually_exclusive_group()
    first_modes.add_argument('--first-balanced-obstruction', action='store_true')
    first_modes.add_argument('--first-mixed-obstruction', action='store_true')
    first_modes.add_argument('--first-local-quota-obstruction', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    fixed = json.loads(arguments.fixed_geometry.read_text()) if arguments.fixed_geometry else None
    report = search(arguments.rows, arguments.columns, arguments.timeout, fixed,
                    require_frozen=not arguments.single_terminal_only,
                    first_balanced_obstruction=arguments.first_balanced_obstruction,
                    first_mixed_obstruction=arguments.first_mixed_obstruction,
                    first_local_quota_obstruction=arguments.first_local_quota_obstruction)
    if arguments.fixed_geometry:
        report['fixed_geometry_source'] = str(arguments.fixed_geometry)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('selected', 'matching', 'checked')}), flush=True)


if __name__ == '__main__':
    main()
