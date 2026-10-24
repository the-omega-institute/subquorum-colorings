"""Exact source and event controls for the distinct-owner residual proof."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import endpoint_tiles, sources
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def east_source(origin, width, breadth, near, far, north):
    return independent_source((breadth, near, far), (True, True, north),
                              (origin+2 if north else origin, width+14+near))


def upper_source(origin, width, breadth, near, far, right):
    return independent_source((breadth, near, far), (False, False, not right),
                              (origin-near, width+13 if right else width+15))


def east_rotor(origin, width, north):
    module = transform_module(rotor(), (False, not north, False),
                              (origin-2 if north else origin+4, width+13))
    return module['endpoints'], module['selected'], {
        tuple(sorted(edge)) for edge in module['matching']}


def upper_rotor(origin, width, left):
    module = transform_module(rotor(), (False, False, not left),
                              (origin-4, width+11 if left else width+17))
    return module['endpoints'], module['selected'], {
        tuple(sorted(edge)) for edge in module['matching']}


def source_counts(current, matching_count, tile_count, support_count):
    tiles = endpoint_tiles(current)
    inside = {point for point in current[1]
              if (point[0]//2, point[1]//2) in tiles}
    assert (len(current[2]), len(tiles), len(inside)) == (
        matching_count, tile_count, support_count)


def parameter_controls():
    east_criteria = east_sets = upper_criteria = upper_sets = rotor_sets = blockers = 0
    for bottom, width in itertools.product((-24, 40), (12, 20, 50)):
        origin = bottom-9
        for gap, old_far in ((8, 4), (8, 14), (10, 16), (10, 200)):
            records = sources(bottom, width)+[
                returning(bottom, width, 0),
                continuation(bottom, width, width+gap, 8, old_far, False)]
            endpoints = set.union(*(record[0] for record in records))
            for breadth, near, north in itertools.product(
                    (6, 8, 10, 12, 50), (4, 6, 8, 12, 50), (False, True)):
                for far in sorted({4, 6, near-2, near, near+2, near+4,
                                   width+near, width+near+2, width+near+4, 200}):
                    if far < 4:
                        continue
                    current = east_source(origin, width, breadth, near, far, north)
                    assert (origin+1, width+14) in current[0]
                    assert (origin, width+14) not in current[0]
                    allowed = ((breadth >= 10 or far <= near+2) if north else
                               ((breadth == 6 and far <= near-2) or
                                (breadth in (8, 10) and far <= width+near+2) or
                                (breadth >= 12 and
                                 (gap == 8 or old_far < breadth+6 or far <= width+near+10))))
                    assert (not current[0] & endpoints) == allowed, (
                        bottom, width, gap, old_far, breadth, near, far, north,
                        sorted(current[0] & endpoints))
                    east_criteria += 1
                    if not allowed:
                        continue
                    half = (near+far)//2
                    source_counts(current, breadth+half-1,
                                  breadth+half if north else breadth+half-2,
                                  half+2 if north else half-2)
                    assert charge(current) == 1-breadth
                    before, after, signature = tile_signature(records, current)
                    expected = {(origin+1, width+14): (0, int(not north))}
                    expected_events = (set() if north else {
                        (8, (origin+1, width+14), (origin+2, width+14))})
                    if not north and breadth == 8:
                        first = width+14+near-far
                        for column in (width+2, width+4):
                            if first <= column:
                                expected[(origin+7, column)] = (1, 2)
                                expected_events |= {
                                    (8, (origin+8, column), (origin+7, column)),
                                    (5, (origin+7, column), (origin+8, column))}
                        if first <= width:
                            expected[(origin+7, width)] = (0, 0)
                    assert signature == expected
                    assert after['events']-before['events'] == expected_events
                    assert after['mass']-before['mass'] == breadth-1
                    assert after['raw_reserve']-before['raw_reserve'] == breadth-1-int(not north)
                    east_sets += 1
            for north in (False, True):
                terminal = east_rotor(origin, width, north)
                before, after, signature = tile_signature(records, terminal)
                assert charge(terminal) == 0
                expected_rotor = ({(origin+1, width+14): (0, 0)} if north else
                                  {(origin+1, width+14): (1, 2),
                                   (origin+3, width+14): (0, 1)})
                assert signature == expected_rotor
                expected_events = (set() if north else {
                    (8, (origin+1, width+14), (origin+2, width+14)),
                    (8, (origin+2, width+15), (origin+2, width+14)),
                    (3, (origin+3, width+14), (origin+3, width+15))})
                assert after['events']-before['events'] == expected_events
                assert after['mass'] == before['mass']
                assert after['raw_reserve']-before['raw_reserve'] == -int(not north)
                rotor_sets += 1
                prefix = records+[terminal]
                occupied = endpoints | terminal[0]
                for breadth, near, right in itertools.product(
                        (6, 8, width+10, width+12, width+14, width+50),
                        (4, 6, 8, 10, 12, 16, 50), (False, True)):
                    column = width+15-breadth
                    for far in sorted({4, 6, near-10, near-8, near-6,
                                       near+6, near+8, near+10, 200}):
                        if far < 4:
                            continue
                        current = upper_source(origin, width, breadth, near, far, right)
                        allowed = right or (
                            (column >= width+12-(width+gap) and near >= 12 and far <= near-8) or
                            (column == 3 and gap == 8 and near >= 8 and far <= near+8) or
                            (column <= 1 and near >= 8))
                        assert (not current[0] & occupied) == allowed
                        upper_criteria += 1
                        if not allowed:
                            continue
                        half = (near+far)//2
                        source_counts(current, breadth+half-1,
                                      breadth+half-2 if right else breadth+half,
                                      half-2 if right else half+2)
                        assert charge(current) == 1-breadth
                        before, after, signature = tile_signature(prefix, current)
                        expected = {(origin-1, width+14): (1, 2)} if north else {}
                        expected_events = set()
                        if north:
                            expected_events.add((8, (origin, width+15), (origin, width+14)))
                            expected_events.add((9, (origin if right else origin-1, width+14),
                                                 (origin if right else origin-1, width+15)))
                        if not right and near == 8:
                            first = width+12-(width+gap)
                            expected.update({(origin-7, col): (1, 4)
                                             for col in range(first, width+11, 2)})
                            for contact_column in range(first, width+12):
                                expected_events |= {
                                    (9, (origin-7, contact_column), (origin-6, contact_column)),
                                    (7, (origin-6, contact_column), (origin-7, contact_column))}
                        assert signature == expected, (bottom, width, gap, old_far,
                                                       north, breadth, near, far, right,
                                                       signature, expected)
                        assert after['events']-before['events'] == expected_events
                        assert after['mass']-before['mass'] == breadth-1
                        debit = width+gap if not right and near == 8 else 0
                        assert after['raw_reserve']-before['raw_reserve'] == breadth-1-debit >= 3
                        upper_sets += 1
            left = upper_rotor(origin, width, True)
            right = upper_rotor(origin, width, False)
            assert not (left[0] | right[0]) & endpoints
            point = origin, width+12
            assert point in records[7][1] and point not in endpoints | left[0]
            assert {(origin, width+11), (origin, width+13), (origin-1, width+12)} <= endpoints | left[0]
            assert (origin+3, width+12) in records[4][0]
            point = origin-1, width+13
            assert point in records[4][1] and point not in endpoints | right[0]
            assert {(origin-2, width+13), (origin-1, width+14), (origin, width+13)} <= endpoints | right[0]
            assert (origin-1, width+11) in records[7][0]
            blockers += 2
    return dict(east_U_exact_disjointness_controls=east_criteria,
                east_U_original_charge_and_complete_tile_event_sets=east_sets,
                upper_U_exact_disjointness_controls=upper_criteria,
                upper_U_original_charge_and_complete_tile_event_sets=upper_sets,
                east_rotor_exact_receipts=rotor_sets,
                upper_rotor_forced_support_blockers=blockers)


def role_controls():
    east, east_rotors = axial_library({(0, 1)})
    upper, upper_rotors = axial_library({(-1, 0), (0, 1)})
    south, south_rotors = axial_library({(1, 0)})
    west, west_rotors = axial_library({(0, -1)})
    assert len(east_rotors) == len(south_rotors) == len(west_rotors) == 2
    assert all((3, 0) in source[0] for source in south)
    assert all((0, -2) in source[0] for source in west+west_rotors)
    assert all((2, 1) in source[0] or (1, 1) in source[0] for source in south_rotors)
    assert all((0, 1) not in source[0] or (0, 2) in source[0]
               for source in upper+upper_rotors)
    count = 0
    bottom, width = 40, 12
    origin = bottom-9
    for gap, far in ((8, 4), (10, 16)):
        records = sources(bottom, width)+[
            returning(bottom, width, 0),
            continuation(bottom, width, width+gap, 8, far, False)]
        occupied = set.union(*(record[0] for record in records))
        for relative in east:
            current = shift(relative, (origin+1, width+14))
            if current[0] & occupied:
                continue
            rows = [point[0] for point in current[0]]
            columns = [point[1] for point in current[0]]
            north = min(rows) < origin+1
            breadth = max(rows)-min(rows)+1
            near = max(columns)-width-14
            remote = min(rows) if north else max(rows)
            far = max(columns)-min(col for row, col in current[0] if row == remote)
            assert current == east_source(origin, width, breadth, near, far, north)
            count += 1
        for north in (False, True):
            terminal = east_rotor(origin, width, north)
            prefix = occupied | terminal[0]
            for relative in upper+upper_rotors:
                current = shift(relative, (origin, width+14))
                if current[0] & prefix:
                    continue
                own = {(row-origin, col-width-14) for row, col in current[0]
                       if abs(row-origin)+abs(col-width-14) == 1}
                assert own == {(-1, 0)}
                count += 1
    return dict(bounded_full_original_role_controls=count,
                terminal_U_dimensions_at_most=18,
                mandatory_support_and_terminal_blocker_catalogues_checked=True,
                role_and_collision_proofs_are_written_for_all_parameters=True)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', parameters=parameter_controls(),
                         roles=role_controls(),
                         scope='Finite corroboration of the general written unconditional '
                         'residual-subinventory theorem. Not a proof of global nonreuse, '
                         'an exterior sign bound or rectangular-grid equality.'), indent=2))
