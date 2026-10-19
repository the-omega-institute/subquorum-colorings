"""Physical phase accounting and sharp cavity controls with escaping sources."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_coalesced_mouths import assemble, move_source
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_mixed_cavity_sources import flank_record, occupied_perpendicular_rung, packed_sources, sharpen_flanks
from check_mixed_source_contacts import source_with_chamber
from check_orthogonal_source_mouths import feasible, square_data
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_remote_comb_rungs import remote_family
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(current, sources, cavity):
    if len({row for row, column in sources[0]['chamber']}) != 2:
        shape, selected, matching = transformed(*current, True, False, False)
        return inspect((*shape, selected, matching),
                       [move_source(source, lambda point: (point[1], point[0])) for source in sources],
                       {(column, row) for row, column in cavity})
    assert feasible(current)
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    components = endpoint_components(current)
    assert all(source['endpoints'] in components for source in sources)
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0]*(
        len(components)-len(sources))+[2]*len(sources)
    assert not sources[0]['endpoints'] & cavity
    rows = sorted({row for row, column in cavity})
    columns = sorted({column for row, column in cavity})
    boundary = set(itertools.product(rows, (columns[0], columns[-1])))
    assert not boundary & endpoints
    assert len(boundary & current[2]) == len(rows)-2
    tiles = {(row//2, column//2) for row, column in cavity}
    assert vertices_of(tiles) == cavity
    owner = {point: index for index, component in enumerate(components) for point in component}
    physical, shifted, band_gains = [], [], Counter()
    for upper in rows[::2]:
        first = [square_data(vertices_of({(upper//2, left//2)}), current, endpoints, owner)
                 for left in columns[::2]]
        second = [square_data(set(itertools.product((upper, upper+1), (left, left+1))),
                              current, endpoints, owner) for left in columns[1:-1:2]]
        physical.extend(first)
        shifted.extend(second)
        for index in range(len(components)):
            difference = sum(record['excess_twice'] for record in first if record['owner'] == index)
            difference -= sum(record['excess_twice'] for record in second if record['owner'] == index)
            assert difference % 2 == 0
            band_gains[index, upper] = difference//2
    source_records, flux, phase = [], 0, 0
    source_components = [source['endpoints'] for source in sources]
    for index, component in enumerate(components):
        gain = sum(band_gains[index, upper] for upper in rows[::2])
        if component in source_components:
            source = sources[source_components.index(component)]
            if source is sources[0]:
                assert gain == 0
                continue
            parallel = len({row for row, column in source['chamber']}) == 2
            tip_tiles = {(row//2, column//2) for row, column in source['tips']}
            tip_count = len(tip_tiles & tiles)
            if parallel:
                assert gain == tip_count
            else:
                chamber_rows = sorted({row for row, column in source['chamber']})
                chamber_columns = sorted({column for row, column in source['chamber']})
                rightward = min(column for row, column in source['tips']) > chamber_columns[-1]
                outer = chamber_columns[0]-1 if rightward else chamber_columns[-1]+1
                inner = chamber_columns[-1]+1 if rightward else chamber_columns[0]-1
                for upper in rows[::2]:
                    band = set(itertools.product((upper, upper+1), columns))
                    if not band & component:
                        assert band_gains[index, upper] == 0
                        continue
                    intersection = set(chamber_rows) & {upper, upper+1}
                    if len(intersection) == 2:
                        outer_count = len(set(itertools.product((upper, upper+1), (outer,))) & current[2])
                        inner_count = len(set(itertools.product((upper, upper+1), (inner,))) & current[2])
                        assert outer_count <= 1 and inner_count <= 1
                        assert band_gains[index, upper] == 2-outer_count-inner_count
                    else:
                        assert len(intersection) == 1
                        end_row = next(iter(intersection))
                        assert end_row in (chamber_rows[0], chamber_rows[-1])
                        optional = int((end_row, outer) in current[2])
                        assert band_gains[index, upper] == 1-optional
                    assert band_gains[index, upper] >= 0
            contained = component <= cavity
            if contained:
                assert gain >= 2
            phase += gain
            source_records.append(dict(parallel=parallel, contained=contained,
                                       touches=bool(component & cavity), tip_count=tip_count,
                                       phase_gain=gain,
                                       band_gains=[band_gains[index, upper] for upper in rows[::2]]))
        else:
            assert len({row for row, column in component}) == 1 or len({column for row, column in component}) == 1
            membership = 0
            for tile in {(row//2, column//2) for row, column in component} & tiles:
                cells = vertices_of({tile})
                if len(cells & component) == 1:
                    membership += 1 if len(cells & current[2]) == 2 else -1
            assert gain == membership
            flux += membership
    payment = sum(2-record['selected'] for record in physical if not record['endpoints'])
    shifted_payment = sum(2-record['selected'] for record in shifted if not record['endpoints'])
    assert payment == 2+phase+flux+shifted_payment
    deficit = checked['area']//2-checked['objective']
    assert deficit >= payment-len(sources)
    positive_donors = [dict(tile=tile, deficit=2-len(vertices_of({tile}) & current[2]))
                      for tile in sorted(tiles) if not vertices_of({tile}) & endpoints
                      and len(vertices_of({tile}) & current[2]) < 2]
    return dict(sources=len(sources), partial_sources=sum(record['touches'] and not record['contained']
                for record in source_records), source_records=source_records,
                source_phase=phase, comb_flux=flux, physical_payment=payment,
                shifted_payment=shifted_payment, positive_donor_count=len(positive_donors),
                positive_donors=positive_donors if len(positive_donors) <= 16 else None,
                half_area_deficit=deficit)


def escaping_source_family(count, width, depth, foreign_width):
    assert count >= 1 and width >= 32*count and width % 2 == 0 and depth >= 3
    assert foreign_width >= 2*depth+2 and foreign_width % 2 == 0
    sources = [source_with_chamber(width, depth)]
    sources.extend(move_source(source_with_chamber(foreign_width, 1),
                   lambda point, index=index: (point[1]+4, point[0]+12+32*index))
                   for index in range(count))
    current = sharpen_flanks(assemble(foreign_width+12, width+8, sources), sources)
    tip = 2*depth+4
    selected = set(current[2])
    for row in range(4, tip+2):
        if row == tip:
            chosen = {5, *range(8, width, 2)}
        elif row == tip+1:
            chosen = {5, *range(7, width, 2), width}
        elif row % 2 == 0:
            chosen = {5, *range(8, width+1, 2)}
        else:
            chosen = {4, 6, 7, *range(9, width+2, 2)}
        for index in range(count):
            chamber = 14+32*index
            if row == 7:
                chosen -= {chamber+1, chamber+3}
            elif row >= 8 and row % 2 == 0:
                chosen -= {chamber, chamber+2, chamber+4}
                chosen.add(chamber+3)
            elif row >= 9:
                chosen -= {chamber+1, chamber+3}
                chosen.update({chamber+2, chamber+4})
        selected.update((row, column) for column in chosen)
    current = *current[:2], selected, current[3]
    cavity = set(itertools.product(range(4, tip+2), range(4, width+2)))
    return current, sources, cavity


def parallel_contact(kind, width, depth):
    root = source_with_chamber(width, depth)
    if kind == 'chamber_inside_tips_outside':
        other = move_source(source_with_chamber(16, depth+3),
                            lambda point: (point[0]+4, point[1]+12))
    else:
        other_width = width if kind == 'one_arm_inside' else 16
        other_depth = depth+3
        axis = 4*depth+11
        other = move_source(source_with_chamber(other_width, other_depth),
                            lambda point: (axis-point[0], point[1]+12))
    rows = max(row for source in (root, other) for row, column in source['selected'])+3
    columns = max(column for source in (root, other) for row, column in source['selected'])+3
    current = assemble(rows+rows % 2, columns+columns % 2, [root, other])
    cavity = set(itertools.product(range(4, 2*depth+6), range(4, width+2)))
    return current, [root, other], cavity


def controls():
    records, images, witness = [], 0, None
    for count, depth, extra_width, extra_length in itertools.product(
            (1, 2, 3, 5), (3, 5, 12), (0, 2), (0, 4)):
        width = 32*count+extra_width
        foreign_width = 2*depth+2+extra_length
        current, sources, cavity = escaping_source_family(count, width, depth, foreign_width)
        result = inspect(current, sources, cavity)
        assert result['partial_sources'] == count and result['source_phase'] == 0
        assert result['physical_payment'] == 2 and result['shifted_payment'] == result['comb_flux'] == 0
        assert result['positive_donors'] == [dict(tile=(depth+2, 3), deficit=1),
                                             dict(tile=(depth+2, width//2), deficit=1)]
        assert all(flank_record(source, current[2])['phase_gain'] == 2 for source in sources[1:])
        records.append(dict(kind='arbitrarily_many_zero_phase_escaping_sources', count=count,
                            width=width, depth=depth, foreign_width=foreign_width, result=result))
        if (count, depth, extra_width, extra_length) == (1, 3, 0, 0):
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3], result=result)
            for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
                def move(point):
                    row, column = point
                    row = current[0]-1-row if vertical else row
                    column = current[1]-1-column if horizontal else column
                    return (column, row) if transpose else (row, column)
                image = inspect((*shape, selected, matching),
                                [move_source(source, move) for source in sources],
                                {move(point) for point in cavity})
                assert image['physical_payment'] == 2 and image['source_phase'] == 0
                images += 1
    for kind, width, depth in itertools.product(
            ('chamber_inside_tips_outside', 'two_tips_inside', 'one_arm_inside'), (32, 48, 80), (3, 5, 12)):
        current, sources, cavity = parallel_contact(kind, width, depth)
        result = inspect(current, sources, cavity)
        expected = {'chamber_inside_tips_outside': 0, 'two_tips_inside': 2, 'one_arm_inside': 1}[kind]
        assert result['source_phase'] == expected and result['partial_sources'] == 1
        records.append(dict(kind=kind, width=width, depth=depth, result=result))
    for orientations in ((False,), (True,), (False, True), (True, False, True)):
        for sharp in (False, True):
            current, sources, cavity = packed_sources(orientations, sharp)
            records.append(dict(kind='complete_mixed_sources', result=inspect(current, sources, cavity)))
    current, sources, cavity = occupied_perpendicular_rung(32, 7, True)
    records.append(dict(kind='complete_source_and_combs', result=inspect(current, sources, cavity)))
    for depth, lengths in itertools.product((1, 3, 7), ((1, 1), (2, 5))):
        current, sources, unused = remote_family(depth, *lengths)
        cavity = set(itertools.product(range(4, 2*depth+6), range(4, 12)))
        records.append(dict(kind='escaping_combs', result=inspect(current, sources, cavity)))
    return dict(status='ALL_CHECKS_PASSED', physical_cases=len(records), symmetry_images=images,
                records=records, sharp_partial_source_witness=witness,
                refuted_rule='D_C >= 2 times the number of root-plus-touching sources',
                global_grid_target_refuted=False,
                scope='Physical controls for the general written nonnegative partial-source phase '
                      'lemma, exact open-source cavity ledger and all-count sharp D_C=2 family. '
                      'Finite checks do not prove arbitrary parameters or general cavity existence.')


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
