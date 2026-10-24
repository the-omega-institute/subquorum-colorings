"""Exact source-role and matching controls for the expanded double class."""

from collections import Counter
import itertools
import json

from all_phase_joint_slots import inspect_slots
from check_activated_singleton_budget import phase_images
from check_component_receivers import vertices_of
from check_exact_event_reserve import fixtures
from check_fullbar_unactivated_obstruction import witness_modules
from check_localized_exterior_tile_budget import complete_certificate
from check_minus_one_tip_obstructions import source
from check_multiple_positive_saturation import inspect_sources
from check_occupied_gate_activation import gate_roles, positive_dimensions
from check_unactivated_double_compensation import both_forced_tiles
from check_short_leg_defect_injection import defect_tiles
from check_width_six_actual_mark_excess import actual_marks, records_of
from dual_guard_compensation import paired_guards
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def compensated(width, left, right):
    return (width == 6 or
            width in (8, 10) and left in (4, 6) and right in (4, 6) or
            width == 8 and {left, right} == {4, 8})


def incoming_role_controls():
    parameters, candidates = gate_roles()
    positive = source(8, 4, 8)
    forbidden = {(5, 2), (9, 7)}
    libraries = []
    for reflected in (False, True):
        library = {}
        for candidate in candidates:
            incoming = (transform_module(candidate['module'], (False, False, True), (0, 9))
                        if reflected else candidate['module'])
            if incoming['endpoints'] & positive['endpoints']:
                continue
            if forbidden & (incoming['endpoints'] | incoming['selected']):
                continue
            library[frozenset(incoming['endpoints'])] = candidate, incoming
        libraries.append(list(library.values()))
    assert all(libraries)
    left_forms = Counter()
    right_forms = Counter()
    collision_images = 0
    for candidate, incoming in libraries[0]:
        assert candidate['phase'] == '11' and candidate['role'] == 'F'
        assert candidate['predecessor'] == (0, 1)
        assert candidate['bar_direction'] == (1, 0) and candidate['height'] == 4
        assert {(row, column) for row in range(2, 8) for column in (5, 6)} <= incoming['endpoints']
        assert max(column for _, column in incoming['endpoints']) == 6
        left_forms['transverse_phase11_height4'] += 1
    for candidate, incoming in libraries[1]:
        assert candidate['phase'] != '10'
        if candidate['phase'] == '01' or candidate['predecessor'] == (0, 1):
            assert (2, 6) in incoming['endpoints']
            collision = (2, 6)
            right_forms['corner_or_transverse'] += 1
        else:
            assert candidate['phase'] == '11' and candidate['predecessor'] == (1, 0)
            height = candidate['height']
            assert height in (4, 6)
            collision = (height+1, 6)
            assert collision in incoming['endpoints']
            right_forms['longitudinal_height%d' % height] += 1
        for _, left in libraries[0]:
            assert left['endpoints'] != incoming['endpoints']
            assert collision in left['endpoints'] & incoming['endpoints']
            for symmetry in itertools.product((False, True), repeat=3):
                moved_left = transform_module(left, symmetry, (2, 4))
                moved_right = transform_module(incoming, symmetry, (2, 4))
                assert moved_left['endpoints'] & moved_right['endpoints']
                collision_images += 1
    return dict(incoming_dimension_triples=len(parameters),
                anchored_catalogue_roles=len(candidates),
                surviving_left_roles=len(libraries[0]), surviving_right_roles=len(libraries[1]),
                left_forms=dict(left_forms), right_forms=dict(right_forms),
                distinct_owner_collisions=len(libraries[0])*len(libraries[1]),
                symmetry_collision_images=collision_images,
                scope='Exact anchored role masks; arbitrary incoming dimensions are covered by the written coordinate argument, not this finite library.')


def dimension_controls():
    checked = reclassified = 0
    smallest_exceptional = None
    for width, left, right in itertools.product(range(6, 32, 2),
                                               range(4, 32, 2), range(4, 32, 2)):
        matching = width+(left+right)//2-1
        module = source(width, left, right)
        assert len(module['matching']) == matching
        eligible = compensated(width, left, right)
        if matching <= 13:
            assert eligible
        if not eligible:
            assert matching >= 14
            smallest_exceptional = matching if smallest_exceptional is None else min(smallest_exceptional, matching)
        if width == 8 and {left, right} == {4, 8}:
            assert eligible and matching == 13
            reclassified += 1
        checked += 1
    assert smallest_exceptional == 14 and reclassified == 2
    return dict(positive_dimension_controls=checked, new_dimension_shapes=reclassified,
                minimum_remaining_exceptional_matching=smallest_exceptional)


def physical_controls():
    images = marked_images = new_shape_double_occurrences = single_mark_occurrences = 0
    negative_capacity_checks = 0
    inventories = list(fixtures())+[('complete_fullbar_exit', witness_modules()),
                                   ('new_shape_isolated', [source(8, 4, 8)])]
    for name, modules in inventories:
        for _, _, _, current, moved in phase_images(modules):
            records = records_of(moved)
            _, potential, _, _ = complete_certificate(records)
            marks = actual_marks(records)
            report = inspect_sources(current, moved)
            assignments = {tuple(item['tile']): item
                           for item in inspect_slots(current, moved)['marked_assignments']}
            assert sum(marks.values()) == report['marked']
            assert potential-sum(marks.values()) == report['exact_joint_margin']
            endpoints = set.union(*(record[0] for record in records))
            defects = defect_tiles(moved, endpoints)
            assigned = set()
            census = Counter()
            for index, marked in marks.items():
                width, left, right, _, _ = positive_dimensions(moved[index])
                single_mark_occurrences += marked == 1
                if marked != 2:
                    continue
                if not compensated(width, left, right):
                    census['exceptional'] += 1
                    continue
                activated = sum(len(cells & records[index][0]) == 1 and
                                len(cells & records[index][1]) == 2 and
                                bool(cells & records[index][1] & endpoints)
                                for cells in (vertices_of({tile}) for tile in moved[index]['receiver']))
                census[activated] += 1
                new_shape_double_occurrences += width == 8 and {left, right} == {4, 8}
                if activated:
                    continue
                blank = []
                for chosen, _, _, _ in paired_guards(moved[index]):
                    tile = tuple(value//2 for value in chosen)
                    if assignments[tile]['kind'] == 'blank_gate':
                        assert defects[tile] == 'L2bar'
                        blank.append(tile)
                if blank:
                    tile = min(blank)
                    slots = {(tile, 0), (tile, 1)}
                else:
                    assert not (width == 8 and {left, right} == {4, 8})
                    forced = both_forced_tiles(moved[index], moved, endpoints)
                    slots = {(tile, 0) for tile in forced}
                assert not assigned & slots
                assigned |= slots
            assert len(assigned) == 2*census[0]
            assert len(assigned) <= report['boundary_cost']
            zero, single, twice = (census[index] for index in range(3))
            exceptional = census['exceptional']
            assert 2*report['event_reserve'] >= 2*zero+single+2*twice
            assert report['exact_joint_margin'] >= report['unmarked_sources']-exceptional-single//2
            positive_matching = sum(len(moved[index]['matching']) for index in marks)
            negative_matching = sum(len(module['matching']) for module in moved
                                    if module['charge'] < 0 and len(module['endpoints']) != 8)
            matching = sum(len(module['matching']) for module in moved)
            assert positive_matching >= 9*len(marks)+5*exceptional
            assert 9*sum(marks.values()) <= 4*negative_matching
            assert 4*matching >= 36*len(marks)+20*exceptional+9*sum(marks.values())
            assert 37*report['exact_joint_margin']+2*matching >= 0
            assert 74*len(current[2])+70*len(current[3]) <= 37*current[0]*current[1]
            marked_images += any(marks.values())
            negative_capacity_checks += 1
            images += 1
    return dict(complete_physical_images=images, marked_images=marked_images,
                negative_matching_capacity_checks=negative_capacity_checks,
                single_marked_positive_occurrences=single_mark_occurrences,
                newly_compensated_double_occurrences=new_shape_double_occurrences,
                scope='Complete physical original-source checks. Newly compensated double shapes, if absent, are covered by the general obstruction and role masks rather than claimed as exercised physical branches.')


def arithmetic_controls():
    checked = negative = 0
    for exceptional, single, positive, reserve, marked in itertools.product(
            range(5), range(7), range(1, 10), range(9), range(19)):
        if exceptional+single > positive or marked > 2*positive:
            continue
        margin = positive+reserve-marked
        if margin < -exceptional-single//2:
            continue
        minimum_matching = (36*positive+20*exceptional+9*marked+3)//4
        assert 37*margin+2*minimum_matching >= 0
        if margin < 0:
            negative += 1
        checked += 1
    assert negative > 0
    witness = dict(positive=2, exceptional=2, single=0, reserve=0, marked=4,
                   margin=-2, matching=37, physical_realization_asserted=False)
    assert 36*2+20*2+9*4 == 4*37
    return dict(signed_budget_controls=checked, negative_margin_controls=negative,
                supplied_inequality_equality=witness)


def main():
    print(json.dumps(dict(status='PASS', roles=incoming_role_controls(),
                         dimensions=dimension_controls(), physical=physical_controls(),
                         arithmetic=arithmetic_controls(),
                         scope='Finite exact controls supplement the general low-cost obstruction and single-use compensation proof. No arbitrary-grid decomposition, new complete AA realization or geometric sharpness claim.'), indent=2))


if __name__ == '__main__':
    main()
