"""Whole-board Hall test for full coverage with an empty paid actual edge set.

This is a standard bipartite matching adapter. It does not optimize positive
TH fees. The delivered augmenting-path implementation uses O(|V||E|) time.
"""
from collections import deque
from strip_tree_compensation import edge, grid, mates, physical_state_linear
from check_mixed_terminal_compensation import neighbours


def zero_fee_extension(h, w, m, t):
    if any(type(x) is not int or x < 1 for x in (h, w)) or h*w % 2:
        raise ValueError('Positive rectangular dimensions and even area required')
    board = grid(h, w); m = {edge(a, b) for a, b in m}; t = set(t)
    p = set(mates(board, m))
    if not t <= board-p:
        raise ValueError('Selected vertices must be unoccupied board vertices')
    holes = board-p-t
    black = sorted(v for v in board if sum(v) % 2 == 0)

    def allowed(a, b):
        return (a not in t or b in holes) and (b not in t or a in holes)

    adj = {v: sorted(z for z in neighbours(v) & board if allowed(v, z)) for v in black}
    left_mate = {}; right_mate = {}
    for start in black:
        if start in left_mate:
            continue
        queue = deque([start]); seen = {start}; parent = {}; end = None
        while queue and end is None:
            v = queue.popleft()
            for z in adj[v]:
                if z in parent:
                    continue
                parent[z] = v
                if z not in right_mate:
                    end = z
                    break
                other = right_mate[z]
                if other not in seen:
                    seen.add(other); queue.append(other)
        if end is not None:
            while True:
                v = parent[end]; previous = left_mate.get(v)
                left_mate[v] = end; right_mate[end] = v
                if previous is None:
                    break
                end = previous
    matching = {edge(v, z) for v, z in left_mate.items()}
    # Alternating reachability from unmatched black vertices exposes a
    # canonical maximum-deficiency Hall set, including when its defect is 0.
    hall_black = set(black)-left_mate.keys(); hall_white = set()
    queue = deque(hall_black)
    while queue:
        v = queue.popleft()
        for z in adj[v]:
            if z in hall_white:
                continue
            hall_white.add(z)
            assert z in right_mate, 'An augmenting path remains'
            other = right_mate[z]
            if other not in hall_black:
                hall_black.add(other); queue.append(other)
    defect = len(black)-len(matching)
    assert len(hall_black)-len(hall_white) == defect
    assert {z for v in hall_black for z in adj[v]} == hall_white
    state = None
    if defect == 0:
        state = physical_state_linear(board, m, matching, t)
        assert state['data']['counts'][0] == 0 and not state['paid']
    return dict(defect=defect, maximum_matching=matching, hall_black=hall_black,
                hall_white=hall_white, empty_paid_full_coverage_exists=defect == 0,
                state=state)


def extension_obstacle(h, w, weights=None):
    """All even h,w>=4: direct Hall defect 0, whole-board defect 1.

    J=hw/2-1. The exact unrestricted lexicographic fee is min of the two
    northwest core weights, under any nonnegative actual-edge weighting.
    """
    if any(type(x) is not int or x < 4 or x % 2 for x in (h, w)):
        raise ValueError('Even dimensions at least four required')
    top = edge((0, 1), (0, 2)); left = edge((1, 0), (2, 0))
    right = edge((2, 3), (3, 3)); m = {top, left, right}
    t = {(0, 3), (1, 2), (2, 1), (3, 0)}
    direct = {edge((0, 3), (1, 3)), edge((1, 2), (1, 1)),
              edge((2, 1), (2, 2)), edge((3, 0), (3, 1))}
    extra_n = set()
    # Two-column additions to the top four rows: HT/TH over two PP rows.
    for c in range(4, w, 2):
        m.update(edge((r, c), (r, c+1)) for r in (2, 3))
        t.update(((0, c+1), (1, c)))
        direct.update((edge((0, c), (0, c+1)), edge((1, c), (1, c+1))))
        extra_n.update(edge((r, c), (r, c+1)) for r in range(4))
    # Two-row additions: HT/TH in columns0,1; matched P elsewhere.
    for r in range(4, h, 2):
        m.update((edge((r, 2), (r+1, 2)), edge((r, 3), (r+1, 3))))
        t.update(((r, 1), (r+1, 0)))
        direct.update((edge((r, 0), (r, 1)), edge((r+1, 0), (r+1, 1))))
        extra_n.update((edge((r, 0), (r, 1)), edge((r+1, 0), (r+1, 1)),
                        edge((r, 2), (r+1, 2)), edge((r, 3), (r+1, 3))))
        for rr in (r, r+1):
            for c in range(4, w, 2):
                e = edge((rr, c), (rr, c+1)); m.add(e); extra_n.add(e)
    pay_top = {edge(a, b) for a, b in [((0, 3), (0, 2)), ((0, 1), (0, 0)),
                ((1, 2), (1, 3)), ((2, 1), (1, 1)), ((3, 0), (3, 1)),
                ((3, 2), (2, 2)), ((1, 0), (2, 0)), ((2, 3), (3, 3))]}
    pay_left = {edge(a, b) for a, b in [((3, 0), (2, 0)), ((1, 0), (0, 0)),
                 ((0, 3), (1, 3)), ((1, 2), (1, 1)), ((2, 1), (3, 1)),
                 ((2, 2), (3, 2)), ((2, 3), (3, 3)), ((0, 1), (0, 2))]}
    weights = {e: 1 for e in m} if weights is None else weights
    if weights.keys() != m or any(x < 0 for x in weights.values()):
        raise ValueError('One nonnegative weight per actual edge required')
    use_top = weights[top] <= weights[left]
    return dict(h=h, w=w, M=m, T=t, direct_matching=direct,
                core_top=top, core_left=left, core_right=right,
                auxiliary=(pay_top if use_top else pay_left) | extra_n,
                exact_fee=min(weights[top], weights[left]), weights=weights,
                hall_set={(0, 0), (0, 2), (2, 0)},
                hall_neighbours={(0, 1), (1, 0)})
