"""Exact unrestricted physical residual/fee optimization on finite grid strips.

Four local labels encode HH, the two TH directions, and TT. No terminal
connectivity pairing is projected away or guessed from scalar reserves.
The frontier records joint labels and actual N-matched bits.
"""
from strip_tree_compensation import edge, grid, mates, physical_state_linear


def solve_frontier(h, w, m, t, weights=None, max_states=None):
    """Lexicographically minimize (number of TT paths, actual TH expense).

    N ranges over ALL full physical auxiliary matchings, without cell limits.
    With s=min(h,w), at most 8**s packed frontier states per vertex and at
    most 12 local transitions per state are considered. Backtracking stores
    O(|V|*8**s) entries; the optimization table alone uses O(8**s) entries.
    A state limit raises rather than returning an approximate certificate.
    """
    if h < 1 or w < 1:
        raise ValueError('Positive grid dimensions required')
    board = grid(h, w); m = {edge(a, b) for a, b in m}; t = set(t)
    original_mm = mates(board, m)
    if not t <= board-original_mm.keys():
        raise ValueError('Selected terminals must be unoccupied board vertices')
    weights = {e: 1 for e in m} if weights is None else {edge(a, b): v for (a, b), v in weights.items()}
    if weights.keys() != m or any(type(v) is not int or v < 0 for v in weights.values()):
        raise ValueError('Exactly one nonnegative integer weight per actual M edge')
    if max_states is not None and (type(max_states) is not int or max_states < 1):
        raise ValueError('State limit must be a positive integer or None')
    if h*w % 2:
        return None
    transpose = h > w
    transform = (lambda v: (v[1], v[0])) if transpose else (lambda v: v)
    hh, ww = (w, h) if transpose else (h, w)
    actual = {edge(transform(a), transform(b)): weights[edge(a, b)] for a, b in m}
    mm = {v: z for e in actual for v, z in [e, e[::-1]]}
    selected = {transform(v) for v in t}
    # 0 = HH/unused, 1 = black-T TH, 2 = white-T TH, 3 = TT.
    # All secondary costs lie in [0,W], so the integer unit enforces exact
    # lexicographic priority without a floating infinity or an epsilon.
    unit = 1+sum(weights.values())
    vertices = [(r, c) for c in range(ww) for r in range(hh)]
    dp = {0: 0}; history = []; peak_states = 1; state_visits = transitions = 0
    for r, c in vertices:
        v = r, c; shift = 3*r; slot_mask = 7 << shift
        left = (r, c-1) if c else None
        up = (r-1, c) if r else None
        if v in mm:
            allowed = (0, 1, 2, 3)
        elif v in selected:
            allowed = (1, 3) if (r+c) % 2 == 0 else (2, 3)
        else:
            allowed = (0, 2) if (r+c) % 2 == 0 else (0, 1)
        prior_m = mm.get(v) if mm.get(v) in (left, up) and v in mm else None
        nxt = {}; pred = {}; state_visits += len(dp)
        for state, cost in dp.items():
            left_slot = (state >> shift) & 7
            up_shift = shift-3
            up_slot = (state >> up_shift) & 7 if up is not None else None
            for colour in allowed:
                if prior_m == left and prior_m is not None and left_slot >> 1 != colour:
                    continue
                if prior_m == up and prior_m is not None and up_slot >> 1 != colour:
                    continue
                extra = unit if v in selected and (r+c) % 2 == 0 and colour == 3 else 0
                if prior_m is not None and colour in (1, 2):
                    extra += actual[edge(v, prior_m)]
                value = cost+extra; actions = []
                # Forget the previous-column vertex only after it is N-covered.
                if left is None or left_slot & 1:
                    actions.append((0, state, 0))
                    if up is not None and not up_slot & 1 and up_slot >> 1 == colour:
                        actions.append((1, state | (1 << up_shift), 2))
                if left is not None and not left_slot & 1 and left_slot >> 1 == colour:
                    actions.append((1, state, 1))
                for covered, updated, action in actions:
                    transitions += 1
                    key = (updated & ~slot_mask) | ((2*colour+covered) << shift)
                    if key not in nxt or value < nxt[key]:
                        nxt[key] = value; pred[key] = (state, action)
        if max_states is not None and len(nxt) > max_states:
            raise RuntimeError('Exact frontier state limit exceeded; no approximate result returned')
        if not nxt:
            return None
        dp = nxt; history.append(pred); peak_states = max(peak_states, len(dp))
    covered_mask = sum(1 << (3*r) for r in range(hh))
    final = [(value, state) for state, value in dp.items() if state & covered_mask == covered_mask]
    if not final:
        return None
    scalar, state = min(final); labels = {}; auxiliary = set()
    for j in range(len(vertices)-1, -1, -1):
        r, c = vertices[j]; v = r, c
        labels[transform(v)] = ((state >> (3*r)) & 7) >> 1
        old, action = history[j][state]
        if action:
            other = (r, c-1) if action == 1 else (r-1, c)
            auxiliary.add(edge(transform(v), transform(other)))
        state = old
    assert state == 0
    physical = physical_state_linear(board, m, auxiliary, t)
    a, _, _ = physical['data']['counts']
    fee = sum(weights[e] for e in physical['paid'])
    assert scalar == unit*a+fee
    assert all(labels[x] == labels[y] for x, y in m | auxiliary)
    # The scalar optimum has no positive-fee coloured P-only cycle. Zero-fee
    # coloured cycles are harmless and can also be normalized unused.
    for vs, _ in physical['cycles']:
        for v in vs:
            labels[v] = 0
    assert scalar == unit*sum(v in t and sum(v) % 2 == 0 and colour == 3
                              for v, colour in labels.items()) + sum(
        weights[e] for e in m if labels[e[0]] in (1, 2))
    assert peak_states <= 8**hh and transitions <= 12*len(board)*8**hh
    return dict(minimum_TT=a, minimum_unpaid_selected=2*a, TH_cost=fee,
                full_coverage=a == 0, scalar_cost=scalar, priority_unit=unit,
                auxiliary=auxiliary, labels=labels, state=physical,
                frontier_height=hh, transposed=transpose, peak_states=peak_states,
                state_visits=state_visits, local_transitions=transitions)
