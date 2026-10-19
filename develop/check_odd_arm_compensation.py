"""Physical controls for single-square odd arms and transported donor budgets."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import all_oriented_bundles, frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def odd_arms(length_parameters):
    north, east, south, west = [2*value+1 for value in length_parameters]
    selected = set()
    matching = []
    paths = [([(0, 0)]+[(-index, 0) for index in range(1, north+1)],
              [(-index, -1 if index % 2 else 1) for index in range(1, north+1)],
              (-north-1, 0)),
             ([(0, 1)]+[(0, 1+index) for index in range(1, east+1)],
              [(-1 if index % 2 else 1, 1+index) for index in range(1, east+1)],
              (0, east+2)),
             ([(1, 1)]+[(1+index, 1) for index in range(1, south+1)],
              [(1+index, 2 if index % 2 else 0) for index in range(1, south+1)],
              (south+2, 1)),
             ([(1, 0)]+[(1, -index) for index in range(1, west+1)],
              [(2 if index % 2 else 0, -index) for index in range(1, west+1)],
              (1, -west-1))]
    for path, supports, axial in paths:
        selected.update(supports)
        selected.add(axial)
        matching.extend(zip(path[::2], path[1::2]))
    offset = (north+3, west+3)
    move = lambda vertex: (vertex[0]+offset[0], vertex[1]+offset[1])
    rows, columns = north+south+8, west+east+8
    return (rows, columns, {move(vertex) for vertex in selected},
            [(move(first), move(second)) for first, second in matching])


def verify(current, parameters):
    total = sum(parameters)
    assert direct_check(*current) == 3*total+12
    endpoints, adjacency, squares = endpoint_data(current)
    assert len(endpoints) == 2*total+8 and len(squares) == 1
    origin = next(iter(squares))
    assert all(coordinate % 2 == 0 for coordinate in origin)
    center = origin[0]//2, origin[1]//2
    square_vertices = {(origin[0]+row, origin[1]+column)
                       for row, column in itertools.product(range(2), repeat=2)}
    assert sum(first in square_vertices and second in square_vertices
               for first, second in current[3]) == 0
    visited = {next(iter(endpoints))}
    pending = list(visited)
    while pending:
        vertex = pending.pop()
        added = adjacency[vertex]-visited
        visited.update(added)
        pending.extend(added)
    assert visited == endpoints
    assert set(occupied_degrees(current).values()) == {3}
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    graph, _ = graph_record(*current)
    receiver = {(row//2, column//2) for row, column in endpoints}
    assert len(receiver) == total+5
    counts = {'center': 0, 'neutral': 0, 'donor': 0}
    twice_charge = 0
    donors = set()
    for tile in receiver:
        index = tile[0]*(current[1]//2)+tile[1]
        chosen = graph['t'][index]
        present = sum((2*tile[0]+row, 2*tile[1]+column) in endpoints
                      for row, column in itertools.product(range(2), repeat=2))
        assert graph['s'][index] == graph['h'][index] == 0
        if tile == center:
            assert (chosen, present, graph['r'][index], graph['deg'][index]) == (0, 4, 2, 4)
            counts['center'] += 1
        elif present == 2:
            assert chosen == 1
            counts['neutral'] += 1
        else:
            assert (chosen, present) == (1, 1)
            counts['donor'] += 1
            donors.add(tile)
        twice_charge += 2*chosen+present+graph['s'][index]-4
    assert counts == dict(center=1, neutral=total, donor=4)
    assert twice_charge == -4
    selected_inside = {vertex for vertex in current[2]
                       if (vertex[0]//2, vertex[1]//2) in receiver}
    assert len(selected_inside) == total+4
    assert len(current[2]) == 2*total+8
    assert sorted(abs(tile[0]-center[0])+abs(tile[1]-center[1]) for tile in donors) == sorted(value+1 for value in parameters)
    if min(parameters) >= 1:
        assert all((center[0]+row, center[1]+column) not in donors
                   for row, column in ((-1, 0), (0, 1), (1, 0), (0, -1)))
    return dict(parameters=list(parameters), shape=list(current[:2]),
                receiver_tiles=len(receiver), matching=len(current[3]),
                frozen_rounds=len(layers), charge_twice=twice_charge,
                donor_tile_distances=sorted(value+1 for value in parameters)), receiver


def packing_control():
    first = odd_arms((1, 2, 3, 4))
    second = odd_arms((4, 1, 2, 3))
    offset = first[1]+4
    selected = first[2] | {(row, column+offset) for row, column in second[2]}
    matching = first[3]+[((left[0], left[1]+offset), (right[0], right[1]+offset))
                         for left, right in second[3]]
    current = max(first[0], second[0]), offset+second[1], selected, matching
    assert direct_check(*current) == 84
    assert frozen_certificate(current)[0] == endpoint_data(current)[0]
    _, first_receiver = verify(first, (1, 2, 3, 4))
    _, second_receiver = verify(second, (4, 1, 2, 3))
    second_receiver = {(row, column+offset//2) for row, column in second_receiver}
    assert not first_receiver & second_receiver
    graph, _ = graph_record(*current)
    charge_twice = 0
    for row, column in first_receiver | second_receiver:
        index = row*(current[1]//2)+column
        charge_twice += graph['deg'][index]-2*graph['r'][index]
    assert charge_twice == -8
    return dict(components=2, receiver_tiles=len(first_receiver | second_receiver), charge_twice=charge_twice)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    parameters = sorted(set(itertools.product(range(4), repeat=4)) |
                        {(size, size, size, size) for size in range(17)} |
                        {(0, 1, 7, 15), (9, 0, 3, 1)})
    records = []
    images = bundles = 0
    for values in parameters:
        current = odd_arms(values)
        record, _ = verify(current, values)
        records.append(record)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            verify((*shape, selected, matching), values)
            images += 1
        if sum(values) <= 2:
            candidates, feasible = all_oriented_bundles(current)
            assert feasible == 0
            bundles += candidates
    report = dict(status='ALL_CHECKS_PASSED', cases=len(records), symmetry_images=images,
                  oriented_bundles_checked=bundles, examples=records,
                  separated_receivers=packing_control(),
                  scope='Finite physical controls of the written all-length theorem; no general coverage or full formalization claim.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'examples'}))


if __name__ == '__main__':
    main()
