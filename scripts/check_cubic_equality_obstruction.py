#!/usr/bin/env python3
"""Independent finite controls of the general cubic equality exclusion."""
from collections import Counter
from itertools import permutations
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
from check_subcubic_selected_stars import diss

if not __debug__:
    raise RuntimeError('Assertions must be enabled')


def graph_components(g):
    unseen = set(range(len(g)))
    components = []
    while unseen:
        seen = {min(unseen)}
        todo = list(seen)
        while todo:
            for b in g[todo.pop()] - seen:
                seen.add(b)
                todo.append(b)
        unseen -= seen
        components.append(seen)
    return components


def degree_two_controls():
    counts = Counter()
    for left, right in ((1, 1), (2, 2), (2, 3), (3, 4), (4, 0)):
        for bits in range(1 << (left*right)):
            g = [set() for _ in range(left+right)]
            for a in range(left):
                for b in range(right):
                    if bits >> (a*right+b) & 1:
                        g[a].add(left+b)
                        g[left+b].add(a)
            if max(map(len, g), default=0) > 2:
                continue
            n = len(g)
            beta = max(len(q) for mask in range(1 << n)
                       if diss(g, q := {a for a in range(n) if mask >> a & 1}))
            four_cycles = all(len(c) == 4 and all(len(g[a]) == 2 for a in c)
                              for c in graph_components(g))
            assert 2*beta >= n and (2*beta == n) == four_cycles
            counts['graphs'] += 1
            counts['literal_subsets'] += 1 << n
            counts['equalities'] += four_cycles
    # Several C4's, and paths/cycles beyond the exhaustive graph range.
    g = [set() for _ in range(8)]
    for h in (0, 4):
        for a in range(4):
            b = h+(a+1) % 4
            g[h+a].add(b)
            g[b].add(h+a)
    assert max(len(q) for mask in range(256)
               if diss(g, q := {a for a in range(8) if mask >> a & 1})) == 4
    larger = []
    for cycle in (False, True):
        for n in range(1 if not cycle else 4, 21, 1 if not cycle else 2):
            g = [{b for b in (a-1, a+1) if 0 <= b < n} for a in range(n)]
            if cycle:
                g[0].add(n-1)
                g[n-1].add(0)
            # A two-bit transfer, independent of the asserted closed formula.
            best = 0
            if n <= 12:
                best = max(len(q) for mask in range(1 << n)
                           if diss(g, q := {a for a in range(n) if mask >> a & 1}))
            else:
                states = {(0, 0, 0, 0): 0}
                for j in range(n):
                    nxt = {}
                    for (first, second, a, b), val in states.items():
                        for bit in (0, 1):
                            if a and b and bit:
                                continue
                            key = (bit if j == 0 else first, bit if j == 1 else second, b, bit)
                            nxt[key] = max(nxt.get(key, -1), val+bit)
                    states = nxt
                best = max(v for (first, second, a, b), v in states.items()
                           if not cycle or not ((a and b and first) or (b and first and second)))
            expected = (2*n)//3 if cycle else (2*n+2)//3
            assert best == expected
            larger.append({'kind': 'cycle' if cycle else 'path', 'n': n, 'beta': best})
    return {'exhaustive': dict(counts), 'two_disjoint_C4_subsets': 256, 'path_cycle_controls': larger}


def oriented_exchange(r, perm):
    # There are 4r six-vertex blocks. Their private a's form r C4's;
    # their helped b's have an arbitrary matching between opposite colours.
    blocks = 4*r
    g = [set() for _ in range(8*blocks)]

    def edge(a, b):
        assert a != b and b not in g[a]
        g[a].add(b)
        g[b].add(a)

    for j in range(blocks):
        for a in range(5):
            edge(6*j+a, 6*j+a+1)
    for t in range(r):
        for a in range(4):
            edge(6*(4*t+a), 6*(4*t+(a+1) % 4))
    left = list(range(0, blocks, 2))
    right = list(range(1, blocks, 2))
    matching = [(a, right[perm[j]]) for j, a in enumerate(left)]
    incidence = [[] for _ in range(r)]
    for t, (a, b) in enumerate(matching):
        edge(6*a+4, 6*b+4)
        incidence[a//4].append(t)
        incidence[b//4].append(t)
    for j in range(blocks):
        edge(6*blocks+2*j, 6*blocks+2*j+1)
    assert all(len(row) == 4 for row in incidence)
    unused = set(range(len(matching)))
    state_a = set()
    closed_trails = 0
    loops = sum(a//4 == b//4 for a, b in matching)
    while unused:
        start = matching[min(unused)][0]//4
        current = start
        while True:
            choices = [e for e in incidence[current] if e in unused]
            if not choices:
                assert current == start
                break
            e = min(choices)
            unused.remove(e)
            a, b = matching[e]
            if a//4 != current:
                a, b = b, a
            assert a//4 == current
            state_a.add(b)
            current = b//4
        closed_trails += 1
    assert all(len(state_a & set(range(4*t, 4*t+4))) == 2 for t in range(r))
    assert all(len(state_a & {a, b}) == 1 for a, b in matching)
    d = set(range(6*blocks, 8*blocks))
    for j in range(blocks):
        d.update(6*j+a for a in ((0, 2, 3, 5) if j in state_a else (1, 2, 4, 5)))
    assert len(d) == 6*blocks and diss(g, d)
    return {'private_cycles': r, 'blocks': blocks, 'matching': matching,
            'state_A_blocks': sorted(state_a), 'loops': loops,
            'closed_trails': closed_trails, 'physical_dissociation_size': len(d)}


def main():
    report = {'degree_two_classification': degree_two_controls(), 'exchange_controls': []}
    for r in (1, 2, 3):
        for p in permutations(range(2*r)):
            report['exchange_controls'].append(oriented_exchange(r, p))
    rng = random.Random(2026111204)
    for r in (4, 5, 8, 16, 64, 128):
        for _ in range(4):
            p = list(range(2*r))
            rng.shuffle(p)
            report['exchange_controls'].append(oriented_exchange(r, p))
    report['scope'] = ('General all-d proof in the note. These are witness-kernel controls; no cubic completions, '
                       'exact cubic optima, asymptotic sharpness, unrestricted-SF value or Lean validation are asserted.')
    out = ROOT/'output/cubic-equality-obstruction-check.json'
    out.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'result': 'PASS', 'degree_two': report['degree_two_classification']['exhaustive'],
                      'matching_models': len(report['exchange_controls']),
                      'loop_models': sum(r['loops'] > 0 for r in report['exchange_controls']),
                      'report_bytes': out.stat().st_size}))


if __name__ == '__main__':
    main()
