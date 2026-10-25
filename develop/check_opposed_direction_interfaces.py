"""Actual fully frozen opposed modules: both uniform directions fail.

Proofs, including the componentwise endpoint-growth obstruction, are in
OPPOSED_DIRECTION_INTERFACES_AND_PIECEWISE_COMPENSATION.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path

from check_forced_mates_and_adjacent_maxima import configuration, forced_order
from check_perpendicular_guarded_reserves import transpose, neighbourhoods, endpoint_hull, hull_formula
from check_selection_maximum_singleton import compile_even_width, cropped, reduced_serial_certificate
from check_residual_corridors import direct_check, transformed
from check_compensation_flow_normal_form import owner_data
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize
from check_promotion_cores import frozen_certificate

if not __debug__:raise RuntimeError('Run with assertions; no -O.')


def reflected_right(v,L):return L-1-v[1],L+v[0]


def family(q):
    assert q>=1
    L=10*q+2;base=configuration(10*q,q);move=lambda v:reflected_right(v,L)
    right=(L,L,{(L-1-c,r) for r,c in base[2]},[tuple((L-1-c,r) for r,c in e) for e in base[3]])
    left=(*base[:2],base[2]-{(2,L-1)},base[3])
    full=(L,2*L,left[2]|{move(v) for v in base[2]},left[3]+[tuple(move(v) for v in e) for e in base[3]])
    return full,left,right


def fast_rank_certificate(cur,layers):
    mate={a:b for e in cur[3] for a,b in (e,e[::-1])};rank={v:i for i,layer in enumerate(layers) for v in layer}
    assert set(rank)==set(mate) and len(rank)==sum(map(len,layers));out=[]
    for v in sorted(mate):
        r,c=v;ns=((r-1,c),(r+1,c),(r,c-1),(r,c+1))
        kept=sorted(u for u in ns if u in cur[2] or (u in mate and rank[mate[u]]<rank[v]))
        assert len(kept)>=2
        out.append(dict(endpoint=v,rank=rank[v],kept_neighbors=kept[:2]))
    return out


def freezing_schedule(q):
    w=10*q;L=w+2;base=cropped(w);reduced=(*base[:2],base[2]-{(w-2,13)},base[3])
    prior=reduced_serial_certificate(w,reduced)
    module=[[v for v in layer if v[1]>=10] for layer in prior];module=[s for s in module if s]
    left=[[(r,c-10+10*i) for r,c in layer] for i in range(q) for layer in module]
    return left+[[reflected_right(v,L) for v in layer] for layer in left]


def forced_certificate(q,cur,N):
    w=10*q;L=w+2;order=forced_order(w,q);order+=[tuple(reflected_right(v,L) for v in e) for e in order]
    canonical={frozenset(e) for e in cur[3]};remaining={v for e in cur[3] for v in e};out=[]
    rank={v:k for k,e in enumerate(order) for v in e};endpoints=set(rank)
    for k,(a,b) in enumerate(order):
        assert frozenset((a,b)) in canonical and N[a]&remaining=={b}
        assert all(rank[u]<k for u in N[a]&endpoints-{b})
        remaining-={a,b};out.append(dict(leaf=a,mate=b,rank=k))
    assert not remaining
    return out


def no_endpoint_augmentation(cur,H,N):
    P={v for e in cur[3] for v in e};mate={a:b for e in cur[3] for a,b in (e,e[::-1])};vertices=P|H
    def augment(v,seen):
        for u in N[v]&vertices-seen:
            seen.add(u)
            if u not in mate or augment(mate[u],seen):mate[v]=u;mate[u]=v;return True
        return False
    assert all(not augment(v,set()) for v in sorted(H) if sum(v)%2==0)
    assert set(mate)==P


def directional_record(q,cur,vertical,totals,independent=False):
    data,meta=compile_even_width(transpose(cur) if vertical else cur)
    kinds,pairs,links,S,Q=data;owner,A,B,M=owner_data(kinds,pairs);L=10*q+2
    if vertical:
        failed={o for o in A if all(v[0]>=L for v in pairs[o])}
    else:
        failed={o for o in A if all(v[1]<L for v in pairs[o])}
    assert (len(A),len(B),len(M),len(failed),len(Q))==(2*q,q,5*q*(q+1),q,5*q+1)
    graph={o:set() for o in S}
    for a,b in links:
        if owner[a]!=owner[b]:graph[owner[a]].add(owner[b])
    closed=set(failed);todo=list(failed)
    while todo:
        o=todo.pop()
        for u in graph[o]-closed:closed.add(u);todo.append(u)
    assert not closed&B and all(not S[o] for o in closed)
    good=A-failed
    assert all(S[a] for a in good) and all(not S[a]&S[b] for a in good for b in good if a!=b)
    flow=fork_flow(*data);assert (flow['value'],flow['cost'],flow['deficit'])==(q,0,q)
    if independent:
        second=optimize(*data);assert (second['value'],second['cost'])==(q,0)
        totals['independent_full_pool_primitive_packs']+=1
    totals['uniform_direction_exact_flow_controls']+=1
    return dict(alphas=sorted(A),betas=sorted(B),mixed=len(M),raw=sorted(Q),
                failed_roots=sorted(failed),closed_owners=sorted(closed),
                owner_links=sorted({(owner[a],owner[b]) for a,b in links}),
                owner_support=[(o,sorted(S[o])) for o in sorted(S)],
                pairs=pairs,value=q,cost=0,deficit=q)


def piecewise_record(q,left,right,totals):
    L=10*q+2;records=[];used=set()
    for region,cur in enumerate((transpose(left),right)):
        data,meta=compile_even_width(cur);kinds,pairs,links,S,Q=data;owner,A,B,M=owner_data(kinds,pairs)
        assert (len(A),len(B),len(Q))==(q,q,2*q+(region==0))
        flow=fork_flow(*data);assert (flow['value'],flow['cost'])==(q,0)
        for i in range(q):
            tip=(10*i+3,1) if region==0 else (L-4-10*i,1)
            a=owner[tip];j=(5*i+1,2,2) if region==0 else (5*(q-i)-1,2,2)
            assert a in A and j in S[a]
            cells={(2,j[0]*2+k) for k in (0,1)} if region==0 else {(j[0]*2+k,L+2) for k in (0,1)}
            assert not cells&used;used|=cells
            records.append(dict(region=region,owner=a,unit=j,physical_cells=sorted(cells)))
    assert len(records)==2*q
    totals['piecewise_distinct_direct_payments']+=len(records)
    return records


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    totals=Counter();records=[];fixture=None
    for q in (*range(1,9),10,12):
        cur,left,right=family(q);L=10*q+2;direct_check(*cur);N=neighbourhoods(*cur[:2]);P={v for e in cur[3] for v in e}
        assert len(cur[2])==70*q*q+26*q+3 and len(cur[3])==30*q*q+10*q
        assert L*L-len(cur[2])-len(cur[3])==4*q+1
        witnesses=fast_rank_certificate(cur,freezing_schedule(q));assert frozen_certificate(cur)[0]==P
        forced=forced_certificate(q,cur,N)
        H=endpoint_hull(cur);old=hull_formula(10*q,q)
        coarse=old|{reflected_right(v,L) for v in old}|{(3,L-2)}
        assert H<=coarse
        attach_left={(10*q-1,10*i+9) for i in range(q)}|{(10*q-1,10*i+3) for i in range(1,q)}
        attach_right={reflected_right(v,L) for v in attach_left}
        for v in coarse:
            if v in attach_left:assert sum(v)%2==0 and v[1]<L
            elif v in attach_right:assert sum(v)%2==1 and v[1]>=L
            else:assert not N[v]&(P|coarse)
        assert all((u[1]<L)==(v[1]<L) for u in P|coarse for v in N[u]&(P|coarse))
        assert not {v for v in H if len(N[v]&(P|cur[2]))<=1}
        no_endpoint_augmentation(cur,H,N)
        h=directional_record(q,cur,False,totals,independent=q<=3)
        v=directional_record(q,cur,True,totals,independent=q<=3)
        pieces=piecewise_record(q,left,right,totals)
        physical=[tuple(v) for payment in pieces for v in payment['physical_cells']]
        assert len(set(physical))==4*q and not set(physical)&(P|cur[2])
        # Before the one deletion, both occupied neighbours of the seam T exist.
        assert (2,L) in cur[2] and (2,L+1) in P and (3,L-1) in cur[2]
        original=(*cur[:2],cur[2]|{(2,L-1)},cur[3])
        try:direct_check(*original)
        except AssertionError:pass
        else:raise AssertionError('The uncorrected interface must be infeasible.')
        totals['opposed_all_parameter_boards']+=1;totals['frozen_endpoint_witnesses']+=len(witnesses)
        totals['forced_unique_matching_pairs']+=len(forced);totals['complete_endpoint_hulls_and_matching_augmentation_checks']+=1
        if q<=3:
            for swap,fi,fj in itertools.product((False,True),repeat=3):
                (R,C),T,M=transformed(*cur,swap,fi,fj);image=(R,C,T,M);direct_check(*image)
                for normalized in (image,transpose(image)):
                    data,meta=compile_even_width(normalized);_,A,B,_=owner_data(*data[:2]);f=fork_flow(*data)
                    assert (len(A),len(B),len(data[4]),f['value'],f['cost'])==(2*q,q,5*q+1,q,0)
                    totals['carried_isometry_direction_controls']+=1
        records.append(dict(q=q,shape=cur[:2],selected=len(cur[2]),matching=len(cur[3]),slack=4*q+1,
            uniform_alphas=2*q,uniform_beta=q,uniform_value=q,uniform_deficit=q,piecewise_value=2*q,
            fixedP_optimum_upper=len(cur[2])+1,endpoint_hull_size=len(H)))
        if q==1:
            fixture=dict(**records[-1],selected_points=sorted(cur[2]),matching_edges=cur[3],
                strict_freezing_witnesses=witnesses,unique_matching_leaf_certificate=forced,
                endpoint_hull=sorted(H),coarse_endpoint_hull=sorted(coarse),
                horizontal=h,vertical=v,piecewise_payments=pieces)
    (Path(__file__).parent/'fixtures/opposed_direction_interface_obstruction.json').write_text(json.dumps(fixture,indent=2)+'\n')
    report=dict(status='PASS',totals=dict(totals),records=records,
        scope='Written all-q physical opposed-direction family; one necessary seam deletion; all endpoints frozen; unique actual M; both aligned global directions pay only q of2q with all raw units; disjoint piecewise perpendicular directions pay2q at zero links; joint T/P inclusion maximal under arbitrary rematching; within one selection of true ALL-T fixed-P optimum.',
        limits=['Not a counterexample to the numerical grid inequality: slack4qplus1.',
                'The two aligned global directions are tested, not every possible phase or arbitrary domino partition.',
                'True fixed-P optimum is bounded within one of displayed T, not claimed equal.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
