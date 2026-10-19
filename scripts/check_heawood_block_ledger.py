"""Boundary controls of the written Heawood capacity-compensation theorem."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from check_cubic_starforming import base
from check_port_return import containing_stars, literal_at
from check_saturated_heawood_transfer import templates
from explore_long_core_SF import clauses


def boundary_controls():
    heawood = base()
    broken = [set(neighbors) for neighbors in heawood]
    broken[0].remove(8)
    broken[8].remove(0)
    counts = Counter()
    for entries in combinations(range(14), 8):
        internal = set(entries)
        chosen_ports = len(internal & {0, 8})
        if chosen_ports == 2:
            continue
        for parent_flags in range(4):
            parents = {14 + index for index in range(2) if parent_flags >> index & 1}
            if chosen_ports == 0 and not parents:
                continue
            if chosen_ports == 1 and parents != {14, 15}:
                continue
            for outer_flags in range(16):
                adjacency = [set(neighbors) for neighbors in broken]
                adjacency += [{0, 16, 17}, {8, 18, 19}, {14}, {14}, {15}, {15}]
                adjacency[0].add(14)
                adjacency[8].add(15)
                selected = internal | parents | {
                    16 + index for index in range(4) if outer_flags >> index & 1}
                counts['boundary_states'] += 1
                containing = containing_stars(adjacency)
                if not all(literal_at(containing, selected, outside)
                           for outside in set(range(14)) - internal):
                    continue
                counts['internally_formed_states'] += 1
                family = clauses(adjacency)
                private = {next(iter(clause & selected)) for clause in family
                           if len(clause & selected) == 1}
                if not internal - {0, 8} <= private:
                    continue
                counts['nonport_minimal_states'] += 1
                if chosen_ports == 0:
                    raise AssertionError('Two omitted ports cannot admit a selected parent at size eight')
                omitted_port = next(iter({0, 8} - internal))
                omitted_parent = 14 if omitted_port == 0 else 15
                if not adjacency[omitted_parent] & selected:
                    counts['isolated_parent_boundary_cases'] += 1
                    continue
                block_highs = {vertex for vertex in internal if len(adjacency[vertex] & selected) >= 2}
                no_import = all(any(not literal_at(containing, selected - {deleted}, outside)
                                    for outside in set(range(14)) - internal)
                                for deleted in block_highs)
                assert not no_import
                counts['active_parent_forced_import_states'] += 1
    classified = templates(heawood, broken)
    for template in classified:
        selected = set(template['selected'])
        port = template['signal_port']
        assert broken[port] <= selected and len(broken[port]) == 2
        assert all(len(broken[neighbor] & selected) == 2 for neighbor in broken[port])
    counts['protected_directional_templates'] = len(classified)
    return counts


def closed_controls():
    adjacency = base()
    containing = containing_stars(adjacency)
    family = clauses(adjacency)
    counts = Counter()
    for entries in combinations(range(14), 8):
        selected = set(entries)
        if not all(literal_at(containing, selected, outside)
                   for outside in set(range(14)) - selected):
            continue
        if any(all(literal_at(containing, selected - {deleted}, outside)
                   for outside in set(range(14)) - (selected - {deleted})) for deleted in selected):
            continue
        counts['minimal_eight_sets'] += 1
        isolates = {vertex for vertex in selected if not adjacency[vertex] & selected}
        cycle = selected - isolates
        assert len(isolates) == 2 and len(cycle) == 6
        assert all(len(adjacency[vertex] & selected) == 2 for vertex in cycle)
        assert all(len(adjacency[outside] & isolates) == len(adjacency[outside] & cycle) == 1
                   for outside in set(range(14)) - selected)
        for deleted in selected:
            assert any(clause & selected == {deleted} for clause in family)
            counts['private_deletion_certificates'] += 1
    return counts


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    boundary = boundary_controls()
    closed = closed_controls()
    report = dict(status='ALL_CHECKS_PASSED', boundary=boundary, closed=closed,
                  scope='Finite boundary controls verify the two restoration branches and '
                        'closed-Heawood classification in the general written proof. Parent '
                        'vertices have two distinct abstract core neighbors. All selected '
                        'non-port private clauses and all block-high internal failures are '
                        'tested using literal stars/global clauses. Arbitrary ambient core '
                        'edges are handled by the written locality proof, not enumeration.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], boundary=boundary, closed=closed)))


if __name__ == '__main__':
    main()
