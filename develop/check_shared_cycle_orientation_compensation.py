"""Reconstruct shared-cycle surgeries and their signed orientation budget."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory, matchings
from check_terminal_cancellation_and_stranded_demand import components


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for first in range(minimum, total+1):
        for remaining in partitions(total-first, first):
            yield (first,)+remaining


def model(sources, cycle_sizes):
    terminals = {('t', index) for index in range(sources)}
    terminals |= {('p', index) for index in range(sources)}
    kinds = {point: 'TP' if point[0] == 't' else 'BP' for point in terminals}
    actual, auxiliary, colours, cycles = [], [], {}, []
    offset = 0
    for size in cycle_sizes:
        cycle = [('x', offset+index) for index in range(2*size)]
        for index in range(size):
            auxiliary.append((cycle[2*index], cycle[2*index+1]))
            actual.append((cycle[2*index+1], cycle[(2*index+2) % len(cycle)]))
        colours.update({point: 1 if index % 2 == 0 else -1
                        for index, point in enumerate(cycle)})
        cycles.append(set(cycle))
        offset += len(cycle)
    return terminals | set(colours), actual, auxiliary, kinds, colours, cycles


def verify(vertices, actual, replacement, kinds, colours, cycles, totals):
    covered = [point for edge in replacement for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == vertices
    records = components(vertices, actual+replacement)
    counts = inventory(records, kinds)
    sources = len(kinds)//2
    assert counts['alpha'] == counts['beta']
    assert counts['mixed'] == sources-2*counts['alpha']
    minimal_budget = len(replacement)
    for flips in itertools.product((-1, 1), repeat=len(cycles)):
        signs = {point: -1 if kind == 'TP' else 1 for point, kind in kinds.items()}
        for cycle, flip in zip(cycles, flips):
            signs.update({point: flip*colours[point] for point in cycle})
        negative = sum(signs[first] == signs[second] == -1 for first, second in replacement)
        positive = sum(signs[first] == signs[second] == 1 for first, second in replacement)
        assert negative == positive
        assert counts['alpha'] <= negative and counts['beta'] <= positive
        if negative == 0:
            assert counts['alpha'] == counts['beta'] == 0
            assert counts['mixed'] == sources
            totals['coherent_orientation_certificates'] += 1
        for record in records:
            local_edges = [edge for edge in replacement if edge[0] in record['vertices']]
            assert all(set(edge) <= record['vertices'] for edge in local_edges)
            charge = sum(signs[first]+signs[second] for first, second in local_edges)
            assert charge == sum(signs[point] for point in record['ends'])
            if not record['ends']:
                assert charge == 0
        minimal_budget = min(minimal_budget, negative)
        totals['signed_orientation_controls'] += 1
    owners = {point: 0 for point in kinds}
    base = {point: 0 if kind == 'TP' else 1 for point, kind in kinds.items()}
    for index, cycle in enumerate(cycles, 1):
        owners.update({point: index for point in cycle})
        base.update({point: int(colours[point] == 1) for point in cycle})
    constraints = [(owners[first], owners[second], 1 ^ base[first] ^ base[second])
                   for first, second in replacement]
    constraints = [edge for edge in constraints if edge[0] != edge[1] or edge[2] != 0]
    adjacency = {node: [] for node in range(len(cycles)+1)}
    for first, second, parity in constraints:
        adjacency[first].append((second, parity))
        adjacency[second].append((first, parity))
    flips, connected = {}, 0
    for root in adjacency:
        if root in flips:
            continue
        flips[root] = 0
        connected += 1
        pending = [root]
        while pending:
            current = pending.pop()
            for following, parity in adjacency[current]:
                if following not in flips:
                    flips[following] = flips[current] ^ parity
                    pending.append(following)
    assert flips[0] == 0
    violations = sum(flips[first] ^ flips[second] != parity
                     for first, second, parity in constraints)
    rank = len(constraints)-len(adjacency)+connected
    signs = {point: 1 if base[point] ^ flips[owners[point]] else -1 for point in vertices}
    negative = sum(signs[first] == signs[second] == -1 for first, second in replacement)
    positive = sum(signs[first] == signs[second] == 1 for first, second in replacement)
    assert violations == 2*negative == 2*positive and violations <= rank
    assert counts['alpha'] <= negative <= rank//2
    assert (violations == 0) == (minimal_budget == 0)
    if rank <= 1:
        assert counts['alpha'] == counts['beta'] == 0
        totals['low_cycle_rank_complete_repairs'] += 1
    if violations and counts['alpha'] == 0:
        totals['incoherent_certificate_but_no_residual_alpha'] += 1
    totals['parity_forest_and_rank_controls'] += 1
    return counts, minimal_budget


def exhaustive_controls(totals):
    for sources in (1, 2, 3):
        for pairs in range(min(3, 5-sources)+1):
            for cycle_sizes in partitions(pairs):
                vertices, actual, auxiliary, kinds, colours, cycles = model(sources, cycle_sizes)
                for replacement in matchings(sorted(vertices)):
                    if 2*len(replacement) != len(vertices):
                        continue
                    verify(vertices, actual, replacement, kinds, colours, cycles, totals)
                    operations = components(vertices, auxiliary+replacement)
                    if all(not record['ends'] or
                           {kinds[point] for point in record['ends']} == {'TP', 'BP'}
                           for record in operations):
                        totals['tp_bp_paths_with_optional_cycle_exchanges'] += 1
                        if all(record['ends'] or len(record['vertices']) == 2 for record in operations):
                            totals['pure_distinct_source_donor_augmentation_replacements'] += 1
                    totals['arbitrary_balanced_auxiliary_replacements'] += 1


def family_control(word, totals):
    sources = len(word)
    vertices, actual, auxiliary, kinds, colours, cycles = model(sources, (sources,))
    replacement, paths = [], []
    for index, direction in enumerate(word):
        first, second = ('x', 2*index+direction), ('x', 2*index+1-direction)
        source, donor = ('t', index), ('p', index)
        replacement.extend([(source, first), (second, donor)])
        paths.append([source, first, second, donor])
    assert len({point for path in paths for point in path}) == 4*sources
    assert len({path[0] for path in paths}) == len({path[-1] for path in paths}) == sources
    assert {frozenset(path[1:3]) for path in paths} == {frozenset(edge) for edge in auxiliary}
    counts, budget = verify(vertices, actual, replacement, kinds, colours, cycles, totals)
    drops = sum(first == 1 and second == 0 for first, second in zip(word, word[1:]+word[:1]))
    rises = sum(first == 0 and second == 1 for first, second in zip(word, word[1:]+word[:1]))
    assert drops == rises == counts['alpha'] == counts['beta']
    assert counts['mixed'] == sources-2*drops
    assert budget == min(sum(word), sources-sum(word))
    tails = {(('T' if point[0] == 't' else 'P'), point[1]): kinds[point] for point in kinds}
    full_actual = actual+[(point, (('T' if point[0] == 't' else 'P'), point[1])) for point in kinds]
    full = inventory(components(vertices | set(tails), full_actual+replacement), tails)
    assert full == counts
    totals['cyclic_word_family_controls'] += 1
    return dict(length=sources, word=''.join(map(str, word)), alpha=counts['alpha'],
                beta=counts['beta'], mixed=counts['mixed'], minimum_orientation_budget=budget,
                full_actual_endpoints=len(vertices)+len(tails))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    exhaustive_controls(totals)
    for length in range(2, 13):
        for word in itertools.product((0, 1), repeat=length):
            result = family_control(word, totals)
            if word in [(0, 0), (0, 1), (0, 0, 0, 1, 1, 1)]:
                examples.append(result)
    for length in range(13, 129):
        for word in [tuple([0]*length), tuple(index % 2 for index in range(length)),
                     tuple([0]*(length//2)+[1]*(length-length//2))]:
            result = family_control(word, totals)
            if length == 128:
                examples.append(result)
    record = dict(status='PASS', totals=dict(totals), examples=examples,
                  scope='All perfect auxiliary replacements on reduced models with 1..3 '
                  'sources, 0..3 cycle pairs and at most ten reduced vertices, with all '
                  'partitions into original cycles and all cycle colour flips. All binary '
                  'words length 2..12 and three word families length 13..128. '
                  'Independent full-tail reconstruction for the word family. '
                  'No frozen grid embedding, universal geometric existence or finite-to-infinite inference.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
