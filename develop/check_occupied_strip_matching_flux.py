"""Finite controls for the general written occupied-strip matching-flux theorem."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from check_even_bridge_support_completion import endpoints_of, tiles_of
from check_native_guard_compensation import charge, force_matching
from check_neutral_pair_donor_saturation import neutral_pair
from check_neutral_portal_strip_compensation import corridor, image_map
from check_residual_corridors import direct_check, transformed


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(current, columns, totals):
    direct_check(*current)
    cells = {point for column in columns for point in column}
    assert len(cells) == 2*len(columns) and len(columns) >= 2
    selected, endpoints = current[2], endpoints_of(current)
    occupied = selected | endpoints
    assert not set(columns[0]) & occupied
    assert not set(columns[-1]) <= occupied
    labels = [tuple(1 if point in selected else 2 if point in endpoints else 0
                    for point in column) for column in columns]
    counts = Counter(tuple(sorted(label)) for label in labels)
    double = counts[(1, 1)]
    blank = counts[(0, 0)]
    mixed = counts[(1, 2)]
    single_endpoint = counts[(0, 2)]
    mates = {point: mate for edge in current[3] for point, mate in (edge, edge[::-1])}
    positions = {point: index for index, column in enumerate(columns) for point in column}
    exports, images = [], []
    for index, label in enumerate(labels):
        if sorted(label) != [1, 2]:
            continue
        endpoint = next(point for point in columns[index] if point in endpoints)
        mate = mates[endpoint]
        if mate not in cells:
            exports.append(endpoint)
        else:
            mate_index = positions[mate]
            assert abs(mate_index-index) == 1
            assert sorted(labels[mate_index]) == [0, 2]
            images.append(mate_index)
    assert len(set(images)) == len(images) == mixed-len(exports)
    unused = single_endpoint-mixed+len(exports)
    assert unused >= 0
    forest = {index for index, label in enumerate(labels)
              if label in ((0, 0), (1, 1))}
    edges = {(index, index+1) for index in range(len(columns)-1)
             if index in forest and index+1 in forest
             and (labels[index] == (1, 1) or labels[index+1] == (1, 1))}
    assert len(edges) == 2*double
    remaining = set(forest)
    component_count = 0
    while remaining:
        pending = [remaining.pop()]
        component_count += 1
        while pending:
            point = pending.pop()
            adjacent = {other for edge in edges if point in edge for other in edge}
            added = adjacent & remaining
            remaining -= added
            pending.extend(added)
    assert component_count == blank-double >= 1
    sealed = labels[-1] == (0, 0)
    delta = 2 if sealed and len(columns) % 2 == 0 else 1
    assert blank-double >= delta
    surplus_twice = 2*len(columns)-2*len(selected & cells)-len(endpoints & cells)
    assert surplus_twice+len(exports) == 2*(blank-double)+unused
    assert surplus_twice >= 2*delta-len(exports)
    internal = sum(set(edge) <= cells for edge in current[3])
    cut = sum(len(set(edge) & cells) == 1 for edge in current[3])
    assert len(endpoints & cells) == 2*internal+cut
    assert cut >= len(exports)
    assert 2*len(selected & cells)+2*internal+cut-len(exports) <= 2*(len(columns)-delta)
    totals['regional_models'] += 1
    totals['mixed_export_models'] += bool(exports)
    totals['only_nonmixed_export_models'] += bool(cut) and not exports
    totals['sealed_even_models'] += delta == 2
    return dict(surplus_twice=surplus_twice, delta=delta, mixed_exports=len(exports),
                all_exports=cut, forest_components=component_count, unused_bp=unused,
                internal_matching_edges=internal)


def physical_ledger(current, tiles):
    selected, endpoints = current[2], endpoints_of(current)
    occupied_tiles = tiles & tiles_of(endpoints)
    deficit = sum(2-len(selected & vertices_of({tile})) for tile in tiles-occupied_tiles)
    raw_twice = sum(2*len(selected & vertices_of({tile}))
                    + len(endpoints & vertices_of({tile}))-4 for tile in occupied_tiles)
    cells = vertices_of(tiles)
    surplus_twice = 4*len(tiles)-2*len(selected & cells)-len(endpoints & cells)
    assert surplus_twice == 2*deficit-raw_twice
    return deficit, raw_twice


def matchings(endpoints, allow_exports):
    if not endpoints:
        yield [], set()
        return
    first = min(endpoints)
    remaining = endpoints-{first}
    if allow_exports:
        for matching, exported in matchings(remaining, allow_exports):
            yield matching, exported | {first}
    for mate in sorted(set(neighbors(first)) & remaining):
        for matching, exported in matchings(remaining-{mate}, allow_exports):
            yield [(first, mate), *matching], exported


def exhaustive_controls(totals):
    census = []
    for length in range(2, 6):
        counts = Counter()
        columns = [((1, column), (2, column)) for column in range(length)]
        for interior in itertools.product(range(3), repeat=2*length-2):
            labels = (0, 0, *interior)
            if labels[-2] and labels[-1]:
                continue
            selected = {columns[index//2][index % 2] for index, label in enumerate(labels) if label == 1}
            endpoints = {columns[index//2][index % 2] for index, label in enumerate(labels) if label == 2}
            if any(len(set(neighbors(point)) & (selected | endpoints)) > 1 for point in selected):
                continue
            for matching, exported in matchings(endpoints, length <= 4):
                exterior = [((0 if point[0] == 1 else 3, point[1]), point) for point in sorted(exported)]
                current = 4, length, selected, matching+exterior
                inspect(current, columns, totals)
                counts['feasible_matchings'] += 1
                counts['with_exports' if exported else 'closed'] += 1
        assert counts['closed'] > 0
        census.append(dict(columns=length, **counts))
    return census


def counterexample(length, sealed):
    selected = {(0, 1), (2, 0), (3, 1)} | {(1-column % 2, column) for column in range(2, length)}
    if sealed:
        selected.remove((0, length-1))
    return 4, length, selected, [((1, 1), (2, 1))]


def counterfamily_controls(totals):
    examples = []
    for length, sealed in itertools.product(range(4, 101, 2), (False, True)):
        current = counterexample(length, sealed)
        columns = [((0, column), (1, column)) for column in range(length)]
        record = inspect(current, columns, totals)
        assert record['surplus_twice'] == (3 if sealed else 1)
        assert record['mixed_exports'] == record['all_exports'] == 1
        assert record['unused_bp'] == 0
        assert min(occupied_degrees(current).values()) == 3
        force_matching(current, totals)
        upper = {(0, column) for column in range(length//2)}
        lower = {(1, column) for column in range(length//2)}
        assert physical_ledger(current, upper) == (int(sealed), -1)
        assert physical_ledger(current, lower)[1] == 1
        assert charge(current) == 0
        assert len(current[2]) == length+1-int(sealed)
        assert current[0]*current[1]//2-direct_check(*current) == length-2+int(sealed)
        totals['sharp_counterfamily_parameters'] += 1
        if length in (4, 20, 100):
            examples.append(dict(columns=length, sealed=sealed, **record))
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                image_columns = [tuple(move(point) for point in column) for column in columns]
                assert inspect((*shape, selected, matching), image_columns, totals) == record
                totals['counterfamily_symmetries'] += 1
    for length in range(3, 32, 2):
        selected = {(row, column) for column in range(1, length, 2) for row in (0, 1)}
        current = 2, length, selected, []
        record = inspect(current, [((0, column), (1, column)) for column in range(length)], totals)
        assert record['surplus_twice'] == 2 and record['forest_components'] == 1
        totals['odd_sealed_parity_obstructions'] += 1
    return examples


def occupied_pair(width, height, pairs):
    current, _, _ = neutral_pair(width, height)
    selected, matching = set(current[2]), list(current[3])
    for index in range(pairs):
        column = 11+6*index
        matching.append(((8, column), (8, column+1)))
        selected |= {(8, column-1), (7, column), (8, column+2), (9, column+1)}
    return *current[:2], selected, matching


def inspect_occupied(current, columns, tiles, pairs, totals):
    record = inspect(current, columns, totals)
    assert record['mixed_exports'] == record['all_exports'] == 0
    endpoints, selected = endpoints_of(current), current[2]
    cells = vertices_of(tiles)
    assert cells == {point for column in columns for point in column}
    components = endpoint_components(current)
    assert len(components) == pairs+1
    used, outside_charge, inside_count = set(), 0, 0
    for component in components:
        receiver = tiles_of(component)
        assert not used & receiver
        used |= receiver
        component_charge_twice = 2*len(selected & vertices_of(receiver))+len(component)-4*len(receiver)
        assert component_charge_twice == (0 if component & cells else 2)
        if component & cells:
            assert receiver <= tiles
            inside_count += 1
        else:
            assert not receiver & tiles
            outside_charge += component_charge_twice//2
    assert inside_count == pairs and outside_charge == 1
    assert charge(current) == 1
    deficit, raw_twice = physical_ledger(current, tiles)
    assert raw_twice == 0 and record['surplus_twice'] == 2*deficit
    all_tiles = set(itertools.product(range(current[0]//2), range(current[1]//2)))
    outside_deficit = sum(2-len(selected & vertices_of({tile})) for tile in all_tiles-tiles-used)
    margin = current[0]*current[1]//2-direct_check(*current)
    assert 2*margin == record['surplus_twice']+2*outside_deficit-2*outside_charge
    assert margin >= record['delta']+outside_deficit-outside_charge >= 0
    assert min(occupied_degrees(current).values()) >= 3
    force_matching(current, totals)
    totals['receiver_closed_occupied_models'] += 1
    return record


def occupied_controls(totals):
    examples = []
    for pairs, height, extra in itertools.product(range(1, 7), (4, 6, 10), (0, 4, 12)):
        width = 6*pairs+16+extra
        current = occupied_pair(width, height, pairs)
        tiles = set(corridor(width, height))
        columns = [((8, column), (9, column))
                   for column in range(6, (width+4 if height == 4 else width+2))]
        record = inspect_occupied(current, columns, tiles, pairs, totals)
        assert len(current[3]) == width+height+pairs
        assert len(current[2]) == height+7+4*pairs
        assert record['delta'] >= (2 if height == 4 else 1)
        totals['occupied_parameter_triples'] += 1
        for seed in range(2):
            selected = set(current[2])
            candidates = sorted(vertices_of(tiles)-(selected | endpoints_of(current)))
            random.Random(1000*pairs+100*height+extra+seed).shuffle(candidates)
            for point in candidates:
                try:
                    direct_check(*current[:2], selected | {point}, current[3])
                except AssertionError:
                    continue
                selected.add(point)
            inspect_occupied((*current[:2], selected, current[3]), columns, tiles, pairs, totals)
            totals['occupied_selection_extensions'] += 1
        if pairs in (1, 6) and height in (4, 10) and extra == 0:
            examples.append(dict(width=width, height=height, pairs=pairs, **record))
            for symmetry in itertools.product((False, True), repeat=3):
                shape, selected, matching = transformed(*current, *symmetry)
                move = image_map(*current[:2], symmetry)
                image_columns = [tuple(move(point) for point in column) for column in columns]
                image_tiles = {tuple(value//2 for value in move((2*row, 2*column))) for row, column in tiles}
                assert inspect_occupied((*shape, selected, matching), image_columns, image_tiles, pairs, totals) == record
                totals['occupied_symmetries'] += 1
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True, type=Path)
    arguments = parser.parse_args()
    totals = Counter()
    census = exhaustive_controls(totals)
    counterexamples = counterfamily_controls(totals)
    occupied = occupied_controls(totals)
    assert totals['mixed_export_models'] and totals['only_nonmixed_export_models']
    report = dict(status='PASS', controls=dict(totals), exhaustive_census=census,
                  counterexamples=counterexamples, occupied_examples=occupied,
                  scope='Finite controls for the general written matching injection and boundary-forest proof. '
                  'All partial matchings with transverse completion on strips of lengths 2..4; '
                  'all closed matchings at length 5. Explicit terminal counterfamilies and '
                  'receiver-closed occupied neutral families, symmetries and feasible extensions. '
                  'No unrestricted coverage, crossing allocation or global target counterexample claimed.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], controls=report['controls'])))


if __name__ == '__main__':
    main()
