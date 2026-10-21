"""Exact full-original controls for renewed support closure and long tail debit."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_batch_terminal_budget import key, transform
from check_secondary_ten_internal_consumer_chains import chain, phi_from
from check_secondary_ten_north_contact_debit import inventory
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def west_rotor(origin, offset):
    module = transform_module(rotor(), (False, False, False), (origin-5, offset-3))
    return (module['endpoints'], module['selected'],
            {tuple(sorted(edge)) for edge in module['matching']})


def south_U(origin, offset, breadth, depth, far, left):
    return independent_source((breadth, depth, far), (False, True, left),
                              (origin+depth-2, offset+2 if left else offset))


def inspect_chain(origin, offset, widths, depths, tail_depth, root_breadth=6):
    bases, root, repairs, sites = chain(origin, offset, widths, depths, root_breadth)
    block_count = len(bases)
    fixed = [record for base in bases for record in base]+[root]+repairs
    rotors = [west_rotor(origin, offset) for origin, east, offset in sites]
    lefts = [south_U(origin, offset, 6, 4, 4, True) for origin, east, offset in sites]
    full = fixed+rotors+lefts
    endpoints = set.union(*(record[0] for record in full))
    assert len(endpoints) == sum(len(record[0]) for record in full)
    assert len({key(record) for record in full}) == len(full)
    before = inventory(fixed)
    middle = inventory(fixed+rotors)
    after = inventory(full)
    assert middle['full'] == before['full'] and middle['events'] == before['events']
    expected_full = set()
    expected_events = set()
    missing = []
    interior_collision_checks = 0
    for index, (origin, east, offset) in enumerate(sites):
        rotor_owner = len(fixed)+index
        left_owner = len(fixed)+block_count+index
        point = origin-2, offset+1
        renewed = origin-3, offset+1
        assert renewed in rotors[index][0] and renewed in lefts[index][1]
        assert point in bases[index][7][1] and point in lefts[index][0]
        assert charge(rotors[index]) == 0 and charge(lefts[index]) == -1
        assert {(origin-3, offset+1), (origin-2, offset),
                (origin-2, offset+2)} <= set(neighbors(point)) & set.union(
                    *(record[0] for record in fixed+rotors))
        expected_full.add(((origin-3)//2, offset//2))
        expected_events |= {
            (rotor_owner, renewed, point),
            (rotor_owner, (origin-2, offset), point),
            (left_owner, point, (origin-2, offset))}
        support = origin-4, offset
        assert support in repairs[index][1] and support not in endpoints
        assert {(origin-4, offset-1), (origin-4, offset+1),
                (origin-3, offset)} <= set(neighbors(support)) & endpoints
        missing.append(support)
        if index < block_count-1:
            collision = sites[index+1][0], offset+1
            assert collision in bases[index+1][4][0]
            for breadth, extra, far in itertools.product((6, widths[index], 40),
                                                        (0, 2, 40), (4, 30)):
                candidate = south_U(origin, offset, breadth, depths[index]-2+extra, far, False)
                assert collision in candidate[0]
                interior_collision_checks += 1
    assert after['full']-middle['full'] == expected_full
    assert after['events']-middle['events'] == expected_events
    assert middle['full'] <= after['full'] and middle['events'] <= after['events']
    baseline = sum(width+9 for width in widths)
    expected_phi = baseline+root_breadth-1-block_count
    assert phi_from(fixed, before) == phi_from(fixed+rotors, middle) == expected_phi
    assert phi_from(full, after) == expected_phi
    tail_origin, east, tail_offset = sites[-1]
    width = widths[-1]
    assert tail_depth >= depths[-1]-2 and tail_depth % 2 == 0
    tail = south_U(tail_origin, tail_offset, width, tail_depth, tail_depth-6, False)
    prefix = fixed+rotors+lefts[:-1]
    prefix_endpoints = set.union(*(record[0] for record in prefix))
    assert not prefix_endpoints & tail[0] and charge(tail) == 1
    prefix_receipt = inventory(prefix)
    tail_receipt = inventory(prefix+[tail])
    assert phi_from(prefix, prefix_receipt) == expected_phi
    rotor_owner = len(fixed)+block_count-1
    tail_owner = len(prefix)
    west_owner = 9*(block_count-1)+5
    origin, offset = tail_origin, tail_offset
    expected_tail_full = {((origin-3)//2, offset//2),
                          ((origin+5)//2, (offset+width)//2)}
    expected_tail_events = {
        (rotor_owner, (origin-3, offset+1), (origin-2, offset+1)),
        (rotor_owner, (origin-2, offset), (origin-2, offset+1)),
        (tail_owner, (origin-1, offset+1), (origin-1, offset))}
    expected_tail_events |= {
        (west_owner, (origin+extra, offset+width+1), (origin+extra, offset+width))
        for extra in (4, 5, 6, 7)}
    expected_tail_events |= {
        (tail_owner, (origin+extra, offset+width), (origin+extra, offset+width+1))
        for extra in (5, 7)}
    assert tail_receipt['full']-prefix_receipt['full'] == expected_tail_full
    assert tail_receipt['events']-prefix_receipt['events'] == expected_tail_events
    assert prefix_receipt['full'] <= tail_receipt['full']
    assert prefix_receipt['events'] <= tail_receipt['events']
    assert tail_receipt['mass'] == prefix_receipt['mass']
    assert phi_from(prefix+[tail], tail_receipt) == expected_phi-4
    tail_endpoints = prefix_endpoints | tail[0]
    assert all(point not in tail_endpoints for point in missing)
    previous_separations = []
    for index in range(block_count-1):
        for record in bases[index]+[repairs[index], rotors[index], lefts[index]]:
            separation = min(column for row, column in record[0])-max(
                column for row, column in tail[0])
            assert separation >= 2
            previous_separations.append(separation)
    compensators = [independent_source((width+14, 6, 4), (False, False, False),
                                       (origin-10, offset-1))
                    for width, (origin, east, offset) in zip(widths, sites)]
    compensated = full+compensators
    compensated_endpoints = set.union(*(record[0] for record in compensated))
    assert len(compensated_endpoints) == sum(len(record[0]) for record in compensated)
    compensated_tail = prefix+[tail]+compensators
    compensated_tail_endpoints = set.union(*(record[0] for record in compensated_tail))
    assert len(compensated_tail_endpoints) == sum(len(record[0]) for record in compensated_tail)
    expected_compensator_full = set()
    expected_compensator_events = set()
    for index, (width, (origin, east, offset)) in enumerate(zip(widths, sites)):
        owner = len(full)+index
        old_owner = 9*block_count+1+index
        assert charge(compensators[index]) == -(width+13)
        assert missing[index] in compensators[index][0]
        expected_compensator_full |= {((origin-9)//2, (offset+column)//2)
                                      for column in range(0, width+14, 2)}
        expected_compensator_full |= {((origin-7)//2, offset//2),
                                      ((origin-5)//2, offset//2),
                                      ((origin-7)//2, (offset+width+12)//2)}
        expected_compensator_events |= {
            event for column in range(1, width+13) for event in (
                (owner, (origin-9, offset+column), (origin-8, offset+column)),
                (old_owner, (origin-8, offset+column), (origin-9, offset+column)))}
        expected_compensator_events |= {
            (owner, (origin+row, offset), (origin+row, offset+1)) for row in (-8, -6, -4)}
        expected_compensator_events |= {
            (old_owner, (origin+row, offset+1), (origin+row, offset)) for row in (-7, -5)}
        expected_compensator_events |= {
            (owner, (origin+row, offset+width+13), (origin+row, offset+width+12))
            for row in (-8, -6)}
        expected_compensator_events.add((old_owner, (origin-7, offset+width+12),
                                         (origin-7, offset+width+13)))
    for originals, old_receipt, expected_value in (
            (compensated, after, expected_phi+block_count),
            (compensated_tail, tail_receipt, expected_phi+block_count-4)):
        receipt = inventory(originals)
        assert receipt['full']-old_receipt['full'] == expected_compensator_full
        assert receipt['events']-old_receipt['events'] == expected_compensator_events
        assert phi_from(originals, receipt) == expected_value
        occupied = set.union(*(record[0] for record in originals))
        last_origin, east, last_offset = sites[-1]
        unresolved = last_origin-1, last_offset+widths[-1]+13
        assert unresolved in bases[-1][4][1] and unresolved not in occupied
        assert {(last_origin-1, east-2), (last_origin, east-1),
                (last_origin-1, east)} <= set(neighbors(unresolved)) & occupied
    return dict(blocks=block_count, baseline=baseline, closed_phi=expected_phi,
                tail_phi=expected_phi-4, root_breadth=root_breadth,
                tail_U=[width, tail_depth, tail_depth-6],
                rotor_increment=dict(mass=0, full_tiles=0, directed_events=0, phi=0),
                simultaneous_left_increment=dict(mass=block_count, full_tiles=block_count,
                                                 directed_events=3*block_count, phi=0),
                tail_increment=dict(positive_owners=1, mass=0, full_tiles=2,
                                    directed_events=9, phi=-4),
                interior_collision_checks=interior_collision_checks,
                previous_column_separation_checks=len(previous_separations),
                minimum_previous_column_separation=min(previous_separations, default=None),
                simultaneous_compensators=dict(originals=block_count,
                    mass=sum(width+13 for width in widths),
                    full_tiles=len(expected_compensator_full),
                    directed_events=len(expected_compensator_events), phi=block_count,
                    compensated_phi=expected_phi+block_count,
                    compensated_tail_phi=expected_phi+block_count-4,
                    still_missing_forced_tail_support=unresolved),
                missing_forced_original_supports=missing,
                complete=False, complete_extendibility='NOT_ASSERTED')


def role_and_charge_controls():
    parameter_controls = role_controls = rotor_controls = collision_controls = 0
    positive_long_disjoint = negative_left_disjoint = 0
    origin, offset = 31, 0
    bases, root, repairs, sites = chain(origin, offset, [12], [24])
    fixed = bases[0]+[root]+repairs+[west_rotor(origin, offset)]
    blocked = set.union(*(record[0] for record in fixed))
    point = origin-2, offset+1
    for breadth, depth, far in itertools.product((6, 12, 22, 40),
                                                (4, 18, 20, 22, 24, 60), (4, 12, 30)):
        expected = [south_U(origin, offset, breadth, depth, far, left)
                    for left in (False, True)]
        forms = {}
        for symmetry in itertools.product((False, True), repeat=3):
            record = independent_source((breadth, depth, far), symmetry, (0, 0))
            for anchor in record[0]:
                if set(neighbors(anchor)) & record[0] != {(anchor[0]+1, anchor[1])}:
                    continue
                moved = shift(record, (point[0]-anchor[0], point[1]-anchor[1]))
                forms[key(moved)] = moved
        for near, other in ((depth, far), (far, depth)):
            for left in (False, True):
                expected_record = south_U(origin, offset, breadth, near, other, left)
                assert key(expected_record) in forms
        assert set(forms) == {key(south_U(origin, offset, breadth, near, other, left))
                              for near, other in ((depth, far), (far, depth))
                              for left in (False, True)}
        role_controls += len(forms)
        for left, record in zip((False, True), expected):
            tile_count = len({(row//2, column//2) for row, column in record[0]})
            inside = sum((row//2, column//2) in {
                (endrow//2, endcolumn//2) for endrow, endcolumn in record[0]}
                         for row, column in record[1])
            expected_tiles = breadth//2+depth//2+far//2+(0 if left else 1)
            expected_inside = depth//2+far//2+(0 if left else 4)
            assert tile_count == expected_tiles and inside == expected_inside
            assert len(record[2]) == breadth-1+depth//2+far//2
            assert charge(record) == (-1 if left else 1)
            if not left and depth < 22:
                collision = origin+depth-3, offset+2
                assert collision in record[0] & bases[0][7][0]
                collision_controls += 1
            if not record[0] & blocked:
                positive_long_disjoint += not left
                negative_left_disjoint += left
        parameter_controls += 1
    forms = {}
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        record = module['endpoints'], module['selected'], {
            tuple(sorted(edge)) for edge in module['matching']}
        for anchor in record[0]:
            if set(neighbors(anchor)) & record[0] == {(anchor[0]+1, anchor[1])}:
                moved = shift(record, (point[0]-anchor[0], point[1]-anchor[1]))
                forms[key(moved)] = moved
    assert len(forms) == 2
    for record in forms.values():
        assert record[0] & {(origin-1, offset+2), (origin-1, offset)}
        assert record[0] & blocked
        rotor_controls += 1
    return dict(parameter_controls=parameter_controls, full_original_south_terminal_roles=role_controls,
                two_charge_phase_controls=2*parameter_controls,
                below_escape_depth_V_collision_controls=collision_controls,
                full_original_rotor_exclusions=rotor_controls,
                sampled_endpoint_disjoint_positive_long_roles=positive_long_disjoint,
                sampled_endpoint_disjoint_negative_left_roles=negative_left_disjoint)


def isometry_controls():
    bases, root, repairs, sites = chain(31, 0, [12, 20], [24, 40])
    fixed = [record for base in bases for record in base]+[root]+repairs
    new_rotors = [west_rotor(origin, offset) for origin, east, offset in sites]
    first_left = south_U(sites[0][0], sites[0][2], 6, 4, 4, True)
    tail = south_U(sites[-1][0], sites[-1][2], 20, 60, 54, False)
    prefix = fixed+new_rotors+[first_left]
    before = inventory(prefix)
    after = inventory(prefix+[tail])
    controls = 0
    for symmetry in itertools.product((False, True), repeat=3):
        transpose, flip_row, flip_column = symmetry
        offset = (-int(flip_column), -int(flip_row)) if transpose else (
            -int(flip_row), -int(flip_column))
        moved_prefix = [transform(record, symmetry, offset) for record in prefix]
        moved_tail = transform(tail, symmetry, offset)
        moved_before = inventory(moved_prefix)
        moved_after = inventory(moved_prefix+[moved_tail])
        expected_events = {(owner, affine(point, symmetry, offset), affine(target, symmetry, offset))
                           for owner, point, target in after['events']-before['events']}
        expected_full = {(affine((2*row, 2*column), symmetry, offset)[0]//2,
                          affine((2*row, 2*column), symmetry, offset)[1]//2)
                         for row, column in after['full']-before['full']}
        assert moved_after['full']-moved_before['full'] == expected_full
        assert moved_after['events']-moved_before['events'] == expected_events
        assert phi_from(moved_prefix+[moved_tail], moved_after)-phi_from(
            moved_prefix, moved_before) == -4
        controls += 1
    return controls


def audit_boundary_controls():
    parameters = target_checks = width_twelve_boundaries = 0
    for origin, offset, width, tail_depth in itertools.product(
            (-33, 31), (-100, 0), (12, 14, 50), (22, 60)):
        bases, root, repairs, sites = chain(origin, offset, [width], [24])
        west = bases[0][5]
        first = bases[0][0]
        candidate = south_U(origin, offset, width, tail_depth, tail_depth-6, False)
        assert max(column//2 for row, column in first[0]) < (offset+width)//2
        assert min(column for row, column in first[0]) > offset+1
        assert max(row for row, column in first[0]) < origin+tail_depth-3
        assert not {(row//2, column//2) for row, column in first[0]} & {
            (row//2, column//2) for row, column in candidate[0]}
        for extra in (2, 4, 5, 6, 7):
            target = origin+extra, offset+width
            intrinsic_row = target[1]-width-1-offset
            assert intrinsic_row == -1 and target not in west[1]
            target_checks += 1
        width_twelve_boundaries += width == 12
        parameters += 1
    return dict(parameter_controls=parameters, W_negative_intrinsic_row_targets=target_checks,
                Q_J_disjoint_endpoint_tiles=parameters,
                width_twelve_adjacent_tile_column_boundaries=width_twelve_boundaries)


def main():
    receipts = []
    for origin, offset, width, depth, extra in itertools.product(
            (-33, 31), (-100, 0), (12, 14, 20, 50), (24, 40, 80), (0, 2, 40)):
        receipts.append(inspect_chain(origin, offset, [width], [depth], depth-2+extra))
    chains = [inspect_chain(31, 0, [12]*8, [24]*8, 22),
              inspect_chain(-33, 200, [12, 20, 14, 50, 18, 24, 12],
                            [24, 40, 26, 80, 30, 24, 60], 100),
              inspect_chain(31, 0, [12+2*(index % 5) for index in range(24)],
                            [24+2*(index % 4) for index in range(24)], 68)]
    print(json.dumps(dict(status='PASS', single_block_parameter_controls=len(receipts),
                         roles_and_phases=role_and_charge_controls(),
                         tile_preserving_isometries=isometry_controls(),
                         accepted_audit_boundary_controls=audit_boundary_controls(),
                         nonuniform_and_long_chains=chains,
                         minimum_example=receipts[0],
                         scope='Exact full-original endpoint, support, matching, physical-tile '
                         'and owner-labelled event set controls of the separate general proof. '
                         'These partial families are incomplete, not asserted extendible, '
                         'and are not counterexamples to the complete-model target. '
                         'No finite cutoff is used as a general classification proof.'), indent=2))


if __name__ == '__main__':
    main()
