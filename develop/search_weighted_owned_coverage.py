"""Discover frozen receivers not covered by distinct capped and guarded donors."""

import argparse
import itertools
import json
from pathlib import Path
import time

import z3

from check_component_receivers import vertices_of
from check_cooperative_promotion import neighbors
from check_owned_donors import endpoint_data
from owned_corner_witnesses import physical_donors
from search_corner_coverage import corner_patterns
from search_frozen_receiver_ceiling import count, encoding, verify


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def symbolic_donors(rows, columns, selected, endpoints):
    domain = set(selected)
    capacities = []
    donated = {}
    for tile in itertools.product(range(rows//2), range(columns//2)):
        cells = vertices_of({tile})
        top, left = (2*coordinate for coordinate in tile)
        patterns = []
        for required, support, excluded in corner_patterns(top, left):
            if not (set(required) | {support} | set(excluded)) <= domain:
                continue
            patterns.append(z3.And([endpoints[point] for point in required]+
                                   [selected[support]]+
                                   [z3.Not(endpoints[point]) for point in excluded]))
        for chosen in sorted(cells):
            anchors = (set(neighbors(chosen))-cells) & domain
            opposite = tuple(4*coordinate+1-value for coordinate, value in zip(tile, chosen))
            guards = (set(neighbors(opposite))-cells) & domain
            for guard in sorted(guards):
                supports = (set(neighbors(guard))-{opposite}) & domain
                patterns.append(z3.And(selected[chosen],
                    z3.Or([endpoints[point] for point in sorted(anchors)]), selected[guard],
                    z3.Or([endpoints[point] for point in sorted(supports)])))
        donated[tile] = z3.Or(patterns)
        capacities.append(z3.If(donated[tile], 2-count(selected[point] for point in cells), 0))
    return donated, z3.Sum(capacities)


def fixture_from_file(path):
    source = json.loads(path.read_text())
    return (*source['shape'], {tuple(point) for point in source['selected']},
            [tuple(tuple(point) for point in edge) for edge in source['matching']])


def fixed_expression_control(current):
    rows, columns, actual_selected, _ = current
    actual_endpoints = endpoint_data(current)[0]
    domain = set(itertools.product(range(rows), range(columns)))
    selected = {point: z3.BoolVal(point in actual_selected) for point in domain}
    endpoints = {point: z3.BoolVal(point in actual_endpoints) for point in domain}
    donated, capacity = symbolic_donors(rows, columns, selected, endpoints)
    records = physical_donors(current)
    assert {tile for tile, expression in donated.items() if z3.is_true(z3.simplify(expression))} == {
        tuple(record['tile']) for record in records}
    assert z3.simplify(capacity).as_long() == sum(record['deficit'] for record in records)
    return records


def search(rows, columns, root, timeout, fixed=None):
    solver, selected, paired, matching, rank, charge = encoding(
        rows, columns, 1, timeout, root, require_frozen=True)
    donated, capacity = symbolic_donors(rows, columns, selected, paired)
    solver.add(capacity < charge)
    if fixed is not None:
        endpoints = endpoint_data(fixed)[0]
        edges = {tuple(sorted(edge)) for edge in fixed[3]}
        for point, variable in paired.items():
            solver.add(variable == (point in endpoints))
        for edge, variable in matching.items():
            solver.add(variable == (edge in edges))
    started = time.monotonic()
    status = solver.check()
    report = dict(status=str(status), shape=[rows, columns], root=root,
                  fixed_endpoints_and_matching=fixed is not None,
                  seconds=round(time.monotonic()-started, 3), timeout_seconds=timeout,
                  z3_version=z3.get_version_string(),
                  scope='Discovery in one even rectangle with one connected endpoint component '
                        'and strict acyclic freeze ranks. Both capped and guarded rules use '
                        'all orientations and actual physical tile identities. Optional fixed '
                        'endpoints and matching leave only selected labels free. '
                        'Unknown is not unsat; finite unsat is not a general coverage proof.')
    if status == z3.sat:
        model = solver.model()
        actual_selected = {point for point, variable in selected.items()
                           if z3.is_true(model.eval(variable))}
        actual_matching = [edge for edge, variable in matching.items()
                           if z3.is_true(model.eval(variable))]
        current = rows, columns, actual_selected, actual_matching
        checked = verify(current)
        donors = fixed_expression_control(current)
        actual_capacity = sum(record['deficit'] for record in donors)
        assert checked['receiver_charge'] == model.eval(charge).as_long()
        assert actual_capacity == model.eval(capacity).as_long() < checked['receiver_charge']
        report.update(selected=sorted(actual_selected), matching=actual_matching,
                      donors=donors, owned_capacity=actual_capacity,
                      checked=checked,
                      ranks=[dict(point=point, rank=model.eval(rank[point]).as_long())
                             for point in sorted(endpoint_data(current)[0])])
    elif status == z3.unknown:
        report['reason_unknown'] = solver.reason_unknown()
    return report


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, default=10)
    parser.add_argument('--columns', type=int, default=10)
    parser.add_argument('--root', type=int, nargs=2, default=(2, 2))
    parser.add_argument('--fixed-fixture', type=Path)
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    fixed = fixture_from_file(arguments.fixed_fixture) if arguments.fixed_fixture else None
    rows, columns = fixed[:2] if fixed else (arguments.rows, arguments.columns)
    root = min(endpoint_data(fixed)[0]) if fixed else tuple(arguments.root)
    report = search(rows, columns, root, arguments.timeout, fixed)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items()
                      if key not in {'selected', 'matching', 'ranks', 'checked'}}))
    if 'checked' in report:
        print(json.dumps({key: value for key, value in report['checked'].items()
                          if key != 'freezing_layers'}))


if __name__ == '__main__':
    main()
