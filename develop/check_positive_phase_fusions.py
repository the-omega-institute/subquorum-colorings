"""Coordinate controls for automatic compensation in positive-phase fusions."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from check_two_leg_corner_obstruction import two_leg_case
from degree_four_overcount import opposed_bands
from degree_three_fusion import four_way, occupied_bands
from discover_fusion_compensation_obstructions import supported_modules
from dual_guard_compensation import inspect as inspect_dual
from rotor_networks import chain, combine, labeled_module, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check_profile(module):
    assert module['charge'] == 1
    endpoints = module['endpoints']
    occupied = endpoints | module['selected']
    profiles = Counter()
    exterior_witnesses = 0
    continuations = 0
    for point in endpoints:
        cells = vertices_of({tuple(value//2 for value in point)})
        assert (set(neighbors(point))-cells) & endpoints
        exterior_witnesses += 1
        for blank in (set(neighbors(point)) & cells)-occupied:
            other = next(iter((set(neighbors(point)) & cells)-{blank}))
            continuation = tuple(2*value-neighbor for value, neighbor in zip(point, other))
            assert other in endpoints and continuation in endpoints and continuation not in cells
            continuations += 1
    for tile in module['receiver']:
        cells = vertices_of({tile})
        current = cells & endpoints
        selected = cells & module['selected']
        profiles['%dP_%dT' % (len(current), len(selected))] += 1
        if len(current) == 1:
            assert selected == set(neighbors(next(iter(current)))) & cells
        elif len(current) == 2:
            first, second = sorted(current)
            assert second in neighbors(first) and len(selected) == 1
        else:
            assert len(current) == 4 and not selected
    return dict(profiles=dict(profiles), exterior_witnesses=exterior_witnesses,
                blank_corner_continuations=continuations)


def inspect(current, modules):
    for module in modules:
        check_profile(module)
    result = inspect_dual(current, modules)
    assert result['marked_sides'] == 0
    assert result['two_guard_unit_donors'] == 2*len(modules)
    assert result['intratile_degree_four_defect'] <= 2*result['new_aligned_faces']
    assert result['two_guard_credit'] >= len(modules)
    network = combine(modules)
    event_tiles = Counter()
    group_events = Counter()
    for index, module in enumerate(modules):
        original_occupied = module['endpoints'] | module['selected']
        for point in module['endpoints']:
            tile = tuple(value//2 for value in point)
            for other in (set(neighbors(point)) & network['endpoints'])-original_occupied:
                if tuple(value//2 for value in other) != tile:
                    continue
                cells = vertices_of({tile})
                assert cells <= network['endpoints']
                assert len(cells & module['endpoints']) == 2
                group_events[index, tile] += 1
                event_tiles[tile] += 1
    assert all(amount == 1 for amount in group_events.values())
    assert all(amount <= 2 for amount in event_tiles.values())
    assert sum(event_tiles.values()) == result['intratile_degree_four_defect']
    return result


def nonhereditary_control():
    current, modules = four_way(8)
    full = inspect(current, modules)
    invalid_pairs = []
    for first, second in itertools.combinations(range(4), 2):
        network = combine([modules[first], modules[second]])
        occupied = network['endpoints'] | network['selected']
        bad = sorted(point for point in network['selected']
                     if sum(other in occupied for other in neighbors(point)) > 1)
        assert bad
        invalid_pairs.append(dict(modules=[first, second], invalid_retained_selections=bad))
    return dict(status='PASS', full_four_module_ledger=full, infeasible_pairs=invalid_pairs,
                scope='Every two-module subcollection is infeasible; the final four-module union is feasible and fully frozen.')


def inspect_mixed(current, modules):
    result = inspect_dual(current, modules)
    network = combine(modules)
    positive_events = Counter()
    for module in modules:
        if module['charge'] <= 0:
            continue
        check_profile(module)
        original_occupied = module['endpoints'] | module['selected']
        for point in module['endpoints']:
            tile = tuple(value//2 for value in point)
            for other in (set(neighbors(point)) & network['endpoints'])-original_occupied:
                if tuple(value//2 for value in other) != tile:
                    continue
                cells = vertices_of({tile})
                assert cells <= network['endpoints']
                assert len(cells & module['endpoints']) == 2
                positive_events[tile] += 1
    assert all(amount <= 2 for amount in positive_events.values())
    positive = sum(positive_events.values())
    nonpositive = result['intratile_degree_four_defect']-positive
    assert nonpositive >= 0
    credit = 2*result['new_aligned_faces']-positive
    assert credit >= 0
    assert result['two_guard_credit'] == (result['positive_modules']+
        result['negative_module_mass']+credit-nonpositive-result['marked_sides'])
    return dict(**result, positive_source_intratile_events=positive,
                nonpositive_source_intratile_events=nonpositive, unspent_square_credit=credit)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    originals = [(spec, module) for spec, module in supported_modules() if spec['kind'] == 'two_leg']
    for width, left, right in [(40, 40, 4), (40, 4, 40), (64, 40, 40)]:
        current, _ = two_leg_case(width, left, right)
        module = labeled_module(current[2], current[3], (), ((3, 2), (3, 1), (2, 3), (1, 3)))
        originals.append((dict(kind='two_leg', width=width, left=left, right=right), module))
    module_records = []
    for spec, module in originals:
        for symmetry in itertools.product((False, True), repeat=3):
            for phase in itertools.product((0, 1), repeat=2):
                moved = transform_module(module, symmetry, phase)
                if moved['charge'] != 1:
                    continue
                module_records.append(dict(parameters=spec, symmetry=symmetry, phase=phase,
                                           **check_profile(moved)))
    fusions = []
    for width in (8, 10, 12, 14, 20, 40):
        current, modules = four_way(width)
        fusions.append(dict(kind='four_way', width=width, **inspect(current, modules)))
        for symmetry, phase, offset, current_image, moved in phase_images(modules):
            if all(module['charge'] == 1 for module in moved):
                fusions.append(dict(kind='four_way_image', width=width, symmetry=symmetry,
                                    phase=phase, **inspect(current_image, moved)))
    for amount in (2, 3, 5):
        _, base_modules = four_way(8)
        modules = [transform_module(module, (False, False, False), (0, 20*index))
                   for index in range(amount) for module in base_modules]
        network = combine(modules)
        current = (18, 20*amount, network['selected'], network['matching'])
        result = inspect(current, modules)
        assert result['new_aligned_faces'] == amount
        fusions.append(dict(kind='disjoint_four_way_cycles', amount=amount, **result))
    mixed = []
    for width in (6, 8, 14, 40):
        current, modules = occupied_bands(width)
        result = inspect_mixed(current, modules)
        assert result['positive_source_intratile_events'] == 2
        assert result['nonpositive_source_intratile_events'] == 2
        assert result['unspent_square_credit'] == 2
        mixed.append(dict(kind='occupied_bands', width=width, **result))
    for width, height in itertools.product((6, 8, 14), (4, 8, 20)):
        current, modules = opposed_bands(width, height)
        mixed.append(dict(kind='opposed_bands', width=width, height=height,
                          **inspect_mixed(current, modules)))
        for symmetry, phase, offset, current_image, moved in phase_images(modules):
            mixed.append(dict(kind='opposed_bands_image', width=width, height=height,
                              symmetry=symmetry, phase=phase, **inspect_mixed(current_image, moved)))
    for amount in (1, 2, 3, 4, 8):
        current, modules = chain(amount)
        mixed.append(dict(kind='star_chain', amount=amount, **inspect_mixed(current, modules)))
    result = dict(status='PASS', positive_module_profiles=module_records, physical_fusions=fusions,
                  mixed_phase_fusions=mixed,
                  nonhereditary_control=nonhereditary_control(),
                  summary=dict(positive_module_profile_images=len(module_records),
                               physical_fusions=len(fusions),
                               mixed_phase_fusions=len(mixed),
                               mixed_cases_with_positive_intratile_events=sum(
                                   record['positive_source_intratile_events'] > 0 for record in mixed),
                               actual_degree_four_fusions=sum(record['degree_four_endpoints'] > 0
                                                             for record in fusions)),
                  scope='Coordinate controls only. All-parameter classification and arbitrary positive-module fusion have separate written proofs; no actual all-positive degree-four example claimed.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
