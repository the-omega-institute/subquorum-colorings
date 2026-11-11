"""Residual Hall demand, source capacity and physical compensation certificates.

The two lower bounds are relaxations for arbitrary full completions retaining
specified terminal paths. Their maximum, not their sum, is valid. A successful
direct-TH remainder matching supplies an attaining full physical certificate.
"""
from heapq import heappop, heappush


def pair(a, b):
    return tuple(sorted((a, b)))


def flow(vertices, arcs, source, sink, limit):
    """Standard integral min-cost flow, unit capacities, exact integer costs."""
    vertices = sorted(vertices, key=repr)
    index = {v: i for i, v in enumerate(vertices)}
    source, sink = index[source], index[sink]
    edges = [(index[a], index[b], cost) for a, b, cost in arcs]
    if len(set((a, b) for a, b, _ in edges)) != len(edges):
        raise ValueError('Parallel arcs are not used by this adapter')
    if any(type(c) is not int or c < 0 for _, _, c in edges) or limit < 0:
        raise ValueError('Nonnegative integer costs and demand required')
    graph = [[] for _ in vertices]
    forwards = []
    for a, b, c in edges:
        forwards.append((a, len(graph[a])))
        graph[a].append([b, len(graph[b]), 1, c])
        graph[b].append([a, len(graph[a])-1, 0, -c])
    value = 0
    while value < limit:
        dist, parent = [None]*len(vertices), [None]*len(vertices)
        dist[source] = 0
        for _ in range(len(vertices)-1):
            changed = False
            for a, options in enumerate(graph):
                if dist[a] is None:
                    continue
                for j, (b, _, capacity, c) in enumerate(options):
                    if capacity and (dist[b] is None or dist[b] > dist[a]+c):
                        dist[b], parent[b], changed = dist[a]+c, (a, j), True
            if not changed:
                break
        if dist[sink] is None:
            break
        b = sink
        while b != source:
            a, j = parent[b]
            arc = graph[a][j]
            arc[2] -= 1
            graph[b][arc[1]][2] += 1
            b = a
        value += 1
    used = [i for i, (a, j) in enumerate(forwards) if not graph[a][j][2]]
    residual = [(a, b, c) for a, options in enumerate(graph)
                for b, _, capacity, c in options if capacity]
    potentials = [0]*len(vertices)
    for _ in range(len(vertices)-1):
        changed = False
        for a, b, c in residual:
            if potentials[b] > potentials[a]+c:
                potentials[b], changed = potentials[a]+c, True
        if not changed:
            break
    assert all(c+potentials[a]-potentials[b] >= 0 for a, b, c in residual)
    reachable, pending = {source}, [source]
    while pending:
        a = pending.pop()
        for b, _, capacity, _ in graph[a]:
            if capacity and b not in reachable:
                reachable.add(b)
                pending.append(b)
    if value < limit:
        assert sink not in reachable
        assert sum(a in reachable and b not in reachable for a, b, _ in edges) == value
    # Decompose the integral flow into source/sink paths; discard circulations.
    remaining = set(used)
    paths = []
    for _ in range(value):
        parent, pending = {source: None}, [source]
        while pending and sink not in parent:
            a = pending.pop()
            for i in sorted(remaining):
                x, b, _ = edges[i]
                if x == a and b not in parent:
                    parent[b] = (a, i)
                    pending.append(b)
        assert sink in parent
        p, b = [sink], sink
        while b != source:
            a, i = parent[b]
            remaining.remove(i)
            b = a
            p.append(b)
        paths.append([vertices[i] for i in reversed(p)])
    # Any discarded circulation has zero cost at a min-cost solution.
    assert sum(edges[i][2] for i in remaining) == 0
    return dict(value=value, cost=sum(edges[i][2] for i in used), limit=limit,
                vertices=vertices, arcs=edges, used=used, source=source, sink=sink,
                potentials=potentials, reachable=sorted(reachable), paths=paths)


def residual_data(board, actual, selected, fixed, weights=None):
    board, actual, selected = set(board), {pair(*e) for e in actual}, set(selected)
    if any(sum(v) % 2 != 1 for v in selected):
        raise ValueError('Selected colour is white (odd coordinate sum)')
    if sum(sum(v) % 2 == 1 for v in board)*2 != len(board):
        raise ValueError('Balanced finite grid board required')
    if any(len(e) != 2 or not set(e) <= board or
           sum(abs(a-b) for a, b in zip(*e)) != 1 for e in actual):
        raise ValueError('Invalid actual matching')
    mate = {v: w for e in actual for v, w in (e, e[::-1])}
    if len(mate) != 2*len(actual) or selected & mate.keys():
        raise ValueError('Actual matching and selected terminals must be disjoint')
    weights = {e: 1 for e in actual} if weights is None else {pair(*e): w for e, w in weights.items()}
    if set(weights) != actual or any(type(w) is not int or w < 0 for w in weights.values()):
        raise ValueError('Exact nonnegative integer weight for every actual edge required')
    q = board-mate.keys()
    removed, fixed_n, paid = set(), set(), 0
    for path in fixed:
        if len(path) < 2 or len(path) % 2 or len(set(path)) != len(path):
            raise ValueError('Simple odd-length terminal path required')
        if not set(path) <= board or set(path) & removed:
            raise ValueError('Fixed paths must be disjoint and inside the board')
        if path[0] not in q or path[-1] not in q or sum(path[0]) % 2 != 1 or sum(path[-1]) % 2:
            raise ValueError('Orient fixed paths from white Q to black Q')
        if any(v not in mate for v in path[1:-1]):
            raise ValueError('Interiors must lie in P')
        if any(sum(abs(x-y) for x, y in zip(a, b)) != 1 for a, b in zip(path, path[1:])):
            raise ValueError('Grid path required')
        if any(pair(path[i], path[i+1]) not in actual for i in range(1, len(path)-1, 2)):
            raise ValueError('Actual pairs must alternate')
        fixed_n.update(pair(path[i], path[i+1]) for i in range(0, len(path)-1, 2))
        if path[0] in selected:
            paid += sum(weights[pair(path[i], path[i+1])] for i in range(1, len(path)-1, 2))
        removed.update(path)
    assert all(bool(set(e) & removed) == (set(e) <= removed) for e in actual)
    remaining = board-removed
    m = {e for e in actual if set(e) <= remaining}
    t = selected-removed
    p = {v for e in m for v in e}
    qr = remaining-p
    white_q = {v for v in qr if sum(v) % 2}
    black_q = qr-white_q
    adjacency = {v: {w for w in remaining if sum(abs(a-b) for a, b in zip(v, w)) == 1}
                 for v in remaining}
    physical = []
    for a in remaining:
        if sum(a) % 2:
            physical.extend((a, b, 0) for b in adjacency[a] if pair(a, b) not in m)
    physical.extend((next(v for v in e if not sum(v) % 2),
                     next(v for v in e if sum(v) % 2), weights[e]) for e in m)
    return dict(board=remaining, actual=m, selected=t, holes=white_q-t,
                black_q=black_q, physical=physical, adjacency=adjacency,
                fixed_auxiliary=fixed_n, fixed_expense=paid, original_board=board,
                original_actual=actual, original_selected=selected, weights=weights)


def route(data, sources, sinks, limit, free=False):
    arcs = [(a, b, 0 if free else c) for a, b, c in data['physical']]
    arcs += [('S', t, 0) for t in sorted(sources)]
    arcs += [(b, 'Z', 0) for b in sorted(sinks)]
    return flow(data['board'] | {'S', 'Z'}, arcs, 'S', 'Z', limit)


def distances(data, source):
    outgoing = {v: [] for v in data['board']}
    for a, b, c in data['physical']:
        outgoing[a].append((b, c))
    dist, pending = {source: 0}, [(0, source)]
    while pending:
        cost, a = heappop(pending)
        if cost != dist[a]:
            continue
        for b, c in outgoing[a]:
            if b not in dist or cost+c < dist[b]:
                dist[b] = cost+c
                heappush(pending, (cost+c, b))
    return dist


def complete_direct(data, extra):
    """Known fixed-path extension test: all remaining TH must be direct."""
    added = residual_data(data['board'], data['actual'], data['selected'], extra,
                          {e: data['weights'][e] for e in data['actual']})
    black = {v for v in added['board'] if not sum(v) % 2}
    white = added['board']-black
    p = {v for e in added['actual'] for v in e}
    arcs = [('S', w, 0) for w in sorted(white)]
    arcs += [(w, b, 0) for w in sorted(white) for b in sorted(added['adjacency'][w])
             if w not in added['selected'] or b not in p]
    arcs += [(b, 'Z', 0) for b in sorted(black)]
    result = flow(added['board'] | {'S', 'Z'}, arcs, 'S', 'Z', len(black))
    if result['value'] < len(black):
        return dict(auxiliary=None, certificate=result)
    auxiliary = set(data['fixed_auxiliary']) | set(added['fixed_auxiliary'])
    auxiliary.update(pair(p[1], p[2]) for p in result['paths'])
    return dict(auxiliary=auxiliary, certificate=result)


def cheapest_non_direct_TH(data):
    """Minimum non-direct residual TH expense, or value zero if none exists.

    Forbid only direct source-to-terminal arcs. Every surviving source/sink
    path must then use an actual edge. The returned flow has demand one;
    value zero denotes no such path, rather than a zero-cost path.
    """
    arcs = [(a, b, c) for a, b, c in data['physical']
            if not (a in data['selected'] and b in data['black_q'])]
    arcs += [('S', t, 0) for t in sorted(data['selected'])]
    arcs += [(b, 'Z', 0) for b in sorted(data['black_q'])]
    return flow(data['board'] | {'S', 'Z'}, arcs, 'S', 'Z', 1)


def bound(data, region, attempt_completion=True):
    dset = set(region)
    if not dset <= data['black_q']:
        raise ValueError('Hall region must consist of remaining black terminals')
    neighbours = {t for t in data['selected'] if data['adjacency'][t] & dset}
    demand = max(0, len(dset)-len(neighbours))
    outside = data['selected']-neighbours
    hh = route(data, data['holes'], dset, min(len(data['holes']), len(dset)), free=True)
    required_th = max(0, demand-hh['value'])
    th = route(data, outside, dset, required_th)
    sources = outside | data['holes']
    abstract_arcs = [('S', t, 0) for t in sorted(sources)]
    abstract_arcs += [(b, 'Z', 0) for b in sorted(dset)]
    for t in sorted(sources):
        dist = distances(data, t)
        abstract_arcs.extend((t, b, 0 if t in data['holes'] else dist[b])
                             for b in sorted(dset) if b in dist)
    joint = flow(sources | dset | {'S', 'Z'}, abstract_arcs, 'S', 'Z', demand)
    feasible = th['value'] == required_th and joint['value'] == demand
    extra_lower = max(th['cost'], joint['cost']) if feasible else None
    answer = dict(region=dset, direct_neighbours=neighbours, demand=demand,
                  max_HH=hh['value'], required_TH=required_th,
                  HH_flow=hh, TH_flow=th, joint_assignment=joint,
                  extra_lower=extra_lower,
                  lower=None if extra_lower is None else data['fixed_expense']+extra_lower)
    if attempt_completion and feasible:
        paths = [p[1:-1] for p in th['paths']]
        completion = complete_direct(data, paths)
        answer['completion'] = completion
        if completion['auxiliary'] is not None:
            assert th['cost'] >= joint['cost']
            answer['certified_optimum'] = data['fixed_expense']+th['cost']
    return answer
