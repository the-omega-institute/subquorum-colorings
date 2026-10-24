"""Compare the discovery vertex-cover encoding with independent incidence matchings."""

import argparse
import itertools
import json
from pathlib import Path

import z3

from check_owned_corner_extensions import separated
from check_remote_deficit_obstruction import fixture as remote_fixture
from check_residual_corridors import transformed
from check_sealed_strip_allocation import ring_case
from check_strip_incidence_allocation import fixture
from check_three_rule_obstruction import fixture as old_fixture
from check_two_leg_corner_obstruction import two_leg_case
from sealed_strip_allocation import maximal_strips
from search_strip_rank_coverage import rank_cover
from strip_incidence_allocation import maximum_run_allocation


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check(current):
    rows, columns, chosen, matching = current
    points = list(itertools.product(range(rows), range(columns)))
    actual_endpoints = {point for edge in matching for point in edge}
    selected = {point: z3.BoolVal(point in chosen) for point in points}
    endpoints = {point: z3.BoolVal(point in actual_endpoints) for point in points}
    solver = z3.Optimize()
    solver.set(timeout=10000)
    cover = rank_cover(solver, selected, endpoints, rows, columns)
    records, _, residual = maximal_strips(current)
    allocation = maximum_run_allocation(records, residual)
    rank = allocation['rank']
    objective = solver.minimize(cover)
    assert solver.check() == z3.sat
    assert objective.lower().as_long() == rank
    assert objective.upper().as_long() == rank
    excess = sum(max(0, len(component['slots'])-len(component['vertices']))
                 for component in allocation['components'])
    assert sum(residual.values())-rank == excess
    return dict(rank=rank, capacity=sum(residual.values()), unallocated_excess=excess)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    abstract_cases = 0
    tiles = list(itertools.product(range(2), range(3)))
    for capacities in itertools.product(range(3), repeat=len(tiles)):
        chosen = set()
        for (row, column), capacity in zip(tiles, capacities):
            chosen.update((2*row, 2*column+offset) for offset in range(2-capacity))
        check((4, 6, chosen, []))
        abstract_cases += 1
    sources = [('new32', fixture()[0]), ('remote28', remote_fixture()[0]),
               ('old22', old_fixture()[0]), ('two_leg', two_leg_case(6, 4, 6)[0]),
               ('ring3', ring_case(3)), ('ring6', ring_case(6))]
    physical = []
    for name, current in sources:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, chosen, matching = transformed(*current, *symmetry)
            physical.append(dict(name=name, symmetry=symmetry,
                                 **check((*shape, chosen, matching))))
    mixed = [dict(components=amount,
                  **check(separated([current for _, current in sources[:amount]])))
             for amount in (2, 3, 4)]
    report = dict(status='PASS', z3_version=z3.get_version_string(),
                  abstract_capacity_patterns=abstract_cases, physical_cases=len(physical),
                  mixed=mixed, physical=physical,
                  scope='For every fixed input the SMT cover attains the independently '
                        'computed incidence matching rank and cannot be smaller. Abstract '
                        'patterns test capacity algebra, not grid feasibility. Physical '
                        'fixtures include isolated runs, parallel slots and separated '
                        'components. The unused-capacity identity is also checked. '
                        'These controls do not prove geometric rank coverage or completeness '
                        'of the full frozen-receiver search encoding.')
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'physical'}))


if __name__ == '__main__':
    main()
