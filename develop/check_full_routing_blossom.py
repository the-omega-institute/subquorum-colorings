"""One weighted matching for full mixed/beta routing and size-two shared fees.

General reduction: docs/FULL_ROUTING_WEIGHTED_MATCHING.md. The production API
uses NetworkX's integer-weight blossom algorithm; exhaustive checks and the
older 2^h flow solver are independent audits only.
"""
import argparse
from collections import Counter, defaultdict
import json
from pathlib import Path
import random
from unittest.mock import patch

import networkx as nx

from check_compensation_flow_normal_form import owner_data
from check_positive_capacity_handoffs import compile_handoffs, compiled_support, snapshot, endpoint_trap, tile_cells
from check_positive_extreme_shared_fees import (
    reduce_extremes, solve_reduced, reduced_data, abstract_instance, sharing_contract,
    paid_legacy_contract, frozen_board, bundle_fixture, subsets,
)
from check_whole_support_fork_normal_form import canonical, optimize, primitive_certificates
from check_whole_support_fork_flow import fork_flow
from check_destructive_exchange_choice import constrained_optimum
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_canonical_band_coarsening import random_board

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def path_fee(paths,offers,groups):
    used={p['output'][1] for p in paths if p['output'][0]=='resource'}
    selected={i for i,g in enumerate(groups) if used&set(g['units'])}
    access=sum(offers[p['offer']]['fee'] for p in paths if p['offer'] is not None)
    return access+sum(groups[i]['fee'] for i in selected),selected


def normalize_beta_routes(paths):
    grouped_paths=defaultdict(list)
    for p in paths:
        if p['beta'] is not None:grouped_paths[p['beta']].append(p)
    count=0
    for b,ps in grouped_paths.items():
        assert 1<=len(ps)<=2
        if not any(p['output']==('whole-beta',b) for p in ps):
            ps[0]['output']=('whole-beta',b);ps[0]['offer']=None;ps[0]['witness']=None;count+=1
        assert sum(p['output']==('whole-beta',b) for p in ps)==1
    return count


def solve_grouped_access(base,offers,groups,required=frozenset()):
    """Exact generic routing problem; each optional group has <=2 outputs.

    base: full owner/type/link network with fixed supports and original Q.
    offers: {owner,unit,fee}, nonnegative linear access fee.
    groups: {units: [one or two original IDs], fee: once if any is used}.
    Group units have no fixed support and groups are pairwise disjoint.
    Extra ungrouped offers are allowed. Returns a normalized actual pack.
    """
    kinds,pairs,links,W,Q=base;own,A,B,M=owner_data(kinds,pairs)
    assert required<=A and set(W)==set(range(len(pairs)))
    assert all(S<=Q for S in W.values())
    assert all(o['owner'] in W and o['unit'] in Q and isinstance(o['fee'],int) and o['fee']>=0 for o in offers)
    grouped=[j for g in groups for j in g['units']]
    assert all(len(g['units']) in (1,2) and isinstance(g['fee'],int) and g['fee']>=0 for g in groups)
    assert len(grouped)==len(set(grouped)) and set(grouped)<=Q
    assert not any(set(grouped)&S for S in W.values())
    # A safe scalar range for EVERY matching, even one with unsaturated
    # ports: each original output uses <=1 access, links leave A/M at most1.
    H=len(A)+len(M);K=H+1
    group_total=sum(g['fee'] for g in groups)
    access_total=sum(o['fee'] for o in offers)
    span=K*(group_total+access_total)+H
    payment_bonus=span+1
    required_bonus=payment_bonus*len(A)+span+1
    port_bonus=required_bonus*len(required)+payment_bonus*len(A)+span+1
    graph=nx.Graph();ports=set();sources={('source',a):a for a in A}
    minus_m=lambda m:('mixed-in',m)
    plus_m=lambda m:('mixed-out',m)
    minus_b=lambda tip:('beta-in',tip)
    plus_b=lambda tip:('beta-out',tip)
    outs=lambda o:[('source',o)] if o in A else [plus_m(o)] if o in M else [plus_b(t) for t in pairs[o]]
    for m in M:ports.update((minus_m(m),plus_m(m)))
    for b in B:
        for t in pairs[b]:ports.update((minus_b(t),plus_b(t)))
    graph.add_nodes_from(ports|set(sources))
    graph.add_nodes_from(('resource',j) for j in Q)
    graph.add_nodes_from(('whole-beta',b) for b in B)
    def add(u,v,lower,tag):
        w=lower+port_bonus*(int(u in ports)+int(v in ports))
        for endpoint in (u,v):
            if endpoint in sources:
                a=sources[endpoint];w+=payment_bonus+required_bonus*int(a in required)
        if not graph.has_edge(u,v) or w>graph[u][v]['weight']:
            graph.add_edge(u,v,weight=w,tag=tag,lower=lower)
    for m in M:add(minus_m(m),plus_m(m),0,('internal',m))
    for b in B:
        for t in pairs[b]:
            add(minus_b(t),plus_b(t),0,('internal-beta',t))
            add(plus_b(t),('whole-beta',b),0,('beta',b,t))
    for p,q in set(links):
        assert kinds[p]=='TP' and kinds[q]=='BP'
        if own[p]==own[q]:continue
        assert own[p] in A|M and own[q] in B|M
        u=outs(own[p])[0];v=minus_b(q) if own[q] in B else minus_m(own[q])
        add(u,v,-1,('link',p,q))
    for o,S in W.items():
        for j in S:
            for u in outs(o):add(u,('resource',j),0,('access',o,j,None))
    for i,o in enumerate(offers):
        for u in outs(o['owner']):
            add(u,('resource',o['unit']),-K*o['fee'],('access',o['owner'],o['unit'],i))
    for i,g in enumerate(groups):
        endpoints=[('resource',j) for j in g['units']]
        if len(endpoints)==1:endpoints.append(('dummy',i))
        add(*endpoints,K*g['fee'],('idle',i))
    matching=nx.max_weight_matching(graph,maxcardinality=False,weight='weight')
    mate={u:v for u,v in matching for u,v in ((u,v),(v,u))}
    assert ports<=mate.keys()
    paid={a for v,a in sources.items() if v in mate}
    if not required<=paid:return dict(feasible=False,paid=sorted(paid))
    # Covered port pairs are either matched internally (inactive) or have
    # one incoming link and one outgoing link/access. Rebuild directed paths.
    forward={};active_internal=set()
    for u,v in matching:
        tag=graph[u][v]['tag']
        if tag[0]=='link':
            p,q=tag[1:];forward[outs(own[p])[0]]=(minus_b(q) if own[q] in B else minus_m(own[q]),tag)
        elif tag[0]=='access':
            o,j,i=tag[1:]
            start=v if u==('resource',j) else u
            forward[start]=(('resource',j),tag)
        elif tag[0]=='beta':
            b,t=tag[1:];forward[plus_b(t)]=(('whole-beta',b),tag)
    for m in M:
        if mate[minus_m(m)]!=plus_m(m):active_internal.add((minus_m(m),plus_m(m)))
    for b in B:
        for t in pairs[b]:
            if mate[minus_b(t)]!=plus_b(t):active_internal.add((minus_b(t),plus_b(t)))
    for u,v in active_internal:forward[u]=(v,('through',))
    traversed=set();paths=[]
    for a in sorted(paid):
        u=('source',a);seen=set();tags=[]
        while u in forward:
            assert u not in seen;seen.add(u);traversed.add(u)
            v,tag=forward[u];tags.append(tag);u=v
        assert u[0] in ('resource','whole-beta')
        actual_links=[(t[1],t[2]) for t in tags if t[0]=='link']
        beta=[own[q] for p,q in actual_links if own[q] in B]
        assert len(beta)<=1
        last=tags[-1]
        paths.append(dict(source=a,links=actual_links,beta=beta[0] if beta else None,
            output=u,offer=last[3] if last[0]=='access' else None,
            witness=last[1] if last[0]=='access' else None))
    # A source-free directed component would be a positive-link-cost cycle;
    # replacing its route matches with internal edges strictly improves W.
    assert traversed==set(forward)
    # Complete idle edges at zero fee as well, for an exact weight identity.
    for i,g in enumerate(groups):
        ep=[('resource',j) for j in g['units']]
        if len(ep)==1:ep.append(('dummy',i))
        if all(v not in mate for v in ep):
            assert g['fee']==0
            matching.add(tuple(ep));mate[ep[0]]=ep[1];mate[ep[1]]=ep[0]
    rawfee,_=path_fee(paths,offers,groups);nlinks=sum(len(p['links']) for p in paths)
    weight=sum(graph[u][v]['weight'] for u,v in matching)
    assert weight==len(ports)*port_bonus+len(paid)*payment_bonus+len(required)*required_bonus+K*group_total-K*rawfee-nlinks
    normalizations=normalize_beta_routes(paths)
    fee,usedgroups=path_fee(paths,offers,groups)
    # If normalization decreased this cost, its matching completion would
    # improve the optimum. Thus an optimal raw matching already has the
    # same fee as the resulting physical normalized pack.
    assert fee==rawfee and nlinks<=H
    intervals=[p['output'][1] for p in paths if p['output'][0]=='resource']
    assert len(intervals)==len(set(intervals))
    ordinary_owners=[]
    for p in paths:
        owners={p['source']}|{own[q] for _,q in p['links'] if own[q] in M}
        ordinary_owners+=list(owners)
    assert len(ordinary_owners)==len(set(ordinary_owners))
    return dict(feasible=True,value=len(paid),fee=fee,links=nlinks,paid=sorted(paid),
        chosen_offers=sorted(p['offer'] for p in paths if p['offer'] is not None),used_groups=sorted(usedgroups),
        paths=paths,matching_weight=weight,port_bonus=port_bonus,payment_bonus=payment_bonus,
        required_bonus=required_bonus,fee_scale=K,covered_ports=len(ports),
        graph_nodes=len(graph),graph_edges=graph.number_of_edges(),matching_calls=1,
        beta_private_normalizations=normalizations)


def solve_reduced_blossom(reduced,weights,required=frozenset()):
    offers=[dict(owner=o['owner'],unit=o['unit'],fee=sum(weights[g] for g in o['gates']-reduced['cores']))
            for o in reduced['offers']]
    groups=[]
    for c in reduced['corridors']:
        if c['core'] is not None:groups.append(dict(units=c['units'],fee=weights[c['core']]))
    result=solve_grouped_access(reduced['base'],offers,groups,required)
    if result['feasible']:
        opened=set().union(set(),*(reduced['offers'][i]['gates'] for i in result['chosen_offers']))
        assert result['fee']==sum(weights[g] for g in opened)
        result.update(opened=sorted(opened),sharing_pivots=len(reduced['cores']))
    return result


def solve_positive_blossom(cur,bits,gates,weights,required=frozenset()):
    c=compile_handoffs(cur,bits,gates)
    if not c['accepted']:return dict(accepted=False,losses=c['losses'])
    reduced=reduce_extremes(c,gates,weights)
    result=solve_reduced_blossom(reduced,weights,required)
    if result['feasible']:result['opened_tiles']=[gates[i] for i in result['opened']]
    return dict(accepted=True,**result)


def strip_paths(result):
    return {k:v for k,v in result.items() if k!='paths'}


def audit_path_certificates(base,offers,result,counts):
    """Independent original primitive checker for the reconstructed pack."""
    own,A,B,M=owner_data(*base[:2]);W={o:set(S) for o,S in base[3].items()}
    for e in offers:W[e['owner']].add(e['unit'])
    data=(*base[:3],W,base[4]);candidates=primitive_certificates(*data)
    sig=lambda p:(p['kind'],tuple(sorted(p['owners'])),tuple(sorted(p['links'])),p['interval'],p['value'],p.get('witness'),p.get('beta'))
    possible={sig(p) for p in candidates};beta=defaultdict(list);certs=[]
    for p in result['paths']:
        if p['beta'] is not None:beta[p['beta']].append(p);continue
        owners={p['source']}|{own[q] for _,q in p['links']}
        certs.append(dict(kind='interval',owners=owners,links=p['links'],interval=p['output'][1],value=1,witness=p['witness']))
    for b,ps in beta.items():
        intervals=[p for p in ps if p['output'][0]=='resource'];assert len(intervals)==len(ps)-1
        owners={b}|{p['source'] for p in ps}|{own[q] for p in ps for _,q in p['links']}
        certs.append(dict(kind='fork' if len(ps)==2 else 'beta',owners=owners,
            links=[e for p in ps for e in p['links']],interval=intervals[0]['output'][1] if intervals else None,
            value=len(ps),beta=b,**(dict(witness=b) if intervals else {})))
    for p in certs:assert sig(p) in possible
    occupied=[o for p in certs for o in p['owners']]
    assert len(occupied)==len(set(occupied))
    assert set(occupied)&A==set(result['paid'])
    assert sum(p['value'] for p in certs)==result['value']
    assert sum(len(p['links']) for p in certs)==result['links']
    counts['reconstructed_packs_checked_by_original_primitives']+=1
    counts['reconstructed_beta_fork_certificates']+=sum(p['kind']=='fork' for p in certs)


def audit_reduced(c,gates,weights,counts,physical=None,all_states=True,required_checks=True):
    reduced=reduce_extremes(c,gates,weights);b=solve_reduced_blossom(reduced,weights)
    f=solve_reduced(reduced,weights)
    assert b['feasible'] and (b['value'],b['fee'],b['links'])==(f['value'],f['fee'],f['links'])
    counts['blossom_vs_previous_parameterized_flow_optima']+=1
    counts['beta_private_normalizations']+=b['beta_private_normalizations']
    audit_path_certificates(reduced['base'],reduced['offers'],b,counts)
    records={}
    for F in subsets(range(len(gates))) if all_states else [frozenset(),frozenset(range(len(gates)))]:
        d=(*c['old']['data'][:3],compiled_support(c,F),c['old']['data'][4]);p=optimize(*d)
        records[F]=(p['value'],sum(weights[g] for g in F),p['cost'],d)
        counts['independent_primitive_physical_or_contract_states']+=1
    if all_states:
        best=max(records.values(),key=lambda t:(t[0],-t[1],-t[2]))
        assert (b['value'],b['fee'],b['links'])==best[:3]
        counts['joint_optima_vs_complete_gate_enumeration']+=1
    F=frozenset(b['opened']);d=(*c['old']['data'][:3],compiled_support(c,F),c['old']['data'][4])
    assert constrained_optimum(d)==(b['value'],b['links'])
    if physical is not None:
        cur,bits=physical;s=snapshot(cur,bits,gates,F)
        assert s['data'][3]==d[3]
        for p in b['paths']:
            if p['output'][0]=='resource':assert p['output'][1] in s['data'][3][p['witness']]
        counts['reconstructed_optimal_physical_states']+=1
    if required_checks and all_states:
        _,A,_,_=owner_data(*c['old']['data'][:2])
        for P in subsets(A):
            old=constrained_optimum(records[frozenset()][3],P)
            answer=solve_reduced_blossom(reduced,weights,P)
            candidates=[]
            for value,fee,links,data in records.values():
                a=constrained_optimum(data,P)
                if a is not None:candidates.append((a[0],fee,a[1]))
            if not candidates:
                assert not answer['feasible'];counts['infeasible_required_source_sets']+=1
                continue
            best=max(candidates,key=lambda t:(t[0],-t[1],-t[2]))
            assert answer['feasible'] and (answer['value'],answer['fee'],answer['links'])==best
            assert P<=set(answer['paid'])
            if old is not None:assert best[:2]==(b['value'],b['fee'])
            counts['prescribed_source_optima']+=1
    return strip_paths(b)


def generic_audit(counts,rng):
    """Independent one/two-slot bundles, arbitrary access fees/full routing."""
    records=[]
    for index in range(130):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,5)))
        kinds,pairs,links=canonical(types);rng.shuffle(links);links=links[:rng.randrange(min(10,len(links))+1)]
        Q=set(range(rng.randrange(1,7)));W={o:set() for o in range(len(pairs))};offers=[];groups=[]
        remain=sorted(Q)
        for _ in range(rng.randrange(1,4)):
            if not remain:break
            n=min(len(remain),rng.randrange(1,3));units=remain[:n];remain=remain[n:]
            groups.append(dict(units=units,fee=rng.randrange(6)))
        for j in Q:
            for o in W:
                if j in remain and rng.random()<.25:W[o].add(j)
                elif rng.random()<.3:offers.append(dict(owner=o,unit=j,fee=rng.randrange(4)))
        base=(kinds,pairs,links,W,Q)
        b=solve_grouped_access(base,offers,groups)
        audit_path_certificates(base,offers,b,counts)
        # Independent audit enumerates EVERY normalized pack and selects
        # cheapest incoming access separately; it never uses the blossom graph.
        from check_positive_extreme_shared_fees import all_normalized_packs
        enabledW={o:set(S) for o,S in W.items()}
        for e in offers:enabledW[e['owner']].add(e['unit'])
        data=(*base[:3],enabledW,Q);candidates=[]
        for pack in all_normalized_packs(data):
            assigned=[(p['witness'],p['interval']) for p in pack['certificates'] if p['interval'] is not None]
            lin=sum(0 if j in W[o] else min(e['fee'] for e in offers if e['owner']==o and e['unit']==j) for o,j in assigned)
            used={j for o,j in assigned}
            fee=lin+sum(g['fee'] for g in groups if set(g['units'])&used)
            links_used=sum(len(p['links']) for p in pack['certificates'])
            paid=set().union(set(),*(set(p['owners']) for p in pack['certificates']))&owner_data(kinds,pairs)[1]
            candidates.append((pack['value'],fee,links_used,paid))
            counts['generic_all_compatible_packs']+=1
            counts['generic_compatible_beta_forks']+=sum(p['kind']=='fork' for p in pack['certificates'])
        best=max(candidates,key=lambda t:(t[0],-t[1],-t[2]))
        assert (b['value'],b['fee'],b['links'])==best[:3]
        for P in subsets(owner_data(kinds,pairs)[1]):
            eligible=[t for t in candidates if P<=t[3]];answer=solve_grouped_access(base,offers,groups,P)
            if not eligible:assert not answer['feasible']
            else:
                expected=max(eligible,key=lambda t:(t[0],-t[1],-t[2]))
                assert answer['feasible'] and (answer['value'],answer['fee'],answer['links'])==expected[:3]
            counts['generic_prescribed_source_audits']+=1
        counts['generic_full_routing_bundle_models']+=1
        counts['beta_private_normalizations']+=b['beta_private_normalizations']
        if index<4:records.append(strip_paths(b))
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();examples={};rng=random.Random(2026102647)
    for left,right in ((1,1),(2,3),(16,17)):
        for one in (False,True):
            cur,bits,ranks,l,r,q=frozen_board(left,right,one);central=(2,16+2*q)
            bits[central]=True;gates=l+r+[central];weights={i:1+(i%3) for i in range(len(gates))}
            c=compile_handoffs(cur,bits,gates);assert c['accepted']
            examples[f'frozen_{left}_{right}_one{one}']=audit_reduced(c,gates,weights,counts,(cur,bits),all_states=len(gates)<9)
            counts['strict_freeze_events']+=len(check_rank_certificate(cur,ranks))
    cur,bits,ranks,gates=bundle_fixture();c=compile_handoffs(cur,bits,gates)
    for fee in (0,3,5,7):
        weights={0:fee,1:3,2:3}
        row=audit_reduced(c,gates,weights,counts,(cur,bits))
        assert (row['value'],row['fee'],row['links'])==(4,min(fee,6),2)
        examples['frozen_cost'+str(fee)]=row
    counts['strict_freeze_events']+=len(check_rank_certificate(cur,ranks))
    for name,types,endpoints,links,fees,one in [
        ('beta_mixed_two_cores','AAAABM',[(4,5),(2,3)],[(0,8),(2,9),(4,10),(6,10)],[(1,3,2),(2,4,1)],False),
        ('one_beta_both_ends','AAB',[(2,2)],[(0,4),(2,5)],[(1,5,3)],False),
        ('single_output','AA',[(0,1)],[],[(1,5,3)],True),
        ('three_cores','AAAAMM',[(0,1),(2,3),(4,5)],[(0,8),(2,8),(4,10),(6,10)],[(1,4,2),(2,3,1),(1,5,1)],False),
    ]:
        ac,ag,aw=sharing_contract(types,endpoints,links,fees,one)
        examples[name]=audit_reduced(ac,ag,aw,counts)
    for same in (False,True):
        ac,ag,aw=paid_legacy_contract(same);examples['legacy'+str(same)]=audit_reduced(ac,ag,aw,counts)
    # Full shared-capacity controls, independent of any corridor drawing.
    kinds,pairs,_=canonical('AAM');base=(kinds,pairs,[(0,4),(2,4)],{0:set(),1:set(),2:set()},{0,1})
    offers=[dict(owner=2,unit=j,fee=0) for j in (0,1)];groups=[dict(units=[0,1],fee=3)]
    answer=solve_grouped_access(base,offers,groups)
    assert (answer['value'],answer['fee'],answer['links'])==(1,3,1)
    examples['shared_mixed_capacity_one']=strip_paths(answer)
    for distinct in (False,True):
        kinds,pairs,_=canonical('AAB')
        base=(kinds,pairs,[(0,4),(2,5 if distinct else 4)],{0:set(),1:set(),2:set()},{0,1})
        answer=solve_grouped_access(base,offers,groups)
        assert (answer['value'],answer['fee'],answer['links'])==((2,3,2) if distinct else (1,0,1))
        examples['beta_distinct_entries'+str(distinct)]=strip_paths(answer)
    # Port saturation forbids a paid source path that dies at a mixed entry.
    kinds,pairs,_=canonical('AM');base=(kinds,pairs,[(0,2)],{0:set(),1:set()},set())
    answer=solve_grouped_access(base,[],[])
    assert answer['value']==answer['fee']==answer['links']==0
    examples['no_dangling_source_path']=strip_paths(answer)
    kinds,pairs,_=canonical('AMM');base=(kinds,pairs,[(3,4),(5,2)],{o:set() for o in range(3)},set())
    answer=solve_grouped_access(base,[],[])
    assert answer['value']==answer['links']==0
    examples['unused_mixed_cycle_removed']=strip_paths(answer)
    for types in ('','BMM'):
        kinds,pairs,_=canonical(types)
        links=[(3,4),(5,2)] if types else []
        answer=solve_grouped_access((kinds,pairs,links,{o:set() for o in range(len(pairs))},set()),[],[])
        assert answer['feasible'] and answer['value']==answer['fee']==answer['links']==0
        counts['empty_or_no_alpha_controls']+=1
    # Force beta normalizations that a chosen optimum may avoid by tie-break.
    import copy
    for slots in ([0],[0,1]):
        ps=[dict(source=i,beta=2,output=('resource',j),offer=i,witness=2,links=[(2*i,4+i)]) for i,j in enumerate(slots)]
        oo=[dict(owner=2,unit=j,fee=2) for j in slots]
        before=copy.deepcopy(ps);fee0,_=path_fee(ps,oo,[dict(units=[0,1],fee=5)])
        assert normalize_beta_routes(ps)==1
        fee1,_=path_fee(ps,oo,[dict(units=[0,1],fee=5)])
        assert fee1<=fee0 and [(p['source'],p['links']) for p in before]==[(p['source'],p['links']) for p in ps]
        counts['forced_beta_normalization_controls']+=1
    for _ in range(100):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,5)))
        ac,ag,aw=abstract_instance(rng,types);audit_reduced(ac,ag,aw,counts)
    generic=generic_audit(counts,rng)
    # Many genuinely physical positive sharing pivots. One matching, while
    # the preceding solver would enumerate 2^12 branch subsets.
    cur,bits,ranks,gates=bundle_fixture();n=12;R,C,T,M=cur
    stacked=(R*n,C,{(r+R*i,c) for i in range(n) for r,c in T},
             [tuple((r+R*i,c) for r,c in e) for i in range(n) for e in M])
    sb={(r+R*i,c):v for i in range(n) for (r,c),v in bits.items()}
    sg=[(r+R*i,c) for i in range(n) for r,c in gates]
    weights={i:(5 if i%3==0 else 3) for i in range(len(sg))}
    def forbidden(*a,**kw):raise AssertionError('one-matching API must not enumerate packs or branch gate sets')
    with patch(__name__+'.subsets',forbidden),patch(__name__+'.solve_reduced',forbidden),patch(__name__+'.optimize',forbidden),patch(__name__+'.constrained_optimum',forbidden),patch(__name__+'.fork_flow',forbidden):
        answer=solve_positive_blossom(stacked,sb,sg,weights)
    assert answer['accepted'] and answer['feasible'] and answer['matching_calls']==1
    assert (answer['value'],answer['fee'],answer['links'],answer['sharing_pivots'])==(48,60,24,12)
    physical=snapshot(stacked,sb,sg,frozenset(answer['opened']));ff=fork_flow(*physical['data'])
    assert (ff['value'],ff['cost'])==(48,24)
    sr=[[(r+R*i,c) for i in range(n) for r,c in layer] for layer in ranks]
    counts['strict_freeze_events']+=len(check_rank_certificate(stacked,sr))
    assert frozen_certificate(stacked)[0]=={v for e in stacked[3] for v in e}
    examples['twelve_physical_sharing_pivots_one_matching']=strip_paths(answer)
    counts['disabled_enumeration_and_branch_API_checks']+=1
    counts['reconstructed_optimal_physical_states']+=1
    cur,bits,gates=endpoint_trap()
    with patch(__name__+'.subsets',forbidden),patch(__name__+'.solve_reduced',forbidden):
        assert not solve_positive_blossom(cur,bits,gates,{0:1,1:1})['accepted']
    counts['disabled_enumeration_and_branch_API_checks']+=1
    result=dict(status='PASS',networkx_version=nx.__version__,counts=dict(counts),examples=examples,generic_controls=generic,
        scope='General written exact reduction to one maximum-weight matching for arbitrary full mixed/beta routing with disjoint optional one/two-output groups and nonnegative access fees. Physical adapter: every passing uniform all-capacity P-free opening input. No gate-subset enumeration in API, no universal 5/6 improvement.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(counts,sort_keys=True))


if __name__=='__main__':main()
