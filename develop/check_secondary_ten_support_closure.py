"""Finite controls for general secondary-ten support closure theorems."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_first_consumer import prescribed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def north_controls():
    library, rotors = axial_library({(-1, 0), (0, -1)})
    patterns = rotor_exclusions = 0
    for bottom, far in itertools.product((-24, 0, 24, 100), (4, 6, 12, 40, 200)):
        returning = independent_source((6, 8, 4), (True, True, True), (bottom+2, 11))
        northern = independent_source((6, 4, far), (False, False, False), (bottom-9, 6))
        assert not returning[0] & northern[0]
        point = bottom-5, 11
        blocked = returning[0] | northern[0]
        assert point in returning[1] and point not in blocked
        assert set(neighbors(point)) & blocked == {(bottom-4, 11), (bottom-5, 12)}
        assert (bottom-8, 11) in northern[0] and (bottom-5, 7) in northern[0]
        for record in library:
            assert shift(record, point)[0] & blocked
        for record in rotors:
            assert shift(record, point)[0] & blocked
            rotor_exclusions += 1
        patterns += 1
    return dict(patterns=patterns, surviving_U_roles=0, surviving_rotor_roles=0,
                excluded_rotor_roles=rotor_exclusions, source_far_lengths=[4, 6, 12, 40, 200])


def window_controls():
    library, rotors = axial_library({(0, -1), (0, 1)})
    patterns = excluded = surviving = positive = negative = tight = empty = rotor_exclusions = 0
    for bottom, width, gap, breadth, far in itertools.product(
            (24, 40), (6, 8, 12, 18), (0, 2, 4, 6, 8), (6, 8, 10, 14), (4, 6, 12)):
        incident = width+gap
        fixed = prescribed(bottom, width, 4)
        fixed.append(independent_source((breadth, incident, far),
                                        (True, True, True), (bottom-4, incident+7)))
        if any(first[0] & second[0] for first, second in itertools.combinations(fixed, 2)):
            excluded += 1
            continue
        point = bottom-6, width+5
        blocked = set.union(*(record[0] for record in fixed))
        assert point in fixed[1][1] and point not in blocked
        assert (bottom-7, width+5) in fixed[1][0]
        assert (bottom-5, width+5) in fixed[2][0]
        local_survivors = 0
        for relative in library:
            record = shift(relative, point)
            if record[0] & blocked:
                continue
            bar = max(column for row, column in record[0])
            span = bottom-5-min(row for row, column in record[0])
            near = bar-min(column for row, column in record[0] if row == bottom-6)
            other = bar-min(column for row, column in record[0] if row == bottom-5-span)
            expected = independent_source((span, near, other), (True, True, True), (bottom-5, bar))
            assert record == expected
            assert width+7 <= bar <= incident+5
            assert 4 <= near <= bar-7 and bar-width-5 <= near
            assert min(span, other) >= 4 and span >= 6
            if bar % 2:
                assert charge(record) == 1
                terminal = bottom-6, bar-near
                assert terminal in record[0]
                assert (bottom-5, bar-near) in record[1] & fixed[2][0]
                positive += 1
            else:
                assert charge(record) == 1-span
                if gap == 4:
                    assert bar == width+8 and span >= 8 and breadth >= 10
                negative += 1
            if incident+7-bar <= far:
                assert span <= breadth-2
            if gap == 2:
                assert bar == width+7 and 8 <= span <= breadth-2 and near <= width
                assert breadth >= 10
                tight += 1
            surviving += 1
            local_survivors += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
            rotor_exclusions += 1
        if gap == 0:
            assert local_survivors == 0
            empty += 1
        patterns += 1
    assert positive and negative and tight and empty
    return dict(disjoint_prescribed_patterns=patterns, excluded_fixed_intersections=excluded,
                surviving_U_roles=surviving, positive_activated_successors=positive,
                negative_successors=negative, tight_gap_positive_controls=tight,
                zero_gap_noncompletion_controls=empty, surviving_rotor_roles=0,
                excluded_rotor_roles=rotor_exclusions,
                bounded_U_dimensions_max=18, all_horizontal_straight_interiors_included=True)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', north=north_controls(), window=window_controls(),
        scope='Finite controls for separately written arbitrary-dimension proofs. '
              'Partial source stencils are not asserted complete. New local activations '
              'have no global nonreuse proof or ledger increment. Full allocation/grid OPEN.'), indent=2))
