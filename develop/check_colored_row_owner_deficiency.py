"""Exact colored row/owner Hall ledgers and monochromatic beta allocations.

Written proofs: docs/COLORED_ROW_OWNER_DEFICIENCY_AND_RESOURCE_CUTS.md.
Physical controls require actual feasibility and complete freezing. Random
row profiles check only the combinatorial adapter, not grid realizability.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_frozen_fork_surplus import row_components
from check_frozen_first_destination_allocation import maximum_matching, fixture as unported_fixture
from check_compensation_flow_normal_form import owner_data, solve, blocked_sources, abstract
from check_beta_exchange_gate_reduction import physical_data
from check_interval_connector_cycles_and_missing_ports import whole_bands, stack
from check_terminal_cancellation_and_stranded_demand import terminal_data, cancel_pairs, direct_family
from check_even_bridge_support_completion import endpoints_of
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Run without -O: validation requires assertions.')


def analyze(tips, adjacency, target_owner, access, totals):
    sources = sorted(tips)
    assert all(len(pair) == 2 and (sum(pair[0])-sum(pair[1])) % 2 == 1 for pair in tips.values())
    assert len({v for pair in tips.values() for v in pair}) == 2*len(sources)
    # One BP of each checkerboard color per beta; one BP globally per mixed.
    slots = [(owner, sum(v) % 2) for v, owner in target_owner.items() if owner[0] == 'beta']
    assert len(set(slots)) == len(slots)
    mixed_owners = [owner for owner in target_owner.values() if owner[0] == 'mixed']
    assert len(set(mixed_owners)) == len(mixed_owners)
    beta_incidence = {a: {target_owner[d] for v in tips[a] for d in adjacency[v]
                           if target_owner[d][0] == 'beta'} for a in sources}
    simple_incidence = {a: beta_incidence[a] | {('interval', i) for i in access.get(a, set())}
                        for a in sources}
    beta_matching = maximum_matching(beta_incidence)
    simple_matching = maximum_matching(simple_incidence)
    worst_beta = worst_simple = 0
    tight_beta = tight_simple = []
    for mask in range(1 << len(sources)):
        chosen = {a for i, a in enumerate(sources) if mask >> i & 1}
        x = {v for a in chosen for v in tips[a]}
        components = row_components(x, adjacency)
        ds = set().union(*(dd for _, dd, _ in components)) if components else set()
        c = Counter(sum(next(iter(dd))) % 2 for _, dd, surplus in components if surplus)
        q = Counter(sum(d) % 2 for d in ds if target_owner[d][0] == 'mixed')
        beta_tips = Counter(target_owner[d] for d in ds if target_owner[d][0] == 'beta')
        b1 = Counter(sum(d) % 2 for d in ds if target_owner[d][0] == 'beta'
                     and beta_tips[target_owner[d]] == 1)
        intervals = set().union(*(access.get(a, set()) for a in chosen)) if chosen else set()
        score = len(chosen)-len(beta_tips)
        assert 2*score == sum(q.values())-sum(c.values())-sum(b1.values())
        for color in (0, 1):
            assert score == q[color]-c[color]-b1[1-color]
        simple_score = score-len(intervals)
        if score >= worst_beta:
            worst_beta, tight_beta = score, sorted(chosen)
        if simple_score >= worst_simple:
            worst_simple, tight_simple = simple_score, sorted(chosen)
        totals['exact_owner_subset_ledgers'] += 1
    k = len(sources)
    assert worst_beta == k-len(beta_matching)
    assert worst_simple == k-len(simple_matching)
    components = row_components({v for pair in tips.values() for v in pair}, adjacency)
    e = Counter()
    for _, dd, surplus in components:
        color = sum(next(iter(dd))) % 2
        q = sum(target_owner[d][0] == 'mixed' for d in dd)
        e[color] += q-int(surplus and q > 0)
    color_matchings = []
    for color in (0, 1):
        incidence = {a: {target_owner[d] for v in tips[a] for d in adjacency[v]
                          if sum(d) % 2 == color and target_owner[d][0] == 'beta'} for a in sources}
        matching = maximum_matching(incidence)
        assert k-len(matching) == e[color]
        color_matchings.append(sorted(matching.items()))
        totals['exact_monochromatic_matching_controls'] += 1
    assert worst_beta <= min(e[0], e[1])
    totals['models'] += 1
    totals['strict_two_color_improvements'] += worst_beta < min(e[0], e[1])
    return dict(alpha=k, beta_deficit=worst_beta, simple_deficit=worst_simple,
                excess_by_bp_color=[e[0], e[1]], beta_matching=sorted(beta_matching.items()),
                simple_matching=sorted(simple_matching.items()), color_matchings=color_matchings,
                tight_beta_subset=tight_beta, tight_simple_subset=tight_simple)


def verify_phase_network(kinds, pairs, links, access, resources, colors, totals, all_cuts=False):
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    assert all(colors[a] != colors[b] for a, b in pairs)
    assert all(colors[a] != colors[b] for a, b in links)
    phase = {m: colors[next(v for v in pairs[m] if kinds[v] == 'TP')] for m in mixed}
    result = solve(kinds, pairs, links, access, resources)
    route_phases = []
    for route in result['routes']:
        values = set()
        for tag in route:
            if tag[0] in ('link', 'access'):
                values.add(colors[tag[1]])
            elif tag[0] == 'mixed':
                values.add(phase[tag[1]])
        assert len(values) == 1
        route_phases.append(next(iter(values)))
    per_phase = []
    for gamma in (0, 1):
        ll = [(a, b) for a, b in links if colors[a] == gamma]
        aa = {v: rr if colors[v] == gamma else set() for v, rr in access.items()}
        per_phase.append((ll, aa))

    def split_blocked(removed):
        rr = {tag for tag in removed if tag[0] != 'mixed'}
        blocked = []
        for gamma, (ll, aa) in enumerate(per_phase):
            gg = {tag for tag in removed if tag[0] == 'mixed' and phase[tag[1]] == gamma}
            blocked.append(blocked_sources(kinds, pairs, ll, aa, resources, rr | gg))
        combined = blocked[0] & blocked[1]
        assert combined == blocked_sources(kinds, pairs, links, access, resources, removed)
        return combined, blocked

    cut = set(result['cut'])
    blocked, bb = split_blocked(cut)
    assert len(blocked)-len(cut) == result['deficit']
    result['route_phases'] = route_phases
    result['phase_blocked_at_min_cut'] = [sorted(x) for x in bb]
    result['shared_resources_at_min_cut'] = sorted(tag for tag in cut if tag[0] != 'mixed')
    if all_cuts:
        units = [('mixed', m) for m in sorted(mixed)]+[('beta', b) for b in sorted(betas)]
        units += [('interval', r) for r in sorted(resources)]
        best = incorrectly_doubled = 0
        for mask in range(1 << len(units)):
            removed = {tag for i, tag in enumerate(units) if mask >> i & 1}
            combined, _ = split_blocked(removed)
            score = len(combined)-len(removed)
            best = max(best, score)
            repeated_resource_count = sum(tag[0] != 'mixed' for tag in removed)
            incorrectly_doubled = max(incorrectly_doubled, score-repeated_resource_count)
            totals['exhaustive_colored_full_route_cuts'] += 1
        assert best == result['deficit']
        result['incorrect_double_resource_cut_deficit'] = incorrectly_doubled
    totals['colored_full_route_models'] += 1
    totals['phase_preserving_routes'] += len(route_phases)
    return result


def physical(current, totals):
    direct_check(*current)
    assert frozen_certificate(current)[0] == endpoints_of(current)
    kinds, pairs, links, access, resources = physical_data(current)
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    _, _, _, _, _, _, ports = terminal_data(current, whole_bands(current))
    # Cover every both-missing original alpha, even if other alphas are ported.
    unported = {a for a in alphas if all(not ports[v] for v in pairs[a])}
    tips = {a: pairs[a] for a in unported}
    adjacency = {v: {d for p, d in links if p == v} for a in tips for v in tips[a]}
    targets = {d: ('beta' if owners[d] in betas else 'mixed', owners[d])
               for ds in adjacency.values() for d in ds}
    owner_access = {a: set().union(*(access.get(v, set()) for v in pairs[a])) for a in tips}
    result = analyze(tips, adjacency, targets, owner_access, totals)
    matched = dict(result['simple_matching'])
    selected, payments = [], []
    for a, (category, target) in sorted(matched.items()):
        if category == 'beta':
            selected.append(next((p, d) for p, d in links if owners[p] == a and owners[d] == target))
        else:
            p = next(v for v in pairs[a] if target in access.get(v, set()))
            payments.append((p, target))
    reduced, inventory, _ = cancel_pairs(kinds, pairs, selected, Counter())
    assert len({v for link in selected for v in link}) == 2*len(selected)
    assert len({r for _, r in payments}) == len(payments)
    assert all(any(p in pair and all(kinds[v] == 'TP' for v in pair) for pair in reduced)
               for p, _ in payments)
    assert len(betas)-inventory['BP', 'BP'] == len(selected)
    assert len(selected)+len(payments) == len(unported)-result['simple_deficit']
    result['lifted_simple_certificate'] = dict(links=selected, payments=payments)
    result['all_original_alphas_unported'] = unported == alphas
    if alphas:
        full = verify_phase_network(kinds, pairs, links, access, resources,
                                    {v: sum(v) % 2 for v in kinds}, totals)
        if unported == alphas:
            assert full['value'] >= len(unported)-result['simple_deficit']
            result['full_route_deficit'] = full['deficit']
            totals['simple_deficit_but_full_routes_complete'] += result['simple_deficit'] > 0 and full['deficit'] == 0
    totals['fully_frozen_geometry_controls'] += 1
    return result


def asymmetric_family(width, height):
    current = direct_family(width, height)
    return (*current[:2], current[2]-{(width+5, 5)}, current[3])


def asymmetric_certificate(current, width, height, totals):
    """Old uniform schedule, with exactly one event postponed/re-witnessed."""
    r = width+4
    schedule = [((5, 3), ((4, 3), (5, 2))), ((5, 7), ((4, 7), (5, 8))),
                ((r, 3), ((r, 2), (r+1, 3))),
                ((r, height+3), ((r, height+4), (r+1, height+3))),
                ((5, 5), ((4, 5), (5, 6)))]
    for c in range(height+1, 5, -2):
        schedule.append(((r, c), ((r+1, c), (r, c+1))))
    for c in range(6, height+3, 2):
        schedule.append(((r-1, c), ((r-2, c), (r, c))))
    schedule.append(((r, 5), ((r-1, 5), (r, 6))))
    schedule.append(((r-1, 4), ((r-1, 3), (r-1, 5))))
    for row in range(6, r-1, 2):
        schedule += [((row, 4), ((row-1, 4), (row, 3))),
                     ((row+1, 3), ((row, 3), (row+1, 4)))]
    for row in range(r-2, 5, -2):
        schedule += [((row, 3), ((row+1, 3), (row, 4))),
                     ((row-1, 4), ((row-1, 3), (row, 4)))]
    schedule.append(((5, 6), ((6, 6), (5, 5))))
    for c in range(4, height+3, 2):
        schedule.append(((r, c), ((r, c-1), (r-1, c))))
        if c <= height:
            schedule.append(((r-1, c+1), ((r-1, c), (r, c+1))))
    mate = {a: b for edge in current[3] for a, b in (edge, edge[::-1])}
    frozen = set()
    for v, witnesses in schedule:
        assert v in mate and v not in frozen and len(set(witnesses)) == 2
        assert all(abs(v[0]-w[0])+abs(v[1]-w[1]) == 1 and w != mate[v] for w in witnesses)
        assert all(w in current[2] or mate[w] in frozen for w in witnesses)
        frozen.add(v)
    assert frozen == set(mate)
    totals['uniform_asymmetric_certificate_events'] += len(schedule)
    return [[v, witnesses] for v, witnesses in schedule]


def assembly(first_color_count, second_color_count):
    base = asymmetric_family(6, 4)
    selected, matching = set(), []
    for i in range(first_color_count+second_color_count):
        flip = int(i >= first_color_count)
        move = lambda v: (v[0]+18*i, v[1]+flip)
        selected |= {move(v) for v in base[2]}
        matching += [tuple(map(move, edge)) for edge in base[3]]
    return 18*(first_color_count+second_color_count), 22, selected, matching


def random_profiles(totals):
    rng = random.Random(2026102505)
    for _ in range(800):
        k, b = rng.randrange(1, 7), rng.randrange(9)
        tips = {a: [] for a in range(k)}
        adjacency, targets = {}, {}
        row_index, mixed_index = 0, 0
        for color in (0, 1):
            aa = list(range(k)); rng.shuffle(aa)
            available_betas = list(range(b)); rng.shuffle(available_betas)
            cursor = 0
            while cursor < k:
                count = rng.randrange(1, min(4, k-cursor)+1)
                group = aa[cursor:cursor+count]; cursor += count
                surplus = count > 1 or rng.choice((False, True))
                row = 4*row_index+color; row_index += 1
                ds = [(row, 2*j) for j in range(count+int(surplus))]
                for d in ds:
                    if available_betas and rng.random() < .65:
                        targets[d] = ('beta', available_betas.pop())
                    else:
                        targets[d] = ('mixed', mixed_index); mixed_index += 1
                for j, a in enumerate(group):
                    v = row, 2*j+1
                    tips[a].append(v)
                    adjacency[v] = {ds[j]} | ({ds[j+1]} if surplus else set())
        resources = set(range(rng.randrange(5)))
        access = {a: {r for r in resources if rng.random() < .35} for a in tips}
        analyze(tips, adjacency, targets, access, totals)
        totals['abstract_colored_row_profiles_not_grid_claims'] += 1


def abstract_phase_controls(totals):
    rng = random.Random(2026102506)
    for _ in range(160):
        k, b, m = rng.randrange(1, 5), rng.randrange(4), rng.randrange(5)
        kinds, pairs, candidates = abstract(('alpha',)*k+('beta',)*b+('mixed',)*m)
        colors = {}
        for a, z in pairs:
            colors[a] = rng.randrange(2)
            colors[z] = 1-colors[a]
        links = [(a, z) for a, z in candidates if colors[a] != colors[z] and rng.random() < .3]
        resources = set(range(rng.randrange(4)))
        access = {v: {r for r in resources if rng.random() < .2} for v in kinds if kinds[v] == 'TP'}
        verify_phase_network(kinds, pairs, links, access, resources, colors, totals, True)
    kinds, pairs, _ = abstract(('alpha', 'alpha', 'beta'))
    colors = {v: v % 2 for v in kinds}
    beta = verify_phase_network(kinds, pairs, [(0, 5), (3, 4)], {}, set(), colors, totals, True)
    assert beta['deficit'] == 1 and beta['incorrect_double_resource_cut_deficit'] == 0
    kinds, pairs, _ = abstract(('alpha', 'alpha'))
    colors = {v: v % 2 for v in kinds}
    interval = verify_phase_network(kinds, pairs, [], {0: {0}, 3: {0}}, {0}, colors, totals, True)
    assert interval['deficit'] == 1 and interval['incorrect_double_resource_cut_deficit'] == 0
    return dict(shared_beta=beta, shared_interval=interval,
                scope='Colored original-terminal controls, not claimed fully frozen physical grids. '
                      'Distinct phase routes still share a whole beta or original interval unit.')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals, examples = Counter(), {}
    # All 480 physical families/offsets of the preceding exchange/fork work.
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
    for w in (6, 10, 20):
        network = combine([transform_module(module, (False, False, False), (w-2, w-2)) for module in star_modules(w)])
        fixtures.append((2*w+2, 2*w+2, network['selected'], network['matching']))
    for model, symmetry, offset in itertools.product(fixtures,
            itertools.product((False, True), repeat=3), itertools.product((2, 3), repeat=2)):
        physical(pad_image(model, symmetry, offset), totals)
    totals['carried_physical_controls'] = totals['fully_frozen_geometry_controls']
    for w, h in itertools.product(range(6, 31, 2), range(4, 21, 2)):
        model = asymmetric_family(w, h)
        schedule = asymmetric_certificate(model, w, h, totals)
        result = physical(model, totals)
        assert result['alpha'] == 1 and result['excess_by_bp_color'] == [0, 1]
        assert result['beta_deficit'] == result['simple_deficit'] == 0
        if (w, h) == (6, 4):
            examples['asymmetric_base'] = dict(shape=model[:2], selected=sorted(model[2]),
                matching=model[3], freezing_schedule=schedule, result=result)
    for p, q in itertools.product(range(5), repeat=2):
        if not p+q:
            continue
        result = physical(assembly(p, q), totals)
        assert result['alpha'] == p+q and result['excess_by_bp_color'] == [q, p]
        assert result['beta_deficit'] == 0
        if (p, q) in ((4, 0), (2, 2)):
            examples['assembly_'+str(p)+'_'+str(q)] = result
    from check_arbitrary_depth_cap_relays import relay_family
    for depth in (1, 2, 5):
        model = relay_family(8, 2*max(depth, 2), depth, depth)[0]
        result = physical(model, totals)
        assert result['beta_deficit'] == result['simple_deficit'] == 1
        assert result['full_route_deficit'] == 0
        examples['relay_depth_'+str(depth)] = result
    random_profiles(totals)
    examples['opposite_phase_resource_nonreuse'] = abstract_phase_controls(totals)
    report = dict(status='PASS', totals=dict(totals), examples=examples,
                  scope='General written exact colored row-owner Hall identities and one-hop allocation criterion; '
                        'uniform asymmetric frozen construction with explicit serial certificate; phase-preserving full routes '
                        'Abstract profiles are not claimed realizable grids. A one-hop failure is not a full-route '
                        'or target-bound counterexample. Universal geometric resource cuts/5of6 remain open.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals))))

if __name__ == '__main__':
    main()
