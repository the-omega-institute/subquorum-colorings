"""Whole-source phase controls for arbitrary orientations inside a source cavity."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_closed_source_cavities import add_vertical
from check_coalesced_mouths import assemble, move_source
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_mixed_source_contacts import source_with_chamber
from check_orthogonal_source_mouths import fill_greedily, inspect
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def flank_record(source, selected):
    rows = sorted({row for row, column in source['chamber']})
    columns = sorted({column for row, column in source['chamber']})
    assert len(columns) == 2 and len(rows) >= 8 and len(rows) % 2 == 0
    rightward = min(column for row, column in source['tips']) > columns[-1]
    outer = columns[0]-1 if rightward else columns[-1]+1
    inner = columns[-1]+1 if rightward else columns[0]-1
    outer_count = sum((row, outer) in selected for row in rows)
    inner_count = sum((row, inner) in selected for row in rows[1:-1])
    assert not {(rows[1], inner), (rows[-2], inner)} & selected
    assert all(not {(first, outer), (first+1, outer)} <= selected for first in rows[:-1])
    assert all(not {(first, inner), (first+1, inner)} <= selected for first in rows[1:-2])
    assert 2*outer_count <= len(rows)
    assert 2*inner_count <= len(rows)-4
    gain = len(rows)-outer_count-inner_count
    assert gain >= 2
    return dict(width=len(rows), outer_count=outer_count, inner_count=inner_count,
                phase_gain=gain, extra_gain=gain-2)


def sharpen_flanks(current, sources):
    selected = set(current[2])
    for source in sources[1:]:
        if len({row for row, column in source['chamber']}) == 2:
            continue
        rows = sorted({row for row, column in source['chamber']})
        columns = sorted({column for row, column in source['chamber']})
        rightward = min(column for row, column in source['tips']) > columns[-1]
        outer = columns[0]-1 if rightward else columns[-1]+1
        inner = columns[-1]+1 if rightward else columns[0]-1
        selected.update((row, outer) for row in rows[::2])
        selected.update((row, inner) for row in rows[2:-2:2])
    return *current[:2], selected, current[3]


def occupied_perpendicular_rung(width, depth, sharp):
    root = source_with_chamber(width, depth)
    inner = move_source(source_with_chamber(8, 1),
                        lambda point: (point[1]+4, point[0]+12))
    current = assemble(2*depth+8, width+8, [root, inner])
    selected, matching = set(current[2]), list(current[3])
    tip = 2*depth+4
    add_vertical(selected, matching, 9, 7, tip, -1)
    add_vertical(selected, matching, 22, 7, tip, 1)
    selected.update((row, column) for row in (tip, tip+1)
                    for column in (5, 7, *range(24, width+1, 2)))
    selected.update((tip, column) for column in (10, 12, 13, 15, 16, 18, 19, 21))
    selected.update((tip+1, column) for column in (11, 14, 17, 20))
    current = *current[:2], selected, matching
    if sharp:
        current = sharpen_flanks(current, [root, inner])
    cavity = set(itertools.product(range(4, tip+2), range(4, width+2)))
    return current, [root, inner], cavity


def packed_sources(orientations, sharp):
    count = len(orientations)
    depth = 16*count+12
    root = source_with_chamber(48, depth)
    sources = [root]
    for index, transpose in enumerate(orientations):
        source = source_with_chamber(8+2*(index % 3), 1+index % 2)
        def move(point, index=index, transpose=transpose):
            row, column = (point[1], point[0]) if transpose else point
            row = 17-row if index % 2 else row
            column = 17-column if index % 3 == 1 else column
            return row+8+32*index, column+8
        sources.append(move_source(source, move))
    current = assemble(2*depth+8, 56, sources)
    if sharp:
        current = sharpen_flanks(current, sources)
    cavity = set(itertools.product(range(4, 2*depth+6), range(4, 50)))
    return current, sources, cavity


def record(current, sources, cavity):
    if len({row for row, column in sources[0]['chamber']}) != 2:
        shape, selected, matching = transformed(*current, True, False, False)
        return record((*shape, selected, matching),
                      [move_source(source, lambda point: (point[1], point[0])) for source in sources],
                      {(column, row) for row, column in cavity})
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    components = endpoint_components(current)
    assert all(source['endpoints'] in components for source in sources)
    assert not sources[0]['endpoints'] & cavity
    assert all(source['endpoints'] <= cavity for source in sources[1:])
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*(len(components)-len(sources))+[2]*len(sources)
    rows = sorted({row for row, column in cavity})
    columns = sorted({column for row, column in cavity})
    boundary = {(row, column) for row in rows for column in (columns[0], columns[-1])}
    assert not boundary & endpoints
    assert len(boundary & current[2]) == len(rows)-2
    tiles = {(row//2, column//2) for row, column in cavity}
    assert vertices_of(tiles) == cavity
    physical = [vertices_of({tile}) for tile in sorted(tiles)]
    shifted = [{(row, column) for row in (upper, upper+1) for column in (left, left+1)}
               for upper in rows[::2] for left in columns[1:-1:2]]
    owner = {point: index for index, component in enumerate(components) for point in component}

    def partition(squares):
        payment, raw = 0, Counter()
        for square in squares:
            paired = square & endpoints
            chosen = len(square & current[2])
            assert chosen <= 2
            if not paired:
                payment += 2-chosen
                continue
            owners = {owner[point] for point in paired}
            assert len(owners) == 1
            raw[next(iter(owners))] += len(paired)+2*chosen-4
        return payment, raw

    original_payment, original_raw = partition(physical)
    shifted_payment, shifted_raw = partition(shifted)
    extras, phases, comb_flux = 0, [], 0
    for index, component in enumerate(components):
        source = next((source for source in sources if source['endpoints'] == component), None)
        difference = original_raw[index]-shifted_raw[index]
        if source is sources[0]:
            assert original_raw[index] == shifted_raw[index] == 0
        elif source is not None:
            assert original_raw[index] == 2
            if len({row for row, column in source['chamber']}) == 2:
                assert shifted_raw[index] == -2
                phases.append(dict(direction='parallel', phase_gain=2, extra_gain=0))
            else:
                phase = flank_record(source, current[2])
                assert difference == 2*phase['phase_gain']
                assert shifted_raw[index] <= -2
                extras += phase['extra_gain']
                phases.append(dict(direction='perpendicular', **phase))
        else:
            for tile in {(row//2, column//2) for row, column in component}:
                cells = vertices_of({tile})
                if len(cells & component) == 1 and cells <= cavity:
                    comb_flux += 1 if len(cells & current[2]) == 2 else -1
    source_raw_difference = sum(2*phase['phase_gain'] for phase in phases)
    assert sum(original_raw.values())-sum(shifted_raw.values()) == source_raw_difference+2*comb_flux
    assert original_payment == 2*len(sources)+comb_flux+extras+shifted_payment
    deficit = checked['area']//2-checked['objective']
    assert deficit >= len(sources)+comb_flux+extras
    return dict(sources=len(sources), source_phases=phases, comb_flux=comb_flux,
                extra_perpendicular_gain=extras, physical_payment=original_payment,
                shifted_payment=shifted_payment, half_area_deficit=deficit,
                original_mouth_ledger=inspect(current, sources))


def controls():
    records, images, witness = [], 0, None
    for width, depth, sharp in itertools.product((32, 48, 80), (7, 12, 25), (False, True)):
        current, sources, cavity = occupied_perpendicular_rung(width, depth, sharp)
        result = record(current, sources, cavity)
        assert result['comb_flux'] == 0
        assert result['source_phases'][0]['phase_gain'] == (2 if sharp else 8)
        assert result['original_mouth_ledger']['weighted_comb_flux'] == -2
        records.append(dict(kind='perpendicular_source_in_occupied_pair_rung', width=width,
                            depth=depth, sharp=sharp, result=result))
        if (width, depth, sharp) == (32, 7, True):
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3], result=result)
            for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
                def move(point):
                    row, column = point
                    row = current[0]-1-row if vertical else row
                    column = current[1]-1-column if horizontal else column
                    return (column, row) if transpose else (row, column)
                image = record((*shape, selected, matching),
                               [move_source(source, move) for source in sources],
                               {move(point) for point in cavity})
                assert image['physical_payment'] == result['physical_payment']
                assert image['source_phases'][0]['phase_gain'] == 2
                images += 1
    for count in (1, 2, 3, 5):
        patterns = list(itertools.product((False, True), repeat=count)) if count <= 3 else [
            (False,)*count, (True,)*count, tuple(index % 2 == 1 for index in range(count))]
        for orientations, sharp in itertools.product(patterns, (False, True)):
            current, sources, cavity = packed_sources(orientations, sharp)
            result = record(current, sources, cavity)
            if sharp:
                assert all(phase['phase_gain'] == 2 for phase in result['source_phases'])
            records.append(dict(kind='arbitrary_source_direction_pattern', orientations=orientations,
                                sharp=sharp, result=result))
            if not sharp:
                filled = fill_greedily(current, sources, count)
                completion = record(filled, sources, cavity)
                records.append(dict(kind='filled_mixed_direction_completion',
                                    orientations=orientations, result=completion))
    return dict(status='ALL_CHECKS_PASSED', physical_cases=len(records), symmetry_images=images,
                records=records, sharp_perpendicular_witness=witness,
                scope='General written complete-source perpendicular phase bound >=2, exact flank '
                      'counts, and arbitrary-orientation enclosed-source cavity identity. Physical '
                      'geometry and normalization remain written; partial foreign sources, general '
                      'cavity existence and the universal grid theorem remain open.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('status', 'physical_cases', 'symmetry_images')}))


if __name__ == '__main__':
    main()
