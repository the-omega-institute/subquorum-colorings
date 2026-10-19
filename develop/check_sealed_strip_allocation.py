"""Physical controls for overlapping sealed strips and reservation before allocation."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_charge_two_frozen_receiver import fixture as charge_two_fixture
from check_component_receivers import verify_terminal, vertices_of
from check_corner_free_frozen_receiver import fixture as corner_free_fixture
from check_owned_corner_extensions import separated
from check_remote_deficit_obstruction import fixture as remote_fixture
from check_residual_corridors import transformed
from check_three_rule_obstruction import fixture as three_rule_fixture
from check_two_leg_corner_obstruction import two_leg_case
from owned_corner_witnesses import physical_donors
from sealed_strip_allocation import allocate_units, sealed_strips


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def ring_case(tiles):
    assert tiles >= 3
    size = 2*tiles
    endpoints = {(row+2, column+2) for row in range(size) for column in range(size)
                 if min(row, column, size-row-1, size-column-1) < 2}
    matching = []
    for tile in itertools.product(range(1, tiles+1), repeat=2):
        cells = vertices_of({tile})
        if cells <= endpoints:
            top, left = (2*coordinate for coordinate in tile)
            matching += [((top, left+local), (top+1, left+local)) for local in (0, 1)]
    selected = {(1, 2), (1, size+1), (size+2, 2), (size+2, size+1)}
    return size+4, size+4, selected, matching


def inspect(current, reserve_old=False):
    ledger = verify_terminal(current)
    reserved = {}
    if reserve_old:
        for record in physical_donors(current, include_endpoint_guard=True):
            reserved[tuple(record['tile'])] = record['deficit']
    records, deficits, residual = sealed_strips(current, reserved)
    multiplicity = Counter(tile for record in records for tile in record['tiles'])
    assert max(multiplicity.values(), default=0) <= 2
    for tile in multiplicity:
        owners = {record['owner'] for record in records if record['owner'] is not None and tile in record['tiles']}
        assert len(owners) <= 1
    eligible, assignments = allocate_units(records, residual)
    usage = Counter(tuple(record['tile']) for record in assignments)
    assert all(amount <= residual[tile] for tile, amount in usage.items())
    assert sum(reserved.values())+len(eligible) <= ledger['empty_deficit']
    return dict(components=len(ledger['receivers']), sealed_strips=len(records),
                eligible_after_reservation=len(eligible), reserved_units=sum(reserved.values()),
                max_tile_multiplicity=max(multiplicity.values(), default=0),
                crossed_tiles=sum(amount == 2 for amount in multiplicity.values()),
                no_endpoint_deficit=ledger['empty_deficit'], allocations=len(assignments),
                charge_twice=sum(record['charge_twice'] for record in ledger['receivers']))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    sources = [('ring_%d' % size, ring_case(size)) for size in (3, 4, 6, 10)]
    sources += [('remote', remote_fixture()[0]), ('charge_two', charge_two_fixture()[0]),
                ('corner_free', corner_free_fixture()[0]), ('old22', three_rule_fixture()[0]),
                ('two_leg', two_leg_case(6, 4, 6)[0])]
    records = []
    for name, current in sources:
        for symmetry in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*current, *symmetry)
            for reserved in (False, True):
                checked = inspect((*shape, selected, matching), reserved)
                records.append(dict(name=name, symmetry=symmetry, reserve_old=reserved, **checked))
    mixed = []
    for number in (2, 3, 4):
        current = separated([source for _, source in sources[-number:]])
        for reserved in (False, True):
            checked = inspect(current, reserved)
            assert checked['components'] == number
            mixed.append(dict(reserve_old=reserved, **checked))
    singleton = ring_case(3)
    strips, deficits, residual = sealed_strips(singleton)
    owned = [record for record in strips if record['owner'] is not None]
    assert len(owned) == 2 and all(record['tiles'] == [(2, 2)] for record in owned)
    assert deficits[(2, 2)] == 2
    _, allocation = allocate_units(owned, residual)
    assert len(allocation) == 2 and {tuple(record['tile']) for record in allocation} == {(2, 2)}
    remote = remote_fixture()[0]
    remote_strips, remote_deficits, remote_residual = sealed_strips(remote)
    assert len(remote_strips) == 2 and all(record['capacity'] == 2 for record in remote_strips)
    assert sum(remote_deficits.values()) == 2
    _, remote_allocation = allocate_units(remote_strips, remote_residual)
    assert len(remote_allocation) == 2
    assert {tuple(record['tile']) for record in remote_allocation} == {(3, 2)}
    report = dict(status='PASS', physical_cases=len(records), mixed_controls=mixed,
                  single_tile_two_orientation_allocation='PASS_two_distinct_units_of_one_capacity_two_tile',
                  frozen_remote_sharpness='PASS_two_strips_each_capacity2_share_only_donor_capacity2;one_unit_each_allocated;full_two_unit_credit_per_strip_FALSE',
                  scope='Controls for general written strip capacity, multiplicity-two, Hall '
                        'allocation and reservation theorems, with actual overlapping physical '
                        'rings and mixed-component cases. Rings are single-terminal, not claimed '
                        'fully frozen. Global strip coverage is not inferred from finite checks.',
                  cases=records)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key != 'cases'}))


if __name__ == '__main__':
    main()
