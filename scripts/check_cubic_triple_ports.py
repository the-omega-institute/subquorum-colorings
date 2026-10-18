"""Literal controls of the additive three-pair penalty and cubic gap1/24."""

import argparse
from collections import Counter
import json
from pathlib import Path

from check_cubic_padding_rings import core, edge
from check_cubic_path_accounting import inspect
from check_cubic_starforming import SELECTED, base, dissociation
from check_regular_starforming import bipartition, masks
from check_starforming_gap import connected


PAIRS = [(12, 13), (14, 15), (16, 17)]


def triple_core():
    adjacency = core(1)
    for first, second in PAIRS:
        adjacency[first].remove(second)
        adjacency[second].remove(first)
    return adjacency


def fixed_core_control():
    adjacency = triple_core()
    neighborhoods = masks(adjacency)
    port_masks = [sum(1 << vertex for vertex in pair) for pair in PAIRS]
    ports = [vertex for pair in PAIRS for vertex in pair]
    profiles = {}
    totals = Counter()
    for selection in range(1 << 20):
        selected = [vertex for vertex in range(20) if selection >> vertex & 1]
        if any((neighborhoods[vertex] & selection).bit_count() > 1 for vertex in selected):
            continue
        omitted = sum(not selection & pair for pair in port_masks)
        chosen_ports = sum(selection >> vertex & 1 for vertex in ports)
        isolated = sum(not neighborhoods[vertex] & selection for vertex in selected)
        complement_edges = sum(vertex < neighbor and not selection >> vertex & 1 and
                               not selection >> neighbor & 1
                               for vertex, neighbors in enumerate(adjacency) for neighbor in neighbors)
        assert 54 - 5 * len(selected) + 2 * chosen_ports == isolated + 2 * complement_edges
        assert len(selected) + omitted <= 12
        signature = ''.join(str(selection >> vertex & 1) for vertex in ports)
        if signature not in profiles or profiles[signature]['beta'] < len(selected):
            profiles[signature] = dict(beta=len(selected), omitted_pairs=omitted, witness=selected)
        totals['dissociation_sets'] += 1
        totals['exact_deficiency_identities'] += 1
        totals['omitted_pairs_' + str(omitted)] += 1
    assert len(profiles) == 64
    maxima = {omitted: max(record['beta'] for record in profiles.values()
                          if record['omitted_pairs'] == omitted) for omitted in range(4)}
    assert maxima == {0: 12, 1: 11, 2: 10, 3: 9}
    return dict(order=20, subsets=1 << 20, totals=dict(totals), profiles=profiles,
                optimum_by_omitted_pair_count=maxima,
                scope='Independent all-subset test of the fixed core. The general local case proof does not use these values as premises.')


def ring(copies):
    adjacency = []
    selected = set()
    attaining = set()
    interfaces = []
    for module in range(copies):
        core_offset = len(adjacency)
        adjacency.extend({core_offset + neighbor for neighbor in neighbors} for neighbors in triple_core())
        selected |= set(range(core_offset, core_offset + 12))
        attaining |= {core_offset + vertex for vertex in [1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]}
        for pair_index in range(2):
            offset = len(adjacency)
            heawood = base()
            heawood[0].remove(8)
            heawood[8].remove(0)
            adjacency.extend({offset + neighbor for neighbor in neighbors} for neighbors in heawood)
            first, second = PAIRS[pair_index]
            edge(adjacency, offset, core_offset + second)
            edge(adjacency, offset + 8, core_offset + first)
            selected |= {offset + vertex for vertex in SELECTED}
            attaining |= set(range(offset, offset + 7))
        interfaces.append((core_offset + 16, core_offset + 17))
    for index, (first, second) in enumerate(interfaces):
        edge(adjacency, first, interfaces[(index + 1) % copies][1])
    return adjacency, selected, attaining


def ring_control(copies):
    adjacency, selected, attaining = ring(copies)
    assert len(adjacency) == 48 * copies
    assert len(selected) == 28 * copies
    assert len(attaining) == 26 * copies
    assert bipartition(adjacency) is not None
    assert all(len(neighbors) == 3 and vertex not in neighbors and
               all(vertex in adjacency[neighbor] for neighbor in neighbors)
               for vertex, neighbors in enumerate(adjacency))
    assert connected(adjacency)
    assert all(connected(adjacency, deleted) for deleted in range(len(adjacency)))
    assert dissociation(adjacency, attaining)
    accounting = inspect(adjacency, selected, len(attaining))
    assert accounting['isolates'] == 4 * copies
    assert accounting['high_paths'] == accounting['slack'] == 0
    assert accounting['augmented_exchange_sizes'] == [len(attaining), len(attaining)]
    assert 24 * (len(selected) - len(attaining)) == len(adjacency)
    return dict(r=copies, order=len(adjacency),
                SF_by_written_omission_composition_and_compensation=28 * copies,
                beta_by_written_omission_composition=26 * copies,
                gap=2 * copies, two_connected=True,
                selected_deletion_checks=len(selected), vertex_deletion_checks=len(adjacency),
                accounting=accounting)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    fixed = fixed_core_control()
    records = [ring_control(copies) for copies in range(1, 11)]
    adjacency, selected, attaining = ring(1)
    report = dict(status='ALL_CHECKS_PASSED',
                  scope='Finite verification of the written additive three-pair omission proof and all-r cubic n48r,beta26r,SF28r family. Fixed-core optima are independently exhaustive; larger beta/SF values are consequences of the written composition and displayed attainment, not independent optimizations.',
                  fixed_core=fixed, rings=records,
                  example=dict(r=1, adjacency=[sorted(neighbors) for neighbors in adjacency],
                               selection=sorted(selected), dissociation_witness=sorted(attaining)),
                  totals=dict(fixed_core_subsets=1 << 20,
                              fixed_core_dissociation_sets=fixed['totals']['dissociation_sets'],
                              port_patterns=len(fixed['profiles']), rings=len(records),
                              selected_deletion_checks=sum(record['selected_deletion_checks'] for record in records),
                              vertex_deletion_checks=sum(record['vertex_deletion_checks'] for record in records)))
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], totals=report['totals'],
                         optimum_by_omitted_pairs=fixed['optimum_by_omitted_pair_count'])))


if __name__ == '__main__':
    main()
