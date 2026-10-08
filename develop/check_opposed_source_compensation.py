#!/usr/bin/env python3
"""Independent grid controls of the all-length opposed-source proof."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_residual_corridors import direct_check, graph_record, transformed
from check_terminal_strands import decompose
from verify_grid_short_path_compensation import feasible, graph as grid_graph


def opposed_frame(width, upper_flips=(), lower_flips=()):
    assert width >= 3
    columns = 2*width
    selected = {(3, 0), (3, columns-1), (6, 0), (6, columns-1),
                (0, 1), (1, 0), (0, columns-2), (1, columns-1),
                (8, 0), (9, 1), (8, columns-1), (9, columns-2)}
    matching = [((row, 2*position+1), (row, 2*position+2))
                for row in (3, 4, 5, 6) for position in range(width-1)]
    matching += [((row, 2*position), (row, 2*position+1))
                 for row in (2, 7) for position in range(1, width-1)]
    matching += [((2, 1), (1, 1)), ((2, columns-2), (1, columns-2)),
                 ((7, 1), (8, 1)), ((7, columns-2), (8, columns-2))]
    for first_row, positions in ((3, upper_flips), (5, lower_flips)):
        assert len(set(positions)) == len(positions)
        for position in positions:
            assert 0 <= position < width-1
            first_column = 2*position+1
            removed = {frozenset(((row, first_column), (row, first_column+1)))
                       for row in (first_row, first_row+1)}
            previous = len(matching)
            matching = [edge for edge in matching if frozenset(edge) not in removed]
            assert len(matching) == previous-2
            matching += [((first_row, column), (first_row+1, column))
                         for column in (first_column, first_column+1)]
    return 10, columns, selected, matching


def twice_charge(graph, region):
    return sum(graph['deg'][tile]-2*graph['r'][tile]
               for tile in region if graph['t'][tile] < 2)


def physical_record(current, expected_crossing=None, sharp=False, strands=False):
    rows, columns, selected, matching = current
    width = columns//2
    objective = direct_check(*current)
    mask = sum(1 << (row*columns+column) for row, column in selected)
    edges = tuple((first[0]*columns+first[1], second[0]*columns+second[1])
                  for first, second in matching)
    assert feasible(grid_graph(rows, columns)[0], mask, edges)
    graph, components = graph_record(*current)
    occupied = selected | {vertex for edge in matching for vertex in edge}
    band = {(row, column) for row in (4, 5) for column in range(columns)}
    assert all((3, column) in occupied and (6, column) in occupied for column in range(columns))
    assert all((row, column) not in occupied for row in (4, 5) for column in (0, columns-1))
    assert all((9-row, column) not in occupied
               for row, column in selected & band)
    blanks = len(band-occupied)
    selected_count = len(selected & band)
    internal = sum(first in band and second in band for first, second in matching)
    crossing = sum((first in band) != (second in band) for first, second in matching)
    assert 2*columns == selected_count+blanks+2*internal+crossing
    assert blanks-selected_count >= 4+crossing % 2
    upper = set(range(width, 2*width))
    receiver = set(range(2*width, 3*width))
    lower = set(range(3*width, 4*width))
    core = upper | receiver | lower
    sigma = sum(graph['s'][tile] for tile in receiver)
    assert sigma == 0
    assert twice_charge(graph, upper) == twice_charge(graph, lower) == 2
    assert twice_charge(graph, receiver) == selected_count-blanks+sigma
    assert twice_charge(graph, core) <= 0
    assert all((first in core) == (second in core) for first, second in graph['E'])
    assert sum(component['excess'] for component in components) == objective-rows*columns//2
    if expected_crossing is not None:
        assert crossing == expected_crossing
    if sharp:
        assert selected_count == 0 and blanks == 4
        assert twice_charge(graph, receiver) == -4 and twice_charge(graph, core) == 0
        assert objective == 12+6*width-4
        assert objective-rows*columns//2 == -4*(width-2)
    decompositions = []
    if strands:
        deficient_core = {tile for tile in core if graph['t'][tile] < 2}
        for choice_index in (0, 1):
            terminal = decompose(current, deficient_core, choice_index)
            assert terminal['terminal']['ports'] == 0
            assert terminal['counts']['LL'] <= terminal['counts']['SS']+terminal['reserve']
            assert terminal['shortage']*2 == twice_charge(graph, core)
            decompositions.append(dict(choice_index=choice_index, counts=terminal['counts'],
                                       reserves=terminal['reserve']))
    return dict(width=width, selected=selected_count, blanks=blanks, crossing=crossing,
                saturated_exports=sigma, band_charge_twice=twice_charge(graph, receiver),
                core_charge_twice=twice_charge(graph, core),
                capacity_two_band_tiles=sum(graph['r'][tile] == 2 for tile in receiver),
                decompositions=decompositions)


def band_matchings(vertices):
    if not vertices:
        yield []
        return
    first = min(vertices)
    remaining = vertices-{first}
    yield from band_matchings(remaining)
    for second in sorted(remaining):
        if sum(abs(first[axis]-second[axis]) for axis in (0, 1)) == 1:
            for rest in band_matchings(remaining-{second}):
                yield [(first, second)]+rest


def exhaustive_receiver(width):
    original = opposed_frame(width)
    vertices = {(row, column) for row in (4, 5) for column in range(1, 2*width-1)}
    outside_matching = [edge for edge in original[3] if edge[0] not in vertices]
    count = saturated_cases = 0
    for matching in band_matchings(vertices):
        used = {vertex for edge in matching for vertex in edge}
        candidates = sorted(vertices-used)
        for mask in range(1 << len(candidates)):
            chosen = {vertex for position, vertex in enumerate(candidates) if mask >> position & 1}
            occupied = used | chosen
            if any(sum(abs(vertex[axis]-neighbor[axis]) for axis in (0, 1)) == 1
                   for vertex in chosen for neighbor in occupied-{vertex}):
                continue
            current = *original[:2], original[2] | chosen, outside_matching+matching
            physical_record(current, expected_crossing=0, strands=True)
            graph, _ = graph_record(*current)
            saturated_cases += any(graph['t'][tile] == 2 for tile in range(2*width, 3*width))
            count += 1
    return dict(width=width, feasible_completions=count, with_saturated_band_tile=saturated_cases,
                maximum_pairing_controls=2*count)


def local_controls():
    valid_columns = []
    for upper, lower in itertools.product(range(3), repeat=2):
        valid = (upper != 1 or lower == 0) and (lower != 1 or upper == 0)
        weight = (upper == 0)+(lower == 0)-(upper == 1)-(lower == 1)
        if valid:
            assert weight >= 0
            valid_columns.append(3*upper+lower)
    assert len(valid_columns) == 6
    assert (1, 2) not in [divmod(column, 3) for column in valid_columns]
    missing_front_word = [(0, 0), (1, 2), (0, 0)]
    assert sum((upper == 0)+(lower == 0)-(upper == 1)-(lower == 1)
               for upper, lower in missing_front_word) == 3
    missing_endpoints_word = [(2, 0), (2, 0)]
    assert sum((upper == 0)+(lower == 0)-(upper == 1)-(lower == 1)
               for upper, lower in missing_endpoints_word) == 2
    return dict(valid_column_types=valid_columns, omitted_hypothesis_controls=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.max_width >= 4
    families = []
    witnesses = []
    symmetry_controls = 0
    for width in range(3, args.max_width+1):
        variants = [((), ()), ((0,), ()), ((0,), (width-2,)),
                    (tuple(range(width-1)), tuple(range(width-1)))]
        original_graph, _ = graph_record(*opposed_frame(width))
        original_charges = [twice_charge(original_graph, {tile}) for tile in range(original_graph['N'])]
        for upper, lower in variants:
            current = opposed_frame(width, upper, lower)
            record = physical_record(current, 2*(len(upper)+len(lower)), sharp=True, strands=True)
            graph, _ = graph_record(*current)
            assert [twice_charge(graph, {tile}) for tile in range(graph['N'])] == original_charges
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                assert direct_check(*shape, selected, matching) == direct_check(*current)
                image_graph, _ = graph_record(*shape, selected, matching)
                moved = transformed(*current[:2], {(row, col) for row in range(2, 8)
                                                   for col in range(2*width)}, [], *symmetry)[1]
                core = {row//2*(shape[1]//2)+col//2 for row, col in moved}
                assert twice_charge(image_graph, core) == 0
                symmetry_controls += 1
            record.update(upper_flips=list(upper), lower_flips=list(lower))
            families.append(record)
            if width == 3:
                witnesses.append(dict(shape=current[:2], selected=sorted(current[2]),
                                      matching=current[3], record=record))
    exhaustive = [exhaustive_receiver(3)]
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/OPPOSED_SOURCE_COMPENSATION.md',
               root/'formal/SubQuorum/OpposedBandCompensation.lean']
    sources.extend(Path(__file__).with_name(name) for name in
                   ('check_residual_corridors.py', 'check_terminal_strands.py',
                    'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', local=local_controls(), families=families,
                  sharp_source_cores=len(families), symmetry_controls=symmetry_controls,
                  exhaustive_receiver=exhaustive, witnesses=witnesses,
                  sha256={str(path.relative_to(root)):hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Independent grid controls; the all-length proof is written and Lean-checked. Small exhaustive receivers use fixed closed fronts; interacting families have actual source-band edges. No unrestricted theorem or full-grid Lean adapter.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:report[key] for key in
                     ('status', 'local', 'sharp_source_cores', 'symmetry_controls', 'exhaustive_receiver')}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: checks use assertions.')
    main()
