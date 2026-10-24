"""Check bounded-height sharp chains and every exact synchronous freezing time."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_connected_sharp_entry_chains import PARTNERS, POINTS
from check_cooperative_promotion import neighbors, occupied_degrees
from check_flexible_block_entries import matching_blocks
from check_matching_block_tile_ledger import connected
from check_promotion_cores import frozen_certificate
from check_rematching_receiver_flux import perfect_matchings
from check_residual_corridors import direct_check
from check_sharp_block_entries import SELECTED


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def translate(point, index):
    return (point[0]+4 if index % 2 == 0 else 6-point[0]), point[1]+6*index


def chain(choices):
    copies = len(choices)
    assert copies >= 1
    matching = [(translate(POINTS[point], index), translate(POINTS[partner], index))
                for index, choice in enumerate(choices)
                for point, partner in enumerate(PARTNERS[choice]) if point < partner]
    endpoints = {point for edge in matching for point in edge}
    selected = {translate(point, index) for index in range(copies) for point in SELECTED}-endpoints
    return 10, 6*copies+2, selected, matching


def times(index, remaining):
    return [3*index+1, 3*remaining+6, 3*index+2, 3*remaining+5,
            3*index+3, 1 if remaining == 0 else 3*remaining+4, 3*index+4, 4,
            3*index+3, 3*remaining+5, 3, 3*index+5, 1, 1, 3*index+6, 2]


def check_interfaces():
    occupied = set(POINTS) | SELECTED
    counts = []
    for index in (0, 1):
        endpoints = {translate(point, index) for point in POINTS}
        selected = {translate(point, index) for point in SELECTED}
        moved_endpoints = {translate(point, index+1) for point in POINTS}
        moved_selected = {translate(point, index+1) for point in SELECTED}
        assert selected & moved_endpoints == {translate((1, 7), index)}
        assert endpoints & moved_selected == {translate((1, 6), index)}
        assert not endpoints & moved_endpoints and not selected & moved_selected
        first = {translate(point, index) for point in occupied}
        second = {translate(point, index+1) for point in occupied}
        cross = {(point, other) for point in first for other in neighbors(point) if other in second}
        counts.append(len(cross))
        for point in endpoints | (selected-moved_endpoints):
            assert not (set(neighbors(point)) & (second-first))
        for point in moved_endpoints | (moved_selected-endpoints):
            assert not (set(neighbors(point)) & (first-second))
    assert counts == [6, 6]
    first = occupied
    second = {(2-row, column+6) for row, column in occupied}
    actual = {(point, other) for point in first for other in neighbors(point) if other in second}
    expected = {((0, 6), (1, 6)), ((1, 5), (1, 6)), ((1, 6), (1, 7)),
                ((1, 7), (2, 7)), ((1, 7), (1, 6)), ((1, 7), (1, 8))}
    assert actual == expected
    return sorted(actual)


def inspect(choices, totals, all_matchings=False):
    copies = len(choices)
    current = chain(choices)
    endpoints = {point for edge in current[3] for point in edge}
    assert direct_check(*current) == 16*copies+2
    assert len(current[2]) == 8*copies+2 and len(current[3]) == 8*copies
    assert connected(endpoints)
    assert Counter(occupied_degrees(current).values()) == {3: 14*copies, 4: 2*copies}
    assert current[0]*current[1]//2-(16*copies+2) == 14*copies+8
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    actual_times = {tuple(row['endpoint']): round_number
                    for round_number, layer in enumerate(layers, 1) for row in layer}
    earlier_vertical = 0
    for index, choice in enumerate(choices):
        arrival = 3*index+1+earlier_vertical
        for site, expected_time in ((0, arrival), (2, arrival+1), (8, arrival+2), (4, arrival+2+choice)):
            assert actual_times[translate(POINTS[site], index)] == expected_time
            totals['matching_independent_entry_times'] += 1
        earlier_vertical += choice
    assert len(layers) >= 3*copies
    if not any(choices):
        expected = {translate(point, index): times(index, copies-1-index)[site]
                    for index in range(copies) for site, point in enumerate(POINTS)}
        assert actual_times == expected
        assert len(layers) == 3*copies+3
        totals['exact_time_endpoints'] += len(endpoints)
        totals['exact_time_chains'] += 1
    if all_matchings:
        matchings = list(perfect_matchings(endpoints))
        assert len(matchings) == 2**copies
        blocks, _, _ = matching_blocks(endpoints, matchings)
        assert Counter(map(len, blocks)) == {2: 6*copies, 4: copies}
        for matching in matchings:
            assert frozen_certificate((*current[:3], matching))[0] == endpoints
        totals['independent_matchings'] += len(matchings)
    totals['models'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    interfaces = check_interfaces()
    totals = Counter()
    for copies in range(1, 8):
        for choices in itertools.product((0, 1), repeat=copies):
            inspect(choices, totals, all_matchings=not any(choices))
    for copies in range(8, 65):
        inspect([0]*copies, totals)
    generator = random.Random(2026102201)
    for copies in (8, 16, 32, 64, 128):
        for _ in range(12):
            inspect([generator.randrange(2) for _ in range(copies)], totals)
    report = dict(status='PASS', controls=dict(totals), interaction_pairs=interfaces,
                  all_matching_choices_through_copies=7, all_horizontal_time_checks_through=64,
                  random_patterns_per_size=12, random_pattern_sizes=[8, 16, 32, 64, 128],
                  exact_time_formula='3k+3 rounds for all-horizontal; every matching needs at least3k; four exact entry times hold for every choice string',
                  scope='Finite checks supplement the arbitrary-k geometric, matching, two-wave '
                        'freezing and exact-time proofs. No new global grid bound claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
