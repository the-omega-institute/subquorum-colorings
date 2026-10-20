"""Reconstruct a connected positive-demand obstruction to least-hull reserve comparison."""

import itertools
import json

from check_closed_extension_reserve import signature
from check_component_receivers import endpoint_components, vertices_of
from check_cooperative_promotion import neighbors
from check_exact_event_reserve import inspect_exact
from check_minus_one_joint_compensation import contained
from check_minus_one_tip_obstructions import source
from check_source_retention_closure import feasible, hull, implications, mark_seed, marked_counts
from dual_guard_compensation import paired_guards
from rotor_networks import affine, combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def specifications(length, width):
    return [
        ((width, length+4, length+2), (False, False, False), (-length-2, -1)),
        ((6, width-2, 4), (True, True, False), (1, width-1)),
        ((length+8, width, 4), (True, True, True), (2, width+1)),
        ((width-2, length, length), (False, True, False), (0, 0)),
        ((6, 4, 4), (True, True, False), (-8, 15)),
        ((14, 4, 4), (True, False, True), (-1, 6)),
        ((8, 8, 6), (False, False, True), (12, width+5)),
        ((6, 6, 4), (True, False, False), (19, width-3)),
        ((12, 8, 4), (True, False, True), (20, width-5)),
        ((6, 4, 4), (False, True, True), (18, width+4)),
        ((8, 8, 6), (False, False, True), (-length-20, width+5)),
        ((6, 6, 4), (True, False, False), (-length-13, width-3)),
        ((12, 8, 4), (True, False, True), (-length-12, width-5)),
        ((6, 4, 4), (False, True, True), (-length-14, width+4)),
        ((8, 8, 6), (True, False, False), (-length-12, -8)),
        ((6, 6, 4), (False, True, False), (-length-4, -1)),
        ((12, 8, 4), (False, True, True), (-length-2, 0)),
        ((6, 4, 4), (True, True, False), (-length-11, -2)),
    ]


def independent_source(parameters, symmetry, offset):
    width, left, right = parameters
    matching = [((0, column), (0, column+1)) for column in range(1, width, 2)]
    matching += [((1, column), (1, column+1)) for column in range(2, width-1, 2)]
    matching += [((row, column), (row+1, column))
                 for column, height in ((1, left), (width, right)) for row in range(1, height, 2)]
    support = {(0, 0), (0, width+1), (left+1, 1), (right+1, width)}
    support |= {(row, 0 if row % 2 == 0 else 2) for row in range(2, left+1)}
    support |= {(row, width+1 if row % 2 == 0 else width-1) for row in range(2, right+1)}
    move = lambda point: affine(point, symmetry, offset)
    return ({move(point) for edge in matching for point in edge},
            {move(point) for point in support},
            {tuple(sorted((move(first), move(second)))) for first, second in matching})


def report(modules, retained):
    chosen = [modules[index] for index in sorted(retained)]
    network = combine(chosen)
    endpoints, selected = network['endpoints'], network['selected']
    occupied = endpoints | selected
    assert len(endpoints) == sum(len(module['endpoints']) for module in chosen)
    assert len(endpoints) == 2*len(network['matching'])
    assert all(len(set(neighbors(point)) & occupied) == 1 for point in selected)
    assert all(len(set(neighbors(point)) & occupied) >= 3 for point in endpoints)
    assert all(sum(abs(first[axis]-second[axis]) for axis in (0, 1)) == 1
               for first, second in network['matching'])
    current, moved = contained(chosen)
    exact = inspect_exact(current, moved)
    direct = signature(modules, retained)
    assert direct['reserve'] == exact['event_reserve']
    return dict(owners=[index+1 for index in sorted(retained)], endpoints=len(endpoints),
                matching=len(network['matching']), selected=len(selected),
                endpoint_components=len(endpoint_components(current)), shape=list(current[:2]),
                ambient_slack=current[0]*current[1]//2-len(network['matching'])-len(selected), **exact)


def witness_owners(modules):
    occupied = set.union(*(module['endpoints'] | module['selected'] for module in modules))
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    result = []
    for index, module in enumerate(modules):
        if module['charge'] != 1:
            continue
        original = module['endpoints'] | module['selected']
        for side, (_, anchor, _, guard) in enumerate(paired_guards(module)):
            choices = {owners[neighbor] for protector in (set(neighbors(anchor)) & module['endpoints']) | {guard}
                       for neighbor in (set(neighbors(protector)) & occupied)-original if neighbor in owners}
            if choices:
                result.append(dict(positive_owner=index+1, side=side, witness_owners=sorted(owner+1 for owner in choices)))
    return result


def inspect(length, width):
    assert length >= 18 and width >= 20 and length % 2 == width % 2 == 0
    manifest = specifications(length, width)
    modules = [transform_module(source(*parameters), symmetry, offset)
               for parameters, symmetry, offset in manifest]
    for module, specification in zip(modules, manifest):
        endpoints, support, matching = independent_source(*specification)
        assert endpoints == module['endpoints'] and support == module['selected']
        assert matching == {tuple(sorted(edge)) for edge in module['matching']}
    clauses, _ = implications(modules)
    assert clauses[4, 5, 3]['point'] == (-1, 11)
    assert clauses[4, 5, 3]['neighbor'] == (-1, 10)
    positives = {index for index, module in enumerate(modules) if module['charge'] == 1}
    assert positives == {4, 5, 6, 10, 14}
    choices = witness_owners(modules)
    assert len(choices) == 6
    assert all(row['witness_owners'] == [row['positive_owner']+3] for row in choices)
    seed = mark_seed(modules)
    closure = hull(clauses, seed)
    assert closure == frozenset(range(3, 18)) and feasible(modules, closure)
    full = report(modules, range(18))
    restricted = report(modules, closure)
    assert full['endpoint_components'] == 1 and restricted['endpoint_components'] == 4
    assert marked_counts(modules, closure) == marked_counts(modules, range(18))
    assert full['positive'] == restricted['positive'] == 5
    assert full['marked'] == restricted['marked'] == 6
    assert full['event_reserve'] == (width+80)//2
    assert restricted['event_reserve'] == width+38
    assert full['activated_positive'] == restricted['activated_positive'] == 5
    assert full['unused_u_triples'] == restricted['unused_u_triples'] == 15
    assert full['sole_irregular_pair'] == width//2+29
    assert restricted['sole_irregular_pair'] == width+27
    assert full['endpoints'] == 6*length+6*width+380
    assert full['selected'] == (3*length+width)//2+72
    assert restricted['endpoints'] == 2*length+2*width+346
    assert restricted['selected'] == 2*length+77
    return dict(length=length, width=width, full=full, least_marked_hull=restricted,
                n0=2, n1=0, n2=3, seed_owners=sorted(index+1 for index in seed),
                actual_mark_witness_owners=choices, all_witness_choices_same_owner_seed=True,
                reserve_drop=restricted['event_reserve']-full['event_reserve'],
                refutes_least_marked_hull_reserve_comparison=True,
                refutes_full_allocation=False)


def main():
    witness = inspect(20, 20)
    controls = [inspect(length, width) for length, width in
                itertools.product((18, 20, 40), (20, 24, 40, 100))]
    print(json.dumps(dict(status='PASS', witness=witness,
                         parameter_controls=[dict(length=row['length'], width=row['width'],
                                                  full_reserve=row['full']['event_reserve'],
                                                  hull_reserve=row['least_marked_hull']['event_reserve'],
                                                  reserve_drop=row['reserve_drop']) for row in controls],
                         scope='Explicit complete18source reconstruction, independent matching/support '
                         'formulas and exact geometric reserve, actual marks and unique witness-owner '
                         'seeds. Full endpoint graph connected, N5G6 with n2>n0; least marked hull '
                         'has four endpoint components. Refutes universal least-marked-hull reserve '
                         'comparison for connected ambient families, not a theorem additionally '
                         'requiring connected hull, not full allocation or grid equality. General '
                         'parameter theorem for this eighteen-source family is not claimed here; '
                         'finite controls do not prove one. The separate nine-source family has '
                         'a written all-parameter insertion proof.'), indent=2))


if __name__ == '__main__':
    main()
