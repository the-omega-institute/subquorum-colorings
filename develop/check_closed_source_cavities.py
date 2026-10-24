"""Physical controls for complete-component cavity closure and nested sources."""

import argparse
import itertools
import json
from pathlib import Path

from check_adaptive_strip_compensation import certificate
from check_coalesced_mouths import assemble, move_source, optimize
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_mixed_source_contacts import source_with_chamber
from check_orthogonal_source_mouths import fill_greedily, inspect
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def add_vertical(selected, matching, column, start, finish, phase):
    selected.update({(start-1, column), (finish+1, column)})
    selected.update((row, column+phase*(1 if row % 2 else -1))
                    for row in range(start, finish+1))
    matching.extend(((row, column), (row+1, column))
                    for row in range(start, finish, 2))


def add_horizontal(selected, matching, row, start, finish):
    selected.update({(row, start-1), (row, finish+1)})
    selected.update((row+(-1 if column % 2 == 0 else 1), column)
                    for column in range(start, finish+1))
    matching.extend(((row, column), (row, column+1))
                    for column in range(start, finish, 2))


def obstructed_rung(width, depth):
    assert width >= 32 and width % 2 == 0 and depth >= 3
    source = source_with_chamber(width, depth)
    selected, matching = set(source['selected']), list(source['matching'])
    tip = 2*depth+4
    add_vertical(selected, matching, 9, 7, tip, -1)
    add_vertical(selected, matching, 22, 7, tip, 1)
    add_horizontal(selected, matching, 6, 14, 17)
    selected.update((row, column) for row in (tip, tip+1)
                    for column in (5, 7, *range(24, width+1, 2)))
    selected.update((tip, column) for column in (10, 12, 13, 15, 16, 18, 19, 21))
    selected.update((tip+1, column) for column in (11, 14, 17, 20))
    current = 2*depth+8, width+8, selected, matching
    cavity = set(itertools.product(range(4, tip+2), range(4, width+2)))
    rung = set(itertools.product((6, 7), range(10, 22)))
    return current, [source], cavity, rung


def nested_cavities(count, extra_depth=0, extra_width=0):
    width, depth = 16*count+32+extra_width, 4*count+2+extra_depth
    sources = [move_source(source_with_chamber(width-16*index, depth-4*index),
                           lambda point, index=index: (point[0]+8*index, point[1]+8*index))
               for index in range(count)]
    current = assemble(2*depth+8, width+8, sources)
    selected, matching = set(current[2]), list(current[3])
    tip = 2*depth+4
    for index in range(count):
        add_vertical(selected, matching, 6+8*index, 7+8*index, tip, 1)
        add_vertical(selected, matching, width-1-8*index, 7+8*index, tip, -1)
        add_horizontal(selected, matching, 6+8*index, 10+8*index, width-5-8*index)
    cavity = set(itertools.product(range(4, tip+2), range(4, width+2)))
    return (*current[:2], selected, matching), sources, cavity


def cavity_record(current, sources, cavity, allow_open=False):
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    components = endpoint_components(current)
    root = sources[0]
    assert not cavity & root['endpoints']
    assert all(component <= cavity for component in components
               if component != root['endpoints'] and component & cavity
               and (not allow_open or component in [source['endpoints'] for source in sources]))
    tiles = {(row//2, column//2) for row, column in cavity}
    assert vertices_of(tiles) == cavity
    rows = sorted({row for row, column in cavity})
    columns = sorted({column for row, column in cavity})
    boundary = {(row, column) for row in rows for column in (columns[0], columns[-1])}
    assert not boundary & endpoints
    assert len(boundary & current[2]) == len(rows)-2
    physical = [vertices_of({tile}) for tile in sorted(tiles)]
    shifted = [{(row, column) for row in (upper, upper+1)
                for column in (left, left+1)}
               for upper in rows[::2] for left in columns[1:-1:2]]
    assert set().union(*shifted) == cavity-boundary

    def partition_record(squares):
        payment = excess_twice = 0
        component_excess = [0]*len(components)
        for square in squares:
            paired = square & endpoints
            selected = len(square & current[2])
            assert selected <= 2
            if not paired:
                payment += 2-selected
                continue
            owners = [index for index, component in enumerate(components) if paired & component]
            assert len(owners) == 1
            value = len(paired)+2*selected-4
            excess_twice += value
            component_excess[owners[0]] += value
        return dict(payment=payment, excess_twice=excess_twice,
                    component_excess_twice=component_excess)

    first, second = partition_record(physical), partition_record(shifted)
    source_sets = [source['endpoints'] for source in sources[1:]]
    flux = 0
    for index, component in enumerate(components):
        if component in source_sets:
            assert first['component_excess_twice'][index] == 2
            assert second['component_excess_twice'][index] == -2
            continue
        local_flux = 0
        if component != root['endpoints']:
            for tile in {(row//2, column//2) for row, column in component}:
                cells = vertices_of({tile})
                if len(cells & component) == 1 and cells <= cavity:
                    count = len(cells & current[2])
                    assert count in (1, 2)
                    local_flux += 1 if count == 2 else -1
        assert first['component_excess_twice'][index]-second['component_excess_twice'][index] == 2*local_flux
        if not allow_open:
            assert local_flux == first['component_excess_twice'][index] == second['component_excess_twice'][index] == 0
        flux += local_flux
    assert first['payment'] == 2*len(sources)+flux+second['payment']
    assert checked['area']//2-checked['objective'] >= len(sources)+flux
    ledger = inspect(current, sources)
    return dict(source_count=len(sources), enclosed_combs=len(components)-len(sources),
                shape=current[:2], physical_tiles=len(physical), shifted_squares=len(shifted),
                removed_selected=len(boundary & current[2]), cavity_comb_flux=flux,
                physical=first, shifted=second,
                ledger=ledger)


def controls():
    records, witness = [], None
    for width, depth in itertools.product((32, 34, 48, 80), (3, 4, 7, 14)):
        current, sources, cavity, rung = obstructed_rung(width, depth)
        record = cavity_record(current, sources, cavity)
        assert record['ledger']['weighted_comb_flux'] == -2
        assert record['ledger']['physical_union_payment'] == 0
        assert certificate(current, sources)['independent_weight'] == 0
        assert rung & endpoint_data(current)[0]
        assert len(endpoint_components(current)) == 4
        assert optimize(current, sources)[2] == current[2]
        records.append(dict(kind='zero_mouth_and_intruded_unique_negative_pair_rung',
                            width=width, depth=depth, result=record))
        if (width, depth) == (32, 3):
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                           cavity=sorted(cavity), intruded_rung=sorted(rung), result=record)
    for count, extra_depth, extra_width in itertools.product((1, 2, 3, 5), (0, 3), (0, 20)):
        current, sources, cavity = nested_cavities(count, extra_depth, extra_width)
        record = cavity_record(current, sources, cavity)
        assert record['enclosed_combs'] == 3*count
        assert record['ledger']['weighted_comb_flux'] == -2*count
        records.append(dict(kind='nested_parallel_sources_and_mixed_combs', count=count,
                            extra_depth=extra_depth, extra_width=extra_width, result=record))
        filled = fill_greedily(current, sources, count)
        record = cavity_record(filled, sources, cavity)
        records.append(dict(kind='filled_nested_completion', count=count,
                            extra_depth=extra_depth, extra_width=extra_width, result=record))
    images = 0
    current, sources, cavity, rung = obstructed_rung(32, 3)
    for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
        checked = verify_terminal((*shape, selected, matching))
        assert checked['area']//2-checked['objective'] == current[0]*current[1]//2-len(current[2])-len(current[3])
        images += 1
    return dict(status='ALL_CHECKS_PASSED', physical_cases=len(records), symmetry_images=images,
                records=records, explicit_obstructed_rung_witness=witness,
                scope='Checks of complete-component cavity closure, exact physical/shifted raw '
                      'weights, nested parallel positive sources and mixed complete combs. '
                      'The explicit zero-mouth family blocks the unique negative-comb pair rung '
                      'with a third complete horizontal comb. General closed-cavity existence '
                      'and arbitrary positive bent sources remain open.')


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
