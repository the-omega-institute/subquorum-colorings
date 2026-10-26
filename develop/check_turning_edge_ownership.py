"""Actual-edge ownership certificates and sharp, arbitrarily long turning relays.

The all-length proofs are in TURNING_ACTUAL_EDGE_COMPENSATION.md. Finite controls
here check the coordinate construction, physical capacities and forced changes.
"""
from collections import Counter, defaultdict
import json
from pathlib import Path

from check_two_row_signed_compensation import charges

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def canonical(u, v):
    return tuple(sorted((u, v)))


def turning_board(q):
    assert q >= 1
    width = 2*q+2
    selected = {(0, 2*q+1), (2, 2*q+1), (3, 2*q)}
    matching = [((1, 2*q), (2, 2*q)), ((0, 2*q), (0, 2*q-1))]
    if q == 1:
        matching += [((0, 0), (1, 0)), ((1, 1), (2, 1)), ((2, 0), (3, 0))]
    else:
        matching += [((0, 2*j+1), (0, 2*j+2)) for j in range(q-1)]
        matching += [((1, 2*j), (1, 2*j+1)) for j in range(1, q)]
        matching += [((0, 0), (1, 0)), ((1, 1), (2, 1)), ((2, 0), (3, 0))]
        matching += [((3, 2*j+1), (3, 2*j+2)) for j in range(q-1)]
        matching += [((2, 2*j), (2, 2*j+1)) for j in range(1, q-1)]
        matching += [((2, 2*q-2), (2, 2*q-1))]
    matching = [canonical(*e) for e in matching]
    trace = [(1, q), (0, q)]
    trace += [(0, j) for j in reversed(range(q))]
    trace += [(1, j) for j in range(q)]
    return 4, width, selected, matching, trace


def adapter(height, width, selected, matching):
    board = {(r, c) for r in range(height) for c in range(width)}
    mate = {}
    assert len(matching) == len(set(matching))
    for u, v in matching:
        assert u in board and v in board and u not in mate and v not in mate
        assert abs(u[0]-v[0])+abs(u[1]-v[1]) == 1
        mate[u], mate[v] = v, u
    assert selected <= board and not selected & mate.keys()
    occupied = selected | mate.keys()
    for r, c in selected:
        assert len(occupied & {(r-1, c), (r+1, c), (r, c-1), (r, c+1)}) <= 1
    tile = lambda u: (u[0]//2, u[1]//2)
    tile_occupied = Counter(tile(u) for u in occupied)
    tiles = [(r, c) for r in range(height//2) for c in range(width//2)]
    demand = {b: max(0, tile_occupied[b]-2) for b in tiles}
    sparse_slack = sum(max(0, 2-tile_occupied[b]) for b in tiles)
    incident = defaultdict(list)
    loops = defaultdict(list)
    between = defaultdict(list)
    for i, (u, v) in enumerate(matching):
        a, b = tile(u), tile(v)
        for z in {a, b}:
            incident[z].append(i)
        if a == b:
            loops[a].append(i)
        else:
            between[frozenset([a, b])].append(i)
    return dict(board=board, occupied=occupied, demand=demand,
                sparse_slack=sparse_slack, tile=tile, incident=incident,
                loops=loops, between=between, holes=board-occupied)


def verify_owner(data, matching, owner):
    assert set(owner) <= set(range(len(matching)))
    count = Counter(owner.values())
    for e, b in owner.items():
        assert e in data['incident'][b]
    assert all(count[b] >= d for b, d in data['demand'].items())
    # Turn owners into a broader endpoint charge certificate, one edge at a time.
    sigma = {}
    for i, (u, v) in enumerate(matching):
        if i not in owner:
            sigma[u] = sigma[v] = -1
        else:
            a, b = data['tile'](u), data['tile'](v)
            chosen = u if owner[i] == a else v
            sigma[u], sigma[v] = (1, -1) if chosen == u else (-1, 1)
        assert sigma[u]+sigma[v] <= 0
    for b, d in data['demand'].items():
        p = [u for u in sigma if data['tile'](u) == b]
        q_block = 2*sum(data['tile'](u) == b for u in data['occupied'])-len(p)-4
        assert q_block <= sum(sigma[u] for u in p)
    return dict(used_edges=len(owner), unused_edges=len(matching)-len(owner),
                exact_tile_demands=all(count[b] == d for b, d in data['demand'].items()))


def augment(data, owner, root):
    changed = dict(owner)
    seen = set()

    def visit(b):
        for e in data['incident'][b]:
            if e in seen:
                continue
            seen.add(e)
            if e not in changed or visit(changed[e]):
                changed[e] = b
                return True
        return False

    assert visit(root)
    return changed


def check_family(q):
    h, w, selected, matching, trace = turning_board(q)
    data = adapter(h, w, selected, matching)
    assert len(selected) == len(data['holes']) == 3
    assert len(matching) == 4*q+1 and len(selected)+len(matching) == 4*q+4
    assert len(trace) == len(set(trace)) == 2*q+2
    path_edges = []
    for a, b in zip(trace, trace[1:]):
        es = data['between'][frozenset([a, b])]
        assert len(es) == 1
        path_edges.append(es[0])
    assert sum(map(len, data['between'].values())) == len(path_edges) == 2*q+1
    for b in trace[:-1]:
        assert data['demand'][b] == len(data['loops'][b])+1
    terminal = trace[-1]
    assert data['demand'][terminal] == len(data['loops'][terminal]) == 1
    owner = {e: b for b, es in data['loops'].items() for e in es}
    owner.update({e: trace[k] for k, e in enumerate(path_edges)})
    final_check = verify_owner(data, matching, owner)
    assert final_check == dict(used_edges=4*q+1, unused_edges=0, exact_tile_demands=True)
    # Remove only the bottom-left selected vertex of the positive source tile.
    old_selected = selected-{(3, 2*q)}
    old_data = adapter(h, w, old_selected, matching)
    assert old_data['demand'][trace[0]] == 0 and data['sparse_slack'] == old_data['sparse_slack'] == 0
    reserve = data['loops'][terminal][0]
    baseline = {e: b for b, es in data['loops'].items() for e in es if e != reserve}
    baseline.update({e: trace[k+1] for k, e in enumerate(path_edges)})
    baseline_check = verify_owner(old_data, matching, baseline)
    assert baseline_check == dict(used_edges=4*q, unused_edges=1, exact_tile_demands=True)
    repaired = augment(data, baseline, trace[0])
    assert repaired == owner
    changed = {e for e in owner if baseline.get(e) != owner[e]}
    assert changed == set(path_edges) | {reserve} and len(changed) == 2*q+2
    assert set(baseline) <= set(repaired)
    # The source and terminal reserve tiles are physically adjacent.
    assert abs(trace[0][0]-terminal[0])+abs(trace[0][1]-terminal[1]) == 1
    return dict(q=q, height=h, width=w, J=len(selected)+len(matching),
                path_edges=len(path_edges), changed_owners=len(changed),
                previous_paid_edges_changed=len(path_edges), all_P_relays=2*q-1,
                adjacent_source_and_reserve_tiles=True,
                all_old_used_physical_edges_retained=True)


def orientation_obstruction():
    h, w, selected, matching, _ = turning_board(1)
    data = adapter(h, w, selected, matching)
    b = (0, 1)
    sigmas = []
    for direction in [0, 1]:
        all_sigma = {}
        for r in range(0, h, 2):
            for c in range(0, w, 2):
                word = {(i, j): 1 if (r+i, c+j) in selected else
                        2 if (r+i, c+j) in data['occupied'] else 0
                        for i in range(2) for j in range(2)}
                if direction:
                    word = {(j, i): d for (i, j), d in word.items()}
                _, sigma, _ = charges(word)
                all_sigma.update({(r+(j if direction else i), c+(i if direction else j)): x
                                  for (i, j), x in sigma.items()})
        sigmas.append(all_sigma)
    assert sigmas[0][1, 2] == sigmas[0][0, 2] == 0
    assert sigmas[1][1, 2] == -1 and sigmas[1][0, 2] == 1
    # Actual edge to the positive block forces V at b; edge to all-P forces H.
    assert sigmas[0][2, 2] == sigmas[1][2, 2] == 1
    assert sigmas[0][0, 1] == sigmas[1][0, 1] == 0
    return dict(status='PROVED_OBSTRUCTION', central_tile=b,
                forced_V_edge=[(1, 2), (2, 2)], forced_H_edge=[(0, 1), (0, 2)],
                scope='Per-tile H/V signed-charge choice cannot make every actual edge nonpositive; actual-edge ownership repairs this sharp board.')


def main():
    records = [check_family(q) for q in range(1, 51)]
    result = dict(status='PASS', sharp_family_controls=len(records),
                  smallest=records[0], largest=records[-1],
                  orientation_obstruction=orientation_obstruction(),
                  scope='Exact actual-coordinate and ownership checks of the written arbitrary-q turning relay and augmentation proof. No general Hall feasibility inferred from finite boards.',
                  not_claimed='Universal existence of ownership on every even-by-even grid; freezing; a universal 5/6 improvement.')
    (ROOT/'output/turning-edge-ownership.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result))


if __name__ == '__main__':
    main()
