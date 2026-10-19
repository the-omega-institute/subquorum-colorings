"""Check exact cavity flux when complete combs cross the open boundary."""

import argparse
import itertools
import json
from pathlib import Path

from check_closed_source_cavities import cavity_record, nested_cavities, obstructed_rung
from check_coalesced_mouths import optimize
from check_mixed_source_contacts import source_with_chamber
from check_remote_comb_rungs import remote_family
from check_saturated_bent_bands import long_bent


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def controls():
    records = []
    for depth, left_length, right_length in itertools.product((1, 2, 5), (1, 2, 5, 12), (1, 2, 5, 12)):
        current, sources, rung = remote_family(depth, left_length, right_length)
        tip = 2*depth+4
        cavity = set(itertools.product(range(4, tip+2), range(4, 12)))
        record = cavity_record(current, sources, cavity, allow_open=True)
        assert record['cavity_comb_flux'] == -2
        records.append(dict(kind='two_sparse_ends_inside_two_saturated_ends_outside',
                            depth=depth, lengths=(left_length, right_length), result=record))
    for width, depth in itertools.product((8, 10, 16, 32), (1, 2, 5, 12)):
        current, unused = long_bent(width, depth, saturate=True)
        sources = [source_with_chamber(width, depth)]
        current = optimize(current, sources)
        cavity = set(itertools.product(range(4, 2*depth+6), range(4, width+2)))
        record = cavity_record(current, sources, cavity, allow_open=True)
        assert record['cavity_comb_flux'] == 0
        assert record['physical']['payment'] == 2
        assert record['shifted']['payment'] == 0
        records.append(dict(kind='sharp_closed_cavity_without_combs', width=width,
                            depth=depth, result=record))
    for count in (1, 2, 3, 5):
        current, sources, cavity = nested_cavities(count)
        record = cavity_record(current, sources, cavity, allow_open=True)
        assert record['cavity_comb_flux'] == 0
        records.append(dict(kind='closed_nested_sources_cancel_all_comb_ends', count=count, result=record))
    current, sources, cavity, rung = obstructed_rung(32, 3)
    record = cavity_record(current, sources, cavity, allow_open=True)
    assert record['cavity_comb_flux'] == 0 and record['ledger']['weighted_comb_flux'] == -2
    records.append(dict(kind='negative_mouth_flux_but_closed_cavity_flux_zero', result=record))
    return dict(status='ALL_CHECKS_PASSED', physical_cases=len(records), records=records,
                scope='Exact original/shifted cavity identity with signed membership of complete-comb '
                      'physical singleton ends, including open combs and closed mixed orientations. '
                      'No partial endpoint receiver is a donor. The geometric flux sum and '
                      'conditional source-cover bound are written; no universal flux bound claimed.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    arguments = parser.parse_args()
    report = controls()
    arguments.output.parent.mkdir(parents=True, exist_ok=True)
    arguments.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({key: report[key] for key in ('status', 'physical_cases')}))


if __name__ == '__main__':
    main()
