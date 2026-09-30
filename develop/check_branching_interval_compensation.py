#!/usr/bin/env python3
"""Coordinate and word controls for branching interval compensation."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_compensation_transport import flip_internal_squares
from check_cross_component_compensation import band_ledger, encode, witness_record
from check_pressure_bands import branching_band, local_controls
from check_residual_corridors import corridor, direct_check, graph_record, transformed
from verify_grid_five_sixths import canonical


def leaf(width=1):
    return dict(width=width, children=[])


def node(*children):
    return dict(width=sum(child['width']+2 for child in children)+len(children)-1,
                children=list(children))


def tree_depth(tree):
    return 1+max((tree_depth(child) for child in tree['children']), default=-1)


def band_region(tile_row, left, width):
    return {(row, column) for row in (2*tile_row, 2*tile_row+1)
            for column in range(2*left, 2*(left+width))}


def cap_vertices(tile_row, tile_column, orientation):
    top, start = 2*tile_row, 2*tile_column
    if orientation == 'R':
        return {(top, start), (top+1, start+1)}
    return {(top, start+1), (top+1, start)}


def tree_configuration(tree):
    _, columns, selected, matching = corridor(tree['width'])
    rows = 2*(tree_depth(tree)+2)
    regions = []

    def build(current, tile_row, left):
        width = current['width']
        top = 2*tile_row
        matching.extend(((top, 2*column), (top, 2*column+1))
                        for column in range(left, left+width))
        children = current['children']
        regions.append(dict(vertices=band_region(tile_row, left, width),
                            terminal=not children, width=width,
                            tile_row=tile_row, left=left))
        if not children:
            matching.extend(((top+1, 2*column+1), (top+1, 2*column+2))
                            for column in range(left, left+width-1))
            return
        exits = set()
        cursor = left
        for child in children:
            right = cursor+child['width']+1
            exits.update((cursor, right))
            matching.extend((((top+1, 2*cursor+1), (top+2, 2*cursor+1)),
                             ((top+1, 2*right), (top+2, 2*right))))
            selected.update(cap_vertices(tile_row+1, cursor, 'R'))
            selected.update(cap_vertices(tile_row+1, right, 'L'))
            build(child, tile_row+1, cursor+1)
            cursor = right+2
        matching.extend(((top+1, 2*column), (top+1, 2*column+1))
                        for column in range(left, left+width) if column not in exits)

    build(tree, 1, 1)
    return (rows, columns, selected, matching), regions


def separator_configuration(left_selected, child_width, right_selected):
    width = left_selected+child_width+right_selected+2
    _, columns, selected, matching = corridor(width)
    matching.extend(((2, 2*column), (2, 2*column+1))
                    for column in range(1, width+1))
    left_exit, right_exit = left_selected+1, left_selected+child_width+2
    selected.update((3, 2*column+1) for column in range(1, left_exit))
    selected.update((3, 2*column) for column in range(right_exit+1, width+1))
    selected.update(cap_vertices(2, left_exit, 'R'))
    selected.update(cap_vertices(2, right_exit, 'L'))
    matching.extend((((3, 2*left_exit+1), (4, 2*left_exit+1)),
                     ((3, 2*right_exit), (4, 2*right_exit))))
    matching.extend(((3, 2*column), (3, 2*column+1))
                    for column in range(left_exit+1, right_exit))
    matching.extend(((4, 2*column), (4, 2*column+1))
                    for column in range(left_exit+1, right_exit))
    matching.extend(((5, 2*column+1), (5, 2*column+2))
                    for column in range(left_exit+1, right_exit-1))
    regions = [dict(vertices=band_region(1, 1, width), terminal=False,
                    width=width, tile_row=1, left=1),
               dict(vertices=band_region(2, left_exit+1, child_width), terminal=True,
                    width=child_width, tile_row=2, left=left_exit+1)]
    return (6, columns, selected, matching), regions


def mixed_neutral_obstacle():
    _, columns, selected, matching = corridor(5)
    selected.update({(2, 5), (3, 4), (2, 7), (3, 8),
                     (4, 2), (5, 3), (4, 7), (5, 6), (4, 11), (5, 10),
                     (4, 0), (5, 1), (4, 13), (5, 12), (4, 5), (5, 8)})
    matching.extend((((2, 2), (2, 3)), ((2, 9), (3, 9)), ((2, 10), (2, 11)),
                     ((3, 3), (4, 3)), ((3, 6), (4, 6)), ((3, 10), (4, 10))))
    return 6, columns, selected, matching


def word_controls(max_width):
    neutral = local_controls()['neutral_states']
    upper_p = {(state['labels'], tuple(state['exit_corners']))
               for state in neutral if state['labels'].startswith('PP/')}
    assert upper_p == {('PP/PP', ()), ('PP/BP', (3,)), ('PP/PB', (2,)),
                       ('PP/BT', ()), ('PP/TB', ())}
    lower_labels = {'F': 'PP', 'R': 'BP', 'L': 'PB', 'X': 'BT', 'Y': 'TB'}
    reports = []
    for width in range(1, max_width+1):
        accepted = 0
        children_total = 0
        for states in itertools.product(lower_labels, repeat=width):
            labels = ''.join(lower_labels[state] for state in states)
            if labels[0] != 'B' or labels[-1] != 'B':
                continue
            if any((index and labels[index-1] != 'B')
                   or (index+1 < len(labels) and labels[index+1] != 'B')
                   for index, label in enumerate(labels) if label == 'T'):
                continue
            exits = [(index, state) for index, state in enumerate(states) if state in ('R', 'L')]
            if any(second[0] == first[0]+1 for first, second in zip(exits, exits[1:])):
                continue
            assert exits and exits[0][1] == 'R' and exits[-1][1] == 'L'
            children = []
            for first, second in zip(exits, exits[1:]):
                if first[1] == 'R' and second[1] == 'L':
                    interval = set(range(first[0]+1, second[0]))
                    assert interval and len(interval) <= width-2
                    assert all(states[index] == 'F' for index in interval)
                    assert all(not interval & previous for previous in children)
                    children.append(interval)
            assert children
            accepted += 1
            children_total += len(children)
        reports.append(dict(tile_width=width, words_examined=5**width,
                            necessary_feasible_words=accepted, child_intervals=children_total))
    return dict(widths=reports, exact_upper_p_neutral_states=sorted(upper_p),
                scope='Necessary label and adjacent-cap conditions, not enumeration of globally feasible matchings.')


def verify_forest(configuration, regions, roots=1, source_tiles=None):
    rows, columns, selected, matching = configuration
    objective = direct_check(*configuration)
    graph, components = graph_record(*configuration)
    charges = [graph['deg'][tile]-2*graph['r'][tile] if graph['t'][tile] < 2 else 0
               for tile in range(graph['N'])]
    source = set(range(columns//2)) if source_tiles is None else set(source_tiles)
    assert sum(charges[tile] for tile in source) == 2*roots
    claimed = set(source)
    terminals = 0
    for region in regions:
        ledger = band_ledger(*configuration, region['vertices'])
        tiles = set(ledger['tiles'])
        assert not claimed & tiles
        claimed.update(tiles)
        assert ledger['charge_twice'] == (-2 if region['terminal'] else 0)
        assert all(charges[tile] <= 0 for tile in tiles)
        if region['terminal']:
            assert ledger['saturated_attachments'] == 0
            terminals += 1
    remainder = sum(charge for tile, charge in enumerate(charges) if tile not in claimed)
    assert remainder <= 0 and terminals >= roots
    assert 2*objective-rows*columns == sum(charges)
    assert 2*objective-rows*columns == 2*(roots-terminals)+remainder
    canonical(rows, columns, *encode(*configuration))
    return dict(rows=rows, columns=columns, sources=roots, terminal_bands=terminals,
                remainder_charge_twice=remainder, q=objective-rows*columns//2,
                max_capacity=max(graph['r']),
                component_excesses=sorted(component['excess'] for component in components))


def symmetry_controls(configuration, regions, roots=1, source_tiles=None):
    baseline = verify_forest(configuration, regions, roots, source_tiles)
    rows, columns, selected, matching = configuration
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        dimensions, moved_selected, moved_matching = transformed(
            *configuration, transpose, flip_rows, flip_columns)
        graph, components = graph_record(*dimensions, moved_selected, moved_matching)
        assert direct_check(*dimensions, moved_selected, moved_matching) == len(selected)+len(matching)
        assert sorted(component['excess'] for component in components) == baseline['component_excesses']
        for region in regions:
            _, moved_region, _ = transformed(rows, columns, region['vertices'], [],
                                             transpose, flip_rows, flip_columns)
            ledger = band_ledger(*dimensions, moved_selected, moved_matching, moved_region)
            assert ledger['charge_twice'] == (-2 if region['terminal'] else 0)
        canonical(*dimensions, *encode(*dimensions, moved_selected, moved_matching))
    return baseline


def multiple_roots(branch_counts):
    selected = set()
    matching = []
    regions = []
    source_tiles = set()
    offset = 0
    for branches in branch_counts:
        configuration = branching_band(branches)
        _, columns, source_selected, source_matching = configuration
        selected.update((row, column+offset) for row, column in source_selected)
        matching.extend(((first[0], first[1]+offset), (second[0], second[1]+offset))
                        for first, second in source_matching)
        source_tiles.update(range(offset//2, (offset+columns)//2))
        width = 4*branches-1
        regions.append(dict(vertices={(row, column+offset)
                                      for row, column in band_region(1, 1, width)}, terminal=False))
        regions.extend(dict(vertices={(row, column+offset)
                                      for row, column in band_region(2, 4*index+2, 1)}, terminal=True)
                       for index in range(branches))
        offset += columns+4
    return (6, offset-4, selected, matching), regions, source_tiles


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-word-width', type=int, default=8)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    if not 3 <= args.max_word_width <= 9:
        parser.error('--max-word-width must be between 3 and 9')
    words = word_controls(args.max_word_width)
    records = []
    images = 0
    for left_selected, child_width, right_selected in itertools.product(range(4), range(1, 7), range(4)):
        configuration, regions = separator_configuration(left_selected, child_width, right_selected)
        symmetry_controls(configuration, regions)
        images += 8
    trees = [leaf(2), leaf(3), node(leaf(1)), node(leaf(1), leaf(2)),
             node(node(leaf(1), leaf(2)), leaf(3)),
             node(node(leaf(1)), node(leaf(2), leaf(1)), leaf(1))]
    for depth in range(2, 10):
        tree = leaf(1)
        for _ in range(depth):
            tree = node(tree)
        trees.append(tree)
    for index, tree in enumerate(trees):
        configuration, regions = tree_configuration(tree)
        original = symmetry_controls(configuration, regions)
        records.append(dict(tree=index, depth=tree_depth(tree), **original))
        images += 8
        if tree['children']:
            for limit in (1, configuration[0]*configuration[1]):
                changed, swaps = flip_internal_squares(configuration, limit)
                assert swaps > 0
                flipped = symmetry_controls(changed, regions)
                assert flipped['q'] == original['q'] and flipped['max_capacity'] == 2
                images += 8
    branching = []
    for branches in range(1, 17):
        configuration = branching_band(branches)
        width = 4*branches-1
        regions = [dict(vertices=band_region(1, 1, width), terminal=False)]
        regions.extend(dict(vertices=band_region(2, 4*index+2, 1), terminal=True)
                       for index in range(branches))
        result = symmetry_controls(configuration, regions)
        assert result['remainder_charge_twice'] == 0 and result['q'] == 1-branches
        branching.append(dict(branches=branches, **result))
        images += 8
    multiple = []
    for branch_counts in ((1, 1), (1, 2), (2, 3, 1), (4, 2, 3, 1)):
        configuration, regions, source_tiles = multiple_roots(branch_counts)
        result = symmetry_controls(configuration, regions, len(branch_counts), source_tiles)
        assert result['terminal_bands'] == sum(branch_counts)
        assert result['remainder_charge_twice'] == -24*(len(branch_counts)-1)
        multiple.append(dict(branch_counts=branch_counts, **result))
        images += 8
    obstacle = mixed_neutral_obstacle()
    witness = witness_record('Neutral band without a P-pressure successor', obstacle,
                             band_region(1, 1, 5))
    assert witness['objective'] == 41 and witness['q'] == -1
    assert witness['band']['charge_twice'] == 0
    assert witness['band']['saturated_attachments'] == 3
    assert len(obstacle[2]) == 22 and len(obstacle[3]) == 19
    assert sorted(component['excess'] for component in witness['components']) == [-1, -1, 0, 0, 0, 0, 1]
    endpoints = {vertex for edge in obstacle[3] for vertex in edge}
    assert (3, 4) in obstacle[2] and (3, 5) not in obstacle[2] | endpoints
    assert not all((2, column) in endpoints for column in range(2, 12))
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        dimensions, selected, matching = transformed(*obstacle, transpose, flip_rows, flip_columns)
        assert direct_check(*dimensions, selected, matching) == 41
        canonical(*dimensions, *encode(*dimensions, selected, matching))
        _, components = graph_record(*dimensions, selected, matching)
        assert sorted(component['excess'] for component in components) == [-1, -1, 0, 0, 0, 0, 1]
    images += 8
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/BRANCHING_INTERVAL_COMPENSATION.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_compensation_transport.py', 'check_cross_component_compensation.py',
        'check_pressure_bands.py', 'check_residual_corridors.py',
        'verify_grid_five_sixths.py', 'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', word_controls=words,
                  separator_configurations=96, tree_records=records,
                  branching_equality_controls=branching, multiple_root_controls=multiple,
                  symmetry_images=images,
                  obstacle=witness,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite controls of separately written proofs. The forest closure and disjointness are hypotheses; general bends and mixed neutral states remain open. No new Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('obstacle', 'tree_records', 'branching_equality_controls',
                                     'multiple_root_controls')}, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
