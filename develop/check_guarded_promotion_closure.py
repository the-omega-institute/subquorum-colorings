"""Guarded promotion closure: only TPs on genuinely added P remain holes.

The arbitrary-extension proof is in GUARDED_PROMOTION_CLOSURE.md.
Finite controls check the physical certificate under simultaneous promotion,
endpoint addition and rematching, with final original resource identities.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_connected_frozen_interval_repair_obstacle import build, connected, load_model, shift
from check_endpoint_extension_replacement import FLEX, augment, static_certificate
from check_selected_extension_budget import endpoints, selectable, sharp_family
from check_merger_completion_reserves import feasible, frozen, owner_data, whole_bands, whole_support_data
from check_cooperative_promotion import neighbors
from check_partial_tip_compensation import lift
from check_reserve_boundary_split import clipped
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import ordinary_flow, optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def base_copies(base, n):
    return base if n == 1 else build(base, n-1)


def square_switches(current):
    """All squares in the FINAL rectangle, including physical seams."""
    mate = {v: w for e in current[3] for v, w in (e, e[::-1])}
    M = {tuple(sorted(e)) for e in current[3]}
    for r, c in sorted(mate):
        a, b, d, e = (r, c), (r, c+1), (r+1, c), (r+1, c+1)
        h = {tuple(sorted(x)) for x in [(a,b),(d,e)]}
        v = {tuple(sorted(x)) for x in [(a,d),(b,e)]}
        if h <= M:
            yield (r,c), (*current[:3], sorted(M-h|v))
        elif v <= M:
            yield (r,c), (*current[:3], sorted(M-v|h))


def local_audit(base):
    P = endpoints(base)
    O = P | base[2]
    allowed, exclusions = [], []
    for v in sorted(P):
        q = (v[0]^1, v[1])
        if q in base[2] | P:
            continue
        blockers = sorted(set(neighbors(q)) & O)
        assert v in blockers
        if len(blockers) == 1:
            allowed.append(v)
        else:
            assert len(blockers) >= 2
            exclusions.append(dict(endpoint=v, partner=q, occupied_blockers=blockers[:2]))
    assert allowed == [(3,14)]
    old, _ = static_certificate(base)
    assert ('bp', (3,13)) not in old
    assert (3,13) not in {u for _,u in FLEX}
    assert (3,13) in P and (3,14) in P
    return dict(unique_promotable_old_endpoint=(3,14), fresh_old_bp_target=(3,13),
                new_selected_guard=(2,14), forced_blank=(2,13), exclusions=exclusions)


def inspect(base, initial, current, n, totals, independent=False, full_pool=False):
    assert feasible(current) and initial[2] <= current[2]
    P0, P = endpoints(initial), endpoints(current)
    assert P0 <= P
    data, meta, _ = whole_support_data(current, whole_bands(current))
    owner, aa, bb, _ = owner_data(*data[:2])
    tips = {v for v,k in data[0].items() if k == 'TP'}
    old, _ = static_certificate(base)
    assignment, pool = {}, set()
    h = p = 0
    for i in range(n):
        for target, source in old.items():
            assignment['bp', shift(target[1],i)] = shift(source,i)
        for source, candidate in FLEX:
            v, u = shift(source,i), shift(candidate,i)
            q = (u[0]^1,u[1])
            assert q not in current[2] | P and u not in current[2]
            if u in P:
                assignment['bp',u] = v
                h += 1
            else:
                j = meta['owner'][u[0]//2,u[1]]
                assert meta['intervals'][j] == dict(band=u[0]//2,first=u[1],last=u[1])
                assert j in data[4] and j not in pool
                assignment['interval',j,0] = v
                pool.add(j)
        guard, source, target, blank = [shift(v,i) for v in [(2,14),(3,14),(3,13),(2,13)]]
        if guard in current[2]:
            assert blank not in current[2] | P
            assert data[0][source] == 'TP' and data[0][target] == 'BP'
            assert (source,target) in data[2] and ('bp',target) not in assignment
            assignment['bp',target] = source
            p += 1
    covered = set(assignment.values())
    promoted = tips & P0 - {shift(v,i) for i in range(n) for v in old.values()} - {
        shift(v,i) for i in range(n) for v,_ in FLEX}
    assert promoted == {shift((3,14),i) for i in range(n) if shift((2,14),i) in current[2]}
    fresh = tips-P0
    assert tips-covered == fresh
    assert len(assignment) == len(covered) == 23*n+p
    assert len(pool) == 5*n-h
    C = [(v,t[1]) for t,v in assignment.items() if t[0] == 'bp']
    assert len(C) == 18*n+h+p
    _, inventory, records = cancel_pairs(*data[:2], C, Counter())
    final_alphas = [r for r in records if not r['cycle'] and r['alpha'] == r['beta']+1]
    k = sum(set(r['ends']) <= fresh for r in final_alphas)
    r, e = 5*n-h, len(fresh)
    used = len(final_alphas)-k
    assert 2*k <= e and used <= min(r,(r+e)//2)
    assert e+p <= len(current[2]-initial[2])
    assert len(aa)+inventory['BP','BP'] == len(bb)+len(final_alphas)
    dd = clipped(data,pool)
    lifted = lift(dd,assignment)
    assert lifted['holes'] == e and lifted['certified_deficit'] == k
    assert lifted['certified_payment'] == len(aa)-k
    ordinary, full = ordinary_flow(*dd), fork_flow(*dd)
    assert full['deficit'] <= ordinary['deficit'] <= k
    if e <= 1:
        assert k == ordinary['deficit'] == full['deficit'] == 0
        assert full['cost'] <= ordinary['cost'] <= 18*n+h+p
    if independent:
        for forks in (False,True):
            answer = optimize(*dd,allow_forks=forks)
            flow = full if forks else ordinary
            assert (answer['value'],answer['cost']) == (flow['value'],flow['cost'])
            totals['independent_primitive_comparisons'] += 1
    is_frozen = frozen(current)
    totals['models'] += 1
    totals['frozen' if is_frozen else 'feasible_nonfrozen'] += 1
    totals['promotion_active_models'] += p > 0
    totals['old_bound_strictly_improved'] += e//2 < (p+e)//2
    totals['positive_fresh_tip_models'] += e > 0
    totals['complete_retained_certificate_models'] += k == 0
    result = dict(copies=n,promoted_retained_tips=p,fresh_endpoint_tips=e,
        covered_tips=len(covered),filled_candidates=h,surviving_units=r,
        alpha=len(aa),beta=len(bb),exact_certificate_loss=k,ordinary_deficit=ordinary['deficit'],
        ordinary_cost=ordinary['cost'],frozen=is_frozen,selected=len(current[2]),endpoints=len(P))
    if full_pool:
        result['full_pool_deficit'] = ordinary_flow(*data)['deficit']
    return result


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output',default='output/guarded-promotion-closure-validation.json')
    args = parser.parse_args()
    base,*_ = load_model()
    audit = local_audit(base)
    totals, named = Counter(), {}
    rng = random.Random(20261025107)
    # Unbounded theorem is written. These include arbitrary simultaneous
    # promotions, extra harmless selections, and actual matching changes.
    for n in range(1,13):
        initial = base_copies(base,n)
        assert connected(initial)
        masks = list(range(1<<n)) if n <= 4 else [0,(1<<n)-1]+[rng.randrange(1<<n) for _ in range(6)]
        for mi,mask in enumerate(masks):
            added = {shift((2,14),i) for i in range(n) if mask>>i&1}
            cur = (*initial[:2],initial[2]|added,initial[3])
            info = inspect(base,initial,cur,n,totals,independent=(n==1 or (n==2 and mi<2)))
            assert info['frozen'] and info['fresh_endpoint_tips'] == 0
            if mask == (1<<n)-1:
                named['all_promotions_'+str(n)] = info
            for _ in range(2):
                sq,cur = rng.choice(list(square_switches(cur)))
                inspect(base,initial,cur,n,totals)
                totals['rematched_models'] += 1
                totals['switches_outside_first_copy'] += sq[1] >= 23
    for mask in range(32):
        cur = base
        for i,(_,u) in enumerate(FLEX):
            if mask>>i&1 and u not in endpoints(cur):
                cur = augment(cur,u)
        cur = (*cur[:2],cur[2]|{(2,14)},cur[3])
        assert feasible(cur)
        inspect(base,base,cur,1,totals,independent=mask<4)
        choices = [t for t in selectable(cur) if (t[0]^1,t[1]) in endpoints(cur)-endpoints(base)]
        if choices:
            t = choices[0]
            cur = (*cur[:2],cur[2]|{t},cur[3])
            info = inspect(base,base,cur,1,totals,independent=mask in (4,16))
            assert info['fresh_endpoint_tips'] == 1 and info['promoted_retained_tips'] == 1
            if mask == 4:
                assert info['frozen']
                named['frozen_310P_two_new_T_two_new_TP'] = info
                from check_promotion_cores import frozen_certificate
                from check_frozen_shared_mixed_gate import check_rank_certificate
                _,layers = frozen_certificate(cur)
                check_rank_certificate(cur,[[x['endpoint'] for x in layer] for layer in layers])
                Path('develop/fixtures/guarded_promotion_fresh_tip_frozen.json').write_text(json.dumps(dict(
                    shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],
                    completely_frozen=True,freezing_layers=[[x['endpoint'] for x in layer] for layer in layers],
                    promoted_old_tp=(3,14),fresh_tp=(19,9),new_selected=[(2,14),(18,9)]),separators=(',',':'))+'\n')
    # Joint unrestricted selections do not create other old-P promotions.
    for trial in range(12):
        n = 1+trial%2
        initial = base_copies(base,n)
        cur = (*initial[:2],initial[2]|{shift((2,14),i) for i in range(n)},initial[3])
        options = selectable(cur)
        rng.shuffle(options)
        for t in options[:50]:
            nxt = (*cur[:2],cur[2]|{t},cur[3])
            if feasible(nxt):
                cur = nxt
        inspect(base,initial,cur,n,totals,independent=trial<2)
        totals['many_new_selection_models'] += 1
    # A sharp NONFROZEN reserved-pool family. Promotions do not count as
    # fresh holes; all loss is from the two new endpoints of each gadget.
    for j in range(1,9):
        cur = sharp_family(base,j)
        cur = (*cur[:2],cur[2]|{(2,14)},cur[3])
        info = inspect(base,base,cur,1,totals,independent=j<=2,full_pool=True)
        assert info['fresh_endpoint_tips'] == 2*j and info['exact_certificate_loss'] == j
        assert info['ordinary_deficit'] == j and info['full_pool_deficit'] == 0
        assert not info['frozen']
        named['sharp_reserved_'+str(j)] = info
    report = dict(status='PASS',counts=dict(totals),fixture_rank_independent_check='PASS310P',local_audit=audit,named=named,
        theorem='Every feasible retained-T/P extension of any number of PP-connected copies, '
          'with arbitrary actual rematching: all retained-P TP promotions have fresh guarded BP '
          'assignments. Only e TP on genuinely added P are holes; exact retained-strategy loss k '
          '<=floor(e/2)<=floor((newT-p)/2). e<=1 implies full ordinary compensation.',
        scope='General proof is written; finite controls corroborate. Sharp restricted-pool '
          'gadgets are NONFROZEN and full-pool compensated. Universal5/6 remains open.')
    Path(args.output).write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals),example=named['frozen_310P_two_new_T_two_new_TP'])))


if __name__ == '__main__':
    main()
