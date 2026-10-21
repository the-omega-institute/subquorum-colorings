"""Full-original exact sets for raised right bands and both actual predecessors."""

import itertools
import json

from check_incident_eight_north_transfer import charge
from check_secondary_ten_arbitrary_t_consumers import expected_local, north_U, old_chain
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def sources(sites, widths, depths, index, breadth, incident, far, parent_far):
    origin, east, offset = sites[index-1]
    current_origin, current_east, current_offset = sites[index]
    parent = north_U(current_origin, current_offset, widths[index-1]+widths[index]+26,
                     depths[index-1]+2, parent_far, False)
    predecessor = north_U(origin, offset, breadth, incident, far, True)
    return parent, predecessor


def receipts(sites, widths, depths, index, breadth, incident, far, parent_far,
             parent_owner, predecessor_owner):
    count = len(widths)
    origin, east, offset = sites[index-1]
    current_origin, current_east, current_offset = sites[index]
    old_width, width = widths[index-1], widths[index]
    old_owner, current_owner = 9*count+index, 9*count+1+index
    parent_full, parent_events = expected_local(current_origin, current_offset, width,
        old_width+width+26, depths[index-1]+2, parent_far, False, current_owner, parent_owner)
    extension = (parent_far-4)//2
    old_far_full = {((origin-7+2*step)//2, (offset+old_width+12)//2)
                    for step in range(extension)}
    old_far_events = {(parent_owner, (origin-8+2*step, offset+old_width+13),
                       (origin-8+2*step, offset+old_width+12)) for step in range(extension+1)}
    old_far_events |= {(old_owner, (origin-7+2*step, offset+old_width+12),
                        (origin-7+2*step, offset+old_width+13)) for step in range(extension)}
    predecessor_full, predecessor_events = expected_local(origin, offset, old_width,
        breadth, incident, far, True, old_owner, predecessor_owner)
    band_full, band_events = set(), set()
    if incident == 6:
        far_column = offset+1-breadth
        band_full = {((origin-11)//2, column//2) for column in range(far_column+1, offset, 2)}
        band_events = {event for column in range(far_column, offset+1)
            for event in ((parent_owner, (origin-11, column), (origin-10, column)),
                          (predecessor_owner, (origin-10, column), (origin-11, column)))}
    boundary_full, boundary_events = set(), set()
    if breadth == width+12:
        first_row = origin-4-incident
        boundary_full = {((first_row+1+2*step)//2, current_offset//2) for step in range(far//2)}
        if incident == 6:
            boundary_full.add(((origin-11)//2, current_offset//2))
        boundary_events = {(parent_owner, (first_row+2*step, current_offset),
                            (first_row+2*step, current_offset+1)) for step in range(far//2+1)}
        boundary_events |= {(predecessor_owner, (first_row+1+2*step, current_offset+1),
                             (first_row+1+2*step, current_offset)) for step in range(far//2)}
    full_groups = [parent_full, old_far_full, predecessor_full, band_full, boundary_full]
    event_groups = [parent_events, old_far_events, predecessor_events, band_events, boundary_events]
    assert sum(map(len, full_groups)) == len(set.union(*full_groups))
    assert sum(map(len, event_groups)) == len(set.union(*event_groups))
    return full_groups, event_groups


def check_pair(origin, offset, widths, depths, index, breadth, incident, far, parent_far):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, 40)
    parent, predecessor = sources(sites, widths, depths, index, breadth, incident, far, parent_far)
    combined = fixed+[parent, predecessor]
    assert len(set.union(*(record[0] for record in combined))) == sum(len(record[0]) for record in combined)
    assert charge(parent) == 1-(widths[index-1]+widths[index]+26)
    assert charge(predecessor) == 1-breadth
    before, parent_after, after = inventory(fixed), inventory(fixed+[parent]), inventory(combined)
    full_groups, event_groups = receipts(sites, widths, depths, index, breadth, incident, far,
                                        parent_far, len(fixed), len(fixed)+1)
    assert parent_after['full']-before['full'] == full_groups[0] | full_groups[1]
    assert parent_after['events']-before['events'] == event_groups[0] | event_groups[1]
    assert after['full']-before['full'] == set.union(*full_groups)
    assert after['events']-before['events'] == set.union(*event_groups)
    old_width, width = widths[index-1], widths[index]
    boundary = int(breadth == width+12)
    expected_gain = (old_width+width+breadth+22-boundary if incident == 4
                     else old_width+width+20+boundary)
    base_phi = phi_from(fixed, before)
    assert phi_from(fixed+[parent], parent_after)-base_phi == old_width+width+23
    assert phi_from(combined, after)-base_phi == expected_gain >= old_width+width+20 >= 44
    corner = (sites[index-1][0]-11)//2, sites[index-1][2]//2
    assert corner not in after['full']
    return expected_gain


def classification_controls():
    decisions = far_decisions = 0
    for old_width, width, depth, parent_far in itertools.product((12, 50), (12, 50), (24, 80), (4, 10)):
        fixed, bases, repairs, sites = old_chain(31, 0, [old_width, width], [depth, 80], 40)
        parent, unused = sources(sites, [old_width, width], [depth, 80], 1, 6, 4, 4, parent_far)
        blocked = set.union(*(record[0] for record in fixed+[parent]))
        origin, east, offset = sites[0]
        for breadth, incident, far, left in itertools.product(
                (6, width+10, width+12, width+14, old_width+14, 140),
                (4, 6, 8, 10, 100), sorted({4, depth-8, depth-6, depth-4, 200}), (False, True)):
            predecessor = north_U(origin, offset, breadth, incident, far, left)
            expected = left and incident in (4, 6) and breadth <= width+12 and far <= depth+incident-12
            assert expected == (not bool(predecessor[0] & blocked))
            decisions += 1
        for other_far in (4, 6, 8, 10, 12, 24, 200):
            candidate, unused = sources(sites, [old_width, width], [depth, 80], 1, 6, 4, 4, other_far)
            assert (other_far <= 10) == (not any(candidate[0] & record[0] for record in fixed))
            far_decisions += 1
    return dict(predecessor_classification_decisions=decisions, parent_far_decisions=far_decisions)


def batch_case(count):
    widths = [12+2*(index % 5) for index in range(count)]
    depths = [24+2*(index % 7) for index in range(count)]
    fixed, bases, repairs, sites = old_chain(-33, -100, widths, depths, 6)
    new_sources, new_full, new_events = [], set(), set()
    expected_gain = 0
    for index in range(1, count, 2):
        incident = 4 if index % 4 == 1 else 6
        breadth = widths[index]+12 if index % 3 else 6
        far = depths[index-1]+incident-12
        parent_far = 4+2*((index//2) % 4)
        parent, predecessor = sources(sites, widths, depths, index, breadth, incident, far, parent_far)
        full_groups, event_groups = receipts(sites, widths, depths, index, breadth, incident,
            far, parent_far, len(fixed)+len(new_sources), len(fixed)+len(new_sources)+1)
        current_full, current_events = set.union(*full_groups), set.union(*event_groups)
        assert not new_full & current_full and not new_events & current_events
        new_full |= current_full
        new_events |= current_events
        new_sources += [parent, predecessor]
        boundary = int(breadth == widths[index]+12)
        expected_gain += (widths[index-1]+widths[index]+breadth+22-boundary if incident == 4
                          else widths[index-1]+widths[index]+20+boundary)
    combined = fixed+new_sources
    assert len(set.union(*(record[0] for record in combined))) == sum(len(record[0]) for record in combined)
    before, after = inventory(fixed), inventory(combined)
    assert after['full']-before['full'] == new_full
    assert after['events']-before['events'] == new_events
    assert phi_from(combined, after)-phi_from(fixed, before) == expected_gain >= 22*count
    return dict(blocks=count, exact_joint_gain=expected_gain, new_full=len(new_full),
                new_events=len(new_events), complete=False, complete_extendibility='NOT_ASSERTED')


def main():
    controls = 0
    for origin, old_width, width, depth, incident, parent_far in itertools.product(
            (-33, 31), (12, 50), (12, 50), (24, 80), (4, 6), (4, 6, 8, 10)):
        for breadth, far in itertools.product((6, width+10, width+12), (4, depth+incident-12)):
            check_pair(origin, -100 if origin < 0 else 200, [old_width, width], [depth, 80],
                       1, breadth, incident, far, parent_far)
            controls += 1
    interior = 0
    for index, incident in itertools.product((1, 2, 3, 4), (4, 6)):
        widths, depths = [12, 14, 50, 16, 20], [24, 80, 26, 100, 24]
        check_pair(31, 0, widths, depths, index, widths[index]+12,
                   incident, depths[index-1]+incident-12, 10)
        interior += 1
    print(json.dumps(dict(status='PASS', exact_pair_set_controls=controls,
        interior_chain_controls=interior, classification=classification_controls(),
        paired_batches=[batch_case(count) for count in (2, 4, 8, 24)],
        scope='Exact full ORIGINAL collision/charge and mixed physical tile / owner-labelled '
              'directed event SET controls for an ordinary general raised-band proof. '
              'Two predecessor depth phases, no old three-owner corner. '
              'No finite search substitutes for proof or complete-model/global claim.'), indent=2))


if __name__ == '__main__':
    main()
