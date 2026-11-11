#!/usr/bin/env python3
"""Standalone literal controls for SHARP_SELECTED_STAR_GAP.md.

No project imports. Small graphs enumerate all selected sets and all permitted
witness choices. All labelled repair matchings are checked, including parallel
edge alternatives. Finite controls support the general proof in the note.
"""
import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')

def graph(n, edges):
    g = [set() for _ in range(n)]
    for u, v in edges:
        assert u != v and 0 <= u < n and 0 <= v < n
        g[u].add(v)
        g[v].add(u)
    return g


def literal(g, s, x):
    # Explicit triples, independent of the witness-neighbourhood classification.
    return any((a in g[x] and b in g[x]) or
               (x in g[a] and b in g[a]) or
               (x in g[b] and a in g[b]) for a, b in combinations(sorted(s), 2))


def forming(g, s):
    return all(literal(g, s, x) for x in range(len(g)) if x not in s)


def minimal(g, s):
    return forming(g, s) and all(not forming(g, s - {v}) for v in s)


def diss(g, s):
    return all(len(g[v] & s) <= 1 for v in s)


def colors(g):
    col = {}
    for root in range(len(g)):
        if root in col:
            continue
        col[root] = 0
        todo = [root]
        while todo:
            u = todo.pop()
            for v in sorted(g[u]):
                if v not in col:
                    col[v] = 1 - col[u]
                    todo.append(v)
                assert col[v] != col[u]
    return col


def structure(g, s):
    unseen, c, leaves, isolates = set(s), set(), [], set()
    while unseen:
        todo, comp = [min(unseen)], set()
        while todo:
            v = todo.pop()
            if v in comp:
                continue
            comp.add(v)
            todo.extend((g[v] & s) - comp)
        unseen -= comp
        if len(comp) == 1:
            isolates |= comp
        elif len(comp) > 2:
            centres = [v for v in comp if g[v] & comp == comp - {v}]
            if len(centres) != 1:
                return None
            centre = centres[0]
            if any(g[v] & comp != {centre} for v in comp - {centre}):
                return None
            c.add(centre)
            leaves.extend(sorted(comp - {centre}))
    return c, sorted(leaves), isolates


def beta_literal(g):
    # Exact maximum by literal forbidden triples, not the exchange construction.
    triples = sorted({sum(1 << v for v in (c, a, b))
                      for c in range(len(g)) for a, b in combinations(g[c], 2)})
    @lru_cache(None)
    def solve(mask):
        for triple in triples:
            if mask & triple == triple:
                return max(solve(mask ^ (1 << v)) for v in range(len(g))
                           if triple >> v & 1)
        return mask.bit_count()
    return solve((1 << len(g)) - 1)


def beta_full_subsets(g):
    """Independent full-subset maximum using literal actual-star triples."""
    triples = {sum(1 << v for v in (centre,a,b))
               for centre in range(len(g)) for a,b in combinations(g[centre],2)}
    best = 0
    for mask in range(1 << len(g)):
        size = mask.bit_count()
        if size > best and not any(mask & triple == triple for triple in triples):
            best = size
    return best


def local_literal(g, s, x):
    """Enumerate actual stars at their centres; no scan of all selected pairs."""
    for centre in sorted({x} | (g[x] & s)):
        for a, b in combinations(sorted(v for v in g[centre] if v == x or v in s), 2):
            if x in (centre, a, b):
                return True
    return False


def all_matchings(edges):
    """Every labelled matching; parallel edges remain distinct choices."""
    result = []
    def visit(j, used, chosen):
        if j == len(edges):
            result.append(tuple(chosen))
            return
        visit(j + 1, used, chosen)
        c, i, _, _ = edges[j]
        if c not in used and i not in used:
            visit(j + 1, used | {c, i}, chosen + [j])
    visit(0, set(), [])
    return result


def augmenting_matching(edges):
    """Independent cardinality algorithm on unlabelled centre/helper pairs."""
    adj = {}
    for c, i, _, _ in edges:
        adj.setdefault(c, set()).add(i)
    mate = {}
    def extend(c, seen):
        for i in sorted(adj[c]):
            if i in seen:
                continue
            seen.add(i)
            if i not in mate or extend(mate[i], seen):
                mate[i] = c
                return True
        return False
    for c in sorted(adj):
        extend(c, set())
    return len(mate)


def equality_template(g, s, centres, leaves, isolates, ws, d):
    if d <= 0 or len(g) != 12 * d:
        return False
    c = len(centres)
    assert c == 2*d and len(leaves) == 2*c
    assert len(isolates) == c and len(s) == 4*c
    assert set(range(len(g))) - s == set(ws)
    assert all(len(g[v]) == 2 for v in centres | set(leaves))
    assert all(len(g[v]) == 1 for v in isolates)
    for centre in centres:
        own = [w for leaf, w in zip(leaves, ws) if centre in g[leaf]]
        assert len(own) == 2
        assert sorted(len(g[w] & s) for w in own) == [1, 2]
    assert sum(len(g[w] & isolates) for w in ws) == c
    return True


def audit(g, s, beta, col, counts):
    st = structure(g, s)
    assert st is not None
    centres, leaves, isolates = st
    owner = {ell: next(iter(g[ell] & centres)) for ell in leaves}
    outside = set(range(len(g))) - s
    options = [tuple(w for w in sorted(outside) if not literal(g, s-{ell}, w))
               for ell in leaves]
    assert all(options)
    for ell, choices in zip(leaves, options):
        for w in choices:
            assert ell in g[w] and (g[w] & s)-{ell} <= isolates
            assert len(g[w] & s) in (1, 2)
    clean = {owner[ell] for ell, choices in zip(leaves, options)
             if any(g[w] & s == {ell} for w in choices)}
    direct = sorted(centres-clean)
    direct_options = [tuple(w for w in sorted(outside)
                            if centre in g[w] and not literal(g, s-{centre}, w))
                      for centre in direct]
    assert all(direct_options)
    for centre, choices in zip(direct, direct_options):
        for w in choices:
            assert (g[w] & s)-{centre} <= isolates
            assert len(g[w] & s) in (1, 2)
    c, e, p, q = len(centres), len(leaves), len(clean), len(direct)
    surplus = e-2*c
    assert surplus >= 0 and p+q == c
    remainder = s-centres-set(leaves)
    assert isolates <= remainder
    d = len(s)-beta
    assert d <= len(g)//12
    if g and min(map(len, g)) >= 2:
        assert d <= (len(g)-1)//12
        counts['minimum_degree_two_selections'] += 1
    rows = set()
    for leaf_ws in product(*options):
        designated = {owner[ell] for ell, w in zip(leaves, leaf_ws)
                      if g[w] & s == {ell}}
        if designated != clean:
            continue
        for centre_ws in product(*direct_options):
            ws = tuple(leaf_ws) + tuple(centre_ws)
            assert len(set(ws)) == len(ws)
            W = set(ws)
            h = {i: len(g[i] & W) for i in isolates}
            a = sum(v == 1 for v in h.values())
            b2 = sum(v == 2 for v in h.values())
            b3 = sum(v >= 3 for v in h.values())
            t = a+b2+b3
            assert a+2*b2+3*b3 <= sum(h.values()) <= c+surplus+2*q
            assert len(g) >= 5*c+2*surplus+q+t
            tleaf = sum(bool(g[i] & set(leaf_ws)) for i in isolates)
            # Two ACTUAL leaf exchange sets; no matching formula assumed.
            leaf_sets = []
            for side in (0, 1):
                kept = {w for w in leaf_ws if col[w] == side}
                helpers = {i for i in isolates if g[i] & kept}
                chosen = (s-centres-helpers) | kept
                assert diss(g, chosen) and len(chosen) <= beta
                leaf_sets.append(chosen)
            assert sum(map(len, leaf_sets)) == 2*(len(s)-c)+e-tleaf
            assert t >= tleaf >= 2*d+surplus
            base = []
            for side in (0, 1):
                chosen = {v for v in s|W if col[v] == side}
                chosen |= {v for v in remainder if col[v] != side
                           and (v not in isolates or h[v] < 2)}
                assert diss(g, chosen) and len(chosen) <= beta
                base.append(chosen)
            assert sum(map(len, base)) == 2*len(s)-p-b2-b3
            gamma = []
            for ell, w in zip(leaves, leaf_ws):
                helper = g[w] & isolates
                if helper and h[next(iter(helper))] == 2:
                    i = next(iter(helper))
                    assert col[owner[ell]] != col[i]
                    gamma.append((owner[ell], i, ell, w))
            matchings = all_matchings(gamma)
            mu = max(map(len, matchings))
            assert mu == augmenting_matching(gamma)
            assert sum(augmenting_matching([z for z in gamma if col[z[0]] == side])
                       for side in (0, 1)) == mu
            for matching in matchings:
                for side in (0, 1):
                    chosen = set(base[side])
                    repair = [gamma[j] for j in matching if col[gamma[j][0]] == side]
                    for centre, helper, ell, w in repair:
                        assert centre in chosen and w in chosen
                        assert ell not in chosen and helper not in chosen
                        chosen.remove(w)
                        chosen.update((ell, helper))
                    assert len(chosen) == len(base[side])+len(repair)
                    assert diss(g, chosen) and len(chosen) <= beta
                    counts['repaired_sets'] += 1
                counts['labelled_repair_matchings'] += 1
            # Every possible two-leaf restriction in this finite model.
            by_c = [list(combinations([ell for ell in leaves if owner[ell] == centre], 2))
                    for centre in sorted(centres)]
            for groups in product(*by_c):
                retained = {v for pair in groups for v in pair}
                reduced = [z for z in gamma if z[2] in retained]
                degrees = Counter(v for z in reduced for v in z[:2])
                assert all(v <= 2 for v in degrees.values())
                assert len(reduced) >= 2*b2-q-surplus
                assert 2*augmenting_matching(reduced) >= len(reduced)
                assert augmenting_matching(reduced) <= mu
                counts['two_leaf_restrictions'] += 1
            B0 = c+2*q-b2-2*b3
            C0 = c-q+b2+b3-mu
            D0 = q+surplus+2*mu-2*b2
            assert B0 >= 2*d and C0 >= 2*d and D0 >= 0
            assert 7*B0+13*C0+3*D0 == 20*c+4*q+3*surplus-b3-7*mu
            assert 10*B0+20*C0+5*D0 == 30*c+5*q+5*surplus-10*mu
            assert 4*len(g) >= 48*d+9*surplus+b3+7*mu
            assert 6*len(g) >= 72*d+q+13*surplus+10*mu
            counts['witness_assignments'] += 1
            counts['direct_only_assignments'] += q > 0
            counts['surplus_leaf_assignments'] += surplus > 0
            counts['large_helper_assignments'] += b3 > 0
            counts['parallel_gamma_assignments'] += len(gamma) > len({z[:2] for z in gamma})
            counts['witness_conflict_assignments'] += any(g[w] & W for w in W)
            counts['positive_gap_assignments'] += d > 0
            counts['equality_templates'] += equality_template(g, s, centres, leaves, isolates, leaf_ws, d)
            rows.add((c, surplus, q, a, b2, b3, mu, d))
    assert rows
    return sorted(rows)


def exhaustive():
    total, rows = Counter(), []
    for a, b in [(a, n-a) for n in range(7) for a in range(n+1)] + [(3, 4)]:
        count = Counter()
        possible = list(product(range(a), range(a, a+b)))
        for edge_mask in range(1 << len(possible)):
            g = graph(a+b, [edge for j, edge in enumerate(possible) if edge_mask >> j & 1])
            subsets = [{v for v in range(a+b) if mask >> v & 1}
                       for mask in range(1 << (a+b))]
            beta = beta_full_subsets(g)
            assert beta == beta_literal(g) == max(len(s) for s in subsets if diss(g, s))
            formed = [forming(g, s) for s in subsets]
            for mask, s in enumerate(subsets):
                count['selections'] += 1
                if not formed[mask] or any(formed[mask ^ (1 << v)] for v in s):
                    continue
                count['minimal_selections'] += 1
                st = structure(g, s)
                if st is None:
                    continue
                count['eligible_selections'] += 1
                count['with_stars'] += bool(st[0])
                audit(g, s, beta, {v: int(v >= a) for v in range(a+b)}, count)
            count['graphs'] += 1
        total.update(count)
        rows.append({'parts': [a, b], **dict(sorted(count.items()))})
    return {'range': 'all labelled graphs in each fixed bipartition of orders 0..6, plus (3,4)',
            'parts': rows, 'totals': dict(sorted(total.items()))}


def fixture(links, extras=False, dense=False):
    labels = sorted({(side, z) for side, z in links if z is not None})
    ids = {key: j+2 for j, key in enumerate(labels)}
    s, edges, ws = set(range(2+len(ids))), [], []
    n = len(s)
    for side, z in links:
        ell, w = n, n+1
        n += 2
        s.add(ell)
        edges += [(side, ell), (ell, w)]
        if z is not None:
            edges.append((w, ids[(side, z)]))
        ws.append((w, side))
    # Direct witnesses may be unchosen at clean centres; test unused vertices.
    for centre in (0, 1):
        edges.append((centre, n))
        n += 1
    if dense:
        edges += [(u, v) for u, a in ws for v, b in ws if a == 0 and b == 1]
    if extras:
        s.update((n, n+1, n+2))
        edges.append((n, n+1))
        n += 3
    return graph(n, edges), s


def gap_family(a, b):
    n = 6*(a+b)
    edges = [(6*j+u, 6*j+v) for j in range(a+b)
             for u, v in ((0, 1), (0, 2), (1, 4), (2, 5), (3, 5))]
    edges += [(6*i+u, 6*j+v) for i in range(a) for j in range(a, a+b)
              for u in (4, 5) for v in (4, 5)]
    return graph(n, edges), {6*j+k for j in range(a+b) for k in range(4)}


def disjoint(first, second):
    g, s = first
    h, t = second
    edges = [(u, v) for u in range(len(g)) for v in g[u] if u < v]
    edges += [(len(g)+u, len(g)+v) for u in range(len(h)) for v in h[u] if u < v]
    return graph(len(g)+len(h), edges), s | {len(g)+v for v in t}


def multiple_options():
    g, s = fixture([(0, 0), (0, 0), (1, 0), (1, 0)], dense=True)
    # Labels: centres0,1; helpers2,3; leaves4,6,8,10; direct witnesses12,13.
    # Two alternative direct witnesses each touch a helper. Extra leaf witnesses
    # give distinct valid choices but no private leaf, so both centres stay q.
    edges = [(u, v) for u in range(len(g)) for v in g[u] if u < v]
    for w, owner, helper in [(14, 0, 3), (15, 1, 2),
                              (16, 4, 2), (17, 8, 3)]:
        edges.extend(((w, owner), (w, helper)))
    edges.extend(((14, 5), (15, 9), (16, 17)))
    return graph(18, edges), s


def shared_two_centres():
    # Two equally coloured centres share the same two h2 helpers. A separate
    # opposite-colour star and real witness conflicts exercise both orientations.
    edges = [(0, 5), (0, 6), (1, 7), (1, 8), (2, 9), (2, 10)]
    for ell, helper in [(5, 3), (6, 4), (7, 3), (8, 4), (9, None), (10, None)]:
        w = ell+6
        edges.append((ell, w))
        if helper is not None:
            edges.append((helper, w))
    edges.extend(((0, 17), (1, 18), (11, 15), (12, 16), (13, 15), (14, 16)))
    return graph(19, edges), set(range(11))


def one_part_beta(g, col):
    parts = [[v for v in range(len(g)) if col[v] == j] for j in (0, 1)]
    left, right = sorted(parts, key=len)
    adj = [sum(1 << j for j, v in enumerate(left) if v in g[w]) for w in right]
    best = 0
    for mask in range(1 << len(left)):
        free, owners = 0, set()
        for neighbours in adj:
            hit = mask & neighbours
            if not hit:
                free += 1
            elif not hit & (hit-1):
                owners.add(hit)
        best = max(best, mask.bit_count()+free+len(owners))
    return best, 1 << len(left)


def targeted():
    models = [
        ('direct_parallel', fixture([(0, 0), (0, 0), (1, 0), (1, 0)], dense=True)),
        ('direct_large_helper', fixture([(0, 0)]*3+[(1, 0)]*3, dense=True)),
        ('mixed_clean_direct', fixture([(0, None), (0, 0), (1, 0), (1, 1)], dense=True)),
        ('surplus_and_extras', fixture([(0, None), (0, 0), (0, 0), (1, None), (1, 0)], True, True)),
        ('multiple_witness_choices', multiple_options()),
        ('two_centres_shared_helpers', shared_two_centres()),
        ('balanced_equality', gap_family(2, 2)),
        ('unbalanced_positive', gap_family(1, 2)),
    ]
    # True positive deficit alongside q>0, with exact beta by component addition.
    direct = fixture([(0, 0), (0, 1), (1, 0), (1, 1)], dense=True)
    models.append(('positive_and_direct', disjoint(gap_family(3, 3), direct)))
    rows = []
    for name, (g, s) in models:
        assert minimal(g, s), name
        col = colors(g)
        if name == 'positive_and_direct':
            # Exact isolated components and the already proved all-a,b formula.
            control, control_subsets = one_part_beta(direct[0], colors(direct[0]))
            beta, subsets = 21+control, control_subsets
            beta_method = 'accepted beta(G_(3,3))=21 plus independent exact direct component'
        else:
            beta, subsets = one_part_beta(g, col)
            assert beta == beta_literal(g)
            beta_method = 'independent one-part optimum and forbidden-triple recurrence'
        counts = Counter()
        params = audit(g, s, beta, col, counts)
        if name == 'positive_and_direct':
            assert len(s)-beta > 0 and all(row[2] > 0 for row in params)
        if name == 'balanced_equality':
            assert len(g) == 12*(len(s)-beta)
        rows.append({'name': name, 'order': len(g), 'selected_size': len(s), 'beta': beta,
                     'beta_method': beta_method, 'one_part_subsets': subsets,
                     'parameters_c_s_q_a_b2_b3_mu_d': [list(row) for row in params],
                     'checks': dict(sorted(counts.items()))})
    return rows


def arithmetic():
    # Separate exact integer arithmetic controls; no optimization library or floats.
    checks = 0
    for c, q, s, b2, b3, mu in product(range(5), repeat=6):
        if q > c:
            continue
        B0, C0, D0 = c+2*q-b2-2*b3, c-q+b2+b3-mu, q+s+2*mu-2*b2
        assert 7*B0+13*C0+3*D0 == 20*c+4*q+3*s-b3-7*mu
        assert 10*B0+20*C0+5*D0 == 30*c+5*q+5*s-10*mu
        for d in range(-3, 5):
            if B0 >= 2*d and C0 >= 2*d and D0 >= 0:
                n = max(0, 5*c+3*s+q+2*d)
                assert 4*n >= 48*d+9*s+b3+7*mu
                assert 6*n >= 72*d+q+13*s+10*mu
                checks += 1
    return {'parameter_tuples': 9375, 'feasible_ledger_checks': checks,
            'method': 'exact integer identities and minimum resource order'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='output/selected-star-general-budget-check.json')
    args = parser.parse_args()
    report = {'status': 'PASS', 'scope': 'finite controls; general proof is in the note',
              'exhaustive': exhaustive(), 'targeted': targeted(), 'arithmetic': arithmetic()}
    path = Path(args.output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': report['status'], 'totals': report['exhaustive']['totals'],
                      'targeted_models': len(report['targeted']), 'output': str(path)}, sort_keys=True))


if __name__ == '__main__':
    main()


