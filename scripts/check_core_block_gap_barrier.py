"""Independent witness controls for arbitrary core-to-Heawood attachments."""

import argparse
from collections import Counter
import json
from pathlib import Path
import random

from check_cubic_padding_rings import core, edge
from check_cubic_path_accounting import pair_stubs
from check_cubic_starforming import EIGHT, SELECTED, base, dissociation
from check_regular_starforming import bipartition, selected_certificate


def instance(cores, blocks, mode, generator):
    for attempt in range(100):
        adjacency = []
        forming = set()
        first = set()
        second = set()
        highs = [[], []]
        leaves = [[], []]
        hubs = [[], []]
        interfaces = [[], []]
        for module in range(cores):
            offset = len(adjacency)
            local = core(1)
            for vertex in range(12, 18):
                local[vertex] -= set(range(12, 18))
            adjacency.extend({offset + neighbor for neighbor in neighbors}
                             for neighbors in local)
            forming |= set(range(offset, offset + 12))
            first |= {offset + vertex for vertex in
                      (1, 3, 5, 6, 7, 8, 9, 10, 11, 12, 14, 16)}
            second |= {offset + vertex for vertex in (1, 3, 5, 6, 7, 8, 9, 10, 11)}
            for color in range(2):
                highs[color].extend(offset + vertex for vertex in range(color, 6, 2))
                leaves[color].extend(offset + 6 + vertex for vertex in range(color, 6, 2))
                hubs[color].append(offset + 18 + color)
                interfaces[color].extend(offset + vertex for vertex in range(12 + color, 18, 2))
        if mode != 'fixed_six_cycles':
            high_set = set(highs[0] + highs[1])
            hub_set = set(hubs[0] + hubs[1])
            for vertex in high_set:
                adjacency[vertex] -= high_set
            for vertex in leaves[0] + leaves[1]:
                adjacency[vertex] -= hub_set
            for vertex in hub_set:
                adjacency[vertex].clear()
            left = generator.sample(highs[0], len(highs[0]))
            right = generator.sample(highs[1], len(highs[1]))
            if mode == 'one_high_cycle':
                for index in range(len(left)):
                    edge(adjacency, left[index], right[index])
                    edge(adjacency, right[index], left[(index + 1) % len(left)])
            else:
                following = generator.sample(right, len(right))
                while any(first_vertex == second_vertex
                          for first_vertex, second_vertex in zip(right, following)):
                    following = generator.sample(right, len(right))
                for index in range(len(left)):
                    edge(adjacency, left[index], right[index])
                    edge(adjacency, left[index], following[index])
            for color in range(2):
                reordered = generator.sample(leaves[color], len(leaves[color]))
                for index, vertex in enumerate(reordered):
                    edge(adjacency, vertex, hubs[color][index // 3])
        chosen = [generator.sample(vertices * 2, blocks) for vertices in interfaces]
        for index in range(blocks):
            offset = len(adjacency)
            block = base()
            block[0].remove(8)
            block[8].remove(0)
            adjacency.extend({offset + neighbor for neighbor in neighbors} for neighbors in block)
            edge(adjacency, offset, chosen[1][index])
            edge(adjacency, offset + 8, chosen[0][index])
            forming |= {offset + vertex for vertex in SELECTED}
            first |= set(range(offset, offset + 7))
            second |= {offset + vertex for vertex in EIGHT}
        stubs = [[vertex for vertex in vertices for count in range(3 - len(adjacency[vertex]))]
                 for vertices in interfaces]
        try:
            pair_stubs(adjacency, stubs[0], stubs[1], generator)
        except AssertionError:
            continue
        return adjacency, forming, first, second, chosen
    raise AssertionError('No simple completion in finite control')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    generator = random.Random(202610191025)
    records = []
    examples = {}
    totals = Counter()
    for cores in range(1, 6):
        for blocks in range(6 * cores + 1):
            for mode in ('fixed_six_cycles', 'one_high_cycle', 'arbitrary_high_cycles'):
                adjacency, forming, first, second, chosen = instance(cores, blocks, mode, generator)
                order = len(adjacency)
                assert order == 20 * cores + 14 * blocks
                assert all(len(neighbors) == 3 and vertex not in neighbors and
                           all(vertex in adjacency[neighbor] for neighbor in neighbors)
                           for vertex, neighbors in enumerate(adjacency))
                assert bipartition(adjacency) is not None
                assert dissociation(adjacency, first) and dissociation(adjacency, second)
                assert len(first) == 12 * cores + 7 * blocks
                assert len(second) == 9 * cores + 8 * blocks
                assert len(forming) == 12 * cores + 8 * blocks
                selected_certificate(adjacency, forming)
                lower = max(len(first), len(second))
                assert 33 * order <= 62 * lower
                capacity = (3 * order - 5 * lower) // 7
                assert 62 * capacity <= 3 * order
                repeated = sum(count == 2 for side in chosen for count in Counter(side).values())
                record = dict(cores=cores, blocks=blocks, mode=mode, order=order,
                              first_witness=len(first), second_witness=len(second),
                              repeated_core_attachment_vertices=repeated,
                              minimal_forming_witness_size=len(forming),
                              gap_upper_from_general_compensation=capacity,
                              exact_beta_or_SF_optimized=False)
                records.append(record)
                totals['instances'] += 1
                totals['dissociation_witnesses'] += 2
                totals['selected_deletions'] += len(forming)
                totals['instances_with_repeated_attachments'] += bool(repeated)
                if repeated and blocks > 3 * cores and mode not in examples:
                    examples[mode] = dict(**record, adjacency=[sorted(neighbors) for neighbors in adjacency],
                                          first=sorted(first), second=sorted(second), forming=sorted(forming))
    report = dict(status='ALL_CHECKS_PASSED', seed=202610191025, totals=dict(totals),
                  records=records, examples=examples,
                  scope='Finite controls of two explicit dissociation witnesses and literal minimal forming witnesses under shared core attachments, arbitrary bipartite high two-factors and regrouped hub triples. No optimized beta/SF or all-order conclusion is inferred from enumeration; the architecture bound has a separate general proof.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], totals=report['totals'])))


if __name__ == '__main__':
    main()
