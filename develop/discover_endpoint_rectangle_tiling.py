"""Exact endpoint-cover discovery; feasibility requires a separate frame proof."""

import argparse
from collections import defaultdict
import itertools
import json
from pathlib import Path
import time

import z3

from check_minus_one_tip_obstructions import source
from rotor_networks import affine, rotor


def endpoint_library(rows, columns):
    seen = set()
    limit = max(rows, columns)
    sources = [(dict(kind='rotor'), rotor())]
    sources.extend((dict(kind='U', parameters=[width, left, right]),
                    source(width, left, right))
                   for width in range(6, limit+1, 2)
                   for left in range(4, limit, 2)
                   for right in range(4, limit, 2))
    for specification, module in sources:
        for symmetry in itertools.product((False, True), repeat=3):
            body = {affine(point, symmetry) for point in module['endpoints']}
            first_row = min(row for row, _ in body)
            first_column = min(column for _, column in body)
            height = max(row for row, _ in body)-first_row+1
            width = max(column for _, column in body)-first_column+1
            if height > rows or width > columns:
                continue
            for row in range(rows-height+1):
                for column in range(columns-width+1):
                    offset = row-first_row, column-first_column
                    endpoints = frozenset((point[0]+offset[0], point[1]+offset[1])
                                          for point in body)
                    if endpoints in seen:
                        continue
                    seen.add(endpoints)
                    yield dict(**specification, symmetry=list(symmetry), offset=list(offset)), endpoints


def search(rows, columns, timeout):
    started = time.monotonic()
    library = list(endpoint_library(rows, columns))
    selected = [z3.Bool('endpoint_tile_%d' % index) for index in range(len(library))]
    cover = defaultdict(list)
    for choice, (_, body) in zip(selected, library):
        for point in body:
            cover[point].append(choice)
    solver = z3.Solver()
    solver.set(timeout=1000*timeout)
    for point in itertools.product(range(rows), range(columns)):
        solver.add(z3.PbEq([(choice, 1) for choice in cover[point]], 1)
                   if cover[point] else z3.BoolVal(False))
    status = solver.check()
    report = dict(status=str(status), rows=rows, columns=columns,
                  timeout_seconds=timeout, candidates=len(library),
                  z3_version=z3.get_version_string(),
                  seconds=round(time.monotonic()-started, 3),
                  scope='Exact endpoint cover only. SAT requires independent original-matching and complete-support frame verification before any compensation claim. UNSAT excludes only this finite rectangle; UNKNOWN excludes nothing.')
    if status == z3.sat:
        model = solver.model()
        chosen = [(specification, body) for choice, (specification, body) in zip(selected, library)
                  if z3.is_true(model.eval(choice))]
        assert set.union(*(set(body) for _, body in chosen)) == set(
            itertools.product(range(rows), range(columns)))
        assert sum(len(body) for _, body in chosen) == rows*columns
        report['tiles'] = [specification for specification, _ in chosen]
    if status == z3.unknown:
        report['reason_unknown'] = solver.reason_unknown()
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, required=True)
    parser.add_argument('--columns', type=int, required=True)
    parser.add_argument('--timeout', type=int, default=30)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    result = search(arguments.rows, arguments.columns, arguments.timeout)
    arguments.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
