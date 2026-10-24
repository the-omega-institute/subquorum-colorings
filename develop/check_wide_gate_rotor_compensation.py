"""Original-source checks for forced two-gate rotor compensation at all widths."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records, rotor_record
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def left_rotor(upper):
    records = {}
    for symmetry in itertools.product((False, True), repeat=3):
        for record in anchor_records(rotor_record(symmetry), (5, 1), {(0, 1)}):
            records[min(row for row, column in record[0])] = record
    assert set(records) == {3, 4}
    return records[3 if upper else 4]


def mirror(record, width):
    move = lambda point: (point[0], width+1-point[1])
    return ({move(point) for point in record[0]}, {move(point) for point in record[1]},
            {tuple(sorted((move(first), move(second)))) for first, second in record[2]})


def old_family(width, amount, top, left_depth, right_depth):
    return [independent_source((width+2, left_depth, right_depth),
                               (False, False, False), (0, -1))]+[
        independent_source((width, 4, 4), (False, False, False), (top+8*index, 0))
        for index in range(amount)]


def check_batch(width, amount, top, extra, choices, offset):
    far_tip = top+8*(amount-1)+4
    old = [shift(record, offset) for record in old_family(
        width, amount, top, far_tip+extra, far_tip+2*extra)]
    before = inventory(old)
    assert phi_from(old, before) == 1-amount
    new, full_expected, events_expected = [], set(), set()
    left_canonical = {upper: left_rotor(upper) for upper in (False, True)}
    up_count = 0
    for index, (left_upper, right_upper) in enumerate(choices):
        row = top+8*index
        for right, upper in ((False, left_upper), (True, right_upper)):
            record = mirror(left_canonical[upper], width) if right else left_canonical[upper]
            record = shift(record, (row+offset[0], offset[1]))
            source = len(old)+len(new)
            assert charge(record) == (-2 if upper else 0)
            new.append(record)
            column = width if right else 0
            tile = ((row+4+offset[0])//2, (column+offset[1])//2)
            assert tile not in full_expected
            full_expected.add(tile)
            if upper:
                point = row+5+offset[0], (width if right else 1)+offset[1]
                events_expected.add((source, point, (point[0]-1, point[1])))
                up_count += 1
    after = inventory(old+new)
    assert after['full']-before['full'] == full_expected
    assert after['events']-before['events'] == events_expected
    assert before['events'] <= after['events']
    assert phi_from(old+new, after)-phi_from(old, before) == 4*(amount-1)+up_count
    assert phi_from(old+new, after) == 3*(amount-1)+up_count
    return up_count


def role_controls():
    U_roles = rotor_roles = 0
    for width in (6, 8, 10, 20):
        old = old_family(width, 2, 2, 20, 20)
        blocked = set.union(*(record[0] for record in old))
        dimensions = itertools.product((6, 8, 12), (4, 6, 10), (4, 6, 10))
        for size, symmetry in itertools.product(dimensions, itertools.product((False, True), repeat=3)):
            record = independent_source(size, symmetry, (0, 0))
            for point, free in (((7, 1), {(0, 1), (1, 0)}),
                                ((7, width), {(0, -1), (1, 0)})):
                for moved in anchor_records(record, point, free):
                    assert moved[0] & blocked
                    U_roles += 1
        for right in (False, True):
            point = (7, width) if right else (7, 1)
            free = {(0, -1), (1, 0)} if right else {(0, 1), (1, 0)}
            candidates = set()
            for symmetry in itertools.product((False, True), repeat=3):
                for moved in anchor_records(rotor_record(symmetry), point, free):
                    rotor_roles += 1
                    if not moved[0] & blocked:
                        candidates.add(tuple(frozenset(part) for part in moved))
            expected = set()
            for upper in (False, True):
                record = mirror(left_rotor(upper), width) if right else left_rotor(upper)
                expected.add(tuple(frozenset(part) for part in shift(record, (2, 0))))
            assert candidates == expected
    return dict(U_roles_excluded=U_roles, exact_rotor_roles=rotor_roles)


def batch_controls():
    checked = sharp = 0
    for width, amount, offset in itertools.product((8, 12), (2, 3, 4, 5), ((0, 0), (-100, -200))):
        for bits in itertools.product((False, True), repeat=2*(amount-1)):
            choices = list(zip(bits[::2], bits[1::2]))
            up_count = check_batch(width, amount, 2, 0, choices, offset)
            checked += 1
            sharp += up_count == 0
    large = []
    for width, amount, top, extra in ((8, 12, 2, 0), (50, 12, 40, 200),
                                     (200, 12, 1000, 2000), (2000, 2, 2000, 4000)):
        choices = [(index % 2 == 0, index % 3 == 0) for index in range(amount-1)]
        up_count = check_batch(width, amount, top, extra, choices, (0, 0))
        large.append(dict(width=width, inner_sources=amount, top=top,
                          rotor_count=2*(amount-1), upper_rotors=up_count,
                          selected_Phi=3*(amount-1)+up_count))
    return dict(exact_full_event_batches=checked, sharp_batches=sharp, large=large)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', roles=role_controls(), batches=batch_controls(),
        scope='Full-source finite controls supplement the all-parameter forced-rotor '
              'classification and simultaneous nonreuse proof; no complete extension '
              'existence or arbitrary-old-baseline monotonicity is claimed.'), indent=2))
