"""Discovery only: simultaneous matching edges, old endpoint coverage, local cuts.

Requires SciPy/NumPy. Printed rational reconstructions of numerical LP solutions
are candidates, not certificates. The separate integer-arithmetic verifier is
the acceptance gate for the lattice witness used in the mathematical note.
"""
import argparse
from fractions import Fraction
import itertools
import json
from pathlib import Path

import numpy as np
from scipy.optimize import linprog, milp, Bounds, LinearConstraint
from scipy.sparse import lil_matrix

from check_connected_band_local_relaxation import connected_cells, WINDOWS
from check_connected_band_mate_coverage_barrier import POINT, reduced
from check_occupied_strip_degree_four_budget import family
from check_endpoint_invasion_sharp_strips import endpoints, free_vertices, edge_key
from check_lower_guard_merger_frontier import guard, lower_guard
from check_cooperative_promotion import neighbors


def solve(m, objective='component', fixed=False, periodic=False, seed=None, lattice=False,
          integral=False, selection_integral=False):
    old = family(m + 1)[0]
    P0 = endpoints(old[3])
    R = old[2] - {guard(i) for i in range(m)} - {lower_guard(i) for i in range(m)}
    R -= {(4, 12 + 6*i) for i in range(m-1)}
    U = free_vertices((*old[:2], R, old[3]))
    C = connected_cells(m)
    adjacent = lambda v: set(neighbors(v))
    if periodic:
        sample = family(6)[0]
        P0 = {reduced(v) for v in endpoints(sample[3]) if 12 <= v[1] < 18}
        U = C = set(POINT)
        R = set()
        adjacent = lambda v: {reduced(w) for w in neighbors(v) if 0 <= w[0] < 6}
    vs = sorted(U)
    possible = U | P0
    es = sorted({edge_key((v, u)) for v in possible for u in adjacent(v) & possible})
    ti = {v: i for i, v in enumerate(vs)}
    ei = {e: len(vs)+i for i, e in enumerate(es)}
    n = len(vs) + len(es)
    inc = {v: {ei[e]: 1 for e in es if v in e} for v in possible}
    rows, rhs, labels, eq, erhs = [], [], [], [], []

    def add(label, parts, b):
        row = {}
        for scale, part in parts:
            for j, a in part.items():
                row[j] = row.get(j, 0) + scale*a
        rows.append(row); rhs.append(b); labels.append(label)

    def t(v): return {ti[v]: 1}
    def o(v): return {ti[v]: 1, **inc[v]}
    for v in sorted(P0):
        eq.append(inc[v]); erhs.append(1)
    for v in vs:
        add(('occupation', v), [(1, o(v))], 1)
        b = len(adjacent(v) & P0)
        ns = sorted(adjacent(v) & U)
        if b >= 2:
            add(('forbid', v), [(1, t(v))], 0)
        if b >= 1:
            for u in ns:
                add(('anchor', v, u), [(1, t(v)), (1, o(u))], 1)
        for a, w in itertools.combinations(ns, 2):
            add(('wedge', v, a, w), [(1, t(v)), (1, o(a)), (1, o(w))], 2)
        add(('degree', v), [(len(ns)+b-1, t(v))]+[(1, o(u)) for u in ns], len(ns))
        if v in C and v[0] == 5:
            add(('star', v), [(1, t(u)) for u in ns+[v]]+[(1, o(u)) for u in ns+[v]], 6)
    for name, pat, b in WINDOWS:
        for i in range(1 if periodic else m):
            S = {(r, c+9+6*i) for r, c in pat}
            if periodic: S = {reduced(v) for v in S}
            if S <= C:
                add((name, i), [(1, t(v)) for v in S]+[(1, o(v)) for v in S], b)
    if fixed:
        for v in sorted(C):
            tv, ov = POINT[reduced(v)]
            if v == (5, 6*m+5): ov = tv
            eq.extend([t(v), inc[v]]); erhs.extend([float(tv), float(ov-tv)])
    if seed is not None:
        ts = {tuple(v): Fraction(q) for v,q in seed['T']}
        xs = {tuple(map(tuple,e)): Fraction(q) for e,q in seed['X']}
        # Keep the middle periodic, leaving two modules for each boundary adapter.
        for v in vs:
            if 20 <= v[1] <= 6*m-8:
                eq.append(t(v)); erhs.append(float(ts.get(reduced(v),0)))
        for e in es:
            if all(20 <= v[1] <= 6*m-8 for v in e):
                pe=edge_key(tuple(reduced(v) for v in e))
                eq.append({ei[e]:1}); erhs.append(float(xs.get(pe,0)))

    def matrix(dicts):
        mat = lil_matrix((len(dicts), n), dtype=float)
        for i, row in enumerate(dicts):
            for j, a in row.items(): mat[i,j] = a
        return mat.tocsr()
    obj = np.zeros(n)
    if objective == 'component':
        for v in C:
            obj[ti[v]] += 2
            for j in inc[v]: obj[j] += 1
    else:
        obj[:] = 1
    if lattice or integral or selection_integral:
        scale=80 if lattice else 1
        integer_mask=np.ones(n)
        if selection_integral:integer_mask[len(vs):]=0
        res=milp(-obj,integrality=integer_mask,bounds=Bounds(0,scale),
                 constraints=[LinearConstraint(matrix(rows),-np.inf,np.array(rhs)*scale),
                              LinearConstraint(matrix(eq),np.array(erhs)*scale,np.array(erhs)*scale)],
                 options={'time_limit':30,'mip_rel_gap':0.02})
        if res.x is not None:
            res.x=res.x/scale;res.fun=res.fun/scale
    else:
        res = linprog(-obj, A_ub=matrix(rows), b_ub=rhs, A_eq=matrix(eq), b_eq=erhs,
                      bounds=(0,None), method='highs')
    out = dict(m=m, objective=objective, fixed_92_point=fixed, periodic=periodic,
               success=bool(res.success),has_incumbent=res.x is not None,
               message=res.message,
               scope='Numerical discovery only; all rational reconstructions require independent exact verification.')
    if hasattr(res, 'mip_gap'):
        out['numerical_mip_gap'] = res.mip_gap
        out['numerical_mip_dual_bound'] = res.mip_dual_bound
    if res.x is not None:
        rat = lambda x: str(Fraction(float(x)).limit_denominator(100000))
        out.update(value=rat(-res.fun+(len(R) if objective=='whole' else 0)),
                   T=[(v,rat(res.x[ti[v]])) for v in vs if res.x[ti[v]]>1e-8],
                   X=[(e,rat(res.x[ei[e]])) for e in es if res.x[ei[e]]>1e-8])
    return out


if __name__ == '__main__':
    p=argparse.ArgumentParser();p.add_argument('--m',type=int,nargs='+',default=[2,3,4,8])
    p.add_argument('--periodic',action='store_true')
    p.add_argument('--seed',type=Path)
    p.add_argument('--lattice',action='store_true')
    p.add_argument('--integral',action='store_true')
    p.add_argument('--selection-integral',action='store_true')
    p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    out=[]
    for m in ([6] if args.periodic else args.m):
        modes=([('whole',False)] if args.integral or args.selection_integral else
               [('component',False)] if args.periodic or args.seed else [('component',True),('component',False),('whole',False)])
        for mode,fixed in modes:
            r=solve(m,mode,fixed,args.periodic,json.loads(args.seed.read_text())[0] if args.seed else None,args.lattice,args.integral,args.selection_integral);out.append(r)
            print({k:v for k,v in r.items() if k not in ['T','X']},flush=True)
    args.output.write_text(json.dumps(out,indent=2)+'\n')
