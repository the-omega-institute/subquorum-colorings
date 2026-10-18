"""Independent controls for twice-cut Heawood blocks and arbitrary interfaces."""

import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random

from check_cubic_padding_rings import edge
from check_cubic_path_accounting import inspect
from check_cubic_starforming import SELECTED, base, dissociation
from check_cubic_triple_ports import PAIRS, triple_core
from check_regular_starforming import bipartition
from check_starforming_gap import connected, forms


CORE_WITNESS = {0, 1, 3, 4, 8, 11, 12, 13, 15, 16, 18, 19}
BLOCK_WITNESS = {0, 2, 4, 6, 8, 11, 12, 13}


def remove(adjacency, first, second):
    adjacency[first].remove(second)
    adjacency[second].remove(first)


def all_two_cut_caps():
    original = base()
    edges = [(first, second) for first, neighbors in enumerate(original)
             for second in sorted(neighbors) if first < second]
    subsets = [[vertex for vertex in range(14) if selection >> vertex & 1]
               for selection in range(1 << 14)]
    records = []
    totals = Counter()
    for first_edge, second_edge in combinations(edges, 2):
        if set(first_edge) & set(second_edge):
            continue
        adjacency = [set(neighbors) for neighbors in original]
        for first, second in [first_edge, second_edge]:
            remove(adjacency, first, second)
        masks = [sum(1 << neighbor for neighbor in neighbors) for neighbors in adjacency]
        optimum = 0
        witness = None
        dense = 0
        for selection, chosen in enumerate(subsets):
            if not all((masks[vertex] & selection).bit_count() <= 1 for vertex in chosen):
                continue
            totals['dissociation_sets'] += 1
            if len(chosen) > optimum:
                optimum = len(chosen)
                witness = chosen
            dense += len(chosen) == 8
        assert optimum == 8
        records.append(dict(cuts=[first_edge, second_edge], beta=optimum,
                            witness=witness, eight_sets=dense))
    assert len(records) == 168
    totals['cut_pairs'] = len(records)
    totals['subsets'] = len(records) * (1 << 14)
    return dict(totals=dict(totals), instances=records)


def explicit_obstacle():
    adjacency = triple_core()
    block = base()
    remove(block, 0, 8)
    remove(block, 4, 12)
    assert dissociation(block, BLOCK_WITNESS)
    assert not block[0] & BLOCK_WITNESS and not block[8] & BLOCK_WITNESS
    assert all(len(block[port] & BLOCK_WITNESS) == 1 for port in [4, 12])
    adjacency += [{20 + neighbor for neighbor in neighbors} for neighbors in block]
    edge(adjacency, 20, 13)
    edge(adjacency, 28, 12)
    witness = CORE_WITNESS | {20 + vertex for vertex in BLOCK_WITNESS}
    selection = set(range(12)) | {20 + vertex for vertex in SELECTED}
    assert len(witness) == len(selection) == 20
    assert dissociation(adjacency, witness)
    assert forms(adjacency, selection)
    assert all(not forms(adjacency, selection - {deleted}) for deleted in selection)
    assert bipartition(adjacency) is not None
    assert all(connected(adjacency, deleted) for deleted in range(34))
    ports = {vertex for vertex in range(34) if len(adjacency[vertex]) == 2}
    assert ports == {14, 15, 16, 17, 24, 32}
    saturated = ports & witness
    assert saturated == {15, 16, 24, 32}
    assert all(len(adjacency[port] & witness) == 1 for port in saturated)
    return dict(order=34, beta_by_written_caps_and_witness=20,
                invalid_local_cap=19, adjacency=[sorted(neighbors) for neighbors in adjacency],
                witness=sorted(witness), minimal_forming_selection=sorted(selection),
                deficient_ports=sorted(ports), saturated_selected_ports=sorted(saturated),
                omitted_ports=sorted(ports - witness), selected_deletion_checks=len(selection),
                vertex_deletion_checks=34)


def composition(attachments, generator):
    adjacency = []
    selection = set()
    remaining = [[], []]
    for attached in attachments:
        core_offset = len(adjacency)
        adjacency += [{core_offset + neighbor for neighbor in neighbors} for neighbors in triple_core()]
        selection |= set(range(core_offset, core_offset + 12))
        for pair_index, (first, second) in enumerate(PAIRS):
            if pair_index >= attached:
                remaining[0].append(core_offset + first)
                remaining[1].append(core_offset + second)
                continue
            offset = len(adjacency)
            block = base()
            remove(block, 0, 8)
            adjacency += [{offset + neighbor for neighbor in neighbors} for neighbors in block]
            selection |= {offset + vertex for vertex in SELECTED}
            edge(adjacency, offset, core_offset + second)
            edge(adjacency, offset + 8, core_offset + first)
    for attempt in range(10000):
        partners = generator.sample(remaining[1], len(remaining[1]))
        matching = list(zip(remaining[0], partners))
        if all(second not in adjacency[first] for first, second in matching):
            break
    else:
        raise AssertionError('No simple finite control matching')
    for first, second in matching:
        edge(adjacency, first, second)
    return adjacency, selection, matching


def interface_controls():
    generator = random.Random(2026101925)
    examples = [[0], [1], [2], [3], [0, 0], [1, 2], [2, 2], [3, 3], [3, 0, 1]]
    examples += [[generator.randrange(4) for core in range(cores)]
                 for cores in range(2, 9) for trial in range(5)]
    records = []
    for attachments in examples:
        adjacency, selection, matching = composition(attachments, generator)
        cores, blocks = len(attachments), sum(attachments)
        beta = 12 * cores + 7 * blocks
        expected_sf = 12 * cores + 8 * blocks
        assert len(adjacency) == 20 * cores + 14 * blocks
        assert len(selection) == expected_sf
        accounting = inspect(adjacency, selection, beta)
        assert accounting['isolates'] == 2 * blocks
        assert accounting['augmented_exchange_sizes'] == [beta, beta]
        is_connected = connected(adjacency)
        if is_connected and cores >= 2:
            assert max(attachments) <= 2 and blocks <= 2 * cores
            assert 24 * blocks <= len(adjacency)
        records.append(dict(attachments=attachments, core_matching=matching,
                            order=len(adjacency), beta_by_written_composition=beta,
                            SF_by_written_composition=expected_sf, gap=blocks,
                            connected=is_connected, accounting=accounting))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    caps = all_two_cut_caps()
    obstacle = explicit_obstacle()
    interfaces = interface_controls()
    report = dict(status='ALL_CHECKS_PASSED',
                  scope='The all-disjoint-cut cap and arbitrary-interface theorem have written proofs. All fixed Heawood cuts are independently exhaustive; the explicit local nineteen-cap failure has a twenty-vertex witness. General composition values follow from the written local caps, isolate and cubic compensation, not larger independent optimization.',
                  heawood_two_cuts=caps, obstacle=obstacle, interfaces=interfaces,
                  totals=dict(two_cut_pairs=caps['totals']['cut_pairs'],
                              two_cut_subsets=caps['totals']['subsets'], interfaces=len(interfaces),
                              connected_interfaces=sum(record['connected'] for record in interfaces),
                              selected_deletion_checks=20 + sum(record['SF_by_written_composition'] for record in interfaces)))
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], totals=report['totals'])))


if __name__ == '__main__':
    main()
