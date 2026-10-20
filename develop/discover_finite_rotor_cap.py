"""Discover complete finite U caps of a forbidden rotor-only contact."""

import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import time

import z3

from all_phase_joint_slots import inspect_slots
from check_cooperative_promotion import neighbors
from check_regular_tile_compensation import inspect
from check_rotor_only_reserve import source_at
from rotor_networks import combine, transform_module, two_leg_module
from search_fusion_fine_budget import count, placements


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def search(rows, columns, maximum, timeout, cap_width):
    started = time.monotonic()
    seed = [source_at((False, 0, 0)), source_at((False, -3, 0)),
            source_at((False, -1, -3)),
            transform_module(two_leg_module(cap_width, 4), (False, False, False), (-4, -cap_width))]
    shift = 8, max(10, cap_width+2)
    seed = [transform_module(module, (False, False, False), shift) for module in seed]
    endpoints = set.union(set(), *(module['endpoints'] for module in seed))
    assert len(endpoints) == sum(len(module['endpoints']) for module in seed)
    library = [(dict(kind='fixed', index=index), module) for index, module in enumerate(seed)]
    library += [(specification, module) for specification, module in placements(rows, columns)
                if not module['endpoints'] & endpoints]
    points = set(itertools.product(range(rows), range(columns)))
    assert all(module['endpoints'] | module['selected'] <= points for _, module in library)
    endpoint_cover = defaultdict(list)
    occupied_cover = defaultdict(list)
    chosen = [z3.Bool('cap_module_%d' % index) for index in range(len(library))]
    for index, (_, module) in enumerate(library):
        for point in module['endpoints']:
            endpoint_cover[point].append(chosen[index])
        for point in module['endpoints'] | module['selected']:
            occupied_cover[point].append(chosen[index])
    endpoint = {point: z3.Bool('cap_p_%d_%d' % point) for point in points}
    occupied = {point: z3.Bool('cap_o_%d_%d' % point) for point in points}
    solver = z3.Solver()
    solver.set(timeout=1000*timeout)
    solver.add(*chosen[:len(seed)], count(chosen) <= maximum)
    for point in points:
        solver.add(endpoint[point] == z3.Or(endpoint_cover[point]))
        if endpoint_cover[point]:
            solver.add(z3.AtMost(*endpoint_cover[point], 1))
        solver.add(occupied[point] == z3.Or(occupied_cover[point]))
        solver.add(z3.Implies(z3.And(occupied[point], z3.Not(endpoint[point])),
            count(occupied[other] for other in neighbors(point) if other in points) <= 1))
    solver.push()
    solver.add(*[z3.Not(choice) for choice in chosen[len(seed):]])
    assert solver.check() == z3.unsat
    solver.pop()
    status = solver.check()
    result = dict(status=str(status), shape=[rows, columns], maximum_modules=maximum,
                  cap_width=cap_width, seed_shift=shift,
                  timeout_seconds=timeout, candidates=len(library), z3_version=z3.get_version_string(),
                  seed_only_control='UNSAT_complete_retained_supports_fail',
                  scope='Finite discovery only, for a fixed typeA rotor pair and explicit positiveU cap. Library is contained U(6,4,4)/rotor placements with all isometries/phases. Endpoint-disjoint original matching and full retained-support feasibility. UNSAT excludes only this window/library/count; UNKNOWN excludes nothing. A SAT witness obstructs extending the rotor-only event-owner theorem to U mixtures, not the coefficient-one grid inequality.')
    if status == z3.sat:
        selected = [(specification, module) for choice, (specification, module) in zip(chosen, library)
                    if z3.is_true(solver.model().eval(choice))]
        modules = [module for _, module in selected]
        network = combine(modules)
        current = rows, columns, network['selected'], network['matching']
        physical = inspect(current, modules, require_frozen=False)
        slots = inspect_slots(current, modules)
        result.update(chosen=[specification for specification, _ in selected],
                      physical=physical, slots=slots,
                      reserve=slots['negative_mass']+physical['residual_square_credit']-
                              slots['irregular_events']-slots['marked_sides'])
    elif status == z3.unknown:
        result['reason_unknown'] = solver.reason_unknown()
    result['seconds'] = round(time.monotonic()-started, 3)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=24)
    parser.add_argument('--columns', type=int, default=24)
    parser.add_argument('--maximum-modules', type=int, default=32)
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--cap-width', type=int, default=6)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert arguments.cap_width >= 6 and arguments.cap_width % 2 == 0
    result = search(arguments.rows, arguments.columns, arguments.maximum_modules,
                    arguments.timeout, arguments.cap_width)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
