"""Exact physical and cubical controls for punctured receiver Euler obstructions."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal
from check_cooperative_promotion import apply_bundle
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def punctured(holes):
    width = 4*holes+2
    missing = set().union(*(set(itertools.product((2, 3), (4*index+2, 4*index+3)))
                            for index in range(holes)))
    endpoints = set(itertools.product(range(6), range(width)))-missing
    matching = [((row+2, column+2), (row+2, column+3))
                for row, column in sorted(endpoints) if column % 2 == 0]
    selected = {(row+2, column+2) for row, column in
                ((-1, 0), (-1, width-1), (6, 0), (6, width-1))}
    return 10, width+4, selected, matching


def euler(tiles):
    vertices = set()
    edges = set()
    for row, column in tiles:
        cycle = [(row, column), (row+1, column), (row+1, column+1), (row, column+1)]
        vertices.update(cycle)
        edges.update(tuple(sorted((first, second))) for first, second in
                     zip(cycle, cycle[1:]+cycle[:1]))
    return dict(vertices=len(vertices), edges=len(edges), faces=len(tiles),
                chi=len(vertices)-len(edges)+len(tiles))


def inspect(current, holes):
    endpoints = endpoint_data(current)[0]
    assert endpoint_components(current) == [endpoints]
    assert frozen_certificate(current)[0] == set()
    checked = verify_terminal(current)
    receiver = checked['receivers'][0]
    tiles = {(row//2, column//2) for row, column in endpoints}
    counts = euler(tiles)
    assert receiver['selected'] == 0
    assert receiver['tiles'] == 5*holes+3
    assert receiver['endpoints'] == 4*receiver['tiles']
    assert receiver['charge_twice'] == 0 and counts['chi'] == 1-holes
    objective = direct_check(*current)
    for color in (0, 1):
        oriented = [edge if sum(edge[0]) % 2 == color else edge[::-1] for edge in current[3]]
        result = apply_bundle(current, oriented)
        assert not result[3] and direct_check(*result) == objective
    return dict(holes=holes, endpoints=len(endpoints), receiver_charge=0, **counts,
                frozen_endpoints=0, feasible_nonempty_color_bundles=2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    images = 0
    for holes in range(1, 33):
        current = punctured(holes)
        records.append(inspect(current, holes))
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            inspect((*shape, selected, matching), holes)
            images += 1
    report = dict(status='PASS', cases=len(records), symmetry_images=images, records=records,
                  scope='Controls for the all-k single-terminal Euler obstruction; '
                        'explicit bundles exclude the fully frozen hypothesis. '
                        'The frozen receiver ceiling and grid inequality remain open.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'records'}))


if __name__ == '__main__':
    main()
