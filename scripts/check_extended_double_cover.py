#!/usr/bin/env python3
"""Literal graph/subset/path controls; no dependency on another checker."""
from itertools import combinations
import json
from pathlib import Path
import random

from extended_double_cover import (extended_cover, optimum_certificate,
                                   representative_certificate, zero_TH_completion)


def base(n, edges):
    result = [set() for _ in range(n)]
    for u, v in edges:
        result[u].add(v)
        result[v].add(u)
    return result


def literal_cover(h):
    n = len(h)
    return [{n+j for j in range(n) if i == j or j in h[i]} for i in range(n)]+[
        {i for i in range(n) if i == j or j in h[i]} for j in range(n)]


def masks(g):
    return [sum(1 << u for u in row) for row in g]


def neighbours(h, selected):
    return {v for u in selected for v in h[u]}


def literal_optima(g):
    adj = masks(g)
    size, beta, sf = 1 << len(g), 0, 0
    forming = bytearray(size)
    for selected in range(size):
        active, dissociation = 0, True
        for v in range(len(g)):
            if selected >> v & 1:
                degree = (adj[v] & selected).bit_count()
                if degree:
                    active |= 1 << v
                if degree > 1:
                    dissociation = False
        if dissociation:
            beta = max(beta, selected.bit_count())
        ok = all((adj[v] & selected).bit_count() >= 2 or adj[v] & active
                 for v in range(len(g)) if not selected >> v & 1)
        forming[selected] = ok
        if ok and all(not forming[selected ^ (1 << v)] for v in range(len(g)) if selected >> v & 1):
            sf = max(sf, selected.bit_count())
    return beta, sf, size


def matchings(g, vertices=None):
    vertices = set(range(len(g))) if vertices is None else vertices
    if not vertices:
        yield set()
        return
    u = min(vertices)
    yield from matchings(g, vertices-{u})
    for v in sorted(g[u] & (vertices-{u})):
        for rest in matchings(g, vertices-{u, v}):
            yield rest | {(min(u, v), max(u, v))}


def score(g, actual, auxiliary, selected, weights):
    assert len(auxiliary)*2 == len(g)
    assert {v for e in auxiliary for v in e} == set(range(len(g)))
    assert all(v in g[u] for u, v in auxiliary)
    m = {v: w for e in actual for v, w in (e, e[::-1])}
    a = {v: w for e in auxiliary for v, w in (e, e[::-1])}
    cost = 0
    for t in selected:
        u, seen = t, {t}
        while True:
            v = a[u]
            assert v not in seen
            seen.add(v)
            if v not in m:
                break
            u = m[v]
            assert u not in seen
            seen.add(u)
            cost += weights[tuple(sorted((u, v)))]
    return cost


def check_certificate(h, result):
    n = len(h)
    matching = result['double_matching']
    assert len({u for u, _ in matching}) == len(matching)
    assert len({v for _, v in matching}) == len(matching)
    assert all(v in h[u] for u, v in matching)
    left, right = set(result['double_vertex_cover_left']), set(result['double_vertex_cover_right'])
    assert all(u in left or v in right for u in range(n) for v in h[u])
    assert len(left)+len(right) == len(matching)
    x, y = set(result['Hall_left']), set(result['Hall_right'])
    assert neighbours(h, x) == y and len(x)-len(y) == n-len(matching)
    independent, adjacent = set(result['critical_independent']), set(result['critical_neighbours'])
    assert not independent & neighbours(h, independent)
    assert adjacent == neighbours(h, independent)
    assert result['deficiency'] == len(independent)-len(adjacent) == n-len(matching)
    g, selected = literal_cover(h), set(result['dissociation'])
    assert all(len(g[v] & selected) <= 1 for v in selected)
    assert len(selected) == result['optimum'] == 2*n-len(matching)


def pair_controls(h):
    g, n = literal_cover(h), len(h)
    adj = masks(g)
    best, pairs, zero, covered = 0, 0, 0, 0
    for actual in matchings(g):
        p = {v for e in actual for v in e}
        mask_p = sum(1 << v for v in p)
        q = sum(1 << v for v in range(2*n) if v not in p)
        selected = q
        while True:
            if all((adj[v] & (selected | mask_p)).bit_count() <= 1
                   for v in range(2*n) if selected >> v & 1):
                t = {v for v in range(2*n) if selected >> v & 1}
                cert = representative_certificate(h, actual, t)
                assert cert['objective'] == len(t)+len(actual)
                assert cert['objective'] <= optimum_certificate(h)['optimum']
                best = max(best, cert['objective'])
                pairs += 1
            if selected == 0:
                break
            selected = (selected-1) & q
        t = {v for v in range(n) if v not in p and len(g[v] & p) <= 1}
        result = zero_TH_completion(h, actual, t)
        auxiliary = {tuple(e) for e in result['auxiliary']}
        weights = {e: (1 << 400) if zero % 7 == 0 else zero % 3 for e in actual}
        assert score(g, actual, auxiliary, t, weights) == 0
        assert all(next(w for e in auxiliary if v in e for w in e if w != v) not in p for v in t)
        zero += 1
        covered += 1 << len(t)
    return dict(representative_pairs=pairs, optimum=best, zero_constructions=zero,
                white_subsets_certified=covered)


def main():
    report = dict(base_graphs=0, literal_subsets=0, observed_SF_equalities=0,
                  representative_pairs=0, zero_constructions=0,
                  white_subsets_certified=0, per_order=[])
    examples = []
    for n in range(6):
        edges = list(combinations(range(n), 2))
        count = 0
        for bits in range(1 << len(edges)):
            h = base(n, [e for i, e in enumerate(edges) if bits >> i & 1])
            cert = optimum_certificate(h)
            check_certificate(h, cert)
            assert extended_cover(h) == literal_cover(h)
            delta = max((len(i)-len(neighbours(h, i)) for bits_i in range(1 << n)
                         if not (i := {v for v in range(n) if bits_i >> v & 1}) & neighbours(h, i)), default=0)
            assert delta == cert['deficiency']
            beta, sf, size = literal_optima(literal_cover(h))
            assert beta == cert['optimum']
            report['observed_SF_equalities'] += sf == beta
            if sf > beta:
                examples.append(dict(n=n, edges=[e for i, e in enumerate(edges) if bits >> i & 1],
                                     beta=beta, sf=sf))
            if n <= 4:
                control = pair_controls(h)
                assert control['optimum'] == beta
                for name in ('representative_pairs', 'zero_constructions', 'white_subsets_certified'):
                    report[name] += control[name]
            report['literal_subsets'] += size
            report['base_graphs'] += 1
            count += 1
        report['per_order'].append(dict(n=n, graphs=count))
    rng = random.Random(2026111203)
    report['larger_certificates'] = 0
    for n in (8, 17, 64, 257, 1024):
        for probability in (0.01, 0.04, 0.15):
            h = base(n, [(u, v) for u in range(n) for v in range(u+1, n)
                         if rng.random() < probability])
            cert = optimum_certificate(h)
            check_certificate(h, cert)
            report['larger_certificates'] += 1
    report['SF_counterexamples_in_finite_run'] = examples
    report['SF_scope'] = 'Finite observations; not a proof of any all-base SF formula'
    report['status'] = 'PASS'
    Path('output').mkdir(exist_ok=True)
    Path('output/extended-double-cover-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
