"""Rebuild the height-four whole-vector certificate using literal stars.

The helper contains the independent Python literal-star specification, not
an import of either C++ generator. Both files must accompany this checker.
"""
from pathlib import Path
import hashlib
import json
import sys
from check_grid_star_transfer import (
    failure_tables, step, closes, literal_board_control)

if not __debug__:
    raise RuntimeError('Verification requires assertions; run without -O.')

ROOT = Path(__file__).resolve().parents[1]


def read_vector(path):
    rows = [tuple(map(int, line.split())) for line in path.read_text().splitlines()]
    assert rows == sorted(rows)
    assert len({key for key, _ in rows}) == len(rows)
    for key, score in rows:
        selected, flags = key & 65535, key >> 16
        assert 0 <= key < 2**32 and flags & ~selected == 0
        assert 0 <= score <= 68
    return dict(rows)


def main():
    if len(sys.argv) != 2:
        raise SystemExit('usage: check_grid_star_height_four.py GENERATED_VECTOR_DIRECTORY')
    directory = Path(sys.argv[1])
    kernel = failure_tables(4)
    controls = [literal_board_control(4, length, kernel) for length in range(1, 5)]
    table = {(0, 0): 0}
    optima, vectors, hashes = [], {}, {}
    for length in range(1, 18):
        new = {}
        for state, score in table.items():
            for column in range(16):
                target = step(state, column, 4, kernel, length >= 3)
                if target is not None:
                    new[target] = max(new.get(target, -1), score + column.bit_count())
        table = new
        optima.append(max(score for state, score in table.items()
                          if closes(state, 4, kernel, length)))
        if length in (15, 17):
            vector = {selected | (flags << 16): score
                      for (selected, flags), score in table.items()}
            path = directory / f'grid-star-h4-v{length}.tsv'
            assert read_vector(path) == vector
            vectors[length] = vector
            hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
        print(f'height=4 length={length} states={len(table)} SF={optima[-1]}',
              file=sys.stderr, flush=True)
    assert optima == [2*n + n % 2 for n in range(1, 18)]
    assert vectors[15].keys() == vectors[17].keys()
    assert all(vectors[17][state] == value + 4
               for state, value in vectors[15].items())
    generated = json.loads((directory / 'grid-star-transfer-h4.json').read_text())
    assert generated['optima'] == optima and generated['translation_checked']
    report = {
        'status': 'PASS', 'height': 4, 'literal_five_column_patterns': 2**20,
        'literal_board_controls': controls,
        'literal_board_subsets': sum(c['subsets'] for c in controls),
        'per_subset_transfer_acceptance_comparisons': sum(c['subsets'] for c in controls),
        'prefixes_reconstructed_from_empty': 17, 'optima': optima,
        'full_state_domain': 3**16, 'reachable_certificate_states': len(vectors[15]),
        'start': 15, 'period': 2, 'increment': 4,
        'full_vectors_independently_reconstructed': True,
        'large_vectors_regenerable_not_required_in_source': True,
        'certificate_sha256': hashes, 'new_Lean': False}
    (ROOT / 'output/grid-star-height-four-check.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
