"""Retained-occupation extensions with new selections: a precise defect budget.

General proofs are in SELECTED_EXTENSIONS_AND_NEW_TP_DEFECT_BUDGET.md.
Finite controls corroborate, and do not replace, the arbitrary-size argument.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import random

from check_endpoint_extension_replacement import FLEX, static_certificate, augment
from check_frozen_mixed_gate_cycle import load_model
from check_occupancy_certificate_all_rematchings import canon, switches
from check_cooperative_promotion import neighbors
from check_merger_completion_reserves import feasible, frozen, owner_data, whole_bands, whole_support_data
from check_partial_tip_compensation import lift
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_reserve_boundary_split import clipped
from check_whole_support_fork_normal_form import ordinary_flow, optimize
from check_whole_support_fork_flow import fork_flow
from check_frozen_tip_slot_obstruction import matching

if not __debug__:
    raise RuntimeError('Assertions are required; do not use -O.')


def endpoints(cur):
    return {v for e in cur[3] for v in e}


def selectable(cur):
    occupied = cur[2] | endpoints(cur)
    return [(r, c) for r in range(cur[0]) for c in range(1, cur[1])
            if (r, c) not in occupied and feasible((*cur[:2], cur[2] | {(r, c)}, cur[3]))]


def inspect(base, cur, old, totals, independent=False):
    assert feasible(cur) and base[2] <= cur[2] and endpoints(base) <= endpoints(cur)
    P = endpoints(cur)
    d, meta, _ = whole_support_data(cur, whole_bands(cur))
    owner, aa, bb, _ = owner_data(*d[:2])
    old_tips = set(old.values()) | {v for v, _ in FLEX}
    tips = {v for v, k in d[0].items() if k == 'TP'}
    assert old_tips <= tips
    new_tips = tips - old_tips
    assert len(new_tips) <= len(cur[2] - base[2])
    assert all((v[0] ^ 1, v[1]) in cur[2] - base[2] for v in new_tips)
    assignment = dict(old)
    pool = set()
    h = 0
    for v, u in FLEX:
        q = (u[0] ^ 1, u[1])
        assert u not in cur[2] and q not in cur[2] | P
        if u in P:
            assignment['bp', u] = v
            h += 1
        else:
            j = meta['owner'][u[0] // 2, u[1]]
            # Simultaneous TT is impossible, even where either site alone
            # is selectable. The surviving units are still SINGLETONS.
            assert meta['intervals'][j] == dict(band=u[0] // 2, first=u[1], last=u[1])
            assert j in d[4] and j not in pool
            pool.add(j)
            assignment['interval', j, 0] = v
    assert len(assignment) == 23 and set(assignment.values()) == old_tips
    links = [(v, t[1]) for t, v in assignment.items() if t[0] == 'bp']
    _, inventory, records = cancel_pairs(d[0], d[1], links, Counter())
    final_alphas = [c for c in records if not c['cycle'] and c['alpha'] == c['beta'] + 1]
    k = sum(set(c['ends']) <= new_tips for c in final_alphas)
    r, delta = 5 - h, len(new_tips)
    paid_intervals = len(final_alphas) - k
    assert 2*k <= delta and paid_intervals <= min(r, (r + delta)//2)
    assert len(aa) + inventory['BP', 'BP'] == len(bb) + len(final_alphas)
    lifted = lift(clipped(d, pool), assignment)
    assert lifted['holes'] == delta and lifted['certified_deficit'] == k
    assert lifted['certified_payment'] + k == len(aa)
    if k:
        # Repair only by different NEW units with a witness at a FREE new
        # TP end. This does not spend a beta-body support as an ordinary stem.
        unresolved = [c for c in final_alphas if set(c['ends']) <= new_tips]
        choices = {}
        for i, c in enumerate(unresolved):
            choices[i] = {('interval', meta['owner'][port], 0)
                          for v in c['ends'] for port in meta['all_ports'][v]
                          if meta['owner'][port] in d[4] - pool}
        repair = matching(choices)
        totals['new_end_repair_matchings'] += 1
        if len(repair) == k:
            extended = dict(assignment)
            for target, i in repair.items():
                j = target[1]
                v = next(v for v in unresolved[i]['ends']
                         if any(meta['owner'][port] == j for port in meta['all_ports'][v]))
                assert target not in extended
                extended[target] = v
            new_pool = pool | {t[1] for t in repair}
            result = lift(clipped(d, new_pool), extended)
            assert result['certified_deficit'] == 0
            assert ordinary_flow(*clipped(d, new_pool))['deficit'] == 0
            totals['disjoint_new_resource_repairs'] += 1
    selected_data = (d[0], d[1], links, d[3], pool)
    witness = ordinary_flow(*selected_data)
    assert witness['value'] >= len(aa) - k and witness['cost'] <= 18 + h
    restricted = clipped(d, pool)
    ordinary, full = ordinary_flow(*restricted), fork_flow(*restricted)
    assert ordinary['deficit'] <= k and full['deficit'] <= ordinary['deficit']
    if k == 0:
        assert ordinary['value'] == full['value'] == len(aa)
        assert full['cost'] <= ordinary['cost'] <= 18 + h
    if delta <= 1:
        assert k == 0
    if P == endpoints(base):
        assert delta <= 1 and new_tips <= {(3, 14)}
    if independent:
        for forks in (False, True):
            exact = optimize(*restricted, allow_forks=forks)
            expected = full if forks else ordinary
            assert (exact['value'], exact['cost']) == (expected['value'], expected['cost'])
            totals['independent_primitive_comparisons'] += 1
    is_frozen = frozen(cur)
    totals['models'] += 1
    totals['frozen' if is_frozen else 'feasible_nonfrozen'] += 1
    totals['positive_new_tp_models'] += delta > 0
    totals['positive_exact_certificate_loss'] += k > 0
    totals['complete_certificates'] += k == 0
    return dict(shape=cur[:2], selected=len(cur[2]), new_selected=len(cur[2]-base[2]), endpoints=len(P), alpha=len(aa), beta=len(bb),
                new_tp=delta, filled_candidates=h, surviving_units=r,
                residual_alpha=len(final_alphas), interval_payments=paid_intervals,
                exact_certificate_loss=k, restricted_deficit=ordinary['deficit'],
                full_pool_deficit=ordinary_flow(*d)['deficit'], frozen=is_frozen)


def sharp_family(base, count):
    """Separated vertical TP--TP owners; reserve all of their new units."""
    T = base[2] | {(30 + 6*i + dr, 3) for i in range(count) for dr in (0, 3)}
    M = base[3] + [((31 + 6*i, 3), (32 + 6*i, 3)) for i in range(count)]
    return 36 + 6*count, 30, T, M


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    base, *_ = load_model()
    old, _ = static_certificate(base)
    totals, named = Counter(), {}
    rng = random.Random(2026102571)
    candidates = selectable(base)
    assert len(candidates) == 155
    promotable = [(r, c) for r, c in candidates if (r ^ 1, c) in endpoints(base)]
    assert promotable == [(2, 14)]
    # Every single new selection in the old rectangle, plus arbitrary-M controls.
    for i, s in enumerate(candidates):
        cur = (*base[:2], base[2] | {s}, base[3])
        info = inspect(base, cur, old, totals, independent=i < 16)
        if s == (2, 14):
            named['unique_old_endpoint_promotion'] = info
        M = canon(base[3])
        for _ in range(2):
            _, M = rng.choice(list(switches(M)))
        inspect(base, (*cur[:3], sorted(M)), old, totals)
        totals['single_new_selection_models'] += 2
    # Joint additions: checking sites independently is not a joint feasibility test.
    for trial in range(64):
        cur = base
        order = list(candidates)
        rng.shuffle(order)
        if trial % 2 == 0:
            order.remove((2, 14))
            order.insert(0, (2, 14))
        for s in order[:20 + trial]:
            nxt = (*cur[:2], cur[2] | {s}, cur[3])
            if feasible(nxt):
                cur = nxt
        M = canon(cur[3])
        for _ in range(4):
            _, M = rng.choice(list(switches(M)))
        cur = (*cur[:3], sorted(M))
        inspect(base, cur, old, totals, independent=trial < 8)
        totals['joint_selected_only_models'] += 1
    # New endpoints and selections simultaneously; recompute every resource.
    for mask in range(32):
        cur = base
        for i, (_, u) in enumerate(FLEX):
            if mask >> i & 1 and u not in endpoints(cur):
                cur = augment(cur, u)
        # One new selection is harmless for ANY endpoint extension: d<=s=1.
        options = selectable(cur)
        partner_is_new_p = [s for s in options if (s[0] ^ 1, s[1]) in endpoints(cur)-endpoints(base)]
        s = (partner_is_new_p or [(2, 14)])[0]
        one = (*cur[:2], cur[2] | {s}, cur[3])
        inspect(base, one, old, totals, independent=mask < 4)
        totals['single_selection_endpoint_extension_models'] += 1
        order = selectable(cur)
        rng.shuffle(order)
        for s in order[:40]:
            nxt = (*cur[:2], cur[2] | {s}, cur[3])
            if feasible(nxt):
                cur = nxt
        info = inspect(base, cur, old, totals, independent=True)
        named['joint_fill_' + str(mask)] = info
        totals['joint_endpoint_selection_models'] += 1
    # Test the candidate/TT exclusions as JOINT configurations, not separate sites.
    exclusions = []
    for v, u in FLEX:
        assert not feasible((*base[:2], base[2] | {u}, base[3]))
        for c in (u[1]-1, u[1]+1):
            tt = {(2*(u[0]//2), c), (2*(u[0]//2)+1, c)}
            assert not feasible((*base[:2], base[2] | tt, base[3]))
        exclusions.append(dict(source=v, candidate=u,
                               retained_endpoint_neighbors=sorted(set(neighbors(u)) & endpoints(base))))
    # An unbounded sharp family for the OLD-RESERVE rule, not a counterexample
    # to compensation with all final resources or to a frozen-only conjecture.
    for count in range(1, 13):
        cur = sharp_family(base, count)
        info = inspect(base, cur, old, totals, independent=count <= 3)
        assert info['new_tp'] == 2*count and info['exact_certificate_loss'] == count
        assert info['restricted_deficit'] == count and info['full_pool_deficit'] == 0
        assert not info['frozen']
        named['sharp_reserved_family_' + str(count)] = info
        totals['sharp_family_models'] += 1
        if count == 1:
            Path('develop/fixtures/selected_extension_reserved_obstacle.json').write_text(json.dumps(dict(
                shape=cur[:2], selected=sorted(cur[2]), matching=cur[3], completely_frozen=False,
                available_rule='ONLY five surviving old certificate units; all other final units reserved',
                new_tp=[(31, 3), (32, 3)], actual_restricted_deficit=1,
                full_pool_deficit=0, scope='Feasible NONFROZEN reserved-pool obstruction; NOTuniversalCompensationCounterexample'), indent=2)+'\n')
    result = dict(status='PASS', totals=dict(totals), original_single_selectable_sites=155,
                  unique_promotable_old_endpoint=(3, 14), candidate_exclusions=exclusions, named=named,
                  scope='ANY feasible finite extension retaining old49T and308P; arbitrary addedT/P and arbitraryM. Old23TP adaptive certificate persists with singleton units. DeltaNewTP holes; exact certificate loss k equals postC alpha paths with TWOnewTPends; 2kLEdeltaLEnewSelections. Full ordinary if k0, especially deltaLE1, hence atMostOneNewSelection with ANYnewP. Fixed oldP arbitraryTextensions ALWAYSfull. Sharp feasible NONFROZEN family disproves ONLYoldReserve sufficiency, fullPool remains complete. Universal frozen compensation and5over6 OPEN.')
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals), promotion=named['unique_old_endpoint_promotion'],
                          sharp=named['sharp_reserved_family_1'])))


if __name__ == '__main__':
    main()
