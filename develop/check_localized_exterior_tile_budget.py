"""Independent exact tile controls for localized complete exterior budgets."""

import itertools
import json
from collections import Counter, defaultdict

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_gap_axial_compensation import transform
from check_exact_event_reserve import fixtures
from check_activated_singleton_budget import phase_images
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_six_row_rotor_exclusion import normalized
from check_terminal_exterior_classification import cap


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def tile_of(point):
    return point[0]//2, point[1]//2


def cells_of(tile):
    return {(2*tile[0]+row, 2*tile[1]+column)
            for row, column in itertools.product(range(2), repeat=2)}


def tile_inventory(records):
    owners = {point: owner for owner, record in enumerate(records) for point in record[0]}
    endpoints = set(owners)
    assert len(endpoints) == sum(len(record[0]) for record in records)
    endpoint_tiles = [{tile_of(point) for point in record[0]} for record in records]
    represented = set.union(*endpoint_tiles)
    supports = defaultdict(list)
    for owner, record in enumerate(records):
        own_occupied = record[0] | record[1]
        assert all(len(set(neighbors(point)) & own_occupied) == 3 for point in record[0])
        assert all(len(set(neighbors(point)) & own_occupied) == 1 for point in record[1])
        for support in record[1]:
            tile = tile_of(support)
            if tile in endpoint_tiles[owner]:
                anchor = set(neighbors(support)) & record[0]
                assert len(anchor) == 1 and tile_of(next(iter(anchor))) == tile
                supports[tile].append((owner, support))
    receipt = inventory(records)
    event_counts = Counter(tile_of(event[1]) for event in receipt['events'])
    result = {}
    for tile in represented:
        cells = cells_of(tile)
        current = cells & endpoints
        own_parts = [cells & record[0] for record in records if cells & record[0]]
        internal_edges = sum(sum(len(set(neighbors(point)) & part) for point in part)//2
                             for part in own_parts)
        edges = sum(len(set(neighbors(point)) & current) for point in current)//2
        original_full = int(any(len(part) == 4 for part in own_parts))
        assert internal_edges == len(current)-len(own_parts)+original_full
        incidences = supports[tile]
        remaining = [(owner, point) for owner, point in incidences if point not in endpoints]
        expected_events = 2*(edges-internal_edges)-(len(incidences)-len(remaining))
        assert expected_events == event_counts[tile]
        weight = 3*len(current)-4*edges-2*len(remaining)+4*int(len(current) == 4)
        result[tile] = dict(endpoints=current, supports=remaining, doubled_weight=weight,
                            endpoint_count=len(current), edge_count=edges,
                            support_count=len(remaining), support_incidence_count=len(incidences))
    positive = sum(charge(record) == 1 for record in records)
    assert all(charge(record) <= 0 or charge(record) == 1 for record in records)
    potential = phi_from(records, receipt)
    assert 2*potential == 4*positive+sum(item['doubled_weight'] for item in result.values())
    return result, potential


def complete_certificate(records):
    data, potential = tile_inventory(records)
    endpoints = set.union(*(record[0] for record in records))
    retained = set.union(*(record[1] for record in records))-endpoints
    occupied = endpoints | retained
    assert all(len(set(neighbors(point)) & occupied) == 1 for point in retained)
    owners = {point: owner for owner, record in enumerate(records) for point in record[0]}
    negative_u = set()
    rotor_pairs = {}
    mates = set()
    allowed = {(1, 1, 1), (1, 2, -1), (2, 0, 2), (2, 1, 0), (3, 0, 1), (4, 0, 0)}
    for tile, item in data.items():
        assert (item['endpoint_count'], item['support_count'], item['doubled_weight']) in allowed
        assert len(item['supports']) == len({point for _, point in item['supports']})
        assert {point for _, point in item['supports']} == cells_of(tile) & retained
        if item['doubled_weight'] != -1:
            continue
        anchor = next(iter(item['endpoints']))
        owner = owners[anchor]
        assert all(index == owner for index, _ in item['supports'])
        original = records[owner]
        if len(original[0]) != 8:
            assert charge(original) == 1
            assert len(set(neighbors(anchor)) & original[0]) == 1
            negative_u.add(tile)
            continue
        candidate_mates = []
        for mate in {tile_of(point) for point in original[0]}:
            cells = cells_of(mate)
            if len(cells & original[0]) != 3:
                continue
            missing = next(iter(cells-original[0]))
            bridges = {point for _, point in item['supports']} & set(neighbors(missing))
            if bridges:
                assert len(bridges) == 1 and missing not in endpoints
                assert data[mate]['doubled_weight'] == 1
                candidate_mates.append(mate)
        assert len(candidate_mates) == 1
        mate = candidate_mates[0]
        assert mate not in mates
        rotor_pairs[tile] = mate
        mates.add(mate)
    counts = Counter(owners[next(iter(data[tile]['endpoints']))] for tile in negative_u)
    assert all(amount <= 2 for amount in counts.values())
    assert not (negative_u & (set(rotor_pairs) | mates))
    positive = sum(charge(record) == 1 for record in records)
    residual = sum(item['doubled_weight'] for tile, item in data.items()
                   if tile not in negative_u | set(rotor_pairs) | mates)
    assert residual >= 0 and len(negative_u) <= 2*positive
    assert 2*potential == 4*positive-len(negative_u)+residual
    assert potential >= positive
    return data, potential, negative_u, rotor_pairs


def old_family(width, rows, left_depth, right_depth):
    assert rows and min(left_depth, right_depth) >= rows[-1]+4
    return [independent_source((width+2, left_depth, right_depth),
                               (False, False, False), (0, -1))]+[
        shift(independent_source((width, 4, 4), (False, False, False), (0, 0)),
              (row, 0)) for row in rows]


def spanning(width, upper, lower, downward):
    depth = lower-upper-6
    original = independent_source((width, depth, depth), (False, False, False), (0, 0))
    return transform(original, lambda point: (
        upper+5+point[0] if downward else lower-1-point[0], point[1]))


def localized_certificate(old, additions, width, rows):
    records = old+additions
    data, potential, negative_u, rotor_pairs = complete_certificate(records)
    baseline, old_potential = tile_inventory(old)
    assert old_potential == 1-len(rows)
    chambers = [{(row//2, column//2)
                 for row in range(upper+2, lower) for column in range(0, width+2)}
                for upper, lower in zip(rows, rows[1:])]
    assert sum(len(region) for region in chambers) == len(set().union(*chambers))
    inside = set().union(*chambers)
    exterior = set(data) | set(baseline)
    exterior -= inside
    regions = chambers+[exterior]
    group = [[] for _ in regions]
    for record in additions:
        tiles = {tile_of(point) for point in record[0]}
        positions = [index for index, region in enumerate(regions) if tiles <= region]
        assert len(positions) == 1
        group[positions[0]].append(record)
    deltas = []
    for index, (region, sources) in enumerate(zip(regions, group)):
        positive = sum(charge(record) == 1 for record in sources)
        old_weight = sum(baseline[tile]['doubled_weight'] for tile in region if tile in baseline)
        assert old_weight == (-4 if index == len(chambers) else -6)
        local_negative = negative_u & region
        allowed_owners = set().union(*(record[0] for record in sources)) if sources else set()
        assert all(data[tile]['endpoints'] <= allowed_owners for tile in local_negative)
        local_pairs = {tile: mate for tile, mate in rotor_pairs.items() if tile in region}
        assert all(mate in region for mate in local_pairs.values())
        removed = local_negative | set(local_pairs) | set(local_pairs.values())
        residual = sum(data[tile]['doubled_weight'] for tile in region-removed if tile in data)
        assert residual >= 0 and len(local_negative) <= 2*positive
        delta = phi_from(old+sources, inventory(old+sources))-old_potential
        final_weight = sum(data[tile]['doubled_weight'] for tile in region if tile in data)
        assert 2*delta == 4*positive+final_weight-old_weight
        assert 2*delta == 4*positive-len(local_negative)+residual-old_weight
        assert delta >= (2 if index == len(chambers) else 3)+positive
        deltas.append(delta)
    assert potential == old_potential+sum(deltas)
    return dict(Phi=potential, chamber_deltas=deltas[:-1], exterior_delta=deltas[-1],
                exterior_positive=sum(charge(record) == 1 for record in group[-1]))


def local_controls():
    checked = 0
    types = Counter()
    cells = cells_of((0, 0))
    for states in itertools.product(range(3), repeat=4):
        points = sorted(cells)
        endpoints = {point for point, state in zip(points, states) if state == 1}
        selected = {point for point, state in zip(points, states) if state == 2}
        if not endpoints:
            continue
        occupied = endpoints | selected
        if any(len(set(neighbors(point)) & occupied) != 1 for point in selected):
            continue
        if any(not set(neighbors(point)) & occupied for point in endpoints):
            continue
        edges = sum(len(set(neighbors(point)) & endpoints) for point in endpoints)//2
        weight = 3*len(endpoints)-4*edges-2*len(selected)+4*int(len(endpoints) == 4)
        assert (len(endpoints), len(selected), weight) in {
            (1, 1, 1), (1, 2, -1), (2, 0, 2), (2, 1, 0), (3, 0, 1), (4, 0, 0)}
        types[len(endpoints), len(selected), weight] += 1
        checked += 1
    return dict(physical_states=checked, types=[dict(endpoints=key[0], supports=key[1],
        doubled_weight=key[2], states=value) for key, value in sorted(types.items())])


def source_controls():
    checked = 0
    for dimensions, symmetry, phase in itertools.product(
            ((6, 4, 4), (8, 4, 10), (20, 12, 4), (100, 40, 60)),
            itertools.product((False, True), repeat=3), itertools.product(range(2), repeat=2)):
        complete_certificate([independent_source(dimensions, symmetry, phase)])
        checked += 1
    for reflected, row, column in itertools.product((False, True), range(2), range(2)):
        complete_certificate([shift(normalized(reflected), (row, column))])
        checked += 1
    return checked


def cut_controls():
    records = [independent_source((6, 4, 4), symmetry, phase)
               for symmetry, phase in itertools.product(
                   itertools.product((False, True), repeat=3),
                   itertools.product(range(2), repeat=2))]
    records += [shift(normalized(reflected), phase)
                for reflected, phase in itertools.product(
                    (False, True), itertools.product(range(2), repeat=2))]
    checked = rejected = 0
    for record in records:
        data, _, negative_u, pairs = complete_certificate([record])
        tiles = sorted(data)
        for choices in itertools.product((False, True), repeat=len(tiles)):
            region = {tile for tile, chosen in zip(tiles, choices) if chosen}
            if any(mate not in region for tile, mate in pairs.items() if tile in region):
                rejected += 1
                continue
            old_weight = sum(data[tile]['doubled_weight'] for tile in region)
            old_terminals = len(region & negative_u)
            assert -old_terminals-old_weight <= 0
            checked += 1
    data, potential, negative_u, pairs = complete_certificate([shift(normalized(False), (1, 0))])
    assert potential == 0 and not negative_u
    tile = (0, 0)
    assert data[tile]['endpoints'] == {(1, 1)}
    assert data[tile]['doubled_weight'] == -1 and pairs[tile] == (1, 0)
    assert -(data[tile]['doubled_weight']) == 1 > 0
    return dict(admissible_single_source_tile_cuts=checked,
                cuts_rejected_for_missing_old_rotor_mate=rejected,
                missing_mate_counterexample=dict(old_Phi=potential, additions=0,
                    marginal=0, positive_added=0, eligible_old_U_terminals=0,
                    old_doubled_tile_weight=-1, false_lower_bound_doubled=1))


def physical_controls():
    checked = 0
    negative_rotor_pairs = 0
    for _, modules in fixtures():
        for _, _, _, _, moved in phase_images(modules):
            records = [(module['endpoints'], module['selected'],
                        {tuple(sorted(edge)) for edge in module['matching']}) for module in moved]
            _, _, _, pairs = complete_certificate(records)
            negative_rotor_pairs += len(pairs)
            checked += 1
    return dict(complete_fusion_images=checked, explicit_negative_rotor_pairs=negative_rotor_pairs)


def crossing_controls():
    checked = 0
    witness = None
    for width, gaps, breadth, near, far, reflected in itertools.product(
            (6, 10, 20), (0, 1, 3), (6, 12, 50), (4, 6, 20), (4, 10, 30), (False, True)):
        rows = tuple(2+10*index for index in range(gaps+1))
        last = rows[-1]+4
        old = old_family(width, rows, last, last+6)
        fill = [spanning(width, upper, lower, False) for upper, lower in zip(rows, rows[1:])]
        closure = cap(width, 4, rows[-1])
        outer = independent_source((breadth, far, near), (False, False, False), (0, 0))
        outer = transform(outer, lambda point: (last+1+near-point[0], point[1]-breadth))
        additions = fill+[closure, outer]
        if reflected:
            move = lambda point: (point[0], width+1-point[1])
            old = [transform(record, move) for record in old]
            additions = [transform(record, move) for record in additions]
        result = localized_certificate(old, additions, width, rows)
        assert result['exterior_delta'] == 6 and result['exterior_positive'] == 2
        assert result['Phi'] == 4*gaps+6
        checked += 1
        if witness is None:
            witness = dict(width=width, gaps=gaps, left_wall=last, right_wall=last+6,
                           breadth=breadth, near=near, far=far, **result)
    return dict(complete_short_wall_crossings=checked, witness=witness)


def chamber_controls():
    checked = 0
    baseline_shared_supports = 0
    for width, gaps, modes, extra in itertools.product(
            (6, 12, 20), ((10,), (12, 20), (10, 12, 10)),
            itertools.product((False, True), repeat=3), (6, 20)):
        rows = [2]
        for gap in gaps:
            rows.append(rows[-1]+gap)
        old = old_family(width, rows, rows[-1]+4+extra, rows[-1]+8+extra)
        additions = [spanning(width, upper, lower, mode)
                     for upper, lower, mode in zip(rows, rows[1:], modes)]
        additions.append(cap(width, 4, rows[-1]))
        result = localized_certificate(old, additions, width, rows)
        assert result['exterior_delta'] == 5
        assert result['chamber_deltas'] == [width+1 if mode else 5 for mode in modes[:len(gaps)]]
        baseline, _ = tile_inventory(old)
        baseline_shared_supports += sum(item['support_count'] !=
            len({point for _, point in item['supports']}) for item in baseline.values())
        checked += 1
    assert baseline_shared_supports > 0
    return dict(complete_nonuniform_chamber_families=checked,
                incomplete_old_tiles_with_shared_support_incidence=baseline_shared_supports)


def incomplete_controls():
    fixed = old_family(6, (2, 12), 28, 32)
    checked = 0
    occupied = set.union(*(record[0] for record in fixed))
    for dimensions, symmetry, offset in itertools.product(
            ((6, 4, 4), (8, 6, 4)), itertools.product((False, True), repeat=3),
            itertools.product(range(-12, 33, 4), range(-12, 17, 4))):
        record = independent_source(dimensions, symmetry, offset)
        if record[0] & occupied:
            continue
        tile_inventory(fixed+[record])
        checked += 1
    return checked


def main():
    print(json.dumps(dict(status='PASS', local=local_controls(), source_images=source_controls(),
        cuts=cut_controls(),
        physical=physical_controls(), incomplete_inventories=incomplete_controls(),
        chambers=chamber_controls(), wall_crossings=crossing_controls(),
        scope='Exact source-labelled event identity with original support multiplicity; '
              'complete tile table and injective rotor pairing; independent localized '
              'marginals on complete nonuniform and finite-wall crossing families. '
              'Separate general written proof, not finite enumeration as proof. '
              'No arbitrary-grid decomposition or unrestricted coefficient improvement.'), indent=2))


if __name__ == '__main__':
    main()
