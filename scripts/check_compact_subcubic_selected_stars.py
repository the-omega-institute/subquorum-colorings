#!/usr/bin/env python3
"""Independent physical subsets, exact optimization, stars and vertex cuts."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from compact_subcubic_selected_stars import core, base, family, spanning_ears

if not __debug__:
    raise RuntimeError('Assertions must be enabled')


def diss(g, selected):
    return all(len(g[v] & selected) <= 1 for v in selected)


def literal(g, selected, outside):
    # Enumerate actual three-vertex stars, allowing a non-induced copy.
    for centre in {outside} | g[outside]:
        for a, b in combinations(g[centre], 2):
            if outside in (a, b, centre) and len({a, b, centre} & selected) == 2:
                return True
    return False


def connected(g, removed):
    rest = set(range(len(g))) - set(removed)
    if not rest:
        return True
    seen = {min(rest)}
    todo = list(seen)
    while todo:
        for v in (g[todo.pop()] & rest)-seen:
            seen.add(v)
            todo.append(v)
    return seen == rest


def exact(g):
    """Branch on v excluded, isolated, or paired with each neighbour."""
    adjacency = [sum(1 << u for u in row) for row in g]

    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        vertices = [v for v in range(len(g)) if mask >> v & 1]
        v = max(vertices, key=lambda v: (adjacency[v] & mask).bit_count())
        neighbours = adjacency[v] & mask
        if not neighbours:
            return mask.bit_count()
        component = frontier = 1 << v
        while frontier:
            bit = frontier & -frontier
            frontier -= bit
            more = adjacency[bit.bit_length()-1] & mask & ~component
            component |= more
            frontier |= more
        if component != mask:
            return solve(component)+solve(mask ^ component)
        closed = neighbours | (1 << v)
        best = max(solve(mask & ~(1 << v)), 1+solve(mask & ~closed))
        while neighbours:
            bit = neighbours & -neighbours
            neighbours -= bit
            best = max(best, 2+solve(mask & ~(closed | adjacency[bit.bit_length()-1])))
        return best

    answer = solve((1 << len(g))-1)
    return {'beta': answer, 'states': solve.cache_info().currsize}


def validate_ears(g, paths):
    used = set()
    for j, path in enumerate(paths):
        assert all(b in g[a] for a, b in zip(path, path[1:]))
        if j == 0:
            assert path[0] == path[-1] and len(set(path[:-1])) == len(path)-1
        else:
            assert path[0] != path[-1] and path[0] in used and path[-1] in used
            assert len(set(path)) == len(path) and not (set(path[1:-1]) & used)
        used.update(path)
    assert used == set(range(len(g)))


def physical(length, k):
    g, s, d, c = family(k, length)
    assert len(g) == 16*length*k and len(s) == 10*length*k
    assert len(d) == (10*length-1)*k and diss(g, d)
    assert all(v != u and v in g[u] and c[v] != c[u]
               for v in range(len(g)) for u in g[v])
    assert min(map(len, g)) == 2 and max(map(len, g)) == 3
    assert all(literal(g, s, v) for v in range(len(g)) if v not in s)
    witnesses = {}
    for v in sorted(s):
        remaining = s-{v}
        near = {v} | g[v] | set().union(*(g[u] for u in g[v]))
        witnesses[v] = next(u for u in sorted(near-remaining) if not literal(g, remaining, u))
    unseen = set(s)
    components = Counter()
    while unseen:
        q = {min(unseen)}
        todo = list(q)
        while todo:
            for v in (g[todo.pop()] & s)-q:
                q.add(v)
                todo.append(v)
        unseen -= q
        components[len(q)] += 1
        if len(q) == 3:
            assert sorted(len(g[v] & q) for v in q) == [1, 1, 2]
    assert dict(components) == {3: 2*length*k, 1: 4*length*k}
    assert connected(g, ()) and all(connected(g, {v}) for v in range(len(g)))
    return {'L': length, 'k': k, 'n': len(g), 'selected': len(s), 'beta_attaining': len(d),
            'degree_counts': dict(sorted(Counter(map(len, g)).items())),
            'selected_components': dict(sorted(components.items())),
            'deletion_witnesses': witnesses, 'single_cuts_checked': len(g)}


def local_controls():
    p = [{u for u in (v-1, v+1) if 0 <= u < 6} for v in range(6)]
    maxima = []
    for mask in range(64):
        q = {v for v in range(6) if mask >> v & 1}
        if diss(p, q):
            assert len(q) <= 4
            if len(q) == 4:
                maxima.append(q)
    assert len(maxima) == 6
    rows = []
    for q in maxima:
        r = {0, 2, 3, 5} if 0 in q else {1, 2, 4, 5}
        assert diss(p, r) and (r & {0, 4}) <= q
        assert all(len(p[v] & r) <= len(p[v] & q) for v in r & {0, 4})
        rows.append({'from': sorted(q), 'to': sorted(r)})
    # All labelled graphs on up to five vertices compare exact recursion to subsets.
    small = 0
    for n in range(1, 6):
        possible = list(combinations(range(n), 2))
        for mask in range(1 << len(possible)):
            g = [set() for _ in range(n)]
            for t, (a, b) in enumerate(possible):
                if mask >> t & 1:
                    g[a].add(b)
                    g[b].add(a)
            brute = max(len(q) for bits in range(1 << n)
                        if diss(g, q := {v for v in range(n) if bits >> v & 1}))
            assert exact(g)['beta'] == brute
            small += 1
    return {'P6_all_subsets': 64, 'normalizations': rows, 'exact_solver_all_small_graphs': small}


def failed_paddings():
    def pairs(q):
        a, b, c, d = q
        return [((a, b), (c, d)), ((a, c), (b, d)), ((a, d), (b, c))]

    g, s, d, c = core()
    classes = [[j for j in range(8) if c[6*j+5] == t] for t in (0, 1)]
    rows = []
    for left, right, swap in product(pairs(classes[0]), pairs(classes[1]), range(2)):
        g, s, d, c = core()
        for pair in left+right:
            w = len(g)
            g.append(set())
            for j in pair:
                g[w].add(6*j+5)
                g[6*j+5].add(w)
        for j in range(2):
            a, b = 48+j, 50+(j ^ swap)
            g[a].add(b)
            g[b].add(a)
        result = exact(g)
        assert result['beta'] >= 32
        rows.append({'pairs': left+right, 'swap': swap, **result})
    assert len(rows) == 18
    return rows


def main():
    report = {'local': local_controls(), 'cores': [], 'ears': [], 'models': []}
    for length in (4, 6, 8):
        for port in (False, True):
            g, s, d, c = core(length, port)
            answer = exact(g)
            assert answer['beta'] == 8*length-1
            assert diss(g, d)
            report['cores'].append({'L': length, 'port': port, **answer})
        if length <= 6:
            count = 0
            g = core(length, False)[0]
            for bits in product(range(2), repeat=2*length):
                q = {6*j+t for j, bit in enumerate(bits)
                     for t in ((0, 2, 3, 5) if not bit else (1, 2, 4, 5))}
                assert not diss(g, q)
                count += 1
            report.setdefault('normalized_states', []).append({'L': length, 'all_states': count})
    for length in (4, 6, 8, 12, 20):
        g, s, d, c = base(length)
        paths = spanning_ears(length)
        validate_ears(g, paths)
        report['ears'].append({'L': length, 'paths': paths})
        u, v = 6, 6*(length+1)
        assert u in d and v not in d and u not in s and v not in s
        g[u].remove(v)
        g[v].remove(u)
        assert diss(g, d)
        assert all((g[a] & s) == (base(length)[0][a] & s) for a in range(len(g)))
        for k in (1, 2, 3, 5):
            report['models'].append(physical(length, k))
    full = exact(base(4)[0])
    assert full['beta'] == 39
    report['independent_full64_exact'] = full
    report['failed52_paddings'] = failed_paddings()
    report['scope'] = ('General even-L and all-k proofs in the note. Independent exact optimization of six cores '
                       'and full H64; 20 physical models with all literal deletion/cut checks. '
                       'No exact unrestricted SF2, Lean or optimal-density assertion.')
    output = ROOT/'output/compact-subcubic-selected-star-check.json'
    output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'result': 'PASS', 'full64_exact': full, 'models': len(report['models']),
                      'literal_deletions': sum(r['selected'] for r in report['models']),
                      'vertex_cuts': sum(r['single_cuts_checked'] for r in report['models']),
                      'report_bytes': output.stat().st_size}))


if __name__ == '__main__':
    main()
