"""Literal independent subset, matching and partial-colouring controls.

Project dependencies: paired_graphs.py and its matcher extended_double_cover.py.
No imports from other checkers or their helper modules.
"""
from itertools import combinations
from pathlib import Path
import json
import random

from paired_graphs import (direct_terminal_completion, minimal_forming_budget,
                           near_complete_base, near_complete_certificate,
                           paired_optimum_certificate, prism_optimum_certificate,
                           representative_budget)


def base(n, edges):
    h = [set() for _ in range(n)]
    for u, v in edges:
        h[u].add(v)
        h[v].add(u)
    return h


def literal_prism(h):
    n = len(h)
    g = [set() for _ in range(2*n)]
    for i in range(n):
        g[i].add(n+i)
        g[n+i].add(i)
        for j in h[i]:
            g[i].add(j)
            g[n+i].add(n+j)
    return g


def unformed(g, selected):
    return {x for x in range(len(g)) if x not in selected
            and len(g[x] & selected) < 2
            and all(not g[y] & selected for y in g[x] & selected)}


def literal_optima(g):
    adj = [sum(1 << u for u in row) for row in g]
    end, beta, sf, minimal = 1 << len(g), 0, 0, []
    forming = bytearray(end)
    for bits in range(end):
        active, dissociation = 0, True
        for v in range(len(g)):
            if bits >> v & 1:
                degree = (adj[v] & bits).bit_count()
                if degree:
                    active |= 1 << v
                if degree > 1:
                    dissociation = False
        if dissociation:
            beta = max(beta, bits.bit_count())
        ok = all((adj[v] & bits).bit_count() >= 2 or adj[v] & active
                 for v in range(len(g)) if not bits >> v & 1)
        forming[bits] = ok
        if ok and all(not forming[bits ^ (1 << v)] for v in range(len(g)) if bits >> v & 1):
            sf = max(sf, bits.bit_count())
            minimal.append({v for v in range(len(g)) if bits >> v & 1})
    return beta, sf, minimal, end


def colour_optimum(g):
    labels, best, count = [0]*len(g), 0, 0
    def visit(v, used):
        nonlocal best, count
        if v == len(g):
            count += 1
            for x, colour in enumerate(labels):
                if not colour:
                    continue
                closed = [labels[u] for u in g[x] | {x} if labels[u]]
                if 2*closed.count(colour) < len(closed):
                    return
            best = max(best, used)
            return
        for colour in range(used+2):
            labels[v] = colour
            visit(v+1, max(used, colour))
    visit(0, 0)
    return best, count


def matchings(g, remaining=None):
    remaining = set(range(len(g))) if remaining is None else remaining
    if not remaining:
        yield set()
        return
    u = min(remaining)
    yield from matchings(g, remaining-{u})
    for v in g[u] & remaining:
        for other in matchings(g, remaining-{u, v}):
            yield other | {(min(u, v), max(u, v))}


def check_dual(h, cert):
    n = len(h)
    matching = cert['double_matching']
    assert all(type(v) is int and 0 <= v < n for edge in matching for v in edge)
    assert len({u for u, _ in matching}) == len({v for _, v in matching}) == len(matching)
    assert all(v in h[u] for u, v in matching)
    left = set(cert['double_vertex_cover_left'])
    right = set(cert['double_vertex_cover_right'])
    assert left <= set(range(n)) and right <= set(range(n))
    assert len(left)+len(right) == len(matching)
    assert all(u in left or v in right for u in range(n) for v in h[u])
    independent, neighbours = set(cert['critical_independent']), set(cert['critical_neighbours'])
    assert independent <= set(range(n)) and neighbours <= set(range(n))
    assert not independent & neighbours
    assert {v for u in independent for v in h[u]} == neighbours
    assert len(independent)-len(neighbours) == n-len(matching) == cert['deficiency']
    assert cert['optimum'] == 2*n-len(matching)


def check_prism_certificate(h):
    g = literal_prism(h)
    cert = prism_optimum_certificate(h)
    check_dual(h, cert['matching_dual'])
    selected = set(cert['forming'])
    assert not unformed(g, selected)
    assert len(selected) == cert['optimum']
    for s, x in cert['deletion_witnesses'].items():
        assert x in unformed(g, selected-{s})
    return cert


def main():
    report = dict(prism_bases=0, prism_literal_subsets=0, prism_minimal_sets=0,
                  partial_colourings=0, colour_models=0, paired_graphs=0,
                  paired_literal_subsets=0, paired_minimal_sets=0,
                  feasible_pairs=0, independent_selections=0, mixed_layer_selections=0,
                  direct_completions=0, positive_extremal_bases=0)
    for n in range(6):
        edges = list(combinations(range(n), 2))
        for bits in range(1 << len(edges)):
            h = base(n, [e for k, e in enumerate(edges) if bits >> k & 1])
            g = literal_prism(h)
            cert = check_prism_certificate(h)
            beta, sf, minimal, subsets = literal_optima(g)
            assert sf == cert['optimum']
            assert sf-beta <= max(0, n-4)
            if n >= 5:
                matching_complement = all(n-1-len(row) <= 1 for row in h)
                assert (beta == 4) == matching_complement
                assert (sf-beta == n-4) == matching_complement
                report['positive_extremal_bases'] += sf-beta == n-4
            for selected in minimal:
                budget = minimal_forming_budget(g, selected)
                assert len(selected) <= n+budget['defects'] <= sf
                if len(selected) == sf:
                    assert budget['defects'] == cert['matching_dual']['deficiency']
                    available = [set(row) for i, row in budget['budgets'].items()
                                 if i not in budget['reserved']]
                    assert all(len(row) == 2 for row in available)
                    assert sum(map(len, available)) == len(set().union(*available))
            if n <= 4:
                psi, count = colour_optimum(g)
                assert beta == psi == sf
                report['colour_models'] += 1
                report['partial_colourings'] += count
            report['prism_bases'] += 1
            report['prism_literal_subsets'] += subsets
            report['prism_minimal_sets'] += len(minimal)
    # Four symmetric edge patterns per orbit pair: none, parallel, cross, both.
    for n in range(5):
        pairs = list(combinations(range(n), 2))
        for presentation in range(4**len(pairs)):
            physical = [(i, n+i) for i in range(n)]
            quotient = []
            for k, (i, j) in enumerate(pairs):
                pattern = presentation // 4**k % 4
                if pattern:
                    quotient.append((i, j))
                if pattern & 1:
                    physical.extend(((i, j), (n+i, n+j)))
                if pattern & 2:
                    physical.extend(((i, n+j), (j, n+i)))
            g, h = base(2*n, physical), base(n, quotient)
            cert = paired_optimum_certificate(g)
            assert cert['quotient'] == h
            check_dual(h, cert['matching_dual'])
            beta, sf, minimal, subsets = literal_optima(g)
            assert beta <= sf <= cert['optimum']
            for selected in minimal:
                budget = minimal_forming_budget(g, selected)
                assert len(selected) <= n+budget['defects'] <= cert['optimum']
            if n <= 3:
                optimum = 0
                for actual in matchings(g):
                    occupied = {v for e in actual for v in e}
                    q = sum(1 << v for v in range(2*n) if v not in occupied)
                    bits = q
                    while True:
                        selected = {v for v in range(2*n) if bits >> v & 1}
                        if all(len(g[t] & (selected | occupied)) <= 1 for t in selected):
                            result = representative_budget(g, actual, selected)
                            optimum = max(optimum, result['objective'])
                            assert result['objective'] <= cert['optimum']
                            report['feasible_pairs'] += 1
                            if all(not g[t] & selected for t in selected):
                                auxiliary = direct_terminal_completion(g, actual, selected)
                                mate = {v: u for edge in auxiliary for v, u in (edge, edge[::-1])}
                                assert len(mate) == 2*n == 2*len(auxiliary)
                                assert all(v in g[u] for u, v in auxiliary)
                                assert all(mate[t] not in selected | occupied for t in selected)
                                report['independent_selections'] += 1
                                report['mixed_layer_selections'] += bool(selected & set(range(n))) and bool(selected & set(range(n, 2*n)))
                                report['direct_completions'] += 1
                        if bits == 0:
                            break
                        bits = (bits-1) & q
                assert optimum == cert['optimum']
            report['paired_graphs'] += 1
            report['paired_literal_subsets'] += subsets
            report['paired_minimal_sets'] += len(minimal)
    report['near_complete_literal_colours'] = []
    for missing in range(3):
        h = near_complete_base(5, missing)
        cert = near_complete_certificate(5, missing)
        psi, count = colour_optimum(literal_prism(h))
        assert psi == cert['psi']
        report['near_complete_literal_colours'].append(dict(n=5, missing=missing, psi=psi, colourings=count))
        report['partial_colourings'] += count
        report['colour_models'] += 1
    rng = random.Random(2026111204)
    report['larger_prism_certificates'] = 0
    for n in (8, 17, 64, 257):
        for probability in (0.01, 0.04, 0.15):
            h = base(n, [(u, v) for u in range(n) for v in range(u+1, n)
                         if rng.random() < probability])
            check_prism_certificate(h)
            report['larger_prism_certificates'] += 1
    report['near_complete_constructed_certificates'] = 0
    for n in (5, 6, 7, 8, 16, 31, 64, 129):
        for missing in sorted({0, 1, 2, n//2}):
            h = near_complete_base(n, missing)
            cert = near_complete_certificate(n, missing)
            g = literal_prism(h)
            assert all(len(g[v] & set(cert['dissociation'])) <= 1 for v in cert['dissociation'])
            assert cert['optimum'] == n
            check_prism_certificate(h)
            report['near_complete_constructed_certificates'] += 1
    report['status'] = 'PASS'
    Path('output').mkdir(exist_ok=True)
    Path('output/paired-graph-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
