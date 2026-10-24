"""Optional Z3 discovery: frozen shared-beta fork configurations.

SAT supplies a fixture, never a general theorem; UNKNOWN is not UNSAT.
The default seeks an exchange obstruction; --free-alpha-ports relaxes that
condition and can produce shared-beta fixtures with no exchange gap. Label 0
with --extra-owners permits additional exterior strands. The permanent
verifiers use no Z3.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import time

import z3

from check_cooperative_promotion import neighbors
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_terminal_cancellation_and_stranded_demand import terminal_data, extended_ports


def search(rows, cols, seconds, output, placement, extra_owners=False, free_alpha_ports=False):
    assert rows >= 12 and cols >= 12 and rows % 2 == cols % 2 == 0
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
    count = lambda terms: z3.Sum([z3.If(term, 1, 0) for term in terms])
    solver = z3.Solver()
    solver.set(timeout=1000*seconds)
    blank = lambda v: z3.And(z3.Not(t[v]), z3.Not(p[v]))
    bb = lambda r, c: z3.And(blank((r, c)), blank((r ^ 1, c)))
    for v in points:
        solver.add(z3.Not(z3.And(t[v], p[v])))
        solver.add(count(m[e] for e in incident[v]) == z3.If(p[v], 1, 0))
        solver.add(rank[v] >= 0, rank[v] < len(points),
                   owner[v] >= (0 if extra_owners else 1), owner[v] <= 3)
        solver.add(z3.Implies(t[v], count(z3.Or(t[w], p[w]) for w in adjacent[v]) <= 1))
        retained = [z3.Or(t[w], z3.Or([
            z3.And(m[e], rank[next(u for u in e if u != w)] < rank[v])
            for e in incident[w]])) for w in adjacent[v]]
        solver.add(z3.Implies(p[v], count(retained) >= 2))
        if v[0] in (0, rows-1) or v[1] in (0, cols-1):
            solver.add(blank(v))
    for a, b in edges:
        solver.add(z3.Implies(m[a, b], owner[a] == owner[b]))
    tp, bp = {}, {}
    for r, c in points:
        v, partner = (r, c), (r ^ 1, c)
        solver.add(z3.Implies(z3.And(p[v], p[partner]), owner[v] == owner[partner]))
        tp[v], bp[v] = z3.And(p[v], t[partner]), z3.And(p[v], blank(partner))
        for sign in (-1, 1):
            guard = z3.And(tp[v], owner[v] == 1, not free_alpha_ports)
            if 0 <= c+sign < cols:
                solver.add(z3.Implies(guard, z3.Not(bb(r, c+sign))))
                if extra_owners:
                    solver.add(z3.Implies(z3.And(guard, p[r, c+sign]), owner[r, c+sign] == 3))
            if 0 <= c+2*sign < cols:
                cap = z3.And(t[r, c+sign], blank((r ^ 1, c+sign)), bb(r, c+2*sign))
                solver.add(z3.Implies(guard, z3.Not(cap)))
    for label in (1, 2, 3):
        solver.add(count(z3.And(tp[v], owner[v] == label) for v in points) == (0 if label == 3 else 2))
        solver.add(count(z3.And(bp[v], owner[v] == label) for v in points) == (2 if label == 3 else 0))
    row, col = 5, cols//2
    payment_tip = ((row, col+3) if placement == 'same-band' else
                   (9, col+1) if placement == 'separated' else None)
    for v, label in [((row, col-1), 1), ((row, col), 3),
                     ((row, col+1), 2)]+([(payment_tip, 2)] if payment_tip is not None else []):
        solver.add(p[v], owner[v] == label)
    solver.add(t[row-1, col-1], t[row-1, col+1], blank((row-1, col)))
    if placement == 'same-band':
        solver.add(t[row-1, col+3], bb(row, col+2))
    elif placement == 'separated':
        solver.add(t[8, col+1], bb(9, col+2), t[8, col+3], blank((9, col+3)))
    started = time.monotonic()
    status = solver.check()
    receipt = dict(status=str(status), reason=solver.reason_unknown(),
                   rows=rows, cols=cols, timeout_seconds=seconds,
                   placement=placement,
                   extra_owners=extra_owners,
                   free_alpha_ports=free_alpha_ports,
                   alpha_one_links_only_to_beta_three=extra_owners and not free_alpha_ports,
                   elapsed_seconds=time.monotonic()-started,
                   scope='Optional bounded discovery; UNKNOWN is not UNSAT.')
    print(json.dumps(receipt), flush=True)
    if status == z3.sat:
        model = solver.model()
        selected = {v for v in points if z3.is_true(model.eval(t[v]))}
        matching = [e for e in edges if z3.is_true(model.eval(m[e]))]
        current = rows, cols, selected, matching
        direct_check(*current)
        frozen, layers = frozen_certificate(current)
        assert frozen == {v for e in matching for v in e}
        bands = whole_bands(current)
        original, labels, intervals, interval_owner, kinds, pairs, ports = terminal_data(current, bands)
        if not extra_owners:
            assert (original['alpha'], original['beta'], original['gamma']) == (2, 1, 0)
        extended = extended_ports(current, bands, labels, intervals, interval_owner, kinds, ports, Counter())
        a_tip = row, col-1
        a_pair = next(pair for pair in pairs if a_tip in pair)
        if not free_alpha_ports:
            assert all(not extended[tip] for tip in a_pair)
        payload = dict(shape=[rows, cols], selected=sorted(selected), matching=matching,
                       freezing_layers=[[entry['endpoint'] for entry in layer] for layer in layers],
                       intended_core_link=[(row, col+1), (row, col)],
                       exchange_link=[a_tip, (row, col)], payment_tip=payment_tip,
                       discovery=receipt)
        if extra_owners:
            from check_beta_exchange_gate_reduction import compile_and_lift, physical_data, protected_value
            data = physical_data(current)
            core = [((row, col+1), (row, col))]
            result = compile_and_lift(*data, core)
            protected = protected_value(*data, core)
            payload['exchange_verification'] = dict(full_value=result['full_value'],
                protected_value=protected, alpha=original['alpha'],
                used_exchange_gates=result['used_exchange_gates'],
                selected_links=result['selected_links'], payments=result['payments'])
            print(json.dumps(payload['exchange_verification']), flush=True)
        output.write_text(json.dumps(payload, indent=2)+'\n')
        print('Verified SAT fixture saved:', output, flush=True)
    else:
        output.write_text(json.dumps(receipt, indent=2)+'\n')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows', type=int, required=True)
    parser.add_argument('--cols', type=int, required=True)
    parser.add_argument('--seconds', type=int, default=60)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--placement', choices=('same-band', 'separated', 'free'), default='separated')
    parser.add_argument('--extra-owners', action='store_true')
    parser.add_argument('--free-alpha-ports', action='store_true')
    args = parser.parse_args()
    search(args.rows, args.cols, args.seconds, args.output, args.placement,
           args.extra_owners, args.free_alpha_ports)
