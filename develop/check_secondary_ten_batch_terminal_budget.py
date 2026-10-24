"""Physical terminal, owner and exact event-set controls for packed repairs."""

import itertools
import json
from collections import Counter

from check_cooperative_promotion import neighbors
from check_incident_eight_north_transfer import axial_library, charge, shift
from check_secondary_ten_distinct_pair_consumers import east_rotor, east_source, upper_source
from check_secondary_ten_north_contact_debit import inventory
from check_secondary_ten_north_return_closure import continuation, returning
from check_secondary_ten_north_third_left_return import phi, sources
from rotor_networks import affine


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def key(record):
    return tuple(frozenset(part) for part in record)


def transform(record, symmetry, offset):
    move = lambda point: affine(point, symmetry, offset)
    return ({move(point) for point in record[0]},
            {move(point) for point in record[1]},
            {tuple(sorted((move(first), move(second)))) for first, second in record[2]})


def transform_route(route, symmetry, offset):
    return dict(base=[transform(record, symmetry, offset) for record in route['base']],
                consumer=transform(route['consumer'], symmetry, offset),
                terminal=affine(route['terminal'], symmetry, offset),
                baseline=route['baseline'], cost=route['cost'], breadth=route['breadth'])


def residual(origin, width, gap=8, far=4):
    return sources(origin+9, width)+[
        returning(origin+9, width, 0),
        continuation(origin+9, width, width+gap, 8, far, False)]


def route(origin, width, breadth, depth, far, kind, north):
    base = residual(origin, width)
    baseline = phi([base[0], base[1], base[5]])
    if kind == 'east':
        consumer = east_source(origin, width, breadth, depth, far, north)
        terminal = origin+1, width+14
    else:
        base += [east_rotor(origin, width, north)]
        consumer = upper_source(origin, width, breadth, depth, far, True)
        terminal = origin, width+14
    return dict(base=base, consumer=consumer, terminal=terminal,
                baseline=baseline, cost=1+int(not north), breadth=breadth)


def batch(routes):
    base_records = [record for current in routes for record in current['base']]
    if len({key(record) for record in base_records}) != len(base_records):
        return None
    consumers = {key(current['consumer']): current['consumer'] for current in routes}
    if consumers.keys() & {key(record) for record in base_records}:
        return None
    records = base_records+list(consumers.values())
    endpoints = [record[0] for record in records]
    if len(set.union(*endpoints)) != sum(map(len, endpoints)):
        return None
    index = {key(record): number for number, record in enumerate(records)}
    global_inventory = inventory(records)
    claimed_full = set()
    claimed_events = set()
    internal_full = set()
    internal_events = set()
    assignments = Counter()
    costs = Counter()
    widths = {}
    used_terminals = {}
    for current in routes:
        base = current['base']
        consumer = current['consumer']
        before, after = inventory(base), inventory(base+[consumer])
        local_full = after['full']-before['full']
        mapping = [index[key(record)] for record in base+[consumer]]
        convert = lambda event: (mapping[event[0]], event[1], event[2])
        base_events = {convert(event) for event in before['events']}
        local_events = {convert(event) for event in after['events']-before['events']}
        assert not internal_full & before['full']
        assert not internal_events & base_events
        internal_full |= before['full']
        internal_events |= base_events
        assert not claimed_full & local_full
        assert not claimed_events & local_events
        claimed_full |= local_full
        claimed_events |= local_events
        base_endpoints = set.union(*(record[0] for record in base))
        for tile in local_full:
            cells = {(2*tile[0]+row, 2*tile[1]+column)
                     for row, column in itertools.product(range(2), repeat=2)}
            assert len(cells & consumer[0]) == len(cells & base_endpoints) == 2
        contact = 2*len(local_full)-len(local_events)
        assert current['baseline']-phi(base)-contact == current['cost']
        owner = index[key(consumer)]
        terminal = current['terminal']
        own_neighbors = set(neighbors(terminal)) & consumer[0]
        assert terminal in consumer[0] and len(own_neighbors) == 1
        inward = next(iter(own_neighbors))
        anchor = 2*terminal[0]-inward[0], 2*terminal[1]-inward[1]
        assert sum(anchor in record[0] for record in base) == 1
        assert terminal not in used_terminals.setdefault(owner, set())
        used_terminals[owner].add(terminal)
        terminals = {point for point in consumer[0]
                     if len(set(neighbors(point)) & consumer[0]) == 1}
        assert len(terminals) == 2 and terminal in terminals
        assignments[owner] += 1
        costs[owner] += current['cost']
        widths[owner] = current['breadth']
        assert charge(consumer) == 1-current['breadth']
    assert not internal_full & claimed_full
    assert not internal_events & claimed_events
    extra_full = global_inventory['full']-internal_full-claimed_full
    extra_events = global_inventory['events']-internal_events-claimed_events
    assert global_inventory['full'] == internal_full | claimed_full | extra_full
    assert global_inventory['events'] == internal_events | claimed_events | extra_events
    for owner, amount in assignments.items():
        assert amount <= 2 and costs[owner] <= 2*amount
        assert widths[owner]-1-costs[owner] >= widths[owner]-1-2*amount >= 1
    remaining = sum(widths[owner]-1-costs[owner] for owner in assignments)
    exterior = 2*len(extra_full)-len(extra_events)
    baseline = sum(current['baseline'] for current in routes)
    assert phi(records) == baseline+remaining+exterior
    assert phi(records) >= baseline+len(consumers)+exterior
    return dict(records=records, remaining=remaining, exterior=exterior,
                full=extra_full, events=extra_events, baseline=baseline,
                phi=phi(records), distinct_consumers=len(consumers),
                routes=len(routes))


def controls():
    independent_batches = shared_batches = shared_isometries = obstructions = 0
    for kind, north in itertools.product(('east', 'rotor'), (False, True)):
        current = route(31, 12, 16, 6, 6, kind, north)
        for symmetry in itertools.product((False, True), repeat=3):
            transpose, flip_row, flip_column = symmetry
            offsets = (int(flip_column), int(flip_row)) if transpose else (
                int(flip_row), int(flip_column))
            first = transform_route(current, symmetry, offsets)
            second = transform_route(current, symmetry, (offsets[0]+1000, offsets[1]+1000))
            result = batch([first, second])
            assert result is not None and result['exterior'] == 0
            independent_batches += 1
    mixed = [transform_route(route(31, 12, 16, 6, 6, kind, north),
                             (False, False, False), (1000*number, -1000*number))
             for number, (kind, north) in enumerate(
                 itertools.product(('east', 'rotor'), (False, True)))]
    mixed_result = batch(mixed)
    assert mixed_result is not None and mixed_result['distinct_consumers'] == 4
    assert mixed_result['exterior'] == 0
    witness = None
    for width, breadth, kind, north, other_north in itertools.product(
            (12, 20, 50, 200), (6, 8, 10, 16, 18, 24, 50),
            ('east', 'rotor'), (False, True), (False, True)):
        if kind == 'east' and north != other_north:
            continue
        first = route(31, width, breadth, 4, 4, kind, north)
        second = route(31, width, breadth, 4, 4, kind, other_north)
        if kind == 'east':
            reflection = (False, True, False)
            offset = (2*31+3-breadth if north else 2*31+1+breadth, 0)
        else:
            reflection = (False, False, True)
            offset = (0, 2*(width+13)+breadth+1)
        second = transform_route(second, reflection, offset)
        assert key(first['consumer']) == key(second['consumer'])
        result = batch([first, second])
        if result is None:
            continue
        assert result['distinct_consumers'] == 1 and result['routes'] == 2
        shared_batches += 1
        if width == 12:
            for symmetry in itertools.product((False, True), repeat=3):
                transpose, flip_row, flip_column = symmetry
                offset = ((int(flip_column)-100, int(flip_row)-200) if transpose else
                          (int(flip_row)-100, int(flip_column)-200))
                moved = batch([transform_route(current, symmetry, offset)
                               for current in (first, second)])
                assert moved is not None
                assert (moved['phi'], moved['baseline'], moved['remaining'], moved['exterior']) == (
                    result['phi'], result['baseline'], result['remaining'], result['exterior'])
                shared_isometries += 1
        if kind == 'east' and north and breadth == 16:
            old_breadth = width+8
            expected_full = {((31-7)//2, column//2) for column in range(4, width+11, 2)}
            expected_events = {(owner, point, target)
                               for column in range(4, width+12)
                               for owner, point, target in (
                                   (7, (31-6, column), (31-7, column)),
                                   (15, (31-7, column), (31-6, column)))}
            assert result['full'] == expected_full and result['events'] == expected_events
            assert result['remaining'] == 13 and result['exterior'] == -old_breadth
            assert result['phi']-result['baseline'] == 5-width
            assert result['phi'] == width+23
            occupied = set.union(*(record[0] | record[1] for record in result['records']))
            endpoints = set.union(*(record[0] for record in result['records']))
            missing = ((31-6, 3), (31-7, 3))
            assert all(point in occupied-endpoints for point in missing)
            assert all(len(set(neighbors(point)) & occupied) >= 2 for point in missing)
            obstructions += 1
            if width == 12:
                witness = dict(origin=31, width=width, residual_breadth=old_breadth,
                               shared_U=[16, 4, 4], remaining_owner_budget=13,
                               extra_full_tiles=sorted(result['full']),
                               extra_directed_events=sorted(result['events']),
                               exterior=result['exterior'], actual_phi=result['phi'],
                               baseline_sum=result['baseline'], gap=5-width,
                               unconsumed_adjacent_original_supports=missing,
                               complete=False)
    assert witness is not None and shared_batches > obstructions
    return dict(status='PASS', independent_isometry_batches=independent_batches,
                mixed_four_route_batches=1,
                endpoint_disjoint_shared_consumer_batches=shared_batches,
                shared_consumer_isometry_batches=shared_isometries,
                unbounded_exterior_family_controls=obstructions, witness=witness,
                scope='Full original-source and exact directed-event controls of a written '
                      'conditional batch theorem. Partial inventories are not asserted complete '
                      'or extendible; global allocation and complete exterior condition remain open.')


def opposing_exclusion_controls():
    forced_sites = upper_collisions = east_role_controls = 0
    library, rotors = axial_library({(-1, 0), (0, 1)})
    for origin, width in itertools.product((-33, 31), (12, 20, 50, 200)):
        first = route(origin, width, 16, 4, 4, 'east', True)
        second = transform_route(first, (False, True, False), (2*origin-13, 0))
        prefix = first['base']+second['base']+[first['consumer']]
        endpoints = set.union(*(record[0] for record in prefix))
        target = origin, width+14
        assert target in first['base'][4][1] and target not in endpoints
        assert (origin, width+13) in first['base'][4][0]
        assert (origin+1, width+14) in first['consumer'][0]
        assert (origin, width+17) in first['consumer'][0]
        assert (origin+1, width+16) in first['consumer'][0]
        forced_sites += 1
        for breadth, depth, far, right in itertools.product(
                (6, 8, 50), (4, 6, 8, 10, 12, 14, 16, 18, 100), (4, 200), (False, True)):
            consumer = upper_source(origin, width, breadth, depth, far, right)
            if depth >= 16:
                witness, blocker = (origin-15, width+14), second['base'][3]
            elif right:
                witness, blocker = (origin+1-depth, width+17), first['consumer']
            elif depth <= 6:
                witness, blocker = (origin+1-depth, width+11), first['base'][7]
            else:
                witness, blocker = (origin+1-depth, width+11), second['base'][7]
            assert target in consumer[0]
            assert witness in consumer[0] & blocker[0]
            upper_collisions += 1
        if width == 12:
            for relative in library:
                if (0, 1) not in relative[0]:
                    continue
                current = shift(relative, target)
                assert (origin, width+17) in current[0] & first['consumer'][0]
                east_role_controls += 1
            for relative in rotors:
                if (0, 1) not in relative[0]:
                    continue
                current = shift(relative, target)
                assert (origin+1, width+16) in current[0] & first['consumer'][0]
                east_role_controls += 1
    return dict(forced_original_support_controls=forced_sites,
                unbounded_parameter_collision_controls=upper_collisions,
                bounded_full_original_east_role_controls=east_role_controls,
                east_U_catalogue_dimensions_at_most=18,
                scope='Written complete-extension exclusion uses the accepted A north-rotor '
                      'exclusions; these full-source checks corroborate the new blockers.')


def reflected_family_controls():
    overlapping = separated = 0
    for origin, width, breadth in itertools.product(
            (-33, 31), (12, 20, 50, 200), (6, 8, 10, 12, 14, 18, 20, 50, 200)):
        first = route(origin, width, breadth, 4, 4, 'east', True)
        second = transform_route(first, (False, True, False), (2*origin+3-breadth, 0))
        assert key(first['consumer']) == key(second['consumer'])
        if breadth <= 14:
            witness = origin+8-breadth, width+11
            assert witness in first['base'][7][0] & second['base'][7][0]
            assert key(first['base'][7]) != key(second['base'][7])
            overlapping += 1
        else:
            assert min(point[0] for record in first['base'] for point in record[0])-max(
                point[0] for record in second['base'] for point in record[0]) >= 3
            result = batch([first, second])
            assert result is not None and result['exterior'] == 0
            assert result['phi']-result['baseline'] == breadth-3 >= 15
            assert result['distinct_consumers'] == 1
            separated += 1
    return dict(explicit_small_breadth_base_collisions=overlapping,
                exact_separated_shared_consumer_ledgers=separated,
                scope='Written all-breadth classification: h<=14 collides, h16 complete-excluded, '
                      'h>=18 has zero exterior and exact excess h-3. No complete realization asserted.')


if __name__ == '__main__':
    result = controls()
    result['opposing_complete_exclusion'] = opposing_exclusion_controls()
    result['reflected_two_route_family'] = reflected_family_controls()
    print(json.dumps(result, indent=2))
