"""Forced sharp-family supports and parity uniqueness for complete original roles."""

import itertools
import json
from collections import Counter

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_secondary_ten_arbitrary_t_consumers import old_chain
from check_secondary_ten_both_far_compensation import originals
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def qualifying(endpoints):
    allowed = {(1, 0), (0, -1)}
    result = set()
    for point in endpoints:
        internal = {(other[0]-point[0], other[1]-point[1])
                    for other in set(neighbors(point)) & endpoints}
        assert internal
        if internal <= allowed:
            result.add(point)
    phases = Counter((row % 2, column % 2) for row, column in result)
    assert all(count == 1 for count in phases.values())
    return len(result)


def main():
    supports = 0
    for pairs, far in ((1, 4), (5, 4), (11, 10), (3, 100), (2, 2000)):
        widths, depths = [12]*(pairs+1), [far+24]*(pairs+1)
        fixed, unused, unused, sites = old_chain(31, -100, widths, depths, 6)
        selected = [originals(sites, widths, (index, 6, 0, far+2, far))
                    for index in range(1, pairs+1)]
        endpoints = set.union(*(record[0] for record in fixed),
                              *(record[0] for pair in selected for record in pair))
        for index, (receiver, consumer) in enumerate(selected, 1):
            anchor, unused, lateral = sites[index]
            point = anchor+far-8, lateral-6
            assert point not in endpoints and point in receiver[1] & consumer[1]
            assert set(neighbors(point)) & endpoints == {
                (point[0]-1, point[1]), (point[0], point[1]+1)}
            assert (point[0] % 2, point[1] % 2) == (1, 0)
            supports += 1
    roles = Counter()
    for breadth, incident, far, symmetry, offset in itertools.product(
            (6, 20, 200), (4, 8, 80), (4, 10, 200),
            itertools.product((False, True), repeat=3),
            ((0, 0), (1, 0), (0, 1), (-33, -100))):
        endpoints = independent_source((breadth, incident, far), symmetry, offset)[0]
        roles[qualifying(endpoints)] += 1
    rotor_roles = Counter()
    for symmetry, offset in itertools.product(itertools.product((False, True), repeat=3),
                                              ((0, 0), (1, 0), (0, 1), (-33, -100))):
        rotor_roles[qualifying(transform_module(rotor(), symmetry, offset)['endpoints'])] += 1
    print(json.dumps(dict(status='PASS', exact_forced_supports=supports,
        U_original_role_controls=sum(roles.values()), U_qualifying_counts=dict(roles),
        rotor_original_role_controls=sum(rotor_roles.values()),
        rotor_qualifying_counts=dict(rotor_roles),
        scope='Finite full-original controls for a written all-dimension same-phase '
              'consumer uniqueness proof and forced m-new-owner consequence. '
              'No complete-extension existence, reserve increment or global bound.'), indent=2))


if __name__ == '__main__':
    main()
