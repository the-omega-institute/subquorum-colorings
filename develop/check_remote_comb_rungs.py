"""Physical controls for distant, original-tile negative-flux compensation."""

import argparse
import itertools
import json
from pathlib import Path

from check_adaptive_strip_compensation import certificate
from check_component_receivers import endpoint_components, vertices_of
from check_frozen_end_locality_obstacle import build as locality_obstacle
from check_mixed_source_contacts import source_with_chamber
from check_orthogonal_source_mouths import inspect, strips_of
from check_owned_donors import endpoint_data
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def remote_family(depth, left_length, right_length):
    source = source_with_chamber(10, depth)
    tip = 2*depth+4
    selected, matching = set(source['selected']), list(source['matching'])
    for column, length, direction in ((5, left_length, 1), (10, right_length, -1)):
        start, finish = tip+1, tip+2*length
        selected.update({(start-1, column), (finish+1, column)})
        selected.update((row, column+direction*(1 if row % 2 else -1))
                        for row in range(start, finish+1))
        matching.extend(((row, column), (row+1, column)) for row in range(start, finish, 2))
    end = tip+2*min(left_length, right_length)
    selected.update({(tip, 7), (tip, 8), (end, 7), (end, 8)})
    rows = max(2*depth+8, tip+2*max(left_length, right_length)+2)
    return (rows, 18, selected, matching), [source], (end, 5, 10)


def rung_record(current, sources, row, left, right):
    physical = inspect(current, sources)
    assert row % 2 == 0 and left % 2 == 1 and right % 2 == 0 and right-left >= 5
    endpoints = endpoint_data(current)[0]
    cells = set(itertools.product((row, row+1), range(left+1, right)))
    assert not cells & endpoints
    tiles = {(upper//2, column//2) for upper, column in cells}
    assert vertices_of(tiles) == cells
    mouths = set().union(*(strip['tiles'] for strip in strips_of(sources)))
    assert not mouths & tiles
    extreme = {(upper, column) for upper in (row, row+1) for column in (left+1, right-1)}
    boundary_selected = len(extreme & current[2])
    assert boundary_selected in (0, 1)
    shifted = [{(upper, column) for upper in (row, row+1) for column in (start, start+1)}
               for start in range(left+2, right-1, 2)]
    shifted_payment = sum(2-len(square & current[2]) for square in shifted)
    assert all(len(square & current[2]) <= 2 for square in shifted)
    payment = sum(2-len(vertices_of({tile}) & current[2]) for tile in tiles)
    assert payment == 2-boundary_selected+shifted_payment >= 2-boundary_selected
    assert physical['outside_remainder'] >= payment
    assert physical['weighted_comb_flux'] == -2
    assert 2*physical['half_area_deficit'] >= -2+2*payment
    assert physical['half_area_deficit'] >= 0
    return dict(shape=current[:2], rung_row=row, rung_columns=(left+1, right-1),
                original_payment=payment, boundary_selected=boundary_selected,
                shifted_payment=shifted_payment, physical=physical)


def controls():
    records = []
    witness = None
    for depth, left_length, right_length in itertools.product((1, 2, 5), (1, 2, 5, 12), (1, 2, 5, 12)):
        current, sources, rung = remote_family(depth, left_length, right_length)
        record = rung_record(current, sources, *rung)
        expected = 2 if left_length == right_length else 1
        assert record['original_payment'] == expected
        assert record['physical']['physical_union_payment'] == 0
        assert record['physical']['shifted_payment'] == 0
        assert record['physical']['perpendicular_phase_gain'] == 0
        assert certificate(current, sources)['independent_weight'] == 0
        records.append(dict(kind='unequal_remote_family', depth=depth,
                            left_length=left_length, right_length=right_length, result=record))
        if (depth, left_length, right_length) == (1, 2, 5):
            witness = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3], result=record)
    for radius in (1, 2, 4, 8, 16, 40):
        original, mouth, _, _ = locality_obstacle(radius)
        shape, selected, matching = transformed(*original, False, True, False)
        source = source_with_chamber(4*radius+14, 2*radius+3)
        move = lambda point: (original[0]-1-point[0], point[1])
        sources = [{key: [tuple(move(point) for point in edge) for edge in value]
                    if key == 'matching' else {move(point) for point in value}
                    for key, value in source.items()}]
        current = *shape, selected, matching
        combs = [component for component in endpoint_components(current)
                 if len({column for row, column in component}) == 1]
        assert len(combs) == 2
        columns = sorted(next(iter(component))[1] for component in combs)
        row = min(max(point[0] for point in component) for component in combs)
        record = rung_record(current, sources, row, *columns)
        assert record['boundary_selected'] == 0
        assert record['original_payment'] >= 2
        assert certificate(current, sources)['independent_weight'] == 0
        records.append(dict(kind='existing_all_radius_obstacle_paid_remotely', radius=radius, result=record))
    return dict(status='ALL_CHECKS_PASSED', physical_cases=len(records), records=records,
                unequal_length_cases=sum(record.get('left_length') != record.get('right_length')
                                        for record in records if 'left_length' in record),
                old_locality_obstacles_paid=6, smallest_unequal_witness=witness,
                scope='Controls of a general written remote-rung proof and exact physical strip '
                      'partition. Original mouths have no payment; distant endpoint-free strips '
                      'provide exterior deficit. No partial receiver/export is a donor. Existing '
                      'all-radius obstacles have W=0 but are paid by distant aligned rungs. '
                      'No general existence of endpoint-free rungs or universal grid bound is claimed.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in
                      ('status', 'physical_cases', 'unequal_length_cases', 'old_locality_obstacles_paid')}))


if __name__ == '__main__':
    main()
