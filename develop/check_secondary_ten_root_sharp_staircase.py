"""Exact physical controls for the sharp actual-staircase compensation theorem."""

import itertools
import json
import random

from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_root_actual_staircase import check_case as previous_case
from check_secondary_ten_root_fourth_consumer import originals
from check_secondary_ten_root_support_staircase import horizontal


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check_case(origin, offset, widths, depths, breadth, consumer_far, dimensions,
               receiver_far=4, root_breadth=6, receiver_breadth=8):
    result = previous_case(origin, offset, widths, depths, breadth, consumer_far,
                           dimensions, receiver_far, root_breadth, receiver_breadth)
    old_width, width = widths[:2]
    stairs = [horizontal(origin, offset, old_width, index, *parameters)
              for index, parameters in enumerate(dimensions)]
    upper_rows = {(origin-9)//2, (origin-11)//2, (origin-13)//2}
    interacting_pairs = []
    pair_total = 0
    for first, second in itertools.combinations(range(4), 2):
        current = inventory([stairs[first], stairs[second]])
        tiles = {tile for tile in current['full'] if tile[0] not in upper_rows}
        events = {event for event in current['events'] if event[1][0]//2 not in upper_rows}
        if tiles or events:
            assert (first, second) == (1, 2)
            assert origin-11+dimensions[1][0]+1 == origin-12+dimensions[2][0]
            interacting_pairs.append([first, second])
        pair_total += 2*len(tiles)-len(events)
    assert pair_total >= -1
    assert result['bottom_far_intervals']+result['old_A_events'] <= 2
    shared_width = dimensions[3][1]-old_width-12
    assert result['bottom_far_total_length'] <= shared_width
    assert result['far_budget'] >= -result['bottom_far_total_length']//2-3
    assert result['far_budget'] >= -shared_width//2-3
    assert result['joint_gain'] >= breadth//2+3 >= 6
    result.update(sharp_lower_bound=breadth//2+3, interacting_far_pairs=interacting_pairs,
                  staircase_pair_receipt=pair_total)
    return result


def sharp_dimensions(old_width, width, depth, breadth):
    return [[6, old_width+breadth+16, 4],
            [8, old_width+breadth+18, 6],
            [10, old_width+breadth+20, 4],
            [depth-2, old_width+width+22, width+10]]


def equality_controls():
    results = []
    for origin, offset, old_width, width, depth in itertools.product(
            (-33, 31), (-100, 200), (12, 50), (12, 20, 50), (24, 80)):
        for breadth in sorted({6, 12, width}):
            ordinal = len(results)
            root_breadth = 6 if ordinal % 2 else 40
            receiver_breadth = root_breadth+2+(ordinal % 3)*2
            receiver_far = 4 if ordinal % 3 else 2000
            count = 2 if ordinal % 2 else 5
            result = check_case(origin, offset, [old_width, width]+[12]*(count-2),
                                [depth]+[24]*(count-1), breadth, 6,
                                sharp_dimensions(old_width, width, depth, breadth),
                                receiver_far, root_breadth, receiver_breadth)
            assert result['joint_gain'] == breadth//2+3
            assert result['staircase_pair_receipt'] == -1
            assert result['bottom_far_intervals'] == result['old_A_events'] == 1
            assert result['ignored_cooperative_tiles'] == 0
            results.append(result)
    return results


def sampled_controls():
    rng = random.Random(221032)
    cases = []
    for old_width, width, depth, breadth, consumer_far in (
            (12, 12, 24, 6, 4), (12, 12, 24, 6, 6),
            (12, 20, 40, 12, 10), (50, 20, 80, 22, 68)):
        fixed, additions, sites = originals(31, 0, [old_width, width], [depth, 24],
                                            6, 8, 4, breadth, consumer_far)
        blocked = set.union(*(source[0] for source in fixed+additions))
        accepted = 0
        for attempt in range(50000):
            incidents = sorted(rng.sample(range(old_width+breadth+14, old_width+width+23, 2), 4))
            occupied = set(blocked)
            dimensions = []
            for index, incident in enumerate(incidents):
                height = rng.choice(range(6, depth+index-4, 2))
                far = rng.choice(range(4, incident-old_width+1, 2))
                candidate = horizontal(31, 0, old_width, index, height, incident, far)
                if candidate[0] & occupied:
                    break
                dimensions.append([height, incident, far])
                occupied |= candidate[0]
            if len(dimensions) != 4:
                continue
            cases.append(check_case(31, 0, [old_width, width], [depth, 24], breadth,
                                    consumer_far, dimensions))
            accepted += 1
            if accepted >= 24:
                break
    return cases


if __name__ == '__main__':
    equalities = equality_controls()
    samples = sampled_controls()
    targeted = [
        check_case(31, 0, [12, 20], [24, 24], 6, 4,
                   [[6, 34, 4], [20, 40, 16], [8, 46, 4], [22, 54, 12]]),
        check_case(-33, 200, [12]*24, [24]*24, 6, 6,
                   sharp_dimensions(12, 12, 24, 6), 2000, 40, 42),
        check_case(31, 0, [12, 12], [24, 24], 14, 12,
                   [[16, 40, 4], [18, 42, 4], [20, 44, 4], [22, 46, 4]]),
        check_case(31, 0, [12, 12], [24, 24], 6, 8,
                   [[6, 34, 4], [8, 36, 6], [10, 38, 4], [12, 46, 16]])
    ]
    explicit = check_case(31, 0, [12, 12], [24, 24], 6, 6,
                          sharp_dimensions(12, 12, 24, 6))
    assert explicit['joint_gain'] == 6
    assert targeted[0]['bottom_far_intervals'] == 2
    assert targeted[1]['joint_gain'] == 6
    assert targeted[3]['old_A_events'] == 2 and targeted[3]['bottom_far_intervals'] == 0
    print(json.dumps(dict(status='PASS', exact_equality_family_controls=len(equalities),
        sampled_controls=len(samples), least_sampled_gain=min(case['joint_gain'] for case in samples),
        sampled_pair_contacts=sum(bool(case['interacting_far_pairs']) for case in samples),
        sampled_A_debit_cases=sum(bool(case['old_A_events']) for case in samples),
        sampled_two_A_debit_cases=sum(case['old_A_events'] == 2 for case in samples),
        targeted_controls=targeted, exact_sharp_witness=explicit,
        scope='The written all-parameter proof gives DeltaPhi>=L/2+3>=6. '
              'The unbounded equality family is proved geometrically in the note; finite '
              'set controls do not prove generality. No complete-extension assertion or '
              'global-family allocation.'), indent=2))
