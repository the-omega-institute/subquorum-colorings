"""Complete corner role catalogues and controls for the general barrier proof."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cap_continuation_budget import phase_of
from check_critical_owner_profiles import anchored_images
from check_minus_one_tip_obstructions import source
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


CORNER = (1, -1)
BACK = {(0, -2), (0, -1), (1, -2), (1, -1)}
MINIMUM = {(0, column) for column in range(-4, 0)} | {
    (row, 0) for row in range(4)}


def barriers(companion_width, companion_height, root_width, root_height):
    companion = {(0, column) for column in range(-companion_height-1, 0)}
    companion.update(itertools.product(range(companion_width),
                                       (-companion_height-1, -companion_height)))
    root = {(row, 0) for row in range(root_height+1)}
    root.update(itertools.product((root_height-1, root_height),
                                  range(1-root_width, 1)))
    return companion, root


def images(dimensions):
    base = source(*dimensions)
    for symmetry in itertools.product((False, True), repeat=3):
        for anchor in base['endpoints']:
            moved_anchor = affine(anchor, symmetry)
            offset = tuple(value-other for value, other in zip(CORNER, moved_anchor))
            module = transform_module(base, symmetry, offset)
            if module['endpoints'] & {(0, -1), (1, 0)}:
                continue
            width, left, right = dimensions
            transpose, flip_row, flip_column = symmetry
            if anchor[0] == 0:
                role = 'B_positive_vertical_bar' if transpose else 'A_phase11_horizontal_bar'
                incident = left if anchor[1] == 1 else right
                if transpose:
                    assert flip_row and flip_column == (anchor[1] == width)
                else:
                    assert not flip_row and flip_column == (anchor[1] == 1)
            else:
                role = 'D_phase10_west_terminal' if transpose else 'C_phase01_south_terminal'
                incident = left if anchor[1] == 1 else right
                assert anchor == (incident, anchor[1]) and anchor[1] in (1, width)
                assert not flip_row if transpose else flip_row
            yield dimensions, symmetry, anchor, module, role, incident


def rotor_catalogue(corner=CORNER, blockers=MINIMUM):
    endpoints = {frozenset(transform_module(module, (False, False, False), corner)['endpoints'])
                 for _, module in anchored_images(rotor())}
    assert len(endpoints) == 16
    assert all(points & blockers for points in endpoints)
    return dict(exact_anchored_roles=len(endpoints), survivors=0)


def source_controls():
    catalogue = []
    for dimensions in itertools.product((6, 8, 14, 40), (4, 6, 12), (4, 8, 20)):
        catalogue.extend(images(dimensions))
    counts = Counter(two_blocker_U_images=len(catalogue))
    roles = Counter()
    examples = {}
    small = 0
    narrow = 0
    for companion_width, companion_height, root_width, root_height, root_far in itertools.product(
            (6, 10), (4, 6, 8, 10, 12), (6, 10), (4, 6, 8, 10, 12, 14), (4, 8)):
        companion, root = barriers(companion_width, companion_height, root_width, root_height)
        root.update((row, 1-root_width) for row in range(root_height-root_far, root_height+1))
        if companion & root:
            counts['incompatible_original_barrier_pairs'] += 1
            continue
        counts['disjoint_barrier_pairs'] += 1
        survivors = 0
        for dimensions, symmetry, anchor, module, role, incident in catalogue:
            if module['endpoints'] & (companion | root):
                continue
            width = dimensions[0]
            phase = phase_of(module)
            own, supports = module['endpoints'] & BACK, module['selected'] & BACK
            if role.startswith('A_'):
                assert phase == '11' and own == {(1, -2), (1, -1)} and not supports
                assert incident <= root_height-4
                assert width <= companion_height-2
            elif role.startswith('B_'):
                assert phase == '00' and own == {(1, -2), (1, -1)}
                assert supports == {(0, -1)} and width <= root_height-2
            elif role.startswith('C_'):
                assert phase == '01' and own == {CORNER} and supports == {(0, -1)}
                assert incident <= root_height-4
                assert (2, -1) in module['endpoints']
                assert width <= companion_height-2 or companion_width <= incident
            else:
                assert phase == '10' and own == {(1, -2), (1, -1)}
                assert supports == {(0, -1)} and incident <= companion_height-2
                assert width <= root_height-2 or root_width <= incident
                assert (1, -3) in module['endpoints']
            if root_height <= 6:
                assert role.startswith('D_')
                assert root_width+2 <= companion_height
            if root_width == companion_height == 6:
                assert root_height >= 12
            roles[role] += 1
            survivors += 1
            examples.setdefault(role, dict(barrier_parameters=[companion_width, companion_height,
                                                               root_width, root_height, root_far],
                                           owner_dimensions=dimensions, symmetry=symmetry,
                                           anchor=anchor, incident=incident))
        if root_height <= 6 and companion_height <= root_width:
            assert survivors == 0
            small += 1
        if root_width == companion_height == 6 and root_height <= 10:
            assert survivors == 0
            narrow += 1
    assert len(roles) == 4
    return dict(counts=counts, surviving_role_counts=roles,
                shallow_excluded_barrier_parameter_sets=small,
                equal_width_six_excluded_barrier_parameter_sets=narrow, partial_examples=examples)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    second_blockers = {(0, column) for column in range(-4, 0)} | {
        (row, -1) for row in range(1, 4)}
    result = dict(status='PASS', rotor_catalogue=rotor_catalogue(),
                  second_corner_rotor_catalogue=rotor_catalogue((1, -2), second_blockers),
                  source_controls=source_controls(),
                  complete_critical_U10_witnesses=0,
                  scope='The 16-root rotor catalogue is exhaustive. U dimension and barrier samples '
                        'are partial geometric controls only; arbitrary-dimension classification and '
                        'barrier inequalities have written proofs with scoped Lean primitives. '
                        'No complete U10 realization, fresh reserve, full allocation or grid equality.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
