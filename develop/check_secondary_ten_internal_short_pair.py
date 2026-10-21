"""Full-original classification and exact simultaneous internal short-pair receipts."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_incident_eight_north_transfer import charge
from check_secondary_ten_arbitrary_t_consumers import north_U, old_chain
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def receipts(anchor, lateral, width, breadth, gap, old_owner, receiver_owner, consumer_owner):
    column = lateral+width+13
    far_column = lateral-breadth-gap
    full = {((anchor-7+2*index)//2, (column-1)//2) for index in range(4)}
    full |= {((anchor-7+2*index)//2, lateral//2) for index in range(2)}
    events = {(owner, source, target) for row in range(anchor-7, anchor, 2)
              for owner, source, target in (
                  (receiver_owner, (row, column), (row, column-1)),
                  (old_owner, (row, column-1), (row, column)))}
    events |= {(owner, source, target) for row in range(anchor-7, anchor-4, 2)
               for owner, source, target in (
                   (consumer_owner, (row, lateral), (row, lateral+1)),
                   (old_owner, (row, lateral+1), (row, lateral)))}
    if gap == 0:
        events |= {(receiver_owner, (anchor-7, far_column), (anchor-7, far_column+1)),
                   (consumer_owner, (anchor-7, far_column+1), (anchor-7, far_column))}
    assert len(full) == 6 and len(events) == 12+2*int(gap == 0)
    return full, events


def check_group(origin, offset, widths, depths, root_breadth, choices):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
    before = inventory(fixed)
    combined = list(fixed)
    expected_full, expected_events = set(), set()
    row_footprints = set()
    gain = 0
    for index, breadth, gap in choices:
        assert index >= 1
        anchor, unused, lateral = sites[index]
        width = widths[index]
        column = lateral+width+13
        receiver = north_U(anchor+3, column, width+breadth+14+gap, 10, 4, True)
        consumer = north_U(anchor, lateral, breadth, 4, 4, True)
        receiver_owner, consumer_owner = len(combined), len(combined)+1
        old_owner = 9*len(widths)+1+index
        full, events = receipts(anchor, lateral, width, breadth, gap,
                               old_owner, receiver_owner, consumer_owner)
        footprint = set(range((anchor-11)//2, (anchor-1)//2+1))
        assert not footprint & row_footprints
        row_footprints |= footprint
        assert not full & expected_full and not events & expected_events
        expected_full |= full
        expected_events |= events
        assert charge(receiver) == -1 and charge(consumer) == 1-breadth
        combined += [receiver, consumer]
        gain += breadth-2*int(gap == 0)
        if gap == 0:
            far_column = lateral-breadth
            target = anchor-6, far_column
            endpoints = set.union(*(record[0] for record in combined))
            assert target in receiver[1] and target not in endpoints
            assert {(anchor-7, far_column), (anchor-6, far_column+1)} <= (
                set(neighbors(target)) & endpoints)
    after = inventory(combined)
    assert after['full']-before['full'] == expected_full
    assert after['events']-before['events'] == expected_events
    assert before['full'] <= after['full'] and before['events'] <= after['events']
    assert after['mass']-before['mass'] == sum(breadth for index, breadth, gap in choices)
    assert phi_from(combined, after)-phi_from(fixed, before) == gain >= 4*len(choices)
    return dict(blocks=len(widths), pairs=len(choices), gain=gain,
                new_full=len(expected_full), new_events=len(expected_events))


def classification_controls():
    decisions = old_disjoint = pair_disjoint = tight_collisions = deep_windows = 0
    for width, previous_depth, current_depth in itertools.product((12, 40), (24, 80), (24, 80)):
        widths, depths = [12, width, 20], [previous_depth, current_depth, 24]
        fixed, unused, unused, sites = old_chain(31, 0, widths, depths, 6)
        blocked = set.union(*(record[0] for record in fixed))
        anchor, unused, lateral = sites[1]
        column = lateral+width+13
        for receiver_breadth, far in itertools.product(
                (6, width+12, width+14, width+16, width+20, width+40), (4, 6, 20)):
            receiver = north_U(anchor+3, column, receiver_breadth, 10, far, True)
            if receiver[0] & blocked:
                continue
            assert receiver_breadth >= width+14
            old_disjoint += 1
            for breadth, incident, other, left in itertools.product(
                    (6, 8, 20), (4, 6, 8, 10, 40), (4, 6, 20), (False, True)):
                consumer = north_U(anchor, lateral, breadth, incident, other, left)
                if not consumer[0] & (blocked | receiver[0]):
                    assert left and incident == 4 and receiver_breadth >= width+breadth+14
                    pair_disjoint += 1
                if receiver_breadth == width+14:
                    mandatory = {(row, lateral) for row in range(anchor-8, anchor-3)}
                    assert receiver[0] & mandatory
                    tight_collisions += 1
                decisions += 1
        next_anchor, unused, next_lateral = sites[2]
        parent = north_U(next_anchor, next_lateral, width+widths[2]+26,
                         current_depth+6, 4, False)
        for receiver_breadth, incident, far in itertools.product(
                range(6, width+widths[2]+36, 2), (10, 12, 14, 24), (4, 6, 20)):
            receiver = north_U(anchor+3, column, receiver_breadth, incident, far, True)
            if not receiver[0] & (blocked | parent[0]):
                assert incident == 10 and receiver_breadth <= width+widths[2]+24
            deep_windows += 1
    return dict(actual_role_decisions=decisions, old_disjoint_receivers=old_disjoint,
        pair_disjoint_survivors=pair_disjoint, tight_breadth_mandatory_collisions=tight_collisions,
        next_deep_window_decisions=deep_windows)


def main():
    exact = 0
    for origin, offset, width, breadth, gap in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (6, 8, 20, 100), (0, 2, 10, 100)):
        check_group(origin, offset, [12, width, 20], [24, 80, 26], 40, [(1, breadth, gap)])
        exact += 1
    batches = []
    for count in (3, 6, 12, 24):
        widths = [12+2*((3*index) % 13) for index in range(count)]
        depths = [24+2*((7*index) % 17) for index in range(count)]
        choices = [(index, 6+2*(index % 5), 0 if index % 2 else 4) for index in range(1, count)]
        batches.append(check_group(31, -100, widths, depths, 6, choices))
    print(json.dumps(dict(status='PASS', classification=classification_controls(),
        exact_single_pair_set_controls=exact, nonuniform_simultaneous_groups=batches,
        scope='General written actual-owner coupling plus exact selected-union compensation '
              'for both far legs4, with disjoint physical tile row footprints. No complete '
              'extension existence or arbitrary exterior marginal/global inequality inferred.'), indent=2))


if __name__ == '__main__':
    main()
