"""Independent controls of distinct bare-port charges and the long-core phase."""

import argparse
from collections import Counter
import json
from pathlib import Path

from check_cubic_starforming import base
from check_exact_cubic import robust_deletions
from check_long_core_words import translate, word_control
from check_starforming_gap import forms
from explore_long_core_SF import clauses, graph, verify_literal


CERTIFICATES = [
    {0: ('A', 1), 6: ('B', 1, 0), 8: ('A', 2), 9: ('A', 3),
     10: ('A', 4), 11: ('A', 5), 18: ('B', 2, 8), 19: ('B', 7, 13)},
    {1: ('A', 1), 4: ('B', 3, 9), 6: ('B', 0, 1), 8: ('B', 2, 1),
     9: ('A', 9), 11: ('B', 19, 9)}]


PHASE = [
    {0, 6, 8, 9, 10, 11, 12, 13, 15, 16, 17, 18, 19},
    {1, 4, 6, 8, 9, 10, 11, 12, 13, 14, 16, 17}]

FULL_WITNESS = {
    0, 7, 10, 12, 14, 15, 16, 17, 18, 20, 21, 22, 23, 24, 25,
    27, 28, 29, 30, 31, 32, 34, 35, 36, 37, 41, 42, 43, 46, 50,
    52, 53, 60, 62, 63, 64, 65, 66, 72, 73, 74, 77, 78, 79,
    89, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 109, 114,
    119, 120, 121, 122, 123}


def local_controls():
    adjacency = base()
    adjacency[0].remove(8)
    adjacency[8].remove(0)
    totals = Counter()
    maxima = {}
    examples = {}
    for mask in range(1 << 14):
        selected = {vertex for vertex in range(14) if mask >> vertex & 1}
        bare = [port for port in [0, 8] if not ({port} | adjacency[port]) & selected]
        safe = robust_deletions(adjacency, selected) - {0, 8}
        count = len(bare)
        totals['all_subsets'] += 1
        if len(selected) + count > 8:
            assert safe
            totals['forced_robust_deletion_cases'] += 1
            totals['bare_' + str(count) + '_deletion_cases'] += 1
        if not safe:
            maxima[count] = max(maxima.get(count, 0), len(selected))
            if len(selected) == 8 - count:
                examples[count] = sorted(selected)
    assert maxima == {0: 8, 1: 7, 2: 6}
    return dict(totals=dict(totals), maximum_without_robust_nonport=maxima,
                attaining_local_no_robust_examples=examples,
                scope='Finite tests of the written Fano proof. Local no-robust examples are not claimed to be globally minimal in an ambient graph.')


def phase_controls():
    records = []
    for repeats in range(1, 13):
        copies = 2 * repeats
        adjacency, pairs, _, _ = word_control('B' * copies)
        ports = {vertex for pair in pairs for vertex in pair}
        chosen = {translate(copies, block, local) for block in range(copies)
                  for local in PHASE[block % 2]}
        assert len(chosen) == 25 * repeats and forms(adjacency, chosen)
        for block in range(copies):
            for owner, certificate in CERTIFICATES[block % 2].items():
                center = translate(copies, block, certificate[1])
                if certificate[0] == 'A':
                    support = {center} | adjacency[center]
                else:
                    neighbor = translate(copies, block, certificate[2])
                    assert neighbor in adjacency[center]
                    support = ({center} | (adjacency[center] - {neighbor}) |
                               (adjacency[neighbor] - {center}))
                assert support & chosen == {translate(copies, block, owner)}
        private_owners = set()
        for clause in clauses(adjacency):
            intersection = clause & chosen
            if len(intersection) == 1:
                private_owners |= intersection
        unsupported = chosen - ports - private_owners
        expected = {translate(copies, block, 10) for block in range(1, copies, 2)}
        assert unsupported == expected
        port_owners = {}
        for vertex in unsupported:
            witnesses = [port for port in chosen & ports if adjacency[port] & chosen == {vertex}]
            assert witnesses == [vertex + 6 * copies]
            assert forms(adjacency, chosen - {vertex})
            smaller = chosen - {vertex}
            lost_activity = {center for center in smaller
                             if adjacency[center] & chosen and not adjacency[center] & smaller}
            assert lost_activity == {vertex - 6 * copies, witnesses[0]}
            affected_outside = (adjacency[vertex] - chosen)
            for center in lost_activity:
                affected_outside |= adjacency[center] - chosen
            assert all(len(adjacency[outside] & smaller) >= 2 for outside in affected_outside)
            port_owners[vertex] = witnesses[0]
        assert len(set(port_owners.values())) == repeats
        records.append(dict(k=copies, repeats=repeats, core_selected_size=len(chosen),
                            unsupported_nonports=sorted(unsupported),
                            unique_selected_port_witnesses=port_owners,
                            forced_distinct_Heawood_losses=repeats,
                            conditional_full_selection_upper=36 * copies))
    adjacency, _ = graph(2)
    assert len(FULL_WITNESS) == 62
    literal = verify_literal(adjacency, FULL_WITNESS)
    core_chosen = {translate(2, block, local) for block in range(2) for local in PHASE[block % 2]}
    assert FULL_WITNESS & set(range(40)) == core_chosen
    block_sizes = []
    bare_counts = []
    for block in range(6):
        offset = 40 + 14 * block
        internal = {vertex for vertex in range(14) if offset + vertex in FULL_WITNESS}
        block_sizes.append(len(internal))
        bare = sum(not ({port} | {neighbor - offset for neighbor in adjacency[offset + port]
                                  if offset <= neighbor < offset + 14}) & internal
                   for port in [0, 8])
        bare_counts.append(bare)
        assert len(internal) + bare <= 8
    assert bare_counts[5] >= 1
    return dict(instances=records,
                nonvacuous_ambient_witness=dict(order=124, selected=sorted(FULL_WITNESS),
                                               selected_size=62, literal_deletion_checks=literal,
                                               block_sizes=block_sizes, bare_counts=bare_counts,
                                               exact_SF_claimed=False))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    local = local_controls()
    phases = phase_controls()
    report = dict(status='ALL_CHECKS_PASSED',
                  scope='The bare-port deficit and all-r phase compensation have general written proofs. Finite enumeration is independent verification only. The explicit core phase refutes a pure core certificate cap, not the conjectured full SF bound.',
                  local=local, phases=phases)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], local=local,
                         phase_instances=len(phases['instances']),
                         literal_ambient_deletions=62)))


if __name__ == '__main__':
    main()
