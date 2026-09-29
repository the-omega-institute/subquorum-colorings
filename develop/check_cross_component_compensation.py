#!/usr/bin/env python3
"""Coordinate controls for the boundary-aware adjacent-band lemma.

Universal statements are proved in docs/CROSS_COMPONENT_COMPENSATION.md.
The existing coordinate, residual and prescribed-routing checkers are reused.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_residual_corridors import corridor, direct_check, graph_record, transformed
from verify_grid_five_sixths import canonical
from verify_grid_short_path_compensation import graph, pairs


def sharp_band(length):
    rows, columns, selected, matching = corridor(length)
    matching += [((2, 2*index), (2, 2*index+1))
                 for index in range(1, length+1)]
    matching += [((3, 2*index+1), (3, 2*index+2))
                 for index in range(1, length)]
    return rows, columns, selected, matching


def escaping_band(length):
    assert length >= 3
    _, columns, selected, matching = corridor(length)
    selected |= {(4, 2), (5, 3), (4, 2*length+1), (5, 2*length)}
    matching += [((2, 2*index), (2, 2*index+1))
                 for index in range(1, length+1)]
    matching += [((3, 2*index), (3, 2*index+1))
                 for index in range(2, length)]
    matching += [((3, 3), (4, 3)), ((3, 2*length), (4, 2*length))]
    return 6, columns, selected, matching


def flipped_band(length):
    rows, columns, selected, matching = sharp_band(length)
    removed = {frozenset(((row, 2*index), (row, 2*index+1)))
               for row in (1, 2) for index in range(1, length+1)}
    matching = [edge for edge in matching if frozenset(edge) not in removed]
    matching += [((1, column), (2, column)) for column in range(2, 2*length+2)]
    return rows, columns, selected, matching


def encode(rows, columns, selected, matching):
    mask = sum(1 << (vertex[0]*columns+vertex[1]) for vertex in selected)
    edges = tuple((first[0]*columns+first[1], second[0]*columns+second[1])
                  for first, second in matching)
    return mask, edges


def band_ledger(rows, columns, selected, matching, band):
    residual_graph, components = graph_record(rows, columns, selected, matching)
    endpoints = {vertex for edge in matching for vertex in edge}
    occupied = selected | endpoints
    tile_columns = columns//2
    band_tiles = {(vertex[0]//2)*tile_columns+vertex[1]//2 for vertex in band}
    assert len(band) == 4*len(band_tiles)
    internal = sum(first in band and second in band for first, second in matching)
    crossing = [(first, second) if first in band else (second, first)
                for first, second in matching if (first in band) != (second in band)]
    attachments = sum(residual_graph['t'][(outside[0]//2)*tile_columns+outside[1]//2] == 2
                      for _, outside in crossing)
    blanks = len(band-occupied)
    singles = len(band & selected)
    charge_twice = sum(residual_graph['deg'][tile]-2*residual_graph['r'][tile]
                       for tile in band_tiles if residual_graph['t'][tile] < 2)
    assert 2*(singles+internal)+len(crossing) == len(band)+singles-blanks
    assert charge_twice == singles-blanks+attachments
    return dict(tiles=sorted(band_tiles), selected=singles, blanks=blanks,
                internal_matching_edges=internal, crossing_matching_edges=len(crossing),
                saturated_attachments=attachments, charge_twice=charge_twice,
                capacity_sum=sum(residual_graph['r'][tile] for tile in band_tiles),
                residual_degrees=[residual_graph['deg'][tile] for tile in sorted(band_tiles)],
                components=components)


def witness_record(name, configuration, band=None):
    rows, columns, selected, matching = configuration
    objective = direct_check(rows, columns, selected, matching)
    mask, edges = encode(*configuration)
    route = canonical(rows, columns, mask, edges)
    residual_graph, components = graph_record(*configuration)
    record = dict(name=name, rows=rows, columns=columns, selected=sorted(selected),
                  matching=matching, objective=objective, q=objective-rows*columns//2,
                  components=components,
                  routing={key: route[key] for key in ('a', 'b', 'c', 'f2', 'f3', 'h', 'paths')},
                  tiles=[dict(tile=tile, selected=residual_graph['t'][tile],
                              internal=residual_graph['h'][tile], attachments=residual_graph['s'][tile],
                              capacity=residual_graph['r'][tile], degree=residual_graph['deg'][tile])
                         for tile in range(residual_graph['N'])])
    if band is not None:
        record['band'] = band_ledger(*configuration, band)
    return record


def state_controls(max_width):
    reports = []
    for width in range(2, max_width+1, 2):
        accepted = 0
        minimum = 2*width
        for middle in itertools.product('BTP', repeat=2*width-2):
            letters = (middle[:width], ('B',)+middle[width:]+('B',))
            if letters[0][0] == 'T' or letters[0][-1] == 'T':
                continue
            valid = True
            for row in range(2):
                for column in range(width):
                    if letters[row][column] != 'T':
                        continue
                    neighbors = [letters[1-row][column]]
                    if column:
                        neighbors.append(letters[row][column-1])
                    if column+1 < width:
                        neighbors.append(letters[row][column+1])
                    if sum(letter != 'B' for letter in neighbors) > row:
                        valid = False
                        break
                if not valid:
                    break
            if valid:
                difference = sum(line.count('B')-line.count('T') for line in letters)
                assert difference >= 2
                minimum = min(minimum, difference)
                accepted += 1
        reports.append(dict(width=width, assignments=3**(2*width-2),
                            accepted=accepted, minimum_blank_minus_selected=minimum,
                            scope='All B/T/P labelings satisfying the ladder hypotheses, even without requiring P to be matchable.'))
    return reports


def feasible_band_controls(max_width):
    reports = []
    for width in range(2, max_width+1, 2):
        adjacency, _ = graph(2, width)
        accepted = total = 0
        best = 0
        for selected, matching in pairs(2, width):
            total += 1
            occupied = selected
            for first, second in matching:
                occupied |= (1 << first) | (1 << second)
            if occupied & ((1 << width) | (1 << (2*width-1))):
                continue
            if selected & (1 | (1 << (width-1))):
                continue
            if any(selected >> column & 1 and adjacency[column] & occupied
                   for column in range(width)):
                continue
            objective = selected.bit_count()+len(matching)
            assert objective <= width-1
            accepted += 1
            best = max(best, objective)
        reports.append(dict(width=width, feasible_pairs_examined=total,
                            accepted=accepted, maximum_objective=best))
    return reports


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-k', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_k < 3:
        parser.error('--max-k must be at least 3')
    symmetry_checks = 0
    records = []
    for length in range(2, args.max_k+1):
        band = {(row, column) for row in (2, 3) for column in range(2, 2*length+2)}
        for name, constructor in (('sharp_closed_band', sharp_band),
                                  ('capacity_two_passages', flipped_band),
                                  ('escaping_attachments', escaping_band)):
            if name == 'escaping_attachments' and length < 3:
                continue
            configuration = constructor(length)
            rows, columns, selected, matching = configuration
            ledger = band_ledger(*configuration, band)
            residual_graph, _ = graph_record(*configuration)
            upper_charge_twice = sum(residual_graph['deg'][tile]-2*residual_graph['r'][tile]
                                     for tile in range(length+2))
            assert upper_charge_twice == 2
            assert ledger['blanks']-ledger['selected'] == 2
            assert ledger['charge_twice'] == (0 if name == 'escaping_attachments' else -2)
            expected_excess = ([1]+[0]*length+[-2]*length if name == 'escaping_attachments'
                               else [0] if name == 'capacity_two_passages' else [1, -1])
            assert sorted(component['excess'] for component in ledger['components']) == sorted(expected_excess)
            if name == 'escaping_attachments':
                assert ledger['saturated_attachments'] == 2 and ledger['capacity_sum'] == 0
            if name == 'capacity_two_passages':
                original = sharp_band(length)
                assert len(matching) == len(original[3])
                assert {vertex for edge in matching for vertex in edge} == {
                    vertex for edge in original[3] for vertex in edge}
                inner_tiles = list(range(1, length+1))+list(range(length+3, 2*length+3))
                assert all(residual_graph['r'][tile] == 2 for tile in inner_tiles)
            for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
                (height, width), transformed_selected, transformed_matching = transformed(
                    rows, columns, selected, matching, transpose, flip_rows, flip_columns)
                objective = direct_check(height, width, transformed_selected, transformed_matching)
                assert objective-height*width//2 == (1-2*length if name == 'escaping_attachments' else 0)
                mask, edges = encode(height, width, transformed_selected, transformed_matching)
                route = canonical(height, width, mask, edges)
                assert route['f2'] == 0
                _, components = graph_record(height, width, transformed_selected, transformed_matching)
                assert sorted(component['excess'] for component in components) == sorted(expected_excess)
                symmetry_checks += 1
            if length == 3:
                records.append(witness_record(name, configuration, band))
    bent_selected = {divmod(vertex, 6) for vertex in (3, 5, 8, 24, 33, 35, 36, 43)}
    bent_matching = [(divmod(first, 6), divmod(second, 6)) for first, second in
                     ((9, 10), (11, 17), (16, 22), (23, 29), (25, 26), (27, 28), (31, 37))]
    bent = (8, 6, bent_selected, bent_matching)
    bent_record = witness_record('bent_four_edge_path', bent)
    assert sorted(component['excess'] for component in bent_record['components']) == [-2]*5+[1]
    assert bent_record['routing']['h'] == 1
    assert any(path['typ'] == 'LL' and path['length'] == 4
               for path in bent_record['routing']['paths'])
    replacement_matching = [edge for edge in bent_matching if edge != ((2, 4), (3, 4))]
    for candidate in ((2, 3), (3, 3)):
        assert direct_check(8, 6, bent_selected | {candidate}, replacement_matching) == bent_record['objective']
        _, replacement_components = graph_record(8, 6, bent_selected | {candidate}, replacement_matching)
        assert all(component['excess'] <= 0 for component in replacement_components)
    try:
        direct_check(8, 6, bent_selected | {(2, 3), (3, 3)}, replacement_matching)
    except AssertionError:
        bent_record['both_promotions_rejected'] = True
    else:
        raise AssertionError('Adjacent promotions unexpectedly compatible')
    bent_record['safe_single_promotions_after_deleting_edge_16_22'] = [(2, 3), (3, 3)]
    records.append(bent_record)
    sources = [Path(__file__), Path(__file__).with_name('check_residual_corridors.py'),
               Path(__file__).with_name('verify_grid_short_path_compensation.py'),
               Path(__file__).with_name('verify_grid_five_sixths.py')]
    report = dict(status='ALL_CHECKS_PASSED', k_range=[2, args.max_k],
                  family_symmetry_checks=symmetry_checks,
                  state_controls=state_controls(6), feasible_band_controls=feasible_band_controls(6),
                  witnesses=records,
                  sha256={source.name: hashlib.sha256(source.read_bytes()).hexdigest() for source in sources},
                  scope='Finite coordinate and exhaustive local controls. The all-k families and compensation inequality have separate written proofs. No new Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'witnesses'}, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
