"""Discover fully frozen receivers with no four-rule donor or sealed maximal run."""

import argparse
import itertools
import json
from pathlib import Path
import time

import z3

from check_cooperative_promotion import neighbors
from check_two_leg_corner_obstruction import saturated_endpoint_donors
from owned_corner_witnesses import physical_donors
from sealed_strip_allocation import maximal_strips, sealed_strips
from search_corner_coverage import corner_patterns
from search_frozen_receiver_ceiling import count, encoding, verify


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def exclude_certificates(solver, selected, endpoints, rows, columns, certificate='sealed'):
    domain = set(selected)
    tiles = list(itertools.product(range(rows//2), range(columns//2)))
    cells = {tile: {(2*tile[0]+first, 2*tile[1]+second)
                    for first, second in itertools.product((0, 1), repeat=2)} for tile in tiles}
    occupied_tile = {tile: z3.Or([endpoints[point] for point in cells[tile]]) for tile in tiles}
    for tile in tiles:
        for required, support, excluded in corner_patterns(2*tile[0], 2*tile[1]):
            if not (set(required) | {support} | set(excluded)) <= domain:
                continue
            solver.add(z3.Not(z3.And([endpoints[point] for point in required] +
                [selected[support]] + [z3.Not(endpoints[point]) for point in excluded])))
        for chosen in cells[tile]:
            exterior_anchor = (set(neighbors(chosen))-cells[tile]) & domain
            anchor = z3.Or([endpoints[point] for point in exterior_anchor])
            opposite = tuple(4*coordinate+1-value for coordinate, value in zip(tile, chosen))
            exterior = (set(neighbors(opposite))-cells[tile]) & domain
            forbidden = []
            for guard in exterior:
                other_neighbors = (set(neighbors(guard))-{opposite}) & domain
                forbidden.append(z3.And(selected[guard], z3.Or([
                    endpoints[point] for point in other_neighbors])))
                forbidden.append(z3.And(endpoints[guard],
                    count(endpoints[point] for point in other_neighbors) == 3,
                    count(z3.Or(endpoints[point], selected[point])
                          for point in (set(neighbors(guard)) & domain)) <= 3))
            forbidden.append(count(endpoints[point] for point in exterior) == 2)
            solver.add(z3.Not(z3.And(z3.Not(occupied_tile[tile]), selected[chosen],
                                     anchor, z3.Or(forbidden))))
    intervals = 0
    for horizontal in (True, False):
        bands, length = (rows//2, columns//2) if horizontal else (columns//2, rows//2)
        for band in range(bands):
            tile_at = lambda position: (band, position) if horizontal else (position, band)
            for start in range(length):
                for stop in range(start+1, length+1):
                    maximal = [z3.Not(occupied_tile[tile_at(position)])
                               for position in range(start, stop)]
                    if start > 0:
                        maximal.append(occupied_tile[tile_at(start-1)])
                    if stop < length:
                        maximal.append(occupied_tile[tile_at(stop)])
                    boundary = {(2*band+local, along) if horizontal else (along, 2*band+local)
                                for local in (0, 1) for along in (2*start, 2*stop-1)}
                    if certificate == 'sealed':
                        solver.add(z3.Implies(z3.And(maximal),
                                             z3.Or([selected[point] for point in boundary])))
                    else:
                        strip_cells = set.union(*(cells[tile_at(position)]
                                                  for position in range(start, stop)))
                        solver.add(z3.Implies(z3.And(maximal),
                            count(selected[point] for point in strip_cells) >= 2*(stop-start)-1))
                    intervals += 1
    return intervals


def search(rows, columns, timeout, certificate='sealed'):
    solver, selected, endpoints, matching, _, _ = encoding(
        rows, columns, 1, timeout, (2, 2), require_frozen=True)
    intervals = exclude_certificates(solver, selected, endpoints, rows, columns, certificate)
    started = time.monotonic()
    status = solver.check()
    report = dict(status=str(status), shape=[rows, columns], timeout_seconds=timeout,
                  seconds=round(time.monotonic()-started, 3), z3_version=z3.get_version_string(),
                  interval_predicates=intervals,
                  excluded_strip_certificate=certificate,
                  scope='Finite discovery: one connected fully frozen endpoint component '
                        'through (2,2), corrected charge at least one, no donor from the '
                        'four corner rules and no maximal endpoint-free run satisfying '
                        'the specified sealed or actual-capacity-at-least-two certificate. '
                        'Unsat is finite only and unknown is not unsat.')
    if status == z3.sat:
        model = solver.model()
        actual_selected = {point for point, variable in selected.items()
                           if z3.is_true(model.eval(variable))}
        actual_matching = [edge for edge, variable in matching.items()
                           if z3.is_true(model.eval(variable))]
        current = rows, columns, actual_selected, actual_matching
        checked = verify(current)
        assert checked['receiver_charge'] >= 1
        assert not physical_donors(current, include_endpoint_guard=True)
        assert not saturated_endpoint_donors(current)
        if certificate == 'sealed':
            assert not sealed_strips(current)[0]
        else:
            assert all(record['capacity'] <= 1 for record in maximal_strips(current)[0])
        report.update(selected=sorted(actual_selected), matching=actual_matching, checked=checked)
    elif status == z3.unknown:
        report['reason_unknown'] = solver.reason_unknown()
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=8)
    parser.add_argument('--columns', type=int, default=10)
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--certificate', choices=('sealed', 'capacity'), default='sealed')
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = search(arguments.rows, arguments.columns, arguments.timeout, arguments.certificate)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('selected', 'matching', 'checked')}), flush=True)


if __name__ == '__main__':
    main()
