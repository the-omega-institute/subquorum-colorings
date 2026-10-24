"""Independent physical reconstruction of two minus-one tip obstructions."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import apply_bundle, neighbors
from check_minus_one_joint_compensation import contained, inspect
from check_promotion_cores import color_data, frozen_certificate, peel
from check_residual_corridors import direct_check
from check_two_leg_corner_obstruction import two_leg_case
from rotor_networks import combine, labeled_module, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def source(width, left, right):
    current, _ = two_leg_case(width, left, right)
    return labeled_module(current[2], current[3], (),
                          ((3, 2), (3, 1), (2, 3), (1, 3)))


def build(specifications):
    return [transform_module(rotor() if parameters is None else source(*parameters),
                             symmetry, offset)
            for parameters, symmetry, offset in specifications]


def two_tip_modules():
    return build([
        ((14, 8, 4), (False, False, False), (6, 7)),
        ((6, 4, 4), (False, False, True), (8, 15)),
        ((6, 4, 4), (False, False, True), (8, 21)),
        ((6, 4, 4), (False, True, False), (17, 8)),
        (None, (False, False, False), (10, 19)),
        ((6, 8, 4), (False, True, False), (21, 14)),
        ((6, 8, 4), (False, True, True), (23, 9)),
    ])


def overloaded_tile_modules():
    return build([
        ((14, 8, 4), (False, False, False), (6, 7)),
        ((6, 4, 4), (False, False, True), (8, 21)),
        ((6, 4, 4), (False, True, False), (15, 1)),
        ((6, 4, 4), (False, True, False), (17, 14)),
        ((6, 4, 4), (False, True, True), (15, 27)),
        (None, (False, False, False), (12, 7)),
        ((6, 8, 4), (False, False, True), (2, 8)),
        ((6, 8, 4), (False, False, True), (8, 15)),
        ((6, 8, 4), (False, True, True), (25, 15)),
    ])


def inspect_events(current, modules):
    result = inspect(current, modules)
    network = combine(modules)
    endpoints = network['endpoints']
    regular = Counter()
    irregular = Counter()
    events = []
    for owner, module in enumerate(modules):
        old_occupied = module['endpoints'] | module['selected']
        for point in sorted(module['endpoints']):
            tile = tuple(value//2 for value in point)
            cells = vertices_of({tile})
            profile = len(cells & module['endpoints']), len(cells & module['selected'])
            for other in sorted((set(neighbors(point)) & endpoints)-old_occupied):
                if tuple(value//2 for value in other) != tile:
                    continue
                is_irregular = profile in {(1, 1), (2, 0)}
                (irregular if is_irregular else regular)[tile] += 1
                events.append(dict(owner=owner, tail=point, target=other,
                                   tile=tile, profile=profile, irregular=is_irregular))
    assert sum(regular.values()) == result['regular_events']
    assert sum(irregular.values()) == result['irregular_events'] == 2
    assert all(record['owner'] == 0 for record in events if record['irregular'])
    assert len([point for point in modules[0]['endpoints']
                if len(set(neighbors(point)) & modules[0]['endpoints']) == 1]) == 2
    assert result['negative_rotors'] == result['marked_sides'] == 0
    assert result['regular_events'] == 21 and result['square_credit'] == 5
    full = []
    for tile in sorted(network['receiver']):
        cells = vertices_of({tile})
        if cells <= endpoints and not any(cells <= module['endpoints'] for module in modules):
            full.append(dict(tile=tile, regular=regular[tile], irregular=irregular[tile],
                             unused_regular_credit=2-regular[tile],
                             total_events=regular[tile]+irregular[tile]))
    assert len(full) == 13 and sum(record['unused_regular_credit'] for record in full) == 5
    assert sum(record['irregular'] for record in full) == 2
    frozen, _ = frozen_certificate(current)
    promotion = None
    for color in (0, 1):
        candidates, adjacency, needs = color_data(current, color)
        core, _ = peel(adjacency, needs)
        if core:
            bundle = [(endpoint, candidates[endpoint]) for endpoint in sorted(core)]
            promoted = apply_bundle(current, bundle)
            direct_check(*promoted)
            promotion = dict(color=color, bundle=bundle, size=len(bundle),
                             resulting_selected=len(promoted[2]), resulting_matching=len(promoted[3]))
            break
    assert promotion is not None
    return dict(**result, shape=current[:2], module_charges=[module['charge'] for module in modules],
                endpoints=len(endpoints), matching=len(current[3]), selected=len(current[2]),
                final_receiver_charge=network['charge'], new_full_tiles=13,
                receiver_tiles=len(network['receiver']), receiver_selections=len(network['receiver_selected']),
                endpoint_components=len(endpoint_components(current)),
                frozen_endpoints=len(frozen), fully_frozen=frozen == endpoints,
                actual_feasible_promotion=promotion,
                irregular_event_records=[record for record in events if record['irregular']],
                full_tile_ledger=full,
                overloaded_tiles=[record for record in full if record['total_events'] > 2])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    images = []
    for name, constructor in [('two_tip', two_tip_modules), ('overloaded_tile', overloaded_tile_modules)]:
        current, modules = contained(constructor())
        record = inspect_events(current, modules)
        if name == 'two_tip':
            assert current[:2] == (18, 24)
            assert (record['positive'], record['minus_one'], record['finer_slack'],
                    record['actual_slack']) == (5, 1, 9, 103)
            assert not record['overloaded_tiles']
            assert record['frozen_endpoints'] == 86
            assert record['actual_feasible_promotion']['size'] == 25
        else:
            assert current[:2] == (24, 28)
            assert (record['positive'], record['minus_one'], record['finer_slack'],
                    record['actual_slack']) == (5, 3, 11, 193)
            assert record['overloaded_tiles'] == [dict(tile=(6, 4), regular=2, irregular=1,
                                                      unused_regular_credit=0, total_events=3)]
            assert record['frozen_endpoints'] == 92
            assert record['actual_feasible_promotion']['size'] == 69
        assert not record['fully_frozen']
        records.append(dict(kind=name, **record))
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            phase = ((int(flip_column), int(flip_row)) if transpose else
                     (int(flip_row), int(flip_column)))
            moved = [transform_module(module, symmetry, phase) for module in modules]
            image, moved = contained(moved)
            checked = inspect_events(image, moved)
            for key in ('positive', 'minus_one', 'regular_events', 'irregular_events',
                        'square_credit', 'finer_slack', 'final_receiver_charge'):
                assert checked[key] == record[key]
            assert len(checked['overloaded_tiles']) == len(record['overloaded_tiles'])
            images.append(dict(kind=name, symmetry=symmetry, status='PASS'))
    result = dict(status='PASS', examples=records, symmetry_images=images,
                  scope='Explicit feasible counterexamples to tip-event exclusion and extending per-tile capacity two to irregular tails. Both targets retain positive finer and actual slack; neither refutes compensation. SAT is used only for discovery. No global minimality or full-freezing claim.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', examples=len(records), symmetry_images=len(images),
                          overloaded_tiles=sum(len(record['overloaded_tiles']) for record in records))))


if __name__ == '__main__':
    main()
