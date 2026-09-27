"""Direct finite checks supporting the independently written structural proofs."""
import json
import re
from pathlib import Path


def direct_double_star():
    edges = {(0, 1), (0, 2), (0, 3), (1, 4), (1, 5)}
    neighbors = [{w for u, w in edges if u == v} | {u for u, w in edges if w == v}
                 for v in range(6)]
    beta = max(mask.bit_count() for mask in range(64)
               if all(not (mask >> v & 1) or
                      sum(mask >> w & 1 for w in neighbors[v]) <= 1 for v in range(6)))
    best, witness = 0, None

    def enumerate_colors(colors, count):
        nonlocal best, witness
        if len(colors) == 6:
            for v in range(6):
                if colors[v] < 0:
                    continue
                same = sum(colors[w] == colors[v] for w in neighbors[v])
                occupied = sum(colors[w] >= 0 for w in neighbors[v])
                if 2 * (1 + same) < 1 + occupied:
                    return
            if count > best:
                best, witness = count, colors
            return
        for color in range(-1, count + 1):
            enumerate_colors(colors + [color], max(count, color + 1))

    enumerate_colors([], 0)
    assert beta == 4 and best == 5
    points = [(2, 2), (2, 3), (1, 2), (2, 1), (2, 4), (3, 3)]
    embedded = {(u, v) for u in range(6) for v in range(u + 1, 6)
                if sum(abs(a - b) for a, b in zip(points[u], points[v])) == 1}
    assert embedded == edges
    return dict(beta2=beta, psi_sq=best, optimal_coloring=witness,
                induced_grid_embedding=points, edges=sorted(edges))


def signed_product():
    h = [[1, 1, 1, 1], [1, -1, 1, -1], [1, 1, -1, -1], [1, -1, -1, 1]]
    s = [[0] * 8 for _ in range(8)]
    for i in range(4):
        for j in range(4):
            s[i][4+j] = s[4+j][i] = h[i][j]
    product = [[0] * 16 for _ in range(16)]
    for u in range(8):
        for v in range(8):
            for a in range(2):
                product[2*u+a][2*v+a] = s[u][v]
        for a in range(2):
            product[2*u+a][2*u+1-a] = 1 if u < 4 else -1
    for matrix, degree in [(s, 4), (product, 5)]:
        n = len(matrix)
        assert all(matrix[i][j] == matrix[j][i] for i in range(n) for j in range(n))
        for i in range(n):
            for j in range(n):
                assert sum(matrix[i][k] * matrix[k][j] for k in range(n)) == (degree if i == j else 0)
    return dict(K44_square_scalar=4, K44_cartesian_K2_square_scalar=5,
                arithmetic='exact Python integers')


def check_enumeration():
    gaps = 0
    for size in range(1, 7):
        lines = Path(f'results/graph-equality-n{size}.txt').read_text().splitlines()
        assert lines[-1].startswith(f'COMPLETE n={size} labelled_graphs={2**(size*(size-1)//2)} ')
        for line in lines[:-1]:
            assert size == 6 and line.startswith('GAP')
            graph = int(re.search(r'graph_mask=(\d+)', line).group(1))
            edges, degrees, e = set(), [0]*6, 0
            for u in range(6):
                for v in range(u+1, 6):
                    if graph >> e & 1:
                        edges.add((u, v))
                        degrees[u] += 1
                        degrees[v] += 1
                    e += 1
            assert sorted(degrees) == [1, 1, 1, 1, 3, 3]
            assert tuple(i for i, d in enumerate(degrees) if d == 3) in edges
            gaps += 1
    assert gaps == 90
    return dict(graphs_checked=33867, strict_gaps=90,
                strict_gap_isomorphism_type='double star with two leaves at each center')


if __name__ == '__main__':
    report = dict(status='passed', double_star=direct_double_star(),
                  signed_matrices=signed_product(), small_graphs=check_enumeration(),
                  lean_formalized=False)
    Path('results/structural-checks.json').write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))
