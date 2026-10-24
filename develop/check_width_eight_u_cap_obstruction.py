"""Exact owner tables and source controls for a width-eight cap obstruction."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_rotor_only_reserve import source_at
from check_two_leg_corner_obstruction import two_leg_case
from rotor_networks import affine, combine, transform_module, two_leg_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def shifted(root, offsets):
    return {(root[0]+point[0], root[1]+point[1]) for point in offsets}


def rotor_owners(target, blocked):
    result = []
    for mirror in (False, True):
        for endpoint in source_at((mirror, 0, 0))['endpoints']:
            owner = mirror, target[0]-endpoint[0], target[1]-endpoint[1]
            if not source_at(owner)['endpoints'] & blocked:
                result.append(owner)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    modules = [source_at((False, 0, 0)), source_at((False, -3, 0)),
               source_at((False, -1, -3)),
               transform_module(two_leg_module(8, 4), (False, False, False), (-4, -8))]
    network = combine(modules)
    seed = network['endpoints']
    assert len(seed) == sum(len(module['endpoints']) for module in modules) == 46
    first, second = (-1, -1), (-2, -1)
    assert first in network['selected'] and len(set(neighbors(first)) & seed) >= 2
    three = {(0, 1), (1, 0), (-2, 0)}
    five = three | {(0, -6), (-2, -4)}
    corridor = {(0, 1), (-1, 0), (1, 0), (0, -6), (-1, -4), (1, -4)}
    assert shifted(first, five) <= seed
    assert rotor_owners(first, seed) == [(False, -3, -5)]
    forced = source_at((False, -3, -5))
    assert not seed & forced['endpoints']
    rotor_branch = seed | forced['endpoints']
    assert second in forced['selected'] and second not in rotor_branch
    assert len(set(neighbors(second)) & rotor_branch) >= 2
    assert rotor_owners(second, rotor_branch) == []
    rotor_barrier = {(-3, -1), (-2, 0), (-2, -3), (2, -1)}
    assert rotor_barrier <= rotor_branch
    original_stencil = {(0, 1), (1, 0), (-2, 0), (0, -4)}
    assert {affine(point, (True, False, True), second) for point in original_stencil} == rotor_barrier
    guaranteed = shifted(first, {(0, -distance) for distance in range(5)})
    u_branch = seed | guaranteed
    assert second not in u_branch and len(set(neighbors(second)) & u_branch) >= 2
    assert rotor_owners(second, u_branch) == []
    assert shifted(second, corridor) <= u_branch
    parameters = list(itertools.product((6, 8, 12), (4, 6, 10), (4, 8, 12)))
    parameters += [(20, 30, 14), (20, 14, 30), (40, 40, 4)]
    corner_contexts = support_contexts = endpoint_controls = 0
    for width, left_height, right_height in parameters:
        current = two_leg_case(width, left_height, right_height)[0]
        for symmetry in itertools.product((False, True), repeat=3):
            endpoints = {affine(point, symmetry) for edge in current[3] for point in edge}
            selected = {affine(point, symmetry) for point in current[2]}
            for root in endpoints:
                endpoint_controls += 1
                assert shifted(root, corridor) & endpoints
                if not shifted(root, three) & endpoints:
                    corner_contexts += 1
                    assert shifted(root, {(0, -distance) for distance in range(1, 5)}) <= endpoints
                    if not shifted(root, five) & endpoints:
                        support_contexts += 1
                        assert (root[0]-1, root[1]) in selected
    result = dict(status='PASS', seed_endpoints=46,
                  first_rotor_owners=[[False, -3, -5]],
                  second_rotor_owners_in_both_branches=[],
                  first_root=list(first), second_root=list(second),
                  rotor_branch_barrier=sorted(rotor_barrier),
                  u_branch_corridor_barrier=sorted(shifted(second, corridor)),
                  parameter_controls=len(parameters), isometry_controls=8*len(parameters),
                  endpoint_controls=endpoint_controls,
                  three_blocker_contexts=corner_contexts, five_blocker_support_contexts=support_contexts,
                  scope='Exact16-role owner exhaustion in three fixed contexts; branch barriers and mandatory neighbors. Representative complete U endpoint/support controls only; arbitrary dimensions and both ownership branches have written proofs and separately scoped Lean lemmas. The finite controls do not prove general noncompletion or the mixed inequality.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
