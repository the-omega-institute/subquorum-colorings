"""Connected frozen extensions obstruct interval-only repair of new-new alphas.

An explicit PP splice and rank replay prove the all-copy construction.
Finite controls validate that proof's concrete data, not its unbounded scope.
"""
import argparse
from collections import Counter
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_frozen_mixed_gate_cycle import load_model
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_merger_completion_reserves import feasible, whole_bands, whole_support_data, owner_data
from check_endpoint_extension_replacement import static_certificate, FLEX
from check_partial_tip_compensation import lift
from check_promotion_cores import frozen_certificate
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_frozen_tip_slot_obstruction import matching
from check_occupied_strip_matching_flux import matchings
from check_reserve_boundary_split import clipped
from check_whole_support_fork_normal_form import ordinary_flow, optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Run without -O: assertions are required.')

BOUNDARY = {(r, c) for r in (2, 3) for c in (1, 22)}
shift = lambda v, i: (v[0], v[1]+24*i)
canon = lambda e: tuple(sorted(e))


def prelude(base):
    """Freeze only endpoints outside the four sites whose mates may change."""
    mate = {v: w for e in base[3] for v, w in (e, e[::-1])}
    frozen, layers = set(), []
    while True:
        kept = base[2] | {v for v in mate if mate[v] in frozen}
        new = {v for v in mate if v not in frozen | BOUNDARY
               and len(set(neighbors(v)) & kept) >= 2}
        if not new:
            break
        layers.append(sorted(new))
        frozen |= new
    assert len(frozen) == 112 and len(layers) == 27
    kept = base[2] | {v for v in mate if mate[v] in frozen}
    witnesses = []
    for v in sorted(BOUNDARY):
        nn = sorted(set(neighbors(v)) & kept)
        assert len(nn) >= 2
        witnesses.append(dict(endpoint=v, witnesses=nn[:2]))
    return layers, witnesses


def build(base, q):
    assert q >= 1
    T = {shift(v, i) for i in range(q+1) for v in base[2]}
    M = [(shift(v, i), shift(w, i)) for i in range(q+1) for v, w in base[3]]
    for i in range(q):
        c = 22+24*i
        old = {canon(((2, c), (3, c))), canon(((2, c+3), (3, c+3)))}
        assert old <= {canon(e) for e in M}
        M = [e for e in M if canon(e) not in old]
        # Four new endpoints; the two old vertical PP edges are replaced by
        # four horizontal edges on the two rows. The entire patch stays PP.
        M += [((r, c+j), (r, c+j+1)) for r in (2, 3) for j in (0, 2)]
    return 28, 24*(q+1), T, M


def lifted_rank(base, cur, q, prefix):
    """A universal construction from the old rank, not a new freezing search."""
    old_frozen, original = frozen_certificate(base)
    assert len(old_frozen) == 308
    layers = [[shift(v, i) for i in range(q+1) for v in layer] for layer in prefix]
    boundary = {shift(v, i) for i in range(q+1) for v in BOUNDARY}
    layers.append(sorted(boundary))
    layers.append([(r, c+24*i) for i in range(q) for r in (2, 3) for c in (23, 24)])
    already = {v for layer in layers for v in layer}
    for layer in original:
        new = [shift(row['endpoint'], i) for i in range(q+1) for row in layer
               if shift(row['endpoint'], i) not in already]
        if new:
            layers.append(new)
            already.update(new)
    assert len(already) == 308*(q+1)+4*q
    # Independent coordinate/rank checker verifies every strict dependency.
    check_rank_certificate(cur, layers)
    return layers


def connected(cur):
    occupied = cur[2] | {v for e in cur[3] for v in e}
    root = min(occupied)
    seen, todo = {root}, [root]
    while todo:
        v = todo.pop()
        for w in set(neighbors(v)) & occupied - seen:
            seen.add(w)
            todo.append(w)
    return len(seen) == len(occupied)


def inspect(base, cur, q, totals, independent=False):
    assert feasible(cur) and connected(cur)
    P = {v for e in cur[3] for v in e}
    assert len(P) == 308+312*q and len(cur[2]) == 49*(q+1)
    old, _ = static_certificate(base)
    d, meta, _ = whole_support_data(cur, whole_bands(cur))
    owner, aa, bb, mm = owner_data(*d[:2])
    assert (len(aa), len(bb), len(mm)) == (4*(q+1), 6*(q+1), 15*(q+1))
    assignment = dict(old)
    pool = set()
    for v, u in FLEX:
        assert u not in cur[2] | P
        j = meta['owner'][u[0]//2, u[1]]
        assert meta['intervals'][j] == dict(band=u[0]//2, first=u[1], last=u[1])
        assignment['interval', j, 0] = v
        pool.add(j)
    C = [(v, t[1]) for t, v in assignment.items() if t[0] == 'bp']
    _, inv, records = cancel_pairs(*d[:2], C, Counter())
    old_tips = set(assignment.values())
    new_tips = {v for v, k in d[0].items() if k == 'TP'}-old_tips
    assert len(new_tips) == 23*q
    residual = [r for r in records if not r['cycle'] and r['alpha'] == r['beta']+1
                and set(r['ends']) <= new_tips]
    assert len(residual) == 4*q
    result = lift(clipped(d, pool), assignment)
    assert result['certified_deficit'] == 4*q
    direct, broad = {}, {}
    for i, record in enumerate(residual):
        direct[i] = {('i', meta['owner'][port]) for v in record['ends']
                     for port in meta['all_ports'][v] if meta['owner'][port] in d[4]-pool}
        broad[i] = {('i', j) for v in record['ends'] for j in d[3][owner[v]]-pool}
    assert len(matching(direct)) == q
    assert len(matching(broad)) == 2*q
    assert sum(not choices for choices in broad.values()) == 2*q
    # Both surviving source classes have an explicit distinct NEW unit.
    for i in range(1, q+1):
        left = owner[shift((5, 4), i)]
        bottom = owner[shift((24, 6), i)]
        for o, coordinate in [(left, (7, 24*i+5)), (bottom, (12, 24*i+7))]:
            j = meta['owner'][coordinate]
            assert j in d[3][o] & d[4] - pool
    # Explicit beta stems: three one-link stems and one two-link stem per copy.
    routes = [[((5, 17), (5, 16))], [((5, 19), (5, 20))],
              [((5, 4), (5, 3))], [((24, 17), (24, 18)), ((18, 15), (18, 16))]]
    used_owners, beta_targets, chosen = set(), set(), []
    for i in range(q+1):
        for route in routes:
            rr = [(shift(v, i), shift(w, i)) for v, w in route]
            assert all(e in d[2] for e in rr)
            oo = [owner[rr[0][0]]] + [owner[w] for v, w in rr]
            assert oo[0] in aa and oo[-1] in bb and set(oo[1:-1]) <= mm
            assert len(set(oo)) == len(oo) and not used_owners & set(oo)
            used_owners.update(oo)
            beta_targets.add(oo[-1])
            chosen += rr
    assert len(beta_targets) == 4*(q+1) and len(chosen) == 5*(q+1)
    # Existing terminals/links still separate by copy, despite the CONNECTED
    # occupied graph. The bridge vertices belong only to PP cycles.
    assert all(v[1]//24 == w[1]//24 for v, w in d[1])
    assert all(v[1]//24 == w[1]//24 for v, w in d[2])
    for solver in (ordinary_flow, fork_flow):
        opt = solver(*clipped(d, set()))
        assert (opt['value'], opt['cost']) == (4*(q+1), 5*(q+1))
        totals['ordinary_full_beta_only_comparisons'] += 1
    # Keep all old C assignments, but add only the NEW copies' beta routes.
    for v, w in chosen[5:]:
        assert ('bp', w) not in assignment and v not in assignment.values()
        assignment['bp', w] = v
    repaired = lift(clipped(d, pool), assignment)
    assert repaired['certified_deficit'] == 0 and repaired['selected_links'] == 18+5*q
    assert ordinary_flow(*d)['value'] == fork_flow(*d)['value'] == len(aa)
    if independent:
        for forks in (False, True):
            exact = optimize(*clipped(d, set()), allow_forks=forks)
            assert (exact['value'], exact['cost']) == (4*(q+1), 5*(q+1))
            totals['independent_primitive_packs'] += 1
    totals['connected_frozen_models'] += 1
    return dict(copies=q+1, added_copies=q, selected=len(cur[2]), endpoints=len(P),
                alpha=len(aa), beta=len(bb), mixed=len(mm), new_tp=23*q,
                residual_new_new_alpha=4*q, direct_free_end_interval_rank=q,
                whole_owner_interval_rank=2*q, zero_whole_support_new_alpha=2*q,
                beta_only_value=4*(q+1), beta_only_min_links=5*(q+1),
                retained_C_plus_new_beta_links=18+5*q, occupied_graph_connected=True,
                owner_beta_link_graph_separates_by_copy=True, completely_frozen=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    base, data, meta, *_ = load_model()
    assert connected(base)
    prefix, boundary_witnesses = prelude(base)
    # Permanent occupied-side witnesses for the two zero-support source classes.
    P = {v for e in base[3] for v in e}
    blockers = []
    for tip in [(5, 6), (5, 19)]:
        component = next(c for c in meta['original']['components']
                         if c['kind'] == ['TP', 'TP'] and (tip[0]//2, tip[1]) in c['nodes'])
        for band, col in component['nodes']:
            guards = [next(v for v in [(2*band, col+dc), (2*band+1, col+dc)] if v in P)
                      for dc in (-1, 1)]
            blockers.append(dict(source_class=tip, node=(band, col), retained_side_endpoints=guards))
    assert len(blockers) == 25
    totals, named = Counter(), {}
    for q in range(1, 13):
        cur = build(base, q)
        layers = lifted_rank(base, cur, q, prefix)
        info = inspect(base, cur, q, totals, independent=q == 1)
        named[str(q)] = info
        if q == 1:
            record = dict(shape=cur[:2], selected=sorted(cur[2]), matching=cur[3],
                          freezing_layers=layers, completely_frozen=True,
                          occupied_graph_connected=True, parameter_q=1, expected=info)
            Path('develop/fixtures/connected_frozen_new_end_obstacle.json').write_text(json.dumps(record, separators=(',', ':'))+'\n')
    # All five perfect matchings of the closed 2x4 PP patch. Classify freezing
    # independently, and never silently identify feasible with frozen.
    cur = build(base, 1)
    reference_data, _, _ = whole_support_data(cur, whole_bands(cur))
    patch = {(r, c) for r in (2, 3) for c in range(22, 26)}
    assert all((v in patch) == (w in patch) for v, w in cur[3])
    outside = [e for e in cur[3] if not set(e) & patch]
    patch_profiles = []
    for edges, _ in matchings(patch, False):
        candidate = (*cur[:3], outside+edges)
        assert feasible(candidate)
        f, _ = frozen_certificate(candidate)
        dd, _, _ = whole_support_data(candidate, whole_bands(candidate))
        assert dd[0] == reference_data[0]
        assert {canon(e) for e in dd[1]} == {canon(e) for e in reference_data[1]}
        assert set(dd[2]) == set(reference_data[2])
        opt = ordinary_flow(*clipped(dd, set()))
        assert (opt['value'], opt['cost']) == (8, 10)
        patch_profiles.append(dict(matching=edges, frozen_endpoints=len(f), completely_frozen=len(f) == 620))
    assert len(patch_profiles) == 5
    recipe = dict(prelude_layers=prefix, boundary_witnesses=boundary_witnesses,
                  zero_support_side_blockers=blockers,
                  rank_recipe='shift preludes to every copy; freeze all four boundary endpoints per copy; freeze four new splice endpoints per bridge; replay original complete ranks, skipping already frozen sites')
    Path('develop/fixtures/connected_frozen_splice_local_certificate.json').write_text(json.dumps(recipe, indent=2)+'\n')
    result = dict(status='PASS', totals=dict(totals), named=named, patch_profiles=patch_profiles,
                  fixed_base_prelude_endpoints=112, fixed_base_prelude_layers=27,
                  fixed_base_occupied_graph_connected=True,
                  zero_support_path_nodes=25, retained_side_blockers=50,
                  scope='Unbounded written q>=1 CONNECTED occupied graph, fully frozen, retains old49T308P but changes two old PP matching edges per bridge; no oldM-retention claim. New-new residual4q; direct free-end interval rankq, even whole-owner interval rank2q; two zero-support new alphas per added copy. Candidate interval-only repair NOTuniversal. Beta-only ordinary/full pays ALL4(q+1) at exact5(q+1)links with distinct beta identities. Can keep old18C and extend by5qnew-beta links. General freezing by112endpoint prelude+4boundary/core+old-rank replay, NOT finite-q enumeration. Terminal/link beta network stays separate by copy although occupied graph connected; not a coupled-owner counterexample. UniversalCompensationAnd5over6OPEN.')
    args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', totals=dict(totals), first=named['1'],
                          patch_frozen_profiles=[r['frozen_endpoints'] for r in patch_profiles])))


if __name__ == '__main__':
    main()
