"""Finite controls for the written cubic zero-remainder normal form."""

import argparse
from collections import Counter
import json
from pathlib import Path
import random

from check_cubic_starforming import SELECTED, base, dissociation
from check_cubic_stability_ports import construction
from check_regular_starforming import bipartition, covered, star_lists
from explore_heawood_two_lifts import exact_bipartite_dissociation


def components(adjacency, vertices):
    unseen = set(vertices)
    result = []
    while unseen:
        reached = {min(unseen)}
        pending = list(reached)
        while pending:
            vertex = pending.pop()
            new = adjacency[vertex] & unseen - reached
            reached |= new
            pending.extend(new)
        unseen -= reached
        result.append(reached)
    return result


def pair_stubs(adjacency, first, second, generator):
    assert len(first) == len(second)
    for attempt in range(10000):
        shuffled = generator.sample(second, len(second))
        edges = list(zip(first, shuffled))
        if len(set(edges)) != len(edges):
            continue
        if any(neighbor in adjacency[vertex] for vertex, neighbor in edges):
            continue
        for vertex, neighbor in edges:
            adjacency[vertex].add(neighbor)
            adjacency[neighbor].add(vertex)
        return
    raise AssertionError('No simple stub pairing found in the finite control')


def normal_instance(high_colors, high_edges, high_three, isolate_counts,
                    matching_pairs, generator):
    adjacency = []
    colors = []
    selected = set()

    def vertex(color, chosen=False):
        identifier = len(adjacency)
        adjacency.append(set())
        colors.append(color)
        if chosen:
            selected.add(identifier)
        return identifier

    def edge(first, second):
        assert first != second and colors[first] != colors[second]
        assert second not in adjacency[first]
        adjacency[first].add(second)
        adjacency[second].add(first)

    for color in high_colors:
        vertex(color, True)
    for first, second in high_edges:
        edge(first, second)
    high_degrees = [len(neighbors) for neighbors in adjacency]
    leaves = []
    outside = []
    isolate_demands = []
    for owner, color in enumerate(high_colors):
        if owner in high_three:
            reserved = vertex(1 - color, True)
            witness = vertex(color)
            edge(owner, reserved)
            edge(reserved, witness)
            leaves.append(reserved)
            outside.append(witness)
        else:
            witness = vertex(1 - color)
            edge(owner, witness)
            outside.append(witness)
            isolate_demands.append(witness)
        for extra in range(2 - high_degrees[owner]):
            leaf = vertex(1 - color, True)
            witness = vertex(color)
            edge(owner, leaf)
            edge(leaf, witness)
            leaves.append(leaf)
            outside.append(witness)
            isolate_demands.append(witness)
    isolates = [vertex(color, True) for color in range(2)
                for count in range(isolate_counts[color])]
    for color in range(2):
        targets = [target for target in isolate_demands if colors[target] != color]
        capacity = [isolate for isolate in isolates if colors[isolate] == color
                    for stub in range(3)]
        assert len(targets) <= len(capacity)
        for target, isolate in zip(targets, generator.sample(capacity, len(capacity))):
            edge(target, isolate)
    matching = []
    for pair in range(matching_pairs):
        first, second = vertex(0, True), vertex(1, True)
        edge(first, second)
        matching.extend((first, second))
    for color in range(2):
        sources = [source for source in leaves + isolates + matching
                   if colors[source] == color for stub in range(3 - len(adjacency[source]))]
        assert len(sources) % 3 == 0
        targets = [vertex(1 - color) for count in range(len(sources) // 3)]
        pair_stubs(adjacency, sources, [target for target in targets for stub in range(3)], generator)
    outside_stubs = [[target for target in outside if colors[target] == color
                      for stub in range(3 - len(adjacency[target]))] for color in range(2)]
    pair_stubs(adjacency, outside_stubs[0], outside_stubs[1], generator)
    assert all(len(neighbors) == 3 for neighbors in adjacency)
    return adjacency, selected


def inspect(adjacency, selected, exact_beta=None):
    colors = bipartition(adjacency)
    assert colors is not None and all(len(neighbors) == 3 for neighbors in adjacency)
    vertices = set(range(len(adjacency)))
    outside = vertices - selected
    stars = star_lists(adjacency)
    mask = sum(1 << vertex for vertex in selected)
    assert all(covered(stars, mask, vertex) for vertex in outside)
    failures = {deleted: {vertex for vertex in outside | {deleted}
                         if not covered(stars, mask ^ (1 << deleted), vertex)}
                for deleted in selected}
    assert all(failures.values())
    counts = {vertex: len(neighbors & selected) for vertex, neighbors in enumerate(adjacency)}
    isolates = {vertex for vertex in selected if counts[vertex] == 0}
    high = {vertex for vertex in selected if counts[vertex] >= 2}
    high_two = {vertex for vertex in high if counts[vertex] == 2}
    high_three = high - high_two
    leaves = {vertex for vertex in selected if counts[vertex] == 1 and adjacency[vertex] & high}
    matching = selected - isolates - high - leaves
    witness = {owner: min(failures[owner] & outside) for owner in high}
    assert len(set(witness.values())) == len(high)
    assert all(3 - counts[witness[owner]] - (counts[owner] - 1) == 0 for owner in high)
    reserved = {owner: next(iter(adjacency[witness[owner]] & selected)) for owner in high_three}
    assert len(set(reserved.values())) == len(high_three)
    extra_leaves = leaves - set(reserved.values())
    extra_witness = {leaf: min(failures[leaf] & outside) for leaf in extra_leaves}
    assert len(set(extra_witness.values())) == len(extra_leaves)
    assert not set(extra_witness.values()) & set(witness.values())
    unused = outside - set(witness.values())
    assert not any(counts[vertex] == 1 for vertex in unused)
    assert {vertex for vertex in unused if counts[vertex] == 2} == set(extra_witness.values())
    private = {witness[owner] for owner in high_three}
    bad = {witness[owner] for owner in high_two}
    extra = set(extra_witness.values())
    full = outside - private - bad - extra
    assert all(counts[vertex] == 3 for vertex in full)
    for owner in high_three:
        assert adjacency[reserved[owner]] & selected == {owner}
        assert adjacency[witness[owner]] & selected == {reserved[owner]}
    for owner in high_two:
        assert adjacency[owner] & outside == {witness[owner]}
        assert adjacency[witness[owner]] & high == {owner}
        assert len(adjacency[witness[owner]] & isolates) == 1
    for leaf, target in extra_witness.items():
        assert adjacency[target] & leaves == {leaf}
        assert len(adjacency[target] & isolates) == 1
    assert all(len(adjacency[leaf] & full) == 1 for leaf in leaves)
    assert all(len(adjacency[vertex] & matching) == 1 and
               len(adjacency[vertex] & full) == 2 for vertex in matching)
    assert all(adjacency[vertex] <= bad | extra | full for vertex in isolates)
    assert all(adjacency[vertex] <= isolates | matching | leaves for vertex in full)
    assert all(len(adjacency[vertex] & outside) == 2 for vertex in private)
    assert all(len(adjacency[vertex] & outside) == 1 for vertex in bad | extra)
    high_components = components(adjacency, high)
    paths = [part for part in high_components if any(len(adjacency[vertex] & high) < 2 for vertex in part)]
    assert len(extra_leaves) == 2 * len(paths)
    assert len(high_two) + len(extra_leaves) <= 3 * len(isolates)
    assert 3 * len(full) == len(high_three) + 2 * len(matching) + 3 * len(isolates) - len(high_two)
    assert 3 * len(vertices) - 5 * len(selected) == len(isolates) + len(extra_leaves)
    support = {leaf: next(iter(adjacency[leaf] & high)) for leaf in extra_leaves}
    per_color = lambda group: [sum(colors[vertex] == color for vertex in group) for color in range(2)]
    bad_counts = per_color(high_two)
    full_counts = per_color(high_three)
    isolate_counts = per_color(isolates)
    extra_counts = [sum(colors[owner] == color for owner in support.values()) for color in range(2)]
    delta_bad = bad_counts[0] - bad_counts[1]
    delta_full = full_counts[0] - full_counts[1]
    delta_extra = extra_counts[0] - extra_counts[1]
    debt = isolate_counts[0] - isolate_counts[1] + 2 * delta_full
    assert delta_bad == -4 * delta_full and delta_extra == -6 * delta_full
    if len(paths) <= 2:
        assert delta_bad == delta_full == delta_extra == 0
    exchanges = []
    augmented = []
    for color in range(2):
        candidate = matching | leaves | {vertex for vertex in isolates if colors[vertex] != color}
        candidate |= {vertex for vertex in high if colors[vertex] == color}
        candidate |= {target for target in witness.values() if colors[target] != color}
        candidate -= {leaf for leaf, owner in support.items() if colors[owner] == color}
        assert dissociation(adjacency, candidate)
        signed_bad = delta_bad if color == 0 else -delta_bad
        assert len(candidate) == len(selected) - isolate_counts[color] - extra_counts[color] + signed_bad
        exchanges.append(candidate)
        additions = {extra_witness[leaf] for leaf in extra_leaves if colors[leaf] == color}
        for leaf in extra_leaves:
            if colors[leaf] == color:
                assert leaf in candidate and not adjacency[leaf] & candidate
                assert adjacency[extra_witness[leaf]] & candidate == {leaf}
        enhanced = candidate | additions
        assert len(enhanced) == len(candidate) + len(additions)
        assert dissociation(adjacency, enhanced)
        augmented.append(enhanced)
    assert len(exchanges[0]) - len(exchanges[1]) == -debt
    optimum = exact_beta if exact_beta is not None else exact_bipartite_dissociation(adjacency)['beta']
    slack = 3 * len(vertices) + 2 * optimum - 7 * len(selected)
    assert slack == abs(debt) + 2 * (optimum - max(map(len, exchanges)))
    assert slack >= abs(debt)
    component_debt = sum(abs(sum((1 if colors[vertex] == 0 else -1)
                                 for vertex in part & isolates) +
                             2 * sum((1 if colors[vertex] == 0 else -1)
                                     for vertex in part & high_three))
                         for part in components(adjacency, vertices))
    assert slack >= component_debt
    augmented_debt = isolate_counts[0] - isolate_counts[1] - 4 * delta_full
    assert sum(map(len, augmented)) == 2 * len(selected) - len(isolates)
    assert len(augmented[0]) - len(augmented[1]) == -augmented_debt
    assert slack == 2 * len(paths) + abs(augmented_debt) + 2 * (optimum - max(map(len, augmented)))
    augmented_component_debt = sum(abs(sum((1 if colors[vertex] == 0 else -1)
                                           for vertex in part & isolates) -
                                       4 * sum((1 if colors[vertex] == 0 else -1)
                                               for vertex in part & high_three))
                                   for part in components(adjacency, vertices))
    assert slack >= 2 * len(paths) + augmented_component_debt
    return dict(order=len(vertices), selected=len(selected), beta=optimum,
                high_paths=len(paths), extra_leaves=len(extra_leaves),
                isolates=len(isolates), high_two=len(high_two), high_three=len(high_three),
                exchange_sizes=list(map(len, exchanges)), debt=debt, slack=slack,
                component_debt=component_debt,
                augmented_exchange_sizes=list(map(len, augmented)), augmented_debt=augmented_debt,
                augmented_component_debt=augmented_component_debt,
                connected=len(components(adjacency, vertices)) == 1)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    generator = random.Random(2026101907)
    records = []
    examples = []
    for trial in range(300):
        high_three = set(generator.sample([0, 2, 4, 6], 2) + generator.sample([1, 3, 5, 7], 2))
        adjacency, selected = normal_instance([vertex % 2 for vertex in range(8)],
                                              [(vertex, vertex + 1) for vertex in range(7)],
                                              high_three, [1, 1], 0, generator)
        record = inspect(adjacency, selected)
        assert record['order'] == 28 and record['selected'] == 16 and record['high_paths'] == 1
        record['trial'] = trial
        record['family'] = 'one_eight_vertex_high_path'
        if not any(example['record']['beta'] == record['beta'] for example in examples):
            examples.append(dict(record=record, adjacency=[sorted(neighbors) for neighbors in adjacency],
                                 selection=sorted(selected),
                                 exact_beta=exact_bipartite_dissociation(adjacency)))
        records.append(record)
    for trial in range(40):
        high_three = set() if trial % 2 == 0 else {0, 1}
        adjacency, selected = normal_instance([0, 1], [], high_three, [1, 1],
                                              2 if not high_three else 1, generator)
        record = inspect(adjacency, selected)
        assert record['high_paths'] == 2 and record['extra_leaves'] == 4
        record['trial'] = trial
        record['family'] = 'two_isolated_high_vertices'
        records.append(record)
    controls = [inspect(base(), SELECTED, 7)]
    for copies in range(1, 7):
        adjacency, selected, attaining = construction(copies)
        controls.append(inspect(adjacency, selected, len(attaining)))
    report = dict(status='ALL_CHECKS_PASSED',
                  scope='Finite controls of literal formation and single deletions, zero-remainder partition, distinct extra witnesses, path counts, color balances, original and augmented exchanges, exact signed and component debt, and the proved positive path penalty. General results have separate written proofs.',
                  seed=2026101907, records=records, earlier_controls=controls, examples=examples,
                  one_path_beta_histogram=dict(Counter(record['beta'] for record in records if record['high_paths'] == 1)),
                  two_path_beta_histogram=dict(Counter(record['beta'] for record in records if record['high_paths'] == 2)),
                  totals=dict(new_instances=len(records), earlier_controls=len(controls),
                              literal_minimal_selections=len(records) + len(controls),
                              exchanges=2 * (len(records) + len(controls)),
                              augmented_exchanges=2 * (len(records) + len(controls)),
                              exact_new_optima=len(records),
                              path_instances_attaining_linear_equality=sum(record['slack'] == 0 for record in records)))
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: value for key, value in report.items() if key in
                      ('status', 'totals', 'one_path_beta_histogram', 'two_path_beta_histogram')}))


if __name__ == '__main__':
    main()
