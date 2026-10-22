"""Exact original-record controls for full-height U families in six rows."""

import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_gap_axial_compensation import baseline, make_source, transform
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def transverse(bar, direction, near, far, height=6):
    assert direction in (-1, 1)
    assert height >= 6 and height % 2 == 0
    assert min(near, far) >= 4 and near % 2 == far % 2 == 0
    original = independent_source((height, near, far), (False, False, False), (0, 0))
    return transform(original, lambda point: (
        height-point[1], bar+point[0] if direction == 1 else bar+1-point[0]))


def inspect(specifications, height=6):
    records = [transverse(*specification, height=height) for specification in specifications]
    receipt = inventory(records)
    aligned = sum(bar % 2 == 0 for bar, direction, near, far in specifications)
    unaligned = len(records)-aligned
    paired = set()
    full = set()
    pair_events = set()
    pairs = []
    for first, second in itertools.combinations(range(len(records)), 2):
        left, right = sorted((first, second), key=lambda owner: specifications[owner][0])
        left_bar, left_direction, _, _ = specifications[left]
        right_bar, right_direction, _, _ = specifications[right]
        assert right_bar >= left_bar+2
        if right_bar != left_bar+2:
            continue
        assert left_direction == -1 and right_direction == 1
        if left_bar % 2 == 0:
            continue
        assert not {left, right} & paired
        paired |= {left, right}
        pairs.append((left, right))
        column = left_bar+1
        full |= {(row, column//2) for row in range(height//2)}
        pair_events |= {(left, (row, column), (row, column+1)) for row in range(height)}
        pair_events |= {(right, (row, column+1), (row, column)) for row in range(height)}
    assert receipt['full'] == full
    assert pair_events <= receipt['events']
    other_events = receipt['events']-pair_events
    labels = set()
    for owner, point, target in other_events:
        bar, direction, _, _ = specifications[owner]
        assert bar % 2 == 1 and owner not in paired
        assert point[0] in (0, height-1) and target[0] == point[0]
        assert point[1] == (bar if direction == 1 else bar+1)
        assert target[1] == point[1]-direction
        foreign = [index for index, record in enumerate(records) if target in record[0]]
        assert len(foreign) == 1 and point in records[foreign[0]][1]
        assert (owner, point[0]) not in labels
        labels.add((owner, point[0]))
    assert len(other_events) <= 2*(unaligned-len(paired))
    for record, (bar, direction, near, far) in zip(records, specifications):
        half_depth = (near+far)//2
        tiles = {(row//2, column//2) for row, column in record[0]}
        inside = {point for point in record[1] if (point[0]//2, point[1]//2) in tiles}
        assert len(record[2]) == height-1+half_depth
        assert len(tiles) == (height//2 if bar % 2 == 0 else height-2)+half_depth
        assert len(inside) == half_depth-2*(bar % 2)
        assert charge(record) == (1-height if bar % 2 else -1)
    value = phi_from(records, receipt)
    assert value == aligned+(height-1)*unaligned-height*len(pairs)-len(other_events)
    assert value >= aligned+(height-3)*unaligned-(height-4)*len(pairs)
    assert 2*value >= 2*aligned+(height-2)*unaligned
    assert value >= aligned+2*unaligned
    return dict(sources=len(records), aligned=aligned, unaligned=unaligned,
                adjacent_unaligned_pairs=len(pairs), other_events=len(other_events), Phi=value)


def pair_specs(width, lower_left, upper_left, offset=0):
    assert width >= 10 and width % 2 == offset % 2 == 0
    return [(offset, 1, lower_left, upper_left),
            (offset+width-2, -1, width-2-lower_left, width-2-upper_left)]


def complete_controls():
    checked = 0
    for width in (10, 12, 16, 24, 60, 2000):
        choices = sorted({4, width-6, 2*((width-2)//4)})
        for lower, upper in itertools.product(choices, repeat=2):
            specifications = pair_specs(width, lower, upper)
            result = inspect(specifications)
            assert result['Phi'] == 2
            outer_width = width+2
            old = baseline(outer_width, (2, 12), 20)
            core = old+[shift(make_source('U', outer_width, 4, 4), (2, 0))]
            records = core+[shift(transverse(*specification), (4, 2))
                            for specification in specifications]
            endpoints = set.union(*(record[0] for record in records))
            supports = set.union(*(record[1] for record in records))-endpoints
            occupied = endpoints | supports
            pocket = {(row, column) for row in range(4, 10) for column in range(2, outer_width)}
            assert all(len(set(neighbors(point)) & occupied) == 1
                       for point in supports & pocket)
            assert phi_from(records, inventory(records))-phi_from(old, inventory(old)) == 7
            checked += 1
    for amount in (1, 2, 3, 8, 30):
        specifications = [specification for index in range(amount)
                          for specification in pair_specs(10, 4, 4, 10*index)]
        assert inspect(specifications)['Phi'] == 2*amount
        checked += 1
    return checked


def parallel_height_controls():
    checked = 0
    for height in (6, 8, 10, 20, 2000):
        for bar, direction, near, far in itertools.product((-3, 0, 3), (-1, 1), (4, 10), (4, 12)):
            inspect([(bar, direction, near, far)], height)
            checked += 1
        assert inspect([(-3, -1, 4, 8), (-1, 1, 6, 10)], height)['Phi'] == height-2
        assert inspect([(0, 1, 4, 8), (12, 1, 6, 10)], height)['Phi'] == 2
        assert inspect([(0, 1, 4, 4), (5, 1, 4, 4)], height)['other_events'] == 2
        checked += 3
    return checked


def singleton_controls():
    checked = 0
    for width in (6, 8, 10, 14, 20):
        old = baseline(width+2, (2, 12), 20)
        core = old+[shift(make_source('U', width+2, 4, 4), (2, 0))]
        fixed_endpoints = set.union(*(record[0] for record in core))
        fixed_supports = set.union(*(record[1] for record in core))-fixed_endpoints
        for bar, direction, near, far in itertools.product(
                range(width-1), (-1, 1), range(4, width, 2), range(4, width, 2)):
            record = transverse(bar, direction, near, far)
            if not all(0 <= column < width for row, column in record[0]):
                continue
            tip = bar+far if direction == 1 else bar+1-far
            support_column = tip+direction
            witness = (0, support_column) if 0 <= support_column < width else (1, tip)
            moved = shift(record, (4, 2))
            point = witness[0]+4, witness[1]+2
            endpoints = fixed_endpoints | moved[0]
            supports = (fixed_supports | moved[1])-endpoints
            assert point in supports
            assert len(set(neighbors(point)) & endpoints) >= 2
            checked += 1
    return checked


def main():
    candidates = [(bar, direction, near, far)
                  for bar, direction, near, far in itertools.product(
                      range(-8, 19), (-1, 1), (4, 6, 10), (4, 8))]
    records = [transverse(*specification) for specification in candidates]
    pairs = 0
    event_examples = {}
    for first, second in itertools.combinations(range(len(records)), 2):
        if records[first][0] & records[second][0]:
            continue
        result = inspect([candidates[first], candidates[second]])
        event_examples.setdefault((result['adjacent_unaligned_pairs'], result['other_events']),
                                  dict(specifications=[candidates[first], candidates[second]], **result))
        pairs += 1
    generator = random.Random(20261022)
    batches = 0
    for attempt in range(100):
        specifications = []
        occupied = set()
        for index in generator.sample(range(len(candidates)), len(candidates)):
            if not occupied & records[index][0]:
                specifications.append(candidates[index])
                occupied |= records[index][0]
        inspect(specifications)
        batches += 1
    sharp_unaligned = [(-3, -1, 4, 8), (-1, 1, 6, 10)]
    assert inspect(sharp_unaligned)['Phi'] == 4
    print(json.dumps(dict(status='PASS', disjoint_pair_controls=pairs,
                         greedy_batches=batches, event_examples=list(event_examples.values()),
                         complete_opposed_pair_controls=complete_controls(),
                         parallel_even_height_controls=parallel_height_controls(),
                         forbidden_singleton_controls=singleton_controls(),
                         sharp_unaligned_pair=inspect(sharp_unaligned),
                         scope='Exact full-record original charge, mixed-tile and labelled-event sets. '
                         'Unbounded theorem separately written. All new sources are full-height '
                         'transverse U; no claim for horizontal U/rotor or arbitrary complete pockets.'), indent=2))


if __name__ == '__main__':
    main()
