"""Exact shape and interval controls for the general six-row rotor exclusion."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_even_bar_contact_ledger import rotor_record
from check_even_gap_axial_compensation import transform
from check_six_row_ceiling_descent import anchored
from check_six_row_transverse_budget import transverse


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def normalized(reflected, top=0, left=0):
    record = rotor_record((False, False, reflected))
    minimum_row = min(row for row, column in record[0])
    minimum_column = min(column for row, column in record[0])
    return transform(record, lambda point: (
        point[0]-minimum_row+top, point[1]-minimum_column+left))


def shape_roles():
    base = normalized(False)
    corner_roles = upper_roles = middle_roles = 0
    for point, reflected in itertools.product(((0, 0), (0, 2), (0, 3)), (False, True)):
        for record in anchored(normalized(reflected), point):
            if not all(0 <= row <= 5 for row, column in record[0]):
                continue
            assert record[0] & base[0]
            corner_roles += 1
    survivors = []
    for reflected, column in itertools.product((False, True), range(1, 4)):
        left = column-(2 if reflected else 1)
        record = normalized(reflected, 2, left)
        upper_support = 1, column
        assert upper_support in record[1] and upper_support in base[0]
        if not record[0] & base[0]:
            assert not reflected and left == 2
            assert {point for point in record[0] if point[0] == 5} == {(5, 4)}
            survivors.append((reflected, left))
        upper_roles += 1
    assert survivors == [(False, 2)]
    for reflected, side, other_reflected in itertools.product((False, True), (0, 3), (False, True)):
        current = normalized(reflected, 1)
        point = 1, side
        assert point in current[1]
        for record in anchored(normalized(other_reflected), point):
            if min(row for row, column in record[0]) != 1:
                continue
            assert current[0] & record[0]
            middle_roles += 1
    for reflected, top in itertools.product((False, True), range(3)):
        record = normalized(reflected, top)
        for point in record[0]:
            if point[0] == top:
                assert (top+1, point[1]) in record[0]
        if top == 2:
            point = 1, 2 if reflected else 1
            assert point in record[1] and (2, point[1]) in record[0]
    return dict(boundary_anchor_roles=corner_roles, lower_upper_support_roles=upper_roles,
                lower_survivors=survivors, middle_corner_roles=middle_roles)


def top_gap_controls():
    base = normalized(False)
    checked = wrong_tip = 0
    for first_depth, second_depth, bottom_left, bottom_right in itertools.product(
            (4, 6, 10, 20), (4, 6, 10, 20), (4, 6, 10, 20), (4, 6, 10, 20)):
        left = transverse(-first_depth, 1, bottom_left, first_depth)
        right = transverse(second_depth+1, -1, bottom_right, second_depth)
        records = [base, left, right]
        if any(first[0] & second[0] for first, second in itertools.combinations(records, 2)):
            continue
        blocked = set.union(*(record[0] for record in records))
        gap = range(2-first_depth, second_depth+1)
        assert all((0, column) in blocked for column in gap)
        left_tip, right_tip = -first_depth+bottom_left, second_depth+2-bottom_right
        assert left_tip % 2 == right_tip % 2 == 0 and left_tip+1 < right_tip
        point = 5, left_tip+1
        assert point in left[1] and point not in blocked and point != (5, 4)
        assert (5, left_tip) in blocked
        for reflected, column in itertools.product((False, True), range(1, 4)):
            candidate = normalized(reflected, 2, column-(2 if reflected else 1))
            upper_support = 1, column
            if not candidate[0] & blocked and upper_support in base[0]:
                assert candidate == normalized(False, 2, 2)
        checked += 1
    for first_depth, second_depth in itertools.product((4, 6, 20, 2000), repeat=2):
        left = transverse(-first_depth, 1, 4, first_depth)
        right = transverse(second_depth+2, -1, 4, second_depth)
        assert not left[0] & base[0] and not right[0] & base[0]
        assert (0, 2) in right[1] and {(0, 1), (0, 3)} <= base[0] | right[0]
        assert (0, 2) not in left[0] | base[0] | right[0]
        wrong_tip += 1
    return dict(closed_top_gap_pairs=checked, forbidden_right_tip_controls=wrong_tip,
                largest_top_depth=2000)


def middle_stem_controls():
    checked = 0
    for reflected, depth, from_left, tip_extra in itertools.product(
            (False, True), (4, 6, 20, 2000), (False, True), (0, 2, 8)):
        current = normalized(reflected, 1)
        anchor = 2 if reflected else 1
        if from_left:
            tip = anchor+tip_extra
            bar = tip-depth
            if bar+1 >= 0:
                continue
            vertical = transverse(bar, 1, 4, depth)
            point = 1, 0
        else:
            tip = anchor-tip_extra
            bar = tip+depth-1
            if bar <= 3:
                continue
            vertical = transverse(bar, -1, 4, depth)
            point = 1, 3
        if current[0] & vertical[0]:
            continue
        assert (0, anchor) in vertical[0] and (0, anchor) in current[1]
        assert point in current[1] and point not in current[0] | vertical[0]
        assert len(set(neighbors(point)) & (current[0] | vertical[0])) >= 2
        checked += 1
    return checked


def main():
    print(json.dumps(dict(status='PASS', shapes=shape_roles(), top_gaps=top_gap_controls(),
                         middle_stems=middle_stem_controls(),
                         scope='Exact finite shape identities and canonical unbounded-interval controls. '
                         'The separate written proof classifies every actual owner and excludes rotors '
                         'at arbitrary pocket width; these controls alone do not prove that theorem.'), indent=2))


if __name__ == '__main__':
    main()
