"""Exact role, sealed-support and both east-terminal frames after the second return."""

import itertools
import json
from collections import defaultdict

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_arbitrary_t_consumers import old_chain
from check_secondary_ten_both_far_charge_separation import counts
from check_secondary_ten_both_far_compensation import originals
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def return_family(width, far):
    fixed, unused, unused, sites = old_chain(31, 0, [width, 12], [far+24]*2, 6)
    receiver, consumer = originals(sites, [width, 12], (1, 6, 0, far+2, far))
    first = independent_source((2*far+20, 4, 40),
                               (True, False, True), (2*far+42, -34))
    second = independent_source((6, 4, width+8),
                                (True, True, False), (16, width+15))
    return fixed+[receiver, consumer, first, second]


def corner_receipts(width, near, owner):
    full = {(22//2, (width+column)//2) for column in (12, 14)}
    full |= {(24//2, (width+column)//2) for column in (12, 14, 16, 18)}
    full |= {(row//2, (width+12)//2) for row in range(26, 24+near, 2)}
    events = {(source_owner, source, target)
              for column in range(width+14, width+20)
              for source_owner, source, target in (
                  (18, (25, column), (24, column)),
                  (owner, (24, column), (25, column)))}
    events |= {(source_owner, source, target)
               for row in range(24, 24+near, 2)
               for source_owner, source, target in (
                   (19, (row, width+12), (row, width+13)),
                   (owner, (row, width+13), (row, width+12)))}
    events.add((28, (22, width+14), (23, width+14)))
    events |= {(owner, (23, column), (22, column))
               for column in range(width+13, width+16)}
    return full, events


def upward_receipts(width, breadth, near, far, owner):
    full = {(11, (width+column)//2) for column in (12, 14)}
    events = {(owner, (23, width+column), (22, width+column)) for column in (13, 15)}
    events.add((28, (22, width+14), (23, width+14)))
    if breadth == 8:
        terminal = width+13+near-far
        full |= {(8, (width+column)//2) for column in (12, 14)
                 if terminal <= width+column}
        events |= {(28, (17, width+column), (16, width+column))
                   for column in (12, 14) if terminal <= width+column}
        events |= {(owner, (16, width+column), (17, width+column))
                   for column in (11, 13, 15) if terminal <= width+column}
    return full, events


def moved_receipts(full, events, translation):
    moved = lambda point: (point[0]+translation[0], point[1]+translation[1])
    return ({(row+translation[0]//2, column+translation[1]//2) for row, column in full},
            {(owner, moved(source), moved(target)) for owner, source, target in events})


def row_frontier(width, far, row):
    assert row >= 28 and row % 2 == 0
    initial = {28: (width+19, width+19), 30: (width+15, width+17),
               32: (width+16, width+16), 34: (width+14, width+14),
               36: (width+14, width+14), 38: (width+5, 11), 40: (11, 11)}
    if row in initial:
        return initial[row]
    if 42 <= row <= far+46:
        return 2, 2
    following = {48: (3, 5), 50: (4, 4), 52: (2, 2),
                 54: (2, 2), 56: (-7, -13), 58: (-13, -13)}
    if row-far in following:
        return following[row-far]
    if far+60 <= row <= 2*far+66:
        return -22, -22
    assert row >= 2*far+68
    return None, None


def role_controls():
    base = return_family(12, 4)
    occupied = set.union(*(record[0] for record in base))
    point = 23, 25
    eligible = south_exclusions = corners = terminals = 0
    for dimensions, symmetry in itertools.product(
            itertools.product((6, 8, 12, 40), (4, 6, 8, 40), (4, 6, 40)),
            itertools.product((False, True), repeat=3)):
        original = independent_source(dimensions, symmetry, (0, 0))
        for anchor in original[0]:
            internal = {(other[0]-anchor[0], other[1]-anchor[1])
                        for other in set(neighbors(anchor)) & original[0]}
            if not internal or not internal <= {(1, 0), (0, 1)}:
                continue
            record = shift(original, (point[0]-anchor[0], point[1]-anchor[1]))
            eligible += 1
            if internal == {(1, 0)}:
                assert record[0] & occupied
                south_exclusions += 1
            if record[0] & occupied:
                continue
            if internal == {(1, 0), (0, 1)}:
                right = max(column for row, column in record[0] if row == point[0])
                breadth = right-point[1]+1
                near = max(row for row, column in record[0] if column == point[1])-point[0]
                far = max(row for row, column in record[0] if column == right)-point[0]
                expected = independent_source((breadth, near, far),
                                               (False, False, False), (23, 24))
                assert record == expected and breadth >= 8 and near in (4, 6)
                corners += 1
            else:
                assert internal == {(0, 1)}
                right = max(column for row, column in record[0] if row == point[0])
                bar_rows = {row for row, column in record[0] if column == right}
                breadth = max(bar_rows)-min(bar_rows)+1
                near = right-point[1]
                upward = max(bar_rows) == point[0]
                far_row = min(bar_rows) if upward else max(bar_rows)
                far = right-min(column for row, column in record[0] if row == far_row)
                expected = independent_source((breadth, near, far),
                    (True, True, upward), (24 if upward else 22, right))
                assert record == expected
                if not upward:
                    assert near >= 8
                terminals += 1
    assert south_exclusions and corners and terminals
    return dict(eligible_U_roles=eligible, south_terminal_exclusions=south_exclusions,
                feasible_corner_normalizations=corners, east_terminal_normalizations=terminals)


def corner_controls():
    cases = rotor_roles = 0
    for width, far, breadth, near, other, translation in itertools.product(
            (12, 50, 2000), (4, 40, 2000), (8, 2000), (4, 6), (4, 2000),
            ((0, 0), (-64, -100))):
        base = [shift(record, translation) for record in return_family(width, far)]
        corner = shift(independent_source((breadth, near, other),
                       (False, False, False), (23, width+12)), translation)
        before, after = inventory(base), inventory(base+[corner])
        full, events = moved_receipts(*corner_receipts(width, near, len(base)), translation)
        assert after['full']-before['full'] == full
        assert after['events']-before['events'] == events
        assert charge(corner) == 1-breadth
        assert phi_from(base+[corner], after)-phi_from(base, before) == breadth-7
        moved = lambda point: (point[0]+translation[0], point[1]+translation[1])
        support = moved((24+near, width+13))
        occupied = set.union(*(record[0] for record in base+[corner]))
        assert support in corner[1] and support not in occupied
        contacts = {moved((23+near, width+13)), moved((24+near, width+12)),
                    moved((24+near, width+14))}
        blocker = moved((31, width+13))
        assert blocker in base[4][0]
        if near == 6:
            contacts.add(blocker)
        assert set(neighbors(support)) & occupied == contacts
        if near == 4:
            witnesses = {moved((30, width+12)), moved((30, width+14))}
            assert moved((30, width+12)) in base[19][0]
            assert moved((30, width+14)) in base[18][0]
            patterns = set()
            for symmetry in itertools.product((False, True), repeat=3):
                module = transform_module(rotor(), symmetry)
                for anchor in module['endpoints']:
                    internal = {(point[0]-anchor[0], point[1]-anchor[1])
                        for point in set(neighbors(anchor)) & module['endpoints']}
                    if internal != {(1, 0)}:
                        continue
                    endpoints = {(row-anchor[0]+support[0], column-anchor[1]+support[1])
                                 for row, column in module['endpoints']}
                    assert endpoints & witnesses
                    patterns.add(frozenset(endpoints))
            assert len(patterns) == 2
            rotor_roles += len(patterns)
        cases += 1
    return dict(exact_corner_receipt_and_nonextension_controls=cases,
                three_neighbour_gate_rotor_exclusions=rotor_roles)


def upward_controls():
    cases = collisions = exceptions = 0
    profiles = set()
    for width, old_far, translation in ((12, 4, (0, 0)), (50, 2000, (-64, -100))):
        base = [shift(record, translation) for record in return_family(width, old_far)]
        occupied = set.union(*(record[0] for record in base))
        before = inventory(base)
        for breadth, near, far in itertools.product((6, 8, 10, 2000),
                (4, 6, 8, 40, 2000), (4, 6, 10, 2000)):
            record = shift(independent_source((breadth, near, far),
                           (True, True, True), (24, width+13+near)), translation)
            allowed = breadth >= 8 or near-far >= 4
            assert allowed == (not bool(record[0] & occupied))
            if not allowed:
                collisions += 1
                continue
            assert counts(record) == (breadth-1+(near+far)//2,
                                      breadth//2+(near+far)//2, (near+far)//2)
            moved = lambda point: (24-point[1]+translation[0],
                                  width+13+near-point[0]+translation[1])
            expected_inside = {moved((near+1, 1)), moved((far+1, breadth))}
            expected_inside |= {moved((row, 2)) for row in range(3, near, 2)}
            expected_inside |= {moved((row, breadth-1)) for row in range(3, far, 2)}
            tiles = {(row//2, column//2) for row, column in record[0]}
            assert {point for point in record[1]
                    if (point[0]//2, point[1]//2) in tiles} == expected_inside
            assert charge(record) == -1
            after = inventory(base+[record])
            full, events = moved_receipts(
                *upward_receipts(width, breadth, near, far, len(base)), translation)
            assert after['full']-before['full'] == full
            assert after['events']-before['events'] == events
            exceptional = int(breadth == 8 and near-far <= 2)
            assert phi_from(base+[record], after)-phi_from(base, before) == 2-exceptional
            assert after['mass']-before['mass'] == 1
            exceptions += exceptional
            if breadth == 8:
                profiles.add('outside' if near-far >= 4 else
                             'oneEvent' if near-far == 2 else
                             'oneFull' if near-far == 0 else 'twoFull')
            cases += 1
    assert profiles == {'outside', 'oneEvent', 'oneFull', 'twoFull'}
    return dict(exact_upward_full_event_set_controls=cases, collision_controls=collisions,
                exceptional_far_receipts=exceptions, far_profiles=sorted(profiles))


def downward_controls():
    cases = collisions = table_rows = 0
    deductions = set()
    for width, old_far, translation in (
            (12, 4, (0, 0)), (50, 40, (-64, -100)), (12, 2000, (20, 200))):
        unshifted = return_family(width, old_far)
        rows = defaultdict(set)
        for record in unshifted:
            for row, column in record[0]:
                rows[row].add(column)
        for row in range(28, 2*old_far+72, 2):
            upper, lower = row_frontier(width, old_far, row)
            assert (max(rows[row]) if rows[row] else None) == upper
            assert (max(rows[row+1]) if rows[row+1] else None) == lower
            if upper is None:
                assert lower is None
            else:
                assert lower is not None and lower <= upper+2*(upper % 2)
            table_rows += 1
        base = [shift(record, translation) for record in unshifted]
        occupied = {point: owner for owner, record in enumerate(base) for point in record[0]}
        before = inventory(base)
        far_rows = set(range(28, 44, 2)) | {old_far+step for step in (46, 48, 50, 52, 54, 56, 58, 60)}
        far_rows |= {2*old_far+66, 2*old_far+68}
        moved = lambda point: (point[0]+translation[0], point[1]+translation[1])
        for row, near in itertools.product(sorted(far_rows), (4, 6, 8, 12, 40, 2000)):
            upper, lower = row_frontier(width, old_far, row)
            breadth = row-22
            bar = width+13+near
            fars = {4, 6, 2000}
            if upper is not None:
                boundary = upper+1+(upper % 2)
                fars |= {bar-boundary+step for step in (-2, 0, 2)}
            for far in sorted(value for value in fars if value >= 4):
                record = shift(independent_source((breadth, near, far),
                               (True, True, False), (22, bar)), translation)
                terminal = bar-far
                allowed = near >= 8 and (upper is None or terminal > upper)
                assert allowed == (not bool(record[0] & occupied.keys()))
                if not allowed:
                    collisions += 1
                    continue
                assert counts(record) == (breadth-1+(near+far)//2,
                    breadth//2+1+(near+far)//2, 4+(near+far)//2)
                assert charge(record) == 1
                move_source = lambda point: moved((22+point[1], bar-point[0]))
                expected_inside = {move_source((0, 0)), move_source((0, breadth+1)),
                                   move_source((near+1, 1)), move_source((far+1, breadth))}
                expected_inside |= {move_source((value, 0)) for value in range(2, near+1, 2)}
                expected_inside |= {move_source((value, breadth+1)) for value in range(2, far+1, 2)}
                tiles = {(value//2, column//2) for value, column in record[0]}
                assert {point for point in record[1]
                        if (point[0]//2, point[1]//2) in tiles} == expected_inside
                full = {(11, (width+column)//2) for column in (12, 14)}
                events = {(owner, source, target) for owner, source, target in (
                    (28, (22, width+14), (23, width+14)),
                    (len(base), (23, width+14), (22, width+14)))}
                full, events = moved_receipts(full, events, translation)
                far_events = set()
                if upper is not None and upper % 2 == 0 and terminal == upper+1:
                    source, target = moved((row, upper)), moved((row, terminal))
                    owner = occupied[source]
                    if target not in base[owner][1]:
                        far_events.add((owner, source, target))
                if upper is not None and upper % 2 == 1 and terminal == upper+2:
                    source, target = moved((row+1, terminal)), moved((row, terminal))
                    if source in occupied:
                        owner = occupied[source]
                        if target not in base[owner][1]:
                            far_events.add((owner, source, target))
                assert len(far_events) <= 1
                after = inventory(base+[record])
                assert after['full']-before['full'] == full
                assert after['events']-before['events'] == events | far_events
                assert after['mass'] == before['mass']
                assert phi_from(base+[record], after)-phi_from(base, before) == 3-len(far_events)
                deductions.add(len(far_events))
                cases += 1
    assert deductions == {0, 1}
    return dict(exact_row_frontier_controls=table_rows,
                exact_downward_full_event_set_controls=cases,
                collision_controls=collisions, far_deductions=sorted(deductions))


def main():
    print(json.dumps(dict(status='PASS', roles=role_controls(), corners=corner_controls(),
        upward=upward_controls(), downward=downward_controls(),
        scope='Finite controls supplement general written '
        'actual-east-terminal classification, arbitrary-corner complete nonextension '
        'and exact all-parameter upward/downward marginal>=1/>=2. Joint allocation and '
        'full-family/global compensation remain OPEN.'), indent=2))


if __name__ == '__main__':
    main()
