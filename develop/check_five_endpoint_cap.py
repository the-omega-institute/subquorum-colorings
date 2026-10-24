"""Check the cap owner obstruction and actual positive gate-consumer roles."""

from collections import Counter
import itertools
import json

from check_component_receivers import vertices_of
from check_connected_marked_hull_obstruction import modules_at
from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_exact_event_reserve import fixtures
from check_minus_one_tip_obstructions import source
from check_periodic_slab_compression import decode
from check_source_retention_closure import feasible, marked_counts
from dual_guard_compensation import paired_guards
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


TARGET = (2, 2)
BLOCKERS = {(1, 2), (2, 1), (3, 2), (2, 6), (1, 4)}
FOUR_BLOCKERS = BLOCKERS-{(2, 6)}
SYMMETRIES = list(itertools.product((False, True), repeat=3))
DIMENSIONS = list(itertools.product((6, 8, 12, 40), (4, 6, 20, 100), (4, 6, 20, 100)))


def owner_controls():
    images = roles = tips = transverse_roles = transverse_bounds = 0
    for dimensions in DIMENSIONS:
        width, left, right = dimensions
        endpoints, support, matching = independent_source(dimensions, (False, False, False), (0, 0))
        assert {point for edge in matching for point in edge} == endpoints
        assert len(endpoints) == 2*len(matching)
        for symmetry in SYMMETRIES:
            current = {affine(point, symmetry) for point in endpoints}
            terminal = {affine(point, symmetry) for point in [(left, 1), (right, width)]}
            actual_tips = set()
            for point in current:
                adjacent = set(neighbors(point)) & current
                assert adjacent
                if len(adjacent) == 1:
                    actual_tips.add(point)
                    other = next(iter(adjacent))
                    continued = tuple(first+4*(second-first) for first, second in zip(point, other))
                    assert continued in current
                    tips += 1
                offset = tuple(first-second for first, second in zip(TARGET, point))
                assert any(tuple(value-shift for value, shift in zip(blocker, offset)) in current
                           for blocker in BLOCKERS)
                if not any(tuple(value-shift for value, shift in zip(blocker, offset)) in current
                           for blocker in FOUR_BLOCKERS):
                    moved = {tuple(value+shift for value, shift in zip(endpoint, offset))
                             for endpoint in current}
                    assert set(neighbors(TARGET)) & moved == {(2, 3)}
                    height = max(column for row, column in moved if row == 2)-2
                    assert height >= 4 and height % 2 == 0
                    for producer_width in (6, 8, 12, 40):
                        if (2, producer_width) not in moved:
                            assert height <= producer_width-4 and producer_width >= 8
                            transverse_bounds += 1
                    transverse_roles += 1
                roles += 1
            assert actual_tips == terminal
            images += 1
    rotor_images = {}
    for symmetry in SYMMETRIES:
        original = transform_module(rotor(), symmetry)
        for point in original['endpoints']:
            offset = tuple(first-second for first, second in zip(TARGET, point))
            current = frozenset(tuple(value+shift for value, shift in zip(endpoint, offset))
                                for endpoint in original['endpoints'])
            assert TARGET in current and current & FOUR_BLOCKERS
            rotor_images[current] = sorted(current & BLOCKERS)
    assert len(rotor_images) == 16
    gate_images = {}
    producer_ring = {(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (3, 1), (4, 1)}
    survivors = set()
    for symmetry in SYMMETRIES:
        original = transform_module(rotor(), symmetry)
        for point in original['endpoints']:
            offset = tuple(first-second for first, second in zip((3, 2), point))
            current = transform_module(original, (False, False, False), offset)
            key = frozenset(current['endpoints'])
            gate_images[key] = current
            if not current['endpoints'] & producer_ring:
                assert TARGET in current['selected']
                survivors.add(key)
    assert len(gate_images) == 16 and len(survivors) == 2
    return dict(dimension_controls=len(DIMENSIONS), u_isometry_images=images,
                u_endpoint_owner_roles=roles, one_neighbor_terminal_roles=tips,
                transverse_terminal_roles=transverse_roles,
                transverse_height_bound_controls=transverse_bounds,
                complete_rotor_owner_roles=len(rotor_images),
                complete_rotor_gate_roles=len(gate_images),
                endpoint_disjoint_rotor_gate_roles_with_forced_support=len(survivors))


def positive_consumer_controls():
    prepared = []
    for dimensions in DIMENSIONS:
        for symmetry in SYMMETRIES:
            module = transform_module(source(*dimensions), symmetry)
            phases = {phase for phase in itertools.product((0, 1), repeat=2)
                      if transform_module(module, (False, False, False), phase)['charge'] == 1}
            prepared.append((module, phases))
    counts = Counter()
    candidates = 0
    for left, right in itertools.product((4, 6, 20), repeat=2):
        producer = source(6, left, right)
        tile = (1, 1)
        gate = (3, 2)
        corner = (2, 2)
        cells = vertices_of({tile})
        for module, phases in prepared:
            for point in module['endpoints']:
                offset = tuple(first-second for first, second in zip(gate, point))
                if tuple(value % 2 for value in offset) not in phases:
                    continue
                original_points = {tuple(value-shift for value, shift in zip(endpoint, offset))
                                   for endpoint in producer['endpoints']}
                if original_points & module['endpoints']:
                    continue
                moved = {tuple(value+shift for value, shift in zip(endpoint, offset))
                         for endpoint in module['endpoints']}
                profile = moved & cells
                assert len(profile) in (1, 2, 4)
                moved_support = {tuple(value+shift for value, shift in zip(selection, offset))
                                 for selection in module['selected']}
                assert len(profile) in (1, 2) and corner in moved_support
                assert BLOCKERS <= producer['endpoints'] | moved
                assert corner not in producer['endpoints'] | moved
                assert len(set(neighbors(corner)) & (producer['endpoints'] | moved)) == 3
                candidates += 1
                counts[len(profile)] += 1
    first = source(6, 4, 4)
    second = transform_module(first, (False, True, False), (7, -4))
    assert not first['endpoints'] & second['endpoints']
    assert BLOCKERS <= first['endpoints'] | second['endpoints']
    assert TARGET in second['selected']
    assert not feasible([first, second], frozenset((0, 1)))
    return dict(width_six_height_controls=9,
                endpoint_disjoint_positive_consumer_candidates=candidates,
                original_profile_counts=dict(counts), reciprocal_pair_cap='PASS')


def physical_controls():
    images = positive_edges = singleton_edges = zero_singleton_edges = 0
    for _, original in fixtures()+[('connected_hull24', modules_at(24))]:
        for symmetry in SYMMETRIES:
            for phase in itertools.product((0, 1), repeat=2):
                modules = [transform_module(module, symmetry, phase) for module in original]
                whole = frozenset(range(len(modules)))
                assert feasible(modules, whole)
                endpoints = {point: owner for owner, module in enumerate(modules)
                             for point in module['endpoints']}
                activated = set()
                assigned = set()
                for owner, module in enumerate(modules):
                    if module['charge'] != 1:
                        continue
                    for tile in module['receiver']:
                        cells = vertices_of({tile})
                        if len(cells & module['endpoints']) == 1 and len(cells & module['selected']) == 2:
                            if cells & module['selected'] & endpoints.keys():
                                activated.add((owner, tile))
                for producer, sides in marked_counts(modules, whole).items():
                    for marked, (gate, _, _, _) in zip(sides, paired_guards(modules[producer])):
                        if not marked:
                            continue
                        consumer = endpoints[gate]
                        tile = tuple(value//2 for value in gate)
                        cells = vertices_of({tile})
                        profile = cells & modules[consumer]['endpoints']
                        original_support = cells & modules[consumer]['selected']
                        if modules[consumer]['charge'] == 1:
                            positive_edges += 1
                            assert decode(modules[producer])[0][0] >= 8
                        if len(profile) == 1 and len(original_support) == 2:
                            assert original_support & endpoints.keys()
                            if modules[consumer]['charge'] == 1:
                                occurrence = (consumer, tile)
                                assert occurrence not in assigned and occurrence in activated
                                assigned.add(occurrence)
                                singleton_edges += 1
                            else:
                                zero_singleton_edges += 1
                assert len(assigned) <= len(activated)
                images += 1
    return dict(complete_physical_images=images,
                positive_to_positive_gate_edges=positive_edges,
                positive_regular_singleton_gate_consumers=singleton_edges,
                zero_regular_singleton_gate_consumers=zero_singleton_edges,
                scope='The fixture count reports actual conditional coverage, including zero occurrence counts; local owner-role controls and written proofs are separate.')


def main():
    print(json.dumps(dict(status='PASS', owner_roles=owner_controls(),
                         positive_consumers=positive_consumer_controls(),
                         physical=physical_controls(),
                         scope='U parameter controls supplement the all-parameter proof. Rotor ownership exhaustion is over all sixteen roles, not a translation cutoff. No full allocation, grid equality, positive-consumer acyclicity or general noncompletion inference from finite UNSAT.'), indent=2))


if __name__ == '__main__':
    main()
