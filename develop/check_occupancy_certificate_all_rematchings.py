"""Fixed-occupancy physical certificate for EVERY actual perfect matching.

The universal proof is in OCCUPANCY_CERTIFICATE_AND_ALL_REMATCHINGS.md.
Finite matching exploration is validation, not a completeness claim.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_frozen_mixed_gate_cycle import load_model
from check_bt_corridor_ports import compile_model
from check_endpoint_free_gap_compensation import gap_access
from check_frozen_tip_slot_obstruction import matching
from check_merger_completion_reserves import feasible,frozen,owner_data,whole_bands,whole_support_data
from check_partial_tip_compensation import lift
from check_reserve_boundary_split import clipped
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import ordinary_flow,optimize

if not __debug__:raise RuntimeError('Run without -O.')
CERT=Path(__file__).parent/'fixtures/mixed_cycle_occupancy_certificate.json'
canon=lambda es:frozenset(tuple(sorted(e)) for e in es)


def switches(M):
    for r in range(27):
        for c in range(23):
            a,b,d,e=(r,c),(r,c+1),(r+1,c),(r+1,c+1)
            h=canon([(a,b),(d,e)]);v=canon([(a,d),(b,e)])
            if h<=M:yield (r,c),M-h|v
            elif v<=M:yield (r,c),M-v|h


def certificate(base):
    record=json.loads(CERT.read_text())
    data,meta=compile_model(base,whole_bands(base),Counter())
    kinds,pairs,links,access,resources=data
    assignments={}
    for row in record['assignments']:
        target=row['target'];v=tuple(row['source'])
        target=('bp',tuple(target[1])) if target[0]=='bp' else ('interval',target[1],0)
        assert target not in assignments
        assignments[target]=v
        assert kinds[v]=='TP'
        if target[0]=='bp':assert (v,target[1]) in links
        else:assert target[1] in access[v]&resources
    assert len(assignments)==23 and set(assignments.values())=={v for v in kinds if kinds[v]=='TP'}
    assert len(set(assignments.values()))==len(assignments)
    reserve={t[1] for t in assignments if t[0]=='interval'}
    assert len(reserve)==5 and len(assignments)-len(reserve)==18
    identities={(meta['intervals'][j]['band'],meta['intervals'][j]['first'],meta['intervals'][j]['last']) for j in reserve}
    assert identities=={(6,12,12),(7,10,10),(9,10,10),(12,7,7),(12,16,16)}
    # Five disjoint physical obstruction groups: ANY all-TP certificate
    # using physical endpoint-free-gap access needs >=5 different units,
    # even if two labelled slots of each unit are permitted.
    full=gap_access(base,whole_bands(base),Counter())[4]
    groups=[{(12,14)},{(14,11)},{(19,11)},
            {(24,2),(24,4),(24,6)},{(24,17),(24,19),(24,21)}]
    neighborhoods=[]
    for H in groups:
        BP={w for v,w in links if v in H}
        assert len(H)-len(BP)==1
        units=set().union(*(full[v] for v in H))
        assert units and units<=resources
        assert len(reserve&units)==1
        neighborhoods.append(units)
    assert all(not E&F for E,F in itertools.combinations(neighborhoods,2))
    assert sum(len(E) for E in groups)==9
    return assignments,reserve,data,meta,groups,neighborhoods


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    base,_,_,*_=load_model();assigned,reserve,static,meta,groups,units=certificate(base)
    old=canon(base[3]);seen={old};front={old};depth_counts=[]
    for depth in range(2):
        nxt={new for M in front for sq,new in switches(M)}-seen
        depth_counts.append(len(nxt));seen|=nxt;front=nxt
    assert depth_counts==[44,952]
    rng=random.Random(2026102551);M=old;random_new=0
    for _ in range(1800):
        possible=list(switches(M));_,M=rng.choice(possible)
        if M not in seen:random_new+=1;seen.add(M)
    totals=Counter();examples={};counts=Counter()
    for i,M in enumerate(sorted(seen,key=repr)):
        cur=(*base[:3],sorted(M));assert feasible(cur)
        data,info,_=whole_support_data(cur,whole_bands(cur));o,aa,bb,mm=owner_data(*data[:2])
        # The actual terminal pairs/owners may change. The physical data
        # used by the SAME certificate must remain identical.
        assert data[0]==static[0] and data[2]==static[2] and data[4]==static[4]
        for k in ('labels','intervals','boundary'):assert info[k]==meta[k]
        restricted=clipped(data,reserve)
        result=lift(restricted,assigned)
        assert result['holes']==result['certified_deficit']==result['final_component_budget']==0
        assert result['certified_payment']==len(aa) and result['selected_links']==18
        ordinary=ordinary_flow(*restricted);full=fork_flow(*restricted)
        assert ordinary['value']==full['value']==len(aa)
        assert ordinary['cost']<=18 and full['cost']<=ordinary['cost']
        if i<80:
            for forks in (False,True):
                exact=optimize(*restricted,allow_forks=forks)
                target=full if forks else ordinary
                assert (exact['value'],exact['cost'])==(target['value'],target['cost'])
                totals['independent_ordinary_full_packs']+=1
        is_frozen=frozen(cur)
        totals['completely_frozen_matching_models' if is_frozen else 'feasible_nonfrozen_matching_models']+=1
        totals['same_certificate_lifts']+=1
        totals['restricted_five_unit_flow_models']+=1
        counts[str((len(aa),len(bb),len(mm)))]+=1
        if str(len(aa)) not in examples:
            examples[str(len(aa))]=dict(alpha=len(aa),beta=len(bb),mixed=len(mm),frozen=is_frozen,ordinary_value=ordinary['value'],ordinary_cost=ordinary['cost'])
        assert len(bb)-len(aa)==2
    result=dict(status='PASS',shape=base[:2],selected=49,endpoints=308,tp=23,bp=27,
        certificate_links=18,certificate_original_units=5,
        unit_coordinates=[(6,12),(7,10),(9,10),(12,7),(12,16)],
        five_disjoint_tip_groups=[sorted(g) for g in groups],physical_group_unit_counts=list(map(len,units)),
        depth1_depth2_discovery_counts=depth_counts,random_walk_new_models=random_new,
        totals=dict(totals),owner_count_profiles=dict(counts),examples=examples,
        scope='Universal written proof: EVERY actual perfect matching on the FIXED308P/49T occupation, frozen or not, admits complete ORDINARY compensation using ONLY five declared original interval units plus original beta resources, at most18actual links. Same23TP physical certificate; interval identities counted once.5units optimal for all-TP physical-cover certificates even2slots, NOT asserted minimal universal payment reserve. Arbitrary new occupied sites/5over6 OPEN.')
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))

if __name__=='__main__':main()
