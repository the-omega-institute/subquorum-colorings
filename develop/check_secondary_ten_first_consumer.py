"""Finite controls for necessary first-consumer forms at secondary length ten."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def prescribed(bottom, width, far):
    return [independent_source((6, 8, 4), (True, True, True), (bottom+2, 11)),
            independent_source((width, 10, far), (False, False, False), (bottom-11, 5))]


def classify(record, bottom):
    point = bottom-5, 7
    own = set(neighbors(point)) & record[0]
    if (bottom-6, 7) in own:
        width = max(column for row, column in record[0])-6
        if len(own) == 1:
            far = max(row for row, column in record[0] if column == width+6)-(bottom-9)
            expected = independent_source((width, 4, far), (False, False, False), (bottom-9, 6))
            kind = 'north_terminal'
        else:
            far = bottom-5-min(row for row, column in record[0] if column == width+6)
            expected = independent_source((width, 4, far), (False, True, False), (bottom-5, 6))
            kind = 'outer_corner'
        incident = 4
    else:
        incident = max(column for row, column in record[0])-7
        outer = incident+7
        if max(row for row, column in record[0]) > bottom-5:
            width = max(row for row, column in record[0])-(bottom-6)
            far = outer-min(column for row, column in record[0] if row == bottom-6+width)
            expected = independent_source((width, incident, far), (True, True, False), (bottom-6, outer))
            kind = 'east_down'
        else:
            width = bottom-4-min(row for row, column in record[0])
            far = outer-min(column for row, column in record[0] if row == bottom-4-width)
            expected = independent_source((width, incident, far), (True, True, True), (bottom-4, outer))
            kind = 'east_up'
    assert record == expected
    assert width >= 6 and incident >= 4 and far >= 4
    assert width % 2 == incident % 2 == far % 2 == 0
    return kind, width, incident, far


def direct_counts(record, kind, width, incident, far):
    tiles = {(row//2, column//2) for row, column in record[0]}
    inside = {point for point in record[1] if (point[0]//2, point[1]//2) in tiles}
    legs = (incident+far)//2
    assert len(record[2]) == width-1+legs
    if kind == 'north_terminal':
        assert len(tiles) == width+legs and len(inside) == legs+2
        expected = 1-width
    elif kind == 'east_up':
        assert len(tiles) == width//2+legs and len(inside) == legs
        expected = -1
    else:
        assert len(tiles) == width//2+legs+1 and len(inside) == legs+4
        expected = 1
    assert charge(record) == expected


def main():
    library, rotors = axial_library({(-1, 0), (0, 1)})
    patterns = excluded = survivors = rotor_exclusions = corner_activations = 0
    counts = dict.fromkeys(('north_terminal', 'outer_corner', 'east_down', 'east_up'), 0)
    for bottom, width, far in itertools.product((16, 24), (6, 8, 12, 18, 24), (4, 6, 12)):
        fixed = prescribed(bottom, width, far)
        if fixed[0][0] & fixed[1][0]:
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
            kind, breadth, incident, other = classify(record, bottom)
            direct_counts(record, kind, breadth, incident, other)
            if kind == 'north_terminal':
                assert breadth <= width-2
            elif kind == 'outer_corner':
                assert other < 6 or breadth >= width
                assert far < 6 or (breadth <= width-2 and other == 4)
                terminal = bottom-9, 7
                assert terminal in record[0]
                assert {(bottom-10, 7), (bottom-9, 6)} <= record[1] & fixed[1][0]
                corner_activations += 1
            elif kind == 'east_down':
                assert incident >= 6 and (far < 6 or incident <= width-4)
            else:
                assert far == 4 and incident >= width
            counts[kind] += 1
            survivors += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
            rotor_exclusions += 1
        patterns += 1
    assert all(counts.values())
    partial_widths = (6, 8, 12, 24, 50, 100, 200)
    for breadth in partial_widths:
        fixed = prescribed(24, breadth+2, 4)
        record = independent_source((breadth, 4, 4), (False, False, False), (15, 6))
        assert all(not first[0] & second[0] for first, second in itertools.combinations(fixed+[record], 2))
        assert (19, 7) in record[0] and charge(record) == 1-breadth
        direct_counts(record, 'north_terminal', breadth, 4, 4)
    output = dict(status='PASS', scope='Necessary forms and local activation; no global allocation or complete stencil claimed',
                  disjoint_prescribed_patterns=patterns, excluded_fixed_intersections=excluded,
                  surviving_U_roles=survivors, roles_by_form=counts,
                  excluded_rotor_roles=rotor_exclusions, actual_corner_activation_controls=corner_activations,
                  partial_north_widths=list(partial_widths), complete_realizability='OPEN',
                  global_injection='OPEN', full_allocation_and_grid_equality='OPEN')
    print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
