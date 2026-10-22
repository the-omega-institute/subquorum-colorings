"""Whole retained-support realizations with a bottom upward-U cap."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_even_gap_axial_compensation import baseline, make_source
from check_incident_eight_north_transfer import shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_six_row_all_phase_horizontal import horizontal, odd_block
from check_six_row_transverse_budget import pair_specs, transverse


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def capped(width, modes, extra):
    rows = tuple(2+10*index for index in range(len(modes)+1))
    records = baseline(width, rows, extra)
    records += [shift(make_source(mode, width, 4, 4), (row, 0))
                for row, mode in zip(rows, modes)]
    records.append(shift(make_source('U', width, 4, 4), (rows[-1], 0)))
    return records


def verify_whole(records):
    endpoints = set.union(*(record[0] for record in records))
    assert len(endpoints) == sum(len(record[0]) for record in records)
    supports = set.union(*(record[1] for record in records))-endpoints
    occupied = endpoints | supports
    assert all(len(set(neighbors(point)) & occupied) == 1 for point in supports)
    assert all(len(set(neighbors(point)) & occupied) >= 3 for point in endpoints)
    matching = set.union(*(record[2] for record in records))
    assert len(endpoints) == 2*len(matching)
    moved = [shift(record, (2, 2)) for record in records]
    full = set.union(*(record[0] | record[1] for record in moved))
    height = max(row for row, column in full)+3
    height += height % 2
    width = max(column for row, column in full)+3
    width += width % 2
    assert all(0 <= row < height and 0 <= column < width for row, column in full)
    potential = phi_from(records, inventory(records))
    assert phi_from(moved, inventory(moved)) == potential
    return potential


def plain_controls():
    patterns = [modes for amount in range(4)
                for modes in itertools.product(('D', 'U'), repeat=amount)]
    patterns += [('U',)*20, ('D', 'U')*10]
    checked = 0
    for width, modes, extra in itertools.product((6, 8, 12, 20, 2000), patterns, (6, 20)):
        records = capped(width, modes, extra)
        expected = 4*len(modes)+(width-4)*modes.count('D')+5
        assert verify_whole(records) == expected
        checked += 1
    return checked


def negative_marginal_controls():
    checked = 0
    witness = None
    for breadth, amount, upward in itertools.product((6, 8, 20), (1, 2, 5), (False, True)):
        width = amount*(breadth+34)+2
        core = capped(width, ('U',), 6)
        verticals, horizontals = [], []
        for index in range(amount):
            added_verticals, added_horizontals = odd_block(
                breadth, index*(breadth+34), upward)
            verticals += added_verticals
            horizontals += added_horizontals
        vertical_records = [shift(transverse(*specification), (4, 2))
                            for specification in verticals]
        horizontal_records = [shift(horizontal(*specification), (4, 2))
                              for specification in horizontals]
        before = core+vertical_records
        after = before+horizontal_records
        before_value = verify_whole(before)
        after_value = verify_whole(after)
        before_endpoints = set.union(*(record[0] for record in before))
        before_supports = set.union(*(record[1] for record in before))-before_endpoints
        expected_inside = {(row+4, column+2+index*(breadth+34))
                           for index in range(amount) for row in (1, 4)
                           for column in (3, 8, 11, 13, breadth+20, breadth+25,
                                          breadth+28, breadth+30)}
        pocket_supports = {point for point in before_supports
                           if 4 <= point[0] <= 9 and 2 <= point[1] < width}
        assert pocket_supports == expected_inside
        after_endpoints = set.union(*(record[0] for record in after))
        after_supports = set.union(*(record[1] for record in after))-after_endpoints
        expected_horizontal = {((1 if upward else 4)+4,
                                column+2+index*(breadth+34))
                               for index in range(amount)
                               for column in (18, breadth+15)}
        after_pocket_supports = {point for point in after_supports
                                 if 4 <= point[0] <= 9 and 2 <= point[1] < width}
        assert after_pocket_supports == expected_inside | expected_horizontal
        assert before_value == 9+16*amount
        assert after_value == 9+(breadth+9)*amount
        assert after_value-before_value == amount*(breadth-7)
        if breadth == 6 and amount == 1 and not upward:
            witness = dict(width=width, old_sources=len(core), added_V=len(verticals),
                           added_H=len(horizontals), before_Phi=before_value,
                           after_Phi=after_value, all_before_supports_degree_one=True,
                           all_after_supports_degree_one=True)
        checked += 1
    return dict(whole_complete_families=checked, both_complete_families=checked,
                exact_before_support_lists=checked, exact_after_support_lists=checked,
                sharp_complete_witness=witness)


def sharp_pocket_controls():
    checked = 0
    for width, modes in itertools.product((12, 14, 20, 2000),
                                           (('U',), ('D', 'U'), ('U', 'D', 'U'))):
        records = capped(width, modes, 6)
        pocket_width = width-2
        for index, mode in enumerate(modes):
            if mode == 'U':
                records += [shift(transverse(*specification), (4+10*index, 2))
                            for specification in pair_specs(pocket_width, 4, pocket_width-6)]
        expected = 4*len(modes)+(width-4)*modes.count('D')+5+2*modes.count('U')
        assert verify_whole(records) == expected
        checked += 1
    return checked


def main():
    print(json.dumps(dict(status='PASS', plain_capped_cores=plain_controls(),
                         negative_H_marginals=negative_marginal_controls(),
                         sharp_nonempty_pocket_realizations=sharp_pocket_controls(),
                         scope='All original retained supports checked globally, not only a pocket; '
                         'endpoint degrees and disjoint matching coverage checked, with even ambient '
                         'embedding and exact full inventory. Separate all-parameter cap/gluing proof '
                         'does not rely on finite enumeration. Both BEFORE and AFTER are verified '
                         'complete for every negative-marginal control; the exact BEFORE pocket '
                         'support list is checked separately.'), indent=2))


if __name__ == '__main__':
    main()
