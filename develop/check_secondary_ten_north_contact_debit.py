"""Exact original-source event checks for the secondary-ten north pair debit."""

import itertools
import json
from collections import Counter

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_first_consumer import prescribed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inventory(records):
    endpoints = set.union(*(record[0] for record in records))
    assert len(endpoints) == sum(len(record[0]) for record in records)
    tiles = {(row//2, column//2) for row, column in endpoints}
    full = set()
    for tile in tiles:
        cells = {(2*tile[0]+row, 2*tile[1]+column)
                 for row, column in itertools.product(range(2), repeat=2)}
        if cells <= endpoints and not any(cells <= record[0] for record in records):
            full.add(tile)
    events = {(index, point, target) for index, record in enumerate(records)
              for point in record[0]
              for target in (set(neighbors(point)) & endpoints)-record[0]-record[1]
              if (point[0]//2, point[1]//2) == (target[0]//2, target[1]//2)}
    mass = sum(max(0, -charge(record)) for record in records)
    return dict(mass=mass, full=full, events=events,
                raw_reserve=mass+2*len(full)-len(events))


def pair_controls():
    patterns = tight = separated = Q_neutral = 0
    for bottom, width, gap, far, other in itertools.product(
            (-24, 40), (8, 10, 20, 50, 200), (2, 4, 8, 40), (4, 6, 10, 40), (4, 6, 12, 50)):
        current = prescribed(bottom, width+gap, far)
        secondary = current[1]
        northern = independent_source((width, 4, other), (False, False, False), (bottom-9, 6))
        assert charge(northern) == 1-width
        base = inventory([secondary])
        joined = inventory([secondary, northern])
        if gap == 2:
            overlap = min(far-2, other)//2
            assert len(joined['full']) == width//2+3+overlap
            assert len(joined['events']) == 2*width+6+2*overlap
            assert joined['raw_reserve']-base['raw_reserve'] == -1
            tight += 1
        else:
            assert len(joined['full']) == width//2+2
            assert len(joined['events']) == 2*width+5
            assert joined['raw_reserve']-base['raw_reserve'] == -2
            separated += 1
        before_Q = inventory(current)
        after_Q = inventory(current+[northern])
        assert after_Q['raw_reserve']-before_Q['raw_reserve'] == joined['raw_reserve']-base['raw_reserve']
        Q_neutral += 1
        patterns += 1
    return dict(arbitrary_parameter_controls=patterns, tight=tight,
                separated=separated, Q_neutral=Q_neutral,
                checked_widths=[8, 10, 20, 50, 200])


def external_controls():
    patterns = interactions = nonzero_full = positive = negative = 0
    signed = Counter()
    witness = None
    bottom = 40
    secondary = prescribed(bottom, 12, 4)[1]
    northern = independent_source((8, 4, 6), (False, False, False), (bottom-9, 6))
    pair = inventory([secondary, northern])
    for dimensions, symmetry, offset in itertools.product(
            ((6, 4, 4), (8, 6, 4), (10, 4, 8)),
            itertools.product((False, True), repeat=3),
            itertools.product(range(22, 40, 2), range(3, 22, 2))):
        external = independent_source(dimensions, symmetry, offset)
        if external[0] & (secondary[0] | northern[0]):
            continue
        before = inventory([secondary, external])
        after = inventory([secondary, external, northern])
        assert pair['full'] <= after['full']-before['full']
        extra_full = (after['full']-before['full'])-pair['full']
        endpoints_external = external[0]
        endpoints_north = northern[0]
        external_events = {event for event in after['events']
                           if (event[0] == 1 and event[2] in endpoints_north) or
                           (event[0] == 2 and event[2] in endpoints_external)}
        delta = after['raw_reserve']-before['raw_reserve']
        assert delta == -2+2*len(extra_full)-len(external_events)
        patterns += 1
        interactions += bool(external_events)
        nonzero_full += bool(extra_full)
        positive += charge(external) == 1
        negative += charge(external) < 0
        external_term = 2*len(extra_full)-len(external_events)
        signed[external_term] += 1
        if external_term == -3 and witness is None:
            missing = bottom-9, 15
            assert missing in northern[1]
            assert missing not in secondary[0] | northern[0] | external[0]
            assert {(bottom-10, 15), (bottom-9, 14)} <= set(neighbors(missing)) & (
                secondary[0] | northern[0] | external[0])
            witness = dict(bottom=bottom, D=[12, 10, 4], L=[8, 4, 6],
                           external_dimensions=list(dimensions), external_symmetry=list(symmetry),
                           external_offset=list(offset), external_charge=charge(external),
                           raw_reserve_before=before['raw_reserve'],
                           raw_reserve_after=after['raw_reserve'],
                           extra_full_tiles=sorted(extra_full), external_term=external_term,
                           missing_forced_original_support=missing,
                           external_events=[dict(owner='W' if event[0] == 1 else 'L',
                                                 endpoint=event[1], target=event[2])
                                            for event in sorted(external_events)])
    assert all((patterns, interactions, nonzero_full, positive, negative)) and witness is not None
    return dict(endpoint_disjoint_partial_patterns=patterns,
                patterns_with_external_events=interactions,
                patterns_with_extra_full_tiles=nonzero_full,
                positive_external_sources=positive, negative_external_sources=negative,
                external_signed_term_distribution=dict(sorted(signed.items())),
                endpoint_only_external_nonnegativity_counterexample=witness,
                complete_feasibility_not_assumed=True)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', pairs=pair_controls(), external=external_controls(),
                         scope='Direct checks of a separately written all-parameter raw event '
                         'functional identity and external owner partition. Partial families '
                         'are not asserted complete or legal extensions. No monotonicity or '
                         'global allocation inequality is inferred.'), indent=2))
