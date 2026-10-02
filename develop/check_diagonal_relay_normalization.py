#!/usr/bin/env python3
"""Controls for saturating diagonal neutral relays without changing charge."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_branching_interval_compensation import mixed_neutral_obstacle
from check_cross_component_compensation import witness_record
from check_mixed_neutral_donors import wide_mixed_obstacle
from check_neutral_relay_obstacle import neutral_completion
from check_residual_corridors import direct_check, graph_record, transformed
from check_same_direction_capacity_donors import configuration


def relay_tiles(current):
    rows, columns, selected, matching = current
    graph, _ = graph_record(*current)
    occupied = selected | {vertex for edge in matching for vertex in edge}
    relays = []
    for tile in range(graph['N']):
        if graph['t'][tile] == 2 or graph['h'][tile] or graph['r'][tile] or graph['deg'][tile]:
            continue
        tile_row, tile_column = divmod(tile, columns//2)
        corners = [(2*tile_row+row, 2*tile_column+column)
                   for row, column in itertools.product(range(2), repeat=2)]
        active = [vertex for vertex in corners if vertex in occupied]
        if len(active) == 2 and active[0][0] != active[1][0] and active[0][1] != active[1][1]:
            relays.append(tile)
    return relays


def saturate(current, tile):
    rows, columns, selected, matching = current
    assert tile in relay_tiles(current)
    tile_row, tile_column = divmod(tile, columns//2)
    vertices = {(2*tile_row+row, 2*tile_column+column)
                for row, column in itertools.product(range(2), repeat=2)}
    removed = [edge for edge in matching if set(edge) & vertices]
    promoted = {vertex for edge in removed for vertex in edge if vertex in vertices}
    graph, _ = graph_record(*current)
    assert 1 <= len(removed) == len(promoted) <= 2
    for edge in removed:
        outside = next(vertex for vertex in edge if vertex not in vertices)
        outside_tile = (outside[0]//2)*(columns//2)+outside[1]//2
        assert graph['t'][outside_tile] == 2
    changed = (rows, columns, selected | promoted,
               [edge for edge in matching if edge not in removed])
    assert direct_check(*current) == direct_check(*changed)
    after, _ = graph_record(*changed)
    assert graph['E'] == after['E'] and graph['ends'] == after['ends']
    assert graph['r'] == after['r'] and graph['deg'] == after['deg']
    assert all(graph['h'][other] == after['h'][other] and graph['s'][other] == after['s'][other]
               for other in range(graph['N']) if other != tile)
    assert after['t'][tile] == 2 and after['s'][tile] == 0
    assert set(relay_tiles(changed)) == set(relay_tiles(current))-{tile}
    return changed


def control(current, name, order=None):
    before = witness_record(name, current)
    relays = relay_tiles(current)
    order = relays if order is None else list(order)
    assert set(order) == set(relays) and len(order) == len(relays)
    changed = current
    for tile in order:
        changed = saturate(changed, tile)
    after = witness_record(name+' normalized', changed)
    assert not relay_tiles(changed)
    assert before['objective'] == after['objective'] and before['q'] == after['q']
    expected_components = [component for component in before['components']
                           if not (len(component['tiles']) == 1 and component['tiles'][0] in relays)]
    assert after['components'] == expected_components
    for first, second in zip(before['tiles'], after['tiles']):
        assert first['degree']-2*first['capacity'] == second['degree']-2*second['capacity']
    return dict(name=name, order=order, removed_matching_edges=len(current[3])-len(changed[3]),
                before=before, after=after)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    fixtures = [(kind, configuration(kind)) for kind in ('neutral_down', 'neutral_up', 'neutral_both')]
    fixtures += [('all_neutral', neutral_completion()),
                 ('mixed_6x14', mixed_neutral_obstacle()),
                 ('mixed_6x20', wide_mixed_obstacle())]
    records = []
    for name, original in fixtures:
        for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, transpose, flip_rows, flip_columns)
            current = (*shape, selected, matching)
            record = control(current, name)
            record['symmetry'] = [transpose, flip_rows, flip_columns]
            records.append(record)
    original = neutral_completion()
    relays = relay_tiles(original)
    assert len(relays) == 3
    normalized = None
    for order in itertools.permutations(relays):
        record = control(original, 'all_neutral_order_check', order)
        key = (record['after']['selected'], record['after']['matching'])
        if normalized is None:
            normalized = key
        assert key == normalized
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/DIAGONAL_RELAY_NORMALIZATION.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_same_direction_capacity_donors.py', 'check_neutral_relay_obstacle.py',
        'check_cross_component_compensation.py', 'check_residual_corridors.py',
        'check_branching_interval_compensation.py', 'check_mixed_neutral_donors.py',
        'verify_grid_five_sixths.py', 'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', witnesses=records, order_checks=6,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite controls for a general normalization proof; no universal grid bound or new Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], symmetry_checks=len(records),
                          order_checks=6, relays_by_fixture={name:len(relay_tiles(current)) for name,current in fixtures})))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
