"""Check a frozen receiver with no slack in any neighboring endpoint-free tile."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import transformed
from check_two_leg_corner_obstruction import saturated_endpoint_donors
from owned_corner_witnesses import physical_donors


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def fixture():
    source = json.loads(Path(__file__).with_name('remote_deficit_frozen_obstruction.json').read_text())
    current = (*source['shape'], {tuple(point) for point in source['selected']},
               [tuple(tuple(point) for point in edge) for edge in source['matching']])
    certificate = [tuple(tuple(point) for point in row) for row in source['freezing_certificate']]
    return current, certificate


def inspect(current, certificate=None):
    endpoints = endpoint_data(current)[0]
    assert endpoint_components(current) == [endpoints]
    assert (len(endpoints), len(current[2]), len(current[3])) == (28, 25, 14)
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints
    if certificate is not None:
        mates = {point: partner for edge in current[3] for point, partner in (edge, edge[::-1])}
        earlier = set()
        for vertex, first, second in certificate:
            assert vertex in endpoints-earlier and first != second
            assert {first, second} <= set(neighbors(vertex))
            assert mates[vertex] not in {first, second}
            assert all(point in current[2] or point in mates and mates[point] in earlier
                       for point in (first, second))
            earlier.add(vertex)
        assert earlier == endpoints
    ledger = verify_terminal(current)
    receiver = ledger['receivers'][0]
    assert (receiver['tiles'], receiver['selected'], receiver['charge_twice']) == (12, 11, 2)
    assert (ledger['objective'], ledger['empty_deficit']) == (39, 2)
    assert Counter(occupied_degrees(current).values()) == {3: 23, 4: 5}
    receiver_tiles = {(row//2, column//2) for row, column in endpoints}
    no_endpoint_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))-receiver_tiles
    records = []
    for tile in sorted(no_endpoint_tiles):
        cells = vertices_of({tile})
        edge_distance = min(sum(abs(first-second) for first, second in zip(tile, other))
                            for other in receiver_tiles)
        corner_distance = min(max(abs(first-second) for first, second in zip(tile, other))
                              for other in receiver_tiles)
        vertex_distance = min(sum(abs(first-second) for first, second in zip(point, endpoint))
                              for point in cells for endpoint in endpoints)
        records.append(dict(tile=tile, deficit=2-len(cells & current[2]),
                            edge_tile_distance=edge_distance, corner_tile_distance=corner_distance,
                            vertex_distance=vertex_distance))
    positive = [record for record in records if record['deficit'] > 0]
    assert len(positive) == 1 and positive[0]['deficit'] == 2
    assert (positive[0]['edge_tile_distance'], positive[0]['corner_tile_distance'],
            positive[0]['vertex_distance']) == (2, 2, 3)
    assert sum(record['deficit'] for record in records if record['corner_tile_distance'] == 1) == 0
    assert physical_donors(current, include_endpoint_guard=True) == []
    assert saturated_endpoint_donors(current) == []
    return dict(receiver=receiver, objective=39, half_area=40, total_deficit=1,
                no_endpoint_deficit=2, adjacent_or_corner_touching_capacity=0,
                all_four_corner_rule_capacity=0, occupied_degrees={3: 23, 4: 5},
                freezing_steps=len(endpoints), freezing_layer_sizes=[len(layer) for layer in layers],
                no_endpoint_tiles=records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    current, certificate = fixture()
    report = inspect(current, certificate)
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, *symmetry)
        inspect((*shape, selected, matching))
    report.update(status='PASS', physical_symmetries=8,
                  scope='Explicit frozen 8-by-10 counterexample to compensation using only '
                        'endpoint-free tiles sharing an edge or corner with the receiver. '
                        'The sole positive deficit tile is at physical tile distance two. '
                        'The global bound holds with deficit one. Boundary is part of this '
                        'instance; no blank-padding invariance or new Lean verification claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'no_endpoint_tiles'}))


if __name__ == '__main__':
    main()
