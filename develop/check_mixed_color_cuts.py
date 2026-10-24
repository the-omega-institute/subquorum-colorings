#!/usr/bin/env python3
"""Physical controls of the directed cut theorem and balanced obstruction."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

from check_residual_corridors import direct_check, graph_record, transformed
from check_residual_cycle_pruning import tile_of
from check_strand_switches import build
from verify_grid_short_path_compensation import feasible, graph, pairs


def connected_obstruction(length):
    if length < 0:
        raise ValueError('Require length >= 0.')
    end = 4+2*length
    matching = [((2, 2), (1, 2)), ((3, 2), (3, 1)), ((3, 3), (4, 3)),
                ((0, 2), (0, 3)), ((2, 0), (2, 1)), ((5, 2), (5, 3))]
    matching.extend(((2, 3+2*index), (2, 4+2*index)) for index in range(length+1))
    matching.extend(((3, 4+2*index), (3, 5+2*index)) for index in range(length))
    matching.extend((((2, end+1), (1, end+1)), ((3, end), (4, end)),
                     ((3, end+1), (3, end+2))))
    current = 6, 8+2*length, set(), matching
    columns = current[1]//2
    region = {columns+index for index in range(1, length+3)}
    region.update((1, columns, 2*columns+1))
    return current, region, {columns+length+2}, {1, columns, columns+1, 2*columns+1}


def bent_obstruction(length):
    if length < 1:
        raise ValueError('Require length >= 1 for the bent version.')
    end = 4+2*length
    matching = [((4, 2), (3, 2)), ((5, 2), (5, 1)), ((5, 3), (6, 3)),
                ((2, 2), (2, 3)), ((4, 0), (4, 1)), ((7, 2), (7, 3))]
    matching.extend(((4, 3+2*index), (4, 4+2*index)) for index in range(length+1))
    matching.extend(((5, 4+2*index), (5, 5+2*index)) for index in range(length+1))
    matching.extend((((4, end+1), (3, end+1)), ((2, end), (1, end)),
                     ((2, end+1), (2, end+2)), ((3, end), (3, end-1))))
    current = 8, 8+2*length, set(), matching
    columns = current[1]//2
    region = {2*columns+index for index in range(1, length+3)}
    region.update((columns+1, 2*columns, 3*columns+1, columns+length+2))
    return current, region, {columns+length+2}, {columns+1, 2*columns, 2*columns+1, 3*columns+1}


def independent_feasibility(current):
    rows, columns, selected, matching = current
    objective = direct_check(*current)
    adjacency, _ = graph(rows, columns)
    mask = sum(1 << (row*columns+column) for row, column in selected)
    edges = tuple((first[0]*columns+first[1], second[0]*columns+second[1])
                  for first, second in matching)
    assert feasible(adjacency, mask, edges)
    return objective


def terminals(current, region, record):
    residual, _ = graph_record(*current)
    port_owners = {}
    for edge, tiles in zip(residual['ends'], residual['E']):
        for vertex, owner, other in ((edge[0], tiles[0], tiles[1]),
                                     (edge[1], tiles[1], tiles[0])):
            if owner not in region and other in region:
                port_owners[divmod(vertex, current[1])] = other
    result = []
    for strand in record['strands']:
        ends = []
        for vertex in strand['ends']:
            tile = tile_of(vertex, current[1])
            kind = 'P' if tile not in region else ('L' if residual['r'][tile] == 0 else 'S')
            owner = port_owners[vertex] if kind == 'P' else tile
            ends.append(dict(vertex=vertex, owner=owner, kind=kind,
                             color=sum(vertex) % 2))
        assert ''.join(sorted(end['kind'] for end in ends)) == strand['kind']
        result.append(ends)
    return residual, result


def cut_bound(current, region, subset, terminal_data):
    residual, strand_ends = terminal_data
    counts = collections.Counter()
    actual = collections.Counter()
    for ends in strand_ends:
        debt = all(end['kind'] in ('L', 'P') for end in ends)
        donor = all(end['kind'] == 'S' for end in ends)
        for end in ends:
            if end['owner'] in subset:
                counts[('S' if end['kind'] == 'S' else 'X', end['color'])] += 1
                actual[('D', end['color'])] += debt
                actual[('N', end['color'])] += donor
    outgoing = incoming = 0
    for edge, tiles in zip(residual['ends'], residual['E']):
        if not all(tile in region for tile in tiles):
            continue
        if (tiles[0] in subset) == (tiles[1] in subset):
            continue
        first = divmod(edge[0], current[1])
        black_owner = tiles[sum(first) % 2]
        outgoing += black_owner in subset
        incoming += black_owner not in subset
    bounds = {('D', 0): max(0, counts[('X', 0)]-counts[('S', 1)]-outgoing),
              ('D', 1): max(0, counts[('X', 1)]-counts[('S', 0)]-incoming),
              ('N', 0): max(0, counts[('S', 0)]-counts[('X', 1)]-outgoing),
              ('N', 1): max(0, counts[('S', 1)]-counts[('X', 0)]-incoming)}
    assert all(actual[key] >= value for key, value in bounds.items())
    return bounds


def all_pairings(current, region):
    initial = build(current, region)
    tiles = sorted(tile for tile, options in initial['choices'].items() if len(options) > 1)
    for choices in itertools.product(*(range(len(initial['choices'][tile])) for tile in tiles)):
        record = build(current, region, dict(zip(tiles, choices)))
        assert record['colors'] == initial['colors']
        yield record


def family_controls(max_length):
    controls = []
    witnesses = []
    families = [('straight', length, connected_obstruction(length)) for length in range(max_length+1)]
    families.extend(('bent', length, bent_obstruction(length)) for length in range(1, max_length+1))
    for variant, length, (original, region, right, left) in families:
        region_vertices = {divmod(vertex, original[1]) for tile in region
                           for vertex in graph_record(*original)[0]['vertices'][tile]}
        right_vertices = {divmod(vertex, original[1]) for tile in right
                          for vertex in graph_record(*original)[0]['vertices'][tile]}
        left_vertices = {divmod(vertex, original[1]) for tile in left
                         for vertex in graph_record(*original)[0]['vertices'][tile]}
        for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, transpose, flip_rows, flip_columns)
            current = *shape, selected, matching
            moved = []
            for vertices in (region_vertices, right_vertices, left_vertices):
                points = transformed(*original[:2], vertices, [], transpose, flip_rows, flip_columns)[1]
                moved.append({tile_of(vertex, current[1]) for vertex in points})
            moved_region, moved_right, moved_left = moved
            objective = independent_feasibility(current)
            assert objective == 10+2*length+2*(variant == 'bent') < current[0]*current[1]//2
            residual, components = graph_record(*current)
            component = next(component for component in components if min(moved_region) in component['tiles'])
            assert moved_region <= set(component['tiles'])
            visited = {min(moved_region)}
            queue = list(visited)
            while queue:
                tile = queue.pop()
                for neighbor, _ in residual['neighbors'][tile]:
                    if neighbor in moved_region and neighbor not in visited:
                        visited.add(neighbor)
                        queue.append(neighbor)
            assert visited == moved_region
            decompositions = 0
            for record in all_pairings(current, moved_region):
                assert record['counts'] == collections.Counter(PP=1, SS=1, PS=1)
                assert not record['cycles'] and record['reserve'] == 0
                assert record['terminal']['ports'] == record['terminal']['slack'] == 3
                assert record['terminal']['positive_zero_leaves'] == 0
                assert record['terminal']['shortage_twice'] == 0
                assert sum(residual['deg'][tile]-2*residual['r'][tile] for tile in moved_region) == -3
                terminal_data = terminals(current, moved_region, record)
                right_bounds = cut_bound(current, moved_region, moved_right, terminal_data)
                left_bounds = cut_bound(current, moved_region, moved_left, terminal_data)
                assert right_bounds[('D', 0)] == right_bounds[('D', 1)] == 1
                assert left_bounds[('N', 0)] == left_bounds[('N', 1)] == 1
                assert sum(right_bounds[('D', color)] for color in (0, 1)) > record['debt']
                decompositions += 1
            assert decompositions == 4
            controls.append(dict(variant=variant, length=length, transpose=transpose, flip_rows=flip_rows,
                                 flip_columns=flip_columns, decompositions=decompositions))
        if length in (0, 1, 4):
            record = build(original, region)
            witnesses.append(dict(variant=variant, shape=list(original[:2]), selected=sorted(original[2]),
                                  matching=original[3], region=sorted(region), right_cut=sorted(right),
                                  left_cut=sorted(left), strand_counts=dict(record['counts']),
                                  region_charge=-1.5, shortage=0, reserve=0))
    return dict(straight_length_range=[0, max_length], bent_length_range=[1, max_length],
                physical_symmetry_controls=len(controls),
                full_pairing_decompositions=4*len(controls), witnesses=witnesses)


def exhaustive():
    reports = []
    for rows, columns in ((2, 2), (2, 4), (4, 2), (2, 6), (6, 2)):
        feasible_pairs = regions = decompositions = cuts = ownership = 0
        for selected_mask, matching in pairs(rows, columns):
            current = rows, columns, {divmod(vertex, columns) for vertex in range(rows*columns)
                                      if selected_mask >> vertex & 1}, [tuple(divmod(vertex, columns) for vertex in edge)
                                                                       for edge in matching]
            residual, _ = graph_record(*current)
            deficient = [tile for tile in range(residual['N']) if residual['t'][tile] < 2]
            for region_mask in range(1, 1 << len(deficient)):
                region = {tile for index, tile in enumerate(deficient) if region_mask >> index & 1}
                ordered = sorted(region)
                for record in all_pairings(current, region):
                    terminal_data = terminals(current, region, record)
                    for cut_mask in range(1, 1 << len(ordered)):
                        subset = {tile for index, tile in enumerate(ordered) if cut_mask >> index & 1}
                        bounds = cut_bound(current, region, subset, terminal_data)
                        complementary = cut_bound(current, region, region-subset, terminal_data)
                        for color in (0, 1):
                            assert bounds[('D', color)]+complementary[('D', color)] <= record['debt']
                            assert bounds[('N', color)]+complementary[('N', color)] <= record['counts']['SS']
                        cuts += 1
                    singleton = [cut_bound(current, region, {tile}, terminal_data) for tile in ordered]
                    for color in (0, 1):
                        assert sum(bounds[('D', color)] for bounds in singleton) <= record['debt']
                        assert sum(bounds[('N', color)] for bounds in singleton) <= record['counts']['SS']
                    ownership += 1
                    decompositions += 1
                regions += 1
            feasible_pairs += 1
        reports.append(dict(shape=[rows, columns], feasible_pairs=feasible_pairs,
                            deficient_regions=regions, full_pairing_decompositions=decompositions,
                            directed_cuts=cuts, disjoint_singleton_allocations=ownership))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-length', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_length < 4:
        parser.error('--max-length must be at least four')
    family = family_controls(args.max_length)
    report = dict(status='ALL_CHECKS_PASSED', family=family, exhaustive=exhaustive())
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/MIXED_COLOR_CUT_OBSTRUCTION.md']
    sources.extend(Path(__file__).with_name(name) for name in ('check_strand_switches.py',
        'check_terminal_strands.py', 'check_residual_corridors.py', 'check_residual_cycle_pruning.py',
        'verify_grid_short_path_compensation.py'))
    report['sha256'] = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest() for path in sources}
    report['scope'] = 'Physical controls of written arbitrary-size cut bounds and all-length balanced obstruction; no target-grid counterexample, universal coefficient improvement or new Lean proof.'
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], exhaustive=report['exhaustive'],
                         family={key: value for key, value in family.items() if key != 'witnesses'})))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
