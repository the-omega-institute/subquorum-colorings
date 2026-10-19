"""Independent physical controls for adaptive, exclusive strip compensation."""

import argparse
from collections import deque
import itertools
import json
from pathlib import Path

from check_coalesced_mouths import move_source
from check_component_receivers import vertices_of
from check_frozen_end_locality_obstacle import build as locality_obstacle
from check_mixed_source_contacts import source_with_chamber
from check_orthogonal_source_mouths import (
    crossing_family, crossing_grid, fill_greedily, inspect, strips_of,
)
from check_owned_donors import endpoint_data
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def maximum_strip_certificate(weights, horizontal, edges, capacities=None):
    count = len(weights)
    source, sink = count, count+1
    residual = [[0]*(count+2) for _ in range(count+2)]
    infinite = sum(weights)+1
    if capacities is None:
        capacities = [infinite]*len(edges)
    assert len(capacities) == len(edges) and all(capacity >= 0 for capacity in capacities)
    for index, weight in enumerate(weights):
        assert weight >= 0
        if horizontal[index]:
            residual[source][index] = weight
        else:
            residual[index][sink] = weight
    for (first, second), capacity in zip(edges, capacities):
        assert horizontal[first] and not horizontal[second]
        residual[first][second] = capacity
    flow = 0
    while True:
        parents = {source: None}
        queue = deque([source])
        while queue and sink not in parents:
            first = queue.popleft()
            for second, capacity in enumerate(residual[first]):
                if capacity and second not in parents:
                    parents[second] = first
                    queue.append(second)
        if sink not in parents:
            break
        amount, second = infinite, sink
        while second != source:
            first = parents[second]
            amount = min(amount, residual[first][second])
            second = first
        second = sink
        while second != source:
            first = parents[second]
            residual[first][second] -= amount
            residual[second][first] += amount
            second = first
        flow += amount
    chosen = {index for index in range(count)
              if (index in parents) == horizontal[index]}
    penalty = sum(capacity for (first, second), capacity in zip(edges, capacities)
                  if first in chosen and second in chosen)
    value = sum(weights[index] for index in chosen)-penalty
    assert value == sum(weights)-flow
    shared_flow = [(first, second, residual[second][first]) for first, second in edges
                   if residual[second][first]]
    assert sum(amount for first, second, amount in shared_flow) == flow
    assert all(residual[second][first] <= capacity
               for (first, second), capacity in zip(edges, capacities))
    for index, weight in enumerate(weights):
        assert sum(amount for first, second, amount in shared_flow
                   if index in (first, second)) <= weight
    return value, chosen, shared_flow


def maximum_independent_certificate(weights, horizontal, edges):
    value, chosen, shared_flow = maximum_strip_certificate(weights, horizontal, edges)
    cover = set(range(len(weights)))-chosen
    assert all(first not in chosen or second not in chosen for first, second in edges)
    assert all(first in cover or second in cover for first, second in edges)
    assert value == sum(weights[index] for index in chosen)
    assert sum(weights[index] for index in cover) == sum(amount for _, _, amount in shared_flow)
    return value, chosen, shared_flow


def certificate(current, sources):
    physical = inspect(current, sources)
    strips = strips_of(sources)
    horizontal = [strip['horizontal'] for strip in strips]
    weights = []
    for strip, record in zip(strips, physical['strips_data']):
        assert record['parallel_tips'] == 2*len(strip['members'])-2
        weights.append(max(0, 2*len(strip['members'])+record['comb_flux']))
        assert record['physical_payment'] >= weights[-1]
    edges = [(first, second) for first, second in itertools.product(range(len(strips)), repeat=2)
             if horizontal[first] and not horizontal[second]
             and strips[first]['tiles'] & strips[second]['tiles']]
    value, chosen, shared_flow = maximum_independent_certificate(weights, horizontal, edges)
    if len(strips) <= 16:
        exhaustive = max(sum(weights[index] for index in range(len(strips)) if mask >> index & 1)
                         for mask in range(1 << len(strips))
                         if all(not (mask >> first & 1 and mask >> second & 1)
                                for first, second in edges))
        assert exhaustive == value
    claimed = set()
    endpoints = endpoint_data(current)[0]
    claimed_payment = 0
    for index in sorted(chosen):
        donors = {tile for tile in strips[index]['tiles'] if not vertices_of({tile}) & endpoints}
        assert not donors & claimed
        claimed.update(donors)
        claimed_payment += sum(2-len(vertices_of({tile}) & current[2]) for tile in donors)
    assert value <= claimed_payment <= physical['physical_union_payment']
    assert physical['half_area_deficit'] >= value-len(sources)+physical['outside_remainder']
    if value >= len(sources):
        assert physical['half_area_deficit'] >= 0
    global_direction = max(sum(weight for index, weight in enumerate(weights) if horizontal[index]),
                           sum(weight for index, weight in enumerate(weights) if not horizontal[index]))
    adjacency = {index: set() for index in range(len(strips))}
    for first, second in edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    unvisited, components = set(adjacency), []
    while unvisited:
        start = min(unvisited)
        unvisited.remove(start)
        component, queue = {start}, [start]
        while queue:
            for following in adjacency[queue.pop()] & unvisited:
                unvisited.remove(following)
                component.add(following)
                queue.append(following)
        components.append(component)
    component_direction = sum(max(sum(weights[index] for index in component if horizontal[index]),
                                  sum(weights[index] for index in component if not horizontal[index]))
                              for component in components)
    assert global_direction <= component_direction <= value
    return dict(sources=len(sources), combs=physical['combs'], strips=len(strips),
                crossing_components=len(components), crossing_edges=len(edges), weights=weights,
                chosen_strips=sorted(chosen), independent_weight=value,
                cover_strips=sorted(set(range(len(strips)))-chosen),
                shared_flow=shared_flow,
                global_direction_bound=global_direction, component_direction_bound=component_direction,
                weighted_comb_flux=physical['weighted_comb_flux'],
                old_crossing_criterion=physical['effective_crossing_loss']+physical['outward'] <=
                                       len(sources)+physical['inward'],
                coefficient_one_certified=value >= len(sources),
                physical_claimed_payment=claimed_payment, physical=physical)


def negative_star(horizontal_count):
    assert horizontal_count >= 2
    current, sources = crossing_grid(horizontal_count, 1)
    tip, column = 8*horizontal_count+8, 4*horizontal_count+2
    selected = set(current[2]) | {(tip-4, column), (tip+1, column)}
    selected.update((row, column+(1 if (row-tip) % 2 else -1)) for row in range(tip-3, tip+1))
    matching = current[3]+[((row, column), (row+1, column)) for row in range(tip-3, tip, 2)]
    return (*current[:2], selected, matching), sources


def negative_forest(count):
    assert count >= 1
    selected, matching, sources = set(), [], []
    baseline, original = negative_star(2)
    for index in range(count):
        transpose = bool(index % 2)
        shape, moved_selected, moved_matching = transformed(*baseline, transpose, False, False)
        assert max(shape) <= 46
        move = lambda point, index=index: (point[0]+2, point[1]+2+50*index)
        selected.update(move(point) for point in moved_selected)
        matching.extend(tuple(move(point) for point in edge) for edge in moved_matching)
        sources.extend(move_source(source,
                       lambda point, move=move, transpose=transpose:
                           move((point[1], point[0]) if transpose else point)) for source in original)
    return (50, 50*count, selected, matching), sources


def symmetry_controls(current, sources, expected):
    for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
        def move(point):
            row, column = point
            row = current[0]-1-row if vertical else row
            column = current[1]-1-column if horizontal else column
            return (column, row) if transpose else (row, column)
        record = certificate((*shape, selected, matching), [move_source(source, move) for source in sources])
        assert record['independent_weight'] == expected
    return 8


def controls():
    records, images = [], 0
    for count in (*range(2, 11), 16, 24):
        current, sources = negative_star(count)
        for seed in (None, 0, 7):
            filled = current if seed is None else fill_greedily(current, sources, seed)
            record = certificate(filled, sources)
            assert record['weighted_comb_flux'] == -1
            assert record['independent_weight'] == 2*count-1
            assert record['crossing_components'] == 1 and record['crossing_edges'] == count
            assert record['coefficient_one_certified']
            if seed is None:
                assert not record['old_crossing_criterion']
                assert record['physical']['effective_crossing_loss'] == 2*count
            records.append(dict(kind='negative_star', count=count, seed=seed, result=record))
        if count in (2, 5):
            images += symmetry_controls(current, sources, 2*count-1)
    smallest = None
    for count in (1, 2, 3, 4, 6, 8, 12):
        current, sources = negative_forest(count)
        for seed in (None, 3):
            filled = current if seed is None else fill_greedily(current, sources, seed)
            record = certificate(filled, sources)
            assert record['weighted_comb_flux'] == -count
            assert record['independent_weight'] == 3*count
            assert record['crossing_components'] == count and record['crossing_edges'] == 2*count
            assert record['coefficient_one_certified']
            if count % 2 == 0:
                assert 2*record['global_direction_bound'] == 5*count < 6*count
            if seed is None:
                assert not record['old_crossing_criterion']
            records.append(dict(kind='negative_forest', count=count, seed=seed, result=record))
        if count in (2, 3):
            images += symmetry_controls(current, sources, 3*count)
        if count == 2:
            smallest = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                            sources=[{key: value if key == 'matching' else sorted(value)
                                      for key, value in source.items()} for source in sources],
                            result=certificate(current, sources))
    for first, second in itertools.product((1, 2, 3, 5), repeat=2):
        current, sources = crossing_grid(first, second)
        records.append(dict(kind='source_only_dense', horizontal=first, vertical=second,
                            result=certificate(current, sources)))
    current, sources = crossing_family(22, filled=True)
    records.append(dict(kind='three_unit_obstacle', result=certificate(current, sources)))
    for radius in (1, 2, 4, 8, 16, 40):
        current, _, _, _ = locality_obstacle(radius)
        sources = [source_with_chamber(4*radius+14, 2*radius+3)]
        record = certificate(current, sources)
        assert record['weighted_comb_flux'] == -2
        assert record['independent_weight'] == 0 and not record['coefficient_one_certified']
        assert record['physical']['half_area_deficit'] > 0
        records.append(dict(kind='known_end_locality_limit', radius=radius, result=record))
    abstract_graphs = 0
    edges = list(itertools.product(range(3), range(3, 6)))
    for edge_mask in range(1 << len(edges)):
        present = [edge for index, edge in enumerate(edges) if edge_mask >> index & 1]
        for weights in ([0, 1, 3, 2, 0, 4], [3, 1, 2, 1, 3, 2]):
            value, _, _ = maximum_independent_certificate(weights, [True]*3+[False]*3, present)
            exhaustive = max(sum(weight for index, weight in enumerate(weights) if mask >> index & 1)
                             for mask in range(64)
                             if all(not (mask >> first & 1 and mask >> second & 1)
                                    for first, second in present))
            assert value == exhaustive
            abstract_graphs += 1
    mixed_value, mixed_chosen, _ = maximum_independent_certificate(
        [3, 1, 1, 3], [True, True, False, False], [(0, 2), (1, 2), (1, 3)])
    assert mixed_value == 6 and mixed_chosen == {0, 3}
    assert any(record['result']['weighted_comb_flux'] < 0 and
               not record['result']['old_crossing_criterion'] and
               record['result']['coefficient_one_certified'] for record in records)
    return dict(status='ALL_CHECKS_PASSED', cases=len(records), symmetry_images=images,
                abstract_bipartite_graph_controls=abstract_graphs,
                negative_flux_cases=sum(record['result']['weighted_comb_flux'] < 0 for record in records),
                uncertified_limit_cases=sum(not record['result']['coefficient_one_certified'] for record in records),
                records=records, two_component_witness=smallest,
                scope='Physical checks of a separately proved exclusive-strip lemma and bipartite '
                      'maximum-weight certificate. Explicit all-count negative-flux star/forest '
                      'families have symbolic proofs. Min-cut outputs have independently checked '
                      'covers and exclusive donor ownership; small graphs also use exhaustive '
                      'independent-set checks. No universal negative-flux or grid theorem is claimed.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in
                      ('status', 'cases', 'symmetry_images', 'negative_flux_cases',
                       'uncertified_limit_cases', 'abstract_bipartite_graph_controls')}))


if __name__ == '__main__':
    main()
