"""Independent source controls for secondary-ten outer-corner transfer."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_tight_transfer import endpoint_square_vertices, ledger_controls
from rotor_networks import affine


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def ownership_controls():
    accepted = excluded = compositions = longer_far = 0
    for parent, width, corner_width, far, corner_far in itertools.product(
            (12, 14, 20, 30), (6, 10, 24), (6, 8, 10, 24, 30),
            (4, 6, 20), (4, 6, 12)):
        bottom = parent+8
        original_x = independent_source((bottom-2, 4, 6), (True, False, False), (2, 3))
        original_q = independent_source((6, 8, 4), (True, True, True), (bottom+2, 11))
        original_h = independent_source((max(width, corner_width)+8, parent, 4),
                                        (False, False, False), (bottom-1-parent, 4))
        original_d = independent_source((width, 10, far), (False, False, False), (bottom-11, 5))
        target = independent_source((corner_width, 4, corner_far),
                                    (False, True, False), (bottom-5, 6))
        records = [original_x, original_q, original_h, original_d, target]
        if any(first[0] & second[0] for first, second in itertools.combinations(records, 2)):
            excluded += 1
            continue
        accepted += 1
        if corner_far >= 6:
            assert far == 4 and corner_width >= width
            longer_far += 1
        if far >= 6:
            assert corner_far == 4 and corner_width <= width-2
        corner, terminal = (bottom-5, 7), (bottom-9, 7)
        axial, lateral = (bottom-10, 7), (bottom-9, 6)
        assert corner in original_q[1] & target[0]
        assert terminal in target[0] and {axial, lateral} <= target[1] & original_d[0]
        assert charge(target) == 1
        assert set(neighbors(axial)) & original_d[0] == {
            (bottom-11, 7), (bottom-10, 6), (bottom-10, 8)}
        assert set(neighbors(lateral)) & original_d[0] == {
            (bottom-10, 6), (bottom-8, 6)}
        tile = {(row, column) for row in (bottom-10, bottom-9) for column in (6, 7)}
        assert tile <= original_d[0] | target[0]
        assert (bottom-11, 8) in original_d[0]
        assert (bottom-12, 8) not in original_d[0]
        assert (bottom-10, 4) in original_x[0]
        assert (bottom-10, 5) in original_h[0]
        assert (bottom-1, 5) in original_h[0] and (bottom-1, 5) not in original_x[0]
        new_chart = lambda point: (bottom-5-point[0], point[1]+6)
        old_s = lambda point: (7-point[0], 3-point[1])
        old_p = lambda point: (point[1]+2, point[0]+2)
        frame_s = lambda point: (bottom-12+point[0], 9-point[1])
        frame_p = lambda point: (bottom-3-point[1], point[0]+4)
        for point in ((0, 1), (1, 1), (4, 1), (2, 6), (14, 20)):
            assert frame_s(old_s(point)) == new_chart(point)
            assert frame_p(old_p(point)) == new_chart(point)
        assert frame_s((1, 1)) == (bottom-11, 8)
        assert frame_s((0, 1)) == (bottom-12, 8)
        assert frame_p((0, 7)) == (bottom-10, 4)
        assert frame_p((1, 7)) == (bottom-10, 5)
        compositions += 2
    assert accepted and longer_far
    return dict(disjoint_five_source_partial_stencils=accepted,
                intersecting_stencils_excluded=excluded,
                legal_corner_far_ge_six_patterns=longer_far,
                all_frame_compositions=compositions,
                same_owner_ordered_degree_three_two_and_full_tiles_checked=True,
                complete_actual_marked_chain_realization=False)


def intrinsic_controls():
    patterns = 0
    for width, far, symmetry in itertools.product(
            (6, 12, 30), (4, 10, 30), itertools.product((False, True), repeat=3)):
        original = independent_source((width, 4, far), symmetry, (-16, 13))[0]
        original_d = independent_source((width, 10, far), symmetry, (-16, 13))[0]
        axial = affine((1, 2), symmetry, (-16, 13))
        lateral = affine((2, 1), symmetry, (-16, 13))
        common = set(neighbors(axial)) & set(neighbors(lateral)) & original_d
        assert common == {affine((1, 1), symmetry, (-16, 13))}
        assert len(set(neighbors(axial)) & original_d) == 3
        assert len(set(neighbors(lateral)) & original_d) == 2
        intrinsic_bar = endpoint_square_vertices(original)
        terminal = affine((4, 1), symmetry, (-16, 13))
        distance = min(max(abs(terminal[0]-point[0]), abs(terminal[1]-point[1]))
                       for point in intrinsic_bar)
        assert distance == 3
        for old_incident in (8, 10, 20):
            old = independent_source((width, old_incident, far), symmetry, (-16, 13))[0]
            old_bar = endpoint_square_vertices(old)
            old_terminal = affine((old_incident, 1), symmetry, (-16, 13))
            old_distance = min(max(abs(old_terminal[0]-point[0]), abs(old_terminal[1]-point[1]))
                               for point in old_bar)
            assert old_distance == old_incident-1 and old_distance != distance
        patterns += 1
    return dict(all_eight_isometry_patterns=patterns,
                original_bar_end_common_neighbor_unique=True,
                recipient_terminal_distance_separates_all_tested_old_upward_lengths=True)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', ownership=ownership_controls(),
                          intrinsic=intrinsic_controls(), ledger=ledger_controls(),
                          scope='Independent finite validation of general written arguments; '
                          'no full marked-chain realization, catalogue proof by enumeration '
                          'or full global Lean formalization.'), indent=2))
