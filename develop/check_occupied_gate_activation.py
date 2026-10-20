"""Exact gate-role controls and physical checks of positive-tip activation."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import inspect_slots, tile_of
from check_activated_singleton_budget import inspect_budget
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from check_minus_one_joint_compensation import marked_gate_modules
from check_minus_one_tip_obstructions import overloaded_tile_modules, source, two_tip_modules
from check_regular_tile_compensation import profile_counts
from check_zero_credit_tip_family import family
from degree_four_overcount import opposed_bands
from degree_three_fusion import four_way_modules, occupied_bands
from dual_guard_compensation import paired_guards
from rotor_networks import affine, chain_modules, rotor, star_modules, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def gate_roles():
    gate = (2, 2)
    cells = vertices_of({(1, 1)})
    parameters = list(itertools.product((6, 8, 14), (4, 6, 10), (4, 8, 12)))
    parameters += [(40, 30, 4), (20, 4, 30)]
    result = []
    for width, left, right in parameters:
        base = source(width, left, right)
        roles = [('A', (0, 1), 0), ('A', (0, width), 0),
                 ('F', (left, 1), left), ('F', (right, width), right)]
        for role, point, height in roles:
            for symmetry in itertools.product((False, True), repeat=3):
                root = affine(point, symmetry)
                offset = tuple(value-original for value, original in zip(gate, root))
                module = transform_module(base, symmetry, offset)
                if (set(neighbors(gate))-cells) & module['endpoints']:
                    continue
                phase = ('01' if module['charge'] == -1 else
                         '11' if profile_counts(module)[3, 0] else '10')
                predecessor = bar_direction = None
                if role == 'F':
                    previous = affine((point[0]-1, point[1]), symmetry, offset)
                    across = affine((point[0], point[1]+(1 if point[1] == 1 else -1)),
                                    symmetry, offset)
                    predecessor = tuple(value-original for value, original in zip(previous, gate))
                    bar_direction = tuple(value-original for value, original in zip(across, gate))
                result.append(dict(parameters=(width, left, right), role=role, height=height,
                                   phase=phase, predecessor=predecessor, bar_direction=bar_direction,
                                   module=module))
    return parameters, result


def local_controls():
    incoming_parameters, candidates = gate_roles()
    positive_parameters = list(itertools.product((6, 8, 14), (4, 8, 12), (4, 6, 14)))
    positive_parameters += [(40, 40, 4), (40, 4, 40)]
    counts = Counter()
    width_six_survivors = Counter()
    for width, left, right in positive_parameters:
        positive = source(width, left, right)
        for candidate in candidates:
            foreign = candidate['module']['endpoints']
            if positive['endpoints'] & foreign:
                continue
            phase = candidate['phase']
            height = candidate['height']
            counts[phase] += 1
            if phase == '10':
                assert candidate['role'] == 'F'
                assert candidate['predecessor'] == (1, 0)
                assert candidate['bar_direction'] == (0, -1)
                assert height >= left and (left+1, 2) in foreign
            if width == 6:
                assert phase in ('10', '11') and candidate['role'] == 'F'
                assert candidate['predecessor'] == (1, 0)
                if phase == '11':
                    assert candidate['bar_direction'] == (0, 1) and height >= right
                if left <= right:
                    assert (left+1, 2) in foreign
                width_six_survivors[phase] += 1
    assert all(counts[phase] > 0 for phase in ('01', '10', '11'))
    assert all(width_six_survivors[phase] > 0 for phase in ('10', '11'))
    return dict(incoming_parameters=len(incoming_parameters),
                positive_parameters=len(positive_parameters),
                source_local_gate_candidates=len(candidates),
                disjoint_gate_cases=dict(counts), width_six_disjoint_cases=dict(width_six_survivors),
                scope='All four A/F roles and eight isometries at a fixed gate for the listed dimensions; the translation is uniquely determined. Dimension coverage is finite; universal dimension arguments are written and separately formalized.')


def positive_dimensions(module):
    for symmetry in itertools.product((False, True), repeat=3):
        oriented = {affine(point, symmetry) for point in module['endpoints']}
        offset = -min(point[0] for point in oriented), 1-min(point[1] for point in oriented)
        endpoints = {affine(point, symmetry, offset) for point in module['endpoints']}
        width = max(point[1] for point in endpoints)
        if width < 6 or width % 2:
            continue
        left = max(point[0] for point in endpoints if point[1] == 1)
        right = max(point[0] for point in endpoints if point[1] == width)
        if min(left, right) < 4 or left % 2 or right % 2:
            continue
        reference = source(width, left, right)
        selected = {affine(point, symmetry, offset) for point in module['selected']}
        if endpoints == reference['endpoints'] and selected == reference['selected']:
            return width, left, right, symmetry, offset
    raise AssertionError('Positive source is not a complete permitted U.')


def physical_control(current, modules):
    report = inspect_budget(current, modules)
    slots = inspect_slots(current, modules)
    endpoints = set.union(*(module['endpoints'] for module in modules))
    sides = {}
    dimensions = {}
    for index, module in enumerate(modules):
        if module['charge'] != 1:
            continue
        dimensions[index] = positive_dimensions(module)
        terminal = []
        for tile in module['receiver']:
            cells = vertices_of({tile})
            own, support = cells & module['endpoints'], cells & module['selected']
            if len(own) == 1 and len(support) == 2:
                terminal.append((next(iter(own)), bool(support & endpoints)))
        assert len(terminal) == 2
        for chosen, anchor, _, _ in paired_guards(module):
            inward = tuple(value-original for value, original in zip(chosen, anchor))
            projection = lambda point: sum(value*direction for value, direction in zip(point, inward))
            matching = [(point, activated) for point, activated in terminal
                        if projection(point) == projection(anchor)]
            assert len(matching) == 1 and tile_of(chosen) not in sides
            sides[tile_of(chosen)] = index, matching[0]
    phase_ten_gates = 0
    shorter_width_six_gates = 0
    for assignment in slots['marked_assignments']:
        if assignment['kind'] != 'gate':
            continue
        index, (tip, activated) = sides[tuple(assignment['tile'])]
        foreign = modules[assignment['owner']]
        if foreign['charge'] <= -5 and profile_counts(foreign)[3, 0] == 0:
            phase_ten_gates += 1
            assert activated
        width, left, right, symmetry, offset = dimensions[index]
        tip_height = affine(tip, symmetry, offset)[0]
        if width == 6 and tip_height == min(left, right):
            shorter_width_six_gates += 1
            assert activated
    eligible = all(value[0] == 6 for value in dimensions.values())
    unequal = sum(left != right for _, left, right, _, _ in dimensions.values())
    if eligible:
        assert report['positive_activated']+report['blank_marks'] >= report['marked']-unequal
        bound = report['positive']-(report['marked']+unequal)//2
        assert report['guaranteed_slack'] >= bound
        if unequal <= 1 or report['marked']+unequal <= 2*report['positive']+1:
            assert bound >= 0
    return dict(positive=report['positive'], marked=report['marked'],
                phase_ten_gates=phase_ten_gates, shorter_width_six_gates=shorter_width_six_gates,
                all_positive_width_six=eligible, unequal_positive=unequal,
                positive_activation=report['positive_activated'], blank_marks=report['blank_marks'],
                event_reserve=report['event_reserve'], guaranteed_slack=report['guaranteed_slack'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    local = local_controls()
    fixtures = [('marked_gate', marked_gate_modules()), ('two_tips', two_tip_modules()),
                ('overloaded', overloaded_tile_modules()), ('zero_credit', family()), ('rotor', [rotor()])]
    fixtures += [('four_way_%d' % width, four_way_modules(width)) for width in (8, 14)]
    fixtures += [('star_%d' % width, star_modules(width)) for width in (6, 14)]
    fixtures += [('chain_%d' % amount, chain_modules(amount)) for amount in (1, 2, 3)]
    for width in (6, 8, 14, 40):
        fixtures.append(('opposed_%d' % width, opposed_bands(width, 4)[1]))
        fixtures.append(('occupied_%d' % width, occupied_bands(width)[1]))
    records = []
    for name, modules in fixtures:
        for symmetry, phase, _, current, moved in phase_images(modules):
            records.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                **physical_control(current, moved)))
    summary = dict(physical_images=len(records),
                   phase_ten_gate_images=sum(record['phase_ten_gates'] > 0 for record in records),
                   shorter_width_six_gate_images=sum(record['shorter_width_six_gates'] > 0
                                                     for record in records),
                   positive_width_six_images=sum(record['all_positive_width_six'] and
                                                record['positive'] > 0 for record in records))
    assert summary['positive_width_six_images']
    arguments.output.write_text(json.dumps(dict(status='PASS', local=local, summary=summary,
        physical=records, scope='Finite role and complete physical controls. General gate-role normalization, compulsory-support activation and the all-parameter width-six theorem are written, with separately scoped Lean coordinate and arithmetic declarations. Universal mixed occupied-gate allocation remains open.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', local=local, summary=summary)))


if __name__ == '__main__':
    main()
