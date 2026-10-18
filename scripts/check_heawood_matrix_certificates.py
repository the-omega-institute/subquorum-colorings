"""Check six explicit certificates supporting the algebraic covering proof."""

import argparse
import json
from pathlib import Path


CASES = [
    ('N1', [(1, 2)], [10, 20, 21, 30, 40, 41, 51], [60, 50, 41, 70, 20, 31, 71], [], [61]),
    ('N2', [(1, 2), (2, 4)], [10, 11, 20, 31, 40, 41, 60], [40, 61, 50, 71, 30, 11, 70], [], [51]),
    ('S', [(3, 3), (1, 2), (2, 1)], [60, 20, 50, 10, 70, 30], [10, 11, 20, 21, 30, 31], [], [41, 51, 61]),
    ('J', [(3, 3), (2, 1)], [60, 20, 70, 30], [10, 11, 30, 31], [10, 50], [21, 41, 51, 61, 71]),
    ('C', [(1, 4), (2, 1), (4, 2)], [10, 20, 41, 60, 70], [41, 40, 31, 10, 30], [50], [21, 51, 61, 71]),
    ('K', [(1, 4), (2, 1), (4, 2), (2, 4)], [20, 30, 31, 40, 50, 51, 70], [11, 40, 31, 10, 20, 51, 60], [], [61]),
]


def outer(point, line):
    return sum(((point >> row & 1) * (line >> column & 1)) << (3 * row + column)
               for row in range(3) for column in range(3))


def binary_rank(vectors):
    basis = {}
    for vector in vectors:
        while vector:
            pivot = vector.bit_length() - 1
            if pivot not in basis:
                basis[pivot] = vector
                break
            vector ^= basis[pivot]
    return len(basis)


def matrix_rows(matrix):
    return [[matrix >> (3 * row + column) & 1 for column in range(3)] for row in range(3)]


def polynomial_coefficients(matrix):
    rows = matrix_rows(matrix)
    trace = rows[0][0] ^ rows[1][1] ^ rows[2][2]
    linear = 0
    for first, second in [(0, 1), (0, 2), (1, 2)]:
        linear ^= (rows[first][first] & rows[second][second]) ^ (rows[first][second] & rows[second][first])
    determinant = 0
    for columns in [(0, 1, 2), (0, 2, 1), (1, 0, 2), (1, 2, 0), (2, 0, 1), (2, 1, 0)]:
        determinant ^= rows[0][columns[0]] & rows[1][columns[1]] & rows[2][columns[2]]
    return [1, trace, linear, determinant]


def adjacent(point, line, twists):
    point_label, point_sheet = divmod(point, 10)
    line_label, line_sheet = divmod(line, 10)
    return ((point_label & line_label).bit_count() % 2 == 0
            and point_sheet ^ line_sheet == int((point_label, line_label) in twists))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    flags = [(point, line) for point in range(1, 8) for line in range(1, 8)
             if (point & line).bit_count() % 2 == 0]
    assert len(flags) == 21
    switchings = []
    for part in (0, 1):
        for label in range(1, 8):
            switching = sum(1 << position for position, flag in enumerate(flags) if flag[part] == label)
            switchings.append(switching)
            image = 0
            for position, flag in enumerate(flags):
                if switching >> position & 1:
                    image ^= outer(*flag)
            assert image == 0
    image_rank = binary_rank([outer(*flag) for flag in flags])
    switching_rank = binary_rank(switchings)
    assert image_rank == 8 and switching_rank == 13
    expected_matrices = {
        'N1': outer(1, 2),
        'N2': outer(1, 2) ^ outer(2, 4),
        'S': (1 << 0) ^ (1 << 4),
        'J': (1 << 0) ^ (1 << 4) ^ outer(1, 2),
        'C': outer(1, 4) ^ outer(2, 1) ^ outer(4, 2),
        'K': outer(1, 4) ^ outer(2, 1) ^ outer(4, 2) ^ outer(2, 4),
    }
    expected_polynomials = {'N1': [1, 0, 0, 0], 'N2': [1, 0, 0, 0],
                            'S': [1, 0, 1, 0], 'J': [1, 0, 1, 0],
                            'C': [1, 0, 0, 1], 'K': [1, 0, 1, 1]}
    records = []
    for name, twisted, matched_points, matched_lines, isolated_points, isolated_lines in CASES:
        twists = set(twisted)
        assert twists <= set(flags)
        matrix = 0
        for flag in twists:
            matrix ^= outer(*flag)
        assert matrix == expected_matrices[name]
        assert polynomial_coefficients(matrix) == expected_polynomials[name]
        selected_points = set(matched_points + isolated_points)
        selected_lines = set(matched_lines + isolated_lines)
        assert len(selected_points) == len(matched_points) + len(isolated_points)
        assert len(selected_lines) == len(matched_lines) + len(isolated_lines)
        assert len(matched_points) == len(matched_lines)
        assert len(selected_points) + len(selected_lines) == 15
        neighborhoods = {line: sorted(point for point in selected_points if adjacent(point, line, twists))
                         for line in sorted(selected_lines)}
        for point, line in zip(matched_points, matched_lines):
            assert neighborhoods[line] == [point], (name, point, line, neighborhoods[line])
        for line in isolated_lines:
            assert neighborhoods[line] == []
        assert all(sum(adjacent(point, line, twists) for line in selected_lines) <= 1
                   for point in selected_points)
        records.append(dict(type=name, twists=twisted, matrix=matrix_rows(matrix),
                            characteristic_polynomial=expected_polynomials[name],
                            selected_points=sorted(selected_points), selected_lines=sorted(selected_lines),
                            matched_edges=len(matched_points),
                            isolated_vertices=len(isolated_points) + len(isolated_lines),
                            line_neighborhoods=neighborhoods))
    report = dict(status='ALL_CHECKS_PASSED', flags=len(flags), image_rank=image_rank,
                  switching_rank=switching_rank, certificates=records,
                  scope='Local quotient-map and six explicit 15-vertex certificates only. '
                  'Algebraic completeness and transfer to all covers have written proofs; '
                  'no solver or enumeration of all 255 signings is used here. No new Lean claim.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'certificates'}, indent=2))


if __name__ == '__main__':
    main()
