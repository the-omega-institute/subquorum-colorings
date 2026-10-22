"""Finite discovery for the whole six-row pocket behind a spanning upward U."""

import argparse
import itertools
import json
import time

import z3

from check_cooperative_promotion import neighbors
from check_demand_hull_reserve_obstruction import independent_source
from check_even_bar_contact_ledger import rotor_record
from check_even_gap_axial_compensation import baseline, make_source
from check_incident_eight_north_transfer import charge, shift
from check_secondary_ten_internal_consumer_chains import phi_from
from check_secondary_ten_north_contact_debit import inventory


if not __debug__:
    raise RuntimeError('Run without -O: discovery uses assertions.')


def source_library(height, width):
    library = {}
    maximum = max(height, width)
    sizes = itertools.product(range(6, maximum+1, 2),
                              range(4, maximum+1, 2), range(4, maximum+1, 2))
    originals = [(independent_source(size, symmetry, (0, 0)),
                  dict(kind='U', dimensions=size, symmetry=symmetry))
                 for size, symmetry in itertools.product(
                     sizes, itertools.product((False, True), repeat=3))]
    originals += [(rotor_record(symmetry), dict(kind='rotor', symmetry=symmetry))
                  for symmetry in itertools.product((False, True), repeat=3)]
    for source, specification in originals:
        minimum_row = min(point[0] for point in source[0])
        maximum_row = max(point[0] for point in source[0])
        minimum_column = min(point[1] for point in source[0])
        maximum_column = max(point[1] for point in source[0])
        if maximum_row-minimum_row >= height or maximum_column-minimum_column >= width:
            continue
        for row, column in itertools.product(range(-minimum_row, height-maximum_row),
                                              range(-minimum_column, width-maximum_column)):
            record = shift(source, (row, column))
            key = tuple(map(frozenset, record))
            library[key] = record, dict(specification, offset=(row, column))
    return list(library.values())


def sum_truth(conditions):
    return z3.Sum([z3.If(condition, 1, 0) for condition in conditions])


def search(width, timeout, threshold, exclude_spanning):
    started = time.monotonic()
    fixed = baseline(width, (2, 12), 20)+[
        shift(make_source('U', width, 4, 4), (2, 0))]
    fixed_endpoints = set.union(*(record[0] for record in fixed))
    fixed_occupied = set.union(*(record[0] | record[1] for record in fixed))
    library = [(shift(record, (4, 2)), specification)
               for record, specification in source_library(6, width-2)]
    choices = [z3.Bool('pocket_source_'+str(index)) for index in range(len(library))]
    pocket = {(row, column) for row in range(4, 10) for column in range(2, width)}
    points = pocket | {other for point in pocket for other in neighbors(point)}
    endpoint_cover = {point: [] for point in points}
    occupied_cover = {point: [] for point in points}
    for choice, (record, specification) in zip(choices, library):
        assert record[0] <= pocket and not record[0] & fixed_endpoints
        assert record[1]-pocket <= fixed_endpoints
        for point in record[0]:
            endpoint_cover[point].append(choice)
        for point in record[0] | record[1]:
            occupied_cover[point].append(choice)
    endpoint = {point: z3.Or(point in fixed_endpoints, *endpoint_cover[point]) for point in points}
    occupied = {point: z3.Or(point in fixed_occupied, *occupied_cover[point]) for point in points}
    solver = z3.Solver()
    solver.set(timeout=timeout*1000)
    for point in pocket:
        if len(endpoint_cover[point]) > 1:
            solver.add(z3.AtMost(*endpoint_cover[point], 1))
        solver.add(z3.Implies(z3.And(occupied[point], z3.Not(endpoint[point])),
                              sum_truth(occupied[other] for other in neighbors(point)) == 1))
    mixed_tiles = []
    for row, column in itertools.product(range(2, 5), range(1, width//2)):
        cells = {(2*row+vertical, 2*column+horizontal)
                 for vertical, horizontal in itertools.product(range(2), repeat=2)}
        single_covers = [choice for choice, (record, specification) in zip(choices, library)
                         if cells <= record[0]]
        mixed_tiles.append(z3.And(*[endpoint[point] for point in cells],
                                   z3.Not(z3.Or(*single_covers))))
    event_terms = []
    for choice, (record, specification) in zip(choices, library):
        for point in record[0]:
            for other in set(neighbors(point))-record[0]-record[1]:
                if other not in pocket or (point[0]//2, point[1]//2) != (other[0]//2, other[1]//2):
                    continue
                event_terms.append(z3.And(choice, endpoint[other]))
    potential = z3.Sum([z3.If(choice, max(0, -charge(record))+int(charge(record)>0), 0)
                        for choice, (record, specification) in zip(choices, library)])
    potential += 2*sum_truth(mixed_tiles)-sum_truth(event_terms)
    solver.add(z3.Or(*choices))
    if threshold is not None:
        solver.add(potential <= threshold)
    if exclude_spanning:
        for choice, (record, specification) in zip(choices, library):
            if specification['kind'] == 'U' and specification['dimensions'] == (width-2, 4, 4):
                columns = {point[1] for point in record[0]}
                rows = {point[0] for point in record[0]}
                if columns == set(range(2, width)) and len(rows) == 5:
                    solver.add(z3.Not(choice))
    verdict = solver.check()
    result = dict(width=width, candidates=len(library), status=str(verdict),
                  threshold=threshold, exclude_spanning=exclude_spanning,
                  seconds=round(time.monotonic()-started, 3), z3_version=z3.get_version_string(),
                  scope='Finite sealed-pocket discovery only; no unbounded theorem inferred.')
    if verdict == z3.sat:
        model = solver.model()
        chosen = [(record, specification) for choice, (record, specification) in zip(choices, library)
                  if z3.is_true(model.eval(choice))]
        records = fixed+[record for record, specification in chosen]
        receipt = inventory(records)
        endpoints = set.union(*(record[0] for record in records))
        support = set.union(*(record[1] for record in records))-endpoints
        actual_occupied = endpoints | support
        assert all(len(set(neighbors(point)) & actual_occupied) == 1 for point in support & pocket)
        increment = phi_from(records, receipt)-phi_from(fixed, inventory(fixed))
        assert increment == model.eval(potential).as_long()
        result.update(increment=increment, sources=[dict(specification, charge=charge(record))
                                                   for record, specification in chosen])
    elif verdict == z3.unknown:
        result['reason'] = solver.reason_unknown()
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--widths', type=int, nargs='+', default=[8, 10, 12, 14])
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--threshold', type=int)
    parser.add_argument('--exclude-spanning', action='store_true')
    arguments = parser.parse_args()
    for width in arguments.widths:
        assert width >= 6 and width % 2 == 0
        print(json.dumps(search(width, arguments.timeout, arguments.threshold,
                                arguments.exclude_spanning)), flush=True)


if __name__ == '__main__':
    main()
