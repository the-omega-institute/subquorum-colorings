"""Fixed-mask and complete-source controls for the arbitrary-width cap barrier."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_rotor_only_reserve import source_at
from check_two_leg_corner_obstruction import two_leg_case
from check_width_eight_u_cap_obstruction import rotor_owners, shifted
from rotor_networks import affine


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    rotors = [source_at((False, 0, 0)), source_at((False, -3, 0)),
              source_at((False, -1, -3))]
    rotor_endpoints = set.union(*(module['endpoints'] for module in rotors))
    cap_mask = {(row, column) for row in (-4, -3) for column in range(-7, 1)}
    cap_mask |= {(-2, 0), (-1, 0), (0, 0)}
    core = rotor_endpoints | cap_mask
    assert len(core) == 43
    first, inner = (-1, -1), (0, -2)
    assert first in set.union(*(module['selected'] for module in rotors))-core
    assert len(set(neighbors(first)) & core) >= 2
    assert rotor_owners(first, core) == [(False, -3, -5)]
    forced = source_at((False, -3, -5))
    assert not core & forced['endpoints']
    rotor_branch = core | forced['endpoints']
    assert rotor_owners((-2, -1), rotor_branch) == []
    ray_mask = core | {(-1, column) for column in range(-5, 0)}
    assert rotor_owners(inner, ray_mask) == []
    assert {(0, -1), (-1, -2), (2, -2)} <= ray_mask
    assert len(set(neighbors(inner)) & ray_mask) >= 2
    parameters = list(itertools.product((6, 8, 12), (4, 6, 10), (4, 8, 12)))
    parameters += [(20, 30, 14), (20, 14, 30), (40, 40, 4)]
    short_contexts = endpoint_controls = 0
    blockers = {(0, 1), (1, 0), (-2, 0), (-2, -4), (-2, -6)}
    for width, left_height, right_height in parameters:
        current = two_leg_case(width, left_height, right_height)[0]
        reference = {point for edge in current[3] for point in edge}
        for symmetry in itertools.product((False, True), repeat=3):
            endpoints = {affine(point, symmetry) for point in reference}
            selected = {affine(point, symmetry) for point in current[2]}
            for original in reference:
                endpoint_controls += 1
                root = affine(original, symmetry)
                if original[0] <= 6 and not shifted(root, blockers) & endpoints:
                    short_contexts += 1
                    assert (root[0]+1, root[1]-1) in selected
                    assert shifted(root, {(1, -3), (1, -5)}) & endpoints
    family_controls = []
    width_six_controls = []
    for cap_left_height in (4, 6, 14, 40):
        current = two_leg_case(6, cap_left_height, 4)[0]
        endpoints = {(point[0]-4, point[1]-6) for edge in current[3] for point in edge}
        known = endpoints | rotor_endpoints
        assert not endpoints & rotor_endpoints
        assert rotor_owners(first, known) == [(False, -3, -5)]
        assert not known & forced['endpoints']
        extended = known | forced['endpoints']
        cavity = {(-2, -4), (-1, -4)}
        boundary = set.union(*(set(neighbors(point)) for point in cavity))-cavity
        assert not cavity & extended and boundary <= extended
        assert (-2, -4) in forced['selected']
        assert len(set(neighbors((-2, -4))) & extended) >= 2
        width_six_controls.append(cap_left_height)
    for cap_width, cap_left_height in itertools.product((8, 10, 12, 16, 24, 64), (4, 6, 14, 40)):
        current = two_leg_case(cap_width, cap_left_height, 4)[0]
        endpoints = {(point[0]-4, point[1]-cap_width) for edge in current[3] for point in edge}
        assert not endpoints & rotor_endpoints
        assert cap_mask <= endpoints
        assert (-1, 1-cap_width) in endpoints
        admissible = list(range(8, cap_width-3, 2))
        assert not admissible if cap_width < 12 else admissible[0] == 8
        family_controls.append(dict(width=cap_width, left_height=cap_left_height,
                                    necessary_entry_heights=admissible))
    result = dict(status='PASS', fixed_core_endpoints=43, exact_rotor_tables=3,
                  parameter_controls=len(parameters), isometry_controls=8*len(parameters),
                  endpoint_controls=endpoint_controls, short_tip_contexts=short_contexts,
                  width_six_left_height_controls=width_six_controls,
                  cap_family_controls=family_controls,
                  scope='Exact local owner/barrier masks and representative U support controls. All-parameter short-tip exclusion, arbitrary-width cap inclusion and necessary8<=h<=W-4,W>=12 are written proofs with separately scoped Lean coordinate/mask/arithmetic declarations. Lists of necessary heights do not assert a feasible extension. Finite controls and cap10 UNSAT do not prove general noncompletion.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'cap_family_controls'}))


if __name__ == '__main__':
    main()
