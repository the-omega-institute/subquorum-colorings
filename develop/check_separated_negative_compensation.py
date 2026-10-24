"""Independent local and physical controls for separated negative receivers."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import boundary, inspect_slots, tile_of
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_degree_three_fusion import phase_images
from check_minus_one_joint_compensation import marked_gate_modules
from check_minus_one_tip_obstructions import overloaded_tile_modules, two_tip_modules
from check_regular_tile_compensation import inspect, profile_counts
from check_zero_credit_tip_family import family
from degree_four_overcount import opposed_bands
from degree_three_fusion import four_way_modules, occupied_bands
from rotor_networks import chain_modules, rotor, star_modules


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def adjacent(corner):
    return {corner ^ 1, corner ^ 2}


def good_profiles():
    profiles = []
    for corner in range(4):
        profiles.append((frozenset({corner}), frozenset(adjacent(corner))))
    for endpoints in itertools.combinations(range(4), 2):
        if endpoints[1] not in adjacent(endpoints[0]):
            continue
        for selected in set(range(4))-set(endpoints):
            profiles.append((frozenset(endpoints), frozenset({selected})))
    return profiles


def local_controls():
    records = []
    for negative_endpoints, negative_selected in [({0}, {1}), ({0, 1}, set())]:
        candidates = [profile for profile in good_profiles() if not profile[0] & negative_endpoints]
        for amount in range(4):
            for foreign in itertools.combinations(candidates, amount):
                profiles = [(negative_endpoints, negative_selected), *foreign]
                endpoints = set.union(set(), *(set(profile[0]) for profile in profiles))
                if len(endpoints) != sum(len(profile[0]) for profile in profiles):
                    continue
                selected = set.union(set(), *(set(profile[1]) for profile in profiles))-endpoints
                occupied = endpoints | selected
                if any(len(adjacent(corner) & occupied) > 1 for corner in selected):
                    continue
                irregular = sum(bool((adjacent(corner) & endpoints)-negative_endpoints-negative_selected)
                                for corner in negative_endpoints)
                regular = sum(len((adjacent(corner) & endpoints)-set(original)-set(support))
                              for original, support in foreign for corner in original)
                full = len(endpoints) == 4
                correction = 2*int(full)-regular
                assert correction >= 0
                if irregular:
                    assert full and regular <= 1 and correction >= 1
                reservation = int(len(negative_endpoints) == 2)
                assert irregular <= correction+reservation
                marks = [0, 1] if reservation and not full and not irregular else [0]
                for marked in marks:
                    assert irregular+marked <= correction+reservation
                    records.append(dict(negative_endpoints=sorted(negative_endpoints),
                                        negative_selected=sorted(negative_selected),
                                        foreign=[dict(endpoints=sorted(original), selected=sorted(support))
                                                 for original, support in foreign],
                                        final_endpoints=sorted(endpoints), final_selected=sorted(selected),
                                        irregular=irregular, regular=regular, correction=correction,
                                        corner_assignment=marked, reservation=reservation))
    return records


def inspect_separated(current, modules):
    negative = [index for index, module in enumerate(modules) if module['charge'] < 0]
    negative_tiles = [module['receiver'] for index, module in enumerate(modules) if index in negative]
    assert sum(map(len, negative_tiles)) == len(set.union(set(), *negative_tiles))
    assert all(not profile_counts(module)[3, 0] for module in modules if module['charge'] == 0)
    slots = inspect_slots(current, modules)
    physical = inspect(current, modules, require_frozen=False)
    endpoints = set.union(set(), *(module['endpoints'] for module in modules))
    regular = Counter()
    irregular = Counter()
    for module in modules:
        old = module['endpoints'] | module['selected']
        possible_irregular = boundary(module)[2]
        for point in module['endpoints']:
            for other in (set(neighbors(point)) & endpoints)-old:
                if tile_of(point) == tile_of(other):
                    (irregular if point in possible_irregular else regular)[tile_of(point)] += 1
    full = {tile for module in modules for tile in module['receiver']
            if vertices_of({tile}) <= endpoints and
            not any(vertices_of({tile}) <= original['endpoints'] for original in modules)}
    correction = {tile: 2*int(tile in full)-regular[tile]
                  for module in modules for tile in module['receiver']}
    assert all(value >= 0 for value in correction.values())
    bar = set()
    negative_u = 0
    negative_rotors = 0
    for index in negative:
        module = modules[index]
        if len(module['endpoints']) == 8:
            negative_rotors += 1
        else:
            negative_u += 1
        for tile in module['receiver']:
            cells = vertices_of({tile})
            profile = len(cells & module['endpoints']), len(cells & module['selected'])
            if profile == (2, 0):
                bar.add(tile)
            if irregular[tile]:
                assert tile in full and regular[tile] <= 1
            assert irregular[tile] <= correction[tile]+int(profile == (2, 0))
    corner_assignments = Counter()
    exceptional = 0
    for record in slots['marked_assignments']:
        module = modules[record['owner']]
        witness = tuple(record['witness'])
        _, failures, possible_irregular = boundary(module)
        if witness in failures & possible_irregular:
            tile = tile_of(witness)
            assert tile in bar and tile not in full and not irregular[tile]
            corner_assignments[tile] += 1
        else:
            exceptional += 1
    assert all(value <= 1 for value in corner_assignments.values())
    for tile in bar:
        assert irregular[tile]+corner_assignments[tile] <= correction[tile]+1
    assert sum(irregular.values())+sum(corner_assignments.values()) <= sum(correction.values())+len(bar)
    assert exceptional <= 2*negative_u and exceptional <= 2*slots['positive']
    assert slots['negative_mass'] == len(bar)+negative_u+2*negative_rotors
    lower_bound = abs(slots['positive']-negative_u)+2*negative_rotors
    assert physical['two_guard_credit'] >= lower_bound
    assert physical['half_area']-physical['objective'] >= lower_bound
    return dict(positive=slots['positive'], negative_u=negative_u, negative_rotors=negative_rotors,
                bar_reservations=len(bar), corner_assignments=sum(corner_assignments.values()),
                exceptional_assignments=exceptional, irregular_events=sum(irregular.values()),
                marked_sides=slots['marked_sides'], square_credit=sum(correction.values()),
                guaranteed_slack=lower_bound, finer_slack=physical['two_guard_credit'],
                old_density_slack=slots['positive']-slots['negative_mass']-2*slots['minus_one']-
                                  2*slots['vertical_phase']+physical['residual_square_credit'],
                actual_slack=physical['half_area']-physical['objective'])


def inspect_general_defect(current, modules):
    slots = inspect_slots(current, modules)
    physical = inspect(current, modules, require_frozen=False)
    endpoints = set.union(set(), *(module['endpoints'] for module in modules))
    represented = {tile: [index for index, module in enumerate(modules) if tile in module['receiver']]
                   for module in modules for tile in module['receiver']}
    negative_u = sum(module['charge'] < 0 and len(module['endpoints']) != 8 for module in modules)
    negative_rotors = sum(module['charge'] == -2 for module in modules)
    irregular = Counter()
    regular = Counter()
    corner_assignments = Counter()
    for module in modules:
        old = module['endpoints'] | module['selected']
        candidates = boundary(module)[2]
        for point in module['endpoints']:
            for other in (set(neighbors(point)) & endpoints)-old:
                if tile_of(point) == tile_of(other):
                    (irregular if point in candidates else regular)[tile_of(point)] += 1
    for record in slots['marked_assignments']:
        _, failures, candidates = boundary(modules[record['owner']])
        witness = tuple(record['witness'])
        if witness in failures & candidates:
            corner_assignments[tile_of(witness)] += 1
    assert all(amount <= 1 for amount in corner_assignments.values())
    bar_reservations = 0
    overlap_tax = 0
    zero_corner_tax = 0
    singleton_overlap_tax = 0
    quadruple_singleton_tax = 0
    irregular_slots = 0
    exceptional_u = 0
    exceptional_rotor = 0
    half_slot_remainder = 0
    for tile, owners in represented.items():
        cells = vertices_of({tile})
        negative = [index for index in owners if modules[index]['charge'] < 0]
        profiles = {index: (len(cells & modules[index]['endpoints']),
                            len(cells & modules[index]['selected'])) for index in owners}
        reservation = sum(profiles[index] == (2, 0) for index in negative)
        singletons = sum(profiles[index] == (1, 1) for index in negative)
        singleton_overlap = int(len(negative) >= 2 and singletons > 0)
        quadruple_singleton = int(singletons == 4)
        singleton_overlap_tax += singleton_overlap
        quadruple_singleton_tax += quadruple_singleton
        bar_reservations += reservation
        overlap = 0
        zero_corner = 0
        if len(negative) >= 2:
            overlap = sum(profiles[index] in {(1, 1), (2, 0)} for index in negative)
            overlap_tax += overlap
        elif len(negative) == 1 and profiles[negative[0]] == (1, 1):
            exceptional = [index for index in owners if modules[index]['charge'] == 0 and
                           profiles[index] == (3, 0)]
            if exceptional:
                assert cells <= endpoints and len(exceptional) == 1
                zero_corner_tax += 1
                zero_corner = 1
        new_full = cells <= endpoints and not any(cells <= module['endpoints'] for module in modules)
        correction = 2*int(new_full)-regular[tile]
        local_slots = sum(len(cells & boundary(modules[index])[2]) for index in owners)
        three_owners = [index for index in owners if profiles[index] == (3, 0)]
        exceptional_three = int(new_full and singletons == 1 and bool(three_owners))
        if exceptional_three:
            assert len(three_owners) == 1
            if len(modules[three_owners[0]]['endpoints']) == 8:
                exceptional_rotor += 1
            else:
                exceptional_u += 1
        local_remainder = local_slots+exceptional_three-2*(irregular[tile]-correction)
        assert local_remainder >= 0
        irregular_slots += local_slots
        half_slot_remainder += local_remainder
        assert correction >= 0
        assert irregular[tile]+corner_assignments[tile] <= correction+reservation+overlap+zero_corner
        assert irregular[tile]+corner_assignments[tile] <= (
            correction+reservation+singleton_overlap+quadruple_singleton+zero_corner)
    assert slots['negative_mass'] == bar_reservations+negative_u+2*negative_rotors
    assert irregular_slots == 2*slots['negative_mass']-2*slots['diagonal_phase']
    assert exceptional_u <= 2*slots['diagonal_phase']
    assert exceptional_rotor == zero_corner_tax
    correction_total = physical['residual_square_credit']
    irregular_total = sum(irregular.values())
    assert irregular_total <= (slots['negative_mass']-slots['diagonal_phase']+
                              correction_total+(exceptional_u+exceptional_rotor)//2)
    assert irregular_total <= slots['negative_mass']+correction_total+exceptional_rotor//2
    half_slot_bound = slots['positive']-slots['marked_sides']-exceptional_rotor//2
    assert physical['two_guard_credit'] >= half_slot_bound
    assert (2*(slots['negative_mass']+correction_total-irregular_total-slots['marked_sides']) ==
            2*slots['diagonal_phase']-exceptional_u-exceptional_rotor+
            half_slot_remainder-2*slots['marked_sides'])
    lower_bound = abs(slots['positive']-negative_u)+2*negative_rotors-overlap_tax-zero_corner_tax
    singleton_bound = (abs(slots['positive']-negative_u)+2*negative_rotors-
                       singleton_overlap_tax-quadruple_singleton_tax-zero_corner_tax)
    assert singleton_bound >= lower_bound
    assert physical['two_guard_credit'] >= singleton_bound
    assert physical['two_guard_credit'] >= lower_bound
    assert physical['half_area']-physical['objective'] >= lower_bound
    return dict(positive=slots['positive'], negative_u=negative_u, negative_rotors=negative_rotors,
                overlap_incidence_tax=overlap_tax, zero_corner_tax=zero_corner_tax,
                singleton_overlap_tax=singleton_overlap_tax,
                quadruple_singleton_tax=quadruple_singleton_tax,
                singleton_guaranteed_slack=singleton_bound,
                irregular_slots=irregular_slots, exceptional_u=exceptional_u,
                exceptional_rotor=exceptional_rotor, half_slot_remainder=half_slot_remainder,
                half_slot_guaranteed_slack=half_slot_bound,
                bar_reservations=bar_reservations, guaranteed_slack=lower_bound,
                finer_slack=physical['two_guard_credit'],
                actual_slack=physical['half_area']-physical['objective'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    local = local_controls()
    fixtures = [('marked_gate', marked_gate_modules()), ('two_tips', two_tip_modules()),
                ('overloaded', overloaded_tile_modules()), ('zero_credit', family()), ('rotor', [rotor()])]
    fixtures += [('four_way_%d' % width, four_way_modules(width)) for width in (8, 14)]
    fixtures += [('star_%d' % width, star_modules(width)) for width in (6, 14)]
    fixtures += [('chain_%d' % amount, chain_modules(amount)) for amount in (1, 2, 3)]
    for width in (6, 8, 14, 40):
        fixtures.append(('opposed_%d' % width, opposed_bands(width, 4)[1]))
        fixtures.append(('occupied_%d' % width, occupied_bands(width)[1]))
    physical = []
    general = []
    excluded = []
    for name, modules in fixtures:
        for symmetry, phase, offset, current, moved in phase_images(modules):
            general.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                **inspect_general_defect(current, moved)))
            negative_tiles = [module['receiver'] for module in moved if module['charge'] < 0]
            shared = sum(map(len, negative_tiles)) != len(set.union(set(), *negative_tiles))
            zero_corners = any(profile_counts(module)[3, 0] for module in moved if module['charge'] == 0)
            if shared or zero_corners:
                excluded.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                     negative_receiver_overlap=shared, zero_rotor_three_endpoint_tile=zero_corners))
                continue
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_separated(current, moved)))
    summary = dict(local_cases=len(local), physical_images=len(physical), excluded_images=len(excluded),
                   general_defect_images=len(general),
                   general_with_overlap=sum(record['overlap_incidence_tax'] > 0 for record in general),
                   general_with_zero_corner=sum(record['zero_corner_tax'] > 0 for record in general),
                   general_nonnegative_bound=sum(record['guaranteed_slack'] >= 0 for record in general),
                   singleton_nonnegative_bound=sum(record['singleton_guaranteed_slack'] >= 0 for record in general),
                   singleton_strict_improvement=sum(record['singleton_guaranteed_slack'] > record['guaranteed_slack']
                                                    for record in general),
                   half_slot_nonnegative_bound=sum(record['half_slot_guaranteed_slack'] >= 0 for record in general),
                   half_slot_strict_improvement=sum(record['half_slot_guaranteed_slack'] > record['guaranteed_slack']
                                                    for record in general),
                   actual_irregular_images=sum(record['irregular_events'] > 0 for record in physical),
                   actual_marked_images=sum(record['marked_sides'] > 0 for record in physical),
                   actual_corner_assignment_images=sum(record['corner_assignments'] > 0 for record in physical),
                   improved_density_images=sum(record['old_density_slack'] < 0 for record in physical))
    assert summary['actual_irregular_images'] and summary['actual_marked_images']
    assert summary['improved_density_images']
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary, local=local,
        physical=physical, excluded=excluded, general_defect_physical=general,
        scope='Finite normalized local-profile controls and complete physical fusion checks. General isometry/source-profile adapter, tilewise proof and arbitrary-parameter theorem are written separately. Excluded cases do not satisfy the zero-tax theorem; all fixtures are separately checked against the general overlap/zero-corner defect inequality. No unrestricted nonnegative compensation claim.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
