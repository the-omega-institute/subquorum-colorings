"""Physical controls for arbitrary source directions and crossing losses."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_coalesced_mouths import assemble, move_source
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors
from check_mixed_source_contacts import add_parallel, source_with_chamber
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def strips_of(sources):
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
            result.append(dict(horizontal=horizontal, tiles=tiles,
                               cells=vertices_of(tiles), members=members))
    return result


def feasible(current):
    rows, columns, selected, matching = current
    endpoints = endpoint_data(current)[0]
    return (len(endpoints) == 2*len(matching) and not endpoints & selected
            and all(0 <= row < rows and 0 <= column < columns for row, column in selected | endpoints)
            and all(len(set(neighbors(point)) & (selected | endpoints)) <= 1 for point in selected))


def fill_greedily(current, sources, seed):
    selected = set(current[2])
    endpoints = endpoint_data(current)[0]
    occupied = selected | endpoints
    choices = sorted(set().union(*(source['mouth'] for source in sources))-selected-endpoints)
    random.Random(seed).shuffle(choices)
    for point in choices:
        adjacent = set(neighbors(point))
        if len(adjacent & occupied) <= 1 and all(
                not set(neighbors(target)) & occupied for target in adjacent & selected):
            selected.add(point)
            occupied.add(point)
    return *current[:2], selected, current[3]


def square_data(cells, current, endpoints, owner):
    paired = cells & endpoints
    owners = {owner[point] for point in paired}
    assert len(owners) == int(bool(paired))
    selected = len(cells & current[2])
    assert selected <= 2
    return dict(endpoints=len(paired), selected=selected,
                owner=next(iter(owners)) if owners else None,
                excess_twice=len(paired)+2*selected-4)


def strip_data(current, strip, sources, components, owner):
    endpoints = endpoint_data(current)[0]
    horizontal = strip['horizontal']
    transverse = sorted({point[0 if horizontal else 1] for point in strip['cells']})
    axial = sorted({point[1 if horizontal else 0] for point in strip['cells']})
    point_of = lambda across, along: (across, along) if horizontal else (along, across)
    assert not {point_of(across, along) for across in transverse
                for along in (axial[0], axial[-1])} & (endpoints | current[2])
    physical = [square_data(vertices_of({tile}), current, endpoints, owner) for tile in strip['tiles']]
    shifted = [square_data({point_of(across, along) for across in transverse
                            for along in (start, start+1)}, current, endpoints, owner)
               for start in axial[1:-1:2]]
    physical_payment = sum(2-record['selected'] for record in physical if not record['endpoints'])
    shifted_payment = sum(2-record['selected'] for record in shifted if not record['endpoints'])
    parallel_tips = comb_flux = perpendicular_gain = 0
    contacts = []
    for index, component in enumerate(components):
        if not component & strip['cells']:
            continue
        first = sum(record['excess_twice'] for record in physical if record['owner'] == index)
        second = sum(record['excess_twice'] for record in shifted if record['owner'] == index)
        difference = first-second
        source = next((source for source in sources if source['endpoints'] == component), None)
        if source is None:
            assert first == -second
            comb_flux += difference//2
        elif horizontal == (len({row for row, column in source['mouth']}) == 2):
            tips = len({(row//2, column//2) for row, column in source['tips']} & strip['tiles'])
            assert difference == 2*tips
            parallel_tips += tips
        else:
            chamber = source['chamber'] & strip['cells']
            tips = len(source['tips'] & strip['cells'])
            chamber_rows = len({point[0 if horizontal else 1] for point in chamber})
            assert chamber and chamber_rows in (1, 2)
            assert (first, tips) == ((0, 0) if chamber_rows == 2 else (1, 1))
            assert difference % 2 == 0
            gain = difference//2
            assert 0 <= gain <= chamber_rows
            perpendicular_gain += gain
            contacts.append(dict(chamber_rows=chamber_rows, tips=tips, physical_excess_twice=first,
                                 shifted_excess_twice=second, phase_gain=gain))
    assert physical_payment == 2+parallel_tips+comb_flux+perpendicular_gain+shifted_payment
    return dict(physical_payment=physical_payment, shifted_payment=shifted_payment,
                parallel_tips=parallel_tips, comb_flux=comb_flux,
                perpendicular_gain=perpendicular_gain, perpendicular_contacts=contacts)


def inspect(current, sources):
    assert feasible(current)
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    components = endpoint_components(current)
    source_components = [source['endpoints'] for source in sources]
    assert all(component in components for component in source_components)
    combs = [component for component in components if component not in source_components]
    assert all(len({row for row, column in component}) == 1 or
               len({column for row, column in component}) == 1 for component in combs)
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*len(combs)+[2]*len(sources)
    owner = {point: index for index, component in enumerate(components) for point in component}
    strips = strips_of(sources)
    multiplicities = Counter(tile for strip in strips for tile in strip['tiles'])
    assert max(multiplicities.values()) <= 2
    crossing_tiles = {tile for tile, count in multiplicities.items() if count == 2}
    union = set(multiplicities)
    records = [strip_data(current, strip, sources, components, owner) for strip in strips]
    assert sum(record['parallel_tips'] for record in records) == 2*len(sources)-2*len(strips)
    outward = inward = duplicate_sparse = duplicate_saturated = 0
    for component in combs:
        sparse, saturated = set(), set()
        for tile in {(row//2, column//2) for row, column in component}:
            cells = vertices_of({tile})
            if len(cells & component) == 1:
                (sparse if len(cells & current[2]) == 1 else saturated).add(tile)
        assert len(sparse) == len(saturated) <= 1
        first, second = bool(sparse & union), bool(saturated & union)
        outward += first and not second
        inward += second and not first
        duplicate_sparse += len(sparse & crossing_tiles)
        duplicate_saturated += len(saturated & crossing_tiles)
    crossing_deficit = sum(2-len(vertices_of({tile}) & current[2]) for tile in crossing_tiles
                           if not vertices_of({tile}) & endpoints)
    crossing_loss = crossing_deficit+duplicate_sparse-duplicate_saturated
    assert crossing_loss <= 2*len(crossing_tiles)
    payment = sum(2-len(vertices_of({tile}) & current[2]) for tile in union
                  if not vertices_of({tile}) & endpoints)
    single_payment = sum(2-len(vertices_of({tile}) & current[2]) for tile in union
                         if multiplicities[tile] == 1 and not vertices_of({tile}) & endpoints)
    individual_payment = sum(record['physical_payment'] for record in records)
    weighted_comb_flux = sum(record['comb_flux'] for record in records)
    assert 2*payment == individual_payment+single_payment
    shifted = sum(record['shifted_payment'] for record in records)
    phase_gain = sum(record['perpendicular_gain'] for record in records)
    assert payment == 2*len(sources)+inward-outward-crossing_loss+shifted+phase_gain
    receiver_tiles = {(row//2, column//2) for row, column in endpoints}
    all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
    remainder = sum(2-len(vertices_of({tile}) & current[2]) for tile in all_tiles-union-receiver_tiles)
    deficit = checked['area']//2-checked['objective']
    assert deficit == len(sources)+inward-outward-crossing_loss+shifted+phase_gain+remainder
    assert 2*deficit == weighted_comb_flux+phase_gain+shifted+single_payment+2*remainder
    if weighted_comb_flux >= 0:
        assert deficit >= 0
    if not combs:
        assert weighted_comb_flux == 0 and payment >= len(sources)
    assert deficit >= len(sources)+inward-outward-2*len(crossing_tiles)
    return dict(sources=len(sources), combs=len(combs), strips=len(strips), crossing_tiles=len(crossing_tiles),
                outward=outward, inward=inward, duplicate_sparse=duplicate_sparse,
                duplicate_saturated=duplicate_saturated, crossing_deficit=crossing_deficit,
                effective_crossing_loss=crossing_loss, physical_union_payment=payment,
                individual_strip_payment=individual_payment, single_covered_payment=single_payment,
                weighted_comb_flux=weighted_comb_flux,
                shifted_payment=shifted, perpendicular_phase_gain=phase_gain,
                half_area_deficit=deficit, outside_remainder=remainder, strips_data=records)


def crossing_family(width=30, filled=False):
    assert width >= 22 and width % 2 == 0
    sources = [source_with_chamber(width, 6), move_source(source_with_chamber(14, 4),
               lambda point: (point[1]+4, point[0]+4))]
    current = assemble(28, width+10, sources)
    if filled:
        additions = {(9, 16), (9, 17), (11, 17), (12, 16), (13, 16), (14, 17), (15, 17),
                     (16, 5), (16, 8), (16, 11), (16, 14), (16, 16), (17, 9), (17, 10),
                     (17, 12), (17, 13), (17, 15), (18, 16), (18, 17)}
        additions.update((row, column) for row in (16, 17) for column in range(18, width+1, 2))
        current = *current[:2], current[2] | additions, current[3]
    return current, sources


def symmetries(current, sources):
    for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
        def move(point):
            row, column = point
            row = current[0]-1-row if vertical else row
            column = current[1]-1-column if horizontal else column
            return (column, row) if transpose else (row, column)
        inspect((*shape, selected, matching), [move_source(source, move) for source in sources])
    return 8


def many_crossings(count):
    sources = [source_with_chamber(4*count+22, 2*count+2)]
    sources.extend(move_source(source_with_chamber(8*(count-index)+6, 2),
                   lambda point, index=index: (point[1]+4+4*index, point[0]+4+4*index))
                   for index in range(count))
    return assemble(8*count+20, 4*count+32, sources), sources


def crossing_grid(horizontal_count, vertical_count):
    width = 8*horizontal_count+12*vertical_count+8
    sources = [move_source(source_with_chamber(width-8*index, 4*horizontal_count+2),
                           lambda point, index=index: (point[0]+4*index, point[1]+4*index))
               for index in range(horizontal_count)]
    sources.extend(move_source(source_with_chamber(8*horizontal_count+6, 2),
                   lambda point, index=index: (point[1]+4*horizontal_count+2,
                                               point[0]+4*horizontal_count+4+12*index))
                   for index in range(vertical_count))
    return assemble(12*horizontal_count+18, width+10, sources), sources


def controls():
    records, images = [], 0
    for width in (*range(22, 63, 2), 100, 200):
        current, sources = crossing_family(width, filled=True)
        record = inspect(current, sources)
        assert (record['physical_union_payment'], record['individual_strip_payment'],
                record['crossing_deficit'], record['shifted_payment'], record['perpendicular_phase_gain']) == (3, 4, 1, 0, 0)
        assert len(current[2]) == width+55 and len(current[3]) == width+36
        records.append(dict(kind='explicit_all_width_obstacle', width=width, result=record))
        if width in (22, 30, 100):
            images += symmetries(current, sources)
    for count in (1, 2, 3, 5, 8, 12):
        current, sources = many_crossings(count)
        current = fill_greedily(current, sources, count)
        record = inspect(current, sources)
        assert record['sources'] == count+1 and record['crossing_tiles'] == count
        records.append(dict(kind='arbitrarily_many_crossings', count=count, result=record))
        if count in (2, 5):
            images += symmetries(current, sources)
    for count in (1, 2, 4, 8):
        sources, selected, matching = [], set(), []
        for index in range(count):
            current, pair = crossing_family(22, filled=True)
            moved = [move_source(source, lambda point, index=index: (point[0], point[1]+36*index))
                     for source in pair]
            sources.extend(moved)
            selected.update((row, column+36*index) for row, column in current[2])
            matching.extend(tuple((row, column+36*index) for row, column in edge) for edge in current[3])
        record = inspect((28, 36*count, selected, matching), sources)
        assert record['sources'] == 2*count and record['crossing_tiles'] == count
        assert record['physical_union_payment'] == 3*count
        assert record['effective_crossing_loss'] == count
        records.append(dict(kind='paired_crossing_compensation', count=count, result=record))
    for horizontal_count, vertical_count in itertools.product((1, 2, 3, 5), repeat=2):
        current, sources = crossing_grid(horizontal_count, vertical_count)
        current = fill_greedily(current, sources, 100*horizontal_count+vertical_count)
        record = inspect(current, sources)
        assert record['sources'] == horizontal_count+vertical_count
        assert record['crossing_tiles'] == horizontal_count*vertical_count
        assert record['weighted_comb_flux'] == 0 and record['combs'] == 0
        assert record['physical_union_payment'] >= len(sources)
        records.append(dict(kind='dense_source_only_crossing_grid', horizontal=horizontal_count,
                            vertical=vertical_count, result=record))
        if (horizontal_count, vertical_count) in ((2, 3), (5, 5)):
            images += symmetries(current, sources)
    for start, finish, phase in itertools.product((11, 12), (16, 17), (-1, 1)):
        if (finish-start+1) % 2:
            continue
        current, sources = crossing_family()
        selected, matching = set(current[2]), list(current[3])
        selected.update({(start-1, 16), (finish+1, 16)})
        selected.update((row, 16+phase*(1 if (row-start) % 2 else -1)) for row in range(start, finish+1))
        matching.extend(((row, 16), (row+1, 16)) for row in range(start, finish, 2))
        current = *current[:2], selected, matching
        for seed in range(3):
            filled = fill_greedily(current, sources, seed)
            records.append(dict(kind='crossing_comb', start=start, finish=finish, phase=phase,
                                seed=seed, result=inspect(filled, sources)))
    for width, depth, vertical, across, reverse in itertools.product((8, 10, 14), (1, 2, 4),
                                                                   range(0, 17, 4), range(0, 21, 4), (False, True)):
        source = source_with_chamber(width, depth)
        move = lambda point: (point[1]+vertical, (25-point[0] if reverse else point[0])+across)
        sources = [source_with_chamber(46, 8), move_source(source, move)]
        current = assemble(42, 58, sources)
        if not feasible(current) or not all(source['endpoints'] in endpoint_components(current) for source in sources):
            continue
        current = fill_greedily(current, sources, width+depth+vertical+across+reverse)
        records.append(dict(kind='placement_control', width=width, depth=depth, vertical=vertical,
                            across=across, reverse=reverse, result=inspect(current, sources)))
    current, sources = crossing_family(38)
    current = add_parallel(current, 16, 17, 4, -1)
    records.append(dict(kind='horizontal_crossing_end', result=inspect(fill_greedily(current, sources, 7), sources)))
    witness, sources = crossing_family(22, filled=True)
    contact_types = Counter(contact['chamber_rows'] for record in records
                            for strip in record['result']['strips_data'] for contact in strip['perpendicular_contacts'])
    assert set(contact_types) == {1, 2}
    assert any(record['result']['duplicate_sparse'] for record in records)
    assert any(record['result']['duplicate_saturated'] for record in records)
    return dict(status='ALL_CHECKS_PASSED', cases=len(records), symmetry_images=images,
                source_only_cases=sum(record['result']['combs'] == 0 for record in records),
                maximum_crossings=max(record['result']['crossing_tiles'] for record in records),
                perpendicular_contact_types=dict(contact_types), records=records,
                witness=dict(shape=witness[:2], selected=sorted(witness[2]), matching=witness[3],
                             result=inspect(witness, sources)),
                scope='Finite controls for the general written crossing-loss and directional-averaging theorems, arbitrary-orientation source-only compensation, and explicit all-width obstacle. Dense crossing grids test the removal of X restrictions. No enumeration replaces proof; no universal grid or complete Lean claim.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('records', 'witness')}))


if __name__ == '__main__':
    main()
