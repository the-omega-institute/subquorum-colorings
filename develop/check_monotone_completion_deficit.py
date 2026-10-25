"""Permanent band links, completion deficit law and shared source-birth circuits.

General proofs: docs/MONOTONE_COMPLETION_DEFICIT_AND_BIRTH_CIRCUITS.md.
Enumeration tests adapters and optima; it does not replace those proofs.
"""
import argparse
from collections import Counter
from functools import lru_cache
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_compensation_flow_normal_form import owner_data
from check_crossing_matching_ports import rectangle,band_resources,strand_parts,model_for_components,compile_partition
from check_degree_changing_bent_completions import family,add_selections,compile_model
from check_forced_mates_and_adjacent_maxima import configuration,uniform_freezing
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_full_pool_interface_profile import family as interface_family
from check_frozen_beta_support_fork import restrict
from check_residual_corridors import direct_check
from check_terminal_defect_port_compensation import matching
from check_two_sided_seam_recourse import components
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import canonical,optimize,evaluate

if not __debug__:raise RuntimeError('Assertions required; no -O.')


def quotient(cur,regions):
    """Canonical capacity slots per fixed gap, NOT persistent forest identities."""
    R,C,T,M=cur;P={v for e in M for v in e};bands=[b for region in regions for b in region['bands']]
    parts,N=strand_parts(P,T,M,bands);Q,gaps,labels=band_resources(P,T,bands)
    original,closed=model_for_components(P,T,bands,parts,Q,gaps)
    own={v:o for o,c in enumerate(closed) for v in c['body']}
    support={o:set() for o in range(len(closed))};pool=set();table={}
    for b,first,after,units in gaps:
        owners=set()
        for c in (first-1,after):
            if 0<=c<len(bands[b]):owners|={own[v] for v in bands[b][c] if v in own}
        key=(b,first,after);slots={(*key,j) for j in range(len(units))}
        table[key]=(frozenset(owners),len(units));pool|=slots
        for o in owners:support[o]|=slots
        assert all({o for o,W in original[3].items() if u in W}==owners for u in units)
    return (*original[:3],support,pool),original,closed,N,table


def legal(cur,v):
    R,C,T,M=cur;P={p for e in M for p in e};O=P|T
    if v in O:return False
    near=set(neighbors(v))&O
    return len(near)<=1 and all(not set(neighbors(t))&O for t in near&T)


def transition(before,after,regions,totals,single=False,independent=False):
    direct_check(*before);direct_check(*after)
    assert before[:2]==after[:2] and before[3]==after[3] and before[2]<=after[2]
    d0,raw0,c0,N,g0=quotient(before,regions);d1,raw1,c1,_,g1=quotient(after,regions)
    assert [x['body'] for x in c0]==[x['body'] for x in c1]
    assert g0.keys()==g1.keys() and all(g0[g][0]==g1[g][0] and g0[g][1]>=g1[g][1] for g in g0)
    assert d1[4]<=d0[4]
    own,A0,B0,X0=owner_data(*d0[:2]);_,A1,B1,X1=owner_data(*d1[:2])
    added=after[2]-before[2];converted={p for p,k in d0[0].items() if k=='BP' and N[p] in added}
    assert set(d0[2])<=set(d1[2])
    assert all(p not in {b for a,b in d0[2]} for p in converted)
    r=len(A1&X0);s=len(A1&B0);t=len(X1&B0);h=len(d0[4])-len(d1[4]);p=len(added)
    assert h+len(converted)==p and len(converted)==r+2*s+t
    assert A0<=A1 and len(A1)-len(A0)==r+s and len(B0-B1)==s+t
    f0=fork_flow(*d0);f1=fork_flow(*d1)
    assert (f0['value'],f0['cost'])==(fork_flow(*raw0)['value'],fork_flow(*raw0)['cost'])
    assert (f1['value'],f1['cost'])==(fork_flow(*raw1)['value'],fork_flow(*raw1)['cost'])
    delta=f1['deficit']-f0['deficit'];assert 0<=delta<=p-s
    assert f1['value']<=f0['value']+r+s
    retained=evaluate(*d1[:2],f0['links'],*d1[3:])['value']
    assert retained>=f0['value']-h-t and retained<=f1['value']
    # Removing only new alpha owners retains all old alpha source identities.
    old_sources=restrict(d1,set(range(len(d1[1])))-(A1-A0),d1[4])
    assert fork_flow(*old_sources)['value']>=f0['value']-h-t
    S0=before[0]*before[1]//2-len(before[2])-len(before[3]);S1=S0-p
    assert -p<=S1+f1['deficit']-S0-f0['deficit']<=-s
    if single:
        assert p==1
        kind='interval' if not converted else ('mixed_birth' if r else 'beta_loss')
        totals[kind+'_delta'+str(delta)]+=1
    if independent:
        for data,f in ((d0,f0),(d1,f1)):
            z=optimize(*data);assert (z['value'],z['cost'])==(f['value'],f['cost'])
            totals['independent_primitive_optima']+=1
    totals['physical_transitions']+=1;totals['preserved_old_links']+=len(d0[2]);totals['converted_BP_no_old_entry']+=len(converted)
    return delta


def controlled(w,k,X,Y,upper,lower):
    """X births alpha; Y removes its private beta; upper/lower shared units open."""
    R,C,T,M=configuration(w,k)
    removed={(0,10*a+5) for a in set(range(k))-X}|{(w+1,10*a+7) for a in set(range(k))-Y}
    removed|={(0,10*i+1) for i in upper}|{(w+1,10*i+1) for i in lower}
    assert removed<=T
    return R,C,T-removed,M


@lru_cache(None)
def schedule(w,k):
    base=configuration(w,k);_,old=uniform_freezing(w,k,base)
    order=[]
    for a in range(k):
        prefix=[(1,3),(w,3),(1,9),(w,9),(1,7),(w-1,8),(1,5),(w,5),(w,7)]
        order += [(r,c+10*a) for r,c in prefix]
    first=set(order);order += [v for layer in old for v in layer if v not in first]
    cur=controlled(w,k,set(),set(),set(range(1,k)),set(range(1,k)))
    layers=[[v] for v in order];check_rank_certificate(cur,layers)
    return layers


def profile(w,k,X,Y,upper,lower,totals,independent=False):
    cur=controlled(w,k,X,Y,upper,lower);direct_check(*cur)
    ranks=check_rank_certificate(cur,schedule(w,k));totals['strict_controlled_rank_events']+=len(ranks)
    d,closed,N=compile_model(cur,[rectangle(0,cur[0],0,cur[1])]);own,A,B,M=owner_data(*d[:2]);f=fork_flow(*d)
    Z=X&Y;comps=components(k,upper,lower)
    deficit=sum(not doubles and set(range(left,right+1))<=Z for left,right,doubles in comps)
    assert (len(A),len(B),len(M),len(d[4]))==(len(X),k-len(Y),7*k-len(X)+len(Y),3*k+len(upper)+len(lower))
    assert (f['value'],f['deficit'])==(len(X)-deficit,deficit)
    assert cur[0]*cur[1]//2-len(cur[2])-len(cur[3])==4*k-len(X)-len(Y)+len(upper)+len(lower)
    # Explicit physical one/two-link routes into distinct private betas or shared units.
    choices={}
    for a in X:
        choices[a]=({('beta',a)} if a not in Y else set())
        for i in (a,a+1):
            if i in upper:choices[a].add(('upper',i))
            if i in lower:choices[a].add(('lower',i))
    assignment=matching(choices)
    assert len(assignment)==f['value'];links=[];used=set()
    for a,resource in assignment.items():
        side,i=resource
        if side=='beta':
            edge=((w,10*a+5),(w,10*a+6));assert edge in d[2] and own[edge[1]] in B
            links.append(edge)
        else:
            row=1 if side=='upper' else w
            if i==a:path=[((row,10*a+5),(row,10*a+4))]
            else:path=[((row,10*a+5),(row,10*a+6)),((row,10*a+7),(row,10*a+8))]
            unit=(0 if side=='upper' else w//2,10*i+1,10*i+1)
            assert all(e in d[2] for e in path) and unit in d[3][own[path[-1][1]]]
            assert unit not in used;used.add(unit);links+=path
    assert len({v for e in links for v in e})==2*len(links)
    assert evaluate(*d[:2],links,*d[3:])['value']==f['value']
    if independent:
        z=optimize(*d);assert (z['value'],z['cost'])==(f['value'],f['cost'])
        totals['independent_controlled_primitive_optima']+=1
    totals['controlled_models']+=1
    return cur,d,f,deficit


def abstract_controls(totals,rng):
    for repeat in range(600):
        types='AABMM' if repeat%2 else 'AABBM'
        kinds,pairs,possible=canonical(types);p=rng.choice([p for p,k in kinds.items() if k=='BP'])
        links=[e for e in possible if e[1]!=p and rng.random()<.28]
        Q=set(range(rng.randrange(1,5)));W={o:{j for j in Q if rng.random()<.45} for o in range(len(pairs))}
        before=(kinds,pairs,links,W,Q);nextk=dict(kinds);nextk[p]='TP'
        after=(nextk,pairs,links+[(p,q) for q in kinds if kinds[q]=='BP' and q!=p and rng.random()<.4],W,Q)
        f0=fork_flow(*before);f1=fork_flow(*after);assert 0<=f1['deficit']-f0['deficit']<=1
        for data,f in [(before,f0),(after,f1)]:
            z=optimize(*data);assert (z['value'],z['cost'])==(f['value'],f['cost'])
            totals['abstract_optima_using_forks']+=any(c['kind']=='fork' for c in f['certificates'])
        totals['abstract_zero_entry_conversions']+=1
    # Arbitrary BP relabeling is NOT a physical completion: the protected entry
    # hypothesis is essential for the sharper minus-beta-birth correction.
    kinds,pairs,_=canonical('AAB');Q={0};W={0:set(),1:set(),2:{0}}
    before=(kinds,pairs,[(0,4),(2,5)],W,Q)
    nextk=dict(kinds);nextk[4]=nextk[5]='TP'
    after=(nextk,pairs,[],W,Q)
    f0=fork_flow(*before);f1=fork_flow(*after)
    assert (f0['value'],f0['deficit'],f1['value'],f1['deficit'])==(2,0,1,2)
    assert f1['deficit']-f0['deficit']>2-1
    totals['nonphysical_relabeling_exclusion_controls']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();rng=random.Random(2026102606);records=[]
    # Every event subset on the smallest two genuinely shared instances.
    for w,k in ((8,1),(8,2),(8,3),(10,3)):
        events=[('X',a) for a in range(k)]+[('Y',a) for a in range(k)]
        events += [('U',i) for i in range(1,k)]+[('L',i) for i in range(1,k)]
        values={}
        for mask in range(1<<len(events)):
            X={a for j,(kind,a) in enumerate(events) if kind=='X' and mask>>j&1}
            Y={a for j,(kind,a) in enumerate(events) if kind=='Y' and mask>>j&1}
            upper={i for j,(kind,i) in enumerate(events) if kind=='U' and not mask>>j&1}
            lower={i for j,(kind,i) in enumerate(events) if kind=='L' and not mask>>j&1}
            cur,d,f,deficit=profile(w,k,X,Y,upper,lower,totals,k<=2 or mask%97==0)
            values[mask]=(deficit,cur)
        for mask,(D,cur) in values.items():
            for j in range(len(events)):
                if mask>>j&1:continue
                D1,nxt=values[mask|(1<<j)];assert 0<=D1-D<=1 and len(nxt[2]-cur[2])==1
                totals['controlled_single_event_edges']+=1
        records.append(dict(width=w,modules=k,all_event_subsets=len(values)))
    for w,k in itertools.product((8,14,32,64),(4,7,12)):
        for repeat in range(5):
            X={a for a in range(k) if rng.randrange(2)};Y={a for a in range(k) if rng.randrange(2)}
            U={i for i in range(1,k) if rng.randrange(2)};L={i for i in range(1,k) if rng.randrange(2)}
            profile(w,k,X,Y,U,L,totals)
        # Every proper birth subset is payable on an all-open single-edge path.
        for X in [set(),set(range(k)),set(range(k))-{rng.randrange(k)}]:
            _,_,f,D=profile(w,k,X,set(range(k)),set(),set(range(1,k)),totals)
            assert D==int(len(X)==k)
            totals['arbitrary_size_joint_birth_circuit_controls']+=1
        # With no shared edge the source birth and beta removal give an AND.
        for X,Y in [(set(),set()),(set(range(k)),set()),(set(),set(range(k))),(set(range(k)),set(range(k)))]:
            _,_,f,D=profile(w,k,X,Y,set(),set(),totals);assert D==len(X&Y)
            totals['arbitrary_size_source_beta_AND_controls']+=1
    # Physical all-board completions, mixed directions and ordinary resource loss.
    for w in (6,8,10,14):
        base=family(w);R,C=base[:2]
        for cut in (2,4,C-2):
            regs=[rectangle(0,R,0,cut),rectangle(0,R,cut,C,True)]
            cur=base
            for step in range(7):
                possible=[v for v in itertools.product(range(R),range(C)) if legal(cur,v)]
                if not possible:break
                v=rng.choice(possible);after=(*cur[:2],cur[2]|{v},cur[3])
                transition(cur,after,regs,totals,True,step==0 and w<=8);cur=after
            transition(base,add_selections(base,rng),regs,totals)
    base,regs=interface_family(8,1,set())
    for v in itertools.product(range(base[0]),range(base[1])):
        if legal(base,v):transition(base,(*base[:2],base[2]|{v},base[3]),regs,totals,True)
    # Sharp frozen endpoint events in the full original pool.
    for kind,point in [('mixed_birth',(0,5)),('beta_loss',(9,7))]:
        target=configuration(8,1);before=(*target[:2],target[2]-{point},target[3])
        assert transition(before,target,[rectangle(0,10,0,12)],totals,True,True)==1
    # Two converting ends of one old beta create only one demand, not two taxes.
    for w,k in itertools.product((8,14,32),(1,3,7)):
        target=configuration(w,k)
        removed={(r,10*a+5) for a in range(k) for r in (0,w+1)}
        before=(*target[:2],target[2]-removed,target[3])
        _,old=uniform_freezing(w,k,target);order=[]
        for a in range(k):
            order += [(r,c+10*a) for r,c in [(1,3),(w,3),(1,9),(w,9),(1,7),(w,7),(1,5),(w,5),(w-1,8)]]
        early=set(order);order += [v for layer in old for v in layer if v not in early]
        totals['strict_beta_birth_rank_events']+=len(check_rank_certificate(before,[[v] for v in order]))
        assert transition(before,target,[rectangle(0,w+2,0,10*k+2)],totals)==k
        totals['sharp_p_minus_beta_birth_controls']+=1
    abstract_controls(totals,rng)
    # Store a three-birth full-pool circuit with a common independent strict schedule.
    cur=controlled(8,3,set(),set(range(3)),set(),{1,2});d,_,_=compile_model(cur,[rectangle(0,10,0,32)])
    fixture=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],frozen_layers=schedule(8,3),
        birth_points=[(0,10*a+5) for a in range(3)],expected_deficits_by_birth_mask=[0]*7+[1],
        scope='Full original standard horizontal-band link network; all actual resources and beta credits retained.')
    path=Path(__file__).parent/'fixtures/monotone_birth_circuit_w8_k3.json'
    path.write_text(json.dumps(fixture,indent=2)+'\n')
    report=dict(status='PASS',counts=dict(totals),exhaustive_profiles=records,
        theorem='Fixed P,M,physical N and retained T: all old standard band links persist; full deficit is monotone and grows by at most added selections MINUS old beta-to-alpha births. Canonical gap coupling recomputes forest identities. Old paid-source certificates lose at most gap capacity loss plus beta-to-mixed count; beta-to-alpha owners had no old incoming entry and cannot cost an old payment. Both ends are counted only once.',
        family='For every even W>=8 and k, explicit fully frozen controls X alpha births,Y private beta removals,Eupper/Elower shared openings give D=number of tree resource components all of whose vertices lie in X intersect Y. Arbitrarily large joint birth circuits and source-beta AND controls in full original pools.',
        limits=['No P additions, M/N rematching, arbitrary extra inter-band cancellation or universal5over6 improvement.',
                'General proofs written; finite enumeration and scoped Lean verify only stated adapters.'])
    args.output.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(totals))))

if __name__=='__main__':main()
