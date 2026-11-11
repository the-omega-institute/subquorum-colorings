"""Standalone literal controls for the decorated-interface theorem."""
import itertools
import json
from pathlib import Path
import random


def failed(g, selected):
    active = {v for v in selected if g[v] & selected}
    return {v for v in g if v not in selected and len(g[v] & selected) < 2
            and not g[v] & active}


def small_graph(n, mask):
    g = {v: set() for v in range(n)}
    for bit, (a, b) in enumerate(itertools.combinations(range(n), 2)):
        if mask >> bit & 1:
            g[a].add(b)
            g[b].add(a)
    return g


def minimum_sets(g, all_minimal=False):
    n = len(g)
    forms = [False] * (1 << n)
    minimal = []
    for mask in range(1 << n):
        s = {v for v in g if mask >> v & 1}
        forms[mask] = not failed(g, s)
        if forms[mask] and all(not forms[mask ^ (1 << v)] for v in s):
            minimal.append(s)
    best = min(map(len, minimal))
    return best, minimal if all_minimal else [min(
        (s for s in minimal if len(s) == best), key=lambda s: tuple(sorted(s)))]


def decorate(h):
    g = {v: set() for v in range(21 * len(h))}

    def edge(a, b):
        g[a].add(b)
        g[b].add(a)

    for j in h:
        y = 21*j + 20
        for c in range(2):
            o = 21*j + 10*c
            for i in range(2):
                for k in range(2):
                    edge(o+i, o+2+k)
                    edge(o+4+i, o+6+k)
                for a, b in [(o+i, o+6+i), (o+2+i, o+4+i),
                             (o+8, o+6+i), (o+9, o+4+i), (y, o+6+i)]:
                    edge(a, b)
        for k in h[j]:
            if j < k:
                edge(y, 21*k+20)
    return g


def attain(h, q):
    s, witnesses = set(), {}
    for j in h:
        for c in range(2):
            o = 21*j + 10*c
            if j in q:
                points = [o, o+1, o+4, o+5, o+8]
                s.update(points)
                witnesses.update({v: v for v in points})
            else:
                s.update([o, o+1, o+2, o+3, o+8, o+9])
                for i in range(2):
                    witnesses[o+i] = o+6+i
                    witnesses[o+2+i] = o+4+i
                witnesses[o+8], witnesses[o+9] = o+8, o+9
        if j in q:
            s.add(21*j+20)
            missing = failed(h, q-{j})
            assert missing
            witnesses[21*j+20] = 21*min(missing)+20
    return s, witnesses


def upper_map(h, g, s):
    c = {j: 12-len(s & set(range(21*j, 21*j+21))) for j in h}
    assert all(x >= 0 for x in c.values())
    p = {j for j in h if c[j] > 0}
    for j in h:
        y = 21*j+20
        zs = {21*j+6, 21*j+7, 21*j+16, 21*j+17}
        if y in s:
            assert c[j] >= 1
            if zs & s:
                assert c[j] >= 2
        if c[j] == 0:
            assert y not in s and not zs & s
    q, paid = set(p), set()
    for j in sorted(p):
        y = 21*j+20
        zs = {21*j+6, 21*j+7, 21*j+16, 21*j+17}
        if y in s and zs & s and not h[j] & p and h[j]:
            q.add(min(h[j]))
            paid.add(j)
    assert len(q) <= len(p)+len(paid) <= sum(c.values())
    assert not failed(h, q)
    assert len(s) <= 12*len(h)-len(q)
    return sum(c.values())


def block_cap(report):
    g = {v: set() for v in range(12)}
    def edge(a, b):
        g[a].add(b)
        g[b].add(a)
    for i in range(2):
        for k in range(2):
            edge(i, 2+k)
            edge(4+i, 6+k)
        for a, b in [(i, 6+i), (2+i, 4+i), (8, 6+i), (9, 4+i), (10, 6+i)]:
            edge(a, b)
    edge(10, 11)  # outside leaf tests preservation of selected y's activity
    for mask in range(1 << 10):
        report['block_patterns'] += 1
        s = {v for v in range(10) if mask >> v & 1} | {10}
        if len(s) < 6 or not s & {6, 7} or failed(g, s):
            continue
        report['forming_cap_candidates'] += 1
        safe = [v for v in s-{10}
                if (s-{v}) & {6, 7} and not failed(g, s-{v})]
        assert safe
        report['safe_cap_deletions_found'] += len(safe)


def main():
    report = dict(status='PASS', block_patterns=0, forming_cap_candidates=0,
                  safe_cap_deletions_found=0, exhaustive_interfaces=0,
                  lifted_minimal_sets=0, specified_deletions=0, upper_maps=0,
                  seeded_minimal_decorations=0, path_strings=0,
                  path_orders=list(range(15)), large_path_sizes=[17, 32, 65],
                  decorated_SF_exhaustively_computed=False, new_Lean=False)
    block_cap(report)
    for n in range(6):
        for mask in range(1 << (n*(n-1)//2)):
            h = small_graph(n, mask)
            best, selections = minimum_sets(h, all_minimal=n <= 4)
            g = decorate(h)
            for q in selections:
                s, witnesses = attain(h, q)
                assert len(s) == 12*n-len(q) and set(witnesses) == s
                assert not failed(g, s)
                for v in s:
                    assert witnesses[v] in failed(g, s-{v})
                    report['specified_deletions'] += 1
                upper_map(h, g, s)
                if len(q) == best:
                    assert len(s) == 12*n-best
                report['lifted_minimal_sets'] += 1
                report['upper_maps'] += 1
            report['exhaustive_interfaces'] += 1

    rng = random.Random(20261112)
    for n in range(2, 13):
        for trial in range(4):
            h = {v: set() for v in range(n)}
            for a, b in itertools.combinations(range(n), 2):
                if rng.randrange(100) < 20+20*trial:
                    h[a].add(b)
                    h[b].add(a)
            best, _ = minimum_sets(h)
            g = decorate(h)
            order = list(g)
            rng.shuffle(order)
            s = set(g)
            for v in order:
                if not failed(g, s-{v}):
                    s.remove(v)
            assert not failed(g, s)
            assert all(failed(g, s-{v}) for v in s)
            loss = upper_map(h, g, s)
            assert loss >= best and len(s) <= 12*n-best
            report['seeded_minimal_decorations'] += 1
            report['upper_maps'] += 1

    for n in report['path_orders']:
        h = {v: {u for u in [v-1, v+1] if 0 <= u < n} for v in range(n)}
        best, _ = minimum_sets(h)
        report['path_strings'] += 1 << n
        assert best == 2*(n//4)+min(n % 4, 2)

    for n in report['large_path_sizes']:
        h = {v: {u for u in [v-1, v+1] if 0 <= u < n} for v in range(n)}
        bits = [0, 1, 1, 0]*(n//4) + {0: [], 1: [1], 2: [1, 1], 3: [1, 1, 0]}[n % 4]
        q = {v for v in h if bits[v]}
        assert not failed(h, q)
        assert all(failed(h, q-{v}) for v in q)
        s, witnesses = attain(h, q)
        g = decorate(h)
        assert not failed(g, s)
        for v in s:
            assert witnesses[v] in failed(g, s-{v})
            report['specified_deletions'] += 1
        assert upper_map(h, g, s) == len(q)
        report['lifted_minimal_sets'] += 1
        report['upper_maps'] += 1
    out = Path(__file__).resolve().parents[1] / 'output'
    out.mkdir(exist_ok=True)
    (out / 'decorated-interface-check.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
