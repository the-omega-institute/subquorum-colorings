"""Exact retention after support changes, using only a normalized pack's old links.

Proof: docs/OLD_LINK_BATCH_REPAIR.md. The production repair does not enumerate
primitives or invoke flow/blossom. Independent optimizers are audit-only.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import canonical, primitive_certificates, optimize
from check_whole_support_fork_flow import fork_flow
from check_destructive_exchange_choice import constrained_optimum, subsets
from check_P_free_pivot_interface import regions, family
from check_degree_changing_bent_completions import compile_model
from check_fully_frozen_elbow_withdrawal import configuration_one
from check_fixed_P_maximum_frozen_elbow import fixture
from check_canonical_band_coarsening import random_board
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_frozen_coordinated_pivots import family as coordinated_family

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def allocation(neighbours, mandatory=frozenset()):
    """Parent-edge construction, with an explicit deficient-tree certificate."""
    demands=set(neighbours);assert mandatory<=demands
    users=defaultdict(set)
    for d,units in neighbours.items():
        for j in units:users[j].add(d)
    assert all(1<=len(ds)<=2 for ds in users.values())
    adjacency=defaultdict(list)
    for j,ds in users.items():
        if len(ds)==2:
            x,y=sorted(ds);adjacency[x].append((y,j));adjacency[y].append((x,j))
    unseen=set(demands);matched={};components=[];infeasible=[]
    while unseen:
        seed=min(unseen);vertices={seed};todo=[seed];tree=set()
        while todo:
            x=todo.pop()
            for y,j in adjacency[x]:
                if y not in vertices:vertices.add(y);todo.append(y);tree.add(j)
        unseen-=vertices
        units=set().union(set(),*(neighbours[d] for d in vertices))
        extras=units-tree
        deficient=not extras
        if deficient:
            choices=vertices-mandatory
            root=min(choices or vertices)
            if not choices:infeasible.append(dict(demands=sorted(vertices),resources=sorted(units)))
            reserve=None
        else:
            reserve=min(extras);root=min(users[reserve])
        reached={root};todo=[root]
        while todo:
            x=todo.pop()
            for y,j in adjacency[x]:
                if j in tree and y not in reached:
                    reached.add(y);todo.append(y);matched[y]=j
        assert reached==vertices
        if reserve is not None:matched[root]=reserve
        assert len(units)==len(vertices)-1 if deficient else len(units)>=len(vertices)
        components.append(dict(demands=sorted(vertices),resources=sorted(units),
            deficient=deficient,root=root))
    assert len(set(matched.values()))==len(matched)
    assert all(j in neighbours[d] for d,j in matched.items())
    return dict(matching=matched,components=components,infeasible=infeasible,
        deficiency=sum(c['deficient'] for c in components))


def repair(data, pack, required=frozenset(), new_sources=frozenset()):
    """Retain as many old paid sources as possible, adding no physical link.

    data is the NEW support model; pack is an OLD owner-disjoint normalized
    primitive pack on the same owners and links. No common old/new unit IDs
    are needed. Each new unit must have at most two distinct owner users.
    """
    kinds,pairs,links,W,Q=data;own,A,B,X=owner_data(kinds,pairs)
    assert all(S<=Q for S in W.values())
    assert all(n<=2 for n in Counter(j for S in W.values() for j in S).values())
    ps=list(pack['certificates']);used=[o for p in ps for o in p['owners']]
    assert len(used)==len(set(used))
    old_paid=set(used)&A;assert new_sources<=A-old_paid
    paid=old_paid|new_sources;assert required<=paid
    oldlinks={e for p in ps for e in p['links']};assert oldlinks<=set(links)
    ps.extend(dict(kind='interval',owners=(a,),links=(),interval=None,value=1,witness=a)
        for a in sorted(new_sources))
    arms={};neighbours={};mandatory=set()
    for i,p in enumerate(ps):
        sources=set(p['owners'])&A
        assert len(sources)==p['value']
        outgoing={own[u]:(u,v) for u,v in p['links']}
        assert len(outgoing)==len(p['links'])
        for a in sorted(sources):
            owners=[a];edges=[]
            while owners[-1] in outgoing:
                edge=outgoing[owners[-1]];edges.append(edge);owners.append(own[edge[1]])
                assert len(owners)==len(set(owners))
            arms[i,a]=(owners,edges)
        if p['kind']=='beta':
            assert len(sources)==1 and set(p['owners'])&B=={p['beta']}
            continue
        assert p['kind'] in ('interval','fork')
        assert len(sources)==(2 if p['kind']=='fork' else 1)
        neighbours[i]=set().union(set(),*(W[o] for o in p['owners']))
        if sources<=required:mandatory.add(i)
    ledger=allocation(neighbours,mandatory)
    if ledger['infeasible']:
        return dict(feasible=False,ledger=ledger)
    result=[]
    def stem(i,a,stop=None,unit=None):
        os,es=arms[i,a]
        if stop is None:
            return dict(kind='beta',owners=tuple(sorted(os)),links=tuple(es),
                interval=None,value=1,beta=os[-1])
        at=os.index(stop)
        return dict(kind='interval',owners=tuple(sorted(os[:at+1])),links=tuple(es[:at]),
            interval=unit,value=1,witness=stop)
    for i,p in enumerate(ps):
        sources=set(p['owners'])&A
        if p['kind']=='beta':result.append(dict(p));continue
        if i not in ledger['matching']:
            if p['kind']=='fork':
                a=min((sources&required) or sources);result.append(stem(i,a))
            continue
        unit=ledger['matching'][i]
        witness=min(o for o in p['owners'] if unit in W[o])
        if p['kind']=='interval':
            result.append(stem(i,next(iter(sources)),witness,unit))
        elif witness==p['beta']:
            result.append(dict(p,interval=unit))
        else:
            a=next(a for a in sources if witness in arms[i,a][0]);other=next(iter(sources-{a}))
            result.extend((stem(i,a,witness,unit),stem(i,other)))
    owners=[o for p in result for o in p['owners']]
    units=[p['interval'] for p in result if p['interval'] is not None]
    chosen=[e for p in result for e in p['links']]
    retained=set(owners)&A
    assert len(owners)==len(set(owners)) and len(units)==len(set(units))
    assert set(chosen)<=oldlinks and required<=retained<=paid
    assert len(paid-retained)==ledger['deficiency']
    return dict(feasible=True,value=len(retained),cost=len(chosen),paid=sorted(retained),
        loss=len(old_paid-retained),new_paid=sorted(retained&new_sources),gain=len(retained)-len(old_paid),
        links=chosen,certificates=result,ledger=ledger)


def signature(p):
    return (p['kind'],tuple(sorted(p['owners'])),tuple(sorted(p['links'])),
        p['interval'],p['value'],p.get('witness'),p.get('beta'))


def audit(data,pack,counts,required_checks=True,new_sources=frozenset()):
    answer=repair(data,pack,new_sources=new_sources);assert answer['feasible']
    candidates={signature(p) for p in primitive_certificates(*data)}
    assert all(signature(p) in candidates for p in answer['certificates'])
    kinds,pairs,_,W,Q=data;_,A,_,_=owner_data(kinds,pairs)
    owners=set().union(set(new_sources),*(set(p['owners']) for p in pack['certificates']))
    paid=owners&A;links=[e for p in pack['certificates'] for e in p['links']]
    restricted=kinds,pairs,links,{o:S if o in owners else set() for o,S in W.items()},Q
    independent=optimize(*restricted)
    assert independent['value']==answer['value']
    counts['independent_old_link_optima']+=1
    counts['old_beta_forks']+=sum(p['kind']=='fork' for p in pack['certificates'])
    counts['deficient_tree_components']+=answer['ledger']['deficiency']
    counts['new_direct_source_payments']+=len(answer['new_paid'])
    counts['prefix_link_savings']+=len(links)-answer['cost']
    for R in subsets(paid) if required_checks else (set(),paid):
        constrained=repair(data,pack,R,new_sources);expected=constrained_optimum(restricted,R)
        assert constrained['feasible']==(expected is not None)
        if expected is not None:assert constrained['value']==expected[0]==answer['value']
        else:
            for c in constrained['ledger']['infeasible']:
                assert len(c['resources'])==len(c['demands'])-1
        counts['prescribed_old_source_sets']+=1
        counts['infeasible_prescriptions']+=expected is None
    return answer


def controls(counts):
    # Old endpoint witness loses support; an earlier mixed prefix saves payment.
    kinds,pairs,_=canonical('AMM')
    old=(kinds,pairs,[(0,2),(3,4)],{0:set(),1:set(),2:{0}},{0})
    pack=optimize(*old);new=(*old[:3],{0:set(),1:{0},2:set()},{0})
    answer=audit(new,pack,counts)
    assert answer['value']==1 and answer['cost']==1
    assert not new[3][pack['certificates'][0]['witness']]
    # A fork can split before its beta and still pay both old sources.
    kinds,pairs,_=canonical('AAMB')
    old=(kinds,pairs,[(0,4),(5,6),(2,7)],{0:set(),1:set(),2:set(),3:{0}},{0})
    pack=optimize(*old);assert pack['certificates'][0]['kind']=='fork'
    new=(*old[:3],{0:set(),1:set(),2:{0},3:set()},{0})
    answer=audit(new,pack,counts)
    assert answer['value']==2 and answer['cost']==2
    assert sorted(p['kind'] for p in answer['certificates'])==['beta','interval']
    # A shared reserve cannot be credited to both old primitives. An unrelated
    # spare unit changes the total inventory, but does not repair the tree.
    kinds,pairs,_=canonical('AA')
    old=(kinds,pairs,[],{0:{0},1:{1}},{0,1})
    new=(*old[:3],{0:{0},1:{0}},{0,1})
    answer=audit(new,optimize(*old),counts)
    assert answer['value']==1 and answer['loss']==1
    # Two parallel original units pay both: capacity-two is not one token.
    answer=audit(old,optimize(*old),counts);assert answer['value']==2
    parallel=(*old[:3],{0:{0,1},1:{0,1}},{0,1})
    answer=audit(parallel,optimize(*old),counts);assert answer['value']==2
    # New physical links can repair a tree: old-link optimality is restricted.
    kinds,pairs,_=canonical('AAM')
    old=(kinds,pairs,[(2,4)],{0:{0},1:{1},2:set()},{0,1})
    pack=optimize(*old);assert pack['cost']==0
    new=(*old[:3],{0:{0},1:{0},2:{1}},{0,1})
    answer=audit(new,pack,counts)
    assert answer['value']==1 and optimize(*new)['value']==2
    # A newly paid direct alpha can merely displace an old mixed-stem source.
    kinds,pairs,_=canonical('AAM')
    old=(kinds,pairs,[(0,4)],{0:set(),1:set(),2:{0}},{0})
    pack=optimize(*old);new=(*old[:3],{0:set(),1:{0},2:{0}},{0})
    answer=audit(new,pack,counts,new_sources={1})
    assert answer['value']==1 and answer['gain']==0
    assert repair(new,pack,{0,1},{1})['feasible'] is False
    assert repair(new,pack,{1},{1})['new_paid']==[1]
    # A second actual resource turns the competing pair into a cycle and
    # yields a strict compensation gain with the old source retained.
    new=(*old[:3],{0:set(),1:{0,1},2:{0,1}},{0,1})
    answer=audit(new,pack,counts,new_sources={1})
    assert answer['gain']==1 and repair(new,pack,{0,1},{1})['feasible']
    # Cardinality is exact; the simple construction need not minimize links.
    kinds,pairs,_=canonical('AAB')
    old=(kinds,pairs,[(0,4),(2,5)],{0:set(),1:set(),2:{0}},{0})
    pack=optimize(*old);new=(*old[:3],{0:{0},1:{1},2:set()},{0,1})
    answer=audit(new,pack,counts)
    assert answer['value']==2 and answer['cost']==1 and optimize(*new)['cost']==0
    counts['targeted_controls']=9
    # Production API must not call either independent enumerator or full flow.
    saved={name:globals()[name] for name in ('primitive_certificates','optimize','constrained_optimum','fork_flow')}
    def forbidden(*args,**kwargs):raise AssertionError('repair must use only the resource graph')
    try:
        for name in saved:globals()[name]=forbidden
        assert repair(new,pack)['value']==2
    finally:globals().update(saved)
    counts['no_enumeration_api_controls']+=1


def physical(counts,rng):
    records=[]
    cases=[]
    for m in (0,3):
        cur,bits,ranks=family(m);cases.append(('frozen-support-loss',cur,bits,ranks))
    cur,bits,ranks=configuration_one();cases.append(('frozen-elbow',cur,bits,ranks))
    raw=fixture();cur,bits=raw[:2];cases.append(('fixed-P-maximum',cur,bits,None))
    for _ in range(18):
        cur=random_board(6,8,rng)
        bits={(r,c):bool(rng.getrandbits(1)) for r in range(0,cur[0],2) for c in range(0,cur[1],2)}
        cases.append(('random-mixed',cur,bits,None))
    for name,cur,bits,ranks in cases:
        direct_check(*cur);P={v for e in cur[3] for v in e}
        if ranks is not None:
            assert frozen_certificate(cur)[0]==P
            counts['strict_freezing_events']+=len(check_rank_certificate(cur,ranks))
        old,closed,_=compile_model(cur,regions(cur,bits));pack=fork_flow(*old)
        gates=[g for g in bits if not {(g[0]+i,g[1]+j) for i,j in itertools.product(range(2),repeat=2)}&P]
        choices=[set(),set(gates),set(gates[::2])]
        if name=='frozen-support-loss':choices.append({(2,16)})
        choices += [set(rng.sample(gates,min(len(gates),rng.randrange(1,6)))) for _ in range(8)]
        for chosen in choices:
            changed={g:not v if g in chosen else v for g,v in bits.items()}
            new,nclosed,_=compile_model(cur,regions(cur,changed))
            assert old[:2]==new[:2] and set(old[2])==set(new[2])
            assert [x['body'] for x in closed]==[x['body'] for x in nclosed]
            answer=audit(new,pack,counts)
            old_paid=set().union(set(),*(set(p['owners']) for p in pack['certificates']))&owner_data(*new[:2])[1]
            audit(new,pack,counts,new_sources=owner_data(*new[:2])[1]-old_paid)
            counts['mixed_target_batches']+=len({changed[g] for g in chosen})==2
            counts['physical_support_change_batches']+=1
            counts['physical_old_link_losses']+=answer['loss']
            if name=='frozen-support-loss' and chosen=={(2,16)}:
                assert pack['value']==2 and answer['value']==1 and fork_flow(*new)['value']==1
                records.append(dict(name=name,shape=list(cur[:2]),pivot=[2,16],old_value=2,
                    old_link_retention=1,unrestricted_new_value=1,loss=1))
    for n in (2,9):
        cur,bits,ranks,gates=coordinated_family(n)
        direct_check(*cur);P={v for e in cur[3] for v in e}
        assert frozen_certificate(cur)[0]==P
        counts['strict_freezing_events']+=len(check_rank_certificate(cur,ranks))
        old,_,_=compile_model(cur,regions(cur,bits));pack=fork_flow(*old)
        changed=dict(bits)
        for g in gates:changed[g]=False
        new,_,_=compile_model(cur,regions(cur,changed))
        _,A,_,_=owner_data(*old[:2])
        old_paid=set().union(set(),*(set(p['owners']) for p in pack['certificates']))&A
        answer=audit(new,pack,counts,new_sources=A-old_paid)
        assert pack['value']==1 and answer['value']==2 and answer['cost']==1 and answer['gain']==1
        records.append(dict(name='frozen-joint-gate-compensation',shape=list(cur[:2]),
            gates=n,old_value=1,new_value_without_new_links=2,old_sources_retained=True,
            links=1,strict_frozen_endpoints=70))
    return records


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();counts=Counter();rng=random.Random(2026102647)
    controls(counts)
    for _ in range(160):
        kinds,pairs,links=canonical(rng.choice(('AAAMM','AAAAB','AAABMM','AAAABB')))
        rng.shuffle(links);links=links[:rng.randrange(min(len(links),9)+1)]
        Q=set(range(rng.randrange(1,6)));W={o:set() for o in range(len(pairs))}
        for j in Q:
            for o in rng.sample(list(W),rng.randrange(3)):W[o].add(j)
        old=kinds,pairs,links,W,Q;pack=optimize(*old)
        newW={o:set() for o in W}
        for j in Q:
            for o in rng.sample(list(W),rng.randrange(3)):newW[o].add(j)
        new=kinds,pairs,links,newW,Q
        audit(new,pack,counts)
        old_paid=set().union(set(),*(set(p['owners']) for p in pack['certificates']))&owner_data(kinds,pairs)[1]
        audit(new,pack,counts,new_sources=owner_data(kinds,pairs)[1]-old_paid)
        counts['generic_support_changes']+=1
    # Audit the theorem on nonoptimal old packs too, including the empty pack.
    for _ in range(24):
        kinds,pairs,links=canonical('AAMB');rng.shuffle(links);links=links[:4]
        Q={0,1};W={o:set() for o in range(len(pairs))};newW={o:set() for o in W}
        for support in (W,newW):
            for j in Q:
                for o in rng.sample(list(W),rng.randrange(3)):support[o].add(j)
        candidates=primitive_certificates(kinds,pairs,links,W,Q)
        def visit(start,owners,used,ps):
            pack=dict(certificates=list(ps),value=sum(p['value'] for p in ps))
            audit((kinds,pairs,links,newW,Q),pack,counts,required_checks=False)
            counts['all_compatible_old_packs']+=1
            for i in range(start,len(candidates)):
                p=candidates[i];unit=set() if p['interval'] is None else {p['interval']}
                if not owners&set(p['owners']) and not used&unit:
                    visit(i+1,owners|set(p['owners']),used|unit,ps+[p])
        visit(0,set(),set(),[])
    records=physical(counts,rng)
    assert counts['old_beta_forks'] and counts['deficient_tree_components'] and counts['mixed_target_batches']
    report=dict(status='PASS',counts=dict(counts),physical_loss_controls=records,
        proof='docs/OLD_LINK_BATCH_REPAIR.md',
        scope='Exact retained old sources plus specified newly eligible direct sources with subsets of a fixed normalized pack\'s old links. Source prescriptions and no repeated original resources. Enumeration is only an independent audit.',
        limitations=['Not a universal grid bound.','Not the optimum when new physical links are permitted.','No minimum-link optimality claim among maximum repairs.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2))


if __name__=='__main__':main()
