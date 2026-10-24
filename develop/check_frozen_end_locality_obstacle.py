"""Explicit all-radius frozen obstruction to end-local no-P donor allocation."""

import argparse
import json
from pathlib import Path

from check_bent_cap_compensation import charge_twice
from check_comb_end_flux import flux_record
from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import graph_record, transformed
from check_transverse_comb_mouths import crossing_family


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def band_word(radius, level):
    prefix = radius+1
    if level < 0:
        return ['BTTB']*prefix+['BPTP', 'TBBT', 'BTTB', 'PBPT']+['TBBT']*prefix
    if level == 0:
        return ['BTBT']*prefix+['BPBT', 'TBBT', 'BTTB', 'PBTB']+['TBTB']*prefix
    if level == 1:
        return ['TBTB']*(prefix+2)+['BTTB']*(prefix+1)+['BBTT']
    return ['BTTB']*(2*prefix+3)+['BBTT']


def build(radius):
    assert radius >= 1
    width, depth, half_length = 4*radius+14, 2*radius+3, radius+2
    tip = 2*depth+2
    left, right = 2*radius+4, 2*radius+9
    current, mouth = crossing_family(width, depth, [left, right], [-1, 1],
                                     upper=2*half_length-1, lower=0)
    selected = set(current[2])
    endpoints = endpoint_data(current)[0]
    patch = set()
    for level in range(-radius, radius+1):
        words = band_word(radius, level)
        assert len(words) == 2*radius+6
        for index, word in enumerate(words):
            tile = ((tip+2)//2+level, 2+index)
            patch.add(tile)
            cells = [(2*tile[0]+row, 2*tile[1]+column)
                     for row in (0, 1) for column in (0, 1)]
            for point, label in zip(cells, word):
                assert (point in endpoints) == (label == 'P')
                if point in selected:
                    assert label == 'T'
                if label == 'T':
                    selected.add(point)
    result = current[0]+2*radius, current[1], selected, current[3]
    end_tiles = {((tip+2)//2, (left+3)//2), ((tip+2)//2, (right+3)//2)}
    return result, mouth, patch, end_tiles


def tile_distance(tile, ends):
    return min(abs(tile[0]-end[0])+abs(tile[1]-end[1]) for end in ends)


def inspect(current, mouth, patch, ends, radius):
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0, 0, 2]
    tiles = {(row, column) for row in range(current[0]//2) for column in range(current[1]//2)}
    receiver_tiles = {(row//2, column//2) for row, column in endpoints}
    no_endpoint = tiles-receiver_tiles
    nearby = {tile for tile in tiles if tile_distance(tile, ends) <= radius}
    assert nearby <= patch
    assert all(len(vertices_of({tile}) & current[2]) == 2 for tile in patch & no_endpoint)
    deficits = {tile: 2-len(vertices_of({tile}) & current[2]) for tile in no_endpoint}
    assert all(deficits[tile] == 0 for tile in nearby & no_endpoint)
    nearest_donor = min(tile_distance(tile, ends) for tile, deficit in deficits.items() if deficit)
    assert nearest_donor == radius+1
    for end in ends:
        assert min(tile_distance(tile, {end}) for tile, deficit in deficits.items() if deficit) == radius+1
    mouth_counts = flux_record(current, mouth)
    assert (mouth_counts['sparse_ends'], mouth_counts['saturated_ends'],
            mouth_counts['no_endpoint_deficit'], mouth_counts['shifted_no_endpoint_deficit']) == (2, 0, 0, 0)
    graph, _ = graph_record(*current)
    combs = [component for component in endpoint_components(current)
             if len({column for row, column in component}) == 1 or
                len({row for row, column in component}) == 1]
    assert len(combs) == 2
    exports = []
    for component in combs:
        whole = {(row//2, column//2) for row, column in component}
        inside = sum(charge_twice(graph, current[1], tile) for tile in whole & patch)
        outside = sum(charge_twice(graph, current[1], tile) for tile in whole-patch)
        assert (inside, outside) == (-1, 1)
        positive = [tile for tile in whole if charge_twice(graph, current[1], tile) > 0]
        assert len(positive) == 1 and tile_distance(positive[0], ends) == radius+1
        exports.append(dict(whole_charge_twice=0, patch_charge_twice=inside,
                            exterior_charge_twice=outside, positive_charge_tile=positive[0],
                            positive_charge_distance=radius+1))
    return dict(radius=radius, shape=current[:2], objective=checked['objective'],
                patch_tiles=len(patch), patch_no_endpoint_tiles=len(patch & no_endpoint),
                nearby_no_endpoint_tiles=len(nearby & no_endpoint), nearest_no_endpoint_donor=nearest_donor,
                mouth=mouth_counts, comb_exports=exports)


def controls():
    records, images = [], 0
    smallest = None
    for radius in (*range(1, 13), 16, 24, 40):
        current, mouth, patch, ends = build(radius)
        record = inspect(current, mouth, patch, ends, radius)
        assert len(current[2]) == 8*radius*radius+32*radius+36
        assert len(current[3]) == 10*radius+25
        assert record['objective'] == 8*radius*radius+42*radius+61
        assert record['patch_no_endpoint_tiles'] == 4*radius*radius+12*radius+4
        assert current[0]*current[1]//2-record['objective'] == 4*radius*radius+52*radius+93
        records.append(record)
        if radius == 1:
            smallest = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                            patch=sorted(patch), sparse_end_tiles=sorted(ends))
        if radius in (1, 4, 12):
            for transpose in (False, True):
                for vertical in (False, True):
                    for horizontal in (False, True):
                        shape, selected, matching = transformed(*current, transpose, vertical, horizontal)
                        _, moved_mouth, _ = transformed(*current[:2], mouth, [], transpose, vertical, horizontal)
                        _, patch_cells, _ = transformed(*current[:2], vertices_of(patch), [], transpose, vertical, horizontal)
                        _, end_cells, _ = transformed(*current[:2], vertices_of(ends), [], transpose, vertical, horizontal)
                        moved_patch = {(row//2, column//2) for row, column in patch_cells}
                        moved_ends = {(row//2, column//2) for row, column in end_cells}
                        inspect((*shape, selected, matching), moved_mouth, moved_patch, moved_ends, radius)
                        images += 1
    return dict(status='ALL_CHECKS_PASSED', explicit_family_cases=len(records), symmetry_images=images,
        family=records, smallest=smallest,
        refuted_rule='Assign a positive original no-P-tile deficit within some fixed tile radius '
                     'of each unmatched sparse end, even for complete frozen one-sided contacts.',
        universal_grid_target_refuted=False,
        scope='Explicit formulas and a separate all-radius proof establish the obstruction. '
              'Controls independently check feasibility, complete freezing, charges, exact counts, '
              'radius coverage and matching-charge separation. No solver, enumeration-based '
              'general proof, or exclusion of distant/source-local compensation is asserted.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('family', 'smallest')}))


if __name__ == '__main__':
    main()
