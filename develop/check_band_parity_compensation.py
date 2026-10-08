#!/usr/bin/env python3
"""Independent physical and finite-certificate controls for band compensation."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from discover_band_potential import allowed, column, cost, discover, endpoint, index
from check_compensation_transport import nested_corridor
from check_residual_corridors import direct_check, graph_record, transformed
from check_terminal_strands import decompose


def potential_controls():
    certificate = discover()
    potential = certificate['potential']
    starts = steps = finishes = 0
    for current in range(9):
        if endpoint(current):
            assert potential[index(1, 0, current)] <= cost(current)
            starts += 1
    for parity, left, current in itertools.product(range(2), range(9), range(9)):
        value = potential[index(parity, left, current)]
        if value is None:
            continue
        for following in range(9):
            if allowed(left, current, following):
                target = potential[index(1-parity, current, following)]
                assert target is not None and target <= value+cost(following)
                steps += 1
        if endpoint(current) and allowed(left, current, 0):
            assert value >= 2-parity
            finishes += 1
    lean = Path(__file__).resolve().parents[1]/'formal/SubQuorum/BandCompensation.lean'
    table = lean.read_text().split('private def potentialTable : List Int := [', 1)[1].split(']', 1)[0]
    assert [int(entry.strip()) for entry in table.split(',')] == [
        -10000 if value is None else value for value in potential]
    return dict(reachable_states=certificate['reachable'], starts=starts, transitions=steps,
                finishes=finishes, independent_table_matches_Lean=True)


def band_record(current, band):
    rows, columns, selected, matching = current
    occupied = selected | {vertex for edge in matching for vertex in edge}
    first_column = min(vertex[1] for vertex in band)
    last_column = max(vertex[1] for vertex in band)
    first_row = min(vertex[0] for vertex in band)
    assert band == {(row, col) for row in (first_row, first_row+1)
                    for col in range(first_column, last_column+1)}
    word = []
    for col in range(first_column, last_column+1):
        labels = [1 if (row, col) in selected else 2 if (row, col) in occupied else 0
                  for row in (first_row, first_row+1)]
        word.append(3*labels[0]+labels[1])
    assert endpoint(word[0]) and endpoint(word[-1])
    padded = [0]+word+[0]
    assert all(allowed(padded[position], padded[position+1], padded[position+2])
               for position in range(len(word)))
    blanks = len(band-occupied)
    selected_count = len(band & selected)
    internal = sum(first in band and second in band for first, second in matching)
    crossing = sum((first in band) != (second in band) for first, second in matching)
    assert 2*len(word) == blanks+selected_count+2*internal+crossing
    target = 2+crossing % 2 if len(word) % 2 == 0 else 1+(crossing+1) % 2
    assert blanks-selected_count >= target
    assert sum(map(cost, word)) == blanks-selected_count
    return dict(width=len(word), selected=selected_count, blanks=blanks, internal=internal,
                crossing=crossing, surplus=blanks-selected_count, sharp_bound=target)


def sharp_word(width, crossing_parity):
    columns = width+2 if width % 2 == 0 else width+1
    selected = {(1, col) for col in range(1, width-1, 2)}
    matching = [((0, col), (0, col+1)) for col in range(0, width-1, 2)]
    if width % 2:
        if crossing_parity:
            matching.append(((0, width-1), (0, width)))
    elif crossing_parity:
        matching.pop()
        matching.append(((0, width-1), (0, width)))
    return 2, columns, selected, matching


def source_patch(width, flips):
    assert 0 <= flips <= width
    original = nested_corridor(width, 2)
    removed = frozenset(((3, 3), (4, 3)))
    matching = [edge for edge in original[3] if frozenset(edge) != removed]
    assert len(matching) == len(original[3])-1
    for tile_column in range(1, flips+1):
        horizontal = {frozenset(((row, 2*tile_column), (row, 2*tile_column+1))) for row in (1, 2)}
        matching = [edge for edge in matching if frozenset(edge) not in horizontal]
        matching.extend((((1, 2*tile_column), (2, 2*tile_column)),
                         ((1, 2*tile_column+1), (2, 2*tile_column+1))))
    current = *original[:3], matching
    band = {(row, col) for row in (2, 3) for col in range(2, 2*width+2)}
    graph, components = graph_record(*current)
    source_tiles = set(range(width+2))
    band_tiles = {width+2+col for col in range(1, width+1)}
    source_charge_twice = sum(graph['deg'][tile]-2*graph['r'][tile] for tile in source_tiles)
    band_charge_twice = sum(graph['deg'][tile]-2*graph['r'][tile] for tile in band_tiles)
    saturated_exports = 0
    for first, second in matching:
        if (first in band) == (second in band):
            continue
        outside = second if first in band else first
        tile = outside[0]//2*(width+2)+outside[1]//2
        saturated_exports += graph['t'][tile] == 2
    objective = direct_check(*current)
    assert objective == current[0]*current[1]//2-1
    record = band_record(current, band)
    assert record['crossing'] == 1+2*flips and saturated_exports == 1
    assert sum(graph['r'][tile] == 2 and graph['deg'][tile] == 4 for tile in source_tiles) == flips
    assert record['surplus'] == record['sharp_bound'] == 3
    assert source_charge_twice == 2 and band_charge_twice == -2
    assert sum(component['excess'] for component in components) == -1
    remaining = {tile for tile in range(graph['N']) if graph['t'][tile] < 2}-source_tiles-band_tiles
    assert sum(graph['deg'][tile]-2*graph['r'][tile] for tile in remaining) == -2
    terminal = decompose(current, band_tiles)
    return current, record | dict(capacity_two_source_passages=flips,
        residual_band_ports=2*flips, saturated_exports=saturated_exports,
        source_charge_twice=source_charge_twice, band_charge_twice=band_charge_twice,
        patch_charge_twice=0, remaining_charge_twice=-2,
        strand_counts=terminal['counts'], reserves=terminal['reserve'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.max_width >= 4
    certificate = potential_controls()
    sharp = []
    for width in range(1, args.max_width+1):
        for parity in range(2):
            if width == 1 and parity == 0:
                current = 2, 2, set(), []
            else:
                current = sharp_word(width, parity)
            direct_check(*current)
            band = {(row, col) for row in (0, 1) for col in range(width)}
            record = band_record(current, band)
            assert record['surplus'] == record['sharp_bound']
            assert record['crossing'] % 2 == parity
            sharp.append(record)
    patches = []
    symmetries = 0
    witnesses = []
    for width in range(3, args.max_width+1):
        for flips in (0, 1, width):
            current, record = source_patch(width, flips)
            for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, transpose, flip_rows, flip_columns)
                assert direct_check(*shape, selected, matching) == current[0]*current[1]//2-1
                symmetries += 1
            patches.append(record)
            if width in (3, 4, 10):
                witnesses.append(dict(shape=current[:2], selected=sorted(current[2]), matching=current[3], record=record))
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'formal/SubQuorum/BandCompensation.lean',
               root/'formal/SubQuorum/EndpointCompensation.lean',
               root/'docs/PARITY_ENHANCED_BAND_COMPENSATION.md']
    sources.extend(Path(__file__).with_name(name) for name in ('discover_band_potential.py',
        'check_compensation_transport.py', 'check_residual_corridors.py', 'check_terminal_strands.py',
        'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', potential=certificate, sharp_band_controls=len(sharp),
                  widths=[1,args.max_width], source_patches=len(patches), symmetry_controls=symmetries,
                  patches=patches, witnesses=witnesses,
                  sha256={str(path.relative_to(root)):hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                  scope='Independent controls of written and Lean all-length proofs. Grid-to-band and charge interfaces remain explicit; no arbitrary-grid Lean theorem or universal coefficient improvement.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status','potential','sharp_band_controls','source_patches','symmetry_controls')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: checks use assertions.')
    main()
