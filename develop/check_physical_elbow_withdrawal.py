"""Full-pool physical rank-one elbow withdrawal; no solver dependencies.

The proof and the complete board specification are in
docs/PHYSICAL_ELBOW_WITHDRAWAL_OBSTRUCTION.md. Enumeration tests that
specification; it is not the proof of the arbitrary-stack conclusion.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_forced_mates_and_adjacent_maxima import configuration
from check_crossing_matching_ports import rectangle
from check_canonical_band_coarsening import canonical_bands, tile_directions, forests
from check_compensation_flow_normal_form import owner_data
from check_degree_changing_bent_completions import compile_model
from check_local_elbow_resource_transfer import adapter, omit
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')

# Rows 0 and 15 are empty. P is checked independently against the actual M.
BOARD = (
    '............................',
    '............................',
    '....T.T.T.T.T.PP............',
    '.....TPPPPPPPT..............',
    '....T..T.PPP...T.T.T.T.T.T..',
    '....T.T.TPPPT.TPPPPPPPPPT...',
    '.....T.T.PPP....T.PPP.T..T..',
    '....T.T.TPPP.T.T.TPPPT.T.T..',
    '.....T.T.PPPT.T.T.PPP.T.T...',
    '....T..PPPPP...T..PPPT.T.T..',
    '.....TPPPPPPPT...TPPP.T.T...',
    '....T.T.T.T.T.PP..PPPPP..T..',
    '..............T.TPPPPPPPT...',
    '...............T.T.T.T.T.T..',
    '............................',
    '............................',
)


def configuration_one():
    base = configuration(8, 1)
    maps = (lambda v: (v[0]+2, 15-v[1]),
            lambda v: (v[0]+4, v[1]+14))
    M = [tuple(f(v) for v in edge) for f in maps for edge in base[3]]
    M += [((5, 15), (5, 16)), ((2, 14), (2, 15)), ((11, 14), (11, 15))]
    assert len(BOARD) == 16 and all(len(row) == 28 for row in BOARD)
    T = {(r, c) for r, row in enumerate(BOARD) for c, x in enumerate(row) if x == 'T'}
    P = {(r, c) for r, row in enumerate(BOARD) for c, x in enumerate(row) if x == 'P'}
    assert P == {v for e in M for v in e}
    bits = {(r, c): ((2 <= r < 12 and 6 <= c < 12) or
                      (4 <= r < 14 and 18 <= c < 24) or (r, c) == (12, 12))
            for r in range(0, 16, 2) for c in range(0, 28, 2)}
    return (16, 28, T, M), bits


def stack(q):
    assert q >= 1
    base, bits = configuration_one()
    cur = (16*q, 28, {(r+16*i, c) for i in range(q) for r, c in base[2]},
           [tuple((r+16*i, c) for r, c in e) for i in range(q) for e in base[3]])
    tiles = {(r+16*i, c): v for i in range(q) for (r, c), v in bits.items()}
    regs = canonical_bands(*cur[:2], [rectangle(r, r+2, c, c+2, v)
                                     for (r, c), v in tiles.items()])
    return cur, regs


def check(q, actions, totals, independent=False):
    cur, regs = stack(q)
    R, C, T, M = cur
    direct_check(*cur)
    d, closed, N = compile_model(cur, regs)
    own, A, B, X = owner_data(*d[:2])
    targets = {own[16*i+3, 12] for i in range(q)}
    sources = {own[16*i+5, 17] for i in range(q)}
    witnesses = {own[16*i+5, 15] for i in range(q)}
    assert A == targets | sources and len(B) == 4*q and len(X) == 5*q
    assert not targets & sources and len(A) == 2*q
    assert all(not d[3][a] for a in A)
    assert len(d[4]) == 118*q
    assert len(T) == 67*q and len(M) == 37*q
    assert R*C//2-len(T)-len(M) == 120*q
    fs = forests(cur, regs)
    lost_by_i = {}
    for i in range(q):
        z = own[16*i+5, 15]
        assert set(closed[z]['body']) == {(16*i+5, 15), (16*i+5, 16)}
        assert d[0][16*i+5, 15] == 'TP' and d[0][16*i+5, 16] == 'BP'
        units = {j for j in d[4] if fs[j][1] == frozenset({(16*i+4, 13), (16*i+5, 13)})}
        assert len(units) == 1 and d[3][z] == units
        assert all({o for o, W in d[3].items() if j in W} == {z} for j in units)
        lost_by_i[i] = units
    external = {(p, t) for p, t in d[2] if own[p] != own[t]}
    reached = set(A)
    while True:
        extra = {own[t] for p, t in external if own[p] in reached} - reached
        if not extra:
            break
        reached |= extra
    assert reached == A | witnesses
    # Other mixed owners can have links, but are unreachable from every
    # source. Keep them and their resources in the complete model.
    assert {(p,t) for p,t in external if own[p] in reached} == {
        ((16*i+5,17),(16*i+5,16)) for i in range(q)}
    P = {v for e in M for v in e}
    frozen, layers = frozen_certificate(cur)
    unfrozen = {(16*i+r, c) for i in range(q) for r in (2, 11) for c in (14, 15)}
    assert P-frozen == unfrozen and len(frozen) == 70*q
    for a in A:
        assert set(closed[a]['body']) <= frozen
        for r, c in d[1][a]:
            assert len({(r+1,c), (r-1,c), (r,c+1), (r,c-1)} & (P | T)) == 3
    assert all(set(closed[z]['body']) <= frozen for z in witnesses)
    totals['strict_frozen_endpoints'] += len(frozen)

    bits = tile_directions(R, C, regs)
    for i in actions:
        bits[16*i+2, 12] = bits[16*i+4, 12] = True
    newregs = canonical_bands(R, C, [rectangle(r,r+2,c,c+2,v) for (r,c),v in bits.items()])
    new, newclosed, N1 = compile_model(cur, newregs)
    assert d[:2] == new[:2] and set(d[2]) == set(new[2])
    assert [o['body'] for o in closed] == [o['body'] for o in newclosed]
    f1 = forests(cur, newregs)
    cells1 = {f1[j][1] for j in new[4]}
    Q = {j for j in d[4] if fs[j][1] not in cells1}
    expected_lost = set().union(*(lost_by_i[i] for i in actions)) if actions else set()
    assert Q == expected_lost
    assert len(Q) == len(actions) and len(new[4]) == len(d[4])
    for i in range(q):
        a, b, z = own[16*i+3, 12], own[16*i+5, 17], own[16*i+5, 15]
        assert not new[3][b]
        assert bool(new[3][a]) == (i in actions)
        assert bool(new[3][z]) == (i not in actions)
        if i in actions:
            assert len(new[3][a]) == 1
            j = next(iter(new[3][a]))
            assert f1[j][1] == frozenset({(16*i+4, 12), (16*i+4, 13)})
            assert {o for o, W in new[3].items() if j in W} == {a}
    residual = omit(d, targets, d[4]-Q)
    models = ((d, (q, q)), (omit(d, targets), (q, q)),
              (residual, (q-len(actions), q-len(actions))),
              (new, (q, q-len(actions))))
    for model, expected in models:
        f = fork_flow(*model)
        assert (f['value'], f['cost']) == expected
        if independent:
            alt = optimize(*model)
            assert (alt['value'], alt['cost']) == expected
            totals['independent_primitive_optima'] += 1
    totals['physical_stack_action_profiles'] += 1
    totals['physical_rank_one_transfers'] += len(actions)
    return dict(copies=q, repaired_copies=sorted(actions), alpha=2*q, beta=4*q,
                raw_resources=118*q, selected=67*q, matching_edges=37*q,
                old_value=q, old_links=q, residual_value=q-len(actions),
                rank_loss=len(actions), new_value=q, new_links=q-len(actions),
                fully_frozen=False, frozen_endpoints=70*q, endpoints=74*q)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--output', type=Path, required=True)
    args = p.parse_args()
    totals = Counter()
    records = []
    for q in range(1, 5):
        for mask in range(1 << q):
            actions = {i for i in range(q) if mask >> i & 1}
            records.append(check(q, actions, totals, independent=q <= 3))
    for q in (8, 16, 32):
        for actions in (set(), {0}, set(range(0,q,2)), set(range(q))):
            records.append(check(q, actions, totals))
    # Normalize/refelect the board, then invoke the previous general adapter
    # with its independent full primitive optimizer. Physical orientation
    # symmetry is checked separately, not presumed by a resource-only model.
    cur, regs = stack(1)
    R, C = cur[:2]
    bits = tile_directions(R, C, regs)
    normalized = (R, C, {(r,C-1-c) for r,c in cur[2]},
                  [tuple((r,C-1-c) for r,c in e) for e in cur[3]])
    normregs = canonical_bands(R,C,[rectangle(r,r+2,C-c-2,C-c,v) for (r,c),v in bits.items()])
    a = adapter(normalized, normregs, 2, 14, True)
    assert (a['old_value'],a['minus_value'],a['rest_value'],a['new_value'],
            a['rank_loss'],a['delta'],a['old_essential_source']) == (1,1,0,1,1,1,0)
    totals['general_adapter_independent_optima'] += 4
    for transpose, flipr, flipc in itertools.product((False,True),repeat=3):
        shape,T,M = transformed(*cur,transpose,flipr,flipc)
        def point(v):
            r,c = v
            if flipr:r=R-1-r
            if flipc:c=C-1-c
            if transpose:r,c=c,r
            return r,c
        regions=[]
        for (r,c),v in bits.items():
            sites=[point((x,y)) for x in (r,r+1) for y in (c,c+1)]
            x0=min(x for x,y in sites);y0=min(y for x,y in sites)
            regions.append(rectangle(x0,x0+2,y0,y0+2,v != transpose))
        direct_check(*shape,T,M)
        model,_,_=compile_model((*shape,T,M),canonical_bands(*shape,regions))
        f=fork_flow(*model);alt=optimize(*model)
        assert (f['value'],f['cost']) == (alt['value'],alt['cost']) == (1,1)
        totals['dihedral_physical_controls'] += 1
    fixture=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],
                 tile_directions=[[r,c,int(v)] for (r,c),v in sorted(bits.items())],
                 patch=dict(row=2,column=12,reflected_horizontally=True),
                 expected=records[1])
    fixture_path=Path(__file__).parent/'fixtures/physical_elbow_rank_one.json'
    fixture_path.write_text(json.dumps(fixture,indent=2)+'\n')
    saved=json.loads(fixture_path.read_text())
    assert set(map(tuple,saved['selected'])) == cur[2]
    assert [tuple(map(tuple,e)) for e in saved['matching']] == cur[3]
    assert saved['expected'] == records[1]
    report=dict(status='PASS',counts=dict(totals),records=records,
                theorem='A feasible canonical mixed H/V full-pool physical elbow has delta=1, old target unpaid, and exact withdrawal rank loss1. Arbitrary q vertically separated copies and any action set F have old/new value q, residual value q-|F|, joint loss |F| and new minimum links q-|F|. All alpha bodies and the paying mixed owner are frozen, but four shield-beta endpoints per copy are not frozen.',
                limits=['Refutes automatic zero withdrawal loss from feasibility, canonical bands, local elbow hypotheses, or frozen degree-three alpha terminals.',
                        'Not a fully frozen-grid counterexample, not a numerical target-inequality counterexample, and not an optimized-direction obstruction.',
                        'No new end-to-end Lean claim: complete physical checks and independent primitive optimization accompany a readable finite construction and arbitrary-copy proof.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals)),indent=2))


if __name__ == '__main__':
    main()
