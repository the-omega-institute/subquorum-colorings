"""Physical sharp block and the odd-owner-path fixed-extraction refinement."""
from fractions import Fraction


def physical(model):
    b = model['b']; g = [set() for _ in range(5*b)]
    colour = [None] * len(g)
    def edge(a, c):
        g[a].add(c); g[c].add(a)
    for i, pair in enumerate(model['P']):
        assert model['index_colours'][pair[0]] == model['index_colours'][pair[1]]
        colour[i] = 1-model['index_colours'][pair[0]]
        for x in pair:
            edge(i, b+x); edge(b+x, 3*b+x)
    for x in range(2*b):
        colour[b+x] = model['index_colours'][x]
        colour[3*b+x] = 1-colour[b+x]
    for a, c in model['Q']: edge(b+a, b+c)
    for a, c in model['B']: edge(3*b+a, 3*b+c)
    assert all(colour[a] != colour[c] for a, row in enumerate(g) for c in row)
    return g, colour


def odd_path_ledger(n, a, p, u, R_size, b, b3, S_size, beta, L,
                    odd_paths, gamma):
    """Exact rational identity, under the actual K4-free extraction hypotheses.

    The calling proof/certificate supplies compatibility and the odd-path count;
    this function checks the numerical hypotheses and returns every ledger term.
    It is not a decision procedure for an arbitrary graph's applicability.
    """
    gamma = Fraction(gamma); bp = b-b3; d = S_size-beta
    minimum = min(a, p); al, pi = a-minimum, p-minimum
    e, r = u-a-2*b, R_size-a-b
    q, tau = n-S_size-p-u, minimum+b-2*d
    Z = 3*beta-3*L-8*bp
    assert 0 <= gamma <= 1 and 0 <= odd_paths <= 2*bp
    assert odd_paths % 2 == 0 and odd_paths >= 2*gamma*bp
    assert Z >= Fraction(odd_paths, 2)
    assert all(t >= 0 for t in (r, q, al, pi, tau, b3, e-b3))
    assert bp == 2*d-minimum+tau-b3
    assert n == 10*d+minimum+r+3*(al+pi)+2*e+q+5*tau
    terms = [Z-gamma*bp, (5+gamma)*(r+q), (12+3*gamma)*(al+pi),
             (7+2*gamma)*(e-b3), (2+gamma)*b3, (24+6*gamma)*tau]
    lhs = (5+gamma)*n-(51+12*gamma)*d
    assert all(t >= 0 for t in terms) and sum(terms) == lhs
    return {'gamma': str(gamma), 'odd_paths': odd_paths, 'bprime': bp,
            'Z': Z, 'terms': [str(t) for t in terms], 'lhs': str(lhs),
            'gap_upper': ((5+gamma)*n/(51+12*gamma)).__floor__()}
