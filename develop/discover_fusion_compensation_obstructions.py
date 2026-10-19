"""Bounded discovery of physical failures of candidate fusion budgets."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_two_leg_corner_obstruction import two_leg_case
from rotor_networks import affine, labeled_module, rotor, transform_module


def supported_modules():
    modules = []
    for width, left, right in itertools.product((6, 8, 10), (4, 6, 8), (4, 6, 8)):
        current, _ = two_leg_case(width, left, right)
        module = labeled_module(current[2], current[3], (), ((3, 2), (3, 1), (2, 3), (1, 3)))
        modules.append((dict(kind='two_leg', width=width, left=left, right=right), module))
    modules.append((dict(kind='rotor'), rotor()))
    return modules


def raw_budget(modules):
    endpoints = set.union(*(module['endpoints'] for module in modules))
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    selected = set.union(*(module['selected'] for module in modules))-endpoints
    occupied = endpoints | selected
    assert all(sum(adjacent in occupied for adjacent in neighbors(point)) == 1 for point in selected)
    degrees = {point: sum(adjacent in occupied for adjacent in neighbors(point)) for point in endpoints}
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    tile = lambda point: tuple(coordinate//2 for coordinate in point)
    tile_counts = Counter(tile(point) for point in endpoints)
    represented = {current: {owners[point] for point in endpoints if tile(point) == current}
                   for current in tile_counts}
    squares = sum(count == 4 and len(represented[current]) > 1 for current, count in tile_counts.items())
    inside = 0
    for module in modules:
        for point in module['endpoints']:
            foreign_new = (set(neighbors(point)) & endpoints)-module['endpoints']-module['selected']
            assert len(foreign_new) == degrees[point]-3
            inside += sum(tile(point) == tile(other) for other in foreign_new)
    positive = 0
    marked = 0
    actual_lost = 0
    for module in modules:
        if module['charge'] <= 0:
            continue
        assert module['charge'] == 1
        positive += 1
        chosen, anchor, opposite, guard = module['guard']
        protectors = (set(neighbors(anchor)) & module['endpoints']) | {guard}
        marked += any(degrees[point] == 4 for point in protectors)
        donor_tile = tile(chosen)
        actual_lost += chosen not in selected or tile_counts[donor_tile] > 0 or sum(
            tile(point) == donor_tile for point in selected) != 1
    negative_mass = positive-sum(module['charge'] for module in modules)
    return dict(charges=[module['charge'] for module in modules], negative_mass=negative_mass,
                degree_four=sum(degree == 4 for degree in degrees.values()), squares=squares,
                inside=inside, marked=marked, actual_lost=actual_lost,
                fine_credit=negative_mass+2*squares-inside-marked,
                actual_single_donor_credit=negative_mass+2*squares-inside-actual_lost)


def pair_controls():
    counts = Counter()
    failures = []
    minimum = None
    modules = supported_modules()
    for first_spec, first in modules:
        for second_spec, second in modules:
            for symmetry in itertools.product((False, True), repeat=3):
                oriented_endpoints = {affine(point, symmetry) for point in second['endpoints']}
                oriented_selected = {affine(point, symmetry) for point in second['selected']}
                offsets = {(adjacent[0]-point[0], adjacent[1]-point[1])
                           for endpoint in first['endpoints'] for adjacent in neighbors(endpoint)
                           for point in oriented_endpoints}
                for offset in sorted(offsets):
                    endpoints_second = {(point[0]+offset[0], point[1]+offset[1]) for point in oriented_endpoints}
                    if first['endpoints'] & endpoints_second:
                        continue
                    endpoints = first['endpoints'] | endpoints_second
                    selected_second = {(point[0]+offset[0], point[1]+offset[1]) for point in oriented_selected}
                    selected = (first['selected'] | selected_second)-endpoints
                    occupied = endpoints | selected
                    if any(sum(adjacent in occupied for adjacent in neighbors(point)) > 1 for point in selected):
                        continue
                    counts['feasible_contact_placements'] += 1
                    moved = transform_module(second, symmetry, offset)
                    for phase in itertools.product(range(2), repeat=2):
                        phased = [transform_module(module, (False, False, False), phase)
                                  for module in (first, moved)]
                        report = raw_budget(phased)
                        counts['phased_cases'] += 1
                        counts['coarse_failures'] += report['degree_four'] > report['negative_mass']+2*report['squares']
                        counts['fine_failures'] += report['fine_credit'] < 0
                        counts['actual_single_donor_failures'] += report['actual_single_donor_credit'] < 0
                        if minimum is None or report['fine_credit'] < minimum:
                            minimum = report['fine_credit']
                        if report['fine_credit'] < 0 and len(failures) < 32:
                            failures.append(dict(first=first_spec, second=second_spec,
                                                 symmetry=symmetry, offset=offset, phase=phase, **report))
    return dict(status='DISCOVERY_ONLY', scope='All ordered pairs in the explicitly listed finite module/parameter family; every relative grid symmetry and every endpoint-contact translation, with all four tile phases. No all-parameter or arbitrary-network conclusion.',
                module_types=len(modules), counts=dict(counts), minimum_fine_credit=minimum, first_failures=failures)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = pair_controls()
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: result[key] for key in ['module_types', 'counts', 'minimum_fine_credit']}))


if __name__ == '__main__':
    main()
