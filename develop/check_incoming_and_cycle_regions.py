"""Coordinate, source-role and planar controls for the incoming/cycle proofs."""

from collections import Counter
import itertools
import json

from all_phase_joint_slots import tile_of
from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_critical_owner_profiles import anchored_images
from check_minus_one_tip_obstructions import source
from check_neutral_port_turning import port_data
from rotor_networks import combine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def incoming_controls():
    counts = Counter()
    parameters = itertools.product((6, 10, 18), (4, 8), (4, 6, 12),
                                   (6, 14), (4, 6, 10, 18), (4, 16))
    for positive_width, short, height, width, companion_height, far in parameters:
        if height < short:
            continue
        incoming = transform_module(source(width, height, far),
                                    (False, True, False), (height+2, positive_width-2))
        point, missing = (short+1, positive_width-1), (short+1, positive_width-2)
        assert point in incoming['endpoints'] and missing not in incoming['endpoints']
        assert phase_of(incoming) == '10'
        counts['incoming_present_missing_pairs'] += 1
        if companion_height < short+2:
            continue
        companion = transform_module(source(width, companion_height, far),
                                     (False, True, True), (companion_height, positive_width+2))
        witness = ((height+1, positive_width+1) if height+1 <= companion_height
                   else (companion_height, positive_width-1))
        assert witness in incoming['endpoints'] & companion['endpoints']
        assert phase_of(companion) == '11'
        counts['complete_B_companion_crossings'] += 1
        counts['B_cap_height_boundaries'] += int(companion_height == short+2)
        for symmetry in ((False, True, True), (True, True, True)):
            cap = transform_module(source(width, companion_height, far),
                                   symmetry, (short+2, positive_width+2))
            assert {point, missing} <= cap['endpoints']
            assert phase_of(cap) == '11'
            counts['cap_distinguishing_pairs'] += 1
    return dict(counts)


def role_controls():
    counts = Counter()
    blockers = {(row, -1) for row in range(-1, 4)} | {(-1, column) for column in range(5)}
    images = {frozenset(module['endpoints']) for _, module in anchored_images(rotor())}
    assert len(images) == 16 and all(image & blockers for image in images)
    counts['exhaustive_rotor_roles_blocked'] = len(images)
    for width, left, right in itertools.product((6, 8, 14), (4, 6, 12), (4, 8, 20)):
        permitted = {(0, 1), (0, width), (left, 1), (right, width)}
        for anchor, image in anchored_images(source(width, left, right)):
            if image['endpoints'] & {(-1, 0), (0, -1)}:
                continue
            assert anchor in permitted
            counts['two_perpendicular_blocker_U_roles'] += 1
    return dict(counts)


def inside(point, curve):
    if point in curve:
        return None
    row, column = point
    crossings = 0
    for first, second in zip(curve, curve[1:]+curve[:1]):
        if (first[0] > row) != (second[0] > row) and first[1] > column:
            assert first[1] == second[1]
            crossings += 1
    return crossings % 2 == 1


def partial_cycle_control():
    modules = [transform_module(source(14, 4, 4), (False, False, False), (0, 1)),
               transform_module(source(6, 4, 4), (True, True, False), (3, 7)),
               transform_module(source(14, 4, 4), (False, True, False), (13, 1)),
               transform_module(source(6, 4, 4), (True, False, False), (3, 10))]
    network = combine(modules)
    data = [port_data(module) for module in modules]
    ports = {port['point']: (owner, index) for owner, record in enumerate(data)
             for index, port in enumerate(record['ports'])}
    contacts = {}
    forced = []
    for point, key in ports.items():
        cells = vertices_of({tile_of(point)})
        assert len(cells & network['endpoints']) == 2
        other = next(iter((cells & network['endpoints'])-{point}))
        contacts[key] = ports[other]
        port = data[key[0]]['ports'][key[1]]
        if port['blank'] in network['endpoints']:
            target = tuple(point[index]+port['inward'][index]+port['exterior'][index]
                           for index in (0, 1))
            anchor = tuple(point[index]+port['inward'][index] for index in (0, 1))
            forced.append((target, anchor))
    owner, entry, curve = 0, 0, []
    while True:
        path = data[owner]['path']
        curve.extend(path if entry == 0 else list(reversed(path)))
        owner, entry = contacts[owner, 1-entry]
        if (owner, entry) == (0, 0):
            break
    assert len(set(curve)) == len(curve)
    assert len(forced) == 4 and len({point for point, _ in forced}) == 4
    assert all(inside(point, curve) and anchor in curve for point, anchor in forced)
    return dict(pure_cycle_sources=4, inward_forced_points=4,
                complete_feasible=False,
                scope='Endpoint-disjoint partial neutral loop only; its four mandatory '
                      'supports remain infeasible. Tests turning/inside adapters, not realizability.')


def rectangle(top, left, bottom, right):
    return ([(top, column) for column in range(left, right)]+
            [(row, right) for row in range(top, bottom)]+
            [(bottom, column) for column in range(right, left, -1)]+
            [(row, left) for row in range(bottom, top, -1)])


def region_controls():
    counts = Counter()
    curves = [rectangle(0, 0, 20, 20), rectangle(3, 3, 17, 17),
              rectangle(6, 6, 14, 14), rectangle(0, 24, 20, 44)]
    for first, second in itertools.permutations(curves, 2):
        assert not set(first) & set(second)
        for anchor in first:
            for step in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                point = tuple(anchor[index]+step[index] for index in (0, 1))
                if inside(point, first) is not True or inside(point, second) is None:
                    continue
                assert inside(point, second) == inside(anchor, second)
                counts['unit_edge_same_side_nested_or_disjoint_controls'] += 1
    for sizes in itertools.product(range(4, 32, 2), repeat=3):
        inward = [(size+4)//2 for size in sizes]
        required = [(size+11)//8 for size in sizes]
        assert all((size+4) % 2 == 0 for size in sizes)
        assert all(4*amount >= demand and 4*(amount-1) < demand
                   for amount, demand in zip(required, inward))
        assert sum(required) >= len(sizes)
        counts['conditional_additive_rounded_cycle_quotas'] += 1
    return dict(counts)


def main():
    print(json.dumps(dict(status='PASS', incoming=incoming_controls(),
                          original_roles=role_controls(), partial_cycle=partial_cycle_control(),
                          regions=region_controls(), complete_critical_U10_realizations=0,
                          complete_pure_U01_cycle_realizations=0,
                          scope='Finite physical/planar/conditional arithmetic controls. '
                                'General source/region proofs are written; scoped Lean '
                                'does not formalize plane separation or full source fusions.'), indent=2))


if __name__ == '__main__':
    main()
