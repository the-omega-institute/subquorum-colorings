"""Independent grid controls for single and alternating-cycle promotions."""

import argparse
import itertools
import json
from pathlib import Path

from check_blank_witness_compensation import witness_record
from check_pressured_collar_compensation import local_valid, region_vertices
from check_residual_corridors import direct_check, transformed
from verify_grid_five_sixths import bits, pairs


def neighbors(vertex):
    row, column = vertex
    return ((row-1, column), (row+1, column), (row, column-1), (row, column+1))


def occupied_degrees(current):
    occupied = current[2] | {vertex for edge in current[3] for vertex in edge}
    return {vertex: sum(adjacent in occupied for adjacent in neighbors(vertex))
            for edge in current[3] for vertex in edge}


def singles(current):
    degrees = occupied_degrees(current)
    return sorted((endpoint, mate) for edge in current[3]
                  for endpoint, mate in (edge, edge[::-1]) if degrees[endpoint] <= 2)


def dependency_graph(current, color):
    degrees = occupied_degrees(current)
    candidates = {}
    for edge in current[3]:
        endpoint, mate = edge if sum(edge[0]) % 2 == color else edge[::-1]
        assert sum(endpoint) % 2 == color and sum(mate) % 2 != color
        if degrees[endpoint] == 3:
            candidates[endpoint] = mate
    mate_owners = {mate: endpoint for endpoint, mate in candidates.items()}
    adjacency = {endpoint: sorted(mate_owners[adjacent] for adjacent in neighbors(endpoint)
                                 if adjacent in mate_owners and mate_owners[adjacent] != endpoint)
                 for endpoint in candidates}
    return candidates, adjacency


def directed_cycle(adjacency):
    finished = set()
    for root in sorted(adjacency):
        if root in finished:
            continue
        path = [root]
        positions = {root: 0}
        pending = [iter(adjacency[root])]
        while pending:
            successor = next(pending[-1], None)
            if successor is None:
                completed = path.pop()
                finished.add(completed)
                del positions[completed]
                pending.pop()
            elif successor in positions:
                return path[positions[successor]:]
            elif successor not in finished:
                positions[successor] = len(path)
                path.append(successor)
                pending.append(iter(adjacency[successor]))
    return []


def apply_bundle(current, bundle):
    assert bundle and len({frozenset(edge) for edge in bundle}) == len(bundle)
    removed_edges = {frozenset(edge) for edge in bundle}
    assert removed_edges <= {frozenset(edge) for edge in current[3]}
    promoted = {endpoint for endpoint, _ in bundle}
    removed = {mate for _, mate in bundle}
    assert not promoted & removed
    before_occupied = current[2] | {vertex for edge in current[3] for vertex in edge}
    after = (*current[:2], current[2] | promoted,
             [edge for edge in current[3] if frozenset(edge) not in removed_edges])
    after_occupied = after[2] | {vertex for edge in after[3] for vertex in edge}
    assert after_occupied == before_occupied-removed
    assert direct_check(*current) == direct_check(*after)
    assert len(after[2]) == len(current[2])+len(bundle)
    assert len(after[3]) == len(current[3])-len(bundle)
    return after


def normalize(current):
    original_edges = len(current[3])
    moves = []
    while True:
        eligible = singles(current)
        if eligible:
            bundle = [eligible[0]]
            kind = 'single'
        else:
            bundle = []
            for color in (0, 1):
                candidates, adjacency = dependency_graph(current, color)
                cycle = directed_cycle(adjacency)
                if cycle:
                    assert len(cycle) >= 2 and len(cycle) == len(set(cycle))
                    assert all(cycle[(index+1) % len(cycle)] in adjacency[endpoint]
                               for index, endpoint in enumerate(cycle))
                    bundle = [(endpoint, candidates[endpoint]) for endpoint in cycle]
                    break
            kind = 'cycle'
        if not bundle:
            break
        current = apply_bundle(current, bundle)
        moves.append(dict(kind=kind, promoted=[endpoint for endpoint, _ in bundle]))
    assert len(moves) <= original_edges
    assert not singles(current)
    assert all(not directed_cycle(dependency_graph(current, color)[1]) for color in (0, 1))
    return current, moves


def mixed_diamonds(size):
    assert size >= 1
    base_selected = {(0, 0), (0, 2), (2, 3), (3, 0), (3, 2),
                     (4, 1), (4, 3), (5, 0), (7, 1), (7, 3)}
    base_matching = [((2, 2), (2, 1)), ((2, 0), (1, 0)), ((1, 1), (1, 2)),
                     ((5, 1), (5, 2)), ((5, 3), (6, 3)), ((6, 1), (6, 2))]
    selected = {(row+8*index, column) for index in range(size) for row, column in base_selected}
    matching = [tuple((row+8*index, column) for row, column in edge)
                for index in range(size) for edge in base_matching]
    tiles = {(4*index+row, column) for index in range(size)
             for row in (1, 2) for column in (0, 1)}
    tiles |= {(4*index+row, 1) for index in range(size-1) for row in (3, 4)}
    return (8*size, 4, selected, matching), tiles


def explicit_absorption(current):
    size = current[0]//8
    for index in range(size):
        offset = 8*index
        shift = lambda vertex: (vertex[0]+offset, vertex[1])
        for bundle in (
                [((2, 1), (2, 2)), ((1, 2), (1, 1))],
                [((1, 0), (2, 0))],
                [((5, 2), (5, 1)), ((6, 1), (6, 2))],
                [((6, 3), (5, 3))]):
            current = apply_bundle(current, [(shift(endpoint), shift(mate)) for endpoint, mate in bundle])
    assert not current[3] and len(current[2]) == 16*size
    return current


def gap_controls():
    checked = normalized_cases = pressured_cases = 0
    internal = ((1, 2), (0, 3), (0, 3), (1, 2))
    for labels in itertools.product(range(3), repeat=4):
        checked += 1
        if labels.count(1) > 1:
            continue
        if labels[3] == 0 and local_valid(labels, ()) and all(
                sum(labels[adjacent] != 0 for adjacent in internal[corner]) >= 2
                for corner in (1, 2) if labels[corner] == 2):
            assert labels.count(0) >= labels.count(1)+1
            normalized_cases += 1
        if labels[0] == 0 and local_valid(labels, (0, 3)):
            assert labels.count(0) >= labels.count(1)+1
            pressured_cases += 1
    return dict(ternary_states=checked, normalized_gap_states=normalized_cases,
                pressured_gap_states=pressured_cases)


def connected(tiles):
    unseen = set(tiles)
    pending = [unseen.pop()]
    while pending:
        tile = pending.pop()
        for adjacent in neighbors(tile):
            if adjacent in unseen:
                unseen.remove(adjacent)
                pending.append(adjacent)
    return not unseen


def family_controls(max_size):
    records = []
    images = 0
    for size in range(1, max_size+1):
        current, tiles = mixed_diamonds(size)
        assert direct_check(*current) == 16*size
        assert connected(tiles) and len(tiles) == 6*size-2
        assert not singles(current)
        assert min(occupied_degrees(current).values()) == 3
        record = witness_record(current, tiles, [])
        regional = record['regional']
        for key, value in dict(charge_twice=size+1, saturated_endpoints=2*size,
                               internal_attachments=2*size, deficient_surplus=size-1,
                               crossing=3*size-1, outgoing_saturated_attachments=0,
                               incoming_saturated_attachments=0).items():
            assert regional[key] == value, (size, key, regional[key], value)
        for key, value in dict(owners=2*size, component_count=2*size, cycle_rank=0,
                               shared_edges=0, private_blanks=size-1, unused_blanks=0).items():
            assert record[key] == value, (size, key, record[key], value)
        assert direct_check(*explicit_absorption(current)) == 16*size
        ending, moves = normalize(current)
        assert not ending[3] and len(ending[2]) == 16*size
        assert sum(move['kind'] == 'cycle' for move in moves) == 2*size
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            image = (*shape, selected, matching)
            moved = transformed(*current[:2], region_vertices(tiles), [], *symmetry)[1]
            moved_tiles = {(row//2, column//2) for row, column in moved}
            assert not singles(image)
            image_record = witness_record(image, moved_tiles, [])
            for key in ('charge_twice', 'deficient_surplus', 'internal_attachments', 'crossing'):
                assert image_record['regional'][key] == regional[key]
            ending, _ = normalize(image)
            assert not ending[3] and len(ending[2]) == 16*size
            images += 1
        records.append(dict(size=size, regional=regional, cycle_moves=2*size,
                            final_selected=16*size))
    return records, images


def exhaustive_controls():
    records = []
    for columns in (2, 4, 6):
        examined = singles_count = cycles_count = 0
        for selected_mask, _, matching_indices in pairs(2, columns):
            current = (2, columns, {divmod(vertex, columns) for vertex in bits(selected_mask)},
                       [(divmod(first, columns), divmod(second, columns))
                        for first, second in matching_indices])
            ending, moves = normalize(current)
            assert current[2] <= ending[2]
            assert direct_check(*current) == direct_check(*ending)
            examined += 1
            singles_count += sum(move['kind'] == 'single' for move in moves)
            cycles_count += sum(move['kind'] == 'cycle' for move in moves)
        records.append(dict(columns=columns, feasible_pairs=examined,
                            single_moves=singles_count, cycle_moves=cycles_count))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-size', type=int, default=32)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    family, images = family_controls(arguments.max_size)
    result = dict(scope='Finite controls; all-size proofs are in the accompanying note.',
                  local_gaps=gap_controls(), family=family, symmetry_images=images,
                  exhaustive=exhaustive_controls(),
                  global_grid_target_refuted=False, full_lean_formalization=False)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(family_sizes=len(family), symmetry_images=images,
                          exhaustive_pairs=sum(record['feasible_pairs'] for record in result['exhaustive']),
                          local_gaps=result['local_gaps'])))


if __name__ == '__main__':
    main()
