"""Physical graph controls; the all-order extremal proof is in the note."""
import argparse
import json
from pathlib import Path

ROWS = ("11001", "11010", "00011", "01111", "10111")


def family(d, r):
    s = d - 2
    half = 5 * r + s
    adj = [set() for _ in range(2 * half)]

    def edge(a, b):
        assert a < half <= b
        adj[a].add(b)
        adj[b].add(a)

    for j in range(r):
        for a, row in enumerate(ROWS):
            for b, bit in enumerate(row):
                if bit == "1":
                    edge(5 * j + a, half + 5 * j + b)
    for q in range(s):
        for j in range(r):
            edge(5 * r + q, half + 5 * j + 2)
            edge(5 * j + 2, half + 5 * r + q)
    for j in range(r):
        for k in range(r):
            for a in range(2):
                for b in range(2):
                    edge(5 * j + a, half + 5 * k + b)
                    edge(5 * j + 3 + a, half + 5 * k + 3 + b)
    selected = {off + 5 * j + a for off in (0, half)
                for j in range(r) for a in (0, 1, 2)}
    return adj, selected, half


def covered(adj, x, selected):
    ns = adj[x] & selected
    return len(ns) >= 2 or any(adj[y] & selected for y in ns)


def connected_after(adj, removed):
    start = 0 if removed != 0 else 1
    seen = {start}
    todo = [start]
    while todo:
        v = todo.pop()
        fresh = adj[v] - seen - {removed}
        seen.update(fresh)
        todo.extend(fresh)
    return len(seen) == len(adj) - 1


def check(d, r):
    adj, selected, half = family(d, r)
    n = len(adj)
    assert n == 10 * r + 2 * (d - 2)
    assert len(selected) == 6 * r
    assert min(map(len, adj)) == d
    assert max(map(len, adj)) == 2 * r + 2
    assert all(not (adj[v] & set(range(half))) for v in range(half))
    assert all(covered(adj, x, selected) for x in range(n) if x not in selected)
    tested = 0
    # Explicit local deletion failures, without assuming the composition cap.
    for j in range(r):
        for off, v, x in ((0, 0, half + 4), (0, 1, half + 3),
                          (0, 2, 2), (half, 0, 4),
                          (half, 1, 3), (half, 2, half + 2)):
            deleted = off + 5 * j + v
            witness = 5 * j + x
            assert not covered(adj, witness, selected - {deleted})
            tested += 1
    # Every copy is still induced H; restriction of any global dissociation
    # set to it is therefore bounded by five by the written base-graph proof.
    for j in range(r):
        vertices = [5 * j + a for a in range(5)] + [half + 5 * j + b for b in range(5)]
        for a in range(5):
            for b in range(5):
                assert (vertices[5 + b] in adj[vertices[a]]) == (ROWS[a][b] == "1")
    if r <= 16:
        removals = list(range(n))
    else:
        removals = sorted({off + 5 * j + a for off in (0, half)
                           for j in (0, r - 1) for a in range(5)} |
                          {5 * r, half + 5 * r})
    assert all(connected_after(adj, v) for v in removals)
    return dict(d=d, r=r, n=n, selected_size=len(selected),
                expected_beta=half, certified_gap_at_least=r - d + 2,
                deletion_failures=tested, vertex_deletions=len(removals),
                degree_two_vertices=sum(len(ns) == 2 for ns in adj))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    cases = [check(d, r) for d in range(3, 9)
             for r in sorted({d, d + 1, d + 4, 16, 64, 128})]
    report = dict(status="PASS", families=len(cases), cases=cases,
                  deletion_failures=sum(c["deletion_failures"] for c in cases),
                  vertex_deletions=sum(c["vertex_deletions"] for c in cases),
                  scope="Physical construction, literal forming predicate and explicit single-deletion failures, induced blocks, exact degrees and connectivity after the listed vertex deletions. Beta upper bound and all-order conclusions have written proofs; these checks do not compute SF optima.")
    args.output.write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({k: v for k, v in report.items() if k != "cases"}))


if __name__ == "__main__":
    main()
