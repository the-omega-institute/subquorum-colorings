"""Original-owner set controls for forced return closure and signed repair."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_north_third_left_return import endpoint_tiles, phi, sources
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def returning(bottom, width, stage):
    return independent_source((width+6+2*stage, 6+2*stage, 4),
                              (False, False, True),
                              (bottom-13-2*stage, width+11+stage))


def continuation(bottom, width, breadth, incident, far, right):
    return independent_source((breadth, incident, far), (False, False, not right),
                              (bottom-7-incident, width+10 if right else width+12))


def tile_signature(base, current):
    before = inventory(base)
    after = inventory(base+[current])
    shared = endpoint_tiles(current) & set.union(*(endpoint_tiles(record) for record in base))
    added_events = after['events']-before['events']
    assert before['events'] <= after['events']
    assert before['full'] <= after['full']
    assert {tile for tile in shared if tile in after['full']} == after['full']-before['full']
    result = {}
    for tile in shared:
        events = {event for event in added_events
                  if (event[1][0]//2, event[1][1]//2) == tile}
        result[(2*tile[0], 2*tile[1])] = (int(tile in after['full']), len(events))
        for owner, endpoint, target in events:
            assert target not in (base+[current])[owner][1]
            assert (owner == len(base)) != (target in current[0])
    assert sum(value[0] for value in result.values()) == len(after['full'])-len(before['full'])
    assert sum(value[1] for value in result.values()) == len(added_events)
    return before, after, result


def branching_controls():
    library, rotors = axial_library({(-1, 0), (0, 1)})
    roles = excluded_rotors = 0
    for bottom, width in itertools.product((-24, 40), (12, 20)):
        base = sources(bottom, width)+[returning(bottom, width, 0)]
        blocked = set.union(*(record[0] for record in base))
        point = bottom-7, width+11
        assert point not in blocked and point in base[-1][1]
        assert set(neighbors(point)) & blocked == {(point[0], point[1]-1),
                                                  (point[0]+1, point[1])}
        for relative in library:
            current = shift(relative, point)
            if current[0] & blocked:
                continue
            assert set(neighbors(point)) & current[0] == {(point[0]-1, point[1])}
            incident = point[0]-min(row for row, column in current[0])
            low = min(column for row, column in current[0])
            high = max(column for row, column in current[0])
            right = low == point[1]
            assert right or high == point[1]
            breadth = high-low+1
            far_column = high if right else low
            far = max(row for row, column in current[0] if column == far_column)-(point[0]-incident)
            assert current == continuation(bottom, width, breadth, incident, far, right)
            roles += 1
        for relative in rotors:
            assert shift(relative, point)[0] & blocked
            excluded_rotors += 1
    return dict(bounded_surviving_U_roles=roles, rotor_exclusions=excluded_rotors,
                catalogue_dimensions_bounded_by=18,
                wide_left_escapes_tested_separately=True)


def repair_controls():
    right_count = interior_count = collision_count = 0
    for bottom, width in itertools.product((-24, 40), (12, 20, 50)):
        origin = bottom-9
        base = sources(bottom, width)+[returning(bottom, width, 0)]
        blocked = set.union(*(record[0] for record in base))
        for breadth, incident, far in itertools.product((6, 8, 20, 50), (4, 6, 8, 20), (4, 12, 50)):
            current = continuation(bottom, width, breadth, incident, far, True)
            assert not current[0] & blocked
            before, after, signature = tile_signature(base, current)
            expected = {(origin-3, width+10): (1, 2),
                        (origin-1, width+10): (1, 2),
                        (origin+1, width+10): (1, 2)}
            if incident == 4:
                expected[origin-3, width+10] = (0, 0)
                expected[origin-1, width+12] = (0, 1)
            else:
                expected[origin-5, width+10] = (0, 0)
            assert signature == expected
            assert charge(current) == 1-breadth
            assert after['raw_reserve']-before['raw_reserve'] == breadth-1-int(incident == 4)
            right_count += 1
        for breadth, incident, far in itertools.product(range(6, width+8, 2), (4, 6, 8, 10, 12, 20), (4, 6, 12)):
            current = continuation(bottom, width, breadth, incident, far, False)
            assert bool(current[0] & blocked) == (far > incident-8)
            if far > incident-8:
                collision_count += 1
                continue
            before, after, signature = tile_signature(base, current)
            expected = {(origin-5, width+10): (0, 1),
                        (origin-3, width+10): (1, 2),
                        (origin-1, width+10): (1, 2),
                        (origin+1, width+10): (1, 2)}
            assert signature == expected
            assert charge(current) == 1-breadth
            assert after['raw_reserve']-before['raw_reserve'] == breadth-2
            interior_count += 1
    return dict(right_all_parameter_controls=right_count,
                interior_left_controls=interior_count, interior_left_collisions=collision_count)


def nested_controls():
    count = 0
    for bottom, width in itertools.product((-24, 40, 100), (12, 14, 20, 50, 200)):
        origin = bottom-9
        base = sources(bottom, width)
        baseline_phi = phi(base[:2]+base[5:])
        for stage in range(3):
            current = returning(bottom, width, stage)
            assert all(not current[0] & record[0] for record in base)
            before, after, signature = tile_signature(base, current)
            assert charge(current) == -width-5-2*stage
            if stage == 0:
                expected = {(origin-3, column): (1, 4) for column in range(6, width+9, 2)}
            elif stage == 1:
                expected = {(origin-5, column): (1, 4) for column in range(6, width+9, 2)}
                expected.update({(origin-5, 4): (1, 3), (origin-5, width+10): (1, 3),
                                 (origin-3, 4): (1, 2), (origin-3, width+10): (1, 2),
                                 (origin-1, width+10): (1, 2), (origin+1, width+10): (1, 2)})
            else:
                expected = {(origin-7, column): (1, 4) for column in range(4, width+11, 2)}
                expected.update({(origin-1, width+12): (0, 1), (origin+1, width+12): (1, 2)})
            assert signature == expected
            assert after['mass']-before['mass'] == width+5+2*stage
            assert after['raw_reserve']-before['raw_reserve'] == (1 if stage < 2 else 0)
            if stage:
                forced = origin+2, width+10+stage
                occupied = set.union(*(record[0] for record in base))
                assert forced in base[-1][1] and forced not in occupied and forced in current[0]
                assert (forced[0], forced[1]-1) in base[-1][0]
                assert (forced[0]+1, forced[1]) in base[4][0]
            base.append(current)
            count += 1
        assert phi(base)-baseline_phi == -1
        occupied = set.union(*(record[0] for record in base))
        next_pattern = returning(bottom, width, 3)
        assert (origin+2, width+13) in next_pattern[0] & base[4][0]
        assert (origin+2, width+13) in base[-1][1]
        pending = origin-1, width+13
        assert pending in base[4][1] and pending not in occupied
        assert (pending[0], pending[1]-1) in base[-1][0]
        assert (pending[0]+1, pending[1]) in base[4][0]
        for stage in range(3):
            support = origin+1-2*stage, 5-stage
            assert support in base[6+stage][1] and support not in occupied
            assert (support[0]-1, support[1]) in base[6+stage][0]
            assert (support[0], support[1]+1) in base[1 if stage == 0 else 5+stage][0]
    return dict(exact_shared_tile_and_event_controls=count,
                translations=3, widths=[12, 14, 20, 50, 200],
                successive_increment=[1, 1, 0], remaining_package_difference=-1,
                forced_supports_still_missing=4, complete_realization_asserted=False)


def double_site_rotor_controls():
    count = 0
    for bottom, width in itertools.product((-24, 40, 100), (12, 14, 20, 50, 200)):
        origin = bottom-9
        base = sources(bottom, width)+[returning(bottom, width, stage) for stage in range(3)]
        module = transform_module(rotor(), (False, True, False), (origin+2, width+12))
        current = module['endpoints'], module['selected'], {tuple(sorted(edge)) for edge in module['matching']}
        assert all(not current[0] & record[0] for record in base)
        first_site = origin-1, width+13
        second_site = origin+1, width+14
        assert first_site in base[4][1] & current[0]
        assert second_site in base[3][1] & current[0]
        assert charge(current) == -2
        tiles = endpoint_tiles(current)
        assert len(tiles) == 5 and len(current[2]) == 4
        inside = {point for point in current[1] if (point[0]//2, point[1]//2) in tiles}
        assert inside == {(origin-3, width+15), (origin-1, width+12),
                          (origin, width+17), (origin+2, width+14)}
        before, after, signature = tile_signature(base, current)
        assert signature == {(origin-1, width+12): (1, 2), (origin+1, width+14): (0, 0)}
        expected_events = {(8, (origin-1, width+12), first_site),
                           (9, first_site, (origin, width+13))}
        assert after['events']-before['events'] == expected_events
        assert after['mass']-before['mass'] == 2
        assert after['raw_reserve']-before['raw_reserve'] == 2
        assert phi(base+[current])-phi(base[:2]+base[5:6]) == 1
        pending = origin-2, width+13
        occupied = set.union(*(record[0] for record in base+[current]))
        assert pending in current[1] and pending not in occupied
        assert (pending[0], pending[1]-1) in base[8][0]
        assert (pending[0]+1, pending[1]) in current[0]
        count += 1
    return dict(exact_rotor_shared_tile_and_event_set_controls=count,
                original_charge=-2, two_sites_one_owner=True, exact_increment=2,
                complete_model_or_unique_consumer_claim=False,
                outside_initial_review_input=True)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', branching=branching_controls(),
                         repairs=repair_controls(), nested=nested_controls(),
                         double_site_rotor=double_site_rotor_controls(),
                         scope='Finite corroboration of written general original-owner '
                         'catalogue and tile proofs; not complete feasibility, new Lean '
                         'verification, or unrestricted global allocation.'), indent=2))
