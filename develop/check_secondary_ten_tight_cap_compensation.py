"""Exact two-sided continuation controls for the general internal tight cap."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import endpoint_tiles, phi, sources


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def controls():
    cases = survivors = 0
    for width, gap, far, cap_index, height in itertools.product(
            (12, 20), (8, 10), (4, 16), range(6), (12, 14, 16, 20, 50)):
        if (gap == 8 and far > 14) or (gap == 10 and far < 16):
            continue
        bottom = 40
        origin = bottom-9
        cap_breadth = (6, 8, 10, 12, width+8, width+10)[cap_index]
        records = sources(bottom, width)+[
            returning(bottom, width, 0),
            continuation(bottom, width, width+gap, 8, far, False)]
        cap = independent_source((cap_breadth, height, height-8),
                                 (False, False, True), (origin+1-height, width+15))
        assert all(not cap[0] & record[0] for record in records)
        assert charge(cap) == 1 and phi(records+[cap]) == phi(records)
        records += [cap]
        occupied = set.union(*(record[0] for record in records))
        for breadth, depth, other in itertools.product(
                (6, 8, 12, 20, 32), (4, 6, 8, 10, 12, 14, 16, 18, 20, 48, 50, 52),
                (4, 6, 10, 20)):
            current = independent_source((breadth, depth, other), (False, False, True),
                                         (origin+2-depth, width+13))
            disjoint = not current[0] & occupied
            expected = breadth <= cap_breadth-4 and 14 <= depth <= height-2 and other <= depth-10
            assert disjoint == expected
            cases += 1
            if not disjoint:
                continue
            half_legs = (depth+other)//2
            tiles = endpoint_tiles(current)
            inside = {point for point in current[1]
                      if (point[0]//2, point[1]//2) in tiles}
            expected_inside = {(origin+2-depth, width+13),
                               (origin+2-depth, width+12-breadth)}
            expected_inside |= {(origin+2-depth+row, width+13)
                                for row in range(2, depth+1, 2)}
            expected_inside |= {(origin+2-depth+row, width+12-breadth)
                                for row in range(2, other+1, 2)}
            assert inside == expected_inside
            assert len(current[2]) == breadth+half_legs-1
            assert len(tiles) == breadth+half_legs and len(inside) == half_legs+2
            assert charge(current) == 1-breadth
            before, after, signature = tile_signature(records, current)
            assert signature == {(origin-1, width+12): (0, 1),
                                 (origin+1, width+12): (1, 2)}
            assert after['events']-before['events'] == {
                (4, (origin, width+13), (origin, width+12)),
                (4, (origin+2, width+13), (origin+2, width+12)),
                (9, (origin+1, width+12), (origin+1, width+13))}
            assert after['full']-before['full'] == {((origin+1)//2, (width+12)//2)}
            assert after['mass']-before['mass'] == breadth-1
            assert phi(records+[current])-phi(records) == breadth-2 >= 4
            assert phi(records+[current])-phi(records[:2]+records[5:6]) == breadth-3 >= 3
            survivors += 1
    return dict(two_sided_exact_disjointness_controls=cases,
                surviving_exact_source_support_tile_event_sets=survivors,
                formula='h<=s-4;14<=d<=ell-2;f<=d-10;DeltaPhi=h-2',
                both_residual_families=True,
                independent_review_of_this_wider_supplement=False,
                unrestricted_result=False)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', controls=controls(),
                         scope='Finite corroboration of the general interval and directed-event '
                         'proof. Partial joint inventories, not arbitrary exterior contributions.'), indent=2))
