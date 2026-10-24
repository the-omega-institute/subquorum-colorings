#!/usr/bin/env python3
"""Check nested compensation transport and unbounded donor distance.

The arbitrary-depth results have written proofs in COMPENSATION_TRANSPORT.md.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_residual_corridors import direct_check, graph_record, transformed
from check_cross_component_compensation import encode
from verify_grid_five_sixths import canonical
from verify_grid_short_path_compensation import check_geometry


def nested_corridor(width, depth):
    if depth < 1 or width < max(2, 2*depth-1):
        raise ValueError('Require depth >= 1 and width >= max(2, 2*depth-1).')
    rows, columns = 2*(depth+1), 2*(width+2)
    selected = {(0, 0), (0, columns-1)}
    matching = [((0, 2*column+1), (0, 2*column+2))
                for column in range(width+1)]
    matching += [((1, 2*column), (1, 2*column+1))
                 for column in range(1, width+1)]
    matching += [((1, 1), (2, 1)), ((1, columns-2), (2, columns-2))]
    for layer in range(1, depth+1):
        left, right = layer, width+1-layer
        for column in range(width+2):
            top, start = 2*layer, 2*column
            if column < left:
                selected.update(((top, start), (top+1, start+1)))
            elif column > right:
                selected.update(((top, start+1), (top+1, start)))
        matching += [((2*layer, 2*column), (2*layer, 2*column+1))
                     for column in range(left, right+1)]
        if layer == depth:
            matching += [((2*layer+1, 2*column+1), (2*layer+1, 2*column+2))
                         for column in range(left, right)]
        else:
            matching += [((2*layer+1, 2*column), (2*layer+1, 2*column+1))
                         for column in range(left+1, right)]
            matching += [((2*layer+1, 2*left+1), (2*layer+2, 2*left+1)),
                         ((2*layer+1, 2*right), (2*layer+2, 2*right))]
    return rows, columns, selected, matching


def flip_internal_squares(configuration, limit):
    rows, columns, selected, matching = configuration
    matching = {tuple(sorted(edge)) for edge in matching}
    swaps = 0
    for top in range(1, rows-1, 2):
        for left in range(0, columns-1, 2):
            upper = ((top, left), (top, left+1))
            lower = ((top+1, left), (top+1, left+1))
            if upper in matching and lower in matching and swaps < limit:
                matching.difference_update((upper, lower))
                matching.update((((top, left), (top+1, left)),
                                 ((top, left+1), (top+1, left+1))))
                swaps += 1
    return (rows, columns, selected, sorted(matching)), swaps


def verify(configuration, width, depth, strict_components):
    rows, columns, selected, matching = configuration
    objective = direct_check(*configuration)
    assert objective == rows*columns//2
    assert len(selected) == 2+2*depth*(depth+1)
    assert len(matching) == 2*(depth+1)*(width+2-depth)-2
    residual, components = graph_record(*configuration)
    assert not check_geometry(residual)
    mask, edges = encode(*configuration)
    routing = canonical(rows, columns, mask, edges)
    assert routing['q'] == 0 and routing['f2'] == 0
    assert routing['a'] == routing['b'] and 2*routing['a']+routing['c'] == 2
    if strict_components:
        assert routing['a'] == routing['b'] == 1 and routing['c'] == 0
    charges = [residual['deg'][tile]-2*residual['r'][tile]
               if residual['t'][tile] < 2 else 0 for tile in range(residual['N'])]
    negative = [tile for tile, charge in enumerate(charges) if charge < 0]
    positive = [tile for tile, charge in enumerate(charges) if charge > 0]
    assert len(positive) == 2 and sum(charges[tile] for tile in positive) == 2
    assert sum(charges[tile] for tile in negative) == -2
    assert all(tile//(width+2) == depth for tile in negative)
    assert all(tile//(width+2) == 0 for tile in positive)
    assert all(charge == 0 for tile, charge in enumerate(charges)
               if tile not in positive+negative)
    source_tiles = range(width+2)
    donor_distance = min(abs(donor//(width+2)-source//(width+2))
                         + abs(donor % (width+2)-source % (width+2))
                         for donor in negative for source in source_tiles)
    assert donor_distance == depth
    layers = []
    for layer in range(1, depth+1):
        band_tiles = [layer*(width+2)+column
                      for column in range(layer, width+2-layer)]
        band = {vertex for tile in band_tiles for vertex in residual['vertices'][tile]}
        blank_count = sum(not (residual['A'] >> vertex & 1) for vertex in band)
        selected_count = sum(mask >> vertex & 1 for vertex in band)
        assert blank_count-selected_count == 2
        attachments = sum(residual['s'][tile] for tile in band_tiles)
        charge_twice = sum(charges[tile] for tile in band_tiles)
        assert attachments == (0 if layer == depth else 2)
        assert charge_twice == (-2 if layer == depth else 0)
        layers.append(dict(layer=layer, tile_width=len(band_tiles),
                           outgoing_saturated_attachments=attachments,
                           blank_minus_selected=blank_count-selected_count,
                           charge_twice=charge_twice))
    if strict_components:
        expected_neutral = (depth-1)*(width+2-depth)
        assert sorted(component['excess'] for component in components) == [-1]+[0]*expected_neutral+[1]
        source = next(component for component in components if component['excess'] == 1)
        donor = next(component for component in components if component['excess'] == -1)
        assert source['edges'] == width+1 and source['capacity'] == width
        terminal_width = width+2-2*depth
        assert donor['edges'] == terminal_width-1 and donor['capacity'] == terminal_width
        assert all(component['edges'] == component['capacity'] == 0
                   for component in components if component['excess'] == 0)
    return dict(width=width, depth=depth, rows=rows, columns=columns,
                selected_count=len(selected), matching_count=len(matching), q=0,
                donor_tile_distance=donor_distance, layers=layers,
                component_excesses=[component['excess'] for component in components],
                routing={key: routing[key] for key in ('a', 'b', 'c', 'f2', 'f3')})


def symmetry_checks(configuration, expected_excesses):
    rows, columns, selected, matching = configuration
    checked = 0
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        (height, breadth), singles, edges = transformed(
            rows, columns, selected, matching, transpose, flip_rows, flip_columns)
        assert direct_check(height, breadth, singles, edges) == height*breadth//2
        residual, components = graph_record(height, breadth, singles, edges)
        assert sorted(component['excess'] for component in components) == sorted(expected_excesses)
        assert not check_geometry(residual)
        mask, encoded = encode(height, breadth, singles, edges)
        route = canonical(height, breadth, mask, encoded)
        assert route['q'] == 0 and route['a'] == route['b']
        assert 2*route['a']+route['c'] == 2
        checked += 1
    return checked


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-depth', type=int, default=16)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_depth < 3:
        parser.error('--max-depth must be at least 3')
    families = []
    flipped = []
    witnesses = []
    images = 0
    for depth in range(1, args.max_depth+1):
        for extra_width in (0, 1, 2, 5):
            width = max(2, 2*depth-1)+extra_width
            configuration = nested_corridor(width, depth)
            record = verify(configuration, width, depth, True)
            images += symmetry_checks(configuration, record['component_excesses'])
            families.append(record)
            for limit in (1, width*(depth+1)):
                changed, swaps = flip_internal_squares(configuration, limit)
                assert swaps > 0
                changed_record = verify(changed, width, depth, False)
                assert {vertex for edge in configuration[3] for vertex in edge} == {
                    vertex for edge in changed[3] for vertex in edge}
                images += symmetry_checks(changed, changed_record['component_excesses'])
                flipped.append(dict(width=width, depth=depth, swaps=swaps,
                                    donor_tile_distance=changed_record['donor_tile_distance'],
                                    component_excesses=changed_record['component_excesses']))
            if depth in (2, 3) and extra_width == 1:
                rows, columns, selected, matching = configuration
                residual, components = graph_record(*configuration)
                witnesses.append(dict(rows=rows, columns=columns,
                                      selected=sorted(selected), matching=matching,
                                      record=record, components=components,
                                      capacities=residual['r'], degrees=residual['deg']))
    source_names = ('check_compensation_transport.py', 'check_cross_component_compensation.py',
                    'check_residual_corridors.py', 'verify_grid_five_sixths.py',
                    'verify_grid_short_path_compensation.py')
    report = dict(status='ALL_CHECKS_PASSED', max_depth=args.max_depth,
                  base_families=len(families), matching_variants=len(flipped),
                  symmetry_images=images, families=families, flipped=flipped, witnesses=witnesses,
                  sha256={name: hashlib.sha256(Path(__file__).with_name(name).read_bytes()).hexdigest()
                          for name in source_names},
                  scope='Finite controls of explicit arbitrary-depth proofs. Distances refer to the fixed tiling and initial residual charges; local transformations are not excluded. No general coefficient-one or new Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('families', 'flipped', 'witnesses')}, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
