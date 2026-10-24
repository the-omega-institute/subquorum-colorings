"""Discovery controls for a five-step downward secondary-ten chain."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def discovery():
    boundary, rotors = axial_library({(-1, 0), (0, 1)})
    bottom = 30
    fixed = [independent_source((6, 8, 4), (True, True, True), (bottom+2, 11)),
             independent_source((24, 10, 6), (False, False, False), (bottom-11, 5))]

    def east(level):
        return independent_source((8+2*level, 6+2*level, 4),
                                  (True, True, False), (bottom-6-level, 13+2*level))

    fixed.append(east(0))
    counts = []
    for level in range(1, 5):
        assert all(not first[0] & second[0] for first, second in itertools.combinations(fixed, 2))
        point = bottom-5-level, 7
        blocked = set.union(*(record[0] for record in fixed))
        assert point in fixed[-1][1] and point not in blocked
        assert (point[0], 6) in fixed[1][0]
        surviving = 0
        for relative in boundary:
            record = shift(relative, point)
            if record[0] & blocked:
                continue
            outer = max(column for row, column in record[0])
            incident = outer-7
            breadth = max(row for row, column in record[0])-(bottom-6-level)
            far = outer-min(column for row, column in record[0]
                            if row == bottom-6-level+breadth)
            assert record == independent_source((breadth, incident, far),
                                                 (True, True, False), (bottom-6-level, outer))
            assert 6+2*level <= incident <= 20
            expected_charge = 1 if level % 2 == 0 else -1
            assert charge(record) == expected_charge
            surviving += 1
        assert surviving
        assert all(shift(relative, point)[0] & blocked for relative in rotors)
        counts.append(dict(level=level, surviving_bounded_east_terminal_roles=surviving,
                           isolated_charge=1 if level % 2 == 0 else -1))
        fixed.append(east(level))
    assert all(not first[0] & second[0] for first, second in itertools.combinations(fixed, 2))
    return dict(status='PASS', fixed_secondary_far_leg=6, bounded_original_dimensions_max=18,
                seven_source_endpoint_disjoint_partial_stencil=True, stages=counts,
                rotor_exclusions=16, scope='Discovery controls only: candidate five-step east '
                'chain at secondary10 far>=6; no complete realization or extra ledger credit.')


if __name__ == '__main__':
    print(json.dumps(discovery(), indent=2))
