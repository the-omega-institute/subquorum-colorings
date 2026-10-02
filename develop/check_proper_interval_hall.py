#!/usr/bin/env python3
"""Finite controls for the proper-interval Hall reduction."""

import itertools
import json
from pathlib import Path


def donor_union(intervals, subset):
    result = set()
    for index in subset:
        left, right = intervals[index]
        result.update(range(left, right + 1))
    return result


def hall_ok(intervals, capacities, subset):
    return sum(capacities[index] for index in donor_union(intervals, subset)) >= len(subset)


def proper(intervals):
    return all(intervals[i][0] < intervals[i + 1][0]
               and intervals[i][1] < intervals[i + 1][1]
               for i in range(len(intervals) - 1))


def all_subsets(size):
    for cardinality in range(size + 1):
        yield from itertools.combinations(range(size), cardinality)


def zero_capacity_hole_control():
    intervals = ((0, 3), (1, 4), (2, 5))
    capacities = (0, 0.5, 0, 1, 0, 0.5)
    checked = 0
    for subset in all_subsets(len(intervals)):
        full = sum(capacities[index] for index in donor_union(intervals, subset))
        holed = sum(capacities[index] for index in donor_union(intervals, subset)
                    if capacities[index] > 0)
        assert full == holed
        checked += 1
    return checked


def controls():
    capacities = (0, 1, 2)
    checked = 0
    for source_count in range(1, 6):
        for donor_count in range(1, 6):
            all_intervals = [(left, right)
                             for left in range(donor_count)
                             for right in range(left, donor_count)]
            for intervals in itertools.combinations(all_intervals, source_count):
                intervals = tuple(sorted(intervals))
                if not proper(intervals):
                    continue
                for capacity_indices in itertools.product(capacities, repeat=donor_count):
                    capacities_half = tuple(value / 2 for value in capacity_indices)
                    blocks_ok = all(
                        hall_ok(intervals, capacities_half, tuple(range(left, right + 1)))
                        for left in range(source_count)
                        for right in range(left, source_count)
                    )
                    all_ok = all(hall_ok(intervals, capacities_half, subset)
                                 for subset in all_subsets(source_count))
                    assert blocks_ok == all_ok
                    checked += 1

    counterexample = {
        'intervals': [(0, 0), (0, 2), (0, 0)],
        'capacities': [1, 1, 1],
        'violating_subset': [0, 2],
        'violating_capacity': 1,
        'all_consecutive_blocks_pass': True,
        'interpretation': 'Nested windows make block-only Hall checks unsound.'
    }
    assert not proper(counterexample['intervals'])
    assert counterexample['violating_capacity'] < len(counterexample['violating_subset'])
    assert all(hall_ok(counterexample['intervals'], counterexample['capacities'],
                       tuple(range(left, right + 1)))
               for left in range(3) for right in range(left, 3))
    return {'status': 'ALL_CHECKS_PASSED', 'proper_families_checked': checked,
            'zero_capacity_hole_subsets_checked': zero_capacity_hole_control(),
            'nonproper_counterexample': counterexample}


def main():
    report = controls()
    output = Path(__file__).with_name('results') / 'proper-interval-hall-2026-10-02.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({'status': report['status'],
                      'proper_families_checked': report['proper_families_checked'],
                      'zero_capacity_hole_subsets_checked':
                      report['zero_capacity_hole_subsets_checked']}))


if __name__ == '__main__':
    main()
