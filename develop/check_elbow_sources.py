"""Independent controls for frozen thick elbows and their partial phase tables."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_comb_channels import occupied_family
from check_cooperative_promotion import neighbors
from check_orthogonal_source_mouths import feasible
from check_orthogonal_source_mouths import strips_of
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def elbow(width, height, additions=()):
    assert width >= 6 and height >= 4 and width % 2 == height % 2 == 0
    endpoints = {(row, column) for row in (0, 1) for column in range(width)}
    endpoints |= {(row, column) for row in range(2, height)
                  for column in (width-2, width-1)}
    endpoints |= {(2, 0), (height, width-1)}
    matching = [((0, column), (0, column+1)) for column in range(0, width, 2)]
    matching += [((1, column), (1, column+1)) for column in range(1, width-2, 2)]
    matching += [((1, 0), (2, 0))]
    matching += [((row, width-1), (row+1, width-1)) for row in range(1, height, 2)]
    matching += [((row, width-2), (row+1, width-2)) for row in range(2, height-1, 2)]
    selected = {(0, -1), (0, width), (2, -1), (3, 0), (height+1, width-1)}
    selected |= {(row, width) for row in range(2, height+1, 2)}
    selected |= {(row, width-3) for row in range(3, height, 2)}
    selected |= set(additions)
    move = lambda point: (point[0]+4, point[1]+5)
    current = (height+8, width+12, {move(point) for point in selected},
               [tuple(move(point) for point in edge) for edge in matching])
    assert endpoint_data(current)[0] == {move(point) for point in endpoints}
    return current


def raw_twice(current, cells):
    endpoints = endpoint_data(current)[0]
    squares = {tuple((row//2, column//2)) for row, column in endpoints & cells}
    assert all(vertices_of({square}) <= cells for square in squares)
    return sum(len(vertices_of({square}) & endpoints)
               + 2*len(vertices_of({square}) & current[2])-4 for square in squares)


def phase(current, cells, horizontal):
    endpoints = endpoint_data(current)[0]
    axis = 1 if horizontal else 0
    across = sorted({point[axis] for point in cells})
    other = sorted({point[1-axis] for point in cells})
    assert set(itertools.product(other, across) if horizontal
               else itertools.product(across, other)) == cells
    assert across[0] % 2 == other[0] % 2 == 0
    assert len(across) % 2 == len(other) % 2 == 0
    boundary = {point for point in cells if point[axis] in (across[0], across[-1])}
    assert not boundary & endpoints
    shifted = []
    for upper in other[::2]:
        for left in across[1:-1:2]:
            square = {(upper+local_row, left+local_column) if horizontal
                      else (left+local_column, upper+local_row)
                      for local_row, local_column in itertools.product((0, 1), repeat=2)}
            if square & endpoints:
                shifted.append(len(square & endpoints)+2*len(square & current[2])-4)
    difference = raw_twice(current, cells)-sum(shifted)
    assert difference % 2 == 0
    return difference//2


def band_records(current, width, height):
    selected = {(row-4, column-5) for row, column in current[2]}
    endpoints = endpoint_data(current)[0]
    rows, columns = current[:2]
    result = []
    for horizontal in (True, False):
        axis = 0 if horizontal else 1
        for band in sorted({point[axis]//2 for point in endpoints}):
            cells = {(row, column) for row in range(rows) for column in range(columns)
                     if (row if horizontal else column)//2 == band}
            gain = phase(current, cells, horizontal)
            relative = 2*band-(4 if horizontal else 5)
            if horizontal:
                expected = int(relative == 2)+int(relative == height)
                kind = 'tip' if expected else 'full'
            elif relative == -1:
                expected, kind = 1-int((-1, 0) in selected), 'left_cap'
            elif relative == width-1:
                expected, kind = 1-int((-1, width-1) in selected), 'right_cap'
            elif relative == width-3:
                upper = sum((-1, column) in selected for column in (relative, relative+1))
                assert upper <= 1
                expected, kind = 2-upper, 'transition'
                assert gain >= 1
            else:
                upper = sum((-1, column) in selected for column in (relative, relative+1))
                lower = sum((2, column) in selected for column in (relative, relative+1))
                assert upper <= 1 and lower <= 1
                expected, kind = 2-upper-lower, 'chamber'
            assert gain == expected and gain >= 0
            result.append(dict(horizontal=horizontal, physical_band=band,
                               relative_start=relative, kind=kind, gain=gain))
    assert sum(record['gain'] for record in result if record['horizontal']) == 2
    upper = sum((-1, column) in selected for column in range(width))
    lower = sum((2, column) in selected for column in range(1, width-3))
    assert 2*upper <= width and 2*lower <= width-4
    assert sum(record['gain'] for record in result if not record['horizontal']) == width-upper-lower >= 2
    return result


def inspect(current, width, height, rectangle_controls=False):
    assert feasible(current)
    endpoints = endpoint_data(current)[0]
    assert endpoint_components(current) == [endpoints]
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    tiles = {(row//2, column//2) for row, column in endpoints}
    receiver = vertices_of(tiles)
    assert len(endpoints) == 2*width+2*height-2
    assert len(current[3]) == width+height-1
    assert len(tiles) == width//2+height+1
    assert len(receiver & current[2]) == height+4
    assert len(receiver & current[2])+len(endpoints)//2-2*len(tiles) == 1
    for point in receiver-endpoints-current[2]:
        adjacent = set(neighbors(point))
        assert len(adjacent & endpoints) >= 2 or any(
            set(neighbors(support)) & endpoints for support in adjacent & current[2])
    records = band_records(current, width, height)
    transition = {(row, column) for row in range(2, height+6)
                  for column in (width+2, width+3)}
    assert not transition & {(6, 5), (height+4, width+4)}
    transition_gain = phase(current, transition, False)
    assert transition_gain >= 1
    rectangles = 0
    if rectangle_controls:
        for horizontal in (True, False):
            for top, bottom in itertools.combinations(range(0, current[0]+1, 2), 2):
                for left, right in itertools.combinations(range(0, current[1]+1, 2), 2):
                    cells = set(itertools.product(range(top, bottom), range(left, right)))
                    if not cells & endpoints:
                        continue
                    boundary = {point for point in cells if point[1 if horizontal else 0]
                                in ((left, right-1) if horizontal else (top, bottom-1))}
                    if boundary & endpoints:
                        continue
                    gain = phase(current, cells, horizontal)
                    if horizontal:
                        expected = len(cells & {(6, 5), (height+4, width+4)})
                        assert gain == expected
                    else:
                        expected = sum(record['gain'] for record in records
                                       if not record['horizontal'] and any(
                                           point in cells and point[1]//2 == record['physical_band']
                                           for point in endpoints))
                        assert gain == expected
                    rectangles += 1
    return dict(width=width, height=height, bands=records, rectangles=rectangles,
                transition_without_tips=transition_gain, freezing_layers=len(layers))


def sharp_flanks(width):
    return {(-1, column) for column in range(0, width, 2)} | {
        (2, column) for column in range(2, width-3, 2)}


def extended_channel(width, depth, elbow_height, left_extra, right_extra):
    minimum = elbow_height//2+2
    current, sources, walls = occupied_family(width, depth, minimum+left_extra,
                                               minimum+right_extra, blocker='none')
    tip = 2*depth+4
    added = elbow(6, elbow_height)
    move = lambda point: (point[0]+tip, point[1]+8)
    current = (*current[:2], current[2] | {move(point) for point in added[2]},
               current[3]+[tuple(move(point) for point in edge) for edge in added[3]])
    assert feasible(current)
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0, 0, 2, 2]
    all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
    payments = {tile: 2-len(vertices_of({tile}) & current[2]) for tile in all_tiles
                if not vertices_of({tile}) & endpoints}
    mouths = Counter(tile for strip in strips_of(sources) for tile in strip['tiles'])
    assert all(payments.get(tile, 0) == 0 for tile in mouths)
    delta = checked['area']//2-checked['objective']
    assert delta == sum(payments.values())-2
    left, right, left_start, right_start, left_end, right_end = walls
    first, last = max(left_start, right_start)-1, min(left_end, right_end)
    cells = set(itertools.product(range(first, last+2), range(left+1, right)))
    channel_tiles = {(row//2, column//2) for row, column in cells}
    gain = phase(current, cells, True)
    assert gain == 2
    shifted_payment = 0
    for upper in range(first, last+2, 2):
        for start in range(left+2, right-1, 2):
            square = set(itertools.product((upper, upper+1), (start, start+1)))
            if not square & endpoints:
                shifted_payment += 2-len(square & current[2])
    unequal = int(left_end != right_end)
    payment = sum(payments.get(tile, 0) for tile in channel_tiles)
    assert payment == 2-unequal+gain+shifted_payment
    half_length = min(left_end, right_end)//2-tip//2
    assert payment == 10*half_length-2*elbow_height-6-unequal
    assert shifted_payment == 10*half_length-2*elbow_height-10
    residual = sum((2-mouths[tile])*count for tile, count in payments.items())
    assert residual == 2*sum(payments.values())
    assert 2*delta == -2-2+residual
    assert -2+residual == 2*delta+2
    assert all(2 <= 2-mouths[tile] for tile in channel_tiles if payments.get(tile, 0) > 0)
    lower_bound = -2-2+2*(2-unequal+gain)
    assert lower_bound == 4-2*unequal
    assert lower_bound <= 2*delta and delta >= 2-unequal
    assert any(4 > 2-mouths[tile] for tile in channel_tiles if payments.get(tile, 0) > 0)
    return dict(width=width, depth=depth, elbow_height=elbow_height,
                wall_half_lengths=(minimum+left_extra, minimum+right_extra),
                source_phase=gain, elbow_tax_twice=2, original_flux=-2,
                physical_payment=payment, shifted_payment=shifted_payment,
                residual_payment=residual, doubled_lower_bound=lower_bound,
                half_area_deficit=delta, unadjusted_ledger_error=2,
                repeated_channel_capacity_rejected=True,
                terminal_occupied=not bool(min(left_extra, right_extra)))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    counts = Counter()
    for width, height in itertools.product((6, 8, 10, 16, 32, 64), (4, 6, 8, 16, 32)):
        for sharp in (False, True):
            current = elbow(width, height, sharp_flanks(width) if sharp else ())
            record = inspect(current, width, height, width <= 10 and height <= 8)
            record['sharp'] = sharp
            if sharp:
                assert sum(band['gain'] for band in record['bands'] if not band['horizontal']) == 2
            records.append(record)
            counts['parameter_cases'] += 1
    for width in (6, 8):
        candidates = [(-1, column) for column in range(width)]
        candidates += [(2, column) for column in range(2, width-3)]
        for chosen in itertools.product((False, True), repeat=len(candidates)):
            additions = {point for point, take in zip(candidates, chosen) if take}
            current = elbow(width, 4, additions)
            if not feasible(current):
                continue
            inspect(current, width, 4)
            counts['exhaustive_flank_cases'] += 1
    for seed in range(32):
        width, height = 10, 8
        current = elbow(width, height)
        points = [(row, column) for row in (-1, 2) for column in range(-1, width+1)]
        points += [(row, column) for row in range(2, height+2) for column in (width-3, width)]
        random.Random(seed).shuffle(points)
        for row, column in points:
            point = row+4, column+5
            trial = *current[:2], current[2] | {point}, current[3]
            if feasible(trial):
                current = trial
        inspect(current, width, height)
        counts['greedy_exterior_cases'] += 1
    channel_records = [extended_channel(width, depth, height, left, right)
                       for width, depth, height, left, right in itertools.product(
                           (32, 40), (1, 3), (4, 6, 10), (0, 2), (0, 2))]
    counts['extended_channel_cases'] = len(channel_records)
    images = 0
    current = elbow(8, 6, sharp_flanks(8))
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, *symmetry)
        image = *shape, selected, matching
        assert feasible(image)
        assert frozen_certificate(image)[0] == endpoint_data(image)[0]
        assert verify_terminal(image)['receivers'][0]['charge_twice'] == 2
        images += 1
    witness = elbow(6, 4, sharp_flanks(6))
    report = dict(status='ALL_CHECKS_PASSED', counts=dict(counts), symmetry_images=images,
                  admissible_rectangles=sum(record['rectangles'] for record in records),
                  records=records, extended_channels=channel_records,
                  witness=dict(shape=witness[:2], selected=sorted(witness[2]), matching=witness[3]),
                  scope='Finite controls of explicit elbow family, complete freezing, exact whole charge, '
                        'all band tables, sharp perpendicular gain two, partial rectangles and tip-free '
                        'transition credit. General proof is separate; arbitrary positive bends remain open.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('records', 'witness', 'extended_channels')}))


if __name__ == '__main__':
    main()
