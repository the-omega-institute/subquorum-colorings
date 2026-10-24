"""Separate marked sides from source charge and check original matching budgets."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import boundary, inspect_slots
from check_degree_three_fusion import phase_images
from check_minus_one_joint_compensation import marked_gate_modules
from check_minus_one_tip_obstructions import overloaded_tile_modules, source, two_tip_modules
from check_regular_tile_compensation import inspect
from check_zero_credit_tip_family import family
from degree_four_overcount import opposed_bands
from degree_three_fusion import occupied_bands
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    source_counts = Counter()
    parameters = list(itertools.product((6, 8, 14), (4, 8, 16), (4, 6, 12)))
    parameters += [(40, 100, 4)]
    for dimensions in parameters:
        original = source(*dimensions)
        for phase, symmetry in itertools.product(itertools.product((0, 1), repeat=2),
                                                  itertools.product((False, True), repeat=3)):
            shifted = transform_module(original, (False, False, False), phase)
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose else
                      (int(flip_row), int(flip_column)))
            module = transform_module(shifted, symmetry, offset)
            no_exterior, failures, _ = boundary(module)
            mark_capacity = len(no_exterior | failures)
            expected = {(0, 0): 0, (0, 1): 2, (1, 0): 2, (1, 1): 4}[phase]
            assert mark_capacity == expected
            assert len(module['matching']) >= 9
            assert 9*mark_capacity <= 4*len(module['matching'])
            assert (module['charge'] == 1) == (phase == (0, 0))
            source_counts[str(phase)] += 1
    fixtures = [('marked_gate', marked_gate_modules()), ('two_tips', two_tip_modules()),
                ('overloaded', overloaded_tile_modules()), ('zero_credit', family()),
                ('opposed', opposed_bands(6, 4)[1]), ('occupied', occupied_bands(6)[1])]
    physical = []
    for name, modules in fixtures:
        for symmetry, phase, offset, current, moved in phase_images(modules):
            slots = inspect_slots(current, moved)
            checked = inspect(current, moved, require_frozen=False)
            marked = slots['marked_sides']
            mass = slots['negative_mass']
            assignments = Counter(record['owner'] for record in slots['marked_assignments'])
            negative_matching = positive_matching = 0
            for owner, module in enumerate(moved):
                if len(module['endpoints']) == 8:
                    assert assignments[owner] == 0
                    continue
                if module['charge'] == 1:
                    assert assignments[owner] == 0
                    positive_matching += len(module['matching'])
                else:
                    no_exterior, failures, _ = boundary(module)
                    assert assignments[owner] <= len(no_exterior | failures) <= 4
                    negative_matching += len(module['matching'])
            assert 9*marked <= 4*negative_matching
            positive = slots['positive']
            matching = len(current[3])
            assert 36*positive+9*marked <= 4*matching
            assert checked['marked_sides'] == marked
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 positive=positive, marked_sides=marked,
                                 negative_original_charge=mass,
                                 negative_U_matching=negative_matching,
                                 positive_U_matching=positive_matching, matching=matching))
    witnesses = [record for record in physical if record['marked_sides'] !=
                 record['negative_original_charge']]
    assert witnesses
    universal = nonexceptional = negative_margins = 0
    for exceptional, single, extra, reserve in itertools.product(range(9), repeat=4):
        positive = exceptional+single+extra
        if 2*reserve < single:
            continue
        for margin in range(-exceptional-single//2, 7):
            marked = positive+reserve-margin
            if not 0 <= marked <= 2*positive:
                continue
            matching = 9*positive+4*exceptional+(9*marked+3)//4
            assert 35*margin+2*matching >= 0
            assert 15*margin+matching >= 0
            universal += 1
            negative_margins += margin < 0
            if exceptional == 0:
                assert 27*margin+matching >= 0
                assert 22*margin+matching >= 0
                nonexceptional += 1
    result = dict(status='PASS', parameter_controls=len(parameters),
                  U_source_image_controls=dict(source_counts), physical_images=len(physical),
                  marked_physical_images=sum(record['marked_sides'] > 0 for record in physical),
                  distinct_charge_mark_images=len(witnesses),
                  example_distinct_charge_mark=witnesses[0],
                  signed_budget_controls=universal, negative_margin_controls=negative_margins,
                  nonexceptional_budget_controls=nonexceptional,
                  new_complete_physical_fixture_coverage=0,
                  scope='Reconstructs source-local mark capacities separately from irregular event pools, actual physical mark assignments and matching sums ONCE per original owner in existing feasible fixtures. Distinguishes G marked sides from S original negative charge. Signed budget enumeration supplements universal written/Lean deductions; no new complete AA fixture or arbitrary-grid decomposition.',
                  physical=physical)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'physical'}))


if __name__ == '__main__':
    main()
