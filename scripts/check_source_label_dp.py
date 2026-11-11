#!/usr/bin/env python3
"""Independent literal full-N enumeration controls for binary-label optimization."""
from itertools import product
import json
from pathlib import Path
import random

from source_label_dp import complete_ladder_zero_fee, optimize_th, pair
from check_residual_hall_compensation import adjacent, score, serial, tilings


def verify(board, actual, selected, weights, retained, result, expected):
    assert result['optimum'] == expected, (result['optimum'], expected)
    stats = result['stats']
    assert stats['max_frontier'] <= stats['frontier_bound']
    assert stats['max_states'] <= 4**stats['max_frontier']
    if expected is None:
        assert 'auxiliary' not in result
        return
    auxiliary, labels = result['auxiliary'], result['labels']
    assert len(auxiliary)*2 == len(board) and {v for e in auxiliary for v in e} == board
    assert all(adjacent(*e) for e in auxiliary)
    assert set(labels) == board and set(labels.values()) <= {0, 1}
    p = {v for e in actual for v in e}
    white_q = {v for v in board-p if sum(v) % 2}
    assert all(labels[t] == 1 for t in selected)
    assert all(labels[w] == 0 for w in white_q-selected)
    assert all(labels[a] == labels[b] for a, b in actual | auxiliary)
    assert sum(weights[e]*labels[e[0]] for e in actual) == expected
    assert score(board, actual, auxiliary, selected, weights)[0] == expected
    fixed_n = {pair(p[i], p[i+1]) for p in retained for i in range(0, len(p)-1, 2)}
    assert fixed_n <= auxiliary


def colour_enumeration(board, actual, selected, weights):
    """Independent reduction check: enumerate pair/black labels then tile each colour."""
    occupied = {v for e in actual for v in e}
    white_q = {v for v in board-occupied if sum(v) % 2}
    blocks = [set(e) for e in sorted(actual)]+[{v} for v in sorted(board-occupied-white_q)]
    best = None
    for bits in product((0, 1), repeat=len(blocks)):
        one = selected | {v for block, bit in zip(blocks, bits) if bit for v in block}
        if next(tilings(one), None) is None or next(tilings(board-one), None) is None:
            continue
        value = sum(weights[e] for e in actual if e[0] in one)
        best = value if best is None else min(best, value)
    return best


def small_models():
    rng = random.Random(2026111201)
    stats = dict(models=0, full_matching_scores=0, feasible_selected_models=0,
                 infeasible_retaining=0, scan_controls=0, value_only_controls=0,
                 colour_enumerations=0, max_frontier=0, max_states=0)
    for h, w, count in [(2, 2, 60), (2, 4, 140), (2, 6, 140), (3, 4, 150),
                         (4, 4, 180), (4, 6, 70), (4, 8, 8), (4, 10, 2)]:
        board = {(r, c) for r in range(h) for c in range(w)}
        ns = list(tilings(board))
        for model in range(count):
            base = rng.choice(ns)
            actual = {e for e in sorted(base) if rng.randrange(3)}
            p = {v for e in actual for v in e}
            white_q = {v for v in board-p if sum(v) % 2}
            allowed = {v for v in white_q if sum(adjacent(v, b) for b in p) <= 1}
            selected = {v for v in sorted(allowed if model % 2 else white_q) if rng.randrange(2)}
            scale = 1 << 400 if model % 23 == 0 else 1
            weights = {e: rng.randrange(5)*scale for e in sorted(actual)}
            paths = score(board, actual, base, selected, weights)[1]
            retained = rng.sample(paths, min(len(paths), model % 3)) if model % 4 else []
            if model % 11 == 0 and paths:
                # A physical path need not extend; find one using a different N,
                # then retain a disjoint path from the base when available.
                other = score(board, actual, rng.choice(ns), selected, weights)[1]
                retained = [rng.choice(other)] if other else []
                used = {v for path in retained for v in path}
                retained += next(([path] for path in paths if not set(path) & used), [])
            fixed = {pair(path[i], path[i+1]) for path in retained for i in range(0, len(path)-1, 2)}
            expected = None
            for n in ns:
                if fixed <= n:
                    fee = score(board, actual, n, selected, weights)[0]
                    stats['full_matching_scores'] += 1
                    expected = fee if expected is None else min(expected, fee)
            result = optimize_th(board, actual, selected, weights, retained)
            verify(board, actual, selected, weights, retained, result, expected)
            stats['infeasible_retaining'] += expected is None
            stats['max_frontier'] = max(stats['max_frontier'], result['stats']['max_frontier'])
            stats['max_states'] = max(stats['max_states'], result['stats']['max_states'])
            stats['feasible_selected_models'] += selected <= allowed
            stats['models'] += 1
            if model % 13 == 0:
                for scan in ('rows', 'columns'):
                    control = optimize_th(board, actual, selected, weights, retained, scan=scan)
                    verify(board, actual, selected, weights, retained, control, expected)
                    stats['scan_controls'] += 1
                value = optimize_th(board, actual, selected, weights, retained, witness=False)
                assert value['optimum'] == expected and 'auxiliary' not in value
                assert value['stats']['parent_entries'] == 0
                stats['value_only_controls'] += 1
            if model < 12 and h*w <= 12 and not retained:
                assert colour_enumeration(board, actual, selected, weights) == expected
                stats['colour_enumerations'] += 1
    return stats


def controls():
    report, witnesses = [], []
    for r in (1, 2, 4, 8, 32, 128):
        board = {(a, b) for a in (0, 1) for b in range(4*r)}
        paths = [[(0, 4*i+j) for j in (3, 2, 1, 0)] for i in range(r)]
        actual = {pair(p[1], p[2]) for p in paths}
        selected = {p[0] for p in paths}
        hh = [[(1, 2*j), (1, 2*j+1)] for j in range(2*r)]
        for mu in (1, 3, 1 << 400):
            weights = {e: mu for e in actual}
            for retained, expected in (([], 0), (hh, r*mu)):
                result = optimize_th(board, actual, selected, weights, retained)
                verify(board, actual, selected, weights, retained, result, expected)
                report.append(dict(r=r, mu=mu, retained_HH=bool(retained),
                                   optimum=expected, stats=result['stats']))
                if r == 4 and mu == 1:
                    witnesses.append(dict(r=r, board=board, actual=actual, selected=selected,
                                          retained=retained, weights=sorted(weights.items()), result=result))
    # Perfect actual matchings consist solely of closed components, all free.
    board = {(r, c) for r in range(4) for c in range(6)}
    actual = next(tilings(board))
    weights = {e: 1 << 400 for e in actual}
    verify(board, actual, set(), weights, [], optimize_th(board, actual, set(), weights), 0)
    verify(board, set(), {v for v in board if sum(v) % 2}, {}, [],
           optimize_th(board, set(), {v for v in board if sum(v) % 2}, {}), 0)
    board = {(0, 0), (0, 1), (0, 2), (2, 1)}
    verify(board, set(), set(), {}, [], optimize_th(board, set(), set(), {}), None)
    board = {(r, c) for r in (0, 1) for c in range(3)}
    retained = [[(0, 1), (0, 0)], [(1, 2), (1, 1)]]
    verify(board, set(), set(), {}, retained,
           optimize_th(board, set(), set(), {}, retained), None)
    verify(set(), set(), set(), {}, [], optimize_th(set(), set(), set(), {}), 0)
    # A negative paid closed component would invalidate the reduction; reject it.
    failures = 0
    for args in [({(0, 0), (0, 1)}, {((0, 0), (0, 1))}, set(), {((0, 0), (0, 1)): -1}),
                 ({(0, 0), (0, 1)}, set(), {(2, 1)}, {}),
                 ({(0, 0), (0, 1)}, {((0, 0), (0, 1))}, {(0, 1)}, {})]:
        try:
            optimize_th(*args)
        except ValueError:
            failures += 1
    assert failures == 3
    return dict(cascades=report, boundary_controls=5, invalid_input_controls=failures), witnesses


def ladder_controls():
    def partials(board):
        if not board:
            yield set()
            return
        a = min(board)
        yield from partials(board-{a})
        for b in sorted(board-{a}):
            if adjacent(a, b):
                for rest in partials(board-{a, b}):
                    yield rest | {pair(a, b)}
    report = dict(exhaustive_actual_matchings=0, selected_subsets_covered=0,
                  dp_controls=0, transformed_controls=0, widths=[])
    for n in range(1, 9):
        board = {(r, c) for r in (0, 1) for c in range(n)}
        count, covered = 0, 0
        for actual in partials(board):
            occupied = {v for e in actual for v in e}
            selected = {v for v in board-occupied if sum(v) % 2 and
                        sum(adjacent(v, b) for b in occupied) <= 1}
            weights = {e: (1 << 400) if count % 7 == 0 else count % 5 for e in actual}
            result = complete_ladder_zero_fee(board, actual, selected, weights)
            assert score(board, actual, result['auxiliary'], selected, weights)[0] == 0
            # All subsets of maximal feasible T inherit this same zero certificate.
            assert all(next(w for e in result['auxiliary'] if t in e for w in e if w != t)
                       not in occupied for t in selected)
            covered += 1 << len(selected)
            if count % 101 == 0:
                exact = optimize_th(board, actual, selected, weights)
                verify(board, actual, selected, weights, [], exact, 0)
                report['dp_controls'] += 1
                for transposed in (False, True):
                    transform = ((lambda v: (v[1]+3, v[0]+5)) if transposed else
                                 (lambda v: (v[0]+3, v[1]+5)))
                    b = {transform(v) for v in board}
                    m = {pair(*map(transform, e)) for e in actual}
                    t = {transform(v) for v in selected}
                    wt = {pair(*map(transform, e)): w for e, w in weights.items()}
                    result = complete_ladder_zero_fee(b, m, t, wt)
                    assert score(b, m, result['auxiliary'], t, wt)[0] == 0
                    report['transformed_controls'] += 1
            count += 1
        report['widths'].append(dict(n=n, actual_matchings=count, selected_subsets=covered))
        report['exhaustive_actual_matchings'] += count
        report['selected_subsets_covered'] += covered
    # Removing the occupied-neighbour condition gives a positive-cost ladder.
    board = {(r, c) for r in (0, 1) for c in range(3)}
    white = [next((r, c) for r in (0, 1) if (r+c) % 2) for c in range(3)]
    black = [next((r, c) for r in (0, 1) if not (r+c) % 2) for c in range(3)]
    actual = {pair(white[0], black[1]), pair(white[1], black[2])}
    selected = {white[2]}
    weights = {e: 1 for e in actual}
    result = optimize_th(board, actual, selected, weights)
    verify(board, actual, selected, weights, [], result, 1)
    try:
        complete_ladder_zero_fee(board, actual, selected, weights)
    except ValueError:
        report['hypothesis_counterexample'] = True
    else:
        raise AssertionError('Invalid selected vertices accepted')
    return report


def masked_controls():
    rng = random.Random(2026111202)
    report = dict(models=0, infeasible_models=0, full_matching_scores=0)
    full = {(r, c) for r in range(4) for c in range(4)}
    for model in range(180):
        whites = sorted(v for v in full if sum(v) % 2)
        blacks = sorted(full-set(whites))
        k = rng.randrange(1, 8)
        board = full-set(rng.sample(whites, k))-set(rng.sample(blacks, k))
        ns = list(tilings(board))
        # Use arbitrary physical matchings even when the board cannot be tiled.
        remaining, actual = set(board), set()
        for a in sorted(board):
            options = sorted(b for b in remaining-{a} if adjacent(a, b))
            if a in remaining and options and rng.randrange(2):
                b = rng.choice(options)
                actual.add(pair(a, b))
                remaining -= {a, b}
        selected = {v for v in sorted(remaining) if sum(v) % 2 and rng.randrange(2)}
        weights = {e: rng.randrange(4) for e in actual}
        fees = [score(board, actual, n, selected, weights)[0] for n in ns]
        expected = min(fees, default=None)
        verify(board, actual, selected, weights, [],
               optimize_th(board, actual, selected, weights), expected)
        report['models'] += 1
        report['infeasible_models'] += expected is None
        report['full_matching_scores'] += len(ns)
    return report


def three_row_controls():
    report, witness = [], None
    for r in (1, 2, 3, 8, 32, 128):
        board = {(a, b) for a in range(3) for b in range(6*r)}
        local_m = [((0, 1), (0, 2)), ((0, 0), (1, 0)),
                   ((1, 2), (2, 2)), ((2, 0), (2, 1))]
        local_n = [((0, 3), (0, 2)), ((0, 1), (1, 1)),
                   ((0, 0), (1, 0)), ((1, 2), (2, 2)), ((2, 0), (2, 1)),
                   ((2, 3), (1, 3)), ((0, 4), (0, 5)),
                   ((1, 4), (1, 5)), ((2, 4), (2, 5))]
        actual = {pair((a, b+6*i), (c, d+6*i)) for i in range(r) for (a, b), (c, d) in local_m}
        auxiliary = {pair((a, b+6*i), (c, d+6*i)) for i in range(r) for (a, b), (c, d) in local_n}
        p = {v for e in actual for v in e}
        selected = {v for v in board-p if sum(v) % 2}
        assert all(sum(adjacent(v, w) for w in p) <= 1 for v in selected)
        centres = {(1, 6*i+1) for i in range(r)}
        assert centres <= board-p
        assert all(all(w in p for w in board if adjacent(c, w)) for c in centres)
        for mu in (0, 1, 1 << 400):
            weights = {e: mu for e in actual}
            assert score(board, actual, auxiliary, selected, weights)[0] == r*mu
            result = optimize_th(board, actual, selected, weights)
            verify(board, actual, selected, weights, [], result, r*mu)
            report.append(dict(r=r, mu=mu, optimum=r*mu, stats=result['stats']))
            if r == 2 and mu == 1:
                witness = dict(board=board, actual=actual, selected=selected,
                               auxiliary=auxiliary, centres=centres, optimum=r)
    return report, witness


def main():
    report = small_models()
    report['controls'], witnesses = controls()
    report['ladder'] = ladder_controls()
    report['masked'] = masked_controls()
    report['three_rows'], three_rows = three_row_controls()
    Path('output/source-label-dp-check.json').write_text(json.dumps(report, indent=2)+'\n')
    Path('output/source-label-dp-witnesses.json').write_text(json.dumps(serial(witnesses), indent=2)+'\n')
    Path('output/three-row-positive-expense.json').write_text(json.dumps(serial(three_rows), indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
