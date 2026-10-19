"""Controls for directional saturated blocks, two-owner loss and overlapping charges."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path

from check_cubic_starforming import base
from check_exact_cubic import robust_deletions
from check_starforming_gap import forms, local_condition
from explore_long_core_SF import verify_literal


def clause_support(adjacency, clause):
    center = clause[1]
    if clause[0] == 'A':
        return {center} | adjacency[center]
    neighbor = clause[2]
    return {center} | (adjacency[center] - {neighbor}) | (adjacency[neighbor] - {center})


def port_clauses(broken, port):
    result = [('A', port)]
    for neighbor in sorted(broken[port]):
        result.extend([('B', port, neighbor), ('B', neighbor, port)])
    return result


def external_owners(adjacency, broken, selected):
    result = {}
    for port in [0, 8]:
        outside_selected = (adjacency[port] - set(range(14))) & selected
        for clause in port_clauses(broken, port):
            hit = clause_support(adjacency, clause) & selected
            if len(hit) == 1 and hit <= outside_selected:
                owner = next(iter(hit))
                assert outside_selected == {owner}
                result.setdefault(owner, []).append(dict(port=port, clause=clause))
    return result


def templates(heawood, broken):
    records = []
    for omitted_port, opposite_port in [(8, 0), (0, 8)]:
        for isolate in sorted(heawood[omitted_port] - {opposite_port}):
            other_neighbor = next(iter(heawood[omitted_port] - {opposite_port, isolate}))
            for joining in sorted(heawood[other_neighbor] - {omitted_port}):
                first_class = {opposite_port, isolate} | (heawood[joining] - {other_neighbor})
                second_class = {vertex for vertex in range(14)
                                if (vertex < 7) == (omitted_port < 7) and
                                vertex not in heawood[isolate]}
                selected = first_class | second_class
                second_isolate = next(iter(heawood[other_neighbor] - {omitted_port, joining}))
                assert len(selected) == 8 and selected & {0, 8} == {opposite_port}
                assert broken[omitted_port] & selected == {isolate}
                assert len(broken[opposite_port] & selected) == 2
                assert {vertex for vertex in selected if not broken[vertex] & selected} == {
                    isolate, second_isolate}
                assert not ({isolate, second_isolate} & {0, 8})
                assert not robust_deletions(broken, selected) - {0, 8}
                records.append(dict(omitted_port=omitted_port, signal_port=opposite_port,
                                    selected=sorted(selected), isolated_neighbor=isolate,
                                    second_isolate=second_isolate))
    assert len({tuple(record['selected']) for record in records}) == 8
    return records


def local_controls(heawood, broken):
    adjacency = [set(neighbors) for neighbors in broken] + [{0}, {8}]
    adjacency[0].add(14)
    adjacency[8].add(15)
    classified = templates(heawood, broken)
    template_lookup = {(tuple(record['selected']), record['omitted_port']) for record in classified}
    counts = Counter()
    maxima = {}
    for mask in range(1 << 14):
        internal = {vertex for vertex in range(14) if mask >> vertex & 1}
        counts['subsets'] += 1
        if robust_deletions(broken, internal) - {0, 8}:
            continue
        counts['subsets_without_robust_nonport'] += 1
        assert len(internal) <= 8
        bare = sum(not (({port} | broken[port]) & internal) for port in [0, 8])
        deficit = 8 - len(internal)
        assert deficit >= bare
        for flags in range(4):
            selected = internal | {14 + index for index in range(2) if flags >> index & 1}
            owners = external_owners(adjacency, broken, selected)
            count_owners = len(owners)
            assert count_owners <= 2
            if count_owners == 2:
                assert len(internal) <= 6
                counts['two_owner_states'] += 1
            signal = int(len(internal) == 8 and count_owners == 1)
            if signal:
                owner, certificates = next(iter(owners.items()))
                ports = {certificate['port'] for certificate in certificates}
                assert len(ports) == 1
                port = next(iter(ports))
                assert (tuple(sorted(internal)), port) in template_lookup
                assert owner == 14 + [0, 8].index(port)
                counts['saturated_directional_states'] += 1
            assert count_owners <= deficit + signal
            assert deficit >= max(bare, count_owners - signal)
            maxima[(bare, count_owners)] = max(maxima.get((bare, count_owners), 0), len(internal))
    assert counts['subsets'] == 16384 and counts['saturated_directional_states'] == 16
    assert maxima[(0, 2)] == maxima[(1, 2)] == maxima[(2, 2)] == 6
    return dict(totals=counts, templates=classified,
                maxima_by_bare_ports_and_external_owners=[dict(bare=key[0], owners=key[1], maximum=value)
                                                         for key, value in sorted(maxima.items())],
                scope='All local subsets and four selected-parent patterns under the necessary absence of robust non-port deletions. These controls verify the general written incidence proofs; they do not assert every state extends to an ambient minimal set.')


def paired_empty_clause_controls(broken):
    counts = Counter()
    for first in port_clauses(broken, 0):
        for second in port_clauses(broken, 8):
            first_support = clause_support(broken, first)
            second_support = clause_support(broken, second)
            assert not first_support & second_support
            assert len(first_support) == (3 if first[0] == 'A' else 4)
            assert len(second_support) == (3 if second[0] == 'A' else 4)
            counts['clause_pairs'] += 1
            allowed = set(range(14)) - first_support - second_support
            for entries in combinations(sorted(allowed), 7):
                assert robust_deletions(broken, set(entries)) - {0, 8}
                counts['seven_selection_robust_checks'] += 1
    assert counts['clause_pairs'] == 25 and counts['seven_selection_robust_checks'] == 16
    return counts


def ambient_examples(broken):
    cases = [
        ('free_directional_import', [(0, 14), (8, 15)],
         {0, 3, 4, 5, 7, 9, 10, 11, 15}, 0, 1, 0),
        ('two_nonbare_imports_cost_two', [(0, 14), (8, 15)],
         {0, 2, 3, 5, 9, 11, 14, 15}, 0, 2, 2),
        ('bare_and_import_share_one_loss', [(0, 14), (14, 15)],
         {1, 2, 4, 9, 11, 12, 13, 14, 15}, 1, 1, 1)]
    records = []
    for name, extra_edges, selected, expected_bare, expected_owners, expected_deficit in cases:
        adjacency = [set(neighbors) for neighbors in broken] + [set(), set()]
        for first, second in extra_edges:
            adjacency[first].add(second)
            adjacency[second].add(first)
        assert forms(adjacency, selected)
        literal_checks = verify_literal(adjacency, selected)
        internal = selected & set(range(14))
        bare = sum(not (({port} | broken[port]) & internal) for port in [0, 8])
        owners = external_owners(adjacency, broken, selected)
        deficit = 8 - len(internal)
        assert (bare, len(owners), deficit) == (expected_bare, expected_owners, expected_deficit)
        failures = {}
        for deleted in sorted(selected):
            smaller = selected - {deleted}
            failures[deleted] = min(outside for outside in set(range(16)) - smaller
                                    if not local_condition(adjacency, smaller, outside))
        records.append(dict(name=name, order=16, extra_edges=extra_edges,
                            selected=sorted(selected), block_selected=sorted(internal),
                            bare_ports=bare, external_owners=owners, deficit=deficit,
                            literal_deletion_checks=literal_checks, deletion_failures=failures))
    assert records[-1]['deficit'] < records[-1]['bare_ports'] + len(records[-1]['external_owners'])
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    heawood = base()
    broken = [set(neighbors) for neighbors in heawood]
    broken[0].remove(8)
    broken[8].remove(0)
    report = dict(status='ALL_CHECKS_PASSED', local=local_controls(heawood, broken),
                  paired_empty_clauses=paired_empty_clause_controls(broken),
                  ambient_examples=ambient_examples(broken),
                  scope='General written Fano proofs classify saturated external private evidence and prove that two different outside owners force at most six block selections. Finite tests check those proofs and three actual minimal ambient sets. General SF(L_k)=36k and the grid bridge remain open.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], local=report['local']['totals'],
                         paired_clauses=report['paired_empty_clauses'],
                         actual_ambient_examples=len(report['ambient_examples']),
                         literal_deletions=sum(record['literal_deletion_checks']
                                               for record in report['ambient_examples']))))


if __name__ == '__main__':
    main()
