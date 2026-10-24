"""Exact controls for terminal one-source closure and exterior obstructions."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records
from check_even_gap_axial_compensation import make_source, transform
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_six_row_all_phase_horizontal import horizontal, odd_block
from check_six_row_rotor_exclusion import normalized
from check_six_row_transverse_budget import transverse
from check_spanning_chamber_global_caps import verify_whole


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def terminal_core(width, gaps, left_depth, right_depth, modes=None):
    rows = tuple(2+10*index for index in range(gaps+1))
    assert min(left_depth, right_depth) >= rows[-1]+6
    modes = ('U',)*gaps if modes is None else modes
    assert len(modes) == gaps
    records = [independent_source((width+2, left_depth, right_depth),
                                  (False, False, False), (0, -1))]
    records += [shift(independent_source((width, 4, 4), (False, False, False), (0, 0)),
                      (row, 0)) for row in rows]
    records += [shift(make_source(mode, width, 4, 4), (row, 0))
                for row, mode in zip(rows, modes)]
    return records


def cap(width, depth, last_bar=2):
    original = independent_source((width, depth, depth), (False, False, False), (0, 0))
    return transform(original, lambda point: (last_bar+depth+5-point[0], point[1]))


def is_complete(records):
    endpoints = set.union(*(record[0] for record in records))
    if len(endpoints) != sum(len(record[0]) for record in records):
        return False
    supports = set.union(*(record[1] for record in records))-endpoints
    occupied = endpoints | supports
    return all(len(set(neighbors(point)) & occupied) == 1 for point in supports)


def signature(record):
    return tuple(frozenset(part) for part in record)


def gate_library(width):
    result = {}
    point, other = (7, 1), (7, width)
    for breadth, near, far, symmetry in itertools.product(
            range(6, width+6, 2), range(4, 16, 2), range(4, 16, 2),
            itertools.product((False, True), repeat=3)):
        original = independent_source((breadth, near, far), symmetry, (0, 0))
        for record in anchor_records(original, point, {(0, 1), (1, 0)}):
            if other in record[0]:
                result[signature(record)] = record
    for reflected in (False, True):
        for record in anchor_records(normalized(reflected), point, {(0, 1), (1, 0)}):
            assert other not in record[0]
    return list(result.values())


def single_source_controls():
    candidates = complete = excluded_downward = short_tails = 0
    for width in (6, 8, 12, 20):
        library = gate_library(width)
        upward = {signature(cap(width, depth)): depth for depth in range(4, 16, 2)}
        downward = {signature(shift(independent_source((width, near, far),
                                                       (False, False, False), (0, 0)),
                                     (7, 0)))
                    for near, far in itertools.product(range(4, 16, 2), repeat=2)}
        for left_extra, right_extra in itertools.product((6, 8, 10, 12, 18, 24), repeat=2):
            left_depth, right_depth = 2+left_extra, 2+right_extra
            fixed = terminal_core(width, 0, left_depth, right_depth)
            endpoints = set.union(*(record[0] for record in fixed))
            found = 0
            for record in library:
                if record[0] & endpoints:
                    continue
                key = signature(record)
                assert key in upward or key in downward
                valid = is_complete(fixed+[record])
                expected = key in upward and min(left_extra, right_extra) >= upward[key]+6
                assert valid == expected
                if key in downward:
                    assert not valid
                    excluded_downward += 1
                if valid:
                    assert verify_whole(fixed+[record])-phi_from(fixed, inventory(fixed)) == 5
                    found += 1
                    complete += 1
                candidates += 1
            if min(left_extra, right_extra) < 10:
                assert found == 0
                short_tails += 1
    return dict(endpoint_disjoint_gate_candidates=candidates,
                complete_single_caps=complete, excluded_downward_candidates=excluded_downward,
                short_tail_no_single_source_controls=short_tails,
                finite_dimensions='breadth6..W+4, independent even depths4..14, all8isometries')


def cap_receipt_controls():
    checked = 0
    for width, gaps, depth in itertools.product((6, 8, 20, 2000), (0, 1, 4), (4, 6, 20)):
        last = 2+10*gaps
        modes = tuple('D' if index % 2 else 'U' for index in range(gaps))
        for left_extra, right_extra in ((0, 0), (0, 8), (12, 0)):
            left_depth = last+depth+6+left_extra
            right_depth = last+depth+6+right_extra
            fixed = terminal_core(width, gaps, left_depth, right_depth, modes)
            record = cap(width, depth, last)
            before, after = inventory(fixed), inventory(fixed+[record])
            assert len(after['full']-before['full']) == depth+2
            assert len(after['events']-before['events']) == 2*depth
            assert charge(record) == 1
            value = verify_whole(fixed+[record])
            assert value == 4*gaps+(width-4)*modes.count('D')+5
            endpoint_union = set.union(*(source[0] for source in fixed+[record]))
            retained = record[1]-endpoint_union
            expected = {(row, column) for row in range(last+6, last+depth+3, 2)
                        for column in (2, width-1)}
            assert retained == expected
            checked += 1
    return checked


def connected(records):
    endpoints = set.union(*(record[0] for record in records))
    root = next(iter(endpoints))
    reached, pending = {root}, [root]
    while pending:
        point = pending.pop()
        added = (set(neighbors(point)) & endpoints)-reached
        reached.update(added)
        pending.extend(added)
    return reached == endpoints


def anchored_negative_controls():
    checked, witness = 0, None
    for breadth, amount, upward in itertools.product((6, 8, 20), (1, 2, 5), (False, True)):
        width = amount*(breadth+34)+2
        fixed = terminal_core(width, 0, 12, 12)
        core = fixed+[cap(width, 4)]
        verticals, horizontals = [], []
        for index in range(amount):
            specs, horizontal_specs = odd_block(breadth, index*(breadth+34), upward)
            verticals += [shift(transverse(*spec), (4, 2)) for spec in specs]
            horizontals += [shift(horizontal(*spec), (4, 2)) for spec in horizontal_specs]
        before, after = core+verticals, core+verticals+horizontals
        first, second = verify_whole(before), verify_whole(after)
        assert first == 5+16*amount
        assert second == 5+(breadth+9)*amount
        assert second-first == amount*(breadth-7)
        assert connected(before) and connected(after)
        if breadth == 6 and amount == 1 and not upward:
            witness = dict(width=width, before_Phi=first, after_Phi=second,
                           both_whole_complete=True, both_endpoint_connected=True,
                           all_new_sources_exterior=True)
        checked += 1
    return dict(complete_connected_exterior_pairs=checked, witness=witness)


def amplification_controls():
    base = terminal_core(6, 0, 12, 12)+[cap(6, 4)]
    fixtures = [normalized(False), normalized(True)]
    fixtures += [independent_source((6, 4, 4), symmetry, (0, 0))
                 for symmetry in itertools.product((False, True), repeat=3)]
    checked = 0
    zero_rotor = 0
    for record in fixtures:
        minimum_row = min(row for row, column in record[0] | record[1])
        minimum_column = min(column for row, column in record[0] | record[1])
        row_shift, column_shift = 2-2*(minimum_row//2), 2-2*(minimum_column//2)
        record = shift(record, (row_shift, column_shift))
        own_value = verify_whole([record])
        for amount in (0, 1, 6, 20):
            records = list(base)
            maximum = max(column for row, column in record[0] | record[1])
            minimum = min(column for row, column in record[0] | record[1])
            stride = maximum-minimum+8
            stride += stride % 2
            for index in range(amount):
                records.append(shift(record, (0, 40+stride*index)))
            assert verify_whole(records) == 5+amount*own_value
            if len(record[2]) == 4 and own_value == 0:
                zero_rotor += 1
            checked += 1
    return dict(separated_copy_controls=checked, zero_charge_rotor_controls=zero_rotor,
                negative_complete_fusion_asserted=False)


def main():
    print(json.dumps(dict(status='PASS', singles=single_source_controls(),
                         cap_receipts=cap_receipt_controls(),
                         anchored_exterior=anchored_negative_controls(),
                         amplification=amplification_controls(),
                         scope='Exact finite source/support/matching controls for separate general '
                         'proofs. No enumeration proves unrestricted exterior sign. The bounded '
                         'exterior-to-global-source implication does not exhibit a negative complete '
                         'source inventory or refute the grid target.'), indent=2))


if __name__ == '__main__':
    main()
