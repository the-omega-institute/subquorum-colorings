"""Full-record controls for actual two-gate compensation at bar spacing ten."""

import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records, rotor_record
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_wide_gate_escape_compensation import signature
from check_wide_gate_rotor_compensation import left_rotor, mirror


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def baseline(width, amount=2, top=2, extra=20):
    bottom = top+10*(amount-1)+4
    return [independent_source((width+2, bottom+extra, bottom+2*extra),
                              (False, False, False), (0, -1))]+[
        independent_source((width, 4, 4), (False, False, False), (top+10*index, 0))
        for index in range(amount)]


def candidate(mode, breadth):
    if mode in ('L', 'H'):
        return left_rotor(mode == 'H')
    return independent_source((breadth, 4, 6 if mode == 'V' else 4),
                              (False, mode != 'D', False), (5 if mode == 'D' else 9, 0))


def options(width):
    return [(mode, breadth, candidate(mode, breadth))
            for breadth in range(6, width+1, 2) for mode in ('D', 'U', 'V')
            if mode != 'V' or breadth < width]+[
        (mode, 4, candidate(mode, 4)) for mode in ('L', 'H')]


def single_receipt(mode, breadth, width, top=2):
    spanning = breadth == width
    if mode in ('L', 'H'):
        return {(top//2+2, 0)}, ({(3, (top+5, 1), (top+4, 1))}
                if mode == 'H' else set()), 2+int(mode == 'H')
    full = {(top//2+row, 0) for row in (2, 3, 4)}
    events = {(0, (top+row, 0), (top+row, 1)) for row in (6, 8)}
    events |= {(3, (top+row, 1), (top+row, 0)) for row in (6, 8)}
    if mode == 'D':
        events.add((3, (top+5, 1), (top+4, 1)))
    if spanning:
        full |= {(row, width//2) for row, column in full}
        events |= {(owner, (point[0], width+1-point[1]),
                    (target[0], width+1-target[1])) for owner, point, target in events}
    gain = breadth+int(spanning) if mode == 'D' else 3+2*int(spanning)
    return full, events, gain


def cross_counts(left_mode, right_mode):
    if left_mode in ('D', 'U', 'V') and right_mode in ('D', 'U', 'V'):
        return (3, 6) if left_mode == right_mode == 'V' else (2, 4)
    mixed = (left_mode in ('D', 'U', 'V')) != (right_mode in ('D', 'U', 'V'))
    debit = mixed and ('L' in (left_mode, right_mode) or 'V' in (left_mode, right_mode))
    return 0, int(debit)


def role_controls():
    sizes = (6, 8, 14, 30, 60)
    depths = (4, 6, 8, 20, 60)
    originals = [independent_source(size, symmetry, (0, 0))
                 for size, symmetry in itertools.product(
                     itertools.product(sizes, depths, depths),
                     itertools.product((False, True), repeat=3))]
    U_roles = rotor_roles = normalized = 0
    for width in (6, 8, 12, 20, 50):
        old = baseline(width)
        occupied = set.union(*(record[0] for record in old))
        point = (7, 1)
        assert point in old[1][1] and point not in occupied
        assert set(neighbors(point)) & occupied == {(6, 1), (7, 0)}
        actual = set()
        for original in originals:
            for record in anchor_records(original, point, {(0, 1), (1, 0)}):
                U_roles += 1
                if not record[0] & occupied:
                    actual.add(signature(record))
        expected = {signature(shift(record, (2, 0))) for mode, breadth, record in options(width)
                    if mode in ('D', 'U', 'V') and breadth in sizes}
        assert actual == expected
        normalized += len(actual)
        actual = set()
        for symmetry in itertools.product((False, True), repeat=3):
            for record in anchor_records(rotor_record(symmetry), point, {(0, 1), (1, 0)}):
                rotor_roles += 1
                if not record[0] & occupied:
                    actual.add(signature(record))
        assert actual == {signature(shift(left_rotor(upper), (2, 0))) for upper in (False, True)}
    return dict(U_roles=U_roles, rotor_roles=rotor_roles, normalized_U_records=normalized)


def checked_pairs(width):
    old = baseline(width)
    before = inventory(old)
    before_Phi = phi_from(old, before)
    assert before_Phi == -1
    choices = []
    for left_mode, left_radius, left in options(width):
        moved = shift(left, (2, 0))
        after = inventory(old+[moved])
        full, events, gain = single_receipt(left_mode, left_radius, width)
        assert after['full']-before['full'] == full
        assert after['events']-before['events'] == events
        assert charge(left) == (1-left_radius if left_mode == 'D' else
                                1 if left_mode in ('U', 'V') else -2 if left_mode == 'H' else 0)
        assert phi_from(old+[moved], after)-before_Phi == gain
        for right_mode, right_radius, right_original in options(width):
            right = mirror(right_original, width)
            shared = signature(left) == signature(right)
            if shared:
                assert left_mode == right_mode and left_mode in ('D', 'U') and left_radius == width
                choices.append(([left], gain))
                continue
            collision = bool(left[0] & right[0])
            assert collision == (left_radius+right_radius > width)
            if collision:
                continue
            cross = inventory([left, right])
            expected = cross_counts(left_mode, right_mode) if left_radius+right_radius == width else (0, 0)
            assert (len(cross['full']), len(cross['events'])) == expected
            right_gain = single_receipt(right_mode, right_radius, width)[2]
            joint_gain = gain+right_gain+2*expected[0]-expected[1]
            pair = [shift(record, (2, 0)) for record in (left, right)]
            after = inventory(old+pair)
            assert phi_from(old+pair, after)-before_Phi == joint_gain
            assert len(after['full']-before['full']) == len(full)+len(single_receipt(right_mode, right_radius, width)[0])+expected[0]
            assert joint_gain >= 4
            choices.append(([left, right], joint_gain))
    assert choices and min(gain for records, gain in choices) == (5 if width == 6 else 4)
    return choices


def batch_controls(pair_library):
    generator = random.Random(20261022)
    batches = 0
    for width, amount, top, offset in itertools.product(
            (6, 8, 12, 20), (2, 3, 6), (2, 40), ((0, 0), (-100, -200))):
        old = [shift(record, offset) for record in baseline(width, amount, top)]
        before = inventory(old)
        assert phi_from(old, before) == 1-amount
        for trial in range(8):
            new, gains = [], []
            for index in range(amount-1):
                records, gain = generator.choice(pair_library[width])
                new.extend(shift(record, (top+10*index+offset[0], offset[1])) for record in records)
                gains.append(gain)
            assert len({signature(record) for record in new}) == len(new)
            after = inventory(old+new)
            assert phi_from(old+new, after) == 1-amount+sum(gains)
            assert phi_from(old+new, after) >= (4 if width == 6 else 3)*(amount-1)
            new_full, new_events = set(), set()
            owner = len(old)
            for index, gain in enumerate(gains):
                row = top+10*index+offset[0]
                gap_records = [record for record in new if row+3 <= min(point[0] for point in record[0]) <= row+5]
                one = inventory(old+gap_records)
                full = one['full']-before['full']
                events = {(owner+event[0]-len(old) if event[0] >= len(old) else event[0], event[1], event[2])
                          for event in one['events']-before['events']}
                assert not new_full & full and not new_events & events
                new_full |= full
                new_events |= events
                owner += len(gap_records)
            assert after['full']-before['full'] == new_full
            assert after['events']-before['events'] == new_events
            batches += 1
    return batches


def run():
    roles = role_controls()
    pairs = {width: checked_pairs(width) for width in (6, 8, 10, 12, 14, 20, 30)}
    batches = batch_controls(pairs)
    large = []
    for width in (100, 2000):
        old = baseline(width, 12, 2000)
        before = inventory(old)
        new = [shift(candidate('U', width), (2000+10*index, 0)) for index in range(11)]
        after = inventory(old+new)
        assert phi_from(old+new, after) == 44
        large.append(dict(width=width, gaps=11, shared_spanning_owners=11, Phi=44))
    return dict(status='PASS', roles=roles,
                pairs={str(width): len(choices) for width, choices in pairs.items()},
                mixed_batches=batches, large=large,
                scope='Finite controls of the written all-parameter spacing-ten actual-owner '
                      'classification and selected simultaneous compensation. Does not prove '
                      'complete-extension existence, arbitrary-old monotonicity or global target.')


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
