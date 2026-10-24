"""Exact controls for an all-width positive-owner negative marginal band."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import endpoint_tiles, phi, sources


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def controls():
    count = 0
    for bottom, width in itertools.product((-24, 40), (12, 14, 20, 50, 200)):
        origin = bottom-9
        for gap, far in ((8, 4), (8, 6), (8, 14), (10, 16), (10, 40), (10, 200)):
            base = sources(bottom, width)+[
                returning(bottom, width, 0),
                continuation(bottom, width, width+gap, 8, far, False)]
            baseline = phi(base[:2]+base[5:6])
            assert phi(base)-baseline == -1
            for incident in (12, 14, 50):
                previous = independent_source(
                    (6, incident, incident-8), (False, False, True),
                    (origin+1-incident, width+15))
                records = base+[previous]
                assert phi(records) == phi(base)
                current = independent_source((6, 4, width+4), (True, False, False),
                                             (origin-13, 4))
                assert all(not first[0] & second[0]
                           for first, second in itertools.combinations(records+[current], 2))
                pending = origin-7, width+8
                assert pending in previous[1] and pending in current[0]
                endpoints = set.union(*(record[0] for record in records))
                assert pending not in endpoints
                assert set(neighbors(pending)) & endpoints == {
                    (origin-7, width+9), (origin-6, width+8)}
                tiles = endpoint_tiles(current)
                inside = {point for point in current[1]
                          if (point[0]//2, point[1]//2) in tiles}
                assert len(current[2]) == width//2+9
                assert len(tiles) == len(inside) == width//2+8
                assert charge(current) == 1
                before, after, signature = tile_signature(records, current)
                central_columns = range(4, width+8, 2)
                expected = {(origin-7, column): (1, 3) for column in central_columns}
                expected[origin-7, width+8] = (1, 1)
                assert signature == expected
                expected_events = set()
                for column in central_columns:
                    for target_column in (column, column+1):
                        expected_events.add((7, (origin-6, target_column),
                                             (origin-7, target_column)))
                    expected_events.add((9, (origin-7, column+1), (origin-6, column+1)))
                expected_events.add((7, (origin-6, width+8), (origin-7, width+8)))
                assert after['events']-before['events'] == expected_events
                assert after['full']-before['full'] == {
                    (row//2, column//2) for row, column in expected}
                assert after['mass'] == before['mass']
                assert len(after['full'])-len(before['full']) == width//2+3
                assert len(after['events'])-len(before['events']) == 3*width//2+7
                assert phi(records+[current])-phi(records) == -width//2
                assert phi(records+[current]) == width//2+8 > 0
                assert phi(records+[current])-baseline == -width//2-1
                remaining = origin+9, 6
                final_endpoints = endpoints | current[0]
                final_supports = set.union(*(record[1] for record in records+[current]))
                assert remaining in final_supports-final_endpoints
                assert {(origin+8, 6), (origin+10, 6)} <= final_endpoints
                count += 1
    return dict(exact_source_tile_event_and_incompleteness_controls=count,
                widths=[12, 14, 20, 50, 200],
                both_residual_families=True,
                unbounded_statement_proved_in_written_note=True,
                complete_extension_or_global_counterexample=False,
                new_Lean_or_independent_review=False)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', controls=controls(),
                         scope='Finite corroboration of the general interval/tile proof. '
                         'Each original owner and each directed event is counted once. '
                         'The prescribed inventory remains incomplete.'), indent=2))
