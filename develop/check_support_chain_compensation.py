"""Physical common-pool controls for complete-source support-chain routing."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import inspect_slots, tile_of
from check_component_receivers import endpoint_components, vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import positive_dimensions
from check_regular_tile_compensation import profile_counts
from check_short_leg_defect_injection import inverse_affine
from check_width_six_interleaving import inspect_payment
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def normalize(module, reflected=False):
    width, left, right, symmetry, offset = positive_dimensions(module)

    def original(point):
        row, column = point
        return inverse_affine((row, width+1-column if reflected else column), symmetry, offset)

    def reference(point):
        row, column = affine(point, symmetry, offset)
        return row, width+1-column if reflected else column

    return right if reflected else left, original, reference


def stop_record(owner, tile, pair, consumed, original_blank, modules, endpoints):
    cells = vertices_of({tile})
    assert cells & endpoints == pair | {consumed}
    assert original_blank not in endpoints
    assert cells & modules[owner]['endpoints'] == pair
    assert cells & modules[owner]['selected'] == {consumed}
    assert len(pair) == 2
    assert not any(len(cells & module['endpoints']) == 2 and
                   not cells & module['selected'] for module in modules)
    return dict(kind='L3_regular_pair', owner=owner, tile=tile,
                pair=sorted(pair), consumed=consumed, original_blank=original_blank)


def incoming_chain(owner, gate, modules, endpoints):
    module = modules[owner]
    assert len(module['endpoints']) != 8 and profile_counts(module)[3, 0] == 2
    width, left, right, symmetry, offset = positive_dimensions(module)
    tip = affine(gate, symmetry, offset)
    assert tip in ((left, 1), (right, width))
    reflected = tip[1] == width
    height, original, _ = normalize(module, reflected)
    cap = tile_of(original((1, 1)))
    cap_cells = vertices_of({cap})
    assert len(cap_cells & module['endpoints']) == 3
    assert not cap_cells & module['selected']
    if not cap_cells <= endpoints:
        return dict(kind='U0', owner=owner, tile=cap, gate=gate, reflected=reflected)
    for index in range(1, height//2):
        pair = {original((2*index+1, 1)), original((2*index+2, 1))}
        consumed = original((2*index+1, 2))
        original_blank = original((2*index+2, 2))
        tile = tile_of(consumed)
        assert consumed in endpoints
        assert {tile_of(point) for point in pair | {original_blank}} == {tile}
        if vertices_of({tile}) <= endpoints:
            continue
        return dict(gate=gate, reflected=reflected,
                    **stop_record(owner, tile, pair, consumed, original_blank, modules, endpoints))
    return None


def exterior_chain(owner, reflected, modules, endpoints):
    module = modules[owner]
    height, original, _ = normalize(module, reflected)
    terminal = vertices_of({tile_of(original((height, 1)))})
    supports = terminal & module['selected']
    assert len(supports) == 2
    if supports & endpoints:
        return None
    consumed_indices = [index for index in range(height//2)
                        if original((2*index, 0)) in endpoints]
    if not consumed_indices:
        return None
    for index in range(min(consumed_indices), height//2):
        pair = {original((2*index, 1)), original((2*index+1, 1))}
        consumed = original((2*index, 0))
        original_blank = original((2*index+1, 0))
        assert consumed in endpoints
        tile = tile_of(consumed)
        if vertices_of({tile}) <= endpoints:
            continue
        return dict(reflected=reflected,
                    **stop_record(owner, tile, pair, consumed, original_blank, modules, endpoints))
    raise AssertionError('Full exterior chain would activate the positive terminal.')


def inspect_chains(current, modules):
    old = inspect_payment(current, modules)
    endpoints = combine(modules)['endpoints']
    marks = inspect_slots(current, modules)['marked_assignments']
    incoming = []
    exterior = []
    tip_owners = set()
    for record in marks:
        if record['kind'] != 'gate':
            continue
        owner = record['owner']
        if not profile_counts(modules[owner])[3, 0]:
            continue
        gate = tuple(record['witness'])
        assert (owner, gate) not in tip_owners
        tip_owners.add((owner, gate))
        routed = incoming_chain(owner, gate, modules, endpoints)
        if routed is not None:
            incoming.append(routed)
    for owner, module in enumerate(modules):
        if module['charge'] != 1:
            continue
        for reflected in (False, True):
            routed = exterior_chain(owner, reflected, modules, endpoints)
            if routed is not None:
                exterior.append(routed)
    records = incoming+exterior
    stops = [tuple(record['tile']) for record in records if record['kind'] == 'L3_regular_pair']
    caps = [(record['owner'], tuple(record['tile'])) for record in incoming
            if record['kind'] == 'U0']
    assert len(stops) == len(set(stops))
    assert len(caps) == len(set(caps))
    unfilled = sum(len(vertices_of({tile}) & module['endpoints']) == 3 and
                   not vertices_of({tile}) <= endpoints
                   for module in modules if len(module['endpoints']) != 8
                   for tile in module['receiver'])
    assert len(caps) <= unfilled
    old_demand = 2*old['zero_double']+old['paid_single']
    assert old_demand+len(records) <= unfilled+old['boundary']
    numerator = old['paid_single']+len(records)-old['single_double']
    bound = old['unmarked']-old['exceptional_double']-((-numerator)//2)
    assert old['margin'] >= bound
    return dict(positive=old['positive'], marked=len(marks), reserve_margin=old['margin'],
                old_bound=old['margin_bound'], new_bound=bound,
                strict_improvement=bound > old['margin_bound'],
                residual_single=-numerator,
                broken_gate_chains=len(incoming), unactivated_exterior_chains=len(exterior),
                unfilled_U_caps=unfilled, boundary=old['boundary'],
                old_slot_demand=old_demand, chain_demands=len(records), records=records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    counts = Counter()
    cases = list(fixtures())
    for width, height in ((6, 4), (6, 8), (8, 6), (14, 10)):
        cases.append(('exterior_stop_%d_%d' % (width, height),
                      [source(width, height, 4), transform_module(source(6, 6, 4),
                       (True, False, False), (-1, -6))]))
    for name, modules in cases:
        for symmetry, phase, _, current, moved in phase_images(modules):
            report = inspect_chains(current, moved)
            records.append(dict(fixture=name, symmetry=symmetry, phase=phase, **report))
            counts['physical_images'] += 1
            counts['broken_gate_chains'] += report['broken_gate_chains']
            counts['unactivated_exterior_chains'] += report['unactivated_exterior_chains']
            counts['strict_improvements'] += report['strict_improvement']
            counts.update(record['kind'] for record in report['records'])
    merged = []
    for index, name in enumerate(('opposed_6', 'exterior_stop_6_8')):
        modules = next(modules for fixture, modules in cases if fixture == name)
        merged.extend(transform_module(module, (False, False, False), (0, 100*index))
                      for module in modules)
    merged.extend(transform_module(module, (False, False, False), (0, 200)) for module in
                  [source(6, 8, 6), transform_module(source(6, 6, 8),
                   (False, True, False), (8, 1))])
    current, moved = contained(merged)
    combined = inspect_chains(current, moved)
    assert combined['broken_gate_chains'] and combined['unactivated_exterior_chains']
    assert combined['old_slot_demand']
    records.append(dict(fixture='separated_three_resource_classes', **combined))
    counts['physical_images'] += 1
    counts['broken_gate_chains'] += combined['broken_gate_chains']
    counts['unactivated_exterior_chains'] += combined['unactivated_exterior_chains']
    counts['strict_improvements'] += combined['strict_improvement']
    counts.update(record['kind'] for record in combined['records'])
    component_records = []
    for component in endpoint_components(current):
        members = [module for module in moved if module['endpoints'] <= component]
        network = combine(members)
        restricted = (*current[:2], network['selected'], network['matching'])
        component_records.append(inspect_chains(restricted, members))
    odd_components = sum(record['residual_single'] % 2 for record in component_records)
    component_bound = sum(record['new_bound'] for record in component_records)
    assert component_bound == combined['new_bound']+odd_components//2
    assert combined['reserve_margin'] >= component_bound
    assert odd_components >= 2 and component_bound > combined['new_bound']
    component_fixture = dict(components=len(component_records), odd_components=odd_components,
                             residuals=[record['residual_single'] for record in component_records],
                             global_bound=combined['new_bound'], component_bound=component_bound,
                             actual_margin=combined['reserve_margin'])
    rounding_cases = 0
    negative_residual_cases = 0
    for residuals in itertools.product(range(-5, 6), repeat=3):
        odds = sum(value % 2 for value in residuals)
        assert sum(residuals)//2-sum(value//2 for value in residuals) == odds//2
        rounding_cases += 1
        negative_residual_cases += any(value < 0 for value in residuals)
    result = dict(status='PASS', summary=dict(counts), physical=records,
                  component_fixture=component_fixture,
                  component_rounding=dict(cases=rounding_cases,
                                          cases_with_negative_residual=negative_residual_cases),
                  scope='Finite complete-source routing, original-pair ownership, chain/witness-pool separation and shared-integer-budget controls. Universal support propagation and source adapters are written; unrestricted allocation/grid equality remain open.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', summary=dict(counts))))


if __name__ == '__main__':
    main()
