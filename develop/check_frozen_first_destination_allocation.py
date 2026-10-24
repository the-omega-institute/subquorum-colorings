"""First-destination allocation, and source sharing after all direct payments.

Enumeration checks the abstract two-witness lemma. The explicit frozen fixture
checks a geometric counterexample; neither enumeration proves a global grid bound.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data, physical, solve
from check_compensation_flow_geometry_frontier import pad_image
from check_frozen_missing_port_bp_injection import inspect as missing_injection
from check_frozen_shared_mixed_gate import check_rank_certificate, fixture as previous_fixture
from check_interval_connector_cycles_and_missing_ports import stack, whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_terminal_cancellation_and_stranded_demand import (
    cancel_pairs, extended_ports, terminal_data,
)

if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')

FIXTURE = Path(__file__).parent / 'fixtures/unported_shared_mixed_gate.json'


def fixture():
    record = json.loads(FIXTURE.read_text())
    current = (*record['shape'], set(map(tuple, record['selected'])),
               [tuple(map(tuple, edge)) for edge in record['matching']])
    layers = [[tuple(v) for v in layer] for layer in record['freezing_layers']]
    return current, layers


def maximum_matching(incidence):
    assignment = {}

    def augment(demand, seen):
        for target in sorted(incidence[demand]):
            if target in seen:
                continue
            seen.add(target)
            if target not in assignment or augment(assignment[target], seen):
                assignment[target] = demand
                return True
        return False

    for demand in sorted(incidence):
        augment(demand, set())
    return {demand: target for target, demand in assignment.items()}


def saturating(incidence):
    matching = maximum_matching(incidence)
    assert len(matching) == len(incidence)
    return matching


def unported_beta_deficit(witnesses):
    """Exact deficit = components whose two endpoints are mixed owners."""
    adjacency = defaultdict(set)
    for alpha, targets in witnesses.items():
        assert len(targets) == 2
        for target in targets:
            assert target[0] in ('mixed', 'beta')
            a, t = ('alpha', alpha), ('target', target)
            adjacency[a].add(t)
            adjacency[t].add(a)
    remaining, bad, transfers = set(adjacency), [], {}
    while remaining:
        start = min(remaining)
        reached, pending = {start}, [start]
        while pending:
            v = pending.pop()
            for other in adjacency[v]-reached:
                reached.add(other)
                pending.append(other)
        remaining -= reached
        alphas = {v[1] for v in reached if v[0] == 'alpha'}
        betas = {v[1] for v in reached if v[0] == 'target' and v[1][0] == 'beta'}
        mixed = {v[1] for v in reached if v[0] == 'target' and v[1][0] == 'mixed'}
        assert len(mixed) <= 2
        if len(mixed) == 2:
            assert len(alphas) == len(betas)+1
            bad.append(dict(alphas=sorted(alphas), mixed=sorted(mixed)))
            chosen = min(mixed)
            tips = adjacency['target', chosen]
            assert len(tips) == 1
            transfers[next(iter(tips))[1]] = chosen
        else:
            assert len(alphas) <= len(betas)
    beta_incidence = {a: {t for t in targets if t[0] == 'beta'}
                      for a, targets in witnesses.items()}
    best = maximum_matching(beta_incidence)
    q = len({t for targets in witnesses.values() for t in targets if t[0] == 'mixed'})
    assert len(best) == len(witnesses)-len(bad)
    assert len(bad) <= q//2
    remainder = {a: targets for a, targets in beta_incidence.items() if a not in transfers}
    optimized = saturating(remainder)
    optimized.update(transfers)
    assert len(optimized) == len(witnesses) and len(set(optimized.values())) == len(optimized)
    assert all(target in witnesses[a] for a, target in optimized.items())
    return dict(beta_paid=len(best), exact_deficit=len(bad), mixed_targets=q,
                mixed_ended_components=bad, beta_matching=sorted(best.items()),
                optimized_first_destinations=sorted(optimized.items()))


def first_destinations(current, bands, totals):
    original, labels, intervals, interval_owner, kinds, pairs, ports = terminal_data(current, bands)
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    injection = dict(missing_injection(current, bands, Counter(), True)['assignment'])
    tokens, by_target = {}, defaultdict(list)
    marked = {interval_owner[b, 0] for b in range(len(bands))}
    marked |= {interval_owner[b, len(band)-1] for b, band in enumerate(bands)
               if len(band) % 2 == 0 and labels[b][-1] == ('B', 'B')}
    for alpha in sorted(alphas):
        for terminal in pairs[alpha]:
            if ports[terminal]:
                target = ('interval', interval_owner[ports[terminal][0]])
                witness = terminal, target
            else:
                bp = injection[terminal]
                category = 'beta' if owners[bp] in betas else 'mixed'
                assert owners[bp] in betas | mixed
                target = category, owners[bp]
                witness = terminal, bp
            tokens[terminal] = dict(alpha=alpha, target=target, witness=witness)
            by_target[target].append(terminal)
    assert len(tokens) == 2*len(alphas)
    for target, tips in by_target.items():
        assert len(tips) <= (1 if target[0] == 'mixed' else 2)
    incidence = {alpha: {tokens[tip]['target'] for tip in pairs[alpha]} for alpha in alphas}
    selected = saturating(incidence)
    links, payments, deferred = [], [], []
    for alpha, target in selected.items():
        terminal = next(tip for tip in pairs[alpha] if tokens[tip]['target'] == target)
        if target[0] != 'interval':
            links.append(tokens[terminal]['witness'])
        if target[0] == 'mixed' or (target[0] == 'interval' and target[1] in marked):
            deferred.append(alpha)
        elif target[0] == 'interval':
            payments.append((terminal, target[1]))
    assert len({v for edge in links for v in edge}) == 2*len(links)
    assert len(set(selected.values())) == len(selected)
    reduced, inventory, _ = cancel_pairs(kinds, pairs, links, Counter())
    used_betas = sum(target[0] == 'beta' for target in selected.values())
    assert original['beta']-inventory['BP', 'BP'] == used_betas
    final_alphas = [pair for pair in reduced if all(kinds[v] == 'TP' for v in pair)]
    for tip, resource in payments:
        assert sum(tip in pair for pair in final_alphas) == 1
        assert any(interval_owner[p] == resource for p in ports[tip])
    assert len(alphas)-used_betas-len(payments) == len(deferred)
    for mask in range(1 << len(alphas)):
        subset = {a for i, a in enumerate(sorted(alphas)) if mask >> i & 1}
        targets = set().union(*(incidence[a] for a in subset)) if subset else set()
        mixed_count = sum(t[0] == 'mixed' for t in targets)
        assert 2*len(subset) <= 2*(len(targets)-mixed_count)+mixed_count
        totals['weighted_Hall_subsets'] += 1
    totals['physical_first_destination_models'] += 1
    totals['first_destination_alphas'] += len(alphas)
    result = dict(alpha=len(alphas), selected=sorted(selected.items()), links=links,
                  payments=payments, deferred=deferred)
    if all(not ports[tip] for a in alphas for tip in pairs[a]):
        witnesses = {a: [tokens[tip]['target'] for tip in pairs[a]] for a in alphas}
        result['unported_beta'] = unported_beta_deficit(witnesses)
        totals['unported_exact_beta_models'] += 1
    return result


def partitions(tokens):
    """Every set partition into singleton/pair blocks, exactly once."""
    if not tokens:
        yield []
        return
    first, *rest = tokens
    for tail in partitions(rest):
        yield [(first,)]+tail
    for i, other in enumerate(rest):
        for tail in partitions(rest[:i]+rest[i+1:]):
            yield [(first, other)]+tail


def abstract_controls(totals):
    for count in range(1, 6):
        for blocks in partitions(list(range(2*count))):
            incidence = {a: set() for a in range(count)}
            for i, block in enumerate(blocks):
                for token in block:
                    incidence[token//2].add(i)
            matching = saturating(incidence)
            assert all(target in incidence[a] for a, target in matching.items())
            for mask in range(1 << count):
                subset = {a for a in range(count) if mask >> a & 1}
                targets = set().union(*(incidence[a] for a in subset)) if subset else set()
                singletons = sum(len(blocks[i]) == 1 for i in targets)
                assert 2*len(subset) <= 2*len(targets)-singletons
            totals['abstract_token_partitions'] += 1
            singleton_indices = [i for i, block in enumerate(blocks) if len(block) == 1]
            masks = (range(1 << len(singleton_indices)) if count <= 4 else
                     sorted({0, (1 << len(singleton_indices))-1}))
            for mask in masks:
                mixed = {i for j, i in enumerate(singleton_indices) if mask >> j & 1}
                witnesses = {a: [] for a in range(count)}
                for i, block in enumerate(blocks):
                    target = ('mixed' if i in mixed else 'beta', i)
                    for token in block:
                        witnesses[token//2].append(target)
                unported_beta_deficit(witnesses)
                totals['typed_unported_token_models'] += 1


def obstacle(current, bands, move, layers):
    direct_check(*current)
    witnesses = check_rank_certificate(current, layers)
    assert frozen_certificate(current)[0] == {v for e in current[3] for v in e}
    data = terminal_data(current, bands)
    original, labels, intervals, interval_owner, kinds, pairs, ports = data
    owners, alphas, betas, mixed = owner_data(kinds, pairs)
    critical = [tuple(map(move, pair)) for pair in
                [((3, 6), (5, 9)), ((5, 11), (10, 11)), ((5, 10), (10, 4))]]
    assert alphas == {owners[critical[0][0]], owners[critical[1][0]]}
    assert all(frozenset(pair) in {frozenset(p) for p in pairs} for pair in critical)
    extended = extended_ports(current, bands, labels, intervals, interval_owner, kinds, ports, Counter())
    assert all(not extended[v] for pair in critical[:2] for v in pair)
    assert all([kinds[v] for v in pair] == ['TP', 'TP'] for pair in critical[:2])
    assert [kinds[v] for v in critical[2]] == ['BP', 'TP']
    links = [(move(v), move((5, 10))) for v in [(5, 9), (5, 11)]]
    assert all(abs(a[0]-b[0])+abs(a[1]-b[1]) == 1 for a, b in links)
    resources = {interval_owner[5, 2], interval_owner[5, 5]}
    marked = {interval_owner[b, c] for b in range(len(bands)) for c in (0, len(bands[b])-1)}
    assert len(resources) == 2 and not resources & marked
    assert {(5, 2), (5, 5)} <= set(extended[critical[2][1]])
    local_kinds = {v: kinds[v] for pair in critical for v in pair}
    restricted = solve(local_kinds, critical, links, {critical[2][1]: resources}, resources)
    assert (restricted['value'], restricted['cost'], restricted['deficit']) == (1, 1, 1)
    full_links = [(move((3, 6)), move((3, 7))), (move((5, 11)), move((5, 12)))]
    assert owners[move((3, 7))] in betas and owners[move((5, 12))] in betas
    assert owners[move((3, 7))] != owners[move((5, 12))]
    assert all(abs(a[0]-b[0])+abs(a[1]-b[1]) == 1 for a, b in full_links)
    _, final_inventory, _ = cancel_pairs(kinds, pairs, full_links, Counter())
    assert final_inventory['TP', 'TP'] == 0
    return dict(original={k: original[k] for k in
                          ('alpha', 'beta', 'gamma', 'balance', 'boundary_budget', 'surplus_twice')},
                critical_pairs=critical, direct_maximum=0, restricted=restricted,
                full_two_beta_links=full_links, strict_rank_witnesses=witnesses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    totals = Counter()
    abstract_controls(totals)
    current, layers = fixture()
    base = obstacle(current, whole_bands(current), lambda v: v, layers)
    full = physical(current, whole_bands(current), [], Counter())
    assert (full['value'], full['cost'], full['deficit']) == (2, 2, 0)
    images = []
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, *symmetry)
        move = image_map(*current[:2], symmetry)
        bands = [[tuple(map(move, col)) for col in band] for band in whole_bands(current)]
        image = (*shape, selected, matching)
        checked = obstacle(image, bands, move, [list(map(move, layer)) for layer in layers])
        first = first_destinations(image, bands, totals)
        images.append(dict(symmetry=symmetry, direct=checked['direct_maximum'],
                           restricted=checked['restricted']['value'], first=first))
    fixtures = [previous_fixture(), current]+[stack(6, 4, [kind]) for kind in ('missing', 'cycle', 'collision')]
    unported_examples = []
    for model, symmetry, offset in itertools.product(fixtures,
            itertools.product((False, True), repeat=3), itertools.product((2, 3), repeat=2)):
        image = pad_image(model, symmetry, offset)
        first = first_destinations(image, whole_bands(image), totals)
        exact = first.get('unported_beta')
        if exact and exact['exact_deficit'] and not unported_examples:
            unported_examples.append(dict(shape=image[:2], symmetry=symmetry, offset=offset,
                                           alpha=first['alpha'], exact=exact))
    assert unported_examples and unported_examples[0]['exact']['exact_deficit'] == 1
    report = dict(status='PASS', totals=dict(totals), base=base, full_network=full, images=images,
                  unported_exact_beta_obstruction=unported_examples,
                  scope='Written first-destination lemma and exact two-mixed-ended beta deficit, '
                  'based on frozen missing-port injection and degree-two witness graphs; '
                  'finite partition checks are regression '
                  'only. Explicit no-direct-access frozen witness disproves source separation after '
                  'maximum direct prepayment. Restricted rule deficit1; full network deficit0, '
                  'minimum cost2 via two distinct whole betas. No universal grid/5/6 result.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals), direct=0, restricted=1, full=2, cost=2)))


if __name__ == '__main__':
    main()
