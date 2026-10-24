"""Reconstruct passive-corner charges and a complete neutral ownership cycle."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import fixtures, inspect_exact
from check_minus_one_tip_obstructions import source
from check_occupied_gate_activation import positive_dimensions
from check_regular_tile_compensation import inspect as inspect_regular
from check_short_leg_defect_injection import defect_tiles, inverse_affine
from check_support_chain_compensation import exterior_chain
from rotor_networks import affine, combine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect_transfers(current, modules):
    exact = inspect_exact(current, modules)
    endpoints = combine(modules)['endpoints']
    owner_of = {point: owner for owner, module in enumerate(modules)
                for point in module['endpoints']}
    defects = defect_tiles(modules, endpoints)
    activated = set()
    for owner, module in enumerate(modules):
        if module['charge'] != 1:
            continue
        width, left, right, symmetry, offset = positive_dimensions(module)
        for leg, reference_tip in enumerate(((left, 1), (right, width))):
            tip = inverse_affine(reference_tip, symmetry, offset)
            if vertices_of({tile_of(tip)}) & module['selected'] & endpoints:
                activated.add((owner, leg))
    assert len(activated) == exact['activated_positive']
    records = []
    direct_tiles = set()
    routed_tiles = set()
    corner_claims = set()
    terminal_claims = set()
    for owner, module in enumerate(modules):
        if phase_of(module) != '10':
            continue
        width, _, _, symmetry, offset = positive_dimensions(module)
        for reflected in (False, True):
            def original(point):
                row, column = point
                return inverse_affine((-row, width+1-column if reflected else column), symmetry, offset)
            corner, consumed, retained, blank = [original(point) for point in
                ((0, 1), (0, 0), (1, 0), (1, 1))]
            cells = vertices_of({tile_of(corner)})
            assert cells == {corner, consumed, retained, blank}
            assert cells & module['endpoints'] == {corner}
            assert cells & module['selected'] == {consumed}
            if cells & endpoints != {corner, consumed} or cells & current[2] != {retained}:
                continue
            assert original((2, 0)) not in endpoints
            adjacent = vertices_of({tile_of(original((0, 2)))})
            parent_pair = {original((0, 2)), original((0, 3))}
            assert adjacent & module['endpoints'] == parent_pair
            assert not adjacent & module['selected']
            assert not adjacent & current[2]
            if not adjacent <= endpoints:
                tile = tile_of(original((0, 2)))
                assert defects[tile] in ('L2bar', 'L3') and tile not in direct_tiles
                direct_tiles.add(tile)
                records.append(dict(owner=owner, reflected=reflected, kind='direct_H', tile=tile))
                continue
            target = original((1, 2))
            foreign = owner_of[target]
            assert foreign != owner and modules[foreign]['charge'] == 1
            width_positive, left, right, positive_symmetry, positive_offset = positive_dimensions(modules[foreign])
            reference = affine(target, positive_symmetry, positive_offset)
            if reference in ((0, 1), (0, width_positive)):
                leg = int(reference[1] == width_positive)
                claim = foreign, leg
                assert claim not in corner_claims
                corner_claims.add(claim)
                if claim in activated:
                    kind = 'activated_corner'
                else:
                    stop = exterior_chain(foreign, bool(leg), modules, endpoints)
                    assert stop is not None and stop['kind'] == 'L3_regular_pair'
                    tile = tuple(stop['tile'])
                    assert tile not in routed_tiles and defects[tile] == 'L3'
                    routed_tiles.add(tile)
                    kind = 'unactivated_corner_H'
            else:
                assert reference in ((left, 1), (right, width_positive))
                leg = int(reference[1] == width_positive)
                claim = foreign, leg
                assert claim in activated and claim not in terminal_claims
                terminal_claims.add(claim)
                kind = 'activated_terminal'
            records.append(dict(owner=owner, reflected=reflected, kind=kind,
                                positive_owner=foreign, leg=leg))
    assert not direct_tiles & routed_tiles
    kinds = Counter(record['kind'] for record in records)
    assert len(direct_tiles)+len(routed_tiles) <= exact['boundary_cost']
    assert kinds['activated_corner'] <= len(activated)
    assert kinds['activated_terminal'] <= len(activated)
    assert len(records) <= 2*exact['activated_positive']+exact['boundary_cost']
    assert len(records)+exact['boundary_cost']+2*exact['unused_u_triples']+2*exact[
        'unpaired_rotor_activation'] <= 4*exact['event_reserve']
    return dict(counted=len(records), kinds=dict(kinds), activation=len(activated),
                boundary=exact['boundary_cost'], reserve=exact['event_reserve'], records=records)


def neutral_cycle():
    modules = [transform_module(rotor(), (False, False, False), offset)
               for offset in ((1, 3), (3, 1), (3, 5), (5, 3))]
    network = combine(modules)
    current = 12, 12, network['selected'], network['matching']
    exact = inspect_exact(current, modules)
    regular = inspect_regular(current, modules, require_frozen=False)
    assert len(network['endpoints']) == 32
    assert len(network['selected']) == len(network['matching']) == 16
    edges = set()
    full_tiles = []
    for tile in network['receiver']:
        cells = vertices_of({tile})
        owners = [owner for owner, module in enumerate(modules) if cells & module['endpoints']]
        if len(owners) > 1:
            assert len(owners) == 2 and cells <= network['endpoints']
            edges.add(tuple(owners))
            full_tiles.append(dict(tile=tile, owners=owners))
    assert edges == {(0, 1), (0, 2), (1, 3), (2, 3)}
    assert len(full_tiles) == regular['new_aligned_faces'] == 4
    assert regular['regular_source_events'] == 8 and regular['irregular_source_events'] == 0
    assert regular['residual_square_credit'] == 0
    assert exact['event_reserve'] == exact['exact_joint_margin'] == 0
    assert all(exact[key] == 0 for key in ('activated_positive', 'unused_u_triples',
        'unpaired_rotor_activation', 'boundary_cost'))
    assert regular['half_area']-regular['objective'] == 40
    support_witnesses = []
    occupied = network['endpoints'] | network['selected']
    for point in sorted(network['selected']):
        neighbors = {(point[0]-1, point[1]), (point[0]+1, point[1]),
                     (point[0], point[1]-1), (point[0], point[1]+1)}
        adjacent = neighbors & occupied
        assert len(adjacent) == 1 and adjacent <= network['endpoints']
        support_witnesses.append(dict(selected=point, anchor=next(iter(adjacent))))
    return modules, dict(complete_feasible=True, shape=[12, 12], endpoints=32, matching=16,
                         selected=16, ownership_edges=sorted(edges), mixed_full_tiles=full_tiles,
                         regular_events=8, residual_credit=0, reserve=0, margin=0,
                         actual_ambient_slack=40, retained_supports=support_witnesses,
                         refuted_rule='Every finite ownership cycle forces a positive A/X/U0/Z0/H or reserve contribution.',
                         target_not_refuted='Negative-U/AA-specific compensation, coefficient one and grid equality remain open.')


def local_roles():
    counts = Counter()
    parameters = list(itertools.product((6, 8, 14), (4, 8, 16), (4, 6, 12)))
    parameters += [(40, 100, 4)]
    target = 1, 2
    for dimensions in parameters:
        width, left, right = dimensions
        base = source(*dimensions)
        for symmetry in itertools.product((False, True), repeat=3):
            points = {affine(point, symmetry) for point in base['endpoints']}
            selections = {affine(point, symmetry) for point in base['selected']}
            for root in base['endpoints']:
                counts['tested_U_roles'] += 1
                reference = affine(root, symmetry)
                offset = target[0]-reference[0], target[1]-reference[1]
                moved_points = {(point[0]+offset[0], point[1]+offset[1]) for point in points}
                moved_selected = {(point[0]+offset[0], point[1]+offset[1]) for point in selections}
                if ((0, 2) in moved_points or (0, 2) not in moved_selected or
                        (1, 1) in moved_points | moved_selected):
                    continue
                moved = transform_module(base, symmetry, offset)
                assert moved['charge'] == 1
                assert root in ((0, 1), (0, width), (left, 1), (right, width))
                counts['positive_corner' if root[0] == 0 else 'positive_terminal'] += 1
    rotor_candidates = []
    for mirror in (False, True):
        base = transform_module(rotor(), (False, False, mirror))
        for root in base['endpoints']:
            counts['exact_rotor_roles'] += 1
            offset = 1-root[0], 2-root[1]
            moved = transform_module(base, (False, False, False), offset)
            if ((0, 2) in moved['endpoints'] or (0, 2) not in moved['selected'] or
                    (1, 1) in moved['endpoints'] | moved['selected']):
                continue
            assert (2, 0) in moved['endpoints']
            rotor_candidates.append((mirror, offset))
    assert rotor_candidates == [(True, (0, 4))]
    return dict(counts)


def neutral_rectangular_family(first, second):
    modules = [transform_module(rotor(), (False, False, False),
                               (2*row+2*column+1, 2*row-2*column+2*second-1))
               for row in range(first) for column in range(second)]
    network = combine(modules)
    side = 2*(first+second)+4
    current = side, side, network['selected'], network['matching']
    exact = inspect_exact(current, modules)
    regular = inspect_regular(current, modules, require_frozen=False)
    edges = (first-1)*second+first*(second-1)
    cycles = (first-1)*(second-1)
    assert len(network['endpoints']) == 8*first*second
    assert len(network['matching']) == 4*first*second
    assert len(network['selected']) == 4*(first+second)
    assert regular['new_aligned_faces'] == edges
    assert regular['regular_source_events'] == 2*edges
    assert regular['irregular_source_events'] == regular['residual_square_credit'] == 0
    assert exact['event_reserve'] == exact['exact_joint_margin'] == 0
    assert exact['boundary_cost'] == exact['unpaired_rotor_activation'] == 0
    assert regular['half_area']-regular['objective'] == (
        2*first*first+2*second*second+4*first+4*second+8)
    return dict(first=first, second=second, sources=first*second,
                ownership_edges=edges, cycle_rank=cycles,
                matching=len(network['matching']), selected=len(network['selected']),
                reserve=0, margin=0, complete_feasible=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    physical = []
    for name, modules in fixtures():
        for symmetry, phase, _, current, moved in phase_images(modules):
            physical.append(dict(fixture=name, symmetry=symmetry, phase=phase,
                                 **inspect_transfers(current, moved)))
    modules, cycle = neutral_cycle()
    cycle_images = 0
    for _, _, _, current, moved in phase_images(modules):
        inspect_transfers(current, moved)
        cycle_images += 1
    summary = dict(physical_images=len(physical), counted_corners=sum(row['counted'] for row in physical),
                   charging_branches=dict(sum((Counter(row['kinds']) for row in physical), Counter())),
                   zero_reserve_cycle_phase_images=cycle_images, complete_AA_fixture_coverage=0)
    family = [neutral_rectangular_family(first, second) for first, second in
              ((1, 1), (1, 4), (2, 2), (2, 5), (3, 4), (4, 7), (8, 8), (16, 3))]
    summary['zero_reserve_rectangular_family_controls'] = len(family)
    summary['largest_control_cycle_rank'] = max(row['cycle_rank'] for row in family)
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary,
        role_controls=local_roles(), physical=physical, neutral_cycle=cycle,
        neutral_rectangular_family=family,
        scope='Reconstructs actual complete feasible counted phase10 corners and shared activation/H routing; universal role and nonreuse proof is written with scoped Lean statements. Exact neutral rotor cycle refutes only unconditional cycle-payment rule. No AA realization or unrestricted/grid closure.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', summary=summary)))


if __name__ == '__main__':
    main()
