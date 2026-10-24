"""Check all alignment phases of complete one-square component receivers."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import (
    endpoint_components, mixed_control, shifted, single_normalize, verify_terminal,
)
from check_cooperative_promotion import neighbors
from check_owned_donors import endpoint_data
from check_residual_corridors import direct_check, transformed
from check_single_square_parity import central_patterns, neutral_obstacle, single_square
from verify_grid_five_sixths import bits, pairs


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


BASE = {
    0: ((1, 0), (2, 2), (2, 2), (4, 4)),
    2: ((3, 2), (3, 3), (3, 3), (4, 4)),
    4: ((5, 4), (4, 4), (4, 4), (4, 4)),
}


def square_counts(current):
    squares = endpoint_data(current)[2]
    return [sum(origin in component for origin in squares) for component in endpoint_components(current)]


def family_controls():
    records = []
    cases = images = extensions = 0
    parameters_all = list(itertools.product(range(3), repeat=4))
    parameters_all += [(0, 1, 7, 19), (31, 0, 1, 2), (4, 16, 3, 0), (20, 21, 22, 23)]
    for central in central_patterns():
        odd = 4-2*len(central)
        for vertical, horizontal in itertools.product((0, 1), repeat=2):
            tiles_base, selected_base = BASE[odd][2*vertical+horizontal]
            expected_twice = 2*selected_base+4+odd-4*tiles_base
            assert expected_twice <= 0
            for parameters in parameters_all:
                current, lengths = single_square(parameters, central)
                current = shifted(current, vertical, horizontal)
                record = verify_terminal(current)
                assert len(record['receivers']) == 1 and square_counts(current) == [1]
                receiver = record['receivers'][0]
                assert receiver['tiles'] == tiles_base+sum(parameters)
                assert receiver['selected'] == selected_base+sum(parameters)
                assert receiver['endpoints'] == 4+odd+2*sum(parameters)
                assert receiver['charge_twice'] == expected_twice
                endpoints = endpoint_data(current)[0]
                tiles = {(row//2, column//2) for row, column in endpoints}
                cells = {(2*row+first, 2*column+second) for row, column in tiles
                         for first, second in itertools.product((0, 1), repeat=2)}
                assert all(set(neighbors(vertex)) & endpoints for vertex in current[2] & cells)
                for vertex in cells-current[2]-endpoints:
                    assert (len(set(neighbors(vertex)) & endpoints) >= 2 or
                            any(support in current[2] and set(neighbors(support)) & endpoints
                                for support in neighbors(vertex)))
                if parameters in [(0, 0, 0, 0), (0, 1, 7, 19), (20, 21, 22, 23)]:
                    for arm in range(4):
                        longer = list(parameters)
                        longer[arm] += 1
                        extended, _ = single_square(longer, central)
                        extended = shifted(extended, vertical, horizontal)
                        following = verify_terminal(extended)['receivers'][0]
                        assert [following[key]-receiver[key] for key in ('tiles', 'selected', 'endpoints')] == [1, 1, 2]
                        extensions += 1
                if parameters in [(0, 0, 0, 0), (0, 1, 7, 19)]:
                    for symmetry in itertools.product((False, True), repeat=3):
                        shape, selected, matching = transformed(*current, *symmetry)
                        image = (*shape, selected, matching)
                        assert verify_terminal(image)['receivers'][0]['charge_twice'] == expected_twice
                        images += 1
                cases += 1
            records.append(dict(central_internal_edges=central, odd_arms=odd,
                                origin_parity=[vertical, horizontal], base_receiver_tiles=tiles_base,
                                base_selected_in_receiver=selected_base, charge_twice=expected_twice,
                                length_choices=len(parameters_all)))
    return records, cases, images, extensions


def exhaustive_controls():
    records = []
    for rows, columns in ((2, 2), (2, 4), (2, 6), (3, 4)):
        examined = accepted = single_moves = 0
        for selected_mask, _, matching in pairs(rows, columns):
            current = (rows+(rows % 2), columns,
                       {divmod(vertex, columns) for vertex in bits(selected_mask)},
                       [(divmod(first, columns), divmod(second, columns)) for first, second in matching])
            examined += 1
            if any(count > 1 for count in square_counts(current)):
                continue
            ending, moves = single_normalize(current)
            assert all(count <= 1 for count in square_counts(ending))
            record = verify_terminal(ending)
            assert all(receiver['charge_twice'] <= 0 for receiver in record['receivers'])
            budget_twice = -sum(receiver['charge_twice'] for receiver in record['receivers'])
            assert ending[0]*ending[1]-2*record['objective'] == budget_twice+2*record['empty_deficit']
            assert direct_check(*current) <= current[0]*current[1]//2
            accepted += 1
            single_moves += moves
        records.append(dict(source_shape=[rows, columns], even_ambient=[rows+(rows % 2), columns],
                            examined=examined, at_most_one_square_pairs=accepted, single_moves=single_moves))
    return records


def sharp_control():
    record = neutral_obstacle()
    current = (*record['shape'], set(map(tuple, record['selected'])),
               [tuple(map(tuple, edge)) for edge in record['matching']])
    checked = verify_terminal(current)
    assert square_counts(current) == [1]
    assert checked['receivers'][0]['charge_twice'] == checked['empty_deficit'] == 0
    assert checked['objective'] == checked['area']//2
    return dict(shape=record['shape'], labels=record['labels'], selected=record['selected'],
                matching=record['matching'], **checked)


def combined_control():
    baseline = mixed_control()
    base_selected = set(map(tuple, baseline['initial_selected']))
    base_matching = [tuple(map(tuple, edge)) for edge in baseline['initial_matching']]
    branch, _ = single_square((1, 2, 0, 1), [(0, 1)])
    branch = shifted(branch, 1, 1)
    move = lambda vertex: (vertex[0]+18, vertex[1]+22)
    selected = base_selected | {move(vertex) for vertex in branch[2]}
    matching = base_matching+[tuple(move(vertex) for vertex in edge) for edge in branch[3]]
    current = 34, 42, selected, matching
    from check_component_receivers import pure_reduce_small
    reduced, rectangular_moves = pure_reduce_small(current)
    ending, single_moves = single_normalize(reduced)
    checked = verify_terminal(ending)
    assert sum(receiver['charge_twice'] for receiver in checked['receivers']) == -4
    assert checked['area']//2-checked['objective'] == 2+checked['empty_deficit']
    assert any(count == 1 for count in square_counts(ending))
    return dict(initial_shape=current[:2], selected=sorted(selected), matching=matching,
                rectangular_moves=rectangular_moves, single_moves=single_moves,
                receiver_budget=2, **checked)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    family, cases, images, extensions = family_controls()
    exhaustive = exhaustive_controls()
    sharp = sharp_control()
    combined = combined_control()
    report = dict(status='ALL_CHECKS_PASSED', family=family, family_cases=cases,
                  symmetry_images=images, two_step_extensions=extensions,
                  exhaustive=exhaustive, sharp=sharp, combined=combined,
                  scope='General proof uses the complete single-square classification, all-length two-step count invariance and explicit base geometry. Finite enumeration only checks counts and fixtures, not a universal grid theorem.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:report[key] for key in ('status', 'family_cases', 'symmetry_images',
                                                'two_step_extensions')}), flush=True)


if __name__ == '__main__':
    main()
