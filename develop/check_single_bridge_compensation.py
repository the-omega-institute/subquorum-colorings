"""Exact one-link cross-component repair by two resource-graph modes.

General proof: docs/SINGLE_BRIDGE_COMPENSATION.md. Production uses only the
old-link allocation kernel; full flow and primitive enumeration are audits.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_old_link_batch_repair import repair, signature
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import canonical, primitive_certificates, optimize
from check_whole_support_fork_flow import fork_flow
from check_destructive_exchange_choice import constrained_optimum
from check_protected_linear_corridors import subsets
from check_frozen_mixed_gate_cycle import load_model, FIXTURE
from check_P_free_pivot_interface import regions
from check_degree_changing_bent_completions import compile_model
from check_canonical_band_coarsening import forests
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_uniform_zero_capacity_openings import tile_cells

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def ordered_stem(data,p):
    own,A,B,M=owner_data(*data[:2]);assert p['kind']=='interval'
    sources=set(p['owners'])&A;assert len(sources)==1 and not set(p['owners'])&B
    outgoing={own[u]:(u,v) for u,v in p['links']}
    assert len(outgoing)==len(p['links'])
    owners=[next(iter(sources))];links=[]
    while owners[-1] in outgoing:
        e=outgoing[owners[-1]];links.append(e);owners.append(own[e[1]])
        assert len(owners)==len(set(owners))
    assert set(owners)==set(p['owners']) and len(links)==len(p['links'])
    return owners,links


def switched_skeleton(data,pack,bridge):
    """Two disjoint alpha stems; receiver's BP belongs to a mixed owner."""
    own,A,B,M=owner_data(*data[:2]);u,v=bridge
    assert bridge in data[2] and data[0][u]=='TP' and data[0][v]=='BP'
    ps=pack['certificates'];used=[o for p in ps for o in p['owners']]
    assert len(used)==len(set(used))
    at={o:i for i,p in enumerate(ps) for o in p['owners']}
    ia,ib=at[own[u]],at[own[v]];assert ia!=ib and own[v] in M
    oldlinks={e for p in ps for e in p['links']};assert bridge not in oldlinks
    ao,ae=ordered_stem(data,ps[ia]);bo,be=ordered_stem(data,ps[ib])
    a=ao.index(own[u]);b=bo.index(own[v]);assert b>=1
    def stem(os,es):
        return dict(kind='interval',owners=tuple(sorted(os)),links=tuple(es),
                    interval=None,value=1,witness=os[-1])
    replacement={ia:stem(ao[:a+1]+bo[b:],ae[:a]+[bridge]+be[b:]),
                 ib:stem(bo[:b],be[:b-1])}
    switched=dict(certificates=[replacement.get(i,p) for i,p in enumerate(ps)])
    used2=[o for p in switched['certificates'] for o in p['owners']]
    assert len(used2)==len(set(used2)) and set(used2)<=set(used)
    assert set(used2)&A==set(used)&A
    assert {e for p in switched['certificates'] for e in p['links']}<=oldlinks|{bridge}
    return switched


def single_bridge(data,pack,bridge,required=frozenset(),new_sources=frozenset()):
    switched=switched_skeleton(data,pack,bridge)
    modes=[repair(data,p,required,new_sources) for p in (pack,switched)]
    feasible=[(i,m) for i,m in enumerate(modes) if m['feasible']]
    if not feasible:return dict(feasible=False,modes=modes)
    i,best=max(feasible,key=lambda im:im[1]['value'])
    answer=dict(best,mode=i,modes=modes)
    if all(m['feasible'] for m in modes):
        assert modes[1]['value']<=modes[0]['value']+1
    return answer


def bridge_batch(data,pack,bridges,fees=None,required=frozenset(),new_sources=frozenset()):
    """Pairwise disjoint pairs of old interval stems; resources stay global.

    Exact maximum payment then minimum fee of actual added bridges. Old link
    count is not minimized. Only structural bridge modes are enumerated.
    """
    own,_,_,_=owner_data(*data[:2]);ps=pack['certificates']
    at={o:i for i,p in enumerate(ps) for o in p['owners']};used=set()
    for e in bridges:
        pair={at[own[e[0]]],at[own[e[1]]]}
        assert len(pair)==2 and not pair&used
        used|=pair;switched_skeleton(data,pack,e)
    fees=dict.fromkeys(range(len(bridges)),1) if fees is None else fees
    assert set(fees)==set(range(len(bridges))) and all(isinstance(w,int) and w>=0 for w in fees.values())
    best=None;proofs=[]
    for choices in itertools.product((False,True),repeat=len(bridges)):
        mode=pack;selected={i for i,on in enumerate(choices) if on}
        for i in sorted(selected):mode=switched_skeleton(data,mode,bridges[i])
        result=repair(data,mode,required,new_sources)
        proofs.append(dict(selected=sorted(selected),feasible=result['feasible'],
            deficiency=result['ledger']['deficiency'],obstructions=result['ledger']['infeasible']))
        if not result['feasible']:continue
        branch_fee=sum(fees[i] for i in selected)
        candidate=dict(result,selected_modes=sorted(selected),branch_fee=branch_fee)
        if best is None or (result['value'],-branch_fee)>(best['value'],-best['branch_fee']):best=candidate
    if best is None:return dict(feasible=False,modes=proofs)
    actual={i for i,e in enumerate(bridges) if e in best['links']}
    assert actual<=set(best['selected_modes'])
    fee=sum(fees[i] for i in actual)
    # If a positively charged selected mode were unused, its smaller mode
    # would represent this same packing and contradict the branch optimum.
    assert fee==best['branch_fee']
    return dict(best,actual_bridges=sorted(actual),bridge_fee=fee,modes=proofs)


def restricted(data,pack,bridge,new_sources=frozenset()):
    _,A,_,_=owner_data(*data[:2])
    owners=set().union(set(new_sources),*(set(p['owners']) for p in pack['certificates']))
    links={e for p in pack['certificates'] for e in p['links']}|{bridge}
    return (*data[:2],sorted(links),{o:S if o in owners else set() for o,S in data[3].items()},data[4])


def audit(data,pack,bridge,counts,new_sources=frozenset()):
    answer=single_bridge(data,pack,bridge,new_sources=new_sources);assert answer['feasible']
    d=restricted(data,pack,bridge,new_sources);independent=optimize(*d);flow=fork_flow(*d)
    assert answer['value']==independent['value']==flow['value']
    candidates={signature(p) for p in primitive_certificates(*d)}
    assert all(signature(p) in candidates for p in answer['certificates'])
    old=repair(data,pack,new_sources=new_sources);assert old['feasible']
    assert old['value']<=answer['value']<=old['value']+1
    counts['independent_bridge_optima']+=1
    counts['strict_bridge_gains']+=answer['value']>old['value']
    _,A,_,_=owner_data(*data[:2]);eligible=(set().union(*(set(p['owners']) for p in pack['certificates']))&A)|new_sources
    for R in subsets(sorted(eligible)):
        found=single_bridge(data,pack,bridge,R,new_sources)
        expected=constrained_optimum(d,R)
        assert found['feasible']==(expected is not None)
        if found['feasible']:
            assert found['value']==expected[0]
            assert R<=set(found['paid'])
            assert all(signature(p) in candidates for p in found['certificates'])
        else:
            assert all(m['ledger']['infeasible'] for m in found['modes'])
            counts['joint_two_mode_obstructions']+=1
        counts['source_prescription_checks']+=1
    return answer


def stem(owners,links,unit=None,witness=None):
    return dict(kind='interval',owners=tuple(owners),links=tuple(links),interval=unit,
                value=1,witness=owners[-1] if witness is None else witness)


def controls(counts):
    kinds,pairs,_=canonical('AAMM')
    bridge=(0,6);links=[(0,4),(2,6),bridge]
    pack=dict(certificates=[stem((0,2),[(0,4)],0),stem((1,3),[(2,6)],1)])
    records=[]
    for split in (False,True):
        W={0:set(),1:{0} if split else set(),2:set(),3:{1} if split else {0,1}}
        data=(kinds,pairs,links,W,{0,1});answer=audit(data,pack,bridge,counts)
        assert answer['value']==(2 if split else 1)
        deficits=[m['ledger']['deficiency'] for m in answer['modes']]
        assert deficits==([1,0] if split else [1,1])
        records.append(dict(name='separated-prefix-suffix' if split else 'surplus-behind-used-entry',
            old_component_deficits=1,receiver_units=2,receiver_unused_units=1,
            mode_deficits=deficits,value=answer['value'],selected_mode=answer['mode'],
            abstract=True,physical_realization_claim=False))
    with patch(__name__+'.optimize',side_effect=AssertionError('No primitive optimizer')), \
         patch(__name__+'.fork_flow',side_effect=AssertionError('No full flow')), \
         patch(__name__+'.constrained_optimum',side_effect=AssertionError('No primitive DP')):
        assert single_bridge(data,pack,bridge)['value']==2
    counts['production_no_flow_or_primitive_enumeration_controls']+=1
    # Each bridge repairs alone, but both need the SAME one-unit reserve.
    kinds,pairs,_=canonical('AAAAMM');bridges=[(0,8),(2,10)]
    pack=dict(certificates=[stem((0,),[]),stem((1,),[]),
        stem((2,4),[(4,8)]),stem((3,5),[(6,10)])])
    data=(kinds,pairs,[(4,8),(6,10)]+bridges,
          {0:set(),1:set(),2:{0},3:{1},4:{2},5:{2}},{0,1,2})
    assert repair(data,pack)['value']==2
    assert all(single_bridge(data,pack,e)['value']==3 for e in bridges)
    result=bridge_batch(data,pack,bridges,{0:5,1:2})
    assert (result['value'],result['bridge_fee'],result['actual_bridges'])==(3,2,[1])
    protected=bridge_batch(data,pack,bridges,{0:5,1:2},required={0})
    assert (protected['value'],protected['bridge_fee'],protected['actual_bridges'])==(3,5,[0])
    assert not bridge_batch(data,pack,bridges,required={0,1})['feasible']
    with patch(__name__+'.optimize',side_effect=AssertionError('No primitive optimizer')), \
         patch(__name__+'.fork_flow',side_effect=AssertionError('No full flow')), \
         patch(__name__+'.constrained_optimum',side_effect=AssertionError('No primitive DP')):
        assert bridge_batch(data,pack,bridges,{0:5,1:2})['bridge_fee']==2
    counts['production_no_flow_or_primitive_enumeration_controls']+=1
    records.append(dict(name='two-bridges-one-original-reserve',old_payment=2,
        each_bridge_alone=3,joint_payment=3,wrong_sum=4,cheapest_actual_bridge=1,fee=2,
        abstract=True,physical_realization_claim=False))
    counts['joint_original_reserve_nonreuse_controls']+=1
    return records


def batch_audits(counts,rng):
    kinds,pairs,_=canonical('AAAAMMMM')
    links=[(0,8),(2,10),(4,12),(6,14)];bridges=[(0,12),(2,14)]
    pack=dict(certificates=[stem((i,i+4),[links[i]]) for i in range(4)])
    for rep in range(36):
        Q=set(range(rng.randrange(1,8)));W={o:set() for o in range(8)}
        for j in Q:
            for o in rng.sample(range(8),rng.randrange(3)):W[o].add(j)
        data=kinds,pairs,links+bridges,W,Q
        fees={0:rep%4,1:(rep*3+2)%5}
        for R in subsets(range(4)):
            candidates=[]
            for F in subsets(range(2)):
                d=(*data[:2],links+[bridges[i] for i in F],W,Q)
                pair=constrained_optimum(d,R)
                if pair is not None:candidates.append((pair[0],sum(fees[i] for i in F)))
            answer=bridge_batch(data,pack,bridges,fees,R)
            assert answer['feasible']==bool(candidates)
            if candidates:
                expected=max(candidates,key=lambda t:(t[0],-t[1]))
                assert (answer['value'],answer['bridge_fee'])==expected
                assert R<=set(answer['paid'])
                actual={bridges[i] for i in answer['actual_bridges']}
                assert {e for e in answer['links'] if e not in links}==actual
                possible={signature(p) for p in primitive_certificates(*data)}
                assert all(signature(p) in possible for p in answer['certificates'])
            else:assert all(not m['feasible'] and m['obstructions'] for m in answer['modes'])
            counts['batch_fee_and_prescription_optima']+=1
        counts['two_bridge_batch_models']+=1


def physical(counts):
    fixture=json.loads((Path(__file__).parent/'fixtures/frozen_single_bridge_compensation.json').read_text())
    base=load_model()[0];R,C,T,M=base
    basebits={(r,c):False for r in range(0,R,2) for c in range(0,C,2)}
    oldbase,_,_=compile_model(base,regions(base,basebits));basefs=forests(base,regions(base,basebits))
    raw=json.loads(FIXTURE.read_text());layers=[[tuple(v) for v in layer] for layer in raw['freezing_layers']]
    records=[]
    for copies in (1,2,4):
        shift=lambda v,k:(v[0]+(R+2)*k,v[1])
        cur=((R+2)*copies-2,C,{shift(v,k) for k in range(copies) for v in T},
             [tuple(shift(v,k) for v in e) for k in range(copies) for e in M])
        bits={(r,c):False for r in range(0,cur[0],2) for c in range(0,C,2)}
        direct_check(*cur);rr=[[shift(v,k) for k in range(copies) for v in layer] for layer in layers]
        assert len(check_rank_certificate(cur,rr))==308*copies
        assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
        counts['strict_freezing_events']+=308*copies
        old,_,_=compile_model(cur,regions(cur,bits));own,A,B,X=owner_data(*old[:2])
        oldfs=forests(cur,regions(cur,bits));bycells={cc:j for j,(cap,cc) in oldfs.items() if cap}
        for k in range(copies):
            g=shift((24,22),k);assert not tile_cells(g)&{v for e in cur[3] for v in e}
            assert 2-len(tile_cells(g)&cur[2])==1
            bits[g]=True
        data,closed,_=compile_model(cur,regions(cur,bits));assert data[:2]==old[:2]
        assert len(cur[2])==49*copies and len(cur[3])==154*copies
        assert (len(A),len(B),len(X))==(4*copies,6*copies,15*copies)
        assert len(data[4])==155*copies-24
        assert cur[0]*cur[1]//2-len(cur[2])-len(cur[3])==157*copies-24
        assert fork_flow(*data)['value']==4*copies
        if copies==1:
            finalfs=forests(cur,regions(cur,bits));byfinal={cc:j for j,(cap,cc) in finalfs.items() if cap}
            unit=lambda r,c:byfinal[frozenset({(r,c),(r+1,c)})]
            beta=own[5,20];a=own[5,19];u=own[5,17];x=own[5,18];d=own[24,17];left=own[5,4]
            explicit=[dict(kind='beta',owners=tuple(sorted((a,beta))),links=(((5,19),(5,20)),),
                interval=None,value=1,beta=beta),
                stem(tuple(sorted((u,x))),[((5,17),(5,18))],unit(10,10),witness=x),
                stem((d,),[],unit(24,7)),stem((left,),[],unit(14,5))]
            possible={signature(p) for p in primitive_certificates(*data)}
            assert all(signature(p) in possible for p in explicit)
            oo=[o for p in explicit for o in p['owners']];jj=[p['interval'] for p in explicit if p['interval'] is not None]
            assert len(oo)==len(set(oo)) and len(jj)==len(set(jj))
        for row in fixture['cases']:
            ps=[];bridges=[]
            for k in range(copies):
                owner_map={o:own[shift(oldbase[1][o][0],k)] for o in range(len(oldbase[1]))}
                for p in fixture['common_pack']['certificates']:
                    unit=bycells[frozenset(shift(v,k) for v in basefs[tuple(p['interval'])][1])]
                    ps.append(dict(p,owners=tuple(sorted(owner_map[o] for o in p['owners'])),
                        links=tuple(tuple(shift(tuple(v),k) for v in e) for e in p['links']),
                        interval=unit,witness=owner_map[p['witness']]))
                bridges.append(tuple(shift(tuple(v),k) for v in row['bridge']))
            pack=dict(certificates=ps);allpaid=set().union(*(set(p['owners'])&A for p in ps))
            initial={signature(p) for p in primitive_certificates(*old)}
            assert all(signature(p) in initial for p in ps)
            assert len({p['interval'] for p in ps})==len(ps)==3*copies
            oldrepair=repair(data,pack);assert oldrepair['value']==2*copies and oldrepair['ledger']['deficiency']==copies
            answer=bridge_batch(data,pack,bridges)
            gain=row['kind']=='gain';expected=3*copies if gain else 2*copies
            assert answer['value']==expected and answer['bridge_fee']==(copies if gain else 0)
            prescribed=bridge_batch(data,pack,bridges,required=allpaid)
            assert prescribed['feasible']==gain
            restricted_links={e for p in ps for e in p['links']}|set(bridges)
            kept=set().union(*(set(p['owners']) for p in ps))
            limited=(*data[:2],sorted(restricted_links),{o:S if o in kept else set() for o,S in data[3].items()},data[4])
            f=fork_flow(*limited);assert f['value']==expected
            if copies==1:
                audit(data,pack,bridges[0],counts)
                head=own[bridges[0][1]]
                assert len(data[3][head])==(4 if gain else 5)
                donor=own[bridges[0][0]]
                assert not data[3][donor]
                if not gain:
                    receiver=next(p for p in ps if head in p['owners'])
                    before,edges=ordered_stem(data,receiver)
                    assert len(before)==2 and not data[3][before[0]]
                counts['physical_single_bridge_base_checks']+=1
            counts['physical_bridge_batch_checks']+=1
            records.append(dict(kind=row['kind'],copies=copies,shape=list(cur[:2]),
                old_source_count=3*copies,old_link_payment=2*copies,with_named_bridges=expected,
                minimum_actual_bridges=answer['bridge_fee'],all_old_sources_retained=gain,
                unrestricted_full_board_payment=4*copies,all_original_units_retained=True))
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True)
    args=p.parse_args();counts=Counter();rng=random.Random(2026102667)
    records=controls(counts)
    for index in range(180):
        # Two chains of arbitrary tested lengths, plus a beta/fork baseline
        # and an eligible new direct source. Full theorem has no length bound.
        na=rng.randrange(1,5);nb=rng.randrange(1,5)
        types='AA'+'M'*(na+nb)+'AAB'+'A'
        kinds,pairs,_=canonical(types);oa=[0]+list(range(2,2+na));ob=[1]+list(range(2+na,2+na+nb))
        edge=lambda x,y:(2*x+(1 if types[x]=='M' else 0),2*y)
        ea=[edge(x,y) for x,y in zip(oa,oa[1:])];eb=[edge(x,y) for x,y in zip(ob,ob[1:])]
        ai=rng.randrange(len(oa));bi=rng.randrange(1,len(ob));bridge=edge(oa[ai],ob[bi])
        a,b,z=2+na+nb,3+na+nb,4+na+nb
        forklinks=[(2*a,2*z),(2*b,2*z+1)]
        ps=[stem(oa,ea),stem(ob,eb)]
        if index%2:
            ps.append(dict(kind='fork',owners=(a,b,z),links=tuple(forklinks),interval=None,
                           value=2,beta=z,witness=z))
        else:ps.append(dict(kind='beta',owners=(a,z),links=(forklinks[0],),interval=None,value=1,beta=z))
        links=ea+eb+forklinks+[bridge];Q=set(range(rng.randrange(1,9)));W={o:set() for o in range(len(pairs))}
        for j in Q:
            for o in rng.sample(list(W),rng.randrange(3)):W[o].add(j)
        data=kinds,pairs,links,W,Q;pack=dict(certificates=ps)
        audit(data,pack,bridge,counts,new_sources={len(pairs)-1})
        counts['arbitrary_length_chain_models']+=1
    batch_audits(counts,rng);physical_records=physical(counts)
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(counts),controls=records,physical=physical_records,
        proof='docs/SINGLE_BRIDGE_COMPENSATION.md',
        scope='Pairwise disjoint pairs of old ordinary stems, one named actual added bridge per pair into a mixed owner. Exact max payment then minimum actual added-bridge fees, with source prescriptions, by 2^k resource-graph modes. Other old beta/fork primitives retained. Frozen capacity-one pivot separates failed and successful actual bridges.',
        limitations=['Not unrestricted new-link compensation or minimum total old/new link count.','Frozen obstruction is to named-link surplus rule; full original board pays all four sources per copy.','No universal 5/6 improvement.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts),controls=records,physical=physical_records),indent=2))


if __name__=='__main__':main()
