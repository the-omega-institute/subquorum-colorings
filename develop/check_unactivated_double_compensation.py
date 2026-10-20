"""Two-slot allocation controls from complete sources and exact role masks."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import inspect_slots, tile_of
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_multiple_positive_saturation import inspect_sources
from check_occupied_gate_activation import gate_roles, positive_dimensions
from check_regular_tile_compensation import profile_counts
from check_saturated_gate_geometry import classify, tip_forbidden
from check_short_leg_defect_injection import defect_tiles, inverse_affine
from degree_four_overcount import opposed_modules
from dual_guard_compensation import paired_guards
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def both_forced_tiles(module, modules, endpoints):
    width, left, right, symmetry, offset = positive_dimensions(module)
    owners = {point: index for index, member in enumerate(modules)
              for point in member['endpoints']}
    result = []
    gate_owners = []
    for reflected, height in ((False, left), (True, right)):
        def original(point):
            row, column = point
            return inverse_affine((row, width+1-column if reflected else column),
                                  symmetry, offset)

        gate = original((2, 2))
        incoming_index = owners[gate]
        gate_owners.append(incoming_index)
        incoming = modules[incoming_index]
        cells = {original(point) for point in itertools.product((6, 7), (2, 3))}
        assert height == 6
        assert cells & incoming['endpoints'] == {original((6, 2)), original((6, 3))}
        assert not cells & incoming['selected']
        assert original((7, 2)) not in endpoints
        tiles = {tile_of(point) for point in cells}
        assert len(tiles) == 1
        result.append(next(iter(tiles)))
    assert width in (8, 10) and left == right == 6
    assert gate_owners[0] == gate_owners[1]
    assert len(set(result)) == 2
    return result


def inspect_compensation(current, modules):
    report = inspect_sources(current, modules)
    slots = inspect_slots(current, modules)
    endpoints = combine(modules)['endpoints']
    marked = {tuple(item['tile']): item for item in slots['marked_assignments']}
    blank = {tile for tile, item in marked.items() if item['kind'] == 'blank_gate'}
    defects = defect_tiles(modules, endpoints)
    assert all(defects[tile] == 'L2bar' for tile in blank)
    actual_pool = {(tile, slot) for tile, kind in defects.items()
                   for slot in range(2 if kind in ('L2bar', 'L2mutual') else 1)}
    assert len(actual_pool) == report['boundary_cost']
    assigned = [(tile, slot) for tile in sorted(blank) for slot in range(2)]
    census = Counter()
    occupied_sources = []
    for index, module in enumerate(modules):
        if module['charge'] != 1:
            continue
        side_marks = [marked[tile_of(guard[0])] for guard in paired_guards(module)
                      if tile_of(guard[0]) in marked]
        if len(side_marks) != 2:
            continue
        width, left, right, _, _ = positive_dimensions(module)
        if width != 6 and (width >= 12 or max(left, right) >= 8):
            census['exceptional_double'] += 1
            continue
        activations = sum(len(cells & module['endpoints']) == 1 and
                          len(cells & module['selected']) == 2 and
                          bool(cells & module['selected'] & endpoints)
                          for cells in map(lambda tile: vertices_of({tile}), module['receiver']))
        census[activations] += 1
        if activations or any(item['kind'] == 'blank_gate' for item in side_marks):
            continue
        forced = both_forced_tiles(module, modules, endpoints)
        for tile in forced:
            assert tile not in blank and defects[tile] in ('L2bar', 'L3')
            assigned.append((tile, 0))
        occupied_sources.append(dict(source=index, forced_tiles=forced))
    assert len(set(assigned)) == len(assigned)
    assert set(assigned) <= actual_pool
    assert len(assigned) == 2*len(blank)+2*len(occupied_sources)
    zero, single, twice = (census[index] for index in range(3))
    assert zero <= len(blank)+len(occupied_sources)
    assert report['boundary_cost'] >= 2*zero
    assert report['activated_positive'] >= single+2*twice
    assert report['double_marked_sources'] == zero+single+twice+census['exceptional_double']
    lower = report['unmarked_sources']-census['exceptional_double']-single//2
    assert report['exact_joint_margin'] >= lower
    if census['exceptional_double'] == 0 and single <= 1:
        assert report['exact_joint_margin'] >= 0
    return dict(zero_activation_double=zero, single_activation_double=single,
                twice_activation_double=twice, exceptional_double=census['exceptional_double'],
                blank_marks=len(blank), occupied_zero_double=len(occupied_sources),
                boundary=report['boundary_cost'], assigned_slots=len(assigned),
                actual_reserve=report['event_reserve'], margin=report['exact_joint_margin'],
                new_margin_bound=lower, occupied_sources=occupied_sources)


def role_controls():
    _, candidates = gate_roles()
    source_roles = Counter()
    positive_pairs = []
    same_owner = 0
    distinct_owner_comparisons = 0
    for width, left, right in itertools.product((8, 10), (4, 6), (4, 6)):
        positive = source(width, left, right)
        left_roles = []
        right_roles = []
        for candidate in candidates:
            module = candidate['module']
            if not module['endpoints'] & positive['endpoints'] and not tip_forbidden(module, left):
                assert classify(candidate) in ('horizontal_tip', 'vertical_tip')
                source_roles[classify(candidate)] += 1
                if (right+1, width-1) not in module['endpoints'] | module['selected']:
                    left_roles.append(candidate)
            moved = transform_module(module, (False, False, True), (0, width+1))
            if moved['endpoints'] & positive['endpoints']:
                continue
            if ((left+1, 2) in moved['endpoints'] | moved['selected'] or
                    (right+1, width-1) in moved['endpoints'] | moved['selected']):
                continue
            right_roles.append(moved)
        for first, second in itertools.product(left_roles, right_roles):
            incoming = first['module']
            if incoming['endpoints'] == second['endpoints']:
                expected = transform_module(source(width-2, 4, 4),
                                            (False, True, False), (6, 1))
                assert left == right == 6
                assert incoming['endpoints'] == expected['endpoints']
                assert incoming['selected'] == expected['selected']
                same_owner += 1
            else:
                distinct_owner_comparisons += 1
                assert incoming['endpoints'] & second['endpoints']
        positive_pairs.append(dict(width=width, left=left, right=right,
                                   left_roles=len(left_roles), right_roles=len(right_roles)))
    assert same_owner > 0 and distinct_owner_comparisons > 0
    blank_profiles = Counter()
    positive = source(14, 8, 8)
    cells = vertices_of({(1, 1)})
    for width, left, right in itertools.product((6, 8, 10, 14), (4, 6, 10), (4, 8, 12)):
        incoming = source(width, left, right)
        for point in ((0, 1), (0, width), (left, 1), (right, width)):
            for symmetry, target in itertools.product(itertools.product((False, True), repeat=3),
                                                       ((3, 2), (2, 3))):
                transformed = affine(point, symmetry)
                offset = tuple(value-original for value, original in zip(target, transformed))
                moved = transform_module(incoming, symmetry, offset)
                if moved['charge'] >= -4 or not profile_counts(moved)[3, 0]:
                    continue
                if moved['endpoints'] & positive['endpoints']:
                    continue
                if (2, 2) in moved['endpoints'] | moved['selected']:
                    continue
                pair = cells & moved['endpoints']
                supports = cells & moved['selected']
                assert pair == {target, (3, 3)}
                assert not {(3, 2), (2, 3)} <= moved['endpoints']
                assert len(supports) in (0, 1)
                if supports:
                    assert supports == {(3, 2), (2, 3)}-{target}
                blank_profiles[len(supports)] += 1
    assert blank_profiles[0] and blank_profiles[1]
    return dict(gate_roles=dict(source_roles), two_gate_controls=positive_pairs,
                shared_owner_controls=same_owner,
                distinct_owner_pair_collisions=distinct_owner_comparisons,
                blank_pair_role_controls=dict(blank_profiles),
                scope='Finite exact source-role masks, not complete physical fusions. The original2P1T blank roles are locally possible but cannot be completed: consuming their support forces a second exact pair owner of y. Universal exclusion and crossbar proofs are written.')


def arithmetic_controls():
    censuses = 0
    first_failures = set()
    for zero, single, twice, exceptional, unmarked in itertools.product(range(6), repeat=5):
        double_count = zero+single+twice+exceptional
        for reserve in range(12):
            if 2*reserve < 2*zero+single+2*twice:
                continue
            margin = unmarked+reserve-double_count
            assert margin >= unmarked-exceptional-single//2
            if exceptional+single//2 <= unmarked:
                assert margin >= 0
            if exceptional == 0 and reserve == 1 and margin < 0:
                first_failures.add((zero, single, twice, unmarked))
            censuses += 1
    assert first_failures == {(0, 2, 0, 0)}
    return dict(census_controls=censuses, remaining_first_failure=list(next(iter(first_failures))),
                scope='Conditional integer controls; the remaining census is not a physical realization.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    roles = role_controls()
    arithmetic = arithmetic_controls()
    physical = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_compensation(current, moved)))
    for amount in (2, 4, 8):
        modules = [transform_module(module, (False, False, False), (0, 20*index))
                   for index in range(amount) for module in opposed_modules(6+2*(index % 2), 4)]
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose else
                      (int(flip_row), int(flip_column)))
            current, moved = contained([transform_module(module, symmetry, offset)
                                        for module in modules])
            report = inspect_compensation(current, moved)
            assert report['zero_activation_double'] == report['occupied_zero_double'] == amount
            assert report['assigned_slots'] == 2*amount
            physical.append(dict(fixture='separated_two_slot_%d' % amount,
                                 symmetry=symmetry, **report))
    summary = dict(physical_images=len(physical),
                   zero_activation_double_occurrences=sum(record['zero_activation_double']
                                                          for record in physical),
                   assigned_slots=sum(record['assigned_slots'] for record in physical),
                   blank_mark_images=sum(record['blank_marks'] > 0 for record in physical),
                   single_activation_double_images=sum(record['single_activation_double'] > 0
                                                        for record in physical),
                   multiple_zero_double_images=sum(record['zero_activation_double'] > 1
                                                    for record in physical))
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary, roles=roles,
        arithmetic=arithmetic, physical=physical,
        scope='Finite physical labelled-slot checks, conditional arithmetic and source-role controls. Universal complete-source blank-pair rigidity, occupied-gate classification, cross-type non-reuse and shared compensation are written; the remaining connected AA candidate is not realized or excluded here.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
