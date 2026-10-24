"""Reconstruct a connected least-marked-hull reserve loss from complete sources."""

import json
from collections import Counter

from check_closed_extension_reserve import signature
from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source, report, witness_owners
from check_component_receivers import vertices_of
from check_minus_one_tip_obstructions import source
from check_source_retention_closure import feasible, hull, implications, mark_seed, marked_counts
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def specifications(length):
    return [
        ((8, length+4, length+2), (False, False, False), (-length-2, 0)),
        ((6, 6, 4), (True, True, False), (1, 8)),
        ((length+8, 8, 4), (True, True, True), (2, 10)),
        ((6, length, length), (False, True, False), (0, 1)),
        ((6, length+6, 4), (False, True, False), (0, 10)),
        ((8, 4, 4), (False, True, False), (-length-7, 3)),
        ((6, 4, 8), (True, False, False), (-length-12, -3)),
        ((6, 4, 6), (True, True, True), (-length-6, 3)),
        ((6, 4, 4), (True, True, True), (-length-11, 8)),
    ]


def modules_at(length):
    return [transform_module(source(*parameters), symmetry, offset)
            for parameters, symmetry, offset in specifications(length)]


def insertion_control(length, modules):
    larger = modules_at(length+2)
    shift = lambda point: (point[0]-2 if point[0] <= -6 else point[0], point[1])
    for index, (current, extended) in enumerate(zip(modules, larger)):
        endpoints = {shift(point) for point in current['endpoints']}
        support = {shift(point) for point in current['selected']}
        endpoint_columns = {0: {1, 8}, 2: {9, 10}, 3: {2, 7}, 4: {11}}.get(index, set())
        extra_endpoints = {(row, column) for row in (-7, -6) for column in endpoint_columns}
        odd_columns = {0: {2, 7}, 3: {3, 6}, 4: {12}}.get(index, set())
        even_columns = {0: {0, 9}, 3: {1, 8}, 4: {10}}.get(index, set())
        extra_support = {(-7, column) for column in odd_columns}
        extra_support |= {(-6, column) for column in even_columns}
        assert extended['endpoints'] == endpoints | extra_endpoints
        assert extended['selected'] == support | extra_support


def inspect(length):
    assert length >= 6 and length % 2 == 0
    modules = modules_at(length)
    for module, specification in zip(modules, specifications(length)):
        endpoints, support, matching = independent_source(*specification)
        assert endpoints == module['endpoints'] and support == module['selected']
        assert matching == {tuple(sorted(edge)) for edge in module['matching']}
    clauses, _ = implications(modules)
    seed = mark_seed(modules)
    retained, whole = frozenset(range(4)), frozenset(range(9))
    assert seed == {0, 3} and hull(clauses, seed) == retained
    assert hull(clauses, retained | {4}) == whole
    assert not feasible(modules, whole-retained)
    assert set(clauses) >= {(0, 3, 2), (0, 2, 1), (2, 4, 5), (2, 5, 6), (5, 6, 7), (5, 7, 8)}
    assert feasible(modules, retained) and feasible(modules, whole)
    assert marked_counts(modules, retained) == marked_counts(modules, whole) == {0: (True, True)}
    witnesses = witness_owners(modules)
    assert len(witnesses) == 2 and all(row['witness_owners'] == [4] for row in witnesses)
    smaller, larger = report(modules, retained), report(modules, whole)
    assert smaller['endpoint_components'] == larger['endpoint_components'] == 1
    assert smaller['event_reserve'] == length//2+13
    assert larger['event_reserve'] == 24
    assert smaller['exact_joint_margin'] == length//2+12 and larger['exact_joint_margin'] == 23
    assert larger['endpoints'] == 7*length+178 and larger['selected'] == 2*length+44
    assert larger['ambient_slack'] == 11*length//2+175
    assert larger['shape'] == [length+28, 22]
    assert (larger['activated_positive'], larger['unused_u_triples'],
            larger['unpaired_rotor_activation'], larger['lone_irregular'],
            larger['sole_irregular_pair'], larger['mutual_non_event'],
            larger['mixed_three'], larger['boundary_cost']) == (1, 5, 0, 5, 17, 0, 3, 42)
    first, second = signature(modules, retained), signature(modules, whole)
    fresh = second['events']-first['events']
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    old_new = {event for event in fresh if event[0] in retained and owners[event[2]] not in retained}
    new_old = {event for event in fresh if event[0] not in retained and owners[event[2]] in retained}
    new_new = fresh-old_new-new_old
    assert len(fresh) == len(old_new)+len(new_old)+len(new_new)
    assert {(owner, target) for owner, _, target in old_new} == {
        (2, (row, 11)) for row in range(-length-6, 1)}
    assert {(owner, target) for owner, _, target in new_old} == {
        (4, (row, 10)) for row in range(-length-5, 0, 2)}
    assert {(owner, target) for owner, _, target in new_new} == {
        (6, (-length-12, -2)), (6, (-length-12, 0)), (6, (-length-7, -1)),
        (7, (-length-11, -1)), (7, (-length-11, 1)), (7, (-length-11, -3))}
    assert (len(old_new), len(new_old), len(new_new)) == (length+7, length//2+3, 6)
    gained = second['full']-first['full']
    assert len(gained) == length//2+5
    assert second['negative']-first['negative'] == 17
    assert second['reserve']-first['reserve'] == 17+2*len(gained)-len(fresh) == 11-length//2
    separator_side = frozenset({2} | set(range(4, 9)))
    assert not any(set(neighbors(point)) & modules[other]['endpoints']
                   for owner in (0, 1, 3) for point in modules[owner]['endpoints']
                   for other in range(4, 9))
    branch = report(modules, separator_side)
    separator_mass = -modules[2]['charge']
    assert branch['endpoint_components'] == 1
    assert branch['positive'] == branch['marked'] == 0
    assert separator_mass == length+7 and branch['event_reserve'] == length//2+18
    assert second['reserve'] == first['reserve']+branch['event_reserve']-separator_mass
    smaller_network, larger_network = combine(modules[:4]), combine(modules)
    actual_profiles = Counter((len(vertices_of({tile}) & larger_network['endpoints']),
                               len(vertices_of({tile}) & larger_network['selected']))
                              for tile in larger_network['receiver'])
    assert actual_profiles == {(4, 0): length+20, (2, 1): 3*length//2+17,
                               (2, 0): 17, (3, 0): 8, (1, 1): 5, (1, 2): 1}
    assert smaller_network['selected'] & larger_network['endpoints'] == {
        (-length-7, 6), (-length-7, 8), (-length-7, 10), (-length-6, 5)}
    assert smaller_network['selected']-larger_network['endpoints'] <= larger_network['selected']
    assert all(len(set(neighbors(point)) & (larger_network['endpoints'] | larger_network['selected'])) == 1
               for point in larger_network['selected'])
    insertion_control(length, modules)
    return dict(length=length, full=larger, least_marked_hull=smaller,
                witness_owners=witnesses, source_seed=[1, 4], least_hull=[1, 2, 3, 4],
                extension_generated_by_one_added_owner=5, added_sources_alone_feasible=False,
                negative_separator_branch=dict(separator_owner=3, shared_negative_mass=separator_mass,
                    positive=0, marked=0, reserve=branch['event_reserve'], endpoint_components=1,
                    reserve_below_shared_mass=branch['event_reserve'] < separator_mass),
                signed_extension=dict(negative_mass=17, mixed_full_gain=len(gained),
                                      old_new=len(old_new), new_old=len(new_old), new_new=len(new_new),
                                      reserve_change=11-length//2), insertion_control='PASS')


def main():
    controls = [inspect(length) for length in (6, 8, 12, 24, 40, 70, 100)]
    print(json.dumps(dict(status='PASS', witness=controls[5],
                         parameter_controls=[dict(length=row['length'],
                             full_reserve=row['full']['event_reserve'],
                             hull_reserve=row['least_marked_hull']['event_reserve'],
                             **row['signed_extension']) for row in controls],
                         scope='Independent reconstruction of Oracle-proposed nine-source family. '
                         'Both endpoint graphs connected; exact actual marked hull, mandatory '
                         'supports, matching, degrees, tile/event reserves, signed loss and '
                         'two-row insertion checked. Finite controls do not replace the written '
                         'all-parameter proof. Refutes least-hull reserve comparison, including '
                         'connected hulls; full allocation and rectangular-grid equality OPEN. '
                         'No Lean claim for this nine-source family.'), indent=2))


if __name__ == '__main__':
    main()
