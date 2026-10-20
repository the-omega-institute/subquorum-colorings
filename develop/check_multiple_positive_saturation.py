"""Shared-demand controls and source-level zero-reserve physical checks."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import inspect_slots, tile_of
from check_exact_event_reserve import fixtures, inspect_exact
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import positive_dimensions
from dual_guard_compensation import paired_guards
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def arithmetic_controls():
    censuses = 0
    margins = 0
    parity_cases = 0
    for amount in range(9):
        for marks in itertools.product(range(4), repeat=amount):
            unmarked = marks.count(0)
            double = marks.count(3)
            single = amount-unmarked-double
            marked = sum(bool(value & 1)+bool(value & 2) for value in marks)
            assert amount == unmarked+single+double
            assert marked == single+2*double
            for reserve in range(amount+2):
                defect = 2*reserve
                margin = amount+reserve-marked
                assert margin == unmarked+reserve-double
                assert (margin >= 0) == (2*double <= 2*unmarked+defect)
                assert (margin < 0) == (double >= unmarked+reserve+1)
                margins += 1
            censuses += 1
    for amount in range(7):
        for defects in itertools.product(range(4), repeat=amount):
            total = sum(defects)
            odd = sum(value % 2 for value in defects)
            rounded = sum((value+1)//2 for value in defects)
            assert 2*rounded == total+odd
            if total % 2 == 0:
                assert 2*(rounded-total//2) == odd
            parity_cases += 1
    return dict(source_censuses=censuses, reserve_margins=margins,
                parity_partitions=parity_cases,
                arithmetic_obstruction=dict(unmarked=0, single=0, double=2,
                    assigned_distinct_defect_units=[1, 1], total_defect=2, reserve=1,
                    separate_rounding=2, joint_margin=-1,
                    scope='Arithmetic inference counterexample only; no physical fusion asserted.'))


def inspect_sources(current, modules):
    exact = inspect_exact(current, modules)
    slots = inspect_slots(current, modules)
    marked_tiles = {tuple(record['tile']) for record in slots['marked_assignments']}
    counts = Counter()
    dimensions = []
    for module in modules:
        if module['charge'] != 1:
            continue
        width, left, right, _, _ = positive_dimensions(module)
        guard_tiles = {tile_of(guard[0]) for guard in paired_guards(module)}
        assert len(guard_tiles) == 2
        marked = len(guard_tiles & marked_tiles)
        counts[marked] += 1
        exceptional = width != 6 and (width >= 12 or max(left, right) >= 8)
        counts['exceptional'] += exceptional
        if exact['event_reserve'] == 0 and marked == 2:
            assert exceptional
        if exact['event_reserve'] == 0:
            for tile in module['receiver']:
                cells = vertices_of({tile})
                if len(cells & module['endpoints']) == 1:
                    assert len(cells & module['selected']) == 2
        dimensions.append(dict(width=width, left=left, right=right,
                               marked=marked, exceptional=exceptional))
    unmarked, single, double = (counts[index] for index in range(3))
    reserve = exact['event_reserve']
    assert exact['positive'] == unmarked+single+double
    assert exact['marked'] == single+2*double
    assert exact['exact_joint_margin'] == unmarked+reserve-double
    if reserve == 0:
        assert double <= counts['exceptional']
        assert exact['exact_joint_margin'] >= unmarked-counts['exceptional']
        if counts['exceptional'] <= unmarked:
            assert exact['exact_joint_margin'] >= 0
    return dict(**exact, unmarked_sources=unmarked, single_marked_sources=single,
                double_marked_sources=double, exceptional_sources=counts['exceptional'],
                dimensions=dimensions)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    arithmetic = arithmetic_controls()
    physical = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_sources(current, moved)))
    for amount in (1, 2, 4, 8):
        modules = [transform_module(source(6+2*(index % 3), 4+2*(index % 2), 4),
                                    (False, False, False), (0, 16*index))
                   for index in range(amount)]
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose else
                      (int(flip_row), int(flip_column)))
            current, moved = contained([transform_module(module, symmetry, offset)
                                        for module in modules])
            report = inspect_sources(current, moved)
            assert report['positive'] == amount and report['event_reserve'] == 0
            assert report['marked'] == 0 and report['exceptional_sources'] == 0
            physical.append(dict(fixture='isolated_positive_%d' % amount,
                                 symmetry=symmetry, **report))
    summary = dict(physical_images=len(physical),
                   zero_reserve_images=sum(record['event_reserve'] == 0 for record in physical),
                   positive_zero_reserve_images=sum(record['event_reserve'] == 0 and
                        record['positive'] > 0 for record in physical),
                   marked_zero_reserve_images=sum(record['event_reserve'] == 0 and
                        record['marked'] > 0 for record in physical),
                   double_marked_images=sum(record['double_marked_sources'] > 0
                                            for record in physical))
    arguments.output.write_text(json.dumps(dict(status='PASS', arithmetic=arithmetic,
        summary=summary, physical=physical,
        scope='Finite shared-demand/parity controls and complete physical source censuses. Isolated positive arrays add nonvacuous arbitrary-N zero-reserve controls but no occupied marked zero-reserve gates. The universal source-local geometry and global saturation theorem have written proofs; the arithmetic obstruction is not a physical counterexample.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', arithmetic=arithmetic, summary=summary)))


if __name__ == '__main__':
    main()
