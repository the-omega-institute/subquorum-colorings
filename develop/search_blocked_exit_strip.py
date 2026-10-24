#!/usr/bin/env python3
"""Finite discovery for the outer-exit successor; no general proof is inferred."""
import argparse
import hashlib
import json
from pathlib import Path

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

from check_cross_component_compensation import band_ledger, witness_record
from check_residual_corridors import corridor, direct_check
from check_mixed_band_boundary_obstacle import general_region_ledger


STATES = ('PPPP', 'PPBP', 'PPPB', 'PPBT', 'PPTB',
          'BPTP', 'PBPT', 'BBTT', 'BTTB', 'TBBT')


def solve(width, time_limit, rows=6):
    assert rows in (6, 8)
    columns = 2*width+4
    vertex_count = rows*columns
    edges = [(vertex, neighbor)
             for vertex in range(vertex_count)
             for neighbor in ([vertex+1] if vertex % columns+1 < columns else [])
             + ([vertex+columns] if vertex//columns+1 < rows else [])]
    edge_index = {frozenset(edge): vertex_count+index for index, edge in enumerate(edges)}
    state_offset = vertex_count+len(edges)
    state_index = {(tile, state): state_offset+10*(tile-1)+state
                   for tile in range(1, width+1) for state in range(10)}
    sat_offset = state_offset+10*width
    export_offset = sat_offset+(rows//2-2)*(width+2)
    variable_count = export_offset+(2*width if rows == 8 else 0)
    incident = [[] for _ in range(vertex_count)]
    for edge, variable in edge_index.items():
        for vertex in edge:
            incident[vertex].append(variable)
    coefficients = []
    lower = []
    upper = []

    def add(entries, low, high):
        coefficients.append(entries)
        lower.append(low)
        upper.append(high)

    def endpoint(vertex, weight=1):
        return {variable: weight for variable in incident[vertex]}

    def merge(*parts):
        result = {}
        for part in parts:
            for variable, value in part.items():
                result[variable] = result.get(variable, 0)+value
        return result

    for vertex in range(vertex_count):
        add(merge({vertex: 1}, endpoint(vertex)), 0, 1)
        neighbors = [next(iter(edge-{vertex})) for edge in edge_index if vertex in edge]
        entries = {vertex: len(neighbors)}
        for neighbor in neighbors:
            entries = merge(entries, {neighbor: 1}, endpoint(neighbor))
        add(entries, -np.inf, len(neighbors)+1)

    _, _, frame_selected, frame_matching = corridor(width)
    for row in (0, 1):
        for column in range(columns):
            vertex = row*columns+column
            add({vertex: 1}, int((row, column) in frame_selected),
                int((row, column) in frame_selected))
            wanted = int(any((row, column) in edge for edge in frame_matching))
            add(endpoint(vertex), wanted, wanted)
    for vertex in frame_selected:
        add({vertex[0]*columns+vertex[1]: 1}, 1, 1)
    for first, second in frame_matching:
        if first[0] == second[0] == 1:
            continue
        variable = edge_index[frozenset((first[0]*columns+first[1],
                                         second[0]*columns+second[1]))]
        add({variable: 1}, 1, 1)
    for tile_column in (0, width+1):
        for row in (2, 3):
            for column in (2*tile_column, 2*tile_column+1):
                vertex = row*columns+column
                if (row, column) not in frame_selected:
                    wanted = int(any((row, column) in edge for edge in frame_matching))
                    add({vertex: 1}, 0, 0)
                    add(endpoint(vertex), wanted, wanted)

    for tile_row in range(2, rows//2):
        for tile_column in range(width+2):
            vertices = [row*columns+column for row in (2*tile_row, 2*tile_row+1)
                        for column in (2*tile_column, 2*tile_column+1)]
            indicator = sat_offset+(tile_row-2)*(width+2)+tile_column
            add(merge({vertex: 1 for vertex in vertices}, {indicator: -2}), 0, np.inf)
            add(merge({vertex: 1 for vertex in vertices}, {indicator: -1}), -np.inf, 1)

    for tile_column in range(1, width+1):
        add({state_index[tile_column, state]: 1 for state in range(10)}, 1, 1)
        vertices = [row*columns+column for row in (2, 3)
                    for column in (2*tile_column, 2*tile_column+1)]
        for corner, vertex in enumerate(vertices):
            selected_state = {state_index[tile_column, state]: -int(labels[corner] == 'T')
                              for state, labels in enumerate(STATES)}
            endpoint_state = {state_index[tile_column, state]: -int(labels[corner] == 'P')
                              for state, labels in enumerate(STATES)}
            add(merge({vertex: 1}, selected_state), 0, 0)
            add(merge(endpoint(vertex), endpoint_state), 0, 0)
        for lower_corner, state in ((2, 2), (3, 1)):
            vertex = vertices[lower_corner]
            variable = edge_index[frozenset((vertex, vertex+columns))]
            exit_state = state_index[tile_column, state]
            add({exit_state: 1, variable: -1}, -np.inf, 0)
            add({exit_state: 1, sat_offset+tile_column: -1}, -np.inf, 0)
            add({variable: 1, sat_offset+tile_column: 1, exit_state: -1}, -np.inf, 1)
            neighbor = vertex+(-1 if lower_corner == 2 else 1)
            add(merge({exit_state: 1, neighbor: -1}, endpoint(neighbor, -1)), -np.inf, 0)
    add({state_index[1, 1]: 1}, 1, 1)
    add({state_index[width, 2]: 1}, 1, 1)

    child_vertices = {row*columns+column for row in (4, 5)
                      for column in range(2, columns-2)}
    objective = np.zeros(variable_count)
    for vertex in child_vertices:
        objective[vertex] -= 2
        for variable in incident[vertex]:
            objective[variable] -= 1
    for tile_column in range(1, width+1):
        for state in (1, 2):
            objective[state_index[tile_column, state]] += 1
    if rows == 8:
        for column in range(2, columns-2):
            tile_column = column//2
            edge_variable = edge_index[frozenset((5*columns+column, 6*columns+column))]
            child_sat = sat_offset+tile_column
            below_sat = sat_offset+width+2+tile_column
            export_variable = export_offset+column-2
            add({edge_variable: 1, below_sat: 1, child_sat: -1}, -np.inf, 1)
            add({export_variable: 1, edge_variable: -1}, -np.inf, 0)
            add({export_variable: 1, child_sat: -1}, -np.inf, 0)
            add({export_variable: 1, edge_variable: -1, child_sat: -1}, -1, np.inf)
            objective[export_variable] += 1
    matrix = lil_matrix((len(coefficients), variable_count))
    for row_number, entries in enumerate(coefficients):
        for variable, value in entries.items():
            matrix[row_number, variable] = value
    result = milp(objective, integrality=np.ones(variable_count),
                  bounds=Bounds(np.zeros(variable_count), np.ones(variable_count)),
                  constraints=LinearConstraint(matrix.tocsr(), lower, upper),
                  options={'time_limit': time_limit, 'mip_rel_gap': 0})
    summary = dict(rows=rows, width=width, status=int(result.status), message=result.message)
    if result.x is None:
        return summary
    selected = {divmod(vertex, columns) for vertex in range(vertex_count) if result.x[vertex] > .5}
    matching = [(divmod(first, columns), divmod(second, columns))
                for edge, variable in edge_index.items() if result.x[variable] > .5
                for first, second in [sorted(edge)]]
    current = rows, columns, selected, matching
    direct_check(*current)
    parent = {(row, column) for row in (2, 3) for column in range(2, columns-2)}
    child = {(row, column) for row in (4, 5) for column in range(2, columns-2)}
    parent_ledger, child_ledger = band_ledger(*current, parent), general_region_ledger(current, child)
    assert parent_ledger['charge_twice'] == 0
    assert child_ledger['charge_twice'] == round(-result.fun-4*width)
    summary.update(parent=parent_ledger, child=child_ledger,
                   witness=witness_record('normalized outer-exit strip', current),
                   parent_word=[STATES[next(state for state in range(10)
                                           if result.x[state_index[tile, state]] > .5)]
                                for tile in range(1, width+1)],
                   optimality_proved_by_solver=result.status == 0)
    return summary


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--widths', type=int, nargs='+', default=[3, 4, 5, 6, 7, 8])
    parser.add_argument('--time-limit', type=float, default=15)
    parser.add_argument('--rows', type=int, choices=(6, 8), default=6)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if any(width < 3 for width in args.widths) or args.time_limit <= 0:
        parser.error('Require widths at least three and a positive time limit.')
    records = []
    for width in args.widths:
        record = solve(width, args.time_limit, args.rows)
        records.append(record)
        print(json.dumps({key: value for key, value in record.items()
                          if key not in ('witness', 'parent', 'child')}, ensure_ascii=False), flush=True)
        if 'child' in record:
            print('child charge twice:', record['child']['charge_twice'], flush=True)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    sources = [Path(__file__), Path(__file__).with_name('check_mixed_band_boundary_obstacle.py')]
    args.output.write_text(json.dumps(dict(scope='Finite discovery, not a general compensation proof.',
                                         widths=args.widths, rows=args.rows, time_limit=args.time_limit,
                                         script_sha256={path.name: hashlib.sha256(path.read_bytes()).hexdigest()
                                                        for path in sources},
                                         records=records), indent=2)+'\n')


if __name__ == '__main__':
    main()
