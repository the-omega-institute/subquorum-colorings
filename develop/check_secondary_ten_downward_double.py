"""Independent controls for downward secondary-ten double activation."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_tight_transfer import endpoint_square_vertices
from rotor_networks import affine


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def chain(bottom, width, far, gap):
    fixed = [independent_source((6, 8, 4), (True, True, True), (bottom+2, 11)),
             independent_source((width, 10, far), (False, False, False), (bottom-11, 5))]
    for level in range(5):
        fixed.append(independent_source((10+2*level, gap+2*level, 4),
                                       (True, True, False),
                                       (bottom-6-level, gap+2*level+7)))
    return fixed


def local_controls(library, rotors):
    patterns = survivors = rotor_exclusions = 0
    for bottom, width, far, gap in itertools.product(
            (20, 38), (24, 40), (6, 20), (6, 8, 10)):
        records = chain(bottom, width, far, gap)
        assert all(not first[0] & second[0]
                   for first, second in itertools.combinations(records, 2))
        for level in range(1, 5):
            fixed = records[:level+2]
            point = bottom-5-level, 7
            blocked = set.union(*(record[0] for record in fixed))
            assert point in fixed[-1][1] and point not in blocked
            assert {(point[0], 6), (point[0]+1, 7)} <= blocked
            count = 0
            for relative in library:
                current = shift(relative, point)
                if current[0] & blocked:
                    continue
                outer = max(column for row, column in current[0])
                incident = outer-7
                breadth = max(row for row, column in current[0])-(bottom-6-level)
                other = outer-min(column for row, column in current[0]
                                  if row == bottom-6-level+breadth)
                expected = independent_source((breadth, incident, other),
                                              (True, True, False),
                                              (bottom-6-level, outer))
                assert current == expected
                assert gap+2*level <= incident <= width-4
                assert charge(current) == (1 if level % 2 == 0 else -1)
                count += 1
            assert count
            survivors += count
            for relative in rotors:
                assert shift(relative, point)[0] & blocked
                rotor_exclusions += 1
            patterns += 1
        for level in (0, 2, 4):
            point = bottom-5-level, 7
            target = records[level+2]
            axial, lateral = (point[0], 6), (point[0]-1, 7)
            assert {axial, lateral} <= target[1] and charge(target) == 1
            assert axial in records[1][0]
            assert lateral in (records[level+3][0] if level < 4 else records[1][0])
        for level in (0, 4):
            point = bottom-5-level, 7
            tile = {(row, column) for row in (point[0]-1, point[0]) for column in (6, 7)}
            assert tile <= set.union(*(record[0] for record in records))
            axial = point[0], 6
            assert set(neighbors(axial)) & records[1][0] == {
                (axial[0]-1, 6), (axial[0]+1, 6)}
    return dict(stage_patterns=patterns, surviving_bounded_U_roles=survivors,
                rotor_exclusions=rotor_exclusions,
                bounded_role_dimension_max=18,
                all_survivors_have_the_stated_frame=True,
                first_last_tiles_full_and_support_profiles_checked=True)


def frame_controls():
    accepted = excluded = compositions = 0
    for parent, width, far, gap in itertools.product(
            (12, 14, 20), (24, 40, 60), (6, 8, 20), (6, 8, 10)):
        bottom = parent+8
        original_q, original_d, *east = chain(bottom, width, far, gap)
        original_x = independent_source((bottom-2, 4, 6), (True, False, False), (2, 3))
        original_h = independent_source((width+4, parent, 4),
                                        (False, False, False), (bottom-1-parent, 4))
        records = [original_q, original_d, original_x, original_h, *east]
        if any(first[0] & second[0] for first, second in itertools.combinations(records, 2)):
            excluded += 1
            continue
        accepted += 1
        witnesses = [
            ((bottom-4, 4), original_x, (bottom-4, 5), original_h),
            ((bottom-8, 6), original_d, (bottom-7, 7), east[2]),
            ((bottom-8, 5), original_h, (bottom-8, 6), original_d),
            ((bottom-7, 4), original_x, (bottom-7, 5), original_h),
            ((bottom-8, 4), original_x, (bottom-8, 5), original_h),
        ]
        for first, first_owner, second, second_owner in witnesses:
            assert first in first_owner[0] and second in second_owner[0]
            assert first_owner is not second_owner
        assert (bottom-12, 6) not in original_d[0]
        assert (bottom-11, 6) in original_d[0]
        for level in (0, 4):
            incident = gap+2*level
            target = lambda point: (bottom-6-level+point[1], incident+7-point[0])
            old_charts = [lambda point: (incident+3-point[0], 3-point[1]),
                          lambda point: (point[1]+2, point[0]+2),
                          lambda point: (point[1]+2, incident+3-point[0]),
                          lambda point: (incident+3-point[0], point[1]+2)]
            frames = [lambda point: (bottom-3-level-point[1], point[0]+4),
                      lambda point: (bottom-8-level+point[0], incident+9-point[1]),
                      lambda point: (bottom-8-level+point[0], point[1]+4),
                      lambda point: (bottom-8-level+point[1], point[0]+4)]
            for frame, chart in zip(frames, old_charts):
                for point in ((0, 1), (1, 1), (3, 7), (12, 18)):
                    assert frame(chart(point)) == target(point)
                compositions += 1
        incident = gap+8
        old_recipient = lambda point: (incident+3-point[0], 11-point[1])
        old_producer = lambda point: (bottom+1-point[1], point[0]+4)
        for point in ((0, 1), (1, 1), (3, 7), (12, 18)):
            assert old_producer(old_recipient(point)) == (bottom-10+point[1], incident+7-point[0])
        for old_near in (4, 6):
            old_x = independent_source((12, old_near, 6), (False, False, False), (0, 0))[0]
            for depth in (3, 4):
                assert (depth, 1) in old_x
                old_x_point = 3, depth+3
                assert old_producer(old_x_point) == (bottom-2-depth, 7)
                assert (bottom-2-depth, 7) in east[depth-3][0]
    assert accepted
    return dict(nine_source_partial_stencils=accepted,
                intersecting_prescribed_stencils_excluded=excluded,
                old_frame_compositions=compositions,
                both_equal_length_old_Vcorner_obstructions_checked=True,
                complete_marked_chain_realization=False)


def invariant_controls():
    patterns = 0
    for width, far, symmetry in itertools.product(
            (6, 20, 40), (4, 10, 20), itertools.product((False, True), repeat=3)):
        original = independent_source((width, 10, far), symmetry, (-11, 16))[0]
        intrinsic_bar = endpoint_square_vertices(original)
        for depth in (2, 4, 5, 6):
            point = affine((depth, 1), symmetry, (-11, 16))
            distance = min(max(abs(point[0]-site[0]), abs(point[1]-site[1]))
                           for site in intrinsic_bar)
            assert distance == depth-1
        patterns += 1
    return dict(all_isometry_and_equal_leg_patterns=patterns,
                original_bar_distances_one_three_four_five_distinct=True)


def ledger_controls():
    inventories = parity = 0
    for base, added in itertools.product(range(-50, 51), range(21)):
        assert (base+2*added+1)//2-(base+1)//2 == added
        parity += 1
    for old, residual, caps, resolved, extra, marked, unmarked, upper in itertools.product(
            (0, 1, 5), range(9), (0, 2), (0, 2), (0, 2), (0, 3), (0, 1), (0, 1)):
        pairs = resolved+1
        total = old+caps+resolved+residual
        positive = (total+1)//2+unmarked
        for added in range(residual+1):
            reserve = (old+2*added+extra+marked+caps+2*pairs+2*upper+1)//2
            margin = positive+reserve-total
            bound = unmarked+upper+pairs+added+(marked-resolved-residual+extra+1)//2
            assert margin >= bound
            threshold = 2*unmarked+2*upper+2*pairs+marked+extra+2*added+1
            if resolved+residual <= threshold:
                assert margin >= 0
            inventories += 1
    return dict(same_inventory_cases=inventories, exact_gain_parity_cases=parity,
                exact_gain_one_per_claim=True)


if __name__ == '__main__':
    library, rotors = axial_library({(-1, 0), (0, 1)})
    print(json.dumps(dict(status='PASS', local=local_controls(library, rotors),
                          old_frames=frame_controls(), intrinsic=invariant_controls(),
                          ledger=ledger_controls(),
                          scope='Finite independent controls only; general forcing, '
                          'actual labelled reconstruction and global nonreuse are written proofs.'), indent=2))
