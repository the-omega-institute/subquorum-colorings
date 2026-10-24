"""Independent physical controls for the four-guard two-row reduction."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import apply_bundle, occupied_degrees
from check_owned_donors import check_structure, endpoint_data
from check_promotion_cores import normalize
from check_residual_corridors import direct_check, graph_record, transformed
from check_single_square_parity import two_square_obstacle

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def ladder_matchings(width):
    vertices = {(row, column) for row in range(2) for column in range(width)}

    def complete(remaining):
        if not remaining:
            yield []
            return
        first = min(remaining)
        for second in sorted(remaining-{first}):
            if abs(first[0]-second[0])+abs(first[1]-second[1]) == 1:
                for rest in complete(remaining-{first, second}):
                    yield [(first, second)]+rest

    return list(complete(vertices))


def straight_arm_ladder(width, parameters, interior_matching):
    corners = [(0, 0), (0, width-1), (1, 0), (1, width-1)]
    directions = [(-1, 0), (-1, 0), (1, 0), (1, 0)]
    outward = [-1, 1, -1, 1]
    lengths = [2*value+1 for value in parameters]
    selected = set()
    matching = [((first[0], first[1]+1), (second[0], second[1]+1))
                for first, second in interior_matching]
    for corner, direction, side, length in zip(corners, directions, outward, lengths):
        path = [(corner[0]+index*direction[0], corner[1]) for index in range(length+1)]
        for index, endpoint in enumerate(path[1:], 1):
            selected.add((endpoint[0], endpoint[1]+side*(1 if index % 2 else -1)))
        selected.add((corner[0]+(length+1)*direction[0], corner[1]))
        matching.extend(zip(path[::2], path[1::2]))
    north, south = max(lengths[:2]), max(lengths[2:])
    offset = north+3, 2
    move = lambda vertex: (vertex[0]+offset[0], vertex[1]+offset[1])
    rows, columns = north+south+8, 2*((width+5)//2)
    current = (rows, columns, {move(vertex) for vertex in selected},
               [(move(first), move(second)) for first, second in matching])
    interior = {move((row, column)) for row in range(2) for column in range(1, width-1)}
    core = {move((row, column)) for row in range(2) for column in range(width)}
    guards = {move((row, column)) for row in (-1, 2) for column in (1, width-2)}
    return current, interior, core, guards


def verify(current, interior, core, guards, width):
    objective = direct_check(*current)
    endpoints, _, squares = endpoint_data(current)
    assert core <= endpoints and len(squares) == width-1
    assert set(occupied_degrees(current).values()) == {3}
    assert not guards & (current[2] | endpoints)
    mates = {endpoint: mate for edge in current[3] for endpoint, mate in (edge, edge[::-1])}
    assert {mates[vertex] for vertex in interior} == interior
    for color in (0, 1):
        promoted = {vertex for vertex in interior if sum(vertex) % 2 == color}
        assert len(promoted) == width-2
        changed = apply_bundle(current, [(vertex, mates[vertex]) for vertex in sorted(promoted)])
        assert direct_check(*changed) == objective
        assert len(changed[2])-len(current[2]) == len(current[3])-len(changed[3]) == width-2
        after_endpoints, _, after_squares = endpoint_data(changed)
        assert not after_endpoints & interior and not after_squares
    return objective


def guard_failure():
    selected = {(1, 3)}
    matching = [((2, column), (3, column)) for column in range(2, 6)]
    current = 6, 8, selected, matching
    assert direct_check(*current) == 5
    interior = {(row, column) for row in (2, 3) for column in (3, 4)}
    mates = {endpoint: mate for edge in matching for endpoint, mate in (edge, edge[::-1])}
    good = []
    for color in (0, 1):
        bundle = [(vertex, mates[vertex]) for vertex in sorted(interior) if sum(vertex) % 2 == color]
        deleted_edges = {frozenset(edge) for edge in bundle}
        changed = (*current[:2], selected | {vertex for vertex, _ in bundle},
                   [edge for edge in matching if frozenset(edge) not in deleted_edges])
        try:
            direct_check(*changed)
        except AssertionError:
            good.append(False)
        else:
            good.append(True)
    assert good == [True, False]
    return dict(shape=[6, 8], selected=sorted(selected), matching=matching,
                feasible_central_colors=good, terminality_claimed=False,
                failure='The top-left interior vertex keeps its left end-column P and occupied north guard; the other color bundle is feasible.')


def guard_masks():
    totals = dict(feasible_masks=0, infeasible_masks=0, color_checks=0,
                  both_canonical_colors_blocked=0, terminality_claimed=False)
    for width in range(4, 13):
        matching = [((2, column), (3, column)) for column in range(2, width+2)]
        interior = {(row, column) for row in (2, 3) for column in range(3, width+1)}
        guards = [(row, column) for row in (1, 4) for column in (3, width)]
        mates = {endpoint: mate for edge in matching for endpoint, mate in (edge, edge[::-1])}
        for mask in range(16):
            selected = {vertex for index, vertex in enumerate(guards) if mask & (1 << index)}
            current = 6, 2*((width+5)//2), selected, matching
            try:
                direct_check(*current)
            except AssertionError:
                totals['infeasible_masks'] += 1
                continue
            totals['feasible_masks'] += 1
            feasible = []
            for color in (0, 1):
                promoted = {vertex for vertex in interior if sum(vertex) % 2 == color}
                removed = {frozenset((vertex, mates[vertex])) for vertex in promoted}
                changed = (*current[:2], selected | promoted,
                           [edge for edge in matching if frozenset(edge) not in removed])
                try:
                    direct_check(*changed)
                except AssertionError:
                    actual = False
                else:
                    actual = True
                expected = not any(sum(guard) % 2 != color for guard in selected)
                assert actual == expected
                feasible.append(actual)
                totals['color_checks'] += 1
            if not any(feasible):
                assert {sum(guard) % 2 for guard in selected} == {0, 1}
                totals['both_canonical_colors_blocked'] += 1
    return totals


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    rows = []
    totals = dict(feasible_cases=0, infeasible_arm_placements=0, symmetry_images=0,
                  checked_color_bundles=0, squarefree_normalizations=0)
    parameters = list(itertools.product(range(2), repeat=4))+[(8, 0, 1, 3), (0, 8, 3, 1)]
    for width in range(4, 13):
        matchings = ladder_matchings(width-2)
        feasible = rejected = 0
        for matching, values in itertools.product(matchings, parameters):
            current, interior, core, guards = straight_arm_ladder(width, values, matching)
            try:
                direct_check(*current)
            except AssertionError:
                rejected += 1
                totals['infeasible_arm_placements'] += 1
                continue
            objective = verify(current, interior, core, guards, width)
            totals['feasible_cases'] += 1
            feasible += 1
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, edges = transformed(*current, *symmetry)
                moved_interior = transformed(*current[:2], interior, [], *symmetry)[1]
                moved_core = transformed(*current[:2], core, [], *symmetry)[1]
                moved_guards = transformed(*current[:2], guards, [], *symmetry)[1]
                assert verify((*shape, selected, edges), moved_interior, moved_core, moved_guards, width) == objective
                totals['symmetry_images'] += 1
                totals['checked_color_bundles'] += 2
            if values == (0, 0, 0, 0):
                ending, _ = normalize(current)
                assert not endpoint_data(ending)[2]
                assert check_structure(ending) is not None
                assert direct_check(*ending) == objective
                totals['squarefree_normalizations'] += 1
        rows.append(dict(width=width, interior_perfect_matchings=len(matchings),
                         feasible_arm_cases=feasible, infeasible_arm_cases=rejected))
    report = dict(status='ALL_CHECKS_PASSED', **totals, widths=rows,
                  occupied_guard=guard_failure(), colorwise_guard_masks=guard_masks(),
                  sharp_width_three=two_square_obstacle(),
                  scope='Finite physical controls for the general written exact colorwise guard criterion; arbitrary matching closure and exterior geometry are proved in the note, not inferred from enumeration.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in ('occupied_guard','sharp_width_three')}))


if __name__ == '__main__':
    main()
