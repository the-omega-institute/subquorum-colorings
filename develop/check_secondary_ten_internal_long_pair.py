"""Exact arbitrary-far internal-pair receipts and actual disjoint tile footprints."""

import itertools
import json

from check_secondary_ten_arbitrary_t_consumers import north_U, old_chain
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_internal_short_pair import receipts
from check_secondary_ten_left_chain_exterior import frontier
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def expected_pair(fixed, sites, widths, index, breadth, gap, far, receiver_owner, consumer_owner):
    anchor, unused, lateral = sites[index]
    allowed, phase, delta, contact = frontier(sites, index, breadth, 4, far)
    assert allowed
    full, events = receipts(anchor, lateral, widths[index], breadth, gap,
                            9*len(widths)+1+index, receiver_owner, consumer_owner)
    if delta:
        other_anchor, unused, other_lateral = sites[contact]
        overlap = (anchor-8+far-other_anchor+2)//2
        assert overlap in (0, 1) and breadth >= 28
        if overlap:
            full.add(((other_anchor-1)//2, (other_lateral-4)//2))
            events.add((consumer_owner, (other_anchor-1, other_lateral-3),
                        (other_anchor-1, other_lateral-4)))
        events |= {(11*len(widths)+1+contact,
                    (other_anchor-2+2*step, other_lateral-4),
                    (other_anchor-2+2*step, other_lateral-3)) for step in range(overlap+1)}
    return full, events, breadth-2*int(gap == 0)-delta, delta


def check_group(fixed, sites, widths, choices):
    before = inventory(fixed)
    combined = list(fixed)
    footprints, expected_full, expected_events = set(), set(), set()
    gain = activations = 0
    for index, breadth, gap, far in choices:
        anchor, unused, lateral = sites[index]
        receiver = north_U(anchor+3, lateral+widths[index]+13,
                           widths[index]+breadth+14+gap, 10, 4, True)
        consumer = north_U(anchor, lateral, breadth, 4, far, True)
        footprint = {(row//2, column//2) for row, column in receiver[0] | consumer[0]}
        assert not footprint & footprints
        footprints |= footprint
        full, events, value, delta = expected_pair(fixed, sites, widths, index,
            breadth, gap, far, len(combined), len(combined)+1)
        assert not full & expected_full and not events & expected_events
        expected_full |= full
        expected_events |= events
        gain += value
        activations += delta
        combined += [receiver, consumer]
    after = inventory(combined)
    assert after['full']-before['full'] == expected_full
    assert after['events']-before['events'] == expected_events
    assert before['full'] <= after['full'] and before['events'] <= after['events']
    assert phi_from(combined, after)-phi_from(fixed, before) == gain >= 4*len(choices)
    return dict(pairs=len(choices), gain=gain, activations=activations,
                new_full=len(expected_full), new_events=len(expected_events))


def main():
    exact = activated = minimum = 0
    batch_controls = []
    for origin, offset in ((31, 0), (-33, -100)):
        widths, depths = [12, 14, 20, 18, 12, 30], [24, 26, 40, 24, 80, 24]
        fixed, unused, unused, sites = old_chain(origin, offset, widths, depths, 40)
        blocked = set.union(*(record[0] for record in fixed))
        choices = []
        for index in range(1, len(widths)):
            anchor, unused, lateral = sites[index]
            breadths = {6, 8, lateral-sites[-1][2]+6}
            for later in range(index+1, len(widths)):
                breadths |= {lateral-sites[later][2]+step for step in (0, 2, 4, 6)}
            for breadth, gap in itertools.product(sorted(breadths), (0, 2)):
                fars = {4, 10, 80, 2000}
                for later in range(index+1, len(widths)):
                    fars |= {sites[later][0]-anchor+step for step in (-4, -2, 0, 2, 6, 8)}
                for far in sorted(far for far in fars if far >= 4):
                    allowed, phase, delta, contact = frontier(sites, index, breadth, 4, far)
                    if not allowed:
                        continue
                    result = check_group(fixed, sites, widths, [(index, breadth, gap, far)])
                    exact += 1
                    activated += delta
                    minimum = result['gain'] if not minimum else min(minimum, result['gain'])
                    if far != 4 and breadth <= 40:
                        choices.append((index, breadth, gap, far))
        for start in range(0, min(200, len(choices)), 7):
            selected, occupied = [], set(blocked)
            used = set()
            for choice in choices[start:]+choices[:start]:
                index, breadth, gap, far = choice
                if index in used:
                    continue
                anchor, unused, lateral = sites[index]
                receiver = north_U(anchor+3, lateral+widths[index]+13,
                                   widths[index]+breadth+14+gap, 10, 4, True)
                consumer = north_U(anchor, lateral, breadth, 4, far, True)
                if (receiver[0] | consumer[0]) & occupied:
                    continue
                assert not receiver[0] & consumer[0]
                occupied |= receiver[0] | consumer[0]
                used.add(index)
                selected.append(choice)
            if len(selected) >= 2:
                batch_controls.append(check_group(fixed, sites, widths, selected))
    long_batches = []
    for count in (3, 6, 12):
        widths = [12+2*(index % 7) for index in range(count)]
        depths = [24+2*(index % 5) for index in range(count)]
        fixed, unused, unused, sites = old_chain(31, -100, widths, depths, 6)
        far_base = sites[-1][2]-1000
        choices = [(index, sites[index][2]-(far_base-100*(count-index)), 0, 2000)
                   for index in range(1, count)]
        long_batches.append(check_group(fixed, sites, widths, choices))
    assert minimum == 4 and activated > 0 and batch_controls
    print(json.dumps(dict(status='PASS', exact_arbitrary_far_pair_sets=exact,
        activated_old_X_receipts=activated, minimum_pair_gain=minimum,
        actual_endpoint_disjoint_batches=len(batch_controls),
        batch_pair_counts=sorted({entry['pairs'] for entry in batch_controls}),
        long_far_2000_batches=long_batches,
        scope='Exact selected-union receipts and pairwise FULL endpoint tile-footprint '
              'disjointness for actual endpoint-disjoint pairs, without a far-leg cutoff '
              'in the written proof. No complete extension existence or global bound.'), indent=2))


if __name__ == '__main__':
    main()
