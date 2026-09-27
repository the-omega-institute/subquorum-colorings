"""Read-only integrity and mathematical checks of the archived evidence."""
import csv
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def formula(m, n):
    def term(a, b):
        return ((a+1)//2)*((2*b+2)//3)+(a//2)*(b//3)
    return max(term(m,n), term(n,m))


def selected(m, n):
    return {(r,c) for r in range(1,m+1) for c in range(1,n+1)
            if (r%2 and c%3) or (not r%2 and not c%3)}


def main():
    develop = ROOT / 'develop'
    hashes = json.loads((develop/'results/SHA256SUMS.json').read_text())
    for name, expected in hashes.items():
        assert hashlib.sha256((develop/name).read_bytes()).hexdigest() == expected, name
    source = json.loads((ROOT/'formal/UPSTREAM.json').read_text())
    for name, expected in source['sha256'].items():
        assert hashlib.sha256((ROOT/'formal'/name).read_bytes()).hexdigest() == expected, name
    count = 0
    for m in range(1,12):
        rows = list(csv.DictReader((develop/f'results/omega-w{m}.csv').open()))
        assert [int(r['length']) for r in rows] == list(range(1,37 if m==11 else 31))
        for row in rows:
            n = int(row['length'])
            assert int(row['width']) == m
            assert int(row['omega']) == int(row['conjectured']) == formula(m,n)
            choices = [selected(m,n), {(c,r) for r,c in selected(n,m)}]
            assert max(map(len,choices)) == formula(m,n)
            for choice in choices:
                assert all(sum(p in choice for p in [(r-1,c),(r+1,c),(r,c-1),(r,c+1)]) <= 1
                           for r,c in choice)
            count += 1
    for m in (8,9,10,11):
        prefix = develop/f'results/omega-w{m}'
        meta = json.loads(prefix.with_suffix('.json').read_text())
        entries = 0
        previous = -1
        with Path(str(prefix)+'-start.tsv').open() as first, Path(str(prefix)+'-end.tsv').open() as last:
            for line in first:
                s, w = map(int,line.split())
                t, z = map(int,next(last).split())
                assert s > previous and s == t and z-w == meta['doubled_increment']
                previous = s
                entries += 1
            assert next(last,None) is None
        assert entries == meta['states']
    print(json.dumps(dict(status='passed', evidence_files=len(hashes),
                          finite_grids=count, vector_translations=[8,9,10,11],
                          pinned_formal_sources='intact'), indent=2))


if __name__ == '__main__':
    main()
