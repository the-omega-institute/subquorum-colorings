"""Compare physical donor witnesses with the optional symbolic discovery encoding."""

import argparse
import itertools
import json
from pathlib import Path

import z3

from check_charge_two_frozen_receiver import fixture as charge_two_fixture
from check_corner_free_frozen_receiver import fixture as corner_free_fixture
from check_owned_corner_extensions import stepped_case
from check_residual_corridors import transformed
from search_weighted_owned_coverage import fixed_expression_control


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    fixtures = [('charge_two', charge_two_fixture()[0], 5),
                ('corner_free', corner_free_fixture()[0], 0),
                ('selected_guard', stepped_case(1), 1)]
    records = []
    for name, source, expected in fixtures:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*source, *symmetry)
            donors = fixed_expression_control((*shape, selected, matching))
            capacity = sum(record['deficit'] for record in donors)
            assert capacity == expected
            records.append(dict(name=name, symmetry=symmetry, actual_capacity=capacity,
                                expected_capacity=expected))
    report = dict(status='PASS', z3_version=z3.get_version_string(),
                  physical_symbolic_cases=len(records), controls=records,
                  scope='Independent physical witness scanner compared to simplified symbolic '
                        'expressions for both original rules and every physical symmetry. '
                        'No universal coverage conclusion follows from these fixed controls.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'controls'}))


if __name__ == '__main__':
    main()
