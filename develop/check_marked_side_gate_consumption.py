"""Check canonical gate consumption in complete feasible source restrictions."""

import itertools
import json
import random

from check_connected_marked_hull_obstruction import modules_at
from check_cooperative_promotion import neighbors
from check_exact_event_reserve import fixtures
from check_source_retention_closure import feasible, hull, implications, marked_counts
from dual_guard_compensation import paired_guards
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def retained_families(modules, clauses):
    amount = len(modules)
    if amount <= 9:
        candidates = [frozenset(index for index in range(amount) if mask >> index & 1)
                      for mask in range(1 << amount)]
    else:
        generator = random.Random(20261021)
        seeds = [set(), set(range(amount))]
        seeds += [{index} for index in range(amount)]
        seeds += [set(pair) for pair in itertools.combinations(range(amount), 2)]
        seeds += [{index for index in range(amount) if generator.randrange(2)}
                  for _ in range(128)]
        candidates = sorted({hull(clauses, seed) for seed in seeds}, key=sorted)
    return [retained for retained in candidates if feasible(modules, retained)]


def inspect(modules, families, clauses):
    owners = {point: index for index, module in enumerate(modules)
              for point in module['endpoints']}
    assert len(owners) == sum(len(module['endpoints']) for module in modules)
    full = frozenset(range(len(modules)))
    full_marks = marked_counts(modules, full)
    gates = {owner: tuple(chosen for chosen, _, _, _ in paired_guards(modules[owner]))
             for owner in full_marks}
    seed = set(full_marks)
    for owner, marks in full_marks.items():
        for gate, marked in zip(gates[owner], marks):
            assert (gate in owners) == marked
            if marked:
                seed.add(owners[gate])
    canonical = hull(clauses, seed)
    assert feasible(modules, canonical)
    assert marked_counts(modules, canonical) == full_marks
    cache = {}
    side_checks = 0
    demand_preserving = 0
    for retained in set(families) | {canonical, full}:
        endpoints = {point for owner in retained for point in modules[owner]['endpoints']}
        marks = marked_counts(modules, retained)
        assert marks == {owner: tuple(gate in endpoints for gate in gates[owner])
                         for owner in retained if owner in gates}
        assert marks == {owner: tuple(owners.get(gate) in retained for gate in gates[owner])
                         for owner in retained if owner in gates}
        side_checks += 2*len(marks)
        if marks == full_marks:
            assert canonical <= retained
            demand_preserving += 1
        cache[retained] = marks
    if len(families) <= 40:
        pairs = list(itertools.combinations_with_replacement(families, 2))
    else:
        generator = random.Random(20261021)
        pairs = [(generator.choice(families), generator.choice(families)) for _ in range(256)]
    for left, right in pairs:
        core = left & right
        joined = hull(clauses, left | right)
        assert feasible(modules, core) and feasible(modules, joined)
        core_marks = cache.get(core)
        if core_marks is None:
            core_marks = marked_counts(modules, core)
        for owner in set(cache[left]) & set(cache[right]):
            assert all(not (first and second) or shared for first, second, shared in
                       zip(cache[left][owner], cache[right][owner], core_marks[owner]))
        count = lambda marks: sum(sum(sides) for sides in marks.values())
        assert count(cache[left])+count(cache[right]) <= count(core_marks)+count(
            marked_counts(modules, joined))
    return dict(legal_restrictions=len(families), positive_side_checks=side_checks,
                legal_pairs=len(pairs), demand_preserving_controls=demand_preserving,
                canonical_hull_owners_1based=sorted(owner+1 for owner in canonical))


def main():
    records = []
    for name, original in fixtures()+[('connected_hull24', modules_at(24)),
                                      ('connected_hull70', modules_at(70))]:
        clauses, _ = implications(original)
        families = retained_families(original, clauses)
        images = []
        for symmetry in itertools.product((False, True), repeat=3):
            for phase in itertools.product((0, 1), repeat=2):
                moved = [transform_module(module, symmetry, phase) for module in original]
                images.append(inspect(moved, families, clauses))
        records.append(dict(fixture=name, owners=len(original), images=len(images),
                            exhaustive_restrictions=len(original) <= 9,
                            **{key: sum(row[key] for row in images) for key in
                               ('legal_restrictions', 'positive_side_checks', 'legal_pairs',
                                'demand_preserving_controls')}))
    print(json.dumps(dict(status='PASS', fixtures=records,
                         **{key: sum(row[key] for row in records) for key in
                            ('images', 'legal_restrictions', 'positive_side_checks', 'legal_pairs',
                             'demand_preserving_controls')},
                         scope='Actual degree-four protector marks versus canonical original '
                         'support consumption and unique endpoint consumer retention. Legal '
                         'restrictions exhaustive through nine owners, deterministic Horn-hull '
                         'samples above nine. All 32 phase/isometry images. Arbitrary legal '
                         'pairs exhaustive through 40 legal restrictions, deterministic 256-pair '
                         'samples beyond. Checks canonical least-demand hull inclusion, zero '
                         'duplicate-new-core marks and G supermodularity on legal joins. '
                         'Finite controls supplement the local general proof; unrestricted '
                         'allocation and rectangular-grid equality remain open.'), indent=2))


if __name__ == '__main__':
    main()
