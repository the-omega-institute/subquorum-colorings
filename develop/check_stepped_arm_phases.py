"""Check all-length stepped phase tables, bad alignment, and mixed channels."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_comb_channels import occupied_family
from check_component_receivers import verify_terminal, vertices_of
from check_elbow_sources import phase
from check_guarded_stepped_arms import stepped
from check_orthogonal_source_mouths import feasible, strips_of
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def optional_flanks(k):
    return [(-1, 3), (1, 5)]+[(row, 3) for row in range(6, 2*k+4, 2)]


def configuration(k, additions=(), shifted=False):
    source = stepped(k)
    move = lambda point: (point[0]+4, point[1]+5+int(shifted))
    return (source['bottom']+8, 16,
            {move(point) for point in source['selected'] | set(additions)},
            [tuple(move(point) for point in edge) for edge in source['matching']])


def verify(k, additions=(), rectangle_controls=False):
    current = configuration(k, additions)
    assert feasible(current)
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    assert checked['receivers'][0]['charge_twice'] == 2
    selected = {(row-4, column-5) for row, column in current[2]}
    bottom = 2*k+4
    rows, columns = current[:2]
    gains = {}
    for horizontal in (True, False):
        records = []
        for band in range((rows if horizontal else columns)//2):
            cells = {point for point in itertools.product(range(rows), range(columns))
                     if point[0 if horizontal else 1]//2 == band}
            actual = phase(current, cells, horizontal)
            relative = 2*band-(4 if horizontal else 5)
            if horizontal:
                expected = (1-int((relative, 3) in selected)
                            if 4 <= relative < bottom else int(relative == bottom))
            else:
                expected = {-1: 1, 1: 0, 3: 2-int((-1, 3) in selected),
                            5: 1-int((1, 5) in selected)}.get(relative, 0)
            assert actual == expected >= 0, (k, additions, horizontal, relative, actual, expected)
            records.append(dict(relative=relative, gain=actual))
        gains[horizontal] = records
    horizontal_total = sum(record['gain'] for record in gains[True])
    vertical_total = sum(record['gain'] for record in gains[False])
    arm_count = sum((row, 3) in selected for row in range(6, bottom, 2))
    assert horizontal_total == k+1-arm_count >= 2
    assert vertical_total == 4-int((-1, 3) in selected)-int((1, 5) in selected) >= 2
    rectangles = 0
    if rectangle_controls:
        for horizontal in (True, False):
            for top, end_row in itertools.combinations(range(0, rows+1, 2), 2):
                for left, end_column in itertools.combinations(range(0, columns+1, 2), 2):
                    cells = set(itertools.product(range(top, end_row), range(left, end_column)))
                    if not cells & endpoints:
                        continue
                    extremes = (left, end_column-1) if horizontal else (top, end_row-1)
                    if any(point in endpoints for point in cells
                           if point[1 if horizontal else 0] in extremes):
                        continue
                    actual = phase(current, cells, horizontal)
                    if horizontal:
                        expected = sum(1-int((row, 3) in selected)
                                       for row in range(4, bottom, 2) if (row+4, 5) in cells)
                        expected += int((bottom+4, 10) in cells)
                    else:
                        expected = sum(record['gain'] for record in gains[False]
                                       if any(point in cells and point[1]//2 ==
                                              (record['relative']+5)//2 for point in endpoints))
                    assert actual == expected >= 0
                    rectangles += 1
    return dict(k=k, added=len(additions), horizontal_phase=horizontal_total,
                vertical_phase=vertical_total, rectangles=rectangles)


def bad_alignment(k):
    current = configuration(k, shifted=True)
    checked = verify_terminal(current)
    assert frozen_certificate(current)[0] == endpoint_data(current)[0]
    assert checked['receivers'][0]['charge_twice'] == -2*k
    rows, columns = current[:2]
    gains = []
    for row in range(0, rows, 2):
        cells = set(itertools.product((row, row+1), range(columns)))
        actual = phase(current, cells, True)
        expected = -int(8 <= row <= 2*k+8)
        assert actual == expected
        gains.append(actual)
    assert sum(gains) == -(k+1)
    return dict(k=k, receiver_charge=-k, full_phase=sum(gains),
                negative_bands=sum(value < 0 for value in gains),
                uncovered_phase_after_spending_whole_negative_charge=1)


def channel(width, depth, k, left_extra, right_extra, sharp):
    minimum = k+4
    current, sources, walls = occupied_family(width, depth, minimum+left_extra,
                                               minimum+right_extra, blocker='none')
    tip = 2*depth+4
    source = stepped(k)
    move = lambda point: (point[0]+tip+4, point[1]+13)
    selected = source['selected'] | (set(optional_flanks(k)) if sharp else set())
    current = (*current[:2], current[2] | {move(point) for point in selected},
               current[3]+[tuple(move(point) for point in edge) for edge in source['matching']])
    assert feasible(current)
    checked = verify_terminal(current)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    assert sorted(receiver['charge_twice'] for receiver in checked['receivers']) == [0, 0, 2, 2]
    payments = {tile: 2-len(vertices_of({tile}) & current[2])
                for tile in itertools.product(range(current[0]//2), range(current[1]//2))
                if not vertices_of({tile}) & endpoints}
    mouths = Counter(tile for strip in strips_of(sources) for tile in strip['tiles'])
    assert all(payments.get(tile, 0) == 0 for tile in mouths)
    left, right, left_start, right_start, left_end, right_end = walls
    first, last = max(left_start, right_start)-1, min(left_end, right_end)
    cells = set(itertools.product(range(first, last+2), range(left+1, right)))
    channel_tiles = {(row//2, column//2) for row, column in cells}
    gain = phase(current, cells, True)
    expected_gain = 2 if sharp else k+1
    assert gain == expected_gain
    shifted = 0
    for top in range(first, last+2, 2):
        for start in range(left+2, right-1, 2):
            square = set(itertools.product((top, top+1), (start, start+1)))
            if not square & endpoints:
                shifted += 2-len(square & current[2])
    payment = sum(payments.get(tile, 0) for tile in channel_tiles)
    length = minimum+min(left_extra, right_extra)
    unequal = int(left_end != right_end)
    assert shifted == 10*length-8*k-(25 if sharp else 23)
    assert payment == (10*length-8*k-21-unequal if sharp else
                       10*length-7*k-20-unequal)
    assert payment == 2-unequal+gain+shifted
    residual = sum((2-mouths[tile])*count for tile, count in payments.items())
    delta = checked['area']//2-checked['objective']
    assert 2*delta == -2-2+residual
    assert all(2 <= 2-mouths[tile] for tile in channel_tiles if payments.get(tile, 0) > 0)
    lower_bound = -2-2+2*(2-unequal+gain)
    assert lower_bound == 2*(gain-unequal) <= 2*delta
    return dict(width=width, depth=depth, k=k, sharp=sharp, unequal=unequal,
                minimum_wall_half_length=length, source_phase=gain,
                physical_payment=payment, shifted_payment=shifted,
                doubled_lower_bound=lower_bound, half_area_deficit=delta,
                source_tax_twice=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = [verify(k, optional_flanks(k) if sharp else (), k <= 2)
               for k, sharp in itertools.product((1, 2, 3, 6, 16, 32), (False, True))]
    exhaustive = 0
    for k in range(1, 7):
        flanks = optional_flanks(k)
        for mask in range(1 << len(flanks)):
            additions = {point for index, point in enumerate(flanks) if mask >> index & 1}
            verify(k, additions)
            exhaustive += 1
    bad = [bad_alignment(k) for k in (1, 2, 3, 6, 16, 32)]
    channels = [channel(width, depth, k, left, right, sharp)
                for width, depth, k, left, right, sharp in itertools.product(
                    (32, 40), (1, 3), (1, 2, 5), (0, 2), (0, 2), (False, True))]
    images = 0
    current = configuration(3, optional_flanks(3))
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, *symmetry)
        image = *shape, selected, matching
        assert feasible(image) and verify_terminal(image)['receivers'][0]['charge_twice'] == 2
        assert frozen_certificate(image)[0] == endpoint_data(image)[0]
        images += 1
    report = dict(status='ALL_CHECKS_PASSED', parameter_cases=len(records), records=records,
                  admissible_rectangles=sum(record['rectangles'] for record in records),
                  exhaustive_flank_cases=exhaustive, bad_alignment_cases=bad,
                  mixed_channel_cases=len(channels), channels=channels, symmetry_images=images,
                  scope='Finite controls of independent all-k phase/freezing/count proofs. '
                        'The shifted-family counterexample refutes the proposed negative-charge '
                        'phase budget, not the target grid inequality. Geometry remains written.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('records', 'channels')}))


if __name__ == '__main__':
    main()
