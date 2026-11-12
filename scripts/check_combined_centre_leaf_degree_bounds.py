#!/usr/bin/env python3
"""Physical cut and exact-integer controls for the combined degree bounds.

Standard library only. Infinite-parameter claims use the companion proof.
The imported modules' standalone main suites are not run by this entry point.
"""
from collections import Counter
import json
from pathlib import Path

import check_selected_star_general_budget as old
import check_full_degree_capacity as cut
import check_free_unused_degree_refinement as prev

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')


def audit(g, S, beta, counts):
    colors = old.colors(g)
    C, leaves, I = old.structure(g, S)
    L = set(leaves)
    d = len(S) - beta
    minimum, maximum = min(map(len, g)), max(map(len, g))
    for values, W, U, P, incidences in cut.allocations(g, S):
        c, q, s, a, b2, b3, mu, m, z0, u = values
        h = {i: len(g[i] & W) for i in I}
        I1 = {i for i in I if h[i] == 1}
        Ip = {i for i in I if h[i] > 0}
        I0 = I - Ip
        Z = {x for x in U if g[x] & S <= C | Ip}
        free = len(Z)
        Q = C | I1
        K = Q | L | P | I0
        assert len(Q) == c + a
        assert len(K) == c + len(L) + a + m + z0
        assert U - Z == {x for x in U if g[x] & (L | P | I0)}
        assert sum(len(g[x] & W) for x in C) == q
        assert all(len(g[x] & W) == 1 for x in L)
        assert all(not (g[x] & W) for x in P | I0)
        assert sum(len(g[x] & S) for x in C) == 2*c + s
        assert all(len(g[x] & S) == 1 for x in L | P)
        assert all(not (g[x] & S) for x in I)

        enlarged = []
        for side in (0, 1):
            witnesses = {w for w in W if colors[w] == side}
            helpers = {i for i in I if g[i] & witnesses}
            D = ((S - C) | witnesses) - helpers
            added = {x for x in Z if colors[x] == side}
            assert all(not (g[x] & D) for x in added)
            assert old.diss(g, D | added)
            assert len(D | added) <= beta
            enlarged.append(D | added)

        t = a + b2 + b3
        H = b3 + mu
        Tp = t - s - q
        J = c + s + 2*q - t - b2 - 2*b3
        R = c - q + b2 + b3 - mu
        repair = q + s + 2*mu - 2*b2
        eta = len(g) - 12*d
        assert J >= 0 and repair >= 0 and R >= 2*d and Tp-free >= 2*d
        assert sum(map(len, enlarged)) == 2*len(S)+s+q-t+free
        assert 4*d <= 2*(a+H-free)-(s+q)
        assert 2*c == J+R+Tp+H and 2*c >= 4*d+free+H
        assert 2*len(g) == 5*J+5*R+7*Tp+5*H+6*s+4*q+2*(m+z0+u)
        assert 2*eta >= 2*u+7*free+5*H+6*s+4*q+2*(m+z0)
        assert c-q+t+m+z0-u >= 2*d

        centre_edges = sum(len(g[x] & U) for x in C)
        q_edges = sum(len(g[x] & U) for x in Q)
        all_edges = sum(len(g[x] & U) for x in K)
        leaf_edges = sum(len(g[x] & U) for x in L)
        assert q_edges == sum(len(g[x] & Q) for x in U)
        assert all_edges == sum(len(g[x] & K) for x in U)
        assert q_edges <= (maximum-1)*u+free
        assert all_edges <= maximum*u
        assert all(len(g[x] & Q) <= maximum-1 for x in U-Z)
        for lower in range(2, minimum+1):
            assert centre_edges >= (lower-2)*c-s-q
            assert leaf_edges >= (lower-2)*(2*c+s)
            short_demand = (lower-2)*c+(lower-1)*a-s-q
            long_demand = 3*(lower-2)*c+(lower-1)*a+(lower-3)*s-q
            long_demand += (lower-1)*m+lower*z0
            assert short_demand <= q_edges
            assert long_demand <= all_edges
            for upper in range(maximum, maximum+3):
                A = upper-1
                assert short_demand <= A*u+free
                assert long_demand <= upper*u
                assert 4*(2*lower-3)*d <= (
                    2*A*u+lower*H-(lower-3)*(s+q)-3*(lower-2)*free)
                rem1 = (7*A+3*(lower-2))*free+(5*A-lower)*H
                rem1 += (6*A+lower-3)*s+(4*A+lower-3)*q+2*A*(m+z0)
                assert 2*A*eta-4*(2*lower-3)*d >= rem1 >= 0
                assert 2*(8*lower-14)*d <= (
                    2*upper*u+(4-lower)*H-(3*lower-7)*s-(lower-3)*q
                    -(5*lower-8)*free-2*(lower-1)*m-2*lower*z0)
                rem2 = (7*upper+5*lower-8)*free+(5*upper+lower-4)*H
                rem2 += (6*upper+3*lower-7)*s+(4*upper+lower-3)*q
                rem2 += 2*(upper+lower-1)*m+2*(upper+lower)*z0
                assert 2*upper*eta-2*(8*lower-14)*d >= rem2 >= 0
                den1, den2 = 12*A+4*lower-6, 12*upper+8*lower-14
                assert d <= A*len(g)//den1
                assert d <= upper*len(g)//den2
                if lower >= 3 and d > 0:
                    assert den1*d < A*len(g)
                if upper < 4*lower-7 and d > 0:
                    assert den2*d < upper*len(g)
                if lower >= 3:
                    assert upper*den1 < A*den2
                counts['degree_parameter_checks'] += 1
        counts['allocations'] += 1
        counts['actual_enlarged_exchanges'] += 2
        counts['centre_to_W_incidences'] += q
        counts['physical_short_cut_edges'] += q_edges
        counts['physical_long_cut_edges'] += all_edges
        counts['with_free_vertices'] += bool(free)
        counts['with_nonfree_vertices'] += u > free
        counts['positive_gap_allocations'] += d > 0
        counts['direct_only_allocations'] += q > 0
        counts['helper_ge3_allocations'] += b3 > 0
        counts['selected_edge_allocations'] += m > 0
        counts['untouched_isolate_allocations'] += z0 > 0


def controls():
    total, ranges = Counter(), {}
    for label, g in prev.small_graphs():
        beta, subsets = old.one_part_beta(g, old.colors(g))
        assert beta == old.beta_literal(g)
        if len(g) <= 7:
            assert beta == old.beta_full_subsets(g)
        formed = cut.literals(g)
        row = Counter()
        for mask, ok in enumerate(formed):
            row['selected_subsets'] += 1
            if not ok or any(formed[mask ^ (1 << x)] for x in range(len(g))
                             if mask >> x & 1):
                continue
            S = {x for x in range(len(g)) if mask >> x & 1}
            if old.structure(g, S) is None:
                continue
            row['eligible_minimal_selections'] += 1
            audit(g, S, beta, row)
        row['graph_inputs'] += 1
        row['one_part_subsets'] += subsets
        total.update(row)
        ranges.setdefault(label, Counter()).update(row)
    return {'totals': dict(sorted(total.items())),
            'ranges': {k: dict(sorted(v.items())) for k, v in sorted(ranges.items())},
            'scope': 'Same 455 explicit graph inputs as the imported free-unused checker. '
                     'All eligible selections and all permitted allocations in each stated range; '
                     'graphs outside the degree theorem test cuts and exchanges only.'}


def targets():
    rows = []
    models = [(f'universal_padding_t{t}', prev.pad(2, 2, t)) for t in (1, 2, 3)]
    models += [('multiple_witness_choices', old.multiple_options()),
               ('direct_large_helper', old.fixture([(0, 0)]*3+[(1, 0)]*3, dense=True)),
               ('shared_helper_centres', old.shared_two_centres()),
               ('surplus_edges_untouched', old.fixture(
                   [(0, None), (0, 0), (0, 0), (1, None), (1, 0)], True, True))]
    for name, (g, S) in models:
        assert old.minimal(g, S) and old.structure(g, S) is not None
        beta, subsets = old.one_part_beta(g, old.colors(g))
        if len(g) <= 24:
            assert beta == old.beta_literal(g)
        counts = Counter()
        audit(g, S, beta, counts)
        rows.append({'name': name, 'order': len(g), 'selected': len(S), 'beta': beta,
                     'minimum_degree': min(map(len, g)),
                     'maximum_degree': max(map(len, g)), 'one_part_subsets': subsets,
                     'checks': dict(sorted(counts.items()))})
    return rows


def arithmetic():
    # The derivation's two key substitutions are equalities plus these
    # nonnegative multiples of the original graph-ledger slacks.
    def identities(v, d, lower, upper, free):
        c, q, s, a, b2, b3, mu, m, z0, u = v
        H, A = b3+mu, upper-1
        t = a+b2+b3
        J, R, Tp = c+s+2*q-t-b2-2*b3, c-q+b2+b3-mu, t-s-q
        repair = q+s+2*mu-2*b2
        eta = 5*c+2*s+q+t+m+z0+u-12*d
        x = a+H-(s+q)/2-free-2*d
        y = c-2*d-(free+H)/2
        assert 2*x == 2*(Tp-free-2*d)+repair
        assert 2*y == J+(R-2*d)+(Tp-free-2*d)
        short = (lower-2)*c+(lower-1)*a-s-q
        long = 3*(lower-2)*c+(lower-1)*a+(lower-3)*s-q
        long += (lower-1)*m+lower*z0
        short_core = 2*(2*lower-3)*d-lower*H/2
        short_core += (lower-3)*(s+q)/2+(3*lower-4)*free/2
        long_core = (8*lower-14)*d-(4-lower)*H/2
        long_core += (3*lower-7)*s/2+(lower-3)*q/2+(5*lower-8)*free/2
        long_core += (lower-1)*m+lower*z0
        assert short == short_core+(lower-2)*y+(lower-1)*x
        assert long == long_core+3*(lower-2)*y+(lower-1)*x
        assert 2*(eta-u)-7*free-5*H-6*s-4*q-2*(m+z0) == (
            5*J+5*(R-2*d)+7*(Tp-free-2*d))
    # Fractions prevent accidental floating-point agreement at huge integers.
    from fractions import Fraction
    checks = 0
    for lower in range(2, 13):
        for upper in range(lower, lower+12):
            for j in range(13):
                v = [Fraction(j == i) for i in range(10)]
                d, free = Fraction(j == 10), Fraction(j == 11)
                identities(v, d, lower, upper, free)
                checks += 1
    for exponent in (64, 401, 1024):
        scale = 10**exponent+7
        identities([Fraction((i+1)*scale) for i in range(10)],
                   Fraction(11*scale), 7, 12, Fraction(12*scale))
    return {'exact_basis_checks': checks, 'large_integer_checks': 3,
            'arbitrary_precision': True, 'graph_sharpness_claim': False}


def main():
    report = {'status': 'PASS', 'graph_controls': controls(), 'targeted': targets(),
              'arithmetic': arithmetic(),
              'scope': 'Both physical cuts, exact ledgers and remainders. '
                       'All-graph statements rely on the written proof; no sharpness claim.'}
    out = Path(__file__).resolve().parents[1]/'output/combined-centre-leaf-degree-check.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, sort_keys=True, indent=2)+'\n')
    print(json.dumps({'status': 'PASS', 'totals': report['graph_controls']['totals'],
                      'targeted_models': len(report['targeted'])}, sort_keys=True))


if __name__ == '__main__':
    main()
