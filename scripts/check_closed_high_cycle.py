"""Independent controls of closed-high-cycle omission and exact cubic rings."""

import argparse
from collections import Counter
import json
from pathlib import Path
import random

from check_cubic_padding_rings import core, edge
from check_cubic_path_accounting import inspect, pair_stubs
from check_cubic_starforming import SELECTED, base, dissociation
from check_cubic_triple_ports import PAIRS, triple_core
from check_regular_starforming import bipartition, covered, masks, star_lists
from check_starforming_gap import connected


def open_core():
    adjacency = triple_core()
    adjacency[12].remove(17)
    adjacency[17].remove(12)
    return adjacency


def fixed_core_control():
    adjacency = open_core()
    neighborhoods = masks(adjacency)
    pairs = [sum(1 << vertex for vertex in pair) for pair in PAIRS]
    totals = Counter()
    profiles = {}
    boundary_profiles = {}
    for selection in range(1 << 20):
        selected = {vertex for vertex in range(20) if selection >> vertex & 1}
        if any((selection & neighborhoods[vertex]).bit_count() > 1 for vertex in selected):
            continue
        omitted = sum(not selection & pair for pair in pairs)
        score = len(selected) + omitted
        assert score <= 12
        signature = ''.join(str(selection >> vertex & 1) for vertex in range(12, 18))
        if signature not in profiles or profiles[signature]['size'] < len(selected):
            profiles[signature] = dict(size=len(selected), omitted=omitted,
                                       score=score, witness=sorted(selected))
        boundary = tuple(0 if vertex not in selected else
                         1 + len(adjacency[vertex] & selected) for vertex in (12, 17))
        boundary_key = ','.join(map(str, boundary))
        if boundary_key not in boundary_profiles or boundary_profiles[boundary_key]['score'] < score:
            boundary_profiles[boundary_key] = dict(score=score, witness=sorted(selected))
        normalized = set(selected)
        for pair in PAIRS:
            if len(normalized & set(pair)) == 1:
                normalized -= set(pair)
        normalized_omitted = sum(not normalized & set(pair) for pair in PAIRS)
        assert dissociation(adjacency, normalized)
        assert len(normalized) + normalized_omitted == score
        cells = [sum(vertex in normalized for vertex in (2 * index, 2 * index + 1,
                                                        6 + 2 * index, 7 + 2 * index))
                 + int(12 + 2 * index in normalized) for index in range(3)]
        hubs = len(normalized & {18, 19})
        assert all(weight <= 3 for weight in cells)
        assert score == 3 + sum(cells) + hubs
        if hubs == 1:
            assert sum(cells) <= 8
        if hubs == 2:
            assert sum(weight == 3 for weight in cells) <= 1
        reflected = {5 - vertex if vertex < 6 else
                     17 - vertex if vertex < 12 else
                     29 - vertex if vertex < 18 else 37 - vertex for vertex in selected}
        assert dissociation(adjacency, reflected)
        totals['dissociation_sets'] += 1
        totals['normalizations'] += 1
        totals['hub_case_' + str(hubs)] += 1
        totals['reflection_checks'] += 1
    assert len(profiles) == 64 and len(boundary_profiles) == 9
    assert all(record['score'] == 12 for record in boundary_profiles.values())
    opened_high = [set(neighbors) for neighbors in adjacency]
    opened_high[1].remove(2)
    opened_high[2].remove(1)
    exceptional = {0, 1, 2, 3, 10, 11, 12, 13, 14, 15, 18, 19}
    assert dissociation(opened_high, exceptional)
    assert not dissociation(adjacency, exceptional)
    assert len(exceptional) + sum(not exceptional & set(pair) for pair in PAIRS) == 13
    return dict(order=20, subsets=1 << 20, totals=dict(totals), port_profiles=profiles,
                boundary_score_profiles=boundary_profiles,
                essential_high_seam_control=dict(deleted_edge=[1, 2],
                                                  selection=sorted(exceptional), score=13),
                scope='All-subset control only. The general omission proof uses cell inequalities and the intact high six-cycle, not the enumerated optimum.')


def ring(copies):
    adjacency = []
    selected = set()
    attaining = set()
    interfaces = []
    for module in range(copies):
        core_offset = len(adjacency)
        adjacency.extend({core_offset + neighbor for neighbor in neighbors} for neighbors in open_core())
        selected |= set(range(core_offset, core_offset + 12))
        attaining |= {core_offset + vertex for vertex in [1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]}
        for first, second in PAIRS:
            offset = len(adjacency)
            heawood = base()
            heawood[0].remove(8)
            heawood[8].remove(0)
            adjacency.extend({offset + neighbor for neighbor in neighbors} for neighbors in heawood)
            edge(adjacency, offset, core_offset + second)
            edge(adjacency, offset + 8, core_offset + first)
            selected |= {offset + vertex for vertex in SELECTED}
            attaining |= set(range(offset, offset + 7))
        interfaces.append((core_offset + 12, core_offset + 17))
    for index, (first, second) in enumerate(interfaces):
        edge(adjacency, first, interfaces[(index + 1) % copies][1])
    return adjacency, selected, attaining


def ring_control(copies):
    adjacency, selected, attaining = ring(copies)
    assert len(adjacency) == 62 * copies
    assert len(selected) == 36 * copies and len(attaining) == 33 * copies
    assert bipartition(adjacency) is not None
    assert all(len(neighbors) == 3 and vertex not in neighbors and
               all(vertex in adjacency[neighbor] for neighbor in neighbors)
               for vertex, neighbors in enumerate(adjacency))
    assert connected(adjacency)
    assert all(connected(adjacency, deleted) for deleted in range(len(adjacency)))
    assert dissociation(adjacency, attaining)
    accounting = inspect(adjacency, selected, len(attaining))
    assert accounting['isolates'] == 6 * copies
    assert accounting['high_paths'] == accounting['slack'] == 0
    assert accounting['augmented_exchange_sizes'] == [33 * copies, 33 * copies]
    return dict(r=copies, order=len(adjacency),
                beta_by_written_omission_proof=33 * copies,
                SF_by_written_compensation_and_attainment=36 * copies,
                gap=3 * copies, two_connected=True,
                selected_deletion_checks=len(selected), vertex_deletion_checks=len(adjacency),
                accounting=accounting)


def arbitrary_gluing_control(cores, blocks, generator):
    adjacency = []
    selected = set()
    attaining = set()
    left = []
    right = []
    for module in range(cores):
        offset = len(adjacency)
        local = core(1)
        for vertex in range(12, 18):
            local[vertex] -= set(range(12, 18))
        adjacency.extend({offset + neighbor for neighbor in neighbors} for neighbors in local)
        selected |= set(range(offset, offset + 12))
        attaining |= {offset + vertex for vertex in [1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16]}
        left.extend(offset + vertex for vertex in (12, 14, 16))
        right.extend(offset + vertex for vertex in (13, 15, 17))
    left_ports = generator.sample(left, blocks)
    right_ports = generator.sample(right, blocks)
    for index in range(blocks):
        offset = len(adjacency)
        heawood = base()
        heawood[0].remove(8)
        heawood[8].remove(0)
        adjacency.extend({offset + neighbor for neighbor in neighbors} for neighbors in heawood)
        edge(adjacency, offset, right_ports[index])
        edge(adjacency, offset + 8, left_ports[index])
        selected |= {offset + vertex for vertex in SELECTED}
        attaining |= set(range(offset, offset + 7))
    left_stubs = [vertex for vertex in left for stub in range(3 - len(adjacency[vertex]))]
    right_stubs = [vertex for vertex in right for stub in range(3 - len(adjacency[vertex]))]
    pair_stubs(adjacency, left_stubs, right_stubs, generator)
    assert len(adjacency) == 20 * cores + 14 * blocks
    assert bipartition(adjacency) is not None
    assert all(len(neighbors) == 3 for neighbors in adjacency)
    assert len(attaining) == 12 * cores + 7 * blocks
    assert dissociation(adjacency, attaining)
    stars = star_lists(adjacency)
    mask = sum(1 << vertex for vertex in selected)
    assert all(covered(stars, mask, vertex) for vertex in set(range(len(adjacency))) - selected)
    for deleted in selected:
        smaller = mask ^ (1 << deleted)
        assert any(not covered(stars, smaller, vertex)
                   for vertex in set(range(len(adjacency))) - (selected - {deleted}))
    return dict(cores=cores, blocks=blocks, order=len(adjacency),
                dissociation_lower_bound=len(attaining),
                minimal_forming_witness_size=len(selected),
                selected_deletion_checks=len(selected),
                exact_beta_or_SF_independently_optimized=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    fixed = fixed_core_control()
    records = [ring_control(copies) for copies in range(1, 11)]
    generator = random.Random(20261019)
    arbitrary = [arbitrary_gluing_control(cores, blocks, generator)
                 for cores in range(1, 6) for blocks in range(3 * cores + 1)
                 for sample in range(2)]
    adjacency, selected, attaining = ring(1)
    report = dict(status='ALL_CHECKS_PASSED', fixed_core=fixed, rings=records,
                  architecture_controls=arbitrary,
                  example=dict(adjacency=[sorted(neighbors) for neighbors in adjacency],
                               selection=sorted(selected), dissociation_witness=sorted(attaining)),
                  totals=dict(fixed_core_subsets=1 << 20,
                              fixed_core_dissociation_sets=fixed['totals']['dissociation_sets'],
                              port_patterns=len(fixed['port_profiles']), rings=len(records),
                              selected_deletion_checks=sum(record['selected_deletion_checks'] for record in records),
                              vertex_deletion_checks=sum(record['vertex_deletion_checks'] for record in records),
                              arbitrary_gluing_instances=len(arbitrary),
                              arbitrary_gluing_selected_deletion_checks=sum(record['selected_deletion_checks'] for record in arbitrary)),
                  scope='Independent fixed-core enumeration, normalization and hub cases; actual ring formation/deletion, dissociation attainment and every vertex-deletion connectivity. Random arbitrary-gluing controls test the architecture lower bound and minimal forming selection, without claiming optimized parameters. All-r exact parameters and architecture upper bound require the written proof; no solver optimum is used as a premise.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], totals=report['totals'])))


if __name__ == '__main__':
    main()
