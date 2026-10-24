"""Discovery only: two genuinely unported alpha owners enter one mixed gate."""
import itertools
import json
import sys
import z3

from check_cooperative_promotion import neighbors
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_terminal_cancellation_and_stranded_demand import terminal_data, extended_ports
from collections import Counter


def search(rows, cols, timeout):
    points = sorted(itertools.product(range(rows), range(cols)))
    universe = set(points)
    adjacent = {v: sorted(set(neighbors(v)) & universe) for v in points}
    edges = sorted({tuple(sorted((v, w))) for v in points for w in adjacent[v]})
    incident = {v: [e for e in edges if v in e] for v in points}
    t = {v: z3.Bool('t_%d_%d' % v) for v in points}
    p = {v: z3.Bool('p_%d_%d' % v) for v in points}
    m = {e: z3.Bool('m_%d_%d_%d_%d' % (*e[0], *e[1])) for e in edges}
    rank = {v: z3.Int('r_%d_%d' % v) for v in points}
    owner = {v: z3.Int('o_%d_%d' % v) for v in points}
    count = lambda terms: z3.Sum([z3.If(a, 1, 0) for a in terms])
    solver = z3.Solver()
    solver.set(timeout=timeout * 1000)
    blank = lambda v: z3.And(z3.Not(t[v]),z3.Not(p[v]))
    bb = lambda row,col: z3.And(blank((row,col)),blank((row^1,col)))
    for v in points:
        solver.add(z3.Not(z3.And(t[v], p[v])))
        solver.add(count(m[e] for e in incident[v]) == z3.If(p[v], 1, 0))
        solver.add(rank[v] >= 0, rank[v] < len(points))
        solver.add(owner[v] >= 0, owner[v] <= 3)
        solver.add(z3.Implies(t[v], count(z3.Or(t[w], p[w]) for w in adjacent[v]) <= 1))
        retained = [z3.Or(t[w], z3.Or([
            z3.And(m[e], rank[next(u for u in e if u != w)] < rank[v])
            for e in incident[w]])) for w in adjacent[v]]
        solver.add(z3.Implies(p[v], count(retained) >= 2))
        if v[0] in (0, rows-1) or v[1] in (0, cols-1):
            solver.add(z3.Not(p[v]), z3.Not(t[v]))
    for a, b in edges:
        solver.add(z3.Implies(m[a, b], owner[a] == owner[b]))
    tp, bp = {}, {}
    for v in points:
        partner = (v[0] ^ 1, v[1])
        solver.add(z3.Implies(z3.And(p[v], p[partner]), owner[v] == owner[partner]))
        tp[v] = z3.And(p[v], t[partner])
        bp[v] = z3.And(p[v], blank(partner))
        for direction in (-1,1):
            r,c=v; mid=c+direction; dest=c+2*direction
            guard=z3.And(tp[v],z3.Or(owner[v]==1,owner[v]==2))
            if 0 <= mid < cols:
                solver.add(z3.Implies(guard,z3.Not(bb(r,mid))))
            if 0 <= dest < cols:
                cap=z3.And(t[r,mid],blank((r^1,mid)),bb(r,dest))
                solver.add(z3.Implies(guard,z3.Not(cap)))
    for label in (1, 2, 3):
        solver.add(count(z3.And(tp[v], owner[v] == label) for v in points) == (1 if label == 3 else 2))
        solver.add(count(z3.And(bp[v], owner[v] == label) for v in points) == (1 if label == 3 else 0))
    row, col = 5, cols//2
    for v, label in [((row, col-1), 1), ((row, col+1), 2), ((row, col), 3)]:
        solver.add(p[v], owner[v] == label)
    solver.add(t[row-1, col-1], t[row-1, col+1], blank((row-1,col)))
    status = solver.check()
    print(status, solver.reason_unknown(), flush=True)
    if status != z3.sat:
        return
    model = solver.model()
    selected = {v for v in points if z3.is_true(model.eval(t[v]))}
    matching = [e for e in edges if z3.is_true(model.eval(m[e]))]
    current = rows, cols, selected, matching
    direct_check(*current)
    assert frozen_certificate(current)[0] == {v for e in matching for v in e}
    data = terminal_data(current, whole_bands(current))
    ports=extended_ports(current,whole_bands(current),*data[1:5],data[6],Counter())
    print('pairs', [(pair, [data[4][v] for v in pair], [ports[v] for v in pair]) for pair in data[5]], flush=True)
    out = dict(shape=[rows, cols], selected=sorted(selected), matching=matching)
    with open('/tmp/subquorum-unported-gate-%dx%d.json'%(rows,cols),'w') as stream:
        json.dump(out, stream, indent=2)


if __name__ == "__main__":
    rows, columns, timeout = map(int, sys.argv[1:])
    search(rows, columns, timeout)
