"""Exact all-phase horizontal boundary bands and complete marginal obstructions."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import rotor_record
from check_even_gap_axial_compensation import baseline, make_source, transform
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_six_row_ceiling_descent import anchored, north
from check_six_row_transverse_budget import inspect, transverse


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def horizontal(left, width, upward):
    record = north(left, width, False)
    return record if upward else transform(record, lambda point: (5-point[0], point[1]))


def audit(verticals, horizontals):
    vertical_records = [transverse(*specification) for specification in verticals]
    records = vertical_records+[horizontal(*specification) for specification in horizontals]
    after = inventory(records)
    before = inventory(vertical_records) if verticals else dict(full=set(), events=set())
    vertical_result = inspect(verticals) if verticals else dict(
        aligned=0, unaligned=0, adjacent_unaligned_pairs=0, other_events=0, Phi=0)
    endpoints_vertical = set.union(*(record[0] for record in vertical_records)) if verticals else set()
    full, events, contact_owners = set(), set(), set()
    horizontal_pairs = 0
    def add_band(first, second, column, full_rows, first_rows, second_rows):
        added_full = {(row, column//2) for row in full_rows}
        added_events = {(first, (row, column), (row, column+1)) for row in first_rows}
        added_events |= {(second, (row, column+1), (row, column)) for row in second_rows}
        assert not full & added_full and not events & added_events
        full.update(added_full)
        events.update(added_events)
    for index, (left, width, upward) in enumerate(horizontals):
        owner = len(verticals)+index
        record = records[owner]
        right = left+width-1
        assert not {point for point in endpoints_vertical if left <= point[1] <= right}
        tiles = {(row//2, column//2) for row, column in record[0]}
        inside = {point for point in record[1] if (point[0]//2, point[1]//2) in tiles}
        assert len(record[2]) == width+3
        assert len(tiles) == width+2+2*(left % 2)
        assert len(inside) == 2+4*(left % 2)
        assert charge(record) == 1-width
        full_rows = (0, 1) if upward else (1, 2)
        emitting_rows = (1, 3) if upward else (2, 4)
        side_rows = range(5) if upward else range(1, 6)
        for previous, (other_left, other_width, other_upward) in enumerate(horizontals[:index]):
            other_right = other_left+other_width-1
            assert right < other_left or other_right < left
            if other_right+1 == left or right+1 == other_left:
                assert upward == other_upward
                if left % 2:
                    first, second, column = ((len(verticals)+previous, owner, other_right)
                                            if other_right < left else
                                            (owner, len(verticals)+previous, right))
                    add_band(first, second, column, full_rows, emitting_rows, emitting_rows)
                    horizontal_pairs += 1
        for vertical_owner, (bar, direction, near, far) in enumerate(verticals):
            if bar+2 == left:
                assert direction == -1
                if left % 2:
                    assert vertical_owner not in contact_owners
                    contact_owners.add(vertical_owner)
                    add_band(vertical_owner, owner, left-1, full_rows, side_rows, emitting_rows)
            elif bar == right+1:
                assert direction == 1
                if left % 2:
                    assert vertical_owner not in contact_owners
                    contact_owners.add(vertical_owner)
                    add_band(owner, vertical_owner, right, full_rows, emitting_rows, side_rows)
    assert full == after['full']-before['full']
    assert events == after['events']-before['events']
    assert all(event[0] not in contact_owners for event in before['events'])
    contacts = len(contact_owners)
    pairs = vertical_result['adjacent_unaligned_pairs']
    aligned, odd = vertical_result['aligned'], vertical_result['unaligned']
    unspent = odd-2*pairs-contacts
    assert unspent >= 0 and vertical_result['other_events'] <= 2*unspent
    mass = sum(width-1 for left, width, upward in horizontals)
    value = phi_from(records, after)
    assert value == vertical_result['Phi']+mass-3*contacts
    assert value >= aligned+2*odd+mass+unspent
    return dict(Phi=value, vertical_Phi=vertical_result['Phi'], H_mass=mass,
                VH_bands=contacts, HH_bands=horizontal_pairs, unspent_odd_bars=unspent)


def odd_block(width, offset=0, upward=False):
    verticals = [(offset+bar, direction, near, far) for bar, direction, near, far in (
        (0, 1, 4, 4), (5, 1, 4, 4), (15, -1, 6, 6),
        (17+width, 1, 4, 4), (22+width, 1, 4, 4), (32+width, -1, 6, 6))]
    return verticals, [(offset+17, width, upward)]


def complete_controls():
    checked = 0
    witness = None
    for width, amount, upward, prefix in itertools.product(
            (6, 8, 20, 2000), (1, 2, 5), (False, True), (0, 6)):
        verticals, horizontals = [], []
        if prefix:
            horizontals.append((0, prefix, upward))
        for index in range(amount):
            added_verticals, added_horizontals = odd_block(width, prefix+(width+34)*index, upward)
            verticals += added_verticals
            horizontals += added_horizontals
        result = audit(verticals, horizontals)
        pocket_width = prefix+(width+34)*amount
        old = baseline(pocket_width+2, (2, 12), 20)
        core = old+[shift(make_source('U', pocket_width+2, 4, 4), (2, 0))]
        added = [transverse(*specification) for specification in verticals]
        added += [horizontal(*specification) for specification in horizontals]
        records = core+[shift(record, (4, 2)) for record in added]
        endpoints = set.union(*(record[0] for record in records))
        supports = set.union(*(record[1] for record in records))-endpoints
        occupied = endpoints | supports
        pocket = {(row, column) for row in range(4, 10)
                  for column in range(2, pocket_width+2)}
        assert all(len(set(neighbors(point)) & occupied) == 1 for point in supports & pocket)
        assert result['Phi'] == amount*(width+9)+(prefix-1 if prefix else 0)
        assert result['Phi']-result['vertical_Phi'] == amount*(width-7)+(prefix-1 if prefix else 0)
        assert phi_from(records, inventory(records))-phi_from(old, inventory(old)) == 5+result['Phi']
        if width == 6 and amount == 1 and not upward and not prefix:
            witness = dict(pocket_width=pocket_width, verticals=verticals,
                           horizontals=horizontals, **result)
        checked += 1
    return dict(locally_complete_families=checked, largest_H_width=2000,
                largest_batch=5, sharp_complete_witness=witness)


def rotor_edge_controls():
    originals = [independent_source(dimensions, symmetry, (0, 0))
                 for dimensions, symmetry in itertools.product(
                     itertools.product((6, 8, 14), (4, 6, 10), (4, 6, 10)),
                     itertools.product((False, True), repeat=3))]
    originals += [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    configurations = forced_roles = 0
    for upward in (False, True):
        current_H = horizontal(1, 6, upward)
        for symmetry, top in itertools.product(itertools.product((False, True), repeat=3), range(3)):
            base = rotor_record(symmetry)
            minimum_row = min(row for row, column in base[0])
            maximum_column = max(column for row, column in base[0])
            current_rotor = transform(base, lambda point: (
                point[0]-minimum_row+top, point[1]-maximum_column))
            assert not current_rotor[0] & current_H[0]
            supports = [point for point in current_H[1] if point[1] == 0
                        and point not in current_rotor[0] and (point[0], -1) in current_rotor[0]]
            assert supports
            point = supports[0]
            assert (point[0], 1) in current_H[0]
            for original in originals:
                for record in anchored(original, point):
                    if not all(0 <= row <= 5 and column <= 0 for row, column in record[0]):
                        continue
                    assert record[0] & (current_H[0] | current_rotor[0])
                    forced_roles += 1
            configurations += 1
    return dict(boundary_rotor_configurations=configurations, impossible_forced_owner_roles=forced_roles)


def band_controls():
    checked = 0
    for left, width, upward, side in itertools.product((1, 7, 21), (6, 8, 20, 2000),
                                                       (False, True), (-1, 1)):
        vertical = (left-2, -1, 4, 10) if side == -1 else (left+width, 1, 10, 4)
        result = audit([vertical], [(left, width, upward)])
        assert result['VH_bands'] == 1 and result['Phi'] == width+1
        checked += 1
    for width, upward in itertools.product((6, 8, 20, 2000), (False, True)):
        result = audit([], [(1, width, upward), (1+width, width, upward)])
        assert result['HH_bands'] == 1 and result['Phi'] == 2*(width-1)
        checked += 1
    return checked


def opposite_neighbor_obstructions():
    checked = 0
    for left, width, first_upward in itertools.product((0, 1, 10, 11), (6, 8, 20), (False, True)):
        first = horizontal(left, width, first_upward)
        second = horizontal(left+width, width, not first_upward)
        row = 5 if first_upward else 0
        point = row, left+width-1
        assert point in second[1] and point not in first[0] | second[0]
        assert (row, left+width) in second[0]
        assert left <= point[1] <= left+width-1
        checked += 1
    return checked


def main():
    print(json.dumps(dict(status='PASS', exact_band_controls=band_controls(),
                         complete_controls=complete_controls(), rotor_edge_controls=rotor_edge_controls(),
                         opposite_neighbor_obstructions=opposite_neighbor_obstructions(),
                         scope='Full canonical records and exact labelled event/tile partitions. '
                         'General source exclusions, owner injection and budget proof are written separately. '
                         'Complete witnesses are pocket-local retained-support controls, not global extensions.'), indent=2))


if __name__ == '__main__':
    main()
