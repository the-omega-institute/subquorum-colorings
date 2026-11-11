"""Rung certificates for graphs with an adjacent involution and their prisms.

Vertices are 0,...,2*n-1; the supplied involution is i <-> n+i.
The only project dependency is the existing ordinary-double-cover matcher.
"""
from extended_double_cover import optimum_certificate, validate_base, validate_pair


def prism(adjacency):
    h = validate_base(adjacency)
    n = len(h)
    return [set(h[i]) | {n+i} for i in range(n)] + [
        {n+j for j in h[i]} | {i} for i in range(n)]


def validate_paired(adjacency):
    g = validate_base(adjacency)
    if len(g) % 2:
        raise ValueError('An even number of vertices is required')
    n = len(g)//2
    tau = lambda v: (v+n) % (2*n)
    if any(tau(v) not in g[v] or {tau(u) for u in g[v]} != g[tau(v)]
           for v in range(2*n)):
        raise ValueError('The supplied paired involution must preserve adjacency and have every rung')
    h = [{u % n for u in g[i] if u % n != i} for i in range(n)]
    return g, h


def _failures(g, selected):
    active = {v for v in selected if g[v] & selected}
    return {x for x in range(len(g)) if x not in selected
            and len(g[x] & selected) < 2 and not g[x] & active}


def minimal_forming_budget(adjacency, selected):
    g, h = validate_paired(adjacency)
    n, selected = len(h), set(selected)
    if not selected <= set(range(2*n)) or _failures(g, selected):
        raise ValueError('Not a forming set on the stated vertices')
    failures = {s: _failures(g, selected-{s}) for s in selected}
    if any(not row for row in failures.values()):
        raise ValueError('Not inclusion-minimal forming')
    doubles = {i for i in range(n) if {i, n+i} <= selected}
    isolated = {i for i in doubles if g[i] & selected == {n+i}
                and g[n+i] & selected == {i}}
    high, empty = doubles-isolated, {i for i in range(n) if not {i, n+i} & selected}
    reserved = {v for i in isolated for v in h[i]}
    assert not isolated & reserved and reserved <= empty
    relevant = high | {n+i for i in high}
    budgets = {i: set() for i in empty}
    for s in relevant:
        assert s not in failures[s]
        for x in failures[s]:
            assert x not in selected and x % n in empty
            budgets[x % n].add(s)
    assert all(len(row) <= 2 for row in budgets.values())
    assert all(not budgets[i] for i in reserved)
    assert len(high) <= len(empty)-len(reserved)
    assert len(selected) <= n+len(isolated)-len(reserved)
    return dict(size=len(selected), isolated=sorted(isolated), high=sorted(high),
                empty=sorted(empty), reserved=sorted(reserved),
                defects=len(isolated)-len(reserved),
                failures={s: sorted(row) for s, row in failures.items()},
                budgets={i: sorted(row) for i, row in budgets.items()})


def representative_budget(adjacency, actual, selected):
    g, h = validate_paired(adjacency)
    n = len(h)
    actual, selected, mate = validate_pair(g, actual, selected)
    outside = set(range(2*n))-selected-mate.keys()
    classes = {name: [] for name in ('TT', 'ZZ', 'TP', 'PZ', 'TZ', 'PP')}
    names = {frozenset(('T', 'P')): 'TP', frozenset(('P', 'Z')): 'PZ',
             frozenset(('T', 'Z')): 'TZ'}
    for i in range(n):
        labels = ['T' if v in selected else 'P' if v in mate else 'Z' for v in (i, n+i)]
        name = labels[0]*2 if labels[0] == labels[1] else names[frozenset(labels)]
        classes[name].append(i)
    injection = []
    for i in classes['TP']:
        p = next(v for v in (i, n+i) if v in mate)
        q = mate[p]
        assert (q+n) % (2*n) in outside
        assert q % n in classes['PZ']
        injection.append((i, q % n))
    assert len({j for _, j in injection}) == len(injection)
    independent = set(classes['TT'])
    neighbours = {v for i in independent for v in h[i]}
    assert not independent & neighbours and neighbours <= set(classes['ZZ'])
    objective = len(actual)+len(selected)
    a, b, u, v = (len(classes[key]) for key in ('TT', 'ZZ', 'TP', 'PZ'))
    assert 2*(objective-n) == 2*(a-b)+u-v
    assert objective <= n+len(independent)-len(neighbours)
    return dict(objective=objective, classes=classes, injection=injection,
                defects=len(independent)-len(neighbours))


def paired_optimum_certificate(adjacency):
    """Exact Omega for any paired graph, and an upper bound for SF_2."""
    g, h = validate_paired(adjacency)
    n = len(h)
    # Retain the ordinary-cover matching dual, without the producer's
    # E(H)-specific dissociation set (which need not work in this G).
    dual = {key: value for key, value in optimum_certificate(h).items()
            if key != 'dissociation'}
    independent = set(dual['critical_independent'])
    neighbours = set(dual['critical_neighbours'])
    rest = set(range(n))-independent-neighbours
    selected = independent | {n+i for i in independent}
    actual = {(i, n+i) for i in rest}
    representative_budget(g, actual, selected)
    assert len(selected)+len(actual) == dual['optimum']
    return dict(optimum=dual['optimum'], quotient=h, matching_dual=dual,
                selected=sorted(selected), actual=sorted(actual))


def prism_optimum_certificate(adjacency):
    """Exact SF_2 and Omega; includes literal local deletion witnesses."""
    h = validate_base(adjacency)
    g, n = prism(h), len(h)
    result = paired_optimum_certificate(g)
    dual = result['matching_dual']
    independent = set(dual['critical_independent'])
    rest = set(range(n))-independent-set(dual['critical_neighbours'])
    selected = independent | {n+i for i in independent} | rest
    assert all(h[i] & rest for i in rest)
    result['forming'] = sorted(selected)
    result['deletion_witnesses'] = {s: s if s % n in independent else n+s for s in selected}
    return result


def direct_terminal_completion(adjacency, actual, selected):
    """Full completion for a feasible independent T, with every T--H direct.

    T may use either or both layers. No bipartiteness is assumed.
    """
    g, h = validate_paired(adjacency)
    n = len(h)
    actual, selected, mate = validate_pair(g, actual, selected)
    if any(g[t] & selected for t in selected):
        raise ValueError('This direct-terminal theorem requires independent T')
    used, auxiliary = set(), set()
    for t in sorted(selected):
        p = (t+n) % (2*n)
        if p not in mate:
            continue
        q = mate[p]
        z = (q+n) % (2*n)
        assert z not in selected and z not in mate and z in g[t]
        assert not {t % n, q % n} & used
        used.update((t % n, q % n))
        auxiliary.update((tuple(sorted((p, q))), tuple(sorted((t, z)))))
    auxiliary.update((i, n+i) for i in range(n) if i not in used)
    return sorted(auxiliary)


def near_complete_base(n, missing):
    if type(n) is not int or type(missing) is not int or n < 5 or not 0 <= 2*missing <= n:
        raise ValueError('Require n>=5 and a matching of missing edges')
    h = [set(range(n))-{i} for i in range(n)]
    for j in range(missing):
        h[2*j].remove(2*j+1)
        h[2*j+1].remove(2*j)
    return h


def near_complete_certificate(n, missing):
    h = near_complete_base(n, missing)
    g = prism(h)
    result = prism_optimum_certificate(h)
    dissociation = [0, 1, n+2, n+3]
    if missing >= 2:
        # Distinct missing leaf pairs and their common rung centre.
        colours = {4: 1, n+4: 1, 0: 2, 1: 3, n+2: 4, n+3: 5}
    else:
        colours = {v: i+1 for i, v in enumerate(dissociation)}
    assert all(2*sum(colours[u] == colours[v] for u in ({v} | g[v]) & colours.keys())
               >= len(({v} | g[v]) & colours.keys()) for v in colours)
    result.update(dissociation=dissociation, colouring=colours, beta=4,
                  psi=4+int(missing >= 2), SF=n, Omega=n)
    return result
