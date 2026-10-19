"""Physical controls for straight shared-blank chains and multiple double links."""

import argparse
import itertools
import json
from pathlib import Path

from check_blank_witness_compensation import staircase, witness_record
from check_attachment_collar_compensation import incoming_witness, internal_debt_path, thick_receiver
from check_pressured_collar_compensation import region_vertices
from check_residual_corridors import transformed


def chain_record(current, tiles, marked):
    record = witness_record(current, tiles, marked)
    selected = current[2]
    tile_edges = {(tile, neighbor) for tile in tiles for neighbor in
                  ((tile[0]+1, tile[1]), (tile[0], tile[1]+1)) if neighbor in tiles}
    unvisited = set(tiles)
    tile_components = 0
    while unvisited:
        tile_components += 1
        pending = [unvisited.pop()]
        while pending:
            row, column = pending.pop()
            for neighbor in ((row-1, column), (row+1, column), (row, column-1), (row, column+1)):
                if neighbor in unvisited:
                    unvisited.remove(neighbor)
                    pending.append(neighbor)
    tile_cycle_rank = len(tile_edges)-len(tiles)+tile_components
    pair_blanks = {}
    for incidence in record['incidence']:
        if len(incidence['owners']) == 2:
            first, second = map(tuple, incidence['owners'])
            assert abs(first[0]-second[0]) == abs(first[1]-second[1]) == 1
            pair_blanks.setdefault((first, second), []).append(incidence['blank'])
    assert all(len(blanks) <= 2 for blanks in pair_blanks.values())
    double_links = sum(len(blanks) == 2 for blanks in pair_blanks.values())
    assert double_links == record['cycle_rank']
    assert double_links <= tile_cycle_rank
    double_squares = set()
    for (first, second), blanks in pair_blanks.items():
        if len(blanks) == 2:
            square = frozenset((first, second, (first[0], second[1]), (second[0], first[1])))
            assert square <= tiles
            assert square not in double_squares
            double_squares.add(square)
    edge_indices = {edge:index for index, edge in enumerate(sorted(tile_edges))}
    cycle_basis = {}
    for square in double_squares:
        cycle_edges = {edge for edge in tile_edges if set(edge) <= square}
        assert len(cycle_edges) == 4
        vector = sum(1 << edge_indices[edge] for edge in cycle_edges)
        while vector:
            pivot = vector.bit_length()-1
            if pivot not in cycle_basis:
                cycle_basis[pivot] = vector
                break
            vector ^= cycle_basis[pivot]
        assert vector
    assert len(cycle_basis) == double_links
    component_records = []
    for component in record['components']:
        owners = sorted(map(tuple, component['owners']))
        orientations = []
        for owner in owners:
            corners = selected & region_vertices({owner})
            local = {(row % 2, column % 2) for row, column in corners}
            assert local in ({(0, 0), (1, 1)}, {(0, 1), (1, 0)})
            orientations.append(1 if (0, 0) in local else -1)
        assert len(set(orientations)) == 1
        slope = orientations[0]
        assert len({column-slope*row for row, column in owners}) == 1
        assert [row for row, _ in owners] == list(range(owners[0][0], owners[-1][0]+1))
        links = [pair for pair in pair_blanks if pair[0] in owners]
        assert len(links) == len(owners)-1
        assert set(links) == set(zip(owners, owners[1:]))
        doubles = sum(len(pair_blanks[pair]) == 2 for pair in links)
        assert doubles == component['cycle_rank']
        assert component['deficit'] == int(not doubles and not component['private'])
        component_records.append(dict(owners=len(owners), slope=slope,
                                      line=owners[0][1]-slope*owners[0][0],
                                      double_links=doubles, private=component['private']))
    assert record['regional']['charge_twice'] == (
        -2*len(marked)+record['regional']['outgoing_saturated_attachments']
        +record['component_count']-double_links-record['private_blanks']-record['unused_blanks'])
    return dict(owners=record['owners'], components=component_records, tile_cycle_rank=tile_cycle_rank,
                double_links=double_links, private_blanks=record['private_blanks'],
                unused_blanks=record['unused_blanks'], unmatched_debts=record['unmatched_debts'],
                charge_twice=record['regional']['charge_twice'],
                objective=record['regional']['objective'])


def multiple_repairs(size, indices):
    current, tiles, marked = staircase(size, 'none')
    rows, columns, selected, original = current
    matching = list(original)
    tiles = set(tiles)
    for index in indices:
        tiles.add((1+index, size-index-1))
        matching.append(((2*index+2, 2*size-2*index-2), (2*index+3, 2*size-2*index-2)))
        matching.append(((2*index+2, 2*size-2*index-1), (2*index+1, 2*size-2*index-1)))
    return (rows, columns, selected, matching), tiles, marked


def displacement_controls():
    cases = []
    for blank_row, blank_column in itertools.product(range(4, 6), repeat=2):
        blank_tile = blank_row//2, blank_column//2
        external = [(row, column) for row, column in (
            (blank_row-1, blank_column), (blank_row+1, blank_column),
            (blank_row, blank_column-1), (blank_row, blank_column+1))
                    if (row//2, column//2) != blank_tile]
        assert len(external) == 2
        for first, second in (external, external[::-1]):
            first_tile = first[0]//2, first[1]//2
            second_tile = second[0]//2, second[1]//2
            assert second_tile == (
                first_tile[0]+(-1 if first[0] % 2 == 0 else 1),
                first_tile[1]+(-1 if first[1] % 2 == 0 else 1))
            assert second[0] % 2 == 1-first[0] % 2
            assert second[1] % 2 == 1-first[1] % 2
            cases.append(dict(blank=(blank_row, blank_column), selected=(first, second)))
    return cases


def marked_selected_tile():
    current = 10, 12, {(4, 4)}, [((4, 3), (5, 3)), ((4, 6), (5, 6))]
    return current, {(2, 2)}, [((2, 2), 2)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-exhaustive-size', type=int, default=8)
    parser.add_argument('--max-size', type=int, default=32)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    assert 2 <= arguments.max_exhaustive_size <= arguments.max_size
    fixtures = []
    symmetry_images = 0
    for size in range(2, arguments.max_size+1):
        if size <= arguments.max_exhaustive_size:
            subsets = [tuple(index for index in range(size-1) if mask >> index & 1)
                       for mask in range(1 << (size-1))]
        else:
            subsets = sorted({(), tuple(range(size-1)), tuple(range(0, size-1, 2)),
                              tuple(range(1, size-1, 2)), (0,), (size-2,)})
        for indices in subsets:
            current, tiles, marked = multiple_repairs(size, indices)
            record = chain_record(current, tiles, marked)
            assert record['owners'] == size
            assert record['double_links'] == len(indices)
            assert record['tile_cycle_rank'] == len(indices)
            assert record['charge_twice'] == 1-len(indices)
            assert record['objective'] == 4*size-1+2*len(indices)
            assert record['unmatched_debts'] == int(not indices)
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                moved = transformed(*current[:2], region_vertices(tiles), [], *symmetry)[1]
                image = chain_record((*shape, selected, matching),
                                     {(row//2, column//2) for row, column in moved}, [])
                for key in ('owners', 'double_links', 'charge_twice', 'unmatched_debts', 'objective'):
                    assert image[key] == record[key]
                symmetry_images += 1
            fixtures.append(dict(size=size, double_link_indices=indices, record=record))
    inherited = []
    for size in range(2, 25):
        for repair in ('none', 'private', 'cycle'):
            inherited.append(chain_record(*staircase(size, repair)))
    for length in range(41):
        inherited.append(chain_record(*internal_debt_path(length)))
    for builder in (incoming_witness, thick_receiver):
        for option in (False, True):
            inherited.append(chain_record(*builder(option)))
    marked_record = chain_record(*marked_selected_tile())
    assert marked_record['charge_twice'] == -2
    assert marked_record['unused_blanks'] == 0
    inherited.append(marked_record)
    report = dict(status='ALL_CHECKS_PASSED', local_displacement_cases=displacement_controls(),
                  physical_regions=len(fixtures), symmetry_images=symmetry_images,
                  inherited_regions=len(inherited), maximum_size=arguments.max_size,
                  exhaustive_subset_size=arguments.max_exhaustive_size, fixtures=fixtures,
                  scope='Finite coordinate, matching, component-classification and multi-resource controls; arbitrary-size classification and all-subset construction have written proofs.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in {'fixtures', 'local_displacement_cases'}}))


if __name__ == '__main__':
    main()
