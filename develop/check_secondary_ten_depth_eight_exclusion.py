"""Full-source controls for the depth-eight complete-extension exclusion."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_secondary_ten_distinct_pair_consumers import east_rotor, upper_source
from check_secondary_ten_north_return_closure import continuation, returning, tile_signature
from check_secondary_ten_north_third_left_return import sources
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check():
    caps = collisions = rotor_collisions = receipts = 0
    for bottom, width in itertools.product((-24, 40), (12, 20, 50)):
        origin = bottom-9
        for gap, old_far in ((8, 4), (8, 14), (10, 16), (10, 200)):
            records = sources(bottom, width)+[
                returning(bottom, width, 0),
                continuation(bottom, width, width+gap, 8, old_far, False)]
            endpoints = set.union(*(record[0] for record in records))
            target = (origin+2, width+12)
            assert target not in endpoints and target in records[7][1]
            anchors = ((origin+2, width+11), (origin+2, width+13),
                       (origin+3, width+12))
            assert anchors[0] in records[7][0]
            assert set(anchors[1:]) <= records[4][0]
            for breadth, far in itertools.product(
                    (width+12, width+14, width+50), (4, 12, 200)):
                cap = upper_source(origin, width, breadth, 8, far, False)
                if cap[0] & endpoints:
                    continue
                assert target not in cap[0]
                caps += 1
                for consumer_breadth, depth, consumer_far, right in itertools.product(
                        (6, 8, 50), (4, 6, 8, 10, 12, 100), (4, 200), (False, True)):
                    consumer = independent_source(
                        (consumer_breadth, depth, consumer_far), (False, False, not right),
                        (origin+2-depth, width+11 if right else width+13))
                    assert target in consumer[0]
                    if depth >= 10:
                        witness = (origin-7, width+12)
                        retained = cap
                    elif right:
                        witness = (origin+3-depth, width+14)
                        retained = cap
                    else:
                        witness = (origin+3-depth, width+11)
                        retained = records[7]
                    assert witness in consumer[0] & retained[0]
                    collisions += 1
                for handed in (False, True):
                    module = transform_module(rotor(), (False, False, handed),
                                              (origin-2, width+9 if not handed else width+15))
                    if target not in module['endpoints']:
                        raise AssertionError(('rotor tip chart', handed))
                    assert (origin, width+13) in module['endpoints'] & records[4][0]
                    rotor_collisions += 1
            if gap == 8 and old_far == 4:
                terminal = east_rotor(origin, width, False)
                cap = upper_source(origin, width, width+12, 8, 4, False)
                before, after, signature = tile_signature(records+[terminal], cap)
                assert after['raw_reserve']-before['raw_reserve'] == 3
                assert sum(value[0] for tile, value in signature.items()) == (width+8)//2
                assert sum(value[1] for tile, value in signature.items()) == 2*(width+8)
                receipts += 1
    return {'status': 'PASS', 'endpoint_disjoint_caps_with_forced_missing_support': caps,
            'explicit_U_collision_witnesses': collisions,
            'explicit_rotor_collision_witnesses': rotor_collisions,
            'unchanged_nonextendible_receipt_witnesses': receipts,
            'scope': 'Finite full-source controls of the written all-parameter exclusion; no complete family is constructed.'}


if __name__ == '__main__':
    print(json.dumps(check(), indent=2))
