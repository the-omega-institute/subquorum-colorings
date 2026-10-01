#!/usr/bin/env python3
"""Discovery MILP for mixed parent words inside neutral pressure frames.

This is an optional finite search, not a proof.  It requires SciPy's HiGHS
MILP interface and is deliberately not part of the required CI controls.
Every tile outside the designated parent row is restricted to a locally
neutral state; tiles on the parent row may use any locally feasible state.
The resulting pair is rechecked by the independent coordinate and canonical
residual verifiers.
"""
import argparse
import hashlib
import itertools
import json
import sys
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

from check_pressure_bands import local_controls
from check_residual_corridors import direct_check, graph_record
from check_cross_component_compensation import encode
from verify_grid_five_sixths import canonical


PARENT_WORDS = {
    12: {(1, 1): 'PP/PB', (1, 2): 'BT/TB', (1, 3): 'BP/TP',
         (1, 5): 'PP/BP'},
    14: {(1, 1): 'PP/BT', (2, 3): 'PP/BP', (1, 3): 'BT/TB',
         (1, 4): 'BP/TP', (1, 5): 'PP/PB'},
}


def label_states():
    neighbors = ((1, 2), (0, 3), (0, 3), (1, 2))
    states = []
    for labels in itertools.product('BTP', repeat=4):
        if labels.count('T') > 2:
            continue
        if any(sum(labels[other] != 'B' for other in neighbors[corner])
               + (corner < 2) > 1
               for corner in range(4) if labels[corner] == 'T'):
            continue
        flat = ''.join(labels)
        states.append((flat, tuple(letter == 'T' for letter in flat),
                       tuple(letter == 'P' for letter in flat)))
    neutral = {state['labels'].replace('/', '')
               for state in local_controls()['neutral_states']}
    return states, neutral


def solve(columns):
    rows = 6
    parent = PARENT_WORDS[columns]
    states, neutral = label_states()
    tile_columns = columns // 2
    tile_count = (rows // 2) * tile_columns
    state_index = {(tile, state): tile * len(states) + state
                   for tile in range(tile_count)
                   for state in range(len(states))}
    edges = []
    for row in range(rows):
        for column in range(columns):
            if column + 1 < columns:
                edges.append(((row, column), (row, column + 1)))
            if row + 1 < rows:
                edges.append(((row, column), (row + 1, column)))
    edge_offset = tile_count * len(states)
    variable_count = edge_offset + len(edges)

    def tile(vertex):
        return (vertex[0] // 2) * tile_columns + vertex[1] // 2

    def corner(vertex):
        return (vertex[0] % 2) * 2 + vertex[1] % 2

    rows_of_coefficients = []
    lower = []
    upper = []

    def add(coefficients, low, high):
        rows_of_coefficients.append(coefficients)
        lower.append(low)
        upper.append(high)

    for tile_number in range(tile_count):
        tile_row = tile_number // tile_columns
        allowed = [state for state, item in enumerate(states)
                   if tile_row == 1 or item[0] in neutral]
        add({state_index[tile_number, state]: 1 for state in allowed}, 1, 1)
        for state in set(range(len(states))) - set(allowed):
            add({state_index[tile_number, state]: 1}, 0, 0)

    for (tile_row, tile_column), wanted in parent.items():
        tile_number = tile_row * tile_columns + tile_column
        state = next(state for state, item in enumerate(states)
                     if item[0] == wanted.replace('/', ''))
        add({state_index[tile_number, state]: 1}, 1, 1)

    for row in range(rows):
        for column in range(columns):
            vertex = (row, column)
            tile_number = tile(vertex)
            position = corner(vertex)
            incident = [edge for edge, (first, second) in enumerate(edges)
                        if vertex == first or vertex == second]
            endpoint = {state_index[tile_number, state]: float(item[2][position])
                        for state, item in enumerate(states)}
            for edge in incident:
                endpoint[edge_offset + edge] = endpoint.get(edge_offset + edge, 0) - 1
            add(endpoint, 0, 0)
            for edge in incident:
                occupied = {state_index[tile_number, state]: float(item[1][position])
                            for state, item in enumerate(states)}
                occupied[edge_offset + edge] = 1
                add(occupied, -np.inf, 1)

    for row in range(rows):
        for column in range(columns):
            vertex = (row, column)
            tile_number = tile(vertex)
            position = corner(vertex)
            neighbors = [(row - 1, column)] if row else []
            if row + 1 < rows:
                neighbors.append((row + 1, column))
            if column:
                neighbors.append((row, column - 1))
            if column + 1 < columns:
                neighbors.append((row, column + 1))
            degree = len(neighbors)
            constraint = {state_index[tile_number, state]: degree * float(item[1][position])
                          for state, item in enumerate(states)}
            for neighbor in neighbors:
                neighbor_tile = tile(neighbor)
                neighbor_position = corner(neighbor)
                for state, item in enumerate(states):
                    index = state_index[neighbor_tile, state]
                    constraint[index] = constraint.get(index, 0) + float(item[1][neighbor_position]) + float(item[2][neighbor_position])
            add(constraint, -np.inf, 1 + degree)

    matrix = lil_matrix((len(rows_of_coefficients), variable_count), dtype=float)
    for row_number, coefficients in enumerate(rows_of_coefficients):
        for index, coefficient in coefficients.items():
            matrix[row_number, index] = coefficient
    objective = np.zeros(variable_count)
    objective[edge_offset:] = -1
    result = milp(objective, integrality=np.ones(variable_count),
                  bounds=Bounds(np.zeros(variable_count), np.ones(variable_count)),
                  constraints=LinearConstraint(matrix.tocsr(), np.array(lower),
                                               np.array(upper)),
                  options={'time_limit': 120})
    if not result.success:
        raise RuntimeError(f'MILP failed for {columns}: {result.message}')

    solution = result.x
    selected = set()
    matching = []
    tile_labels = {}
    for tile_number in range(tile_count):
        state = max(range(len(states)),
                    key=lambda candidate: solution[state_index[tile_number, candidate]])
        flat, selected_corners, _ = states[state]
        tile_row, tile_column = divmod(tile_number, tile_columns)
        tile_labels[f'{tile_row},{tile_column}'] = flat[:2] + '/' + flat[2:]
        for position, (row_delta, column_delta) in enumerate(((0, 0), (0, 1), (1, 0), (1, 1))):
            if selected_corners[position]:
                selected.add((2 * tile_row + row_delta, 2 * tile_column + column_delta))
    for edge, (first, second) in enumerate(edges):
        if solution[edge_offset + edge] > 0.5:
            matching.append((first, second))

    objective_value = direct_check(rows, columns, selected, matching)
    route = canonical(rows, columns, *encode(rows, columns, selected, matching))
    _, components = graph_record(rows, columns, selected, matching)
    for (tile_row, tile_column), wanted in parent.items():
        assert tile_labels[f'{tile_row},{tile_column}'] == wanted
    return dict(rows=rows, columns=columns, objective=objective_value,
                q=objective_value - rows * columns // 2,
                parent_labels={f'{row},{column}': label
                               for (row, column), label in parent.items()},
                tile_labels=tile_labels, selected=sorted(selected),
                matching=matching,
                component_excesses=sorted(item['excess'] for item in components),
                routing={key: route[key] for key in ('a', 'b', 'c', 'f2', 'f3', 'h')},
                interpretation='Finite MILP discovery with neutral states outside the parent row; not a general theorem.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    reports = [solve(columns) for columns in (12, 14)]
    report = dict(status='ALL_CHECKS_PASSED', witnesses=reports,
                  scope='Discovery only; SciPy MILP and two fixed parent words do not establish a universal neutral-frame bound.',
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'],
                      'q_values': [item['q'] for item in reports]}))


if __name__ == '__main__':
    main()
