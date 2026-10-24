"""Capacity-two rank bound and first separating-obstruction controls."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import vertices_of
from strip_incidence_allocation import maximum_run_allocation


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def array_records(rows, columns):
    tiles = list(itertools.product(range(rows), range(columns)))
    records = [dict(orientation='horizontal',
                    tiles=[tile for tile in tiles if tile[0] == row]) for row in range(rows)]
    records += [dict(orientation='vertical',
                     tiles=[tile for tile in tiles if tile[1] == column]) for column in range(columns)]
    return tiles, records


def inspect(records, residual):
    allocation = maximum_run_allocation(records, residual)
    rank = allocation['rank']
    capacity = sum(residual.values())
    if rank <= 1:
        assert capacity == rank
    else:
        assert capacity <= rank*rank//2
    for charge in range(1, min(3, capacity)+1):
        assert charge <= rank
    first = capacity >= 4 and rank < 4
    if first:
        assert rank == 3 and capacity == 4
        positive = [tile for tile, value in residual.items() if value]
        assert len(positive) == 2 and all(residual[tile] == 2 for tile in positive)
        assert positive[0][0] == positive[1][0] or positive[0][1] == positive[1][1]
        active = allocation['components']
        assert len(active) == 1
        assert len(active[0]['vertices']) == 3 and len(active[0]['slots']) == 4
    return rank, capacity, first


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    tiles, records = array_records(2, 3)
    first_patterns = []
    patterns = 0
    for capacities in itertools.product(range(3), repeat=len(tiles)):
        residual = dict(zip(tiles, capacities))
        rank, capacity, first = inspect(records, residual)
        if first:
            first_patterns.append(dict(positive_tiles=[tile for tile in tiles if residual[tile]],
                                       capacity=capacity, rank=rank))
        patterns += 1
    assert len(first_patterns) == 9
    sharpness = []
    for rank in range(2, 65):
        rows, columns = rank//2, (rank+1)//2
        tiles, records = array_records(rows, columns)
        actual_rank, capacity, _ = inspect(records, {tile: 2 for tile in tiles})
        assert actual_rank == rank and capacity == rank*rank//2
        sharpness.append(dict(rank=rank, tile_shape=[rows, columns], capacity=capacity,
                              physical_blank_vertices=len(vertices_of(set(tiles)))))
    report = dict(status='PASS', capacity_patterns=patterns,
                  first_obstruction_resource_patterns=first_patterns,
                  sharpness_cases=sharpness,
                  scope='Finite controls for separately written all-graph proofs. All '
                        '729 multiplicity-zero/one/two patterns on a two-by-three array '
                        'satisfy the quadratic bound and low-charge implication. '
                        'All nine first-resource shapes are two doubled edges at a shared '
                        'run. Blank rectangles attain the bound for ranks two through '
                        '64 but have receiver charge zero; they are not grid or '
                        'compensation counterexamples. No frozen charge-four example '
                        'or universal geometric coverage theorem is asserted.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], capacity_patterns=patterns,
                         first_resource_patterns=len(first_patterns),
                         sharpness_cases=len(sharpness))))


if __name__ == '__main__':
    main()
