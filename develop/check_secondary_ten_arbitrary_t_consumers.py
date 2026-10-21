"""Full-original exact-set controls for arbitrary north consumers and nested bands."""

import itertools
import json
from collections import Counter

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_batch_terminal_budget import key, transform
from check_secondary_ten_internal_consumer_chains import chain, phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_renewed_support_escape import south_U, west_rotor
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def north_U(origin, offset, breadth, depth, far, left):
    return independent_source((breadth, depth, far), (False, False, left),
                              (origin-4-depth, offset+1 if left else offset-1))


def old_chain(origin, offset, widths, depths, root_breadth):
    bases, root, repairs, sites = chain(origin, offset, widths, depths, root_breadth)
    return ([record for base in bases for record in base]+[root]+repairs+
            [west_rotor(origin, offset) for origin, east, offset in sites]+
            [south_U(origin, offset, 6, 4, 4, True) for origin, east, offset in sites],
            bases, repairs, sites)


def classification(width, root_breadth, breadth, depth, far, left):
    if left:
        return True, 'left', breadth-1
    if depth == 4:
        return False, 'bar_collision', None
    if depth == 6:
        if breadth <= width+12:
            return False, 'P_bar_collision', None
        if breadth == width+14:
            return far <= 8, 'right_tight', 1
        if breadth <= width+root_breadth+14:
            return False, 'K_bar_collision', None
        return True, 'right_wide', breadth-width-14
    if breadth <= width+12:
        return far <= depth-6, 'right_deep', breadth-2
    if breadth == width+14:
        return far <= depth+2, 'right_deep_special', breadth-2-int(far >= depth-4)
    if breadth <= width+root_breadth+14:
        return far <= depth-4, 'right_deep', breadth-2
    return True, 'right_deep', breadth-2


def expected_local(origin, offset, width, breadth, depth, far, left, old_owner, new_owner):
    full = {((origin-7)//2, offset//2), ((origin-5)//2, offset//2)}
    near_rows = (-7, -5) if left else (-8, -6, -4)
    events = {(new_owner, (origin+row, offset), (origin+row, offset+1))
              for row in near_rows}
    events |= {(old_owner, (origin+row, offset+1), (origin+row, offset))
               for row in (-7, -5)}
    if left:
        return full, events
    if depth >= 8:
        if breadth == width+14 and far >= depth-4:
            overlap = (far-depth+4)//2
            full |= {((origin-7+2*index)//2, (offset+width+12)//2)
                     for index in range(overlap)}
            events |= {(new_owner, (origin-8+2*index, offset+width+13),
                         (origin-8+2*index, offset+width+12))
                        for index in range(overlap+1)}
            events |= {(old_owner, (origin-7+2*index, offset+width+12),
                         (origin-7+2*index, offset+width+13))
                        for index in range(overlap)}
        return full, events
    full |= {((origin-9)//2, (offset+column)//2) for column in range(0, width+12, 2)}
    events |= {event for column in range(1, width+13) for event in (
        (new_owner, (origin-9, offset+column), (origin-8, offset+column)),
        (old_owner, (origin-8, offset+column), (origin-9, offset+column)))}
    if breadth == width+14:
        extension = (far-4)//2
        full.add(((origin-9)//2, (offset+width+12)//2))
        full |= {((origin-7+2*index)//2, (offset+width+12)//2)
                 for index in range(extension+1)}
        events |= {(new_owner, (origin-8+2*index, offset+width+13),
                     (origin-8+2*index, offset+width+12))
                    for index in range(extension+2)}
        events |= {(old_owner, (origin-7+2*index, offset+width+12),
                     (origin-7+2*index, offset+width+13))
                    for index in range(extension+1)}
    return full, events


def single_block_controls():
    controls = surviving = tail_controls = charge_controls = 0
    phases = Counter()
    minimum = None
    for origin, width, old_depth, root_breadth in itertools.product(
            (-33, 31), (12, 20, 50), (24, 80), (6, 10, 40)):
        offset = -100 if origin < 0 else 200
        fixed, bases, repairs, sites = old_chain(origin, offset, [width], [old_depth], root_breadth)
        blocked = set.union(*(record[0] for record in fixed))
        before = inventory(fixed)
        tail = south_U(origin, offset, width, old_depth+40, old_depth+34, False)
        tail_fixed = fixed[:-1]+[tail]
        tail_blocked = set.union(*(record[0] for record in tail_fixed))
        tail_before = inventory(tail_fixed)
        breadths = sorted({6, 8, 12, width+12, width+14, width+16,
                           width+root_breadth+14, width+root_breadth+16, 2*width+4})
        for breadth, depth, far, left in itertools.product(
                breadths, (4, 6, 8, 10, 50), (4, 6, 8, 10, 50), (False, True)):
            candidate = north_U(origin, offset, breadth, depth, far, left)
            allowed, phase, gain = classification(width, root_breadth, breadth, depth, far, left)
            disjoint = not bool(candidate[0] & blocked)
            assert disjoint == allowed
            assert not bool(candidate[0] & tail_blocked) == allowed
            controls += 1
            half_near, half_far = depth//2, far//2
            tiles = {(row//2, column//2) for row, column in candidate[0]}
            inside = {point for point in candidate[1] if (point[0]//2, point[1]//2) in tiles}
            assert len(tiles) == breadth+half_near+half_far+(0 if left else -2)
            assert len(inside) == half_near+half_far+(2 if left else -2)
            assert charge(candidate) == 1-breadth
            charge_controls += 1
            if not allowed:
                continue
            expected_full, expected_events = expected_local(origin, offset, width, breadth,
                                                             depth, far, left, 10, len(fixed))
            after = inventory(fixed+[candidate])
            assert after['full']-before['full'] == expected_full
            assert after['events']-before['events'] == expected_events
            assert before['full'] <= after['full'] and before['events'] <= after['events']
            assert phi_from(fixed+[candidate], after)-phi_from(fixed, before) == gain
            assert gain >= 1
            assert (gain == 1) == (not left and breadth == width+14 and depth == 6 and far <= 8)
            tail_after = inventory(tail_fixed+[candidate])
            assert tail_after['full']-tail_before['full'] == expected_full
            assert tail_after['events']-tail_before['events'] == expected_events
            assert phi_from(tail_fixed+[candidate], tail_after)-phi_from(tail_fixed, tail_before) == gain
            tail_controls += 1
            phases[phase] += 1
            surviving += 1
            minimum = gain if minimum is None else min(minimum, gain)
    return dict(full_original_parameter_controls=controls,
                charge_tile_support_count_controls=charge_controls,
                surviving_exact_set_controls=surviving,
                tail_replacement_exact_set_controls=tail_controls,
                phase_counts=dict(phases), minimum_gain=minimum)


def role_controls():
    original_roles = triples = 0
    forms = {}
    origin, offset = 31, 0
    point = origin-4, offset
    for breadth, depth, far in itertools.product((6, 14, 40), (4, 6, 50), (4, 8, 60)):
        library = {}
        for symmetry in itertools.product((False, True), repeat=3):
            record = independent_source((breadth, depth, far), symmetry, (0, 0))
            for anchor in record[0]:
                if set(neighbors(anchor)) & record[0] == {(anchor[0]-1, anchor[1])}:
                    moved = shift(record, (point[0]-anchor[0], point[1]-anchor[1]))
                    library[key(moved)] = moved
        expected = {key(north_U(origin, offset, breadth, near, other, left))
                    for near, other in ((depth, far), (far, depth)) for left in (False, True)}
        assert set(library) == expected
        original_roles += len(library)
        triples += 1
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        record = module['endpoints'], module['selected'], {
            tuple(sorted(edge)) for edge in module['matching']}
        for anchor in record[0]:
            if set(neighbors(anchor)) & record[0] == {(anchor[0]-1, anchor[1])}:
                moved = shift(record, (point[0]-anchor[0], point[1]-anchor[1]))
                forms[key(moved)] = moved
    assert len(forms) == 2
    fixed, bases, repairs, sites = old_chain(origin, offset, [12], [24], 6)
    for record in forms.values():
        assert (origin-6, offset+1) in record[0] & repairs[0][0]
    return dict(parameter_triples=triples, full_original_north_terminal_roles=original_roles,
                full_original_rotor_exclusions=len(forms))


def nested_case(origin, offset, widths, depths, root_breadth=6, last_breadth=6, extra=0, padding=0):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
    count = len(widths)
    breadths = [last_breadth]*count
    for index in range(count-2, -1, -1):
        breadths[index] = breadths[index+1]+widths[index+1]+14+extra
    first_row = origin-2*count-12-padding
    consumers = []
    near_full = set()
    near_events = set()
    cross_full = set()
    cross_events = set()
    for index, (breadth, (current_origin, east, current_offset)) in enumerate(zip(breadths, sites)):
        bar_row = first_row+2*index
        depth = current_origin-4-bar_row
        assert depth >= 10 and depth % 2 == 0
        candidate = north_U(current_origin, current_offset, breadth, depth, 4, True)
        consumers.append(candidate)
        assert charge(candidate) == 1-breadth
        old_owner = 9*count+1+index
        owner = len(fixed)+index
        current_full, current_events = expected_local(current_origin, current_offset,
            widths[index], breadth, depth, 4, True, old_owner, owner)
        assert not near_full & current_full and not near_events & current_events
        near_full |= current_full
        near_events |= current_events
        if index:
            far_column = current_offset+1-breadth
            assert current_offset % 2 == 0 and far_column % 2 == 1
            current_full = {((bar_row-1)//2, column//2)
                            for column in range(far_column+1, current_offset, 2)}
            current_events = {event for column in range(far_column, current_offset+1)
                              for event in (
                                  (owner-1, (bar_row-1, column), (bar_row, column)),
                                  (owner, (bar_row, column), (bar_row-1, column)))}
            assert len(current_full) == breadth//2-1
            assert len(current_events) == 2*breadth
            assert not cross_full & current_full and not cross_events & current_events
            cross_full |= current_full
            cross_events |= current_events
    assert not near_full & cross_full and not near_events & cross_events
    combined = fixed+consumers
    endpoints = set.union(*(record[0] for record in combined))
    assert len(endpoints) == sum(len(record[0]) for record in combined)
    assert len({key(record) for record in combined}) == len(combined)
    before = inventory(fixed)
    after = inventory(combined)
    assert after['full']-before['full'] == near_full | cross_full
    assert after['events']-before['events'] == near_events | cross_events
    gain = phi_from(combined, after)-phi_from(fixed, before)
    assert gain == breadths[0]-3*count+2 >= 23*count-18 >= count
    prefix_checks = 0
    if count <= 8:
        current = fixed
        previous = phi_from(fixed, before)
        for index, consumer in enumerate(consumers):
            individual = inventory(fixed+[consumer])
            assert phi_from(fixed+[consumer], individual)-phi_from(fixed, before) == breadths[index]-1
            current = current+[consumer]
            receipt = inventory(current)
            value = phi_from(current, receipt)
            assert value-previous == (breadths[0]-1 if index == 0 else -3)
            previous = value
            prefix_checks += 1
    last_origin, east, last_offset = sites[-1]
    unresolved = last_origin-1, east-1
    assert unresolved in bases[-1][4][1] and unresolved not in endpoints
    assert {(last_origin-1, east-2), (last_origin, east-1),
            (last_origin-1, east)} <= set(neighbors(unresolved)) & endpoints
    tail = south_U(last_origin, last_offset, widths[-1], depths[-1]+40, depths[-1]+34, False)
    tail_fixed = fixed[:-1]+[tail]
    tail_combined = tail_fixed+consumers
    assert len(set.union(*(record[0] for record in tail_combined))) == sum(
        len(record[0]) for record in tail_combined)
    tail_before = inventory(tail_fixed)
    tail_after = inventory(tail_combined)
    assert tail_after['full']-tail_before['full'] == near_full | cross_full
    assert tail_after['events']-tail_before['events'] == near_events | cross_events
    assert phi_from(tail_combined, tail_after)-phi_from(tail_fixed, tail_before) == gain
    return dict(blocks=count, breadths=breadths, total_mass=sum(breadth-1 for breadth in breadths),
                individual_new_full=len(near_full), individual_new_events=len(near_events),
                cross_full=len(cross_full), cross_events=len(cross_events),
                cross_signed_debit=2*len(cross_full)-len(cross_events),
                exact_joint_gain=gain, prefix_checks=prefix_checks,
                later_prefix_marginal=-3 if count > 1 else None,
                compensated_phi=phi_from(combined, after),
                tail_compensated_phi=phi_from(tail_combined, tail_after),
                missing_forced_original_support=unresolved, complete=False,
                complete_extendibility='NOT_ASSERTED')


def isometry_controls():
    fixed, bases, repairs, sites = old_chain(31, 0, [12], [24], 6)
    checks = 0
    for breadth, depth, far, left in ((6, 4, 100, True), (26, 6, 8, False),
                                     (34, 6, 100, False), (26, 10, 12, False)):
        candidate = north_U(31, 0, breadth, depth, far, left)
        before, after = inventory(fixed), inventory(fixed+[candidate])
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = (-int(flip_column), -int(flip_row)) if transpose else (
                -int(flip_row), -int(flip_column))
            moved = [transform(record, symmetry, offset) for record in fixed]
            moved_candidate = transform(candidate, symmetry, offset)
            moved_before, moved_after = inventory(moved), inventory(moved+[moved_candidate])
            expected_events = {(owner, affine(point, symmetry, offset), affine(target, symmetry, offset))
                               for owner, point, target in after['events']-before['events']}
            expected_full = {(affine((2*row, 2*column), symmetry, offset)[0]//2,
                              affine((2*row, 2*column), symmetry, offset)[1]//2)
                             for row, column in after['full']-before['full']}
            assert moved_after['events']-moved_before['events'] == expected_events
            assert moved_after['full']-moved_before['full'] == expected_full
            checks += 1
    return checks


def main():
    nested = [nested_case(31, 0, [12]*count, [24]*count) for count in (1, 2, 3, 8)]
    nested += [nested_case(-33, 200, [12+2*(index % 4) for index in range(count)],
                           [24+2*(index % 5) for index in range(count)], 10, 20, 6, 20)
               for count in (7, 24)]
    print(json.dumps(dict(status='PASS', local=single_block_controls(), roles=role_controls(),
                         tile_preserving_isometries=isometry_controls(), nested=nested,
                         scope='Exact full ORIGINAL endpoint/support/matching and mixed-tile '
                         'and owner-labelled directed-event SET controls of independent general '
                         'proofs. A finite cutoff is not a classification proof. Actual complete '
                         'extensions are not asserted, and no global 5/6 or triple equality '
                         'conclusion is inferred.'), indent=2))


if __name__ == '__main__':
    main()
