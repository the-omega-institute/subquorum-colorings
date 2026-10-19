"""Physical controls for regular profiles, rotor barriers and irregular tax."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from degree_four_overcount import opposed_bands
from degree_three_fusion import occupied_bands
from discover_fusion_compensation_obstructions import supported_modules
from dual_guard_compensation import inspect as inspect_dual
from rotor_networks import combine, rotor, star_modules, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def profile_counts(module):
    result = Counter()
    for tile in module['receiver']:
        cells = vertices_of({tile})
        endpoints = cells & module['endpoints']
        selected = cells & module['selected']
        kind = len(endpoints), len(selected)
        result[kind] += 1
        assert kind in {(1, 2), (2, 1), (3, 0), (4, 0), (1, 1), (2, 0)}
        if len(endpoints) == 1:
            assert selected <= set(neighbors(next(iter(endpoints))))
        if len(endpoints) == 2:
            first, second = sorted(endpoints)
            assert second in neighbors(first)
    return result


def irregular_capacity(module):
    profiles = profile_counts(module)
    return profiles[1, 1]+2*profiles[2, 0]


def barrier_controls():
    core = {(row, column) for row in (0, 1) for column in range(1, 7)} | {
        (row, 1) for row in range(2, 5)}
    records = []
    for mirror in (False, True):
        base = transform_module(rotor(), (False, False, mirror))
        for source in sorted(base['endpoints']):
            witnesses = []
            for target in [(2, 2), (3, 2), (2, 3)]:
                offset = tuple(value-original for value, original in zip(target, source))
                moved = transform_module(base, (False, False, False), offset)
                overlap = sorted(core & moved['endpoints'])
                gate_occupied = (2, 2) in moved['endpoints'] | moved['selected']
                assert overlap or target != (2, 2) and gate_occupied
                witnesses.append(dict(target=target, blocker=overlap[0] if overlap else None,
                                      gate_occupied=gate_occupied))
            records.append(dict(mirror=mirror, source=source, witnesses=witnesses))
    base = rotor()
    quarter = lambda point: (point[1], 5-point[0])
    assert {quarter(point) for point in base['endpoints']} == base['endpoints']
    assert {quarter(point) for point in base['selected']} == base['selected']
    return dict(status='PASS', endpoint_core=sorted(core), complete_role_cases=records,
                scope='Two translation classes from quarter-turn invariance, eight endpoint roles per class, three target corners. Every target placement has its exact determined offset; not a bounded translation search.')


def inspect(current, modules, require_frozen=True, rotor_only_negative=False):
    result = inspect_dual(current, modules, require_frozen=require_frozen)
    network = combine(modules)
    regular_events = Counter()
    irregular = 0
    potential = 0
    for module in modules:
        potential += irregular_capacity(module)
        old_occupied = module['endpoints'] | module['selected']
        local_regular = Counter()
        for point in module['endpoints']:
            tile = tuple(value//2 for value in point)
            cells = vertices_of({tile})
            kind = len(cells & module['endpoints']), len(cells & module['selected'])
            for other in (set(neighbors(point)) & network['endpoints'])-old_occupied:
                if tuple(value//2 for value in other) != tile:
                    continue
                if kind in {(1, 1), (2, 0)}:
                    irregular += 1
                else:
                    assert cells <= network['endpoints']
                    assert kind in {(2, 1), (3, 0)}
                    regular_events[tile] += 1
                    local_regular[tile] += 1
        for tile, amount in local_regular.items():
            assert amount <= (2 if len(vertices_of({tile}) & module['endpoints']) == 3 else 1)
    assert all(amount <= 2 for amount in regular_events.values())
    regular = sum(regular_events.values())
    assert regular+irregular == result['intratile_degree_four_defect']
    diagonal = sum(module['charge'] <= -5 and profile_counts(module)[3, 0] == 2 for module in modules)
    assert potential == 2*result['negative_module_mass']-2*diagonal
    assert irregular <= potential
    credit = 2*result['new_aligned_faces']-regular
    assert credit >= 0
    assert result['two_guard_credit'] == (result['positive_modules']+
        result['negative_module_mass']+credit-irregular-result['marked_sides'])
    if rotor_only_negative:
        assert result['marked_sides'] == 0
        assert result['two_guard_unit_donors'] == 2*result['positive_modules']
    return dict(**result, regular_source_events=regular, irregular_source_events=irregular,
                irregular_potential=potential, diagonal_negative_modules=diagonal,
                residual_square_credit=credit,
                coarse_irregular_credit=result['positive_modules']+
                    result['negative_module_mass']+credit-potential-result['marked_sides'])


def phase_catalogue():
    records = []
    for spec, base in supported_modules():
        for phase in itertools.product(range(2), repeat=2):
            moved = transform_module(base, (False, False, False), phase)
            counts = profile_counts(moved)
            if spec['kind'] == 'two_leg':
                width = spec['width']
                half_sum = (spec['left']+spec['right'])//2
                expected = {
                    (0, 0): {(4, 0): (width-2)//2, (2, 1): half_sum, (1, 2): 2},
                    (0, 1): {(4, 0): width//2, (2, 1): half_sum-2, (1, 1): 2},
                    (1, 0): {(2, 0): width-2, (2, 1): half_sum, (1, 1): 2},
                    (1, 1): {(2, 0): width-2, (2, 1): half_sum-2, (3, 0): 2},
                }[phase]
                diagonal = int(phase == (1, 1))
            else:
                expected = {(0, 0): {(4, 0): 1, (1, 1): 4},
                            (0, 1): {(1, 2): 2, (3, 0): 2},
                            (1, 0): {(1, 2): 2, (3, 0): 2},
                            (1, 1): {(2, 1): 4}}[phase]
                diagonal = 0
            assert counts == Counter(expected)
            negative_mass = int(moved['charge'] > 0)-moved['charge']
            assert irregular_capacity(moved) == 2*negative_mass-2*diagonal
            records.append(dict(parameters=spec, phase=phase, original_charge=moved['charge'],
                                profiles={str(key): value for key, value in counts.items()},
                                irregular_capacity=irregular_capacity(moved), diagonal=diagonal))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    for width in (6, 8, 14, 40):
        current, modules = occupied_bands(width)
        records.append(dict(kind='occupied_bands', width=width, **inspect(current, modules)))
    for width, height in itertools.product((6, 8, 14), (4, 8, 20)):
        current, modules = opposed_bands(width, height)
        for symmetry, phase, offset, current_image, moved in phase_images(modules):
            records.append(dict(kind='opposed_bands_image', width=width, height=height,
                                symmetry=symmetry, phase=phase, **inspect(current_image, moved)))
    for width in (6, 8, 14, 40):
        modules = [transform_module(module, (False, False, False), (width+2, width+2))
                   for module in star_modules(width)]
        network = combine(modules)
        rows = 2*(max(point[0] for point in network['endpoints'] | network['selected'])//2+1)
        columns = 2*(max(point[1] for point in network['endpoints'] | network['selected'])//2+1)
        records.append(dict(kind='rotor_star', width=width,
                            **inspect((rows, columns, network['selected'], network['matching']),
                                      modules, rotor_only_negative=True)))
    chains = []
    for amount in (1, 2, 3, 4, 8, 16, 32):
        modules = [transform_module(rotor(), (False, False, False), (2*index, 2*index+1))
                   for index in range(amount)]
        network = combine(modules)
        current = (2*amount+4, 2*amount+6, network['selected'], network['matching'])
        record = inspect(current, modules, require_frozen=False, rotor_only_negative=True)
        assert record['new_aligned_faces'] == 2*(amount-1)
        assert record['regular_source_events'] == 4*(amount-1)
        assert record['irregular_source_events'] == 0
        assert record['actual_charge'] == 0
        chains.append(dict(amount=amount, **record))
    catalogue = phase_catalogue()
    result = dict(status='PASS', phase_catalogue=catalogue, barrier=barrier_controls(),
                  physical_fusions=records, zero_rotor_chains=chains,
                  summary=dict(phase_catalogue_cases=len(catalogue), barrier_roles=16, barrier_target_cases=48,
                               mixed_fusions=len(records), zero_rotor_chains=len(chains),
                               controls_with_actual_regular_events=sum(
                                   record['regular_source_events'] > 0 for record in records+chains)),
                  scope='General profile/barrier/tax results have written proofs. Complete fixed rotor orbit controls and finite physical checks; no claim that the degree-four rotor chains are fully frozen.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result['summary']))


if __name__ == '__main__':
    main()
