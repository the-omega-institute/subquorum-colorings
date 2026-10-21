"""Exact original-source controls for forced width-five stacks and their joint ledger."""

from collections import deque
import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_root_fourth_consumer import originals
from check_secondary_ten_root_sharp_staircase import check_case, sharp_dimensions
from check_secondary_ten_root_support_staircase import horizontal
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def rectangle(top, bottom, left, right):
    return {(row, column) for row in range(top, bottom+1)
            for column in range(left, right+1)}


def free_component(point, occupied):
    reached, queue = {point}, deque([point])
    while queue:
        current = queue.popleft()
        for adjacent in set(neighbors(current))-occupied-reached:
            reached.add(adjacent)
            queue.append(adjacent)
            assert len(reached) < 100000
    return reached


def make_prefix(origin, offset, widths, depths, breadth, consumer_far, dimensions,
                root_breadth=6, receiver_far=4):
    fixed, additions, sites = originals(origin, offset, widths, depths, root_breadth,
                                        root_breadth+2, receiver_far, breadth, consumer_far)
    stairs = [horizontal(origin, offset, widths[0], index, *parameters)
              for index, parameters in enumerate(dimensions)]
    records = fixed+additions+stairs
    return fixed, additions, records


def verify_stack(origin, offset, widths, depths, breadth, consumer_far, dimensions, heights,
                 root_breadth=6, receiver_far=4):
    old_width, width, depth = widths[0], widths[1], depths[0]
    assert dimensions[3] == [depth-2, old_width+width+18, dimensions[3][2]]
    assert all(height >= 6 and height % 2 == 0 for height in heights)
    assert sum(heights) == depth-2
    fixed, additions, records = make_prefix(origin, offset, widths, depths, breadth,
                                            consumer_far, dimensions, root_breadth, receiver_far)
    prefix = check_case(origin, offset, widths, depths, breadth, consumer_far, dimensions,
                        receiver_far, root_breadth, root_breadth+2)
    top, bottom, left = origin-12, origin+depth-15, offset-width-11
    cavity = rectangle(top, bottom, left, left+4)
    before = inventory(records)
    old_endpoints = set.union(*(record[0] for record in records))
    old_supports = set.union(*(record[1] for record in records))
    assert not cavity & old_endpoints
    assert cavity & old_supports == {(row, left) for row in range(top+1, bottom+1, 2)}
    boundary = set.union(*(set(neighbors(point))-cavity for point in cavity))
    assert boundary <= old_endpoints
    stack, bands = [], []
    current = bottom
    for height in heights:
        source = independent_source((height, 4, 4), (True, False, False), (current-height, left))
        band_top = current-height+1
        assert source[0] <= rectangle(band_top, current, left, left+4)
        assert charge(source) == 1-height
        tiles = {(row//2, column//2) for row, column in source[0]}
        inside_supports = {point for point in source[1] if (point[0]//2, point[1]//2) in tiles}
        assert len(source[2]) == height+3 and len(tiles) == height+4 and len(inside_supports) == 6
        stack.append(source)
        bands.append((band_top, current))
        current -= height
    assert current == top-1
    joined = records+stack
    after = inventory(joined)
    occupied = set.union(*(record[0] for record in joined))
    assert len(occupied) == sum(len(record[0]) for record in joined)
    owner = {point: index for index, record in enumerate(joined) for point in record[0]}
    missing = set.union(*(record[1] for record in joined))-occupied
    expected_missing = {(row, left+3) for band_top, band_bottom in bands
                        for row in (band_top+1, band_bottom-1)}
    assert cavity & missing == expected_missing
    all_occupied = occupied | missing
    assert all(len(set(neighbors(point)) & all_occupied) == 1 for point in expected_missing)
    assert all(set(neighbors(point)) <= cavity for point in expected_missing)
    assert set.union(*(record[1] for record in stack))-cavity <= occupied
    assert all(point in old_endpoints for record in stack for endpoint in record[0]
               for point in set(neighbors(endpoint))-cavity)
    for band_top, band_bottom in bands:
        notch = rectangle(band_top+1, band_bottom-1, left+2, left+4)
        assert free_component((band_top+1, left+2), occupied) == notch
    interfaces = {band_top-1 for band_top, band_bottom in bands if band_top != top}
    special_rows = {top-1, bottom} | interfaces
    expected_full = {(row//2, (left-1)//2) for row in range(top-1, bottom+1, 2)}
    expected_full |= {(row//2, column//2) for row in special_rows
                     for column in (left+1, left+3)}
    new_full = after['full']-before['full']
    assert before['full'] <= after['full'] and new_full == expected_full
    expected_events = set()
    parent_owner = len(fixed)
    next_P_owner = 9*len(widths)+2
    for row in range(top, bottom+1):
        inside, outside = (row, left), (row, left-1)
        expected_events.add((owner[inside], inside, outside))
        if row % 2:
            expected_events.add((parent_owner, outside, inside))
    for wall_row, inside_row, wall_owner in ((top-1, top, parent_owner),
                                              (bottom+1, bottom, next_P_owner)):
        for column in range(left, left+5):
            inside, outside = (inside_row, column), (wall_row, column)
            expected_events.add((wall_owner, outside, inside))
            if column in (left+1, left+3):
                expected_events.add((owner[inside], inside, outside))
    for row in interfaces:
        for column in (left+1, left+3):
            upper, lower = (row, column), (row+1, column)
            expected_events.add((owner[upper], upper, lower))
            expected_events.add((owner[lower], lower, upper))
    assert before['events'] <= after['events']
    assert after['events']-before['events'] == expected_events
    size, count = depth-2, len(heights)
    assert after['mass']-before['mass'] == size-count
    assert len(new_full) == size//2+2*count+3
    assert len(expected_events) == 3*size//2+4*count+10
    gain = phi_from(joined, after)-phi_from(records, before)
    assert gain == size//2-count-4 >= 4
    assert prefix['joint_gain']+gain >= breadth//2+11 >= 14
    return dict(depth=depth, heights=heights, prefix_gain=prefix['joint_gain'],
                stack_gain=gain, enlarged_gain=prefix['joint_gain']+gain,
                negative_mass=size-count, new_full_tiles=len(new_full),
                new_directed_events=len(expected_events), unconsumed_inside=len(expected_missing))


def corner_and_right_controls():
    accepted = right_exclusions = rotor_controls = 0
    for height_total in (6, 8, 22, 40):
        bottom, left = 40, -23
        top = bottom-height_total+1
        cavity = rectangle(top, bottom, left, left+4)
        for height in range(6, height_total+1, 2):
            seen = set()
            for symmetry in itertools.product((False, True), repeat=3):
                template = independent_source((height, 4, 4), symmetry, (0, 0))
                for endpoint in template[0]:
                    shift = (bottom-endpoint[0], left-endpoint[1])
                    source = independent_source((height, 4, 4), symmetry, shift)
                    if source[0] <= cavity:
                        seen.add(tuple(frozenset(part) for part in source))
            expected = {tuple(frozenset(part) for part in independent_source((height, 4, 4), symmetry,
                         (bottom-height, column)))
                        for symmetry, column in (((True, False, False), left),
                                                  ((True, True, False), left+4))}
            assert seen == expected and len(seen) == 2
            accepted += len(seen)
            right = independent_source((height, 4, 4), (True, True, False),
                                       (bottom-height, left+4))
            band_top = bottom-height+1
            notch = rectangle(band_top+1, bottom-1, left, left+2)
            outside_left = {(row, left-1) for row in range(band_top, bottom+1)}
            occupied = right[0] | outside_left
            point = (band_top+1, left)
            assert point not in occupied and point[0] % 2 == 0
            assert {(band_top, left), (band_top+1, left-1)} <= set(neighbors(point)) & occupied
            assert free_component(point, occupied) == notch
            right_exclusions += 1
        for symmetry in itertools.product((False, True), repeat=3):
            points = transform_module(rotor(), symmetry)['endpoints']
            for endpoint in points:
                shifted = {(row+bottom-endpoint[0], column+left-endpoint[1])
                           for row, column in points}
                assert not shifted <= cavity
                rotor_controls += 1
    return dict(normalized_U_corner_placements=accepted,
                right_bar_narrow_notches=right_exclusions, rotor_corner_exclusions=rotor_controls)


def height_partitions(total, generator):
    maximal = total//6
    choices = [[total], [6]*(maximal-1)+[total-6*(maximal-1)]]
    if total >= 12:
        choices += [[6, total-6], [total-6, 6]]
    for iteration in range(4):
        count = generator.randint(1, maximal)
        values = [6]*count
        for step in range((total-6*count)//2):
            values[generator.randrange(count)] += 2
        choices.append(values)
    return [list(values) for values in sorted({tuple(values) for values in choices})]


def stack_controls():
    generator = random.Random(2205)
    cases = []
    for origin, offset, width, depth in itertools.product((-33, 31), (-100, 200),
                                                          (12, 20), (24, 26, 40, 80)):
        dimensions = sharp_dimensions(12, width, depth, 6)
        dimensions[3][1] -= 4
        dimensions[3][2] -= 4
        for heights in height_partitions(depth-2, generator):
            cases.append(verify_stack(origin, offset, [12, width], [depth, 24], 6, 6,
                                      dimensions, heights))
    nonuniform = 0
    for attempt in range(3000):
        depth, width = generator.choice((24, 30, 40)), generator.choice((20, 30, 50))
        breadth = generator.choice((6, 8, 10))
        last = 12+width+18
        first = generator.randrange(12+breadth+14, last-5, 2)
        second = generator.randrange(first+2, last-3, 2)
        third = generator.randrange(second+2, last-1, 2)
        dimensions = [[generator.randrange(6, depth+index-4, 2), incident,
                       generator.randrange(4, width+12, 2)]
                      for index, incident in enumerate((first, second, third))]
        dimensions.append([depth-2, last, generator.randrange(4, width+8, 2)])
        consumer_far = generator.randrange(4, depth-7, 2)
        fixed, additions, records = make_prefix(31, 0, [12, width], [depth, 24],
                                                breadth, consumer_far, dimensions)
        if len(set.union(*(record[0] for record in records))) != sum(len(record[0]) for record in records):
            continue
        heights = height_partitions(depth-2, generator)[-1]
        cases.append(verify_stack(31, 0, [12, width], [depth, 24], breadth,
                                  consumer_far, dimensions, heights))
        nonuniform += 1
        if nonuniform == 32:
            break
    assert nonuniform == 32
    return cases, nonuniform


def simultaneous_controls():
    results = []
    for count in (2, 3, 5):
        pieces, stacks, footprints = [], [], []
        for index in range(count):
            depth, offset = 24+2*index, 2000*index
            dimensions = sharp_dimensions(12, 12, depth, 6)
            dimensions[3][1] -= 4
            dimensions[3][2] -= 4
            fixed, additions, records = make_prefix(31, offset, [12, 12], [depth, 24],
                                                    6, 6, dimensions)
            amount = (depth-2)//6
            heights = [6]*(amount-1)+[depth-2-6*(amount-1)]
            bottom, left = 31+depth-15, offset-23
            current_stack = []
            for height in heights:
                current_stack.append(independent_source((height, 4, 4),
                                      (True, False, False), (bottom-height, left)))
                bottom -= height
            cavity = rectangle(19, 31+depth-15, left, left+4)
            footprint = {(row//2, column//2) for row, column in cavity}
            assert all(not footprint & previous for previous in footprints)
            assert {(row//2, column//2) for source in current_stack
                    for row, column in source[0]} <= footprint
            pieces.append(records)
            stacks.append(current_stack)
            footprints.append(footprint)
        retained = [source for piece in pieces for source in piece]
        fresh = [source for stack in stacks for source in stack]
        before, after = inventory(retained), inventory(retained+fresh)
        expected_full, expected_events = set(), set()
        old_offset, new_offset = 0, len(retained)
        expected_gain = 0
        for piece, stack in zip(pieces, stacks):
            local_before, local_after = inventory(piece), inventory(piece+stack)
            current_full = local_after['full']-local_before['full']
            assert not current_full & expected_full
            expected_full |= current_full
            for owner, point, target in local_after['events']-local_before['events']:
                global_owner = old_offset+owner if owner < len(piece) else new_offset+owner-len(piece)
                expected_events.add((global_owner, point, target))
            expected_gain += phi_from(piece+stack, local_after)-phi_from(piece, local_before)
            old_offset += len(piece)
            new_offset += len(stack)
        assert after['full']-before['full'] == expected_full
        assert after['events']-before['events'] == expected_events
        actual_gain = phi_from(retained+fresh, after)-phi_from(retained, before)
        assert actual_gain == expected_gain >= 4*count
        results.append(dict(cavities=count, exact_gain=actual_gain,
                            full_tiles=len(expected_full), directed_events=len(expected_events)))
    return results


if __name__ == '__main__':
    corners = corner_and_right_controls()
    cases, nonuniform = stack_controls()
    print(json.dumps(dict(status='PASS', corner_controls=corners,
        exact_stack_controls=len(cases), nonuniform_actual_staircases=nonuniform,
        simultaneous_cavity_controls=simultaneous_controls(),
        minimum_stack_gain=min(case['stack_gain'] for case in cases),
        minimum_enlarged_gain=min(case['enlarged_gain'] for case in cases),
        extremal_controls=[case for case in cases if case['stack_gain'] == 4][:4],
        scope='Finite full-original controls supplement the general corner, recursive-trapping '
              'and joint-receipt proof. Exact cavity support closure is checked; no complete '
              'global extension, allocation of old prefix reserves or global grid bound is asserted.'), indent=2))
