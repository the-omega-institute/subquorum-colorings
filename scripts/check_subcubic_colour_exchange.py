#!/usr/bin/env python3
"""Literal two-colour repairs and exact coefficient certificates; stdlib only."""
from collections import Counter
from itertools import product
from pathlib import Path
import json
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from subcubic_colour_repairs import construct
from compact_subcubic_selected_stars import core, base
from check_compact_subcubic_selected_stars import exact, diss, literal
import check_selected_star_general_budget as old
import check_full_degree_capacity as cut

if not __debug__:
    raise RuntimeError('Assertions must be enabled')


def check(g, S, beta, allocation, count):
    v, W, U, P, unused = allocation
    c, q, s, a, b2, b3, mu, m, z0, u = v
    C, leaves, I = old.structure(g, S)
    col = old.colors(g)
    assert max(map(len, g), default=0) <= 3
    assert all(len(g[w] & (S-I)) == 1 and len(g[w] & I) <= 1 for w in W)
    d = len(S)-beta
    model = construct(g, S, C, I, W, col)
    A = model['private']
    E = model['exceptional']
    assert len(model['blocks']) == c
    assert sum(kind == 'claw' for kind, *rest in model['blocks']) == s
    assert sum(kind == 'direct' for kind, *rest in model['blocks']) == q
    assert len(A) == c-q-s
    assert diss(g, model['baseline']) and len(model['baseline']) == len(S)-c
    assert diss(g, model['baseline_plus_exceptional'])
    assert len(model['baseline_plus_exceptional']) <= beta
    assert len(E) <= c-d
    assert sum(map(len, model['raw'])) == 2*(len(S)-c)+2*c-s
    deleted_a = set().union(*model['deleted_private'])
    deleted_i = set().union(*model['deleted_helpers'])
    assert deleted_a <= E and len(deleted_a) == sum(map(len, model['deleted_private']))
    assert len(deleted_i) == sum(map(len, model['deleted_helpers'])) <= b2+b3
    for D in model['repaired']:
        assert diss(g, D) and len(D) <= beta
    assert sum(map(len, model['repaired'])) >= 2*(len(S)-c)+2*c-s-len(E)-b2-b3
    assert 2*d <= s+len(E)+b2+b3
    K = c+s+b2+b3
    assert K >= 3*d
    J = c+s+2*q-a-2*b2-3*b3
    R = c-q+b2+b3-mu
    Tp = a+b2+b3-s-q
    Dslack = q+s+2*mu-2*b2
    h = {i: len(g[i] & W) for i in I}
    Z = {v for v in U if g[v] & S <= C | {i for i in I if h[i]}}
    free = len(Z)
    assert J >= 0 and Dslack >= 0 and R >= 2*d and Tp-free >= 2*d
    n = len(g)
    assert 4*n == 9*J+2*R+13*Tp+Dslack+9*K+2*s+7*b3+4*(m+z0+u)
    assert 57*d <= 4*n
    if min(map(len, g), default=0) >= 2:
        V = 2*u+free-a
        assert V >= 0
        assert 8*n == 21*J+2*R+33*(Tp-free)+Dslack+17*K+4*V+10*s+19*b3+8*(m+z0)+29*free
        assert 121*d <= 8*n
        count['minimum2_allocations'] += 1
    if g and min(map(len, g)) == max(map(len, g)) == 3:
        B = c-q+a+b2+b3+m+z0-u
        F = 3*u-2*c+s-3*(a+b2+b3)+3*q-2*m-3*z0
        assert B >= 2*d and F >= 0
        assert n == 2*J+4*Tp+2*K+5*B+2*F+2*b3+2*z0
        assert 24*d <= n
        count['cubic_allocations'] += 1
    count['allocations'] += 1
    count['with_claws'] += s > 0
    count['with_direct_centres'] += q > 0
    count['with_h2_helpers'] += b2 > 0
    count['with_h3_helpers'] += b3 > 0
    count['with_selected_edges'] += m > 0
    count['with_untouched_isolates'] += z0 > 0
    count['with_private_repairs'] += bool(deleted_a)
    count['with_helper_repairs'] += bool(deleted_i)
    count['private_repair_vertices'] += len(deleted_a)
    count['helper_repair_vertices'] += len(deleted_i)
    count['baseline_constructions'] += 1
    count['complementary_constructions'] += 2
    count['positive_gaps'] += d > 0
    return {'n': n, 'S': len(S), 'beta': beta, 'gap': d, 'parameters': v,
            'E': sorted(E), 'deleted_private': [sorted(x) for x in model['deleted_private']],
            'deleted_helpers': [sorted(x) for x in model['deleted_helpers']],
            'repaired_sizes': list(map(len, model['repaired']))}


def small():
    counts = Counter()
    for left, right in ((1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3), (3, 4)):
        possible = list(product(range(left), range(left, left+right)))
        for bits in range(1 << len(possible)):
            g = old.graph(left+right, [e for j, e in enumerate(possible) if bits >> j & 1])
            if max(map(len, g)) > 3:
                continue
            beta = exact(g)['beta']
            assert beta == old.beta_full_subsets(g)
            formed = cut.literals(g)
            for mask, ok in enumerate(formed):
                counts['selected_subsets'] += 1
                if not ok or any(formed[mask ^ (1 << j)] for j in range(len(g)) if mask >> j & 1):
                    continue
                S = {j for j in range(len(g)) if mask >> j & 1}
                if old.structure(g, S) is None:
                    continue
                counts['minimal_selected_sets'] += 1
                for allocation in cut.allocations(g, S):
                    check(g, S, beta, allocation, counts)
            counts['graphs'] += 1
    return dict(sorted(counts.items()))


def random_fixture(seed):
    rng = random.Random(seed)
    g, colours, S, W = [], {}, set(), set()
    helpers = {}
    def vertex(colour, selected=False):
        v = len(g);g.append(set());colours[v] = colour
        if selected:S.add(v)
        return v
    def edge(a, b):
        assert a != b and b not in g[a] and colours[a] != colours[b]
        g[a].add(b);g[b].add(a)
    def witness(owner, helper=False):
        v = vertex(1-colours[owner]);edge(v, owner);W.add(v)
        if helper:
            choices = [i for i in helpers if colours[i] != colours[v] and len(g[i]) < 3]
            i = rng.choice(choices) if choices and rng.randrange(3) else vertex(1-colours[v], True)
            helpers[i] = True;edge(i, v)
        return v
    for j in range(rng.randrange(2, 5)):
        kind = rng.choice(('clean', 'claw', 'direct'))
        c = vertex(rng.randrange(2), True)
        leaves = []
        for t in range(3 if kind == 'claw' else 2):
            ell = vertex(1-colours[c], True);edge(c, ell);leaves.append(ell)
            witness(ell, kind == 'direct' or (t > 0 and rng.randrange(2)))
        if kind == 'direct':witness(c, bool(rng.randrange(2)))
    for a in sorted(W):
        for b in sorted(W):
            if a < b and colours[a] != colours[b] and len(g[a]) < 3 and len(g[b]) < 3 and rng.randrange(4) == 0:
                edge(a, b)
    # Add a selected matching component and an untouched selected isolate.
    if seed % 3 == 0:
        a, b = vertex(0, True), vertex(1, True);edge(a, b)
    if seed % 5 == 0:vertex(0, True)
    assert all(literal(g, S, v) for v in range(len(g)) if v not in S)
    for v in S:
        near = {v} | g[v] | set().union(*(g[u] for u in g[v]))
        assert any(not literal(g, S-{v}, u) for u in near-(S-{v}))
    return g, S


def arithmetic():
    from fractions import Fraction as Q
    rows = []
    def identities(v, g):
        c,q,s,a,b2,b3,mu,m,z0,u = v
        n = 5*c+2*s+q+a+b2+b3+m+z0+u
        J = c+s+2*q-a-2*b2-3*b3;R = c-q+b2+b3-mu
        Tp = a+b2+b3-s-q;D = q+s+2*mu-2*b2;K = c+s+b2+b3
        assert 4*n == 9*J+2*R+13*Tp+D+9*K+2*s+7*b3+4*(m+z0+u)
        assert 8*n == 21*J+2*R+33*(Tp-g)+D+17*K+4*(2*u+g-a)+10*s+19*b3+8*(m+z0)+29*g
        B = c-q+a+b2+b3+m+z0-u;F = 3*u-2*c+s-3*(a+b2+b3)+3*q-2*m-3*z0
        assert n == 2*J+4*Tp+2*K+5*B+2*F+2*b3+2*z0
    for j in range(11):
        v = [0]*10
        if j < 10:v[j] = 1
        identities(v, int(j == 10))
    for exponent in (64,401):identities([10**exponent*(j+1)+7 for j in range(10)],10**exponent)
    # Exact feasible numerical ledger points; these do not assert graph realizations.
    for label,v,n in [('general',[Q(9,4),Q(1,2),0,Q(7,4),Q(3,4),0,Q(1,2),0,0,0],Q(57,4)),
                      ('minimum2',[Q(9,4),Q(1,2),0,Q(7,4),Q(3,4),0,Q(1,2),0,0,Q(7,8)],Q(121,8)),
                      ('cubic',[Q(9,4),0,Q(1,2),Q(9,4),Q(1,4),0,0,Q(13,4),0,6],Q(24))]:
        identities(v,0)
        c,q,s,a,b2,b3,mu,m,z0,u = v
        assert n == 5*c+2*s+q+a+b2+b3+m+z0+u
        assert c+s+2*q-a-2*b2-3*b3>=0 and c-q+b2+b3-mu>=2
        assert a+b2+b3-s-q>=2 and q+s+2*mu-2*b2>=0 and c+s+b2+b3>=3
        rows.append({'kind':label,'order_per_gap':str(n),'parameters':list(map(str,v)), 'graph_realization_claim':False})
    return {'basis_identity_controls':11,'large_integer_controls':2,'numerical_primal_points':rows}


def main():
    counts = Counter();targets = []
    for seed in range(80):
        g, S = random_fixture(20261112000+seed)
        beta = exact(g)['beta']
        allocations = list(cut.allocations(g, S))
        for allocation in allocations:
            targets.append(check(g, S, beta, allocation, counts))
    for label, builder in [('pendant48',core),('minimum2_64',base)]:
        g,S,D,col = builder(4);beta = exact(g)['beta']
        row = check(g,S,beta,next(cut.allocations(g,S)),counts);row['name']=label;targets.append(row)
    report = {'small_graphs':small(),'target_counts':dict(sorted(counts.items())),
              'targets':targets,'arithmetic':arithmetic(),
              'scope':'General proof establishes all three coefficients. Small graphs enumerate all minimal '
                       'eligible selections/allocations; targeted graphs independently optimize beta. Numerical '
                       'primal points certify only the stated ledger relaxation, not graph sharpness. No Lean or exact SF2 claim.'}
    out = ROOT/'output/subcubic-colour-exchange-check.json'
    out.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'result':'PASS','small_graphs':report['small_graphs'],'targets':report['target_counts'],
                      'report_bytes':out.stat().st_size}))


if __name__=='__main__':main()
