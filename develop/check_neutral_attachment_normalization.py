#!/usr/bin/env python3
"""Coordinate and residual controls for neutral attachment promotion."""
import argparse
import collections
import hashlib
import itertools
import json
from pathlib import Path

from check_branching_interval_compensation import mixed_neutral_obstacle
from check_compensation_transport import flip_internal_squares
from check_cross_component_compensation import flipped_band, witness_record
from check_diagonal_relay_normalization import relay_tiles
from check_mixed_neutral_donors import wide_mixed_obstacle
from check_neutral_relay_obstacle import neutral_completion
from check_pressure_bands import branching_band
from check_residual_corridors import direct_check, graph_record, transformed
from check_same_direction_capacity_donors import configuration
from verify_grid_five_sixths import bits, pairs


def neighbors(vertex):
    row, column = vertex
    return ((row-1, column), (row+1, column),
            (row, column-1), (row, column+1))


def attachment_universe(current):
    rows, columns, selected, matching = current
    residual_graph, _ = graph_record(*current)
    candidates = []
    for first, second in matching:
        for endpoint, mate in ((first, second), (second, first)):
            source = (endpoint[0]//2)*(columns//2)+endpoint[1]//2
            receiving = (mate[0]//2)*(columns//2)+mate[1]//2
            if (residual_graph['t'][source] < 2
                    and residual_graph['deg'][source] == 2*residual_graph['r'][source]
                    and residual_graph['t'][receiving] == 2):
                candidates.append((endpoint, mate))
    return sorted(candidates)


def eligible(current):
    occupied = current[2] | {vertex for edge in current[3] for vertex in edge}
    return [edge for edge in attachment_universe(current)
            if sum(vertex in occupied for vertex in neighbors(edge[0])) <= 2]


def promote(current, edge):
    assert edge in eligible(current)
    endpoint, mate = edge
    changed = (*current[:2], current[2] | {endpoint},
               [old_edge for old_edge in current[3] if set(old_edge) != set(edge)])
    assert direct_check(*current) == direct_check(*changed)
    before, before_components = graph_record(*current)
    after, after_components = graph_record(*changed)
    for key in ('E', 'ends', 'r', 'deg'):
        assert before[key] == after[key], (key, edge)
    assert [degree-2*capacity for degree, capacity in zip(before['deg'], before['r'])] == [
        degree-2*capacity for degree, capacity in zip(after['deg'], after['r'])]
    removed = {tile for tile in range(before['N'])
               if before['t'][tile] < 2 and after['t'][tile] == 2}
    expected = [component for component in before_components
                if not (len(component['tiles']) == 1 and component['tiles'][0] in removed)]
    assert expected == after_components
    assert all(before['r'][tile] == before['deg'][tile] == 0 for tile in removed)
    assert set(attachment_universe(changed)) == set(attachment_universe(current))-{edge}
    assert set(eligible(current))-{edge} <= set(eligible(changed))
    return changed


def normalize(current, reverse=False):
    processed = []
    while candidates := eligible(current):
        edge = candidates[-1] if reverse else candidates[0]
        current = promote(current, edge)
        processed.append(edge)
    assert not relay_tiles(current)
    return current, processed


def queue_normalize(current):
    rows, columns, selected, matching = current
    universe = dict(attachment_universe(current))
    occupied = selected | {vertex for edge in matching for vertex in edge}
    degrees = {endpoint: sum(vertex in occupied for vertex in neighbors(endpoint))
               for endpoint in universe}
    pending = collections.deque(endpoint for endpoint in universe if degrees[endpoint] <= 2)
    processed = set()
    while pending:
        endpoint = pending.popleft()
        if endpoint in processed:
            continue
        assert degrees[endpoint] <= 2
        processed.add(endpoint)
        mate = universe[endpoint]
        assert mate in occupied
        occupied.remove(mate)
        for neighbor in neighbors(mate):
            if neighbor in degrees and neighbor not in processed:
                degrees[neighbor] -= 1
                if degrees[neighbor] <= 2:
                    pending.append(neighbor)
    removed = {frozenset((endpoint, universe[endpoint])) for endpoint in processed}
    changed = (rows, columns, selected | processed,
               [edge for edge in matching if frozenset(edge) not in removed])
    assert not eligible(changed)
    return changed


def signature(current):
    return tuple(sorted(current[2])), tuple(sorted(tuple(sorted(edge)) for edge in current[3]))


def all_orders(current):
    candidates = eligible(current)
    if not candidates:
        return {signature(current)}, 1
    outcomes = set()
    order_count = 0
    for edge in candidates:
        endings, count = all_orders(promote(current, edge))
        outcomes.update(endings)
        order_count += count
    assert len(outcomes) == 1
    return outcomes, order_count


def three_endpoint(kind):
    selected = {(4, 2), (5, 3)}
    matching = [((3, 3), (4, 3))]
    if kind == 'passage':
        matching.extend((((2, 2), (1, 2)), ((2, 3), (1, 3))))
    else:
        matching.append(((2, 2), (2, 3)))
    if kind == 'blocked':
        matching.append(((3, 4), (2, 4)))
    return 6, 6, selected, matching


def blocked_control():
    current = three_endpoint('blocked')
    assert direct_check(*current) == 5
    residual_graph, _ = graph_record(*current)
    tile = 4
    assert residual_graph['t'][tile] == 0
    assert residual_graph['deg'][tile] == 2*residual_graph['r'][tile] == 0
    assert ((3, 3), (4, 3)) in attachment_universe(current)
    assert ((3, 3), (4, 3)) not in eligible(current)
    changed = (*current[:2], current[2] | {(3, 3)},
               [edge for edge in current[3] if set(edge) != {(3, 3), (4, 3)}])
    occupied = changed[2] | {vertex for edge in changed[3] for vertex in edge}
    violating_neighbors = sorted(vertex for vertex in neighbors((3, 3)) if vertex in occupied)
    assert violating_neighbors == [(2, 3), (3, 4)]
    try:
        direct_check(*changed)
    except AssertionError:
        return dict(before=witness_record('blocked neutral attachment', current),
                    failed_promotion=[3, 3], occupied_neighbors_after=violating_neighbors,
                    failed_rule='Promote every neutral attachment without checking occupied degree.',
                    grid_target_refuted=False)
    raise AssertionError('Blocked promotion unexpectedly feasible.')


def exhaustive_controls():
    records = []
    for columns in (2, 4, 6):
        examined = with_moves = moves = 0
        for selected_mask, _, matching_indices in pairs(2, columns):
            current = (2, columns, {divmod(vertex, columns) for vertex in bits(selected_mask)},
                       [(divmod(first, columns), divmod(second, columns))
                        for first, second in matching_indices])
            examined += 1
            first, processed = normalize(current)
            second, _ = normalize(current, reverse=True)
            assert signature(first) == signature(second) == signature(queue_normalize(current))
            with_moves += bool(processed)
            moves += len(processed)
        records.append(dict(rows=2, columns=columns, feasible_pairs=examined,
                            pairs_with_promotions=with_moves, promotions=moves))
    assert sum(record['feasible_pairs'] for record in records) == 12752
    return records


def pressure_band_control(current):
    rows, columns, selected, matching = current
    residual_graph, _ = graph_record(*current)
    endpoints = {vertex for edge in matching for vertex in edge}
    occupied = selected | endpoints
    assert all((1, column) in endpoints for column in range(2, columns-2))
    allowed = {'PP/PP', 'PP/BP', 'PP/PB', 'PP/BT', 'PP/TB',
               'BP/TP', 'PB/PT', 'BB/TT', 'BT/TB', 'TB/BT'}
    states = []
    exits = []
    for tile_column in range(1, columns//2-1):
        tile = columns//2+tile_column
        assert residual_graph['deg'][tile] == 2*residual_graph['r'][tile]
        letters = ['T' if (row, column) in selected else
                   'P' if (row, column) in endpoints else 'B'
                   for row in (2, 3) for column in (2*tile_column, 2*tile_column+1)]
        state = ''.join(letters[:2])+'/'+''.join(letters[2:])
        assert state in allowed
        states.append(state)
        if state in ('PP/BP', 'PP/PB'):
            endpoint = (3, 2*tile_column+(state == 'PP/BP'))
            assert sum(vertex in occupied for vertex in neighbors(endpoint)) == 3
            assert residual_graph['s'][tile] == 1
            exits.append((tile_column, 'R' if state == 'PP/BP' else 'L'))
        else:
            assert residual_graph['s'][tile] == 0
    assert exits[0][1] == 'R' and exits[-1][1] == 'L'
    assert any(first[1] == 'R' and second[1] == 'L'
               for first, second in zip(exits, exits[1:]))
    return dict(states=states, exits=exits)


def fixtures():
    cases = [(kind, configuration(kind)) for kind in ('neutral_down', 'neutral_up', 'neutral_both')]
    cases.extend((('all_neutral_8x8', neutral_completion()),
                  ('mixed_6x14', mixed_neutral_obstacle()),
                  ('mixed_6x20', wide_mixed_obstacle()),
                  ('branching_two_pairs', branching_band(2)),
                  ('capacity_two_routes', flipped_band(3))))
    cases.extend(('three_P_'+kind, three_endpoint(kind))
                 for kind in ('isolated', 'passage', 'blocked'))
    current, swaps = flip_internal_squares(mixed_neutral_obstacle(), 100)
    assert swaps > 0
    cases.append(('mixed_capacity_two', current))
    selected = {divmod(vertex, 6) for vertex in (3, 5, 8, 24, 33, 35, 36, 43)}
    matching = [(divmod(first, 6), divmod(second, 6))
                for first, second in ((9, 10), (11, 17), (16, 22), (23, 29),
                                      (25, 26), (27, 28), (31, 37))]
    cases.append(('bent_positive_path', (8, 6, selected, matching)))
    return cases


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    records = []
    order_controls = []
    pressure_bands = []
    for name, original in fixtures():
        outcomes, order_count = all_orders(original)
        changed, moves = normalize(original)
        assert outcomes == {signature(changed)}
        order_controls.append(dict(name=name, legal_complete_orders=order_count, moves=len(moves)))
        for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, transpose, flip_rows, flip_columns)
            current = (*shape, selected, matching)
            normalized, processed = normalize(current)
            opposite, _ = normalize(current, reverse=True)
            assert signature(normalized) == signature(opposite) == signature(queue_normalize(current))
            expected_shape, expected_selected, expected_matching = transformed(
                *changed, transpose, flip_rows, flip_columns)
            assert shape == expected_shape
            assert signature(normalized) == signature((*shape, expected_selected, expected_matching))
            before = witness_record(name, current)
            after = witness_record(name+' normalized', normalized)
            records.append(dict(name=name, symmetry=[transpose, flip_rows, flip_columns],
                                moves=processed, before=before, after=after))
        if name == 'all_neutral_8x8':
            assert len(moves) == 4 and len(changed[2]) == 32 and not changed[3]
        if name == 'three_P_passage':
            graph, _ = graph_record(*changed)
            assert graph['r'][4] == 1 and graph['deg'][4] == 2 and max(graph['r']) == 2
        if name in ('branching_two_pairs', 'bent_positive_path'):
            assert not moves
            _, components = graph_record(*changed)
            assert any(component['excess'] == 1 for component in components)
        if name in ('mixed_6x14', 'mixed_6x20', 'branching_two_pairs', 'mixed_capacity_two'):
            pressure_bands.append(dict(name=name, **pressure_band_control(changed)))
    exhaustive = exhaustive_controls()
    irreducible_branches = []
    for branches in range(1, 33):
        current = branching_band(branches)
        assert direct_check(*current)-current[0]*current[1]//2 == 1-branches
        assert not eligible(current)
        assert signature(current) == signature(queue_normalize(current))
        band = pressure_band_control(current)
        assert len(band['exits']) == 2*branches
        irreducible_branches.append(branches)
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/NEUTRAL_ATTACHMENT_NORMALIZATION.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_diagonal_relay_normalization.py', 'check_residual_corridors.py',
        'check_cross_component_compensation.py', 'check_branching_interval_compensation.py',
        'check_mixed_neutral_donors.py', 'check_neutral_relay_obstacle.py',
        'check_pressure_bands.py', 'check_same_direction_capacity_donors.py',
        'check_compensation_transport.py', 'verify_grid_five_sixths.py',
        'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', symmetry_controls=len(records),
                  order_controls=order_controls, exhaustive_ladders=exhaustive,
                  normalized_pressure_bands=pressure_bands,
                  irreducible_branch_counts=irreducible_branches,
                  blocked_move=blocked_control(), witnesses=records,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite controls for the general charge-preserving normalization proof; no universal compensation or new Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in ('witnesses', 'blocked_move', 'sha256')}, indent=2))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
