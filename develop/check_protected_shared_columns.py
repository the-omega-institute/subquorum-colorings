"""Frozen long alpha columns, persistent shared units, and exact elimination.

The all-parameter and arbitrary-rematching proofs are in
docs/PROTECTED_SHARED_COLUMNS_AND_FRESH_ENDS.md. Finite controls corroborate
those proofs; they do not establish the universal compensation conjecture.
"""
import argparse
from collections import Counter
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_frozen_beta_support_fork import restrict
from check_frozen_shared_mixed_gate import check_rank_certificate, fixture as dense
from check_frozen_tip_slot_obstruction import fixture as costly
from check_merger_completion_reserves import additions, feasible, frozen
from check_promotion_cores import frozen_certificate
from check_whole_support_fork_normal_form import whole_support_data, ordinary_flow, optimize, owner_data
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_whole_support_fork_flow import fork_flow
from check_guarded_promotion_closure import load_model, inspect as promotion_inspect

if not __debug__:
    raise RuntimeError('Run without -O.')


def family(m, length, r=3, c=3, minimum_columns=18):
    assert m >= 1 and length >= 2 and r >= 3 and r % 2 == 1 and c >= 2
    cs = [c+3*i for i in range(m)]
    selected = {(r-1,x) for x in cs} | {(r+2*length,x) for x in cs}
    selected |= {(r+j,x+(-1 if j % 2 == 0 else 1))
                 for x in cs for j in range(2*length)}
    edges = [((r+2*i,x),(r+2*i+1,x)) for x in cs for i in range(length)]
    rows = r+2*length+5
    columns = max(minimum_columns, 2*((cs[-1]+6)//2))
    current = (rows, columns, selected, edges)
    layers = [[(r+2*k,x) for x in cs] + [(r+2*(length-k-1)+1,x) for x in cs]
              for k in range(length)]
    return current, layers


def shared_coordinates(m, length, r=3, c=3):
    return [(r//2,c+3*i+1) for i in range(m-1)] + [
        ((r+2*length-1)//2,c+3*i+2) for i in range(m-1)]


def join(top, bottom):
    assert top[0] % 2 == bottom[0] % 2 == 0
    move = lambda v: (v[0]+top[0],v[1])
    return (top[0]+bottom[0],max(top[1],bottom[1]),
            top[2] | {move(v) for v in bottom[2]},
            top[3]+[tuple(move(v) for v in e) for e in bottom[3]])


def inspect(current, m, length, totals, r=3, c=3, independent=False):
    assert feasible(current)
    d, meta, _ = whole_support_data(current,whole_bands(current))
    owner, alphas, _, _ = owner_data(*d[:2])
    endpoints = {v for e in current[3] for v in e}
    mate = {v:w for e in current[3] for v,w in (e,e[::-1])}
    old, _ = family(m,length,r,c,minimum_columns=current[1])
    old_p = {v for e in old[3] for v in e}
    # General fresh-tip separation lemma, corroborated here for the frozen
    # starting core. The full proof does not depend on this particular core.
    for v in endpoints-old_p:
        if (v[0]^1,v[1]) in current[2]:
            horizontal={(v[0],v[1]-1),(v[0],v[1]+1)}
            assert not horizontal & (old_p | old[2])
            totals['fresh_tip_separation_instances'] += 1
    selected_sources = {owner[r,c+3*i] for i in range(m)}
    assert len(selected_sources) == m and selected_sources <= alphas
    # The actual matching is not an extension hypothesis: it is a checked
    # consequence of the saturated-T collar and the even-path graph.
    for i in range(m):
        x = c+3*i
        a = owner[r,x]
        assert set(d[1][a]) == {(r,x),(r+2*length-1,x)}
        assert not any(owner[u] == a for u,v in d[2])
        for j in range(2*length):
            p = (r+j,x)
            guard = (r+j+(1 if j%2 == 0 else -1),x+(1 if j%2 == 0 else -1))
            anchor = (guard[0],x)
            blank = (r+j,guard[1])
            assert guard in current[2] and anchor in endpoints
            assert anchor in neighbors(guard) and blank in neighbors(guard) and anchor != blank
            assert blank not in current[2] | endpoints
            assert mate[p] == (r+j+(1 if j%2 == 0 else -1),x)
    units = set()
    for i in range(m-1):
        for b,x in ((r//2,c+3*i+1),((r+2*length-1)//2,c+3*i+2)):
            unit = meta['owner'][b,x]
            assert meta['intervals'][unit] == dict(band=b,first=x,last=x)
            assert unit in d[4]
            assert {o for o,js in d[3].items() if unit in js} == {owner[r,c+3*i],owner[r,c+3*(i+1)]}
            assert unit not in units
            units.add(unit)
    assert len(units) == 2*(m-1)
    if m >= 2:
        assigned = [(r//2,c+1),((r+2*length-1)//2,c+2)] + [
            (r//2,c+3*(i-1)+1) for i in range(2,m)]
        chosen = {meta['owner'][p] for p in assigned}
        assert len(chosen) == m
        assert all(meta['owner'][p] in d[3][owner[r,c+3*i]] for i,p in enumerate(assigned))
        keep = set(range(len(d[1])))-selected_sources
        full = fork_flow(*d)
        for deleted in (chosen,units):
            residual = restrict(d,keep,d[4]-deleted)
            rem = fork_flow(*residual)
            assert (full['value'],full['cost']) == (m+rem['value'],rem['cost'])
            ordinary = ordinary_flow(*d)
            ordinary_rem = ordinary_flow(*residual)
            assert (ordinary['value'],ordinary['cost']) == (m+ordinary_rem['value'],ordinary_rem['cost'])
            totals['ordinary_and_fork_exact_eliminations'] += 1
            if independent:
                for data in (d,residual):
                    brute = optimize(*data)
                    flow = fork_flow(*data)
                    assert (brute['value'],brute['cost']) == (flow['value'],flow['cost'])
                    totals['independent_primitive_comparisons'] += 1
        totals['positive_residual_cost_models'] += rem['cost'] > 0
        totals['nonempty_residual_alpha_models'] += bool(owner_data(*residual[:2])[1])
    is_frozen = frozen(current)
    totals['models'] += 1
    totals['frozen_models' if is_frozen else 'feasible_nonfrozen_models'] += 1


def square_flips(current):
    edges = {frozenset(e) for e in current[3]}
    for r in range(current[0]-1):
        for c in range(1,current[1]-1):
            a,b,d,e = (r,c),(r,c+1),(r+1,c),(r+1,c+1)
            horizontal = {frozenset((a,b)),frozenset((d,e))}
            vertical = {frozenset((a,d)),frozenset((b,e))}
            for old,new in ((horizontal,vertical),(vertical,horizontal)):
                if old <= edges:
                    yield (*current[:3],[tuple(sorted(x)) for x in sorted(edges-old | new,key=lambda e:sorted(e))])


def fresh_obstruction(m, length, totals):
    # A nonempty completely frozen old board with a fixed old-only payment
    # certificate. The new block lives in new bands; no old interval pays it.
    old,_ = family(2,2)
    new,_ = family(m,length)
    cur = join(old,new)
    assert feasible(cur) and frozen(cur)
    d,meta,_ = whole_support_data(cur,whole_bands(cur))
    old_d,old_meta,_ = whole_support_data(old,whole_bands(old))
    old_ids = {tuple(sorted(old_meta['intervals'][j].items())) for j in old_d[4]}
    retained = {j for j in d[4] if tuple(sorted(meta['intervals'][j].items())) in old_ids}
    owner,alphas,_,_ = owner_data(*d[:2])
    restricted = restrict(d,set(range(len(d[1]))),retained)
    assert ordinary_flow(*restricted)['value'] == 2
    assert ordinary_flow(*d)['value'] == m+2
    fresh_tips = {v for v in d[0] if v[0] >= old[0] and d[0][v] == 'TP'}
    assert len(fresh_tips) == 2*m
    # M symmetric-difference M0 consists of single matching edges; each has
    # at most one fresh TP although they form m fresh--fresh alpha strands.
    added_edges = [e for e in cur[3] if e[0][0] >= old[0]]
    assert all(len(set(e)&fresh_tips) <= 1 for e in added_edges)
    totals['frozen_matching_difference_counterexamples'] += 1
    return dict(m=m,length=length,fresh_TP=2*m,new_new_alpha=m,
                old_pool_deficit=m,full_pool_deficit=0,matching_difference_components=m*length)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    totals=Counter();examples=[]
    for m in range(1,7):
        for length in (2,3,4,7,12):
            cur,layers=family(m,length)
            check_rank_certificate(cur,layers)
            assert frozen_certificate(cur)[0] == {v for e in cur[3] for v in e}
            inspect(cur,m,length,totals,independent=m<=3 and length<=3)
            totals['explicit_rank_certificates'] += 1
    # All feasible single additions on a fixed rectangle, including final
    # nonfrozen boards. No matching-retention claim is inferred from these.
    base,_=family(2,2,minimum_columns=12)
    for tag,cur in additions(base):
        totals['single_addition_candidates'] += 1
        if feasible(cur):
            inspect(cur,2,2,totals)
            totals['single_addition_feasible'] += 1
    # Nonempty external compensation of strictly positive link cost.
    for m in (2,3,5):
        for length in (2,5):
            for h in (1,2,3):
                cur=join(family(m,length)[0],costly(h,2))
                inspect(cur,m,length,totals,independent=m==2 and h==1)
                totals['positive_cost_exterior_controls'] += 1
    # Actual rematching is allowed outside the rigid columns. These switch
    # sequences retain every selected/occupied site, not the old mates.
    rng=random.Random(2026102507)
    for m,length in ((2,2),(3,4)):
        cur=join(family(m,length)[0],dense())
        for step in range(40):
            candidates=list(square_flips(cur))
            assert candidates
            cur=rng.choice(candidates)
            inspect(cur,m,length,totals,independent=step in (0,39))
            totals['actual_rematching_controls'] += 1
    # Multiple new endpoints/selections, accepted solely on feasibility.
    for run in range(8):
        cur=base
        for depth in range(8):
            candidates=list(additions(cur));rng.shuffle(candidates)
            for tag,trial in candidates:
                if feasible(trial):
                    cur=trial;break
            else:raise AssertionError('No feasible extension')
            inspect(cur,2,2,totals)
            totals['multi_addition_prefixes'] += 1
    for m in range(1,7):
        examples.append(fresh_obstruction(m,2+m%3,totals))
    actual_base,*_=load_model()
    actual_examples=[];promotion_counts=Counter()
    old_layers=[[w['endpoint'] for w in layer] for layer in frozen_certificate(actual_base)[1]]
    for m in range(1,7):
        new,layers=family(m,2)
        cur=join(actual_base,new)
        check_rank_certificate(cur,old_layers+[
            [(v[0]+actual_base[0],v[1]) for v in layer] for layer in layers])
        result=promotion_inspect(actual_base,actual_base,cur,1,promotion_counts,full_pool=True)
        assert result['frozen'] and result['fresh_endpoint_tips']==2*m
        assert result['exact_certificate_loss']==result['ordinary_deficit']==m
        assert result['full_pool_deficit']==0
        actual_examples.append(result)
        totals['actual_308P_core_frozen_sharp_examples'] += 1
    stored=json.loads((Path(__file__).parent/'fixtures/protected_shared_columns_fresh_obstruction.json').read_text())
    cur=(*stored['shape'],set(map(tuple,stored['selected'])),[tuple(map(tuple,e)) for e in stored['matching']])
    old,old_layers=family(2,2);new,new_layers=family(2,2)
    assert cur==join(old,new)
    layers=[[tuple(v) for v in layer] for layer in stored['freezing_layers']]
    check_rank_certificate(cur,layers)
    assert frozen(cur) and feasible(cur)
    assert stored['old_matching']==[[list(v) for v in e] for e in old[3]]
    totals['permanent_frozen_fixture_rank_checks'] += 1
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),fresh_obstructions=examples,
        actual_308P_core_frozen_sharp_examples=actual_examples,promotion_adapter_counts=dict(promotion_counts),
        scope='All-parameter proof is separate. Frozen saturated-T collars force old mates under arbitrary feasible T/P retention and rematching. Shared internal units pay all m>=2 columns; exact ordinary/full elimination. Matching-difference rule fails on fully frozen boards. Universal compensation and numerical 5/6 improvement remain open.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__ == '__main__': main()
