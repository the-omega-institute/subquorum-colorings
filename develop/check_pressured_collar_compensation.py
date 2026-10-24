"""Independent local-state and physical-grid controls for pressured collars."""

import argparse
import itertools
import json
from pathlib import Path

from check_mixed_band_boundary_obstacle import general_region_ledger
from check_residual_corridors import direct_check, graph_record, transformed


FACES = ((0, 1), (1, 3), (2, 3), (0, 2))
NEIGHBORS = ((1, 2), (0, 3), (0, 3), (1, 2))
DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))


def local_valid(labels, sides):
    return all(sum(labels[neighbor] != 0 for neighbor in NEIGHBORS[corner])+
               sum(corner in FACES[side] for side in sides) <= 1
               for corner in range(4) if labels[corner] == 1)


def local_controls():
    pressured = terminal = 0
    for labels in itertools.product(range(3), repeat=4):
        for mask in range(1, 16):
            sides = [side for side in range(4) if mask >> side & 1]
            if local_valid(labels, sides):
                assert labels.count(0) >= labels.count(1)
                assert labels.count(1) != 2 or labels.count(2) == 0
                pressured += 1
        for side in range(4):
            if all(labels[corner] == 0 for corner in FACES[side]) and local_valid(
                    labels, ((side+1) % 4, (side+3) % 4)):
                assert labels.count(0)-labels.count(1) >= 2
                terminal += 1
    return dict(valid_pressured_states=pressured, valid_oriented_terminal_states=terminal)


def neighbors(vertex):
    return [(vertex[0]+vertical, vertex[1]+horizontal) for vertical, horizontal in DIRECTIONS]


def region_vertices(tiles):
    return {(2*tile_row+vertical, 2*tile_column+horizontal)
            for tile_row, tile_column in tiles for vertical, horizontal in itertools.product(range(2), repeat=2)}


def cap_vertices(tiles):
    caps = set()
    leaves = 0
    for tile in tiles:
        adjacent = [(side, neighbor) for side, neighbor in enumerate(neighbors(tile)) if neighbor in tiles]
        assert 1 <= len(adjacent) <= 3
        if len(adjacent) == 1:
            side = (adjacent[0][0]+2) % 4
            caps.update((2*tile[0]+corner//2, 2*tile[1]+corner % 2) for corner in FACES[side])
            leaves += 1
    return caps, leaves


def complete_matching(rows, columns, blanks, selected=(), forced=()):
    selected = set(selected)
    used = [vertex for edge in forced for vertex in edge]
    assert len(used) == len(set(used))
    assert not (set(used) & (blanks | selected))
    available = {(row, column) for row in range(rows) for column in range(columns)}
    available -= blanks | selected | set(used)
    mate = {}

    def extend(vertex, visited):
        for neighbor in neighbors(vertex):
            if neighbor not in available or neighbor in visited:
                continue
            visited.add(neighbor)
            if neighbor not in mate or extend(mate[neighbor], visited):
                mate[neighbor] = vertex
                return True
        return False

    for vertex in sorted(available):
        if sum(vertex) % 2 == 0:
            assert extend(vertex, set()), (rows, columns, vertex)
    matching = list(forced)+[(vertex, neighbor) for neighbor, vertex in mate.items()]
    assert {vertex for edge in matching for vertex in edge} == available | set(used)
    return rows, columns, selected, matching


def check_region(current, region, expected_leaves):
    rows, columns, selected, matching = current
    objective = direct_check(*current)
    tiles = {(row//2, column//2) for row, column in region}
    assert region_vertices(tiles) == region
    caps, leaves = cap_vertices(tiles)
    assert leaves == expected_leaves
    occupied = selected | {vertex for edge in matching for vertex in edge}
    assert not (caps & occupied)
    for tile in tiles:
        adjacent = [side for side, neighbor in enumerate(neighbors(tile)) if neighbor in tiles]
        cap_side = (adjacent[0]+2) % 4 if len(adjacent) == 1 else None
        for side, neighbor_tile in enumerate(neighbors(tile)):
            if neighbor_tile in tiles or side == cap_side:
                continue
            for corner in FACES[side]:
                vertical, horizontal = DIRECTIONS[side]
                outside = 2*tile[0]+corner//2+vertical, 2*tile[1]+corner % 2+horizontal
                assert 0 <= outside[0] < rows and 0 <= outside[1] < columns
                assert outside in occupied
    ledger = general_region_ledger(current, region)
    crossing = sum((first in region) != (second in region) for first, second in matching)
    internal = sum(first in region and second in region for first, second in matching)
    selected_count, blanks = ledger['selected'], ledger['blanks']
    assert len(region) == selected_count+blanks+2*internal+crossing
    assert blanks-selected_count >= 2*leaves+crossing % 2
    assert ledger['incoming_saturated_attachments'] == 0
    assert ledger['charge_twice'] <= -2*leaves+ledger['outgoing_saturated_attachments']-crossing % 2
    graph, _ = graph_record(*current)
    return dict(leaves=leaves, tile_count=len(tiles), objective=objective, crossing=crossing,
                internal_matching_edges=internal, capacity_two_tiles=sum(graph['r'][tile] == 2 for tile in ledger['tiles']),
                **ledger)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    symmetry_count = 0
    for arm_length in range(3, 10):
        straight = {(2, column) for column in range(2, 2+arm_length)}
        bent = straight | {(row, 1+arm_length) for row in range(3, 6)}
        branched = {(4, column) for column in range(2, 2+arm_length)} | {(row, 3) for row in (2, 3)}
        for name, tiles in (('straight', straight), ('bent', bent), ('branched', branched)):
            blanks, leaves = cap_vertices(tiles)
            current = complete_matching(18, 28, blanks)
            region = region_vertices(tiles)
            record = check_region(current, region, leaves)
            assert record['charge_twice'] == -2*leaves
            assert record['blanks'] == 2*leaves and record['selected'] == 0
            for symmetry in itertools.product((False, True), repeat=3):
                shape, chosen, matching = transformed(*current, *symmetry)
                moved = transformed(*current[:2], region, [], *symmetry)[1]
                image = check_region((*shape, chosen, matching), moved, leaves)
                assert image['charge_twice'] == record['charge_twice']
                symmetry_count += 1
            records.append(dict(family=name, arm_length=arm_length, record=record))
    tiles = {(2, column) for column in range(2, 8)} | {(row, 7) for row in range(3, 6)}
    blanks, leaves = cap_vertices(tiles)
    forced = [((4, 14), (4, 15)), ((5, 14), (5, 13)), ((5, 15), (6, 15))]
    forced += [edge for row in (4, 5) for edge in (((row, 6), (row, 5)), ((row, 7), (row, 8)))]
    current = complete_matching(18, 20, blanks, forced=forced)
    record = check_region(current, region_vertices(tiles), leaves)
    graph, _ = graph_record(*current)
    turn_tile, capacity_tile = 2*10+7, 2*10+3
    assert graph['r'][turn_tile] == 1 and graph['deg'][turn_tile] == 2
    assert graph['r'][capacity_tile] == 2 and graph['deg'][capacity_tile] == 4
    assert record['charge_twice'] == -4
    witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                   region_tiles=sorted(tiles), forced_edges=forced, record=record,
                   turn_tile=turn_tile, capacity_two_tile=capacity_tile)
    straight = {(2, column) for column in range(2, 8)}
    caps, leaves = cap_vertices(straight)
    boundary_cases = (
        ('odd_boundary', caps | {(4, 6), (0, 1)}, set(), []),
        ('saturated_inside', caps | {(4, 9), (5, 8), (4, 7), (5, 10), (4, 6), (5, 11)},
         {(4, 8), (5, 9)}, []),
        ('one_saturated_export', caps | {(2, 4), (3, 3), (1, 5), (2, 6), (4, 7), (0, 1)},
         {(2, 5), (3, 4)}, [((3, 5), (4, 5))]))
    boundary_records = []
    for name, blanks, selected, forced in boundary_cases:
        current = complete_matching(18, 20, blanks, selected, forced)
        record = check_region(current, region_vertices(straight), leaves)
        if name == 'odd_boundary':
            assert record['crossing'] % 2 == 1 and record['charge_twice'] == -5
        elif name == 'saturated_inside':
            graph, _ = graph_record(*current)
            assert graph['t'][24] == 2
        else:
            assert record['outgoing_saturated_attachments'] == record['crossing'] % 2 == 1
            assert record['charge_twice'] == -4
        for symmetry in itertools.product((False, True), repeat=3):
            shape, chosen, matching = transformed(*current, *symmetry)
            moved = transformed(*current[:2], region_vertices(straight), [], *symmetry)[1]
            image = check_region((*shape, chosen, matching), moved, leaves)
            assert image['charge_twice'] == record['charge_twice']
            assert image['outgoing_saturated_attachments'] == record['outgoing_saturated_attachments']
            symmetry_count += 1
        boundary_records.append(dict(name=name, blanks=sorted(blanks), selected=sorted(selected),
                                     forced_edges=forced, shape=current[:2], record=record))
    report = dict(status='ALL_CHECKS_PASSED', local=local_controls(),
                  physical_receivers=len(records)+1+len(boundary_records), symmetry_images=symmetry_count,
                  families=records, forced_bend_capacity_two_witness=witness,
                  boundary_records=boundary_records,
                  scope='Finite local and physical matching controls; the arbitrary-size collar and compensation theorem has a separate written proof. These fixtures are receivers, not source-attached target counterexamples.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key not in {'families', 'forced_bend_capacity_two_witness', 'boundary_records'}}))


if __name__ == '__main__':
    main()
