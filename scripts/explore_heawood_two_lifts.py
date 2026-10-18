"""Discovery controls for connected two-sheeted Heawood covers."""

import argparse
from collections import Counter, deque
import json
from pathlib import Path

from check_cubic_starforming import SELECTED, base
from check_regular_compensation import connected_after_deletion, exchange_control
from check_regular_starforming import bipartition


def exact_bipartite_dissociation(adjacency):
    colors = bipartition(adjacency)
    assert colors is not None
    left = [vertex for vertex in range(len(adjacency)) if colors[vertex] == 0]
    right = [vertex for vertex in range(len(adjacency)) if colors[vertex] == 1]
    positions = {vertex: position for position, vertex in enumerate(left)}
    neighborhoods = {vertex: sum(1 << positions[neighbor] for neighbor in adjacency[vertex])
                     for vertex in right}
    largest = 0
    attaining = set()
    for selection in range(1 << len(left)):
        independent = []
        private = {}
        for vertex, neighborhood in neighborhoods.items():
            neighbors = neighborhood & selection
            if neighbors == 0:
                independent.append(vertex)
            elif neighbors.bit_count() == 1:
                private[neighbors] = vertex
        size = selection.bit_count() + len(independent) + len(private)
        if size > largest:
            largest = size
            attaining = {vertex for position, vertex in enumerate(left) if selection >> position & 1}
            attaining |= set(independent) | set(private.values())
    assert len(attaining) == largest
    assert all(len(adjacency[vertex] & attaining) <= 1 for vertex in attaining)
    return dict(beta=largest, witness=sorted(attaining), method='exact_one_part_subset_and_private_neighbor_groups',
                left_subsets=1 << len(left))


def tree_and_cotree(adjacency):
    reached = {0}
    queue = deque([0])
    tree = set()
    while queue:
        vertex = queue.popleft()
        for neighbor in sorted(adjacency[vertex]):
            if neighbor not in reached:
                reached.add(neighbor)
                tree.add(tuple(sorted((vertex, neighbor))))
                queue.append(neighbor)
    edges = {(vertex, neighbor) for vertex, neighbors in enumerate(adjacency)
             for neighbor in neighbors if vertex < neighbor}
    assert len(tree) == 13 and len(edges - tree) == 8
    return tree, sorted(edges - tree)


def lift(adjacency, negative):
    order = len(adjacency)
    result = [set() for vertex in range(2 * order)]
    for vertex, neighbors in enumerate(adjacency):
        for neighbor in neighbors:
            if vertex >= neighbor:
                continue
            sign = int((vertex, neighbor) in negative)
            for sheet in (0, 1):
                first, second = order * sheet + vertex, order * (sheet ^ sign) + neighbor
                result[first].add(second)
                result[second].add(first)
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    adjacency = base()
    tree, cotree = tree_and_cotree(adjacency)
    previous = json.loads(arguments.output.read_text()) if arguments.output.exists() else None
    previous_values = {record['signature']: record['optimum']['beta']
                       for record in previous['records']} if previous else {}
    selected = SELECTED | {14 + vertex for vertex in SELECTED}
    totals = Counter()
    records = []
    for signature in range(1, 1 << len(cotree)):
        negative = {edge for position, edge in enumerate(cotree) if signature >> position & 1}
        lifted = lift(adjacency, negative)
        for deleted in range(len(lifted)):
            assert connected_after_deletion(lifted, deleted)
        exchange_control(lifted, selected, totals)
        optimum = exact_bipartite_dissociation(lifted)
        if signature in previous_values:
            assert optimum['beta'] == previous_values[signature]
        record = dict(signature=signature, negative_edges=sorted(negative), optimum=optimum)
        records.append(record)
        print(json.dumps(dict(signature=signature, beta=optimum['beta'])), flush=True)
        report = dict(scope='Discovery only: all nontrivial normalized two-sheeted Heawood covers. Does not prove an arbitrary-order connected gap bound.',
                      cotree_edges=cotree, tree_edges=sorted(tree), records=records,
                      beta_counts=dict(Counter(item['optimum']['beta'] for item in records)),
                      completed_signatures=len(records), expected_signatures=255)
        arguments.output.write_text(json.dumps(report, indent=2) + '\n')


if __name__ == '__main__':
    main()
