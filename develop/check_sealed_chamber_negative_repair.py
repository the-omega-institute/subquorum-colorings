"""Full-source checks for sealed-gap localization and a negative-branch repair."""

import itertools
import json
import random

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records, rotor_record
from check_even_gap_axial_compensation import baseline, make_source, transform
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_wide_gate_escape_compensation import signature


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def negative_source():
    return independent_source((6, 4, 4), (True, True, False), (3, 7))


def repaired_source(breadth, near, far):
    return independent_source((breadth, near, far), (True, True, True), (12, 1+near))


def retained(width, rows, extra=0):
    return baseline(width, rows, extra)


def branch(width, top=2, extra=0):
    return retained(width, (top, top+12), extra)+[
        shift(make_source('R', 6, 4, 4), (top, 0)),
        shift(negative_source(), (top, 0))]


def options(width):
    return [(breadth, near, far, repaired_source(breadth, near, far))
            for breadth in (6, 8, 10) for near in range(8, width-1, 2)
            for far in range(4, near-(7 if breadth < 10 else 1), 2)]


def branch_receipts(width, top=2, extra=0, offset=(0, 0)):
    records = [shift(record, offset) for record in branch(width, top, extra)]
    before = inventory(records[:3])
    selected = inventory(records[:4])
    after = inventory(records)
    assert phi_from(records[:3], before) == -1
    assert phi_from(records[:4], selected) == 1
    assert phi_from(records, after) == 0
    assert charge(records[-1]) == -1
    full = {(top//2+2+offset[0]//2, 2+offset[1]//2)}
    events = {(3, (top+5+offset[0], 4+offset[1]), (top+4+offset[0], 4+offset[1])),
              (3, (top+9+offset[0], 2+offset[1]), (top+9+offset[0], 3+offset[1])),
              (4, (top+4+offset[0], 3+offset[1]), (top+5+offset[0], 3+offset[1])),
              (4, (top+4+offset[0], 5+offset[1]), (top+5+offset[0], 5+offset[1]))}
    assert after['full']-selected['full'] == full
    actual_events = after['events']-selected['events']
    assert len(actual_events) == 4
    assert actual_events == events
    gate = top+11+offset[0], 1+offset[1]
    endpoints = set.union(*(record[0] for record in records))
    assert gate in records[3][1] and gate not in endpoints
    assert set(neighbors(gate)) & endpoints == {
        (gate[0]-1, gate[1]), (gate[0]+1, gate[1]), (gate[0], gate[1]-1)}
    return records


def role_controls():
    dimensions = tuple(itertools.product((6, 8, 10, 12, 40), (4, 6, 8, 12, 40), (4, 6, 8, 12, 40)))
    originals = [independent_source(size, symmetry, (0, 0))
                 for size, symmetry in itertools.product(dimensions, itertools.product((False, True), repeat=3))]
    rotors = [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    roles = [0, 0]
    patterns = survivors = 0
    for width, top, extra, offset in itertools.product(
            (8, 10, 12, 14, 20, 100), (2, 40), (0, 20), ((0, 0), (-100, -200))):
        fixed = branch_receipts(width, top, extra, offset)
        endpoints = set.union(*(record[0] for record in fixed))
        gate = top+11+offset[0], 1+offset[1]
        actual = set()
        for kind, library in enumerate((originals, rotors)):
            for original in library:
                for record in anchor_records(original, gate, {(0, 1)}):
                    roles[kind] += 1
                    if not record[0] & endpoints:
                        assert kind == 0
                        actual.add(signature(record))
        expected = {signature(shift(record, (top+offset[0], offset[1])))
                    for breadth, near, far, record in options(width)
                    if (breadth, near, far) in dimensions}
        assert actual == expected
        if width == 8:
            assert not actual and not options(width)
        else:
            assert options(width)
        patterns += 1
        survivors += len(actual)
    return dict(patterns=patterns, U_roles=roles[0], rotor_roles=roles[1], survivors=survivors)


def receipt_controls():
    checked = 0
    for width, top in itertools.product((10, 12, 14, 20, 40, 100), (2, 40)):
        fixed = branch(width, top, 20)
        before = inventory(fixed)
        for breadth, near, far, canonical in options(width):
            record = shift(canonical, (top, 0))
            after = inventory(fixed+[record])
            expected_full = {(top//2+5, column) for column in (0, 1, 2)}
            expected_events = {(3, (top+10, column), (top+11, column)) for column in (2, 4)}
            expected_events |= {(5, (top+11, column), (top+10, column)) for column in (1, 3, 5)}
            assert after['full']-before['full'] == expected_full
            assert after['events']-before['events'] == expected_events
            assert before['full'] <= after['full'] and before['events'] <= after['events']
            assert charge(record) == -1
            assert phi_from(fixed+[record], after)-phi_from(fixed, before) == 2
            checked += 1
    return checked


def localization_controls():
    checked = sources = outside = 0
    library = [independent_source(size, symmetry, (0, 0))
               for size, symmetry in itertools.product(((6, 4, 4), (8, 6, 4), (6, 4, 8)),
                   itertools.product((False, True), repeat=3))]
    library += [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    for width, gap in itertools.product((6, 12, 20), (10, 12, 20)):
        old = retained(width, (2, 2+gap), 20)
        occupied = set.union(*(record[0] for record in old))
        chamber = {(row, column) for row in range(4, 2+gap) for column in range(1, width+1)}
        chamber_tiles = {(row//2, column//2) for row, column in chamber}
        for original in library:
            for row, column in itertools.product(range(-10, 30, 2), range(-10, 31, 2)):
                record = shift(original, (row, column))
                if record[0] & occupied:
                    continue
                sources += 1
                if record[0] & chamber:
                    assert record[0] <= chamber
                    checked += 1
                else:
                    assert not {(point[0]//2, point[1]//2) for point in record[0]} & chamber_tiles
                    outside += 1
    return dict(chambers=9, endpoint_disjoint_sources=sources, confined=checked, outside_tile_separated=outside)


def batch_controls():
    checked = 0
    for width, amount, top, offset in itertools.product(
            (10, 14, 20, 40), (2, 3, 6, 12), (2, 40), ((0, 0), (-100, -200))):
        rows = [top+12*index for index in range(amount)]
        old = [shift(record, offset) for record in retained(width, rows, 20)]
        selected, debits, repairs = [], [], []
        for index, row in enumerate(rows[:-1]):
            selected.append(shift(make_source('R', 6, 4, 4), (row+offset[0], offset[1])))
            debits.append(shift(negative_source(), (row+offset[0], offset[1])))
            breadth, near, far, record = options(width)[index % len(options(width))]
            repairs.append(shift(record, (row+offset[0], offset[1])))
        base_phi = phi_from(old+selected, inventory(old+selected))
        negative_phi = phi_from(old+selected+debits, inventory(old+selected+debits))
        final_records = old+selected+debits+repairs
        after = inventory(final_records)
        assert base_phi == amount-1 and negative_phi == 0
        assert phi_from(final_records, after) == 2*(amount-1)
        assert len({signature(record) for record in final_records}) == len(final_records)
        checked += 1
    return checked


def isometry_controls():
    checked = 0
    fixed = branch(20, 2, 20)
    repair = shift(repaired_source(10, 8, 4), (2, 0))
    for transpose, flip_row, flip_column in itertools.product((False, True), repeat=3):
        def move(point):
            row = 1-point[0] if flip_row else point[0]
            column = 1-point[1] if flip_column else point[1]
            return (column, row) if transpose else (row, column)
        records = [transform(record, move) for record in fixed+[repair]]
        assert phi_from(records[:4], inventory(records[:4])) == 1
        assert phi_from(records[:5], inventory(records[:5])) == 0
        assert phi_from(records, inventory(records)) == 2
        checked += 1
    return checked


def whole_inventory_partition_controls():
    generator = random.Random(20261022)
    library = [independent_source(size, symmetry, (0, 0))
               for size, symmetry in itertools.product(((6, 4, 4), (8, 6, 4), (6, 4, 8)),
                   itertools.product((False, True), repeat=3))]
    library += [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    checked = total_sources = exterior_sources = 0
    for width, gaps, top in itertools.product((10, 20), ((12, 12), (12, 20, 14)), (2, 40)):
        rows = [top]
        for gap in gaps:
            rows.append(rows[-1]+gap)
        old = retained(width, rows, 20)
        before = inventory(old)
        for trial in range(16):
            blocked = set.union(*(record[0] for record in old))
            new, groups = [], [[] for gap in gaps]+[[]]
            for attempt in range(160):
                record = shift(generator.choice(library),
                               (generator.randrange(top-12, rows[-1]+12),
                                generator.randrange(-14, width+15)))
                if record[0] & blocked:
                    continue
                blocked |= record[0]
                group = len(gaps)
                for index in range(len(gaps)):
                    chamber = lambda point: rows[index]+2 <= point[0] < rows[index+1] and 1 <= point[1] <= width
                    if any(chamber(point) for point in record[0]):
                        assert all(chamber(point) for point in record[0])
                        group = index
                        break
                groups[group].append(len(new))
                new.append(record)
            assert new
            after = inventory(old+new)
            full_partition, event_partition = set(), set()
            total_marginal = 0
            for group in groups:
                isolated_records = old+[new[index] for index in group]
                isolated = inventory(isolated_records)
                full = isolated['full']-before['full']
                events = {(owner if owner < len(old) else len(old)+group[owner-len(old)], point, target)
                          for owner, point, target in isolated['events']-before['events']}
                assert not full_partition & full and not event_partition & events
                full_partition |= full
                event_partition |= events
                total_marginal += phi_from(isolated_records, isolated)-phi_from(old, before)
            assert after['full']-before['full'] == full_partition
            assert after['events']-before['events'] == event_partition
            assert phi_from(old+new, after) == -len(gaps)+total_marginal
            total_sources += len(new)
            exterior_sources += len(groups[-1])
            checked += 1
    return dict(batches=checked, new_sources=total_sources, exterior_sources=exterior_sources)


def large_controls():
    checked = 0
    fixed = branch(2000, 2000, 2000)
    before = inventory(fixed)
    for breadth, near, far in ((6, 1998, 1990), (8, 1998, 4), (10, 1998, 1996), (10, 8, 4)):
        record = shift(repaired_source(breadth, near, far), (2000, 0))
        after = inventory(fixed+[record])
        assert charge(record) == -1
        assert len(after['full']-before['full']) == 3 and len(after['events']-before['events']) == 5
        assert phi_from(fixed+[record], after) == 2
        checked += 1
    return checked


if __name__ == '__main__':
    print(json.dumps(dict(status='PASS', roles=role_controls(), exact_repair_receipts=receipt_controls(),
        localization=localization_controls(), simultaneous_batches=batch_controls(),
        tile_preserving_isometries=isometry_controls(),
        whole_inventory_partitions=whole_inventory_partition_controls(), large_2000=large_controls(),
        scope='Finite full-original controls supplement the written connected-source barrier '
              'localization and specified negative-branch actual repair. No arbitrary '
              'unselected-source bound, complete existence or global target.'), indent=2))
