"""Independent controls of robust deletion and exact Heawood-port composition."""

import argparse
from collections import Counter
from itertools import combinations, product
import json
from pathlib import Path
import random

from check_cubic_starforming import base, dissociation, literal_stars, port_state, SELECTED, star_masks
from check_starforming_gap import connected, forms


def robust_deletions(adjacency, selected):
    degrees = [len(neighbors & selected) for neighbors in adjacency]
    return {deleted for deleted in selected if degrees[deleted] and
            all(degrees[center] >= 2 for center in adjacency[deleted] & selected) and
            all(degrees[outside] >= 3 or
                (degrees[outside] == 2 and
                 any(degrees[other] for other in (adjacency[outside] & selected) - {deleted}))
                for outside in adjacency[deleted] - selected)}


def obstruction_complement(adjacency, selected):
    degrees = [len(neighbors & selected) for neighbors in adjacency]
    forbidden = {vertex for vertex in selected if degrees[vertex] == 0}
    for vertex, neighbors in enumerate(adjacency):
        chosen = neighbors & selected
        if degrees[vertex] == 1:
            forbidden |= chosen
        if vertex not in selected and degrees[vertex] == 2:
            forbidden.update(deleted for deleted in chosen
                             if any(degrees[other] == 0 for other in chosen - {deleted}))
    return selected - forbidden


def without_edge(adjacency, first, second):
    broken = [set(neighbors) for neighbors in adjacency]
    broken[first].remove(second)
    broken[second].remove(first)
    return broken


def local_controls():
    adjacency = base()
    edges = [(point, line) for point in range(7) for line in adjacency[point]]
    nine_sets = [set(vertices) for vertices in combinations(range(14), 9)]
    candidate_counts = Counter()
    for selected in nine_sets:
        safe = robust_deletions(adjacency, selected)
        assert safe == obstruction_complement(adjacency, selected)
        points = len(selected & set(range(7)))
        if points in (2, 4):
            assert len(safe) >= 5
        if points == 3:
            assert len(safe & set(range(7, 14))) >= 4
        candidate_counts[(points, len(safe))] += 1
    perturbations = 0
    line_perturbations = 0
    for first, second in edges:
        broken = without_edge(adjacency, first, second)
        for selected in nine_sets:
            original = robust_deletions(adjacency, selected)
            remaining = robust_deletions(broken, selected) - {first, second}
            assert remaining
            assert len(original - remaining) <= 4
            if len(selected & set(range(7))) == 3:
                assert len((original & set(range(7, 14))) - remaining) <= 2
                line_perturbations += 1
            perturbations += 1
    broken = without_edge(adjacency, 0, 8)
    dense = []
    monotone = 0
    vertices = set(range(14))
    for size in range(9, 15):
        for entries in combinations(range(14), size):
            selected = set(entries)
            safe = robust_deletions(broken, selected) - {0, 8}
            assert safe
            assert safe == obstruction_complement(broken, selected) - {0, 8}
            dense.append((selected, safe))
            for added in vertices - selected:
                assert safe <= robust_deletions(broken, selected | {added})
                monotone += len(safe)
    forming = []
    proper_forming = []
    minimal = Counter()
    capacities = {}
    for mask in range(1 << 14):
        selected = {vertex for vertex in range(14) if mask >> vertex & 1}
        if dissociation(broken, selected):
            state = port_state(broken, selected)
            capacities[state] = max(capacities.get(state, 0), len(selected))
        forming.append(forms(broken, selected))
        proper_forming.append(any(forming[mask ^ (1 << vertex)] or
                                  proper_forming[mask ^ (1 << vertex)]
                                  for vertex in selected))
        if forming[mask] and not proper_forming[mask]:
            minimal[len(selected)] += 1
    assert max(minimal) == 8
    return broken, dense, capacities, dict(nine_sets=len(nine_sets), all_flag_perturbations=perturbations,
                               line_perturbations=line_perturbations,
                               dense_sets=len(dense), upward_closure_deletions=monotone,
                               full_graph_candidate_counts=[dict(points=key[0], robust=key[1], count=value)
                                                            for key, value in sorted(candidate_counts.items())],
                               broken_block_minimal_counts=dict(minimal),
                               broken_block_SF2_finite_exact=8)


def ambient_controls(broken, dense):
    generator = random.Random(2026101908)
    selections = 0
    deletions = 0
    for trial in range(32):
        outside_count = 1 + trial % 5
        adjacency = [set(neighbors) for neighbors in broken] + [set() for vertex in range(outside_count)]
        possible = list(combinations(range(14, 14 + outside_count), 2))
        possible += [(port, vertex) for port in (0, 8) for vertex in range(14, 14 + outside_count)]
        possible.append((0, 8))
        for first, second in possible:
            if generator.random() < 0.45:
                adjacency[first].add(second)
                adjacency[second].add(first)
        stars = star_masks(adjacency)
        for core, safe in generator.sample(dense, 48):
            for mask in range(1 << outside_count):
                selected = core | {14 + vertex for vertex in range(outside_count) if mask >> vertex & 1}
                selections += 1
                if not forms(adjacency, selected):
                    continue
                for deleted in safe:
                    smaller = selected - {deleted}
                    assert forms(adjacency, smaller)
                    assert all(literal_stars(stars, smaller, outside)
                               for outside in set(range(len(adjacency))) - smaller)
                    deletions += 1
    return dict(graphs=32, core_and_outside_selections=selections,
                safe_deletions_checked_with_literal_stars=deletions,
                arbitrary_external_edges=True, restored_incidence_allowed=True)


def independence_number(copies, edges):
    return max(mask.bit_count() for mask in range(1 << copies)
               if all(not (mask >> first & 1 and mask >> second & 1) for first, second in edges))


def port_optimum(copies, port_edges, capacities):
    maximum = 0
    for states in product(capacities, repeat=copies):
        total = sum(capacities[state] for state in states)
        if total <= maximum:
            continue
        selected = [entry[0] for state in states for entry in state]
        degrees = [entry[1] for state in states for entry in state]
        valid = True
        for first, second in port_edges:
            if selected[first] and selected[second]:
                degrees[first] += 1
                degrees[second] += 1
                if degrees[first] > 1 or degrees[second] > 1:
                    valid = False
                    break
        if valid:
            maximum = total
    return maximum


def interaction_controls(capacities):
    generator = random.Random(2026101914)
    results = []
    for copies in range(1, 5):
        possible = list(combinations(range(2 * copies), 2))
        graphs = range(1 << len(possible)) if copies <= 2 else [
            generator.randrange(1 << len(possible)) for trial in range(24)]
        for mask in graphs:
            edges = [edge for index, edge in enumerate(possible) if mask >> index & 1]
            interaction = {(first // 2, second // 2) for first, second in edges}
            alpha = independence_number(copies, interaction)
            beta = port_optimum(copies, edges, capacities)
            assert beta == 7 * copies + alpha
            results.append(dict(copies=copies, port_edges=edges,
                                loop_aware_independence=alpha, exact_port_optimization=beta,
                                exact_gap=copies - alpha))
    return results


def interface_controls():
    generator = random.Random(202610198)
    results = []
    for copies in range(1, 17):
        original = base()
        adjacency = [{14 * block + neighbor for neighbor in original[vertex]}
                     for block in range(copies) for vertex in range(14)]
        ports = [14 * block + port for block in range(copies) for port in (0, 8)]
        for block in range(copies):
            first, second = 14 * block, 14 * block + 8
            adjacency[first].remove(second)
            adjacency[second].remove(first)
        edges = 0
        for first, second in combinations(ports, 2):
            if generator.random() < 0.4:
                adjacency[first].add(second)
                adjacency[second].add(first)
                edges += 1
        selected = {14 * block + vertex for block in range(copies) for vertex in SELECTED}
        assert len(selected) == 8 * copies
        assert forms(adjacency, selected)
        assert all(not forms(adjacency, selected - {deleted}) for deleted in selected)
        results.append(dict(copies=copies, port_edges=edges, minimal_set_size=len(selected)))
    return results


def reciprocal_controls():
    generator = random.Random(2026101915)
    results = []
    for copies in range(1, 17):
        interaction = {(block - 1, block) for block in range(1, copies)}
        interaction.update(edge for edge in combinations(range(copies), 2) if generator.random() < 0.3)
        original = base()
        broken = without_edge(original, 0, 8)
        adjacency = [{14 * block + neighbor for neighbor in broken[vertex]}
                     for block in range(copies) for vertex in range(14)]
        for first, second in interaction:
            for line_block, point_block in [(first, second), (second, first)]:
                left, right = 14 * line_block + 8, 14 * point_block
                adjacency[left].add(right)
                adjacency[right].add(left)
        assert all(connected(adjacency, removed=vertex) for vertex in range(14 * copies))
        assert all((vertex % 14 < 7) != (neighbor % 14 < 7)
                   for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors)
        assert all(14 * block + 7 + point in adjacency[14 * block + point]
                   for block in range(copies) for point in range(7))
        interaction_degrees = [sum(vertex in edge for edge in interaction) for vertex in range(copies)]
        assert max(map(len, adjacency)) == max(3, 2 + max(interaction_degrees))
        alpha = independence_number(copies, interaction)
        results.append(dict(copies=copies, interaction_edges=len(interaction),
                            interaction_independence=alpha, exact_gap=copies - alpha,
                            two_connected=True, bipartite=True, matching_size=7 * copies))
    return results


def general_controls():
    graphs = 0
    perturbations = 0
    for order in range(2, 6):
        possible = list(combinations(range(order), 2))
        for graph_mask in range(1 << len(possible)):
            adjacency = [set() for vertex in range(order)]
            edges = []
            for index, (first, second) in enumerate(possible):
                if graph_mask >> index & 1:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
                    edges.append((first, second))
            if any(len(neighbors) > 3 for neighbors in adjacency):
                continue
            graphs += 1
            for mask in range(1 << order):
                selected = {vertex for vertex in range(order) if mask >> vertex & 1}
                original = robust_deletions(adjacency, selected)
                assert original == obstruction_complement(adjacency, selected)
                for first, second in edges:
                    broken = without_edge(adjacency, first, second)
                    remaining = robust_deletions(broken, selected) - {first, second}
                    selected_ports = len(selected & {first, second})
                    assert len(original - remaining) <= [0, 2, 4][selected_ports]
                    perturbations += 1
    return dict(labeled_graphs=graphs, maximum_order=5, perturbations=perturbations)


def boundary_controls():
    cycle = [{1, 3}, {0, 2}, {1, 3}, {0, 2}]
    broken_cycle = without_edge(cycle, 0, 1)
    losses = []
    for selected in [{0, 1, 2, 3}, {0, 2, 3}]:
        before = robust_deletions(cycle, selected)
        after = robust_deletions(broken_cycle, selected) - {0, 1}
        losses.append(len(before - after))
    assert losses == [4, 2]
    adjacency = without_edge(base(), 0, 8) + [set() for vertex in range(14)]
    for vertex in range(14):
        adjacency[vertex].add(14 + vertex)
        adjacency[14 + vertex].add(vertex)
    selected = set(range(14))
    assert forms(adjacency, selected)
    assert all(not forms(adjacency, selected - {deleted}) for deleted in selected)
    return dict(sharp_degree3_budgets=losses,
                forbidden_nonport_attachments_allow_minimal_core_selection=14)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    broken, dense, capacities, local = local_controls()
    report = dict(status='ALL_CHECKS_PASSED', local=local,
                  ambient=ambient_controls(broken, dense),
                  interfaces=interface_controls(), general_degree3=general_controls(),
                  interaction_formulas=interaction_controls(capacities),
                  reciprocal_realizations=reciprocal_controls(),
                  hypothesis_and_sharpness=boundary_controls(),
                  scope='Independent finite controls of the written Fano/perturbation proof. Exact global SF=8r follows from the general local cap and rewiring argument, not extrapolation from these checks.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; verification uses assertions.')
    main()
