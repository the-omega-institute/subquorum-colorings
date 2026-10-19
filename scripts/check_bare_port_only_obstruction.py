"""Explicit all-length cover obstruction to bare-port-only compensation."""

import argparse
import json
from pathlib import Path

from check_boundary_loss import private_owners
from check_long_core_words import translate, word_control
from check_starforming_gap import forms, local_condition
from explore_long_core_SF import clauses, graph, verify_literal


BASE_SELECTION = {
    1, 5, 7, 10, 12, 14, 15, 17, 19, 21, 23, 24, 25, 26, 28, 29, 30,
    31, 32, 33, 34, 35, 36, 37, 38, 41, 44, 46, 50, 52, 53, 57, 58,
    60, 61, 62, 66, 67, 68, 69, 72, 74, 80, 81, 86, 90, 91, 92, 94,
    95, 99, 103, 104, 105, 108, 109, 111, 114, 116, 120, 122, 123}

DELETION_FAILURES = [
    1, 4, 8, 10, 0, 2, 3, 4, 8, 9, 11, 48, 40, 55, 28, 78, 18, 82,
    20, 96, 118, 110, 16, 3, 38, 41, 44, 46, 50, 42, 43, 64, 56, 63,
    54, 55, 56, 64, 78, 69, 70, 71, 70, 71, 86, 83, 88, 85, 89, 85,
    99, 100, 97, 98, 98, 106, 111, 114, 116, 120, 112, 113]

SINGLE_NEIGHBOR_STARS = [
    (3, 15, 37), (4, 5, 17), (8, 7, 19), (54, 61, 58), (55, 62, 26),
    (56, 66, 58), (63, 60, 61), (64, 57, 67), (70, 80, 72), (71, 81, 74),
    (78, 68, 29), (89, 86, 94), (93, 86, 94), (106, 99, 109), (107, 99, 109)]


CORE_PRIVATE_CERTIFICATES = {
    1: ('A', 1), 5: ('A', 4), 7: ('A', 8), 10: ('A', 10),
    12: ('B', 0, 1), 14: ('B', 2, 1), 15: ('A', 3), 17: ('B', 4, 5),
    19: ('B', 8, 7), 21: ('B', 9, 10), 23: ('B', 11, 10),
    36: ('B', 16, 28), 37: ('B', 3, 15), 38: ('A', 38)}


def projection(repeats, vertex):
    copies = 2 * repeats
    if vertex < 6 * copies:
        return vertex % 12
    if vertex < 12 * copies:
        return 12 + (vertex - 6 * copies) % 12
    if vertex < 18 * copies:
        return 24 + (vertex - 12 * copies) % 12
    if vertex < 20 * copies:
        return 36 + (vertex - 18 * copies) % 4
    block, local = divmod(vertex - 20 * copies, 14)
    return 40 + 14 * (block % 6) + local


def base_certificates():
    adjacency, _ = graph(2)
    assert len(BASE_SELECTION) == len(DELETION_FAILURES) == 62
    outside = set(range(124)) - BASE_SELECTION
    single = {vertex for vertex in outside if len(adjacency[vertex] & BASE_SELECTION) == 1}
    assert single == {vertex for vertex, _, _ in SINGLE_NEIGHBOR_STARS}
    assert all(len(adjacency[vertex] & BASE_SELECTION) >= 2 for vertex in outside - single)
    for vertex, center, leaf in SINGLE_NEIGHBOR_STARS:
        assert adjacency[vertex] & BASE_SELECTION == {center}
        assert leaf in adjacency[center] & BASE_SELECTION
    deletion_checks = []
    for deleted, failure in zip(sorted(BASE_SELECTION), DELETION_FAILURES):
        remaining = BASE_SELECTION - {deleted}
        assert failure not in remaining and not local_condition(adjacency, remaining, failure)
        neighbors = adjacency[failure] & remaining
        assert len(neighbors) <= 1 and all(not adjacency[neighbor] & remaining for neighbor in neighbors)
        deletion_checks.append(dict(deleted=deleted, failed_outside=failure,
                                    retained_selected_neighbors=sorted(neighbors)))
    assert verify_literal(adjacency, BASE_SELECTION) == 62
    core, pairs, _, _ = word_control('BB')
    chosen = BASE_SELECTION & set(range(40))
    ports = {vertex for pair in pairs for vertex in pair}
    internal_owners = private_owners(core, chosen)
    assert forms(core, chosen) and len(chosen) == 25
    assert chosen - ports <= internal_owners
    assert chosen - ports == set(CORE_PRIVATE_CERTIFICATES)
    for owner, certificate in CORE_PRIVATE_CERTIFICATES.items():
        center = certificate[1]
        if certificate[0] == 'A':
            support = {center} | core[center]
        else:
            neighbor = certificate[2]
            assert neighbor in core[center]
            support = {center} | (core[center] - {neighbor}) | (core[neighbor] - {center})
        assert support & chosen == {owner}
    return dict(order=124, selected=sorted(BASE_SELECTION), selected_size=62,
                core_selected=sorted(chosen), core_selected_size=25, core_forms=True,
                selected_core_ports=len(chosen & ports),
                selected_core_nonports=len(chosen - ports),
                all_selected_core_nonports_have_internal_private_clauses=True,
                explicit_core_private_certificates=CORE_PRIVATE_CERTIFICATES,
                core_patterns=[[local for local in range(20) if translate(2, block, local) in chosen]
                               for block in range(2)],
                block_patterns=[[vertex for vertex in range(14) if 40 + 14 * block + vertex in BASE_SELECTION]
                                for block in range(6)],
                formation_single_neighbor_stars=SINGLE_NEIGHBOR_STARS,
                other_outside_vertices_have_two_selected_neighbors=True,
                explicit_deletion_certificates=deletion_checks, literal_deletion_checks=62)


def cover_controls():
    base, _ = graph(2)
    records = []
    for repeats in range(1, 13):
        copies = 2 * repeats
        adjacency, _ = graph(copies)
        projected = [projection(repeats, vertex) for vertex in range(len(adjacency))]
        assert all(projected.count(vertex) == repeats for vertex in range(124))
        for vertex, neighbors in enumerate(adjacency):
            image = {projected[neighbor] for neighbor in neighbors}
            assert image == base[projected[vertex]] and len(image) == len(neighbors)
        chosen = {vertex for vertex in range(len(adjacency)) if projected[vertex] in BASE_SELECTION}
        assert len(chosen) == 62 * repeats and forms(adjacency, chosen)
        assert chosen <= private_owners(adjacency, chosen)
        core_selected = chosen & set(range(20 * copies))
        assert len(core_selected) == 25 * repeats
        inside = [neighbors & set(range(20 * copies)) for neighbors in adjacency[:20 * copies]]
        assert forms(inside, core_selected)
        bare_count = 0
        block_sizes = []
        for block in range(3 * copies):
            offset = 20 * copies + 14 * block
            selected = {vertex for vertex in chosen if offset <= vertex < offset + 14}
            block_sizes.append(len(selected))
            for port in [offset, offset + 8]:
                internal_neighbors = {neighbor for neighbor in adjacency[port]
                                      if offset <= neighbor < offset + 14}
                bare_count += not (({port} | internal_neighbors) & selected)
        assert bare_count == 0 and sum(block_sizes) == 37 * repeats
        deficits = [8 - count for count in block_sizes]
        assert sum(deficits) == 11 * repeats
        records.append(dict(repeats=repeats, k=copies, order=len(adjacency),
                            selected_size=len(chosen), core_selected_size=len(core_selected),
                            covering_locally_bijective=True,
                            full_minimality_private_owners_checked=True,
                            total_bare_ports=bare_count, core_excess_over_12k=repeats,
                            block_sizes=block_sizes, total_actual_block_loss=sum(deficits),
                            target_36k=36 * copies,
                            target_violated=False))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    base = base_certificates()
    covers = cover_controls()
    report = dict(status='ALL_CHECKS_PASSED', base=base, finite_cover_controls=covers,
                  scope='The explicit base set and deletion witnesses, together with the general triangle-free covering pullback theorem and written covering map, prove the all-r obstruction. Finite cover checks are verification only. The rule core_excess<=bare_ports is false even for an internally forming core; SF(L_k)<=36k is not refuted.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], base_selected=62, base_core_selected=25,
                         literal_base_deletions=62, finite_cover_instances=len(covers),
                         bare_ports_in_each_cover=0, target_SF_refuted=False)))


if __name__ == '__main__':
    main()
