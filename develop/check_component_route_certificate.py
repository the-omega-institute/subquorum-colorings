"""Lift component route certificates without spending a beta reserve twice.

The graph reduction is a sufficient certificate, not an exact replacement for
unrestricted route flow. Both the grouped-reserve obstruction and a strict
lower-bound example are checked explicitly.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import abstract, owner_data, solve
from check_frozen_first_destination_allocation import fixture, maximum_matching
from check_frozen_missing_port_bp_injection import inspect as missing_injection
from check_interval_connector_cycles_and_missing_ports import stack, whole_bands
from check_arbitrary_depth_cap_relays import relay_family
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import cancel_pairs, extended_ports, terminal_data

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


def decomposition(kinds, pairs, fixed):
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    assert len({p for link in fixed for p in link}) == 2*len(fixed)
    assert {p for a in alphas for p in pairs[a]} == {a for a, _ in fixed}
    assert all(kinds[a] == 'TP' and kinds[b] == 'BP' for a, b in fixed)
    assert all(owners[a] in alphas and owners[b] in betas | mixed for a, b in fixed)
    adjacency = defaultdict(set)
    targets = defaultdict(set)
    f_by_owner = {}
    for a, b in fixed:
        x, y = owners[a], owners[b]
        adjacency[x].add(y)
        adjacency[y].add(x)
        targets[x].add(y)
        f_by_owner[x, y] = a, b
    # An isolated original beta is also a surplus component with one unit.
    remaining, components = set(adjacency) | betas, []
    while remaining:
        start = min(remaining)
        reached, pending = {start}, [start]
        while pending:
            v = pending.pop()
            for other in adjacency[v]-reached:
                reached.add(other)
                pending.append(other)
        remaining -= reached
        aa, bb, mm = reached & alphas, reached & betas, reached & mixed
        assert len(mm) <= 2
        balance = len(bb)-len(aa)
        assert balance in (-1, 0, 1)
        assert (balance == -1) == (len(mm) == 2)
        category = {-1: 'demand', 0: 'balanced', 1: 'reserve'}[balance]
        components.append(dict(kind=category, alphas=aa, betas=bb, mixed=mm))
    owner_component = {owner: i for i, c in enumerate(components)
                       for owner in c['alphas'] | c['betas'] | c['mixed']}
    return owners, alphas, betas, mixed, components, owner_component, targets, f_by_owner


def certificate(kinds, pairs, links, access, resources, injection):
    (owners, alphas, betas, mixed, components, owner_component,
     targets, f_by_owner) = decomposition(kinds, pairs, injection)
    assert set(injection) <= set(links)
    demands = [i for i, c in enumerate(components) if c['kind'] == 'demand']
    reserves = [i for i, c in enumerate(components) if c['kind'] == 'reserve']
    t, s, k = len(demands), len(reserves), len(alphas)
    assert len(betas)+t == k+s
    assert len(resources)+len(betas)-k == len(resources)+s-t
    synthetic_pairs, synthetic_kinds = [], {}
    exit_tip, entry_tip = {}, {}
    source_components, reserve_components = {}, {}
    source_points, beta_points = {}, {}
    for component in demands:
        index = len(synthetic_pairs)
        pair = 2*index, 2*index+1
        synthetic_pairs.append(pair)
        synthetic_kinds.update({point: 'TP' for point in pair})
        source_components[index] = component
        source_points[component] = pair[0]
    for owner in sorted(mixed):
        index = len(synthetic_pairs)
        pair = 2*index, 2*index+1
        synthetic_pairs.append(pair)
        synthetic_kinds.update({pair[0]: 'BP', pair[1]: 'TP'})
        entry_tip[owner], exit_tip[owner] = pair
    for component in reserves:
        index = len(synthetic_pairs)
        pair = 2*index, 2*index+1
        synthetic_pairs.append(pair)
        synthetic_kinds.update({point: 'BP' for point in pair})
        reserve_components[index] = component
        beta_points[component] = pair[0]
    witnessed_links, witnessed_access = {}, {}
    synthetic_access = defaultdict(set)

    def start(point):
        owner = owners[point]
        if owner in mixed:
            return exit_tip[owner]
        if owner in alphas and owner_component[owner] in demands:
            return source_points[owner_component[owner]]
        return None

    def finish(point):
        owner = owners[point]
        if owner in mixed:
            return entry_tip[owner]
        if owner in betas and owner_component[owner] in reserves:
            return beta_points[owner_component[owner]]
        return None

    for a, b in links:
        assert kinds[a] == 'TP' and kinds[b] == 'BP'
        x, y = start(a), finish(b)
        if x is not None and y is not None and owners[a] != owners[b]:
            witnessed_links.setdefault((x, y), (a, b))
    for point, choices in access.items():
        x = start(point)
        if x is not None:
            for resource in choices:
                assert resource in resources
                synthetic_access[x].add(resource)
                witnessed_access.setdefault((x, resource), (point, resource))
    routed = solve(synthetic_kinds, synthetic_pairs, list(witnessed_links),
                   synthetic_access, resources)
    source_roots, beta_roots, exterior, payments = {}, {}, [], []
    for route in routed['routes']:
        source_id = route[0][1]
        component = source_components[source_id]
        first = next(tag for tag in route if tag[0] in ('link', 'access'))
        real_start = (witnessed_links[tuple(first[1:])][0] if first[0] == 'link' else
                      witnessed_access[tuple(first[1:])][0])
        source_roots[component] = owners[real_start]
        for tag in route:
            if tag[0] == 'link':
                actual = witnessed_links[tuple(tag[1:])]
                exterior.append(actual)
                if owners[actual[1]] in betas:
                    beta_roots[owner_component[owners[actual[1]]]] = owners[actual[1]]
            elif tag[0] == 'access':
                payments.append(witnessed_access[tuple(tag[1:])])
    assert len(source_roots) == routed['value']
    core = []
    component_records = []
    for i, component in enumerate(components):
        aa, bb = set(component['alphas']), set(component['betas'])
        if component['kind'] == 'demand':
            aa.remove(source_roots.get(i, min(aa)))
        if component['kind'] == 'reserve':
            bb.remove(beta_roots.get(i, min(bb)))
        incidence = {a: targets[a] & bb for a in aa}
        chosen = maximum_matching(incidence)
        assert len(chosen) == len(aa)
        core.extend(f_by_owner[a, b] for a, b in chosen.items())
        component_records.append(dict(index=i, kind=component['kind'],
                                      alphas=sorted(component['alphas']), betas=sorted(component['betas']),
                                      mixed=sorted(component['mixed'])))
    assert len(core) == k-t
    selected = core+exterior
    assert len({v for edge in selected for v in edge}) == 2*len(selected)
    assert set(selected) <= set(links)
    reduced, inventory, _ = cancel_pairs(kinds, pairs, selected, Counter())
    final_alphas = [pair for pair in reduced if all(kinds[v] == 'TP' for v in pair)]
    paid = set()
    for point, resource in payments:
        assert resource in access.get(point, set())
        owner = next(i for i, pair in enumerate(final_alphas) if point in pair)
        assert owner not in paid
        paid.add(owner)
    assert len({resource for _, resource in payments}) == len(payments)
    compensation = len(betas)-inventory['BP', 'BP']+len(payments)
    assert compensation == k-t+routed['value']
    assert len(selected) == k-t+routed['cost']
    assert len(final_alphas)-len(payments) == t-routed['value']
    full = solve(kinds, pairs, links, access, resources)
    assert compensation <= full['value']
    return dict(alpha=k, original_beta=len(betas), demand_components=t, reserve_components=s,
                quotient_value=routed['value'], quotient_cost=routed['cost'],
                compensation=compensation, remaining=t-routed['value'], links=selected,
                payments=payments, source_roots=sorted(source_roots.items()),
                beta_roots=sorted(beta_roots.items()), components=component_records,
                unrestricted_value=full['value'], unrestricted_cost=full['cost'])


def group_obstruction():
    kinds, pairs, _ = abstract(('alpha', 'alpha', 'alpha', 'beta', 'beta')+('mixed',)*4)
    injection = [(0, 10), (1, 12), (2, 14), (3, 16), (4, 6), (5, 8)]
    links = injection+[(0, 7), (2, 9)]
    result = certificate(kinds, pairs, links, {}, set(), injection)
    assert (result['demand_components'], result['reserve_components']) == (2, 1)
    assert (result['quotient_value'], result['compensation'], result['unrestricted_value']) == (1, 2, 2)
    # Treating each original beta as a spare would claim baseline1+2=3,
    # but there are only two beta units and no intervals.
    assert result['original_beta'] == 2 and result['remaining'] == 1
    return result


def balanced_exchange_obstruction():
    kinds, pairs, _ = abstract(('alpha', 'alpha', 'mixed', 'mixed', 'mixed', 'beta'))
    injection = [(0, 4), (1, 6), (2, 8), (3, 10)]
    links, access = injection+[(0, 11)], {2: {0}}
    result = certificate(kinds, pairs, links, access, {0}, injection)
    assert (result['quotient_value'], result['compensation'], result['unrestricted_value']) == (0, 1, 2)
    return result


def abstract_controls(totals):
    generator = random.Random(20261025)
    for _ in range(600):
        k = generator.randrange(1, 6)
        beta, mixed = generator.randrange(k+2), generator.randrange(2*k+3)
        if 2*beta+mixed < 2*k:
            mixed += 2*k-(2*beta+mixed)
        kinds, pairs, candidates = abstract(('alpha',)*k+('beta',)*beta+('mixed',)*mixed)
        targets = [p for p, kind in kinds.items() if kind == 'BP']
        generator.shuffle(targets)
        injection = list(zip(range(2*k), targets[:2*k]))
        links = sorted(set(injection) | {edge for edge in candidates if generator.random() < .08})
        resources = set(range(generator.randrange(4)))
        access = {p: {r for r in resources if generator.random() < .15}
                  for p, kind in kinds.items() if kind == 'TP'}
        result = certificate(kinds, pairs, links, access, resources, injection)
        totals['abstract_models'] += 1
        totals['strict_conservative_models'] += result['compensation'] < result['unrestricted_value']
        totals['lifted_routes'] += result['quotient_value']


def balanced_exchange_controls(totals):
    # The mixed--beta-ended path is m,a0,b0,...,a(n-1),b(n-1).
    # Removing ai and bj permits all other internal payments iff i <= j.
    for n in range(1, 21):
        for i, j in itertools.product(range(n), repeat=2):
            incidence = {a: ({a, a-1} & set(range(n)))-{j}
                         for a in range(n) if a != i}
            chosen = maximum_matching(incidence)
            assert (len(chosen) == n-1) == (i <= j)
            if i <= j:
                explicit = {a: a-1 if i < a <= j else a
                            for a in range(n) if a != i}
                assert len(set(explicit.values())) == n-1
                assert set(explicit.values()) == set(range(n))-{j}
                assert all(b in incidence[a] for a, b in explicit.items())
            totals['balanced_root_pairs'] += 1
            cyclic = {a: {a, (a-1) % n}-{j} for a in range(n) if a != i}
            assert len(maximum_matching(cyclic)) == n-1
            totals['balanced_cycle_root_pairs'] += 1

    # Chains of compatible exchanges: each intermediate balanced component
    # sacrifices one old core payment and supplies two exterior paid pieces.
    # This validates the h correction in the link and compensation formulas.
    for h in range(1, 13):
        sizes = [1+(index*3+h) % 7 for index in range(h)]
        k = 1+sum(sizes)
        kinds, pairs, _ = abstract(('alpha',)*k+('beta',)*(k-1)+('mixed',)*(h+2))
        mixed_start = 2*k-1
        fixed = [(pairs[0][0], pairs[mixed_start][0]),
                 (pairs[0][1], pairs[mixed_start+1][0])]
        alpha_start, beta_start = 1, k
        roots, beta_roots, exterior = {0}, set(), []
        outgoing = pairs[0][0]
        for component, n in enumerate(sizes):
            for a in range(n):
                first_target = (pairs[mixed_start+2+component][0] if a == 0 else
                                pairs[beta_start+a-1][1])
                fixed.extend([(pairs[alpha_start+a][0], first_target),
                              (pairs[alpha_start+a][1], pairs[beta_start+a][0])])
            i = (component+h) % n
            j = i+(component % (n-i))
            roots.add(alpha_start+i)
            beta_roots.add(beta_start+j)
            exterior.append((outgoing, pairs[beta_start+j][0]))
            outgoing = pairs[alpha_start+i][0]
            alpha_start += n
            beta_start += n
        data = decomposition(kinds, pairs, fixed)
        targets, witnesses = data[-2:]
        available_beta = set(range(k, 2*k-1))-beta_roots
        incidence = {a: targets[a] & available_beta for a in range(k) if a not in roots}
        matching = maximum_matching(incidence)
        assert len(matching) == k-1-h
        core = [witnesses[a, b] for a, b in matching.items()]
        selected = core+exterior
        assert len(selected) == k-1
        assert len({p for edge in selected for p in edge}) == 2*len(selected)
        reduced, inventory, _ = cancel_pairs(kinds, pairs, selected, Counter())
        final_alpha = [pair for pair in reduced if all(kinds[p] == 'TP' for p in pair)]
        assert len(final_alpha) == 1 and outgoing in final_alpha[0]
        # One distinct original interval pays the final exterior piece.
        assert (k-1)-inventory['BP', 'BP']+1 == k
        all_links = sorted(set(fixed+exterior))
        full = solve(kinds, pairs, all_links, {outgoing: {0}}, {0})
        assert full['value'] == k
        totals['balanced_exchange_chains'] += 1


def physical_data(current, bands):
    direct_check(*current)
    assert frozen_certificate(current)[0] == {v for e in current[3] for v in e}
    original, labels, intervals, owner, kinds, pairs, ports = terminal_data(current, bands)
    owners, alphas, _, _ = owner_data(kinds, pairs)
    assert all(not ports[p] for a in alphas for p in pairs[a])
    injection = missing_injection(current, bands, Counter(), True)['assignment']
    assert len(injection) == 2*len(alphas)
    extended = extended_ports(current, bands, labels, intervals, owner, kinds, ports, Counter())
    marked = {owner[b, 0] for b in range(len(bands))}
    marked |= {owner[b, len(band)-1] for b, band in enumerate(bands)
               if len(band) % 2 == 0 and labels[b][-1] == ('B', 'B')}
    resources = set(range(len(intervals)))-marked
    access = {p: {owner[port] for port in extended[p]} & resources
              for p in kinds if kinds[p] == 'TP'}
    links = [(a, b) for a in kinds for b in kinds if kinds[a] == 'TP' and kinds[b] == 'BP'
             and a[0] == b[0] and abs(a[1]-b[1]) == 1]
    return kinds, pairs, links, access, resources, injection


def physical_controls(totals):
    examples = []
    current, _ = fixture()
    data = physical_data(current, whole_bands(current))
    kinds, pairs, links, access, resources, _ = data
    _, alphas, _, _ = owner_data(kinds, pairs)
    tips = [v for a in sorted(alphas) for v in pairs[a]]
    choices = [[b for a, b in links if a == v] for v in tips]
    for targets in itertools.product(*choices):
        if len(set(targets)) != len(targets):
            continue
        result = certificate(kinds, pairs, links, access, resources, list(zip(tips, targets)))
        assert result['compensation'] == 2
        totals['unported_fixture_injections'] += 1
        if result['demand_components'] and not examples:
            examples.append(dict(family='unported_gate', result=result))
    for amount in range(1, 6):
        current = stack(6, 4, ['missing']*amount)
        result = certificate(*physical_data(current, whole_bands(current)))
        assert result['compensation'] == result['alpha'] == amount
        assert result['demand_components'] == amount
        totals['separated_missing_stacks'] += 1
        if amount == 3:
            examples.append(dict(family='three_missing_components', result=result))
    for width, upper, lower in itertools.product((8, 12), (1, 2, 4), (1, 3, 6)):
        current, bands, _ = relay_family(width, 4, upper, lower)
        result = certificate(*physical_data(current, bands))
        assert result['compensation'] == 1
        # The short right exits hit marked boundary intervals. They do not
        # pay the one-sided budget; only the two unmarked left exits count.
        assert result['quotient_cost'] == min(upper, lower)
        assert result['quotient_cost'] == result['unrestricted_cost']
        totals['depth_relay_families'] += 1
    return examples


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals = Counter()
    grouped, exchange = group_obstruction(), balanced_exchange_obstruction()
    abstract_controls(totals)
    balanced_exchange_controls(totals)
    examples = physical_controls(totals)
    report = dict(status='PASS', totals=dict(totals), grouped_reserve_obstruction=grouped,
                  conservative_limit=exchange, physical_examples=examples,
                  scope='Written component route lifting with one reserve per beta-surplus path. '
                  'All certificates reconstruct original terminal matchings and interval payments. '
                  'Quotient flow is a sufficient lower bound, not unrestricted equality. '
                  'Compatible balanced transfers have separate root-pair and chain controls; '
                  'no ordinary-flow reduction for that enlarged class is claimed. '
                  'Abstract obstructions are not physical frozen-grid counterexamples. '
                  'No universal grid or 5/6 improvement follows from finite controls.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals))))


if __name__ == '__main__':
    main()
