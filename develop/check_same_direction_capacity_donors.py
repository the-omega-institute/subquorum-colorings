#!/usr/bin/env python3
"""Check capacity donors and all neutral same-direction receiving tiles."""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from check_cross_component_compensation import band_ledger, witness_record
from check_guarded_half_donors import cap_pattern
from check_residual_corridors import transformed


def local_controls():
    models = []
    choices = [('B', 0), ('T', 0), ('P', 0), ('P', 1)]
    for upper, lower in itertools.product(choices, repeat=2):
        labels = [upper[0], lower[0]]
        selected = labels.count('T')
        endpoints = labels.count('P')
        attachments = upper[1]+lower[1]
        capacity = 2-selected-attachments
        degree = endpoints-attachments
        charge_twice = degree-2*capacity
        assert 0 <= degree <= capacity
        assert charge_twice == -capacity-(2-selected-endpoints)
        assert charge_twice <= -capacity
        assert (charge_twice == 0) == (
            selected+endpoints == 2 and attachments == endpoints)
        models.append(dict(labels=labels[0]+'B/B'+labels[1],
                           attachments=attachments, capacity=capacity,
                           degree=degree, charge_twice=charge_twice,
                           saturated=selected == 2))
    assert len(models) == 16
    assert sum(model['charge_twice'] == 0 for model in models) == 4
    return models


def configuration(kind):
    states, matching = cap_pattern('RR', 0)
    selected = {vertex for vertex, label in states.items() if label == 'T'}
    if kind in ('half', 'neutral_down'):
        selected.add((0, 0))
        matching.append(((1, 1), (2, 1)))
        if kind == 'neutral_down':
            selected.update(((2, 0), (3, 1)))
    elif kind == 'neutral_up':
        selected.update(((1, 1), (-2, 0), (-1, 1)))
        matching.append(((0, 0), (-1, 0)))
    elif kind in ('full', 'neutral_both'):
        matching.extend((((0, 0), (-1, 0)), ((1, 1), (2, 1))))
        if kind == 'neutral_both':
            selected.update(((-2, 0), (-1, 1), (2, 0), (3, 1)))
    elif kind == 'saturated':
        selected.update(((0, 0), (1, 1)))
    else:
        raise ValueError(kind)
    shifted = lambda vertex: (vertex[0]+2, vertex[1]+2)
    return 6, 6, {shifted(vertex) for vertex in selected}, [
        (shifted(first), shifted(second)) for first, second in matching]


def witness_controls():
    expected = {
        'half': (1, 0, 0, 1, 1, -1),
        'full': (0, 0, 0, 2, 2, -2),
        'neutral_down': (1, 0, 1, 0, 0, 0),
        'neutral_up': (1, 0, 1, 0, 0, 0),
        'neutral_both': (0, 0, 2, 0, 0, 0),
        'saturated': (2, 0, 0, 0, 0, 0),
    }
    records = []
    for kind, values in expected.items():
        original = configuration(kind)
        for transpose, flip_row, flip_column in itertools.product((False, True), repeat=3):
            shape, selected, matching = transformed(*original, transpose, flip_row, flip_column)
            current = (*shape, selected, matching)
            record = witness_record(kind, current)
            region = {(row, column) for row, column in itertools.product((2, 3), repeat=2)}
            ledger = band_ledger(*current, region)
            tile = record['tiles'][ledger['tiles'][0]]
            observed = (tile['selected'], tile['internal'], tile['attachments'],
                        tile['capacity'], tile['degree'], ledger['charge_twice'])
            assert observed == values
            assert record['q'] <= 0
            assert 2*record['q'] == sum(
                item['degree']-2*item['capacity'] for item in record['tiles']
                if item['selected'] < 2)
            if kind == 'neutral_down':
                assert record['objective'] == 10 and record['q'] == -8
            if kind == 'half' and not any((transpose, flip_row, flip_column)):
                occupied = selected | {vertex for edge in matching for vertex in edge}
                assert (1, 2) not in occupied
            record['symmetry'] = [transpose, flip_row, flip_column]
            record['donor_ledger'] = ledger
            records.append(record)
    assert len(records) == 48
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    models = local_controls()
    witnesses = witness_controls()
    root = Path(__file__).resolve().parents[1]
    sources = [Path(__file__), root/'docs/SAME_DIRECTION_CAPACITY_DONORS.md']
    sources.extend(Path(__file__).with_name(name) for name in (
        'check_cross_component_compensation.py', 'check_guarded_half_donors.py',
        'check_residual_corridors.py', 'verify_grid_five_sixths.py',
        'verify_grid_short_path_compensation.py'))
    report = dict(status='ALL_CHECKS_PASSED', local_models=models, witnesses=witnesses,
                  sha256={str(path.relative_to(root)): hashlib.sha256(path.read_bytes()).hexdigest()
                          for path in sources},
                  scope='Finite controls for a separate general proof; no general grid allocation or Lean claim.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status=report['status'], local_models=len(models),
                          symmetry_checks=len(witnesses), scope=report['scope'])))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O: verification uses assertions.')
    main()
