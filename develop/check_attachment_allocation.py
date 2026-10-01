#!/usr/bin/env python3
"""Exact half-integral controls for attachment-aware donor allocation."""

import argparse
import hashlib
import itertools
import json
from pathlib import Path


def neighborhoods(windows):
    return [set(window) for window in windows]


def max_flow(windows, demands, capacities):
    source_count = len(windows)
    donor_count = len(capacities)
    sink = 1 + source_count + donor_count
    residual = [dict() for _ in range(sink + 1)]

    def edge(left, right, capacity):
        residual[left][right] = capacity
        residual[right][left] = 0

    for source, donors in enumerate(neighborhoods(windows)):
        edge(0, source + 1, demands[source])
        for donor in donors:
            edge(source + 1, 1 + source_count + donor, sum(demands) + 1)
    for donor, capacity in enumerate(capacities):
        edge(1 + source_count + donor, sink, capacity)

    flow = 0
    while True:
        predecessor = {0: None}
        queue = [0]
        for vertex in queue:
            if sink in predecessor:
                break
            for neighbor, capacity in residual[vertex].items():
                if capacity > 0 and neighbor not in predecessor:
                    predecessor[neighbor] = vertex
                    queue.append(neighbor)
        if sink not in predecessor:
            return flow
        amount = sum(demands)
        vertex = sink
        while vertex:
            parent = predecessor[vertex]
            amount = min(amount, residual[parent][vertex])
            vertex = parent
        vertex = sink
        while vertex:
            parent = predecessor[vertex]
            residual[parent][vertex] -= amount
            residual[vertex][parent] += amount
            vertex = parent
        flow += amount


def deficiency(windows, demands, capacities):
    greatest = 0
    neighbors = neighborhoods(windows)
    for mask in range(1 << len(windows)):
        selected = [i for i in range(len(windows)) if mask & (1 << i)]
        union = set().union(*(neighbors[i] for i in selected))
        shortage = sum(demands[i] for i in selected) - sum(
            capacities[j] for j in union)
        greatest = max(greatest, shortage)
    return greatest


def verify(name, windows, demands, capacities, expected):
    flow = max_flow(windows, demands, capacities)
    shortfall = deficiency(windows, demands, capacities)
    assert shortfall == sum(demands) - flow
    assert shortfall == expected
    return dict(name=name, windows=windows, doubled_demands=demands,
                doubled_capacities=capacities, doubled_flow=flow,
                doubled_shortfall=shortfall,
                allocation_exists=shortfall == 0)


def controls():
    examples = [
        verify('one_band_two_attachments', ((0, 1),), (2,), (2, 0), 0),
        verify('two_bands_separate_donors', ((0,), (1,)), (1, 1), (1, 1), 0),
        verify('two_half_demands_share_one_donor', ((0,), (0,)), (1, 1), (2,), 0),
        verify('shared_donor_reused_without_union_check', ((0,), (0,)),
               (2, 2), (2,), 2),
        verify('nested_windows_with_enough_outer_capacity', ((0, 2), (1,)),
               (2, 2), (2, 2, 2), 0),
    ]
    exhaustive = 0
    for source_count in range(1, 4):
        donor_count = 3
        all_windows = [tuple(index for index in range(donor_count)
                             if mask & (1 << index))
                       for mask in range(1, 1 << donor_count)]
        for windows in itertools.product(all_windows, repeat=source_count):
            for demands in itertools.product((1, 2), repeat=source_count):
                for capacities in itertools.product((0, 1, 2), repeat=donor_count):
                    flow = max_flow(windows, demands, capacities)
                    shortfall = deficiency(windows, demands, capacities)
                    assert flow + shortfall == sum(demands)
                    exhaustive += 1
    return dict(status='ALL_CHECKS_PASSED', exhaustive_models=exhaustive,
                examples=examples,
                scope='Half-integral attachment allocation only; no geometric incidence claim.',
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in ('status', 'exhaustive_models')}))


if __name__ == '__main__':
    main()
