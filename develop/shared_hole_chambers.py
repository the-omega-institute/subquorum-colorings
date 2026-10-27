"""Feasible near-half-area family: every C-minimizer can overpay TH unboundedly."""
from check_unbounded_hole_relay import family as isolated_core
from strip_tree_compensation import edge, grid


def _complete_core(core, relay):
    m = set(core['M'])
    actual = {edge(relay[i], relay[i+1]) for i in range(1, len(relay)-1, 2)}
    assert actual <= m
    n = m-actual
    n.update(edge(relay[i], relay[i+1]) for i in range(0, len(relay)-1, 2))
    index = core['line'].index(relay[0]); assert index % 2 == 0
    for segment in (core['line'][:index], core['line'][index+1:]):
        assert len(segment) % 2 == 0
        n.update(edge(segment[i], segment[i+1]) for i in range(0, len(segment), 2))
    return n, actual


def shared_hole_chambers(k, short=None):
    short = k if short is None else short
    if any(type(x) is not int or x < 1 for x in (k, short)) or short > k:
        raise ValueError('Integers k>=short>=1 required')
    first = isolated_core(k); second = isolated_core(short); n = first['n']
    height = 4*k+4*short+2; width = height+2
    move = lambda v: (v[0]+4*k, v[1]+n)
    move_e = lambda e: edge(move(e[0]), move(e[1]))
    first_m = set(first['M']); second_m = {move_e(e) for e in second['M']}; m = first_m | second_m
    p = {v for e in m for v in e}; board = grid(height, width)
    z = (4*k, 4*k+1); t = {v for v in board-p if sum(v) % 2}-{z}
    first_straight, first_actual = _complete_core(first, first['long_path'])
    second_straight, second_actual = _complete_core(second, second['long_path'])
    # L-shaped corner relay: 2k actual edges, starts at the unique white H.
    corner = [z]+[(r, 4*k) for r in range(4*k, 2*k-1, -1)]
    corner += [(2*k, c) for c in range(4*k-1, 2*k-1, -1)]
    corner_n, corner_actual = _complete_core(first, corner)
    outside = set()
    for r in range(height):
        if r < 4*k: columns = range(n, width, 2)
        elif r < n: columns = ()
        else: columns = range(0, n, 2)
        outside.update(edge((r, c), (r, c+1)) for c in columns)
    all_terminal_auxiliary = first_straight | {move_e(e) for e in second_straight} | outside
    true_TH_auxiliary = corner_n | {move_e(e) for e in second_straight} | outside
    return dict(k=k, short=short, height=height, width=width, board=board, M=m, P=p, T=t,
                H=board-p-t, white_hole=z, centres={first['h'], move(second['h'])},
                first_centre=first['h'], second_centre=move(second['h']),
                true_TH_auxiliary=true_TH_auxiliary,
                all_terminal_auxiliary=all_terminal_auxiliary,
                true_TH_paid={move_e(e) for e in second_actual},
                free_HH_actual=corner_actual, corner_relay=corner,
                exact_TH_fee=short, exact_all_terminal_cost=k+short,
                every_all_terminal_minimizer_TH_fee=k+short)
