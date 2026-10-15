"""Check the local facts and explicit deletion choices behind the general proof."""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random

from check_starforming_gap import graph, forms, local_condition


PORTS = {0, 5}
VERTICES = set(range(10))


def dominates(adjacency, selected):
    return all(adjacency[vertex] & selected for vertex in VERTICES - selected)


def safe_deletions(adjacency, selected):
    return [deleted for deleted in sorted(selected - PORTS)
            if forms(adjacency, selected - {deleted})
            and all(not (port in selected and adjacency[port] & selected)
                    or adjacency[port] & (selected - {deleted}) for port in PORTS)]


def local_checks():
    adjacency = graph(1)
    closed = [adjacency[vertex] | {vertex} for vertex in range(10)]
    triples = [neighbors for neighbors in closed if len(neighbors) == 3]
    quadruples = [neighbors for neighbors in closed if len(neighbors) == 4]
    assert len(triples) == 2 and triples[0].isdisjoint(triples[1])
    assert len(quadruples) == 4
    assert all(len(first & second) <= 2 for first, second in combinations(quadruples, 2))
    assert all(len(adjacency[first]) + len(adjacency[second]) >= 6
               for first in range(10) for second in adjacency[first])
    records = []
    for mask in range(1024):
        selected = {vertex for vertex in range(10) if mask >> vertex & 1}
        if len(selected) >= 6:
            assert forms(adjacency, selected) == dominates(adjacency, selected)
        if len(selected) < 7 or not dominates(adjacency, selected):
            continue
        candidates = selected - PORTS
        bad_domination = {deleted for deleted in candidates
                          if not dominates(adjacency, selected - {deleted})}
        bad_activity = {deleted for deleted in candidates
                        if any(port in selected and adjacency[port] & selected
                               and not adjacency[port] & (selected - {deleted})
                               for port in PORTS)}
        assert len(bad_domination) <= 2 and len(bad_activity) <= 2
        safe = safe_deletions(adjacency, selected)
        assert safe
        records.append(dict(mask=mask, selected=sorted(selected),
                            safe_deletions=safe, bad_domination=sorted(bad_domination),
                            bad_activity=sorted(bad_activity)))
    return dict(dense_dominating_selections=len(records),
                safe_choice_counts=dict(Counter(len(record['safe_deletions']) for record in records)),
                choices=records)


def extension_checks():
    randomizer = random.Random(20261015)
    adjacency = graph(1)
    checks = 0
    for trial in range(60):
        extended = [set(neighbors) for neighbors in adjacency] + [set() for extra in range(8)]
        for first in range(18):
            for second in range(max(10, first + 1), 18):
                if first < 10 and first not in PORTS:
                    continue
                if randomizer.randrange(3) == 0:
                    extended[first].add(second)
                    extended[second].add(first)
        for mask in range(1024):
            local = {vertex for vertex in range(10) if mask >> vertex & 1}
            if len(local) < 7:
                continue
            selected = local | {vertex for vertex in range(10, 18) if randomizer.randrange(2)}
            if not forms(extended, selected):
                continue
            assert dominates(adjacency, local)
            for deleted in safe_deletions(adjacency, local):
                assert forms(extended, selected - {deleted})
                for outside in set(range(18)) - (selected - {deleted}):
                    assert local_condition(extended, selected - {deleted}, outside)
                checks += 1
    return dict(random_extensions=60, safe_global_deletions_checked=checks,
                outside_graphs_may_be_nonbipartite=True, seed=20261015)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = dict(status='ALL_CHECKS_PASSED', local=local_checks(),
                  extensions=extension_checks(),
                  scope='Finite controls only. The arbitrary-interface upper bound '
                        'and exact composition values have general written proofs.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'],
                          dense_selections=report['local']['dense_dominating_selections'],
                          extensions=report['extensions'])))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; verification uses assertions.')
    main()
