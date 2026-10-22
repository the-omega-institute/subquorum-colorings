"""Exact physical-column controls for transverse and aligned horizontal U families."""

import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_gap_axial_compensation import transform
from check_even_gap_axial_compensation import baseline, make_source
from check_incident_eight_north_transfer import charge
from check_incident_eight_north_transfer import shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_six_row_transverse_budget import inspect, pair_specs, transverse


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def horizontal(left, width, upward):
    assert left % 2 == width % 2 == 0 and width >= 6
    original = independent_source((width, 4, 4), (False, False, False), (0, 0))
    return transform(original, lambda point: (
        4-point[0] if upward else 1+point[0], left-1+point[1]))


def audit(verticals, horizontals, complete=False):
    vertical_records = [transverse(*specification) for specification in verticals]
    horizontal_records = [horizontal(*specification) for specification in horizontals]
    records = vertical_records+horizontal_records
    after = inventory(records)
    before = inventory(vertical_records) if vertical_records else dict(full=set(), events=set())
    old_value = phi_from(vertical_records, before) if vertical_records else 0
    if verticals:
        inspect(verticals)
    vertical_endpoints = set.union(*(record[0] for record in vertical_records)) if vertical_records else set()
    owners = {point: owner for owner, record in enumerate(vertical_records) for point in record[0]}
    partition_full = set()
    partition_events = set()
    gains = []
    for index, (record, specification) in enumerate(zip(horizontal_records, horizontals)):
        left, width, upward = specification
        right = left+width-1
        for other, other_specification in zip(horizontal_records, horizontals):
            if other is record:
                continue
            other_left, other_width, _ = other_specification
            assert right < other_left or other_left+other_width-1 < left
        assert charge(record) == 1-width
        extreme_row, bar_row = (5, 4) if upward else (0, 1)
        forbidden_row = 0 if upward else 5
        assert not {(forbidden_row, column) for column in range(left, right+1)} & vertical_endpoints
        bars = [(bar, bar+1) for bar, direction, near, far in verticals]
        assert all(bar_right < left or right < bar_left for bar_left, bar_right in bars)
        visitors = {owners[extreme_row, column] for column in range(left, right+1)
                    if (extreme_row, column) in owners}
        assert len(visitors) <= 2
        partial = seams = debit = 0
        expected_full = set()
        expected_events = set()
        for tile_column in range(left//2, (right+1)//2):
            columns = 2*tile_column, 2*tile_column+1
            covered = [column for column in columns if (extreme_row, column) in owners]
            current_events = set()
            for column in covered:
                point, target = (extreme_row, column), (bar_row, column)
                vertical_owner = owners[point]
                current_events.add((len(verticals)+index, target, point))
                if target not in vertical_records[vertical_owner][1]:
                    current_events.add((vertical_owner, point, target))
            if len(covered) == 2:
                expected_full.add((min(extreme_row, bar_row)//2, tile_column))
                if owners[extreme_row, columns[0]] == owners[extreme_row, columns[1]]:
                    assert len(current_events) == 3
                else:
                    seams += 1
                    assert len(current_events) <= 4
            elif covered:
                partial += 1
                assert len(current_events) <= 2
            expected_events |= current_events
            debit += len(current_events)-2*int(len(covered) == 2)
        assert partial <= 2 and seams <= 1 and not partial*seams
        assert debit <= width//2+2
        if complete:
            assert partial == 0
            assert debit <= width//2+1
            assert debit == 0
        footprint = {(row//2, column//2) for row, column in record[0]}
        actual_full = (after['full']-before['full']) & footprint
        actual_events = {event for event in after['events']-before['events']
                         if (event[1][0]//2, event[1][1]//2) in footprint}
        assert actual_full == expected_full and actual_events == expected_events
        assert not partition_full & expected_full and not partition_events & expected_events
        partition_full |= expected_full
        partition_events |= expected_events
        gain = width-1-debit
        assert gain >= width//2-3
        if complete:
            assert gain >= width//2-2
        gains.append(dict(left=left, width=width, upward=upward, visitors=len(visitors),
                          partial_columns=partial, seam_columns=seams, exact_gain=gain))
    assert partition_full == after['full']-before['full']
    assert partition_events == after['events']-before['events']
    assert phi_from(records, after)-old_value == sum(row['exact_gain'] for row in gains)
    assert phi_from(records, after) >= len(verticals)+sum(width//2-3 for left, width, up in horizontals)
    return dict(sources=len(records), Phi=phi_from(records, after), additions=gains)


def complete_controls():
    checked = mixed = 0
    blocks = [('H', 6, False), ('H', 8, True), ('V', 10, False)]
    patterns = [pattern for pattern in itertools.product(blocks, repeat=3)
                if all(first[0] != 'H' or second[0] != 'H' or first[2] == second[2]
                       for first, second in zip(pattern, pattern[1:]))]
    patterns += [(('H', width, upward),) for width, upward
                 in itertools.product((6, 20, 2000), (False, True))]
    for pattern in patterns:
        verticals, horizontals = [], []
        offset = 0
        for kind, width, upward in pattern:
            if kind == 'H':
                horizontals.append((offset, width, upward))
            else:
                verticals += pair_specs(width, 4, 4, offset)
            offset += width
        old = baseline(offset+2, (2, 12), 20)
        core = old+[shift(make_source('U', offset+2, 4, 4), (2, 0))]
        added = [transverse(*specification) for specification in verticals]
        added += [horizontal(*specification) for specification in horizontals]
        records = core+[shift(record, (4, 2)) for record in added]
        endpoints = set.union(*(record[0] for record in records))
        supports = set.union(*(record[1] for record in records))-endpoints
        occupied = endpoints | supports
        pocket = {(row, column) for row in range(4, 10) for column in range(2, offset+2)}
        assert all(len(set(neighbors(point)) & occupied) == 1 for point in supports & pocket)
        result = audit(verticals, horizontals, complete=True)
        assert result['Phi'] >= len(verticals)+len(horizontals)
        assert phi_from(records, inventory(records))-phi_from(old, inventory(old)) == 5+result['Phi']
        checked += 1
        mixed += bool(verticals and horizontals)
    return dict(locally_complete_families=checked, genuinely_mixed_complete_families=mixed)


def sharp_partial(width, left=6, upward=False):
    verticals = [(0, 1, 4, left+width-4), (left+width+4, -1, 4, 6)]
    if upward:
        verticals = [(bar, direction, far, near) for bar, direction, near, far in verticals]
    result = audit(verticals, [(left, width, upward)])
    assert result['additions'][0]['exact_gain'] == width//2-3
    return result


def boundary_owner_controls():
    from check_even_bar_contact_ledger import rotor_record
    checked = 0
    old = independent_source((6, 4, 4), (False, False, False), (0, 0))
    point = (5, 1)
    for symmetry in itertools.product((False, True), repeat=3):
        record = rotor_record(symmetry)
        for anchor in record[0]:
            moved = transform(record, lambda site: (site[0]+point[0]-anchor[0],
                                                    site[1]+point[1]-anchor[1]))
            assert (not all(0 <= row <= 5 for row, column in moved[0])
                    or moved[0] & old[0])
            checked += 1
    return checked


def main():
    generator = random.Random(20261022)
    candidates = [(('V', (bar, direction, near, far)), transverse(bar, direction, near, far))
                  for bar, direction, near, far in itertools.product(
                      range(-8, 35), (-1, 1), (4, 8), (4, 10))]
    candidates += [(('H', (left, width, upward)), horizontal(left, width, upward))
                   for left, width, upward in itertools.product(range(-4, 26, 2), (6, 8, 12), (False, True))]
    batches = mixed = 0
    for attempt in range(160):
        occupied = set()
        verticals, horizontals = [], []
        for position in generator.sample(range(len(candidates)), len(candidates)):
            (kind, specification), record = candidates[position]
            if occupied & record[0]:
                continue
            occupied |= record[0]
            (verticals if kind == 'V' else horizontals).append(specification)
        audit(verticals, horizontals)
        batches += 1
        mixed += bool(verticals and horizontals)
    sharp = [sharp_partial(width, left, upward)
             for width, left, upward in itertools.product((6, 8, 20, 2000), (6, 20), (False, True))]
    print(json.dumps(dict(status='PASS', simultaneous_families=batches,
                         genuinely_mixed_families=mixed, sharp_partial_families=len(sharp),
                         sharp_width_six=sharp[0], rotor_boundary_owner_roles=boundary_owner_controls(),
                         complete_controls=complete_controls(),
                         scope='Exact full-source accounting; arbitrary-parameter theorem is separately written. '
                         'Horizontal U projections tile-aligned, interior bar phase only; no rotors. '
                         'Complete-pocket strengthening requires inherited completeness, not asserted by '
                         'the endpoint-only sharp marginal examples.'), indent=2))


if __name__ == '__main__':
    main()
