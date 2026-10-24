"""Independent controls for a general short-return noncompletion theorem."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_opposed_stem_support_gap import source_candidates
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def explicit_rotor(leg):
    matching = {tuple(sorted(edge)) for edge in (
        ((leg-3, 7), (leg-2, 7)), ((leg-2, 8), (leg-2, 9)),
        ((leg-1, 6), (leg-1, 7)), ((leg-1, 8), (leg, 8)))}
    endpoints = {point for edge in matching for point in edge}
    supports = {(leg-4, 7), (leg-3, 6), (leg-3, 9), (leg-2, 10),
                (leg-1, 5), (leg, 6), (leg, 9), (leg+1, 8)}
    return endpoints, supports, matching


def rotor_roles(leg):
    point = leg, 8
    footprints = {}
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        for tip in module['endpoints']:
            own = set(neighbors(tip)) & module['endpoints']
            if len(own) != 1:
                continue
            moved = transform_module(module, (False, False, False),
                                     (point[0]-tip[0], point[1]-tip[1]))
            if not set(neighbors(point)) & moved['endpoints'] <= {(leg-1, 8), (leg, 9)}:
                continue
            footprints[frozenset(moved['endpoints'])] = moved
    assert len(footprints) == 4
    expected = explicit_rotor(leg)
    survivors = []
    for module in footprints.values():
        if (leg-1, 10) not in module['endpoints']:
            actual = module['endpoints'], module['selected'], {
                tuple(sorted(edge)) for edge in module['matching']}
            assert actual == expected
            survivors.append(actual)
    assert survivors == [expected]
    return len(footprints)


def cavity_control(leg):
    returning = independent_source((6, 8, 4), (True, True, True), (leg+2, 11))
    forced = explicit_rotor(leg)
    assert not returning[0] & forced[0]
    endpoints = returning[0] | forced[0]
    boundary = {(row, column) for row in range(leg-4, leg-1)
                for column in range(7, 11)
                if row in (leg-4, leg-2) or column in (7, 10)}
    inside = {(leg-3, 8), (leg-3, 9)}
    assert boundary <= endpoints and not inside & endpoints
    occupied = endpoints | returning[1] | forced[1]
    for point, source in [((leg-3, 8), returning), ((leg-3, 9), forced)]:
        assert point in source[1]
        assert len(set(neighbors(point)) & source[0]) == 1
        assert len(set(neighbors(point)) & occupied) >= 2
    return returning, forced


def controls():
    patterns = 0
    for leg, near in itertools.product((8, 10, 12, 16, 24, 40), (4, 6, 20, 52)):
        returning, forced = cavity_control(leg)
        corner = independent_source((leg-2, near, 4), (True, False, False), (2, 3))
        assert not corner[0] & returning[0]
        point = leg, 8
        assert point in returning[1] and point not in corner[0] | returning[0]
        assert (leg, 7) in corner[0] and (leg+1, 8) in returning[0]
        candidates, rotors = source_candidates(point, corner[0] | returning[0])
        assert not candidates and len(rotors) == 1
        assert rotors[0]['endpoints'] == forced[0] and rotors[0]['selected'] == forced[1]
        assert {tuple(sorted(edge)) for edge in rotors[0]['matching']} == forced[2]
        longer = independent_source((leg-2, near, 6), (True, False, False), (2, 3))
        assert point in longer[0] and (leg, 10) in returning[0]
        patterns += 1
    cavity_patterns = 0
    for leg in (-60, -3, 0, 8, 17, 100):
        cavity_control(leg)
        assert rotor_roles(leg) == 4
        cavity_patterns += 1
    return dict(status='PASS', forced_consumer_patterns=patterns,
                cavity_and_four_rotor_role_patterns=cavity_patterns,
                each_forced_consumer=dict(U=0, rotor=1),
                all_sources_reconstructed_with_original_matching_and_supports=True,
                far_leg_six_is_outside_forcing_argument=True,
                scope='Finite controls of a separate arbitrary-dimension X_far4/Q6_8_4 '
                      'noncompletion proof. U anchored roles bounded by18 only; not '
                      'unbounded enumeration. No reserve, activation or global target '
                      'conclusion follows from excluding an impossible stencil.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
