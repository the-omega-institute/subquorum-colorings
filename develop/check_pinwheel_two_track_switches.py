"""Exact joint direction optimization for disjoint two-mixed pinwheel tiles.

General geometry and flow equivalence: PINWHEEL_TWO_TRACK_SWITCHES.md.
No solver dependency; physical original resources are keyed by their cells.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import occupied_degrees
from check_crossing_matching_ports import rectangle, strand_parts, band_resources, model_for_components
from check_four_outward_alpha_localization import fixture, cells
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_owned_donors import capacity_cross
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import brute, evaluate, canonical
from rotor_networks import chain

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def model(cur,roots=(),flips=frozenset()):
    R,C,T,M=cur;P={v for e in M for v in e};regions=[]
    for r in range(0,R,2):
        row=sorted(c for a,c in roots if a==r);last=0
        for c in row:
            if last<c:regions.append(rectangle(r,r+2,last,c))
            regions.append(rectangle(r,r+2,c,c+2,(r,c) in flips));last=c+2
        if last<C:regions.append(rectangle(r,r+2,last,C))
    bands=[b for x in regions for b in x['bands']]
    parts,partner=strand_parts(P,T,M,bands)
    Q,gaps,_=band_resources(P,T,bands)
    raw,closed=model_for_components(P,T,bands,parts,Q,gaps)
    keys={j:tuple(sorted(v for pair in bands[j[0]][j[1]:j[2]+1] for v in pair)) for j in Q}
    resources=set(keys.values());assert len(resources)==len(Q)
    access={v:set() for v in P}
    for b,first,after,units in gaps:
        for c in (first-1,after):
            if 0<=c<len(bands[b]):
                for v in bands[b][c]:
                    if v in P:access[v]|={keys[j] for j in units}
    support={o:{keys[j] for j in w} for o,w in raw[3].items()}
    assert all(support[o]==set().union(*(access[v] for v in x['body'])) for o,x in enumerate(closed))
    return (raw[0],raw[1],raw[2],support,resources),closed,access,partner


def pinwheels(cur,totals):
    R,C,T,M=cur;P={v for e in M for v in e};mate={v:w for e in M for v,w in (e,e[::-1])}
    assert set(occupied_degrees(cur).values())=={3}
    base,closed,access,partner=model(cur);own,A,B,Z=owner_data(*base[:2])
    body={v:o for o,x in enumerate(closed) for v in x['body']};roots=[];switches=[];seen=set()
    for r,c in itertools.product(range(0,R,2),range(0,C,2)):
        Q=cells((r,c))
        if not Q<=P or any(mate[v] in Q for v in Q):continue
        ds=[(mate[v][0]-v[0],mate[v][1]-v[1]) for v in [(r,c),(r,c+1),(r+1,c),(r+1,c+1)]]
        assert ds in [[(-1,0),(0,1),(0,-1),(1,0)],[(0,-1),(-1,0),(1,0),(0,1)]]
        endpoints=[];owners=[];entry=[]
        for col in (c,c+1):
            wire=[(r,col),(r+1,col)]
            x=next(v for v in wire if mate[v][0]==v[0]);bp=mate[x]
            assert partner[bp] not in T|P and base[0][bp]=='BP'
            endpoints.append(bp);owners.append(body[x]);entry.append((x,bp))
        assert owners[0]!=owners[1]
        totals['pinwheel_tiles']+=1
        if not all(o in Z for o in owners):continue
        assert not set(owners)&seen;seen|=set(owners)
        roots.append((r,c));tracks=[]
        for o,(x,bp) in zip(owners,entry):
            stub={x,bp};tail=closed[o]['body']-stub
            assert not any(access[v] for v in Q)
            tracks.append(dict(owner=o,bp=bp,tp=next(v for v in base[1][o] if base[0][v]=='TP'),
                stub=stub,tail=tail,stub_support=set().union(*(access[v] for v in stub)),
                tail_support=set().union(*(access[v] for v in tail))))
        switches.append(dict(tile=(r,c),tracks=tracks))
    totals['two_mixed_switches']+=len(switches)
    # Region cuts around the roots preserve the entire original model exactly.
    split,_,_,_=model(cur,roots)
    assert split==base
    return base,roots,switches


def min_cost_flow(arcs,source,sink):
    edges=[];adj=defaultdict(list)
    for u,v,cap,cost,tag in arcs:
        i=len(edges);edges += [dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
                              dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)]
        adj[u].append(i);adj[v].append(i+1)
    nodes=set(adj)|{source,sink};value=cost=0
    while True:
        distance={source:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in distance and (e['v'] not in distance or distance[e['v']]>distance[e['u']]+e['cost']):
                    distance[e['v']]=distance[e['u']]+e['cost'];parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in distance:break
        v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v);i=parent[v];edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1;cost+=distance[sink]
    used=[(e['tag'],e['initial']-e['cap']) for e in edges[::2] if e['initial']>e['cap']]
    return value,cost,used


def switch_flow(data,switches,available):
    kinds,pairs,links,W,Q=data;own,A,B,Z=owner_data(kinds,pairs)
    assert available<=Q
    selected={t['owner'] for s in switches for t in s['tracks']};source=('source',);sink=('sink',);arcs=[]
    def add(u,v,cap=1,cost=0,tag=None):arcs.append((u,v,cap,cost,tag))
    exit=lambda o:('alpha',o) if o in A else ('out',o) if o in Z else ('beta',o)
    for a in sorted(A):add(source,exit(a),tag=('source',a))
    for m in sorted(Z-selected):add(('in',m),exit(m),tag=('mixed',m))
    for b in sorted(B):
        for tip in pairs[b]:add(('tip',tip),exit(b),tag=('tip',tip))
        add(exit(b),sink,tag=('beta',b))
    for q in sorted(available):add(('interval',q),sink,tag=('interval',q))
    for k,s in enumerate(switches):
        for t in s['tracks']:
            o=t['owner'];add(('in',o),('stub',o),tag=('entry',o));add(('tail',o),exit(o),tag=('output',o))
            for q in sorted(t['stub_support']&available):add(('stub',o),('interval',q),len(A)+1,tag=('stub_access',o,q))
            for q in sorted(t['tail_support']&available):add(exit(o),('interval',q),len(A)+1,tag=('tail_access',o,q))
        for i,j in itertools.product(range(2),repeat=2):
            a=s['tracks'][i]['owner'];b=s['tracks'][j]['owner']
            add(('stub',a),('tail',b),tag=('switch',k,i,j))
    # Self links at a switched owner MUST stay: a flip may make them nonself.
    for a,b in sorted(set(links)):
        if own[a]==own[b] and own[a] not in selected:continue
        target=('tip',b) if own[b] in B else ('in',own[b])
        add(exit(own[a]),target,len(A)+1,1,('link',a,b))
    for o in sorted(set(W)-selected):
        for q in sorted(W[o]&available):add(exit(o),('interval',q),len(A)+1,tag=('access',o,q))
    value,cost,used=min_cost_flow(arcs,source,sink)
    flips=set();chosen=[]
    for k,s in enumerate(switches):
        cross=[tag[2:] for tag,n in used if tag and tag[:2]==('switch',k) for _ in range(n)]
        assert len(cross)<=2 and len({i for i,j in cross})==len({j for i,j in cross})==len(cross)
        parity={i^j for i,j in cross};assert len(parity)<=1
        if parity=={1}:flips.add(s['tile'])
    for tag,n in used:
        if tag and tag[0]=='link':assert n==1;chosen.append(tag[1:])
    assert len(chosen)==cost and len({v for e in chosen for v in e})==2*len(chosen)
    return dict(value=value,cost=cost,flips=flips,links=chosen)


def restrict(data,available):
    return (*data[:3],{o:w&available for o,w in data[3].items()},available)


def reachable_owners(data):
    own,A,B,Z=owner_data(*data[:2]);seen=set(A);todo=list(A)
    while todo:
        o=todo.pop()
        for a,b in data[2]:
            if own[a]==o and own[b] not in seen:seen.add(own[b]);todo.append(own[b])
    return seen,own,A


def stack(q):
    base,j=fixture();T=set();M=[];schedule=[]
    for k in range(q):
        move=lambda v:(v[0]+16*k,v[1])
        T|={move(v) for v in base[2]};M += [tuple(map(move,e)) for e in base[3]]
        schedule += [[move(v) for v in wave] for wave in j['frozen_schedule']]
    return (16*q-2,14,T,M),schedule


def compare(cur,totals,rng,pools=8,terminal=False):
    direct_check(*cur);P={v for e in cur[3] for v in e};assert frozen_certificate(cur)[0]==P
    totals['physical_models']+=1
    data,roots,switches=pinwheels(cur,totals)
    variants=[]
    for bits in itertools.product((False,True),repeat=len(roots)):
        flips={r for r,b in zip(roots,bits) if b};d,closed,access,_=model(cur,roots,flips)
        assert d[0]==data[0] and set(d[2])==set(data[2]) and d[4]==data[4]
        # Check exact bodies and support decomposition, not only optimum values.
        by_bp={bp:(o,x) for o,x in enumerate(closed) for kind,bp in x['ends'] if kind=='B'}
        for s in switches:
            for i,t in enumerate(s['tracks']):
                other=s['tracks'][i^int(s['tile'] in flips)]
                o,x=by_bp[t['bp']]
                assert x['body']==t['stub']|other['tail']
                assert d[3][o]==t['stub_support']|other['tail_support']
        variants.append((flips,d))
        totals['physical_orientation_assignments']+=1
    available_sets=[set(),data[4]]+[{q for q in sorted(data[4]) if rng.getrandbits(1)} for _ in range(pools)]
    for available in available_sets:
        answer=switch_flow(data,switches,available);values=[]
        for flips,d in variants:
            f=fork_flow(*restrict(d,available));values.append((f['value'],f['cost']))
            if terminal:
                independent,count=brute(*restrict(d,available));assert independent==(f['value'],f['cost'])
                totals['independent_terminal_matchings']+=count
        expected=max(values,key=lambda x:(x[0],-x[1]))
        assert expected==(answer['value'],answer['cost'])
        assert answer['value']<=values[0][0]+len(roots)
        for (flips,d),(value,cost) in zip(variants,values):
            assert abs(value-values[0][0])<=len(flips)
        lifted=next(d for flips,d in variants if flips==answer['flips'])
        check=evaluate(*lifted[:2],answer['links'],{o:w&available for o,w in lifted[3].items()},available)
        assert check['value']==answer['value']
        totals['joint_resource_pool_comparisons']+=1;totals['selected_physical_link_lifts']+=len(answer['links'])
    return data,roots,switches


def abstract_controls(rng,totals):
    # A previously self link can be essential after the transposition.
    kinds,pairs,_=canonical('AMM')
    switch=dict(tile=(0,0),tracks=[dict(owner=1,bp=2,tp=3,stub_support=set(),tail_support=set()),
        dict(owner=2,bp=4,tp=5,stub_support={0},tail_support=set())])
    data=(kinds,pairs,[(0,2),(5,4)],{0:set(),1:set(),2:{0}},{0})
    assert fork_flow(*data)['value']==0
    fixed=switch_flow(data,[switch],{0})
    assert (fixed['value'],fixed['cost'])==(1,2) and (5,4) in fixed['links']
    assert switch_flow((kinds,pairs,[(0,2)],data[3],data[4]),[switch],{0})['value']==0
    lifted=(kinds,[(0,1),(2,5),(4,3)],data[2],data[3],data[4])
    assert evaluate(*lifted[:2],fixed['links'],*lifted[3:])['value']==1
    totals['essential_old_self_link_controls']+=1
    for run in range(320):
        q=1+run%3;kinds,pairs,possible=canonical('AAAA'+'MM'*q+'MB')
        own,A,B,Z=owner_data(kinds,pairs);mixed=sorted(Z);switches=[];Q=set(range(4))
        W={o:{j for j in Q if rng.randrange(3)==0} for o in range(len(pairs))}
        for k in range(q):
            tracks=[]
            for o in mixed[2*k:2*k+2]:
                stub={j for j in W[o] if rng.getrandbits(1)}
                tail=W[o]-stub
                # Some original units can border both pieces; keep their identity.
                if run%7==0:stub|=tail
                tracks.append(dict(owner=o,bp=next(v for v in pairs[o] if kinds[v]=='BP'),
                    tp=next(v for v in pairs[o] if kinds[v]=='TP'),stub_support=stub,tail_support=tail))
            switches.append(dict(tile=(k,0),tracks=tracks))
        rng.shuffle(possible);links=possible[:rng.randrange(min(16,len(possible))+1)]
        available={j for j in Q if rng.getrandbits(1)};data=(kinds,pairs,links,W,Q)
        answer=switch_flow(data,switches,available);values=[];lift=None
        for bits in itertools.product((False,True),repeat=q):
            ps=list(pairs);support=dict(W);flips=set()
            for s,flip in zip(switches,bits):
                if flip:flips.add(s['tile'])
                for i,t in enumerate(s['tracks']):
                    other=s['tracks'][i^int(flip)];o=t['owner']
                    ps[o]=(t['bp'],other['tp']);support[o]=t['stub_support']|other['tail_support']
            variant=(kinds,ps,links,support,Q)
            result=fork_flow(*restrict(variant,available));values.append((result['value'],result['cost']))
            assert abs(result['value']-values[0][0])<=len(flips)
            if flips==answer['flips']:lift=variant
            totals['abstract_orientation_comparisons']+=1
        assert max(values,key=lambda x:(x[0],-x[1]))==(answer['value'],answer['cost'])
        assert answer['value']<=values[0][0]+q
        assert evaluate(*lift[:2],answer['links'],{o:w&available for o,w in lift[3].items()},available)['value']==answer['value']
        totals['abstract_switch_networks']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();rng=random.Random(20261026);family=[]
    abstract_controls(rng,totals)
    for q in (1,2,3,4):
        cur,schedule=stack(q);totals['strict_rank_events']+=len(check_rank_certificate(cur,schedule))
        data,roots,switches=compare(cur,totals,rng,12,terminal=q==1)
        right={((16*k+6,4),(16*k+7,4)) for k in range(q)}
        left={((16*k+2,5),(16*k+3,5)) for k in range(q)}
        assert right|left<=data[4] and len(roots)==q
        before=fork_flow(*restrict(data,right));after=switch_flow(data,switches,right)
        lost=fork_flow(*restrict(model(cur,roots,set(roots))[0],left))
        assert (before['value'],before['cost'])==(0,0)
        assert (after['value'],after['cost'])==(q,q) and after['flips']==set(roots)
        assert (lost['value'],lost['cost'])==(0,0)
        full=fork_flow(*data);assert (full['value'],full['cost'])==(q,0)
        for bits in itertools.product((False,True),repeat=q):
            chosen={root for root,b in zip(roots,bits) if b}
            d=model(cur,roots,chosen)[0]
            actual=fork_flow(*restrict(d,right))
            assert (actual['value'],actual['cost'])==(len(chosen),len(chosen))
            totals['all_subsets_sharp_family_checks']+=1
        if q==1:
            for flipped in (False,True):
                d=model(cur,roots,set(roots) if flipped else set())[0]
                reach,own,A=reachable_owners(d)
                assert len(A)==1 and reach==A|{own[5,3]}
                assert ((5,2),(5,3)) in d[2]
                assert bool(d[3][own[5,3]]&right)==flipped
                assert all(not d[3][a]&right for a in A)
        family.append(dict(q=q,shape=cur[:2],endpoints=len(cur[3])*2,selected=len(cur[2]),roots=roots,
            right_available=sorted(right),before=(0,0),after=(q,q),flips=sorted(after['flips']),
            left_available=sorted(left),all_flipped_left_payment=0,full_pool=(q,0)))
    for q in (1,2,3):compare(chain(q)[0],totals,rng,4)
    for q in (1,2,3):compare(capacity_cross(q)[0],totals,rng,4)
    cur,_=fixture()
    for sym in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,*sym);compare((*shape,T,M),totals,rng,4)
    report=dict(status='PASS',totals=dict(totals),family=family,
        theorem='Written: exact-degree-three bundle-terminal four-outward tiles are pinwheels; each original wire has a unique horizontal-M BP; distinct wires/owners; mixed owner meets at most one tile. For any collection with both owners mixed, maximizing compensation and then minimizing physical link cost over all tile orientations equals one two-by-two-switch integral flow, for any available original resource subset. Every flow yields actual tile orientations. Gain is at most one per flipped root; all-q separated physical copies attain it on a restricted original pool.',
        limitations='Uniform background outside selected nonadjacent root tiles; two original owners must both be mixed. No beta-track extension asserted. Restricted-pool gain q is not full-pool deficit repair: witness full pool already pays q at cost0. General donor coverage and universal5/6 remain open.')
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',**totals)))


if __name__=='__main__':main()
