"""Exact controls for complete ten-row chambers and an excluded partial chain."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import rotor_record
from check_even_gap_axial_compensation import baseline, make_source, transform
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_ten_row_gate_compensation import checked_pairs
from check_wide_gate_escape_compensation import signature
from check_wide_gate_rotor_compensation import left_rotor, mirror


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def pocket_rotors():
    first = shift(rotor_record((False, False, False)), (-1, -1))
    second = transform(first, lambda point: (point[0], 3-point[1]))
    return [shift(record, (top, 0)) for top in range(3) for record in (first, second)]


def occupied_border():
    return {(row, column) for row in (-1, 6) for column in range(-1, 5)} | {
        (row, column) for row in range(-1, 7) for column in (-1, 4)}


def pocket_controls():
    records = pocket_rotors()
    expected = {(0, 1), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (3, 2)}
    assert records[0][0] == expected
    orbit = set()
    for symmetry in itertools.product((False, True), repeat=3):
        original = rotor_record(symmetry)
        top = min(row for row, column in original[0])
        left = min(column for row, column in original[0])
        for row in range(3):
            orbit.add(signature(shift(original, (row-top, -left))))
    assert orbit == {signature(record) for record in records}
    witnesses = ((0, 0), (0, 0), (0, 1), (0, 2), (2, 0), (2, 0))
    own = ((0, 1), (1, 0), (1, 1), (1, 2), (2, 1), (3, 0))
    boundary = ((-1, 0), (-1, 0), (-1, 1), (-1, 2), (2, -1), (2, -1))
    for record, point, anchor, blocker in zip(records, witnesses, own, boundary):
        assert point in record[1]-record[0]
        assert anchor in record[0] and blocker in occupied_border()
        assert anchor != blocker and {anchor, blocker} <= set(neighbors(point))
        assert all(0 <= row <= 5 and 0 <= column <= 3 for row, column in record[0])
    pair_table = ((1, 0, (1, 1)), (2, 0, (1, 1)), (2, 1, (1, 1)),
                  (3, 0, (1, 2)), (3, 1, (1, 2)), (3, 2, (2, 1)),
                  (4, 0, (2, 1)), (4, 1, (2, 1)), (4, 2, (2, 1)),
                  (4, 3, (3, 1)), (5, 0, (2, 2)), (5, 1, (2, 2)),
                  (5, 2, (2, 2)), (5, 3, (2, 2)), (5, 4, (3, 1)))
    for first, second, point in pair_table:
        assert point in records[first][0] & records[second][0]
    assert left_rotor(True)[0] & mirror(left_rotor(True), 6)[0] == {(4, 3), (4, 4)}
    choices = checked_pairs(6)
    assert len(choices) == 2
    assert {(signature(records[0]), gain) for records, gain in choices} == {
        (signature(make_source('D', 6, 4, 4)), 7),
        (signature(make_source('U', 6, 4, 4)), 5)}
    return dict(fixed_rotor_records=6, complete_dihedral_images=24,
                pair_intersections=15, support_witnesses=6, full_gate_states=2)


def source_span_controls():
    checked = 0
    for size, symmetry in itertools.product(
            ((6, 4, 4), (8, 6, 4), (6, 4, 8), (2000, 4, 4), (6, 2000, 4)),
            itertools.product((False, True), repeat=3)):
        record = independent_source(size, symmetry, (0, 0))
        height = max(row for row, column in record[0])-min(row for row, column in record[0])+1
        width = max(column for row, column in record[0])-min(column for row, column in record[0])+1
        assert height >= 5 and width >= 5
        checked += 1
    for symmetry in itertools.product((False, True), repeat=3):
        record = rotor_record(symmetry)
        assert max(row for row, column in record[0])-min(row for row, column in record[0]) == 3
        checked += 1
    return checked


def chamber_controls():
    checked = 0
    for width, top, extra in itertools.product((6, 8, 12, 40, 2000), (2, 40), (0, 20)):
        old = baseline(width, (top, top+10), extra)
        old_endpoints = set.union(*(record[0] for record in old))
        chamber = {(row, column) for row in range(top+2, top+10)
                   for column in range(1, width+1)}
        for mode in ('D', 'U'):
            selected = shift(make_source(mode, width, 4, 4), (top, 0))
            endpoints = old_endpoints | selected[0]
            if mode == 'D':
                expected = {(row, column) for row in (*range(top+2, top+5), *range(top+7, top+10))
                            for column in range(2, width)}
            else:
                expected = {(row, column) for row in range(top+2, top+8) for column in range(2, width)}
            assert chamber-endpoints == expected
            records = old+[selected]
            supports = set.union(*(record[1] for record in records))-endpoints
            occupied = endpoints | supports
            assert all(len(set(neighbors(point)) & occupied) == 1 for point in supports & chamber)
            gain = phi_from(records, inventory(records))-phi_from(old, inventory(old))
            assert gain == (width+1 if mode == 'D' else 5)
            if mode == 'U':
                tiles = {(row//2, column//2) for row, column in expected}
                assert not tiles & {(row//2, column//2) for row, column in endpoints}
            checked += 1
    return checked


def batch_controls():
    checked = 0
    for amount in (2, 3, 6, 12, 40):
        for top, pattern in itertools.product((2, 40), range(8)):
            rows = [top+10*index for index in range(amount)]
            old = baseline(6, rows, 20)
            modes = ['D' if (index+pattern) % 3 == 0 else 'U' for index in range(amount-1)]
            records = old+[shift(make_source(mode, 6, 4, 4), (row, 0))
                           for mode, row in zip(modes, rows)]
            assert phi_from(records, inventory(records)) == 4*(amount-1)+2*modes.count('D')
            checked += 1
    return checked


def rotor_chain_controls():
    checked = exact_events = 0
    first = pocket_rotors()[0]
    for amount, top in itertools.product((1, 2, 3, 6, 12, 40, 200), (2, 40)):
        width = 3*amount+3+(3*amount+3) % 2
        old = baseline(width, (top, top+10), 20)
        spanning = shift(make_source('U', width, 4, 4), (top, 0))
        fixed = old+[spanning]
        rotors = [shift(first, (top+2, 2+3*index)) for index in range(amount)]
        records = fixed+rotors
        before, after = inventory(fixed), inventory(records)
        expected_events = set()
        for index in range(amount-1):
            if index % 2 == 0:
                point, target = (top+4, 4+3*index), (top+4, 5+3*index)
                owner = 4+index
            else:
                point, target = (top+3, 6+3*index), (top+3, 5+3*index)
                owner = 5+index
            expected_events.add((owner, point, target))
        assert after['events']-before['events'] == expected_events
        assert after['full'] == before['full']
        assert all(charge(record) == 0 for record in rotors)
        for index, record in enumerate(rotors):
            tile_count = len({(row//2, column//2) for row, column in record[0]})
            inside = sum((row//2, column//2) in {(first//2, second//2) for first, second in record[0]}
                         for row, column in record[1])
            assert (len(record[2]), tile_count, inside) == (4, 4, 4)
        assert phi_from(records, after) == 5-amount
        if amount >= 2:
            endpoints = set.union(*(record[0] for record in records))
            point = top+2, 5
            assert point in rotors[0][1] and point not in endpoints
            assert set(neighbors(point)) & endpoints == {(top+1, 5), (top+2, 6), (top+3, 5)}
            assert (top+2, 3) in rotors[0][0]
        exact_events += len(expected_events)
        checked += 1
    return dict(chains=checked, exact_source_labelled_events=exact_events,
                longest_chain=200, most_negative_partial_Phi=-195)


def terminal_controls():
    checked = 0
    library = [independent_source(size, symmetry, (0, 0))
               for size, symmetry in itertools.product(
                   ((6, 4, 4), (8, 6, 4), (6, 4, 8), (2000, 4, 4)),
                   itertools.product((False, True), repeat=3))]
    library += [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    for record in library:
        for point in record[0]:
            internal = set(neighbors(point)) & record[0]
            if len(internal) == 1:
                target = next(iter(internal))
                second = 2*target[0]-point[0], 2*target[1]-point[1]
                assert second in record[0]
                checked += 1
    return checked


def multigap_chain_controls():
    checked = 0
    rotor = pocket_rotors()[0]
    for gaps, amount, top in itertools.product((1, 2, 5), (1, 2, 8), (2, 40)):
        width = 3*amount+3+(3*amount+3) % 2
        rows = [top+10*index for index in range(gaps+1)]
        old = baseline(width, rows, 20)
        core = old+[shift(make_source('U', width, 4, 4), (top, 0))]
        records = core+[shift(rotor, (top+2, 2+3*index)) for index in range(amount)]
        assert phi_from(old, inventory(old)) == -gaps
        assert phi_from(records, inventory(records)) == 6-gaps-amount
        assert phi_from(records, inventory(records))-phi_from(old, inventory(old)) == 6-amount
        checked += 1
    return checked


def nonempty_upward_pocket_control():
    width, top = 12, 2
    fixed = baseline(width, (top, top+10), 20)+[
        shift(make_source('U', width, 4, 4), (top, 0))]
    additions = [shift(independent_source((6, 4, 4), symmetry, offset), (top+2, 2))
                 for symmetry, offset in (((True, False, True), (6, 0)),
                                          ((True, True, True), (6, 9)))]
    records = fixed+additions
    before, after = inventory(fixed), inventory(records)
    endpoints = set.union(*(record[0] for record in records))
    supports = set.union(*(record[1] for record in records))-endpoints
    occupied = endpoints | supports
    chamber = {(row, column) for row in range(top+2, top+10) for column in range(1, width+1)}
    assert all(len(set(neighbors(point)) & occupied) == 1 for point in supports & chamber)
    assert all(charge(record) == -1 for record in additions)
    assert before['full'] == after['full'] and before['events'] == after['events']
    assert phi_from(records, after)-phi_from(fixed, before) == 2
    return dict(width=12, additional_rotated_U_sources=2, exact_marginal=2,
                locally_complete_retained_supports=True, global_extension_not_asserted=True)


def main():
    print(json.dumps(dict(status='PASS', source_spans=source_span_controls(),
                         width_six_pocket=pocket_controls(), complete_core_states=chamber_controls(),
                         simultaneous_full_chambers=batch_controls(), negative_chain=rotor_chain_controls(),
                         multigap_chain_baselines=multigap_chain_controls(),
                         terminal_continuations=terminal_controls(),
                         nonempty_upward_pocket=nonempty_upward_pocket_control(),
                         scope='Exact canonical T/H/M controls of separately written unbounded spanning-D '
                         'closure, width-six full-chamber classification, physical nonreuse and excluded '
                         'partial-chain obstruction. No full exterior sign or arbitrary-width upward-pocket '
                         'inequality is inferred.'), indent=2))


if __name__ == '__main__':
    main()
