"""Independent controls of the maximal-width Vcorner two-source obstruction."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def rotor_forms():
    forms = set()
    for symmetry in itertools.product((False, True), repeat=3):
        endpoints = transform_module(rotor(), symmetry)['endpoints']
        for point in endpoints:
            if set(neighbors(point)) & endpoints == {(point[0], point[1]+1)}:
                forms.add(frozenset((row-point[0], column-point[1]) for row, column in endpoints))
    assert len(forms) == 2
    assert all({(-1, 1), (1, 1)} & points for points in forms)
    return forms


def controls():
    forms = rotor_forms()
    pairs = 0
    terminals = 0
    rotors = 0
    for width, leg, far, near, other in itertools.product(
            (6, 8, 10, 14, 22), (8, 12, 20), (4, 10), (4, 10),
            (4, 6, 8, 10, 12, 16, 18)):
        if other < width-4:
            continue
        fixed = independent_source((width, leg, far), (False, True, False), (leg+3, 1))
        corner = independent_source((leg-2, near, other), (True, False, False), (2, 3))
        if fixed[0] & corner[0]:
            continue
        point = (leg+1, 3)
        endpoints = fixed[0] | corner[0]
        assert point in corner[1] and point not in endpoints
        assert set(neighbors(point)) & endpoints == {(leg, 3), (leg+1, 2), (leg+2, 3)}
        assert (leg+1, width+1) in fixed[0]
        pairs += 1
        for source_width, incident, other_leg, upward in itertools.product(
                (6, 14), range(4, 26, 2), (4, 12), (False, True)):
            offset = (leg+2, incident+3) if upward else (leg, incident+3)
            symmetry = (True, True, upward)
            current = independent_source((source_width, incident, other_leg), symmetry, offset)
            assert point in current[0]
            assert set(neighbors(point)) & current[0] == {(leg+1, 4)}
            if incident >= width-2:
                witness = (leg+1, width+1)
                assert witness in current[0] & fixed[0]
            elif upward:
                witness = (leg, incident+3)
                assert witness in current[0] & corner[0]
            else:
                witness = (leg+2, incident+3)
                assert witness in current[0] & fixed[0]
            terminals += 1
        for footprint in forms:
            current = {(point[0]+row, point[1]+column) for row, column in footprint}
            assert current & endpoints
            rotors += 1
    boundary_pairs = 0
    for width, leg in itertools.product(range(8, 40, 2), repeat=2):
        boundary_fixed = independent_source((width, leg, 4),
                                            (False, True, False), (leg+3, 1))
        boundary_corner = independent_source((leg-2, 4, width-4),
                                             (True, False, False), (2, 3))
        assert not boundary_fixed[0] & boundary_corner[0]
        boundary_pairs += 1
    fixed = independent_source((8, 8, 4), (False, True, False), (11, 1))
    corner = independent_source((6, 10, 4), (True, False, False), (2, 3))
    assert not fixed[0] & corner[0]
    assert (9, 3) in corner[1]
    return dict(status='PASS', disjoint_fixed_pairs=pairs, terminal_collision_cases=terminals,
                rotor_collision_cases=rotors, distinct_east_rotor_forms=len(forms),
                matched_seed_forced_point=[9, 3], boundary_partial_pairs=boundary_pairs,
                scope='Finite controls of a separate all-dimension written proof; no finite enumeration used as exhaustion.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
