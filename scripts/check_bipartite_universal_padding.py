#!/usr/bin/env python3
"""Independent finite controls for the universal bipartite padding theorem.

Standard library only. General parameter conclusions use the written proof.
The exact solver enumerates one part; small optima also use every full subset.
"""
from collections import deque
from itertools import combinations
import hashlib
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def mask_of(vertices):
    return sum(1 << v for v in vertices)


def add(adj, u, v):
    assert u != v and not (adj[u] >> v & 1)
    adj[u] |= 1 << v
    adj[v] |= 1 << u


def padded(adj, left, t):
    n = len(adj)
    out = list(adj) + [0] * (2 * t)
    X, Y = set(range(n, n + t)), set(range(n + t, n + 2 * t))
    right = set(range(n)) - left
    for x in sorted(X):
        for v in sorted(right | Y):
            add(out, x, v)
    for y in sorted(Y):
        for v in sorted(left):
            add(out, y, v)
    return out, left | X, X, Y


def diss(adj, D):
    return all((adj[v] & D).bit_count() <= 1 for v in bits(D))


def one_part_beta(adj, left):
    """For each left set, choose all zero-neighbours and one per sole owner."""
    left = sorted(left)
    right = sorted(set(range(len(adj))) - set(left))
    best, witness = 0, 0
    for local in range(1 << len(left)):
        chosen = mask_of(left[i] for i in bits(local))
        zero, owners = 0, {}
        for v in right:
            neighbours = adj[v] & chosen
            if not neighbours:
                zero |= 1 << v
            elif neighbours.bit_count() == 1:
                owners.setdefault(neighbours, v)
        D = chosen | zero | mask_of(owners.values())
        size = D.bit_count()
        if size > best:
            best, witness = size, D
    assert diss(adj, witness)
    return best, witness, 1 << len(left)


def literal_beta(adj):
    return max(D.bit_count() for D in range(1 << len(adj)) if diss(adj, D))


def formed(adj, S, v):
    """Literal non-induced stars on one outside and two selected vertices."""
    for u, w in combinations(bits(S), 2):
        if ((adj[v] >> u & 1) + (adj[v] >> w & 1)
                + (adj[u] >> w & 1)) >= 2:
            return True
    return False


def forming(adj, S):
    return all(formed(adj, S, v) for v in bits(((1 << len(adj)) - 1) ^ S))


def minimal(adj, S):
    return forming(adj, S) and all(not forming(adj, S ^ (1 << v)) for v in bits(S))


def small_graphs():
    graphs = no_isolate_graphs = exact = full_subsets = eligible = 0
    digest = hashlib.sha256()
    for a in range(1, 4):
        for b in range(1, 4):
            edges = [(u, a + v) for u in range(a) for v in range(b)]
            for edge_mask in range(1 << len(edges)):
                adj = [0] * (a + b)
                for i, (u, v) in enumerate(edges):
                    if edge_mask >> i & 1:
                        add(adj, u, v)
                left = set(range(a))
                beta, _, _ = one_part_beta(adj, left)
                assert beta == literal_beta(adj)
                graphs += 1
                no_isolate_graphs += int(all(adj))
                full_subsets += 1 << len(adj)
                selections = [S for S in range(1 << len(adj))
                              if (S & mask_of(left)).bit_count() >= 2
                              and (S & (((1 << len(adj)) - 1) ^ mask_of(left))).bit_count() >= 2
                              and minimal(adj, S)]
                eligible += len(selections)
                for t in (1, 2):
                    out, out_left, _, _ = padded(adj, left, t)
                    actual, _, _ = one_part_beta(out, out_left)
                    delta_A = min(adj[v].bit_count() for v in range(a))
                    delta_B = min(adj[v].bit_count() for v in range(a, a + b))
                    expected = max(beta, a + t, b + t, a - delta_B + 2, b - delta_A + 2)
                    assert actual == expected == literal_beta(out)
                    if all(adj) or t >= 2:
                        assert actual == max(beta, a + t, b + t)
                    exact += 1
                    full_subsets += 1 << len(out)
                    digest.update(bytes((a, b, t, actual)))
                    for S in selections:
                        assert minimal(out, S)
    assert eligible > 0
    # The no-isolate assumption is necessary for the stated t=1 formula.
    out, left, _, _ = padded([0, 0], {0}, 1)
    actual, witness, _ = one_part_beta(out, left)
    assert actual == literal_beta(out) == 3
    assert max(literal_beta([0, 0]), 2, 2) == 2
    return {'all_bipartite_graphs': graphs, 'no_isolate_graphs': no_isolate_graphs,
            'padded_exact_optima': exact,
            'full_subsets': full_subsets, 'eligible_old_minimal_selections': eligible,
            'literal_padding_minimality_checks': 2 * eligible,
            'optimum_sequence_sha256': digest.hexdigest(),
            'isolate_counterexample': {'old_order': 2, 't': 1, 'actual_beta': actual,
                                       'formula_without_hypothesis': 2,
                                       'attaining_set': list(bits(witness))}}


def base(r):
    adj = [0] * (12 * r)
    left = set()
    S = 0
    for i in range(2 * r):
        c, l, m, z, p, h = range(6 * i, 6 * i + 6)
        for u, v in ((c, l), (c, m), (l, p), (m, h), (z, h)):
            add(adj, u, v)
        left.update((c, p, h) if i < r else (l, m, z))
        S |= mask_of((c, l, m, z))
    for i in range(r):
        for j in range(r, 2 * r):
            for u in (6 * i + 4, 6 * i + 5):
                for v in (6 * j + 4, 6 * j + 5):
                    add(adj, u, v)
    D = mask_of(6 * i + k for i in range(2 * r)
                for k in ((0, 3, 4, 5) if i < r else (1, 2, 3)))
    assert diss(adj, D) and D.bit_count() == 7 * r
    return adj, left, S, D


def connected(adj, deleted):
    remaining = ((1 << len(adj)) - 1) ^ deleted
    if not remaining:
        return True
    reached = remaining & -remaining
    frontier = reached
    while frontier:
        fresh = 0
        for v in bits(frontier):
            fresh |= adj[v]
        frontier = fresh & remaining & ~reached
        reached |= frontier
    return reached == remaining


def vertex_paths(adj, source, target, limit):
    """Integral vertex-split flow, stopped at the required lower bound."""
    n = len(adj)
    cap = [dict() for _ in range(2 * n)]

    def arc(u, v, amount):
        cap[u][v] = amount
        cap[v].setdefault(u, 0)

    for v in range(n):
        arc(2 * v, 2 * v + 1, n if v in (source, target) else 1)
        for w in bits(adj[v]):
            arc(2 * v + 1, 2 * w, n)
    start, end, flow = 2 * source + 1, 2 * target, 0
    while flow < limit:
        parent = {start: None}
        queue = deque([start])
        while queue and end not in parent:
            v = queue.popleft()
            for w, available in cap[v].items():
                if available and w not in parent:
                    parent[w] = v
                    queue.append(w)
        if end not in parent:
            return flow
        amount, v = limit - flow, end
        while parent[v] is not None:
            amount = min(amount, cap[parent[v]][v])
            v = parent[v]
        v = end
        while parent[v] is not None:
            u = parent[v]
            cap[u][v] -= amount
            cap[v][u] += amount
            v = u
        flow += amount
    return flow


def family(r, t, exact=False, physical_connectivity=False):
    adj, left, S, old_D = base(r)
    adj, left, X, Y = padded(adj, left, t)
    n = len(adj)
    beta = max(7 * r, 6 * r + t)
    D = old_D if 7 * r >= 6 * r + t else mask_of(left)
    assert n == 12 * r + 2 * t and len(left) == n // 2
    assert S.bit_count() == 8 * r and diss(adj, D) and D.bit_count() == beta
    assert S.bit_count() - beta == min(r, 2 * r - t)
    assert min(row.bit_count() for row in adj) == t + 1
    assert max(row.bit_count() for row in adj) == 6 * r + t
    assert connected(adj, 0)
    left_mask = mask_of(left)
    assert all(not (adj[v] & (left_mask if v in left else ((1 << n) - 1) ^ left_mask))
               for v in range(n))
    # Selected graph is exactly 2r P3 and 2r isolated vertices.
    for i in range(2 * r):
        c, l, m, z, p, h = range(6 * i, 6 * i + 6)
        assert adj[c] & S == mask_of((l, m))
        assert adj[l] & S == adj[m] & S == 1 << c
        assert not (adj[z] & S)
        for deleted, failure in ((c, p), (l, p), (m, h), (z, z)):
            assert not formed(adj, S ^ (1 << deleted), failure)
    assert forming(adj, S)
    # An explicit cut of size t+1 at an old pendant vertex.
    cut = adj[3]
    assert cut.bit_count() == t + 1 and not connected(adj, cut)
    result = {'r': r, 't': t, 'order': n, 'selected': S.bit_count(),
              'beta_from_general_theorem': beta, 'selected_gap': S.bit_count() - beta,
              'min_degree': t + 1, 'max_degree': 6 * r + t,
              'connectivity_from_general_proof': t + 1,
              'explicit_cut': list(bits(cut)), 'deletion_failures': 8 * r,
              'selected_components': {'P3': 2 * r, 'isolates': 2 * r, 'edges': 0}}
    if exact:
        value, witness, count = one_part_beta(adj, left)
        assert value == beta
        result.update({'independent_exact_beta': value, 'one_part_subsets': count,
                       'exact_attaining_set': list(bits(witness))})
    if physical_connectivity:
        pairs = 0
        for u, v in combinations(range(n), 2):
            if not (adj[u] >> v & 1):
                assert vertex_paths(adj, u, v, t + 1) == t + 1
                pairs += 1
        result['all_nonadjacent_pair_vertex_flow_checks'] = pairs
    if t == r:
        assert 2 * beta == n
        assert 4 * beta == 28 * r < 30 * r == 2 * S.bit_count() + n
        result['strengthening_counterexample'] = {'lhs': 28 * r, 'rhs': 30 * r}
    return result


def main():
    small = small_graphs()
    physical = [family(2, t, exact=True, physical_connectivity=True) for t in range(1, 5)]
    physical += [family(3, t, exact=True, physical_connectivity=True) for t in (1, 3)]
    larger = [family(r, t) for r, t in ((4, 1), (4, 4), (8, 2), (8, 8), (16, 3), (32, 32))]
    report = {'status': 'PASS', 'scope': 'Finite controls; all-parameter conclusions use the complete written proofs.',
              'small_bipartite_graphs': small, 'exact_family_controls': physical,
              'larger_certificate_controls': larger,
              'totals': {'exact_padded_small_graphs': small['padded_exact_optima'],
                         'literal_full_subsets': small['full_subsets'],
                         'family_exact_optima': len(physical),
                         'family_one_part_subsets': sum(x['one_part_subsets'] for x in physical),
                         'nonadjacent_pair_vertex_flows': sum(x['all_nonadjacent_pair_vertex_flow_checks'] for x in physical),
                         'family_deletion_failures': sum(x['deletion_failures'] for x in physical + larger),
                         'maximum_order': max(x['order'] for x in physical + larger)}}
    out = Path(__file__).resolve().parents[1] / 'output/bipartite-universal-padding-check.json'
    out.parent.mkdir(exist_ok=True)
    out.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': 'PASS', **report['totals']}, sort_keys=True))


if __name__ == '__main__':
    main()
