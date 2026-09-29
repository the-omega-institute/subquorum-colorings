#!/usr/bin/env python3
"""Controls for tilewise nonpositivity and arbitrarily branching neutral bands."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_compensation_transport import flip_internal_squares, nested_corridor
from check_cross_component_compensation import band_ledger, encode, sharp_band, witness_record
from check_residual_corridors import corridor, direct_check, graph_record, transformed
from verify_grid_five_sixths import canonical
from verify_grid_short_path_compensation import check_geometry


def branching_band(branches):
    if branches < 1:
        raise ValueError('Require at least one branch.')
    width = 4*branches-1
    _, columns, selected, matching = corridor(width)
    selected.update(((4, 0), (5, 1), (4, columns-1), (5, columns-2)))
    matching += [((2, 2*column), (2, 2*column+1))
                 for column in range(1, width+1)]
    for branch in range(branches):
        left, middle, right = 4*branch+1, 4*branch+2, 4*branch+3
        selected.update(((4, 2*left), (5, 2*left+1),
                         (4, 2*right+1), (5, 2*right)))
        matching += [((3, 2*left+1), (4, 2*left+1)),
                     ((3, 2*right), (4, 2*right)),
                     ((3, 2*middle), (3, 2*middle+1)),
                     ((4, 2*middle), (4, 2*middle+1))]
        if branch+1 < branches:
            separator = 4*branch+4
            selected.update(((5, 2*separator), (5, 2*separator+1)))
            matching.append(((3, 2*separator), (3, 2*separator+1)))
    return 6, columns, selected, matching


def local_controls():
    neighbors = ((1, 2), (0, 3), (0, 3), (1, 2))
    accepted = 0
    neutral = []
    for labels in itertools.product('BTP', repeat=4):
        selected = labels.count('T')
        endpoints = labels.count('P')
        if selected > 2:
            continue
        if any(sum(labels[other] != 'B' for other in neighbors[corner])
               + (corner < 2) > 1
               for corner in range(4) if labels[corner] == 'T'):
            continue
        for exits in ((), (2,), (3,), (2, 3)):
            if any(labels[corner] != 'P' or labels[5-corner] != 'B'
                   for corner in exits):
                continue
            accepted += 1
            if selected == 2:
                assert endpoints == 0 and not exits
                charge_twice = 0
            else:
                charge_twice = 2*selected+endpoints+len(exits)-4
            assert charge_twice <= 0, (labels, exits)
            if charge_twice == 0:
                neutral.append(dict(labels=''.join(labels[:2])+'/'+''.join(labels[2:]),
                                    exit_corners=list(exits), saturated=selected == 2))
    return dict(labelings_examined=81, feasible_relaxed_tile_states=accepted,
                neutral_states=neutral,
                scope='Necessary local conditions only; P matching and neighboring-tile compatibility are not assumed or inferred.')


def band_vertices(configuration):
    columns = configuration[1]
    return {(row, column) for row in (2, 3) for column in range(2, columns-2)}


def verify_image(configuration, region, expected_exits, expected_charge, branches=None):
    rows, columns, selected, matching = configuration
    objective = direct_check(*configuration)
    residual_graph, components = graph_record(*configuration)
    ledger = band_ledger(*configuration, region)
    assert ledger['saturated_attachments'] == expected_exits
    assert ledger['charge_twice'] == expected_charge
    for tile in ledger['tiles']:
        if residual_graph['t'][tile] < 2:
            assert residual_graph['deg'][tile]-2*residual_graph['r'][tile] <= 0
    assert not check_geometry(residual_graph)
    canonical(rows, columns, *encode(*configuration))
    if branches is not None:
        assert len(selected) == 6*branches+8
        assert len(matching) == 17*branches-1
        assert objective-rows*columns//2 == 1-branches
        assert ledger['blanks']-ledger['selected'] == 2*branches
        assert expected_exits == 2*branches and expected_charge == 0
    return sorted(component['excess'] for component in components)


def symmetry_controls(configuration, expected_exits, expected_charge, branches=None):
    region = band_vertices(configuration)
    original_excesses = verify_image(configuration, region, expected_exits, expected_charge, branches)
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        dimensions, selected, matching = transformed(*configuration, transpose, flip_rows, flip_columns)
        _, moved_region, _ = transformed(configuration[0], configuration[1], region, [],
                                          transpose, flip_rows, flip_columns)
        excesses = verify_image((*dimensions, selected, matching), moved_region,
                                expected_exits, expected_charge, branches)
        assert excesses == original_excesses
    return 8


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-branches', type=int, default=32)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if args.max_branches < 2:
        parser.error('--max-branches must be at least two')
    local = local_controls()
    images = 0
    witnesses = []
    for branches in range(1, args.max_branches+1):
        configuration = branching_band(branches)
        graph, components = graph_record(*configuration)
        assert sorted(component['excess'] for component in components) == [-1]*branches+[0]*(4*branches-1)+[1]
        assert all(graph['r'][tile] == graph['deg'][tile] == 0
                   for tile in range(4*branches+2, 8*branches+1))
        images += symmetry_controls(configuration, 2*branches, 0, branches)
        for limit in (1, configuration[1]):
            changed, swaps = flip_internal_squares(configuration, limit)
            assert swaps > 0
            before, _ = graph_record(*configuration)
            after, _ = graph_record(*changed)
            assert before['t'] == after['t']
            assert [degree-2*capacity for degree, capacity in zip(before['deg'], before['r'])] == [
                degree-2*capacity for degree, capacity in zip(after['deg'], after['r'])]
            assert max(after['r']) == 2
            images += symmetry_controls(changed, 2*branches, 0, branches)
        if branches <= 2:
            witnesses.append(witness_record(f'{branches} outgoing branches', configuration,
                                            band_vertices(configuration)))
    single_exit = nested_corridor(3, 2)
    single_exit[2].remove((4, 7))
    sharp_cases = ((sharp_band(3), 0, -2), (single_exit, 1, -1),
                   (branching_band(1), 2, 0))
    for configuration, exits, charge in sharp_cases:
        images += symmetry_controls(configuration, exits, charge)
        witnesses.append(witness_record(f'sharp sigma={exits}', configuration,
                                        band_vertices(configuration)))
    proof = Path(__file__).resolve().parents[1]/'docs/PRESSURE_BAND_BRANCHING.md'
    sources = [Path(__file__)] + [Path(__file__).with_name(name) for name in (
        'check_compensation_transport.py', 'check_cross_component_compensation.py',
        'check_residual_corridors.py', 'verify_grid_five_sixths.py',
        'verify_grid_short_path_compensation.py')] + [proof]
    report = dict(status='ALL_CHECKS_PASSED', max_branches=args.max_branches,
                  family_symmetry_images=24*args.max_branches, sharpness_images=24,
                  total_symmetry_images=images, local_controls=local, witnesses=witnesses,
                  sha256={path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in sources},
                  scope='Written all-size proofs are separate. Finite controls do not establish global compensation or unique donor ownership. No new Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'witnesses'}, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
