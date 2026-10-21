"""Controls of an arbitrary-dimension support-gap obstruction and escape theorem."""

from collections import Counter
import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def normalized_pair(width, other_width, near, other_near, far, gap):
    return [independent_source((width, near, far), (True, False, False), (-width, 0)),
            independent_source((other_width, other_near, far),
                               (True, True, True), (other_width-gap, far+2))]


def gap_controls():
    counts = Counter()
    for width, other_width, near, other_near, far, gap in itertools.product(
            (6, 8, 14, 28), (6, 8, 14, 28), (4, 10, 24), (4, 10, 24),
            (4, 6, 12, 24), (2, 3)):
        first, second = normalized_pair(width, other_width, near, other_near, far, gap)
        endpoints = first[0] | second[0]
        assert not first[0] & second[0]
        boundary = {(row, column) for row in range(-gap, 1)
                    for column in range(1, far+2)
                    if row in (-gap, 0) or column in (1, far+1)}
        inside = {(row, column) for row in range(1-gap, 0)
                  for column in range(2, far+1)}
        assert boundary <= endpoints and not inside & endpoints
        support = (-1, 3)
        assert support in inside & first[1] and (0, 3) in first[0]
        occupied = endpoints | first[1] | second[1]
        assert len(set(neighbors(support)) & occupied) >= 2
        if gap == 2:
            assert (-2, 3) in second[0] and support in second[1]
        else:
            assert (-2, 3) in second[1]-endpoints
            assert (-2, 3) in neighbors(support)
            assert len(set(neighbors(support)) & endpoints) == 1
            assert len(set(neighbors((-2, 3))) & endpoints) == 1
        counts[gap] += 1
    return dict(parameter_patterns=dict(counts),
                endpoint_only_checks_miss_the_gap_three_conflict=counts[3])


def source_candidates(point, blocked, absent=()):
    shapes = {}
    for parameters in itertools.product(range(6, 20, 2), range(4, 20, 2), range(4, 20, 2)):
        width, near, far = parameters
        for symmetry in itertools.product((False, True), repeat=3):
            for anchor in ((0, 1), (0, width), (near, 1), (far, width)):
                moved = affine(anchor, symmetry)
                offset = (point[0]-moved[0], point[1]-moved[1])
                record = independent_source(parameters, symmetry, offset)
                if record[0] & blocked or record[0] & set(absent):
                    continue
                key = frozenset(record[0]), frozenset(record[1]), frozenset(record[2])
                shapes[key] = record
    rotors = {}
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        for anchor in module['endpoints']:
            if len(set(neighbors(anchor)) & module['endpoints']) != 1:
                continue
            current = transform_module(module, (False, False, False),
                                       (point[0]-anchor[0], point[1]-anchor[1]))
            if current['endpoints'] & blocked or current['endpoints'] & set(absent):
                continue
            rotors[frozenset(current['endpoints'])] = current
    return list(shapes.values()), list(rotors.values())


def excluded_corner(record, bottom):
    endpoints = record[0]
    first = min(row for row, _ in endpoints)
    last = max(row for row, _ in endpoints)
    width = last-first+1
    near = max(column for row, column in endpoints if row == first)-5
    if width < 6 or near < 4 or last != bottom:
        return False
    return record == independent_source((width, near, 4),
                                        (True, False, False), (bottom-width, 5))


def escape(record, leg):
    endpoints = record[0]
    first = min(row for row, _ in endpoints)
    last_column = max(column for _, column in endpoints)
    width = last_column-4
    near = leg-1-first
    far = max(row for row, column in endpoints if column == last_column)-first
    if width < 6 or min(near, far) < 4:
        return False
    expected = independent_source((width, near, far), (False, False, False), (first, 4))
    if record != expected:
        return False
    assert 6 <= near <= leg-6
    return True


def chain(leg, corner_far):
    height = leg+6
    specifications = [((height+4, 4, 4), (False, False, False), (0, 0)),
                      ((12, leg, 4), (False, True, False), (leg+3, 1)),
                      ((leg+4, height, 4), (True, True, False), (1, height+2)),
                      ((leg-2, 4, corner_far), (True, False, False), (2, 3)),
                      ((6, 8, 4), (True, True, True), (leg+2, 11))]
    records = [independent_source(*specification) for specification in specifications]
    fixed = set().union(*(record[0] for record in records))
    assert len(fixed) == sum(len(record[0]) for record in records)
    return fixed


def role_controls():
    results = []
    for leg, corner_far in itertools.product((8, 10, 12, 18), (4, 6)):
        fixed = chain(leg, corner_far)
        lower = (leg-1, 5)
        upper = (leg-2, 5)
        candidates, rotors = source_candidates(lower, fixed)
        assert not rotors
        excluded = sum(excluded_corner(record, leg-1) for record in candidates)
        survivors = [record for record in candidates if not excluded_corner(record, leg-1)]
        assert all(escape(record, leg) for record in survivors)
        if leg <= 10:
            assert not survivors
        upper_candidates, upper_rotors = source_candidates(upper, fixed, (lower,))
        upper_excluded = sum(excluded_corner(record, leg-2) for record in upper_candidates)
        assert all(excluded_corner(record, leg-2) or lower in record[1]
                   for record in upper_candidates)
        assert all(lower in record['selected'] for record in upper_rotors)
        results.append(dict(leg=leg, corner_far=corner_far, lower_U_candidates=len(candidates),
                            lower_gap_three_exclusions=excluded,
                            lower_necessary_north_escapes=len(survivors), lower_rotors=0,
                            upper_U_candidates_with_lower_absent=len(upper_candidates),
                            upper_gap_two_exclusions=upper_excluded,
                            upper_U_force_lower=len(upper_candidates)-upper_excluded,
                            upper_rotors_force_lower=len(upper_rotors)))
    return results


def translation_controls():
    cases = 0
    for leg, width, near, gap in itertools.product(
            (10, 14, 24), (6, 10, 20), (4, 8, 20), (2, 3)):
        first, second = normalized_pair(width, 6, near, 8, 4, gap)
        bottom = leg-4+gap
        offset = (bottom, 5)
        moved = []
        for record in (first, second):
            endpoints, support, matching = record
            move = lambda point: (point[0]+offset[0], point[1]+offset[1])
            moved.append(({move(point) for point in endpoints},
                          {move(point) for point in support},
                          {tuple(sorted((move(start), move(end)))) for start, end in matching}))
        assert moved[0] == independent_source((width, near, 4),
                                              (True, False, False), (bottom-width, 5))
        assert moved[1] == independent_source((6, 8, 4),
                                              (True, True, True), (leg+2, 11))
        cases += 1
    return cases


def cross_owner_controls():
    lower_collisions = upper_exclusions = 0
    for leg, height, far in itertools.product(range(8, 32, 2), range(8, 34, 2), range(4, 40, 2)):
        cross = independent_source((leg-2, height, far),
                                   (True, True, False), (1, height+2))
        corner = independent_source((leg-2, 4, 4), (True, False, False), (2, 3))
        if (leg-1, 5) in cross[0]:
            assert (leg-1, 4) in cross[0] & corner[0]
            lower_collisions += 1
        assert (leg-2, 5) not in cross[0]
        upper_exclusions += 1
    return dict(lower_same_owner_collisions=lower_collisions,
                upper_parity_exclusions=upper_exclusions)


def controls():
    return dict(status='PASS', opposed_gap=gap_controls(),
                actual_corner_roles=role_controls(), translated_intruder_identities=translation_controls(),
                cross_owner_exclusions=cross_owner_controls(),
                scope='Independent finite endpoint/support/matching and anchored-role controls of '
                      'a separate arbitrary-dimension proof. The role library bounds widths/legs '
                      'at18; it does not supply unbounded exhaustion. Necessary H escapes are '
                      'partial, not complete witnesses. No new reserve is assigned to impossible '
                      'two-source intruders; full allocation/grid remains open.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
