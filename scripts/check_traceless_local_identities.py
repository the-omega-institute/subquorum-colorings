"""Independent controls for the three local representatives in the alternative proof."""

import argparse
import json
from pathlib import Path

from check_heawood_matrix_certificates import matrix_rows, polynomial_coefficients


def product(first, second):
    first_rows = matrix_rows(first)
    second_rows = matrix_rows(second)
    return sum((sum(first_rows[row][inner] * second_rows[inner][column] for inner in range(3)) % 2)
               << (3 * row + column) for row in range(3) for column in range(3))


def trace(matrix):
    return (matrix >> 0 & 1) ^ (matrix >> 4 & 1) ^ (matrix >> 8 & 1)


def power(matrix, exponent):
    result = 273
    for position in range(exponent):
        result = product(result, matrix)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    companion = 172
    squared = product(companion, companion)
    fourth = power(companion, 4)
    assert power(companion, 7) == 273
    assert companion ^ squared == fourth
    assert polynomial_coefficients(companion) == [1, 0, 1, 1]
    assert trace(product(companion, squared)) == trace(product(companion, fourth)) == 1
    records = []
    all_elements = {companion, squared, fourth}
    for representative, expected_pair in [(95, (0, 1)), (102, (1, 1)), (157, (1, 0))]:
        orbit = [product(product(power(companion, exponent), representative),
                         power(companion, (-exponent) % 7)) for exponent in range(7)]
        assert product(companion, representative) != product(representative, companion)
        assert len(set(orbit)) == 7 and not all_elements & set(orbit)
        all_elements.update(orbit)
        assert all(polynomial_coefficients(matrix) == [1, 0, 1, 1] for matrix in orbit)
        assert all((trace(product(companion, matrix)), trace(product(squared, matrix))) == expected_pair
                   for matrix in orbit)
        assert all(polynomial_coefficients(companion ^ matrix)[-1] == 0 for matrix in orbit)
        if representative == 95:
            assert [trace(product(representative, matrix)) for matrix in orbit] == [0, 0, 1, 1, 1, 1, 0]
        records.append(dict(representative=matrix_rows(representative), orbit=orbit,
                            trace_pair=expected_pair, determinant_of_sum=0))
    assert len(all_elements) == 24
    report = dict(status='ALL_LOCAL_IDENTITIES_PASSED', companion=matrix_rows(companion),
                  representatives=records, certified_distinct_elements=24,
                  scope='Direct identities for three local conjugation representatives. '
                  'Completeness follows in the written proof from conjugacy and centralizer order, '
                  'not from exhaustive subspace enumeration. The shorter primary proof uses '
                  'rank-one counting and the verified existing dimension theorem.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'representatives'}, indent=2))


if __name__ == '__main__':
    main()
