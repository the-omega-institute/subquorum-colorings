"""Nonnegative vertex penalties and a boundary-aware subcubic certificate."""
from fractions import Fraction
from subcubic_two_endpoint import resources, full_certificate as preceding_certificate
from subcubic_phase_pairing import expectation
from subcubic_partial_template import one_side
from subcubic_intrinsic_obstruction import path_cycle_optimum


def potential(D, costs):
    return len(D)-sum((costs[v] for v in D), Fraction(0))


def weighted_phase(m, costs):
    H = m['I'] | m['C'] | m['X']
    assert set(costs) == H and all(v >= 0 for v in costs.values())
    res = resources(m)
    terms = list(res['pairing']['terms'])
    terms += [(row['delta'], row['requirements']) for row in res['events']]
    for x, c in sorted(m['owner'].items()):
        j, bit = m['group'][x], m['colour'][x]
        terms += [(-costs[x], {j: bit}), (-costs[c], {j: 1-bit})]
    initial = expectation(terms, {})
    bound = (-res['pairing']['rho']+Fraction(res['tg'], 6)
             -sum((costs[v] for v in m['C'] | m['X']), Fraction(0))/2)
    assert initial >= bound
    fixed, steps = {}, [initial]
    for j in range(len(m['components'])):
        values = [expectation(terms, fixed | {j: bit}) for bit in (0, 1)]
        fixed[j] = int(values[1] > values[0])
        steps.append(max(values))
        assert steps[-1] >= steps[-2]
    Y = {x for x in m['X'] if m['colour'][x] == fixed[m['group'][x]]}
    A = m['C']-{m['owner'][x] for x in Y}
    core = path_cycle_optimum(m['g'], A)
    D = m['I'] | Y | core
    b = len(m['I'])
    costs_I = sum((costs[v] for v in m['I']), Fraction(0))
    assert len(Y) == len(A) == b
    assert potential(D, costs) >= Fraction(8*b, 3)-costs_I+steps[-1]
    guarantee = (Fraction(5*b, 2)+Fraction(res['pairing']['odd'], 3)
                 +res['sigma']+Fraction(res['tg'], 6)-costs_I
                 -sum((costs[v] for v in m['C'] | m['X']), Fraction(0))/2)
    assert potential(D, costs) >= guarantee
    return D, dict(resources=res, terms=terms, initial=initial, phases=fixed,
                   steps=steps, retained=A, witnesses=Y, core=core,
                   phase_guarantee=guarantee)


def weighted_template(m, costs):
    phased, data = weighted_phase(m, costs)
    sides = tuple(one_side(m, bit)[0] for bit in (0, 1))
    b = len(m['I']); res = data['resources']
    total = {k: sum((costs[v] for v in m[k]), Fraction(0)) for k in ('I', 'C', 'X')}
    assert len(sides[0])+len(sides[1]) >= Fraction(11*b, 2)-res['pairing']['odd']
    assert all(sum(v in D for D in sides) == 1 for v in m['C'])
    one_side_guarantee = (Fraction(11*b, 4)-Fraction(res['pairing']['odd'], 2)
                          -total['I']-total['C']/2-total['X'])
    assert sum(potential(D, costs) for D in sides)/2 >= one_side_guarantee
    best = max((phased, *sides), key=lambda D: (potential(D, costs), len(D), sorted(D)))
    guarantee = (Fraction(13*b, 5)+3*res['sigma']/5+Fraction(res['tg'], 10)
                 -total['I']-total['C']/2-7*total['X']/10)
    assert guarantee == 3*data['phase_guarantee']/5+2*one_side_guarantee/5
    assert potential(best, costs) >= guarantee
    return best, dict(**data, alternatives=(phased, *sides), guarantee=guarantee,
                      one_side_guarantee=one_side_guarantee, layer_costs=total)


def full_certificate(g, S, colour, beta):
    old, preceding = preceding_certificate(g, S, colour, beta)
    m = preceding['template']; H = m['I'] | m['C'] | m['X']
    exterior = set(range(len(g)))-H
    costs = {v: Fraction(len(g[v] & exterior), 2) for v in H}
    inner, weighted = weighted_template(m, costs)
    forbidden = set().union(*(g[v] & exterior for v in inner))
    outer = tuple({v for v in exterior-forbidden if colour[v] == bit} for bit in (0, 1))
    extended = tuple(inner | side for side in outer)
    assert max(map(len, extended)) >= Fraction(len(g)-len(H), 2)+potential(inner, costs)
    r = weighted['resources']; c = preceding['counts']; bp = len(m['I'])
    exterior_bound = (Fraction(len(g), 2)+Fraction(bp, 10)+3*r['sigma']/5
                      -Fraction(2*r['tg'], 5)-Fraction(r['tb'], 2)
                      -Fraction(7*(r['sg']+r['sb']), 10)-Fraction(3*c['q'], 2))
    assert beta >= max(map(len, extended)) >= exterior_bound
    T = 2*c['m']+c['alpha']+c['pi']+2*c['e']+3*c['b3']
    W = 5*c['r']+10*c['q']+14*c['Z']-5*T
    assert W >= 0
    terms = [W, 97*c['r'], 241*(c['alpha']+c['pi']),
             144*(c['e']-c['b3']), 47*c['b3'], 92*c['q'], 482*c['tau']]
    assert all(x >= 0 for x in terms)
    assert sum(terms) == 102*len(g)-1034*(len(S)-beta)
    assert 517*(len(S)-beta) <= 51*len(g)
    best = max((old, *extended), key=lambda D: (len(D), sorted(D)))
    return best, dict(preceding=preceding, weighted=weighted, costs=costs,
                      inner=inner, exterior_alternatives=extended,
                      alternatives=(old, *extended), W=W,
                      nonnegative_terms=terms, exterior_bound=exterior_bound)
