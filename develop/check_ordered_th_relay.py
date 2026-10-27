"""Controls for the written ordered-TH relay theorem; no solver is required."""
from itertools import combinations
import json
from pathlib import Path

from check_mixed_terminal_compensation import (
    all_matchings, decompose, edge, grid, neighbours, selected_feasible,
    square_candidates,
)

if not __debug__:
    raise RuntimeError('Run this verifier with assertions enabled')

ROOT = Path(__file__).resolve().parents[1]


def all_gates(h, w, n, data):
    owner = {e: i for i, p in enumerate(data['paths']) for e in p['N']}
    result = []
    for r in range(h-1):
        for c in range(w-1):
            horizontal = {edge((r, c), (r, c+1)),
                          edge((r+1, c), (r+1, c+1))}
            vertical = {edge((r, c), (r+1, c)),
                        edge((r, c+1), (r+1, c+1))}
            for old, new in [(horizontal, vertical), (vertical, horizontal)]:
                if not old <= set(n) or not old <= owner.keys():
                    continue
                ids = {owner[e] for e in old}
                if len(ids) != 2:
                    continue
                result.append(dict(square=(r, c), old=old, new=new, ids=ids,
                                   cut={owner[e]: e for e in old},
                                   vertices={u for e in old for u in e}))
    return result


def relay(h, w, m, n, t, chain, gates, require_order=True):
    board = grid(h, w); before = decompose(board, m, n, t)
    paths = before['paths']; assert len(chain) >= 2
    assert len(set(chain)) == len(chain) and len(gates) == len(chain)-1
    assert paths[chain[0]]['kind'] == 'TT'
    assert paths[chain[-1]]['kind'] == 'HH'
    assert all(paths[i]['kind'] == 'TH' for i in chain[1:-1])
    vertices = set()
    for j, g in enumerate(gates):
        assert g['ids'] == {chain[j], chain[j+1]}
        assert not vertices & g['vertices']; vertices |= g['vertices']
        assert not g['old'] & set(m) and not g['new'] & set(m)
    orders = []
    for j, index in enumerate(chain[1:-1], 1):
        pv = paths[index]['vertices']
        if pv[-1] in t:
            pv = list(reversed(pv))
        assert pv[0] in t and pv[-1] in before['H']
        positions = {edge(u, v): k for k, (u, v) in enumerate(zip(pv, pv[1:]))}
        incoming = positions[gates[j-1]['cut'][index]]
        outgoing = positions[gates[j]['cut'][index]]
        assert incoming != outgoing
        orders.append((outgoing, incoming))
    correct = all(outgoing < incoming for outgoing, incoming in orders)
    if require_order:
        assert correct, orders
    current = set(n)
    for j, g in enumerate(gates):
        assert g['old'] <= current
        if correct:
            mid = decompose(board, m, sorted(current), t)
            own = {e: k for k, p in enumerate(mid['paths']) for e in p['N']}
            ids = [own[e] for e in g['old']]
            kinds = {mid['paths'][k]['kind'] for k in ids}
            assert len(set(ids)) == 2
            assert kinds == {'TT', 'HH' if j == len(gates)-1 else 'TH'}
        current = current-g['old'] | g['new']
        mid = decompose(board, m, sorted(current), t)
        assert before['path_M'] == mid['path_M']
        assert set(m) & set(n) == set(m) & current
    after = decompose(board, m, sorted(current), t)
    a, b, th = before['counts']
    if correct:
        assert after['counts'] == (a-1, b-1, th+2)
    else:
        # The first wrong gate strands a TT component in the affected chain.
        unaffected_tt = sum(paths[i]['kind'] == 'TT'
                            for i in range(len(paths)) if i not in chain)
        assert after['counts'][0] > unaffected_tt
    # A separate simultaneous construction checks commutation explicitly.
    simultaneous = (set(n)-set().union(*(g['old'] for g in gates)))
    simultaneous |= set().union(*(g['new'] for g in gates))
    assert simultaneous == current
    paid_t, paid_h, used = set(), set(), set()
    for p in after['paths']:
        if p['kind'] != 'TH':
            continue
        u, v = p['vertices'][0], p['vertices'][-1]
        if v in t:
            u, v = v, u
        assert u in t and v in before['H']
        assert u not in paid_t and v not in paid_h and not used & p['M']
        paid_t.add(u); paid_h.add(v); used |= p['M']
    return dict(correct_order=correct, orders=orders, before=before['counts'],
                after=after['counts'], initial_paid_M=len(set().union(
                    *(p['M'] for p in before['paths'] if p['kind'] == 'TH'))),
                final_paid_M=len(used), paid_T=len(paid_t),
                auxiliary=sorted(current), paths=after['paths'])


def family(r):
    assert r >= 1
    h, w = 2*r+2, 4
    m = {edge((0, 1), (0, 2))}
    n = {edge((0, 0), (0, 1)), edge((0, 2), (0, 3)),
         edge((2*r+1, 0), (2*r+1, 1)),
         edge((2*r+1, 2), (2*r+1, 3))}
    t = {(0, 0), (0, 3)}
    for i in range(1, r+1):
        upper, lower = 2*i-1, 2*i
        m.add(edge((upper, 2), (lower, 2)))
        n |= {edge((upper, c), (lower, c)) for c in (0, 1)}
        n |= {edge((row, 2), (row, 3)) for row in (upper, lower)}
        t.add((lower, 3))
    return h, w, sorted(m), sorted(n), t


def family_control(r):
    h, w, m, n, t = family(r); board = grid(h, w)
    p = {u for e in m for u in e}; assert selected_feasible(p, t)
    d = decompose(board, m, n, t)
    assert d['counts'] == (1, 2*r+2, r)
    assert not square_candidates(h, w, n, d)
    gates_by_square = {g['square']: g for g in all_gates(h, w, n, d)}
    gates = [gates_by_square[(2*i, 2)] for i in range(r+1)]
    chain = [next(i for i, x in enumerate(d['paths']) if x['kind'] == 'TT')]
    for g in gates:
        assert chain[-1] in g['ids']
        chain.append(next(i for i in g['ids'] if i != chain[-1]))
    result = relay(h, w, m, n, t, chain, gates)
    assert result['orders'] == [(0, 2)]*r
    assert result['after'] == (0, 2*r+1, r+2)
    assert result['initial_paid_M'] == r and result['final_paid_M'] == r+1
    long = [x for x in result['paths'] if x['kind'] == 'TH' and x['M']]
    assert len(long) == 1 and len(long[0]['M']) == r+1
    assert len(long[0]['vertices'])-1 == 2*r+3
    # This relay is a certificate, not a cost optimum: all T have direct payments.
    adjacent = [((0, 0), (1, 0)), ((0, 3), (1, 3))]
    adjacent += [((2*i, 3), (2*i+1, 3)) for i in range(1, r+1)]
    assert {u for u, v in adjacent} == t
    assert len({v for u, v in adjacent}) == len(t)
    assert all(v in d['H'] and v in neighbours(u) for u, v in adjacent)
    assert len(t) == r+2 and len(d['H']) == 5*r+4 and len(m) == r+1
    assert len(t)+len(m) == len(board)//2-(2*r+1)
    return dict(relays=r, height=h, T=len(t), H=len(d['H']), M=len(m),
                direct_TT_HH_square_edges=0, specified_switches=r+1,
                before=d['counts'], after=result['after'],
                relay_paid_M=r+1, incremental_paid_M=1,
                optimal_unrestricted_payment_cost=0,
                J=len(t)+len(m), half_area_margin=2*r+1)


def packed_control(q, r):
    """Actual separated copies, including the full auxiliary matching on gaps."""
    h, _, source_m, source_n, source_t = family(r)
    w = 6*q-2; m = set(); n = set(); t = set()
    for j in range(q):
        shift = lambda u: (u[0], u[1]+6*j)
        m |= {edge(shift(u), shift(v)) for u, v in source_m}
        n |= {edge(shift(u), shift(v)) for u, v in source_n}
        t |= {shift(u) for u in source_t}
        if j < q-1:
            n |= {edge((row, col), (row+1, col))
                  for row in range(0, h, 2) for col in (6*j+4, 6*j+5)}
    board = grid(h, w); m = sorted(m); n = sorted(n)
    before = decompose(board, m, n, t); assert selected_feasible(before['P'], t)
    assert before['counts'] == (q, (2*q-1)*(2*r+2), q*r)
    assert not square_candidates(h, w, n, before)
    original_sets = []; physical = set(); initial_n = n
    for j in range(q):
        data = decompose(board, m, n, t)
        by_square = {g['square']: g for g in all_gates(h, w, n, data)}
        gates = [by_square[(2*i, 6*j+2)] for i in range(r+1)]
        chain = [next(i for i, p in enumerate(data['paths'])
                      if p['kind'] == 'TT' and (0, 6*j) in p['vertices'])]
        for g in gates:
            chain.append(next(k for k in g['ids'] if k != chain[-1]))
        old_vertices = set().union(*(set(data['paths'][k]['vertices']) for k in chain))
        assert not physical & old_vertices; physical |= old_vertices
        original_sets.append(old_vertices)
        result = relay(h, w, m, n, t, chain, gates)
        n = result['auxiliary']
    final = decompose(board, m, n, t)
    assert final['counts'] == (0, (2*q-1)*(2*r+2)-q, q*(r+2))
    assert set(m) & set(initial_n) == set(m) & set(n)
    assert final['path_M'] == before['path_M']
    used = set().union(*(p['M'] for p in final['paths'] if p['kind'] == 'TH'))
    assert len(used) == q*(r+1)
    return dict(chains=q, intermediate_paths_each=r,
                before=before['counts'], after=final['counts'],
                final_paid_M=len(used), incremental_paid_M=q)


def wrong_order_control():
    h, w = 6, 12; board = grid(h, w)
    a = [(1, c) for c in range(1, 11)]
    c = [(4, 3), (3, 3)]+[(2, col) for col in range(3, 9)]+[(3, 8), (4, 8)]
    b = [(3, 5), (3, 6)]
    m = sorted({edge(p[i], p[i+1]) for p in (a, c, b)
                for i in range(1, len(p)-1, 2)})
    extra = [((0,0),(1,0)), ((0,1),(0,2)), ((0,3),(0,4)),
             ((0,5),(0,6)), ((0,7),(0,8)), ((0,9),(0,10)),
             ((0,11),(1,11)), ((2,0),(2,1)), ((2,2),(3,2)),
             ((2,9),(2,10)), ((2,11),(3,11)), ((3,0),(3,1)),
             ((3,4),(4,4)), ((3,7),(4,7)), ((3,9),(4,9)),
             ((3,10),(4,10)), ((4,0),(5,0)), ((4,1),(4,2)),
             ((4,5),(5,5)), ((4,6),(5,6)), ((4,11),(5,11)),
             ((5,1),(5,2)), ((5,3),(5,4)), ((5,7),(5,8)), ((5,9),(5,10))]
    n = sorted({edge(p[i], p[i+1]) for p in (a, c, b)
                for i in range(0, len(p)-1, 2)} | {edge(*e) for e in extra})
    t = {a[0], a[-1], c[0]}; p = {u for e in m for u in e}
    assert selected_feasible(p, t)
    d = decompose(board, m, n, t)
    chain = [next(i for i, path in enumerate(d['paths'])
                  if set(path['vertices']) == set(pv)) for pv in (a, c, b)]
    by_square = {g['square']: g for g in all_gates(h, w, n, d)}
    result = relay(h, w, m, n, t, chain,
                   [by_square[(1, 3)], by_square[(2, 5)]], require_order=False)
    assert not result['correct_order'] and result['orders'] == [(4, 2)]
    assert result['before'] == result['after'] == (1, 26, 1)
    remaining = [p['vertices'] for p in result['paths'] if p['kind'] == 'TT']
    assert len(remaining) == 1 and set((remaining[0][0], remaining[0][-1])) == {(1,1),(4,3)}
    # Explicit zero-M payments refute any suggestion of target/payment failure.
    for u, v in [((1,1),(0,1)), ((1,10),(0,10)), ((4,3),(5,3))]:
        assert u in t and v in d['H'] and v in neighbours(u)
    return dict(height=h, width=w, feasible=True, M=m, N=n, T=sorted(t),
                original_paths=dict(TT=a, TH_from_T=c, HH=b),
                witness_squares=[(1,3),(2,5)], gate_outgoing_incoming=[4,2],
                before=result['before'], after=result['after'],
                stranded_TT_endpoints=[(1,1),(4,3)],
                optimal_payment_cost=0, J=len(t)+len(m), area=72,
                failure_scope='The two specified disjoint square switches with wrong TH port order; not all possible certificates or the numerical target.')


def exhaustive_small_controls():
    board = grid(2, 4); ns = list(all_matchings(board))
    good = bad = feasible = 0
    for m in all_matchings(board, partial=True):
        for n in ns:
            initial = decompose(board, m, n, set())
            gg = all_gates(2, 4, n, initial)
            for g1, g2 in combinations(gg, 2):
                if g1['vertices'] & g2['vertices']:
                    continue
                mid = g1['ids'] & g2['ids']
                if len(mid) != 1:
                    continue
                c = next(iter(mid)); endpoints = [next(iter(g['ids']-{c})) for g in (g1,g2)]
                if endpoints[0] == endpoints[1]:
                    continue
                paths = initial['paths']
                for aa, bb, gates in [(endpoints[0], endpoints[1], [g1,g2]),
                                      (endpoints[1], endpoints[0], [g2,g1])]:
                    for ct in (paths[c]['vertices'][0], paths[c]['vertices'][-1]):
                        t = {paths[aa]['vertices'][0], paths[aa]['vertices'][-1], ct}
                        out = relay(2, 4, m, n, t, [aa,c,bb], gates, require_order=False)
                        good += out['correct_order']; bad += not out['correct_order']
                        feasible += selected_feasible(initial['P'], t)
    assert good > 0 and bad > 0
    return dict(correct_order=good, wrong_order=bad,
                feasible_among_these_tiny_matching_controls=feasible,
                scope='All partial M/full N/two-gate three-path relays on 2x4; feasibility not assumed for matching-only controls.')


def order_word_controls():
    """Every assignment of TH terminal orientation on short relay chains."""
    good = bad = 0
    for r in range(1, 9):
        h, w, m, n, original_t = family(r)
        for word in range(1 << r):
            t = {(0,0), (0,3)}
            t |= {(2*i-1 if word >> (i-1) & 1 else 2*i, 3)
                  for i in range(1, r+1)}
            d = decompose(grid(h,w), m, n, t)
            gg = {g['square']: g for g in all_gates(h,w,n,d)}
            gates = [gg[(2*i,2)] for i in range(r+1)]
            chain = [next(i for i,p in enumerate(d['paths']) if p['kind']=='TT')]
            for g in gates:
                chain.append(next(i for i in g['ids'] if i != chain[-1]))
            result = relay(h,w,m,n,t,chain,gates,require_order=False)
            assert result['correct_order'] == (word == 0)
            good += word == 0; bad += word != 0
    return dict(correct_words=good, failing_words=bad,
                scope='Matching-only controls for all TH orientations at r1..8; flipped selections need not be sub-quorum feasible.')


def main():
    small = exhaustive_small_controls()
    words = order_word_controls()
    rows = [family_control(r) for r in range(1, 81)]
    packed = [packed_control(q, r) for q in range(1, 9) for r in (1, 2, 3, 5, 8)]
    wrong = wrong_order_control()
    result = dict(status='PASS', small_matching_controls=small, contact_order_words=words,
                  actual_family_parameters=len(rows), smallest=rows[0], largest=rows[-1],
                  actual_disjoint_chain_packing_controls=len(packed),
                  largest_packing=packed[-1],
                  feasible_wrong_order_obstruction=wrong,
                  trust_boundary='General iff port-order relay and component-disjoint chain packing are written proofs. Finite controls do not prove universal existence, optimality or a universal 5/6 improvement. The positive family deliberately has a cheaper zero-M payment, so no minimum relay-cost claim is made.')
    (ROOT/'output/ordered-th-relay.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(dict(status='PASS', small=small, order_words=words, family_parameters=len(rows),
                          packed_controls=len(packed), largest=rows[-1],
                          wrong_order_counts=wrong['after'])))


if __name__ == '__main__':
    main()
