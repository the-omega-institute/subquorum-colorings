"""Balanced physical-side construction and a boundary-aware7/71 certificate."""
from fractions import Fraction
from subcubic_boundary_expectation import weighted_phase, potential, full_certificate as preceding_certificate


def side_options(m, side, order, cyclic, costs):
    helpers = list(dict.fromkeys(m['centre'][x] for x in order))
    eligible = [i for i in helpers if m['graph_colour'][i] == side]
    k = len(eligible)
    if cyclic:
        supports = [{eligible[(start+2*j) % k] for j in range(k//2)} for start in range(k)]
    else:
        supports = [set(eligible[parity::2]) for parity in (0, 1)]
    if not supports: supports = [set()]
    owners = {m['owner'][x] for x in order if m['graph_colour'][m['owner'][x]] == side}
    options = []
    for J in supports:
        doubles = {x for x in order if m['centre'][x] in J}
        forbidden = {m['q'][x] for x in doubles if x in m['q']}
        D = owners | doubles | (set(helpers)-J)
        for i in helpers:
            if m['graph_colour'][i] == side: continue
            available = (m['g'][i] & m['X'])-forbidden
            assert available
            D.add(min(available, key=lambda v: (costs[v], v)))
        assert all(len(m['g'][v] & D) <= 1 for v in D)
        options.append((D, J))
    return options


def balanced_sides(m, costs):
    sides, choices = [], []
    for side in (0, 1):
        D, chosen = set(), []
        for order, cyclic in zip(m['components'], m['cyclic']):
            options = side_options(m, side, order, cyclic, costs)
            best, J = max(options, key=lambda row: (potential(row[0], costs), len(row[0]), sorted(row[0])))
            D.update(best); chosen.append(J)
        assert all(len(m['g'][v] & D) <= 1 for v in D)
        sides.append(D); choices.append(chosen)
    return tuple(sides), choices


def weighted_template(m, costs):
    phased, data = weighted_phase(m, costs)
    sides, choices = balanced_sides(m, costs)
    b = len(m['I']); res = data['resources']
    total = {k: sum((costs[v] for v in m[k]), Fraction(0)) for k in ('I', 'C', 'X')}
    one_side_guarantee = (Fraction(11*b, 4)-Fraction(res['pairing']['odd'], 2)
                          -total['I']-(total['C']+total['X'])/2)
    assert sum(potential(D, costs) for D in sides)/2 >= one_side_guarantee
    best = max((phased, *sides), key=lambda D: (potential(D, costs), len(D), sorted(D)))
    guarantee = (Fraction(13*b, 5)+3*res['sigma']/5+Fraction(res['tg'], 10)
                 -total['I']-(total['C']+total['X'])/2)
    assert guarantee == 3*data['phase_guarantee']/5+2*one_side_guarantee/5
    assert potential(best, costs) >= guarantee
    return best, dict(**data, alternatives=(phased, *sides), guarantee=guarantee,
                      one_side_guarantee=one_side_guarantee, layer_costs=total,
                      side_choices=choices)


def full_certificate(g, S, colour, beta):
    old, previous = preceding_certificate(g, S, colour, beta)
    base = previous['preceding']; m = base['template']; H = m['I'] | m['C'] | m['X']
    exterior = set(range(len(g)))-H
    costs = {v: Fraction(len(g[v] & exterior), 2) for v in H}
    inner, weighted = weighted_template(m, costs)
    forbidden = set().union(*(g[v] & exterior for v in inner))
    outer = tuple({v for v in exterior-forbidden if colour[v] == bit} for bit in (0, 1))
    extended = tuple(inner | side for side in outer)
    assert max(map(len, extended)) >= Fraction(len(g)-len(H), 2)+potential(inner, costs)
    r = weighted['resources']; c = base['counts']; bp = len(m['I'])
    exterior_bound = (Fraction(len(g), 2)+Fraction(bp, 10)+3*r['sigma']/5
                      -Fraction(2*r['tg'], 5)-Fraction(r['tb'], 2)
                      -Fraction(r['sg']+r['sb'], 2)-Fraction(3*c['q'], 2))
    assert beta >= max(map(len, extended)) >= exterior_bound
    T = 2*c['m']+c['alpha']+c['pi']+2*c['e']+3*c['b3']
    W = c['r']+2*c['q']+2*c['Z']-T
    assert W >= 0
    terms = [W, 13*c['r'], 33*(c['alpha']+c['pi']),
             20*(c['e']-c['b3']), 7*c['b3'], 12*c['q'], 66*c['tau']]
    assert all(x >= 0 for x in terms)
    assert sum(terms) == 14*len(g)-142*(len(S)-beta)
    assert 71*(len(S)-beta) <= 7*len(g)
    best = max((old, *extended), key=lambda D: (len(D), sorted(D)))
    return best, dict(preceding=base, previous=previous, weighted=weighted, costs=costs,
                      inner=inner, exterior_alternatives=extended,
                      alternatives=(old, *extended), W=W,
                      nonnegative_terms=terms, exterior_bound=exterior_bound)
