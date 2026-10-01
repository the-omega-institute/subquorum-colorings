#!/usr/bin/env python3
"""Exact controls for interval containment Hall and allocation deficiency."""

import argparse
import hashlib
import itertools
import json
from collections import deque
from pathlib import Path


def neighborhoods(windows):
    return [set() if window is None else set(range(window[0], window[1] + 1))
            for window in windows]


def subset_deficiency(windows, capacities):
    neighbors = neighborhoods(windows)
    greatest = 0
    for mask in range(1 << len(windows)):
        selected = [index for index in range(len(windows)) if mask & (1 << index)]
        union = set().union(*(neighbors[index] for index in selected))
        greatest = max(greatest, 2 * len(selected) - sum(capacities[index] for index in union))
    return greatest


def interval_deficiency(windows, capacities):
    prefix = [0]
    for capacity in capacities:
        prefix.append(prefix[-1] + capacity)
    best = [0] * (len(capacities) + 1)
    collections = [()] * len(best)
    for end in range(1, len(best)):
        best[end] = best[end - 1]
        collections[end] = collections[end - 1]
        for start in range(end):
            count = sum(window is not None and start <= window[0]
                        and window[1] < end for window in windows)
            candidate = best[start] + 2 * count - prefix[end] + prefix[start]
            if candidate > best[end]:
                best[end] = candidate
                collections[end] = collections[start] + ((start, end - 1),)
    shortage = 2 * windows.count(None) + best[-1]
    intervals = collections[-1]
    selected = [index for index, window in enumerate(windows)
                if window is None or any(start <= window[0] and window[1] <= end
                                         for start, end in intervals)]
    neighbors = neighborhoods(windows)
    union = set().union(*(neighbors[index] for index in selected))
    assert 2 * len(selected) - sum(capacities[index] for index in union) == shortage
    return shortage, intervals, selected


def max_flow(windows, capacities):
    source_count = len(windows)
    donor_count = len(capacities)
    sink = 1 + source_count + donor_count
    residual = [dict() for _ in range(sink + 1)]

    def edge(first, second, capacity):
        residual[first][second] = capacity
        residual[second][first] = 0

    for index, donors in enumerate(neighborhoods(windows)):
        edge(0, index + 1, 2)
        for donor in donors:
            edge(index + 1, 1 + source_count + donor, 2 * source_count + 1)
    for donor, capacity in enumerate(capacities):
        edge(1 + source_count + donor, sink, capacity)
    flow = 0
    while True:
        predecessor = {0: None}
        pending = deque([0])
        while pending and sink not in predecessor:
            vertex = pending.popleft()
            for neighbor, capacity in residual[vertex].items():
                if capacity > 0 and neighbor not in predecessor:
                    predecessor[neighbor] = vertex
                    pending.append(neighbor)
        if sink not in predecessor:
            return flow
        amount = 2 * source_count
        vertex = sink
        while vertex != 0:
            parent = predecessor[vertex]
            amount = min(amount, residual[parent][vertex])
            vertex = parent
        vertex = sink
        while vertex != 0:
            parent = predecessor[vertex]
            residual[parent][vertex] -= amount
            residual[vertex][parent] += amount
            vertex = parent
        flow += amount


def verify(windows, capacities):
    deficiency, intervals, selected = interval_deficiency(windows, capacities)
    assert deficiency == subset_deficiency(windows, capacities)
    flow = max_flow(windows, capacities)
    assert flow + deficiency == 2 * len(windows)
    contained_ok = None not in windows and all(
        2 * sum(start <= window[0] and window[1] <= end for window in windows)
        <= sum(capacities[start:end + 1])
        for start in range(len(capacities))
        for end in range(start, len(capacities))
    )
    assert contained_ok == (deficiency == 0)
    return dict(windows=windows, doubled_capacities=capacities,
                doubled_deficiency=deficiency, doubled_max_flow=flow,
                disjoint_obstruction_intervals=intervals,
                obstruction_sources=selected)


def controls():
    count = 0
    for donor_count in range(1, 5):
        possible = [None] + [(start, end) for start in range(donor_count)
                             for end in range(start, donor_count)]
        for source_count in range(5):
            for windows in itertools.combinations_with_replacement(possible, source_count):
                for capacities in itertools.product((0, 1, 2), repeat=donor_count):
                    verify(windows, capacities)
                    count += 1
    examples = {
        'nested_source_block_obstacle': verify(((0, 0), (0, 2), (0, 0)), (2, 2, 2)),
        'two_separated_shortages': verify(((0, 0), (0, 0), (2, 2), (2, 2)), (2, 4, 2)),
        'empty_windows': verify((None, None, (0, 1)), (2, 2)),
        'fractional_shared_donors': verify(((0, 1), (0, 1)), (1, 3)),
        'closed_child_only': verify(((2, 3),), (2, 0, 0, 0, 0, 2)),
        'closed_child_with_outer_donors': verify(((0, 5),), (2, 0, 0, 0, 0, 2)),
    }
    assert examples['nested_source_block_obstacle']['doubled_deficiency'] == 2
    assert examples['two_separated_shortages']['doubled_deficiency'] == 4
    assert examples['fractional_shared_donors']['doubled_deficiency'] == 0
    assert examples['empty_windows']['doubled_deficiency'] == 4
    assert examples['closed_child_only']['doubled_deficiency'] == 2
    assert examples['closed_child_with_outer_donors']['doubled_deficiency'] == 0
    forest_models = []
    for windows, capacities in (
            (((0, 1), (3, 5), (7, 9)), (1, 1, 0, 1, 1, 1, 0, 1, 1, 1)),
            (((0, 3), (5, 6)), (1, 1, 0, 0, 1, 2, 2)),
            (((1, 2), (4, 7), (9, 9)), (0, 2, 2, 0, 1, 1, 0, 1, 0, 2)),
    ):
        record = verify(windows, capacities)
        assert record['doubled_deficiency'] == 0
        forest_models.append(record)
    hole_subsets = 0
    for capacities in itertools.product((0, 1, 2), repeat=5):
        windows = ((0, 2), (1, 3), (2, 4))
        full = neighborhoods(windows)
        holed = [{donor for donor in neighbors if capacities[donor]} for neighbors in full]
        for mask in range(1 << len(windows)):
            selected = [index for index in range(len(windows)) if mask & (1 << index)]
            full_union = set().union(*(full[index] for index in selected))
            holed_union = set().union(*(holed[index] for index in selected))
            assert sum(capacities[index] for index in full_union) == sum(
                capacities[index] for index in holed_union)
            hole_subsets += 1
    return dict(status='ALL_CHECKS_PASSED', exhaustive_models=count,
                zero_capacity_hole_subsets=hole_subsets, examples=examples,
                laminar_forest_models=forest_models,
                scope='Interval incidence and allocation only; no grid feasibility claim.',
                script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    report = controls()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({key: report[key] for key in
                      ('status', 'exhaustive_models', 'zero_capacity_hole_subsets')}))


if __name__ == '__main__':
    main()
