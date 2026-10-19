"""Physical controls for the all-phase joint slot theorem."""

import argparse
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import boundary, inspect_slots
from check_degree_three_fusion import phase_images
from check_minus_one_joint_compensation import contained, marked_gate_modules
from check_minus_one_tip_obstructions import overloaded_tile_modules, source, two_tip_modules
from check_regular_tile_compensation import inspect
from check_zero_credit_tip_family import family
from degree_four_overcount import opposed_bands
from degree_three_fusion import four_way_modules, occupied_bands
from rotor_networks import chain_modules, rotor, star_modules, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def boundary_controls():
    records = []
    parameters = list(itertools.product((6, 8, 14), (4, 8, 16), (4, 6, 12)))+[(40, 100, 4)]
    for width, left, right in parameters:
        base = source(width, left, right)
        for phase in itertools.product(range(2), repeat=2):
            original = transform_module(base, (False, False, False), phase)
            corners = {(phase[0], 1+phase[1]), (phase[0], width+phase[1])}
            tips = {(left+phase[0], 1+phase[1]), (right+phase[0], width+phase[1])}
            expected_no_exterior = (set() if phase == (0, 0) else
                                    corners if phase == (0, 1) else tips)
            expected_failures = corners | tips if phase == (1, 1) else set()
            for symmetry in itertools.product((False, True), repeat=3):
                transpose, flip_row, flip_column = symmetry
                shift = ((int(flip_column), int(flip_row)) if transpose else
                         (int(flip_row), int(flip_column)))
                module = transform_module(original, symmetry, shift)
                def move(point):
                    row, column = point
                    row = 1-row if flip_row else row
                    column = 1-column if flip_column else column
                    return (column, row) if transpose else (row, column)
                no_exterior, failures, irregular = boundary(module)
                assert no_exterior == {move(point) for point in expected_no_exterior}
                assert failures == {move(point) for point in expected_failures}
                expected_irregular = {(0, 0): 0, (0, 1): 2,
                                      (1, 0): 2*width-2, (1, 1): 2*width-4}[phase]
                assert len(irregular) == expected_irregular
                pool = no_exterior | failures | irregular
                expected_pool = {(0, 0): 0, (0, 1): 4,
                                 (1, 0): 2*width, (1, 1): 2*width-2}[phase]
                assert len(pool) == expected_pool
                assert failures-irregular <= {move(point) for point in tips}
                records.append(dict(parameters=[width, left, right], phase=phase,
                                    symmetry=symmetry, no_exterior=len(no_exterior),
                                    continuation_failures=len(failures),
                                    irregular_capacity=len(irregular), slot_capacity=len(pool)))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    boundaries = boundary_controls()
    fixtures = [('marked_gate', marked_gate_modules()), ('two_tips', two_tip_modules()),
                ('overloaded_tile', overloaded_tile_modules()), ('zero_credit_frozen', family())]
    fixtures += [('four_way_%d' % width, four_way_modules(width)) for width in (8, 14)]
    fixtures += [('star_%d' % width, star_modules(width)) for width in (6, 14)]
    fixtures += [('chain_%d' % amount, chain_modules(amount)) for amount in (1, 2, 3)]
    fixtures += [('rotor', [rotor()])]
    for width in (6, 14):
        fixtures.append(('opposed_%d' % width, opposed_bands(width, 4)[1]))
        fixtures.append(('occupied_%d' % width, occupied_bands(width)[1]))
    records = []
    for name, modules in fixtures:
        for symmetry, phase, offset, current, moved in phase_images(modules):
            slots = inspect_slots(current, moved)
            physical = inspect(current, moved, require_frozen=False)
            assert slots['marked_sides'] == physical['marked_sides']
            assert slots['irregular_events'] == physical['irregular_source_events']
            assert slots['positive'] == physical['positive_modules']
            assert slots['negative_mass'] == physical['negative_module_mass']
            lower_bound = (slots['positive']-slots['negative_mass']-2*slots['minus_one']-
                           2*slots['vertical_phase']+physical['residual_square_credit'])
            assert lower_bound <= physical['two_guard_credit'] <= physical['half_area']-physical['objective']
            records.append(dict(fixture=name, symmetry=symmetry, phase=phase, **slots,
                                square_credit=physical['residual_square_credit'],
                                guaranteed_slack=lower_bound, finer_slack=physical['two_guard_credit'],
                                actual_slack=physical['half_area']-physical['objective']))
    arguments.output.write_text(json.dumps(dict(status='PASS', boundary_images=boundaries,
        physical=records, summary=dict(boundary_images=len(boundaries), physical_images=len(records),
        marked_images=sum(record['marked_sides'] > 0 for record in records),
        row_shifted_marked_images=sum(any(item['source_charge'] <= -5 for item in record['marked_assignments'])
                                     for record in records)),
        scope='Independent controls for the written all-phase boundary classification and single-use joint slot theorem; no universal residual/grid bound inferred.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS', boundary_images=len(boundaries), physical_images=len(records),
                         row_shifted_marked_images=sum(any(item['source_charge'] <= -5
                             for item in record['marked_assignments']) for record in records))))


if __name__ == '__main__':
    main()
