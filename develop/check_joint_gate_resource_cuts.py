"""Joint capacity-one mixed entrances and shared original-interval cuts.

The arbitrary-size theorem is proved in JOINT_GATE_RESOURCE_CUTS.md.
This verifier checks its graph adapter against independent primitive packing.
No discovery solver is required.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_merger_completion_reserves import (
    STATES, complete, feasible, frozen, load, owner_data, whole_bands,
    whole_support_data,
)
from check_reserve_boundary_split import clipped, distance
from check_whole_support_fork_normal_form import canonical, optimize
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Assertions required; run without -O.')


def subsets(xs):
    xs=sorted(xs)
    for mask in range(1 << len(xs)):
        yield {v for i,v in enumerate(xs) if mask >> i & 1}


def matching_rank(left, adjacent):
    """Ordinary augmenting-path matching, independently of strand primitives."""
    used={}
    def augment(v,seen):
        for w in sorted(adjacent[v]):
            if w in seen: continue
            seen.add(w)
            if w not in used or augment(used[w],seen):
                used[w]=v
                return True
        return False
    return sum(augment(v,set()) for v in sorted(left))


def tree_count(sources, gates, incidence):
    """Single-incidence gates are loops; all isolated sources count as trees."""
    parent={a:a for a in sources}
    def root(a):
        while parent[a] != a:
            a=parent[a]
        return a
    for g in gates:
        ends=sorted(incidence[g] & sources)
        assert 1 <= len(ends) <= 2
        for a in ends[1:]:parent[root(a)]=root(ends[0])
    vertices=Counter(root(a) for a in sources)
    edges=Counter(root(next(iter(incidence[g] & sources))) for g in gates)
    return sum(edges[c] == v-1 for c,v in vertices.items())


def joint_cut(sources, incidence, support):
    gates=set(incidence)
    assert set(support)==gates
    ranks={}
    for H in subsets(gates):
        t=tree_count(sources,H,incidence)
        source_rank=matching_rank(sources,{a:{g for g in H if a in incidence[g]} for a in sources})
        assert source_rank==len(sources)-t
        K=gates-H
        interval_rank=matching_rank(K,support)
        union_bound=min(len(K-J)+len(set().union(set(),*(support[g] for g in J))) for J in subsets(K))
        assert interval_rank==union_bound, 'All shared original units counted by union, once.'
        ranks[frozenset(H)]=(source_rank,interval_rank,t)
    H=min(ranks,key=lambda h:ranks[h][0]+ranks[h][1])
    sr,ir,t=ranks[H]
    return dict(value=sr+ir,deficit=len(sources)-sr-ir,tree_count=t,
                outside_interval_rank=ir,separator_gates=sorted(H))


def strands(sources,incidence,support):
    """Abstract interfaces, not an asserted physical grid embedding."""
    sources=sorted(sources);gates=sorted(incidence)
    kinds,pairs,_=canonical('A'*len(sources)+'M'*len(gates))
    ai={a:i for i,a in enumerate(sources)}
    gi={g:len(sources)+i for i,g in enumerate(gates)}
    links=[(pairs[ai[a]][0],pairs[gi[g]][0]) for g in gates for a in incidence[g]]
    W={o:set() for o in range(len(pairs))}
    for g in gates:W[gi[g]]=set(support[g])
    return kinds,pairs,links,W,set().union(set(),*support.values())


def check_abstract(sources,incidence,support,totals,independent=True):
    cut=joint_cut(sources,incidence,support)
    d=strands(sources,incidence,support)
    flow=fork_flow(*d)
    assert flow['value']==cut['value']
    assert flow['cost']==flow['value'], 'All synthetic entry paths cost exactly one.'
    if independent:
        brute=optimize(*d)
        assert (brute['value'],brute['cost'])==(flow['value'],flow['cost'])
        totals['independent_abstract_packs']+=1
    totals['joint_cut_models']+=1
    # Direct private units cost zero; entering a gate costs one.
    P={a for a in sources if a % 2==0}
    U=sources-P
    reduced_inc={g:ends & U for g,ends in incidence.items() if ends & U}
    reduced_support={g:support[g] for g in reduced_inc}
    remainder=joint_cut(U,reduced_inc,reduced_support)
    enriched=(*d[:3],{o:set(js) for o,js in d[3].items()},set(d[4]))
    for a in P:
        owner=sorted(sources).index(a);j=10+a
        assert j not in enriched[4]
        enriched[3][owner].add(j);enriched[4].add(j)
    full=fork_flow(*enriched)
    assert (full['value'],full['cost'])==(len(P)+remainder['value'],remainder['value'])
    totals['private_prepayment_models']+=1
    return cut


def physical_model(cur):
    assert feasible(cur) and frozen(cur)
    d,meta,_=whole_support_data(cur,whole_bands(cur))
    o,aa,bb,mm=owner_data(*d[:2]);left,right=o[5,6],o[5,12]
    assert aa=={left,right}
    gate,tail=o[5,9],o[10,8]
    dl,dr=distance(d,left),distance(d,right)
    assert set(dl)&set(dr)=={gate,tail}
    filled=(5,5) in o
    beta=o[5,5] if filled else None
    assert set(dl)&bb==({beta} if filled else set()) and not set(dr)&bb
    # Every nontrivial reachable transition is accounted for, not pruned away.
    edges={(o[u],o[v]) for u,v in d[2] if o[u]!=o[v] and (o[u] in dl or o[u] in dr)}
    expected={(left,o[3,2]),(left,o[5,7]),(o[5,7],gate),
              (right,o[5,11]),(o[5,11],gate),(gate,tail)}
    if filled: expected.add((left,beta))
    assert edges==expected
    groups=[d[3][left],d[3][o[3,2]],d[3][right],d[3][gate],d[3][tail]]
    assert list(map(len,groups))[1:]==[2,5,6,5]
    flat=[j for group in groups for j in group]
    assert len(flat)==len(set(flat))
    for j in d[4]:
        ds=[min((dist[x] for x in dist if j in d[3][x]),default=None) for dist in (dl,dr)]
        expected=([0,None] if j in groups[0] else [1,None] if j in groups[1] else
                  [None,0] if j in groups[2] else [2,2] if j in groups[3] else
                  [3,3] if j in groups[4] else [None,None])
        assert ds==expected
    return d,meta,groups,filled


def physical_prediction(groups,filled,A):
    ell=0 if A&groups[0] else 1 if filled or A&groups[1] else None
    r=0 if A&groups[2] else None
    gate=2 if A&groups[3] else 3 if A&groups[4] else None
    private=[v for v in (ell,r) if v is not None]
    p=len(private)
    use=bool(p<2 and gate is not None)
    return p+use,sum(private)+(gate if use else 0)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);args=ap.parse_args()
    totals=Counter();rng=random.Random(2026102504)
    # Exhaust all ordered 3-gate graphs on 3 sources (loops allowed),
    # and every singleton interval label per gate. Shared supports are below.
    S=set(range(3));ends=[set(v) for v in itertools.combinations_with_replacement(range(3),2)]
    for choices in itertools.product(range(len(ends)),repeat=3):
        incidence={g:ends[e] for g,e in enumerate(choices)}
        for labels in itertools.product(range(3),repeat=3):
            support={g:{j} for g,j in enumerate(labels)}
            check_abstract(S,incidence,support,totals)
    for _ in range(1000):
        n=rng.randint(1,5);m=rng.randint(0,6);S=set(range(n))
        incidence={g:set(rng.sample(sorted(S),rng.randint(1,min(2,n)))) for g in range(m)}
        support={g:{j for j in range(5) if rng.randrange(2)} for g in range(m)}
        check_abstract(S,incidence,support,totals)
    # Both incidence degrees satisfy the physical two-owner bounds.
    S=set(range(4));incidence={0:{0,1},1:{1,2},2:{2,0},3:{3},4:{3}}
    support={0:{0,1},1:{2},2:{2},3:{0,3},4:{1,3}}
    assert all(sum(j in v for v in support.values())<=2 for j in range(4))
    named=check_abstract(S,incidence,support,totals)
    source_rank=matching_rank(S,{a:{g for g in incidence if a in incidence[g]} for a in S})
    interval_rank=matching_rank(set(incidence),support)
    reachable_rank=matching_rank(S,{a:set().union(*(support[g] for g in incidence if a in incidence[g])) for a in S})
    assert source_rank==interval_rank==reachable_rank==4 and named['value']==3
    named.update(source_gate_rank=source_rank,gate_interval_rank=interval_rank,
                 source_interval_reachability_rank=reachable_rank,physical_embedding='not asserted')
    # Even-cycle control also obeys the necessary opposite-terminal gate
    # coloring. It still does not assert a full frozen physical embedding.
    S5=set(range(5));inc5={0:{0,1},1:{1,2},2:{2,3},3:{3,0},4:{4},5:{4}}
    sup5={0:{0,1},1:{2},2:{3},3:{2},4:{0,4},5:{1,4}}
    even=check_abstract(S5,inc5,sup5,totals)
    source5=matching_rank(S5,{a:{g for g in inc5 if a in inc5[g]} for a in S5})
    interval5=matching_rank(set(inc5),sup5)
    reachable5=matching_rank(S5,{a:set().union(*(sup5[g] for g in inc5 if a in inc5[g])) for a in S5})
    colors={g:g%2 for g in inc5}
    assert all(len({colors[g] for g in inc5 if a in inc5[g]})==2 for a in S5)
    assert all(sum(j in js for js in sup5.values())<=2 for j in range(5))
    assert source5==interval5==reachable5==5 and even['value']==4
    even.update(source_gate_rank=source5,gate_interval_rank=interval5,
        source_interval_reachability_rank=reachable5,opposite_terminal_gate_coloring=colors,
        physical_embedding='not asserted; necessary parity only')
    _,base=load();physical={}
    for state in STATES:
        if state[0] in ('inner_beta','outer_beta'):continue
        d,meta,groups,filled=physical_model(complete(base,state))
        pools=[d[4],set()]
        for flags in itertools.product((False,True),repeat=5):
            selected=[g for g,flag in zip(groups,flags) if g and flag]
            pools.extend([set().union(set(),*selected),{min(g) for g in selected}])
        for count in (1,2):pools.extend(map(set,itertools.combinations(sorted(d[4]),count)))
        pools.extend({j for j in d[4] if rng.randrange(2)} for _ in range(128))
        for A in pools:
            expected=physical_prediction(groups,filled,A);data=clipped(d,A)
            flow=fork_flow(*data)
            assert (flow['value'],flow['cost'])==expected
            for forks in (False,True):
                brute=optimize(*data,allow_forks=forks)
                assert (brute['value'],brute['cost'])==expected
                totals['independent_physical_packs']+=1
            totals['complete_board_availability_models']+=1
        gate_only=groups[3]|groups[4]
        answer=fork_flow(*clipped(d,gate_only))
        assert (answer['value'],answer['cost'])==((2,3) if filled else (1,2))
        physical[state[0]]=dict(group_sizes=list(map(len,groups)),only_gate_intervals=(answer['value'],answer['cost']),
            full_pool=physical_prediction(groups,filled,d[4]),all_original_owners_links_betas_retained=True)
    record=dict(status='PASS',totals=dict(totals),named_joint_obstruction=named,even_cycle_obstruction=even,physical=physical,
        scope='Arbitrary-size joint gate/resource rank and tree-cut theorem is written, not inferred from finite tests. Physical adapter uses complete original active-merger board and all four frozen caps with arbitrary original interval availability. Four- and five-source joint obstructions are abstract only; no physical embedding or universal5/6 improvement asserted.')
    args.output.write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record))

if __name__=='__main__':main()
