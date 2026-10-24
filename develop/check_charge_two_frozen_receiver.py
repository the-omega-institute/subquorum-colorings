"""Independent physical and ordered-proof checks for the frozen charge-two receiver."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed
from search_corner_coverage import witnesses


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def fixture():
    source = json.loads(Path(__file__).with_name('charge_two_frozen_receiver.json').read_text())
    current = (*source['shape'], {tuple(point) for point in source['selected']},
               [tuple(tuple(point) for point in edge) for edge in source['matching']])
    certificate = [tuple(tuple(point) for point in row) for row in source['freezing_certificate']]
    return current, certificate


def inspect(current, certificate=None):
    objective = direct_check(*current)
    endpoints = endpoint_data(current)[0]
    assert endpoint_components(current) == [endpoints]
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
    checked = verify_terminal(current)
    receiver = checked['receivers'][0]
    assert (len(current[2]), len(current[3]), len(endpoints)) == (20, 19, 38)
    assert (receiver['tiles'], receiver['selected'], receiver['charge_twice']) == (17, 17, 4)
    tiles = {(row//2, column//2) for row, column in endpoints}
    cells = vertices_of(tiles)
    assert len(cells-current[2]-endpoints) == 13
    inventory = Counter((len(vertices_of({tile}) & endpoints),
                         len(vertices_of({tile}) & current[2])) for tile in tiles)
    assert inventory == {(1, 2): 6, (2, 1): 5, (3, 0): 2, (4, 0): 4}
    graph, _ = graph_record(*current)
    original_twice = sum(graph['deg'][row*(current[1]//2)+column]
                         -2*graph['r'][row*(current[1]//2)+column]
                         for row, column in tiles
                         if graph['t'][row*(current[1]//2)+column] < 2)
    assert original_twice == 4
    for point in cells-current[2]-endpoints:
        assert len(set(neighbors(point)) & endpoints) >= 2 or any(
            set(neighbors(support)) & endpoints for support in set(neighbors(point)) & current[2])
    donor_tiles = {tuple(coordinate//2 for coordinate in witness['square'])
                   for witness in witnesses(*current[:2], current[2], endpoints)}
    donor_records = []
    for tile in sorted(donor_tiles):
        donor_cells = vertices_of({tile})
        assert not donor_cells & endpoints and tile not in tiles
        deficit = 2-len(donor_cells & current[2])
        assert deficit >= 1
        donor_records.append(dict(tile=tile, deficit=deficit))
    assert len(donor_tiles) == 4
    assert sorted(record['deficit'] for record in donor_records) == [1, 1, 1, 2]
    assert sum(record['deficit'] for record in donor_records) == 5
    if certificate is not None:
        assert donor_tiles == {(1, 1), (3, 0), (3, 3), (5, 1)}
        assert len(vertices_of({(1, 1)}) & current[2]) == 1
        assert len(vertices_of({(3, 3)}) & current[2]) == 1
    return dict(shape=current[:2], endpoints=len(endpoints), matching_edges=len(current[3]),
                selected=len(current[2]), receiver_tiles=len(tiles), selected_in_receiver=17,
                blanks_in_receiver=13, corrected_charge_twice=original_twice,
                saturated_endpoint_transfers=receiver['transfers'],
                occupied_degrees=dict(sorted(Counter(occupied_degrees(current).values()).items())),
                freezing_layer_sizes=[len(layer) for layer in layers],
                ordered_certificate_steps=len(certificate) if certificate is not None else None,
                distinct_capped_donors=donor_records, actual_owned_capacity=5,
                guaranteed_owned_units=4,
                objective=objective, no_endpoint_deficit=checked['empty_deficit'],
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
    report.update(status='PASS', symmetry_images=8,
                  scope='Complete explicit frozen charge-two counterexample to the whole-receiver '
                        'ceiling; ordered freezing is a general exclusion proof for arbitrary '
                        'mixed bundles, not exhaustive bundle enumeration. Four distinct capped '
                        'donor tiles are deduplicated before adding physical capacities. '
                        'The coefficient-one grid inequality is not refuted.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
