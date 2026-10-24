"""Check partial PP connectors, actual cycles, and frozen missing-port families."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_even_bridge_support_completion import endpoints_of
from check_native_guard_compensation import force_matching
from check_neutral_pair_donor_saturation import neutral_pair
from check_neutral_portal_strip_compensation import image_map
from check_occupied_strip_matching_flux import matchings
from check_pp_path_terminal_ledger import inspect as inspect_paths
from check_receiver_overlap_and_pp_source_collision import collision_family, forest_intervals
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def whole_bands(current):
    return [[((2*band, column), (2*band+1, column))
             for column in range(current[1])] for band in range(current[0]//2)]


def block(kind, width, height):
    base = collision_family(width, height, 1)
    if kind == 'cycle':
        moves = [lambda point: (point[0], point[1]+height+2),
                 lambda point: (point[0], height+8-point[1])]
        selected = set().union(*({move(point) for point in base[2]} for move in moves))
        matching = [tuple(move(point) for point in edge) for move in moves for edge in base[3]]
    else:
        assert kind in ('collision', 'missing')
        selected = base[2]
        if kind == 'missing':
            selected = selected-{(4, 3), (5, 3), (width+4, 3), (width+5, 3)}
            selected |= {(5, 4), (width+4, 4)}
        selected = {(row, column-2) for row, column in selected}
        matching = [tuple((row, column-2) for row, column in edge) for edge in base[3]]
    return width+12, 2*height+12, selected, matching


def stack(width, height, kinds):
    assert kinds
    selected, matching = set(), []
    for index, kind in enumerate(kinds):
        current = block(kind, width, height)
        move = lambda point: (point[0]+index*(width+12), point[1])
        selected |= {move(point) for point in current[2]}
        matching += [tuple(move(point) for point in edge) for edge in current[3]]
    return len(kinds)*(width+12), 2*height+12, selected, matching


def inspect(current, bands, totals, policy=None):
    record = inspect_paths(current, bands, totals, True)
    assert record['cuts'] == 0
    labels, nodes, owner = forest_intervals(current, bands)
    assert len(nodes) == record['balance']
    paths = [component for component in record['components'] if component['kind'] == ['TP', 'TP']]
    adjacency, connectors, missing, degree_four = defaultdict(list), [], 0, 0
    endpoints = endpoints_of(current)
    cell_owner = {point: (band, column) for band, columns in enumerate(bands)
                  for column, cells in enumerate(columns) for point in cells}
    mate = {first: second for edge in current[3] for first, second in (edge, edge[::-1])}
    used_ports = set()
    for path_index, path in enumerate(paths):
        choices = []
        for band, column in (path['nodes'][0], path['nodes'][-1]):
            assert 0 < column < len(bands[band])-1
            endpoint = next(point for point in bands[band][column] if point in endpoints)
            mate_band, mate_column = cell_owner[mate[endpoint]]
            assert mate_band != band and mate_column == column
            choices.append([(band, neighbor) for neighbor in (column-1, column+1)
                            if 0 <= neighbor < len(bands[band])
                            and labels[band][neighbor] == ('B', 'B')])
            degree = len(set(neighbors(endpoint)) & (current[2] | endpoints))
            assert len(choices[-1])+degree == 4
            degree_four += degree == 4
            mate_degree = len(set(neighbors(mate[endpoint])) & (current[2] | endpoints))
            if degree == 4 and mate_degree >= 3:
                adjacent_bp = [neighbor for neighbor in (column-1, column+1)
                               if labels[band][neighbor] == ('B', 'P')]
                assert adjacent_bp
                totals['missing_terminals_with_adjacent_bp'] += 1
        if not all(choices):
            missing += 1
            continue
        selection = policy(path_index, choices) if policy else (choices[0][0], choices[1][0])
        if selection is None:
            continue
        ports = []
        for options, port in zip(choices, selection):
            assert port in options
            band, column = port
            interval = nodes[owner[port]]
            terminal = path['nodes'][0] if options is choices[0] else path['nodes'][-1]
            side = 'left' if column > terminal[1] else 'right'
            assert column == interval['first' if side == 'left' else 'last']
            assert (owner[port], side) not in used_ports
            used_ports.add((owner[port], side))
            ports.append(owner[port])
        first, second = ports
        edge_index = len(connectors)
        adjacency[first].append((second, edge_index))
        adjacency[second].append((first, edge_index))
        connectors.append(ports)
    assert all(len(adjacency[index]) <= 2 for index in range(len(nodes)))
    residual = len(paths)-len(connectors)
    assert missing <= degree_four <= 2*missing
    boundary = {owner[band, 0] for band in range(len(bands))}
    if len(bands[0]) % 2 == 0:
        last = {owner[band, len(columns)-1] for band, columns in enumerate(bands)
                if labels[band][-1] == ('B', 'B')}
        assert not boundary & last
        boundary |= last
    assert len(boundary) == record['boundary_budget']
    assert all(len(adjacency[index]) <= 1 for index in boundary)
    remaining, classes, components = set(range(len(nodes))), Counter(), []
    while remaining:
        start = min(remaining)
        reached, pending, edges = {start}, [start], set()
        while pending:
            node = pending.pop()
            for other, edge in adjacency[node]:
                edges.add(edge)
                if other not in reached:
                    reached.add(other)
                    pending.append(other)
        remaining -= reached
        marks = len(reached & boundary)
        if len(edges) == len(reached):
            assert marks == 0 and all(len(adjacency[node]) == 2 for node in reached)
            classes['cycles'] += 1
            kind = 'cycle'
        else:
            assert len(edges)+1 == len(reached) and marks <= 2
            classes['h'+str(marks)] += 1
            kind = 'h'+str(marks)
        if edges:
            components.append(dict(kind=kind, vertices=sorted(reached), edges=sorted(edges)))
    path_count = sum(classes['h'+str(marks)] for marks in range(3))
    assert len(nodes)-len(connectors) == path_count
    assert record['boundary_budget'] == classes['h1']+2*classes['h2']
    margin = classes['h0']+record['beta']-classes['h2']-residual
    assert record['surplus_twice'] == 2*(path_count+record['beta']-residual)
    assert record['surplus_twice']-2*record['boundary_budget'] == 2*margin
    assert (margin >= 0) == (classes['h2']+residual <= classes['h0']+record['beta'])
    assert classes['h0']+classes['cycles']+record['beta']-classes['h2']-residual-classes['cycles'] == margin
    totals['connector_models'] += 1
    totals['actual_connector_cycles'] += classes['cycles']
    totals['actual_missing_port_paths'] += missing
    totals['degree_four_alpha_terminals'] += degree_four
    totals['boundary_collision_paths'] += classes['h2']
    totals['omitted_attachable_paths'] += residual-missing
    return dict(alpha=record['alpha'], beta=record['beta'], gamma=record['gamma'],
                pp_cycles=sum(component['kind'] == ['cycle'] for component in record['components']),
                intervals=len(nodes), connector_edges=len(connectors), residual=residual,
                missing_port_paths=missing, **{key: classes[key] for key in ('h0', 'h1', 'h2', 'cycles')},
                degree_four_alpha_terminals=degree_four,
                boundary=record['boundary_budget'], surplus_twice=record['surplus_twice'],
                margin_twice=2*margin, nontrivial_components=components)


def family_control(width, height, kinds, totals):
    current = stack(width, height, kinds)
    direct_check(*current)
    force_matching(current, totals)
    record = inspect(current, whole_bands(current), totals)
    counts = Counter(kinds)
    cycles, collisions, missing = (counts[kind] for kind in ('cycle', 'collision', 'missing'))
    base_surplus = width*height+5*width+10*height+61
    surplus = cycles*(width*height+4*width+8*height+54)
    surplus += collisions*base_surplus+missing*(base_surplus+2)
    assert len(current[2]) == cycles*(2*height+18)+collisions*(height+11)+missing*(height+9)
    assert len(current[3]) == (2*cycles+collisions+missing)*(width+height)
    assert record['alpha'] == 2*cycles+collisions+missing and record['beta'] == 0
    assert record['gamma'] == (2*cycles+collisions+missing)*(height+1)
    assert record['pp_cycles'] == (2*cycles+collisions+missing)*(width//2-1)
    assert record['cycles'] == cycles and record['h2'] == collisions
    assert record['residual'] == record['missing_port_paths'] == missing
    assert record['boundary'] == len(kinds)*(width+12)
    assert record['surplus_twice'] == 2*surplus
    assert record['h0'] == surplus-record['boundary']+collisions+missing
    assert record['margin_twice'] > 0
    for component in record['nontrivial_components']:
        assert len(component['vertices']) == 2
        assert len(component['edges']) == (2 if component['kind'] == 'cycle' else 1)
    endpoints = endpoints_of(current)
    for index, kind in enumerate(kinds):
        if kind != 'missing':
            continue
        offset = index*(width+12)
        for row in (5, width+4):
            new_selection = offset+row, 2
            assert set(neighbors(new_selection)) & (current[2] | endpoints) == {(offset+row, 3)}
    totals['family_packets'] += 1
    return current, record


def short_controls(totals):
    for length in range(2, 5):
        points = [(row, column) for column in range(1, length) for row in range(4)]
        bands = [[((2*band, column), (2*band+1, column))
                  for column in range(length)] for band in range(2)]
        for labels in itertools.product(range(3), repeat=len(points)):
            if all(labels[-4+row] for row in (0, 1)) or all(labels[-4+row] for row in (2, 3)):
                continue
            selected = {point for point, label in zip(points, labels) if label == 1}
            endpoints = {point for point, label in zip(points, labels) if label == 2}
            if any(len(set(neighbors(point)) & (selected | endpoints)) > 1 for point in selected):
                continue
            for matching, exported in matchings(endpoints, False):
                assert not exported
                inspect((4, length, selected, matching), bands, totals)
                totals['short_matching_models'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, references = Counter(), []
    for width, height, kind in itertools.product(range(6, 25, 2), range(4, 19, 2),
                                                 ('cycle', 'collision', 'missing')):
        current, record = family_control(width, height, [kind], totals)
        totals['parameter_triples'] += 1
        if width == 6 and height == 4:
            references.append(dict(kind=kind, shape=current[:2], selected=sorted(current[2]),
                                   matching=current[3], **record))
            bands = whole_bands(current)
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                image_bands = [[tuple(move(point) for point in column) for column in columns]
                               for columns in bands]
                image_record = inspect((*shape, selected, matching), image_bands, totals)
                assert image_record == record
                totals['symmetry_images'] += 1
    for copies in range(1, 41):
        family_control(6, 4, ['cycle']*copies, totals)
        family_control(6, 4, ['missing']*copies, totals)
        totals['unbounded_multiplicity_controls'] += 2
    for cycles, collisions, missing in itertools.product(range(4), repeat=3):
        if not cycles+collisions+missing:
            continue
        kinds = ['cycle']*cycles+['collision']*collisions+['missing']*missing
        current, _ = family_control(6, 4, kinds, totals)
        inspect(current, whole_bands(current), totals, lambda index, choices: None)
        inspect(current, whole_bands(current), totals,
                lambda index, choices: None if index % 2 else (choices[0][-1], choices[1][-1]))
        totals['mixed_inventory_controls'] += 1
    current, _, _ = neutral_pair(6, 4)
    bands = whole_bands(current)
    for first, second in itertools.product(range(2), repeat=2):
        inspect(current, bands, totals,
                lambda index, choices: (choices[0][first % len(choices[0])],
                                        choices[1][second % len(choices[1])]))
        totals['alternative_port_controls'] += 1
    short_controls(totals)
    report = dict(status='PASS', controls=dict(totals), references=references,
                  scope='Uniform written partial-connector identity and all-parameter frozen cycle/'
                        'missing-port constructions; finite discovery/controls are not general proofs. '
                        'Grid-to-multigraph, degree and coordinate adapters remain written.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', controls=dict(totals))))


if __name__ == '__main__':
    main()
