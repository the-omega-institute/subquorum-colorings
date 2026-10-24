"""Actual single-use reserve and long-leg controls for the 37/39 proof."""

from collections import Counter
import itertools
import json

from all_phase_joint_slots import inspect_slots, tile_of
from check_activated_singleton_budget import phase_images
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_exact_event_reserve import fixtures
from check_fullbar_unactivated_obstruction import witness_modules
from check_localized_exterior_tile_budget import complete_certificate
from check_low_cost_exceptional_doubles import compensated
from check_minus_one_tip_obstructions import source
from check_multiple_positive_saturation import inspect_sources
from check_occupied_gate_activation import positive_dimensions
from check_short_leg_defect_injection import defect_tiles, inverse_affine, local_controls
from check_unactivated_double_compensation import both_forced_tiles
from check_width_six_actual_mark_excess import actual_marks, records_of
from degree_four_overcount import opposed_modules
from dual_guard_compensation import paired_guards
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def middle_dimensions(width, left, right):
    return width == 8 and (left, right) in {(6, 8), (8, 6), (4, 10), (10, 4)}


def terminal_occurrences(module, endpoints):
    return {(tile[0], tile[1]) for tile in module['receiver']
            if len(vertices_of({tile}) & module['endpoints']) == 1
            and len(vertices_of({tile}) & module['selected']) == 2
            and bool(vertices_of({tile}) & module['selected'] & endpoints)}


def inspect_compensation(current, modules):
    records = records_of(modules)
    _, potential, _, _ = complete_certificate(records)
    report = inspect_sources(current, modules)
    endpoints = set.union(*(module['endpoints'] for module in modules))
    owners = {point: index for index, module in enumerate(modules)
              for point in module['endpoints']}
    assert len(owners) == sum(len(module['endpoints']) for module in modules)
    marks = actual_marks(records)
    assignments = {tuple(item['tile']): item
                   for item in inspect_slots(current, modules)['marked_assignments']}
    defects = defect_tiles(modules, endpoints)
    actual_h = {(tile, slot) for tile, kind in defects.items()
                for slot in range(2 if kind in ('L2bar', 'L2mutual') else 1)}
    actual_a = {(index, tile) for index in marks
                for tile in terminal_occurrences(modules[index], endpoints)}
    assert len(actual_h) == report['boundary_cost']
    assert len(actual_a) == report['activated_positive']
    reserved_h = []
    reserved_a = []
    assigned_legs = []
    census = Counter()
    for index, marked in marks.items():
        if marked != 2:
            continue
        producer = modules[index]
        width, left, right, symmetry, offset = positive_dimensions(producer)
        activation = sorted(terminal_occurrences(producer, endpoints))
        old = compensated(width, left, right)
        middle = middle_dimensions(width, left, right)
        if not old and not middle:
            census['remaining'] += 1
            continue
        if old:
            census['old_%d' % len(activation)] += 1
        else:
            census['middle'] += 1
        if activation:
            chosen = activation if old else activation[:1]
            reserved_a.extend((index, tile) for tile in chosen)
            continue
        blank = [tile_of(guard[0]) for guard in paired_guards(producer)
                 if assignments[tile_of(guard[0])]['kind'] == 'blank_gate']
        if blank:
            tile = min(blank)
            assert defects[tile] == 'L2bar'
            reserved_h.extend((tile, slot) for slot in range(2 if old else 1))
            continue
        if old:
            reserved_h.extend((tile, 0) for tile in both_forced_tiles(producer, modules, endpoints))
            continue
        reflected = left > right

        def original(point):
            row, column = point
            return inverse_affine((row, width+1-column if reflected else column), symmetry, offset)

        if {left, right} == {6, 8}:
            cells = {original(point) for point in itertools.product((6, 7), (2, 3))}
            incoming = modules[owners[original((2, 2))]]
            assert cells & incoming['endpoints'] == {original((6, 2)), original((6, 3))}
            assert not cells & incoming['selected']
            assert not cells & (producer['endpoints'] | producer['selected'])
            assert original((7, 2)) not in endpoints | current[2]
            tile = tile_of(original((6, 2)))
            assert cells == vertices_of({tile}) and defects[tile] in ('L2bar', 'L3')
            reserved_h.append((tile, 0))
            census['middle_y_forced'] += 1
        else:
            assert {left, right} == {4, 10}
            gate = original((2, 7))
            owner = owners[gate]
            incoming = modules[owner]
            assert incoming['charge'] < 0 and len(incoming['endpoints']) != 8
            donor_tile = tile_of(gate)
            assert donor_tile in assignments
            breadth, near, far, incoming_symmetry, incoming_offset = positive_dimensions(incoming)
            normalized_gate = affine(gate, incoming_symmetry, incoming_offset)
            terminals = {(near, 1): (0, near), (far, breadth): (1, far)}
            leg, height = terminals[normalized_gate]
            assert height == 8
            assigned_legs.append((owner, leg))
            cells = {original(point) for point in itertools.product((10, 11), (6, 7))}
            assert cells & incoming['endpoints'] == {original((10, 7)), original((10, 6))}
            assert not cells & incoming['selected']
            assert not cells & (producer['endpoints'] | producer['selected'])
            assert original((11, 7)) not in endpoints | current[2]
            tile = tile_of(original((10, 7)))
            assert cells == vertices_of({tile}) and defects[tile] in ('L2bar', 'L3')
            reserved_h.append((tile, 0))
            census['special'] += 1
    assert len(set(reserved_a)) == len(reserved_a) and set(reserved_a) <= actual_a
    assert len(set(reserved_h)) == len(reserved_h) and set(reserved_h) <= actual_h
    assert len(set(assigned_legs)) == len(assigned_legs)
    zero, single, twice = (census['old_%d' % amount] for amount in range(3))
    middle, remaining, credit = (census[name] for name in ('middle', 'remaining', 'special'))
    assert len(reserved_a)+len(reserved_h) == 2*zero+single+2*twice+middle
    assert 2*report['event_reserve'] >= 2*zero+single+2*twice+middle
    positive_matching = sum(len(modules[index]['matching']) for index in marks)
    negative_matching = negative_sources = 0
    for index, module in enumerate(modules):
        if module['charge'] >= 0 or len(module['endpoints']) == 8:
            continue
        negative_sources += 1
        chosen = sum(owner == index for owner, _ in assigned_legs)
        assert len(module['matching']) >= 9+2*chosen
        negative_matching += len(module['matching'])
    total_matching = sum(len(module['matching']) for module in modules)
    marked = sum(marks.values())
    assert marked == report['marked'] and marked <= 4*negative_sources
    assert positive_matching >= 9*len(marks)+5*middle+6*remaining
    assert 4*negative_matching >= 9*marked+8*credit
    assert 4*total_matching >= 36*len(marks)+20*middle+24*remaining+9*marked+8*credit
    margin = potential-marked
    assert margin == report['exact_joint_margin']
    assert margin >= report['unmarked_sources']-remaining-(single+middle)//2
    if remaining == 0:
        assert 27*margin+total_matching >= 0
    assert 39*margin+2*total_matching >= 0
    assert 78*len(current[2])+74*len(current[3]) <= 39*current[0]*current[1]
    return dict(census=census, assigned_h=len(reserved_h), assigned_a=len(reserved_a),
                assigned_long_legs=len(assigned_legs), actual_middle_doubles=middle,
                actual_special_doubles=credit, marked=marked)


def original_long_leg_controls():
    checked = terminal_slots = same_owner_two_legs = 0
    for width, left, right in itertools.product((6, 8, 14, 40), (4, 8, 12), (4, 8, 20)):
        base = source(width, left, right)
        matching = len(base['matching'])
        long_sides = [side for side, height in enumerate((left, right)) if height >= 8]
        for symmetry in itertools.product((False, True), repeat=3):
            for size in range(len(long_sides)+1):
                for chosen in itertools.combinations(long_sides, size):
                    tips = [affine(((left, 1), (right, width))[side], symmetry, (2, 4))
                            for side in chosen]
                    assert len(set(tips)) == len(chosen)
                    assert matching >= 9+2*len(chosen)
                    moved = transform_module(base, symmetry, (2, 4))
                    breadth, near, far, frame, offset = positive_dimensions(moved)
                    normalized_tips = {affine(point, frame, offset) for point in tips}
                    normalized_legs = {(near, 1): near, (far, breadth): far}
                    assert all(normalized_legs[point] >= 8 for point in normalized_tips)
                    terminal_slots += len(chosen)
                    same_owner_two_legs += len(chosen) == 2
                    checked += 1
    y = source(8, 6, 8)
    incoming = transform_module(source(6, 4, 4), (False, True, False), (6, 1))
    cells = vertices_of({(3, 1)})
    assert cells & incoming['endpoints'] == {(6, 2), (6, 3)}
    assert not cells & (incoming['selected'] | y['endpoints'] | y['selected'])
    assert len(set(neighbors((6, 2))) & incoming['endpoints']) == 2
    assert len(set(neighbors((6, 3))) & incoming['endpoints']) == 3
    exclusions = local_controls()['donor_orientations']
    assert len(exclusions) == 8
    return dict(original_matching_controls=checked, distinct_terminal_slots=terminal_slots,
                same_original_two_long_leg_controls=same_owner_two_legs,
                inherited_blank_donor_orientation_exclusions=len(exclusions),
                y_original_pair_hypotheses=True,
                scope='Original local masks and source matching sizes; not new complete Y/X realizations.')


def tight_clearance_controls():
    checked = 0
    for height, breadth, far, width in itertools.product(range(6, 50, 2),
                                                       (6, 8, 14, 40), (4, 6, 12, 40),
                                                       (6, 8, 10, 14)):
        incoming = transform_module(source(breadth, height-2, far),
                                    (False, True, False), (height, 1))
        producer = source(width, height, 4)
        cells = vertices_of({(height//2, 1)})
        assert cells & incoming['endpoints'] == {(height, 2), (height, 3)}
        assert not cells & incoming['selected']
        assert not cells & (producer['endpoints'] | producer['selected'])
        assert len(set(neighbors((height, 2))) & incoming['endpoints']) == 2
        assert len(set(neighbors((height, 3))) & incoming['endpoints']) == 3
        checked += 1
    return dict(exact_local_tight_clearance_masks=checked,
                scope='Original local pair masks for arbitrary-height proof; these are not asserted to be complete endpoint-disjoint source fusions.')


def main():
    inventories = list(fixtures())+[('complete_fullbar_exit', witness_modules()),
                                  ('isolated_y', [source(8, 6, 8)]),
                                  ('isolated_x', [source(8, 4, 10)])]
    for amount in (2, 4, 8):
        modules = [transform_module(module, (False, False, False), (0, 30*index))
                   for index in range(amount) for module in opposed_modules(6+2*(index % 2), 4)]
        inventories.append(('multiple_old_forced_%d' % amount, modules))
    totals = Counter()
    for _, modules in inventories:
        for _, _, _, current, moved in phase_images(modules):
            record = inspect_compensation(current, moved)
            totals['complete_physical_images'] += 1
            totals['marked_images'] += bool(record['marked'])
            for key in ('assigned_h', 'assigned_a', 'assigned_long_legs',
                        'actual_middle_doubles', 'actual_special_doubles'):
                totals[key] += record[key]
            totals['images_multiple_allocations'] += record['assigned_h']+record['assigned_a'] > 2
    print(json.dumps(dict(status='PASS', physical=dict(totals),
                          local=original_long_leg_controls(),
                          tight_clearance=tight_clearance_controls(),
                          scope='Physical resource slots and original legs are allocated before aggregate checks. Zero new-branch complete occurrences, if reported, are explicit coverage limitations; all-parameter geometry and injections are written proofs.'), indent=2))


if __name__ == '__main__':
    main()
