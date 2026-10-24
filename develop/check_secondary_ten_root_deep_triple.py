"""Full-original classification and exact physical-set controls for the root triple."""

import itertools
import json

from check_incident_eight_north_transfer import charge
from check_secondary_ten_arbitrary_t_consumers import expected_local, north_U, old_chain, role_controls
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def expected_addition(origin, offset, width, next_width, breadth, incident, far,
                      old_owner, parent_owner, consumer_owner):
    full, events = expected_local(origin, offset, width, breadth, incident, far,
                                   True, old_owner, consumer_owner)
    bar_full, bar_events, far_full, far_events = set(), set(), set(), set()
    far_column = offset+1-breadth
    if incident == 8:
        bar_full = {((origin-13)//2, column//2)
                    for column in range(far_column+1, offset, 2)}
        bar_events = {event for column in range(far_column, offset+1) for event in (
            (parent_owner, (origin-13, column), (origin-12, column)),
            (consumer_owner, (origin-12, column), (origin-13, column)))}
    if breadth == next_width+12:
        parent_column = offset-next_width-12
        bar_row = origin-4-incident
        terminal = bar_row+far
        far_full = {(row//2, parent_column//2)
                    for row in range(bar_row+1, terminal, 2)}
        if incident == 8:
            far_full.add(((bar_row-1)//2, parent_column//2))
        far_events = {(parent_owner, (row, parent_column), (row, far_column))
                      for row in range(bar_row, terminal+1, 2)}
        far_events |= {(consumer_owner, (row, far_column), (row, parent_column))
                       for row in range(bar_row+1, terminal, 2)}
    assert not full & bar_full and not full & far_full and not bar_full & far_full
    assert not events & bar_events and not events & far_events and not bar_events & far_events
    return full | bar_full | far_full, events | bar_events | far_events


def normalized_events(records, labels):
    return {(labels[owner], point, target)
            for owner, point, target in inventory(records)['events']}


def check_case(origin, offset, widths, depths, root_breadth, receiver_breadth,
               receiver_far, breadth, incident, far, check_orders=False):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
    old_width, next_width, depth = widths[0], widths[1], depths[0]
    current_origin, unused, current_offset = sites[1]
    column = offset+old_width+13
    parent = north_U(current_origin, current_offset, old_width+next_width+26, depth+4, 4, False)
    receiver = north_U(origin+3, column, receiver_breadth, 8, receiver_far, False)
    consumer = north_U(origin, offset, breadth, incident, far, True)
    combined = fixed+[parent, receiver, consumer]
    blocked = set.union(*(record[0] for record in combined))
    assert len(blocked) == sum(len(record[0]) for record in combined)
    assert charge(parent) == -(old_width+next_width+25)
    assert charge(receiver) == 1 and charge(consumer) == 1-breadth
    before, pair, after = inventory(fixed), inventory(fixed+[parent, receiver]), inventory(combined)
    expected_full, expected_events = expected_addition(origin, offset, old_width,
        next_width, breadth, incident, far, 9*len(widths)+1, len(fixed), len(fixed)+2)
    assert after['full']-pair['full'] == expected_full
    assert after['events']-pair['events'] == expected_events
    assert pair['full'] <= after['full'] and pair['events'] <= after['events']
    assert not (pair['full']-before['full']) & expected_full
    assert not (pair['events']-before['events']) & expected_events
    tight = int(breadth == next_width+12)
    deepest = int(incident == 8)
    expected_total_full = (8 if not deepest else breadth//2+7)+tight*(far//2+deepest)
    expected_total_events = 17+2*breadth*deepest+tight*(far+1)
    assert len(after['full']-before['full']) == expected_total_full
    assert len(after['events']-before['events']) == expected_total_events
    assert after['mass']-before['mass'] == old_width+next_width+breadth+24
    pair_gain = phi_from(fixed+[parent, receiver], pair)-phi_from(fixed, before)
    joint_gain = phi_from(combined, after)-phi_from(fixed, before)
    expected_gain = (old_width+next_width+breadth+24-tight if not deepest
                     else old_width+next_width+22+tight)
    assert pair_gain == old_width+next_width+25
    assert joint_gain == expected_gain >= 46
    assert joint_gain-pair_gain == (breadth-1-tight if not deepest else -3+tight)
    if check_orders:
        expected_normalized = normalized_events(combined, list(range(len(fixed)))+['B', 'R', 'A'])
        for order in itertools.permutations(((parent, 'B'), (receiver, 'R'), (consumer, 'A'))):
            records = fixed+[record for record, label in order]
            labels = list(range(len(fixed)))+[label for record, label in order]
            reordered = inventory(records)
            assert reordered['full'] == after['full']
            assert normalized_events(records, labels) == expected_normalized
            assert phi_from(records, reordered) == phi_from(combined, after)
    return dict(blocks=len(widths), breadth=breadth, incident=incident, far=far,
                receiver_breadth=receiver_breadth, receiver_far=receiver_far,
                tight=bool(tight), pair_gain=pair_gain, joint_gain=joint_gain,
                consumer_marginal=joint_gain-pair_gain,
                complete=False, complete_extendibility='NOT_ASSERTED')


def classification_controls():
    decisions = surviving = exact = 0
    phases = {4: 0, 6: 0, 8: 0}
    for origin, offset, old_width, next_width, depth, root_breadth in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80), (6, 40)):
        fixed, bases, repairs, sites = old_chain(origin, offset,
            [old_width, next_width], [depth, 80], root_breadth)
        current_origin, unused, current_offset = sites[1]
        column = offset+old_width+13
        parent = north_U(current_origin, current_offset, old_width+next_width+26, depth+4, 4, False)
        receiver = north_U(origin+3, column, root_breadth+2, 8, 4, False)
        blocked = set.union(*(record[0] for record in fixed+[parent, receiver]))
        breadths = sorted({6, next_width+10, next_width+12, next_width+14,
                          old_width+12, old_width+14, old_width+root_breadth+16, 200})
        for breadth, incident, far, left in itertools.product(
                breadths, (4, 6, 8, 10, 24, 100),
                (4, depth-8, depth-6, depth-4, depth-2, 200), (True, False)):
            consumer = north_U(origin, offset, breadth, incident, far, left)
            expected = (left and incident in (4, 6, 8) and breadth <= next_width+12
                        and far <= depth+incident-12)
            assert expected == (not bool(consumer[0] & blocked)), (
                origin, offset, old_width, next_width, depth, root_breadth,
                breadth, incident, far, left)
            decisions += 1
            if not expected:
                continue
            surviving += 1
            if breadth in (6, next_width+12):
                check_case(origin, offset, [old_width, next_width], [depth, 80],
                    root_breadth, root_breadth+2, 4, breadth, incident, far)
                exact += 1
                phases[incident] += 1
    return dict(full_original_classification_decisions=decisions, surviving=surviving,
                exact_physical_set_controls=exact, exact_controls_by_incident=phases)


def main():
    classification = classification_controls()
    long_controls = []
    for count, incident, tight, receiver_far in itertools.product(
            (5, 24), (4, 6, 8), (False, True), (4, 2000)):
        widths = [12+2*(index % 7) for index in range(count)]
        depths = [24+2*(index % 5) for index in range(count)]
        breadth = widths[1]+12 if tight else 6
        long_controls.append(check_case(31, 200, widths, depths, 40, 142,
            receiver_far, breadth, incident, depths[0]+incident-12,
            check_orders=count == 5 and receiver_far == 4))
    witness = check_case(31, 0, [12, 12], [24, 24], 6, 8, 4, 6, 8, 4,
                         check_orders=True)
    assert witness['pair_gain'] == 49 and witness['joint_gain'] == 46
    print(json.dumps(dict(status='PASS', classification=classification,
        full_north_terminal_role_controls=role_controls(), long_chain_controls=long_controls,
        negative_marginal_witness=witness,
        scope='General proof separately establishes every actual t0-owner classification '
              'conditional on the specified root B and arbitrary allowed R in the explicit '
              'full-U/rotor model. Exact SETS partition near, bar and tight far receipts. '
              'Enumeration is a control, not a general proof. No complete extension, arbitrary '
              'extra-owner monotonicity, grid exhaustion or global 5/6 improvement is asserted.'), indent=2))


if __name__ == '__main__':
    main()
