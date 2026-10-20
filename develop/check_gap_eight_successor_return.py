"""Controls of old-P return rigidity; the displayed family is PARTIAL."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_cooperative_promotion import neighbors


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def interval_controls():
    count = 0
    matched = 0
    for width, height, far, incident, return_leg in itertools.product(
            (10, 18, 26), (12, 18), (4, 10, 18), (4, 8, 16), (6, 10, 18, 24)):
        if return_leg < incident+2:
            continue
        cross = independent_source((width, height, far),
                                   (True, True, False), (1, height+2))
        returned = independent_source((width, return_leg, height),
                                      (True, True, True),
                                      (width+2, height+return_leg-incident))
        common = (width+1, height+1)
        assert common in cross[0] & returned[0]
        cross_interval = {column for row, column in cross[0] if row == width+1}
        return_interval = {column for row, column in returned[0] if row == width+1}
        assert cross_interval == set(range(height+2-far, height+3))
        assert return_interval == set(range(height-incident, height+return_leg-incident+1))
        equal = cross[0] == returned[0]
        assert equal == (return_leg == incident+2 and far == incident+2)
        if equal:
            assert cross == returned
            matched += 1
        count += 1
    return dict(interval_and_common_endpoint_cases=count, matched_full_source_identities=matched)


def partial_pattern():
    specifications = [
        ((22, 4, 4), (False, False, False), (0, 0)),
        ((8, 8, 4), (False, True, False), (11, 1)),
        ((18, 18, 10), (True, True, False), (1, 20)),
        ((6, 10, 4), (True, False, False), (2, 3)),
        ((14, 4, 4), (True, True, False), (2, 18)),
        ((6, 6, 4), (True, False, True), (18, 12)),
        ((8, 8, 4), (True, False, True), (19, 10)),
        ((14, 4, 4), (False, True, False), (21, 8))]
    modules = [independent_source(*specification) for specification in specifications]
    for first, second in itertools.combinations(modules, 2):
        assert not first[0] & second[0]
        assert not first[2] & second[2]
    cross, terminal, producer = modules[2], modules[6], modules[7]
    assert independent_source((18, 10, 18), (True, True, True), (20, 20)) == cross
    assert (18, 18) in terminal[0]
    assert {(18, 19), (19, 18)} <= terminal[1] & cross[0]
    assert {(18, 10), (18, 11)} <= terminal[0]
    assert (18, 10) in producer[1]
    assert (19, 10) in terminal[1] & cross[0]
    chain = [(0, 1, (3, 2)), (1, 2, (2, 2)), (2, 3, (3, 3)),
             (3, 4, (3, 14)), (4, 5, (17, 18)), (5, 6, (18, 18))]
    for support_owner, endpoint_owner, point in chain:
        assert point in modules[support_owner][1] & modules[endpoint_owner][0]
    endpoints = set().union(*(module[0] for module in modules))
    supports = set().union(*(module[1] for module in modules))-endpoints
    occupied = endpoints | supports
    violations = sum(len(set(neighbors(point)) & occupied) != 1 for point in supports)
    assert violations > 0
    return dict(specifications=specifications, endpoints=len(endpoints),
                remaining_support_degree_violations=violations,
                scope='PARTIAL ONLY: not a complete-family witness or compensation counterexample.')


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', controls=interval_controls(),
                          matched_partial=partial_pattern()), indent=2))
