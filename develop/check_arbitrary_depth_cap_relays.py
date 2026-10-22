"""Check arbitrary-depth frozen relays and exact horizontal access distance."""

import argparse
from collections import Counter, defaultdict
import heapq
import itertools
import json
from pathlib import Path

from check_terminal_cancellation_and_stranded_demand import (
    all_link_matchings, cancel_pairs, direct_family, extended_ports,
    inspect_extended, terminal_data, uniform_certificates,
)
from check_even_bridge_support_completion import endpoints_of
from check_native_guard_compensation import force_matching
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def relay_family(width, height, upper, lower):
    assert width >= 8 and height >= 4 and width % 2 == height % 2 == 0
    assert min(upper, lower) >= 1
    base = direct_family(width, height)
    selected, matching = set(base[2]), list(base[3])
    for row, sign, depth in ((5, -1, upper), (width+4, 1, lower)):
        selected.remove((row, 2))
        selected.update((row+sign, 3-2*index) for index in range(1, depth+1))
        selected.add((row, 2-2*depth))
        selected.update((row-sign, 4-2*index) for index in range(2, depth+1))
        selected.add((row-2*sign, 1))
        matching.extend(((row, 3-2*index), (row, 4-2*index))
                        for index in range(1, depth+1))
        matching.append(((row-sign, 2), (row-2*sign, 2)))
    shift = 2*max(upper, lower)
    move = lambda point: (point[0], point[1]+shift)
    current = (base[0], base[1]+shift, {move(point) for point in selected},
               [tuple(map(move, edge)) for edge in matching])
    bands = [[((row, column), (row+1, column))
              for column in range(height+6+shift)] for row in range(4, width+5, 2)]
    return current, bands, move


def serial_certificate(current, width, height, upper, lower, move, totals):
    base = direct_family(width, height)
    uniform_certificates(base, width, height, Counter())
    base_frozen, layers = frozen_certificate(base)
    assert base_frozen == endpoints_of(base)
    schedule = []
    for row, sign, depth in ((5, -1, upper), (width+4, 1, lower)):
        for index in range(depth, 0, -1):
            point = row, 3-2*index
            schedule.append((point, ((row+sign, point[1]), (row, point[1]-1))))
    schedule.extend((event['endpoint'], event['kept_neighbors'])
                    for layer in layers for event in layer)
    for row, sign, depth in ((5, -1, upper), (width+4, 1, lower)):
        schedule.extend([
            ((row-sign, 2), ((row, 2), (row-sign, 3))),
            ((row-2*sign, 2), ((row-2*sign, 1), (row-2*sign, 3))),
            ((row, 2), ((row, 3), (row-sign, 2))),
        ])
        for index in range(2, depth+1):
            column = 4-2*index
            schedule.append(((row, column), ((row-sign, column), (row, column+1))))
    mates = {point: other for edge in current[3] for point, other in (edge, edge[::-1])}
    frozen = set()
    for raw_point, raw_witnesses in schedule:
        point, witnesses = move(raw_point), [move(other) for other in raw_witnesses]
        assert point in mates and point not in frozen and len(set(witnesses)) == 2
        assert all(abs(point[0]-other[0])+abs(point[1]-other[1]) == 1
                   and other != mates[point] for other in witnesses)
        assert all(other in current[2] or mates[other] in frozen for other in witnesses)
        frozen.add(point)
    assert frozen == set(mates)
    totals['serial_freezing_events'] += len(schedule)


def shortest_access(row, start, kinds, pairs, choices, ports):
    adjacency = defaultdict(list)
    for first, second in pairs:
        if first[0] == second[0] == row:
            adjacency[first].append((second, 0))
            adjacency[second].append((first, 0))
    for first, second in choices:
        if first[0] == second[0] == row:
            adjacency[first].append((second, 1))
            adjacency[second].append((first, 1))
    distances, pending = {start: 0}, [(0, start)]
    while pending:
        distance, point = heapq.heappop(pending)
        if distance != distances[point]:
            continue
        for other, cost in adjacency[point]:
            if distance+cost < distances.get(other, float('inf')):
                distances[other] = distance+cost
                heapq.heappush(pending, (distance+cost, other))
    return min(distance for point, distance in distances.items()
               if kinds[point] == 'TP' and ports[point])


def control(width, height, upper, lower, totals, exhaustive=False):
    current, bands, move = relay_family(width, height, upper, lower)
    direct_check(*current)
    force_matching(current, totals)
    serial_certificate(current, width, height, upper, lower, move, totals)
    cells = {point for band in bands for column in band for point in column}
    endpoints = endpoints_of(current)
    assert current[2] | endpoints <= cells
    assert all((2*(row//2)+offset_row, 2*(column//2)+offset_column) in cells
               for row, column in endpoints
               for offset_row, offset_column in itertools.product((0, 1), repeat=2))
    depth, length = max(upper, lower), upper+lower
    assert len(current[2]) == height+9+2*length
    assert len(current[3]) == width+height+length+2
    surplus = width*height//2+2*width-height-5+depth*(width+2)-3*length
    budget = width+2
    margin = surplus-budget
    assert margin == (17+(width//2-4)*(height+2+2*depth)
                      +3*(height-4)+4*(depth-1)+3*(2*depth-length)) >= 17
    original, labels, intervals, owners, kinds, pairs, ports = terminal_data(current, bands)
    assert [original[key] for key in ('alpha', 'beta', 'gamma')] == [1, 0, height+1+length]
    assert original['surplus_twice'] == 2*surplus
    assert original['boundary_budget'] == budget
    extended = extended_ports(current, bands, labels, intervals, owners, kinds, ports, totals)
    for row, count, right in ((5, upper, 7), (width+4, lower, height+3)):
        row_tips = {point for point in kinds if point[0] == row and kinds[point] == 'TP'}
        assert all(not ports[point] for point in row_tips)
        assert {point for point in row_tips if extended[point]} == {
            move((row, 3-2*count)), move((row, right))}
    choices = [(first, second) for first in sorted(kinds) for second in sorted(kinds)
               if kinds[first] == 'TP' and kinds[second] == 'BP'
               and first[0] == second[0] and abs(first[1]-second[1]) == 1]
    minimum = min(upper, 2)+min(lower, height//2)
    assert sum(shortest_access(row, move((row, 3)), kinds, pairs, choices, extended)
               for row in (5, width+4)) == minimum
    optimal = []
    for row, left_depth, right_depth in ((5, upper, 2), (width+4, lower, height//2)):
        if left_depth <= right_depth:
            optimal.extend((move((row, 5-2*index)), move((row, 4-2*index)))
                           for index in range(1, left_depth+1))
        else:
            optimal.extend((move((row, 1+2*index)), move((row, 2+2*index)))
                           for index in range(1, right_depth+1))
    assert len(optimal) == minimum
    assert inspect_extended(current, bands, optimal, totals)['omitted'] == 0
    initial = inspect_extended(current, bands, [], totals)
    assert initial['omitted'] == 1 and initial['h0'] == margin+1
    links = [(move((row, 5-2*index)), move((row, 4-2*index)))
             for row, count in ((5, upper), (width+4, lower)) for index in range(1, count+1)]
    final = inspect_extended(current, bands, links, totals)
    assert final['alpha'] == 1 and final['beta'] == final['omitted'] == final.get('h2', 0) == 0
    assert final['h0'] == margin and final['margin_twice'] == 2*margin
    if exhaustive:
        best = float('inf')
        for selected_links in all_link_matchings(choices):
            reduced, inventory, _ = cancel_pairs(kinds, pairs, selected_links, totals)
            assert inventory['TP', 'TP'] == 1 and inventory['BP', 'BP'] == 0
            alpha = next(pair for pair in reduced if all(kinds[point] == 'TP' for point in pair))
            if all(extended[point] for point in alpha):
                best = min(best, len(selected_links))
            totals['exhaustive_horizontal_matchings'] += 1
        assert best == minimum
        totals['exhaustive_parameter_tuples'] += 1
    totals['parameter_tuples'] += 1
    return dict(parameters=[width, height, upper, lower], selected=len(current[2]),
                matching=len(current[3]), surplus=surplus, boundary_budget=budget,
                minimum_access_links=minimum, initial=initial, compensated=final)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    for parameters in itertools.product((8, 10, 16), (4, 6, 10), (1, 2, 5), (1, 3, 6)):
        control(*parameters, totals)
    for parameters in ((8, 4, 1, 1), (8, 6, 2, 1), (8, 8, 1, 2)):
        examples.append(control(*parameters, totals, exhaustive=True))
    for length in (3, 4, 8, 16, 32, 64):
        record = control(8, 2*length, length, length, totals)
        assert record['minimum_access_links'] == length+2
        assert record['surplus'] == 10*length+11
        examples.append(record)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals),
        examples=examples, scope='Finite checks support the written all-parameter proof; '
        'they do not establish the universal grid inequality.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
