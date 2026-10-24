"""Exact source-level implications and least feasible complete-source hulls."""

from collections import defaultdict
import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_exact_event_reserve import fixtures
from check_exact_event_reserve import inspect_exact
from check_component_receivers import endpoint_components
from check_minus_one_joint_compensation import contained, marked_gate_modules
from check_minus_one_tip_obstructions import source
from dual_guard_compensation import paired_guards
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def feasible(modules, retained):
    if not retained:
        return True
    endpoints = set.union(*(modules[index]['endpoints'] for index in retained))
    occupied = set.union(*(modules[index]['endpoints'] | modules[index]['selected']
                           for index in retained))
    return all(len(set(neighbors(point)) & occupied) == 1 for point in occupied-endpoints)


def implications(modules):
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    assert len(owners) == sum(len(module['endpoints']) for module in modules)
    assert feasible(modules, set(range(len(modules))))
    occupied_by = defaultdict(set)
    for index, module in enumerate(modules):
        assert feasible(modules, {index})
        for point in module['endpoints'] | module['selected']:
            occupied_by[point].add(index)
    clauses = {}
    occurrences = 0
    for producer, module in enumerate(modules):
        for point in sorted(module['selected']):
            anchors = set(neighbors(point)) & module['endpoints']
            assert len(anchors) == 1
            anchor = next(iter(anchors))
            for neighbor in set(neighbors(point))-{anchor}:
                for other in occupied_by[neighbor]:
                    assert point in owners
                    consumer = owners[point]
                    if consumer in (producer, other):
                        continue
                    assert producer != other
                    key = (*sorted((producer, other)), consumer)
                    clauses.setdefault(key, dict(producer=producer, other=other,
                                                  point=point, neighbor=neighbor,
                                                  anchor=anchor, consumer=consumer))
                    occurrences += 1
    return clauses, occurrences


def hull(clauses, seed):
    retained = frozenset(seed)
    while True:
        extended = retained | {consumer for first, second, consumer in clauses
                               if first in retained and second in retained}
        if extended == retained:
            return retained
        retained = extended


def marked_counts(modules, retained):
    occupied = set.union(*(modules[index]['endpoints'] | modules[index]['selected']
                           for index in retained)) if retained else set()
    result = {}
    for index in retained:
        module = modules[index]
        if module['charge'] != 1:
            continue
        result[index] = tuple(any(len(set(neighbors(point)) & occupied) == 4
                                 for point in (set(neighbors(anchor)) & module['endpoints']) | {guard})
                              for _, anchor, _, guard in paired_guards(module))
    return result


def mark_seed(modules):
    network = combine(modules)
    occupied = network['endpoints'] | network['selected']
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    seed = {index for index, module in enumerate(modules) if module['charge'] == 1}
    for index in tuple(seed):
        module = modules[index]
        original = module['endpoints'] | module['selected']
        for _, anchor, _, guard in paired_guards(module):
            protectors = (set(neighbors(anchor)) & module['endpoints']) | {guard}
            affected = sorted(point for point in protectors if len(set(neighbors(point)) & occupied) == 4)
            if not affected:
                continue
            foreign = (set(neighbors(affected[0])) & occupied)-original
            assert len(foreign) == 1
            witness = next(iter(foreign))
            assert witness in owners
            seed.add(owners[witness])
    return seed


def inspect(name, modules):
    clauses, occurrences = implications(modules)
    amount = len(modules)
    full = frozenset(range(amount))
    if amount <= 7:
        masks = range(1 << amount)
    else:
        generator = random.Random(20261020)
        masks = sorted({0, (1 << amount)-1} | {1 << index for index in range(amount)} |
                       {generator.randrange(1 << amount) for _ in range(128)})
    closed_sets = []
    checked = []
    for mask in masks:
        seed = frozenset(index for index in range(amount) if mask >> index & 1)
        is_closed = all(first not in seed or second not in seed or consumer in seed
                        for first, second, consumer in clauses)
        assert feasible(modules, seed) == is_closed
        completion = hull(clauses, seed)
        assert seed <= completion <= full and feasible(modules, completion)
        assert hull(clauses, completion) == completion
        if is_closed:
            closed_sets.append(seed)
        checked.append((seed, completion))
    minimality_controls = 0
    if amount <= 7:
        for seed, completion in checked:
            supersets = [closed for closed in closed_sets if seed <= closed]
            assert frozenset.intersection(*supersets) == completion
            minimality_controls += 1
    seed = mark_seed(modules)
    completion = hull(clauses, seed)
    assert marked_counts(modules, completion) == marked_counts(modules, full)
    return dict(fixture=name, owners=amount, distinct_nontrivial_clauses=len(clauses),
                raw_conflict_occurrences=occurrences, checked_subfamilies=len(checked),
                exhaustive=amount <= 7, independent_minimality_controls=minimality_controls,
                positive_mark_seed=sorted(seed), positive_mark_hull=sorted(completion),
                full_marked_sides=sum(sum(sides) for sides in marked_counts(modules, full).values()))


def cut_modules(length, width):
    specifications = [
        ((width, length+4, length+2), (False, False, False), (-length-2, -1)),
        ((6, width-2, 4), (True, True, False), (1, width-1)),
        ((length+8, width, 4), (True, True, True), (2, width+1)),
        ((width-2, length, length), (False, True, False), (0, 0)),
    ]
    return [transform_module(source(*parameters), symmetry, offset)
            for parameters, symmetry, offset in specifications]


def marked_reserve_nonmonotonicity():
    base = cut_modules(10, 8)
    chamber = [transform_module(module, (False, False, False), (30, 30))
               for module in marked_gate_modules()]
    reports = []
    for modules in ([base[3]]+chamber, base+chamber):
        current, moved = contained(modules)
        report = inspect_exact(current, moved)
        report['endpoint_components'] = len(endpoint_components(current))
        reports.append(report)
    assert [(row['positive'], row['marked'], row['event_reserve']) for row in reports] == [
        (1, 2, 11), (1, 2, 9)]
    assert all(row['endpoint_components'] == 2 for row in reports)
    return dict(smaller=reports[0], larger=reports[1],
                scope='Two endpoint components, nested complete feasible fusions, '
                      'all positives and actual marks preserved; not a connected '
                      'counterexample or a failure of allocation.')


def main():
    physical = [inspect(name, modules) for name, modules in fixtures()]
    band_controls = []
    common = None
    for length, width in itertools.product((4, 10, 40), (8, 10, 14)):
        modules = cut_modules(length, width)
        current, occurrences = implications(modules)
        if common is None:
            common = set(current)
        assert set(current) == common
        assert len(common) == 8
        assert all(hull(current, pair) == frozenset(range(4))
                   for pair in itertools.combinations(range(4), 2))
        band_controls.append(dict(length=length, width=width,
                                  raw_conflict_occurrences=occurrences,
                                  distinct_nontrivial_clauses=len(current),
                                  all_two_owner_hulls_are_full=True))
    print(json.dumps(dict(status='PASS', physical=physical, bands=band_controls,
                         marked_reserve_nonmonotonicity=marked_reserve_nonmonotonicity(),
                         checked_subfamilies=sum(row['checked_subfamilies'] for row in physical),
                         independent_minimality_controls=sum(row['independent_minimality_controls']
                                                             for row in physical),
                         scope='Complete existing source fixtures. Exact implication models '
                         'compared with direct mandatory-support feasibility. Exhaustive only '
                         'through seven owners; larger fixtures use deterministic samples. '
                         'Band controls are finite parameter checks. General intersection, '
                         'least-hull and mark preservation proofs are written separately. '
                         'No reserve monotonicity or full allocation claim.'), indent=2))


if __name__ == '__main__':
    main()
