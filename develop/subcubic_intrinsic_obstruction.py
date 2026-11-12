"""Constructive dissociation certificates for degree-three intrinsic templates."""
from fractions import Fraction
from itertools import product


def template(k, first, second, interface):
    h = 2*k
    if k < 1 or any(sorted(p) != list(range(h)) for p in (first, second, interface)):
        raise ValueError('Use k>=1 and three permutations of range(2k)')
    if any(a == b for a, b in zip(first, second)):
        raise ValueError('The two core matchings must be edge-disjoint')
    g = [set() for _ in range(10*k)]

    def edge(a, b):
        g[a].add(b)
        g[b].add(a)

    C = set(range(2*h))
    X = set(range(2*h, 4*h))
    I = set(range(4*h, 5*h))
    owner, centre, pair = {}, {}, {}
    for i in range(h):
        edge(i, h+first[i])
        edge(i, h+second[i])
        edge(2*h+i, 3*h+interface[i])
        for c, x in ((i, 3*h+i), (h+i, 2*h+i)):
            edge(c, x)
            owner[x] = c
    for j in range(k):
        for base, z in ((2*h, 4*h+k+j), (3*h, 4*h+j)):
            a, b = base+2*j, base+2*j+1
            edge(z, a)
            edge(z, b)
            pair[a], pair[b] = b, a
            centre[a] = centre[b] = z
    q = {x: next(iter(g[x] & X)) for x in X}
    aux = {x: {pair[x], q[x]} for x in X}
    components, group, colour = [], {}, {}
    unseen = set(X)
    while unseen:
        start = min(unseen)
        order, previous, v = [], None, start
        while v not in order:
            order.append(v)
            group[v], colour[v] = len(components), (len(order)-1) % 2
            nxt = min(aux[v] - ({previous} if previous is not None else set()))
            previous, v = v, nxt
        assert v == start and len(order) % 4 == 0
        components.append(order)
        unseen -= set(order)
    return dict(k=k, g=g, C=C, X=X, I=I, owner=owner, centre=centre,
                pair=pair, q=q, components=components, group=group, colour=colour)


def side_certificate(m):
    k, h = m['k'], 2*m['k']
    J = set()
    lengths = []
    for component in m['components']:
        pairs = list(dict.fromkeys((x-3*h)//2 for x in component if x >= 3*h))
        ell = len(pairs)
        assert 4*ell == len(component)
        lengths.append(ell)
        J.update(pairs[j] for j in range(0, 2*(ell//2), 2))
    T = {3*h+2*j+t for j in J for t in (0, 1)}
    forbidden = {m['q'][x] for x in T}
    D = set(range(h)) | T | {4*h+j for j in range(k) if j not in J}
    D.update(range(4*h+k, 5*h))
    for j in range(k):
        available = {2*h+2*j, 2*h+2*j+1} - forbidden
        if available:
            D.add(min(available))
    return D, dict(delta=sum(ell//2 for ell in lengths),
                   k0=lengths.count(1), lengths=lengths, J=sorted(J))


def short_expectation(m, fixed):
    """Exact conditional expectation; each summand uses at most three bits."""
    inverse = {c: x for x, c in m['owner'].items()}
    total = Fraction(0)
    for v in sorted(m['C']):
        x = inverse[v]
        if len(m['components'][m['group'][x]]) != 4:
            continue
        core_neighbours = m['g'][v] & m['C']
        involved = {m['group'][inverse[u]] for u in core_neighbours | {v}}
        free = sorted(involved - fixed.keys())
        good = 0
        for bits in product((0, 1), repeat=len(free)):
            phase = fixed | dict(zip(free, bits))

            def present(u):
                w = inverse[u]
                return m['colour'][w] != phase[m['group'][w]]

            good += present(v) and sum(present(u) for u in core_neighbours) <= 1
        total += Fraction(good, 2**len(free))
    return total


def path_cycle_optimum(g, allowed):
    """Three-consecutive-bit DP, including the wrap constraints for cycles."""
    answer = set()
    unseen = set(allowed)
    while unseen:
        start = min(unseen)
        component, todo = {start}, [start]
        while todo:
            for u in (g[todo.pop()] & allowed)-component:
                component.add(u)
                todo.append(u)
        assert all(len(g[v] & component) <= 2 for v in component)
        endpoints = sorted(v for v in component if len(g[v] & component) <= 1)
        cyclic = not endpoints
        v, previous, order = (endpoints[0] if endpoints else start), None, []
        while v not in order:
            order.append(v)
            nxt = sorted((g[v] & component)-({previous} if previous is not None else set()))
            if not nxt:
                break
            previous, v = v, nxt[0]
        assert set(order) == component
        n = len(order)
        candidates = []
        for prefix in product((0, 1), repeat=min(2, n)):
            states = {prefix: prefix}
            for _ in range(2, n):
                fresh = {}
                for tail, word in states.items():
                    for bit in (0, 1):
                        if tail == (1, 1) and bit:
                            continue
                        key, new_word = (tail[-1], bit), word+(bit,)
                        if key not in fresh or sum(new_word) > sum(fresh[key]):
                            fresh[key] = new_word
                states = fresh
            for word in states.values():
                if cyclic and (word[-2:]+word[:1] == (1, 1, 1)
                               or word[-1:]+word[:2] == (1, 1, 1)):
                    continue
                candidates.append(word)
        word = max(candidates, key=lambda w: (sum(w), w))
        answer.update(v for v, bit in zip(order, word) if bit)
        unseen -= component
    return answer


def phase_certificate(m):
    fixed = {}
    initial = short_expectation(m, fixed)
    expectations = [initial]
    for j in range(len(m['components'])):
        a, b = (short_expectation(m, fixed | {j: bit}) for bit in (0, 1))
        fixed[j] = int(b > a)
        expectations.append(max(a, b))
        assert expectations[-1] >= expectations[-2]
    Y = {x for x in m['X'] if m['colour'][x] == fixed[m['group'][x]]}
    R = m['C'] - {m['owner'][x] for x in Y}
    Z = path_cycle_optimum(m['g'], R)
    L = sum(len(m['g'][v] & R) <= 1 for v in R)
    D = m['I'] | Y | Z
    return D, dict(phases=[fixed[j] for j in range(len(fixed))],
                   expectation=[str(v) for v in expectations],
                   initial=initial, L=L, R=R, Z=Z, Y=Y)


def certificates(m):
    first, ledger = side_certificate(m)
    second, phase = phase_certificate(m)
    return (first if len(first) >= len(second) else second), first, second, ledger, phase
