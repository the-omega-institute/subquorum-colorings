"""Exact all-width/far-leg controls for the left north-terminal pair branch."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import endpoint_tiles, phi, sources


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def controls():
    cases = accepted = band_zero = tip_zero = escaped = consumer_cases = consumer_sets = 0
    for bottom, width in itertools.product((-24, 40), (12, 20, 50)):
        origin = bottom-9
        for gap, far in ((8, 4), (8, 6), (8, 14), (10, 16), (10, 40), (10, 200)):
            records = sources(bottom, width)+[
                returning(bottom, width, 0),
                continuation(bottom, width, width+gap, 8, far, False)]
            endpoints = set.union(*(record[0] for record in records))
            for breadth, height in itertools.product(
                    (6, 8, 10, width+10, width+12, width+14, width+16, width+50),
                    (4, 6, 8, 10, 12, 14, 16, 50)):
                column = width+15-breadth
                for other in sorted({4, 6, height-10, height-8, height+6, height+8, height+10, 200}):
                    if other < 4:
                        continue
                    current = independent_source((breadth, height, other),
                                                 (False, False, True),
                                                 (origin+1-height, width+15))
                    band = breadth <= width+gap+2
                    tip = gap == 8 and column == 3
                    expected = (height >= 12 and other <= height-8 if band else
                                height >= 10 and other <= height+8 if tip else height >= 10)
                    assert bool(current[0] & endpoints) != expected
                    cases += 1
                    if not expected:
                        continue
                    zero = (band and other == height-8) or (tip and other == height+8)
                    assert {(origin, width+14), (origin+1, width+14)} <= current[0]
                    half_legs = (height+other)//2
                    tiles = endpoint_tiles(current)
                    inside = {point for point in current[1]
                              if (point[0]//2, point[1]//2) in tiles}
                    assert len(current[2]) == breadth+half_legs-1
                    assert len(tiles) == breadth//2+half_legs+1
                    assert len(inside) == half_legs+4 and charge(current) == 1
                    before, after, signature = tile_signature(records, current)
                    expected_signature = {(origin+1, width+14): (0, 0)}
                    events = set()
                    if zero and band:
                        expected_signature[origin-7, column-1] = (0, 1)
                        events.add((7, (origin-6, column), (origin-7, column)))
                        band_zero += 1
                    elif zero:
                        expected_signature[origin+9, 2] = (0, 1)
                        events.add((0, (origin+10, 3), (origin+9, 3)))
                        tip_zero += 1
                    assert signature == expected_signature
                    assert after['events']-before['events'] == events
                    assert before['full'] == after['full'] and before['mass'] == after['mass']
                    assert phi(records+[current])-phi(records) == 1-int(zero)
                    assert phi(records+[current])-phi(records[:2]+records[5:6]) == -int(zero)
                    accepted += 1
                    escaped += int(column <= 1)
                    if not (zero and bottom == 40 and width in (12, 20)
                            and (gap, far) in ((8, 4), (10, 16))):
                        continue
                    combined = records+[current]
                    blocked = endpoints | current[0]
                    depths = sorted({4, 8, 10, 12, 14, height-2, height, height+2})
                    for span, depth, leg in itertools.product(
                            sorted({6, 8, max(6, breadth-4), breadth-2, breadth}), depths, (4, 14)):
                        if span < 6 or depth < 4:
                            continue
                        consumer = independent_source((span, depth, leg), (False, False, True),
                                                      (origin+2-depth, width+13))
                        disjoint = not consumer[0] & blocked
                        allowed = span <= breadth-4 and 14 <= depth <= height-2 and leg <= depth-10
                        assert disjoint == allowed
                        consumer_cases += 1
                        if not allowed:
                            continue
                        previous, following, shared = tile_signature(combined, consumer)
                        assert shared == {(origin-1, width+12): (0, 1),
                                          (origin+1, width+12): (1, 2)}
                        assert following['events']-previous['events'] == {
                            (4, (origin, width+13), (origin, width+12)),
                            (4, (origin+2, width+13), (origin+2, width+12)),
                            (9, (origin+1, width+12), (origin+1, width+13))}
                        assert charge(consumer) == 1-span
                        assert following['mass']-previous['mass'] == span-1
                        assert phi(combined+[consumer])-phi(combined) == span-2 >= 4
                        consumer_sets += 1
    return dict(all_left_north_caps_disjointness_controls=cases,
                accepted_exact_original_charge_tile_event_sets=accepted,
                zero_band_controls=band_zero, zero_Q_tip_controls=tip_zero,
                escaped_far_columns_at_most_one_controls=escaped,
                both_zero_types_consumer_disjointness_controls=consumer_cases,
                surviving_consumer_exact_event_sets=consumer_sets,
                complete_extension_existence_claimed=False,
                full_north_terminal_U_branch_local_compensation=True,
                unrestricted_allocation_or_grid_equality=False)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', controls=controls(),
                         scope='Finite corroboration of the all-parameter written classification. '
                         'One common original-owner ledger; no arbitrary exterior sign claim.'), indent=2))
