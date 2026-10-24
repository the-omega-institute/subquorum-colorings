"""Reconstruct physical S/P/R transfers and the remaining negative-U path debt."""

from collections import Counter
import itertools
import json

from check_component_receivers import vertices_of
from check_connected_marked_hull_obstruction import modules_at
from check_exact_event_reserve import fixtures
from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import inverse_of, original, protected_fixtures
from check_periodic_slab_compression import decode, defects
from check_source_retention_closure import feasible, implications, marked_counts
from check_marked_side_gate_consumption import retained_families
from dual_guard_compensation import paired_guards
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


ROTOR_POINTS = {(3, 2), (4, 2), (4, 3), (4, 4),
                (5, 1), (5, 2), (5, 3), (6, 3)}
OTHER_ROTOR = {(3, 2), (3, 3), (4, 3), (5, 3),
               (2, 4), (3, 4), (4, 4), (4, 5)}


def side_frame(module, side):
    (width, near, far), move = decode(module)
    if side == 0:
        return (width, near, far), move
    return (width, far, near), lambda point: move((point[0], width+1-point[1]))


def normalized(module, inverse):
    return {field: {inverse(point) for point in module[field]}
            for field in ('endpoints', 'selected')}


def compare_original(module, expected):
    assert all(module[field] == expected[field] for field in ('endpoints', 'selected'))


def transverse(module):
    points = module['endpoints']
    height = max(column for row, column in points if row == 2)-2
    width = max(row for row, _ in points)-1
    far = height+2-min(column for row, column in points if row == width+1)
    compare_original(module, original((width, height, far),
                                     (True, True, False), (1, height+2)))
    return width, height, far


def trace_paths(vertices, edges, marked, activated):
    incoming = {target: source for source, (target, _) in edges.items()}
    assert len(incoming) == len(edges)
    assert set(edges) <= marked and set(incoming) <= activated
    visited = set()
    bad = surplus = cycles = 0
    paths = []
    for start in sorted(vertices-incoming.keys()):
        path = [start]
        while path[-1] in edges:
            path.append(edges[path[-1]][0])
            assert path[-1] not in path[:-1]
        assert not set(path) & visited
        visited.update(path)
        sink = path[-1]
        unpaid = sink in marked and start not in activated
        unused = (1+int(start in activated)) if sink not in marked else 0
        if unpaid and len(path) > 1:
            assert edges[start][1] == 'P'
        bad += unpaid
        surplus += unused
        paths.append(dict(vertices=path, bad=bool(unpaid), surplus=unused))
    for start in sorted(vertices-visited):
        if start in visited:
            continue
        current = start
        cycle = set()
        while current not in cycle:
            assert current not in visited and current in edges
            cycle.add(current)
            current = edges[current][0]
        assert current == start
        visited.update(cycle)
        cycles += 1
    assert visited == vertices
    assert len(vertices)+len(activated)-2*len(marked) == surplus-bad
    return dict(bad=bad, surplus=surplus, cycles=cycles, paths=paths)


def physical_case(modules, retained):
    chosen = [modules[index] for index in sorted(retained)]
    assert feasible(modules, retained)
    owners = {point: owner for owner in retained for point in modules[owner]['endpoints']}
    assert len(owners) == sum(len(modules[owner]['endpoints']) for owner in retained)
    sides = {}
    terminal_vertices = {}
    marked = set()
    activated = set()
    edges = {}
    counts = Counter()
    marks = marked_counts(modules, retained)
    for owner, owner_marks in marks.items():
        for side, is_marked in enumerate(owner_marks):
            dimensions, move = side_frame(modules[owner], side)
            width, near, far = dimensions
            vertex = owner, side
            gate, terminal = move((3, 2)), move((near, 1))
            assert gate == paired_guards(modules[owner])[side][0]
            sides[vertex] = dimensions, move
            assert terminal not in terminal_vertices
            terminal_vertices[terminal] = vertex
            tile = tuple(value//2 for value in terminal)
            if vertices_of({tile}) & modules[owner]['selected'] & owners.keys():
                activated.add(vertex)
            assert is_marked == (gate in owners)
            if is_marked:
                marked.add(vertex)
    for vertex in sorted(marked):
        dimensions, move = sides[vertex]
        width, near, far = dimensions
        inverse = inverse_of(move)
        gate = move((3, 2))
        consumer_owner = owners[gate]
        consumer = modules[consumer_owner]
        points = normalized(consumer, inverse)
        if consumer['charge'] == 1:
            profile = len(vertices_of({(1, 1)}) & points['endpoints'])
            if profile == 1:
                target = terminal_vertices[gate]
                assert vertex in activated
                channel = 'S'
            else:
                assert profile == 2
                incident = max(column for row, column in points['endpoints'] if row == 3)-2
                target = terminal_vertices[move((3, incident+2))]
                channel = 'P'
        elif consumer['guard'] is None:
            assert points['endpoints'] == ROTOR_POINTS and consumer['charge'] < 0
            assert near == 4 and vertex in activated
            cross = normalized(modules[owners[move((2, 2))]], inverse)
            _, height, _ = transverse(cross)
            companion_owner = owners[move((3, 3))]
            companion = normalized(modules[companion_owner], inverse)
            companion_width = max(row for row, _ in companion['endpoints'])-2
            incident = max(column for row, column in companion['endpoints'] if row == 3)-3
            companion_far = incident+3-min(column for row, column in companion['endpoints']
                                         if row == companion_width+2)
            compare_original(companion, original((companion_width, incident, companion_far),
                                                (True, True, False), (2, incident+3)))
            assert 4 <= incident <= height-4 and height <= width-4
            assert width >= 12 and modules[companion_owner]['charge'] == 1
            target = terminal_vertices[move((3, 3))]
            channel = 'R'
        else:
            assert consumer['charge'] < 0 and consumer['guard'] is not None
            counts['negative_U_sinks'] += 1
            continue
        assert target in activated and target not in {target for target, _ in edges.values()}
        edges[vertex] = target, channel
        counts[channel] += 1
    vertices = set(sides)
    result = trace_paths(vertices, edges, marked, activated)
    for vertex, (target, channel) in edges.items():
        if channel != 'P' or target not in edges:
            continue
        next_target, next_channel = edges[target]
        _, height, _ = transverse(normalized(
            modules[owners[sides[vertex][1]((2, 2))]], inverse_of(sides[vertex][1])))
        if next_channel == 'P':
            assert sides[next_target][0][0] <= height-4 <= sides[vertex][0][0]-8
            counts['consecutive_PP'] += 1
        elif next_channel == 'S':
            raise AssertionError('A P->S transition contradicts the transverse column/bar enclosure')
        else:
            assert sides[target][0][1] == 4
            assert sides[next_target][0][1] >= 6
            assert sides[target][0][0] >= 14
            counts['consecutive_PR'] += 1
    activation_counts, boundary, reserve = defects(chosen) if chosen else ((0, 0, 0), {}, 0)
    assert activation_counts[0] == len(activated)
    capacity = sum(activation_counts[1:])+sum(boundary.values())
    margin = len(vertices)//2+reserve-len(marked)
    assert 2*margin == capacity+result['surplus']-result['bad']
    counts.update(physical_paths=len(result['paths']), physical_cycles=result['cycles'],
                  bad_paths=result['bad'], unmarked_surplus=result['surplus'])
    return counts


def rotor_role_controls():
    gate_images = {}
    for symmetry in SYMMETRIES:
        moved = transform_module(rotor(), symmetry)
        for endpoint in moved['endpoints']:
            current = transform_module(moved, (False, False, False),
                                       (3-endpoint[0], 2-endpoint[1]))
            gate_images[frozenset(current['endpoints'])] = current
    blockers = {(1, 1), (1, 2), (1, 3), (1, 4), (2, 1), (3, 1), (4, 1)}
    survivors = [module for points, module in gate_images.items() if not points & blockers]
    assert len(gate_images) == 16
    assert {frozenset(module['endpoints']) for module in survivors} == {
        frozenset(ROTOR_POINTS), frozenset(OTHER_ROTOR)}
    actual = next(module for module in survivors if module['endpoints'] == ROTOR_POINTS)
    assert actual['charge'] < 0 and {(2, 2), (3, 4)} <= actual['selected']
    companion_roles = 0
    companion_footprints = set()
    for symmetry in SYMMETRIES:
        moved = transform_module(rotor(), symmetry)
        for endpoint in moved['endpoints']:
            current = transform_module(moved, (False, False, False),
                                       (3-endpoint[0], 3-endpoint[1]))
            own_neighbors = current['endpoints'] & {(2, 3), (3, 2), (4, 3), (3, 4)}
            if own_neighbors == {(3, 4)}:
                assert current['endpoints'] & {(2, 4), (4, 4)}
                companion_roles += 1
                companion_footprints.add(frozenset(current['endpoints']))
    return dict(all_rotor_gate_footprints=16, endpoint_disjoint_survivors=2,
                permitted_after_forced_tip=1,
                excluded_companion_rotor_role_images=companion_roles,
                excluded_companion_rotor_footprints=len(companion_footprints))


def interval_controls():
    consecutive_pairs = pair_singletons = rotor_companions = shifted_companions = 0
    for width, height, next_width in itertools.product(range(10, 42, 2),
                                                       range(6, 38, 2), range(6, 34, 2)):
        if height > width-4:
            continue
        cross = original((12, height, 4), (True, True, False), (1, height+2))
        next_source = original((next_width, 4, 4), offset=(4, 4))
        if (4, height+1) not in next_source['endpoints']:
            assert next_width <= height-4 <= width-8
            assert not next_source['endpoints'] & cross['endpoints']
        else:
            assert (4, height+1) in cross['endpoints']
        consecutive_pairs += 1
    for height, incident in itertools.product(range(6, 34, 2), range(4, 30, 2)):
        cross = original((6, height, 4), (False, True, False), (height, -1))
        single = original((6, incident, 4), (False, True, True), (incident+3, 3))
        if (height-1, 2) not in single['endpoints']:
            assert incident <= height-6
        else:
            assert (height-1, 2) in cross['endpoints']
        witness = (incident+2, 0) if incident+2 <= height else (height-1, 2)
        assert witness in single['endpoints'] & cross['endpoints']
        pair_singletons += 1
        second_companion = original((6, incident, 4), (False, True, True), (incident+5, 5))
        witness = (incident+4, 0) if incident+4 <= height else (height-1, 4)
        assert witness in second_companion['endpoints'] & cross['endpoints']
        shifted_companions += 1
    for height, incident in itertools.product(range(8, 34, 2), range(4, 30, 2)):
        if incident > height-4:
            continue
        cross = original((12, height, 4), (True, True, False), (1, height+2))
        companion = original((8, incident, 4), (True, True, False), (2, incident+3))
        assert companion['charge'] == 1
        assert not cross['endpoints'] & companion['endpoints']
        assert not ROTOR_POINTS & (cross['endpoints'] | companion['endpoints'])
        assert {(2, 3), (3, 2)} <= companion['selected']
        assert (2, 3) in cross['endpoints'] and (3, 2) in ROTOR_POINTS
        rotor_companions += 1
    return dict(consecutive_pair_width_controls=consecutive_pairs,
                pair_singleton_exclusion_controls=pair_singletons,
                small_companion_pair_rotor_exclusion_controls=shifted_companions,
                rotor_companion_activation_controls=rotor_companions,
                scope='Coordinate interval/collision checks and original companion profiles; '
                      'partial patterns are not asserted to have complete feasible extensions.')


def graph_controls():
    checked = 0
    for amount in range(5):
        vertices = set(range(amount))
        for targets in itertools.product(range(-1, amount), repeat=amount):
            image = [target for target in targets if target >= 0]
            if len(image) != len(set(image)):
                continue
            edges = {source: (target, 'P') for source, target in enumerate(targets) if target >= 0}
            roots = sorted(vertices-set(image))
            sinks = sorted(vertices-edges.keys())
            for root_bits in range(1 << len(roots)):
                activated = set(image) | {root for index, root in enumerate(roots)
                                          if root_bits >> index & 1}
                for sink_bits in range(1 << len(sinks)):
                    marked = set(edges) | {sink for index, sink in enumerate(sinks)
                                           if sink_bits >> index & 1}
                    trace_paths(vertices, edges, marked, activated)
                    checked += 1
    return dict(partial_injection_labelled_graphs=checked, maximum_vertices=4,
                scope='Exact finite graph/unit-label controls, including cycles and isolated '
                      'bad negative endings; no geometric realizability or full allocation inference.')


def main():
    counts = Counter({key: 0 for key in ['S', 'P', 'R', 'consecutive_PP',
                     'consecutive_PS', 'consecutive_PR', 'negative_U_sinks']})
    restrictions = images = 0
    for _, original_modules in fixtures()+protected_fixtures()+[('connected_hull24', modules_at(24))]:
        clauses, _ = implications(original_modules)
        retained = retained_families(original_modules, clauses)
        for symmetry in SYMMETRIES:
            for phase in itertools.product((0, 1), repeat=2):
                modules = [transform_module(module, symmetry, phase) for module in original_modules]
                for owners in retained:
                    counts.update(physical_case(modules, owners))
                    restrictions += 1
                images += 1
    print(json.dumps(dict(status='PASS', rotor_roles=rotor_role_controls(),
                         intervals=interval_controls(), abstract_paths=graph_controls(),
                         physical=dict(images=images, legal_restrictions=restrictions, **counts),
                         scope='General proofs are written separately. Existing complete fixtures '
                               'can have zero rotor/S/PP/PS/PR channels; their counts remain explicit. '
                               'No bounded census proves unrestricted allocation or grid equality.'), indent=2))


if __name__ == '__main__':
    main()
