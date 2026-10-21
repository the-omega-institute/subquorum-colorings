"""Exact original-source controls for the root and its forced bar-support owner."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_both_far_charge_separation import counts
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_short_return_root_compensation import prefix
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def baseline(width, old_far, length, other, root_bar, root_width, root_far):
    records = prefix(width, old_far, length, width+4, other)
    column = width+13
    root = independent_source((root_width, 30-root_bar, root_far),
                             (False, False, False), (root_bar, column-1))
    return records, root


def allowed(width, length, other, root_bar, root_width, bar, breadth, far, west):
    if bar > 18 or bar % 2 or breadth < 6 or breadth % 2 or far < 4 or far % 2:
        return False
    terminal = bar+far
    if not west:
        if bar > root_bar-2:
            return False
        if breadth <= root_width:
            return terminal <= root_bar-2
        if breadth == root_width+2 and root_width == 6:
            return terminal <= 24
        return True
    top = 23-length
    if bar > top-3:
        return False
    far_column = width+13-breadth
    old_terminal = width+11-other
    if far_column >= old_terminal:
        return terminal <= top-1
    return terminal <= 20 if far_column >= -33 else True


def expected_receipts(width, root_bar, root_width, root_far,
                      bar, breadth, far, west, root_owner, owner):
    column = width+13
    start = max(root_bar, bar)
    full = {(row//2, (column-1)//2) for row in range(start, 23, 2)}
    events = {(root_owner, (row, column), (row, column-1))
              for row in range(start+1, 22, 2)}
    events |= {(owner, (row, column-1), (row, column))
               for row in range(start+int(west), 23-int(west), 2)}
    events.add((19, (23, column-1), (22, column-1)))
    adjacent = (not west and breadth == root_width+2 and bar+far >= root_bar)
    cap = (not west and root_width == 6 and breadth == 8 and bar+far == 24)
    triple = cap and root_bar+root_far == 24
    if adjacent:
        right = column+root_width-1
        stop = min(root_bar+root_far, bar+far)
        full |= {(row//2, right//2) for row in range(root_bar, stop, 2)}
        events |= {(root_owner, (row, right), (row, right+1))
                   for row in range(root_bar+1, stop, 2)}
        events |= {(owner, (row, right+1), (row, right))
                   for row in range(root_bar, stop+1, 2)}
    if cap:
        events.add((18, (25, column+6), (24, column+6)))
    if triple:
        full.add((12, (column+5)//2))
    return full, events, tuple(map(int, (adjacent, cap, triple)))


def role_controls():
    records, root = baseline(12, 4, 6, 4, 18, 6, 4)
    occupied = set.union(*(record[0] for record in records+[root]))
    support = 22, 24
    assert support in root[1] and support not in occupied
    assert set(neighbors(support)) & occupied == {(22, 23), (22, 25), (23, 24)}
    roles = normalized = rotor_exclusions = 0
    orientations = set()
    for dimensions, symmetry in itertools.product(
            itertools.product((6, 8, 14, 40), (4, 6, 8, 40), (4, 6, 8, 40)),
            itertools.product((False, True), repeat=3)):
        original = independent_source(dimensions, symmetry, (0, 0))
        for anchor in original[0]:
            if {point for point in neighbors(anchor) if point in original[0]} != {
                    (anchor[0]-1, anchor[1])}:
                continue
            roles += 1
            candidate = shift(original, (22-anchor[0], 24-anchor[1]))
            if candidate[0] & occupied:
                continue
            bar = min(row for row, column in candidate[0] if column == 24)
            bar_columns = [column for row, column in candidate[0] if row == bar]
            west = max(bar_columns) == 24
            breadth = max(bar_columns)-min(bar_columns)+1
            far_column = min(bar_columns) if west else max(bar_columns)
            far = max(row for row, column in candidate[0] if column == far_column)-bar
            expected = independent_source((breadth, 22-bar, far),
                (False, False, west), (bar, 25 if west else 23))
            assert expected == candidate
            assert allowed(12, 6, 4, 18, 6, bar, breadth, far, west)
            orientations.add(west)
            normalized += 1
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        for anchor in module['endpoints']:
            if set(neighbors(anchor)) & module['endpoints'] != {(anchor[0]-1, anchor[1])}:
                continue
            endpoints = {(row-anchor[0]+22, column-anchor[1]+24)
                         for row, column in module['endpoints']}
            assert (20, 23) in endpoints & occupied
            rotor_exclusions += 1
    assert orientations == {False, True}
    return dict(U_roles=roles, exact_record_normalizations=normalized,
                rotor_exclusions=rotor_exclusions)


def receipt_controls():
    cases = collisions = negative = zero_pairs = triple_cases = 0
    marginal_values = set()
    profiles = set()
    frames = [(12, 4, 6, 4, 22, 8, 4), (12, 40, 10, 40, 20, 6, 4),
              (12, 4, 6, 4, 18, 6, 4), (12, 4, 6, 4, 16, 6, 4),
              (50, 4, 40, 6, 0, 14, 40), (12, 4, 6, 4, -40, 8, 40)]
    for frame in frames:
        width, old_far, length, other, root_bar, root_width, root_far = frame
        records, root = baseline(*frame)
        initial = inventory(records)
        with_root = records+[root]
        occupied = set.union(*(record[0] for record in with_root))
        before = inventory(with_root)
        column, top, old_terminal = width+13, 23-length, width+11-other
        old_delta = int(root_width == 6 and root_bar+root_far == 24)
        assert phi_from(with_root, before)-phi_from(records, initial) == 1-old_delta
        root_owner, owner = len(records), len(with_root)
        bars = {18, root_bar-2, root_bar-4, root_bar-6, top-3, top-5, -50}
        bars = {bar for bar in bars if bar <= 18 and bar % 2 == 0}
        breadths = {6, 8, root_width, root_width+2, root_width+4, 40}
        breadths |= {column-value for value in (old_terminal, old_terminal-2, -33, -35)}
        breadths = {value for value in breadths if value >= 6 and value % 2 == 0}
        for bar, breadth, west in itertools.product(sorted(bars), sorted(breadths), (False, True)):
            fars = {4, 6, 40}
            fars |= {target-bar+offset for target in (
                root_bar-2, root_bar, root_bar+root_far, 24, top-1, 20)
                     for offset in (-2, 0, 2)}
            for far in sorted(value for value in fars if value >= 4 and value % 2 == 0):
                candidate = independent_source((breadth, 22-bar, far),
                    (False, False, west), (bar, column if west else column-2))
                legal = allowed(width, length, other, root_bar, root_width,
                                bar, breadth, far, west)
                assert legal == (not bool(candidate[0] & occupied)), (frame, bar, breadth, far, west)
                if not legal:
                    collisions += 1
                    continue
                after = inventory(with_root+[candidate])
                full, events, indicators = expected_receipts(width, root_bar, root_width,
                    root_far, bar, breadth, far, west, root_owner, owner)
                assert after['full']-before['full'] == full, (frame, bar, breadth, far, west, 'full')
                assert after['events']-before['events'] == events, (frame, bar, breadth, far, west, 'events')
                assert before['events'] <= after['events']
                legs = (22-bar+far)//2
                assert counts(candidate) == (breadth-1+legs,
                    breadth//2+legs+int(west), legs+4*int(west))
                assert charge(candidate) == (1 if west else -1)
                adjacent, cap, triple = indicators
                marginal = 2 if west else 1-adjacent-cap+2*triple
                assert phi_from(with_root+[candidate], after)-phi_from(with_root, before) == marginal
                pair = phi_from(with_root+[candidate], after)-phi_from(records, initial)
                assert pair == marginal+1-old_delta and pair >= 0
                assert phi_from(with_root+[candidate], after) >= width//2+34
                assert triple == cap*old_delta
                if old_delta:
                    old_event = (18, (25, column+5), (24, column+5))
                    assert old_event in before['events'] & after['events']
                    assert old_event not in events
                marginal_values.add(marginal)
                profiles.add((west, indicators))
                cases += 1
                negative += marginal < 0
                zero_pairs += pair == 0
                triple_cases += triple
    assert marginal_values == {-1, 0, 1, 2}
    assert negative and zero_pairs and triple_cases
    return dict(exact_set_controls=cases, collisions=collisions,
                negative_marginals=negative, zero_joint_pairs=zero_pairs,
                three_owner_corrections=triple_cases, marginals=sorted(marginal_values),
                receipt_profiles=len(profiles))


def sharp_control():
    records, root = baseline(12, 4, 6, 4, 18, 6, 4)
    receiver = independent_source((8, 6, 8), (False, False, False), (16, 23))
    totals = [phi_from(selected, inventory(selected))
              for selected in (records, records+[root], records+[root, receiver])]
    assert totals == [40, 41, 40]
    return dict(selected_Phi=totals, root_marginal=1, receiver_marginal=-1,
                joint_marginal=0, complete_extension_existence='NOT_ASSERTED')


def large_controls():
    controls = 0
    for root_bar, root_width, root_far, bar, breadth, far, west in (
            (18, 6, 4, 16, 8, 8, False),
            (22, 2000, 2000, 18, 2002, 2000, False),
            (22, 8, 4, -1982, 2002, 4, True),
            (22, 8, 4, -1982, 2048, 2000, True)):
        records, root = baseline(2000, 2000, 2000, 2000,
                                 root_bar, root_width, root_far)
        with_root = records+[root]
        candidate = independent_source((breadth, 22-bar, far),
            (False, False, west), (bar, 2013 if west else 2011))
        assert allowed(2000, 2000, 2000, root_bar, root_width,
                       bar, breadth, far, west)
        before, after = inventory(with_root), inventory(with_root+[candidate])
        full, events, indicators = expected_receipts(2000, root_bar, root_width,
            root_far, bar, breadth, far, west, len(records), len(with_root))
        assert after['full']-before['full'] == full
        assert after['events']-before['events'] == events
        assert before['events'] <= after['events']
        adjacent, cap, triple = indicators
        assert phi_from(with_root+[candidate], after)-phi_from(with_root, before) == (
            2 if west else 1-adjacent-cap+2*triple)
        assert phi_from(with_root+[candidate], after)-phi_from(records, inventory(records)) >= 0
        controls += 1
    return dict(large_width_height_far_controls=controls)


def main():
    print(json.dumps(dict(status='PASS', roles=role_controls(), receipts=receipt_controls(),
        sharp=sharp_control(), large=large_controls(),
        scope='Finite exact-set controls supplement the general '
        'two-owner compensation proof after a maximal short upward return. '
        'No complete-extension existence, arbitrary-group allocation or global bound.'), indent=2))


if __name__ == '__main__':
    main()
