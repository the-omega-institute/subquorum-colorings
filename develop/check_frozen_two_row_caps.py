"""Check the all-length fully frozen two-row capped-ladder obstruction."""

import argparse
import itertools
import json
from pathlib import Path

from check_bipartite_promotion import verify as verify_bundle_completeness
from check_cooperative_promotion import neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def capped_ladder(width):
    assert width >= 3
    right_row = width % 2
    outside = lambda row: -1 if row == 0 else 2
    selected = {(-1, -1), (0, -2), (2, 0), (outside(right_row), width),
                (right_row, width+1), (outside(1-right_row), width-1)}
    matching = [((0, -1), (0, 0))]
    matching += [((index % 2, index-1), (index % 2, index))
                 for index in range(1, width+1)]
    move = lambda vertex: (vertex[0]+2, vertex[1]+2)
    return (6, 2*((width+5)//2), {move(vertex) for vertex in selected},
            [(move(first), move(second)) for first, second in matching])


def verify(current, width):
    assert direct_check(*current) == width+7
    endpoints, adjacency, squares = endpoint_data(current)
    assert len(current[2]) == 6 and len(current[3]) == width+1
    assert len(endpoints) == 2*width+2 and len(squares) == width-1
    assert {row for row, _ in endpoints} == {2, 3}
    pending = [next(iter(endpoints))]
    reached = set(pending)
    while pending:
        vertex = pending.pop()
        added = adjacency[vertex]-reached
        reached.update(added)
        pending.extend(added)
    assert reached == endpoints
    assert set(occupied_degrees(current).values()) == {3}
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints and [len(layer) for layer in layers] == [2]*(width+1)
    mates = {vertex: partner for first, second in current[3]
             for vertex, partner in ((first, second), (second, first))}
    wave = [(2, 1)]+[(3 if index % 2 else 2, index+1) for index in range(1, width+1)]
    assert len(wave) == width+1 and len(set(wave)) == width+1
    assert len(set(neighbors(wave[0])) & current[2]) == 2
    assert mates[wave[0]] in neighbors(wave[1])
    assert len(set(neighbors(wave[1])) & current[2]) == 1
    for index in range(width-1):
        first, second = mates[wave[index]], mates[wave[index+1]]
        assert first != second and {first, second} <= set(neighbors(wave[index+2]))
    reflected = {(5-row if width % 2 else row, width+3-column) for row, column in wave}
    assert set(wave).isdisjoint(reflected) and set(wave) | reflected == endpoints
    occupied = current[2] | endpoints
    checked = verify_bundle_completeness(current[2], current[3],
        {vertex: set(neighbors(vertex)) & occupied for vertex in occupied},
        {vertex: sum(vertex) % 2 for vertex in occupied}, exhaustive=width <= 8)
    receiver = {(row//2, column//2) for row, column in endpoints}
    assert len(receiver) == width//2+2
    receiver_vertices = {(2*row+local_row, 2*column+local_column)
                         for row, column in receiver
                         for local_row, local_column in itertools.product((0, 1), repeat=2)}
    forced_blanks = receiver_vertices-occupied
    assert len(forced_blanks) == 4-width % 2
    for vertex in forced_blanks:
        adjacent = set(neighbors(vertex))
        assert adjacent & current[2] or len(adjacent & endpoints) >= 2
    graph, _ = graph_record(*current)
    charge_twice = []
    for tile_row, tile_column in sorted(receiver):
        tile = tile_row*(current[1]//2)+tile_column
        present = sum((2*tile_row+row, 2*tile_column+column) in endpoints
                      for row, column in itertools.product((0, 1), repeat=2))
        assert graph['s'][tile] == 0
        if present == 4:
            assert tuple(graph[key][tile] for key in ('t', 'h', 'r', 'deg')) == (0, 1, 1, 2)
        elif present == 1:
            assert present == 1
            assert tuple(graph[key][tile] for key in ('t', 'h', 'r', 'deg')) == (1, 0, 1, 1)
        else:
            assert width % 2 and present == 3
            assert tuple(graph[key][tile] for key in ('t', 'h', 'r', 'deg')) == (0, 1, 1, 1)
        charge_twice.append(graph['deg'][tile]-2*graph['r'][tile])
    assert sorted(charge_twice) == [-1, -1]+[0]*(width//2)
    assert sum(charge_twice) == -2
    return dict(width=width, selected=6, matching_edges=width+1, endpoints=2*width+2,
                endpoint_squares=width-1, aligned_endpoint_squares=width//2,
                receiver_tiles=len(receiver), receiver_charge_twice=-2,
                receiver_forced_blanks=len(forced_blanks),
                frozen_layer_sizes=[2]*(width+1), **checked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    symmetry_images = 0
    for width in range(3, 65):
        current = capped_ladder(width)
        records.append(verify(current, width))
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            image = (*shape, selected, matching)
            assert direct_check(*image) == width+7
            endpoints, _, squares = endpoint_data(image)
            assert len(squares) == width-1 and frozen_certificate(image)[0] == endpoints
            graph, _ = graph_record(*image)
            receiver = {(row//2, column//2) for row, column in endpoints}
            assert sum(graph['deg'][row*(shape[1]//2)+column]
                       -2*graph['r'][row*(shape[1]//2)+column]
                       for row, column in receiver) == -2
            symmetry_images += 1
    smallest = capped_ladder(3)
    oracle = (4, 7, {(0, 1), (1, 0), (0, 4), (3, 2), (3, 5), (2, 6)},
              [((1, 1), (1, 2)), ((1, 3), (1, 4)),
               ((2, 2), (2, 3)), ((2, 4), (2, 5))])
    assert direct_check(*oracle) == 10
    oracle_endpoints, _, oracle_squares = endpoint_data(oracle)
    assert len(oracle_squares) == 2 and len(oracle_endpoints) == 8
    assert frozen_certificate(oracle)[0] == oracle_endpoints
    oracle_occupied = oracle[2] | oracle_endpoints
    oracle_checked = verify_bundle_completeness(oracle[2], oracle[3],
        {vertex: set(neighbors(vertex)) & oracle_occupied for vertex in oracle_occupied},
        {vertex: sum(vertex) % 2 for vertex in oracle_occupied})
    assert oracle_checked['feasible_choices'] == 1 and oracle_checked['layers'] == 4
    report = dict(status='ALL_CHECKS_PASSED', family_cases=len(records),
                  symmetry_images=symmetry_images, family=records,
                  smallest=dict(shape=smallest[:2], selected=sorted(smallest[2]),
                                matching=smallest[3], nonempty_oriented_bundles=80,
                                feasible_nonempty_bundles=0),
                  original_oracle_obstacle=dict(shape=oracle[:2], selected=sorted(oracle[2]),
                                                matching=oracle[3], **oracle_checked),
                  refuted_claims=['Every complete endpoint component contained in two rows can normalize to a square-free endpoint graph.',
                                  'The endpoint-tile receiver of a frozen component pays a fixed positive amount per endpoint square.'],
                  global_grid_inequality_refuted=False,
                  scope='General proof uses two acyclic retained-mate waves and an exact original tile ledger; finite cases only verify implementation and fixtures.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'family'}))


if __name__ == '__main__':
    main()
