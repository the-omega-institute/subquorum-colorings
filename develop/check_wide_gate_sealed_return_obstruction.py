"""Full-source controls for all-width nonextension of the nested even-U seed."""

import itertools
import json

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import anchor_records, rotor_record
from check_incident_eight_north_transfer import shift
from check_wide_gate_escape_compensation import escape, retained, signature
from check_wide_gate_rotor_compensation import mirror


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def libraries():
    dimensions = itertools.product((6, 8, 14, 30), (4, 6, 12, 40), (4, 6, 12, 40))
    U_records = [independent_source(size, symmetry, (0, 0))
                 for size, symmetry in itertools.product(dimensions,
                     itertools.product((False, True), repeat=3))]
    rotor_records = [rotor_record(symmetry) for symmetry in itertools.product((False, True), repeat=3)]
    return U_records, rotor_records


def normalized_base(width, depth, far):
    return [shift(record, (-2, 0)) for record in retained(width, 2, 2)]+[escape(depth, far, 0)]


def short_U(breadth, side, north):
    return independent_source((breadth, 4, 4), (False, north, True),
                              (7 if north else 3, side+1))


def terminal_rotors(point, free, rotor_records):
    return {signature(record): record for original in rotor_records
            for record in anchor_records(original, point, free)}


def exclude_gate(records, gate, free, U_records, rotor_records):
    occupied = set.union(*(record[0] for record in records))
    assert len(occupied) == sum(len(record[0]) for record in records)
    assert gate not in occupied and any(gate in record[1] for record in records)
    own_directions = {(row-gate[0], column-gate[1])
                      for row, column in set(neighbors(gate)) & occupied}
    assert own_directions.isdisjoint(free) and len(own_directions) >= 2
    U_roles = rotor_roles = 0
    for original in U_records:
        for record in anchor_records(original, gate, free):
            assert record[0] & occupied
            U_roles += 1
    for original in rotor_records:
        for record in anchor_records(original, gate, free):
            assert record[0] & occupied
            rotor_roles += 1
    return U_roles, rotor_roles


def check_case(width, depth, far, U_records, rotor_records, moved=False):
    assert 4 <= far <= depth-4 and depth <= width-10
    base = normalized_base(width, depth, far)
    occupied = set.union(*(record[0] for record in base))
    assert len(occupied) == sum(len(record[0]) for record in base)
    side = depth+1-far
    point = (7, side)
    assert point in base[-1][1] and point not in occupied
    assert set(neighbors(point)) & occupied == {(7, side+1), (8, side)}
    actual_U = {}
    for original in U_records:
        for record in anchor_records(original, point, {(-1, 0), (0, -1)}):
            if not record[0] & occupied:
                actual_U[signature(record)] = record
    expected_U = {signature(short_U(breadth, side, north))
                  for breadth in (6, 8, 14, 30) for north in (False, True)
                  if breadth <= side-5}
    assert set(actual_U) == expected_U
    actual_rotors = {key: record for key, record in terminal_rotors(
        point, {(-1, 0), (0, -1)}, rotor_records).items() if not record[0] & occupied}
    north_only = terminal_rotors(point, {(-1, 0)}, rotor_records)
    expected_rotors = {key for key, record in north_only.items()
                       if side >= 7 or min(column for row, column in record[0]) == side-1}
    assert set(actual_rotors) == expected_rotors
    U_roles = rotor_roles = gate_count = 0
    for record in actual_rotors.values():
        column = next(column for row, column in record[0] if row == 4)
        gate = (3, column)
        counts = exclude_gate(base+[record], gate, {(0, -1), (0, 1)}, U_records, rotor_records)
        U_roles += counts[0]
        rotor_roles += counts[1]
        gate_count += 1
    all_short = [short_U(breadth, side, north)
                 for breadth in range(6, side-4, 2) for north in (False, True)]
    for record in all_short:
        gate = (3, side+1)
        counts = exclude_gate(base+[record], gate, {(0, 1), (1, 0)}, U_records, rotor_records)
        U_roles += counts[0]
        rotor_roles += counts[1]
        gate_count += 1
    if moved:
        candidates = list(actual_rotors.values())+all_short
        for record in candidates:
            gate = ((3, next(column for row, column in record[0] if row == 4))
                    if min(row for row, column in record[0]) == 4 else (3, side+1))
            free = {(0, -1), (0, 1)} if min(row for row, column in record[0]) == 4 else {(0, 1), (1, 0)}
            records = [shift(mirror(original, width), (-100, -200)) for original in base+[record]]
            moved_gate = gate[0]-100, width+1-gate[1]-200
            moved_free = {(row, -column) for row, column in free}
            exclude_gate(records, moved_gate, moved_free, U_records, rotor_records)
    return dict(normalized_U=len(actual_U), normalized_rotors=len(actual_rotors),
                full_short_U_shapes=len(all_short), sealed_gates=gate_count,
                excluded_U_roles=U_roles, excluded_rotor_roles=rotor_roles)


def run():
    U_records, rotor_records = libraries()
    totals = dict(cases=0, normalized_U=0, normalized_rotors=0, full_short_U_shapes=0,
                  sealed_gates=0, excluded_U_roles=0, excluded_rotor_roles=0)
    for depth, far in itertools.product((8, 10, 14, 20, 30, 40), (4, 6, 10, 20, 30)):
        if far > depth-4:
            continue
        result = check_case(depth+30, depth, far, U_records, rotor_records, moved=True)
        totals['cases'] += 1
        for key, value in result.items():
            totals[key] += value
    large = []
    for width, depth, far in ((200, 100, 40), (2000, 1000, 900)):
        result = check_case(width, depth, far, U_records, rotor_records)
        large.append(dict(width=width, near=depth, far=far, **result))
    return dict(status='PASS', controls=totals, large_controls=large,
                scope='General written all-width three-original nonextension; finite '
                      'role controls validate the exhaustive source-to-gate argument. '
                      'Does not exclude arbitrary multicyclic contact components or '
                      'prove a global grid inequality. No complete-family existence claimed.')


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
