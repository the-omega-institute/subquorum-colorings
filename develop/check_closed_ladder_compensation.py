"""Independent full-N checks of the direct closed-ladder construction."""
from pathlib import Path
import json
import random

from closed_ladder_compensation import construct_ladder, construct_closed_bands
from joint_frontier_compensation import solve_frontier
from check_strip_tree_compensation import partial_matchings
from check_general_square_ports import all_matchings, edge, grid, physical_state, selected_feasible

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')
ROOT = Path(__file__).resolve().parents[1]


def feasible_subsets(q, p, t=None):
    """Enumerate all feasible subsets; the condition is hereditary."""
    t = set() if t is None else t
    if not q:
        yield t
        return
    v, *rest = q
    yield from feasible_subsets(rest, p, t)
    if selected_feasible(p, t | {v}):
        yield from feasible_subsets(rest, p, t | {v})


def check_witness(h, w, m, t, result):
    # This older decomposition has an independent component implementation.
    state = physical_state(grid(h, w), m, result['auxiliary'], t)
    assert state['data']['counts'][0] == result['minimum_TT']
    assert not state['paid']
    assert all(len(path['vertices']) == 2 and not path['M']
               for path in state['data']['paths'] if path['kind'] == 'TH')
    return state


def direct_defect(board, p, t):
    """Standard augmenting paths in the direct T-to-H bipartite graph."""
    holes = board-p-t
    adjacency = {v: sorted(z for z in holes if sum(abs(x-y) for x, y in zip(v, z)) == 1)
                 for v in t}
    matched = {}

    def augment(v, seen):
        for z in adjacency[v]:
            if z in seen:
                continue
            seen.add(z)
            if z not in matched or augment(matched[z], seen):
                matched[z] = v
                return True
        return False

    for v in sorted(t):
        augment(v, set())
    return len(t)-len(matched)


def exhaustive():
    rows = []
    for w in range(1, 7):
        board = grid(2, w); full = [set(n) for n in all_matchings(board)]
        models = evaluations = exceptions = mixed = frontier_checks = 0
        blocks_tp = blocks_tt = 0
        for m in partial_matchings(board):
            p = {v for e in m for v in e}
            for t in feasible_subsets(sorted(board-p), p):
                result = construct_ladder(w, m, t)
                check_witness(2, w, m, t, result)
                defect = direct_defect(board, p, t)
                scores = []
                for n in full:
                    state = physical_state(board, m, n, t)
                    a, fee = state['data']['counts'][0], len(state['paid'])
                    assert 2*a+fee >= defect
                    scores.append((a, fee))
                expected = int(w % 2 == 1 and not m and t == {
                    (r, c) for r in range(2) for c in range(0, w, 2)})
                assert (result['minimum_TT'], result['TH_cost']) == min(scores) == (expected, 0)
                assert defect == 2*expected
                if w <= 4:
                    weights = {e: (7*sum(e[0])+sum(e[1])) % 11 for e in m}
                    frontier = solve_frontier(2, w, m, t, weights)
                    assert (frontier['minimum_TT'], frontier['TH_cost']) == (expected, 0)
                    frontier_checks += 1
                models += 1; evaluations += len(full); exceptions += expected
                mixed += any(a[0] == b[0] for a, b in m) and any(a[1] == b[1] for a, b in m)
                blocks_tp += sum(b['kind'] == 'TP-PH' for b in result['blocks'])
                blocks_tt += sum(b['kind'] == 'TT-HH' for b in result['blocks'])
        rows.append(dict(width=w, all_feasible_actual_models=models,
                         full_N_per_model=len(full), full_auxiliary_evaluations=evaluations,
                         exceptional_models=exceptions, mixed_direction_models=mixed,
                         frontier_checks=frontier_checks, used_TP_PH_blocks=blocks_tp,
                         used_TT_HH_blocks=blocks_tt, direct_defect_inequality_checked=True))
    return rows


def large_families():
    rows = []
    for repetitions in [1, 4, 16, 128, 1024]:
        w = 8*repetitions; m = set(); t = set()
        for c in range(0, w, 8):
            m.update((edge((0, c), (0, c+1)), edge((0, c+3), (1, c+3))))
            t.update(((1, c), (0, c+5), (1, c+5), (0, c+7)))
        for reflected in [False, True]:
            transform = (lambda v: (1-v[0], w-1-v[1])) if reflected else (lambda v: v)
            actual = {edge(transform(a), transform(b)) for a, b in m}
            selected = {transform(v) for v in t}
            result = construct_ladder(w, actual, selected)
            assert result['minimum_TT'] == result['TH_cost'] == 0
            assert not result['state']['paid'] and len(result['auxiliary']) == w
            assert len(result['blocks']) == 2*repetitions
            rows.append(dict(width=w, reflected=reflected, mixed_actual_edges=len(m),
                             selected=len(t), direct_TP_PH_blocks=repetitions,
                             direct_TT_HH_blocks=repetitions, minimum_TT=0, TH_fee=0,
                             traversal=result['state']['traversal_counts']))
    odd = []
    for w in [1, 3, 5, 129, 4097]:
        t = {(r, c) for r in range(2) for c in range(0, w, 2)}
        result = construct_ladder(w, set(), t)
        assert result['exceptional'] and result['minimum_TT'] == 1
        assert result['state']['data']['counts'] == (1, 0, w-1)
        odd.append(dict(width=w, minimum_TT=1, TH_fee=0, direct_TH=w-1))
    return dict(mixed_direction_families=rows, odd_exceptional_families=odd)


def band_controls():
    rng = random.Random(102727); rows = []
    for i in range(48):
        h, w = [(4, 4), (4, 6), (6, 2)][i % 3]
        board = grid(h, w)
        edges = sorted({edge(v, z) for v in board for z in [(v[0]+1, v[1]), (v[0], v[1]+1)]
                        if z in board and v[0]//2 == z[0]//2})
        rng.shuffle(edges); m = set(); p = set()
        for e in edges:
            if not set(e) & p and rng.random() < .5:
                m.add(e); p.update(e)
        t = set(); q = sorted(board-p); rng.shuffle(q)
        for v in q:
            if rng.random() < .9 and selected_feasible(p, t | {v}):
                t.add(v)
        result = construct_closed_bands(h, w, m, t)
        check_witness(h, w, m, t, result)
        weights = {e: (10**400+7 if i == 0 else rng.randrange(12)) for e in m}
        frontier = solve_frontier(h, w, m, t, weights)
        assert (frontier['minimum_TT'], frontier['TH_cost']) == (0, 0)
        scores = []
        for n in all_matchings(board):
            state = physical_state(board, m, n, t)
            scores.append((state['data']['counts'][0], sum(weights[e] for e in state['paid'])))
        assert min(scores) == (0, 0)
        rows.append(dict(height=h, width=w, actual_edges=len(m), selected=len(t),
                         full_auxiliary_evaluations=len(scores), minimum_TT=0, TH_fee=0))
    return rows


def seam_obstacle():
    m = {edge((0, 1), (0, 2)), edge((1, 1), (2, 1))}
    t = {(0, 0), (0, 3), (2, 0), (2, 3), (3, 1), (3, 3)}
    board = grid(4, 4); p = {v for e in m for v in e}; holes = board-p-t
    assert selected_feasible(p, t)
    subset = {(0, 0), (2, 0), (3, 1), (3, 3)}
    hood = {z for v in subset for z in holes if sum(abs(x-y) for x, y in zip(v, z)) == 1}
    assert hood == {(1, 0), (3, 0), (3, 2)} and len(subset) > len(hood)
    assert direct_defect(board, p, t) == 1
    witness = {edge(a, b) for a, b in [((0, 0), (0, 1)), ((0, 2), (1, 2)),
               ((0, 3), (1, 3)), ((1, 0), (2, 0)), ((1, 1), (2, 1)),
               ((2, 2), (2, 3)), ((3, 0), (3, 1)), ((3, 2), (3, 3))]}
    state = physical_state(board, m, witness, t)
    assert state['data']['counts'][0] == 0 and state['paid'] == {edge((0, 1), (0, 2))}
    scores = []
    for n in all_matchings(board):
        s = physical_state(board, m, n, t); scores.append((s['data']['counts'][0], len(s['paid'])))
    assert len(scores) == 36 and min(scores) == (0, 1)
    result = solve_frontier(4, 4, m, t)
    assert (result['minimum_TT'], result['TH_cost']) == (0, 1)
    try:
        construct_closed_bands(4, 4, m, t)
    except ValueError as e:
        assert 'closed inside' in str(e)
    else:
        raise AssertionError('An actual band-seam edge must not be silently removed')
    return dict(exact_minimum_TT=0, exact_unit_TH_fee=1, Hall_selected=sorted(subset),
                Hall_hole_neighbours=sorted(hood), exact_direct_Hall_defect=1,
                full_auxiliary_evaluations=36,
                closed_band_adapter_rejects_actual_seam=True,
                failure_scope='Unrestricted universal zero-fee extension fails; full coverage and the numerical target are not refuted.')


def main():
    rows = exhaustive(); families = large_families(); bands = band_controls()
    out = dict(status='PASS', exhaustive=rows,
               all_feasible_actual_models=sum(x['all_feasible_actual_models'] for x in rows),
               full_auxiliary_evaluations=sum(x['full_auxiliary_evaluations'] for x in rows),
               frontier_checks=sum(x['frontier_checks'] for x in rows),
               large_families=families, band_controls=bands, seam_obstacle=seam_obstacle(),
               scope='All feasible ladders of widths 1..6, all their full N; weighted frontier checks at widths 1..4; mixed-direction families, odd exceptions, closed bands and explicit seam Hall obstruction.',
               proof_scope='All-size direct compensation and unique odd exception have a written proof. Empty paid edge set works for all nonnegative weights. No new universal numerical coefficient or Lean claim.')
    (ROOT/'output/closed-ladder-compensation.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status', 'all_feasible_actual_models',
                                        'full_auxiliary_evaluations', 'frontier_checks']}))


if __name__ == '__main__':
    main()
