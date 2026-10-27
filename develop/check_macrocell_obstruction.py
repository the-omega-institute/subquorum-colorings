"""Check the written complete-port relaxation and physical coarsening gap.

Enumeration validates local/finite adapters, not the quantified all-size proof.
No numerical target or universal two-batch theorem is asserted.
"""
from collections import deque
from itertools import product
from pathlib import Path
import json

from check_general_square_ports import (
    all_matchings, all_squares, debt_compensation, edge, grid, mates,
    physical_state, PortNetwork, selected_feasible,
)
from check_unique_matching_hole_barrier import family

if not __debug__:
    raise RuntimeError('Run with assertions enabled')
ROOT = Path(__file__).resolve().parents[1]


class Flow:
    """Independent unit integral flow; distinct physical arcs retain identity."""
    def __init__(self):
        self.g = {}

    def add(self, u, v, capacity):
        self.g.setdefault(u, []); self.g.setdefault(v, [])
        if u == v:
            return None  # Self loops never improve source-sink value.
        i, j = len(self.g[u]), len(self.g[v])
        self.g[u].append([v, j, capacity])
        self.g[v].append([u, i, 0])
        return u, i, capacity

    def run(self, source, sink):
        value = 0
        while True:
            prev = {source: None}; todo = deque([source])
            while todo and sink not in prev:
                u = todo.popleft()
                for j, (v, _, cap) in enumerate(self.g[u]):
                    if cap and v not in prev:
                        prev[v] = u, j; todo.append(v)
            if sink not in prev:
                return value
            v = sink
            while v != source:
                u, j = prev[v]; _, reverse, _ = self.g[u][j]
                self.g[u][j][2] -= 1; self.g[v][reverse][2] += 1; v = u
            value += 1

    def used(self, handle):
        return 0 if handle is None else handle[2]-self.g[handle[0]][handle[1]][2]


def model(q, w):
    m, t = set(), set()
    _, oldm, oldt, _, _ = family(w)
    for k in range(q):
        shift = lambda v: (v[0]+8*k, v[1])
        m |= {edge(shift(a), shift(b)) for a, b in oldm}
        t |= {shift(v) for v in oldt}
    return grid(8*q, w), m, t


def horizontal(board):
    return {edge((r, c), (r, c+1)) for r, c in board if c % 2 == 0}


def relaxed_counts(board, m, n, t, cell):
    """Walk actual M and nongeometric, cell-confined complete-port N."""
    mm = mates(board, m); nm = {}
    for a, b in n:
        assert a not in nm and b not in nm and cell(a) == cell(b)
        assert sum(a) % 2 != sum(b) % 2
        nm[a], nm[b] = b, a
    assert nm.keys() == board
    unseen = board-mm.keys(); counts = [0, 0, 0]
    while unseen:
        start = min(unseen); v = start; seen = {start}
        while True:
            v = nm[v]; assert v not in seen; seen.add(v)
            if v not in mm:
                break
            v = mm[v]; assert v not in seen; seen.add(v)
        assert v in unseen and start != v
        unseen -= {start, v}
        counts[0 if start in t and v in t else 1 if start not in t and v not in t else 2] += 1
    return counts


def hall_defect(vertices, red):
    """Return a genuine same-bit local Hall witness, or None for a full lift."""
    for bit in [False, True]:
        black = sorted(v for v in vertices if sum(v) % 2 == 0 and (v in red) == bit)
        white = {v for v in vertices if sum(v) % 2 and (v in red) == bit}
        assert len(black) == len(white)
        for mask in range(1 << len(black)):
            a = {v for j, v in enumerate(black) if mask >> j & 1}
            image = {v for v in white if any(sum(abs(x-y) for x, y in zip(u, v)) == 1 for u in a)}
            if len(image) < len(a):
                return dict(bit=bit, black=sorted(a), neighbours=sorted(image), deficit=len(a)-len(image))
    return None


def coarse(board, m, t, enumerate_cuts=False):
    cell = lambda v: (v[0]//4, v[1]//2)
    ids = sorted({cell(v) for v in board}); p = {v for e in m for v in e}
    assert selected_feasible(p, t)
    tcount = {c: sum(cell(v) == c for v in t) for c in ids}
    pcount = {c: sum(cell(v) == c for v in p) for c in ids}
    internal = {c: sum(cell(a) == cell(b) == c for a, b in m) for c in ids}
    k = {c: 8-2*tcount[c]-pcount[c] for c in ids}
    slack = {c: 4-tcount[c]-internal[c] for c in ids}
    cross = [(cell(a), cell(b)) for a, b in m if cell(a) != cell(b)]
    debt = {c: max(-k[c], 0) for c in ids}; reserve = {c: max(k[c], 0) for c in ids}
    df = debt_compensation(ids, cross, debt, reserve)
    assert df['value'] == sum(debt.values()) and df['uncompensated'] == 0
    # Explicit certificate: two DISTINCT actual edges per active band; capacities
    # and receiving budgets checked by physical identity, including w=6.
    used = set(); received = {c: 0 for c in ids}
    for band in sorted({c[0] for c in ids if debt[c]}):
        n = max(c[1] for c in ids)+1
        for j, receiver in [(0, 1), (n-1, n-2)]:
            sender = band, j; target = band, receiver
            candidates = [e for e in m if {cell(e[0]), cell(e[1])} == {sender, target}]
            assert len(candidates) == 1 and candidates[0] not in used
            used.add(candidates[0]); received[target] += 1
    assert len(used) == sum(debt.values())
    assert all(received[c] <= reserve[c] for c in ids)

    f = Flow(); source, sink = ('source',), ('sink',)
    sources, sinks, arcs = {}, {}, {}
    for c in ids:
        f.g[c] = []
    for v in board-p:
        if sum(v) % 2 == 0 and v in t:
            sources[v] = f.add(source, cell(v), 1)
        elif sum(v) % 2 and v not in t:
            sinks[v] = f.add(cell(v), sink, 1)
    for e in sorted(m):
        a, b = e
        white, black = (a, b) if sum(a) % 2 else (b, a)
        arcs[e] = f.add(cell(white), cell(black), 1)
    value = f.run(source, sink); delta = len(sources)-value
    assert delta == 0
    redblack, redwhite = set(sources), {v for v, h in sinks.items() if f.used(h)}
    for e, h in arcs.items():
        if f.used(h):
            a, b = e
            white, black = (a, b) if sum(a) % 2 else (b, a)
            redblack.add(black); redwhite.add(white)
    nrel = set(); failed_hall = {}
    for c in ids:
        vertices = {v for v in board if cell(v) == c}
        witness = hall_defect(vertices, redblack | redwhite)
        if witness is not None:
            failed_hall[c] = witness
        for red in [False, True]:
            black = sorted(v for v in board if cell(v) == c and sum(v) % 2 == 0 and (v in redblack) == red)
            white = sorted(v for v in board if cell(v) == c and sum(v) % 2 and (v in redwhite) == red)
            assert len(black) == len(white)
            nrel |= {edge(a, b) for a, b in zip(black, white)}
    counts = relaxed_counts(board, m, nrel, t, cell)
    assert counts[0] == 0
    nongrid = [e for e in nrel if sum(abs(a-b) for a, b in zip(*e)) != 1]
    assert nongrid
    assert {c[0] for c in failed_hall} >= {c[0] for c in ids if debt[c]}
    cuts = 0
    if enumerate_cuts:
        best = 0
        for bits in range(1 << len(ids)):
            u = {c for j, c in enumerate(ids) if bits >> j & 1}
            region = {v for v in board if cell(v) in u}
            excess = len(t & region)+sum(set(e) <= region for e in m)-4*len(u)
            ecount = sum(a in u and b in u for a, b in cross)
            boundary = sum((a in u) != (b in u) for a, b in cross)
            assert excess == ecount-sum(slack[c] for c in u)
            assert 2*excess == sum(debt[c]-reserve[c] for c in u)-boundary
            assert excess <= 0; best = max(best, excess); cuts += 1
        assert best == delta
    return dict(relaxed_TT=delta, debt=sum(debt.values()), debt_flow=df['value'],
                explicit_single_use_edges=len(used), explicit_max_received=max(received.values()),
                relaxed_auxiliary_nongrid_edges=len(nongrid), regional_cuts=cuts,
                failed_local_Hall_cells=len(failed_hall),
                first_local_Hall_witness=dict(cell=min(failed_hall), **failed_hall[min(failed_hall)]))


def batch_controls(q, w, m, t, board):
    n0 = horizontal(board); initial = physical_state(board, m, n0, t)
    assert initial['data']['counts'][0] == q and len(initial['paid']) == 2*q
    gates = {g['square']: g for g in all_squares(8*q, w, n0)}
    pool = [gates[8*k-1, 2] for k in range(1, q)]
    net = PortNetwork(8*q, w, m, n0, t, pool)
    coverage = net.coverage(); state = net.actual(coverage['switches'])
    assert coverage['delta'] == 1 and state['data']['counts'][0] == 1
    assert len(state['paid']) == 2*q+(q-1)*(w//2-1)
    states = [initial]; n = set(n0)
    for parity in [0, 1]:
        by = {g['square']: g for g in all_squares(8*q, w, n)}
        used = set()
        for r in range(0, 8*q, 2):
            for c in range(parity, w-1, 2):
                g = by[r, c]; assert not used & g['vertices']; used |= g['vertices']
                n = n-g['old'] | g['new']
        states.append(physical_state(board, m, n, t))
    assert states[1]['data']['counts'][0] == q
    assert states[2]['data']['counts'][0] == 0 and not states[2]['paid']
    top = {e for e in m if all(v[0] % 8 == 0 for v in e)}
    mid = {e for e in m if all(v[0] % 8 == 1 for v in e)}
    side = m-top-mid
    assert states[0]['paid'] == side and states[0]['bad'] == top and states[0]['free'] == mid
    assert not states[1]['paid'] and states[1]['bad'] == m and not states[1]['free']
    assert not states[2]['paid'] and states[2]['bad'] == mid | side and states[2]['free'] == top
    for old, new in zip(states, states[1:]):
        assert len(new['paid'])-len(old['paid']) == len(old['bad'])-len(new['bad'])+len(old['free'])-len(new['free'])
    return dict(initial_TT=q, explicit_one_batch_TT=1,
                one_batch_paid_M=len(state['paid']), final_two_batch_TT=0,
                two_batch_paid_M=[len(s['paid']) for s in states], exact_resource_sets=True)


def local_controls():
    local = list(all_matchings(grid(4, 2))); assert len(local) == 5
    for n in local:
        nm = mates(grid(4, 2), n, full=True)
        assert ((nm[0, 0] == (0, 1) and nm[0, 1] == (0, 0)) or
                (nm[0, 0] == (1, 0) and nm[0, 1] == (1, 1)))
        assert nm[0, 1] == (0, 0) or (nm[0, 1] == (1, 1) and nm[2, 1] in {(2, 0), (3, 1)})
    profiles = 0; liftable = 0
    vertices = grid(4, 2); order = sorted(vertices)
    for mask in range(1 << len(order)):
        red = {v for j, v in enumerate(order) if mask >> j & 1}
        if sum(sum(v) % 2 == 0 for v in red) != sum(sum(v) % 2 == 1 for v in red):
            continue
        witness = hall_defect(vertices, red)
        realizable = any(all((a in red) == (b in red) for a, b in n) for n in local)
        assert (witness is None) == realizable
        profiles += 1; liftable += realizable
    assert profiles == 70
    return local, dict(balanced_local_bit_profiles=profiles, liftable_local_bit_profiles=liftable)


def exhaustive(local, q, w):
    board, m, t = model(q, w); minimum = q+1; models = 0
    # Exhaust active cells. All separator-cell phases are irrelevant: P=T=empty
    # there, and both M,N are confined away from the active bands.
    for choices in product(range(5), repeat=q*(w//2)):
        n = {e for e in horizontal(board) if e[0][0] % 8 >= 4}
        for k in range(q):
            for j in range(w//2):
                choice = choices[k*(w//2)+j]
                n |= {edge((a[0]+8*k, a[1]+2*j), (b[0]+8*k, b[1]+2*j)) for a, b in local[choice]}
        state = physical_state(board, m, n, t)
        assert state['data']['counts'][0] >= q
        minimum = min(minimum, state['data']['counts'][0]); models += 1
    assert minimum == q
    return dict(copies=q, width=w, active_cell_auxiliaries=models, exact_minimum_TT=minimum,
                separator_phases='Irrelevant by absence of M/T and cell confinement; fixed horizontal in enumeration')


def main():
    local, hall = local_controls(); rows = []
    for q, widths in [(1, range(6, 106, 2)), (2, range(6, 46, 2)), (3, range(6, 26, 2)),
                      (5, [6, 10, 20]), (10, [6, 10]), (25, [6])]:
        for w in widths:
            board, m, t = model(q, w)
            stats = coarse(board, m, t, enumerate_cuts=(q == 1 and w <= 10) or (q == 2 and w == 6))
            batches = batch_controls(q, w, m, t, board)
            assert len(m) == q*(w-1) and len(t) == q*w
            rows.append(dict(copies=q, width=w, M=len(m), T=len(t), physical_macrocell_minimum_TT=q,
                             **stats, **batches))
    controls = [exhaustive(local, 1, w) for w in [6, 8, 10]]+[exhaustive(local, 2, 6)]
    out = dict(status='PASS', actual_models=len(rows), local_domino_states=len(local), **hall,
               regional_cuts=sum(r['regional_cuts'] for r in rows),
               enumerated_active_cell_auxiliaries=sum(r['active_cell_auxiliaries'] for r in controls),
               exhaustive_controls=controls, families=rows,
               scope='Balanced-cell complete-port relaxation; capacity-respecting false macrocell certificates; physical forced-port/stacked gap; exact one/two-batch separation and actual M class sets.',
               trust_boundary='Quantified proofs are written; finite controls do not establish general geometry. Numerical 5/6 improvement and universal successive-batch coverage remain open.')
    (ROOT/'output/macrocell-obstruction.json').write_text(json.dumps(out, indent=2)+'\n')
    print(json.dumps({k:v for k,v in out.items() if k not in ['families', 'exhaustive_controls']}))


if __name__ == '__main__':
    main()
