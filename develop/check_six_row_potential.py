"""Check a fixed local invariant, independently of finite-width optimization.

Only Python integers and the standard library are used. Column words, not the
discovery DP's selected/endpoint subset recursion, generate the legal columns.
The all-length argument and the grid adapter are in SIX_ROW_BOUNDARY_INVARIANT.md.
"""
import argparse
from collections import defaultdict
from itertools import product
import json
from pathlib import Path
import random

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
HEIGHT = 6
MASK = 63


def decode(index):
    digits = [(index // 4**r) % 4 for r in range(6)]
    return tuple(sum(1 << r for r, d in enumerate(digits) if pred(d))
                 for pred in (lambda d: d != 0, lambda d: d == 2,
                              lambda d: d == 3))


def encode(o, f, r):
    assert f & ~o == r & ~o == f & r == 0
    return sum((3 if r >> j & 1 else 2 if f >> j & 1 else
                1 if o >> j & 1 else 0) * 4**j for j in range(6))


def valid(state):
    o, f, _ = state
    return not (f & (o << 1) & (o >> 1))


def columns():
    # 0=hole, 1=selected, 2=mate left, 3=mate right,
    # 4=mate below, 5=mate above. Vertical partners must agree.
    out = []
    for word in product(range(6), repeat=6):
        if any((d == 4 and (r == 5 or word[r+1] != 5)) or
               (d == 5 and (r == 0 or word[r-1] != 4))
               for r, d in enumerate(word)):
            continue
        o = sum(1 << r for r, d in enumerate(word) if d)
        t = sum(1 << r for r, d in enumerate(word) if d == 1)
        if t & (o << 1) & (o >> 1):
            continue
        l = sum(1 << r for r, d in enumerate(word) if d == 2)
        right = sum(1 << r for r, d in enumerate(word) if d == 3)
        v = t & ((o << 1) | (o >> 1))
        out.append((t, o, l, right, v, 2*t.bit_count()+(o^t).bit_count()))
    assert len(out) == len(set(out)) == 3345
    return out


def successor(state, column):
    o, f, r = state
    t, new_o, l, right, v, _ = column
    if l != r or f & new_o or v & o:
        return None
    new_f = v | (t & o)
    return new_o, new_f, right


def local_audit(data):
    even, odd = data['even'], data['odd']
    assert len(even) == len(odd) == 4096
    states = [(i, decode(i)) for i in range(4096) if valid(decode(i))]
    assert len(states) == 2404
    assert all(encode(*decode(i)) == i for i in range(4096))
    for i in range(4096):
        assert (even[i] is not None) == (odd[i] is not None) == valid(decode(i))
        if even[i] is not None:
            assert type(even[i]) is type(odd[i]) is int
    cols = columns()
    by_left = defaultdict(list)
    for c in cols:
        by_left[c[2]].append(c)
    transitions = seed = terminal = 0
    for i, state in states:
        if state[2] == 0:
            assert even[i] <= 0 and odd[i] <= 2, ('terminal', i)
            terminal += 1
        for c in by_left[state[2]]:
            new = successor(state, c)
            if new is None:
                continue
            assert valid(new), ('closure', state, c, new)
            j = encode(*new)
            assert c[5]-6+even[i] <= odd[j], ('even-to-odd', i, j, c)
            assert c[5]-6+odd[i] <= even[j], ('odd-to-even', i, j, c)
            transitions += 1
    for c in by_left[0]:
        new = successor((0, 0, 0), c)
        assert new is not None and valid(new)
        j = encode(*new)
        assert c[5]-6 <= odd[j], ('seed', c)
        seed += 1
    assert transitions == 145524 and seed == 740
    return dict(valid_states=len(states), column_variants=len(cols),
                compatible_transitions=transitions, phase_inequalities=2*transitions,
                first_column_cases=seed, terminal_states=terminal)


def project_board(width, selected, matching, data):
    board = {(r, c) for r in range(6) for c in range(width)}
    mate = {}
    for u, v in matching:
        assert u in board and v in board and u not in mate and v not in mate
        assert abs(u[0]-v[0])+abs(u[1]-v[1]) == 1
        mate[u] = v
        mate[v] = u
    assert selected <= board and not selected & mate.keys()
    occupied = selected | mate.keys()
    for r, c in selected:
        assert sum((a, b) in occupied for a, b in
                   [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]) <= 1
    state = (0, 0, 0)
    score = 0
    legal_cols = set(columns())
    for c in range(width):
        t = sum(1 << r for r in range(6) if (r, c) in selected)
        o = sum(1 << r for r in range(6) if (r, c) in occupied)
        l = sum(1 << r for r in range(6)
                if (r, c) in mate and mate[r, c][1] == c-1)
        right = sum(1 << r for r in range(6)
                    if (r, c) in mate and mate[r, c][1] == c+1)
        v = t & ((o << 1) | (o >> 1))
        col = (t, o, l, right, v, 2*t.bit_count()+(o^t).bit_count())
        assert col in legal_cols
        state = successor(state, col)
        assert state is not None and valid(state)
        score += col[5]
        phi = data['odd' if c % 2 == 0 else 'even'][encode(*state)]
        assert score-6*(c+1) <= phi
    assert state[2] == 0 and score == 2*(len(selected)+len(matching))
    assert score <= 6*width+2*(width % 2)
    return len(selected)+len(matching)


def board_controls(data, count=160):
    rng = random.Random(20261027)
    for i in range(count):
        width = rng.randrange(1, 61)
        vertices = [(r, c) for r in range(6) for c in range(width)]
        rng.shuffle(vertices)
        occupied = set()
        matching = []
        for r, c in vertices:
            if (r, c) in occupied or rng.random() > .25:
                continue
            choices = [(a, b) for a, b in [(r-1, c), (r+1, c), (r, c-1), (r, c+1)]
                       if 0 <= a < 6 and 0 <= b < width and (a, b) not in occupied]
            if choices:
                v = rng.choice(choices)
                matching.append(((r, c), v))
                occupied.update([(r, c), v])
        selected = set()
        for r, c in vertices:
            u = (r, c)
            if u in occupied or rng.random() > .8:
                continue
            neighbours = {(r-1, c), (r+1, c), (r, c-1), (r, c+1)}
            if len(neighbours & occupied) <= 1 and all(
                    sum(v in occupied for v in [(a-1, b), (a+1, b), (a, b-1), (a, b+1)]) == 0
                    for a, b in neighbours & selected):
                selected.add(u)
                occupied.add(u)
        project_board(width, selected, matching, data)
    for width in range(1, 81):
        selected = {(r, c) for c in range(width)
                    for r in ([0, 2, 4, 5] if c % 2 == 0 else [1, 3])}
        assert project_board(width, selected, [], data) == 3*width+width % 2
    # Deliberate corruption must be detected by a local premise, without DP.
    damaged = dict(data, even=list(data['even']))
    damaged['even'][0] = 1
    try:
        local_audit(damaged)
    except AssertionError:
        pass
    else:
        raise AssertionError('corrupt potential accepted')
    return dict(random_actual_matching_boards=count, sharp_boards=80,
                corruption_control='PASS')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, default=ROOT/'output/six-row-potential-check.json')
    args = parser.parse_args()
    data = json.loads((ROOT/'output/six-row-potential.json').read_text())
    result = dict(status='PASS', **local_audit(data), **board_controls(data),
                  scope='Fixed local certificate and executable grid adapter; no finite-width optimization used. General length induction is separate.',
                  not_claimed='End-to-end Lean formalization of the grid theorem; extension to arbitrary heights; universal 5/6 improvement.')
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
