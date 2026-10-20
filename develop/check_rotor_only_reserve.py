"""Exact rotor-role controls and complete rectangular rotor-family checks."""

import argparse
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_regular_tile_compensation import inspect
from rotor_networks import combine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def source_at(owner):
    mirror, row, column = owner
    return transform_module(rotor(), (False, False, mirror), (row, column))


def possible_owners(target, existing):
    occupied = set.union(set(), *(source_at(owner)['endpoints'] for owner in existing))
    result = set()
    for mirror in (False, True):
        for endpoint in rotor()['endpoints']:
            owner = (mirror, target[0]-endpoint[0],
                     target[1]-(-endpoint[1] if mirror else endpoint[1]))
            if not source_at(owner)['endpoints'] & occupied:
                result.add(owner)
    return sorted(result)


def role_controls():
    cases = [
        ((1, 3), [(False, 0, 0)],
         [(False, -3, 0), (False, -2, 2), (True, -3, 6)]),
        ((1, 1), [(False, 0, 0), (False, -3, 0)],
         [(False, -1, -3), (True, -2, 2)]),
        ((2, 1), [(False, 0, 0), (False, -3, 0), (True, -2, 2)], []),
        ((0, 0), [(False, 0, 0), (False, -3, 0), (False, -1, -3)],
         [(False, -4, -3)]),
        ((1, 4), [(False, 0, 0), (True, -3, 6)], [(True, -1, 8)]),
        ((3, 4), [(False, 0, 0), (True, -3, 6), (True, -1, 8)],
         [(False, 2, 2)]),
    ]
    records = []
    for index, (target, existing, expected) in enumerate(cases):
        actual = possible_owners(target, existing)
        assert set(actual) == set(expected)
        endpoints = set.union(set(), *(source_at(owner)['endpoints'] for owner in existing))
        selected = set.union(set(), *(source_at(owner)['selected'] for owner in existing))
        anchors = set(neighbors(target)) & endpoints
        if index:
            assert target in selected-endpoints and len(anchors) >= 2
        records.append(dict(target=target, existing=existing, owners=actual,
                            persistent_neighbors=sorted(anchors), forced_support=bool(index)))
    source = rotor()
    quarter = lambda point: (point[1], 5-point[0])
    assert {quarter(point) for point in source['endpoints']} == source['endpoints']
    assert {quarter(point) for point in source['selected']} == source['selected']
    return records


def index_difference(point):
    row, column = point
    if (row+column) % 4 or (row-column) % 4:
        return None
    return (row+column)//4, (row-column)//4


def family_role_controls():
    source = rotor()
    endpoints, selected = source['endpoints'], source['selected']
    for points in (endpoints, selected):
        differences = {index_difference((first[0]-second[0], first[1]-second[1]))
                       for first in points for second in points}
        differences.discard(None)
        assert differences == {(0, 0)}
    groups = {
        (0, 2): ((-1, 0), 0, -1), (1, 1): ((-1, 0), 0, -1),
        (1, 4): ((0, -1), 1, -1), (2, 5): ((0, -1), 1, -1),
        (4, 4): ((1, 0), 0, 1), (5, 3): ((1, 0), 0, 1),
        (3, 0): ((0, 1), 1, 1), (4, 1): ((0, 1), 1, 1),
    }
    records = []
    for point in sorted(selected):
        consumers = {index_difference((point[0]-endpoint[0], point[1]-endpoint[1]))
                     for endpoint in endpoints}
        consumers.discard(None)
        expected, axis, direction = groups[point]
        assert consumers == {expected}
        anchor = next(iter(set(neighbors(point)) & endpoints))
        blockers = {index_difference((neighbor[0]-occupied[0], neighbor[1]-occupied[1]))
                    for neighbor in neighbors(point) if neighbor != anchor
                    for occupied in endpoints | selected}
        blockers.discard(None)
        assert all(offset[axis] == direction for offset in blockers)
        records.append(dict(support=point, anchor=anchor, consumers=sorted(consumers),
                            possible_extra_neighbor_sources=sorted(blockers),
                            outward_axis=axis, outward_direction=direction))
    return records


def negative_array(first_size, second_size):
    return [source_at((False, 2*first+2*second, 2*first-2*second))
            for first in range(first_size) for second in range(second_size)]


def analyze_rotors(modules):
    assert all(len(module['endpoints']) == 8 for module in modules)
    negative = [module for module in modules if module['charge'] == -2]
    centers = []
    chirality = {}
    reference = rotor()['endpoints']
    for module in negative:
        full = [square for square in module['receiver']
                if {(2*square[0]+row, 2*square[1]+column)
                    for row in (0, 1) for column in (0, 1)} <= module['endpoints']]
        assert len(full) == 1
        center = full[0]
        centers.append(center)
        translated = {(point[0]-2*(center[0]-1), point[1]-2*(center[1]-1))
                      for point in module['endpoints']}
        chirality[center] = translated == reference
    assert len(set(centers)) == len(centers)
    remaining = set(centers)
    components = []
    while remaining:
        seed = min(remaining)
        component = {seed}
        queue = [seed]
        remaining.remove(seed)
        while queue:
            center = queue.pop()
            for row_step, column_step in itertools.product((-1, 1), repeat=2):
                other = center[0]+row_step, center[1]+column_step
                if other in remaining:
                    remaining.remove(other)
                    component.add(other)
                    queue.append(other)
        assert len({chirality[center] for center in component}) == 1
        rotated = {((point[0]-seed[0]+point[1]-seed[1])//2,
                    (point[0]-seed[0]-point[1]+seed[1])//2) for point in component}
        first = range(min(point[0] for point in rotated), max(point[0] for point in rotated)+1)
        second = range(min(point[1] for point in rotated), max(point[1] for point in rotated)+1)
        assert rotated == set(itertools.product(first, second))
        components.append((len(first), len(second)))
    network = combine(modules)
    shift = tuple(2*(-min(point[axis] for point in network['endpoints'] | network['selected'])//2+1)
                  for axis in range(2))
    moved = [transform_module(module, (False, False, False), shift) for module in modules]
    network = combine(moved)
    shape = tuple(2*(max(point[axis] for point in network['endpoints'] | network['selected'])//2+1)
                  for axis in range(2))
    result = inspect((*shape, network['selected'], network['matching']), moved, require_frozen=False)
    vertices = len(negative)
    edges = sum((first-1)*second+first*(second-1) for first, second in components)
    faces = sum((first-1)*(second-1) for first, second in components)
    assert vertices-edges+faces == len(components)
    assert result['irregular_source_events'] == 2*edges
    assert result['residual_square_credit'] >= 2*faces
    reserve = 2*vertices+result['residual_square_credit']-result['irregular_source_events']
    assert reserve >= 2*len(components)
    assert result['half_area']-result['objective'] >= 2*len(components)
    if len(negative) == len(modules):
        assert result['residual_square_credit'] == 2*faces
        assert reserve == 2*len(components)
    return dict(negative_rotors=vertices, zero_rotors=len(modules)-vertices,
                components=components, edges=edges, faces=faces, reserve=reserve,
                irregular=result['irregular_source_events'],
                credit=result['residual_square_credit'],
                actual_slack=result['half_area']-result['objective'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    roles = role_controls()
    supports = family_role_controls()
    records = []
    for first, second in itertools.product((1, 2, 3, 5, 8), repeat=2):
        modules = negative_array(first, second)
        record = analyze_rotors(modules)
        assert record['negative_rotors'] == first*second
        assert record['irregular'] == 4*first*second-2*first-2*second
        assert record['credit'] == 2*(first-1)*(second-1) and record['reserve'] == 2
        network = combine(modules)
        assert len(network['endpoints']) == 8*first*second
        assert len(network['selected']) == 4*(first+second)
        records.append(dict(kind='negative_rectangle', first=first, second=second, **record))
    for symmetry in itertools.product((False, True), repeat=3):
        for phase in itertools.product(range(2), repeat=2):
            modules = [transform_module(module, symmetry, phase) for module in negative_array(3, 4)]
            records.append(dict(kind='all_isometries_phases', symmetry=symmetry, phase=phase,
                                **analyze_rotors(modules)))
    modules = negative_array(2, 3)
    modules += [source_at((True, 50, 55)), source_at((False, 80, 81)),
                source_at((False, 100, 101)), source_at((False, 102, 103))]
    records.append(dict(kind='separated_mixed_components', **analyze_rotors(modules)))
    modules = negative_array(2, 3)+[source_at((False, -4, -1))]
    records.append(dict(kind='actual_negative_zero_support_contact', **analyze_rotors(modules)))
    summary = dict(exact_owner_tables=len(roles), exact_family_support_roles=len(supports),
                   physical_fusions=len(records),
                   negative_rectangle_parameters=25,
                   nonnegative_reserve=sum(record['reserve'] >= 0 for record in records))
    arguments.output.write_text(json.dumps(dict(status='PASS', summary=summary,
        owner_roles=roles, family_support_roles=supports, physical=records,
        scope='Six complete16-role classifications and exact all-index family support-role differences. Physical fixtures control the written finite-propagation/rectangle theorem; their bounded sizes do not prove it.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **summary)))


if __name__ == '__main__':
    main()
