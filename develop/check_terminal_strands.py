#!/usr/bin/env python3
"""Physical strand controls for exact single-use regional compensation."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

from check_exterior_component_budgets import bent_receiver, tile_set
from check_mixed_band_boundary_obstacle import capacity_two, configuration
from check_residual_corridors import corridor, direct_check, graph_record, transformed
from check_residual_cycle_pruning import boundary, figure_eight, irreducible_ring, terminal_record, tile_of
from verify_grid_short_path_compensation import pairs


def adjacent(first, second):
    return abs(first[0]-second[0])+abs(first[1]-second[1]) == 1


def local_choices(endpoints):
    possible = [edge for edge in itertools.combinations(sorted(endpoints), 2) if adjacent(*edge)]
    choices = []
    for count in range(len(possible)+1):
        for candidate in itertools.combinations(possible, count):
            vertices = [vertex for edge in candidate for vertex in edge]
            if len(set(vertices)) == len(vertices):
                choices.append(candidate)
    maximum = max(map(len, choices))
    return [candidate for candidate in choices if len(candidate) == maximum]


def decompose(current, region, choice_index=0):
    graph, _ = graph_record(*current)
    assert all(graph['t'][tile] < 2 for tile in region)
    residual_edges = [tuple(divmod(vertex, current[1]) for vertex in edge)
                      for edge, tile_edge in zip(graph['ends'], graph['E'])
                      if tile_edge[0] in region or tile_edge[1] in region]
    ends = collections.defaultdict(set)
    adjacency = collections.defaultdict(list)
    matching_pairs = {frozenset(edge) for edge in residual_edges}
    for first, second in residual_edges:
        adjacency[first].append(second)
        adjacency[second].append(first)
        for vertex in (first, second):
            tile = tile_of(vertex, current[1])
            if tile in region:
                ends[tile].add(vertex)
    terminal_types = {}
    local_pairs = []
    unpaired = reserve = 0
    for tile in sorted(region):
        endpoints = ends[tile]
        capacity = graph['r'][tile]
        degree = graph['deg'][tile]
        assert len(endpoints) == degree
        candidate = local_choices(endpoints)[choice_index % len(local_choices(endpoints))]
        if capacity == 0:
            assert degree <= 1 and not candidate
            for vertex in endpoints:
                terminal_types[vertex] = 'L'
        else:
            used = {vertex for edge in candidate for vertex in edge}
            remaining = endpoints-used
            unused = 2*capacity-degree
            assert 0 <= len(remaining) <= unused and (unused-len(remaining)) % 2 == 0
            unpaired += len(remaining)
            reserve += (unused-len(remaining))//2
            for vertex in remaining:
                terminal_types[vertex] = 'S'
        for first, second in candidate:
            adjacency[first].append(second)
            adjacency[second].append(first)
            local_pairs.append((first, second))
    for vertex in adjacency:
        if tile_of(vertex, current[1]) not in region:
            terminal_types[vertex] = 'P'
        assert len(adjacency[vertex]) in (1, 2)
        assert (len(adjacency[vertex]) == 1) == (vertex in terminal_types)
    pending = set(adjacency)
    paths = []
    cycles = []
    edge_total = 0
    while pending:
        start = min(pending)
        component = {start}
        queue = [start]
        while queue:
            vertex = queue.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in component:
                    component.add(neighbor)
                    queue.append(neighbor)
        pending -= component
        terminals = sorted(vertex for vertex in component if len(adjacency[vertex]) == 1)
        assert len(terminals) in (0, 2)
        edges = {frozenset((vertex, neighbor)) for vertex in component for neighbor in adjacency[vertex]}
        original = edges & matching_pairs
        auxiliary = edges-matching_pairs
        edge_total += len(edges)
        record = dict(vertices=sorted(component), matching=sorted(map(sorted, original)),
                      auxiliary=sorted(map(sorted, auxiliary)))
        if terminals:
            assert len(original) == len(auxiliary)+1
            kind = ''.join(sorted(terminal_types[vertex] for vertex in terminals))
            record.update(kind=kind, endpoints=terminals)
            if kind == 'PP':
                assert (sum(terminals[0])-sum(terminals[1])) % 2 == 1
            paths.append(record)
        else:
            assert len(original) == len(auxiliary)
            cycles.append(record)
    assert edge_total == len(residual_edges)+len(local_pairs)
    counts = {kind: sum(path['kind'] == kind for path in paths) for kind in ('LL', 'LP', 'LS', 'PP', 'PS', 'SS')}
    terminal = terminal_record(current, region)
    assert terminal['positive_zero_leaves'] == 2*counts['LL']+counts['LP']+counts['LS']
    assert terminal['ports'] == 2*counts['PP']+counts['LP']+counts['PS']
    assert unpaired == 2*counts['SS']+counts['LS']+counts['PS']
    assert terminal['slack'] == unpaired+2*reserve
    shortage = counts['LL']+counts['LP']+counts['PP']-counts['SS']-reserve
    assert terminal['shortage_twice'] == 2*shortage
    neutral = all(graph['deg'][tile] == 2*graph['r'][tile] for tile in region)
    if neutral:
        assert terminal['positive_zero_leaves'] == terminal['slack'] == unpaired == reserve == 0
        assert counts['PP']*2 == terminal['ports']
        assert not any(counts[kind] for kind in ('LL', 'LP', 'LS', 'PS', 'SS'))
    return dict(terminal=terminal, counts=counts, unpaired=unpaired, reserve=reserve,
                shortage=shortage, neutral=neutral, paths=paths, cycles=cycles)


def prune_cycles(current, region, record):
    deleted = {frozenset(edge) for cycle in record['cycles'] for edge in cycle['matching']}
    inserted = [tuple(map(tuple, edge)) for cycle in record['cycles'] for edge in cycle['auxiliary']]
    changed = (*current[:3], [edge for edge in current[3] if frozenset(edge) not in deleted]+inserted)
    assert direct_check(*current) == direct_check(*changed)
    assert {vertex for edge in current[3] for vertex in edge} == {vertex for edge in changed[3] for vertex in edge}
    assert boundary(current, region) == boundary(changed, region)
    before, _ = graph_record(*current)
    after, _ = graph_record(*changed)
    for tile in range(before['N']):
        assert before['t'][tile] == after['t'][tile] and before['s'][tile] == after['s'][tile]
        assert before['deg'][tile]-2*before['r'][tile] == after['deg'][tile]-2*after['r'][tile]
    assert terminal_record(current, region) == terminal_record(changed, region)
    if record['neutral'] and not record['terminal']['ports']:
        assert all(after['deg'][tile] == after['r'][tile] == 0 for tile in region)
    return len(deleted)


def exhaustive():
    reports = []
    for rows, columns in ((2, 2), (2, 4), (4, 2), (2, 6), (6, 2)):
        feasible = regions = neutral_regions = closed_neutral = cycles = removed = 0
        totals = collections.Counter()
        for selected_mask, matching in pairs(rows, columns):
            current = rows, columns, {divmod(vertex, columns) for vertex in range(rows*columns)
                                      if selected_mask >> vertex & 1}, [tuple(divmod(vertex, columns) for vertex in edge)
                                                                       for edge in matching]
            graph, _ = graph_record(*current)
            deficient = [tile for tile in range(graph['N']) if graph['t'][tile] < 2]
            for mask in range(1, 1 << len(deficient)):
                region = {tile for index, tile in enumerate(deficient) if mask >> index & 1}
                record = decompose(current, region)
                totals.update(record['counts'])
                regions += 1
                neutral_regions += record['neutral']
                closed_neutral += record['neutral'] and record['terminal']['ports'] == 0
                cycles += len(record['cycles'])
                if record['cycles'] or record['neutral']:
                    removed += prune_cycles(current, region, record)
                if len(region) == len(deficient):
                    assert 2*direct_check(*current)-rows*columns == 2*(record['counts']['LL']-record['counts']['SS']-record['reserve'])
            feasible += 1
        reports.append(dict(shape=[rows, columns], feasible_pairs=feasible, regions=regions,
                            neutral_regions=neutral_regions, closed_neutral_regions=closed_neutral,
                            alternating_cycles=cycles, removed_matching_edges=removed, strands=dict(totals)))
    return reports


def fixtures():
    controls = []
    for one_port in (False, True):
        for name, constructor in (('capacity-two figure-eight', figure_eight), ('diagonal ring', irreducible_ring)):
            built = constructor(one_port)
            original, vertices = built[:2]
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*original, *symmetry)
                current = (*shape, selected, matching)
                moved = transformed(*original[:2], vertices, [], *symmetry)[1]
                region = tile_set(current, moved)
                for choice_index in (0, 1):
                    record = decompose(current, region, choice_index)
                    removed = prune_cycles(current, region, record)
                    if name == 'diagonal ring':
                        assert record['counts']['SS'] == 2-int(one_port)
                        assert record['counts']['PS'] == int(one_port)
                        assert record['reserve'] == 0 and not record['cycles']
                    else:
                        assert record['shortage'] == 0
                        if not one_port:
                            assert record['neutral'] and not record['paths'] and removed == 8
                        else:
                            assert record['counts']['PS'] == 1 and record['counts']['SS'] == 0
                    controls.append(dict(fixture=name, one_port=one_port, symmetry=symmetry,
                                         choice_index=choice_index, counts=record['counts'],
                                         reserve=record['reserve'], shortage=record['shortage'],
                                         cycles=len(record['cycles']), removed=removed))
    return controls


def long_controls(max_length):
    records = []
    for length in range(2, max_length+1):
        original = corridor(length)
        whole = {column for column in range(original[1]//2)}
        source = decompose(original, whole)
        partial = decompose(original, whole-{original[1]//2-1})
        assert source['counts']['LL'] == 1 and source['shortage'] == 1
        assert partial['counts']['LP'] == 1 and partial['shortage'] == 1
        for variation in ('two_ports', 'capacity_two', 'one_port'):
            current, vertices = bent_receiver(length, variation)
            record = decompose(current, tile_set(current, vertices))
            assert record['counts']['PP'] == int(variation != 'one_port')
            assert record['counts']['PS'] == int(variation == 'one_port')
            assert record['reserve'] == int(variation == 'capacity_two')
            assert record['shortage'] == int(variation == 'two_ports')
            records.append(dict(length=length, variation=variation, counts=record['counts'],
                                reserve=record['reserve'], shortage=record['shortage']))
    return records


def local_table():
    corners = {(row, column) for row, column in itertools.product(range(2), repeat=2)}
    controls = 0
    for capacity in (1, 2):
        for degree in range(2*capacity+1):
            for endpoints in itertools.combinations(sorted(corners), degree):
                if capacity == 1 and degree == 2 and not adjacent(*endpoints):
                    continue
                for choice in local_choices(endpoints):
                    unpaired = degree-2*len(choice)
                    unused = 2*capacity-degree
                    assert 0 <= unpaired <= unused and (unused-unpaired) % 2 == 0
                    controls += 1
    return controls


def mixed_family(max_length):
    controls = []
    for modules in range(1, max_length+1):
        original = configuration(modules)
        for flipped in (False, True):
            current = capacity_two(original) if flipped else original
            graph, _ = graph_record(*current)
            region = {tile for tile in range(graph['N']) if graph['t'][tile] < 2}
            record = decompose(current, region)
            assert record['counts']['LL'] == record['reserve'] == 1
            assert record['counts']['LS'] == modules
            assert record['counts']['SS'] == record['counts']['LP'] == record['counts']['PP'] == record['counts']['PS'] == 0
            assert record['shortage'] == 0
            assert record['terminal']['positive_zero_leaves'] == modules+2
            assert record['terminal']['slack'] == modules+2
            removed = prune_cycles(current, region, record)
            controls.append(dict(modules=modules, capacity_two=flipped, counts=record['counts'],
                                 reserve=record['reserve'], cycles=len(record['cycles']), removed=removed))
    return controls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-length', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_length < 2:
        parser.error('--max-length must be at least two')
    report = dict(status='ALL_CHECKS_PASSED', local_pairing_controls=local_table(),
                  exhaustive=exhaustive(), symmetry_controls=fixtures(),
                  length_controls=long_controls(args.max_length), length_range=[2, args.max_length],
                  corridor_region_controls=2*(args.max_length-1), mixed_family_controls=mixed_family(args.max_length))
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/TERMINAL_STRAND_ACCOUNTING.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_exterior_component_budgets.py', 'check_residual_cycle_pruning.py',
        'check_residual_corridors.py', 'verify_grid_short_path_compensation.py',
        'check_mixed_band_boundary_obstacle.py'))
    report['sha256'] = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    report['scope'] = 'Finite controls of the general local pairing table and strand proofs. No universal donor allocation, new strip theorem or new Lean theorem.'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('status', 'local_pairing_controls', 'exhaustive', 'length_range')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
