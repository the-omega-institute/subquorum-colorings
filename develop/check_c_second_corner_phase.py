"""Physical controls for the C second-corner phase exclusion and typed pools."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cap_continuation_budget import phase_of
from check_critical_owner_profiles import anchored_images
from check_minus_one_tip_obstructions import source
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


BLOCKERS = {(0, -4), (0, -3), (0, -2), (0, -1),
            (1, -1), (2, -1), (3, -1)}


def north(width, incident, far):
    return transform_module(source(width, incident, far),
                            (False, True, False), (incident+1, -3))


def east(width, incident, far):
    return transform_module(source(width, incident, far),
                            (True, False, True), (2, -incident-2))


def orientation_controls():
    counts = Counter()
    for width, left, right in itertools.product((6, 8, 14), (4, 6, 12), (4, 8, 20)):
        expected = {frozenset(build(width, incident, far)['endpoints'])
                    for incident, far in ((left, right), (right, left))
                    for build in (north, east)}
        observed = set()
        for _, anchored in anchored_images(source(width, left, right)):
            current = transform_module(anchored, (False, False, False), (1, -2))
            if current['endpoints'] & BLOCKERS or phase_of(current) != '01':
                continue
            assert current['endpoints'] & {(0, -2), (0, -1), (1, -2), (1, -1)} == {(1, -2)}
            observed.add(frozenset(current['endpoints']))
            counts['anchored_phase01_survivors'] += 1
        assert observed == expected
        counts['independent_dimension_catalogues'] += 1
    return dict(counts)


def collision_controls():
    counts = Counter()
    for width, incident, far, other_width, other_incident, other_far in itertools.product(
            (6, 10), (4, 6, 10, 18), (4, 12), (6, 14), (4, 6, 8, 16), (4, 20)):
        current = transform_module(source(width, far, incident),
                                   (False, True, False), (incident+1, -width-1))
        other = north(other_width, other_incident, other_far)
        point = ((incident, -2) if other_incident+1 >= incident
                 else (other_incident+1, -1))
        assert point in current['endpoints'] & other['endpoints']
        assert phase_of(current) == phase_of(other) == '01'
        assert current['endpoints'] & {(0, -2), (0, -1), (1, -2), (1, -1)} == {(1, -1)}
        counts['north_crossings'] += 1
        companion = transform_module(source(width, incident, far),
                                     (True, False, False), (-1, -incident-1))
        other = east(other_width, other_incident, other_far)
        point = ((1, -incident) if other_incident+2 >= incident
                 else (0, -other_incident-2))
        assert point in companion['endpoints'] & other['endpoints']
        assert phase_of(companion) == '11' and phase_of(other) == '01'
        counts['east_crossings'] += 1
        counts['east_equality_boundary'] += int(other_incident+2 == incident)
    return dict(counts)


def pool_controls():
    counts = Counter()
    for claims in itertools.product(range(3), repeat=9):
        cap01, cap10, old01, old10, route_c, negative_c, interior_d, second_d01, second_d10 = claims
        if negative_c > route_c or second_d01+second_d10 > interior_d:
            continue
        used01 = cap01+old01+route_c+second_d01
        used10 = cap10+old10+negative_c+interior_d+second_d10
        unused01, unused10 = used01 % 2, used10 % 2
        source01, source10 = (used01+unused01)//2, (used10+unused10)//2
        assert used01+used10+unused01+unused10 == 2*(source01+source10)
        assert cap10+old10+negative_c+interior_d+second_d10 <= 2*source10
        if negative_c == route_c:
            assert cap10+old10+route_c+interior_d+second_d10 <= 2*source10
            counts['conditional_aa_typed_budgets'] += 1
        counts['conditional_joint_typed_budgets'] += 1
    return dict(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path)
    arguments = parser.parse_args()
    result = dict(status='PASS', orientation=orientation_controls(),
                  collisions=collision_controls(), pools=pool_controls(),
                  complete_critical_U10_realizations=0,
                  scope='Sampled independent U dimensions and conditional arithmetic only. '
                        'General crossing proofs are written and scoped in Lean. '
                        'No unrestricted allocation or grid equality.')
    rendered = json.dumps(result, indent=2)+'\n'
    if arguments.output:
        arguments.output.write_text(rendered)
    print(rendered, end='')


if __name__ == '__main__':
    main()
