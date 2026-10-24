"""Full-original controls for the forced four-row root support staircase."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_root_fourth_consumer import originals
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_internal_consumer_chains import phi_from
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def horizontal(origin, offset, old_width, index, height, incident, far, down=True):
    return independent_source((height, incident, far), (True, False, not down),
        (origin-10-index if down else origin-8-index, offset+old_width+12-incident))


def frontier(width, depth, breadth, far):
    return breadth <= width or breadth == width+2 and far <= depth-12


def witness(origin, offset, widths, depths, root_breadth, receiver_breadth,
            receiver_far, breadth, consumer_far):
    old_width, width, depth = widths[0], widths[1], depths[0]
    assert frontier(width, depth, breadth, consumer_far)
    fixed, additions, sites = originals(origin, offset, widths, depths, root_breadth,
        receiver_breadth, receiver_far, breadth, consumer_far)
    height = 6 if breadth <= width else consumer_far+4
    cascade = [horizontal(origin, offset, old_width, index, height+2*index,
                         old_width+width+16+2*index, 4) for index in range(4)]
    full = fixed+additions+cascade
    endpoints = set.union(*(source[0] for source in full))
    assert len(endpoints) == sum(len(source[0]) for source in full)
    assert [charge(source) for source in cascade] == [-1, 1, -1, 1]
    column = offset+old_width+12
    for index in range(1, 4):
        retained = fixed+additions+cascade[:index]
        before = set.union(*(source[0] for source in retained))
        point = origin-9-index, column
        assert point in cascade[index-1][1] and point not in before
        assert {(point[0], point[1]+1), (point[0]+1, point[1])} <= before
        assert point in cascade[index][0]
    assert (origin-13, column) in additions[0][0] & cascade[3][1]
    return fixed, additions, cascade


def witness_controls():
    cases = 0
    for origin, offset, old_width, width, depth, count, receiver_far in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80), (2, 5), (4, 2000)):
        for breadth, consumer_far in itertools.product((6, width, width+2),
                                                       (4, depth-12, depth-10, depth-8)):
            if not frontier(width, depth, breadth, consumer_far):
                continue
            witness(origin, offset, [old_width, width]+[12]*(count-2),
                    [depth]+[24]*(count-1), 40, 42, receiver_far, breadth, consumer_far)
            cases += 1
    return dict(full_original_geometric_witnesses=cases,
                fresh_support_and_two_neighbor_checks=3*cases,
                final_support_already_consumed_by_B=cases,
                complete_extendibility='NOT_ASSERTED')


def geometric_necessary_controls():
    decisions = disjoint = trades = 0
    for old_width, width, depth, breadth, consumer_far in (
            (12, 12, 24, 6, 4), (12, 12, 24, 14, 12),
            (50, 20, 80, 6, 72), (50, 20, 80, 22, 68)):
        fixed, additions, cascade = witness(31, 0, [old_width, width], [depth, 24],
                                           6, 8, 4, breadth, consumer_far)
        for index in range(1, 4):
            retained = fixed+additions+cascade[:index]
            blocked = set.union(*(source[0] for source in retained))
            previous_depth = old_width+width+14+2*index
            previous_height = (6 if breadth <= width else consumer_far+4)+2*(index-1)
            for height, incident, far, down in itertools.product(
                    sorted({6, 8, previous_height-2, previous_height,
                            previous_height+2, depth-4, depth-2, depth}),
                    sorted({4, previous_depth, previous_depth+2,
                            previous_depth+4, previous_depth+6,
                            old_width+width+22, old_width+width+24}), (4, 6, 100), (False, True)):
                if height < 6:
                    continue
                candidate = horizontal(31, 0, old_width, index, height, incident, far, down)
                decisions += 1
                if candidate[0] & blocked:
                    continue
                assert down
                assert previous_depth+2 <= incident <= old_width+width+22
                assert height < depth+index-4
                assert height >= previous_height+2 or incident >= previous_depth+far+2
                disjoint += 1
                trades += int(height <= previous_height)
    assert disjoint and trades
    return dict(candidate_role_decisions=decisions, geometrically_disjoint=disjoint,
                short_height_forces_extra_depth_controls=trades)


def rotor_controls():
    checks = 0
    fixed, additions, cascade = witness(31, 0, [12, 12], [24, 24], 6, 8, 4, 6, 4)
    for index in range(1, 4):
        point = 31-9-index, 24
        blocked = set.union(*(source[0] for source in fixed+additions+cascade[:index]))
        forms = set()
        for symmetry in itertools.product((False, True), repeat=3):
            module = transform_module(rotor(), symmetry)
            for anchor in module['endpoints']:
                own = {(row-anchor[0], column-anchor[1])
                       for row, column in set(neighbors(anchor)) & module['endpoints']}
                if own <= {(-1, 0), (0, -1)}:
                    moved = frozenset((point[0]+row-anchor[0], point[1]+column-anchor[1])
                                      for row, column in module['endpoints'])
                    forms.add(moved)
        assert len(forms) == 4
        assert all(form & blocked for form in forms)
        checks += len(forms)
    return dict(fixed_rotor_collision_controls=checks)


def ledger_case(origin, offset, widths, depths, breadth, consumer_far, count_orders=False):
    old_width, width, depth = widths[0], widths[1], depths[0]
    fixed, additions, cascade = witness(origin, offset, widths, depths, 6, 8, 4,
                                        breadth, consumer_far)
    height = 6 if breadth <= width else consumer_far+4
    column = offset+old_width+12
    first_column = offset-width-6
    last_column = offset-width-10
    second_owner, third_owner, fourth_owner = len(fixed)+4, len(fixed)+5, len(fixed)+6
    parent_owner, next_P_owner = len(fixed), 9*len(widths)+2
    epsilon = int(breadth == width+2 and consumer_far == depth-12)
    previous = fixed+additions+cascade[:1]
    for index in range(1, 4):
        before = inventory(previous)
        previous += [cascade[index]]
        after = inventory(previous)
        if index == 1:
            full = set()
            events = {(parent_owner, (origin-10, column+1), (origin-10, column))}
        elif index == 2:
            full = {((origin-11)//2, current//2)
                    for current in range(first_column, column+1, 2)}
            far_row = origin+height-9
            full.add((far_row//2, first_column//2))
            events = {(third_owner if current % 2 == 0 else second_owner,
                       (origin-11 if current % 2 == 0 else origin-10, current),
                       (origin-10 if current % 2 == 0 else origin-11, current))
                      for current in range(first_column, column+1)}
            events |= {(third_owner if current % 2 == 0 else second_owner,
                        (far_row+1 if current % 2 == 0 else far_row, current),
                        (far_row if current % 2 == 0 else far_row+1, current))
                       for current in range(first_column, first_column+3)}
        else:
            full = {((origin-13)//2, current//2)
                    for current in range(last_column, column+1, 2)}
            events = {(parent_owner, (origin-13, current), (origin-12, current))
                      for current in range(last_column, column+1)}
            events |= {(fourth_owner, (origin-12, current), (origin-13, current))
                       for current in range(last_column+1, column, 2)}
            events.add((parent_owner, (origin-12, column+1), (origin-12, column)))
            if epsilon:
                far_row = origin+depth-15
                full |= {(far_row//2, current//2)
                         for current in (last_column, last_column+2)}
                events |= {(next_P_owner, (far_row+1, current), (far_row, current))
                           for current in range(last_column, last_column+5)}
                events |= {(fourth_owner, (far_row, current), (far_row+1, current))
                           for current in (last_column+1, last_column+3)}
        assert after['full']-before['full'] == full
        assert after['events']-before['events'] == events
        assert before['full'] <= after['full'] and before['events'] <= after['events']
    base = inventory(fixed)
    after = inventory(previous)
    near_count = old_width+breadth+12
    second_depth = old_width+width+18
    fourth_depth = old_width+width+22
    assert after['mass']-base['mass'] == old_width+width+breadth+26
    assert sum(charge(source) > 0 for source in additions+cascade) == 3
    assert len(after['full']-base['full']) == 11+(near_count+second_depth+fourth_depth)//2+2*epsilon
    assert len(after['events']-base['events']) == 24+3*near_count//2+second_depth+3*fourth_depth//2+7*epsilon
    joint = phi_from(previous, after)-phi_from(fixed, base)
    assert joint == width//2+breadth//2+10-3*epsilon >= 19
    if count_orders:
        canonical_labels = list(range(len(fixed)))+['B', 'R', 'A', 'J0', 'J1', 'J2', 'J3']
        expected = {(canonical_labels[owner], point, target) for owner, point, target in after['events']}
        for order in itertools.permutations(range(4)):
            records = fixed+additions+[cascade[index] for index in order]
            labels = list(range(len(fixed)))+['B', 'R', 'A']+['J'+str(index) for index in order]
            actual = inventory(records)
            assert actual['full'] == after['full']
            assert {(labels[owner], point, target) for owner, point, target in actual['events']} == expected
    return epsilon, joint


def ledger_controls():
    cases = corrections = 0
    least = None
    for origin, offset, old_width, width, depth in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20), (24, 80)):
        for breadth, consumer_far in ((6, 4), (width, depth-8),
                                     (width+2, 4), (width+2, depth-12)):
            epsilon, joint = ledger_case(origin, offset, [old_width, width], [depth, 24],
                                         breadth, consumer_far)
            cases += 1
            corrections += epsilon
            least = joint if least is None else min(least, joint)
    ledger_case(31, 0, [12, 12], [24, 24], 6, 4, True)
    ledger_case(31, 0, [12]*24, [24]*24, 14, 12)
    return dict(exact_full_tile_and_labelled_event_set_cases=cases+2,
                next_P_tight_corrections=corrections+1, least_joint_gain=least,
                horizontal_insertion_order_checks=24, long_chain_blocks=24)


def explicit_ledger():
    fixed, additions, cascade = witness(31, 0, [12, 12], [24, 24], 6, 8, 4, 6, 4)
    base = inventory(fixed)
    previous = fixed+additions
    previous_phi = phi_from(previous, inventory(previous))
    marginals = []
    for source in cascade:
        previous += [source]
        current_phi = phi_from(previous, inventory(previous))
        marginals.append(current_phi-previous_phi)
        previous_phi = current_phi
    after = inventory(previous)
    assert marginals == [-14, 0, 1, -22]
    increments = dict(mass=after['mass']-base['mass'],
        positive_owners=sum(charge(source) > 0 for source in additions+cascade),
        full_tiles=len(after['full']-base['full']), events=len(after['events']-base['events']))
    assert previous_phi-phi_from(fixed, base) == 19
    return dict(parameters=dict(old_width=12, width=12, depth=24, breadth=6, far=4),
                horizontal_dimensions=[[6+2*index, 40+2*index, 4] for index in range(4)],
                marginal_sequence=marginals, joint_gain=19, increments=increments,
                complete_extendibility='NOT_ASSERTED')


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', witnesses=witness_controls(),
        necessary=geometric_necessary_controls(), rotors=rotor_controls(),
        ledgers=ledger_controls(),
        explicit_partial_ledger=explicit_ledger(),
        scope='Finite controls supplement the general all-parameter forced-support staircase '
              'and geometric frontier proof. This does not prove complete extendibility, '
              'nonnegative arbitrary-family increments, a global5/6 improvement or grid equality.'), indent=2))
