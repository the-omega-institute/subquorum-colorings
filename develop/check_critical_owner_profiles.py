"""Critical original profiles and jointly reserved H/Z0 stop controls."""

import argparse
import itertools
import json
from collections import Counter
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_activated_singleton_budget import rotor_pairs
from check_cap_continuation_budget import phase_of
from check_closed_neutral_receivers import closed_contacts
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_critical_closed_owner_counterexample import modules as six_sources
from check_critical_closed_owner_counterexample import canonical
from check_critical_phase01_bar_returns import family
from check_exact_event_reserve import fixtures, inspect_exact
from check_full_neutral_receivers import add, scale
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import positive_dimensions
from check_passive_corner_transfers import inspect_transfers
from check_support_chain_compensation import exterior_chain
from rotor_networks import affine, combine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


SQUARE = {(0, 0), (1, 0), (0, 1), (1, 1)}


def anchored_images(base):
    for symmetry in itertools.product((False, True), repeat=3):
        for anchor in base['endpoints']:
            offset = tuple(-value for value in affine(anchor, symmetry))
            yield anchor, transform_module(base, symmetry, offset)


def local_U_controls():
    counts = Counter()
    for dimensions in itertools.product((6, 8, 14, 40), (4, 6, 12), (4, 8, 20)):
        base = source(*dimensions)
        for anchor, module in anchored_images(base):
            counts['U_endpoint_images'] += 1
            own = module['endpoints']
            if own & {(-1, 0), (0, -1)}:
                continue
            counts['two_blocker_survivors'] += 1
            phase = phase_of(module)
            assert phase != '00'
            profile, support = own & SQUARE, module['selected'] & SQUARE
            if phase == '01':
                assert anchor in {(0, 1), (0, dimensions[0])}
                assert profile == SQUARE and not support
            else:
                assert phase in {'10', '11'}
                assert anchor in {(dimensions[1], 1), (dimensions[2], dimensions[0])}
                assert profile in ({(0, 0), (1, 0)}, {(0, 0), (0, 1)})
                expected = ({(0, 1)} if (1, 0) in profile else {(1, 0)})
                assert support == (expected if phase == '10' else {(1, 1)})
            for clearance in (1, 3, 5, 9, 19):
                wall = {(-1, column) for column in range(clearance+1)}
                wall.update((row, clearance) for row in (0, 1, 2))
                if own & wall:
                    continue
                counts['complete_bar_wall_survivors_'+phase] += 1
                if phase == '10':
                    assert profile == {(0, 0), (1, 0)} and support == {(0, 1)}
    return dict(counts)


def exact_rotor_controls():
    images = {frozenset(module['endpoints']): module for _, module in anchored_images(rotor())}
    assert len(images) == 16
    local = [module for module in images.values()
             if not module['endpoints'] & {(-1, 0), (0, -1)}]
    assert len(local) == 4
    counts = Counter(exact_rotor_roots=16, two_blocker_survivors=4)
    for module in local:
        assert module['charge'] == 0
        assert len(module['endpoints'] & SQUARE) in (2, 3)
        assert len(set(neighbors((0, 0))) & module['endpoints']) == 1
        for clearance in (1, 3, 5, 9):
            wall = {(-1, column) for column in range(clearance+1)}
            wall.update((row, clearance) for row in (0, 1, 2))
            if module['endpoints'] & wall:
                continue
            assert clearance >= 3
            profile = module['endpoints'] & SQUARE
            if len(profile) == 2:
                assert profile == {(0, 0), (1, 0)}
                assert module['selected'] & SQUARE == {(0, 1)}
            else:
                assert profile == {(0, 0), (1, 0), (1, 1)}
                singleton, _ = rotor_pairs(module)[(0, 0)]
                assert vertices_of({singleton}) & module['endpoints'] == {(1, 2)}
                assert {(0, 2), (1, 3)} == vertices_of({singleton}) & module['selected']
                assert (-1, 2) in wall and (1, 2) in module['endpoints']
            counts['complete_bar_wall_survivors'] += 1
    tips = [point for point in rotor()['endpoints']
            if len(set(neighbors(point)) & rotor()['endpoints']) == 1]
    assert len(tips) == 4
    for first, second in itertools.combinations(tips, 2):
        assert any(abs(value-other) > 1 for value, other in zip(first, second))
    return dict(counts)


def profile_capacity_controls():
    profiles = [frozenset(points) for size in (2, 3, 4)
                for points in itertools.combinations(SQUARE, size)]
    checked = Counter()
    for amount in range(1, 5):
        for current in itertools.combinations(profiles, amount):
            if sum(len(profile) for profile in current) != len(set.union(*(set(profile) for profile in current))):
                continue
            assert amount <= 2
            if amount == 2:
                assert all(len(profile) == 2 for profile in current)
                assert set.union(*(set(profile) for profile in current)) == SQUARE
            checked[str(amount)] += 1
    return dict(disjoint_original_profile_packings=dict(checked),
                scope='Four-corner capacity after separately proved owner/tile injection; not a complete critical sharing realization.')


def normalized(point, origin, frame):
    offset = tuple(value-base for value, base in zip(point, origin))
    return (sum(value*(-direction) for value, direction in zip(offset, frame[0])),
            sum(value*direction for value, direction in zip(offset, frame[1])))


def phase_eleven_terminal_fixture():
    dimensions = 6, 4, 4
    symmetry, offset = (True, True, False), (1, 12)
    terminal = transform_module(source(*dimensions), symmetry, offset)
    matching, supports = canonical(dimensions)
    assert {frozenset(edge) for edge in terminal['matching']} == {
        frozenset(affine(point, symmetry, offset) for point in edge) for edge in matching}
    assert terminal['selected'] == {affine(point, symmetry, offset) for point in supports}
    return six_sources()[:3]+[terminal]


def event_families(modules):
    network = combine(modules)
    endpoints = network['endpoints']
    phases = [phase_of(module) for module in modules]
    owner_at = {point: owner for owner, module in enumerate(modules) for point in module['endpoints']}
    data, closed, contacts, _, _ = closed_contacts(modules)
    regular, critical = [], []
    for key, target in contacts.items():
        if phases[key[0]] != '01' or phases[target[0]] != '01':
            continue
        port = data[key[0]]['ports'][key[1]]
        if port['blank'] not in endpoints:
            continue
        frame = port['inward'], port['exterior']
        point = add(add(port['point'], frame[0]), frame[1])
        regular.append((key[0], point, frame))
        incoming = owner_at[point]
        if phases[incoming] != '11':
            continue
        width = positive_dimensions(modules[incoming])[0]
        height = max(sum((value-base)*direction for value, base, direction
                         in zip(site, port['point'], frame[0])) for site in modules[key[0]]['endpoints'])
        if height >= width+4:
            regular.append((key[0], add(point, scale(frame[0], width)), frame))
            continue
        assert height == width+2
        root = add(point, scale(frame[0], width-1))
        opposite = [site for site in modules[incoming]['endpoints']
                    if sum((value-base)*direction for value, base, direction
                           in zip(site, root, frame[0])) == 0]
        far_height = max(sum((value-base)*direction for value, base, direction
                             in zip(site, root, frame[1])) for site in opposite)
        forced = add(root, scale(frame[1], far_height+1))
        assert forced in endpoints & modules[incoming]['selected']
        critical.append((key[0], forced, frame, owner_at[forced]))
    return regular, critical, closed, phases


def inspect(current, modules):
    network = combine(modules)
    endpoints = network['endpoints']
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    assert all(len(set(neighbors(point)) & (endpoints | network['selected'])) <= 1
               for point in network['selected'])
    regular, critical, closed, phases = event_families(modules)
    assert len({point for _, point, _, _ in critical}) == len(critical)
    regular_tiles, additional, ordinary_stops = set(), set(), set()
    for owner, point, frame in regular:
        receiver = tile_of(point)
        assert receiver not in regular_tiles
        regular_tiles.add(receiver)
        cells = vertices_of({receiver})
        pair = {add(point, scale(frame[1], -1)), add(point, add(frame[0], scale(frame[1], -1)))}
        assert cells & modules[owner]['endpoints'] == pair
        additional.update((cells & endpoints)-pair)
        if not cells <= endpoints:
            ordinary_stops.add(receiver)
    assert len(additional)+len(ordinary_stops) == 2*len(regular)
    profiles, owner_tiles, by_tile = [], set(), Counter()
    eligible_stops, rotor_stops, rotor_pairings = set(), set(), set()
    counts = Counter(critical_events=len(critical), regular_receivers=len(regular))
    for active, point, frame, owner in critical:
        receiver = tile_of(point)
        assert receiver not in regular_tiles
        assert (owner, receiver) not in owner_tiles
        owner_tiles.add((owner, receiver))
        by_tile[receiver] += 1
        cells = vertices_of({receiver})
        own = cells & modules[owner]['endpoints']
        assert len(own) in (2, 3, 4)
        assert not any(own & earlier for _, _, earlier in profiles)
        profiles.append((owner, receiver, own))
        counts['critical_profile_'+str(len(own))] += 1
        body = {normalized(site, point, frame) for site in modules[active]['endpoints']}
        clearance = max(column for row, column in body if row == -1)
        assert clearance >= 1 and clearance % 2 == 1
        assert {(-1, column) for column in range(clearance+1)} <= body
        assert {(row, clearance) for row in (0, 1, 2)} <= body
        if phases[owner] == '01':
            assert own == cells
            continue
        counts['non_phase01_critical_events'] += 1
        assert phases[owner] in {'10', '11', 'rotor'}
        normal_profile = {normalized(site, point, frame) for site in own}
        normal_support = {normalized(site, point, frame) for site in modules[owner]['selected'] & cells}
        if phases[owner] == '11':
            assert len(own) == 2 and normal_support == {(1, 1)}
            continue
        if len(own) == 2:
            assert normal_profile == {(0, 0), (1, 0)} and normal_support == {(0, 1)}
            forced = add(point, frame[1])
            assert forced in modules[owner]['selected'] & endpoints
            if not cells <= endpoints:
                assert len(cells & endpoints) == 3 and receiver not in eligible_stops
                eligible_stops.add(receiver)
        else:
            assert phases[owner] == 'rotor' and modules[owner]['charge'] == 0
            assert len(own) == 3 and normal_profile == {(0, 0), (1, 0), (1, 1)}
            forced = add(point, scale(frame[1], 2))
            assert forced in modules[owner]['selected'] & endpoints
            singleton, _ = rotor_pairs(modules[owner])[receiver]
            assert (owner, singleton) not in rotor_pairings
            rotor_pairings.add((owner, singleton))
            if not cells <= endpoints:
                rotor_stops.add((owner, receiver))
    assert all(amount <= 2 for amount in by_tile.values())
    counts['shared_critical_tiles'] = sum(amount == 2 for amount in by_tile.values())
    counts['critical_H_stops'] = len(eligible_stops)
    counts['critical_Z0_stops'] = len(rotor_stops)
    exact = inspect_exact(current, modules)
    transfers = inspect_transfers(current, modules)
    old_stops = set()
    for record in transfers['records']:
        if record['kind'] == 'direct_H':
            old_stops.add(tuple(record['tile']))
        elif record['kind'] == 'unactivated_corner_H':
            stop = exterior_chain(record['positive_owner'], bool(record['leg']), modules, endpoints)
            old_stops.add(tuple(stop['tile']))
    assert not old_stops & (ordinary_stops | eligible_stops)
    assert not ordinary_stops & eligible_stops
    assert len(old_stops | ordinary_stops | eligible_stops) <= exact['boundary_cost']
    assert transfers['counted']+len(ordinary_stops)+len(eligible_stops) <= (
        2*exact['activated_positive']+exact['boundary_cost'])
    assert len(rotor_stops) <= exact['unpaired_rotor_activation']
    assert transfers['counted']+len(ordinary_stops)+len(eligible_stops)+len(rotor_stops)+exact[
        'unused_u_triples'] <= 2*exact['event_reserve']+exact['activated_positive']
    for chosen in (set(), {owner for owner in closed if phases[owner] == '01'}):
        original_chosen = {site for owner in chosen for site in modules[owner]['endpoints']}
        external = [(owner, receiver, profile) for owner, receiver, profile in profiles if owner not in chosen]
        returns = [(owner, receiver, profile) for owner, receiver, profile in profiles if owner in chosen]
        external_mass = set().union(*(profile for _, _, profile in external))
        return_mass = set().union(*(profile for _, _, profile in returns))
        assert not external_mass & (original_chosen | additional | return_mass)
        assert not return_mass & additional
        expected = 2*len(external)+sum(len(profile) == 3 for _, _, profile in external)+2*sum(
            len(profile) == 4 for _, _, profile in external)
        assert len(external_mass) == expected
        assert len(return_mass) == 4*len(returns)
        assert len(additional | external_mass | return_mass)+len(ordinary_stops) == (
            2*len(regular)+expected+4*len(returns))
    return dict(counts)


def neutral_exit_receipt():
    modules = phase_eleven_terminal_fixture()
    network = combine(modules)
    current = 20, 30, network['selected'], network['matching']
    report = inspect(current, modules)
    assert [phase_of(module) for module in modules] == ['01', '11', '01', '11']
    assert len(network['matching']) == 64 and len(network['endpoints']) == 128
    assert len(network['selected']) == 28
    assert report['critical_events'] == report['critical_profile_2'] == 1
    assert report['critical_H_stops'] == report['critical_Z0_stops'] == 0
    cells = vertices_of({(1, 4)})
    assert cells & network['endpoints'] == {(2, 8), (2, 9)}
    assert cells & network['selected'] == {(3, 9)}
    assert (2, 8) in modules[3]['endpoints'] & modules[1]['selected']
    assert all(0 <= row < 20 and 0 <= column < 30
               for row, column in network['endpoints'] | network['selected'])
    exact = inspect_exact(current, modules)
    assert exact == dict(positive=0, marked=0, activated_positive=0,
                         unused_u_triples=4, unpaired_rotor_activation=0,
                         lone_irregular=2, sole_irregular_pair=7, mutual_non_event=0,
                         mixed_three=0, boundary_cost=16, event_reserve=10,
                         exact_joint_margin=10)
    anchors = []
    for point in sorted(network['selected']):
        occupied = set(neighbors(point)) & (network['endpoints'] | network['selected'])
        assert len(occupied) == 1 and occupied <= network['endpoints']
        anchors.append(dict(support=point, anchor=next(iter(occupied))))
    return dict(shape=[20, 30], matching_edges=64, endpoints=128, retained_supports=28,
                objective=92, half_area=300, ambient_slack=208, critical_root=[2, 8],
                critical_final_profile=[2, 1], critical_owner_phase='11',
                exact_census=exact, support_anchors=anchors,
                refuted_rule='Every critical U terminal receiver has at least three final endpoints or pays an H/Z0 stop.',
                not_refuted='Eligible U10/rotor stop lemma, full allocation and grid equality.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    controls = fixtures()+[('critical_six', six_sources()),
                           ('critical_phase11_terminal', phase_eleven_terminal_fixture())]
    controls += [('critical_family_'+str(width), family(width)) for width in (20, 22, 26, 40, 100)]
    totals = Counter()
    for name, modules in controls:
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offset = ((int(flip_column), int(flip_row)) if transpose
                      else (int(flip_row), int(flip_column)))
            current, moved = contained([transform_module(module, symmetry, offset) for module in modules])
            totals.update(inspect(current, moved))
            totals['complete_feasible_images'] += 1
    result = dict(status='PASS', U_roles=local_U_controls(), rotor_roles=exact_rotor_controls(),
                  profile_packings=profile_capacity_controls(), complete_controls=dict(totals),
                  neutral_exit_certificate=neutral_exit_receipt(),
                  complete_AA_coverage=0,
                  scope='General U roles/profiles/wall proof and exact rotor catalogue are independently formalized. '
                        'Finite complete controls check actual original-profile unions, physical stops and one H/Z0 ledger. '
                        'A four-source complete phase11 terminal fixture supplies non-phase01 critical coverage; '
                        'critical H/Z0 stops, sharing and AA have no complete witnesses in this batch. '
                        'No full allocation, improved unrestricted constant or grid equality claim.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
