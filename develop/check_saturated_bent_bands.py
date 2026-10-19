"""Check frozen positive long-arm sources with arbitrarily deep saturated inward bands."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import verify_terminal
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def long_bent(width, depth, saturate=True):
    assert width >= 8 and width % 2 == 0 and depth >= 1
    length = 2*depth+1
    matching = [((0, column), (0, column+1)) for column in range(0, width, 2)]
    matching += [((1, column), (1, column+1)) for column in range(1, width-1, 2)]
    matching += [((1, column), (2, column)) for column in (0, width-1)]
    matching += [((position+1, column), (position+2, column))
                 for column in (0, width-1) for position in range(2, length, 2)]
    selected = {(0, -1), (0, width), (length+2, 0), (length+2, width-1)}
    selected |= {(position+1, -1 if position % 2 else 1) for position in range(1, length+1)}
    selected |= {(position+1, width if position % 2 else width-2)
                 for position in range(1, length+1)}
    bands = set()
    for layer in range(depth if saturate else 0):
        upper, lower = 2+2*layer, 3+2*layer
        selected.update({(upper, 2), (lower, 1), (lower, 3), (lower, 4)})
        for tile in range(3, width//2):
            selected.update({(upper, 2*tile-1), (lower, 2*tile)})
        bands.update((layer+2, tile+2) for tile in range(width//2-1))
    move = lambda vertex: (vertex[0]+2, vertex[1]+3)
    current = 2*depth+8, width+8, {move(vertex) for vertex in selected}, [
        tuple(move(vertex) for vertex in edge) for edge in matching]
    return current, bands


def verify(width, depth):
    current, bands = long_bent(width, depth)
    assert direct_check(*current) == (depth+1)*width+2*depth+7
    checked = verify_terminal(current)
    assert len(checked['receivers']) == 1
    receiver = checked['receivers'][0]
    assert (receiver['tiles'], receiver['selected'], receiver['endpoints'], receiver['charge_twice']) == (
        width//2+2*depth+3, 2*depth+6, 2*width+4*depth+2, 2)
    endpoints = endpoint_data(current)[0]
    assert frozen_certificate(current)[0] == endpoints
    assert len(endpoint_data(current)[2]) == width-1
    assert len(current[2]) == depth*width+6
    graph, _ = graph_record(*current)
    receiver_tiles = {(row//2, column//2) for row, column in endpoints}
    assert not receiver_tiles & bands
    assert len(bands) == depth*(width//2-1)
    for row, column in bands:
        position = row*(current[1]//2)+column
        assert graph['t'][position] == 2
        assert not {(2*row+local_row, 2*column+local_column)
                    for local_row, local_column in itertools.product((0, 1), repeat=2)} & endpoints
    assert (2, 2) in bands and (2, width//2) in bands
    for layers in range(1, depth+1):
        prefix = {tile for tile in bands if tile[0] < layers+2}
        assert len(prefix) == layers*(width//2-1)
        assert all(graph['t'][row*(current[1]//2)+column] == 2 for row, column in prefix)
    return current, dict(width=width, depth=depth, odd_arm_length=2*depth+1,
                         receiver=receiver, inward_saturated_tiles=len(bands),
                         enlarged_receiver_charge_twice=2, objective=checked['objective'],
                         ambient_area=checked['area'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    images = 0
    for width in range(8, 33, 2):
        for depth in [1, 2, 3, 7, 16, 31]:
            current, record = verify(width, depth)
            records.append(record)
            if width in (8, 16, 32) and depth in (1, 7, 31):
                for symmetry in itertools.product((False, True), repeat=3):
                    shape, selected, matching = transformed(*current, *symmetry)
                    image = (*shape, selected, matching)
                    assert verify_terminal(image)['receivers'][0]['charge_twice'] == 2
                    assert frozen_certificate(image)[0] == endpoint_data(image)[0]
                    images += 1
    smallest, bands = long_bent(8, 1)
    report = dict(status='ALL_CHECKS_PASSED', family_cases=len(records), symmetry_images=images,
                  family=records,
                  smallest=dict(shape=smallest[:2], selected=sorted(smallest[2]), matching=smallest[3],
                                saturated_inward_band=sorted(bands)),
                  refuted_rules=['The unit-tail canonical donor still pays one after both tails are extended.',
                                 'A fixed number of complete inward bands always compensates a positive bent receiver.'],
                  global_coefficient_one_refuted=False,
                  scope='Finite controls for the independent all-width/all-depth written construction and freezing/count proof. No exclusion of alternative exterior donors or general compensation rules is claimed.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('family', 'smallest')}))


if __name__ == '__main__':
    main()
