"""Exact corner receipts and full bounded joint-consumer role controls."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import endpoint_tiles, phi, sources
from check_secondary_ten_persistent_pair_compensation import rotor_record


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def corner(origin, width, breadth, near, far, horizontal):
    return independent_source((breadth, near, far),
                              (False, True, False) if horizontal else (True, False, True),
                              (origin+1, width+13) if horizontal else (origin+2, width+14))


def controls():
    horizontal_count = vertical_count = roles = rotor_roles = 0
    for bottom, width in itertools.product((-24, 40), (12, 20, 50)):
        origin = bottom-9
        for gap, far in ((8, 4), (8, 14), (10, 16), (10, 200)):
            records = sources(bottom, width)+[
                returning(bottom, width, 0),
                continuation(bottom, width, width+gap, 8, far, False)]
            for breadth, near, other, horizontal in itertools.product(
                    (6, 8, 50), (4, 12, 50), (4, 20, 200), (False, True)):
                current = corner(origin, width, breadth, near, other, horizontal)
                assert {(origin, width+14), (origin+1, width+14)} <= current[0]
                assert all(not current[0] & record[0] for record in records)
                half_legs = (near+other)//2
                tiles = endpoint_tiles(current)
                inside = {point for point in current[1]
                          if (point[0]//2, point[1]//2) in tiles}
                assert len(current[2]) == breadth+half_legs-1
                before, after, signature = tile_signature(records, current)
                assert signature == {(origin+1, width+14): (0, int(horizontal))}
                assert after['full'] == before['full']
                if horizontal:
                    assert len(tiles) == breadth+half_legs-2
                    assert len(inside) == half_legs-2 and charge(current) == 1-breadth
                    assert after['mass']-before['mass'] == breadth-1
                    assert after['events']-before['events'] == {
                        (8, (origin+1, width+14), (origin+2, width+14))}
                    assert phi(records+[current])-phi(records) == breadth-2 >= 4
                    horizontal_count += 1
                else:
                    assert len(tiles) == breadth//2+half_legs+1
                    assert len(inside) == half_legs+4 and charge(current) == 1
                    assert after['mass'] == before['mass'] and after['events'] == before['events']
                    assert phi(records+[current])-phi(records) == 1
                    vertical_count += 1
    library, rotors = axial_library({(-1, 0), (0, 1)})
    joint_library = [record for record in library if (-1, 0) in record[0]]
    joint_rotors = [record for record in rotors if (-1, 0) in record[0]]
    assert len(joint_rotors) == 2
    for gap, far in ((8, 4), (10, 16)):
        bottom, width = 40, 12
        origin = bottom-9
        point = origin+1, width+14
        records = sources(bottom, width)+[
            returning(bottom, width, 0),
            continuation(bottom, width, width+gap, 8, far, False)]
        occupied = set.union(*(record[0] for record in records))
        for relative in joint_library:
            current = shift(relative, point)
            if current[0] & occupied:
                continue
            own = {(row-point[0], column-point[1]) for row, column in current[0]
                   if abs(row-point[0])+abs(column-point[1]) == 1}
            if own == {(-1, 0)}:
                first = min(row for row, column in current[0])
                low = min(column for row, column in current[0])
                high = max(column for row, column in current[0])
                right = low == point[1]
                assert right or high == point[1]
                breadth = high-low+1
                incident = point[0]-first
                column = high if right else low
                other = max(row for row, col in current[0] if col == column)-first
                expected = independent_source((breadth, incident, other), (False, False, not right),
                                              (first, width+13 if right else width+15))
            else:
                assert own == {(-1, 0), (0, 1)}
                horizontal = (point[0]-1, point[1]+2) in current[0]
                if horizontal:
                    last = max(column for row, column in current[0])
                    breadth = last-point[1]+1
                    incident = point[0]-min(row for row, col in current[0] if col == point[1])
                    other = point[0]-min(row for row, col in current[0] if col == last)
                else:
                    first = min(row for row, column in current[0])
                    breadth = point[0]-first+1
                    incident = max(col for row, col in current[0] if row == point[0])-point[1]
                    other = max(col for row, col in current[0] if row == first)-point[1]
                expected = corner(origin, width, breadth, incident, other, horizontal)
            assert current == expected
            roles += 1
        for relative in joint_rotors:
            current = shift(relative, point)
            if current[0] & occupied:
                assert (origin, width+13) in current[0] & records[4][0]
            else:
                assert current == rotor_record(origin, width)
            rotor_roles += 1
    return dict(horizontal_corner_exact_receipts=horizontal_count,
                vertical_corner_exact_receipts=vertical_count,
                bounded_joint_U_full_source_role_controls=roles,
                joint_rotor_catalogue_controls=rotor_roles,
                U_catalogue_dimensions_at_most=18,
                all_parameter_classification_proved_in_written_note=True,
                distinct_consumers_or_global_nonreuse_solved=False)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', controls=controls(),
                         scope='Finite corroboration of the written full joint-consumer role '
                         'classification and corner charge/contact proofs. General north-terminal '
                         'receipts and zero continuations have separate controls.'), indent=2))
