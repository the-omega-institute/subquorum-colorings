"""Explore promotion and guard ownership in pure two-row endpoint components."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_ladder_reduction import ladder_matchings
from check_promotion_cores import color_data, frozen_certificate, normalize, peel
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def independent_words(width):
    return [mask for mask in range(1 << width) if not mask & (mask << 1)]


def supports(width, single_terminal=True):
    words = independent_words(width)
    for top, bottom, left, right in itertools.product(words, words, range(3), range(3)):
        selected = {(1, column+2) for column in range(width) if top >> column & 1}
        selected |= {(4, column+2) for column in range(width) if bottom >> column & 1}
        if left:
            selected.add((left+1, 1))
        if right:
            selected.add((right+1, width+2))
        core = {(row, column) for row in (2, 3) for column in range(2, width+2)}
        if not single_terminal or all(
                sum(adjacent in selected | core for adjacent in neighbors(vertex)) >= 3
                for vertex in core):
            yield selected


def square_count(endpoints, width):
    return sum({(row, column) for row in (2, 3) for column in (left, left+1)} <= endpoints
               for left in range(2, width+1))


def check(width, selected, matching):
    edges = [tuple((row+2, column+2) for row, column in edge) for edge in matching]
    current = 6, 2*((width+4)//2), selected, edges
    direct_check(*current)
    endpoints = {vertex for edge in edges for vertex in edge}
    results = []
    for color in (0, 1):
        candidates, adjacency, needs = color_data(current, color)
        promoted, _ = peel(adjacency, needs)
        deleted = promoted | {candidates[vertex] for vertex in promoted}
        results.append(dict(color=color, bundle_size=len(promoted),
                            remaining_squares=square_count(endpoints-deleted, width)))
    return current, results


def exact_obstacle(current, width):
    endpoints = {vertex for edge in current[3] for vertex in edge}
    feasible = removing = examined = 0
    for states in itertools.product((0, 1, 2), repeat=len(current[3])):
        if not any(states):
            continue
        promoted = set()
        removed = set()
        for state, edge in zip(states, current[3]):
            if state:
                promoted.add(edge[state-1])
                removed.add(edge[2-state])
        occupied = (current[2] | endpoints)-removed
        valid = all(sum(adjacent in occupied for adjacent in neighbors(vertex)) <= 1
                    for vertex in promoted)
        examined += 1
        if valid:
            feasible += 1
            removing += square_count(endpoints-promoted-removed, width) == 0
    frozen, layers = frozen_certificate(current)
    return dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
                bundles_examined=examined, feasible_bundles=feasible,
                square_removing_bundles=removing, frozen_endpoints=len(frozen),
                frozen_layers=layers)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, default=6)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = []
    obstacle = None
    for width in range(2, arguments.max_width+1):
        cases = closed = remaining = failed_normalizations = 0
        for selected, matching in itertools.product(supports(width), ladder_matchings(width)):
            current, results = check(width, selected, matching)
            cases += 1
            closed += all(record['bundle_size'] == 0 for record in results)
            if all(record['remaining_squares'] for record in results):
                remaining += 1
                ending, _ = normalize(current)
                if square_count({vertex for edge in ending[3] for vertex in edge}, width):
                    failed_normalizations += 1
                    print(json.dumps(dict(normalization_obstacle=exact_obstacle(current, width))), flush=True)
                if obstacle is None:
                    obstacle = dict(width=width, color_cores=results,
                                    certificate=exact_obstacle(current, width))
                    print(json.dumps(dict(first_single_color_obstacle=obstacle)), flush=True)
        row = dict(width=width, cases=cases, both_color_cores_empty=closed,
                   neither_color_core_removes_all_squares=remaining,
                   failed_normalizations=failed_normalizations)
        totals.append(row)
        print(json.dumps(row), flush=True)
    report = dict(status='EXPLORATION_COMPLETED', widths=totals,
                  first_single_color_obstacle=obstacle,
                  general_target_refuted=False,
                  scope='Finite discovery controls only. A single-color obstacle has a successful mixed-color bundle; no general theorem follows from this enumeration.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
