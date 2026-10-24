"""Find finite frozen receivers outside the capped-corner sufficient criterion."""

import argparse
import itertools
import json
from pathlib import Path
import time

from check_component_receivers import verify_terminal
from check_cooperative_promotion import neighbors
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check


def corner_patterns(top, left):
    for transpose, flip_row, flip_column in itertools.product((False, True), repeat=3):
        def move(point):
            row, column = point
            row = 1-row if flip_row else row
            column = 1-column if flip_column else column
            if transpose:
                row, column = column, row
            return top+row, left+column
        yield ([move(point) for point in ((-1, -1), (-1, 0), (-1, 1), (-1, 2), (0, -1))],
               move((1, -1)), [move(point) for point in ((0, 0), (0, 1))])


def witnesses(rows, columns, selected, endpoints):
    result = []
    for top, left in itertools.product(range(0, rows, 2), range(0, columns, 2)):
        for orientation, (required, support, excluded) in enumerate(corner_patterns(top, left)):
            if set(required) <= endpoints and support in selected and not set(excluded) & endpoints:
                result.append(dict(square=[top, left], orientation=orientation))
    return result


def search(rows, columns, charge_twice, exclude_corners, timeout, negative_band=None,
           require_freezing=True):
    import z3

    vertices = list(itertools.product(range(rows), range(columns)))
    domain = set(vertices)
    adjacency = {point: sorted(set(neighbors(point)) & domain) for point in vertices}
    edges = [(point, other) for point in vertices for other in adjacency[point] if point < other]
    selected = {point: z3.Bool('t_%s_%s' % point) for point in vertices}
    endpoints = {point: z3.Bool('p_%s_%s' % point) for point in vertices}
    matching = {edge: z3.Bool('m_%s_%s_%s_%s' % (*edge[0], *edge[1])) for edge in edges}
    distance = {point: z3.Int('d_%s_%s' % point) for point in vertices}
    freeze = {point: z3.Int('f_%s_%s' % point) for point in vertices}
    root = (3, 3)
    solver = z3.Solver()
    solver.set(timeout=timeout*1000)

    def count(expressions):
        return z3.Sum([z3.If(expression, 1, 0) for expression in expressions])

    def matched(first, second):
        return matching[tuple(sorted((first, second)))]

    for point in vertices:
        solver.add(z3.Not(z3.And(selected[point], endpoints[point])))
        solver.add(count(matched(point, other) for other in adjacency[point]) ==
                   z3.If(endpoints[point], 1, 0))
        occupied = count(z3.Or(selected[other], endpoints[other]) for other in adjacency[point])
        solver.add(z3.Implies(selected[point], occupied <= 1))
        solver.add(z3.Implies(endpoints[point], occupied >= 3))
        if min(point) < 2 or point[0] >= rows-2 or point[1] >= columns-2:
            solver.add(z3.Not(endpoints[point]))
        solver.add(distance[point] >= 0, distance[point] < len(vertices))
        if point != root:
            solver.add(z3.Implies(endpoints[point], z3.Or([
                z3.And(endpoints[other], distance[other] < distance[point])
                for other in adjacency[point]])))
        solver.add(freeze[point] >= 0, freeze[point] < len(vertices))
        retained = [z3.Or(selected[other], z3.Or([
            z3.And(matched(other, mate), freeze[mate] < freeze[point])
            for mate in adjacency[other]])) for other in adjacency[point]]
        if require_freezing:
            solver.add(z3.Implies(endpoints[point], count(retained) >= 2))
    solver.add(endpoints[root], distance[root] == 0)
    receiver_terms = []
    for top, left in itertools.product(range(0, rows, 2), range(0, columns, 2)):
        corners = list(itertools.product((top, top+1), (left, left+1)))
        has_endpoint = z3.Or([endpoints[point] for point in corners])
        receiver_terms.append(z3.If(has_endpoint,
            2*count(selected[point] for point in corners)+count(endpoints[point] for point in corners)-4, 0))
        if exclude_corners:
            for required, support, excluded in corner_patterns(top, left):
                if not (set(required) | {support} | set(excluded)) <= domain:
                    continue
                solver.add(z3.Not(z3.And([endpoints[point] for point in required]+
                    [selected[support]]+[z3.Not(endpoints[point]) for point in excluded])))
    solver.add(z3.Sum(receiver_terms) >= charge_twice)
    if negative_band:
        horizontal = negative_band == 'horizontal'
        gains = []
        for band in range((rows if horizontal else columns)//2):
            physical, shifted = [], []
            for along in range(0, columns if horizontal else rows, 2):
                corners = [(2*band+across, along+offset) if horizontal else
                           (along+offset, 2*band+across)
                           for across, offset in itertools.product((0, 1), repeat=2)]
                physical.append(z3.If(z3.Or([endpoints[point] for point in corners]),
                    2*count(selected[point] for point in corners)+
                    count(endpoints[point] for point in corners)-4, 0))
            for along in range(1, (columns if horizontal else rows)-1, 2):
                corners = [(2*band+across, along+offset) if horizontal else
                           (along+offset, 2*band+across)
                           for across, offset in itertools.product((0, 1), repeat=2)]
                shifted.append(z3.If(z3.Or([endpoints[point] for point in corners]),
                    2*count(selected[point] for point in corners)+
                    count(endpoints[point] for point in corners)-4, 0))
            gains.append(z3.Sum(physical)-z3.Sum(shifted))
        solver.add(z3.Or([gain < 0 for gain in gains]))
    started = time.monotonic()
    status = solver.check()
    result = dict(shape=[rows, columns], minimum_charge_twice=charge_twice,
                  corners_excluded=exclude_corners, negative_band=negative_band,
                  require_freezing=require_freezing,
                  seconds=round(time.monotonic()-started, 3),
                  solver_status=str(status), scope='Finite discovery; unsat/unknown gives no general theorem.')
    if status != z3.sat:
        result['reason_unknown'] = solver.reason_unknown() if status == z3.unknown else None
        return result
    model = solver.model()
    actual_selected = {point for point in vertices if z3.is_true(model.eval(selected[point]))}
    actual_matching = [edge for edge in edges if z3.is_true(model.eval(matching[edge]))]
    actual_endpoints = {point for edge in actual_matching for point in edge}
    current = rows, columns, actual_selected, actual_matching
    direct_check(*current)
    checked = verify_terminal(current)
    assert len(checked['receivers']) == 1
    assert checked['receivers'][0]['charge_twice'] >= charge_twice
    frozen, layers = frozen_certificate(current)
    assert not require_freezing or frozen == actual_endpoints
    found = witnesses(rows, columns, actual_selected, actual_endpoints)
    assert not exclude_corners or not found
    if negative_band:
        from check_elbow_sources import phase
        actual_gains = []
        for band in range((rows if horizontal else columns)//2):
            cells = {point for point in vertices if point[0 if horizontal else 1]//2 == band}
            actual_gains.append(phase(current, cells, horizontal))
        assert min(actual_gains) < 0
        result['band_gains'] = actual_gains
    result.update(selected=sorted(actual_selected), matching=actual_matching, receiver=checked,
                  corner_witnesses=found, freezing_layers=layers,
                  frozen_endpoints=len(frozen),
                  labels=[''.join('P' if (row, column) in actual_endpoints else
                                  'T' if (row, column) in actual_selected else '.'
                                  for column in range(columns)) for row in range(rows)])
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=10)
    parser.add_argument('--columns', type=int, default=10)
    parser.add_argument('--charge-twice', type=int, default=2)
    parser.add_argument('--exclude-corners', action='store_true')
    parser.add_argument('--timeout', type=int, default=45)
    parser.add_argument('--negative-band', choices=('horizontal', 'vertical'))
    parser.add_argument('--no-freezing', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert arguments.rows >= 8 and arguments.columns >= 8
    assert arguments.rows % 2 == arguments.columns % 2 == 0
    result = search(arguments.rows, arguments.columns, arguments.charge_twice,
                    arguments.exclude_corners, arguments.timeout, arguments.negative_band,
                    not arguments.no_freezing)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key not in
                      ('matching', 'selected', 'freezing_layers')}), flush=True)


if __name__ == '__main__':
    main()
