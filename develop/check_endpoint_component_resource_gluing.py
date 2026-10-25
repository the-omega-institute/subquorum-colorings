"""Exact original-P-component gluing and unbounded-order withdrawal witnesses.

No external solver dependency. General proofs are in
docs/ENDPOINT_COMPONENT_RESOURCE_GLUING.md; enumeration only validates them.
"""
import argparse
from collections import Counter
import itertools as it
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import canonical, whole_support_data, brute
from check_whole_support_fork_flow import fork_flow
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_owned_donors import endpoint_data
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_single_square_routing import shared_gap

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def restrict(d, Q):
    return (*d[:3], {o: W & Q for o, W in d[3].items()}, set(Q))


def local(d, group, Q):
    keep = sorted(group)
    tips = {v for o in keep for v in d[1][o]}
    return ({v: d[0][v] for v in tips}, [d[1][o] for o in keep],
            [e for e in d[2] if set(e) <= tips],
            {i: d[3][o] & Q for i, o in enumerate(keep)}, set(Q))


def physical_groups(cur, d):
    P, adj, _ = endpoint_data(cur)
    component = {}
    for v in sorted(P):
        if v in component:
            continue
        tag = len(set(component.values())); todo = [v]; component[v] = tag
        while todo:
            u = todo.pop()
            for w in adj[u]:
                if w not in component:
                    component[w] = tag; todo.append(w)
    groups = {}
    tip_owner, A, _, _ = owner_data(*d[:2])
    owner_component = {}
    for o, pair in enumerate(d[1]):
        assert len({component[v] for v in pair}) == 1
        tag = component[pair[0]]; owner_component[o] = tag
        groups.setdefault(tag, set()).add(o)
    assert all(owner_component[tip_owner[u]] == owner_component[tip_owner[v]]
               for u, v in d[2])
    return list(groups.values()), A


def lattice_checks(d, groups, Q, totals, independent=False):
    """All availability sets and all pairs, on one small ORIGINAL subpool."""
    assert set().union(set(), *groups) == set(range(len(d[1])))
    assert sum(map(len, groups)) == len(d[1])
    owner, A, _, _ = owner_data(*d[:2])
    group_id = {o: i for i, g in enumerate(groups) for o in g}
    assert all(group_id[owner[u]] == group_id[owner[v]] for u, v in d[2])
    active = [g for g in groups if g & A]
    units = sorted(Q); size = 1 << len(units); full = size-1
    sets = [{j for t, j in enumerate(units) if m >> t & 1} for m in range(size)]
    ranks = [[fork_flow(*local(d, g, R))['value'] for R in sets] for g in active]
    for values in ranks:
        for m in range(size):
            for bit in range(len(units)):
                if not (m >> bit & 1):
                    assert 0 <= values[m | (1 << bit)]-values[m] <= 1
                    totals['unit_increment_checks'] += 1
            for z in range(size):
                assert values[m]+values[z] >= values[m | z]+values[m & z]
                totals['rank_submodularity_pairs'] += 1
    shared_mask = sum(1 << t for t, j in enumerate(units)
                      if sum(any(j in d[3][o] for o in g) for g in active) >= 2)
    for m, available in enumerate(sets):
        result = fork_flow(*restrict(d, available))
        candidates = {r: (m ^ r).bit_count()+sum(v[r] for v in ranks)
                      for r in range(size) if r & m == r}
        optimum = min(candidates.values())
        assert result['value'] == optimum
        minimizers = [r for r, value in candidates.items() if value == optimum]
        required = m & ~shared_mask
        assert any(r & required == required for r in minimizers)
        for r in minimizers:
            for s in minimizers:
                assert candidates[r | s] == candidates[r & s] == optimum
                totals['minimizer_lattice_pairs'] += 1
        base = len(A)-sum(v[m] for v in ranks)
        extra = max(sum(v[m]-v[r] for v in ranks)-(m ^ r).bit_count()
                    for r in candidates)
        shared_extra = max(sum(v[m]-v[r] for v in ranks)-(m ^ r).bit_count()
                           for r in candidates if (m ^ r) & ~shared_mask == 0)
        assert len(A)-result['value'] == base+extra and extra == shared_extra
        totals['exact_gluing_availability_sets'] += 1
        totals['positive_joint_overlap_cases'] += extra > 0
        if independent and len(d[2]) <= 10:
            answer, count = brute(*restrict(d, available))
            assert answer == (result['value'], result['cost'])
            totals['independent_terminal_matchings'] += count
    totals['lattice_models'] += 1
    totals['models_with_multiple_active_P_components_or_abstract_groups'] += len(active) >= 2
    return dict(active_components=len(active), original_subpool=units,
                full_value=fork_flow(*restrict(d, Q))['value'], local_values=[v[full] for v in ranks])


def abstract_controls(totals):
    rng = random.Random(202610250521)
    patterns = [('AAMB', 'AMB'), ('AAMMB', 'AAB'), ('AMMB', 'ABB'),
                ('AM', 'AM'), ('BMM', 'AABM'), ('A', 'A', 'A')]
    for index in range(120):
        blocks = patterns[index % len(patterns)]
        types = ''.join(blocks); kinds, pairs, possible = canonical(types)
        groups = []; start = 0
        for b in blocks:
            groups.append(set(range(start, start+len(b)))); start += len(b)
        tag = {o: i for i, g in enumerate(groups) for o in g}
        links = [e for e in possible if tag[e[0]//2] == tag[e[1]//2] and rng.random() < .35]
        I = set(range(1+index % 5))
        W = {o: {j for j in I if rng.random() < .4} for o in range(len(pairs))}
        d = (kinds, pairs, links, W, I)
        lattice_checks(d, groups, I, totals, independent=index < 18)
    # Forced deep mixed path, both separate entries of a beta, and a fork.
    kinds, pairs, _ = canonical('AAMMBAM')
    d = (kinds, pairs, [(0, 4), (5, 6), (7, 8), (2, 9), (10, 12)],
         {o: ({0, 1} if o == 4 else {0} if o == 6 else set()) for o in range(7)}, {0, 1})
    lattice_checks(d, [{0, 1, 2, 3, 4}, {5, 6}], {0, 1}, totals, True)
    f = fork_flow(*d)
    assert f['value'] == 3 and any(p['kind'] == 'fork' for p in f['certificates'])
    assert max(len(p['links']) for p in f['certificates']) >= 4
    kinds, pairs, _ = canonical('AMAM')
    cost = (kinds, pairs, [(0, 2), (4, 6)], {0: {0}, 1: {1}, 2: {0}, 3: {2}}, {0, 1, 2})
    locals_ = [fork_flow(*local(cost, g, cost[4])) for g in [{0, 1}, {2, 3}]]
    global_ = fork_flow(*cost)
    answer, count = brute(*cost); totals['independent_terminal_matchings'] += count
    assert answer == (global_['value'], global_['cost']) == (2, 1)
    assert [(v['value'], v['cost']) for v in locals_] == [(1, 0), (1, 0)]
    lattice_checks(cost, [{0, 1}, {2, 3}], cost[4], totals, True)
    return dict(scope='abstract, not asserted physical',
                forced_layered_beta_fork=dict(value=f['value'], cost=f['cost'], certificates=f['certificates']),
                cost_countercontrol=dict(local_value_cost=[[1, 0], [1, 0]], global_value_cost=[2, 1]))


def path_family(n):
    cs = [4+4*i for i in range(n)]
    T = {(r, c) for c in cs for r in (2, 5)}
    T |= {(3, c+1) for c in cs}; T |= {(4, c-1) for c in cs}
    return (8, 4*n+6, T, [((3, c), (4, c)) for c in cs])


def path_checks(totals):
    records = []
    for n in list(range(2, 11))+[16, 32, 64]:
        cur = path_family(n); direct_check(*cur)
        P, adj, sq = endpoint_data(cur)
        assert frozen_certificate(cur)[0] == P and not sq and all(len(adj[v]) == 1 for v in P)
        d, meta, _ = whole_support_data(cur, whole_bands(cur)); groups, A = physical_groups(cur, d)
        assert len(A) == len(groups) == n and not d[2]
        units = []
        for i in range(n-1):
            ids = [j for j in d[4] if meta['intervals'][j] ==
                   dict(band=1, first=6+4*i, last=6+4*i)]
            assert len(ids) == 1; units += ids
            owners = {o for o, W in d[3].items() if ids[0] in W}
            assert {d[1][o][0][1] for o in owners} == {4+4*i, 8+4*i}
        Q = set(units)
        f = fork_flow(*restrict(d, Q)); whole = fork_flow(*d)
        assert (f['value'], f['cost']) == (n-1, 0)
        assert (whole['value'], whole['cost']) == (n, 0)
        assert all(fork_flow(*local(d, g, Q))['value'] == 1 for g in groups)
        zero = {j for j in d[4] if all(j not in W for W in d[3].values())}
        assert len(zero) >= n
        assert fork_flow(*restrict(d, Q | zero))['value'] == n-1
        # Explicit distinct full-pool payment described in the written proof.
        for o in A:
            c = d[1][o][0][1]
            assert any(meta['intervals'][j] == dict(band=2, first=c+1, last=c+1) for j in d[3][o])
        withdrawals = (range(1 << (n-1)) if n <= 10 else
                       [0, (1 << (n-1))-1]+[((1 << (n-1))-1) ^ (1 << r) for r in range(n-1)])
        incidence = [{i for i, j in enumerate(units) if j in d[3][o]} for o in
                     sorted(A, key=lambda o: d[1][o][0][1])]
        for mask in withdrawals:
            J = {i for i in range(n-1) if mask >> i & 1}
            losing = {v for v, incident in enumerate(incidence) if incident <= J}
            if len(J) == n-1:
                assert len(losing)-len(J) == 1
            else:
                r = next(i for i in range(n-1) if i not in J)
                assert r not in losing and r+1 not in losing
                images = [v if v < r else v-1 for v in losing]
                assert len(set(images)) == len(losing) and set(images) <= J
                assert len(losing) <= len(J)
            totals['path_withdrawal_subsets'] += 1
        if n <= 5:
            lattice_checks(d, groups, Q, totals, True)
        totals['frozen_path_images'] += 1
        records.append(dict(n=n, shape=cur[:2], restricted_value=n-1,
                            local_sum=n, full_pool_value=n, zero_owner_units=len(zero),
                            designated_units=[meta['intervals'][j] for j in units],
                            withdrawals='all' if n <= 10 else 'empty/full/all-one-edge-retained'))
    return records


def frozen_fixture_checks(totals):
    names = ['frozen_intrinsic_one_unit_gap', 'protected_shared_columns_fresh_obstruction',
             'whole_support_donor_collision', 'frozen_mixed_cycle_square_switch']
    rng = random.Random(202610250522); records = []
    for name in names:
        j = json.loads((Path(__file__).parent/'fixtures'/f'{name}.json').read_text())
        cur = (*j['shape'], set(map(tuple, j['selected'])), [tuple(map(tuple, e)) for e in j['matching']])
        direct_check(*cur); P, _, _ = endpoint_data(cur)
        assert frozen_certificate(cur)[0] == P
        d, _, _ = whole_support_data(cur, whole_bands(cur)); groups, A = physical_groups(cur, d)
        for trial in range(3):
            shared = [q for q in sorted(d[4]) if sum(any(q in d[3][o] for o in g)
                                                     for g in groups if g & A) >= 2]
            other = sorted(d[4]-set(shared)); rng.shuffle(shared); rng.shuffle(other)
            Q = set((shared+other)[:5])
            row = lattice_checks(d, groups, Q, totals, independent=len(d[2]) <= 8)
            records.append(dict(fixture=name, trial=trial, **row))
        totals['frozen_fixture_images'] += 1
    cur = shared_gap(10); direct_check(*cur)
    assert frozen_certificate(cur)[0] == endpoint_data(cur)[0]
    d, _, _ = whole_support_data(cur, whole_bands(cur)); groups, A = physical_groups(cur, d)
    shared = {j for j in d[4] if sum(any(j in d[3][o] for o in g) for g in groups) >= 2}
    Q = {min(shared)}
    result = lattice_checks(d, groups, Q, totals, True)
    assert result['active_components'] == result['full_value'] == 1
    records.append(dict(fixture='source-free-square shared unit is effectively private', **result))
    return records


def main():
    p = argparse.ArgumentParser(); p.add_argument('--output', type=Path, required=True)
    args = p.parse_args(); totals = Counter()
    abstract = abstract_controls(totals)
    physical = frozen_fixture_checks(totals)
    paths = path_checks(totals)
    result = dict(status='PASS', scope='finite checks only; arbitrary-size claims have written proofs',
                  totals=dict(totals), abstract_controls=abstract, frozen_controls=physical, path_family=paths,
                  limitations=['restricted original pools are not full-board counterexamples',
                               'value gluing does not give a local minimum-cost gluing rule',
                               'universal geometric compensation and 5/6 improvement remain open'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals)), indent=2))


if __name__ == '__main__':
    main()
