#!/usr/bin/env python3
"""Finite controls for guarded half donors and single-use cap certificates."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_branching_interval_compensation import band_region
from check_cross_component_compensation import band_ledger, encode, witness_record
from check_mixed_neutral_donors import compatible, wide_mixed_obstacle
from check_pressure_bands import local_controls
from check_residual_corridors import direct_check, graph_record, transformed
from grid_three_step_patterns import Conflict, Patch, point
from search_residual_paths import partial_check
from verify_grid_five_sixths import canonical


def rotate(vertex, turns):
    for iteration in range(turns):
        vertex = vertex[1], 1-vertex[0]
    return vertex


def cap_pattern(kind, turns):
    states = {}
    edges = []
    caps = [((0, -1), 'PTTB' if kind == 'LL' else 'TPBT'),
            ((0, 1), 'TPBT' if kind == 'RR' else 'PTTB')]
    for tile, labels in caps:
        for corner, label in zip(((0, 0), (0, 1), (1, 0), (1, 1)), labels):
            vertex = point(tile, corner)
            states[rotate(vertex, turns)] = label
            if label == 'P':
                edges.append((rotate(vertex, turns),
                              rotate((vertex[0]-1, vertex[1]), turns)))
    return states, edges


def certificate_controls():
    certificates = list(itertools.product(('RL', 'RR', 'LL'), range(4)))
    rejected = {}
    guard_pairs = []
    for first, second in itertools.combinations(certificates, 2):
        patch = Patch()
        reason = None
        try:
            for kind, turns in (first, second):
                states, edges = cap_pattern(kind, turns)
                for vertex, label in states.items():
                    patch.cell(vertex, label)
                for edge in edges:
                    patch.edge(*edge)
            partial_check(patch)
        except Conflict as error:
            reason = str(error)
        if reason is None:
            assert first[0] != 'RL' and second[0] != 'RL'
            assert first[1] % 2 != second[1] % 2
            parent = {rotate((-2+row, column), first[1])
                      for row, column in itertools.product(range(2), repeat=2)}
            labels = [patch.states[vertex] for vertex in parent]
            assert labels.count('T') == 2 and labels.count('P') == 1
            guard_pairs.append([first, second])
            reason = 'saturated_parent_with_P'
        rejected[reason] = rejected.get(reason, 0)+1
    assert sum(rejected.values()) == 66 and len(guard_pairs) == 4
    return dict(certificates=12, distinct_pairs=66, rejections=rejected,
                compatible_caps_rejected_by_parent_guard=guard_pairs)


def local_bound_controls():
    accepted = []
    for upper_left, lower_right in itertools.product('BP', 'BPT'):
        for attachments in range(2 if lower_right == 'P' else 1):
            selected = int(lower_right == 'T')
            endpoints = int(upper_left == 'P')+int(lower_right == 'P')
            charge_twice = 2*selected+endpoints+attachments-4
            assert charge_twice <= -1
            accepted.append(dict(labels=upper_left+'B/B'+lower_right,
                                 downward_saturated_attachments=attachments,
                                 charge_twice=charge_twice))
    return dict(states=accepted, scope='Necessary local possibilities; no global realizability inferred.')


def neutral_gap_controls():
    states = local_controls()['neutral_states']
    triples = []
    for first, middle, last in itertools.product(states, repeat=3):
        exits = first['exit_corners']
        if exits not in ([2], [3]) or last['exit_corners'] != exits:
            continue
        if middle['exit_corners'] or not compatible(first, middle) or not compatible(middle, last):
            continue
        orientation = 'R' if exits == [3] else 'L'
        labels = middle['labels'].replace('/', '')
        guarded = labels[2 if orientation == 'R' else 3] != 'B'
        assert guarded == (middle['labels'] in ('PB/PT', 'PP/PP')
                           if orientation == 'R' else middle['labels'] in ('BP/TP', 'PP/PP'))
        triples.append(dict(orientation=orientation, labels=[state['labels']
                            for state in (first, middle, last)], occupied_guard=guarded))
    return dict(necessary_triples=triples,
                scope='Necessary pressure/label compatibility only; not full matching realizability.')


def unguarded_middle_controls():
    states = local_controls()['neutral_states']
    transitions = [[second for second, candidate in enumerate(states)
                    if compatible(first, candidate)] for first in states]
    triples = []
    for first, middle, last in itertools.product(range(len(states)), repeat=3):
        if states[first]['exit_corners'] != [3] or states[last]['exit_corners'] != [3]:
            continue
        if states[middle]['exit_corners']:
            continue
        if middle not in transitions[first] or last not in transitions[middle]:
            continue
        labels = states[middle]['labels']
        if labels not in ('PP/BT', 'TB/BT'):
            continue
        triples.append(dict(labels=labels, left=states[first]['labels'],
                            right=states[last]['labels']))
    assert {item['labels'] for item in triples} == {'PP/BT', 'TB/BT'}
    return dict(width_one_unguarded_middle_states=sorted({item['labels'] for item in triples}),
                compatible_triples=triples,
                scope='Finite necessary-state classification; no global matching realizability inferred.')


def unguarded_transition_controls():
    states = local_controls()['neutral_states']
    transitions = {}
    for label in ('PP/BT', 'TB/BT'):
        state = next(item for item in states if item['labels'] == label)
        transitions[label] = sorted(
            candidate['labels'] + ('/R' if candidate['exit_corners'] == [3]
                                   else '/L' if candidate['exit_corners'] == [2] else '')
            for candidate in states if compatible(state, candidate))
    assert transitions['PP/BT'] == ['PP/BP/R', 'PP/BT']
    assert transitions['TB/BT'] == [
        'BT/PB/L', 'BT/TB', 'PB/PT', 'PP/BP/R', 'PP/BT',
        'PP/PB/L', 'PP/PP', 'TB/BP/R', 'TB/BT']
    return dict(successors=transitions,
                interpretation='PP/BT is a pure delay state; TB/BT can turn or continue.',
                scope='Finite necessary-state transitions; no global matching realizability inferred.')


def local_witness(kind):
    patch = Patch()
    states, edges = cap_pattern('RR', 0)
    for vertex, label in states.items():
        patch.cell(vertex, label)
    for edge in edges:
        patch.edge(*edge)
    if kind == 'sharp':
        patch.cell((1, 1), 'T')
        patch.edge((0, 0), (-1, 0))
        shift = (4, 2)
    elif kind == 'blank_guard':
        patch.cell((0, 0), 'T')
        patch.cell((1, 1), 'T')
        for tile, labels in [((-1, -1), 'TBBP'), ((-1, 0), 'TBBT'),
                             ((-1, 1), 'TBBP')]:
            for corner, label in zip(((0, 0), (0, 1), (1, 0), (1, 1)), labels):
                patch.cell(point(tile, corner), label)
        for column in (-2, 0, 2):
            patch.edge((-3, column), (-3, column+1))
        shift = (4, 2)
    elif kind == 'saturated_parent':
        patch.attachment((0, 0), (0, 0), (0, 1))
        patch.attachment((0, 0), (1, 1), (1, 0))
        shift = (2, 2)
    else:
        raise ValueError(kind)
    patch.finish()
    def moved(vertex):
        return vertex[0]+shift[0], vertex[1]+shift[1]
    selected = {moved(vertex) for vertex, label in patch.states.items() if label == 'T'}
    matching = [(moved(first), moved(second)) for first, second in patch.mate.items()
                if first < second]
    region = {moved(vertex) for vertex in itertools.product(range(2), repeat=2)}
    return (6, 6, selected, matching), region


def guarded_recognition(configuration, tile_column, orientation):
    rows, columns, selected, matching = configuration
    endpoints = {vertex for edge in matching for vertex in edge}
    def label(vertex):
        return 'T' if vertex in selected else 'P' if vertex in endpoints else 'B'
    cap_labels = 'TPBT' if orientation == 'R' else 'PTTB'
    for column in (tile_column-1, tile_column+1):
        vertices = [(4+row, 2*column+offset)
                    for row, offset in itertools.product(range(2), repeat=2)]
        assert ''.join(map(label, vertices)) == cap_labels
        cap_endpoint = next(vertex for vertex in vertices if label(vertex) == 'P')
        assert frozenset((cap_endpoint, (cap_endpoint[0]-1, cap_endpoint[1]))) in {
            frozenset(edge) for edge in matching}
    guard = (3, 2*tile_column+(orientation == 'L'))
    assert guard in selected | endpoints
    parent_labels = [label((2+row, 2*tile_column+offset))
                     for row, offset in itertools.product(range(2), repeat=2)]
    assert not (parent_labels.count('T') == 2 and 'P' in parent_labels)


def witness_controls():
    reports = []
    image_count = 0
    for kind, expected in (('sharp', -1), ('blank_guard', 0), ('saturated_parent', 0)):
        configuration, region = local_witness(kind)
        for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
            dimensions, selected, matching = transformed(*configuration, transpose, flip_rows, flip_columns)
            _, moved_region, _ = transformed(configuration[0], configuration[1], region, [],
                                              transpose, flip_rows, flip_columns)
            direct_check(*dimensions, selected, matching)
            canonical(*dimensions, *encode(*dimensions, selected, matching))
            ledger = band_ledger(*dimensions, selected, matching, moved_region)
            assert ledger['charge_twice'] == expected
            image_count += 1
        reports.append(witness_record(kind, configuration, region))
    wide = wide_mixed_obstacle()
    guarded_recognition(wide, 2, 'R')
    guarded_recognition(wide, 7, 'L')
    regions = [band_region(0, 0, 10), band_region(1, 1, 8),
               band_region(2, 4, 2), band_region(2, 2, 1), band_region(2, 7, 1)]
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        dimensions, selected, matching = transformed(*wide, transpose, flip_rows, flip_columns)
        assert direct_check(*dimensions, selected, matching) == 59
        canonical(*dimensions, *encode(*dimensions, selected, matching))
        claimed = set()
        charges = []
        for region in regions:
            _, moved_region, _ = transformed(wide[0], wide[1], region, [], transpose, flip_rows, flip_columns)
            ledger = band_ledger(*dimensions, selected, matching, moved_region)
            assert not claimed & set(ledger['tiles'])
            claimed.update(ledger['tiles'])
            charges.append(ledger['charge_twice'])
        residual_graph, components = graph_record(*dimensions, selected, matching)
        remainder = sum(residual_graph['deg'][tile]-2*residual_graph['r'][tile]
                        for tile in range(residual_graph['N'])
                        if tile not in claimed and residual_graph['t'][tile] < 2)
        assert charges == [2, 0, 0, -2, -2] and remainder == 0
        assert sum(charges)+remainder == 2*(59-60)
        assert 1-2/2+remainder/2 == 0
        image_count += 1
    reports.append(witness_record('6x20 guarded outside donors', wide))
    return dict(symmetry_images=image_count, witnesses=reports,
                wide_partition_charge_twice=[2, 0, 0, -2, -2],
                wide_remainder_charge_twice=0, certified_half_budget=1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED', local_bound=local_bound_controls(),
                  certificate_uniqueness=certificate_controls(), neutral_gaps=neutral_gap_controls(),
                  unguarded_middle=unguarded_middle_controls(),
                  unguarded_transitions=unguarded_transition_controls(),
                  coordinate_controls=witness_controls(),
                  scope='General lemmas are written separately. No arbitrary-grid allocation proof or new Lean claim.')
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/GUARDED_HALF_DONORS.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_branching_interval_compensation.py', 'check_cross_component_compensation.py',
        'check_mixed_neutral_donors.py', 'check_pressure_bands.py', 'check_residual_corridors.py',
        'grid_three_step_patterns.py', 'search_residual_paths.py', 'verify_grid_five_sixths.py',
        'verify_grid_short_path_compensation.py'))
    report['sha256'] = {str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                        for path in sources}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], symmetry_images=report['coordinate_controls']['symmetry_images'],
                          certificate_pairs=66, scope=report['scope']), indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
