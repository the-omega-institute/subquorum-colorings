"""Exact original-source controls for a shared persistent-pair compensation."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import endpoint_tiles, phi, sources
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def rotor_record(origin, width):
    module = transform_module(rotor(), (False, True, False), (origin+2, width+12))
    return module['endpoints'], module['selected'], {tuple(sorted(edge)) for edge in module['matching']}


def controls():
    U_count = rotor_count = order_count = positive_obstacles = 0
    for bottom, width in itertools.product((-24, 40), (12, 20, 50)):
        origin = bottom-9
        base = sources(bottom, width)+[returning(bottom, width, 0)]
        for gap, far in ((8, 4), (8, 6), (8, 14), (10, 16), (10, 40), (10, 200)):
            records = base+[continuation(bottom, width, width+gap, 8, far, False)]
            assert phi(records)-phi(records[:2]+records[5:6]) == -1
            pair = {(origin, width+14), (origin+1, width+14)}
            for breadth, incident, other in itertools.product((6, 8, 20), (4, 6, 20), (4, 12, 50)):
                current = independent_source((breadth, incident, other), (False, False, False),
                                             (origin+1-incident, width+13))
                assert pair <= current[0]
                assert all(not current[0] & record[0] for record in records)
                tiles = endpoint_tiles(current)
                inside = {point for point in current[1] if (point[0]//2, point[1]//2) in tiles}
                half_legs = (incident+other)//2
                assert len(current[2]) == breadth+half_legs-1
                assert len(tiles) == breadth//2+half_legs
                assert len(inside) == half_legs
                assert charge(current) == -1
                before, after, signature = tile_signature(records, current)
                assert signature == {(origin+1, width+14): (0, 0)}
                assert after['full'] == before['full']
                assert after['events'] == before['events']
                assert after['mass']-before['mass'] == 1
                assert phi(records+[current]) == phi(records[:2]+records[5:6])
                U_count += 1
            current = rotor_record(origin, width)
            assert pair <= current[0]
            assert all(not current[0] & record[0] for record in records)
            before, after, signature = tile_signature(records, current)
            assert signature == {(origin-1, width+12): (0, 1), (origin+1, width+14): (0, 0)}
            assert after['events']-before['events'] == {(8, (origin-1, width+13), (origin, width+13))}
            assert after['mass']-before['mass'] == 2
            assert phi(records+[current]) == phi(records[:2]+records[5:6])
            rotor_count += 1
            for incident in (12, 14, 50):
                current = independent_source((6, incident, incident-8), (False, False, True),
                                             (origin+1-incident, width+15))
                assert pair <= current[0]
                assert all(not current[0] & record[0] for record in records)
                tiles = endpoint_tiles(current)
                inside = {point for point in current[1] if (point[0]//2, point[1]//2) in tiles}
                assert len(current[2]) == incident+1
                assert len(tiles) == incident and len(inside) == incident
                assert charge(current) == 1
                before, after, signature = tile_signature(records, current)
                assert signature == {(origin-7, width+8): (0, 1), (origin+1, width+14): (0, 0)}
                assert after['events']-before['events'] == {(7, (origin-6, width+9), (origin-7, width+9))}
                assert after['mass'] == before['mass'] and after['full'] == before['full']
                assert phi(records+[current]) == phi(records)
                pending = origin-7, width+8
                assert pending in current[1]
                assert pending not in set.union(*(record[0] for record in records+[current]))
                assert (pending[0], pending[1]+1) in current[0]
                assert (pending[0]+1, pending[1]) in records[7][0]
                positive_obstacles += 1
        records = base+[returning(bottom, width, 1)]
        next_return = returning(bottom, width, 2)
        current = rotor_record(origin, width)
        base_value = phi(records)
        assert phi(records+[next_return])-base_value == 0
        assert phi(records+[current])-base_value == 1
        assert phi(records+[next_return, current])-phi(records+[next_return]) == 2
        assert phi(records+[current, next_return])-phi(records+[current]) == 1
        assert phi(records+[current, next_return]) == phi(records+[next_return, current])
        before, after_return, _ = tile_signature(records, next_return)
        _, after_rotor, _ = tile_signature(records, current)
        _, after_both, _ = tile_signature(records+[next_return], current)
        assert charge(next_return) == -width-9
        assert len(after_return['full'])-len(before['full']) == width//2+5
        assert len(after_return['events'])-len(before['events']) == 2*width+19
        normalized_rotor_events = {(9 if owner == 8 else owner, endpoint, target)
                                   for owner, endpoint, target in after_rotor['events']}
        assert after_both['events']-(after_return['events'] | normalized_rotor_events) == {
            (8, (origin-1, width+12), (origin-1, width+13))}
        assert after_both['full']-(after_return['full'] | after_rotor['full']) == {
            ((origin-1)//2, (width+12)//2)}
        order_count += 1
    return dict(U_source_phase_and_exact_set_controls=U_count,
                rotor_exact_set_controls=rotor_count,
                joint_insertion_order_controls=order_count,
                joint_full_tile_and_cross_event_identity_controls=order_count,
                positive_joint_consumer_zero_increment_controls=positive_obstacles,
                residual_families_both_covered=True,
                complete_or_unrestricted_result=False)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', controls=controls(),
                         scope='Finite corroboration of separately written general conditional '
                         'compensation. One original consumer serves both persistent supports, '
                         'one exact reserve receipt. No complete-consumer classification, '
                         'new Lean validation or global grid theorem.'), indent=2))
