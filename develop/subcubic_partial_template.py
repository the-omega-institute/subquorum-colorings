"""Partial-template certificates and extraction from any minimal forming set."""
from subcubic_intrinsic_obstruction import phase_certificate


def layers(g, C, I, X, owner, centre, graph_colour):
    C, I, X = set(C), set(I), set(X)
    pair = {}
    for i in I:
        a, b = sorted(g[i] & X)
        pair[a], pair[b] = b, a
    q = {x: next(iter(g[x] & X)) for x in X if g[x] & X}
    aux = {x: {pair[x]} | ({q[x]} if x in q else set()) for x in X}
    components, cyclic, group, colour = [], [], {}, {}
    unseen = set(X)
    while unseen:
        found, todo = {min(unseen)}, [min(unseen)]
        while todo:
            for w in aux[todo.pop()]-found:
                found.add(w)
                todo.append(w)
        endpoints = sorted(v for v in found if len(aux[v]) == 1)
        current, previous, order = (endpoints[0] if endpoints else min(found)), None, []
        while current not in order:
            order.append(current)
            group[current], colour[current] = len(components), (len(order)-1) % 2
            nxt = sorted(aux[current]-({previous} if previous is not None else set()))
            if not nxt:
                break
            previous, current = current, nxt[0]
        assert set(order) == found and len(order) % 2 == 0
        assert endpoints or len(order) % 4 == 0
        components.append(order)
        cyclic.append(not endpoints)
        unseen -= found
    return dict(g=g, C=C, I=I, X=X, owner=owner, centre=centre, pair=pair,
                q=q, components=components, cyclic=cyclic, group=group,
                colour=colour, graph_colour=graph_colour)


def one_side(m, side):
    J, gain = set(), 0
    for order, cyclic in zip(m['components'], m['cyclic']):
        pairs = list(dict.fromkeys(m['centre'][x] for x in order
                                   if m['graph_colour'][x] != side))
        stop = 2*(len(pairs)//2) if cyclic else len(pairs)
        chosen = pairs[:stop:2]
        gain += len(chosen)
        J.update(chosen)
    T = {x for x in m['X'] if m['centre'][x] in J}
    forbidden = {m['q'][x] for x in T if x in m['q']}
    D = {c for c in m['C'] if m['graph_colour'][c] == side} | T
    D.update(i for i in m['I'] if m['graph_colour'][i] == side and i not in J)
    for i in sorted(m['I']):
        if m['graph_colour'][i] == side:
            continue
        D.add(i)
        available = (m['g'][i] & m['X']) - forbidden
        if available:
            D.add(min(available))
    return D, gain


def template_certificates(m):
    first, da = one_side(m, 0)
    second, db = one_side(m, 1)
    phased, phase = phase_certificate(m)
    b = len(m['I'])
    b0 = sum(len(c)//2 for c in m['components'] if len(c) == 4)
    assert 3*(da+db) >= b-b0
    assert 2*phase['initial'] >= b0
    assert 4*len(phase['Z']) >= 2*b+phase['L']
    assert len(first)+len(second) == 5*b+da+db
    D = max((first, second, phased), key=lambda d: (len(d), sorted(d)))
    assert 7*len(D) >= 18*b
    return D, dict(da=da, db=db, b=b, b0=b0, phase=phase,
                   alternatives=(first, second, phased))


def decompose(g, S):
    S = set(S)
    outside = set(range(len(g)))-S
    I = {v for v in S if not g[v] & S}
    R = I | {v for v in S if len(g[v] & S) == 1
             and len(g[next(iter(g[v] & S))] & S) == 1}
    C = S-R
    triples = []
    for c in sorted(C):
        options = [(ell, x) for ell in sorted(g[c] & C) if g[ell] & S == {c}
                   for x in sorted(outside) if g[x] & S == {ell}]
        if options:
            ell, x = options[0]
            triples.append((c, ell, x))
    used = {v for triple in triples for v in triple}
    assert len(used) == 3*len(triples)
    pairs = []
    for v in sorted(C-used):
        options = [x for x in sorted(outside) if v in g[x] & S
                   and len((g[x] & S)-{v}) <= 1 and (g[x] & S)-{v} <= I]
        assert options, (v, S, g)
        pairs.append((v, options[0]))
    assert len({x for _, x in pairs}) == len(pairs)
    assert not {x for _, x in pairs} & used
    h = {i: sum(i in g[x] for _, x in pairs) for i in I}
    a = sum(t == 1 for t in h.values())
    b = sum(t >= 2 for t in h.values())
    b3 = sum(t == 3 for t in h.values())
    I0 = {i for i in I if h[i] == 2}
    good = [(v, x) for v, x in pairs if g[x] & I0]
    C0, X0 = {v for v, _ in good}, {x for _, x in good}
    owner = {x: v for v, x in good}
    centre = {x: next(iter(g[x] & I0)) for x in X0}
    return dict(R=R, I=I, triples=triples, pairs=pairs, h=h, a=a, b=b,
                b3=b3, C0=C0, X0=X0, I0=I0, owner=owner, centre=centre)


def full_certificate(g, S, graph_colour, beta):
    w = decompose(g, S)
    m = layers(g, w['C0'], w['I0'], w['X0'], w['owner'], w['centre'], graph_colour)
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
    Z = 7*beta-7*(len(w['R'])-len(w['I0'])+p)-18*len(w['I0'])
    terms = [Z, 11*r, 26*alpha, 26*pi, 4*e, 11*(e-b3), 11*q, 52*tau]
    assert all(t >= 0 for t in terms)
    assert sum(terms) == 11*len(g)-111*d
    return D, dict(witnesses=w, template=m, inner=inner, retained=retained,
                   alternatives=certificates['alternatives'], template_ledger=certificates,
                   counts=dict(p=p, u=u, a=a, b=b, b3=b3, m=minimum, e=e,
                               r=r, q=q, tau=tau, alpha=alpha, pi=pi, Z=Z, d=d),
                   nonnegative_terms=terms)
