"""Full-source checks for an even-bar contact ledger and a two-gate obstruction."""

import itertools
import json
import random

from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def footprint(record):
    return {(row//2, column//2) for row, column in record[0]}


def ledger(records):
    receipt = inventory(records)
    owners = {point: owner for owner, record in enumerate(records) for point in record[0]}
    tiles = {}
    for point, owner in owners.items():
        tiles.setdefault((point[0]//2, point[1]//2), set()).add(owner)
    assert max(map(len, tiles.values())) <= 2
    signs = [charge(record) for record in records]
    assert set(signs) <= {-1, 1}
    edges, positive_degrees = [], {}
    full_partition, event_partition = set(), set()
    for first, second in itertools.combinations(range(len(records)), 2):
        shared = footprint(records[first]) & footprint(records[second])
        assert not (shared and signs[first] == signs[second] == -1)
        for column in {tile[1] for tile in shared}:
            band = {tile for tile in shared if tile[1] == column}
            full = receipt['full'] & band
            events = {event for event in receipt['events']
                      if {event[0], owners[event[2]]} == {first, second}
                      and (event[1][0]//2, event[1][1]//2) in band}
            assert not full_partition & full and not event_partition & events
            full_partition |= full
            event_partition |= events
            opposite = signs[first] != signs[second]
            assert 2*len(full)-len(events) == -int(opposite)
            if opposite:
                edges.append((first, second, column))
                positive = first if signs[first] == 1 else second
                positive_degrees[positive] = positive_degrees.get(positive, 0)+1
    assert all(degree <= 2 for degree in positive_degrees.values())
    assert full_partition == receipt['full'] and event_partition == receipt['events']
    assert phi_from(records, receipt) == len(records)-len(edges)
    parent = list(range(len(records)))
    def representative(owner):
        while parent[owner] != owner:
            owner = parent[owner]
        return owner
    for first, second, column in edges:
        parent[representative(first)] = representative(second)
    components = len({representative(owner) for owner in range(len(records))})
    cycles = len(edges)-len(records)+components
    assert phi_from(records, receipt) == components-cycles
    return dict(sources=len(records), contacts=len(edges), components=components,
                cycle_rank=cycles, Phi=phi_from(records, receipt))


def nested(amount):
    outer = independent_source((8, 8*amount+4, 8*amount+4),
                               (False, False, False), (0, -1))
    return [outer]+[independent_source((6, 4, 4), (False, False, False), (2+8*index, 0))
                    for index in range(amount)]


def contact_controls():
    candidates = [independent_source(dimensions, (False, False, False), offset)
                  for dimensions, offset in itertools.product(
                      ((6, 4, 4), (8, 6, 10), (12, 10, 6)),
                      itertools.product((-4, 0, 4, 10), (-10, -3, 0, 1, 8)))]
    pairs = 0
    for first, second in itertools.combinations(candidates, 2):
        if not first[0] & second[0]:
            ledger([first, second])
            pairs += 1
    generator = random.Random(20261022)
    batches = 0
    for attempt in range(40):
        ordered = generator.sample(candidates, len(candidates))
        chosen, occupied = [], set()
        for record in ordered:
            if not record[0] & occupied:
                chosen.append(record)
                occupied |= record[0]
        ledger(chosen)
        batches += 1
    nested_results = [ledger(nested(amount)) for amount in (1, 2, 3, 6, 12)]
    assert all(row['Phi'] == 2-row['sources'] for row in nested_results)
    return dict(disjoint_pairs=pairs, greedy_batches=batches, nested=nested_results)


def rotor_record(symmetry):
    module = transform_module(rotor(), symmetry)
    return module['endpoints'], module['selected'], {tuple(sorted(edge)) for edge in module['matching']}


def anchor_records(record, point, free):
    for anchor in record[0]:
        own = {(row-anchor[0], column-anchor[1]) for row, column in record[0]
               if abs(row-anchor[0])+abs(column-anchor[1]) == 1}
        if own and own <= free:
            yield shift(record, (point[0]-anchor[0], point[1]-anchor[1]))


def obstruction_controls():
    fixed = nested(2)
    blocked = set.union(*(record[0] for record in fixed))
    points = (7, 1), (7, 6)
    assert set(points) <= fixed[1][1] and not set(points) & blocked
    dimensions = itertools.product((6, 8, 12), (4, 6, 10), (4, 6, 10))
    checked_U = 0
    for size, symmetry in itertools.product(dimensions, itertools.product((False, True), repeat=3)):
        record = independent_source(size, symmetry, (0, 0))
        for point, free in zip(points, ({(0, 1), (1, 0)}, {(0, -1), (1, 0)})):
            for moved in anchor_records(record, point, free):
                assert moved[0] & blocked
                checked_U += 1
    survivors = []
    checked_rotor = 0
    for point, free in zip(points, ({(0, 1), (1, 0)}, {(0, -1), (1, 0)})):
        current = set()
        for symmetry in itertools.product((False, True), repeat=3):
            for moved in anchor_records(rotor_record(symmetry), point, free):
                checked_rotor += 1
                if not moved[0] & blocked:
                    current.add(frozenset(moved[0]))
        assert len(current) == 2
        survivors.append(current)
    collisions = [sorted(left & right) for left, right in itertools.product(*survivors)]
    assert len(collisions) == 4 and all(collisions)
    large = 0
    for top, left_depth, right_depth, next_depth in (
            (2, 8, 8, 4), (10, 16, 100, 200), (2000, 4000, 6000, 4000)):
        records = [independent_source((8, left_depth, right_depth),
                                      (False, False, False), (0, -1)),
                   independent_source((6, 4, 4), (False, False, False), (top, 0)),
                   independent_source((6, next_depth, 4), (False, False, False), (top+8, 0))]
        endpoints = set.union(*(record[0] for record in records))
        assert len(endpoints) == sum(len(record[0]) for record in records)
        for point in ((top+5, 1), (top+5, 6)):
            assert point in records[1][1] and point not in endpoints
        large += 1
    return dict(U_roles_excluded=checked_U, rotor_roles=checked_rotor,
                surviving_rotor_shapes_per_gate=[len(current) for current in survivors],
                every_distinct_gate_pair_collides=len(collisions), large_parameter_controls=large)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', contact_ledger=contact_controls(),
        three_original_obstruction=obstruction_controls(),
        scope='Finite controls supplement the general contact ledger and three-original '
              'nonextension proof; arbitrary orientations appear only in the gate-owner exclusion. '
              'No unrestricted global bound is asserted.'), indent=2))
