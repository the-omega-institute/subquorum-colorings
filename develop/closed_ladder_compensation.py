"""Construct zero-actual-edge-fee certificates on matching-closed ladders.

The sole residual case is the full odd alternating TT/HH pattern. The
construction uses disjoint column pairs, not a scalar resource relaxation.
"""
from strip_tree_compensation import edge, grid, mates, physical_state_linear
from check_mixed_terminal_compensation import neighbours


def _check_selection(board, p, t):
    if not t <= board-p:
        raise ValueError('A feasible selected set disjoint from actual M is required')
    # Build this union ONCE. The older finite-enumeration helper rebuilds it
    # for each selected vertex and is not suitable for this linear constructor.
    occupied = p | t
    if any(sum(z in occupied for z in neighbours(v)) > 1 for v in t):
        raise ValueError('A feasible selected set disjoint from actual M is required')


def construct_ladder(width, m, t):
    """Return an exact minimum-(TT, TH fee) witness on a feasible 2 x width.

    Every TH component is one auxiliary edge, so the paid actual edge set
    is empty for every nonnegative weighting. Column processing and the
    final tagged component traversal use O(width) operations and storage.
    """
    if type(width) is not int or width < 1:
        raise ValueError('Positive integer width required')
    board = grid(2, width); m = {edge(a, b) for a, b in m}; t = set(t)
    mm = mates(board, m); p = set(mm)
    _check_selection(board, p, t)
    labels = {v: ('P' if v in p else 'T' if v in t else 'H') for v in board}
    columns = [tuple(labels[r, c] for r in range(2)) for c in range(width)]
    used = set(); auxiliary = set(); blocks = []; unmatched_tt = []

    def pair(c, d, kind):
        assert abs(c-d) == 1 and c not in used and d not in used
        used.update((c, d))
        auxiliary.update(edge((r, c), (r, d)) for r in range(2))
        blocks.append(dict(columns=(c, d), kind=kind))

    # Every TP column has a forced PH mate. The injection makes these
    # two-column blocks disjoint and closes their two P endpoints under M.
    for c, column in enumerate(columns):
        if set(column) != {'T', 'P'}:
            continue
        r = column.index('P'); partner = mm[r, c]; d = partner[1]
        assert partner[0] == r and columns[d][r] == 'P'
        assert columns[d][1-r] == 'H'
        pair(c, d, 'TP-PH')

    # Scan each TT/HH alternating component left to right. Prefer a free
    # left HH; a component starting with TT is paired to the right instead.
    # An unmatched final TT can occur only in the full odd exceptional word.
    for c, column in enumerate(columns):
        if column != ('T', 'T'):
            continue
        if c > 0 and columns[c-1] == ('H', 'H') and c-1 not in used:
            pair(c, c-1, 'TT-HH')
        elif c+1 < width and columns[c+1] == ('H', 'H') and c+1 not in used:
            pair(c, c+1, 'TT-HH')
        else:
            unmatched_tt.append(c)
    exceptional = width % 2 == 1 and all(
        column == (('T', 'T') if c % 2 == 0 else ('H', 'H'))
        for c, column in enumerate(columns))
    assert len(unmatched_tt) == int(exceptional)
    for c in range(width):
        if c not in used:
            auxiliary.add(edge((0, c), (1, c)))
    state = physical_state_linear(board, m, auxiliary, t)
    assert state['data']['counts'][0] == int(exceptional)
    assert not state['paid']
    assert all(len(path['N']) == 1 and not path['M']
               for path in state['data']['paths'] if path['kind'] == 'TH')
    return dict(auxiliary=auxiliary, state=state, blocks=blocks,
                exceptional=exceptional, minimum_TT=int(exceptional), TH_cost=0,
                full_coverage=not exceptional, unmatched_TT_columns=unmatched_tt)


def construct_closed_bands(height, width, m, t):
    """Combine ladders on an even x even board with no actual seam edge.

    Seams are between rows 2j+1 and 2j+2 (zero based). An actual edge crossing
    any such seam is rejected, rather than deleted or treated as a free hole.
    """
    if any(type(x) is not int or x < 2 or x % 2 for x in (height, width)):
        raise ValueError('Positive even height and width required')
    board = grid(height, width); m = {edge(a, b) for a, b in m}; t = set(t)
    mm = mates(board, m); p = set(mm)
    _check_selection(board, p, t)
    if any(a[0]//2 != b[0]//2 for a, b in m):
        raise ValueError('Actual M must be closed inside each two-row band')
    per_m = [set() for _ in range(height//2)]
    per_t = [set() for _ in range(height//2)]
    for a, b in m:
        band = a[0]//2; offset = 2*band
        per_m[band].add(edge((a[0]-offset, a[1]), (b[0]-offset, b[1])))
    for r, c in t:
        per_t[r//2].add((r % 2, c))
    auxiliary = set()
    for j, (local_m, local_t) in enumerate(zip(per_m, per_t)):
        local = construct_ladder(width, local_m, local_t)
        auxiliary.update(edge((a[0]+2*j, a[1]), (b[0]+2*j, b[1]))
                         for a, b in local['auxiliary'])
    state = physical_state_linear(board, m, auxiliary, t)
    assert state['data']['counts'][0] == 0 and not state['paid']
    assert all(len(path['N']) == 1 and not path['M']
               for path in state['data']['paths'] if path['kind'] == 'TH')
    return dict(auxiliary=auxiliary, state=state, minimum_TT=0, TH_cost=0,
                full_coverage=True)
