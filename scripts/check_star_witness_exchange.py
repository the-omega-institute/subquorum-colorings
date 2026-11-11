#!/usr/bin/env python3
"""Finite audit of the independent-leaf-witness exchange (standard library).

Run from any directory; --output overrides the default sibling output report.
Exhaustion is of labelled bipartite graphs with specified part sizes, including
isolated vertices. Literal K1,2 enumeration independently checks formation and
all single deletions; monotonicity makes those deletions certify minimality.
This is a finite verifier, not a proof of the unrestricted grid conjecture.
"""
import argparse
import itertools as it
import json
from collections import Counter
from pathlib import Path


def graph(n, edges):
    adj = [set() for _ in range(n)]
    for u, v in edges:
        assert 0 <= u < n and 0 <= v < n and u != v
        adj[u].add(v)
        adj[v].add(u)
    return adj


def literal_formed(g, s, x):
    """Search all stars containing x; extra edges are allowed."""
    allowed = s | {x}
    for c in allowed:
        for a, b in it.combinations(sorted(g[c] & allowed), 2):
            if x in (c, a, b):
                return True
    return False


def forming(g, s):
    return all(literal_formed(g, s, x) for x in range(len(g)) if x not in s)


def minimal(g, s):
    return forming(g, s) and all(not forming(g, s - {v}) for v in s)


def dissociation(g, d):
    return all(len(g[v] & d) <= 1 for v in d)


def components(vertices, neighbors):
    unseen = set(vertices)
    while unseen:
        todo = [min(unseen)]
        comp = set()
        while todo:
            v = todo.pop()
            if v in comp:
                continue
            comp.add(v)
            todo.extend(set(neighbors(v)) - comp)
        unseen -= comp
        yield comp


def stars(g, s):
    leaves = {}
    unaffected = set()
    for k in components(s, lambda v: g[v] & s):
        if len(k) <= 2:
            unaffected |= k
            continue
        centres = [v for v in k if len(g[v] & k) == len(k) - 1]
        if len(centres) != 1:
            return None
        c = centres[0]
        if any(g[v] & k != {c} for v in k - {c}):
            return None
        for leaf in sorted(k - {c}):
            leaves[leaf] = c
    return leaves, unaffected


def witness_options(g, s, leaves):
    # Derive choices from literal deletion failures, not the classification.
    return [tuple(x for x in range(len(g)) if x not in s and
                  not literal_formed(g, s - {leaf}, x)) for leaf in leaves]


def auxiliary(g, s, leaves, choice):
    isolates = {v for v in s if not g[v] & s}
    edges = []
    for leaf, w in zip(leaves, choice):
        assert w in g[leaf]
        ns = g[w] & s
        assert leaf in ns and len(ns) in (1, 2)
        other = ns - {leaf}
        assert other <= isolates
        endpoint = next(iter(other)) if other else len(g) + leaf
        edges.append((leaves[leaf], endpoint, leaf, w))
    assert len(set(choice)) == len(choice)
    vertices = {v for e in edges for v in e[:2]}
    incidence = {v: [] for v in vertices}
    for i, e in enumerate(edges):
        for v in e[:2]:
            incidence[v].append(i)
    parts = []
    for vs in components(vertices, lambda v: [edges[i][0] if edges[i][1] == v
                                             else edges[i][1] for i in incidence[v]]):
        es = sorted({i for v in vs for i in incidence[v]})
        parts.append((vs, es))
    return edges, incidence, parts


def exact_cover(g, witnesses):
    vertices = sorted(witnesses)
    conflicts = [(u, v) for u in vertices for v in g[u] & witnesses if u < v]
    for size in range(len(vertices) + 1):
        for candidate in it.combinations(vertices, size):
            cover = set(candidate)
            if all(u in cover or v in cover for u, v in conflicts):
                return cover
    raise AssertionError('unreachable')


def audit(g, s, leaves, unaffected, choice, counts):
    edges, incidence, parts = auxiliary(g, s, leaves, choice)
    independent = all(not g[w] & set(choice) for w in choice)
    roots = [sorted(vs) if len(es) == len(vs) - 1 else [None]
             for vs, es in parts]
    for selected_roots in it.product(*roots):
        d = set(unaffected) - {v for e in edges for v in e[:2]}
        q = 0
        for (vs, es), root in zip(parts, selected_roots):
            actual = {v for v in vs if v < len(g)}
            if root is None:
                assert len(es) >= len(vs)
                q += len(es) - len(actual)
                d.update(v for i in es for v in edges[i][2:])
                counts['cycle_component_runs'] += 1
            else:
                counts['dummy_root_runs' if root >= len(g) else 'actual_root_runs'] += 1
                d |= actual
                seen = {root}
                todo = [root]
                while todo:
                    parent = todo.pop()
                    for i in incidence[parent]:
                        c, z, leaf, w = edges[i]
                        child = z if parent == c else c
                        if child in seen:
                            continue
                        seen.add(child)
                        todo.append(child)
                        d.add(leaf if child == c else w)
                assert seen == vs
        assert len(d) == len(s) + q
        assert d <= s | set(choice)
        retained = d & set(choice)
        # Removing all witness-witness edges must leave maximum degree <= 1.
        assert all(len((g[v] & d) - (retained if v in retained else set())) <= 1
                   for v in d)
        cover = exact_cover(g, retained)
        assert dissociation(g, d - cover)
        assert len(d - cover) == len(s) + q - len(cover)
        counts['exchange_runs'] += 1
        counts['positive_surplus_runs'] += q > 0
        counts['positive_cover_runs'] += bool(cover)
        if independent:
            assert not cover and dissociation(g, d) and len(d) >= len(s)
            counts['independent_runs'] += 1
        else:
            counts['nonindependent_runs'] += 1


def exhaust(counts):
    ranges = [(a, b) for a in range(4) for b in range(a, 7 - a)]
    ranges.append((3, 4))
    rows = []
    for a, b in ranges:
        local = Counter()
        possible = list(it.product(range(a), range(a, a + b)))
        for mask in range(1 << len(possible)):
            g = graph(a + b, [e for i, e in enumerate(possible) if mask >> i & 1])
            local['graphs'] += 1
            for sm in range(1 << (a + b)):
                s = {v for v in range(a + b) if sm >> v & 1}
                local['selections'] += 1
                if not minimal(g, s):
                    continue
                local['minimal_selections'] += 1
                structure = stars(g, s)
                if structure is None:
                    continue
                local['eligible_selections'] += 1
                leaves, unaffected = structure
                local['with_star_selections'] += bool(leaves)
                options = witness_options(g, s, leaves)
                assert all(options)
                for choice in it.product(*options):
                    local['witness_assignments'] += 1
                    audit(g, s, leaves, unaffected, choice, counts)
        rows.append({'parts': [a, b], **dict(sorted(local.items()))})
    return rows


def fixture(name, links, counts, conflicts=(), extras=False):
    # links: (centre label, isolate label or None); every centre has >=2 leaves.
    labels = sorted({c for c, _ in links} | {z for _, z in links if z is not None})
    ids = {label: i for i, label in enumerate(labels)}
    s = set(ids.values())
    edges = []
    leaves = {}
    choice = []
    n = len(ids)
    for c, z in links:
        leaf, w = n, n + 1
        n += 2
        s.add(leaf)
        leaves[leaf] = ids[c]
        choice.append(w)
        edges += [(ids[c], leaf), (leaf, w)]
        if z is not None:
            edges.append((w, ids[z]))
    for c in sorted({c for c, _ in links}):
        edges.append((ids[c], n))  # omitted t_c makes deletion of c fail
        n += 1
    for i, j in conflicts:
        edges.append((choice[i], choice[j]))
    if extras:
        s.update((n, n + 1, n + 2))
        edges.append((n, n + 1))
        n += 3
    g = graph(n, edges)
    # Independent bipartiteness check, including added witness conflicts.
    color = {}
    for v in range(n):
        if v in color:
            continue
        color[v] = 0
        todo = [v]
        while todo:
            u = todo.pop()
            for w in g[u]:
                if w not in color:
                    color[w] = 1 - color[u]
                    todo.append(w)
                assert color[w] != color[u]
    assert minimal(g, s)
    structure = stars(g, s)
    assert structure is not None and structure[0] == leaves
    before = counts.copy()
    audit(g, s, *structure, choice, counts)
    return {'name': name, 'vertices': n, 'selected': len(s),
            'auxiliary_edges': len(links), 'witness_conflicts': len(conflicts),
            'checks': dict(sorted((counts - before).items()))}


def grid_example(counts):
    index = lambda r, c: (r - 1) * 6 + c - 1
    edges = [(index(r, c), index(rr, cc)) for r in range(1, 7)
             for c in range(1, 7) for rr, cc in ((r + 1, c), (r, c + 1))
             if rr <= 6 and cc <= 6]
    g = graph(36, edges)
    rows = [(1, 4, 6), (1, 3, 5), (1, 3, 4, 6), (2, 6), (3, 5), (1, 2, 4, 6)]
    s = {index(r, c) for r, cs in enumerate(rows, 1) for c in cs}
    assert len(s) == 18 and minimal(g, s)
    leaves, unaffected = stars(g, s)
    options = witness_options(g, s, leaves)
    by_leaf = dict(zip(leaves, options))
    assert by_leaf[index(1, 1)] == (index(1, 2),)
    assert by_leaf[index(2, 3)] == (index(1, 3),)
    assert index(1, 3) in g[index(1, 2)]
    assignments = list(it.product(*options))
    assert assignments and all(any(g[w] & set(ws) for w in ws) for ws in assignments)
    for ws in assignments:
        audit(g, s, leaves, unaffected, ws, counts)
    d = (s - {index(2, 1), index(3, 3)}) | {index(1, 2), index(4, 4)}
    assert len(d) == len(s) == 18 and dissociation(g, d)
    return {'vertices': 36, 'selected': len(s), 'explicit_dissociation_size': len(d),
            'star_leaves': len(leaves), 'witness_assignments': len(assignments),
            'independent_assignments': 0,
            'forced_adjacent_witnesses': [[1, 2], [1, 3]]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parents[1]
                        / 'output/star-witness-exchange-check.json')
    args = parser.parse_args()
    counts = Counter()
    rows = exhaust(counts)
    fixtures = [
        fixture('private_dummy_tree', [('c', None)] * 2, counts, extras=True),
        fixture('shared_isolate_tree', [('c1', 'z'), ('c1', None),
                                       ('c2', 'z'), ('c2', None)], counts),
        fixture('parallel_cycle', [('c', 'z')] * 2, counts),
        fixture('ordinary_four_cycle', [('a', 'x'), ('a', 'y'),
                                         ('b', 'x'), ('b', 'y')], counts),
        fixture('positive_cycle_surplus', [('c', 'z')] * 3, counts),
        fixture('conflicting_private_trees', [('a', None)] * 2 + [('b', None)] * 2,
                counts, conflicts=[(0, 2)]),
    ]
    grid = grid_example(counts)
    for key in ('independent_runs', 'nonindependent_runs', 'dummy_root_runs',
                'actual_root_runs', 'cycle_component_runs', 'positive_surplus_runs',
                'positive_cover_runs'):
        assert counts[key] > 0, key
    assert sum(r.get('with_star_selections', 0) for r in rows) > 0
    report = {'status': 'pass', 'scope': 'Finite labelled bipartite graph audit; not a general proof',
              'exhaustive_ranges': rows, 'fixtures': fixtures, 'grid_6x6': grid,
              'checks': dict(sorted(counts.items())),
              'mathematical_issues': [
                  'Private dummy endpoints are auxiliary only; actual private paths have length two.',
                  'Extra omitted centre witnesses t_c certify fixture minimality; bare length-three subdivisions need not.',
                  'Witness independence is a hypothesis, refuted as automatic by the 6x6 example.'],
              'extension': 'Exact brute-force minimum vertex cover of retained witness conflicts; size S+q-tau verified.'}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'pass', 'graphs': sum(r['graphs'] for r in rows),
                      'selections': sum(r['selections'] for r in rows),
                      'checks': dict(sorted(counts.items()))}, sort_keys=True))


if __name__ == '__main__':
    main()
