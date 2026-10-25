"""Short horizontal mixed chains: simultaneous contraction and corridor slots.

Original board, original interval IDs; no physical deletion or frozen recursion.
General proof: SHORT_MIXED_CHAINS_AND_CORRIDOR_HOLE_BUDGET.md.
"""
import argparse
from collections import Counter,defaultdict
import itertools
import json
from pathlib import Path

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import fixture as slot_fixture,matching
from check_frozen_beta_support_fork import fixture as fork_fixture
from check_interval_connector_cycles_and_missing_ports import stack,whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_paired_hole_certificates import exact_check,paired_fixture
from check_partial_tip_compensation import interaction_components
from check_residual_corridors import transformed
from check_residual_reserve_cost_profile import Network
from check_frozen_beta_support_fork import restrict
from check_endpoint_free_gap_compensation import gap_access
from check_shared_pocket_completion import fixture as loose_fixture
from check_tight_shared_pocket import fixture as tight_fixture
from check_vertical_tip_injection import inspect as old_certificate
from check_whole_support_fork_normal_form import ordinary_flow,whole_support_data,optimize,evaluate,canonical
from check_whole_support_fork_flow import fork_flow

if not __debug__:raise RuntimeError('Assertions required; run without -O.')


def chains(current,bands,data):
    kinds,pairs,links,_,_=data;owner,_,_,mixed=owner_data(kinds,pairs)
    loc={v:(b,c,p) for b,cols in enumerate(bands) for c,col in enumerate(cols) for p,v in enumerate(col)}
    mate={v:w for e in current[3] for v,w in (e,e[::-1])}
    short={o for o in mixed if any(set(e)==set(pairs[o]) and loc[e[0]][0]==loc[e[1]][0] for e in current[3])}
    tp={o:next(v for v in pairs[o] if kinds[v]=='TP') for o in short}
    bp={o:next(v for v in pairs[o] if kinds[v]=='BP') for o in short}
    outgoing={};incoming={};internal={}
    for u,v in links:
        a,b=owner[u],owner[v]
        if a!=b and a in short and b in short:
            assert a not in outgoing and b not in incoming
            outgoing[a]=b;incoming[b]=a;internal[a,b]=(u,v)
    unseen=set(short);answer=[]
    for head in sorted(short-incoming.keys()):
        row=[];a=head
        while True:
            assert a in unseen;unseen.remove(a);row.append(a)
            if a not in outgoing:break
            a=outgoing[a]
        b,c,p=loc[bp[head]];direction=loc[tp[head]][1]-c;assert direction in (-1,1)
        for i,a in enumerate(row):
            assert loc[bp[a]]==(b,c+2*direction*i,p)
            assert loc[tp[a]]==(b,c+direction*(2*i+1),p)
            assert mate[tp[a]]==bp[a]
        answer.append(row)
    assert not unseen,'A cycle of short horizontal mixed owners would contradict strict row progress.'
    return answer,tp,bp,internal


def contract_flow(data,rows,tp,bp,internal,omit_toll=False):
    kinds,pairs,links,support,resources=data;owner,alphas,betas,mixed=owner_data(kinds,pairs)
    outgoing=defaultdict(set)
    for u,v in links:
        if owner[u]!=owner[v]:outgoing[owner[u]].add(owner[v])
    reached=set(alphas);todo=list(reached)
    while todo:
        for b in outgoing[todo.pop()]-reached:reached.add(b);todo.append(b)
    short={a for row in rows for a in row};group={a:i for i,row in enumerate(rows) for a in row}
    active={i for i,row in enumerate(rows) if row[0] in reached}
    for i,row in enumerate(rows):
        assert all((a in reached)==(i in active) for a in row)
        if i in active:assert all(not support[a] for a in row[:-1])
    graph=Network();source=('s',);sink=('t',);graph.nodes|={source,sink}
    def exit_node(a):
        if a in short:
            i=group[a];assert i in active and a==rows[i][-1];return ('chainout',i)
        return ('alpha',a) if a in alphas else ('beta',a) if a in betas else ('out',a)
    for a in alphas:graph.add(source,exit_node(a),1,tag=('alpha',a))
    for a in mixed-short:graph.add(('in',a),exit_node(a),1,tag=('mixed',a))
    for i in sorted(active):
        toll=0 if omit_toll else len(rows[i])-1
        graph.add(('chainin',i),('chainout',i),1,toll,('chain',i))
    for b in betas:
        for v in pairs[b]:graph.add(('bp',v),exit_node(b),1,tag=('bp',v))
        graph.add(exit_node(b),sink,1,tag=('beta',b))
    for j in resources:graph.add(('j',j),sink,1,tag=('interval',j))
    large=len(alphas)+1
    for u,v in sorted(set(links)):
        a,b=owner[u],owner[v]
        if a==b:continue
        if a in short and b in short and group[a]==group[b]:continue
        if (a in short and group[a] not in active) or (b in short and group[b] not in active):continue
        if b in short:
            i=group[b];assert b==rows[i][0] and v==bp[b];entry=('chainin',i)
        else:entry=('bp',v) if b in betas else ('in',b)
        graph.add(exit_node(a),entry,large,1,('link',u,v))
    for a,js in support.items():
        if a in short and (group[a] not in active or a!=rows[group[a]][-1]):
            if group[a] in active:assert not js
            continue
        for j in js:graph.add(exit_node(a),('j',j),large,tag=('access',a,j))
    value=cost=0
    while (extra:=graph.augment(source,sink)) is not None:value+=1;cost+=extra
    graph.potentials();chosen=[];active_toll=0
    for edge in graph.edges[::2]:
        amount=edge['initial']-edge['cap']
        if not amount:continue
        tag=edge['tag']
        if tag[0]=='link':assert amount==1;chosen.append(tuple(tag[1:]))
        if tag[0]=='chain':
            assert amount==1;row=rows[tag[1]]
            chosen.extend(internal[a,b] for a,b in zip(row,row[1:]));active_toll+=len(row)-1
    assert len(set(chosen))==len(chosen)
    assert len({u for u,v in chosen})==len(chosen)==len({v for u,v in chosen})
    assert evaluate(*data[:2],chosen,*data[3:])['value']==value
    assert len(chosen)==cost+(active_toll if omit_toll else 0)
    return dict(value=value,cost=cost,lifted_cost=len(chosen),chain_toll=active_toll,
                original_mixed=len(mixed),contracted_mixed=len(mixed-short)+len(active),
                nodes=len(graph.nodes),links=chosen)


def inspect(current,bands,totals,independent=False):
    old=old_certificate(current,bands,Counter())
    data,meta,_=whole_support_data(current,bands);kinds,pairs,links,support,resources=data
    owner,aa,_,_=owner_data(kinds,pairs);rows,tp,bp,internal=chains(current,bands,data)
    ports={v:{meta['owner'][p] for p in meta['all_ports'][v]} for v,k in kinds.items() if k=='TP'}
    # Existing free-tip corridor ownership: at most one user at either interval side.
    allusers=defaultdict(set)
    for v,js in ports.items():
        for j in js:allusers[j].add(v)
    assert all(len(u)<=2 for u in allusers.values())
    assert all(len(u)<=1 for j,u in allusers.items() if j in meta['boundary'])
    assigned={};users=defaultdict(list)
    for v,js in sorted(ports.items()):
        if js&resources:
            j=min(js&resources);assert j in support[owner[v]]
            slot=len(users[j]);assert slot<2;users[j].append(v);assigned['interval',j,slot]=v
    vertical={tuple(v) for v in old['vertical_missing']}-set(assigned.values())
    adjacency={v:{('bp',w) for u,w in links if u==v} for v in vertical}
    injected=matching(adjacency);assert len(injected)==len(vertical);assigned.update(injected)
    # Reachable chain supports occur only at the tail's genuine free gap.
    free_gap=gap_access(current,bands,Counter())[4]
    for row in rows:
        incoming=[(u,v) for u,v in links if v==bp[row[0]] and owner[u] not in row]
        if incoming:
            assert set().union(*(support[a] for a in row))==free_gap[tp[row[-1]]]
            assert all(not support[a] for a in row[:-1])
            totals['chain_support_tail_equalities']+=1
    reduced=contract_flow(data,rows,tp,bp,internal)
    original=fork_flow(*data)
    assert (reduced['value'],reduced['cost'])==(original['value'],original['cost'])
    totals['full_value_cost_contractions']+=1;totals['actual_contracted_link_lifts']+=1
    totals['mixed_gates_removed']+=reduced['original_mixed']-reduced['contracted_mixed']
    before=exact_check(data,assigned,Counter());added=[]
    for row in rows:
        for a,b in zip(row,row[1:]):
            u,v=internal[a,b]
            assert u==tp[a] and v==bp[b]
            assert not ports[u], 'An internal chain TP has a BP on each horizontal side.'
            assert u not in assigned.values() and ('bp',v) not in assigned
            # Its only TP neighbors are its own mate and preceding short TP.
            assert {x for x,y in links if y==v}<={tp[a],tp[b]}
            assigned['bp',v]=u;added.append((u,v))
    after=exact_check(data,assigned,Counter())
    assert after['certified_deficit']<=before['certified_deficit']
    holes={v for v in ports if v not in assigned.values()}
    oldholes=set(map(tuple,old['short_holes']+old['boundary_holes']))
    assert holes<=oldholes
    tails={tp[row[-1]] for row in rows if not ports[tp[row[-1]]]&resources}
    vertical_boundary={tuple(v) for v in old['boundary_holes'] if v not in tp.values() and v not in assigned.values()}
    assert holes==tails|vertical_boundary and not tails&vertical_boundary
    boundary={v for v in holes if ports[v]};exits=holes-boundary
    assert all(ports[v]<=meta['boundary'] for v in boundary)
    assert len(boundary)<=len(meta['boundary'])
    assert exits<=tails
    grouped=[]
    for part in interaction_components(data):
        owners={i for tag,i in part if tag=='o'};hh={v for v in holes if owner[v] in owners}
        if owners&aa or hh:grouped.append(dict(alpha=len(owners&aa),chain_exits=len(hh&exits),boundary=len(hh&boundary)))
    budget=sum(min(g['alpha'],(g['chain_exits']+g['boundary'])//2) for g in grouped)
    assert budget==after['interaction_budget']<=old['interaction_bound']
    full,ordinary=fork_flow(*data),ordinary_flow(*data)
    assert full['value']>=ordinary['value']>=len(aa)-budget
    if independent:
        result=optimize(*data);assert (result['value'],result['cost'])==(full['value'],full['cost'])
        totals['independent_primitive_pack_comparisons']+=1
    totals['frozen_boards']+=1;totals['short_chains']+=len(rows);totals['short_owners']+=len(tp)
    totals['internal_links_added']+=len(added);totals['corridor_interval_assignments']+=sum(t[0]=='interval' for t in assigned)
    totals['strict_coarse_budget_improvements']+=budget<old['interaction_bound']
    totals['strict_chain_fine_improvements']+=after['certified_deficit']<before['certified_deficit']
    totals['new_zero_budget_nonempty_alpha_boards']+=bool(aa) and budget==0<old['interaction_bound']
    totals['remaining_positive_budgets']+=budget>0
    totals['remaining_certificate_deficits']+=after['certified_deficit']>0
    totals['unported_chain_exits']+=len(exits);totals['boundary_exceptions']+=len(boundary)
    return dict(alpha=len(aa),chain_lengths=[len(row) for row in rows],
        internal_links=added,unported_chain_exits=sorted(exits),boundary_exceptions=sorted(boundary),
        old_budget=old['interaction_bound'],new_budget=budget,prechain_deficit=before['certified_deficit'],
        new_certificate_deficit=after['certified_deficit'],full_value=full['value'],minimum_links=full['cost'],
        groups=grouped,assignment=[dict(target=t,tip=v) for t,v in sorted(assigned.items(),key=repr)])


def fixture_cases():
    result=[]
    for width,height,kind in itertools.product(range(6,19,2),range(4,13,2),('missing','cycle','collision')):
        current=stack(width,height,[kind]);result.append((current,whole_bands(current),False))
    for q in range(1,7):
        for fixture in (tight_fixture,loose_fixture):
            for filled in (set(),set(range(q))):
                current,_=fixture(q,filled);result.append((current,whole_bands(current),q==1))
        for pad in (0,2,10):
            current=slot_fixture(q,pad);result.append((current,whole_bands(current),q==1))
    paired,_=paired_fixture();fixtures=[slot_fixture(),paired,fork_fixture()[0],stack(6,4,['missing','collision'])]
    for name in ('unported_shared_mixed_gate.json','frozen_short_beta_deletion.json','frozen_vertical_mixed_missing_tip.json'):
        r=json.loads((Path(__file__).parent/'fixtures'/name).read_text())
        fixtures.append((*r['shape'],set(map(tuple,r['selected'])),[tuple(map(tuple,e)) for e in r['matching']]))
    for idx,current in enumerate(fixtures):
        bands=whole_bands(current)
        for sym in itertools.product((False,True),repeat=3):
            shape,selected,edges=transformed(*current,*sym);move=image_map(*current[:2],sym)
            carried=[[tuple(move(v) for v in col) for col in cols] for cols in bands]
            result.append(((*shape,selected,edges),carried,idx<2))
    return result


def toll_control(current,bands,totals):
    data,meta,_=whole_support_data(current,bands);owner,alphas,betas,mixed=owner_data(*data[:2])
    source=owner[(5,7)];j=meta['owner'][5,14]
    assert source in alphas and j in data[4]
    restricted=restrict(data,{source}|mixed,{j})
    rows,tp,bp,internal=chains(current,bands,restricted)
    correct=contract_flow(restricted,rows,tp,bp,internal)
    wrong=contract_flow(restricted,rows,tp,bp,internal,True)
    full=fork_flow(*restricted);independent=optimize(*restricted)
    assert (correct['value'],correct['cost'])==(full['value'],full['cost'])==(independent['value'],independent['cost'])==(1,3)
    assert (wrong['value'],wrong['cost'],wrong['lifted_cost'])==(1,2,3)
    ro,ra,rb,rm=owner_data(*restricted[:2])
    owner_edges=sorted({(ro[u],ro[v]) for u,v in restricted[2] if ro[u]!=ro[v]})
    # Exact adapter for the unbounded-walk potential checked in Lean.
    assert ra=={0} and not rb and len(restricted[1])==6
    assert owner_edges==[(0,1),(1,4),(4,5)]
    assert {a for a,js in restricted[3].items() if js}=={5}
    totals['independent_primitive_pack_comparisons']+=1
    return dict(source_tips=restricted[1][next(iter(owner_data(*restricted[:2])[1]))],interval_coordinate=(5,14,14),correct=correct,invalid_free_contraction=wrong,
        owner_edges=owner_edges,source_owner=0,interval_support_owners=[5],
        scope='Available-source/beta/interval restriction on an unchanged fully frozen original board; refutes dropping chain toll, not full-pool target.')


def abstract_checks(totals):
    controls=[]
    for m in range(1,33):
        kinds,pairs,_=canonical('A'+'M'*m)
        rows=[list(range(1,m+1))];tp={a:2*a+1 for a in rows[0]};bp={a:2*a for a in rows[0]}
        internal={(a,b):(tp[a],bp[b]) for a,b in zip(rows[0],rows[0][1:])}
        links=[(0,bp[1])]+list(internal.values());support={a:set() for a in range(m+1)};support[m]={0}
        data=kinds,pairs,links,support,{0};answer=contract_flow(data,rows,tp,bp,internal)
        independent=optimize(*data)
        assert (answer['value'],answer['cost'])==(independent['value'],independent['cost'])==(1,m)
        totals['abstract_chain_length_controls']+=1;totals['independent_primitive_pack_comparisons']+=1
        for kind,separate in [('M',False),('B',False),('B',True)]:
            kinds,pairs,_=canonical('AA'+'M'*(2*m)+kind);target=2+2*m
            rows=[list(range(2,2+m)),list(range(2+m,2+2*m))]
            tp={a:2*a+1 for row in rows for a in row};bp={a:2*a for row in rows for a in row}
            internal={(a,b):(tp[a],bp[b]) for row in rows for a,b in zip(row,row[1:])}
            links=[(2*i,bp[row[0]]) for i,row in enumerate(rows)]+list(internal.values())
            links += [(tp[row[-1]],2*target+int(separate and i==1)) for i,row in enumerate(rows)]
            resources={0,1} if kind=='M' else {0};support={a:set() for a in range(target+1)};support[target]=resources
            data=kinds,pairs,links,support,resources;answer=contract_flow(data,rows,tp,bp,internal)
            independent=optimize(*data);expected_value=2 if separate else 1
            assert (answer['value'],answer['cost'])==(independent['value'],independent['cost'])==(expected_value,expected_value*(m+1))
            totals['abstract_shared_receiver_controls']+=1;totals['independent_primitive_pack_comparisons']+=1
            if m in (1,2,32):controls.append(dict(chain_length=m,receiver=kind,separate_beta_tips=separate,**answer))
    return controls


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();named={'abstract_receiver_controls':abstract_checks(totals)}
    for current,bands,independent in fixture_cases():inspect(current,bands,totals,independent)
    for name,current in [('sealed',slot_fixture()),('paired',paired_fixture()[0])]:
        named[name]=inspect(current,whole_bands(current),totals,True)
    r=json.loads((Path(__file__).parent/'fixtures/frozen_vertical_mixed_missing_tip.json').read_text())
    for q in range(1,9):
        move=lambda v,i:(v[0]+14*i,v[1])
        current=(14*q,16,{move(tuple(v),i) for i in range(q) for v in r['selected']},
                 [tuple(move(tuple(v),i) for v in e) for i in range(q) for e in r['matching']])
        record=inspect(current,whole_bands(current),totals,q==1)
        if q==1:
            named['vertical_mixed']=record;named['actual_toll_control']=toll_control(current,whole_bands(current),totals)
        assert record['new_budget']==0 and record['full_value']==2*q and record['minimum_links']==0
        data,meta,_=whole_support_data(current,whole_bands(current));owner,aa,bb,mm=owner_data(*data[:2])
        sources={owner[5+14*i,7] for i in range(q)}
        resources={meta['owner'][5+7*i,14] for i in range(q)}
        restricted=restrict(data,sources|mm,resources)
        rows,tp,bp,internal=chains(current,whole_bands(current),restricted)
        correct=contract_flow(restricted,rows,tp,bp,internal)
        wrong=contract_flow(restricted,rows,tp,bp,internal,True)
        assert (correct['value'],correct['cost'])==(q,3*q)
        assert (wrong['value'],wrong['cost'],wrong['lifted_cost'])==(q,2*q,3*q)
        totals['restricted_toll_copy_models']+=1
        totals['new_fixture_copy_models']+=1
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),named=named,
        scope='General frozen geometric short-chain decomposition and simultaneous internal-link extension, with existing BT-corridor slot ownership; defect counts only remaining unported chain tails and marked boundary exceptions. Universal geometric compensation and5/6 open.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))

if __name__=='__main__':main()
