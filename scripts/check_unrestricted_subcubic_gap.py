#!/usr/bin/env python3
"""Physical template, extraction, cross-edge and exact-budget controls."""
from collections import Counter
from itertools import combinations, product
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from subcubic_partial_template import full_certificate, layers, template_certificates
from check_subcubic_intrinsic_obstruction import diss, exact, literal, private_optimum

if not __debug__:
    raise RuntimeError('Assertions must be enabled')

COUNTS = Counter()
FEATURES = Counter()
DIGEST = hashlib.sha256()


def valid_graph(g, colour):
    assert all(v != u and v in g[u] and colour[v] != colour[u]
               for v in range(len(g)) for u in g[v])
    assert all(len(row) <= 3 for row in g)


def all_minimal(g):
    n = len(g)
    masks = [sum(1 << u for u in row) for row in g]
    form = []
    beta = 0
    for bits in range(1 << n):
        if all((masks[v] & bits).bit_count() <= 1 for v in range(n) if bits >> v & 1):
            beta = max(beta, bits.bit_count())
        okay = True
        for v in range(n):
            if bits >> v & 1:
                continue
            ns = masks[v] & bits
            if ns.bit_count() >= 2:
                continue
            if not ns or not (masks[ns.bit_length()-1] & bits):
                okay = False
                break
        form.append(okay)
    minimal = []
    for bits in range(1 << n):
        if form[bits] and all(not form[bits ^ (1 << v)] for v in range(n) if bits >> v & 1):
            minimal.append({v for v in range(n) if bits >> v & 1})
    return beta, minimal


def check_selection(g, colour, S, beta):
    D, data = full_certificate(g, S, colour, beta)
    w, m, ledger = data['witnesses'], data['template'], data['counts']
    assert diss(g, D) and len(D) <= beta
    assert not (data['inner'] & data['retained'])
    assert all(not (g[v] & data['inner']) for v in data['retained'])
    assert diss(g, data['retained'])
    assert all(diss(g, t) for t in data['alternatives'])
    assert len(m['C']) == len(m['X']) == 2*len(m['I'])
    assert all(g[x] & S == {m['owner'][x], m['centre'][x]} for x in m['X'])
    assert all(len(g[c] & m['C']) <= 2 for c in m['C'])
    assert all(len(g[x] & m['X']) <= 1 for x in m['X'])
    assert 7*len(data['inner']) >= 18*len(m['I'])
    assert 111*(len(S)-beta) <= 11*len(g)
    for key in ('p', 'a', 'b3', 'r', 'q', 'e'):
        FEATURES[key+'_positive'] += ledger[key] > 0
    FEATURES['nonempty_template'] += bool(m['I'])
    FEATURES['retained_leaf'] += bool(w['triples'])
    FEATURES['unbalanced_template'] += sum(1 if colour[i] else -1 for i in m['I']) != 0
    FEATURES['partial_interface'] += any(not (g[x] & m['X']) for x in m['X'])
    FEATURES['positive_gap'] += len(S) > beta
    FEATURES['selected_degree_two'] += any(len(g[v] & S) == 2 for v in S)
    COUNTS['minimal_selections'] += 1
    DIGEST.update(json.dumps([len(g), sorted(S), beta, sorted(D), ledger], sort_keys=True).encode()+b'\n')


def check_graph(g, colour):
    valid_graph(g, colour)
    beta, selections = all_minimal(g)
    assert exact(g)[0] == beta
    for S in selections:
        check_selection(g, colour, S, beta)
    COUNTS['graphs'] += 1
    COUNTS['literal_subsets'] += 1 << len(g)


def matchings(left, right):
    if not left:
        yield []
        return
    yield from matchings(left[1:], right)
    for v in right:
        for remaining in matchings(left[1:], [w for w in right if w != v]):
            yield [(left[0], v)] + remaining


def partial_model(b, r, core, interface):
    I, X, C = set(range(b)), set(range(b, 3*b)), set(range(3*b, 5*b))
    colour = {i: int(i >= r) for i in I}
    owner, centre = {}, {}
    g = [set() for _ in range(5*b)]

    def edge(a, c):
        g[a].add(c)
        g[c].add(a)

    for i in range(b):
        for t in range(2):
            x, c = b+2*i+t, 3*b+2*i+t
            colour[x], colour[c] = 1-colour[i], colour[i]
            owner[x], centre[x] = c, i
            edge(i, x)
            edge(c, x)
    for a, c in core+interface:
        edge(a, c)
    return layers(g, C, I, X, owner, centre, colour)


def check_template(m, optimize):
    g, colour, b = m['g'], m['graph_colour'], len(m['I'])
    valid_graph(g, colour)
    D, meta = template_certificates(m)
    assert all(diss(g, d) for d in meta['alternatives']) and diss(g, D)
    assert 7*len(D) >= 18*b
    S = m['C'] | m['I']
    assert all(literal(g, S, x) for x in m['X'])
    inverse = {c: x for x, c in m['owner'].items()}
    assert all(not literal(g, S-{v}, v if v in m['I'] else inverse[v]) for v in S)
    if optimize:
        beta = exact(g)[0]
        assert beta == private_optimum(g, sorted(v for v in colour if not colour[v]))
        assert beta >= len(D)
        check_selection(g, colour, S, beta)
    COUNTS['partial_templates'] += 1
    FEATURES['template_path'] += any(not t for t in m['cyclic'])
    FEATURES['template_cycle'] += any(m['cyclic'])
    FEATURES['template_unbalanced'] += sum(1 if colour[i] else -1 for i in m['I']) != 0
    FEATURES['isolated_core_vertex'] += any(not (g[c] & m['C']) for c in m['C'])


def main():
    for n in range(8):
        for a in range(n//2+1):
            edges = list(product(range(a), range(a, n)))
            for bits in range(1 << len(edges)):
                g = [set() for _ in range(n)]
                for j, (v, w) in enumerate(edges):
                    if bits >> j & 1:
                        g[v].add(w)
                        g[w].add(v)
                if max(map(len, g), default=0) <= 3:
                    check_graph(g, {v: int(v >= a) for v in range(n)})
    exhaustive_graphs = COUNTS['graphs']
    for b in range(1, 4):
        for r in range(b+1):
            seed = partial_model(b, r, [], [])
            ca = sorted(c for c in seed['C'] if not seed['graph_colour'][c])
            cb = sorted(seed['C']-set(ca))
            xa = sorted(x for x in seed['X'] if not seed['graph_colour'][x])
            xb = sorted(seed['X']-set(xa))
            edges = list(product(ca, cb))
            for mask in range(1 << len(edges)):
                core = [edge for j, edge in enumerate(edges) if mask >> j & 1]
                if any(sum(v in edge for edge in core) > 2 for v in seed['C']):
                    continue
                for interface in matchings(xa, xb):
                    check_template(partial_model(b, r, core, interface), True)
    exhaustive_templates = COUNTS['partial_templates']
    rng = random.Random(111181)
    for j in range(90):
        n = rng.randrange(8, 13)
        a = rng.randrange(1, n)
        g = [set() for _ in range(n)]
        edges = list(product(range(a), range(a, n)))
        rng.shuffle(edges)
        for v, w in edges:
            if len(g[v]) < 3 and len(g[w]) < 3 and rng.random() < .6:
                g[v].add(w)
                g[w].add(v)
        check_graph(g, {v: int(v >= a) for v in range(n)})
    # Heawood: exact unrestricted beta and all minimal sets, including cycles.
    g = [set() for _ in range(14)]
    for j in range(7):
        for v in (j, (j-1) % 7, (j-3) % 7):
            g[v].add(7+j)
            g[7+j].add(v)
    beta, selections = all_minimal(g)
    assert beta == exact(g)[0] == 7
    assert max(map(len, selections)) == 8
    for S in selections:
        check_selection(g, {v: int(v >= 7) for v in range(14)}, S, beta)
    heawood_minimal = len(selections)
    for b in (4, 8, 16, 32):
        for j in range(12):
            r = rng.randrange(b+1)
            m = partial_model(b, r, [], [])
            colour = m['graph_colour']
            ca = [v for v in m['C'] if not colour[v]]
            cb = [v for v in m['C'] if colour[v]]
            xa = [v for v in m['X'] if not colour[v]]
            xb = [v for v in m['X'] if colour[v]]
            rng.shuffle(xa)
            rng.shuffle(xb)
            interface = list(zip(xa, xb))[:rng.randrange(min(len(xa), len(xb))+1)]
            core, degrees = [], Counter()
            edges = list(product(ca, cb))
            rng.shuffle(edges)
            for u, v in edges:
                if degrees[u] < 2 and degrees[v] < 2 and rng.random() < .6:
                    core.append((u, v))
                    degrees[u] += 1
                    degrees[v] += 1
            check_template(partial_model(b, r, core, interface), False)
    assert all(FEATURES[k] for k in ('p_positive', 'a_positive', 'b3_positive',
               'retained_leaf', 'nonempty_template', 'partial_interface', 'positive_gap'))
    report = dict(counts=dict(COUNTS), features=dict(FEATURES),
                  exhaustive_labelled_graphs=exhaustive_graphs,
                  exhaustive_partial_templates=exhaustive_templates,
                  heawood_all_minimal_sets=heawood_minimal,
                  exact_control_digest=DIGEST.hexdigest(),
                  scope='General written proof. Finite controls test physical extraction, safe retained leaves, partial/unbalanced templates and the exact nonnegative identity. Larger models check certificates, not exact optima. No graph-sharpness, Lean or grid theorem.')
    out = ROOT/'output/unrestricted-subcubic-gap-check.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': 'PASS', **report, 'report_bytes': out.stat().st_size,
                      'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
