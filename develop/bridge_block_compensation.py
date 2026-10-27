"""Exact physical strip fees parameterized by the largest bridge-block rank.

Only colour-label costs are passed between blocks. Physical P-only cycles
are normalized after the complete global optimum, never inside a message.
"""
from itertools import product

from strip_tree_compensation import (
    edge, grid, mates, local_optimum, physical_state_linear, _normalize_optimum,
)


def bridge_partition(cells, adjacency):
    """Linear iterative bridge extraction; parent identity is an EDGE.

    Distinct parallel physical edges therefore prevent each other being
    bridges. A single parent-vertex comparison would be incorrect here.
    """
    entered = {}; low = {}; parent = {}; bridges = set(); clock = 0
    for root in cells:
        if root in entered:
            continue
        entered[root] = low[root] = clock; clock += 1; parent[root] = None
        stack = [(root, iter(adjacency[root]))]
        while stack:
            c, neighbours = stack[-1]
            try:
                nxt, e, _, _ = next(neighbours)
            except StopIteration:
                stack.pop()
                if parent[c] is not None:
                    up, e = parent[c]
                    if low[c] > entered[up]:
                        bridges.add(e)
                    low[up] = min(low[up], low[c])
                continue
            if parent[c] is not None and e == parent[c][1]:
                continue
            if nxt in entered:
                low[c] = min(low[c], entered[nxt])
            else:
                parent[nxt] = (c, e); entered[nxt] = low[nxt] = clock; clock += 1
                stack.append((nxt, iter(adjacency[nxt])))
    owner = {}; blocks = []
    for root in cells:
        if root in owner:
            continue
        bid = len(blocks); members = []; owner[root] = bid; todo = [root]
        while todo:
            c = todo.pop(); members.append(c)
            for nxt, e, _, _ in adjacency[c]:
                if e not in bridges and nxt not in owner:
                    owner[nxt] = bid; todo.append(nxt)
        blocks.append(members)
    return bridges, owner, blocks


def _block_plan(members, adjacency, bridges):
    """Choose the block's spanning tree and distinct feedback actual edges."""
    root = members[0]; parent = {root: None}; order = []; todo = [root]
    children = {c: [] for c in members}; feedback = []; used = set()
    while todo:
        c = todo.pop(); order.append(c)
        for nxt, e, v, z in adjacency[c]:
            if e in bridges or e in used:
                continue
            used.add(e)
            if nxt in parent:
                feedback.append(e)
            else:
                parent[nxt] = (c, e, z, v); children[c].append((nxt, e, v, z)); todo.append(nxt)
    assert len(order) == len(members)
    assert len(feedback) == len(used)-len(members)+1
    return root, parent, order, children, feedback


def _region_labels(plan, cells, internal, allowed, weights, boundary_cost, pins):
    """Forest colour optimization on a union of cells, with unary boundary fees.

    Boundary endpoints remain occupied as determined by the GLOBAL matching.
    A bridge is absent only from this message graph, not from the footprint.
    """
    root, parent, order, children, _ = plan
    solutions = {}; messages = {}
    for c in reversed(order):
        rows, vs = cells[c]
        unary = {v: list(boundary_cost.get(v, (0, 0, 0))) for v in vs}
        local_allowed = {v: {pins[v]} if v in pins else allowed[v] for v in vs}
        for child, _, v, _ in children[c]:
            unary[v] = [None if x is None or y is None else x+y
                        for x, y in zip(unary[v], messages[child])]
        if parent[c] is None:
            local = local_optimum(rows, local_allowed, unary, internal[c], weights)
            if local is None:
                return None
            solutions[c] = {None: local}; best = local['cost']
        else:
            _, e, v, _ = parent[c]; solutions[c] = {}; messages[c] = []
            for colour in range(3):
                local = local_optimum(rows, local_allowed, unary, internal[c], weights, (v, colour))
                solutions[c][colour] = local
                messages[c].append(None if local is None else local['cost']+weights[e]*(colour != 0))
    labels = {}; n = set(); todo = [(root, None)]
    while todo:
        c, colour = todo.pop(); local = solutions[c][colour]; assert local is not None
        labels.update(local['labels']); n.update(local['auxiliary'])
        for child, _, v, _ in children[c]:
            todo.append((child, local['labels'][v]))
    return dict(cost=best, labels=labels, auxiliary=n)


def solve_bridge_blocks(h, w, m, t, cell_height=4, weights=None, max_block_rank=None):
    """O(sum_B 3**rank(B) |V_B|) arithmetic operations, O(|V|) storage.

    B ranges over components after ALL bridges are deleted from the actual-M
    cell multigraph. Global cycle rank may be unbounded even if each B has
    rank one. The count is unaffected by parallel edges or free doubled cycles.
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
    cells = {}
    for r in range(0, h, cell_height):
        for c in range(0, w, 2):
            rows = [(rr, [c, c+1]) for rr in range(r, min(r+cell_height, h))]
            vs = [(rr, cc) for rr, columns in rows for cc in columns]
            cells[cell((r, c))] = rows, vs
    internal = {c: [] for c in cells}; adjacency = {c: [] for c in cells}
    for e in m:
        a, b = e; ca, cb = cell(a), cell(b)
        if ca == cb:
            internal[ca].append(e)
        else:
            adjacency[ca].append((cb, e, a, b)); adjacency[cb].append((ca, e, b, a))
    bridges, owner, blocks = bridge_partition(cells, adjacency)
    plans = [_block_plan(members, adjacency, bridges) for members in blocks]
    ranks = [len(plan[-1]) for plan in plans]
    if max_block_rank is not None and max(ranks) > max_block_rank:
        raise ValueError('Explicit maximum bridge-block cycle rank exceeded')
    b_adj = {b: [] for b in range(len(blocks))}
    for e in bridges:
        a, b = e; ba, bb = owner[cell(a)], owner[cell(b)]
        b_adj[ba].append((bb, e, a, b)); b_adj[bb].append((ba, e, b, a))
    roots = []; parent = {}; order = []; children = {b: [] for b in b_adj}
    for root in b_adj:
        if root in parent:
            continue
        parent[root] = None; roots.append(root); todo = [root]
        while todo:
            b = todo.pop(); order.append(b)
            for nxt, e, v, z in b_adj[b]:
                if nxt in parent:
                    continue
                parent[nxt] = (b, e, z, v); children[b].append((nxt, e, v, z)); todo.append(nxt)
    allowed = {v: ({0, 1, 2} if v in mm else
                   {1 if sum(v) % 2 == 0 else 2} if v in t else
                   {0, 2 if sum(v) % 2 == 0 else 1}) for v in board}
    solutions = {}; messages = {}; branch_evaluations = 0
    for bid in reversed(order):
        boundary = {v: messages[child] for child, _, v, _ in children[bid]}
        conditions = [None] if parent[bid] is None else range(3)
        solutions[bid] = {}; messages[bid] = []
        for condition in conditions:
            parent_pins = {} if condition is None else {parent[bid][2]: condition}
            best = None
            for colours in product(range(3), repeat=ranks[bid]):
                pins = dict(parent_pins); extra = 0
                for e, colour in zip(plans[bid][-1], colours):
                    for v in e:
                        pins[v] = colour
                    extra += weights[e]*(colour != 0)
                result = _region_labels(plans[bid], cells, internal, allowed, weights, boundary, pins)
                branch_evaluations += 1
                if result is not None:
                    result['cost'] += extra
                    if best is None or result['cost'] < best['cost']:
                        best = result
            solutions[bid][condition] = best
            if condition is not None:
                e = parent[bid][1]
                messages[bid].append(None if best is None else best['cost']+weights[e]*(condition != 0))
        if parent[bid] is None and solutions[bid][None] is None:
            return None
    labels = {}; n = set(); todo = [(r, None) for r in roots]
    final_cost = sum(solutions[r][None]['cost'] for r in roots)
    while todo:
        bid, colour = todo.pop(); result = solutions[bid][colour]; assert result is not None
        labels.update(result['labels']); n.update(result['auxiliary'])
        for child, _, v, _ in children[bid]:
            todo.append((child, result['labels'][v]))
    state = physical_state_linear(board, m, n, t)
    assert state['data']['counts'][0] == 0
    assert all(labels[a] == labels[b] for a, b in m | n)
    assert all(cell(a) == cell(b) for a, b in n)
    assert final_cost == sum(weights[e] for e in m if labels[e[0]] != 0)
    physical_cost = sum(weights[e] for e in state['paid'])
    return _normalize_optimum(dict(cost=final_cost, physical_cost=physical_cost,
        labels=labels, auxiliary=n, state=state, cells=len(cells),
        bridge_edges=len(bridges), blocks=len(blocks), block_cycle_ranks=ranks,
        cycle_rank=sum(ranks), max_block_cycle_rank=max(ranks),
        branch_evaluations=branch_evaluations))
