"""Independent small physical N enumeration and unbounded-rank bridge controls."""
from pathlib import Path
import json
import random

from bridge_block_compensation import solve_bridge_blocks, bridge_partition
from strip_tree_compensation import physical_state_linear
from check_strip_tree_compensation import auxiliaries, partial_matchings, compare, rank
from check_general_square_ports import edge, grid, selected_feasible

if not __debug__:
    raise RuntimeError('Run with assertions enabled')
ROOT = Path(__file__).resolve().parents[1]


def exhaustive():
    cases = evaluations = 0; positive = 0
    for h, w, ch in [(2, 4, 2), (4, 2, 4)]:
        board = grid(h, w); nlist = auxiliaries(h, w, ch)
        for m in partial_matchings(board):
            p = {v for e in m for v in e}; q = sorted(board-p)
            for bits in range(1 << len(q)):
                t = {v for j, v in enumerate(q) if bits >> j & 1}
                if not selected_feasible(p, t):
                    continue
                for weighted in [False, True]:
                    weights = {e: (sum(sum(v) for v in e) % 5 if weighted else 1) for e in m}
                    old = compare(h, w, m, t, ch, nlist, weights)
                    new = solve_bridge_blocks(h, w, m, t, ch, weights)
                    assert (None if new is None else new['cost']) == old['fee']
                    if new is not None:
                        assert new['auxiliary'] in nlist and new['cycle_rank'] == rank(h, w, m, ch)
                    cases += 1; evaluations += len(nlist); positive += old['fee'] not in (None, 0)
    return dict(actual_weighted_models=cases, full_auxiliary_evaluations=evaluations,
                positive_fee_models=positive)


def random_controls():
    rng = random.Random(102743); rows = []
    for j in range(64):
        h, w, ch = [(4, 6, 2), (4, 4, 4), (5, 4, 3), (6, 4, 3)][j % 4]
        board = grid(h, w)
        edges = sorted({edge((r, c), z) for r, c in board
                        for z in [(r+1, c), (r, c+1)] if z in board})
        rng.shuffle(edges); m = set(); p = set()
        for e in edges:
            if not set(e) & p and rng.random() < .65 and rank(h, w, m | {e}, ch) <= 4:
                m.add(e); p.update(e)
        t = set(); candidates = sorted(board-p); rng.shuffle(candidates)
        for v in candidates:
            if rng.random() < .7 and selected_feasible(p, t | {v}):
                t.add(v)
        weights = {e: rng.randrange(8) for e in m}
        nlist = auxiliaries(h, w, ch); old = compare(h, w, m, t, ch, nlist, weights)
        result = solve_bridge_blocks(h, w, m, t, ch, weights)
        assert (None if result is None else result['cost']) == old['fee']
        rows.append(dict(height=h, width=w, cell_height=ch, fee=old['fee'],
                         cycle_rank=old['cycle_rank'], full_auxiliaries=len(nlist),
                         block_ranks=None if result is None else result['block_cycle_ranks']))
    return rows


def cycle_chain(q):
    """Connected actual-M graph with q rank-one blocks and q-1 bridges."""
    w = 4*q
    m = {edge((r, 4*j+1), (r, 4*j+2)) for j in range(q) for r in [0, 1]}
    m |= {edge((2, 4*j+3), (2, 4*j+4)) for j in range(q-1)}
    t = {(3, 0), (0, w-1)}
    assert selected_feasible({v for e in m for v in e}, t)
    weights = {e: 10**400 if j % 2 else 0 for j, e in enumerate(sorted(m))}
    result = solve_bridge_blocks(4, w, m, t, 4, weights, max_block_rank=1)
    assert result is not None and result['cost'] == 0
    assert result['cycle_rank'] == q and result['max_block_cycle_rank'] == 1
    assert result['blocks'] == q and result['bridge_edges'] == q-1
    assert result['branch_evaluations'] == 9*q-6
    return dict(cycles=q, vertices=16*q, bridges=q-1, block_rank=1,
                conditional_feedback_evaluations=result['branch_evaluations'], exact_fee=0)


def integer_control():
    e0 = edge((0, 0), (1, 0)); e1 = edge((0, 1), (0, 2))
    result = solve_bridge_blocks(2, 4, {e0, e1}, {(0, 3), (1, 2)}, 2,
                                 {e0: 10**800, e1: 10**400+7})
    assert result['cost'] == 10**400+7
    parallel = {edge((0, 1), (0, 2)), edge((1, 1), (1, 2))}
    try:
        solve_bridge_blocks(2, 4, parallel, set(), 2, max_block_rank=0)
    except ValueError:
        pass
    else:
        raise AssertionError('Parallel physical edges must count towards block rank')
    return dict(huge_positive_optimum_exact=True, parallel_block_rank_guard=True)


def positive_bridge_control():
    # Discovered by search, then fixed here and independently exhausted over
    # all 256 physical N. The forced paid bridge leads towards a cyclic block.
    m = {edge(a, b) for a, b in [((0, 3), (0, 4)), ((0, 5), (0, 6)),
         ((1, 0), (1, 1)), ((1, 6), (2, 6)), ((1, 7), (2, 7)),
         ((2, 2), (3, 2)), ((2, 4), (2, 5)), ((3, 0), (3, 1)),
         ((3, 4), (3, 5)), ((3, 6), (3, 7))]}
    t = {(0, 0), (0, 2), (1, 3)}
    assert selected_feasible({v for e in m for v in e}, t)
    forced = edge((0, 3), (0, 4)); rows = []
    for fee in [1, 10**400+11]:
        weights = {e: 1 for e in m}; weights[forced] = fee
        old = compare(4, 8, m, t, 2, auxiliaries(4, 8, 2), weights)
        result = solve_bridge_blocks(4, 8, m, t, 2, weights)
        assert old['fee'] == result['cost'] == fee
        assert result['state']['paid'] == {forced}
        assert result['cycle_rank'] == 1 and result['bridge_edges'] == 2
        rows.append(dict(fee_digits=len(str(fee)), full_auxiliaries=256,
                         exact_unique_paid_bridge=True, cycle_rank=1, bridges=2))
    return rows


def bridgeless_rank_barrier(n):
    # All-n physical obstruction to a bounded-rank inference from feasibility
    # or half-area equality. Do NOT run exponential conditioning at large n.
    w = 2*n; board = grid(2, w)
    m = {edge((r, c), (r, c+1)) for r in range(2) for c in range(1, w-1, 2)}
    t = {(0, 0), (0, w-1)}; p = {v for e in m for v in e}
    assert selected_feasible(p, t) and len(m)+len(t) == len(board)//2
    auxiliary = {edge((0, c), (1, c)) for c in range(w)}
    state = physical_state_linear(board, m, auxiliary, t)
    assert state['data']['counts'] == (0, 0, 2) and state['free'] == m
    cells = list(range(n)); adj = {c: [] for c in cells}
    for e in m:
        a, b = e; ca, cb = a[1]//2, b[1]//2
        adj[ca].append((cb, e, a, b)); adj[cb].append((ca, e, b, a))
    bridges, _, blocks = bridge_partition(cells, adj)
    assert not bridges and len(blocks) == 1
    assert len(m)-n+1 == n-1
    if n <= 4:
        result = solve_bridge_blocks(2, w, m, t, 2)
        assert result['cost'] == 0 and result['max_block_cycle_rank'] == n-1
    if n > 2:
        try:
            solve_bridge_blocks(2, w, m, t, 2, max_block_rank=1)
        except ValueError:
            pass
        else:
            raise AssertionError('Adjacent rank-one cycles share cells and form one bridge block')
    return dict(cells=n, vertices=4*n, global_and_block_rank=n-1, bridges=0,
                exact_half_area=True, explicit_zero_fee=True)


def main():
    small = exhaustive(); randoms = random_controls()
    chains = [cycle_chain(q) for q in [1, 2, 4, 16, 64, 256]]
    out = dict(status='PASS', exhaustive=small, random_actual_models=len(randoms),
               random_controls=randoms, connected_cycle_chains=chains,
               integer_and_parallel_controls=integer_control(),
               positive_bridge_controls=positive_bridge_control(),
               post_submission_bridgeless_rank_barrier=[bridgeless_rank_barrier(n)
                   for n in [2, 3, 4, 8, 32, 256]],
               scope='Exact same-colour physical strip fee via bridge-block messages; exponential only in each local block rank, with global normalization.',
               trust_boundary='All-size proof and complexity bound are written; finite matching enumerations and chain controls test the implementation. No new Lean declaration or universal 5/6 improvement.')
    (ROOT/'output/bridge-block-compensation.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status', 'exhaustive', 'random_actual_models', 'connected_cycle_chains']}))


if __name__ == '__main__':
    main()
