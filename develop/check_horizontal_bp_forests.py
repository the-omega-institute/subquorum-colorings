"""Original horizontal-BP mixed forests, exact weighted compression and controls.

The general geometric/path proofs are in HORIZONTAL_BP_FORESTS.md.
Uses only the Python standard library and existing independent verifiers.
"""
import argparse
from collections import Counter, defaultdict
import itertools, json, random
from pathlib import Path
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import canonical, evaluate, brute, whole_support_data, contract
from check_whole_support_fork_flow import fork_flow
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_residual_corridors import direct_check

if not __debug__:raise RuntimeError('Run without -O: assertions required.')


def forests(data,H):
    kinds,pairs,links,W,I=data
    owner,A,B,M=owner_data(kinds,pairs);H=set(H)
    assert H<=M
    links=sorted(e for e in set(links) if owner[e[0]]!=owner[e[1]])
    incoming=defaultdict(list);outgoing=defaultdict(list)
    for e in links:
        incoming[owner[e[1]]].append(e);outgoing[owner[e[0]]].append(e)
    assert all(len(incoming[h])<=1 for h in H)
    reachable=set(A);pending=list(A)
    while pending:
        u=pending.pop()
        for e in outgoing[u]:
            v=owner[e[1]]
            if v not in reachable:reachable.add(v);pending.append(v)
    live=H&reachable;root_of={};paths={};trees={}
    roots=sorted(h for h in live if owner[incoming[h][0][0]] not in H)
    for root in roots:
        tree=set();todo=[(root,())]
        while todo:
            h,path=todo.pop()
            assert h not in root_of
            root_of[h]=root;paths[h]=path;tree.add(h)
            for e in outgoing[h]:
                v=owner[e[1]]
                if v in live:todo.append((v,path+(e,)))
        trees[root]=tree
    assert set(root_of)==live
    assert all(owner[incoming[h][0][0]] in trees[root] for root,tree in trees.items() for h in tree if h!=root)
    return dict(trees=trees,root_of=root_of,paths=paths,removed=H-live,incoming=incoming,
                outgoing=outgoing,owner=owner,A=A,B=B,M=M,H=H)


def solve_compressed(data,H,ignore_internal_tolls=False):
    kinds,pairs,links,W,I=data;F=forests(data,H)
    owner,A,B,M=F['owner'],F['A'],F['B'],F['M'];root_of=F['root_of'];H=F['H']
    edges=[];adj=defaultdict(list);s=('s',);t=('t',)
    def add(u,v,cap,cost=0,lift=()):
        i=len(edges);edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,lift=lift),
                                  dict(u=v,v=u,cap=0,initial=0,cost=-cost,lift=())]);adj[u].append(i);adj[v].append(i+1)
    def out(o):
        return ('a',o) if o in A else ('b',o) if o in B else ('fo',root_of[o]) if o in H else ('mo',o)
    def entry(tip):
        o=owner[tip]
        return ('bp',tip) if o in B else ('fi',root_of[o]) if o in H else ('mi',o)
    for a in A:add(s,out(a),1)
    for m in M-H:add(('mi',m),out(m),1)
    for root in F['trees']:add(('fi',root),out(root),1)
    for b in B:
        for tip in pairs[b]:add(('bp',tip),out(b),1)
        add(out(b),t,1)
    for j in I:add(('j',j),t,1)
    large=len(A)+1
    for e in sorted(set(links)):
        u,v=map(owner.get,e)
        if u==v or u in H:continue
        if v in F['removed']:continue
        if v in H:assert v==root_of[v]
        add(out(u),entry(e[1]),large,1,(e,))
    for o in set(range(len(pairs)))-H:
        for j in W[o]:add(out(o),('j',j),large)
    # Distinct outputs keep ORIGINAL interval IDs and actual beta BP entries.
    for root,tree in F['trees'].items():
        choices={}
        def offer(target,path):
            if target not in choices or len(path)<len(choices[target]):choices[target]=path
        for h in tree:
            path=F['paths'][h]
            for j in W[h]:offer(('j',j),path)
            for e in F['outgoing'][h]:
                if owner[e[1]] not in H:offer(entry(e[1]),path+(e,))
        for target,path in choices.items():
            # Deliberately wrong option is used only for a cost countercontrol.
            cost=(int(bool(path) and target[0]!='j') if ignore_internal_tolls else len(path))
            add(out(root),target,large,cost,path)
    nodes=set(adj)|{s,t};value=cost=0
    while True:
        dist={s:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in dist:
                    candidate=dist[e['u']]+e['cost']
                    if e['v'] not in dist or candidate<dist[e['v']]:dist[e['v']]=candidate;parent[e['v']]=i;changed=True
            if not changed:break
        assert all(not e['cap'] or e['u'] not in dist or dist.get(e['v'],10**12)<=dist[e['u']]+e['cost'] for e in edges)
        if t not in dist:break
        v=t;seen=set()
        while v!=s:
            assert v not in seen;seen.add(v);i=parent[v];edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1;cost+=dist[t]
    selected=[x for e in edges[::2] for x in e['lift'] if e['initial']>e['cap']]
    assert len(selected)==len(set(selected))
    assert len({v for e in selected for v in e})==2*len(selected)
    assert evaluate(*data[:2],selected,*data[3:])['value']==value
    if not ignore_internal_tolls:assert len(selected)==cost
    return dict(value=value,cost=cost,lifted_links=len(selected),selected=selected,
                trees=len(F['trees']),live_h=len(root_of),removed_h=len(F['removed']),
                max_depth=max(map(len,F['paths'].values()),default=0))


def physical(totals):
    records=[]
    # A fixture is admitted only after independent feasibility and freezing checks.
    for path in sorted((Path(__file__).parent/'fixtures').glob('*.json')):
        j=json.loads(path.read_text())
        if not all(k in j for k in ('shape','selected','matching')):continue
        if not (len(j['shape'])==2 and all(isinstance(x,int) for x in j['shape'])):continue
        current=(*j['shape'],set(map(tuple,j['selected'])),[tuple(map(tuple,e)) for e in j['matching']])
        mate={v:w for e in current[3] for v,w in (e,e[::-1])}
        frozen,layers=frozen_certificate(current)
        if frozen!=set(mate):continue
        direct_check(*current)
        check_rank_certificate(current,[[tuple(w['endpoint']) for w in layer] for layer in layers])
        data,meta,_=whole_support_data(current,whole_bands(current));owner,A,B,M=owner_data(*data[:2])
        H=set();long=0;branch=0
        for m in M:
            bp=next(v for v in data[1][m] if data[0][v]=='BP')
            tp=next(v for v in data[1][m] if data[0][v]=='TP')
            if bp[0]!=mate[bp][0]:continue
            H.add(m);long+=mate[bp]!=tp
            candidates=[e for e in data[2] if owner[e[1]]==m and owner[e[0]]!=m]
            assert len(candidates)<=1
            for u,v in candidates:
                assert u[0]==v[0] and abs(u[1]-v[1])==1 and u!=mate[v]
            branch+=sum(owner[u]==m and owner[v]!=m for u,v in data[2])>1
        F=forests(data,H)
        totals['physical_frozen_fixtures']+=1;totals['physical_h_owners']+=len(H)
        totals['physical_long_h_owners']+=long;totals['physical_branching_h_owners']+=branch
        totals['physical_live_h_owners']+=len(F['root_of'])
        totals['physical_multi_owner_trees']+=sum(len(t)>1 for t in F['trees'].values())
        pools=[set(data[4]),set(),{i for i in data[4] if i%2==0},{i for i in data[4] if i%3==1}]
        for Q in pools:
            cur=(*data[:3],{o:w&Q for o,w in data[3].items()},Q)
            actual=fork_flow(*cur);ans=solve_compressed(cur,H)
            assert (actual['value'],actual['cost'])==(ans['value'],ans['cost'])
            totals['physical_full_flow_cost_comparisons']+=1
        records.append(dict(fixture=path.name,endpoints=len(mate),h_owners=len(H),long_h=long,
                            branching_h=branch,trees=len(F['trees']),live_h=len(F['root_of'])))
    return records



def physical_frontier_control(totals):
    path=Path(__file__).parent/'fixtures/frozen_active_short_tail_merger.json'
    j=json.loads(path.read_text());current=(*j['shape'],set(map(tuple,j['selected'])),[tuple(map(tuple,e)) for e in j['matching']])
    data,meta,_=whole_support_data(current,whole_bands(current));owner,A,B,M=owner_data(*data[:2])
    chosen=[owner[v] for v in [(5,6),(5,12),(5,7),(5,11),(5,9)]]
    assert len(set(chosen))==5 and set(chosen[:2])<=A and set(chosen[2:])<=M
    Q={i for i in data[4] if (meta['intervals'][i]['band'],meta['intervals'][i]['first'],meta['intervals'][i]['last']) in [(5,10,10),(5,12,12)]}
    assert len(Q)==2
    pairs=[data[1][o] for o in chosen];tips={v for pair in pairs for v in pair}
    d=({v:data[0][v] for v in tips},pairs,[e for e in data[2] if set(e)<=tips],
       {i:data[3][o]&Q for i,o in enumerate(chosen)},Q)
    mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    assert all(mate[v][0]==v[0] for v in [(5,7),(5,11)])
    assert mate[(5,9)]==(6,9)
    F=forests(d,{2,3});assert list(map(len,F['trees'].values()))==[1,1]
    ans=solve_compressed(d,{2,3});orig=fork_flow(*d);independent,count=brute(*d)
    assert independent==(ans['value'],ans['cost'])==(orig['value'],orig['cost'])==(1,2)
    assert all(not d[3][o] for o in range(4)) and d[3][4]==Q
    totals['actual_restricted_vertical_frontier_collision']=1
    totals['independent_terminal_matchings']+=count
    return dict(fixture=path.name,scope='Earlier completely frozen board; RESTRICTED five-owner two-resource allocation, not full-board deficit.',
                horizontal_roots=[(5,7),(5,11)],vertical_frontier=(5,9),original_units=sorted(Q),**ans)


def abstract(totals):
    rng=random.Random(20261025051);records=[]
    for i in range(220):
        na=rng.randrange(1,4);nh=rng.randrange(1,6);nv=rng.randrange(3);nb=rng.randrange(1,4)
        kinds,pairs,_=canonical('A'*na+'M'*(nh+nv)+'B'*nb)
        H=set(range(na,na+nh));M=set(range(na,na+nh+nv));A=set(range(na))
        tp=lambda o:pairs[o][1] if o in M else pairs[o][0]
        bp=lambda o:pairs[o][0]
        links=[]
        # Every H owner has one predecessor, possibly in a sealed directed cycle.
        for h in sorted(H):
            choices=sorted(A|M-{h})
            if rng.random()<.85:links.append((tp(rng.choice(choices)),bp(h)))
        for o in sorted(A|M):
            for v in range(na+nh,len(pairs)):
                if o!=v and rng.random()<.22:
                    target=rng.choice(pairs[v]) if v>=na+nh+nv else bp(v)
                    links.append((tp(o),target))
        links=sorted(set(links));I=set(range(rng.randrange(1,4)))
        W={o:{j for j in I if rng.random()<.24} for o in range(len(pairs))}
        data=kinds,pairs,links,W,I
        ans=solve_compressed(data,H);orig=fork_flow(*data)
        assert (ans['value'],ans['cost'])==(orig['value'],orig['cost'])
        totals['abstract_full_flow_cost_comparisons']+=1
        totals['abstract_models_with_pruned_h']+=bool(ans['removed_h'])
        F=forests(data,H)
        totals['abstract_branching_h_owners']+=sum(sum(F['owner'][e[1]] in H for e in F['outgoing'][h])>1 for h in H)
        if len(links)<=10 and i<45:
            independent,count=brute(*data)
            assert independent==(ans['value'],ans['cost'])
            totals['independent_terminal_models']+=1;totals['independent_terminal_matchings']+=count
    # Two trees with a common VERTICAL gate still collide despite two sinks.
    kinds,pairs,_=canonical('AAMMM')
    d=(kinds,pairs,[(0,4),(2,6),(5,8),(7,8)],
       {0:set(),1:set(),2:set(),3:set(),4:{0,1}},{0,1})
    ans=solve_compressed(d,{2,3});assert (ans['value'],ans['cost'])==(1,2)
    records.append(dict(control='two_h_trees_first_vertical_gate_collision',**ans))
    # Distinct trees share one original interval; no owner gate can duplicate it.
    kinds,pairs,_=canonical('AAMM')
    d=(kinds,pairs,[(0,4),(2,6)],{0:set(),1:set(),2:{0},3:{0}},{0})
    ans=solve_compressed(d,{2,3});assert (ans['value'],ans['cost'])==(1,1)
    records.append(dict(control='two_h_trees_one_original_interval',**ans))
    # A branching tree, shallow/deep supports and a sealed two-node H cycle.
    kinds,pairs,_=canonical('AMMMMM')
    d=(kinds,pairs,[(0,2),(3,4),(3,6),(9,10),(11,8)],
       {0:set(),1:{1},2:set(),3:{0},4:set(),5:set()},{0,1})
    restrict=lambda Q:(*d[:3],{o:w&Q for o,w in d[3].items()},Q)
    deep=restrict({0});shallow=restrict({1})
    ans=solve_compressed(deep,{1,2,3,4,5});wrong=solve_compressed(deep,{1,2,3,4,5},True)
    shallow_ans=solve_compressed(shallow,{1,2,3,4,5})
    assert (ans['value'],ans['cost'],ans['removed_h'])==(1,2,2)
    assert (shallow_ans['value'],shallow_ans['cost'])==(1,1)
    assert (wrong['value'],wrong['cost'],wrong['lifted_links'])==(1,1,2)
    records.append(dict(control='branching_tolls_and_unreachable_cycle',deep_resource_only=ans,
                        root_resource_only=shallow_ans,wrong_zero_internal_toll=wrong))
    totals['explicit_abstract_countercontrols']=3
    return records



def serial_interfaces(totals):
    from check_frozen_serial_escape import decorated
    rng=random.Random(20261025053);examples=[]
    for test in range(100):
        q=rng.randrange(1,5);lengths=tuple(rng.randrange(2,5) for _ in range(q))
        spec=tuple(rng.choice(('M','M','B','I0','I1','H')) for _ in range(q))
        raw,C,base,_=decorated(lengths,spec)
        kinds,pairs,links,W,I=raw;kinds=dict(kinds);pairs=list(pairs);links=list(links);W={o:set(w) for o,w in W.items()};I=set(I)|{0,1,2}
        owner,A,B,M=owner_data(kinds,pairs);N=sum(lengths);skeleton_count=3*N
        H={o for o in M if o>=skeleton_count};original_roots=sorted(H)
        for root in original_roots:
            nodes=[root];children=Counter()
            for _ in range(rng.randrange(4)):
                h=rng.choice([x for x in nodes if children[x]<2]);o=len(pairs);v=2*o
                kinds[v]='BP';kinds[v+1]='TP';pairs.append((v,v+1));W[o]=set();links.append((pairs[h][1],v));children[h]+=1;nodes.append(o);H.add(o)
            for h in nodes:W[h]={j for j in I if rng.random()<.25}
        owner,A,B,M=owner_data(kinds,pairs)
        baseline_betas={owner[v] for u,v in base};remaining_betas=B-baseline_betas
        for h in sorted(H):
            if remaining_betas and rng.random()<.45:links.append((pairs[h][1],pairs[rng.choice(sorted(remaining_betas))][0]))
        # A shared vertical-BP frontier is kept in the full comparison, but is
        # excluded from the forest-only exact interface and never counted as a sink.
        vgate=len(pairs);v=2*vgate;kinds[v]='BP';kinds[v+1]='TP';pairs.append((v,v+1));W[vgate]={0,1}
        for root in original_roots:
            if rng.random()<.6:links.append((pairs[root][1],v))
        data=kinds,pairs,sorted(set(links)),W,I
        owner,A,B,M=owner_data(kinds,pairs)
        F=forests(data,H);assert set(F['trees'])==set(original_roots)
        choices=[];offset=0
        for n,case in zip(lengths,spec):
            tip=pairs[offset+n+1][1];offset+=3*n;offers={}
            def offer(resource,path):
                if resource not in offers or len(path)<len(offers[resource]):offers[resource]=path
            for j in W[owner[tip]]:offer(('interval',j),())
            for e in data[2]:
                if e[0]!=tip:continue
                target=owner[e[1]]
                if target in remaining_betas:offer(('beta',target),(e,))
                if target in H:
                    assert target==F['root_of'][target]
                    for h in F['trees'][target]:
                        prefix=(e,)+F['paths'][h]
                        for j in W[h]:offer(('interval',j),prefix)
                        for last in F['outgoing'][h]:
                            b=owner[last[1]]
                            if b in remaining_betas:offer(('beta',b),prefix+(last,))
            choices.append(offers)
        best=None
        def search(i,used,selected):
            nonlocal best
            if i==q:
                score=(len(selected),-sum(len(choices[a][r]) for a,r in selected))
                if best is None or score>best[0]:best=(score,list(selected))
                return
            search(i+1,used,selected)
            for r in choices[i]:
                if r not in used:search(i+1,used|{r},selected+[(i,r)])
        search(0,set(),[]);nu,negative_cost=best[0];tau=-negative_cost
        old_rank=spec.count('B')+len({x for x in spec if x.startswith('I')})
        assert nu>=old_rank
        totals['serial_strict_gain_over_direct_escape_bound']+=nu>old_rank
        selected=C+base+[e for i,r in best[1] for e in choices[i][r]]
        assert len({v for e in selected for v in e})==2*len(selected)
        assert len(selected)==2*N-q+tau
        assert evaluate(*data[:2],selected,*data[3:])['value']==N-q+nu
        # Exact comparison after freezing the baseline and cutting off vertical
        # frontier arcs. This is a declared certificate class, not the full board.
        filtered=(*data[:2],[e for e in data[2] if owner[e[1]]!=vgate and
                    (owner[e[0]] not in H or owner[e[1]] not in baseline_betas)],*data[3:])
        ans=fork_flow(*contract(filtered,C+base))
        assert (ans['value'],ans['cost'])==(nu,tau)
        full=fork_flow(*contract(data,C))
        assert full['value']>=N-q+nu
        totals['serial_forest_matching_certificates']+=1
        totals['serial_fixed_baseline_exact_value_cost_checks']+=1
        totals['serial_full_fixed_c_lower_bound_checks']+=1
        totals['serial_vertical_frontier_additional_gain_controls']+=full['value']>N-q+nu
        if test<5:examples.append(dict(spec=spec,lengths=lengths,rank=nu,previous_direct_rank=old_rank,added_cost=tau,payment=N-q+nu,full_fixed_c_payment=full['value']))
    return examples


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();p=physical(totals);a=abstract(totals);physical_control=physical_frontier_control(totals);serial=serial_interfaces(totals)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(dict(status='passed',counts=dict(totals),physical=p,controls=a,physical_frontier_control=physical_control,serial_interfaces=serial,
        scope='General geometric indegree/forest proof is written. Physical horizontal-BP mixed includes long bent owners; branching controls abstract. Exact full-flow value/cost compression, not universal compensation or 5/6.'),indent=2)+'\n')
    print(json.dumps(dict(totals),indent=2))
if __name__=='__main__':main()
