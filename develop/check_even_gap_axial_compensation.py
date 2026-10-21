"""Exact source controls for all even gaps and the one-axial-owner theorem."""

import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records, rotor_record
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_ten_row_gate_compensation import candidate as ten_candidate
from check_ten_row_gate_compensation import checked_pairs
from check_wide_gate_escape_compensation import signature
from check_wide_gate_rotor_compensation import left_rotor, mirror


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def transform(record, move):
    return ({move(point) for point in record[0]},
            {move(point) for point in record[1]},
            {tuple(sorted((move(first), move(second)))) for first, second in record[2]})


def baseline(width, rows, extra=0):
    bottom = rows[-1]+4
    return [independent_source((width+2, bottom+extra, bottom+2*extra),
                              (False, False, False), (0, -1))]+[
        independent_source((width, 4, 4), (False, False, False), (row, 0))
        for row in rows]


def make_source(mode, breadth, near, far):
    canonical = independent_source((breadth, near, far), (False, False, False), (0, 0))
    charts = dict(D=lambda point: (5+point[0], point[1]),
                  U=lambda point: (5+near-point[0], point[1]),
                  R=lambda point: (4+point[1], 1+point[0]),
                  E=lambda point: (4+point[1], 1+near-point[0]))
    return transform(canonical, charts[mode])


def options(width, gap):
    records = []
    for breadth in range(6, width+1, 2):
        for near, far in itertools.product(range(4, gap-5, 2), repeat=2):
            records.append(('D', breadth, near, far, make_source('D', breadth, near, far)))
        for near in range(4, gap-5, 2):
            for far in range(4, near+(1 if breadth == width else 3), 2):
                records.append(('U', breadth, near, far, make_source('U', breadth, near, far)))
    for breadth in range(6, gap-5, 2):
        for near, far in itertools.product(range(4, width-1, 2), repeat=2):
            records.append(('R', breadth, near, far, make_source('R', breadth, near, far)))
        for near in range(4, width-1, 2):
            for far in range(4, near+1, 2):
                records.append(('E', breadth, near, far, make_source('E', breadth, near, far)))
    records.extend((mode, 0, 0, 0, left_rotor(mode == 'H')) for mode in ('H', 'L'))
    assert len({signature(row[-1]) for row in records}) == len(records)
    return records


def receipt(mode, breadth, near, far, width):
    if mode == 'D':
        spanning = int(breadth == width)
        full = near//2+1+spanning*(far//2+1)
        events = near+1+spanning*(far+1)
        return full, events, 1-breadth, breadth+spanning
    if mode == 'U':
        spanning = int(breadth == width)
        equal = int(near == far)
        full = near//2+1+spanning*(far//2+equal)
        events = near+spanning*far
        return full, events, 1, 3+2*spanning*equal
    if mode == 'R':
        return breadth//2, 3*breadth//2, 1-breadth, breadth//2-1
    if mode == 'E':
        equal = int(near == far)
        return 1, equal, 1, 3-equal
    return 1, int(mode == 'H'), -2 if mode == 'H' else 0, 3 if mode == 'H' else 2


def exact_receipt(mode, breadth, near, far, width, top=2):
    full, events = set(), set()
    def wall_band(first, last):
        return {(owner, (top+row, column), (top+row, 1-column))
                for row in range(first, last+1, 2) for owner, column in ((0, 0), (3, 1))}
    if mode in ('D', 'U'):
        full = {(top//2+row, 0) for row in range(2, near//2+3)}
        events = wall_band(6, near+4)
        if mode == 'D':
            events.add((3, (top+5, 1), (top+4, 1)))
        if breadth == width:
            if mode == 'D':
                far_full = {(top//2+row, width//2) for row in range(2, far//2+3)}
                far_events = wall_band(6, far+4)
                far_events.add((3, (top+5, 1), (top+4, 1)))
            else:
                far_full = {(top//2+row, width//2)
                            for row in range(3+(near-far)//2, near//2+3)}
                if far == near:
                    far_full.add((top//2+2, width//2))
                far_events = wall_band(6+near-far, near+4)
            full |= far_full
            events |= {(owner, (point[0], width+1-point[1]),
                        (target[0], width+1-target[1])) for owner, point, target in far_events}
    elif mode == 'R':
        full = {(top//2+row, 0) for row in range(2, breadth//2+2)}
        events = {(3, (top+row, 1), (top+row, 0)) for row in range(5, breadth+5)}
        events |= {(0, (top+row, 0), (top+row, 1)) for row in range(6, breadth+5, 2)}
    else:
        full = {(top//2+2, 0)}
        if mode == 'E' and near == far:
            events = {(0, (top+breadth+4, 0), (top+breadth+4, 1))}
        elif mode == 'H':
            events = {(3, (top+5, 1), (top+4, 1))}
    return full, events


def role_controls():
    dimensions = tuple(itertools.product((6, 8, 14, 40), (4, 6, 12, 40), (4, 6, 12, 40)))
    originals = [independent_source(size, symmetry, (0, 0))
                 for size, symmetry in itertools.product(dimensions, itertools.product((False, True), repeat=3))]
    rotors = [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    checked = [0, 0]
    survivors = patterns = 0
    for width, gap in itertools.product((6, 8, 12, 20), (10, 12, 14, 20)):
        old = baseline(width, (2, 2+gap), 20)
        occupied = set.union(*(record[0] for record in old))
        point = (7, 1)
        assert point in old[1][1] and point not in occupied
        assert set(neighbors(point)) & occupied == {(6, 1), (7, 0)}
        catalogue = {signature(shift(row[-1], (2, 0))) for row in options(width, gap)}
        for kind, library in enumerate((originals, rotors)):
            actual = set()
            for original in library:
                for record in anchor_records(original, point, {(0, 1), (1, 0)}):
                    checked[kind] += 1
                    if record[0] & occupied:
                        continue
                    assert signature(record) in catalogue
                    actual.add(signature(record))
            expected = set()
            for mode, breadth, near, far, record in options(width, gap):
                source_kind = int(mode in ('H', 'L'))
                if source_kind == kind and (kind or (breadth, near, far) in dimensions):
                    expected.add(signature(shift(record, (2, 0))))
            assert actual == expected
            survivors += len(actual)
        patterns += 1
    return dict(patterns=patterns, U_roles=checked[0], rotor_roles=checked[1], survivors=survivors)


def receipt_controls():
    checked = 0
    modes = {}
    library = {}
    for width, gap in itertools.product((6, 8, 12, 20), (10, 12, 14, 20)):
        old = baseline(width, (2, 2+gap), 20)
        before = inventory(old)
        assert phi_from(old, before) == -1
        choices = options(width, gap)
        for mode, breadth, near, far, canonical in choices:
            record = shift(canonical, (2, 0))
            full, events, expected_charge, gain = receipt(mode, breadth, near, far, width)
            after = inventory(old+[record])
            assert len(after['full']-before['full']) == full
            assert len(after['events']-before['events']) == events
            expected_full, expected_events = exact_receipt(mode, breadth, near, far, width)
            assert after['full']-before['full'] == expected_full
            assert after['events']-before['events'] == expected_events
            assert before['full'] <= after['full'] and before['events'] <= after['events']
            assert charge(record) == expected_charge
            assert phi_from(old+[record], after)-phi_from(old, before) == gain >= 2
            assert all(3 <= row <= gap-1 for row, column in canonical[0])
            assert (5, 1) in canonical[0]
            checked += 1
            modes[mode] = modes.get(mode, 0)+1
        library[width, gap] = choices
    return dict(records=checked, modes=modes), library


def mixed_batch_controls(library):
    generator = random.Random(20261022)
    ten_pairs = {width: [(records, gain) for records, gain in checked_pairs(width)
                         if all(signature(record) not in {signature(left_rotor(False)),
                             signature(mirror(left_rotor(False), width))} for record in records)]
                 for width in (6, 8, 12, 20)}
    checked = strengthened = 0
    for width, amount, top, offset in itertools.product(
            (6, 8, 12, 20), (2, 3, 6, 12), (2, 40), ((0, 0), (-100, -200))):
        for trial in range(4):
            gaps = [generator.choice((10, 12, 14, 20)) for index in range(amount-1)]
            rows = [top]
            for gap in gaps:
                rows.append(rows[-1]+gap)
            old = [shift(record, offset) for record in baseline(width, rows, 20)]
            before = inventory(old)
            assert phi_from(old, before) == 1-amount
            new, gains = [], []
            for index, gap in enumerate(gaps):
                mode, breadth, near, far, record = generator.choice(library[width, gap])
                new.append(shift(record, (rows[index]+offset[0], offset[1])))
                gains.append(receipt(mode, breadth, near, far, width)[-1])
            after = inventory(old+new)
            assert phi_from(old+new, after) == 1-amount+sum(gains) >= amount-1
            full_partition, event_partition = set(), set()
            for index, record in enumerate(new):
                isolated = inventory(old+[record])
                full = isolated['full']-before['full']
                events = {(len(old)+index if owner == len(old) else owner, point, target)
                          for owner, point, target in isolated['events']-before['events']}
                assert not full_partition & full and not event_partition & events
                full_partition |= full
                event_partition |= events
            assert full_partition == after['full']-before['full']
            assert event_partition == after['events']-before['events']
            assert len({signature(record) for record in new}) == len(new)
            checked += 1
            combined, combined_gains = [], []
            for index, gap in enumerate(gaps):
                if gap == 10:
                    records, gain = generator.choice(ten_pairs[width])
                    combined.extend(shift(record, (rows[index]+offset[0], offset[1])) for record in records)
                    combined_gains.append(gain)
                else:
                    combined.append(new[index])
                    combined_gains.append(gains[index])
            joint = inventory(old+combined)
            assert phi_from(old+combined, joint) == 1-amount+sum(combined_gains)
            assert phi_from(old+combined, joint) >= amount-1+3*gaps.count(10)
            strengthened += 1
    return dict(one_owner_batches=checked, mixed_10_both_gate_batches=strengthened)


def isometry_controls():
    checked = 0
    width, gap, top = 20, 20, 2
    old = baseline(width, (top, top+gap), 20)
    specifications = [('D', 20, 8, 12), ('U', 20, 8, 6), ('U', 10, 8, 10),
                      ('R', 12, 4, 10), ('E', 12, 10, 10), ('E', 6, 10, 4),
                      ('H', 0, 0, 0), ('L', 0, 0, 0)]
    before = inventory(old)
    for mode, breadth, near, far in specifications:
        canonical = left_rotor(mode == 'H') if mode in ('H', 'L') else make_source(mode, breadth, near, far)
        record = shift(canonical, (top, 0))
        expected_full, expected_events = exact_receipt(mode, breadth, near, far, width, top)
        for transpose, flip_row, flip_column, offset in itertools.product(
                (False, True), (False, True), (False, True), ((0, 0), (-100, -200))):
            def move(point):
                row = 1-point[0] if flip_row else point[0]
                column = 1-point[1] if flip_column else point[1]
                if transpose:
                    row, column = column, row
                return row+offset[0], column+offset[1]
            transformed = [transform(source, move) for source in old+[record]]
            first, second = inventory(transformed[:-1]), inventory(transformed)
            moved_full = {(move((2*row, 2*column))[0]//2,
                           move((2*row, 2*column))[1]//2) for row, column in expected_full}
            moved_events = {(owner, move(point), move(target)) for owner, point, target in expected_events}
            assert second['full']-first['full'] == moved_full
            assert second['events']-first['events'] == moved_events
            assert phi_from(transformed, second)-phi_from(transformed[:-1], first) == receipt(
                mode, breadth, near, far, width)[-1]
            checked += 1
    assert phi_from(old, before) == -1
    return checked


def residual_controls():
    checked = 0
    for width, amount in itertools.product((6, 20), (0, 1, 4, 5, 20, 40)):
        rows = [2, 12]+[24+12*index for index in range(amount)]
        old = baseline(width, rows, 20)
        core = old+[shift(ten_candidate('U', width), (2, 0))]
        assert phi_from(core, inventory(core)) == 4-amount
        receivers = [shift(make_source('R', 6, 4, 4), (row, 0)) for row in rows[1:-1]]
        after = inventory(core+receivers)
        assert phi_from(core+receivers, after) == 4+amount
        checked += 1
    return checked


def large_controls():
    cases = []
    for width, gap in ((6, 2000), (2000, 12), (2000, 2000)):
        old = baseline(width, (2000, 2000+gap), 20)
        before = inventory(old)
        choices = [('D', width, gap-6, 4), ('U', width, gap-6, gap-6),
                   ('R', gap-6, width-2, 4), ('E', gap-6, width-2, width-2)]
        for mode, breadth, near, far in choices:
            canonical = make_source(mode, breadth, near, far)
            after = inventory(old+[shift(canonical, (2000, 0))])
            full, events, expected_charge, gain = receipt(mode, breadth, near, far, width)
            assert (len(after['full']-before['full']), len(after['events']-before['events'])) == (full, events)
            assert charge(canonical) == expected_charge
            assert phi_from(old+[shift(canonical, (2000, 0))], after)-phi_from(old, before) == gain >= 2
        cases.append(dict(width=width, gap=gap, four_source_types=True))
    return cases


def run():
    roles = role_controls()
    receipts, library = receipt_controls()
    return dict(status='PASS', roles=roles, receipts=receipts,
                batches=mixed_batch_controls(library), residual_repairs=residual_controls(),
                tile_preserving_isometries=isometry_controls(), large=large_controls(),
                scope='Finite full-record controls of the separate written all-even-gap source '
                      'classification and selected-inventory compensation. General proofs are '
                      'not inferred from enumeration. No complete extension existence, '
                      'nonnegative unselected-source marginal or global grid bound.')


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
