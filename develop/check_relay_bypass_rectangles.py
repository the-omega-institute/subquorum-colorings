"""Check the arbitrary-entrant relay theorem; general proof is in docs/.

No solver dependencies. Explicit packings independently check flow optima,
cheap-matching certificates and the fixed-subset private-quota cost formula.
"""
import argparse
from collections import Counter
import itertools as it
import json
from pathlib import Path
import random

from check_multisource_relay_bypass import solve, brute, coupled_defect_rank

if not __debug__:
    raise RuntimeError('Assertions are required; run without -O.')


def subsets(items, size=None):
    items = sorted(items)
    for n in (range(len(items)+1) if size is None else [size]):
        yield from it.combinations(items, n)


def private_matchings(S, J, edge):
    """Independent exhaustive list, including nonmaximum matchings."""
    if not S:
        yield []
        return
    a, *tail = S
    yield from private_matchings(tail, J, edge)
    for j in J:
        if edge(a, j):
            for rest in private_matchings(tail, tuple(k for k in J if k != j), edge):
                yield [(a, j)] + rest


def maximum_matching(S, J, edge):
    assigned = {}
    def augment(a, seen):
        for j in sorted(J):
            if j in seen or not edge(a, j):
                continue
            seen.add(j)
            if j not in assigned or augment(assigned[j], seen):
                assigned[j] = a
                return True
        return False
    for a in sorted(S):
        augment(a, set())
    return [(a, j) for j, a in assigned.items()]


def cheap(model, g, a, j):
    data = model['gates'][g]
    return (j in model['direct'][a] and
            model['direct'][a][j] <= data['entry'][a]+data['output'][j])


def choices(model, Q):
    result = {a: [dict(source=a, unit=j, gate=None, cost=d)
                  for j, d in direct.items() if j in Q]
              for a, direct in model['direct'].items()}
    for g, data in model['gates'].items():
        for a, e in data['entry'].items():
            for j, o in data['output'].items():
                if j in Q:
                    result[a].append(dict(source=a, unit=j, gate=g, cost=e+o))
    return result


def project(model, Q):
    # The earlier flow utility's projection-only guard assumes <=c+1 entrants.
    # Increasing this unused capacity changes no projected arc or cost.
    relaxed = dict(direct=model['direct'], gates={
        g: dict(data, capacity=max(data.get('capacity', 1), len(data['entry'])))
        for g, data in model['gates'].items()})
    return solve(relaxed, Q, True)


def empty_squares(model, Q, g):
    data = model['gates'][g]
    c = data.get('capacity', 1)
    units = set(data['output']) & Q
    for q in range(c+1, min(len(data['entry']), len(units))+1):
        for X in subsets(data['entry'], q):
            for Y in subsets(units, q):
                if not any(cheap(model, g, a, j) for a in X for j in Y):
                    yield frozenset(X), frozenset(Y), q-c


def rectangle_rank(model, Q):
    families = [list(empty_squares(model, Q, g)) for g in model['gates']]
    local_sum = sum(max((w for _, _, w in f), default=0) for f in families)
    def visit(i, sources, units):
        if i == len(families):
            return 0
        best = visit(i+1, sources, units)
        for X, Y, w in families[i]:
            if not X & sources and not Y & units:
                best = max(best, w+visit(i+1, sources | X, units | Y))
        return best
    return visit(0, frozenset(), frozenset()), local_sum


def repair(model, Q, packing):
    result = [dict(p) for p in packing if p['gate'] is None]
    loss = 0
    holes = []
    for g, data in model['gates'].items():
        using = [p for p in packing if p['gate'] == g]
        S = {p['source'] for p in using}
        J = {p['unit'] for p in using}
        H = maximum_matching(S, J, lambda a, j: cheap(model, g, a, j))
        X = S-{a for a, _ in H}
        Y = J-{j for _, j in H}
        assert len(X) == len(Y)
        assert not any(cheap(model, g, a, j) for a in X for j in Y)
        c = data.get('capacity', 1)
        ell = max(0, len(X)-c)
        loss += ell
        if ell:
            holes.append((g, X, Y, ell))
        local = [dict(source=a, unit=j, gate=None, cost=model['direct'][a][j]) for a, j in H]
        local += [dict(source=a, unit=j, gate=g, cost=data['entry'][a]+data['output'][j])
                  for a, j in list(zip(sorted(X), sorted(Y)))[:c]]
        assert len(local) == len(using)-ell
        assert sum(p['cost'] for p in local) <= sum(p['cost'] for p in using)
        if ell == 0:
            assert {p['source'] for p in local} == S
            assert {p['unit'] for p in local} == J
        result += local
    assert len(result) == len(packing)-loss
    assert len({p['source'] for p in result}) == len(result) == len({p['unit'] for p in result})
    assert all(p in choices(model, Q)[p['source']] for p in result)
    loads = Counter(p['gate'] for p in result if p['gate'] is not None)
    assert all(n <= model['gates'][g].get('capacity', 1) for g, n in loads.items())
    for i, (_, X, Y, _) in enumerate(holes):
        assert all(not X & xx and not Y & yy for _, xx, yy, _ in holes[:i])
    assert sum(p['cost'] for p in result) <= sum(p['cost'] for p in packing)
    return result, loss


def check_model(model, Q, counts, independent=False):
    projected = project(model, Q)
    actual = solve(model, Q)
    certificate, loss = repair(model, Q, projected['routes'])
    rank, local_sum = rectangle_rank(model, Q)
    safe = not any(next(empty_squares(model, Q, g), None) for g in model['gates'])
    assert loss <= rank <= projected['value']
    assert actual['value'] >= len(certificate) == projected['value']-loss
    assert actual['value'] >= projected['value']-rank
    if safe or loss == 0:
        assert (actual['value'], actual['cost']) == (projected['value'], projected['cost'])
    if all(len(d['entry']) <= d.get('capacity', 1)+1 for d in model['gates'].values()):
        old_rank, _ = coupled_defect_rank(model, Q)
        assert old_rank == rank
        counts['old_rank_equalities'] += 1
    if independent:
        for enforce, answer in [(False, projected), (True, actual)]:
            exact, n = brute(choices(model, Q), enforce,
                             {g: d.get('capacity', 1) for g, d in model['gates'].items()})
            assert exact == (answer['value'], answer['cost'])
            counts['independent_route_packings'] += n
        counts['independent_models'] += 1
    counts['network_models'] += 1
    counts['safe_network_models'] += safe
    counts['strict_joint_overlap_improvements'] += rank < local_sum
    counts['projection_value_gaps'] += projected['value'] > actual['value']
    counts['projection_cost_only_gaps'] += (projected['value'] == actual['value'] and projected['cost'] < actual['cost'])
    return dict(projection=[projected['value'], projected['cost']],
                actual=[actual['value'], actual['cost']], K=rank, local_sum=local_sum, safe=safe)


def local_exhaustion(counts):
    # All binary 3x3 private relations, both capacities. Costs are separable
    # at the relay and privately nonuniform. Every balanced subinterface is tested.
    for bits in range(1 << 9):
        D = {a: {j: a+j+1-((a+j) % 2) for j in range(3) if bits >> (3*a+j) & 1}
             for a in range(3)}
        for c in (1, 2):
            model = dict(direct=D, gates={0: dict(capacity=c,
                entry={a: a+1 for a in range(3)}, output={j: j for j in range(3)})})
            universal = True
            for t in range(4):
                for S in subsets(range(3), t):
                    for J in subsets(range(3), t):
                        existing = lambda a, j: j in D[a]
                        allH = list(private_matchings(S, J, existing))
                        mu = max(map(len, allH))
                        assert len(maximum_matching(S, J, existing)) == mu
                        predicted = min(t, c+mu)
                        quota = max(0, t-c)
                        baseline = sum(a+1 for a in S)+sum(J)
                        full_costs = [baseline+sum(D[a][j]-(a+1)-j for a, j in H)
                                      for H in allH if len(H) >= quota]
                        local = dict(direct={a: {j: d for j, d in D[a].items() if j in J} for a in S},
                            gates={0: dict(capacity=c, entry={a: a+1 for a in S}, output={j: j for j in J})})
                        answer, n = brute(choices(local, set(J)), True, {0: c})
                        assert answer[0] == predicted
                        if predicted == t:
                            assert answer[1] == min(full_costs)
                        else:
                            assert not full_costs
                        universal &= predicted == t
                        counts['local_subset_interfaces'] += 1
                        counts['local_independent_packings'] += n
                        # Every all-relay pairing must preserve its original identities.
                        for perm in it.permutations(J):
                            P = [dict(source=a, unit=j, gate=0, cost=a+1+j) for a, j in zip(S, perm)]
                            fixed, loss = repair(model, set(J), P)
                            assert len(fixed) == predicted and loss == t-predicted
                            counts['all_relay_pairings'] += 1
            safe = next(empty_squares(model, set(range(3)), 0), None) is None
            assert universal == safe
            counts['exhaustive_relations_and_capacities'] += 1
            counts['safe_exhaustive_relations_and_capacities'] += safe


def controls(counts):
    results = {}
    for c, k, n in [(1, 1, 3), (1, 2, 6), (2, 1, 4), (2, 3, 8), (3, 2, 9)]:
        model = dict(direct={a: {j: 0 for j in range(n)} if a < k else {} for a in range(n)},
            gates={0: dict(capacity=c, entry={a: 1 for a in range(n)}, output={j: 0 for j in range(n)})})
        r = check_model(model, set(range(n)), counts, independent=n <= 4)
        assert (r['projection'][0], r['actual'][0], r['K']) == (n, c+k, n-c-k)
        assert all(any(cheap(model, 0, a, j) for a in range(n)) for j in range(n))
        results[f'covered_everywhere_c{c}_k{k}_n{n}'] = r
    model = dict(direct={a: {j: 2 for j in range(2)} for a in range(2)},
        gates={0: dict(capacity=1, entry={a: 1 for a in range(2)}, output={j: 0 for j in range(2)})})
    r = check_model(model, {0, 1}, counts, True)
    assert r['projection'] == [2, 2] and r['actual'] == [2, 3]
    results['cost_only_empty_square'] = r
    offset = dict(direct={0: {0: 0}, 1: {1: 11}, 2: {}}, gates={0: dict(
        capacity=1, entry={a: 10 for a in range(3)}, output={j: 0 for j in range(3)})})
    r = check_model(offset, {0, 1, 2}, counts, True)
    all_gate = [dict(source=a, unit=a, gate=0, cost=10) for a in range(3)]
    fixed, ell = repair(offset, {0, 1, 2}, all_gate)
    assert ell == 1 and len(fixed) == 2
    assert r['projection'] == [3, 20] and r['actual'] == [3, 21]
    assert r['actual'][1] < sum(p['cost'] for p in all_gate)
    results['cheap_loss_conservative_costly_bypass_offset'] = r
    # Check the cost formula with expensive private routes and optional cheap ones.
    rng = random.Random(20261025092)
    for _ in range(160):
        n = rng.randrange(1, 5); c = rng.randrange(1, n+1)
        e = {a: rng.randrange(4) for a in range(n)}
        o = {j: rng.randrange(4) for j in range(n)}
        D = {a: {j: rng.randrange(9) for j in range(n) if rng.random() < .6} for a in range(n)}
        m = dict(direct=D, gates={0: dict(capacity=c, entry=e, output=o)})
        answer, packings = brute(choices(m, set(range(n))), True, {0: c})
        allH = list(private_matchings(tuple(range(n)), tuple(range(n)), lambda a, j: j in D[a]))
        mu = max(map(len, allH))
        assert answer[0] == min(n, c+mu)
        eligible = [sum(e.values())+sum(o.values())+sum(D[a][j]-e[a]-o[j] for a, j in H)
                    for H in allH if len(H) >= n-c]
        if answer[0] == n:
            assert answer[1] == min(eligible)
        else:
            assert not eligible
        counts['weighted_private_quota_controls'] += 1
        counts['weighted_quota_independent_packings'] += packings
    diag = dict(direct={a: {a: 0} for a in range(4)}, gates={0: dict(capacity=1,
        entry={a: 1 for a in range(4)}, output={j: 0 for j in range(4)})})
    r = check_model(diag, set(range(4)), counts, True)
    assert not r['safe'] and r['projection'] == r['actual'] == [4, 0]
    results['unsafe_but_full_optimum_exact'] = r
    for shared in ('source', 'unit'):
        m = dict(direct={a: {} for a in range(4)}, gates={g: dict(capacity=1,
            entry={a: 1 for a in ((0, g+1) if shared == 'source' else (2*g, 2*g+1))},
            output={j: 0 for j in ((0, g+1) if shared == 'unit' else (2*g, 2*g+1))}) for g in range(2)})
        Q = set().union(*(set(d['output']) for d in m['gates'].values()))
        r = check_model(m, Q, counts, True)
        assert (r['local_sum'], r['K']) == (2, 1)
        results[f'shared_{shared}_not_double_counted'] = r
    return results


def physical(counts):
    from check_multisource_relay_bypass import fixture, inspect, whole_bands, owner_data, fork_flow, restrict
    board, layers = fixture()
    d, pools, _ = inspect(board, whole_bands(board), layers)
    owner, _, _, _ = owner_data(*d[:2]); a, b = owner[5, 13], owner[5, 15]
    L, R, X, S, Y = pools
    m = dict(direct={a: {j: 0 for j in L}, b: {**{j: 0 for j in R}, **{j: 1 for j in X}}},
        gates={0: dict(capacity=1, entry={a: 1, b: 1}, output={**{j: 0 for j in S}, **{j: 4 for j in Y}})})
    safe = gaps = 0
    for sizes in it.product(range(3), repeat=5):
        Q = set().union(*(set(sorted(p)[:n]) for p, n in zip((S, L-S, R, X, Y), sizes)))
        r = check_model(m, Q, counts)
        actual = fork_flow(*restrict(d, Q))
        assert r['actual'] == [actual['value'], actual['cost']]
        safe += r['safe']; gaps += r['projection'][0] > r['actual'][0]
        counts['physical_original_pool_patterns'] += 1
    assert (safe, gaps) == (162, 1)
    return dict(existing_board='fully frozen 56P/26T; complete original routing, no new embedding',
                patterns=243, safe=162, strict_value_gaps=1)


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--output', type=Path, required=True); args = ap.parse_args()
    counts = Counter(); local_exhaustion(counts); cc = controls(counts)
    rng = random.Random(20261025093)
    for i in range(180):
        na = rng.randrange(2, 6); nj = rng.randrange(1, 6); ng = rng.randrange(1, 4)
        m = dict(direct={a: {j: rng.randrange(7) for j in range(nj) if rng.random() < .42} for a in range(na)},
                 gates={g: dict(capacity=rng.choice((1, 1, 2)),
                     entry={a: rng.randrange(4) for a in range(na) if rng.random() < .8},
                     output={j: rng.randrange(4) for j in range(nj) if rng.random() < .8}) for g in range(ng)})
        check_model(m, set(range(nj)), counts, independent=i < 35 and na <= 4)
    pp = physical(counts)
    result = dict(status='PASS', counts=dict(counts), controls=cc, physical=pp,
        scope='General proofs are written separately. Exhaustion is supplementary. Arbitrary entrant counts, exact isolated quota cost, cheap matching repairs and coupled original-identity rectangle rank. Private-owner disjointness assumed, not inferred. No new physical embedding, no universal grid bound, no mail. Lean scope recorded separately.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **dict(counts))))


if __name__ == '__main__':
    main()
