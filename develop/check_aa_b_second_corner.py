"""Exact B rotor obstruction and AA incoming-owner/census controls."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_backfill_band_outputs import band_sources
from check_critical_owner_profiles import anchored_images
from check_minus_one_tip_obstructions import source
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


BLOCKERS = {(-1, -2), (-1, -1), (-1, 0), (-1, 1),
            (0, 1), (0, 2), (0, 3)}


def rotor_and_stencil_controls():
    images = {frozenset(module['endpoints']) for _, module in anchored_images(rotor())}
    assert len(images) == 16
    remaining = [points for points in images if not points & BLOCKERS]
    assert len(remaining) == 2
    assert all((1, 0) in points for points in remaining)
    count = 0
    for width, height, incident, far in itertools.product((6, 10, 18), (8, 12, 20),
                                                        (4, 6, 10), (4, 8)):
        companion, current = band_sources('B', width, height, 4, 6, incident, far)
        if incident > height-4 or companion['endpoints'] & current['endpoints']:
            continue
        second = (1, -incident-2)
        physical = {(row+second[0], column+second[1]) for row, column in BLOCKERS}
        assert physical <= companion['endpoints'] | current['endpoints']
        count += 1
    assert count > 0
    return dict(exact_rotor_roles=16, generic_survivors=2, survivors_with_incoming_endpoint=0,
                sampled_B_interior_stencils=count,
                surviving_relative_endpoint_sets=[sorted(points) for points in remaining])


def incoming_controls():
    counts = Counter()
    for width, first_short, lower_height, second_short, upper_height in itertools.product(
            (6, 10, 18), (4, 6, 10), (4, 6, 10, 20), (4, 6, 12), (4, 6, 12, 20)):
        if lower_height < first_short or upper_height < second_short:
            continue
        lower = transform_module(source(width, lower_height, 4),
                                 (False, True, False), (lower_height+2, 4))
        if lower_height == first_short:
            assert (first_short+1, 7) in lower['endpoints']
            assert (first_short, 7) not in lower['endpoints']
            counts['equal_height_companion_pair_collisions'] += 1
            continue
        assert lower_height >= first_short+2
        assert (first_short+1, 6) not in lower['endpoints']
        offset = first_short+second_short-upper_height-1
        upper = transform_module(source(width+2, upper_height, 8),
                                 (False, False, False), (offset, 4))
        common = (first_short+1, 5)
        distinguished = (offset, 6)
        assert common in lower['endpoints'] & upper['endpoints']
        assert distinguished in upper['endpoints']-lower['endpoints']
        counts['distinct_opposite_incoming_owner_collisions'] += 1
        counts['upper_equal_short_boundary'] += int(upper_height == second_short)
    assert counts['distinct_opposite_incoming_owner_collisions'] > 0
    return dict(counts=counts,
                scope='Intentional endpoint collisions refute the proposed simultaneous owners; '
                      'these are not complete feasible AA examples.')


def ledger_controls():
    count = 0
    for phase11, old, route_c, interior_d, unused in itertools.product(
            range(3), range(3), range(3), range(3), range(3)):
        interior_b = 0
        pool = 2*phase11+old+2*route_c+2*interior_d+interior_b+unused
        if pool % 2:
            continue
        for cap_d in range(2*phase11+1):
            for route_a in range(2*phase11-cap_d+1):
                unselected = 2*phase11-cap_d-route_a
                all_routes = route_a+interior_b+route_c+cap_d+interior_d
                retained = all_routes+route_c+interior_d+old+unselected
                assert pool == retained+unused
                assert retained <= pool
                assert (2-interior_b)+interior_b == 2
                count += 1
    assert count > 0
    return dict(conditional_AA_negative_only_all_route_identities=count,
                scope='Conditional source-occurrence arithmetic; not complete source fusions.')


def negative_terminal_crossings():
    counts = Counter()
    for companion_width, height, short_height, width, incident in itertools.product(
            (6, 10, 18), (8, 12, 20, 40), (4, 6, 10), (6, 8, 14), (4, 6, 10, 20, 40)):
        if height < short_height+4:
            continue
        companion = transform_module(source(companion_width, height, 4),
                                     (False, True, True), (height, 8))
        current = transform_module(source(width, incident, 8),
                                   (False, True, False), (short_height+incident+1, 5))
        if short_height+incident+1 >= height-1:
            collision = (height-1, 6)
            counts['terminal_stem_crosses_companion_bar'] += 1
        else:
            collision = (short_height+incident+1, 7)
            counts['terminal_bar_crosses_companion_stem'] += 1
        assert collision in companion['endpoints'] & current['endpoints']
    assert all(counts.values())
    return dict(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = dict(status='PASS', rotor_and_stencil=rotor_and_stencil_controls(),
                  incoming_owners=incoming_controls(), ledgers=ledger_controls(),
                  negative_terminal_crossings=negative_terminal_crossings(),
                  complete_critical_U10_realizations=0, complete_AA_realizations=0,
                  scope='Fixed rotor catalogue and sampled incoming-owner collisions supplement '
                        'general written proofs. No unrestricted allocation or grid equality.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
