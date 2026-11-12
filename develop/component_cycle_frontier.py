"""Exact fixed-list budget frontiers by the candidate component cycle rank.

Standard tree-factor messages evaluate each path/cycle factor by run parity.
Nonforest variables are conditioned once. Costs are unit matching numbers.
"""
from itertools import product
from collections import Counter
from nonisolated_exchange_frontier import validate, endpoint


def _plan(data):
    components = data['components']
    owner = {v: j for j, (vertices, _) in enumerate(components) for v in vertices}
    dsu = list(range(len(components)))
    adjacency = [[] for _ in components]
    forest, feedback = [], []

    def find(v):
        while dsu[v] != v:
            dsu[v] = dsu[dsu[v]]
            v = dsu[v]
        return v

    for i, (x, y) in enumerate(data['operations']):
        a, b = owner[x], owner[y]
        ra, rb = find(a), find(b)
        if ra == rb:
            feedback.append(i)
        else:
            dsu[ra] = rb
            forest.append(i)
            adjacency[a].append((b, i))
            adjacency[b].append((a, i))
    parent, parent_edge, roots, postorder = {}, {}, [], []
    for root in range(len(components)):
        if root in parent:
            continue
        roots.append(root)
        parent[root], parent_edge[root] = None, None
        stack, preorder = [root], []
        while stack:
            v = stack.pop()
            preorder.append(v)
            for child, i in adjacency[v]:
                if child == parent[v]:
                    continue
                assert child not in parent
                parent[child], parent_edge[child] = v, i
                stack.append(child)
        postorder.extend(reversed(preorder))
    assert len(feedback) == len(data['operations']) - len(components) + len(roots)
    children = [{i: child for child, i in adjacency[v] if parent.get(child) == v}
                for v in range(len(components))]
    return dict(forest_edges=forest, feedback_edges=feedback, roots=roots,
                postorder=postorder, parent_edge=parent_edge, children=children)


def _conditioned_forest(data, plan, pins):
    """Each residual candidate is counted in its CHILD message exactly once."""
    messages, steps, peak = {}, 0, 1

    def keep(table, key, value):
        old = table.get(key)
        if old is None or value < old:
            table[key] = value

    for component in plan['postorder']:
        vertices, cyclic = data['components'][component]
        pe = plan['parent_edge'][component]
        messages[component] = {}
        for parent_bit in ((None,) if pe is None else (0, 1)):
            count = int(parent_bit or 0)
            chosen = (1 << pe) if pe is not None and parent_bit else 0
            states = {(count, h, h): (0, chosen) for h in ((0, 1) if cyclic else (0,))}
            peak = max(peak, len(states))
            for v in vertices:
                if v not in data['vertex_op']:
                    options = [(int(v in data['U']), 0, 0, 0)]
                else:
                    i, role = data['vertex_op'][v]
                    if i in pins:
                        bit = pins[i]
                        options = [(bit if role else 1-bit, 0, 0, 0)]
                    elif i == pe:
                        options = [(parent_bit if role else 1-parent_bit, 0, 0, 0)]
                    else:
                        child = plan['children'][component][i]
                        options = [(s if role else 1-s, t, cost, mask)
                                   for s in (0, 1)
                                   for t, (cost, mask) in messages[child][s].items()]
                new = {}
                for (t, p, h), (cost, mask) in states.items():
                    for present, dt, dc, dm in options:
                        assert not (mask & dm)
                        key = (t+dt, 1-p if present else 0, h)
                        keep(new, key, (cost+dc+int(bool(present and p)), mask | dm))
                        steps += 1
                states = new
                peak = max(peak, len(states))
            result = {}
            for (t, p, h), value in states.items():
                if not cyclic or p == h:
                    keep(result, t, value)
            messages[component][parent_bit] = result
    pin_count = sum(pins.values())
    pin_mask = sum(1 << i for i, bit in pins.items() if bit)
    total = {pin_count: (0, pin_mask)}
    for root in plan['roots']:
        new = {}
        for t, (cost, mask) in total.items():
            for dt, (dc, dm) in messages[root][None].items():
                assert not (mask & dm)
                keep(new, t+dt, (cost+dc, mask | dm))
                steps += 1
        total = new
    q = len(data['operations'])
    assert set(total) == set(range(pin_count, pin_count + q-len(pins)+1))
    assert all(t == mask.bit_count() for t, (cost, mask) in total.items())
    assert peak <= 4*(q+1)
    return total, steps, peak


def component_frontier(n, edges, U, operations, component_orders=None, forest_only=False):
    """All exact-count optima, in O(2^k N(q+1)^2) arithmetic transitions.

    k is the cycle rank of the multigraph on COMPLETE ambient components,
    with one edge per candidate. Loops and parallel edges count normally.
    component_orders may change the rooted forest but not frontier costs.
    Integer masks and complete witnesses have polynomial bit overhead.
    """
    data = validate(n, edges, U, operations, component_orders)
    plan = _plan(data)
    feedback = plan['feedback_edges']
    if forest_only and feedback:
        raise ValueError('Candidates must join distinct components in a forest')
    total, steps, peak = {}, 0, 1
    for bits in product((0, 1), repeat=len(feedback)):
        branch, branch_steps, branch_peak = _conditioned_forest(data, plan, dict(zip(feedback, bits)))
        steps += branch_steps
        peak = max(peak, branch_peak)
        for t, value in branch.items():
            if t not in total or value < total[t]:
                total[t] = value
    q = len(data['operations'])
    assert set(total) == set(range(q+1))
    rows = [dict(operations=t, cost=total[t][0], selected_mask=total[t][1]) for t in range(q+1)]
    assert all(row['selected_mask'].bit_count() == row['operations'] for row in rows)
    best = min(rows, key=lambda row: (row['cost'], row['operations'], row['selected_mask']))
    return dict(cycle_rank=len(feedback), component_count=len(data['components']),
                component_tree_count=len(plan['roots']), forest_edges=plan['forest_edges'],
                feedback_edges=feedback, conditioned_branches=1 << len(feedback),
                peak_component_states=peak, transitions=steps,
                component_orders=[K for K, _ in data['components']], frontier=rows, best=best)


def physical_component_frontier(b, P, Q, B, colour, U, operations):
    """All subsets of a list with one permitted swap per DISTINCT owner."""
    from owner_matching_certificate import prepare
    data = prepare(b, P, Q, B, colour)
    n, U, ops = 2*b, set(U), [tuple(e) for e in operations]
    V = set(range(n))
    degree = Counter(v for a, c in data['B'] if a not in U and c not in U for v in (a, c))
    if not U <= V or max(degree.values(), default=0) > 1:
        raise ValueError('Permitted initial omission required')
    owner_of = {v: i for i, (K, _) in enumerate(data['owner_components']) for v in K}
    local = [[] for _ in data['owner_components']]
    for e in data['B']:
        local[owner_of[e[0]]].append(e)
    used = set()
    for i, x, y in ops:
        if i not in range(len(local)) or i in used:
            raise ValueError('Distinct owners required')
        used.add(i)
        K = set(data['owner_components'][i][0])
        remaining = (K-U) | {x}
        remaining.discard(y)
        degree = Counter(v for a, c in local[i] if a in remaining and c in remaining for v in (a, c))
        if x not in U & K or y not in K-U or max(degree.values(), default=0) > 1:
            raise ValueError('Permitted within-owner replacement required')
    pairs = [(x, y) for _, x, y in ops]
    out = component_frontier(n, data['P']+data['Q'], U, pairs)
    mask = out['best']['selected_mask']
    selected = [i for i in range(len(ops)) if mask >> i & 1]
    cert = endpoint(n, data['P']+data['Q'], U, pairs, selected)
    cert.update(owners=sorted(V-set(cert['U'])),
                witnesses=sorted(set(cert['U'])-set(cert['cover'])),
                beta_I_lower=3*b-cert['actual_cost'])
    return dict(**out, certificate=cert)


def component_star_family(q, types=None):
    """Even q>=2: physical order10q, two-connected bipartite min2/max3.

    Candidate component graph is a star, whereas every complete-component
    traversal has pair width at least q/2. Initial omissions are minimum.
    """
    if not isinstance(q, int) or isinstance(q, bool) or q < 2 or q % 2:
        raise ValueError('Even integer q>=2 required')
    types = [0]*q if types is None else list(types)
    if len(types) != q or any(t not in (0, 1) for t in types):
        raise ValueError('One binary type per owner required')
    P = [e for i in range(q) for e in ((2*i, 2*i+1), (2*q+2*i, 2*q+2*i+1))]
    Q = [(2*i+1, 2*((i+1) % q)) for i in range(q)]
    squares = [[2*i, 2*q+2*i, 2*i+1, 2*q+2*i+1] for i in range(q)]
    B = [e for K in squares for e in zip(K, K[1:]+K[:1])]
    U = [2*i for i in range(q)] + [2*i+1 if not types[i] else 2*q+2*i+1 for i in range(q)]
    colour = [i % 2 for i in range(q) for _ in (0, 1)] + [1-i % 2 for i in range(q) for _ in (0, 1)]
    return dict(q=q, b=2*q, types=types, P=P, Q=Q, B=B, colour=colour,
                initial_U=U, operations=[[i, 2*i, 2*q+2*i] for i in range(q)])
