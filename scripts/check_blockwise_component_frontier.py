"""Independent literal costs for block-rank frontiers and P2 tractability."""
from pathlib import Path
from functools import lru_cache
from itertools import combinations, permutations
from collections import Counter
import argparse, hashlib, json, random, sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'develop'))
from blockwise_component_frontier import blockwise_frontier
from primary_exchange_hardness import charged_vertex_cover_template
if not __debug__:
    raise RuntimeError('Assertions required')
counts, digest, rng = Counter(), hashlib.sha256(), random.Random(13112698)


def literal_cost(n, E, U):
    adjacency = [0]*n
    for a, b in E:
        adjacency[a] |= 1 << b
        adjacency[b] |= 1 << a
    @lru_cache(None)
    def solve(mask):
        if not mask:
            return 0
        bit = mask & -mask
        v = bit.bit_length()-1
        left = mask ^ bit
        best = solve(left)
        neighbours = adjacency[v] & left
        while neighbours:
            w = neighbours & -neighbours
            neighbours ^= w
            best = max(best, 1+solve(left ^ w))
        return best
    return solve(sum(1 << v for v in U))


def check(n, E, U, operations, p2=False):
    result = blockwise_frontier(n, E, U, operations)
    if p2:
        assert result['maximum_block_cycle_rank'] <= 1
        counts['matching_ambient_models'] += 1
    expected = {}
    for mask in range(1 << len(operations)):
        S = [i for i in range(len(operations)) if mask >> i & 1]
        final = (set(U)-{operations[i][0] for i in S}) | {operations[i][1] for i in S}
        value = (literal_cost(n, E, final), mask)
        t = len(S)
        if t not in expected or value < expected[t]:
            expected[t] = value
        counts['literal_batch_comparisons'] += 1
    assert [(r['cost'], r['selected_mask']) for r in result['frontier']] == [expected[t] for t in range(len(operations)+1)]
    cert = result['certificate']; final = set(cert['U']); cover = set(cert['cover']); matching = cert['matching']
    EE = {tuple(sorted(e)) for e in E}
    assert len(cover) == len(matching) == cert['actual_cost'] == result['best']['cost']
    assert len({v for e in matching for v in e}) == 2*len(matching)
    assert all(tuple(sorted(e)) in EE and set(e) <= final for e in matching)
    assert all(a in cover or b in cover for a, b in E if a in final and b in final)
    counts['exact_frontiers'] += 1
    counts['exact_budget_rows'] += len(result['frontier'])
    digest.update(json.dumps([n, E, sorted(U), operations, result['frontier']], sort_keys=True).encode())
    return result


# Every graph through4 restricted to maxdegree1, every U and candidate injection.
for n in range(5):
    possible = list(combinations(range(n), 2))
    for edge_mask in range(1 << len(possible)):
        E = [e for i, e in enumerate(possible) if edge_mask >> i & 1]
        degree = Counter(v for e in E for v in e)
        if max(degree.values(), default=0) > 1:
            continue
        for mask in range(1 << n):
            U = {v for v in range(n) if mask >> v & 1}
            outside = sorted(set(range(n))-U)
            for q in range(min(len(U), len(outside))+1):
                for X in combinations(sorted(U), q):
                    for Y in permutations(outside, q):
                        check(n, E, U, list(zip(X, Y)), p2=True)
        counts['all_small_matching_graphs'] += 1

# Arbitrary path/even-cycle mixtures, including nontrivial component cycle ranks.
for trial in range(280):
    n = rng.randrange(1, 17)
    vertices = list(range(n)); rng.shuffle(vertices)
    E, offset = [], 0
    while offset < n:
        size = rng.randrange(1, min(n-offset, 6)+1)
        K = vertices[offset:offset+size]; offset += size
        E.extend(zip(K, K[1:]))
        if size >= 4 and size % 2 == 0 and rng.randrange(2):
            E.append((K[-1], K[0]))
    U = {v for v in range(n) if rng.randrange(2)}
    X, Y = sorted(U), sorted(set(range(n))-U)
    rng.shuffle(X); rng.shuffle(Y)
    q = rng.randrange(min(len(X), len(Y), 7)+1)
    operations = list(zip(X[:q], Y[:q]))
    result = check(n, E, U, operations)
    reordered = blockwise_frontier(n, reversed(E), iter(U), iter(reversed(operations)))
    assert [r['cost'] for r in reordered['frontier']] == [r['cost'] for r in result['frontier']]
    counts['one_shot_permutation_controls'] += 1

# P4 physical hardness models as small general-domain controls, not new hardness.
for h, H in [(1, []), (2, [(0, 1)]), (3, [(0, 1), (1, 2)])]:
    x = charged_vertex_cover_template(h, H)
    q = min(x['q'], 9)
    check(2*x['b'], x['P']+x['Q'], x['initial_U'], [(a, b) for _, a, b in x['operations'][:q]])
    counts['physical_constructor_controls'] += 1

# Total cycle rank grows without exponential work; explicit all-row certificates.
large = []
for r in (1, 2, 4, 16, 64, 256):
    E = [(2*i, 2*i+1) for i in range(r)]
    U = {2*i for i in range(r)}
    result = blockwise_frontier(2*r, E, U, E)
    assert result['total_cycle_rank'] == r and result['maximum_block_cycle_rank'] == 1
    assert result['conditioned_branches'] == 2*r
    assert all(row['cost'] == 0 and row['selected_mask'].bit_count() == row['operations'] for row in result['frontier'])
    large.append(dict(r=r, total_rank=r, maximum_block_rank=1,
                      branches=result['conditioned_branches'],
                      convolution_transitions=result['convolution_transitions']))
    counts['unbounded_total_rank_families'] += 1

# Parallel two-edge cycle and empty/zero-operation instances are explicit.
result = check(4, [(0, 1), (2, 3)], {0, 2}, [(0, 3), (2, 1)], p2=True)
assert len(result['blocks']) == 1 and result['total_cycle_rank'] == 1
check(0, [], set(), [], p2=True)
for args in [(3, [(0, 1), (1, 2), (2, 0)], {0}, [(0, 1)]),
             (2, [(0, 1)], {0}, [(0, 1), (0, 1)])]:
    try:
        blockwise_frontier(*args)
    except ValueError:
        counts['invalid_input_rejections'] += 1
    else:
        raise AssertionError('Invalid instance accepted')

report = dict(scope='Exact connected-block factorization of unit maximum-matching cost over a fixed replacement list; largest block rank rather than total rank; polynomial P2/isolated-vertex class. No unrestricted omission, SF/beta or grid complexity claim.',
              counts=dict(sorted(counts.items())), digest=digest.hexdigest(), unbounded_total_rank=large)
p = argparse.ArgumentParser(); p.add_argument('--output', default=str(ROOT/'output/blockwise-component-frontier-check.json'))
dest = Path(p.parse_args().output); dest.parent.mkdir(parents=True, exist_ok=True)
dest.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
print(json.dumps(report['counts'], sort_keys=True))
