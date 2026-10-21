"""Exact original-source obstruction to nonnegative forced-site consumption."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_arbitrary_t_consumers import old_chain
from check_secondary_ten_both_far_compensation import originals
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    cases = []
    for far, translation in itertools.product((4, 6, 10, 40, 100, 2000),
                                               ((0, 0), (-64, -100), (20, 200))):
        fixed, unused, unused, sites = old_chain(31, 0, [12]*2, [far+24]*2, 6)
        receiver, consumer = originals(sites, [12]*2, (1, 6, 0, far+2, far))
        owner = independent_source((2*far+20, 4, 40), (True, False, True), (2*far+42, -34))
        moved = lambda point: (point[0]+translation[0], point[1]+translation[1])
        fixed = [shift(record, translation) for record in fixed]
        receiver, consumer, owner = [shift(record, translation)
                                     for record in (receiver, consumer, owner)]
        base = fixed+[receiver, consumer]
        before, after = inventory(base), inventory(base+[owner])
        point, renewed = moved((2*far+41, -30)), moved((22, 7))
        owner_index = len(base)
        full = {(moved(point)[0]//2, moved(point)[1]//2)
                for point in ((22, 2), (22, 4), (2*far+40, -30))}
        events = {(19, moved((23, column)), moved((22, column))) for column in range(1, 7)}
        events |= {(owner_index, moved((22, column)), moved((23, column)))
                   for column in (2, 4, 6)}
        events.add((owner_index, point, moved((2*far+40, -30))))
        assert after['full']-before['full'] == full and len(full) == 3
        assert after['events']-before['events'] == events and len(events) == 10
        assert before['full'] <= after['full'] and before['events'] <= after['events']
        assert after['mass']-before['mass'] == 1 and charge(owner) == -1
        tiles = {(row//2, column//2) for row, column in owner[0]}
        inside = {support for support in owner[1]
                  if (support[0]//2, support[1]//2) in tiles}
        assert (len(owner[2]), len(tiles), len(inside)) == (2*far+41, far+32, 22)
        assert phi_from(base+[owner], after)-phi_from(base, before) == -3
        old = inventory(fixed)
        assert phi_from(base, before)-phi_from(fixed, old) == 4
        assert phi_from(base+[owner], after)-phi_from(fixed, old) == 1
        endpoints = set.union(*(record[0] for record in base+[owner]))
        assert point in owner[0] and renewed not in endpoints and renewed in owner[1]
        assert set(neighbors(renewed)) & endpoints == {moved((22, 6)), moved((23, 7))}
        cases.append(dict(far=far, translation=translation, owner_width=2*far+20,
                          new_owner_increment=-3, total_selected_increment=1))
    print(json.dumps(dict(status='PASS', exact_original_set_controls=len(cases), cases=cases,
        scope='All-even-g written exact three-unit return-debit family. Refutes '
              'nonnegative marginal from endpoint-disjoint forced-site consumption '
              'alone. Complete extendibility OPEN; not a global counterexample. '
              'New far axial support is still forced.'), indent=2))


if __name__ == '__main__':
    main()
