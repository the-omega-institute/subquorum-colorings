#!/usr/bin/env python3
"""Literal graph/subset/path controls; no dependency on another checker."""
from itertools import combinations
import json
from pathlib import Path
import random

from extended_double_cover import (extended_cover, minimal_forming_certificate, optimum_certificate,
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
    size, beta, sf, minimal_sets = 1 << len(g), 0, 0, []
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
            minimal_sets.append({v for v in range(len(g)) if selected >> v & 1})
    return beta, sf, size, minimal_sets


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
    # Validate domains before indexing: Python's negative indices are not
    # additional graph vertices. This helper also accepts external witnesses.
    def check_ids(values, limit):
        assert all(type(v) is int and 0 <= v < limit for v in values)
        assert len(set(values)) == len(values)
    for edge in matching:
        assert len(edge) == 2
        assert all(type(v) is int and 0 <= v < n for v in edge)
    for key in ('double_vertex_cover_left', 'double_vertex_cover_right',
                'Hall_left', 'Hall_right', 'critical_independent', 'critical_neighbours'):
        check_ids(result[key], n)
    check_ids(result['dissociation'], 2*n)
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
                  white_subsets_certified=0, minimal_forming_sets=0,
                  empty_rung_budgets=0, reserved_empty_rungs=0,
                  high_rung_occurrences=0, per_order=[])
    examples = []
    # The independent review supplied this formerly accepted malformed
    # K_(1,3) certificate: -4 aliases 0 during indexing, faking a third edge.
    star = base(4, [(0, 1), (0, 2), (0, 3)])
    malformed = dict(double_matching=[(0, 1), (-4, 2), (1, 0)],
                     double_vertex_cover_left=[0, 1], double_vertex_cover_right=[0],
                     Hall_left=[1, 2], Hall_right=[0], critical_independent=[1, 2],
                     critical_neighbours=[0], deficiency=1,
                     dissociation=[1, 2, 3, 5, 6], optimum=5)
    try:
        check_certificate(star, malformed)
    except AssertionError:
        report['malformed_certificate_rejected'] = True
    else:
        raise AssertionError('Accepted a vertex outside the graph domain')
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
            beta, sf, size, minimal_sets = literal_optima(literal_cover(h))
            assert beta == sf == cert['optimum']
            for selected in minimal_sets:
                witness = minimal_forming_certificate(h, selected)
                assert witness['size'] <= n+witness['independent_defect'] <= n+delta
                if len(selected) == cert['optimum']:
                    assert witness['independent_defect'] == delta
                    reserved = set(witness['isolated_neighbours'])
                    pairs = [set(values) for i, values in witness['empty_rung_deletions'].items()
                             if i not in reserved]
                    assert all(len(values) == 2 for values in pairs)
                    assert sum(map(len, pairs)) == len(set().union(*pairs))
                # Independently recalculate every returned failed-formation vertex.
                for s, failures in witness['deletion_witnesses'].items():
                    reduced = selected-{s}
                    for x in failures:
                        assert len(literal_cover(h)[x] & reduced) <= 1
                        assert all(not literal_cover(h)[v] & reduced
                                   for v in literal_cover(h)[x] & reduced)
                report['minimal_forming_sets'] += 1
                report['empty_rung_budgets'] += len(witness['empty_rung_deletions'])
                report['reserved_empty_rungs'] += len(witness['isolated_neighbours'])
                report['high_rung_occurrences'] += len(witness['high_rungs'])
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
            minimal_forming_certificate(h, cert['dissociation'])
            report['larger_certificates'] += 1
    report['SF_counterexamples_in_finite_run'] = examples
    report['SF_scope'] = 'All minimal forming sets checked on small bases; general two-per-empty-rung proof in note establishes all-base formula'
    report['status'] = 'PASS'
    Path('output').mkdir(exist_ok=True)
    Path('output/extended-double-cover-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
