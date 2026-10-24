"""Complete cost/reserve frontier by terminal exchanges in a residual flow.

Independent reservation/primitive optimizations check the reduction; they
are not its general proof. The existing full-flow solver is unchanged.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_even_bridge_support_completion import endpoints_of
from check_frozen_beta_support_fork import fixture, stacked
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_simultaneous_interval_release import delete, fixed_paid_model, sectors, subsets
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical, optimize, whole_support_data

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


class Network:
    def __init__(self):
        self.edges=[]
        self.nodes=set()

    def add(self,u,v,capacity,cost=0,tag=None):
        index=len(self.edges)
        self.edges.extend([dict(u=u,v=v,cap=capacity,initial=capacity,cost=cost,tag=tag),
                           dict(u=v,v=u,cap=0,initial=0,cost=-cost,tag=None)])
        self.nodes|={u,v}
        return index

    def send(self,index,amount=1):
        assert self.edges[index]['cap']>=amount
        self.edges[index]['cap']-=amount
        self.edges[index^1]['cap']+=amount

    def augment(self,source,sink):
        distance={source:0};parent={}
        for _ in range(len(self.nodes)-1):
            changed=False
            for i,e in enumerate(self.edges):
                if e['cap'] and e['u'] in distance:
                    d=distance[e['u']]+e['cost']
                    if e['v'] not in distance or d<distance[e['v']]:
                        distance[e['v']]=d;parent[e['v']]=i;changed=True
            if not changed:break
        if sink not in distance:return None
        path=[];v=sink;seen=set()
        while v!=source:
            assert v not in seen;seen.add(v)
            i=parent[v];path.append(i);v=self.edges[i]['u']
        for i in path:self.send(i)
        return distance[sink]

    def potentials(self):
        # Distances from a virtual zero-cost source joined to every node.
        distance={v:0 for v in self.nodes}
        for turn in range(len(self.nodes)):
            changed=False
            for e in self.edges:
                if e['cap'] and distance[e['v']]>distance[e['u']]+e['cost']:
                    distance[e['v']]=distance[e['u']]+e['cost'];changed=True
            if not changed:break
            assert turn<len(self.nodes)-1,'Negative residual cycle'
        assert all(e['cost']+distance[e['u']]-distance[e['v']]>=0
                   for e in self.edges if e['cap'])
        return distance

    def reachable(self,source):
        seen={source};todo=[source];adj=defaultdict(list)
        for e in self.edges:
            if e['cap']:adj[e['u']].append(e['v'])
        while todo:
            u=todo.pop()
            for v in adj[u]:
                if v not in seen:seen.add(v);todo.append(v)
        return seen


def build(data):
    kinds,pairs,links,support,resources=data
    owner,alphas,betas,mixed=owner_data(kinds,pairs)
    graph=Network();source=('source',);sink=('sink',);terminals={}
    graph.nodes|={source,sink}
    exit_node=lambda o:('alpha',o) if o in alphas else ('out',o) if o in mixed else ('beta',o)
    for a in sorted(alphas):graph.add(source,exit_node(a),1,tag=('source',a))
    for m in sorted(mixed):graph.add(('in',m),exit_node(m),1,tag=('mixed',m))
    for b in sorted(betas):
        for tip in pairs[b]:graph.add(('tip',tip),exit_node(b),1,tag=('tip',tip))
        terminals['beta',b]=graph.add(exit_node(b),sink,1,tag=('beta',b))
    for j in sorted(resources):
        terminals['interval',j]=graph.add(('interval',j),sink,1,tag=('interval',j))
    large=len(alphas)+1
    for u,v in sorted(set(links)):
        if owner[u]!=owner[v]:
            assert kinds[u]=='TP' and kinds[v]=='BP'
            entry=('tip',v) if owner[v] in betas else ('in',owner[v])
            graph.add(exit_node(owner[u]),entry,large,1,('link',u,v))
    for o in sorted(support):
        for j in sorted(support[o]):
            graph.add(exit_node(o),('interval',j),large,tag=('access',o,j))
    value=cost=0
    while (extra:=graph.augment(source,sink)) is not None:
        value+=1;cost+=extra
    expected=fork_flow(*data)
    assert (value,cost)==(expected['value'],expected['cost'])
    assert value==len(alphas),'Restrict to a fully payable fixed source set first.'
    # Put the actual edge flow, not just its displayed certificate, into the
    # private-beta-first normal form. The adjustment has original cost zero.
    for b in betas:
        i=terminals['beta',b]
        if graph.edges[i]['cap']==0:continue
        access=[j for j,e in enumerate(graph.edges) if j%2==0
                and e['u']==exit_node(b) and e['tag'][0]=='access'
                and e['initial']>e['cap']]
        if access:
            j=access[0];unit=graph.edges[j]['tag'][2]
            graph.send(j^1);graph.send(terminals['interval',unit]^1);graph.send(i)
    graph.potentials()
    validate(graph,source,sink,value,cost)
    return graph,source,sink,terminals,value,cost


def validate(graph,source,sink,value,cost,flows=None):
    if flows is None:flows=[e['initial']-e['cap'] for e in graph.edges[::2]]
    balance=Counter();actual_cost=0
    for e,amount in zip(graph.edges[::2],flows):
        assert 0<=amount<=e['initial']
        balance[e['u']]+=amount;balance[e['v']]-=amount
        actual_cost+=amount*e['cost']
    assert balance[source]==value and balance[sink]==-value
    assert all(v in (source,sink) or n==0 for v,n in balance.items())
    assert actual_cost==cost
    assert all(amount==1 for e,amount in zip(graph.edges[::2],flows)
               if e['tag'][0]=='source')


def exchange_network(base,F,zero_only=False,potential=None):
    graph,source,sink,terminals,value,cost=base
    if potential is None:potential=graph.potentials()
    assert all(e['cost']+potential[e['u']]-potential[e['v']]>=0
               for e in graph.edges if e['cap'])
    auxiliary=Network();start=('release-start',);end=('release-end',)
    auxiliary.nodes|={start,end}
    for i,e in enumerate(graph.edges):
        if e['cap'] and e['u']!=sink and e['v']!=sink:
            reduced=e['cost']+potential[e['u']]-potential[e['v']]
            if not zero_only or reduced==0:
                auxiliary.add(e['u'],e['v'],e['cap'],0 if zero_only else e['cost'],('residual',i))
    used={unit for unit,i in terminals.items() if graph.edges[i]['cap']==0}
    candidates={('interval',j) for j in F}
    for unit in sorted(used&candidates):
        i=terminals[unit];v=graph.edges[i]['u']
        reduced=potential[sink]-potential[v]
        assert reduced>=0
        if not zero_only or reduced==0:
            auxiliary.add(start,v,1,tag=('release',i))
    for unit in sorted(set(terminals)-used-candidates):
        i=terminals[unit];v=graph.edges[i]['u']
        reduced=potential[v]-potential[sink]
        assert reduced>=0
        if not zero_only or reduced==0:
            auxiliary.add(v,end,1,tag=('receive',i))
    return auxiliary,start,end,len(F)-len(used&candidates),used


def profile(base,F,totals,lift=True):
    original,source,sink,terminals,p,cost=base
    auxiliary,start,end,old_unused,used=exchange_network(base,F)
    values=[0];marginals=[];negative_reverse_uses=0
    while (extra:=auxiliary.augment(start,end)) is not None:
        assert extra>=0
        marginals.append(extra);values.append(values[-1]+extra)
        assert marginals==sorted(marginals)
        if lift:
            flows=[e['initial']-e['cap'] for e in original.edges[::2]]
            for e in auxiliary.edges[::2]:
                amount=e['initial']-e['cap'];kind,i=e['tag']
                if kind=='residual':
                    flows[i//2]+=amount*(1 if i%2==0 else -1)
                    negative_reverse_uses+=bool(amount and original.edges[i]['cost']<0)
                else:flows[i//2]+=amount*(-1 if kind=='release' else 1)
            validate(original,source,sink,p,cost+values[-1],flows)
            new_used={unit for unit,i in terminals.items() if flows[i//2]}
            before={('interval',j) for j in F}&used
            after={('interval',j) for j in F}&new_used
            assert after<=before and len(before)-len(after)==len(values)-1
            totals['lifted_capacity_conservation_cost_and_identity_checks']+=1
    zero,start0,end0,_,_=exchange_network(base,F,True)
    zero_value=0
    while zero.augment(start0,end0) is not None:zero_value+=1
    side=zero.reachable(start0)
    cut=sum(e['initial'] for e in zero.edges[::2] if e['u'] in side and e['v'] not in side)
    assert end0 not in side and cut==zero_value
    assert zero_value==sum(v==0 for v in values[1:])
    totals['cost_profile_models']+=1
    totals['zero_reduced_cost_cut_certificates']+=1
    totals['profiles_using_negative_reverse_links']+=bool(negative_reverse_uses)
    return dict(initial_unused=old_unused,additional_release_minimum_cost=values,
                zero_cost_additional_release=zero_value,zero_cost_cut_capacity=cut,
                reverse_link_uses_in_lifts=negative_reverse_uses)


def alternate_zero_cost_root(base):
    original,source,sink,terminals,p,cost=base
    for unit,i in sorted(terminals.items()):
        if unit[0]!='interval' or original.edges[i]['cap']!=0:continue
        auxiliary,start,end,_,_=exchange_network(base,{unit[1]},True)
        if auxiliary.augment(start,end) is None:continue
        flows=[e['initial']-e['cap'] for e in original.edges[::2]]
        for e in auxiliary.edges[::2]:
            amount=e['initial']-e['cap'];kind,j=e['tag']
            if kind=='residual':flows[j//2]+=amount*(1 if j%2==0 else -1)
            else:flows[j//2]+=amount*(-1 if kind=='release' else 1)
        reroot=Network();reroot.nodes=set(original.nodes)
        reroot.edges=[dict(e) for e in original.edges]
        for j,amount in enumerate(flows):
            reroot.edges[2*j]['cap']=reroot.edges[2*j]['initial']-amount
            reroot.edges[2*j+1]['cap']=amount
        validate(reroot,source,sink,p,cost);reroot.potentials()
        assert reroot.edges[i]['cap']==1
        return reroot,source,sink,terminals,p,cost
    return None


def direct_costs(data,F,p,totals,independent=False):
    costs={}
    for H in subsets(F):
        f=fork_flow(*delete(data,H))
        if independent:
            other=optimize(*delete(data,H))
            assert (f['value'],f['cost'])==(other['value'],other['cost'])
            totals['independent_primitive_reservation_comparisons']+=1
        costs[H]=f['cost'] if f['value']==p else None
        totals['direct_resource_reservation_models']+=1
    return costs


def check_profile(result,costs,F,base_cost,totals):
    for r in range(len(F)+1):
        choices=[c for H,c in costs.items() if H<=F and len(H)>=r and c is not None]
        direct=min(choices) if choices else None
        h=max(0,r-result['initial_unused'])
        predicted=base_cost+result['additional_release_minimum_cost'][h] if h<len(result['additional_release_minimum_cost']) else None
        assert predicted==direct,(r,result,predicted,direct)
        totals['exact_cost_at_requested_release_comparisons']+=1


def abstract_checks(totals):
    rng=random.Random(20261102);reverse_example=None
    for index in range(360):
        kinds,pairs,possible=canonical('AA'+''.join(rng.choice('ABM') for _ in range(rng.randrange(1,7))))
        rng.shuffle(possible);resources=set(range(rng.randrange(6)))
        support={o:set() for o in range(len(pairs))}
        for j in resources:
            for o in rng.sample(range(len(pairs)),rng.randrange(min(2,len(pairs))+1)):support[o].add(j)
        data,p=fixed_paid_model((kinds,pairs,possible[:rng.randrange(min(16,len(possible))+1)],support,resources))
        base=build(data)
        costs=direct_costs(data,resources,p,totals,index<48)
        for F in subsets(resources):
            result=profile(base,F,totals)
            check_profile(result,costs,F,base[-1],totals)
            if result['reverse_link_uses_in_lifts'] and reverse_example is None:
                reverse_example=dict(kinds=data[0],pairs=data[1],links=data[2],
                    support={str(o):sorted(w) for o,w in data[3].items()},resources=sorted(resources),
                    candidates=sorted(F),profile=result)
        if index<80 and (alternative:=alternate_zero_cost_root(base)) is not None:
            for F in subsets(resources):
                result=profile(alternative,F,totals)
                check_profile(result,costs,F,base[-1],totals)
                totals['different_optimal_baseline_candidate_checks']+=1
        totals['abstract_fixed_paid_systems']+=1
    assert reverse_example is not None
    return reverse_example


def explicit_controls(totals):
    kinds,pairs,_=canonical('AABB')
    data=(kinds,pairs,[(0,4),(2,5),(2,6)],{0:{0},1:set(),2:set(),3:set()},{0})
    base=build(data);result=profile(base,{0},totals)
    assert result['additional_release_minimum_cost']==[0,1]
    assert result['reverse_link_uses_in_lifts']>0
    wrong,start,end,_,_=exchange_network(base,{0})
    for e in wrong.edges[::2]:
        if e['tag'][0]=='residual' and base[0].edges[e['tag'][1]]['cost']<0:e['cap']=0
    assert wrong.augment(start,end) is None
    expected=optimize(*delete(data,{0}))
    assert (expected['value'],expected['cost'])==(2,2)
    reverse=dict(types='AABB',links=data[2],support={'A':[0]},baseline_cost=1,
        exact_extra_cost=1,without_reverse_links='No auxiliary path',profile=result)
    kinds,pairs,_=canonical('AB')
    data=(kinds,pairs,[(0,2)],{0:{0},1:set()},{0})
    base=build(data);graph,source,sink,terminals,p,cost=base
    pi={v:0 for v in graph.nodes}
    for v in (source,('alpha',0),('interval',0)):pi[v]=-1
    zero,start,end,_,_=exchange_network(base,{0},True,pi)
    assert zero.augment(start,end) is None
    # Deliberately omit the positive represented reverse-sink gate. The
    # remaining zero-internal-cost path then gives the false free release.
    zero.add(start,('interval',0),1)
    assert zero.augment(start,end)==0
    expected=optimize(*delete(data,{0}))
    assert (expected['value'],expected['cost'])==(1,1)
    gate=dict(types='AB',link=[0,2],baseline_cost=0,exact_extra_cost=1,
        internal_zero_cost_path=True,represented_reverse_sink_reduced_cost=1,
        correct_zero_capacity=0,incorrect_capacity_without_terminal_test=1)
    totals['explicit_reverse_and_terminal_gate_rule_obstructions']+=2
    return dict(reverse_link=reverse,terminal_potential=gate)


def physical_base(totals):
    current,_=fixture();direct_check(*current)
    assert frozen_certificate(current)[0]==endpoints_of(current)
    data,_,_=whole_support_data(current,whole_bands(current));base=build(data)
    group,_=sectors(data);aw,cw,bw=group;F=aw|cw|bw
    costs=direct_costs(data,F,3,totals,True)
    chosen={}
    for K in subsets(F):
        result=profile(base,K,totals)
        check_profile(result,costs,K,1,totals)
        totals['physical_candidate_sets']+=1
        for name,w in [('C_pocket',cw),('A_and_C_support',aw|cw),('eleven_unit_sector',F)]:
            if K==w:chosen[name]=result
    alternative=alternate_zero_cost_root(base)
    assert alternative is not None
    for K in (cw,aw|cw,F,{min(aw)}):
        result=profile(alternative,K,totals)
        check_profile(result,costs,K,1,totals)
        totals['different_optimal_baseline_candidate_checks']+=1
    assert chosen['C_pocket']['initial_unused']==1
    assert chosen['C_pocket']['additional_release_minimum_cost']==[0,1]
    assert chosen['A_and_C_support']['initial_unused']==5
    assert chosen['A_and_C_support']['additional_release_minimum_cost']==[0,1,2]
    assert chosen['eleven_unit_sector']['initial_unused']==9
    assert chosen['eleven_unit_sector']['additional_release_minimum_cost']==[0,1]
    return chosen


def stack_checks(totals):
    records=[]
    for q in range(1,17):
        current=stacked(q);direct_check(*current)
        assert frozen_certificate(current)[0]==endpoints_of(current)
        data,_,_=whole_support_data(current,whole_bands(current));base=build(data)
        groups=[sectors(data,lambda v,i=i:(v[0]+16*i,v[1]))[0] for i in range(q)]
        for name,F,old,steps in [
            ('C_pockets',set().union(*(w[1] for w in groups)),q,q),
            ('A_and_C_support',set().union(*(w[0]|w[1] for w in groups)),5*q,2*q),
            ('eleven_unit_sectors',set().union(*(set().union(*w) for w in groups)),9*q,q)]:
            result=profile(base,F,totals)
            assert result['initial_unused']==old
            assert result['additional_release_minimum_cost']==list(range(steps+1))
            assert result['zero_cost_additional_release']==0
            records.append(dict(copies=q,family=name,**result))
            totals['physical_stack_candidate_sets']+=1
    return records


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args();totals=Counter()
    explicit=explicit_controls(totals);abstract=abstract_checks(totals)
    print(json.dumps(dict(stage='abstract',totals=dict(totals))),flush=True)
    physical=physical_base(totals);stacks=stack_checks(totals)
    report=dict(status='PASS',totals=dict(totals),explicit_rule_obstructions=explicit,
        seeded_negative_reverse_link_control=abstract,
        physical_cost_profiles=physical,physical_stacks=stacks,
        scope='Written general residual terminal-exchange reduction for exact additional-link '
              'cost at every simultaneous reserve target, with a fixed paid-source set and '
              'an optimal baseline; zero reduced-cost cut gives unchanged-link capacity. '
              'Independent full reservation/primitive optima, actual lifted flows, and finite '
              'physical stack controls support the proof; no universal geometric bound claimed.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))),flush=True)


if __name__=='__main__':main()
