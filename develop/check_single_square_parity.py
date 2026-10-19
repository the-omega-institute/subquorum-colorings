"""Physical controls for all central matchings and a neutral misalignment obstacle."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import apply_bundle, neighbors, occupied_degrees
from check_owned_donors import endpoint_data
from check_promotion_cores import all_oriented_bundles, frozen_certificate
from check_residual_corridors import direct_check, graph_record, transformed

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def central_patterns():
    cycle = [(0, 1), (1, 2), (2, 3), (3, 0)]
    return [list(chosen) for count in range(3) for chosen in itertools.combinations(cycle, count)
            if len({corner for edge in chosen for corner in edge}) == 2*count]


def single_square(parameters, central_matching):
    corners = [(0, 0), (0, 1), (1, 1), (1, 0)]
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    outer_sides = [(0, -1), (-1, 0), (0, 1), (1, 0)]
    internal = {corner for edge in central_matching for corner in edge}
    lengths = [2*value+int(index not in internal) for index, value in enumerate(parameters)]
    selected = set()
    matching = [(corners[first], corners[second]) for first, second in central_matching]
    for corner_index, (corner, direction, side, length) in enumerate(zip(corners, directions, outer_sides, lengths)):
        path = [(corner[0]+index*direction[0], corner[1]+index*direction[1])
                for index in range(length+1)]
        for index, endpoint in enumerate(path[1:], 1):
            sign = 1 if index % 2 else -1
            selected.add((endpoint[0]+sign*side[0], endpoint[1]+sign*side[1]))
        selected.add((corner[0]+(length+1)*direction[0], corner[1]+(length+1)*direction[1]))
        paired_path = path[1:] if corner_index in internal else path
        matching.extend(zip(paired_path[::2], paired_path[1::2]))
    offset = 2*((lengths[0]+3)//2)+2, 2*((lengths[3]+3)//2)+2
    rows = 2*((offset[0]+lengths[2]+5)//2)
    columns = 2*((offset[1]+lengths[1]+5)//2)
    move = lambda vertex: (vertex[0]+offset[0], vertex[1]+offset[1])
    return (rows, columns, {move(vertex) for vertex in selected},
            [(move(first), move(second)) for first, second in matching]), lengths


def verify(current, lengths, central_matching):
    odd = sum(length % 2 for length in lengths)
    total = sum(length//2 for length in lengths)
    internal_count = len(central_matching)
    assert odd+2*internal_count == 4
    assert direct_check(*current) == 6+3*total+3*odd//2
    endpoints, adjacency, squares = endpoint_data(current)
    assert len(endpoints) == 4+2*total+odd and len(squares) == 1
    origin = next(iter(squares))
    assert all(coordinate % 2 == 0 for coordinate in origin)
    center = origin[0]//2, origin[1]//2
    corners = [(origin[0]+row, origin[1]+column) for row, column in ((0, 0), (0, 1), (1, 1), (1, 0))]
    central_edges = {frozenset(edge) for edge in current[3] if set(edge) <= set(corners)}
    assert len(central_edges) == internal_count
    outgoing = {corner for edge in current[3] for corner in edge
                if corner in corners and not set(edge) <= set(corners)}
    assert len(outgoing) == odd
    if odd == 2:
        first, second = outgoing
        assert second in neighbors(first)
    pending = [corners[0]]
    visited = set(pending)
    while pending:
        vertex = pending.pop()
        added = adjacency[vertex]-visited
        visited.update(added)
        pending.extend(added)
    assert visited == endpoints
    assert set(occupied_degrees(current).values()) == {3}
    frozen, layers = frozen_certificate(current)
    if odd:
        assert frozen == endpoints
    else:
        assert len(frozen) == total and not frozen & set(corners)
        mates = {endpoint: mate for edge in current[3] for endpoint, mate in (edge, edge[::-1])}
        for color in (0, 1):
            promoted = [corner for corner in corners if sum(corner) % 2 == color]
            changed = apply_bundle(current, [(vertex, mates[vertex]) for vertex in promoted])
            assert not endpoint_data(changed)[2]
            assert len(changed[3]) == len(current[3])-2
    graph, _ = graph_record(*current)
    receiver = {(row//2, column//2) for row, column in endpoints}
    assert len(receiver) == 1+total+odd
    counts = dict(center=0, neutral=0, donor=0)
    charge_twice = 0
    for tile in receiver:
        index = tile[0]*(current[1]//2)+tile[1]
        present = sum((2*tile[0]+row, 2*tile[1]+column) in endpoints
                      for row, column in itertools.product(range(2), repeat=2))
        chosen = graph['t'][index]
        assert graph['s'][index] == 0
        if tile == center:
            assert (chosen, present, graph['h'][index], graph['r'][index], graph['deg'][index]) == (0, 4, internal_count, odd//2, odd)
            counts['center'] += 1
        elif present == 2:
            assert chosen == 1
            counts['neutral'] += 1
        else:
            assert (chosen, present) == (1, 1)
            counts['donor'] += 1
        charge_twice += graph['deg'][index]-2*graph['r'][index]
    assert counts == dict(center=1, neutral=total, donor=odd)
    assert charge_twice == -odd
    assert len(current[2]) == 2*total+odd+4
    assert sum((row//2, column//2) in receiver for row, column in current[2]) == total+odd
    return dict(lengths=lengths, central_internal_edges=internal_count, odd_arms=odd,
                receiver_tiles=len(receiver), charge_twice=charge_twice, frozen_rounds=len(layers))


def neutral_misaligned_family(current):
    move = lambda vertex: (vertex[0]+1, vertex[1]+1)
    shifted = (current[0]+2, current[1]+2, {move(vertex) for vertex in current[2]},
               [(move(first), move(second)) for first, second in current[3]])
    assert direct_check(*shifted) == direct_check(*current)
    endpoints, _, squares = endpoint_data(shifted)
    assert len(squares) == 1
    assert all(coordinate % 2 == 1 for coordinate in next(iter(squares)))
    receiver = {(row//2, column//2) for row, column in endpoints}
    assert len(receiver) == len(current[3])
    assert frozen_certificate(shifted)[0] == endpoints
    assert all((first[0]//2, first[1]//2) == (second[0]//2, second[1]//2)
               for first, second in shifted[3])
    graph, _ = graph_record(*shifted)
    for row, column in receiver:
        index = row*(shifted[1]//2)+column
        assert tuple(graph[key][index] for key in ('t', 'h', 's', 'r', 'deg')) == (1, 1, 0, 0, 0)
    assert sum((row//2, column//2) in receiver for row, column in shifted[2]) == len(receiver)


def neutral_obstacle():
    labels = ['TBTBTTBT', 'BTBTBBTB', 'TBTPBTBT', 'TBBPPPTB',
              'BTPPPBBT', 'TBTBPTBT', 'BTBBTBTB', 'TBTTBTBT']
    selected = {(row, column) for row, line in enumerate(labels)
                for column, label in enumerate(line) if label == 'T'}
    displayed_endpoints = {(row, column) for row, line in enumerate(labels)
                           for column, label in enumerate(line) if label == 'P'}
    matching = [((3, 3), (2, 3)), ((3, 4), (3, 5)), ((4, 4), (5, 4)), ((4, 3), (4, 2))]
    original = 8, 8, selected, matching
    assert {vertex for edge in matching for vertex in edge} == displayed_endpoints
    assert len(selected) == 28
    assert all_oriented_bundles(original) == (80, 0)
    for symmetry in itertools.product((False, True), repeat=3):
        shape, chosen, edges = transformed(*original, *symmetry)
        current = *shape, chosen, edges
        assert direct_check(*current) == 32
        endpoints, _, squares = endpoint_data(current)
        assert len(endpoints) == 8 and squares == {(3, 3)}
        assert frozen_certificate(current)[0] == endpoints
        assert [len(layer) for layer in frozen_certificate(current)[1]] == [4, 4]
        assert set(occupied_degrees(current).values()) == {3}
        graph, _ = graph_record(*current)
        assert all(degree-2*capacity == 0 for degree, capacity in zip(graph['deg'], graph['r']))
        for tile_index in range(16):
            tile = divmod(tile_index, 4)
            present = sum((2*tile[0]+row, 2*tile[1]+column) in endpoints
                          for row, column in itertools.product(range(2), repeat=2))
            if present:
                assert (graph['t'][tile_index], present, graph['h'][tile_index], graph['s'][tile_index]) == (1, 2, 1, 0)
            else:
                assert graph['t'][tile_index] == 2
    return dict(shape=[8, 8], labels=labels, selected=sorted(selected), matching=matching,
                objective=32, all_tile_charges_twice=[0]*16, frozen_layers=[4, 4],
                nonempty_bundles_checked=80, feasible_bundles=0, symmetry_images=8,
                low_occupancy_endpoint_donors=0,
                refuted_rule='Alignment-free strictly negative budget per frozen single-square component; target global inequality holds with equality.')


def two_square_obstacle():
    labels = ['TBTBTB', 'BTPBPT', 'TBPPPB', 'TBPPPB', 'BTPBPT', 'TBTBTB']
    selected = {(row, column) for row, line in enumerate(labels)
                for column, label in enumerate(line) if label == 'T'}
    matching = [((2, 2), (1, 2)), ((2, 4), (1, 4)), ((3, 2), (4, 2)),
                ((3, 4), (4, 4)), ((2, 3), (3, 3))]
    original = 6, 6, selected, matching
    assert all_oriented_bundles(original) == (242, 0)
    for symmetry in itertools.product((False, True), repeat=3):
        shape, chosen, edges = transformed(*original, *symmetry)
        current = *shape, chosen, edges
        assert direct_check(*current) == 17
        endpoints, _, squares = endpoint_data(current)
        assert len(endpoints) == 10 and len(squares) == 2
        assert frozen_certificate(current)[0] == endpoints
        assert [len(layer) for layer in frozen_certificate(current)[1]] == [4, 2, 4]
        assert set(occupied_degrees(current).values()) == {3}
        graph, _ = graph_record(*current)
        charges = [degree-2*capacity for degree, capacity in zip(graph['deg'], graph['r'])]
        assert sorted(charges) == [-1, -1]+[0]*7
        attachment_tiles = [index for index, attached in enumerate(graph['s']) if attached]
        assert len(attachment_tiles) == 1
        index = attachment_tiles[0]
        assert tuple(graph[key][index] for key in ('t', 'h', 's', 'r', 'deg')) == (0, 0, 2, 0, 0)
    return dict(shape=[6, 6], labels=labels, selected=sorted(selected), matching=matching,
                objective=17, total_charge_twice=-2, saturated_attachment_count=2,
                frozen_layers=[4, 2, 4], symmetry_images=8,
                nonempty_bundles_checked=242, feasible_bundles=0,
                refuted_rule='Two-unit payment based solely on freezing and the presence of an aligned P-square, or independent one-unit payments for these two overlapping squares.',
                aligned_square_outward_corners=2,
                uniqueness_relaxation_retaining_four_outward_mates='UNRESOLVED_BY_THIS_FIXTURE')


def corrected_ledger_fixture():
    current = 4, 4, {(0, 2), (1, 1), (2, 3), (3, 2)}, [((1, 2), (2, 2))]
    assert direct_check(*current) == 5
    assert set(occupied_degrees(current).values()) == {3}
    graph, _ = graph_record(*current)
    assert tuple(graph[key][1] for key in ('t', 'h', 's', 'r', 'deg')) == (1, 0, 1, 0, 0)
    assert graph['deg'][1]-2*graph['r'][1] == 0
    return dict(shape=[4, 4], selected=sorted(current[2]), matching=current[3],
                deficient_tile=[0, 1], selected_count=1, endpoints_count=1,
                saturated_attachments=1, adjusted_capacity=0, charge_twice=0,
                unadjusted_capacity=1, incorrect_unadjusted_charge_twice=-2)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    patterns = central_patterns()
    assert len(patterns) == 7
    totals = dict(cases=0, symmetry_images=0, odd_zero=0, odd_two=0, odd_four=0,
                  frozen_cases=0, removable_cases=0, bundles_checked=0, neutral_shift_cases=0)
    examples = []
    parameters = list(itertools.product(range(4), repeat=4))+[(8, 8, 8, 8), (0, 1, 7, 15)]
    for pattern in patterns:
        for values in parameters:
            current, lengths = single_square(values, pattern)
            record = verify(current, lengths, pattern)
            odd = record['odd_arms']
            totals['cases'] += 1
            totals[{0:'odd_zero', 2:'odd_two', 4:'odd_four'}[odd]] += 1
            totals['frozen_cases' if odd else 'removable_cases'] += 1
            if odd == 4:
                neutral_misaligned_family(current)
                totals['neutral_shift_cases'] += 1
            for symmetry in itertools.product((False, True), repeat=3):
                shape, chosen, edges = transformed(*current, *symmetry)
                verify((*shape, chosen, edges), lengths, pattern)
                totals['symmetry_images'] += 1
            if sum(values) <= 1 and odd:
                candidates, feasible = all_oriented_bundles(current)
                assert feasible == 0
                totals['bundles_checked'] += candidates
            if values in ((0, 0, 0, 0), (8, 8, 8, 8)):
                examples.append(record)
    report = dict(status='ALL_CHECKS_PASSED', central_patterns=patterns, **totals,
                  representative_cases=examples, neutral_misalignment_obstacle=neutral_obstacle(),
                  two_square_obstacle=two_square_obstacle(),
                  corrected_ledger_fixture=corrected_ledger_fixture(),
                  scope='Finite controls of general written structural/parity/budget proofs; complete geometry is not Lean formalized and multi-square/source coverage remains open.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key:value for key,value in report.items() if key not in ('representative_cases','neutral_misalignment_obstacle','two_square_obstacle','corrected_ledger_fixture')}))


if __name__ == '__main__':
    main()
