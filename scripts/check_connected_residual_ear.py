"""Standalone certificates for one ear with a connected residual graph."""
import json
from pathlib import Path


def construct(s):
    g = {}
    left = {'e', 'alpha'}
    selected = {'d', 'e'}
    witnesses = {'d': 'alpha', 'e': 'beta'}

    def edge(a, b):
        g.setdefault(a, set()).add(b)
        g.setdefault(b, set()).add(a)

    for j in range(1, s + 1):
        y = f'{j}:y'
        local_left = {y}
        local_right = set()
        edge('d' if j % 2 else 'e', y)
        if j > 1:
            edge(f'{j-1}:y', y)
        for c in range(2):
            groups = {a: [f'{j}:{c}:{a}{i}' for i in range(2)]
                      for a in 'AVWZ'}
            p, u = f'{j}:{c}:p', f'{j}:{c}:u'
            for a in groups['A']:
                for v in groups['V']:
                    edge(a, v)
            for w in groups['W']:
                for z in groups['Z']:
                    edge(w, z)
            for i in range(2):
                a, v, w, z = [groups[t][i] for t in 'AVWZ']
                for x, t in [(a, z), (v, w), (p, z), (u, w), (y, z)]:
                    edge(x, t)
                witnesses[a], witnesses[v] = z, w
            witnesses[p], witnesses[u] = p, u
            selected.update(groups['A'] + groups['V'] + [p, u])
            local_left.update(groups['A'] + groups['W'] + [p])
            local_right.update(groups['V'] + groups['Z'] + [u])
        left.update(local_left if j % 2 else local_right)
    for a, b in [('d', 'e'), ('d', 'alpha'), ('alpha', 'beta'), ('beta', 'e')]:
        edge(a, b)
    square = {'d', 'e', 'alpha', 'beta'}
    residual = {v: row - square for v, row in g.items() if v not in square}
    return g, residual, left, selected, witnesses


def unformed(g, selected):
    active = {v for v in selected if g[v] & selected}
    return {v for v in g if v not in selected and len(g[v] & selected) < 2
            and not g[v] & active}


def connected(g):
    first = next(iter(g))
    seen, queue = {first}, [first]
    for v in queue:
        for u in g[v] - seen:
            seen.add(u)
            queue.append(u)
    return len(seen) == len(g)


def main():
    report = dict(status='PASS', sizes=[1, 2, 3, 4, 8, 16, 64], models=0,
                  single_deletions=0, specified_witnesses=0,
                  path_subsets=0, path_dominating_sets=0,
                  exact_residual_SF_computed=False,
                  upper_bound_source='written local-cap and domination proofs',
                  new_Lean=False)
    for s in report['sizes']:
        g, r, left, selected, witnesses = construct(s)
        assert len(r) == 21*s and len(g) == 21*s + 4
        assert max(map(len, r.values())) <= 6
        assert len(g['d']) == (s+1)//2 + 2
        assert len(g['e']) == s//2 + 2
        assert connected(g) and connected(r)
        assert all((a in left) != (b in left) for a, row in g.items() for b in row)
        base = {v: row - {'alpha', 'beta'} for v, row in g.items()
                if v not in {'alpha', 'beta'}}
        assert connected(base)
        assert set(base) - {'d', 'e'} == set(r)
        assert all(base[v] - {'d', 'e'} == r[v] for v in r)
        assert len(selected) == 12*s + 2 and set(witnesses) == selected
        assert not unformed(g, selected)
        for v in selected:
            failed = unformed(g, selected - {v})
            assert failed and witnesses[v] in failed
            report['single_deletions'] += 1
            report['specified_witnesses'] += 1
        report['models'] += 1

    for s in range(1, 15):
        all_bits = (1 << s) - 1
        best = s
        for mask in range(1 << s):
            report['path_subsets'] += 1
            covered = (mask | (mask << 1) | (mask >> 1)) & all_bits
            assert covered.bit_count() <= 3 * mask.bit_count()
            if covered == all_bits:
                report['path_dominating_sets'] += 1
                assert 3 * mask.bit_count() >= s
                best = min(best, mask.bit_count())
        assert best == (s + 2)//3

    out = Path(__file__).resolve().parents[1] / 'output'
    out.mkdir(exist_ok=True)
    (out / 'connected-residual-ear-check.json').write_text(
        json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
