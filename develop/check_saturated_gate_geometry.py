"""Role controls for saturated bad gates, including a common source owner."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import gate_roles
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def tip_forbidden(module, height):
    point = height+1, 2
    return point in module['endpoints'] | module['selected']


def classify(candidate):
    if candidate['phase'] == '01':
        return 'corner'
    if candidate['phase'] == '11' and candidate['predecessor'] == (0, 1):
        return 'horizontal_tip'
    if candidate['phase'] == '11' and candidate['predecessor'] == (1, 0):
        return 'vertical_tip'
    return 'activated_phase10'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    _, candidates = gate_roles()
    positive_parameters = list(itertools.product((6, 8, 10, 12, 14, 20), (4, 6, 8, 12),
                                                 (4, 6, 8, 12)))
    positive_parameters += [(40, 40, 4), (40, 4, 40)]
    counts = Counter()
    same_owner = Counter()
    pair_count = 0
    for width, left, right in positive_parameters:
        positive = source(width, left, right)
        horizontal = []
        for candidate in candidates:
            incoming = candidate['module']
            if incoming['endpoints'] & positive['endpoints'] or tip_forbidden(incoming, left):
                continue
            kind = classify(candidate)
            assert kind != 'activated_phase10'
            counts[kind] += 1
            height = candidate['height']
            incoming_width = candidate['parameters'][0]
            if kind == 'vertical_tip':
                assert height <= left-2
                assert incoming_width <= width-2 or right <= height <= left-2
                if left <= right:
                    assert incoming_width <= width-2
                    counts['shorter_side_width_descent'] += 1
                outward = {(height+2, 2), (height+2, 3)}
                tile = vertices_of({((height+2)//2, 1)})
                assert tile & incoming['endpoints'] == outward
                assert not tile & incoming['selected']
                if height == left-2:
                    assert (left+1, 2) in tile
                    counts['vertical_equality_excluded_by_saturation'] += 1
            else:
                assert {(2, column) for column in range(2, 7)} <= incoming['endpoints']
                horizontal.append(candidate)
            if (2, width-1) not in incoming['endpoints']:
                continue
            reflected = transform_module(incoming, (False, False, True), (0, width+1))
            if tip_forbidden(reflected, right):
                continue
            incoming_left = max(point[0] for point in incoming['endpoints'] if point[1] == 2)-2
            incoming_right = max(point[0] for point in incoming['endpoints'] if point[1] == width-1)-2
            upright = (source(width-2, incoming_left, incoming_right)
                       if width >= 8 and min(incoming_left, incoming_right) >= 4 else None)
            nested_upright = (transform_module(upright, (False, False, False), (2, 1))
                              if upright is not None else None)
            inverted = (transform_module(source(width-2, height, height),
                                         (False, True, False), (height+2, 1))
                        if width >= 8 and height >= 4 else None)
            if nested_upright is not None and incoming['endpoints'] == nested_upright['endpoints']:
                assert incoming['selected'] == nested_upright['selected']
                assert incoming_left <= left-4
                assert incoming_right <= right-4
                same_owner['upright'] += 1
            elif inverted is not None and incoming['endpoints'] == inverted['endpoints']:
                assert incoming['selected'] == inverted['selected']
                assert height <= min(left, right)-2
                same_owner['inverted'] += 1
            else:
                raise AssertionError('Unclassified common-owner two-gate source.')
        for first, second in itertools.product(horizontal, repeat=2):
            other = transform_module(second['module'], (False, False, True), (0, width+1))
            if other['endpoints'] & positive['endpoints'] or tip_forbidden(other, right):
                continue
            pair_count += 1
            if width <= 10:
                assert (2, 5) in first['module']['endpoints'] & other['endpoints']
    assert counts['corner'] and counts['horizontal_tip'] and counts['vertical_tip']
    assert counts['vertical_equality_excluded_by_saturation']
    assert same_owner['upright'] and same_owner['inverted']
    result = dict(status='PASS', positive_parameters=len(positive_parameters),
                  candidate_roles=len(candidates), role_counts=dict(counts),
                  common_owner_controls=dict(same_owner), horizontal_pair_controls=pair_count,
                  scope='Finite endpoint/support role controls, including both common-owner normal forms and nonvacuous vertical equality exclusions. Controls are not complete feasible fusions and do not prove global saturation impossible. Universal role/parity/support/full-tile arguments and the single-positive necessary dimension condition are written separately.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
