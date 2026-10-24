"""Distinct forced supports and joint regular/irregular pair reservations."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import inspect_occurrences, phase_of
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures, inspect_exact
from check_minus_one_joint_compensation import contained
from check_neutral_port_turning import port_data
from check_passive_corner_transfers import inspect_transfers
from check_short_leg_defect_injection import defect_tiles
from check_support_chain_compensation import exterior_chain
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def move(point, direction, amount=1):
    return tuple(value+amount*delta for value, delta in zip(point, direction))


def exact_orientation_controls():
    directions = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    frames = [(first, second) for first, second in itertools.product(directions, repeat=2)
              if sum(value*other for value, other in zip(first, second)) == 0]
    result = []
    for first, second in frames:
        active = [move(tuple(-value-other for value, other in zip(first, second)), first, index)
                  for index in range(3)]
        survivors = []
        witnesses = []
        for other_first, other_second in frames:
            other_active = [move(tuple(-value-other for value, other in zip(other_first, other_second)),
                                 other_first, index) for index in range(3)]
            other_passive = [move(tuple(-value for value in other_first), other_second, index)
                             for index in range(2)]
            collisions = [(point, 'active') for point in active
                          if point in other_active and first != other_first]
            collisions += [(point, 'passive') for point in active
                           if point in other_passive and first != other_second]
            if collisions:
                witnesses.append(dict(other=(other_first, other_second), witness=collisions[0]))
            else:
                survivors.append((other_first, other_second))
        assert survivors == [(first, second)]
        result.append(dict(frame=(first, second), excluded=witnesses, survivors=survivors))
    return result


def inspect_joint(current, modules):
    exact = inspect_exact(current, modules)
    caps = inspect_occurrences(modules)
    transfers = inspect_transfers(current, modules)
    network = combine(modules)
    endpoints, selected = network['endpoints'], network['selected']
    owner_at = {point: owner for owner, module in enumerate(modules) for point in module['endpoints']}
    phases = [phase_of(module) for module in modules]
    data = {owner: row for owner, module in enumerate(modules)
            if (row := port_data(module)) is not None}
    port_at = {port['point']: (owner, index) for owner, row in data.items()
               for index, port in enumerate(row['ports'])}
    contacts = {}
    active_contacts = []
    for point, key in port_at.items():
        cells = vertices_of({tile_of(point)})
        if len(cells & endpoints) != 2 or len(cells & selected) != 1:
            continue
        target = next(iter((cells & endpoints)-{point}))
        if target not in port_at:
            continue
        contacts[key] = port_at[target]
        port = data[key[0]]['ports'][key[1]]
        if port['blank'] in endpoints and phases[key[0]] == phases[port_at[target][0]] == '01':
            active_contacts.append(key)
    closed_owners, visited = set(), set()
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
        if all((owner, index) in contacts for owner in component for index in (0, 1)):
            closed_owners.update(component)
    closed01_endpoints = {point for owner in closed_owners if phases[owner] == '01'
                          for point in modules[owner]['endpoints']}
    defects = defect_tiles(modules, endpoints)
    forced_points, stop_tiles, forced_types = set(), set(), Counter()
    forced_pool_points = set()
    for owner, index in active_contacts:
        port = data[owner]['ports'][index]
        partner = contacts[owner, index][0]
        predecessor = move(port['point'], port['inward'])
        second_predecessor = move(port['point'], port['inward'], 2)
        forced = move(predecessor, port['exterior'])
        assert forced in modules[owner]['selected'] & modules[partner]['selected']
        assert forced in endpoints and forced not in modules[owner]['endpoints'] | modules[partner]['endpoints']
        assert forced not in forced_points and forced not in closed01_endpoints
        forced_points.add(forced)
        forced_types[phases[owner_at[forced]]] += 1
        cells = vertices_of({tile_of(forced)})
        assert cells & modules[owner]['endpoints'] == {predecessor, second_predecessor}
        assert cells & modules[owner]['selected'] == {forced}
        if len(cells & modules[owner_at[forced]]['endpoints']) == 1 and phases[owner_at[forced]] in ('01', '10'):
            forced_pool_points.add(forced)
        if not cells <= endpoints:
            tile = tile_of(forced)
            assert len(cells & endpoints) == 3 and not cells & selected
            assert defects[tile] == 'L3' and tile not in stop_tiles
            stop_tiles.add(tile)
    direct = {tuple(row['tile']) for row in transfers['records'] if row['kind'] == 'direct_H'}
    routed = set()
    for row in transfers['records']:
        if row['kind'] == 'unactivated_corner_H':
            stop = exterior_chain(row['positive_owner'], bool(row['leg']), modules, endpoints)
            routed.add(tuple(stop['tile']))
    assert not stop_tiles & (direct | routed)
    assert len(stop_tiles)+len(direct)+len(routed) <= exact['boundary_cost']
    assert transfers['counted']+len(stop_tiles) <= 2*exact['activated_positive']+exact['boundary_cost']
    pool = set(port_at)
    irregular, regular = set(), set()
    negative_caps = set()
    for point in pool:
        cells = vertices_of({tile_of(point)})
        foreign_pairs = [module for module in modules if len(cells & module['endpoints']) == 2]
        assert len(foreign_pairs) <= 1
        if foreign_pairs:
            support = len(cells & foreign_pairs[0]['selected'])
            assert support in (0, 1)
            (regular if support else irregular).add(point)
    for owner, module in enumerate(modules):
        if phases[owner] != '11':
            continue
        for tile in module['receiver']:
            cells = vertices_of({tile})
            if len(cells & module['endpoints']) == 3 and cells <= endpoints:
                point = next(iter(cells-module['endpoints']))
                if phases[owner_at[point]] in ('01', '10'):
                    negative_caps.add(point)
    assert len(irregular) == caps['pair_reserved']
    assert len(negative_caps) == caps['negative_cap_fillers']
    assert not irregular & regular
    all_pairs = irregular | regular
    assert not negative_caps & all_pairs and negative_caps | all_pairs <= pool
    assert forced_pool_points <= regular
    unused = len(pool-negative_caps-all_pairs)
    assert (len(negative_caps)+len(all_pairs)+unused ==
            2*(caps['phase01']+caps['phase10']))
    exact_expansion = (2*(caps['phase11']-caps['phase01']-caps['phase10'])+len(all_pairs)+
                       caps['activation']-caps['positive_cap_fillers']+
                       exact['unpaired_rotor_activation']+exact['boundary_cost']+unused)
    assert exact_expansion == 2*exact['event_reserve']
    return dict(irregular_pair_slots=len(irregular), regular_pair_slots=len(regular),
                all_pair_slots=len(all_pairs), unused_singletons=unused,
                forced_contacts=len(active_contacts), forced_distinct_points=len(forced_points),
                forced_owner_phases=dict(forced_types), regular_stops=len(stop_tiles),
                forced_Pneg_reserved=len(forced_pool_points), counted_B=transfers['counted'],
                boundary=exact['boundary_cost'], activation=caps['activation'],
                negative_cap_fillers=len(negative_caps), complete_feasible=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    physical, cap_fixture, paired_fixture = [], None, None
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            row = inspect_joint(current, moved)
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase, **row))
            if row['negative_cap_fillers'] and cap_fixture is None:
                cap_fixture = moved
            if inspect_occurrences(moved)['paired'] and paired_fixture is None:
                paired_fixture = moved
    separated = cap_fixture+[transform_module(module, (False, False, False), (0, 1000))
                             for module in paired_fixture]
    current, moved = contained(separated)
    physical.append(dict(fixture='separated_caps_and_paired', **inspect_joint(current, moved)))
    summary = dict(complete_feasible_images=len(physical),
                   irregular_pair_slots=sum(row['irregular_pair_slots'] for row in physical),
                   regular_pair_slots=sum(row['regular_pair_slots'] for row in physical),
                   strictly_stronger_images=sum(row['regular_pair_slots'] > 0 for row in physical),
                   forced_contacts=sum(row['forced_contacts'] for row in physical),
                   forced_distinct_points=sum(row['forced_distinct_points'] for row in physical),
                   regular_stops=sum(row['regular_stops'] for row in physical),
                   forced_Pneg_reserved=sum(row['forced_Pneg_reserved'] for row in physical),
                   complete_AA_fixture_coverage=0)
    result = dict(status='PASS', summary=summary, exact_orientation_controls=exact_orientation_controls(),
                  physical=physical,
                  scope='General local direction-tag injection and exact-pair-versus-cap exclusion have written proofs with scoped Lean checks. Controls verify real complete unions, forced owner exclusion and simultaneous H stops. No general AA closure, fresh reserve from endpoints/full tiles, or grid equality.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', summary=summary)))


if __name__ == '__main__':
    main()
