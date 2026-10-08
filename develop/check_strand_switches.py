#!/usr/bin/env python3
"""Controls for auxiliary pairing invariants and debt-donor switches."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

from check_exterior_component_budgets import bent_receiver, tile_set
from check_residual_corridors import direct_check, graph_record, transformed
from check_terminal_strands import local_choices
from check_residual_cycle_pruning import terminal_record, tile_of
from verify_grid_short_path_compensation import pairs


def strand_graph(adjacency, labels):
    pending = set(adjacency)
    strands = []
    cycles = []
    while pending:
        start = min(pending)
        vertices = {start}
        queue = [start]
        while queue:
            vertex = queue.pop()
            for neighbor in adjacency[vertex]:
                if neighbor not in vertices:
                    vertices.add(neighbor)
                    queue.append(neighbor)
        pending -= vertices
        ends = sorted(vertex for vertex in vertices if len(adjacency[vertex]) == 1)
        assert len(ends) in (0, 2)
        assert all(len(adjacency[vertex]) in (1, 2) for vertex in vertices)
        if ends:
            assert all(vertex in labels for vertex in ends)
            strands.append(dict(vertices=vertices, ends=ends, kind=''.join(sorted(labels[vertex] for vertex in ends))))
        else:
            cycles.append(vertices)
    return strands, cycles


def build(current, region, overrides=None):
    overrides = overrides or {}
    graph, _ = graph_record(*current)
    assert all(graph['t'][tile] < 2 for tile in region)
    adjacency = collections.defaultdict(set)
    endpoints = collections.defaultdict(set)
    labels = {}
    for edge, tile_edge in zip(graph['ends'], graph['E']):
        if not any(tile in region for tile in tile_edge):
            continue
        first, second = (divmod(vertex, current[1]) for vertex in edge)
        adjacency[first].add(second)
        adjacency[second].add(first)
        for vertex in (first, second):
            tile = tile_of(vertex, current[1])
            if tile in region:
                endpoints[tile].add(vertex)
            else:
                labels[vertex] = 'P'
    choices = {}
    reserve = 0
    reserves = {}
    colors = collections.Counter()
    for tile in sorted(region):
        options = local_choices(endpoints[tile])
        choice = overrides.get(tile, 0)
        assert 0 <= choice < len(options)
        choices[tile] = options
        selected = options[choice]
        used = {vertex for edge in selected for vertex in edge}
        unpaired = endpoints[tile]-used
        if graph['r'][tile]:
            unused = 2*graph['r'][tile]-graph['deg'][tile]
            assert 0 <= len(unpaired) <= unused and (unused-len(unpaired)) % 2 == 0
            reserve += (unused-len(unpaired))//2
            reserves[tile] = (unused-len(unpaired))//2
            kind = 'S'
        else:
            assert len(unpaired) <= 1
            kind = 'L'
        for vertex in unpaired:
            labels[vertex] = kind
        for first, second in selected:
            adjacency[first].add(second)
            adjacency[second].add(first)
    for vertex, kind in labels.items():
        colors[(kind, sum(vertex) % 2)] += 1
    strands, cycles = strand_graph(adjacency, labels)
    counts = collections.Counter(strand['kind'] for strand in strands)
    for strand in strands:
        assert (sum(strand['ends'][0])-sum(strand['ends'][1])) % 2 == 1
    terminal = terminal_record(current, region)
    debt = sum(counts[kind] for kind in ('LL', 'LP', 'PP'))
    shortage = debt-counts['SS']-reserve
    assert terminal['shortage_twice'] == 2*shortage
    assert shortage == colors[('L', 0)]+colors[('P', 0)]-colors[('S', 1)]-reserve
    assert shortage == colors[('L', 1)]+colors[('P', 1)]-colors[('S', 0)]-reserve
    return dict(strands=strands, cycles=cycles, counts=counts, colors=colors,
                reserve=reserve, reserves=reserves, terminal=terminal, choices=choices, debt=debt)


def switch_tile(current, region, record):
    debt_paths = [strand for strand in record['strands'] if strand['kind'] in ('LL', 'LP', 'PP')]
    donors = [strand for strand in record['strands'] if strand['kind'] == 'SS']
    for debt in debt_paths:
        debt_tiles = {tile_of(vertex, current[1]) for vertex in debt['vertices']} & region
        for donor in donors:
            donor_tiles = {tile_of(vertex, current[1]) for vertex in donor['vertices']} & region
            shared = debt_tiles & donor_tiles
            if shared:
                tile = min(shared)
                assert len(record['choices'][tile]) == 2
                return tile
    return None


def normalize(current, region, overrides=None):
    overrides = dict(overrides or {})
    record = build(current, region, overrides)
    limit = min(record['debt'], record['counts']['SS'])
    steps = 0
    while (tile := switch_tile(current, region, record)) is not None:
        overrides[tile] = 1-overrides.get(tile, 0)
        changed = build(current, region, overrides)
        assert changed['debt'] == record['debt']-1
        assert changed['counts']['SS'] == record['counts']['SS']-1
        assert changed['reserve'] == record['reserve']
        assert changed['colors'] == record['colors']
        assert changed['terminal'] == record['terminal']
        record = changed
        steps += 1
    assert steps <= limit
    return record, steps


def fixture(degree):
    matching = [((2, 2), (1, 2)), ((2, 3), (2, 4)), ((3, 3), (4, 3)),
                ((3, 2), (3, 1)), ((2, 0), (2, 1)), ((5, 2), (5, 3))]
    tiles = [(1, 1), (1, 0), (2, 1)]
    if degree == 3:
        matching.remove(((3, 3), (4, 3)))
        tiles.remove((2, 1))
    vertices = {(2*row+corner_row, 2*column+corner_column)
                for row, column in tiles for corner_row, corner_column in itertools.product(range(2), repeat=2)}
    return (6, 6, set(), matching), vertices


def reserve_payment(current, region, record):
    assigned = set()
    paid = 0
    graph, _ = graph_record(*current)
    for strand in record['strands']:
        if strand['kind'] not in ('LL', 'LP', 'PP'):
            continue
        tiles = {tile_of(vertex, current[1]) for vertex in strand['vertices']} & region
        candidates = {tile for tile in tiles if record['reserves'].get(tile, 0)}
        if candidates:
            tile = min(candidates)
            assert tile not in assigned
            assert graph['r'][tile] == graph['deg'][tile] == 2
            assert record['reserves'][tile] == 1
            assigned.add(tile)
            paid += 1
    assert record['debt']-paid-record['counts']['SS']-(record['reserve']-paid) == record['terminal']['shortage_twice']//2
    return paid


def coordinate_controls():
    records = []
    for degree in (3, 4):
        original, vertices = fixture(degree)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, *symmetry)
            current = (*shape, selected, matching)
            moved = transformed(*original[:2], vertices, [], *symmetry)[1]
            region = tile_set(current, moved)
            direct_check(*current)
            baseline = build(current, region)
            for choice in (0, 1):
                overrides = {tile:choice for tile, options in baseline['choices'].items() if len(options) == 2}
                record = build(current, region, overrides)
                changed, steps = normalize(current, region, overrides)
                assert record['terminal']['ports'] == 2 and record['terminal']['charge_twice'] == -2
                assert record['reserve'] == changed['reserve'] == 0
                assert changed['counts']['PS'] == 2 and changed['debt'] == changed['counts']['SS'] == 0
                records.append(dict(degree=degree, symmetry=symmetry, initial_choice=choice,
                                    before=dict(record['counts']), after=dict(changed['counts']), steps=steps))
    return records


def reserve_controls():
    records = []
    for length in range(2, 41):
        current, vertices = bent_receiver(length, 'capacity_two')
        region = tile_set(current, vertices)
        record, steps = normalize(current, region)
        assert record['debt'] == record['reserve'] == reserve_payment(current, region, record) == 1
        assert record['counts']['SS'] == steps == 0
        records.append(dict(length=length, paid=1, remaining_debt=0, remaining_reserve=0))
    return records


def abstract_controls():
    checked = 0
    for degree, debt_kind, lengths in itertools.product((3, 4), ('LL', 'LP', 'PP'), itertools.product((1, 3, 5), repeat=4)):
        corners = ((0, 0), (0, 1), (1, 1), (1, 0))
        initial = ((corners[0], corners[1]), (corners[2], corners[3])) if degree == 4 else ((corners[0], corners[1]),)
        final = ((corners[0], corners[3]), (corners[1], corners[2])) if degree == 4 else ((corners[1], corners[2]),)
        active = corners if degree == 4 else corners[:3]
        labels = {}
        base = collections.defaultdict(set)
        terminal_kinds = (*debt_kind, 'S', 'S') if degree == 4 else (*debt_kind, 'S')
        for index, corner in enumerate(active):
            cursor = corner
            for position in range(lengths[index]):
                endpoint = (10+index, position)
                base[cursor].add(endpoint)
                base[endpoint].add(cursor)
                cursor = endpoint
            labels[cursor] = terminal_kinds[index]
        if degree == 3:
            labels[corners[2]] = 'S'
        records = []
        for auxiliary in (initial, final):
            adjacency = collections.defaultdict(set, {vertex:set(neighbors) for vertex,neighbors in base.items()})
            current_labels = dict(labels)
            if degree == 3 and auxiliary == final:
                del current_labels[corners[2]]
                current_labels[corners[0]] = 'S'
            for first, second in auxiliary:
                adjacency[first].add(second)
                adjacency[second].add(first)
            strands, cycles = strand_graph(adjacency, current_labels)
            assert not cycles
            records.append(collections.Counter(strand['kind'] for strand in strands))
        assert records[0][debt_kind] == records[0]['SS'] == 1
        assert records[1][debt_kind] == records[1]['SS'] == 0
        assert records[1]['LS'] == debt_kind.count('L') and records[1]['PS'] == debt_kind.count('P')
        checked += 1
    return checked


def exhaustive():
    reports = []
    for rows, columns in ((2, 2), (2, 4), (4, 2), (2, 6), (6, 2)):
        feasible = regions = alternate = steps = reserve_payments = 0
        for mask, matching in pairs(rows, columns):
            current = rows, columns, {divmod(vertex, columns) for vertex in range(rows*columns) if mask >> vertex & 1}, [tuple(divmod(vertex, columns) for vertex in edge) for edge in matching]
            graph, _ = graph_record(*current)
            deficient = [tile for tile in range(graph['N']) if graph['t'][tile] < 2]
            for mask in range(1, 1 << len(deficient)):
                region = {tile for index,tile in enumerate(deficient) if mask >> index & 1}
                baseline = build(current, region)
                normalized, count = normalize(current, region)
                steps += count
                reserve_payments += reserve_payment(current, region, normalized)
                for tile, options in baseline['choices'].items():
                    if len(options) == 2:
                        changed = build(current, region, {tile:1})
                        assert changed['colors'] == baseline['colors']
                        assert changed['reserve'] == baseline['reserve']
                        assert changed['terminal'] == baseline['terminal']
                        alternate += 1
                regions += 1
            feasible += 1
        reports.append(dict(shape=[rows,columns], feasible_pairs=feasible, regions=regions,
                            alternative_local_pairings=alternate, switch_steps=steps, reserve_payments=reserve_payments))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED', exhaustive=exhaustive(),
                  abstract_switch_controls=abstract_controls(), coordinate_controls=coordinate_controls(),
                  bent_reserve_controls=reserve_controls())
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/STRAND_SWITCH_NORMAL_FORM.md']
    sources.extend(Path(__file__).with_name(name) for name in ('check_terminal_strands.py',
        'check_residual_cycle_pruning.py', 'check_residual_corridors.py', 'verify_grid_short_path_compensation.py'))
    report['sha256'] = {str(path.relative_to(root)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    report['scope'] = 'Finite controls of the written auxiliary switch and pairing-choice invariant proofs; no physical rematching or universal donor allocation.'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','exhaustive','abstract_switch_controls')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
