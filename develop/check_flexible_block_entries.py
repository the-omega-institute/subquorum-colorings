"""Validate flexible-block reductions using independently enumerated matchings."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_charge_two_frozen_receiver import fixture as charge_two
from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_exchange_terminal_nonunique import fixture, graft
from check_promotion_cores import feasible_bundle, frozen_certificate
from check_rematching_receiver_flux import perfect_matchings
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def matching_blocks(endpoints, matchings):
    allowed = {point: set() for point in endpoints}
    for matching in matchings:
        for first, second in matching:
            allowed[first].add(second)
            allowed[second].add(first)
    blocks = []
    unseen = set(endpoints)
    while unseen:
        pending = [min(unseen)]
        block = set()
        while pending:
            point = pending.pop()
            if point in block:
                continue
            block.add(point)
            pending.extend(allowed[point]-block)
        unseen -= block
        blocks.append(block)
    owner = {point: index for index, block in enumerate(blocks) for point in block}
    for point in endpoints:
        assert all(owner[other] != owner[point] or other in allowed[point]
                   for other in set(neighbors(point)) & endpoints)
    return blocks, owner, allowed


def inspect(current, totals):
    direct_check(*current)
    endpoints = {point for edge in current[3] for point in edge}
    degrees = occupied_degrees(current)
    assert all(degree >= 3 for degree in degrees.values())
    matchings = list(perfect_matchings(endpoints))
    assert matchings
    blocks, owner, allowed = matching_blocks(endpoints, matchings)
    flexible = {index for index, block in enumerate(blocks) if len(block) > 2}
    two_selected = [point for point in endpoints if owner[point] in flexible
                    and len(set(neighbors(point)) & current[2]) >= 2]
    for point in two_selected:
        adjacent = sorted(set(neighbors(point)) & endpoints)
        assert len(adjacent) == 2 and len(allowed[point]) == 2
        assert sum(abs(adjacent[0][axis]-adjacent[1][axis]) for axis in (0, 1)) == 2
        assert adjacent[0][0] != adjacent[1][0] and adjacent[0][1] != adjacent[1][1]
        fourth = tuple(sum(other[axis] for other in adjacent)-point[axis] for axis in (0, 1))
        assert fourth in endpoints and owner[fourth] == owner[point]
        witnesses = []
        for matching in matchings:
            mate = {first: second for edge in matching for first, second in (edge, edge[::-1])}
            if {mate[other] for other in adjacent} == {point, fourth}:
                assert feasible_bundle((*current[:3], matching), [(other, mate[other]) for other in adjacent])
                witnesses.append(matching)
        assert witnesses
        totals['two_selection_witnesses'] += 1
    frozen_records = [frozen_certificate((*current[:3], matching)) for matching in matchings]
    exchange_terminal = all(frozen == endpoints for frozen, _ in frozen_records)
    totals['models'] += 1
    totals['matchings'] += len(matchings)
    if not exchange_terminal:
        totals['nonterminal_models'] += 1
        return
    totals['exchange_terminal_models'] += 1
    totals['flexible_blocks'] += len(flexible)
    assert not two_selected
    incoming = {index: set() for index in range(len(blocks))}
    outgoing = {index: set() for index in range(len(blocks))}
    for point in endpoints:
        if sum(point) % 2:
            continue
        for other in set(neighbors(point)) & endpoints:
            if owner[point] != owner[other]:
                outgoing[owner[point]].add(owner[other])
                incoming[owner[other]].add(owner[point])
    for index, block in enumerate(blocks):
        for color, boundary in ((1, incoming), (0, outgoing)):
            if boundary[index]:
                continue
            assert len(block) == 2
            leaf = next(point for point in block if sum(point) % 2 == color)
            assert len(set(neighbors(leaf)) & endpoints) == 1
            selected = set(neighbors(leaf)) & current[2]
            assert len(selected) == 2 and degrees[leaf] == 3
            first, second = sorted(selected)
            assert first[0] != second[0] and first[1] != second[1]
            assert all(degrees[point] == 3 for point in block)
            totals['forced_boundary_checks'] += 1
    for matching, (_, layers) in zip(matchings, frozen_records):
        mate = {first: second for edge in matching for first, second in (edge, edge[::-1])}
        earlier = set()
        seen = set()
        entries = set()
        for layer in layers:
            for row in layer:
                point = tuple(row['endpoint'])
                key = owner[point], sum(point) % 2
                if owner[point] in flexible and key not in seen:
                    internal = set(neighbors(point)) & blocks[owner[point]]
                    kept = current[2] | {mate[previous] for previous in earlier}
                    outside = set(neighbors(point)) & kept
                    assert degrees[point] == 4 and len(internal) == len(outside) == 2
                    assert not internal & outside and outside-endpoints <= current[2]
                    assert outside & endpoints
                    assert all(mate[other] in earlier for other in outside & endpoints)
                    seen.add(key)
                    entries.add(point)
                    totals['entry_checks'] += 1
                earlier.add(point)
        assert len(entries) == len(seen) == 2*len(flexible)
        assert all(degrees[point] == 4 for point in entries)
    assert 2*len(flexible) <= sum(degree == 4 for degree in degrees.values())


def endpoint_box(rows, columns, totals):
    points = list(itertools.product(range(1, rows+1), range(1, columns+1)))
    domain_models = 0
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
            if any(len(set(neighbors(point)) & (endpoints | selected)) < 3 for point in endpoints):
                continue
            inspect((rows+2, columns+2, selected, matchings[0]), totals)
            domain_models += 1
    return domain_models


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    unlockable = (6, 8, {(1, 2), (2, 1), (4, 2), (2, 5), (4, 4)},
                  [((2, column), (3, column)) for column in range(2, 5)])
    cases = [unlockable, charge_two()[0], fixture(), elbow(6, 4)]
    cases += [graft(width, height) for width, height in ((6, 4), (10, 8), (22, 18))]
    for current in cases:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            inspect((*shape, selected, matching), totals)
    domain_models = endpoint_box(3, 4, totals)
    assert totals['two_selection_witnesses'] >= 8
    assert totals['nonterminal_models'] >= 16
    assert totals['entry_checks'] >= 16
    report = dict(status='PASS', controls=dict(totals), fixture_symmetries=8*len(cases),
                  endpoint_box=[3, 4], endpoint_box_models=domain_models,
                  domain='Every nonempty endpoint subset in the stated box admitting a perfect '
                        'matching, and every feasible endpoint-adjacent support selection '
                        'with occupied endpoint degree at least three; one-site blank padding.',
                  scope='Finite controls of the written general proofs. No compensation '
                        'capacity, new grid bound, minimality or Lean verification claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
