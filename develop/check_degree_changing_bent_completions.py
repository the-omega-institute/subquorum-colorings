"""Monotone source births, arbitrary degree-changing completions and sharp cuts.

Written all-size proofs: DEGREE_CHANGING_BENT_COMPLETIONS.md. Standard library.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_bent_gap_private_reserves import family
from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors,occupied_degrees
from check_crossing_matching_ports import rectangle,strand_parts,band_resources,model_for_components,compile_partition
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_residual_corridors import direct_check
from check_terminal_defect_port_compensation import matching
from check_whole_support_fork_flow import fork_flow
from degree_three_fusion import occupied_band_certificate

if not __debug__:raise RuntimeError('Assertions required; do not run with -O.')


def compile_model(cur,regions):
    R,C,T,M=cur;P={v for e in M for v in e};bands=[];seen=set()
    for region in regions:
        assert not seen&region['cells'];seen|=region['cells'];bands+=region['bands']
    assert seen==set(itertools.product(range(R),range(C)))
    parts,partner=strand_parts(P,T,M,bands);Q,gaps,labels=band_resources(P,T,bands)
    data,closed=model_for_components(P,T,bands,parts,Q,gaps)
    _,A,B,_=owner_data(*data[:2]);assert R*C//2-len(T)-len(M)==len(Q)+len(B)-len(A)
    return data,closed,partner


def add_selections(cur,rng):
    R,C,T0,M=cur;P={v for e in M for v in e};T=set(T0);O=P|T
    candidates=sorted(set(itertools.product(range(R),range(C)))-O);rng.shuffle(candidates)
    for v in candidates:
        near=set(neighbors(v))&O
        if len(near)<=1 and all(not set(neighbors(t))&O for t in near&T):
            T.add(v);O.add(v)
    return R,C,T,M


def birth_check(before,after,regions,totals):
    direct_check(*before);direct_check(*after)
    assert before[:2]==after[:2] and before[3]==after[3] and before[2]<=after[2]
    d0,c0,N=compile_model(before,regions);d1,c1,_=compile_model(after,regions)
    assert [x['body'] for x in c0]==[x['body'] for x in c1]
    owner,A0,B0,X0=owner_data(*d0[:2]);_,A1,B1,X1=owner_data(*d1[:2])
    mate={p:q for e in before[3] for p,q in (e,e[::-1])}
    added=after[2]-before[2]
    converted={p for p,kind in d0[0].items() if kind=='BP' and N[p] in added}
    bad={p for p in converted if N[mate[p]] not in neighbors(N[p])}
    for p in converted-bad:
        a=owner[p]
        assert a in B0 and c0[a]['body']=={p,mate[p]}
        assert d0[0][mate[p]]=='BP' and N[mate[p]] not in after[2]
    mixed_births=A1&X0;beta_births=A1&B0;beta_to_mixed=B0&X1
    assert A0<=A1
    assert len(A1)==len(A0)+len(mixed_births)+len(beta_births)
    assert len(B1)+len(beta_births)+len(beta_to_mixed)==len(B0)
    assert len(X1)+len(mixed_births)==len(X0)+len(beta_to_mixed)
    assert len(converted)==len(mixed_births)+2*len(beta_births)+len(beta_to_mixed)
    assert len(mixed_births)+2*len(beta_births)<=len(bad)
    assert len(d1[4])-len(d0[4])==-len(added)+len(converted)
    assert len(B1)-len(A1)==len(B0)-len(A0)-len(converted)
    # Each birth owns a distinct actual M edge; no seam credit is duplicated.
    chosen=[]
    for a in sorted(A1-A0):
        candidates={tuple(sorted((p,mate[p]))) for p in bad&c0[a]['body']}
        assert candidates;chosen.append(min(candidates))
    active_bad={tuple(sorted((p,mate[p]))) for p in bad}
    assert len(set(chosen))==len(chosen) and len(chosen)<=len(active_bad)
    totals['monotone_transition_models']+=1;totals['converted_BP_endpoints']+=len(converted)
    totals['mixed_to_alpha_births']+=len(mixed_births);totals['beta_to_alpha_births']+=len(beta_births)
    totals['square_BP_conversions_to_mixed_only']+=len(converted-bad)
    totals['distinct_actual_edge_birth_witnesses']+=len(chosen)
    return d1,c1,dict(old_alpha=len(A0),alpha=len(A1),old_beta=len(B0),beta=len(B1),
        old_mixed=len(X0),mixed=len(X1),added=len(added),converted=len(converted),bad_converted=len(bad),
        births=len(A1-A0),active_bad_edges=len(active_bad))


def sharp_completion(w,q=1,sealed=False):
    R,C,T0,M=family(w,q);T=set(T0);n=w-2;start=w+2
    for i in range(q):
        top={1} if w==6 else {1}|set(range(4,n-1,2))
        bottom={0,n-1} if w==6 else set(range(n))-top
        T|={(4+10*i,start+j) for j in top}
        T|={(5+10*i,start+j) for j in bottom}
        T|={(7+10*i if j in bottom else 6+10*i,start+j) for j in range(1,n-1)}
        if sealed:T|={(7+10*i,c) for c in range(1,w,2)}
    return R,C,T,M


def reachable(data,start):
    owner,A,B,X=owner_data(*data[:2]);edges={a:set() for a in range(len(data[1]))}
    for p,q in data[2]:
        if owner[p]!=owner[q]:edges[owner[p]].add(owner[q])
    found={start};todo=[start]
    while todo:
        for b in edges[todo.pop()]:
            if b not in found:found.add(b);todo.append(b)
    return found


def family_check(w,q,cur,totals,rng,sharp=False,sealed=False,flow=False):
    base=family(w,q);R,C,T,M=cur;regions=[rectangle(0,R,0,C)]
    data,closed,birth=birth_check(base,cur,regions,totals)
    _,A,B,X=owner_data(*data[:2]);assert len(A)==q and not birth['births']
    rank=[[(p[0]+10*i,p[1])] for i in range(q) for p,a,b in occupied_band_certificate(w)]
    totals['strict_family_rank_events']+=len(check_rank_certificate(cur,rank))
    g=3 if w==6 else 2;U={a:data[3][a] for a in A}
    for a in A:
        assert len(U[a])>=g
        assert all({o for o,W in data[3].items() if u in W}=={a} for u in U[a])
        if sharp:assert len(U[a])==g
        if sealed:
            i=min(r for r,c in closed[a]['body'])//10
            F=reachable(data,a);assert not F&B and F-{a}<=X
            expected={(r+10*i,c) for r in (6,) for c in range(1,w+1)}
            assert set().union(*(closed[o]['body'] for o in F-{a}))==expected
            assert all(not data[3][o] for o in F-{a})
    assert len(matching(U))==q
    if sharp:assert len(T)==(2*w+6-(w==6)+(w//2 if sealed else 0))*q
    allunits=sorted(data[4]);tests=[set(),set(allunits)]
    for r in (1,2,3,4,7):tests.append(set(rng.sample(allunits,min(r,len(allunits)))))
    for count in sorted({1,min(q,2),q}):
        tests.append(set().union(*(U[a] for a in sorted(A)[:count])))
    for removed in tests:
        t=sum(W<=removed for W in U.values())
        assert g*t<=len(removed)
        direct=q-len(matching({a:W-removed for a,W in U.items()}));assert direct==t
        totals['private_joint_withdrawals']+=1
        if flow:
            result=fork_flow(*data[:3],{o:W-removed for o,W in data[3].items()},data[4]-removed)
            assert q-result['value']<=t and g*(q-result['value'])<=len(removed)
            if not t:assert result['value']==q and result['cost']==0
            if sealed:assert result['value']==q-t and result['cost']==0
            totals['whole_network_withdrawal_checks']+=1
        if sharp and sealed and t==q and len(removed)==g*q:
            totals['sharp_full_network_deficit_controls']+=1
    totals['family_models']+=1
    if len(T)>len(base[2]) and occupied_degrees(cur)!=occupied_degrees(base):totals['genuine_degree_changing_family_models']+=1
    if sealed:totals['sealed_family_models']+=1
    return dict(width=w,copies=q,selected=len(T),alpha=q,beta=len(B),mixed=len(X),private_bound=g,
        actual_private_counts=sorted(map(len,U.values())),sharp=sharp,sealed=sealed,
        new_degree_four=sum(d==4 for d in occupied_degrees(cur).values())-4*q)


def exhaustive_gaps(w,totals):
    cur=family(w);R,C,T,M=cur;P={v for e in M for v in e};O=P|T
    domain={(r,c) for r in (4,5,6,7) for c in range(w+2,2*w)}
    candidates=[]
    for v in sorted(domain-T):
        near=set(neighbors(v))&O
        if len(near)<=1 and all(not set(neighbors(t))&O for t in near&T):candidates.append(v)
    least=100
    for bits in range(1<<len(candidates)):
        final=(R,C,T|{v for j,v in enumerate(candidates) if bits>>j&1},M)
        try:direct_check(*final)
        except AssertionError:continue
        d,_,_=compile_model(final,[rectangle(0,R,0,C)]);_,A,B,X=owner_data(*d[:2])
        least=min(least,len(d[3][next(iter(A))]));totals['exhaustive_gap_completions_w'+str(w)]+=1
    assert least==(3 if w==6 else 2)


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();rng=random.Random(2026102604);records=[];seams=[]
    for w,q in itertools.product((6,8,10,14,20,32,64),(1,2,3,7)):
        samples=[(family(w,q),False,False),(sharp_completion(w,q),True,False),(sharp_completion(w,q,True),True,True)]
        samples += [(add_selections(family(w,q),rng),False,False) for _ in range(3)]
        samples += [(add_selections(sharp_completion(w,q,True),rng),False,True)]
        for cur,sharp,sealed in samples:
            records.append(family_check(w,q,cur,totals,rng,sharp,sealed,w<=14 and q<=3))
    for w in (6,8):exhaustive_gaps(w,totals)
    # Sharp generic source births, not claimed frozen.
    M=[((1,0),(2,0))];regs=[rectangle(0,4,0,2)]
    for oldT in (set(),{(0,0)}):
        _,_,record=birth_check((4,2,oldT,M),(4,2,{(0,0),(3,0)},M),regs,totals)
        assert record['births']==record['active_bad_edges']==1
        totals['sharp_nonfrozen_birth_controls']+=1
    # Actual fully frozen seam births: one new source per crossing M edge.
    for w,q in itertools.product((6,8,10,14,20,32),(1,2,3,7)):
        base=family(w,q);R,C,T,M=base
        regions=[rectangle(0,R,0,2),rectangle(0,R,2,C,True)]
        final=(R,C,T|{(7+10*i,1) for i in range(q)},M)
        d,closed,record=birth_check(base,final,regions,totals)
        assert record['old_alpha']==record['old_beta']==0
        assert record['old_mixed']==3*q and record['alpha']==q and record['mixed']==2*q
        assert record['converted']==record['bad_converted']==record['births']==record['active_bad_edges']==q
        _,A,B,X=owner_data(*d[:2]);assert not B
        for a in A:
            i=min(r for r,c in closed[a]['body'])//10
            body={(2+10*i,c) for c in range(w,2*w+1)}
            body|={(r+10*i,c) for r in (3,4,5) for c in (w,w+1)}
            body|={(6+10*i,c) for c in range(1,w+2)}
            assert closed[a]['body']==body
        result=fork_flow(*d);assert result['value']==q and result['cost']==0
        rank=[[(p[0]+10*i,p[1])] for i in range(q) for p,a,b in occupied_band_certificate(w)]
        totals['strict_seam_rank_events']+=len(check_rank_certificate(final,rank))
        independent,_=compile_partition(final,regions)
        assert independent['alpha']==q and independent['beta']==0 and independent['slack']==R*C//2-len(final[2])-len(M)
        totals['sharp_frozen_seam_birth_models']+=1;totals['independent_seam_compiler_comparisons']+=1
        seams.append(dict(width=w,copies=q,**record))
    # General mixed completions can change both inventory and resource count.
    for w in (6,8,10,14):
        base=family(w);R,C=base[:2]
        for cut in range(2,C,2):
            for direction in (False,True):
                regions=[rectangle(0,R,0,cut,direction),rectangle(0,R,cut,C,not direction)]
                for repeat in range(2):
                    birth_check(base,add_selections(base,rng),regions,totals)
                    totals['general_mixed_transition_models']+=1
    fixture=json.loads((Path(__file__).parent/'fixtures/degree_changing_bent_w8.json').read_text())
    stored=(*fixture['shape'],set(map(tuple,fixture['selected'])),[tuple(map(tuple,e)) for e in fixture['matching']])
    assert stored==sharp_completion(8,sealed=True);direct_check(*stored)
    totals['stored_fixture_rank_events']=len(check_rank_certificate(stored,[[tuple(v) for v in layer] for layer in fixture['frozen_layers']]))
    d,_,_=compile_model(stored,[rectangle(0,8,0,18)]);_,A,B,X=owner_data(*d[:2]);U=d[3][next(iter(A))]
    result=fork_flow(*d[:3],{o:W-U for o,W in d[3].items()},d[4]-U)
    assert fixture['expected']==dict(P=44,M=22,T=len(stored[2]),alpha=1,beta=len(B),mixed=len(X),
        private_units=len(U),whole_after_private_withdrawal_value=result['value'],slack=8*18//2-len(stored[2])-22)
    out=dict(status='PASS',counts=dict(totals),family=records,sharp_frozen_seams=seams,
        theorem='All monotone feasible fixed-P,M extensions: old alpha bodies persist; a newly born alpha owns a distinct actual M edge whose N partners are nonadjacent. Mixed births plus twice beta births <= converted BP incidences on such edges. Exact resource/strand transition ledger retained.',
        family_theorem='All occupied-family monotone feasible T extensions, allowing degree changes: exactly q alphas, at least 2 private units each (3 at w6), sharp. Degree-changing sealed extensions have no beta or interval exit beyond alpha private support; exact whole value after withdrawals counts alpha owners with surviving direct units, cost0. Arbitrary full-network withdrawal bound is sharp.',
        scope='General proofs written; enumeration verifies and discovers. No arbitrary newP or actual-M rematching. Mixed-direction regions restore all actual M edges. Sharp seam births are fully frozen and paid at zero links, not numerical counterexamples. Sealed deficiency is after explicit interval withdrawal; its full original pool pays all sources.')
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(totals))))

if __name__=='__main__':main()
