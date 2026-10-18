"""Independent controls for the written robust-core deletion theorem."""

import argparse
from itertools import combinations
import json
from pathlib import Path
import random

from check_starforming_gap import forms, literal_condition
from check_subcubic_starforming import CORE, base, cycle_controls


ATTACHMENTS = {3, 11}
BRANCHES = {1, 2, 7, 10}
VERTICES = set(CORE)
ADJACENCY = {vertex: base()[vertex] & VERTICES for vertex in CORE}


def robust(selected, deleted):
    if deleted not in selected - ATTACHMENTS or not ADJACENCY[deleted] & selected:
        return False
    if any(not ADJACENCY[center] & (selected - {deleted})
           for center in ADJACENCY[deleted] & selected):
        return False
    for outside in ADJACENCY[deleted] - selected:
        neighbors = ADJACENCY[outside] & selected
        if len(neighbors) >= 3:
            continue
        if len(neighbors) != 2:
            return False
        other = next(iter(neighbors - {deleted}))
        if not ADJACENCY[other] & selected:
            return False
    return True


def table_choice(omitted):
    selected = VERTICES - omitted
    missing_branches = omitted & BRANCHES
    if not missing_branches:
        return 4 if 4 in selected else 9 if 9 in selected else 5 if {5, 11} <= selected else 8
    if len(missing_branches) == 1:
        branch = next(iter(missing_branches))
        first, second, companion, fallback = {
            1: (9, 4, 5, 8), 2: (9, 4, 3, 8),
            7: (4, 9, 8, 5), 10: (4, 9, 11, 5),
        }[branch]
        return first if first in selected else second if {second, companion} <= selected else fallback
    if len(missing_branches) == 2:
        pair = frozenset(selected & BRANCHES)
        missing = next(iter(omitted - BRANCHES))
        if pair == {1, 7}:
            return 4 if missing not in {4, 3, 8} else 9
        if pair == {2, 10}:
            return 4 if missing not in {4, 5, 11} else 9
        if pair == {1, 2}:
            return 9 if missing not in {9, 8, 11} else 5 if missing in {9, 8} else 1
        if pair == {7, 10}:
            return 4 if missing not in {4, 5, 3} else 8 if missing in {4, 5} else 7
        if pair == {1, 10}:
            return 4 if missing not in {4, 3} else 9
        return 9 if missing not in {9, 11} else 4
    return 9 if selected & BRANCHES & {1, 2} else 4


def local_controls():
    triples = list(combinations(CORE, 3))
    for omitted in triples:
        assert robust(VERTICES - set(omitted), table_choice(set(omitted)))
    upward_checks = 0
    dense = []
    for mask in range(1 << 10):
        selected = {vertex for position, vertex in enumerate(CORE) if mask >> position & 1}
        choices = [vertex for vertex in selected if robust(selected, vertex)]
        if len(selected) >= 7:
            assert choices
            dense.append((selected, choices))
        for deleted in choices:
            for added in VERTICES - selected:
                assert robust(selected | {added}, deleted)
                upward_checks += 1
    return dense, dict(omitted_triples=len(triples), dense_core_selections=len(dense),
                       upward_closure_single_additions=upward_checks)


def surrounding_controls(dense):
    generator = random.Random(20261019)
    checked = 0
    forming_checked = 0
    core_image = {vertex: position for position, vertex in enumerate(CORE)}
    graphs = []
    for outside_order in range(5):
        for trial in range(8):
            adjacency = [set() for vertex in range(10 + outside_order)]
            for vertex in CORE:
                adjacency[core_image[vertex]].update(core_image[neighbor] for neighbor in ADJACENCY[vertex])
            for first, second in combinations(range(10 + outside_order), 2):
                if second < 10 or first < 10 and CORE[first] not in ATTACHMENTS:
                    continue
                if generator.randrange(2):
                    adjacency[first].add(second)
                    adjacency[second].add(first)
            graphs.append((adjacency, outside_order))
    for adjacency, outside_order in graphs:
        for selected, choices in dense:
            for outside_mask in range(1 << outside_order):
                global_selected = {core_image[vertex] for vertex in selected} | {
                    10 + vertex for vertex in range(outside_order) if outside_mask >> vertex & 1}
                if not forms(adjacency, global_selected):
                    continue
                forming_checked += 1
                for deleted in choices:
                    reduced = global_selected - {core_image[deleted]}
                    assert forms(adjacency, reduced)
                    assert all(literal_condition(adjacency, reduced, outside)
                               for outside in set(range(len(adjacency))) - reduced)
                    checked += 1
    return dict(seed=20261019, surrounding_graphs=len(graphs),
                forming_selections=forming_checked, literal_star_safe_deletions=checked,
                allows_nonbipartite_outside_and_multiple_attachment_neighbors=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    dense, local = local_controls()
    report = dict(status='ALL_CHECKS_PASSED', local=local,
                  surrounding=surrounding_controls(dense),
                  cyclic_attainment=[cycle_controls(copies) for copies in range(2, 34, 2)],
                  scope='Controls for the analytic local proof and arbitrary-outside deletion argument; finite surrounding graphs do not replace the general theorem.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ['status', 'local', 'surrounding']}))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; verification uses assertions.')
    main()
