import argparse
import itertools
import json
import time
from collections import defaultdict
from pathlib import Path

import z3
from check_demand_hull_reserve_obstruction import independent_source
from check_cooperative_promotion import neighbors
from rotor_networks import rotor, transform_module


def source_record(specification):
    parameters, symmetry, offset = specification
    if parameters != 'rotor':
        return independent_source(parameters, symmetry, offset)
    module = transform_module(rotor(), symmetry, offset)
    return (module['endpoints'], module['selected'],
            {tuple(sorted(edge)) for edge in module['matching']})


def verify_completion(specifications):
    records = [source_record(specification) for specification in specifications]
    endpoints = set().union(*(record[0] for record in records))
    assert len(endpoints) == sum(len(record[0]) for record in records)
    matching = set().union(*(record[2] for record in records))
    assert len(matching) == sum(len(record[2]) for record in records)
    assert len(endpoints) == 2*len(matching)
    assert {point for edge in matching for point in edge} == endpoints
    assert all(second in neighbors(first) for first, second in matching)
    supports = set().union(*(record[1] for record in records))-endpoints
    occupied = endpoints | supports
    assert all(len(set(neighbors(point)) & occupied) == 1 for point in supports)
    assert all(len(set(neighbors(point)) & occupied) >= 3 for point in endpoints)
    return dict(status='PASS', sources=len(records), endpoints=len(endpoints),
                matching_edges=len(matching), selected=len(supports),
                retained_unconsumed_supports=True, original_matchings_unchanged=True,
                selected_degree_one=True, endpoint_degree_at_least_three=True)

started = time.monotonic()
parser = argparse.ArgumentParser()
parser.add_argument('cross_width', type=int, nargs='?', default=10)
parser.add_argument('upper_row', type=int, nargs='?', default=18)
parser.add_argument('--companion', choices=['H', 'E', 'S', 'S6'], default='H')
parser.add_argument('--maximum-width', type=int, default=12)
parser.add_argument('--maximum-leg', type=int, default=8)
parser.add_argument('--maximum-additions', type=int, default=10)
parser.add_argument('--seed-json')
parser.add_argument('--include-rotors', action='store_true')
parser.add_argument('--lower-row', type=int, default=-6)
parser.add_argument('--lower-column', type=int, default=-6)
parser.add_argument('--upper-column', type=int, default=22)
parser.add_argument('--timeout-seconds', type=int, default=90)
arguments = parser.parse_args()
if arguments.companion == 'H':
    specifications = [((12, 4, 4), (False, False, False), (0, 0)),
                      ((6, 6, 4), (False, True, False), (9, 1)),
                      ((arguments.cross_width, 8, 4), (True, True, False), (1, 10)),
                      ((6, 4, 4), (False, False, False), (3, 2))]
elif arguments.companion == 'S6':
    specifications = [((10, 4, 4), (False, False, False), (0, 0)),
                      ((10, 8, 4), (False, True, False), (11, 1)),
                      ((arguments.cross_width, 6, 4), (True, True, False), (1, 8)),
                      ((8, 6, 4), (False, True, False), (9, 2))]
else:
    companion_frame = ((True, True, False), (2, 7)) if arguments.companion == 'E' else (
        (False, True, False), (7, 2))
    specifications = [((14, 4, 4), (False, False, False), (0, 0)),
                      ((8, 8, 4), (False, True, False), (11, 1)),
                      ((arguments.cross_width, 10, 4), (True, True, False), (1, 12)),
                      ((6, 4, 4), *companion_frame)]
if arguments.seed_json:
    specifications = json.loads(Path(arguments.seed_json).read_text())['specifications']
seed = [source_record(specification) for specification in specifications]
fixed = set().union(*(record[0] for record in seed))
assert len(fixed) == sum(len(record[0]) for record in seed)
lower = (arguments.lower_row, arguments.lower_column)
upper = (arguments.upper_row, arguments.upper_column)
assert all(lower[axis] <= point[axis] <= upper[axis]
           for record in seed for point in record[0] | record[1] for axis in (0, 1))
library = []
seen = set()
parameters = list(itertools.product(range(6, arguments.maximum_width+1, 2),
                                   range(4, arguments.maximum_leg+1, 2),
                                   range(4, arguments.maximum_leg+1, 2)))
if arguments.include_rotors:
    parameters.append('rotor')
for dimensions in parameters:
    for symmetry in itertools.product((False, True), repeat=3):
        endpoints, supports, matching = source_record((dimensions, symmetry, (0, 0)))
        occupied = endpoints | supports
        minimum = tuple(min(point[axis] for point in occupied) for axis in (0, 1))
        maximum = tuple(max(point[axis] for point in occupied) for axis in (0, 1))
        for row in range(lower[0]-minimum[0], upper[0]-maximum[0]+1):
            for column in range(lower[1]-minimum[1], upper[1]-maximum[1]+1):
                shifted = {(first+row, second+column) for first, second in endpoints}
                if shifted & fixed:
                    continue
                selections = {(first+row, second+column) for first, second in supports}
                key = frozenset(shifted), frozenset(selections)
                if key in seen:
                    continue
                seen.add(key)
                library.append(((dimensions, symmetry, (row, column)), shifted, selections))
print('candidates', len(library), 'generation_seconds', round(time.monotonic()-started, 2), flush=True)
chosen = [z3.Bool('chosen_%d' % index) for index in range(len(library))]
endpoint_cover = defaultdict(list)
occupied_cover = defaultdict(list)
fixed_occupied = set().union(*(record[0] | record[1] for record in seed))
points = set(itertools.product(range(lower[0], upper[0]+1), range(lower[1], upper[1]+1)))
for index, (_, endpoints, supports) in enumerate(library):
    for point in endpoints:
        endpoint_cover[point].append(chosen[index])
    for point in endpoints | supports:
        occupied_cover[point].append(chosen[index])
endpoint = {point: z3.Or(point in fixed, *endpoint_cover[point]) for point in points}
occupied = {point: z3.Or(point in fixed_occupied, *occupied_cover[point]) for point in points}
solver = z3.Solver()
solver.set(timeout=1000*arguments.timeout_seconds)
solver.add(z3.PbLe([(choice, 1) for choice in chosen], arguments.maximum_additions))
for point in points:
    if endpoint_cover[point]:
        solver.add(z3.AtMost(*endpoint_cover[point], 1))
    solver.add(z3.Implies(z3.And(occupied[point], z3.Not(endpoint[point])),
                          z3.PbLe([(occupied[other], 1) for other in neighbors(point) if other in points], 1)))
print('solving', round(time.monotonic()-started, 2), flush=True)
status = solver.check()
result = dict(status=str(status), candidates=len(library), seconds=round(time.monotonic()-started, 2),
              lower=lower, upper=upper, maximum_width=arguments.maximum_width,
              maximum_leg=arguments.maximum_leg, maximum_additions=arguments.maximum_additions,
              seed_json=arguments.seed_json,
              include_rotors=arguments.include_rotors,
              source='Finite bounded discovery; UNSAT excludes this candidate library only, not arbitrary U/rotor extensions.')
if status == z3.sat:
    model = solver.model()
    selected = [specification for choice, (specification, _, _) in zip(chosen, library)
                if z3.is_true(model.eval(choice))]
    result['specifications'] = specifications+selected
    result['independent_direct_verification'] = verify_completion(result['specifications'])
print(json.dumps(result), flush=True)
