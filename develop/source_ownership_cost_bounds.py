"""Physical source-ownership bounds; exact when positive source basins separate.

Both optimizers route every Q terminal and share each actual edge once.
The costs bracket TH expense, not the original all-terminal objective.
"""
from collections import deque
from strip_tree_compensation import edge, grid, mates
from check_mixed_terminal_compensation import neighbours
from monochromatic_completion_flow import solve_completion_flow
from terminal_source_budget import terminal_source_budget


def source_ownership_bounds(h, w, m, t, weights=None):
    if any(type(x) is not int or x < 1 for x in (h, w)) or h*w % 2:
        raise ValueError('Positive dimensions and even rectangular area required')
    board = grid(h, w); m = {edge(a, b) for a, b in m}; t = set(t)
    mm = mates(board, m); p = set(mm); q = board-p
    if not t <= q or len({sum(v) % 2 for v in t}) > 1:
        raise ValueError('T must be an unoccupied monochromatic set')
    colour = sum(next(iter(t))) % 2 if t else 1
    starts = {v for v in q if sum(v) % 2 == colour}
    weights = {e: 1 for e in m} if weights is None else {edge(a, b): c for (a, b), c in weights.items()}
    if weights.keys() != m or any(type(c) is not int or c < 0 for c in weights.values()):
        raise ValueError('Exactly one nonnegative integer weight per actual edge required')
    directed = {v: [] for v in board}; tails = {}
    for e in m:
        a, b = e
        if sum(a) % 2 == colour: a, b = b, a
        directed[a].append(b); tails[e] = a
    for a in board:
        if sum(a) % 2 != colour: continue
        for b in neighbours(a) & board:
            if edge(a, b) not in m: directed[a].append(b)

    original_arcs = {(a, b) for a, vs in directed.items() for b in vs}
    def reachable(sources, arcs):
        out = {v: [] for v in board}
        for a, b in sorted(arcs): out[a].append(b)
        reach = set(sources); todo = deque(sorted(reach))
        while todo:
            for v in out[todo.popleft()]:
                if v not in reach: reach.add(v); todo.append(v)
        return reach

    rt = reachable(t, original_arcs); rh = reachable(starts-t, original_arcs)
    ambiguous = {e for e in m if tails[e] in rt & rh}
    exclusive_t = {e for e in m if tails[e] in rt-rh}
    exclusive_h = {e for e in m if tails[e] in rh-rt}
    unreachable = m-ambiguous-exclusive_t-exclusive_h
    lower_weights = {e: weights[e] if e in exclusive_t else 0 for e in m}
    upper_weights = {e: weights[e] if tails[e] in rt else 0 for e in m}
    low = solve_completion_flow(h, w, m, t, lower_weights)
    high = solve_completion_flow(h, w, m, t, upper_weights)
    lower = low['all_terminal_cost']; upper = high['all_terminal_cost']
    low_fee = sum(weights[e] for e in low['state']['paid'])
    high_fee = sum(weights[e] for e in high['state']['paid'])
    best = low if low_fee <= high_fee else high
    fee = min(low_fee, high_fee); ambiguity_weight = sum(weights[e] for e in ambiguous)
    assert lower <= fee <= high_fee <= upper <= lower+ambiguity_weight
    budget = terminal_source_budget(board, directed, t, starts-t, q-starts,
                                    {(tails[e], mm[tails[e]]): weights[e] for e in m})
    combined_lower = max(lower, budget['lower_bound'])
    assert combined_lower <= fee
    separated = ambiguity_weight == 0
    if separated: assert lower == low_fee == high_fee == upper
    return dict(auxiliary=best['auxiliary'], state=best['state'], weights=weights,
                source_colour=colour, T_reach=rt, H_reach=rh,
                ambiguous=ambiguous, exclusive_T=exclusive_t, exclusive_H=exclusive_h,
                unreachable=unreachable, ambiguity_weight=ambiguity_weight,
                lower_bound=lower, static_upper_bound=upper, TH_fee=fee,
                exactness_certified=(fee == combined_lower), source_separated=separated,
                combined_lower_bound=combined_lower, source_budget=budget,
                lower_flow=low, upper_flow=high,
                lower_candidate_fee=low_fee, upper_candidate_fee=high_fee)
