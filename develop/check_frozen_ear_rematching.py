"""Solver-free freezing-preserving ear rematching and private-payments checks.

No solver is required. All-size statements have separate rank-lift,
alternating-path and private-resource proofs in the accompanying note.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_merger_completion_reserves import (
    STATES, additions, complete, feasible, frozen, frozen_certificate,
    inspect, load, neighbors, owner_data, residual_fixture, whole_bands,
    whole_support_data,
)
from check_rematching_receiver_flux import canonical

if not __debug__:
    raise RuntimeError('Run without -O.')

REMOVED=((7,14),(7,15))
ADDED=[((7,14),(8,14)),((7,15),(8,15)),((9,14),(9,15))]
NEW_T={(9,16),(10,14)}
NEW_P={(8,14),(8,15),(9,14),(9,15)}
LOST={(4,14,14),(4,15,15),(4,16,16),(5,14,14)}


def ear(current):
    assert REMOVED in canonical(current[3])
    assert not NEW_P & (current[2]|{v for e in current[3] for v in e})
    return (*current[:2],current[2]|NEW_T,
            [e for e in current[3] if tuple(sorted(e))!=REMOVED]+ADDED)


def intervals(current):
    d,meta,_=whole_support_data(current,whole_bands(current))
    return {(meta['intervals'][j]['band'],meta['intervals'][j]['first'],meta['intervals'][j]['last']) for j in d[4]}


def lifted_ranks(before):
    _,layers=frozen_certificate(before)
    old={tuple(w['endpoint']):i for i,layer in enumerate(layers) for w in layer}
    ranks={v:3*r for v,r in old.items()};u,v=REMOVED
    ranks.update({(8,14):3*old[v]+2,(8,15):3*old[u]+2,
                  (9,14):3*old[u]+1,(9,15):3*old[v]+1})
    return ranks


def check_ranks(current,ranks):
    mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    assert set(ranks)==set(mate)
    for v in mate:
        retained={w for w in neighbors(v) if w in current[2] or
                  (w in mate and ranks[mate[w]]<ranks[v])}
        assert len(retained)>=2


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True)
    a=ap.parse_args();_,base=load();totals=Counter();good=[];models={}
    fixture=json.loads((Path(__file__).resolve().parent/'fixtures/frozen_four_endpoint_ear_rematching.json').read_text())
    saved=(*fixture['shape'],set(map(tuple,fixture['selected'])),
           [tuple(map(tuple,e)) for e in fixture['matching']])
    expected=ear(base)
    assert saved[:3]==expected[:3] and canonical(saved[3])==canonical(expected[3])
    ranks={tuple(w['endpoint']):w['rank'] for w in fixture['strict_witnesses']}
    check_ranks(saved,ranks)
    mate={v:w for e in saved[3] for v,w in (e,e[::-1])}
    for record in fixture['strict_witnesses']:
        v=tuple(record['endpoint']);kept=list(map(tuple,record['kept_neighbors']))
        assert len(kept)==len(set(kept))==2
        assert all(w in set(neighbors(v)) and (w in saved[2] or
            (w in mate and ranks[mate[w]]<ranks[v])) for w in kept)
    path=list(map(tuple,fixture['right_alpha_path']))
    assert path[0]==(5,12) and path[-1]==(3,15) and len(set(path))==len(path)==16
    assert all((mate[u]==v if i%2==0 else (u[0]^1,u[1])==v)
               for i,(u,v) in enumerate(zip(path,path[1:])))
    totals['saved_fixture_and_strict_witnesses']=1
    for state in STATES:
        if state[0] in ('inner_beta','outer_beta'):
            continue
        cur=complete(base,state);ext=ear(cur)
        assert feasible(ext) and frozen(ext)
        ranks=lifted_ranks(cur);check_ranks(ext,ranks)
        assert canonical(cur[3])-canonical(ext[3])=={REMOVED}
        assert len(ext[3])==len(cur[3])+2 and len(ext[2])==len(cur[2])+2
        assert intervals(cur)-intervals(ext)==LOST and not intervals(ext)-intervals(cur)
        for label,x in [('before',cur),('after',ext)]:
            data,meta,_=whole_support_data(x,whole_bands(x));o,aa,bb,mm=owner_data(*data[:2])
            assert len(aa)==2 and len(bb)==(3 if state[0]=='cycle_beta' else 2)
            assert o[5,12]==o[3,15] in aa
            assert data[1][o[5,12]]==((3,15),(5,12))
        result=inspect(ext,whole_bands(ext),[0],totals,independent=True)
        assert result['full_value']==2 and result['full_cost']==int(state[0]=='cycle_beta')
        models[state[0]]=dict(new_selections=sorted(NEW_T),new_endpoints=sorted(NEW_P),
            removed=[REMOVED],added=ADDED,lost_original_intervals=sorted(LOST),
            objective_increase=4,interval_count_change=-4,alpha_change=0,beta_change=0,
            full_value=result['full_value'],full_cost=result['full_cost'])
        good.extend([(state,cur,False),(state,ext,True)])
        totals['concrete_ear_rank_lifts']+=1
        # Every feasible one-step monotone extension of the modified board.
        for tag,changed in additions(ext):
            totals['single_addition_candidates']+=1
            if not feasible(changed):
                continue
            totals['single_addition_feasible']+=1
            if not frozen(changed):
                continue
            inspect(changed,whole_bands(changed),[0],totals)
            totals['single_addition_frozen']+=1
    # All eight choices (four cap states, with/without ear) in up to3 copies.
    for q in range(1,4):
        for choices in itertools.product(range(8),repeat=q):
            selected=set();matching=[];Iold=0;ears=0;filled=0
            for i,ch in enumerate(choices):
                state,cur,has_ear=good[ch];move=lambda v:(v[0]+14*i,v[1])
                selected|={move(v) for v in cur[2]}
                matching.extend(tuple(move(v) for v in e) for e in cur[3])
                Iold+=len(intervals(complete(base,state)));ears+=has_ear
                filled+=state[0]=='cycle_beta'
            joined=(14*q,18,selected,matching)
            assert len(intervals(joined))==Iold-4*ears
            record=inspect(joined,whole_bands(joined),[14*i for i in range(q)],totals,independent=q<=2)
            assert record['full_value']==2*q and record['full_cost']==filled
            totals['copy_choices']+=1
    # Nonempty residual problems remain fully in the allocation network.
    for state,cur,has_ear in good:
        if not has_ear:
            continue
        for h in (1,2,3):
            outside=residual_fixture(h,2);move=lambda v:(v[0]+14,v[1])
            joined=(14+outside[0],18,cur[2]|{move(v) for v in outside[2]},
                    cur[3]+[tuple(move(v) for v in e) for e in outside[3]])
            rec=inspect(joined,whole_bands(joined),[0],totals,independent=True)
            assert (rec['residual_value'],rec['residual_cost'])==(h,h)
            totals['positive_residual_controls']+=1
    rng=random.Random(2026102502)
    for state,initial,has_ear in good:
        if not has_ear:
            continue
        for run in range(8):
            cur=initial
            for depth in range(6):
                candidates=list(additions(cur));rng.shuffle(candidates)
                for _,changed in candidates:
                    if feasible(changed) and frozen(changed):
                        cur=changed;break
                else:
                    break
                inspect(cur,whole_bands(cur),[0],totals,independent=run==0 and depth==5)
                totals['multi_addition_frozen_prefixes']+=1
    # A tempting two-new-endpoint square flip cannot be frozen: each bottom
    # endpoint would need the selected site below it, and those sites conflict.
    h={(9,14),(9,15)}
    square=(*base[:2],base[2],
            [e for e in base[3] if tuple(sorted(e))!=REMOVED]+ADDED[:2])
    for flags in itertools.product((False,True),repeat=2):
        T=square[2]|{v for v,flag in zip(sorted(h),flags) if flag}
        current=(*square[:2],T,square[3])
        assert not (feasible(current) and frozen(current))
        totals['two_endpoint_square_support_controls']+=1
    a.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),models=models,
        scope='General rank lifting for four-endpoint matched-edge ear; actual old-matching-retention rule counterexample, NOT compensation counterexample. Four cap states and optional-ear all-q private-payment theorem with arbitrary further monotone feasible frozen extensions retaining modified T/M. Exact four original interval loss per ear, no new beta/alpha. Universal compensation and5/6 OPEN.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':
    main()
