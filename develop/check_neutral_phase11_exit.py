"""Independent phase11 original-owner geometry controls, not complete configurations."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_minus_one_tip_obstructions import source
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def exact_frame_controls():
    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    frames = [(first, second) for first, second in itertools.product(directions, repeat=2)
              if sum(left*right for left, right in zip(first, second)) == 0]

    def tags(frame, is_corner):
        first, second = frame
        active = {(step*first[0]-second[0], step*first[1]-second[1])
                  for step in (-1, 0, 1)}
        passive = {(-first[0]+step*second[0], -first[1]+step*second[1])
                   for step in (0, 1)}
        assert not active & passive
        return {**{point: first for point in active},
                **{point: None if is_corner else second for point in passive}}

    def compatible(first, second):
        return all(first[point] == second[point] for point in first.keys() & second.keys())

    second_survivors = first_second_survivors = 0
    for first, second in itertools.product(frames, repeat=2):
        second_compatible = compatible(tags(first, True), tags(second, True))
        assert second_compatible == (first == second)
        second_survivors += second_compatible
        first_second_compatible = compatible(tags(first, False), tags(second, True))
        assert not first_second_compatible
        first_second_survivors += first_second_compatible
    return dict(second_frame_pairs=64, second_frame_survivors=second_survivors,
                first_second_frame_pairs=64, first_second_frame_survivors=first_second_survivors)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    blockers = {(1, 0), (2, 1), (0, 0), (2, 2)}
    passive = transform_module(source(6, 4, 4), (True, True, False), (1, 5))
    counts = Counter()
    witnesses = []
    for dimensions in itertools.product((6, 8, 14), (4, 6, 10, 20), (4, 8, 16)):
        width, left, right = dimensions
        base = source(*dimensions)
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            for anchor in sorted(base['endpoints']):
                root = affine(anchor, symmetry)
                module = transform_module(base, symmetry, (1-root[0], 1-root[1]))
                if phase_of(module) != '11':
                    continue
                counts['phase11_original_endpoint_images'] += 1
                origin = (anchor[0]-(0 if flip_row else 1),
                          anchor[1]-(0 if flip_column else 1))
                assert origin[0] % 2 == origin[1] % 2 == 1
                if blockers & module['endpoints']:
                    continue
                assert not flip_row
                counts['four_blocker_survivors'] += 1
                if not transpose:
                    assert anchor == ((left, 1) if flip_column else (right, width))
                    counts['west_facing_terminal_stencils'] += 1
                else:
                    assert anchor == ((0, 1) if flip_column else (0, width))
                    counts['outer_corner_stencils'] += 1
                    adjacent_tile = vertices_of({(0, 1)})
                    assert adjacent_tile & module['endpoints'] == {(0, 2), (1, 2), (1, 3)}
                    assert not adjacent_tile & module['selected']
                    assert {(0, 1), (1, 1)} <= module['endpoints']
                    assert {(row+1, 1) for row in range(1-width, 1)} <= module['endpoints']
                    counts['exact_adjacent_original_3P0T_tiles'] += 1
                for active in range(4, 44, 2):
                    parent = transform_module(source(14, active, 4),
                                              (False, False, False), (2-active, -1))
                    collision = parent['endpoints'] & module['endpoints']
                    if not transpose:
                        assert collision
                        counts['terminal_active_height_collisions'] += 1
                        continue
                    if collision:
                        counts['corner_active_height_collisions'] += 1
                        continue
                    counts['endpoint_disjoint_corner_stencils'] += 1
                    assert active >= width+2
                    top_support = (1-width, 1)
                    assert top_support in module['selected']
                    assert top_support not in module['endpoints']
                    if active == width+2:
                        assert top_support in parent['endpoints']
                        counts['boundary_support_consumed_by_active_bar'] += 1
                    else:
                        assert active >= width+4
                        assert top_support in parent['selected']
                        assert top_support not in parent['endpoints'] | passive['endpoints']
                        assert (1-width, 0) in parent['endpoints']
                        assert (2-width, 1) in module['endpoints']
                        assert {(row, 0) for row in (0-width, 1-width, 2-width)} <= parent['endpoints']
                        assert {(2-width, 1), (2-width, 2)} <= module['endpoints']
                        counts['second_forced_point_geometry'] += 1
                        if len(witnesses) < 4:
                            witnesses.append(dict(dimensions=dimensions, symmetry=symmetry,
                                                  anchor=anchor, active=active,
                                                  second_forced_point=top_support,
                                                  partial_only=True))
    assert counts['outer_corner_stencils'] > 0
    assert counts['second_forced_point_geometry'] > 0
    frames = exact_frame_controls()
    result = dict(status='PASS', counts=dict(counts), exact_frame_controls=frames,
                  partial_stencil_witnesses=witnesses,
                  complete_feasible_phase11_exit_coverage=0,
                  complete_closed01_contact_coverage=0, complete_AA_coverage=0,
                  scope='Original-source endpoint/support reconstruction and exact eight-frame tag controls. '
                  'General role exclusion, width and second-force conclusions use the written '
                  'arbitrary-dimension proofs and Lean statements. Endpoint-disjoint stencils '
                  'are not complete feasible instances, compensation payments or counterexamples.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', counts=dict(counts), exact_frame_controls=frames,
                          complete_feasible_phase11_exit_coverage=0)))


if __name__ == '__main__':
    main()
