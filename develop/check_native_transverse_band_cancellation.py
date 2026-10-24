"""Controls for all-length native transverse cancellation across occupied bands."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import neighbors
from check_even_bridge_support_completion import endpoints_of, tiles_of
from check_native_guard_compensation import force_matching
from check_neutral_pair_donor_saturation import neutral_pair
from check_neutral_portal_strip_compensation import image_map
from check_occupied_strip_matching_flux import inspect as inspect_strip, matchings
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def packet_columns(bands, length):
    return [[((2*band, column), (2*band+1, column)) for column in range(length)]
            for band in range(bands)]


def packet_hypotheses(current, bands):
    selected, endpoints = current[2], endpoints_of(current)
    owner = {point: (band, column) for band, columns in enumerate(bands)
             for column, points in enumerate(columns) for point in points}
    mixed = {point for columns in bands for points in columns
             if len(set(points) & selected) == len(set(points) & endpoints) == 1
             for point in points if point in endpoints}
    for first, second in current[3]:
        if first not in mixed and second not in mixed:
            continue
        if first not in owner or second not in owner:
            return False
        if owner[first][0] != owner[second][0]:
            if any(len(set(neighbors(point)) & selected) < 2 for point in (first, second)):
                return False
    return True


def inspect_packet(current, bands, totals):
    direct_check(*current)
    assert packet_hypotheses(current, bands)
    selected, endpoints = current[2], endpoints_of(current)
    labels = [[tuple(1 if point in selected else 2 if point in endpoints else 0
                     for point in points) for points in columns] for columns in bands]
    positions = {point: (band, column) for band, columns in enumerate(bands)
                 for column, points in enumerate(columns) for point in points}
    region = set(positions)
    length = len(bands[0])
    assert all(len(columns) == length for columns in bands)
    strip_records = [inspect_strip(current, columns, Counter()) for columns in bands]
    nodes, node_at = [], {}
    for band, columns in enumerate(labels):
        remaining = {column for column, label in enumerate(columns) if label in ((0, 0), (1, 1))}
        while remaining:
            start = min(remaining)
            reached, pending = {start}, [start]
            remaining.remove(start)
            while pending:
                point = pending.pop()
                adjacent = {other for other in (point-1, point+1) if other in remaining
                            and (columns[point] == (1, 1) or columns[other] == (1, 1))}
                remaining -= adjacent
                reached |= adjacent
                pending.extend(adjacent)
            first, last = min(reached), max(reached)
            assert reached == set(range(first, last+1))
            assert (last-first+1) % 2 == 1
            assert columns[first] == columns[last] == (0, 0)
            index = len(nodes)
            nodes.append(dict(band=band, first=first, last=last))
            for column in reached:
                node_at[band, column] = index
    incoming, outgoing, edges = {}, {}, []
    for first, second in current[3]:
        if first not in positions or second not in positions:
            continue
        first_band, column = positions[first]
        second_band, second_column = positions[second]
        if first_band == second_band:
            continue
        first_mixed = sorted(labels[first_band][column]) == [1, 2]
        second_mixed = sorted(labels[second_band][second_column]) == [1, 2]
        if not first_mixed and not second_mixed:
            totals['uncharged_internal_cross_edges'] += 1
            continue
        assert abs(first_band-second_band) == 1 and column == second_column
        assert first_mixed and second_mixed
        assert all(len(set(neighbors(point)) & selected) == 2 for point in (first, second))
        assert all(set(neighbors(point)) & endpoints == {mate}
                   for point, mate in ((first, second), (second, first)))
        upper, lower = sorted((first_band, second_band))
        pinwheels = [(upper, lower), (lower, upper)]
        orientations = [(left, right) for left, right in pinwheels
                        if labels[left][column-1] == labels[right][column+1] == (0, 0)]
        assert len(orientations) == 1
        left_band, right_band = orientations[0]
        source, target = node_at[left_band, column-1], node_at[right_band, column+1]
        assert nodes[source]['last'] == column-1 and nodes[target]['first'] == column+1
        assert source not in outgoing and target not in incoming
        outgoing[source], incoming[target] = target, source
        edges.append((source, target))
    assert len(edges) == len(set(edges))
    assert sum(record['mixed_exports'] for record in strip_records) == 2*len(edges)
    roots = set(range(len(nodes)))-set(incoming)
    paths, path_owner = [], {}
    for root in sorted(roots):
        path, point = [], root
        while True:
            assert point not in path_owner
            path_owner[point] = len(paths)
            path.append(point)
            if point not in outgoing:
                break
            following = outgoing[point]
            assert nodes[following]['first'] == nodes[point]['last']+2
            point = following
        span = nodes[path[-1]]['last']-nodes[path[0]]['first']+1
        assert span % 2 == 1
        paths.append(path)
    assert len(path_owner) == len(nodes)
    assert len(paths) == len(nodes)-len(edges)
    first_paths = {path_owner[node_at[band, 0]] for band in range(len(bands))}
    assert len(first_paths) == len(bands)
    sealed = [band for band, columns in enumerate(labels)
              if columns[-1] == (0, 0)] if length % 2 == 0 else []
    sealed_paths = {path_owner[node_at[band, length-1]] for band in sealed}
    assert len(sealed_paths) == len(sealed) and not first_paths & sealed_paths
    assert len(paths) >= len(bands)+len(sealed)
    unused = sum(record['unused_bp'] for record in strip_records)
    surplus_twice = 2*len(bands)*length-2*len(selected & region)-len(endpoints & region)
    assert surplus_twice == sum(record['surplus_twice'] for record in strip_records)
    assert surplus_twice == 2*(len(nodes)-len(edges))+unused
    assert surplus_twice >= 2*(len(bands)+len(sealed))
    internal = sum(set(edge) <= region for edge in current[3])
    cut = sum(len(set(edge) & region) == 1 for edge in current[3])
    assert 2*len(selected & region)+2*internal+cut <= 2*(len(bands)*length-len(bands)-len(sealed))
    totals['packet_models'] += 1
    totals['charged_cross_edges'] += len(edges)
    totals['packets_with_charged_edges'] += bool(edges)
    totals['band_forests'] += len(nodes)
    totals['joint_paths'] += len(paths)
    return dict(surplus_twice=surplus_twice, charged_edges=len(edges),
                forest_intervals=len(nodes), paths=len(paths), unused_bp=unused,
                bands=len(bands), sealed_bands=len(sealed), external_matching_cuts=cut,
                band_surplus_twice=[record['surplus_twice'] for record in strip_records])


def sharp_family(pairs, sealed_mask=0):
    length = 4*pairs+2
    selected, matching = set(), []
    for index in range(pairs):
        column = 4*index+3
        matching.append(((1, column), (2, column)))
        profile = ({0, 1, 3}, {2}, {0, 3}, {1}) if index % 2 == 0 else (
            {0, 2, 3}, {1}, {0, 3}, {2})
        selected |= {(row, column-2+offset) for offset, rows in enumerate(profile) for row in rows}
    final_rows = {0, 2} if pairs % 2 else {1, 3}
    selected |= {(row, length-1) for row in final_rows if not (sealed_mask >> (row//2) & 1)}
    return 4, length, selected, matching


def sharp_controls(totals):
    records = []
    for pairs, sealed_mask in itertools.product(range(1, 81), range(4)):
        current = sharp_family(pairs, sealed_mask)
        bands = packet_columns(2, current[1])
        record = inspect_packet(current, bands, totals)
        assert record['surplus_twice'] == 4+2*sealed_mask.bit_count()
        assert record['charged_edges'] == pairs and record['unused_bp'] == 0
        assert record['paths'] == 2+sealed_mask.bit_count()
        assert len(current[2]) == 7*pairs+2-sealed_mask.bit_count()
        assert len(current[3]) == pairs
        components = endpoint_components(current)
        assert len(components) == pairs and all(len(component) == 2 for component in components)
        for component in components:
            receiver = tiles_of(component)
            assert len(receiver) == 2 and {row for row, column in receiver} == {0, 1}
            raw = sorted(2*len(current[2] & vertices_of({tile}))+1-4 for tile in receiver)
            assert raw == [-1, 1]
        force_matching(current, totals)
        totals['sharp_parameters'] += 1
        if pairs in (1, 2, 9, 80):
            records.append(dict(pairs=pairs, sealed_mask=sealed_mask, **record))
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                image_bands = [[tuple(move(point) for point in column) for column in columns] for columns in bands]
                assert inspect_packet((*shape, selected, matching), image_bands, totals) == record
                totals['sharp_symmetries'] += 1
    return records


def exhaustive_controls(totals):
    census = []
    for length in (2, 3, 4):
        counts = Counter()
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
                current = 4, length, selected, matching
                counts['feasible_matchings'] += 1
                if not packet_hypotheses(current, bands):
                    counts['outside_native_hypotheses'] += 1
                    continue
                record = inspect_packet(current, bands, totals)
                counts['accepted'] += 1
                counts['charged'] += bool(record['charged_edges'])
        census.append(dict(columns=length, **counts))
    return census


def additional_controls(totals):
    for seed in range(40):
        generator = random.Random(1700+seed)
        bands_count, length = generator.choice((3, 4, 6)), generator.choice((8, 10, 14))
        candidates = [((row, column), (row+1, column))
                      for row in range(1, 2*bands_count-1, 2)
                      for column in range(2, length-1)]
        generator.shuffle(candidates)
        selected, matching = set(), []
        for first, second in candidates:
            row, column = first
            sign = generator.choice((-1, 1))
            supports = {(row-1, column), (row, column+sign),
                        (row+1, column-sign), (row+2, column)}
            candidate = 2*bands_count, length, selected | supports, matching+[(first, second)]
            try:
                direct_check(*candidate)
            except AssertionError:
                continue
            selected |= supports
            matching.append((first, second))
        current = 2*bands_count, length, selected, matching
        bands = packet_columns(bands_count, length)
        inspect_packet(current, bands, totals)
        totals['multiband_pinwheel_packets'] += 1
        remaining = [(row, column) for row in range(2*bands_count)
                     for column in range(1, length-1) if (row, column) not in selected | endpoints_of(current)]
        generator.shuffle(remaining)
        for point in remaining:
            try:
                direct_check(*current[:2], selected | {point}, matching)
            except AssertionError:
                continue
            selected.add(point)
        inspect_packet((*current[:2], selected, matching), bands, totals)
        totals['multiband_selection_extensions'] += 1
    for mode in ('internal_vertical', 'internal_horizontal', 'external_bp'):
        selected = {(0, 1), (0, 2)}
        matching = [((1, 4), (2, 4))] if mode == 'internal_vertical' else [((2, 3), (2, 4))]
        rows, columns = 4, 8
        if mode == 'external_bp':
            rows = 6
            matching = [((3, 4), (4, 4))]
        inspect_packet((rows, columns, selected, matching), packet_columns(2, columns), totals)
        totals['nonmixed_matching_controls'] += 1
    residuals = []
    for width, height in itertools.product((6, 12, 30), (4, 8, 20)):
        current, _, _ = neutral_pair(width, height)
        bands = packet_columns(current[0]//2, current[1])
        assert not packet_hypotheses(current, bands)
        force_matching(current, totals)
        first, second = (7, 5), (8, 5)
        assert (first, second) in current[3]
        assert len(set(neighbors(first)) & current[2]) == 1
        assert len(set(neighbors(second)) & current[2]) == 2
        assert (6, 5) in endpoints_of(current) and (9, 5) in current[2]
        assert all(not set(columns[0]) & (current[2] | endpoints_of(current))
                   and not set(columns[-1]) & (current[2] | endpoints_of(current)) for columns in bands)
        residuals.append(dict(width=width, height=height, edge=[first, second],
                              upper_native_selected_neighbors=1, lower_native_selected_neighbors=2,
                              upper_band_column='PP', lower_band_column='PT',
                              matching_closed_in_whole_packet=True, unique_frozen=True))
        totals['fully_frozen_nonnative_residuals'] += 1
    return residuals


def positive_source_controls(totals):
    records = []
    for pairs, height, extra in itertools.product(range(1, 7), (4, 6, 10), (0, 6)):
        width = 6*pairs+16+extra
        root, _, _ = neutral_pair(width, height)
        selected, matching = set(root[2]), list(root[3])
        for index in range(pairs):
            column = 11+6*index
            matching.append(((9, column), (10, column)))
            selected |= {(8, column), (9, column+1), (10, column-1), (11, column)}
        current = *root[:2], selected, matching
        stop = width+4 if height == 4 else width+2
        bands = [[((row, column), (row+1, column)) for column in range(6, stop)] for row in (8, 10)]
        record = inspect_packet(current, bands, totals)
        cells = {point for columns in bands for column in columns for point in column}
        packet_tiles = tiles_of(cells)
        used, inside, outside_positive = set(), 0, 0
        for component in endpoint_components(current):
            receiver = tiles_of(component)
            assert not receiver & used
            used |= receiver
            charge_twice = 2*len(selected & vertices_of(receiver))+len(component)-4*len(receiver)
            if component & cells:
                assert receiver <= packet_tiles and len(component) == 2 and charge_twice == 0
                assert len({row for row, column in receiver}) == 2
                inside += 1
            else:
                assert not receiver & packet_tiles and charge_twice == 2
                outside_positive += 1
        assert inside == pairs and outside_positive == 1
        assert record['charged_edges'] == pairs and record['external_matching_cuts'] == 0
        assert len(selected) == height+7+4*pairs and len(matching) == width+height+pairs
        all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
        outside_deficit = sum(2-len(selected & vertices_of({tile})) for tile in all_tiles-packet_tiles-used)
        margin = current[0]*current[1]//2-direct_check(*current)
        assert 2*margin == record['surplus_twice']+2*outside_deficit-2*outside_positive
        assert margin >= record['bands']+record['sealed_bands']+outside_deficit-outside_positive >= 0
        force_matching(current, totals)
        totals['positive_source_packets'] += 1
        if pairs in (1, 6) and height in (4, 10) and extra == 0:
            records.append(dict(width=width, height=height, pairs=pairs, **record))
            for symmetry in itertools.product((False, True), repeat=3):
                shape, image_selected, image_matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                image_bands = [[tuple(move(point) for point in column) for column in columns] for columns in bands]
                assert inspect_packet((*shape, image_selected, image_matching), image_bands, totals) == record
                totals['positive_source_symmetries'] += 1
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals = Counter()
    sharp = sharp_controls(totals)
    census = exhaustive_controls(totals)
    residuals = additional_controls(totals)
    positive_sources = positive_source_controls(totals)
    assert totals['packets_with_charged_edges'] and totals['uncharged_internal_cross_edges']
    report = dict(status='PASS', controls=dict(totals), sharp_examples=sharp,
                  exhaustive_census=census, fully_frozen_nonnative_residuals=residuals,
                  positive_source_packets=positive_sources,
                  scope='Finite controls for the written arbitrary-band/length native pinwheel and path-forest proof. '
                  'Native witnesses are ORIGINAL selections; no mixed export leaves the packet. '
                  'All matching choices in short full-board label models, sharp all-r split-receiver '
                  'families, symmetries, multiband packets and feasible selection extensions. '
                  'No claim that arbitrary exchange-terminal exits satisfy native support, or that '
                  'overlapping packets are covered.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], controls=report['controls'])))


if __name__ == '__main__':
    main()
