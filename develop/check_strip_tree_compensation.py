"""Independent physical enumerations for the strip/tree exact cost theorem."""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import random

from strip_tree_compensation import solve, solve_cycle_rank, word_lifts, _forest_labels
from check_general_square_ports import all_matchings, edge, grid, physical_state, selected_feasible
from check_unique_matching_hole_barrier import family as closed_family
from check_unbounded_hole_relay import family as relay_family

if not __debug__:
    raise RuntimeError('Run with assertions enabled')
ROOT = Path(__file__).resolve().parents[1]


def partial_matchings(vertices):
    if not vertices:
        yield frozenset(); return
    a = min(vertices); rest = vertices-{a}
    yield from partial_matchings(rest)
    for b in sorted(rest):
        if sum(abs(x-y) for x, y in zip(a, b)) == 1:
            for m in partial_matchings(rest-{b}):
                yield m | {edge(a, b)}


def colour_controls():
    rows = []
    for colours, max_h in [(2, 6), (3, 4)]:
        previous, current = 1, colours
        for h in range(max_h+1):
            if h == 0:
                expected = 1
            elif h == 1:
                expected = current
            else:
                previous, current = current, colours*current+colours*(colours-1)*previous
                expected = current
            vertices = sorted(grid(h, 2)); local = list(all_matchings(set(vertices)))
            accepted = 0; tested = 0
            for labels in product(range(colours), repeat=2*h):
                lab = dict(zip(vertices, labels)); word = [tuple(lab[r, c] for c in range(2)) for r in range(h)]
                exists = any(all(lab[a] == lab[b] for a, b in n) for n in local)
                assert exists == word_lifts(word)
                accepted += exists; tested += 1
            assert accepted == expected
            rows.append(dict(colours=colours, height=h, profiles=tested, liftable=accepted))
    return rows


def auxiliaries(h, w, cell_height):
    ids = [(r, c) for r in range(0, h, cell_height) for c in range(0, w, 2)]
    local = [list(all_matchings({(rr, cc) for rr in range(r, min(r+cell_height, h)) for cc in [c, c+1]})) for r, c in ids]
    return [set().union(*choices) for choices in product(*local)]


def rank(h, w, m, cell_height):
    cell = lambda v: (v[0]//cell_height, v[1]//2)
    ids = {cell(v) for v in grid(h, w)}; adjacency = {c: set() for c in ids}; cross = 0
    for a, b in m:
        ca, cb = cell(a), cell(b)
        if ca != cb:
            adjacency[ca].add(cb); adjacency[cb].add(ca); cross += 1
    unseen = set(ids); components = 0
    while unseen:
        todo = [unseen.pop()]; components += 1
        while todo:
            c = todo.pop()
            for z in adjacency[c] & unseen:
                unseen.remove(z); todo.append(z)
    return cross-len(ids)+components


def compare(h, w, m, t, cell_height, nlist, weights):
    best = None; covering = 0
    for n in nlist:
        state = physical_state(grid(h, w), m, n, t)
        if state['data']['counts'][0] == 0:
            fee = sum(weights[e] for e in state['paid'])
            best = fee if best is None else min(best, fee); covering += 1
    k = rank(h, w, m, cell_height)
    result = (solve(h, w, m, t, cell_height, weights) if k == 0 else
              solve_cycle_rank(h, w, m, t, cell_height, weights, max_rank=6))
    assert (None if result is None else result['cost']) == best
    if result is not None:
        assert result['auxiliary'] in nlist
        assert result['physical_cost'] == best
    return dict(feasible=best is not None, fee=best, covering_auxiliaries=covering, cycle_rank=k)


def exhaustive_controls(h, w, cell_height):
    board = grid(h, w); nlist = auxiliaries(h, w, cell_height)
    cases = 0; feasible = 0; positive = 0; ranks = Counter(); physical = 0
    for m in partial_matchings(board):
        p = {v for e in m for v in e}; q = sorted(board-p)
        for bits in range(1 << len(q)):
            t = {v for j, v in enumerate(q) if bits >> j & 1}
            if not selected_feasible(p, t):
                continue
            for weighted in [False, True]:
                weights = {e: (sum(sum(v) for v in e) % 5 if weighted else 1) for e in m}
                row = compare(h, w, m, t, cell_height, nlist, weights)
                cases += 1; feasible += row['feasible']; positive += row['fee'] not in [None, 0]
                ranks[row['cycle_rank']] += 1; physical += len(nlist)
    return dict(height=h, width=w, cell_height=cell_height, actual_weighted_models=cases,
                feasible=feasible, positive_cost=positive, full_auxiliary_evaluations=physical,
                cycle_ranks=dict(sorted(ranks.items())))


def random_controls():
    rng = random.Random(102731); rows = []
    for i in range(100):
        h, w, ch = [(4, 4, 4), (4, 6, 2), (6, 4, 3), (5, 4, 3)][i % 4]
        board = grid(h, w); edges = sorted({edge(v, z) for v in board for z in board if sum(abs(a-b) for a, b in zip(v, z)) == 1})
        rng.shuffle(edges); m = set(); p = set()
        for e in edges:
            if set(e) & p or rng.random() > .6:
                continue
            # Keep controlled cycle rank, while retaining genuine parallel edges.
            if rank(h, w, m | {e}, ch) <= (0 if i < 40 else 3):
                m.add(e); p |= set(e)
        t = set(); vertices = sorted(board-p); rng.shuffle(vertices)
        for v in vertices:
            if rng.random() < .65 and selected_feasible(p, t | {v}):
                t.add(v)
        weights = {e: rng.randrange(8) for e in sorted(m)}
        nlist = auxiliaries(h, w, ch); row = compare(h, w, m, t, ch, nlist, weights)
        row.update(height=h, width=w, cell_height=ch, full_auxiliaries=len(nlist)); rows.append(row)
    return rows


def relocated_family(w):
    _, oldm, oldt, _, _ = closed_family(w); m = set(oldm)
    assert solve(4, w, m, oldt, 4) is None
    t = oldt-{(3, w-2)} | {(3, w-3)}
    assert selected_feasible({v for e in m for v in e}, t)
    result = solve(4, w, m, t, 4); assert result is not None and result['cost'] == w//2
    # Explicit width-independent witness: fifth phase on left, all vertical on
    # right, horizontal top / vertical bottom in each interior 4-by-2 strip.
    n = {edge((0, 0), (0, 1)), edge((3, 0), (3, 1)),
         edge((1, 0), (2, 0)), edge((1, 1), (2, 1))}
    n |= {edge((r, c), (r+1, c)) for r in [0, 2] for c in [w-2, w-1]}
    for c in range(2, w-2, 2):
        n |= {edge((r, c), (r, c+1)) for r in [0, 1]}
        n |= {edge((2, cc), (3, cc)) for cc in [c, c+1]}
    state = physical_state(grid(4, w), m, n, t)
    top = {e for e in m if all(v[0] == 0 for v in e)}
    right = edge((1, w-2), (2, w-2)); expected = top | {right}
    assert state['data']['counts'][0] == 0 and state['paid'] == expected
    assert state['free'] == m-expected and not state['bad']
    weights = {e: sum(sum(v) for v in e) % 7 for e in m}
    weighted = solve(4, w, m, t, 4, weights)
    assert weighted is not None and weighted['cost'] == sum(weights[e] for e in expected)
    # Same final N2 as before: the moved selection swaps T/H on one TH edge.
    n2 = {edge((r, c), (r, c+1)) for r in range(4) for c in range(1, w-1, 2)}
    n2 |= {edge((r, c), (r+1, c)) for r in [0, 2] for c in [0, w-1]}
    final = physical_state(grid(4, w), m, n2, t)
    assert final['data']['counts'][0] == 0 and not final['paid']
    return dict(width=w, unchanged_selection_infeasible=True, one_batch_minimum_paid_M=w//2,
                explicit_optimal_paid_edges=len(expected), two_batch_paid_M=0,
                exact_optimal_paid_and_free_sets=True, nonnegative_weighted_formula=True)


def long_fee_family(k):
    d = relay_family(k); n = d['n']; m = set(d['M']); t = d['T']
    result = solve(n, n, m, t, n)
    assert result is not None and result['cost'] == k
    # Cell-confined completion using a horizontal central relay, not the prior
    # vertical relay. All other T are directly matched to adjacent H.
    auxiliary = {edge((r, c), (r, c+1)) for r in range(n) for c in range(0, n-2, 2)}
    auxiliary |= {edge((r, c), (r+1, c)) for c in [n-2, n-1]
                  for r in list(range(0, 2*k, 2))+list(range(2*k+1, 4*k, 2))}
    auxiliary |= {edge((r, n-2), (r, n-1)) for r in [2*k, n-1]}
    state = physical_state(d['board'], m, auxiliary, t)
    expected = {edge((2*k, c), (2*k, c+1)) for c in range(2*k+1, 4*k, 2)}
    assert len(expected) == k and state['paid'] == expected and state['data']['counts'][0] == 0
    return dict(k=k, side=n, exact_cell_confined_cost=k, cross_edges=result['cross_edges'],
                explicit_horizontal_relay_exact_paid_set=True)


def cycle_controls():
    m = {edge((0, 1), (0, 2)), edge((1, 1), (1, 2))}
    try:
        solve(2, 4, m, set(), 2)
    except ValueError:
        pass
    else:
        raise AssertionError('Parallel physical edges must not be merged into a forest')
    result = solve_cycle_rank(2, 4, m, set(), 2)
    assert result['cycle_rank'] == 1 and result['branches'] == 3 and result['cost'] == 0
    # Fix one feedback edge red: the two actual M edges become a forced red
    # P-only 4-cycle. The branch's label cost is 2, actual TH cost is 0.
    fixed = {max(m): 1}; branch = _forest_labels(2, 4, m, set(), 2, feedback=fixed)
    assert branch['cost'] == 2 and branch['physical_cost'] == 0
    return dict(parallel_edges_retained=True, cycle_rank=1, feedback_branches=3,
                constrained_coloured_cycle_label_cost=2, actual_TH_cost=0,
                global_cycle_normalization_deferred=True)


def main():
    words = colour_controls()
    exhaustive = [exhaustive_controls(2, 4, 2), exhaustive_controls(4, 2, 4)]
    randoms = random_controls()
    relocated = [relocated_family(w) for w in range(6, 106, 2)]
    longfees = [long_fee_family(k) for k in range(1, 17)]
    cycles = cycle_controls()
    out = dict(status='PASS', colour_profiles=sum(r['profiles'] for r in words),
               local_word_controls=words, exhaustive_controls=exhaustive,
               exhaustive_actual_weighted_models=sum(r['actual_weighted_models'] for r in exhaustive),
               exhaustive_full_auxiliary_evaluations=sum(r['full_auxiliary_evaluations'] for r in exhaustive),
               random_actual_models=len(randoms), random_controls=randoms,
               relocated_family_controls=relocated, long_fee_controls=longfees, cycle_control=cycles,
               scope='Exact physical same-colour ladder language, three-colour weighted model, forest messages and cycle-rank feedback; exact w/2 one-batch versus zero two-batch cost after one T relocation; inherited isolated-hole k family has new strip-confined horizontal optimal completion.',
               trust_boundary='All-size correctness and complexity are written proofs, finite controls validate implementation; no universal 5/6 or unrestricted polynomial solver claimed.')
    (ROOT/'output/strip-tree-compensation.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','colour_profiles','exhaustive_actual_weighted_models','exhaustive_full_auxiliary_evaluations','random_actual_models']}))


if __name__ == '__main__':
    main()
