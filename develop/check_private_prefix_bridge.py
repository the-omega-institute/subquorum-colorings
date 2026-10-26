"""Polynomial private prefix/suffix bridge repair with old identity retention.

Proof: docs/PRIVATE_PREFIX_BRIDGE_COMPENSATION.md. Production uses request
graphs, not structural mode enumeration or full routing optimization.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_single_bridge_compensation import ordered_stem, switched_skeleton, bridge_batch, stem
from check_old_link_batch_repair import allocation, signature
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import canonical, primitive_certificates, optimize
from check_whole_support_fork_flow import fork_flow
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


def frame_with_direct_sources(data,pack,new_sources):
    _,A,_,_=owner_data(*data[:2]);paid=set().union(set(),*(set(p['owners']) for p in pack['certificates']))&A
    assert new_sources<=A-paid
    return dict(certificates=list(pack['certificates'])+[stem((a,),[]) for a in sorted(new_sources)])


def request_data(data,frame):
    W=data[3];neighbours={i:set().union(set(),*(W[o] for o in p['owners']))
        for i,p in enumerate(frame['certificates']) if p['kind']!='beta'}
    users=defaultdict(set)
    for i,S in neighbours.items():
        for j in S:users[j].add(i)
    assert all(len(ds)<=2 for ds in users.values())
    return neighbours,users


def recognize_private(data,frame,bridges,witnesses=None):
    own,_,_,_=owner_data(*data[:2]);ps=frame['certificates']
    at={o:i for i,p in enumerate(ps) for o in p['owners']}
    assert len(at)==sum(len(p['owners']) for p in ps)
    neighbours,users=request_data(data,frame);ledger=allocation(neighbours)
    components={d:i for i,c in enumerate(ledger['components']) for d in c['demands']}
    used=set();records=[]
    for k,e in enumerate(bridges):
        switched_skeleton(data,frame,e)
        ia,ib=at[own[e[0]]],at[own[e[1]]]
        assert not {ia,ib}&used;used|={ia,ib}
        component=components[ia]
        if not ledger['components'][component]['deficient']:
            return dict(accepted=False,reason='Donor request is not in a deficient tree.',bridge=k)
        bo,be=ordered_stem(data,ps[ib]);cut=bo.index(own[e[1]])
        prefix=set().union(set(),*(data[3][o] for o in bo[:cut]))
        suffix=set().union(set(),*(data[3][o] for o in bo[cut:]))
        pre=sorted(j for j in prefix if users[j]=={ib})
        post=sorted(j for j in suffix if users[j]=={ib})
        pair=next(((l,r) for l in pre for r in post if l!=r),None) if witnesses is None else witnesses[k]
        if pair is not None and not (pair[0] in pre and pair[1] in post and pair[0]!=pair[1]):
            return dict(accepted=False,reason='Supplied geometric witnesses are not distinct private pre/post units.',bridge=k)
        if pair is None:return dict(accepted=False,reason='No distinct request-private prefix/suffix units.',bridge=k)
        assert not ledger['components'][components[ib]]['deficient']
        records.append(dict(index=k,donor=ia,receiver=ib,component=component,
            prefix=prefix,suffix=suffix,pre=pair[0],post=pair[1]))
    return dict(accepted=True,records=records,neighbours=neighbours,users=users,ledger=ledger)


def lift(data,frame,matching):
    """Standard old-request allocation lift, with its specific unit IDs kept."""
    own,A,B,X=owner_data(*data[:2]);W=data[3];result=[]
    for i,p in enumerate(frame['certificates']):
        sources=set(p['owners'])&A
        if p['kind']=='beta':result.append(dict(p));continue
        outgoing={own[u]:(u,v) for u,v in p['links']};arms={}
        for a in sources:
            os=[a];es=[]
            while os[-1] in outgoing:
                e=outgoing[os[-1]];es.append(e);os.append(own[e[1]])
            arms[a]=os,es
        def truncate(a,stop=None,unit=None):
            os,es=arms[a]
            if stop is None:return dict(kind='beta',owners=tuple(sorted(os)),links=tuple(es),
                interval=None,value=1,beta=os[-1])
            pos=os.index(stop)
            return stem(tuple(sorted(os[:pos+1])),es[:pos],unit,witness=stop)
        if i not in matching:
            if p['kind']=='fork':result.append(truncate(min(sources)))
            continue
        j=matching[i];witness=min(o for o in p['owners'] if j in W[o])
        if p['kind']=='interval':result.append(truncate(next(iter(sources)),witness,j))
        elif witness==p['beta']:result.append(dict(p,interval=j))
        else:
            a=next(a for a in sources if witness in arms[a][0]);b=next(iter(sources-{a}))
            result.extend([truncate(a,witness,j),truncate(b)])
    os=[o for p in result for o in p['owners']];js=[p['interval'] for p in result if p['interval'] is not None]
    assert len(os)==len(set(os)) and len(js)==len(set(js))
    paid=set(os)&A
    return dict(value=len(paid),paid=sorted(paid),used=set(js),certificates=result,
                links=[e for p in result for e in p['links']])


def solve_private(data,pack,bridges,fees=None,new_sources=frozenset(),baseline_matching=None,witnesses=None):
    frame=frame_with_direct_sources(data,pack,new_sources)
    c=recognize_private(data,frame,bridges,witnesses)
    if not c['accepted']:return c
    fees=dict.fromkeys(range(len(bridges)),1) if fees is None else fees
    assert set(fees)==set(range(len(bridges))) and all(isinstance(w,int) and w>=0 for w in fees.values())
    old=dict(c['ledger']['matching'] if baseline_matching is None else baseline_matching)
    assert len(old)==len(c['neighbours'])-c['ledger']['deficiency']
    assert len(set(old.values()))==len(old) and all(j in c['neighbours'][d] for d,j in old.items())
    before=lift(data,frame,old);chosen={}
    for r in c['records']:
        T=r['component']
        if T not in chosen or (fees[r['index']],r['index'])<(fees[chosen[T]['index']],chosen[T]['index']):chosen[T]=r
    matching=dict(old);mode=frame;fresh=[]
    for T,r in sorted(chosen.items()):
        ia,ib=r['donor'],r['receiver'];tree=set(c['ledger']['components'][T]['demands'])
        rooted=allocation({d:c['neighbours'][d] for d in tree},tree-{ia})
        assert set(rooted['matching'])==tree-{ia}
        assert set(rooted['matching'].values())==set(c['ledger']['components'][T]['resources'])
        for d in tree:matching.pop(d,None)
        matching.update(rooted['matching'])
        previous=matching[ib];l,s=r['pre'],r['post']
        if previous not in (l,s):
            if previous in r['prefix']:l=previous
            else:assert previous in r['suffix'];s=previous
        assert l!=s and previous in (l,s) and l in r['prefix'] and s in r['suffix']
        added=s if l==previous else l
        assert added not in before['used'];fresh.append(added)
        matching[ib]=l;matching[ia]=s
        mode=switched_skeleton(data,mode,bridges[r['index']])
    newneighbours,_=request_data(data,mode)
    assert all(j in newneighbours[d] for d,j in matching.items())
    assert len(set(matching.values()))==len(matching)
    after=lift(data,mode,matching);indices=sorted(r['index'] for r in chosen.values())
    assert set(before['paid'])<=set(after['paid']) and before['used']<=after['used']
    assert after['used']-before['used']==set(fresh) and len(set(fresh))==len(chosen)
    assert after['value']==before['value']+len(chosen)
    actual=[i for i,e in enumerate(bridges) if e in after['links']]
    assert actual==indices
    return dict(accepted=True,**after,old_value=before['value'],old_paid=before['paid'],old_used=before['used'],
        added=set(fresh),selected=indices,bridge_fee=sum(fees[i] for i in indices),
        repaired_trees=len(chosen),old_deficiency=c['ledger']['deficiency'],
        remaining_deficiency=c['ledger']['deficiency']-len(chosen))


def check(data,pack,bridges,fees,counts,new_sources=frozenset(),all_baselines=False,baseline_matching=None,witnesses=None):
    frame=frame_with_direct_sources(data,pack,new_sources);c=recognize_private(data,frame,bridges,witnesses);assert c['accepted']
    answer=solve_private(data,pack,bridges,fees,new_sources,baseline_matching,witnesses)
    # Independent mode algorithm and primitive packing check exact value/fee.
    other=bridge_batch(data,frame,bridges,fees)
    assert (answer['value'],answer['bridge_fee'])==(other['value'],other['bridge_fee'])
    E0={e for p in frame['certificates'] for e in p['links']}
    selected_owners=set().union(set(),*(set(p['owners']) for p in frame['certificates']))
    d=(*data[:2],sorted(E0|set(bridges)),{o:S if o in selected_owners else set() for o,S in data[3].items()},data[4])
    independent=optimize(*d);assert independent['value']==answer['value']==fork_flow(*d)['value']
    legal={signature(p) for p in primitive_certificates(*d)}
    assert all(signature(p) in legal for p in answer['certificates'])
    counts['independent_value_and_bridge_fee_optima']+=1
    counts['retained_paid_source_and_unit_set_checks']+=1
    if all_baselines:
        ds=sorted(c['neighbours']);best=len(ds)-c['ledger']['deficiency']
        def visit(pos,matching,used):
            if pos==len(ds):
                if len(matching)!=best:return
                z=solve_private(data,pack,bridges,fees,new_sources,matching,witnesses)
                assert (z['value'],z['bridge_fee'])==(answer['value'],answer['bridge_fee'])
                assert set(matching.values())<=z['used']
                counts['all_maximum_baseline_identity_checks']+=1
                return
            d=ds[pos];visit(pos+1,matching,used)
            for j in c['neighbours'][d]-used:visit(pos+1,dict(matching)|{d:j},used|{j})
        visit(0,{},set())
    return answer


def abstract_controls(counts,rng):
    kinds,pairs,_=canonical('AAAAMM');bridges=[(0,8),(2,10)]
    pack=dict(certificates=[stem((2,4),[(4,8)]),stem((3,5),[(6,10)])])
    W={0:{0},1:{0},2:{1},3:{3},4:{2},5:{4}}
    data=kinds,pairs,[(4,8),(6,10)]+bridges,W,set(range(5))
    z=check(data,pack,bridges,{0:5,1:2},counts,{0,1},all_baselines=True)
    assert (z['old_value'],z['value'],z['repaired_trees'],z['bridge_fee'],z['selected'])==(3,4,1,2,[1])
    # Same receiver component, distinct private pairs: no double use.
    for rep in range(28):
        W={0:set(),1:set(),2:{0,4},3:{2,4},4:{1},5:{3}}
        if rep%2:W[0].add(5);W[1].add(5)
        Q=set().union(*W.values())
        # Extra request-private alternatives on either side test preservation
        # when the old assigned unit is neither displayed witness.
        for j in range(6,6+rep%4):W[rng.choice((2,3,4,5))].add(j);Q.add(j)
        data=kinds,pairs,[(4,8),(6,10)]+bridges,W,Q
        z=check(data,pack,bridges,{0:rep%5,1:(rep*3)%7},counts,{0,1},all_baselines=rep<8)
        assert z['repaired_trees']==(1 if rep%2 else 2)
    # Merely private to the union of TWO receivers is insufficient.
    W={0:set(),1:set(),2:{0},3:{1},4:{2},5:{2}}
    data=kinds,pairs,[(4,8),(6,10)]+bridges,W,{0,1,2}
    rejected=solve_private(data,pack,bridges,new_sources={0,1})
    assert not rejected['accepted']
    counts['nonprivate_shared_reserve_rule_rejections']+=1


def frozen(copies,counts,production=False):
    base=load_model()[0];R,C,T,M=base;shift=lambda v,k:(v[0]+30*k,v[1])
    cur=(30*copies-2,24,{shift(v,k) for k in range(copies) for v in T},
         [tuple(shift(v,k) for v in e) for k in range(copies) for e in M])
    bits={(r,c):False for r in range(0,cur[0],2) for c in range(0,24,2)}
    direct_check(*cur);data,closed,_=compile_model(cur,regions(cur,bits));own,A,B,X=owner_data(*data[:2])
    raw=json.loads(FIXTURE.read_text());rr=[[shift(tuple(v),k) for k in range(copies) for v in layer] for layer in raw['freezing_layers']]
    assert len(check_rank_certificate(cur,rr))==308*copies and frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
    counts['strict_freezing_events']+=308*copies
    fs=forests(cur,regions(cur,bits));bycells={cc:j for j,(cap,cc) in fs.items() if cap}
    ps=[];bridges=[];new=set();tiles=[];baseline={};witnesses={}
    for k in range(copies):
        get=lambda r,c:own[shift((r,c),k)]
        unit=lambda r,c:bycells[frozenset({shift((r,c),k),shift((r+1,c),k)})]
        eleft=tuple(shift(v,k) for v in ((5,4),(5,5)))
        eright=tuple(shift(v,k) for v in ((24,19),(24,20)))
        ebottom=tuple(shift(v,k) for v in ((24,17),(24,18)))
        ps.extend([stem(tuple(sorted((get(5,4),get(5,5)))),[eleft],unit(14,6),get(5,5)),
                   stem(tuple(sorted((get(24,19),get(24,20)))),[eright],unit(24,23),get(24,20)),
                   stem(tuple(sorted((get(24,17),get(24,18)))),[ebottom],unit(14,13),get(24,18))])
        bridges.append(tuple(shift(v,k) for v in ((5,6),(5,5))));new.add(get(5,6))
        tile=shift((14,6),k);assert not tile_cells(tile)&(cur[2]|{v for e in cur[3] for v in e})
        j0,j1=unit(14,6),unit(14,7);assert j0!=j1
        assert {o for o,S in data[3].items() if j0 in S}=={get(5,4),get(5,5)}
        assert {o for o,S in data[3].items() if j1 in S}=={get(5,4),get(5,5)}
        witnesses[k]=(j0,j1)
        baseline.update({3*k:unit(14,6),3*k+1:unit(24,23),3*k+2:unit(14,13)})
        tiles.append(dict(tile=tile,units=[j0,j1],boundary_owners=[get(5,4),get(5,5)]))
    pack=dict(certificates=ps);fees={i:1+i%3 for i in range(copies)}
    if production:
        with patch(__name__+'.bridge_batch',side_effect=AssertionError('No 2^k modes')), \
             patch(__name__+'.optimize',side_effect=AssertionError('No primitive packs')), \
             patch(__name__+'.fork_flow',side_effect=AssertionError('No full flow')):
            z=solve_private(data,pack,bridges,fees,new,baseline,witnesses)
        counts['production_no_mode_pack_or_flow_enumeration']+=1
    elif copies<=2:
        z=check(data,pack,bridges,fees,counts,new,baseline_matching=baseline,witnesses=witnesses)
        initial={signature(p) for p in primitive_certificates(*data)}
        assert all(signature(p) in initial for p in ps)
    else:
        z=solve_private(data,pack,bridges,fees,new,baseline,witnesses)
        assert fork_flow(*data)['value']==z['value']
        counts['polynomial_full_flow_physical_crosschecks']+=1
    assert (z['old_value'],z['value'],z['repaired_trees'],z['bridge_fee'])==(3*copies,4*copies,copies,sum(fees.values()))
    assert z['remaining_deficiency']==0 and set(z['paid'])==A and len(z['added'])==copies
    assert z['old_used']=={p['interval'] for p in ps}
    assert all(set(t['units'])<=z['used'] for t in tiles)
    counts['frozen_cap_two_prefix_suffix_boards']+=1
    return dict(copies=copies,shape=list(cur[:2]),old_payment=z['old_value'],new_payment=z['value'],
        old_used=len(z['old_used']),retained_all_old_units=z['old_used']<=z['used'],
        new_distinct_units=len(z['added']),new_bridges=len(z['selected']),fee=z['bridge_fee'],
        old_deficiency=z['old_deficiency'],geometric_capacity_two_tiles=tiles[:1],
        production_polynomial=production)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();rng=random.Random(2026102671);abstract_controls(counts,rng)
    records=[frozen(q,counts) for q in (1,2,4)];records.append(frozen(16,counts,production=True))
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(counts),physical=records,
        proof='docs/PRIVATE_PREFIX_BRIDGE_COMPENSATION.md',
        scope='Distinct request-private pre-entry/post-entry units for bridges on disjoint old stem pairs; donor requests in deficient trees. Eligible new direct sources included. Exact polynomial value and minimum actual bridge fee; preserves any maximum request-allocation baseline paid sources and used original units.',
        limitations=['Not arbitrary shared-path bridge networks.','Privacy is relative to all declared requests, not just two selected sources.','No universal 5/6 improvement.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(counts),physical=records),indent=2))


if __name__=='__main__':main()
