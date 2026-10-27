"""Independent exhaustive and weighted controls for whole-board extension."""
from itertools import product
from pathlib import Path
import json
import random

from zero_fee_extension import zero_fee_extension, extension_obstacle
from strip_tree_compensation import physical_state_linear
from check_strip_tree_compensation import partial_matchings
from check_general_square_ports import all_matchings, edge, grid, mates, physical_state, selected_feasible
from check_closed_ladder_compensation import direct_defect
from check_mixed_terminal_compensation import neighbours
from joint_frontier_compensation import solve_frontier

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')
ROOT = Path(__file__).resolve().parents[1]


def allowed_edges(board, p, t):
    holes = board-p-t
    return {edge(v, z) for v in board for z in neighbours(v) & board
            if (v not in t or z in holes) and (z not in t or v in holes)}


def check_result(board, m, t, result, allowed):
    matched = result['maximum_matching']
    mates(board, matched)
    assert matched <= allowed
    assert len(matched) == len(board)//2-result['defect']
    x, hood = result['hall_black'], result['hall_white']
    assert all(sum(v) % 2 == 0 for v in x)
    actual_hood = {v if z in x else z for v, z in allowed if v in x or z in x}
    assert hood == actual_hood and len(x)-len(hood) == result['defect']
    assert result['empty_paid_full_coverage_exists'] == (result['defect'] == 0)
    if not result['defect']:
        old = physical_state(board, m, matched, t)
        assert old['data']['counts'][0] == 0 and not old['paid']


def check_inequalities(board, m, n, t, defect, direct, allowed):
    # This older tagged-component implementation is independent of the
    # production traversal and of the augmenting-path maximum matcher.
    state = physical_state(board, m, n, t)
    a = state['data']['counts'][0]; paid = state['paid']
    changed = [path for path in state['data']['paths']
               if path['kind'] == 'TT' or (path['kind'] == 'TH' and path['M'])]
    k = sum(path['kind'] == 'TH' for path in changed)
    replacement = set(n)
    for path in changed:
        replacement.difference_update(path['N']); replacement.update(path['M'])
    mates(board, replacement)
    assert replacement <= allowed
    assert len(replacement) == len(board)//2-a-k
    assert a+k >= defect and k <= len(paid)
    assert a+len(paid) >= defect and 2*a+len(paid) >= direct
    return a, len(paid)


def exhaustive():
    rows = []
    for h, w in [(1, 2), (1, 4), (1, 6), (1, 8), (2, 2), (2, 3), (3, 2), (2, 4)]:
        board = grid(h, w)
        partial = [set(m) for m in partial_matchings(board)]
        full = [set(n) for n in all_matchings(board)]
        cache = {}; models = evaluations = balanced = nonfeasible = frontier = 0
        for m in partial:
            p = {v for e in m for v in e}; q = sorted(board-p)
            for bits in product((False, True), repeat=len(q)):
                t = {v for v, bit in zip(q, bits) if bit}
                allowed = allowed_edges(board, p, t)
                result = zero_fee_extension(h, w, m, t)
                check_result(board, m, t, result, allowed)
                key = frozenset(allowed)
                if key not in cache:
                    cache[key] = max(len(r) for r in partial if r <= allowed)
                assert result['defect'] == len(board)//2-cache[key]
                d = direct_defect(board, p, t)
                scores = [check_inequalities(board, m, n, t, result['defect'], d, allowed) for n in full]
                assert (min(scores) == (0, 0)) == (result['defect'] == 0)
                if len(t) == len(board-p-t):
                    assert (d == 0) == (result['defect'] == 0)
                    balanced += 1
                if len(board) <= 6:
                    r = solve_frontier(h, w, m, t)
                    assert (r['minimum_TT'], r['TH_cost']) == min(scores)
                    frontier += 1
                models += 1; evaluations += len(full)
                nonfeasible += not selected_feasible(p, t)
        row = dict(height=h, width=w, all_actual_matchings=len(partial),
                   all_actual_and_selected_models=models,
                   nonfeasible_models_included=nonfeasible,
                   full_auxiliary_evaluations=evaluations,
                   distinct_allowed_graphs=len(cache),
                   balanced_terminal_models=balanced, frontier_checks=frontier)
        rows.append(row)
        print(json.dumps(row), flush=True)
    return rows


def larger_general_controls():
    rng = random.Random(2026102703); rows = []
    for h, w in [(3, 4), (4, 4), (4, 6)]:
        board = grid(h, w); full = [set(n) for n in all_matchings(board)]
        edges = sorted({edge(v, z) for v in board for z in neighbours(v) & board})
        evaluations = 0
        for _ in range(32):
            rng.shuffle(edges); m = set(); p = set()
            for e in edges:
                if not set(e) & p and rng.random() < .35:
                    m.add(e); p.update(e)
            t = {v for v in board-p if rng.random() < .6}
            result = zero_fee_extension(h, w, m, t); allowed = allowed_edges(board, p, t)
            check_result(board, m, t, result, allowed)
            d = direct_defect(board, p, t)
            scores = [check_inequalities(board, m, n, t, result['defect'], d, allowed) for n in full]
            assert (min(scores) == (0, 0)) == (result['defect'] == 0)
            r = solve_frontier(h, w, m, t)
            assert (r['minimum_TT'], r['TH_cost']) == min(scores)
            evaluations += len(full)
        rows.append(dict(height=h, width=w, models=32, full_auxiliary_evaluations=evaluations, frontier_checks=32))
    return rows


def check_family(h, w, weights=None):
    f = extension_obstacle(h, w, weights); m, t, n = f['M'], f['T'], f['auxiliary']
    board = grid(h, w); p = {v for e in m for v in e}; holes = board-p-t
    occupied = p | t
    assert all(len(neighbours(v) & occupied) <= 1 for v in t)
    assert len(m)+len(t) == h*w//2-1 and len(holes) == len(t)+2
    dm = f['direct_matching']; mates(board, dm)
    assert all((a in t and b in holes) or (b in t and a in holes) for a, b in dm)
    assert len(dm) == len(t)
    allowed = allowed_edges(board, p, t)
    hood = {v if z in f['hall_set'] else z for v, z in allowed if v in f['hall_set'] or z in f['hall_set']}
    assert hood == f['hall_neighbours'] and len(f['hall_set'])-len(hood) == 1
    result = zero_fee_extension(h, w, m, t)
    assert result['defect'] == 1
    state = physical_state_linear(board, m, n, t)
    assert state['data']['counts'][0] == 0 and len(state['paid']) == 1
    assert state['paid'] <= {f['core_top'], f['core_left']}
    assert sum(f['weights'][e] for e in state['paid']) == f['exact_fee']
    if len(board) <= 100:
        old = physical_state(board, m, n, t)
        assert old['paid'] == state['paid'] and old['data']['counts'] == state['data']['counts']
    return f, result


def families():
    dimensions = [(4, 4), (4, 6), (6, 4), (6, 6), (4, 64), (64, 4), (20, 24), (40, 48), (128, 128)]
    rows = []
    for h, w in dimensions:
        f, result = check_family(h, w)
        rows.append(dict(height=h, width=w, J=len(f['M'])+len(f['T']), direct_defect=0,
                         whole_board_defect=result['defect'], witness_TT=0, witness_unit_fee=1))
    weighted = []
    for h, w in dimensions[:3]:
        base = extension_obstacle(h, w)
        full = [set(n) for n in all_matchings(grid(h, w))]
        for top, left in [(1, 7), (9, 2), (4, 4), (0, 5), (6, 0), (0, 0), (10**400+7, 10**400+3)]:
            weights = {e: (10**400+17 if top > 100 else 13) for e in base['M']}
            weights[base['core_top']] = top; weights[base['core_left']] = left
            f, result = check_family(h, w, weights)
            scores = []
            for n in full:
                s = physical_state(grid(h, w), f['M'], n, f['T'])
                a = s['data']['counts'][0]
                assert a == 0  # All selected terminals have the same parity.
                assert s['paid'] & {f['core_top'], f['core_left']}
                scores.append((a, sum(weights[e] for e in s['paid'])))
            assert min(scores) == (0, min(top, left))
            r = solve_frontier(h, w, f['M'], f['T'], weights)
            assert (r['minimum_TT'], r['TH_cost']) == min(scores)
            weighted.append(dict(height=h, width=w, top_weight=top, left_weight=left,
                                 exact_fee=min(top, left), full_auxiliary_evaluations=len(full),
                                 nonempty_paid_set_unavoidable=True, whole_board_defect=1))
    return dict(unit_families=rows, weighted_controls=weighted)


def validation_rejections():
    bad=[(0, 4, set(), set()), (3, 3, set(), set()), (2, 2, set(), {(3, 0)})]
    for args in bad:
        try: zero_fee_extension(*args)
        except ValueError: pass
        else: raise AssertionError(('invalid input accepted', args))
    for h, w in [(2, 4), (5, 4), (4, 3)]:
        try: extension_obstacle(h, w)
        except ValueError: pass
        else: raise AssertionError('invalid family dimensions accepted')
    return dict(invalid_dimension_or_selection_inputs_rejected=6)


def main():
    rows = exhaustive(); random_rows = larger_general_controls(); family = families()
    out = dict(status='PASS', exhaustive=rows, larger_general_controls=random_rows, families=family,
               input_controls=validation_rejections(),
               exhaustive_models=sum(r['all_actual_and_selected_models'] for r in rows),
               full_auxiliary_evaluations=sum(r['full_auxiliary_evaluations'] for r in rows+random_rows)+sum(r['full_auxiliary_evaluations'] for r in family['weighted_controls']),
               frontier_checks=sum(r['frontier_checks'] for r in rows+random_rows)+len(family['weighted_controls']),
               scope='All actual matchings and all T subsets on the eight listed even-area boards, including infeasible selections; every full N; independent partial-matching maxima, Hall witnesses, component replacement, larger seeded controls and exact weighted family witnesses.',
               proof_scope='The exact extension criterion, a+p lower bound and all-even-dimension weighted family have written proofs; finite checks validate implementations. No Lean or improved universal numerical coefficient is claimed.')
    (ROOT/'output/zero-fee-extension.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:out[k] for k in ['status','exhaustive_models','full_auxiliary_evaluations','frontier_checks']}), flush=True)


if __name__ == '__main__':
    main()
