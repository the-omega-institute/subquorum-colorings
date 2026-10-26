"""Exact shared activation costs via weighted matching, and a frozen adapter.

General reduction/proofs: docs/CAPACITY_TWO_GATE_BUNDLES.md.
This small-graph DP is an independent checker, not a blossom implementation.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_canonical_band_coarsening import forests
from check_compensation_flow_normal_form import owner_data
from check_degree_changing_bent_completions import compile_model
from check_fully_frozen_elbow_withdrawal import configuration_one
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_P_free_pivot_interface import regions
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Assertions required; do not use -O.')


def bipartite(choices,required=frozenset()):
    at={}
    def visit(a,seen):
        for r in sorted(choices[a]):
            if r in seen:continue
            seen.add(r)
            if r not in at or visit(at[r],seen):
                at[r]=a
                return True
        return False
    for a in sorted(required):assert visit(a,set())
    for a in sorted(set(choices)-set(required)):visit(a,set())
    assert len(set(at.values()))==len(at)
    assert set(required)<=set(at.values())
    return {a:r for r,a in at.items()}


def direct_optimum(sources,free,blocks,weights,enabled,required=frozenset()):
    """Enumerate activation choices, then independently match actual units."""
    enabled=sorted(enabled);best=None
    for mask in range(1<<len(enabled)):
        selected={i for k,i in enumerate(enabled) if mask>>k&1}
        choices={a:{('free',j) for j,S in enumerate(free) if a in S} for a in range(sources)}
        for i in selected:
            for j,S in enumerate(blocks[i]):
                for a in S:choices[a].add(('bundle',i,j))
        assignment=bipartite(choices,required)
        result=len(assignment),sum(weights[i] for i in selected)
        if best is None or (result[0],-result[1])>(best['value'],-best['cost']):
            best=dict(value=result[0],cost=result[1],selected=sorted(selected),assignment=assignment)
    return best


def weighted_matching(nodes,edges):
    """Exhaustive vertex-mask DP used only to verify the general reduction."""
    ids={v:i for i,v in enumerate(nodes)};adj={i:[] for i in range(len(nodes))}
    for u,v,w in edges:
        i,j=ids[u],ids[v];adj[i].append((j,w));adj[j].append((i,w))
    @lru_cache(None)
    def solve(mask):
        if not mask:return 0,()
        i=(mask&-mask).bit_length()-1
        rest=mask^(1<<i);best=solve(rest)
        for j,w in adj[i]:
            if rest>>j&1:
                value,pairs=solve(rest^(1<<j));candidate=value+w,((i,j),)+pairs
                if candidate[0]>best[0]:best=candidate
        return best
    weight,pairs=solve((1<<len(nodes))-1)
    return weight,[(nodes[i],nodes[j]) for i,j in pairs]


def graph_optimum(sources,free,blocks,weights,enabled,required=frozenset()):
    assert len(blocks)==len(weights) and all(len(block) in (1,2) for block in blocks)
    assert all(isinstance(w,int) and w>=0 for w in weights)
    assert all(set(S)<=set(range(sources)) for S in free)
    assert all(set(S)<=set(range(sources)) for block in blocks for S in block)
    C=sum(weights[i] for i in enabled);K=C+1;priority=K*sources+C+1
    nodes=[('source',a) for a in range(sources)]+[('free',j) for j in range(len(free))]
    edges=[]
    for j,S in enumerate(free):
        edges += [(('source',a),('free',j),K+priority*int(a in required)) for a in sorted(S)]
    for i in sorted(enabled):
        slots=[('slot',i,j) for j in range(2)];nodes+=slots
        edges.append((slots[0],slots[1],weights[i]))
        for j,S in enumerate(blocks[i]):
            edges += [(('source',a),slots[j],K+priority*int(a in required)) for a in sorted(S)]
    weight,matching=weighted_matching(nodes,edges)
    assignment={}
    for u,v in matching:
        if v[0]=='source':u,v=v,u
        if u[0]=='source':assignment[u[1]]=v
    assert len(set(assignment.values()))==len(assignment)
    selected={r[1] for r in assignment.values() if r[0]=='slot'}
    # Insert every unused bundle's internal edge (possibly of zero weight).
    used={v for edge in matching for v in edge}
    for i in enabled-selected:
        if (('slot',i,0),('slot',i,1)) not in matching and (('slot',i,1),('slot',i,0)) not in matching:
            assert ('slot',i,0) not in used and ('slot',i,1) not in used
            matching.append((('slot',i,0),('slot',i,1)))
    value=len(assignment);cost=sum(weights[i] for i in selected)
    assert set(required)<=set(assignment)
    assert weight==C+K*value-cost+priority*len(required)
    for a,r in assignment.items():
        if r[0]=='free':assert a in free[r[1]]
        else:assert r[1] in selected and r[2]<len(blocks[r[1]]) and a in blocks[r[1]][r[2]]
    return dict(value=value,cost=cost,selected=sorted(selected),matching_weight=weight,constant=C,scale=K,protected_sources=sorted(required))


def verify(sources,free,blocks,weights,enabled,counts):
    graph=graph_optimum(sources,free,blocks,weights,enabled)
    direct=direct_optimum(sources,free,blocks,weights,enabled)
    assert (graph['value'],graph['cost'])==(direct['value'],direct['cost'])
    counts['independent_weighted_graph_vs_activation_comparisons']+=1
    old_paid=set(bipartite({a:{j for j,S in enumerate(free) if a in S} for a in range(sources)}))
    protected_graph=graph_optimum(sources,free,blocks,weights,enabled,old_paid)
    protected_direct=direct_optimum(sources,free,blocks,weights,enabled,old_paid)
    assert (protected_graph['value'],protected_graph['cost'])==(protected_direct['value'],protected_direct['cost'])==(graph['value'],graph['cost'])
    counts['same_optimum_cost_with_old_sources_preserved']+=1
    return dict(enabled=sorted(enabled),weights=weights,**graph)


def physical():
    cur,bits,ranks=configuration_one();R,C,T,M=cur
    reflect=lambda v:(v[0],57-v[1])
    cur=16,58,T|set(map(reflect,T)),M+[tuple(map(reflect,e)) for e in M]
    bb={(r,c):False for r in range(0,16,2) for c in range(0,58,2)}
    bb.update(bits);bb.update({(r,56-c):v for (r,c),v in bits.items()});bb[2,28]=True
    ranks=[[p for v in layer for p in (v,reflect(v))] for layer in ranks]
    return cur,bb,ranks,[(2,28),(10,16),(10,40)]


def physical_adapter(counts):
    cur,bits,ranks,gates=physical();P={v for e in cur[3] for v in e}
    direct_check(*cur)
    assert len(cur[2])==166 and len(cur[3])==70 and len(P)==140
    assert len(check_rank_certificate(cur,ranks))==140 and frozen_certificate(cur)[0]==P
    counts['strict_physical_freezing_events']+=140
    assert all(not {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}&P for r,c in gates)
    first=None;states=[];blockcells=[];newblockcells=[]
    for mask in range(8):
        changed=dict(bits)
        for i,tile in enumerate(gates):changed[tile]=not bool(mask>>i&1)
        regs=regions(cur,changed);data,closed,_=compile_model(cur,regs);fs=forests(cur,regs)
        cells={fs[j][1] for j in data[4]};support={o:{fs[j][1] for j in W} for o,W in data[3].items()}
        own,A,B,X=owner_data(*data[:2]);left,right=own[3,12],own[3,45]
        assert A=={left,right,own[5,17],own[5,40]} and (len(A),len(B),len(X))==(4,4,10)
        zleft,zright=own[5,15],own[5,42]
        external={(p,q) for p,q in data[2] if own[p]!=own[q]}
        assert {(p,q) for p,q in external if own[p] in A|{zleft,zright}}=={((5,17),(5,16)),((5,40),(5,41))}
        assert not support[own[5,17]] and not support[own[5,40]]
        assert support[zleft]=={frozenset({(4,13),(5,13)})}
        assert support[zright]=={frozenset({(4,44),(5,44)})}
        O=P|cur[2]
        assert all(len({(r+1,c),(r-1,c),(r,c+1),(r,c-1)}&O)==3 for a in A for r,c in data[1][a])
        f=fork_flow(*data);alt=optimize(*data)
        assert (f['value'],f['cost'])==(alt['value'],alt['cost'])
        if first is None:
            first=(data,closed,cells,support)
            assert not support[left] and not support[right]
        assert data[:2]==first[0][:2] and set(data[2])==set(first[0][2])
        assert [c['body'] for c in closed]==[c['body'] for c in first[1]]
        assert len(cells)==228==16*58//2-166-70
        assert all(support[o]==first[3][o] for o in support if o not in (left,right))
        if mask in (1,2,4):
            lost=first[2]-cells;new=cells-first[2]
            assert len(lost)==len(new)==(2 if mask==1 else 1)
            assert all(not any(cell in W for W in first[3].values()) for cell in lost)
            if mask==1:assert support[left]==support[right]==new
            elif mask==2:assert support[left]==new and not support[right]
            else:assert support[right]==new and not support[left]
            blockcells.append(lost);newblockcells.append(new)
        selected={i for i in range(3) if mask>>i&1}
        expected=2+(2 if 0 in selected or {1,2}<=selected else int(bool(selected)))
        assert (f['value'],f['cost'])==(expected,2)
        states.append(dict(selected=sorted(selected),value=f['value'],links=f['cost'],
                           left_support=[sorted(c) for c in sorted(support[left],key=lambda x:sorted(x))],
                           right_support=[sorted(c) for c in sorted(support[right],key=lambda x:sorted(x))]))
        counts['physical_all_subset_adapters']+=1;counts['physical_independent_primitive_optima']+=1
    assert sum(map(len,blockcells))==len(set().union(*blockcells))==4
    assert sum(map(len,newblockcells))==len(set().union(*newblockcells))==4
    for mask in range(8):
        changed=dict(bits)
        for i,tile in enumerate(gates):changed[tile]=not bool(mask>>i&1)
        regs=regions(cur,changed);data,_,_=compile_model(cur,regs);fs=forests(cur,regs)
        cells={fs[j][1] for j in data[4]};chosen={i for i in range(3) if mask>>i&1}
        assert cells==(first[2]-set().union(set(),*(blockcells[i] for i in chosen)))|set().union(set(),*(newblockcells[i] for i in chosen))
        own,_,_,_=owner_data(*data[:2])
        for a,available in ((own[3,12],{0,1}),(own[3,45],{0,2})):
            assert {fs[j][1] for j in data[3][a]}==set().union(set(),*(newblockcells[i] for i in chosen&available))
    # Independent physical subset costs, compared with the two-slot reduction.
    blocks=[[{0,1},{0,1}],[{0}],[{1}]];cost_profiles=[]
    for weights in ((1,1,1),(3,2,2),(5,1,1),(0,2,2),(2,0,0)):
        for mask in range(8):
            enabled={i for i in range(3) if mask>>i&1}
            result=verify(2,[],blocks,list(weights),enabled,counts)
            candidates=[(s['value'],sum(weights[i] for i in s['selected'])) for s in states if set(s['selected'])<=enabled]
            expected=max(candidates,key=lambda x:(x[0],-x[1]))
            assert (result['value']+2,result['cost'])==expected
            cost_profiles.append(result)
    assert graph_optimum(2,[],blocks,[3,2,2],{0,1,2})['selected']==[0]
    # Charging the shared fee once per source instead prefers the wrong repair.
    wrong=[]
    for l,r in itertools.product(((0,0),(0,1),(1,0)),((0,0),(0,1),(2,0))):
        if l==r:continue
        wrong.append(dict(assignment=[l,r],per_payment_fee=[3,2,2][l[0]]+[3,2,2][r[0]],
                          actual_fee=sum([3,2,2][i] for i in {l[0],r[0]})))
    bad=min(wrong,key=lambda x:x['per_payment_fee'])
    assert bad['per_payment_fee']==bad['actual_fee']==4
    assert {i for i,j in bad['assignment']}=={1,2}
    counts['per_payment_fee_wrong_choice_controls']+=1
    # The shared two-resource bundle alone pays both, so one-token compression
    # is invalid when two different source witnesses may use the group.
    assert graph_optimum(2,[],blocks,[1,1,1],{0})['value']==2
    assert len(bipartite({0:{0},1:{0}}))==1
    counts['shared_two_unit_no_single_token_compression_controls']+=1
    R,C=cur[:2]
    for tr,fr,fc in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,tr,fr,fc);image=(*shape,T,M)
        def point(v):
            r,c=v
            if fr:r=R-1-r
            if fc:c=C-1-c
            return (c,r) if tr else (r,c)
        def tile_image(tile):
            cc=[point((tile[0]+i,tile[1]+j)) for i,j in itertools.product(range(2),repeat=2)]
            return min(r for r,c in cc),min(c for r,c in cc)
        base={tile_image(t):v!=tr for t,v in bits.items()}
        check_rank_certificate(image,[[point(v) for v in layer] for layer in ranks])
        for mask in range(8):
            changed=dict(base)
            for i,t in enumerate(gates):changed[tile_image(t)]=(not bool(mask>>i&1))!=tr
            d,_,_=compile_model(image,regions(image,changed));f=fork_flow(*d)
            assert (f['value'],f['cost'])==(states[mask]['value'],2)
            counts['dihedral_joint_states']+=1
    return dict(shape=list(cur[:2]),selected=166,matching=70,frozen=140,raw=228,
                gates=gates,baseline_payment=2,residual_sources=2,block_capacities=[2,1,1],
                states=states,cost_profiles=cost_profiles,per_payment_fee_wrong_choice=bad)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    counts=Counter();records=[];rng=random.Random(2026102701)
    verify(0,[],[[set(),set()]],[3],{0},counts)
    counts['empty_residual_source_controls']+=1
    for _ in range(120):
        sources=rng.randrange(1,7);m=rng.randrange(1,5)
        blocks=[[{a for a in range(sources) if rng.randrange(2)} for _ in range(rng.randrange(1,3))] for _ in range(m)]
        free=[{a for a in range(sources) if rng.randrange(2)} for _ in range(rng.randrange(3))]
        weights=[rng.randrange(6) for _ in blocks]
        for mask in range(1<<m):
            records.append(verify(sources,free,blocks,weights,{i for i in range(m) if mask>>i&1},counts))
        counts['abstract_models']+=1
    adapter=physical_adapter(counts)
    # Capacity-three / shared-gate controls: exact cover possible vs impossible.
    universe=set(range(6));triples=[{0,1,2},{3,4,5},{0,3,4},{1,2,5}]
    assert any(set().union(*S)==universe for S in itertools.combinations(triples,2))
    noncover=[{0,1,2},{0,3,4},{0,4,5}]
    assert set().union(*noncover)==universe
    assert not any(set().union(*S)==universe for S in itertools.combinations(noncover,2))
    counts['capacity_three_exact_cover_controls']+=2
    out=dict(status='PASS',scope='Independent finite checks of a general weighted-matching reduction and its explicit frozen-grid adapter. Capacity-three hardness is a written standard X3C reduction, not a frozen-grid hardness claim.',
             counts=dict(counts),abstract_checks=records,physical_adapter=adapter)
    args.output.parent.mkdir(parents=True,exist_ok=True);args.output.write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(counts,sort_keys=True))


if __name__=='__main__':main()
