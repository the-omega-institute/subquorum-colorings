"""Independent original-source controls for third-left repair and return."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_north_gap_four_package import consumer, fixed_sources


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def sources(bottom, width):
    origin = bottom-9
    return fixed_sources(bottom, width, 4, 6)+[
        consumer(bottom, width, 8, 6, 4, True),
        independent_source((6, 4, 4), (False, True, False), (origin+4, width+7)),
        independent_source((6, 4, 4), (True, False, False), (origin+1, width+1))]


def candidate(bottom, width, breadth, incident, far):
    return independent_source((breadth, incident, far), (False, False, True),
                              (bottom-7-incident, width+11))


def endpoint_tiles(record):
    return {(row//2, column//2) for row, column in record[0]}


def phi(records):
    return inventory(records)['raw_reserve']+sum(charge(record)>0 for record in records)


def interior_controls():
    accepted = rejected = 0
    for bottom, width in itertools.product((-24, 40), (12, 14, 20, 50)):
        records = sources(bottom, width)
        occupied = set.union(*(record[0] for record in records))
        tiles = set.union(*(endpoint_tiles(record) for record in records))
        before = inventory(records)
        for breadth, incident, far in itertools.product(
                range(6, width+6, 2), (4, 6, 10, 12, 20), (4, 6, 10, 18)):
            current = candidate(bottom, width, breadth, incident, far)
            disjoint = not current[0] & occupied
            assert disjoint == (far <= incident-6)
            if not disjoint:
                rejected += 1
                continue
            assert not endpoint_tiles(current) & tiles
            assert charge(current) == 1-breadth
            after = inventory(records+[current])
            assert after['mass']-before['mass'] == breadth-1
            assert after['full'] == before['full']
            assert after['events'] == before['events']
            assert after['raw_reserve']-before['raw_reserve'] == breadth-1
            accepted += 1
    return dict(endpoint_disjoint_cases=accepted, collision_cases=rejected,
                exact_disjointness_criterion='z<=ell-6', exact_increment='k-1')


def return_controls():
    count = 0
    witness = None
    for bottom, width in itertools.product((-24, 40, 100), (12, 14, 20, 50, 200)):
        origin = bottom-9
        records = sources(bottom, width)
        current = candidate(bottom, width, width+6, 6, 4)
        assert all(not first[0] & second[0]
                   for first, second in itertools.combinations(records+[current], 2))
        occupied = set.union(*(record[0] for record in records+[current]))
        assert (origin+2, width+10) in current[0]
        assert charge(current) == -width-5
        for base in (records[:-1], records):
            before = inventory(base)
            after = inventory(base+[current])
            expected_tiles = {((origin-3)//2, column//2)
                              for column in range(6, width+9, 2)}
            assert after['full']-before['full'] == expected_tiles
            assert before['full'] <= after['full']
            assert endpoint_tiles(current) & set.union(
                *(endpoint_tiles(record) for record in base)) == expected_tiles
            expected_events = set()
            for column in range(6, width+10):
                upper = origin-3, column
                lower = origin-2, column
                expected_events.add((len(base), upper, lower))
                expected_events.add((1, lower, upper))
            assert after['events']-before['events'] == expected_events
            assert before['events'] <= after['events']
            assert after['mass']-before['mass'] == width+5
            assert after['raw_reserve']-before['raw_reserve'] == 1
            count += 1
        for missing in ((origin+1, 5), (origin+2, width+11)):
            assert missing in current[1] and missing not in occupied
        assert (origin, 5) in current[0]
        assert (origin+1, 6) in records[1][0]
        assert (origin+3, width+11) in records[4][0]
        assert phi(records+[current])-phi(records[:2]+records[5:]) == -2
        if bottom == 40 and width == 12:
            witness = dict(bottom=bottom, width=width, U=[width+6, 6, 4],
                           raw_increment=1, delta_mass=width+5,
                           delta_full=(width+4)//2, delta_events=2*(width+4),
                           baseline_phi=phi(records[:2]+records[5:]),
                           before_phi=phi(records), after_phi=phi(records+[current]),
                           absent_original_supports=[[origin+1, 5], [origin+2, width+11]])
    assert witness is not None
    return dict(exact_set_controls_with_and_without_W=count, widths=[12, 14, 20, 50, 200],
                local_uniform_ge3_rule='REFUTED_for_endpoint_disjoint_partial_families',
                complete_model_or_target_counterexample=False, witness=witness)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', interior=interior_controls(),
                         returning_bar=return_controls(),
                         scope='Finite corroboration of separately written general geometric '
                         'proofs. Original supports, directed events and positive-original-owner '
                         'N only. No complete feasibility or unrestricted allocation asserted.'),
                     indent=2))
