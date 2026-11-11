#!/usr/bin/env python3
"""Standalone literal audit. Run with assertions enabled; writes only the JSON report.

Non-induced K1,2 means a triple with a vertex incident to the other two.
Single-deletion minimality is sufficient because formation is upward closed.
The finite audit supports, but does not replace, the general exchange argument.
"""
import argparse
from collections import Counter
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path


def graph(n, edges):
    g = [set() for _ in range(n)]
    for u, v in edges:
        assert u != v and 0 <= u < n and 0 <= v < n
        g[u].add(v)
        g[v].add(u)
    return g


def literal(g, s, x):
    # Explicit triples, independent of the witness-neighbourhood classification.
    return any((a in g[x] and b in g[x]) or
               (x in g[a] and b in g[a]) or
               (x in g[b] and a in g[b]) for a, b in combinations(sorted(s), 2))


def forming(g, s):
    return all(literal(g, s, x) for x in range(len(g)) if x not in s)


def minimal(g, s):
    return forming(g, s) and all(not forming(g, s - {v}) for v in s)


def diss(g, s):
    return all(len(g[v] & s) <= 1 for v in s)


def colors(g):
    col = {}
    for root in range(len(g)):
        if root in col:
            continue
        col[root] = 0
        todo = [root]
        while todo:
            u = todo.pop()
            for v in sorted(g[u]):
                if v not in col:
                    col[v] = 1 - col[u]
                    todo.append(v)
                assert col[v] != col[u]
    return col


def structure(g, s):
    unseen, c, leaves, isolates = set(s), set(), [], set()
    while unseen:
        todo, comp = [min(unseen)], set()
        while todo:
            v = todo.pop()
            if v in comp:
                continue
            comp.add(v)
            todo.extend((g[v] & s) - comp)
        unseen -= comp
        if len(comp) == 1:
            isolates |= comp
        elif len(comp) > 2:
            centres = [v for v in comp if g[v] & comp == comp - {v}]
            if len(centres) != 1:
                return None
            centre = centres[0]
            if any(g[v] & comp != {centre} for v in comp - {centre}):
                return None
            c.add(centre)
            leaves.extend(sorted(comp - {centre}))
    return c, sorted(leaves), isolates


def beta_literal(g):
    # Exact maximum by literal forbidden triples, not the exchange construction.
    triples = sorted({sum(1 << v for v in (c, a, b))
                      for c in range(len(g)) for a, b in combinations(g[c], 2)})
    @lru_cache(None)
    def solve(mask):
        for triple in triples:
            if mask & triple == triple:
                return max(solve(mask ^ (1 << v)) for v in range(len(g))
                           if triple >> v & 1)
        return mask.bit_count()
    return solve((1 << len(g)) - 1)


def beta_full_subsets(g):
    """Independent full-subset maximum using literal actual-star triples."""
    triples = {sum(1 << v for v in (centre,a,b))
               for centre in range(len(g)) for a,b in combinations(g[centre],2)}
    best = 0
    for mask in range(1 << len(g)):
        size = mask.bit_count()
        if size > best and not any(mask & triple == triple for triple in triples):
            best = size
    return best


def local_literal(g, s, x):
    """Enumerate actual stars at their centres; no scan of all selected pairs."""
    for centre in sorted({x} | (g[x] & s)):
        for a, b in combinations(sorted(v for v in g[centre] if v == x or v in s), 2):
            if x in (centre, a, b):
                return True
    return False


def matching_dual(g, vertices, col):
    """Augmenting paths plus alternating reachability (Konig certificate)."""
    left = sorted(v for v in vertices if col[v] == 0)
    mate = {}
    def augment(u, seen):
        for v in sorted(g[u] & vertices):
            if v in seen:
                continue
            seen.add(v)
            if v not in mate or augment(mate[v], seen):
                mate[v] = u
                return True
        return False
    for u in left:
        augment(u, set())
    matching = sorted((u, v) for v, u in mate.items())
    reached = set(left) - set(mate.values())
    todo = sorted(reached)
    while todo:
        u = todo.pop()
        for v in sorted(g[u] & vertices):
            if mate.get(v) == u:
                continue
            reached.add(v)
            if v in mate and mate[v] not in reached:
                reached.add(mate[v])
                todo.append(mate[v])
    cover = (set(left) - reached) | (reached - set(left))
    independent = vertices - cover
    assert len({v for edge in matching for v in edge}) == 2 * len(matching)
    assert all(v in g[u] for u, v in matching)
    assert all(u in cover or v in cover for u in vertices for v in g[u] & vertices)
    assert all(not g[v] & independent for v in independent)
    assert len(cover) == len(matching)
    return matching, cover, independent


def restricted_scan(g, s, leaves, ws, centres, h):
    """All restricted subsets, without assuming centres must be excluded."""
    base = set(leaves)
    optional = sorted((s | set(ws)) - base)
    best = -1
    for mask in range(1 << len(optional)):
        d = base | {v for i, v in enumerate(optional) if mask >> i & 1}
        if diss(g, d):
            assert not d & centres
            q = d & h
            assert all(not g[v] & q for v in q)
            best = max(best, len(d))
    return best


def leaf_matching(g, s, leaves, c, isolates, ws, col, enumerate_small=True):
    h = set(ws) | isolates  # ALL selected isolates, including untouched ones.
    matching, cover, independent = matching_dual(g, h, col)
    exact = len(s) - len(c) + len(leaves) - len(matching)
    unaffected = s - c - set(leaves) - isolates
    d = set(leaves) | unaffected | independent
    assert len(d) == exact and diss(g, d)
    assert set(leaves) <= d and not d & c
    small_scan = enumerate_small and len((s | set(ws)) - set(leaves)) <= 20
    if small_scan:
        assert restricted_scan(g, s, leaves, ws, c, h) == exact
    alpha = None
    if enumerate_small and len(h) <= 20:
        ordered = sorted(h)
        alpha = 0
        for mask in range(1 << len(ordered)):
            q = {v for i, v in enumerate(ordered) if mask >> i & 1}
            if all(not g[v] & q for v in q):
                alpha = max(alpha, len(q))
                constructed = set(leaves) | unaffected | q
                assert diss(g, constructed)
                assert len(constructed) == len(leaves) + len(unaffected) + len(q)
        assert alpha == len(h) - len(matching) == len(independent)
        assert exact == len(leaves) + len(unaffected) + alpha
    if not isolates:
        assert 2 * len(matching) <= len(leaves)
        assert len(leaves) - len(matching) >= len(c)
    return {'c':len(c), 'e':len(leaves), 'isolates':len(isolates),
            'alpha_Q':len(independent), 'alpha_Q_bruteforce':alpha,
            'restricted_subsets_enumerated':(1 << len((s | set(ws))-set(leaves))) if small_scan else 0,
            'both_directions_checked':small_scan and alpha is not None,
            'nu':len(matching), 'restricted_optimum':exact,
            'sufficient_criterion':len(leaves)-len(matching) >= len(c),
            'matching':[list(edge) for edge in matching],
            'minimum_vertex_cover':sorted(cover),
            'maximum_independent_set':sorted(independent),
            'optimal_leaf_retaining_set':sorted(d)}


def audit(g, s, beta, col, counts):
    st = structure(g, s)
    if st is None:
        return []
    c, leaves, isolates = st
    opts = [tuple(x for x in range(len(g)) if x not in s and
                  not literal(g, s - {leaf}, x)) for leaf in leaves]
    assert all(opts)
    rows = []
    for ws in product(*opts):
        assert len(set(ws)) == len(ws)
        for leaf, w in zip(leaves, ws):
            assert leaf in g[w] and (g[w] & s) - {leaf} <= isolates
            assert len(g[w] & s) in (1, 2)
        wa = {w for w in ws if col[w] == 0}
        wb = set(ws) - wa
        jb = {z for z in isolates if g[z] & wa}
        ja = {z for z in isolates if g[z] & wb}
        assert not ja & jb
        da, db = (s - c - jb) | wa, (s - c - ja) | wb
        assert diss(g, da) and diss(g, db)
        e, t = len(leaves), len(ja | jb)
        sizes = [len(s) - len(c) + len(wa) - len(jb),
                 len(s) - len(c) + len(wb) - len(ja)]
        assert sizes == [len(da), len(db)]
        bound = max(sizes)
        rounded = len(s) - len(c) + (e - t + 1) // 2
        criterion = e - t >= 2 * len(c) - 1
        assert beta >= bound >= rounded
        assert not criterion or len(s) <= beta
        assert isolates or e >= 2 * len(c)
        cert = leaf_matching(g, s, leaves, c, isolates, ws, col)
        assert beta >= cert['restricted_optimum'] >= bound
        assert e >= 2 * len(c)
        if t <= 1:
            assert criterion and cert['sufficient_criterion']
            assert cert['restricted_optimum'] >= len(s)
        counts['matching_assignments'] += 1
        counts['restricted_enumerations'] += cert['restricted_subsets_enumerated'] > 0
        counts['alpha_Q_bruteforce_comparisons'] += cert['alpha_Q_bruteforce'] is not None
        counts['both_directions_enumerated'] += cert['both_directions_checked']
        counts['matching_criterion_success' if cert['sufficient_criterion'] else 'matching_criterion_failure'] += 1
        counts['assignments'] += 1
        counts['criterion_success' if criterion else 'criterion_failure'] += 1
        counts['bound_below_selected' if bound < len(s) else 'bound_covers_selected'] += 1
        counts['actual_target_failure'] += len(s) > beta
        counts['conflicting_assignments'] += any(g[w] & set(ws) for w in ws)
        rows.append((len(c), e, t, bound, rounded, criterion))
    return rows


def exhaust():
    rows, total = [], Counter()
    for a, b in [(a, b) for n in range(7) for a in range(n + 1) for b in [n-a]] + [(3, 4)]:
        ct = Counter()
        possible = list(product(range(a), range(a, a+b)))
        for mask in range(1 << len(possible)):
            g = graph(a+b, [uv for i, uv in enumerate(possible) if mask >> i & 1])
            ct['graphs'] += 1
            subsets = [{v for v in range(a+b) if sm >> v & 1} for sm in range(1 << (a+b))]
            # Independent literal beta scan on every graph, including ineligible graphs.
            beta = beta_full_subsets(g)
            assert beta == max(len(s) for s in subsets if diss(g, s))
            assert beta == beta_literal(g)
            formed = [forming(g, s) for s in subsets]
            for sm, s in enumerate(subsets):
                ct['selections'] += 1
                if not formed[sm] or any(formed[sm ^ (1 << v)] for v in s):
                    continue
                ct['minimal_selections'] += 1
                if structure(g, s) is None:
                    continue
                ct['eligible_selections'] += 1
                ct['with_stars'] += bool(structure(g, s)[0])
                audit(g, s, beta, {v: int(v >= a) for v in range(a+b)}, ct)
        rows.append({'parts': [a,b], **dict(sorted(ct.items()))})
        total.update(ct)
    return rows, total


def fixture(name, links, extras=False, dense=False):
    # Links specify centre colour and optional shared selected isolate label.
    labels = sorted({(side, z) for side, z in links if z is not None})
    ids = {key: i+2 for i, key in enumerate(labels)}
    s, edges, ws = set(range(2+len(ids))), [], []
    n = len(s)
    for side, z in links:
        leaf, w = n, n+1
        n += 2
        s.add(leaf)
        edges += [(side, leaf), (leaf, w)]
        if z is not None:
            edges.append((w, ids[(side,z)]))
        ws.append((w,side))
    # Private centre neighbours ensure centre deletion fails.
    for centre in (0,1):
        edges.append((centre,n))
        n += 1
    if dense:
        edges += [(u,v) for u,a in ws for v,b in ws if a == 0 and b == 1]
    if extras:
        s.update((n,n+1,n+2))
        edges.append((n,n+1))
        n += 3
    return name, graph(n,edges), s


def summarize(name,g,s):
    assert minimal(g,s), name
    ct = Counter()
    beta = beta_literal(g)
    # Independent literal full-subset maximum for every small fixture.
    if len(g) <= 23:
        assert beta == beta_full_subsets(g)
    rows = audit(g,s,beta,colors(g),ct)
    c, leaves, isolates = structure(g, s)
    options = [tuple(x for x in range(len(g)) if x not in s and not literal(g,s-{leaf},x)) for leaf in leaves]
    certs = [leaf_matching(g,s,leaves,c,isolates,ws,colors(g)) for ws in product(*options)]
    return {'leaf_matching_certificates':certs, 'name':name,'vertices':len(g),'selected':sorted(s),'beta':beta,
            'budgets_c_e_t_bound_rounded_criterion': [list(r) for r in sorted(set(rows))],
            'checks':dict(sorted(ct.items()))}


def grid():
    g = graph(36, [(6*r+c,6*rr+cc) for r in range(6) for c in range(6)
                  for rr,cc in ((r+1,c),(r,c+1)) if rr<6 and cc<6])
    s = {6*r+c-1 for r,cs in enumerate([(1,4,6),(1,3,5),(1,3,4,6),(2,6),(3,5),(1,2,4,6)]) for c in cs}
    # Exact row DP: retain previous row and its predecessor; test actual degrees.
    states = {(0,0):0}
    history = []
    for row in range(7):
        nxt, parents = {}, {}
        for (prevprev,prev), value in states.items():
            for cur in range(64) if row<6 else (0,):
                if any(prev>>c&1 and ((prevprev>>c&1)+(cur>>c&1)+
                       (int(c>0 and prev>>(c-1)&1))+(int(c<5 and prev>>(c+1)&1)))>1 for c in range(6)):
                    continue
                key = prev,cur
                score = value + cur.bit_count()
                if score > nxt.get(key, -1):
                    nxt[key] = score
                    parents[key] = (prevprev, prev)
        states = nxt
        history.append(parents)
    beta = max(states.values())
    assert beta == 18
    key = max(states, key=states.get)
    masks = []
    for parents in reversed(history):
        masks.append(key[1])
        key = parents[key]
    masks = list(reversed(masks))[:6]
    optimum = {6*r+c for r, mask in enumerate(masks) for c in range(6) if mask >> c & 1}
    assert len(optimum) == beta and diss(g, optimum)
    assert minimal(g,s)
    ct = Counter()
    rows = audit(g,s,beta,colors(g),ct)
    c, leaves, isolates = structure(g,s)
    ws = [next(x for x in range(len(g)) if x not in s and not literal(g,s-{leaf},x)) for leaf in leaves]
    cert = leaf_matching(g,s,leaves,c,isolates,ws,colors(g))
    assert (cert['nu'],cert['e'],cert['c'],cert['restricted_optimum']) == (2,4,2,18)
    return {'leaf_matching_certificate':cert, 'name':'old_6x6','vertices':36,'selected':sorted(s),'beta':beta,
            'beta_method':'exact row DP validating induced degrees',
            'optimal_dissociation':sorted(optimum),
            'budgets_c_e_t_bound_rounded_criterion':[list(r) for r in sorted(set(rows))],
            'checks':dict(sorted(ct.items()))}


def block_family(r, connected):
    base = [(0,2),(0,3),(1,4),(1,5),(2,8),(3,9),(4,10),(5,11),
            (9,6),(11,7)] + list(product((8,9),(10,11)))
    edges = [(12*i+u,12*i+v) for i in range(r) for u,v in base]
    if connected:
        edges += [(12*i+9,12*(i+1)+11) for i in range(r-1)]
    g = graph(12*r, edges)
    assert sum(map(len, g)) // 2 == 14*r + (r-1 if connected else 0)
    s = {12*i+v for i in range(r) for v in range(8)}
    col = colors(g)
    c, leaves, isolates = structure(g,s)
    ws = [12*i+v for i in range(r) for v in (8,9,10,11)]
    assert len(c) == 2*r and len(leaves) == 4*r and len(isolates) == 2*r
    assert all(local_literal(g,s,x) for x in range(len(g)) if x not in s)
    # Every single deletion fails, checked with actual local K1,2 enumeration.
    failures = []
    for v in sorted(s):
        reduced = s - {v}
        x = next((x for x in sorted(set(range(len(g))) - reduced)
                  if not local_literal(g,reduced,x)), None)
        assert x is not None
        failures.append((v,x))
    for leaf, w in zip(leaves, ws):
        assert not local_literal(g,s-{leaf},w)
        assert leaf in g[w] and (g[w] & s)-{leaf} <= isolates
        assert [x for x in sorted(set(range(len(g)))-s)
                if not local_literal(g,s-{leaf},x)] == [w]
    if r <= 4:
        # Direct activity characterization cross-check; literal predicate above
        # is independent of this two-case shortcut.
        def active_formed(selected, x):
            ns = g[x] & selected
            return len(ns) >= 2 or any(g[v] & selected for v in ns)
        for reduced in [s] + [s-{v} for v in sorted(s)]:
            for x in sorted(set(range(len(g)))-reduced):
                assert active_formed(reduced,x) == local_literal(g,reduced,x)
        if r == 1:
            assert minimal(g,s)
            for reduced in [s] + [s-{v} for v in sorted(s)]:
                for x in sorted(set(range(len(g)))-reduced):
                    assert literal(g,reduced,x) == local_literal(g,reduced,x)
    cert = leaf_matching(g,s,leaves,c,isolates,ws,col,enumerate_small=(r==1))
    explicit_matching = [(12*i+u,12*i+v) for i in range(r)
                         for u,v in ((9,6),(11,7),(8,10))]
    assert all(v in g[u] for u,v in explicit_matching)
    assert {v for edge in explicit_matching for v in edge} == set(ws) | isolates
    assert len(explicit_matching) == cert['nu'] == 3*r
    assert cert['restricted_optimum'] == 7*r
    h = set(ws) | isolates
    explicit_cover = {12*i+v for i in range(r) for v in (9,10,11)}
    explicit_independent = {12*i+v for i in range(r) for v in (6,7,8)}
    assert len(explicit_cover) == len(explicit_independent) == 3*r
    assert explicit_cover | explicit_independent == h
    assert all(u in explicit_cover or v in explicit_cover for u in h for v in g[u] & h)
    assert all(not g[v] & explicit_independent for v in explicit_independent)
    printed_leaf_set = set(leaves) | explicit_independent
    assert len(printed_leaf_set) == 7*r and diss(g, printed_leaf_set)
    optimum = {12*i+v for i in range(r) for v in (0,1,3,5,6,7,8,10)}
    assert len(optimum) == 8*r and diss(g,optimum)
    factor = [[12*i+v for v in triple] for i in range(r)
              for triple in ((0,2,8),(1,4,10),(6,9,3),(7,11,5))]
    assert len({v for triple in factor for v in triple}) == len(g)
    assert sum(map(len,factor)) == len(g)
    assert all(triple[0] in g[triple[1]] and triple[2] in g[triple[1]]
               for triple in factor)
    # Each disjoint P3 permits at most two vertices in ANY dissociation set.
    assert 2*len(factor) == len(optimum)
    if r == 1:
        assert beta_literal(g) == 8
        assert beta_full_subsets(g) == 8
    degree = max(map(len,g))
    assert degree == (5 if connected and r > 1 else 4)
    seen, todo = {0}, [0]
    while todo:
        u = todo.pop()
        for v in g[u]-seen:
            seen.add(v)
            todo.append(v)
    assert (len(seen) == len(g)) == (connected or r == 1)
    # Orientation controls are still checked on the actual large graphs.
    wa = {w for w in ws if col[w] == 0}
    wb = set(ws)-wa
    jb = {z for z in isolates if g[z] & wa}
    ja = {z for z in isolates if g[z] & wb}
    da, db = (s-c-jb)|wa, (s-c-ja)|wb
    assert diss(g,da) and diss(g,db)
    assert len(da) == len(s)-len(c)+len(wa)-len(jb)
    assert len(db) == len(s)-len(c)+len(wb)-len(ja)
    return {'blocks':r,'connected':connected or r==1,'vertices':len(g),
            'edges':sum(map(len,g))//2,
            'selected_size':len(s),'beta':8*r,'restricted_optimum':7*r,
            'leaf_retaining_loss':r,'matching_number':3*r,'max_degree':degree,
            'orientation_sizes':[len(da),len(db)],
            'certificates':{'matching_dual_verified':True,'explicit_perfect_matching_verified':True,
                            'printed_cover_and_independent_set_verified':True,
                            'printed_leaf_retaining_set_verified':True,
                            'P3_factor_upper_bound':8*r,'dissociation_lower_bound':8*r,
                            'single_deletion_failures_checked':len(failures),
                            'unique_leaf_witnesses_checked':len(leaves),
                            'matching_edges_and_disjoint_endpoints_verified':True,
                            'optimal_D_induced_degrees_verified':True,
                            'leaf_retaining_D_induced_degrees_verified':True},
            **({'explicit_matching':explicit_matching,'matching_dual':cert,
                'optimal_dissociation':sorted(optimum),'P3_factor':factor,
                'deletion_failure_witnesses':failures} if r==1 else {})}


def main():
    if not __debug__:
        raise SystemExit('Assertions must be enabled; do not use -O.')
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1]/'output/star-leaf-budget-check.json')
    args = p.parse_args()
    ranges, counts = exhaust()
    target = graph(10,[(0,2),(0,3),(1,4),(1,5),(2,6),(3,7),(4,8),(5,9)]+list(product((6,7),(8,9))))
    fixtures = [summarize('forced_conflicting_opposite_P3s',target,set(range(6)))]
    assert fixtures[0]['beta'] == 6
    for spec in [fixture('shared_isolate_odd_threshold',[(0,'z'),(0,'z'),(1,None),(1,None)],dense=True),
                 fixture('touched_helpers_criterion_failure',[(0,'x'),(0,'y'),(1,'x'),(1,'y')],dense=True),
                 fixture('larger_stars_shared_helpers_edges',[(0,'z')]*3+[(1,'z')]*3,extras=True,dense=True)]:
        fixtures.append(summarize(*spec))
    assert fixtures[1]['budgets_c_e_t_bound_rounded_criterion'] == [[2,4,1,7,7,True]]
    assert fixtures[2]['checks']['criterion_failure'] > 0
    assert fixtures[2]['checks']['bound_below_selected'] > 0
    assert all(f['checks']['actual_target_failure'] == 0 for f in fixtures)
    control = graph(12,[(0,2),(0,3),(1,4),(1,5),(2,8),(3,9),(4,10),(5,11),
                        (8,6),(9,6),(10,7),(11,7)]+list(product((8,9),(10,11))))
    s = set(range(8))
    deletable = [v for v in s if forming(control,s-{v})]
    assert forming(control,s) and not minimal(control,s) and {0,1} <= set(deletable)
    assert beta_literal(control) == 7
    report = {'status':'PASS','scope':'All labelled fixed bipartitions of total order <=6, plus (3,4); all eligible minimal selections and all direct witness choices.',
              'exhaustive_ranges':ranges,'totals':dict(sorted(counts.items())),
              'fixtures':fixtures+[grid()],
              'block_obstructions':[block_family(r,connected)
                  for r in list(range(1,9))+[16,64,128] for connected in (False,True)],
              'exact_leaf_retaining_theorem':{
                  'H':'G[W union I], I all selected isolates',
                  'optimum':'|S|-c+e-nu(H)',
                  'sufficient_condition':'e-nu(H)>=c',
                  'argument':'Retained leaves exclude every centre. W union I must be independent because every chosen witness already has its own retained leaf. Conversely any independent set of H together with all leaves and unaffected selected edges is dissociation. Matching and equal-size vertex cover certify the exact optimum.'},
              'nonminimal_control':{'vertices':12,'selected':8,'beta':7,'deletable':deletable,'rejected_as_counterexample':True},
              'mathematical_issues':['No failed bound found. Matching criterion failure and restricted optimum below |S| are not actual beta failures.',
              'Witnesses are distinct across leaves; a leaf can have multiple admissible witnesses.',
              'Touched isolates are counted once per colour, not once per incident witness.',
              'Without isolates nu(H)<=floor(e/2) and e>=2c imply the sufficient matching criterion.',
              'Connected block certificates prove beta=8r and leaf-retaining optimum=7r on each checked r. No exact star-forming-number claim is made.']}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(report,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':'PASS','totals':report['totals']},sort_keys=True))


if __name__ == '__main__':
    main()
