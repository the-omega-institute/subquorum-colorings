"""All-extension blank certificates and full-network mixed-cycle elimination.

General proof: docs/PERSISTENT_MIXED_CYCLE_BETA_CORE.md. No solver needed.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random
import re

from check_frozen_mixed_gate_cycle import load_model
from check_merger_completion_reserves import (
    additions, feasible, frozen, neighbors, owner_data, whole_bands, whole_support_data,
)
from check_frozen_beta_support_fork import restrict
from check_frozen_tip_slot_obstruction import fixture as residual_fixture, independent_strands
from check_reserve_boundary_split import clipped
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')

PRIMARY = [
    ((3,4),(3,5),(2,5)), ((3,19),(2,19),(2,20)),
    ((4,3),(4,4),(5,4)), ((4,5),(3,5),(2,5)),
    ((4,15),(3,15),(3,14)), ((4,16),(4,17),(5,17)),
    ((4,18),(4,17),(5,17)), ((4,20),(4,19),(5,19)),
    ((19,16),(19,15),(18,15)), ((21,16),(20,16),(20,17)),
    ((25,5),(25,4),(24,4)), ((25,18),(25,17),(24,17)),
]
ENCLOSED = [(3,3),(3,20),(21,17)]
SOURCE_TIPS = [(5,6),(5,19),(24,6),(5,4)]
GATE_TIPS = [(5,5),(5,18),(24,18),(24,5)]
BETA_TIPS = [(5,16),(5,20),(5,3),(18,16)]
WITNESS = [((5,17),(5,16)), ((5,19),(5,20)), ((5,4),(5,3)),
           ((24,17),(24,18)), ((18,15),(18,16))]


def certificate(base):
    oldP = {v for e in base[3] for v in e}
    oldT = base[2]
    blank = {q for q,t,w in PRIMARY}
    assert len(blank) == 12 and len(set(ENCLOSED)) == 3 and not blank & set(ENCLOSED)
    for q,t,w in PRIMARY:
        assert q not in oldT | oldP and t in oldT and w in oldT | oldP
        assert q != w and q in neighbors(t) and w in neighbors(t)
    stars = []
    for q in ENCLOSED:
        assert q not in oldT | oldP
        ps = sorted(set(neighbors(q)) & oldP)
        bs = sorted(set(neighbors(q)) & blank)
        assert len(ps) >= 2 and set(ps) | set(bs) == set(neighbors(q))
        stars.append(dict(point=q,old_endpoints=ps,guard_blanks=bs))
    old_data,_,_ = whole_support_data(base,whole_bands(base))
    own,_,_,_ = owner_data(*old_data[:2])
    owners = {own[v] for v in SOURCE_TIPS+GATE_TIPS+BETA_TIPS}
    _,components = independent_strands(base,whole_bands(base))
    bodies = {tip: next(body for tips,body in components if tip in tips)
              for tip in SOURCE_TIPS+GATE_TIPS+BETA_TIPS}
    required = {(v[0]^1,v[1]) for owner in owners for v in old_data[1][owner]
                if old_data[0][v] == 'BP'}
    assert len(required) == 12 and required <= blank | set(ENCLOSED)
    # Every future potential horizontal entry is certified by retained PP,
    # selected T, a fixed BP partner, or an internal-core old TP.
    entries = []
    for owner in owners:
        for v in old_data[1][owner]:
            if old_data[0][v] != 'BP':
                continue
            for w in ((v[0],v[1]-1),(v[0],v[1]+1)):
                q = (w[0]^1,w[1])
                if w in oldT:
                    reason = 'retained_selected_not_endpoint'
                elif w in oldP and q in oldP:
                    reason = 'retained_PP_not_TP'
                elif w in oldP and q in blank | set(ENCLOSED):
                    reason = 'permanent_BP_not_TP'
                else:
                    assert w in oldP and q in oldT and own[w] in owners
                    reason = 'retained_internal_core_TP'
                entries.append(dict(bp=v,side=w,partner=q,reason=reason))
    assert len(entries) == 24
    # Check the Lean coordinate adapter's local retained assumptions against
    # the actual fixture, rather than assuming that manually copied guards agree.
    lean = (Path(__file__).resolve().parents[1] /
            'formal/SubQuorum/PersistentMixedCycleBetaCore.lean').read_text()
    points = r'\((\d+),(\d+)\)'
    triples = lambda text:[tuple((int(v[i]),int(v[i+1])) for i in (0,2,4))
                           for v in re.findall('⟨'+points+','+points+','+points+'⟩',text)]
    assert triples(lean.split('def guards :')[1].split('def directBlanks')[0]) == PRIMARY
    formal_stars = triples(lean.split('def stars :')[1].split('def protectedBlanks')[0])
    assert [q for q,a,b in formal_stars] == ENCLOSED
    assert all({a,b} <= oldP and {a,b} <= set(neighbors(q)) and a != b for q,a,b in formal_stars)
    edge_text = lean.split('def guardMatching :')[1].split('def wall :')[0]
    formal_edges = [((int(a),int(b)),(int(c),int(d)))
                    for a,b,c,d in re.findall(r'\('+points+','+points+r'\)',edge_text)]
    assert len(formal_edges) == 7
    assert {tuple(sorted(e)) for e in formal_edges} <= {tuple(sorted(e)) for e in base[3]}
    formal_wall = {v for e in formal_edges for v in e}
    assert all(set(neighbors(q)) & oldP <= formal_wall for q in ENCLOSED)
    return dict(primary=PRIMARY,enclosed=stars,bp_side_checks=entries,required_terminal_blanks=sorted(required),
                lean_guard_matching=formal_edges,formal_adapter_matches_actual=True),bodies


def inspect(cur, base, moves, bodies, Qmode, totals, rng, independent=False):
    assert feasible(cur)
    old_edges = {tuple(sorted((move(u),move(v)))) for move in moves for u,v in base[3]}
    assert old_edges <= {tuple(sorted(e)) for e in cur[3]}
    assert all({move(v) for v in base[2]} <= cur[2] for move in moves)
    endpoints = {v for e in cur[3] for v in e}
    data,meta,_ = whole_support_data(cur,whole_bands(cur))
    own,alphas,betas,mixed = owner_data(*data[:2])
    _,components = independent_strands(cur,whole_bands(cur))
    body_for_tip = {v:body for tips,body in components for v in tips}
    core = set()
    sources = set()
    for move in moves:
        assert all(move(q) not in endpoints | cur[2] for q in [r[0] for r in PRIMARY]+ENCLOSED)
        ss = {own[move(v)] for v in SOURCE_TIPS}
        gg = {own[move(v)] for v in GATE_TIPS}
        bb = {own[move(v)] for v in BETA_TIPS}
        assert ss <= alphas and gg <= mixed and bb <= betas
        assert len(ss) == len(gg) == len(bb) == 4
        packet = ss | gg | bb
        assert len(packet) == 12 and not packet & core
        core |= packet
        sources |= ss
        for tip,body in bodies.items():
            assert body_for_tip[move(tip)] == {move(v) for v in body}
        assert all((move(u),move(v)) in data[2] for u,v in WITNESS)
    incoming = [(u,v) for u,v in data[2] if own[v] in core]
    assert all(own[u] in core for u,v in incoming)
    assert len(incoming) == 12*len(moves)
    if Qmode == 'empty':
        Q = set()
    elif Qmode == 'all':
        Q = data[4]
    elif Qmode == 'random':
        Q = {u for u in data[4] if rng.randrange(3)==0}
    else:
        assert isinstance(Qmode,tuple)
        Q = {meta['owner'][b,c] for b,c in Qmode}
    final = clipped(data,Q)
    residual = restrict(final,set(range(len(data[1])))-core,Q)
    _,ra,rb,rm = owner_data(*residual[:2])
    assert len(alphas)-len(ra) == len(betas)-len(rb) == len(mixed)-len(rm) == 4*len(moves)
    assert len(Q)+len(betas)-len(alphas) == len(Q)+len(rb)-len(ra)
    f = fork_flow(*final)
    r = fork_flow(*residual)
    assert f['value'] == 4*len(moves)+r['value']
    assert r['cost'] <= f['cost'] <= 5*len(moves)+r['cost']
    if independent:
        for allow in (False,True):
            ff = optimize(*final,allow_forks=allow)
            rr = optimize(*residual,allow_forks=allow)
            assert ff['value'] == 4*len(moves)+rr['value']
            assert rr['cost'] <= ff['cost'] <= 5*len(moves)+rr['cost']
            totals['independent_ordinary_full_eliminations'] += 1
    is_frozen = frozen(cur)
    totals['extension_availability_models'] += 1
    totals['completely_frozen_models' if is_frozen else 'feasible_nonfrozen_models'] += 1
    totals['preserved_original_strand_bodies'] += 12*len(moves)
    totals['nonempty_residual_source_models'] += bool(ra)
    totals['positive_residual_payment_models'] += r['value'] > 0
    return dict(value=f['value'],cost=f['cost'],residual_value=r['value'],residual_cost=r['cost'],
                frozen=is_frozen,alphas=len(alphas),betas=len(betas))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--output',type=Path,required=True)
    args = ap.parse_args()
    base,*_ = load_model()
    cert,bodies = certificate(base)
    totals = Counter()
    rng = random.Random(2026102522)
    identity = lambda v:v
    baseline = {}
    for label,mode in [('empty','empty'),('all','all'),('two_original',((6,15),(9,13))),('random','random')]:
        baseline[label] = inspect(base,base,[identity],bodies,mode,totals,rng,True)
    # All feasible single T/M additions. Nonfrozen states are retained and
    # labeled as such: the theorem only needs feasibility of the extension.
    feasible_extensions = []
    for tag,cur in additions(base):
        totals['single_addition_candidates'] += 1
        if not feasible(cur):
            continue
        feasible_extensions.append((tag,cur))
        record = inspect(cur,base,[identity],bodies,'random',totals,rng,
                         independent=len(feasible_extensions)<=12)
        totals['feasible_single_additions'] += 1
        totals['frozen_single_additions'] += record['frozen']
    # Arbitrary simultaneous additions, sampled by both feasibility-only and
    # frozen prefixes; every accepted prefix is checked, with final intervals.
    for frozen_required in (False,True):
        for trial in range(8):
            cur = base
            for depth in range(8):
                candidates = list(additions(cur))
                rng.shuffle(candidates)
                chosen = next((ext for tag,ext in candidates
                               if feasible(ext) and (not frozen_required or frozen(ext))),None)
                if chosen is None:
                    break
                cur = chosen
                inspect(cur,base,[identity],bodies,'empty' if depth%2 else 'random',totals,rng)
                totals['multi_addition_prefixes'] += 1
    # Coordinate certificates under both reflections and even translations.
    for vertical,horizontal,pad in itertools.product((False,True),(False,True),(0,2)):
        move = lambda v:(27-v[0]+pad if vertical else v[0]+pad,
                        23-v[1]+pad if horizontal else v[1]+pad)
        cur = (28+2*pad,24+2*pad,{move(v) for v in base[2]},
               [tuple(move(v) for v in e) for e in base[3]])
        inspect(cur,base,[move],bodies,'empty',totals,rng)
        totals['symmetry_padding_controls'] += 1
    # Multi-core final boards with independent outside alpha problems. The
    # final boundary and original interval pool are recomputed, not imported.
    for q in (1,2,3):
        moves = [(lambda v,shift=32*i+2:(v[0]+shift,v[1])) for i in range(q)]
        for h in (0,1,2,3):
            T = {move(v) for move in moves for v in base[2]}
            M = [tuple(move(v) for v in e) for move in moves for e in base[3]]
            rows,cols = 32*q,24
            if h:
                patch = residual_fixture(h)
                shift = lambda v:(v[0],v[1]+28)
                T |= {shift(v) for v in patch[2]}
                M += [tuple(shift(v) for v in e) for e in patch[3]]
                rows,cols = max(rows,patch[0]),44
            cur = (rows,cols,T,M)
            assert frozen(cur)
            for mode in ('empty','all','random'):
                record = inspect(cur,base,moves,bodies,mode,totals,rng,independent=q==1 and h<=2)
                assert record['residual_value'] == h
                totals['multi_core_exterior_controls'] += 1
    record = dict(status='PASS',certificate=cert,baseline=baseline,totals=dict(totals),
        scope='All feasible old-T-and-actual-M-retaining extensions preserve12protected original strands via15permanent blanks and24BPside checks. Closed core pays4with4distinctwholebetas5links, no intervals. Both ordinary/full V4q+Vres,cres<=c<=5q+cres for arbitrary final-original interval availability, with ledger unchanged. General proof independent of finite extensions; no arbitrary-rematching theorem or5over6 improvement.')
    args.output.write_text(json.dumps(record,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',baseline=baseline,totals=dict(totals))))


if __name__ == '__main__':
    main()
