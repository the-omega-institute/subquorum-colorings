"""Literal independent controls for square and path attachments; no project imports."""
from collections import deque
from itertools import combinations, product
from pathlib import Path
import json
import random


def graph(n, edges):
    g = [0]*n
    for u,v in edges:
        assert u != v and 0 <= u < n and 0 <= v < n
        g[u] |= 1 << v
        g[v] |= 1 << u
    return g


def attach(g, roots):
    """Roots are disjoint singletons (paths) or existing edges (squares)."""
    out = g[:]
    seen = set()
    clusters = []
    for root in roots:
        assert len(root) in (1,2) and not (seen & set(root))
        seen.update(root)
        a = len(out)
        b = a+1
        out.extend([0,0])
        edges = [(root[0],a),(a,b)]
        if len(root) == 2:
            d,e = root
            assert g[d] >> e & 1
            edges.append((b,e))
        for u,v in edges:
            out[u] |= 1 << v
            out[v] |= 1 << u
        clusters.append(tuple(root)+(a,b))
    return out,clusters,seen


def unformed(g, selected):
    active = sum(1 << v for v,row in enumerate(g)
                 if selected >> v & 1 and row & selected)
    return [v for v,row in enumerate(g) if not (selected >> v & 1)
            and (row & selected).bit_count() < 2 and not (row & active)]


def dissociation(g, selected):
    return all(not (selected >> v & 1) or (row & selected).bit_count() <= 1
               for v,row in enumerate(g))


def literal(g):
    formed = []
    minimal = []
    beta = 0
    for selected in range(1 << len(g)):
        if dissociation(g,selected):
            beta = max(beta,selected.bit_count())
        ok = not unformed(g,selected)
        formed.append(ok)
        if ok and all(not formed[selected ^ (1 << v)]
                      for v in range(len(g)) if selected >> v & 1):
            minimal.append(selected)
    return beta,max(map(int.bit_count,minimal)),minimal


def restrict(g, vertices):
    return [sum(1 << j for j,w in enumerate(vertices) if g[v] >> w & 1)
            for v in vertices]


def matchings(g):
    edges = [(u,v) for u in range(len(g)) for v in range(u+1,len(g))
             if g[u] >> v & 1]
    def visit(i, used, chosen):
        if i == len(edges):
            yield chosen
            return
        yield from visit(i+1,used,chosen)
        u,v = edges[i]
        if u not in used and v not in used:
            yield from visit(i+1,used|{u,v},chosen+[(u,v)])
    yield from visit(0,set(),[])


def check_instance(base, roots, report, kind):
    g,clusters,deleted = attach(base,roots)
    remainder = [v for v in range(len(base)) if v not in deleted]
    f = restrict(base,remainder)
    bf,sf,mf = literal(f)
    bg,sg,mg = literal(g)
    k = len(roots)
    assert bg == 2*k+bf and 2*k+sf <= sg <= 2*k+len(f)
    for selected in mg:
        assert all(sum(selected >> v & 1 for v in cluster) == 2
                   for cluster in clusters)
    if not f:
        assert len(mg) == (6 if kind == 'square' else 3)**k
        assert {s.bit_count() for s in mg} == {2*k}
        report['fully_covered_models'] += 1
    new_pairs = sum((1 << cluster[-2]) | (1 << cluster[-1]) for cluster in clusters)
    for old in mf:
        lifted = new_pairs | sum(1 << v for j,v in enumerate(remainder) if old >> j & 1)
        assert not unformed(g,lifted)
        assert all(unformed(g,lifted ^ (1 << v))
                   for v in range(len(g)) if lifted >> v & 1)
        report['minimal_set_lifts'] += 1
    report[kind+'_models'] += 1
    report['literal_subsets'] += (1 << len(f))+(1 << len(g))
    report['local_caps'] += len(mg)*k


def median_triples(g):
    n = len(g)
    distances = []
    for s in range(n):
        d = [-1]*n
        d[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            for u in range(n):
                if g[v] >> u & 1 and d[u] == -1:
                    d[u] = d[v]+1
                    queue.append(u)
        assert min(d) >= 0
        distances.append(d)
    intervals = [[sum(1 << x for x in range(n)
                      if distances[a][x]+distances[x][b] == distances[a][b])
                  for b in range(n)] for a in range(n)]
    for a,b,c in combinations(range(n),3):
        assert (intervals[a][b] & intervals[a][c] & intervals[b][c]).bit_count() == 1
    return n*(n-1)*(n-2)//6


def connected_after_deletion(g, removed):
    remaining = set(range(len(g)))-{removed}
    first = min(remaining)
    seen = {first}
    queue = [first]
    for v in queue:
        for u in remaining-seen:
            if g[v] >> u & 1:
                seen.add(u)
                queue.append(u)
    return seen == remaining


def activity_obstruction(m, square):
    """Two cliques and private roots; certificates use literal formation."""
    t = list(range(m))
    x = list(range(m,2*m))
    roots = [(2*m+i,3*m+i) if square else (2*m+i,)
             for i in range(m)]
    edges = list(combinations(t,2))+list(combinations(x,2))
    for i,root in enumerate(roots):
        edges.extend([(root[0],t[i]),(root[0],x[i])])
        if square:
            edges.append(root)
    base = graph((4 if square else 3)*m,edges)
    g,clusters,_ = attach(base,roots)
    selected = sum(1 << v for v in t)
    selected |= sum((1 << c[0]) | (1 << c[-1]) for c in clusters)
    assert selected.bit_count() == 3*m and not unformed(g,selected)
    checks = 0
    for i,c in enumerate(clusters):
        for deleted,witness in ((t[i],x[i]),(c[0],c[-2]),(c[-1],c[-1])):
            assert witness in unformed(g,selected ^ (1 << deleted))
            checks += 1
    attaining = sum((1 << c[-2]) | (1 << c[-1]) for c in clusters)
    attaining |= sum(1 << v for v in (t[:2]+x[:2]))
    assert attaining.bit_count() == 2*m+4 and dissociation(g,attaining)
    return checks


def main():
    report = dict(status='PASS',square_models=0,path_models=0,literal_subsets=0,
                  fully_covered_models=0,minimal_set_lifts=0,local_caps=0,
                  larger_pair_selections=0,median_models=0,median_triples=0,
                  vertex_deletions=0,interior_edge_models=0,
                  activity_obstruction_models=0,activity_deletion_witnesses=0,
                  new_Lean=False)
    for n in range(5):
        edges = list(combinations(range(n),2))
        for code in range(1 << len(edges)):
            base = graph(n,[e for j,e in enumerate(edges) if code >> j & 1])
            for matching in matchings(base):
                check_instance(base,matching,report,'square')
            for deleted in range(1 << n):
                roots = [(v,) for v in range(n) if deleted >> v & 1]
                check_instance(base,roots,report,'path')

    rng = random.Random(2026111201)
    for n in (6,10,32,128,512):
        matching = [(v,v+1) for v in range(0,n,2)]
        edges = set(matching)
        edges.update((u,v) for u in range(n) for v in range(u+1,n)
                     if rng.randrange(100) < 8)
        g,clusters,_ = attach(graph(n,edges),matching)
        for _ in range(16):
            selected = sum(sum(1 << v for v in rng.sample(cluster,2)) for cluster in clusters)
            assert not unformed(g,selected)
            assert all(unformed(g,selected ^ (1 << v))
                       for v in range(len(g)) if selected >> v & 1)
            report['larger_pair_selections'] += 1

    for h,w in ((2,2),(2,3),(3,3),(3,4),(4,4)):
        edges = [(h0*w+j,h0*w+j+1) for h0 in range(h) for j in range(w-1)]
        edges += [(i*w+j,(i+1)*w+j) for i in range(h-1) for j in range(w)]
        base = graph(h*w,edges)
        outer = [(u,v) for u,v in edges
                 if (u//w == v//w and u//w in (0,h-1))
                 or (u%w == v%w and u%w in (0,w-1))]
        matching = []
        used = set()
        for u,v in outer:
            if u not in used and v not in used:
                matching.append((u,v))
                used.update((u,v))
        g,_,_ = attach(base,matching)
        assert max(map(int.bit_count,g)) <= 4
        report['median_triples'] += median_triples(g)
        assert all(connected_after_deletion(g,v) for v in range(len(g)))
        report['median_models'] += 1
        report['vertex_deletions'] += len(g)

    # New scope: attachments along interior edges, not only boundary ears.
    for h,w,matching in ((3,4,[(5,6)]),(4,4,[(5,6),(9,10)])):
        edges = [(i*w+j,i*w+j+1) for i in range(h) for j in range(w-1)]
        edges += [(i*w+j,(i+1)*w+j) for i in range(h-1) for j in range(w)]
        g,_,_ = attach(graph(h*w,edges),matching)
        # Interior roots have old degree four, hence new degree five.
        assert max(map(int.bit_count,g)) == 5
        report['median_triples'] += median_triples(g)
        assert all(connected_after_deletion(g,v) for v in range(len(g)))
        report['median_models'] += 1
        report['interior_edge_models'] += 1
        report['vertex_deletions'] += len(g)

    for m in (5,6,7,16,64,256):
        for square in (False,True):
            report['activity_deletion_witnesses'] += activity_obstruction(m,square)
            report['activity_obstruction_models'] += 1

    out = Path(__file__).resolve().parents[1]/'output'
    out.mkdir(exist_ok=True)
    (out/'square-ear-composition-check.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))


if __name__ == '__main__':
    main()
