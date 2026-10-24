"""Reconstruct complete sources and certify the exact cost of one source cut."""

from collections import Counter
import itertools
import json

from check_cap_continuation_budget import phase_of
from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_minus_one_tip_obstructions import source
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def inspect(length, width):
    assert length >= 4 and width >= 8 and length % 2 == width % 2 == 0
    specifications = [
        ((width, length+4, length+2), (False, False, False), (-length-2, -1)),
        ((6, width-2, 4), (True, True, False), (1, width-1)),
        ((length+8, width, 4), (True, True, True), (2, width+1)),
        ((width-2, length, length), (False, True, False), (0, 0)),
    ]
    modules = [transform_module(source(*parameters), symmetry, offset)
               for parameters, symmetry, offset in specifications]
    network = combine(modules)
    endpoints, selected = network['endpoints'], network['selected']
    occupied = endpoints | selected
    assert len(endpoints) == sum(len(module['endpoints']) for module in modules)
    assert len(endpoints) == 2*len(network['matching']) == 6*length+6*width+28
    assert all(sum(abs(first[index]-second[index]) for index in (0, 1)) == 1
               for first, second in network['matching'])
    assert all(len(set(neighbors(point)) & occupied) == 1 for point in selected)
    assert all(len(set(neighbors(point)) & occupied) >= 3 for point in endpoints)
    assert [phase_of(module) for module in modules] == ['01', '01', '01', '10']
    assert all(module['charge'] < 0 for module in modules)
    assert len(selected) == (3*length+width)//2+11
    census = Counter()
    boundary = 0
    for tile in network['receiver']:
        cells = vertices_of({tile})
        profile = len(cells & endpoints), len(cells & selected)
        census[profile] += 1
        originals = [module for module in modules if cells & module['endpoints']]
        kinds = [(len(cells & module['endpoints']), len(cells & module['selected']))
                 for module in originals]
        if profile == (1, 1):
            assert kinds == [(1, 1)]
            boundary += 1
        if profile == (2, 0):
            assert len(originals) == 1 and originals[0] is modules[3]
            assert kinds == [(2, 0)]
            boundary += 2
    assert census == Counter({(4, 0): 3*length//2+width+7,
                              (2, 1): width//2+1, (2, 0): width//2-2, (1, 1): 2})
    assert boundary == width-2
    for module in modules:
        for tile in module['receiver']:
            cells = vertices_of({tile})
            assert (len(cells & module['endpoints']), len(cells & module['selected'])) != (1, 2)
            assert len(cells & module['endpoints']) != 3
    kept = modules[2:]
    persistent = set.union(*(module['endpoints'] for module in kept))
    support = set.union(*(module['selected'] for module in kept))
    visible = support-endpoints
    restored = support & (endpoints-persistent)
    assert support-persistent == visible | restored and not visible & restored
    assert all(not set(neighbors(point)) & restored for point in visible)
    forced = {point for point in restored if len(set(neighbors(point)) & persistent) >= 2}
    assert forced == {(-2*index, width-1) for index in range(length//2+1)}
    remaining = restored-forced
    edges = {tuple(sorted((point, other))) for point in remaining
             for other in set(neighbors(point)) & remaining}
    assert edges == {((0, 0), (1, 0))}
    omissions = forced | {(0, 0)}
    relaxed = (support-persistent)-omissions
    assert all(len(set(neighbors(point)) & (persistent | relaxed)) == 1 for point in relaxed)
    minimum_omissions = len(omissions)
    assert minimum_omissions == length//2+2
    degree_excess = sum(len(set(neighbors(point)) & persistent)-1+
                        len(set(neighbors(point)) & restored) for point in restored)
    assert degree_excess == length//2+4
    slack = (length+18)*(width+4)//2-len(network['matching'])-len(selected)
    assert slack == (length*(width-5)+11*width+22)//2 > 0
    return dict(length=length, width=width, endpoints=len(endpoints),
                matching=len(network['matching']), selected=len(selected),
                positive_sources=0, marked_positive_sides=0,
                activation=0, unused_u=0, rotor=0, boundary=boundary,
                reserve=boundary//2, allocation_margin=boundary//2,
                restored_supports=len(restored), mandatory_omissions=minimum_omissions,
                degree_excess=degree_excess, ambient_slack=slack,
                refutes_unit_pool_payment=minimum_omissions > boundary)


def main():
    witness = inspect(10, 8)
    assert witness['mandatory_omissions'] == 7 and witness['boundary'] == 6
    controls = [inspect(length, width) for length, width in
                itertools.product((4, 6, 8, 10, 20, 40), (8, 10, 14, 20))]
    print(json.dumps(dict(status='PASS', witness=witness,
                         complete_family_controls=len(controls), controls=controls,
                         scope='Complete original-source reconstructions, unchanged matching, '
                         'all mandatory supports and full occupied-degree checks. Exact minimum '
                         'omission certificate: forced multiple-anchor omissions plus one '
                         'independent selected-selected edge, with an attaining relaxed cut. '
                         'Finite parameter checks do not prove the whole parametric family. '
                         'The concrete witness refutes unrestricted source-cut payment, '
                         'not full allocation or rectangular-grid equality.'), indent=2))


if __name__ == '__main__':
    main()
