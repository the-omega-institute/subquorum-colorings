"""Exact all-original sets for a width-dependent positive-owner return debit."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_arbitrary_t_consumers import old_chain
from check_secondary_ten_both_far_charge_separation import counts
from check_secondary_ten_both_far_compensation import originals
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    cases = []
    for width, far, translation in itertools.product(
            (12, 14, 50, 2000), (4, 6, 40, 2000), ((0, 0), (-64, -100), (20, 200))):
        fixed, unused, unused, sites = old_chain(31, 0, [width, 12], [far+24]*2, 6)
        receiver, consumer = originals(sites, [width, 12], (1, 6, 0, far+2, far))
        first = independent_source((2*far+20, 4, 40),
                                   (True, False, True), (2*far+42, -34))
        second = independent_source((6, 4, width+8),
                                    (True, True, False), (16, width+15))
        fixed = [shift(record, translation) for record in fixed]
        receiver, consumer, first, second = [shift(record, translation)
                                            for record in (receiver, consumer, first, second)]
        moved = lambda point: (point[0]+translation[0], point[1]+translation[1])
        paired = fixed+[receiver, consumer]
        base = paired+[first]
        old, pair_receipt, before, after = [inventory(records)
                                           for records in (fixed, paired, base, base+[second])]
        assert phi_from(paired, pair_receipt)-phi_from(fixed, old) == 4
        assert phi_from(base, before)-phi_from(paired, pair_receipt) == -3
        assert counts(second) == (width//2+11, width//2+10, width//2+10)
        assert charge(second) == 1
        assert after['mass'] == before['mass']
        assert sum(charge(record) > 0 for record in base+[second]) == 1+sum(
            charge(record) > 0 for record in base)
        full = {(moved((22, column))[0]//2, moved((22, column))[1]//2)
                for column in range(6, width+12, 2)}
        events = {(19, moved((23, column)), moved((22, column)))
                  for column in range(7, width+13)}
        events |= {(len(base), moved((22, column)), moved((23, column)))
                   for column in range(8, width+13, 2)}
        assert after['full']-before['full'] == full and len(full) == width//2+3
        assert after['events']-before['events'] == events and len(events) == 3*width//2+9
        assert before['full'] <= after['full'] and before['events'] <= after['events']
        old_corner_events = {
            (19, moved((23, 6)), moved((22, 6))),
            (len(base)-1, moved((22, 6)), moved((23, 6)))}
        assert old_corner_events <= before['events'] & after['events']
        corner_cells = {moved((row, column)) for row in (22, 23) for column in (6, 7)}
        corner_new_events = {event for event in after['events']-before['events']
                             if event[1] in corner_cells and event[2] in corner_cells}
        assert corner_new_events == {(19, moved((23, 7)), moved((22, 7)))}
        assert phi_from(base+[second], after)-phi_from(base, before) == -width//2-2
        assert phi_from(base+[second], after)-phi_from(fixed, old) == -width//2-1
        occupied = set.union(*(record[0] for record in base+[second]))
        support = moved((23, width+13))
        assert moved((22, 7)) in first[1] & second[0]
        assert support in second[1] & fixed[19][1] and support not in occupied
        assert set(neighbors(support)) & occupied == {
            moved((22, width+13)), moved((23, width+12))}
        witnesses = {moved((25, width+14)), moved((22, width+14))}
        assert moved((25, width+14)) in fixed[18][0]
        assert moved((22, width+14)) in second[0]
        patterns = set()
        for symmetry in itertools.product((False, True), repeat=3):
            module = transform_module(rotor(), symmetry)
            record = module['endpoints'], module['selected'], {
                tuple(sorted(edge)) for edge in module['matching']}
            for anchor in record[0]:
                internal = {(point[0]-anchor[0], point[1]-anchor[1])
                            for point in set(neighbors(anchor)) & record[0]}
                if not internal or not internal <= {(1, 0), (0, 1)}:
                    continue
                candidate = shift(record, (support[0]-anchor[0], support[1]-anchor[1]))
                assert candidate[0] & witnesses
                patterns.add(frozenset(candidate[0]))
        assert len(patterns) == 4
        cases.append(dict(width=width, far=far, translation=translation,
                          second_marginal=-width//2-2, total_selected_increment=-width//2-1))
    print(json.dumps(dict(status='PASS', exact_original_set_controls=len(cases), cases=cases,
        rotor_exclusion_controls=4*len(cases),
        scope='General written two-parameter unbounded positive-owner return debit. '
              'Exact NEW full/event sets, next forced support and rotor exclusion checked. Complete '
              'extendibility OPEN; no global inequality or selected-pair counterexample.'), indent=2))


if __name__ == '__main__':
    main()
