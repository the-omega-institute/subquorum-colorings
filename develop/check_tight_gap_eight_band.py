"""Geometric controls for the tight gap-eight band activation channel."""

from collections import Counter
import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import original
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def records(dimensions, symmetry, offset):
    endpoints, supports, matching = independent_source(dimensions, symmetry, offset)
    assert len(endpoints) == 2*len(matching)
    assert {point for edge in matching for point in edge} == endpoints
    return endpoints, supports


def candidate_roles():
    result = []
    for dimensions in itertools.product((6, 10, 20), (4, 6, 8, 12, 20, 32), (4, 8, 16)):
        for symmetry in SYMMETRIES:
            module = original(dimensions, symmetry)
            for point in module['endpoints']:
                own = set(neighbors(point)) & module['endpoints']
                allowed = {(point[0]+1, point[1]), (point[0], point[1]-1)}
                if not own <= allowed:
                    continue
                shifted = transform_module(module, (False, False, False), (-point[0], -point[1]))
                result.append((dimensions, symmetry, point, shifted))
    return result


def rotor_controls():
    forms = {}
    for symmetry in SYMMETRIES:
        module = transform_module(rotor(), symmetry)
        for point in module['endpoints']:
            own = set(neighbors(point)) & module['endpoints']
            if not own <= {(point[0]+1, point[1]), (point[0], point[1]-1)}:
                continue
            moved = transform_module(module, (False, False, False), (-point[0], -point[1]))
            forms[frozenset(moved['endpoints'])] = moved
    assert len(forms) == 4
    west = [points for points in forms if (0, -1) in points]
    south = [points for points in forms if (1, 0) in points]
    assert len(west) == len(south) == 2
    assert all({(-1, -1), (-1, -2)} & points for points in west)
    assert all((2, 0) in points for points in south)
    return dict(four_rotor_roles_excluded=4, negative_successor_rotor_roles_excluded=2)


def geometric_controls():
    counts = Counter()
    candidates = candidate_roles()
    for height, width, far, other in itertools.product((12, 18, 26), (10, 18, 28), (4, 8), (4, 10)):
        breadth = width-4
        cross, _ = records((width, height, far), (True, True, False), (1, height+2))
        east, supports = records((breadth, 4, other), (True, True, False), (2, height))
        assert not cross & east
        point = (width-1, height)
        successor = (width, height)
        assert point in supports and point not in cross | east
        assert {(width-2, height), (width-1, height+1), (width+1, height)} <= cross | east
        assert len(set(neighbors((width-1, height+1))) & cross) == 3
        assert len(set(neighbors((width-2, height))) & east) == 2
        fixed = cross | east
        for dimensions, symmetry, anchor, module in candidates:
            moved = transform_module(module, (False, False, False), point)
            counts['anchored_U_roles'] += 1
            if moved['endpoints'] & fixed:
                continue
            assert set(neighbors(point)) & moved['endpoints'] == {(width-1, height-1)}
            if anchor == affine((dimensions[1], 1), symmetry):
                incident = dimensions[1]
            else:
                assert anchor == affine((dimensions[2], dimensions[0]), symmetry)
                incident = dimensions[2]
            downward = max(row for row, _ in moved['endpoints']) > point[0]
            if downward:
                assert incident >= far and moved['charge'] == 1
                assert {(width-2, height), (width-1, height+1)} <= moved['selected'] & fixed
                counts['positive_downward_terminal_roles'] += 1
                continue
            assert incident >= other+2 and moved['charge'] == -1
            assert successor in moved['selected'] and successor not in fixed | moved['endpoints']
            assert {(width-1, height), (width, height+1), (width+1, height)} <= fixed | moved['endpoints']
            counts['negative_upward_terminal_roles'] += 1
            for new_incident, new_downward in itertools.product((4, 8, 12, 24, 40), (False, True)):
                offset = (width-1, height-new_incident) if new_downward else (
                    width+1, height-new_incident)
                successor_module = original((6, new_incident, 4),
                                            (True, False, not new_downward), offset)
                if successor_module['endpoints'] & (fixed | moved['endpoints']):
                    continue
                if new_downward:
                    assert new_incident >= far and successor_module['charge'] < 0
                    counts['negative_downward_successor_roles'] += 1
                else:
                    assert new_incident >= incident+2 and successor_module['charge'] == 1
                    assert {(width, height+1), (width+1, height)} <= successor_module['selected'] & cross
                    counts['positive_upward_successor_roles_not_credited'] += 1
    return dict(counts)


def old_target_controls():
    counts = Counter()
    for width, height, far, incident, old_far in itertools.product(
            (10, 18, 28), (12, 18), (4, 10), (4, 8, 16), (4, 12)):
        cross, _ = records((width, height, far), (True, True, False), (1, height+2))
        rows = [
            ('S', (6, 4, old_far), (True, True, True), (width+1, height+3),
             (1, 1), (0, 1), lambda row, column: (incident+3-row, 3-column)),
            ('P', (incident+4, 4, old_far), (False, False, False),
             (width-4, height-incident-2), (0, incident+3), (0, 1),
             lambda row, column: (column+2, row+2)),
            ('E', (6, 4, old_far), (False, False, True), (width-4, height+3),
             (0, 1), (0, 6), lambda row, column: (column+2, incident+3-row)),
            ('Scomp', (6, 4, old_far), (True, True, False), (width-4, height+3),
             (1, 1), (0, 1), lambda row, column: (incident+3-row, column+2))]
        for name, dimensions, symmetry, offset, witness, outside, target_frame in rows:
            endpoints, _ = records(dimensions, symmetry, offset)
            assert affine(witness, symmetry, offset) in endpoints & cross
            assert affine(outside, symmetry, offset) in endpoints-cross
            for test in ((0, 1), (1, 1), (incident, 1), (4, 6)):
                assert affine(target_frame(*test), symmetry, offset) == (
                    test[1]+width-2, test[0]+height-incident)
            counts[name+'_collision_and_self_owner_exclusion'] += 1
        canonical, _ = records((width, height, far), (False, False, False), (0, 0))
        assert len(set(neighbors((4, 1))) & canonical) == 2
    return dict(counts)


def normalized_partial_control():
    specifications = [
        ((22, 4, 4), (False, False, False), (0, 0)),
        ((12, 8, 4), (False, True, False), (11, 1)),
        ((18, 18, 8), (True, True, False), (1, 20)),
        ((6, 10, 4), (True, False, False), (2, 3)),
        ((14, 4, 8), (True, True, False), (2, 18)),
        ((6, 8, 4), (True, False, False), (16, 10))]
    modules = [original(*specification) for specification in specifications]
    endpoints = set().union(*(module['endpoints'] for module in modules))
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    assert (3, 2) in modules[0]['selected'] & modules[1]['endpoints']
    assert (2, 2) in modules[1]['selected'] & modules[2]['endpoints']
    assert (3, 3) in modules[2]['selected'] & modules[3]['endpoints']
    assert (3, 14) in modules[3]['selected'] & modules[4]['endpoints']
    assert (17, 18) in modules[4]['selected'] & modules[5]['endpoints']
    assert {(16, 18), (17, 19)} <= modules[5]['selected'] & endpoints
    assert modules[5]['charge'] == 1
    return dict(specifications=specifications, scope='Six-source normalized PARTIAL chain only; not a complete extension.')


def general_width_controls():
    counts = Counter()
    for breadth, slack, height, far, incident, target_width in itertools.product(
            (6, 10, 18), (4, 6, 8, 14), (12, 22), (4, 10), (4, 6, 12), (6, 10)):
        width = breadth+slack
        cross, _ = records((width, height, far), (True, True, False), (1, height+2))
        east, _ = records((breadth, 4, 4), (True, True, False), (2, height))
        north, east_support = (breadth+2, height), (breadth+3, height+1)
        assert len(set(neighbors(east_support)) & cross) == 3
        assert set(neighbors(north)) & east == {(breadth+1, height), (breadth+2, height-1)}
        rightward = original((target_width, incident, 4), (False, True, False),
                             (incident+breadth+3, height-1))
        assert rightward['endpoints'] & cross
        counts['south_terminal_rightward_bar_exclusions'] += 1
        for role, symmetry, offset in (
                ('D', (True, False, False), (breadth+2, height-incident)),
                ('L', (False, True, True), (incident+breadth+3, height+1))):
            target = original((target_width, incident, 4), symmetry, offset)
            if target['endpoints'] & (cross | east):
                continue
            assert target['charge'] == 1
            assert {north, east_support} <= target['selected'] & (cross | east)
            if role == 'L':
                assert incident <= slack-4
            elif target_width >= slack:
                assert incident >= far
            counts[role+'_PARTIAL_positive_targets'] += 1
        frames = [
            ('D_S', (True, True, True), (breadth+5, height+3),
             (1, 1), (0, 1), lambda row, column: (incident+3-row, 3-column), 'D'),
            ('D_P', (False, False, False), (breadth, height-incident-2),
             (0, incident+3), (0, 1), lambda row, column: (column+2, row+2), 'D'),
            ('D_E', (False, False, True), (breadth, height+3),
             (0, 1), (0, 6), lambda row, column: (column+2, incident+3-row), 'D'),
            ('D_Scomp', (True, True, False), (breadth, height+3),
             (1, 1), (0, 1), lambda row, column: (incident+3-row, column+2), 'D'),
            ('L_S', (False, False, False), (breadth, height-2),
             (0, 3), (0, 1), lambda row, column: (incident+3-row, 3-column), 'L'),
            ('L_P', (True, True, True), (incident+breadth+5, height+3),
             (1, incident+3), (0, incident+3), lambda row, column: (column+2, row+2), 'L'),
            ('L_E', (True, True, False), (breadth, height+3),
             (1, 1), (0, 1), lambda row, column: (column+2, incident+3-row), 'L'),
            ('L_Scomp', (False, False, True), (breadth, height+3),
             (0, 1), (0, 6), lambda row, column: (incident+3-row, column+2), 'L')]
        for name, symmetry, offset, collision, outside, old_frame, role in frames:
            old_width = incident+4 if name.endswith('_P') else 6
            old, _ = records((old_width, 4, 10), symmetry, offset)
            assert affine(collision, symmetry, offset) in old & cross
            assert affine(outside, symmetry, offset) in old-cross
            for row, column in ((0, 1), (1, 1), (incident, 1), (4, 6)):
                target_point = (column+breadth+2, row+height-incident) if role == 'D' else (
                    incident+breadth+3-row, height+1-column)
                assert affine(old_frame(row, column), symmetry, offset) == target_point
            counts[name+'_collision_and_self_owner_exclusion'] += 1
    return dict(counts)


def integer_controls():
    checked = 0
    for difference, extra, transferred in itertools.product(range(-20, 21), range(6), range(7)):
        old = -((-(difference+extra))//2)
        new = -((-(difference+extra+transferred))//2)
        assert new-old in (transferred//2, (transferred+1)//2)
        assert (new >= 0) == (difference+extra+transferred >= -1)
        checked += 1
    return checked


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', rotors=rotor_controls(),
                         geometry=geometric_controls(), old_targets=old_target_controls(),
                         general_widths=general_width_controls(),
                         normalized_partial=normalized_partial_control(), integer_controls=integer_controls(),
                         scope='Finite controls supplement written arbitrary-dimension proofs. '
                               'No complete witness; global source-role reconstruction and joint injection remain written. '
                               'Negative continuation activations are not credited.'), indent=2))
