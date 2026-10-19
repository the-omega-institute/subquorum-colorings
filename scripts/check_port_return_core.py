"""Controls for the all-saturated core obstruction and direct-return slack."""

import argparse
from itertools import combinations
import json
from pathlib import Path

from check_boundary_loss import private_owners
from check_cubic_starforming import SELECTED
from check_port_return import containing_stars, literal_at
from check_regular_starforming import bipartition
from check_starforming_gap import forms, local_condition
from explore_long_core_SF import graph, verify_literal


CORE = {1, 2, 3, 4, 6, 8, 9, 10, 11, 12}
TRANSFER = {0, 3, 4, 5, 7, 9, 10, 11}
BASE_SELECTED = CORE | {20 + vertex for vertex in TRANSFER} | {
    offset + vertex for offset in (34, 48) for vertex in SELECTED}


def projection(copies, vertex):
    if vertex < 6 * copies:
        return vertex % 6
    if vertex < 12 * copies:
        return 6 + (vertex - 6 * copies) % 6
    if vertex < 18 * copies:
        return 12 + (vertex - 12 * copies) % 6
    if vertex < 20 * copies:
        return 18 + (vertex - 18 * copies) % 2
    block, local = divmod(vertex - 20 * copies, 14)
    return 20 + 14 * (block % 3) + local


def capacity_values(adjacency, selected, beta=None):
    assert all(len(neighbors) == 3 for neighbors in adjacency)
    counts = [len(neighbors & selected) for neighbors in adjacency]
    isolates = sum(counts[vertex] == 0 for vertex in selected)
    direct_roots = {port for port in selected if counts[port] == 2 and
                    any(outside not in selected and adjacency[outside] & selected == {port}
                        for outside in adjacency[port])}
    assert 5 * len(selected) + isolates + len(direct_roots) <= 3 * len(adjacency)
    if beta is not None:
        assert 7 * len(selected) + len(direct_roots) <= 3 * len(adjacency) + 2 * beta
    return dict(isolates=isolates, direct_degree_two_roots=len(direct_roots),
                refined_capacity_slack=3 * len(adjacency) - 5 * len(selected) - isolates,
                linear_slack=None if beta is None else
                3 * len(adjacency) + 2 * beta - 7 * len(selected))


def small_cubic_controls():
    edges = list(combinations(range(6), 2))
    graphs = minimal_sets = strengthened_cases = bipartite_sets = 0
    for chosen_edges in combinations(edges, 9):
        adjacency = [set() for vertex in range(6)]
        for first, second in chosen_edges:
            adjacency[first].add(second)
            adjacency[second].add(first)
        if any(len(neighbors) != 3 for neighbors in adjacency):
            continue
        graphs += 1
        containing = containing_stars(adjacency)
        selections = [{vertex for vertex in range(6) if mask >> vertex & 1}
                      for mask in range(64)]
        forming = [all(literal_at(containing, selected, outside)
                       for outside in set(range(6)) - selected) for selected in selections]
        beta = None
        if bipartition(adjacency) is not None:
            beta = max(len(selected) for selected in selections
                       if all(len(adjacency[vertex] & selected) <= 1 for vertex in selected))
        for mask, selected in enumerate(selections):
            if not forming[mask] or any(forming[mask ^ (1 << vertex)] for vertex in selected):
                continue
            values = capacity_values(adjacency, selected, beta)
            minimal_sets += 1
            strengthened_cases += values['direct_degree_two_roots'] > 0
            bipartite_sets += beta is not None
    assert graphs == 70
    return dict(cubic_graphs_order_six=graphs, minimal_selections=minimal_sets,
                strict_direct_corrections=strengthened_cases,
                bipartite_minimal_selections=bipartite_sets)


def obstruction_controls():
    base, _ = graph(1)
    assert len(BASE_SELECTED) == 34 and verify_literal(base, BASE_SELECTED) == 34
    deletions = []
    for deleted in sorted(BASE_SELECTED):
        remaining = BASE_SELECTED - {deleted}
        failure = min(outside for outside in set(range(62)) - remaining
                      if not local_condition(base, remaining, outside))
        deletions.append(dict(deleted=deleted, failing_vertex=failure))
    records = []
    for copies in range(1, 13):
        adjacency, _ = graph(copies)
        projected = [projection(copies, vertex) for vertex in range(len(adjacency))]
        assert all(projected.count(vertex) == copies for vertex in range(62))
        assert all({projected[neighbor] for neighbor in neighbors} == base[projected[vertex]]
                   and len(neighbors) == len(base[projected[vertex]])
                   for vertex, neighbors in enumerate(adjacency))
        selected = {vertex for vertex, image in enumerate(projected) if image in BASE_SELECTED}
        assert forms(adjacency, selected) and selected <= private_owners(adjacency, selected)
        core_selected = selected & set(range(20 * copies))
        assert len(selected) == 34 * copies and len(core_selected) == 10 * copies
        assert all(sum(20 * copies + 14 * block + local in selected for local in range(14)) == 8
                   for block in range(3 * copies))
        for block in range(3 * copies):
            offset = 20 * copies + 14 * block
            for port in (offset, offset + 8):
                assert ({port} | {neighbor for neighbor in adjacency[port]
                                  if offset <= neighbor < offset + 14}) & selected
        signals = []
        for cell in range(copies):
            port = 20 * copies + 42 * cell
            incoming = 12 * copies + 6 * cell
            exit_vertex = incoming + 1
            assert incoming in selected and exit_vertex not in selected
            assert adjacency[exit_vertex] & selected == {port}
            assert len(adjacency[port] & selected) == 2
            signals.append(dict(port=port, incoming_owner=incoming, return_witness=exit_vertex))
        assert len({signal['return_witness'] for signal in signals}) == copies
        values = capacity_values(adjacency, selected, 33 * copies + copies // 2)
        assert values['direct_degree_two_roots'] >= copies
        records.append(dict(k=copies, order=len(adjacency), selected_size=len(selected),
                            core_selected_size=len(core_selected), all_block_sizes_eight=True,
                            total_actual_block_loss=0, total_bare_ports=0,
                            saturated_directional_imports=copies, direct_returns=copies,
                            core_deficit_below_12k=2 * copies,
                            neighborhood_cover_checked=True, private_minimality_checked=True,
                            **values))
    return dict(base_selected=sorted(BASE_SELECTED), base_core_selected=sorted(CORE),
                literal_base_deletions=34, deletion_certificates=deletions,
                finite_cover_controls=records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    small = small_cubic_controls()
    obstruction = obstruction_controls()
    report = dict(status='ALL_CHECKS_PASSED', cubic_capacity=small,
                  all_saturated_obstruction=obstruction,
                  scope='Written general capacity identity proves the direct-return slack. '
                        'The explicit base certificate and triangle-free covering theorem '
                        'prove an all-k minimal family with 34k selections, 10k core vertices, '
                        'k directional signals and zero actual block loss. Finite controls '
                        'do not replace these proofs or refute SF(L_k)<=36k.')
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], cubic_capacity=small,
                         literal_base_deletions=34, finite_covers=12,
                         block_deficits_in_each_cover=0)))


if __name__ == '__main__':
    main()
