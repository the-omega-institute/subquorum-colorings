"""Physical matching-cut certificates for owner cores with only P1, P2, C4.

The two physical colour sides are not bipartition classes of the auxiliary
graph. Inside either side, P plus the perfect opposite-square matching R is
bipartite. A partial matching Q joins the sides.
"""
from subcubic_square_core import square_components


def bipartition_components(graph, vertices):
    """Return proper classes of every component of the induced graph."""
    vertices = set(vertices)
    colour, result = {}, []
    for root in sorted(vertices):
        if root in colour:
            continue
        colour[root] = 0
        classes, todo = [{root}, set()], [root]
        while todo:
            v = todo.pop()
            for u in sorted(graph[v] & vertices):
                if u in colour:
                    assert colour[u] != colour[v]
                else:
                    colour[u] = 1-colour[v]
                    classes[colour[u]].add(u)
                    todo.append(u)
        result.append(classes)
    return result


def matching_cut_certificate(P, Q, R, colour):
    """Independent set >=ceil(3n/8) in this physically structured graph.

    P,Q are partial matching dictionaries; R is a perfect matching dictionary.
    P,R preserve the supplied colour; Q reverses it. Both colour sides have
    equal even order. The implementation sorts labels for reproducibility;
    bipartition and matching-neighbour selection themselves take linear work.
    """
    V = set(colour)
    assert set(R) == V and len(V) % 4 == 0
    sides = [{v for v in V if colour[v] == c} for c in (0, 1)]
    assert len(sides[0]) == len(sides[1]) == len(V)//2
    for matching, same in ((P, True), (Q, False), (R, True)):
        assert set(matching) <= V
        assert all(u != v and u in V and matching.get(u) == v and
                   ((colour[v] == colour[u]) == same)
                   for v, u in matching.items())
    J = {v: {m[v] for m in (P, Q, R) if v in m} for v in V}
    inside = {v: {m[v] for m in (P, R) if v in m} for v in V}
    alternatives = []
    for side in (0, 1):
        blocks = bipartition_components(inside, sides[side])
        assert all(len(a) == len(b) for a, b in blocks)
        first = set().union(*(a for a, _ in blocks)) if blocks else set()
        assert 4*len(first) == len(V)
        forbidden = {Q[v] for v in first if v in Q}
        available = sides[1-side]-forbidden
        remaining = bipartition_components(inside, available)
        second = set().union(*(max(ab, key=lambda a: (len(a), sorted(a)))
                               for ab in remaining)) if remaining else set()
        chosen = first | second
        assert len(available) >= len(V)//4
        assert len(second) >= (len(available)+1)//2
        assert all(not J[v] & chosen for v in chosen)
        assert 8*len(chosen) >= 3*len(V)
        alternatives.append(dict(side=side, first=first, forbidden=forbidden,
                                 available=available, second=second, chosen=chosen))
    best = max(alternatives, key=lambda a: (len(a['chosen']), sorted(a['chosen'])))
    return best['chosen'], dict(auxiliary=J, alternatives=alternatives,
                               guarantee=(3*len(V)+7)//8)


def template_certificate(m):
    g, C, I, X = (m[k] for k in ('g', 'C', 'I', 'X'))
    squares = square_components(m)
    inverse = {c: x for x, c in m['owner'].items()}
    assert set(inverse) == C and set(m['owner']) == X
    V = {inverse[c] for square in squares for c in square}
    P, Q, R = {}, {}, {}
    for i in I:
        pair = sorted(g[i] & X)
        assert len(pair) == 2
        a, b = pair
        if a in V and b in V:
            P[a], P[b] = b, a
    for v in V:
        mates = g[v] & X
        assert len(mates) <= 1
        if mates and next(iter(mates)) in V:
            Q[v] = next(iter(mates))
    for square in squares:
        for side in (0, 1):
            a, b = sorted(inverse[c] for c in square
                          if m['graph_colour'][c] == side)
            R[a], R[b] = b, a
    colour = {v: m['graph_colour'][v] for v in V}
    chosen, cut = matching_cut_certificate(P, Q, R, colour)
    deleted = {m['owner'][v] for v in chosen}
    for v, u in R.items():
        if v < u and not {v, u} & chosen:
            deleted.add(m['owner'][v])
    b, t = len(I), len(squares)
    assert len(C) == len(X) == 2*b and 2*t <= b
    assert len(deleted) == 2*t
    D = set(I) | (C-deleted) | chosen
    guarantee = 3*b-t//2
    assert all(len(g[v] & D) <= 1 for v in D)
    assert len(D) >= guarantee >= (11*b+3)//4
    surplus = b-4*(t//2)
    assert surplus == b-2*t+2*(t % 2) >= 0
    return D, dict(square_count=t, chosen=chosen, deleted=deleted,
                   auxiliary=cut['auxiliary'], cut=cut, P=P, Q=Q, R=R,
                   guarantee=guarantee, structural_surplus_W=surplus)


def lift_certificate(g, S, colour, w, beta):
    """The fixed actual extraction must have a P1/P2/C4 owner core."""
    model = dict(g=g, C=w['C0'], I=w['I0'], X=w['X0'],
                 owner=w['owner'], graph_colour=colour)
    inner, data = template_certificate(model)
    retained = (w['R']-w['I0']) | {ell for c, ell, x in w['triples']}
    assert not inner & retained and all(not g[v] & inner for v in retained)
    D = inner | retained
    assert all(len(g[v] & D) <= 1 for v in D) and len(D) <= beta
    p, u = len(w['triples']), len(w['pairs'])
    a, b, b3 = w['a'], w['b'], w['b3']
    minimum = min(a, p)
    alpha, pi = a-minimum, p-minimum
    e, r = u-a-2*b, len(w['R'])-a-b
    q, d = len(g)-len(S)-p-u, len(S)-beta
    tau = minimum+b-2*d
    bp, L = len(w['I0']), len(retained)
    assert bp == b-b3
    assert len(g) == 10*d+minimum+r+3*(alpha+pi)+2*e+q+5*tau
    assert beta-L == 2*minimum+alpha+pi+3*b+e-b3-d
    W = 4*(beta-L)-11*bp
    assert 2*d+W == 7*minimum+4*(alpha+pi)+4*e+7*b3+tau
    terms = [W, 7*r, 17*(alpha+pi), 10*(e-b3), 3*b3, 7*q, 34*tau]
    assert all(v >= 0 for v in terms)
    assert W >= data['structural_surplus_W']
    assert sum(terms) == 7*len(g)-72*d
    return D, dict(template=data, inner=inner, retained=retained, W=W,
                   d=d, bprime=bp, L=L, nonnegative_terms=terms,
                   exact_margin=7*len(g)-72*d)
