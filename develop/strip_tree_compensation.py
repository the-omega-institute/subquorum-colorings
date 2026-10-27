"""Exact physical TH payment solver for two-column cells with forest M graph.

Standard tree messages are coupled to an exact ladder matching transfer.
Cross-cell edges are never merged: parallel edges and cycles are rejected.
Costs are nonnegative integers, charged once per actual matching edge.
"""
from itertools import product
from math import inf

from check_general_square_ports import edge, grid, mates, physical_state


def word_lifts(word):
    """Canonical rung / paired-mixed-row decoder, valid for any alphabet."""
    j = 0
    while j < len(word):
        a, b = word[j]
        if a == b:
            j += 1
        elif j+1 < len(word) and tuple(word[j+1]) == (a, b):
            j += 2
        else:
            return False
    return True


def local_optimum(rows, allowed, unary, internal, weights, parent_pin=None):
    """At most 18 previous-label/pending-N states, 9 row labels each.

    A pending N row is joined by BOTH vertical dominoes to the next row.
    Previous row labels are retained even without pending N, to enforce
    actual M vertical edges. This is a physical matching DP, not a scalar flow.
    """
    lower_mask = {}; horizontal_m = set(); row_cost = {}
    for e in internal:
        a, b = e
        if a[0] == b[0]:
            horizontal_m.add(a[0])
        else:
            lower_mask.setdefault(b[0], set()).add(a[1])
        # Count this INTERNAL actual edge once, at its smaller endpoint.
        row_cost[a] = row_cost.get(a, 0)+weights[e]
    dp = {(None, False): 0}; history = []
    for r, columns in rows:
        vertices = [(r, c) for c in columns]
        options = []
        for pair in product(range(3), repeat=2):
            if any(pair[j] not in allowed[v] for j, v in enumerate(vertices)):
                continue
            if parent_pin is not None and any(v == parent_pin[0] and pair[j] != parent_pin[1]
                                              for j, v in enumerate(vertices)):
                continue
            if r in horizontal_m and pair[0] != pair[1]:
                continue
            cost = sum(unary[v][pair[j]]+row_cost.get(v, 0)*(pair[j] != 0)
                       for j, v in enumerate(vertices))
            if cost < inf:
                options.append((pair, cost))
        nxt = {}; pred = {}
        for oldkey, oldcost in dp.items():
            previous, pending = oldkey
            for pair, cost in options:
                if any(previous is None or previous[columns.index(c)] != pair[columns.index(c)]
                       for c in lower_mask.get(r, [])):
                    continue
                if pending:
                    actions = [False] if pair == previous else []
                else:
                    actions = [True]+([False] if pair[0] == pair[1] else [])
                for newpending in actions:
                    key = pair, newpending; value = oldcost+cost
                    if value < nxt.get(key, inf):
                        nxt[key] = value; pred[key] = oldkey
        dp = nxt; history.append(pred)
    final = [(cost, key) for key, cost in dp.items() if not key[1]]
    if not final:
        return None
    best, key = min(final); labels = {}; matching = set()
    for j in range(len(rows)-1, -1, -1):
        r, columns = rows[j]; pair, newpending = key; oldkey = history[j][key]
        labels.update({(r, c): pair[k] for k, c in enumerate(columns)})
        if oldkey[1]:
            matching |= {edge((r-1, c), (r, c)) for c in columns}
        elif not newpending:
            matching.add(edge((r, columns[0]), (r, columns[1])))
        key = oldkey
    return dict(cost=best, labels=labels, auxiliary=matching)


def _forest_labels(h, w, m, t, cell_height=4, weights=None, feedback=None):
    """Minimize a physical same-colour labeling with fixed feedback colours.

    The partition has two-column strips cut at multiples of cell_height;
    the final row block may be shorter. An actual cross-cell M MULTIGRAPH
    becomes a forest after the specified feedback edges are removed from
    the message graph only. They still occupy vertices, impose equal colours,
    and incur their single actual edge cost. Coloured cycles may overprice
    this restricted branch; normalization is deferred to the global optimum.
    """
    if h < 1 or w < 2 or w % 2 or cell_height < 1:
        raise ValueError('Positive dimensions, even width, positive cell height required')
    board = grid(h, w); m = {edge(a, b) for a, b in m}; t = set(t); mm = mates(board, m)
    if not t <= board-mm.keys():
        raise ValueError('Selected terminals must be unoccupied board vertices')
    weights = {e: 1 for e in m} if weights is None else {edge(a, b): x for (a, b), x in weights.items()}
    if weights.keys() != m or any(type(x) is not int or x < 0 for x in weights.values()):
        raise ValueError('Exactly one nonnegative integer weight per actual M edge')
    cell = lambda v: (v[0]//cell_height, v[1]//2)
    feedback = {} if feedback is None else {edge(a, b): colour for (a, b), colour in feedback.items()}
    if not feedback.keys() <= m or any(colour not in range(3) for colour in feedback.values()):
        raise ValueError('Feedback colours require actual M edges and colours 0,1,2')
    if any(cell(a) == cell(b) for a, b in feedback):
        raise ValueError('Only cross-cell actual edges belong to a feedback set')
    cells = {}; internal = {}; adjacency = {}
    for r in range(h):
        for column in range(w):
            v = r, column; c = cell(v); cells.setdefault(c, []).append(v)
    for c in cells:
        internal[c] = []; adjacency[c] = []
    for e in m:
        a, b = e; ca, cb = cell(a), cell(b)
        if ca == cb:
            internal[ca].append(e)
        elif e not in feedback:
            adjacency[ca].append((cb, e, a, b)); adjacency[cb].append((ca, e, b, a))
    roots = []; parent = {}; order = []; children = {c: [] for c in cells}
    for start in cells:
        if start in parent:
            continue
        roots.append(start); parent[start] = None; todo = [start]
        while todo:
            c = todo.pop(); order.append(c)
            for nxt, e, v, z in adjacency[c]:
                if parent[c] is not None and e == parent[c][1]:
                    continue
                if nxt in parent:
                    raise ValueError('Actual cross-cell M multigraph has a cycle or parallel edges')
                parent[nxt] = (c, e, z, v); children[c].append((nxt, e, v, z)); todo.append(nxt)
    allowed = {}
    for v in board:
        if v in mm:
            allowed[v] = {0, 1, 2}
        elif v in t:
            allowed[v] = {1 if sum(v) % 2 == 0 else 2}
        else:
            allowed[v] = {0, 2 if sum(v) % 2 == 0 else 1}
    for e, colour in feedback.items():
        for v in e:
            allowed[v] = {colour}
    solutions = {}; messages = {}; final_cost = 0
    for c in reversed(order):
        vs = cells[c]; columns = [vs[0][1], vs[0][1]+1]; rs = range(vs[0][0], vs[-1][0]+1)
        rows = [(r, columns) for r in rs]
        unary = {v: [0, 0, 0] for v in vs}
        for child, _, v, _ in children[c]:
            unary[v] = [x+y for x, y in zip(unary[v], messages[child])]
        if parent[c] is None:
            local = local_optimum(rows, allowed, unary, internal[c], weights)
            if local is None:
                return None
            solutions[c] = {None: local}; final_cost += local['cost']
        else:
            _, e, v, _ = parent[c]; solutions[c] = {}; messages[c] = []
            for colour in range(3):
                local = local_optimum(rows, allowed, unary, internal[c], weights, (v, colour))
                solutions[c][colour] = local
                messages[c].append(inf if local is None else local['cost']+weights[e]*(colour != 0))
    labels = {}; n = set(); todo = [(r, None) for r in roots]
    while todo:
        c, colour = todo.pop(); local = solutions[c][colour]; assert local is not None
        labels.update(local['labels']); n |= local['auxiliary']
        for child, _, v, _ in children[c]:
            todo.append((child, local['labels'][v]))
    final_cost += sum(weights[e]*(colour != 0) for e, colour in feedback.items())
    state = physical_state(board, m, n, t)
    assert state['data']['counts'][0] == 0
    assert all(cell(a) == cell(b) for a, b in n)
    assert all(labels[a] == labels[b] for a, b in m | n)
    physical_cost = sum(weights[e] for e in state['paid'])
    assert physical_cost <= final_cost == sum(weights[e] for e in m if labels[e[0]] != 0)
    return dict(cost=final_cost, physical_cost=physical_cost, auxiliary=n, labels=labels, state=state,
                cells=len(cells), cross_edges=sum(len(a) for a in adjacency.values())//2,
                tree_components=len(roots), total_label_cost=final_cost)


def _normalize_optimum(result):
    if result is not None:
        # This equality holds at the unrestricted labeling optimum. It need
        # NOT hold in a fixed feedback-colour branch: an enforced coloured
        # P-only cycle is a genuine extra labeling charge in that branch.
        assert result['physical_cost'] == result['cost']
        for vertices, _ in result['state']['cycles']:
            for v in vertices:
                result['labels'][v] = 0
    return result


def solve(h, w, m, t, cell_height=4, weights=None):
    """Exact minimum physical fee for a forest; reject parallel/cyclic M graph."""
    return _normalize_optimum(_forest_labels(h, w, m, t, cell_height, weights))


def solve_cycle_rank(h, w, m, t, cell_height=4, weights=None, max_rank=None):
    """Exact physical cost in O(3**k * |V|) arithmetic operations.

    k is the cross-cell M MULTIGRAPH cycle rank. A feedback edge is removed
    only from tree messages, never from the actual matching or endpoint set.
    """
    if h < 1 or w < 2 or w % 2 or cell_height < 1:
        raise ValueError('Positive dimensions, even width, positive cell height required')
    m = {edge(a, b) for a, b in m}; t = set(t)
    cell = lambda v: (v[0]//cell_height, v[1]//2)
    cells = {cell(v) for v in grid(h, w)}; adjacency = {c: [] for c in cells}; feedback = []
    for e in {edge(a, b) for a, b in m}:
        a, b = e; ca, cb = cell(a), cell(b)
        if ca == cb:
            continue
        adjacency[ca].append((cb, e)); adjacency[cb].append((ca, e))
    seen_cells = set(); seen_edges = set()
    for root in cells:
        if root in seen_cells:
            continue
        seen_cells.add(root); todo = [root]
        while todo:
            c = todo.pop()
            for neighbour, e in adjacency[c]:
                if e in seen_edges:
                    continue
                seen_edges.add(e)
                if neighbour in seen_cells:
                    feedback.append(e)
                else:
                    seen_cells.add(neighbour); todo.append(neighbour)
    if max_rank is not None and len(feedback) > max_rank:
        raise ValueError('Explicit maximum cycle rank exceeded')
    best = None; branches = 0
    for colours in product(range(3), repeat=len(feedback)):
        result = _forest_labels(h, w, m, t, cell_height, weights, dict(zip(feedback, colours)))
        branches += 1
        if result is not None and (best is None or result['cost'] < best['cost']):
            best = result
    if best is not None:
        best['feedback_edges'] = feedback; best['cycle_rank'] = len(feedback); best['branches'] = branches
    return _normalize_optimum(best)
