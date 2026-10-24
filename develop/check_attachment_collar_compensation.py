"""Finite controls of the attachment-corrected all-region compensation proof."""

import argparse
import itertools
import json
from pathlib import Path

from check_mixed_band_boundary_obstacle import general_region_ledger
from check_pressured_collar_compensation import DIRECTIONS, FACES, local_valid, region_vertices
from check_residual_corridors import direct_check, graph_record, transformed


def local_controls():
    deficient = saturated = 0
    for labels in itertools.product(range(3), repeat=4):
        if not local_valid(labels, ()):
            continue
        selected = labels.count(1)
        if selected < 2:
            assert labels.count(0) >= selected
            deficient += 1
        else:
            assert selected == 2 and labels.count(2) <= 1
            assert labels.count(0)+labels.count(2) == 2
            saturated += 1
    return dict(valid_unpressured_deficient_states=deficient, valid_saturated_states=saturated)


def regional_record(current, tiles, marked):
    rows, columns, selected, matching = current
    objective = direct_check(*current)
    region = region_vertices(tiles)
    occupied = selected | {vertex for edge in matching for vertex in edge}
    assert len(marked) == len({tile for tile, _ in marked})
    for tile, cap_side in marked:
        assert tile in tiles
        for corner in FACES[cap_side]:
            assert (2*tile[0]+corner//2, 2*tile[1]+corner % 2) not in occupied
        for side in ((cap_side+1) % 4, (cap_side+3) % 4):
            for corner in FACES[side]:
                vertical, horizontal = DIRECTIONS[side]
                outside = 2*tile[0]+corner//2+vertical, 2*tile[1]+corner % 2+horizontal
                assert 0 <= outside[0] < rows and 0 <= outside[1] < columns
                assert outside in occupied
    graph, _ = graph_record(*current)
    tile_of = lambda vertex: vertex[0]//2*(columns//2)+vertex[1]//2
    saturated = {tile for tile in range(graph['N']) if graph['t'][tile] == 2}
    ledger = general_region_ledger(current, region)
    internal_attachments = sum(first in region and second in region and
                               ((tile_of(first) in saturated) != (tile_of(second) in saturated))
                               for first, second in matching)
    saturated_endpoints = sum(vertex in region and tile_of(vertex) in saturated
                              for edge in matching for vertex in edge)
    deficient_surplus = sum(len(region_vertices({tile})-occupied)-len(region_vertices({tile}) & selected)
                            for tile in tiles if tile_of((2*tile[0], 2*tile[1])) not in saturated)
    crossing = sum((first in region) != (second in region) for first, second in matching)
    outgoing = ledger['outgoing_saturated_attachments']
    incoming = ledger['incoming_saturated_attachments']
    assert saturated_endpoints == internal_attachments+incoming
    assert deficient_surplus >= 2*len(marked)
    assert deficient_surplus == ledger['blanks']-ledger['selected']+saturated_endpoints
    assert deficient_surplus % 2 == (crossing+saturated_endpoints) % 2
    assert ledger['charge_twice'] == -deficient_surplus+internal_attachments+outgoing
    assert ledger['charge_twice'] <= -2*len(marked)+internal_attachments+outgoing-(crossing+saturated_endpoints) % 2
    return dict(tile_count=len(tiles), marked_tiles=len(marked), crossing=crossing,
                saturated_endpoints=saturated_endpoints, internal_attachments=internal_attachments,
                deficient_surplus=deficient_surplus, objective=objective, **ledger)


def image_marked(current, marked, symmetry):
    result = []
    for tile, side in marked:
        original_tile = region_vertices({tile})
        image_tile = transformed(*current[:2], original_tile, [], *symmetry)[1]
        new_tile = min(row//2 for row, _ in image_tile), min(column//2 for _, column in image_tile)
        cap = {(2*tile[0]+corner//2, 2*tile[1]+corner % 2) for corner in FACES[side]}
        image_cap = transformed(*current[:2], cap, [], *symmetry)[1]
        new_side = next(candidate for candidate in range(4)
                        if {(2*new_tile[0]+corner//2, 2*new_tile[1]+corner % 2)
                            for corner in FACES[candidate]} == image_cap)
        result.append((new_tile, new_side))
    return result


def check_images(current, tiles, marked):
    record = regional_record(current, tiles, marked)
    for symmetry in itertools.product((False, True), repeat=3):
        shape, chosen, matching = transformed(*current, *symmetry)
        moved = transformed(*current[:2], region_vertices(tiles), [], *symmetry)[1]
        image_tiles = {(row//2, column//2) for row, column in moved}
        image = regional_record((*shape, chosen, matching), image_tiles,
                                image_marked(current, marked, symmetry))
        for key in ('charge_twice', 'deficient_surplus', 'saturated_endpoints',
                    'internal_attachments', 'crossing', 'outgoing_saturated_attachments',
                    'incoming_saturated_attachments'):
            assert image[key] == record[key], key
    return record


def incoming_witness(marked_terminal):
    selected = {(4, 10), (5, 11)}
    matching = [((4, 11), (4, 12))]
    tiles = {(2, 5)}
    marked = []
    if marked_terminal:
        tiles.add((2, 2))
        marked.append(((2, 2), 3))
        matching += [((4, 5), (5, 5)), ((3, 4), (3, 5)), ((6, 4), (6, 5))]
    return (10, 16, selected, matching), tiles, marked


def internal_debt_path(length):
    assert length >= 0
    selected = {(2, 2), (3, 3), (3, 5)}
    matching = [((2, 3), (2, 4)), ((2, 5), (1, 5))]
    tiles = {(1, 1), (1, 2)}
    if length:
        tiles |= {(0, column) for column in range(2, length+2)}
        matching += [((0, 4), (1, 4))]
        matching += [((1, 2*column), (1, 2*column+1)) for column in range(3, length+2)]
        matching += [((0, 2*column+1), (0, 2*column+2)) for column in range(2, length+2)]
    return (6, 2*length+8, selected, matching), tiles, []


def thick_receiver(incoming=False):
    tiles = {(row, column) for row in range(3, 6) for column in range(3, 6)}
    tiles |= {(4, column) for column in (1, 2, 6, 7)}
    marked = [((4, 1), 3), ((4, 7), 1)]
    blanks = {(2*tile[0]+corner//2, 2*tile[1]+corner % 2)
              for tile, side in marked for corner in FACES[side]}
    selected = set()
    matching = []
    for tile in tiles:
        for column in (2*tile[1], 2*tile[1]+1):
            edge = ((2*tile[0], column), (2*tile[0]+1, column))
            if not (set(edge) & blanks):
                matching.append(edge)
    for tile, _ in marked:
        for row in (2*tile[0]-1, 2*tile[0]+2):
            matching.append(((row, 2*tile[1]), (row, 2*tile[1]+1)))
    if incoming:
        saturated_tile = (3, 4)
        selected = {(6, 8), (7, 9)}
        saturated_vertices = region_vertices({saturated_tile})
        forbidden = {neighbor for vertex in selected
                     for vertical, horizontal in DIRECTIONS
                     if (neighbor := (vertex[0]+vertical, vertex[1]+horizontal)) != (6, 9)}
        matching = [edge for edge in matching if not set(edge) & (saturated_vertices | forbidden)]
        matching.append(((6, 9), (5, 9)))
    return (16, 20, selected, matching), tiles, marked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-length', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert arguments.max_length >= 1
    fixtures = []
    for marked_terminal in (False, True):
        current, tiles, marked = incoming_witness(marked_terminal)
        record = check_images(current, tiles, marked)
        assert record['charge_twice'] == -2*len(marked)
        assert record['crossing'] == record['saturated_endpoints'] == 1
        assert record['internal_attachments'] == 0
        assert record['charge_twice'] > -2*len(marked)-record['crossing'] % 2
        fixtures.append(dict(name='incoming_with_terminal' if marked_terminal else 'incoming_only',
                             shape=current[:2], selected=sorted(current[2]), matching=current[3],
                             region_tiles=sorted(tiles), marked=marked, record=record))
    for length in range(arguments.max_length+1):
        current, tiles, marked = internal_debt_path(length)
        record = check_images(current, tiles, marked)
        assert record['charge_twice'] == record['internal_attachments'] == 1
        assert record['deficient_surplus'] == record['outgoing_saturated_attachments'] == 0
        assert record['crossing'] == record['saturated_endpoints'] == 1
        assert direct_check(*current) == 2*length+5
        graph, _ = graph_record(*current)
        for column in range(2, length+2):
            assert graph['h'][column] == graph['r'][column] == 1
            assert graph['deg'][column] == 2
        fixtures.append(dict(name='internal_debt_path', length=length, record=record))
    for incoming in (False, True):
        current, tiles, marked = thick_receiver(incoming)
        record = check_images(current, tiles, marked)
        assert record['internal_attachments'] == record['outgoing_saturated_attachments'] == 0
        assert record['charge_twice'] <= -4
        assert max(sum((tile[0]+vertical, tile[1]+horizontal) in tiles
                       for vertical, horizontal in DIRECTIONS) for tile in tiles) == 4
        if incoming:
            assert record['saturated_endpoints'] == record['incoming_saturated_attachments'] == 1
        else:
            assert record['charge_twice'] == -4
        fixtures.append(dict(name='thick_incoming' if incoming else 'thick_sharp',
                             shape=current[:2], selected=sorted(current[2]), matching=current[3],
                             region_tiles=sorted(tiles), marked=marked, record=record))
    report = dict(status='ALL_CHECKS_PASSED', local=local_controls(),
                  physical_regions=len(fixtures), symmetry_images=8*len(fixtures),
                  max_debt_path_length=arguments.max_length, fixtures=fixtures,
                  scope='Finite controls; arbitrary-size proof and all-length connected debt construction are written separately. The two refuted rules do not refute the grid inequality.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key!='fixtures'}))


if __name__ == '__main__':
    main()
