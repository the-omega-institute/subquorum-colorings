"""Exact TH expense by binary component labels and a grid frontier DP.

No connectivity partitions are needed: labels are equal along M and chosen N.
Only nonnegative integer actual-edge weights are supported.  The exponential
parameter is the shorter bounding-box side, not the total number of vertices.
"""


def pair(a, b):
    return tuple(sorted((a, b)))


def adjacent(a, b):
    return abs(a[0]-b[0])+abs(a[1]-b[1]) == 1


def prepare(board, actual, selected, weights=None, retained=()):
    """Validate inputs and remove complete, disjoint retained terminal paths."""
    board, selected = set(board), set(selected)
    if any(not isinstance(v, tuple) or len(v) != 2 or
           any(type(x) is not int for x in v) for v in board):
        raise ValueError('Grid vertices must be pairs of integers')
    if not selected <= board or any(sum(v) % 2 != 1 for v in selected):
        raise ValueError('Selected vertices must be white board vertices')
    if 2*sum(sum(v) % 2 for v in board) != len(board):
        raise ValueError('Balanced grid board required')
    actual = {pair(*e) for e in actual}
    if any(not set(e) <= board or not adjacent(*e) for e in actual):
        raise ValueError('Actual edges must be board edges')
    mate = {v: w for e in actual for v, w in (e, e[::-1])}
    if len(mate) != 2*len(actual) or selected & mate.keys():
        raise ValueError('Actual matching and selected terminals must be disjoint')
    weights = ({e: 1 for e in actual} if weights is None else
               {pair(*e): w for e, w in weights.items()})
    if weights.keys() != actual or any(type(w) is not int or w < 0 for w in weights.values()):
        raise ValueError('Require an exact nonnegative integer weight per actual edge')
    q = board-mate.keys()
    removed, fixed_n, fixed_labels, expense = set(), set(), {}, 0
    for raw_path in retained:
        path = list(raw_path)
        if len(path) < 2 or len(path) % 2 or len(set(path)) != len(path):
            raise ValueError('Retain simple paths of odd edge length')
        if not set(path) <= board or set(path) & removed:
            raise ValueError('Retained paths must be inside the board and disjoint')
        if (path[0] not in q or path[-1] not in q or
                sum(path[0]) % 2 != 1 or sum(path[-1]) % 2 != 0):
            raise ValueError('Orient retained paths from white Q to black Q')
        if any(v not in mate for v in path[1:-1]):
            raise ValueError('Path interiors must be actual matching endpoints')
        if any(not adjacent(a, b) for a, b in zip(path, path[1:])):
            raise ValueError('Retain grid paths')
        if any(pair(path[i], path[i+1]) not in actual for i in range(1, len(path)-1, 2)):
            raise ValueError('Actual pairs must alternate with auxiliary edges')
        label = int(path[0] in selected)
        fixed_labels.update((v, label) for v in path)
        fixed_n.update(pair(path[i], path[i+1]) for i in range(0, len(path)-1, 2))
        expense += label*sum(weights[pair(path[i], path[i+1])]
                             for i in range(1, len(path)-1, 2))
        removed.update(path)
    assert all(not set(e) & removed or set(e) <= removed for e in actual)
    residual = board-removed
    return dict(board=residual, actual={e for e in actual if set(e) <= residual},
                selected=selected-removed, weights=weights,
                fixed_auxiliary=fixed_n, fixed_labels=fixed_labels, fixed_expense=expense)


def optimize_th(board, actual, selected, weights=None, retained=(), scan='auto', witness=True):
    """Return exact optimum (None if infeasible), optional N/labels and work counts.

    scan='columns' scans columns then rows; 'rows' is its transpose.
    Value-only mode retains rolling state tables, without witness parents.
    """
    data = prepare(board, actual, selected, weights, retained)
    vertices, actual, selected = data['board'], data['actual'], data['selected']
    p = {v for e in actual for v in e}
    white_q = {v for v in vertices-p if sum(v) % 2}
    if scan not in {'auto', 'rows', 'columns'}:
        raise ValueError('Unknown scan direction')
    height = max((v[0] for v in vertices), default=0)-min((v[0] for v in vertices), default=0)+1
    width = max((v[1] for v in vertices), default=0)-min((v[1] for v in vertices), default=0)+1
    if scan == 'auto':
        scan = 'columns' if height <= width else 'rows'
    order = sorted(vertices, key=(lambda v: (v[1], v[0])) if scan == 'columns' else None)
    index = {v: i for i, v in enumerate(order)}
    # Four probes per vertex: no quadratic all-pairs adjacency construction.
    neighbours = {v: sorted(w for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1))
                             if (w := (v[0]+dr, v[1]+dc)) in vertices) for v in vertices}
    last = {v: max([index[v]]+[index[w] for w in neighbours[v]]) for v in vertices}
    expiring = {}
    for v in order:
        expiring.setdefault(last[v], []).append(v)
    bag, table, history = [], {(): 0}, []
    stats = dict(vertices=len(vertices), edges=sum(map(len, neighbours.values()))//2,
                 scan=scan, frontier_bound=(height if scan == 'columns' else width)+1,
                 max_frontier=0, max_states=1, events=0, states_processed=0,
                 transitions=0, parent_entries=0)

    def advance(options):
        nonlocal table
        new, parents = {}, {}
        stats['events'] += 1
        stats['states_processed'] += len(table)
        for state, cost in table.items():
            for target, fee, action in options(state):
                stats['transitions'] += 1
                candidate = cost+fee
                if target not in new or candidate < new[target]:
                    new[target] = candidate
                    if witness:
                        parents[target] = (state, action)
        table = new
        stats['max_states'] = max(stats['max_states'], len(table))
        if witness:
            history.append(parents)
            stats['parent_entries'] += len(parents)

    for i, v in enumerate(order):
        labels = (int(v in selected),) if v in white_q else (0, 1)
        advance(lambda state: ((state+(2*label,), 0, ('label', v, label)) for label in labels))
        bag.append(v)
        stats['max_frontier'] = max(stats['max_frontier'], len(bag))
        for u in neighbours[v]:
            if index[u] >= i:
                continue
            a, b, edge = bag.index(u), bag.index(v), pair(u, v)
            is_actual = edge in actual

            def choices(state):
                x, y = state[a], state[b]
                same = x//2 == y//2
                if is_actual and not same:
                    return
                fee = data['weights'][edge]*(x//2) if is_actual else 0
                yield state, fee, None
                if same and not x % 2 and not y % 2:
                    new = list(state)
                    new[a] += 1
                    new[b] += 1
                    yield tuple(new), fee, ('edge', edge)
            advance(choices)
        for u in expiring.get(i, ()):
            position = bag.index(u)
            advance(lambda state: [(state[:position]+state[position+1:], 0, None)]
                    if state[position] % 2 else [])
            bag.pop(position)
    assert not bag
    optimum = table.get(())
    result = dict(optimum=None if optimum is None else optimum+data['fixed_expense'],
                  fixed_expense=data['fixed_expense'], stats=stats)
    if witness and optimum is not None:
        auxiliary, labels, state = set(data['fixed_auxiliary']), dict(data['fixed_labels']), ()
        for parents in reversed(history):
            state, action = parents[state]
            if action is not None:
                if action[0] == 'edge':
                    auxiliary.add(action[1])
                else:
                    labels[action[1]] = action[2]
        assert state == ()
        result.update(auxiliary=auxiliary, labels=labels)
    return result


def complete_ladder_zero_fee(board, actual, selected, weights=None):
    """Linear construction on a full 2-by-n ladder with feasible selected whites.

    Returns a full auxiliary matching of TH expense zero. Transposed/translated
    ladders are supported. No retained paths are imposed by this constructor.
    """
    data = prepare(board, actual, selected, weights)
    board, actual, selected = data['board'], data['actual'], data['selected']
    if not board:
        raise ValueError('Nonempty full 2-by-n rectangle required')
    r0, r1 = min(v[0] for v in board), max(v[0] for v in board)
    c0, c1 = min(v[1] for v in board), max(v[1] for v in board)
    h, w = r1-r0+1, c1-c0+1
    if 2 not in (h, w) or len(board) != h*w:
        raise ValueError('Full 2-by-n rectangle required')
    columns = ([[(r0, c), (r1, c)] for c in range(c0, c1+1)] if h == 2 else
               [[(r, c0), (r, c1)] for r in range(r0, r1+1)])
    white = [next(v for v in col if sum(v) % 2) for col in columns]
    black = [next(v for v in col if not sum(v) % 2) for col in columns]
    column_of = {v: i for i, col in enumerate(columns) for v in col}
    mate = {v: w for e in actual for v, w in (e, e[::-1])}
    if any(sum((t[0]+dr, t[1]+dc) in mate for dr, dc in
               ((-1, 0), (1, 0), (0, -1), (0, 1))) > 1 for t in selected):
        raise ValueError('Each selected vertex must have at most one occupied neighbour')
    auxiliary, used, swaps = set(), set(), []
    for j, t in enumerate(white):
        if t not in selected or black[j] not in mate:
            continue
        i = column_of[mate[black[j]]]
        assert abs(i-j) == 1 and black[i] not in mate
        assert not {i, j} & used
        used.update((i, j))
        swaps.append((i, j))
        auxiliary.update((pair(white[i], black[j]), pair(white[j], black[i])))
    auxiliary.update(pair(white[j], black[j]) for j in range(len(columns)) if j not in used)
    return dict(optimum=0, auxiliary=auxiliary, swaps=swaps)
