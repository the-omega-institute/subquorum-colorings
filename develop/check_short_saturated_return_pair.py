"""Finite controls of the general four-row chamber and joint pair theorem."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_pair_transfer_protected_defects import original
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def pair_records(leg, near, far, incident):
    corner = independent_source((leg-2, near, far),
                                (True, False, False), (2, 3))
    consumer = independent_source((6, incident, incident-2),
                                  (True, True, True), (leg+2, incident+3))
    return corner, consumer


def pair_controls():
    patterns = images = far_owners = accepted_rotors = rotor_controls = 0
    for leg, near, far, incident in itertools.product(
            (8, 10, 16, 30), (4, 8, 20), (4, 6, 10, 18), (6, 8, 12, 20, 28)):
        if incident < far+2:
            continue
        corner, consumer = pair_records(leg, near, far, incident)
        fixed = corner[0] | consumer[0]
        assert not corner[0] & consumer[0]
        assert original((6, incident, incident-2),
                        (True, True, True), (leg+2, incident+3))['charge'] == -1
        boundary = {(row, column) for row in range(leg-4, leg+2)
                    for column in range(4, incident+3)
                    if row in (leg-4, leg+1) or column in (4, incident+2)}
        inside = {(row, column) for row in range(leg-3, leg+1)
                  for column in range(5, incident+2)}
        assert boundary <= fixed and not inside & consumer[0]
        assert inside & corner[0] == {(leg, column) for column in range(5, far+4)}
        pair = {(leg-2, 4), (leg-1, 4)}
        missing = {(leg-2, 5), (leg-1, 5)}
        tile = pair | missing
        assert tile & fixed == pair and not tile & corner[1]
        assert missing <= inside and {(leg, 6), (leg, 7)} <= corner[0]
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            moved = set()
            for row, column in tile:
                moved_row = 1-row if flip_row else row
                moved_column = 1-column if flip_column else column
                moved.add((moved_column, moved_row) if transpose else (moved_row, moved_column))
            assert len({(row//2, column//2) for row, column in moved}) == 1
            images += 1
        for symmetry in itertools.product((False, True), repeat=3):
            shape = transform_module(rotor(), symmetry)
            row_offset = leg-3-min(row for row, _ in shape['endpoints'])
            for column_offset in range(5-min(column for _, column in shape['endpoints']), incident+3):
                current = {(row+row_offset, column+column_offset)
                           for row, column in shape['endpoints']}
                if not current <= inside:
                    continue
                rotor_controls += 1
                if any(column == 5 for _, column in current):
                    assert current & {(leg, 6), (leg, 7)}
                    far_owners += 1
                if not current & fixed:
                    assert all(column != 5 for _, column in current)
                    accepted_rotors += 1
        patterns += 1
    return dict(endpoint_disjoint_patterns=patterns, aligned_images=images,
                confined_rotor_images=rotor_controls,
                first_column_rotor_collisions=far_owners,
                farther_right_endpoint_only_rotor_images=accepted_rotors)


def rotor_shapes():
    expected = {
        frozenset({(-2, 1), (-1, 1), (-1, 2), (-1, 3),
                   (0, 0), (0, 1), (0, 2), (1, 2)}),
        frozenset({(-1, 2), (0, 0), (0, 1), (0, 2),
                   (1, 1), (1, 2), (1, 3), (2, 1)})}
    normalized = set()
    for symmetry in itertools.product((False, True), repeat=3):
        shape = transform_module(rotor(), symmetry)['endpoints']
        first_column = min(column for _, column in shape)
        tips = [point for point in shape if point[1] == first_column]
        assert len(tips) == 1
        anchor = tips[0]
        current = frozenset((row-anchor[0], column-anchor[1]) for row, column in shape)
        normalized.add(current)
    assert normalized == expected
    extent = 0
    for parameters, symmetry in itertools.product(
            itertools.product((6, 8, 20), (4, 10, 28), (4, 12, 30)),
            itertools.product((False, True), repeat=3)):
        endpoints = independent_source(parameters, symmetry, (0, 0))[0]
        assert max(row for row, _ in endpoints)-min(row for row, _ in endpoints) >= 4
        extent += 1
    return dict(normalized_left_tip_shapes=len(normalized), U_extent_controls=extent)


def actual_chain_controls():
    actual = old_frames = 0
    for leg, far, incident in itertools.product((8, 10, 18), (4, 6, 8), (6, 8, 12)):
        if incident < far+2:
            continue
        width = incident+4
        height = width+2
        corner, consumer = pair_records(leg, 4, far, incident)
        specifications = [((height+4, 4, 4), (False, False, False), (0, 0)),
                          ((width, leg, 4), (False, True, False), (leg+3, 1)),
                          ((leg+width+4, height, 4), (True, True, False), (1, height+2))]
        records = [independent_source(*specification) for specification in specifications]
        records += [corner, consumer]
        endpoints = set().union(*(record[0] for record in records))
        assert len(endpoints) == sum(len(record[0]) for record in records)
        assert (3, 2) in records[1][0] and (3, 3) in corner[0]
        assert (leg+1, 3) in corner[1] & consumer[0]
        assert {(leg+1, 2), (leg+2, 3)} <= consumer[1] & records[1][0]
        for old_height in range(4, 30, 2):
            old_cross = independent_source((6, old_height, 4),
                                           (False, False, False), (leg+1-old_height, 1))
            assert (leg+1, 2) in old_cross[0] & records[1][0]
            assert (leg+1-old_height, 3) in old_cross[0]-records[1][0]
            old_frames += 1
        actual += 1
    return dict(endpoint_only_actual_marked_chain_patterns=actual,
                old_H_owner_frame_exclusions=old_frames)


def opening_controls():
    intruders = shared = 0
    for leg in range(10, 42, 2):
        height = leg+4
        specifications = [((height+4, 4, 4), (False, False, False), (0, 0)),
                          ((12, leg, 4), (False, True, False), (leg+3, 1)),
                          ((leg+4, height, 4), (True, True, False), (1, height+2)),
                          ((leg-2, 4, 6), (True, False, False), (2, 3)),
                          ((6, 8, 4), (True, True, True), (leg+2, 11)),
                          ((6, 4, 4), (True, False, False), (leg-7, 5))]
        records = [independent_source(*specification) for specification in specifications]
        endpoints = set().union(*(record[0] for record in records))
        assert len(endpoints) == sum(len(record[0]) for record in records)
        assert {(leg-2, 5), (leg-1, 5)} <= records[-1][0]
        points = {(leg-5, 7), (leg-5, 8), (leg-5, 9)}
        supports = set().union(*(record[1] for record in records))
        assert points <= supports-endpoints
        assert all(len(set(neighbors(point)) & endpoints) >= 2 for point in points)
        intruders += 1
        if leg >= 14:
            current = independent_source((6, 4, 4), (True, True, True), (leg-4, 11))
            assert not current[0] & endpoints and points <= current[0]
            shared += 1
    return dict(short_far_leg_partial_intruders=intruders,
                shared_consumer_partial_continuations=shared,
                complete_family_counterexample=False)


def controls():
    return dict(status='PASS', pair_geometry=pair_controls(), source_catalogue=rotor_shapes(),
                actual_demand_frames=actual_chain_controls(), residual_opening=opening_controls(),
                scope='Finite independent endpoint/support/matching controls of a separate '
                      'general four-row proof. Partial marked chains and opening intruders are '
                      'not complete-family witnesses. Joint demand injection is proved in writing; '
                      'no finite search replaces it or proves the full allocation/grid target.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
