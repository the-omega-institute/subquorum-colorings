"""Independent role controls for arbitrary-length negative singleton companions."""

from collections import Counter
import itertools
import json

from check_cooperative_promotion import neighbors
from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import original, rectangle_points
from check_short_negative_singleton_endings import candidates, fixed, same
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def companion_role(dimensions, module):
    width, near, far = dimensions
    for incident, other in ((near, far), (far, near)):
        specifications = [
            ('E', (True, True, False), (2, incident+3)),
            ('S', (False, True, False), (incident+3, 2)),
            ('H', (False, False, False), (3, 2)),
            ('V', (True, False, False), (2, 3)),
        ]
        for kind, symmetry, offset in specifications:
            if same(module, original((width, incident, other), symmetry, offset)):
                return kind, width, incident, other
    raise AssertionError(('unclassified', dimensions, sorted(module['endpoints'])))


def general_role_controls():
    counts = Counter()
    examples = {}
    library = candidates()
    for width, incident, cross_width, height in itertools.product(
            (6, 8, 12), (6, 8, 10, 14), (6, 10, 14), (6, 10, 14, 20)):
        modules = fixed(width, incident, 4, cross_width, height, 4)
        endpoints = set().union(*(module['endpoints'] for module in modules))
        if len(endpoints) != sum(len(module['endpoints']) for module in modules):
            continue
        counts['fixed_patterns'] += 1
        for dimensions, module in library:
            if module['endpoints'] & endpoints:
                continue
            kind, breadth, leg, other = companion_role(dimensions, module)
            if kind == 'E':
                assert leg <= height-4
                assert breadth <= incident-2 or leg >= width
            elif kind == 'S':
                assert leg <= incident-2
                assert breadth <= height-2 or leg >= cross_width
                if breadth <= height-2:
                    assert other <= leg
                if leg == 4:
                    assert other == 4 and breadth <= height-2
                    inside, boundary = rectangle_points((2, 6, 3, breadth+2))
                    assert boundary <= endpoints | module['endpoints']
                    assert not inside & (endpoints | module['endpoints'])
                    assert {(4, 4), (4, breadth+1)} <= inside & module['selected']
                    forced = (3, breadth+1)
                    assert forced in inside & modules[2]['selected']
                    assert {(2, breadth+1), (3, breadth+2)} <= endpoints | module['endpoints']
                    assert forced not in endpoints | module['endpoints']
                    counts['S4_no_extension_stencils'] += 1
            elif kind == 'H':
                assert leg <= incident-2 and breadth <= height-2
            else:
                assert breadth <= incident-2 and leg <= height-4
            if kind in ('E', 'S'):
                assert module['charge'] == 1
                assert {(2, 3), (3, 2)} <= module['selected'] & endpoints
                assert (3, 3) in module['endpoints']
                counts['positive_long' if incident >= 8 else 'positive_short'] += 1
            else:
                assert module['charge'] < 0
            counts[kind] += 1
            if kind not in examples or (incident >= 8 and examples[kind]['incident'] == 6):
                examples[kind] = dict(singleton_width=width, incident=incident,
                                      cross_width=cross_width, height=height,
                                      companion=(breadth, leg, other))
            if kind == 'E' and leg < width:
                counts['E_smaller_than_singleton_width'] += 1
                examples.setdefault('E_short_bar_exception', dict(
                    singleton_width=width, incident=incident,
                    cross_width=cross_width, height=height,
                    companion=(breadth, leg, other)))
    counts['anchored_U_candidates'] = len(library)
    assert all(counts[kind] > 0 for kind in ('E', 'S', 'H', 'V'))
    assert counts['E_smaller_than_singleton_width'] > 0
    return dict(counts=counts, partial_examples=examples)


def rotor_exclusion_controls():
    footprints = {}
    for symmetry in SYMMETRIES:
        module = transform_module(rotor(), symmetry)
        for point in module['endpoints']:
            own = set(neighbors(point)) & module['endpoints']
            if not own or not own <= {(point[0]+1, point[1]), (point[0], point[1]+1)}:
                continue
            moved = transform_module(module, (False, False, False), (3-point[0], 3-point[1]))
            footprints[frozenset(moved['endpoints'])] = moved
    blockers = {(2, 4), (2, 5), (4, 2), (5, 2)}
    assert len(footprints) == 4
    assert all(blockers & footprint for footprint in footprints)
    return len(footprints)


def injection_collision_controls():
    counts = Counter()
    for leg, breadth in itertools.product((4, 6, 10, 18), (6, 8, 14, 24)):
        old_width = max(leg+4, breadth)
        old_south_pair = original((old_width, 4, 4), (True, False, True), (leg+5, 0))
        assert (3, 1) in old_south_pair['endpoints']
        assert any(column == 0 for _, column in old_south_pair['endpoints'])
        base = original((max(12, leg+8), 4, 4))
        assert (3, 1) in base['endpoints']
        assert not any(column == 0 for _, column in base['endpoints'])
        counts['S_P_actual_endpoint_and_self_owner_exclusion'] += 1
    for width in (6, 8, 14, 24):
        base = original((width, 4, 4))
        for symmetry, offset, local_point in [
                ((True, False, True), (5, 0), (1, 5)),
                ((False, False, True), (0, 5), (0, 4))]:
            hypothetical = original((6, 4, 4), symmetry, offset)
            assert (0, 1) in hypothetical['endpoints'] & base['endpoints']
            assert any(column == 0 for _, column in hypothetical['endpoints'])
            counts['E_S_and_S_S_collisions'] += 1
    for height, leg in itertools.product((8, 12, 20, 28), (4, 6, 10, 18)):
        if leg+4 > height:
            continue
        producer_width = height+4
        base = original((producer_width, 4, 4))
        hypothetical = original((6, 4, 4), (False, False, True), (0, leg+5))
        assert (0, leg+4) in base['endpoints'] & hypothetical['endpoints']
        assert max(column for _, column in hypothetical['endpoints']) < producer_width
        counts['E_P_and_self_owner_exclusion'] += 1
    return counts


def narrow_south_obstruction_controls():
    tested = 0
    for cross_width, leg, breadth, other in itertools.product(
            (6, 8, 12, 18), (6, 8, 12, 20), (6, 8, 12, 18), (4, 6, 10)):
        if leg < cross_width:
            continue
        cross = original((cross_width, 6, 4), (True, True, False), (1, 8))
        south = original((breadth, leg, other), (False, True, False), (leg+3, 2))
        if cross['endpoints'] & south['endpoints']:
            continue
        endpoints = cross['endpoints'] | south['endpoints']
        inside, boundary = rectangle_points((2, cross_width+1, 3, 7))
        assert boundary <= endpoints
        assert not inside & endpoints
        assert len({column for _, column in inside}) == 3
        forced = (cross_width, 4)
        assert forced in inside & south['selected']
        assert {(cross_width, 3), (cross_width+1, 4)} <= endpoints
        tested += 1
    assert tested > 0
    return tested


if __name__ == '__main__':
    print(json.dumps(dict(
        status='PASS', roles=general_role_controls(),
        excluded_rotor_footprints=rotor_exclusion_controls(),
        injection_collisions=injection_collision_controls(),
        narrow_south_obstructions=narrow_south_obstruction_controls(),
        scope='Endpoint-disjoint PARTIAL role controls at independent dimensions; '
              'not complete realizations or a universal allocation proof. '
              'All-length role exhaustion and joint injection are written proofs.'), indent=2))
