#!/usr/bin/env python3
"""Physical and exact controls for vertex penalties and the 51/517 bound."""
from collections import Counter
from fractions import Fraction
from functools import lru_cache
from itertools import product
from pathlib import Path
import hashlib, json, random, sys
ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT/'develop'), str(ROOT/'scripts')]
from subcubic_boundary_expectation import weighted_template, full_certificate, potential
from subcubic_phase_pairing import expectation
from subcubic_intrinsic_obstruction import path_cycle_optimum
from subcubic_partial_template import layers
from check_unrestricted_subcubic_gap import all_minimal, matchings, partial_model, valid_graph
from check_subcubic_intrinsic_obstruction import diss, exact
from check_two_endpoint import long_class_paths, mixed_loss_model
from check_odd_cycle_compensation import profile_model
from check_zero_budget_repair import zero_model
if not __debug__: raise RuntimeError('Assertions required')
COUNTS, FEATURES = Counter(), Counter()
DIGEST = hashlib.sha256()


def exact_weighted(g, costs):
    adj = [sum(1 << u for u in row) for row in g]
    @lru_cache(None)
    def solve(mask):
        if not mask: return Fraction(0)
        v = max((v for v in range(len(g)) if mask >> v & 1),
                key=lambda v: (adj[v] & mask).bit_count())
        ns = adj[v] & mask; closed = ns | (1 << v)
        best = max(solve(mask ^ (1 << v)), 1-costs[v]+solve(mask & ~closed))
        while ns:
            bit = ns & -ns; ns -= bit; u = bit.bit_length()-1
            best = max(best, 2-costs[v]-costs[u]+solve(mask & ~(closed | adj[u])))
        return best
    return solve((1 << len(g))-1)


def selection(g, colour, S, beta):
    D, a = full_certificate(g, S, colour, beta)
    assert all(diss(g, Q) and len(Q) <= beta for Q in a['alternatives'])
    assert D in a['alternatives']
    assert sum(a['nonnegative_terms']) == 102*len(g)-1034*(len(S)-beta)
    c = a['preceding']['counts']
    for k in ('p', 'q', 'e', 'b3', 'Z'): FEATURES['ambient_'+k] += c[k] > 0
    for layer, cost in a['weighted']['layer_costs'].items(): FEATURES['boundary_'+layer] += cost > 0
    old_size = len(a['preceding']['inner'])
    FEATURES['weighted_inner_smaller'] += len(a['inner']) < old_size
    FEATURES['weighted_inner_different'] += a['inner'] != a['preceding']['inner']
    FEATURES['new_full_set_improves_old'] += len(D) > max(map(len, a['preceding']['alternatives']))
    COUNTS['minimal_selections'] += 1
    DIGEST.update(json.dumps([len(g), sorted(S), beta, sorted(D), str(a['W'])]).encode()+b'\n')


def graph(g, colour):
    valid_graph(g, colour); beta, ss = all_minimal(g)
    assert beta == exact(g)[0]
    for S in ss: selection(g, colour, S, beta)
    COUNTS['graphs'] += 1


def template(m, all_phases=True, optimize=False):
    valid_graph(m['g'], m['graph_colour'])
    H = m['I'] | m['C'] | m['X']
    COUNTS['exact_weighted_template_models'] += optimize
    assignments = [
        {v: Fraction(0) for v in H},
        {v: Fraction(1, 2) for v in H},
        {v: Fraction((v*7+3) % 5, 2) for v in H},
        {v: Fraction(int(v in m['X'])) for v in H},
    ]
    if H:
        assignments.append({v: Fraction((1 << 400) if v == min(H) else (v % 3), 3) for v in H})
    for costs in assignments:
        D, a = weighted_template(m, costs)
        assert all(diss(m['g'], Q) for Q in a['alternatives'])
        assert potential(D, costs) >= a['guarantee']
        if optimize:
            optimum = exact_weighted(m['g'], costs)
            assert optimum >= potential(D, costs)
            COUNTS['exact_weighted_instances'] += 1
            if len(m['g']) <= 5:
                literal = max(potential({v for v in H if mask >> v & 1}, costs)
                              for mask in range(1 << len(m['g']))
                              if diss(m['g'], {v for v in H if mask >> v & 1}))
                assert optimum == literal
                COUNTS['literal_weighted_crosschecks'] += 1
        if all_phases:
            scores = {}
            b = len(m['I'])
            cost_I = sum((costs[v] for v in m['I']), Fraction(0))
            for bits in product((0, 1), repeat=len(m['components'])):
                selected = {x for x in m['X'] if m['colour'][x] == bits[m['group'][x]]}
                retained = m['C']-{m['owner'][x] for x in selected}
                actual = m['I'] | selected | path_cycle_optimum(m['g'], retained)
                score = expectation(a['terms'], dict(enumerate(bits)))
                assert diss(m['g'], actual)
                assert potential(actual, costs) >= Fraction(8*b, 3)-cost_I+score
                scores[bits] = score
                COUNTS['physical_weighted_phases'] += 1
            assert sum(scores.values())/len(scores) == a['initial']
            for j, value in enumerate(a['steps']):
                eligible = [v for bits, v in scores.items()
                            if all(bits[k] == a['phases'][k] for k in range(j))]
                assert sum(eligible)/len(eligible) == value
                COUNTS['conditional_expectation_controls'] += 1
        FEATURES['positive_sigma'] += a['resources']['sigma'] > 0
        FEATURES['good_auxiliary'] += a['resources']['bG'] > 0
        FEATURES['bad_physical'] += a['resources']['tb'] > 0
        FEATURES['bad_auxiliary'] += a['resources']['sb'] > 0
        COUNTS['cost_assignments'] += 1
    COUNTS['templates'] += 1


def main():
    for n in range(8):
        for left in range(n//2+1):
            edges = list(product(range(left), range(left, n)))
            for mask in range(1 << len(edges)):
                g = [set() for _ in range(n)]
                for j, (v, u) in enumerate(edges):
                    if mask >> j & 1: g[v].add(u); g[u].add(v)
                if max(map(len, g), default=0) <= 3: graph(g, {v: int(v >= left) for v in range(n)})
    exhaustive = COUNTS['graphs']
    for b in range(1, 4):
        for left in range(b+1):
            s = partial_model(b, left, [], [])
            aa = sorted(v for v in s['C'] if not s['graph_colour'][v]); bb = sorted(s['C']-set(aa))
            xa = sorted(v for v in s['X'] if not s['graph_colour'][v]); xb = sorted(s['X']-set(xa))
            edges = list(product(aa, bb))
            for mask in range(1 << len(edges)):
                core = [e for j, e in enumerate(edges) if mask >> j & 1]
                if any(sum(v in e for e in core) > 2 for v in s['C']): continue
                for interface in matchings(xa, xb):
                    m = partial_model(b, left, core, interface)
                    template(m, optimize=b <= 2)
                    beta = exact(m['g'])[0]
                    selection(m['g'], m['graph_colour'], m['I'] | m['C'], beta)
                    COUNTS['exact_small_templates'] += 1
    rng = random.Random(51751)
    for _ in range(90):
        n = rng.randrange(8, 13); left = rng.randrange(1, n)
        g = [set() for _ in range(n)]; edges = list(product(range(left), range(left, n))); rng.shuffle(edges)
        for v, u in edges:
            if len(g[v]) < 3 and len(g[u]) < 3 and rng.random() < .6: g[v].add(u); g[u].add(v)
        graph(g, {v: int(v >= left) for v in range(n)})
    g = [set() for _ in range(14)]
    for j in range(7):
        for v in (j, (j-1) % 7, (j-3) % 7): g[v].add(7+j); g[7+j].add(v)
    beta, ss = all_minimal(g); assert beta == exact(g)[0] == 7
    for S in ss: selection(g, {v: int(v >= 7) for v in range(14)}, S, beta)
    profiles = [([1], []), ([3], []), ([5], []), ([2], []), ([4], []), ([], [4]),
                ([], [8]), ([1, 1], []), ([1, 3], []), ([3, 3, 1], []),
                ([1], [4]), ([3, 2], [4]), ([1, 3, 2], [4, 8])]
    for cycles, paths in profiles:
        for mode in ('empty', 'matching', 'cycle', 'random'):
            for seed in range(4): template(zero_model(cycles, paths, mode, seed))
        for mode in ('empty', 'intact', 'random', 'broken'):
            for seed in range(6): template(profile_model(cycles, paths, mode, seed))
    for cycles, paths, good in [([], [4], False), ([3], [], False), ([5], [], False),
                               ([3], [4], True), ([2, 3], [4], True)]:
        template(long_class_paths(cycles, paths, good))
    for cyclic in (False, True): template(mixed_loss_model(cyclic))
    assert all(FEATURES[k] > 0 for k in ('boundary_I', 'boundary_C', 'boundary_X',
                                       'positive_sigma', 'good_auxiliary', 'bad_physical', 'bad_auxiliary',
                                       'weighted_inner_different'))
    report = {'status': 'PASS', 'counts': dict(sorted(COUNTS.items())),
              'features': dict(sorted(FEATURES.items())), 'exhaustive_graph_models': exhaustive,
              'ambient_digest': DIGEST.hexdigest(),
              'scope': 'General nonnegative vertex-penalty lemma and universal 517d<=51n proof. All minimal sets in the small, seeded and specified cubic graph controls; separately canonical minimal selections on5200 templates; physical candidate sets, ambient exterior extensions, all phases and conditional expectations for prescribed templates. 580 exact unrestricted weighted instances on116 template models with b<=2 (order<=10); all 5200 small templates use exact unweighted ambient beta. Larger templates check actual candidates and all phases, not unrestricted large optima. Zero costs and rational costs with 401-bit numerators. Earlier imported main suites are not executed. No sharpness, Lean or grid claim.'}
    data = (json.dumps(report, indent=2, sort_keys=True)+'\n').encode()
    (ROOT/'output/boundary-expectation-check.json').write_bytes(data)
    print(json.dumps({'status': 'PASS', 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}))


if __name__ == '__main__': main()
