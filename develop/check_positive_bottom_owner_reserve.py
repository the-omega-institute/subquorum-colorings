"""Positive-image and distinct-leg controls for the unbounded bottom-owner obstruction."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_minus_one_tip_obstructions import source
from check_width_six_bottom_owner import candidates
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    parameters = list(itertools.product((6, 8, 12, 20), (4, 6, 10, 20), (4, 8, 12)))
    parameters += [(40, 30, 4), (20, 4, 30)]
    counts = Counter()
    records = []
    height = 10
    incoming = transform_module(source(12, height, 4), (False, True, False), (height+2, 1))
    for clearance in (4, 6, 8, 10, 14, 20, 32, 44):
        long = height+clearance
        positive = source(6, long, 4)
        target = height+3, 2
        blank = {(long+1, 2)}
        blocked = positive['endpoints'] | incoming['endpoints'] | {(long+1, 1)}
        surviving_positive = 0
        for dimensions, endpoint, symmetry, offset, endpoints, selected in candidates(
                parameters, target, blocked, blank, counts):
            module = transform_module(source(*dimensions), symmetry, offset)
            if module['charge'] != 1:
                continue
            width, left, right = dimensions
            assert endpoint in ((0, 1), (0, width))
            assert width <= clearance-4
            into_bar = affine((0, endpoint[1]+(1 if endpoint[1] == 1 else -1)), symmetry, offset)
            assert into_bar == (target[0]+1, target[1])
            near_support = target[0]-1, target[1]
            far_support = target[0]+width, target[1]
            assert {near_support, far_support} <= selected
            assert near_support in incoming['endpoints']
            far_anchor = target[0]+width-1, target[1]
            wall_anchor = target[0]+width, target[1]-1
            assert far_anchor in endpoints and wall_anchor in positive['endpoints']
            assert near_support != far_support
            surviving_positive += 1
            counts['positive_corner_with_two_consumed_leg_starts'] += 1
        records.append(dict(clearance=clearance, positive_survivors=surviving_positive))
    assert counts['positive_corner_with_two_consumed_leg_starts'] > 0
    assert all(record['positive_survivors'] == 0 for record in records if record['clearance'] <= 8)
    budgets = 0
    for near_activated, far_activated in itertools.product((False, True), repeat=2):
        activation = 1+int(near_activated)+int(far_activated)
        exterior = int(not near_activated)+int(not far_activated)
        assert activation+exterior == 3
        for extra_activation, extra_pool, rotor in itertools.product(range(5), repeat=3):
            defect = activation+extra_activation+exterior+extra_pool+rotor
            if defect%2:
                continue
            reserve = defect//2
            assert reserve >= 2
            budgets += 1
    result = dict(status='PASS', parameter_controls=len(parameters), role_controls=dict(counts),
                  clearance_contexts=records, distinct_leg_budget_cases=budgets,
                  new_complete_physical_fixture_coverage=0,
                  scope='Representative arbitrary-image positive source roles, forced consumption of two different original exterior bar-end supports, and all4 activation/exterior choices. Universal classification and reserve deductions are separately Lean-checked; physical A/X routes are accepted written dependencies. No complete feasible residual or arbitrary-grid theorem.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
