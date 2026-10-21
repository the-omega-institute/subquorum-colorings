"""Geometric controls of a six-source obstruction; finite discovery is not the proof."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_pair_transfer_protected_defects import original
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


FIXED = [
    ((10, 8, 4), (False, True, False), (11, 1)),
    ((18, 20, 10), (True, True, False), (1, 22)),
    ((6, 12, 4), (True, False, False), (2, 3)),
    ((14, 4, 4), (True, True, False), (2, 20)),
    ((6, 6, 4), (True, False, True), (18, 14)),
    ((8, 8, 4), (True, False, True), (19, 12))]
Q_SPECIFICATION = ((6, 6, 4), (True, True, True), (10, 9))


def catalogue_roles(point, fixed):
    assert point not in fixed
    candidates = {}
    for width, near, far in itertools.product(range(6, 28, 2), range(4, 28, 2), range(4, 28, 2)):
        for symmetry in itertools.product((False, True), repeat=3):
            for anchor in ((near, 1), (far, width), (0, 1), (0, width)):
                moved = affine(anchor, symmetry)
                offset = (point[0]-moved[0], point[1]-moved[1])
                record = independent_source((width, near, far), symmetry, offset)
                if record[0] & fixed:
                    continue
                key = frozenset(record[0])
                candidates.setdefault(key, ((width, near, far), symmetry, offset))
    rotor_candidates = set()
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        for anchor in module['endpoints']:
            own = set(neighbors(anchor)) & module['endpoints']
            if len(own) != 1:
                continue
            current = transform_module(module, (False, False, False),
                                       (point[0]-anchor[0], point[1]-anchor[1]))
            if not current['endpoints'] & fixed:
                rotor_candidates.add(frozenset(current['endpoints']))
    return candidates, rotor_candidates


def controls():
    records = [independent_source(*specification) for specification in FIXED]
    fixed = set().union(*(record[0] for record in records))
    assert len(fixed) == sum(len(record[0]) for record in records)
    first, rotor_forms = catalogue_roles((9, 3), fixed)
    forced = independent_source(*Q_SPECIFICATION)
    assert set(first) == {frozenset(forced[0])} and not rotor_forms
    assert original(*Q_SPECIFICATION)['charge'] == -1
    assert {(9, 2), (10, 3)} <= forced[1] & records[0][0]
    fixed |= forced[0]
    assert (4, 10) in records[2][1] and {(3, 10), (4, 9)} <= fixed
    second, rotor_forms = catalogue_roles((4, 10), fixed)
    assert not rotor_forms
    corner_specifications = [((width, 4, far), (False, False, False), (4, 9))
                             for width, far in itertools.product((6, 8), (4, 6))]
    east_specifications = [((6, incident, far), (True, True, False), (3, incident+10))
                           for incident, far in ((6, 4), (8, 4), (8, 6))]
    expected = {frozenset(independent_source(*specification)[0])
                for specification in corner_specifications+east_specifications}
    assert set(second) == expected
    for specification in corner_specifications:
        current = independent_source(*specification)
        assert (9, 10) in current[1] and (9, 10) not in fixed | current[0]
        assert set(neighbors((9, 10))) <= fixed | current[0]
    late_counts = {}
    sealed = 0
    for specification in east_specifications:
        current = independent_source(*specification)
        assert original(*specification)['charge'] == -5
        endpoints = fixed | current[0]
        assert (10, 12) in records[5][1]
        late, rotor_forms = catalogue_roles((10, 12), endpoints)
        assert not rotor_forms
        name = 'P%d_far%d' % (specification[0][1], specification[0][2])
        late_counts[name] = len(late)
        if specification[0][1:] != (8, 4):
            assert not late
            continue
        final_specifications = [((6, 4, far), (True, False, False), (4, 12))
                                for far in (4, 6)]
        assert set(late) == {frozenset(independent_source(*choice)[0])
                             for choice in final_specifications}
        for choice in final_specifications:
            final = independent_source(*choice)
            assert not final[0] & endpoints
            whole = endpoints | final[0]
            boundary = {(row, column) for row in range(9, 13) for column in range(16, 20)
                        if row in (9, 12) or column in (16, 19)}
            assert boundary <= whole
            assert (11, 17) in records[5][1] and (11, 17) not in whole
            assert {(11, 16), (12, 17)} <= whole
            interior = {(row, column) for row in range(9, 13) for column in range(16, 20)}-boundary
            assert interior == {(10, 17), (10, 18), (11, 17), (11, 18)}
            assert (11, 17) in interior
            sealed += 1
    return dict(status='PASS', fixed_sources=len(records), fixed_endpoints=sum(len(record[0]) for record in records),
                first_U_consumer_shapes=len(first), first_rotor_consumers=0,
                second_U_consumer_shapes=len(second), impossible_corner_shapes=4,
                east_successor_shapes=3, east_successor_charge=-5, late_U_consumer_counts=late_counts,
                late_rotor_consumers=0, sealed_two_by_two_cases=sealed,
                catalogue_widths=[6, 26], catalogue_independent_legs=[4, 26],
                scope='Finite role controls verify a separate written arbitrary-dimension proof; not enumeration-based exhaustion or a complete witness.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
