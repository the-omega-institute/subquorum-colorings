"""Exact tree recurrences; direct partial-color enumeration supplies small controls."""
import itertools
import json
from pathlib import Path


def parameters(adj):
    """Return beta_2 and psi_sq using rooted-tree integer dynamic programs."""
    def visit(v, parent):
        children = [visit(w, v) for w in adj[v] if w != parent]
        beta, psi = {}, {}
        for occupied in (0, 1):
            for parent_occupied in (0, 1):
                # Dissociation: an occupied vertex has at most one occupied neighbor.
                scores = {0: occupied}
                for child_beta, _ in children:
                    nxt = {}
                    for count, value in scores.items():
                        for child_occupied in (0, 1):
                            key = count + child_occupied
                            candidate = value + child_beta[child_occupied, occupied]
                            nxt[key] = max(nxt.get(key, -10**9), candidate)
                    scores = nxt
                beta[occupied, parent_occupied] = max(
                    (value for count, value in scores.items()
                     if not occupied or count + parent_occupied <= 1), default=-10**9)
                for same_parent in range(min(occupied, parent_occupied) + 1):
                    # Every monochromatic component contributes one color.
                    # Charge its parent edge once, at the child endpoint.
                    scores = {(0, 0): occupied - same_parent}
                    for _, child_psi in children:
                        nxt = {}
                        for (count, same), value in scores.items():
                            for child_occupied in (0, 1):
                                for same_child in range(min(occupied, child_occupied) + 1):
                                    key = count + child_occupied, same + same_child
                                    candidate = value + child_psi[child_occupied, occupied, same_child]
                                    nxt[key] = max(nxt.get(key, -10**9), candidate)
                        scores = nxt
                    psi[occupied, parent_occupied, same_parent] = max(
                        (value for (count, same), value in scores.items()
                         if not occupied or count + parent_occupied <= 1 + 2*(same + same_parent)),
                        default=-10**9)
        return beta, psi

    b, p = visit(0, -1)
    return max(b[x, 0] for x in (0, 1)), max(p[x, 0, 0] for x in (0, 1))


def hub_double_stars(k):
    adj = [set() for _ in range(6*k+1)]
    for i in range(k):
        u, v, a, b, c, d = range(6*i+1, 6*i+7)
        for x, y in [(u,v), (u,a), (u,b), (v,c), (v,d), (0,a)]:
            adj[x].add(y)
            adj[y].add(x)
    return adj


def graft_double_stars(base):
    """Attach the leaf a of a fresh double star to each base vertex."""
    k = len(base)
    adj = [set(neighbors) for neighbors in base] + [set() for _ in range(6*k)]
    for i in range(k):
        u, v, a, b, c, d = range(k+6*i, k+6*i+6)
        for x, y in [(u,v), (u,a), (u,b), (v,c), (v,d), (i,a)]:
            adj[x].add(y)
            adj[y].add(x)
    return adj


def prufer_tree(code):
    n = len(code)+2
    degree = [1]*n
    for v in code:
        degree[v] += 1
    adj = [set() for _ in range(n)]
    for v in code:
        leaf = next(i for i, d in enumerate(degree) if d == 1)
        adj[leaf].add(v)
        adj[v].add(leaf)
        degree[leaf] -= 1
        degree[v] -= 1
    u, v = [i for i, d in enumerate(degree) if d == 1]
    adj[u].add(v)
    adj[v].add(u)
    return adj


def direct(adj):
    n = len(adj)
    beta = max(mask.bit_count() for mask in range(1 << n)
               if all(not (mask >> v & 1) or sum(mask >> w & 1 for w in adj[v]) <= 1
                      for v in range(n)))
    psi = 0
    def colorings(colors, count):
        nonlocal psi
        if len(colors) == n:
            if all(colors[v] < 0 or
                   sum(colors[w] >= 0 for w in adj[v]) <=
                   1 + 2*sum(colors[w] == colors[v] for w in adj[v]) for v in range(n)):
                psi = max(psi, count)
            return
        for c in range(-1, count+1):
            colorings(colors+[c], max(count, c+1))
    colorings([], 0)
    return beta, psi


if __name__ == '__main__':
    direct_checks = 0
    for n in range(2, 6):
        for code in itertools.product(range(n), repeat=n-2):
            adj = prufer_tree(code)
            assert parameters(adj) == direct(adj)
            direct_checks += 1
    gaps = 0
    for code in itertools.product(range(6), repeat=4):
        adj = prufer_tree(code)
        b, p = parameters(adj)
        double_star = sorted(map(len, adj)) == [1,1,1,1,3,3]
        assert (p > b) == double_star
        gaps += p > b
    family = []
    for k in range(1, 31):
        b, p = parameters(hub_double_stars(k))
        assert (b, p) == (4*k+1, 5*k), (k,b,p)
        family.append(dict(k=k, vertices=6*k+1, beta2=b, psi_sq=p))
    report = dict(status='passed', direct_partial_coloring_controls=direct_checks,
                  six_vertex_trees=1296, six_vertex_strict_gaps=gaps,
                  connected_family=family, lean_formalized=False)
    graft_controls = 0
    for n in range(2, 6):
        for code in itertools.product(range(n), repeat=n-2):
            base = prufer_tree(code)
            assert parameters(graft_double_stars(base)) == (4*n+parameters(base)[0], 5*n)
            graft_controls += 1
    subcubic = []
    for k in range(1, 31):
        base = [{w for w in (v-1, v+1) if 0 <= w < k} for v in range(k)]
        graph = graft_double_stars(base)
        b, p = parameters(graph)
        assert (b, p) == (4*k+(2*k+2)//3, 5*k)
        assert max(map(len, graph)) == 3
        subcubic.append(dict(k=k, vertices=7*k, beta2=b, psi_sq=p, gap=p-b))
    report['grafting_tree_controls'] = graft_controls
    report['subcubic_family'] = subcubic
    Path('results/tree-parameters.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items()
                      if k not in ('connected_family', 'subcubic_family')},indent=2))
    print('Connected family checked for k=1..30; last:', family[-1])
    print('Subcubic family checked for k=1..30; last:', subcubic[-1])
