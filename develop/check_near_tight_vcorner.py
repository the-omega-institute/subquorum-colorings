"""Independent geometric controls for near-tight Vcorner double activation."""

from collections import Counter
import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import original
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def records(dimensions, symmetry, offset):
    endpoints, supports, matching = independent_source(dimensions, symmetry, offset)
    assert {point for edge in matching for point in edge} == endpoints
    assert len(endpoints) == 2*len(matching)
    return endpoints, supports


def shifted(points, offset):
    return {(row+offset[0], column+offset[1]) for row, column in points}


def rotor_controls():
    footprints = {}
    for symmetry in SYMMETRIES:
        module = transform_module(rotor(), symmetry)
        for point in module['endpoints']:
            own = set(neighbors(point)) & module['endpoints']
            allowed = {(point[0]+1, point[1]), (point[0], point[1]+1)}
            if not own <= allowed:
                continue
            moved = transform_module(module, (False, False, False), (-point[0], -point[1]))
            footprints[frozenset(moved['endpoints'])] = moved
    assert len(footprints) == 4
    south = [module for module in footprints.values() if (1, 0) in module['endpoints']]
    east = [module for module in footprints.values() if (0, 1) in module['endpoints']]
    assert len(south) == len(east) == 2
    assert all({(-1, 1), (-1, 2)} & module['endpoints'] for module in east)
    for first, second in itertools.product(south, repeat=2):
        assert first['endpoints'] & shifted(second['endpoints'], (0, 1))
    for module in south:
        assert module['endpoints'] & {(1, 1), (2, 1)}
        assert shifted(module['endpoints'], (0, 1)) & {(1, 0), (2, 0)}
    return dict(anchored_footprints=4, south_adjacent_tip_pairs=4,
                rotor_followed_by_terminal_collisions=2,
                terminal_followed_by_rotor_collisions=2)


def candidate_roles():
    candidates = []
    for dimensions in itertools.product((6, 8, 14, 24), (4, 6, 8, 12, 20), (4, 6, 10)):
        width, leg, far = dimensions
        forms = [('Sleft', (False, True, True), (leg, 1)),
                 ('Sright', (False, True, False), (leg, -1)),
                 ('Edown', (True, True, False), (-1, leg)),
                 ('Eup', (True, True, True), (1, leg)),
                 ('Hcorner', (False, False, False), (0, -1)),
                 ('Vcorner', (True, False, False), (-1, 0))]
        for name, symmetry, offset in forms:
            endpoints, supports = records(dimensions, symmetry, offset)
            assert (0, 0) in endpoints
            assert set(neighbors((0, 0))) & endpoints <= {(1, 0), (0, 1)}
            candidates.append((name, width, leg, far, endpoints, supports))
    return candidates


def boundary_controls():
    counts = Counter()
    candidates = candidate_roles()
    for height, width, far in itertools.product((10, 14, 20, 32), (6, 10, 14, 22), (4, 8)):
        cross, supports = records((width, height, far), (True, True, False), (1, height+2))
        for column in (height-2, height-1):
            for kind, breadth, leg, other, endpoints, _ in candidates:
                moved = shifted(endpoints, (3, column))
                counts['anchored_U_boundary_roles'] += 1
                if moved & cross:
                    continue
                assert kind == 'Sleft'
                assert leg <= width-4
                counts['surviving_left_south_terminal_roles'] += 1
        assert (3, height-1) in supports
        assert {(2, height-2), (2, height-1), (2, height), (3, height+1)} <= cross
        counts['forced_endcap_and_inner_support_stencils'] += 1
    return dict(counts)


def partial_chain_controls():
    counts = Counter()
    examples = []
    for height, width, cross_far, corner_width, corner_far in itertools.product(
            (18, 20, 24, 30), (14, 18, 24, 32), (4, 8), (6, 8), (4, 6)):
        column = height-2
        specifications = [((width, height, cross_far), (True, True, False), (1, height+2)),
                          ((corner_width, height-6, corner_far), (True, False, False), (2, 3))]
        for first_width, first_leg, middle_width, middle_leg, last_width, last_leg in (
                (6, 6, 8, 8, 10, 10), (6, 8, 8, 10, 10, 12),
                (6, 6, 6, 12, 6, 18), (8, 8, 10, 10, 12, 12)):
            current = specifications+[
                ((first_width, first_leg, 4), (False, True, True), (first_leg+3, column+1)),
                ((middle_width, middle_leg, 4), (False, True, True), (middle_leg+3, height)),
                ((last_width, last_leg, 4), (False, True, True), (last_leg+3, height+1))]
            modules = [records(*specification) for specification in current]
            endpoints = set().union(*(module[0] for module in modules))
            if len(endpoints) != sum(len(module[0]) for module in modules):
                continue
            cross, corner, first, middle, last = modules
            assert first_leg >= 6 and first_leg+2 <= middle_leg
            assert middle_leg+2 <= last_leg <= width-4
            assert width >= 14
            assert (3, column) in corner[1] & first[0]
            assert (3, height-1) in cross[1] & middle[0]
            assert (3, height) in middle[1] & last[0]
            assert {(2, column), (3, column+1)} <= first[1] & endpoints
            assert {(2, height), (3, height+1)} <= last[1] & cross[0]
            assert (2, column) in cross[0] and (3, column+1) not in cross[0]
            assert (3, column+1) in middle[0]
            assert width >= first_leg+8
            counts['disjoint_five_source_PARTIAL_chains'] += 1
            if len(examples) < 2:
                examples.append(current)
            for specification in current:
                module = original(*specification)
                endpoints_check, supports_check = records(*specification)
                assert module['endpoints'] == endpoints_check and module['selected'] == supports_check
            assert original(*current[2])['charge'] == original(*current[4])['charge'] == 1
            assert original(*current[3])['charge'] == -1
    assert counts['disjoint_five_source_PARTIAL_chains'] > 0
    return dict(counts=counts, examples=examples,
                scope='Endpoint-disjoint original C/X/Q1/D/Q2 chains only; no complete extension claimed.')


def prior_target_controls():
    counts = Counter()
    for height, leg, cross_width in itertools.product((10, 14, 22, 34), (6, 8, 14, 24),
                                                       (6, 14, 26)):
        column = height-2
        base = original((height+4, 4, 4))
        cross = original((cross_width, height, 4), (True, True, False), (1, height+2))
        specifications = [
            ('S', (6, 4, 4), (False, False, False), (0, column-2), (0, column-1)),
            ('P', (leg+4, 4, 4), (True, True, True), (leg+5, column+3), (2, height)),
            ('Ecomp', (6, 4, 4), (True, True, False), (0, column+3), (1, height)),
            ('Scomp', (6, 4, 4), (False, False, True), (0, column+3), (0, height))]
        for name, dimensions, symmetry, offset, point in specifications:
            producer = original(dimensions, symmetry, offset)
            fixed = cross if name == 'P' else base
            assert point in fixed['endpoints'] & producer['endpoints']
            assert producer['endpoints'] != fixed['endpoints']
            counts[name+'_collision_and_self_exclusion'] += 1
    return dict(counts)


def repeated_owner_control():
    height = 18
    incident = 8
    original_return = original((height-2, incident, incident),
                               (False, True, False), (incident+3, 1))
    relabelled_middle = original((height-2, incident, incident),
                                 (False, True, True), (incident+3, height))
    for field in ('endpoints', 'selected'):
        assert original_return[field] == relabelled_middle[field]
    assert set(map(frozenset, original_return['matching'])) == set(
        map(frozenset, relabelled_middle['matching']))
    specifications = [((18, height, 4), (True, True, False), (1, height+2)),
                      ((6, height-6, 4), (True, False, False), (2, 3)),
                      ((6, 6, 4), (False, True, True), (9, height-1)),
                      ((height-2, incident, incident), (False, True, False), (incident+3, 1)),
                      ((10, 14, 4), (False, True, True), (17, height+1))]
    modules = [records(*specification) for specification in specifications]
    assert len(set().union(*(module[0] for module in modules))) == sum(
        len(module[0]) for module in modules)
    return dict(middle_is_original_B=True, endpoints_supports_and_matching_identical=True,
                scope='Endpoint-disjoint PARTIAL C/X/Q1/B/Q2 control, not a complete witness.')


def integer_controls():
    checked = 0
    for difference, transferred in itertools.product(range(-40, 41), range(21)):
        old_floor = -((-difference)//2)
        new_floor = -((-(difference+2*transferred))//2)
        assert new_floor-old_floor == transferred
        for baseline in (0, 1, 4):
            assert (baseline+new_floor >= 0) == (difference+2*transferred >= -2*baseline-1)
        checked += 1
    return checked


def next_gap_control():
    specifications = [((18, 18, 8), (True, True, False), (1, 20)),
                      ((6, 10, 4), (True, False, False), (2, 3)),
                      ((6, 4, 4), (True, True, False), (2, 18))]
    modules = [records(*specification) for specification in specifications]
    assert len(set().union(*(module[0] for module in modules))) == sum(
        len(module[0]) for module in modules)
    assert (3, 14) in modules[1][1] & modules[2][0]
    assert set(neighbors((3, 14))) & modules[2][0] == {(3, 15)}
    assert original(*specifications[2])['charge'] == -5
    return dict(gap=8, east_terminal_role_survives_endpoint_constraints=True,
                specifications=specifications,
                scope='PARTIAL only; explains failure of the gap-six boundary-role proof to cover gap eight. '
                      'Not a complete-fusion counterexample to double activation or allocation.')


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', rotors=rotor_controls(),
                         boundary=boundary_controls(), chains=partial_chain_controls(),
                         prior_targets=prior_target_controls(), repeated_owner=repeated_owner_control(),
                         integer_controls=integer_controls(), next_gap=next_gap_control(),
                         scope='Finite discovery/verification supplements the general written proof. '
                               'Original-source role exhaustion, labelled reconstruction and global '
                               'joint injection are not replaced by these controls.'), indent=2))
