"""All-role boundary-stop and orientation controls for the joint core obstruction."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_minus_one_tip_obstructions import source
from check_regular_tile_compensation import profile_counts
from check_rotor_only_reserve import source_at
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def plus(first, second):
    return first[0]+second[0], first[1]+second[1]


def scale(amount, point):
    return amount*point[0], amount*point[1]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    parameters = list(itertools.product((6, 8, 12), (4, 6, 10), (4, 8, 12)))
    parameters += [(40, 30, 4), (20, 4, 30)]
    counts = Counter()
    for dimensions in parameters:
        width, left, right = dimensions
        module = source(*dimensions)
        for symmetry in itertools.product((False, True), repeat=3):
            body = {affine(point, symmetry) for point in module['endpoints']}
            supports = {affine(point, symmetry) for point in module['selected']}
            for endpoint in module['endpoints']:
                origin = affine(endpoint, symmetry)
                for row in (13, 14):
                    counts['U_role_tests'] += 1
                    target = row, 2
                    offset = target[0]-origin[0], target[1]-origin[1]
                    endpoints = {(point[0]+offset[0], point[1]+offset[1]) for point in body}
                    selected = {(point[0]+offset[0], point[1]+offset[1]) for point in supports}
                    if (row, 1) in endpoints or (row+1, 2) in endpoints | selected:
                        continue
                    moved = transform_module(module, symmetry, offset)
                    if endpoint in ((0, 1), (0, width)):
                        counts['corner_stops_'+str(row%2)] += 1
                        toward_bar = affine((0, endpoint[1]+(1 if endpoint[1] == 1 else -1)),
                                            symmetry, offset)
                        toward_leg = affine((1, endpoint[1]), symmetry, offset)
                        assert toward_bar == (row, 3) and toward_leg == (row-1, 2)
                        assert moved['charge'] == (-1 if row%2 else 1-width)
                    else:
                        assert endpoint in ((left, 1), (right, width))
                        counts['terminal_stops_'+str(row%2)] += 1
                        predecessor = affine((endpoint[0]-1, endpoint[1]), symmetry, offset)
                        across = affine((endpoint[0], endpoint[1]+(1 if endpoint[1] == 1 else -1)),
                                        symmetry, offset)
                        assert predecessor == (row, 3) and across == (row+1, 2)
                        assert profile_counts(moved)[3, 0] == (0 if row%2 else 2)
                    if row%2 == 0:
                        cells = vertices_of({(row//2, 1)})
                        assert cells & endpoints == {(row, 2), (row, 3)}
                        expected = set() if endpoint in ((0, 1), (0, width)) else {(row+1, 3)}
                        assert cells & selected == expected
                        counts['even_stop_exact_profiles'] += 1
    rotor_survivors = []
    for mirror in (False, True):
        original = source_at((mirror, 0, 0))
        for endpoint in original['endpoints']:
            owner = mirror, -endpoint[0], -endpoint[1]
            moved = source_at(owner)
            if (0, -1) in moved['endpoints'] or (1, 0) in moved['endpoints'] | moved['selected']:
                continue
            rotor_survivors.append(owner)
            assert (2, 0) in moved['selected'] and (2, 1) in moved['endpoints']
            assert moved['endpoints'] & {(0, 0), (0, 1), (1, 0), (1, 1)} == {(0, 0), (0, 1), (1, 1)}
    assert rotor_survivors == [(True, -2, 4)]
    frames = [(affine((1, 0), symmetry), affine((0, 1), symmetry))
              for symmetry in itertools.product((False, True), repeat=3)]
    mutual_orientations = coordinate_cases = 0
    for first_frame, second_frame in itertools.product(frames, repeat=2):
        first_down, first_inside = first_frame
        second_down, second_inside = second_frame
        if second_down != first_inside or first_down != second_inside:
            continue
        mutual_orientations += 1
        assert first_down != scale(-1, second_inside)
        assert second_down != scale(-1, first_inside)
        for first_port, second_port, first_row, second_row in itertools.product(
                (2, 4), (2, 4), range(1, 30), range(1, 30)):
            first_stop = plus(scale(first_row, first_down), first_inside)
            second_anchor = plus(first_stop,
                                 scale(-1, plus(scale(2, second_down), scale(second_port, second_inside))))
            second_stop = plus(second_anchor, plus(scale(second_row, second_down), second_inside))
            first_core_tip = plus(scale(2, first_down), scale(first_port, first_inside))
            if second_stop != first_core_tip:
                continue
            assert first_row == second_port+1 and second_row == first_port+1
            assert first_row <= 5 and second_row <= 5
            coordinate_cases += 1
    assert mutual_orientations == 8 and coordinate_cases == 32
    result = dict(status='PASS', parameter_controls=len(parameters), U_controls=dict(counts),
                  exact_rotor_roles=16, surviving_rotor_owners=rotor_survivors,
                  orthogonal_frames=len(frames), mutual_predecessor_frames=mutual_orientations,
                  mutual_core_coordinate_cases=coordinate_cases,
                  new_complete_physical_fixture_coverage=0,
                  scope='Representative arbitrary-dimension/isometry U stop roles and exact even-tile profiles; exact16-role rotor catalogue; all8 physical frame choices and finite mutual-core coordinate controls. Universal role and normalized-coordinate proofs are separate Lean statements. Physical last-point existence, saturation and cross-core near/far ownership adapters remain written; no finite AA closure or fresh defect payment claimed.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
