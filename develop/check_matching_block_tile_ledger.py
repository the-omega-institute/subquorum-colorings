"""Check actual matching-block tile accounting and all-width band certificates."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_charge_two_frozen_receiver import fixture as charge_two
from check_component_receivers import shifted, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_exchange_terminal_nonunique import fixture, graft
from check_flexible_block_entries import matching_blocks
from check_owned_donors import straight_comb
from check_promotion_cores import frozen_certificate
from check_rematching_receiver_flux import canonical, perfect_matchings
from check_residual_corridors import direct_check, transformed
from degree_three_fusion import occupied_bands, occupied_band_certificate


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def connected(points):
    if not points:
        return True
    reached = {min(points)}
    while True:
        extended = reached | {other for point in reached for other in neighbors(point) if other in points}
        if extended == reached:
            return reached == points
        reached = extended


def inspect(current, totals):
    objective = direct_check(*current)
    endpoints = {point for edge in current[3] for point in edge}
    assert all(degree >= 3 for degree in occupied_degrees(current).values())
    matchings = list(perfect_matchings(endpoints))
    blocks, owner, _ = matching_blocks(endpoints, matchings)
    assert matchings
    tiles = {(row//2, column//2) for row, column in endpoints}
    charges = []
    no_two_selected = True
    for block in blocks:
        receiver = {(row//2, column//2) for row, column in block}
        charge = len(block)//2+sum(len(current[2] & vertices_of({tile}))-2 for tile in receiver)
        charges.append(charge)
        if len(block) == 2:
            assert charge <= 0
            totals['forced_block_checks'] += 1
        elif all(len(set(neighbors(point)) & current[2]) <= 1 for point in block):
            assert charge <= 0
            for tile in receiver:
                cells = vertices_of({tile})
                assert len(block & cells)+2*len(current[2] & cells) <= 4
            totals['flexible_block_checks'] += 1
        else:
            no_two_selected = False
    weighted_edges = mixed_full = overlap = 0
    inventory = Counter()
    for tile in tiles:
        cells = vertices_of({tile})
        local = endpoints & cells
        owners = {owner[point] for point in local}
        assert connected(local)
        for index in owners:
            assert connected(blocks[index] & cells)
            totals['block_tile_connectivity_checks'] += 1
        selected = len(current[2] & cells)
        cross = sum(point < other and owner[point] != owner[other]
                    for point in local for other in set(neighbors(point)) & local)
        full = int(len(local) == 4 and len(owners) > 1)
        assert cross == len(owners)-1+full
        weighted_edges += (2-selected)*cross
        mixed_full += full
        overlap += (len(owners)-1)*(2-selected)
        inventory[len(local), selected, len(owners), cross] += 1
        if len(local)+2*selected > 4:
            assert len(local) == 1 and selected == 2
            forced = len(blocks[owner[next(iter(local))]]) == 2
            if no_two_selected:
                assert forced
            totals['positive_forced_singletons' if forced else 'nonterminal_flexible_singletons'] += 1
    charge = len(endpoints)//2+sum(len(current[2] & vertices_of({tile}))-2 for tile in tiles)
    assert overlap == weighted_edges-2*mixed_full
    assert charge == sum(charges)+overlap
    exchange_terminal = all(frozen_certificate((*current[:3], matching))[0] == endpoints
                            for matching in matchings)
    if exchange_terminal:
        assert no_two_selected and max(charges, default=0) <= 0
        totals['exchange_terminal_models'] += 1
        if weighted_edges == 0:
            assert mixed_full == 0 and charge <= 0
            totals['separated_block_models'] += 1
    if current[0] % 2 == current[1] % 2 == 0:
        all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
        deficit = sum(2-len(current[2] & vertices_of({tile})) for tile in all_tiles-tiles)
        assert deficit >= 0
        assert current[0]*current[1]//2-objective == deficit-sum(charges)+2*mixed_full-weighted_edges
    totals['models'] += 1
    totals['matchings'] += len(matchings)
    return dict(blocks=len(blocks), flexible_blocks=sum(len(block) > 2 for block in blocks),
                block_charges=charges, buffer=-sum(charges), interface_weight=weighted_edges,
                mixed_full_tiles=mixed_full, overlap_correction=overlap,
                receiver_charge=charge, exchange_terminal=exchange_terminal,
                inventory=[dict(count=number, profile=list(profile)) for profile, number in sorted(inventory.items())])


def small_models(rows, columns):
    points = list(itertools.product(range(1, rows+1), range(1, columns+1)))
    for mask in range(1, 1 << len(points)):
        if mask.bit_count() % 2:
            continue
        endpoints = {point for index, point in enumerate(points) if mask >> index & 1}
        if 2*sum(sum(point) % 2 == 0 for point in endpoints) != len(endpoints):
            continue
        matchings = list(perfect_matchings(endpoints))
        if not matchings:
            continue
        supports = sorted({other for point in endpoints for other in neighbors(point)
                           if other not in endpoints and len(set(neighbors(other)) & endpoints) == 1})
        available = set(supports)
        if any(len(set(neighbors(point)) & (endpoints | available)) < 3 for point in endpoints):
            continue
        for selection_mask in range(1 << len(supports)):
            selected = {point for index, point in enumerate(supports) if selection_mask >> index & 1}
            if any(set(neighbors(point)) & selected for point in selected):
                continue
            if all(len(set(neighbors(point)) & (endpoints | selected)) >= 3 for point in endpoints):
                yield rows+2+rows % 2, columns+2+columns % 2, selected, matchings[0]


def band_forcing(width):
    edges = [((4, width), (3, width)), ((2, width), (1, width))]
    edges += [((0 if column % 2 == 0 else 1, column),
               (0 if column % 2 == 0 else 1, column-1)) for column in range(width, 1, -1)]
    other = [((4, 1), (3, 1)), ((2, 1), (1, 1))]
    other += [((0 if column % 2 else 1, column),
               (0 if column % 2 else 1, column+1)) for column in range(1, width)]
    edges += [tuple((4-row, column-width) for row, column in edge) for edge in other]
    edges += [((0, 0), (1, 0)), ((1, 1), (2, 1)),
              ((2, 0), (3, 0)), ((3, 1), (4, 1))]
    return [tuple((row+2, column+width) for row, column in edge) for edge in edges]


def band_tiles(width):
    records = {(2, -width//2): (1, 1, 1, 0), (2, width//2): (1, 2, 1, 0),
               (0, -width//2): (2, 1, 1, 0), (1, -width//2): (2, 1, 1, 0),
               (0, width//2): (2, 1, 2, 1), (1, width//2): (2, 1, 2, 1),
               (2, 0): (2, 1, 2, 1), (1, 0): (4, 0, 3, 3)}
    for column in range(-width//2+1, 0):
        records[1, column] = 2, 0, 1, 0
        records[2, column] = 2, 0, 2, 1
    for column in range(width//2):
        records[0, column] = 4, 0, 3, 3
    return {(row+1, column+width//2): profile for (row, column), profile in records.items()}


def check_band(width, totals):
    current = occupied_bands(width)[0]
    endpoints = {point for edge in current[3] for point in edge}
    remaining = set(endpoints)
    forced = band_forcing(width)
    for leaf, mate in forced:
        assert set(neighbors(leaf)) & remaining == {mate}
        remaining -= {leaf, mate}
    assert not remaining and canonical(forced) == canonical(current[3])
    totals['band_forced_edges'] += len(forced)
    earlier = set()
    mate = {first: second for edge in current[3] for first, second in (edge, edge[::-1])}
    for point, first, second in occupied_band_certificate(width):
        assert point in endpoints-earlier and first != second
        assert {first, second} <= set(neighbors(point)) and mate[point] not in {first, second}
        assert all(other in current[2] or other in mate and mate[other] in earlier for other in (first, second))
        earlier.add(point)
    assert earlier == endpoints
    owner = {point: index for index, edge in enumerate(current[3]) for point in edge}
    expected = band_tiles(width)
    assert set(expected) == {(row//2, column//2) for row, column in endpoints}
    for tile, profile in expected.items():
        cells = vertices_of({tile})
        local = cells & endpoints
        cross = sum(point < other and owner[point] != owner[other]
                    for point in local for other in set(neighbors(point)) & local)
        assert profile == (len(local), len(cells & current[2]), len({owner[point] for point in local}), cross)
    record = inspect(current, totals)
    assert record['blocks'] == 2*width+6 and record['flexible_blocks'] == 0
    assert record['buffer'] == 4*width+3 and record['interface_weight'] == 4*width+7
    assert record['mixed_full_tiles'] == width//2+1 and record['receiver_charge'] == 2-width
    assert record['exchange_terminal']
    totals['band_widths'] += 1
    return record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    cases = [fixture(), graft(6, 4), graft(10, 8), charge_two()[0], elbow(6, 4)]
    cases += [shifted(straight_comb(size), 0, 1) for size in (1, 3, 8)]
    for current in cases:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            inspect((*shape, selected, matching), totals)
    band_phase_images = 0
    for width in (6, 10, 20):
        for phase in itertools.product((0, 1), repeat=2):
            current = shifted(occupied_bands(width)[0], *phase)
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                record = inspect((*shape, selected, matching), totals)
                assert record['flexible_blocks'] == 0 and record['exchange_terminal']
                band_phase_images += 1
    domain_models = 0
    for current in small_models(3, 4):
        inspect(current, totals)
        domain_models += 1
    band_records = {}
    for width in range(6, 101, 2):
        record = check_band(width, totals)
        if width in (6, 8, 20, 100):
            band_records[str(width)] = record
    positive = inspect(graft(6, 4), totals)
    assert positive['buffer'] == 21 and positive['interface_weight'] == 28
    assert positive['mixed_full_tiles'] == 3 and positive['receiver_charge'] == 1
    assert positive['blocks'] == 15 and positive['flexible_blocks'] == 1
    assert max(positive['block_charges']) == 0 and positive['exchange_terminal']
    assert domain_models == 1086 and totals['separated_block_models'] >= 24
    report = dict(status='PASS', controls=dict(totals), endpoint_box=[3, 4],
                  endpoint_box_models=domain_models, fixture_symmetries=8*len(cases),
                  band_phase_symmetry_controls=band_phase_images,
                  band_width_range=[6, 100, 2], band_records=band_records,
                  omitted_interface_counterexample=positive,
                  scope='Finite validation of written tile connectivity, block nonpositivity, '
                        'exact accounting and the all-width occupied-band forcing proof. '
                        'No unrestricted compensation inequality or new global coefficient claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('band_records', 'omitted_interface_counterexample')}, indent=2))


if __name__ == '__main__':
    main()
