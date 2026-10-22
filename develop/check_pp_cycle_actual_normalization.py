"""Check legal actual PP-cycle normalization and subsequent compensation."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory, matchings
from check_exchange_terminal_nonunique import fixture, graft
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_shared_cycle_orientation_compensation import model, partitions
from check_terminal_cancellation_and_stranded_demand import components


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def normalize(vertices, actual, auxiliary, totals):
    before = components(vertices, actual+auxiliary)
    cycle_vertices = set().union(*(record['vertices'] for record in before if not record['ends']))
    following = [edge for edge in actual if edge[0] not in cycle_vertices]
    following += [edge for edge in auxiliary if edge[0] in cycle_vertices]
    covered = [point for edge in following for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == vertices
    assert len(following) == len(actual)
    after = components(vertices, following+auxiliary)
    assert all(len(record['vertices']) == 2 for record in after if not record['ends'])
    original_paths = {(frozenset(record['vertices']), tuple(record['ends']))
                      for record in before if record['ends']}
    final_paths = {(frozenset(record['vertices']), tuple(record['ends']))
                   for record in after if record['ends']}
    assert original_paths == final_paths
    totals['normalization_controls'] += 1
    totals['nontrivial_cycles_normalized'] += sum(not record['ends'] and len(record['vertices']) > 2
                                                  for record in before)
    return following


def compensate(vertices, actual, auxiliary, replacement, kinds, totals):
    tails = {(('T' if point[0] == 't' else 'P'), point[1]): kinds[point] for point in kinds}
    full_actual = actual+[(point, (('T' if point[0] == 't' else 'P'), point[1])) for point in kinds]
    full_vertices = vertices | set(tails)
    full_kinds = kinds | tails
    old_counts = inventory(components(full_vertices, full_actual+auxiliary), full_kinds)
    assert old_counts['alpha'] == old_counts['beta'] == len(kinds)//2
    following = normalize(full_vertices, full_actual, auxiliary, totals)
    middle = inventory(components(full_vertices, following+auxiliary), full_kinds)
    assert all(old_counts[kind] == middle[kind] for kind in ('alpha', 'beta', 'mixed'))
    final = inventory(components(full_vertices, following+replacement), tails)
    assert final['alpha'] == final['beta'] == 0
    assert final['mixed'] == len(kinds)//2
    totals['complete_simultaneous_compensation_controls'] += 1


def abstract_controls(totals):
    for sources in (1, 2, 3):
        for pairs in range(min(3, 5-sources)+1):
            for cycle_sizes in partitions(pairs):
                vertices, actual, auxiliary, kinds, _, _ = model(sources, cycle_sizes)
                for replacement in matchings(sorted(vertices)):
                    if 2*len(replacement) != len(vertices):
                        continue
                    operations = components(vertices, auxiliary+replacement)
                    if not all(not record['ends'] or
                               {kinds[point] for point in record['ends']} == {'TP', 'BP'}
                               for record in operations):
                        continue
                    compensate(vertices, actual, auxiliary, replacement, kinds, totals)
                    totals['small_distinct_donor_augmentation_controls'] += 1


def word_control(word, totals):
    vertices, actual, auxiliary, kinds, _, _ = model(len(word), (len(word),))
    replacement = []
    for index, direction in enumerate(word):
        replacement += [(('t', index), ('x', 2*index+direction)),
                        (('x', 2*index+1-direction), ('p', index))]
    compensate(vertices, actual, auxiliary, replacement, kinds, totals)
    totals['all_direction_word_repairs'] += 1


def physical_controls(totals):
    bases = [fixture()]
    bases += [graft(width, height) for width, height in itertools.product((6, 10, 22), (4, 8, 18))]
    for base, symmetry, phase in itertools.product(bases, itertools.product((False, True), repeat=3),
                                                  itertools.product((0, 1), repeat=2)):
        shape, selected, matching = transformed(*base, *symmetry)
        shift = lambda point: (point[0]+2+phase[0], point[1]+2+phase[1])
        current = (2*((shape[0]+5+phase[0])//2), 2*((shape[1]+5+phase[1])//2),
                   {shift(point) for point in selected},
                   [tuple(shift(point) for point in edge) for edge in matching])
        direct_check(*current)
        vertices = {point for edge in current[3] for point in edge}
        bands = whole_bands(current)
        auxiliary = [tuple(column) for band in bands for column in band if set(column) <= vertices]
        mate = {point: other for band in bands for column in band
                for point, other in (column, column[::-1])}
        covered = {point for edge in auxiliary for point in edge}
        kinds = {point: 'TP' if mate[point] in current[2] else 'BP' for point in vertices-covered}
        old_counts = inventory(components(vertices, current[3]+auxiliary), kinds)
        following = normalize(vertices, current[3], auxiliary, totals)
        new = (*current[:3], following)
        direct_check(*new)
        assert frozen_certificate(current)[0] == frozen_certificate(new)[0] == vertices
        new_counts = inventory(components(vertices, following+auxiliary), kinds)
        assert all(old_counts[kind] == new_counts[kind] for kind in ('alpha', 'beta', 'mixed'))
        assert {point for edge in following for point in edge} == vertices
        totals['physical_exchange_terminal_controls'] += 1
        totals['physical_controls_with_changed_actual_matching'] += (
            {frozenset(edge) for edge in current[3]} != {frozenset(edge) for edge in following})


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    abstract_controls(totals)
    for length in range(2, 13):
        for word in itertools.product((0, 1), repeat=length):
            word_control(word, totals)
    for length in range(13, 129):
        for word in [tuple([0]*length), tuple(index % 2 for index in range(length)),
                     tuple([0]*(length//2)+[1]*(length-length//2))]:
            word_control(word, totals)
    physical_controls(totals)
    record = dict(status='PASS', totals=dict(totals),
                  scope='Actual M-to-A exchanges on closed PP cycles; independent endpoint '
                  'coverage and old open-strand preservation; all qualifying small replacements '
                  'from shared-cycle controls and all 8536 cyclic-word controls. Physical '
                  'exchange-terminal nonunique core and nine elbow grafts, eight symmetries, '
                  'four band phases. Freezing after exchange checked for these controls only; '
                  'no general fixed-matching freezing invariance or universal linkage existence.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
