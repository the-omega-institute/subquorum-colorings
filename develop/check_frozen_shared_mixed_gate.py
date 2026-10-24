"""Verify a physical frozen obstruction to blanket source separation.

The canonical witness is explicit; running this verifier does not need Z3.
Its rank certificate is checked independently of the repository peeling code.
"""

import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import physical, solve
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_terminal_cancellation_and_stranded_demand import extended_ports, terminal_data


if not __debug__:
    raise RuntimeError('Run without -O: verification uses assertions.')


ROWS = (
    '................',
    '....T.T.........',
    '....PPPT....T...',
    '....PP.....TP...',
    '..T.PP.T.T..PPT.',
    '.TP.PPPPPP..PP..',
    '..PPPPPPPPPPPP..',
    '..PPPPPPPPPPPP..',
    '..PPPPP.PP.PPPT.',
    '.TPP..T.PPPP....',
    '...PT..TP.PPPT..',
    '...T....T.T.T...',
    '................',
    '................',
)

MATCHING = [
    ((2, 4), (3, 4)), ((2, 5), (2, 6)), ((3, 5), (4, 5)),
    ((3, 12), (4, 12)), ((4, 4), (5, 4)), ((4, 13), (5, 13)),
    ((5, 2), (6, 2)), ((5, 5), (5, 6)), ((5, 7), (6, 7)),
    ((5, 8), (6, 8)), ((5, 9), (6, 9)), ((5, 12), (6, 12)),
    ((6, 3), (6, 4)), ((6, 5), (6, 6)), ((6, 10), (6, 11)),
    ((6, 13), (7, 13)), ((7, 2), (7, 3)), ((7, 4), (7, 5)),
    ((7, 6), (7, 7)), ((7, 8), (8, 8)), ((7, 9), (7, 10)),
    ((7, 11), (7, 12)), ((8, 2), (9, 2)), ((8, 3), (8, 4)),
    ((8, 5), (8, 6)), ((8, 9), (9, 9)), ((8, 11), (9, 11)),
    ((8, 12), (8, 13)), ((9, 3), (10, 3)), ((9, 8), (10, 8)),
    ((9, 10), (10, 10)), ((10, 11), (10, 12)),
]

LAYERS = [
    [(2, 6), (3, 12), (5, 2), (10, 3), (10, 8), (10, 12)],
    [(2, 4), (4, 13), (9, 2), (10, 10)],
    [(3, 5), (5, 12), (7, 2), (8, 3), (9, 9), (9, 11)],
    [(4, 4), (6, 3), (6, 13), (7, 4), (8, 8)],
    [(5, 5), (6, 5), (7, 9), (7, 12), (8, 5), (8, 13)],
    [(5, 7), (6, 11), (7, 6), (7, 11), (8, 11)],
    [(6, 6), (6, 7), (6, 8), (7, 7), (7, 10), (8, 12)],
    [(5, 6), (5, 9), (6, 4), (6, 9), (7, 5), (7, 8), (7, 13), (8, 6)],
    [(5, 4), (5, 8), (6, 10), (6, 12), (7, 3), (8, 4), (8, 9)],
    [(4, 5), (5, 13), (6, 2), (8, 2), (9, 8), (9, 10)],
    [(3, 4), (4, 12), (9, 3), (10, 11)],
    [(2, 5)],
]

CRITICAL_PAIRS = [((3, 12), (5, 9)), ((5, 2), (5, 7)), ((5, 8), (10, 8))]
CRITICAL_TRACES = [
    [(1, 12), (2, 12), (3, 12), (3, 11), (3, 10), (3, 9), (2, 9)],
    [(2, 2), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6), (3, 7), (2, 7)],
    [(2, 8), (3, 8), (4, 8), (5, 8)],
]


def fixture():
    selected = {(r, c) for r, row in enumerate(ROWS) for c, value in enumerate(row) if value == 'T'}
    endpoints = {(r, c) for r, row in enumerate(ROWS) for c, value in enumerate(row) if value == 'P'}
    assert len({v for e in MATCHING for v in e}) == 2*len(MATCHING)
    assert endpoints == {v for e in MATCHING for v in e}
    return len(ROWS), len(ROWS[0]), selected, list(MATCHING)


def check_rank_certificate(current, layers):
    """Check every strict dependency using coordinates, not a peeling result."""
    mate = {u: v for edge in current[3] for u, v in (edge, edge[::-1])}
    rank = {v: i for i, layer in enumerate(layers) for v in layer}
    assert len(rank) == sum(map(len, layers)) == len(mate) and set(rank) == set(mate)
    witnesses = []
    for v in sorted(mate):
        kept = []
        for w in current[2] | set(mate):
            if abs(v[0]-w[0])+abs(v[1]-w[1]) != 1:
                continue
            if w in current[2] or rank[mate[w]] < rank[v]:
                kept.append(w)
        assert len(kept) >= 2
        witnesses.append(dict(endpoint=v, rank=rank[v], kept_neighbors=sorted(kept)[:2]))
    return witnesses


def inspect_image(current, bands, move, layers):
    direct_check(*current)
    witnesses = check_rank_certificate(current, layers)
    assert frozen_certificate(current)[0] == {v for e in current[3] for v in e}
    data = terminal_data(current, bands)
    original, labels, intervals, interval_owner, kinds, pairs, ports = data
    critical = [tuple(map(move, pair)) for pair in CRITICAL_PAIRS]
    for index, pair in enumerate(critical):
        assert frozenset(pair) in {frozenset(p) for p in pairs}
        assert [kinds[v] for v in pair] == (['TP', 'TP'] if index < 2 else ['BP', 'TP'])
    extended = extended_ports(current, bands, labels, intervals, interval_owner, kinds, ports, Counter())
    resources = {interval_owner[5, 6], interval_owner[5, 9]}
    assert len(resources) == 2
    assert all(intervals[r] == dict(band=5, first=c, last=c)
               for c, r in ((6, interval_owner[5, 6]), (9, interval_owner[5, 9])))
    assert {(5, 6), (5, 9)} <= set(extended[move((10, 8))])
    boundary = {interval_owner[b, c] for b in range(len(bands)) for c in (0, len(bands[b])-1)}
    assert not resources & boundary
    links = [(move(v), move((5, 8))) for v in ((5, 7), (5, 9))]
    assert all(abs(u[0]-v[0])+abs(u[1]-v[1]) == 1 for u, v in links)
    local_kinds = {v: kinds[v] for pair in critical for v in pair}
    local = solve(local_kinds, critical, links, {move((10, 8)): resources}, resources)
    assert (local['value'], local['cost'], local['deficit']) == (1, 1, 1)
    assert local['cut'] == [('mixed', 2)] and set(local['blocked']) == {0, 1}
    # Explicit reachability matching: alpha 0 -> resource 0, alpha 1 -> resource 1.
    # Each has its displayed link, then the unique mixed strand, then either access.
    assert len(links) == len(resources) == 2 and len({v for _, v in links}) == 1
    # Of four subsets of links only three are terminal matchings; none uses both.
    legal_subsets = [subset for n in range(3) for subset in itertools.combinations(links, n)
                     if len({v for e in subset for v in e}) == 2*len(subset)]
    assert len(legal_subsets) == 3 and max(map(len, legal_subsets)) == 1
    bypass = [move((3, 12)), move((5, 2))]
    bypass_resources = [interval_owner[1, 13], interval_owner[2, 3]]
    assert len(set(bypass_resources)) == 2 and not set(bypass_resources) & boundary
    for v, r in zip(bypass, bypass_resources):
        assert any(interval_owner[port] == r for port in ports[v])
    return dict(ledger={key: original[key] for key in
                        ('alpha', 'beta', 'gamma', 'balance', 'boundary_budget', 'surplus_twice')},
                local=local, projection_value=2, gate_resources=sorted(resources),
                bypass_terminals=bypass, bypass_resources=bypass_resources,
                strict_rank_witnesses=witnesses)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    current = fixture()
    bands = whole_bands(current)
    base = inspect_image(current, bands, lambda v: v, LAYERS)
    data = terminal_data(current, bands)
    for trace in CRITICAL_TRACES:
        assert any(p['nodes'] in (trace, trace[::-1]) for p in data[0]['components'])
    full = physical(current, bands, [], Counter())
    assert (full['value'], full['cost'], full['deficit']) == (2, 0, 0)
    images = []
    for symmetry in itertools.product((False, True), repeat=3):
        shape, selected, matching = transformed(*current, *symmetry)
        move = image_map(*current[:2], symmetry)
        image_bands = [[tuple(map(move, cells)) for cells in band] for band in bands]
        image_layers = [list(map(move, layer)) for layer in LAYERS]
        checked = inspect_image((*shape, selected, matching), image_bands, move, image_layers)
        images.append(dict(symmetry=symmetry, local_value=checked['local']['value'],
                           projection_value=checked['projection_value']))
    report = dict(status='PASS', shape=current[:2], selected=sorted(current[2]), matching=current[3],
                  layer_sizes=list(map(len, LAYERS)), base=base, full_network=full, images=images,
                  scope='Explicit fully frozen physical counterexample to blanket source separation; '
                  'projection 2 versus flow 1 for the declared restricted relay rule. '
                  'The full physical network has flow 2. No counterexample to the global inequality '
                  'or to source separation under stronger residual-source hypotheses is asserted. '
                  'No Lean or independent review is implied by this checker.')
    args.output.write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', endpoints=64, symmetry_images=len(images),
                         projection=2, restricted_flow=1, full_flow=2, full_cost=0)))


if __name__ == '__main__':
    main()
