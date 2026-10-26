"""Actual-coordinate controls for the written arbitrary-k relay-cost theorem."""
import json
from pathlib import Path

from check_isolated_hole_detours import edge, neighbours, valid, maximum_adjacent_matching

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def family(k):
    assert k >= 1
    n = 4*k+2
    board = {(r, c) for r in range(n) for c in range(n)}
    h = (2*k, 2*k)
    p = {(r, c) for r in range(n-1) for c in range(n-1)}-{h}
    m = [edge((r, c), (r+1, c))
         for r in list(range(0, 2*k, 2))+list(range(2*k+1, 4*k, 2))
         for c in range(4*k+1)]
    m += [edge((2*k, c), (2*k, c+1))
          for c in list(range(0, 2*k, 2))+list(range(2*k+1, 4*k, 2))]
    line = [(r, n-1) for r in range(n)]+[(n-1, c) for c in reversed(range(n-1))]
    t = {u for u in line if sum(u) % 2}
    long_path = [(r, 2*k) for r in reversed(range(2*k, 4*k+2))]
    position = line.index(long_path[0])
    paths = [long_path]
    for segment in [line[:position], line[position+1:]]:
        assert len(segment) % 2 == 0
        for i in range(0, len(segment), 2):
            a, b = segment[i:i+2]
            paths.append([a, b] if a in t else [b, a])
    return dict(k=k, n=n, board=board, P=p, M=m, H=board-p-t, T=t,
                h=h, line=line, paths=paths, long_path=long_path, position=position)


def check(k):
    d = family(k)
    board, p, m, t, holes, h = [d[x] for x in ['board', 'P', 'M', 'T', 'H', 'h']]
    assert valid(board, p, t)
    assert len(p) == 16*k*k+8*k and len(m) == 8*k*k+4*k
    assert len({u for e in m for u in e}) == 2*len(m)
    assert {u for e in m for u in e} == p
    assert all(v in neighbours(u) for u, v in m)
    assert len(t) == len(holes) == 4*k+2
    assert len(t)+len(m) == d['n']**2//2
    assert {u for u in board-p if len(neighbours(u) & p) >= 2} == {h}
    assert neighbours(h) <= p
    assert min(abs(u[0]-h[0])+abs(u[1]-h[1]) for u in t) == 2*k+1
    assert len(d['line']) == 8*k+3 and len(set(d['line'])) == len(d['line'])
    assert d['position'] == 6*k+2
    assert all((u in t) == (i % 2 == 0) for i, u in enumerate(d['line']))
    flat = [u for path in d['paths'] for u in path]
    assert len(flat) == len(set(flat))
    assert {path[0] for path in d['paths']} == t
    assert {path[-1] for path in d['paths']} == holes
    used_edges = set()
    mset = set(m)
    for path in d['paths']:
        assert len(path) % 2 == 0
        assert all(v in neighbours(u) for u, v in zip(path, path[1:]))
        assert set(path[1:-1]) <= p
        for i, (u, v) in enumerate(zip(path, path[1:])):
            e = edge(u, v)
            if i % 2:
                assert e in mset and e not in used_edges
                used_edges.add(e)
            else:
                assert e not in mset
    assert len(used_edges) == k
    assert len(d['long_path'])-1 == 2*k+1
    adjacent = [path for path in d['paths'] if len(path) == 2]
    assert len(adjacent) == 4*k+1
    assert {path[-1] for path in adjacent} == holes-{h}
    assert maximum_adjacent_matching(t, holes) == 4*k+1
    # Explicit standard matching-decomposition adapter: another actual
    # matching on the same P, independent of the matching used by the detour.
    # Transposition preserves P/h/T and produces a distinct M for every k.
    alternative = [edge((a[1], a[0]), (b[1], b[0])) for a, b in m]
    assert set(alternative) != mset
    decomposition_check(d, alternative)
    return dict(k=k, side=d['n'], T=len(t), H=len(holes), M=len(m),
                J=len(t)+len(m), exact_adjacent_defect=1,
                minimum_T_to_centre_distance=2*k+1,
                exact_minimum_actual_relay_edges=k,
                no_fixed_ell_cover_for_each_ell_below_k=True,
                transposed_rematching_payment_checked=True)


def decomposition_check(d, m):
    """Union with a full horizontal matching, keeping double edges separate."""
    n = d['n']
    fixed = [edge((r, c), (r, c+1)) for r in range(n) for c in range(0, n, 2)]
    mate_m = {u: v for a, b in m for u, v in [(a, b), (b, a)]}
    mate_n = {u: v for a, b in fixed for u, v in [(a, b), (b, a)]}
    paths = []
    for t in sorted(d['T']):
        path = [t]
        while True:
            u = mate_n[path[-1]]; path.append(u)
            if u not in d['P']:
                assert u in d['H']
                break
            path.append(mate_m[u])
            assert len(path) == len(set(path)), 'Must not enter a P-only cycle'
        paths.append(path)
    flat = [u for path in paths for u in path]
    assert len(flat) == len(set(flat))
    assert {p[-1] for p in paths} == d['H']
    relay = sum((len(path)-2)//2 for path in paths)
    assert relay >= d['k']


def main():
    rows = [check(k) for k in range(1, 41)]
    result = dict(status='PASS', parameter_controls=len(rows),
                  smallest=rows[0], largest=rows[-1],
                  scope='Written all-k sharp actual family: adjacent defect one, relay-edge cost k for explicit M, geometric lower bound k under every rematching, no fixed-length forced-hole detour exact cover even fractionally. Standard full-matching decomposition checks another actual M per parameter.',
                  trust_boundary='All-k lower bound, fractional conservation and every-rematching decomposition are written proofs. Finite actual-coordinate controls are validation. No unique matching, freezing, universal numeric counterexample or end-to-end Lean grid formalization is claimed.')
    (ROOT/'output/unbounded-hole-relay.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
