"""Positive-pivot extreme reassignment and exact shared-fee optimization.

General proofs: docs/POSITIVE_EXTREMES_AND_SHARED_FEES.md. The physical API
recognizes in linear snapshots, branches only on certified sharing pivots,
and uses integral min-cost flow per branch. Gate-subset and primitive-pack
enumeration occur only in the separate audit routines.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random
from unittest.mock import patch

from check_compensation_flow_normal_form import owner_data
from check_positive_capacity_handoffs import (
    compile_handoffs, compiled_support, snapshot, endpoint_trap, tile_cells,
)
from check_protected_linear_corridors import frozen_board, subsets
from check_whole_support_fork_normal_form import canonical, primitive_certificates, optimize
from check_whole_support_fork_flow import fork_flow
from check_destructive_exchange_choice import constrained_optimum
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_canonical_band_coarsening import random_board
from check_capacity_two_gate_bundles import physical as bundle_fixture

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def reduce_extremes(compiled,gates,weights):
    """Retain old-ID extreme offers; certify every actual fee overlap.

    The caller supplies the successful physical handoff compiler. Abstract
    uses below are audit-only instances of the separately stated corridor
    contract, not claimed embeddings into physical grids.
    """
    assert compiled['accepted']
    assert set(weights)==set(range(len(gates)))
    assert all(isinstance(w,int) and w>=0 for w in weights.values())
    old=compiled['old'];full=compiled['full'];oo=[];corridors=[];cores=set()
    H={j for j,v in full['axes'].items() if not v};seen=[];gate_seen=[]
    for ci,c in enumerate(compiled['gaps']):
        units=sorted(c['units'],key=lambda j:sorted(full['anchors'][j]))
        seen+=units;gate_seen+=c['gates'];ids=[]
        for side,uid in [('left',units[0] if units else None),('right',units[-1] if units else None)]:
            o=c[side]
            if o is None or uid is None:continue
            col=min(c for r,c in full['anchors'][uid])
            req=frozenset(g for g in c['gates'] if
                (gates[g][1]<=col if side=='left' else gates[g][1]+1>=col))
            legacy=uid in old['data'][3][o]
            if legacy:req=frozenset()
            ids.append(len(oo));oo.append(dict(corridor=ci,side=side,owner=o,unit=uid,gates=req,legacy=legacy))
        core=None
        if len(ids)==2:
            a,b=(oo[i] for i in ids);shared=a['gates']&b['gates']
            # Any overlap must be the common containing positive pivot.
            if shared:
                assert len(shared)==1
                g=next(iter(shared))
                assert all(full['anchors'][u]<=tile_cells(gates[g]) for u in (a['unit'],b['unit']))
                assert len(units) in (1,2)
                assert not any(u in S for S in old['data'][3].values() for u in units)
                if a['unit']!=b['unit'] and a['owner']!=b['owner'] and weights[g]>0:
                    assert len(units)==2
                    core=g;cores.add(g)
        corridors.append({**c,'units':units,'offers':ids,'core':core})
    assert set(seen)==H and len(seen)==len(H)
    assert sorted(gate_seen)==list(range(len(gates)))
    for i,a in enumerate(oo):
        for b in oo[i+1:]:
            overlap=a['gates']&b['gates']
            if overlap:
                assert a['corridor']==b['corridor']
                if a['unit']!=b['unit'] and a['owner']!=b['owner']:
                    assert {g for g in overlap if weights[g]>0}<=cores
    base=(*old['data'][:3],{o:set(S)-H for o,S in old['data'][3].items()},old['data'][4])
    return dict(base=base,offers=oo,corridors=corridors,cores=frozenset(cores),compiled=compiled)


def reduced_data(reduced,F):
    base=reduced['base'];W={o:set(S) for o,S in base[3].items()}
    for offer in reduced['offers']:
        if offer['gates']<=F:W[offer['owner']].add(offer['unit'])
    return (*base[:3],W,base[4])


def flow_branch(reduced,weights,enabled,required=frozenset(),split_shared=False):
    """One integral min-cost maximum fork flow; no independent DP check.

    Each enabled sharing pivot is paid once as a branch constant. The
    remaining offer charges are additive on every normalized physical pack.
    split_shared is audit-only: it deliberately double-charges the core.
    """
    base=reduced['base'];kinds,pairs,links,W,Q=base
    own,A,B,M=owner_data(kinds,pairs);assert required<=A
    H=len(A)+len(M);K=H+1;protect=K*sum(weights.values())+H+1
    cores=frozenset() if split_shared else reduced['cores']
    assert enabled<=cores
    source=('s',);sink=('t',);edges=[];adj=defaultdict(list)
    def add(u,v,cap,cost=0,tag=None):
        i=len(edges)
        edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
                      dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    exit=lambda o:('a',o) if o in A else ('out',o) if o in M else ('b',o)
    for a in sorted(A):add(source,exit(a),1,-protect if a in required else 0,('source',a))
    for m in sorted(M):add(('in',m),exit(m),1,tag=('mixed',m))
    for b in sorted(B):
        for tip in pairs[b]:add(('tip',tip),exit(b),1,tag=('tip',tip))
        add(exit(b),sink,1,tag=('beta',b))
    for j in sorted(Q):add(('resource',j),sink,1,tag=('resource',j))
    for p,q in sorted(set(links)):
        if own[p]!=own[q]:
            add(exit(own[p]),('tip',q) if own[q] in B else ('in',own[q]),len(A)+1,1,('link',p,q))
    for o,S in W.items():
        for j in sorted(S):add(exit(o),('resource',j),len(A)+1,tag=('access',o,j))
    for i,o in enumerate(reduced['offers']):
        if o['gates']&cores<=enabled:
            fee=sum(weights[g] for g in o['gates']-cores)
            add(exit(o['owner']),('resource',o['unit']),1,K*fee,('offer',i))
    value=0;nodes=set(adj)|{source,sink}
    while True:
        dist={source:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in dist:
                    alt=dist[e['u']]+e['cost']
                    if e['v'] not in dist or alt<dist[e['v']]:
                        dist[e['v']]=alt;parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in dist:break
        v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v);i=parent[v]
            edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1
    used=[e for e in edges[::2] if e['initial']>e['cap']]
    paid={e['tag'][1] for e in used if e['tag'][0]=='source'}
    if not required<=paid:return None
    chosen=[e['tag'][1] for e in used if e['tag'][0]=='offer']
    opened=set().union(set(),*(reduced['offers'][i]['gates'] for i in chosen))
    nlinks=sum(e['initial']-e['cap'] for e in used if e['tag'][0]=='link')
    linear=sum(sum(weights[g] for g in reduced['offers'][i]['gates']-cores) for i in chosen)
    actual=sum(weights[g] for g in opened);nominal=linear+sum(weights[g] for g in enabled)
    assert actual<=nominal and nlinks<=H
    return dict(value=value,fee=nominal,actual_fee=actual,links=nlinks,opened=sorted(opened),paid=sorted(paid),
                chosen_offers=chosen,enabled_cores=sorted(enabled),scale=K)


def solve_reduced(reduced,weights,required=frozenset()):
    """Enumerate only the certified sharing cores, not physical gate sets."""
    cores=sorted(reduced['cores']);best=None
    for mask in range(1<<len(cores)):
        enabled=frozenset(g for i,g in enumerate(cores) if mask>>i&1)
        result=flow_branch(reduced,weights,enabled,required)
        if result is not None and (best is None or
            (-result['value'],result['fee'],result['links'])<(-best['value'],best['fee'],best['links'])):
            best=result
    if best is not None:
        # A positive branch constant cannot remain unused in a global
        # optimum: the branch with just used cores is no more expensive.
        assert best['actual_fee']==best['fee']
        best.update(sharing_cores=cores,flow_branches=1<<len(cores))
    return best


def solve_positive_openings(cur,bits,gates,weights,required=frozenset()):
    compiled=compile_handoffs(cur,bits,gates)
    if not compiled['accepted']:return dict(accepted=False,losses=compiled['losses'])
    reduced=reduce_extremes(compiled,gates,weights)
    result=solve_reduced(reduced,weights,required)
    if result is None:return dict(accepted=True,feasible=False)
    return dict(accepted=True,feasible=True,**result,opened_tiles=[gates[i] for i in result['opened']])


def transfer_pack(pack,reduced,F,counts):
    """Audit the constructive transfer with the exact original primitives."""
    data=reduced_data(reduced,F);where={u:i for i,c in enumerate(reduced['corridors']) for u in c['units']}
    signature=lambda p:(p['kind'],p['owners'],tuple(sorted(p['links'])),p['interval'],p['value'],p.get('witness'),p.get('beta'))
    candidates={signature(p) for p in primitive_certificates(*data)};certs=[]
    for p in pack['certificates']:
        q=dict(p);j=p['interval']
        if j in where:
            c=reduced['corridors'][where[j]]
            offers=[reduced['offers'][i] for i in c['offers']]
            choices=[o for o in offers if o['owner']==p['witness'] and o['gates']<=F]
            assert choices
            q['interval']=choices[0]['unit']
            counts['transferred_interval_uses']+=1
            counts['transferred_beta_forks']+=p['kind']=='fork'
        assert signature(q) in candidates
        certs.append(q)
    owners=[o for p in certs for o in p['owners']];units=[p['interval'] for p in certs if p['interval'] is not None]
    assert len(owners)==len(set(owners)) and len(units)==len(set(units))
    assert sum(p['value'] for p in certs)==pack['value']
    assert [p['links'] for p in certs]==[p['links'] for p in pack['certificates']]
    counts['source_owner_and_link_preserving_pack_transfers']+=1


def all_normalized_packs(data):
    """Independent audit enumeration of all compatible primitive packs."""
    _,A,_,_=owner_data(*data[:2]);ps=primitive_certificates(*data)
    by={a:[p for p in ps if a in p['owners']] for a in A}
    def visit(occupied,used,chosen):
        left=A-occupied
        if not left:
            yield dict(value=sum(p['value'] for p in chosen),certificates=chosen)
            return
        a=min(left)
        yield from visit(occupied|{a},used,chosen)
        for p in by[a]:
            if set(p['owners'])&occupied or p['interval'] in used:continue
            yield from visit(occupied|set(p['owners']),used|({p['interval']} if p['interval'] is not None else set()),chosen+[p])
    yield from visit(set(),set(),[])


def validate(compiled,gates,weights,counts,physical=None,all_states=True,source_checks=True,audit_all_packs=False):
    reduced=reduce_extremes(compiled,gates,weights);records={};G=frozenset(range(len(gates)))
    states=subsets(G) if all_states else [frozenset(),G]
    for F in states:
        original=(*compiled['old']['data'][:3],compiled_support(compiled,F),compiled['old']['data'][4])
        compressed=reduced_data(reduced,F)
        if physical is not None:
            cur,bits=physical;s=snapshot(cur,bits,gates,F)
            assert original[3]==s['data'][3]
            counts['physical_support_equalities']+=1
        p=optimize(*original);q=optimize(*compressed);f=fork_flow(*original)
        assert (p['value'],p['cost'])==(q['value'],q['cost'])==(f['value'],f['cost'])
        transfer_pack(f,reduced,F,counts)
        if audit_all_packs:
            for pack in all_normalized_packs(original):
                transfer_pack(pack,reduced,F,counts)
                counts['all_compatible_normalized_packs_transferred']+=1
        records[F]=dict(original=original,compressed=compressed,value=p['value'],fee=sum(weights[g] for g in F),links=p['cost'])
        counts['extreme_state_independent_primitive_comparisons']+=1
    result=solve_reduced(reduced,weights)
    assert result is not None
    if all_states:
        expected=max(records.values(),key=lambda r:(r['value'],-r['fee'],-r['links']))
        assert (result['value'],result['fee'],result['links'])==(expected['value'],expected['fee'],expected['links'])
        counts['exact_joint_optima_vs_all_gate_subsets']+=1
    F=frozenset(result['opened']);actual=(*compiled['old']['data'][:3],compiled_support(compiled,F),compiled['old']['data'][4])
    assert constrained_optimum(actual)==(result['value'],result['links'])
    if physical is not None:
        cur,bits=physical;s=snapshot(cur,bits,gates,F)
        assert s['data'][3]==actual[3]
        counts['reconstructed_optimal_physical_states']+=1
    counts['optimizer_flow_branches']+=result['flow_branches']
    counts['models_with_sharing_cores' if reduced['cores'] else 'single_flow_models']+=1
    if source_checks and all_states:
        _,A,_,_=owner_data(*compiled['old']['data'][:2])
        for P in subsets(A):
            if constrained_optimum(records[frozenset()]['original'],P) is None:continue
            protected=solve_reduced(reduced,weights,P)
            assert protected is not None and P<=set(protected['paid'])
            assert (protected['value'],protected['fee'])==(result['value'],result['fee'])
            candidates=[]
            for r in records.values():
                a=constrained_optimum(r['original'],P);b=constrained_optimum(r['compressed'],P)
                assert a==b
                if a is not None:candidates.append((a[0],r['fee'],a[1]))
            expected=max(candidates,key=lambda t:(t[0],-t[1],-t[2]))
            assert (protected['value'],protected['fee'],protected['links'])==expected
            counts['prescribed_old_source_joint_optima']+=1
    return dict(value=result['value'],fee=result['fee'],links=result['links'],opened=result['opened'],
                gates=len(gates),states=len(records),cores=sorted(reduced['cores']),flow_branches=result['flow_branches'])


def abstract_instance(rng,types='AAABM'):
    """Audit-only corridor contract, with local legacy handoffs.

    No claim that an arbitrary randomized owner network embeds in a grid.
    """
    kinds,pairs,possible=canonical(types);rng.shuffle(possible)
    links=possible[:rng.randrange(min(9,len(possible))+1)]
    W={o:set() for o in range(len(pairs))};Q=set();anchors={};axes={};gates=[];weights={};gaps=[];paths=[]
    for j in range(rng.randrange(3)):
        Q.add(j);anchors[j]=frozenset({(100+j,0)});axes[j]=True
        for o in W:
            if rng.randrange(2):W[o].add(j)
    for ci in range(rng.randrange(1,4)):
        row=2*ci;owners=[rng.choice([None]+list(W)) for _ in range(2)];units=[];gg=[];origin={}
        for col in range(rng.randrange(1,5)):
            gate=None
            if len(gates)<5 and rng.random()<.65:
                gate=len(gates);gates.append((row,2*col));weights[gate]=rng.randrange(6);gg.append(gate)
            cap=rng.randrange(3) if gate is not None else rng.randrange(1,3)
            for k in range(cap):
                j=len(Q);Q.add(j);units.append(j);anchors[j]=frozenset({(row,2*col+k),(row+1,2*col+k)});axes[j]=False;origin[j]=gate
        for j in units:
            col=min(c for r,c in anchors[j]);q=origin[j]
            reqs=[frozenset(g for g in gg if (gates[g][1]<=col if side==0 else gates[g][1]+1>=col)) for side in range(2)]
            for o,req in zip(owners,reqs):
                if o is not None:paths.append((o,j,req))
            if q is None:
                for o,req in zip(owners,reqs):
                    if o is not None and not req:W[o].add(j)
        for q in gg:
            local=[j for j in units if origin[j]==q]
            if not local:continue
            eligible={o for o,j,req in paths if j==local[0] and req<={q}}
            legacy={o for o in eligible if rng.randrange(2)}
            for o in legacy:W[o].update(local)
        gaps.append(dict(left=owners[0],right=owners[1],units=units,gates=gg))
    olddata=(kinds,pairs,links,W,Q)
    compiled=dict(accepted=True,old=dict(data=olddata),full=dict(anchors=anchors,axes=axes),gaps=gaps,paths=paths)
    return compiled,gates,weights


def sharing_contract(types,endpoints,links,profiles,one=False):
    """Explicit abstract controls with any number of competing fee cores."""
    kinds,pairs,_=canonical(types);W={o:set() for o in range(len(pairs))}
    Q=set();anchors={};axes={};gates=[];weights={};gaps=[];paths=[]
    for ci,((L,R),(lf,qf,rf)) in enumerate(zip(endpoints,profiles)):
        row=2*ci;gg=[];units=[]
        for col,fee in zip((0,2,4),(lf,qf,rf)):
            g=len(gates);gates.append((row,col));gg.append(g);weights[g]=fee
        for k in range(1 if one else 2):
            j=len(Q);Q.add(j);units.append(j);axes[j]=False
            anchors[j]=frozenset({(row,2+k),(row+1,2+k)})
            if L is not None:paths.append((L,j,frozenset(gg[:2])))
            if R is not None:paths.append((R,j,frozenset(gg[1:])))
        gaps.append(dict(left=L,right=R,units=units,gates=gg))
    olddata=(kinds,pairs,links,W,Q)
    c=dict(accepted=True,old=dict(data=olddata),full=dict(anchors=anchors,axes=axes),gaps=gaps,paths=paths)
    return c,gates,weights


def paid_legacy_contract(coincident=False):
    """Nonvacuous legacy controls, including a right-only singleton handoff."""
    kinds,pairs,_=canonical('AAB' if coincident else 'AAAB')
    beta=2 if coincident else 3
    links=[(0,4),(2,5)] if coincident else [(2,6),(4,7)]
    W={o:set() for o in range(len(pairs))}
    if coincident:
        gates=[(0,0),(0,4),(0,6)];weights={0:3,1:4,2:5};units=[0,1,2]
        anchors={j:frozenset({(0,c),(1,c)}) for j,c in enumerate((2,6,7))}
        W[beta]={1,2};endpoints=(beta,beta)
    else:
        gates=[(0,2)];weights={0:5};units=[0,1]
        anchors={j:frozenset({(0,2+j),(1,2+j)}) for j in units}
        W[0]={0,1};endpoints=(0,beta)
    paths=[]
    for j in units:
        col=min(c for r,c in anchors[j])
        for side,o in enumerate(endpoints):
            req=frozenset(i for i,g in enumerate(gates) if (g[1]<=col if side==0 else g[1]+1>=col))
            paths.append((o,j,req))
    old=(kinds,pairs,links,W,set(units))
    c=dict(accepted=True,old=dict(data=old),full=dict(anchors=anchors,axes={j:False for j in units}),
           paths=paths,gaps=[dict(left=endpoints[0],right=endpoints[1],units=units,gates=list(range(len(gates))))])
    return c,gates,weights


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();examples={};rng=random.Random(2026102641)
    # Small feasible legacy-support controls; only first gate is variable.
    for one in (False,True):
        cur,bits,gates=endpoint_trap(one);gates=gates[:1];weights={0:3}
        c=compile_handoffs(cur,bits,gates);assert c['accepted']
        examples['legacy_'+str(one)]=validate(c,gates,weights,counts,(cur,bits))
    # Frozen cap-one and cap-two pivot corridors, including arbitrary many
    # zero-capacity prefix cuts and zero-cost shared pivots.
    for nleft,nright in ((1,1),(2,2),(2,3),(16,17)):
        for one in (False,True):
            cur,bits,ranks,left,right,q=frozen_board(nleft,nright,one);central=(2,16+2*q)
            bits[central]=True;gates=left+right+[central]
            weights={i:1+(i%3) for i in range(len(gates))}
            c=compile_handoffs(cur,bits,gates);assert c['accepted']
            for zero in (False,True):
                ww=dict(weights)
                if zero:ww[len(gates)-1]=0
                row=validate(c,gates,ww,counts,(cur,bits),all_states=len(gates)<=8)
                assert len(row['cores'])==int(not one and not zero)
                examples[f'frozen_{nleft}_{nright}_one{one}_zero{zero}']=row
            counts['strict_freeze_events']+=len(check_rank_certificate(cur,ranks))
            assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
    cur,bits,ranks,gates=bundle_fixture();c=compile_handoffs(cur,bits,gates);assert c['accepted']
    for cost in (0,3,5,7):
        weights={0:cost,1:3,2:3};row=validate(c,gates,weights,counts,(cur,bits))
        assert (row['value'],row['fee'],row['links'])==(4,min(cost,6),2)
        examples['frozen_bundle_cost'+str(cost)]=row
    counts['strict_freeze_events']+=len(check_rank_certificate(cur,ranks))
    # Existing physical sharing adapter refutes charging the central fee
    # separately on its two extreme support arcs.
    weights={0:5,1:3,2:3};reduced=reduce_extremes(c,gates,weights)
    wrong=flow_branch(reduced,weights,frozenset(),split_shared=True)
    right=solve_reduced(reduced,weights)
    assert wrong['value']==right['value']==4 and wrong['fee']==6 and right['fee']==5
    examples['double_fee_shortcut']=dict(correct_fee=right['fee'],wrong_fee=wrong['fee'],
        correct_opened=right['opened'],wrong_opened=wrong['opened'],fully_frozen=True)
    # Two physical sharing pivots, preserving both modules' freeze schedule.
    shift=lambda v:(v[0]+16,v[1])
    stacked=(32,cur[1],cur[2]|set(map(shift,cur[2])),cur[3]+[tuple(map(shift,e)) for e in cur[3]])
    sb=dict(bits);sb.update({shift(g):v for g,v in bits.items()})
    sg=gates+[shift(g) for g in gates]
    sc=compile_handoffs(stacked,sb,sg);assert sc['accepted']
    ww={i:(5 if i%3==0 else 3) for i in range(6)}
    row=validate(sc,sg,ww,counts,(stacked,sb),source_checks=False)
    assert (row['value'],row['fee'],row['links'],row['flow_branches'])==(8,10,4,4)
    examples['two_frozen_sharing_pivots']=row
    sr=[layer+[shift(v) for v in layer] for layer in ranks]
    counts['strict_freeze_events']+=len(check_rank_certificate(stacked,sr))
    assert frozen_certificate(stacked)[0]=={v for e in stacked[3] for v in e}
    for name,types,endpoints,links,fees,one in [
        ('beta_mixed_competing_two_cores','AAAABM',[(4,5),(2,3)],[(0,8),(2,9),(4,10),(6,10)],[(1,3,2),(2,4,1)],False),
        ('same_beta_two_ends','AAB',[(2,2)],[(0,4),(2,5)],[(1,5,3)],False),
        ('one_output_two_ends','AA',[(0,1)],[],[(1,5,3)],True),
        ('three_competing_cores','AAAAMM',[(0,1),(2,3),(4,5)],[(0,8),(2,8),(4,10),(6,10)],[(1,4,2),(2,3,1),(1,5,1)],False),
    ]:
        ac,ag,aw=sharing_contract(types,endpoints,links,fees,one)
        examples[name]=validate(ac,ag,aw,counts,audit_all_packs=len(ag)<=6)
        if name in ('same_beta_two_ends','one_output_two_ends'):assert not examples[name]['cores']
    for same in (False,True):
        ac,ag,aw=paid_legacy_contract(same)
        row=validate(ac,ag,aw,counts,audit_all_packs=True)
        assert not row['cores']
        assert (row['value'],row['fee'],row['links'])==((2,0,2) if same else (3,5,2))
        examples['paid_legacy_coincident'+str(same)]=row
    for index in range(100):
        types='AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,5)))
        c,gates,weights=abstract_instance(rng,types)
        validate(c,gates,weights,counts,audit_all_packs=index<12)
    # Independent sparse physical boards: recognition may reject, and no
    # optimization conclusion is attached to those rejected configurations.
    for _ in range(40):
        raw=random_board(8,8,rng)
        cur=(*raw[:2],{v for v in raw[2] if rng.random()<.35},[e for e in raw[3] if rng.random()<.3])
        P={v for e in cur[3] for v in e}
        bits={(r,c):bool(rng.randrange(2)) for r in range(0,8,2) for c in range(0,8,2)}
        candidates=[g for g in bits if not tile_cells(g)&P];rng.shuffle(candidates);gates=candidates[:4]
        for g in gates:bits[g]=True
        c=compile_handoffs(cur,bits,gates)
        if c['accepted']:
            validate(c,gates,{i:rng.randrange(5) for i in range(len(gates))},counts,(cur,bits))
            counts['accepted_random_physical_boards']+=1
        else:counts['rejected_random_physical_boards']+=1
    # The actual optimizer may enumerate its h core bits, but neither all
    # physical gate subsets nor any primitive packing is needed by the API.
    def forbidden(*a,**kw):raise AssertionError('API must not call audit enumeration or packing routines')
    for one in (False,True):
        cur,bits,ranks,left,right,q=frozen_board(16,17,one);g=(2,16+2*q);bits[g]=True;gates=left+right+[g]
        weights={i:1 for i in range(len(gates))}
        with patch(__name__+'.subsets',forbidden),patch(__name__+'.optimize',forbidden),patch(__name__+'.constrained_optimum',forbidden),patch(__name__+'.fork_flow',forbidden),patch(__name__+'.primitive_certificates',forbidden):
            result=solve_positive_openings(cur,bits,gates,weights)
            assert result['accepted'] and result['flow_branches']==(1 if one else 2) and len(gates)==34
            counts['enumeration_and_pack_disabled_API_checks']+=1
        examples['large_actual_API_one'+str(one)]=dict(gates=len(gates),value=result['value'],fee=result['fee'],links=result['links'],
                                         sharing_cores=result['sharing_cores'],flow_branches=result['flow_branches'])
        if one:
            c=compile_handoffs(cur,bits,gates);_,A,_,_=owner_data(*c['old']['data'][:2])
            assert solve_positive_openings(cur,bits,gates,weights,A)==dict(accepted=True,feasible=False)
            counts['infeasible_prescribed_source_API_checks']+=1
    cur,bits,gates=endpoint_trap()
    with patch(__name__+'.subsets',forbidden),patch(__name__+'.optimize',forbidden),patch(__name__+'.constrained_optimum',forbidden),patch(__name__+'.fork_flow',forbidden):
        assert not solve_positive_openings(cur,bits,gates,{0:1,1:1})['accepted']
        counts['enumeration_and_pack_disabled_API_checks']+=1
    result=dict(status='PASS',counts=dict(counts),examples=examples,
        scope='Written general positive extreme theorem and shared-fee core classification; exact 2^h flow optimizer for recognized uniform all-capacity physical pivots. Enumeration only in independent audits. No universal 5/6 or polynomial-in-h claim.')
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(counts,sort_keys=True))


if __name__=='__main__':main()
