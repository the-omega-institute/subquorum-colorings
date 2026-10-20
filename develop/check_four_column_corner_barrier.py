"""Check the two-rotor four-column barrier and forced long-H far-leg stencils."""

import itertools
import json

from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import original, rectangle_points
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def rotor_controls():
    variants = {}
    for symmetry in SYMMETRIES:
        module = transform_module(rotor(), symmetry, (0, 0))
        column = min(point[1] for point in module['endpoints'])
        tips = [point for point in module['endpoints'] if point[1] == column]
        assert len(tips) == 1
        tip = tips[0]
        moved = transform_module(module, (False, False, False), (-tip[0], -tip[1]))
        variants[frozenset(moved['endpoints'])] = moved
    assert len(variants) == 2
    collisions = 0
    for module in variants.values():
        assert {(-1, 2), (0, 2), (1, 2)} <= module['endpoints']
        assert {point for point in module['endpoints'] if point[1] == 0} == {(0, 0)}
        adjacent_supports = {(step, 0) for step in (-1, 1)} & module['selected']
        assert len(adjacent_supports) == 1
        for other, step in itertools.product(variants.values(), (-1, 1)):
            shifted = {(row+step, column) for row, column in other['endpoints']}
            assert (0, 2) in shifted & module['endpoints']
            collisions += 1
    placements = 0
    for height, module in itertools.product((6, 8, 12, 20, 38), variants.values()):
        inside, boundary = rectangle_points((4, height+2, 3, 8))
        for row in range(5, height+2):
            moved = transform_module(module, (False, False, False), (row, 4))
            if not moved['endpoints'] <= inside:
                continue
            adjacent_support = next(point for point in moved['selected']
                                    if point in {(row-1, 4), (row+1, 4)})
            assert adjacent_support in inside
            assert (adjacent_support[0], 3) in boundary
            placements += 1
    assert placements > 0
    return dict(forms=len(variants), adjacent_tip_collisions=collisions,
                four_column_placements=placements)


def wrong_return_controls():
    patterns = wrong = 0
    for incident in (6, 8, 10, 14, 22, 40):
        for returning_far, corner_far in itertools.product(
                range(4, incident+3, 2), (incident-2, incident, incident+8)):
            returning = original((6, incident, returning_far),
                                 (False, True, False), (incident+3, 1))
            corner = original((6, incident-2, corner_far), offset=(3, 2))
            endpoints = returning['endpoints'] | corner['endpoints']
            if len(endpoints) != len(returning['endpoints'])+len(corner['endpoints']):
                assert returning_far >= incident
                continue
            assert returning_far <= incident-2
            inside, boundary = rectangle_points((4, incident+2, 3, 8))
            assert boundary-{(incident+2, 8)} <= endpoints
            assert not {point for point in inside if point[1] == 4} & endpoints
            if returning_far < incident-2:
                forced = (incident+2-returning_far, 7)
                assert forced in inside & returning['selected']
                assert forced not in endpoints
                assert {(forced[0]+1, 7), (forced[0], 8)} <= endpoints
                wrong += 1
            patterns += 1
    assert wrong > 0
    return dict(disjoint_two_owner_patterns=patterns, impossible_wrong_return_stencils=wrong)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', rotor=rotor_controls(),
                         returning=wrong_return_controls(),
                         scope='Exact rotor endpoint/support forms and pair collisions, '
                               'fixed-boundary and original mandatory-support coordinates. '
                               'Wrong-return stencils are partial, with nonextension proved '
                               'generally in the written argument, not by finite search.'), indent=2))
