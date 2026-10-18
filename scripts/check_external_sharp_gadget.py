"""Independent finite controls of Bhattacharjee's published H-sharp identity."""

import argparse
from itertools import combinations
import json
from pathlib import Path

from check_cubic_starforming import dissociation
from check_starforming_gap import forms


def check_graph(order, edges):
    adjacency = [set() for vertex in range(2 * order + 3 * len(edges))]
    gadget_edges = [(vertex, order + vertex) for vertex in range(order)]
    for index, (first, second) in enumerate(edges):
        left = 2 * order + 3 * index
        gadget_edges.extend([(first, left), (left, left + 1),
                             (left + 1, left + 2), (left + 2, second)])
    for first, second in gadget_edges:
        adjacency[first].add(second)
        adjacency[second].add(first)
    independent = [set(vertex for vertex in range(order) if mask >> vertex & 1)
                   for mask in range(1 << order)
                   if all(not (mask >> first & 1 and mask >> second & 1)
                          for first, second in edges)]
    alpha = max(map(len, independent))
    target = order + 2 * len(edges) + alpha
    for selected in independent:
        witness = selected | set(range(order, 2 * order))
        for index, (first, second) in enumerate(edges):
            left = 2 * order + 3 * index
            witness.update([left + 1, left + 2 if first in selected else left])
        assert len(witness) == order + 2 * len(edges) + len(selected)
        assert dissociation(adjacency, witness)
    beta = 0
    star = 0
    forming = []
    proper_forming = []
    minimal_count = 0
    for mask in range(1 << len(adjacency)):
        selected = {vertex for vertex in range(len(adjacency)) if mask >> vertex & 1}
        if dissociation(adjacency, selected):
            beta = max(beta, len(selected))
        forming.append(forms(adjacency, selected))
        proper_forming.append(any(forming[mask ^ (1 << vertex)] or
                                  proper_forming[mask ^ (1 << vertex)]
                                  for vertex in selected))
        if not forming[mask] or proper_forming[mask]:
            continue
        minimal_count += 1
        star = max(star, len(selected))
        doubled = {vertex for vertex in range(order)
                   if {vertex, order + vertex} <= selected}
        assert all(vertex in selected or order + vertex in selected for vertex in range(order))
        for index, (first, second) in enumerate(edges):
            inner = set(range(2 * order + 3 * index, 2 * order + 3 * index + 3))
            assert len(inner & selected) <= 2
            if first in doubled and second in doubled:
                assert len(inner & selected) <= 1
        induced_edges = sum(first in doubled and second in doubled for first, second in edges)
        assert len(selected) <= order + len(doubled) + 2 * len(edges) - induced_edges
        assert len(doubled) - induced_edges <= alpha
    assert beta == star == target
    return dict(base_order=order, base_edges=edges, gadget_order=len(adjacency),
                alpha=alpha, beta2=beta, SF2=star, minimal_sets_checked=minimal_count,
                subsets_checked=1 << len(adjacency))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    graphs = []
    for order in range(1, 5):
        possible = list(combinations(range(order), 2))
        for size in range(len(possible) + 1 if order <= 3 else 3):
            for edges in combinations(possible, size):
                graphs.append(check_graph(order, edges))
    report = dict(status='ALL_CHECKS_PASSED', graphs=graphs,
                  external_author='Deep Bhattacharjee',
                  external_revision='82c7cf4974d7eab76d5f04afdc4c8d563daecdc1',
                  source='https://github.com/creelie/Conjecture-002/tree/v1.1.0',
                  scope='Independent finite controls, not a new proof or a rebuild of external Lean. All labeled base graphs of orders 1..3, and order 4 with at most two edges. All proper subsets used for minimality.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], graphs=len(graphs),
                         subsets=sum(graph['subsets_checked'] for graph in graphs))))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; verification uses assertions.')
    main()
