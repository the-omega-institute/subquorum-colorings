"""Source-preserving interface reoptimization; no external solver dependency.

General proofs and precise limitations: INTERFACE_RESERVE_REOPTIMIZATION.md.
"""
import argparse
from collections import Counter, defaultdict, deque
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_crossing_matching_ports import (rectangle, strand_parts, band_resources,
    model_for_components, compile_partition)
from check_frozen_beta_support_fork import restrict
from check_selection_maximum_singleton import cropped, reduced_serial_certificate
from check_whole_support_fork_flow import fork_flow, normalize_beta_paths
from check_whole_support_fork_normal_form import canonical, primitive_certificates, evaluate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__: raise RuntimeError('Assertions required; run without -O.')


def extension(data, interface, totals):
    """Old-only max flow, then restore new sources and augment, without reset.

    Each BFS path is simple and cannot reverse ANY previously saturated
    source arc. Independent min-cost fork_flow is NOT assumed to retain sources.
    """
    kinds, pairs, links, support, resources = data
    owner, alphas, betas, mixed = owner_data(kinds, pairs)
    assert interface <= alphas
    s, t = ('source',), ('sink',)
    edges = []; adj = defaultdict(list); source_arcs = {}
    def add(u, v, cap, tag):
        i = len(edges)
        edges.extend([dict(u=u,v=v,cap=cap,initial=cap,tag=tag),
                      dict(u=v,v=u,cap=0,initial=0,tag=None)])
        adj[u].append(i); adj[v].append(i+1)
        return i
    out = lambda o: ('alpha',o) if o in alphas else ('out',o) if o in mixed else ('beta',o)
    for a in sorted(alphas):
        source_arcs[a] = add(s,out(a),int(a not in interface),('source',a))
    for m in sorted(mixed): add(('in',m),out(m),1,('mixed',m))
    for b in sorted(betas):
        for tip in pairs[b]: add(('tip',tip),out(b),1,('tip',tip))
        add(out(b),t,1,('beta',b))
    for j in sorted(resources): add(('interval',j),t,1,('interval',j))
    for u,v in sorted(set(links)):
        assert kinds[u]=='TP' and kinds[v]=='BP'
        if owner[u]==owner[v]: continue
        assert owner[u] not in interface  # direct-interface network
        add(out(owner[u]),('tip',v) if owner[v] in betas else ('in',owner[v]),
            len(alphas)+1,('link',u,v))
    for o,js in support.items():
        for j in sorted(js): add(out(o),('interval',j),len(alphas)+1,('access',o,j))
    def paid():
        return {a for a,i in source_arcs.items() if edges[i]['initial']-edges[i]['cap']==1}
    value = 0; history = []
    def augment():
        nonlocal value
        before = paid(); parent = {}; seen = {s}; queue = deque([s])
        while queue and t not in seen:
            u = queue.popleft()
            for i in adj[u]:
                e = edges[i]
                if e['cap'] and e['v'] not in seen:
                    seen.add(e['v']); parent[e['v']] = i; queue.append(e['v'])
        if t not in seen: return False
        v = t; path = []
        while v != s:
            i = parent[v]; path.append(i); v = edges[i]['u']
        vertices = [s]+[edges[i]['v'] for i in reversed(path)]
        assert len(vertices)==len(set(vertices))
        assert all(i != (j^1) for i in path for j in source_arcs.values())
        for i in path: edges[i]['cap']-=1; edges[i^1]['cap']+=1
        value += 1
        assert before <= paid() and len(paid())==value
        history.append(sorted(paid())); totals['simple_augmentations_checked']+=1
        return True
    while augment(): pass
    protected = paid(); p = value
    for a in interface:
        i = source_arcs[a]; assert edges[i]['initial']==edges[i]['cap']==0
        edges[i]['initial']=edges[i]['cap']=1
    while augment():
        assert protected <= paid() and paid()-interface==protected
    # Independently extract source-to-sink paths. Discard residual forward
    # circulations, if any; they contain no source or sink arc and pay nobody.
    remaining = {i:e['initial']-e['cap'] for i,e in enumerate(edges) if i%2==0}
    paths = []
    for a in sorted(paid()):
        first = source_arcs[a]; remaining[first]-=1
        root = edges[first]['v']; parent={}; seen={root}; queue=deque([root])
        while queue and t not in seen:
            u=queue.popleft()
            for i in adj[u]:
                if i%2 or not remaining[i]: continue
                v=edges[i]['v']
                if v not in seen: seen.add(v);parent[v]=i;queue.append(v)
        assert t in seen
        v=t; route=[]
        while v!=root:
            i=parent[v];remaining[i]-=1;route.append(i);v=edges[i]['u']
        tags=[edges[first]['tag']]+[edges[i]['tag'] for i in reversed(route)]
        bs=[owner[z[1]] for z in tags if z[0]=='tip'];assert len(bs)<=1
        paths.append(dict(source=a,links=[(z[1],z[2]) for z in tags if z[0]=='link'],
            resource=tags[-1],beta=bs[0] if bs else None))
    by_beta=defaultdict(list)
    for path in paths:
        if path['beta'] is not None: by_beta[path['beta']].append(path)
    for b,ps in by_beta.items(): normalize_beta_paths(b,ps)
    chosen=[e for path in paths for e in path['links']]
    used=[path['resource'] for path in paths]
    assert len(used)==len(set(used))==value
    assert len({v for e in chosen for v in e})==2*len(chosen)
    assert evaluate(*data[:2],chosen,*data[3:])['value']==value
    assert {x['source'] for x in paths}==paid()
    totals['protected_sources_retained']+=len(protected)
    totals['distinct_terminal_assignments']+=value
    return dict(value=value,old_value=p,theta=value-p,protected=sorted(protected),
        paid=sorted(paid()),paths=paths,augmentation_paid_history=history,
        discarded_cycle_arc_flow=sum(remaining.values()))


def constrained_primitive(data, protected):
    """Independent exhaustive primitive packing with prescribed source IDs."""
    _,alphas,_,_=owner_data(*data[:2]);ps=primitive_certificates(*data)
    @lru_cache(None)
    def visit(decided, occupied, used):
        left=alphas-set(decided)
        if not left: return (0,0)
        a=min(left);best=(-10000,10000)
        if a not in protected:
            best=visit(tuple(sorted(set(decided)|{a})),occupied,used)
        for cert in ps:
            owners=set(cert['owners']);sources=owners&alphas
            if a not in sources or sources&set(decided): continue
            if owners&set(occupied): continue
            j=cert['interval']
            if j is not None and j in used: continue
            v,c=visit(tuple(sorted(set(decided)|sources)),
                tuple(sorted(set(occupied)|owners)),
                tuple(sorted(set(used)|({j} if j is not None else set()))))
            candidate=(v+cert['value'],c+len(cert['links']))
            if (candidate[0],-candidate[1])>(best[0],-best[1]):best=candidate
        return best
    return visit((),(),())


def subsets(xs):
    xs=sorted(xs)
    for mask in range(1<<len(xs)):
        yield {x for i,x in enumerate(xs) if mask>>i&1}


def check(data, groups, interface, totals, independent=False):
    own,A,_,_=owner_data(*data[:2])
    assert not set().union(set(),*groups)&interface
    assert set().union(set(),*groups)|interface==set(range(len(data[1])))
    assert sum(map(len,groups))+len(interface)==len(data[1])
    local_units=[set().union(set(),*(data[3][o] for o in g)) for g in groups]
    assert all(not x&y for x,y in itertools.combinations(local_units,2))
    local=[fork_flow(*restrict(data,g,data[4])) for g in groups]
    p=sum(f['value'] for f in local);a=len(interface)
    answer=extension(data,interface,totals);joint=fork_flow(*data)
    assert answer['old_value']==p and answer['value']==joint['value'], (data,groups,interface,answer,p,joint)
    values=[];defects=[];cut_by_pool={}
    for F in subsets(data[4]):
        vs=sum(fork_flow(*restrict(data,g,F))['value'] for g in groups)
        h=fork_flow(*restrict(data,interface,F))['value']
        cut=len(data[4]-F)+vs+h
        deficit=p-vs+a-h-len(data[4]-F)
        values.append(cut);defects.append(deficit)
        cut_by_pool[frozenset(F)]=cut
        assert p+a-cut==deficit
        totals['joint_withdrawal_cuts']+=1
    assert min(values)==joint['value']
    assert max(defects)==a-answer['theta']>=0
    assert (max(defects)==0)==(answer['theta']==a)
    assert 0<=answer['theta']<=a
    interface_units=set().union(set(),*(data[3][o] for o in interface))
    shared=interface_units&set().union(set(),*local_units)
    assert min(c for F,c in cut_by_pool.items() if data[4]-set(F)<=shared)==joint['value']
    minimizers={F for F,c in cut_by_pool.items() if c==joint['value']}
    for F,G in itertools.product(minimizers,repeat=2):
        assert F&G in minimizers and F|G in minimizers
        totals['minimizer_uncrossing_pairs']+=1
    if not shared:
        assert answer['theta']==fork_flow(*restrict(data,interface,data[4]))['value']
        totals['disjoint_interface_exact_additivity']+=1
    if independent:
        old=A-interface
        # Check EVERY feasible maximum old paid set, including ties omitted
        # by the initial BFS pack; each must survive at joint maximum.
        for P in itertools.combinations(sorted(old),p):
            P=set(P)
            if constrained_primitive(restrict(data,set(range(len(data[1])))-interface,data[4]),
                    {sorted(set(range(len(data[1])))-interface).index(x) for x in P})[0]!=p:
                continue
            # Feasibility above alone is insufficient when p=0; the empty
            # set is correctly included. A constrained packing at old max
            # pays all |P|=p protected old identities.
            v,c=constrained_primitive(data,P)
            assert v==joint['value'] and c>=joint['cost']
            totals['all_maximum_old_paid_sets_extended']+=1
        assert constrained_primitive(data,set())[0:2]==(joint['value'],joint['cost'])
        totals['independent_primitive_models']+=1
    totals['models']+=1
    return answer


def physical_model(cur):
    R,C,T,M=cur;P={v for e in M for v in e}
    regions=[rectangle(0,R,0,14),rectangle(0,R,14,C,True)]
    bands=[b for r in regions for b in r['bands']]
    parts,_=strand_parts(P,T,M,bands);Q,gaps,_=band_resources(P,T,bands)
    full,cs=model_for_components(P,T,bands,parts,Q,gaps)
    by_body={frozenset(x['body']):i for i,x in enumerate(cs)};groups=[]
    for r in regions:
        local_parts,_=strand_parts(P,T,M,r['bands'])
        groups.append({by_body[frozenset(x['body'])] for x in local_parts if x['kind'] in ('TT','BB','BT')})
    _,A,_,_=owner_data(*full[:2]);closed=set().union(*groups);I=A-closed
    selected=closed|I;renumber={o:i for i,o in enumerate(sorted(selected))}
    joint=restrict(full,selected,Q)
    interface_tips={v for i in I for v in full[1][i]}
    joint=(*joint[:2],[e for e in joint[2] if e[0] not in interface_tips],*joint[3:])
    return joint,[{renumber[o] for o in g} for g in groups],{renumber[o] for o in I},regions,full


def physical(w,totals,fixture_path):
    base=cropped(w);cur=(*base[:2],base[2]-{(0,1)},base[3]);R,C,T,M=cur
    direct_check(*cur);P={v for e in M for v in e}
    assert frozen_certificate(cur)[0]==P
    reduced_serial_certificate(w,cur)
    assert (len(T),len(M),len(P))==(40,3*w+10,6*w+20)
    assert R*C//2-len(T)-len(M)==8*w-28
    data,groups,I,regions,full=physical_model(cur)
    partition,_=compile_partition(cur,regions)
    own,A,B,_=owner_data(*data[:2]);assert len(A-I)==len(I)==1
    old=next(iter(A-I));new=next(iter(I))
    assert set(data[1][old])=={(1,5),(w,5)} and set(data[1][new])=={(1,13),(w,13)}
    j=(w//2,11,11);l=(0,1,1);Q={j,l}
    assert Q<=data[4] and not data[3][old] and j in data[3][new] and l not in data[3][new]
    lower=[((w,5),(w,6)),((w,7),(w,8))];upper=[((1,5),(1,4))]
    assert all(e in data[2] for e in lower+upper)
    assert j in data[3][own[(w,8)]] and l in data[3][own[(1,4)]]
    assert own[(w,6)]==own[(w,7)] and own[(1,4)]==own[(1,3)]
    closed=set().union(*groups)
    old_data=restrict(data,closed,Q)
    assert (fork_flow(*old_data)['value'],fork_flow(*old_data)['cost'])==(1,1)
    old_j=restrict(data,closed,{j});baseline=fork_flow(*old_j)
    assert (baseline['value'],baseline['cost'])==(1,2)
    assert baseline['links']==lower
    # The fixed baseline spends j; its only unused available unit is l.
    assert not data[3][new]&{l}
    # Keep all selected owner identities, just restrict actual availability.
    restricted=(*data[:3],{o:js&Q for o,js in data[3].items()},Q)
    answer=check(restricted,groups,I,totals,independent=w<=10)
    optimum=fork_flow(*restricted)
    assert (optimum['value'],optimum['cost'],answer['theta'])==(2,1,1)
    assert set(optimum['links'])==set(upper)
    # Explicit prescribed witness, independent of the optimizer's routes.
    assert evaluate(*restricted[:2],upper,*restricted[3:])['value']==2
    if w==8:
        frozen,layers=frozen_certificate(cur)
        fixture=dict(shape=(R,C),selected_points=sorted(T),matching_edges=M,
            freezing_layers=[[x['endpoint'] for x in layer] for layer in layers],
            available_original_units=sorted(Q),all_original_units=sorted(full[4]),
            kinds=sorted(data[0].items()),pairs=data[1],links=data[2],
            support=[(o,sorted(js)) for o,js in data[3].items()],
            old_owner=old,interface_owner=new,shared=j,private=l,
            old_baseline_links=lower,rerouted_old_links=upper,
            old_baseline_value=1,old_baseline_cost=2,local_minimum_cost=1,
            fixed_unused_matching=0,joint_value=2,joint_minimum_cost=1,theta=1,
            limits='Restricted two-unit pool; chosen old pack maximizes value but not minimum link cost; no strict full-pool gain claimed.')
        fixture_path.write_text(json.dumps(fixture,indent=2)+'\n')
    totals['fully_frozen_physical_boards']+=1
    return dict(W=w,shape=(R,C),selected=40,matching=len(M),frozen=len(P),
        numerical_slack=8*w-28,available_pool=sorted(Q),full_original_count=len(full[4]),
        fixed_pack_nu=0,theta=1,old_baseline_cost=2,local_minimum_cost=1,joint_minimum_cost=1,
        partition_compiled=True)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();rng=random.Random(2026102507)
    # One or two disjoint old networks, including two-entry beta forks and
    # mixed layers. Interface alphas use direct original units only.
    for types,groups,I in [('AAB',[{0,2}],{1}),('AAAB',[{0,1,3}],{2}),
                          ('AAMAB',[{0,2},{3,4}],{1}),('AAAMMAB',[{0,1,3,4},{5,6}],{2})]:
        kinds,pairs,possible=canonical(types)
        own,A,B,X=owner_data(kinds,pairs)
        possible=[e for e in possible if any({own[e[0]],own[e[1]]}<=g for g in groups)]
        for trial in range(70):
            links=[e for e in possible if rng.randrange(2)]
            Q=set(range(rng.randrange(4)))
            home={j:rng.randrange(len(groups)) for j in Q}
            support={o:{j for j in Q if rng.randrange(2) and
                (o in I or any(o in g and home[j]==i for i,g in enumerate(groups)))}
                for o in range(len(pairs))}
            check((kinds,pairs,links,support,Q),groups,I,totals,independent=trial<14)
    # Cost obstruction: a local cost-zero max must gain one link to pay I.
    kinds,pairs,_=canonical('AAB');data=(kinds,pairs,[(0,4)],{0:{0},1:{0},2:set()},{0})
    abstract=check(data,[{0,2}],{1},totals,True)
    assert (abstract['theta'],fork_flow(*data)['cost'])==(1,1)
    assert fork_flow(*restrict(data,{0,2},{0}))['cost']==0
    # Capacity-two beta fork: h(Q)=1 does not imply one extra payment.
    # The same original j is already needed for the second old arm.
    kinds,pairs,_=canonical('AABA')
    data=(kinds,pairs,[(0,4),(2,5)],{0:set(),1:set(),2:{0},3:{0}},{0})
    fork_control=check(data,[{0,1,2}],{3},totals,True)
    assert (fork_control['old_value'],fork_control['value'],fork_control['theta'])==(2,2,0)
    assert any(c['kind']=='fork' for c in fork_flow(*restrict(data,{0,1,2},{0}))['certificates'])
    totals['forced_two_entry_beta_fork_obstructions']+=1
    # Empty original pool retains a genuine private beta payment; no new
    # source, and no old source, are legitimate limiting cases.
    kinds,pairs,_=canonical('AB')
    check((kinds,pairs,[(0,2)],{0:set(),1:set()},set()),[{0,1}],set(),totals,True)
    kinds,pairs,_=canonical('AA')
    check((kinds,pairs,[],{0:{0},1:{0}},{0}),[set()],{0,1},totals,True)
    # Two distinct maximum old paid sets, neither privileged by the theorem.
    kinds,pairs,_=canonical('AAA')
    check((kinds,pairs,[],{0:{0},1:{0},2:{0}},{0}),[{0,1}],{2},totals,True)
    records=[physical(w,totals,Path(__file__).parent/'fixtures/interface_reserve_exchange.json')
             for w in (8,10,12,16,20,40,64,128)]
    report=dict(status='PASS',totals=dict(totals),physical_controls=records,
        proof='docs/INTERFACE_RESERVE_REOPTIMIZATION.md',
        scope='Exact joint cuts; old-only then restored-source residual augmentation with all paid source identities retained at every step; normalized whole-beta outputs; exhaustive small prescribed old maximum sets; all-W written frozen mixed-direction restricted two-unit exchange.',
        limits=['The general max-flow and all-W geometric statements rely on written proofs, not finite extrapolation.',
                'Physical strict gain uses a value-maximum, non-minimum-cost baseline and an explicitly restricted original pool.',
                'No strict full-pool physical gain or universal5over6 improvement claimed.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
