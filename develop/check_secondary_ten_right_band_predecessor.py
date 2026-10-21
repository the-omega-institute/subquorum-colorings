"""Exact full-original mixed-direction band and forced-predecessor controls."""

import itertools
import json

from check_incident_eight_north_transfer import charge
from check_secondary_ten_arbitrary_t_consumers import expected_local, north_U, old_chain
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def pair_sources(sites, widths, depths, index, breadth, far, parent_far=4):
    origin, east, offset = sites[index-1]
    current_origin, current_east, current_offset = sites[index]
    parent_breadth = widths[index-1]+widths[index]+26
    parent = north_U(current_origin, current_offset, parent_breadth, depths[index-1], parent_far, False)
    predecessor = north_U(origin, offset, breadth, 4, far, True)
    return parent, predecessor


def receipts(sites, widths, depths, index, breadth, far, parent_owner, predecessor_owner, parent_far=4):
    count = len(widths)
    origin, east, offset = sites[index-1]
    current_origin, current_east, current_offset = sites[index]
    old_width, width = widths[index-1], widths[index]
    old_owner, current_owner = 9*count+index, 9*count+1+index
    parent_breadth = old_width+width+26
    parent_full, parent_events = expected_local(current_origin, current_offset, width,
        parent_breadth, depths[index-1], parent_far, False, current_owner, parent_owner)
    old_band_full = {((origin-9)//2, column//2)
                     for column in range(offset+2, offset+old_width+12, 2)}
    old_band_full |= {((origin-9)//2, (offset+old_width+12)//2),
                      ((origin-7)//2, (offset+old_width+12)//2)}
    old_band_events = {event for column in range(offset+1, offset+old_width+13)
        for event in ((parent_owner, (origin-9, column), (origin-8, column)),
                      (old_owner, (origin-8, column), (origin-9, column)))}
    old_band_events |= {(parent_owner, (row, offset+old_width+13), (row, offset+old_width+12))
                        for row in (origin-8, origin-6)}
    old_band_events.add((old_owner, (origin-7, offset+old_width+12),
                        (origin-7, offset+old_width+13)))
    extension = (parent_far-4)//2
    for step in range(extension):
        old_band_full.add(((origin-5+2*step)//2, (offset+old_width+12)//2))
        old_band_events.add((parent_owner, (origin-4+2*step, offset+old_width+13),
                             (origin-4+2*step, offset+old_width+12)))
        old_band_events.add((old_owner, (origin-5+2*step, offset+old_width+12),
                             (origin-5+2*step, offset+old_width+13)))
    predecessor_full, predecessor_events = expected_local(origin, offset, old_width,
        breadth, 4, far, True, old_owner, predecessor_owner)
    far_column = offset+1-breadth
    new_band_full = {((origin-9)//2, column//2)
                     for column in range(far_column+1, offset, 2)}
    new_band_events = {event for column in range(far_column, offset+1)
        for event in ((parent_owner, (origin-9, column), (origin-8, column)),
                      (predecessor_owner, (origin-8, column), (origin-9, column)))}
    corner = {((origin-9)//2, offset//2)}
    boundary_full = set()
    boundary_events = set()
    if breadth == width+12:
        boundary_full = {((origin-9)//2, current_offset//2)}
        boundary_full |= {((origin-7+2*step)//2, current_offset//2) for step in range(far//2)}
        boundary_events = {(parent_owner, (origin-8+2*step, current_offset),
                            (origin-8+2*step, current_offset+1)) for step in range(far//2+1)}
        boundary_events |= {(predecessor_owner, (origin-7+2*step, current_offset+1),
                             (origin-7+2*step, current_offset)) for step in range(far//2)}
    full_groups = [parent_full, old_band_full, predecessor_full, new_band_full, corner, boundary_full]
    event_groups = [parent_events, old_band_events, predecessor_events, new_band_events, boundary_events]
    assert sum(map(len, full_groups)) == len(set.union(*full_groups))
    assert sum(map(len, event_groups)) == len(set.union(*event_groups))
    return full_groups, event_groups


def check_pair(origin, offset, widths, depths, index, breadth, far, root_breadth=6, parent_far=4):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
    parent, predecessor = pair_sources(sites, widths, depths, index, breadth, far, parent_far)
    combined = fixed+[parent, predecessor]
    assert len(set.union(*(record[0] for record in combined))) == sum(len(record[0]) for record in combined)
    assert charge(parent) == 1-(widths[index-1]+widths[index]+26)
    assert charge(predecessor) == 1-breadth
    before = inventory(fixed)
    parent_after = inventory(fixed+[parent])
    after = inventory(combined)
    full_groups, event_groups = receipts(sites, widths, depths, index, breadth, far,
                                        len(fixed), len(fixed)+1, parent_far)
    assert parent_after['full']-before['full'] == full_groups[0] | full_groups[1]
    assert parent_after['events']-before['events'] == event_groups[0] | event_groups[1]
    assert after['full']-before['full'] == set.union(*full_groups)
    assert after['events']-before['events'] == set.union(*event_groups)
    old_width, width = widths[index-1], widths[index]
    boundary = int(breadth == width+12)
    extension = (parent_far-4)//2
    assert len(after['full']-before['full']) == (old_width+breadth)//2+11+extension+boundary*(1+far//2)
    assert len(after['events']-before['events']) == 2*old_width+2*breadth+36+2*extension+boundary*(far+1)
    base_phi = phi_from(fixed, before)
    parent_gain = phi_from(fixed+[parent], parent_after)-base_phi
    joint_gain = phi_from(combined, after)-base_phi
    assert parent_gain == width+11
    assert joint_gain == width+10+boundary >= 22
    assert joint_gain-parent_gain == -1+boundary
    predecessor_alone = inventory(fixed+[predecessor])
    assert phi_from(fixed+[predecessor], predecessor_alone)-base_phi == breadth-1
    corner = next(iter(full_groups[4]))
    assert corner not in parent_after['full'] and corner not in predecessor_alone['full']
    assert corner not in inventory([parent, predecessor])['full']
    return dict(parent_gain=parent_gain, joint_gain=joint_gain,
                exterior_debit=-(old_width+13), boundary=boundary)


def role_controls():
    controls = allowed_count = 0
    for old_width, width, depth in itertools.product((12, 50), (12, 50), (24, 80)):
        fixed, bases, repairs, sites = old_chain(31, 0, [old_width, width], [depth, 80], 10)
        parent, unused = pair_sources(sites, [old_width, width], [depth, 80], 1, 6, 4)
        blocked = set.union(*(record[0] for record in fixed+[parent]))
        origin, east, offset = sites[0]
        for breadth, incident, far, left in itertools.product(
                sorted({6, 8, width+10, width+12, width+14, old_width+width+26, 120}),
                (4, 6, 8, 24, 100), sorted({4, 8, depth-8, depth-6, 100}), (False, True)):
            candidate = north_U(origin, offset, breadth, incident, far, left)
            expected = left and incident == 4 and breadth <= width+12 and far <= depth-8
            assert expected == (not bool(candidate[0] & blocked))
            controls += 1
            allowed_count += int(expected)
    return dict(full_source_collision_classification_controls=controls, surviving=allowed_count)


def batch_case(count, boundary):
    widths = [12+2*(index % 5) for index in range(count)]
    depths = [24+2*(index % 7) for index in range(count)]
    fixed, bases, repairs, sites = old_chain(31, 0, widths, depths, 10)
    new_sources = []
    new_full = set()
    new_events = set()
    expected_gain = 0
    for index in range(1, count, 2):
        breadth = widths[index]+12 if boundary else 6
        far = depths[index-1]-8 if boundary else 4
        parent, predecessor = pair_sources(sites, widths, depths, index, breadth, far)
        full_groups, event_groups = receipts(sites, widths, depths, index, breadth, far,
                                            len(fixed)+len(new_sources), len(fixed)+len(new_sources)+1)
        current_full, current_events = set.union(*full_groups), set.union(*event_groups)
        assert not new_full & current_full and not new_events & current_events
        new_full |= current_full
        new_events |= current_events
        new_sources += [parent, predecessor]
        expected_gain += widths[index]+10+int(boundary)
    combined = fixed+new_sources
    assert len(set.union(*(record[0] for record in combined))) == sum(len(record[0]) for record in combined)
    before, after = inventory(fixed), inventory(combined)
    assert after['full']-before['full'] == new_full
    assert after['events']-before['events'] == new_events
    gain = phi_from(combined, after)-phi_from(fixed, before)
    assert gain == expected_gain >= 11*count
    missing = sites[-1][0]-1, sites[-1][1]-1
    assert missing in bases[-1][4][1] and missing not in set.union(*(record[0] for record in combined))
    return dict(blocks=count, boundary=boundary, exact_joint_gain=gain,
                three_owner_corners=count//2, new_full=len(new_full), new_events=len(new_events),
                complete=False, complete_extendibility='NOT_ASSERTED')


def main():
    pair_controls = boundary_controls = 0
    maximum_exterior_loss = 0
    for origin, old_width, width, depth, root_breadth in itertools.product(
            (-33, 31), (12, 50, 200), (12, 50), (24, 80), (6, 40)):
        for breadth, far in itertools.product((6, width+10, width+12), (4, depth-8)):
            result = check_pair(origin, -100 if origin < 0 else 200,
                                [old_width, width], [depth, 80], 1, breadth, far, root_breadth)
            pair_controls += 1
            boundary_controls += result['boundary']
            maximum_exterior_loss = max(maximum_exterior_loss, -result['exterior_debit'])
    interior_controls = 0
    for index in (1, 2, 3, 4):
        for boundary in (False, True):
            widths, depths = [12, 14, 16, 50, 20], [24, 80, 26, 100, 24]
            check_pair(31, 0, widths, depths, index,
                       widths[index]+12 if boundary else 6,
                       depths[index-1]-8 if boundary else 4, 40)
            interior_controls += 1
    far_phase_controls = far_collision_controls = 0
    for old_width, width, depth, parent_far in itertools.product(
            (12, 50), (12, 50), (24, 80), (4, 6, 8)):
        for boundary in (False, True):
            check_pair(31, 0, [old_width, width], [depth, 80], 1,
                       width+12 if boundary else 6, depth-8, 10, parent_far)
            far_phase_controls += 1
        fixed, bases, repairs, sites = old_chain(31, 0, [old_width, width], [depth, 80], 10)
        for excluded_far in (10, 12, 24, 80, 200):
            parent, unused = pair_sources(sites, [old_width, width], [depth, 80], 1, 6, 4, excluded_far)
            assert (31, old_width+13) in parent[0] & bases[0][4][0]
            far_collision_controls += 1
    print(json.dumps(dict(status='PASS', pair_exact_set_controls=pair_controls,
        boundary_controls=boundary_controls, interior_full_chain_controls=interior_controls,
        far_phase_exact_set_controls=far_phase_controls, far_collision_controls=far_collision_controls,
        largest_tested_exterior_loss=maximum_exterior_loss, roles=role_controls(),
        paired_batches=[batch_case(count, boundary) for count in (2, 4, 8, 24)
                        for boundary in (False, True)],
        scope='Exact FULL ORIGINAL collision, matching/support charge, physical mixed full-tile '
              'and owner-labelled directed-event SET controls for general written proofs. '
              'Three-owner corner counted separately. No finite enumeration replaces proof; '
              'no complete extension or global 5/6 claim.'), indent=2))


if __name__ == '__main__':
    main()
