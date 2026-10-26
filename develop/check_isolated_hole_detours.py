"""Solver-free controls for the written all-q isolated-hole/detour proof.

The column DP is independent of the cover and optimizes arbitrary T at fixed P.
Finite controls are not used as a proof of the periodic construction.
"""
from collections import defaultdict
from itertools import combinations
import json
from pathlib import Path
import random

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
BASE_M = [((0, 2), (1, 2)), ((2, 0), (2, 1)),
          ((2, 3), (2, 4)), ((3, 2), (4, 2))]
BASE_G = [((0, 0), (1, 0)), ((0, 1), (1, 1)), ((0, 3), (1, 3)),
          ((3, 0), (3, 1)), ((3, 3), (4, 3)), ((3, 4), (3, 5)),
          ((5, 2), (5, 3))]
BASE_S = [(0, 4), (0, 6), (2, 6), (4, 0), (4, 4), (4, 6)]
BASE_F = {(1, 1), (1, 3), (2, 2), (3, 1), (3, 3)}
BASE_PATH = ((2, 5), (2, 4), (2, 3), (2, 2))


def neighbours(u):
    r, c = u
    return {(r-1, c), (r+1, c), (r, c-1), (r, c+1)}


def edge(u, v):
    return tuple(sorted((u, v)))


def square(r, c):
    return frozenset((r+i, c+j) for i in (0, 1) for j in (0, 1))


def family(q, padding=(0, 0, 0, 0)):
    assert q >= 1 and all(x >= 0 and x % 2 == 0 for x in padding)
    top, bottom, left, right = padding
    height, width = 6+top+bottom, 8*q+left+right
    board = {(r, c) for r in range(height) for c in range(width)}
    matching, pairs, squares, paths = [], [], [], []
    forced, centres = set(), set()
    for j in range(q):
        def shift(u):
            return u[0]+top, u[1]+left+8*j
        matching += [edge(shift(a), shift(b)) for a, b in BASE_M]
        pairs += [tuple(map(shift, p)) for p in BASE_G]
        squares += [frozenset(map(shift, square(*a))) for a in BASE_S]
        paths.append(tuple(map(shift, BASE_PATH)))
        forced |= set(map(shift, BASE_F)); centres.add(shift((2, 2)))
    # Disjoint padding: first horizontal full-width strips, then side strips.
    for start, stop in [(0, top), (top+6, height)]:
        squares += [square(r, c) for r in range(start, stop, 2)
                    for c in range(0, width, 2)]
    for start, stop in [(0, left), (left+8*q, width)]:
        squares += [square(r, c) for r in range(top, top+6, 2)
                    for c in range(start, stop, 2)]
    p = {u for e in matching for u in e}
    return dict(q=q, height=height, width=width, board=board, matching=matching,
                P=p, pairs=pairs, squares=squares, paths=paths,
                forced=forced, centres=centres)


def valid(board, p, t):
    return t <= board-p and all(len(neighbours(u) & (p | t)) <= 1 for u in t)


def cover_check(d):
    board, p, m = d['board'], d['P'], d['matching']
    assert len(m) == 4*d['q'] and len(p) == 2*len(m)
    assert all(v in neighbours(u) for u, v in m)
    mate = {u: v for a, b in m for u, v in [(a, b), (b, a)]}
    assert all(neighbours(u) & p == {mate[u]} for u in p)
    # The induced P graph is exactly M, so the matching is unique.
    forced = {u for u in board-p if len(neighbours(u) & p) >= 2}
    assert forced == d['forced'] and len(forced) == 5*d['q']
    assert all(sum(u) % 2 == 0 for u in forced)
    assert all(neighbours(u) <= p for u in d['centres'])
    assert len(d['centres']) == d['q']
    flat = []
    for a, b in d['pairs']:
        assert b in neighbours(a) and (neighbours(a) & p or neighbours(b) & p)
        flat += [a, b]
    for s in d['squares']:
        assert len(s) == 4 and not s & p
        assert s == square(min(u[0] for u in s), min(u[1] for u in s))
        flat += list(s)
    used = set()
    for t, x, y, h in d['paths']:
        assert len({t, x, y, h}) == 4
        assert x in neighbours(t) and h in neighbours(y)
        e = edge(x, y)
        assert e in m and e not in used
        assert h in forced and t not in p
        used.add(e); flat += [t, h]
    assert len(flat) == len(set(flat)) and set(flat) == board-p
    # All possible local pieces, in every square alignment, have the
    # imbalance used in the written integral/fractional impossibility proof.
    qsites = board-p
    assert sum(sum(u) % 2 == 0 for u in qsites)*2 == len(qsites)
    assert all(not (neighbours(u) & qsites) for u in d['centres'])
    assert all(sum(u) % 2 != sum(v) % 2
               for u in qsites for v in neighbours(u) & qsites)
    for r in range(d['height']-1):
        for c in range(d['width']-1):
            s = square(r, c)
            if s <= qsites:
                assert sum(sum(u) % 2 == 0 for u in s) == 2
                assert not s & d['centres']


def square_payment(s, t):
    selections, holes = sorted(s & t), s-t
    assert len(selections) <= 2
    def visit(k, used):
        if k == len(selections):
            return {}
        u = selections[k]
        for h in sorted(neighbours(u) & holes-used):
            tail = visit(k+1, used | {h})
            if tail is not None:
                return {u: h, **tail}
        return None
    result = visit(0, set())
    assert result is not None
    return result


def payment_check(d, t):
    board, p = d['board'], d['P']
    assert valid(board, p, t)
    holes = board-p-t
    paths = []
    for pair in d['pairs']:
        selected = set(pair) & t
        assert len(selected) <= 1
        if selected:
            u = next(iter(selected)); h = next(iter(set(pair)-selected))
            paths.append((u, h))
    for s in d['squares']:
        paths += list(square_payment(s, t).items())
    for path in d['paths']:
        if path[0] in t:
            paths.append(path)
        assert path[-1] in holes
    assert {path[0] for path in paths} == t and len(paths) == len(t)
    assert all(path[-1] in holes for path in paths)
    flat = [u for path in paths for u in path]
    assert len(flat) == len(set(flat))
    relay_edges = set()
    for path in paths:
        assert len(path) in (2, 4)
        assert all(v in neighbours(u) for u, v in zip(path, path[1:]))
        if len(path) == 4:
            e = edge(path[1], path[2])
            assert e in d['matching'] and e not in relay_edges
            relay_edges.add(e)
    capacity = len(d['pairs'])+len(d['paths'])+2*len(d['squares'])
    deficit = capacity-len(t)
    assert deficit >= 0 and len(holes)-len(t) == 2*deficit
    assert len(t)+len(d['matching']) == len(board)//2-deficit
    assert len(relay_edges) <= d['q']
    return dict(selections=len(t), holes=len(holes), deficit=deficit,
                relay_edges=len(relay_edges), paths=paths)


def maximum_adjacent_matching(t, holes):
    owner = {}
    def augment(u, seen):
        for h in sorted(neighbours(u) & holes):
            if h in seen:
                continue
            seen.add(h)
            if h not in owner or augment(owner[h], seen):
                owner[h] = u
                return True
        return False
    for u in sorted(t):
        augment(u, set())
    return len(owner)


def sharp_check(d, independent=False):
    t = {u for u in d['board']-d['P'] if sum(u) % 2}
    out = payment_check(d, t)
    assert out['deficit'] == 0 and out['relay_edges'] == d['q']
    adjacent = [path for path in out['paths'] if len(path) == 2]
    assert len(adjacent) == len(t)-d['q']
    assert {path[-1] for path in adjacent} == d['board']-d['P']-t-d['centres']
    if independent:
        assert maximum_adjacent_matching(t, d['board']-d['P']-t) == len(t)-d['q']
    return dict(q=d['q'], height=d['height'], width=d['width'], T=len(t),
                H=out['holes'], M=len(d['matching']), J=len(d['board'])//2,
                exact_adjacent_matching=len(adjacent), exact_adjacent_defect=d['q'],
                exact_minimum_relay_edges=d['q'], forced_holes=len(d['forced']))


def arbitrary_selection_dp(d):
    """All feasible T, column by column, without cover/forced-hole assumptions.

    State (previous T mask, previous selected sites already seeing one occupied
    neighbour). Vertical and left neighbours are checked on entry; the next
    column must avoid adding a second neighbour. Store all-count/best/max-count.
    """
    height, width = d['height'], d['width']
    pcols = [sum(1 << r for r in range(height) if (r, c) in d['P'])
             for c in range(width)]
    states = {(0, 0): (1, 0, 1)}
    peak = 1
    for c, pmask in enumerate(pcols):
        choices = []
        for selected in range(1 << height):
            if selected & pmask:
                continue
            occupied = selected | pmask
            if selected & (occupied << 1) & (occupied >> 1):
                continue
            vertical = selected & ((occupied << 1) | (occupied >> 1))
            choices.append((selected, occupied, vertical, selected.bit_count()))
        new = {}
        for (old_t, old_blocked), (count, best, max_count) in states.items():
            old_occupied = old_t | (pcols[c-1] if c else 0)
            for selected, occupied, vertical, size in choices:
                if old_blocked & occupied or vertical & old_occupied:
                    continue
                blocked = vertical | (selected & old_occupied)
                key = selected, blocked
                previous = new.get(key, (0, -1, 0))
                score = best+size
                new[key] = (previous[0]+count, max(previous[1], score),
                            max_count if score > previous[1] else
                            previous[2]+max_count if score == previous[1] else previous[2])
        states = new; peak = max(peak, len(states))
    best = max(v[1] for v in states.values())
    assert best == len(d['board'])//2-len(d['matching'])
    return dict(q=d['q'], maximum_T=best, maximum_J=best+len(d['matching']),
                feasible_T=sum(v[0] for v in states.values()),
                maximizing_T=sum(v[2] for v in states.values() if v[1] == best),
                peak_states=peak)


def corner_control():
    board = {(r, c) for r in range(4) for c in range(4)}
    p = {(0, 1), (0, 2), (1, 0), (2, 0)}
    sites = sorted(board-p)
    histogram = defaultdict(int)
    for mask in range(1 << len(sites)):
        t = {u for i, u in enumerate(sites) if mask >> i & 1}
        if valid(board, p, t):
            histogram[len(t)] += 1
    sharp = {u for u in sites if sum(u) % 2}
    assert max(histogram) == 6 and len(sharp) == 6
    assert valid(board, p, sharp)
    assert maximum_adjacent_matching(sharp, board-p-sharp) == 5
    dp = arbitrary_selection_dp(dict(board=board, P=p, height=4, width=4,
                                    matching=[((0, 1), (0, 2)), ((1, 0), (2, 0))], q=0))
    assert dp['feasible_T'] == sum(histogram.values())
    assert dp['maximum_T'] == max(histogram) and dp['maximizing_T'] == histogram[6]
    return dict(profiles=1 << len(sites), feasible_T=sum(histogram.values()),
                histogram=dict(sorted(histogram.items())), maximum_T=6, adjacent_defect=1,
                independent_DP_matches_full_exhaustion=True)


def main():
    rows = []
    sampled = 0
    rng = random.Random(20261027)
    for q in range(1, 51):
        d = family(q); cover_check(d)
        rows.append(sharp_check(d, independent=q <= 12))
        for mode in range(4):
            order = sorted(d['board']-d['P']); rng.shuffle(order)
            t = set()
            occupied = set(d['P'])
            for u in order:
                if mode == 0 and rng.randrange(2):
                    continue
                if len(neighbours(u) & occupied) > 1:
                    continue
                if any(neighbours(v) & occupied for v in neighbours(u) & t):
                    continue
                t.add(u); occupied.add(u)
            payment_check(d, t); sampled += 1
    padded = []
    for q, padding in [(1, (2, 2, 2, 2)), (2, (4, 6, 8, 2)),
                       (3, (12, 10, 14, 16)), (5, (0, 4, 6, 0))]:
        d = family(q, padding); cover_check(d)
        padded.append(sharp_check(d, independent=True))
    local = 0
    s = square(0, 0)
    for size in range(5):
        for combo in combinations(sorted(s), size):
            t = set(combo)
            if valid(set(s), set(), t):
                square_payment(s, t); local += 1
    assert local == 11
    dp = [arbitrary_selection_dp(family(q)) for q in range(1, 5)]
    result = dict(status='PASS', parameter_controls=len(rows), smallest=rows[0],
                  largest=rows[-1], arbitrary_both_colour_samples=sampled,
                  padded_controls=padded, exhaustive_square_states=local,
                  corner_exhaustion=corner_control(), independent_column_dp=dp,
                  scope='Written all-q mixed-cover proof, exact arbitrary-T fixed-footprint maximum, exact adjacent defect q, no integral/fractional local cover, and q necessary/sufficient physical relay edges. Padding preserves all claims.',
                  trust_boundary='Finite DP and samples validate adapters, not universal-width proof. Fractional impossibility and minimum-cost lower bound are written conservation/disjointness proofs. Universal cover existence, arbitrary footprints, freezing, 5/6 improvement and end-to-end grid Lean are not claimed.')
    (ROOT/'output/isolated-hole-detours.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
