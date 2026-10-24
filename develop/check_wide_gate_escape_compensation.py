"""Exact original-source controls for forced wide-gate escape pairs."""

import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records, rotor_record
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_wide_gate_rotor_compensation import left_rotor, mirror, old_family


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def signature(record):
    return tuple(frozenset(part) for part in record)


def escape(depth, far, top):
    return independent_source((6, depth, far), (True, True, False), (top+1, 2+depth))


def retained(width, amount, top, extra=0):
    bottom = top+8*(amount-1)+4
    old = old_family(width, amount, top, bottom+extra, bottom+2*extra)
    rotors = [shift(mirror(left_rotor(True), width) if right else left_rotor(True),
                    (top+8*index, 0))
              for index, right in itertools.product(range(amount-1), (False, True))]
    return old+rotors


def record_counts(depth, far):
    record = escape(depth, far, 0)
    expected_endpoints = {(2, column) for column in range(2, depth+3)}
    expected_endpoints |= {(row, depth+2) for row in range(2, 8)}
    expected_endpoints |= {(row, depth+1) for row in range(3, 7)}
    expected_endpoints |= {(7, column) for column in range(depth+2-far, depth+3)}
    expected_support = {(1, column) for column in range(2, depth+3, 2)}
    expected_support |= {(8, column) for column in range(depth+2-far, depth+3, 2)}
    expected_support |= {(2, 1), (7, depth+1-far)}
    expected_support |= {(3, column) for column in range(3, depth, 2)}
    expected_support |= {(6, column) for column in range(depth+3-far, depth, 2)}
    assert record[0] == expected_endpoints and record[1] == expected_support
    tiles = {(row//2, column//2) for row, column in record[0]}
    inside = {point for point in record[1] if (point[0]//2, point[1]//2) in tiles}
    half_sum = (depth+far)//2
    assert (len(record[2]), len(tiles), len(inside)) == (5+half_sum, 4+half_sum, half_sum-2)
    assert charge(record) == -5


def north_gate(records, point):
    occupied = set.union(*(record[0] for record in records))
    assert point not in occupied and any(point in record[1] for record in records)
    assert set(neighbors(point)) & occupied == {
        (point[0], point[1]-1), (point[0], point[1]+1), (point[0]+1, point[1])}
    U_roles = rotor_roles = 0
    dimensions = itertools.product((6, 8, 14), (4, 6, 20), (4, 8, 24))
    for size, symmetry in itertools.product(dimensions, itertools.product((False, True), repeat=3)):
        record = independent_source(size, symmetry, (0, 0))
        for moved in anchor_records(record, point, {(-1, 0)}):
            assert moved[0] & occupied
            U_roles += 1
    for symmetry in itertools.product((False, True), repeat=3):
        for moved in anchor_records(rotor_record(symmetry), point, {(-1, 0)}):
            assert moved[0] & occupied
            rotor_roles += 1
    return U_roles, rotor_roles


def owner_controls():
    U_excluded = rotor_excluded = escape_roles = normalized = 0
    for width in (8, 10, 14, 16, 24, 50):
        old = old_family(width, 2, 2, 30, 30)
        counts = north_gate(old+[shift(left_rotor(False), (2, 0))], (9, 1))
        U_excluded += counts[0]
        rotor_excluded += counts[1]
        base = retained(width, 2, 2)
        occupied = set.union(*(record[0] for record in base))
        point = (4, 2)
        assert set(neighbors(point)) & occupied == {(3, 2), (4, 1), (5, 2)}
        dimensions = itertools.product((6, 8, 14), (4, 6, 10, 20, 40), (4, 6, 10, 20, 40))
        found = set()
        for size, symmetry in itertools.product(dimensions, itertools.product((False, True), repeat=3)):
            record = independent_source(size, symmetry, (0, 0))
            for moved in anchor_records(record, point, {(0, 1)}):
                escape_roles += 1
                if not moved[0] & occupied:
                    found.add(signature(moved))
        expected = {signature(escape(depth, far, 2))
                    for depth, far in itertools.product((4, 6, 10, 20, 40), repeat=2)
                    if far <= depth <= width-6}
        assert found == expected
        normalized += len(found)
        for symmetry in itertools.product((False, True), repeat=3):
            for moved in anchor_records(rotor_record(symmetry), point, {(0, 1)}):
                assert moved[0] & occupied
                rotor_excluded += 1
        for depth in range(4, width-5, 2):
            counts = north_gate(base+[escape(depth, depth, 2)], (9, 1))
            U_excluded += counts[0]
            rotor_excluded += counts[1]
    return dict(north_gate_U_roles_excluded=U_excluded,
                rotor_roles_excluded=rotor_excluded,
                east_terminal_U_roles=escape_roles, normalized_records=normalized)


def check_pair_batch(width, amount, top, parameters, offset=(0, 0), extra=0):
    assert width >= 16 and width % 2 == top % 2 == 0
    assert len(parameters) == amount-1
    base = [shift(record, offset) for record in retained(width, amount, top, extra)]
    before = inventory(base)
    assert phi_from(base, before) == 5*(amount-1)
    new, expected_full, expected_events = [], set(), set()
    tight = 0
    for index, (left_depth, left_far, right_depth, right_far) in enumerate(parameters):
        assert min(left_depth, right_depth) >= 6
        assert 4 <= left_far <= left_depth-2 and 4 <= right_far <= right_depth-2
        assert left_depth+right_depth <= width-4
        assert all(value % 2 == 0 for value in (left_depth, left_far, right_depth, right_far))
        row = top+8*index
        owners = []
        for right, depth, far in ((False, left_depth, left_far), (True, right_depth, right_far)):
            record = escape(depth, far, row)
            if right:
                record = mirror(record, width)
            record = shift(record, offset)
            owner = len(base)+len(new)
            owners.append(owner)
            new.append(record)
            assert charge(record) == -5
            point = row+2+offset[0], (width-1 if right else 2)+offset[1]
            expected_events.add((owner, point, (point[0]+1, point[1])))
        if left_depth+right_depth == width-4:
            tight += 1
            column = left_depth+2+offset[1]
            for delta in (2, 4, 6):
                tile = ((row+delta+offset[0])//2, column//2)
                assert tile not in expected_full
                expected_full.add(tile)
            for delta in range(2, 8):
                left = row+delta+offset[0], column
                right = left[0], column+1
                expected_events.add((owners[0], left, right))
                expected_events.add((owners[1], right, left))
    after = inventory(base+new)
    assert after['full']-before['full'] == expected_full
    assert after['events']-before['events'] == expected_events
    assert before['events'] <= after['events']
    assert len(expected_full) == 3*tight
    assert len(expected_events) == 2*(amount-1)+12*tight
    assert phi_from(base+new, after)-phi_from(base, before) == 8*(amount-1)-6*tight
    assert phi_from(base+new, after) == 13*(amount-1)-6*tight >= 7*(amount-1)
    return tight


def receipt_controls():
    singles = pairs = tight = edge_debits = 0
    for width in (16, 18, 20, 24, 30):
        base = retained(width, 2, 2)
        before = inventory(base)
        for depth in range(6, width-5, 2):
            for far in range(4, depth-1, 2):
                record_counts(depth, far)
                record = escape(depth, far, 2)
                after = inventory(base+[record])
                assert after['full'] == before['full']
                expected_events = {(len(base), (4, 2), (5, 2))}
                boundary = depth == width-6
                if boundary:
                    expected_events.add((len(base), (6, width-4), (6, width-3)))
                    edge_debits += 1
                assert after['events']-before['events'] == expected_events
                assert phi_from(base+[record], after)-phi_from(base, before) == 4-int(boundary)
                singles += 1
        for left_depth, right_depth in itertools.product(range(6, width-9, 2), repeat=2):
            if left_depth+right_depth > width-4:
                continue
            for left_far, right_far in itertools.product(range(4, left_depth-1, 2),
                                                        range(4, right_depth-1, 2)):
                tight += check_pair_batch(width, 2, 2, [(left_depth, left_far, right_depth, right_far)])
                pairs += 1
    generator = random.Random(20261022)
    batches = 0
    for width, amount, top, offset in itertools.product((16, 24, 40), (3, 8, 12),
                                                       (2, 100), ((0, 0), (-200, -400))):
        parameters = []
        for index in range(amount-1):
            left_depth = generator.randrange(6, width-9, 2)
            right_depth = generator.randrange(6, width-3-left_depth, 2)
            parameters.append((left_depth, generator.randrange(4, left_depth-1, 2),
                               right_depth, generator.randrange(4, right_depth-1, 2)))
        check_pair_batch(width, amount, top, parameters, offset)
        batches += 1
    for width, amount, top, extra in ((200, 12, 1000, 2000), (2000, 2, 2000, 4000)):
        check_pair_batch(width, amount, top, [(6, 4, width-10, 4)]*(amount-1), extra=extra)
        batches += 1
    return dict(exact_single_escape_inventories=singles, single_boundary_debits=edge_debits,
                exact_pair_inventories=pairs,
                tight_pairs=tight, simultaneous_batches=batches,
                narrow_complete_extension_exclusion='All even W=8,10,12,14 by necessary depth pair sum')


def short_far_controls():
    cases = U_roles = rotor_roles = 0
    for width in (16, 20, 40):
        for depth in range(6, width-5, 2):
            records = retained(width, 2, 2)+[escape(depth, depth-2, 2)]
            occupied = set.union(*(record[0] for record in records))
            point = (9, 3)
            assert point in records[-1][1] and point not in occupied
            assert set(neighbors(point)) & occupied == {(8, 3), (9, 4), (10, 3)}
            dimensions = itertools.product((6, 8, 14), (4, 6, 20), (4, 8, 24))
            for size, symmetry in itertools.product(dimensions, itertools.product((False, True), repeat=3)):
                record = independent_source(size, symmetry, (0, 0))
                for moved in anchor_records(record, point, {(0, -1)}):
                    assert moved[0] & occupied
                    U_roles += 1
            for symmetry in itertools.product((False, True), repeat=3):
                for moved in anchor_records(rotor_record(symmetry), point, {(0, -1)}):
                    assert moved[0] & occupied
                    rotor_roles += 1
            cases += 1
    return dict(cases=cases, U_roles_excluded=U_roles, rotor_roles_excluded=rotor_roles,
                consequence='Actual f<=k-4, k>=8 and W>=20; W16/18 also excluded. '
                            'Post-submission addendum, not in initial oracle packet.')


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', owners=owner_controls(), receipts=receipt_controls(),
        short_far=short_far_controls(),
        scope='Finite original-source controls supplement general role, support and '
              'nonreuse proofs. Selected-family Phi>=7g, no arbitrary-extension '
              'monotonicity, complete-family existence or global bound claimed.'), indent=2))
