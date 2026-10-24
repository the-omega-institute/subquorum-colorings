"""Phase10 forced-point roles and complete full-pair exit controls."""

import argparse
import itertools
import json
from pathlib import Path

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_degree_three_fusion import phase_images
from check_exact_event_reserve import inspect_exact
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_neutral_port_turning import inspect_curves
from check_neutral_support_injection import inspect_joint
from check_promotion_cores import frozen_certificate
from check_regular_tile_compensation import inspect as inspect_regular
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def family(active, incoming):
    assert active % 2 == incoming % 2 == 0 and incoming >= 6 and active >= incoming+4
    return [transform_module(source(14, active, 4), (False, False, False), (2-active, -1)),
            transform_module(source(6, 4, 4), (True, True, False), (1, 5)),
            transform_module(source(6, incoming, 4), (False, False, False), (1-incoming, 0))]


def support_range_controls(active, incoming):
    modules = [transform_module(module, (False, False, False), (-1, -1))
               for module in family(active, incoming)]
    expected = [
        {(1-active, -2), (1-active, 13), (2, -1), (6-active, 12),
         (3-active, 13), (5-active, 13), (4-active, 11)}
        | {(row, -2) for row in range(3-active, 2, 2)}
        | {(row, 0) for row in range(4-active, 1, 2)},
        {(0, 4), (7, 4), (1, -1), (6, -1), (0, 2),
         (0, 0), (2, 1), (7, 2), (7, 0), (5, 1)},
        {(-incoming, -1), (-incoming, 6), (1, 0), (5-incoming, 5),
         (2-incoming, 6), (4-incoming, 6), (3-incoming, 4)}
        | {(row, -1) for row in range(2-incoming, 1, 2)}
        | {(row, 1) for row in range(3-incoming, 0, 2)}]
    assert [module['selected'] for module in modules] == expected
    return sum(map(len, expected))


def local_role_controls():
    fixed = {(2, 0), (1, 0), (0, 0), (2, 1), (2, 2)}
    candidates = surviving = tile_adapters = 0
    for dimensions in ((6, 4, 4), (8, 6, 12), (14, 12, 4), (20, 4, 16),
                       (40, 30, 16), (6, 100, 4)):
        width, left, right = dimensions
        base = source(*dimensions)
        for symmetry in itertools.product((False, True), repeat=3):
            for anchor in base['endpoints']:
                root = affine(anchor, symmetry)
                offset = 1-root[0], 1-root[1]
                module = transform_module(base, symmetry, offset)
                transpose, flip_row, flip_column = symmetry
                canonical_cells = set()
                for row, column in vertices_of({(0, 0)}):
                    delta = (column-1, row-1) if transpose else (row-1, column-1)
                    canonical_cells.add((anchor[0]+(-delta[0] if flip_row else delta[0]),
                                         anchor[1]+(-delta[1] if flip_column else delta[1])))
                origin = (min(point[0] for point in canonical_cells),
                          min(point[1] for point in canonical_cells))
                assert canonical_cells == {(origin[0]+row, origin[1]+column)
                                           for row, column in itertools.product((0, 1), repeat=2)}
                assert origin == (anchor[0]-(0 if flip_row else 1),
                                  anchor[1]-(0 if flip_column else 1))
                assert (phase_of(module) == '10') == (origin[0] % 2 == 1 and origin[1] % 2 == 0)
                tile_adapters += 1
                if phase_of(module) != '10':
                    continue
                candidates += 1
                if module['endpoints'] & fixed:
                    continue
                surviving += 1
                assert anchor in ((left, 1), (right, width))
                predecessor = affine((anchor[0]-1, anchor[1]), symmetry, offset)
                other_leg_column = width if anchor[1] == 1 else 1
                other_tip = affine((anchor[0], other_leg_column), symmetry, offset)
                assert predecessor == (0, 1)
                assert other_tip[0] == 1 and other_tip[1] > 1
                cells = vertices_of({tile_of((1, 1))})
                assert cells & module['endpoints'] == {(0, 1), (1, 1)}
    assert surviving > 0
    collisions = []
    for active, incoming in itertools.product(range(4, 24, 2), range(4, 24, 2)):
        parent = transform_module(source(14, active, 4), (False, False, False),
                                  (2-active, -1))
        child = transform_module(source(6, incoming, 4), (False, False, False),
                                 (1-incoming, 0))
        if not parent['endpoints'] & child['endpoints']:
            assert incoming+4 <= active
        if active < incoming+4:
            assert parent['endpoints'] & child['endpoints']
            collisions.append(dict(active=active, incoming=incoming,
                                   collision=min(parent['endpoints'] & child['endpoints'])))
    return dict(transported_tile_adapter_images=tile_adapters,
                phase10_endpoint_candidates=candidates, surviving_north_terminal_roles=surviving,
                height_collision_cases=len(collisions), collisions=collisions)


def fixed_witness():
    modules = family(10, 6)
    assert [phase_of(module) for module in modules] == ['01', '01', '10']
    endpoints = combine(modules)['endpoints']
    assert vertices_of({(0, 0)}) <= endpoints
    assert vertices_of({(0, 0)}) & modules[2]['endpoints'] == {(0, 1), (1, 1)}
    current, moved = contained(modules)
    joint = inspect_joint(current, moved)
    exact = inspect_exact(current, moved)
    regular = inspect_regular(current, moved, require_frozen=False)
    frozen, _ = frozen_certificate(current)
    network = combine(moved)
    assert len(frozen) == len(network['endpoints']) == 78
    assert (len(current[3]), len(current[2]), current[:2]) == (39, 27, (18, 18))
    assert joint['forced_owner_phases'] == {'10': 1}
    assert joint['forced_contacts'] == 1
    assert joint['regular_stops'] == joint['forced_Pneg_reserved'] == 0
    assert exact['boundary_cost'] == 12 and exact['event_reserve'] == exact['exact_joint_margin'] == 6
    assert regular['half_area']-regular['objective'] == 96
    return dict(active=10, incoming=6, shape=current[:2], endpoints=78, matching_edges=39,
                retained_supports=27, frozen_endpoints=78, exact=exact, joint=joint,
                ambient_slack=96,
                source_specifications=[dict(dimensions=(14, 10, 4), symmetry=(False, False, False),
                                            offset=(-8, -1)),
                                       dict(dimensions=(6, 4, 4), symmetry=(True, True, False),
                                            offset=(1, 5)),
                                       dict(dimensions=(6, 6, 4), symmetry=(False, False, False),
                                            offset=(-5, 0))])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    physical = []
    support_coordinates = 0
    for incoming, gap in itertools.product((6, 8, 12, 20), (4, 6, 10)):
        active = incoming+gap
        modules = family(active, incoming)
        support_coordinates += support_range_controls(active, incoming)
        for symmetry, phase, _, current, moved in phase_images(modules):
            joint = inspect_joint(current, moved)
            curves = inspect_curves(current, moved)
            assert not curves['closed_components']
            if [phase_of(module) for module in moved] == ['01', '01', '10']:
                assert joint['forced_contacts'] == 1
                assert joint['forced_owner_phases'] == {'10': 1}
                assert joint['regular_stops'] == joint['forced_Pneg_reserved'] == 0
            physical.append(dict(active=active, incoming=incoming, gap=gap, symmetry=symmetry,
                                 phase=phase, forced_contacts=joint['forced_contacts'],
                                 full_forced_receivers=joint['forced_contacts']-joint['regular_stops'],
                                 forced_pool_reservations=joint['forced_Pneg_reserved'],
                                 closed_components=len(curves['closed_components']),
                                 complete_feasible=True))
    summary = dict(parameter_cases=12, complete_feasible_images=len(physical),
                   full_forced_receivers=sum(row['full_forced_receivers'] for row in physical),
                   independently_reconstructed_original_support_coordinates=support_coordinates,
                   complete_closed01_contact_coverage=0, complete_AA_coverage=0)
    result = dict(status='PASS', summary=summary, roles=local_role_controls(),
                  explicit_witness=fixed_witness(), physical=physical,
                  refuted_rule='A full neutral01 forced receiver always places its forced point in the U-only Pneg reservation pool.',
                  scope='Written arbitrary-dimension role/height proof and all-parameter complete-family feasibility. Finite role, height and family/isometry controls; explicit source reconstruction and freezing audit. No global mixed-chain descent, new uniform coefficient, AA realization or grid counterexample.')
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', summary=summary)))


if __name__ == '__main__':
    main()
