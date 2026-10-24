"""Check actual even-bridge completion, terminality and exact interface taxes."""

import argparse
from collections import Counter
import itertools
import json
import math
from pathlib import Path

from check_bounded_height_sharp_chains import chain
from check_component_receivers import endpoint_components, shifted, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_exchange_terminal_nonunique import fixture, graft
from check_flexible_block_entries import matching_blocks
from check_matching_block_tile_ledger import small_models
from check_promotion_cores import color_data, frozen_certificate, peel
from check_rematching_receiver_flux import canonical, perfect_matchings
from check_residual_corridors import direct_check, transformed
from degree_three_fusion import occupied_bands


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def endpoints_of(current):
    return {point for edge in current[3] for point in edge}


def tiles_of(points):
    return {(row//2, column//2) for row, column in points}


def bridge_cuts(endpoints):
    for first in sorted(endpoints):
        for second in sorted(set(neighbors(first)) & endpoints):
            if first >= second:
                continue
            reached = {first}
            pending = [first]
            while pending:
                point = pending.pop()
                for other in set(neighbors(point)) & endpoints:
                    if {point, other} == {first, second} or other in reached:
                        continue
                    reached.add(other)
                    pending.append(other)
            if second not in reached:
                yield first, second, reached, endpoints-reached


def completed(current, side, supports):
    selected = {point for point in current[2] if set(neighbors(point)) & side} | supports
    matching = [edge for edge in current[3] if edge[0] in side and edge[1] in side]
    result = *current[:2], selected, matching
    assert endpoints_of(result) == side
    direct_check(*result)
    assert occupied_degrees(result) == {point: occupied_degrees(current)[point] for point in side}
    return result


def ledger(current, totals):
    endpoints = endpoints_of(current)
    matchings = list(perfect_matchings(endpoints))
    assert matchings
    blocks, owner, allowed = matching_blocks(endpoints, matchings)
    tiles = tiles_of(endpoints)
    for tile in tiles:
        cells = vertices_of({tile})
        for point in current[2] & cells:
            assert len(set(neighbors(point)) & endpoints & cells) == 1
            totals['tile_anchor_checks'] += 1
    charges = [len(block)//2+sum(len(current[2] & vertices_of({tile}))-2
                                for tile in tiles_of(block)) for block in blocks]
    interface = mixed = 0
    for tile in tiles:
        cells = vertices_of({tile})
        local = endpoints & cells
        cross = sum(point < other and owner[point] != owner[other]
                    for point in local for other in set(neighbors(point)) & local)
        interface += (2-len(current[2] & cells))*cross
        mixed += int(len(local) == 4 and len({owner[point] for point in local}) > 1)
    charge = len(endpoints)//2+sum(len(current[2] & vertices_of({tile}))-2 for tile in tiles)
    assert charge == interface-2*mixed+sum(charges)
    terminal = True
    for matching in matchings:
        candidate = *current[:3], matching
        frozen = frozen_certificate(candidate)[0] == endpoints
        empty_cores = all(not peel(*color_data(candidate, color)[1:])[0] for color in (0, 1))
        assert frozen == empty_cores
        terminal &= frozen
    if terminal:
        assert max(charges, default=0) <= 0
    totals['ledger_models'] += 1
    totals['matching_terminal_checks'] += len(matchings)
    return dict(charge=charge, interface=interface, buffer=-sum(charges), mixed=mixed,
                terminal=terminal, matchings={frozenset(canonical(matching)) for matching in matchings},
                blocks={frozenset(block) for block in blocks}, owner=owner, allowed=allowed)


def inspect(current, totals, profiles, examples):
    direct_check(*current)
    assert min(occupied_degrees(current).values()) >= 3
    for component in endpoint_components(current):
        base = completed(current, component, set())
        original = ledger(base, totals)
        for first, second, left, right in bridge_cuts(component):
            if len(left) % 2:
                assert all(tuple(sorted((first, second))) in matching for matching in original['matchings'])
                totals['odd_bridge_checks'] += 1
                continue
            first_pair = completed(base, left, {second})
            second_pair = completed(base, right, {first})
            first_record = ledger(first_pair, totals)
            second_record = ledger(second_pair, totals)
            assert original['matchings'] == {first_matching | second_matching
                                            for first_matching in first_record['matchings']
                                            for second_matching in second_record['matchings']}
            assert original['blocks'] == first_record['blocks'] | second_record['blocks']
            assert original['terminal'] == (first_record['terminal'] and second_record['terminal'])
            assert original['charge'] == first_record['charge']+second_record['charge']
            shared = tiles_of(left) & tiles_of(right)
            intratile = (first[0]//2, first[1]//2) == (second[0]//2, second[1]//2)
            assert len(shared) == int(intratile)
            correction = 0
            profile = 'intertile'
            if intratile:
                cells = vertices_of(shared)
                count = len(component & cells)
                selected = len(base[2] & cells)
                assert count in (2, 3)
                if count == 2:
                    assert selected == 1
                    correction = 2-selected
                    profile = f'two-endpoint-t{selected}'
                else:
                    assert selected == 0
                    internal = [(point, other) for point in component & cells
                                for other in set(neighbors(point)) & component & cells
                                if point < other and (point in left) == (other in left)]
                    assert len(internal) == 1
                    source, target = internal[0]
                    cross_block = int(original['owner'][source] != original['owner'][target])
                    correction = 2+cross_block
                    profile = f'three-endpoint-h{cross_block}'
            assert original['mixed'] == first_record['mixed']+second_record['mixed']
            for name in ('interface', 'buffer'):
                assert original[name] == first_record[name]+second_record[name]+correction
            profiles[profile] += 1
            if profile not in examples:
                examples[profile] = dict(shape=list(base[:2]), selected=sorted(base[2]),
                                         matching=base[3], bridge=[first, second], correction=correction)
            totals['even_bridge_cuts'] += 1
            totals['terminal_even_bridge_cuts' if original['terminal'] else 'nonterminal_even_bridge_cuts'] += 1
    totals['input_models'] += 1


def check_full_split(current, totals):
    original = ledger(current, totals)
    endpoints = endpoints_of(current)
    removed = {(first, second) for first, second, side, _ in bridge_cuts(endpoints) if len(side) % 2 == 0}
    remaining = set(endpoints)
    pieces = []
    while remaining:
        start = min(remaining)
        reached = {start}
        pending = [start]
        while pending:
            point = pending.pop()
            for other in set(neighbors(point)) & endpoints:
                if tuple(sorted((point, other))) in removed or other in reached:
                    continue
                reached.add(other)
                pending.append(other)
        remaining -= reached
        supports = {other for point in reached for other in set(neighbors(point)) & (endpoints-reached)}
        pair = completed(current, reached, supports)
        record = ledger(pair, totals)
        assert all(len(side) % 2 for _, _, side, _ in bridge_cuts(reached))
        pieces.append(record)
    assert sum(piece['charge'] for piece in pieces) == original['charge']
    assert all(piece['terminal'] for piece in pieces) == original['terminal']
    assert len(original['matchings']) == math.prod(len(piece['matchings']) for piece in pieces)
    totals['full_split_models'] += 1
    totals['full_split_pieces'] += len(pieces)
    return dict(original_charge=original['charge'], completed_charges=[piece['charge'] for piece in pieces])


def negative_controls():
    odd = 4, 4, {(0, 1), (1, 0), (2, 2), (1, 3)}, [((1, 1), (1, 2))]
    direct_check(*odd)
    assert set(occupied_degrees(odd).values()) == {3}
    cuts = list(bridge_cuts(endpoints_of(odd)))
    assert len(cuts) == 1 and len(cuts[0][2]) == 1
    square = {(1, 1), (1, 2), (2, 1), (2, 2)}
    selected = {(0, 1), (1, 3), (3, 2), (2, 0)}
    matching = [((1, 1), (2, 1)), ((1, 2), (2, 2))]
    original = 4, 4, selected, matching
    direct_check(*original)
    assert set(occupied_degrees(original).values()) == {3}
    assert not list(bridge_cuts(square))
    failed = 0
    for column in (1, 2):
        side = {point for point in square if point[1] == column}
        native = {point for point in selected if set(neighbors(point)) & side}
        try:
            direct_check(4, 4, native | (square-side), [edge for edge in matching if edge[0] in side])
        except AssertionError:
            failed += 1
    assert failed == 2
    return dict(odd_forced_bridge=True, nonbridge_completed_sides_infeasible=failed)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    totals, profiles, examples = Counter(), Counter(), {}
    for current in small_models(3, 4):
        inspect(current, totals, profiles, examples)
    assert totals['input_models'] == 1086
    domain_cuts = totals['even_bridge_cuts']
    cases = [fixture(), graft(6, 4), graft(10, 8), elbow(6, 4), occupied_bands(6)[0]]
    cases += [chain(choices) for count in range(1, 5)
              for choices in itertools.product((0, 1), repeat=count)]
    for current in cases:
        inspect(current, totals, profiles, examples)
        check_full_split(current, totals)
    for current in (graft(6, 4), chain((0, 1, 0)), occupied_bands(6)[0]):
        for phase in itertools.product((0, 1), repeat=2):
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*shifted(current, *phase), *symmetry)
                image = *shape, selected, matching
                inspect(image, totals, profiles, examples)
                check_full_split(image, totals)
    positive = check_full_split(graft(6, 4), totals)
    assert positive['original_charge'] == 1
    assert sorted(positive['completed_charges']) == [0, 1]
    branches = {'intertile', 'two-endpoint-t1',
                'three-endpoint-h0', 'three-endpoint-h1'}
    assert set(profiles) == branches
    report = dict(status='PASS', controls=dict(totals), endpoint_box_models=1086,
                  endpoint_box_even_cuts=domain_cuts, correction_profiles=dict(profiles),
                  two_endpoint_t0_bridge_impossible=True,
                  correction_examples=examples, positive_graft=positive,
                  negative_controls=negative_controls(),
                  scope='Finite checks of the general written even-bridge completion theorem; '
                        'not a proof by enumeration or an unrestricted compensation inequality.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'correction_examples'}, indent=2))


if __name__ == '__main__':
    main()
