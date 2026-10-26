"""Exact checks of the structural signed-strip lemma and its sharp obstruction."""
from itertools import product
import json
from pathlib import Path

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]
SITES = [(r, c) for r in range(2) for c in range(2)]


def adjacent(u, v):
    return abs(u[0]-v[0])+abs(u[1]-v[1]) == 1


def feasible_local(word):
    occupied = {u for u, d in word.items() if d}
    return all(sum(adjacent(u, v) for v in occupied) <= 1
               for u, d in word.items() if d == 1)


def charges(word):
    t = {u for u, d in word.items() if d == 1}
    p = {u for u, d in word.items() if d == 2}
    h = {u for u, d in word.items() if d == 0}
    q = len(t)-len(h)
    if len(t) == 2 and len(p) == 1:
        sigma = {u: 1 for u in p}
        kind = 'positive'
    elif len(t) == 1 and len(p) == 2:
        if len({u[0] for u in p}) == 1:
            selected = next(iter(t))
            sigma = {u: 1 if u[1] == selected[1] else -1 for u in p}
            kind = 'neutral_horizontal'
        else:
            assert len({u[1] for u in p}) == 1
            sigma = {u: 0 for u in p}
            kind = 'neutral_vertical'
    elif len(p) == 4:
        sigma = {u: 0 for u in p}
        kind = 'all_endpoints'
    elif len(t) == 2 and not p:
        sigma = {}
        kind = 'two_selected'
    elif len(p) == 3 and not t:
        hole = next(iter(h))
        sigma = {u: -1 if u[1] == hole[1] else 0 for u in p}
        kind = 'three_endpoints'
    else:
        assert len(t)+len(p) <= 2
        sigma = {u: -1 for u in p}
        kind = 'other'
    assert set(sigma) == p
    return q, sigma, kind


def local_checks():
    blocks = []
    counts = {}
    internal = interfaces = 0
    for labels in product(range(3), repeat=4):
        word = dict(zip(SITES, labels))
        if not feasible_local(word):
            continue
        q, sigma, kind = charges(word)
        assert q <= sum(sigma.values())
        counts[kind] = counts.get(kind, 0)+1
        for u in sigma:
            for v in sigma:
                if u < v and adjacent(u, v):
                    assert sigma[u]+sigma[v] <= 0
                    internal += 1
        blocks.append((word, sigma))
    for a, sa in blocks:
        for b, sb in blocks:
            joined = dict(a)
            joined.update({(r, c+2): d for (r, c), d in b.items()})
            if not feasible_local(joined):
                continue
            for r in range(2):
                if a[r, 1] == b[r, 0] == 2:
                    assert sa[r, 1]+sb[r, 0] <= 0
                    interfaces += 1
    return dict(feasible_blocks=len(blocks), block_types=counts,
                within_block_actual_edge_controls=internal,
                horizontal_interface_actual_edge_controls=interfaces)


def board_ledger(height, width, selected, matching):
    assert height % 2 == width % 2 == 0
    board = {(r, c) for r in range(height) for c in range(width)}
    mate = {}
    for u, v in matching:
        assert u in board and v in board and adjacent(u, v)
        assert u not in mate and v not in mate
        mate[u] = v
        mate[v] = u
    assert selected <= board and not selected & mate.keys()
    occupied = selected | mate.keys()
    assert all(sum(adjacent(u, v) for v in occupied) <= 1 for u in selected)
    sigma = {}
    slack = 0
    for r in range(0, height, 2):
        for c in range(0, width, 2):
            word = {(a, b): 1 if (r+a, c+b) in selected else
                    2 if (r+a, c+b) in mate else 0 for a, b in SITES}
            q, local_sigma, _ = charges(word)
            sigma.update({(r+a, c+b): x for (a, b), x in local_sigma.items()})
            slack += sum(local_sigma.values())-q
    cross = internal = 0
    negative_edges = []
    crossing_edges = []
    for u, v in matching:
        payment = sigma[u]+sigma[v]
        if u[0]//2 == v[0]//2:
            assert payment <= 0
            internal += payment
            if payment < 0:
                negative_edges.append((u, v, payment))
        else:
            cross += payment
            crossing_edges.append((u, v, payment))
    holes = board-occupied
    assert len(selected)-len(holes) == cross+internal-slack
    return dict(T=len(selected), M=len(matching), H=len(holes),
                J=len(selected)+len(matching), area=height*width,
                cross_charge=cross, internal_charge=internal, block_slack=slack,
                negative_internal_edges=negative_edges, crossing_edges=crossing_edges)


def sharp_obstruction(width):
    assert width >= 4 and width % 2 == 0
    selected = {(0, 0), (3, 0), (5, 0)}
    matching = [((1, 0), (2, 0)), ((1, 1), (1, 2)), ((0, 2), (0, 3)),
                ((1, 3), (2, 3)), ((2, 1), (2, 2)), ((3, 2), (3, 3)),
                ((4, 1), (5, 1)), ((4, 2), (4, 3)), ((5, 2), (5, 3))]
    matching += [((r, c), (r+1, c))
                 for c in range(4, width) for r in [0, 2, 4]]
    ledger = board_ledger(6, width, selected, matching)
    assert ledger['J'] == 3*width and ledger['T'] == ledger['H'] == 3
    assert (ledger['cross_charge'], ledger['internal_charge'], ledger['block_slack']) == (2, -2, 0)
    assert len(ledger['negative_internal_edges']) == 2
    return dict(width=width, **ledger)


def main():
    local = local_checks()
    controls = [sharp_obstruction(w) for w in range(4, 82, 2)]
    original = board_ledger(6, 4, {(0, 0), (3, 0)},
                            [((1, 0), (2, 0)), ((1, 1), (1, 2)), ((0, 2), (0, 3)),
                             ((1, 3), (2, 3)), ((2, 1), (2, 2)), ((3, 2), (3, 3))])
    assert original['J'] == 8 and original['cross_charge'] == 2
    result = dict(status='PASS', **local, sharp_extensions=len(controls),
                  smallest_sharp_obstruction=controls[0], original_assistance_example=original,
                  scope='Checks the written all-width signed two-row lemma, actual-edge ledger, and symbolic even-width sharp obstruction. Finite board checks are controls only.',
                  remaining='General cross-strip compensation inequality for arbitrary heights; purely structural anchor-free six-row proof.')
    (ROOT/'output/two-row-signed-compensation.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
