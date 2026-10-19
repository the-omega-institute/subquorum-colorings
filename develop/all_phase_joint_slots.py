"""Single-use corner, tip and irregular slots for every supported source phase."""

import itertools

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors, occupied_degrees
from dual_guard_compensation import paired_guards
from rotor_networks import combine


def tile_of(point):
    return tuple(value//2 for value in point)


def boundary(module):
    endpoints = module['endpoints']
    occupied = endpoints | module['selected']
    no_exterior = set()
    continuation_failures = set()
    irregular = set()
    for point in endpoints:
        cells = vertices_of({tile_of(point)})
        if not (set(neighbors(point))-cells) & endpoints:
            no_exterior.add(point)
        profile = len(cells & endpoints), len(cells & module['selected'])
        for blank in (set(neighbors(point)) & cells)-occupied:
            other = next(iter((set(neighbors(point)) & cells)-{blank}))
            continuation = tuple(2*value-original for value, original in zip(point, other))
            if continuation not in endpoints:
                continuation_failures.add(point)
            if profile in {(1, 1), (2, 0)}:
                irregular.add(point)
    return no_exterior, continuation_failures, irregular


def inspect_slots(current, modules):
    network = combine(modules)
    endpoints = network['endpoints']
    owners = {point: index for index, module in enumerate(modules) for point in module['endpoints']}
    assert len(owners) == sum(len(module['endpoints']) for module in modules)
    degrees = occupied_degrees(current)
    boundaries = [boundary(module) for module in modules]
    pools = []
    events = set()
    positive = 0
    negative_mass = 0
    minus_one = 0
    vertical_phase = 0
    diagonal_phase = 0
    for index, module in enumerate(modules):
        no_exterior, failures, irregular = boundaries[index]
        rotor = len(module['endpoints']) == 8
        pool = irregular if rotor else irregular | no_exterior | failures
        pools.append(pool)
        charge = module['charge']
        if charge == 1:
            positive += 1
            assert not pool
        else:
            negative_mass -= charge
            if charge == -1:
                minus_one += 1
                assert not failures and len(no_exterior) == len(irregular) == 2
                assert len(pool) == 4
            elif charge <= -5:
                if failures:
                    diagonal_phase += 1
                    assert len(failures) == 4 and len(pool) == -2*charge
                else:
                    vertical_phase += 1
                    assert len(no_exterior) == 2 and len(pool) == -2*charge+2
            else:
                assert rotor and charge in (0, -2)
                assert len(pool) == -2*charge
        old_occupied = module['endpoints'] | module['selected']
        for point in irregular:
            new_neighbors = (set(neighbors(point)) & endpoints)-old_occupied
            if any(tile_of(point) == tile_of(other) for other in new_neighbors):
                events.add(point)
    assigned = set()
    records = []
    donor_tiles = set()
    for module in modules:
        if module['charge'] != 1:
            continue
        for selected, anchor, opposite, guard in paired_guards(module):
            tile = tile_of(selected)
            assert tile not in donor_tiles
            donor_tiles.add(tile)
            protectors = (set(neighbors(anchor)) & module['endpoints']) | {guard}
            if not any(degrees[point] == 4 for point in protectors):
                continue
            inward = tuple(first-second for first, second in zip(selected, anchor))
            gate = tuple(first-second for first, second in zip(opposite, inward))
            if gate in endpoints:
                witness = gate
                kind = 'gate'
                assert witness in boundaries[owners[witness]][0]
            else:
                assert gate not in network['selected']
                candidates = {selected, opposite} & endpoints
                assert candidates
                witness = min(candidates)
                kind = 'blank_gate'
                assert witness in boundaries[owners[witness]][1]
            owner = owners[witness]
            assert len(modules[owner]['endpoints']) != 8
            assert witness in pools[owner] and witness not in assigned
            assert witness not in events
            assigned.add(witness)
            records.append(dict(tile=tile, witness=witness, owner=owner, kind=kind,
                                source_charge=modules[owner]['charge']))
    capacity = sum(len(pool) for pool in pools)
    assert capacity == 2*negative_mass+2*minus_one+2*vertical_phase
    assert not events & assigned
    assert events | assigned <= set.union(set(), *pools)
    assert len(events)+len(assigned) <= capacity
    return dict(positive=positive, negative_mass=negative_mass, minus_one=minus_one,
                vertical_phase=vertical_phase, diagonal_phase=diagonal_phase,
                irregular_events=len(events), marked_sides=len(assigned),
                joint_capacity=capacity, marked_assignments=records)
