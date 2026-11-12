"""Mixed auxiliary/owner bridges; see docs/MIXED_OWNER_BRIDGES.md.

The omission constructions are polynomial. The mixed colouring and one-K4
routine reuse a feasibility colouring search, without a runtime claim for it.
"""
from itertools import combinations, product
from owner_matching_certificate import components, prepare, materialize, three_colour
from all_helper_optimization import score


def _edges(edges):
    return sorted({tuple(sorted(e)) for e in edges})


def _permitted(n, B, U):
    S = set(range(n)) - set(U)
    return all(sum(v in e and set(e) <= S for e in B) <= 1 for v in S)


def _finish(data, U, method, **extra):
    n = 2*data['b']; U = set(U)
    assert _permitted(n, data['B'], U)
    T, M = score(n, data['P'], data['Q'], U)
    value = 3*data['b'] - len(M)
    assert len(T) == len(U)-len(M)
    assert value == data['b'] + n-len(U)+len(T) >= (8*data['b']+2)//3
    return dict(applicable=True, method=method, U=sorted(U),
                owners=sorted(set(range(n))-U), witnesses=sorted(T),
                matching=M, beta_I_lower=value, **extra)


def mixed_colouring(n, A, B):
    """A-proper three-colouring, each B colour class of induced degree <=1.

    A is any simple max-degree-two graph; B is paths and even cycles.
    """
    A, B = _edges(A), _edges(B)
    for E in (A, B):
        assert all(0 <= a < b < n for a, b in E)
        assert all(sum(v in e for e in E) <= 2 for v in range(n))
    R, F = [], []
    for order, cyclic in components(n, B):
        assert not cyclic or len(order) % 2 == 0
        edges = list(zip(order, order[1:]+order[:1])) if cyclic else list(zip(order, order[1:]))
        R += edges[::2]; F += edges[1::2]
    J = _edges(A+R); removed = []
    for K, _ in components_general(n, J):
        if len(K) == 4 and sum(set(e) <= set(K) for e in J) == 6:
            removed.append(K)
    absent = {v for K in removed for v in K}
    c = three_colour(set(range(n))-absent, [e for e in J if not set(e)&absent])
    for K in removed:
        lists = {v: set(range(3))-{c[u] for e in F if v in e for u in e if u != v and u in c} for v in K}
        assert all(len(z) >= 2 for z in lists.values())
        feasible = None
        for colours in product(*(sorted(lists[v]) for v in K)):
            trial = dict(zip(K, colours))
            if all(trial[a] != trial[b] for a,b in A if a in trial and b in trial):
                feasible = trial; break
        assert feasible is not None
        c.update(feasible)
    assert all(c[a] != c[b] for a,b in A)
    assert all(sum(v in e and c[e[0]] == c[e[1]] for e in B) <= 1 for v in range(n))
    return dict(colouring=sorted(c.items()), largest_class=sorted(max(
        ({v for v in c if c[v] == k} for k in range(3)), key=len)), restored_squares=removed)


def components_general(n, E):
    """Connected sets, also for max degree three graphs."""
    adj = [set() for _ in range(n)]
    for a,b in E: adj[a].add(b); adj[b].add(a)
    unseen = set(range(n)); result = []
    while unseen:
        root = min(unseen); part = {root}; todo = [root]
        while todo:
            for v in adj[todo.pop()]-part: part.add(v); todo.append(v)
        unseen -= part; result.append((sorted(part), adj))
    return result


def square_six_bridge(b, P, Q, B, colour):
    """Any number of owner C4's, other owner cycles of length 6k, all paths."""
    data = prepare(b,P,Q,B,colour); n = 2*b
    owners = data['owner_components']; I = set(); outside = []
    for K, cyclic in owners:
        if cyclic and len(K) == 4: I.update(K)
        elif cyclic and len(K) % 6:
            return dict(applicable=False, reason='owner cycle outside C4/6k class')
        else: outside.append((K,cyclic))
    second_edges = [e for e in data['P'] if set(e) <= I]
    for K, cyclic in owners:
        if cyclic and len(K) == 4: second_edges += [(K[0],K[2]),(K[1],K[3])]
    adj = {v:set() for v in I}
    for a,c in second_edges: adj[a].add(c); adj[c].add(a)
    bit = {}
    for root in sorted(I):
        if root in bit: continue
        bit[root] = 0; todo = [root]
        while todo:
            v = todo.pop()
            for u in sorted(adj[v]):
                if u not in bit: bit[u] = 1-bit[v]; todo.append(u)
                assert bit[u] != bit[v]
    labels = {v:2*colour[v]+bit[v] for v in I}
    A = _edges(data['P']+data['Q']); candidates = []
    for pair in combinations(range(4),2):
        UI = {v for v in I if labels[v] in pair}; U = set(UI)
        twice_budget = 2*sum(set(e) <= UI for e in A); phases = []
        for K,cyclic in outside:
            choices = []
            for p in range(3):
                X = {v for j,v in enumerate(K) if j%3 == p}
                weight = sum(1+sum(v in e and len(set(e)&UI) == 1 for e in A) for v in X)
                choices.append((weight,p,X))
            weight,p,X = min(choices,key=lambda z:(z[0],z[1]))
            phases.append(p); U |= X; twice_budget += weight
        assert _permitted(n,B,U)
        candidates.append((twice_budget,sorted(U),list(pair),phases))
    budget,U,pair,phases = min(candidates)
    assert 3*budget <= n
    return _finish(data,U,'four-label interface budget', labels=sorted(labels.items()),
                   label_pair=pair, outside_phases=phases, twice_budget=budget,
                   six_candidate_budgets=[x[0] for x in candidates])


def _minimum_omission(K, cyclic):
    if not cyclic: return {v for j,v in enumerate(K) if j%3 == 2}
    m = len(K); k = (m+2)//3; gaps = [3]*k; gaps[-1] -= 3*k-m
    U = set(); j = 0
    for gap in gaps: U.add(K[j]); j = (j+gap)%m
    assert j == 0 and len(U) == k
    return U


def _exchange(K, start):
    m = len(K); order = K[start:]+K[:start]
    if m == 4: U = {order[0],order[2]}
    else:
        k = (m+2)//3; gaps = [3]*k; gaps[-1] = 2
        if m%3 == 1: gaps[1] = 2
        assert sum(gaps) == m
        U = set(); j = 0
        for gap in gaps: U.add(order[j]); j = (j+gap)%m
        assert j == 0
    return U, (U-{order[0]})|{order[1]}


def cardinality_bridge(b,P,Q,B,colour):
    """Minimum omissions, with one matching-edge saving at even cardinality.

    Some exceptional cycle is required for the saving. All minimum choices
    outside that cycle can be kept fixed. See Theorem 4's local count lemma.
    """
    data = prepare(b,P,Q,B,colour); n = 2*b; owners = data['owner_components']
    U = set().union(*(_minimum_omission(K,c) for K,c in owners)) if owners else set()
    if len(U)//2 <= n//6: return _finish(data,U,'minimum omission cardinality')
    bad = [K for K,c in owners if c and len(K)%6]
    if len(U)%2 or not bad or len(U)//2-1 > n//6:
        return dict(applicable=False, reason='minimum omission bound exceeds target after one saving')
    C = bad[0]; U0 = U-set(C)
    for j in range(len(C)):
        for UC in _exchange(C,j):
            candidate = U0|UC
            if len(score(n,P,Q,candidate)[1]) <= n//6:
                return _finish(data,candidate,'exceptional-cycle exchange',
                               minimum_omission_count=len(U), exchange_start=j,
                               exchanged_cycle=C)
    raise AssertionError('Local auxiliary component balance forces a saving')


def one_exception_bridge(b,P,Q,B,colour):
    """At most one owner cycle of length not divisible by six; arbitrary A."""
    data = prepare(b,P,Q,B,colour)
    if sum(c and len(K)%6 != 0 for K,c in data['owner_components']) > 1:
        return dict(applicable=False, reason='more than one exceptional owner cycle')
    result = cardinality_bridge(b,P,Q,B,colour)
    assert result['applicable']
    return result


def one_K4_bridge(b,P,Q,B,colour,values=None):
    """Repair <=1 K4 for a specified owner matching (virtual owner-C4 diagonals)."""
    data = prepare(b,P,Q,B,colour)
    values = [0]*len(data['choices']) if values is None else values
    rec = materialize(data,values); n = 2*b; z = len(rec['K4']); o = data['odd_paths']
    if z>1: return dict(applicable=False, reason='specified matching has multiple K4s')
    R = rec['R']; W = set(rec['matched']); holes = set(range(n))-W
    if z == 0 or o >= 2:
        bad = set().union(*(set(K) for K in rec['K4'])) if z else set()
        c = three_colour(W-bad,[e for e in rec['edges'] if not set(e)&bad])
        T = max(({v for v in c if c[v]==k} for k in range(3)),key=len)|{min(K) for K in rec['K4']}
        S = set(holes)
        for a,d in R: S.add(a if a not in T else d)
        return _finish(data,set(range(n))-S,'specified matching bound', specified_values=values, K4=z)
    assert z == 1 and o == 0
    K = set(rec['K4'][0]); inner = [e for e in R if set(e)<=K]; e,f = inner
    assert e in data['B'] and f in data['B']
    ext = [p for p in R if not set(p)&K]; mate = {a:d for a,d in ext for a,d in ((a,d),(d,a))}
    c = three_colour(W-K,[p for p in rec['edges'] if not set(p)&K])
    neighbours = {v for p in data['B'] if set(p)&set(e) for v in p if v not in K}
    mates = {mate[v] for v in neighbours}
    assert len(neighbours) <= 2 and not neighbours&mates
    tstar = min(set(range(3))-{c[v] for v in mates}); candidates = []
    for t in range(3):
        T = set(f)|{v for v in c if c[v] == t}; S = set(e) if t == tstar else {e[0]}
        for a,d in ext:
            if t == tstar and a in mates: S.add(a)
            elif t == tstar and d in mates: S.add(d)
            else: S.add(a if a not in T else d)
        assert not S&T and all(not set(p)<=T for p in P+Q)
        assert _permitted(n,B,set(range(n))-S)
        candidates.append((b+len(S)+len(T),S,T))
    assert sum(x[0] for x in candidates) == 8*b
    value,S,T = max(candidates,key=lambda x:x[0])
    return _finish(data,set(range(n))-S,'one-K4 doubled-owner repair', specified_values=values,
                   repaired_square=sorted(K), three_sizes=[x[0] for x in candidates],
                   repair_colour=tstar, repair_initial_value=value)
