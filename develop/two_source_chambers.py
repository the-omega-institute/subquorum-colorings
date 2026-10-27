"""Two isolated-hole squares separated by a two-column Q strip."""
from check_unbounded_hole_relay import family as isolated_core
from strip_tree_compensation import edge, grid


def two_source_chambers(k):
    if type(k) is not int or k < 1: raise ValueError('Positive integer k required')
    f = isolated_core(k); n = f['n']; shift = n+2
    move = lambda v: (v[0], v[1]+shift)
    move_e = lambda e: edge(move(e[0]), move(e[1]))
    first_m = set(f['M']); second_m = {move_e(e) for e in first_m}
    m = first_m | second_m; t = set(f['T']); board = grid(n, 2*n+2)
    relay_m = {edge(f['long_path'][i], f['long_path'][i+1])
               for i in range(1, len(f['long_path'])-1, 2)}
    first_n = first_m-relay_m
    for path in f['paths']:
        first_n.update(edge(path[i], path[i+1]) for i in range(0, len(path)-1, 2))
    n_full = first_n | {move_e(e) for e in first_n}
    n_full.update(edge((r, n), (r, n+1)) for r in range(n))
    return dict(height=n, width=2*n+2, board=board, M=m, T=t,
                first_M=first_m, second_M=second_m, auxiliary=n_full,
                TH_paid=relay_m, HH_actual={move_e(e) for e in relay_m},
                first_hole=f['h'], second_hole=move(f['h']),
                exact_TH_fee=k, exact_all_terminal_cost=2*k)
