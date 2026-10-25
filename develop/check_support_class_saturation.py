"""Pointwise cancellation preservation and the original singleton-pair core.

Solver-free checks only; arbitrary-size proofs are in the companion note.
"""
import argparse
from collections import Counter, defaultdict
import itertools as it
import json
from pathlib import Path
import random

from check_whole_support_fork_normal_form import canonical, whole_support_data, evaluate
from check_whole_support_fork_flow import fork_flow
from check_compensation_flow_normal_form import owner_data
from check_terminal_cancellation_and_stranded_demand import all_link_matchings, cancel_pairs
from check_endpoint_component_resource_gluing import physical_groups, local, restrict, path_family
from check_single_square_routing import prune, shared_gap
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def support_classes(d):
    classes = defaultdict(set)
    for j in d[4]:
        U = frozenset(o for o, W in d[3].items() if j in W)
        classes[U].add(j)
    return dict(classes)


def saturate(d, cross_only=False, component=None):
    W = {o: set(js) for o, js in d[3].items()}; selectors = {}
    for U, units in support_classes(d).items():
        if not U or len(units) < len(U):
            continue
        if cross_only and len({component[o] for o in U}) <= 1:
            continue
        e = dict(zip(sorted(U), sorted(units))); selectors[U] = e
        for o in U:
            W[o] -= units; W[o].add(e[o])
    return (*d[:3], W, set(d[4])), selectors


def virtual_owners(d, C):
    owner, _, _, _ = owner_data(*d[:2])
    _, _, comps = cancel_pairs(d[0], d[1], list(C), Counter())
    return [{owner[v] for v in c['vertices']} for c in comps
            if not c['cycle'] and c['alpha'] == c['beta']+1]


def allocation(d, groups, paid):
    """Independent small DFS matching, retaining an original owner witness."""
    choices = {i: {j: next(o for o in sorted(groups[i]) if j in d[3][o])
                   for j in sorted(d[4]) if any(j in d[3][o] for o in groups[i])} for i in paid}
    order = sorted(paid, key=lambda i: len(choices[i]))
    def visit(t, used):
        if t == len(order):
            return {}
        i = order[t]
        for j, o in choices[i].items():
            if j not in used:
                rest = visit(t+1, used | {j})
                if rest is not None:
                    return {i: (j, o), **rest}
        return None
    return visit(0, set())


def fixed_matching_check(d, sharp, selectors, C, totals):
    groups = virtual_owners(d, C)
    old_classes = {j: U for U, js in support_classes(d).items() for j in js}
    before = evaluate(*d[:2], list(C), *d[3:])
    after = evaluate(*sharp[:2], list(C), *sharp[3:])
    assert before['value'] == after['value'] and before['remaining_beta'] == after['remaining_beta']
    if len(groups) <= 7:
        masks = range(1 << len(groups)); totals['fixed_matchings_with_all_paid_subsets'] += 1
    else:
        full = (1 << len(groups))-1
        rng = random.Random(202610250627+len(groups))
        masks = {0, full} | {1 << i for i in range(len(groups))}
        masks |= {full ^ (1 << i) for i in range(len(groups))}
        masks |= {rng.getrandbits(len(groups)) for _ in range(32)}
        totals['fixed_matchings_with_sampled_paid_subsets'] += 1
    for mask in masks:
        paid = {i for i in range(len(groups)) if mask >> i & 1}
        old = allocation(d, groups, paid); new = allocation(sharp, groups, paid)
        assert (old is None) == (new is None)
        if old is not None:
            mapped = {i: (selectors[old_classes[j]][o] if old_classes[j] in selectors else j)
                      for i, (j, o) in old.items()}
            assert len(set(mapped.values())) == len(mapped)
            assert all(mapped[i] in sharp[3][o] for i, (_, o) in old.items())
            assert len({o for _, o in old.values()}) == len(old)
        totals['prescribed_virtual_alpha_subsets'] += 1
    totals['fixed_terminal_matchings'] += 1


def inspect(d, totals, rng, exhaustive=False, sampled=12):
    sharp, selectors = saturate(d)
    assert sharp[4] == d[4] and all(sharp[3][o] <= d[3][o] for o in d[3])
    a = fork_flow(*d); b = fork_flow(*sharp)
    assert (a['value'], a['cost']) == (b['value'], b['cost'])
    if exhaustive:
        for C in all_link_matchings(d[2]):
            fixed_matching_check(d, sharp, selectors, C, totals)
    else:
        cases = [[], a['links'], b['links']]
        for _ in range(sampled):
            edges = list(d[2]); rng.shuffle(edges); used = set(); C = []
            for e in edges:
                if not set(e) & used and rng.random() < .5:
                    C.append(e); used.update(e)
            cases.append(C)
        for C in cases:
            fixed_matching_check(d, sharp, selectors, C, totals)
    totals['models'] += 1
    totals['saturated_nonempty_classes'] += len(selectors)
    totals['removed_support_incidences'] += sum(len(d[3][o])-len(sharp[3][o]) for o in d[3])
    totals['models_with_removed_incidences'] += sharp[3] != d[3]
    totals['models_with_fork_optimum'] += any(c['kind'] == 'fork' for c in a['certificates'])
    return a, sharp


def singleton_core_check(d, groups, totals):
    owner, A, _, _ = owner_data(*d[:2])
    assert set().union(set(), *groups) == set(range(len(d[1])))
    active = [g for g in groups if g & A]
    removed = {o for g in groups if not g & A for o in g}
    kept = [o for o in range(len(d[1])) if o not in removed]
    renumber = {o: i for i, o in enumerate(kept)}
    d = prune(d, removed)
    groups = [{renumber[o] for o in g} for g in active]
    comp = {o: i for i, g in enumerate(groups) for o in g}
    assert all(len(U) <= 2 for U in support_classes(d))
    E = set()
    cross_units = 0; cross_classes = 0
    for U, js in support_classes(d).items():
        if len({comp[o] for o in U}) == 2:
            cross_units += len(js); cross_classes += 1
            if len(js) == 1:
                E |= js
    sharp, _ = saturate(d, True, comp)
    assert len(E) <= 12, 'Exhaustive singleton-core control intentionally bounded.'
    values = []; orientations = []; Q = d[4]; units = sorted(E)
    endpoints = {j: sorted({comp[o] for o, W in d[3].items() if j in W}) for j in E}
    base = [fork_flow(*local(d, g, Q)) for g in groups]
    for mask in range(1 << len(units)):
        J = {j for i, j in enumerate(units) if mask >> i & 1}; R = Q-J
        vi = [fork_flow(*local(d, g, R))['value'] for g in groups]
        reduced_vi = [fork_flow(*local(sharp, g, R))['value'] for g in groups]
        assert vi == reduced_vi
        values.append(len(J)+sum(vi)); totals['singleton_core_withdrawals'] += 1
        assigned = {j: endpoints[j][(mask >> i) & 1] for i, j in enumerate(units)}
        local_optima = [fork_flow(*local(d, g, (Q-E) | {j for j in E if assigned[j] == i}))
                        for i, g in enumerate(groups)]
        orientations.append((sum(v['value'] for v in local_optima), sum(v['cost'] for v in local_optima)))
        totals['singleton_core_orientations'] += 1
    full = fork_flow(*d); reduced = fork_flow(*sharp)
    assert min(values) == full['value'] == reduced['value']
    assert full['cost'] == reduced['cost']
    assert max(orientations, key=lambda x: (x[0], -x[1])) == (full['value'], full['cost'])
    totals['strict_joint_value_losses'] += full['value'] < sum(v['value'] for v in base)
    totals['strict_joint_cost_losses_at_equal_value'] += (full['value'] == sum(v['value'] for v in base)
                                                        and full['cost'] > sum(v['cost'] for v in base))
    if not E:
        assert (full['value'], full['cost']) == (sum(v['value'] for v in base), sum(v['cost'] for v in base))
        totals['empty_core_value_and_cost_additivity'] += 1
        totals['empty_core_multiple_active_additivity'] += len(groups) >= 2
    totals['singleton_core_models'] += 1
    return dict(active_components=len(groups), cross_units_before=cross_units,
                cross_support_classes=cross_classes, singleton_core_units=sorted(E),
                local_value_cost=[[v['value'], v['cost']] for v in base],
                global_value_cost=[full['value'], full['cost']],
                orientation_value_cost=list(max(orientations, key=lambda x: (x[0], -x[1]))))


def abstract_checks(totals):
    rng = random.Random(202610250625)
    for index in range(160):
        types = 'AA'+''.join(rng.choice('ABM') for _ in range(1+index % 5))
        kinds, pairs, possible = canonical(types); rng.shuffle(possible)
        links = possible[:rng.randrange(min(9, len(possible))+1)]
        W = {o: set() for o in range(len(pairs))}; Q = set()
        for _ in range(1+index % 5):
            U = set(rng.sample(range(len(pairs)), rng.randrange(1, min(len(pairs), 4)+1)))
            count = rng.randrange(1, len(U)+3)
            js = set(range(len(Q), len(Q)+count)); Q |= js
            for o in U:
                W[o] |= js
        inspect((kinds, pairs, links, W, Q), totals, rng, exhaustive=True)
    # Arbitrary layering and two beta entries, with duplicate beta-body resources.
    kinds, pairs, _ = canonical('AAMMB')
    fork = (kinds, pairs, [(0, 4), (5, 6), (7, 8), (2, 9)],
            {0: set(), 1: set(), 2: set(), 3: set(), 4: {0, 1, 2}}, {0, 1, 2})
    answer, _ = inspect(fork, totals, rng, True)
    assert (answer['value'], answer['cost']) == (2, 4)
    assert any(c['kind'] == 'fork' for c in answer['certificates'])
    for index in range(100):
        kinds, pairs, possible = canonical('AAMMBAMB')
        groups = [{0, 1, 2, 3, 4}, {5, 6, 7}]
        comp = {o: i for i, g in enumerate(groups) for o in g}
        links = [e for e in possible if comp[e[0]//2] == comp[e[1]//2] and rng.random() < .3]
        rng.shuffle(links); links = links[:10]
        W = {o: set() for o in range(len(pairs))}; Q = set(range(1+index % 8))
        for j in Q:
            for o in rng.sample(range(len(pairs)), rng.randrange(3)):
                W[o].add(j)
        d = (kinds, pairs, links, W, Q)
        singleton_core_check(d, groups, totals)
    # A component-pair grouping can destroy both reachable direct payments.
    kinds, pairs, _ = canonical('AMAM')
    coarse = (kinds, pairs, [], {0: {0}, 1: {1}, 2: {1}, 3: {0}}, {0, 1})
    wrong = (*coarse[:3], {0: set(), 1: {1}, 2: set(), 3: {0}}, coarse[4])
    assert (fork_flow(*coarse)['value'], fork_flow(*wrong)['value']) == (2, 0)
    inspect(coarse, totals, rng, True)
    singleton_core_check(coarse, [{0, 1}, {2, 3}], totals)
    cost = (kinds, pairs, [(0, 2), (4, 6)], {0: {0}, 1: {1}, 2: {0}, 3: {2}}, {0, 1, 2})
    cost_control = singleton_core_check(cost, [{0, 1}, {2, 3}], totals)
    assert cost_control['orientation_value_cost'] == [2, 1]
    assert cost_control['local_value_cost'] == [[1, 0], [1, 0]]
    # Reusing a static selector AFTER a reservation is not valid.
    kinds, pairs, _ = canonical('AM')
    initial = (kinds, pairs, [], {0: {0, 1}, 1: {0, 1}}, {0, 1})
    sharp, _ = saturate(initial)
    assert (fork_flow(*restrict(initial, {1}))['value'], fork_flow(*restrict(sharp, {1}))['value']) == (1, 0)
    rebuilt, _ = saturate(restrict(initial, {1}))
    assert fork_flow(*rebuilt)['value'] == 1
    return dict(layered_fork_value_cost=[2, 4], wrong_component_grouping_value=[2, 0],
                wrong_static_reservation_value=[1, 0], singleton_cost_control=cost_control,
                scope='abstract, not asserted physical')


def physical_checks(totals):
    rng = random.Random(202610250626); records = []
    names = ['frozen_intrinsic_one_unit_gap', 'protected_shared_columns_fresh_obstruction',
             'whole_support_donor_collision', 'frozen_mixed_cycle_square_switch',
             'frozen_beta_support_fork', 'frozen_beta_fork_escape', 'frozen_all_mixed_gate_cycle']
    for name in names:
        j = json.loads((Path(__file__).parent/'fixtures'/f'{name}.json').read_text())
        cur = (*j['shape'], set(map(tuple, j['selected'])), [tuple(map(tuple, e)) for e in j['matching']])
        direct_check(*cur); P = {v for e in cur[3] for v in e}
        assert frozen_certificate(cur)[0] == P
        d, meta, _ = whole_support_data(cur, whole_bands(cur)); groups, _ = physical_groups(cur, d)
        inspect(d, totals, rng, exhaustive=len(d[2]) <= 10)
        row = singleton_core_check(d, groups, totals)
        # Original IDs after source-free pruning are retained; geometry is unchanged.
        row['core_geometry'] = [meta['intervals'][q] for q in row['singleton_core_units']]
        records.append(dict(fixture=name, **row))
        for trial in range(12):
            Q = {q for q in d[4] if rng.random() < .3}
            dd = restrict(d, Q)
            inspect(dd, totals, rng, exhaustive=False, sampled=3)
            singleton_core_check(dd, groups, totals)
        totals['frozen_fixture_images'] += 1
    cur = shared_gap(10); direct_check(*cur)
    d, _, _ = whole_support_data(cur, whole_bands(cur)); groups, _ = physical_groups(cur, d)
    records.append(dict(fixture='source-free-square shared gap', **singleton_core_check(d, groups, totals)))
    for n in list(range(2, 13))+[24, 48, 96]:
        cur = path_family(n); direct_check(*cur)
        assert frozen_certificate(cur)[0] == {v for e in cur[3] for v in e}
        d, meta, _ = whole_support_data(cur, whole_bands(cur)); groups, _ = physical_groups(cur, d)
        companion = {q for q in d[4] if meta['intervals'][q]['band'] == 1 and
                     meta['intervals'][q]['first'] in {6+4*i+t for i in range(n-1) for t in (0, 1)}}
        assert len(companion) == 2*(n-1)
        dd = restrict(d, companion)
        inspect(dd, totals, rng, exhaustive=True)
        row = singleton_core_check(dd, groups, totals)
        assert not row['singleton_core_units'] and row['global_value_cost'] == [n, 0]
        if n <= 8:
            one = {q for q in companion if (meta['intervals'][q]['first']-6) % 4 == 0}
            smaller = singleton_core_check(restrict(d, one), groups, totals)
            assert len(smaller['singleton_core_units']) == n-1 and smaller['global_value_cost'] == [n-1, 0]
        totals['frozen_companion_path_images'] += 1
        records.append(dict(fixture='frozen path with both original companion units', n=n, **row))
    return records


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', required=True, type=Path)
    args = p.parse_args(); totals = Counter()
    abstract = abstract_checks(totals); physical = physical_checks(totals)
    result = dict(status='PASS', totals=dict(totals), abstract_controls=abstract, physical=physical,
                  scope='Finite corroboration of written all-size fixed-C saturation and singleton-core proofs.',
                  limits=['available Q must be fixed before class construction',
                          'original whole-owner classes, not component-pair classes',
                          'keep original interval counts in physical ledger',
                          'no universal full-pool geometric compensation or 5/6 improvement'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), indent=2))


if __name__ == '__main__':
    main()
