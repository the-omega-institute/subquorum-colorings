"""Discover/check source-preserving two-row compression with exact defect loss."""

import itertools
import json
import random

from check_activated_singleton_budget import rotor_pairs
from check_closed_extension_reserve import signature
from check_component_receivers import vertices_of
from check_connected_marked_hull_obstruction import modules_at
from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_exact_event_reserve import fixtures
from check_minus_one_tip_obstructions import source
from check_source_retention_closure import feasible, hull, implications, marked_counts
from dual_guard_compensation import paired_guards
from rotor_networks import labeled_module, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def decode(module):
    chosen, anchor, opposite, _ = module['guard']
    column_step = tuple(first-second for first, second in zip(chosen, anchor))
    row_step = tuple(first+step-second for first, step, second in
                     zip(chosen, column_step, opposite))
    offset = tuple(value-3*row-2*column for value, row, column in
                   zip(chosen, row_step, column_step))
    local = lambda point: tuple(sum((value-origin)*step for value, origin, step in
                                    zip(point, offset, direction))
                                for direction in (row_step, column_step))
    endpoints = {local(point) for point in module['endpoints']}
    width = max(column for _, column in endpoints)
    left = max(row for row, column in endpoints if column == 1)
    right = max(row for row, column in endpoints if column == width)
    move = lambda point: tuple(origin+point[0]*row+point[1]*column for origin, row, column in
                               zip(offset, row_step, column_step))
    return (width, left, right), move


def rebuilt_u(module):
    dimensions, move = decode(module)
    width, left, right = dimensions
    assert width >= 6 and min(left, right) >= 4
    assert not any(value % 2 for value in dimensions)
    endpoints, support, matching = independent_source(dimensions, (False, False, False), (0, 0))
    assert {move(point) for point in endpoints} == module['endpoints']
    assert {move(point) for point in support} == module['selected']
    return labeled_module(module['selected'],
                          [tuple(move(point) for point in edge) for edge in matching],
                          module['ports'], module['guard'])


def critical_rows(modules):
    values = set()
    for module in modules:
        if module['guard'] is None:
            features = module['endpoints'] | module['selected']
        else:
            (width, left, right), move = decode(module)
            knots = [(0, 1), (1, width), (2, 1), (left, 1), (2, width), (right, width),
                     (0, 0), (0, width+1), (left+1, 1), (right+1, width),
                     (2, 0), (left, 0), (3, 2), (left-1, 2),
                     (2, width+1), (right, width+1), (3, width-1), (right-1, width-1)]
            features = {move(point) for point in knots}
            features |= {point for side in paired_guards(module) for point in side}
        for tile in module['receiver']:
            cells = vertices_of({tile})
            profile = len(cells & module['endpoints']), len(cells & module['selected'])
            if profile in ((1, 2), (3, 0)):
                features |= cells
        assert len(features) <= 40
        values |= {row for row, _ in features}
    return values


def defects(modules):
    endpoints = {point for module in modules for point in module['endpoints']}
    boundary = {}
    positive_activation = unused_u = unpaired_rotor = 0
    for module in modules:
        for tile in module['receiver']:
            cells = vertices_of({tile})
            profile = len(cells & module['endpoints']), len(cells & module['selected'])
            if module['charge'] == 1 and profile == (1, 2):
                positive_activation += bool(cells & module['selected'] & endpoints)
            if module['guard'] is not None and profile == (3, 0):
                unused_u += not cells <= endpoints
        if module['guard'] is None:
            for triple, (singleton, _) in rotor_pairs(module).items():
                unpaired_rotor += (bool(vertices_of({singleton}) & module['selected'] & endpoints)
                                   and not vertices_of({triple}) <= endpoints)
    for tile in {tile for module in modules for tile in module['receiver']}:
        cells = vertices_of({tile})
        originals = [module for module in modules if tile in module['receiver']]
        profiles = [(len(cells & module['endpoints']), len(cells & module['selected']))
                    for module in originals]
        amount = len(cells & endpoints)
        value = int(amount == 1 and profiles == [(1, 1)])
        value += 2*int(amount == 2 and profiles == [(2, 0)])
        if amount == 2 and profiles == [(1, 1), (1, 1)]:
            events = sum(len((set(neighbors(point)) & cells & endpoints)-
                             module['endpoints']-module['selected'])
                         for module in originals for point in cells & module['endpoints'])
            value += 2*int(events == 0)
        value += int(amount == 3 and len(originals) > 1)
        if value:
            boundary[tile] = value
    reserve = signature(modules, frozenset(range(len(modules))))['reserve']
    assert 2*reserve == positive_activation+unused_u+unpaired_rotor+sum(boundary.values())
    return (positive_activation, unused_u, unpaired_rotor), boundary, reserve


def cut_at(modules):
    features = critical_rows(modules)
    forbidden = {coordinate+step for coordinate in features for step in range(-4, 5)}
    occupied_rows = [row for module in modules
                     for row, _ in module['endpoints'] | module['selected']]
    return next((row for row in range(min(occupied_rows), max(occupied_rows))
                 if row % 2 == 0 and row not in forbidden and row+1 not in forbidden), None)


def canonical_demand_hull(modules, clauses):
    owners = {point: owner for owner, module in enumerate(modules) for point in module['endpoints']}
    marks = marked_counts(modules, frozenset(range(len(modules))))
    seed = set(marks)
    for owner, sides in marks.items():
        for marked, (gate, _, _, _) in zip(sides, paired_guards(modules[owner])):
            assert marked == (gate in owners)
            if marked:
                seed.add(owners[gate])
    return hull(clauses, seed)


def compress_once(modules, cut):
    def move(point):
        row, column = point
        assert row not in (cut, cut+1)
        return row-2*int(row >= cut+2), column

    transformed = []
    for module in modules:
        for key in ('endpoints', 'selected'):
            rows = {row: {column for current, column in module[key] if current == row}
                    for row in (cut-1, cut, cut+1, cut+2)}
            assert rows[cut-1] == rows[cut+1] and rows[cut] == rows[cut+2]
        points = lambda values: {move(point) for point in values if point[0] not in (cut, cut+1)}
        if module['guard'] is None:
            assert not any(point[0] in (cut, cut+1)
                           for point in module['endpoints'] | module['selected'])
            current = labeled_module(points(module['selected']),
                                     [tuple(move(point) for point in edge) for edge in module['matching']],
                                     points(module['ports']))
        else:
            current = dict(module, endpoints=points(module['endpoints']),
                           selected=points(module['selected']), ports=points(module['ports']),
                           guard=tuple(move(point) for point in module['guard']))
            current = rebuilt_u(current)
        assert current['charge'] > 0 if module['charge'] > 0 else current['charge'] <= 0
        transformed.append(current)
    whole = frozenset(range(len(modules)))
    assert feasible(modules, whole) and feasible(transformed, whole)
    assert set(implications(modules)[0]) == set(implications(transformed)[0])
    for family in (modules, transformed):
        endpoints = {point for module in family for point in module['endpoints']}
        occupied = {point for module in family for point in module['endpoints'] | module['selected']}
        assert len(endpoints) == sum(len(module['endpoints']) for module in family)
        assert all(len(set(neighbors(point)) & occupied) >= 3 for point in endpoints)
    assert marked_counts(modules, whole) == marked_counts(transformed, whole)
    special, boundary, reserve = defects(modules)
    new_special, new_boundary, new_reserve = defects(transformed)
    assert special == new_special
    removed = sum(value for (row, _), value in boundary.items() if row == cut//2)
    assert 2*(reserve-new_reserve) == removed >= 0
    moved_boundary = {(row-int(2*row >= cut+2), column): value
                      for (row, column), value in boundary.items() if row != cut//2}
    assert new_boundary == moved_boundary
    return transformed, dict(cut=cut, reserve_before=reserve, reserve_after=new_reserve,
                             removed_boundary_defect=removed)


def compress(modules):
    operations = []
    original = modules
    for axis in (0, 1):
        if axis:
            modules = [transform_module(module, (True, False, False)) for module in modules]
        while (cut := cut_at(modules)) is not None:
            modules, record = compress_once(modules, cut)
            operations.append(dict(axis=axis, **record))
        if axis:
            modules = [transform_module(module, (True, False, False)) for module in modules]
    occupied = {point for module in modules for point in module['endpoints'] | module['selected']}
    shape = [max(point[axis] for point in occupied)-min(point[axis] for point in occupied)+1
             for axis in (0, 1)]
    assert max(shape) <= 512*len(modules)+2
    whole = frozenset(range(len(modules)))
    assert marked_counts(original, whole) == marked_counts(modules, whole)
    clauses = implications(original)[0]
    canonical = canonical_demand_hull(original, clauses)
    assert canonical == canonical_demand_hull(modules, implications(modules)[0])
    if len(modules) <= 9:
        seeds = [{owner for owner in whole if mask >> owner & 1}
                 for mask in range(1 << len(modules))]
    else:
        generator = random.Random(20261021)
        seeds = [set(), set(whole)]+[{owner} for owner in whole]
        seeds += [{owner for owner in whole if generator.randrange(2)} for _ in range(96)]
    legal = {hull(clauses, seed) for seed in seeds} | {canonical}
    for retained in legal:
        assert feasible(original, retained) and feasible(modules, retained)
        assert marked_counts(original, retained) == marked_counts(modules, retained)
        assert signature(modules, retained)['reserve'] <= signature(original, retained)['reserve']
    return dict(owners=len(modules), operations=len(operations), shape=shape,
                legal_restriction_controls=len(legal),
                reserve_before=signature(original, whole)['reserve'],
                reserve_after=signature(modules, whole)['reserve'],
                canonical_hull_owners_1based=sorted(owner+1 for owner in canonical),
                canonical_hull_reserve_before=signature(original, canonical)['reserve'],
                canonical_hull_reserve_after=signature(modules, canonical)['reserve'],
                strict_steps=sum(row['reserve_after'] < row['reserve_before'] for row in operations),
                removed_boundary_defect=sum(row['removed_boundary_defect'] for row in operations))


def main():
    records = []
    cases = fixtures()+[('connected_hull24', modules_at(24)),
                        ('connected_hull70', modules_at(70))]
    cases += [('asymmetric_%d_%d_%d' % parameters, [source(*parameters)])
              for parameters in ((6, 100, 4), (100, 4, 6), (40, 60, 100))]
    for name, original in cases:
        images = []
        for symmetry in itertools.product((False, True), repeat=3):
            for phase in itertools.product((0, 1), repeat=2):
                modules = [transform_module(module, symmetry, phase) for module in original]
                images.append(compress(modules))
        records.append(dict(fixture=name, images=len(images),
                            operations=sum(row['operations'] for row in images),
                            legal_restriction_controls=sum(row['legal_restriction_controls'] for row in images),
                            strict_steps=sum(row['strict_steps'] for row in images),
                            removed_boundary_defect=sum(row['removed_boundary_defect'] for row in images),
                            example=images[0]))
    print(json.dumps(dict(status='PASS', fixtures=records,
                         **{key: sum(row[key] for row in records) for key in
                            ('images', 'operations', 'strict_steps', 'removed_boundary_defect',
                             'legal_restriction_controls')},
                         scope='Full complete sources in all 32 phase/isometry images. '
                         'Every step reconstructs allowed U dimensions and original matching, '
                         'checks source-coloured seam periodicity, full feasibility, identical '
                         'original-owner Horn clause keys, exact '
                         'side indicators, unchanged A/U0/Z0, actual tile defect transport '
                         'and 2(Rold-Rnew)=Hdeleted. Asymmetric dimensions included. '
                         'Final legal restrictions exhaustive through nine owners, '
                         'deterministic seed-hull samples beyond: exact mark preservation '
                         'and pointwise nonincreasing reserve. '
                         'This supplements the written general compression theorem, not '
                         'an allocation or arbitrary-grid proof.'), indent=2))


if __name__ == '__main__':
    main()
