"""Discover and check terminal endpoint shapes contained in two consecutive rows."""

import argparse
import itertools
import json
from pathlib import Path

from check_component_receivers import endpoint_components, verify_terminal
from check_cooperative_promotion import apply_bundle, neighbors
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def connected(endpoints):
    reached = {min(endpoints)}
    pending = list(reached)
    while pending:
        added = set(neighbors(pending.pop())) & (endpoints-reached)
        reached.update(added)
        pending.extend(added)
    return reached == endpoints


def matchings(endpoints):
    if not endpoints:
        yield []
        return
    first = min(endpoints)
    for second in sorted(set(neighbors(first)) & endpoints):
        for rest in matchings(endpoints-{first, second}):
            yield [(first, second)]+rest


def support_sets(endpoints):
    exterior = set().union(*(set(neighbors(vertex)) for vertex in endpoints))-endpoints
    possible = {vertex for vertex in exterior if len(set(neighbors(vertex)) & endpoints) == 1}
    options = []
    for vertex in sorted(endpoints):
        internal = len(set(neighbors(vertex)) & endpoints)
        candidates = sorted(set(neighbors(vertex)) & possible)
        need = max(0, 3-internal)
        if len(candidates) < need:
            return
        choices = [frozenset(chosen) for size in range(need, len(candidates)+1)
                   for chosen in itertools.combinations(candidates, size)]
        options.append(choices)
    options.sort(key=lambda choices: len(choices))

    def extend(index, chosen, forbidden):
        if index == len(options):
            yield chosen
            return
        for following in options[index]:
            if following & forbidden:
                continue
            prohibited = set().union(*(set(neighbors(vertex)) for vertex in following)) if following else set()
            yield from extend(index+1, chosen | following, forbidden | prohibited)

    yield from extend(0, set(), set())


def chambers(endpoints):
    full = sorted(column for column in {column for _, column in endpoints}
                  if {(0, column), (1, column)} <= endpoints)
    result = []
    for column in full:
        if result and result[-1][-1]+1 == column:
            result[-1].append(column)
        else:
            result.append([column])
    return result


def chamber_bundle(current, first, width):
    selected = current[2]
    endpoints = {vertex for edge in current[3] for vertex in edge}
    core = {(row, column) for row in (2, 3) for column in range(first, first+width)}
    mates = {endpoint: mate for edge in current[3] for endpoint, mate in (edge, edge[::-1])}
    assert core <= endpoints and {mates[vertex] for vertex in core} == core
    occupied = selected | endpoints
    doubled = {vertex for vertex in core if len(set(neighbors(vertex)) & (occupied-core)) == 2}
    colors = {sum(vertex) % 2 for vertex in doubled}
    if len(colors) <= 1:
        color = 1-next(iter(colors)) if colors else 0
        promoted = {vertex for vertex in core if sum(vertex) % 2 == color}
    else:
        left_seed = next(vertex for vertex in doubled if vertex[1] == first)
        left_color = 1-sum(left_seed) % 2
        right_color = 1-left_color
        blocks = []
        column = first
        while column < first+width:
            if mates[2, column] == (3, column):
                blocks.append((column, column))
                column += 1
            else:
                assert mates[2, column] == (2, column+1)
                assert mates[3, column] == (3, column+1)
                blocks.append((column, column+1))
                column += 2
        color_row = lambda color, column: 2 if (2+column) % 2 == color else 3
        support = lambda row, column: (1 if row == 2 else 4, column) in selected
        for left, right in blocks:
            right_guard = right < first+width-1 and support(color_row(right_color, right+1), right+1)
            if right_guard:
                continue
            left_guard = left > first and support(color_row(left_color, left-1), left-1)
            assert not left_guard
            promoted = {vertex for vertex in core if
                        (vertex[1] < left and sum(vertex) % 2 == left_color) or
                        (vertex[1] > right and sum(vertex) % 2 == right_color)}
            if left != right:
                retained_row = color_row(right_color, left)
                promoted_row = 5-retained_row
                choices = [(promoted_row, position) for position in (left, right)
                           if not support(promoted_row, position)]
                assert choices
                promoted.add(choices[0])
            break
        else:
            raise AssertionError('No blank switch block.')
    bundle = [(vertex, mates[vertex]) for vertex in sorted(promoted)]
    assert len(bundle) in (width-1, width)
    changed = apply_bundle(current, bundle)
    assert direct_check(*changed) == direct_check(*current)
    assert len({vertex for edge in changed[3] for vertex in edge} & core) <= 2
    return bundle


def classify(endpoints, selected, matching):
    if len({row for row, _ in endpoints}) == 1 or len({column for _, column in endpoints}) == 1:
        return dict(kind='comb')
    runs = chambers(endpoints)
    assert len(runs) == 1
    run = runs[0]
    width = len(run)
    assert width >= 3
    left = {vertex for vertex in endpoints if vertex[1] < run[0]}
    right = {vertex for vertex in endpoints if vertex[1] > run[-1]}
    assert len(left) % 2 == len(right) % 2 == 1
    left_row = next(iter(left))[0]
    right_row = next(iter(right))[0]
    assert right_row == (left_row+width) % 2
    assert all(row == left_row for row, _ in left)
    assert all(row == right_row for row, _ in right)
    assert all(first[0] == second[0] for first, second in matching)
    return dict(kind='capped', width=width, left_tail=len(left), right_tail=len(right),
                left_row=left_row, selected=len(selected))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, default=7)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    examples = {}
    total = closed_checks = 0
    for span in range(1, arguments.max_width+1):
        shapes = supports = cases = frozen_cases = combs = caps = 0
        for columns in itertools.product((1, 2, 3), repeat=span):
            endpoints = {(row, column) for column, mask in enumerate(columns)
                         for row in (0, 1) if mask >> row & 1}
            if len(endpoints) % 2 or not connected(endpoints):
                continue
            actual_matchings = list(matchings(endpoints))
            if not actual_matchings:
                continue
            shapes += 1
            for selected in support_sets(endpoints):
                supports += 1
                if len(endpoints) > 2:
                    assert all(len(run) >= 2 for run in chambers(endpoints))
                move = lambda vertex: (vertex[0]+2, vertex[1]+2)
                chosen = {move(vertex) for vertex in selected}
                for matching in actual_matchings:
                    current = 6, 2*((span+5)//2), chosen, [tuple(move(vertex) for vertex in edge)
                                                         for edge in matching]
                    direct_check(*current)
                    for run in chambers(endpoints):
                        if len(run) < 2:
                            continue
                        core = {(row, column) for row in (0, 1) for column in run}
                        if all((first in core) == (second in core) for first, second in matching):
                            chamber_bundle(current, run[0]+2, len(run))
                            closed_checks += 1
                    frozen = frozen_certificate(current)[0]
                    cases += 1
                    if len(frozen) != len(endpoints):
                        continue
                    result = classify(endpoints, selected, matching)
                    verify_terminal(current)
                    frozen_cases += 1
                    combs += result['kind'] == 'comb'
                    caps += result['kind'] == 'capped'
                    key = result['kind']
                    if key not in examples:
                        examples[key] = dict(shape=current[:2], selected=sorted(chosen), matching=current[3],
                                             classification=result)
        record = dict(span=span, matched_shapes=shapes, support_patterns=supports,
                      single_terminal_configurations=cases, bundle_terminal_configurations=frozen_cases,
                      combs=combs, capped=caps)
        records.append(record)
        total += cases
        print(json.dumps(record), flush=True)
    report = dict(status='ALL_CHECKS_PASSED', spans=records, single_terminal_configurations=total,
                  closed_chamber_bundle_checks=closed_checks, examples=examples,
                  scope='Finite discovery and controls for two-row terminal classification and matching-closed chamber promotion. General proofs required independently.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')


if __name__ == '__main__':
    main()
