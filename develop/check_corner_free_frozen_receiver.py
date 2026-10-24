"""Independent certificate and local-donor checks for a frozen degree-three obstruction."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from owned_corner_witnesses import physical_donors


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def fixture():
    source = json.loads(Path(__file__).with_name('corner_free_frozen_receiver.json').read_text())
    current = (*source['shape'], {tuple(point) for point in source['selected']},
               [tuple(tuple(point) for point in edge) for edge in source['matching']])
    certificate = [tuple(tuple(point) for point in row) for row in source['freezing_certificate']]
    return current, certificate


def inspect(current, certificate=None):
    objective = direct_check(*current)
    endpoints = endpoint_data(current)[0]
    assert (len(endpoints), len(current[2]), len(current[3])) == (20, 12, 10)
    assert endpoint_components(current) == [endpoints]
    assert set(occupied_degrees(current).values()) == {3}
    assert all(len(set(neighbors(point)) & endpoints) == 1 for point in current[2])
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints and [len(layer) for layer in layers] == [2]*10
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
    assert (receiver['tiles'], receiver['selected'], receiver['charge_twice']) == (9, 9, 2)
    tiles = {(row//2, column//2) for row, column in endpoints}
    inventory = Counter((len(vertices_of({tile}) & endpoints),
                         len(vertices_of({tile}) & current[2])) for tile in tiles)
    assert len(vertices_of(tiles)-endpoints-current[2]) == 7
    assert physical_donors(current) == []
    extended = physical_donors(current, include_endpoint_guard=True)
    assert any(record['endpoint_guarded'] for record in extended)
    return dict(shape=current[:2], objective=objective, endpoints=20, selected=12,
                matching_edges=10, receiver_tiles=9, selected_in_receiver=9,
                blanks_in_receiver=7, original_corrected_charge_twice=2,
                occupied_degree=3, freezing_layer_sizes=[2]*10,
                original_owned_capacity=0, extended_donors=extended,
                no_endpoint_deficit=ledger['empty_deficit'],
                whole_grid_deficit=current[0]*current[1]//2-objective,
                receiver_inventory=[dict(endpoints=paired, selected=selected, tiles=number)
                                    for (paired, selected), number in sorted(inventory.items())])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    current, certificate = fixture()
    report = inspect(current, certificate)
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, *symmetry)
        inspect((*shape, selected, matching))
    padded = (current[0]+4, current[1]+4,
              {(row+2, column+2) for row, column in current[2]},
              [tuple((row+2, column+2) for row, column in edge) for edge in current[3]])
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*padded, *symmetry)
        inspect((*shape, selected, matching))
    report.update(status='PASS', physical_symmetries=8, padded_symmetries=8,
                  scope='Explicit frozen occupied-degree-three counterexample to universal '
                        'coverage by capped and selected-guarded corners. A same-component '
                        'two-endpoint guard supplies a distinct unit here; universal extended '
                        'coverage and the global grid target are not proved.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
