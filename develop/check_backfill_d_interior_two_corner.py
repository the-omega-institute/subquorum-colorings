"""D-interior second-corner source stencils and conditional single-pool controls."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_backfill_band_outputs import band_sources
from check_backfill_corner_routing import rotor_catalogue
from check_cap_continuation_budget import phase_of
from check_critical_owner_profiles import anchored_images
from check_minus_one_tip_obstructions import source
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


BLOCKERS = {(-1, -2), (-1, -1), (-1, 0), (-1, 1),
            (0, 1), (1, 1), (2, 1)}
TILE = {(-1, 0), (-1, 1), (0, 0), (0, 1)}


def stencil_controls():
    counts = Counter()
    parameters = itertools.product((6, 10, 18), (6, 8, 12, 20), (4, 10),
                                   (6, 8, 14), (4, 6, 10, 18), (4, 8, 16))
    for companion_width, height, companion_far, width, incident, far in parameters:
        companion, current = band_sources('D', companion_width, height, companion_far,
                                          width, incident, far)
        if companion['endpoints'] & current['endpoints'] or incident > height-4:
            continue
        second = (1, -incident-2)
        first = (1, -incident-1)
        from_companion = {(0, column) for column in range(-incident-4, -incident)}
        from_current = {(row, -incident-1) for row in (1, 2, 3)}
        assert from_companion <= companion['endpoints']
        assert from_current <= current['endpoints']
        relative = {(row-second[0], column-second[1])
                    for row, column in from_companion | from_current}
        assert relative == BLOCKERS
        cells = {(row+second[0], column+second[1]) for row, column in TILE}
        assert companion['endpoints'] & cells == {(0, -incident-2), (0, -incident-1)}
        assert current['endpoints'] & cells == {first}
        assert second not in companion['endpoints'] | current['endpoints']
        counts['endpoint_disjoint_D_interior_stencils'] += 1
    assert counts['endpoint_disjoint_D_interior_stencils'] == 264
    return dict(counts=counts, rotor=rotor_catalogue((0, 0), BLOCKERS),
                complete_critical_U10_realizations=0)


def singleton_controls():
    counts = Counter()
    second = (1, -2)
    blockers = {(row+second[0], column+second[1]) for row, column in BLOCKERS}
    cells = {(row+second[0], column+second[1]) for row, column in TILE}
    supports = {(0, -2), (1, -1)}
    for dimensions in itertools.product((6, 8, 14), (4, 6), (4, 8, 12)):
        for _, anchored in anchored_images(source(*dimensions)):
            module = transform_module(anchored, (False, False, False), second)
            if module['endpoints'] & blockers:
                continue
            assert module['endpoints'] & cells == {second}
            phase = phase_of(module)
            assert phase in ('00', '01', '10')
            if phase == '00':
                assert module['selected'] & cells == supports
            counts['sampled_singleton_phase_'+phase] += 1
    assert all(counts['sampled_singleton_phase_'+phase] for phase in ('00', '01', '10'))
    return dict(counts=counts,
                scope='Sampled U dimensions only; the general singleton catalogue is a written input. '
                      'Anchored images can repeat a source image. No complete critical realization.')


def ledger_controls():
    counts = Counter()
    parameters = itertools.product(range(3), range(2), range(2), range(3),
                                   range(3), range(3), range(2))
    for negative_cap, old, route_c, negative_c, interior_d, negative_d, unused in parameters:
        if negative_c > route_c or negative_d > interior_d:
            continue
        positive_c, positive_d = route_c-negative_c, interior_d-negative_d
        negative_pool = negative_cap+old+route_c+negative_c+interior_d+negative_d+unused
        if negative_pool % 2:
            continue
        negative_sources = negative_pool//2
        for positive_cap, unfilled, interior_b, slack, rotor, boundary in itertools.product(
                range(2), range(3), range(2), range(2), range(2), range(3)):
            cap_count = negative_cap+positive_cap+unfilled
            if cap_count % 2:
                continue
            phase11 = cap_count//2
            activation = positive_cap+positive_c+interior_b+positive_d+slack
            twice_reserve = activation+unfilled+rotor+boundary
            if twice_reserve % 2:
                continue
            new_retained = 2*(phase11-negative_sources)+old+2*route_c+2*interior_d+interior_b
            old_retained = new_retained-interior_d
            old_unused = negative_d+unused
            old_slack = activation-positive_cap-positive_c-interior_b
            assert old_slack+old_unused == slack+unused+interior_d
            assert twice_reserve == new_retained+slack+rotor+boundary+unused
            assert new_retained+rotor+boundary <= twice_reserve
            assert 2*phase11+old+2*route_c+2*interior_d+interior_b <= (
                2*negative_sources+activation+unfilled)
            for route_a in range(cap_count+1):
                selected_left = cap_count-route_a
                cap_b = min(positive_cap, selected_left)
                cap_d = min(negative_cap, selected_left-cap_b)
                unselected = cap_count-route_a-cap_b-cap_d
                all_routes = route_a+cap_b+interior_b+route_c+cap_d+interior_d
                all_retained = all_routes+route_c+interior_d-2*negative_sources+old+unselected
                assert all_retained == new_retained
                assert all_routes+route_c+interior_d+old+unselected <= (
                    2*negative_sources+activation+unfilled)
                terminal = slack
                counted = activation+terminal
                old_stops, rotor_stops = boundary, rotor
                assert counted+old_stops+rotor_stops+all_retained+unused <= (
                    twice_reserve+activation)
                counts['conditional_all_route_and_shared_ledger_instances'] += 1
            counts['conditional_enlarged_pool_instances'] += 1
            counts['strict_improvements_over_old_retained_term'] += int(new_retained > old_retained)
            counts['negative_source_census_instances'] += int(phase11 < negative_sources)
    assert counts['strict_improvements_over_old_retained_term'] > 0
    assert counts['negative_source_census_instances'] > 0
    return dict(counts)


def aa_controls():
    counts = Counter()
    companion_arm = {(-1, -1), (-1, -2)}
    corner_arm = {(1, 1), (2, 1)}
    for symmetry in itertools.product((False, True), repeat=3):
        if {affine((-1, 0), symmetry), affine((0, 1), symmetry)} != {(1, 0), (0, 1)}:
            continue
        arms = [{affine(point, symmetry) for point in arm}
                for arm in (companion_arm, corner_arm)]
        assert sum(arm == {(1, -1), (1, -2)} for arm in arms) == 1
        counts['compatible_terminal_support_frames'] += 1
    assert counts['compatible_terminal_support_frames'] == 2
    for width, short_height, height, far in itertools.product(
            (6, 10, 18), (4, 6, 10, 20), (4, 6, 10, 20, 40), (4, 8, 16)):
        if height < short_height:
            continue
        incoming = transform_module(source(width, height, far),
                                    (False, True, False), (height+2, 4))
        assert (short_height+1, 5) in incoming['endpoints']
        assert (short_height+1, 4) not in incoming['endpoints']
        counts['incoming_original_owner_boundary_controls'] += 1
        counts['height_equals_short_boundary_controls'] += int(height == short_height)
    return dict(counts=counts,
                scope='All eight signed frames, exactly two compatible; sampled legal incoming '
                      'owners including equal-height boundary. These are adapters, not complete AA fusions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = dict(status='PASS', stencils=stencil_controls(),
                  singleton_samples=singleton_controls(), ledgers=ledger_controls(),
                  aa=aa_controls(),
                  scope='Exact finite rotor template; sampled complete F/H source stencils and U '
                        'singleton roles; conditional ledgers. General proof and nonreuse are written. '
                        'No complete critical U10 realizability, unrestricted allocation or grid equality.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
