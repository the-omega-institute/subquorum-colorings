"""Exact representative/dissociation certificates for extended double covers."""


def validate_base(adjacency):
    h = [set(row) for row in adjacency]
    n = len(h)
    if any(any(type(v) is not int or not 0 <= v < n or v == u for v in row)
           for u, row in enumerate(h)):
        raise ValueError('Finite simple base on consecutive integer vertices required')
    if any(u not in h[v] for u, row in enumerate(h) for v in row):
        raise ValueError('Undirected base required')
    return h


def extended_cover(adjacency):
    h = validate_base(adjacency)
    n = len(h)
    g = [set() for _ in range(2*n)]
    for u in range(n):
        for v in h[u] | {u}:
            g[u].add(n+v)
            g[n+v].add(u)
    return g


def optimum_certificate(adjacency):
    """Kuhn augmentations on the ordinary double cover, plus a Hall witness.

    Ordinary double-cover edges have no diagonal rungs. Indices on its two
    sides are separately 0,...,n-1. The returned dissociation set uses the
    extended-cover convention white i, black n+i.
    """
    h = validate_base(adjacency)
    n = len(h)
    right, left = {}, {}
    options = [sorted(row) for row in h]
    for root in range(n):
        parent, seen_l, pending, endpoint = {}, {root}, [root], None
        while pending and endpoint is None:
            u = pending.pop()
            for v in options[u]:
                if v in parent:
                    continue
                parent[v] = u
                if v not in right:
                    endpoint = v
                    break
                if right[v] not in seen_l:
                    seen_l.add(right[v])
                    pending.append(right[v])
        if endpoint is not None:
            v = endpoint
            while True:
                u = parent[v]
                old = left.get(u)
                left[u], right[v] = v, u
                if old is None:
                    break
                v = old
    reached_l, reached_r = set(range(n))-left.keys(), set()
    pending = sorted(reached_l)
    while pending:
        u = pending.pop()
        for v in h[u]-reached_r:
            # A matched u was reached from its matched v, so that v is
            # already reached. All newly reached edges are nonmatching.
            reached_r.add(v)
            if v in right and right[v] not in reached_l:
                reached_l.add(right[v])
                pending.append(right[v])
    assert {v for u in reached_l for v in h[u]} == reached_r
    independent = reached_l-reached_r
    neighbours = {v for u in independent for v in h[u]}
    delta = n-len(right)
    assert not independent & neighbours
    assert len(independent)-len(neighbours) == delta
    rest = set(range(n))-independent-neighbours
    dissociation = independent | {n+v for v in independent} | rest
    return dict(optimum=n+delta, deficiency=delta,
                double_matching=sorted((u, v) for v, u in right.items()),
                double_vertex_cover_left=sorted(set(range(n))-reached_l),
                double_vertex_cover_right=sorted(reached_r),
                Hall_left=sorted(reached_l), Hall_right=sorted(reached_r),
                critical_independent=sorted(independent),
                critical_neighbours=sorted(neighbours), dissociation=sorted(dissociation))


def validate_pair(g, actual, selected):
    actual = {tuple(sorted(e)) for e in actual}
    selected = set(selected)
    vertices = set(range(len(g)))
    if not selected <= vertices:
        raise ValueError('Selected vertices outside graph')
    if any(len(e) != 2 or not set(e) <= vertices or e[1] not in g[e[0]] for e in actual):
        raise ValueError('Invalid actual edge')
    mate = {v: w for e in actual for v, w in (e, e[::-1])}
    if len(mate) != 2*len(actual) or selected & mate.keys():
        raise ValueError('Actual edges must be a matching disjoint from selection')
    occupied_or_selected = selected | mate.keys()
    if any(len(g[t] & occupied_or_selected) > 1 for t in selected):
        raise ValueError('Infeasible representative pair')
    return actual, selected, mate


def representative_certificate(adjacency, actual, selected):
    h = validate_base(adjacency)
    n = len(h)
    g = extended_cover(h)
    actual, selected, mate = validate_pair(g, actual, selected)
    outside = set(range(2*n))-selected-mate.keys()
    classes = {name: [] for name in ('TT', 'ZZ', 'TP', 'PZ', 'TZ', 'PP')}
    kinds = {frozenset(('T', 'P')): 'TP', frozenset(('P', 'Z')): 'PZ',
             frozenset(('T', 'Z')): 'TZ'}
    for i in range(n):
        labels = ['T' if v in selected else 'P' if v in mate else 'Z' for v in (i, n+i)]
        kind = labels[0]*2 if labels[0] == labels[1] else kinds[frozenset(labels)]
        classes[kind].append(i)
    injection = []
    for i in classes['TP']:
        p = next(v for v in (i, n+i) if v in mate)
        j = mate[p] % n
        assert j in classes['PZ']
        injection.append((i, j))
    assert len({j for _, j in injection}) == len(injection)
    independent = set(classes['TT'])
    neighbours = {v for u in independent for v in h[u]}
    assert not independent & neighbours and neighbours <= set(classes['ZZ'])
    objective = len(selected)+len(actual)
    a, b, u, v = (len(classes[k]) for k in ('TT', 'ZZ', 'TP', 'PZ'))
    assert 2*(objective-n) == 2*(a-b)+u-v
    return dict(objective=objective, classes=classes, injection=injection,
                TT_neighbours=sorted(neighbours),
                independent_defect=len(independent)-len(neighbours))


def zero_TH_completion(adjacency, actual, selected):
    """Direct terminal completion for feasible white-only T, arbitrary M.

    Every selected vertex is paired directly with black Q. Thus every
    nonnegative choice of actual-edge weights has true TH expense zero.
    """
    h = validate_base(adjacency)
    n = len(h)
    actual, selected, mate = validate_pair(extended_cover(h), actual, selected)
    if any(t >= n for t in selected):
        raise ValueError('Selected sources must be white')
    used, auxiliary, swaps = set(), set(), []
    for j in sorted(selected):
        if n+j not in mate:
            continue
        i = mate[n+j]
        assert i < n and i != j and j in h[i] and n+i not in mate
        assert not {i, j} & used
        used.update((i, j))
        swaps.append((i, j))
        auxiliary.update(((i, n+j), (j, n+i)))
    auxiliary.update((i, n+i) for i in range(n) if i not in used)
    return dict(auxiliary=sorted(auxiliary), swaps=swaps)


def minimal_forming_certificate(adjacency, selected):
    """Validate minimal formation and expose its two-per-empty-rung budget.

    This constructs literal deletion witnesses; it does not infer minimality
    from the proved parameter formula. Cost is polynomial in cover size.
    """
    h = validate_base(adjacency)
    n = len(h)
    g = extended_cover(h)
    selected = set(selected)
    vertices = set(range(2*n))
    if not selected <= vertices:
        raise ValueError('Selected vertices outside graph')

    def unformed(s):
        active = {v for v in s if g[v] & s}
        return {x for x in vertices-s if len(g[x] & s) < 2 and not g[x] & active}

    if unformed(selected):
        raise ValueError('Set is not forming')
    failures = {s: unformed(selected-{s}) for s in selected}
    if any(not values for values in failures.values()):
        raise ValueError('Set is not inclusion-minimal forming')
    doubles = {i for i in range(n) if {i, n+i} <= selected}
    isolated = {i for i in doubles if g[i] & selected == {n+i}
                and g[n+i] & selected == {i}}
    high = doubles-isolated
    empty = {i for i in range(n) if not {i, n+i} & selected}
    near_isolated = {v for u in isolated for v in h[u]}
    assert not isolated & near_isolated and near_isolated <= empty
    relevant = high | {n+i for i in high}
    budget = {i: set() for i in empty}
    for s in relevant:
        assert s not in failures[s] and failures[s]
        for x in failures[s]:
            assert x not in selected and x % n in empty
            budget[x % n].add(s)
    assert all(len(values) <= 2 for values in budget.values())
    assert all(not budget[i] for i in near_isolated)
    assert relevant <= {s for values in budget.values() for s in values}
    defect = len(isolated)-len(near_isolated)
    assert len(high) <= len(empty)-len(near_isolated)
    assert len(selected) <= n+defect
    return dict(size=len(selected), isolated_rungs=sorted(isolated),
                isolated_neighbours=sorted(near_isolated), high_rungs=sorted(high),
                empty_rungs=sorted(empty), independent_defect=defect,
                deletion_witnesses={s: sorted(values) for s, values in failures.items()},
                empty_rung_deletions={i: sorted(values) for i, values in budget.items()})
