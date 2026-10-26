"""Verify an explicit obstruction; the general local upper bound is written."""
import json
from pathlib import Path

from check_six_row_potential import columns, successor

ROOT = Path(__file__).resolve().parents[1]


def actual_board(completion):
    selected = {(2, 0)}
    matching = [((r, 0), (r, 1)) for r in [1, 4, 5]]
    for c, word in enumerate(completion, 1):
        t, o, l, right, _, _ = word
        selected.update((r, c) for r in range(6) if t >> r & 1)
        matching.extend(((r, c), (r, c+1)) for r in range(6) if right >> r & 1)
        # The literal completions contain no vertical matching edges.
        assert (o ^ t) == l | right
    width = len(completion)+1
    board = {(r, c) for r in range(6) for c in range(width)}
    mate = {}
    for u, v in matching:
        assert u in board and v in board and u not in mate and v not in mate
        assert abs(u[0]-v[0])+abs(u[1]-v[1]) == 1
        mate[u], mate[v] = v, u
    assert not selected & mate.keys()
    occupied = selected | mate.keys()
    for r, c in selected:
        neighbours = {(r-1, c), (r+1, c), (r, c-1), (r, c+1)}
        assert len(neighbours & occupied) <= 1
    old_o = sum(1 << r for r in range(6) if (r, 0) in occupied)
    old_f = sum(1 << r for r in range(6) if (r, 0) in selected and
                any((a, 0) in occupied for a in [r-1, r+1]))
    old_r = sum(1 << r for r in range(6)
                if (r, 0) in mate and mate[r, 0][1] == 1)
    state = (old_o, old_f, old_r)
    assert state == (54, 4, 50)
    for word in completion:
        assert word in columns()
        state = successor(state, word)
        assert state is not None
    assert state[2] == 0
    reward = sum(word[5] for word in completion)-6*len(completion)
    endpoints = {v for v in mate if v[1] >= 1}
    assert reward == 2*sum(c >= 1 for _, c in selected)+len(endpoints)-6*len(completion)
    return dict(width=width, T=sorted(selected), M=matching,
                J=len(selected)+len(matching), reward=reward)


def main():
    short = [(0, 50, 50, 0, 0, 3), (45, 45, 0, 0, 12, 8)]
    long = [(9, 59, 50, 0, 9, 7), (20, 22, 0, 2, 4, 5),
            (41, 43, 2, 0, 1, 7), (42, 42, 0, 0, 0, 6)]
    short_board = actual_board(short)
    long_board = actual_board(long)
    assert short_board['reward'] == -1 and long_board['reward'] == 1
    assert short_board['J'] == 8 and long_board['J'] == 15
    cols = columns()
    best = -1000
    cases = 0
    for a in cols:
        s = successor((54, 4, 50), a)
        if s is None:
            continue
        for b in cols:
            t = successor(s, b)
            if t is not None and t[2] == 0:
                best = max(best, a[5]+b[5]-12)
                cases += 1
    assert best == -1
    result = dict(status='PASS', boundary=dict(O=54, F=4, R=50, index=3884),
                  short_completions_checked=cases, exact_short_reward=best,
                  short_attainer=short_board, four_column_obstruction=long_board,
                  failed_rule='Every closed four-column completion is dominated by a zero- or two-column completion.',
                  scope='Literal feasible boards and finite control. The exact short upper bound has a separate structural proof; this does not refute the half-area target.')
    (ROOT/'output/two-column-compression-obstruction.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in {'short_attainer','four_column_obstruction'}}))


if __name__ == '__main__':
    main()
