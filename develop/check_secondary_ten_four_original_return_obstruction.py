"""Exact source and role controls for a four-original complete-extension obstruction."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import shift
from check_secondary_ten_both_far_charge_separation import counts
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_next_support_east_terminal import return_family
from check_secondary_ten_north_contact_debit import inventory
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def blockers(column):
    return ({(row, column-1) for row in range(23, 34)} |
            {(row, column+1) for row in range(25, 32)} |
            {(22, column), (31, column)})


def four_originals(width):
    column = width+13
    return [independent_source((6, 6, 4), (False, False, False), (25, column)),
            independent_source((width+12, 10, 4), (False, False, True), (23, column)),
            independent_source((6, 4, 4), (False, True, False), (35, width+7)),
            independent_source((6, 4, width+8), (True, True, False), (16, width+15))]


def role_controls():
    column = 25
    support = 25, column
    occupied = blockers(column)
    roles = collisions = corners = rotor_roles = 0
    normalizations = set()
    for dimensions, symmetry in itertools.product(
            itertools.product((6, 8, 14, 40), (4, 6, 8, 40), (4, 6, 8, 40)),
            itertools.product((False, True), repeat=3)):
        original = independent_source(dimensions, symmetry, (0, 0))
        for anchor in original[0]:
            internal = {(point[0]-anchor[0], point[1]-anchor[1])
                        for point in set(neighbors(anchor)) & original[0]}
            if not internal or not internal <= {(-1, 0), (1, 0)}:
                continue
            roles += 1
            candidate = shift(original, (support[0]-anchor[0], support[1]-anchor[1]))
            if candidate[0] & occupied:
                collisions += 1
                continue
            breadth = max(value for row, value in candidate[0] if row == 23)-column+1
            near = max(row for row, value in candidate[0] if value == column)-23
            far = max(row for row, value in candidate[0]
                      if value == column+breadth-1)-23
            expected = independent_source((breadth, near, far),
                                         (False, False, False), (23, column-1))
            assert candidate == expected and near in (4, 6)
            assert breadth >= 6 and far >= 4
            normalizations.add((breadth, near, far))
            corners += 1
    rotor_patterns = set()
    for symmetry in itertools.product((False, True), repeat=3):
        module = transform_module(rotor(), symmetry)
        for anchor in module['endpoints']:
            internal = {(point[0]-anchor[0], point[1]-anchor[1])
                        for point in set(neighbors(anchor)) & module['endpoints']}
            if not internal or not internal <= {(-1, 0), (1, 0)}:
                continue
            endpoints = {(row-anchor[0]+25, value-anchor[1]+column)
                         for row, value in module['endpoints']}
            assert endpoints & occupied
            direction = next(iter(internal))[0]
            assert (25+2*direction, column-1) in endpoints & occupied
            rotor_patterns.add(frozenset(endpoints))
            rotor_roles += 1
    assert len(rotor_patterns) == 4 and corners and collisions
    return dict(eligible_U_roles=roles, colliding_U_roles=collisions,
                exact_corner_normalizations=corners,
                distinct_corner_records=len(normalizations),
                excluded_rotor_placements=rotor_roles, rotor_patterns=4)


def gate_controls():
    cases = three_gates = four_gates = rotor_roles = 0
    for column, breadth, depth, far in itertools.product(
            (-101, 25, 2013), (6, 8, 40, 2000), (4, 6), (4, 40, 2000)):
        corner = independent_source((breadth, depth, far),
                                    (False, False, False), (23, column-1))
        occupied = blockers(column)
        assert not corner[0] & occupied
        support = 24+depth, column
        assert support in corner[1] and support not in corner[0] | occupied
        neighbours = set(neighbors(support)) & (occupied | corner[0])
        expected = {(23+depth, column), (24+depth, column-1),
                    (24+depth, column+1)}
        if depth == 6:
            expected.add((31, column))
            four_gates += 1
        else:
            three_gates += 1
            for length in (4, 6, 40, 2000):
                assert (31, column) in {(support[0]+step, column)
                                       for step in range(length+1)} & occupied
            patterns = set()
            for symmetry in itertools.product((False, True), repeat=3):
                module = transform_module(rotor(), symmetry)
                for anchor in module['endpoints']:
                    internal = {(point[0]-anchor[0], point[1]-anchor[1])
                                for point in set(neighbors(anchor)) & module['endpoints']}
                    if internal != {(1, 0)}:
                        continue
                    endpoints = {(row-anchor[0]+support[0], value-anchor[1]+column)
                                 for row, value in module['endpoints']}
                    assert (30, column-1) in endpoints & occupied
                    patterns.add(frozenset(endpoints))
            assert len(patterns) == 2
            rotor_roles += len(patterns)
        assert neighbours == expected
        cases += 1
    return dict(exact_corner_second_support_controls=cases,
                three_neighbour_gates=three_gates, four_neighbour_gates=four_gates,
                south_rotor_exclusions=rotor_roles)


def application_controls():
    subfamilies = inherited = isometries = 0
    for width in (12, 14, 50, 2000):
        originals = four_originals(width)
        column = width+13
        occupied = set.union(*(record[0] for record in originals))
        assert len(occupied) == sum(len(record[0]) for record in originals)
        assert blockers(column) <= occupied
        support = 25, column
        assert support in originals[0][1] and support not in occupied
        assert not {(25, column), (28, column), (30, column)} & occupied
        assert set(neighbors(support)) & occupied == {(25, column-1), (25, column+1)}
        subfamilies += 1
        for far in (4, 6, 40, 2000):
            family = return_family(width, far)
            assert originals == [family[index] for index in (18, 19, 4, 28)]
            inherited += 1
        for symmetry, translation in itertools.product(
                itertools.product((False, True), repeat=3), ((0, 0), (-64, -100), (20, 200))):
            moved = lambda point: affine(point, symmetry, translation)
            transformed = [{moved(point) for point in record[0]} for record in originals]
            moved_occupied = set.union(*transformed)
            assert len(moved_occupied) == sum(map(len, transformed))
            assert {moved(point) for point in blockers(column)} <= moved_occupied
            assert moved(support) not in moved_occupied
            assert set(neighbors(moved(support))) & moved_occupied == {
                moved((25, column-1)), moved((25, column+1))}
            isometries += 1
    return dict(full_four_original_subfamilies=subfamilies,
                exact_H3_family_inclusions=inherited, isometric_applications=isometries)


def short_return_controls():
    exact = excluded = 0
    for width, far in ((12, 4), (50, 40), (2000, 2000)):
        family = return_family(width, far)[:-1]
        before = inventory(family)
        column = width+13
        fixed = four_originals(width)[:3]
        for breadth, depth, other in itertools.product(
                (6, 8, 2000), sorted({4, 6, width+4, width+6, width+8, 2000}),
                (4, 6, 2000)):
            bar = 7+depth
            record = independent_source((breadth, depth, other),
                                        (True, True, True), (23, bar))
            after = inventory(family+[record])
            assert counts(record) == (breadth-1+(depth+other)//2,
                                      breadth//2+1+(depth+other)//2, 4+(depth+other)//2)
            if depth >= width+6:
                occupied = set.union(*(original[0] for original in fixed+[record]))
                assert blockers(column) <= occupied
                assert not {(25, column), (28, column), (30, column)} & occupied
                excluded += 1
                continue
            assert depth <= width+4
            full = {(11, value//2) for value in range(6, bar, 2)}
            events = {(19, (23, value), (22, value)) for value in range(7, bar+1)}
            events |= {(len(family), (22, value), (23, value))
                       for value in range(8, bar, 2)}
            assert after['full']-before['full'] == full and len(full) == depth//2+1
            assert after['events']-before['events'] == events and len(events) == 3*depth//2+1
            assert {(19, (23, 6), (22, 6)),
                    (27, (22, 6), (23, 6))} <= before['events'] & after['events']
            assert phi_from(family+[record], after)-phi_from(family, before) == 2-depth//2
            exact += 1
    return dict(exact_short_return_receipts=exact, excluded_reaching_return_controls=excluded)


def main():
    print(json.dumps(dict(status='PASS', roles=role_controls(), gates=gate_controls(),
        applications=application_controls(), short_returns=short_return_controls(),
        scope='Finite controls supplement the general four-original no-complete-extension '
        'proof in the full even-U/rotor model. No global inequality or catalogue '
        'exhaustion is claimed.'), indent=2))


if __name__ == '__main__':
    main()
