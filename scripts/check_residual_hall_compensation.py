#!/usr/bin/env python3
"""Full-matching and literal-path controls for the residual theorem."""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import random

from residual_hall_compensation import bound, pair, residual_data


def adjacent(a, b):
    return sum(abs(x-y) for x, y in zip(a, b)) == 1


def tilings(board):
    if not board:
        yield set()
        return
    a = min(board)
    for b in sorted(board-{a}):
        if adjacent(a, b):
            for rest in tilings(board-{a, b}):
                yield rest | {pair(a, b)}


def score(board, actual, auxiliary, selected, weights):
    assert len(auxiliary)*2 == len(board)
    assert {v for e in auxiliary for v in e} == board
    assert all(adjacent(*e) for e in auxiliary)
    m = {v: w for e in actual for v, w in (e, e[::-1])}
    n = {v: w for e in auxiliary for v, w in (e, e[::-1])}
    paths, total = [], 0
    for source in sorted(v for v in board-m.keys() if sum(v) % 2):
        path, fee, v = [source], 0, source
        while True:
            v = n[v]
            path.append(v)
            if v not in m:
                break
            if source in selected:
                fee += weights[pair(v, m[v])]
            v = m[v]
            path.append(v)
        assert len(path) == len(set(path))
        paths.append(path)
        total += fee
    return total, paths


def literal_paths(board, actual, source, sinks, weights):
    mate = {v: w for e in actual for v, w in (e, e[::-1])}
    result = []

    def visit(path, fee):
        a = path[-1]
        for b in sorted(board-set(path)):
            if not adjacent(a, b) or pair(a, b) in actual:
                continue
            if b not in mate:
                if b in sinks:
                    result.append((path+[b], fee))
            elif mate[b] not in path:
                visit(path+[b, mate[b]], fee+weights[pair(b, mate[b])])
    visit([source], 0)
    return result


def literal_pack(data, sources, sinks, count, free=False):
    vertices = {v: i for i, v in enumerate(sorted(data['board']))}
    options = []
    for source in sorted(sources):
        options.append([(sum(1 << vertices[v] for v in p), 0 if free else cost)
                        for p, cost in literal_paths(data['board'], data['actual'],
                                                     source, sinks, data['weights'])])

    @lru_cache(None)
    def search(i, used, left):
        if left == 0:
            return 0
        if len(options)-i < left:
            return None
        best = search(i+1, used, left)
        for mask, cost in options[i]:
            if not mask & used:
                tail = search(i+1, used | mask, left-1)
                if tail is not None and (best is None or cost+tail < best):
                    best = cost+tail
        return best
    return search(0, 0, count)


def physical_arcs(data, free=False):
    result = set()
    for a in data['board']:
        for b in data['board']:
            if sum(a) % 2 and adjacent(a, b) and pair(a, b) not in data['actual']:
                result.add((a, b, 0))
    for e in data['actual']:
        black = next(v for v in e if not sum(v) % 2)
        white = next(v for v in e if sum(v) % 2)
        result.add((black, white, 0 if free else data['weights'][e]))
    return result


def check_flow(result, expected):
    labels = result['vertices']
    edges = result['arcs']
    assert {(labels[a], labels[b], c) for a, b, c in edges} == expected
    used = set(result['used'])
    assert len(used) == len(result['used']) and all(0 <= i < len(edges) for i in used)
    balance = [0]*len(labels)
    residual = []
    for i, (a, b, c) in enumerate(edges):
        if i in used:
            balance[a] -= 1
            balance[b] += 1
            residual.append((b, a, -c))
        else:
            residual.append((a, b, c))
    assert balance[result['source']] == -result['value']
    assert balance[result['sink']] == result['value']
    assert all(v == 0 for i, v in enumerate(balance)
               if i not in {result['source'], result['sink']})
    assert result['cost'] == sum(edges[i][2] for i in used)
    pot = result['potentials']
    assert len(pot) == len(labels)
    assert all(c+pot[a]-pot[b] >= 0 for a, b, c in residual)
    reached = {result['source']}
    while True:
        new = reached | {b for a, b, _ in residual if a in reached}
        if new == reached:
            break
        reached = new
    assert reached == set(result['reachable'])
    if result['value'] < result['limit']:
        assert result['sink'] not in reached
        assert sum(a in reached and b not in reached for a, b, _ in edges) == result['value']


def check_networks(data, result, literal=False):
    d = result['region']
    f = {t for t in data['selected'] if any(adjacent(t, b) for b in d)}
    assert f == result['direct_neighbours']
    outside = data['selected']-f
    for name, sources, free in [('HH_flow', data['holes'], True),
                                 ('TH_flow', outside, False)]:
        expected = physical_arcs(data, free)
        expected |= {('S', t, 0) for t in sources} | {(b, 'Z', 0) for b in d}
        check_flow(result[name], expected)
    # Independent Bellman--Ford, on the literal physical graph, for assignment costs.
    expected = {('S', t, 0) for t in outside | data['holes']} | {(b, 'Z', 0) for b in d}
    arcs = physical_arcs(data)
    for t in outside | data['holes']:
        dist = {t: 0}
        for _ in range(len(data['board'])-1):
            old = dict(dist)
            for a, b, c in arcs:
                if a in old and (b not in dist or old[a]+c < dist[b]):
                    dist[b] = old[a]+c
            if dist == old:
                break
        expected |= {(t, b, 0 if t in data['holes'] else dist[b]) for b in d if b in dist}
    check_flow(result['joint_assignment'], expected)
    if literal:
        limit = min(len(data['holes']), len(d))
        h = max(k for k in range(limit+1)
                if literal_pack(data, data['holes'], d, k, free=True) is not None)
        assert h == result['max_HH']
        assert literal_pack(data, outside, d, result['required_TH']) == (
            result['TH_flow']['cost'] if result['TH_flow']['value'] == result['required_TH'] else None)


def small_controls():
    rng = random.Random(20261112)
    stats = dict(models=0, regions=0, full_matching_scores=0, literal_path_controls=0,
                 exact_completions=0, infeasible_relaxations=0, feasible_selected_models=0,
                 joint_stronger=0, physical_stronger=0)
    for height, width, count in [(2, 4, 90), (2, 6, 90), (3, 4, 70), (4, 4, 70), (4, 6, 24)]:
        board = {(r, c) for r in range(height) for c in range(width)}
        ns = list(tilings(board))
        for model in range(count):
            base = ns[rng.randrange(len(ns))]
            actual = {e for e in sorted(base) if rng.randrange(3) != 0}
            p = {v for e in actual for v in e}
            white_q = {v for v in board-p if sum(v) % 2}
            allowed = {t for t in white_q if sum(adjacent(t, b) for b in p) <= 1}
            selected = {v for v in sorted(allowed if model % 2 else white_q) if rng.randrange(3)}
            scale = (1 << 400) if model % 29 == 0 else 1
            weights = {e: rng.randrange(5)*scale for e in sorted(actual)}
            fees, paths = score(board, actual, base, selected, weights)
            stats['full_matching_scores'] += 1
            chosen = rng.sample(paths, min(len(paths), model % 3))
            if model % 7 == 0:
                # Physical disjointness alone need not guarantee a full extension.
                candidates = [path for t in sorted(white_q)
                              for path, _ in literal_paths(board, actual, t, board-p-white_q, weights)]
                rng.shuffle(candidates)
                chosen, occupied = [], set()
                for path in candidates:
                    if not set(path) & occupied:
                        chosen.append(path)
                        occupied.update(path)
                    if len(chosen) == 2:
                        break
            fixed_n = {pair(path[i], path[i+1]) for path in chosen for i in range(0, len(path)-1, 2)}
            data = residual_data(board, actual, selected, chosen, weights)
            assert data['board'] == board-{v for path in chosen for v in path}
            exact = None
            for n in ns:
                if fixed_n <= n:
                    fee, _ = score(board, actual, n, selected, weights)
                    stats['full_matching_scores'] += 1
                    exact = fee if exact is None else min(exact, fee)
            black = sorted(data['black_q'])
            regions = [set(black), {v for v in black if rng.randrange(2)}]
            regions += [{v} for v in black[:2]]
            for region in regions:
                result = bound(data, region)
                literal = height == 2 and len(data['board']) <= 12
                check_networks(data, result, literal=literal)
                stats['literal_path_controls'] += int(literal)
                stats['regions'] += 1
                if result['lower'] is None:
                    assert exact is None
                    stats['infeasible_relaxations'] += 1
                elif exact is not None:
                    assert result['lower'] <= exact
                if 'certified_optimum' in result:
                    n = result['completion']['auxiliary']
                    assert fixed_n <= n
                    fee, _ = score(board, actual, n, selected, weights)
                    stats['full_matching_scores'] += 1
                    assert fee == exact == result['certified_optimum']
                    stats['exact_completions'] += 1
                if result['TH_flow']['value'] == result['required_TH'] and result['joint_assignment']['value'] == result['demand']:
                    stats['joint_stronger'] += result['joint_assignment']['cost'] > result['TH_flow']['cost']
                    stats['physical_stronger'] += result['joint_assignment']['cost'] < result['TH_flow']['cost']
            stats['models'] += 1
            stats['feasible_selected_models'] += selected <= allowed
    return stats


def applications():
    fixtures = json.loads(Path('output/multiport-grid-certificates.json').read_text())
    certificates = {}
    for label, item in fixtures.items():
        board = {(r, c) for r in range(item['height']) for c in range(item['width'])}
        actual = {pair(*map(tuple, e)) for e in item['actual']}
        selected = set(map(tuple, item['selected']))
        if label == 'unit':
            fixed = [list(map(tuple, path)) for path in item['bad_paths']]
            data = residual_data(board, actual, selected, fixed)
            result = bound(data, set(map(tuple, item['hall_black'])))
            check_networks(data, result)
            assert result['lower'] == result['certified_optimum'] == 4
            assert result['TH_flow']['cost'] == result['joint_assignment']['cost'] == 2
            assert data['fixed_expense']+result['TH_flow']['cost']+result['joint_assignment']['cost'] == 6
            assert score(board, actual, result['completion']['auxiliary'], selected, data['weights'])[0] == 4
            certificates[label] = result
        else:
            fixed = [[(6, 15), (5, 15), (4, 15), (3, 15)],
                     [(9, 12), (9, 11), (9, 10), (9, 9)]]
            cheap = {pair(*map(tuple, e)) for e in item['cheap_actual_edges']}
            original_region = set(map(tuple, item['hall_black']))
            for k in [0, 1, 2, 3, 11, 1 << 400]:
                weights = {e: 1 if e in cheap else k for e in actual}
                data = residual_data(board, actual, selected, fixed, weights)
                results = [bound(data, region) for region in
                           [original_region, {(3, 5)}, original_region | {(3, 5)}]]
                for r in results:
                    check_networks(data, r)
                assert [r['demand'] for r in results] == [1, 1, 2]
                assert [r['max_HH'] for r in results] == [1, 1, 1]
                assert [r['lower'] for r in results] == [2, 2, k+2]
                r = results[-1]
                assert r['certified_optimum'] == k+2
                assert score(board, actual, r['completion']['auxiliary'], selected, weights)[0] == k+2
                if k == 3:
                    # Independently reconstruct the printed all-K row certificate.
                    printed_paths = fixed + [[(0, 5), (1, 5), (2, 5), (3, 5)],
                        [(6, 7), (7, 7), (7, 8), (7, 9), (8, 9), (8, 8),
                         (8, 7), (9, 7), (9, 8), (10, 8), (10, 7), (11, 7),
                         (11, 8), (11, 9), (10, 9), (10, 10), (10, 11), (10, 12)]]
                    vertical_columns = {0: [2], 1: [8, 9, 12], 2: [2],
                        3: [0, 1, 8, 9, 10, 11, 12], 4: [2],
                        5: [0, 1, 8, 9, 10, 11, 12],
                        6: [2, 3, 4, 5, 6, 13, 14], 7: [0, 1, 12, 17],
                        8: [2, 3, 4, 5, 6, 15, 16], 9: [0, 1, 17], 10: [6]}
                    intervals = {0: [(0, 1), (3, 4), (6, 17)],
                        1: [(0, 1), (10, 11)], 2: [(0, 1), (10, 11)],
                        3: [], 4: [], 5: [], 6: [(16, 17)], 7: [(15, 16)],
                        8: [(13, 14)], 9: [(13, 14)],
                        10: [(2, 5), (13, 16)], 11: [(0, 5), (12, 17)]}
                    used = {v for p in printed_paths for v in p}
                    n = {pair(p[i], p[i+1]) for p in printed_paths
                         for i in range(0, len(p)-1, 2)}
                    n |= {e for e in actual if not set(e) & used}
                    vertical = {pair((a, b), (a+1, b)) for a, cols in vertical_columns.items() for b in cols}
                    horizontal = {pair((a, b), (a, b+1)) for a, runs in intervals.items()
                                  for left, right in runs for b in range(left, right+1, 2)}
                    assert len(vertical) == 42 and len(horizontal) == 26
                    n |= vertical | horizontal
                    # Minimum-flow and remainder tie choices may give another N.
                    # Check the printed witness itself, without requiring identity.
                    assert len(n) == 108
                    assert score(board, actual, n, selected, weights)[0] == 5
                    r['printed_auxiliary'] = n
                    r['printed_paths'] = printed_paths
                    r['printed_vertical'] = vertical
                    r['printed_horizontal_intervals'] = intervals
                    certificates[label] = r
    return certificates


def incomparable_controls():
    controls = {}
    for k in [1, 2, 17, 1 << 400]:
        board = {(r, c) for r in range(4) for c in range(10)}
        actual = set()
        for r, c in [(1, 1), (1, 7)]:
            for (a, b), (x, y) in [((0, 0), (0, 1)), ((0, 2), (1, 2)),
                                   ((2, 2), (2, 1)), ((2, 0), (1, 0))]:
                actual.add(pair((r+a, c+b), (r+x, c+y)))
        p = {v for e in actual for v in e}
        selected = {v for v in board-p if sum(v) % 2}-{(0, 7)}
        assert all(sum(adjacent(t, b) for b in p) <= 1 for t in selected)
        weights = {e: k if all(v[1] < 5 for v in e) else 1 for e in actual}
        data = residual_data(board, actual, selected, [], weights)
        result = bound(data, {(2, 2), (2, 8)})
        check_networks(data, result)
        assert result['joint_assignment']['cost'] == k
        assert result['TH_flow']['cost'] == 1
        paths = [[(0, 1), (1, 1), (1, 2), (2, 2)], [(0, 7), (1, 7), (1, 8), (2, 8)]]
        used = {v for path in paths for v in path}
        n = {pair(path[i], path[i+1]) for path in paths for i in [0, 2]}
        n |= {e for e in actual if not set(e) & used}
        n |= {pair((r, c), (r+1, c)) for r in [0, 2] for c in [0, 6]}
        n |= {pair((r, b), (r, b+1)) for r, runs in
              [(0, [(2, 5), (8, 9)]), (1, [(4, 5)]), (2, [(4, 5)]), (3, [(4, 5)])]
              for left, right in runs for b in range(left, right+1, 2)}
        assert score(board, actual, n, selected, weights)[0] == result['lower'] == k
        if k == 17:
            controls['joint_stronger'] = dict(result=result, actual=actual, selected=selected,
                                              attaining_auxiliary=n, selected_feasible=True)

        board = {(r, c) for r in range(6) for c in range(6)}
        actual = {pair(a, b) for a, b in [
            ((0, 0), (0, 1)), ((0, 2), (0, 3)), ((0, 4), (0, 5)),
            ((1, 0), (2, 0)), ((1, 1), (1, 2)), ((1, 4), (1, 5)),
            ((2, 2), (2, 3)), ((2, 5), (3, 5)), ((3, 0), (3, 1)), ((3, 3), (3, 4)),
            ((4, 0), (4, 1)), ((4, 2), (4, 3)), ((4, 4), (4, 5)),
            ((5, 0), (5, 1)), ((5, 2), (5, 3)), ((5, 4), (5, 5))]}
        selected = {(2, 1), (3, 2)}
        weights = {e: 1 if e == pair((2, 2), (2, 3)) else k for e in actual}
        data = residual_data(board, actual, selected, [], weights)
        result = bound(data, {(1, 3), (2, 4)})
        check_networks(data, result)
        assert result['joint_assignment']['cost'] == 2
        assert result['TH_flow']['cost'] == k+1
        assert result['certified_optimum'] == k+1
        assert score(board, actual, result['completion']['auxiliary'], selected, weights)[0] == k+1
        if k == 17:
            controls['physical_stronger'] = dict(result=result, actual=actual, selected=selected,
                                                 selected_feasible=False)
    return controls


def serial(value):
    if isinstance(value, dict):
        return {str(k): serial(v) for k, v in value.items()}
    if isinstance(value, set):
        return [serial(v) for v in sorted(value, key=repr)]
    if isinstance(value, (list, tuple)):
        return [serial(v) for v in value]
    return value


def main():
    report = small_controls()
    certificates = applications()
    certificates['incomparability'] = incomparable_controls()
    report.update(status='PASS', weighted_parameter_controls=6,
                  incomparable_bound_parameter_controls=8,
                  unit_retaining_optimum=4, weighted_retaining_formula='K+2, all integers K>=2',
                  scope='Written general proof and all-K construction; finite matching/path controls, no Lean execution.')
    Path('output/residual-hall-compensation-check.json').write_text(json.dumps(report, indent=2)+'\n')
    Path('output/residual-hall-certificates.json').write_text(json.dumps(serial(certificates), indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
