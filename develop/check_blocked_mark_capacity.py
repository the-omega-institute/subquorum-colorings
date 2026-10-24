"""Exact role, original-slot and complete-fusion controls for coefficient 39/41."""

from collections import Counter
import itertools
import json

from all_phase_joint_slots import boundary, inspect_slots, tile_of
from check_activated_singleton_budget import phase_images
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_cost_fourteen_compensation import middle_dimensions, terminal_occurrences
from check_exact_event_reserve import fixtures
from check_fullbar_unactivated_obstruction import witness_modules
from check_localized_exterior_tile_budget import complete_certificate
from check_low_cost_exceptional_doubles import compensated
from check_minus_one_tip_obstructions import source
from check_multiple_positive_saturation import inspect_sources
from check_occupied_gate_activation import positive_dimensions
from check_regular_tile_compensation import profile_counts
from check_short_leg_defect_injection import defect_tiles, inverse_affine
from check_unactivated_double_compensation import both_forced_tiles
from check_width_six_actual_mark_excess import actual_marks, records_of
from degree_four_overcount import opposed_modules
from dual_guard_compensation import paired_guards
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def two_slot_dimensions(width, left, right):
    return compensated(width, left, right) or width == 10 and {left, right} == {4, 8}


def fifteen_dimensions(width, left, right):
    return (width == 8 and (left, right) in {(4, 12), (12, 4), (6, 10), (10, 6), (8, 8)}
            or (width, left, right) == (12, 4, 4))


def original_leg(module, terminal):
    width, left, right, symmetry, offset = positive_dimensions(module)
    normalized = affine(terminal, symmetry, offset)
    if normalized == (left, 1):
        return 0, left, inverse_affine((0, 1), symmetry, offset)
    assert normalized == (right, width)
    return 1, right, inverse_affine((0, width), symmetry, offset)


def phase_and_corners(module):
    width, left, right, symmetry, offset = positive_dimensions(module)
    corners = {inverse_affine(point, symmetry, offset) for point in ((0, 1), (0, width))}
    phase = ('01' if module['charge'] == -1 else '11' if boundary(module)[1] else '10')
    return phase, corners


def anchored_roles():
    parameters = list(itertools.product((6, 8, 12, 20), (4, 6, 8, 10, 12),
                                       (4, 6, 8, 10, 12)))+[(40, 30, 4), (20, 4, 30)]
    gate = (2, 2)
    cells = vertices_of({(1, 1)})
    roles = []
    for dimensions in parameters:
        width, left, right = dimensions
        base = source(*dimensions)
        for role, point, height in [('A', (0, 1), 0), ('A', (0, width), 0),
                                     ('F', (left, 1), left), ('F', (right, width), right)]:
            for symmetry in itertools.product((False, True), repeat=3):
                root = affine(point, symmetry)
                offset = tuple(target-value for target, value in zip(gate, root))
                module = transform_module(base, symmetry, offset)
                if (set(neighbors(gate))-cells) & module['endpoints']:
                    continue
                phase = ('01' if module['charge'] == -1 else
                         '11' if profile_counts(module)[3, 0] else '10')
                predecessor = (None if role == 'A' else
                               tuple(value-target for value, target in
                                     zip(affine((point[0]-1, point[1]), symmetry, offset), gate)))
                roles.append(dict(parameters=dimensions, role=role, phase=phase,
                                  height=height, predecessor=predecessor, module=module))
    return parameters, roles


def forced_corner_premises(producer, incoming, corner, target):
    assert corner in incoming['endpoints']
    assert target in producer['selected']
    assert set(neighbors(corner))-(incoming['endpoints'] | incoming['selected']) == {target}
    assert tile_of(corner) == tile_of(target)
    assert corner in boundary(incoming)[2]
    assert len(set(neighbors(target)) & (producer['endpoints'] | incoming['endpoints'])) >= 2


def role_controls():
    dimensions, roles = anchored_roles()
    results = []
    for parameters in ((8, 4, 12), (8, 6, 10), (8, 8, 8), (10, 4, 8), (12, 4, 4)):
        width, left, right = parameters
        producer = source(*parameters)
        forbidden = {(left+1, 2), (right+1, width-1)}
        libraries = []
        for reflected in (False, True):
            library = {}
            for specification in roles:
                incoming = (transform_module(specification['module'], (False, False, True), (0, width+1))
                            if reflected else specification['module'])
                if producer['endpoints'] & incoming['endpoints']:
                    continue
                if forbidden & (incoming['endpoints'] | incoming['selected']):
                    continue
                library[frozenset(incoming['endpoints'])] = specification, incoming
            libraries.append(list(library.values()))
        census = Counter()
        for first, left_owner in libraries[0]:
            for second, right_owner in libraries[1]:
                if left_owner['endpoints'] == right_owner['endpoints']:
                    if parameters == (8, 6, 10):
                        expected = transform_module(source(6, 4, 4), (False, True, False), (6, 1))
                        assert left_owner['endpoints'] == expected['endpoints']
                        census['common_tight'] += 1
                    else:
                        assert parameters == (8, 8, 8)
                        upright = transform_module(source(6, 4, 4), (False, False, False), (2, 1))
                        if left_owner['endpoints'] == upright['endpoints']:
                            assert left_owner['charge'] == -1
                            census['common_phase01_capacity'] += 1
                        else:
                            height = original_leg(left_owner, (2, 2))[1]
                            assert height in (4, 6)
                            expected = transform_module(source(6, height, height),
                                                        (False, True, False), (height+2, 1))
                            assert left_owner['endpoints'] == expected['endpoints']
                            if height == 4:
                                forced_corner_premises(producer, left_owner, (6, 2), (7, 2))
                                census['common_forced_corner_event'] += 1
                            else:
                                census['common_tight'] += 1
                elif left_owner['endpoints'] & right_owner['endpoints']:
                    census['distinct_owner_collision'] += 1
                elif parameters == (8, 4, 12):
                    assert first['phase'] == second['phase'] == '11'
                    assert first['predecessor'] == (0, 1) and first['height'] == 4
                    assert second['predecessor'] == (1, 0) and second['height'] in (8, 10)
                    assert first['parameters'][0] <= second['height']-2
                    if second['height'] == 8:
                        forced_corner_premises(producer, right_owner, (10, 7), (11, 7))
                        assert original_leg(right_owner, (2, 7))[2] == (10, 7)
                        census['disjoint_forced_corner_event'] += 1
                    else:
                        census['disjoint_tight'] += 1
                else:
                    assert parameters == (12, 4, 4)
                    assert first['phase'] == second['phase'] == '11'
                    assert first['height'] == second['height'] == 4
                    assert first['predecessor'] == second['predecessor'] == (0, 1)
                    for incoming, corner, target, other in (
                            (left_owner, (2, 6), (2, 7), right_owner),
                            (right_owner, (2, 7), (2, 6), left_owner)):
                        assert corner in boundary(incoming)[2]
                        assert set(neighbors(corner))-(incoming['endpoints'] | incoming['selected']) == {target}
                        assert target in other['endpoints'] and tile_of(corner) == tile_of(target)
                    assert original_leg(left_owner, (2, 2))[2] == (2, 6)
                    census['disjoint_adjacent_bands_two_corner_events'] += 1
        results.append(dict(parameters=parameters, left_roles=len(libraries[0]),
                            right_roles=len(libraries[1]), outcomes=dict(census)))
    return dict(incoming_dimensions=len(dimensions), anchored_roles=len(roles), cases=results,
                scope='Finite original role masks and forced-consumption premises, not complete new fusions or an unbounded proof.')


def physical_control(current, modules):
    records = records_of(modules)
    _, potential, _, _ = complete_certificate(records)
    report = inspect_sources(current, modules)
    endpoints = set.union(*(module['endpoints'] for module in modules))
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    marks = actual_marks(records)
    assignments = {tuple(item['tile']): item for item in inspect_slots(current, modules)['marked_assignments']}
    assigned_mark_points = {item['witness'] for item in assignments.values()}
    defects = defect_tiles(modules, endpoints)
    h_pool = {(tile, slot) for tile, kind in defects.items()
              for slot in range(2 if kind in ('L2bar', 'L2mutual') else 1)}
    a_pool = {(index, tile) for index in marks for tile in terminal_occurrences(modules[index], endpoints)}
    phases = Counter()
    fired_corners = set()
    negative_matching = 0
    for index, module in enumerate(modules):
        if module['charge'] >= 0 or len(module['endpoints']) == 8:
            continue
        phase, corners = phase_and_corners(module)
        phases[phase] += 1
        negative_matching += len(module['matching'])
        if phase != '11':
            continue
        occupied = module['endpoints'] | module['selected']
        for corner in corners:
            assert corner in boundary(module)[2]
            if any(target in endpoints and tile_of(target) == tile_of(corner)
                   for target in set(neighbors(corner))-occupied):
                fired_corners.add((index, corner))
                assert corner not in assigned_mark_points
    marked = sum(marks.values())
    capacity = 2*phases['01']+2*phases['10']+4*phases['11']
    assert marked+len(fired_corners) <= capacity
    assert 4*negative_matching >= 9*marked+18*phases['01']+18*phases['10']+9*len(fired_corners)
    census = Counter()
    reserved_h = []
    reserved_a = []
    bad_tokens = []
    for index, marked_sides in marks.items():
        if marked_sides != 2:
            continue
        producer = modules[index]
        width, left, right, symmetry, offset = positive_dimensions(producer)
        census['new_two_slot'] += width == 10 and {left, right} == {4, 8}
        two = two_slot_dimensions(width, left, right)
        fourteen = middle_dimensions(width, left, right)
        fifteen = fifteen_dimensions(width, left, right)
        if not (two or fourteen or fifteen):
            assert len(producer['matching']) >= 16
            census['remaining'] += 1
            continue
        activation = sorted(terminal_occurrences(producer, endpoints))
        census['two_%d' % len(activation) if two else 'fourteen' if fourteen else 'fifteen'] += 1
        if activation:
            reserved_a.extend((index, tile) for tile in (activation if two else activation[:1]))
            continue
        blank = [tile_of(guard[0]) for guard in paired_guards(producer)
                 if assignments[tile_of(guard[0])]['kind'] == 'blank_gate']
        if blank:
            reserved_h.extend((min(blank), slot) for slot in range(2 if two else 1))
            continue
        if two:
            assert not (width == 10 and {left, right} == {4, 8})
            reserved_h.extend((tile, 0) for tile in both_forced_tiles(producer, modules, endpoints))
            continue

        def original(point):
            return inverse_affine(point, symmetry, offset)

        tight = []
        for reflected, height in ((False, left), (True, right)):
            gate = original((2, width-1 if reflected else 2))
            owner = owners[gate]
            incoming = modules[owner]
            if phase_and_corners(incoming)[0] != '11':
                continue
            _, incident, _ = original_leg(incoming, gate)
            if incident != height-2:
                continue
            columns = (width-2, width-1) if reflected else (2, 3)
            cells = {original(point) for point in itertools.product((height, height+1), columns)}
            corner = original((height, width-1 if reflected else 2))
            assert not cells & incoming['selected']
            assert not cells & (producer['endpoints'] | producer['selected'])
            assert len(cells & incoming['endpoints']) == 2
            tile = tile_of(corner)
            assert cells == vertices_of({tile}) and defects[tile] in ('L2bar', 'L3')
            tight.append(tile)
        if tight:
            reserved_h.append((min(tight), 0))
            continue
        assert fifteen
        census['bad'] += 1
        gate = original((2, 2 if left >= right else width-1))
        if width == 8 and left == right == 8:
            owner = owners[gate]
            if modules[owner]['charge'] == -1:
                assert owners[original((2, 2))] == owners[original((2, 7))]
                bad_tokens.append(('source01', owner))
                continue
        owner = owners[gate]
        _, _, corner = original_leg(modules[owner], gate)
        assert (owner, corner) in fired_corners
        bad_tokens.append(('corner11', owner, corner))
    assert len(set(reserved_h)) == len(reserved_h) and set(reserved_h) <= h_pool
    assert len(set(reserved_a)) == len(reserved_a) and set(reserved_a) <= a_pool
    assert len(set(bad_tokens)) == len(bad_tokens)
    zero, single, twice = (census['two_%d' % amount] for amount in range(3))
    fourteen, fifteen, remaining, bad = (census[key] for key in ('fourteen', 'fifteen', 'remaining', 'bad'))
    assert len(reserved_h)+len(reserved_a) == 2*zero+single+2*twice+fourteen+fifteen-bad
    assert bad <= phases['01']+len(fired_corners)
    assert marked+bad <= 4*sum(phases.values())
    assert 2*report['event_reserve'] >= 2*zero+single+2*twice+fourteen+fifteen-bad
    positive_matching = sum(len(modules[index]['matching']) for index in marks)
    matching = sum(len(module['matching']) for module in modules)
    assert positive_matching >= 9*len(marks)+5*fourteen+6*fifteen+7*remaining
    assert 4*matching >= 36*len(marks)+20*fourteen+24*fifteen+28*remaining+9*marked+9*bad
    margin = potential-marked
    assert margin == report['exact_joint_margin']
    assert 41*margin+2*matching >= 0
    assert 82*len(current[2])+78*len(current[3]) <= 41*current[0]*current[1]
    return dict(fired_phase11_corners=len(fired_corners), bad=bad, fifteen=fifteen,
                reserved_h=len(reserved_h), reserved_a=len(reserved_a),
                strict_corner_capacity=bool(fired_corners), new_two_slot=census['new_two_slot'])


def dimension_controls():
    checked = 0
    for width, left, right in itertools.product(range(6, 34, 2), range(4, 34, 2), range(4, 34, 2)):
        matching = width+(left+right)//2-1
        covered = (two_slot_dimensions(width, left, right) or middle_dimensions(width, left, right)
                   or fifteen_dimensions(width, left, right))
        if matching <= 15:
            assert covered
        if not covered:
            assert matching >= 16
        checked += 1
    return checked


def arithmetic_controls():
    checked = negative = 0
    for single, fourteen, fifteen, remaining in itertools.product(range(5), repeat=4):
        for bad in range(fifteen+1):
            for zero, twice, unmarked in itertools.product(range(3), repeat=3):
                positive = zero+single+twice+fourteen+fifteen+remaining+unmarked
                marked = 2*(zero+single+twice+fourteen+fifteen+remaining)
                minimum = (2*zero+single+2*twice+fourteen+fifteen-bad+1)//2
                for reserve in range(minimum, minimum+3):
                    margin = positive+reserve-marked
                    budget = 36*positive+20*fourteen+24*fifteen+28*remaining+9*marked+9*bad
                    matching = (budget+3)//4
                    assert 41*margin+2*matching >= 0
                    checked += 1
                    negative += margin < 0
    return dict(conditional_budgets=checked, negative_margin_budgets=negative)


def main():
    inventories = list(fixtures())+[('fullbar_exit', witness_modules()),
                                  ('isolated_15_8_8', [source(8, 8, 8)]),
                                  ('isolated_15_12_4', [source(12, 4, 4)]),
                                  ('isolated_two_slot', [source(10, 4, 8)])]
    for amount in (2, 4, 8):
        modules = [transform_module(module, (False, False, False), (0, 30*index))
                   for index in range(amount) for module in opposed_modules(6+2*(index % 2), 4)]
        inventories.append(('multiple_%d' % amount, modules))
    totals = Counter()
    for _, modules in inventories:
        for _, _, _, current, moved in phase_images(modules):
            record = physical_control(current, moved)
            totals['complete_physical_images'] += 1
            for key, value in record.items():
                totals[key] += value
    print(json.dumps(dict(status='PASS', roles=role_controls(),
                          dimensions=dimension_controls(), arithmetic=arithmetic_controls(),
                          physical=dict(totals),
                          scope='Exact resource, event and original-capacity checks. New cost15 complete branches, if zero, are explicit limitations; the universal geometry/injections are written proofs.'), indent=2))


if __name__ == '__main__':
    main()
