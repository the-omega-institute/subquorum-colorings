"""Finite completion search for a fixed complete-source critical U10 seed."""

import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import time

import z3

from check_cooperative_promotion import neighbors
from check_critical_owner_profiles import event_families, inspect
from check_minus_one_tip_obstructions import source
from rotor_networks import combine, transform_module
from search_fusion_fine_budget import count, placements


SPECIFICATIONS = [
    ((26, 12, 4), (False, False, False), (0, 1)),
    ((10, 8, 4), (True, False, False), (1, 3)),
    ((6, 4, 4), (True, True, False), (11, 7)),
    ((6, 4, 20), (False, True, False), (22, 6)),
]


def search(timeout, maximum, nonfull):
    started = time.monotonic()
    rows, columns = 30, 32
    fixed = [transform_module(source(*dimensions), symmetry, offset)
             for dimensions, symmetry, offset in SPECIFICATIONS]
    endpoints = set.union(*(module['endpoints'] for module in fixed))
    assert len(endpoints) == sum(len(module['endpoints']) for module in fixed)
    forbidden = {(13, 2), (13, 3)} | ({(3, 13)} if nonfull else set())
    library = [(dict(fixed=index), module) for index, module in enumerate(fixed)]
    for specification, module in placements(rows, columns):
        if not module['endpoints'] & (endpoints | forbidden):
            library.append((specification, module))
    points = set(itertools.product(range(rows), range(columns)))
    chosen = [z3.Bool('critical10_module_'+str(index)) for index in range(len(library))]
    endpoint_cover, occupied_cover = defaultdict(list), defaultdict(list)
    for choice, (_, module) in zip(chosen, library):
        assert module['endpoints'] | module['selected'] <= points
        for point in module['endpoints']:
            endpoint_cover[point].append(choice)
        for point in module['endpoints'] | module['selected']:
            occupied_cover[point].append(choice)
    endpoint = {point: z3.Bool('critical10_p_%d_%d' % point) for point in points}
    occupied = {point: z3.Bool('critical10_o_%d_%d' % point) for point in points}
    solver = z3.Solver()
    solver.set(timeout=1000*timeout)
    solver.add(*chosen[:4], count(chosen) <= maximum)
    for point in points:
        solver.add(endpoint[point] == z3.Or(endpoint_cover[point]))
        if endpoint_cover[point]:
            solver.add(z3.AtMost(*endpoint_cover[point], 1))
        solver.add(occupied[point] == z3.Or(occupied_cover[point]))
        solver.add(z3.Implies(z3.And(occupied[point], z3.Not(endpoint[point])),
                              count(occupied[other] for other in neighbors(point)
                                    if other in points) <= 1))
    status = solver.check()
    result = dict(status=str(status), shape=[rows, columns], fixed_specifications=SPECIFICATIONS,
                  maximum_modules=maximum, timeout_seconds=timeout,
                  require_nonfull_critical_receiver=nonfull, candidates=len(library),
                  z3_version=z3.get_version_string(),
                  scope='Finite fixed four-source seed completion with all contained U(6,4,4) '
                        'and rotor placements; full original endpoint uniqueness and mandatory '
                        'retained-support degree checked simultaneously, actual neutral contact '
                        'preserved. UNSAT excludes this library/window/seed/count only; UNKNOWN '
                        'excludes nothing. No general realizability or allocation conclusion.')
    if status == z3.sat:
        model = solver.model()
        selected = [(specification, module) for choice, (specification, module) in zip(chosen, library)
                    if z3.is_true(model.eval(choice))]
        modules = [module for _, module in selected]
        network = combine(modules)
        assert len(network['endpoints']) == sum(len(module['endpoints']) for module in modules)
        assert all(len(set(neighbors(point)) & (network['endpoints'] | network['selected'])) <= 1
                   for point in network['selected'])
        regular, critical, _, phases = event_families(modules)
        assert phases[:4] == ['01', '11', '01', '10']
        assert (0, (2, 12), ((-1, 0), (0, 1)), 3) in critical
        assert {(2, 10), (2, 11), (3, 10), (3, 11)} <= network['endpoints']
        if nonfull:
            assert (3, 13) not in network['endpoints']
        result.update(chosen=[specification for specification, _ in selected],
                      matching=[list(edge) for edge in network['matching']],
                      retained_supports=sorted(network['selected']),
                      checked=inspect((rows, columns, network['selected'], network['matching']), modules),
                      ordinary_receivers=len(regular), critical_events=len(critical))
    elif status == z3.unknown:
        result['reason_unknown'] = solver.reason_unknown()
    result['seconds'] = round(time.monotonic()-started, 3)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--maximum-modules', type=int, default=24)
    parser.add_argument('--nonfull', action='store_true')
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = search(arguments.timeout, arguments.maximum_modules, arguments.nonfull)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
