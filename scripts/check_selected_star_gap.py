#!/usr/bin/env python3
"""Independent finite controls for SELECTED_STAR_COMPONENT_GAPS.md."""
from functools import lru_cache
from itertools import combinations, product
import json
from pathlib import Path
import sys

if not __debug__:
    raise RuntimeError('Run with assertions enabled, without -O.')


def bits(mask):
    while mask:
        bit = mask & -mask
        yield bit.bit_length() - 1
        mask ^= bit


def graph(a, b):
    assert a >= 1 and b >= 1
    n = 6 * (a + b)
    adj = [0] * n
    left = set()

    def add(u, v):
        assert u != v and not (adj[u] >> v & 1)
        adj[u] |= 1 << v
        adj[v] |= 1 << u

    for i in range(a + b):
        x, l, h, p, u, v = range(6 * i, 6 * i + 6)
        for first, second in [(x, l), (x, h), (l, u), (h, v), (p, v)]:
            add(first, second)
        left.update([x, u, v] if i < a else [l, h, p])
    for i in range(a):
        for j in range(a, a + b):
            for u in [6 * i + 4, 6 * i + 5]:
                for v in [6 * j + 4, 6 * j + 5]:
                    add(u, v)
    return adj, left


def mask_of(vertices):
    return sum(1 << v for v in vertices)


def dissociation(adj, chosen):
    return all((adj[v] & chosen).bit_count() <= 1 for v in bits(chosen))


def formed_local(adj, chosen, v):
    neighbours = adj[v] & chosen
    return neighbours.bit_count() >= 2 or any(adj[u] & chosen for u in bits(neighbours))


def formed_literal(adj, chosen, v):
    """Enumerate triples and count their actual edges, without the local test."""
    for u, w in combinations(bits(chosen), 2):
        edges = ((adj[v] >> u) & 1) + ((adj[v] >> w) & 1) + ((adj[u] >> w) & 1)
        if edges >= 2:
            return True
    return False


def exact_beta(adj):
    """Unrestricted isolated/paired/excluded-vertex recurrence with a witness."""
    calls = 0

    @lru_cache(None)
    def visit(allowed):
        nonlocal calls
        calls += 1
        if not allowed:
            return 0
        v = max(bits(allowed), key=lambda u: (adj[u] & allowed).bit_count())
        neighbours = adj[v] & allowed
        if neighbours.bit_count() <= 1:
            return allowed
        options = [visit(allowed & ~(1 << v)),
                   (1 << v) | visit(allowed & ~(neighbours | (1 << v)))]
        for u in bits(neighbours):
            rest = allowed & ~(adj[u] | adj[v] | (1 << u) | (1 << v))
            options.append((1 << u) | (1 << v) | visit(rest))
        return max(options, key=lambda item: (item.bit_count(), item))

    witness = visit((1 << len(adj)) - 1)
    assert dissociation(adj, witness)
    return witness.bit_count(), calls, witness


def one_part_beta(adj, left):
    """Enumerate one part and optimize actual degree-one choices in the other."""
    left = sorted(left)
    right = sorted(set(range(len(adj))) - set(left))
    best = 0
    for local in range(1 << len(left)):
        chosen = mask_of(left[i] for i in bits(local))
        no_neighbour = 0
        owners = set()
        for w in right:
            neighbours = adj[w] & chosen
            if not neighbours:
                no_neighbour += 1
            elif neighbours.bit_count() == 1:
                owners.add(neighbours)
        best = max(best, chosen.bit_count() + no_neighbour + len(owners))
    return best, 1 << len(left)


def literal_beta(adj, leaves):
    best = restricted = 0
    for chosen in range(1 << len(adj)):
        size = chosen.bit_count()
        keeps_leaves = chosen & leaves == leaves
        if (size > best or (keeps_leaves and size > restricted)) and dissociation(adj, chosen):
            best = max(best, size)
            if keeps_leaves:
                restricted = max(restricted, size)
    return best, restricted, 1 << len(adj)


def local_tables():
    """Independent enumeration supplies every block bound used in the proof."""
    adj = [0] * 6
    for u, v in [(0, 1), (0, 2), (1, 4), (2, 5), (3, 5)]:
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    result = {}
    for fixed in [0, 1 << 4, 1 << 5, (1 << 4) | (1 << 5)]:
        valid = [fixed | chosen for chosen in range(16) if dissociation(adj, fixed | chosen)]
        result[str(fixed)] = max(chosen.bit_count() for chosen in valid)
    assert result == {'0': 3, '16': 4, '32': 4, '48': 4}
    for witness, expected in [(4, 4), (5, 3)]:
        valid = [(1 << witness) | chosen for chosen in range(16)
                 if not (adj[witness] & chosen)
                 and dissociation(adj, (1 << witness) | chosen)]
        actual = max(chosen.bit_count() for chosen in valid)
        assert actual == expected
        result['cross_paired_' + str(witness)] = actual
    return result


def check(a, b, literal=False, recursive=False, one_part=False, full=False):
    adj, left = graph(a, b)
    c, n = a + b, len(adj)
    all_vertices = set(range(n))
    S = mask_of(6 * i + k for i in range(c) for k in range(4))
    leaves = mask_of(6 * i + k for i in range(c) for k in [1, 2])
    W = ((1 << n) - 1) ^ S
    assert n == 6 * c and len(left) == n // 2
    assert sum(row.bit_count() for row in adj) // 2 == 5 * c + 4 * a * b
    assert max(row.bit_count() for row in adj) == 2 * max(a, b) + 2
    assert all(not (adj[v] & mask_of(left if v in left else all_vertices - left))
               for v in range(n))
    reached, frontier = {0}, {0}
    while frontier:
        fresh = set().union(*(set(bits(adj[v])) for v in frontier)) - reached
        reached |= fresh
        frontier = fresh
    assert len(reached) == n
    assert all(formed_local(adj, S, v) for v in bits(W))
    deletion_checks = witness_checks = literal_checks = 0
    for i in range(c):
        x, l, h, p, u, v = range(6 * i, 6 * i + 6)
        assert adj[x] & S == (1 << l) | (1 << h)
        assert adj[l] & S == adj[h] & S == 1 << x
        assert not (adj[p] & S)
        assert adj[u] & S == 1 << l
        assert adj[v] & S == (1 << h) | (1 << p)
        assert adj[u] & S == 1 << l  # clean leaf at every centre
        for deleted, failure in [(x, u), (l, u), (h, v), (p, p)]:
            smaller = S ^ (1 << deleted)
            assert not (smaller >> failure & 1)
            assert not formed_local(adj, smaller, failure)
            deletion_checks += 1
            if literal:
                assert not formed_literal(adj, smaller, failure)
                for outside in bits(((1 << n) - 1) ^ smaller):
                    assert formed_local(adj, smaller, outside) == formed_literal(adj, smaller, outside)
                    literal_checks += 1
        for leaf, owner in [(l, u), (h, v)]:
            failures = [z for z in bits(W) if not formed_local(adj, S ^ (1 << leaf), z)]
            assert failures == [owner]
            witness_checks += 1

    D_A, D_B = set(), set()
    for i in range(c):
        x, l, h, p, u, v = range(6 * i, 6 * i + 6)
        D_A.update([x, p, u, v] if i < a else [l, h, p])
        D_B.update([l, h, p] if i < a else [x, p, u, v])
    D_pair = set()
    for i in range(c):
        x, l, h, p, u, v = range(6 * i, 6 * i + 6)
        D_pair.update([x, h, p, u] if i in [0, a] else [l, h, p])
        for path in [(x, l, u), (p, v, h)]:
            assert sum((adj[z] & mask_of(path)).bit_count() for z in path) // 2 == 2
    for chosen, expected in [(D_A, 4 * a + 3 * b), (D_B, 3 * a + 4 * b), (D_pair, 3 * c + 2)]:
        assert len(chosen) == expected and dissociation(adj, mask_of(chosen))
    beta = 3 * c + max(a, b, 2)
    assert max(len(D_A), len(D_B), len(D_pair)) == beta
    # Exact forced-witness Q matching saturates its smaller bipartition.
    Q_vertices = set(bits(W)) | {6 * i + 3 for i in range(c)}
    matching = [(6 * i + 5, 6 * i + 3) for i in range(c)]
    matching += [(6 * i + 4, 6 * (a + i) + 4) for i in range(min(a, b))]
    ends = [v for edge in matching for v in edge]
    assert len(ends) == len(set(ends))
    assert all(u in Q_vertices and v in Q_vertices and adj[u] >> v & 1 for u, v in matching)
    assert len(matching) == min(len(Q_vertices & left), len(Q_vertices - left)) == c + min(a, b)
    leaf_optimum = 4 * c - min(a, b)
    delta = S.bit_count() - beta
    assert delta >= 0 and 12 * delta <= n
    if a == b and a >= 2:
        assert beta == 7 * a and S.bit_count() == 8 * a and 12 * delta == n
    result = {'a': a, 'b': b, 'order': n, 'edges': 5 * c + 4 * a * b,
              'maximum_degree': 2 * max(a, b) + 2, 'minimal_selected_size': S.bit_count(),
              'beta_certificate': beta, 'true_deficit': delta,
              'leaf_retaining_optimum': leaf_optimum,
              'deletion_failures_checked': deletion_checks,
              'unique_leaf_witnesses_checked': witness_checks,
              'literal_local_comparisons': literal_checks}
    if recursive:
        exact, calls, witness = exact_beta(adj)
        assert exact == beta
        result.update({'unrestricted_exact_beta': exact, 'recursion_states': calls,
                       'exact_attaining_set': list(bits(witness))})
    if one_part:
        exact, count = one_part_beta(adj, left)
        assert exact == beta
        result['one_part_subsets'] = count
    if full:
        exact, restricted, count = literal_beta(adj, leaves)
        assert exact == beta and restricted == leaf_optimum
        result['literal_full_subsets'] = count
        result['literal_leaf_retaining_optimum'] = restricted
    if (a, b) == (1, 2):
        result['explicit_certificate'] = {
            'names_by_index': [str(i + 1) + ':' + name for i in range(c)
                               for name in ['x', 'l', 'h', 'p', 'u', 'v']],
            'edges': [[u, v] for u in range(n) for v in bits(adj[u]) if u < v],
            'bipartition_left': sorted(left), 'minimal_selection': list(bits(S)),
            'attaining_dissociation': sorted(D_B),
            'all_four_case_upper_bounds': [3 * c, 4 * a + 3 * b, 3 * a + 4 * b, 3 * c + 2]}
    return result


def bounded_degree_chain(r):
    base, base_left = graph(2, 2)
    n = 24 * r
    adj = [row << (24 * j) for j in range(r) for row in base]
    left = set()
    S = D = 0
    for j in range(r):
        left.update(24 * j + v for v in (base_left if j % 2 == 0 else set(range(24)) - base_left))
        S |= mask_of(24 * j + 6 * i + k for i in range(4) for k in range(4))
        D |= mask_of(24 * j + 6 * i + k for i in range(4)
                     for k in ([0, 3, 4, 5] if i < 2 else [1, 2, 3]))
    joins = [(24 * j + 22, 24 * (j + 1) + 16) for j in range(r - 1)]
    for u, v in joins:
        assert not (D >> u & 1) and not (D >> v & 1)
        assert (u in left) != (v in left)
        adj[u] |= 1 << v
        adj[v] |= 1 << u
    assert sum(row.bit_count() for row in adj) // 2 == 37 * r - 1
    assert max(row.bit_count() for row in adj) == 6
    assert S.bit_count() == 16 * r and D.bit_count() == 14 * r and dissociation(adj, D)
    assert 12 * (S.bit_count() - D.bit_count()) == n
    assert all(formed_local(adj, S, v) for v in bits(((1 << n) - 1) ^ S))
    for j in range(r):
        assert [row >> (24 * j) & ((1 << 24) - 1) for row in adj[24*j:24*j+24]] == base
        for i in range(4):
            x, l, h, p, u, v = range(24 * j + 6 * i, 24 * j + 6 * i + 6)
            assert adj[u] & S == 1 << l
            for deleted, failure in [(x, u), (l, u), (h, v), (p, p)]:
                assert not formed_local(adj, S ^ (1 << deleted), failure)
    result = {'r': r, 'order': n, 'edges': 37 * r - 1, 'maximum_degree': 6,
              'minimal_selected_size': S.bit_count(), 'beta_certificate': D.bit_count(),
              'deletion_failures_checked': 16 * r, 'clean_leaf_witnesses': 4 * r,
              'new_edges_all_omitted_in_attaining_set': True,
              'each_induced_base_block_verified': True}
    if r <= 2:
        exact, calls, witness = exact_beta(adj)
        assert exact == 14 * r
        result.update({'unrestricted_exact_beta': exact, 'recursion_states': calls})
    return result


def sharp_arithmetic():
    """Check all bounded integer inputs of the general clean-leaf proof."""
    checks = 0
    for c in range(21):
        for e in range(2 * c, 4 * c + 5):
            for t in range(e - c + 1):
                bound = c - ((e - t + 1) // 2)
                for d in range(1, bound + 1):
                    n = c + 2 * e + t
                    assert 2 * d <= 2 * c - e + t <= c
                    assert n >= 3 * e - c + 2 * d >= 5 * c + 2 * d >= 12 * d
                    checks += 1
    return checks


def main():
    tables = local_tables()
    small = [check(a, b, literal=True, recursive=True, one_part=a+b <= 5,
                   full=(a, b) in [(1, 1), (1, 2), (2, 1)])
             for a, b in product(range(1, 5), repeat=2)]
    large_pairs = [(r, r) for r in [1, 2, 3, 4, 8, 16, 64, 128]]
    large_pairs += [(1, 16), (16, 1), (2, 64), (64, 2)]
    large = [check(a, b) for a, b in large_pairs]
    chains = [bounded_degree_chain(r) for r in [1, 2, 3, 4, 8, 16, 64, 128]]
    report = {'status': 'PASS', 'scope': 'finite controls; all-parameter conclusions use the written proofs',
              'block_upper_bound_tables': tables, 'small_independent_controls': small,
              'large_certificate_controls': large, 'bounded_degree_chains': chains,
              'sharp_bound_arithmetic_controls': sharp_arithmetic(),
              'totals': {
                  'exact_unrestricted_instances': len(small) + sum('unrestricted_exact_beta' in item for item in chains),
                  'literal_full_subsets': sum(item.get('literal_full_subsets', 0) for item in small),
                  'one_part_subsets': sum(item.get('one_part_subsets', 0) for item in small),
                  'literal_local_comparisons': sum(item['literal_local_comparisons'] for item in small),
                  'deletion_failures': sum(item['deletion_failures_checked'] for item in small + large + chains),
                  'unique_leaf_witnesses': sum(item['unique_leaf_witnesses_checked'] for item in small + large),
                  'maximum_order': max(item['order'] for item in small + large + chains)}}
    output = Path(__file__).resolve().parents[1] / 'output/selected-star-gap-check.json'
    output.parent.mkdir(exist_ok=True)
    output.write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'status': report['status'], **report['totals']}, sort_keys=True))


if __name__ == '__main__':
    main()
