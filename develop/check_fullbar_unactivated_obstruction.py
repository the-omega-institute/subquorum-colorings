"""Reconstruct a complete unactivated full-bar gate and its zero-defect exit."""

from collections import Counter
import itertools
import json

from check_component_receivers import vertices_of
from check_demand_hull_reserve_obstruction import report
from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import inverse_of, original
from check_rotor_transfer_path_endings import physical_case, side_frame
from check_source_retention_closure import feasible, hull, implications, marked_counts
from rotor_networks import affine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


SPECIFICATIONS = [
    ((14, 8, 4), (False, False, False), (0, 0)),
    ((6, 4, 4), (True, False, False), (1, 2)),
    ((6, 4, 4), (False, True, False), (4, 14)),
    ((6, 6, 4), (True, False, False), (1, 7)),
    ((6, 6, 4), (True, True, True), (9, 13)),
    ((6, 8, 4), (True, True, True), (14, 6)),
    ((8, 4, 4), (True, True, False), (4, 18)),
    ((10, 4, 4), (True, True, False), (8, 11)),
]


def witness_modules():
    return [original(parameters, symmetry, offset)
            for parameters, symmetry, offset in SPECIFICATIONS]


def fullbar_form(module):
    points = module['endpoints']
    width = max(column for _, column in points)-1
    near = max(row for row, column in points if column == 2)-2
    far = max(row for row, column in points if column == width+1)-2
    if width >= 6 and min(near, far) >= 4 and width % 2 == near % 2 == far % 2 == 0:
        expected = original((width, near, far), offset=(2, 1))
        if all(module[field] == expected[field] for field in ('endpoints', 'selected')):
            return 'horizontal', (width, near, far)
    width = max(row for row, _ in points)-1
    near = max(column for row, column in points if row == 2)-2
    far = max(column for row, column in points if row == width+1)-2
    assert width >= 6 and min(near, far) >= 4
    expected = original((width, near, far), (True, False, False), (1, 2))
    assert all(module[field] == expected[field] for field in ('endpoints', 'selected'))
    return 'vertical', (width, near, far)


def catalogue_controls():
    fixed = {(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (3, 1), (4, 1)}
    cells = vertices_of({(1, 1)})
    counts = Counter()
    prepared = {}
    for dimensions in itertools.product((6, 8, 14), (4, 6, 10), (4, 8)):
        for symmetry in SYMMETRIES:
            oriented = original(dimensions, symmetry)
            for endpoint in oriented['endpoints']:
                moved = transform_module(oriented, (False, False, False),
                                         (3-endpoint[0], 2-endpoint[1]))
                if not cells <= moved['endpoints'] or moved['endpoints'] & fixed:
                    continue
                key = frozenset(moved['endpoints']), frozenset(moved['selected'])
                prepared[key] = moved
    for consumer in prepared.values():
        kind, (width, near, far) = fullbar_form(consumer)
        assert consumer['charge'] == -1
        counts[kind] += 1
        for base_width, base_near in itertools.product((6, 8, 14, 24), (4, 6, 8, 12, 20)):
            base = original((base_width, base_near, 4))
            if base['endpoints'] & consumer['endpoints']:
                continue
            assert width <= base_width-2 if kind == 'horizontal' else near <= base_width-4
            original_occupied = consumer['endpoints'] | consumer['selected']
            if (base_near+1, 2) not in original_occupied:
                assert near <= base_near-4 if kind == 'horizontal' else width <= base_near-2
                forced = (near+3, 2) if kind == 'horizontal' else (width+2, 2)
                assert forced in consumer['selected']
                assert (forced[0], 1) in base['endpoints']
                counts['unactivated_clearance_patterns'] += 1
            counts['endpoint_disjoint_producer_patterns'] += 1
    return dict(anchored_distinct_consumers=len(prepared), counts=dict(counts),
                scope='All anchored endpoint roles and isometries in the explicit dimension '
                      'library, with no translation cutoff after anchoring. Partial patterns '
                      'check the written classification/clearance proof, not completion.')


def inspect_witness(modules, move=lambda point: point):
    retained = set(range(len(modules)))
    clauses, _ = implications(modules)
    assert hull(clauses, {0, 1}) == frozenset(retained)
    assert feasible(modules, retained) and not feasible(modules, {0, 1})
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    assert len(owners) == 184
    gate, terminal = move((3, 2)), move((8, 1))
    terminal_tile = tuple(value//2 for value in terminal)
    supports = {move((8, 0)), move((9, 1))}
    assert supports == modules[0]['selected'] & vertices_of({terminal_tile})
    assert not supports & owners.keys() and owners[gate] == 1
    gate_tile = tuple(value//2 for value in gate)
    assert vertices_of({gate_tile}) <= modules[1]['endpoints']
    side = next(side for side in (0, 1) if side_frame(modules[0], side)[1]((3, 2)) == gate)
    assert marked_counts(modules, retained)[0][side]
    forced = move((8, 2))
    assert forced in modules[1]['selected'] and owners[forced] == 5
    cells = vertices_of({tuple(value//2 for value in forced)})
    assert cells & owners.keys() == {move((8, 2)), move((8, 3))}
    assert modules[5]['endpoints'] & cells == cells & owners.keys()
    assert modules[5]['selected'] & cells == {move((9, 3))}
    assert move((9, 2)) not in set.union(*(module['endpoints'] | module['selected']
                                        for module in modules))
    paths = physical_case(modules, retained)
    return dict(gate_owner=2, forced_support_consumer=6,
                original_terminal_supports_retained=True, gate_marked=True,
                producer_terminal_activated=False, adjacent_final_profile=[2, 1],
                adjacent_profile_owners=1, adjacent_tile_defect=0,
                least_feasible_seed_hull_owners=len(retained), paths=dict(paths))


def main():
    modules = witness_modules()
    witness = inspect_witness(modules)
    physical = report(modules, range(len(modules)))
    assert physical['endpoint_components'] == 1
    assert (physical['positive'], physical['marked'], physical['event_reserve'],
            physical['exact_joint_margin']) == (3, 3, 19, 19)
    inverse = inverse_of(side_frame(modules[0], 0)[1])
    normalized_consumer = {field: {inverse(point) for point in modules[1][field]}
                           for field in ('endpoints', 'selected')}
    assert fullbar_form(normalized_consumer) == ('vertical', (6, 4, 4))
    images = 0
    for symmetry in SYMMETRIES:
        for phase in itertools.product((0, 1), repeat=2):
            transformed = [transform_module(module, symmetry, phase) for module in modules]
            owners = set(range(len(modules)))
            assert feasible(transformed, owners)
            physical_case(transformed, owners)
            if transformed[0]['charge'] == 1:
                move = lambda point: affine(point, symmetry, phase)
                inspect_witness(transformed, move)
                images += 1
    print(json.dumps(dict(status='PASS', witness=witness, physical=physical,
                         specifications=SPECIFICATIONS, catalogue=catalogue_controls(),
                         phase_isometry_images=32, obstruction_preserving_images=images,
                         refutes_fullbar_implies_producer_activation=True,
                         refutes_forced_exit_tile_has_positive_defect=True,
                         refutes_full_allocation=False,
                         scope='Explicit complete connected eight-source counterexample to two '
                               'local rules, with exact original matching/support reconstruction, '
                               'degree feasibility, least Horn hull and actual path ledger. '
                               'The full allocation margin is POSITIVE nineteen. No source-count '
                               'minimality, unrestricted allocation or grid conclusion.'), indent=2))


if __name__ == '__main__':
    main()
