"""Controls for fixed-M terminal constraints and simultaneous N-square switches.

General proofs are written in MIXED_TERMINAL_SQUARE_COMPENSATION.md. Neither
exhaustive small boards nor the family controls assert universal geometric Hall.
"""
from collections import Counter
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def edge(a, b):
    return tuple(sorted((a, b)))


def neighbours(u):
    r, c = u
    return {(r-1, c), (r+1, c), (r, c-1), (r, c+1)}


def grid(h, w):
    return {(r, c) for r in range(h) for c in range(w)}


def mates(board, matching, full=False):
    result = {}
    assert len(matching) == len(set(matching))
    for a, b in matching:
        assert a in board and b in board and b in neighbours(a)
        assert a not in result and b not in result
        result[a], result[b] = b, a
    if full:
        assert set(result) == board
    return result


def decompose(board, matching, auxiliary, selected):
    mm = mates(board, matching); nm = mates(board, auxiliary, full=True)
    q = board-mm.keys(); assert selected <= q
    holes = q-selected
    unseen = set(q); occupied_vertices = set(); used_m = set(); paths = []
    while unseen:
        start = min(unseen); path = [start]; resources = set(); n_edges = []
        while True:
            v = nm[path[-1]]; n_edges.append(edge(path[-1], v)); path.append(v)
            if v in q:
                break
            z = mm[v]; resources.add(edge(v, z)); path.append(z)
            assert len(path) == len(set(path))
        assert path[-1] in unseen and path[-1] != start
        assert len(path) == len(set(path)) and len(path) % 2 == 0
        assert not occupied_vertices & set(path)
        assert not used_m & resources
        occupied_vertices.update(path); used_m.update(resources)
        unseen -= {path[0], path[-1]}
        kind = 'TT' if path[0] in selected and path[-1] in selected else (
            'HH' if path[0] in holes and path[-1] in holes else 'TH')
        paths.append(dict(kind=kind, vertices=path, M=resources, N=n_edges))
    remainder = board-occupied_vertices
    assert remainder <= mm.keys()
    assert all(mm[u] in remainder and nm[u] in remainder for u in remainder)
    counts = Counter(path['kind'] for path in paths)
    a, b, t = [counts[k] for k in ['TT', 'HH', 'TH']]
    assert len(selected) == 2*a+t and len(holes) == 2*b+t
    assert len(holes)-len(selected) == 2*(b-a)
    assert 2*(len(selected)+len(matching)) == len(board)-2*(b-a)
    return dict(paths=paths, counts=(a, b, t), path_M=used_m,
                P=set(mm), Q=q, H=holes, remainder=remainder)


def square_candidates(h, w, auxiliary, data):
    owner = {e: i for i, path in enumerate(data['paths']) for e in path['N']}
    nset = set(auxiliary); result = []
    for r in range(h-1):
        for c in range(w-1):
            a, b, z, d = (r, c), (r, c+1), (r+1, c+1), (r+1, c)
            horizontal = {edge(a, b), edge(d, z)}
            vertical = {edge(a, d), edge(b, z)}
            for old, new in [(horizontal, vertical), (vertical, horizontal)]:
                if not old <= nset or not old <= owner.keys():
                    continue
                indices = [owner[e] for e in sorted(old)]
                kinds = [data['paths'][i]['kind'] for i in indices]
                if set(kinds) != {'TT', 'HH'}:
                    continue
                left = indices[kinds.index('TT')]; right = indices[kinds.index('HH')]
                result.append(dict(left=left, right=right, old=old, new=new,
                                   vertices={a, b, z, d}, square=(r, c)))
    return result


def component_matching(candidates):
    by_left = {}
    for i, candidate in enumerate(candidates):
        by_left.setdefault(candidate['left'], []).append(i)
    owner = {}
    def augment(left, seen):
        for index in by_left[left]:
            right = candidates[index]['right']
            if right in seen:
                continue
            seen.add(right)
            if right not in owner or augment(candidates[owner[right]]['left'], seen):
                owner[right] = index
                return True
        return False
    for left in sorted(by_left):
        augment(left, set())
    return list(owner.values())


def check_switches(h, w, matching, auxiliary, selected, exhaustive_batch=True):
    board = grid(h, w)
    old = decompose(board, matching, auxiliary, selected)
    candidates = square_candidates(h, w, auxiliary, old)
    chosen = component_matching(candidates)
    if exhaustive_batch:
        best = 0
        for mask in range(1 << len(candidates)):
            component_ids, vertices = set(), set(); size = 0
            for i, candidate in enumerate(candidates):
                if not mask >> i & 1:
                    continue
                ids = {candidate['left'], candidate['right']}
                if ids & component_ids:
                    break
                assert not vertices & candidate['vertices']
                component_ids |= ids; vertices |= candidate['vertices']; size += 1
            else:
                best = max(best, size)
        assert best == len(chosen)
    new_n = set(auxiliary); component_ids = set(); vertices = set()
    for i in chosen:
        candidate = candidates[i]
        ids = {candidate['left'], candidate['right']}
        assert not ids & component_ids and not vertices & candidate['vertices']
        assert not candidate['old'] & set(matching)
        assert not candidate['new'] & set(matching)
        component_ids |= ids; vertices |= candidate['vertices']
        new_n -= candidate['old']; new_n |= candidate['new']
    new = decompose(board, matching, sorted(new_n), selected)
    a, b, t = old['counts']; s = len(chosen)
    assert new['counts'] == (a-s, b-s, t+2*s)
    assert old['path_M'] == new['path_M']
    assert set(matching) & set(auxiliary) == set(matching) & new_n
    paid_t, paid_h, used_m = set(), set(), set()
    for path in new['paths']:
        if path['kind'] != 'TH':
            continue
        u, v = path['vertices'][0], path['vertices'][-1]
        if v in selected:
            u, v = v, u
        assert u in selected and v in new['H']
        assert u not in paid_t and v not in paid_h and not used_m & path['M']
        paid_t.add(u); paid_h.add(v); used_m |= path['M']
    assert len(paid_t) == len(paid_h) == t+2*s
    assert len(selected-paid_t) == 2*(a-s)
    assert len(new['H']-paid_h) == 2*(b-s)
    if s == a:
        assert paid_t == selected and len(selected) <= len(new['H'])
        assert len(selected)+len(matching) == len(board)//2-(b-a)
        assert 6*len(selected)+5*len(matching) == 3*len(board)-6*(b-a)-len(matching)
    return dict(before=old['counts'], after=new['counts'], candidates=len(candidates),
                repaired=s, full=s == a, used_actual_M=len(used_m), auxiliary=sorted(new_n))


def all_matchings(board, partial=False):
    if not board:
        yield []
        return
    u = min(board)
    if partial:
        yield from all_matchings(board-{u}, partial=True)
    for v in sorted(neighbours(u) & board):
        for tail in all_matchings(board-{u, v}, partial=partial):
            yield [edge(u, v)]+tail


def selected_feasible(p, t):
    return not p & t and all(len(neighbours(u) & (p | t)) <= 1 for u in t)


def exhaustive_strip():
    h, w = 2, 4; board = grid(h, w)
    full = list(all_matchings(board)); controls = positive = hall = unbalanced = 0
    cyclic = 0
    for m in all_matchings(board, partial=True):
        p = {u for e in m for u in e}; q = sorted(board-p)
        for n in full:
            for mask in range(1 << len(q)):
                t = {u for i, u in enumerate(q) if mask >> i & 1}
                out = check_switches(h, w, m, n, t)
                controls += 1; positive += out['repaired'] > 0
                hall += out['full'] and out['before'][0] > 0
                unbalanced += 2*len(t) != len(q)
                cyclic += len(set(m)-set(n)) > len(decompose(board, m, n, t)['path_M'])
    assert positive > 0 and hall > 0 and unbalanced > 0 and cyclic > 0
    return dict(controls=controls, positive_batches=positive,
                nonvacuous_full_Hall_cases=hall, unbalanced_partitions=unbalanced,
                lost_M_counts_including_unused_cycles=cyclic)


def family(b):
    assert b >= 0
    h, w = 4+2*b, 4
    m = [edge((0, 1), (0, 2)), edge((1, 1), (2, 1))]
    t = {(0, 0), (0, 3), (2, 0), (2, 3), (3, 1), (3, 3)}
    n0 = set(m) | {edge(a, z) for a, z in [
        ((0, 0), (1, 0)), ((0, 3), (1, 3)), ((2, 0), (3, 0)),
        ((3, 1), (3, 2)), ((1, 2), (2, 2)), ((2, 3), (3, 3))]}
    bad = {edge(a, z) for a, z in [
        ((1, 1), (2, 1)), ((0, 0), (0, 1)), ((0, 2), (0, 3)),
        ((1, 2), (1, 3)), ((2, 0), (1, 0)), ((3, 1), (3, 0)),
        ((3, 3), (3, 2)), ((2, 3), (2, 2))]}
    for j in range(b):
        for r in [4+2*j, 5+2*j]:
            t |= {(r, c) for c in range(4) if c % 2 == j % 2}
            band_edges = {edge((r, c), (r, c+1)) for c in (0, 2)}
            n0 |= band_edges; bad |= band_edges
    return h, w, m, sorted(n0), sorted(bad), t


def family_control(b):
    h, w, m, n0, bad, t = family(b); board = grid(h, w)
    p = {u for e in m for u in e}; holes = board-p-t
    assert selected_feasible(p, t)
    assert len(t) == len(holes) == 6+4*b and len(t)+len(m) == len(board)//2
    assert {(u[0]+u[1]) % 2 for u in t} == {0, 1}
    assert not neighbours((1, 2)) & t
    assert len(set(m) & set(n0)) == 2
    assert len(list(all_matchings(p))) == 1
    failed = check_switches(h, w, m, n0, t)
    assert failed['candidates'] == 0 and failed['before'] == (1, 1, 4+4*b)
    repaired = check_switches(h, w, m, bad, t)
    assert repaired['candidates'] == repaired['repaired'] == 1
    assert repaired['before'] == (1, 1, 4+4*b) and repaired['after'] == (0, 0, 6+4*b)
    assert repaired['used_actual_M'] == 1
    assert len(set(m) & set(repaired['auxiliary'])) == 1
    return dict(bands=b, height=h, T=len(t), H=len(holes), M=2,
                J=len(board)//2, exact_R_all=2, exact_R_TH=1,
                exact_legal_cost=1, exact_terminal_penalty=1,
                one_square_repairs_without_extra_M=True)


def core_optimization_controls():
    """Separate bitmask enumeration of all full N, partial M and balanced T.

    Compare actual component path cost with direct retained-edge intersection.
    Square-certificate assertions are separate from this optimizer.
    """
    count = 16; adj = [[v for v in range(count)
                        if abs(u//4-v//4)+abs(u%4-v%4) == 1] for u in range(count)]
    board = set(range(count))
    edges = [(u, v) for u in board for v in adj[u] if u < v]
    index = {e: i for i, e in enumerate(edges)}
    def generate(rest, partial):
        if not rest:
            yield []
            return
        u = min(rest)
        if partial:
            yield from generate(rest-{u}, True)
        for v in adj[u]:
            if v in rest:
                for tail in generate(rest-{u, v}, partial):
                    yield [(u, v)]+tail
    def encode(es):
        mm = [-1]*count; mask = 0
        for u, v in es:
            mm[u], mm[v] = v, u; mask |= 1 << index[tuple(sorted((u, v)))]
        return mm, mask
    ns = [encode(es) for es in generate(board, False)]
    assert len(ns) == 36
    models = pairs = overcounts = feasible = mixed = penalty = absent = 0
    example = None
    for es in generate(board, True):
        mm, mask = encode(es); q = [u for u in board if mm[u] < 0]
        p = sum(1 << u for u in board if mm[u] >= 0)
        options = []
        for nm, nmask in ns:
            unseen = set(q); terminal_pairs = []; used = set(); cost = 0
            while unseen:
                start = min(unseen); v = start; seen = {v}
                while True:
                    v = nm[v]; assert v not in seen; seen.add(v)
                    if mm[v] < 0:
                        break
                    v = mm[v]; cost += 1; assert v not in seen; seen.add(v)
                assert not seen & used and v in unseen and v != start
                used |= seen; unseen -= {start, v}; terminal_pairs.append((start, v))
            retained = (mask & nmask).bit_count(); lost = len(es)-retained
            assert cost <= lost
            overcounts += cost < lost; pairs += 1
            options.append((cost, retained, terminal_pairs))
        r_all = max(x[1] for x in options)
        assert min(x[0] for x in options) == len(es)-r_all
        for combo in combinations(q, len(q)//2):
            t = sum(1 << u for u in combo); occupied = p | t
            if any(sum(bool(occupied >> v & 1) for v in adj[u]) > 1 for u in combo):
                continue
            feasible += 1
            colours = {(u//4+u%4) % 2 for u in combo}; mixed += len(colours) == 2
            legal = [o for o in options if all(((t >> u) & 1)+((t >> v) & 1) == 1
                                              for u, v in o[2])]
            if not legal:
                absent += 1
                continue
            r_th = max(o[1] for o in legal); actual = min(o[0] for o in legal)
            assert actual == len(es)-r_th
            assert actual == len(es)-r_all+(r_all-r_th)
            penalty += r_all > r_th
            if r_all > r_th and example is None:
                example = dict(M=es, T=combo, R_all=r_all, R_TH=r_th, actual_cost=actual)
        models += 1
    @lru_cache(None)
    def independent_count(rest):
        if not rest:
            return 1
        u = (rest & -rest).bit_length()-1
        return independent_count(rest ^ (1 << u))+sum(
            independent_count(rest ^ (1 << u) ^ (1 << v)) for v in adj[u] if rest >> v & 1)
    assert models == independent_count((1 << count)-1) == 10012
    assert pairs == models*36 and overcounts > 0 and penalty > 0
    return dict(partial_M=models, full_N=36, M_N_pairs=pairs,
                unused_cycle_overcount_cases=overcounts,
                feasible_balanced_selections=feasible, mixed_colour_cases=mixed,
                strict_terminal_penalty_cases=penalty, no_admissible_N_cases=absent,
                first_strict_case=example)


def main():
    strip = exhaustive_strip()
    rows = [family_control(b) for b in range(41)]
    optimization = core_optimization_controls()
    result = dict(status='PASS', exhaustive_2by4=strip, family_parameters=len(rows),
                  smallest=rows[0], largest=rows[-1], core_optimization=optimization,
                  scope='Written fixed-M TT/HH square and simultaneous component-matching compensation; exact residuals and conditional weighted bound; balanced constrained-retention equivalence; all-length feasible mixed penalty-one family.',
                  trust_boundary='The path decomposition, arm gluing, Hall and all-length coordinate argument are written proofs. Small exhaustive controls are not universal Hall/retention feasibility evidence. No universal 5/6 improvement, freezing or end-to-end grid Lean is claimed.')
    (ROOT/'output/mixed-terminal-compensation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
