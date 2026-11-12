#!/usr/bin/env python3
"""Physical exchanges, exact optima and integral stability ledgers."""
from collections import Counter
from fractions import Fraction
from itertools import combinations, permutations, product
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from subcubic_star_stability import exchanges
from compact_subcubic_selected_stars import base
from check_compact_subcubic_selected_stars import exact, diss, literal
import check_selected_star_general_budget as old
import check_full_degree_capacity as cut

if not __debug__:
    raise RuntimeError('Assertions must be enabled')


def private_beta(g, q):
    order = sorted(q)
    index = {a: j for j, a in enumerate(order)}
    return exact([{index[b] for b in g[a] & q} for a in order])['beta']


def audit(g, S, beta, allocation, count):
    v, W, U, P, unused = allocation
    c, q, s, a, b2, b3, mu, m, z0, u = v
    C, leaves, I = old.structure(g, S)
    assert min(map(len, g)) >= 2 and max(map(len, g)) <= 3
    d = len(S)-beta
    h = {i: len(g[i] & W) for i in I}
    Z = {v for v in U if g[v] & S <= C | {i for i in I if h[i]}}
    free = len(Z)
    J = c+s+2*q-a-2*b2-3*b3
    R = c-q+b2+b3-mu
    Tp = a+b2+b3-s-q
    H = b3+mu
    r, x = R-2*d, Tp-free-2*d
    eta = len(g)-13*d
    assert min(J, r, x, eta) >= 0
    assert a <= 2*u+free
    assert 4*eta >= 10*(J+r)+14*(free+x)+8*H+13*s+9*q+4*(m+z0)
    model = exchanges(g, S, C, I, W)
    pre = model['preliminary']
    A = {row['a'] for row in pre}
    c0 = len(pre)
    b = c-c0
    bad = model['bad_private_vertices']
    assert c0 >= a-3*s-3*q
    assert 2*b <= J+r+x+3*H+5*s+5*q
    baseline = model['baseline']
    assert diss(g, baseline)
    assert all(not (g[v] & baseline) for v in A)
    ba = private_beta(g, A)
    assert 10*ba >= 5*c0+bad
    assert len(baseline)+ba <= beta
    assert bad <= 5*(c-2*d+b)
    assert diss(g, model['exchange']) and len(model['exchange']) <= beta
    assert d <= b+bad
    assert 2*d <= 11*(J+r+x)+5*free+23*H+30*s+30*q
    assert 263*d <= 20*len(g)
    count['allocations'] += 1
    count['direct_q_allocations'] += q > 0
    count['surplus_leaf_allocations'] += s > 0
    count['large_helper_allocations'] += b3 > 0
    count['preliminary_blocks'] += c0
    count['retained_C4_blocks'] += len(model['final'])
    count['positive_gap_allocations'] += d > 0
    count['physical_exchanges'] += 2
    return {'n': len(g), 'selected': len(S), 'beta': beta, 'd': d,
            'parameters': v, 'J': J, 'r': r, 'x': x, 'g': free,
            'eta': eta, 'preliminary': c0, 'bad_private': bad,
            'final_blocks': len(model['final']), 'exchange_size': len(model['exchange'])}


def small_graphs():
    count = Counter()
    for left, right in ((2, 2), (2, 3), (3, 3), (3, 4)):
        edges = list(product(range(left), range(left, left+right)))
        for bits in range(1 << len(edges)):
            g = old.graph(left+right, [e for j, e in enumerate(edges) if bits >> j & 1])
            if min(map(len, g)) < 2 or max(map(len, g)) > 3:
                continue
            beta = exact(g)['beta']
            assert beta == old.beta_full_subsets(g)
            formed = cut.literals(g)
            for mask, ok in enumerate(formed):
                count['selected_subsets'] += 1
                if not ok or any(formed[mask ^ (1 << j)] for j in range(len(g)) if mask >> j & 1):
                    continue
                S = {j for j in range(len(g)) if mask >> j & 1}
                if old.structure(g, S) is None:
                    continue
                count['eligible_minimal_sets'] += 1
                for allocation in cut.allocations(g, S):
                    audit(g, S, beta, allocation, count)
            count['graphs'] += 1
    return dict(sorted(count.items()))


def kernel(r, pairs):
    blocks = 4*r
    g = [set() for _ in range(8*blocks)]
    def edge(a, b):
        assert a != b and b not in g[a]
        g[a].add(b)
        g[b].add(a)
    for j in range(blocks):
        for t in range(5):
            edge(6*j+t, 6*j+t+1)
    for h in range(0, blocks, 4):
        for t in range(4):
            edge(6*(h+t), 6*(h+(t+1) % 4))
    for a, b in pairs:
        edge(6*a+4, 6*b+4)
    S = {6*j+t for j in range(blocks) for t in (1, 2, 3, 5)}
    # Complete each pair of same-colour i's by a square with two new isolates.
    for h in range(0, blocks, 4):
        for t, pair in enumerate(((h, h+2), (h+1, h+3))):
            o = 6*blocks+8*(h//4)+4*t
            for j in range(4):
                edge(o+j, o+(j+1) % 4)
            edge(6*pair[0]+5, o+1)
            edge(6*pair[1]+5, o+3)
            S.update((o, o+2))
    C = {6*j+2 for j in range(blocks)}
    I = {6*j+5 for j in range(blocks)} | (S-set(range(6*blocks)))
    W = {6*j+t for j in range(blocks) for t in (0, 4)}
    result = exchanges(g, S, C, I, W)
    assert old.colors(g)
    assert all(literal(g, S, v) for v in range(len(g)) if v not in S)
    for v in S:
        near = {v} | g[v] | set().union(*(g[u] for u in g[v]))
        assert any(not literal(g, S-{v}, u) for u in near-(S-{v}))
    assert diss(g, result['exchange']) and len(result['exchange']) == len(S)
    assert len(result['final']) == blocks
    assert min(map(len, g)) == 2 and max(map(len, g)) == 3
    return {'private_C4s': r, 'matching': pairs, 'n': len(g), 'selected': len(S),
            'exchange_size': len(result['exchange']), 'state_A': sorted(result['state_A_private']),
            'quotient_loops': sum(a//4 == b//4 for a, b in pairs),
            'helped_isolates': blocks-2*len(pairs)}


def orientation_controls():
    rows = []
    for r in (1, 2):
        left, right = list(range(0, 4*r, 2)), list(range(1, 4*r, 2))
        for perm in permutations(right):
            for mask in range(1 << len(left)):
                rows.append(kernel(r, [(a, b) for j, (a, b) in enumerate(zip(left, perm)) if mask >> j & 1]))
    rng = random.Random(2026111207)
    for r in (3, 4, 8, 16, 32):
        for _ in range(6):
            left, right = list(range(0, 4*r, 2)), list(range(1, 4*r, 2))
            rng.shuffle(right)
            rows.append(kernel(r, [(a, b) for a, b in zip(left, right) if rng.randrange(3)]))
    return rows


def degree_two_margin():
    rows = []
    for cycle in (False, True):
        for n in range(1 if not cycle else 4, 33, 1 if not cycle else 2):
            g = [{u for u in (v-1, v+1) if 0 <= u < n} for v in range(n)]
            if cycle:
                g[0].add(n-1)
                g[n-1].add(0)
            beta = exact(g)['beta']
            assert beta == (2*n//3 if cycle else (2*n+2)//3)
            bad = 0 if cycle and n == 4 else n
            assert 10*beta >= 5*n+bad
            rows.append({'cycle': cycle, 'n': n, 'beta': beta, 'bad': bad})
    return rows


def main():
    count = Counter()
    g, S, D, col = base(4)
    beta = exact(g)['beta']
    assert beta == 39
    allocation = next(cut.allocations(g, S))
    positive = audit(g, S, beta, allocation, count)
    coefficients = {'J': (Fraction(11, 2), Fraction(5, 2)),
                    'r': (Fraction(11, 2), Fraction(5, 2)),
                    'g': (Fraction(5, 2), Fraction(7, 2)),
                    'x': (Fraction(11, 2), Fraction(7, 2)),
                    'H': (Fraction(23, 2), Fraction(2)),
                    's': (Fraction(15), Fraction(13, 4)),
                    'q': (Fraction(15), Fraction(9, 4))}
    assert all(3*a <= 20*b for a, b in coefficients.values())
    report = {'degree_two_margin': degree_two_margin(), 'small_graphs': small_graphs(),
              'orientation_controls': orientation_controls(), 'positive64': positive,
              'positive_checks': dict(count),
              'coefficient_comparison': {k: [str(a), str(b)] for k, (a, b) in coefficients.items()},
              'scope': 'General proof gives the 20/263 coefficient; exhaustive small selections, partial helped '
                       'matchings with loops/isolates and a separately exact positive64 graph validate physical '
                       'exchanges. No asymptotic sharpness or exact SF2 claim.'}
    output = ROOT/'output/subcubic-star-stability-check.json'
    output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'result': 'PASS', 'small_graphs': report['small_graphs'],
                      'orientation_controls': len(report['orientation_controls']),
                      'positive64': positive, 'report_bytes': output.stat().st_size}))


if __name__ == '__main__':
    main()
