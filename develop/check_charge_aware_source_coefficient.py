"""Original source-charge and signed-budget controls for improved coefficients."""

import argparse
import itertools
import json
from pathlib import Path

from check_minus_one_tip_obstructions import source
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    source_cases = negative_cases = positive_cases = rotor_cases = 0
    parameters = list(itertools.product((6, 8, 12, 20), (4, 6, 10), (4, 8, 12)))
    parameters += [(40, 30, 4), (20, 4, 30)]
    for width, left, right in parameters:
        for symmetry, phase in itertools.product(itertools.product((False, True), repeat=3),
                                                  itertools.product((0, 1), repeat=2)):
            module = transform_module(source(width, left, right), symmetry, phase)
            matching = len(module['matching'])
            assert matching == width+(left+right)//2-1
            charge = module['charge']
            if charge < 0:
                assert -charge in (1, width-1)
                assert matching >= -charge+4
                negative_cases += 1
            else:
                assert charge == 1
                assert matching >= 9
                if width != 6 and (width >= 12 or max(left, right) >= 8):
                    assert matching >= 13
                positive_cases += 1
            source_cases += 1
    for symmetry, phase in itertools.product(itertools.product((False, True), repeat=3),
                                              itertools.product((0, 1), repeat=2)):
        module = transform_module(rotor(), symmetry, phase)
        assert module['charge'] in (0, -2)
        assert len(module['matching']) == 4 >= -module['charge']
        rotor_cases += 1
    universal_cases = nonexceptional_cases = negative_margin_cases = 0
    for exceptional, single, extra_positive, reserve in itertools.product(range(9), repeat=4):
        positive = exceptional+single+extra_positive
        for margin in range(-exceptional-single//2, 7):
            negative_charge = positive+reserve-margin
            if negative_charge < 0:
                continue
            matching = 9*positive+4*exceptional+negative_charge
            assert 15*margin+matching >= 0
            universal_cases += 1
            negative_margin_cases += margin < 0
            if exceptional == 0 and 2*reserve >= single:
                assert 22*margin+matching >= 0
                nonexceptional_cases += 1
    assert negative_margin_cases > 0 and nonexceptional_cases > 0
    result = dict(status='PASS', source_image_controls=source_cases,
                  negative_U_images=negative_cases, positive_U_images=positive_cases,
                  rotor_image_controls=rotor_cases, universal_signed_budget_cases=universal_cases,
                  negative_margin_cases=negative_margin_cases,
                  nonexceptional_signed_budget_cases=nonexceptional_cases,
                  new_complete_physical_fixture_coverage=0,
                  scope='Reconstructed original U/rotor matching cardinalities and charges over representative arbitrary images, and signed aggregate budgets. Universal deductions are written and Lean-checked; no finite cutoff is part of either theorem.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
