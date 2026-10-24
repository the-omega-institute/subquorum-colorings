"""Discover selected-only completions pushing whole-receiver deficit beyond a radius."""

import argparse
import itertools
import json
from pathlib import Path
import time

import z3

from check_component_receivers import verify_terminal, vertices_of
from check_cooperative_promotion import neighbors
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_remote_deficit_obstruction import fixture, tile_resources
from search_frozen_receiver_ceiling import count


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def search(radius, timeout):
    assert radius >= 1
    original, certificate = fixture()
    margin = 2*(radius+1)
    move = lambda point: (point[0]+margin, point[1]+margin)
    endpoints = {move(point) for point in endpoint_data(original)[0]}
    matching = [tuple(move(point) for point in edge) for edge in original[3]]
    rows, columns = original[0]+2*margin, original[1]+2*margin
    domain = set(itertools.product(range(rows), range(columns)))
    receiver = {(row//2, column//2) for row, column in endpoints}
    receiver_cells = vertices_of(receiver)
    original_selected = {move(point) for point in original[2]}
    mandatory = {point for point in original_selected
                 if point in receiver_cells or set(neighbors(point)) & endpoints}
    selected = {point: z3.Bool('selected_%d_%d' % point) for point in sorted(domain)}
    solver = z3.Solver()
    solver.set(timeout=timeout*1000)
    for point in sorted(domain):
        if point in endpoints:
            solver.add(z3.Not(selected[point]))
        if point in mandatory:
            solver.add(selected[point])
        if point in receiver_cells and point not in original_selected:
            solver.add(z3.Not(selected[point]))
        adjacent = set(neighbors(point)) & domain
        degree = count(z3.Or(selected[other], z3.BoolVal(other in endpoints)) for other in adjacent)
        solver.add(z3.Implies(selected[point], degree <= 1))
    for tile in itertools.product(range(rows//2), range(columns//2)):
        if tile in receiver:
            continue
        distance = min(max(abs(first-second) for first, second in zip(tile, other))
                       for other in receiver)
        if distance <= radius:
            solver.add(count(selected[point] for point in vertices_of({tile})) == 2)
    started = time.monotonic()
    status = solver.check()
    report = dict(status=str(status), radius=radius, shape=[rows, columns], margin=margin,
                  seconds=round(time.monotonic()-started, 3), timeout_seconds=timeout,
                  z3_version=z3.get_version_string(),
                  scope='Selected-only discovery with the fixed 28-endpoint matching, original '
                        'receiver labels and all original endpoint-adjacent supports retained. '
                        'Every endpoint-free tile within Chebyshev physical tile radius R must '
                        'have two selections. Finite unsat does not refute other templates or '
                        'prove a radius bound; sat is an explicit completion, not an all-R proof.')
    if status == z3.sat:
        model = solver.model()
        actual_selected = {point for point in selected if z3.is_true(model.eval(selected[point]))}
        current = rows, columns, actual_selected, matching
        assert mandatory <= actual_selected
        assert actual_selected & receiver_cells == original_selected & receiver_cells
        assert frozen_certificate(current)[0] == endpoints
        ledger = verify_terminal(current)
        assert ledger['receivers'][0]['charge_twice'] == 2
        resources = tile_resources(current)
        assert all(record['deficit'] == 0 for record in resources if record['corner_tile_distance'] <= radius)
        report.update(selected=sorted(actual_selected), matching=matching,
                      freezing_certificate=[tuple(move(point) for point in row) for row in certificate],
                      receiver=ledger['receivers'][0], no_endpoint_deficit=ledger['empty_deficit'],
                      nearest_positive_deficit=min(record['corner_tile_distance'] for record in resources
                                                   if record['deficit'] > 0))
    elif status == z3.unknown:
        report['reason_unknown'] = solver.reason_unknown()
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--radius', type=int, required=True)
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = search(arguments.radius, arguments.timeout)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {'selected', 'matching', 'freezing_certificate'}}))


if __name__ == '__main__':
    main()
