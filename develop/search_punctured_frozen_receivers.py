"""Discover frozen full-tile receivers with holes; finite search only."""

import argparse
import itertools
import json
from pathlib import Path
import time

import z3

from check_component_receivers import verify_terminal
from check_cooperative_promotion import neighbors
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def search(holes, timeout):
    width = 4*holes+2
    endpoints = set(itertools.product(range(6), range(width)))
    for index in range(holes):
        endpoints -= set(itertools.product((2, 3), (4*index+2, 4*index+3)))
    endpoints |= {(0, -1), (0, width)}
    prescribed = {(-1, -1), (0, -2), (-1, width), (0, width+1)}
    candidates = set().union(*(set(neighbors(point)) for point in endpoints))-endpoints
    candidates = {point for point in candidates
                  if len(set(neighbors(point)) & endpoints) == 1}
    assert prescribed <= candidates
    edges = sorted({tuple(sorted((point, other))) for point in endpoints
                    for other in set(neighbors(point)) & endpoints})
    selected = {point: z3.Bool('t_%d_%d' % point) for point in candidates}
    matching = {edge: z3.Bool('m_%d_%d_%d_%d' % (*edge[0], *edge[1])) for edge in edges}
    rank = {point: z3.Int('r_%d_%d' % point) for point in endpoints}
    solver = z3.Solver()
    solver.set(timeout=1000*timeout)
    count = lambda terms: z3.Sum([z3.If(term, 1, 0) for term in terms])
    incident = {point: [edge for edge in edges if point in edge] for point in endpoints}
    for point in prescribed:
        solver.add(selected[point])
    for point in candidates:
        for other in set(neighbors(point)) & candidates:
            solver.add(z3.Not(z3.And(selected[point], selected[other])))
    for point in endpoints:
        solver.add(count(matching[edge] for edge in incident[point]) == 1)
        solver.add(rank[point] >= 0, rank[point] < len(endpoints))
        occupied = len(set(neighbors(point)) & endpoints)
        solver.add(occupied+count(selected[other] for other in set(neighbors(point)) & candidates) >= 3)
        retained = []
        for other in neighbors(point):
            if other in selected:
                retained.append(selected[other])
            if other in endpoints:
                retained.append(z3.Or([z3.And(matching[edge], rank[next(
                    partner for partner in edge if partner != other)] < rank[point])
                    for edge in incident[other]]))
        solver.add(count(retained) >= 2)
    started = time.monotonic()
    status = solver.check()
    report = dict(status=str(status), holes=holes, endpoint_box=[6, width],
                  seconds=round(time.monotonic()-started, 3), timeout_seconds=timeout,
                  scope='Fixed punctured six-row full-tile shape, top corner tails, '
                        'arbitrary independent single-endpoint supports and actual perfect matching. '
                        'Finite discovery only; unknown is not unsat.')
    if status == z3.sat:
        model = solver.model()
        actual_selected = {point for point in candidates if z3.is_true(model.eval(selected[point]))}
        actual_matching = [edge for edge in edges if z3.is_true(model.eval(matching[edge]))]
        occupied = actual_selected | endpoints
        row_offset = 4-min(point[0] for point in occupied)
        column_offset = 4-min(point[1] for point in occupied)
        row_offset += row_offset % 2
        column_offset += column_offset % 2
        move = lambda point: (point[0]+row_offset, point[1]+column_offset)
        rows = max(point[0] for point in occupied)+row_offset+5
        columns = max(point[1] for point in occupied)+column_offset+5
        current = (rows+rows % 2, columns+columns % 2,
                   {move(point) for point in actual_selected},
                   [tuple(move(point) for point in edge) for edge in actual_matching])
        checked = verify_terminal(current)
        assert frozen_certificate(current)[0] == endpoint_data(current)[0]
        assert len(checked['receivers']) == 1
        report.update(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                      checked=checked)
    else:
        report['reason_unknown'] = solver.reason_unknown() if status == z3.unknown else None
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--holes', type=int, required=True)
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert arguments.holes >= 1
    report = search(arguments.holes, arguments.timeout)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key in ('status', 'holes', 'seconds', 'reason_unknown', 'checked')}))


if __name__ == '__main__':
    main()
