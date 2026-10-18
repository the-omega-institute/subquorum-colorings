"""Discovery-only mixed-cycle controls; no general stability conclusion."""

import argparse
from collections import Counter
import json
from itertools import combinations
from pathlib import Path
import random
import sys

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import csr_matrix

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from check_regular_starforming import selected_certificate, bipartition


def build(copies, generator):
    adjacency = []
    colors = []
    def vertices(count, color):
        start = len(adjacency)
        adjacency.extend(set() for position in range(count))
        colors.extend(color for position in range(count))
        return list(range(start, start + count))
    bad = [vertices(3, color) for color in range(2)]
    high = [vertices(3 * copies, color) for color in range(2)]
    leaves = [vertices(3 * copies, 1 - color) for color in range(2)]
    isolated = [vertices(1, color) for color in range(2)]
    private = [vertices(3 * copies, color) for color in range(2)]
    tight = [vertices(3, 1 - color) for color in range(2)]
    full = [vertices(copies, color) for color in range(2)]
    def edge(first, second):
        assert colors[first] != colors[second] and second not in adjacency[first]
        adjacency[first].add(second)
        adjacency[second].add(first)
    left = bad[0] + high[0]
    right = bad[1] + high[1]
    generator.shuffle(left)
    generator.shuffle(right)
    for position in range(len(left)):
        edge(left[position], right[position])
        edge(right[position], left[(position + 1) % len(left)])
    for color in range(2):
        permutation = list(range(3 * copies))
        generator.shuffle(permutation)
        for position in range(3 * copies):
            edge(high[color][position], leaves[color][position])
            edge(leaves[color][position], private[color][position])
            edge(leaves[color][permutation[position]], full[color][position // 3])
        for position in range(3):
            edge(bad[color][position], tight[color][position])
            edge(tight[color][position], isolated[color][0])
    outside_left = private[0] * 2 + tight[1]
    outside_right = private[1] * 2 + tight[0]
    while True:
        generator.shuffle(outside_right)
        pairs = list(zip(outside_left, outside_right))
        if len(set(pairs)) == len(pairs):
            break
    for first, second in pairs:
        edge(first, second)
    selection = set(sum(bad + high + leaves + isolated, []))
    assert len(adjacency) == 14 + 20 * copies
    assert len(selection) == 8 + 12 * copies
    assert all(len(neighbors) == 3 for neighbors in adjacency)
    assert bipartition(adjacency) is not None
    selected_certificate(adjacency, selection)
    return adjacency, selection


def beta(adjacency):
    triples = sorted({tuple(sorted((center, first, second)))
                      for center, neighbors in enumerate(adjacency)
                      for first, second in combinations(neighbors, 2)})
    matrix = np.zeros((len(triples), len(adjacency)))
    for row, triple in enumerate(triples):
        matrix[row, list(triple)] = 1
    result = milp(-np.ones(len(adjacency)), integrality=np.ones(len(adjacency)),
                  bounds=Bounds(np.zeros(len(adjacency)), np.ones(len(adjacency))),
                  constraints=LinearConstraint(csr_matrix(matrix), -np.inf, 2),
                  options={'time_limit': 20, 'mip_rel_gap': 0})
    if result.status:
        return None
    selected = {vertex for vertex, value in enumerate(result.x) if value > 0.5}
    assert all(len(adjacency[vertex] & selected) <= 1 for vertex in selected)
    return len(selected), sorted(selected)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--trials', type=int, default=100)
    arguments = parser.parse_args()
    generator = random.Random(202610190421)
    records = []
    timed_out = []
    representatives = {}
    stop = False
    for copies in (1, 2, 3):
        for trial in range(arguments.trials):
            adjacency, selected = build(copies, generator)
            solved = beta(adjacency)
            if solved is None:
                timed_out.append(dict(k=copies, trial=trial))
                continue
            value, witness = solved
            record = dict(k=copies, trial=trial, order=len(adjacency), SF=len(selected),
                          beta=value, gap=len(selected) - value,
                          candidate_slack=2 * (value - len(selected) + 1))
            records.append(record)
            representatives.setdefault((copies, value), dict(
                **record, selection=sorted(selected), beta_witness=witness,
                edges=[[vertex, neighbor] for vertex, neighbors in enumerate(adjacency)
                       for neighbor in sorted(neighbors) if vertex < neighbor]))
            if record['candidate_slack'] < 0:
                stop = True
                break
        print(json.dumps(dict(k=copies, completed=len(records))), flush=True)
        if stop:
            break
    counts = Counter((record['k'], record['beta']) for record in records)
    receipt = dict(seed=202610190421, trials_per_size=arguments.trials,
                   scope='Discovery only: mixed selected-degree-two/three cycles and outside degree-one/two rewiring. Literal minimality is checked, and the written regular bound gives exact SF. MILP beta optima are finite checks, not a general proof.',
                   candidate_status='UNPROVED', counterexample_found=stop,
                   completed_instances=len(records), timed_out=timed_out,
                   outcome_counts=[dict(k=copies, beta=value, count=count)
                                   for (copies, value), count in sorted(counts.items())],
                   instances=records, representatives=list(representatives.values()))
    arguments.output.write_text(json.dumps(receipt, indent=2) + '\n')


if __name__ == '__main__':
    main()
