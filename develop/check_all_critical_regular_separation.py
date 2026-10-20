"""Exact shared-tile orientations and complete source owner collision controls."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from check_full_neutral_receivers import add, scale, tile
from check_minus_one_tip_obstructions import source
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def exact_shared_tile_cases():
    counts = Counter()
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    frames = [(first, second) for first, second in itertools.product(directions, repeat=2)
              if sum(value*other for value, other in zip(first, second)) == 0]
    critical = {(-1, -1): (-1, 0), (-1, 0): (-1, 0), (-1, 1): (-1, 0),
                (0, -1): None, (0, -2): None}
    square = {(0, 0), (1, 0), (0, 1), (1, 1)}
    survivors = set()
    for frame, point in itertools.product(frames, square):
        counts['frame_point_pairs'] += 1
        if tile(frame, point) != square:
            continue
        counts['same_physical_tile_cases'] += 1
        if point == (0, 0):
            counts['excluded_by_global_forced_point_separation'] += 1
            continue
        active = {add(point, add(scale(frame[0], step), scale(frame[1], -1))): frame[0]
                  for step in (-1, 0, 1, 2)}
        other = [add(point, add(scale(frame[0], -1), scale(frame[1], step)))
                 for step in (0, 1)]
        compatible = (all(critical[site] == value for site, value in active.items() if site in critical)
                      and all(critical[site] in (None, frame[1]) for site in other if site in critical))
        if compatible:
            survivors.add((point, frame))
    expected = {((1, 0), ((-1, 0), (0, -1))),
                ((1, 1), ((-1, 0), (0, 1))),
                ((0, 1), ((0, -1), (-1, 0)))}
    assert survivors == expected
    counts['tag_compatible_nonzero_cases'] = len(survivors)
    return dict(counts=counts, survivors=sorted(survivors))


def U_owner_controls():
    counts = Counter()
    for dimensions in itertools.product((6, 8, 14, 40), (4, 6, 12), (4, 8, 20)):
        base = source(*dimensions)
        for symmetry in itertools.product((False, True), repeat=3):
            for anchor in base['endpoints']:
                offset = tuple(-value for value in affine(anchor, symmetry))
                module = transform_module(base, symmetry, offset)
                counts['original_U_endpoint_images'] += 1
                if module['endpoints'] & {(-1, 0), (0, -1), (0, 1)}:
                    continue
                assert anchor in ((dimensions[1], 1), (dimensions[2], dimensions[0]))
                assert (1, 0) in module['endpoints'] and (2, 0) in module['endpoints']
                assert (2, -1) not in module['endpoints']
                counts['downward_terminal_survivors'] += 1
    return dict(counts)


def exact_rotor_owners():
    translated = {}
    for symmetry in itertools.product((False, True), repeat=3):
        for anchor in rotor()['endpoints']:
            offset = tuple(-value for value in affine(anchor, symmetry))
            module = transform_module(rotor(), symmetry, offset)
            translated[frozenset(module['endpoints'])] = module
    assert len(translated) == 16
    survivors = []
    for endpoints in translated:
        if endpoints & {(-1, 0), (0, -1), (0, 1)}:
            continue
        assert (2, 0) in endpoints
        survivors.append(sorted(endpoints))
    assert survivors
    return dict(all_rotor_translations_owning_origin=len(translated),
                three_blocker_survivors=len(survivors), survivors=survivors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = dict(status='PASS', normalized_shared_tile_controls=exact_shared_tile_cases(),
                  arbitrary_dimension_proof_controls=U_owner_controls(),
                  exact_rotor_owner_controls=exact_rotor_owners(),
                  complete_other_phase_critical_coverage=0, complete_AA_coverage=0,
                  scope='Exhaustive finite orientation and rotor-root roles; finite U endpoint images '
                        'control the separately proved arbitrary-dimension terminal lemma. '
                        'Physical original-owner/type/coordinate adapters are written. '
                        'The preceding complete fixture batch covers phase01 returns only. '
                        'Not critical-to-critical tile injection or the full allocation theorem.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
