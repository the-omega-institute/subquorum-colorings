"""Exact original-source and physical-set controls for the first deep root pair."""

import itertools
import json

from check_incident_eight_north_transfer import charge
from check_secondary_ten_arbitrary_t_consumers import expected_local, north_U, old_chain
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check_pair(origin, offset, widths, depths, root_breadth, breadth, far):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
    old_width, width, depth = widths[0], widths[1], depths[0]
    current_origin, unused, current_offset = sites[1]
    column = offset+old_width+13
    parent = north_U(current_origin, current_offset, old_width+width+26, depth+4, 4, False)
    receiver = north_U(origin+3, column, breadth, 8, far, False)
    combined = fixed+[parent, receiver]
    assert len(set.union(*(record[0] for record in combined))) == sum(len(record[0]) for record in combined)
    assert charge(parent) == -(old_width+width+25) and charge(receiver) == 1
    before, parent_after, after = inventory(fixed), inventory(fixed+[parent]), inventory(combined)
    current_P_owner, old_P_owner = 9*len(widths)+2, 9*len(widths)+1
    parent_owner, receiver_owner = len(fixed), len(fixed)+1
    parent_full, parent_events = expected_local(current_origin, current_offset, width,
        old_width+width+26, depth+4, 4, False, current_P_owner, parent_owner)
    receiver_full = {((origin-7+2*step)//2, (column-1)//2) for step in range(4)}
    receiver_events = {(receiver_owner, (row, column), (row, column-1))
                       for row in range(origin-8, origin-1, 2)}
    receiver_events |= {(old_P_owner, (row, column-1), (row, column))
                        for row in range(origin-7, origin, 2)}
    assert len(parent_full) == 2 and len(parent_events) == 5
    assert len(receiver_full) == 4 and len(receiver_events) == 8
    assert not parent_full & receiver_full and not parent_events & receiver_events
    assert parent_after['full']-before['full'] == parent_full
    assert parent_after['events']-before['events'] == parent_events
    assert after['full']-parent_after['full'] == receiver_full
    assert after['events']-parent_after['events'] == receiver_events
    assert after['full']-before['full'] == parent_full | receiver_full
    assert after['events']-before['events'] == parent_events | receiver_events
    bottom = (origin-1)//2, (column-1)//2
    assert bottom not in before['full'] and bottom in receiver_full
    assert bottom not in inventory([fixed[old_P_owner], receiver])['full']
    assert (origin, column) in receiver[1] and (origin-1, column) in bases[0][4][1]
    base_phi = phi_from(fixed, before)
    parent_gain = phi_from(fixed+[parent], parent_after)-base_phi
    joint_gain = phi_from(combined, after)-base_phi
    assert parent_gain == old_width+width+24
    assert joint_gain == old_width+width+25 >= 49
    assert joint_gain-parent_gain == 1
    return dict(blocks=len(widths), breadth=breadth, far=far,
                parent_gain=parent_gain, joint_gain=joint_gain,
                complete=False, complete_extendibility='NOT_ASSERTED')


def classification_controls():
    decisions = surviving = 0
    for old_width, width, depth, root_breadth in itertools.product(
            (12, 50), (12, 50), (24, 80), (6, 40)):
        fixed, bases, repairs, sites = old_chain(31, 200, [old_width, width], [depth, 80], root_breadth)
        current_origin, unused, current_offset = sites[1]
        parent = north_U(current_origin, current_offset, old_width+width+26, depth+4, 4, False)
        blocked = set.union(*(record[0] for record in fixed+[parent]))
        column = 200+old_width+13
        for breadth, incident, far, left in itertools.product(
                sorted({6, root_breadth, root_breadth+2, root_breadth+10, 200}),
                (4, 6, 8, 10, 24, 100), (4, 6, 80), (False, True)):
            receiver = north_U(34, column, breadth, incident, far, left)
            expected = not left and incident == 8 and breadth >= root_breadth+2
            assert expected == (not bool(receiver[0] & blocked))
            decisions += 1
            surviving += int(expected)
    return dict(full_original_U_role_decisions=decisions, surviving=surviving)


def main():
    controls = 0
    for origin, offset, old_width, width, depth, root_breadth in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80), (6, 40)):
        for breadth, far in itertools.product((root_breadth+2, root_breadth+10, root_breadth+100), (4, 6, 200)):
            check_pair(origin, offset, [old_width, width], [depth, 80], root_breadth, breadth, far)
            controls += 1
    long_controls = []
    for count, far in itertools.product((5, 24), (4, 2000)):
        widths = [12+2*(index % 7) for index in range(count)]
        depths = [24+2*(index % 5) for index in range(count)]
        long_controls.append(check_pair(31, 200, widths, depths, 40, 42, far))
    print(json.dumps(dict(status='PASS', exact_pair_set_controls=controls,
        classification=classification_controls(), long_chain_controls=long_controls,
        scope='FULL original collision/charge and exact physical full-tile/event SETS. '
              'The P/R/E three-owner bottom tile is counted once; axial directions are excluded. '
              'No finite control substitutes for the all-parameter proof or proves a complete extension.'), indent=2))


if __name__ == '__main__':
    main()
