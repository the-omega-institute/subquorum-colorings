"""Controls for exact actual-matching PP-path accounting and a backward connector."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_even_bridge_support_completion import endpoints_of
from check_native_guard_compensation import force_matching
from check_native_transverse_band_cancellation import packet_columns, sharp_family
from check_neutral_pair_donor_saturation import neutral_pair
from check_neutral_portal_strip_compensation import image_map
from check_occupied_strip_matching_flux import matchings
from check_promotion_cores import degree_four_patch, tight_diamond
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(current, bands, totals, boundary=False):
    direct_check(*current)
    selected, endpoints = current[2], endpoints_of(current)
    owner, kinds, counts = {}, {}, Counter()
    for band, columns in enumerate(bands):
        for column, points in enumerate(columns):
            assert len(set(points)) == 2
            assert all(point not in owner for point in points)
            node = band, column
            owner.update({point: node for point in points})
            label = tuple(sorted('T' if point in selected else 'P' if point in endpoints
                                 else 'B' for point in points))
            counts[label] += 1
            if 'P' in label:
                kinds[node] = 'PP' if label == ('P', 'P') else 'TP' if 'T' in label else 'BP'
        if boundary:
            assert not set(columns[0]) & (selected | endpoints)
            assert not set(columns[-1]) <= selected | endpoints
    adjacency, edge_nodes = defaultdict(list), {}
    for index, edge in enumerate(current[3]):
        if not any(point in owner for point in edge):
            continue
        nodes = []
        for point in edge:
            node = owner.get(point)
            if node is None:
                node = 'outside', index
                kinds[node] = 'X'
            nodes.append(node)
        first, second = nodes
        adjacency[first].append((second, index))
        adjacency[second].append((first, index))
        edge_nodes[index] = first, second
    assert set(adjacency) == set(kinds)
    assert all(len(adjacency[node]) == (2 if kind == 'PP' else 1)
               for node, kind in kinds.items())
    remaining, owned_edges, components, path_counts = set(kinds), set(), [], Counter()
    while remaining:
        start = min(remaining, key=repr)
        reached, pending, edges = {start}, [start], set()
        while pending:
            node = pending.pop()
            for other, edge in adjacency[node]:
                edges.add(edge)
                if other not in reached:
                    reached.add(other)
                    pending.append(other)
        remaining -= reached
        assert not edges & owned_edges
        owned_edges |= edges
        terminals = sorted((node for node in reached if kinds[node] != 'PP'), key=repr)
        if terminals:
            assert len(terminals) == 2 and len(edges) == len(reached)-1
            path_kind = tuple(sorted(kinds[node] for node in terminals))
            path_counts[path_kind] += 1
            trace, traversed, node, previous = [], set(), terminals[0], None
            while True:
                trace.append(node)
                following = [(other, edge) for other, edge in adjacency[node] if edge != previous]
                if not following:
                    break
                assert len(following) == 1
                node, previous = following[0]
                assert previous not in traversed
                traversed.add(previous)
            assert node == terminals[1] and set(trace) == reached and traversed == edges
            components.append(dict(kind=list(path_kind), nodes=trace, edges=sorted(edges)))
        else:
            assert all(kinds[node] == 'PP' for node in reached)
            assert len(edges) == len(reached)
            components.append(dict(kind=['cycle'], nodes=sorted(reached), edges=sorted(edges)))
    assert owned_edges == set(edge_nodes)
    alpha, beta = path_counts['TP', 'TP'], path_counts['BP', 'BP']
    gamma = path_counts['BP', 'TP']
    tau, delta = path_counts['TP', 'X'], path_counts['BP', 'X']
    exterior_pairs = path_counts['X', 'X']
    mixed, single = counts['P', 'T'], counts['B', 'P']
    assert mixed == 2*alpha+gamma+tau
    assert single == 2*beta+gamma+delta
    cuts = sum(kind == 'X' for kind in kinds.values())
    assert cuts == 2*exterior_pairs+tau+delta
    balance = counts['B', 'B']-counts['T', 'T']
    cells = set(owner)
    surplus_twice = len(cells)-2*len(selected & cells)-len(endpoints & cells)
    assert surplus_twice == 2*balance+single-mixed
    assert surplus_twice == 2*(balance+beta-alpha)+delta-tau
    boundary_budget = None
    if boundary:
        length = len(bands[0])
        assert all(len(columns) == length for columns in bands)
        sealed = sum(not set(columns[-1]) & (selected | endpoints) for columns in bands)
        boundary_budget = len(bands)+(sealed if length % 2 == 0 else 0)
        assert balance >= boundary_budget
        assert (surplus_twice >= 2*boundary_budget) == (
            2*alpha+tau <= 2*(balance-boundary_budget+beta)+delta)
    totals['models'] += 1
    totals['matching_edges_owned'] += len(owned_edges)
    totals['pp_columns'] += counts['P', 'P']
    for kind, count in path_counts.items():
        totals['paths_'+'_'.join(kind)] += count
    totals['pp_cycles'] += sum(component['kind'] == ['cycle'] for component in components)
    totals['open_packets'] += bool(cuts)
    return dict(alpha=alpha, beta=beta, gamma=gamma, tau=tau, delta=delta,
                exterior_pairs=exterior_pairs, cuts=cuts, balance=balance,
                surplus_twice=surplus_twice, boundary_budget=boundary_budget,
                components=components)


def neutral_controls(totals):
    examples = []
    for width, height in itertools.product(range(6, 43, 2), range(4, 31, 2)):
        current, _, _ = neutral_pair(width, height)
        bands = packet_columns(current[0]//2, current[1])
        record = inspect(current, bands, totals, True)
        assert (record['alpha'], record['beta'], record['gamma'], record['cuts']) == (1, 0, 0, 0)
        paths = [component for component in record['components'] if component['kind'] == ['TP', 'TP']]
        assert len(paths) == 1
        path = paths[0]
        expected = [(4, 5), (3, 5)]
        expected += [(2, column) for column in range(5, width+5)]
        expected += [(band, width+4) for band in range(3, height//2+3)]
        assert path['nodes'] == expected or path['nodes'] == expected[::-1]
        assert len(path['nodes']) == width+height//2+2
        assert len(path['edges']) == width+height//2+1
        cycles = [component for component in record['components'] if component['kind'] == ['cycle']]
        assert len(cycles) == height//2-1
        assert {tuple(component['nodes'][0]) for component in cycles} == {
            (band, width+3) for band in range(3, height//2+2)}
        assert all(len(component['nodes']) == len(component['edges']) == 1 for component in cycles)
        assert len(current[3]) == width+height and len(current[2]) == height+7
        assert record['balance'] == width*height//2+3*width+4*height+42
        assert record['surplus_twice'] == 2*(record['balance']-1)
        left_tip, right_tip = (8, 5), (height+4, width+4)
        assert all(len(set(neighbors(point)) & current[2]) == 2 for point in (left_tip, right_tip))
        start_interval = (height//2+2, width+3)
        end_interval = (4, 6)
        endpoints = endpoints_of(current)
        for band, column in (start_interval, end_interval):
            assert not {(2*band, column), (2*band+1, column)} & (current[2] | endpoints)
        assert start_interval[1] > end_interval[1]
        assert start_interval[1] % 2 != end_interval[1] % 2
        force_matching(current, totals)
        totals['neutral_parameters'] += 1
        alternate_bands = [[((2*band+1, column), (2*band+2, column))
                            for column in range(current[1])]
                           for band in range(height//2+3)]
        alternate = inspect(current, alternate_bands, totals, True)
        assert (alternate['alpha'], alternate['beta'], alternate['gamma'], alternate['cuts']) == (
            0, width-2, 1, 0)
        assert alternate['surplus_twice'] == record['surplus_twice']-2*(width+12)
        assert alternate['balance'] == record['balance']-2*width-11
        alternate_cycles = [component for component in alternate['components']
                            if component['kind'] == ['cycle']]
        assert len(alternate_cycles) == height//2+2
        assert all(len(component['nodes']) == len(component['edges']) == 1
                   for component in alternate_cycles)
        bent = [component for component in alternate['components']
                if len(component['nodes']) > 2]
        assert len(bent) == 1 and bent[0]['kind'] == ['BP', 'BP']
        expected_bent = [(2, width+2)]+[(band, width+3) for band in range(2, height//2+2)]
        assert bent[0]['nodes'] in (expected_bent, expected_bent[::-1])
        assert len(bent[0]['edges']) == height//2
        assert alternate['surplus_twice'] >= 2*alternate['boundary_budget']
        totals['alternate_phase_parameters'] += 1
        if (width, height) in ((6, 4), (12, 8), (42, 30)):
            examples.append(dict(width=width, height=height, **record,
                                 backward_connector=[start_interval, end_interval],
                                 alternate_phase=alternate))
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                image_bands = [[tuple(move(point) for point in column) for column in columns]
                               for columns in bands]
                image_record = inspect((*shape, selected, matching), image_bands, totals, True)
                assert image_record == record
                totals['symmetry_images'] += 1
        if width in (6, 12, 42) and height in (4, 8, 30):
            for first_band, last_band, first_column, last_column in (
                    (3, 5, 4, width+6), (2, 3, 4, width+6),
                    (3, height//2+3, 5, width+4), (2, height//2+3, 6, width+5)):
                cropped = [columns[first_column:last_column] for columns in bands[first_band:last_band]]
                inspect(current, cropped, totals)
                totals['neutral_open_crops'] += 1
    return examples


def short_controls(totals):
    census = []
    for length in range(2, 5):
        checked = 0
        points = [(row, column) for column in range(1, length) for row in range(4)]
        bands = packet_columns(2, length)
        for labels in itertools.product(range(3), repeat=len(points)):
            if all(labels[-4+row] for row in (0, 1)) or all(labels[-4+row] for row in (2, 3)):
                continue
            selected = {point for point, label in zip(points, labels) if label == 1}
            endpoints = {point for point, label in zip(points, labels) if label == 2}
            if any(len(set(neighbors(point)) & (selected | endpoints)) > 1 for point in selected):
                continue
            for matching, exported in matchings(endpoints, False):
                assert not exported
                inspect((4, length, selected, matching), bands, totals, True)
                checked += 1
        census.append(dict(columns=length, matchings=checked))
    return census


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    totals = Counter()
    examples = neutral_controls(totals)
    for pairs, mask in itertools.product(range(1, 81), range(4)):
        current = sharp_family(pairs, mask)
        record = inspect(current, packet_columns(2, current[1]), totals, True)
        assert record['alpha'] == pairs and record['beta'] == record['cuts'] == 0
        assert record['surplus_twice'] == 2*(2+mask.bit_count())
        totals['native_sharp_parameters'] += 1
    fixtures = [degree_four_patch(), tight_diamond()[0],
                (2, 2, set(), [((0, 0), (0, 1)), ((1, 0), (1, 1))]),
                (2, 2, set(), [((0, 0), (1, 0)), ((0, 1), (1, 1))]),
                (2, 2, {(1, 0)}, [((0, 0), (0, 1))]),
                (4, 3, set(), [((0, 1), (1, 1)), ((2, 1), (3, 1))])]
    for current in fixtures:
        inspect(current, packet_columns(current[0]//2, current[1]), totals)
        totals['fixtures'] += 1
    inspect(fixtures[-1], [[((1, column), (2, column)) for column in range(3)]], totals)
    totals['fixtures'] += 1
    inspect((4, 3, set(), [((1, 1), (2, 1))]), packet_columns(1, 3), totals)
    totals['fixtures'] += 1
    census = short_controls(totals)
    assert all(totals['paths_'+'_'.join(kind)] > 0 for kind in (
        ('TP', 'TP'), ('BP', 'BP'), ('BP', 'TP'), ('TP', 'X'), ('BP', 'X'), ('X', 'X')))
    result = dict(status='PASS', controls=dict(totals), short_census=census,
                  neutral_examples=examples,
                  scope='Finite controls for the written all-size exact PP-path ledger, including external stubs, loops and parallel edges; all-parameter neutral backward connector is a rule obstruction, not a target counterexample. General compensation remains open.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status=result['status'], controls=result['controls'], short_census=census)))


if __name__ == '__main__':
    main()
