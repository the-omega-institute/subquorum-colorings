"""Check legal shared-core gluing with actual event, tile and mark overlap."""

import itertools
import json
import random

from check_closed_extension_reserve import signature
from check_connected_marked_hull_obstruction import modules_at
from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import report
from check_exact_event_reserve import fixtures
from check_source_retention_closure import feasible, hull, implications, marked_counts
from rotor_networks import transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def contact_graph(modules):
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    assert len(owners) == sum(len(module['endpoints']) for module in modules)
    graph = {index: set() for index in range(len(modules))}
    for point, owner in owners.items():
        for neighbor in neighbors(point):
            other = owners.get(neighbor)
            if other is not None and other != owner:
                graph[owner].add(other)
    return graph


def components(graph, retained):
    remaining = set(retained)
    parts = []
    while remaining:
        part = {min(remaining)}
        remaining -= part
        frontier = list(part)
        while frontier:
            fresh = graph[frontier.pop()] & remaining
            remaining -= fresh
            part |= fresh
            frontier.extend(fresh)
        parts.append(frozenset(part))
    return parts


def cuts(modules):
    amount = len(modules)
    whole = frozenset(range(amount))
    graph = contact_graph(modules)
    if amount <= 9:
        candidates = [frozenset(index for index in range(amount) if mask >> index & 1)
                      for mask in range(1 << amount)]
    else:
        clauses, _ = implications(modules)
        seeds = [{first, second} for first, second in itertools.combinations(range(amount), 2)]
        generator = random.Random(20261021)
        seeds += [{index for index in range(amount) if generator.randrange(2)} for _ in range(96)]
        candidates = sorted({hull(clauses, seed) for seed in seeds}, key=lambda core: tuple(sorted(core)))
    result = []
    for core in candidates:
        if len(core) < 2 or len(core) > amount-2:
            continue
        parts = components(graph, whole-core)
        if len(parts) < 2 or not feasible(modules, core):
            continue
        masks = range(1, 1 << (len(parts)-1)) if len(parts) <= 8 else [1 << index for index in range(len(parts)-1)]
        for mask in masks:
            first = frozenset().union(*(part for index, part in enumerate(parts) if mask >> index & 1))
            second = whole-core-first
            assert first and second
            result.append((core, core | first, core | second))
    return result


def inspect(modules, core, left, right, cache):
    whole = frozenset(range(len(modules)))
    assert left | right == whole and left & right == core
    for retained in (core, left, right, whole):
        if retained not in cache:
            assert feasible(modules, retained)
            cache[retained] = signature(modules, retained), marked_counts(modules, retained)
    current, first, second, shared = (cache[retained][0] for retained in (whole, left, right, core))
    assert first['events'] | second['events'] == current['events']
    assert first['events'] & second['events'] == shared['events']
    assert first['full'] | second['full'] == current['full']
    assert first['full'] & second['full'] == shared['full']
    assert current['reserve'] == first['reserve']+second['reserve']-shared['reserve']
    marks, left_marks, right_marks, core_marks = (cache[retained][1] for retained in (whole, left, right, core))
    duplicate = 0
    for owner, sides in marks.items():
        if owner in core:
            assert sides == tuple(first_side or second_side for first_side, second_side in
                                  zip(left_marks[owner], right_marks[owner]))
            duplicate += sum(first_side and second_side and not shared_side
                             for first_side, second_side, shared_side in
                             zip(left_marks[owner], right_marks[owner], core_marks[owner]))
        elif owner in left:
            assert sides == left_marks[owner]
        else:
            assert sides == right_marks[owner]
    margin = lambda retained: len(cache[retained][1])+cache[retained][0]['reserve']-sum(
        sum(sides) for sides in cache[retained][1].values())
    assert margin(whole) == margin(left)+margin(right)-margin(core)+duplicate
    assert duplicate == 0
    assert margin(whole) == margin(left)+margin(right)-margin(core)
    return dict(core_owners=len(core), core_events=len(shared['events']),
                core_mixed_full_tiles=len(shared['full']), core_reserve=shared['reserve'],
                core_negative_mass=shared['negative'], duplicate_new_common_sides=duplicate)


def main():
    records = []
    for name, original in fixtures()+[('connected_hull24', modules_at(24)), ('connected_hull70', modules_at(70))]:
        splits = cuts(original)
        if not splits:
            continue
        totals = []
        for symmetry in itertools.product((False, True), repeat=3):
            for phase in itertools.product((0, 1), repeat=2):
                moved = [transform_module(module, symmetry, phase) for module in original]
                cache = {}
                totals += [inspect(moved, core, left, right, cache) for core, left, right in splits]
        records.append(dict(fixture=name, owners=len(original), shared_core_cuts=len(splits),
                            phase_images=32, checks=len(totals),
                            cores_with_nonzero_events=sum(row['core_events'] > 0 for row in totals),
                            cores_with_mixed_full_tiles=sum(row['core_mixed_full_tiles'] > 0 for row in totals),
                            nontrivial_shared_reserve=sum(row['core_reserve'] != row['core_negative_mass'] for row in totals),
                            duplicate_new_common_sides=sum(row['duplicate_new_common_sides'] for row in totals)))
    modules = modules_at(24)
    core = frozenset({2, 5, 6, 7, 8})
    left, right = frozenset(range(9))-{4}, core | {4}
    witness = inspect(modules, core, left, right, {})
    witness.update(full=report(modules, frozenset(range(9))),
                   left=report(modules, left), right=report(modules, right),
                   core=report(modules, core), core_owners_1based=sorted(owner+1 for owner in core))
    assert witness['core']['endpoint_components'] == 1
    assert witness['core_reserve'] == 41 and witness['core_negative_mass'] == 43
    assert witness['full']['event_reserve'] == 24
    print(json.dumps(dict(status='PASS', fixtures=records, checks=sum(row['checks'] for row in records),
                         witness=witness,
                         scope='Complete feasible shared cores of at least two owners; actual '
                         'mandatory-support restrictions, event/full-tile union AND intersection, '
                         'actual marks and exact signed overlap valuation. All 32 phase/isometry '
                         'images per eligible fixture. Core subsets exhaustive through nine '
                         'owners; larger fixtures use pair/random seed hulls; branch partitions '
                         'exhaustive through eight components and singleton samples beyond. '
                         'Finite controls do not replace the general proof or establish full '
                         'allocation or grid equality.'), indent=2))


if __name__ == '__main__':
    main()
