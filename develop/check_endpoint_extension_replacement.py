"""Arbitrary endpoint additions/rematching with a fixed saturated selected set.

The general proof is in ENDPOINT_EXTENSIONS_AND_LOCAL_RESOURCE_REPLACEMENT.md.
Finite exploration checks the actual geometry and simultaneous certificates.
"""
import argparse
from collections import Counter,deque
import itertools
import json
from pathlib import Path
import random

from check_frozen_mixed_gate_cycle import load_model
from check_occupancy_certificate_all_rematchings import certificate,switches,canon
from check_cooperative_promotion import neighbors
from check_merger_completion_reserves import feasible,frozen,owner_data,whole_bands,whole_support_data
from check_promotion_cores import frozen_certificate
from check_partial_tip_compensation import lift
from check_reserve_boundary_split import clipped
from check_terminal_cancellation_and_stranded_demand import cancel_pairs
from check_whole_support_fork_normal_form import ordinary_flow,optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Run without -O.')
FLEX=[((12,14),(12,15)),((14,11),(14,10)),((19,11),(19,10)),((24,6),(24,7)),((24,17),(24,16))]


def static_certificate(base):
    old,_,d,meta,_,_=certificate(base)
    old={t:v for t,v in old.items() if t[0]=='bp'}
    P={v for e in base[3] for v in e};occupied=P|base[2]
    assert len(old)==18
    assert all(len(set(neighbors(t))&occupied)==1 for t in base[2])
    sat=[dict(selected=t,occupied=next(iter(set(neighbors(t))&occupied))) for t in sorted(base[2])]
    for v,u in FLEX:
        t=(v[0]^1,v[1]);q=(u[0]^1,u[1])
        assert t in base[2] and v in P and u not in occupied and q not in occupied
        assert u in neighbors(v) and q in neighbors(t)
        assert (u[0]//2,u[1])==next((meta['intervals'][j]['band'],meta['intervals'][j]['first'])
            for j in d[4] if meta['intervals'][j]['band']==u[0]//2 and meta['intervals'][j]['first']==u[1])
    assert len({u for v,u in FLEX})==5
    assert {v for v,u in FLEX}|set(old.values())=={v for v,k in d[0].items() if k=='TP'}
    return old,sat


def augment(cur,start):
    """A new endpoint may require rematching old edges; no old-M retention."""
    T=cur[2];mate={v:w for e in cur[3] for v,w in (e,e[::-1])};P=set(mate)
    assert start not in P|T and not set(neighbors(start))&T
    todo=deque([(start,[],[],{start})]);seen={start}
    while todo:
        v,add,remove,used=todo.popleft()
        for w in sorted(neighbors(v)):
            if not (0<=w[0]<cur[0] and 0<w[1]<cur[1]) or w in used or w in T:continue
            if w not in P:
                if set(neighbors(w))&T:continue
                drop={tuple(sorted(e)) for e in remove}
                es=[e for e in cur[3] if tuple(sorted(e)) not in drop]+add+[(v,w)]
                ans=(*cur[:3],es)
                if feasible(ans):return ans
            else:
                z=mate[w]
                if z in used or z in seen:continue
                seen.add(z);todo.append((z,add+[(v,w)],remove+[(w,z)],used|{w,z}))
    raise RuntimeError(('no feasible augmenting path',start))


def inspect(base,cur,old,totals,independent=False):
    assert cur[2]==base[2] and feasible(cur)
    P={v for e in cur[3] for v in e};oldP={v for e in base[3] for v in e}
    assert oldP<=P
    d,meta,_=whole_support_data(cur,whole_bands(cur));o,aa,bb,mm=owner_data(*d[:2])
    old_tips={v for v,k in whole_support_data(base,whole_bands(base))[0][0].items() if k=='TP'}
    assert {v for v,k in d[0].items() if k=='TP'}==old_tips
    assigned=dict(old);pool=set();h=0
    for v,u in FLEX:
        q=(u[0]^1,u[1]);assert q not in cur[2]|P
        if u in P:
            assigned['bp',u]=v;h+=1
            assert d[0][u]=='BP' and (v,u) in d[2]
        else:
            j=meta['owner'][u[0]//2,u[1]]
            assert meta['intervals'][j]==dict(band=u[0]//2,first=u[1],last=u[1])
            assert j in d[4]
            assigned['interval',j,0]=v;pool.add(j)
    assert len(assigned)==23 and len(pool)==5-h
    restricted=clipped(d,pool)
    lifted=lift(restricted,assigned)
    assert lifted['holes']==lifted['certified_deficit']==0
    assert lifted['certified_payment']==len(aa) and lifted['selected_links']==18+h
    links=[(v,t[1]) for t,v in assigned.items() if t[0]=='bp']
    reduced,inventory,_=cancel_pairs(d[0],d[1],links,Counter())
    aC=inventory['TP','TP'];bC=inventory['BP','BP']
    assert 2*aC<=5-h and len(aa)+bC==len(bb)+aC
    ordinary=ordinary_flow(*restricted);full=fork_flow(*restricted);beta=ordinary_flow(*clipped(d,set()))
    assert ordinary['value']==full['value']==len(aa)
    assert ordinary['cost']<=18+h and full['cost']<=ordinary['cost']
    assert beta['value']>=len(aa)-(5-h)//2
    if h>=4:assert beta['value']==len(aa)
    if independent:
        for allow in (False,True):
            brute=optimize(*restricted,allow_forks=allow);expected=full if allow else ordinary
            assert (brute['value'],brute['cost'])==(expected['value'],expected['cost'])
            totals['independent_ordinary_full_packs']+=1
    is_frozen=frozen(cur)
    totals['frozen_models' if is_frozen else 'feasible_nonfrozen_models']+=1
    totals['models']+=1;totals['filled_target_'+str(h)]+=1
    return dict(endpoints=len(P),alpha=len(aa),beta=len(bb),filled_targets=h,surviving_packet_units=5-h,
                certificate_links=18+h,final_alpha=aC,ordinary_cost=ordinary['cost'],beta_only_value=beta['value'],frozen=is_frozen)


def save_control_fixture(cur,path):
    f,layers=frozen_certificate(cur)
    is_frozen=len(f)==2*len(cur[3])
    record=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],
        completely_frozen=is_frozen,freezing_layers=[[r['endpoint'] for r in layer] for layer in layers])
    if is_frozen:
        from check_frozen_shared_mixed_gate import check_rank_certificate
        check_rank_certificate(cur,[[tuple(v) for v in layer] for layer in record['freezing_layers']])
    Path(path).write_text(json.dumps(record,indent=2)+'\n')


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    base,*_=load_model();old,sat=static_certificate(base);totals=Counter();named={};rng=random.Random(2026102561)
    snapshot=dict(selected_saturation=sat,bp_assignments=[dict(source=v,target=t[1]) for t,v in old.items()],
        flexible_assignments=[dict(source=v,candidate=u,guard=(v[0]^1,v[1]),protected_blank=(u[0]^1,u[1]),unit=(u[0]//2,u[1])) for v,u in FLEX])
    Path('develop/fixtures/saturated_endpoint_extension_certificate.json').write_text(json.dumps(snapshot,indent=2)+'\n')
    # All32 filled-subset requests; an augmenting path may also fill another
    # target. The actual h is recomputed rather than assumed from the request.
    for bits in itertools.product((False,True),repeat=5):
        cur=base
        for (v,u),flag in zip(FLEX,bits):
            P={p for e in cur[3] for p in e}
            if flag and u not in P:cur=augment(cur,u)
        info=inspect(base,cur,old,totals,independent=True)
        named['requested_'+''.join(str(int(b)) for b in bits)]=info
        if all(bits):
            save_control_fixture(cur,'develop/fixtures/endpoint_extension_all_five.json')
        if bits==(True,False,False,False,False):
            assert info['frozen'] and info['filled_targets']==1
            save_control_fixture(cur,'develop/fixtures/endpoint_extension_one_target_frozen.json')
        # Arbitrary old/new square rematching is independent of feasibility;
        # it can change freezing, so labels are checked for every final state.
        M=canon(cur[3])
        for step in range(6):
            choices=list(switches(M));_,M=rng.choice(choices)
            inspect(base,(*cur[:3],sorted(M)),old,totals,independent=step==0)
            totals['rematched_extension_models']+=1
    # Every feasible single new matching edge retaining the original M.
    oldP={v for e in base[3] for v in e}
    blanks={(r,c) for r in range(28) for c in range(1,24)}-oldP-base[2]
    for u in sorted(blanks):
        for v in sorted(set(neighbors(u))&blanks):
            if u>=v:continue
            cur=(*base[:3],base[3]+[(u,v)])
            if not feasible(cur):continue
            inspect(base,cur,old,totals)
            totals['single_new_edge_models']+=1
    # Larger rectangles, arbitrary extra disconnected matched pairs, plus
    # simultaneous rematching of the original geometry. New P may be outside.
    for run in range(20):
        cur=base;M=canon(base[3])
        for _ in range(10):_,M=rng.choice(list(switches(M)))
        cur=(34,30,base[2],list(M)+[((30,2+2*i),(30,3+2*i)) for i in range(run%8+1)])
        inspect(base,cur,old,totals,independent=run<4)
        totals['larger_rectangle_models']+=1
    result=dict(status='PASS',old_selected=49,old_endpoints=308,old_tp=23,old_bp_certificate=18,
        immediate_packet_units=[(6,15),(7,10),(9,10),(12,7),(12,16)],totals=dict(totals),named=named,
        scope='ALL finite feasible extensions with EXACT same49selectedT, containing old308P, arbitrary grid perfect matching of finalP and larger same-phase rectangle. No retained oldM, no freezing assumption. Same23TP; adaptive18+hBP and5-hdistinct final original intervals cover ALLTP. Full ORDINARY compensation;costLE18+h;atMostFloor((5-h)/2)intervalPayments;hge4_betaOnlyComplete. Additional selections/other occupations/universal5over6 OPEN. All-five fixture explicitly NONFROZEN if labelled so.')
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals),all_five=named['requested_11111'])))

if __name__=='__main__':main()
