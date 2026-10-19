"""Independent literal and deletion controls for private star clauses."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import random

from check_cubic_starforming import base, star_masks
from check_exact_cubic import robust_deletions
from check_long_core_words import translate, word_control
from check_regular_starforming import masks
from check_starforming_gap import forms, graph
from explore_long_core_deletions import safe_deletions
from explore_long_core_SF import clauses


ROBUST_OBSTACLE = {0, 1, 3, 4, 5, 6, 8, 10, 11, 12, 13, 15, 18}


def exhaustive(adjacency):
    order = len(adjacency)
    clause_masks = [sum(1 << vertex for vertex in clause) for clause in clauses(adjacency)]
    stars = star_masks(adjacency)
    forming = []
    has_proper_forming = []
    minimal_count = 0
    for selection in range(1 << order):
        chosen = {vertex for vertex in range(order) if selection >> vertex & 1}
        hits = all(selection & clause for clause in clause_masks)
        literal = all(any(star >> outside & 1 and star & (selection | (1 << outside)) == star
                          for star in stars) for outside in set(range(order)) - chosen)
        assert hits == literal == forms(adjacency, chosen)
        forming.append(literal)
        has_proper_forming.append(any(forming[selection ^ (1 << vertex)] or
                                      has_proper_forming[selection ^ (1 << vertex)]
                                      for vertex in chosen))
        minimal = literal and not has_proper_forming[selection]
        private = all(any(selection & clause == 1 << vertex for clause in clause_masks)
                      for vertex in chosen)
        assert minimal == (hits and private)
        minimal_count += minimal
    return dict(order=order, clauses=len(clause_masks), subsets=1 << order,
                minimal_selections=minimal_count)


def small_graphs():
    count_graphs = 0
    count_subsets = 0
    for order in range(6):
        possible = list(combinations(range(order), 2))
        for edges in range(1 << len(possible)):
            adjacency = [set() for vertex in range(order)]
            for index, (first, second) in enumerate(possible):
                if edges >> index & 1:
                    adjacency[first].add(second)
                    adjacency[second].add(first)
            result = exhaustive(adjacency)
            count_graphs += 1
            count_subsets += result['subsets']
    return dict(graphs=count_graphs, subsets=count_subsets)


def core_controls():
    adjacency, pairs, _, _ = word_control('B')
    ports = {vertex for pair in pairs for vertex in pair}
    nonport_mask = sum(1 << vertex for vertex in set(range(20)) - ports)
    clause_masks = [sum(1 << vertex for vertex in clause) for clause in clauses(adjacency)]
    neighborhoods = masks(adjacency)
    checked = 0
    generator = random.Random(20261019)
    direct_comparisons = 0
    for selection in range(1 << 20):
        if selection.bit_count() < 13:
            continue
        checked += 1
        owners = 0
        for clause in clause_masks:
            intersection = selection & clause
            if intersection.bit_count() == 1:
                owners |= intersection
        for port in ports:
            if selection >> port & 1:
                neighbors = selection & neighborhoods[port]
                if neighbors.bit_count() == 1:
                    owners |= neighbors
        safe_mask = selection & nonport_mask & ~owners
        assert safe_mask
        if generator.randrange(1000) == 0:
            chosen = {vertex for vertex in range(20) if selection >> vertex & 1}
            direct = safe_deletions(adjacency, chosen, ports)
            assert direct == {vertex for vertex in range(20) if safe_mask >> vertex & 1}
            direct_comparisons += 1
    repeated = []
    for copies in range(1, 17):
        adjacency, pairs, _, _ = word_control('B' * copies)
        ports = {vertex for pair in pairs for vertex in pair}
        chosen = {translate(copies, block, local)
                  for block in range(copies) for local in ROBUST_OBSTACLE}
        assert len(chosen) == 13 * copies and forms(adjacency, chosen)
        assert not robust_deletions(adjacency, chosen) - ports
        safe = safe_deletions(adjacency, chosen, ports)
        assert {6 * block for block in range(copies)} <= safe
        repeated.append(dict(k=copies, core_selected_size=len(chosen),
                             robust_nonport_deletions=0, safe_nonport_deletions=sorted(safe)))
    return dict(dense_fixed_core_selections=checked, direct_comparisons=direct_comparisons,
                fixed_core_safe_deletion_claim='Finite k1 control only; no all-k upper proof.',
                repeated_robust_rule_obstacle=repeated,
                robust_obstacle_local_selection=sorted(ROBUST_OBSTACLE))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED',
                  scope='Independent finite tests of the general written and Lean clause equivalence and boundary-certificate theorem. All proper subsets are tested for minimality through dynamic subset closure. Dense fixed-core tests are a lead only. The13k robust-rule obstruction has a written periodic proof and is not a global minimal forming set.',
                  small_graphs=small_graphs(),
                  named_graphs=dict(base_counterexample=exhaustive(graph(1)),
                                    Heawood=exhaustive(base())), core=core_controls())
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], small_graphs=report['small_graphs'],
                         named_graphs=report['named_graphs'],
                         dense_core_selections=report['core']['dense_fixed_core_selections'])))


if __name__ == '__main__':
    main()
