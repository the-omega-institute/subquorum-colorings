"""Shared class margins and physical boundary repair for the 31/314 bound."""
from collections import Counter
from fractions import Fraction
from subcubic_partial_template import decompose, layers, one_side
from subcubic_phase_pairing import pairing_data, expectation
from subcubic_phase_slack import owner_slack
from subcubic_zero_budget_repair import components, restriction
from subcubic_intrinsic_obstruction import path_cycle_optimum


def resources(m):
    data = pairing_data(m)
    slack = owner_slack(m, data)
    inverse = {c: x for x, c in m['owner'].items()}
    events, bad, counts, flags, good = [], [], Counter(), Counter(), []

    def literal(v):
        x = inverse[v]
        return m['group'][x], 1-m['colour'][x]

    for K in components(m['g'], m['C']):
        ends = sorted(v for v in K if len(m['g'][v] & K) <= 1)
        if not ends:
            continue
        order, previous, current = [], None, ends[0]
        while current is not None:
            order.append(current)
            nxt = sorted((m['g'][current] & K)-({previous} if previous is not None else set()))
            previous, current = current, nxt[0] if nxt else None
        assert set(order) == K
        run = 1
        while run < len(order) and literal(order[run]) == literal(order[0]):
            run += 1
        if run >= 3:
            j, bit = literal(order[0]); key = j, 1-bit
            triple = set(order[:3]); counts[key] += 1
            bad.append(dict(K=K, triple=triple, key=key))
            continue
        prefix = set(order[:run]); requirements = dict([literal(order[0])])
        boundary = order[run] if run < len(order) else None
        if boundary is not None:
            j, bit = literal(boundary)
            assert j not in requirements or requirements[j] == 1-bit
            requirements[j] = 1-bit
        delta = Fraction((3-(2*run)%3)%3, 3)
        assert delta/Fraction(2**len(requirements)) >= Fraction(1, 12)
        events.append(dict(K=K, prefix=prefix, boundary=boundary,
                           requirements=requirements, delta=delta))

    sg = sb = bG = 0
    for j, (order, cyclic) in enumerate(zip(m['components'], m['cyclic'])):
        if data['classes'][j, 0]['distinguished']:
            continue
        keys = [(j, bit) for bit in (0, 1)]
        failing = [key for key in keys if data['classes'][key].get('non_square_mono', False)
                   or data['classes'][key]['remaining']]
        if not failing:
            sub = restriction(m, set(order)); b = len(sub['I'])
            assert b % 4 == 0
            assert all(m['g'][v] & m['C'] <= sub['C'] for v in sub['C'])
            good.append(dict(j=j, X=set(order), model=sub, b=b))
            bG += b
            sg += not cyclic
        elif not cyclic:
            flags[failing[0]] += 1; sb += 1
    assert 4*sg <= bG
    used = set(); rows = []
    for row in bad:
        assert not used & row['triple']; used |= row['triple']
    for key, c in data['classes'].items():
        p, f = counts[key], flags[key]
        M = c['budget']-c['loss']
        triples = set().union(*(r['triple'] for r in bad if r['key'] == key))
        mixed = set().union(*(s for s, _ in c['mixed']))
        assert len(triples) == 3*p and triples <= c['remaining']
        assert not triples & (mixed | c['monochromatic'])
        assert f in (0, 1)
        if c['distinguished']:
            assert f == 0 and p <= 6*M
        else:
            assert M >= Fraction(p, 4)
            if f:
                assert M >= Fraction(1, 12)
            assert 2*p+2*f <= 24*M
        rows.append(dict(key=key, margin=M, p=p, f=f,
                         distinguished=c['distinguished'], triple_vertices=triples))
    tg, tb = len(events), len(bad)
    assert 2*tb+2*sb <= 24*slack['sigma']
    return dict(pairing=data, slack=slack, sigma=slack['sigma'], classes=rows,
                events=events, bad_paths=bad, good_components=good,
                tg=tg, tb=tb, sg=sg, sb=sb, bG=bG)


def template_certificate(m):
    res = resources(m); replaced = set(); goodX = set()
    for row in res['good_components']:
        sub = row['model']
        alternatives = [one_side(sub, bit)[0] for bit in (0, 1)]
        best = max(alternatives, key=lambda d: (len(d), sorted(d)))
        assert 4*len(best) >= 11*row['b']
        replaced |= best; goodX |= row['X']
    rem = restriction(m, m['X']-goodX)
    rres = resources(rem); assert rres['sigma'] == res['sigma']
    assert rres['tg'] == res['tg'] and not rres['good_components']
    pairing = rres['pairing']
    terms = pairing['terms']+[(r['delta'], r['requirements']) for r in rres['events']]
    initial = expectation(terms, {})
    assert initial >= -pairing['rho']+Fraction(res['tg'], 12)
    fixed, steps = {}, [initial]
    for j in range(len(rem['components'])):
        values = [expectation(terms, fixed | {j: bit}) for bit in (0, 1)]
        fixed[j] = int(values[1] > values[0]); steps.append(max(values))
        assert steps[-1] >= steps[-2]
    Y = {x for x in rem['X'] if rem['colour'][x] == fixed[rem['group'][x]]}
    A = rem['C']-{rem['owner'][x] for x in Y}
    core = path_cycle_optimum(m['g'], A)
    assert Fraction(len(core))-Fraction(2*len(rem['I']), 3) >= steps[-1]
    repaired = replaced | rem['I'] | Y | core
    b, o, sigma = len(m['I']), res['pairing']['odd'], res['sigma']
    assert len(repaired) >= Fraction(5*b, 2)+Fraction(o, 3)+sigma+Fraction(res['bG'], 4)+Fraction(res['tg'], 12)
    first, second = [one_side(m, bit)[0] for bit in (0, 1)]
    assert max(len(first), len(second)) >= Fraction(11*b, 4)-Fraction(o, 2)
    best = max((first, second, repaired), key=lambda d: (len(d), sorted(d)))
    assert 5*len(best) >= 13*b+3*sigma+Fraction(3*res['bG']+res['tg'], 4)
    return best, dict(resources=res, remainder=rem, remainder_resources=rres,
                      terms=terms, initial=initial, phases=fixed, steps=steps,
                      A=A, core=core, alternatives=(first, second, repaired))


def full_certificate(g, S, colour, beta):
    w = decompose(g, S)
    m = layers(g, w['C0'], w['I0'], w['X0'], w['owner'], w['centre'], colour)
    inner, template = template_certificate(m)
    res = template['resources']; sigma = res['sigma']
    retained = (w['R']-w['I0']) | {ell for c, ell, x in w['triples']}
    lifted = inner | retained
    H = m['I'] | m['C'] | m['X']; exterior = set(range(len(g)))-H
    boundary = {tuple(sorted((v, u))) for v in H for u in g[v]-H}
    by_layer = {name: sum(len(g[v]-H) for v in m[name]) for name in ('I', 'C', 'X')}
    p, u, a, b, b3 = len(w['triples']), len(w['pairs']), w['a'], w['b'], w['b3']
    minimum = min(a, p); alpha, pi = a-minimum, p-minimum
    e, r = u-a-2*b, len(w['R'])-a-b
    q = len(g)-len(S)-p-u; d = len(S)-beta; tau = minimum+b-2*d
    bp = len(m['I']); Z = 5*beta-5*len(retained)-13*bp
    assert bp == b-b3 and e >= b3
    assert all(v >= 0 for v in (alpha, pi, e, r, q, tau, Z))
    assert Z >= 3*sigma+Fraction(3*res['bG']+res['tg'], 4)
    assert by_layer['C'] <= 2*(res['tg']+res['tb'])
    assert by_layer['X'] <= 2*(res['sg']+res['sb'])
    assert by_layer['I'] <= 3*q
    B = len(boundary)
    assert B == sum(by_layer.values())
    forbidden = set().union(*(g[v] & exterior for v in inner))
    outer = [{v for v in exterior-forbidden if colour[v] == bit} for bit in (0, 1)]
    assert sum(map(len, outer)) >= len(exterior)-B
    externals = tuple(inner | part for part in outer)
    assert beta >= max(map(len, externals))
    assert beta >= Fraction(len(g), 2)+Fraction(bp, 10)+3*sigma/5-Fraction(19*res['tg']+2*res['bG'], 20)-res['tb']-res['sb']-Fraction(3*q, 2)
    assert 2*beta-len(g)-Fraction(bp, 5) == -2*minimum-alpha-pi+r-2*e-3*b3-q+Fraction(2*Z, 5)
    W = r+2*q+8*Z-(2*minimum+alpha+pi+2*e+3*b3)
    assert W >= 0
    terms = [W, 61*r, 147*(alpha+pi), 86*(e-b3), 25*b3, 60*q, 294*tau]
    assert all(v >= 0 for v in terms)
    assert sum(terms) == 62*len(g)-628*d
    assert 314*d <= 31*len(g)
    best = max((lifted, *externals), key=lambda t: (len(t), sorted(t)))
    return best, dict(witnesses=w, template=m, template_data=template,
        inner=inner, retained=retained, alternatives=(lifted, *externals),
        boundary=boundary, boundary_by_layer=by_layer, nonnegative_terms=terms,
        counts=dict(p=p, u=u, a=a, b=b, b3=b3, m=minimum, alpha=alpha, pi=pi,
                    e=e, r=r, q=q, d=d, tau=tau, Z=Z, W=W))
