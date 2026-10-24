"""Exact all-original role and receipt controls for actual short-return root owners."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_both_far_charge_separation import counts
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_next_support_east_terminal import return_family
from check_secondary_ten_north_contact_debit import inventory
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def prefix(width, far, breadth, depth, other):
    old = return_family(width, far)[:-1]
    returned = independent_source((breadth, depth, other),
                                 (True, True, True), (23, 7+depth))
    return old+[returned]


def allowed(width, return_breadth, return_depth, return_far, bar, breadth, far, left):
    assert bar % 2 == 0 and bar <= 22
    terminal = bar+far
    if not left:
        return breadth >= 8 or terminal <= 24
    if bar >= 22:
        return False
    column = width+13
    far_column = column+1-breadth
    return_bar = 7+return_depth
    return_top = 23-return_breadth
    return_terminal = return_bar-return_far
    if far_column >= return_bar+1:
        return terminal <= 22
    if bar > return_top-3:
        return False
    if far_column >= return_terminal+1:
        return terminal <= return_top-1
    return terminal <= 20 if far_column >= -34 else True


def expected_receipts(width, return_breadth, return_depth, return_far,
                      bar, breadth, far, left, owner):
    column = width+13
    full = {(row//2, column//2) for row in (24, 26, 28, 30)}
    events = {(19, (row, column-1), (row, column)) for row in (24, 26, 28, 30)}
    events |= {(owner, (row if left else row-1, column),
                (row if left else row-1, column-1)) for row in (24, 26, 28, 30)}
    terminal = bar+far
    frontier = 'rightOutside'
    if not left:
        if breadth == 6:
            frontier = 'rightRoot'
            if terminal == 24:
                events.add((18, (25, column+5), (24, column+5)))
    else:
        far_column = column+1-breadth
        return_bar = 7+return_depth
        return_top = 23-return_breadth
        return_terminal = return_bar-return_far
        if far_column >= return_bar+1:
            frontier = 'leftRepair'
            if terminal == 22:
                events.add((19, (23, far_column), (22, far_column)))
        elif far_column >= return_terminal+1:
            frontier = 'leftReturnedFar'
            if terminal == return_top-1:
                events.add((28, (return_top, far_column), (return_top-1, far_column)))
        elif far_column >= -34:
            frontier = 'leftRow22'
        else:
            frontier = 'leftOutside'
    return full, events, frontier


def role_controls():
    cases = early = normalized = rotor_cases = 0
    directions = set()
    records = prefix(12, 4, 6, 16, 4)
    occupied = set.union(*(record[0] for record in records))
    support = 25, 25
    assert support in records[18][1] and support not in occupied
    for dimensions, symmetry in itertools.product(
            itertools.product((6, 8, 14, 40), (4, 6, 8, 12, 40), (4, 6, 8, 40)),
            itertools.product((False, True), repeat=3)):
        original = independent_source(dimensions, symmetry, (0, 0))
        for anchor in original[0]:
            internal = {(point[0]-anchor[0], point[1]-anchor[1])
                        for point in set(neighbors(anchor)) & original[0]}
            if not internal or not internal <= {(-1, 0), (1, 0)}:
                continue
            candidate = shift(original, (25-anchor[0], 25-anchor[1]))
            if candidate[0] & occupied:
                continue
            cases += 1
            leg_rows = [row for row, column in candidate[0] if column == 25]
            bar, terminal = min(leg_rows), max(leg_rows)
            assert 25 <= terminal <= 30
            if terminal < 30:
                axial = terminal+1, 25
                assert axial in candidate[1] and axial not in occupied | candidate[0]
                assert {(terminal, 25), (terminal+1, 24), (terminal+1, 26)} <= (
                    set(neighbors(axial)) & (occupied | candidate[0]))
                early += 1
                continue
            assert bar <= 22 and bar % 2 == 0
            bar_columns = [column for row, column in candidate[0] if row == bar]
            leftmost, rightmost = min(bar_columns), max(bar_columns)
            left = rightmost == 25
            assert left or leftmost == 25
            breadth = rightmost-leftmost+1
            far_column = leftmost if left else rightmost
            far = max(row for row, column in candidate[0] if column == far_column)-bar
            expected = independent_source((breadth, 30-bar, far),
                                         (False, False, left), (bar, 26 if left else 24))
            assert candidate == expected
            assert allowed(12, 6, 16, 4, bar, breadth, far, left)
            directions.add(left)
            normalized += 1
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        for anchor in module['endpoints']:
            internal = {(point[0]-anchor[0], point[1]-anchor[1])
                        for point in set(neighbors(anchor)) & module['endpoints']}
            if not internal or not internal <= {(-1, 0), (1, 0)}:
                continue
            endpoints = {(row-anchor[0]+25, column-anchor[1]+25)
                         for row, column in module['endpoints']}
            assert endpoints & occupied
            rotor_cases += 1
    assert directions == {False, True} and early
    return dict(endpoint_disjoint_U_roles=cases, forbidden_early_tips=early,
                exact_full_record_normalizations=normalized, rotor_exclusions=rotor_cases)


def receipt_controls():
    cases = collisions = 0
    profiles = set()
    deductions = set()
    for width, old_far, return_breadth, return_depth, return_far in (
            (12, 4, 6, 4, 4), (12, 40, 10, 16, 40), (50, 4, 8, 20, 6)):
        records = prefix(width, old_far, return_breadth, return_depth, return_far)
        occupied = set.union(*(record[0] for record in records))
        before = inventory(records)
        column = width+13
        old_bottom_event = (4, (31, column), (31, column-1))
        assert old_bottom_event in before['events']
        return_bar = 7+return_depth
        return_top = 23-return_breadth
        return_terminal = return_bar-return_far
        bars = {22, 20, 18, 16, return_top-1, return_top-3, return_top-5, -40}
        breadths = {6, 8, 14, 40, 2000}
        breadths |= {column+1-value for value in (
            return_bar+1, return_bar-1, return_terminal+1, return_terminal-1, -34, -36)}
        breadths = {value for value in breadths if value >= 6 and value % 2 == 0}
        for bar, breadth, left in itertools.product(sorted(bars), sorted(breadths), (False, True)):
            fars = {4, 6, 40, 2000}
            fars |= {target-bar+offset for target in (24, 22, 20, return_top-1)
                     for offset in (-2, 0, 2)}
            for far in sorted(value for value in fars if value >= 4 and value % 2 == 0):
                candidate = independent_source((breadth, 30-bar, far),
                    (False, False, left), (bar, column+1 if left else column-1))
                legal = allowed(width, return_breadth, return_depth, return_far,
                                bar, breadth, far, left)
                assert legal == (not bool(candidate[0] & occupied)), (
                    width, return_breadth, return_depth, return_far, bar, breadth, far, left)
                if not legal:
                    collisions += 1
                    continue
                after = inventory(records+[candidate])
                assert old_bottom_event in after['events']
                full, events, profile = expected_receipts(width, return_breadth,
                    return_depth, return_far, bar, breadth, far, left, len(records))
                assert after['full']-before['full'] == full
                assert after['events']-before['events'] == events
                legs = (30-bar+far)//2
                expected_counts = (breadth-1+legs,
                    breadth//2+legs+int(not left), legs+4*int(not left))
                assert counts(candidate) == expected_counts
                assert charge(candidate) == (-1 if left else 1)
                deduction = len(events)-8
                assert deduction in (0, 1)
                assert phi_from(records+[candidate], after)-phi_from(records, before) == 1-deduction
                assert phi_from(records+[candidate], after) >= width//2+34
                profiles.add(profile)
                deductions.add(deduction)
                cases += 1
    assert profiles == {'rightOutside', 'rightRoot', 'leftRepair',
                        'leftReturnedFar', 'leftRow22', 'leftOutside'}
    assert deductions == {0, 1}
    return dict(exact_full_event_set_controls=cases, collision_controls=collisions,
                frontier_profiles=sorted(profiles), far_deductions=sorted(deductions))


def stress_controls():
    width = 2000
    records = prefix(width, 2000, 2000, 2004, 2000)
    before = inventory(records)
    column, return_top = width+13, 23-2000
    manifests = [(22, 8, 2000, False), (20, 6, 4, False),
                 (return_top-5, 6, 4, True),
                 (return_top-3, column+37, 2000, True)]
    for bar, breadth, far, left in manifests:
        candidate = independent_source((breadth, 30-bar, far),
            (False, False, left), (bar, column+1 if left else column-1))
        assert allowed(width, 2000, 2004, 2000, bar, breadth, far, left)
        after = inventory(records+[candidate])
        full, events, unused = expected_receipts(width, 2000, 2004, 2000,
                                                bar, breadth, far, left, len(records))
        assert after['full']-before['full'] == full
        assert after['events']-before['events'] == events
        assert phi_from(records+[candidate], after)-phi_from(records, before) == 9-len(events)
    return dict(large_width_height_and_far_controls=len(manifests))


def main():
    print(json.dumps(dict(status='PASS', roles=role_controls(), receipts=receipt_controls(),
        stress=stress_controls(), scope='Finite controls supplement the all-parameter '
        'actual root-owner normalization and exact1-delta>=0 proof in the stated '
        'full U/rotor model. No complete extension existence/global claim.'), indent=2))


if __name__ == '__main__':
    main()
