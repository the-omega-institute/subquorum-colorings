"""Actual connected frozen boards: joint use of seam resources and beta reserves.

The arbitrary-size argument is in FROZEN_SHARED_SEAM_COMPENSATION.md.
Controls check physical identities, exhaustive small reservation states, and
independent primitive packing, not an inference from bounded enumeration.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_connected_frozen_interval_repair_obstacle import (
    build, connected, lifted_rank, load_model, owner_data, prelude, shift,
    whole_bands, whole_support_data,
)
from check_frozen_beta_support_fork import restrict
from check_merger_completion_reserves import feasible
from check_partial_tip_compensation import live_prune
from check_whole_support_fork_normal_form import ordinary_flow, optimize, primitive_certificates
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def interface(data, meta, q):
    owner, aa, bb, mm = owner_data(*data[:2])
    seams = []
    for i in range(q):
        units = {meta['owner'][12, 23+24*i], meta['owner'][12, 24+24*i]}
        assert len(units) == 2 and units <= data[4]
        for col in (23+24*i, 24+24*i):
            j = meta['owner'][12, col]
            assert meta['intervals'][j] == dict(band=12, first=col, last=col)
        gates = {owner[shift((24, 20), i)], owner[shift((24, 2), i+1)]}
        assert gates <= mm and len(gates) == 2
        for j in units:
            assert {o for o, js in data[3].items() if j in js} == gates
        seams.append(dict(units=units,
            sources=(owner[shift((24, 19), i)], owner[shift((24, 4), i+1)]),
            reserves=(owner[shift((5, 20), i)], owner[shift((5, 3), i+1)])))
    assert len(set().union(*(s['units'] for s in seams))) == 2*q
    assert len({b for s in seams for b in s['reserves']}) == 2*q
    # No beta body has access to the tested interval pool, hence no forks.
    Q = set().union(*(s['units'] for s in seams))
    assert all(not data[3][b] & Q for b in bb)
    pruned, live = live_prune(data)
    live_owners = aa | bb | set(live['live_mixed'])
    shared_live = set()
    for j in data[4]:
        users = {o for o in live_owners if j in data[3][o]}
        copies = {data[1][o][0][1]//24 for o in users}
        if len(copies) > 1:
            shared_live.add(j)
    assert shared_live == Q
    return seams, Q, live


def check_routes(data, Q, q):
    """Enumerate simple routes once; compare to the written complete table."""
    owner, aa, bb, mm = owner_data(*data[:2])
    ps = primitive_certificates(*restrict(data, set(range(len(data[1]))), Q))
    assert not any(p['kind'] == 'fork' for p in ps)
    for i in range(q+1):
        top = owner[shift((5, 17), i)]
        left = owner[shift((5, 4), i)]
        right = owner[shift((5, 19), i)]
        bottom = owner[shift((24, 17), i)]
        expected = {
            top: {(owner[shift((5, 7), i)], 1), (owner[shift((5, 16), i)], 1)},
            left: {(owner[shift((5, 3), i)], 1)},
            right: {(owner[shift((5, 20), i)], 1), (owner[shift((18, 16), i)], 2)},
            bottom: {(owner[shift((18, 16), i)], 2)},
        }
        for a, targets in expected.items():
            actual = {(p['beta'], len(p['links'])) for p in ps
                      if p['kind'] == 'beta' and a in p['owners']}
            assert actual == targets
        for a in (top, bottom):
            assert not any(p['kind'] == 'interval' and a in p['owners'] for p in ps)
        for a in (left, right):
            actual = [p for p in ps if p['kind'] == 'interval' and a in p['owners']]
            expected_units = set()
            for j in Q:
                # Only the incident seam, never a remote resource.
                col = shift((24, 4 if a == left else 19), i)[1]
                expected_gate = owner[(24, col-2 if a == left else col+1)]
                if j in data[3][expected_gate]:
                    expected_units.add(j)
            assert {p['interval'] for p in actual} == expected_units
            assert all(len(p['links']) == 1 for p in actual)


def check_state(data, seams, states, totals, independent=False):
    removed, Q = set(), set()
    deficiency = 0
    local = []
    for s, (reserve_mask, unit_mask) in zip(seams, states):
        removed |= {b for i, b in enumerate(s['reserves']) if reserve_mask >> i & 1}
        chosen = {j for i, j in enumerate(sorted(s['units'])) if unit_mask >> i & 1}
        Q |= chosen
        r = reserve_mask.bit_count()
        deficiency += max(0, r-len(chosen))
        local.append((r, len(chosen)))
    dd = restrict(data, set(range(len(data[1])))-removed, Q)
    n = len(seams)+1
    expected = (4*n-deficiency, 5*n-deficiency)
    a, b = ordinary_flow(*dd), fork_flow(*dd)
    assert (a['value'], a['cost']) == (b['value'], b['cost']) == expected
    totals['reservation_models'] += 1
    totals['ordinary_full_comparisons'] += 1
    totals['positive_deficit_models'] += deficiency > 0
    totals['naive_independent_credit_overcounts'] += any(r == 2 and z == 1 for r, z in local)
    if independent:
        c = optimize(*dd)
        assert (c['value'], c['cost']) == expected
        totals['independent_primitive_packs'] += 1


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', default='output/frozen-shared-seam-validation.json')
    args = parser.parse_args()
    base, *_ = load_model()
    prefix, _ = prelude(base)
    rng = random.Random(20261025)
    totals, families = Counter(), []
    options = list(itertools.product(range(4), repeat=2))
    for q in range(1, 13):
        cur = build(base, q)
        assert feasible(cur) and connected(cur)
        lifted_rank(base, cur, q, prefix)
        data, meta, _ = whole_support_data(cur, whole_bands(cur))
        seams, Q, live = interface(data, meta, q)
        check_routes(data, Q, q)
        if q <= 2:
            states = list(itertools.product(options, repeat=q))
        else:
            states = [tuple(rng.choice(options) for _ in range(q)) for _ in range(12)]
        # Every seam: both old side betas reserved, one original unit opened.
        states.append(tuple((3, 1) for _ in range(q)))
        # Both distinct units repair every seam simultaneously.
        states.append(tuple((3, 3) for _ in range(q)))
        for i, state in enumerate(states):
            check_state(data, seams, state, totals,
                        independent=(q == 1 or (q == 2 and (i % 32 == 0 or i >= 256))))
        totals['connected_frozen_families'] += 1
        families.append(dict(q=q, endpoints=2*len(cur[3]), live_shared_intervals=len(Q),
                             states=len(states), removed_mixed=len(live['removed_mixed'])))
    report = dict(status='PASS', counts=dict(totals), families=families,
        theorem='Any q>=1; original seam identities, reserved whole side-beta owners, '
                'only seam interval pool: D=sum max(0,r_i-z_i), Vord=Vfull=4(q+1)-D, '
                'cord=cfull=5(q+1)-D. Full unrestricted board remains compensated.',
        scope='Finite controls corroborate arbitrary-q written proof; not a universal grid theorem.')
    Path(args.output).write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', counts=dict(totals))))


if __name__ == '__main__':
    main()
