"""Independent controls for terminal component ownership and square-free bounds."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import apply_bundle, neighbors, occupied_degrees
from check_frozen_two_row_caps import capped_ladder
from check_owned_donors import endpoint_data, straight_comb
from check_promotion_cores import frozen_certificate, tight_diamond
from check_residual_corridors import direct_check, graph_record, transformed
from verify_grid_five_sixths import bits, pairs


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def endpoint_components(current):
    endpoints, adjacency, _ = endpoint_data(current)
    remaining = set(endpoints)
    components = []
    while remaining:
        pending = [min(remaining)]
        component = set(pending)
        remaining.difference_update(component)
        while pending:
            added = adjacency[pending.pop()] & remaining
            remaining.difference_update(added)
            component.update(added)
            pending.extend(added)
        components.append(component)
    return components


def vertices_of(tiles):
    return {(2*row+local_row, 2*column+local_column)
            for row, column in tiles
            for local_row, local_column in itertools.product((0, 1), repeat=2)}


def single_normalize(current):
    original = direct_check(*current)
    moves = 0
    while True:
        degrees = occupied_degrees(current)
        candidates = [vertex for vertex in sorted(degrees) if degrees[vertex] <= 2]
        if not candidates:
            assert direct_check(*current) == original
            return current, moves
        vertex = candidates[0]
        mate = next(second if first == vertex else first
                    for first, second in current[3] if vertex in (first, second))
        current = apply_bundle(current, [(vertex, mate)])
        moves += 1


def verify_terminal(current, expected_caps=None):
    objective = direct_check(*current)
    rows, columns, selected, _ = current
    assert rows % 2 == columns % 2 == 0
    assert all(degree >= 3 for degree in occupied_degrees(current).values())
    graph, _ = graph_record(*current)
    all_tiles = set(itertools.product(range(rows//2), range(columns//2)))
    used = set()
    receivers = []
    for component in endpoint_components(current):
        tiles = {(row//2, column//2) for row, column in component}
        assert not tiles & used
        used.update(tiles)
        cells = vertices_of(tiles)
        endpoints = endpoint_data(current)[0] & cells
        assert endpoints == component
        charge_twice = sum(graph['deg'][row*(columns//2)+column]
                           - 2*graph['r'][row*(columns//2)+column]
                           for row, column in tiles
                           if graph['t'][row*(columns//2)+column] < 2)
        selected_count = len(selected & cells)
        assert charge_twice == 2*selected_count+len(component)-4*len(tiles)
        saturated_endpoints = sum(graph['t'][vertex[0]//2*(columns//2)+vertex[1]//2] == 2
                                  for vertex in component)
        transfers = sum(graph['s'][row*(columns//2)+column]
                        for row, column in tiles if graph['t'][row*(columns//2)+column] < 2)
        assert transfers == saturated_endpoints
        straight = len({row for row, _ in component}) == 1 or len({column for _, column in component}) == 1
        if straight:
            assert charge_twice == 0
        receivers.append(dict(endpoints=len(component), tiles=len(tiles), selected=selected_count,
                              charge_twice=charge_twice, straight=straight,
                              saturated_endpoints=saturated_endpoints, transfers=transfers))
    empty_tiles = all_tiles-used
    empty_deficit = sum(2-graph['t'][row*(columns//2)+column] for row, column in empty_tiles)
    assert 2*objective-rows*columns == sum(record['charge_twice'] for record in receivers)-2*empty_deficit
    if expected_caps is not None:
        assert sum(record['charge_twice'] for record in receivers) == -2*expected_caps
        assert rows*columns//2-objective == expected_caps+empty_deficit
    return dict(receivers=receivers, no_endpoint_tiles=len(empty_tiles), empty_deficit=empty_deficit,
                objective=objective, area=rows*columns)


def local_controls():
    adjacent = ((1, 2), (0, 3), (0, 3), (1, 2))
    valid = nonempty = 0
    for labels in itertools.product(range(3), repeat=4):
        for exterior in itertools.product(range(3), repeat=4):
            degrees = [sum(labels[neighbor] != 0 for neighbor in adjacent[corner])+exterior[corner]
                       for corner in range(4)]
            if any(label == 1 and degrees[corner] > 1 or label == 2 and degrees[corner] < 3
                   for corner, label in enumerate(labels)):
                continue
            valid += 1
            endpoints = {corner for corner, label in enumerate(labels) if label == 2}
            if not endpoints:
                continue
            nonempty += 1
            reached = {min(endpoints)}
            while True:
                extended = reached | {neighbor for corner in reached for neighbor in adjacent[corner]
                                      if neighbor in endpoints}
                if extended == reached:
                    break
                reached = extended
            assert reached == endpoints
    return dict(models=3**8, feasible_terminal_models=valid, nonempty_endpoint_models=nonempty)


def shifted(current, vertical, horizontal):
    move = lambda vertex: (vertex[0]+vertical, vertex[1]+horizontal)
    rows, columns, selected, matching = current
    return rows+2, columns+2, {move(vertex) for vertex in selected}, [tuple(move(vertex) for vertex in edge)
                                                                   for edge in matching]


def comb_controls():
    records = []
    images = 0
    for size in range(1, 65):
        phases = []
        for vertical, horizontal in itertools.product((0, 1), repeat=2):
            current = shifted(straight_comb(size), vertical, horizontal)
            record = verify_terminal(current, expected_caps=0)
            receiver = record['receivers'][0]
            misaligned = (3+horizontal) % 2
            assert receiver['tiles'] == size+misaligned
            assert receiver['selected'] == size+2*misaligned
            cells = vertices_of({(row//2, column//2) for row, column in endpoint_data(current)[0]})
            for vertex in cells-current[2]-endpoint_data(current)[0]:
                assert any(support in current[2] and
                           any(endpoint in endpoint_data(current)[0] for endpoint in neighbors(support))
                           for support in neighbors(vertex))
            phases.append(dict(vertical=vertical, horizontal=horizontal, **receiver))
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                verify_terminal((*shape, selected, matching), expected_caps=0)
                images += 1
        records.append(dict(matching_edges=size, phases=phases))
    return records, images


def exhaustive_controls():
    records = []
    for rows, columns in ((2, 2), (2, 4), (2, 6), (3, 4)):
        count = terminal = square_free = promotions = nonempty_terminal = 0
        for selected_mask, _, matching in pairs(rows, columns):
            current = (rows+(rows % 2), columns,
                       {divmod(vertex, columns) for vertex in bits(selected_mask)},
                       [(divmod(first, columns), divmod(second, columns)) for first, second in matching])
            if all(degree >= 3 for degree in occupied_degrees(current).values()):
                verify_terminal(current)
                terminal += 1
                nonempty_terminal += bool(current[3])
            if not endpoint_data(current)[2]:
                ending, moves = single_normalize(current)
                assert not endpoint_data(ending)[2]
                record = verify_terminal(ending, expected_caps=0)
                assert all(receiver['straight'] for receiver in record['receivers'])
                assert direct_check(*current) <= current[0]*current[1]//2
                assert moves <= len(current[3])
                square_free += 1
                promotions += moves
            count += 1
        record = dict(original_shape=[rows, columns], even_ambient=[rows+(rows % 2), columns],
                      feasible_pairs=count, terminal_pairs=terminal, nonempty_terminal=nonempty_terminal,
                      square_free_pairs=square_free, single_promotions=promotions)
        records.append(record)
        print(json.dumps(record), flush=True)
    return records


def pure_reduce_small(current):
    moves = 0
    for component in endpoint_components(current):
        if len(component) < 4:
            continue
        row_set = {row for row, _ in component}
        column_set = {column for _, column in component}
        if len(component) != len(row_set)*len(column_set) or 2 not in (len(row_set), len(column_set)):
            continue
        edges = [edge for edge in current[3] if edge[0] in component]
        found = False
        for states in itertools.product((0, 1, 2), repeat=len(edges)):
            if sum(state != 0 for state in states) < len(edges)-1:
                continue
            bundle = [edge if state == 1 else edge[::-1] for state, edge in zip(states, edges) if state]
            try:
                changed = apply_bundle(current, bundle)
            except AssertionError:
                continue
            assert len(endpoint_data(changed)[0] & component) <= 2
            current = changed
            moves += 1
            found = True
            break
        assert found
    return current, moves


def mixed_control():
    first, _ = tight_diamond()
    shape, selected, matching = transformed(*first, True, False, False)
    second = (*shape, selected, matching)
    cap = capped_ladder(5)
    pure = (6, 8, {(1, 2), (1, 4), (4, 2), (4, 4), (2, 1), (3, 5)},
            [((2, column), (3, column)) for column in range(2, 5)])
    selected = set()
    matching = []
    for pattern, vertical, horizontal in ((first, 0, 0), (second, 0, 10),
                                          (cap, 10, 0), (pure, 10, 12)):
        move = lambda vertex: (vertex[0]+vertical, vertex[1]+horizontal)
        selected.update(move(vertex) for vertex in pattern[2])
        matching.extend(tuple(move(vertex) for vertex in edge) for edge in pattern[3])
    current = 18, 22, selected, matching
    objective = direct_check(*current)
    reduced, rectangular_moves = pure_reduce_small(current)
    ending, single_moves = single_normalize(reduced)
    assert direct_check(*ending) == objective
    record = verify_terminal(ending, expected_caps=1)
    assert any(receiver['straight'] for receiver in record['receivers'])
    assert any(len({row for row, _ in component}) == 1 for component in endpoint_components(ending))
    assert any(len({column for _, column in component}) == 1 for component in endpoint_components(ending))
    assert frozen_certificate(ending)[0] == endpoint_data(ending)[0]
    return dict(initial_shape=current[:2], initial_selected=sorted(current[2]), initial_matching=current[3],
                rectangular_moves=rectangular_moves, single_moves=single_moves, **record)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    local = local_controls()
    combs, images = comb_controls()
    exhaustive = exhaustive_controls()
    mixed = mixed_control()
    report = dict(status='ALL_CHECKS_PASSED', local=local, comb_lengths=64,
                  alignment_phases=256, symmetry_images=images, combs=combs,
                  exhaustive=exhaustive, mixed=mixed,
                  scope='General proofs establish terminal tile ownership, closed-receiver accounting, zero charge for every comb alignment and coefficient one for the square-free/pure-rectangle/prescribed-capped class. Finite controls do not establish a universal grid inequality.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], comb_lengths=64, symmetry_images=images,
                         feasible_pairs=sum(record['feasible_pairs'] for record in exhaustive))), flush=True)


if __name__ == '__main__':
    main()
