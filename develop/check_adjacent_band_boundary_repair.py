"""Adjacent-band reserves, actual frozen boundary failures and joint allocation.

Standard library only; general proofs: ADJACENT_BAND_BOUNDARY_REPAIR.md.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors, occupied_degrees
from check_crossing_matching_ports import rectangle, strand_parts, band_resources, model_for_components, compile_partition
from check_four_outward_alpha_localization import fixture as root_fixture
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_interval_connector_cycles_and_missing_ports import block
from check_pinwheel_two_track_switches import model
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_terminal_defect_port_compensation import port_graph, deficit, matching, brute
from check_whole_support_fork_flow import fork_flow
from degree_three_fusion import four_way, corner_join, occupied_bands
from rotor_networks import chain

if not __debug__:
    raise RuntimeError('Assertions are required; do not run with -O.')


def copies(q, sealed=False):
    assert q >= 1
    cur,_=chain(1);shape,T,M=transformed(*cur,True,False,False)
    assert shape == (30,30)
    if sealed:
        T |= {(r,c) for r in (0,1,14,15) for c in (0,2,4,6)}
        T |= {(r,c) for r in (14,15,28,29) for c in (23,25,27,29)}
    selected={(r+32*i,c) for i in range(q) for r,c in T}
    matching_edges=[tuple((r+32*i,c) for r,c in edge) for i in range(q) for edge in M]
    return 32*q-2,30,selected,matching_edges


def guard_witnesses(cur):
    R,C,T,M=cur;P={v for e in M for v in e};O=T|P
    data,closed,access,partner=model(cur)
    own,A,B,mixed=owner_data(*data[:2])
    caps={};keys={};forest_at={}
    # Independent forest extraction, also valid for nonterminal P degrees.
    for r in range(0,R,2):
        labels=[tuple(sorted('P' if (rr,c) in P else 'T' if (rr,c) in T else 'B'
                             for rr in (r,r+1))) for c in range(C)]
        remaining={c for c,l in enumerate(labels) if l in (('B','B'),('T','T'))}
        while remaining:
            first=min(remaining);cols={first};todo=[first];remaining.remove(first)
            while todo:
                c=todo.pop()
                for d in (c-1,c+1):
                    if d in remaining and (labels[c]==('T','T') or labels[d]==('T','T')):
                        cols.add(d);todo.append(d);remaining.remove(d)
            u=(r,min(cols),max(cols));cap=sum(1 if labels[c]==('B','B') else -1 for c in cols)
            assert cap in (0,1)
            caps[u]=cap;keys[u]=tuple(sorted(itertools.product((r,r+1),cols)))
            for c in cols:forest_at[r,c]=u
    assert {keys[u] for u in caps if caps[u]}==data[4]
    chosen={a:[] for a in A};all_pairs=Counter()
    for a in sorted(A):
        body=closed[a]['body'];used_bands=set()
        for r in range(0,R-2,2):
            if {r,r+2}&used_bands:continue
            options=[]
            for c in range(C):
                if not all(any((rr,c) in body for rr in (b,b+1)) for b in (r,r+2)):
                    continue
                for side in (-1,1):
                    x=c+side
                    if not 0<=x<C or any((rr,x) in O for rr in range(r,r+4)):
                        continue
                    units=[forest_at[b,x] for b in (r,r+2)]
                    for b,u in zip((r,r+2),units):
                        if not caps[u]:
                            outward=x+side;assert 0<=outward<C
                            assert {(b,outward),(b+1,outward)}<=T
                    assert any(caps[u] for u in units)
                    all_pairs['one_zero_band' if any(not caps[u] for u in units) else 'both_positive_bands']+=1
                    u=next(u for u in units if caps[u])
                    assert keys[u] in data[3][a]
                    options.append(dict(first_row=r,p_column=c,side=side,
                                        chosen_unit=keys[u],balanced_bands=[b for b,v in zip((r,r+2),units) if not caps[v]]))
            if options:
                chosen[a].append(options[0]);used_bands|={r,r+2}
        assert len({w['chosen_unit'] for w in chosen[a]})==len(chosen[a])
    slack=R*C//2-len(T)-len(M)
    assert slack==len(data[4])+len(B)-len(A)
    if min(occupied_degrees(cur).values())>=3:
        previous,_,_,_,parts,d4,boundary,_=port_graph(cur);assert previous==data
        info=dict(port_deficit=deficit(parts,set()),boundary=boundary,d4=d4,slack=slack)
    else:info=dict(port_deficit=None,boundary=None,d4=None,slack=slack)
    return data,chosen,all_pairs,info


def mixed_guard_witnesses(cur,regions):
    """Restore every actual M first; witnesses belong to GLOBAL alpha owners."""
    R,C,T,M=cur;P={v for e in M for v in e};O=T|P
    bands=[];region_of={};offsets=[]
    for i,region in enumerate(regions):
        assert not set(region_of)&region['cells']
        region_of.update({v:i for v in region['cells']})
        offsets.append(len(bands));bands+=region['bands']
    assert set(region_of)==set(itertools.product(range(R),range(C)))
    parts,partner=strand_parts(P,T,M,bands)
    Q,gaps,labels=band_resources(P,T,bands)
    raw,closed=model_for_components(P,T,bands,parts,Q,gaps)
    keys={j:tuple(sorted(v for pair in bands[j[0]][j[1]:j[2]+1] for v in pair)) for j in Q}
    assert len(set(keys.values()))==len(Q)
    data=(*raw[:3],{o:{keys[j] for j in W} for o,W in raw[3].items()},set(keys.values()))
    own,A,B,mixed=owner_data(*data[:2])
    positive_at={(j[0],c):keys[j] for j in Q for c in range(j[1],j[2]+1)}
    chosen={a:[] for a in A};local=Counter()
    for a in sorted(A):
        body=closed[a]['body'];used=set()
        for rid,region in enumerate(regions):
            offset=offsets[rid]
            for lb in range(len(region['bands'])-1):
                b0,b1=offset+lb,offset+lb+1
                if {b0,b1}&used:continue
                options=[]
                for c in range(len(bands[b0])):
                    if not all(set(bands[b][c])&body for b in (b0,b1)):continue
                    for side in (-1,1):
                        x=c+side
                        if not 0<=x<len(bands[b0]):continue
                        if any(v in O for b in (b0,b1) for v in bands[b][x]):continue
                        units=[positive_at.get((b,x)) for b in (b0,b1)]
                        for b,u in zip((b0,b1),units):
                            if u is None:
                                y=x+side;assert 0<=y<len(bands[b])
                                assert set(bands[b][y])<=T
                        assert any(u is not None for u in units)
                        local['mixed_one_zero_band' if any(u is None for u in units) else 'mixed_both_positive_bands']+=1
                        unit=next(u for u in units if u is not None);assert unit in data[3][a]
                        options.append(dict(region=rid,first_band=b0,p_column=c,side=side,chosen_unit=unit))
                if options:
                    chosen[a].append(options[0]);used|={b0,b1}
        assert len({w['chosen_unit'] for w in chosen[a]})==len(chosen[a])
    slack=R*C//2-len(T)-len(M);assert slack==len(Q)+len(B)-len(A)
    crossing=[e for e in M if region_of[e[0]]!=region_of[e[1]]]
    interface={a for a in A if len({region_of[v] for v in closed[a]['body']})>1}
    info=dict(port_deficit=None,boundary=None,d4=None,slack=slack,
              crossing_actual_matching_edges=len(crossing),global_interface_alphas=len(interface),
              interface_alphas_with_two_guard_pairs=sum(len(chosen[a])>=2 for a in interface))
    return data,chosen,local,info


def physical(name,cur,totals,rng,private=False,verify_flow=False,regions=None):
    direct_check(*cur)
    data,guards,local,info=(guard_witnesses(cur) if regions is None else mixed_guard_witnesses(cur,regions))
    own,A,B,mixed=owner_data(*data[:2]);Q=data[4]
    support={a:data[3][a] for a in A};g={a:len(guards[a]) for a in A}
    all_inc=Counter(u for a in A for u in support[a])
    assert all(n<=2 for n in all_inc.values())
    selected_inc=Counter(w['chosen_unit'] for a in A for w in guards[a])
    assert all(n<=2 for n in selected_inc.values())
    G=sum(g.values());assert G<=2*len(Q)
    assert info['slack']>=len(B)+(G-2*len(A)+1)//2
    if G+2*len(B)>=2*len(A)-1:
        assert info['slack']>=0;totals['global_coefficient_one_criteria']+=1
    minimum=min(g.values(),default=0)
    if A and minimum>=2:
        assert len(matching(support))==len(A)
        totals['nonvacuous_boundary_independent_full_payment']+=1
    if private:
        assert set(occupied_degrees(cur).values())=={3}
        assert A and minimum>=4
        for a in A:
            for w in guards[a]:
                u=w['chosen_unit']
                assert {o for o,units in data[3].items() if u in units}=={a}
        assert G<=len(Q) and info['slack']>=len(B)+3*len(A)
        totals['private_four_reserve_models']+=1
    removed_sets=[set()]
    ordered=sorted(Q)
    for r in (1,2,3,4,7):removed_sets.append(set(rng.sample(ordered,min(r,len(Q)))))
    removed_sets += [{u for u in ordered if rng.randrange(2)} for _ in range(2)]
    if A:
        first=min(A)
        removed_sets.append({w['chosen_unit'] for w in guards[first]})
    for removed in removed_sets:
        available=Q-removed
        choices={a:support[a]&available for a in A}
        value=len(matching(choices));D=len(A)-value
        if A and minimum>=2:
            assert minimum*D<=2*len(removed)
            if len(removed)<=minimum-2:assert D==0
            totals['geometric_joint_withdrawal_bounds']+=1
        if private:
            lost={a for a in A if {w['chosen_unit'] for w in guards[a]}<=removed}
            assert 4*len(lost)<=len(removed) and D<=len(lost)
            assert 4*D<=len(removed)
            totals['private_joint_withdrawal_bounds']+=1
        if len(A)<=4:
            # Restrict exhaustive assignment to designated witness units.
            small={a:{w['chosen_unit'] for w in guards[a]}&available for a in A}
            assert brute(small)==len(matching(small))
            totals['independent_small_guard_allocations']+=1
        if verify_flow:
            restricted=(*data[:3],{o:W&available for o,W in data[3].items()},available)
            flow=fork_flow(*restricted)
            assert flow['value']>=value
            if value==len(A):assert flow['value']==len(A) and flow['cost']==0
            totals['whole_fork_lower_bounds']+=1
    totals.update(local);totals['physical_models']+=1;totals['alpha_paths']+=len(A)
    totals['chosen_band_disjoint_pairs']+=G
    totals['positive_boundary_port_deficit_models']+=(info['port_deficit'] or 0)>0
    if regions is not None:
        totals['mixed_direction_partitions']+=1
        totals['crossing_actual_matching_edges']+=info['crossing_actual_matching_edges']
        totals['global_interface_alphas']+=info['global_interface_alphas']
        totals['interface_alphas_with_two_guard_pairs']+=info['interface_alphas_with_two_guard_pairs']
        if info['global_interface_alphas'] and A and minimum>=2:
            totals['all_global_alphas_paid_including_interfaces']+=1
    return dict(name=name,shape=list(cur[:2]),alpha=len(A),beta=len(B),guard_counts=sorted(g.values()),
                whole_direct_value=len(matching(support)),**info),guards


def extension(cur,rng):
    R,C,T0,M=cur;P={v for e in M for v in e};T=set(T0);O=T|P
    candidates=[v for v in itertools.product(range(R),range(C)) if v not in O
                and not set(neighbors(v))&P]
    rng.shuffle(candidates)
    for v in candidates:
        near=set(neighbors(v))&O
        if len(near)<=1 and not any(set(neighbors(t))&O for t in near):
            T.add(v);O.add(v)
    return R,C,T,M


def abstract_controls(totals,rng):
    for n,g in itertools.product(range(1,8),range(2,7)):
        for run in range(8):
            stubs=[(a,i) for a in range(n) for i in range(g)];rng.shuffle(stubs)
            groups=[]
            while stubs:
                a,i=stubs.pop();other=next((j for j,t in enumerate(stubs) if t[0]!=a),None)
                if other is not None and rng.randrange(3):
                    b,_=stubs.pop(other);groups.append({a,b})
                else:groups.append({a})
            W={a:{u for u,owners in enumerate(groups) if a in owners} for a in range(n)}
            assert all(len(w)==g for w in W.values()) and g*n<=2*len(groups)
            if len(groups)<=10:
                tests=[{u for u in range(len(groups)) if bits>>u&1} for bits in range(1<<len(groups))]
            else:
                tests=[set(),set(range(len(groups)))]+[{u for u in range(len(groups)) if rng.randrange(2)} for _ in range(30)]
            for removed in tests:
                value=len(matching({a:w-removed for a,w in W.items()}));D=n-value
                assert g*D<=2*len(removed)
                if len(removed)<=g-2:assert D==0
                totals['abstract_joint_withdrawals']+=1
            totals['abstract_incidence_models']+=1
    for g in range(2,7):
        # Two sources sharing all g resources: withdrawing all attains gD=2r.
        W={0:set(range(g)),1:set(range(g))};assert len(matching(W))==2
        removed=set(range(g));D=2-len(matching({a:w-removed for a,w in W.items()}))
        assert g*D==2*len(removed);totals['sharp_abstract_shared_withdrawals']+=1


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    totals=Counter();rng=random.Random(2026102602);records=[]
    fixture_path=Path(__file__).parent/'fixtures/degree_three_double_boundary_zero_paths.json'
    fixture=json.loads(fixture_path.read_text())
    cur=(*fixture['shape'],set(map(tuple,fixture['selected'])),[tuple(map(tuple,e)) for e in fixture['matching']])
    assert cur==copies(1,True)
    totals['independent_stored_rank_events']+=len(check_rank_certificate(cur,
        [[tuple(v) for v in wave] for wave in fixture['frozen_layers']]))
    for q in (1,2,3,4,7,12):
        cur=copies(q,True);data=model(cur)[0];own,A,B,mixed=owner_data(*data[:2])
        P={v for e in cur[3] for v in e};frozen,layers=frozen_certificate(cur);assert frozen==P
        totals['independent_copy_rank_events']+=len(check_rank_certificate(cur,
            [[w['endpoint'] for w in wave] for wave in layers]))
        record,guards=physical('sealed-copies'+str(q),cur,totals,rng,True,q<=4)
        assert len(P)==144*q and len(cur[3])==72*q and len(cur[2])==72*q
        assert len(A)==2*q and not B and record['port_deficit']==2*q and record['boundary']==4*q
        assert len(data[4])==338*q-30 and record['slack']==336*q-30
        assert record['whole_direct_value']==2*q
        if q==1:
            assert len(fixture['frozen_layers'])==36
            assert fixture['expected']==dict(P=len(P),M=len(cur[3]),T=len(cur[2]),alpha=len(A),beta=len(B),
                boundary_defects=record['boundary'],port_deficit=record['port_deficit'],
                whole_value=record['whole_direct_value'],whole_cost=0,slack=record['slack'])
        records.append(record)
        for repeat in range(5):
            ext=extension(copies(q,repeat%2==0),rng)
            record,_=physical('selection-extension'+str((q,repeat)),ext,totals,rng,True,q<=3)
            assert record['alpha']==2*q and record['beta']==0
            records.append(record);totals['selection_extension_controls']+=1
    families=[('root',root_fixture()[0]),('cycle',block('cycle',6,4)),('missing',block('missing',6,4))]
    for q in (1,2,3,4):families.append(('chain'+str(q),chain(q)[0]))
    for w in (8,10,14):
        families.extend([('four'+str(w),four_way(w)[0]),('corner'+str(w),corner_join(w)[0]),
                         ('occupied'+str(w),occupied_bands(w)[0])])
    for name,cur in families:
        for sym in itertools.product((False,True),repeat=3):
            shape,T,M=transformed(*cur,*sym)
            record,_=physical(name+str(sym),(*shape,T,M),totals,rng,False,name in ('root','cycle'))
            records.append(record)
    # The local and allocation theorems impose no endpoint-degree lower bound.
    for width in (4,6,10):
        cur=(4,width,{(0,2),(3,2)},[((1,2),(2,2))])
        assert min(occupied_degrees(cur).values())==2
        record,_=physical('nonterminal-'+str(width),cur,totals,rng,False,True)
        records.append(record);totals['nonterminal_physical_controls']+=1
    # Different N directions, actual M crossing cuts, and GLOBAL source identity.
    for sealed in (False,True):
        cur=copies(1,sealed);R,C=cur[:2]
        for cut in (2,4,8,16,24):
            for top in (False,True):
                regions=[rectangle(0,cut,0,C,top),rectangle(cut,R,0,C,not top)]
                record,_=physical('mixed-cut'+str((sealed,cut,top)),cur,totals,rng,False,True,regions)
                independent,_=compile_partition(cur,regions)
                assert independent['alpha']==record['alpha'] and independent['beta']==record['beta']
                assert independent['slack']==record['slack']
                assert independent['value']>=record['whole_direct_value']
                records.append(record);totals['independent_cut_ledger_comparisons']+=1
        bounds=[(0,16,0,14),(0,16,14,C),(16,R,0,14),(16,R,14,C)]
        for orientation in itertools.product((False,True),repeat=4):
            if len(set(orientation))==1:continue
            regions=[rectangle(*b,v) for b,v in zip(bounds,orientation)]
            record,_=physical('mixed-four'+str((sealed,orientation)),cur,totals,rng,False,True,regions)
            records.append(record)
    abstract_controls(totals,rng)
    result=dict(status='PASS',counts=dict(totals),records=records,
        theorem='Written adjacent exposed BB/P bands cannot both have balanced boundary forests; band-disjoint pairs certify distinct original whole-support units. Sum guard counts<=2L; global coefficient-one criterion; >=2 per alpha gives zero-link all-payment. Uniform g reserve gives gD<=2r; private g reserves give gD<=r.',
        obstruction='Actual30x30_144P72M72T_AllDegree3_36WaveFrozen_2AlphaNoBeta_All4PortsBalanced_DirectPortValue0_WholeSupportValue2Cost0;ArbitrarySeparatedQCopiesPortDeficit2q_Whole2q;EveryFixedPMonotoneDegree3SelectionExtensionRetains4PrivateCertifiedUnitsPerAlpha_DeficitLEfloorReservedOver4.',
        scope='Universal proofs are written, not inferred from controls. Exact port-only obstruction is not a full-network or numerical counterexample. Arbitrary grid alpha coverage, short bends, new P and universal5/6 remain open.')
    args.output.write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(totals))))


if __name__=='__main__':main()
