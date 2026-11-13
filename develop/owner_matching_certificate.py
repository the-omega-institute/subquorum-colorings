"""Owner matching certificates; 2-SAT is exact for K4 avoidance, not beta_I."""
from collections import deque


def components(n, edges):
    adj = [set() for _ in range(n)]
    for a, b in edges:
        adj[a].add(b); adj[b].add(a)
    unseen = set(range(n)); result = []
    while unseen:
        root = min(unseen); block = {root}; todo = [root]
        while todo:
            for u in adj[todo.pop()] - block:
                block.add(u); todo.append(u)
        ends = sorted(v for v in block if len(adj[v]) < 2)
        start = ends[0] if ends else min(block)
        order = []; previous = None; v = start
        while v not in order:
            order.append(v)
            choices = sorted(adj[v] - ({previous} if previous is not None else set()))
            if not choices: break
            previous, v = v, choices[0]
        assert set(order) == block
        result.append((order, not ends)); unseen -= block
    return result


def _path(adj, start, target, allowed):
    parent = {start: None}; todo = deque([start])
    while todo:
        v = todo.popleft()
        if v == target:
            answer = []
            while v is not None: answer.append(v); v = parent[v]
            return answer[::-1]
        for u in sorted(adj[v]):
            if u in allowed and u not in parent: parent[u] = v; todo.append(u)
    raise AssertionError('SCC path missing')


def sat(variables, clauses):
    """A clause forbids the simultaneous requirements [(variable,phase),...]."""
    adj = [set() for _ in range(2 * variables)]
    reverse = [set() for _ in adj]
    for i, clause in enumerate(clauses):
        if not clause: return None, {'empty_clause': i}
        assert len(clause) <= 2
        factors = [2 * v + p for v, p in clause]
        if len(factors) == 1: factors *= 2
        a, b = factors
        for x, y in ((a, b ^ 1), (b, a ^ 1)):
            adj[x].add(y); reverse[y].add(x)
    seen = set(); order = []
    for root in range(len(adj)):
        if root in seen: continue
        stack = [(root, False)]
        while stack:
            v, done = stack.pop()
            if done: order.append(v); continue
            if v in seen: continue
            seen.add(v)
            stack.append((v, True))
            for u in sorted(adj[v], reverse=True):
                if u not in seen: stack.append((u, False))
    label = {}; blocks = []
    for root in reversed(order):
        if root in label: continue
        k = len(blocks); block = {root}; label[root] = k; todo = [root]
        while todo:
            for u in reverse[todo.pop()]:
                if u not in label: label[u] = k; block.add(u); todo.append(u)
        blocks.append(block)
    for v in range(variables):
        if label[2*v] == label[2*v+1]:
            block = blocks[label[2*v]]
            return None, {'variable': v, 'zero_to_one': _path(adj, 2*v, 2*v+1, block),
                          'one_to_zero': _path(adj, 2*v+1, 2*v, block)}
    values = [int(label[2*v+1] > label[2*v]) for v in range(variables)]
    assert all(not all(values[v] == p for v, p in clause) for clause in clauses)
    return values, None


def prepare(b, P, Q, B, colour):
    """Build alternating path/cycle choices, square diagonals, and all K4 clauses."""
    n = 2*b; V = set(range(n))
    assert b >= 0 and len(colour) == n and set(colour) <= {0, 1}
    P = sorted({tuple(sorted(e)) for e in P})
    Q = sorted({tuple(sorted(e)) for e in Q})
    B = sorted({tuple(sorted(e)) for e in B})
    assert len(P) == b and sorted(x for e in P for x in e) == list(range(n))
    assert len({x for e in Q for x in e}) == 2*len(Q)
    assert all(a in V and c in V and a != c for a,c in P+Q+B)
    assert all(colour[a] == colour[c] for a,c in P)
    assert all(colour[a] != colour[c] for a,c in Q+B)
    assert all(sum(v in e for e in B) <= 2 for v in V)
    owner_components = components(n, B); choices = []; fixed = []; sources = {}
    odd_paths = 0
    def register(edges, requirement):
        for edge in edges:
            edge = tuple(sorted(edge)); assert edge not in sources
            sources[edge] = requirement
    for order, cyclic in owner_components:
        k = len(order)
        if cyclic: assert k >= 4 and k % 2 == 0
        else: odd_paths += k % 2
        if cyclic and k == 4:
            edges = [(order[0], order[2]), (order[1], order[3])]
            fixed += edges; register(edges, None)
        elif (cyclic or k % 2) and k > 1:
            phases = [[(order[j], order[(j+1) % k]) for j in range(p, k-1+(cyclic and p == 1), 2)] for p in (0,1)]
            variable = len(choices); choices.append(phases)
            for phase, edges in enumerate(phases): register(edges, (variable, phase))
        else:
            edges = [(order[j], order[j+1]) for j in range(0, k-1, 2)]
            fixed += edges; register(edges, None)
    A = set(P+Q); clauses = []; bad_blocks = []
    for order, cyclic in components(n, A):
        if not cyclic or len(order) != 4: continue
        diagonal = [tuple(sorted((order[0],order[2]))), tuple(sorted((order[1],order[3])))]
        if not all(e in sources for e in diagonal): continue
        requirements = sorted({sources[e] for e in diagonal if sources[e] is not None})
        if any((v,1-p) in requirements for v,p in requirements): continue
        clauses.append(requirements); bad_blocks.append(sorted(order))
    return dict(b=b, P=P, Q=Q, B=B, colour=colour, owner_components=owner_components,
                choices=choices, fixed=fixed, odd_paths=odd_paths,
                clauses=clauses, bad_blocks=bad_blocks)


def materialize(data, values):
    assert len(values) == len(data['choices']) and all(v in (0,1) for v in values)
    R = list(data['fixed'])
    for choices, phase in zip(data['choices'], values): R += choices[phase]
    R = sorted(tuple(sorted(e)) for e in R)
    assert len({v for e in R for v in e}) == 2*len(R)
    W = {v for e in R for v in e}; A = set(data['P']+data['Q'])
    J = sorted(e for e in A | set(R) if set(e) <= W)
    bad = [K for K, clause in zip(data['bad_blocks'],data['clauses'])
           if all(values[v] == p for v,p in clause)]
    return dict(R=R, matched=sorted(W), edges=J, K4=bad)


def three_colour(vertices, edges):
    """DSATUR feasibility search; existence follows from Brooks, no runtime claim."""
    adj = {v:set() for v in vertices}
    for a,b in edges: adj[a].add(b); adj[b].add(a)
    assigned = {}
    # Explicit frames reproduce the recursive search order without a Python
    # recursion-depth limit. Backtracking still has no polynomial bound.
    stack = []
    while len(assigned) < len(adj):
        v = max((v for v in adj if v not in assigned),
                key=lambda v:(len({assigned[u] for u in adj[v] if u in assigned}),len(adj[v]),-v))
        unavailable = {assigned[u] for u in adj[v] if u in assigned}
        stack.append((v, iter([c for c in range(3) if c not in unavailable])))
        while stack:
            v, choices = stack[-1]
            assigned.pop(v, None)
            try:
                assigned[v] = next(choices)
                break
            except StopIteration:
                stack.pop()
        else:
            raise AssertionError('Expected K4-free subcubic graph')
    return assigned


def certificate(data):
    values, obstruction = sat(len(data['choices']), data['clauses'])
    if values is None: return dict(feasible=False, obstruction=obstruction)
    result = materialize(data, values)
    assert not result['K4']
    classes = three_colour(result['matched'], result['edges'])
    T = max(({v for v in classes if classes[v] == c} for c in range(3)), key=len)
    S = set(range(2*data['b'])) - set(result['matched'])
    for a,b in result['R']: S.add(a if a not in T else b)
    assert not S&T and all(not ({a,b} <= T) for a,b in data['P']+data['Q'])
    assert all(sum(v in e and set(e)<=S for e in data['B'])<=1 for v in S)
    b, o = data['b'], data['odd_paths']
    bound = b + (2*b+o)//2 + (2*b-o+2)//3
    assert len(S) == (2*b+o)//2 and b+len(S)+len(T) >= bound >= (8*b+2)//3
    return dict(feasible=True, values=values, owners=sorted(S), witnesses=sorted(T),
                beta_I_lower=b+len(S)+len(T), bound=bound, odd_paths=o,
                R=result['R'], colouring=sorted(classes.items()))


def template_certificate(m, colour):
    g, X, C, I = (m[k] for k in ('g','X','C','I'))
    order = sorted(X); index = {x:j for j,x in enumerate(order)}
    inverse = {c:x for x,c in m['owner'].items()}
    P = [tuple(index[x] for x in sorted(g[i]&X)) for i in sorted(I)]
    Q = [(index[x],index[y]) for x in X for y in g[x]&X if x<y]
    B = [(index[inverse[c]],index[inverse[d]]) for c in C for d in g[c]&C if c<d]
    data = prepare(len(I),P,Q,B,[colour[x] for x in order])
    rec = certificate(data)
    if not rec['feasible']: return None, dict(prepared=data,certificate=rec)
    D = set(I)|{order[j] for j in rec['witnesses']}|{m['owner'][order[j]] for j in rec['owners']}
    assert all(len(g[v]&D)<=1 for v in D) and len(D)>=(8*len(I)+2)//3
    return D, dict(prepared=data,certificate=rec)


def lift_certificate(g, S, w, beta, colour):
    m = dict(g=g,C=w['C0'],I=w['I0'],X=w['X0'],owner=w['owner'])
    inner, rec = template_certificate(m,colour)
    if inner is None: return None,rec
    retained = (w['R']-w['I0'])|{ell for c,ell,x in w['triples']}
    assert not retained&inner and all(not g[v]&inner for v in retained)
    D = inner|retained
    assert all(len(g[v]&D)<=1 for v in D) and len(D)<=beta
    p,u = len(w['triples']),len(w['pairs'])
    a,b,b3 = w['a'],w['b'],w['b3']; minimum=min(a,p)
    al,pi = a-minimum,p-minimum
    e,r = u-a-2*b,len(w['R'])-a-b
    q,d = len(g)-len(S)-p-u,len(S)-beta
    tau = minimum+b-2*d; L,bp = len(retained),len(w['I0'])
    Z = 3*beta-3*L-8*bp
    terms = [Z,5*r,12*(al+pi),24*tau,7*(e-b3),2*b3,5*q]
    assert all(t>=0 for t in terms) and sum(terms)==5*len(g)-51*d
    return D,dict(template=rec,inner=inner,retained=retained,Z=Z,
                  d=d,bprime=bp,L=L,nonnegative_terms=terms)
