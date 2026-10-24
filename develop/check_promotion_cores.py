"""Threshold cores and frozen-endpoint certificates for promotion bundles."""

import argparse
import collections
import itertools
import json
import random
from pathlib import Path

from check_blank_witness_compensation import witness_record
from check_cooperative_promotion import (
    apply_bundle, connected, dependency_graph, directed_cycle, neighbors, occupied_degrees,
)
from check_pressured_collar_compensation import region_vertices
from check_residual_corridors import direct_check, transformed
from verify_grid_five_sixths import bits, pairs

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def color_data(current, color):
    degrees = occupied_degrees(current)
    candidates = {}
    for edge in current[3]:
        endpoint, mate = edge if sum(edge[0]) % 2 == color else edge[::-1]
        assert sum(endpoint) % 2 == color and sum(mate) % 2 != color
        candidates[endpoint] = mate
    mate_owners = {mate: endpoint for endpoint, mate in candidates.items()}
    adjacency = {endpoint: {mate_owners[adjacent] for adjacent in neighbors(endpoint)
                            if adjacent in mate_owners and mate_owners[adjacent] != endpoint}
                 for endpoint in candidates}
    needs = {endpoint: max(0, degrees[endpoint]-2) for endpoint in candidates}
    return candidates, adjacency, needs


def peel(adjacency, needs, reverse=False):
    remaining = set(adjacency)
    counts = {vertex: len(adjacent) for vertex, adjacent in adjacency.items()}
    predecessors = {vertex: set() for vertex in adjacency}
    for vertex, adjacent in adjacency.items():
        for successor in adjacent:
            predecessors[successor].add(vertex)
    pending = collections.deque(sorted((vertex for vertex in remaining
                                        if counts[vertex] < needs[vertex]), reverse=reverse))
    removals = []
    while pending:
        vertex = pending.popleft()
        if vertex not in remaining:
            continue
        assert counts[vertex] < needs[vertex]
        removals.append(dict(vertex=vertex, surviving_neighbors=counts[vertex], need=needs[vertex]))
        remaining.remove(vertex)
        for predecessor in sorted(predecessors[vertex], reverse=reverse):
            if predecessor in remaining:
                counts[predecessor] -= 1
                if counts[predecessor] < needs[predecessor]:
                    pending.append(predecessor)
    assert all(len(adjacency[vertex] & remaining) >= needs[vertex] for vertex in remaining)
    return remaining, removals


def normalize(current):
    moves = []
    while True:
        bundle = []
        for color in (0, 1):
            candidates, adjacency, needs = color_data(current, color)
            core, _ = peel(adjacency, needs)
            if core:
                bundle = [(endpoint, candidates[endpoint]) for endpoint in sorted(core)]
                break
        if not bundle:
            return current, moves
        current = apply_bundle(current, bundle)
        moves.append(dict(color=color, promoted=[endpoint for endpoint, _ in bundle]))


def frozen_certificate(current):
    mates = {endpoint: mate for edge in current[3] for endpoint, mate in (edge, edge[::-1])}
    frozen = set()
    layers = []
    while True:
        kept = current[2] | {endpoint for endpoint, mate in mates.items() if mate in frozen}
        newly_frozen = {endpoint for endpoint in mates if endpoint not in frozen
                        and sum(adjacent in kept for adjacent in neighbors(endpoint)) >= 2}
        if not newly_frozen:
            break
        witnesses = [dict(endpoint=endpoint,
                          kept_neighbors=sorted(adjacent for adjacent in neighbors(endpoint) if adjacent in kept)[:2])
                     for endpoint in sorted(newly_frozen)]
        layers.append(witnesses)
        frozen |= newly_frozen
    return frozen, layers


def anchored_diamonds(size):
    assert size >= 1
    base_selected = {(1, 1), (1, 3), (2, 0), (2, 5), (3, 2), (3, 4),
                     (4, 3), (4, 5), (5, 2), (5, 7), (6, 4), (6, 6)}
    base_matching = [((2, 4), (2, 3)), ((2, 2), (2, 1)),
                     ((5, 3), (5, 4)), ((5, 5), (5, 6))]
    selected = {(row+6*index, column) for index in range(size) for row, column in base_selected}
    matching = [tuple((row+6*index, column) for row, column in edge)
                for index in range(size) for edge in base_matching]
    tiles = {(3*index+row, column) for index in range(size)
             for row in (1, 2) for column in (1, 2)}
    tiles |= {(3*index+3, 1) for index in range(size-1)}
    return (6*size+2, 8, selected, matching), tiles


def degree_four_patch():
    selected = {(0, 2), (1, 1), (1, 6), (7, 2), (7, 6)}
    matching = [((1, 2), (2, 2)), ((2, 3), (2, 4)), ((2, 5), (2, 6)),
                ((3, 2), (4, 2)), ((5, 2), (6, 2))]
    matching += [((row, column), (row, column+1))
                 for row in range(3, 7) for column in (3, 5)]
    return 8, 8, selected, matching


def tight_diamond():
    labels = ('TBTBTTBT', 'BTBTBBTB', 'TPPPPTBT', 'BBTBTBTB',
              'TTBTBTBB', 'BBTPPPPT', 'TTBBTBTB', 'BBTTBTBT')
    current, tiles = anchored_diamonds(1)
    selected = {(row, column) for row, line in enumerate(labels)
                for column, label in enumerate(line) if label == 'T'}
    endpoints = {(row, column) for row, line in enumerate(labels)
                 for column, label in enumerate(line) if label == 'P'}
    assert current[2] <= selected
    assert endpoints == {vertex for edge in current[3] for vertex in edge}
    return (*current[:2], selected, current[3]), tiles


def feasible_bundle(current, bundle):
    if not bundle:
        return True
    remaining = current[2] | {vertex for edge in current[3] for vertex in edge}
    remaining -= {mate for _, mate in bundle}
    return all(sum(adjacent in remaining for adjacent in neighbors(endpoint)) <= 1
               for endpoint, _ in bundle)


def exact_color_controls(current):
    examined = 0
    for color in (0, 1):
        candidates, adjacency, needs = color_data(current, color)
        core, _ = peel(adjacency, needs)
        assert core == peel(adjacency, needs, reverse=True)[0]
        vertices = sorted(candidates)
        union = set()
        for mask in range(1 << len(vertices)):
            subset = {vertex for index, vertex in enumerate(vertices) if mask >> index & 1}
            bundle = [(endpoint, candidates[endpoint]) for endpoint in subset]
            actual = feasible_bundle(current, bundle)
            threshold = all(len(adjacency[endpoint] & subset) >= needs[endpoint] for endpoint in subset)
            assert actual == threshold
            if actual:
                assert subset <= core
                union |= subset
            examined += 1
        assert core == union
        if core:
            apply_bundle(current, [(endpoint, candidates[endpoint]) for endpoint in core])
    return examined


def all_oriented_bundles(current):
    assert len(current[3]) <= 8
    feasible = examined = 0
    for states in itertools.product((0, 1, 2), repeat=len(current[3])):
        bundle = [edge if state == 1 else edge[::-1]
                  for edge, state in zip(current[3], states) if state]
        if not bundle:
            continue
        examined += 1
        if feasible_bundle(current, bundle):
            apply_bundle(current, bundle)
            feasible += 1
    return examined, feasible


def family_controls(max_size):
    records = []
    images = 0
    for size in range(1, max_size+1):
        current, tiles = anchored_diamonds(size)
        assert direct_check(*current) == 16*size
        assert len(current[2]) == 12*size and len(current[3]) == 4*size
        assert set(occupied_degrees(current).values()) == {3}
        assert connected(tiles) and len(tiles) == 5*size-1
        frozen, layers = frozen_certificate(current)
        assert frozen == {vertex for edge in current[3] for vertex in edge}
        assert [len(layer) for layer in layers] == [4*size, 4*size]
        assert all(not directed_cycle(dependency_graph(current, color)[1]) for color in (0, 1))
        assert all(not peel(*color_data(current, color)[1:])[0] for color in (0, 1))
        ending, moves = normalize(current)
        assert not moves and ending == current
        record = witness_record(current, tiles, [])
        for key, value in dict(charge_twice=2, deficient_surplus=2*size-2,
                               saturated_endpoints=2*size, internal_attachments=2*size,
                               crossing=2*size, outgoing_saturated_attachments=0,
                               incoming_saturated_attachments=0).items():
            assert record['regional'][key] == value, (size, key, record['regional'][key])
        for key, value in dict(owners=2*size, component_count=2*size,
                               shared_edges=0, cycle_rank=0, private_blanks=size-1,
                               unused_blanks=size-1, free_blanks=2*size-2).items():
            assert record[key] == value, (size, key, record[key])
        donor = {(0, 1)}
        assert not donor & tiles
        assert witness_record(current, donor, [])['regional']['charge_twice'] == -2
        assert witness_record(current, tiles | donor, [])['regional']['charge_twice'] == 0
        anchored_donors = {(3*index+row, column) for index in range(size)
                           for row, column in ((1, 0), (2, 3))}
        assert len(anchored_donors) == 2*size and not anchored_donors & tiles
        assert all(witness_record(current, {tile}, [])['regional']['charge_twice'] == -1
                   for tile in anchored_donors)
        assert witness_record(current, tiles | anchored_donors, [])['regional']['charge_twice'] == 2-2*size
        for symmetry in itertools.product((False, True), repeat=3):
            shape, chosen, matching = transformed(*current, *symmetry)
            image = (*shape, chosen, matching)
            assert direct_check(*image) == 16*size
            assert len(frozen_certificate(image)[0]) == 8*size
            moved = transformed(*current[:2], region_vertices(tiles), [], *symmetry)[1]
            moved_tiles = {(row//2, column//2) for row, column in moved}
            assert witness_record(image, moved_tiles, [])['regional']['charge_twice'] == 2
            moved_donor = transformed(*current[:2], region_vertices(donor), [], *symmetry)[1]
            donor_tiles = {(row//2, column//2) for row, column in moved_donor}
            assert not donor_tiles & moved_tiles
            assert witness_record(image, donor_tiles, [])['regional']['charge_twice'] == -2
            assert witness_record(image, donor_tiles | moved_tiles, [])['regional']['charge_twice'] == 0
            images += 1
        records.append(dict(size=size, tiles=len(tiles), charge_twice=2,
                            occupied_degrees=[3], frozen_layer_sizes=[len(layer) for layer in layers],
                            deficient_surplus=2*size-2, private_blanks=size-1,
                            unused_blanks=size-1, objective=16*size,
                            whole_grid_charge_twice=-16*size-16,
                            one_tile_donor_charge_twice=-2, repaired_charge_twice=0))
    literal = []
    for size in (1, 2):
        current, _ = anchored_diamonds(size)
        examined, feasible = all_oriented_bundles(current)
        assert not feasible
        literal.append(dict(size=size, nonempty_oriented_bundles=examined, feasible=feasible))
    return records, images, literal


def exhaustive_controls():
    records = []
    for columns in (2, 4, 6):
        examined = subsets = moves_count = 0
        for selected_mask, _, matching_indices in pairs(2, columns):
            current = (2, columns, {divmod(vertex, columns) for vertex in bits(selected_mask)},
                       [(divmod(first, columns), divmod(second, columns))
                        for first, second in matching_indices])
            subsets += exact_color_controls(current)
            ending, moves = normalize(current)
            assert direct_check(*ending) == direct_check(*current)
            frozen, _ = frozen_certificate(current)
            assert not frozen & {vertex for move in moves for vertex in move['promoted']}
            examined += 1
            moves_count += len(moves)
        records.append(dict(columns=columns, feasible_pairs=examined,
                            color_subsets=subsets, core_promotions=moves_count))
    return records


def random_controls():
    generator = random.Random(20261019)
    records = []
    for _ in range(400):
        selected = set()
        matching = []
        available = {(row, column) for row in range(4) for column in range(4)}
        vertices = sorted(available)
        generator.shuffle(vertices)
        for vertex in vertices:
            if vertex not in available:
                continue
            available.remove(vertex)
            options = [None, 'selected']+sorted(set(neighbors(vertex)) & available)
            generator.shuffle(options)
            for option in options:
                candidate = (4, 4, selected | ({vertex} if option == 'selected' else set()),
                             matching+([(vertex, option)] if isinstance(option, tuple) else []))
                try:
                    direct_check(*candidate)
                except AssertionError:
                    continue
                selected, matching = candidate[2:]
                if isinstance(option, tuple):
                    available.remove(option)
                break
        current = (4, 4, selected, matching)
        records.append(exact_color_controls(current))
        normalize(current)
    return dict(grids=len(records), color_subsets=sum(records))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-size', type=int, default=32)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert arguments.max_size >= 1
    family, images, literal = family_controls(arguments.max_size)
    current = degree_four_patch()
    assert direct_check(*current) == 18
    candidates, adjacency, needs = color_data(current, 1)
    core, removals = peel(adjacency, needs)
    assert len(core) == 12 and len(removals) == 1
    degree_four = sum(occupied_degrees(current)[endpoint] == 4 for endpoint in core)
    assert degree_four > 0
    changed = apply_bundle(current, [(endpoint, candidates[endpoint]) for endpoint in core])
    assert len(changed[3]) == 1 and len(changed[2]) == 17
    abstract = {vertex: set(range(4))-{vertex} for vertex in range(4)}
    assert peel(abstract, {vertex: 2 for vertex in range(4)})[0] == set(range(4))
    tight, tight_tiles = tight_diamond()
    assert direct_check(*tight) == 32 and len(tight[2]) == 28
    assert len(frozen_certificate(tight)[0]) == 8
    assert set(occupied_degrees(tight).values()) == {3}
    assert all(not peel(*color_data(tight, color)[1:])[0] for color in (0, 1))
    assert witness_record(tight, tight_tiles, [])['regional']['charge_twice'] == 2
    tight_charges = [dict(tile=(row, column), charge_twice=record['regional']['charge_twice'])
                    for row in range(4) for column in range(4)
                    if (record := witness_record(tight, {(row, column)}, []))['regional']['charge_twice']]
    assert sorted(entry['charge_twice'] for entry in tight_charges) == [-1, -1, 1, 1]
    assert all_oriented_bundles(tight) == (80, 0)
    assert witness_record(tight, tight_tiles | {(1, 0), (2, 3)}, [])['regional']['charge_twice'] == 0
    for row in range(8):
        for column in range(8):
            vertex = row, column
            if vertex in tight[2] | {endpoint for edge in tight[3] for endpoint in edge}:
                continue
            try:
                direct_check(*tight[:2], tight[2] | {vertex}, tight[3])
            except AssertionError:
                continue
            raise AssertionError('The tight selected set was not inclusion-maximal.')
    result = dict(scope='Finite controls; general proofs are in PROMOTION_CORES_AND_ANCHORED_OBSTRUCTIONS.md.',
                  family=family, symmetry_images=images, literal_oriented_bundles=literal,
                  exhaustive=exhaustive_controls(), random=random_controls(),
                  degree_four_patch=dict(promoted=len(core), degree_four_endpoints=degree_four,
                                         final_selected=17, final_matching=1),
                  tight_diamond=dict(selected=28, matching=4, objective=32,
                                     regional_charge_twice=2, nonzero_tile_charges=tight_charges,
                                     frozen_endpoints=8, nonempty_oriented_bundles=80, feasible_bundles=0),
                  abstract_K44_core_size=4, grid_target_refuted=False,
                  maximal_selected_among_objective_maximizers_claimed=False)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(family_sizes=len(family), symmetry_images=images,
                          feasible_pairs=sum(record['feasible_pairs'] for record in result['exhaustive']),
                          color_subsets=sum(record['color_subsets'] for record in result['exhaustive']),
                          random=result['random'], literal=literal,
                          degree_four_patch=result['degree_four_patch'])))


if __name__ == '__main__':
    main()
