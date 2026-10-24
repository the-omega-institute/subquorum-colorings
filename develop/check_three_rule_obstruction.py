"""Physical and certificate checks for a receiver invisible to all three corner rules."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed
from owned_corner_witnesses import physical_donors
from search_corner_coverage import corner_patterns


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def fixture():
    source = json.loads(Path(__file__).with_name('three_rule_frozen_obstruction.json').read_text())
    current = (*source['shape'], {tuple(point) for point in source['selected']},
               [tuple(tuple(point) for point in edge) for edge in source['matching']])
    certificate = [tuple(tuple(point) for point in row) for row in source['freezing_certificate']]
    return current, certificate


def inspect(current, certificate=None):
    endpoints, adjacency, _ = endpoint_data(current)
    assert (len(endpoints), len(current[2]), len(current[3])) == (22, 14, 11)
    assert endpoint_components(current) == [endpoints]
    assert all(len(set(neighbors(point)) & endpoints) == 1 for point in current[2])
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    if certificate is not None:
        mates = {point: partner for edge in current[3] for point, partner in (edge, edge[::-1])}
        earlier = set()
        for vertex, first, second in certificate:
            assert vertex in endpoints-earlier and first != second
            assert {first, second} <= set(neighbors(vertex))
            assert mates[vertex] not in {first, second}
            for retained in (first, second):
                assert retained in current[2] or retained in mates and mates[retained] in earlier
            earlier.add(vertex)
        assert earlier == endpoints
    ledger = verify_terminal(current)
    receiver = ledger['receivers'][0]
    assert (receiver['tiles'], receiver['selected'], receiver['charge_twice']) == (10, 10, 2)
    assert physical_donors(current) == []
    assert physical_donors(current, include_endpoint_guard=True) == []
    candidates = []
    for top, left in itertools.product(range(0, current[0], 2), range(0, current[1], 2)):
        for required, support, _ in corner_patterns(top, left):
            if set(required[:4]) <= endpoints:
                assert required[4] not in endpoints or support not in current[2]
                candidates.append((top, left))
    assert len(candidates) == 14
    degrees = Counter(occupied_degrees(current).values())
    assert degrees == {3: 18, 4: 4}
    return dict(shape=current[:2], endpoints=22, selected=14, matching_edges=11,
                receiver_tiles=10, selected_in_receiver=10, blanks_in_receiver=8,
                original_corrected_charge_twice=2, occupied_degrees=dict(sorted(degrees.items())),
                geometric_degree_four=[point for point in sorted(endpoints) if len(adjacency[point]) == 4],
                freezing_layer_sizes=[len(layer) for layer in layers],
                ordered_freezing_steps=22, capped_extended_side_candidates=len(candidates),
                original_two_rule_capacity=0, extended_three_rule_capacity=0,
                objective=ledger['objective'], no_endpoint_deficit=ledger['empty_deficit'],
                whole_grid_deficit=current[0]*current[1]//2-ledger['objective'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    current, certificate = fixture()
    report = inspect(current, certificate)
    for padding in (0, 2):
        move = lambda point: (point[0]+padding, point[1]+padding)
        padded = (current[0]+2*padding, current[1]+2*padding,
                  {move(point) for point in current[2]},
                  [tuple(move(point) for point in edge) for edge in current[3]])
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*padded, *symmetry)
            inspect((*shape, selected, matching))
    report.update(status='PASS', physical_symmetries=8, padded_symmetries=8,
                  scope='Explicit frozen counterexample to universal coverage by capped, '
                        'selected-guarded and same-component two-endpoint-guarded donors. '
                        'The conditional compensation theorems remain valid. '
                        'The grid target is not refuted. No new Lean claim for this22endpoint example.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
