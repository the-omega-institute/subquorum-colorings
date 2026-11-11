#!/usr/bin/env python3
"""Literal matching/path controls for residual attainment and route counts."""
from itertools import combinations
import json
from pathlib import Path
import random

from residual_hall_compensation import (bound, cheapest_non_direct_TH,
                                        complete_direct, pair, residual_data)
from check_residual_hall_compensation import (adjacent, check_flow, literal_paths,
                                             physical_arcs, score, serial, tilings)


def minimum_families(data, region, count, target):
    neighbours = {t for t in data['selected']
                  if any(adjacent(t, b) for b in region)}
    options = [(p, cost) for t in sorted(data['selected']-neighbours)
               for p, cost in literal_paths(data['board'], data['actual'], t,
                                             region, data['weights'])]

    def visit(start, chosen, used, cost):
        if len(chosen) == count:
            if cost == target:
                yield chosen
            return
        for i in range(start, len(options)):
            p, fee = options[i]
            if cost+fee <= target and not used.intersection(p):
                yield from visit(i+1, chosen+[p], used | set(p), cost+fee)

    return list(visit(0, [], set(), 0))


def auxiliary_on(paths):
    return {pair(p[i], p[i+1]) for p in paths for i in range(0, len(p)-1, 2)}


def unit_optimizer_tie():
    board = {(r, c) for r in range(18) for c in range(18)}
    origins = [(6, 6), (2, 0), (0, 10), (10, 12), (12, 2)]
    local = {pair((a, b), (a+1, b)) for a in [0, 3] for b in range(5)}
    local |= {pair((2, 0), (2, 1)), pair((2, 3), (2, 4))}
    actual = {pair((r+a, c+b), (r+x, c+y)) for r, c in origins
              for (a, b), (x, y) in local}
    occupied = {v for e in actual for v in e}
    holes = {(5, 10), (6, 5), (10, 11), (11, 6)}
    selected = {v for v in board-occupied if sum(v) % 2}-holes
    centres = {(r+2, c+2) for r, c in origins}
    data = residual_data(board, actual, selected, [])
    result = bound(data, centres, attempt_completion=False)
    assert (result['demand'], result['max_HH'], result['required_TH']) == (5, 4, 1)
    assert result['TH_flow']['cost'] == result['joint_assignment']['cost'] == 1
    assert all(sum(adjacent(t, b) for b in occupied) <= 1 for t in selected)
    good = [(8, 5), (8, 6), (8, 7), (8, 8)]
    bad = [(5, 8), (6, 8), (7, 8), (8, 8)]
    for path in [good, bad]:
        assert path[0] in selected and path[-1] in centres
        assert path in [p for p, cost in literal_paths(board, actual, path[0], centres,
                                                       data['weights']) if cost == 1]
    success, failure = complete_direct(data, [good]), complete_direct(data, [bad])
    assert success['auxiliary'] is not None and failure['auxiliary'] is None
    fee, paths = score(board, actual, success['auxiliary'], selected, data['weights'])
    assert fee == 1 and good in paths
    assert all(len(p) == 2 for p in paths if p[0] in selected-{good[0]})
    terminal_vertices = {v for path in paths for v in path}
    # Replace free closed components by doubled common actual edges.
    full_n = auxiliary_on(paths) | {e for e in actual if not set(e) & terminal_vertices}
    assert score(board, actual, full_n, selected, data['weights'])[0] == 1
    printed_paths = [good,
        [(5, 10), (4, 10), (3, 10), (3, 11), (4, 11), (4, 12), (3, 12), (2, 12)],
        [(6, 5), (6, 4), (5, 4), (4, 4), (4, 3), (4, 2)],
        [(10, 11), (10, 12), (11, 12), (11, 13), (10, 13), (10, 14), (11, 14),
         (11, 15), (10, 15), (10, 16), (11, 16), (12, 16), (12, 15), (12, 14)],
        [(11, 6), (12, 6), (13, 6), (14, 6), (14, 5), (14, 4)]]
    vertical_columns = {0: [8, 9, 17], 2: [7, 8, 9, 15, 16, 17],
        4: [5, 6, 7, 8, 9, 15, 16, 17], 6: [11, 12, 13, 14, 15, 16, 17],
        8: [0, 11, 12, 13, 14, 15, 16, 17], 9: [1], 10: [0, 2, 5, 17],
        11: [1, 7, 8, 9], 12: [0, 10, 11, 17], 13: [1, 7, 8, 9],
        14: [0, 10, 11, 17], 15: [1, 7, 8, 9, 12, 13, 14, 15, 16], 16: [0, 17]}
    horizontal_intervals = {0: [(0, 7), (15, 16)], 1: [(0, 7), (15, 16)],
        2: [(5, 6)], 3: [(5, 6)], 5: [(11, 14)], 7: [(0, 5)], 8: [(1, 4)],
        9: [(2, 5)], 10: [(3, 4)], 11: [(3, 4), (10, 11)],
        16: [(10, 11)], 17: [(1, 16)]}
    vertical = {pair((a, b), (a+1, b)) for a, cols in vertical_columns.items() for b in cols}
    horizontal = {pair((a, b), (a, b+1)) for a, runs in horizontal_intervals.items()
                  for left, right in runs for b in range(left, right+1, 2)}
    assert len(vertical) == 64 and len(horizontal) == 33
    used = {v for p in printed_paths for v in p}
    printed_n = auxiliary_on(printed_paths) | vertical | horizontal
    printed_n |= {e for e in actual if not set(e) & used}
    assert len(printed_n) == 162
    printed_fee, printed_terminal_paths = score(board, actual, printed_n, selected, data['weights'])
    assert printed_fee == 1
    assert all(p in printed_terminal_paths for p in printed_paths)
    chamber = {(r, c) for r in range(2) for c in range(10)}
    chamber |= {(r, c) for r in range(2, 6) for c in range(5, 10)}
    black = {v for v in chamber if not sum(v) % 2}
    white = chamber-black
    assert len(black) == len(white) == 20 and bad[0] in white
    assert {t for t in selected if any(adjacent(t, b) for b in black)} == white
    residual = residual_data(board, actual, selected, [bad])
    cut = failure['certificate']
    reached = {cut['vertices'][i] for i in cut['reachable']}
    hall_black = {b for b in residual['board'] if not sum(b) % 2 and b not in reached}
    p = {v for e in residual['actual'] for v in e}
    hall_white = {w for w in residual['board'] if sum(w) % 2 and
                  any(adjacent(w, b) and (w not in residual['selected'] or b not in p)
                      for b in hall_black)}
    assert len(hall_black) > len(hall_white)
    return dict(board=[18, 18], origins=origins, actual=actual, selected=selected,
                holes=holes, centres=centres, bad_path=bad, good_path=good,
                demand=5, max_HH=4, required_TH=1, physical_cost=1, true_optimum=1,
                full_auxiliary=printed_n, terminal_paths=printed_terminal_paths,
                printed_vertical_columns=vertical_columns,
                printed_horizontal_intervals=horizontal_intervals,
                chamber_black=black, chamber_white=white,
                bad_remainder_Hall_black=hall_black, bad_remainder_Hall_white=hall_white)


def cascade_controls():
    stats = dict(parameter_models=0, all_region_checks=0, forced_steps=0,
                 largest_r=32)
    witness = None
    for r in list(range(1, 9))+[16, 32]:
        board = {(0, c) for c in range(4*r)}
        paths = [[(0, 4*(r-i)+j) for j in [3, 2, 1, 0]] for i in range(1, r+1)]
        actual = {pair(p[1], p[2]) for p in paths}
        selected = {p[0] for p in paths}
        for mu in [1, 3, 1 << 400]:
            weights = {e: mu for e in actual}
            data = residual_data(board, actual, selected, [], weights)
            full = list(tilings(board))
            assert len(full) == 1
            assert full[0] == auxiliary_on(paths)
            fee, terminal_paths = score(board, actual, full[0], selected, weights)
            assert fee == r*mu and len(terminal_paths) == r
            assert all(len(p) == 4 for p in terminal_paths)
            assert cheapest_non_direct_TH(data)['cost'] == mu
            lifted = {(row, c) for row in [0, 1] for c in range(4*r)}
            hh = [[(1, 2*j), (1, 2*j+1)] for j in range(2*r)]
            lifted_data = residual_data(lifted, actual, selected, hh, weights)
            assert lifted_data['board'] == data['board']
            assert lifted_data['actual'] == data['actual']
            assert lifted_data['selected'] == data['selected']
            assert lifted_data['holes'] == set() and lifted_data['fixed_expense'] == 0
            retained_n = auxiliary_on(paths+hh)
            assert score(lifted, actual, retained_n, selected, weights)[0] == r*mu
            vertical_n = {pair((0, c), (1, c)) for c in range(4*r)}
            assert score(lifted, actual, vertical_n, selected, weights)[0] == 0
            occupied = {v for e in actual for v in e}
            assert all(sum(adjacent(t, v) for v in occupied) == 1 for t in selected)
            if r <= 8:
                black = sorted(data['black_q'])
                maximum = 0
                for mask in range(1 << r):
                    d = {b for i, b in enumerate(black) if mask & (1 << i)}
                    result = bound(data, d, attempt_completion=False)
                    expect = mu if paths[-1][-1] in d else 0
                    assert result['TH_flow']['cost'] == result['joint_assignment']['cost'] == expect
                    assert result['required_TH'] == int(expect != 0)
                    maximum = max(maximum, result['lower'])
                    stats['all_region_checks'] += 1
                assert maximum == mu
            steps = []
            for i, path in enumerate(paths):
                residual = residual_data(board, actual, selected, paths[:i], weights)
                assert residual['adjacency'][path[0]] == {path[1]}
                assert residual['adjacency'][path[2]] == {path[1], path[3]}
                result = bound(residual, residual['black_q'], attempt_completion=False)
                assert residual['selected']-result['direct_neighbours'] == {path[0]}
                assert result['required_TH'] == result['TH_flow']['value'] == 1
                assert result['TH_flow']['cost'] == mu and result['lower'] == (i+1)*mu
                steps.append(dict(fixed_paths=i, forced_path=path,
                                  fixed_expense=i*mu, next_expense=mu, lower=(i+1)*mu))
                stats['forced_steps'] += 1
            if r == 8 and mu == 1:
                witness = dict(board=[1, 4*r], actual=actual, selected=selected,
                               full_auxiliary=full[0], terminal_paths=paths,
                               initial_all_region_bound=1, true_optimum=r, forced_steps=steps,
                               rectangle_board=[2, 4*r], retained_HH=hh,
                               rectangle_retaining_auxiliary=retained_n,
                               rectangle_unrestricted_auxiliary=vertical_n,
                               rectangle_retaining_optimum=r, rectangle_unrestricted_optimum=0)
            stats['parameter_models'] += 1
    return stats, witness


def main():
    rng = random.Random(20261113)
    stats = dict(models=0, regions=0, physical_hypothesis_checks=0,
                 positive_hypothesis_regions=0, equality_cases=0,
                 nontrivial_equality_cases=0, optimal_families=0,
                 direct_remainder_comparisons=0, route_count_checks=0,
                 zero_path_regions=0, mixed_optimizer_regions=0)
    for h, w, count in [(2, 4, 80), (2, 6, 90), (3, 4, 100), (4, 4, 250)]:
        board = {(r, c) for r in range(h) for c in range(w)}
        full = list(tilings(board))
        for model in range(count):
            base = rng.choice(full)
            actual = {e for e in sorted(base) if rng.randrange(3)}
            occupied = {v for e in actual for v in e}
            white_q = {v for v in board-occupied if sum(v) % 2}
            selected = {v for v in sorted(white_q) if model % 2 == 0 or rng.randrange(3)}
            if h == w == 4 and model < 40:
                # A matched 3x3 ring forces a non-direct TH arrival at its centre.
                actual = {pair((1+a, 1+b), (1+x, 1+y)) for (a, b), (x, y) in
                          [((0, 0), (0, 1)), ((0, 2), (1, 2)),
                           ((2, 2), (2, 1)), ((2, 0), (1, 0))]}
                occupied = {v for e in actual for v in e}
                selected = {v for v in board-occupied if sum(v) % 2}
            scale = 1 << 400 if model % 53 == 0 else 1
            weights = {e: (rng.randrange(4) if model % 4 == 0 else rng.randrange(1, 5))*scale
                       for e in sorted(actual)}
            _, paths = score(board, actual, base, selected, weights)
            fixed = [] if h == w == 4 and model < 40 else rng.sample(paths, min(len(paths), model % 3))
            fixed_n = auxiliary_on(fixed)
            data = residual_data(board, actual, selected, fixed, weights)
            retained = []
            for n in full:
                if fixed_n <= n:
                    fee, ps = score(board, actual, n, selected, weights)
                    retained.append((n, fee, ps))
            assert retained
            exact = min(f for _, f, _ in retained)
            all_paths = [p for t in sorted(data['selected'])
                         for p, _ in literal_paths(data['board'], data['actual'], t,
                                                   data['black_q'], data['weights'])
                         if len(p) > 2]
            literal_eta = min((sum(data['weights'][pair(p[i], p[i+1])]
                                   for i in range(1, len(p)-1, 2))
                               for p in all_paths), default=None)
            flow = cheapest_non_direct_TH(data)
            eta = flow['cost'] if flow['value'] else None
            assert eta == literal_eta
            expected = {(a, b, c) for a, b, c in physical_arcs(data)
                        if not (a in data['selected'] and b in data['black_q'])}
            expected |= {('S', t, 0) for t in data['selected']}
            expected |= {(b, 'Z', 0) for b in data['black_q']}
            check_flow(flow, expected)
            stats['physical_hypothesis_checks'] += 1
            black = sorted(data['black_q'])
            regions = [{b} for b in black]
            regions += [set(rng.sample(black, min(2, len(black))))]
            for d in regions:
                result = bound(data, d, attempt_completion=False)
                s, cf = result['required_TH'], result['TH_flow']
                assert cf['value'] == s
                families = minimum_families(data, d, s, cf['cost'])
                assert families
                succeeds = []
                for family in families:
                    completion = complete_direct(data, family)
                    added = auxiliary_on(family)
                    excluded_sources = {p[0] for p in fixed+family}
                    brute = any(added <= n and all(len(p) == 2 for p in ps
                                if p[0] in selected-excluded_sources)
                                for n, _, ps in retained)
                    success = completion['auxiliary'] is not None
                    assert success == brute
                    if success:
                        assert score(board, actual, completion['auxiliary'], selected,
                                     weights)[0] == data['fixed_expense']+cf['cost']
                    succeeds.append(success)
                    stats['direct_remainder_comparisons'] += 1
                equality = exact == data['fixed_expense']+cf['cost']
                if eta is None or eta > 0:
                    assert equality == any(succeeds)
                    stats['positive_hypothesis_regions'] += 1
                    stats['equality_cases'] += int(equality)
                    stats['nontrivial_equality_cases'] += int(equality and s > 0)
                else:
                    stats['zero_path_regions'] += 1
                for _, fee, ps in retained:
                    m = sum(len(p) > 2 and p[0] in data['selected'] for p in ps)
                    assert m >= s
                    if eta is None:
                        assert m == s == 0 and fee == data['fixed_expense']
                    else:
                        assert fee >= data['fixed_expense']+cf['cost']+(m-s)*eta
                    stats['route_count_checks'] += 1
                if any(succeeds) and not all(succeeds):
                    stats['mixed_optimizer_regions'] += 1
                stats['optimal_families'] += len(families)
                stats['regions'] += 1
            stats['models'] += 1

    # A positive-weight case where all minimum C_s families fail to extend:
    # the endpoint assignment, not the physical one-path fee, is binding.
    board = {(r, c) for r in range(4) for c in range(10)}
    actual = {pair((r+a, c+b), (r+x, c+y)) for r, c in [(1, 1), (1, 7)]
              for (a, b), (x, y) in [((0, 0), (0, 1)), ((0, 2), (1, 2)),
                                     ((2, 2), (2, 1)), ((2, 0), (1, 0))]}
    occupied = {v for e in actual for v in e}
    selected = {v for v in board-occupied if sum(v) % 2}-{(0, 7)}
    weights = {e: 3 if min(v[1] for v in e) < 5 else 1 for e in actual}
    data = residual_data(board, actual, selected, [], weights)
    result = bound(data, {(2, 2), (2, 8)}, attempt_completion=False)
    assert result['required_TH'] == result['TH_flow']['cost'] == 1
    families = minimum_families(data, result['region'], 1, 1)
    assert families and all(complete_direct(data, p)['auxiliary'] is None for p in families)
    full = list(tilings(board))
    exact = None
    for n in full:
        fee, ps = score(board, actual, n, selected, weights)
        m = sum(len(p) > 2 and p[0] in selected for p in ps)
        assert fee >= 1+(m-1)
        exact = fee if exact is None else min(exact, fee)
    assert exact == 3
    stats['strict_nonattainment_case'] = dict(full_matchings=len(full),
                                             optimal_families=len(families),
                                             physical_bound=1, true_optimum=3)

    # Positive C_s equality can require another zero-cost non-direct TH path.
    board = {(r, c) for r in [0, 2] for c in range(4)}
    actual = {pair((r, 1), (r, 2)) for r in [0, 2]}
    selected = {(0, 3), (2, 3)}
    weights = {pair((0, 1), (0, 2)): 1, pair((2, 1), (2, 2)): 0}
    data = residual_data(board, actual, selected, [], weights)
    result = bound(data, {(0, 0)})
    ns = list(tilings(board))
    assert len(ns) == 1 and score(board, actual, ns[0], selected, weights)[0] == 1
    assert result['required_TH'] == result['TH_flow']['cost'] == 1
    assert result['completion']['auxiliary'] is None
    assert cheapest_non_direct_TH(data)['cost'] == 0
    assert all(sum(adjacent(t, v) for v in data['board']-data['black_q']-selected) == 1
               for t in selected)
    stats.update(status='PASS', zero_weight_counterexample=True,
                 integer_weight_bits=401,
                 scope='General proof plus independent literal paths and full matching controls; no Lean.')
    rectangle = unit_optimizer_tie()
    Path('output/attainment-optimizer-tie.json').write_text(json.dumps(serial(rectangle), indent=2)+'\n')
    stats['unit_rectangle_optimizer_tie'] = dict(board=[18, 18], true_optimum=1,
        physical_cost=1, rejected_path_cost=1,
        rejected_remainder_Hall_black=len(rectangle['bad_remainder_Hall_black']),
        rejected_remainder_Hall_white=len(rectangle['bad_remainder_Hall_white']))
    cascade_report, cascade = cascade_controls()
    stats['forced_cascade'] = cascade_report
    Path('output/forced-hall-cascade.json').write_text(json.dumps(serial(cascade), indent=2)+'\n')
    Path('output/positive-attainment-check.json').write_text(json.dumps(stats, indent=2)+'\n')
    print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
