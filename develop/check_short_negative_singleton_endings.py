"""Original-role controls for length-four and length-six negative singleton exits."""

from collections import Counter
import itertools
import json

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_five_endpoint_cap import SYMMETRIES
from check_demand_hull_reserve_obstruction import report
from check_pair_transfer_protected_defects import original, rectangle_points
from check_persistent_corridor_capacity import certificates
from check_source_retention_closure import hull, implications
from rotor_networks import affine, rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


WITNESS = [
    ((12, 4, 4), (False, False, False), (0, 0)),
    ((6, 6, 4), (False, True, False), (9, 1)),
    ((14, 8, 4), (True, True, False), (1, 10)),
    ((6, 4, 4), (False, False, False), (3, 2)),
    ((6, 4, 4), (False, False, False), (5, -5)),
    ((6, 4, 8), (False, False, False), (-4, -6)),
    ((6, 6, 6), (True, False, False), (15, 6)),
    ((8, 4, 8), (True, True, True), (5, 17)),
    ((10, 4, 4), (False, True, False), (6, 10)),
    ((10, 4, 6), (False, True, False), (14, -2)),
    ((10, 6, 6), (False, True, False), (21, -5)),
]


def same(first, second):
    return all(first[field] == second[field] for field in ('endpoints', 'selected'))


def fixed(width, incident, far, cross_width, height, cross_far):
    return [original((height+4, 4, 4)),
            original((width, incident, far), (False, True, False), (incident+3, 1)),
            original((cross_width, height, cross_far), (True, True, False), (1, height+2))]


def shortest_enclosure_controls():
    count = 0
    for width, far, cross_width, height, cross_far in itertools.product(
            (6, 8, 14), (4, 6, 10), (6, 10, 14), (8, 12, 18), (4, 6)):
        base, terminal, cross = fixed(width, 4, far, cross_width, height, cross_far)
        if terminal['endpoints'] & cross['endpoints']:
            continue
        assert height >= width+2
        inside, boundary = rectangle_points((2, 6, 2, width+1))
        assert boundary <= terminal['endpoints'] | cross['endpoints']
        assert not inside & (terminal['endpoints'] | cross['endpoints'])
        assert (3, 3) in inside and (3, 3) in cross['selected']
        assert {(2, 3), (3, 2)} <= terminal['endpoints'] | cross['endpoints']
        count += 1
    return count


def candidates():
    result = {}
    for dimensions in itertools.product((6, 8, 12, 18), (4, 6, 8, 12), (4, 6, 10)):
        for symmetry in SYMMETRIES:
            module = original(dimensions, symmetry)
            for chosen in module['endpoints']:
                own = set(neighbors(chosen)) & module['endpoints']
                allowed = {(chosen[0]+1, chosen[1]), (chosen[0], chosen[1]+1)}
                if not own or not own <= allowed:
                    continue
                moved = transform_module(module, (False, False, False),
                                         (3-chosen[0], 3-chosen[1]))
                key = frozenset(moved['endpoints']), frozenset(moved['selected'])
                result[key] = dimensions, moved
    return list(result.values())


def classify(dimensions, module):
    width, near, far = dimensions
    for incident, other in ((near, far), (far, near)):
        east = original((width, incident, other), (True, True, False), (2, incident+3))
        if same(module, east):
            return 'positive_east', width, incident, other
        south = original((width, incident, other), (False, True, False), (incident+3, 2))
        if same(module, south):
            assert incident == other == 4
            return 'positive_south', width, incident, other
        upper = original((width, incident, other), offset=(3, 2))
        if same(module, upper):
            assert incident == 4
            return 'negative_upper', width, incident, other
    raise AssertionError(('unclassified', dimensions, sorted(module['endpoints'])))


def role_controls():
    totals = Counter()
    prepared = candidates()
    for width, far, cross_width, height, cross_far in itertools.product(
            (6, 8, 12), (4, 6), (6, 10, 14), (6, 8, 12, 16), (4, 6)):
        modules = fixed(width, 6, far, cross_width, height, cross_far)
        endpoints = set().union(*(module['endpoints'] for module in modules))
        if len(endpoints) != sum(len(module['endpoints']) for module in modules):
            continue
        totals['disjoint_fixed_patterns'] += 1
        for dimensions, module in prepared:
            if module['endpoints'] & endpoints:
                continue
            kind, breadth, incident, other = classify(dimensions, module)
            if kind == 'positive_east':
                assert width <= incident <= height-4
                assert height+4 >= width+8 >= 14
            else:
                assert breadth <= height-2
            if kind.startswith('positive'):
                assert module['charge'] == 1
                assert {(2, 3), (3, 2)} <= module['selected'] & endpoints
            if kind == 'positive_south':
                assert breadth <= width-2
                inside, boundary = rectangle_points((2, 6, 3, breadth+2))
                assert boundary <= endpoints | module['endpoints']
                assert not inside & (endpoints | module['endpoints'])
                assert {(4, 4), (4, breadth+1)} <= inside & module['selected']
            if kind == 'negative_upper':
                last = min(breadth+2, width+1)
                inside, boundary = rectangle_points((4, 8, 3, last))
                assert boundary <= endpoints | module['endpoints']
                assert not inside & (endpoints | module['endpoints'])
                receipt = vertices_of({(2, 2)})
                assert len(receipt & module['endpoints']) == 2
                assert not receipt & module['selected']
                assert len(receipt & (endpoints | module['endpoints'])) == 2
                assert module['charge'] < 0
            totals[kind] += 1
    totals['anchored_U_role_candidates'] = len(prepared)
    rotor_candidates = {}
    for symmetry in SYMMETRIES:
        module = transform_module(rotor(), symmetry)
        for chosen in module['endpoints']:
            own = set(neighbors(chosen)) & module['endpoints']
            allowed = {(chosen[0]+1, chosen[1]), (chosen[0], chosen[1]+1)}
            if not own or not own <= allowed:
                continue
            moved = transform_module(module, (False, False, False),
                                     (3-chosen[0], 3-chosen[1]))
            rotor_candidates[frozenset(moved['endpoints'])] = moved
    assert len(rotor_candidates) == 4
    fixed_points = {(2, 4), (2, 5), (5, 2), (4, 2)}
    assert all(module['endpoints'] & fixed_points for module in rotor_candidates.values())
    totals['rotor_tip_roles_excluded'] = len(rotor_candidates)
    return totals


def collision_and_rounding_controls():
    tested = 0
    for producer_width, height, incident, breadth in itertools.product(
            (12, 14, 20, 32), (8, 10, 16, 24), (4, 6, 10, 18), (6, 8, 14)):
        if not incident+4 <= height <= producer_width-4:
            continue
        base = original((producer_width, 4, 4))
        other = original((breadth, 4, 4), (False, False, True), (0, incident+5))
        assert (0, incident+4) in base['endpoints'] & other['endpoints']
        assert max(column for _, column in other['endpoints']) < producer_width
        tested += 1
    rounding = 0
    for positives, transferred, caps, pairs, unmarked, residual in itertools.product(
            range(5), range(5), range(3), range(4), range(3), range(5)):
        marked = transferred+caps+pairs+residual
        if marked > 2*(positives-unmarked):
            continue
        for lower, upper, prior in itertools.product(range(pairs, pairs+2), range(caps, caps+2), range(3)):
            reserve = (transferred+prior+caps+2*lower+2*upper+1)//2
            margin = positives+reserve-marked
            assert margin >= unmarked+upper+(lower+prior-residual+1)//2
            if residual <= 2*unmarked+2*upper+lower+prior+1:
                assert margin >= 0
            rounding += 1
    return dict(pair_transfer_self_collision_controls=tested,
                exact_integer_allocation_controls=rounding)


def complete_witness_controls():
    base = [original(*specification) for specification in WITNESS]
    whole = frozenset(range(len(base)))
    exact = report(base, whole)
    assert (exact['endpoints'], exact['matching'], exact['selected'], exact['endpoint_components']) == (
        278, 139, 62, 1)
    assert (exact['positive'], exact['marked'], exact['event_reserve'], exact['exact_joint_margin']) == (
        3, 2, 26, 27)
    assert (exact['activated_positive'], exact['unused_u_triples'], exact['lone_irregular'],
            exact['sole_irregular_pair'], exact['mixed_three']) == (4, 2, 5, 19, 3)
    images = preserving = 0
    for symmetry in SYMMETRIES:
        for phase in itertools.product((0, 1), repeat=2):
            modules = [transform_module(module, symmetry, phase) for module in base]
            current = report(modules, whole)
            assert current['endpoint_components'] == 1
            clauses, _ = implications(modules)
            assert hull(clauses, {0, 1}) == whole
            images += 1
            if modules[0]['charge'] != 1 or modules[1]['charge'] != -1:
                continue
            move = lambda point: affine(point, symmetry, phase)
            pair = {move(point) for point in vertices_of({(2, 2)})}
            key = tuple(value//2 for value in next(iter(pair)))
            if pair != vertices_of({key}):
                continue
            _, _, lower, _ = certificates(modules)
            assert key in lower
            preserving += 1
    assert preserving == 8
    return dict(images=images, b6_negative_branch_images=preserving,
                exact_connected_report=exact, least_feasible_seed_hull=list(range(11)),
                source_count_minimality_claim=False,
                scope='Complete actual negative H branch, every original support and matching '
                      'retained. Connectedness and Horn closure checked independently; '
                      'positive margin27, not an allocation counterexample.')


def tight_return_obstruction():
    terminal = original((6, 6, 4), (False, True, False), (9, 1))
    cross = original((10, 8, 4), (True, True, False), (1, 10))
    upper = original((6, 4, 4), offset=(3, 2))
    endpoints = terminal['endpoints'] | cross['endpoints'] | upper['endpoints']
    assert len(endpoints) == sum(len(module['endpoints']) for module in (terminal, cross, upper))
    assert (8, 8) in upper['selected'] and (8, 8) not in endpoints
    assert {(7, 8), (8, 7), (8, 9), (11, 8)} <= endpoints
    first = transform_module(rotor(), (False, False, False), (7, 6))
    second = transform_module(rotor(), (False, False, True), (7, 10))
    assert (8, 8) in first['endpoints'] & second['endpoints']
    assert (10, 9) in first['endpoints'] & cross['endpoints']
    assert (9, 7) in second['endpoints'] & terminal['endpoints']
    return dict(prescribed_owners=3, forced_support=[8, 8],
                foreign_neighbors=[[7, 8], [8, 7], [8, 9]],
                forbidden_U_stem_point=[11, 8],
                forbidden_rotor_points=[[10, 9], [9, 7]],
                scope='The fixed stencil and two rotor roles are checked here; the '
                      'written minimum-leg argument excludes ALL U dimensions and '
                      'arbitrary complete U/rotor extensions, not just a finite library.')


def main():
    result = dict(status='PASS', shortest_disjoint_enclosures=shortest_enclosure_controls(),
                  length_six_role_controls=role_controls(),
                  algebra=collision_and_rounding_controls(),
                  complete_witness=complete_witness_controls(),
                  tight_return_obstruction=tight_return_obstruction(),
                  scope='Original matching/support reconstructions and endpoint-disjoint '
                        'PARTIAL role patterns, not complete realizations. The proof for '
                        'unbounded dimensions and arbitrary added U/rotor sources is written. '
                        'The separate eleven-source manifest realizes only the H channel; '
                        'no unrestricted allocation or grid theorem is claimed.')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
