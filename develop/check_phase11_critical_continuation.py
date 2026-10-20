"""Critical occupied-band geometry and exact physical-corner/tag controls."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from check_cap_continuation_budget import phase_of
from check_minus_one_tip_obstructions import source
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def exact_frames():
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    frames = [(first, second) for first, second in itertools.product(directions, repeat=2)
              if sum(left*right for left, right in zip(first, second)) == 0]

    def tags(frame, kind):
        first, second = frame
        if kind == 'critical':
            active = {(first[0]+step*second[0], first[1]+step*second[1])
                      for step in (-1, 0, 1)}
            corner = {(-step*second[0], -step*second[1]) for step in (1, 2)}
        else:
            active = {(step*first[0]-second[0], step*first[1]-second[1])
                      for step in (-1, 0, 1)}
            corner = {(-first[0]+step*second[0], -first[1]+step*second[1])
                      for step in (0, 1)}
        assert not active & corner
        return {**{point: first for point in active},
                **{point: second if kind == 'first' else None for point in corner}}

    def diagonal(frame, kind):
        first, second = frame
        difference = (second[0]-first[0], second[1]-first[1])
        return difference if kind == 'critical' else tuple(-value for value in difference)

    counts = Counter()
    for first, second in itertools.product(frames, repeat=2):
        critical = tags(first, 'critical')
        for kind in ('critical', 'long', 'first'):
            other = tags(second, kind)
            compatible = all(critical[point] == other[point]
                             for point in critical.keys() & other.keys())
            same_tile_corner = diagonal(first, 'critical') == diagonal(second, kind)
            counts[kind+'_ordered_frame_pairs'] += 1
            counts[kind+'_tag_only_survivors'] += compatible
            counts[kind+'_tag_and_partition_survivors'] += compatible and same_tile_corner
            assert (compatible and same_tile_corner) == (kind == 'critical' and first == second)
    return dict(counts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    counts = Counter()
    examples = []
    for active_width, width, left, right, far in itertools.product(
            (10, 14, 20), (6, 8, 12), (4, 6, 10), (4, 8), (4, 6)):
        active = width+2
        parent = transform_module(source(active_width, active, far),
                                  (False, False, False), (2-active, -1))
        for reflected in (False, True):
            base = source(width, left, right)
            symmetry = (True, False, reflected)
            anchor = (0, 1) if reflected else (0, width)
            root = affine(anchor, symmetry)
            child = transform_module(base, symmetry, (1-root[0], 1-root[1]))
            assert [phase_of(parent), phase_of(child)] == ['01', '11']
            counts['critical_original_source_pairs'] += 1
            height = right if reflected else left
            collision = parent['endpoints'] & child['endpoints']
            if height >= active_width-2:
                assert (2-width, active_width-1) in collision
                counts['opposite_leg_far_stem_collisions'] += 1
            if collision:
                counts['endpoint_collision_pairs'] += 1
                continue
            assert height+4 <= active_width
            counts['endpoint_disjoint_partial_pairs'] += 1
            point = (2-width, height+2)
            assert point in child['selected']
            assert point not in parent['endpoints'] | child['endpoints']
            assert (point[0]-1, point[1]) in parent['endpoints']
            assert (point[0], point[1]-1) in child['endpoints']
            assert {(point[0]-1, point[1]+step) for step in (-1, 0, 1)} <= parent['endpoints']
            assert {(point[0], point[1]-step) for step in (1, 2)} <= child['endpoints']
            for image in itertools.product((False, True), repeat=3):
                transpose, flip_row, flip_column = image
                offset = (int(flip_column), int(flip_row)) if transpose else (int(flip_row), int(flip_column))
                move = lambda site: affine(site, image, offset)
                moved_point = move(point)
                north, east = affine((-1, 0), image), affine((0, 1), image)
                expected = (east[0]-north[0], east[1]-north[1])
                actual = tuple(1 if value % 2 == 0 else -1 for value in moved_point)
                assert actual == expected
                moved_first = move((1, 1))
                assert tuple(1 if value % 2 == 0 else -1 for value in moved_first) == tuple(-value for value in expected)
                counts['physical_partition_preserving_images'] += 1
            if len(examples) < 3:
                examples.append(dict(active_width=active_width, active=active,
                                     child_dimensions=(width, left, right), reflected=reflected,
                                     forced_critical_point=point, partial_only=True))
    assert counts['endpoint_disjoint_partial_pairs'] > 0
    frames = exact_frames()
    result = dict(status='PASS', counts=dict(counts), exact_frame_controls=frames,
                  partial_examples=examples, complete_feasible_phase11_exit_coverage=0,
                  complete_closed01_contact_coverage=0, complete_AA_coverage=0,
                  scope='Original endpoint/support geometry, actual aligned-partition corner '
                  'diagonals under all eight preserving isometries, and exact orientation '
                  'tag/partition exhaustion. Partial pairs are not complete feasible '
                  'configurations or target counterexamples. General claims use written '
                  'arbitrary-dimension proofs and Lean statements.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', counts=dict(counts), exact_frame_controls=frames)))


if __name__ == '__main__':
    main()
