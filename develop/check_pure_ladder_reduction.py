"""Construct and check the general pure-two-row-component reduction."""

import argparse
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import apply_bundle, neighbors, occupied_degrees
from check_ladder_reduction import ladder_matchings
from check_owned_donors import endpoint_data
from check_pure_ladders import supports
from check_residual_corridors import direct_check, transformed

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def construct(current, width):
    selected = current[2]
    endpoints = {vertex for edge in current[3] for vertex in edge}
    core = {(row, column) for row in (2, 3) for column in range(2, width+2)}
    assert core <= endpoints
    assert all(set(neighbors(vertex)) & (endpoints-core) == set() for vertex in core)
    mates = {endpoint: mate for edge in current[3] for endpoint, mate in (edge, edge[::-1])}
    assert {mates[vertex] for vertex in core} == core
    corner_supports = {vertex: len(set(neighbors(vertex)) & selected)
                       for vertex in core if vertex[1] in (2, width+1)}
    doubled = {vertex for vertex, count in corner_supports.items() if count == 2}
    colors = {sum(vertex) % 2 for vertex in doubled}
    if len(colors) <= 1:
        color = 1-next(iter(colors)) if colors else 0
        promoted = {vertex for vertex in core if sum(vertex) % 2 == color}
        return [(vertex, mates[vertex]) for vertex in sorted(promoted)], 'whole_color'
    left_seed = next(vertex for vertex in doubled if vertex[1] == 2)
    left_color = 1-sum(left_seed) % 2
    right_color = 1-left_color
    blocks = []
    column = 2
    while column < width+2:
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
    for first, last in blocks:
        right_guard = last < width+1 and support(color_row(right_color, last+1), last+1)
        if right_guard:
            continue
        left_guard = first > 2 and support(color_row(left_color, first-1), first-1)
        assert not left_guard
        promoted = {vertex for vertex in core if
                    (vertex[1] < first and sum(vertex) % 2 == left_color)
                    or (vertex[1] > last and sum(vertex) % 2 == right_color)}
        kind = 'vertical_switch'
        if first != last:
            retained_row = color_row(right_color, first)
            promoted_row = 5-retained_row
            choices = [(promoted_row, position) for position in (first, last)
                       if not support(promoted_row, position)]
            assert choices
            promoted.add(choices[0])
            kind = 'horizontal_switch'
        return [(vertex, mates[vertex]) for vertex in sorted(promoted)], kind
    raise AssertionError('The last actual matching block has no right guard.')


def verify(current, width):
    objective = direct_check(*current)
    bundle, kind = construct(current, width)
    assert len(bundle) in (width-1, width)
    changed = apply_bundle(current, bundle)
    assert direct_check(*changed) == objective
    assert len(changed[3]) <= 1 and len(endpoint_data(changed)[0]) <= 2
    assert not endpoint_data(changed)[2]
    return kind, bundle


def random_matching(width, generator):
    column = 0
    matching = []
    while column < width:
        if column == width-1 or generator.randrange(2):
            matching.append(((0, column), (1, column)))
            column += 1
        else:
            matching += [((row, column), (row, column+1)) for row in (0, 1)]
            column += 2
    return matching


def random_supports(width, generator):
    selected = set()
    for row in (1, 4):
        for column in range(2, width+2):
            if (row, column-1) not in selected and generator.randrange(2):
                selected.add((row, column))
    for column in (1, width+2):
        choice = generator.randrange(3)
        if choice:
            selected.add((choice+1, column))
    return selected


def physical(width, selected, matching):
    moved = [tuple((row+2, column+2) for row, column in edge) for edge in matching]
    return 6, 2*((width+4)//2), selected, moved


def sharp_failure():
    selected = {(1, 2), (1, 4), (4, 2), (4, 4), (2, 1), (3, 5)}
    current = physical(3, selected, [((0, column), (1, column)) for column in range(3)])
    direct_check(*current)
    assert min(occupied_degrees(current).values()) == 3
    feasible = full = 0
    for states in itertools.product((0, 1, 2), repeat=3):
        if not any(states):
            continue
        chosen = {edge[state-1] for edge, state in zip(current[3], states) if state}
        deleted = {edge[2-state] for edge, state in zip(current[3], states) if state}
        occupied = (current[2] | {vertex for edge in current[3] for vertex in edge})-deleted
        if all(sum(adjacent in occupied for adjacent in neighbors(vertex)) <= 1 for vertex in chosen):
            feasible += 1
            full += all(states)
    assert feasible and not full
    kind, bundle = verify(current, 3)
    assert len(bundle) == 2
    return dict(shape=current[:2], selected=sorted(selected), matching=current[3],
                occupied_degrees=sorted(occupied_degrees(current).values()),
                nonempty_oriented_bundles=26, feasible_bundles=feasible,
                feasible_full_promotions=full, constructed_kind=kind,
                constructed_bundle=bundle, minimum_remaining_matching_edges=1,
                refuted_rule='Every pure two-row endpoint component can have all its matching edges promoted.',
                square_removal_refuted=False, global_inequality_refuted=False)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-width', type=int, default=8)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = dict(whole_color=0, vertical_switch=0, horizontal_switch=0)
    rows = []
    representatives = {}
    for width in range(2, arguments.max_width+1):
        counts = {key: 0 for key in totals}
        for selected, matching in itertools.product(supports(width, single_terminal=False),
                                                    ladder_matchings(width)):
            current = physical(width, selected, matching)
            kind, bundle = verify(current, width)
            counts[kind] += 1
            if kind not in representatives:
                representatives[kind] = dict(width=width, shape=current[:2], selected=sorted(selected),
                                             matching=current[3], bundle=bundle)
        for key in totals:
            totals[key] += counts[key]
        rows.append(dict(width=width, cases=sum(counts.values()), **counts))
        print(json.dumps(rows[-1]), flush=True)
    generator = random.Random(20261019)
    randomized = symmetry_images = 0
    for width in range(9, 65):
        for _ in range(32):
            selected = random_supports(width, generator)
            current = physical(width, selected, random_matching(width, generator))
            kind, bundle = verify(current, width)
            randomized += 1
            if width in (9, 16, 32, 64):
                for symmetry in itertools.product((False, True), repeat=3):
                    shape, moved_selected, moved_matching = transformed(*current, *symmetry)
                    firsts = transformed(*current[:2], {first for first, _ in bundle}, [], *symmetry)[1]
                    mates = {endpoint: mate for edge in moved_matching for endpoint, mate in (edge, edge[::-1])}
                    changed = apply_bundle((*shape, moved_selected, moved_matching),
                                           [(vertex, mates[vertex]) for vertex in sorted(firsts)])
                    assert len(changed[3]) <= 1 and not endpoint_data(changed)[2]
                    symmetry_images += 1
    report = dict(status='ALL_CHECKS_PASSED', exhaustive_cases=sum(totals.values()),
                  exhaustive_widths=rows, exhaustive_kinds=totals,
                  randomized_cases=randomized, symmetry_images=symmetry_images,
                  representatives=representatives, sharp_one_domino_obstacle=sharp_failure(),
                  scope='Finite checks of the constructive general proof for every pure two-row endpoint component, with no single-terminality or interior-closure hypothesis; general validity rests on block decomposition and a proved blank-switch existence lemma.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items()
                      if key not in ('representatives', 'sharp_one_domino_obstacle')}))


if __name__ == '__main__':
    main()
