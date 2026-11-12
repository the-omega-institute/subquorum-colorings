#!/usr/bin/env python3
"""Literal star, exact core, port-state and spanning-ear controls; standard library only."""
from collections import Counter, deque
from functools import lru_cache
from itertools import combinations, product
from pathlib import Path
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'develop'))
from subcubic_selected_stars import base, family

if not __debug__:
    raise RuntimeError('Assertions must be enabled')


def diss(g, q):
    return all(len(g[a] & q) <= 1 for a in q)


def literal(g, s, x):
    for c in {x} | g[x]:
        if c != x and c not in s:
            continue
        for a, b in combinations(g[c] & (s | {x}), 2):
            if x in (a, b, c) and len({a, b, c} & s) == 2:
                return True
    return False


def connected(g, removed=()):
    rest = set(range(len(g))) - set(removed)
    seen = {min(rest)}
    todo = list(seen)
    while todo:
        for b in (g[todo.pop()] & rest) - seen:
            seen.add(b)
            todo.append(b)
    return seen == rest


def exact_beta(g):
    adj = [sum(1 << b for b in row) for row in g]

    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        vertices = [a for a in range(len(g)) if mask >> a & 1]
        v = max(vertices, key=lambda a: (adj[a] & mask).bit_count())
        neighbours = adj[v] & mask
        if not neighbours:
            return mask.bit_count()
        # Isolate a component before branching.
        comp = 1 << v
        frontier = comp
        while frontier:
            bit = frontier & -frontier
            frontier -= bit
            more = adj[bit.bit_length()-1] & mask & ~comp
            comp |= more
            frontier |= more
        if comp != mask:
            return solve(comp) + solve(mask ^ comp)
        closed = neighbours | (1 << v)
        best = max(solve(mask & ~(1 << v)), 1+solve(mask & ~closed))
        while neighbours:
            bit = neighbours & -neighbours
            neighbours -= bit
            u = bit.bit_length()-1
            best = max(best, 2+solve(mask & ~(closed | adj[u])))
        return best

    answer = solve((1 << len(g))-1)
    return {'beta': answer, 'recursion_states': solve.cache_info().currsize}


def ears(g):
    # Find an initial cycle, then add open ears with new internal vertices.
    a = 0
    b = min(g[a])
    pred = {a: None}
    todo = deque([a])
    while b not in pred:
        v = todo.popleft()
        for w in sorted(g[v]):
            if {v, w} == {a, b} or w in pred:
                continue
            pred[w] = v
            todo.append(w)
    path = [b]
    while path[-1] != a:
        path.append(pred[path[-1]])
    result = [list(reversed(path)) + [a]]
    used = set(result[0])
    while len(used) < len(g):
        candidates = []
        for a in sorted(used):
            pred = {a: None}
            todo = deque([a])
            end = None
            while todo and end is None:
                v = todo.popleft()
                for w in sorted(g[v]):
                    if w in pred:
                        continue
                    if w in used:
                        if v != a and w != a:
                            pred[w] = v
                            end = w
                            break
                        continue
                    pred[w] = v
                    todo.append(w)
            if end is not None:
                path = [end]
                while path[-1] != a:
                    path.append(pred[path[-1]])
                candidates.append(list(reversed(path)))
        assert candidates
        p = min(candidates, key=lambda x: (len(x), x))
        result.append(p)
        used.update(p)
    return result


def validate_ears(g, es):
    used = set()
    for j, p in enumerate(es):
        assert all(b in g[a] for a, b in zip(p, p[1:]))
        assert len(set(p[1:-1])) == len(p)-2
        if j == 0:
            assert p[0] == p[-1] and len(set(p[:-1])) == len(p)-1
        else:
            assert p[0] != p[-1] and p[0] in used and p[-1] in used
            assert not (set(p[1:-1]) & used)
        used.update(p)
    assert used == set(range(len(g)))


def local_controls(g):
    path = [{b for b in (a-1, a+1) if 0 <= b < 6} for a in range(6)]
    maxima = []
    all_diss = []
    for mask in range(64):
        q = {a for a in range(6) if mask >> a & 1}
        if diss(path, q):
            all_diss.append(q)
            if len(q) == 4:
                maxima.append(q)
    assert max(map(len, all_diss)) == 4 and len(maxima) == 6
    normalizations = []
    for q in maxima:
        r = {0, 2, 3, 5} if 0 in q else {1, 2, 4, 5}
        assert diss(path, r) and len(r) == len(q)
        assert (r & {0, 4}) <= (q & {0, 4})
        for v in r & {0, 4}:
            assert len(path[v] & r) <= len(path[v] & q)
        normalizations.append({'from': sorted(q), 'to': sorted(r)})
    core = [{b for b in row if b < 60} for row in g[:60]]
    half = [{b for b in row if b < 30} for row in core[:30]]
    half_states = []
    for bits in product(range(2), repeat=5):
        q = {6*j+a for j in range(5)
             for a in ((0, 2, 3, 5) if bits[j] == 0 else (1, 2, 4, 5))}
        if diss(half, q):
            assert bits[0] == 1
            half_states.append(bits)
    for bits in product(range(2), repeat=10):
        q = {6*j+a for j in range(10)
             for a in ((0, 2, 3, 5) if bits[j] == 0 else (1, 2, 4, 5))}
        assert not diss(core, q)
    exact = exact_beta(core)
    assert exact['beta'] == 39
    return {'P6_subsets': 64, 'P6_maxima': normalizations,
            'five_block_states': 32, 'feasible_five_block_states': half_states,
            'ten_block_normalized_states': 1024, 'core_independent_exact': exact}


def physical(g, s, d, colours, all_cuts=True):
    assert len(g) % 90 == 0
    k = len(g)//90
    assert len(s) == 56*k and len(d) == 55*k and diss(g, d)
    assert min(map(len, g)) == 2 and max(map(len, g)) == 3
    assert all(a != b and a in g[b] and colours[a] != colours[b]
               for a in range(len(g)) for b in g[a])
    assert all(literal(g, s, x) for x in range(len(g)) if x not in s)
    failures = {}
    for v in sorted(s):
        s1 = s - {v}
        near = {v} | g[v] | set().union(*(g[a] for a in g[v]))
        failures[v] = next(x for x in sorted(near-s1) if not literal(g, s1, x))
    shapes = Counter()
    unseen = set(s)
    while unseen:
        root = min(unseen)
        component = {root}
        todo = [root]
        while todo:
            for b in (g[todo.pop()] & s) - component:
                component.add(b)
                todo.append(b)
        unseen -= component
        shapes[len(component)] += 1
        if len(component) == 3:
            assert sorted(len(g[a] & s) for a in component) == [1, 1, 2]
    assert dict(shapes) == {3: 12*k, 1: 20*k}
    assert connected(g)
    cuts = list(range(len(g))) if all_cuts else []
    assert all(connected(g, {v}) for v in cuts)
    return {'k': k, 'n': len(g), 'selected': len(s), 'attaining': len(d),
            'edges': sum(map(len, g))//2, 'degree_counts': dict(sorted(Counter(map(len, g)).items())),
            'selected_components': dict(sorted(shapes.items())),
            'literal_deletion_witnesses': failures, 'single_vertex_cuts_checked': len(cuts)}


def main():
    g, s, d, colours = base()
    report = {'local': local_controls(g), 'models': []}
    es = json.loads((ROOT/'develop/fixtures/subcubic-selected-ears.json').read_text())
    validate_ears(g, es)
    report['spanning_open_ears'] = es
    # Independent physical subsets of each attachment, not just the partition cap.
    attachment_checks = []
    for vertices, expected in [(list(range(60+4*t, 64+4*t)), 2) for t in range(4)] + [
            (list(range(76, 83)), 4), (list(range(83, 90)), 4)]:
        best = max(len(q) for mask in range(1 << len(vertices))
                   if diss(g, q := {a for j, a in enumerate(vertices) if mask >> j & 1}))
        assert best == expected
        attachment_checks.append({'vertices': vertices, 'all_subsets': 1 << len(vertices), 'beta': best})
    report['attachment_all_subsets'] = attachment_checks
    for k in (1, 2, 3, 5, 8, 13):
        report['models'].append(physical(*family(k)))
    portless = [set(row) for row in g]
    portless[76].remove(83)
    portless[83].remove(76)
    assert all((portless[a] & s) == (g[a] & s) for a in range(90))
    assert diss(portless, d) and not(portless[76] & d) and not(portless[83] & d)
    assert all(literal(portless, s, x) for x in range(90) if x not in s)
    for v in s:
        assert any(not literal(portless, s-{v}, x) for x in (set(range(90))-s)|{v})
    report['safe_port'] = {'edge': [76, 83], 'selected_neighbourhoods_unchanged': True,
                           'attaining_endpoints_isolated_after_deletion': True}
    report['scope'] = ('General analytic cap and all-k proof in the note. Exact unrestricted solve of the 60-vertex core only; '
                       'local attachment enumeration and literal checks of six whole family graphs. No exact SF, Lean or priority claim.')
    out = ROOT/'output/subcubic-selected-star-check.json'
    out.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'result': 'PASS', 'core_beta': report['local']['core_independent_exact'],
                      'physical_models': len(report['models']), 'deletion_witnesses': sum(r['selected'] for r in report['models']),
                      'single_cuts': sum(r['single_vertex_cuts_checked'] for r in report['models']),
                      'report_bytes': out.stat().st_size}))


if __name__ == '__main__':
    main()
