"""Finite discovery of complete exterior budgets with immutable source records."""

import argparse
from collections import defaultdict
import itertools
import json
import time

import z3

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_gap_axial_compensation import baseline, make_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory
from check_six_row_rotor_exclusion import normalized
from check_spanning_chamber_global_caps import verify_whole


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def placements(rows, columns, fixed, chambers):
    blocked = set.union(*(record[0] for record in fixed))
    dimensions = range(4, max(rows, columns), 2)
    shapes = set()
    for breadth, near, far in itertools.product(range(6, max(rows, columns), 2),
                                               dimensions, dimensions):
        for symmetry in itertools.product((False, True), repeat=3):
            record = independent_source((breadth, near, far), symmetry, (0, 0))
            lower_row = min(row for row, column in record[0])
            lower_column = min(column for row, column in record[0])
            record = shift(record, (-lower_row, -lower_column))
            shapes.add((tuple(sorted(record[0])), tuple(sorted(record[1])),
                        tuple(sorted(record[2]))))
    for reflected in (False, True):
        record = normalized(reflected)
        shapes.add(tuple(tuple(sorted(part)) for part in record))
    for shape in sorted(shapes):
        record = tuple(set(part) for part in shape)
        occupied = record[0] | record[1]
        min_row = min(row for row, column in occupied)
        max_row = max(row for row, column in occupied)
        min_column = min(column for row, column in occupied)
        max_column = max(column for row, column in occupied)
        for row in range(-min_row, rows-max_row):
            for column in range(-min_column, columns-max_column):
                moved = shift(record, (row, column))
                if moved[0] & (blocked | chambers):
                    continue
                yield moved


def count(conditions):
    return z3.Sum([z3.If(condition, 1, 0) for condition in conditions])


def search(rows, columns, width, gaps, upper, timeout, row_shift, column_shift):
    started = time.monotonic()
    bar_rows = tuple(2+10*index for index in range(gaps+1))
    old = baseline(width, bar_rows, 6)
    old[0] = independent_source((width+2, bar_rows[-1]+10, bar_rows[-1]+10),
                                (False, False, False), (0, -1))
    fixed = old+[shift(make_source('U', width, 4, 4), (row, 0))
                 for row in bar_rows[:-1]]
    fixed = [shift(record, (row_shift, column_shift)) for record in fixed]
    chambers = {(row+row_shift, column+column_shift) for top in bar_rows[:-1]
                for row in range(top+2, top+10) for column in range(1, width+1)}
    points = set(itertools.product(range(rows), range(columns)))
    assert all(record[0] | record[1] <= points for record in fixed)
    candidates = list(placements(rows, columns, fixed, chambers))
    records = fixed+candidates
    selected = [z3.BoolVal(True) for record in fixed]
    selected += [z3.Bool('exterior_%d' % index) for index in range(len(candidates))]
    endpoint_cover = defaultdict(list)
    occupied_cover = defaultdict(list)
    tile_cover = defaultdict(list)
    for choice, record in zip(selected, records):
        for point in record[0]:
            endpoint_cover[point].append(choice)
        for point in record[0] | record[1]:
            occupied_cover[point].append(choice)
        tiles = {(row//2, column//2) for row, column in record[0]}
        for tile in tiles:
            cells = {(2*tile[0]+row, 2*tile[1]+column)
                     for row, column in itertools.product(range(2), repeat=2)}
            if cells <= record[0]:
                tile_cover[tile].append(choice)
    endpoint = {point: z3.Bool('endpoint_%d_%d' % point) for point in points}
    occupied = {point: z3.Bool('occupied_%d_%d' % point) for point in points}
    solver = z3.Solver()
    solver.set(timeout=1000*timeout)
    for point in points:
        solver.add(endpoint[point] == z3.Or(endpoint_cover[point]))
        solver.add(occupied[point] == z3.Or(occupied_cover[point]))
        if endpoint_cover[point]:
            solver.add(z3.AtMost(*endpoint_cover[point], 1))
        solver.add(z3.Implies(z3.And(occupied[point], z3.Not(endpoint[point])),
                             count(occupied[other] for other in neighbors(point)
                                   if other in points) <= 1))
    mixed = []
    for row, column in itertools.product(range(rows//2), range(columns//2)):
        cells = [(2*row+local_row, 2*column+local_column)
                 for local_row, local_column in itertools.product(range(2), repeat=2)]
        mixed.append(z3.And(*[endpoint[point] for point in cells],
                            z3.Not(z3.Or(tile_cover[row, column]))))
    events = []
    for choice, record in zip(selected, records):
        for point in record[0]:
            for target in set(neighbors(point))-record[0]-record[1]:
                if target in points and (point[0]//2, point[1]//2) == (target[0]//2, target[1]//2):
                    events.append(z3.And(choice, endpoint[target]))
    mass = z3.Sum([z3.If(choice, max(0, -charge(record))+int(charge(record) > 0), 0)
                   for choice, record in zip(selected, records)])
    potential = mass+2*count(mixed)-count(events)
    base_value = phi_from(fixed, inventory(fixed))
    known_cap = shift(make_source('U', width, 4, 4),
                      (bar_rows[-1]+row_shift, column_shift))
    assert known_cap in candidates
    known_cap_index = candidates.index(known_cap)
    known_value = verify_whole(fixed+[known_cap])
    assert known_value-base_value == 5
    solver.push()
    solver.add(*[choice == (index == known_cap_index)
                 for index, choice in enumerate(selected[len(fixed):])])
    assert solver.check() == z3.sat
    assert solver.model().eval(potential).as_long() == known_value
    solver.pop()
    solver.add(potential-base_value < upper)
    print(json.dumps(dict(phase='solving', candidates=len(candidates),
                          construction_seconds=round(time.monotonic()-started, 3))), flush=True)
    status = solver.check()
    result = dict(status=str(status), rows=rows, columns=columns, width=width,
                  gaps=gaps, offset=[row_shift, column_shift],
                  strict_exterior_upper_bound=upper,
                  known_complete_cap='SAT_exact_marginal5',
                  candidates=len(candidates), fixed_Phi=base_value,
                  timeout_seconds=timeout, z3_version=z3.get_version_string(),
                  scope='Finite discovery with every contained legal full-even-U and standard-rotor '
                  'record, arbitrary isometries/phases. All immutable supports fit the window. '
                  'Sealed chambers fixed to spanning U; new sources exterior only. '
                  'UNSAT applies only to this window and fixed family, UNKNOWN excludes nothing.')
    if status == z3.sat:
        model = solver.model()
        chosen = [record for choice, record in zip(selected, records)
                  if z3.is_true(model.eval(choice))]
        value = verify_whole(chosen)
        assert value == model.eval(potential).as_long()
        assert value-base_value < upper
        result.update(Phi=value, exterior_marginal=value-base_value,
                      records=[dict(endpoints=sorted(record[0]), supports=sorted(record[1]),
                                    matching=sorted(record[2]), charge=charge(record))
                               for record in chosen])
    elif status == z3.unknown:
        result['reason_unknown'] = solver.reason_unknown()
    result['seconds'] = round(time.monotonic()-started, 3)
    print(json.dumps(result, indent=2), flush=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=18)
    parser.add_argument('--columns', type=int, default=12)
    parser.add_argument('--width', type=int, default=6)
    parser.add_argument('--gaps', type=int, default=0)
    parser.add_argument('--upper', type=int, default=5)
    parser.add_argument('--timeout', type=int, default=40)
    parser.add_argument('--row-shift', type=int, default=2)
    parser.add_argument('--column-shift', type=int, default=2)
    arguments = parser.parse_args()
    assert arguments.rows % 2 == arguments.columns % 2 == arguments.width % 2 == 0
    search(arguments.rows, arguments.columns, arguments.width, arguments.gaps,
           arguments.upper, arguments.timeout, arguments.row_shift, arguments.column_shift)


if __name__ == '__main__':
    main()
