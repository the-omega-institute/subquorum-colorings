import argparse
import itertools
import json
import time
from collections import defaultdict
from pathlib import Path

import z3
from check_demand_hull_reserve_obstruction import independent_source
from check_cooperative_promotion import neighbors

started = time.monotonic()
parser = argparse.ArgumentParser()
parser.add_argument('cross_width', type=int, nargs='?', default=10)
parser.add_argument('upper_row', type=int, nargs='?', default=18)
parser.add_argument('--companion', choices=['H', 'E', 'S', 'S6'], default='H')
parser.add_argument('--maximum-width', type=int, default=12)
parser.add_argument('--maximum-leg', type=int, default=8)
parser.add_argument('--maximum-additions', type=int, default=10)
parser.add_argument('--seed-json')
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
seed = [independent_source(*specification) for specification in specifications]
fixed = set().union(*(record[0] for record in seed))
assert len(fixed) == sum(len(record[0]) for record in seed)
lower = (arguments.lower_row, arguments.lower_column)
upper = (arguments.upper_row, arguments.upper_column)
assert all(lower[axis] <= point[axis] <= upper[axis]
           for record in seed for point in record[0] | record[1] for axis in (0, 1))
library = []
seen = set()
for dimensions in itertools.product(range(6, arguments.maximum_width+1, 2),
                                    range(4, arguments.maximum_leg+1, 2),
                                    range(4, arguments.maximum_leg+1, 2)):
    for symmetry in itertools.product((False, True), repeat=3):
        endpoints, supports, matching = independent_source(dimensions, symmetry, (0, 0))
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
              source='Finite U-only discovery; UNSAT excludes this bounded library only, not arbitrary U/rotor extensions.')
if status == z3.sat:
    model = solver.model()
    selected = [specification for choice, (specification, _, _) in zip(chosen, library)
                if z3.is_true(model.eval(choice))]
    result['specifications'] = specifications+selected
print(json.dumps(result), flush=True)
