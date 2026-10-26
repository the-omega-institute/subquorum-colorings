"""Exact simultaneous edge-capacity witness and periodic splice controls.

No optimization dependencies. The all-length argument is the periodic splice
and bounded support classification in the accompanying mathematical note.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_cooperative_promotion import neighbors
from check_connected_band_local_relaxation import connected_cells, WINDOWS, reduced
from check_connected_band_mate_coverage_barrier import POINT
from check_endpoint_invasion_sharp_strips import endpoints, free_vertices, edge_key
from check_lower_guard_merger_frontier import guard, lower_guard
from check_occupied_strip_degree_four_budget import family

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

ROOT = Path(__file__).resolve().parents[1]
DATA = json.loads((ROOT/'develop/fixtures/connected_band_fractional_matching_splice.json').read_text())
SCALE = 80
assert DATA['scale'] == SCALE and DATA['base_m'] == 8 and DATA['splice_column'] == 24


def read_part(part):
    ts = {tuple(v): q for v,q in part['T']}
    xs = {edge_key(tuple(map(tuple,e))): q for e,q in part['X']}
    assert len(ts) == len(part['T']) and len(xs) == len(part['X'])
    assert all(isinstance(q,int) and 0 < q <= SCALE for q in [*ts.values(),*xs.values()])
    return ts,xs


BASE_T,BASE_X = read_part(DATA['base'])
PERIOD_T,PERIOD_X = read_part(DATA['period'])


def domain(m):
    assert m >= 2
    old = family(m+1)[0]
    P0 = endpoints(old[3])
    R = old[2]-{guard(i) for i in range(m)}-{lower_guard(i) for i in range(m)}
    R -= {(4,12+6*i) for i in range(m-1)}
    U = free_vertices((*old[:2],R,old[3]))
    C = connected_cells(m)
    possible = U | P0
    es = {edge_key((v,u)) for v in possible for u in set(neighbors(v))&possible}
    return old,R,P0,U,C,es


def witness(m):
    assert m >= 8
    old,R,P0,U,C,es = domain(m)
    shift = 6*(m-8)
    split = 24
    def new_t(v):
        r,c = v
        if c < split: return BASE_T.get(v,0)
        if c >= split+shift: return BASE_T.get((r,c-shift),0)
        return PERIOD_T.get(reduced(v),0)
    def x(e):
        if all(c < split for r,c in e): return BASE_X.get(e,0)
        if all(c >= split+shift for r,c in e):
            return BASE_X.get(edge_key(tuple((r,c-shift) for r,c in e)),0)
        return PERIOD_X.get(edge_key(tuple(reduced(v) for v in e)),0)
    ts = {v:new_t(v) for v in U}
    xs = {e:x(e) for e in es}
    return (old,R,P0,U,C,es),ts,xs


def check(m,counts):
    (old,R,P0,U,C,es),ts,xs = witness(m)
    inc = Counter()
    for (v,u),q in xs.items():
        assert q >= 0 and abs(v[0]-u[0])+abs(v[1]-u[1]) == 1
        inc[v] += q; inc[u] += q
        counts['edge_capacity_checks'] += 1
    assert all(inc[v] == SCALE for v in P0)
    counts['old_endpoint_equalities'] += len(P0)
    assert all(not set(neighbors(v)) & R for v in U)
    assert len(R) == 5*m+14 and len(P0) == 8*m+10
    assert len(C) == 17*m-4 and len(U-C) == 17
    assert all(0 <= ts[v] <= ts[v]+inc[v] <= SCALE for v in U)
    o = lambda v: ts[v]+inc[v]
    for v in U:
        ns = set(neighbors(v)) & U
        b = len(set(neighbors(v)) & P0)
        if b >= 2: assert ts[v] == 0
        if b:
            assert all(ts[v]+o(u) <= SCALE for u in ns)
        for a,w in itertools.combinations(ns,2):
            assert ts[v]+o(a)+o(w) <= 2*SCALE
        assert (len(ns)+b-1)*ts[v]+sum(o(u) for u in ns) <= len(ns)*SCALE
        assert inc[v] <= b*SCALE+sum(inc[u] for u in ns)
        counts['free_vertex_checks'] += 1
        if v in C and v[0] == 5:
            assert sum(ts[u]+o(u) for u in ns|{v}) <= 6*SCALE
            counts['bottom_star_checks'] += 1
    # Independently check ordinary global occupation/selection inequalities,
    # including every retained selection, old endpoint and forced blank.
    board = set(itertools.product(range(6),range(6*m+10)))
    tall = lambda v: SCALE if v in R else ts.get(v,0)
    oall = lambda v: tall(v)+inc[v]
    for v in board:
        ns = set(neighbors(v)) & board
        assert 0 <= tall(v) <= oall(v) <= SCALE
        for a,w in itertools.combinations(ns,2):
            assert tall(v)+oall(a)+oall(w) <= 2*SCALE
        assert (len(ns)-1)*tall(v)+sum(oall(u) for u in ns) <= len(ns)*SCALE
        counts['whole_board_vertex_checks'] += 1
    for name,pat,bound in WINDOWS:
        for i in range(-2,m+2):
            S = {(r,c+9+6*i) for r,c in pat}
            if S <= C:
                assert sum(ts[v]+o(v) for v in S) <= bound*SCALE
                counts['window_checks'] += 1
    charge = sum(2*ts[v]+inc[v] for v in C)
    whole = SCALE*len(R)+sum(ts.values())+sum(xs.values())
    assert charge == 1548*m-315
    assert whole == 1494*m+1394
    assert whole-80*(18*m+29) == 54*m-926
    counts['finite_splice_controls'] += 1
    return dict(m=m,component_charge_scaled80=charge,whole_objective_scaled80=whole,
                whole_gap_scaled80=whole-80*(18*m+29))


def local_splice_proof_controls(counts):
    # The seed board agrees with the periodic point throughout columns20..40;
    # all window supports have horizontal diameter4, all vertex supports2.
    (old,R,P0,U,C,es),ts,xs = witness(8)
    assert set(BASE_T) <= U and set(BASE_X) <= es
    assert ts == {v:BASE_T.get(v,0) for v in U}
    assert xs == {e:BASE_X.get(e,0) for e in es}
    for v in U:
        if 20 <= v[1] <= 40: assert ts[v] == PERIOD_T.get(reduced(v),0)
    for e in es:
        if all(20 <= v[1] <= 40 for v in e):
            assert xs[e] == PERIOD_X.get(edge_key(tuple(reduced(v) for v in e)),0)
    assert max(max(c for r,c in pat)-min(c for r,c in pat) for _,pat,_ in WINDOWS)==4
    assert sum(PERIOD_T.values()) == 614
    assert sum(PERIOD_X.values()) == 480
    assert sum(BASE_T.values())+sum(BASE_X.values())+80*len(R) == 13346
    pphases = {reduced(v) for v in P0 if 20 <= v[1] <= 40}
    rphases = {reduced(v) for v in R if 20 <= v[1] <= 40}
    uphases = {reduced(v) for v in U if 20 <= v[1] <= 40}
    assert rphases == {(0,1),(0,3),(0,5),(1,2),(1,4)}
    assert uphases == set(POINT)
    assert set(PERIOD_T) <= uphases
    possible_phases = pphases | uphases
    for v,u in PERIOD_X:
        assert v in possible_phases and u in possible_phases
        assert u in {reduced(w) for w in neighbors(v) if 0 <= w[0] < 6}
    for c in range(20,41):
        for r in range(6):
            v=(r,c)
            assert (v in P0) == (reduced(v) in pphases)
            assert (v in R) == (reduced(v) in rphases)
            assert (v in U) == (reduced(v) in uphases)
    # New full periods contribute80*5+614+480=1494 to the board objective.
    assert 80*5+614+480 == 1494
    counts['exact_periodic_splice_adapter_checks'] += 1


def old92_hall_obstruction(m,counts):
    old,R,P0,U,C,es=domain(m)
    a=6*m
    A={(1,a+6),(2,a+5),(2,a+7),(3,a+6),(3,a+8)}
    N={(1,a+5),(1,a+7),(2,a+6),(3,a+5),(3,a+7)}
    assert {u for e in es for v,u in [e,e[::-1]] if v in A} == N
    assert A-{(2,a+5)} <= P0 and N-{(3,a+5)} <= P0
    p92=lambda v:92 if v in P0 else int(92*(POINT[reduced(v)][1]-POINT[reduced(v)][0]))
    assert sum(p92(v) for v in A)==460
    assert sum(p92(v) for v in N)==429
    counts['old92_exact_Hall_obstructions']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();local_splice_proof_controls(counts)
    for m in [2,3,8,18,128]:old92_hall_obstruction(m,counts)
    samples=[check(m,counts) for m in [*range(8,25),32,64,128]]
    out=dict(status='PASS',counts=dict(counts),scale=80,samples=samples,
             component_formula='(1548m-315)/80',whole_formula='(747m+697)/40',
             whole_gap_above_18m_plus29='(27m-463)/40; positive for every m>=18',
             old92_obstruction='Terminal Hall set A has endpoint demand460/92 but its entire neighbour set has429/92; deficit31/92. Independent of pocket values and valid at every m>=2 by translation.',
             scope='All-length written periodic-splice construction, m>=8. Exact rational simultaneous matching-edge variables saturate all old endpoints, obey shared vertex capacities, and satisfy the prior bounds/anchors/wedges/full-selected-degree/bottom-stars/four module-window system. The whole-board fractional objective exceeds18m+29 for every m>=18. Not an integer occupation, frozen configuration or whole-board integer counterexample. The all-length coordinate and bounded-support classification is a written proof, with exact finite controls through128; no LP output is accepted as proof.')
    args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts),first=samples[0],m18=samples[10]),indent=2))


if __name__ == '__main__': main()
