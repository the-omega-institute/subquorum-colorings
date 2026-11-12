"""Distinct low-degree and isolated-cycle credits for partial templates."""
from fractions import Fraction
from itertools import product

from subcubic_intrinsic_obstruction import path_cycle_optimum
from subcubic_partial_template import decompose, layers, one_side


def credit_classes(m):
    """An odd quotient cycle has two owner classes of order 2 mod 4."""
    broken, intact = [], []
    odd = 0
    for group, (order, cyclic) in enumerate(zip(m['components'], m['cyclic'])):
        if not cyclic or (len(order)//4) % 2 == 0:
            continue
        odd += 1
        for bit in (0, 1):
            U = {m['owner'][x] for x in order if m['colour'][x] == bit}
            bad = {v for v in U if len(m['g'][v] & U) < 2}
            assert len(U) % 4 == 2
            if bad:
                assert len(bad) >= 2
                broken.append(dict(group=group, bit=bit, U=U, bad=bad))
            else:
                intact.append(dict(group=group, bit=bit, U=U))
    return dict(odd=odd, broken=broken, intact=intact)


def expectation(m, credits, fixed):
    """Exact local expectation; a vertex event uses at most three bits."""
    inverse = {c: x for x, c in m['owner'].items()}
    score = Fraction(0)
    for row in credits['broken']:
        for v in sorted(row['bad']):
            ns = m['g'][v] & m['C']
            involved = {m['group'][inverse[u]] for u in ns | {v}}
            free = sorted(involved - fixed.keys())
            favorable = 0
            for bits in product((0, 1), repeat=len(free)):
                phase = fixed | dict(zip(free, bits))

                def present(u):
                    x = inverse[u]
                    return m['colour'][x] != phase[m['group'][x]]

                favorable += present(v) and sum(present(u) for u in ns) <= 1
            score += Fraction(favorable, 4*2**len(free))
    for row in credits['intact']:
        score += (Fraction(int(fixed[row['group']] != row['bit']))
                  if row['group'] in fixed else Fraction(1, 2))
    return score


def phase_certificate(m):
    credits = credit_classes(m)
    fixed = {}
    initial = expectation(m, credits, fixed)
    assert 4*initial >= credits['odd']
    steps = [initial]
    for j in range(len(m['components'])):
        a, b = (expectation(m, credits, fixed | {j: bit}) for bit in (0, 1))
        fixed[j] = int(b > a)
        steps.append(max(a, b))
        assert steps[-1] >= steps[-2]
    Y = {x for x in m['X'] if m['colour'][x] == fixed[m['group'][x]]}
    R = m['C'] - {m['owner'][x] for x in Y}
    Z = path_cycle_optimum(m['g'], R)
    assert Fraction(len(Z))-Fraction(len(R), 2) >= steps[-1]
    return m['I'] | Y | Z, dict(credits=credits, initial=initial,
            steps=steps, phases=fixed, Y=Y, R=R, Z=Z, score=steps[-1])


def template_certificates(m):
    first, da = one_side(m, 0)
    second, db = one_side(m, 1)
    phased, phase = phase_certificate(m)
    b, odd = len(m['I']), phase['credits']['odd']
    assert len(first)+len(second) == 5*b+da+db
    assert 2*(da+db) >= b-2*odd
    assert 4*len(phased) >= 10*b+odd
    D = max((first, second, phased), key=lambda d: (len(d), sorted(d)))
    assert 12*len(D) >= 31*b
    return D, dict(b=b, odd=odd, da=da, db=db, phase=phase,
                   alternatives=(first, second, phased))


def full_certificate(g, S, graph_colour, beta):
    w = decompose(g, S)
    m = layers(g, w['C0'], w['I0'], w['X0'], w['owner'],
               w['centre'], graph_colour)
    inner, certificates = template_certificates(m)
    leaves = {ell for c, ell, x in w['triples']}
    retained = (w['R']-w['I0']) | leaves
    D = inner | retained
    p, u, a, b, b3 = len(w['triples']), len(w['pairs']), w['a'], w['b'], w['b3']
    minimum = min(a, p)
    e, r = u-a-2*b, len(w['R'])-a-b
    q = len(g)-len(S)-p-u
    d = len(S)-beta
    tau, alpha, pi = minimum+b-2*d, a-minimum, p-minimum
    Z = 12*beta-12*(len(w['R'])-len(w['I0'])+p)-31*len(w['I0'])
    terms = [Z, 19*r, 45*alpha, 45*pi, 7*e, 19*(e-b3), 19*q, 90*tau]
    assert all(t >= 0 for t in terms)
    assert sum(terms) == 19*len(g)-192*d
    return D, dict(witnesses=w, template=m, inner=inner, retained=retained,
                   alternatives=certificates['alternatives'], template_ledger=certificates,
                   counts=dict(p=p, u=u, a=a, b=b, b3=b3, m=minimum, e=e,
                               r=r, q=q, tau=tau, alpha=alpha, pi=pi, Z=Z, d=d),
                   nonnegative_terms=terms)
