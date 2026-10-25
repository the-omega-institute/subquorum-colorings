"""Cyclic beta escapes: exact gap cuts, pruning, costs, actual frozen control.

General proofs are in docs/CYCLIC_BETA_ESCAPE_CUTS.md. No SAT dependency.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_frozen_mixed_gate_cycle import load_model
from check_merger_completion_reserves import owner_data, feasible, frozen, whole_bands, whole_support_data
from check_frozen_beta_support_fork import restrict
from check_reserve_boundary_split import clipped
from check_joint_gate_resource_cuts import subsets, matching_rank
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Run without -O.')


def components(n, edges):
    adjacency = {v: set() for v in range(n)}
    for ends in edges.values():
        for v in ends:
            adjacency[v] |= ends - {v}
    left, result = set(range(n)), []
    while left:
        seen, todo = set(), [min(left)]
        while todo:
            v = todo.pop()
            if v not in seen:
                seen.add(v)
                todo.extend(adjacency[v] - seen)
        left -= seen
        result.append(seen)
    return result


def resource_trees(n, intervals):
    return [c for c in components(n, intervals)
            if sum(bool(ends & c) for ends in intervals.values()) == len(c)-1]


def gaps(n, deleted):
    if not deleted:
        return [set(range(n))]
    return components(n, {i: {i, (i+1) % n} for i in range(n) if i not in deleted})


def matching(adjacent):
    used = {}

    def augment(v, seen):
        for w in sorted(adjacent[v]):
            if w in seen:
                continue
            seen.add(w)
            if w not in used or augment(used[w], seen):
                used[w] = v
                return True
        return False

    for v in adjacent:
        augment(v, set())
    return {v: w for w, v in used.items()}


def criterion(n, trees, deleted):
    if not deleted:
        return not trees, {}, []
    blocks = gaps(n, deleted)
    assignment = matching({i: {k for k, block in enumerate(blocks) if tree & block}
                           for i, tree in enumerate(trees)})
    return len(assignment) == len(trees), assignment, blocks


def prune(n, trees, deleted):
    good, assignment, blocks = criterion(n, trees, deleted)
    assert good
    if not trees:
        return set()
    roots = sorted(min(trees[i] & blocks[k]) for i, k in assignment.items())
    chosen = set()
    for v, w in zip(roots, roots[1:]+roots[:1]):
        arc = [(v+j) % n for j in range((w-v) % n or n)]
        chosen.add(next(i for i in arc if i in deleted))
    assert chosen <= deleted and len(chosen) == len(trees)
    assert criterion(n, trees, chosen)[0]
    return chosen


def primitive_pack(n, intervals, beta, remaining=None, entry=None, exit_cost=None, beta_cost=None):
    """Independent route recursion: different source/gate/unit/beta masks.

    This does not call the component criterion, graph rank, or strand flow.
    """
    remaining = sorted(range(n) if remaining is None else remaining)
    units = sorted(intervals)
    beta_ids = sorted(set().union(set(), *beta.values()))
    uid = {u: i for i, u in enumerate(units)}
    bid = {b: i for i, b in enumerate(beta_ids)}
    choices = {}
    for s in remaining:
        choices[s] = []
        for g in (s, (s+1) % n):
            for u in units:
                if g in intervals[u]:
                    toll = 1 if entry is None else entry[s, g] + exit_cost[g, u]
                    choices[s].append((1 << g, 1 << uid[u], 0, toll))
        for b in beta.get(s, set()):
            toll = 1 if beta_cost is None else beta_cost[s, b]
            choices[s].append((0, 0, 1 << bid[b], toll))

    @lru_cache(None)
    def visit(i, gm, um, bm):
        if i == len(remaining):
            return 0, 0
        best = visit(i+1, gm, um, bm)
        for g, u, b, toll in choices[remaining[i]]:
            if gm & g or um & u or bm & b:
                continue
            v, c = visit(i+1, gm | g, um | u, bm | b)
            proposal = v+1, c+toll
            if (proposal[0], -proposal[1]) > (best[0], -best[1]):
                best = proposal
        return best

    return visit(0, 0, 0, 0)


def exact_deficit(n, trees, beta):
    all_sources = set(range(n))
    for u_size in range(n+1):
        for unpaid in itertools.combinations(range(n), u_size):
            U = set(unpaid)
            for E in subsets(all_sources-U):
                if matching_rank(E, beta) != len(E):
                    continue
                if criterion(n, trees, U | E)[0]:
                    return u_size
    raise AssertionError('Leaving every source unpaid always works.')


def minimum_full_beta_uses(n, trees, beta):
    good = [len(E) for E in subsets(range(n))
            if matching_rank(E, beta) == len(E) and criterion(n, trees, E)[0]]
    return min(good) if good else None


def weighted_matching_cost(vertices, intervals, exit_cost):
    vertices = sorted(vertices)
    units = sorted(intervals)

    @lru_cache(None)
    def visit(i, used):
        if i == len(vertices):
            return 0
        g = vertices[i]
        return min((exit_cost[g, u] + visit(i+1, used | (1 << j))
                    for j, u in enumerate(units) if not used >> j & 1 and g in intervals[u]),
                   default=float('inf'))

    return visit(0, 0)


def fixed_beta_cost_formula(n, intervals, E, entry, exit_cost):
    """Equation (3), excluding the already fixed beta-route tolls."""
    trees = resource_trees(n, intervals)
    assert len(E) == len(trees) and E
    good, _, blocks = criterion(n, trees, E)
    if not good:
        return float('inf')
    non_tree = set(range(n)) - set().union(set(), *trees)
    non_cost = weighted_matching_cost(non_tree, intervals, exit_cost)
    weights = {}
    for k, block in enumerate(blocks):
        # Order the path from its deleted incoming source edge.
        start = next(v for v in block if (v-1) % n in E)
        order = [(start+j) % n for j in range(len(block))]
        assert set(order) == block
        for i, tree in enumerate(trees):
            candidates = []
            for v in tree & block:
                root_pos = order.index(v)
                a_cost = sum(entry[order[j], order[j] if j < root_pos else order[j+1]]
                             for j in range(len(order)-1))
                b_cost = weighted_matching_cost(tree-{v}, intervals, exit_cost)
                candidates.append(a_cost+b_cost)
            weights[i, k] = min(candidates, default=float('inf'))
    return non_cost + min(sum(weights[i, k] for i, k in enumerate(perm))
                          for perm in itertools.permutations(range(len(blocks))))


def physical(totals):
    cur, data, meta, *_ = load_model()  # Rechecks actual strict freezing, solver free.
    own, alphas, betas, _ = owner_data(*data[:2])
    S = [own[v] for v in [(5,6), (5,19), (24,6), (5,4)]]
    G = [own[v] for v in [(5,5), (5,18), (24,18), (24,5)]]
    beta_edges = [((5,17), (5,16)), ((5,19), (5,20)), ((5,4), (5,3))]
    B = {i: own[v] for i, (_, v) in zip((0,1,3), beta_edges)}
    assert len(set(B.values())) == 3 and set(B.values()) <= betas
    Q = {meta['owner'][pos] for pos in [(6,15), (9,13)]}
    expected_intervals = {meta['owner'][6,15]: {1}, meta['owner'][9,13]: {2,3}}
    assert all({i for i, g in enumerate(G) if u in data[3][g]} == ends
               for u, ends in expected_intervals.items())
    records = {}
    for allowed in subsets(B):
        keep = set(S+G) | {B[i] for i in allowed}
        local = restrict(data, keep, Q)
        lo, la, lb, lm = owner_data(*local[:2])
        assert len(la) == len(lm) == 4 and len(lb) == len(allowed)
        expected_links = {(u,v) for u,v in data[2]
                          if own[u] in S and own[v] in G}
        expected_links |= {e for i,e in zip((0,1,3), beta_edges) if i in allowed}
        assert set(local[2]) == expected_links, 'ALL induced original links must be accounted for.'
        assert len(expected_links) == 8+len(allowed)
        assert all(not local[3][a] for a in la | lb)
        flow = fork_flow(*local)
        ordinary = optimize(*local, allow_forks=False)
        full = optimize(*local, allow_forks=True)
        beta_inc = {i: {i} if i in allowed else set() for i in range(4)}
        independent = primitive_pack(4, expected_intervals, beta_inc)
        expected = 2 if not allowed else 4 if 3 in allowed and len(allowed) >= 2 else 3
        assert (flow['value'],flow['cost']) == (ordinary['value'],ordinary['cost']) == (
            full['value'],full['cost']) == independent == (expected,expected)
        assert 4-exact_deficit(4,resource_trees(4,expected_intervals),beta_inc) == expected
        records[','.join('ABCD'[i] for i in sorted(allowed)) or 'none'] = dict(value=expected,cost=expected,
            minimum_full_beta_uses=minimum_full_beta_uses(4,resource_trees(4,expected_intervals),beta_inc))
        totals['actual_induced_interfaces'] += 1
        totals['independent_actual_ordinary_full_packs'] += 2
    trees = resource_trees(4,expected_intervals)
    good, match, blocks = criterion(4,trees,{0,1})
    assert not good and len(trees) == 2 and len(match) == 1
    full_flow = fork_flow(*clipped(data,Q))
    for forks in (False,True):
        check = optimize(*clipped(data,Q),allow_forks=forks)
        assert (check['value'],check['cost']) == (4,4)
    assert (full_flow['value'],full_flow['cost']) == (4,4)
    totals['complete_original_comparisons'] += 3
    # Literal separated frozen boards. Union/intersection terms count copy
    # deficits, while every beta and interval keeps its own original identity.
    for q in (2,3):
        for mode in range(10):
            T, M, gate_points, source_points, selected_betas = set(), [], [], [], []
            unit_positions, Ea, Eb, Ed = [], set(), set(), set()
            for i in range(q):
                shift = 32*i+2
                move = lambda v: (v[0]+shift,v[1])
                T |= {move(v) for v in cur[2]}
                M += [tuple(move(v) for v in e) for e in cur[3]]
                source_points += [move(v) for v in [(5,6),(5,19),(24,6),(5,4)]]
                gate_points += [move(v) for v in [(5,5),(5,18),(24,18),(24,5)]]
                unit_positions += [(16*i+1+b,c) for b,c in [(6,15),(9,13)]]
                mask = mode if mode < 8 else (i*3+mode) % 8
                for bit, (copyset, edge) in enumerate(zip((Ea,Eb,Ed),beta_edges)):
                    if mask >> bit & 1:
                        copyset.add(i)
                        selected_betas.append(move(edge[1]))
            joined = (32*q,24,T,M)
            assert feasible(joined) and frozen(joined)
            joined_data, joined_meta, _ = whole_support_data(joined,whole_bands(joined))
            joined_own, joined_alphas, _, _ = owner_data(*joined_data[:2])
            assert joined_alphas == {joined_own[v] for v in source_points}
            kept = joined_alphas | {joined_own[v] for v in gate_points+selected_betas}
            units = {joined_meta['owner'][pos] for pos in unit_positions}
            induced = restrict(joined_data,kept,units)
            local_flow = fork_flow(*induced)
            expected = 2*q + len(Ea|Eb|Ed) + len(Ed & (Ea|Eb))
            assert (local_flow['value'],local_flow['cost']) == (expected,expected)
            whole_flow = fork_flow(*clipped(joined_data,units))
            assert (whole_flow['value'],whole_flow['cost']) == (4*q,4*q)
            totals['separated_actual_frozen_copy_models'] += 1
    return dict(shape=cur[:2], endpoints=2*len(cur[3]), selected=len(cur[2]),
        actual_original_betas=len(betas), available_units=[meta['intervals'][u] for u in sorted(Q)],
        induced=records, failed_pair=dict(escaped=['A','B'],tree_count=2,gap_count=2,
            tree_gap_rank=1,gaps=[sorted(g) for g in blocks]),complete_original=dict(value=4,cost=4))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    rng = random.Random(2026102511)
    totals = Counter()
    for trial in range(420):
        n = rng.randint(3,7 if trial < 300 else 6)
        intervals = {u: set(rng.sample(range(n),rng.choice((1,2))))
                     for u in range(rng.randint(0,n+3))}
        trees = resource_trees(n,intervals)
        assert len(trees) == n-matching_rank(set(range(n)),
            {g:{u for u,ends in intervals.items() if g in ends} for g in range(n)})
        beta = {s:{b for b in range(n) if rng.randrange(4)==0} for s in range(n)}
        for E in subsets(range(n)):
            good, _, blocks = criterion(n,trees,E)
            gate_pack = primitive_pack(n,intervals,{},set(range(n))-E)
            assert good == (gate_pack[0] == n-len(E))
            if E:
                assert len(blocks) == len(E)
            totals['fixed_escape_criterion_comparisons'] += 1
            if good:
                pruned = prune(n,trees,E)
                assert len(pruned) == len(trees)
                totals['successful_prunings'] += 1
            if trial >= 300 and good and len(E) == len(trees) and E:
                entry = {(s,g):rng.randint(0,8) for s in range(n) for g in (s,(s+1)%n)}
                exit_cost = {(g,u):rng.randint(0,8) for u,ends in intervals.items() for g in ends}
                direct = primitive_pack(n,intervals,{},set(range(n))-E,entry,exit_cost)
                formula = fixed_beta_cost_formula(n,intervals,E,entry,exit_cost)
                assert direct == (n-len(E),formula)
                totals['weighted_fixed_beta_cost_comparisons'] += 1
        if trial >= 300:
            pack = primitive_pack(n,intervals,beta)
            deficit = exact_deficit(n,trees,beta)
            assert pack == (n-deficit,n-deficit)
            beta_min = minimum_full_beta_uses(n,trees,beta)
            assert beta_min == (len(trees) if deficit == 0 else None)
            totals['joint_deficit_independent_pack_comparisons'] += 1
    # Systematic four-gate controls, including disconnected trees, loops,
    # parallel interval identities, and every escaped-source subset.
    ends = [set(e) for e in itertools.combinations_with_replacement(range(4),2)]
    for choices in itertools.combinations_with_replacement(range(len(ends)),3):
        intervals = {u:ends[v] for u,v in enumerate(choices)}
        trees = resource_trees(4,intervals)
        for E in subsets(range(4)):
            good = criterion(4,trees,E)[0]
            assert good == (primitive_pack(4,intervals,{},set(range(4))-E)[0] == 4-len(E))
            if good:
                prune(4,trees,E)
            totals['systematic_four_gate_comparisons'] += 1
    actual = physical(totals)
    record = dict(status='PASS', totals=dict(totals), actual=actual,
        scope='General cyclic tree/gap Hall criterion, exact deficit, beta pruning and fixed-matching cost have written proofs. Actual induced owner interface is restricted; complete original board remains V4/c4. No universal compensation or5/6 improvement.')
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(record))


if __name__ == '__main__':
    main()
