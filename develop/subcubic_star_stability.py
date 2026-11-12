"""Construct the two exchanges used in the quantitative subcubic bound.

The caller supplies one permitted witness assignment W, the selected
centres C and selected isolates I. No optimum or witness search is used.
"""


def exchanges(g, selected, centres, isolates, witnesses):
    preliminary = []
    h = {i: len(g[i] & witnesses) for i in isolates}
    for centre in sorted(centres):
        leaves = sorted(g[centre] & selected)
        if len(leaves) != 2:
            continue
        choices = [(leaf, next(w for w in sorted(witnesses) if leaf in g[w]))
                   for leaf in leaves]
        private = [(leaf, w) for leaf, w in choices if g[w] & selected == {leaf}]
        helped = [(leaf, w, next(iter(g[w] & isolates))) for leaf, w in choices
                  if len(g[w] & isolates) == 1]
        if len(private) == len(helped) == 1 and h[helped[0][2]] == 1:
            x, a = private[0]
            y, b, i = helped[0]
            preliminary.append({'a': a, 'x': x, 'c': centre, 'y': y, 'b': b, 'i': i})
    private = {row['a'] for row in preliminary}
    baseline = selected-centres
    for row in preliminary:
        baseline.add(row['c'])
        baseline.remove(row['x'])
    assert len(baseline) == len(selected)-len(centres)
    components = []
    unseen = set(private)
    while unseen:
        component = {min(unseen)}
        todo = list(component)
        while todo:
            for v in (g[todo.pop()] & private)-component:
                component.add(v)
                todo.append(v)
        unseen -= component
        components.append(component)
    cycles = [q for q in components if len(q) == 4 and all(len(g[v] & q) == 2 for v in q)]
    cycle_of = {a: j for j, q in enumerate(cycles) for a in q}
    final = [row for row in preliminary if row['a'] in cycle_of]
    by_b = {row['b']: row for row in final}
    physical_edges = [(a, b) for a in sorted(by_b) for b in sorted(g[a] & by_b.keys()) if a < b]
    assert all(len(g[b] & by_b.keys()) <= 1 for b in by_b)
    # Quotient edges remember physical endpoints; dummy edges pair odd degrees.
    edges = []
    for a, b in physical_edges:
        edges.append((cycle_of[by_b[a]['a']], cycle_of[by_b[b]['a']], a, b))
    degree = [0]*len(cycles)
    for u, v, a, b in edges:
        degree[u] += 1
        degree[v] += 1
    assert max(degree, default=0) <= 4
    odd = [j for j, d in enumerate(degree) if d % 2]
    assert len(odd) % 2 == 0
    for u, v in zip(odd[::2], odd[1::2]):
        edges.append((u, v, None, None))
    incidence = [[] for _ in cycles]
    for j, (u, v, a, b) in enumerate(edges):
        incidence[u].append(j)
        incidence[v].append(j)
    unused = set(range(len(edges)))
    state_a = set()
    while unused:
        start = current = edges[min(unused)][0]
        while True:
            choices = [j for j in incidence[current] if j in unused]
            if not choices:
                assert current == start
                break
            j = min(choices)
            unused.remove(j)
            u, v, a, b = edges[j]
            if u != current:
                u, v, a, b = v, u, b, a
            assert u == current
            if b is not None:
                state_a.add(by_b[b]['a'])
            current = v
    for cycle in cycles:
        assert len(cycle & state_a) <= 2
        for a in sorted(cycle-state_a):
            if len(cycle & state_a) == 2:
                break
            state_a.add(a)
    final_centres = {row['c'] for row in final}
    result = selected-(centres-final_centres)
    for row in final:
        if row['a'] in state_a:
            result.remove(row['x'])
            result.add(row['a'])
        else:
            result.remove(row['y'])
            result.add(row['b'])
    assert len(result) == len(selected)-(len(centres)-len(final))
    return {'preliminary': preliminary, 'private_components': components,
            'cycles': cycles, 'bad_private_vertices': len(private)-4*len(cycles),
            'baseline': baseline, 'final': final, 'exchange': result,
            'state_A_private': state_a, 'helped_matching': physical_edges}
