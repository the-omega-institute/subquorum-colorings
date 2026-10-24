"""Exact-set controls of compensation for arbitrary actual root staircase dimensions."""

import itertools
import json
import random

from check_incident_eight_north_transfer import charge
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_root_fourth_consumer import originals, allowed
from check_secondary_ten_root_support_staircase import horizontal


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check_case(origin, offset, widths, depths, breadth, consumer_far, dimensions,
               receiver_far=4, root_breadth=6, receiver_breadth=8):
    old_width, width, depth = widths[0], widths[1], depths[0]
    fixed, additions, sites = originals(origin, offset, widths, depths, root_breadth, receiver_breadth,
                                        receiver_far, breadth, consumer_far)
    stairs = [horizontal(origin, offset, old_width, index, *parameters)
              for index, parameters in enumerate(dimensions)]
    records = fixed+additions+stairs
    assert len(dimensions) == 4
    assert old_width+breadth+14 <= dimensions[0][1]
    assert dimensions[3][1] <= old_width+width+22
    assert all(dimensions[index-1][1]+2 <= dimensions[index][1] for index in range(1, 4))
    assert all(height >= 6 and far >= 4 and height < depth+index-4
               and all(parameter % 2 == 0 for parameter in (height, incident, far))
               for index, (height, incident, far) in enumerate(dimensions))
    assert len(set.union(*(source[0] for source in records))) == sum(len(source[0]) for source in records)
    before, after = inventory(fixed+additions), inventory(records)
    assert [charge(source) for source in stairs] == [-1, 1, -1, 1]
    initial_owner = len(fixed)+3
    parent_owner, consumer_owner = len(fixed), len(fixed)+2
    old_P_owner, rotor_owner = 9*len(widths)+1, 10*len(widths)+1
    column = offset+old_width+12
    first_column = column-dimensions[1][1]
    third_column = column-dimensions[3][1]
    near_rows = {(origin-9)//2, (origin-11)//2, (origin-13)//2}
    new_full = after['full']-before['full']
    new_events = after['events']-before['events']
    expected_near_full = {((origin-9)//2, current//2)
                         for current in range(offset+2-breadth, column+1, 2)}
    expected_near_full |= {((origin-11)//2, current//2)
                          for current in range(first_column, column+1, 2)}
    expected_near_full |= {((origin-13)//2, current//2)
                          for current in range(third_column, column+1, 2)}
    assert {tile for tile in new_full if tile[0] in near_rows} == expected_near_full
    expected_near_events = {(initial_owner, (origin-9, current), (origin-8, current))
                            for current in range(offset+2-breadth, column+1, 2)}
    expected_near_events |= {(consumer_owner, (origin-8, current), (origin-9, current))
                             for current in range(offset+1-breadth, offset+1)}
    expected_near_events |= {(old_P_owner, (origin-8, current), (origin-9, current))
                             for current in range(offset+1, column+1)}
    expected_near_events.add((parent_owner, (origin-10, column+1), (origin-10, column)))
    expected_near_events |= {(initial_owner+2 if current % 2 == 0 else initial_owner+1,
                             (origin-11 if current % 2 == 0 else origin-10, current),
                             (origin-10 if current % 2 == 0 else origin-11, current))
                            for current in range(first_column, column+1)}
    expected_near_events |= {(parent_owner, (origin-13, current), (origin-12, current))
                             for current in range(third_column, column+1)}
    expected_near_events |= {(initial_owner+3, (origin-12, current), (origin-13, current))
                             for current in range(third_column+1, column, 2)}
    expected_near_events.add((parent_owner, (origin-12, column+1), (origin-12, column)))
    assert {event for event in new_events if event[1][0]//2 in near_rows} == expected_near_events
    far_full = new_full-expected_near_full
    far_events = new_events-expected_near_events
    paid_full, paid_events = set(), set()
    pair_total = 0
    for first, second in itertools.combinations(range(4), 2):
        current = inventory([stairs[first], stairs[second]])
        tiles = {tile for tile in current['full'] if tile[0] not in near_rows}
        events = {(initial_owner+(first if owner == 0 else second), point, target)
                  for owner, point, target in current['events'] if point[0]//2 not in near_rows}
        assert tiles <= far_full and events <= far_events
        assert not paid_full & tiles and not paid_events & events
        if first % 2 == second % 2:
            assert not tiles and not events
        assert 2*len(tiles)-len(events) >= -1
        paid_full |= tiles
        paid_events |= events
        pair_total += 2*len(tiles)-len(events)
    assert pair_total >= -4
    bottom_row = (origin+depth-15)//2
    bottom_full = {tile for tile in far_full if tile[0] == bottom_row}
    bottom_events = {event for event in far_events-paid_events if event[1][0]//2 == bottom_row}
    bottom_indices = [index for index in (1, 3)
                      if origin-10-index+dimensions[index][0] == origin+depth-15]
    bottom_count = len(bottom_indices)
    bottom_length = sum(dimensions[index][2] for index in bottom_indices)
    assert 2*len(bottom_full)-len(bottom_events) == -bottom_length//2-bottom_count
    if bottom_count:
        assert bottom_length <= dimensions[3][1]-old_width-12-2*(bottom_count-1)
    assert 2*len(bottom_full)-len(bottom_events) >= -(dimensions[3][1]-old_width-12)//2-1
    assert not paid_full & bottom_full and not paid_events & bottom_events
    paid_full |= bottom_full
    paid_events |= bottom_events
    point_owner = {point: owner for owner, source in enumerate(records) for point in source[0]}
    remainder_events = far_events-paid_events
    old_A = old_rotor = 0
    rotor_tiles = set()
    for owner, point, target in remainder_events:
        assert owner in (consumer_owner, rotor_owner)
        current_index = point_owner[target]-initial_owner
        assert current_index in (1, 3)
        far_row = origin-10-current_index+dimensions[current_index][0]
        endpoint_column = column-dimensions[current_index][1]+dimensions[current_index][2]
        if owner == consumer_owner:
            assert point == (far_row, offset+1-breadth)
            assert target == (far_row, endpoint_column)
            assert endpoint_column == offset-breadth
            old_A += 1
        else:
            assert far_row == origin-3 and endpoint_column == offset-2
            assert target == (origin-3, offset-2)
            assert point in {(origin-3, offset-1), (origin-2, offset-2)}
            rotor_tiles.add(((origin-3)//2, (offset-2)//2))
            old_rotor += 1
    assert old_A <= 2 and old_rotor <= 2
    assert rotor_tiles <= far_full-paid_full
    assert old_rotor == 2*len(rotor_tiles)
    paid_full |= rotor_tiles
    far_budget = 2*len(far_full)-len(far_events)
    joint = phi_from(records, after)-phi_from(fixed, inventory(fixed))
    predicted_base = old_width//2+width+breadth//2+22-dimensions[3][1]//2
    assert joint == predicted_base+far_budget
    assert far_budget >= -4-(dimensions[3][1]-old_width-12)//2-1-2
    assert joint >= breadth//2-1 >= 2
    return dict(dimensions=dimensions, joint_gain=joint, far_budget=far_budget,
                lower_bound=breadth//2-1, bottom_far_intervals=bottom_count,
                bottom_far_total_length=bottom_length, old_A_events=old_A,
                old_rotor_events=old_rotor,
                ignored_cooperative_tiles=len(far_full-paid_full))


def sampled_controls():
    rng = random.Random(221031)
    cases = []
    for old_width, width, depth, breadth, consumer_far in (
            (12, 12, 24, 6, 4), (12, 20, 24, 6, 4), (12, 50, 24, 6, 4)):
        fixed, additions, sites = originals(31, 0, [old_width, width], [depth, 24], 6, 8, 4,
                                            breadth, consumer_far)
        blocked = set.union(*(source[0] for source in fixed+additions))
        accepted = 0
        for attempt in range(70000):
            incidents = sorted(rng.sample(range(old_width+breadth+14, old_width+width+23, 2), 4))
            occupied = set(blocked)
            dimensions = []
            for index, incident in enumerate(incidents):
                height = rng.choice(range(6, depth+index-4, 2))
                far = rng.choice(range(4, incident-old_width+1, 2))
                if index == 0 and not allowed(old_width, width, depth, breadth, consumer_far,
                                              height, incident, far, True):
                    break
                source = horizontal(31, 0, old_width, index, height, incident, far)
                if source[0] & occupied:
                    break
                dimensions.append([height, incident, far])
                occupied |= source[0]
            if len(dimensions) != 4:
                continue
            cases.append(check_case(31, 0, [old_width, width], [depth, 24], breadth,
                                    consumer_far, dimensions))
            accepted += 1
            if accepted >= 40:
                break
    return cases


if __name__ == '__main__':
    sampled = sampled_controls()
    targeted = [
        check_case(31, 0, [12, 20], [24, 24], 6, 4,
                   [[6, 34, 4], [20, 40, 16], [8, 46, 4], [22, 54, 12]]),
        check_case(31, 0, [12, 12], [24, 24], 6, 8,
                   [[6, 34, 4], [8, 38, 8], [10, 40, 4], [12, 46, 4]]),
        check_case(-33, 200, [12]*24, [24]*24, 6, 8,
                   [[6, 34, 4], [8, 38, 8], [10, 40, 4], [12, 46, 4]], 2000)
    ]
    assert targeted[0]['bottom_far_intervals'] == 2
    assert targeted[1]['old_A_events'] > 0
    explicit = check_case(31, 0, [12, 12], [24, 24], 6, 4,
                         [[16, 32, 4], [10, 38, 4], [20, 44, 12], [22, 46, 20]])
    assert explicit['joint_gain'] == 9
    print(json.dumps(dict(status='PASS', sampled_exact_set_controls=len(sampled),
        least_tested_joint_gain=min(case['joint_gain'] for case in sampled),
        least_all_checked_joint_gain=min(case['joint_gain'] for case in sampled+targeted+[explicit]),
        two_bottom_interval_cases=sum(case['bottom_far_intervals'] == 2 for case in sampled),
        old_A_event_cases=sum(case['old_A_events'] > 0 for case in sampled),
        old_rotor_event_cases=sum(case['old_rotor_events'] > 0 for case in sampled),
        targeted_boundary_controls=targeted,
        explicit_nonuniform_example=explicit,
        scope='Exact physical SET checks for a separate general proof for arbitrary actual '
              'staircase dimensions. Random samples are reproducible controls, not a proof '
              'or an exhaustive grid/complete-family classification. Other owners and global '
              'allocation remain OPEN.'), indent=2))
