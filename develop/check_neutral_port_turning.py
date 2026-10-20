"""Reconstruct U port curves; distinguish geometric controls from complete fusions."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures, inspect_exact
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import positive_dimensions
from check_short_leg_defect_injection import inverse_affine
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def subtract(first, second):
    return first[0]-second[0], first[1]-second[1]


def determinant(first, second):
    return first[0]*second[1]-first[1]*second[0]


def port_data(module):
    phase = phase_of(module)
    if phase not in ('01', '10'):
        return None
    width, left, right, symmetry, offset = positive_dimensions(module)
    if phase == '01':
        reference = ([(row, 1) for row in range(left, -1, -1)]+
                     [(0, column) for column in range(2, width+1)]+
                     [(row, width) for row in range(1, right+1)])
    else:
        reference = [(0, column) for column in range(1, width+1)]
    path = [inverse_affine(point, symmetry, offset) for point in reference]
    assert set(path) <= module['endpoints'] and len(set(path)) == len(path)
    ports = []
    for endpoint, neighbor in ((path[0], path[1]), (path[-1], path[-2])):
        cells = vertices_of({tile_of(endpoint)})
        support = cells & module['selected']
        assert cells & module['endpoints'] == {endpoint} and len(support) == 1
        support = next(iter(support))
        blank = next(point for point in cells-{endpoint, support}
                     if sum(abs(value) for value in subtract(point, endpoint)) == 1)
        inward, exterior = subtract(neighbor, endpoint), subtract(blank, endpoint)
        assert subtract(support, endpoint) == tuple(-value for value in inward)
        chirality = determinant(inward, exterior)
        assert abs(chirality) == 1
        ports.append(dict(point=endpoint, support=support, blank=blank,
                          inward=inward, exterior=exterior, chirality=chirality))
    assert ports[0]['chirality'] == -ports[1]['chirality']
    turns = sum(determinant(subtract(middle, first), subtract(last, middle))
                for first, middle, last in zip(path, path[1:], path[2:]))
    assert turns == -2*ports[1]['chirality']*int(phase == '01')
    return dict(phase=phase, path=path, ports=ports)


def inspect_curves(current, modules, require_complete=True):
    exact = inspect_exact(current, modules) if require_complete else None
    network = combine(modules)
    endpoints, selected = network['endpoints'], network['selected']
    data = {owner: result for owner, module in enumerate(modules)
            if (result := port_data(module)) is not None}
    port_at = {port['point']: (owner, index) for owner, row in data.items()
               for index, port in enumerate(row['ports'])}
    contacts = {}
    active = {}
    for point, key in port_at.items():
        cells = vertices_of({tile_of(point)})
        if len(cells & endpoints) != 2 or len(cells & selected) != 1:
            continue
        other = next(iter((cells & endpoints)-{point}))
        if other not in port_at:
            continue
        port = data[key[0]]['ports'][key[1]]
        is_active = port['support'] not in endpoints and port['blank'] in endpoints
        is_passive = port['support'] in endpoints and port['blank'] not in endpoints
        assert is_active != is_passive
        contacts[key] = port_at[other]
        active[key] = int(is_active)
    forced01_points = []
    for key, target in contacts.items():
        assert contacts[target] == key and active[key]+active[target] == 1
        if active[key]:
            first = data[key[0]]['ports'][key[1]]
            second = data[target[0]]['ports'][target[1]]
            assert second['inward'] == first['exterior']
            assert second['exterior'] == tuple(-value for value in first['inward'])
            if data[key[0]]['phase'] == data[target[0]]['phase'] == '01':
                forced = tuple(first['point'][index]+first['inward'][index]+
                               first['exterior'][index] for index in (0, 1))
                predecessor = tuple(first['point'][index]+first['inward'][index]
                                    for index in (0, 1))
                assert forced in modules[key[0]]['selected'] & modules[target[0]]['selected']
                assert predecessor in modules[key[0]]['endpoints']
                assert forced not in modules[key[0]]['endpoints'] | modules[target[0]]['endpoints']
                forced01_points.append(forced)
                if require_complete:
                    assert forced in endpoints
    visited = set()
    cycles = []
    for root in data:
        if root in visited:
            continue
        component, pending = set(), [root]
        while pending:
            owner = pending.pop()
            if owner in component:
                continue
            component.add(owner)
            pending.extend(contacts[(owner, index)][0] for index in (0, 1)
                           if (owner, index) in contacts)
        visited.update(component)
        if not all((owner, index) in contacts for owner in component for index in (0, 1)):
            continue
        owner, entry = root, 0
        curve, signed_turn = [], 0
        while True:
            row = data[owner]
            path = row['path'] if entry == 0 else list(reversed(row['path']))
            curve.extend(path)
            exit_index = 1-entry
            chirality = row['ports'][exit_index]['chirality']
            signed_turn += chirality*(2*int(row['phase'] == '01')+2*active[owner, exit_index]-1)
            owner, entry = contacts[owner, exit_index]
            if (owner, entry) == (root, 0):
                break
        assert len(curve) == len(set(curve))
        assert len(component) % 2 == 0
        directions = [subtract(curve[(index+1) % len(curve)], point)
                      for index, point in enumerate(curve)]
        assert all(sum(abs(value) for value in direction) == 1 for direction in directions)
        turns = sum(determinant(directions[index-1], direction)
                    for index, direction in enumerate(directions))
        assert turns == -signed_turn and abs(turns) == 4
        first = sum(data[owner]['phase'] == '01' for owner in component)
        second = len(component)-first
        passive = sum(not active[owner, index] for owner in component
                      if data[owner]['phase'] == '10' for index in (0, 1))
        sinks = sum(data[owner]['phase'] == '01' and
                    active[owner, 0]+active[owner, 1] == 0 for owner in component)
        phase01_edges = sum(data[key[0]]['phase'] == data[target[0]]['phase'] == '01'
                            for key, target in contacts.items() if key[0] in component)//2
        assert first-second+2*passive >= 4 and sinks+passive >= 2
        if passive == 0:
            assert phase01_edges == first-second and phase01_edges >= 4
        cycles.append(dict(phase01=first, phase10=second, passive10=passive,
                           double_passive01=sinks, neutral01_edges=phase01_edges,
                           curve_vertices=len(curve), turns=turns))
    total_passive = sum(row['passive10'] for row in cycles)
    if require_complete:
        assert total_passive <= 2*exact['activated_positive']+exact['boundary_cost']
    assert sum(row['phase01']-row['phase10'] for row in cycles)+2*total_passive >= 4*len(cycles)
    return dict(eligible_sources=len(data), neutral_edges=len(contacts)//2,
                neutral01_forced_contacts=len(forced01_points),
                neutral01_forced_points=len(set(forced01_points)),
                closed_components=cycles)


def partial_sink_loop():
    modules = [transform_module(source(14, 4, 4), (False, False, False), (0, 1)),
               transform_module(source(6, 4, 4), (True, True, False), (3, 7)),
               transform_module(source(14, 4, 4), (False, True, False), (13, 1)),
               transform_module(source(6, 4, 4), (True, False, False), (3, 10))]
    network = combine(modules)
    assert len(network['endpoints']) == sum(len(module['endpoints']) for module in modules)
    violations = sorted(point for point in network['selected'] if
                        len(set(neighbors(point)) & (network['selected'] | network['endpoints'])) > 1)
    assert violations == [(3, 3), (3, 14), (10, 3), (10, 14)]
    curve = inspect_curves(None, modules, require_complete=False)
    assert len(curve['closed_components']) == 1
    component = curve['closed_components'][0]
    assert component['phase01'] == 4 and component['phase10'] == component['passive10'] == 0
    assert component['double_passive01'] == 2
    return dict(complete_feasible=False, endpoint_disjoint=True,
                support_violations=violations, port_graph=curve,
                interpretation='Sharp no-passive10 geometry only. Four mandatory supports are infeasible; not a complete fusion, AA realization or counterexample.')


def role_controls():
    count = 0
    phases = Counter()
    for width, left, right in ((6, 4, 4), (8, 6, 10), (14, 12, 4), (40, 30, 16)):
        for symmetry in itertools.product((False, True), repeat=3):
            for offset in itertools.product((0, 1), repeat=2):
                result = port_data(transform_module(source(width, left, right), symmetry, offset))
                if result:
                    count += 1
                    phases[result['phase']] += 1
    return dict(source_images=count, phases=dict(phases))


def signed_controls():
    counts = Counter()
    witnesses = []
    for size in (2, 4, 6, 8):
        signs = [(-1)**index for index in range(size)]
        for kinds in itertools.product((0, 1), repeat=size):
            for exits in itertools.product((-1, 1), repeat=size):
                counts['cyclic_words'] += 1
                active = [1+(exits[index]-exits[index-1])//2 for index in range(size)]
                turn = sum(sign*(2*kind+exit_value)
                           for sign, kind, exit_value in zip(signs, kinds, exits))
                rewritten = sum(sign*(amount if kind else amount-2)
                                for sign, kind, amount in zip(signs, kinds, active))
                assert turn == rewritten
                passive = sum(2-amount for kind, amount in zip(kinds, active) if not kind)
                sinks = sum(kind and amount == 0 for kind, amount in zip(kinds, active))
                first = sum(kinds)
                if abs(turn) != 4:
                    continue
                counts['turn_four_words'] += 1
                assert 2*first-size+2*passive >= 4
                assert sinks+passive >= 2
                if passive == 0:
                    counts['no_passive10_words'] += 1
                    assert 2*first-size >= 4 and sinks >= 2
                    if not witnesses:
                        witnesses.append(dict(kinds=kinds, exits=exits, active=active,
                                              turn=turn, geometry_realized=False))
    return dict(counts=counts, abstract_witnesses=witnesses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    physical = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_curves(current, moved)))
    summary = dict(complete_feasible_images=len(physical),
                   neutral_edges=sum(row['neutral_edges'] for row in physical),
                   neutral01_forced_contacts=sum(row['neutral01_forced_contacts'] for row in physical),
                   closed_components=sum(len(row['closed_components']) for row in physical))
    report = dict(status='PASS', summary=summary, roles=role_controls(),
                  signed=signed_controls(), physical=physical, partial_sink_loop=partial_sink_loop(),
                  scope='General written planar turning proof is separate. Physical counts report actual complete-fixture coverage only; abstract signed words are not geometric realizations. No general finite-source or grid closure.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', summary=summary, roles=report['roles'],
                          signed_counts=report['signed']['counts'])))


if __name__ == '__main__':
    main()
