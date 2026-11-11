"""Simultaneous separated-core relays and direct exterior completion.

This is an exact optimizer for the stated normal form, not for arbitrary TH
expense. It uses ordinary min-cost bipartite matching, and returns either a
full physical auxiliary matching or a terminal Hall obstruction.
"""
from heapq import heappop, heappush


def neighbours(v):
    a, b = v
    return {(a - 1, b), (a + 1, b), (a, b - 1), (a, b + 1)}


def edge(a, b):
    return tuple(sorted((a, b)))


def assignment(left, right, costs):
    """Exact integer min-cost assignment, with residual-potential/Hall evidence.

    Successive shortest augmenting paths use Bellman--Ford. Vertices may be
    arbitrary hashable objects; source/sink and residual arcs use integer IDs.
    None denotes infeasibility, never a large finite cost sentinel.
    """
    left, right = sorted(left, key=repr), sorted(right, key=repr)
    if len(left) != len(right):
        raise ValueError('Balanced assignment required')
    if any(a not in left or b not in right or type(c) is not int or c < 0
           for (a, b), c in costs.items()):
        raise ValueError('Invalid edge or nonnegative integer cost')
    n = len(left)
    li, ri = {a: j for j, a in enumerate(left)}, {b: n+j for j, b in enumerate(right)}
    source, sink = 2*n, 2*n+1
    graph = [[] for _ in range(2*n+2)]

    def add(a, b, c):
        f, r = [b, len(graph[b]), 1, c], [a, len(graph[a]), 0, -c]
        graph[a].append(f)
        graph[b].append(r)
        return f

    for a in left:
        add(source, li[a], 0)
    for b in right:
        add(ri[b], sink, 0)
    physical = {(a, b): add(li[a], ri[b], c) for (a, b), c in costs.items()}
    flow = 0
    while flow < n:
        dist, parent = [None]*len(graph), [None]*len(graph)
        dist[source] = 0
        for _ in range(len(graph)-1):
            changed = False
            for a, arcs in enumerate(graph):
                if dist[a] is None:
                    continue
                for j, (b, _, capacity, c) in enumerate(arcs):
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
        flow += 1
    matched = {a: b for (a, b), arc in physical.items() if arc[2] == 0}
    residual = [(a, b, c) for a, arcs in enumerate(graph)
                for b, _, capacity, c in arcs if capacity]
    if flow < n:
        # Reverse alternating search from all unmatched right vertices.
        inverse = {b: a for a, b in matched.items()}
        seen_r, seen_l = set(right)-inverse.keys(), set()
        todo = list(seen_r)
        while todo:
            b = todo.pop()
            for a in left:
                if (a, b) not in costs or matched.get(a) == b or a in seen_l:
                    continue
                seen_l.add(a)
                if a in matched and matched[a] not in seen_r:
                    seen_r.add(matched[a])
                    todo.append(matched[a])
        actual_neighbours = {a for (a, b) in costs if b in seen_r}
        assert actual_neighbours == seen_l and len(seen_l) < len(seen_r)
        return dict(optimum=None, matching=matched, hall_right=seen_r,
                    hall_neighbours=seen_l)
    # Super-source distance potentials certify nonnegative residual costs.
    potentials = [0]*len(graph)
    for _ in range(len(graph)-1):
        changed = False
        for a, b, c in residual:
            if potentials[b] > potentials[a]+c:
                potentials[b], changed = potentials[a]+c, True
        if not changed:
            break
    assert all(c+potentials[a]-potentials[b] >= 0 for a, b, c in residual)
    return dict(optimum=sum(costs[a, b] for a, b in matched.items()),
                matching=matched, left=left, right=right,
                potentials=potentials, residual=residual)


def _relay(start, centre, part, mate, weights):
    allowed = part | {start, centre}
    dist, parent = {start: 0}, {}
    heap = [(0, start)]
    while heap:
        d, v = heappop(heap)
        if d != dist[v]:
            continue
        if v == centre:
            path = [v]
            while v != start:
                v = parent[v]
                path.append(v)
            return dict(cost=d, path=list(reversed(path)))
        if sum(v) % 2:  # non-M auxiliary step, white to black
            options = neighbours(v) & allowed
            if v in mate:
                options.discard(mate[v])
        else:  # actual step, black to its white mate
            options = {mate[v]} if v in mate else set()
        for z in sorted(options):
            c = weights[edge(v, z)] if v in mate and mate[v] == z else 0
            nd = d+c
            if z not in dist or nd < dist[z]:
                dist[z], parent[z] = nd, v
                heappush(heap, (nd, z))
    return None


def solve(board, actual, selected, parts, centres, weights=None,
          holes_to_exterior=True):
    """Return the exact centre-relay/direct-exterior normal-form optimum.

    Set holes_to_exterior=False to require all white HH sources to serve
    centres. In that case exactly q=r-|W| selected sources serve centres.
    """
    board, actual, selected = set(board), {edge(a, b) for a, b in actual}, set(selected)
    parts, centres = [set(p) for p in parts], list(centres)
    mate = {}
    for a, b in actual:
        if a not in board or b not in board or b not in neighbours(a) or a in mate or b in mate:
            raise ValueError('Actual edges must form a grid matching')
        mate[a], mate[b] = b, a
    p, r = set(mate), len(parts)
    if not r or len(centres) != r or len(set(centres)) != r:
        raise ValueError('One distinct centre per core required')
    owner = {v: i for i, part in enumerate(parts) for v in part}
    if set(owner) != p or sum(map(len, parts)) != len(p):
        raise ValueError('Cores must partition P')
    if any(owner[a] != owner[b] for a, b in actual):
        raise ValueError('Actual edge crosses cores')
    if any(owner[v] != owner[z] for v in p for z in neighbours(v) & p):
        raise ValueError('Core interiors must be nonadjacent')
    q_vertices = board-p
    if len({v for v in board if sum(v) % 2})*2 != len(board):
        raise ValueError('Balanced board required')
    if any(c not in q_vertices or sum(c) % 2 for c in centres):
        raise ValueError('Centres must be black Q vertices')
    if any(not neighbours(c) & p <= parts[i] for i, c in enumerate(centres)):
        raise ValueError('Centre touches another core')
    if not selected <= q_vertices or any(sum(t) % 2 != 1 for t in selected):
        raise ValueError('Selected vertices must be white Q')
    if any(len(neighbours(t) & p) > 1 for t in selected):
        raise ValueError('Selected vertex has more than one P neighbour')
    if any(neighbours(c) & selected for c in centres):
        raise ValueError('No centre may have a direct selected neighbour')
    white = {v for v in q_vertices if sum(v) % 2}
    holes = white-selected
    black = q_vertices-white-set(centres)
    weights = {e: 1 for e in actual} if weights is None else {edge(a, b): c for (a, b), c in weights.items()}
    if weights.keys() != actual or any(type(c) is not int or c < 0 for c in weights.values()):
        raise ValueError('Every actual edge needs a nonnegative integer weight')
    paths, fees = {}, {}
    for t in sorted(white):
        for i, centre in enumerate(centres):
            relay = _relay(t, centre, parts[i], mate, weights)
            if relay is not None:
                paths[t, i] = relay
                fees[t, ('c', i)] = relay['cost'] if t in selected else 0
        if t in selected or holes_to_exterior:
            for b in neighbours(t) & black:
                fees[t, ('b', b)] = 0
    result = assignment(white, {('b', b) for b in black} | {('c', i) for i in range(r)}, fees)
    result.update(holes=holes, exterior_black=black, selected=selected,
                  relay_options=paths, costs=fees, auxiliary=None,
                  q=r-len(holes), holes_to_exterior=holes_to_exterior)
    if result['optimum'] is None:
        return result
    auxiliary, used_actual, occupied, relays = set(), set(), set(), []
    for t, (kind, target) in result['matching'].items():
        if kind == 'b':
            path = [t, target]
        else:
            path = paths[t, target]['path']
            relays.append(dict(source=t, core=target, path=path, paid=t in selected))
        assert not occupied & set(path)
        occupied.update(path)
        auxiliary.update(edge(path[j], path[j+1]) for j in range(0, len(path)-1, 2))
        used_actual.update(edge(path[j], path[j+1]) for j in range(1, len(path)-1, 2))
    auxiliary.update(actual-used_actual)
    result.update(auxiliary=auxiliary, relays=relays,
                  th_centres=sum(t in selected and kind == 'c'
                                 for t, (kind, _) in result['matching'].items()))
    return result


def source_budget(result, number_of_cores):
    """The q-root HH discount lower bound; None if hypotheses are absent.

    Require all centres to have finite TH expense and Gamma to saturate W.
    Here q=r-|W|>=1. A dummy root represents a relaxed T entrance.
    """
    holes, selected = result['holes'], result['selected']
    q = number_of_cores-len(holes)
    if q < 1:
        return None
    rho = {}
    for i in range(number_of_cores):
        choices = [p['cost'] for (t, j), p in result['relay_options'].items()
                   if t in selected and j == i]
        if not choices:
            return None
        rho[i] = min(choices)
    left = {('w', z) for z in holes} | {('root', j) for j in range(q)}
    costs = {(('w', z), i): 0 for z in holes for i in range(number_of_cores)
             if (z, i) in result['relay_options']}
    costs.update({(('root', j), i): rho[i] for j in range(q) for i in range(number_of_cores)})
    relaxed = assignment(left, set(range(number_of_cores)), costs)
    return None if relaxed['optimum'] is None else dict(lower=relaxed['optimum'], rho=rho,
                                                       assignment=relaxed)
