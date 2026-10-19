"""Physical-grid controls and independent assignments for shared blank witnesses."""

import argparse
import itertools
import json
from pathlib import Path

from check_attachment_collar_compensation import (
    image_marked, incoming_witness, internal_debt_path, regional_record, thick_receiver,
)
from check_pressured_collar_compensation import DIRECTIONS, FACES, region_vertices
from check_residual_corridors import graph_record, transformed


def witness_record(current, tiles, marked):
    rows, columns, selected, matching = current
    record = regional_record(current, tiles, marked)
    graph, _ = graph_record(*current)
    occupied = selected | {vertex for edge in matching for vertex in edge}
    tile_of = lambda vertex: (vertex[0]//2, vertex[1]//2)
    tile_index = lambda tile: tile[0]*(columns//2)+tile[1]
    saturated = {tile for tile in tiles if graph['t'][tile_index(tile)] == 2}
    marked_sides = dict(marked)
    free = set()
    for tile in tiles-saturated:
        vertices = region_vertices({tile})
        blanks = vertices-occupied
        cap = set()
        if tile in marked_sides:
            cap = {(2*tile[0]+corner//2, 2*tile[1]+corner % 2)
                   for corner in FACES[marked_sides[tile]]}
        reserved = set(cap)
        chosen = vertices & selected
        if chosen:
            assert len(chosen) == 1
            selected_vertex = next(iter(chosen))
            candidates = {vertex for vertex in blanks-cap
                          if sum(abs(vertex[axis]-selected_vertex[axis]) for axis in (0, 1)) == 1}
            assert candidates
            reserved.add(min(candidates))
        assert reserved <= blanks
        assert len(reserved) == len(chosen)+2*(tile in marked_sides)
        free |= blanks-reserved
    owners = set()
    region = region_vertices(tiles)
    for first, second in matching:
        if first not in region or second not in region:
            continue
        first_tile, second_tile = tile_of(first), tile_of(second)
        if first_tile in saturated and second_tile not in saturated:
            owners.add(first_tile)
        elif second_tile in saturated and first_tile not in saturated:
            owners.add(second_tile)
    assert len(owners) == record['internal_attachments']
    adjacency = {owner:set() for owner in owners}
    blank_owners = {blank:set() for blank in free}
    for owner in owners:
        for vertex in selected & region_vertices({owner}):
            for vertical, horizontal in DIRECTIONS:
                blank = vertex[0]+vertical, vertex[1]+horizontal
                if blank in free:
                    assert tile_of(blank) != owner
                    adjacency[owner].add(blank)
                    blank_owners[blank].add(owner)
    assert max(map(len, blank_owners.values()), default=0) <= 2
    shared = [(blank, tuple(sorted(attached))) for blank, attached in blank_owners.items() if len(attached) == 2]
    private = {blank:next(iter(attached)) for blank, attached in blank_owners.items() if len(attached) == 1}
    unused = {blank for blank, attached in blank_owners.items() if not attached}
    neighbors = {owner:[] for owner in owners}
    for blank, (first, second) in shared:
        neighbors[first].append((second, blank))
        neighbors[second].append((first, blank))
    components = []
    visited = set()
    for start in sorted(owners):
        if start in visited:
            continue
        component = {start}
        visited.add(start)
        pending = [start]
        while pending:
            owner = pending.pop()
            for neighbor, _ in neighbors[owner]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    component.add(neighbor)
                    pending.append(neighbor)
        edge_count = sum(len(neighbors[owner]) for owner in component)//2
        private_count = sum(owner in component for owner in private.values())
        cycle_rank = edge_count-len(component)+1
        assert cycle_rank >= 0
        components.append(dict(owners=sorted(component), shared=edge_count,
                               private=private_count, cycle_rank=cycle_rank,
                               deficit=int(cycle_rank == 0 and private_count == 0)))
    mate = {}

    def augment(owner, seen):
        for blank in sorted(adjacency[owner]):
            if blank in seen:
                continue
            seen.add(blank)
            if blank not in mate or augment(mate[blank], seen):
                mate[blank] = owner
                return True
        return False

    for owner in sorted(owners):
        augment(owner, set())
    bad = sum(component['deficit'] for component in components)
    assert len(mate) == len(owners)-bad
    assert len(set(mate.values())) == len(mate)
    assert all(blank in adjacency[owner] for blank, owner in mate.items())
    cycle_rank = sum(component['cycle_rank'] for component in components)
    assert len(free) == record['deficient_surplus']-2*len(marked)
    assert len(free) == len(shared)+len(private)+len(unused)
    assert len(shared)+len(components) == len(owners)+cycle_rank
    assert record['charge_twice'] == -2*len(marked)+record['outgoing_saturated_attachments']+len(components)-cycle_rank-len(private)-len(unused)
    if all(len(candidates) >= 2 for candidates in adjacency.values()):
        assert len(mate) == len(owners)
        assert record['charge_twice'] <= -2*len(marked)+record['outgoing_saturated_attachments']
    return dict(regional=record, free_blanks=len(free), owners=len(owners),
                shared_edges=len(shared), private_blanks=len(private), unused_blanks=len(unused),
                component_count=len(components), cycle_rank=cycle_rank, unmatched_debts=bad,
                assigned_debts=len(mate), components=components,
                incidence=[dict(blank=blank, owners=sorted(attached)) for blank, attached in sorted(blank_owners.items())],
                assignment=[dict(blank=blank, owner=owner) for blank, owner in sorted(mate.items())])


def staircase(size, repair):
    assert size >= 2 and repair in ('none', 'private', 'cycle')
    saturated = [(1+index, size-index) for index in range(size)]
    deficient = [(2+index, size-index) for index in range(size-1)]
    corner = lambda tile, position: (2*tile[0]+position//2, 2*tile[1]+position % 2)
    selected = {corner(tile, position) for tile in saturated for position in (1, 2)}
    matching = [(corner(saturated[0], 3), corner(deficient[0], 1))]
    matching += [(corner(saturated[index], 3), corner(deficient[index-1], 2)) for index in range(1, size)]
    matching += [(corner(tile, 1), corner(tile, 3)) for tile in deficient[1:]]
    last = corner(deficient[0], 3)
    matching.append((last, (last[0], last[1]+1)))
    tiles = set(saturated+deficient)
    if repair != 'none':
        added = (0, size) if repair == 'private' else (1, size-1)
        tiles.add(added)
        matching.append((corner(added, 0), corner(added, 2)))
        start = corner(added, 1)
        end = (start[0], start[1]+1) if repair == 'private' else (start[0]-1, start[1])
        matching.append((start, end))
    return (2*size+4, 2*size+6, selected, matching), tiles, []


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-size', type=int, default=24)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert arguments.max_size >= 2
    fixtures = []
    symmetry_images = 0
    for size in range(2, arguments.max_size+1):
        for repair in ('none', 'private', 'cycle'):
            current, tiles, marked = staircase(size, repair)
            record = witness_record(current, tiles, marked)
            assert record['owners'] == size and record['component_count'] == 1
            assert record['unused_blanks'] == 0
            assert record['regional']['charge_twice'] == int(repair == 'none')
            assert record['private_blanks'] == int(repair == 'private')
            assert record['cycle_rank'] == int(repair == 'cycle')
            assert record['unmatched_debts'] == int(repair == 'none')
            assert record['regional']['objective'] == 4*size-1+2*(repair != 'none')
            for symmetry in itertools.product((False, True), repeat=3):
                shape, chosen, matching = transformed(*current, *symmetry)
                moved = transformed(*current[:2], region_vertices(tiles), [], *symmetry)[1]
                image_tiles = {(row//2, column//2) for row, column in moved}
                image = witness_record((*shape, chosen, matching), image_tiles, image_marked(current, marked, symmetry))
                for key in ('free_blanks', 'owners', 'shared_edges', 'private_blanks', 'unused_blanks',
                            'component_count', 'cycle_rank', 'unmatched_debts', 'assigned_debts'):
                    assert image[key] == record[key], key
                symmetry_images += 1
            fixtures.append(dict(size=size, repair=repair, record=record))
    inherited = []
    for length in range(41):
        current, tiles, marked = internal_debt_path(length)
        inherited.append(witness_record(current, tiles, marked))
    for builder in (incoming_witness, thick_receiver):
        for option in (False, True):
            current, tiles, marked = builder(option)
            inherited.append(witness_record(current, tiles, marked))
    report = dict(status='ALL_CHECKS_PASSED', staircase_regions=len(fixtures),
                  staircase_symmetry_images=symmetry_images, inherited_regions=len(inherited),
                  maximum_staircase_size=arguments.max_size, fixtures=fixtures, inherited=inherited,
                  scope='Finite physical and maximum-assignment controls; general witness multiplicity, graph allocation and all-size staircase/repair proofs are written separately.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in {'fixtures', 'inherited'}}))


if __name__ == '__main__':
    main()
