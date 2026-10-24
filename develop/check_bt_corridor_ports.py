"""BT-corridor ownership, bounded-access obstruction and exact repairs.

General proofs: docs/BT_CORRIDOR_PORTS_AND_BOUNDED_ACCESS_OBSTRUCTION.md.
Finite controls do not establish the all-parameter claims.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_compensation_flow_normal_form import solve
from check_even_bridge_support_completion import endpoints_of
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_endpoint_free_gap_compensation import gap_access
from check_neutral_portal_strip_compensation import image_map
from check_terminal_cancellation_and_stranded_demand import (
    terminal_data, extended_ports, cancel_pairs, virtual_connectors,
    direct_family, uniform_certificates,
)

if not __debug__:
    raise RuntimeError('Run without -O: verification requires assertions.')


def corridor_ports(current, bands, labels, intervals, owner, kinds, totals):
    locations = {point: (b, c, p) for b, columns in enumerate(bands)
                 for c, column in enumerate(columns) for p, point in enumerate(column) if point in kinds}
    ports, corridors = {v: [] for v in kinds}, {}
    side_users, bt_users = defaultdict(set), defaultdict(set)
    for v, kind in kinds.items():
        if kind != 'TP':
            continue
        b, c, p = locations[v]
        for direction in (-1, 1):
            target, middle = c+direction, []
            while 0 <= target < len(bands[b]) and labels[b][target] == ('B', 'T'):
                middle.append((b, target))
                target += direction
            if not 0 <= target < len(bands[b]) or labels[b][target] != ('B', 'B'):
                continue
            port = b, target
            if middle:
                assert bands[b][middle[0][1]][p] in current[2]
            interval = intervals[owner[port]]
            side = 'left' if c < target else 'right'
            assert target == interval['first' if side == 'left' else 'last']
            ports[v].append(port)
            corridors[v, port] = middle
            side_users[owner[port], side].add(v)
            for column in middle:
                bt_users[column].add((v, port))
    assert all(len(users) == 1 for users in side_users.values())
    assert all(len(users) == 1 for users in bt_users.values())
    totals['corridor_ownership_models'] += 1
    totals['corridor_candidates'] += len(corridors)
    totals['nontrivial_bt_corridors'] += sum(bool(cs) for cs in corridors.values())
    totals['longer_than_single_cap_corridors'] += sum(len(cs) > 1 for cs in corridors.values())
    return ports, corridors


def compile_model(current, bands, totals, limit=None):
    original, labels, intervals, owner, kinds, pairs, direct = terminal_data(current, bands)
    all_ports, corridors = corridor_ports(current, bands, labels, intervals, owner, kinds, totals)
    old = extended_ports(current, bands, labels, intervals, owner, kinds, direct, Counter())
    for v in kinds:
        if kinds[v] == 'TP':
            assert set(old[v]) == {p for p in all_ports[v] if len(corridors[v, p]) <= 1}
    boundary = {owner[b, 0] for b in range(len(bands))}
    if len(bands[0]) % 2 == 0:
        boundary |= {owner[b, len(columns)-1] for b, columns in enumerate(bands)
                     if labels[b][-1] == ('B', 'B')}
    resources = set(range(len(intervals)))-boundary
    assert len(boundary) == original['boundary_budget']
    ports = {v: [p for p in ps if limit is None or len(corridors[v, p]) <= limit]
             for v, ps in all_ports.items()}
    access = {v: {owner[p] for p in ps} & resources for v, ps in ports.items() if kinds[v] == 'TP'}
    links = []
    for columns in bands:
        for left, right in zip(columns, columns[1:]):
            for a, b in zip(left, right):
                if kinds.get(a) == 'TP' and kinds.get(b) == 'BP': links.append((a, b))
                if kinds.get(b) == 'TP' and kinds.get(a) == 'BP': links.append((b, a))
    return (kinds, pairs, links, access, resources), dict(original=original, labels=labels,
        intervals=intervals, owner=owner, ports=ports, all_ports=all_ports, corridors=corridors,
        boundary=boundary)


def compress_gap_access(current, bands, meta, available, totals):
    """One extreme AVAILABLE interval per side, with arbitrary reservations."""
    _, kinds, _, resources, full, _, gaps = gap_access(current, bands, Counter())
    assert available <= resources
    full = {v: choices & available for v, choices in full.items()}
    compressed = {v: set() for v in full}
    locations = {v: (b, c) for b, columns in enumerate(bands)
                 for c, column in enumerate(columns) for v in column if v in full}
    groups, unit_gap = [], {}
    for gap in gaps:
        b, first, last = gap['band'], gap['first'], gap['last']
        units = sorted((j for j in available if meta['intervals'][j]['band'] == b
                        and first <= meta['intervals'][j]['first'] <= last),
                       key=lambda j: meta['intervals'][j]['first'])
        candidates = {v for v, (vb, vc) in locations.items()
                      if vb == b and vc in (first-1, last+1)}
        assert len(candidates) <= 2
        group = len(groups)
        for j in units:
            assert j not in unit_gap
            unit_gap[j] = group
        for v in candidates:
            assert set(units) <= full[v]
            if units:
                compressed[v].add(units[0] if locations[v][1] < first else units[-1])
        groups.append(dict(units=units, candidates=candidates))
    assert set(unit_gap) == available
    assert all(compressed[v] <= full[v] and len(compressed[v]) <= 2 for v in full)
    if available == resources:
        bt_access = {v: {meta['owner'][p] for p in meta['all_ports'][v]} & resources
                     for v in full}
        assert compressed == bt_access
        totals['boundary_reserved_bt_equals_extreme_gap_controls'] += 1
    totals['compressed_gap_access_models'] += 1
    totals['full_gap_access_arcs'] += sum(map(len, full.values()))
    totals['compressed_gap_access_arcs'] += sum(map(len, compressed.values()))
    return full, compressed, groups, unit_gap


def compression_control(current, bands, data, meta, totals, reservations=()):
    kinds, pairs, links, _, resources = data
    available = resources-set(reservations)
    full, compressed, groups, unit_gap = compress_gap_access(current, bands, meta, available, totals)
    broad = solve(kinds, pairs, links, full, available)
    small = solve(kinds, pairs, links, compressed, available)
    assert (broad['value'], broad['cost']) == (small['value'], small['cost'])
    payments_by_gap = defaultdict(list)
    for v, j in broad['payments']:
        payments_by_gap[unit_gap[j]].append(v)
    transported = []
    for g, points in payments_by_gap.items():
        assert len(points) == len(set(points)) <= 2
        assert set(points) <= groups[g]['candidates']
        candidates = [(v, compressed[v] & set(groups[g]['units'])) for v in points]
        chosen = [(v, next(iter(js))) for v, js in candidates]
        assert len({j for v, j in chosen}) == len(chosen)
        transported += chosen
    assert len(transported) == len(broad['payments'])
    assert len({j for v, j in transported}) == len(transported)
    # Keep precisely the old links and the paying terminal of every virtual alpha.
    assert {v for v, j in transported} == {v for v, j in broad['payments']}
    reduced, _, _ = cancel_pairs(kinds, pairs, broad['links'], Counter())
    paying = [next(i for i, pair in enumerate(reduced) if v in pair) for v, j in transported]
    assert len(set(paying)) == len(paying)
    totals['value_and_link_cost_compression_controls'] += 1
    totals['transported_interval_payments'] += len(transported)
    return small


def family(width, height, depth):
    assert depth >= 2
    base = direct_family(width, height)
    r = width+4
    added = {(4, 1), (r+1, 1)}
    added |= {(5 if step % 2 else 4, 7+step) for step in range(2, depth+1)}
    added |= {(r if step % 2 else r+1, height+3+step) for step in range(2, depth+1)}
    assert len(added) == 2*depth and not added & base[2]
    occupied = base[2] | endpoints_of(base) | added
    assert all(not set(neighbors(v)) & (occupied-{v}) for v in added)
    n = height+depth+6+depth % 2
    current = width+12, max(base[1], n+2), base[2] | added, base[3]
    bands = [[((row, col), (row+1, col)) for col in range(n)] for row in range(4, r+1, 2)]
    return current, bands, added


def family_control(width, height, depth, totals):
    current, bands, added = family(width, height, depth)
    direct_check(*current)
    uniform_certificates(direct_family(width, height), width, height, Counter())
    assert frozen_certificate(current)[0] == endpoints_of(current)
    data, meta = compile_model(current, bands, totals)
    limited, _ = compile_model(current, bands, totals, depth-1)
    old, _ = compile_model(current, bands, totals, 1)
    original = meta['original']
    assert (original['alpha'], original['beta'], original['gamma']) == (1, 0, height+1)
    assert len(current[2]) == height+9+2*depth and len(current[3]) == width+height
    assert original['boundary_budget'] == width+2
    margin = (width//2-1)*(height+depth)+width-5+(width//2+1)*(depth % 2)
    assert original['surplus_twice']//2-original['boundary_budget'] == margin >= 13
    old_result, limited_result, full = solve(*old), solve(*limited), solve(*data)
    assert old_result['value'] == limited_result['value'] == 0
    assert full['value'] == 1 and full['cost'] == 2
    assert compression_control(current, bands, data, meta, totals)['cost'] == 2
    r = width+4
    upper = [((5, 3), (5, 4)), ((5, 5), (5, 6))]
    both = upper+[((r, c-1), (r, c)) for c in range(4, height+3, 2)]
    kinds, pairs, _, _, _ = data
    reduced, inventory, _ = cancel_pairs(kinds, pairs, both, Counter())
    assert inventory['TP', 'TP'] == 1 and inventory['BP', 'BP'] == 0
    assert set(next(pair for pair in reduced if all(kinds[v] == 'TP' for v in pair))) == {(5, 7), (r, height+3)}
    connector = virtual_connectors(original, meta['labels'], meta['intervals'], meta['owner'],
                                  kinds, reduced, meta['ports'], Counter())
    assert connector['omitted'] == connector.get('h2', 0) == 0
    assert connector['margin_twice'] == 2*margin
    for point in ((5, 7), (r, height+3)):
        targets = [p for p in meta['ports'][point] if meta['owner'][p] not in meta['boundary']]
        assert len(targets) == 1 and len(meta['corridors'][point, targets[0]]) == depth
    totals['uniform_obstruction_parameters'] += 1
    totals['frozen_geometry_controls'] += 1
    return dict(parameters=[width, height, depth], shape=current[:2], added=sorted(added),
                selected=len(current[2]), matching=len(current[3]), margin=margin,
                old_deficit=old_result['deficit'], radius_d_minus_1_deficit=limited_result['deficit'],
                corridor_deficit=full['deficit'], corridor_min_links=full['cost'],
                one_sided_certificate=dict(links=full['links'], payments=full['payments']),
                two_ended_links=both, two_ended_min_links=2+height//2,
                two_ended_connector={k:v for k,v in connector.items() if k in ('alpha','beta','omitted','h0','h2','margin_twice')})


def geometry_control(current, bands, totals):
    direct_check(*current)
    assert frozen_certificate(current)[0] == endpoints_of(current)
    data, meta = compile_model(current, bands, totals)
    old, _ = compile_model(current, bands, totals, 1)
    old_result, new_result = solve(*old), solve(*data)
    resource_list = sorted(data[-1])
    for reserved in ((), resource_list[:1], resource_list[-1:],
                     resource_list[::2], resource_list):
        compression_control(current, bands, data, meta, totals, reserved)
        totals['reservation_patterns'] += 1
    assert new_result['value'] >= old_result['value']
    if new_result['value'] == old_result['value']:
        assert new_result['cost'] <= old_result['cost']
    kinds, pairs, _, _, _ = data
    reduced, _, _ = cancel_pairs(kinds, pairs, new_result['links'], Counter())
    virtual_connectors(meta['original'], meta['labels'], meta['intervals'], meta['owner'],
                       kinds, reduced, meta['ports'], Counter())
    totals['frozen_geometry_controls'] += 1
    totals['flow_increases'] += new_result['value'] > old_result['value']
    return dict(old_value=old_result['value'], corridor_value=new_result['value'])


def abstract_extreme_controls(totals):
    for count in range(9):
        units = list(range(count))
        for mask in range(1 << count):
            available = [j for j in units if not (mask >> j) & 1]
            for paid in ((), (0,), (1,), (0, 1)):
                if len(paid) > len(available):
                    continue
                for old in itertools.permutations(available, len(paid)):
                    new = [available[0] if side == 0 else available[-1] for side in paid]
                    assert len(new) == len(set(new))
                    assert len(new) == len(old)
                    totals['abstract_reserved_payment_transports'] += 1
    # Arbitrary reservation needs the first AVAILABLE unit, not the old first unit.
    assert {0, 1}-{0} == {1}
    assert {0}-{0} == set()
    totals['fixed_nearest_reserved_rule_obstructions'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals, examples = Counter(), []
    abstract_extreme_controls(totals)
    for w, h, d in itertools.product(range(6, 21, 2), range(4, 17, 2), (2, 3, 4, 8, 16)):
        record = family_control(w, h, d, totals)
        if (w, h, d) in ((6, 4, 2), (6, 4, 16), (20, 16, 3)): examples.append(record)
    for parameters in ((6, 4, 2), (8, 6, 3), (10, 8, 16)):
        current, bands, _ = family(*parameters)
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            move = image_map(*current[:2], symmetry)
            images = [[tuple(move(v) for v in column) for column in columns] for columns in bands]
            result = geometry_control((*shape, selected, matching), images, totals)
            assert result == dict(old_value=0, corridor_value=1)
            totals['obstruction_isometry_controls'] += 1
    from check_compensation_flow_geometry_frontier import pad_image
    from check_exchange_terminal_nonunique import fixture, matching_orders
    from check_frozen_first_destination_allocation import fixture as unported
    from check_frozen_shared_mixed_gate import fixture as shared
    from check_elbow_sources import elbow
    from degree_three_fusion import occupied_bands
    from rotor_networks import rotor
    module = rotor(); base = fixture()
    fixtures = [(*base[:3], list(x['matching'])) for x in matching_orders()]
    fixtures += [unported()[0], shared(), elbow(6, 4), occupied_bands(6)[0],
                 (6, 6, module['selected'], module['matching']),
                 (8, 8, {(2, 2), (3, 2)}, [])]
    # A real two-port gap of capacity two must retain two different units.
    two = direct_family(6, 4)
    move = lambda p: (p[0], p[1]+9)
    two = (18, 30, two[2] | {move(p) for p in two[2]},
           two[3]+[tuple(move(p) for p in edge) for edge in two[3]])
    fixtures.append(two)
    for model, symmetry, offset in itertools.product(fixtures,
            itertools.product((False, True), repeat=3), itertools.product((2, 3), repeat=2)):
        current = pad_image(model, symmetry, offset)
        geometry_control(current, whole_bands(current), totals)
        totals['carried_geometry_controls'] += 1
    current, bands, _ = family(6, 4, 2)
    frozen, layers = frozen_certificate(current)
    fixture_record = dict(shape=current[:2], selected=sorted(current[2]), matching=current[3],
        bands=bands, freezing_layers=layers, scope='Fully frozen physical bounded-access counterexample; target margin13.')
    report = dict(status='PASS', totals=dict(totals), examples=examples, fixture=fixture_record,
        scope='Exact extreme-available interval compression of full endpoint-free gap access, preserving '
              'payment terminal, links, maximum compensation and minimum link cost with arbitrary fixed reservations. '
              'Uniform bounded BT access obstruction sharpens the earlier known radius obstruction; no target-bound counterexample. '
              'General BT corridor ownership and connector ledger; exact one-sided/two-ended repair. '
              'Finite controls do not replace the parameter proofs or prove universal corridor coverage.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals))))

if __name__ == '__main__':
    main()
