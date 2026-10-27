"""New d=0, delta_0=1 family; reuse the established isolated-hole core."""
from check_unbounded_hole_relay import family as isolated_core
from strip_tree_compensation import edge, grid


def long_extension_obstacle(k):
    if type(k) is not int or k < 1: raise ValueError('Positive integer k required')
    core = isolated_core(k); n = core['n']; side = n+2
    board = grid(side, side); m = set(core['M']); p = core['P']
    q = board-p; white_hole = (0, side-1)
    t = {v for v in q if sum(v) % 2 == 1}-{white_hole}
    # Direct matching covers every T but leaves h and the remote white H.
    line = core['line']; direct = {edge(line[i], line[i+1]) for i in range(1, len(line), 2)}
    direct.add(edge(line[0], (0, n)))
    direct.update(edge((r, n), (r, n+1)) for r in range(1, n))
    direct.update(edge((n, c), (n+1, c)) for c in range(side))
    # A full N attains cost k: the inherited long TH plus all old direct
    # payments; newly added cells are paired without using actual M.
    long_m = {edge(core['long_path'][i], core['long_path'][i+1])
              for i in range(1, len(core['long_path'])-1, 2)}
    auxiliary = m-long_m
    for path in core['paths']:
        auxiliary.update(edge(path[i], path[i+1]) for i in range(0, len(path)-1, 2))
    auxiliary.update(edge((r, n), (r, n+1)) for r in range(n))
    auxiliary.update(edge((n, c), (n+1, c)) for c in range(side))
    hall_black = {v for v in grid(n-1, n-1) if sum(v) % 2 == 0}
    hall_white = grid(n-1, n-1)-hall_black
    return dict(k=k, side=side, board=board, M=m, P=p, T=t, H=q-t,
                centre=core['h'], white_hole=white_hole, direct=direct,
                auxiliary=auxiliary, paid=long_m, hall_black=hall_black,
                hall_white=hall_white, exact_fee=k, core=core)


def free_hh_relay_obstacle(k):
    """All-terminal cost k but true TH optimum 0, with T nonempty."""
    if type(k) is not int or k < 1: raise ValueError('Positive integer k required')
    core=isolated_core(k); m=set(core['M']); white_hole=core['long_path'][0]
    t=core['T']-{white_hole}
    path_m={edge(core['long_path'][i],core['long_path'][i+1])
            for i in range(1,len(core['long_path'])-1,2)}
    auxiliary=m-path_m
    for path in core['paths']:
        auxiliary.update(edge(path[i],path[i+1]) for i in range(0,len(path)-1,2))
    return dict(k=k, side=core['n'], M=m, T=t, P=core['P'], board=core['board'],
                white_hole=white_hole, auxiliary=auxiliary, all_terminal_cost=k,
                exact_TH_fee=0, core=core)
