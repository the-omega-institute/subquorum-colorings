"""Full-record controls for ceiling descent and excluded boundary horizontal U."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import rotor_record
from check_even_gap_axial_compensation import transform
from check_six_row_mixed_aligned_u_budget import complete_controls
from check_six_row_transverse_budget import transverse


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def north(left, width, down):
    original = independent_source((width, 4, 4), (False, False, False), (0, 0))
    return transform(original, lambda point: (
        point[0] if down else 4-point[0], left-1+point[1]))


def anchored(record, point):
    for anchor in record[0]:
        yield transform(record, lambda site: (
            site[0]+point[0]-anchor[0], site[1]+point[1]-anchor[1]))


def corner_roles():
    checked = survivors = 0
    for dimensions, symmetry in itertools.product(
            itertools.product((6, 8, 14, 30), (4, 6, 10), (4, 6, 10)),
            itertools.product((False, True), repeat=3)):
        original = independent_source(dimensions, symmetry, (0, 0))
        for record in anchored(original, (4, 0)):
            checked += 1
            if not all(0 <= row <= 4 and column <= 0 for row, column in record[0]):
                continue
            left = min(column for row, column in record[0])
            width = 1-left
            assert record in (north(left, width, True), north(left, width, False))
            assert (4, left-1) in record[1] and (0, left) in record[0]
            survivors += 1
    rotor_roles = 0
    normalized = set()
    for symmetry in itertools.product((False, True), repeat=3):
        original = rotor_record(symmetry)
        minimum_row = min(row for row, column in original[0])
        minimum_column = min(column for row, column in original[0])
        normalized.add(frozenset((row-minimum_row, column-minimum_column)
                                 for row, column in original[0]))
        bottom = max(row for row, column in original[0])
        right = max(column for row, column in original[0])
        assert (bottom, right) not in original[0]
        assert all((row-1, column) in original[0]
                   for row, column in original[0] if row == bottom)
        for record in anchored(original, (4, 0)):
            assert not all(0 <= row <= 4 and column <= 0 for row, column in record[0])
            rotor_roles += 1
    assert len(normalized) == 2
    for width, down in itertools.product((6, 20, 2000), (False, True)):
        record = north(1-width, width, down)
        assert (4, 0) in record[0] and (4, -width) in record[1]
    return dict(U_anchor_roles=checked, surviving_north_roles=survivors,
                forbidden_rotor_anchor_roles=rotor_roles,
                normalized_rotor_shapes=len(normalized), large_north_controls=6)


def bottom_support_owners():
    checked = surviving = 0
    originals = [(independent_source(dimensions, symmetry, (0, 0)), symmetry[0])
                 for dimensions, symmetry in itertools.product(
                     itertools.product((6, 8, 14), (4, 6, 10), (4, 6, 10)),
                     itertools.product((False, True), repeat=3))]
    originals += [(rotor_record(symmetry), False)
                  for symmetry in itertools.product((False, True), repeat=3)]
    for width in (6, 8, 20, 2000):
        old = north(0, width, True)
        assert (5, 0) in old[1]
        for original, transverse_orientation in originals:
            for record in anchored(original, (5, 0)):
                checked += 1
                if (not all(0 <= row <= 5 for row, column in record[0])
                        or record[0] & old[0]):
                    continue
                assert transverse_orientation
                bottom = {column for row, column in record[0] if row == 5}
                top = {column for row, column in record[0] if row == 0}
                assert len(bottom) >= len(top)+2
                surviving += 1
    assert surviving
    return dict(anchor_roles=checked, surviving_transverse_roles=surviving,
                nontransverse_survivors=0)


def descent_obstructions():
    checked = 0
    for width, amount, left, alternate in itertools.product(
            (6, 8, 20, 2000), (1, 2, 3, 8), (6, 20), (False, True)):
        records = [transverse(0, 1, left+width*amount, 4)]
        records += [north(left+width*index, width, not alternate or index % 2 == 0)
                    for index in range(amount)]
        endpoints = set.union(*(record[0] for record in records))
        assert len(endpoints) == sum(len(record[0]) for record in records)
        for index in range(1, amount+1):
            next_support = 4, left+width*(index-1)-1
            assert next_support in records[index][1]
            assert {(4, next_support[1]+1), (5, next_support[1])} <= (
                set(neighbors(next_support)) & endpoints)
            if index > 1:
                assert next_support in records[index-1][0]
        first_support = 4, left-1
        assert first_support not in endpoints
        assert len(set(neighbors(first_support)) & endpoints) >= 2
        checked += 1
    return dict(partial_chains=checked, largest_width=2000,
                conclusion='Every displayed finite leftward consumer chain leaves its first '
                'renewed support unconsumed with at least two endpoint neighbours. '
                'General exclusion is a separate descent proof, not extrapolation.')


def interior_rotor_separation():
    checked = 0
    for width, upward in itertools.product((6, 8, 20), (False, True)):
        old = north(0, width, False)
        if not upward:
            old = transform(old, lambda point: (5-point[0], point[1]))
        for symmetry in itertools.product((False, True), repeat=3):
            original = rotor_record(symmetry)
            for point in itertools.product(range(6), range(width)):
                for record in anchored(original, point):
                    assert (not all(0 <= row <= 5 for row, column in record[0])
                            or bool(record[0] & old[0]))
                    checked += 1
    return dict(anchor_roles=checked, survivors=0)


def main():
    print(json.dumps(dict(status='PASS', corner_roles=corner_roles(),
                         bottom_support_owners=bottom_support_owners(),
                         descent_obstructions=descent_obstructions(),
                         interior_rotor_separation=interior_rotor_separation(),
                         exact_H_peeling_complete_controls=complete_controls(),
                         scope='Exact immutable canonical record controls. Full strip source '
                         'classification, connected-wall confinement, support forcing and '
                         'unbounded descent are separately proved. No grid-global claim.'), indent=2))


if __name__ == '__main__':
    main()
