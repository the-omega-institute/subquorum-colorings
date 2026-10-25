"""Exact filled-pocket-tree compression with exterior capacity retained.

All-size arguments: POCKET_TREE_EXTERIOR_COMPRESSION.md. The ordinary
grouped flow preserves value; a discounted circulation preserves cost too.
No SAT solver is imported. Existing full-flow solvers are not changed.
"""
import argparse
from collections import Counter, defaultdict, deque
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_residual_reserve_cost_profile import Network
from check_shared_pocket_completion import fixture as loose_fixture
from check_tight_shared_pocket import fixture as tight_fixture
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical, evaluate, optimize, whole_support_data

if not __debug__:
    raise RuntimeError('Run without -O; assertions required.')


def validate_blocks(data,blocks):
    owner,aa,bb,_=owner_data(*data[:2]);seen=set();local=set()
    for vertices,edges in blocks:
        assert vertices and vertices<=aa and not vertices&seen
        seen|=vertices;adj=defaultdict(set)
        assert len(edges)==len(vertices)-1
        for a,b,beta in edges:
            assert a!=b and {a,b}<=vertices and beta in bb and beta not in local
            assert not data[3][beta]
            incoming=[edge for edge in data[2] if owner[edge[1]]==beta]
            assert len(incoming)==2 and {owner[u] for u,v in incoming}=={a,b}
            assert len({v for u,v in incoming})==2
            local.add(beta);adj[a].add(b);adj[b].add(a)
        reached={min(vertices)};todo=list(reached)
        while todo:
            for v in adj[todo.pop()]-reached:reached.add(v);todo.append(v)
        assert reached==vertices
    return seen,local


def compressed(data,blocks,discounted=False):
    kinds,pairs,links,support,resources=data
    owner,alphas,betas,mixed=owner_data(kinds,pairs)
    grouped,local=validate_blocks(data,blocks)
    baseline=sum(len(v)-1 for v,e in blocks)
    penalty=len(set(links))+baseline+1
    graph=Network();source=('s',);sink=('t',);graph.nodes|={source,sink}
    exit_node=lambda o:('a',o) if o in alphas else ('out',o) if o in mixed else ('b',o)
    for a in sorted(alphas-grouped):
        graph.add(source,exit_node(a),1,-penalty if discounted else 0,('outside',a))
    for i,(vertices,_) in enumerate(blocks):
        g=('group',i)
        graph.add(source,g,1,-penalty if discounted else 0,('first',i))
        if discounted and len(vertices)>1:
            graph.add(source,g,len(vertices)-1,-1,('extra',i))
        for a in sorted(vertices):graph.add(g,exit_node(a),1,0,('choose',i,a))
    for m in sorted(mixed):graph.add(('in',m),exit_node(m),1,0,('mixed',m))
    for b in sorted(betas-local):
        for tip in pairs[b]:graph.add(('tip',tip),exit_node(b),1,0,('tip',tip))
        graph.add(exit_node(b),sink,1,0,('beta',b))
    for j in sorted(resources):graph.add(('j',j),sink,1,0,('interval',j))
    large=len(alphas)+1
    for u,v in sorted(set(links)):
        if owner[u]==owner[v] or owner[v] in local:continue
        entry=('tip',v) if owner[v] in betas else ('in',owner[v])
        graph.add(exit_node(owner[u]),entry,large,1,('link',u,v))
    for o in sorted(support):
        if o in local:continue
        for j in sorted(support[o]):graph.add(exit_node(o),('j',j),large,0,('support',o,j))
    external_value=network_cost=0
    while True:
        before=[e['cap'] for e in graph.edges]
        extra=graph.augment(source,sink)
        if extra is None:break
        if discounted and extra>=0:
            for e,cap in zip(graph.edges,before):e['cap']=cap
            break
        external_value+=1;network_cost+=extra
    # Check the actual network flow independently of the optimizer's totals.
    balance=Counter();actual_cost=0;roots=defaultdict(set)
    selected=[];outside=set();first=set();bonus=0;used_resources=set()
    for e in graph.edges[::2]:
        amount=e['initial']-e['cap'];assert 0<=amount<=e['initial']
        balance[e['u']]+=amount;balance[e['v']]-=amount
        actual_cost+=amount*e['cost']
        if not amount:continue
        tag=e['tag']
        if tag[0]=='choose':assert amount==1;roots[tag[1]].add(tag[2])
        if tag[0]=='outside':assert amount==1;outside.add(tag[1])
        if tag[0]=='first':assert amount==1;first.add(tag[1])
        if tag[0]=='extra':bonus+=amount
        if tag[0]=='link':assert amount==1;selected.append(tag[1:])
        if tag[0] in ('interval','beta'):
            assert amount==1 and tag not in used_resources;used_resources.add(tag)
    assert actual_cost==network_cost
    assert balance[source]==external_value and balance[sink]==-external_value
    assert all(v in (source,sink) or amount==0 for v,amount in balance.items())
    assert first=={i for i in roots if roots[i]}
    assert bonus==sum(max(0,len(roots[i])-1) for i in range(len(blocks)))
    score=len(outside)+len(first)
    assert network_cost==(len(selected)-bonus-penalty*score if discounted else len(selected))
    # Lift: root each tree at all selected exterior representatives, or at
    # one unpaid root. Every remaining alpha receives one distinct parent beta.
    internal=[]
    for i,(vertices,edges) in enumerate(blocks):
        seeds=roots[i] or {min(vertices)};reached=set(seeds);queue=deque(sorted(seeds))
        adj=defaultdict(list)
        for a,b,beta in edges:adj[a].append((b,beta));adj[b].append((a,beta))
        spent=set()
        while queue:
            a=queue.popleft()
            for b,beta in adj[a]:
                if b in reached:continue
                reached.add(b);queue.append(b)
                assert beta not in spent;spent.add(beta)
                internal.append(next(edge for edge in links if owner[edge[0]]==b and owner[edge[1]]==beta))
        assert reached==vertices and len(spent)==len(vertices)-max(1,len(roots[i]))
    selected+=internal
    assert len({u for u,v in selected})==len(selected)
    assert len({v for u,v in selected})==len(selected)
    assert len(internal)==baseline-bonus
    lifted=evaluate(kinds,pairs,selected,support,resources)
    assert lifted['value']==baseline+score
    answer=dict(value=baseline+score,cost=len(selected),baseline=baseline,
        exterior_coverage=score,exterior_paths=external_value,extra_exits=bonus,
        roots={i:sorted(roots[i]) for i in range(len(blocks))},links=selected)
    if not discounted:
        side=graph.reachable(source)
        cut=sum(e['initial'] for e in graph.edges[::2] if e['u'] in side and e['v'] not in side)
        assert cut==score==external_value
        answer['exterior_cut_capacity']=cut
    else:
        # Check the actual variable-flow circulation, including its return
        # edge and reverse return capacity, not just fixed-value optimality.
        back=graph.add(sink,source,len(alphas),0,('return',))
        graph.send(back,external_value)
        graph.potentials()
        assert network_cost+penalty*score+baseline==answer['cost']
    return answer


def compare(data,blocks,totals,independent=False):
    direct=fork_flow(*data);single=compressed(data,blocks);exact=compressed(data,blocks,True)
    assert single['value']==direct['value']==exact['value']
    assert exact['cost']==direct['cost']
    assert single['cost']>=exact['cost']
    grouped,_=validate_blocks(data,blocks)
    unsupported=all(not data[3][a] for a in grouped)
    if unsupported:
        assert single['cost']==direct['cost'];totals['unsupported_exact_cost_controls']+=1
    totals['models']+=1;totals['capacity_and_cost_checked_flow_lifts']+=2
    totals['simple_value_equalities']+=1;totals['discounted_value_cost_equalities']+=1
    totals['simple_cost_overestimates']+=single['cost']>direct['cost']
    totals['joint_exterior_deficits']+=direct['deficit']>0
    totals['discounted_multiple_exterior_exit_controls']+=exact['extra_exits']>0
    if independent:
        result=optimize(*data)
        assert (result['value'],result['cost'])==(exact['value'],exact['cost'])
        totals['independent_primitive_pack_comparisons']+=1
    return dict(value=direct['value'],cost=direct['cost'],simple_cost=single['cost'],
        baseline=single['baseline'],exterior_value=single['exterior_coverage'],
        exact_extra_exits=exact['extra_exits'])


def random_model(rng,unsupported=False):
    sizes=[rng.randrange(1,5) for _ in range(rng.randrange(1,4))]
    p=rng.randrange(3);n=sum(sizes)+p;trees=[];cursor=0;nb=0
    for size in sizes:
        vertices=set(range(cursor,cursor+size));edges=[]
        for v in range(cursor+1,cursor+size):
            edges.append((v,rng.randrange(cursor,v),n+nb));nb+=1
        trees.append((vertices,edges));cursor+=size
    external_betas=rng.randrange(3);mixed=rng.randrange(3)
    kinds,pairs,_=canonical('A'*n+'B'*(nb+external_betas)+'M'*mixed)
    links=[]
    for vertices,edges in trees:
        for a,b,beta in edges:links.extend([(2*a,2*beta),(2*b+1,2*beta+1)])
    owner,aa,bb,mm=owner_data(kinds,pairs);local={b for v,e in trees for a,c,b in e}
    for u in kinds:
        if kinds[u]!='TP':continue
        for v in kinds:
            if kinds[v]=='BP' and owner[v] not in local and rng.random()<.11:links.append((u,v))
    resources=set(range(rng.randrange(5)));support={o:set() for o in range(len(pairs))}
    grouped=set().union(*(v for v,e in trees))
    for o in support:
        if o in local or (unsupported and o in grouped):continue
        support[o]={j for j in resources if rng.random()<.3}
    return (kinds,pairs,links,support,resources),trees


def abstract_checks(totals):
    rng=random.Random(2026102502)
    for i in range(600):
        data,trees=random_model(rng,unsupported=i%2==0)
        compare(data,trees,totals,independent=len(trees)<=2 and len(data[1])<=10)
    # Two internally deficient trees each see the same exterior resource.
    # A per-tree reachability assertion pays two residual demands falsely.
    kinds,pairs,_=canonical('AAAABBB')
    data=(kinds,pairs,[(0,8),(3,9),(4,10),(7,11),(0,12),(4,13)],
          {o:set() for o in range(7)},set())
    trees=[({0,1},[(0,1,4)]),({2,3},[(2,3,5)])]
    result=compare(data,trees,totals,True)
    assert (result['value'],result['baseline'],result['exterior_value'])==(3,2,1)
    # Exterior beta body support and two separate BP gates remain usable
    # jointly: these two residual trees can form one genuine exterior fork.
    fork_support={o:({0} if o==6 else set()) for o in range(7)}
    repaired=(*data[:3],fork_support,{0})
    fixed=compare(repaired,trees,totals,True)
    assert (fixed['value'],fixed['cost'])==(4,4)
    # A local beta with body support is not an empty-support pocket unit:
    # its fork can pay both sources even with no exterior exit.
    k,p,_=canonical('AAB')
    invalid=(k,p,[(0,4),(3,5)],{0:set(),1:set(),2:{0}},{0})
    assert (fork_flow(*invalid)['value'],fork_flow(*invalid)['cost'])==(2,2)
    try:validate_blocks(invalid,[({0,1},[(0,1,2)])])
    except AssertionError:pass
    else:raise AssertionError('Nonempty internal beta support was not rejected.')
    totals['rejected_internal_beta_support_control']+=1
    return dict(shared_whole_beta=result,same_beta_with_body_interval=fixed,
        nonempty_internal_beta_support=dict(original_value=2,invalid_baseline_only_value=1,
            compression_hypothesis_rejected=True))


def physical_checks(totals):
    records=[]
    for name,fixture in [('outside_intervals',loose_fixture),('unsupported',tight_fixture)]:
        for q in range(1,13):
            masks=range(1<<q) if q<=5 else [0]+[(1<<s)-1 for s in range(1,q+1)]
            for mask in masks:
                filled={i for i in range(q) if mask>>i&1}
                cur,layers=fixture(q,filled)
                direct_check(*cur);check_rank_certificate(cur,layers)
                assert frozen_certificate(cur)[0]=={v for edge in cur[3] for v in edge}
                data,_,_=whole_support_data(cur,whole_bands(cur));owner,_,_,_=owner_data(*data[:2])
                blocks=[]
                for i in sorted(filled):
                    a,b,beta=(owner[8+16*i,c] for c in (4,7,5))
                    blocks.append(({a,b},[(a,b,beta)]))
                result=compare(data,blocks,totals,independent=q<=2)
                assert result['value']==2*q
                assert result['cost']==(2*len(filled) if name=='unsupported' else 0)
                assert result['simple_cost']==(2*len(filled) if name=='unsupported' else len(filled))
                records.append(dict(family=name,copies=q,filled=sorted(filled),**result))
                totals['frozen_physical_boards']+=1
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();controls=abstract_checks(totals);physical=physical_checks(totals)
    report=dict(status='PASS',totals=dict(totals),joint_controls=controls,physical=physical,
        scope='Exact full-network cardinal compression of filled pocket trees; exact simple '
        'cost when every grouped alpha has empty direct support; discounted circulation '
        'restores general exact cost. All exterior mixed/BP/beta/interval identities retained. '
        'General proofs written; no universal frozen saturation or5/6 improvement.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
