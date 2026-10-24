"""Check exact endpoint-dependent repair costs in frozen reflected packets."""

import argparse
from collections import Counter, defaultdict, deque
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory
from check_full_domain_marker_compensation import full_signs
from check_native_guard_compensation import force_matching
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    components, direct_family, terminal_data, uniform_certificates,
)


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def family(width, depth, tail):
    assert width >= 6 and tail >= 4 and width % 2 == tail % 2 == 0 and depth >= 1
    shift = 2*depth+tail
    selected, actual, owners, bases = set(), [], {}, []
    for owner, (size, height, vertical, horizontal, reflect) in enumerate([
        (width, 4, 0, 0, False), (width+2, tail, -1, -2*depth-5, True),
        (width+2, 4, -1, 2*depth+5, False),
    ]):
        base = direct_family(size, height)

        def move(point):
            return point[0]+vertical, (10-point[1] if reflect else point[1])+horizontal+shift

        following = {move(point) for point in base[2]}
        endpoints = {move(point) for edge in base[3] for point in edge}
        assert not (following | endpoints) & (selected | set(owners))
        selected.update(following)
        actual.extend(tuple(map(move, edge)) for edge in base[3])
        owners.update({point: owner for point in endpoints})
        bases.append((base, size, height))
    for row, opposite in [(5, 4), (width+4, width+5)]:
        for step in range(1, 2*depth+1):
            selected.add((opposite if step % 2 else row, 2-2*depth+step+shift))
            selected.add((row if step % 2 else opposite, 7+step+shift))
    current = width+12, 4*depth+tail+16, selected, actual
    bands = [[((row, column), (row+1, column)) for column in range(current[1])]
             for row in range(2, width+7, 2)]
    return current, bands, owners, bases, shift


def candidate_graph(current, bands, labels, vertices):
    edges, portals = set(), {}
    for first in vertices:
        for vertical, horizontal in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            second = first[0]+vertical, first[1]+horizontal
            if second in vertices:
                edges.add(frozenset((first, second)))
    for band, columns in enumerate(bands):
        position = 0
        while position < len(columns):
            if 'P' in labels[band][position]:
                position += 1
                continue
            start = position
            while position < len(columns) and 'P' not in labels[band][position]:
                position += 1
            if start == 0 or position == len(columns):
                continue
            if all(sorted(labels[band][column]) == ['B', 'T']
                   for column in range(start, position)):
                cells = {point for column in columns[start:position] for point in column}
                assert not cells & vertices and 2*len(cells & current[2]) == len(cells)
                for first in set(columns[start-1]) & vertices:
                    for second in set(columns[position]) & vertices:
                        edge = frozenset((first, second))
                        assert edge not in portals
                        portals[edge] = cells
                        edges.add(edge)
    adjacency = defaultdict(set)
    for edge in edges:
        first, second = tuple(edge)
        adjacency[first].add(second)
        adjacency[second].add(first)
    return edges, portals, adjacency


def shortest_walks(source, donors, adjacency, mate):
    reached, pending, results = {source}, deque([(source, (source,), 0)]), {}
    while pending:
        cursor, route, cost = pending.popleft()
        for target in sorted(adjacency[cursor]):
            if target in donors:
                results.setdefault(target, (cost+1, route+(target,)))
            elif target in mate and mate[target] not in reached:
                reached.add(mate[target])
                pending.append((mate[target], route+(target, mate[target]), cost+1))
    return results


def repair_paths(width, tail, outer, shift):
    lower, bottom = width+4, width+5
    source_upper, source_lower = (5, 3+shift), (lower, 3+shift)
    target_upper, target_lower = (4, outer-2), (bottom, outer-tail)
    upper = [source_upper, (4, outer), (5, outer), (5, outer-1),
             (4, outer-1), target_upper]
    vertical = [source_lower, (lower, outer), (bottom, outer),
                (bottom, outer-1), (lower, outer-1)]
    for row in range(lower, 5, -2):
        vertical.extend([(row-1, outer-1), (row-2, outer-1)])
    vertical.append(target_upper)
    horizontal = [source_lower, (bottom, outer), (lower, outer),
                  (lower, outer-1), (bottom, outer-1)]
    for step in range(1, tail):
        row, opposite = (bottom, lower) if step % 2 else (lower, bottom)
        horizontal.append((row, outer-step-1))
        if step < tail-1:
            horizontal.append((opposite, outer-step-1))
    assert horizontal[-1] == target_lower
    return [('upper', upper, 3), ('lower_vertical', vertical, width//2+3),
            ('lower_horizontal', horizontal, tail+1)]


def check_repair(current, auxiliary, kinds, edges, portals, route, expected, totals):
    vertices = {point for edge in current[3] for point in edge}
    assert len(route) == len(set(route))
    added = list(zip(route[::2], route[1::2]))
    removed = {frozenset(edge) for edge in zip(route[1:-1:2], route[2:-1:2])}
    old = {frozenset(edge) for edge in auxiliary}
    assert removed <= old and len(removed) == expected-1 and len(added) == expected
    assert all(frozenset(edge) in edges-old for edge in added)
    assert frozenset(added[0]) in portals
    assert all(frozenset(edge) not in portals for edge in added[1:])
    following = [edge for edge in auxiliary if frozenset(edge) not in removed]+added
    source, donor = route[0], route[-1]
    covered = [point for edge in following for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == set(vertices)-set(kinds) | {source, donor}
    assert {frozenset(edge) for edge in following}-old == {frozenset(edge) for edge in added}
    signs, cycles, markers = full_signs(vertices, current[3], auxiliary, kinds, {source, donor}, {})
    assert not markers
    boundary_cycle = next(cycle for cycle in cycles if route[1] in cycle)
    assert boundary_cycle == {route[1], route[2]}
    if signs[route[1]] != 1:
        signs.update({point: -signs[point] for point in boundary_cycle})
    assert all(signs[first]+signs[second] == 0 for first, second in following)
    records = components(vertices, current[3]+following)
    final = inventory(records, {point: kind for point, kind in kinds.items()
                                if point not in {source, donor}})
    assert (final['alpha'], final['beta'], final['mixed']) == (0, 1, 8)
    totals['complete_coherent_repairs'] += 1
    totals['new_auxiliary_edges'] += len(added)
    totals['deleted_auxiliary_edges'] += len(removed)


def control(width, depth, tail, totals):
    current, bands, owners, bases, shift = family(width, depth, tail)
    direct_check(*current)
    force_matching(current, totals)
    for base, size, height in bases:
        uniform_certificates(base, size, height, totals)
    vertices = set(owners)
    original, labels, _, _, kinds, pairs, _ = terminal_data(current, bands)
    assert (original['alpha'], original['beta'], original['gamma']) == (1, 2, 7)
    assert len(current[2]) == 8*depth+tail+27 and len(current[3]) == 3*width+tail+12
    cells = {point for band in bands for column in band for point in column}
    assert current[2] | vertices <= cells
    assert all((2*(row//2)+vertical, 2*(column//2)+horizontal) in cells
               for row, column in vertices for vertical, horizontal in itertools.product((0, 1), repeat=2))
    margin = (2*depth+6)*width+4*depth+7+(width+2)*(tail-4)//2
    assert original['boundary_budget'] == width+6
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*margin and margin > 0
    auxiliary = [tuple(column) for band in bands for column in band if set(column) <= vertices]
    mate = {point: other for first, second in auxiliary
            for point, other in [(first, second), (second, first)]}
    edges, portals, adjacency = candidate_graph(current, bands, labels, vertices)
    assert len(portals) == 8
    outer, right_outer = 2-2*depth+shift, 2*depth+8+shift
    expected_portals = {frozenset((source, target))
                        for row, opposite in [(5, 4), (width+4, width+5)]
                        for source_column, target_column in [(3+shift, outer), (7+shift, right_outer)]
                        for source in [(row, source_column)]
                        for target in [(row, target_column), (opposite, target_column)]}
    assert set(portals) == expected_portals
    assert all(owners[first] == owners[second] or edge in portals
               for edge in edges for first, second in [tuple(edge)])
    for edge in edges-set(portals):
        first, second = tuple(edge)
        assert abs(first[0]//2-second[0]//2)+abs(first[1]-second[1]) <= 1
    assert all(first[0]//2 == second[0]//2 and first[1] == second[1]
               for first, second in auxiliary)
    sources = {(5, 3+shift), (width+4, 3+shift)}
    assert sources == {point for pair in pairs if all(kinds[point] == 'TP' for point in pair) for point in pair}
    donors = {point for pair in pairs if all(kinds[point] == 'BP' for point in pair) for point in pair}
    target_upper, target_lower = (4, outer-2), (width+5, outer-tail)
    assert donors & {point for point, owner in owners.items() if owner == 1} == {target_upper, target_lower}
    costs = {}
    for source in sources:
        available_portals = {edge for edge in portals if edge <= set(mate) | donors | {source}}
        assert available_portals == {edge for edge in portals if source in edge}
        walks = shortest_walks(source, donors, adjacency, mate)
        assert set(walks) == {target_upper, target_lower}
        for cost, route in walks.values():
            assert len(route) == len(set(route)) and len(route) == 2*cost
        expected = 3 if source[0] == 5 else min(tail+1, width//2+3)
        assert min(cost for cost, _ in walks.values()) == expected
        if source[0] != 5:
            assert walks[target_upper][0] == width//2+3 and walks[target_lower][0] == tail+1
        costs['upper' if source[0] == 5 else 'lower'] = expected
        totals['endpoint_shortest_walk_checks'] += 1
    for _, route, expected in repair_paths(width, tail, outer, shift):
        check_repair(current, auxiliary, kinds, edges, portals, route, expected, totals)
    totals['frozen_unique_physical_models'] += 1
    totals['exact_portal_witnesses'] += len(portals)
    return dict(width=width, depth=depth, tail=tail, margin=margin, costs=costs)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    parameters = set(itertools.product((6, 8, 12, 20, 32), (1, 2, 4, 8), (4, 6, 10, 20, 32)))
    parameters.update((4*index, depth, 2*index) for index in range(2, 17) for depth in (1, 5))
    totals, examples = Counter(), []
    for width, depth, tail in sorted(parameters):
        record = control(width, depth, tail, totals)
        if (width, depth, tail) in {(6, 1, 4), (8, 1, 4), (32, 1, 16), (64, 5, 32)}:
            examples.append(record)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals), examples=examples,
        scope='Finite physical controls for the all-parameter terminal-choice cost theorem. '
              'Exact candidate relation: occupied grid edges and all row choices across maximal '
              'all-BT endpoint-free gaps. Lower bounds use written symmetric-difference and '
              'quotient-distance proofs; no exhaustive matching enumeration or global grid claim.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
