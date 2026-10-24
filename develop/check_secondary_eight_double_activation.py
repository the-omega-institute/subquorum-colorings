"""Independent bounded controls for the secondary-eight double activation proof."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift, sources


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def east_terminal(bottom, level, width, incident, far):
    return independent_source((width, incident, far),
                              (True, True, False), (bottom-6-level, incident+7))


def fixed_pair(bottom, width, far):
    return [independent_source((6, 8, 4), (True, True, True), (bottom+2, 11)),
            independent_source((width, 8, far), (False, False, False), (bottom-9, 5))]


def disjoint(records):
    return all(not first[0] & second[0] for first, second in itertools.combinations(records, 2))


def frame(record, bottom, level):
    incident = max(column for row, column in record[0])-7
    width = max(row for row, column in record[0])-(bottom-6-level)
    far_row = bottom-6-level+width
    far = incident+7-min(column for row, column in record[0] if row == far_row)
    assert record == east_terminal(bottom, level, width, incident, far)
    return width, incident, far


def first_controls(library, rotors):
    patterns = excluded = survivors = 0
    for bottom, width, far in itertools.product((16, 24), (6, 8, 10, 14, 20), (4, 8)):
        fixed = fixed_pair(bottom, width, far)
        if not disjoint(fixed):
            excluded += 1
            continue
        blocked = fixed[0][0] | fixed[1][0]
        point = bottom-5, 7
        assert point in fixed[0][1] and point not in blocked
        assert set(neighbors(point)) & blocked == {(bottom-5, 6), (bottom-4, 7)}
        for relative in library:
            record = shift(relative, point)
            if record[0] & blocked:
                continue
            breadth, incident, other = frame(record, bottom, 0)
            assert 6 <= incident <= width-4 and charge(record) == 1
            assert (bottom-6, 7) in record[1] & fixed[1][1]
            assert (bottom-5, 6) in record[1] & fixed[1][0]
            assert breadth >= 6 and other >= 4
            survivors += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
        patterns += 1
    return dict(disjoint_patterns=patterns, excluded_fixed_intersections=excluded,
                surviving_E_roles=survivors, surviving_rotors=0)


def second_controls(library, rotors):
    patterns = excluded = survivors = 0
    for bottom, width, far, breadth, incident, other in itertools.product(
            (16, 24), (14, 20), (4, 8), (6, 8, 12), (6, 8, 10), (4, 6)):
        fixed = fixed_pair(bottom, width, far)
        fixed.append(east_terminal(bottom, 0, breadth, incident, other))
        if not disjoint(fixed):
            excluded += 1
            continue
        blocked = set.union(*(record[0] for record in fixed))
        point = bottom-6, 7
        assert point in fixed[1][1] & fixed[2][1] and point not in blocked
        assert set(neighbors(point)) & blocked == {(bottom-6, 6), (bottom-5, 7)}
        for relative in library:
            record = shift(relative, point)
            if record[0] & blocked:
                continue
            span, length, unused = frame(record, bottom, 1)
            assert incident+2 <= length <= width-4 and charge(record) == -1
            assert (bottom-7, 7) in record[1]
            assert unused >= 4
            survivors += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
        patterns += 1
    return dict(disjoint_patterns=patterns, excluded_fixed_intersections=excluded,
                surviving_negative_F_roles=survivors, surviving_rotors=0)


def third_controls(library, rotors):
    patterns = excluded = survivors = 0
    for bottom, width, breadth, incident, middle_width, gap, middle_far in itertools.product(
            (16, 24), (16, 22), (6, 8), (6, 8), (6, 10), (2, 4), (4, 6)):
        fixed = fixed_pair(bottom, width, 4)
        fixed.append(east_terminal(bottom, 0, breadth, incident, 4))
        fixed.append(east_terminal(bottom, 1, middle_width, incident+gap, middle_far))
        if not disjoint(fixed):
            excluded += 1
            continue
        blocked = set.union(*(record[0] for record in fixed))
        point = bottom-7, 7
        assert point in fixed[3][1] and point not in blocked
        assert set(neighbors(point)) & blocked == {
            (bottom-8, 7), (bottom-7, 6), (bottom-6, 7)}
        assert (bottom-5, 6) in fixed[2][1] & fixed[1][0]
        assert (bottom-6, 7) in fixed[2][1] & fixed[3][0]
        for relative in library:
            record = shift(relative, point)
            if record[0] & blocked:
                continue
            span, length, unused = frame(record, bottom, 2)
            assert incident+gap+2 <= length <= width-4 and charge(record) == 1
            assert (bottom-7, 6) in record[1] & fixed[1][0]
            assert (bottom-8, 7) in record[1] & fixed[1][0]
            assert span >= 6 and unused >= 4
            tile = {(row, column) for row in (bottom-8, bottom-7) for column in (6, 7)}
            assert tile-{point} <= fixed[1][0]
            survivors += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
        patterns += 1
    return dict(disjoint_patterns=patterns, excluded_fixed_intersections=excluded,
                surviving_positive_T_roles=survivors, surviving_rotors=0)


def ownership_and_ledger_controls():
    patterns = compositions = ceilings = 0
    for bottom, parent_incident in itertools.product((24, 40), (10, 12, 16)):
        fixed = sources(bottom, 4, 30, parent_incident, 4)
        current = fixed_pair(bottom, 22, 4)[1]
        last = east_terminal(bottom, 2, 8, 14, 4)
        assert (bottom-4, 4) in fixed[0][0] and (bottom-4, 5) in fixed[2][0]
        assert (bottom-8, 6) in current[0] and (bottom-7, 7) in last[0]
        assert (bottom-8, 5) in fixed[2][0] and (bottom-8, 6) in current[0]
        assert (bottom-7, 4) in fixed[0][0] and (bottom-7, 5) in fixed[2][0]
        assert (bottom-6, 4) in fixed[0][0] and (bottom-6, 5) in fixed[2][0]
        assert (bottom-10, 6) not in current[0] and (bottom-9, 6) in current[0]
        for incident, row, column in itertools.product((6, 10, 16), range(5), range(1, 8)):
            old = [(incident+3-row, 3-column), (column+2, row+2),
                   (column+2, incident+3-row), (incident+3-row, column+2)]
            maps = [lambda point: (bottom-3-point[1], point[0]+4),
                    lambda point: (bottom-8+point[0], incident+9-point[1]),
                    lambda point: (bottom-8+point[0], point[1]+4),
                    lambda point: (bottom-8+point[1], point[0]+4)]
            assert all(move(point) == (bottom-6+column, incident+7-row)
                       for move, point in zip(maps, old))
            tight_frame = lambda point: (bottom+1-point[1], point[0]+4)
            assert tight_frame((column+2, row+3)) == (bottom-2-row, column+6)
            compositions += 5
        patterns += 1
    for baseline, added in itertools.product(range(-40, 41), range(17)):
        assert (baseline+2*added+1)//2 == added+(baseline+1)//2
        ceilings += 1
    return dict(ownership_patterns=patterns, frame_compositions=compositions,
                exact_double_activation_ceiling_controls=ceilings)


def controls():
    boundary, boundary_rotors = axial_library({(-1, 0), (0, 1)})
    east, east_rotors = axial_library({(0, 1)})
    assert len(boundary_rotors) == 4 and len(east_rotors) == 2
    return dict(status='PASS', first=first_controls(boundary, boundary_rotors),
                second=second_controls(boundary, boundary_rotors),
                third=third_controls(east, east_rotors),
                accounting=ownership_and_ledger_controls(),
                U_dimensions_bounded_by=18, every_bounded_endpoint_anchor_examined=True,
                scope='Finite controls of arbitrary-dimension written proofs, not a general '
                      'proof or complete actual marked-chain realization. Each stage starts '
                      'from disjoint PARTIAL original sources. Global injection uses the '
                      'specified actual-chain and accepted catalogue adapters. Full grid OPEN.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
