"""Reconstruct closed neutral contacts and their distinct physical receivers."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures
from check_minus_one_tip_obstructions import source
from check_neutral_port_turning import port_data
from check_neutral_support_injection import inspect_joint
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def add(first, second):
    return tuple(value+other for value, other in zip(first, second))


def closed_contacts(modules):
    network = combine(modules)
    endpoints, selected = network['endpoints'], network['selected']
    data = {owner: record for owner, module in enumerate(modules)
            if (record := port_data(module)) is not None}
    port_at = {port['point']: (owner, index) for owner, record in data.items()
               for index, port in enumerate(record['ports'])}
    contacts, active = {}, {}
    for point, key in port_at.items():
        cells = vertices_of({tile_of(point)})
        if len(cells & endpoints) != 2 or len(cells & selected) != 1:
            continue
        other = next(iter((cells & endpoints)-{point}))
        if other not in port_at:
            continue
        contacts[key] = port_at[other]
        active[key] = data[key[0]]['ports'][key[1]]['blank'] in endpoints
    visited, closed = set(), set()
    component_count = 0
    for root in data:
        if root in visited:
            continue
        component, pending = set(), [root]
        while pending:
            owner = pending.pop()
            if owner in component:
                continue
            component.add(owner)
            pending.extend(contacts[owner, index][0] for index in (0, 1)
                           if (owner, index) in contacts)
        visited.update(component)
        if all((owner, index) in contacts for owner in component for index in (0, 1)):
            closed.update(component)
            component_count += 1
    edges = []
    for key, target in contacts.items():
        if key[0] not in closed or not active[key]:
            continue
        assert not active[target] and contacts[target] == key
        if data[key[0]]['phase'] == data[target[0]]['phase'] == '01':
            port = data[key[0]]['ports'][key[1]]
            forced = add(add(port['point'], port['inward']), port['exterior'])
            pair = {add(port['point'], port['inward']),
                    add(add(port['point'], port['inward']), port['inward'])}
            edges.append(dict(owner=key[0], port=key[1], forced=forced,
                              next=add(forced, port['inward']), pair=pair,
                              tile=tile_of(forced)))
    return data, closed, contacts, edges, component_count


def inspect_closed(modules, complete=True):
    network = combine(modules)
    endpoints = network['endpoints']
    data, closed, contacts, edges, components = closed_contacts(modules)
    closed01 = {point for owner in closed if data[owner]['phase'] == '01'
                for point in modules[owner]['endpoints']}
    assert len({edge['tile'] for edge in edges}) == len(edges)
    positions, prescribed = set(), set()
    stops = 0
    for edge in edges:
        cells = vertices_of({edge['tile']})
        assert cells & modules[edge['owner']]['endpoints'] == edge['pair']
        assert cells-edge['pair'] == {edge['forced'], edge['next']}
        assert not (cells-edge['pair']) & closed01
        assert not prescribed & (cells-edge['pair'])
        prescribed.update(cells-edge['pair'])
        if complete:
            assert edge['forced'] in endpoints
            assert len(cells & endpoints) in (3, 4)
            stops += int(not cells <= endpoints)
            positions.update((cells & endpoints)-edge['pair'])
    phase01 = sum(data[owner]['phase'] == '01' for owner in closed)
    phase10 = len(closed)-phase01
    edge10 = sum(key < target and key[0] in closed and
                 data[key[0]]['phase'] == data[target[0]]['phase'] == '10'
                 for key, target in contacts.items())
    mixed = sum(key < target and key[0] in closed and
                data[key[0]]['phase'] != data[target[0]]['phase']
                for key, target in contacts.items())
    assert 2*phase01 == 2*len(edges)+mixed
    assert 2*phase10 == 2*edge10+mixed
    assert len(edges)-edge10 == phase01-phase10
    if complete:
        assert len(positions)+stops == 2*len(edges)
    return dict(complete_feasible=complete, closed_components=components,
                closed_phase01=phase01, closed_phase10=phase10,
                closed01_contacts=len(edges), closed10_contacts=edge10,
                distinct_receivers=len(edges), actual_outside_positions=len(positions),
                prescribed_opposite_positions=len(prescribed), nonfull_stops=stops)


def catalogue_controls():
    adjacent = [pair for pair in itertools.combinations(range(4), 2)
                if sum(abs(first-second) for first, second in
                       zip(divmod(pair[0], 2), divmod(pair[1], 2))) == 1]
    assert [pair for pair in adjacent if not set(pair) & {0, 2}] == [(1, 3)]
    counts = Counter()
    images = 0
    for dimensions in ((6, 4, 4), (8, 6, 12), (14, 12, 4), (40, 30, 16)):
        for _, _, _, _, modules in phase_images([source(*dimensions)]):
            module = modules[0]
            if phase_of(module) != '01':
                continue
            images += 1
            for tile in module['receiver']:
                cells = vertices_of({tile})
                profile = len(cells & module['endpoints']), len(cells & module['selected'])
                assert profile in ((1, 1), (2, 1), (4, 0))
                counts[profile] += 1
    return dict(adjacent_pairs=adjacent, phase01_source_images=images,
                profile_counts=[dict(profile=profile, count=count)
                                for profile, count in sorted(counts.items())])


def partial_control():
    modules = [transform_module(source(14, 4, 4), (False, False, False), (0, 1)),
               transform_module(source(6, 4, 4), (True, True, False), (3, 7)),
               transform_module(source(14, 4, 4), (False, True, False), (13, 1)),
               transform_module(source(6, 4, 4), (True, False, False), (3, 10))]
    result = inspect_closed(modules, complete=False)
    assert result['closed01_contacts'] == result['distinct_receivers'] == 4
    assert result['prescribed_opposite_positions'] == 8
    assert result['actual_outside_positions'] == 0
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    physical = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            joint = inspect_joint(current, moved)
            row = inspect_closed(moved)
            assert joint['counted_B']+row['nonfull_stops'] <= 2*joint['activation']+joint['boundary']
            assert 2*row['closed01_contacts']+joint['counted_B'] <= (
                row['actual_outside_positions']+2*joint['activation']+joint['boundary'])
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase, **row))
    summary = dict(complete_feasible_images=len(physical),
                   closed_components=sum(row['closed_components'] for row in physical),
                   complete_closed01_contacts=sum(row['closed01_contacts'] for row in physical),
                   complete_full_forced_receivers=sum(row['distinct_receivers']-row['nonfull_stops']
                                                      for row in physical),
                   complete_AA_contact_coverage=0)
    report = dict(status='PASS', summary=summary, catalogue=catalogue_controls(),
                  partial_polygon=partial_control(), physical=physical,
                  scope='Written arbitrary-source receiver injection and outside-endpoint proof; finite catalogue/physical controls only. Complete closed01-contact/full-receiver/AA coverage is zero. Partial polygon has infeasible mandatory supports. No fresh reserve or general grid closure.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', summary=summary)))


if __name__ == '__main__':
    main()
