"""Full-original controls for internal borrowing and zero-gain forced consumers."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_batch_terminal_budget import key, residual, transform
from check_secondary_ten_distinct_pair_consumers import east_rotor, upper_source
from check_secondary_ten_north_contact_debit import inventory
from rotor_networks import rotor, transform_module


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def chain(origin, column_shift, widths, depths, root_breadth=6):
    assert widths and len(widths) == len(depths)
    assert origin % 2 == 1 and column_shift % 2 == 0
    assert root_breadth >= 6 and root_breadth % 2 == 0
    bases = []
    sites = []
    repairs = []
    previous_origin = previous_shift = None
    for index, (width, depth) in enumerate(zip(widths, depths)):
        assert width >= 12 and depth >= 24 and width % 2 == depth % 2 == 0
        if index:
            origin = previous_origin+depths[index-1]-6
            column_shift = previous_shift-width-12
        base = residual(origin, width, 10, depth)+[east_rotor(origin, width, True)]
        base = [shift(record, (0, column_shift)) for record in base]
        base_endpoints = set.union(*(record[0] for record in base))
        long_stem = {(row, column_shift+2)
                     for row in range(origin-4, origin+depth-5)}
        assert long_stem <= base[7][0]
        body = base_endpoints-long_stem
        assert all(origin-6 <= row <= origin+10 for row, column in body)
        assert min(column for row, column in base_endpoints) == column_shift+2
        assert max(column for row, column in base_endpoints) == width+17+column_shift
        if index:
            selected = shift(upper_source(origin, width, widths[index-1]+10,
                                         depths[index-1], 8, True), (0, column_shift))
            assert key(selected) == key(bases[-1][7])
        bases.append(base)
        sites.append((origin, width+14+column_shift, column_shift))
        repairs.append(independent_source((width+12, 10, 4),
                                         (False, False, True),
                                         (origin-8, width+13+column_shift)))
        previous_origin, previous_shift = origin, column_shift
    root = shift(upper_source(sites[0][0], widths[0], root_breadth, 6, 4, True),
                 (0, sites[0][2]))
    return bases, root, repairs, sites


def phi_from(records, receipt):
    return receipt['raw_reserve']+sum(charge(record) > 0 for record in records)


def verify_chain(origin, column_shift, widths, depths, root_breadth=6):
    bases, root, repairs, sites = chain(origin, column_shift, widths, depths, root_breadth)
    records = [record for base in bases for record in base]+[root]
    repaired = records+repairs
    assert len({key(record) for record in repaired}) == len(repaired)
    endpoints = set.union(*(record[0] for record in records))
    repaired_endpoints = set.union(*(record[0] for record in repaired))
    assert len(endpoints) == sum(len(record[0]) for record in records)
    assert len(repaired_endpoints) == sum(len(record[0]) for record in repaired)
    internal_full = set()
    internal_events = set()
    for index, base in enumerate(bases):
        receipt = inventory(base)
        assert phi_from(base, receipt) == widths[index]+8
        assert not internal_full & receipt['full']
        internal_full |= receipt['full']
        converted = {(9*index+owner, point, target)
                     for owner, point, target in receipt['events']}
        assert not internal_events & converted
        internal_events |= converted
    before = inventory(records)
    baseline = sum(width+9 for width in widths)
    expected_cross_full = set()
    expected_cross_events = set()
    missing = []
    renewed = []
    for index, (origin, east_column, offset) in enumerate(sites):
        expected_cross_full.add(((origin-1)//2, east_column//2))
        consumer_owner = len(records)-1 if index == 0 else 9*(index-1)+7
        rotor_owner = 9*index+8
        point, target = (origin, east_column), (origin, east_column+1)
        expected_cross_events |= {(consumer_owner, point, target),
                                  (rotor_owner, target, point)}
        support = origin+2, east_column-2
        assert support in bases[index][7][1] and support not in endpoints
        blockers = {(origin+2, east_column-3), (origin+2, east_column-1),
                    (origin+3, east_column-2)}
        assert blockers <= set(neighbors(support)) & endpoints
        assert support in repairs[index][0]
        assert support[0] % 2 == 1 and support[1] % 2 == 0
        assert charge(repairs[index]) == -(widths[index]+11)
        missing.append(support)
        renewed_support = origin-3, offset+1
        assert renewed_support in repairs[index][1]
        assert renewed_support not in repaired_endpoints
        assert {(origin-4, offset+1), (origin-3, offset+2)} <= (
            set(neighbors(renewed_support)) & repaired_endpoints)
        renewed.append(renewed_support)
    assert before['full']-internal_full == expected_cross_full
    assert before['events']-internal_events == expected_cross_events
    assert phi_from(records, before) == baseline+root_breadth-1-len(bases)
    after = inventory(repaired)
    expected_new_full = set()
    expected_new_events = set()
    for index, (origin, east_column, offset) in enumerate(sites):
        width = widths[index]
        consumer_owner = len(records)+index
        old_owner = 9*index+7
        east_owner = 9*index+4
        band_full = {((origin-7)//2, column//2)
                     for column in range(offset+2, offset+width+12, 2)}
        band_events = {(owner, point, target)
                       for column in range(offset+2, offset+width+12)
                       for owner, point, target in (
                           (old_owner, (origin-6, column), (origin-7, column)),
                           (consumer_owner, (origin-7, column), (origin-6, column)))}
        near_full = {((origin+1)//2, (east_column-2)//2)}
        near_events = {(east_owner, (origin, east_column-1), (origin, east_column-2)),
                       (east_owner, (origin+2, east_column-1), (origin+2, east_column-2)),
                       (consumer_owner, (origin+1, east_column-2), (origin+1, east_column-1))}
        assert not expected_new_full & (band_full | near_full)
        assert not expected_new_events & (band_events | near_events)
        expected_new_full |= band_full | near_full
        expected_new_events |= band_events | near_events
    assert after['full']-before['full'] == expected_new_full
    assert after['events']-before['events'] == expected_new_events
    assert before['full'] <= after['full'] and before['events'] <= after['events']
    assert phi_from(repaired, after) == phi_from(records, before)
    return dict(originals=len(records), repaired_originals=len(repaired),
                blocks=len(bases), baseline=baseline, phi=phi_from(records, before),
                relative_excess=root_breadth-1-len(bases), root_mass=root_breadth-1,
                cross_full_tiles=len(expected_cross_full),
                cross_directed_events=len(expected_cross_events),
                new_repair_mass=sum(width+11 for width in widths),
                new_repair_full_tiles=len(expected_new_full),
                new_repair_directed_events=len(expected_new_events),
                forced_fresh_supports=missing, renewed_missing_supports=renewed,
                complete=False, complete_extendibility='NOT_ASSERTED')


def parity_and_role_controls():
    terminal_controls = rotor_controls = 0
    for breadth, near, far, symmetry in itertools.product(
            (6, 8, 24, 100), (4, 10, 50), (4, 8, 100),
            itertools.product((False, True), repeat=3)):
        record = independent_source((breadth, near, far), symmetry, (-31, 42))
        terminals = [point for point in record[0]
                     if len(set(neighbors(point)) & record[0]) == 1]
        assert len(terminals) == 2
        assert sum(terminals[0]) % 2 != sum(terminals[1]) % 2
        terminal_controls += 1
    for origin, width, offset in itertools.product((-33, 31), (12, 50), (-100, 0, 200)):
        support = origin+2, width+12+offset
        blocker = origin, width+13+offset
        forms = set()
        for symmetry in itertools.product((False, True), repeat=3):
            module = transform_module(rotor(), symmetry)
            record = module['endpoints'], module['selected'], {
                tuple(sorted(edge)) for edge in module['matching']}
            for endpoint in record[0]:
                own = set(neighbors(endpoint)) & record[0]
                if own != {(endpoint[0]-1, endpoint[1])}:
                    continue
                moved = shift(record, (support[0]-endpoint[0], support[1]-endpoint[1]))
                forms.add(key(moved))
                assert blocker in moved[0]
        assert len(forms) == 2
        rotor_controls += len(forms)
    return dict(opposite_color_full_original_terminal_controls=terminal_controls,
                full_original_north_tip_rotor_collision_controls=rotor_controls)


def controls():
    count = 0
    for origin, width, depth, amount in itertools.product(
            (-33, 31), (12, 20, 50), (24, 26, 50, 200), (1, 2, 6, 10)):
        verify_chain(origin, -100, [width]*amount, [depth]*amount)
        count += 1
    nonuniform = []
    for amount, root_breadth in ((7, 6), (12, 8), (24, 10)):
        widths = [12+2*(index % 7) for index in range(amount)]
        depths = [24+2*(index % 11) for index in range(amount)]
        nonuniform.append(verify_chain(31, 0, widths, depths, root_breadth))
    symmetry_controls = 0
    bases, root, repairs, sites = chain(31, 0, [12, 20, 14], [24, 50, 26])
    records = [record for base in bases for record in base]+[root]
    initial_phi = phi_from(records, inventory(records))
    repaired_phi = phi_from(records+repairs, inventory(records+repairs))
    for symmetry in itertools.product((False, True), repeat=3):
        transpose, flip_row, flip_column = symmetry
        offset = ((int(flip_column)-100, int(flip_row)-200) if transpose else
                  (int(flip_row)-100, int(flip_column)-200))
        moved = [transform(record, symmetry, offset) for record in records]
        moved_repairs = [transform(record, symmetry, offset) for record in repairs]
        assert phi_from(moved, inventory(moved)) == initial_phi
        assert phi_from(moved+moved_repairs, inventory(moved+moved_repairs)) == repaired_phi
        symmetry_controls += 1
    witness = verify_chain(31, 0, [12]*8, [24]*8)
    assert witness['relative_excess'] == -3 and witness['phi'] > 0
    return dict(status='PASS', exact_chain_and_zero_gain_set_controls=count,
                nonuniform_controls=nonuniform, tile_preserving_isometry_controls=symmetry_controls,
                role_and_parity=parity_and_role_controls(), witness=witness,
                scope='Finite corroboration of general written chain obstruction, fresh-owner '
                      'lemma and simultaneous zero-gain family. Exact original matching/support '
                      'and physical full-tile/directed-event sets. Neither complete extension '
                      'existence nor failure of a complete-model inequality is asserted.')


if __name__ == '__main__':
    print(json.dumps(controls(), indent=2))
