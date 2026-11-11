#!/usr/bin/env python3
"""Literal and unrestricted controls for clean-witness port compositions."""
from functools import lru_cache
from itertools import combinations
import json
from pathlib import Path
import sys

if not __debug__:
    raise RuntimeError('Assertions must be enabled; do not use -O.')


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def mask(vertices):
    return sum(1 << v for v in vertices)


BASE_EDGES = [(0, 1), (0, 2), (1, 4), (2, 5), (3, 5),
              (6, 7), (6, 8), (7, 10), (8, 11), (9, 11),
              (4, 10), (4, 11), (5, 10), (5, 11)]
BASE_S = mask([0, 1, 2, 3, 6, 7, 8, 9])
BASE_LEFT = {0, 4, 5, 7, 8, 9}
D8 = mask([0, 2, 3, 4, 6, 8, 9, 10])
D7 = mask([0, 1, 3, 5, 7, 8, 9])
PORTS = (1 << 4) | (1 << 10)


def construct(r, arcs):
    adj = [0] * (12 * r)
    seen = set()

    def edge(u, v):
        assert u != v and not (adj[u] >> v & 1)
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    for j in range(r):
        for u, v in BASE_EDGES:
            edge(12 * j + u, 12 * j + v)
    for j, k in arcs:
        assert 0 <= j < r and 0 <= k < r and j != k
        pair = tuple(sorted([j, k]))
        assert pair not in seen
        seen.add(pair)
        edge(12 * j + 4, 12 * k + 10)
    return adj


def dissociation(adj, chosen):
    return all((adj[v] & chosen).bit_count() <= 1 for v in bits(chosen))


def formed_local(adj, chosen, v):
    neighbours = adj[v] & chosen
    return neighbours.bit_count() >= 2 or any(adj[u] & chosen for u in bits(neighbours))


def formed_literal(adj, chosen, v):
    for u, w in combinations(bits(chosen), 2):
        if ((adj[v] >> u) & 1) + ((adj[v] >> w) & 1) + ((adj[u] >> w) & 1) >= 2:
            return True
    return False


def exact_beta(adj):
    calls = 0

    @lru_cache(None)
    def visit(allowed):
        nonlocal calls
        calls += 1
        if not allowed:
            return 0
        first = allowed & -allowed
        reached = frontier = first
        while frontier:
            fresh = 0
            for u in bits(frontier):
                fresh |= adj[u] & allowed
            frontier = fresh & ~reached
            reached |= frontier
        if reached != allowed:
            return visit(reached) | visit(allowed ^ reached)
        v = max(bits(allowed), key=lambda u: (adj[u] & allowed).bit_count())
        neighbours = adj[v] & allowed
        if neighbours.bit_count() <= 1:
            return allowed
        choices = [visit(allowed & ~(1 << v)),
                   (1 << v) | visit(allowed & ~(neighbours | (1 << v)))]
        for u in bits(neighbours):
            choices.append((1 << v) | (1 << u) |
                           visit(allowed & ~(adj[v] | adj[u] | (1 << u) | (1 << v))))
        return max(choices, key=lambda chosen: (chosen.bit_count(), chosen))

    D = visit((1 << len(adj)) - 1)
    assert dissociation(adj, D)
    return D.bit_count(), calls


def one_part_beta(adj):
    left = [12 * j + v for j in range(len(adj) // 12) for v in sorted(BASE_LEFT)]
    right = sorted(set(range(len(adj))) - set(left))
    best = 0
    for subset in range(1 << len(left)):
        chosen = mask(left[i] for i in bits(subset))
        isolated = 0
        owners = set()
        for v in right:
            neighbours = adj[v] & chosen
            if not neighbours:
                isolated += 1
            elif neighbours.bit_count() == 1:
                owners.add(neighbours)
        best = max(best, chosen.bit_count() + isolated + len(owners))
    return best, 1 << len(left)


def independent(r, arcs, chosen):
    return all(not (chosen >> j & 1 and chosen >> k & 1) for j, k in arcs)


def alpha_literal(r, arcs):
    return max((chosen for chosen in range(1 << r) if independent(r, arcs, chosen)),
               key=lambda chosen: (chosen.bit_count(), chosen))


def check(r, arcs, J=None, exact=False, literal=False, one_part=False):
    adj = construct(r, arcs)
    if J is None:
        J = alpha_literal(r, arcs)
    assert independent(r, arcs, J) and not (J >> r)
    n = len(adj)
    S = sum(BASE_S << (12 * j) for j in range(r))
    D = sum((D8 if J >> j & 1 else D7) << (12 * j) for j in range(r))
    expected = 7 * r + J.bit_count()
    assert S.bit_count() == 8 * r and D.bit_count() == expected and dissociation(adj, D)
    left = mask(12 * j + v for j in range(r) for v in BASE_LEFT)
    assert all(not (adj[v] & (left if left >> v & 1 else ((1 << n) - 1) ^ left)) for v in range(n))
    assert sum(row.bit_count() for row in adj) // 2 == 14 * r + len(arcs)
    outdegrees = [sum(j == v for j, k in arcs) for v in range(r)]
    indegrees = [sum(k == v for j, k in arcs) for v in range(r)]
    degree = max([row.bit_count() for row in adj], default=0)
    assert degree == (max(4, 3 + max(outdegrees), 3 + max(indegrees)) if r else 0)
    deletion_checks = literal_checks = 0
    for j in range(r):
        block = [row >> (12 * j) & ((1 << 12) - 1) for row in adj[12*j:12*j+12]]
        assert block == construct(1, [])
        for half in range(2):
            x, l, h, p, u, v = range(12 * j + 6 * half, 12 * j + 6 * half + 6)
            assert adj[u] & S == 1 << l
            assert adj[v] & S == (1 << h) | (1 << p)
            for deleted, failure in [(x, u), (l, u), (h, v), (p, p)]:
                assert not formed_local(adj, S ^ (1 << deleted), failure)
                deletion_checks += 1
                if literal:
                    assert not formed_literal(adj, S ^ (1 << deleted), failure)
                    literal_checks += 1
        for outside in [12*j+4, 12*j+5, 12*j+10, 12*j+11]:
            assert formed_local(adj, S, outside)
            if literal:
                assert formed_literal(adj, S, outside)
                literal_checks += 1
    result = {'r': r, 'arcs': [list(edge) for edge in arcs], 'order': n,
              'edges': 14 * r + len(arcs), 'maximum_degree': degree,
              'independent_interface_set': list(bits(J)), 'alpha_certificate': J.bit_count(),
              'minimal_selected_size': S.bit_count(), 'beta_certificate': expected,
              'selected_deficit': r - J.bit_count(), 'deletion_failures': deletion_checks,
              'literal_star_checks': literal_checks}
    if exact:
        value, calls = exact_beta(adj)
        assert value == expected
        result.update({'exact_unrestricted_beta': value, 'recursion_states': calls})
    if one_part:
        value, count = one_part_beta(adj)
        assert value == expected
        result['independent_one_part_subsets'] = count
    return result


def main():
    base = construct(1, [])
    all_valid = [chosen for chosen in range(1 << 12) if dissociation(base, chosen)]
    assert max(chosen.bit_count() for chosen in all_valid) == 8
    eight_sets = [chosen for chosen in all_valid if chosen.bit_count() == 8]
    assert all(chosen & PORTS == PORTS for chosen in eight_sets)
    assert dissociation(base, D8) and dissociation(base, D7) and not (D7 & PORTS)
    formation_checks = 0
    for chosen in range(1 << 12):
        for v in bits(((1 << 12) - 1) ^ chosen):
            assert formed_local(base, chosen, v) == formed_literal(base, chosen, v)
            formation_checks += 1
    small = []
    for r in range(5):
        edges = list(combinations(range(r), 2))
        for encoded in range(1 << len(edges)):
            arcs = [edge for i, edge in enumerate(edges) if encoded >> i & 1]
            small.append(check(r, arcs, exact=True, literal=True,
                               one_part=r <= 2 or (r == 3 and len(arcs) == 3)))
    orientations = []
    for encoded in range(8):
        arcs = [(u, v) if encoded >> i & 1 else (v, u)
                for i, (u, v) in enumerate(combinations(range(3), 2))]
        orientations.append(check(3, arcs, exact=True, literal=True))
    large = []
    for r in [1, 2, 3, 4, 8, 16, 64, 128]:
        arcs = [(j, j + 1) for j in range(r - 1)]
        J = mask(range(0, r, 2))
        assert J.bit_count() == (r + 1) // 2
        large.append({'family': 'path', **check(r, arcs, J=J)})
        if r >= 3:
            arcs = [(j, (j + 1) % r) for j in range(r)]
            J = mask(range(0, r - (r % 2), 2))
            assert J.bit_count() == r // 2
            large.append({'family': 'cycle', **check(r, arcs, J=J)})
        arcs = list(combinations(range(r), 2))
        large.append({'family': 'complete', **check(r, arcs, J=1)})
    report = {'status': 'PASS', 'scope': 'finite controls of the written all-interface theorem',
              'block_full_subsets': 4096, 'block_valid_eight_sets': len(eight_sets),
              'block_literal_local_comparisons': formation_checks,
              'small_all_interface_graphs': small, 'triangle_orientations': orientations,
              'large_families': large,
              'totals': {'exact_unrestricted_instances': len(small) + len(orientations),
                         'all_labelled_interface_graphs_orders_zero_through_four': len(small),
                         'triangle_orientations': len(orientations),
                         'independent_one_part_subsets': sum(x.get('independent_one_part_subsets', 0) for x in small),
                         'deletion_failures': sum(x['deletion_failures'] for x in small + orientations + large),
                         'literal_star_checks': sum(x['literal_star_checks'] for x in small + orientations),
                         'maximum_order': max(x['order'] for x in large)}}
    output = Path(__file__).resolve().parents[1] / 'output/selected-star-ports-check.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report['totals'], sort_keys=True))


if __name__ == '__main__':
    main()
