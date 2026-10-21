"""Exact immutable-source controls for aligned batches and old-band losses."""

import itertools
import json

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_root_bar_pair_compensation import baseline


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def footprint(record):
    return {(row//2, column//2) for row, column in record[0]}


def packing_controls():
    candidates = [independent_source(dimensions, (False, False, False), offset)
                  for dimensions, offset in itertools.product(
                      ((6, 4, 4), (8, 6, 10), (20, 14, 4)),
                      itertools.product((-8, -2, 0, 4, 12), (-11, -3, 1, 9, 21)))]
    checked = rejected = 0
    for first, second in itertools.combinations(candidates, 2):
        if first[0] & second[0]:
            rejected += 1
            continue
        assert not footprint(first) & footprint(second)
        checked += 1
    positive = independent_source((8, 10, 10), (False, False, False), (0, 0))
    translated = shift(positive, (4, 8))
    assert charge(positive) == charge(translated) == 1
    assert not positive[0] & translated[0]
    assert footprint(positive) & footprint(translated)
    return dict(disjoint_aligned_pairs=checked, rejected_collisions=rejected,
                opposite_phase_counterexample_shared_tiles=len(
                    footprint(positive) & footprint(translated)))


def family(amount, offset):
    old_groups, pairs = [], []
    far_column = 25+100*(amount-1)+7
    for index in range(amount):
        column = 25+100*index
        root_bar = -10*(amount-1-index)
        breadth = far_column-column+1
        old, root = baseline(12, 4, 6, 4, root_bar, breadth, 4)
        if index == 0:
            next_dimensions = breadth+2, 28-root_bar, 8-root_bar
        else:
            next_dimensions = 6, 28-root_bar, 4
        next_owner = independent_source(next_dimensions, (False, False, False),
                                        (root_bar-6, 23))
        translation = offset[0], offset[1]+100*index
        old_groups.append([shift(record, translation) for record in old])
        pairs.append([shift(root, translation), shift(next_owner, translation)])
    return old_groups, pairs


def batch_control(amount, offset):
    old_groups, pairs = family(amount, offset)
    old = [record for group in old_groups for record in group]
    new = [record for pair in pairs for record in pair]
    all_records = old+new
    before, after = inventory(old), inventory(all_records)
    endpoint_owners = {point: owner for owner, record in enumerate(all_records)
                       for point in record[0]}
    local_gains, common_gains, individual_full = [], [], set()
    individual_events = set()
    for pair_index, (group, pair) in enumerate(zip(old_groups, pairs)):
        local_before, local_after = inventory(group), inventory(group+pair)
        local_gains.append(phi_from(group+pair, local_after)-phi_from(group, local_before))
        single = inventory(old+pair)
        common_gains.append(phi_from(old+pair, single)-phi_from(old, before))
        new_full = single['full']-before['full']
        assert not new_full & individual_full
        individual_full |= new_full
        new_events = {(owner if owner < len(old) else owner+2*pair_index, point, target)
                      for owner, point, target in single['events']-before['events']}
        assert not new_events & individual_events
        individual_events |= new_events
    assert local_gains == common_gains == [1]+[2]*(amount-1)
    cooperative_full = after['full']-before['full']-individual_full
    cross_events = {event for event in after['events']
                    if event[0] >= len(old) and endpoint_owners[event[2]] >= len(old)
                    and (event[0]-len(old))//2 != (endpoint_owners[event[2]]-len(old))//2}
    assert before['events'] <= after['events']
    assert not individual_events & cross_events
    assert after['events']-before['events'] == individual_events | cross_events
    contacts = {}
    for first in range(amount):
        for second in range(first+1, amount):
            assert not footprint(pairs[first][0]) & footprint(pairs[second][0])
            assert not footprint(pairs[first][1]) & footprint(pairs[second][1])
        for second in range(amount):
            if first == second:
                continue
            shared = footprint(pairs[first][0]) & footprint(pairs[second][1])
            if shared:
                contacts[first, second] = shared
    assert set(contacts) == {(index, 0) for index in range(1, amount)}
    for (root_index, next_index), shared in contacts.items():
        root_bar = -10*(amount-1-root_index)+offset[0]
        root_far = 25+100*(amount-1)+7+offset[1]
        assert (root_bar, root_far+1) in pairs[next_index][1][0]
        assert all(tile[1] == root_far//2 for tile in shared)
        source_indices = {len(old)+2*root_index, len(old)+2*next_index+1}
        events = {event for event in cross_events
                  if {event[0], endpoint_owners[event[2]]} == source_indices}
        assert 2*len(cooperative_full & shared)-len(events) == -1
    correction = 2*len(cooperative_full)-len(cross_events)
    joint = phi_from(all_records, after)-phi_from(old, before)
    assert correction == 1-amount
    assert joint == sum(common_gains)+correction == amount
    retained = old+[record for pair in pairs[1:] for record in pair]
    retained_before = inventory(retained)
    retained_after = inventory(retained+pairs[0])
    old_extension_gain = phi_from(retained+pairs[0], retained_after)-phi_from(retained, retained_before)
    assert old_extension_gain == 2-amount
    return dict(amount=amount, translation=offset, local_sum=sum(local_gains),
                joint_gain=joint, foreign_contacts=len(contacts), correction=correction,
                root_zero_added_after_other_pairs=old_extension_gain)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', packing=packing_controls(),
        batches=[batch_control(amount, offset) for amount, offset in itertools.product(
            (1, 2, 3, 6, 12), ((0, 0), (-100, -200)))],
        scope='Finite exact-set controls only. General proofs are in the companion note. '
              'No complete extension existence or global grid bound is asserted.'), indent=2))
