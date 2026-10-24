"""Independent finite controls of the maximal width-ten permanent pair proof."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_pair_transfer_protected_defects import original
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def aligned_move(point, symmetry):
    transpose, flip_row, flip_column = symmetry
    row, column = point
    row = 1-row if flip_row else row
    column = 1-column if flip_column else column
    return (column, row) if transpose else (row, column)


def controls():
    fixed_cases = absent_cross = enclosed = images = old_frames = strip_pairs = 0
    negative_q = 0
    for leg, height, near, far_b, width_c, far_c in itertools.product(
            (8, 10, 16, 24), (8, 12, 20), (4, 6, 12), (4, 6, 12),
            (6, 8, 10, 16, 24, 26), (4, 6, 12, 20)):
        if near > height-4:
            continue
        base = independent_source((10, leg, far_b), (False, True, False), (leg+3, 1))
        cross = independent_source((width_c, height, far_c),
                                   (True, True, False), (1, height+2))
        corner = independent_source((leg-2, near, 4), (True, False, False), (2, 3))
        records = [base, cross, corner]
        endpoints = set().union(*(record[0] for record in records))
        if len(endpoints) != sum(len(record[0]) for record in records):
            continue
        point = (leg+1, 3)
        assert point not in endpoints and point in corner[1]
        assert {(leg, 3), (leg+1, 2), (leg+2, 3)} <= endpoints
        assert (2, 9) in cross[0]
        absent_cross += int(width_c == leg)
        fixed_cases += 1
        for new_width in range(6, leg, 2):
            specification = ((new_width, 6, 4), (True, True, True), (leg+2, 9))
            consumer = independent_source(*specification)
            if consumer[0] & endpoints:
                continue
            assert original(*specification)['charge'] == -1
            negative_q += 1
            first_row = leg+2-new_width
            boundary = {(row, column) for row in range(first_row, leg+2)
                        for column in range(4, 9)
                        if row in (first_row, leg+1) or column in (4, 8)}
            inside = {(row, column) for row in range(first_row+1, leg+1)
                      for column in range(5, 8)}
            fixed = corner[0] | consumer[0]
            assert boundary <= fixed and not inside & consumer[0]
            assert inside & corner[0] == {(leg, column) for column in range(5, 8)}
            pair = {(leg-2, 4), (leg-1, 4)}
            missing = {(leg-2, 5), (leg-1, 5)}
            tile = pair | missing
            assert tile & endpoints == pair and not tile & consumer[0]
            assert missing <= inside and not missing & corner[1]
            assert not tile & corner[1]
            assert {(row, 4) for row, _ in missing} <= corner[0]
            old_corner = independent_source((leg-2, 4, near),
                                            (False, False, False), (3, 2))
            old_return = independent_source((new_width, 6, 4),
                                            (False, True, False), (9, 1))
            move = lambda vertex: (leg+3-vertex[1], vertex[0])
            for old_record, actual in ((old_corner, corner), (old_return, consumer)):
                assert {move(vertex) for vertex in old_record[0]} == actual[0]
                assert {move(vertex) for vertex in old_record[1]} == actual[1]
                assert {tuple(sorted((move(first), move(second))))
                        for first, second in old_record[2]} == actual[2]
            for index in range(new_width//2-2):
                strip_tile = {(leg-2-2*index+shift, column)
                              for shift in (0, 1) for column in (4, 5)}
                strip_endpoints = {vertex for vertex in strip_tile if vertex[1] == 4}
                strip_missing = strip_tile-strip_endpoints
                assert strip_tile & (endpoints | consumer[0]) == strip_endpoints
                assert strip_missing <= inside and not strip_missing & corner[1]
                strip_pairs += 1
            for symmetry in itertools.product((False, True), repeat=3):
                moved = {aligned_move(vertex, symmetry) for vertex in tile}
                assert len({(row//2, column//2) for row, column in moved}) == 1
                images += 1
            enclosed += 1
        for old_height in range(4, 30, 2):
            witness = (leg+1-old_height, 3)
            assert witness not in base[0]
            old_cross = independent_source((6, old_height, 4),
                (False, False, False), (leg+1-old_height, 1))
            assert witness in old_cross[0] and (leg+1, 2) in old_cross[0] & base[0]
            old_frames += 1

    roles = rotor_cases = 0
    for leg in (8, 12, 20):
        base = independent_source((10, leg, 4), (False, True, False), (leg+3, 1))
        corner = independent_source((leg-2, 4, 4), (True, False, False), (2, 3))
        cross = independent_source((leg+4, 12, 4), (True, True, False), (1, 14))
        fixed = base[0] | corner[0] | cross[0]
        assert len(fixed) == sum(len(record[0]) for record in (base, corner, cross))
        for width, incident, far, upward in itertools.product(
                range(6, leg+6, 2), range(4, 18, 2), range(4, 16, 2), (False, True)):
            offset = (leg+2, incident+3) if upward else (leg, incident+3)
            record = independent_source((width, incident, far), (True, True, upward), offset)
            if not record[0] & fixed:
                assert upward and incident == 6 and width <= leg-2 and far == 4
            roles += 1
        point = (leg+1, 3)
        for symmetry in itertools.product((False, True), repeat=3):
            module = transform_module(rotor(), symmetry)
            for anchor in module['endpoints']:
                if set(neighbors(anchor)) & module['endpoints'] != {(anchor[0], anchor[1]+1)}:
                    continue
                moved = {(row+point[0]-anchor[0], column+point[1]-anchor[1])
                         for row, column in module['endpoints']}
                assert moved & fixed
                rotor_cases += 1

    extents = 0
    dimensions = list(itertools.product((6, 10, 18), (4, 8, 16), (4, 8, 16)))
    for parameters in dimensions+['rotor']:
        for symmetry in itertools.product((False, True), repeat=3):
            if parameters == 'rotor':
                endpoints = transform_module(rotor(), symmetry)['endpoints']
            else:
                endpoints = independent_source(parameters, symmetry, (0, 0))[0]
            reachable = {next(iter(endpoints))}
            pending = list(reachable)
            while pending:
                for point in set(neighbors(pending.pop())) & endpoints-reachable:
                    reachable.add(point)
                    pending.append(point)
            assert reachable == endpoints
            assert all(max(point[axis] for point in endpoints)-
                       min(point[axis] for point in endpoints) >= 3 for axis in (0, 1))
            extents += 1
    assert absent_cross > 0 and enclosed > 0
    return dict(status='PASS', endpoint_disjoint_BCX=fixed_cases, cross_width_equals_b=absent_cross,
                enclosed_partial_geometries=enclosed, negative_Q_profiles=negative_q,
                aligned_tile_images=images, old_H_frame_owner_exclusions=old_frames,
                existing_lower_strip_pairs=strip_pairs,
                independent_terminal_dimensions=roles, rotor_anchored_cases=rotor_cases,
                source_connectivity_extent_controls=extents,
                scope='Finite independent geometry/profile controls of a written arbitrary-dimension proof. '
                      'No complete Vcorner realization or finite-enumeration exhaustion claimed.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
