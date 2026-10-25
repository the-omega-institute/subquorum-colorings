"""Fixed-rectangle residual-domain theorem: local audit and actual M/PP/C checks.

Proof for every extension: docs/RESIDUAL_FRESH_DOMAINS.md.
No solver dependency; the saved nonfrozen witness is checked from scratch.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_conditional_fresh_tip_closure import (load_model, PROTECTED, partner,
    endpoints, inspect, activate, augment_with_selection, frozen_caps, square_switches)
from check_endpoint_extension_replacement import FLEX, static_certificate
from check_cooperative_promotion import neighbors
from check_merger_completion_reserves import feasible, whole_bands, whole_support_data
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import ordinary_flow
from check_promotion_cores import frozen_certificate
from check_frozen_shared_mixed_gate import check_rank_certificate

if not __debug__: raise RuntimeError('Run without -O.')
H={(17,9),(26,13),(26,14),(26,15)}
VERTICAL={(1,16),(1,17),(16,9)}|H

def color(v): return sum(v)%2

def transverse(v): return (v[0]+(-1 if v[0]%2==0 else 1),v[1])

def geometry(base):
    board={(r,c) for r in range(28) for c in range(24)}
    P0=endpoints(base);O=P0|base[2];old,_=static_certificate(base)
    F={v for v in board if v[1]==0 or (v not in O and set(neighbors(v))&base[2])}
    Q={t[1] for t in old}|{w for v,w in FLEX}|{(3,13)}|{w for v,w in PROTECTED}
    potential={v for v in board if 0<v[1]<23 and v not in O and partner(v) not in O
      and not set(neighbors(partner(v)))&O and not set(neighbors(v))&base[2]}
    S=potential-{v for v,w in PROTECTED}
    expected={(0,c) for c in range(14,19)}|{(1,c) for c in (15,16,17)}|{(16,8),(16,9),(17,9)}
    expected|={(r,c) for r in (26,27) for c in (1,3,5,7,9,10,12,13,14,15,16,18,20,22)}
    assert S==expected and len(potential)==66 and len(S)==39
    assert not {(v,u) for v in S for u in Q if v[0]==u[0] and u in neighbors(v)}
    vertical={v for v in S if transverse(v) in board-F}
    assert vertical==VERTICAL
    records=[]
    for v in sorted(vertical):
        u=transverse(v);available=set(neighbors(u))&board-F
        assert u not in Q
        if v not in H: assert partner(u) in F
        records.append(dict(tip=v,mate=u,mate_partner_forced_blank=partner(u) in F,
                            max_occupied_degree=len(available),possible_occupied_neighbors=sorted(available)))
    assert set(neighbors((18,9)))&board-F=={(17,9),(19,9)}
    # Adjacent bottom tips would force adjacent selections, each seeing its own P.
    assert partner((26,14)) in neighbors(partner((26,13)))
    assert partner((26,14)) in neighbors(partner((26,15)))
    return S,F,Q,dict(potential_count=len(potential),unprotected=sorted(S),vertical_cases=records,
                      final_alpha_hole_domain=sorted(H),degree_two_mate=(18,9))


def check(base,cur,S,F,Q,totals,independent=False):
    assert cur[:2]==(28,24) and feasible(cur)
    result=inspect(base,base,cur,1,totals,independent)
    P=endpoints(cur);assert not F&(P|cur[2])
    d,_,_=whole_support_data(cur,whole_bands(cur));old,_=static_certificate(base)
    tips={v for v,k in d[0].items() if k=='TP'}
    holes=(tips-endpoints(base))-{v for v,w in PROTECTED}
    assert holes<=S
    C=[(v,t[1]) for t,v in old.items()]
    C += [(v,w) for v,w in FLEX if w in P]
    if (2,14) in cur[2]: C.append(((3,14),(3,13)))
    C += [(v,w) for v,w in PROTECTED if v in tips and w in P]
    assert all(w in Q for v,w in C)
    reduced,_,records=cancel_pairs(*d[:2],C,Counter())
    # Independent physical multigraph reconstruction, retaining parallel M/PP edges.
    edges=[('M',a,b) for a,b in cur[3]]
    edges += [('S',v,partner(v)) for v in P if v<partner(v) and partner(v) in P]
    edges += [('S',v,w) for v,w in C]
    adj=defaultdict(list)
    for i,(kind,a,b) in enumerate(edges):
        assert b in neighbors(a) and color(a)!=color(b)
        adj[a].append((b,kind,i));adj[b].append((a,kind,i))
    assert set(adj)==P
    for v in P:
        assert sum(k=='M' for w,k,i in adj[v])==1
        assert sum(k=='S' for w,k,i in adj[v])<=1
    physical_pairs=set();unseen=set(P)
    while unseen:
        start=min(unseen);seen={start};todo=[start];used=set()
        while todo:
            v=todo.pop()
            for w,kind,i in adj[v]:
                used.add(i)
                if w not in seen:seen.add(w);todo.append(w)
        unseen-=seen;ends=sorted(v for v in seen if len(adj[v])==1)
        if not ends: assert len(used)==len(seen);continue
        assert len(ends)==2 and len(used)+1==len(seen) and len(used)%2==1
        assert color(ends[0])!=color(ends[1])
        physical_pairs.add(tuple(ends));totals['physical_odd_paths']+=1
    assert physical_pairs=={tuple(sorted(e)) for e in reduced}
    mate={a:b for e in cur[3] for a,b in (e,e[::-1])}
    linked={v for e in C for v in e}
    relevant=set()
    for v in holes:
        u=mate[v]
        if v[0]==u[0] or partner(u) in F:
            assert d[0][u]=='BP' and u not in Q and not {v,u}&linked
            assert tuple(sorted((v,u))) in physical_pairs
            totals['untouched_mixed_holes']+=1
        else:
            assert u==transverse(v) and v in H
            relevant.add(v)
    assert not ((26,14) in tips and {(26,13),(26,15)}&tips)
    loss_pairs=[tuple(sorted(e)) for e in reduced if all(v in holes and d[0][v]=='TP' for v in e)]
    assert all(set(e)<=relevant for e in loss_pairs)
    assert len(loss_pairs)==result['exact_strategy_loss']<=min(sum(color(v)==0 for v in relevant),sum(color(v)==1 for v in relevant))<=1
    if loss_pairs:
        assert (17,9) in loss_pairs[0] and set(loss_pairs[0])&{(26,13),(26,15)}
        assert mate[(17,9)]==(18,9)
    degree3=all(len(set(neighbors(v))&(P|cur[2]))>=3 for v in P)
    if degree3 or result['frozen']:
        assert not loss_pairs and result['ordinary_deficit']==0
        totals['min_degree_three_models']+=degree3
    totals['active_unprotected_tips']+=len(holes)
    totals['models_with_unprotected_tips']+=bool(holes)
    totals['models_with_relevant_holes']+=bool(relevant)
    totals['loss_one_models']+=bool(loss_pairs)
    return dict(**result,relevant_holes=sorted(relevant),loss_pairs=loss_pairs,min_degree_three=degree3,
                full_pool_ordinary_deficit=ordinary_flow(*d)['deficit'])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    base,*_=load_model();S,F,Q,audit=geometry(base);totals=Counter();named={}
    check(base,base,S,F,Q,totals,True)
    _,cap=frozen_caps(base,1);named['frozen_caps']=check(base,cap,S,F,Q,totals,True)
    j=json.loads(Path('develop/fixtures/residual_fresh_degree_three_bottom.json').read_text())
    cur=(*base[:2],base[2]|set(map(tuple,j['new_selected'])),base[3]+[tuple(map(tuple,e)) for e in j['new_matching']])
    bottom=check(base,cur,S,F,Q,totals,True)
    assert bottom['min_degree_three'] and not bottom['frozen'] and bottom['unprotected_fresh']==2
    named['degree_three_nonfrozen_bottom']=bottom
    for sq,alt in square_switches(cur):
        check(base,alt,S,F,Q,totals);totals['degree_three_bottom_rematches']+=1
    j=json.loads(Path('develop/fixtures/residual_fresh_frozen_bottom.json').read_text())
    cur=(*base[:2],base[2]|set(map(tuple,j['new_selected'])),base[3]+[tuple(map(tuple,e)) for e in j['new_matching']])
    layers=[[w['endpoint'] for w in layer] for layer in frozen_certificate(base)[1]]
    layers += [[tuple(w['endpoint']) for w in layer] for layer in j['appended_rank_layers']]
    check_rank_certificate(cur,layers)
    bottom=check(base,cur,S,F,Q,totals,True)
    assert bottom['frozen'] and bottom['unprotected_fresh']==2 and bottom['ordinary_deficit']==0
    assert bottom['endpoints']==318 and bottom['selected']==52
    totals['frozen_bottom_independent_rank_checks']+=1
    named['frozen_unprotected_bottom']=bottom
    for sq,alt in square_switches(cur):
        check(base,alt,S,F,Q,totals);totals['frozen_bottom_rematches']+=1
    for v in sorted(S):
        cur=activate(base,v)
        if cur is None:totals['no_single_augmenting_completion']+=1;continue
        named[str(v)]=check(base,cur,S,F,Q,totals,True)
        for sq,alt in list(square_switches(cur))[:4]:
            check(base,alt,S,F,Q,totals);totals['actual_rematches']+=1
    # Force the transverse exceptional mates, avoiding a horizontal augment choice.
    for v in sorted(VERTICAL):
        u=transverse(v);trial=(*base[:2],base[2]|{partner(v)},base[3]+[(v,u)])
        if feasible(trial):
            named['transverse_'+str(v)]=check(base,trial,S,F,Q,totals,True)
            totals['forced_transverse_models']+=1
    rng=random.Random(2026102511)
    options=sorted(S|{v for v,w in PROTECTED})
    for run in range(24):
        cur=base;rng.shuffle(options)
        for v in options:
            trial=activate(cur,v)
            if trial is None:continue
            cur=trial;check(base,cur,S,F,Q,totals)
        named['simultaneous_'+str(run)]=check(base,cur,S,F,Q,totals)
        totals['simultaneous_runs']+=1
    j=json.loads(Path('develop/fixtures/residual_fresh_one_loss_nonfrozen.json').read_text())
    cur=(*j['shape'],set(map(tuple,j['selected'])),[tuple(map(tuple,e)) for e in j['matching']])
    witness=check(base,cur,S,F,Q,totals,True)
    assert witness['endpoints']==330 and witness['selected']==51 and not witness['frozen']
    assert witness['exact_strategy_loss']==witness['ordinary_deficit']==1
    assert witness['full_pool_ordinary_deficit']==0
    assert witness['loss_pairs']==[((17,9),(26,13))]
    named['sharp_restricted_pool_witness']=witness
    for sq,alt in square_switches(cur):
        check(base,alt,S,F,Q,totals);totals['sharp_witness_rematches']+=1
    report=dict(status='PASS',counts=dict(totals),geometry=audit,named=named,
        scope='Written every-feasible-extension theorem on this fixed 28x24 rectangle only: strategy loss <=1, loss zero if all final P have occupied degree >=3, hence every frozen extension fully compensated. 330P nonfrozen witness has restricted-pool true deficit1, full-pool0. Not universal grids, larger rectangles, copies, or numerical 5/6 improvement.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals),witness=witness)))

if __name__=='__main__':main()
