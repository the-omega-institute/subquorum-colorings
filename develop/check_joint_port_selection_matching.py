"""Check exact selector matching for distinct source/resource ports and relays."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_component_isolated_auxiliary_compensation import inventory
from check_balanced_mixed_port_compensation import activate
from check_full_domain_marker_compensation import full_signs
from check_port_choice_rematching_cost import family
from check_terminal_cancellation_and_stranded_demand import components, terminal_data


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def edge_set(edges):
    return {frozenset(edge) for edge in edges}


def wrapped(point):
    return 'physical', point


def build_graph(internal, sources, resources, relays, candidates, selected):
    ports = [point for pair in sources+resources+relays for point in pair]
    assert len(ports) == len(set(ports)) and not set(ports) & set(internal)
    physical = set(internal) | set(ports)
    assert all(len(edge) == 2 and edge <= physical for edge in candidates)
    vertices = {wrapped(point) for point in physical}
    edges = {frozenset(wrapped(point) for point in edge) for edge in candidates}
    for category, groups in [('source', sources), ('resource', resources)]:
        slots = [(category+'_slot', index) for index in range(selected)]
        vertices.update(slots)
        for index, pair in enumerate(groups):
            opened, holding = (category+'_open', index), (category+'_hold', index)
            vertices.update([opened, holding])
            edges.update(frozenset((selector, wrapped(point)))
                         for selector in [opened, holding] for point in pair)
            edges.update(frozenset((opened, slot)) for slot in slots)
    for index, (first, second) in enumerate(relays):
        left, right = ('relay_left', index), ('relay_right', index)
        vertices.update([left, right])
        edges.update(edge_set([(wrapped(first), left), (left, right), (right, wrapped(second))]))
    return vertices, edges


def all_perfect(vertices, edges):
    adjacency = {point: set() for point in vertices}
    for edge in edges:
        first, second = tuple(edge)
        adjacency[first].add(second)
        adjacency[second].add(first)

    def extend(remaining):
        if not remaining:
            yield []
            return
        first = min(remaining, key=lambda point: (len(adjacency[point] & remaining), point))
        for second in sorted(adjacency[first] & remaining):
            for following in extend(remaining-{first, second}):
                yield [(first, second)]+following

    yield from extend(set(vertices))


def perfect_on(vertices, edges, matching):
    covered = [point for edge in matching for point in edge]
    assert len(covered) == len(set(covered)) and set(covered) == vertices
    assert edge_set(matching) <= edges


def check_coverage(internal, sources, resources, relays, candidates, selected, replacement):
    covered = [point for edge in replacement for point in edge]
    assert len(covered) == len(set(covered)) and set(internal) <= set(covered)
    assert edge_set(replacement) <= candidates
    assert all(len(set(pair) & set(covered)) <= 1 for pair in sources+resources)
    assert sum(bool(set(pair) & set(covered)) for pair in sources) == selected
    assert sum(bool(set(pair) & set(covered)) for pair in resources) == selected
    assert all(len(set(pair) & set(covered)) in (0, 2) for pair in relays)
    assert set(covered) <= set(internal) | {point for pair in sources+resources+relays for point in pair}


def project(matching):
    return [tuple(point[1] for point in edge) for edge in matching
            if all(point[0] == 'physical' for point in edge)]


def lift(internal, sources, resources, relays, candidates, selected, replacement):
    check_coverage(internal, sources, resources, relays, candidates, selected, replacement)
    following = [tuple(wrapped(point) for point in edge) for edge in replacement]
    covered = {point for edge in replacement for point in edge}
    for category, groups in [('source', sources), ('resource', resources)]:
        active = [index for index, pair in enumerate(groups) if set(pair) & covered]
        slots = {index: position for position, index in enumerate(active)}
        for index, pair in enumerate(groups):
            opened, holding = (category+'_open', index), (category+'_hold', index)
            if index in slots:
                following.extend([(opened, (category+'_slot', slots[index])),
                                  (holding, wrapped(next(point for point in pair if point not in covered)))])
            else:
                following.extend([(opened, wrapped(pair[0])), (holding, wrapped(pair[1]))])
    for index, (first, second) in enumerate(relays):
        left, right = ('relay_left', index), ('relay_right', index)
        if first in covered:
            following.append((left, right))
        else:
            following.extend([(wrapped(first), left), (right, wrapped(second))])
    vertices, edges = build_graph(internal, sources, resources, relays, candidates, selected)
    perfect_on(vertices, edges, following)
    assert edge_set(project(following)) == edge_set(replacement)
    return following


def direct_replacements(internal, sources, resources, relays, candidates, selected):
    for source_indices in itertools.combinations(range(len(sources)), selected):
        for resource_indices in itertools.combinations(range(len(resources)), selected):
            for choices in itertools.product((0, 1), repeat=2*selected):
                chosen = {sources[index][choice] for index, choice in zip(source_indices, choices[:selected])}
                chosen.update(resources[index][choice] for index, choice in zip(resource_indices, choices[selected:]))
                for flags in itertools.product((False, True), repeat=len(relays)):
                    domain = set(internal) | chosen | {point for pair, flag in zip(relays, flags) if flag for point in pair}
                    yield from all_perfect(domain, {edge for edge in candidates if edge <= domain})


def abstract_controls(totals):
    generator = random.Random(231023)
    for pair_count, source_count, resource_count, relay_count in itertools.product(range(2), range(3), range(3), range(2)):
        count = 2*(pair_count+source_count+resource_count+relay_count)
        if count > 8:
            continue
        internal = set(range(2*pair_count))
        pairs = [tuple(range(index, index+2)) for index in range(2*pair_count, count, 2)]
        sources = pairs[:source_count]
        resources = pairs[source_count:source_count+resource_count]
        relays = pairs[source_count+resource_count:]
        old = edge_set(zip(range(0, 2*pair_count, 2), range(1, 2*pair_count, 2)))
        complete = list(itertools.combinations(range(count), 2))
        if count <= 4:
            graphs = [edge_set(edge for edge, flag in zip(complete, flags) if flag)
                      for flags in itertools.product((False, True), repeat=len(complete))]
        else:
            graphs = [set(), old, edge_set(complete)]
            graphs.extend(edge_set(edge for edge in complete if generator.randrange(2)) for _ in range(24))
        for candidates in graphs:
            for selected in range(min(source_count, resource_count)+1):
                vertices, edges = build_graph(internal, sources, resources, relays, candidates, selected)
                projected = set()
                for matching in all_perfect(vertices, edges):
                    replacement = project(matching)
                    check_coverage(internal, sources, resources, relays, candidates, selected, replacement)
                    projected.add(frozenset(edge_set(replacement)))
                    totals['selector_perfect_matchings'] += 1
                direct = set()
                for replacement in direct_replacements(internal, sources, resources, relays, candidates, selected):
                    direct.add(frozenset(edge_set(replacement)))
                    matching = lift(internal, sources, resources, relays, candidates, selected, replacement)
                    assert sum(frozenset(edge) not in old for edge in replacement) == sum(
                        frozenset(point[1] for point in edge) not in old for edge in matching
                        if all(point[0] == 'physical' for point in edge))
                    totals['independent_reverse_lifts'] += 1
                assert projected == direct
                totals['coverage_models'] += 1
                totals['distinct_projected_replacements'] += len(projected)
                totals['infeasible_coverage_models'] += not projected


def examples(totals):
    sources, resources = [(0, 1), (2, 3)], [(4, 5), (6, 7)]
    collision = edge_set([(0, 4), (2, 5)])
    assert all(any(direct_replacements(set(), [source], resources, [], collision, 1)) for source in sources)
    vertices, edges = build_graph(set(), sources, resources, [], collision, 2)
    assert not list(all_perfect(vertices, edges))
    joint = collision | edge_set([(1, 6)])
    vertices, edges = build_graph(set(), sources, resources, [], joint, 2)
    matching = next(all_perfect(vertices, edges))
    assert edge_set(project(matching)) == edge_set([(1, 6), (2, 5)])
    totals['shared_beta_and_joint_choice_examples'] += 2
    vertices = set(range(8))
    actual, auxiliary = [(0, 1), (2, 3), (4, 5), (6, 7)], [(5, 6)]
    kinds = {0: 'TP', 1: 'TP', 2: 'BP', 3: 'BP', 4: 'TP', 7: 'BP'}
    candidates = edge_set(auxiliary+[(0, 5), (6, 2)])
    matching = lift({5, 6}, [(0, 1)], [(2, 3)], [(4, 7)], candidates, 1, [(0, 5), (6, 2)])
    replacement = project(matching)
    signs, cycles, _ = full_signs(vertices, actual, auxiliary, kinds, {0, 2}, {})
    assert not cycles
    assert sum(signs[first] == signs[second] == -1 for first, second in replacement) == 1
    final = inventory(components(vertices, actual+replacement), {point: kind for point, kind in kinds.items() if point not in {0, 2}})
    assert final['alpha'] == final['beta'] == 1
    totals['coverage_without_coherence_obstructions'] += 1
    candidates = edge_set([(0, 4), (5, 2)])
    graph_vertices, graph_edges = build_graph(set(), [(0, 1)], [(2, 3)], [(4, 5)], candidates, 1)
    matching = next(all_perfect(graph_vertices, graph_edges))
    replacement = project(matching)
    assert edge_set(replacement) == candidates
    kinds = {0: 'TP', 1: 'TP', 2: 'BP', 3: 'BP', 4: 'BP', 5: 'TP'}
    actual = [(0, 1), (2, 3), (4, 5)]
    records = components(set(range(6)), actual)
    active = [record for record in records if set(record['ends']) == {4, 5}]
    _, signs, _, _ = activate((set(range(6)), actual, [], kinds, {0, 2}, {}), active)
    assert all(signs[first]+signs[second] == 0 for first, second in replacement)
    totals['balanced_relay_selection_examples'] += 1


def interval_control(totals):
    sources, resources = [(0, 1), (2, 3)], [(6, 7), (8, 9), (10, 11)]
    replacement = [(0, 8), (2, 10)]
    candidates = edge_set(replacement)
    lift(set(), sources, resources, [], candidates, 2, replacement)
    actual = [(point, point+1) for point in range(0, 12, 2)]
    vertices = set(range(12))
    kinds = {point: 'TP' if point < 6 else 'BP' for point in vertices}
    chosen = {0, 2, 8, 10}
    signs, _, markers = full_signs(vertices, actual, [], kinds, chosen, {4: 0})
    assert all(signs[first]+signs[second] == 0 for first, second in replacement)
    records = components(vertices, actual+replacement)
    final = inventory(records, {point: kind for point, kind in kinds.items() if point not in chosen})
    assert (final['alpha'], final['beta'], final['mixed']) == (1, 1, 2)
    assert markers == {frozenset((4, 5)): (4, 0)}
    original_intervals, virtualized_intervals, backed = {0, 1, 2}, {1, 2}, {0}
    remaining = original_intervals-virtualized_intervals
    assert not virtualized_intervals & backed and backed <= remaining
    assert len(original_intervals)+1-3 == len(remaining)+(1+len(virtualized_intervals))-3
    assert len(remaining)+final['beta']-final['alpha'] == 1
    totals['interval_virtualization_and_reserved_backing_examples'] += 1


def physical_lifts(totals):
    for width, depth, tail in [(6, 1, 4), (32, 1, 16), (64, 5, 32)]:
        current, bands, owners, _, shift = family(width, depth, tail)
        _, _, _, _, kinds, pairs, _ = terminal_data(current, bands)
        sources = [pair for pair in pairs if all(kinds[point] == 'TP' for point in pair)]
        resources = [pair for pair in pairs if all(kinds[point] == 'BP' for point in pair)]
        relays = [pair for pair in pairs if {kinds[point] for point in pair} == {'TP', 'BP'}]
        internal = set(owners)-set(kinds)
        auxiliary = [tuple(column) for band in bands for column in band if set(column) <= internal]
        lower, bottom, outer = width+4, width+5, 2*depth+8+shift
        route = [(lower, 7+shift), (bottom, outer), (lower, outer),
                 (lower, outer+1), (bottom, outer+1), (bottom, outer+2),
                 (lower, outer+2), (lower, outer+3), (bottom, outer+3), (bottom, outer+4)]
        added = [((lower, 3+shift), (lower, 4+shift)),
                 ((lower, 5+shift), (lower, 6+shift))]+list(zip(route[::2], route[1::2]))
        removed = edge_set(zip(route[1:-1:2], route[2:-1:2]))
        following = [edge for edge in auxiliary if frozenset(edge) not in removed]+added
        candidates = edge_set(auxiliary+added)
        lifted = lift(internal, sources, resources, relays, candidates, 1, following)
        assert len(edge_set(project(lifted))-edge_set(auxiliary)) == 7
        totals['physical_seven_edge_selector_lifts'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    abstract_controls(totals)
    examples(totals)
    interval_control(totals)
    physical_lifts(totals)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals),
        scope='Exact projected matching-set comparison on the stated finite graph controls, '
              'reverse lifts and cost preservation; explicit capacity/greedy/coherence examples '
              'and three real-grid lifts. Counts sum modeled occurrences across inputs, '
              'not globally distinct graphs or resources. General proof is written. No blossom implementation, '
              'universal coherent existence or full matching Lean formalization.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
