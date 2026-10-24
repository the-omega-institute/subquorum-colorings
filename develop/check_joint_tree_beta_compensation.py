"""Exact joint support-interval / whole-beta allocation and weighted rerooting.

General proofs are in JOINT_TREE_BETA_COMPENSATION.md. Enumeration is a
regression and discovery tool, not a proof of the theorem or a grid bound.
"""
import argparse
from collections import Counter, defaultdict, deque
import itertools
import json
from pathlib import Path
import random

from check_one_sided_interval_allocation import allocate

if not __debug__:
    raise RuntimeError('Verification requires assertions; do not use -O.')


def min_cost_matching(demands, incidence, cost):
    """Independent flat successive shortest augmenting paths, Bellman--Ford.

    Resources are typed by the caller. Returns maximum cardinality FIRST,
    then minimum cost; negative costs preserve old assignments.
    """
    start, end = ('s',), ('t',)
    graph = defaultdict(list)

    def edge(a, b, c):
        forward, reverse = [b, 1, c, None], [a, 0, -c, None]
        forward[3], reverse[3] = reverse, forward
        graph[a].append(forward)
        graph[b].append(reverse)
        return forward

    for a in range(demands):
        edge(start, ('a', a), 0)
    arcs = {}
    for resource, owners in incidence.items():
        edge(('r', resource), end, 0)
        for a in sorted(owners):
            arcs[a, resource] = edge(('a', a), ('r', resource), cost(a, resource))
    nodes = list(graph)
    while True:
        distance, parent = {start: 0}, {}
        for _ in range(len(nodes)-1):
            changed = False
            for v in nodes:
                if v not in distance:
                    continue
                for arc in graph[v]:
                    w, capacity, c, _ = arc
                    if capacity and (w not in distance or distance[w] > distance[v]+c):
                        distance[w], parent[w] = distance[v]+c, (v, arc)
                        changed = True
            if not changed:
                break
        if end not in distance:
            break
        v = end
        while v != start:
            u, arc = parent[v]
            arc[1] -= 1
            arc[3][1] += 1
            v = u
    return {a: resource for (a, resource), arc in arcs.items() if arc[1] == 0}


def rooted_tree(vertices, resources, incidence, root):
    adjacency = defaultdict(list)
    for j in resources:
        assert len(incidence[j]) == 2
        a, b = sorted(incidence[j])
        adjacency[a].append((b, j))
        adjacency[b].append((a, j))
    distance, assignment, pending = {root: 0}, {}, deque([root])
    while pending:
        v = pending.popleft()
        for w, j in adjacency[v]:
            if w not in distance:
                distance[w], assignment[w] = distance[v]+1, j
                pending.append(w)
    assert set(distance) == set(vertices)
    assert set(assignment.values()) == set(resources)
    return assignment, distance


def joint_allocate(k, incidence, betas, baseline=None):
    canonical = allocate(k, incidence)
    baseline = dict(canonical['assignment'] if baseline is None else baseline)
    assert len(baseline) == k-len(canonical['deficient'])
    assert len(set(baseline.values())) == len(baseline)
    assert all(a in incidence[j] for a, j in baseline.items())
    assert all(users <= set(range(k)) for users in betas.values())
    trees, weights, roots = canonical['deficient'], {}, {}
    collapsed = {b: set() for b in betas}
    for i, tree in enumerate(trees):
        missing = set(tree['demands'])-set(baseline)
        assert len(missing) == 1
        old_root = next(iter(missing))
        old_assignment, distance = rooted_tree(tree['demands'], tree['resources'], incidence, old_root)
        assert old_assignment == {a: baseline[a] for a in tree['demands'] if a in baseline}
        for b, users in betas.items():
            candidates = set(tree['demands']) & users
            if candidates:
                root = min(candidates, key=lambda a: (distance[a], a))
                weights[i, b], roots[i, b] = distance[root], root
                collapsed[b].add(i)
    matched = min_cost_matching(len(trees), collapsed, lambda i, b: weights[i, b])
    interval_assignment, beta_assignment = dict(baseline), {}
    for i, b in matched.items():
        tree, root = trees[i], roots[i, b]
        new, _ = rooted_tree(tree['demands'], tree['resources'], incidence, root)
        interval_assignment = {a: j for a, j in interval_assignment.items() if a not in tree['demands']}
        interval_assignment.update(new)
        beta_assignment[root] = b
    paid = set(interval_assignment) | set(beta_assignment)
    mu, t = len(matched), len(trees)
    assert not set(interval_assignment) & set(beta_assignment)
    assert len(set(interval_assignment.values())) == len(interval_assignment)
    assert len(set(beta_assignment.values())) == mu
    assert set(interval_assignment.values()) == set(baseline.values())
    assert set(baseline) <= paid
    assert all(a in incidence[j] for a, j in interval_assignment.items())
    assert all(a in betas[b] for a, b in beta_assignment.items())
    assert len(paid) == k-t+mu
    changes = sum(interval_assignment.get(a) != j for a, j in baseline.items())
    assert changes == sum(weights[i, b] for i, b in matched.items())
    return dict(intervals=interval_assignment, betas=beta_assignment, paid=len(paid),
                t=t, mu=mu, changes=changes, baseline=baseline,
                collapsed=collapsed, matched=matched, trees=trees)


def all_assignments(k, incidence):
    def visit(a, used, assignment):
        if a == k:
            yield dict(assignment)
            return
        yield from visit(a+1, used, assignment)
        for j, owners in incidence.items():
            if a in owners and j not in used:
                assignment[a] = j
                yield from visit(a+1, used | {j}, assignment)
                del assignment[a]
    yield from visit(0, set(), {})


def verify(k, incidence, betas, totals, baseline=None, exhaustive=False):
    result = joint_allocate(k, incidence, betas, baseline)
    old = result['baseline']
    flat = {('I', j): users for j, users in incidence.items()}
    flat.update({('B', b): users for b, users in betas.items()})

    def score(assignment):
        return (len(assignment), -sum(r[0] == 'B' for r in assignment.values()),
                sum(assignment.get(a) == ('I', j) for a, j in old.items()))

    independent = min_cost_matching(k, flat,
        lambda a, r: k+1 if r[0] == 'B' else -int(old.get(a) == r[1]))
    target = (result['paid'], -result['mu'], len(old)-result['changes'])
    assert score(independent) == target, (incidence, betas, old, result, independent)
    if exhaustive:
        assert max(map(score, all_assignments(k, flat))) == target
        totals['flat_exhaustive_assignment_comparisons'] += 1
    totals['independent_flat_min_cost_comparisons'] += 1
    totals['positive_reroot_controls'] += result['changes'] > 0
    totals['shared_beta_controls'] += any(len(users) > 1 for users in result['collapsed'].values())
    totals['unrepaired_tree_controls'] += result['mu'] < result['t']
    return result


def physical_control(current, bands, totals, exhaustive=False):
    from check_boundary_sealed_gap_obstruction import support_allocation
    from check_bt_corridor_ports import compile_model
    from check_even_bridge_support_completion import endpoints_of
    from check_promotion_cores import frozen_certificate
    from check_residual_corridors import direct_check
    from check_terminal_cancellation_and_stranded_demand import all_link_matchings
    direct_check(*current)
    frozen, _ = frozen_certificate(current)
    assert frozen == endpoints_of(current)
    data, meta = compile_model(current, bands, Counter())
    kinds, pairs, links, _, _ = data
    choices = all_link_matchings(links) if exhaustive else ([],)+tuple([link] for link in links)
    examples = []
    for fixed in choices:
        before, model = support_allocation(current, bands, data, meta, fixed, Counter(), return_model=True)
        beta_pairs = [pair for pair in model['reduced'] if all(kinds[v] == 'BP' for v in pair)]
        alpha_owner = {v: a for a, pair in enumerate(model['alphas']) for v in pair}
        beta_owner = {v: b for b, pair in enumerate(beta_pairs) for v in pair}
        betas, witness = {b: set() for b in range(len(beta_pairs))}, {}
        for tp, bp in links:
            if tp in alpha_owner and bp in beta_owner:
                a, b = alpha_owner[tp], beta_owner[bp]
                betas[b].add(a)
                witness[a, b] = tp, bp
        result = verify(before['alpha'], model['incidence'], betas, totals)
        added = [witness[a, b] for a, b in result['betas'].items()]
        endpoints = [v for link in list(fixed)+added for v in link]
        assert len(endpoints) == len(set(endpoints))
        after, after_model = support_allocation(current, bands, data, meta, list(fixed)+added,
                                                Counter(), return_model=True)
        assert after['alpha'] == before['alpha']-result['mu']
        assert after['beta'] == before['beta']-result['mu']
        assert after['margin'] == before['margin']
        after_ids = {frozenset(pair): a for a, pair in enumerate(after_model['alphas'])}
        for a, j in result['intervals'].items():
            new = after_ids[frozenset(model['alphas'][a])]
            assert new in after_model['incidence'][j]
            # Every retained whole-support witness uses the same original strand.
            old_support = model['witness'][a, j]['original_strand']
            records = [c for c in after_model['records'] if set(c['ends']) == set(model['alphas'][a])]
            assert len(records) == 1 and set(pairs[old_support]) <= set(records[0]['vertices'])
        assert len(result['intervals'])+len(added) == before['alpha']-result['t']+result['mu']
        totals['frozen_fixed_c0_lift_checks'] += 1
        totals['physical_repaired_trees'] += result['mu']
        totals['physical_positive_reroot_controls'] += result['changes'] > 0
        totals['physical_nonsingleton_deficient_trees'] += sum(len(t['demands']) > 1 for t in result['trees'])
        if not fixed and result['t']:
            examples.append(dict(alpha=before['alpha'], beta=before['beta'], t=result['t'],
                mu=result['mu'], paid=result['paid'], changes=result['changes'],
                margin=before['margin'], extra_links=added,
                tree_sizes=[len(t['demands']) for t in result['trees']]))
    totals['frozen_geometry_controls'] += 1
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals, examples = Counter(), {}
    for k in range(4):
        owners = [set(c) for size in range(min(2, k)+1) for c in itertools.combinations(range(k), size)]
        all_beta_owners = [set(c) for size in range(k+1) for c in itertools.combinations(range(k), size)]
        for ii in itertools.product(owners, repeat=2):
            incidence = dict(enumerate(ii))
            optimum = len(allocate(k, incidence)['assignment'])
            baselines = [a for a in all_assignments(k, incidence) if len(a) == optimum]
            for bb in itertools.product(all_beta_owners, repeat=2):
                for baseline in baselines:
                    verify(k, incidence, dict(enumerate(bb)), totals, baseline, exhaustive=True)
                    totals['all_small_maximum_baselines'] += 1
    rng = random.Random(20261025)
    for _ in range(1600):
        k = rng.randrange(1, 23)
        incidence = {j: set(rng.sample(range(k), rng.randrange(min(k, 2)+1)))
                     for j in range(rng.randrange(2*k+1))}
        betas = {b: {a for a in range(k) if rng.randrange(5) == 0}
                 for b in range(rng.randrange(10))}
        verify(k, incidence, betas, totals)
    # Arbitrarily distant reroot and a genuine beta competition obstruction.
    for n in range(2, 41):
        incidence = {j: {j, j+1} for j in range(n-1)}
        baseline = {a: a-1 for a in range(1, n)}
        result = verify(n, incidence, {0: {n-1}}, totals, baseline)
        assert result['paid'] == n and result['mu'] == 1 and result['changes'] == n-1
    result = verify(4, {0: {0, 1}, 1: {2, 3}}, {0: {1, 3}}, totals)
    assert (result['t'], result['mu'], result['paid']) == (2, 1, 3)
    examples['shared_whole_beta_obstruction'] = dict(k=4, intervals=[[0, 1], [2, 3]],
        beta_owners=[[1, 3]], t=2, mu=1, deficit=1,
        scope='Abstract incidence counterexample to separate reuse of one beta; no frozen realization claimed.')

    from check_boundary_sealed_gap_obstruction import family
    from check_compensation_flow_geometry_frontier import pad_image
    from check_frozen_first_destination_allocation import fixture
    from check_interval_connector_cycles_and_missing_ports import whole_bands
    from check_one_sided_interval_allocation import chain_family
    from check_exchange_terminal_nonunique import fixture as bent_fixture, matching_orders
    base, crop, _ = family(6, 4, 10)
    physical_control(base, crop, totals, exhaustive=True)
    unported, _ = fixture()
    examples['unported_frozen_repairs'] = []
    for symmetry in itertools.product((False, True), repeat=3):
        for offset in ((2, 2), (3, 3)):
            current = pad_image(unported, symmetry, offset)
            examples['unported_frozen_repairs'] += physical_control(current, whole_bands(current), totals)
    bent = bent_fixture()
    for order in matching_orders():
        current = (*bent[:3], list(order['matching']))
        current = pad_image(current, (False, False, False), (2, 2))
        physical_control(current, whole_bands(current), totals, exhaustive=True)
    for n in range(2, 8):
        current, bands, _ = chain_family(6, n)
        physical_control(current, bands, totals)
    assert totals['physical_repaired_trees'] > 0
    assert totals['positive_reroot_controls'] > 0
    report = dict(status='PASS', totals=dict(totals), examples=examples,
        scope='General written joint allocation theorem and weighted rerooting proof; independent flat '
              'min-cost/exhaustive regression checks; actual frozen C0+C1 cancellation and retained-support checks. '
              'Only direct whole-beta links; mixed relays and a universal grid/5of6 bound are not established.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals))))


if __name__ == '__main__':
    main()
