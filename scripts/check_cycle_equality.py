"""Check the cycle family from its physical graph, without using H gluing."""
import argparse
import json
from pathlib import Path
from check_minimum_degree_sharpness import covered, connected_after


def family(r):
    half = 5 * r
    adj = [set() for _ in range(2 * half)]

    def edge(a, b):
        assert a < half <= b
        adj[a].add(b)
        adj[b].add(a)

    for j in range(r):
        for t in range(2):
            edge(5 * j + 2, half + 5 * j + 3 + t)
            edge(5 * j + 3 + t, half + 5 * j + 2)
            edge(5 * j + 3 + t, half + 5 * j + 3 + t)
            edge(5 * j + t, half + 5 * j + 3 + t)
            edge(5 * j + 3 + t, half + 5 * j + t)
    for i in range(2 * r):
        for j in range(2 * r):
            edge(5 * (i // 2) + i % 2, half + 5 * (j // 2) + j % 2)
    return adj, half


def check(r):
    adj, half = family(r)
    n = len(adj)
    selected = {off + 5 * j + a for off in (0, half)
                for j in range(r) for a in (0, 1, 2)}
    assert len(selected) == 6 * r
    assert all(covered(adj, v, selected) for v in range(n) if v not in selected)
    for j in range(r):
        for off in (0, half):
            for t in range(2):
                owner = off + 5 * j + t
                witness = half - off + 5 * j + 3 + t
                assert not covered(adj, witness, selected - {owner})
            iso = off + 5 * j + 2
            assert not covered(adj, iso, selected - {iso})
    assert {len(v) for v in adj} == {2, 3, 2 * r + 1}
    assert sum(len(v) == 2 for v in adj) == 2 * r
    assert not any(len(v) == 4 for v in adj)
    removals = list(range(n)) if r <= 16 else [off + 5 * j + t for off in (0, half) for j in (0, r - 1) for t in range(5)]
    assert all(connected_after(adj, v) for v in removals)
    return dict(r=r, n=n, selected_size=len(selected), degree_two=2 * r,
                degree_four=0, deletion_failures=6 * r,
                vertex_deletions=len(removals))


def local_eight():
    # Two support leaves in A, I_A, two W_A; I_B and two W_B in B.
    edges = [(0, 6), (1, 7), (2, 6), (2, 7), (3, 5), (4, 5), (3, 6), (4, 7)]
    adj = [set() for _ in range(8)]
    for a, b in edges:
        adj[a].add(b)
        adj[b].add(a)
    sizes = [s.bit_count() for s in range(256)
             if all(sum(s >> j & 1 for j in adj[v]) <= 1
                    for v in range(8) if s >> v & 1)]
    assert max(sizes) == 5
    return dict(subsets=256, beta_2=5)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = [check(r) for r in list(range(2, 13)) + [32, 128]]
    report = dict(status="PASS", local_eight=local_eight(), families=len(cases),
                  deletion_failures=sum(c["deletion_failures"] for c in cases),
                  vertex_deletions=sum(c["vertex_deletions"] for c in cases), cases=cases,
                  scope="The literal graph, all displayed minimality failures, degree multiset and listed vertex deletions. The all-r exact beta/SF values rely on the written proof. No H composition formula is used.")
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}))


if __name__ == "__main__":
    main()
