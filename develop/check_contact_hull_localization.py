"""Check feasible contact hulls and actual signed component localization."""

import itertools
import json

from check_closed_extension_reserve import signature
from check_component_receivers import vertices_of
from check_connected_marked_hull_obstruction import modules_at, specifications
from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_exact_event_reserve import fixtures
from check_feasible_core_separator import contact_graph, components
from check_marked_side_gate_consumption import retained_families
from check_source_retention_closure import feasible, hull, implications, marked_counts
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def raw_contact_obstruction_certificate():
    modules = modules_at(24)
    for module, specification in zip(modules, specifications(24)):
        endpoints, support, matching = independent_source(*specification)
        assert endpoints == module['endpoints'] and support == module['selected']
        assert matching == {tuple(sorted(edge)) for edge in module['matching']}
    inside = frozenset({5, 7, 8})
    added = frozenset(range(9))-inside
    graph = contact_graph(modules)
    assert components(graph, added) == [added]
    direct = frozenset().union(*(graph[owner] & inside for owner in added))
    assert direct == {5, 7}
    clauses, _ = implications(modules)
    assert hull(clauses, direct) == inside and feasible(modules, inside)
    assert not feasible(modules, direct)
    assert clauses[(5, 7, 8)] == dict(producer=5, other=7, point=(-36, 4),
                                     neighbor=(-36, 3), anchor=(-35, 4), consumer=8)
    endpoints = {point for owner in inside for point in modules[owner]['endpoints']}
    occupied = {point for owner in inside for point in
                modules[owner]['endpoints'] | modules[owner]['selected']}
    edges = [edge for owner in inside for edge in modules[owner]['matching']]
    assert len(endpoints) == 60 and len(edges) == 30
    assert len({point for edge in edges for point in edge}) == 2*len(edges)
    assert len(occupied-endpoints) == 26
    selected = []
    for owner in sorted(inside):
        for point in sorted(modules[owner]['selected']-endpoints):
            adjacent = set(neighbors(point)) & occupied
            assert len(adjacent) == 1
            neighbor = next(iter(adjacent))
            selected.append(dict(owner_1based=owner+1,
                                 normalized_support=(point[0]+24, point[1]),
                                 normalized_unique_neighbor=(neighbor[0]+24, neighbor[1])))
    assert len(selected) == 26
    return dict(status='PASS', full_fixture='J24', inside_1based=[6, 8, 9],
                added_1based=sorted(owner+1 for owner in added),
                direct_contacts_1based=[6, 8], exact_closure_1based=[6, 8, 9],
                endpoints=60, matching_edges=30, mandatory_selected=26,
                raw_contact_failure=dict(support=(-36, 4), original_producer_1based=6,
                                         anchor=(-35, 4), other_endpoint=(-36, 3),
                                         other_owner_1based=8, forced_consumer_1based=9),
                normalized_selected_certificate=selected,
                scope='Explicit complete physical counterexample to raw-contact feasibility. '
                      'Independent source/matching reconstruction; every mandatory support '
                      'checked. No allocation or grid counterexample claim.')


def plans(modules, families, clauses):
    graph = contact_graph(modules)
    whole = frozenset(range(len(modules)))
    result = []
    for inside in families:
        parts = components(graph, whole-inside)
        for mask in range(1 << len(parts)):
            chosen = [part for index, part in enumerate(parts) if mask >> index & 1]
            added = frozenset().union(*chosen)
            direct = frozenset().union(*(graph[owner] & inside for owner in added))
            core = hull(clauses, direct)
            assert core <= inside
            assert not any(graph[owner] & (inside-core) for owner in added)
            result.append((inside, tuple(parts), mask, added, direct, core))
    return graph, result


def inspect(modules, expected_graph, clauses, cases):
    assert contact_graph(modules) == expected_graph
    cache = {}

    def data(retained):
        if retained not in cache:
            assert feasible(modules, retained)
            current = signature(modules, retained)
            marks = marked_counts(modules, retained)
            endpoints = {point for owner in retained for point in modules[owner]['endpoints']}
            current['activation'] = sum(
                len(vertices_of({tile}) & modules[owner]['endpoints']) == 1 and
                len(vertices_of({tile}) & modules[owner]['selected']) == 2 and
                bool(vertices_of({tile}) & modules[owner]['selected'] & endpoints)
                for owner in retained if modules[owner]['charge'] == 1
                for tile in modules[owner]['receiver'])
            current['positive'] = len(marks)
            current['marks'] = {(owner, side) for owner, sides in marks.items()
                                for side, present in enumerate(sides) if present}
            current['margin'] = len(marks)+current['reserve']-len(current['marks'])
            assert 2*current['reserve'] >= current['activation']
            cache[retained] = current
        return cache[retained]

    checked = strict_cores = raw_failures = negative_collections = 0
    witness = None
    for inside, parts, mask, added, direct, core in cases:
        old, small, full, local = (data(retained) for retained in
                                  (inside, core, inside | added, core | added))
        assert hull(clauses, direct) == core
        for field in ['events', 'full', 'marks']:
            assert full[field] == old[field] | local[field]
            assert small[field] == old[field] & local[field]
        for field in ['reserve', 'positive', 'margin']:
            assert full[field]-old[field] == local[field]-small[field]
        assert local['activation'] >= small['activation']
        deltas = [data(inside | part)['reserve']-old['reserve']
                  for index, part in enumerate(parts) if mask >> index & 1]
        assert sum(deltas) == full['reserve']-old['reserve']
        if deltas and all(change < 0 for change in deltas):
            loss = -sum(deltas)
            assert loss == small['reserve']-local['reserve']
            assert 2*loss <= 2*small['reserve']-small['activation']
            negative_collections += 1
        if not feasible(modules, direct):
            raw_failures += 1
            assert direct < core
            if witness is None:
                endpoints = {point for owner in direct for point in modules[owner]['endpoints']}
                occupied = {point for owner in direct for point in
                            modules[owner]['endpoints'] | modules[owner]['selected']}
                bad = sorted(point for point in occupied-endpoints
                             if len(set(neighbors(point)) & occupied) > 1)
                assert bad
                point = bad[0]
                witness = dict(inside_1based=sorted(owner+1 for owner in inside),
                               added_1based=sorted(owner+1 for owner in added),
                               direct_1based=sorted(owner+1 for owner in direct),
                               closure_1based=sorted(owner+1 for owner in core),
                               restored_support=point,
                               occupied_neighbors=sorted(set(neighbors(point)) & occupied))
        strict_cores += int(core < inside)
        checked += 1
    return dict(contact_subextensions=checked, contact_cores_strictly_smaller_than_old=strict_cores,
                raw_contact_infeasible=raw_failures,
                strictly_losing_component_collections=negative_collections,
                first_raw_contact_obstruction=witness)


def main():
    records = []
    for name, original in fixtures()+[('connected_hull24', modules_at(24)),
                                      ('connected_hull70', modules_at(70))]:
        clauses, _ = implications(original)
        families = retained_families(original, clauses)
        graph, cases = plans(original, families, clauses)
        images = []
        for symmetry in itertools.product((False, True), repeat=3):
            for phase in itertools.product((0, 1), repeat=2):
                moved = [transform_module(module, symmetry, phase) for module in original]
                images.append(inspect(moved, graph, clauses, cases))
        keys = ['contact_subextensions', 'contact_cores_strictly_smaller_than_old',
                'raw_contact_infeasible', 'strictly_losing_component_collections']
        records.append(dict(fixture=name, owners=len(original), images=len(images),
                            **{key: sum(image[key] for image in images) for key in keys},
                            first_image_obstruction=images[0]['first_raw_contact_obstruction']))
    print(json.dumps(dict(status='PASS', fixtures=records,
                         images=sum(row['images'] for row in records),
                         **{key: sum(row[key] for row in records) for key in keys},
                         scope='Actual contact graph and exact Horn closure; complete support '
                         'feasibility of all three retained families; events/full tiles/marks '
                         'union and intersection; signed reserve and margin localization and '
                         'simultaneous local loss bound. Core subsets exhaustive through nine '
                         'owners, deterministic Horn-hull samples above nine; every component '
                         'subunion per tested core; all32phase/isometry images. Finite controls '
                         'supplement general proof. No reserve monotonicity, independent contact '
                         'budgets, full allocation or grid equality claim.'), indent=2))


if __name__ == '__main__':
    main()
