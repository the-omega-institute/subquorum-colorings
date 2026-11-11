"""Independent finite controls for the four-attachment written proof.

Uses only the standard library. --exact invokes a separate C++ subset evaluator.
Finite controls do not replace the general argument.
"""
import argparse
from collections import Counter
from itertools import combinations
import json
from pathlib import Path
import random
import subprocess
import tempfile

ROWS = ('11001', '11010', '00011', '01111', '10111')
PORTS = {0, 1, 5, 6}
SELECTED = {0, 1, 2, 5, 6, 7}
WITNESSES = {0: 9, 1: 8, 2: 2, 5: 4, 6: 3, 7: 7}


def base():
    adj = [set() for _ in range(10)]
    for a, row in enumerate(ROWS):
        for b, entry in enumerate(row):
            if entry == '1':
                adj[a].add(5 + b)
                adj[5 + b].add(a)
    return adj


def condition(adj, chosen, x):
    neighbors = adj[x] & chosen
    return len(neighbors) >= 2 or any(adj[u] & chosen for u in neighbors)


def literal(adj, chosen, x):
    # Examine each possible center and two distinct leaves of a star containing x.
    support = chosen | {x}
    return any(x in {center, u, v}
               for center in support
               for u, v in combinations(adj[center] & support, 2))


def forms(adj, chosen):
    return all(condition(adj, chosen, x) for x in set(range(len(adj))) - chosen)


def dominates(adj, chosen):
    return all(adj[x] & chosen for x in set(range(len(adj))) - chosen)


def safe(adj, chosen):
    return [v for v in sorted(chosen - PORTS)
            if forms(adj, chosen - {v})
            and all(not adj[p] & chosen or adj[p] & (chosen - {v})
                    for p in chosen & PORTS)]


def local_checks():
    adj = base()
    closed = [adj[x] | {x} for x in range(10)]
    triples = [c for c in closed if len(c) == 3]
    quads = [c for c in closed if len(c) == 4]
    assert len(triples) == 2 and triples[0].isdisjoint(triples[1])
    assert len(quads) == 4 and all(len(a & b) <= 2 for a, b in combinations(quads, 2))
    assert all(len(adj[x]) + len(adj[y]) >= 6 for x in range(10) for y in adj[x])
    records = []
    literal_checks = 0
    minimal_hist = Counter()
    beta = 0
    for mask in range(1024):
        chosen = {v for v in range(10) if mask >> v & 1}
        for x in set(range(10)) - chosen:
            assert condition(adj, chosen, x) == literal(adj, chosen, x)
            literal_checks += 1
        if all(len(adj[x] & chosen) <= 1 for x in chosen):
            beta = max(beta, len(chosen))
        if forms(adj, chosen) and all(not forms(adj, chosen - {v}) for v in chosen):
            minimal_hist[len(chosen)] += 1
        if len(chosen) >= 6:
            assert forms(adj, chosen) == dominates(adj, chosen)
        if len(chosen) < 7 or not dominates(adj, chosen):
            continue
        t = len(chosen & PORTS)
        bad_dom = {v for v in chosen - PORTS if not dominates(adj, chosen - {v})}
        bad_activity = {v for v in chosen - PORTS
                        if any(adj[p] & chosen and not adj[p] & (chosen - {v})
                               for p in chosen & PORTS)}
        assert len(bad_dom) <= 2
        assert len(bad_activity) <= t if t <= 2 else not bad_activity
        assert len(chosen - PORTS) > len(bad_dom | bad_activity)
        choices = safe(adj, chosen)
        assert choices
        records.append(dict(mask=mask, selected_ports=t, safe_deletions=choices))
    assert beta == 5 and max(minimal_hist) == 6
    return dict(subsets=1024, literal_local_comparisons=literal_checks,
                dense_dominating_selections=len(records), beta_2=beta, SF_2=max(minimal_hist),
                minimal_size_counts=dict(minimal_hist), safe_choices=records)


def ambient_checks():
    rng = random.Random(20261111)
    checked = 0
    covered = Counter()
    for trial in range(60):
        adj = base() + [set() for _ in range(8)]
        for x in range(18):
            for y in range(max(10, x + 1), 18):
                if x < 10 and x not in PORTS:
                    continue
                if rng.randrange(3) == 0:
                    adj[x].add(y)
                    adj[y].add(x)
        for local_mask in range(1024):
            local = {v for v in range(10) if local_mask >> v & 1}
            if len(local) < 7:
                continue
            chosen = local | {x for x in range(10, 18) if rng.randrange(2)}
            if not forms(adj, chosen):
                continue
            assert dominates(base(), local)
            choices = safe(base(), local)
            assert choices
            for v in choices:
                assert forms(adj, chosen - {v})
                checked += 1
            covered[len(local & PORTS)] += 1
    return dict(seed=20261111, surrounding_graphs=60, safe_global_deletions=checked,
                forming_restrictions_by_selected_ports=dict(covered),
                nonbipartite_surroundings_allowed=True)


def connected(adj, deleted=None):
    vertices = set(range(len(adj))) - ({deleted} if deleted is not None else set())
    if not vertices:
        return True
    seen = {next(iter(vertices))}
    todo = list(seen)
    while todo:
        for u in adj[todo.pop()] & vertices - seen:
            seen.add(u)
            todo.append(u)
    return seen == vertices


def euler_orientation(q):
    edges = {tuple(sorted((x, y))) for x, ns in enumerate(q) for y in ns}
    stack = [0]
    tour = []
    while stack:
        x = stack[-1]
        choices = [y for y in q[x] if tuple(sorted((x, y))) in edges]
        if choices:
            y = min(choices)
            edges.remove(tuple(sorted((x, y))))
            stack.append(y)
        else:
            tour.append(stack.pop())
    assert not edges
    tour.reverse()
    return list(zip(tour, tour[1:]))


def topology_checks():
    records = []
    for order in range(5, 25):
        q = [{(x + d) % order for d in (-2, -1, 1, 2)} for x in range(order)]
        arcs = euler_orientation(q)
        assert Counter(x for x, y in arcs) == Counter({x: 2 for x in range(order)})
        assert Counter(y for x, y in arcs) == Counter({x: 2 for x in range(order)})
        adj = [set() for _ in range(10 * order)]
        for i in range(order):
            for x, ns in enumerate(base()):
                adj[10 * i + x].update(10 * i + y for y in ns)
        outgoing = Counter()
        incoming = Counter()
        for x, y in arcs:
            u, v = 10 * x + 5 + outgoing[x], 10 * y + incoming[y]
            outgoing[x] += 1
            incoming[y] += 1
            adj[u].add(v)
            adj[v].add(u)
        chosen = {10 * i + v for i in range(order) for v in SELECTED}
        assert len(chosen) == 6 * order and forms(adj, chosen)
        for i in range(order):
            for deleted, failure in WITNESSES.items():
                assert not condition(adj, chosen - {10 * i + deleted}, 10 * i + failure)
        independent = {10 * i + a for i in range(order) for a in range(5)}
        assert all(not adj[x] & independent for x in independent)
        assert sum(map(len, adj)) == 36 * order
        assert Counter(map(len, adj)) == {2: 2 * order, 4: 8 * order}
        assert all((x % 10 < 5) != (y % 10 < 5) for x, ns in enumerate(adj) for y in ns)
        assert connected(adj) and all(connected(adj, v) for v in range(len(adj)))
        assert all(len(adj[10 * i + p]) == 4 for i in range(order) for p in PORTS)
        records.append(dict(interface_vertices=order, order=10 * order,
                            edges=18 * order, attaining_forming_size=len(chosen),
                            attaining_dissociation_size=len(independent), two_connected=True))
    return records


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    p.add_argument('--exact', action='store_true')
    args = p.parse_args()
    report = dict(status='PASS', local=local_checks(), ambient=ambient_checks(),
                  topologies=topology_checks(),
                  scope='Finite independent controls. General conclusions have written proofs; no new Lean run.')
    if args.exact:
        with tempfile.TemporaryDirectory(prefix='four-port-exact-') as tmp:
            executable = Path(tmp) / 'exact'
            subprocess.run(['c++', '-O3', '-std=c++17', '-Wall', '-Wextra',
                            str(Path(__file__).with_name('four_port_exact.cpp')),
                            '-o', str(executable)], check=True)
            result = subprocess.run([str(executable)], capture_output=True, text=True, check=True)
            report['exact_two_block'] = json.loads(result.stdout)
        assert len(report['exact_two_block']) == 256
        assert all(x['beta_2'] == 10 and x['SF_2'] == 12 for x in report['exact_two_block'])
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(dict(status=report['status'], local=report['local']['dense_dominating_selections'],
                          ambient=report['ambient'], topology_models=len(report['topologies']),
                          exact_patterns=len(report.get('exact_two_block', [])),
                          exact_subsets=sum(x['subsets'] for x in report.get('exact_two_block', [])))))


if __name__ == '__main__':
    if not __debug__:
        raise RuntimeError('Run without -O; assertions are part of verification.')
    main()
