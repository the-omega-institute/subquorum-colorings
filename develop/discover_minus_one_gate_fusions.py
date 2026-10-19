"""Finite discovery of feasible minus-one invasion of a positive donor gate."""

import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import time

import z3

from check_cooperative_promotion import neighbors
from check_minus_one_joint_compensation import inspect
from check_two_leg_corner_obstruction import two_leg_case
from rotor_networks import combine, labeled_module, transform_module, two_leg_module
from search_fusion_fine_budget import count, placements


def extra_placements(rows, columns, parameters, fixed_endpoints):
    seen = set()
    for width, left, right in parameters:
        current, _ = two_leg_case(width, left, right)
        base = labeled_module(current[2], current[3], (),
                              ((3, 2), (3, 1), (2, 3), (1, 3)))
        for symmetry in itertools.product((False, True), repeat=3):
            oriented = transform_module(base, symmetry)
            occupied = oriented['endpoints'] | oriented['selected']
            lower = tuple(min(point[axis] for point in occupied) for axis in (0, 1))
            upper = tuple(max(point[axis] for point in occupied) for axis in (0, 1))
            for row in range(-lower[0], rows-upper[0]):
                for column in range(-lower[1], columns-upper[1]):
                    endpoints = {(first+row, second+column)
                                 for first, second in oriented['endpoints']}
                    if endpoints & fixed_endpoints:
                        continue
                    selected = {(first+row, second+column)
                                for first, second in oriented['selected']}
                    key = frozenset(endpoints), frozenset(selected)
                    if key in seen:
                        continue
                    seen.add(key)
                    module = transform_module(oriented, (False, False, False), (row, column))
                    if module['charge'] in (1, -1):
                        yield dict(kind='extra_two_leg', width=width, left_height=left,
                                   right_height=right, symmetry=symmetry,
                                   offset=(row, column)), module


def search(rows, columns, maximum_modules, timeout, demand, extra_modules=(),
           seed_parameters=(6, 4, 4), tip_rotor_fill=False):
    started = time.monotonic()
    if demand == 'gate':
        fixed = [transform_module(two_leg_module(14, 4), (False, False, False), (6, 6)),
                 transform_module(two_leg_module(6, 4), (False, False, False), (8, 7))]
        assert [module['charge'] for module in fixed] == [1, -1]
        assert not fixed[0]['endpoints'] & fixed[1]['endpoints']
        library = [(dict(kind='fixed_positive', width=14, symmetry=[False]*3, offset=[6, 6]), fixed[0]),
                   (dict(kind='fixed_negative', width=6, symmetry=[False]*3, offset=[8, 7]), fixed[1])]
    else:
        width, left, right = seed_parameters
        current, _ = two_leg_case(width, left, right)
        base = labeled_module(current[2], current[3], (),
                              ((3, 2), (3, 1), (2, 3), (1, 3)))
        fixed = [transform_module(base, (False, False, False), (6, 7))]
        assert fixed[0]['charge'] == -1
        library = [(dict(kind='fixed_negative', width=width, left_height=left,
                         right_height=right, symmetry=[False]*3, offset=[6, 7]), fixed[0])]
    fixed_endpoints = set.union(*(module['endpoints'] for module in fixed))
    for spec, module in placements(rows, columns):
        if module['charge'] not in (1, -1, 0, -2) or module['endpoints'] & fixed_endpoints:
            continue
        library.append((spec, module))
    library.extend(extra_placements(rows, columns, extra_modules, fixed_endpoints))
    points = [(row, column) for row in range(rows) for column in range(columns)]
    endpoint_cover = defaultdict(list)
    occupied_cover = defaultdict(list)
    choices = [z3.Bool('minus_one_module_%d' % index) for index in range(len(library))]
    for index, (_, module) in enumerate(library):
        for point in module['endpoints']:
            endpoint_cover[point].append(choices[index])
        for point in module['endpoints'] | module['selected']:
            assert point in points
            occupied_cover[point].append(choices[index])
    endpoints = {point: z3.Bool('minus_one_p_%d_%d' % point) for point in points}
    occupied = {point: z3.Bool('minus_one_o_%d_%d' % point) for point in points}
    solver = z3.Solver()
    solver.set(timeout=timeout*1000)
    solver.add(*choices[:len(fixed)], count(choices) <= maximum_modules)
    if demand == 'tip':
        solver.add(endpoints[(seed_parameters[1]+6, 9)])
        if tip_rotor_fill:
            tip = seed_parameters[1]+6, 8
            other_corners = {(tip[0], 9), (tip[0]+1, 8), (tip[0]+1, 9)}
            solver.add(z3.Or([choice for choice, (spec, module) in zip(choices, library)
                              if spec['kind'] == 'rotor' and other_corners <= module['endpoints']]))
    for point in points:
        covering = endpoint_cover[point]
        solver.add(endpoints[point] == z3.Or(covering))
        if covering:
            solver.add(z3.AtMost(*covering, 1))
        solver.add(occupied[point] == z3.Or(occupied_cover[point]))
        solver.add(z3.Implies(z3.And(occupied[point], z3.Not(endpoints[point])),
                              count(occupied[other] for other in neighbors(point) if other in occupied) <= 1))
    status = solver.check()
    result = dict(status=str(status), demand=demand, rows=rows, columns=columns, maximum_modules=maximum_modules,
                  timeout_seconds=timeout, candidates=len(library), z3_version=z3.get_version_string(),
                  extra_modules=list(extra_modules),
                  seed_parameters=list(seed_parameters) if demand == 'tip' else None,
                  tip_rotor_fill=tip_rotor_fill,
                  seconds=round(time.monotonic()-started, 3),
                  scope='Finite fixed-seed discovery only. Source library is contained two_leg(6,4,4), rotors and the explicitly listed extra_modules, all orientations; gate mode also requires one two_leg(14,4,4). Two-leg charges restricted to +1/-1. No freezing requirement. UNSAT is only this window/library/seed/count restriction; UNKNOWN excludes nothing.')
    if status == z3.sat:
        model = solver.model()
        chosen = [(spec, module) for choice, (spec, module) in zip(choices, library)
                  if z3.is_true(model.eval(choice))]
        modules = [module for _, module in chosen]
        network = combine(modules)
        physical = inspect((rows, columns, network['selected'], network['matching']), modules)
        assert physical['marked_sides'] > 0 if demand == 'gate' else physical['irregular_tip_events'] > 0
        result.update(chosen=[spec for spec, _ in chosen], checked=physical)
    elif status == z3.unknown:
        result['reason_unknown'] = solver.reason_unknown()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=24)
    parser.add_argument('--columns', type=int, default=28)
    parser.add_argument('--maximum-modules', type=int, default=8)
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--demand', choices=['gate', 'tip'], default='gate')
    parser.add_argument('--extra-module', type=int, nargs=3, action='append', default=[],
                        metavar=('WIDTH', 'LEFT_HEIGHT', 'RIGHT_HEIGHT'))
    parser.add_argument('--seed-module', type=int, nargs=3, default=(6, 4, 4),
                        metavar=('WIDTH', 'LEFT_HEIGHT', 'RIGHT_HEIGHT'))
    parser.add_argument('--tip-rotor-fill', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = search(arguments.rows, arguments.columns, arguments.maximum_modules,
                    arguments.timeout, arguments.demand, arguments.extra_module,
                    arguments.seed_module, arguments.tip_rotor_fill)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
