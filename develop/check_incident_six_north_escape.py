"""Independent finite controls of the north-escape obstruction and complete pair."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def prescribed(bottom, near, far, width, other):
    return [
        independent_source((bottom-2, near, far), (True, False, False), (2, 3)),
        independent_source((6, 8, 4), (True, True, True), (bottom+2, 11)),
        independent_source((width, 6, other), (False, False, False), (bottom-7, 4)),
    ]


def obstruction_controls():
    cases = []
    for bottom, near, far, width, other in itertools.product(
            (12, 24, 40), (4, 20), (4, 6), (8, 10, 20), (4, 12)):
        sources = prescribed(bottom, near, far, width, other)
        assert all(not first[0] & second[0]
                   for first, second in itertools.combinations(sources, 2))
        point = bottom-4, 6
        assert point in sources[1][1] & sources[2][1]
        assert not any(point in source[0] for source in sources)
        assert (bottom-4, 5) in sources[2][0]
        assert (bottom-4, 7) in sources[1][0]
        blocked = set.union(*(source[0] for source in sources))
        relative = {(row-point[0], column-point[1]) for row, column in blocked}
        cases.append(relative)
    axial_roles = interior_roles = rejected_roles = 0
    for parameters in itertools.product(range(6, 20, 2), range(4, 20, 2), range(4, 20, 2)):
        original = independent_source(parameters, (False, False, False), (0, 0))[0]
        for symmetry in itertools.product((False, True), repeat=3):
            endpoints = {affine(point, symmetry) for point in original}
            for anchor in endpoints:
                relative = {(row-anchor[0], column-anchor[1]) for row, column in endpoints}
                own = relative & {(-1, 0), (1, 0), (0, -1), (0, 1)}
                if not own <= {(-1, 0), (1, 0)}:
                    continue
                assert own
                axial_roles += 1
                interior_roles += len(own) == 2
                for blocked in cases:
                    assert relative & blocked
                    rejected_roles += 1
    rotor_footprints = {}
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        for anchor in module['endpoints']:
            relative = frozenset((row-anchor[0], column-anchor[1])
                                 for row, column in module['endpoints'])
            own = relative & {(-1, 0), (1, 0), (0, -1), (0, 1)}
            if not own <= {(-1, 0), (1, 0)}:
                continue
            assert len(own) == 1
            blocker = (-2, -1) if (-1, 0) in own else (2, -1)
            assert blocker in relative
            assert all(blocker in blocked for blocked in cases)
            rotor_footprints[relative] = blocker
    assert len(rotor_footprints) == 4
    return dict(disjoint_prescribed_patterns=len(cases), U_axial_roles=axial_roles,
                U_straight_interior_roles=interior_roles,
                U_role_pattern_collisions=rejected_roles, rotor_tip_footprints=4,
                surviving_consumers=0, U_dimensions_bounded_by=18,
                includes_every_endpoint_anchor_in_each_bounded_U=True)


def pair_control(bottom, near, expect_complete=True):
    corner, returning = prescribed(bottom, near, 6, 8, 4)[:2]
    assert not corner[0] & returning[0]
    endpoints = corner[0] | returning[0]
    selected = (corner[1] | returning[1])-endpoints
    occupied = endpoints | selected
    bad_selected = {point for point in selected if len(set(neighbors(point)) & occupied) != 1}
    bad_endpoints = {point for point in endpoints if len(set(neighbors(point)) & occupied) < 3}
    if not expect_complete:
        assert bad_selected
        return dict(bottom=bottom, near=near, bad_selected=sorted(bad_selected),
                    bad_endpoints=sorted(bad_endpoints))
    assert not bad_selected and not bad_endpoints
    expected_corner = {(2, column) for column in range(3, near+4, 2)}
    expected_corner |= {(3, near+4)} | {(4, column) for column in range(6, near+3, 2)}
    expected_corner |= {(bottom-1, 6), (bottom-1, 8)}
    expected_return = {(bottom+2, column) for column in (3, 5, 7, 9, 11)}
    expected_return |= {(bottom-5, column) for column in (7, 9, 11)}
    expected_return |= {(bottom+1, 2), (bottom-4, 6), (bottom-3, 8)}
    assert corner[1]-endpoints == expected_corner
    assert returning[1]-endpoints == expected_return
    assert not expected_corner & expected_return
    assert corner[1] & returning[0] == {
        (bottom+1, 3), (bottom+1, 5), (bottom+1, 7), (bottom+1, 9), (bottom, 10)}
    assert returning[1] & corner[0] == {(bottom, 4), (bottom, 6), (bottom, 8)}
    matching = corner[2] | returning[2]
    flat = [point for edge in matching for point in edge]
    assert len(flat) == len(set(flat)) and set(flat) == endpoints
    assert all(second in neighbors(first) for first, second in matching)
    for source in (corner, returning):
        for support in source[1]-endpoints:
            assert set(neighbors(support)) & occupied == set(neighbors(support)) & source[0]
    reached = {min(endpoints)}
    pending = list(reached)
    while pending:
        added = set(neighbors(pending.pop())) & endpoints-reached
        reached.update(added)
        pending.extend(added)
    assert reached == endpoints
    assert len(endpoints) == 2*bottom+near+22
    assert len(matching) == bottom+near//2+11
    assert len(selected) == near+14
    assert all(0 <= row < bottom+4 and 0 <= column < max(near+6, 12)
               for row, column in occupied)
    return dict(bottom=bottom, near=near, endpoints=len(endpoints),
                matching=len(matching), selected=len(selected))


def controls():
    pairs = [pair_control(bottom, near) for bottom, near in
             itertools.product(range(10, 42, 2), range(4, 42, 2))]
    pairs.extend(pair_control(*parameters) for parameters in ((100, 200), (200, 4), (10, 200)))
    negatives = [pair_control(8, near, False) for near in (4, 6, 20)]
    return dict(status='PASS', obstruction=obstruction_controls(),
                complete_pair_patterns=len(pairs), extreme_pair_patterns=pairs[-3:],
                bottom_eight_negative_controls=negatives,
                scope='Finite controls only. Arbitrary-dimension statements use the written '
                      'proof and scoped Lean lemmas. The complete two-source pair has no '
                      'actual A/B/C gate or positive marked producer. No complete Vcorner '
                      'witness, unrestricted allocation or grid equality is established.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
