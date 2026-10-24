"""Independent controls for tight secondary-ten target nonreuse and accounting."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from rotor_networks import affine


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def endpoint_square_vertices(endpoints):
    result = set()
    for row, column in endpoints:
        square = {(row, column), (row+1, column),
                  (row, column+1), (row+1, column+1)}
        if square <= endpoints:
            result |= square
    return result


def square_depth_controls():
    patterns = 0
    for width, near, far, symmetry, offset in itertools.product(
            (6, 8, 20), (6, 10, 30), (4, 8, 20),
            itertools.product((False, True), repeat=3), ((0, 0), (-13, 22))):
        endpoints = independent_source((width, near, far), symmetry, offset)[0]
        intrinsic_bar = {affine((row, column), symmetry, offset)
                         for row in (0, 1) for column in range(1, width+1)}
        square_bar = endpoint_square_vertices(endpoints)
        assert square_bar == intrinsic_bar
        depth_four = affine((4, 1), symmetry, offset)
        depth_five = affine((5, 1), symmetry, offset)
        distance = lambda point: min(max(abs(point[0]-site[0]), abs(point[1]-site[1]))
                                     for site in square_bar)
        assert distance(depth_four) == 3 and distance(depth_five) == 4
        patterns += 1
    return dict(original_U_patterns_all_eight_isometries=patterns,
                square_vertices_exactly_original_bar=True,
                depth_four_and_five_intrinsically_distinct=True)


def prescribed(bottom, parent, parent_width, width, breadth, successor_width):
    specs = [
        ((bottom-2, 4, 6), (True, False, False), (2, 3)),
        ((6, 8, 4), (True, True, True), (bottom+2, 11)),
        ((parent_width, parent, 4), (False, False, False), (bottom-1-parent, 4)),
        ((width, 10, 4), (False, False, False), (bottom-11, 5)),
        ((successor_width, width+2, 4), (True, True, True), (bottom-4, width+9)),
        ((breadth, width, 4), (True, True, True), (bottom-5, width+7)),
    ]
    return [independent_source(*spec) for spec in specs]


def ownership_controls():
    disjoint = excluded = compositions = 0
    parents = {}
    for parent, width, breadth, successor_width in itertools.product(
            (12, 14, 16, 20, 30), (6, 10, 20), (8, 10, 12), (10, 12, 14)):
        for parent_width in range(6, width+16, 2):
            bottom = parent+8
            records = prescribed(bottom, parent, parent_width, width, breadth, successor_width)
            if any(first[0] & second[0] for first, second in itertools.combinations(records, 2)):
                excluded += 1
                continue
            original_x, original_q, original_h, original_d, original_e, target = records
            assert parent >= 16
            parents[parent] = parents.get(parent, 0)+1
            axial, lateral, terminal = (bottom-6, 6), (bottom-5, 7), (bottom-6, 7)
            assert terminal in target[0] and {axial, lateral} <= target[1]
            assert axial in original_d[0] and lateral in original_e[0]
            assert charge(target) == 1
            assert set(neighbors(axial)) & original_d[0] == {(bottom-7, 6), (bottom-5, 6)}
            tile = {(row, column) for row in (bottom-6, bottom-5) for column in (6, 7)}
            assert tile-{terminal} <= original_d[0] | original_e[0]
            assert (bottom-1, 5) not in original_x[0]
            assert (bottom-1, 6) not in original_h[0]
            owner_pairs = [
                ((bottom-7, 4), original_x, (bottom-7, 5), original_h),
                ((bottom-3, 6), original_d, (bottom-4, 7), original_q),
                ((bottom-3, 5), original_h, (bottom-3, 6), original_d),
                ((bottom-4, 4), original_x, (bottom-4, 5), original_h),
            ]
            for first_point, first_owner, second_point, second_owner in owner_pairs:
                assert first_point in first_owner[0] and second_point in second_owner[0]
                assert first_owner is not second_owner and not first_owner[0] & second_owner[0]
            disjoint += 1
    for bottom, width, row, column in itertools.product((18, 24, 40), (6, 10, 20), range(6), range(1, 9)):
        old = [(width+3-row, 3-column), (column+2, row+2),
               (column+2, width+3-row), (width+3-row, column+2)]
        maps = [lambda point: (bottom-8+point[1], point[0]+4),
                lambda point: (bottom-3-point[0], width+9-point[1]),
                lambda point: (bottom-3-point[0], point[1]+4),
                lambda point: (bottom-3-point[1], point[0]+4)]
        assert all(move(point) == (bottom-5-column, width+7-row)
                   for move, point in zip(maps, old))
        compositions += 4
    assert disjoint and 16 in parents
    return dict(disjoint_six_source_partial_patterns=disjoint,
                excluded_fixed_intersections=excluded, surviving_parent_lengths=parents,
                frame_compositions=compositions,
                all_four_two_owner_witness_pairs_checked=True,
                both_support_consumers_and_full_terminal_tile_checked=True)


def parent_obstruction_controls():
    patterns = 0
    for parent, width, parent_width, breadth, successor_width, far in itertools.product(
            (12, 14), (6, 10, 20, 50), range(6, 64, 2), (8, 10, 20), (10, 12, 30), (4, 8, 20)):
        bottom = parent+8
        original_h = independent_source((parent_width, parent, far),
                                        (False, False, False), (bottom-1-parent, 4))[0]
        original_d = independent_source((width, 10, 4), (False, False, False), (bottom-11, 5))[0]
        original_e = independent_source((successor_width, width+2, 4),
                                        (True, True, True), (bottom-4, width+9))[0]
        target = independent_source((breadth, width, 4),
                                    (True, True, True), (bottom-5, width+7))[0]
        if parent_width <= width:
            assert (bottom-11, parent_width+4) in original_h & original_d
        elif parent == 12 or parent_width == width+2:
            assert (bottom-13, width+6) in original_h & target
        else:
            assert parent_width >= width+4 and parent == 14
            assert (bottom-14, width+8) in original_h & original_e
        patterns += 1
    return dict(parent_twelve_and_fourteen_collision_controls=patterns,
                all_dimensions_unbounded_in_written_proof=True)


def ledger_controls():
    ceiling_patterns = inventory_patterns = 0
    for baseline, added in itertools.product(range(-40, 41), range(21)):
        gain = (baseline+added+1)//2-(baseline+1)//2
        assert gain in {added//2, (added+1)//2}
        assert (baseline+added+3)//2-(baseline+added+1)//2 == 1
        ceiling_patterns += 1
    for old_claims, residual, caps, resolved, extra, m8, unmarked, upper in itertools.product(
            (0, 1, 5), range(9), (0, 2), (0, 2), (0, 2), (0, 3), (0, 1), (0, 1)):
        pairs = resolved+1
        total = old_claims+caps+resolved+residual
        positive_count = (total+1)//2+unmarked
        for added in range(residual+1):
            reserve = (old_claims+added+extra+m8+caps+2*pairs+2*upper+1)//2
            bound = unmarked+upper+pairs+(m8-resolved-residual+extra+added+1)//2
            margin = positive_count+reserve-total
            assert margin >= bound
            if resolved+residual <= 2*unmarked+2*upper+2*pairs+m8+extra+added+1:
                assert margin >= 0
            inventory_patterns += 1
    return dict(exact_ceiling_and_parity_controls=ceiling_patterns,
                same_inventory_bound_and_threshold_controls=inventory_patterns)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', intrinsic_depth=square_depth_controls(),
        ownership=ownership_controls(), parent_obstructions=parent_obstruction_controls(),
        ledger=ledger_controls(), scope='Finite validation of separately written unbounded '
        'source-reconstruction and joint-nonreuse proofs. Six-source stencils are PARTIAL; '
        'no complete actual marked-chain realization or full allocation/grid equality claimed.'), indent=2))
