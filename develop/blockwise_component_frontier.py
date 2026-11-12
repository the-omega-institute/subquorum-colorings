"""Factor exact budget frontiers over connected candidate-component blocks.

The exponent is the maximum block cycle rank, not their sum. In particular,
ambient matchings (isolated vertices/P2 only) have block rank at most one.
"""
from component_cycle_frontier import component_frontier
from nonisolated_exchange_frontier import validate, endpoint


def blockwise_frontier(n, edges, U, operations):
    """Exact F(t), witnesses, and sum-of-block-exponent transition bound.

    Domain: simple bipartite ambient maximum degree2, distinct removal and
    addition endpoints. All subsets of the supplied candidate list allowed.
    """
    data = validate(n, edges, U, operations)
    components = data['components']
    owner = {v: j for j, (K, _) in enumerate(components) for v in K}
    adjacency = [set() for _ in components]
    for x, y in data['operations']:
        a, b = owner[x], owner[y]
        adjacency[a].add(b)
        adjacency[b].add(a)
    blocks, seen = [], set()
    for root in range(len(components)):
        if root in seen:
            continue
        seen.add(root)
        block, stack = [root], [root]
        while stack:
            for child in sorted(adjacency[stack.pop()] - seen):
                seen.add(child)
                block.append(child)
                stack.append(child)
        blocks.append(sorted(block))
    vertex_block = {v: j for j, block in enumerate(blocks)
                    for c in block for v in components[c][0]}
    block_edges = [[] for _ in blocks]
    block_ops = [[] for _ in blocks]
    for a, b in data['edges']:
        assert vertex_block[a] == vertex_block[b]
        block_edges[vertex_block[a]].append((a, b))
    for i, (x, y) in enumerate(data['operations']):
        assert vertex_block[x] == vertex_block[y]
        block_ops[vertex_block[x]].append(i)
    total, details, transitions, convolution = {0: (0, 0)}, [], 0, 0
    for j, block in enumerate(blocks):
        vertices = sorted(v for c in block for v in components[c][0])
        local = {v: k for k, v in enumerate(vertices)}
        ops = block_ops[j]
        result = component_frontier(
            len(vertices), [(local[a], local[b]) for a, b in block_edges[j]],
            {local[v] for v in vertices if v in data['U']},
            [(local[data['operations'][i][0]], local[data['operations'][i][1]]) for i in ops])
        rows = [(row['operations'], row['cost'],
                 sum(1 << i for k, i in enumerate(ops) if row['selected_mask'] >> k & 1))
                for row in result['frontier']]
        new = {}
        for t, (cost, mask) in total.items():
            for dt, dc, dm in rows:
                assert not (mask & dm)
                candidate = (cost + dc, mask | dm)
                if t + dt not in new or candidate < new[t + dt]:
                    new[t + dt] = candidate
                convolution += 1
        total = new
        transitions += result['transitions']
        details.append(dict(vertices=vertices, candidate_indices=ops,
                            component_count=len(block), cycle_rank=result['cycle_rank'],
                            conditioned_branches=result['conditioned_branches']))
    q = len(data['operations'])
    assert set(total) == set(range(q + 1))
    rows = [dict(operations=t, cost=total[t][0], selected_mask=total[t][1])
            for t in range(q + 1)]
    assert all(row['selected_mask'].bit_count() == row['operations'] for row in rows)
    best = min(rows, key=lambda r: (r['cost'], r['operations'], r['selected_mask']))
    selected = [i for i in range(q) if best['selected_mask'] >> i & 1]
    certificate = endpoint(n, data['edges'], data['U'], data['operations'], selected)
    assert certificate['actual_cost'] == best['cost']
    return dict(frontier=rows, best=best, certificate=certificate, blocks=details,
                total_cycle_rank=sum(b['cycle_rank'] for b in details),
                maximum_block_cycle_rank=max((b['cycle_rank'] for b in details), default=0),
                conditioned_branches=sum(b['conditioned_branches'] for b in details),
                transitions=transitions, convolution_transitions=convolution)
