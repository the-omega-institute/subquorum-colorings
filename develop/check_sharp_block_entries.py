"""Check sharp degree-four entry counts and complete finite freezing witnesses."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, shifted, verify_terminal
from check_cooperative_promotion import neighbors, occupied_degrees
from check_flexible_block_entries import matching_blocks
from check_promotion_cores import all_oriented_bundles, frozen_certificate
from check_rematching_receiver_flux import canonical, perfect_matchings
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


SELECTED = {(0, 1), (0, 3), (0, 6), (1, 0), (1, 7),
            (3, 6), (4, 0), (4, 5), (5, 1), (5, 3)}
FORCED = [((1, 1), (1, 2)), ((1, 6), (1, 5)), ((3, 5), (2, 5)),
          ((4, 1), (4, 2)), ((4, 3), (3, 3)), ((3, 2), (2, 2))]
SQUARE = [((1, 3), (1, 4)), ((2, 3), (2, 4))]


def fixture():
    return 6, 8, set(SELECTED), FORCED+SQUARE


def inspect(current, copies=1):
    assert direct_check(*current) == 18*copies
    endpoints = {point for edge in current[3] for point in edge}
    degrees = occupied_degrees(current)
    assert Counter(degrees.values()) == {3: 14*copies, 4: 2*copies}
    assert all(len(set(neighbors(point)) & (endpoints | current[2])) == 1 for point in current[2])
    matchings = list(perfect_matchings(endpoints))
    assert len(matchings) == 2**copies
    blocks, _, _ = matching_blocks(endpoints, matchings)
    assert Counter(map(len, blocks)) == {2: 6*copies, 4: copies}
    assert all(degrees[point] == 3 for block in blocks if len(block) == 2 for point in block)
    assert len(endpoint_components(current)) == copies
    records = []
    for matching in matchings:
        frozen, layers = frozen_certificate((*current[:3], matching))
        assert frozen == endpoints
        mate = {first: second for edge in matching for first, second in (edge, edge[::-1])}
        earlier = set()
        ordered = []
        for layer in layers:
            for row in layer:
                point = tuple(row['endpoint'])
                first, second = map(tuple, row['kept_neighbors'])
                assert first != second and {first, second} <= set(neighbors(point))
                assert mate[point] not in {first, second}
                assert all(other in current[2] or other in mate and mate[other] in earlier
                           for other in (first, second))
                earlier.add(point)
                ordered.append([point, first, second])
        assert earlier == endpoints
        records.append(dict(matching=matching, certificate=ordered))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    base = fixture()
    remaining = {point for edge in base[3] for point in edge}
    for leaf, mate in FORCED:
        assert set(neighbors(leaf)) & remaining == {mate}
        remaining -= {leaf, mate}
    assert remaining == {point for edge in SQUARE for point in edge}
    records = inspect(base)
    assert canonical(records[0]['matching']) != canonical(records[1]['matching'])
    oriented_bundles = 0
    for record in records:
        tested, feasible = all_oriented_bundles((*base[:3], record['matching']))
        assert feasible == 0
        oriented_bundles += tested
    phase_charges = {}
    images = 0
    for phase in itertools.product((0, 1), repeat=2):
        current = shifted(base, *phase)
        phase_charges[str(phase)] = sum(row['charge_twice']//2 for row in verify_terminal(current)['receivers'])
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            inspect((*shape, selected, matching))
            images += 1
    disjoint_controls = []
    for copies in range(1, 6):
        selected = {(row, column+10*index) for index in range(copies) for row, column in SELECTED}
        matching = [tuple((row, column+10*index) for row, column in edge)
                    for index in range(copies) for edge in base[3]]
        current = 6, 10*copies, selected, matching
        inspect(current, copies)
        ledger = verify_terminal(current)
        assert sum(row['charge_twice'] for row in ledger['receivers']) == 0
        assert ledger['area']//2-ledger['objective'] == 12*copies
        disjoint_controls.append(dict(copies=copies, flexible_blocks=copies,
                                      degree_four=2*copies, perfect_matchings=2**copies))
    report = dict(status='PASS', selected=sorted(SELECTED), forced_matching_order=FORCED,
                  matching_certificates=records, degree_four_endpoints=[(1, 3), (2, 3)],
                  forced_degree_four_endpoints=0, flexible_blocks=1,
                  oriented_nonempty_bundles_rejected=oriented_bundles,
                  phase_symmetry_controls=images, phase_charges=phase_charges,
                  disjoint_controls=disjoint_controls,
                  discovery='Z3 found the fixed witness after a satisfiable known-three-junction control. '
                            'The proof uses six forced pairs and both complete retained-neighbor transcripts, not solver completeness.',
                  scope='Sharpness of 2f<=j for general exchange-terminal pairs, and failure of '
                        'requiring an additional forced-block degree-four endpoint. The core is '
                        'charge zero; no positive-charge sharpness or new grid bound claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('matching_certificates', 'selected', 'forced_matching_order')}, indent=2))


if __name__ == '__main__':
    main()
