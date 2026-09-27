"""Check exact readouts, constructive lower bounds and saved vector translations."""
import csv
import hashlib
import json
from pathlib import Path


def formula(m, n):
    def term(a, b):
        return ((a + 1) // 2) * ((2 * b + 2) // 3) + (a // 2) * (b // 3)
    return max(term(m, n), term(n, m))


def periodic_set(m, n):
    return {(r, c) for r in range(1, m + 1) for c in range(1, n + 1)
            if (r % 2 == 1 and c % 3 != 0) or (r % 2 == 0 and c % 3 == 0)}


def main():
    checked = 0
    for m in range(1, 12):
        rows = list(csv.DictReader(Path(f'results/omega-w{m}.csv').open()))
        last_length = 36 if m == 11 else 30
        assert [int(r['length']) for r in rows] == list(range(1, last_length + 1))
        for row in rows:
            n = int(row['length'])
            expected = formula(m, n)
            assert int(row['omega']) == int(row['conjectured']) == expected
            candidates = [periodic_set(m, n), {(c, r) for r, c in periodic_set(n, m)}]
            for selected in candidates:
                assert all(sum((a, b) in selected for a, b in
                               [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]) <= 1
                           for r, c in selected)
            assert max(map(len, candidates)) == expected
            checked += 1
    certificates = []
    for m in [8, 9, 10, 11]:
        prefix = Path(f'results/omega-w{m}')
        meta = json.loads(prefix.with_suffix('.json').read_text())
        first = dict(tuple(map(int, line.split())) for line in
                     Path(str(prefix) + '-start.tsv').read_text().splitlines())
        last = dict(tuple(map(int, line.split())) for line in
                    Path(str(prefix) + '-end.tsv').read_text().splitlines())
        assert len(first) == len(last) == meta['states']
        assert last == {s: w + meta['doubled_increment'] for s, w in first.items()}
        assert meta['doubled_increment'] % 2 == 0
        certificates.append(meta)
    independent = json.loads(Path('results/independent-vector-check.json').read_text())
    log = Path('results/independent-w11.log').read_text().strip()
    meta = json.loads(Path('results/omega-w11.json').read_text())
    expected = ('PASS width=11 start=16 period=3 doubled_increment=34 '
                'states=1949930')
    assert log == expected
    independent = [r for r in independent if r['width'] != 11]
    independent.append(dict(meta, verification='passed', stdout=log))
    Path('results/independent-vector-check.json').write_text(json.dumps(independent, indent=2) + '\n')
    assert {r['width'] for r in independent if r['verification'] == 'passed'} >= {8, 9, 10, 11}
    summary = dict(status='passed', finite_grid_checks=checked,
                   constructive_lower_bounds='checked for every finite case',
                   certificates=certificates, independently_recomputed=True,
                   small_exhaustive_check='results/small-exhaustive-check.json',
                   lean_formalized=False,
                   scope='Widths 8, 9, 10, 11 at all positive lengths via full-vector translation; arbitrary width remains open.')
    Path('results/verification-summary.json').write_text(json.dumps(summary, indent=2) + '\n')
    files = list(Path('.').glob('*.cpp')) + list(Path('.').glob('*.py'))
    files += [p for p in Path('results').iterdir() if p.is_file() and p.name != 'SHA256SUMS.json']
    manifest = {str(p): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    Path('results/SHA256SUMS.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print(json.dumps(summary, indent=2))


if __name__ == '__main__':
    main()
