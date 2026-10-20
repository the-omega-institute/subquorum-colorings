"""Check a three-column long-H enclosure and complete unbounded family controls."""

import itertools
import json

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import report
from check_five_endpoint_cap import SYMMETRIES
from check_pair_transfer_protected_defects import original, rectangle_points
from check_periodic_slab_compression import defects
from check_persistent_corridor_capacity import certificates
from check_short_negative_singleton_endings import WITNESS
from check_source_retention_closure import feasible
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def specifications(stretch):
    assert stretch >= 0 and stretch % 2 == 0
    return [
        ((12, 4, 4), (False, False, False), (0, 0)),
        ((6, 6+stretch, 4+stretch), (False, True, False), (9+stretch, 1)),
        ((14+stretch, 8, 4), (True, True, False), (1, 10)),
        ((6, 4+stretch, 4+stretch), (False, False, False), (3, 2)),
        ((6, 4+stretch, 4+stretch), (False, False, False), (5, -5)),
        ((6, 4, 8), (False, False, False), (-4, -6)),
        ((6, 6, 6), (True, False, False), (15+stretch, 6)),
        ((8, 4, 8), (True, True, True), (5, 17)),
        ((10, 4, 4), (False, True, False), (6, 10)),
        ((10, 4, 6), (False, True, False), (14+stretch, -2)),
        ((10, 6, 6), (False, True, False), (21+stretch, -5)),
    ]


def enclosure_controls():
    checked = 0
    for incident, far, width, other in itertools.product(
            (6, 8, 12, 20, 38), (4, 6, 10, 18, 36, 42),
            (6, 8, 12, 22), (4, 6, 12, 28)):
        if far < incident-2:
            continue
        returning = original((6, incident, far), (False, True, False), (incident+3, 1))
        corner = original((width, incident-2, other), offset=(3, 2))
        endpoints = returning['endpoints'] | corner['endpoints']
        if len(endpoints) != len(returning['endpoints'])+len(corner['endpoints']):
            continue
        inside, boundary = rectangle_points((4, incident+2, 3, 7))
        assert boundary <= endpoints
        assert not inside & endpoints
        assert {column for _, column in inside} == {4, 5, 6}
        tile = vertices_of({(2, 2)})
        assert tile & endpoints == {(4, 4), (4, 5)}
        assert not tile & corner['selected']
        assert {(5, 4), (5, 5)} <= inside
        checked += 1
    assert checked > 0
    return checked


def family_controls():
    assert specifications(0) == WITNESS
    base = [original(*specification) for specification in specifications(0)]
    base_network = combine(base)
    base_values, base_boundary, _ = defects(base)
    slab_columns = {-4, 1, 2, 3, 7, 8, 9, 10}
    examples = []
    images = 0
    for stretch in (0, 2, 4, 6, 10, 18, 32, 60):
        modules = [original(*specification) for specification in specifications(stretch)]
        network = combine(modules)
        shift = lambda point: (point[0]+stretch*(point[0] >= 7), point[1])
        slab_endpoints = {(row, column) for row in range(7, 7+stretch)
                          for column in slab_columns}
        slab_selected = {(row, column) for row in range(7, 7+stretch)
                         for column in ({-5} if row % 2 else {-3, 0, 4, 6})}
        assert network['endpoints'] == {shift(point) for point in base_network['endpoints']} | slab_endpoints
        assert network['selected'] == {shift(point) for point in base_network['selected']} | slab_selected
        whole = frozenset(range(len(modules)))
        assert feasible(modules, whole)
        _, _, lower, _ = certificates(modules)
        assert (2, 2) in lower
        exact = report(modules, whole)
        assert exact['endpoint_components'] == 1
        assert (exact['endpoints'], exact['matching'], exact['selected']) == (
            278+8*stretch, 139+4*stretch, 62+5*stretch//2)
        assert (exact['positive'], exact['marked'], exact['activated_positive']) == (3, 2, 4)
        assert (exact['event_reserve'], exact['exact_joint_margin']) == (26+stretch//2, 27+stretch//2)
        for symmetry in SYMMETRIES:
            for phase in itertools.product((0, 1), repeat=2):
                moved = [transform_module(module, symmetry, phase) for module in modules]
                assert feasible(moved, whole)
                endpoints = set().union(*(module['endpoints'] for module in moved))
                occupied = endpoints | set().union(*(module['selected'] for module in moved))
                move = lambda point: affine(point, symmetry, phase)
                cells = {move(point) for point in vertices_of({(2, 2)})}
                assert {move((4, 4)), move((4, 5))} == cells & endpoints
                assert not {move((5, 4)), move((5, 5))} & occupied
                assert all(len(set(neighbors(point)) & occupied) == 1 for point in occupied-endpoints)
                images += 1
        values, boundary, reserve = defects(modules)
        expected_boundary = {(row+stretch//2*(row >= 4), column): weight
                             for (row, column), weight in base_boundary.items()}
        fresh_boundary = {(row//2, 5): 2 for row in range(8, 8+stretch, 2)}
        assert not expected_boundary.keys() & fresh_boundary.keys()
        assert boundary == expected_boundary | fresh_boundary
        assert values == base_values
        assert boundary[(2, 2)] == 2
        examples.append(dict(stretch=stretch, singleton_leg=6+stretch,
                             corner_leg=4+stretch, endpoints=len(network['endpoints']),
                             selected=len(network['selected']), reserve=reserve,
                             allocation_margin=exact['exact_joint_margin'],
                             activated=values[0]))
    return dict(complete_family_images=images, examples=examples)


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', enclosure_patterns=enclosure_controls(),
                         complete_family=family_controls(),
                         scope='Endpoint/support/matching reconstructions of complete eleven-source '
                               'families and a three-column certificate. The unbounded enclosure, '
                               'receipt injection and family insertion proof are written; these '
                               'finite controls do not establish unrestricted allocation.'), indent=2))
