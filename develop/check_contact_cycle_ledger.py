"""Compare the compressed permutation theorem with physical grid surgery.

General proofs, including all-size cycle rank and span credit, are in the note.
Finite controls never assert general grid coverage or a universal bound.
"""
from itertools import product, combinations
import json
from pathlib import Path

from check_mixed_terminal_compensation import (
    decompose, edge, grid, mates, selected_feasible,
)
from check_ordered_th_relay import all_gates

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def components(vertices, edges):
    adjacency = {v: set() for v in vertices}
    for a, b in edges:
        assert a in vertices and b in vertices
        adjacency[a].add(b); adjacency[b].add(a)
    unseen = set(vertices); result = []
    while unseen:
        found = {min(unseen)}; todo = list(found)
        while todo:
            for v in adjacency[todo.pop()] - found:
                found.add(v); todo.append(v)
        unseen -= found; result.append(found)
    return result


def analyse(h, w, m, n, t, gates):
    assert gates
    board = grid(h, w); m = set(m); n = set(n)
    before = decompose(board, m, n, t)
    assert selected_feasible(before['P'], t)
    affected_ids = set().union(*(g['ids'] for g in gates))
    alpha = {}; tau = {}; resources = {}; vertices = {}; terminal = {}; cut_orders = {}
    chosen_vertices = set(); nn = set(n)
    for j, g in enumerate(gates):
        assert len(g['ids']) == 2
        assert not chosen_vertices & g['vertices']; chosen_vertices |= g['vertices']
        assert not (g['old'] | g['new']) & m and g['old'] <= nn
        nn = nn - g['old'] | g['new']
        a, b = sorted(g['ids']); x, y = ('g', j, a), ('g', j, b)
        tau[x] = y; tau[y] = x
    affected = set(); old_th = set(); old_bad = set()
    for i in sorted(affected_ids):
        p = before['paths'][i]; pv = p['vertices']
        if sum(pv[0]) % 2:
            pv = list(reversed(pv))
        assert sum(pv[0]) % 2 == 0 and sum(pv[-1]) % 2 == 1
        terminal[i] = (pv[0], pv[-1]); affected |= set(pv)
        if p['kind'] == 'TH': old_th |= p['M']
        else: old_bad |= p['M']
        positions = {edge(a, b): j for j, (a, b) in enumerate(zip(pv, pv[1:]))}
        cuts = sorted((positions[g['cut'][i]], ('g', j, i))
                      for j, g in enumerate(gates) if i in g['ids'])
        assert all(pos % 2 == 0 for pos, _ in cuts)
        cut_orders[i] = [symbol[1] for _, symbol in cuts]
        symbols = [('s', i)] + [symbol for _, symbol in cuts]
        tau[('s', i)] = ('s', i)
        for a, b in zip(symbols, symbols[1:] + symbols[:1]): alpha[a] = b
        fragments = [pv[a:b+1] for a, b in zip(
            [0] + [pos+1 for pos, _ in cuts],
            [pos for pos, _ in cuts] + [len(pv)-1])]
        for symbol, fragment in zip(symbols, fragments):
            vertices[symbol] = set(fragment)
            resources[symbol] = {e for e in m if set(e) <= set(fragment)}
    assert set(alpha) == set(tau) == set(vertices)
    assert len(alpha) == len(affected_ids) + 2*len(gates)
    assert sum(map(len, vertices.values())) == len(affected)
    assert set().union(*vertices.values()) == affected
    assert sum(map(len, resources.values())) == len(old_th | old_bad)
    assert set().union(*resources.values()) == old_th | old_bad
    f = {x: alpha[tau[x]] for x in alpha}; assert set(f.values()) == set(f)
    unseen = set(f); predicted_paths = {}; predicted_cycles = {}; pi = {}
    while unseen:
        first = min(unseen); orbit = []; x = first
        while x not in orbit:
            orbit.append(x); unseen.remove(x); x = f[x]
        assert x == first
        markers = [j for j, x in enumerate(orbit) if x[0] == 's']
        if not markers:
            vs = frozenset().union(*(vertices[tau[x]] for x in orbit))
            rs = frozenset().union(*(resources[tau[x]] for x in orbit))
            predicted_cycles[vs] = rs
        else:
            for j in markers:
                x = orbit[j]; start = x[1]; vs = set(); rs = set()
                while True:
                    vs |= vertices[tau[x]]; rs |= resources[tau[x]]
                    x = f[x]
                    if x[0] == 's': break
                endpoints = (terminal[start][0], terminal[x[1]][1])
                pi[start] = x[1]
                assert set(endpoints) <= vs
                predicted_paths[frozenset(vs)] = (frozenset(rs), frozenset(endpoints))
    after = decompose(board, m, nn, t)
    output_paths = [p for p in after['paths'] if set(p['vertices']) & affected]
    actual_paths = {frozenset(p['vertices']): (frozenset(p['M']),
                    frozenset([p['vertices'][0], p['vertices'][-1]])) for p in output_paths}
    assert predicted_paths == actual_paths
    assert len(output_paths) == len(affected_ids)
    cycle_vertices = after['remainder'] & affected
    actual_cycle_sets = components(cycle_vertices,
        {e for e in m | nn if set(e) <= cycle_vertices})
    actual_cycles = {frozenset(vs): frozenset(e for e in m if set(e) <= vs)
                     for vs in actual_cycle_sets}
    assert predicted_cycles == actual_cycles
    graph_edges = [tuple(g['ids']) for g in gates]
    cc = len(components(affected_ids, graph_edges))
    rank = len(gates) - len(affected_ids) + cc
    assert len(actual_cycles) <= rank
    assert set(pi) == set(pi.values()) == affected_ids
    routing_cycles = len(components(affected_ids, list(pi.items())))
    assert (len(actual_cycles)+routing_cycles-len(affected_ids)-len(gates)) % 2 == 0
    if len(affected_ids) == len(gates) == 2:
        i,j = sorted(affected_ids)
        same_order = cut_orders[i] == cut_orders[j]
        assert cut_orders[i] == cut_orders[j] or cut_orders[i] == cut_orders[j][::-1]
        assert (pi[i] == i) == same_order
        assert len(actual_cycles) == int(not same_order)
    paid = set().union(*(p['M'] for p in output_paths if p['kind'] == 'TH'))
    bad = set().union(*(p['M'] for p in output_paths if p['kind'] != 'TH'))
    cycle_m = set().union(*actual_cycles.values())
    assert not paid & bad and not paid & cycle_m and not bad & cycle_m
    assert old_th | old_bad == paid | bad | cycle_m
    assert len(paid)-len(old_th) == len(old_bad)-len(bad)-len(cycle_m)
    assert set(m) & nn == m & n
    normalized = {e for e in nn if not set(e) <= cycle_vertices} | cycle_m
    mates(board, normalized, full=True)
    normal_data = decompose(board, m, normalized, t)
    assert normal_data['counts'] == after['counts']
    assert [(p['vertices'],p['M']) for p in normal_data['paths']] == [
        (p['vertices'],p['M']) for p in after['paths']]
    assert m & normalized == (m & n) | cycle_m
    assert not (m & n) & cycle_m
    a0,b0,t0 = before['counts']; a1,b1,t1 = after['counts']
    assert a0-a1 == b0-b1 and t1-t0 == 2*(a0-a1)
    return dict(before=before['counts'],after=after['counts'],
                original_paths=len(affected_ids),contacts=len(gates),
                contact_rank=rank,cycles=len(actual_cycles),cycle_M=len(cycle_m),
                old_TH_M=len(old_th),old_bad_M=len(old_bad),new_TH_M=len(paid),
                new_bad_M=len(bad),symbols=len(f))


def row_family(h, w, selection='TT'):
    assert h % 2 == w % 2 == 0 and h >= 4 and w >= 4
    m = {edge((r,c),(r,c+1)) for r in range(1,h-1) for c in range(1,w-2,2)}
    n = {edge((r,c),(r,c+1)) for r in range(h) for c in range(0,w,2)}
    if selection == 'TT':
        t = {(r,c) for r in range(1,h-1,2) for c in (0,w-1)}
    else:
        assert selection == 'TH'
        t = {(r,0 if r % 2 else w-1) for r in range(1,h-1)}
    d = decompose(grid(h,w),m,n,t)
    assert selected_feasible(d['P'],t)
    return m,n,t,all_gates(h,w,n,d)


def ladder(w, columns):
    m,n,t,allg = row_family(4,w)
    gates = [g for g in allg if g['square'][0] == 1 and g['square'][1] in columns]
    assert len(gates) == len(columns)
    result = analyse(4,w,m,n,t,gates)
    lo,hi = min(columns),max(columns)
    assert result['before'] == (1,w+1,0) and result['after'] == (0,w,2)
    assert result['cycles'] == len(columns)-1 == result['contact_rank']
    assert result['cycle_M'] == hi-lo
    assert result['new_TH_M'] == lo + w-2-hi
    assert result['old_bad_M'] == w-2 and result['new_bad_M'] == 0
    return result


def same_order_witness():
    """Actual feasible 8x6 same-order TT/HH fixture, with no search at runtime."""
    m = {
        edge((0,0),(1,0)), edge((0,1),(0,2)), edge((0,3),(0,4)),
        edge((0,5),(1,5)), edge((1,1),(1,2)), edge((2,0),(2,1)),
        edge((2,2),(3,2)), edge((2,3),(2,4)), edge((2,5),(3,5)),
        edge((3,0),(3,1)), edge((3,3),(4,3)), edge((3,4),(4,4)),
        edge((4,5),(5,5)), edge((6,5),(7,5)),
    }
    n = {
        edge((0,0),(0,1)), edge((0,2),(0,3)), edge((0,4),(0,5)),
        edge((1,0),(1,1)), edge((1,2),(1,3)), edge((1,4),(1,5)),
        edge((2,0),(3,0)), edge((2,1),(3,1)), edge((2,2),(2,3)),
        edge((2,4),(2,5)), edge((3,2),(3,3)), edge((3,4),(3,5)),
        edge((4,3),(5,3)), edge((4,4),(4,5)), edge((5,5),(6,5)),
        edge((7,5),(7,4)), edge((4,0),(4,1)), edge((4,2),(5,2)),
        edge((5,0),(5,1)), edge((5,4),(6,4)), edge((6,0),(6,1)),
        edge((6,2),(6,3)), edge((7,0),(7,1)), edge((7,2),(7,3)),
    }
    t = {(5,3),(7,4)}; data = decompose(grid(8,6),m,n,t)
    gates = [g for g in all_gates(8,6,n,data) if g['square'] in [(1,2),(1,4)]]
    assert len(gates) == 2
    single = [analyse(8,6,m,n,t,[g]) for g in gates]
    both = analyse(8,6,m,n,t,gates)
    assert both['before'] == both['after'] == (1,9,0)
    assert both['cycles'] == 0 and both['new_bad_M'] == 12
    assert all(r['after'] == (0,8,2) and r['new_TH_M'] == 12 for r in single)
    # Other certificates exist: these two adjacent hole payments use no M.
    payments = [edge((5,3),(6,3)),edge((7,4),(7,3))]
    assert len({v for e in payments for v in e}) == 4
    assert {(6,3),(7,3)} <= data['H']
    mates(grid(8,6),payments)
    return dict(h=8,w=6,M=sorted(m),N=sorted(n),T=sorted(t),
                squares=[g['square'] for g in gates],result=both,
                single_contact_results=single,zero_M_payments=payments)


def main():
    small = 0
    for w in range(4,19,2):
        columns = list(range(0,w,2))
        for k in range(1,len(columns)+1):
            for chosen in combinations(columns,k): ladder(w,chosen); small += 1
    long = []
    for s in range(1,81):
        w = 2*s+2
        for chosen in [[0,w-2],list(range(0,w,2)),[0]]:
            long.append(ladder(w,chosen))
    networks = 0; cyclic = 0; residual = 0; spanning_four = 0
    # At each column-pair choose a matching of the three possible row contacts.
    # The support condition is exact; these controls include mixed TT/HH and TH.
    patterns = [(),(1,),(2,),(3,),(1,3)]
    for selection in ['TT','TH']:
        h,w = 6,8; m,n,t,allg = row_family(h,w,selection)
        lookup = {g['square']:g for g in allg}
        for choices in product(patterns,repeat=w//2):
            gates = [lookup[(r,2*j)] for j,rows in enumerate(choices) for r in rows]
            if not gates: continue
            result = analyse(h,w,m,n,t,gates)
            networks += 1; cyclic += result['cycles']>0
            residual += result['after'][0]>0
            spanning_four += result['original_paths']==4
    assert cyclic and residual and spanning_four
    witness = same_order_witness()
    (ROOT/'output/two-contact-same-order-witness.json').write_text(
        json.dumps(witness,indent=2)+'\n')
    output=dict(status='PASS',small_ladder_subsets=small,
                long_family_controls=len(long),four_path_networks=networks,
                networks_with_cycles=cyclic,networks_with_residual_TT=residual,
                networks_affecting_four_original_paths=spanning_four,
                largest_sparse_credit=long[-3],largest_dense_credit=long[-2],
                largest_single_contact=long[-1],
                same_order_witness=witness['result'],
                verified='Exact compressed endpoint pairs, physical fragment and M-edge sets versus direct path/cycle decomposition; cycle-rank bound and permutation parity; two-contact order dichotomy; full N and feasible fixed M,T; exact signed ledger; safe normalization and retention identity.',
                trust_boundary='All-size permutation/forest/cycle-rank and span-credit results have written proofs. Finite actual grids test these proofs and the adapter; no universal coverage, universal5/6 improvement or general novelty of permutation surgery is claimed.')
    (ROOT/'output/contact-cycle-ledger.json').write_text(json.dumps(output,indent=2)+'\n')
    print(json.dumps(output))


if __name__ == '__main__': main()
