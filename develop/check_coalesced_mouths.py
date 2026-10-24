"""Physical controls for coalesced mouths and internal saturated source tips."""

import argparse
import itertools
import json
from pathlib import Path

from check_comb_end_debt import KINDS
from check_comb_end_flux import flux_record
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_long_bent_terminal_strips import terminal_strip
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed
from check_saturated_bent_bands import long_bent
from check_transverse_comb_mouths import optimize_strip


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def move_source(source, move):
    return {key: ([tuple(move(point) for point in edge) for edge in value]
                  if key == 'matching' else {move(point) for point in value})
            for key, value in source.items()}


def source_record(width, depth):
    current, _ = long_bent(width, depth, saturate=False)
    return dict(selected=current[2], matching=current[3], endpoints=endpoint_data(current)[0],
                mouth=terminal_strip(width, depth), tips={(2*depth+4, 3), (2*depth+4, width+2)})


def assemble(rows, columns, sources):
    return (rows, columns, set().union(*(source['selected'] for source in sources)),
            [edge for source in sources for edge in source['matching']])


def nested_family(count, extra_width=0):
    sources = [move_source(source_record(8*(count-index)+6+extra_width, 2*(count-index)+1),
                           lambda point, index=index: (point[0]+4*index, point[1]+4*index))
               for index in range(count)]
    return assemble(4*count+10, 8*count+14+extra_width, sources), sources


def alternating_family(count):
    sources = [move_source(source_record(22, 3),
                           lambda point, index=index: (21-point[0] if index % 2 else point[0],
                                                       point[1]+14*index))
               for index in range(count)]
    return assemble(22, 14*count+16, sources), sources


def sharp_nested_family(count):
    current, sources = nested_family(count)
    raw_tip, inner_left = 4*count+4, 4*(count-1)
    additions = {(raw_tip+1, 4*index-2) for index in range(1, count)}
    additions.update((raw_tip+1, 8*count+7-4*index) for index in range(1, count))
    additions.update((row, inner_left+offset) for row in (raw_tip, raw_tip+1)
                     for offset in (3, 5, 7, 9, 11))
    selected = current[2] | {(row+2, column+3) for row, column in additions}
    return (current[0], current[1], selected, current[3]), sources


def add_contacts(current, source_count, count, kind, phase):
    selected, matching = set(current[2]), list(current[3])
    tip = 4*source_count+6
    upper, lower = KINDS[kind]
    for index in range(count):
        column = 4*source_count+4+4*index
        points = [(row, column) for row in range(tip-upper, tip+lower+1)]
        matching.extend(zip(points[::2], points[1::2]))
        selected.update({(tip-upper-1, column), (tip+lower+1, column)})
        selected.update((row, column+phase*(1 if (row-tip) % 2 else -1))
                        for row in range(tip-upper, tip+lower+1))
    rows = max(current[0], max(row for row, column in selected)+1)
    return rows+rows % 2, current[1], selected, matching


def bridge_family(source_count, comb_count):
    first, sources = nested_family(source_count, 4*comb_count)
    axis = 8*source_count+21
    others = [move_source(source, lambda point: (axis-point[0], point[1])) for source in sources]
    sources = sources+others
    current = assemble(8*source_count+22, first[1], sources)
    selected, matching = set(current[2]), list(current[3])
    for index in range(comb_count):
        column = 4*source_count+4+4*index
        start, finish = 4*source_count+7, 4*source_count+14
        selected.update({(start-1, column), (finish+1, column)})
        selected.update((row, column-1 if row % 2 else column+1) for row in range(start, finish+1))
        matching.extend(((row, column), (row+1, column)) for row in range(start, finish, 2))
    return (current[0], current[1], selected, matching), sources


def coalesce(sources):
    groups = {}
    for index, source in enumerate(sources):
        tiles = {(row//2, column//2) for row, column in source['mouth']}
        horizontal = len({row for row, column in tiles}) == 1
        band = next(iter(tiles))[0 if horizontal else 1]
        positions = {tile[1 if horizontal else 0] for tile in tiles}
        groups.setdefault((horizontal, band), []).append((min(positions), max(positions), index))
    result = []
    for (horizontal, band), intervals in groups.items():
        merged = []
        for lower, upper, index in sorted(intervals):
            if merged and lower <= merged[-1][1]+1:
                merged[-1][1] = max(merged[-1][1], upper)
                merged[-1][2].append(index)
            else:
                merged.append([lower, upper, [index]])
        for lower, upper, members in merged:
            tiles = {(band, position) if horizontal else (position, band)
                     for position in range(lower, upper+1)}
            result.append(dict(tiles=tiles, cells=vertices_of(tiles), members=members))
    used = set()
    for strip in result:
        assert not used & strip['tiles']
        used.update(strip['tiles'])
    assert vertices_of(used) == set().union(*(source['mouth'] for source in sources))
    return result


def optimize(current, sources):
    for strip in coalesce(sources):
        if len({row for row, column in strip['cells']}) == 2:
            current = optimize_strip(current, strip['cells'])
        else:
            shape, selected, matching = transformed(*current, True, False, False)
            cells = {(column, row) for row, column in strip['cells']}
            turned = optimize_strip((*shape, selected, matching), cells)
            shape, selected, matching = transformed(*turned, True, False, False)
            current = *shape, selected, matching
    return current


def inspect(current, sources):
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    components = endpoint_components(current)
    for source in sources:
        assert source['endpoints'] in components
    combs = [component for component in components
             if component not in [source['endpoints'] for source in sources]]
    assert all(len({row for row, column in component}) == 1 or
               len({column for row, column in component}) == 1 for component in combs)
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*len(combs)+[2]*len(sources)
    strips = coalesce(sources)
    union = set().union(*(strip['tiles'] for strip in strips))
    tip_tiles = {(row//2, column//2) for source in sources for row, column in source['tips']}
    assert len(tip_tiles) == 2*len(sources)
    internal_tips = tip_tiles & union
    assert len(internal_tips) == 2*len(sources)-2*len(strips)
    assert all(len(vertices_of({tile}) & current[2]) == 2 for tile in tip_tiles)
    internal = outward = inward = 0
    for component in combs:
        sparse, saturated = set(), set()
        tiles = {(row//2, column//2) for row, column in component}
        for tile in tiles:
            cells = vertices_of({tile})
            if len(cells & component) == 1:
                count = len(cells & current[2])
                assert count in (1, 2)
                (sparse if count == 1 else saturated).add(tile)
        assert len(sparse) == len(saturated) <= 1
        sparse_inside, saturated_inside = bool(sparse & union), bool(saturated & union)
        internal += sparse_inside and saturated_inside
        outward += sparse_inside and not saturated_inside
        inward += saturated_inside and not sparse_inside
    records = [flux_record(current, strip['cells']) for strip in strips]
    assert sum(record['sparse_ends'] for record in records) == internal+outward
    assert sum(record['saturated_ends'] for record in records) == internal+inward+len(internal_tips)
    payment = sum(record['no_endpoint_deficit'] for record in records)
    shifted = sum(record['shifted_no_endpoint_deficit'] for record in records)
    assert payment == 2*len(sources)+inward-outward+shifted
    all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
    receivers = {(row//2, column//2) for row, column in endpoints}
    remainder = sum(2-len(vertices_of({tile}) & current[2]) for tile in all_tiles-union-receivers)
    deficit = current[0]*current[1]//2-checked['objective']
    assert deficit == len(sources)+inward-outward+shifted+remainder
    original_claims = sum(len(source['mouth'])//4 for source in sources)
    duplicate_payment = sum(flux_record(current, source['mouth'])['no_endpoint_deficit'] for source in sources)
    return dict(sources=len(sources), merged_strips=len(strips), internal_source_tips=len(internal_tips),
                contact_combs=len(combs), internal_comb_contacts=internal, outward_contacts=outward,
                inward_contacts=inward, physical_payment=payment, shifted_deficit=shifted,
                outside_deficit=remainder, objective=checked['objective'], half_area_deficit=deficit,
                repeated_mouth_tile_claims=original_claims-len(union),
                naive_repeated_donor_sum=duplicate_payment, strip_records=records)


def symmetry_check(current, sources):
    for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
        def move(point):
            row, column = point
            row = current[0]-1-row if vertical else row
            column = current[1]-1-column if horizontal else column
            return (column, row) if transpose else (row, column)
        moved = [move_source(source, move) for source in sources]
        inspect((*shape, selected, matching), moved)
    return 8


def controls():
    records, images = [], 0
    witness = None
    for count in (*range(1, 17), 24, 40):
        current, sources = nested_family(count)
        baseline = inspect(current, sources)
        assert len(current[2]) == 4*count*count+14*count
        assert len(current[3]) == 6*count*count+15*count
        assert baseline['physical_payment'] == 4*count+8
        assert baseline['shifted_deficit'] == 2*count+8
        current, sources = sharp_nested_family(count)
        record = inspect(current, sources)
        assert record['physical_payment'] == 2*count and record['shifted_deficit'] == 0
        assert len(current[2]) == 4*count*count+16*count+8
        assert record['objective'] == 10*count*count+31*count+8
        assert record['naive_repeated_donor_sum'] == count*(count+1)
        assert record['repeated_mouth_tile_claims'] == 2*(count*count-1)
        records.append(dict(kind='explicit_sharp_nested', count=count, baseline=baseline, filled=record))
        if count in (1, 3, 8):
            images += symmetry_check(current, sources)
        if count == 3:
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                           mouths=[sorted(source['mouth']) for source in sources], result=record)
    for count in range(1, 13):
        current, sources = alternating_family(count)
        current = optimize(current, sources)
        record = inspect(current, sources)
        assert record['physical_payment'] == 2*count and record['shifted_deficit'] == 0
        records.append(dict(kind='alternating_interleaved', count=count, optimized=record))
    for count, comb_count, kind, phase in itertools.product(range(1, 7), range(1, 4), KINDS, (-1, 1)):
        current, sources = nested_family(count, 4*comb_count)
        current = optimize(add_contacts(current, count, comb_count, kind, phase), sources)
        record = inspect(current, sources)
        records.append(dict(kind='nested_with_contacts', count=count, comb_count=comb_count,
                            contact_kind=kind, phase=phase, optimized=record))
    for count, comb_count in itertools.product(range(1, 7), range(1, 5)):
        current, sources = bridge_family(count, comb_count)
        current = optimize(current, sources)
        record = inspect(current, sources)
        assert record['merged_strips'] == 2 and record['internal_comb_contacts'] == comb_count
        assert record['outward_contacts'] == record['inward_contacts'] == 0
        assert record['physical_payment'] >= 4*count
        records.append(dict(kind='nested_bridge', count=count, comb_count=comb_count, optimized=record))
    first, sources = nested_family(3)
    other, other_sources = alternating_family(4)
    moved = [move_source(source, lambda point: (point[1], point[0]+first[1]+4)) for source in other_sources]
    sources = sources+moved
    mixed = assemble(max(first[0], other[1]), first[1]+4+other[0], sources)
    mixed = optimize(mixed, sources)
    records.append(dict(kind='mixed_orientation_clusters', optimized=inspect(mixed, sources)))
    images += symmetry_check(mixed, sources)
    return dict(status='ALL_CHECKS_PASSED', configurations=len(records), symmetry_images=images,
                family=records, witness=witness,
                scope='Independent finite physical controls for a separate general written proof. '
                      'Explicit arbitrary-k sharp nested family uses no optimizer. Strip optimization is '
                      'only a finite control. No new Lean or universal-grid claim.')


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
