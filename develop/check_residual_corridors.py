#!/usr/bin/env python3
"""Check the explicit unbounded LL corridor family and its local replacement."""
import argparse
import hashlib
import json
from pathlib import Path

from verify_grid_short_path_compensation import residual, check_geometry


def corridor(k):
    m, n = 4, 2*k+4
    T = {(0, 0), (0, n-1), (2, 0), (3, 1), (2, n-1), (3, n-2)}
    M = [((0, 2*i+1), (0, 2*i+2)) for i in range(k+1)]
    M += [((1, 2*i), (1, 2*i+1)) for i in range(1, k+1)]
    M += [((1, 1), (2, 1)), ((1, n-2), (2, n-2))]
    return m, n, T, M


def direct_check(m, n, T, M):
    # Coordinate checks do not use the patch builder or bit-mask feasibility code.
    used = set()
    for u, v in M:
        assert abs(u[0]-v[0])+abs(u[1]-v[1]) == 1
        assert u not in used and v not in used and u not in T and v not in T
        used.update((u, v))
    occupied = T | used
    assert all(0 <= i < m and 0 <= j < n for i, j in occupied)
    for i, j in T:
        assert sum((i+di, j+dj) in occupied
                   for di, dj in ((1, 0), (-1, 0), (0, 1), (0, -1))) <= 1
    return len(T)+len(M)


def graph_record(m, n, T, M):
    index = lambda v: v[0]*n+v[1]
    g = residual(m, n, sum(1 << index(v) for v in T),
                 tuple((index(u), index(v)) for u, v in M))
    seen = set()
    components = []
    for start in range(g['N']):
        if g['t'][start] == 2 or start in seen:
            continue
        todo = [start]; seen.add(start); vertices = []
        while todo:
            v = todo.pop(); vertices.append(v)
            for w, _ in g['neighbors'][v]:
                if w not in seen:
                    seen.add(w); todo.append(w)
        C = sum(g['deg'][v] for v in vertices)//2
        R = sum(g['r'][v] for v in vertices)
        components.append(dict(tiles=sorted(vertices), edges=C, capacity=R, excess=C-R))
    return g, components


def transformed(m, n, T, M, transpose, flip_i, flip_j):
    def f(v):
        i, j = v
        i = m-1-i if flip_i else i
        j = n-1-j if flip_j else j
        return (j, i) if transpose else (i, j)
    return (n, m) if transpose else (m, n), {f(v) for v in T}, [(f(u), f(v)) for u, v in M]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-k', type=int, default=40)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    assert args.max_k >= 2
    examples = []
    count = 0
    for k in range(1, args.max_k+1):
        m, n, T, M = corridor(k)
        newT = T | {(2, 2*i) for i in range(1, k+1)}
        newM = [(u, v) for u, v in M if u[0] != 1 or v[0] != 1]
        for transpose in (False, True):
            for flip_i in (False, True):
                for flip_j in (False, True):
                    (a, b), U, N = transformed(m, n, T, M, transpose, flip_i, flip_j)
                    _, newU, newN = transformed(m, n, newT, newM, transpose, flip_i, flip_j)
                    objective = direct_check(a, b, U, N)
                    assert objective == direct_check(a, b, newU, newN) == 2*k+9
                    g, components = graph_record(a, b, U, N)
                    ng, nc = graph_record(a, b, newU, newN)
                    positives = [c for c in components if c['excess'] > 0]
                    assert len(positives) == 1
                    assert positives[0]['edges'] == k+1
                    assert positives[0]['capacity'] == k
                    assert sum(c['excess'] for c in components) == 1-2*k
                    assert sum(g['h']) == k and sum(ng['h']) == 0
                    assert all(c['excess'] <= 0 for c in nc)
                    assert len(check_geometry(g)) == (1 if k == 1 else 0)
                    count += 1
        if k in (2, 3):
            _, components = graph_record(m, n, T, M)
            examples.append(dict(k=k, m=m, n=n, T=sorted(T), M=M,
                                 objective=2*k+9, q=1-2*k, components=components))
    report = dict(status='ALL_CHECKS_PASSED', k_range=[1, args.max_k],
                  symmetry_images_checked=count, examples=examples,
                  scope='Finite regression checks; the all-k construction and local replacement have a separate written proof.',
                  script_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'examples'}))


if __name__ == '__main__':
    main()
