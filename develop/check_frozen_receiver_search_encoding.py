"""Fixed positive and negative controls for the receiver discovery encoding."""

import argparse
import json
from pathlib import Path

import z3

from check_bent_cap_compensation import bent_cap
from check_elbow_sources import elbow
from check_frozen_rail_elbows import rail_elbow
from check_promotion_cores import degree_four_patch
from search_frozen_receiver_ceiling import encoding, verify


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def check(name, current, require_frozen, expected):
    endpoints = {point for edge in current[3] for point in edge}
    matching = {tuple(sorted(edge)) for edge in current[3]}
    checked = verify(current, require_frozen=False)
    solver, selected, paired, edges, _, charge = encoding(
        *current[:2], checked['receiver_charge'], 10, min(endpoints), require_frozen)
    for point, variable in selected.items():
        solver.add(variable == (point in current[2]))
    for point, variable in paired.items():
        solver.add(variable == (point in endpoints))
    for edge, variable in edges.items():
        solver.add(variable == (edge in matching))
    status = solver.check()
    assert str(status) == expected, (name, require_frozen, status)
    if status == z3.sat:
        assert solver.model().eval(charge).as_long() == checked['receiver_charge']
    if require_frozen:
        assert checked['fully_frozen'] == (expected == 'sat')
    return dict(name=name, require_frozen=require_frozen, status=str(status),
                charge=checked['receiver_charge'], independently_frozen=checked['fully_frozen'])


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    records = []
    for name, current in [('positive_bent', bent_cap(4)), ('positive_elbow', elbow(6, 4)),
                          ('positive_occupied_rail', rail_elbow(6, 4, [(1, 4, {0, 3})])[0])]:
        records.append(check(name, current, True, 'sat'))
    square = (6, 6, {(1, 2), (2, 4), (4, 3), (3, 1)},
              [((2, 2), (2, 3)), ((3, 2), (3, 3))])
    for name, current in [('degree_four_promotable_patch', degree_four_patch()),
                          ('degree_three_alternating_square', square)]:
        records.append(check(name, current, True, 'unsat'))
        records.append(check(name, current, False, 'sat'))
    report = dict(status='PASS', z3_version=z3.get_version_string(), controls=records,
                  scope='Fixed known physical configurations test strict-rank freezing, '
                        'connectivity and exact charge in the discovery encoding. '
                        'No unrestricted ceiling conclusion is inferred.')
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report))


if __name__ == '__main__':
    main()
