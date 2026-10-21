"""Exact source controls for the general width-six/eight cap noncompletion."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import phi, sources


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def controls():
    library, rotors = axial_library({(-1, 0)})
    assert len(rotors) == 2
    assert all((-2, 1) in record[0] for record in rotors)
    caps = collision_witnesses = rotor_collisions = catalogue_roles = 0
    for bottom, width in itertools.product((-24, 40), (12, 20, 200)):
        origin = bottom-9
        point = origin+2, width+12
        for gap, far in ((8, 4), (8, 6), (8, 14), (10, 16), (10, 40), (10, 200)):
            records = sources(bottom, width)+[
                returning(bottom, width, 0),
                continuation(bottom, width, width+gap, 8, far, False)]
            for cap_breadth, height in itertools.product((6, 8), (12, 14, 50)):
                current = independent_source(
                    (cap_breadth, height, height-8), (False, False, True),
                    (origin+1-height, width+15))
                assert all(not current[0] & record[0] for record in records)
                assert charge(current) == 1
                before, after, signature = tile_signature(records, current)
                assert signature == {
                    (origin-7, width+14-cap_breadth): (0, 1),
                    (origin+1, width+14): (0, 0)}
                assert after['mass'] == before['mass']
                assert after['full'] == before['full']
                assert phi(records+[current]) == phi(records)
                assert after['events']-before['events'] == {
                    (7, (origin-6, width+15-cap_breadth),
                     (origin-7, width+15-cap_breadth))}
                occupied = set.union(*(record[0] for record in records+[current]))
                assert point in records[7][1] and point not in occupied
                assert set(neighbors(point)) & occupied == {
                    (origin+2, width+11), (origin+2, width+13),
                    (origin+3, width+12)}
                for relative in rotors:
                    consumer = shift(relative, point)
                    witness = origin, width+13
                    assert witness in consumer[0] & records[4][0]
                    rotor_collisions += 1
                depths = sorted({4, 6, 8, 10, 12, height-2, height, height+2, height+50})
                for breadth, depth, other, right in itertools.product(
                        (6, 8, 20, width+10), depths, (4, 12, 50), (False, True)):
                    consumer = independent_source(
                        (breadth, depth, other), (False, False, not right),
                        (origin+2-depth, width+11 if right else width+13))
                    assert point in consumer[0]
                    assert set(neighbors(point)) & consumer[0] == {(point[0]-1, point[1])}
                    if depth >= height:
                        witness = origin+2-height, width+12
                        blocker = current
                    elif right:
                        witness = origin+3-depth, width+14
                        blocker = current
                    elif depth <= 8:
                        witness = origin+3-depth, width+11
                        blocker = records[7]
                    else:
                        witness = origin+3-depth, width+15-cap_breadth
                        blocker = current
                    assert witness in consumer[0] & blocker[0]
                    collision_witnesses += 1
                if bottom == 40 and width == 12 and gap == 8 and far == 4:
                    for relative in library:
                        consumer = shift(relative, point)
                        assert consumer[0] & occupied
                        catalogue_roles += 1
                caps += 1
    return dict(exact_positive_zero_increment_cap_controls=caps,
                explicit_all_parameter_collision_witness_controls=collision_witnesses,
                north_rotor_cavity_collision_controls=rotor_collisions,
                bounded_full_north_U_catalogue_controls=catalogue_roles,
                catalogue_dimensions_at_most=18,
                cap_breadths=[6, 8], both_residual_families=True,
                complete_family_exclusion_proved_in_written_note=True,
                unrestricted_allocation_or_grid_equality=False)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', controls=controls(),
                         scope='Finite source-set and catalogue corroboration of the general '
                         'collision proof. No finite catalogue is used to prove all sizes. '
                         'Lean geometry has separate execution evidence.'), indent=2))
