"""Independent periodic weights, fixed-core enumeration and ring witnesses."""

import argparse
from collections import Counter
import json
from pathlib import Path

from check_cubic_path_accounting import inspect
from check_cubic_starforming import SELECTED, base, dissociation
from check_cubic_stability_ports import construction
from check_regular_starforming import bipartition, masks
from check_starforming_gap import connected


HIGH_WEIGHTS = [1, 0, 0, -1, 2, -2]
LEAF_WEIGHTS = [0, -1, 1, 0, -1, 1]
OUTSIDE_WEIGHTS = [-1, 2, -2, 1, 0, 0]


def edge(adjacency, first, second):
    assert first != second and second not in adjacency[first]
    adjacency[first].add(second)
    adjacency[second].add(first)


def core(copies):
    size = 6 * copies
    adjacency = [set() for vertex in range(20 * copies)]
    for index in range(size):
        for first, second in [(index, (index + 1) % size),
                              (2 * size + index, 2 * size + (index + 1) % size),
                              (index, size + index), (size + index, 2 * size + index),
                              (size + index, 3 * size + 2 * (index // 6) + index % 2)]:
            edge(adjacency, first, second)
    return adjacency


def broken_core(copies):
    adjacency = core(copies)
    first_pair = (12 * copies, 12 * copies + 1)
    second_pair = (12 * copies + 2, 12 * copies + 3)
    for first, second in (first_pair, second_pair):
        adjacency[first].remove(second)
        adjacency[second].remove(first)
    return adjacency, first_pair, second_pair


def core_control(copies):
    original = core(copies)
    adjacency, first_pair, second_pair = broken_core(copies)
    size = 6 * copies
    weights = [HIGH_WEIGHTS[index % 6] for index in range(size)]
    weights += [LEAF_WEIGHTS[index % 6] for index in range(size)]
    weights += [OUTSIDE_WEIGHTS[index % 6] for index in range(size)]
    weights += [0] * (2 * copies)
    assert sum(weights) == 0
    assert all(sum(weights[neighbor] for neighbor in neighbors) + 2 * weights[vertex] == 0
               for vertex, neighbors in enumerate(original))
    assert sum(weights[vertex] for vertex in first_pair) == 1
    assert sum(weights[vertex] for vertex in second_pair) == -1
    assert sum(3 - len(neighbors) for neighbors in adjacency) == 4
    assert all(len(neighbors) == (2 if vertex in first_pair + second_pair else 3)
               for vertex, neighbors in enumerate(adjacency))
    attaining = set(range(size, 2 * size)) | set(range(1, size, 2)) | set(range(2 * size, 3 * size, 2))
    assert len(attaining) == 12 * copies and dissociation(adjacency, attaining)
    return dict(k=copies, order=len(adjacency), weight_sum=sum(weights),
                row_identities_checked=len(adjacency), first_pair_weight=1, second_pair_weight=-1,
                dissociation_witness_size=len(attaining))


def enumerate_fixed_core():
    adjacency, first_pair, second_pair = broken_core(1)
    neighborhoods = masks(adjacency)
    ports = first_pair + second_pair
    first_mask = sum(1 << vertex for vertex in first_pair)
    second_mask = sum(1 << vertex for vertex in second_pair)
    profile = {}
    totals = Counter()
    for selection in range(1 << len(adjacency)):
        selected = [vertex for vertex in range(len(adjacency)) if selection >> vertex & 1]
        if any((neighborhoods[vertex] & selection).bit_count() > 1 for vertex in selected):
            continue
        signature = ''.join(str(selection >> vertex & 1) for vertex in ports)
        total_ports = sum(selection >> vertex & 1 for vertex in ports)
        isolated = sum(not neighborhoods[vertex] & selection for vertex in selected)
        outside_edges = sum(vertex < neighbor and not selection >> vertex & 1 and
                            not selection >> neighbor & 1
                            for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors)
        assert 60 - 5 * len(selected) - 4 + 2 * total_ports == isolated + 2 * outside_edges
        assert len(selected) <= 12
        if not selection & first_mask or not selection & second_mask:
            assert len(selected) <= 11
        if signature not in profile or len(selected) > profile[signature]['beta']:
            profile[signature] = dict(beta=len(selected), witness=selected)
        totals['dissociation_sets'] += 1
        totals['exact_deficiency_identities'] += 1
    assert len(profile) == 16 and max(record['beta'] for record in profile.values()) == 12
    return dict(order=20, ports=ports, subsets=1 << len(adjacency),
                totals=dict(totals), profile=profile,
                scope='All subsets of the fixed20vertex gadget, independently testing the all-k written weight proof.')


def ring(core_sizes):
    adjacency = []
    selected = set()
    attaining = set()
    modules = []
    for copies in core_sizes:
        block_offset = len(adjacency)
        heawood = base()
        heawood[0].remove(8)
        heawood[8].remove(0)
        adjacency.extend({block_offset + neighbor for neighbor in neighbors} for neighbors in heawood)
        core_offset = len(adjacency)
        local, first_pair, second_pair = broken_core(copies)
        adjacency.extend({core_offset + neighbor for neighbor in neighbors} for neighbors in local)
        edge(adjacency, block_offset, core_offset + first_pair[1])
        edge(adjacency, block_offset + 8, core_offset + first_pair[0])
        selected |= {block_offset + vertex for vertex in SELECTED}
        selected |= set(range(core_offset, core_offset + 12 * copies))
        attaining |= set(range(block_offset, block_offset + 7))
        attaining |= set(range(core_offset + 6 * copies, core_offset + 12 * copies))
        attaining |= set(range(core_offset + 1, core_offset + 6 * copies, 2))
        attaining |= set(range(core_offset + 12 * copies, core_offset + 18 * copies, 2))
        modules.append((core_offset + second_pair[0], core_offset + second_pair[1]))
    for index, (first, second) in enumerate(modules):
        edge(adjacency, first, modules[(index + 1) % len(modules)][1])
    return adjacency, selected, attaining


def ring_control(core_sizes):
    adjacency, selected, attaining = ring(core_sizes)
    copies, total = len(core_sizes), sum(core_sizes)
    assert len(adjacency) == 14 * copies + 20 * total
    assert len(selected) == 8 * copies + 12 * total
    assert len(attaining) == 7 * copies + 12 * total
    assert all(len(neighbors) == 3 and vertex not in neighbors and
               all(vertex in adjacency[neighbor] for neighbor in neighbors)
               for vertex, neighbors in enumerate(adjacency))
    assert bipartition(adjacency) is not None and connected(adjacency)
    assert all(connected(adjacency, removed) for removed in range(len(adjacency)))
    assert dissociation(adjacency, attaining)
    assert 7 * len(selected) == 3 * len(adjacency) + 2 * len(attaining)
    accounting = inspect(adjacency, selected, len(attaining))
    assert accounting['high_paths'] == accounting['slack'] == 0
    assert accounting['isolates'] == 2 * copies
    assert accounting['augmented_exchange_sizes'] == [len(attaining), len(attaining)]
    if copies == 1:
        previous = construction(core_sizes[0])
        assert adjacency == previous[0] and selected == previous[1] and attaining == previous[2]
    return dict(core_sizes=core_sizes, order=len(adjacency),
                SF_by_written_compensation_and_witness=len(selected),
                beta_by_written_four_port_proof=len(attaining), gap=copies,
                two_connected=True, vertex_deletion_checks=len(adjacency),
                accounting=accounting)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    for copies in (1, 2, 3, 5, 8):
        for sizes in ([1] * copies, [2] * copies, [1 + index % 3 for index in range(copies)]):
            records.append(ring_control(sizes))
    adjacency, selected, attaining = ring([1, 1])
    report = dict(status='ALL_CHECKS_PASSED',
                  scope='All-order claims have written deficiency/periodic-weight/interface proofs. Finite controls verify the fixed four-port core exhaustively, periodic identities, literal minimality, dissociation attainment, normal-form equality and every vertex deletion. Larger exact beta/SF labels cite the written proof, not an independent optimizer.',
                  fixed_core=enumerate_fixed_core(),
                  periodic_cores=[core_control(copies) for copies in range(1, 17)],
                  rings=records,
                  example=dict(core_sizes=[1, 1], adjacency=[sorted(neighbors) for neighbors in adjacency],
                               selection=sorted(selected), dissociation_witness=sorted(attaining)),
                  totals=dict(rings=len(records),
                              vertex_deletion_checks=sum(record['order'] for record in records),
                              selected_deletion_checks=sum(record['SF_by_written_compensation_and_witness'] for record in records),
                              periodic_rows=sum(20 * copies for copies in range(1, 17)),
                              fixed_core_subsets=1 << 20))
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], totals=report['totals'],
                         fixed_core=report['fixed_core']['totals'])))


if __name__ == '__main__':
    main()
