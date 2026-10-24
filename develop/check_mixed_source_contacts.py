"""Physical controls for signed flux with mixed combs and full source contacts."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_bent_cap_compensation import charge_twice
from check_coalesced_mouths import assemble, coalesce, move_source, optimize, source_record
from check_comb_end_debt import KINDS
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import graph_record, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def source_with_chamber(width, depth):
    source = source_record(width, depth)
    source['chamber'] = {(row, column) for row in (2, 3) for column in range(3, width+3)}
    return source


def source_family(count, kind):
    sources = [move_source(source_with_chamber(8*(count-index)+6,
                           2*count+1-index if kind == 'arms' else 1),
                           lambda point, index=index: (point[0]+4*index, point[1]+4*index))
               for index in range(count)]
    rows = 6*count+8 if kind == 'arms' else 4*count+6
    return assemble(rows, 8*count+14, sources), sources


def add_parallel(current, row, start, length, phase):
    selected, matching = set(current[2]), list(current[3])
    selected.update({(row, start-1), (row, start+length)})
    selected.update((row+phase*(1 if index % 2 else -1), start+index) for index in range(length))
    matching.extend(((row, column), (row, column+1)) for column in range(start, start+length, 2))
    return current[0], current[1], selected, matching


def comb_family(length, offset, row_offset, phase, kind):
    source = source_with_chamber(2*length+44, 3)
    current = assemble(18, 2*length+52, [source])
    current = add_parallel(current, 10+row_offset, 8+offset, length, phase)
    if kind is not None:
        upper, lower = KINDS[kind]
        column = length+18
        selected, matching = set(current[2]), list(current[3])
        selected.update({(9-upper, column), (11+lower, column)})
        selected.update((row, column+phase*(1 if (row-10) % 2 else -1))
                        for row in range(10-upper, 11+lower))
        matching.extend(((row, column), (row+1, column)) for row in range(10-upper, 10+lower, 2))
        current = current[0], current[1], selected, matching
    return current, [source]


def square_record(cells, current, endpoints, owner):
    endpoint_count = len(cells & endpoints)
    selected_count = len(cells & current[2])
    assert (endpoint_count, selected_count) in ((0, 0), (0, 1), (0, 2), (1, 1), (1, 2), (2, 1), (4, 0))
    owners = {owner[point] for point in cells & endpoints}
    assert len(owners) == int(bool(endpoint_count))
    return dict(endpoints=endpoint_count, selected=selected_count,
                owner=next(iter(owners)) if owners else None,
                raw_excess_twice=2*selected_count+endpoint_count-4)


def strip_record(current, strip, endpoints, components, owner):
    cells = strip['cells']
    horizontal = len({row for row, column in cells}) == 2
    if not horizontal:
        shape, selected, matching = transformed(*current, True, False, False)
        moved = dict(cells={(column, row) for row, column in cells},
                     tiles={(column, row) for row, column in strip['tiles']})
        moved_components = [{(column, row) for row, column in component} for component in components]
        moved_owner = {(column, row): index for (row, column), index in owner.items()}
        return strip_record((*shape, selected, matching), moved,
                            {(column, row) for row, column in endpoints}, moved_components, moved_owner)
    rows = sorted({row for row, column in cells})
    columns = sorted({column for row, column in cells})
    assert all((row, column) not in endpoints | current[2] for row in rows
               for column in (columns[0], columns[-1]))
    physical = [square_record(vertices_of({tile}), current, endpoints, owner) for tile in sorted(strip['tiles'])]
    shifted = [square_record({(row, target) for row in rows for target in (column, column+1)},
                            current, endpoints, owner) for column in columns[1:-1:2]]
    sparse = sum(record['endpoints'] == record['selected'] == 1 for record in physical)
    saturated = sum((record['endpoints'], record['selected']) == (1, 2) for record in physical)
    shifted_sparse = sum(record['endpoints'] == record['selected'] == 1 for record in shifted)
    shifted_saturated = sum((record['endpoints'], record['selected']) == (1, 2) for record in shifted)
    assert shifted_saturated-shifted_sparse == sparse-saturated
    deficit = sum(2-record['selected'] for record in physical if not record['endpoints'])
    shifted_deficit = sum(2-record['selected'] for record in shifted if not record['endpoints'])
    assert deficit == 2-sparse+saturated+shifted_deficit
    parallel = 0
    for index, component in enumerate(components):
        if component & cells and len({row for row, column in component}) == 1:
            assert component <= cells
            assert sum(record['raw_excess_twice'] for record in physical if record['owner'] == index) == 0
            assert sum(record['raw_excess_twice'] for record in shifted if record['owner'] == index) == 0
            parallel += 1
    return dict(sparse=sparse, saturated=saturated, shifted_sparse=shifted_sparse,
                shifted_saturated=shifted_saturated, physical_payment=deficit,
                shifted_deficit=shifted_deficit, physical_four_endpoint_tiles=sum(
                    record['endpoints'] == 4 for record in physical), shifted_four_endpoint_squares=sum(
                    record['endpoints'] == 4 for record in shifted), parallel_combs=parallel,
                individual_type_swap_holds=(shifted_sparse == saturated and shifted_saturated == sparse))


def inspect(current, sources):
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    components = endpoint_components(current)
    source_components = [source['endpoints'] for source in sources]
    for component in source_components:
        assert component in components
    combs = [component for component in components if component not in source_components]
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*len(combs)+[2]*len(sources)
    owner = {point: index for index, component in enumerate(components) for point in component}
    chamber_contacts = arm_contacts = tip_contacts = 0
    for source in sources:
        horizontal = len({row for row, column in source['mouth']}) == 2
        for other in sources:
            if other is source:
                continue
            contacts = other['endpoints'] & source['mouth']
            if contacts:
                assert horizontal == (len({row for row, column in other['mouth']}) == 2)
                chamber_contacts += len(contacts & other['chamber'])
                tip_contacts += len(contacts & other['tips'])
                arm_contacts += len(contacts-other['chamber']-other['tips'])
    strips = coalesce(sources)
    union = set().union(*(strip['tiles'] for strip in strips))
    tip_tiles = {(row//2, column//2) for source in sources for row, column in source['tips']}
    internal_tips = tip_tiles & union
    assert len(tip_tiles) == 2*len(sources)
    assert len(internal_tips) == 2*len(sources)-2*len(strips)
    records = [strip_record(current, strip, endpoints, components, owner) for strip in strips]
    internal = outward = inward = 0
    for component in combs:
        sparse, saturated = set(), set()
        for tile in {(row//2, column//2) for row, column in component}:
            cells = vertices_of({tile})
            if len(cells & component) == 1:
                (saturated if len(cells & current[2]) == 2 else sparse).add(tile)
        assert len(sparse) == len(saturated) <= 1
        first, second = bool(sparse & union), bool(saturated & union)
        internal += first and second
        outward += first and not second
        inward += second and not first
    assert sum(record['sparse'] for record in records) == internal+outward
    assert sum(record['saturated'] for record in records) == internal+inward+len(internal_tips)
    payment = sum(record['physical_payment'] for record in records)
    shifted = sum(record['shifted_deficit'] for record in records)
    assert payment == 2*len(sources)+inward-outward+shifted
    all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
    receiver_tiles = {(row//2, column//2) for row, column in endpoints}
    outside = sum(2-len(vertices_of({tile}) & current[2]) for tile in all_tiles-union-receiver_tiles)
    deficit = current[0]*current[1]//2-checked['objective']
    assert deficit == len(sources)+inward-outward+shifted+outside
    graph, _ = graph_record(*current)
    source_tiles = {(row//2, column//2) for component in source_components for row, column in component}
    positive = [tile for tile in source_tiles & union if charge_twice(graph, current[1], tile) > 0]
    return dict(sources=len(sources), combs=len(combs), merged_strips=len(strips),
                internal_comb_contacts=internal, outward_contacts=outward, inward_contacts=inward,
                internal_source_tips=len(internal_tips), chamber_contact_endpoints=chamber_contacts,
                nonterminal_arm_contact_endpoints=arm_contacts, source_tip_contacts=tip_contacts,
                physical_payment=payment, shifted_deficit=shifted, objective=checked['objective'],
                half_area_deficit=deficit, positive_corrected_source_tiles_in_union=len(positive),
                positive_corrected_source_charge_twice=sum(charge_twice(graph, current[1], tile) for tile in positive),
                strip_records=records)


def symmetry_check(current, sources):
    for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
        def move(point):
            row, column = point
            row = current[0]-1-row if vertical else row
            column = current[1]-1-column if horizontal else column
            return (column, row) if transpose else (row, column)
        inspect((*shape, selected, matching), [move_source(source, move) for source in sources])
    return 8


def controls():
    records, images, witness = [], 0, None
    for kind, count in itertools.product(('arms', 'chambers'), (*range(1, 13), 16, 24)):
        current, sources = source_family(count, kind)
        baseline = inspect(current, sources)
        if kind == 'arms':
            assert len(current[2]) == 6*count*count+12*count
            assert len(current[3]) == 7*count*count+14*count
            assert baseline['nonterminal_arm_contact_endpoints'] == 2*count*(count-1)
            assert baseline['positive_corrected_source_tiles_in_union'] == 2*(count-1)
            assert baseline['positive_corrected_source_charge_twice'] == 2*(count-1)
        else:
            assert len(current[2]) == 10*count
            assert len(current[3]) == 4*count*count+13*count
            assert sum(record['physical_four_endpoint_tiles'] for record in baseline['strip_records']) == 2*(count*count-1)
        current = optimize(current, sources)
        record = inspect(current, sources)
        assert record['physical_payment'] >= 2*count
        records.append(dict(kind=kind, count=count, baseline=baseline, filled=record))
        if count in (2, 5, 12):
            images += symmetry_check(current, sources)
    failed_type_swaps = 0
    for length, offset, row_offset, phase, kind in itertools.product((2, 4, 8, 12), (0, 1),
                                                                   (0, 1), (-1, 1), (None, *KINDS)):
        current, sources = comb_family(length, offset, row_offset, phase, kind)
        current = optimize(current, sources)
        record = inspect(current, sources)
        failed_type_swaps += not record['strip_records'][0]['individual_type_swap_holds']
        records.append(dict(kind='mixed_combs', length=length, offset=offset, row_offset=row_offset,
                            phase=phase, perpendicular_kind=kind, result=record))
        if length == 4 and offset == row_offset == 0 and phase == 1 and kind is None:
            assert (record['strip_records'][0]['sparse'], record['strip_records'][0]['saturated'],
                    record['strip_records'][0]['shifted_sparse'], record['strip_records'][0]['shifted_saturated']) == (0, 0, 1, 1)
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3], result=record)
    first, first_sources = source_family(3, 'arms')
    first = add_parallel(first, 22, 16, 4, 1)
    other, other_sources = source_family(3, 'chambers')
    moved = [move_source(source, lambda point: (point[1], point[0]+first[1]+4)) for source in other_sources]
    mixed = (max(first[0], other[1]), first[1]+4+other[0],
             first[2] | set().union(*(source['selected'] for source in moved)),
             first[3]+[edge for source in moved for edge in source['matching']])
    sources = first_sources+moved
    mixed = optimize(mixed, sources)
    records.append(dict(kind='mixed_orientation_source_clusters', result=inspect(mixed, sources)))
    images += symmetry_check(mixed, sources)
    assert failed_type_swaps and witness is not None
    return dict(status='ALL_CHECKS_PASSED', configurations=len(records), symmetry_images=images,
                individual_type_swap_failures=failed_type_swaps, family=records, witness=witness,
                scope='Finite physical controls for the independent general signed-imbalance proof. '
                      'All-k baseline arm/chamber source families use explicit formulas only. '
                      'Strip optimization is supplementary; no universal grid or full Lean claim.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('family', 'witness')}))


if __name__ == '__main__':
    main()
