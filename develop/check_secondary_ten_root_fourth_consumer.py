"""Full-original role classification and exact four-owner root receipts."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_arbitrary_t_consumers import north_U, old_chain
from check_secondary_ten_batch_terminal_budget import key
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_cooperative_promotion import neighbors
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def west_receiver(origin, offset, old_width, height, incident, far, down=True):
    return independent_source((height, incident, far), (True, False, not down),
        (origin-10 if down else origin-8, offset+old_width+12-incident))


def allowed(old_width, width, depth, breadth, consumer_far, height, incident, far, down):
    if not down or not old_width+breadth+14 <= incident <= old_width+width+22:
        return False
    if height > depth-6:
        return False
    cap = (incident-old_width-breadth-12 if height <= consumer_far+2
           else incident-old_width-(18 if height <= 12 else 12))
    return far <= cap


def originals(origin, offset, widths, depths, root_breadth, receiver_breadth,
              receiver_far, breadth, consumer_far):
    fixed, bases, repairs, sites = old_chain(origin, offset, widths, depths, root_breadth)
    old_width, width, depth = widths[0], widths[1], depths[0]
    current_origin, unused, current_offset = sites[1]
    column = offset+old_width+13
    parent = north_U(current_origin, current_offset, old_width+width+26, depth+4, 4, False)
    receiver = north_U(origin+3, column, receiver_breadth, 8, receiver_far, False)
    consumer = north_U(origin, offset, breadth, 4, consumer_far, True)
    return fixed, [parent, receiver, consumer], sites


def normalized_events(records, labels):
    return {(labels[owner], point, target)
            for owner, point, target in inventory(records)['events']}


def check_case(origin, offset, widths, depths, root_breadth, receiver_breadth,
               receiver_far, breadth, consumer_far, height, incident, far,
               check_orders=False):
    old_width, width, depth = widths[0], widths[1], depths[0]
    assert allowed(old_width, width, depth, breadth, consumer_far, height, incident, far, True)
    fixed, additions, sites = originals(origin, offset, widths, depths, root_breadth,
        receiver_breadth, receiver_far, breadth, consumer_far)
    parent, receiver, consumer = additions
    fourth = west_receiver(origin, offset, old_width, height, incident, far)
    before_records, after_records = fixed+additions, fixed+additions+[fourth]
    assert len(set.union(*(source[0] for source in after_records))) == sum(
        len(source[0]) for source in after_records)
    point = origin-9, offset+old_width+12
    assert point in receiver[1] and point not in set.union(*(source[0] for source in before_records))
    assert point in fourth[0]
    assert (point[0], point[1]+1) in fourth[1] & receiver[0]
    assert charge(fourth) == -1
    leg_half = (incident+far)//2
    endpoint_tiles = {(row//2, column//2) for row, column in fourth[0]}
    supports_inside = {point for point in fourth[1] if (point[0]//2, point[1]//2) in endpoint_tiles}
    assert len(fourth[2]) == height+leg_half-1
    assert len(endpoint_tiles) == height//2+leg_half
    assert len(supports_inside) == leg_half
    baseline, before, after = inventory(fixed), inventory(before_records), inventory(after_records)
    fourth_owner, consumer_owner, old_owner = len(fixed)+3, len(fixed)+2, 9*len(widths)+1
    left = offset+1-breadth
    right = offset+old_width+12
    expected_full = {((origin-9)//2, column//2) for column in range(left+1, right+1, 2)}
    expected_events = {(fourth_owner, (origin-9, column), (origin-8, column))
                       for column in range(left+1, right+1, 2)}
    expected_events |= {(consumer_owner, (origin-8, column), (origin-9, column))
                        for column in range(left, offset+1)}
    expected_events |= {(old_owner, (origin-8, column), (origin-9, column))
                        for column in range(offset+1, right+1)}
    assert after['full']-before['full'] == expected_full
    assert after['events']-before['events'] == expected_events
    assert before['full'] <= after['full'] and before['events'] <= after['events']
    assert not (before['full']-baseline['full']) & expected_full
    assert not (before['events']-baseline['events']) & expected_events
    count = old_width+breadth+12
    assert len(expected_full) == count//2 and len(expected_events) == 3*count//2
    interface_tile = (origin-9)//2, offset//2
    terminal_tile = (origin-9)//2, right//2
    assert interface_tile in expected_full and terminal_tile in expected_full
    old_P = fixed[old_owner]
    assert interface_tile not in inventory([fourth, consumer])['full']
    assert interface_tile not in inventory([fourth, old_P])['full']
    assert terminal_tile not in inventory([fourth, receiver])['full']
    assert terminal_tile not in inventory([fourth, old_P])['full']
    marginal = phi_from(after_records, after)-phi_from(before_records, before)
    joint = phi_from(after_records, after)-phi_from(fixed, baseline)
    assert marginal == 1-count//2
    assert joint == old_width//2+width+breadth//2+19 >= 40
    assert after['mass']-baseline['mass'] == old_width+width+breadth+25
    assert len(after['full']-baseline['full']) == 8+count//2
    assert len(after['events']-baseline['events']) == 17+3*count//2
    if check_orders:
        labels = list(range(len(fixed)))+['B', 'R', 'A', 'J']
        events = normalized_events(after_records, labels)
        for order in itertools.permutations(zip(additions+[fourth], ['B', 'R', 'A', 'J'])):
            reordered = fixed+[source for source, label in order]
            reordered_labels = list(range(len(fixed)))+[label for source, label in order]
            assert inventory(reordered)['full'] == after['full']
            assert normalized_events(reordered, reordered_labels) == events
    return dict(blocks=len(widths), old_width=old_width, next_width=width,
                consumer_breadth=breadth, consumer_far=consumer_far,
                fourth_dimensions=[height, incident, far], fourth_charge=-1,
                fourth_marginal=marginal, joint_gain=joint,
                complete_extendibility='NOT_ASSERTED')


def classification_controls():
    decisions = survivors = exact = 0
    phases = dict(below_A_far=0, beyond_A_before_X=0, beyond_A_before_V=0)
    for origin, offset, old_width, width, depth in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80)):
        fixed, additions, sites = originals(origin, offset, [old_width, width],
            [depth, 24], 6, 8, 8, 6, 4)
        for breadth, consumer_far in itertools.product((6, width+6, width+8, width+10),
                                                      (4, depth-10, depth-8)):
            consumer = north_U(origin, offset, breadth, 4, consumer_far, True)
            records = fixed+additions[:2]+[consumer]
            blocked = set.union(*(source[0] for source in records))
            heights = sorted({6, 8, 12, 14, depth-6, depth-4, 100})
            incidents = sorted({4, old_width+breadth+12, old_width+breadth+14,
                old_width+breadth+16, old_width+width+22, old_width+width+24})
            for height, incident, far, down in itertools.product(
                    heights, incidents, (4, 6, 100), (False, True)):
                fourth = west_receiver(origin, offset, old_width, height, incident, far, down)
                expected = allowed(old_width, width, depth, breadth, consumer_far,
                                   height, incident, far, down)
                assert expected == (not bool(fourth[0] & blocked)), (
                    origin, offset, old_width, width, depth, breadth, consumer_far,
                    height, incident, far, down)
                decisions += 1
                if not expected:
                    continue
                survivors += 1
                if incident in (old_width+breadth+14, old_width+width+22) and far == 4:
                    check_case(origin, offset, [old_width, width], [depth, 24], 6, 8,
                               8, breadth, consumer_far, height, incident, far)
                    exact += 1
                    phase = ('below_A_far' if height <= consumer_far+2 else
                             'beyond_A_before_X' if height <= 12 else 'beyond_A_before_V')
                    phases[phase] += 1
    assert all(phases.values())
    return dict(full_original_west_role_decisions=decisions, surviving=survivors,
                exact_full_set_controls=exact, exact_controls_by_far_regime=phases)


def excluded_role_controls():
    U_cases = rotor_cases = 0
    origin, offset, old_width, width, depth = 31, 200, 12, 12, 24
    fixed, additions, sites = originals(origin, offset, [old_width, width], [depth, 24], 6, 8, 4, 6, 4)
    parent = additions[0]
    point = origin-9, offset+old_width+12
    witness = origin-13, point[1]
    for height, incident, far in itertools.product((6, 14, 50), (4, 8, 100), (4, 8, 100)):
        candidates = [north_U(origin-5, point[1], height, incident, far, left)
                      for left in (False, True)]
        candidates += [independent_source((height, incident, far), symmetry, displacement)
            for symmetry, displacement in (
                ((False, True, True), (point[0], point[1]+1)),
                ((True, True, True), (point[0]+1, point[1])))]
        for candidate in candidates:
            assert point in candidate[0] and witness in candidate[0] & parent[0]
            U_cases += 1
    forms = {}
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        source = module['endpoints'], module['selected'], {
            tuple(sorted(edge)) for edge in module['matching']}
        for anchor in source[0]:
            adjacent = {(row-anchor[0], column-anchor[1])
                        for row, column in set(neighbors(anchor)) & source[0]}
            if adjacent <= {(-1, 0), (0, -1)}:
                moved = shift(source, (point[0]-anchor[0], point[1]-anchor[1]))
                forms[key(moved)] = moved
    assert len(forms) == 4
    blocked = set.union(*(source[0] for source in fixed+additions))
    for source in forms.values():
        assert source[0] & blocked
        rotor_cases += 1
    return dict(north_terminal_and_corner_U_collisions=U_cases,
                exhaustive_guard_compatible_rotor_roles=rotor_cases)


def existence_controls():
    count = 0
    for old_width, width, depth, breadth, far in itertools.product(
            (12, 50), (12, 20), (24, 80), (6, 18, 20, 22, 26, 28, 30), (4, 14, 16, 70, 72)):
        if breadth > width+10 or far > depth-8:
            continue
        expected = breadth <= width+6 or (breadth == width+8 and far <= depth-10)
        if expected:
            height = 6 if breadth <= width+6 else far+4
            incident = old_width+width+22
            assert allowed(old_width, width, depth, breadth, far, height, incident, 4, True)
            check_case(31, 200, [old_width, width], [depth, 24], 6, 8, 4,
                       breadth, far, height, incident, 4)
        count += 1
    return dict(geometric_existence_boundary_controls=count,
                positive_cases_use_explicit_full_original_witnesses=True,
                negative_cases_justified_by_separate_general_proof=True)


def main():
    classification = classification_controls()
    long_controls = []
    for count, tall, receiver_far in itertools.product((5, 24), (False, True), (4, 2000)):
        widths = [12+2*(index % 7) for index in range(count)]
        depths = [24+2*(index % 5) for index in range(count)]
        breadth = 6 if tall else widths[1]+8
        height = 14 if tall else 8
        incident = widths[0]+breadth+14 if tall else widths[0]+widths[1]+22
        long_controls.append(check_case(31, 200, widths, depths, 40, 42, receiver_far,
                                       breadth, 4, height, incident, 4))
    witness = check_case(31, 0, [12, 12], [24, 24], 6, 8, 4, 6, 4, 8, 34, 4, True)
    assert witness['fourth_marginal'] == -14 and witness['joint_gain'] == 40
    print(json.dumps(dict(status='PASS', classification=classification,
        excluded_roles=excluded_role_controls(), geometric_existence=existence_controls(),
        long_chain_controls=long_controls, explicit_partial_inventory_witness=witness,
        scope='Full ORIGINAL endpoint, support, matching and exact physical full-tile/labelled-event '
              'SETS. Separate all-parameter proof covers every actual fourth owner in the explicit '
              'full-U/rotor model. Both J/A/P0 and J/P0/R full tiles counted once. Finite controls '
              'do not replace that proof. No complete extension, arbitrary extra-owner monotonicity '
              'or global5/6/grid-equality result is asserted.'), indent=2))


if __name__ == '__main__':
    main()
