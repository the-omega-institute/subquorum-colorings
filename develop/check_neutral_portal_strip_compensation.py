"""Independent strip, first-stop and physical-capacity controls for neutral portals."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_component_receivers import vertices_of
from check_even_bridge_support_completion import endpoints_of, tiles_of
from check_native_guard_compensation import charge, force_matching
from check_neutral_pair_donor_saturation import neutral_pair
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


SIDES = ({0, 2}, {1, 3}, {0, 1}, {2, 3})


def collision_controls(totals):
    minima = {}
    for selection_mask, claim_mask in itertools.product(range(16), repeat=2):
        selected = {corner for corner in range(4) if selection_mask >> corner & 1}
        arrivals = {side for side in range(4) if claim_mask >> side & 1}
        if len(selected) > 2 or not arrivals or len(selected) == 2:
            continue
        if any(selected & SIDES[side] for side in arrivals):
            continue
        deficit = 2-len(selected)
        assert len(arrivals) <= 2*deficit
        if arrivals <= {0, 1} or arrivals <= {2, 3}:
            assert len(arrivals) <= deficit
        minima[claim_mask] = min(minima.get(claim_mask, 2), deficit)
        totals['local_stop_masks'] += 1
    assert len(minima) == 15
    assert minima[1 | 4] == 1 and minima[1 | 2] == 2 and minima[15] == 2
    for four_sides in (False, True):
        selected = {(2, 1), (3, 1), (1, 2), (1, 3)}
        if four_sides:
            selected |= {(2, 4), (3, 4), (4, 2), (4, 3)}
        else:
            selected.add((3, 3))
        direct_check(6, 6, selected, [])
        deficit = 2-len(selected & vertices_of({(1, 1)}))
        assert deficit == (2 if four_sides else 1)
        totals['feasible_transverse_collision_patches'] += 1
    return minima


def strip_controls(totals):
    records = []
    for length in range(1, 5):
        minima = {False: 2*length, True: 2*length}
        count = 0
        for interior in itertools.product(range(4), repeat=2*length-2):
            for last in (0, 1):
                columns = (0, *interior, last)
                selected = {(row, column) for column, mask in enumerate(columns)
                            for row in (0, 1) if mask >> row & 1}
                try:
                    direct_check(2, 2*length, selected, [])
                except AssertionError:
                    continue
                deficits = [2-len(selected & vertices_of({(0, index)})) for index in range(length)]
                assert min(deficits) >= 0 and sum(deficits) >= 1
                if last == 0:
                    assert sum(deficits) >= 2
                stop = next(index for index, deficit in enumerate(deficits) if deficit)
                assert not {(0, 2*stop), (1, 2*stop)} & selected
                minima[bool(last)] = min(minima[bool(last)], sum(deficits))
                count += 1
        assert minima == {False: 2, True: 1}
        records.append(dict(length=length, feasible_selections=count, sealed_minimum=2,
                            one_corner_minimum=1))
        totals['exhaustive_short_strip_models'] += count
    return records


def corridor(width, height):
    last = width//2+int(height == 4)
    return [(4, column) for column in range(3, last+1)]


def inspect(current, strip, totals, marker=None):
    direct_check(*current)
    endpoints = endpoints_of(current)
    assert not vertices_of(set(strip)) & endpoints
    deficits = [2-len(current[2] & vertices_of({tile})) for tile in strip]
    assert sum(deficits) >= 1 and min(deficits) >= 0
    stop_index = next(index for index, deficit in enumerate(deficits) if deficit)
    stop = strip[stop_index]
    if len(strip) > 1:
        direction = tuple(strip[1][axis]-strip[0][axis] for axis in (0, 1))
    elif marker is not None:
        marker_tile = tuple(coordinate//2 for coordinate in marker)
        direction = tuple(strip[0][axis]-marker_tile[axis] for axis in (0, 1))
    else:
        direction = (0, 1)
    assert sum(abs(coordinate) for coordinate in direction) == 1
    entry = {point for point in vertices_of({stop})
             if (point[0] % 2 == int(direction[0] < 0) if direction[0]
                 else point[1] % 2 == int(direction[1] < 0))}
    assert len(entry) == 2 and not entry & (current[2] | endpoints)
    if marker is not None:
        assert marker in endpoints
        marker_tile = tuple(coordinate//2 for coordinate in marker)
        assert marker_tile == tuple(strip[0][axis]-direction[axis] for axis in (0, 1))
    assert charge(current) >= 1
    totals['physical_corridor_models'] += 1
    return dict(stop=stop, deficit=deficits[stop_index], direction=direction,
                total_capacity=sum(deficits), length=len(strip), saturated_prefix=stop_index)


def image_map(rows, columns, symmetry, offset=(0, 0)):
    transpose, flip_row, flip_column = symmetry

    def move(point):
        row, column = point
        row = rows-1-row if flip_row else row
        column = columns-1-column if flip_column else column
        row, column = (column, row) if transpose else (row, column)
        return row+offset[0], column+offset[1]

    return move


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    totals = Counter()
    local = collision_controls(totals)
    strips = strip_controls(totals)
    sharp = []
    for width, height in itertools.product(range(6, 31, 2), (4, 6, 10)):
        current, _, _ = neutral_pair(width, height)
        strip = corridor(width, height)
        cells = vertices_of(set(strip))
        extra = {(row, 2*column+1) for _, column in strip[:-1] for row in (8, 9)}
        if height >= 6:
            extra.add((8, 2*strip[-1][1]+1))
        filled = *current[:2], current[2] | extra, current[3]
        result = inspect(filled, strip, totals, (8, 5))
        assert result['total_capacity'] == (2 if height == 4 else 1)
        assert result['saturated_prefix'] == len(strip)-1
        assert charge(filled) == 1
        force_matching(filled, totals)
        totals['sharp_parameter_pairs'] += 1
        if (width, height) in ((6, 4), (6, 6), (30, 4), (30, 10)):
            sharp.append(dict(parameters=[width, height], **result))
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*filled, *symmetry)
                move = image_map(*filled[:2], symmetry)
                image_strip = [tuple(coordinate//2 for coordinate in move((2*row, 2*column)))
                               for row, column in strip]
                image = *shape, selected, matching
                image_result = inspect(image, image_strip, totals, move((8, 5)))
                assert image_result['total_capacity'] == result['total_capacity']
                totals['physical_symmetries'] += 1
        for seed in range(4):
            selected = set(current[2])
            candidates = sorted(cells-selected)
            random.Random(1000*width+100*height+seed).shuffle(candidates)
            for point in candidates:
                candidate = *current[:2], selected | {point}, current[3]
                try:
                    direct_check(*candidate)
                except AssertionError:
                    continue
                selected.add(point)
            extension = *current[:2], selected, current[3]
            record = inspect(extension, strip, totals, (8, 5))
            assert record['total_capacity'] >= (2 if height == 4 else 1)
            assert frozen_certificate(extension)[0] == endpoints_of(extension)
            assert charge(extension) == 1
            totals['feasible_selection_extensions'] += 1
    mixed_selected, mixed_matching, claims = set(), [], []
    base, _, _ = neutral_pair(12, 8)
    for index, symmetry in enumerate(((False, False, False), (False, True, True),
                                      (True, False, False), (True, True, True))):
        offset = 40*(index//2), 40*(index % 2)
        move = image_map(*base[:2], symmetry, offset)
        mixed_selected |= {move(point) for point in base[2]}
        mixed_matching += [tuple(move(point) for point in edge) for edge in base[3]]
        claims.append(([tuple(coordinate//2 for coordinate in move((2*row, 2*column)))
                        for row, column in corridor(12, 8)], move((8, 5))))
    mixed = 90, 90, mixed_selected, mixed_matching
    stops = [inspect(mixed, strip, totals, marker) for strip, marker in claims]
    counts = Counter(record['stop'] for record in stops)
    for tile, requests in counts.items():
        assert requests <= 2*(2-len(mixed_selected & vertices_of({tile})))
    assert charge(mixed) == len(claims) == 4
    assert len(mixed_matching) >= 10*len(claims)
    assert 20*len(mixed_selected)+19*len(mixed_matching) <= 10*mixed[0]*mixed[1]
    totals['mixed_positive_source_configurations'] += 1
    report = dict(status='PASS', controls=dict(totals), short_strips=strips,
                  local_capacity_minima=local, sharp_examples=sharp,
                  mixed_claims=stops,
                  scope='Finite controls for the general written arbitrary-exterior endpoint-free '
                  'corridor theorem, first-stop propagation/injection and mixed allocation. '
                  'The mixed physical source example has disjoint stops; local transverse '
                  'sharpness patches are feasible but have no positive sources. No universal '
                  'coverage, mixed-source sharpness or grid triple equality claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], controls=report['controls'])))


if __name__ == '__main__':
    main()
