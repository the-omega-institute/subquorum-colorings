"""Check distinct adjacent BP terminals and closed freezing obstructions."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors, occupied_degrees
from check_elbow_sources import elbow
from check_even_bridge_support_completion import endpoints_of
from check_exchange_terminal_nonunique import fixture, graft
from check_interval_connector_cycles_and_missing_ports import stack, whole_bands
from check_neutral_pair_donor_saturation import neutral_pair
from check_neutral_portal_strip_compensation import image_map
from check_pp_path_terminal_ledger import inspect as inspect_paths
from check_promotion_cores import degree_four_patch, frozen_certificate, tight_diamond
from check_receiver_overlap_and_pp_source_collision import forest_intervals
from check_residual_corridors import direct_check, transformed
from degree_three_fusion import occupied_bands


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(current, bands, totals, require_frozen):
    direct_check(*current)
    record = inspect_paths(current, bands, Counter(), True)
    assert record['cuts'] == 0
    labels, _, _ = forest_intervals(current, bands)
    endpoints = endpoints_of(current)
    mate = {first: second for edge in current[3] for first, second in (edge, edge[::-1])}
    frozen, layers = frozen_certificate(current)
    assert (frozen == endpoints) == require_frozen
    missing, location = set(), {}
    for path in record['components']:
        if path['kind'] != ['TP', 'TP']:
            continue
        for band, column in (path['nodes'][0], path['nodes'][-1]):
            if not any(labels[band][adjacent] == ('B', 'B') for adjacent in (column-1, column+1)):
                endpoint = next(point for point in bands[band][column] if point in endpoints)
                missing.add(endpoint)
                location[endpoint] = band, column, bands[band][column].index(endpoint)
    adjacency = defaultdict(set)
    for endpoint in missing:
        band, column, position = location[endpoint]
        for adjacent in (column-1, column+1):
            other = bands[band][adjacent][position]
            if other in endpoints:
                assert other not in missing
                assert labels[band][adjacent] == ('B', 'P')
                adjacency[endpoint].add(other)
                adjacency[other].add(endpoint)
    remaining = missing | set(adjacency)
    assignments, bad_sets = {}, []
    while remaining:
        start = min(remaining)
        reached, pending = {start}, [start]
        while pending:
            node = pending.pop()
            assert len(adjacency[node]) <= 2
            for other in adjacency[node]-reached:
                assert abs(node[0]-other[0])+abs(node[1]-other[1]) == 1
                reached.add(other)
                pending.append(other)
        remaining -= reached
        ends = [node for node in reached if len(adjacency[node]) <= 1]
        assert len(ends) == (1 if len(reached) == 1 else 2)
        start = min(ends, key=lambda node: (node in missing, node))
        trace, previous, node = [], None, start
        while True:
            trace.append(node)
            following = adjacency[node]-{previous}
            if not following:
                break
            assert len(following) == 1
            previous, node = node, next(iter(following))
        assert set(trace) == reached and len(trace) == len(reached)
        for index, node in enumerate(trace):
            if node in missing and index:
                assert trace[index-1] not in missing
                assignments[node] = trace[index-1]
        if all(node in missing for node in ends):
            demand = reached & missing
            bp = reached-missing
            blocked = bp | {mate[endpoint] for endpoint in demand}
            assert len(demand) == len(bp)+1 and blocked
            first = next(iter(demand))
            direction = mate[first][0]-first[0], mate[first][1]-first[1]
            for endpoint in bp:
                assert mate[endpoint] == (endpoint[0]+direction[0], endpoint[1]+direction[1])
            for endpoint in blocked:
                nonmate = set(neighbors(endpoint)) & (current[2] | endpoints)-{mate[endpoint]}
                outside = {other for other in nonmate
                           if other in current[2] or mate[other] not in blocked}
                assert len(outside) <= (0 if endpoint in bp else 1)
            assert not frozen & blocked
            bad_sets.append(sorted(blocked))
    assert len(set(assignments.values())) == len(assignments)
    assert all(other in adjacency[endpoint] for endpoint, other in assignments.items())
    assert len(assignments) == len(missing)-len(bad_sets)
    independent = {}

    def augment(endpoint, visited):
        for other in adjacency[endpoint]-visited:
            visited.add(other)
            if other not in independent or augment(independent[other], visited):
                independent[other] = endpoint
                return True
        return False

    for endpoint in sorted(missing):
        augment(endpoint, set())
    assert len(independent) == len(assignments)
    if require_frozen:
        assert not bad_sets and len(assignments) == len(missing)
    totals['models'] += 1
    totals['fully_frozen_models'] += require_frozen
    totals['missing_alpha_terminals'] += len(missing)
    totals['distinct_adjacent_bp_assignments'] += len(assignments)
    totals['nonempty_frozen_injections'] += require_frozen and bool(missing)
    totals['closed_dependency_obstructions'] += len(bad_sets)
    return dict(missing=sorted(missing), assignment=sorted(assignments.items()),
                frozen_count=len(frozen), endpoint_count=len(endpoints),
                frozen_layers=len(layers), bad_closed_sets=bad_sets, beta=record['beta'])


def padded(current):
    move = lambda point: (point[0]+2, point[1]+2)
    return current[0]+4, current[1]+4, {move(point) for point in current[2]}, [
        tuple(move(point) for point in edge) for edge in current[3]]


def nonfrozen_obstruction():
    selected = {(row, column) for row in (0, 3) for column in (2, 4, 6)}
    selected |= {(1, 1), (1, 7)}
    return 4, 10, selected, [((1, column), (2, column)) for column in range(2, 7)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    for width, height, kind in itertools.product(range(6, 31, 2), range(4, 21, 2),
                                                 ('missing', 'cycle', 'collision')):
        current = stack(width, height, [kind])
        record = inspect(current, whole_bands(current), totals, True)
        if kind == 'missing':
            assert len(record['missing']) == len(record['assignment']) == 2 and record['beta'] == 0
        totals['parameter_triples'] += 1
        if width == 6 and height == 4:
            examples.append(dict(kind=kind, **record))
    for cycles, collisions, missing in itertools.product(range(3), repeat=3):
        if not cycles+collisions+missing:
            continue
        current = stack(6, 4, ['cycle']*cycles+['collision']*collisions+['missing']*missing)
        record = inspect(current, whole_bands(current), totals, True)
        assert len(record['assignment']) == 2*missing
        totals['mixed_inventory_controls'] += 1
    fixtures = [neutral_pair(6, 4)[0], degree_four_patch(), tight_diamond()[0],
                elbow(6, 4), graft(6, 4), occupied_bands(6)[0], fixture()]
    fixtures = [padded(current) for current in fixtures]
    fixtures += [stack(6, 4, ['missing']), nonfrozen_obstruction()]
    for current in fixtures:
        is_frozen = frozen_certificate(current)[0] == endpoints_of(current)
        bands = whole_bands(current)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            move = image_map(*current[:2], symmetry)
            image_bands = [[tuple(move(point) for point in column) for column in columns]
                           for columns in bands]
            inspect((*shape, selected, matching), image_bands, totals, is_frozen)
            totals['fixture_symmetry_controls'] += 1
    current = nonfrozen_obstruction()
    assert min(occupied_degrees(current).values()) == 3
    record = inspect(current, whole_bands(current), totals, False)
    assert record['frozen_count'] == 2 and record['endpoint_count'] == 10
    assert len(record['missing']) == 4 and len(record['assignment']) == 3
    assert record['bad_closed_sets'] == [[(1, 3), (1, 5), (2, 2), (2, 4), (2, 6)]]
    examples.append(dict(kind='degree-three-but-not-frozen', shape=current[:2],
                         selected=sorted(current[2]), matching=current[3], **record))
    report = dict(status='PASS', controls=dict(totals), examples=examples,
                  scope='Uniform written injection into distinct BP terminals under complete freezing; '
                        'closed dependency obstruction and explicit failure under degree>=3 alone. '
                        'An injection into BP terminals is not an injection into BP--BP unit resources.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', controls=dict(totals))))


if __name__ == '__main__':
    main()
