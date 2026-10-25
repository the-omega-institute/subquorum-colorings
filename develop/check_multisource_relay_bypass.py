"""Multiple source pairs, private bypasses and exact relay-capacity lifting.

The general proofs and physical adapter hypotheses are in
MULTISOURCE_RELAY_BYPASS_AND_DEFECT_BOUND.md. No solver dependency.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_two_sided_dead_escape import fixture, inspect, restrict
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_normal_form import whole_support_data
from check_whole_support_fork_flow import fork_flow
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def options(model, Q):
    D, G = model['direct'], model['gates']
    out = {a:[dict(source=a,unit=j,gate=None,cost=c)
              for j,c in D[a].items() if j in Q] for a in D}
    for g, data in G.items():
        assert 1 <= data.get('capacity',1) and len(data['entry']) <= data.get('capacity',1)+1
        for a,e in data['entry'].items():
            for j,o in data['output'].items():
                if j in Q:out[a].append(dict(source=a,unit=j,gate=g,cost=e+o))
    return out


def mincost(arcs, s, t):
    edges=[]; adj=defaultdict(list)
    def add(u,v,cap,cost,tag):
        i=len(edges);edges.extend([dict(u=u,v=v,cap=cap,initial=cap,cost=cost,tag=tag),
                                  dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        adj[u].append(i);adj[v].append(i+1)
    for arc in arcs:add(*arc)
    value=cost=0; nodes=set(adj)|{s,t}
    while True:
        dist={s:0};parent={}
        for _ in range(len(nodes)-1):
            changed=False
            for i,e in enumerate(edges):
                if e['cap'] and e['u'] in dist:
                    candidate=dist[e['u']]+e['cost']
                    if candidate<dist.get(e['v'],10**12):
                        dist[e['v']]=candidate;parent[e['v']]=i;changed=True
            if not changed:break
        if t not in dist:break
        v=t;seen=set()
        while v!=s:
            assert v not in seen;seen.add(v);i=parent[v]
            edges[i]['cap']-=1;edges[i^1]['cap']+=1;v=edges[i]['u']
        value+=1;cost+=dist[t]
    return value,cost,[e['tag'] for e in edges[::2] if e['initial']>e['cap'] and e['tag'] is not None]


def solve(model,Q,project=False):
    D,G=model['direct'],model['gates'];s=('s',);t=('t',);arcs=[]
    for a in D:arcs.append((s,('a',a),1,0,None))
    for j in Q:arcs.append((('j',j),t,1,0,None))
    if project:
        for a,choices in options(model,Q).items():
            for p in choices:arcs.append((('a',a),('j',p['unit']),1,p['cost'],p))
    else:
        for a in D:
            for j,c in D[a].items():
                if j in Q:arcs.append((('a',a),('j',j),1,c,('direct',a,j,c)))
        for g,data in G.items():
            arcs.append((('gi',g),('go',g),data.get('capacity',1),0,None))
            for a,e in data['entry'].items():arcs.append((('a',a),('gi',g),1,e,('entry',a,g,e)))
            for j,o in data['output'].items():
                if j in Q:arcs.append((('go',g),('j',j),1,o,('output',g,j,o)))
    value,cost,tags=mincost(arcs,s,t)
    if project:P=tags
    else:
        outputs=defaultdict(list)
        for z in tags:
            if z[0]=='output':outputs[z[1]].append(z[2:])
        P=[]
        for z in tags:
            if z[0]=='direct':P.append(dict(source=z[1],unit=z[2],gate=None,cost=z[3]))
            if z[0]=='entry':
                j,o=outputs[z[2]].pop();P.append(dict(source=z[1],unit=j,gate=z[2],cost=z[3]+o))
    assert len(P)==value and sum(p['cost'] for p in P)==cost
    assert len({p['source'] for p in P})==len({p['unit'] for p in P})==len(P)
    return dict(value=value,cost=cost,routes=P)


def brute(choices,enforce=True,capacities=None):
    """Independent direct recursion on named routes, without a flow network."""
    best=(0,0);count=0;capacities=capacities or {}
    def visit(i,sources,units,gates,value,cost):
        nonlocal best,count
        if i==len(sources):
            count+=1
            if (value,-cost)>(best[0],-best[1]):best=value,cost
            return
        a=sources[i];visit(i+1,sources,units,gates,value,cost)
        for p in choices[a]:
            if p['unit'] in units or (enforce and p['gate'] is not None and gates.get(p['gate'],0)>=capacities.get(p['gate'],1)):continue
            next_gates=dict(gates)
            if p['gate'] is not None:next_gates[p['gate']]=next_gates.get(p['gate'],0)+1
            visit(i+1,sources,units|{p['unit']},next_gates,value+1,cost+p['cost'])
    visit(0,list(choices),set(),{},0,0)
    return best,count


def uncovered(model,Q):
    D=model['direct'];E={}
    for g,data in model['gates'].items():
        E[g]={j for j,o in data['output'].items() if j in Q and not any(
            j in D[a] and D[a][j]<=e+o for a,e in data['entry'].items())}
    return E


def repair(model,Q,P):
    """Retain the resource set at every bypass repair; drop one only if needed."""
    P=[dict(p) for p in P];before=sum(p['cost'] for p in P);E=uncovered(model,Q)
    losses=[];swaps=0;fixed=0
    for g,data in model['gates'].items():
        using=[p for p in P if p['gate']==g]
        cap=data.get('capacity',1)
        assert len(using)<=cap+1
        if len(using)<=cap:continue
        assert {p['source'] for p in using}==set(data['entry'])
        choices=[(a,j) for a,e in data['entry'].items()
                 for j in {p['unit'] for p in using}
                 if j in model['direct'][a] and model['direct'][a][j]<=e+data['output'][j]]
        if choices:
            a,j=choices[0]
            k=next(p['unit'] for p in using if p['source']==a)
            b=next(p['source'] for p in using if p['unit']==j)
            swaps+=k!=j
            replacement=[]
            for p in using:
                if p['source']==a:replacement.append(dict(source=a,unit=j,gate=None,cost=model['direct'][a][j]))
                elif p['source']==b:replacement.append(dict(source=b,unit=k,gate=g,cost=data['entry'][b]+data['output'][k]))
                else:replacement.append(dict(p))
            assert sum(p['cost'] for p in replacement)<=sum(p['cost'] for p in using)
            assert {p['unit'] for p in replacement}=={p['unit'] for p in using}
            P=[p for p in P if p['gate']!=g]+replacement;fixed+=1
        else:
            assert {p['unit'] for p in using}<=E[g]
            # Drop the more expensive route; every other original assignment stays.
            removed=max(using,key=lambda p:p['cost']);P.remove(removed);losses.append(g)
    assert len({p['source'] for p in P})==len({p['unit'] for p in P})==len(P)
    loads=Counter(p['gate'] for p in P if p['gate'] is not None)
    assert all(n<=model['gates'][g].get('capacity',1) for g,n in loads.items())
    assert all(p in options(model,Q)[p['source']] for p in P)
    assert sum(p['cost'] for p in P)<=before
    return dict(value=len(P),cost=sum(p['cost'] for p in P),routes=P,losses=losses,swaps=swaps,fixed=fixed)


def coupled_defect_rank(model,Q):
    """Pack disjoint full input groups and c+1 DIFFERENT original units per gate."""
    E=uncovered(model,Q)
    bad=[g for g,data in model['gates'].items() if len(data['entry'])==data.get('capacity',1)+1 and len(E[g])>=data.get('capacity',1)+1]
    best=source_rank=0
    for mask in range(1<<len(bad)):
        family=[g for i,g in enumerate(bad) if mask>>i&1]
        sources=[a for g in family for a in model['gates'][g]['entry']]
        if len(sources)!=len(set(sources)):continue
        source_rank=max(source_rank,len(family))
        assigned={}
        def augment(slot,seen):
            for j in E[slot[0]]:
                if j in seen:continue
                seen.add(j)
                if j not in assigned or augment(assigned[j],seen):assigned[j]=slot;return True
            return False
        if all(augment((g,i),set()) for g in family for i in range(model['gates'][g].get('capacity',1)+1)):best=max(best,len(family))
    bound=min(source_rank,len(set().union(*(E[g] for g in bad)))//min(model['gates'][g].get('capacity',1)+1 for g in bad)) if bad else 0
    assert best<=bound<=len(bad)
    return best,dict(bad_gates=len(bad),source_group_rank=source_rank,coarse_bound=bound)


def check_model(model,Q,counts,do_brute=False):
    projected=solve(model,Q,True);actual=solve(model,Q);cert=repair(model,Q,projected['routes'])
    kappa,details=coupled_defect_rank(model,Q);nu=projected['value']
    assert len(cert['losses'])<=kappa and 2*kappa<=nu
    if all(data.get('capacity',1)==2 for data in model['gates'].values()):
        assert 3*kappa<=nu and actual['value']>=(2*nu+2)//3
    assert actual['value']>=cert['value']==nu-len(cert['losses'])>=nu-kappa
    safe=all(len(E)<=model['gates'][g].get('capacity',1) or len(model['gates'][g]['entry'])<=model['gates'][g].get('capacity',1) for g,E in uncovered(model,Q).items())
    if safe or not cert['losses']:
        assert (actual['value'],actual['cost'])==(nu,projected['cost'])
    if do_brute:
        for enforce,answer in [(False,projected),(True,actual)]:
            exact,n=brute(options(model,Q),enforce,{g:data.get('capacity',1) for g,data in model['gates'].items()})
            assert exact==(answer['value'],answer['cost'])
            counts['independent_route_packings']+=n
        counts['independent_models']+=1
    counts['models']+=1;counts['universally_safe_models']+=safe
    counts['zero_loss_projection_optima']+=not cert['losses']
    counts['strict_projection_gaps']+=actual['value']<nu
    counts['strict_cost_gaps_at_same_value']+=actual['value']==nu and actual['cost']>projected['cost']
    counts['repair_losses_recovered_by_other_full_routes']+=cert['value']<actual['value']
    counts['strict_coupled_improvement_over_bad_gate_count']+=kappa<details['bad_gates']
    return dict(projected_value=nu,projected_cost=projected['cost'],value=actual['value'],cost=actual['cost'],
                certificate_value=cert['value'],certificate_cost=cert['cost'],kappa=kappa,safe=safe,**details)


def controls(counts):
    # Covered outputs split between the two entrants; a fixed anchor is unnecessary.
    split=dict(direct={0:{0:0},1:{1:0}},gates={0:dict(entry={0:1,1:1},output={0:0,1:0})})
    P=[dict(source=0,unit=1,gate=0,cost=1),dict(source=1,unit=0,gate=0,cost=1)]
    cert=repair(split,{0,1},P);assert cert['value']==2 and cert['swaps']==1 and cert['fixed']==1
    check_model(split,{0,1},counts,True)
    # Distinct bad gates can compete for the same sources or original units.
    source_overlap=dict(direct={0:{},1:{},2:{}},gates={
        g:dict(entry={0:1,g+1:1},output={2*g:0,2*g+1:0}) for g in range(2)})
    r=check_model(source_overlap,set(range(4)),counts,True)
    assert (r['bad_gates'],r['kappa'],r['projected_value'],r['value'])==(2,1,3,2)
    resource_overlap=dict(direct={a:{} for a in range(4)},gates={
        g:dict(entry={2*g:1,2*g+1:1},output={0:0,1:0,2:0}) for g in range(2)})
    r=check_model(resource_overlap,{0,1,2},counts,True)
    assert (r['bad_gates'],r['kappa'],r['projected_value'],r['value'])==(2,1,3,2)
    cap_two=dict(direct={0:{0:0},1:{},2:{}},gates={0:dict(capacity=2,entry={0:1,1:1,2:1},output={0:0,1:0,2:0})})
    rr=check_model(cap_two,{0,1,2},counts,True);assert (rr['value'],rr['cost'],rr['safe'])==(3,2,True)
    no_cover=dict(direct={0:{},1:{},2:{}},gates=cap_two['gates'])
    rr=check_model(no_cover,{0,1,2},counts,True);assert (rr['projected_value'],rr['value'],rr['kappa'])==(3,2,1)
    # Three entrants: full coverage by one source does not remove one gate's cap.
    degree3={a:[] for a in range(3)}
    for a in degree3:
        degree3[a]=[dict(source=a,unit=j,gate=0,cost=1) for j in range(3)]
    degree3[0]+=[dict(source=0,unit=j,gate=None,cost=0) for j in range(3)]
    assert brute(degree3,False)[0]==(3,2) and brute(degree3,True)[0]==(2,1)
    # Nonseparable source/output costs: the matching swap can increase costs.
    nonseparable={0:[dict(source=0,unit=0,gate=None,cost=1)],1:[]}
    for a in (0,1):
        for j in (0,1):nonseparable[a].append(dict(source=a,unit=j,gate=0,cost=11 if a==j else 1))
    assert brute(nonseparable,False)[0]==(2,2) and brute(nonseparable,True)[0]==(2,12)
    # A purported private bypass shared between modules reuses its one capacity.
    shared={a:[] for a in range(4)};relaxed={a:[] for a in range(4)}
    for g in (0,1):
        for a in (2*g,2*g+1):
            for j in (2*g,2*g+1):
                p=dict(source=a,unit=j,gate=g,cost=1);shared[a].append(p);relaxed[a].append(p)
        for j in (2*g,2*g+1):
            shared[2*g].append(dict(source=2*g,unit=j,gate=2,cost=1))
            relaxed[2*g].append(dict(source=2*g,unit=j,gate=None,cost=1))
    assert brute(relaxed,False)[0]==(4,4) and brute(shared,True)[0]==(3,3)
    return dict(capacity_two='three entrants: two uncovered units safe; three uncovered units projection3 actual2',split_covered_outputs='repair swaps two assignments, preserves both original units',
                overlapping_bad_source_pairs='2 bad gates, coupled rank1, projection3 actual2',
                overlapping_uncovered_units='2 bad gates but3 original units, coupled rank1',
                three_entrants='coverage alone: projection3 actual2',
                nonseparable_costs='same value2, projected cost2 actual cost12',
                shared_bypass_capacity='purported private bypass reused, projection4 actual3')


def physical(counts):
    c,layers=fixture();d,pools,base=inspect(c,whole_bands(c),layers)
    owner,A,B,M=owner_data(*d[:2]);a=owner[5,13];b=owner[5,15];L,R,X,S,Y=pools
    model=dict(direct={a:{j:0 for j in L},b:{**{j:0 for j in R},**{j:1 for j in X}}},
               gates={0:dict(entry={a:1,b:1},output={**{j:0 for j in S},**{j:4 for j in Y}})})
    assert uncovered(model,d[4])[0]==Y
    safe=0;gap=0
    for sizes in itertools.product(range(3),repeat=5):
        Q=set().union(*(set(sorted(p)[:n]) for p,n in zip((S,L-S,R,X,Y),sizes)))
        result=check_model(model,Q,counts)
        real=fork_flow(*restrict(d,Q));assert (real['value'],real['cost'])==(result['value'],result['cost'])
        safe+=result['safe'];gap+=result['value']<result['projected_value']
        counts['physical_original_subset_patterns']+=1
    assert safe==162 and gap==1
    copies=[]
    for q in (2,3,5):
        cur,ls=fixture(q);direct_check(*cur);check_rank_certificate(cur,ls)
        assert frozen_certificate(cur)[0]=={v for e in cur[3] for v in e}
        di,meta,_=whole_support_data(cur,whole_bands(cur));oi,Ai,_,_=owner_data(*di[:2])
        direct={a:{j:0 for j in di[3][a]} for a in Ai};gates={};allY=set();oneY=set();shadow_plus_Y=set()
        for i in range(q):
            aa,bb=oi[5+14*i,13],oi[5+14*i,15]
            xx=di[3][oi[7+14*i,21]];ss=di[3][oi[5+14*i,14]];yy=di[3][oi[10+14*i,21]]
            direct[bb].update({j:1 for j in xx});gates[i]=dict(entry={aa:1,bb:1},output={**{j:0 for j in ss},**{j:4 for j in yy}})
            allY|=yy;oneY.add(min(yy));shadow_plus_Y|={min(ss),min(yy)}
        mm=dict(direct=direct,gates=gates)
        for label,Q in [('full',di[4]),('all_tails',allY),('one_tail_per_gate',oneY),('one_shadow_plus_tail',shadow_plus_Y)]:
            r=check_model(mm,Q,counts);real=fork_flow(*restrict(di,Q))
            assert (r['value'],r['cost'])==(real['value'],real['cost'])
            if label=='all_tails':assert (r['projected_value'],r['value'],r['kappa'])==(2*q,q,q)
            if label=='one_shadow_plus_tail':assert (r['projected_value'],r['value'],r['cost'],r['safe'])==(2*q,2*q,5*q,True)
            copies.append(dict(q=q,pool=label,**r));counts['physical_copy_pool_controls']+=1
    return dict(base=base,safe_patterns=safe,strict_gap_patterns=gap,copies=copies)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    counts=Counter();cc=controls(counts);rng=random.Random(20261025083)
    for i in range(360):
        na=rng.randrange(2,7);nj=rng.randrange(1,7);ng=rng.randrange(1,6)
        D={a:{j:rng.randrange(4) for j in range(nj) if rng.random()<.3} for a in range(na)}
        G={}
        for g in range(ng):
            capacity=rng.choice((1,1,2))
            G[g]=dict(capacity=capacity,entry={a:rng.randrange(1,4) for a in rng.sample(range(na),rng.randrange(1,min(capacity+1,na)+1))},
                      output={j:rng.randrange(4) for j in range(nj) if rng.random()<.65})
        Q={j for j in range(nj) if rng.random()<.85}
        check_model(dict(direct=D,gates=G),Q,counts,do_brute=i<65 and na<=4)
    pp=physical(counts)
    result=dict(status='PASS',counts=dict(counts),countercontrols=cc,physical=pp,
        scope='General lifting and coupled defect proofs written separately. Abstract private bypasses are assumed disjoint; countercontrol shows failure when shared. Physical application uses complete original56P26T routing, original intervals and disjoint copies; no new physical grid or universal5/6 improvement. Lean scope separate.')
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',**dict(counts))))


if __name__=='__main__':main()
