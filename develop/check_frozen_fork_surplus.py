"""Deterministic controls for the frozen fork theorem and exact row surplus.

The general proofs are in docs/FROZEN_FORK_EXCLUSION_AND_ROW_SURPLUS.md.
No solver or finite list is used as a replacement for those proofs.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors, occupied_degrees
from check_even_bridge_support_completion import endpoints_of
from check_frozen_first_destination_allocation import fixture as unported_fixture, maximum_matching
from check_interval_connector_cycles_and_missing_ports import stack, whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import terminal_data, cancel_pairs

if not __debug__:
    raise RuntimeError('Run without -O: validation requires assertions.')


def row_components(tips, adjacency):
    graph = defaultdict(set)
    for a in tips:
        for d in adjacency[a]:
            graph[a].add(d)
            graph[d].add(a)
    remaining, result = set(graph), []
    while remaining:
        start = min(remaining)
        reached, pending = {start}, [start]
        while pending:
            for other in graph[pending.pop()]-reached:
                reached.add(other)
                pending.append(other)
        remaining -= reached
        ends = sorted(v for v in reached if len(graph[v]) == 1)
        assert len(ends) == 2 and sum(len(graph[v]) for v in reached) == 2*(len(reached)-1)
        aa, dd = reached & tips, reached-tips
        surplus = len(dd)-len(aa)
        assert (len(reached) == 2 and surplus == 0) or (surplus == 1 and not set(ends) & tips)
        result.append((aa, dd, surplus))
    return result


def minimum_mixed_matching(tips, adjacency, mixed):
    """Independent subset DP over actual BP terminals, keeping minimum cost."""
    targets = sorted(set().union(*(adjacency[a] for a in tips))) if tips else []
    index = {d: i for i, d in enumerate(targets)}
    states = {0: 0}
    for a in sorted(tips):
        following = {}
        for mask, cost in states.items():
            for d in adjacency[a]:
                bit = 1 << index[d]
                if not mask & bit:
                    key, value = mask | bit, cost+int(d in mixed)
                    following[key] = min(value, following.get(key, value))
        states = following
    assert states
    return min(states.values())


def inspect(current, totals, subsets=True):
    direct_check(*current)
    endpoints = endpoints_of(current)
    assert frozen_certificate(current)[0] == endpoints
    original, labels, intervals, interval_owner, kinds, pairs, ports = terminal_data(current, whole_bands(current))
    owner = {v: i for i, pair in enumerate(pairs) for v in pair}
    alpha = {i for i, pair in enumerate(pairs) if all(kinds[v] == 'TP' for v in pair)}
    beta = {i for i, pair in enumerate(pairs) if all(kinds[v] == 'BP' for v in pair)}
    mixed = set(range(len(pairs)))-alpha-beta
    # An original open strand consists of q matching edges and q-1 band edges.
    assert all((sum(a)-sum(b)) % 2 == 1 for a, b in pairs)
    all_tips = {v for i in alpha for v in pairs[i]}
    mate = {a: b for e in current[3] for a, b in (e, e[::-1])}
    forks = []
    for d in kinds:
        if kinds[d] != 'BP':
            continue
        u, w = (d[0], d[1]-1), (d[0], d[1]+1)
        if u in all_tips and w in all_tips:
            direction = mate[u][0]-u[0]
            assert direction in (-1, 1) and mate[w] == (w[0]+direction, w[1])
            assert mate[d] == (d[0]+direction, d[1])
            assert (u[0], u[1]-1) not in current[2]
            assert (w[0], w[1]+1) not in current[2]
            forks.append((u, d, w))
    missing = {v for v in all_tips if not ports[v]}
    adjacency = {a: {d for d in kinds if kinds[d] == 'BP' and a[0] == d[0]
                      and abs(a[1]-d[1]) == 1} for a in missing}
    assert all(1 <= len(ds) <= 2 for ds in adjacency.values())
    choices = [set(missing)]
    if subsets and len(missing) <= 12:
        ordered = sorted(missing)
        choices = [{a for i, a in enumerate(ordered) if mask >> i & 1}
                   for mask in range(1 << len(ordered))]
    example = None
    for tips in choices:
        components = row_components(tips, adjacency)
        targets = set().union(*(dd for _, dd, _ in components)) if components else set()
        c = sum(s for _, _, s in components)
        assert len(targets) == len(tips)+c
        assert all(len({owner[d] for d in dd}) == len(dd) for _, dd, _ in components)
        mixed_tips = {d for d in targets if owner[d] in mixed}
        cm = sum(bool(dd & mixed_tips) for _, dd, s in components if s)
        # Construct an injection omitting any prescribed target on each surplus path.
        assignment = {}
        for aa, dd, surplus in components:
            omit = min(dd & mixed_tips) if surplus and dd & mixed_tips else (min(dd) if surplus else None)
            remaining = set(dd)-({omit} if omit is not None else set())
            # Leaf elimination on the path after deleting the chosen D root.
            pending = set(aa)
            while pending:
                a = next(a for a in sorted(pending) if len(adjacency[a] & remaining) == 1)
                d = next(iter(adjacency[a] & remaining))
                assignment[a] = d
                pending.remove(a)
                remaining.remove(d)
            assert not remaining
        assert len(set(assignment.values())) == len(tips)
        assert sum(d in mixed_tips for d in assignment.values()) == len(mixed_tips)-cm
        if len(tips) <= 12:
            assert minimum_mixed_matching(tips, adjacency, mixed_tips) == len(mixed_tips)-cm
            totals['independent_minimum_mixed_controls'] += 1
        totals['tip_subset_controls'] += 1
        totals['surplus_row_components'] += c
        if tips == missing:
            example = dict(missing=sorted(tips), targets=sorted(targets), c=c,
                           q=len(mixed_tips), c_m=cm, minimum_mixed=len(mixed_tips)-cm,
                           assignment=sorted(assignment.items()),
                           row_components=[dict(alpha_tips=sorted(aa), bp_tips=sorted(dd),
                                                owners=[owner[d] for d in sorted(dd)], surplus=s)
                                           for aa, dd, s in components])
    unported = sorted(i for i in alpha if set(pairs[i]) <= missing)
    for mask in range(1 << len(unported)):
        chosen = {a for i, a in enumerate(unported) if mask >> i & 1}
        tips = {v for a in chosen for v in pairs[a]}
        components = row_components(tips, adjacency)
        targets = set().union(*(dd for _, dd, _ in components)) if components else set()
        c = sum(s for _, _, s in components)
        nb = {owner[d] for d in targets} & beta
        nm = {owner[d] for d in targets} & mixed
        assert 2*len(chosen)+c <= 2*len(nb)+len(nm)
        totals['weighted_owner_hall_controls'] += 1
    if all_tips <= missing:
        f = dict(example['assignment'])
        beta_incidence = {a: {owner[f[v]] for v in pairs[a] if owner[f[v]] in beta} for a in alpha}
        beta_paid = len(maximum_matching(beta_incidence))
        assert len(alpha)-beta_paid <= example['minimum_mixed']//2
        example['optimized_beta_payments'] = beta_paid
        totals['optimized_beta_deficit_controls'] += 1
    if all_tips <= missing and example['minimum_mixed'] == 0:
        f = dict(example['assignment'])
        incidence = {a: {owner[f[v]] for v in pairs[a]} for a in alpha}
        matching = maximum_matching(incidence)
        assert len(matching) == len(alpha) and set(matching.values()) <= beta
        links = [next((v, f[v]) for v in pairs[a] if owner[f[v]] == target)
                 for a, target in sorted(matching.items())]
        _, inventory, _ = cancel_pairs(kinds, pairs, links, Counter())
        assert inventory['TP', 'TP'] == 0
        assert inventory['BP', 'BP'] == len(beta)-len(alpha)
        example['beta_only_certificate'] = dict(alpha=len(alpha), beta=len(beta),
            distinct_beta_owners=sorted(matching.values()), links=links,
            compensation=len(links), remaining_alpha=0)
        totals['complete_beta_only_class_controls'] += 1
        totals['nonempty_complete_beta_only_controls'] += bool(alpha)
    totals['frozen_geometries'] += 1
    totals['forks'] += len(forks)
    return example


def nonfrozen_control():
    current = (8, 8, {(2, 2), (2, 4), (3, 1), (5, 2), (5, 4)},
               [((3, c), (4, c)) for c in (2, 3, 4)])
    direct_check(*current)
    assert min(occupied_degrees(current).values()) >= 3
    _, _, _, _, kinds, pairs, _ = terminal_data(current, whole_bands(current))
    assert any(set(pair) == {(3, 2), (4, 2)} for pair in pairs)
    assert kinds[(3, 2)] == kinds[(3, 4)] == 'TP' and kinds[(3, 3)] == 'BP'
    blocked = {(3, 3), (4, 2)}
    endpoints, selected = endpoints_of(current), current[2]
    mate = {a: b for e in current[3] for a, b in (e, e[::-1])}
    for v in blocked:
        outside = {w for w in neighbors(v) if w != mate[v]
                   and (w in selected or (w in endpoints and mate[w] not in blocked))}
        assert len(outside) <= 1
    frozen, _ = frozen_certificate(current)
    assert not frozen & blocked
    return dict(shape=current[:2], selected=sorted(selected), matching=current[3],
                blocked=sorted(blocked), frozen=sorted(frozen),
                scope='Feasible degree-three fork with outer T; not fully frozen. Not a target-bound counterexample.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals = Counter()
    # Reuse all 480 physical controls of the exact-exchange checker without solving flows again.
    # Generate the same family inventory directly; avoid mocks of verification routines.
    from check_compensation_flow_geometry_frontier import pad_image
    from check_elbow_sources import elbow
    from check_exchange_terminal_nonunique import fixture, graft, matching_orders
    from check_frozen_shared_mixed_gate import fixture as shared_fixture
    from check_promotion_cores import tight_diamond
    from degree_three_fusion import occupied_bands
    from rotor_networks import combine, rotor, star_modules, transform_module
    base = fixture()
    fixtures = [(*base[:3], list(x['matching'])) for x in matching_orders()]
    fixtures += [graft(6, 4), elbow(6, 4), tight_diamond()[0], occupied_bands(6)[0],
                 unported_fixture()[0], shared_fixture()]
    fixtures += [stack(6, 4, [kind]) for kind in ('missing', 'collision', 'cycle')]
    module = rotor()
    fixtures.append((6, 6, module['selected'], module['matching']))
    for width in (6, 10, 20):
        network = combine([transform_module(module, (False, False, False), (width-2, width-2))
                           for module in star_modules(width)])
        fixtures.append((2*width+2, 2*width+2, network['selected'], network['matching']))
    for model, symmetry, offset in itertools.product(fixtures,
            itertools.product((False, True), repeat=3), itertools.product((2, 3), repeat=2)):
        inspect(pad_image(model, symmetry, offset), totals)
    totals['carried_physical_geometries'] = totals['frozen_geometries']
    for width, height, kind in itertools.product(range(6, 31, 2), range(4, 21, 2),
                                                 ('missing', 'cycle', 'collision')):
        inspect(stack(width, height, [kind]), totals)
    for cycles, collisions, missing in itertools.product(range(3), repeat=3):
        if cycles+collisions+missing:
            inspect(stack(6, 4, ['cycle']*cycles+['collision']*collisions+['missing']*missing), totals)
    sat_path = Path(__file__).resolve().parents[1] / 'output/frozen-shared-beta-free-ports-14x20.json'
    sat = json.loads(sat_path.read_text())
    sat_model = (*sat['shape'], set(map(tuple, sat['selected'])), [tuple(map(tuple, e)) for e in sat['matching']])
    sat_result = inspect(sat_model, totals)
    from check_beta_exchange_gate_reduction import physical_data, compile_and_lift, protected_value
    data = physical_data(sat_model)
    core = [tuple(map(tuple, sat['intended_core_link']))]
    exchange = compile_and_lift(*data, core)
    protected = protected_value(*data, core)
    assert exchange['full_value'] == protected == sat['exchange_verification']['full_value'] == 2
    assert exchange['used_exchange_gates'] == 0
    sat_result['exchange_replay'] = dict(full_value=2, protected_value=protected, used_exchange_gates=0)
    example = inspect(unported_fixture()[0], totals)
    report = dict(status='PASS', totals=dict(totals), unported_fixture=example,
                  shared_beta_fixture=sat_result, nonfrozen_control=nonfrozen_control(),
                  scope='Written general fork exclusion and exact missing-tip row surplus; finite geometry and '
                        'independent minimum-cost injection controls. No universal grid bound or route coverage claimed.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals), example=example)))

if __name__ == '__main__':
    main()
