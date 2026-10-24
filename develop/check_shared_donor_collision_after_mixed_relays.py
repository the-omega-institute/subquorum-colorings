"""Check two unpaid alpha components reaching the same single interval unit."""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_arbitrary_depth_cap_relays import relay_family
from check_even_bridge_support_completion import endpoints_of
from check_native_guard_compensation import force_matching
from check_one_sided_interval_allocation import grid_allocation
from check_residual_corridors import direct_check


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def collision_family(width):
    base, _, _ = relay_family(width, 4, 1, 1)
    shift = lambda point: (point[0], point[1]+10)
    current = (base[0], base[1]+10, base[2] | {shift(point) for point in base[2]},
               base[3]+[tuple(map(shift, edge)) for edge in base[3]])
    bands = [[((row, column), (row+1, column)) for column in range(22)]
             for row in range(4, width+5, 2)]
    return current, bands


def control(width, totals):
    current, bands = collision_family(width)
    direct_check(*current)
    force_matching(current, totals)
    cells = {point for band in bands for column in band for point in column}
    endpoints = endpoints_of(current)
    assert current[2] | endpoints <= cells
    assert all((2*(row//2)+offset_row, 2*(column//2)+offset_column) in cells
               for row, column in endpoints
               for offset_row, offset_column in itertools.product((0, 1), repeat=2))
    assert len(current[2]) == 34 and len(current[3]) == 2*width+16
    initial = [((5, 5), (5, 6))]
    left, right = ((5, 7), (5, 8)), ((5, 15), (5, 14))
    records = {}
    for name, extra in (('initial', []), ('left_only', [left]),
                        ('right_only', [right]), ('both', [left, right])):
        record, data = grid_allocation(current, bands, initial+extra)
        assert record['alpha'] == 2 and record['beta'] == 0
        assert record['margin'] == 8*width-30 > 0
        if name == 'initial':
            assert record['defect'] == 2 and record['assigned'] == 0
            assert record['incident_resources'][1] == record['incident_resources'][2] == 0
        else:
            assert record['defect'] == 1 and record['assigned'] == 1
            resource = data[-1][0, 11]
            assert set(record['allocation']['assignment'].values()) == {resource}
            assert record['incident_resources'][2 if name == 'both' else 1] == 1
            assert record['incident_resources'][1 if name == 'both' else 2] == 0
        records[name] = dict(assigned=record['assigned'], deficit=record['defect'],
                             resources=sorted(record['allocation']['assignment'].values()))
    assert records['left_only']['resources'] == records['right_only']['resources'] == records['both']['resources']
    totals['fully_frozen_unique_collision_families'] += 1
    totals['original_beta_resources'] += 0
    return dict(width=width, packet_dimensions=[width+2, 22], selected=34,
                matching=2*width+16, surplus=9*width-28, boundary=width+2,
                margin=8*width-30, states=records)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    totals, examples = Counter(), []
    for width in range(8, 41, 2):
        record = control(width, totals)
        if width in (8, 20, 40):
            examples.append(record)
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(dict(status='PASS', totals=dict(totals), examples=examples,
        scope='Finite controls for the written all-even-width collision construction; '
              'failure concerns distinct-resource allocation, not the grid inequality.'), indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), sort_keys=True))


if __name__ == '__main__':
    main()
