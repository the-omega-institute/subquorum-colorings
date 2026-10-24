"""Check arbitrary endpoint-free gap capacities and blocked finite-radius access."""

import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data, physical, solve
from check_compensation_flow_geometry_frontier import pad_image
from check_exchange_terminal_nonunique import fixture, matching_orders
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_native_guard_compensation import force_matching
from check_one_sided_interval_allocation import allocate, independent_maximum
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import (
    cancel_pairs, direct_family, extended_ports, terminal_data, uniform_certificates,
)
from degree_three_fusion import occupied_bands
from rotor_networks import rotor


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def blocked_family(width, depth):
    assert width >= 6 and width % 2 == 0 and depth >= 1
    base = direct_family(width, 4)
    added = set()
    for row, opposite in [(5, 4), (width+4, width+5)]:
        for step in range(1, depth+1):
            selected_row = opposite if step % 2 else row
            added.update([(selected_row, 2-step), (selected_row, 8+step)])
    assert not added & base[2] and len(added) == 4*depth
    shift = depth+2
    move = lambda point: (point[0], point[1]+shift)
    current = (width+12, 2*depth+24, {move(point) for point in base[2] | added},
               [tuple(move(point) for point in pair) for pair in base[3]])
    bands = [[((row, column), (row+1, column)) for column in range(2, 2*depth+12)]
             for row in range(4, width+5, 2)]
    return current, bands, added, move


def gap_access(current, bands, totals):
    original, labels, intervals, interval_owner, kinds, pairs, direct = terminal_data(current, bands)
    marked = {interval_owner[band, column] for band in range(len(bands))
              for column in (0, len(bands[band])-1) if labels[band][column] == ('B', 'B')}
    assert len(marked) == original['boundary_budget']
    resources = set(range(len(intervals)))-marked
    access = {point: set() for point in kinds if kinds[point] == 'TP'}
    distances = {point: {} for point in access}
    physical_owners, gaps = defaultdict(set), []
    locations = {point: (band, column) for band, columns in enumerate(bands)
                 for column, cells in enumerate(columns) for point in cells if point in kinds}
    for band, columns in enumerate(bands):
        position = 0
        while position < len(columns):
            if 'P' in labels[band][position]:
                position += 1
                continue
            first = position
            while position < len(columns) and 'P' not in labels[band][position]:
                position += 1
            last = position-1
            units = {interval_owner[band, column] for column in range(first, last+1)
                     if (band, column) in interval_owner}
            for resource in units:
                assert intervals[resource]['band'] == band
                assert first <= intervals[resource]['first'] <= intervals[resource]['last'] <= last
            cells = {point for column in columns[first:last+1] for point in column}
            assert len(cells)//2-len(current[2] & cells) == len(units)
            remaining = units-marked
            totals['tt_columns_in_gaps'] += sum(labels[band][column] == ('T', 'T')
                                               for column in range(first, last+1))
            candidates = []
            for boundary in (first-1, last+1):
                if not 0 <= boundary < len(columns):
                    continue
                terminals = [point for point in columns[boundary] if kinds.get(point) == 'TP']
                assert len(terminals) <= 1
                candidates += terminals
                for point in terminals:
                    access[point].update(remaining)
                    for resource in remaining:
                        physical_owners[resource].add(point)
                        target = intervals[resource]
                        column = locations[point][1]
                        distance = min(abs(column-target['first']), abs(column-target['last']))
                        distances[point][resource] = distance
            assert len(candidates) <= 2
            totals['endpoint_free_gaps'] += 1
            totals['gap_unit_resources'] += len(remaining)
            gaps.append(dict(band=band, first=first, last=last,
                             raw_capacity=len(units), reserved=len(units & marked),
                             available_capacity=len(remaining), candidate_terminals=len(candidates)))
    assert all(len(users) <= 2 for users in physical_owners.values())
    old_access = extended_ports(current, bands, labels, intervals, interval_owner,
                                kinds, direct, Counter())
    assert all({interval_owner[port] for port in old_access[point]} & resources <= access[point]
               for point in access)
    totals['gap_adapters'] += 1
    return original, kinds, pairs, resources, access, distances, gaps


def allocation_control(current, bands, fixed, totals):
    original, kinds, pairs, resources, access, _, _ = gap_access(current, bands, totals)
    reduced, inventory, _ = cancel_pairs(kinds, pairs, fixed, Counter())
    alphas = [pair for pair in reduced if all(kinds[point] == 'TP' for point in pair)]
    incidence = {resource: {index for index, pair in enumerate(alphas)
                            if any(resource in access[point] for point in pair)}
                 for resource in resources}
    assert all(len(owners) <= 2 for owners in incidence.values())
    result = allocate(len(alphas), incidence)
    paid = len(result['assignment'])
    assert paid == independent_maximum(len(alphas), incidence)
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*(
        len(resources)-paid+inventory['BP', 'BP']-len(result['deficient']))
    totals['exact_gap_allocation_controls'] += 1


def geometry_controls(totals):
    base = fixture()
    fixtures = [('bent', (*base[:3], list(record['matching'])))
                for record in matching_orders()]
    module = rotor()
    fixtures += [('rotor', (6, 6, module['selected'], module['matching'])),
                 ('occupied', occupied_bands(6)[0]),
                 ('tt_forest', (8, 8, {(2, 2), (3, 2)}, []))]
    for (name, current), symmetry, offset in itertools.product(
            fixtures, itertools.product((False, True), repeat=3),
            itertools.product((2, 3), repeat=2)):
        current = pad_image(current, symmetry, offset)
        direct_check(*current)
        assert frozen_certificate(current)[0] == {point for pair in current[3] for point in pair}
        bands = whole_bands(current)
        allocation_control(current, bands, [], totals)
        _, _, _, _, kinds, pairs, _ = terminal_data(current, bands)
        candidates = [(first, second) for first in kinds for second in kinds
                      if kinds[first] == 'TP' and kinds[second] == 'BP'
                      and first[0] == second[0] and abs(first[1]-second[1]) == 1]
        for link in candidates:
            allocation_control(current, bands, [link], totals)
            totals['fixed_single_link_gap_controls'] += 1
        totals['gap_geometry_'+name] += 1
    first = direct_family(6, 4)
    move = lambda point: (point[0], point[1]+9)
    current = (18, 30, first[2] | {move(point) for point in first[2]},
               first[3]+[tuple(move(point) for point in pair) for pair in first[3]])
    direct_check(*current)
    assert frozen_certificate(current)[0] == {point for pair in current[3] for point in pair}
    bands = whole_bands(current)
    _, _, _, _, access, _, gaps = gap_access(current, bands, totals)
    gap = next(gap for gap in gaps if gap['band'] == 2 and gap['first'] == 8)
    assert gap['available_capacity'] == 2 and gap['candidate_terminals'] == 2
    assert len(access[(5, 7)] & access[(5, 12)]) == 2
    allocation_control(current, bands, [], totals)
    totals['two_port_capacity_two_gap_controls'] += 1
    assert totals['tt_columns_in_gaps'] > 0


def control(width, depth, totals):
    current, bands, added, move = blocked_family(width, depth)
    direct_check(*current)
    assert all(not any(abs(first[0]-second[0])+abs(first[1]-second[1]) == 1
                       for second in current[2] | {point for pair in current[3] for point in pair}
                       if second != move(point)) for point in added for first in [move(point)])
    force_matching(current, totals)
    uniform_certificates(direct_family(width, 4), width, 4, Counter())
    frozen, _ = frozen_certificate(current)
    assert frozen == {point for pair in current[3] for point in pair}
    old = physical(current, bands, [], totals)
    assert old['value'] == 0 and old['deficit'] == 1 and old['cut'] == []
    original, kinds, pairs, resources, access, distances, gaps = gap_access(current, bands, totals)
    assert (original['alpha'], original['beta'], original['gamma']) == (1, 0, 5)
    expected = 3*width-9+(width-2)*depth
    assert len(current[2]) == 13+4*depth and len(current[3]) == width+4
    assert original['surplus_twice']-2*original['boundary_budget'] == 2*expected
    assert len(resources) == expected+1
    links = [(first, second) for first in kinds for second in kinds
             if kinds[first] == 'TP' and kinds[second] == 'BP'
             and first[0] == second[0] and abs(first[1]-second[1]) == 1]
    owners, alphas, _, _ = owner_data(kinds, pairs)
    reachable_tips = {move((row, column)) for row in (5, width+4) for column in (3, 5, 7)}
    assert all(kinds[point] == 'TP' for point in reachable_tips)
    assert min(distance for point in reachable_tips for distance in distances[point].values()) == depth+2
    bounded = {point: {resource for resource in choices if distances[point][resource] < depth+2}
               for point, choices in access.items()}
    limited = solve(kinds, pairs, links, bounded, resources)
    assert limited['value'] == 0 and limited['cut'] == []
    full = solve(kinds, pairs, links, access, resources)
    assert full['value'] == 1 and full['cost'] == 0
    initial_alpha = next(iter(alphas))
    assert full['routes'][0][0] == ('source', initial_alpha)
    assert all(owners[point] in alphas for point, _ in full['payments'])
    totals['fully_frozen_blocked_families'] += 1
    totals['old_unrestricted_flow_deficits'] += 1
    totals['finite_radius_obstructions'] += 1
    totals['zero_link_gap_repairs'] += 1
    return dict(width=width, depth=depth, selected=len(current[2]), matching=len(current[3]),
                packet_shape=[width+2, 2*depth+10], margin=expected,
                unmarked_resources=len(resources), old_maximum=old['value'],
                old_deficit=old['deficit'], minimum_gap_distance=depth+2,
                new_maximum=full['value'], minimum_new_links=full['cost'],
                near_gap_capacities=[gap for gap in gaps if gap['candidate_terminals']])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    for width, depth in itertools.product((6, 8, 12, 20), range(1, 33)):
        record = control(width, depth, totals)
        if (width, depth) in ((6, 1), (8, 8), (20, 32)):
            examples.append(record)
    geometry_controls(totals)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals), examples=examples,
        scope='Finite controls for the written arbitrary-length fully frozen unrouteable family '
        'under direct/single-cap access, the failure of every fixed endpoint-free access radius, '
        'and zero-link compensation via exact capacities of maximal endpoint-free gaps. '
        'No universal grid inequality is asserted.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
