"""Check connected sharp entry chains and uniform two-stage certificates."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors, occupied_degrees
from check_flexible_block_entries import matching_blocks
from check_matching_block_tile_ledger import connected
from check_promotion_cores import frozen_certificate
from check_rematching_receiver_flux import perfect_matchings
from check_residual_corridors import direct_check, transformed
from check_sharp_block_entries import SELECTED, fixture


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


POINTS = sorted({point for edge in fixture()[3] for point in edge})
SITES = POINTS + sorted(SELECTED)
PARTNERS = (
    [1, 0, 3, 2, 5, 4, 10, 8, 7, 12, 6, 15, 9, 14, 13, 11],
    [1, 0, 7, 8, 5, 4, 10, 2, 3, 12, 6, 15, 9, 14, 13, 11],
)
CERTIFICATES = (
    [(0, 16, 19), (12, 21, 23), (2, 17, 1), (4, 3, 9),
     (8, 3, 9), (6, 1, 7), (11, 7, 10), (14, 10, 15),
     (5, 18, 20), (13, 22, 24), (15, 14, 25), (10, 11, 14),
     (7, 6, 11), (3, 4, 8), (1, 2, 6), (9, 4, 8)],
    [(0, 16, 19), (12, 21, 23), (2, 17, 1), (6, 1, 7),
     (8, 7, 9), (4, 3, 9), (11, 7, 10), (14, 10, 15),
     (5, 18, 20), (13, 22, 24), (15, 14, 25), (10, 11, 14),
     (7, 6, 11), (1, 2, 6), (3, 2, 4), (9, 4, 8)],
)


def translate(point, index, row_shift=0):
    return point[0]-3*index+row_shift, point[1]+6*index


def chain(choices):
    copies = len(choices)
    assert copies >= 1
    row_shift = 2*((3*(copies-1)+1)//2)
    selected = {translate(point, index, row_shift)
                for index in range(copies) for point in SELECTED}
    matching = []
    for index, choice in enumerate(choices):
        matching.extend((translate(POINTS[point], index, row_shift),
                         translate(POINTS[partner], index, row_shift))
                        for point, partner in enumerate(PARTNERS[choice]) if point < partner)
    endpoints = {point for edge in matching for point in edge}
    selected -= endpoints
    return row_shift+6, 6*copies+2, selected, matching


def check_interactions():
    endpoints = set(POINTS)
    occupied = endpoints | SELECTED
    moved_endpoints = {translate(point, 1) for point in endpoints}
    moved_selected = {translate(point, 1) for point in SELECTED}
    moved_occupied = moved_endpoints | moved_selected
    assert not endpoints & moved_endpoints and not SELECTED & moved_selected
    assert SELECTED & moved_endpoints == {(1, 7)}
    assert endpoints & moved_selected == {(1, 6)}
    expected = {((0, 6), (1, 6)), ((1, 5), (1, 6)), ((1, 6), (1, 7)),
                ((1, 7), (2, 7)), ((1, 7), (1, 6)), ((1, 7), (1, 8))}
    actual = {(point, other) for point in occupied for other in neighbors(point)
              if other in moved_occupied}
    assert actual == expected
    assert {(point, other) for point in endpoints for other in neighbors(point)
            if other in moved_endpoints} == {((1, 6), (1, 7))}
    for index in range(2, 5):
        moved = {translate(point, index) for point in occupied}
        assert not occupied & moved
        assert not {(point, other) for point in occupied for other in neighbors(point) if other in moved}
    return sorted(expected)


def check_templates():
    for choice, certificate in enumerate(CERTIFICATES):
        earlier = set()
        for step, (endpoint, first, second) in enumerate(certificate):
            assert first != second and {SITES[first], SITES[second]} <= set(neighbors(POINTS[endpoint]))
            assert first != PARTNERS[choice][endpoint] != second
            for witness in (first, second):
                if witness < 16:
                    assert PARTNERS[choice][witness] in earlier
                elif witness in (20, 22):
                    assert step >= 8
            earlier.add(endpoint)
        assert earlier == set(range(16))
        assert {4, 14} <= {row[0] for row in certificate[:8]}
    return 32


def inspect(choices, totals, enumerate_matchings=False):
    current = chain(choices)
    copies = len(choices)
    row_shift = current[0]-6
    objective = direct_check(*current)
    assert objective == 16*copies+2
    assert len(current[2]) == 8*copies+2 and len(current[3]) == 8*copies
    endpoints = {point for edge in current[3] for point in edge}
    assert len(endpoints) == 16*copies and connected(endpoints)
    assert Counter(occupied_degrees(current).values()) == {3: 14*copies, 4: 2*copies}
    assert current[0]*current[1]//2-objective == row_shift*(3*copies+1)+2*copies+4
    bridges = set()
    for index in range(copies-1):
        bridges.add(frozenset((translate((1, 6), index, row_shift),
                               translate((4, 1), index+1, row_shift))))
    owner = {translate(point, index, row_shift): index
             for index in range(copies) for point in POINTS}
    actual_cross = {frozenset((point, other)) for point in endpoints for other in neighbors(point)
                    if other in endpoints and owner[point] != owner[other]}
    assert actual_cross == bridges
    mate = {first: second for edge in current[3] for first, second in (edge, edge[::-1])}
    earlier = set()
    for step in range(16):
        newly_frozen = set()
        for index, choice in enumerate(choices):
            endpoint, first, second = CERTIFICATES[choice][step]
            point = translate(POINTS[endpoint], index, row_shift)
            witnesses = {translate(SITES[witness], index, row_shift) for witness in (first, second)}
            assert len(witnesses) == 2 and witnesses <= set(neighbors(point))
            assert mate[point] not in witnesses
            assert all(witness in current[2] or witness in mate and mate[witness] in earlier
                       for witness in witnesses)
            newly_frozen.add(point)
            totals['certificate_rows'] += 1
        earlier |= newly_frozen
    assert earlier == endpoints
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints and len(layers) <= 16
    if enumerate_matchings:
        matchings = list(perfect_matchings(endpoints))
        assert len(matchings) == 2**copies
        blocks, _, _ = matching_blocks(endpoints, matchings)
        assert Counter(map(len, blocks)) == {2: 6*copies, 4: copies}
        for matching in matchings:
            assert not {frozenset(edge) for edge in matching} & bridges
            assert frozen_certificate((*current[:3], matching))[0] == endpoints
        totals['independent_matchings'] += len(matchings)
    totals['models'] += 1
    totals['chosen_matching_edges'] += len(current[3])
    return current


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    interactions = check_interactions()
    template_rows = check_templates()
    totals = Counter()
    for copies in range(1, 8):
        for choices in itertools.product((0, 1), repeat=copies):
            inspect(choices, totals, enumerate_matchings=not any(choices))
    images = 0
    for copies in range(1, 5):
        current = chain([index % 2 for index in range(copies)])
        for phase in itertools.product((0, 1), repeat=2):
            shifted = (current[0]+2*phase[0], current[1]+2*phase[1],
                       {(row+phase[0], column+phase[1]) for row, column in current[2]},
                       [tuple((row+phase[0], column+phase[1]) for row, column in edge)
                        for edge in current[3]])
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*shifted, *symmetry)
                image = (*shape, selected, matching)
                assert direct_check(*image) == 16*copies+2
                endpoints = {point for edge in matching for point in edge}
                assert connected(endpoints)
                assert Counter(occupied_degrees(image).values()) == {3: 14*copies, 4: 2*copies}
                for replacement in perfect_matchings(endpoints):
                    assert frozen_certificate((*image[:3], replacement))[0] == endpoints
                    totals['image_matching_checks'] += 1
                images += 1
    generator = random.Random(20261022)
    large_controls = []
    for copies in (8, 16, 32, 64, 128):
        for _ in range(12):
            inspect([generator.randrange(2) for _ in range(copies)], totals)
        large_controls.append(dict(copies=copies, chosen_patterns=12))
    report = dict(status='PASS', controls=dict(totals), interaction_pairs=interactions,
                  fixed_template_rows=template_rows, phase_symmetry_images=images,
                  all_matching_choices_through_copies=7, large_controls=large_controls,
                  endpoint_sites=POINTS, support_sites=sorted(SELECTED),
                  partners=PARTNERS, two_stage_certificates=CERTIFICATES,
                  scope='Written arbitrary-k connected sharpness theorem, supplemented by finite '
                        'coordinate, independent matching, degree and freezing controls. No '
                        'positive-demand sharpness, minimum-size result or new grid bound claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('partners', 'two_stage_certificates', 'endpoint_sites', 'support_sites')}, indent=2))


if __name__ == '__main__':
    main()
