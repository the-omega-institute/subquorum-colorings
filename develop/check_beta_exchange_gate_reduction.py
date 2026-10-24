"""Exact residual compensation after original alpha--beta prepayments.

Every used core pair becomes one exchange gate with both original beta
entry tips and both original alpha exit tips. This is a reversible payment,
not contraction of an immutable terminal link.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import abstract, exhaustive, owner_data, solve
from check_frozen_first_destination_allocation import maximum_matching, fixture as unported_fixture
from check_frozen_shared_mixed_gate import fixture as shared_fixture
from check_terminal_cancellation_and_stranded_demand import cancel_pairs, extended_ports, terminal_data
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Verification requires assertions; do not use -O.')


def compile_and_lift(kinds, pairs, links, access, resources, core):
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    assert set(core) <= set(links)
    assert all(owners[a] in alphas and owners[b] in betas for a, b in core)
    assert len({owners[a] for a, _ in core}) == len(core)
    assert len({owners[b] for _, b in core}) == len(core)
    m = len(core)
    paid_alpha = {owners[a] for a, _ in core}
    paid_beta = {owners[b] for _, b in core}
    free_alpha, spare_beta = alphas-paid_alpha, betas-paid_beta
    types, starts, ends, gate_core = [], {}, {}, {}
    source_owner, mixed_owner, beta_owner = {}, {}, {}

    def add(kind):
        index = len(types)
        types.append(kind)
        return index, 2*index, 2*index+1

    for a in sorted(free_alpha):
        index, first, _ = add('alpha')
        starts[a] = first
        source_owner[index] = a
    for owner in sorted(mixed):
        index, first, second = add('mixed')
        ends[owner], starts[owner] = first, second
        mixed_owner[index] = owner
    for index, (a, b) in enumerate(core):
        gate, first, second = add('mixed')
        ends[owners[b]], starts[owners[a]] = first, second
        gate_core[gate] = index
    for b in sorted(spare_beta):
        index, first, _ = add('beta')
        ends[b] = first
        beta_owner[index] = b
    synthetic_kinds, synthetic_pairs, _ = abstract(types)
    witnesses, access_witnesses = {}, {}
    synthetic_access = defaultdict(set)
    for a, b in links:
        assert kinds[a] == 'TP' and kinds[b] == 'BP'
        if owners[a] == owners[b]:
            continue
        first, second = starts[owners[a]], ends[owners[b]]
        if first//2 != second//2:
            witnesses.setdefault((first, second), (a, b))
    for point, choices in access.items():
        assert kinds[point] == 'TP' or not choices
        if kinds[point] != 'TP':
            continue
        tail = starts[owners[point]]
        for resource in choices:
            assert resource in resources
            synthetic_access[tail].add(resource)
            access_witnesses.setdefault((tail, resource), (point, resource))
    routed = solve(synthetic_kinds, synthetic_pairs, list(witnesses), synthetic_access, resources)
    used_core = {gate_core[tag[1]] for route in routed['routes'] for tag in route
                 if tag[0] == 'mixed' and tag[1] in gate_core}
    exterior = [witnesses[tuple(tag[1:])] for route in routed['routes'] for tag in route
                if tag[0] == 'link']
    payments = [access_witnesses[tuple(tag[1:])] for route in routed['routes'] for tag in route
                if tag[0] == 'access']
    retained = [edge for index, edge in enumerate(core) if index not in used_core]
    selected = retained+exterior
    assert len({p for edge in selected for p in edge}) == 2*len(selected)
    assert set(selected) <= set(links)
    reduced, inventory, records = cancel_pairs(kinds, pairs, selected, Counter())
    final_alpha = [pair for pair in reduced if all(kinds[p] == 'TP' for p in pair)]
    assigned = set()
    for point, resource in payments:
        assert resource in access[point]
        final = next(index for index, pair in enumerate(final_alpha) if point in pair)
        assert final not in assigned
        assigned.add(final)
    assert len({resource for _, resource in payments}) == len(payments)
    # Independently recover actual original paid-source/resource supports.
    actual_paid, actual_beta = set(), set()
    payment_tips = {point for point, _ in payments}
    for record in records:
        original_owners = {owners[p] for p in record['vertices']}
        aa, bb = original_owners & alphas, original_owners & betas
        assert len(aa) <= 1 and len(bb) <= 1
        if bb and aa:
            actual_paid |= aa
            actual_beta |= bb
        elif aa and payment_tips & set(record['ends']):
            actual_paid |= aa
    assert paid_alpha <= actual_paid and paid_beta <= actual_beta
    value = len(betas)-inventory['BP', 'BP']+len(payments)
    assert value == m+routed['value'] == len(actual_paid)
    assert len(final_alpha)-len(payments) == len(alphas)-value
    assert len(selected) == m-len(used_core)+routed['cost']
    full = solve(kinds, pairs, links, access, resources)
    assert value == full['value']
    cut_original = []
    for category, index in routed['cut']:
        if category == 'mixed' and index in gate_core:
            cut_original.append(('exchange', gate_core[index], core[gate_core[index]]))
        elif category == 'mixed':
            cut_original.append(('mixed', mixed_owner[index], pairs[mixed_owner[index]]))
        elif category == 'beta':
            cut_original.append(('beta', beta_owner[index], pairs[beta_owner[index]]))
        else:
            assert category == 'interval'
            cut_original.append(('interval', index))
    blocked_original = sorted(source_owner[index] for index in routed['blocked'])
    assert len(blocked_original)-len(cut_original) == len(alphas)-value
    return dict(core_size=m, residual_value=routed['value'], full_value=value,
                deficit=len(alphas)-value, used_exchange_gates=len(used_core),
                exterior_links=routed['cost'], lifted_links=len(selected),
                unrestricted_minimum_links=full['cost'], core=core,
                retained_core=retained, selected_links=selected, payments=payments,
                paid_sources=sorted(actual_paid), used_betas=sorted(actual_beta),
                residual_cut=routed['cut'], residual_blocked=routed['blocked'],
                source_root_owners=sorted(free_alpha),
                residual_cut_original=cut_original, residual_blocked_original=blocked_original)


def protected_value(kinds, pairs, links, access, resources, core):
    owners, _, _, _ = owner_data(kinds, pairs)
    removed = {owners[p] for edge in core for p in edge}
    remaining = [pair for index, pair in enumerate(pairs) if index not in removed]
    labels = {p: kinds[p] for pair in remaining for p in pair}
    edges = [(a, b) for a, b in links if a in labels and b in labels]
    ports = {p: access.get(p, set()) for p in labels if labels[p] == 'TP'}
    return len(core)+solve(labels, remaining, edges, ports, resources)['value']


def port_recovery_obstruction():
    kinds, pairs, _ = abstract(('alpha', 'alpha', 'beta'))
    core, links, access = [(2, 4)], [(2, 4), (0, 4)], {2: {0}}
    result = compile_and_lift(kinds, pairs, links, access, {0}, core)
    assert result['full_value'] == 2 and result['used_exchange_gates'] == 1
    assert result['selected_links'] == [(0, 4)] and result['payments'] == [(2, 0)]
    result['protected_core_value'] = protected_value(kinds, pairs, links, access, {0}, core)
    assert result['protected_core_value'] == 1
    # Literal contraction keeps only unused tips 3 and 5 on the virtual mixed.
    # Neither the needed incoming BP4 nor outgoing TP2 survives that operation.
    return result


def cost_limit():
    kinds, pairs, _ = abstract(('alpha', 'beta'))
    result = compile_and_lift(kinds, pairs, [(0, 2)], {1: {0}}, {0}, [(0, 2)])
    assert result['full_value'] == 1
    assert result['lifted_links'] == 1 and result['unrestricted_minimum_links'] == 0
    return result


def exhaustive_controls(totals):
    kinds, pairs, candidates = abstract(('alpha', 'alpha', 'beta'))
    for mask in range(1 << len(candidates)):
        links = [edge for index, edge in enumerate(candidates) if mask >> index & 1]
        for ports in range(16):
            access = {p: {0} for p in range(4) if ports >> p & 1}
            for core in [[]]+[[edge] for edge in links]:
                result = compile_and_lift(kinds, pairs, links, access, {0}, core)
                totals['exhaustive_core_controls'] += 1
                totals['exchange_gate_uses'] += result['used_exchange_gates']
            if ports in (0, 15) and mask % 17 == 0:
                counted = Counter()
                full = solve(kinds, pairs, links, access, {0})
                assert (full['value'], full['cost']) == exhaustive(kinds, pairs, links, access, counted)
                totals['independent_original_terminal_matchings'] += counted['independent_terminal_matchings']
                totals['independently_enumerated_models'] += 1
            totals['exhaustive_original_models'] += 1


def random_controls(totals):
    generator = random.Random(2026102502)
    for _ in range(800):
        k, b, mixed = generator.randrange(1, 7), generator.randrange(7), generator.randrange(6)
        kinds, pairs, candidates = abstract(('alpha',)*k+('beta',)*b+('mixed',)*mixed)
        links = [edge for edge in candidates if generator.random() < .15]
        resources = set(range(generator.randrange(5)))
        access = {p: {r for r in resources if generator.random() < .2}
                  for p in kinds if kinds[p] == 'TP'}
        owners, alphas, betas, _ = owner_data(kinds, pairs)
        eligible = [(a, z) for a, z in links if owners[a] in alphas and owners[z] in betas]
        generator.shuffle(eligible)
        used_a, used_b, core = set(), set(), []
        for a, z in eligible:
            if owners[a] not in used_a and owners[z] not in used_b and generator.random() < .6:
                core.append((a, z))
                used_a.add(owners[a]); used_b.add(owners[z])
        result = compile_and_lift(kinds, pairs, links, access, resources, core)
        totals['random_core_controls'] += 1
        totals['exchange_gate_uses'] += result['used_exchange_gates']
        totals['strict_protected_gaps'] += protected_value(kinds, pairs, links, access, resources, core) < result['full_value']


def multiport_instance(n, removed_alpha, removed_beta):
    h = len(removed_alpha)
    kinds, pairs, _ = abstract(('alpha',)*(n+h)+('beta',)*n)
    core = [(pairs[h+i][0], pairs[h+n+i][0]) for i in range(n)]
    backward = [(pairs[h+i][1], pairs[h+n+i-1][1]) for i in range(1, n)]
    incoming = [(pairs[index][0], pairs[h+n+j][0]) for index, j in enumerate(removed_beta)]
    access = {pairs[h+i][0]: {index} for index, i in enumerate(removed_alpha)}
    result = compile_and_lift(kinds, pairs, core+backward+incoming, access, set(range(h)), core)
    return result


def multiport_controls(totals):
    for n in range(10):
        universe = set(range(n))
        for h in range(n+1):
            for aa, bb in itertools.product(itertools.combinations(range(n), h), repeat=2):
                condition = all(i <= j for i, j in zip(aa, bb))
                condition &= all(bb[index] < aa[index+1] for index in range(h-1))
                incidence = {a: ({a, a-1} & universe)-set(bb) for a in universe-set(aa)}
                assert (len(maximum_matching(incidence)) == n-h) == condition
                if condition:
                    explicit = {a: a-1 if any(i < a <= j for i, j in zip(aa, bb)) else a
                                for a in universe-set(aa)}
                    assert set(explicit.values()) == universe-set(bb)
                    assert len(explicit.values()) == len(set(explicit.values()))
                    assert all(b in incidence[a] for a, b in explicit.items())
                    used = [set(range(i, j+1)) for i, j in zip(aa, bb)]
                    if used:
                        assert sum(map(len, used)) == len(set().union(*used))
                totals['multiport_root_sets'] += 1
                if 1 <= n <= 5 and h:
                    routed = multiport_instance(n, aa, bb)
                    assert (routed['full_value'] == n+h) == condition
                    totals['multiport_route_controls'] += 1
    result = multiport_instance(6, (0, 3), (1, 4))
    assert result['residual_value'] == 2 and result['used_exchange_gates'] == 4
    assert result['full_value'] == 8 and result['lifted_links'] == 6
    return result


def physical_data(current, bands=None):
    direct_check(*current)
    assert frozen_certificate(current)[0] == {p for edge in current[3] for p in edge}
    bands = whole_bands(current) if bands is None else bands
    original, labels, intervals, interval_owner, kinds, pairs, ports = terminal_data(current, bands)
    extended = extended_ports(current, bands, labels, intervals, interval_owner, kinds, ports, Counter())
    marked = {interval_owner[i, 0] for i in range(len(bands))}
    marked |= {interval_owner[i, len(band)-1] for i, band in enumerate(bands)
               if len(band) % 2 == 0 and labels[i][-1] == ('B', 'B')}
    resources = set(range(len(intervals)))-marked
    access = {p: {interval_owner[q] for q in extended[p]} & resources for p in kinds if kinds[p] == 'TP'}
    links = [(a, b) for a in kinds for b in kinds if kinds[a] == 'TP' and kinds[b] == 'BP'
             and a[0] == b[0] and abs(a[1]-b[1]) == 1]
    return kinds, pairs, links, access, resources


def physical_controls(totals):
    from check_compensation_flow_geometry_frontier import pad_image
    from check_elbow_sources import elbow
    from check_exchange_terminal_nonunique import fixture, graft, matching_orders
    from check_interval_connector_cycles_and_missing_ports import stack
    from check_promotion_cores import tight_diamond
    from degree_three_fusion import occupied_bands
    from rotor_networks import chain, combine, rotor, star_modules, transform_module
    base = fixture()
    fixtures = [('bent_'+str(i), (*base[:3], list(x['matching']))) for i, x in enumerate(matching_orders())]
    fixtures += [('graft', graft(6, 4)), ('elbow', elbow(6, 4)), ('diamond', tight_diamond()[0]),
                 ('occupied', occupied_bands(6)[0]), ('unported', unported_fixture()[0]),
                 ('shared', shared_fixture())]
    fixtures += [(kind, stack(6, 4, [kind])) for kind in ('missing', 'collision', 'cycle')]
    module = rotor()
    fixtures.append(('capacity_two_rotor', (6, 6, module['selected'], module['matching'])))
    for width in (6, 10, 20):
        modules = [transform_module(module, (False, False, False), (width-2, width-2))
                   for module in star_modules(width)]
        network = combine(modules)
        fixtures.append(('branched_star_'+str(width), (2*width+2, 2*width+2, network['selected'], network['matching'])))
    records = []
    for (name, model), symmetry, offset in itertools.product(fixtures,
            itertools.product((False, True), repeat=3), itertools.product((2, 3), repeat=2)):
        current = pad_image(model, symmetry, offset)
        kinds, pairs, links, access, resources = physical_data(current)
        owners, aa, bb, _ = owner_data(kinds, pairs)
        incidence = {a: {owners[z] for p, z in links if owners[p] == a and owners[z] in bb} for a in aa}
        matching = maximum_matching(incidence)
        largest = [next((p, z) for p, z in links if owners[p] == a and owners[z] == b)
                   for a, b in sorted(matching.items())]
        # All subsets of this owner-disjoint core test arbitrary partial payments.
        for mask in range(1 << len(largest)):
            core = [edge for i, edge in enumerate(largest) if mask >> i & 1]
            result = compile_and_lift(kinds, pairs, links, access, resources, core)
            totals['physical_core_controls'] += 1
            totals['physical_exchange_gate_uses'] += result['used_exchange_gates']
        totals['physical_geometries'] += 1
        if largest and not symmetry[0] and not symmetry[1] and not symmetry[2] and offset == (2, 2):
            records.append(dict(family=name, alpha=len(aa), beta=len(bb), core=len(largest),
                                full_value=result['full_value']))
    return records


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals = Counter()
    recovery, costs = port_recovery_obstruction(), cost_limit()
    exhaustive_controls(totals)
    random_controls(totals)
    multiport = multiport_controls(totals)
    physical = physical_controls(totals)
    report = dict(status='PASS', totals=dict(totals), port_recovery_obstruction=recovery,
                  cardinality_not_cost=costs, multiport_balanced_example=multiport,
                  physical_families=physical,
                  scope='Written exact cardinality reduction for any owner-disjoint original alpha-beta core. '
                  'Every compiled route packing is lifted and its original paid-source and beta supports checked. '
                  'Independent finite terminal enumeration is a bounded cross-check, not a general proof. '
                  'No geometric coverage or universal 5/6 improvement is claimed.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals))))


if __name__ == '__main__':
    main()
