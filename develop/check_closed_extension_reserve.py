"""Actual directed-event transfers on legal closed source extensions."""

import itertools
import json
import random

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_exact_event_reserve import fixtures, inspect_exact
from check_minus_one_joint_compensation import contained, marked_gate_modules
from check_source_retention_closure import cut_modules, feasible, hull, implications, marked_counts
from rotor_networks import combine, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def signature(modules, retained):
    if not retained:
        return dict(negative=0, full=set(), events=set(), reserve=0)
    chosen = [modules[index] for index in retained]
    network = combine(chosen)
    endpoints = network['endpoints']
    full = {tile for tile in network['receiver'] if vertices_of({tile}) <= endpoints
            and not any(vertices_of({tile}) <= module['endpoints'] for module in chosen)}
    events = {(index, point, other) for index in retained for point in modules[index]['endpoints']
              for other in (set(neighbors(point)) & endpoints)-modules[index]['endpoints']-
              modules[index]['selected'] if tuple(value//2 for value in point) ==
              tuple(value//2 for value in other)}
    negative = sum(max(0, -modules[index]['charge']) for index in retained)
    return dict(negative=negative, full=full, events=events,
                reserve=negative+2*len(full)-len(events))


def extensions(name, modules):
    clauses, _ = implications(modules)
    amount = len(modules)
    if amount <= 7:
        masks = range(1 << amount)
    else:
        generator = random.Random(20261020)
        masks = {0, (1 << amount)-1} | {1 << index for index in range(amount)} | {
            generator.randrange(1 << amount) for _ in range(128)}
    closed_sets = {hull(clauses, {index for index in range(amount) if mask >> index & 1})
                   for mask in masks}
    data = {retained: signature(modules, retained) for retained in closed_sets}
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    checked = falling = negative_additions = 0
    for smaller, larger in itertools.product(closed_sets, repeat=2):
        if not smaller < larger:
            continue
        assert feasible(modules, smaller) and feasible(modules, larger)
        added = larger-smaller
        first, second = data[smaller], data[larger]
        assert first['full'] <= second['full'] and first['events'] <= second['events']
        fresh = second['events']-first['events']
        old_new = {event for event in fresh if event[0] in smaller and owners[event[2]] in added}
        new_old = {event for event in fresh if event[0] in added and owners[event[2]] in smaller}
        new_new = {event for event in fresh if event[0] in added and owners[event[2]] in added}
        assert old_new | new_old | new_new == fresh
        assert len(fresh) == len(old_new)+len(new_old)+len(new_new)
        source_mass = sum(max(0, -modules[index]['charge']) for index in added)
        full_gain = len(second['full']-first['full'])
        assert second['reserve']-first['reserve'] == source_mass+2*full_gain-len(fresh)
        checked += 1
        falling += int(second['reserve'] < first['reserve'])
        negative_additions += int(all(modules[index]['charge'] <= 0 for index in added))
    return dict(fixture=name, owners=amount, distinct_legal_subfamilies=len(closed_sets),
                legal_extension_pairs=checked, falling_reserve_pairs=falling,
                nonpositive_only_extensions=negative_additions,
                exhaustive_closed_sets=amount <= 7)


def lattice_counterexample():
    modules = cut_modules(10, 8)+[transform_module(module, (False, False, False), (30, 30))
                                 for module in marked_gate_modules()]
    clauses, _ = implications(modules)
    chamber = frozenset(range(4, len(modules)))
    sets = [chamber]+[chamber | {index} for index in range(4)]+[frozenset(range(len(modules)))]
    expected = [6, 7, 7, 7, 11, 9]
    records = []
    for retained, reserve in zip(sets, expected):
        assert hull(clauses, retained) == retained and feasible(modules, retained)
        report = signature(modules, retained)
        current, moved = contained([modules[index] for index in sorted(retained)])
        independent = inspect_exact(current, moved)
        assert report['reserve'] == reserve == independent['event_reserve']
        assert independent['positive'] == 1 and independent['marked'] == 2
        records.append(dict(added_negative_owners=sorted(index+1 for index in retained if index < 4),
                            reserve=reserve, positive=1, marked=2,
                            allocation_margin=independent['exact_joint_margin']))
    assert hull(clauses, sets[1] | sets[2]) == sets[-1]
    assert sets[1] & sets[2] == chamber
    assert expected[1]+expected[2] < expected[0]+expected[-1]
    assert hull(clauses, sets[3] | sets[4]) == sets[-1]
    assert sets[3] & sets[4] == chamber
    assert expected[3]+expected[4] > expected[0]+expected[-1]
    assert marked_counts(modules, sets[1]) == marked_counts(modules, sets[-1])
    return dict(records=records, submodularity_failure=dict(left=14, right=15),
                supermodularity_failure=dict(left=18, right=15),
                scope='Meet is intersection, join is the exact feasible Horn hull of the '
                      'union. Same fixed complete family and N1,G2 throughout. Examples '
                      'use a separate negative endpoint component; no connected-example '
                      'or allocation-counterexample claim.')


def main():
    controls = [extensions(name, modules) for name, modules in fixtures()]
    print(json.dumps(dict(status='PASS', fixtures=controls,
                         legal_extension_pairs=sum(row['legal_extension_pairs'] for row in controls),
                         lattice_counterexample=lattice_counterexample(),
                         scope='Exact complete-source directed events and actual new mixed '
                         'full tiles on legal extensions. Exhaustive closure sets through '
                         'seven owners only; larger fixtures use sampled hulls. General '
                         'signed-transfer identity and lattice obstructions are written '
                         'proofs. No signed-transfer bound, reserve comparison with the '
                         'least marked hull, or full allocation is inferred.'), indent=2))


if __name__ == '__main__':
    main()
