"""Source-role controls for the forced bottom owner and clearance-four branch."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from check_minus_one_tip_obstructions import source
from check_regular_tile_compensation import profile_counts
from check_width_eight_u_cap_obstruction import rotor_owners
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def candidates(parameters, target, blocked, blank, counts):
    for width, left, right in parameters:
        module = source(width, left, right)
        for symmetry in itertools.product((False, True), repeat=3):
            body = {affine(point, symmetry) for point in module['endpoints']}
            supports = {affine(point, symmetry) for point in module['selected']}
            for endpoint in module['endpoints']:
                counts['tested_roles'] += 1
                origin = affine(endpoint, symmetry)
                offset = target[0]-origin[0], target[1]-origin[1]
                endpoints = {(point[0]+offset[0], point[1]+offset[1]) for point in body}
                if endpoints & blocked:
                    continue
                selected = {(point[0]+offset[0], point[1]+offset[1]) for point in supports}
                if (endpoints | selected) & blank:
                    continue
                yield (width, left, right), endpoint, symmetry, offset, endpoints, selected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    parameters = list(itertools.product((6, 8, 12, 20), (4, 6, 10, 20), (4, 8, 12)))
    parameters += [(40, 30, 4), (20, 4, 30)]
    height = 10
    incoming = transform_module(source(12, height, 4), (False, True, False), (height+2, 1))
    first_counts = Counter()
    first_classes = Counter()
    for clearance in (4, 6):
        long = height+clearance
        positive = source(6, long, 4)
        target = height+3, 2
        blocked = positive['endpoints'] | incoming['endpoints'] | {(long+1, 1)}
        blank = {(long+1, 2)}
        assert target in positive['selected']
        assert (height+2, 2) in incoming['endpoints']
        assert rotor_owners(target, blocked) == []
        for dimensions, endpoint, symmetry, offset, _, _ in candidates(
                parameters, target, blocked, blank, first_counts):
            width, left, right = dimensions
            assert endpoint in ((left, 1), (right, width))
            assert affine((endpoint[0]-1, endpoint[1]), symmetry, offset) == (target[0], 3)
            across = affine((endpoint[0], endpoint[1]+(1 if endpoint[1] == 1 else -1)),
                            symmetry, offset)
            direction = 'down' if across == (target[0]+1, 2) else 'up'
            assert across == (target[0]+(1 if direction == 'down' else -1), 2)
            moved = transform_module(source(*dimensions), symmetry, offset)
            assert profile_counts(moved)[3, 0] == (0 if direction == 'down' else 2)
            first_classes[str(clearance)+'_'+direction] += 1
    assert all(first_classes[str(clearance)+'_'+direction] > 0
               for clearance in (4, 6) for direction in ('up', 'down'))
    partials = []
    second_counts = Counter()
    positive = source(6, 14, 4)
    for width, incident in ((8, 14), (6, 16)):
        wrapper = transform_module(source(width, incident, 4),
                                   (True, True, True), (14, incident+2))
        modules = [positive, incoming, wrapper]
        network = combine(modules)
        assert len(network['endpoints']) == sum(len(module['endpoints']) for module in modules)
        assert not (15, 2) in wrapper['endpoints'] | wrapper['selected']
        assert profile_counts(wrapper)[3, 0] == 2
        assert (14, 2) in wrapper['selected']
        blocked = network['endpoints'] | {(15, 1)}
        assert rotor_owners((14, 2), blocked | {(15, 2)}) == []
        for dimensions, endpoint, symmetry, offset, endpoints, selected in candidates(
                parameters, (14, 2), blocked, {(15, 2)}, second_counts):
            owner_width, left, right = dimensions
            assert endpoint in ((left, 1), (right, owner_width))
            assert affine((endpoint[0]-1, endpoint[1]), symmetry, offset) == (14, 3)
            across = affine((endpoint[0], endpoint[1]+(1 if endpoint[1] == 1 else -1)),
                            symmetry, offset)
            assert across == (15, 2)
            moved = transform_module(source(*dimensions), symmetry, offset)
            assert profile_counts(moved)[3, 0] == 2
            cells = vertices_of({(7, 1)})
            assert cells & endpoints == {(14, 2), (14, 3)}
            assert cells & selected == {(15, 3)}
            assert (15, 2) not in endpoints | selected
            second_counts['downward_U11_terminal_profiles'] += 1
        bad_supports = sorted(point for point in network['selected']
                              if sum((point[0]+delta[0], point[1]+delta[1]) in
                                     network['endpoints'] | network['selected']
                                     for delta in ((-1, 0), (1, 0), (0, -1), (0, 1))) > 1)
        assert bad_supports
        partials.append(dict(wrapper_dimensions=[width, incident, 4],
                             disjoint_original_endpoints=True, forbidden_point_avoided=True,
                             wrapper_phase='11', complete_feasible=False,
                             infeasible_retained_supports=bad_supports,
                             scope='Local endpoint/forbidden-point compatible upward wrapper; not a complete-source fusion or a counterexample to compensation.'))
    result = dict(status='PASS', parameter_controls=len(parameters),
                  first_role_controls=dict(first_counts), first_surviving_classes=dict(first_classes),
                  second_role_controls=dict(second_counts), local_upward_wrappers=partials,
                  new_complete_physical_fixture_coverage=0,
                  scope='Representative all-role/all-isometry endpoint and support controls, nonvacuous upward wrapping alternatives, and exact forced second-owner profiles. Universal U-role classification is separately proved in Lean; source-normalization and global saturation implications remain written. No finite closure or ambient counterexample is claimed.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', first=dict(first_counts), classes=dict(first_classes),
                          second=dict(second_counts), partial_upward_wrappers=len(partials))))


if __name__ == '__main__':
    main()
