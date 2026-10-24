"""Finite SAT discovery of overlapping physical module budgets."""

import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import time

import z3

from check_cooperative_promotion import neighbors
from check_degree_three_fusion import inspect
from discover_fusion_compensation_obstructions import raw_budget
from rotor_networks import combine, rotor, transform_module, two_leg_module


def count(conditions):
    return z3.Sum([z3.If(condition, 1, 0) for condition in conditions])


def placements(rows, columns):
    result = []
    seen = set()
    for name, base in [('two_leg', two_leg_module(6, 4)), ('rotor', rotor())]:
        for symmetry in itertools.product((False, True), repeat=3):
            oriented = transform_module(base, symmetry)
            occupied = oriented['endpoints'] | oriented['selected']
            lower = tuple(min(point[axis] for point in occupied) for axis in (0, 1))
            upper = tuple(max(point[axis] for point in occupied) for axis in (0, 1))
            for row in range(-lower[0], rows-upper[0]):
                for column in range(-lower[1], columns-upper[1]):
                    module = transform_module(oriented, (False, False, False), (row, column))
                    key = (frozenset(module['endpoints']), frozenset(module['selected']),
                           module['guard'] if module['charge'] > 0 else None)
                    if key in seen:
                        continue
                    seen.add(key)
                    result.append((dict(kind=name, symmetry=symmetry, offset=(row, column)), module))
    return result


def search(rows, columns, timeout, maximum_modules, anchor_offset=None):
    started = time.monotonic()
    library = placements(rows, columns)
    points = list(itertools.product(range(rows), range(columns)))
    selected = [z3.Bool('module_%d' % index) for index in range(len(library))]
    endpoint_cover = defaultdict(list)
    occupied_cover = defaultdict(list)
    full_tile_cover = defaultdict(list)
    for index, (spec, module) in enumerate(library):
        for point in module['endpoints']:
            endpoint_cover[point].append(index)
        for point in module['endpoints'] | module['selected']:
            occupied_cover[point].append(index)
        for tile in module['receiver']:
            if sum((row//2, column//2) == tile for row, column in module['endpoints']) == 4:
                full_tile_cover[tile].append(index)
    endpoints = {point: z3.Bool('p_%d_%d' % point) for point in points}
    occupied = {point: z3.Bool('o_%d_%d' % point) for point in points}
    solver = z3.Solver()
    solver.set(timeout=timeout*1000)
    solver.add(count(selected) >= 3, count(selected) <= maximum_modules)
    if anchor_offset is not None:
        anchor = transform_module(two_leg_module(6, 4), (False, False, False), anchor_offset)
        anchors = [index for index, (_, module) in enumerate(library)
                   if module['endpoints'] == anchor['endpoints'] and module['selected'] == anchor['selected']
                   and module['guard'] == anchor['guard']]
        assert len(anchors) == 1
        solver.add(selected[anchors[0]])
    for point in points:
        covering = [selected[index] for index in endpoint_cover[point]]
        solver.add(endpoints[point] == z3.Or(covering))
        if covering:
            solver.add(z3.AtMost(*covering, 1))
        solver.add(occupied[point] == z3.Or([selected[index] for index in occupied_cover[point]]))
        solver.add(z3.Implies(z3.And(occupied[point], z3.Not(endpoints[point])),
                              count(occupied[other] for other in neighbors(point) if other in occupied) <= 1))
    squares = []
    for row, column in itertools.product(range(rows//2), range(columns//2)):
        cells = [(2*row+local_row, 2*column+local_column)
                 for local_row, local_column in itertools.product(range(2), repeat=2)]
        squares.append(z3.And([endpoints[point] for point in cells]+
                              [z3.Not(z3.Or([selected[index] for index in full_tile_cover[row, column]]))]))
    inside = []
    marked = []
    for index, (_, module) in enumerate(library):
        original_occupied = module['endpoints'] | module['selected']
        for point in module['endpoints']:
            missing = set(neighbors(point))-original_occupied
            assert len(missing) == 1
            other = next(iter(missing))
            if other in endpoints and tuple(value//2 for value in point) == tuple(value//2 for value in other):
                inside.append(z3.And(selected[index], endpoints[other]))
        if module['charge'] <= 0:
            continue
        chosen, anchor, opposite, guard = module['guard']
        protectors = (set(neighbors(anchor)) & module['endpoints']) | {guard}
        missing = set.union(*(set(neighbors(point))-original_occupied for point in protectors))
        marked.append(z3.And(selected[index], z3.Or([endpoints[point] for point in missing if point in endpoints])))
    negative_mass = z3.Sum([z3.If(selected[index], max(0, -module['charge']), 0)
                           for index, (_, module) in enumerate(library)])
    fine_credit = negative_mass+2*count(squares)-count(inside)-count(marked)
    control = None
    if rows >= 16 and columns >= 16 and anchor_offset in (None, (2, 2)):
        control_modules = [transform_module(two_leg_module(6, 4), (False, False, False), offset)
                           for offset in [(2, 2), (10, 2)]]
        control_modules.append(transform_module(rotor(), (False, False, False), (10, 10)))
        control_indices = []
        for expected in control_modules:
            candidates = [index for index, (_, module) in enumerate(library)
                          if module['endpoints'] == expected['endpoints'] and
                          module['selected'] == expected['selected'] and
                          (module['charge'] <= 0 or module['guard'] == expected['guard'])]
            assert candidates
            control_indices.append(candidates[0])
        solver.push()
        solver.add(*[variable == (index in control_indices) for index, variable in enumerate(selected)])
        assert solver.check() == z3.sat
        model = solver.model()
        raw = raw_budget(control_modules)
        assert model.eval(fine_credit).as_long() == raw['fine_credit'] == 2
        network = combine(control_modules)
        physical = inspect((rows, columns, network['selected'], network['matching']), control_modules,
                           allow_degree_four=True)
        assert physical['certified_slack_lower_bound'] == 2
        control = dict(status='PASS', modules=3, fine_credit=2,
                       check='A fixed feasible fully frozen three-module assignment agrees between SAT and independent physical ledgers.')
        solver.pop()
    solver.add(fine_credit < 0)
    status = solver.check()
    result = dict(status=str(status), rows=rows, columns=columns, maximum_modules=maximum_modules,
                  fixed_anchor_offset=anchor_offset, module_types='two_leg(6,4,4), rotor; all contained placements/guards, with union occupancy and retained-support feasibility',
                  placements=len(library), z3_version=z3.get_version_string(), timeout_seconds=timeout,
                  positive_encoding_control=control,
                  seconds=round(time.monotonic()-started, 3),
                  scope='Finite discovery only. UNSAT covers this window/library/anchor/module-count restriction, UNKNOWN is not exclusion. No freezing assumed by the search.')
    if status == z3.sat:
        model = solver.model()
        chosen = [(spec, module) for index, (spec, module) in enumerate(library)
                  if z3.is_true(model.eval(selected[index]))]
        modules = [module for spec, module in chosen]
        network = combine(modules)
        report = raw_budget(modules)
        assert model.eval(fine_credit).as_long() == report['fine_credit'] < 0
        physical = inspect((rows, columns, network['selected'], network['matching']), modules,
                           require_frozen=False, allow_degree_four=True)
        assert physical['certified_slack_lower_bound'] == report['fine_credit']
        result.update(chosen=[spec for spec, module in chosen], budget=report, physical=physical)
    elif status == z3.unknown:
        result['reason_unknown'] = solver.reason_unknown()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=16)
    parser.add_argument('--columns', type=int, default=16)
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--maximum-modules', type=int, default=6)
    parser.add_argument('--anchor-row', type=int)
    parser.add_argument('--anchor-column', type=int)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert arguments.rows % 2 == arguments.columns % 2 == 0
    assert (arguments.anchor_row is None) == (arguments.anchor_column is None)
    anchor = None if arguments.anchor_row is None else (arguments.anchor_row, arguments.anchor_column)
    result = search(arguments.rows, arguments.columns, arguments.timeout, arguments.maximum_modules, anchor)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
