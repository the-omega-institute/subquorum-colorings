#!/usr/bin/env python3
"""Coordinate controls for alternating circuit pruning and one-port budgets."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

from check_cross_component_compensation import witness_record
from check_exterior_component_budgets import bent_receiver, component_budgets, tile_set
from check_neutral_attachment_normalization import eligible
from check_residual_corridors import corridor, direct_check, graph_record, transformed
from verify_grid_short_path_compensation import pairs


def tile_of(vertex, columns):
    return vertex[0]//2*(columns//2)+vertex[1]//2


def adjacent(first, second):
    return abs(first[0]-second[0])+abs(first[1]-second[1]) == 1


def passage_check(current, graph):
    endpoints = collections.defaultdict(list)
    for first, second in graph['ends']:
        for vertex in (first, second):
            point = divmod(vertex, current[1])
            endpoints[tile_of(point, current[1])].append(point)
    checked = 0
    for tile in range(graph['N']):
        if graph['r'][tile] == 1 and graph['deg'][tile] == 2:
            first, second = endpoints[tile]
            assert adjacent(first, second)
            checked += 1
    return checked


def terminal_record(current, region):
    graph, _ = graph_record(*current)
    assert all(graph['t'][tile] < 2 for tile in region)
    ports = sum((first in region) != (second in region) for first, second in graph['E'])
    leaves = sum(graph['r'][tile] == 0 and graph['deg'][tile] == 1 for tile in region)
    slack = sum(2*graph['r'][tile]-graph['deg'][tile] for tile in region if graph['r'][tile] > 0)
    charge_twice = sum(graph['deg'][tile]-2*graph['r'][tile] for tile in region)
    assert slack >= 0 and charge_twice == leaves-slack
    assert (slack-ports-leaves) % 2 == 0
    assert ports+charge_twice <= 2*((ports+leaves)//2)
    if not leaves:
        assert charge_twice <= -(ports % 2)
        if ports == 1:
            assert charge_twice <= -1
    return dict(ports=ports, positive_zero_leaves=leaves, slack=slack,
                charge_twice=charge_twice, shortage_twice=ports+charge_twice)


def auxiliary(current, region):
    graph, _ = graph_record(*current)
    internal = []
    black = {}
    white = {}
    for edge in current[3]:
        first, second = (tile_of(vertex, current[1]) for vertex in edge)
        if first == second or first not in region or second not in region:
            continue
        if graph['t'][first] == 2 or graph['t'][second] == 2:
            continue
        index = len(internal)
        internal.append(edge)
        for vertex in edge:
            (black if sum(vertex) % 2 == 0 else white)[vertex] = index
    arcs = [[] for _ in internal]
    for first, source in black.items():
        for second in ((first[0]-1, first[1]), (first[0]+1, first[1]),
                       (first[0], first[1]-1), (first[0], first[1]+1)):
            if second in white and tile_of(first, current[1]) == tile_of(second, current[1]):
                target = white[second]
                assert source != target
                arcs[source].append((source, target, first, second))
    return internal, arcs


def find_cycle(arcs):
    colors = [0]*len(arcs)
    parent = {}
    for start in range(len(arcs)):
        if colors[start]:
            continue
        colors[start] = 1
        stack = [(start, iter(arcs[start]))]
        while stack:
            source, iterator = stack[-1]
            arc = next(iterator, None)
            if arc is None:
                colors[source] = 2
                stack.pop()
                continue
            target = arc[1]
            if colors[target] == 0:
                parent[target] = arc
                colors[target] = 1
                stack.append((target, iter(arcs[target])))
            elif colors[target] == 1:
                path = []
                cursor = source
                while cursor != target:
                    path.append(parent[cursor])
                    cursor = parent[cursor][0]
                return list(reversed(path))+[arc]
    return None


def boundary(current, region):
    return {frozenset(edge) for edge in current[3]
            if (tile_of(edge[0], current[1]) in region) != (tile_of(edge[1], current[1]) in region)}


def cancel(current, region, cycle):
    internal, arcs = auxiliary(current, region)
    assert cycle and len(cycle) >= 2
    assert all(arc in arcs[arc[0]] for arc in cycle)
    assert len({arc[0] for arc in cycle}) == len(cycle)
    assert all(cycle[index][1] == cycle[(index+1) % len(cycle)][0] for index in range(len(cycle)))
    removed = {frozenset(internal[arc[0]]) for arc in cycle}
    new_edges = [(arc[2], arc[3]) for arc in cycle]
    changed = (*current[:3], [edge for edge in current[3] if frozenset(edge) not in removed]+new_edges)
    assert direct_check(*current) == direct_check(*changed)
    assert len(current[3]) == len(changed[3])
    assert {vertex for edge in current[3] for vertex in edge} == {
        vertex for edge in changed[3] for vertex in edge}
    before, _ = graph_record(*current)
    after, _ = graph_record(*changed)
    visits = collections.Counter(tile_of(first, current[1]) for first, _ in new_edges)
    for tile in range(before['N']):
        assert before['t'][tile] == after['t'][tile]
        assert before['s'][tile] == after['s'][tile]
        assert after['h'][tile] == before['h'][tile]+visits[tile]
        assert after['r'][tile] == before['r'][tile]-visits[tile]
        assert after['deg'][tile] == before['deg'][tile]-2*visits[tile]
        assert before['deg'][tile]-2*before['r'][tile] == after['deg'][tile]-2*after['r'][tile]
    assert len(after['E']) == len(before['E'])-len(cycle)
    assert boundary(current, region) == boundary(changed, region)
    assert set(eligible(current)) == set(eligible(changed))
    assert terminal_record(current, region) == terminal_record(changed, region)
    assert sum(record['signed_shortfall'] for record in component_budgets(current, region)) == sum(
        record['signed_shortfall'] for record in component_budgets(changed, region))
    return changed, dict(removed_residual_edges=len(cycle), new_internal_edges=len(cycle),
                         tile_visits=dict(visits), repeated_tile=any(count == 2 for count in visits.values()))


def normalize(current, region):
    initial_edges = len(auxiliary(current, region)[0])
    steps = []
    while cycle := find_cycle(auxiliary(current, region)[1]):
        current, record = cancel(current, region, cycle)
        steps.append(record)
    assert len(steps) <= initial_edges//2
    return current, steps


def figure_eight(one_port=False):
    matching = [((2, 2), (1, 2)), ((1, 3), (1, 4)), ((1, 5), (2, 5)), ((2, 4), (2, 3)),
                ((3, 2), (3, 1)), ((3, 0), (4, 0)), ((4, 1), (4, 2)), ((4, 3), (3, 3)),
                ((0, 2), (0, 3)), ((0, 4), (0, 5)), ((3, 4), (3, 5)),
                ((2, 0), (2, 1)), ((5, 0), (5, 1)), ((5, 2), (5, 3))]
    if one_port:
        matching.remove(((0, 2), (0, 3)))
        matching.append(((0, 2), (-1, 2)))
    new_pairs = [((2, 2), (3, 2)), ((2, 3), (3, 3)),
                 ((1, 2), (1, 3)), ((1, 4), (1, 5)), ((2, 4), (2, 5)),
                 ((3, 0), (3, 1)), ((4, 0), (4, 1)), ((4, 2), (4, 3))]
    shift = lambda point: (point[0]+2, point[1]+2)
    matching = [tuple(shift(vertex) for vertex in edge) for edge in matching]
    new_pairs = [tuple(shift(vertex) for vertex in edge) for edge in new_pairs]
    tiles = ((0, 1), (0, 2), (1, 0), (1, 1), (1, 2), (2, 0), (2, 1))
    vertices = {shift((2*row+corner_row, 2*column+corner_column))
                for row, column in tiles for corner_row, corner_column in itertools.product(range(2), repeat=2)}
    return (10, 10, set(), matching), vertices, new_pairs


def prescribed_cycle(current, region, new_pairs):
    _, arcs = auxiliary(current, region)
    desired = {frozenset(edge) for edge in new_pairs}
    selected_arcs = [arc for options in arcs for arc in options if frozenset(arc[2:]) in desired]
    assert len(selected_arcs) == len(desired)
    successor = {arc[0]: arc for arc in selected_arcs}
    result = []
    cursor = min(successor)
    while cursor not in {arc[0] for arc in result}:
        result.append(successor[cursor])
        cursor = result[-1][1]
    assert len(result) == len(selected_arcs) and cursor == result[0][0]
    return result


def irreducible_ring(one_port=False):
    matching = [((0, 1), (0, 2)), ((1, 2), (2, 2)), ((3, 2), (3, 1)),
                ((2, 0), (1, 0)), ((0, 3), (1, 3)), ((2, 3), (3, 3))]
    if one_port:
        matching.append(((0, 0), (-1, 0)))
    shift = lambda point: (point[0]+2, point[1]+2)
    matching = [tuple(shift(vertex) for vertex in edge) for edge in matching]
    vertices = {shift((row, column)) for row in range(4) for column in range(4)}
    return (8, 8, set(), matching), vertices


def exhaustive():
    reports = []
    for rows, columns in ((2, 2), (2, 4), (4, 2), (2, 6), (6, 2)):
        count = subsets = passages = cancellations = removed = 0
        for mask, matching_indices in pairs(rows, columns):
            selected = {divmod(vertex, columns) for vertex in range(rows*columns) if mask >> vertex & 1}
            current = rows, columns, selected, [tuple(divmod(vertex, columns) for vertex in edge)
                                                for edge in matching_indices]
            graph, _ = graph_record(*current)
            passages += passage_check(current, graph)
            deficient = [tile for tile in range(graph['N']) if graph['t'][tile] < 2]
            for mask in range(1, 1 << len(deficient)):
                region = {tile for index, tile in enumerate(deficient) if mask >> index & 1}
                terminal_record(current, region)
                subsets += 1
            _, steps = normalize(current, set(deficient))
            cancellations += len(steps)
            removed += sum(step['removed_residual_edges'] for step in steps)
            count += 1
        reports.append(dict(shape=[rows, columns], feasible_pairs=count, deficient_subsets=subsets,
                            capacity_one_passages=passages, cancellations=cancellations, removed_edges=removed))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-length', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_length < 2:
        parser.error('--max-length must be at least two')
    reports = exhaustive()
    witnesses = []
    controls = []
    for one_port in (False, True):
        original, region, new_pairs = figure_eight(one_port)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, *symmetry)
            current = (*shape, selected, matching)
            moved_region = transformed(*original[:2], region, [], *symmetry)[1]
            moved_pairs = transformed(*original[:2], set(), new_pairs, *symmetry)[2]
            tiles = tile_set(current, moved_region)
            direct_check(*current)
            circuit = prescribed_cycle(current, tiles, moved_pairs)
            changed, step = cancel(current, tiles, circuit)
            assert step['removed_residual_edges'] == 8 and step['repeated_tile']
            assert find_cycle(auxiliary(changed, tiles)[1]) is None
            before = terminal_record(current, tiles)
            after = terminal_record(changed, tiles)
            assert before['ports'] == after['ports'] == int(one_port)
            assert before['charge_twice'] == after['charge_twice'] == -int(one_port)
            assert after['positive_zero_leaves'] == 0
            controls.append(dict(fixture='repeated-tile circuit', one_port=one_port,
                                 symmetry=symmetry, before=before, after=after, step=step))
        record = witness_record('Two cycles sharing a capacity-two tile'+(' with one port' if one_port else ''), original)
        changed, step = cancel(original, tile_set(original, region), prescribed_cycle(original, tile_set(original, region), new_pairs))
        record.update(before=terminal_record(original, tile_set(original, region)),
                      after=witness_record('After repeated-tile cancellation', changed), cancellation=step)
        witnesses.append(record)
    for one_port in (False, True):
        original, region = irreducible_ring(one_port)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, *symmetry)
            current = (*shape, selected, matching)
            moved_region = transformed(*original[:2], region, [], *symmetry)[1]
            tiles = tile_set(current, moved_region)
            direct_check(*current)
            assert find_cycle(auxiliary(current, tiles)[1]) is None
            record = terminal_record(current, tiles)
            assert record['ports'] == int(one_port) and record['charge_twice'] == -4+int(one_port)
            component, = component_budgets(current, tiles)
            assert component['cycle_rank'] == 1 and component['capacity_two'] == 2
            controls.append(dict(fixture='irreducible diagonal cycle', one_port=one_port,
                                 symmetry=symmetry, terminal=record, component=component))
        record = witness_record('Irreducible two-diagonal cycle'+(' with one port' if one_port else ''), original)
        record['terminal'] = terminal_record(original, tile_set(original, region))
        witnesses.append(record)
    long_controls = []
    for length in range(2, args.max_length+1):
        original = corridor(length)
        left_source = {(row, column) for row in (0, 1) for column in range(original[1]-2)}
        record = terminal_record(original, tile_set(original, left_source))
        assert record == dict(ports=1, positive_zero_leaves=1, slack=0, charge_twice=1, shortage_twice=2)
        assert not eligible(original)
        bent, region = bent_receiver(length, 'one_port')
        donor = terminal_record(bent, tile_set(bent, region))
        assert donor == dict(ports=1, positive_zero_leaves=0, slack=1, charge_twice=-1, shortage_twice=0)
        long_controls.append(dict(length=length, excluded_leaf_example=record, one_port_bent_donor=donor))
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/RESIDUAL_CYCLE_PRUNING.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_exterior_component_budgets.py', 'check_neutral_attachment_normalization.py',
        'check_residual_corridors.py', 'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', exhaustive=reports, symmetry_controls=len(controls),
                  controls=controls, witnesses=witnesses, length_range=[2, args.max_length],
                  long_controls=long_controls,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite controls of elementary written adjacency, parity and alternating-circuit proofs. The global source conclusion retains its explicit geometry and prior width-six Omega dependency. No universal grid or new Lean theorem.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('status', 'exhaustive', 'symmetry_controls', 'length_range')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
