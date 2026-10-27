"""A weighted Hall-style lower bound from capacity-one white HH sources.

Shortest T-to-black-Q distances are lower bounds, not independently
compatible routes. A maximum-discount matching gives each H source at
most one free terminal; shared actual paths are not selected as a certificate.
"""
import heapq
from check_residual_reserve_cost_profile import Network


def terminal_source_budget(board, directed, t, white_holes, black_terminals, arc_cost):
    distance = {v: 0 for v in t}; heap = [(0, v) for v in sorted(t)]
    heapq.heapify(heap)
    while heap:
        cost, v = heapq.heappop(heap)
        if cost != distance[v]: continue
        for z in directed[v]:
            candidate = cost+arc_cost.get((v, z), 0)
            if z not in distance or candidate < distance[z]:
                distance[z] = candidate; heapq.heappush(heap, (candidate, z))
    # A terminal unreachable from T must be HH, but assigning it zero lower
    # weight simply relaxes that mandatory use of an HH source. Safe, weaker.
    ell = {v: distance.get(v, 0) for v in black_terminals}
    positive = {v for v, cost in ell.items() if cost > 0}
    cap = max(ell.values(), default=0)
    net = Network(); source = ('budget_source',); sink = ('budget_sink',)
    net.nodes.update({source, sink}); links = {}; reachability = {}
    for h in sorted(white_holes):
        reach = {h}; todo = [h]
        while todo:
            for z in directed[todo.pop()]:
                if z not in reach: reach.add(z); todo.append(z)
        reachability[h] = reach & positive
        node = ('hole', h)
        net.add(source, node, 1); net.add(node, sink, 1, cap)
        for b in sorted(reachability[h]):
            links[h, b] = net.add(node, ('black', b), 1, cap-ell[b])
    for b in sorted(positive): net.add(('black', b), sink, 1)
    value = cost = 0
    while (extra := net.augment(source, sink)) is not None:
        value += 1; cost += extra
    assert value == len(white_holes)
    potential = net.potentials()
    matching = {pair for pair, index in links.items() if net.edges[index]['cap'] == 0}
    assert len({h for h, b in matching}) == len(matching) == len({b for h, b in matching})
    saving = sum(ell[b] for h, b in matching)
    assert saving == len(white_holes)*cap-cost
    lower = sum(ell.values())-saving; assert lower >= 0
    return dict(lower_bound=lower, terminal_lower_weights=ell, max_discount=saving,
                discount_matching=matching, reachable_discount_pairs=reachability,
                T_distances=distance, unreachable_from_T=set(black_terminals)-distance.keys(),
                potential=potential,
                residual_arcs=[(e['u'], e['v'], e['cap'], e['cost']) for e in net.edges if e['cap']])
