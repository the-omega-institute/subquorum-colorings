"""Exact fixed-seed controls for a positive U cap that cannot be completed."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_rotor_only_reserve import source_at
from check_two_leg_corner_obstruction import two_leg_case
from rotor_networks import combine, labeled_module, transform_module, two_leg_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def seed_modules():
    return [source_at((False, 0, 0)), source_at((False, -3, 0)),
            source_at((False, -1, -3)),
            transform_module(two_leg_module(6, 4), (False, False, False), (-4, -6))]


def has_u_certificate(point, endpoints):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    adjacent = set(neighbors(point)) & endpoints
    return (len(adjacent) >= 3 or
            any((point[0]+direction[0], point[1]+direction[1]) in endpoints and
                (point[0]-direction[0], point[1]-direction[1]) in endpoints
                for direction in directions) or
            any(all((point[0]+distance*direction[0], point[1]+distance*direction[1]) in endpoints
                    for distance in range(1, 5)) for direction in directions))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    modules = seed_modules()
    network = combine(modules)
    assert len(network['endpoints']) == sum(len(module['endpoints']) for module in modules) == 42
    first = (-1, -1)
    blocking = {(-1, 0), (0, -1), (-3, -1), (-1, -5)}
    assert blocking <= network['endpoints']
    assert first in network['selected'] and len(set(neighbors(first)) & network['endpoints']) >= 2
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    assert all(any((first[0]+distance*direction[0], first[1]+distance*direction[1]) in blocking
                   for distance in range(1, 5)) for direction in directions)
    candidates = []
    for mirror in (False, True):
        for point in source_at((mirror, 0, 0))['endpoints']:
            owner = mirror, first[0]-point[0], first[1]-point[1]
            if not source_at(owner)['endpoints'] & network['endpoints']:
                candidates.append(owner)
    assert candidates == [(False, -3, -5)]
    forced = source_at(candidates[0])
    completed = combine(modules+[forced])
    second = (-2, -4)
    cavity = {second, (-1, -4)}
    boundary = set.union(set(), *(set(neighbors(point)) for point in cavity))-cavity
    assert len(completed['endpoints']) == 50 and not cavity & completed['endpoints']
    assert boundary <= completed['endpoints'] and len(boundary) == 6
    assert second in completed['selected']
    assert len(set(neighbors(second)) & completed['endpoints']) >= 2
    controls = []
    for width, left, right in itertools.product((6, 8, 14), (4, 6, 10), (4, 8, 12)):
        current, _ = two_leg_case(width, left, right)
        base = labeled_module(current[2], current[3], ())
        for symmetry in itertools.product((False, True), repeat=3):
            source = transform_module(base, symmetry)
            assert all(has_u_certificate(point, source['endpoints']) for point in source['endpoints'])
        controls.append(dict(width=width, left=left, right=right))
    arguments.output.write_text(json.dumps(dict(status='PASS', seed_endpoints=sorted(network['endpoints']),
        first_forced=first, blocking_stencil=sorted(blocking), exact_rotor_owner=candidates[0],
        second_forced=second, cavity=sorted(cavity), cavity_boundary=sorted(boundary),
        u_parameter_controls=controls, summary=dict(exact_rotor_roles=16, seed_endpoints=42,
        forced_endpoint_union=50, closed_cavity_size=2, parameter_controls=27, isometry_controls=216),
        scope='Exact fixed geometry and complete16-role rotor classification. General U certificate follows from the written all-parameter endpoint role split, not these27 parameter controls. Connected original endpoint sets cannot leave the closed cavity without overlapping existing endpoints; each permitted source has at least8 endpoints. This excludes completion of the specified partial seed by arbitrary further U/rotor sources, not the joint inequality.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', exact_rotor_roles=16, closed_cavity_size=2,
                          parameter_controls=27, isometry_controls=216)))


if __name__ == '__main__':
    main()
