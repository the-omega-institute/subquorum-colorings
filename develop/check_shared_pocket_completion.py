"""Solver-free physical completion and simultaneous pocket-resource accounting.

The all-size proofs are in SHARED_POCKET_COMPLETION_AND_JOINT_DEFICIT.md.
The graph formulas use established two-owner allocation; optional Z3 only
supplies a concrete initial board and is not imported by this verifier.
"""
import argparse
from collections import Counter,defaultdict,deque
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_beta_support_fork import restrict
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_neutral_portal_strip_compensation import image_map
from check_one_sided_interval_allocation import allocate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check,transformed
from check_whole_support_fork_normal_form import whole_support_data,canonical,optimize,ordinary_flow
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Run without -O; assertions required.')
FIXTURE=Path(__file__).parent/'fixtures/frozen_shared_pocket.json'


def fixture(copies=1,filled=frozenset(),padding=0):
    assert copies>=1 and set(filled)<=set(range(copies)) and padding>=0 and padding%2==0
    j=json.loads(FIXTURE.read_text());moves=[lambda v,i=i:(v[0]+16*i,v[1]) for i in range(copies)]
    current=(16*copies,14+padding,{f(tuple(v)) for f in moves for v in j['selected']},
        [tuple(f(tuple(v)) for v in e) for f in moves for e in j['matching']])
    layers=[[f(tuple(w['endpoint'])) for f in moves for w in layer] for layer in j['freezing_layers']]
    current=(*current[:3],current[3]+[((8+16*i,5),(8+16*i,6)) for i in sorted(filled)])
    if filled:layers.append([(8+16*i,c) for i in sorted(filled) for c in (5,6)])
    return current,layers


def graph_model(n,edges,filled):
    kinds,pairs,_=canonical('A'*n+'B'*len(filled));links=[]
    support={o:set() for o in range(len(pairs))};units=set();incidence={};cost={};beta=n
    for e,(a,b) in enumerate(edges):
        assert 0<=a<n and 0<=b<n
        if e in filled:
            links += [(2*a,2*beta),(2*b+1,2*beta+1)]
            incidence[1,e,0]={a,b};cost[1,e,0]=1;beta+=1
        else:
            for slot in (0,1):
                j=2*e+slot;units.add(j);support[a].add(j);support[b].add(j)
                incidence[0,e,slot]={a,b};cost[0,e,slot]=0
    return (kinds,pairs,links,support,units),incidence,cost


def component_data(n,edges):
    adj=defaultdict(list)
    for i,(a,b) in enumerate(edges):adj[a].append((b,i));adj[b].append((a,i))
    remaining=set(range(n));components=[]
    while remaining:
        root=min(remaining);seen={root};pending=[root]
        while pending:
            for v,_ in adj[pending.pop()]:
                if v not in seen:seen.add(v);pending.append(v)
        remaining-=seen;ee={i for v in seen for _,i in adj[v]};components.append((seen,ee))
    return adj,components


def joint_formula(n,edges,filled):
    adjacency,components=component_data(n,edges)
    zero={v for i,edge in enumerate(edges) if i not in filled for v in edge}
    deficient=sum(ee<=set(filled) and len(ee)==len(vv)-1 for vv,ee in components)
    return n-deficient,n-deficient-len(zero),zero,components,adjacency


def constructive(n,edges,filled,incidence):
    value,cost,zero,components,adj=joint_formula(n,edges,filled)
    intervals={j:vs for j,vs in incidence.items() if j[0]==0}
    answer=dict(allocate(n,intervals)['assignment'])
    assert set(answer)==zero
    for vertices,ee in components:
        seeds=vertices&zero
        if seeds:
            reached=set(seeds);distance={v:0 for v in seeds};queue=deque(sorted(seeds))
            while queue:
                u=queue.popleft()
                for v,e in adj[u]:
                    if v in reached:continue
                    assert e in filled
                    distance[v]=distance[u]+1;reached.add(v);queue.append(v)
                    answer[v]=(1,e,0)
            assert reached==vertices
        else:
            order=sorted(vertices);index={v:i for i,v in enumerate(order)}
            beta_units={(1,e,0):{index[v] for v in edges[e]} for e in ee}
            local=allocate(len(order),beta_units)['assignment']
            answer.update({order[v]:j for v,j in local.items()})
    assert len(answer)==value and len(set(answer.values()))==value
    assert all(v in incidence[j] for v,j in answer.items())
    assert sum(j[0] for j in answer.values())==cost
    return answer


def independent_resource_pack(n,incidence,cost):
    resources=sorted(incidence);position={j:i for i,j in enumerate(resources)}
    choices={a:[j for j in resources if a in incidence[j]] for a in range(n)}
    @lru_cache(None)
    def visit(a,used):
        if a==n:return 0,0
        best=visit(a+1,used)
        for j in choices[a]:
            bit=1<<position[j]
            if used&bit:continue
            value,c=visit(a+1,used|bit);proposal=value+1,c+cost[j]
            if (proposal[0],-proposal[1])>(best[0],-best[1]):best=proposal
        return best
    return visit(0,0)


def check_graph(n,edges,filled,totals,primitive=False):
    data,incidence,cost=graph_model(n,edges,filled)
    value,links,zero,_,_=joint_formula(n,edges,filled)
    constructive(n,edges,filled,incidence)
    assert independent_resource_pack(n,incidence,cost)==(value,links)
    for solver in (ordinary_flow,fork_flow):
        answer=solver(*data);assert (answer['value'],answer['cost'])==(value,links)
        totals['abstract_flow_comparisons']+=1
    if primitive:
        answer=optimize(*data);assert (answer['value'],answer['cost'])==(value,links)
        totals['independent_primitive_pack_comparisons']+=1
    totals['graph_states']+=1;totals['constructive_resource_packs']+=1
    totals['independent_resource_pack_comparisons']+=1
    totals['states_with_deficit']+=value<n
    totals['states_with_full_payment_and_positive_links']+=value==n and links>0


def abstract_checks(totals):
    for n in range(1,5):
        possible=list(itertools.combinations_with_replacement(range(n),2))
        for m in range(4):
            for edges in itertools.combinations_with_replacement(possible,m):
                for mask in range(1<<m):
                    filled={i for i in range(m) if mask>>i&1}
                    check_graph(n,edges,filled,totals,primitive=n<=3 and m<=2)
    rng=random.Random(20261027)
    for _ in range(240):
        n=rng.randrange(2,8);edges=[(rng.randrange(n),rng.randrange(n)) for _ in range(rng.randrange(1,9))]
        filled={i for i in range(len(edges)) if rng.randrange(2)}
        check_graph(n,edges,filled,totals)
    # A long filled tree loses ONE, not one per filled pocket; a cycle
    # loses none. One empty edge in the tree repairs its final deficit.
    records=[]
    for n in range(2,33):
        tree=[(i,i+1) for i in range(n-1)];cycle=tree+[(n-1,0)]
        for name,edges,filled in [('filled_tree',tree,set(range(n-1))),
            ('filled_cycle',cycle,set(range(n))),('one_empty_tree',tree,set(range(1,n-1)))]:
            data,incidence,_=graph_model(n,edges,filled);v,c,_,_,_=joint_formula(n,edges,filled)
            constructive(n,edges,filled,incidence)
            f=fork_flow(*data);assert (f['value'],f['cost'])==(v,c)
            totals['long_joint_graph_controls']+=1
            records.append(dict(vertices=n,kind=name,payment=v,minimum_links=c))
    return records


def physical_one(current,bands,locations,totals,full=True):
    direct_check(*current);P={v for e in current[3] for v in e}
    assert frozen_certificate(current)[0]==P
    data,meta,_=whole_support_data(current,bands);owner,aa,bb,mm=owner_data(*data[:2])
    private_pool=set();selected=set();occupied=0
    for location in locations:
        left,right,u,v,lower_u,lower_v,above_u,above_v,band,c1,c2=location
        assert left in owner and right in owner and owner[left] in aa and owner[right] in aa
        assert owner[left]!=owner[right]
        selected|={owner[left],owner[right]}
        assert not {lower_u,lower_v}&(current[2]|P)
        assert {above_u,above_v}<=P
        if u in P:
            occupied+=1
            beta=owner[u];assert beta in bb and owner[v]==beta
            assert set(data[1][beta])=={u,v} and not data[3][beta]
            assert {e[0] for e in data[2] if e[1] in (u,v)}=={left,right}
            selected.add(beta)
        else:
            assert not {u,v}&(current[2]|P)
            js={meta['owner'][band,c] for c in (c1,c2)}
            assert len(js)==2 and js<=data[4]
            for j in js:assert {o for o,w in data[3].items() if j in w}=={owner[left],owner[right]}
            private_pool|=js
    local=restrict(data,selected,private_pool)
    q=len(locations)
    for solver in (ordinary_flow,fork_flow):
        f=solver(*local);assert (f['value'],f['cost'])==(2*q-occupied,occupied)
        totals['physical_restricted_value_cost_comparisons']+=1
        if full:
            f=solver(*data);assert (f['value'],f['cost'])==(2*q,0)
            totals['physical_full_pool_value_cost_comparisons']+=1
    if q<=2:
        f=optimize(*local);assert (f['value'],f['cost'])==(2*q-occupied,occupied)
        totals['independent_physical_primitive_packs']+=1
    totals['frozen_physical_boards']+=1
    return data,meta


def locations(q=1,move=lambda v:v):
    return [(move((8+16*i,4)),move((8+16*i,7)),move((8+16*i,5)),move((8+16*i,6)),
        move((9+16*i,5)),move((9+16*i,6)),move((7+16*i,5)),move((7+16*i,6)),
        4+8*i,5,6) for i in range(q)]


def physical_checks(totals):
    records=[]
    for q in range(1,13):
        masks=range(1<<q) if q<=6 else [0]+[(1<<s)-1 for s in range(1,q+1)]
        for mask in masks:
            filled={i for i in range(q) if mask>>i&1}
            cur,layers=fixture(q,filled);check_rank_certificate(cur,layers)
            data,meta=physical_one(cur,whole_bands(cur),locations(q),totals)
            _,aa,bb,mm=owner_data(*data[:2])
            assert (len(aa),len(bb),len(mm))==(2*q,len(filled),2*q)
            assert (len(cur[2]),len(cur[3]),len(data[4]))==(21*q,18*q+len(filled),59*q-2*len(filled))
            assert len(data[4])+len(bb)-len(aa)==57*q-len(filled)
            # The precise interval coordinate identities lost by filling.
            empty,_=fixture(q);old,om,_=whole_support_data(empty,whole_bands(empty))
            keys=lambda d,m:{(m['intervals'][j]['band'],m['intervals'][j]['first'],m['intervals'][j]['last']) for j in d[4]}
            lost={(4+8*i,c,c) for i in filled for c in (5,6)}
            assert keys(old,om)-lost==keys(data,meta)
            totals['exact_original_interval_deletion_checks']+=1
            records.append(dict(copies=q,filled=sorted(filled),restricted_payment=2*q-len(filled),
                restricted_links=len(filled),full_payment=2*q,full_links=0,margin=57*q-len(filled)))
    for padding,plug in itertools.product((2,10),(False,True)):
        cur,L=fixture(1,{0} if plug else set(),padding);check_rank_certificate(cur,L)
        physical_one(cur,whole_bands(cur),locations(),totals)
        totals['right_padding_controls']+=1
    for sym,plug in itertools.product(itertools.product((False,True),repeat=3),(False,True)):
        cur,L=fixture(1,{0} if plug else set());move=image_map(*cur[:2],sym)
        shape,T,M=transformed(*cur,*sym);image=(shape[0],shape[1],T,M)
        bands=[[tuple(map(move,col)) for col in band] for band in whole_bands(cur)]
        check_rank_certificate(image,[[move(v) for v in layer] for layer in L])
        physical_one(image,bands,locations(move=move),totals)
        totals['carried_band_isometries']+=1
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();abstract=abstract_checks(totals);physical=physical_checks(totals)
    report=dict(status='PASS',totals=dict(totals),long_joint_graphs=abstract,physical=physical,
        scope='Exact simultaneous guarded-pocket graph resource accounting and minimum links, '
        'with fully frozen actual shared-pocket restricted-interface loss. Full physical pool '
        'still pays every original alpha at zero links. No universal grid counterexample, '
        'no all-graph frozen realization, no proof that exterior compensation always exists.')
    args.output.write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
