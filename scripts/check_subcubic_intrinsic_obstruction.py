#!/usr/bin/env python3
"""Physical checks and independent unrestricted optimization of the template."""
from collections import Counter
from functools import lru_cache
from itertools import combinations, permutations, product
from pathlib import Path
import hashlib
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from subcubic_intrinsic_obstruction import certificates, template

if not __debug__:
    raise RuntimeError('Run with assertions enabled')


def diss(g, D):
    return all(len(g[v] & D) <= 1 for v in D)


def literal(g, S, outside):
    for c in {outside} | g[outside]:
        for a, b in combinations(g[c], 2):
            if outside in (c, a, b) and len({c, a, b} & S) == 2:
                return True
    return False


def exact(g):
    """Unrestricted excluded/isolated/paired recurrence, independent of phases."""
    adj = [sum(1 << u for u in row) for row in g]

    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        vertices = [v for v in range(len(g)) if mask >> v & 1]
        v = max(vertices, key=lambda u: (adj[u] & mask).bit_count())
        ns = adj[v] & mask
        if not ns:
            return mask.bit_count()
        closed = ns | (1 << v)
        best = max(solve(mask ^ (1 << v)), 1+solve(mask & ~closed))
        while ns:
            bit = ns & -ns
            ns -= bit
            best = max(best, 2+solve(mask & ~(closed | adj[bit.bit_length()-1])))
        return best

    return solve((1 << len(g))-1), solve.cache_info().currsize


def private_optimum(g, A):
    B = set(range(len(g))) - set(A)
    rows = [sum(1 << j for j, a in enumerate(A) if a in g[b]) for b in B]
    best = 0
    for mask in range(1 << len(A)):
        private, empty = 0, 0
        for row in rows:
            ns = row & mask
            if not ns:
                empty += 1
            elif ns & (ns-1) == 0:
                private |= ns
        best = max(best, mask.bit_count()+private.bit_count()+empty)
    return best


def validate(m, optimize=False, brute=False, all_phases=False):
    k, g = m['k'], m['g']
    h = 2*k
    A = set(range(h)) | set(range(2*h, 3*h)) | set(range(4*h, 4*h+k))
    assert len(g) == 10*k and len(A) == 5*k
    assert all(v != u and v in g[u] and ((v in A) != (u in A))
               for v in range(len(g)) for u in g[v])
    assert all(len(g[v]) == (2 if v in m['I'] else 3) for v in range(len(g)))
    S = m['I'] | m['C']
    assert len(S) == 6*k and all(literal(g, S, x) for x in m['X'])
    inverse = {c: x for x, c in m['owner'].items()}
    for v in S:
        w = v if v in m['I'] else inverse[v]
        assert w not in S-{v} and not literal(g, S-{v}, w)
    best, side, phased, ledger, phase = certificates(m)
    delta, k0 = ledger['delta'], ledger['k0']
    assert sum(ledger['lengths']) == k
    assert delta*3 >= k-k0
    assert all(diss(g, D) for D in (best, side, phased))
    assert len(side) == 5*k+delta
    assert phase['initial'] >= k0
    assert phase['L'] >= int(phase['expectation'][-1]) >= k0
    short_core = {m['owner'][x] for comp in m['components'] if len(comp) == 4 for x in comp}
    final_short_low = sum(len(g[v] & phase['R']) <= 1 for v in phase['R'] & short_core)
    assert str(final_short_low) == phase['expectation'][-1]
    assert 4*len(phase['Z']) >= 4*k+phase['L']
    assert len(phased) >= 5*k+(k0+3)//4
    assert len(best) >= 5*k+max(delta, (k0+3)//4) >= 5*k+(k+6)//7
    row = dict(k=k, lengths=ledger['lengths'], delta=delta, k0=k0,
               side=len(side), phased=len(phased), bound=5*k+(k+6)//7,
               low_degree=phase['L'], initial_expectation=str(phase['initial']))
    phase_count = 0
    if all_phases:
        total_low = 0
        for bits in product((0, 1), repeat=len(m['components'])):
            Y = {x for x in m['X'] if m['colour'][x] == bits[m['group'][x]]}
            R = m['C']-{m['owner'][x] for x in Y}
            low = sum(len(g[v] & R) <= 1 for v in R)
            short_low = sum(len(g[v] & R) <= 1 for v in R & short_core)
            assert len(Y) == len(R) == 2*k
            assert all(len({x, m['pair'][x]} & Y) == 1 for x in m['X'])
            assert all(len({x, m['q'][x]} & Y) == 1 for x in m['X'])
            relabel = {v: j for j, v in enumerate(sorted(R))}
            residual = [{relabel[u] for u in g[v] & R} for v in sorted(R)]
            z, _ = exact(residual)
            assert z == private_optimum(residual, [relabel[v] for v in sorted(A & R)])
            assert 4*z >= 4*k+low and diss(g, m['I'] | Y)
            total_low += short_low
            phase_count += 1
        assert str(phase['initial']) == str(__import__('fractions').Fraction(total_low, phase_count))
    row['all_phase_controls'] = phase_count
    if optimize:
        beta, states = exact(g)
        assert beta == private_optimum(g, sorted(A)) and beta >= len(best)
        row.update(beta=beta, states=states)
    if brute:
        maximum = max(mask.bit_count() for mask in range(1 << len(g))
                      if diss(g, {v for v in range(len(g)) if mask >> v & 1}))
        assert maximum == row['beta']
        row['literal_subsets'] = 1 << len(g)
    return row


def two_regular_cores(h):
    for rows in product(list(combinations(range(h), 2)), repeat=h):
        if any(sum(b in row for row in rows) != 2 for b in range(h)):
            continue
        # A bipartite two-regular graph decomposes into two perfect matchings.
        p = next(p for p in permutations(range(h)) if all(p[a] in rows[a] for a in range(h)))
        q = tuple(next(b for b in rows[a] if b != p[a]) for a in range(h))
        assert len(set(q)) == h
        yield p, q


def seeded(k, rng, matching_kind):
    h = 2*k
    p = list(range(h))
    rng.shuffle(p)
    while True:
        q = list(range(h))
        rng.shuffle(q)
        if all(a != b for a, b in zip(p, q)):
            break
    interface = list(range(h))
    if matching_kind == 'arbitrary':
        rng.shuffle(interface)
    elif matching_kind == 'pair-preserving':
        order = list(range(k))
        rng.shuffle(order)
        interface = []
        for j in range(k):
            flip = rng.randrange(2)
            interface.extend(2*order[j]+(a ^ flip) for a in (0, 1))
    else:
        # One long component, including odd ell where delta/ell=1/3 is tight.
        interface = [i if i % 2 == 0 else (i+2) % h for i in range(h)]
    return template(k, p, q, interface)


def path_cycle_controls():
    from subcubic_intrinsic_obstruction import path_cycle_optimum
    count = 0
    for n in range(1, 25):
        for cyclic in (False, True):
            if cyclic and (n < 4 or n % 2):
                continue
            g = [{u for u in (v-1, v+1) if 0 <= u < n} for v in range(n)]
            if cyclic:
                g[0].add(n-1)
                g[-1].add(0)
            D = path_cycle_optimum(g, set(range(n)))
            target = (2*n)//3 if cyclic else (2*n+2)//3
            assert diss(g, D) and len(D) == target
            if n <= 10:
                assert exact(g)[0] == target
            count += 1
    return count


def main():
    report = {'path_cycle_models': path_cycle_controls(), 'exhaustive': {}, 'seeded': [], 'large': []}
    histogram, digest, total, phases, subsets = Counter(), hashlib.sha256(), 0, 0, 0
    for k in (1, 2):
        controls = 0
        for p, q in two_regular_cores(2*k):
            for interface in permutations(range(2*k)):
                m = template(k, p, q, interface)
                row = validate(m, optimize=True, brute=(k == 1), all_phases=True)
                if k == 2 and row['beta'] == 11 and 'twenty_vertex_certificate' not in report:
                    D, _, _, ledger, phase = certificates(m)
                    report['twenty_vertex_certificate'] = dict(
                        first=list(p), second=list(q), interface=list(interface),
                        graph=[sorted(ns) for ns in m['g']],
                        selected=sorted(m['C'] | m['I']), dissociation=sorted(D),
                        beta=row['beta'], phases=phase['phases'], lengths=ledger['lengths'])
                histogram[f"k{k}:beta{row['beta']}"] += 1
                digest.update(json.dumps([p, q, interface, row], sort_keys=True).encode()+b'\n')
                controls += 1
                phases += row['all_phase_controls']
                subsets += row.get('literal_subsets', 0)
        report['exhaustive'][str(k)] = controls
        total += controls
    rng = random.Random(20261112)
    for k in (3, 4, 5, 7, 8):
        for kind in ('arbitrary', 'pair-preserving', 'one-long-cycle'):
            for j in range(4):
                row = validate(seeded(k, rng, kind), optimize=(k == 3), all_phases=(k <= 5))
                row.update(kind=kind, replicate=j)
                report['seeded'].append(row)
    for k in (16, 64, 256):
        for kind in ('arbitrary', 'pair-preserving', 'one-long-cycle'):
            row = validate(seeded(k, rng, kind))
            row['kind'] = kind
            report['large'].append(row)
    report.update(exact_histogram=dict(sorted(histogram.items())), exhaustive_digest=digest.hexdigest(),
                  exhaustive_models=total, exhaustive_phase_controls=phases, literal_subsets=subsets,
                  scope='General written proofs, finite physical/independent exact controls; no sharpness, Lean or rectangular-grid theorem.')
    output = ROOT/'output/subcubic-intrinsic-obstruction-check.json'
    output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({'status': 'PASS', 'exhaustive': report['exhaustive'],
                      'seeded': len(report['seeded']), 'large': len(report['large']),
                      'report_bytes': output.stat().st_size,
                      'sha256': hashlib.sha256(output.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
