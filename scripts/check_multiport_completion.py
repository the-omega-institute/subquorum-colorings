"""Literal controls for multiport completion; no external packages.

The matching oracle uses exhaustive injections, and physical scoring follows
tagged alternating components without importing the optimizer's traversal.
"""
import argparse
from itertools import combinations, permutations, product
import json
from pathlib import Path
import random

from multiport_completion import assignment, solve, source_budget


def adjacent(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1]) == 1


def pair(a, b):
    return tuple(sorted((a, b)))


def exhaustive_assignment(left, right, costs):
    values = [sum(costs[a, b] for a, b in zip(left, order))
              for order in permutations(right)
              if all((a, b) in costs for a, b in zip(left, order))]
    return min(values) if values else None


def check_certificate(result, costs, left, right):
    if result['optimum'] is None:
        s = result['hall_right']
        n = {a for a in left if any((a, b) in costs for b in s)}
        assert n == result['hall_neighbours'] and len(n) < len(s)
    else:
        m = result['matching']
        assert set(m) == set(left) and set(m.values()) == set(right)
        assert result['optimum'] == sum(costs[a, b] for a, b in m.items())
        pot = result['potentials']
        # Reconstruct every residual arc from the literal matching and costs.
        # This avoids accepting a solver certificate that omits a bad arc.
        lorder, rorder = result['left'], result['right']
        n = len(lorder)
        li = {a: j for j, a in enumerate(lorder)}
        ri = {b: n+j for j, b in enumerate(rorder)}
        residual = {(li[a], 2*n, 0) for a in lorder}
        residual |= {(2*n+1, ri[b], 0) for b in rorder}
        for (a, b), c in costs.items():
            residual.add((ri[b], li[a], -c) if m[a] == b else (li[a], ri[b], c))
        assert set(result['residual']) == residual
        assert all(c+pot[a]-pot[b] >= 0 for a, b, c in residual)


def check_assignments():
    rng, models = random.Random(17111), 0
    for n in range(4):
        left, right = list(range(n)), list(range(n))
        edges = list(product(left, right))
        for mask in range(1 << len(edges)):
            for weighted in range(3):
                costs = {e: (0 if weighted == 0 else rng.randrange(8) if weighted == 1
                             else (1 << 400)+rng.randrange(8))
                         for j, e in enumerate(edges) if mask >> j & 1}
                r = assignment(left, right, costs)
                assert r['optimum'] == exhaustive_assignment(left, right, costs)
                check_certificate(r, costs, left, right)
                models += 1
    for _ in range(128):
        n = rng.randrange(4, 7)
        edges = list(product(range(n), repeat=2))
        costs = {e: rng.randrange(10) for e in edges if rng.randrange(4)}
        r = assignment(range(n), range(n), costs)
        assert r['optimum'] == exhaustive_assignment(list(range(n)), list(range(n)), costs)
        check_certificate(r, costs, range(n), range(n))
        models += 1
    return models


def saturates(black, white, edges):
    """Independent exhaustive injection, used only for small controls."""
    return any(all((b, t) in edges for b, t in zip(black, order))
               for order in permutations(white, len(black)))


def check_exposures():
    graphs = tests = exchanges = 0
    for nb in range(1, 4):
        for surplus in range(1, 4):
            nt = nb+surplus
            if nb*nt > 12:
                continue
            b, t = list(range(nb)), set(range(nt))
            all_edges = list(product(b, t))
            for mask in range(1 << len(all_edges)):
                edges = {e for j, e in enumerate(all_edges) if mask >> j & 1}
                if not saturates(b, sorted(t), edges):
                    continue
                bases = []
                for a0 in combinations(sorted(t), surplus):
                    a = set(a0)
                    actual = saturates(b, sorted(t-a), edges)
                    condition = True
                    for dmask in range(1 << nb):
                        d = {j for j in b if dmask >> j & 1}
                        n = {x for v, x in edges if v in d}
                        if len(a & n) > len(n)-len(d):
                            condition = False
                    assert actual == condition
                    tests += 1
                    if actual:
                        bases.append(a)
                assert bases
                for a in bases:
                    for c in bases:
                        for x in a-c:
                            assert any(a-{x} | {y} in bases for y in c-a)
                            exchanges += 1
                graphs += 1
    return dict(graphs=graphs, deletion_sets=tests, basis_exchanges=exchanges)


def fixture(height, width, origins, orientations=0):
    board = set(product(range(height), range(width)))
    pattern = [((0, 0), (0, 1)), ((0, 2), (1, 2)),
               ((2, 2), (2, 1)), ((2, 0), (1, 0))]
    parts, centres, actual = [], [], set()
    for i, (a, b) in enumerate(origins):
        centre = (a+1, b+1)
        centres.append(centre)
        parts.append(set(product(range(a, a+3), range(b, b+3)))-{centre})
        for x, y in pattern:
            if orientations >> i & 1:
                x, y = (x[1], x[0]), (y[1], y[0])
            actual.add(pair((x[0]+a, x[1]+b), (y[0]+a, y[1]+b)))
    p = set.union(*parts)
    white = {v for v in board-p if sum(v) % 2}
    holes = {v for v in white if sum(adjacent(v, x) for x in p) > 1}
    return board, actual, white-holes, parts, centres


def physical_score(board, actual, auxiliary, selected, centres, weights):
    """Direct independent tagged traversal of each white Q terminal."""
    mm, nn = {}, {}
    for a, b in actual:
        assert a not in mm and b not in mm and adjacent(a, b)
        mm[a], mm[b] = b, a
    for a, b in auxiliary:
        assert a in board and b in board and a not in nn and b not in nn and adjacent(a, b)
        nn[a], nn[b] = b, a
    assert set(nn) == board
    terminals = {v for v in board-mm.keys() if sum(v) % 2}
    used, paid, paths = set(), set(), []
    for t in sorted(terminals):
        v, path, resource = t, [t], set()
        while True:
            z = nn[v]
            assert z not in path
            path.append(z)
            if z not in mm:
                break
            resource.add(pair(z, mm[z]))
            v = mm[z]
            assert v not in path
            path.append(v)
        assert not used & set(path)
        used.update(path)
        if t in selected:
            assert not paid & resource
            paid.update(resource)
        paths.append((t, path[-1], path, t in selected))
    return dict(cost=sum(weights[e] for e in paid), paths=paths,
                th_centres=sum(t in selected and v in centres for t, v, _, _ in paths))


def exterior_matching(black, white):
    """Independent ordinary augmenting matcher, for larger physical fixtures."""
    matched = {}
    def augment(b, seen):
        for t in sorted(white):
            if adjacent(b, t) and t not in seen:
                seen.add(t)
                if t not in matched or augment(matched[t], seen):
                    matched[t] = b
                    return True
        return False
    if not all(augment(b, set()) for b in sorted(black)):
        return None
    return {b: t for t, b in matched.items()}


def row_matching(black, white, vertical):
    """Explicit certificate: fixed vertical edges, then horizontal row pairs."""
    remaining = set(black) | set(white)
    pairs = set()
    for a, b in vertical:
        assert a in remaining and b in remaining and adjacent(a, b)
        pairs.add(pair(a, b))
        remaining -= {a, b}
    for row in sorted({v[0] for v in remaining}):
        cells = sorted(v for v in remaining if v[0] == row)
        assert len(cells) % 2 == 0
        for a, b in zip(cells[::2], cells[1::2]):
            assert adjacent(a, b)
            pairs.add(pair(a, b))
    return {a if a in black else b: b if a in black else a for a, b in pairs}


def check_physical():
    rng, models, exact_budgets = random.Random(81311), 0, 0
    layouts = [(8, 12, [(1, 3), (1, 9), (5, 5)]),
               (4, 10, [(0, 0), (0, 6)]),
               (6, 12, [(1, 1), (1, 7)]),
               (4, 22, [(0, 0), (0, 6), (0, 12), (0, 18)])]
    for h, w, origins in layouts:
        for orientation in range(1 << len(origins)):
            data = fixture(h, w, origins, orientation)
            for kind in range(6):
                weights = {e: 1 if kind == 0 else 0 if kind == 1 else rng.randrange(8)
                           if kind < 5 else (1 << 400)+rng.randrange(8) for e in data[1]}
                for allow in [False, True]:
                    result = solve(*data, weights, holes_to_exterior=allow)
                    right = {('c', i) for i in range(len(origins))} | {('b', v) for v in result['exterior_black']}
                    check_certificate(result, result['costs'], data[2] | result['holes'], right)
                    assert result['optimum'] is not None
                    score = physical_score(data[0], data[1], result['auxiliary'], data[2], data[4], weights)
                    assert score['cost'] == result['optimum']
                    if not allow:
                        assert score['th_centres'] == result['q']
                    budget = source_budget(result, len(origins))
                    assert budget is not None and budget['lower'] <= score['cost']
                    if budget['lower'] == score['cost']:
                        exact_budgets += 1
                    models += 1
    # Exercise the direct exterior HH branch at k>q, rather than assuming
    # an optimizer on the main controls happened to choose that branch.
    board, actual, selected, parts, centres = fixture(6, 8, [(0, 0), (2, 4)])
    all_options = solve(board, actual, selected, parts, centres)
    costs = {e: c for e, c in all_options['costs'].items()
             if not (e[0] in all_options['holes'] and e[1][0] == 'c')}
    forced = assignment(selected | all_options['holes'], all_options['right'], costs)
    assert forced['optimum'] == 2 and all_options['q'] == 1
    check_certificate(forced, costs, selected | all_options['holes'], all_options['right'])
    n, used = set(), set()
    for t, (kind, target) in forced['matching'].items():
        path = ([t, target] if kind == 'b' else all_options['relay_options'][t, target]['path'])
        n.update(pair(path[j], path[j+1]) for j in range(0, len(path)-1, 2))
        used.update(pair(path[j], path[j+1]) for j in range(1, len(path)-1, 2))
    n.update(actual-used)
    score = physical_score(board, actual, n, selected, centres, {e: 1 for e in actual})
    assert score['cost'] == 2 and score['th_centres'] == 2
    assert any(t in all_options['holes'] and v not in centres and len(path) == 2
               for t, v, path, _ in score['paths'])
    return dict(models=models, exact_budget_controls=exact_budgets,
                extra_direct_HH_control=dict(board=[6, 8], q=1, th_centres=2, expense=2))


def tilings(board):
    if not board:
        yield set()
        return
    a = min(board)
    for b in sorted(board-{a}):
        if adjacent(a, b):
            for rest in tilings(board-{a, b}):
                yield rest | {pair(a, b)}


def check_full_matchings():
    data = fixture(4, 10, [(0, 0), (0, 6)])
    board, actual, selected, parts, centres = data
    weights_list = [{e: 1 for e in actual}, {e: 0 for e in actual},
                    {e: j % 3 for j, e in enumerate(sorted(actual))}]
    best = [None]*len(weights_list)
    full_best = [None]*len(weights_list)
    count = normal = 0
    for auxiliary in tilings(board):
        for j, weights in enumerate(weights_list):
            score = physical_score(board, actual, auxiliary, selected, centres, weights)
            value = score['cost']
            full_best[j] = value if full_best[j] is None else min(full_best[j], value)
            in_form = all(v in centres or len(path) == 2 for _, v, path, _ in score['paths'])
            if in_form:
                best[j] = value if best[j] is None else min(best[j], value)
        count += 1
        normal += in_form
    for j, weights in enumerate(weights_list):
        result = solve(*data, weights, holes_to_exterior=False)
        assert result['optimum'] == best[j]
        budget = source_budget(result, len(centres))
        assert budget['lower'] <= full_best[j] <= best[j]
        if all(weights.values()) and all(budget['rho'].values()):
            assert (full_best[j] == budget['lower']) == (best[j] == budget['lower'])
    return dict(full_matchings=count, normal_form_matchings=normal,
                scoring_passes=count*len(weights_list), exact_normal_form_optima=best,
                unrestricted_optima=full_best)


def obstruction():
    data = fixture(8, 12, [(1, 3), (1, 9), (5, 5)])
    board, actual, selected, parts, centres = data
    weights = {e: 1 for e in actual}
    result = solve(*data, weights, holes_to_exterior=False)
    assert result['q'] == 2 and result['holes'] == {(4, 5)}
    assert len(selected) == 35 and len(result['exterior_black']) == 33
    assert result['optimum'] == source_budget(result, 3)['lower'] == 2
    d = {(4, 10), (5, 9), (5, 11), (6, 8), (6, 10), (7, 9), (7, 11)}
    f = {t for t in selected if any(adjacent(t, b) for b in d)}
    expected = {(4, 9), (4, 11), (5, 8), (5, 10), (6, 9), (6, 11), (7, 8), (7, 10)}
    assert f == expected and len(d) == 7 and len(f) == 8
    bad_a, bad_c = (4, 9), (5, 8)
    assert exterior_matching(result['exterior_black'], selected-{bad_a, bad_c}) is None
    good = []
    for a, c in [(bad_a, (4, 7)), ((3, 8), bad_c)]:
        direct = exterior_matching(result['exterior_black'], selected-{a, c})
        assert direct is not None
        common = [((0, 2), (1, 2)), ((0, 7), (1, 7)), ((1, 6), (2, 6)),
                  ((1, 8), (2, 8)), ((2, 2), (3, 2)), ((2, 7), (3, 7)),
                  ((3, 6), (4, 6)), ((4, 4), (5, 4)), ((6, 4), (7, 4))]
        extra = ((3, 8), (4, 8)) if a == bad_a else ((4, 9), (5, 9))
        direct = row_matching(result['exterior_black'], selected-{a, c}, common+[extra])
        paths = [result['relay_options'][a, 1]['path'], result['relay_options'][c, 2]['path'],
                 result['relay_options'][(4, 5), 0]['path']]
        n, used = {pair(b, t) for b, t in direct.items()}, set()
        for path in paths:
            n.update(pair(path[j], path[j+1]) for j in range(0, len(path)-1, 2))
            used.update(pair(path[j], path[j+1]) for j in range(1, len(path)-1, 2))
        n.update(actual-used)
        score = physical_score(board, actual, n, selected, centres, weights)
        assert score['cost'] == 2 and score['th_centres'] == 2
        good.append(dict(ports=[a, c], relays=paths, auxiliary=sorted(n), direct=sorted(direct.items())))
    bad_paths = [result['relay_options'][bad_a, 1]['path'], result['relay_options'][bad_c, 2]['path']]
    assert bad_paths == [[(4, 9), (3, 9), (2, 9), (2, 10)],
                         [(5, 8), (5, 7), (6, 7), (6, 6)]]
    # Referee's physical k=3 control: retaining the two bad relays need not
    # leave exactly two TH centres. It does still prevent fee-two completion.
    k3_paths = bad_paths + [[(4, 3), (3, 3), (2, 3), (2, 4)],
                           [(0, 11), (1, 11), (2, 11), (3, 11), (3, 10), (4, 10)]]
    vertical = [((a, b), (a+1, b)) for a in [0, 2] for b in [2, 7, 8]]
    vertical += [((a, 6), (a+1, 6)) for a in [1, 3]]
    vertical += [((4, b), (5, b)) for b in [2, 11]]+[((6, 4), (7, 4))]
    direct = row_matching(result['exterior_black']-{(4, 10), (4, 4)},
                          selected-{path[0] for path in k3_paths}, vertical)
    n = {pair(b, t) for b, t in direct.items()} | {pair((4, 5), (4, 4))}
    used = set()
    for path in k3_paths:
        n.update(pair(path[j], path[j+1]) for j in range(0, len(path)-1, 2))
        used.update(pair(path[j], path[j+1]) for j in range(1, len(path)-1, 2))
    n.update(actual-used)
    score = physical_score(board, actual, n, selected, centres, weights)
    assert score['cost'] == 5 and score['th_centres'] == 3
    assert sum(path[0] in f for path in k3_paths if path[-1] in centres) == 2
    k3 = dict(th_centres=3, expense=5, centre_withdrawal=2,
              origin='Coordinate construction suggested by scoped editor review',
              paths=k3_paths, auxiliary=sorted(n))
    return dict(height=8, width=12, origins=[(1, 3), (1, 9), (5, 5)], actual=sorted(actual),
                selected=sorted(selected), white_holes=sorted(result['holes']), centres=centres,
                exterior_black=sorted(result['exterior_black']), hall_black=sorted(d),
                hall_neighbours=sorted(f), bad_ports=[bad_a, bad_c], bad_paths=bad_paths,
                hall_after_deletion=[7, 6], exact_unit_optimum=2, good_completions=good,
                retaining_bad_pair_k3_control=k3)


def weighted_obstruction():
    board = set(product(range(12), range(18)))
    origins = [(1, 3), (1, 13), (7, 7)]
    pattern = [((0, 2), (1, 2)), ((2, 0), (2, 1)),
               ((2, 4), (2, 3)), ((4, 2), (3, 2))]
    for a in [0, 3]:
        for b in [0, 3]:
            pattern.extend([((a, b), (a, b+1)), ((a+1, b), (a+1, b+1))])
    parts, centres, actual = [], [], set()
    for a, b in origins:
        c = (a+2, b+2)
        centres.append(c)
        parts.append(set(product(range(a, a+5), range(b, b+5)))-{c})
        actual.update(pair((a+x, b+y), (a+z, b+w)) for (x, y), (z, w) in pattern)
    p = set.union(*parts)
    white = {v for v in board-p if sum(v) % 2}
    holes = {v for v in white if sum(adjacent(v, z) for z in p) > 1}
    selected = white-holes
    cheap = {pair((5, 15), (4, 15)), pair((9, 11), (9, 10))}
    bad = {(6, 15), (9, 12)}
    d = {(6, 14), (6, 16), (7, 13), (7, 15), (7, 17), (8, 12),
         (8, 14), (8, 16), (9, 13), (9, 15), (9, 17), (10, 12),
         (10, 14), (10, 16), (11, 13), (11, 15), (11, 17)}
    f = {t for t in selected if any(adjacent(t, b) for b in d)}
    assert holes == {(6, 7)} and len(d) == 17 and len(f) == 18 and bad <= f
    controls, witnesses = [], []
    for k in [1, 2, 3, 7, 101, 1 << 400]:
        weights = {e: 1 if e in cheap else k for e in actual}
        for allow in [False, True]:
            result = solve(board, actual, selected, parts, centres, weights, allow)
            assert result['q'] == 2 and source_budget(result, 3)['lower'] == 2
            assert result['optimum'] == k+1
            score = physical_score(board, actual, result['auxiliary'], selected, centres, weights)
            assert score['cost'] == k+1
            if k > 1:
                only_cheap = {(t, i) for (t, i), path in result['relay_options'].items()
                              if t in selected and path['cost'] == 1}
                assert only_cheap == {((6, 15), 1), ((9, 12), 2)}
            controls.append(dict(k=str(k), holes_to_exterior=allow, normal_form=k+1, budget=2))
        if k != 7:
            continue
        assert exterior_matching(result['exterior_black'], selected-bad) is None
        for a, c in [((6, 15), (9, 6)), ((3, 12), (9, 12))]:
            direct = exterior_matching(result['exterior_black'], selected-{a, c})
            assert direct is not None
            vertical = None
            if a == (6, 15):
                vertical = [((x, y), (x+1, y)) for y in [2, 12] for x in [1, 3, 5]]
                vertical += [((7, 6), (8, 6)), ((10, 6), (11, 6))]
                direct = row_matching(result['exterior_black'], selected-{a, c}, vertical)
            paths = [result['relay_options'][a, 1]['path'], result['relay_options'][c, 2]['path'],
                     result['relay_options'][(6, 7), 0]['path']]
            n, used = {pair(b, t) for b, t in direct.items()}, set()
            for path in paths:
                n.update(pair(path[j], path[j+1]) for j in range(0, len(path)-1, 2))
                used.update(pair(path[j], path[j+1]) for j in range(1, len(path)-1, 2))
            n.update(actual-used)
            assert physical_score(board, actual, n, selected, centres, weights)['cost'] == 8
            # These lists have one paid cheap edge and one paid K edge, for all K.
            paid_edges = set()
            for path in paths[:2]:
                paid_edges.update(pair(path[j], path[j+1]) for j in range(1, len(path)-1, 2))
            assert len(paid_edges & cheap) == len(paid_edges-cheap) == 1
            witnesses.append(dict(ports=[a, c], relays=paths, auxiliary=sorted(n), vertical=vertical,
                                  direct=sorted(direct.items()), paid=sorted(paid_edges)))
    return dict(height=12, width=18, origins=origins, local_matching_pattern=pattern,
                actual=sorted(actual), selected=sorted(selected), white_holes=sorted(holes),
                centres=centres, hall_black=sorted(d), hall_neighbours=sorted(f),
                hall_after_deletion=[17, 16], bad_ports=sorted(bad), cheap_actual_edges=sorted(cheap),
                general_formula='Lambda_q=2; f*=U_centres=U_direct=K+1 for every integer K>=2',
                exact_controls=controls, attaining_completions=witnesses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='output/multiport-completion-check.json')
    parser.add_argument('--certificates', default='output/multiport-grid-certificates.json')
    args = parser.parse_args()
    report = dict(scope='Finite controls of written general proofs. Normal-form optimizer is not an unrestricted TH optimizer. No Lean or grid triple-equality conclusion.',
                  assignment_models=check_assignments(), exposure=check_exposures(),
                  physical=check_physical(), exhaustive_board=check_full_matchings())
    certificate = obstruction()
    weighted = weighted_obstruction()
    report['unit_obstruction'] = dict(board=[8, 12], hall=[7, 6], exact_optimum=2,
                                     individually_attaining_completions=len(certificate['good_completions']))
    report['weighted_obstruction'] = dict(board=[12, 18], hall=[17, 16],
                                        exact_controls=len(weighted['exact_controls']),
                                        symbolic_cost='K+1', source_budget=2)
    certificates = dict(unit=certificate, weighted=weighted)
    for name, value in [(args.output, report), (args.certificates, certificates)]:
        path = Path(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
