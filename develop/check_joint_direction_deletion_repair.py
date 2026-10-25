"""One physical repair model and exact direction/deletion quota frontier.

General proof: docs/JOINT_DIRECTION_AND_ISOLATED_DELETION_REPAIR.md.
Finite checks corroborate, rather than replace, that proof.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow,normalize_beta_paths
from check_whole_support_fork_normal_form import canonical,evaluate
from check_interface_reserve_reoptimization import subsets,constrained_primitive
from check_isolated_repair_selection import available,isolated,paid_sources
from check_forced_mates_and_adjacent_maxima import configuration,uniform_freezing
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_crossing_matching_ports import rectangle,compile_partition,strand_parts
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:raise RuntimeError('Assertions required; do not use -O.')


def joint_flow(data,actions,s,d,protected=set()):
    """Exact max payment, protected old sources, min deletion/flip/weight/links.

    Actions are distinct candidate interval sinks. H proxies a private
    strip payment; C is an actual outside-strip deletion singleton.
    """
    kinds,pairs,links,W,Q=data;own,A,B,X=owner_data(kinds,pairs)
    assert set(actions)<=Q and protected<=A and s>=0 and d>=0
    assert all(x['kind'] in ('H','C') and x['weight']>=0 for x in actions.values())
    source=('source',);sink=('sink',);zero=(0,0,0,0,0);edges=[];adj=defaultdict(list)
    plus=lambda a,b:tuple(x+y for x,y in zip(a,b))
    def add(u,v,cap,cost=zero,tag=None):
        i=len(edges);edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
            dict(u=v,v=u,cap=0,initial=0,cost=tuple(-x for x in cost),tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    out=lambda o:('alpha',o) if o in A else ('out',o) if o in X else ('beta',o)
    for a in sorted(A):add(source,out(a),1,(-int(a in protected),0,0,0,0),('source',a))
    for x in sorted(X):add(('in',x),out(x),1,tag=('mixed',x))
    for b in sorted(B):
        for tip in pairs[b]:add(('tip',tip),out(b),1,tag=('tip',tip))
        add(out(b),sink,1,tag=('beta',b))
    for j in sorted(Q):
        if j in actions:
            kind=actions[j]['kind'];cost=(0,int(kind=='C'),int(kind=='H'),actions[j]['weight'],0)
            add(('interval',j),('quota',kind),1,cost,('interval',j))
        else:add(('interval',j),sink,1,tag=('interval',j))
    add(('quota','H'),sink,s,tag=('quota','H'));add(('quota','C'),sink,d,tag=('quota','C'))
    large=len(A)+1
    for u,v in sorted(set(links)):
        if own[u]==own[v]:continue
        assert kinds[u]=='TP' and kinds[v]=='BP'
        add(out(own[u]),('tip',v) if own[v] in B else ('in',own[v]),large,(0,0,0,0,1),('link',u,v))
    for o,js in W.items():
        for j in sorted(js):add(out(o),('interval',j),large,tag=('access',o,j))
    nodes=set(adj)|{source,sink};value=0;total=zero
    while True:
        distance={source:zero};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in distance:
                    candidate=plus(distance[e['u']],e['cost'])
                    if e['v'] not in distance or candidate<distance[e['v']]:
                        distance[e['v']]=candidate;parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in distance:break
        v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v);i=parent[v]
            edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1;total=plus(total,distance[sink])
    remaining={i:e['initial']-e['cap'] for i,e in enumerate(edges) if i%2==0};paths=[]
    for i in adj[source]:
        if i%2 or not remaining[i]:continue
        u=source;tags=[];seen=set()
        while u!=sink:
            assert u not in seen;seen.add(u)
            j=next(j for j in adj[u] if j%2==0 and remaining[j]>0)
            remaining[j]-=1;e=edges[j];tags.append(e['tag']);u=e['v']
        beta=[own[t[1]] for t in tags if t[0]=='tip'];assert len(beta)<=1
        paths.append(dict(source=tags[0][1],beta=beta[0] if beta else None,
            resource=next(t for t in reversed(tags) if t[0] in ('interval','beta')),
            links=[(t[1],t[2]) for t in tags if t[0]=='link']))
    assert not any(remaining.values())
    for b in B:
        ps=[p for p in paths if p['beta']==b]
        if ps:normalize_beta_paths(b,ps)
    paid={p['source'] for p in paths};chosen=[e for p in paths for e in p['links']]
    terminals=[p['resource'] for p in paths]
    used={j for tag,j in terminals if tag=='interval' and j in actions}
    C={j for j in used if actions[j]['kind']=='C'};H=used-C
    assert len(C)<=d and len(H)<=s
    assert len(terminals)==len(set(terminals))==value
    assert len({v for e in chosen for v in e})==2*len(chosen)
    assert total==(-len(paid&protected),len(C),len(H),sum(actions[j]['weight'] for j in used),len(chosen))
    enabled=available(data,(Q-set(actions))|used)
    assert evaluate(*enabled[:2],chosen,*enabled[3:])['value']==value
    return dict(value=value,used=used,deletions=C,flips=H,paid=paid,cost=len(chosen),lex=total,paths=paths)


def abstract_check(data,actions,totals,independent=False):
    H={j for j,x in actions.items() if x['kind']=='H'};C=set(actions)-H;Q0=data[4]-set(actions)
    old=available(data,Q0);oldflow=fork_flow(*old);p=oldflow['value'];protected=paid_sources(old,oldflow)
    subsets_all=list(subsets(set(actions)));profiles={frozenset(F):fork_flow(*available(data,Q0|F)) for F in subsets_all}
    gain={F:f['value']-p for F,f in profiles.items()}
    RH=gain[frozenset(H)];RC=gain[frozenset(C)];R=gain[frozenset(actions)]
    for s,d in itertools.product(range(len(H)+1),range(len(C)+1)):
        expected=p+min(R,s+d,s+RC,d+RH)
        actual=joint_flow(data,actions,s,d,protected);assert actual['value']==expected and protected<=actual['paid']
        h=min(s,RH);G=expected-p
        assert (len(actual['flips']),len(actual['deletions']))==(h,G-h)
        totals['exact_optimal_action_count_profiles']+=1
        eligible=[F for F in subsets_all if len(F&H)<=s and len(F&C)<=d]
        assert max(profiles[frozenset(F)]['value'] for F in eligible)==expected
        totals['four_rank_quota_profiles']+=1
        if independent:
            best=None
            for F in eligible:
                value,cost=constrained_primitive(available(data,Q0|F),protected)
                score=(-value,len(F&C),len(F&H),sum(actions[j]['weight'] for j in F),cost)
                best=score if best is None or score<best else best
            score=(-actual['value'],len(actual['deletions']),len(actual['flips']),actual['lex'][3],actual['cost'])
            assert score==best,(score,best)
            totals['independent_lexicographic_optima']+=1
    # All possible target gains and switch limits, including infeasible ones.
    for target,s in itertools.product(range(R+1),range(len(H)+1)):
        feasible=[len(F&C) for F in subsets_all if len(F&H)<=s and gain[frozenset(F)]>=target]
        assert bool(feasible)==(target<=s+RC)
        if feasible:assert min(feasible)==max(0,target-s,target-RH)
        totals['minimum_deletion_target_profiles']+=1
    bestbudget=min(len(set(F)&C)-gain[F] for F in gain)
    assert bestbudget==-RH
    full=[F for F in gain if gain[F]==R]
    assert min(len(set(F)&C) for F in full)==R-RH
    totals['exact_combined_budget_optima']+=1;totals['abstract_models']+=1


def family(w,q,F,Y):
    assert w>=8 and w%2==0 and q>=1 and F<=set(range(q))
    h=w+2;R=q*(w+6)-4;T=set();M=[];layers=[]
    _,seed=uniform_freezing(w,1,configuration(w,1))
    for a in range(q):
        off=a*(w+6);base=configuration(w,1)
        T|={(r+off,c) for r,c in base[2]};M += [tuple((r+off,c) for r,c in e) for e in base[3]]
        layers += [[(off+r,c) for r,c in layer] for layer in seed]
        if a<q-1:T|={(off+h,4),(off+h+1,5),(off+h+1,6),(off+h+2,4),(off+h+3,4)}
    basecur=R,12,T,M;X=set(isolated(basecur));assert Y<=X
    effective={(a*(w+6)+h,4) for a in range(q-1)};assert effective<=X
    assert len(X)==q*(7*w//2-14)-1
    cur=R,12,T-Y,M;regions=[rectangle(0,R,0,2,True)]
    for a in range(q):
        off=a*(w+6);regions.append(rectangle(off,off+h,2,4,a in F))
        if a<q-1:regions.append(rectangle(off+h,off+h+4,2,4,True))
    regions += [rectangle(0,R,4,10,True),rectangle(0,R,10,12,True)]
    return basecur,cur,regions,layers,X,effective


def physical(w,q,F,Y,totals,independent=False,save=False):
    base,cur,regions,layers,X,effective=family(w,q,F,Y);direct_check(*cur)
    witnesses=check_rank_certificate(cur,layers);P={v for e in cur[3] for v in e};assert frozen_certificate(cur)[0]==P
    rec,data=compile_partition(cur,regions);own,A,B,M=owner_data(*data[:2]);assert (len(A),len(B),len(M))==(q,q,q*(w//2-2))
    assert rec['raw']==rec['slack']==21*q-19+len(Y)
    assert len(base[2])==q*(9*w//2+5)+5*(q-1)
    assert len(rec['crossing_edges'])==2*q
    active={a for a in range(q-1) if (a*(w+6)+w+2,4) in Y};components=[];part={0}
    for a in range(q-1):
        if a in active:part.add(a+1)
        else:components.append(part);part={a+1}
    components.append(part);hit=sum(bool(part&F) for part in components)
    expected=len(active)+hit;assert (rec['value'],rec['deficit'],rec['cost'])==(expected,q-expected,0)
    # Cross-operation commutation uses real band cells, not shifted indices.
    band_keys=[tuple(cols) for region in regions for cols in region['bands']]
    current_id=lambda j:(band_keys[j[0]],j[1],j[2])
    _,oldcur,oldregions,_,_,_=family(w,q,set(),set());_,olddata=compile_partition(oldcur,oldregions)
    old_keys=[tuple(cols) for region in oldregions for cols in region['bands']]
    old_id=lambda j:(old_keys[j[0]],j[1],j[2])
    strips={(a*(w+6)+r,c) for a in range(q) for r in range(w+2) for c in (2,3)}
    is_outside=lambda key:not {v for pair in key for v in pair}&strips
    old_outside={old_id(j) for j in olddata[4] if is_outside(old_keys[j[0]])}
    new_outside={current_id(j) for j in data[4] if is_outside(band_keys[j[0]])}
    by_cell={v:(b,c) for b,cols in enumerate(band_keys) for c,pair in enumerate(cols) for v in pair}
    added=set()
    for x in Y-strips:
        b,c=by_cell[x];j=(b,c,c);assert j in data[4];added.add(current_id(j))
    assert len(added)==len(Y-strips) and new_outside==old_outside|added
    for o in olddata[3]:
        oldW={old_id(j) for j in olddata[3][o] if is_outside(old_keys[j[0]])}
        newW={current_id(j) for j in data[3][o] if is_outside(band_keys[j[0]])}
        assert oldW<=newW and newW-oldW<=added
    assert data[:3]==olddata[:3]
    describe=lambda parts:{(frozenset(x['body']),tuple(x['ends'])) for x in parts}
    assert describe(strand_parts(P,cur[2],cur[3],[cols for r in regions for cols in r['bands']])[0])==describe(strand_parts(P,oldcur[2],oldcur[3],[cols for r in oldregions for cols in r['bands']])[0])
    for a in range(q):
        off=a*(w+6);root=own[(off+1,3)];assert root in A
        assert not any(own[u]==root for u,v in data[2])
        assert not olddata[3][root]
        # All reachable nonprivate resources are precisely deleted seam units.
        seam={j for j in data[3][root] if band_keys[j[0]][0][0][1]==4}
        expected_seams={a0*(w+6)+w+2 for a0 in active&{a-1,a}}
        assert {j[1] for j in seam}==expected_seams and all(j[1]==j[2] for j in seam)
        private=data[3][root]-seam
        if a in F:
            assert len(private)>=2
            assert all({o for o,js in data[3].items() if j in js}=={root} for j in private)
        else:assert not private
    if independent:
        assert constrained_primitive(data,set())==(expected,0)
        totals['independent_physical_primitive_profiles']+=1
    if save:
        fixture=dict(W=w,q=q,flips=sorted(F),deleted=sorted(Y),all_isolated=sorted(X),effective=sorted(effective),shape=cur[:2],
            selected=sorted(cur[2]),matching=cur[3],freezing_layers=layers,witnesses=witnesses,
            regions=[dict(bounds=r['bounds'],vertical=r['vertical']) for r in regions],pairs=data[1],links=data[2],
            supports=[(o,sorted(js)) for o,js in data[3].items()],resources=sorted(data[4]),
            value=rec['value'],deficit=rec['deficit'],cost=rec['cost'],slack=rec['slack'])
        (Path(__file__).parent/'fixtures/joint_direction_deletion_repair.json').write_text(json.dumps(fixture,indent=2)+'\n')
    totals['physical_models']+=1;totals['strict_freezing_events']+=len(witnesses)
    return dict(W=w,q=q,flips=len(F),deletions=len(Y),effective_deletions=len(active),value=expected,slack=rec['slack'])



def physical_joint_solver(w,q,totals):
    """Compile actual physical H/C units, then run the quota solver on them.

    Every outside isolated candidate is included; private proxy sinks name
    true row2 strip units, not synthetic abstract resources.
    """
    _,_,_,_,X,_=family(w,q,set(),set())
    strips={(a*(w+6)+r,c) for a in range(q) for r in range(w+2) for c in (2,3)}
    outside=X-strips
    _,cur,regions,_,_,_=family(w,q,set(range(q)),outside)
    _,data=compile_partition(cur,regions)
    bands=[tuple(cols) for r in regions for cols in r['bands']]
    by_cell={v:(b,c) for b,cols in enumerate(bands) for c,pair in enumerate(cols) for v in pair}
    actions={}
    for x in outside:
        b,c=by_cell[x];j=(b,c,c);assert j in data[4]
        actions[j]=dict(kind='C',weight=0)
    for a in range(q):
        b,c=by_cell[(a*(w+6)+2,2)];j=(b,c,c);assert j in data[4] and j not in actions
        actions[j]=dict(kind='H',weight=0)
    keep={j for j in data[4] if not {v for pair in bands[j[0]] for v in pair}&strips}|set(actions)
    data=available(data,keep)
    H={j for j,x in actions.items() if x['kind']=='H'};C=set(actions)-H;Q0=data[4]-set(actions)
    assert fork_flow(*available(data,Q0))['value']==0
    assert fork_flow(*available(data,Q0|H))['value']==q
    assert fork_flow(*available(data,Q0|C))['value']==q-1
    for s,d in itertools.product(range(q+1),range(q+1)):
        result=joint_flow(data,actions,s,d)
        expected=min(q,s+d,s+q-1);h=min(s,q)
        assert result['value']==expected and result['cost']==0
        assert (len(result['flips']),len(result['deletions']))==(h,expected-h)
        totals['actual_grid_joint_quota_flow_profiles']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args();totals=Counter();records=[];rng=random.Random(20261026)
    for types in ('AA','AAA','AAB','AAAB','AAM','AAAMB','AAABMM'):
        for i in range(6):
            kinds,pairs,possible=canonical(types);rng.shuffle(possible);links=possible[:rng.randrange(min(8,len(possible))+1)]
            Q=set(range(rng.randrange(3)));W={o:{j for j in Q if rng.randrange(2)} for o in range(len(pairs))}
            _,A,_,_=owner_data(kinds,pairs);actions={};nextj=len(Q)
            for a in sorted(A):
                if rng.randrange(2):
                    j=nextj;nextj+=1;Q.add(j);W[a].add(j);actions[j]=dict(kind='H',weight=rng.randrange(5))
            for _ in range(2):
                j=nextj;nextj+=1;Q.add(j);actions[j]=dict(kind='C',weight=rng.randrange(5))
                for o in W:
                    if rng.randrange(2):W[o].add(j)
            abstract_check((kinds,pairs,links,W,Q),actions,totals,independent=i<3)
    kinds,pairs,_=canonical('AA')
    bad_data=(kinds,pairs,[],{0:{0,2},1:{1}},{0,1,2})
    bad_actions={0:dict(kind='H',weight=0),1:dict(kind='H',weight=1),2:dict(kind='C',weight=0)}
    chosen=joint_flow(bad_data,bad_actions,1,1)
    assert chosen['value']==2 and chosen['used']=={1,2}
    assert fork_flow(*available(bad_data,{0,2}))['value']==1
    abstract_check(bad_data,bad_actions,totals,independent=True)
    totals['separate_cheapest_first_failure_controls']=1
    kinds,pairs,_=canonical('AAB')
    for second_tip in (4,5):
        beta_data=(kinds,pairs,[(0,4),(2,second_tip)],{0:{1},1:set(),2:{0}},{0,1})
        beta_actions={0:dict(kind='C',weight=0),1:dict(kind='H',weight=0)}
        beta_only=joint_flow(beta_data,beta_actions,0,1)
        assert beta_only['value']==(1 if second_tip==4 else 2)
        abstract_check(beta_data,beta_actions,totals,independent=True)
        totals['explicit_shared_vs_distinct_beta_entry_controls']+=1
    for w in (8,10):
        for q in range(1,5):
            _,_,_,_,X,E=family(w,q,set(),set());inside=set()
            for a in range(q):
                off=a*(w+6);inside|={x for x in X if off<=x[0]<off+w+2 and x[1] in (2,3)}
            for F,C in itertools.product(subsets(range(q)),subsets(E)):
                for Y in {frozenset(C),frozenset(C|inside),frozenset(C|(X-E))}:
                    records.append(physical(w,q,F,set(Y),totals,independent=q<=2,save=(w,q,F,set(Y))==(8,2,{0},E)))
            physical_joint_solver(w,q,totals)
            # Full candidate frontier, not an artificially restricted resource pool.
            for s,d in itertools.product(range(q+1),range(q+1)):
                maximum=max(len(C)+sum(bool(part&F) for part in path_components(q,{a for a in range(q-1) if (a*(w+6)+w+2,4) in C}))
                    for F in subsets(range(q)) for C in subsets(E) if len(F)<=s and len(C)<=d)
                assert maximum==min(q,s+d,s+q-1)
                totals['physical_complete_candidate_frontier_entries']+=1
    for w,q in itertools.product((12,20,40,64),(1,3,8,16)):
        _,_,_,_,X,E=family(w,q,set(),set())
        for F,Y in [(set(),set()),(set(),X),({0},E),(set(range(q)),set()),(set(range(0,q,2)),{x for i,x in enumerate(sorted(X)) if i%2==0})]:
            records.append(physical(w,q,F,Y,totals))
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,
        scope='Physical joint guarded-switch/isolated-deletion adapter, one contracted action rank, exact two-quota frontier and combined-budget optimum; full-candidate frozen path family.',
        limits=['Finite enumeration corroborates general proofs.','No arbitrary direction changes, no universal 5/6 improvement.','Direction sinks proxy existing physical strip reserves; only deletions increase slack.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))


def path_components(q,active):
    out=[];part={0}
    for a in range(q-1):
        if a in active:part.add(a+1)
        else:out.append(part);part={a+1}
    return out+[part]

if __name__=='__main__':main()
