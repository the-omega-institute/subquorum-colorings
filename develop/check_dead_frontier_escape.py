"""Solver-free check of a frozen mixed-fork escape with no productive route.

See DEAD_FORCED_MIXED_ESCAPE.md for the general rank proof and all-copy family.
Finite images are regression checks, not a substitute for those arguments.
"""
import argparse
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_horizontal_bp_forests import forests, solve_compressed
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_partial_tip_compensation import live_prune
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import brute, evaluate, whole_support_data

if not __debug__:
    raise RuntimeError('Run without -O: assertions required.')

FIXTURE = Path(__file__).parent/'fixtures/frozen_dead_forced_mixed_escape.json'
LEFT = ((5, 2), (5, 5))
RIGHT = ((5, 7), (10, 9))
GATE = ((5, 6), (10, 4))
DEAD = ((5, 8), (5, 9))


def fixture(copies=1):
    assert copies >= 1
    j = json.loads(FIXTURE.read_text())
    move = lambda v, i: (v[0]+14*i, v[1])
    current = (14*copies, 18,
               {move(v, i) for i in range(copies) for v in j['selected']},
               [tuple(move(v, i) for v in e) for i in range(copies) for e in j['matching']])
    layers = [[move(v, i) for i in range(copies) for v in layer]
              for layer in j['freezing_layers']]
    return current, layers


def inspect(current, bands, layers, moves):
    direct_check(*current)
    ranks = check_rank_certificate(current, layers)
    endpoints = {v for e in current[3] for v in e}
    assert frozen_certificate(current)[0] == endpoints
    kinds0, components = independent_strands(current, bands)
    data, meta, _ = whole_support_data(current, bands)
    kinds, pairs, links, W, resources = data
    assert kinds == kinds0
    assert {frozenset(p) for p in pairs} == {tips for tips, _ in components if tips}
    owner, A, B, M = owner_data(kinds, pairs)
    mate = {v: w for e in current[3] for v, w in (e, e[::-1])}
    # In transposed images, identify H relative to the transported bands.
    partner = {v: w for band in bands for e in band for v, w in (e, e[::-1])}
    H = {m for m in M for bp in pairs[m]
         if kinds[bp] == 'BP'
         and sum((mate[bp][k]-bp[k])*(partner[bp][k]-bp[k]) for k in (0, 1)) == 0}
    F = forests(data, H)
    pruned, prune_record = live_prune(data)
    records = []
    explicit_links = []
    used_intervals = set()
    for move in moves:
        left, right, gate, dead = [tuple(map(move, p)) for p in (LEFT, RIGHT, GATE, DEAD)]
        al, ar, g, d = [owner[p[0]] for p in (left, right, gate, dead)]
        assert len({al, ar, g, d}) == 4
        assert {al, ar} <= A and {g, d} <= M
        for p in (left, right, gate, dead):
            assert frozenset(p) in {frozenset(q) for q in pairs}
        assert [kinds[v] for v in gate] == ['BP', 'TP']
        assert [kinds[v] for v in dead] == ['BP', 'TP']
        assert all(e in links for e in [(left[1], gate[0]), (right[0], gate[0]), (right[0], dead[0])])
        assert mate[gate[0]] == move((6, 6))
        assert mate[right[0]] == move((6, 7))
        assert mate[left[1]] == move((6, 5))
        assert mate[dead[0]] == dead[1]
        assert next(body for tips, body in components if frozenset(dead) == tips) == set(dead)
        assert not W[d]
        assert not meta['all_ports'][dead[0]] and not meta['all_ports'][dead[1]]
        assert [e for e in links if e[0] == dead[1]] == [(dead[1], dead[0])]
        assert F['root_of'][d] == d and F['trees'][d] == {d}
        assert F['incoming'][d] == [(right[0], dead[0])]
        assert not F['outgoing'][d]
        assert d in prune_record['removed_mixed']
        # The receiver has >=2 ORIGINAL unmarked units, despite a dead escape.
        assert len(W[g]) == 3 and W[g] <= W[ar]
        assert not W[al]
        # Explicit legal whole-beta + original-interval packing, not just flow.
        beta = owner[move((5, 3))]
        assert beta in B and frozenset(pairs[beta]) == frozenset(map(move, ((5, 3), (5, 4))))
        e = (left[0], move((5, 3)))
        assert e in links
        explicit_links.append(e)
        unit = min(W[g])
        assert unit not in used_intervals
        used_intervals.add(unit)
        records.append(dict(left_alpha=left, right_alpha=right, gate=gate, dead=dead,
                            dead_support=[], nonself_dead_outputs=[],
                            gate_units=[meta['intervals'][j] for j in sorted(W[g])],
                            explicit_beta_link=e, explicit_right_unit=meta['intervals'][unit]))
    q = len(moves)
    assert (len(A), len(B), len(M)) == (2*q, q, 5*q)
    assert len(endpoints) == 50*q and len(current[2]) == 25*q
    assert len({v for e in explicit_links for v in e}) == 2*q
    assert evaluate(kinds, pairs, explicit_links, W, resources)['value'] == 2*q
    # Compare three implementations, retaining the entire original pool.
    full = fork_flow(*data)
    compressed = solve_compressed(data, H)
    live = fork_flow(*pruned)
    assert all((r['value'], r['cost']) == (2*q, q) for r in (full, compressed, live))
    return dict(copies=q, endpoints=len(endpoints), selected=len(current[2]),
                alpha=len(A), beta=len(B), mixed=len(M), dead_forced_escapes=q,
                full_payment=full['value'], minimum_link_cost=full['cost'],
                rank_witnesses=len(ranks), motifs=records), data


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output', type=Path, required=True)
    a = ap.parse_args()
    cur, layers = fixture()
    base, data = inspect(cur, whole_bands(cur), layers, [lambda v: v])
    answer, count = brute(*data)
    assert answer == (2, 1) and count == 390
    images = []
    bands = whole_bands(cur)
    for sym in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*cur, *sym)
        move = image_map(*cur[:2], sym)
        bs = [[tuple(map(move, e)) for e in band] for band in bands]
        ls = [list(map(move, layer)) for layer in layers]
        r, d = inspect((*shape, selected, matching), bs, ls, [move])
        exact, n = brute(*d)
        assert exact == (2, 1) and n == count
        images.append(dict(symmetry=sym, **r))
    stacks = []
    for q in (2, 3, 5, 8):
        c, ls = fixture(q)
        moves = [lambda v, i=i: (v[0]+14*i, v[1]) for i in range(q)]
        r, _ = inspect(c, whole_bands(c), ls, moves)
        stacks.append(r)
    report = dict(status='PASS', fixture=str(FIXTURE.relative_to(Path(__file__).parent.parent)),
                  base=base, independent_base_terminal_matchings=count,
                  independent_image_terminal_matchings=8*count,
                  images=images, stacked_controls=stacks,
                  scope='Solver-free explicit frozen rule counterexample, all original resources; '
                  'written general rank extension and arbitrary-copy proof separate. '
                  'Full payment remains complete; no global inequality counterexample or 5/6 improvement. '
                  'No new Lean or Oracle verification.')
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', endpoints=50, selected=25, forced_dead_escape=1,
                         full_payment=2, min_links=1, symmetry_images=8,
                         independent_base_matchings=count, stacked_copies=[2, 3, 5, 8])))


if __name__ == '__main__':
    main()
