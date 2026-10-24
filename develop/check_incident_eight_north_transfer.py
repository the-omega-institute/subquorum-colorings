"""Independent finite controls for the eight-step escape activation transfer."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def shift(record, offset):
    move = lambda point: (point[0]+offset[0], point[1]+offset[1])
    return ({move(point) for point in record[0]}, {move(point) for point in record[1]},
            {tuple(sorted((move(first), move(second)))) for first, second in record[2]})


def axial_library(allowed):
    library = {}
    for dimensions in itertools.product(range(6, 20, 2), range(4, 20, 2), range(4, 20, 2)):
        for symmetry in itertools.product((False, True), repeat=3):
            original = independent_source(dimensions, symmetry, (0, 0))
            for anchor in original[0]:
                own = {(row-anchor[0], column-anchor[1])
                       for row, column in set(neighbors(anchor)) & original[0]}
                if not own <= allowed:
                    continue
                assert own
                moved = shift(original, (-anchor[0], -anchor[1]))
                key = tuple(frozenset(part) for part in moved)
                library[key] = moved
    rotors = {}
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        record = module['endpoints'], module['selected'], {
            tuple(sorted(edge)) for edge in module['matching']}
        for anchor in module['endpoints']:
            own = {(row-anchor[0], column-anchor[1])
                   for row, column in set(neighbors(anchor)) & module['endpoints']}
            if own <= allowed:
                moved = shift(record, (-anchor[0], -anchor[1]))
                rotors[frozenset(moved[0])] = moved
    return list(library.values()), list(rotors.values())


def sources(bottom, near, width, incident, other):
    return [independent_source((bottom-2, near, 6), (True, False, False), (2, 3)),
            independent_source((6, 8, 4), (True, True, True), (bottom+2, 11)),
            independent_source((width, incident, other),
                               (False, False, False), (bottom-1-incident, 4))]


def charge(record):
    tiles = {(row//2, column//2) for row, column in record[0]}
    selected_inside = {point for point in record[1] if (point[0]//2, point[1]//2) in tiles}
    return len(record[2])+len(selected_inside)-2*len(tiles)


def secondary_controls(library, rotors):
    patterns = survivors = 0
    for incident, extra, width, other in itertools.product(
            (8, 10, 12), (6, 16), (8, 12, 20), (4, 12)):
        bottom = incident+extra
        fixed = sources(bottom, 4, width, incident, other)
        blocked = set.union(*(record[0] for record in fixed))
        assert len(blocked) == sum(len(record[0]) for record in fixed)
        point = bottom-1, 6
        assert point in fixed[0][1] and point not in blocked
        assert (bottom, 6) in fixed[0][0] and (bottom-1, 5) in fixed[2][0]
        for relative in library:
            current = shift(relative, point)
            if current[0] & blocked:
                continue
            outer = min(row for row, column in current[0])
            breadth = max(column for row, column in current[0])-5
            length = bottom-1-outer
            far = max(row for row, column in current[0] if column == breadth+5)-outer
            assert 6 <= length <= incident-2
            assert current == independent_source((breadth, length, far),
                                                 (False, False, False), (outer, 5))
            survivors += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
        patterns += 1
    return dict(prescribed_patterns=patterns, surviving_U_roles=survivors,
                surviving_rotors=0, every_survivor_has_the_stated_secondary_frame=True)


def positive_controls(library, rotors):
    patterns = survivors = blocked_eight = intersecting_fixed = 0
    for parent_incident, near, width, breadth, other, far in itertools.product(
            (8, 10, 12), (4, 20), (10, 12, 16, 20), (8, 10, 12, 18), (4, 12), (4, 10)):
        bottom = parent_incident+6
        if parent_incident == 8 and breadth > width-2:
            continue
        fixed = sources(bottom, near, width, parent_incident, other)
        intermediate = independent_source((breadth, 6, far),
                                          (False, False, False), (bottom-7, 5))
        fixed.append(intermediate)
        blocked = set.union(*(record[0] for record in fixed))
        if len(blocked) != sum(len(record[0]) for record in fixed):
            intersecting_fixed += 1
            continue
        point = bottom-5, 7
        assert point in fixed[1][1] and point not in blocked
        assert set(neighbors(point)) & blocked == {
            (bottom-6, 7), (bottom-5, 6), (bottom-4, 7)}
        count = 0
        for relative in library:
            current = shift(relative, point)
            if current[0] & blocked:
                continue
            outer = max(column for row, column in current[0])
            length = outer-7
            span = max(row for row, column in current[0])-(bottom-6)
            other_leg = outer-min(column for row, column in current[0]
                                  if row == bottom-6+span)
            assert 6 <= length <= breadth-4
            expected = independent_source((span, length, other_leg),
                                           (True, True, False), (bottom-6, length+7))
            assert current == expected and charge(current) == 1
            assert (bottom-5, 6) in current[1] & intermediate[0]
            assert (bottom-6, 7) in current[1] & intermediate[0]
            tile = {(row, column) for row in (bottom-6, bottom-5) for column in (6, 7)}
            assert tile-{point} <= intermediate[0]
            assert len(set(neighbors((bottom-5, 6))) & intermediate[0]) == 2
            assert len(set(neighbors((bottom-6, 7))) & intermediate[0]) == 3
            assert charge(intermediate) == 1-breadth and charge(fixed[2]) == 1-width
            assert (bottom-4, 4) in fixed[0][0] and (bottom-4, 5) in fixed[2][0]
            assert (bottom-8, 6) not in intermediate[0] and (bottom-7, 6) in intermediate[0]
            survivors += 1
            count += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
        if breadth == 8:
            assert count == 0
            blocked_eight += 1
        patterns += 1
    return dict(prescribed_patterns=patterns, surviving_positive_U_roles=survivors,
                surviving_rotors=0, width_eight_D_noncompletion_controls=blocked_eight,
                excluded_fixed_source_intersections=intersecting_fixed,
                parent_incident_lengths=[8, 10, 12], secondary_incident_length=6,
                every_survivor_has_exact_activated_positive_E_frame=True)


def old_frame_controls():
    comparisons = 0
    for bottom, incident, row, column in itertools.product(
            (14, 24, 100), (6, 8, 20), range(5), range(1, 8)):
        target = lambda first, second: (bottom-6+second, incident+7-first)
        old_s = incident+3-row, 3-column
        old_p = column+2, row+2
        assert (bottom-3-old_s[1], old_s[0]+4) == target(row, column)
        assert (bottom-8+old_p[0], incident+9-old_p[1]) == target(row, column)
        comparisons += 2
    parity = 0
    for baseline, added in itertools.product(range(-40, 41), range(17)):
        gain = (baseline+added+1)//2-(baseline+1)//2
        assert gain >= 0 and gain in (added//2, (added+1)//2)
        assert (baseline+added+3)//2-(baseline+added+1)//2 == 1
        parity += 1
    return dict(old_source_frame_compositions=comparisons, integer_ceiling_controls=parity)


def actual_fence_controls():
    patterns = feasible_roles = 0
    for bottom, gate_width, width, incident, far, gate_far in itertools.product(
            (14, 24), (12, 14, 16, 24), (6, 8, 12), (6, 8, 10, 14), (4, 6, 12), (4, 10)):
        fixed = sources(bottom, 4, 12, 8, 6)[:2]
        fixed.append(independent_source((gate_width, bottom, gate_far),
                                        (False, True, False), (bottom+3, 1)))
        target = independent_source((width, incident, far),
                                     (True, True, False), (bottom-6, incident+7))
        patterns += 1
        if target[0] & set.union(*(record[0] for record in fixed)):
            continue
        if width == 6:
            assert 4 <= far <= incident-6 and incident >= 10
        else:
            assert incident >= gate_width-4
        assert incident >= 8
        if gate_width >= 14:
            assert incident >= 10
        feasible_roles += 1
    return dict(parameter_patterns=patterns, endpoint_disjoint_partial_roles=feasible_roles,
                every_role_has_the_stated_B_fence_alternative=True)


def controls():
    north_east, first_rotors = axial_library({(-1, 0), (0, 1)})
    east, second_rotors = axial_library({(0, 1)})
    assert len(first_rotors) == 4 and len(second_rotors) == 2
    return dict(status='PASS', secondary=secondary_controls(north_east, first_rotors),
                positive=positive_controls(east, second_rotors), accounting=old_frame_controls(),
                actual_B_fence=actual_fence_controls(),
                U_dimensions_at_most=18, all_endpoint_anchors_examined=True,
                library_roles=dict(north_or_east=len(north_east), east_only=len(east)),
                scope='Finite controls of separate general proofs. Candidate sources are '
                      'PARTIAL, never complete marked-chain witnesses. Global reconstruction '
                      'and simultaneous target nonreuse use the written proof and explicit '
                      'old target dependencies. No unrestricted allocation/grid conclusion.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
