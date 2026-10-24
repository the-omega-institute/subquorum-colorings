"""Check fixed mixed-relay signs, endpoint incidence and an open obstruction."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_component_isolated_auxiliary_compensation import inventory, matchings
from check_shared_cycle_orientation_compensation import partitions
from check_terminal_cancellation_and_stranded_demand import components


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def model(sources, relay_sizes, cycle_sizes):
    chosen = {('t', index, 0): 'TP' for index in range(sources)}
    chosen.update({('p', index, 0): 'BP' for index in range(sources)})
    vertices, actual, auxiliary, free, cycles = set(chosen), [], [], {}, []
    colours = {point: -1 if kind == 'TP' else 1 for point, kind in chosen.items()}
    for index, size in enumerate(relay_sizes):
        path = [('m', index, position) for position in range(2*size+2)]
        vertices.update(path)
        actual += list(zip(path[::2], path[1::2]))
        auxiliary += list(zip(path[1:-1:2], path[2:-1:2]))
        free[path[0]], free[path[-1]] = 'TP', 'BP'
        colours.update({point: 1 if position % 2 == 0 else -1
                        for position, point in enumerate(path)})
    for index, size in enumerate(cycle_sizes):
        cycle = [('c', index, position) for position in range(2*size)]
        vertices.update(cycle)
        auxiliary += list(zip(cycle[::2], cycle[1::2]))
        actual += [(cycle[2*position+1], cycle[(2*position+2) % len(cycle)])
                   for position in range(size)]
        colours.update({point: 1 if position % 2 == 0 else -1
                        for position, point in enumerate(cycle)})
        cycles.append(set(cycle))
    return vertices, actual, auxiliary, chosen, free, colours, cycles


def forest_budget(replacement, colours, cycles, counts):
    owners = {point: 0 for point in colours}
    for index, cycle in enumerate(cycles, 1):
        owners.update({point: index for point in cycle})
    base = {point: int(sign == 1) for point, sign in colours.items()}
    constraints = [(owners[first], owners[second], 1 ^ base[first] ^ base[second])
                   for first, second in replacement]
    constraints = [edge for edge in constraints if edge[0] != edge[1] or edge[2]]
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
    errors = sum(flips[first] ^ flips[second] != parity
                 for first, second, parity in constraints)
    rank = len(constraints)-len(adjacency)+connected
    signs = {point: 1 if base[point] ^ flips[owners[point]] else -1 for point in colours}
    negative = sum(signs[first] == signs[second] == -1 for first, second in replacement)
    positive = sum(signs[first] == signs[second] == 1 for first, second in replacement)
    assert errors == 2*negative == 2*positive and errors <= rank
    assert counts['alpha'] <= negative <= rank//2
    return errors, rank


def verify(data, replacement, totals):
    vertices, actual, auxiliary, chosen, free, colours, cycles = data
    domain = vertices-set(free)
    covered = [point for edge in replacement for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == domain
    assert {point for edge in actual for point in edge} == vertices-set(chosen)
    assert {point for edge in auxiliary for point in edge} == vertices-set(chosen)-set(free)
    assert all(colours[first]+colours[second] == 0 for first, second in actual+auxiliary)
    physical = chosen | free
    records = components(vertices, actual+replacement)
    counts = inventory(records, physical)
    sources, relays = len(chosen)//2, len(free)//2
    assert counts['alpha'] == counts['beta']
    assert counts['mixed'] == sources+relays-2*counts['alpha']
    minimum = len(replacement)
    for flips in itertools.product((-1, 1), repeat=len(cycles)):
        signs = dict(colours)
        for cycle, flip in zip(cycles, flips):
            signs.update({point: colours[point]*flip for point in cycle})
        negative = sum(signs[first] == signs[second] == -1 for first, second in replacement)
        positive = sum(signs[first] == signs[second] == 1 for first, second in replacement)
        assert negative == positive and counts['alpha'] <= negative
        for record in records:
            local = record['vertices']
            new_edges = [edge for edge in replacement if edge[0] in local]
            old_edges = [edge for edge in actual if edge[0] in local]
            assert all(set(edge) <= local for edge in new_edges+old_edges)
            new_ends = [point for edge in new_edges for point in edge]
            old_ends = [point for edge in old_edges for point in edge]
            assert Counter(new_ends+list(local & set(free))) == Counter(old_ends+list(local & set(chosen)))
            charge = sum(signs[point] for point in new_ends)
            physical_charge = sum(-1 if physical[point] == 'TP' else 1 for point in record['ends'])
            assert charge == physical_charge
            if record['ends'] and not new_edges:
                assert {physical[point] for point in record['ends']} == {'TP', 'BP'}
                totals['retained_mixed_paths_without_auxiliary_edges'] += 1
        if negative == 0:
            assert counts['alpha'] == counts['beta'] == 0
            totals['coherent_mixed_relay_certificates'] += 1
        minimum = min(minimum, negative)
        totals['signed_mixed_relay_controls'] += 1
    errors, rank = forest_budget(replacement, colours, cycles, counts)
    assert (errors == 0) == (minimum == 0)
    if rank <= 1:
        assert counts['alpha'] == counts['beta'] == 0
        totals['low_rank_complete_mixed_repairs'] += 1
    totals['mixed_parity_rank_controls'] += 1
    tails = {(('T' if point[0] == 't' else 'P'), point[1], 0): kind for point, kind in chosen.items()}
    full_actual = actual+[(point, (('T' if point[0] == 't' else 'P'), point[1], 0)) for point in chosen]
    full_vertices = vertices | set(tails)
    original = inventory(components(full_vertices, full_actual+auxiliary), physical | tails)
    assert (original['alpha'], original['beta'], original['mixed']) == (sources, sources, relays)
    final = inventory(components(full_vertices, full_actual+replacement), free | tails)
    assert final == counts
    totals['full_tail_reconstructions'] += 1
    return counts, minimum, rank


def perfect_matchings(vertices, edges):
    if not vertices:
        yield []
        return
    first = min(vertices)
    for second in sorted(vertices-{first}):
        if frozenset((first, second)) in edges:
            for following in perfect_matchings(vertices-{first, second}, edges):
                yield [(first, second)]+following


def obstruction(totals):
    data = model(1, (1,), ())
    source, donor = ('t', 0, 0), ('p', 0, 0)
    first, second = ('m', 0, 1), ('m', 0, 2)
    bad, good = [(source, first), (second, donor)], [(source, second), (first, donor)]
    bad_counts, bad_budget, bad_rank = verify(data, bad, totals)
    good_counts, good_budget, good_rank = verify(data, good, totals)
    assert (bad_counts['alpha'], bad_counts['beta'], bad_counts['mixed'], bad_budget, bad_rank) == (1, 1, 0, 1, 2)
    assert (good_counts['alpha'], good_counts['beta'], good_counts['mixed'], good_budget, good_rank) == (0, 0, 2, 0, 0)
    vertices, actual, auxiliary, chosen, free, _, _ = data
    tails = {(('T' if point[0] == 't' else 'P'), point[1], 0) for point in chosen}
    full_actual = actual+[(point, (('T' if point[0] == 't' else 'P'), point[1], 0)) for point in chosen]
    edges = {frozenset(edge) for edge in full_actual+auxiliary+bad+good}
    alternatives = list(perfect_matchings(vertices | tails, edges))
    assert len(alternatives) == 1
    assert {frozenset(edge) for edge in alternatives[0]} == {frozenset(edge) for edge in full_actual}
    return dict(actual_endpoints=len(vertices | tails), actual_perfect_matchings=1,
                bad=dict(alpha=1, beta=1, mixed=0, orientation_budget=1, parity_rank=2),
                good=dict(alpha=0, beta=0, mixed=2, orientation_budget=0, parity_rank=0))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    example = obstruction(totals)
    for sources in (1, 2):
        for relay_count in (1, 2):
            for relay_sizes in itertools.product(range(3), repeat=relay_count):
                for cycle_pairs in range(3):
                    if sources+sum(relay_sizes)+cycle_pairs > 5:
                        continue
                    for cycle_sizes in partitions(cycle_pairs):
                        data = model(sources, relay_sizes, cycle_sizes)
                        vertices, _, auxiliary, chosen, free, _, _ = data
                        domain = vertices-set(free)
                        for replacement in matchings(sorted(domain)):
                            if 2*len(replacement) != len(domain):
                                continue
                            verify(data, replacement, totals)
                            operations = components(domain, auxiliary+replacement)
                            if all(not record['ends'] or {chosen[point] for point in record['ends']} == {'TP', 'BP'}
                                   for record in operations):
                                totals['tp_bp_augmentation_paths_with_optional_cycle_exchanges'] += 1
                            totals['arbitrary_mixed_relay_replacements'] += 1
    record = dict(status='PASS', totals=dict(totals), obstruction=example,
                  scope='All perfect N replacements in reduced models with 1..2 source/donor '
                  'pairs, 1..2 mixed relays with 0..2 internal PP pairs each, 0..2 cycle PP '
                  'pairs in all partitions, at most ten N-covered vertices. All cycle flips, '
                  'per-component incidence multiplicities, fixed mixed boundary colours, '
                  'forest rank, full tails and explicit eight-point matching uniqueness. '
                  'No frozen-grid embedding or universal geometric existence.')
    arguments.output.write_text(json.dumps(record, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
