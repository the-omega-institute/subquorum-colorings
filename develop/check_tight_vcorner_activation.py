"""Reconstruct tight Vcorner forcing and collisions with prior activation targets."""

from collections import Counter
import itertools
import json

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import original
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def south_terminals():
    candidates = []
    for dimensions in itertools.product((6, 8, 10, 14, 20, 26),
                                        (4, 6, 8, 12, 18, 24), (4, 6, 10, 16)):
        for left in (False, True):
            module = original(dimensions, (False, True, left),
                              (dimensions[1], 1 if left else -1))
            assert (0, 0) in module['endpoints']
            assert set(neighbors((0, 0))) & module['endpoints'] == {(1, 0)}
            candidates.append((dimensions, left, module))
    return candidates


def rotor_controls():
    footprints = {}
    for symmetry in SYMMETRIES:
        module = transform_module(rotor(), symmetry)
        for point in module['endpoints']:
            if set(neighbors(point)) & module['endpoints'] != {(point[0]+1, point[1])}:
                continue
            moved = transform_module(module, (False, False, False), (-point[0], -point[1]))
            footprints[frozenset(moved['endpoints'])] = moved
    assert len(footprints) == 2
    assert all(points & {(1, 1), (2, 1)} for points in footprints)
    return len(footprints)


def forcing_controls():
    counts = Counter()
    examples = {}
    candidates = south_terminals()
    for height, cross_width, cross_far, corner_width, corner_far in itertools.product(
            (8, 12, 16, 24), (6, 8, 10, 14, 22), (4, 8), (6, 8, 12), (4, 6, 10)):
        cross = original((cross_width, height, cross_far),
                         (True, True, False), (1, height+2))
        corner = original((corner_width, height-4, corner_far),
                          (True, False, False), (2, 3))
        if cross['endpoints'] & corner['endpoints']:
            continue
        fixed = cross['endpoints'] | corner['endpoints']
        target = (3, height)
        assert target in corner['selected'] and target not in fixed
        assert {(3, height-1), (2, height), (3, height+1)} <= fixed
        counts['disjoint_C_X_patterns'] += 1
        survived = 0
        for dimensions, left, prototype in candidates:
            companion = transform_module(prototype, (False, False, False), target)
            if fixed & companion['endpoints']:
                continue
            width, leg, far = dimensions
            assert left
            assert companion['charge'] == 1
            assert 6 <= leg <= cross_width-4
            if width <= height-4:
                assert far <= leg-2
                counts['short_bar_longer_near'] += 1
            else:
                assert width >= height-2 and leg >= corner_width+2
                counts['wide_bar_below_corner'] += 1
            supports = {(2, height), (3, height+1)}
            assert supports <= companion['selected'] & cross['endpoints']
            tile = vertices_of({(1, height//2)})
            assert tile & companion['endpoints'] == {target}
            assert len(tile & cross['endpoints']) == 3
            assert tile <= fixed | companion['endpoints']
            assert cross_width >= 10
            if height == 8:
                assert cross_width >= corner_width+6
            counts['disjoint_C_X_Q_partial_patterns'] += 1
            survived += 1
            examples.setdefault('wide' if width >= height-2 else 'short', dict(
                cross=(cross_width, height, cross_far),
                corner=(corner_width, height-4, corner_far), companion=dimensions))
        if cross_width in (6, 8):
            assert survived == 0
            counts['small_cross_no_U_consumer_controls'] += 1
    assert counts['disjoint_C_X_Q_partial_patterns'] > 0
    return dict(counts=counts, partial_examples=examples,
                candidate_south_terminal_frames=len(candidates))


def prior_target_collisions():
    counts = Counter()
    for height, leg, cross_width in itertools.product((8, 12, 20, 28), (6, 8, 12, 20),
                                                       (10, 14, 24)):
        base = original((height+4, 4, 4))
        cross = original((cross_width, height, 4), (True, True, False), (1, height+2))
        old_singleton_producer = original((6, 4, 6), offset=(0, height-2))
        assert (0, height-1) in base['endpoints'] & old_singleton_producer['endpoints']
        assert all(column > 1 for _, column in old_singleton_producer['endpoints'])
        assert any(column == 1 for _, column in base['endpoints'])
        counts['old_S_collision_and_self_exclusion'] += 1
        old_pair_producer = original((leg+4, 4, 6),
                                     (True, True, True), (leg+5, height+3))
        assert (3, height+2) in cross['endpoints'] & old_pair_producer['endpoints']
        assert any(column == height+3 for _, column in old_pair_producer['endpoints'])
        assert all(column <= height+2 for _, column in cross['endpoints'])
        counts['old_P_collision_and_self_exclusion'] += 1
    return counts


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', excluded_south_rotor_footprints=rotor_controls(),
                         forcing=forcing_controls(), prior_targets=prior_target_collisions(),
                         scope='Independent original-source endpoint/support/phase controls. '
                               'C/X and C/X/Q examples are PARTIAL and are not claimed complete. '
                               'General consumer exhaustion, injectivity, cross-type support-owner '
                               'separation and simultaneous ledger are written proofs.'), indent=2))
