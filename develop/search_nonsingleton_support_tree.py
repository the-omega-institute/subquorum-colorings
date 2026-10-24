"""Discovery only: two frozen original alpha owners sharing one support unit.

Use `uv run --with z3-solver python ...`. UNKNOWN is not nonexistence.
Successful candidates are independently recompiled before they are archived.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import time

import z3

from check_boundary_sealed_gap_obstruction import support_allocation
from check_bt_corridor_ports import compile_model
from check_cooperative_promotion import neighbors
from check_even_bridge_support_completion import endpoints_of
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_joint_tree_beta_compensation import joint_allocate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check


def search(rows, cols, timeout, one_sided_beta=False, competing_tree=False):
    points = sorted(itertools.product(range(rows), range(cols)))
    universe = set(points)
    adjacent = {v: sorted(set(neighbors(v)) & universe) for v in points}
    edges = sorted({tuple(sorted((v, w))) for v in points for w in adjacent[v]})
    incident = {v: [e for e in edges if v in e] for v in points}
    t = {v: z3.Bool('t_%d_%d' % v) for v in points}
    p = {v: z3.Bool('p_%d_%d' % v) for v in points}
    m = {e: z3.Bool('m_%d_%d_%d_%d' % (*e[0], *e[1])) for e in edges}
    rank = {v: z3.Int('rank_%d_%d' % v) for v in points}
    owner = {v: z3.Int('owner_%d_%d' % v) for v in points}
    count = lambda terms: z3.Sum([z3.If(a, 1, 0) for a in terms])
    solver = z3.Solver()
    solver.set(timeout=timeout*1000, random_seed=20261025)
    blank = lambda v: z3.And(z3.Not(t[v]), z3.Not(p[v]))
    for v in points:
        solver.add(z3.Not(z3.And(t[v], p[v])))
        solver.add(count(m[e] for e in incident[v]) == z3.If(p[v], 1, 0))
        solver.add(rank[v] >= 0, rank[v] < len(points), owner[v] >= 0,
                   owner[v] <= (6 if competing_tree else 5 if one_sided_beta else 2))
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
        partner = v[0] ^ 1, v[1]
        solver.add(z3.Implies(z3.And(p[v], p[partner]), owner[v] == owner[partner]))
        tp[v], bp[v] = z3.And(p[v], t[partner]), z3.And(p[v], blank(partner))
    for label in ((1, 2, 6) if competing_tree else (1, 2)):
        solver.add(count(z3.And(tp[v], owner[v] == label) for v in points) == 2)
        solver.add(count(z3.And(bp[v], owner[v] == label) for v in points) == 0)
    target_band, target_col = 2, cols//2
    target_row = 2*target_band+1
    for c, label in ((target_col-1, 1), (target_col+1, 2)):
        solver.add(p[target_row, c], owner[target_row, c] == label,
                   t[target_row-1, c])
    solver.add(blank((target_row, target_col)), blank((target_row-1, target_col)))
    if one_sided_beta:
        for label in (3, 4, 5):
            solver.add(count(z3.And(tp[v], owner[v] == label) for v in points) == (0 if label == 5 else 1))
            solver.add(count(z3.And(bp[v], owner[v] == label) for v in points) == (2 if label == 5 else 1))
        beta_witnesses = []
        for v in points:
            for w in ((v[0], v[1]-1), (v[0], v[1]+1)):
                if w not in universe:
                    continue
                solver.add(z3.Implies(z3.And(tp[v], owner[v] == 1, bp[w]),
                                      z3.Or(owner[w] == 3, owner[w] == 4)))
                beta_witnesses.append(z3.And(tp[v], owner[v] == 2, bp[w], owner[w] == 5))
        solver.add(z3.Or(beta_witnesses))
        if competing_tree:
            competitors=[]
            for v in points:
                for w in ((v[0],v[1]-1),(v[0],v[1]+1)):
                    if w not in universe:
                        continue
                    solver.add(z3.Implies(z3.And(tp[v],z3.Or(owner[v] == 2,owner[v] == 6),bp[w]),
                                          z3.Or(owner[w] == 3,owner[w] == 4,owner[w] == 5)))
                    competitors.append(z3.And(tp[v],owner[v] == 6,bp[w],owner[w] == 5))
            solver.add(z3.Or(competitors))
    # Nearest P owner on either side; zero also denotes no P boundary.
    for band in range(rows//2):
        po, bb, node = {}, {}, {}
        for c in range(cols):
            a, b = (2*band, c), (2*band+1, c)
            po[c] = z3.Or(p[a], p[b])
            bb[c] = z3.And(blank(a), blank(b))
            node[c] = z3.If(p[a], owner[a], owner[b])
        left = {c: z3.Int('left_%d_%d' % (band,c)) for c in range(cols)}
        right = {c: z3.Int('right_%d_%d' % (band,c)) for c in range(cols)}
        for c in range(cols):
            solver.add(left[c] == z3.If(po[c], node[c], left[c-1] if c else 0))
            solver.add(right[c] == z3.If(po[c], node[c], right[c+1] if c+1 < cols else 0))
            if c not in (0, cols-1) and (band, c) != (target_band, target_col):
                forbidden=(1,2,6) if competing_tree else (1,2)
                solver.add(z3.Implies(bb[c], z3.And(
                    [z3.And(left[c] != label,right[c] != label) for label in forbidden])))
    start = time.monotonic()
    status = solver.check()
    report = dict(shape=[rows,cols], timeout_seconds=timeout, solver_version=z3.get_version_string(),
                  status=str(status), seconds=time.monotonic()-start,
                  target=[target_band,target_col], one_sided_beta=one_sided_beta,
                  competing_tree=competing_tree,
                  reason=solver.reason_unknown())
    if status != z3.sat:
        return report
    model = solver.model()
    selected = {v for v in points if z3.is_true(model.eval(t[v]))}
    matching = [e for e in edges if z3.is_true(model.eval(m[e]))]
    current = rows, cols, selected, matching
    direct_check(*current)
    frozen, layers = frozen_certificate(current)
    assert frozen == endpoints_of(current)
    bands = whole_bands(current)
    data, meta = compile_model(current, bands, Counter())
    result, support = support_allocation(current,bands,data,meta,[],Counter(),return_model=True)
    kinds = data[0]
    betas = [pair for pair in support['reduced'] if all(kinds[v] == 'BP' for v in pair)]
    aa = {v: a for a,pair in enumerate(support['alphas']) for v in pair}
    bb = {v: b for b,pair in enumerate(betas) for v in pair}
    adjacency = {b: set() for b in range(len(betas))}
    for a,b in data[2]:
        if a in aa and b in bb:
            adjacency[bb[b]].add(aa[a])
    joint = joint_allocate(result['alpha'],support['incidence'],adjacency)
    assert any(len(tree['demands']) == 2 for tree in joint['trees'])
    reroot_control = None
    if one_sided_beta and not competing_tree:
        first,second = aa[target_row,target_col-1], aa[target_row,target_col+1]
        assert all(first not in users for users in adjacency.values())
        assert any(second in users for users in adjacency.values())
        shared = next(j for j,users in support['incidence'].items() if first in users and second in users)
        baseline = dict(joint['baseline'])
        baseline.pop(first,None);baseline.pop(second,None);baseline[second] = shared
        rerooted = joint_allocate(result['alpha'],support['incidence'],adjacency,baseline)
        assert rerooted['changes'] >= 1
        reroot_control = dict(first=first,second=second,shared=shared,
                              baseline=baseline,changes=rerooted['changes'],
                              interval_assignment=rerooted['intervals'],beta_assignment=rerooted['betas'])
    if competing_tree:
        assert joint['t'] > joint['mu']
    report.update(selected=sorted(selected),matching=matching,freezing_layers=layers,
                  alpha_pairs=support['alphas'], beta_pairs=betas, support=result,
                  incidence=[dict(interval=j,owners=sorted(users),record=meta['intervals'][j])
                             for j,users in support['incidence'].items() if users],
                  beta_adjacency={b: sorted(users) for b,users in adjacency.items()},
                  trees=joint['trees'],mu=joint['mu'],changes=joint['changes'],
                  forced_reroot=reroot_control)
    return report


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rows',type=int,required=True)
    parser.add_argument('--cols',type=int,required=True)
    parser.add_argument('--timeout-seconds',type=int,default=60)
    parser.add_argument('--one-sided-beta',action='store_true')
    parser.add_argument('--competing-tree',action='store_true')
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    assert args.rows >= 10 and args.cols >= 14 and args.rows%2 == args.cols%2 == 0
    assert not args.competing_tree or args.one_sided_beta
    result=search(args.rows,args.cols,args.timeout_seconds,args.one_sided_beta,args.competing_tree)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k in
                     ('shape','status','seconds','reason','mu','changes')}))


if __name__ == '__main__':
    main()
