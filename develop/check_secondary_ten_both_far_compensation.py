"""Exact arbitrary-both-far receipts, triple tiles and simultaneous physical ledgers."""

import itertools
import json
import random
from collections import Counter

from check_secondary_ten_arbitrary_t_consumers import expected_local, north_U, old_chain
from check_secondary_ten_e_far_frontier import frontier as receiver_frontier
from check_secondary_ten_e_far_frontier import receipts as receiver_receipts
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_left_chain_exterior import frontier as consumer_frontier
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def originals(sites, widths, choice):
    index, breadth, gap, receiver_far, consumer_far = choice
    anchor, unused, lateral = sites[index]
    column = lateral+widths[index]+13
    return (north_U(anchor+3, column, widths[index]+breadth+14+gap,
                    10, receiver_far, True),
            north_U(anchor, lateral, breadth, 4, consumer_far, True))


def predicted(sites, widths, choice, receiver_owner, consumer_owner):
    index, breadth, gap, receiver_far, consumer_far = choice
    anchor, unused, lateral = sites[index]
    column = lateral-breadth-gap
    bottom = anchor-11+receiver_far
    terminal = anchor-8+consumer_far
    allowed, phase, deduction, contact = receiver_frontier(sites, index, column, bottom)
    other_allowed, unused, exceptional, other_contact = consumer_frontier(
        sites, index, breadth, 4, consumer_far)
    assert allowed and other_allowed
    receiver_full, receiver_events = receiver_receipts(sites, index, len(widths),
        column, bottom, phase, deduction, contact, receiver_owner)
    consumer_full, consumer_events = expected_local(anchor, lateral, widths[index],
        breadth, 4, consumer_far, True, 9*len(widths)+1+index, consumer_owner)
    if exceptional:
        other_anchor, unused, other_lateral = sites[other_contact]
        overlap = (terminal-other_anchor+2)//2
        assert overlap in (0, 1) and breadth >= 28
        if overlap:
            consumer_full.add(((other_anchor-1)//2, (other_lateral-4)//2))
            consumer_events.add((consumer_owner, (other_anchor-1, other_lateral-3),
                                 (other_anchor-1, other_lateral-4)))
        consumer_events |= {(11*len(widths)+1+other_contact,
            (other_anchor-2+2*step, other_lateral-4),
            (other_anchor-2+2*step, other_lateral-3)) for step in range(overlap+1)}
    mutual_full, mutual_events, triple_full = set(), set(), set()
    epsilon = int(gap == 0 and bottom < terminal)
    triple = int(gap == 0 and contact is not None
                 and column == sites[contact][2]-4
                 and bottom == sites[contact][0]-3
                 and terminal >= sites[contact][0]-2)
    if gap == 0:
        assert contact == other_contact
        mutual_full = {(row//2, column//2)
                       for row in range(anchor-7, min(bottom-2, terminal-1)+1, 2)}
        mutual_events = {(owner, source, target)
                         for row in range(anchor-7, min(bottom, terminal-1)+1, 2)
                         for owner, source, target in (
                             (receiver_owner, (row, column), (row, column+1)),
                             (consumer_owner, (row, column+1), (row, column)))}
        assert len(mutual_events)-2*len(mutual_full) == 2*epsilon
    if triple:
        triple_full.add((bottom//2, column//2))
    full_parts = (receiver_full, consumer_full, mutual_full, triple_full)
    event_parts = (receiver_events, consumer_events, mutual_events)
    assert all(not first & second for first, second in itertools.combinations(full_parts, 2))
    assert all(not first & second for first, second in itertools.combinations(event_parts, 2))
    assert deduction+2*epsilon <= 2
    value = breadth-deduction-exceptional-2*epsilon+2*triple
    assert value >= 4 and (not exceptional or value >= 25)
    return (set.union(*full_parts), set.union(*event_parts), value,
            (phase, deduction, exceptional, epsilon, triple))


def check_group(fixed, sites, widths, choices, before=None):
    before = inventory(fixed) if before is None else before
    combined = list(fixed)
    full, events, footprints = set(), set(), set()
    value = 0
    profiles = Counter()
    for choice in choices:
        receiver, consumer = originals(sites, widths, choice)
        footprint = {(row//2, column//2) for row, column in receiver[0] | consumer[0]}
        assert not footprint & footprints
        footprints |= footprint
        pair_full, pair_events, pair_gain, profile = predicted(
            sites, widths, choice, len(combined), len(combined)+1)
        assert not pair_full & full and not pair_events & events
        full |= pair_full
        events |= pair_events
        value += pair_gain
        profiles[str(profile)] += 1
        combined += [receiver, consumer]
    after = inventory(combined)
    assert after['full']-before['full'] == full
    assert after['events']-before['events'] == events
    assert before['full'] <= after['full'] and before['events'] <= after['events']
    assert after['mass']-before['mass'] == sum(choice[1] for choice in choices)
    assert phi_from(combined, after)-phi_from(fixed, before) == value >= 4*len(choices)
    return dict(pairs=len(choices), exact_gain=value, new_full=len(full),
                new_events=len(events), profiles=dict(profiles))


def pair_controls(origin, offset):
    widths, depths = [12, 14, 20, 18], [24, 26, 40, 24]
    fixed, unused, unused, sites = old_chain(origin, offset, widths, depths, 6)
    before = inventory(fixed)
    exact = 0
    profiles = Counter()
    minimum = None
    for index in range(1, len(widths)):
        anchor, unused, lateral = sites[index]
        breadths = {6, 8, lateral-sites[-1][2]+8}
        fars = {4, 6, 8, 12, 30, 100}
        for later in range(index+1, len(sites)):
            breadths |= {lateral-sites[later][2]+step for step in (-2, 0, 2, 4, 6)}
            fars |= {sites[later][0]-anchor+step for step in (2, 4, 6, 8, 10)}
        for breadth, gap, receiver_far, consumer_far in itertools.product(
                sorted(breadths), (0, 2, 18), sorted(fars), sorted(fars)):
            if breadth < 6 or min(receiver_far, consumer_far) < 4:
                continue
            bottom, terminal = anchor-11+receiver_far, anchor-8+consumer_far
            if not receiver_frontier(sites, index, lateral-breadth-gap, bottom)[0]:
                continue
            if not consumer_frontier(sites, index, breadth, 4, consumer_far)[0]:
                continue
            result = check_group(fixed, sites, widths,
                [(index, breadth, gap, receiver_far, consumer_far)], before)
            profiles.update(result['profiles'])
            minimum = result['exact_gain'] if minimum is None else min(minimum, result['exact_gain'])
            exact += 1
    assert minimum == 4
    assert any(profile.endswith(', 1)') for profile in profiles)
    return dict(exact_full_event_set_controls=exact, minimum_pair_gain=minimum,
                profiles=dict(sorted(profiles.items())))


def batch_controls():
    generator = random.Random(20261022)
    widths, depths = [12, 14, 20, 18, 12, 30], [24, 26, 40, 24, 80, 24]
    fixed, unused, unused, sites = old_chain(31, -100, widths, depths, 6)
    before = inventory(fixed)
    blocked = set.union(*(record[0] for record in fixed))
    groups = []
    for attempt in range(60):
        occupied = set(blocked)
        selected = []
        indices = list(range(1, len(widths)))
        generator.shuffle(indices)
        for index in indices:
            for trial in range(30):
                choice = (index, generator.choice((6, 8, 20, 40, 80, 150)),
                          generator.choice((0, 2, 6, 18)),
                          generator.choice((4, 6, 10, 20, 40, 80, 200)),
                          generator.choice((4, 6, 10, 20, 40, 80, 200)))
                receiver, consumer = originals(sites, widths, choice)
                if (receiver[0] | consumer[0]) & occupied:
                    continue
                assert not receiver[0] & consumer[0]
                occupied |= receiver[0] | consumer[0]
                selected.append(choice)
                break
        if len(selected) >= 2:
            groups.append(check_group(fixed, sites, widths, selected, before))
    assert groups and max(group['pairs'] for group in groups) >= 4
    return dict(actual_endpoint_disjoint_groups=len(groups),
                pair_counts=sorted({group['pairs'] for group in groups}),
                minimum_gain_per_pair=min(group['exact_gain']/group['pairs'] for group in groups))


def long_controls():
    groups = []
    for count in (3, 6, 12):
        widths = [12+2*(index % 7) for index in range(count)]
        depths = [24+2*(index % 5) for index in range(count)]
        fixed, unused, unused, sites = old_chain(31, -100, widths, depths, 6)
        outside = sites[-1][2]-1000
        choices = [(index, sites[index][2]-(outside-100*(count-index)),
                    2*(index % 2), 2000+2*(index % 3), 2000+2*(index % 5))
                   for index in range(1, count)]
        groups.append(check_group(fixed, sites, widths, choices))
    fixed, unused, unused, sites = old_chain(31, 0, [12]*3, [24]*3, 6)
    triple = check_group(fixed, sites, [12]*3, [(1, 28, 0, 26, 24)])
    assert triple['exact_gain'] == 27
    old_loss = check_group(fixed, sites, [12]*3, [(1, 6, 18, 22, 4)])
    assert old_loss['exact_gain'] == 4
    return dict(both_far_2000_groups=groups, triple_owner_correction=triple,
                sharp_old_chain_loss=old_loss)


def main():
    print(json.dumps(dict(status='PASS', pairs=[pair_controls(31, 0),
        pair_controls(-33, -100)], batches=batch_controls(), long_legs=long_controls(),
        scope='Exact physical full-tile and owner-labelled event SETS for both '
              'arbitrary far legs, including the triple-owner correction and '
              'automatic pair-footprint separation. Finite controls supplement '
              'the unbounded written proof; no complete extension or global bound.'), indent=2))


if __name__ == '__main__':
    main()
