#!/usr/bin/env python3
"""Check an all-neutral full grid containing a same-direction relay."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_cross_component_compensation import band_ledger, witness_record
from check_residual_corridors import transformed


def neutral_completion():
    selected = {
        (0, 0), (0, 2), (0, 3), (0, 5), (0, 7), (1, 7),
        (2, 0), (2, 2), (2, 4), (2, 6), (3, 1), (3, 5), (3, 7),
        (4, 0), (4, 2), (4, 4), (4, 6), (5, 1), (5, 3), (5, 5), (5, 7),
        (6, 0), (6, 2), (6, 4), (7, 0), (7, 2), (7, 4), (7, 7),
    }
    matching = [((1, 1), (2, 1)), ((1, 5), (2, 5)),
                ((3, 3), (4, 3)), ((5, 6), (6, 6))]
    return 8, 8, selected, matching


def patch_controls(configuration):
    rows, columns, selected, matching = configuration
    endpoints = {vertex for edge in matching for vertex in edge}
    expected = {(1, 0): 'TP/BT', (1, 1): 'TB/BP',
                (1, 2): 'TP/BT', (2, 1): 'TP/BT'}
    for (tile_row, tile_column), wanted in expected.items():
        labels = ''.join('T' if vertex in selected else 'P' if vertex in endpoints else 'B'
                         for vertex in ((2*tile_row+row, 2*tile_column+column)
                                        for row, column in itertools.product(range(2), repeat=2)))
        assert labels[:2]+'/'+labels[2:] == wanted
    edges = {frozenset(edge) for edge in matching}
    assert all(frozenset(edge) in edges for edge in (
        ((1, 1), (2, 1)), ((1, 5), (2, 5)), ((3, 3), (4, 3))))
    assert (1, 2) not in selected | endpoints
    return [dict(tile=list(tile), labels=labels) for tile, labels in expected.items()]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    original = neutral_completion()
    patch = patch_controls(original)
    records = []
    region = {(row, column) for row, column in itertools.product((2, 3), repeat=2)}
    for transpose, flip_rows, flip_columns in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*original, transpose, flip_rows, flip_columns)
        _, moved_region, _ = transformed(original[0], original[1], region, [],
                                          transpose, flip_rows, flip_columns)
        current = (*shape, selected, matching)
        record = witness_record('all_neutral_relay_completion', current)
        assert len(selected) == 28 and len(matching) == 4
        assert record['objective'] == 32 and record['q'] == 0
        assert sum(tile['selected'] == 2 for tile in record['tiles']) == 12
        assert all(tile['capacity'] == tile['degree'] == tile['internal'] == 0
                   for tile in record['tiles'])
        assert len(record['components']) == 4
        assert all(component['excess'] == 0 and len(component['tiles']) == 1
                   for component in record['components'])
        ledger = band_ledger(*current, moved_region)
        assert (ledger['selected'], ledger['saturated_attachments'],
                ledger['capacity_sum'], ledger['residual_degrees'],
                ledger['charge_twice']) == (1, 1, 0, [0], 0)
        record['relay_ledger'] = ledger
        record['symmetry'] = [transpose, flip_rows, flip_columns]
        records.append(record)
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/NEUTRAL_RELAY_OBSTACLE.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_cross_component_compensation.py', 'check_residual_corridors.py',
        'verify_grid_five_sixths.py', 'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', patch=patch, witnesses=records,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Exact counterexample to unconditional relay-to-negative-region propagation; no positive source in this witness, and no grid-conjecture refutation.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], symmetry_checks=len(records),
                          q=0, zero_charge_tiles=16, scope=report['scope'])))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
