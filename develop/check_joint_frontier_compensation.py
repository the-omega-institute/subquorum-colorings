"""Compare joint boundary labels with complete unrestricted physical N lists."""
from pathlib import Path
import json
import random

from joint_frontier_compensation import solve_frontier
from check_strip_tree_compensation import partial_matchings
from check_general_square_ports import all_matchings, edge, grid, physical_state, selected_feasible
from check_unique_matching_hole_barrier import family as closed_family

if not __debug__:
    raise RuntimeError('Run with assertions enabled')
ROOT = Path(__file__).resolve().parents[1]


def compare(h, w, m, t, weights, nlist):
    board = grid(h, w); scores = []
    for n in nlist:
        state = physical_state(board, m, n, t)
        scores.append((state['data']['counts'][0], sum(weights[e] for e in state['paid'])))
    best = min(scores) if scores else None
    result = solve_frontier(h, w, m, t, weights)
    assert (None if result is None else (result['minimum_TT'], result['TH_cost'])) == best
    if result is not None:
        assert result['auxiliary'] in nlist
        assert result['minimum_unpaid_selected'] == 2*best[0]
        assert result['full_coverage'] == (best[0] == 0)
    return result


def exhaustive():
    rows = []
    for h, w in [(2, 4), (4, 2), (2, 3), (3, 2), (1, 4), (4, 1)]:
        board = grid(h, w); nlist = [set(n) for n in all_matchings(board)]
        cases = evaluations = residuals = positive = feasible = 0
        for m in partial_matchings(board):
            p = {v for e in m for v in e}; q = sorted(board-p)
            for bits in range(1 << len(q)):
                t = {v for j, v in enumerate(q) if bits >> j & 1}
                for weighted in [False, True]:
                    weights = {e: (sum(sum(v) for v in e) % 5 if weighted else 1) for e in m}
                    result = compare(h, w, m, t, weights, nlist)
                    cases += 1; evaluations += len(nlist)
                    residuals += result['minimum_TT'] > 0; positive += result['TH_cost'] > 0
                    feasible += selected_feasible(p, t)
        rows.append(dict(height=h, width=w, actual_weighted_models=cases,
                         full_N_per_model=len(nlist), full_auxiliary_evaluations=evaluations,
                         positive_residual_models=residuals, positive_fee_models=positive,
                         models_satisfying_original_selection_condition=feasible))
    return rows


def random_controls():
    rng = random.Random(102753); rows = []
    for i in range(72):
        h, w = [(4, 4), (3, 4), (2, 6), (6, 2)][i % 4]
        board = grid(h, w)
        edges = sorted({edge(v, z) for v in board for z in [(v[0]+1, v[1]), (v[0], v[1]+1)] if z in board})
        rng.shuffle(edges); m = set(); p = set()
        for e in edges:
            if not set(e) & p and rng.random() < .6:
                m.add(e); p.update(e)
        t = set(); candidates = sorted(board-p); rng.shuffle(candidates)
        for v in candidates:
            if rng.random() < .8 and (i % 2 or selected_feasible(p, t | {v})):
                t.add(v)
        weights = {e: rng.randrange(8) for e in m}
        nlist = [set(n) for n in all_matchings(board)]
        result = compare(h, w, m, t, weights, nlist)
        rows.append(dict(height=h, width=w, full_auxiliaries=len(nlist),
                         residual_TT=result['minimum_TT'], TH_fee=result['TH_cost'],
                         peak_frontier_states=result['peak_states']))
    return rows


def unrestricted_family_controls():
    rows = []
    for w in [6, 8, 12, 24, 52, 104]:
        _, m, t, _, _ = closed_family(w)
        for relocated in [False, True]:
            tt = t-{(3, w-2)} | {(3, w-3)} if relocated else t
            result = solve_frontier(4, w, m, tt)
            assert result['minimum_TT'] == 0 and result['TH_cost'] == 0
            rows.append(dict(width=w, relocated=relocated, minimum_TT=0, exact_unrestricted_fee=0,
                             peak_frontier_states=result['peak_states']))
    return rows


def integer_and_guards():
    m = {edge((0, 1), (0, 2)), edge((1, 1), (2, 1))}
    t = {(0, 0), (0, 3), (2, 0), (2, 3), (3, 1), (3, 3)}
    weights = {edge((0, 1), (0, 2)): 10**400+7, edge((1, 1), (2, 1)): 10**500}
    result = compare(4, 4, m, t, weights, [set(n) for n in all_matchings(grid(4, 4))])
    assert result['minimum_TT'] == 0 and result['TH_cost'] == 10**400+7
    overhalf = {(0, 0), (1, 0), (0, 2), (1, 2)}
    assert selected_feasible(set(), overhalf)
    defect = solve_frontier(2, 3, set(), overhalf)
    assert defect['minimum_TT'] == 1 and defect['minimum_unpaid_selected'] == 2
    assert solve_frontier(3, 3, set(), set()) is None
    try:
        solve_frontier(2, 4, set(), set(), max_states=1)
    except RuntimeError:
        pass
    else:
        raise AssertionError('Resource guard must raise, not approximate')
    try:
        solve_frontier(4, 4, m, t, {e: -1 for e in m})
    except ValueError:
        pass
    else:
        raise AssertionError('Negative costs are outside the theorem')
    return dict(huge_positive_optimum_digits=401, huge_positive_optimum_exact=True,
                feasible_two_by_three_exact_residual_TT=1, odd_area_no_full_N=True,
                state_limit_raises=True, negative_weights_rejected=True)


def unbounded_bridgeless_family():
    rows = []
    for n in [2, 4, 8, 32, 128, 256]:
        w = 2*n
        m = {edge((r, c), (r, c+1)) for r in range(2) for c in range(1, w-1, 2)}
        t = {(0, 0), (0, w-1)}
        result = solve_frontier(2, w, m, t)
        assert result['minimum_TT'] == result['TH_cost'] == 0
        assert result['peak_states'] <= 8**2
        rows.append(dict(cells=n, global_and_bridge_block_rank=n-1,
                         minimum_TT=0, exact_fee=0, peak_states=result['peak_states'],
                         local_transitions=result['local_transitions']))
    return rows


def main():
    small = exhaustive(); randoms = random_controls()
    out = dict(status='PASS', exhaustive=small,
               exhaustive_actual_weighted_models=sum(x['actual_weighted_models'] for x in small),
               exhaustive_full_auxiliary_evaluations=sum(x['full_auxiliary_evaluations'] for x in small),
               random_actual_models=len(randoms), random_controls=randoms,
               unrestricted_families=unrestricted_family_controls(),
               integer_and_guard_controls=integer_and_guards(),
               unbounded_bridgeless_controls=unbounded_bridgeless_family(),
               scope='Exact unrestricted full-N lexicographic residual TT / actual TH fee via joint four-colour frontier. No cell restriction, global-rank assumption, or premature coloured-cycle refund.',
               trust_boundary='All-size label equivalence, frontier invariant and operation bound are written; these enumerations validate implementation. No new Lean formalization or universal numerical 5/6 improvement.')
    (ROOT/'output/joint-frontier-compensation.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','exhaustive_actual_weighted_models',
                                        'exhaustive_full_auxiliary_evaluations','random_actual_models']}))


if __name__ == '__main__':
    main()
