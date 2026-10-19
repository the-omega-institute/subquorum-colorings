"""Physical controls for whole-channel compensation with occupied terminal bands."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_closed_source_cavities import add_horizontal, add_vertical
from check_coalesced_mouths import assemble, move_source
from check_component_receivers import endpoint_components, vertices_of
from check_mixed_cavity_sources import sharpen_flanks
from check_mixed_source_contacts import source_with_chamber
from check_open_source_cavities import region_record
from check_orthogonal_source_mouths import inspect, strips_of
from check_owned_donors import endpoint_data
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def channel_record(current, sources, walls):
    left, right, left_start, right_start, left_end, right_end = walls
    assert left % 2 == 1 and right % 2 == 0 and right-left >= 5
    assert left_start % 2 == right_start % 2 == 1
    assert left_end % 2 == right_end % 2 == 0
    assert max(left_start, right_start) <= min(left_end, right_end)
    endpoints = endpoint_data(current)[0]
    components = endpoint_components(current)
    for column, start, end, direction in ((left, left_start, left_end, 1),
                                         (right, right_start, right_end, -1)):
        assert {(row, column) for row in range(start, end+1)} in components
        supports = {(start-1, column), (end+1, column)}
        supports.update((row, column+direction*(1 if row % 2 else -1))
                        for row in range(start, end+1))
        assert supports <= current[2]
    first, last = max(left_start, right_start)-1, min(left_end, right_end)
    unequal = int(left_end != right_end)
    cells = set(itertools.product(range(first, last+2), range(left+1, right)))
    record = region_record(current, sources, cells, 2-unequal)
    for column, end in ((left+1, left_end), (right-1, right_end)):
        assert not {(row, column) for row in range(first, last+2)} & endpoints
        assert {(row, column) for row in range(first+1, last, 2)} <= current[2]
        assert not {(row, column) for row in range(first, last+1, 2)} & current[2]
        assert ((last+1, column) in current[2]) == (end > last)
    return cells, dict(record, rows=(first, last+1), columns=(left+1, right-1),
                       unequal=unequal, base_payment=2-unequal,
                       terminal_endpoint_count=len(endpoints & set(itertools.product(
                           (last, last+1), range(left+1, right)))))


def residual_record(current, sources, channels):
    endpoints = endpoint_data(current)[0]
    mouths = Counter(tile for strip in strips_of(sources) for tile in strip['tiles'])
    usage = Counter()
    total = 0
    lower_payment = 0
    for cells, record in channels:
        weight = record.get('certificate_weight', 1+record['unequal'])
        assert weight >= 0
        usage.update({tile: weight for tile in {(row//2, column//2) for row, column in cells}})
        total += weight*record['physical_payment']
        lower_payment += weight*(record['base_payment']+record['source_phase']+record['comb_flux'])
    positive = {tile: 2-len(vertices_of({tile}) & current[2])
                for tile in itertools.product(range(current[0]//2), range(current[1]//2))
                if not vertices_of({tile}) & endpoints
                and len(vertices_of({tile}) & current[2]) < 2}
    violations = [tile for tile in positive if usage[tile] > 2-mouths[tile]]
    ledger = inspect(current, sources)
    residual = sum((2-mouths[tile])*payment for tile, payment in positive.items())
    assert residual == ledger['single_covered_payment']+2*ledger['outside_remainder']
    if not violations:
        assert lower_payment <= total <= residual
        assert 2*ledger['half_area_deficit'] >= ledger['weighted_comb_flux']+lower_payment
        if ledger['weighted_comb_flux']+lower_payment >= -1:
            assert ledger['half_area_deficit'] >= 0
    return dict(capacity_valid=not violations, violation_count=len(violations),
                channel_count=len(channels), weighted_payment=total,
                lower_payment=lower_payment,
                doubled_lower_bound=ledger['weighted_comb_flux']+lower_payment,
                residual_payment=residual, original_ledger=ledger)


def occupied_family(width, depth, left_length, right_length, blocker='comb'):
    assert width >= 32 and width % 2 == 0 and depth >= 1
    assert min(left_length, right_length) >= (6 if blocker == 'source' else 2)
    root = source_with_chamber(width, depth)
    tip = 2*depth+4
    sources = [root]
    if blocker == 'source':
        sources.append(move_source(source_with_chamber(8, 1),
                                    lambda point: (point[1]+tip+2, point[0]+12)))
    rows = tip+2*max(left_length, right_length)+4
    current = assemble(rows, width+8, sources)
    selected, matching = set(current[2]), list(current[3])
    add_vertical(selected, matching, 9, tip+1, tip+2*left_length, 1)
    add_vertical(selected, matching, 22, tip+1, tip+2*right_length, -1)
    last = tip+2*min(left_length, right_length)
    if blocker == 'comb':
        add_horizontal(selected, matching, last, 14, 17)
    selected.update((row, column) for row in (tip, tip+1)
                    for column in (5, 7, *range(24, width+1, 2)))
    selected.update((tip, column) for column in (9, 11, 14, 17, 20, 22))
    selected.update((tip+1, column) for column in (10, 12, 13, 15, 16, 18, 19, 21))
    current = rows, width+8, selected, matching
    if blocker == 'source':
        current = sharpen_flanks(current, sources)
    walls = 9, 22, tip+1, tip+1, tip+2*left_length, tip+2*right_length
    return current, sources, walls


def bare_channel(left_start, right_start, left_end, right_end, escaping=0, incoming=False):
    selected, matching = set(), []
    add_vertical(selected, matching, 9, left_start, left_end, 1)
    add_vertical(selected, matching, 30, right_start, right_end, -1)
    first, last = max(left_start, right_start)-1, min(left_end, right_end)
    for index in range(escaping):
        start, end = (first-3, first+2) if incoming else (first+3, last+4)
        add_vertical(selected, matching, 14+4*index, start, end, -1)
    return (max(left_end, right_end)+8, 36, selected, matching), [], (
        9, 30, left_start, right_start, left_end, right_end)


def controls():
    records = []
    witness = None
    for width, depth, left_length, right_length in itertools.product(
            (32, 40, 64), (1, 3, 7), (2, 3, 6, 11), (2, 3, 6, 11)):
        current, sources, walls = occupied_family(width, depth, left_length, right_length)
        cells, record = channel_record(current, sources, walls)
        assert record['terminal_endpoint_count'] == 4
        assert record['source_phase'] == record['comb_flux'] == 0
        assert record['physical_payment'] == 10*min(left_length, right_length)-6-record['unequal']
        resources = residual_record(current, sources, [(cells, record)])
        assert resources['capacity_valid']
        ledger = resources['original_ledger']
        assert ledger['weighted_comb_flux'] == -2
        assert ledger['physical_union_payment'] == ledger['shifted_payment'] == 0
        assert ledger['single_covered_payment'] == ledger['perpendicular_phase_gain'] == 0
        if not record['unequal']:
            assert residual_record(current, sources, [(cells, record)]*2)['capacity_valid']
            assert not residual_record(current, sources, [(cells, record)]*3)['capacity_valid']
        else:
            assert not residual_record(current, sources, [(cells, record)]*2)['capacity_valid']
        records.append(dict(kind='zero_mouth_occupied_terminal_comb', width=width, depth=depth,
                            left_length=left_length, right_length=right_length,
                            channel=record, resources=resources))
        if (width, depth, left_length, right_length) == (32, 1, 2, 2):
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                           walls=walls, channel=record, resources=resources)
    for left_start, right_start, left_end, right_end in itertools.product(
            (5, 7, 9), (5, 7, 9), (12, 18), (12, 18)):
        current, sources, walls = bare_channel(left_start, right_start, left_end, right_end)
        _, record = channel_record(current, sources, walls)
        assert record['comb_flux'] == record['source_phase'] == 0
        records.append(dict(kind='different_start_heights', walls=walls, channel=record))
    for escaping, incoming in itertools.product((1, 2, 3), (False, True)):
        current, sources, walls = bare_channel(7, 9, 16, 18, escaping, incoming)
        _, record = channel_record(current, sources, walls)
        assert record['comb_flux'] == escaping*(1 if incoming else -1)
        records.append(dict(kind='signed_complete_comb_exits', escaping=escaping,
                            incoming=incoming, channel=record))
    for depth, left_length, right_length in itertools.product((1, 3), (6, 8), (6, 8)):
        current, sources, walls = occupied_family(32, depth, left_length, right_length, 'source')
        cells, record = channel_record(current, sources, walls)
        assert record['source_phase'] == 2 and record['comb_flux'] == 0
        if min(left_length, right_length) == 6:
            assert record['terminal_endpoint_count'] > 0
        baseline_resources = residual_record(current, sources, [(cells, record)])
        record = dict(record, certificate_weight=1)
        resources = residual_record(current, sources, [(cells, record)])
        assert resources['capacity_valid']
        assert baseline_resources['capacity_valid'] == (left_length == right_length)
        assert baseline_resources['violation_count'] == 3*record['unequal']
        assert resources['original_ledger']['weighted_comb_flux'] == -2
        assert resources['original_ledger']['single_covered_payment'] == 6
        assert resources['doubled_lower_bound'] == 2-record['unequal']
        assert resources['original_ledger']['half_area_deficit'] >= 1
        records.append(dict(kind='complete_perpendicular_source_inside_channel', depth=depth,
                            left_length=left_length, right_length=right_length,
                            channel=record, resources=resources, baseline_resources=baseline_resources))
    symmetry_images = 0
    current, sources, walls = occupied_family(32, 1, 2, 3)
    cells, record = channel_record(current, sources, walls)
    for transpose, vertical, horizontal in itertools.product((False, True), repeat=3):
        def move(point):
            row, column = point
            row = current[0]-1-row if vertical else row
            column = current[1]-1-column if horizontal else column
            return (column, row) if transpose else (row, column)
        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
        moved = region_record((*shape, selected, matching), [move_source(source, move) for source in sources],
                              {move(point) for point in cells}, record['base_payment'], not transpose)
        assert moved['physical_payment'] == record['physical_payment']
        assert moved['source_phase'] == record['source_phase']
        assert moved['comb_flux'] == record['comb_flux']
        symmetry_images += 1
    return dict(status='ALL_CHECKS_PASSED', physical_cases=len(records), symmetry_images=symmetry_images,
                records=records, smallest_occupied_witness=witness,
                scope='Physical checks of the general written whole-channel identity and residual '
                      'capacity theorem, including occupied terminal bands, unequal ends, different '
                      'starts, signed comb exits, complete perpendicular sources, symmetry and '
                      'rejected over-allocation. General geometry is proved in the note; existence '
                      'of enough channels and unrestricted grid equality remain open.')


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
