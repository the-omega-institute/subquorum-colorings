"""Compatible certificates when the owner core has components P1, P2 or C4."""


def components(g, vertices):
    remaining = set(vertices)
    result = []
    while remaining:
        start = min(remaining)
        seen, stack = {start}, [start]
        while stack:
            v = stack.pop()
            for u in g[v] & remaining - seen:
                seen.add(u)
                stack.append(u)
        remaining -= seen
        result.append(seen)
    return result


def square_components(m):
    result = []
    for block in components(m['g'], m['C']):
        if len(block) <= 2:
            continue
        if len(block) != 4 or any(len(m['g'][v] & block) != 2 for v in block):
            raise ValueError('Owner core must have only P1, P2 and C4 components')
        result.append(block)
    return result


def independent_certificate(graph):
    """Maximal independent set with no improving one-for-two exchange."""
    vertices = set(graph)
    if any(v in graph[v] or len(graph[v]) > 3 or
           any(u not in graph or v not in graph[u] for u in graph[v])
           for v in graph):
        raise ValueError('Use a simple undirected graph of maximum degree three')
    if any(graph[v] & graph[u] for v in graph for u in graph[v]):
        raise ValueError('Use a triangle-free graph')
    chosen, exchanges = set(), []
    while True:
        for v in sorted(vertices - chosen):
            if not graph[v] & chosen:
                chosen.add(v)
        private = {v: [] for v in chosen}
        for v in sorted(vertices - chosen):
            ns = graph[v] & chosen
            assert ns
            if len(ns) == 1:
                private[next(iter(ns))].append(v)
        candidates = [v for v in sorted(chosen) if len(private[v]) >= 2]
        if not candidates:
            break
        v = candidates[0]
        a, b = private[v][:2]
        assert b not in graph[a]
        chosen.remove(v)
        chosen.update((a, b))
        exchanges.append((v, a, b))
    outside = vertices - chosen
    b1 = sum(len(graph[v] & chosen) == 1 for v in outside)
    crossing = sum(len(graph[v] & chosen) for v in outside)
    assert b1 <= len(chosen) and 2*len(outside) <= crossing+b1 <= 4*len(chosen)
    assert 3*len(chosen) >= len(vertices)
    return chosen, dict(exchanges=exchanges, private_count=b1, crossing=crossing)


def template_certificate(m):
    g, C, X, I = (m[k] for k in ('g', 'C', 'X', 'I'))
    squares = square_components(m)
    inverse = {c: x for x, c in m['owner'].items()}
    square_owners = set().union(*squares) if squares else set()
    vertices = {inverse[c] for c in square_owners}
    graph = {x: set(g[x] & X & vertices) for x in vertices}
    for i in I:
        pair = sorted(g[i] & X & vertices)
        if len(pair) == 2:
            a, b = pair
            graph[a].add(b); graph[b].add(a)
    pairs = []
    for square in squares:
        for side in (0, 1):
            a, b = sorted(c for c in square if m['graph_colour'][c] == side)
            x, y = inverse[a], inverse[b]
            pairs.append((x, y))
            graph[x].add(y); graph[y].add(x)
    chosen, independent = independent_certificate(graph)
    deleted = {m['owner'][x] for x in chosen}
    for x, y in pairs:
        if x not in chosen and y not in chosen:
            deleted.add(m['owner'][min(x, y)])
    assert len(deleted) == 2*len(squares)
    D = set(I) | (C-deleted) | chosen
    assert all(len(g[v] & D) <= 1 for v in D)
    b, t = len(I), len(squares)
    assert len(C) == len(X) == 2*b and 2*t <= b
    assert len(D) >= 3*b-(2*t)//3
    return D, dict(square_count=t, auxiliary=graph, chosen=chosen, deleted=deleted,
                   independent=independent, guarantee=3*b-(2*t)//3,
                   structural_surplus=b-2*t+((-4*t) % 3))


def lift_certificate(g, S, colour, witnesses, beta):
    """Use an existing fixed disjoint witness extraction; beta is a supplied bound."""
    w = witnesses
    m = dict(g=g, C=w['C0'], I=w['I0'], X=w['X0'],
             owner=w['owner'], graph_colour=colour)
    inner, data = template_certificate(m)
    retained = (w['R']-w['I0']) | {ell for c, ell, x in w['triples']}
    assert not retained & inner
    assert all(not (g[v] & inner) for v in retained)
    D = inner | retained
    assert all(len(g[v] & D) <= 1 for v in D) and len(D) <= beta
    p, u = len(w['triples']), len(w['pairs'])
    a, b, b3 = w['a'], w['b'], w['b3']
    minimum = min(a, p)
    alpha, pi = a-minimum, p-minimum
    e, r = u-a-2*b, len(w['R'])-a-b
    q, d = len(g)-len(S)-p-u, len(S)-beta
    tau = minimum+b-2*d
    L, bp = len(retained), len(w['I0'])
    Z = 3*beta-3*L-8*bp
    terms = [Z, 5*r, 12*(alpha+pi), 24*tau, 7*(e-b3), 2*b3, 5*q]
    assert all(t >= 0 for t in terms)
    assert Z >= data['structural_surplus']
    assert sum(terms) == 5*len(g)-51*d
    return D, dict(template=data, inner=inner, retained=retained, nonnegative_terms=terms,
                   Z=Z, d=d, bprime=bp, L=L)
