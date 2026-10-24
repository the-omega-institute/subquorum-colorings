"""Controls for the first downward activation without a far-leg fence."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_tight_transfer import ledger_controls, square_depth_controls


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def local_controls(library, rotors):
    patterns = upward = downward = empty = rotor_exclusions = 0
    for bottom, width, incident, breadth in itertools.product(
            (20, 38), (6, 10, 24), (6, 10, 20), (8, 10)):
        fixed = [independent_source((6, 8, 4), (True, True, True), (bottom+2, 11)),
                 independent_source((width, 10, 4), (False, False, False), (bottom-11, 5)),
                 independent_source((breadth, incident, 4),
                                    (True, True, False), (bottom-6, incident+7))]
        assert all(not first[0] & second[0] for first, second in itertools.combinations(fixed, 2))
        point = bottom-6, 7
        blocked = set.union(*(record[0] for record in fixed))
        assert point in fixed[2][1] and point not in blocked
        assert set(neighbors(point)) & blocked == {(bottom-6, 6), (bottom-5, 7)}
        count = 0
        for relative in library:
            current = shift(relative, point)
            if current[0] & blocked:
                continue
            outer = max(column for row, column in current[0])
            near = outer-7
            low = min(row for row, column in current[0])
            high = max(row for row, column in current[0])
            if low == point[0]:
                extent = high-(bottom-7)
                other = outer-min(column for row, column in current[0] if row == high)
                expected = independent_source((extent, near, other),
                                              (True, True, False), (bottom-7, outer))
                assert current == expected and charge(current) == -1
                downward += 1
            else:
                assert high == point[0]
                extent = bottom-5-low
                other = outer-min(column for row, column in current[0] if row == low)
                expected = independent_source((extent, near, other),
                                              (True, True, True), (bottom-5, outer))
                assert current == expected and charge(current) == 1
                upward += 1
            count += 1
        if not count:
            empty += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
            rotor_exclusions += 1
        patterns += 1
    assert upward and downward
    return dict(three_source_patterns=patterns, surviving_upward_U_roles=upward,
                surviving_downward_U_roles=downward,
                no_bounded_survivor_not_an_impossibility_claim=empty,
                rotor_exclusions=rotor_exclusions, bounded_U_dimensions_max=18,
                all_survivors_are_east_terminals=True)


def ownership_controls():
    patterns = compositions = 0
    for parent, width, incident in itertools.product((12, 20, 30), (6, 10, 24), (6, 8, 10, 20)):
        bottom = parent+8
        following_incident = max(width, incident)+4
        original_q = independent_source((6, 8, 4), (True, True, True), (bottom+2, 11))
        original_d = independent_source((width, 10, 4), (False, False, False), (bottom-11, 5))
        target = independent_source((10, incident, 4), (True, True, False), (bottom-6, incident+7))
        following = independent_source((6, following_incident, 4),
                                       (True, True, True), (bottom-5, following_incident+7))
        original_x = independent_source((bottom-2, 4, 6), (True, False, False), (2, 3))
        original_h = independent_source((following_incident+20, parent, 4),
                                        (False, False, False), (bottom-1-parent, 4))
        records = [original_q, original_d, target, following, original_x, original_h]
        assert all(not first[0] & second[0] for first, second in itertools.combinations(records, 2))
        terminal = bottom-5, 7
        axial, lateral = (bottom-5, 6), (bottom-6, 7)
        assert terminal in target[0] and {axial, lateral} <= target[1]
        assert axial in original_d[0] and lateral in following[0]
        assert charge(target) == charge(following) == 1
        tile = {(row, column) for row in (bottom-6, bottom-5) for column in (6, 7)}
        assert tile <= original_d[0] | target[0] | following[0]
        assert (bottom-7, 7) not in set.union(*(record[0] for record in records))
        frames = [lambda point: (bottom-3-point[1], point[0]+4),
                  lambda point: (bottom-8+point[0], incident+9-point[1]),
                  lambda point: (bottom-8+point[0], point[1]+4),
                  lambda point: (bottom-8+point[1], point[0]+4)]
        old_charts = [lambda point: (incident+3-point[0], 3-point[1]),
                      lambda point: (point[1]+2, point[0]+2),
                      lambda point: (point[1]+2, incident+3-point[0]),
                      lambda point: (incident+3-point[0], point[1]+2)]
        new_chart = lambda point: (bottom-6+point[1], incident+7-point[0])
        for frame, old_chart in zip(frames, old_charts):
            for point in ((0, 1), (1, 1), (4, 8), (12, 18)):
                assert frame(old_chart(point)) == new_chart(point)
            compositions += 1
        witnesses = [((bottom-4, 4), original_x, (bottom-4, 5), original_h),
                     ((bottom-8, 6), original_d, (bottom-8, 5), original_h),
                     ((bottom-7, 4), original_x, (bottom-7, 5), original_h)]
        for first, first_owner, second, second_owner in witnesses:
            assert first in first_owner[0] and second in second_owner[0]
            assert first_owner is not second_owner
        assert frames[1]((0, incident+3)) == (bottom-8, 6)
        assert frames[1]((0, incident+4)) == (bottom-8, 5)
        assert (bottom-1, 6) in original_d[0] and (bottom-1, 6) not in original_h[0]
        patterns += 1
    return dict(six_source_partial_upward_bend_patterns=patterns,
                all_four_old_frame_compositions=compositions,
                new_old_P_witnesses_do_not_use_E2=True,
                third_downward_terminal_absent_in_all_patterns=True,
                complete_actual_marked_chain_realization=False)


if __name__ == '__main__':
    library, rotors = axial_library({(-1, 0), (0, 1)})
    print(json.dumps(dict(status='PASS', local=local_controls(library, rotors),
                          ownership=ownership_controls(),
                          depth=square_depth_controls(), ledger=ledger_controls(),
                          scope='Finite checks of a separately written general proof. '
                          'Partial upward bends do not assert complete realizability, '
                          'a global counterexample, or a second new activation.'), indent=2))
