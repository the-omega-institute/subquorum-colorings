"""Original single-square wires, exact routing counts and safe owner pruning.

No solver dependency. General proofs are in SINGLE_SQUARE_WIRES_AND_SOURCE_FREE_PRUNING.md.
"""
import argparse
from collections import Counter, defaultdict
import itertools as it
import json
from pathlib import Path
import random

from check_single_square_parity import single_square, central_patterns
from check_odd_arm_compensation import odd_arms
from check_owned_donors import endpoint_data
from check_whole_support_fork_normal_form import whole_support_data, brute, evaluate
from check_whole_support_fork_flow import fork_flow
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_compensation_flow_normal_form import owner_data
from check_promotion_cores import frozen_certificate
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_residual_corridors import direct_check, graph_record, transformed
from check_multisource_relay_bypass import solve as relay_solve

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def image(cur, symmetry):
    shape, T, M = transformed(*cur, *symmetry)
    return *shape, T, M


def prune(data, removed):
    kinds, pairs, links, W, I = data
    keep = [i for i in range(len(pairs)) if i not in removed]
    tips = {v for i in keep for v in pairs[i]}
    return ({v: kinds[v] for v in tips}, [pairs[i] for i in keep],
            [e for e in links if set(e) <= tips], {k: W[i] for k, i in enumerate(keep)}, I)


def restrict(data, Q):
    return (*data[:3], {a: W & Q for a, W in data[3].items()}, Q)


def inspect_square(cur, counts):
    direct_check(*cur)
    P, adjacency, squares = endpoint_data(cur)
    assert len(squares) == 1
    r, c = next(iter(squares)); assert r % 2 == c % 2 == 0
    reached = {(r, c)}; todo = [(r, c)]
    while todo:
        for v in adjacency[todo.pop()]:
            if v not in reached:
                reached.add(v); todo.append(v)
    assert reached == P
    Q = {(r+i, c+j) for i in range(2) for j in range(2)}
    lengths = [sum(v[0] < r for v in P), sum(v[1] > c+1 for v in P),
               sum(v[0] > r+1 for v in P), sum(v[1] < c for v in P)]
    a = [n//2 for n in lengths]; eps = [n % 2 for n in lengths]; o = sum(eps)
    assert o in (0, 2, 4) and eps[0]+eps[2] == eps[1]+eps[3] == o//2
    frozen, _ = frozen_certificate(cur)
    assert (frozen == P) == (o >= 2)
    d, meta, _ = whole_support_data(cur, whole_bands(cur))
    owner, A, B, M = owner_data(*d[:2]); assert not A and not B
    mate = {v: w for e in cur[3] for v, w in (e, e[::-1])}
    assert all((lambda bp: mate[bp][0] == bp[0])(
        next(v for v in d[1][m] if d[0][v] == 'BP')) for m in M)
    edges = {(owner[u], owner[v]) for u, v in d[2] if owner[u] != owner[v]}
    incoming = Counter(v for _, v in edges); outgoing = defaultdict(list)
    for u, v in edges:
        outgoing[u].append(v)
    assert all(incoming[m] <= 1 and len(outgoing[m]) <= 1 for m in M)
    chains = []; seen = set()
    for start in sorted(m for m in M if incoming[m] == 0):
        chain = []; u = start
        while True:
            assert u not in seen; seen.add(u); chain.append(u)
            if not outgoing[u]:
                break
            u = outgoing[u][0]
        chains.append(chain)
    assert seen == M
    predicted = sorted(n for n in [a[1]+eps[1], a[3]+eps[3]] if n)
    assert sorted(map(len, chains)) == predicted
    assert len(M) == a[1]+a[3]+o//2
    assert len(edges) == sum(max(n-1, 0) for n in predicted)
    assert sum(owner[u] == owner[v] for u, v in d[2]) == a[1]+a[3]
    vi = sum(set(e) <= Q and e[0][1] == e[1][1] for e in cur[3])
    hi = sum(set(e) <= Q and e[0][0] == e[1][0] for e in cur[3])
    cycles = sum(comp['kind'] == ['cycle'] for comp in meta['original']['components'])
    assert cycles == a[0]*(1-eps[0])+a[2]*(1-eps[2])+vi+int(hi == 2)
    g, _ = graph_record(*cur)
    tiles = {(v[0]//2, v[1]//2) for v in P}
    charge2 = sum(g['deg'][x*(cur[1]//2)+y]-2*g['r'][x*(cur[1]//2)+y] for x, y in tiles)
    assert charge2 == -o
    counts['single_square_images'] += 1
    counts['fully_frozen_single_square_images'] += o >= 2
    counts['source_free_mixed_owners'] += len(M)
    counts['original_pp_m_cycles'] += cycles
    counts['nonself_chain_links'] += len(edges)
    return dict(lengths=lengths, odd_arms=o, mixed=len(M), cycles=cycles, chains=predicted)


def shared_gap(C):
    base = odd_arms((0, 0, 0, 0))
    return (10, C+6, base[2] | {(2, C), (5, C), (3, C+1), (4, C-1)},
            base[3]+[((3, C), (4, C))])


def shared_gap_checks(counts):
    records = []
    for C in range(10, 51, 2):
        for fr, fc in it.product((False, True), repeat=2):
            cur = image(shared_gap(C), (False, fr, fc)); direct_check(*cur)
            P, adj, squares = endpoint_data(cur)
            assert frozen_certificate(cur)[0] == P and len(squares) == 1
            start = next(iter(squares)); H = {start}; todo = [start]
            while todo:
                for v in adj[todo.pop()]:
                    if v not in H:
                        H.add(v); todo.append(v)
            assert len(H) == 8
            graph, _ = graph_record(*cur)
            receiver_tiles = {(r//2, c//2) for r, c in H}
            assert sum(graph['deg'][r*(cur[1]//2)+c]-2*graph['r'][r*(cur[1]//2)+c]
                       for r, c in receiver_tiles) == -4
            d, meta, _ = whole_support_data(cur, whole_bands(cur))
            owner, A, B, M = owner_data(*d[:2])
            removed = {owner[v] for v in H if v in owner}
            assert len(A) == 1 and not B and removed == M and len(M) == 2
            a = next(iter(A)); old_units = set(d[4]); kept = prune(d, removed)
            assert kept[4] == old_units and kept[3][0] == d[3][a]
            dead_support = set().union(*(d[3][m] for m in removed))
            shared = dead_support & d[3][a]
            assert shared
            if not fr and not fc:
                north = {j for j in shared if meta['intervals'][j]['band'] == 1 and
                         5 <= meta['intervals'][j]['first'] <= meta['intervals'][j]['last'] < C}
                assert len(north) == C-6
            unit = min(shared)
            for Q in [set(), {unit}, old_units, {j for j in old_units if j % 3 == 0}]:
                original = fork_flow(*restrict(d, Q)); reduced = fork_flow(*restrict(kept, Q))
                assert (original['value'], original['cost']) == (reduced['value'], reduced['cost'])
                assert original['value'] == bool(Q & d[3][a]) and original['cost'] == 0
                counts['shared_gap_pruning_flow_comparisons'] += 1
            wrong_Q = {unit}-dead_support
            wrong = fork_flow(*restrict(kept, wrong_Q))
            assert wrong['value'] == 0
            counts['frozen_shared_gap_images'] += 1
            counts['resource_deletion_countercontrols'] += 1
            if C == 10 and not fr and not fc:
                # Exhaust all 2^12 original source-support availability subsets.
                units = sorted(d[3][a]); assert len(units) == 12
                others = sorted(old_units-set(units)); rng = random.Random(20261025099)
                for mask in range(1 << len(units)):
                    Q = {j for i, j in enumerate(units) if mask >> i & 1}
                    Q |= {j for j in others if rng.random() < .4}
                    x = fork_flow(*restrict(d, Q)); y = fork_flow(*restrict(kept, Q))
                    assert (x['value'], x['cost']) == (y['value'], y['cost']) == (int(mask != 0), 0)
                    if mask < 64:
                        exact, n = brute(*restrict(d, Q))
                        assert exact == (x['value'], x['cost'])
                        counts['independent_shared_gap_terminal_matchings'] += n
                    counts['all_source_support_subsets'] += 1
                records.append(dict(C=C, shape=cur[:2], selected=sorted(cur[2]), matching=cur[3],
                    removed_owner_tips=[d[1][m] for m in sorted(removed)],
                    original_alpha=d[1][a], shared_example=meta['intervals'][unit],
                    source_support_units=len(units), north_shared_units=C-6,
                    correct_payment=1, wrong_resource_deletion_payment=0))
    return records


def same_owner_obstruction(counts):
    path = Path(__file__).parent/'fixtures/frozen_mixed_cycle_square_switch.json'
    j = json.loads(path.read_text())
    cur = (*j['shape'], set(map(tuple, j['selected'])), [tuple(map(tuple, e)) for e in j['matching']])
    direct_check(*cur); P = {v for e in cur[3] for v in e}
    frozen, layers = frozen_certificate(cur); assert frozen == P
    check_rank_certificate(cur, [[w['endpoint'] for w in layer] for layer in layers])
    d, meta, _ = whole_support_data(cur, whole_bands(cur)); owner, A, B, M = owner_data(*d[:2])
    target = owner[5, 18]; sources = [owner[5, 17], owner[5, 19]]
    assert target in M and set(sources) <= A and len(set(sources)) == 2
    assert set(d[1][target]) == {(5, 18), (12, 14)}
    comp = next(comp for comp in meta['original']['components'] if (5, 16) in map(tuple, comp['nodes']))
    assert (5, 17) in list(map(tuple, comp['nodes'])) and comp['kind'] == ['BP', 'TP']
    assert list(map(tuple, comp['nodes'])) == [(2, 18), (3, 18), (4, 18), (5, 18), (6, 18),
        (6, 17), (5, 17), (4, 17), (4, 16), (5, 16), (5, 15), (5, 14), (6, 14)]
    g, _ = graph_record(*cur); idx = 5*(cur[1]//2)+8
    assert (g['t'][idx], g['h'][idx], g['s'][idx], g['r'][idx], g['deg'][idx]) == (0, 0, 0, 2, 4)
    assert {(r, c) for r in (10, 11) for c in (16, 17)} <= P
    Q = {i for i in d[4] if (meta['intervals'][i]['band'], meta['intervals'][i]['first'], meta['intervals'][i]['last'])
         in [(5, 10, 10), (5, 12, 12)]}
    assert len(Q) == 2 and Q <= d[3][target] and all(not d[3][s] for s in sources)
    chosen = sources+[target]; tips = {v for a in chosen for v in d[1][a]}
    restricted = ({v: d[0][v] for v in tips}, [d[1][a] for a in chosen],
                  [e for e in d[2] if set(e) <= tips], {i: d[3][a] & Q for i, a in enumerate(chosen)}, Q)
    actual = fork_flow(*restricted); independent, n = brute(*restricted)
    assert (actual['value'], actual['cost']) == independent == (1, 1) and n == 3
    false = relay_solve(dict(direct={0: {}, 1: {}}, gates={0: dict(capacity=2,
                        entry={0: 1, 1: 1}, output={u: 0 for u in Q})}), Q)
    assert (false['value'], false['cost']) == (2, 2)
    complete = fork_flow(*d)
    assert (complete['value'], complete['cost'], len(A)) == (4, 2, 4)
    assert evaluate(*d[:2], complete['links'], *d[3:])['value'] == 4
    counts['same_owner_frozen_tile_obstructions'] += 1
    counts['independent_same_owner_terminal_matchings'] += n
    return dict(fixture=path.name, shape=cur[:2], endpoints=len(P), selected=len(cur[2]),
                tile=[5, 8], residual_capacity=2, residual_degree=4, mixed_ends=d[1][target],
                original_trace=comp['nodes'], source_ends=[d[1][s] for s in sources],
                original_units=[meta['intervals'][i] for i in sorted(Q)],
                actual_restricted=[1, 1], false_capacity_two=[2, 2],
                complete_board=[4, 2], complete_certificates=complete['certificates'])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--output', type=Path, required=True); args = ap.parse_args()
    counts = Counter()
    for pattern in central_patterns():
        for parameters in it.product(range(3), repeat=4):
            cur, _ = single_square(parameters, pattern)
            for symmetry in it.product((False, True), repeat=3):
                inspect_square(image(cur, symmetry), counts)
        inspect_square(single_square((8, 13, 21, 34), pattern)[0], counts)
    gap = shared_gap_checks(counts); same = same_owner_obstruction(counts)
    result = dict(status='PASS', counts=dict(counts), shared_gap=gap, same_owner=same,
        scope='General all-length routing and owner-only pruning proofs written separately. All seven single-square matchings, original identities and costs retained. Existing frozen same-owner tile is a counterexample to a tile-to-capacity-two-relay adapter in a declared restricted certificate, not a full-board or grid target counterexample. No new Oracle/mail/manuscript change. Lean scope separate.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', **dict(counts))))


if __name__ == '__main__':
    main()
