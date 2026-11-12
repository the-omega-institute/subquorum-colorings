#!/usr/bin/env python3
"""Physical, all-phase and independent-optimum checks of odd-cycle credits."""
from collections import Counter
from fractions import Fraction
from itertools import product
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from subcubic_odd_cycle_compensation import full_certificate, template_certificates
from subcubic_partial_template import layers
from check_unrestricted_subcubic_gap import all_minimal, matchings, partial_model, valid_graph
from check_subcubic_intrinsic_obstruction import diss, exact, literal, private_optimum

if not __debug__:
    raise RuntimeError('Assertions must be enabled')

COUNTS, FEATURES = Counter(), Counter()
DIGEST = hashlib.sha256()


def components(g, allowed):
    unseen, answer = set(allowed), []
    while unseen:
        found, todo = {min(unseen)}, [min(unseen)]
        while todo:
            for u in (g[todo.pop()] & unseen)-found:
                found.add(u)
                todo.append(u)
        unseen -= found
        answer.append(found)
    return answer


def residual_optimum(g, allowed):
    """Independent component formula, not the production three-bit DP."""
    total = 0
    for comp in components(g, allowed):
        degrees = [len(g[v] & comp) for v in comp]
        assert max(degrees) <= 2
        cyclic = min(degrees) == 2
        assert not cyclic or len(comp) % 2 == 0
        total += (2*len(comp))//3 if cyclic else (2*len(comp)+2)//3
    return total


def reference_score(m, bits):
    R = {m['owner'][x] for x in m['X']
         if m['colour'][x] != bits[m['group'][x]]}
    bad_vertices, claimed_cycles = set(), set()
    score = Fraction(0)
    for j, (order, cyclic) in enumerate(zip(m['components'], m['cyclic'])):
        if not cyclic or len(order) % 8 != 4:
            continue
        for bit in (0, 1):
            U = {m['owner'][x] for x in order if m['colour'][x] == bit}
            bad = {v for v in U if len(m['g'][v] & U) <= 1}
            if bad:
                assert len(bad) >= 2 and not (bad & bad_vertices)
                bad_vertices |= bad
                score += Fraction(sum(v in R and len(m['g'][v] & R) <= 1
                                      for v in bad), 4)
            elif U <= R:
                assert all(m['g'][v] & m['C'] <= U for v in U)
                choices = [tuple(sorted(comp)) for comp in components(m['g'], U)
                           if len(comp) != 4]
                assert choices and choices[0] not in claimed_cycles
                claimed_cycles.add(choices[0])
                score += 1
    assert not bad_vertices & {v for comp in claimed_cycles for v in comp}
    optimum = residual_optimum(m['g'], R)
    assert Fraction(optimum)-Fraction(len(R), 2) >= score
    COUNTS['phase_assignments'] += 1
    return score, R, optimum


def check_selection(g, colour, S, beta):
    D, data = full_certificate(g, S, colour, beta)
    w, m, ledger = data['witnesses'], data['template'], data['counts']
    assert diss(g, D) and len(D) <= beta
    assert not data['inner'] & data['retained']
    assert all(not (g[v] & data['inner']) for v in data['retained'])
    assert diss(g, data['retained'])
    assert all(diss(g, d) for d in data['alternatives'])
    assert 12*len(data['inner']) >= 31*len(m['I'])
    assert 192*(len(S)-beta) <= 19*len(g)
    assert all(g[x] & S == {m['owner'][x], m['centre'][x]} for x in m['X'])
    for key in ('p', 'a', 'b3', 'r', 'q', 'e'):
        FEATURES[key+'_positive'] += ledger[key] > 0
    FEATURES['retained_leaf'] += bool(w['triples'])
    FEATURES['nonempty_extracted_template'] += bool(m['I'])
    FEATURES['positive_gap'] += len(S) > beta
    FEATURES['selected_degree_two'] += any(len(g[v] & S) == 2 for v in S)
    COUNTS['minimal_selections'] += 1
    DIGEST.update(json.dumps([len(g), sorted(S), beta, sorted(D), ledger],
                             sort_keys=True).encode()+b'\n')


def check_graph(g, colour):
    valid_graph(g, colour)
    beta, selections = all_minimal(g)
    assert exact(g)[0] == beta
    for S in selections:
        check_selection(g, colour, S, beta)
    COUNTS['graphs'] += 1
    COUNTS['literal_subsets'] += 1 << len(g)


def check_template(m, optimize=False, all_phases=False):
    g, b = m['g'], len(m['I'])
    valid_graph(g, m['graph_colour'])
    D, meta = template_certificates(m)
    assert diss(g, D) and all(diss(g, d) for d in meta['alternatives'])
    assert 12*len(D) >= 31*b
    phase, credits = meta['phase'], meta['phase']['credits']
    for row in credits['broken']:
        FEATURES['broken_classes'] += 1
        FEATURES['exactly_two_internal_defects'] += len(row['bad']) == 2
    FEATURES['intact_classes'] += len(credits['intact'])
    FEATURES['long_odd_cycles'] += sum(t and len(c) % 8 == 4 and len(c) > 4
                                     for c, t in zip(m['components'], m['cyclic']))
    FEATURES['partial_interface'] += any(not t for t in m['cyclic'])
    FEATURES['unbalanced_template'] += sum(1 if m['graph_colour'][i] else -1
                                            for i in m['I']) != 0
    FEATURES['fractional_initial_score'] += phase['initial'].denominator != 1
    S = m['C'] | m['I']
    assert all(literal(g, S, x) for x in m['X'])
    inverse = {c: x for x, c in m['owner'].items()}
    assert all(not literal(g, S-{v}, v if v in m['I'] else inverse[v]) for v in S)
    if optimize:
        beta = exact(g)[0]
        assert beta == private_optimum(g, [v for v in range(len(g))
                                          if not m['graph_colour'][v]])
        assert beta >= len(D)
        check_selection(g, m['graph_colour'], S, beta)
        COUNTS['exact_templates'] += 1
    if all_phases:
        scores = {}
        for bits in product((0, 1), repeat=len(m['components'])):
            score, R, optimum = reference_score(m, bits)
            scores[bits] = score
            if b <= 6:
                vertices = sorted(R)
                remap = {v: j for j, v in enumerate(vertices)}
                induced = [{remap[u] for u in g[v] & R} for v in vertices]
                assert exact(induced)[0] == optimum
                COUNTS['independent_residual_recurrences'] += 1
        assert sum(scores.values())/len(scores) == phase['initial']
        assert 4*sum(scores.values()) >= len(scores)*credits['odd']
        for k, expected in enumerate(phase['steps']):
            options = [s for bits, s in scores.items()
                       if all(bits[j] == phase['phases'][j] for j in range(k))]
            assert sum(options)/len(options) == expected
            COUNTS['conditional_expectation_comparisons'] += 1
        final = tuple(phase['phases'][j] for j in range(len(m['components'])))
        assert scores[final] == phase['score']
    COUNTS['templates'] += 1


def profile_model(cycle_ells, path_pairs, mode, seed=0):
    """Prescribed auxiliary cycles/paths, with physical original-colour edges."""
    specs = [(4*ell, True) for ell in cycle_ells]+[(2*h, False) for h in path_pairs]
    b = sum(n//2 for n, _ in specs)
    g = [set() for _ in range(5*b)]
    I, X, C = set(range(b)), set(range(b, 3*b)), set(range(3*b, 5*b))
    colour, owner, centre, phase_classes = {}, {}, {}, []

    def edge(v, u):
        assert v != u and colour[v] != colour[u]
        g[v].add(u)
        g[u].add(v)

    used_x, used_i = 0, 0
    for n, cyclic in specs:
        order = list(range(b+used_x, b+used_x+n))
        for k, x in enumerate(order):
            c = 3*b+(x-b)
            colour[x], colour[c] = (k//2) % 2, 1-(k//2) % 2
            owner[x] = c
            centre[x] = used_i+k//2
            colour[centre[x]] = 1-colour[x]
            edge(x, c)
            edge(x, centre[x])
        for k in range(1, n-1, 2):
            edge(order[k], order[k+1])
        if cyclic:
            edge(order[-1], order[0])
        phase_classes += [{owner[x] for k, x in enumerate(order) if k % 2 == bit}
                          for bit in (0, 1)] if cyclic else []
        used_x += n
        used_i += n//2
    rng = random.Random(seed)
    if mode in ('intact', 'broken'):
        endpoints = []
        for U in phase_classes:
            a = sorted(v for v in U if not colour[v])
            c = sorted(U-set(a))
            seq = [v for pair in zip(a, c) for v in pair]
            if mode == 'intact' and len(seq) >= 4:
                # A long intact class may consist of C4 plus a longer cycle.
                chunks = [seq[:4], seq[4:]] if len(seq) >= 10 else [seq]
                for part in chunks:
                    for v, u in zip(part, part[1:]+part[:1]):
                        edge(v, u)
            else:
                for v, u in zip(seq, seq[1:]):
                    edge(v, u)
                endpoints.append((seq[0], seq[-1]))
        if mode == 'broken' and len(endpoints) > 1:
            for j, (_, v) in enumerate(endpoints):
                edge(v, endpoints[(j+1) % len(endpoints)][0])
    elif mode == 'random':
        edges = list(product([v for v in C if not colour[v]],
                             [v for v in C if colour[v]]))
        rng.shuffle(edges)
        for v, u in edges:
            if len(g[v] & C) < 2 and len(g[u] & C) < 2 and rng.random() < .65:
                edge(v, u)
    else:
        assert mode == 'empty'
    return layers(g, C, I, X, owner, centre, colour)


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
                core = [e for j, e in enumerate(edges) if mask >> j & 1]
                if any(sum(v in e for e in core) > 2 for v in seed['C']):
                    continue
                for interface in matchings(xa, xb):
                    check_template(partial_model(b, r, core, interface), True, True)
    exhaustive_templates = COUNTS['templates']
    rng = random.Random(111181)
    for _ in range(90):
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
    g = [set() for _ in range(14)]
    for j in range(7):
        for v in (j, (j-1) % 7, (j-3) % 7):
            g[v].add(7+j)
            g[7+j].add(v)
    beta, selections = all_minimal(g)
    assert beta == exact(g)[0] == 7 and max(map(len, selections)) == 8
    for S in selections:
        check_selection(g, {v: int(v >= 7) for v in range(14)}, S, beta)
    profiles = [([1], []), ([2], []), ([3], []), ([5], []), ([7], []),
                ([1, 3], []), ([1, 1, 2], []), ([3, 5], []),
                ([1, 3, 2], [1, 2]), ([], [1, 2, 3, 4]), ([1, 1, 1, 1], [4])]
    targeted = 0
    for cycles, paths in profiles:
        for j, mode in enumerate(('empty', 'intact', 'broken', 'random')):
            check_template(profile_model(cycles, paths, mode, 831+j), False, True)
            targeted += 1
    for j in range(12):
        check_template(profile_model([1, 2, 3, 5], [1, 3, 4], 'random', 900+j),
                       False, True)
        targeted += 1
    for cycles, paths in [([1]*64, []), ([3]*24, [1, 2, 5]),
                          ([1]*8+[3]*8+[5]*4+[2]*3, [1, 2, 5, 8])]:
        for mode in ('intact', 'broken', 'random'):
            check_template(profile_model(cycles, paths, mode, 111192), False, False)
    assert all(FEATURES[k] for k in ('long_odd_cycles', 'intact_classes',
               'broken_classes', 'exactly_two_internal_defects',
               'partial_interface', 'unbalanced_template', 'retained_leaf',
               'b3_positive', 'positive_gap'))
    report = dict(counts=dict(COUNTS), features=dict(FEATURES),
            exhaustive_graph_models=exhaustive_graphs,
            exhaustive_partial_templates=exhaustive_templates,
            all_phase_targeted_templates=targeted,
            heawood_minimal_selections=len(selections),
            exact_control_digest=DIGEST.hexdigest(),
            scope='Written general proof. Exhaustive templates check one distinguished minimal set each; general graph controls check all minimal sets. All-phase comparisons use independent residual component formulas and local-event expectations. Larger templates check physical certificates, not unrestricted optima. No Lean or graph-sharpness.')
    out = ROOT/'output/odd-cycle-compensation-check.json'
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': 'PASS', **report, 'report_bytes': out.stat().st_size,
                     'sha256': hashlib.sha256(out.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
