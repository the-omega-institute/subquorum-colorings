"""Joint pinwheel direction optimization with fixed beta-core identities.

See PINWHEEL_BETA_CORE_SWITCHES.md for the general proof. No discovery solver.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import occupied_degrees
from check_compensation_flow_normal_form import owner_data
from check_four_outward_alpha_localization import cells,fixture
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_pinwheel_two_track_switches import model,min_cost_flow,restrict,stack
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import evaluate,brute,canonical
from rotor_networks import chain

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def layout(cur,totals,selected=None):
    R,C,T,M=cur;P={v for e in M for v in e};mate={v:w for e in M for v,w in (e,e[::-1])}
    assert set(occupied_degrees(cur).values())=={3}
    data,closed,access,partner=model(cur);own,A,B,Z=owner_data(*data[:2])
    body={v:o for o,x in enumerate(closed) for v in x['body']};switches=[];stubs=defaultdict(set)
    all_roots=[]
    for r,c in itertools.product(range(0,R,2),range(0,C,2)):
        Q=cells((r,c))
        if not Q<=P or any(mate[v] in Q for v in Q):continue
        all_roots.append((r,c))
        if selected is not None and (r,c) not in selected:continue
        tracks=[]
        for col in (c,c+1):
            wire=[(r,col),(r+1,col)]
            horizontal=[v for v in wire if mate[v][0]==v[0]];assert len(horizontal)==1
            x=horizontal[0];bp=mate[x];o=body[x];stub={x,bp}
            assert data[0][bp]=='BP' and partner[bp] not in T|P
            assert o in B|Z and not any(access[v] for v in Q)
            tracks.append(dict(owner=o,bp=bp,body=stub,support=set().union(*(access[v] for v in stub))))
            stubs[o]|=stub
        assert tracks[0]['owner']!=tracks[1]['owner']
        switches.append(dict(tile=(r,c),tracks=tracks))
    roots=[s['tile'] for s in switches]
    cores={o:dict(body=x['body']-stubs[o],support=set().union(*(access[v] for v in x['body']-stubs[o])))
           for o,x in enumerate(closed)}
    bp_seen=[t['bp'] for s in switches for t in s['tracks']]
    assert len(bp_seen)==len(set(bp_seen))
    ports=Counter(t['owner'] for s in switches for t in s['tracks'])
    for o in cores:
        assert cores[o]['body']
        assert data[3][o]==cores[o]['support']|set().union(set(),*(t['support'] for s in switches for t in s['tracks'] if t['owner']==o))
        assert ports[o]<= (2 if o in B else 1 if o in Z else 0)
    assert model(cur,roots)[0]==data
    totals['selected_tiles']+=len(roots);totals['beta_cores_with_two_root_ports']+=sum(ports[b]==2 for b in B)
    totals['beta_cores_with_one_root_port']+=sum(ports[b]==1 for b in B)
    return data,roots,switches,cores


def core_flow(data,switches,cores,available,beta_units=1):
    kinds,pairs,links,W,Q=data;own,A,B,Z=owner_data(kinds,pairs);assert available<=Q
    forced={t['bp']:t for s in switches for t in s['tracks']}
    ports=Counter(t['owner'] for s in switches for t in s['tracks'])
    source=('source',);sink=('sink',);arcs=[]
    def add(u,v,cap=1,cost=0,tag=None):arcs.append((u,v,cap,cost,tag))
    exit=lambda o:('alpha',o) if o in A else ('out',o) if o in Z else ('beta',o)
    for a in sorted(A):add(source,exit(a),tag=('source',a))
    for m in sorted(Z):
        if not ports[m]:add(('in',m),exit(m),tag=('mixed',m))
    for b in sorted(B):
        for bp in pairs[b]:
            if bp not in forced:add(('tip',bp),exit(b),tag=('tip',bp))
        # beta_units=2 is an intentionally wrong diagnostic, never the theorem.
        add(exit(b),sink,beta_units,tag=('whole_beta_core',b))
    for q in sorted(available):add(('interval',q),sink,tag=('interval',q))
    for o in sorted(cores):
        for q in sorted(cores[o]['support']&available):add(exit(o),('interval',q),len(A)+1,tag=('core_access',o,q))
    for k,s in enumerate(switches):
        for i,t in enumerate(s['tracks']):
            bp=t['bp'];add(('entry',bp),('stub',bp),tag=('forced_BP',bp))
            for q in sorted(t['support']&available):add(('stub',bp),('interval',q),len(A)+1,tag=('stub_access',bp,q))
            add(('port',k,i),exit(t['owner']),tag=('core_port',k,i,t['owner']))
        for i,j in itertools.product(range(2),repeat=2):
            add(('stub',s['tracks'][i]['bp']),('port',k,j),tag=('switch',k,i,j))
    for tp,bp in sorted(set(links)):
        target=(('entry',bp) if bp in forced else ('tip',bp) if own[bp] in B else ('in',own[bp]))
        add(exit(own[tp]),target,len(A)+1,1,('link',tp,bp))
    value,cost,used=min_cost_flow(arcs,source,sink);flips=set()
    # Reconstruct residual reachability independently from the tagged flow.
    usage={tag:n for tag,n in used};assert len({tag for u,v,cap,c,tag in arcs})==len(arcs)
    residual=defaultdict(list)
    for u,v,cap,c,tag in arcs:
        n=usage.get(tag,0)
        if n<cap:residual[u].append(v)
        if n:residual[v].append(u)
    source_side={source};todo=[source]
    while todo:
        u=todo.pop()
        for v in residual[u]:
            if v not in source_side:source_side.add(v);todo.append(v)
    assert sink not in source_side
    cut=[(tag,cap) for u,v,cap,c,tag in arcs if u in source_side and v not in source_side]
    assert sum(cap for tag,cap in cut)==value
    separator={tag for tag,cap in cut if tag[0]!='source'}
    forward=defaultdict(list)
    for u,v,cap,c,tag in arcs:
        if tag not in separator:forward[u].append(v)
    blocked=[]
    for a in A:
        seen={exit(a)};todo=[exit(a)]
        while todo:
            u=todo.pop()
            for v in forward[u]:
                if v not in seen:seen.add(v);todo.append(v)
        if sink not in seen:blocked.append(a)
    if beta_units==1:
        assert all(cap==1 for tag,cap in cut)
        assert len(A)-value==len(blocked)-len(separator)
    for k,s in enumerate(switches):
        cross=[tag[2:] for tag,n in used if tag and tag[:2]==('switch',k) for _ in range(n)]
        assert len({i for i,j in cross})==len({j for i,j in cross})==len(cross)<=2
        parity={i^j for i,j in cross};assert len(parity)<=1
        if parity=={1}:flips.add(s['tile'])
    chosen=[]
    for tag,n in used:
        if tag and tag[0]=='link':assert n==1;chosen.append(tag[1:])
    assert len(chosen)==cost and len({v for e in chosen for v in e})==2*len(chosen)
    return dict(value=value,cost=cost,flips=flips,links=chosen,used=used,
        separator=sorted(separator),blocked_sources=sorted(blocked),deficit=len(A)-value)


def compare(cur,totals,rng,pools=5,terminal=False,selected=None):
    direct_check(*cur);P={v for e in cur[3] for v in e};frozen,layers=frozen_certificate(cur);assert frozen==P
    totals['independent_rank_events']+=len(check_rank_certificate(cur,
        [[w['endpoint'] for w in wave] for wave in layers]))
    totals['physical_models']+=1
    data,roots,switches,cores=layout(cur,totals,selected)
    variants=[]
    for bits in itertools.product((False,True),repeat=len(roots)):
        flips={r for r,b in zip(roots,bits) if b};d,closed,access,_=model(cur,roots,flips)
        assert d[0]==data[0] and set(d[2])==set(data[2]) and d[4]==data[4]
        expected={o:set(c['body']) for o,c in cores.items()};expectedW={o:set(c['support']) for o,c in cores.items()}
        for s in switches:
            for i,stub in enumerate(s['tracks']):
                o=s['tracks'][i^int(s['tile'] in flips)]['owner']
                expected[o]|=stub['body'];expectedW[o]|=stub['support']
        body_owner={v:o for o,x in enumerate(closed) for v in x['body']}
        actual=[]
        for o,c in cores.items():
            a=body_owner[min(c['body'])];actual.append(a)
            assert closed[a]['body']==expected[o] and d[3][a]==expectedW[o]
        assert len(actual)==len(set(actual))==len(closed)
        variants.append((flips,d));totals['physical_orientation_assignments']+=1
    sets=[set(),data[4]]+[{j for j in sorted(data[4]) if rng.getrandbits(1)} for _ in range(pools)]
    for available in sets:
        result=core_flow(data,switches,cores,available);values=[]
        for flips,d in variants:
            f=fork_flow(*restrict(d,available));values.append((f['value'],f['cost']))
            assert abs(values[-1][0]-values[0][0])<=len(flips)
            if terminal:
                expected,count=brute(*restrict(d,available));assert expected==values[-1]
                totals['independent_terminal_matchings']+=count
        assert max(values,key=lambda x:(x[0],-x[1]))==(result['value'],result['cost'])
        assert result['value']<=values[0][0]+len(roots)
        lift=next(d for f,d in variants if f==result['flips'])
        assert evaluate(*lift[:2],result['links'],{o:w&available for o,w in lift[3].items()},available)['value']==result['value']
        totals['joint_pool_comparisons']+=1;totals['selected_physical_link_lifts']+=len(result['links'])
        totals['positive_direction_optimized_deficits']+=result['deficit']>0
    return data,roots,switches,cores


def abstract_controls(totals,rng):
    # The beta fork's one interval is on a forced BP stub, not its core.
    kinds,pairs,_=canonical('AABMM')
    switches=[dict(tile=(0,0),tracks=[dict(owner=2,bp=4,support={0}),dict(owner=3,bp=6,support=set())]),
              dict(tile=(1,0),tracks=[dict(owner=2,bp=5,support=set()),dict(owner=4,bp=8,support=set())])]
    cores={o:dict(support=set()) for o in range(5)}
    data=(kinds,pairs,[(0,4),(2,5)],{0:set(),1:set(),2:{0},3:set(),4:set()},{0})
    result=core_flow(data,switches,cores,{0})
    assert (result['value'],result['cost'])==(2,2)
    assert fork_flow(*data)['value']==2
    without=[dict(tile=s['tile'],tracks=[dict(t,support=set()) for t in s['tracks']]) for s in switches]
    assert core_flow(data,without,cores,{0})['value']==1
    totals['essential_beta_stub_support_controls']+=1
    for run in range(360):
        q=1+run%3;kindstr='AAAA'+'B'*q+'M'*(q+1)
        kinds,pairs,possible=canonical(kindstr);own,A,B,Z=owner_data(kinds,pairs)
        bps=[v for v,k in kinds.items() if k=='BP'];rng.shuffle(bps)
        for _ in range(1000):
            rng.shuffle(bps);chosen=bps[:2*q]
            if all(own[chosen[2*k]]!=own[chosen[2*k+1]] for k in range(q)):break
        else:raise AssertionError('Failed to construct distinct-owner roots')
        switches=[];cores={o:dict(support=set()) for o in range(len(pairs))};Q=set(range(4))
        for k in range(q):
            tracks=[dict(owner=own[bp],bp=bp,support={j for j in Q if rng.randrange(3)==0}) for bp in chosen[2*k:2*k+2]]
            switches.append(dict(tile=(k,0),tracks=tracks))
        for c in cores.values():c['support']={j for j in Q if rng.randrange(3)==0}
        W={o:set(c['support']) for o,c in cores.items()}
        for s in switches:
            for t in s['tracks']:W[t['owner']]|=t['support']
        rng.shuffle(possible);links=possible[:rng.randrange(min(18,len(possible))+1)]
        data=(kinds,pairs,links,W,Q);available={j for j in Q if rng.getrandbits(1)}
        result=core_flow(data,switches,cores,available);vals=[];lift=None
        for bits in itertools.product((False,True),repeat=q):
            newends={o:[v for v in pair if v not in chosen] for o,pair in enumerate(pairs)}
            newW={o:set(c['support']) for o,c in cores.items()};flips=set()
            for s,flip in zip(switches,bits):
                if flip:flips.add(s['tile'])
                for i,t in enumerate(s['tracks']):
                    o=s['tracks'][i^int(flip)]['owner'];newends[o].append(t['bp']);newW[o]|=t['support']
            assert all(len(v)==2 for v in newends.values())
            variant=(kinds,[tuple(newends[o]) for o in range(len(pairs))],links,newW,Q)
            f=fork_flow(*restrict(variant,available));vals.append((f['value'],f['cost']))
            assert abs(vals[-1][0]-vals[0][0])<=len(flips)
            if flips==result['flips']:lift=variant
            totals['abstract_orientation_comparisons']+=1
        assert max(vals,key=lambda x:(x[0],-x[1]))==(result['value'],result['cost'])
        assert evaluate(*lift[:2],result['links'],{o:w&available for o,w in lift[3].items()},available)['value']==result['value']
        totals['abstract_core_networks']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();rng=random.Random(20261027)
    abstract_controls(totals,rng)
    for q in (1,2,3):
        cur,_=stack(q);compare(cur,totals,rng,5,terminal=q==1)
    cur,_=fixture()
    for sym in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,*sym);compare((*shape,T,M),totals,rng,5,terminal=False)
    chain_records=[]
    for q in (1,2,3,4):
        shape,T,M=transformed(*chain(q)[0],True,False,False);current=(*shape,T,M)
        data,roots,switches,cores=compare(current,totals,rng,3)
        good=core_flow(data,switches,cores,set());bad=core_flow(data,switches,cores,set(),beta_units=2)
        _,A,B,Z=owner_data(*data[:2])
        assert len(roots)==q and len(B)==q-1
        assert (good['value'],good['cost'])==(q-1,3*(q-1))
        assert (bad['value'],bad['cost'])==(2*(q-1),6*(q-1))
        full=fork_flow(*data);assert (full['value'],full['cost'])==(2*q,0)
        chain_records.append(dict(q=q,shape=shape,endpoints=2*len(M),selected=len(T),roots=roots,
            beta_cores=len(B),correct_empty_pool=(good['value'],good['cost']),
            wrong_two_beta_units=(bad['value'],bad['cost']),full_original_pool=(full['value'],full['cost'])))
        if q==2:
            saved=json.loads((Path(__file__).parent/'fixtures/pinwheel_beta_bridge_duplicate_credit.json').read_text())
            assert tuple(saved['shape'])==shape and set(map(tuple,saved['selected']))==T
            assert [tuple(map(tuple,e)) for e in saved['matching']]==M
            assert set(map(tuple,saved['roots']))==set(roots)
            assert len(check_rank_certificate(current,[[tuple(v) for v in wave] for wave in saved['frozen_schedule']]))==322
            lift=model(current,roots,bad['flips'])[0]
            actual=evaluate(*lift[:2],bad['links'],{o:set() for o in lift[3]},set())['value']
            independent,count=brute(*lift[:2],bad['links'],{o:set() for o in lift[3]},set())
            assert actual==1 and independent==(1,3) and count==64
            assert len(good['separator'])==1 and good['separator'][0][0]=='whole_beta_core'
            assert len(good['blocked_sources'])==4 and good['deficit']==3
            totals['independent_terminal_matchings']+=count
            chain_records[-1]['duplicate_credit_counterexample']=dict(
                flips=sorted(bad['flips']),six_actual_links=bad['links'],wrong_claim=2,
                actual_payment=actual,restricted_link_subset_optimum=independent,
                independently_enumerated_subsets=count,correct_separator=good['separator'],
                blocked_sources=good['blocked_sources'],direction_optimized_deficit=3)
            # Also exercise a beta tail whose second root is left untouched.
            compare(current,totals,rng,3,selected={roots[0]})
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),chain_controls=chain_records,
        theorem='Written: arbitrary selected degree-three frozen pinwheel tiles admit one exact joint min-cost flow using fixed outside alpha/mixed/beta cores, each beta core one private unit; stub-supported beta-fork payment is moved to its incoming stub before the switch. Every integral flow extends to physical directions and normalizes to legal stems/forks. Exact direction-optimized deficit=max_Z(blocked_sources-|Z|) on shared original unit gates. Gain at most one per root.',
        limitations='Uniform original background; exact degree3 and bundle terminality; available original resources arbitrary. No new full-pool deficit repair or universal5/6. Chain q controls test known physical families; no all-q incorrect-credit deficit formula claimed without separate written routing proof.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',**totals)))


if __name__=='__main__':main()
