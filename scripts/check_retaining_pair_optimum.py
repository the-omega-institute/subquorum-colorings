#!/usr/bin/env python3
"""Independent coordinate check of the exact retaining-pair unit optimum."""
import json
from pathlib import Path


def adjacent(a, b):
    return sum(abs(x-y) for x, y in zip(a, b)) == 1


def edge(a, b):
    return tuple(sorted((a, b)))


def main():
    board = {(a, b) for a in range(8) for b in range(12)}
    origins = [(1, 3), (1, 9), (5, 5)]
    local = [((0, 0), (0, 1)), ((0, 2), (1, 2)),
             ((2, 2), (2, 1)), ((2, 0), (1, 0))]
    actual = set()
    squares = set()
    for r, c in origins:
        squares.update((r+a, c+b) for a in range(3) for b in range(3))
        actual.update(edge((r+a, c+b), (r+x, c+y))
                      for (a, b), (x, y) in local)
    mate = {a: b for e in actual for a, b in (e, e[::-1])}
    q = board-mate.keys()
    white = {v for v in q if sum(v) % 2}
    holes = {(4, 5)}
    selected = white-holes
    assert all(sum(adjacent(t, p) for p in mate) <= 1 for t in selected)
    a = [(4, 9), (3, 9), (2, 9), (2, 10)]
    c = [(5, 8), (5, 7), (6, 7), (6, 6)]
    h = [(4, 5), (3, 5), (3, 4), (2, 4)]
    extra = [(0, 11), (1, 11), (2, 11), (3, 11), (3, 10), (4, 10)]
    paths = [a, c, h, extra]
    used = {v for p in [a, c] for v in p}
    d = {(4, 10), (5, 9), (5, 11), (6, 8), (6, 10), (7, 9), (7, 11)}
    f = {t for t in selected if any(adjacent(t, b) for b in d)}
    assert f == {(4, 9), (4, 11), (5, 8), (5, 10),
                 (6, 9), (6, 11), (7, 8), (7, 10)}
    assert len(d) == 7 and len(f) == 8

    # Alternating white-state reachability stops at every Q endpoint.
    reached = set(holes)
    pending = list(holes)
    hh_ends = set()
    while pending:
        s = pending.pop()
        for b in board-used:
            if not adjacent(s, b):
                continue
            if b not in mate:
                hh_ends.add(b)
            elif mate[b] not in used and mate[b] not in reached:
                reached.add(mate[b])
                pending.append(mate[b])
    assert reached == {(4, 5), (3, 4), (2, 3), (1, 4), (2, 5), (5, 6)}
    assert not hh_ends & d
    boundary = {w for w in mate if sum(w) % 2 and any(adjacent(w, b) for b in d)}
    assert boundary == {(3, 10), (6, 7)}
    one_edge = [[s, b, w, end]
                for s in selected-f-used
                for b, w in mate.items() if not sum(b) % 2
                if b not in used and w not in used and adjacent(s, b)
                for end in d if adjacent(w, end)]
    assert not one_edge

    # Construct N from relays, unused actual edges, and a literal exterior tiling.
    all_path_vertices = {v for p in paths for v in p}
    assert sum(map(len, paths)) == len(all_path_vertices)
    auxiliary = set()
    for p in paths:
        assert all(adjacent(x, y) for x, y in zip(p, p[1:]))
        assert all(edge(p[i], p[i+1]) in actual for i in range(1, len(p)-1, 2))
        auxiliary.update(edge(p[i], p[i+1]) for i in range(0, len(p)-1, 2))
    auxiliary.update(e for e in actual if not set(e) & all_path_vertices)
    vertical = [edge((r, b), (r+1, b)) for r, b in
                [(0, 2), (0, 7), (0, 8), (1, 6), (2, 2), (2, 7),
                 (2, 8), (3, 6), (4, 2), (4, 11), (6, 4)]]
    outside = board-squares-holes-{a[0], c[0], extra[0], extra[-1]}
    assert all(set(e) <= outside for e in vertical)
    remaining = outside-{v for e in vertical for v in e}
    rows = {}
    horizontal = []
    for r in range(8):
        runs = []
        for b in sorted(b for rr, b in remaining if rr == r):
            if not runs or b > runs[-1][-1]+1:
                runs.append([b])
            else:
                runs[-1].append(b)
        rows[r] = [[run[0], run[-1]] for run in runs]
        assert all(len(run) % 2 == 0 for run in runs)
        horizontal.extend(edge((r, run[i]), (r, run[i+1]))
                          for run in runs for i in range(0, len(run), 2))
    auxiliary.update(vertical)
    auxiliary.update(horizontal)
    assert len(auxiliary) == 48
    assert {v for e in auxiliary for v in e} == board
    assert all(adjacent(*e) for e in auxiliary)
    nmate = {a: b for e in auxiliary for a, b in (e, e[::-1])}
    assert len(nmate) == 96

    # Score actual tagged alternating components, independently of construction.
    expense = 0
    terminal_paths = []
    for source in sorted(white):
        path = [source]
        v = source
        paid = []
        while True:
            v = nmate[v]
            path.append(v)
            if v not in mate:
                break
            paid.append(edge(v, mate[v]))
            v = mate[v]
            path.append(v)
        assert len(set(path)) == len(path)
        fee = len(paid) if source in selected else 0
        expense += fee
        if len(path) > 2:
            terminal_paths.append(dict(path=path, fee=fee, actual_edges=paid))
    assert expense == 4
    assert {tuple(map(tuple, p['path'])) for p in terminal_paths} == {
        tuple(p) for p in paths}
    result = dict(status='PASS', constrained_unit_optimum=4,
                  unrestricted_unit_optimum=2,
                  lower_bound='A and C withdraw two sources; no HH path enters D; '
                              'a TH path from outside F to D needs at least two M edges.',
                  hall_black=sorted(d), hall_white=sorted(f),
                  HH_reachable_white_states=sorted(reached),
                  HH_endpoints=sorted(hh_ends), one_actual_compensations=one_edge,
                  actual=sorted(actual), auxiliary=sorted(auxiliary),
                  terminal_paths=terminal_paths, exterior_vertical=vertical,
                  horizontal_intervals=rows,
                  scope='Coordinate proof over all retaining matchings; no new Lean execution.')
    output = Path('output/retaining-pair-exact-four.json')
    output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k: result[k] for k in ['status', 'constrained_unit_optimum',
                                           'lower_bound', 'scope']}, indent=2))


if __name__ == '__main__':
    main()
