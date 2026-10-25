"""Full physical gap suppression and exact immutable-link retraction controls.

No resource reservations, solver or optional dependencies. General proofs:
docs/FROZEN_GAP_CAPACITY_AND_LINK_RETRACTION.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_colored_interval_slots import physical
from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_merger_completion_reserves import feasible, frozen
from check_partial_tip_compensation import live_prune
from check_whole_support_fork_normal_form import whole_support_data, ordinary_flow, contract, optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Run without -O; assertions are required.')


def family(capacities,w=30,padding=0,mirror=False):
    q=len(capacities);L=w-20
    assert q and all(0<=c<=L for c in capacities)
    old,move,layers=physical(q,w,padding,mirror)
    added={move((2 if j%2==0 else 3,j),0,i)
           for i,c in enumerate(capacities) for j in range(10,10+L-c)}
    cur=(*old[:2],old[2]|added,old[3])
    C=[(move((3,6),side,i),move((3,7),side,i)) for i in range(q) for side in (0,1)]
    beta=[(move((3,6),side,i),move((3,5),side,i)) for i in range(q) for side in (0,1)]
    return old,cur,move,layers,added,C,beta


def coordinate_units(data,meta):
    return {tuple(meta['intervals'][j][k] for k in ('band','first','last')) for j in data[4]}


def inspect(capacities,w,padding,mirror,totals,exhaust=False,primitive=False):
    q=len(capacities);L=w-20
    old,cur,move,layers,added,C,beta=family(capacities,w,padding,mirror)
    oldP={v for edge in old[3] for v in edge};oldO=oldP|old[2]
    assert all(not (set(neighbors(v))&(oldO|added)) for v in added)
    assert feasible(cur) and frozen(cur)
    check_rank_certificate(cur,layers)
    assert cur[3] == old[3] and old[2] <= cur[2]
    assert len(oldP)==40*q and len(cur[3])==20*q and len(cur[2])==q*(w+22)-sum(capacities)
    assert all(set(neighbors(v))&oldO == set(neighbors(v))&(cur[2]|oldP) for v in oldP)
    oldd,oldmeta,_=whole_support_data(old,whole_bands(old))
    data,meta,_=whole_support_data(cur,whole_bands(cur))
    assert data[:3]==oldd[:3], 'Endpoint types, original strands and link graph must be unchanged.'
    removed={(move((2,j),0,i)[0]//2,move((2,j),0,i)[1],move((2,j),0,i)[1])
             for i,c in enumerate(capacities) for j in range(10,10+L-c)}
    assert removed <= coordinate_units(oldd,oldmeta)
    assert coordinate_units(data,meta) == coordinate_units(oldd,oldmeta)-removed
    assert len(oldd[4])-len(data[4])==len(added)==sum(L-c for c in capacities)
    owner,aa,bb,mm=owner_data(*data[:2])
    assert (len(aa),len(bb))==(2*q,2*q)
    for i,c in enumerate(capacities):
        shared=None
        for side in (0,1):
            tip=move((3,8),side,i);a=owner[move((3,6),side,i)]
            assert a in aa and not data[3][a]
            support=data[3][owner[tip]]
            expected={meta['owner'][move((2,j),0,i)[0]//2,move((2,j),0,i)[1]]
                      for j in range(10+L-c,w-10)}
            assert support == expected and len(support)==c
            if shared is not None:assert support==shared
            shared=support
        # In the FULL original graph the outer A end has a dead mixed
        # branch, rather than no target. Its support is empty and its TP
        # only points back to its own BP. Do not silently discard it.
        for side in (0,1):
            bp,tp=(move(v,side,i) for v in ((6,7),(6,8)))
            dead=owner[tp]
            assert owner[bp]==dead and not data[3][dead]
            assert [e for e in data[2] if e[0]==tp]==[(tp,bp)]
            assert (move((6,6),side,i),bp) in data[2]
    for forks in (False,True):
        ans=fork_flow(*data) if forks else ordinary_flow(*data)
        assert (ans['value'],ans['cost'],ans['deficit'])==(2*q,2*q,0)
        totals['unconstrained_full_pool_flow_checks']+=1
    margin=cur[0]*cur[1]//2-len(cur[2])-len(cur[3])
    assert margin==(6*w+7*padding-42)*q+sum(capacities)>0
    assert len(data[4])==(6*w+7*padding-56)*q+sum(capacities)

    rng=random.Random(20261025038+q*13+sum(capacities))
    masks=set(range(1<<(2*q))) if exhaust else {0,(1<<(2*q))-1}
    if not exhaust:
        masks|={rng.randrange(1<<(2*q)) for _ in range(20)}
    D=sum(max(0,2-c) for c in capacities)
    # First D labelled old C links each fix a different missing payment.
    tokens=[2*i+side for i,c in enumerate(capacities) for side in range(max(0,2-c))]
    assert len(tokens)==len(set(tokens))==D
    frontier_masks={}
    for budget in range(2*q+2):
        releases=set(tokens[:min(budget,D)])
        mask=sum(1<<j for j in range(2*q) if j not in releases)
        masks.add(mask);frontier_masks[budget]=mask
    results={}
    for mask in sorted(masks):
        kept=[edge for j,edge in enumerate(C) if mask>>j&1]
        k=[sum(mask>>(2*i+s)&1 for s in (0,1)) for i in range(q)]
        r=2*q-len(kept)
        value=2*q-sum(max(0,k[i]-capacities[i]) for i in range(q))
        contracted=contract(data,kept)
        assert contracted[4] == data[4], 'No physical interval is reserved or deleted during contraction.'
        for forks in (False,True):
            ans=fork_flow(*contracted) if forks else ordinary_flow(*contracted)
            assert (ans['value'],ans['cost'])==(value,r),(capacities,mask,forks,ans,value,r)
            totals['contracted_ordinary_full_checks']+=1
            if primitive:
                direct=optimize(*contracted,allow_forks=forks)
                assert (direct['value'],direct['cost'])==(value,r)
                totals['independent_primitive_comparisons']+=1
        if mask==(1<<(2*q))-1:
            # Delete only branches proved off every productive route,
            # keeping all physical resources and endpoints in the board.
            pruned,_=live_prune(contracted)
            oo,afterA,_,_=owner_data(*pruned[:2])
            assert len(afterA)==2*q
            assert all(oo[v] not in afterA for v,t in pruned[2])
            assert value==sum(min(2,c) for c in capacities)
            totals['no_productive_exit_locked_alpha_checks']+=2*q
        results[mask]=(value,r)
    for budget,mask in frontier_masks.items():
        value,cost=results[mask]
        assert value==2*q-max(0,D-budget) and cost==min(budget,D)
        # Explicit simultaneous route repair: keep all other old C links;
        # use each released source's private beta, never a duplicated resource.
        released={j for j in range(2*q) if not (mask>>j&1)}
        replacement=[e for j,e in enumerate(C) if j not in released]+[e for j,e in enumerate(beta) if j in released]
        assert len(replacement)==2*q and len({v for e in replacement for v in e})==4*q
        final=contract(data,replacement)
        answer=ordinary_flow(*final)
        assert answer['cost']==0
        assert len(released)+answer['value']==value
        totals['frontier_witnesses']+=1
        if exhaust:
            # Complete search over every permitted earlier-link subset,
            # maximising value and then minimising additional link cost.
            options=[(v,c) for v,c in results.values() if c<=budget]
            best=min(options,key=lambda x:(-x[0],x[1]))
            assert best==(value,cost)
            totals['exhaustive_budget_optima']+=1
    totals['physical_boards']+=1
    totals['independent_strict_rank_certificates']+=1
    totals['isolated_new_selections_checked']+=len(added)
    totals['retained_link_subsets_checked']+=len(masks)
    totals['exhaustive_subset_boards']+=exhaust
    return dict(shape=cur[:2],capacities=list(capacities),endpoints=40*q,
        selected=len(cur[2]),added_selected=len(added),actual_edges=20*q,
        available_original_units=len(data[4]),initial_available_units=len(oldd[4]),
        full_payment=2*q,full_minimum_links=2*q,all_kept_value=2*q-D,
        minimum_retractions_for_full=D,margin=margin,kept_subsets_checked=len(masks),
        frontier=[dict(budget=b,payment=results[m][0],extra_links=results[m][1]) for b,m in frontier_masks.items()])


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    totals=Counter();named={}
    for w in (30,32,40):
        for c in range(w-19):
            for padding in (0,2):
                for mirror in (False,True):
                    r=inspect((c,),w,padding,mirror,totals,True,
                              w==30 and c in (0,1,2) and padding==0)
                    if w==30 and c in (0,1,2,10) and padding==0 and not mirror:named['single_capacity_'+str(c)]=r
    print(json.dumps(dict(stage='all_single_capacities',boards=totals['physical_boards'])),flush=True)
    for q in (2,3):
        for capacities in itertools.product((0,1,2),repeat=q):
            for mirror in (False,True):inspect(capacities,30,0,mirror,totals,True)
    print(json.dumps(dict(stage='all_small_profiles_and_subsets',boards=totals['physical_boards'])),flush=True)
    rng=random.Random(20261025039)
    for q in (4,6,8):
        profiles={(1,)*q,(0,)*q,(2,)*q,(10,)*q}
        profiles|={tuple(rng.randrange(11) for _ in range(q)) for _ in range(4)}
        for capacities in sorted(profiles):
            for mirror in (False,True):
                r=inspect(capacities,30,2,mirror,totals)
                if q==8 and capacities==(1,)*q and not mirror:named['eight_intrinsic_collisions']=r
    assert totals['independent_primitive_comparisons']==48
    report=dict(status='PASS',counts=dict(totals),named=named,
        scope='General written endpoint/M/degree/strand/link/freeze-preserving capacity suppression for all even w>=30, arbitrary q and capacity vector; exact immutable-link value/cost and minimal-retraction frontier. No artificial reservations. Finite controls do not prove universal grid compensation or improve 5/6.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals))),flush=True)


if __name__=='__main__':main()
