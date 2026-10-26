"""Actual-board controls for the all-width no-rematching barrier and hole cover.

The arbitrary-width proofs are written separately. Finite selector controls
check the guarded-pair adapter, not a universal-grid extrapolation.
"""
from collections import Counter
from itertools import product
import json
from pathlib import Path

from check_turning_edge_ownership import adapter, canonical, verify_owner
from check_component_cut_exchange import all_matchings

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def family(w):
    assert w >= 6 and w % 2 == 0
    p = {(r, c) for r in (0, 1) for c in range(1, w-1)} | {(2, 1), (2, w-2)}
    m = [canonical((1, 1), (2, 1)), canonical((1, w-2), (2, w-2))]
    m += [canonical((0, c), (0, c+1)) for c in range(1, w-2, 2)]
    m += [canonical((1, c), (1, c+1)) for c in range(2, w-3, 2)]
    t = {(0, 0), (0, w-1), (2, 0), (2, w-1), (3, 1), (3, w-2)}
    t |= {(2, c) for c in range(3, w-3, 2)}
    t |= {(3, c) for c in range(4, w-2, 2)}
    forced_holes = {(2, 2), (2, w-3)}
    pairs = [((0, 0), (1, 0)), ((2, 0), (3, 0)),
             ((0, w-1), (1, w-1)), ((2, w-1), (3, w-1)),
             ((3, 1), (3, 2)), ((3, w-2), (3, w-3))]
    pairs += [((2, c), (3, c)) for c in range(3, w-3)]
    return p, m, t, forced_holes, pairs


def near(u, v):
    return abs(u[0]-v[0])+abs(u[1]-v[1]) == 1


def forcing_order(p, matching):
    remaining = set(p); forced = []
    while remaining:
        leaves = [(u, [v for v in remaining if near(u, v)]) for u in remaining]
        leaves = [(u, vs[0]) for u, vs in leaves if len(vs) == 1]
        assert leaves, 'No forced leaf: cannot certify uniqueness by peeling'
        u, v = min(leaves)
        edge = canonical(u, v)
        assert edge in matching
        forced.append(edge); remaining -= {u, v}
    assert set(forced) == set(matching)
    return forced


def guard_cover(w, p, forced_holes, pairs):
    q = {(r, c) for r in range(4) for c in range(w)}-p
    endpoints = [u for pair in pairs for u in pair]
    assert len(pairs) == w and len(endpoints) == len(set(endpoints))
    assert set(endpoints) == q-forced_holes
    assert len(forced_holes) == 2
    assert all(sum(near(h, x) for x in p) >= 2 for h in forced_holes)
    for a, b in pairs:
        assert near(a, b) and any(near(a, x) for x in p)
    return {u: v for a, b in pairs for u, v in [(a, b), (b, a)]}


def hole_certificate(data, t, partner):
    assert t <= partner.keys()
    image = {partner[u] for u in t}
    assert len(image) == len(t) and image <= data['holes']
    assert all(near(u, partner[u]) for u in t)
    return len(data['holes']-image)


def check_width(w):
    p, matching, selected, forced_holes, pairs = family(w)
    data = adapter(4, w, selected, matching)
    assert {u for e in matching for u in e} == p
    assert len(p) == 2*w-2 and len(matching) == w-1
    assert len(selected) == w and len(data['holes']) == w+2
    assert len(selected)+len(matching) == 2*w-1
    assert len(forcing_order(p, matching)) == w-1
    partner = guard_cover(w, p, forced_holes, pairs)
    assert hole_certificate(data, selected, partner) == 2
    assert data['holes']-{partner[u] for u in selected} == forced_holes
    assert all(sum(u in selected for u in pair) == 1 for pair in pairs)
    # All P is in this tile set; no arbitrary regrouping of P-only charges
    # can compensate its strictly positive q sum under unchanged tile demands.
    n = w//2
    cut = {(0, c) for c in range(n)} | {(1, 0), (1, n-1)}
    assert all(data['tile'](u) in cut for u in p)
    cut_q = sum(2*sum(data['tile'](u) == b for u in selected)
                + sum(data['tile'](u) == b for u in p)-4 for b in cut)
    assert cut_q == 2
    assert sum(data['demand'].values()) == w and len(matching) == w-1
    assert data['sparse_slack'] == 2
    # Reposition ONE selected vertex, preserving cardinality and actual M.
    normalized = selected-{(3, w-2)} | {(3, w-3)}
    normalized_data = adapter(4, w, normalized, matching)
    assert len(normalized) == len(selected)
    trace = [(1, 0)]+[(0, c) for c in range(n)]+[(1, n-1)]
    owner = {e: b for b, es in normalized_data['loops'].items() for e in es}
    for a, b in zip(trace, trace[1:]):
        es = normalized_data['between'][frozenset([a, b])]
        assert len(es) == 1
        owner[es[0]] = a
    assert verify_owner(normalized_data, matching, owner) == dict(
        used_edges=w-1, unused_edges=0, exact_tile_demands=True)
    assert normalized_data['sparse_slack'] == 1
    return dict(width=w, T=w, M=w-1, H=w+2, J=2*w-1,
                sharp_gap_from_half=1, guarded_pairs=len(pairs),
                forced_holes=sorted(forced_holes), unique_matching_forced_edges=w-1,
                demand=w, all_physical_resources=w-1, endpoint_charge_cut_excess=2,
                arbitrary_rematching_cannot_repair=True,
                adjacent_hole_injection_unused_holes=2,
                one_step_T_relocation_repairs_ownership=True,
                normalization_preserves_M_P_and_T_cardinality=True)


def selector_controls(w):
    p, matching, _, forced_holes, pairs = family(w)
    partner = guard_cover(w, p, forced_holes, pairs)
    accepted = 0; maximizers = 0; by_size = Counter()
    for values in product(range(3), repeat=w):
        t = {pair[v-1] for pair, v in zip(pairs, values) if v}
        try:
            data = adapter(4, w, t, matching)
        except AssertionError:
            continue
        accepted += 1; by_size[len(t)] += 1
        assert len(t) <= w
        assert hole_certificate(data, t, partner) == 2+2*(w-len(t))
        maximizers += len(t) == w
    # A separate direct perfect-matching enumeration checks the uniqueness
    # adapter at these small widths; all-width uniqueness is a written peel.
    matching_count = sum(1 for _ in all_matchings(p))
    assert matching_count == 1
    return dict(width=w, profiles=3**w, feasible_selector_sets=accepted,
                sharp_selector_sets=maximizers, selector_histogram=dict(sorted(by_size.items())),
                perfect_matchings=matching_count)


def main():
    rows = [check_width(w) for w in range(6, 105, 2)]
    controls = [selector_controls(w) for w in (6, 8)]
    result = dict(status='PASS', width_controls=len(rows), smallest=rows[0], largest=rows[-1],
                  arbitrary_selector_controls=controls,
                  finite_profile_count=sum(r['profiles'] for r in controls),
                  feasible_selector_sets=sum(r['feasible_selector_sets'] for r in controls),
                  scope='Written all-even-width exact maximum for fixed P with arbitrary T; unique actual matching; all-rematching and all-endpoint-only charge obstruction for explicit sharp T; guarded-pair adjacent-hole certificate; one-selection relocation repair.',
                  trust_boundary='Finite profiles validate adapters; universal-grid bounds, arbitrary-P normalization, freezing, and end-to-end coordinate Lean are not proved.')
    (ROOT/'output/unique-matching-hole-barrier.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
