"""Complete physical routing for one-colour selections, using standard min-cost flow.

Reuse the existing exact-integer residual solver. All terminals, including
same-colour holes, must be routed. Costs count M on BOTH TH and HH paths;
this equals TH expense under the stated zero-weight HH reachability condition.
"""
from collections import deque
from strip_tree_compensation import edge, grid, mates, physical_state_linear
from check_mixed_terminal_compensation import neighbours
from check_residual_reserve_cost_profile import Network


def solve_completion_flow(h, w, m, t, weights=None):
    if any(type(x) is not int or x < 1 for x in (h, w)) or h*w % 2:
        raise ValueError('Positive rectangular dimensions and even area required')
    board = grid(h, w); m = {edge(a, b) for a, b in m}; t = set(t)
    mm = mates(board, m); p = set(mm); q = board-p
    if not t <= q or len({sum(v) % 2 for v in t}) > 1:
        raise ValueError('T must consist of unoccupied vertices of one checkerboard colour')
    colour = sum(next(iter(t))) % 2 if t else 1
    starts = {v for v in q if sum(v) % 2 == colour}; ends = q-starts
    weights = {e: 1 for e in m} if weights is None else {edge(a, b): c for (a, b), c in weights.items()}
    if weights.keys() != m or any(type(c) is not int or c < 0 for c in weights.values()):
        raise ValueError('Exactly one nonnegative integer weight per actual edge required')
    net = Network(); source = ('source',); sink = ('sink',)
    net.nodes.update(board | {source, sink})
    for v in sorted(starts): net.add(source, v, 1, tag=('source', v))
    for v in sorted(ends): net.add(v, sink, 1, tag=('sink', v))
    internal = {}; directed = {v: [] for v in board}
    for e in sorted(m):
        a, b = e
        if sum(a) % 2 == colour: a, b = b, a
        internal[e] = net.add(a, b, 1, weights[e], ('M', e))
        directed[a].append(b)
    for a in sorted(board):
        if sum(a) % 2 != colour: continue
        for b in sorted(neighbours(a) & board):
            e = edge(a, b)
            if e not in m:
                net.add(a, b, 1, tag=('N', e)); directed[a].append(b)
    # A sufficient exactness condition: no HH source can traverse a positive
    # actual edge. Ordinary directed reachability ignores shared capacities.
    reach = set(starts-t); todo = deque(reach)
    while todo:
        for v in directed[todo.popleft()]:
            if v not in reach: reach.add(v); todo.append(v)
    exact = all(weights[e] == 0 or net.edges[i]['u'] not in reach for e, i in internal.items())
    value = cost = 0
    while (extra := net.augment(source, sink)) is not None:
        value += 1; cost += extra
    assert value == len(starts) == len(ends), 'Ambient full matching implies complete routing'
    potential = net.potentials()  # Nonnegative residual reduced costs certify fixed-value optimality.
    used = [e for e in net.edges[::2] if e['initial'] > e['cap']]
    successor = {}
    for e in used:
        if e['u'] == source or e['v'] == sink: continue
        assert e['u'] not in successor
        successor[e['u']] = e
    n = set(); path_m = set(); visited = set()
    for start in sorted(starts):
        v = start
        while v not in ends:
            assert v not in visited; visited.add(v)
            e = successor[v]
            if e['tag'][0] == 'N': n.add(e['tag'][1])
            else: path_m.add(e['tag'][1])
            v = e['v']
        assert v not in visited; visited.add(v)
    cycle_m = {e for e, i in internal.items() if net.edges[i]['cap'] == 0}-path_m
    assert sum(weights[e] for e in cycle_m) == 0
    n.update(m-path_m)  # Double all unused M; discard zero-cost flow circulations.
    state = physical_state_linear(board, m, n, t)
    assert state['data']['counts'][0] == 0
    all_path_m = set().union(set(), *(path['M'] for path in state['data']['paths']))
    assert all_path_m == path_m
    fee = sum(weights[e] for e in state['paid'])
    assert sum(weights[e] for e in all_path_m) == cost and fee <= cost
    if exact: assert fee == cost
    certificate = [(e['u'], e['v'], e['cap'], e['cost']) for e in net.edges if e['cap']]
    return dict(auxiliary=n, state=state, value=value, all_terminal_cost=cost,
                TH_fee=fee, TH_exactness_certified=exact, same_colour_hole_reach=reach,
                source_colour=colour, weights=weights,
                potential=potential, residual_arcs=certificate,
                node_count=len(net.nodes), directed_arc_count=len(net.edges)//2)
