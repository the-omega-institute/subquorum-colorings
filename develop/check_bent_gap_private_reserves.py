"""General gap reserves and sharp retaining completions of an occupied bent family.

All-size proofs: docs/BENT_GAP_PRIVATE_RESERVES.md. Standard library only.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_adjacent_band_boundary_repair import copies as star_copies, extension, guard_witnesses, mixed_guard_witnesses
from check_compensation_flow_normal_form import owner_data
from check_cooperative_promotion import neighbors, occupied_degrees
from check_crossing_matching_ports import rectangle, strand_parts, band_resources, model_for_components, compile_partition
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_residual_corridors import direct_check, transformed
from check_terminal_defect_port_compensation import matching, brute
from check_whole_support_fork_flow import fork_flow
from degree_three_fusion import occupied_bands, occupied_band_certificate, corner_join, four_way

if not __debug__:raise RuntimeError('Assertions required; do not run with -O.')


def compile_gaps(cur,regions):
    R,C,T,M=cur;P={v for e in M for v in e};bands=[];locations=[];cells=set()
    for rid,region in enumerate(regions):
        assert not cells&region['cells'];cells|=region['cells']
        bands+=region['bands'];locations += [(rid,b) for b in range(len(region['bands']))]
    assert cells==set(itertools.product(range(R),range(C)))
    parts,_=strand_parts(P,T,M,bands);Q,gaps,labels=band_resources(P,T,bands)
    data,closed=model_for_components(P,T,bands,parts,Q,gaps)
    _,A,B,_=owner_data(*data[:2]);nodes={}
    for a in A:
        for b,cols in enumerate(bands):
            for c,pair in enumerate(cols):
                if set(pair)&closed[a]['body']:nodes[b,c]=a
    selected={a:set() for a in A};credits={a:[] for a in A};outer={a:[] for a in A};counts=Counter()
    for b,start,stop,U in gaps:
        users={nodes[b,c] for c in (start-1,stop) if (b,c) in nodes}
        if not users:continue
        n=stop-start;word=labels[b][start:stop];bb=[c for c in range(start,stop) if labels[b][c]==('B','B')]
        internal=0<start and stop<len(bands[b]);bound=0;reasons=[]
        if internal:
            if bb:bound=1;reasons.append('internal_BB')
            blank_rows=[j for j in (0,1) if all(pair[j] not in P|T for pair in bands[b][start:stop])]
            if blank_rows:
                bound=max(bound,n//3);reasons.append('blank_row_pressure')
            if blank_rows and n>=4:
                other=1-blank_rows[0]
                # Both boundary P vertices in the selected row anchor the end T.
                if all(bands[b][c][other] in T for c in (start,stop-1)) and all(
                    bands[b][c][other] in P for c in (start-1,stop)):
                    bound=max(bound,2+(n-4)//3);reasons.append('anchored_blank_row')
            if word[0]==word[-1]==('B','B'):

                bound=max(bound,2 if n%2==0 else 1);reasons.append('BB_ends_even' if n%2==0 else 'BB_ends_odd')
        elif bb:
            side=-1 if start==0 else 1
            if any(c%2!=(1 if side==-1 else 0) for c in bb):
                bound=1;reasons.append('boundary_phase')
        assert len(U)>=bound
        for a in users:
            gid=(b,start,stop)
            if bound:
                chosen=set(sorted(U)[:bound]);assert not selected[a]&chosen
                selected[a]|=chosen;credits[a].append(dict(gap=gid,bound=bound,reasons=reasons,units=sorted(chosen)))
                counts.update(reasons)
            elif bb and not internal:
                outer[a].append((gid,-1 if start==0 else 1,U))
    # Offset-free same-side boundary exclusions. Entire gaps, not immediate BB.
    for a in A:
        used=set()
        for gid,s,U in outer[a]:
            if gid in used:continue
            b=gid[0]
            candidate=next(((other,V) for other,t,V in outer[a] if other not in used
                and t==s and locations[other[0]]==(locations[b][0],locations[b][1]+1)),None)
            if candidate is None:continue
            other,V=candidate
            boundary=0 if s==-1 else len(bands[b])-1
            if not U:assert labels[b][boundary]==('T','T')
            if not V:assert labels[other[0]][boundary]==('T','T')
            assert U or V
            u=min(U|V);assert u not in selected[a]
            selected[a].add(u);used|={gid,other}
            credits[a].append(dict(boundary_pair=(gid,other),bound=1,units=[u]))
            counts['offset_free_boundary_pairs']+=1
    assert all(selected[a]<=data[3][a] for a in A)
    incidence=Counter(u for a in A for u in selected[a]);assert all(v<=2 for v in incidence.values())
    S=R*C//2-len(T)-len(M);assert S==len(Q)+len(B)-len(A)
    return data,closed,selected,credits,counts


def family(w,q=1,saturated=False):
    assert w>=6 and w%2==0 and q>=1
    R,C,T0,M=occupied_bands(w)[0];T=set(T0);n=w-2;start=w+2
    if saturated:
        filled={0,n-1}|{j for j in range(2,n-2) if (j-2)%3<2}
        T|={(5,start+j) for j in filled}
        T|={(7 if j in filled else 6,start+j) for j in range(1,n-1)}
    return 10*q-2,C,{(r+10*i,c) for i in range(q) for r,c in T},[
        tuple((r+10*i,c) for r,c in edge) for i in range(q) for edge in M]


def family_check(w,q,cur,totals,rng,exact=False,flow=False):
    direct_check(*cur);base=family(w,q);R,C,T,M=cur;P={v for e in M for v in e}
    assert base[2]<=T and base[3]==M and occupied_degrees(cur)==occupied_degrees(base)
    assert all(not set(neighbors(v))&P for v in T-base[2])
    schedule=[[(v[0]+10*i,v[1])] for i in range(q) for v,a,b in occupied_band_certificate(w)]
    totals['independent_strict_rank_events']+=len(check_rank_certificate(cur,schedule))
    regions=[rectangle(0,R,0,C)];data,closed,reserves,credits,counts=compile_gaps(cur,regions)
    owners,A,B,mixed=owner_data(*data[:2]);assert len(A)==q and len(B)==(w-1)*q and not mixed
    expected_links={((6+10*i,w+1),(6+10*i,w)) for i in range(q)}
    assert set(data[2])==expected_links
    dedicated={owners[b] for a,b in expected_links};assert len(dedicated)==q and dedicated<=B
    assert all(not data[3][b] for b in dedicated)
    totals['distinct_dedicated_beta_certificates']+=q
    g=w//3+2;choices={a:data[3][a] for a in A}
    assert len(P)==(4*w+12)*q
    for a in A:
        i=min(r for r,c in closed[a]['body'])//10
        body={(r+10*i,c) for r in (2,3) for c in range(w+1,2*w+1)}
        body|={(r+10*i,c) for r in (4,5,6) for c in (w+1,2*w)}
        assert closed[a]['body']==body
        U=choices[a];assert len(U)>=g and len(reserves[a])>=g
        assert all({o for o,W in data[3].items() if u in W}=={a} for u in U)
        if exact:assert len(U)==g
    assert len(matching(choices))==q and len(matching(reserves))==q
    if exact:assert len(T)==(2*w+6-w//3)*q
    old=guard_witnesses(cur)[1]
    if cur==base:
        assert all(not old[a] for a in A);totals['old_zero_witness_new_paid_sources']+=q
    tests=[set(),set().union(*choices.values())]
    all_units=sorted(data[4])
    for r in (1,2,g-1,g,g+1):tests.append(set(rng.sample(all_units,min(r,len(all_units)))))
    # Target whole private sets as well as random withdrawals.
    ordered=sorted(A)
    for t in (1,min(2,q),q):tests.append(set().union(*(choices[a] for a in ordered[:t])))
    for removed in tests:
        available=data[4]-removed;direct=q-len(matching({a:U-removed for a,U in choices.items()}))
        assert g*direct<=len(removed)
        totals['private_joint_withdrawals']+=1
        if exact and removed==set().union(*choices.values()):
            assert direct==q and len(removed)==g*q;totals['sharp_direct_withdrawals']+=1
        if flow:
            result=fork_flow(*data[:3],{o:W&available for o,W in data[3].items()},available)
            assert result['value']==q and result['cost']==direct
            if direct==0:assert result['value']==q and result['cost']==0
            if exact and removed==set().union(*choices.values()):
                assert result['value']==q and result['cost']==q
                totals['direct_deficit_repaired_by_links']+=1
            totals['whole_fork_comparisons']+=1
    totals['family_models']+=1;totals.update(counts)
    return dict(width=w,copies=q,selected=len(T),alpha=q,beta=len(B),private_bound=g,
                actual_private_counts=sorted(map(len,choices.values())),saturated=exact,
                dedicated_beta_links=q,whole_withdrawal_formula='value=q; minimum_links=number_of_alphas_with_all_current_body_units_reserved',
                frozen_rank_events=len(P),whole_zero_link_value=q)


def local_word_controls(totals):
    # Necessary local constraints for internal no-P gaps; end TT cannot face P.
    alphabet=('BB','BT','TB','TT')
    for n in range(1,9):
        for word in itertools.product(alphabet,repeat=n):
            if word[0]=='TT' or word[-1]=='TT':continue
            if any(sum(word[d][r]=='T' for d in (c-1,c+1) if 0<=d<n)+(word[c][1-r]=='T')>1
                for c in range(n) for r in (0,1) if word[c][r]=='T'):continue
            units=sum(x=='BB' for x in word)-sum(x=='TT' for x in word)
            assert units>=0
            if units==0:
                assert all(x in ('BT','TB') for x in word)
                assert not any(a==b==c for a,b,c in zip(word,word[1:],word[2:]))
            if any(x=='BB' for x in word):assert units>=1
            if all(x[0]=='B' for x in word) or all(x[1]=='B' for x in word):assert units>=n//3
            if word[0]==word[-1]=='BB':assert units>=(2 if n%2==0 else 1)
            if n>=4 and any(all(x[j]=='B' for x in word) and word[0][1-j]==word[-1][1-j]=='T'
                and word[1][1-j]==word[-2][1-j]=='B' for j in (0,1)):
                assert units>=2+(n-4)//3
            totals['local_internal_words']+=1


def boundary_shift_controls(totals):
    # A local control; the two P columns need not be the same global owner.
    base=(4,8,{(0,0),(1,0),(3,0),(2,2),(3,2)},
          [((0,2),(0,3)),((2,4),(3,4))])
    for symmetry in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*base,*symmetry);cur=(*shape,T,M);direct_check(*cur)
        P={v for e in M for v in e};bands=rectangle(0,shape[0],0,shape[1],symmetry[0])['bands']
        Q,gaps,labels=band_resources(P,T,bands);seen=False
        for b,start,stop,U in gaps:
            side=-1 if start==0 else 1 if stop==len(bands[b]) else 0
            if not side or not any(labels[b][c]==('B','B') for c in range(start,stop)):continue
            for d,first,after,V in gaps:
                other_side=-1 if first==0 else 1 if after==len(bands[d]) else 0
                if d!=b+1 or other_side!=side:continue
                if not any(labels[d][c]==('B','B') for c in range(first,after)):continue
                edge=stop if side==-1 else start
                other_edge=after if side==-1 else first
                if abs(edge-other_edge)!=2:continue
                assert U or V
                if bool(U)!=bool(V):seen=True
        assert seen;totals['actual_offset_boundary_controls']+=1


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--output',type=Path,required=True);args=parser.parse_args()
    totals=Counter();rng=random.Random(2026102603);records=[];mixed=[]
    local_word_controls(totals)
    boundary_shift_controls(totals)
    fixture=json.loads((Path(__file__).parent/'fixtures/bent_occupied_band_sharp_w8.json').read_text())
    fixed=(*fixture['shape'],set(map(tuple,fixture['selected'])),[tuple(map(tuple,e)) for e in fixture['matching']])
    assert fixed==family(8,saturated=True);direct_check(*fixed)
    totals['stored_fixture_strict_rank_events']=len(check_rank_certificate(fixed,
        [[tuple(v) for v in layer] for layer in fixture['frozen_layers']]))
    d,_,*_=compile_gaps(fixed,[rectangle(0,8,0,18)]);_,A,B,_=owner_data(*d[:2])
    U=d[3][next(iter(A))];full=fork_flow(*d)
    reserved=fork_flow(*d[:3],{o:W-U for o,W in d[3].items()},d[4]-U)
    assert fixture['expected']==dict(P=2*len(fixed[3]),M=len(fixed[3]),T=len(fixed[2]),alpha=len(A),beta=len(B),
        private_units=len(U),whole_value=full['value'],whole_cost=full['cost'],
        after_all_direct_units_reserved_value=reserved['value'],after_all_direct_units_reserved_cost=reserved['cost'])
    for w,q in itertools.product((6,8,10,14,20,32,64),(1,2,3,7)):
        for saturated in (False,True):
            cur=family(w,q,saturated)
            records.append(family_check(w,q,cur,totals,rng,saturated,w<=14 and q<=3))
        for repeat in range(3):
            cur=extension(family(w,q,repeat%2==0),rng)
            records.append(family_check(w,q,cur,totals,rng,False,w<=10 and q<=2))
            totals['random_retaining_completions']+=1
    # Exhaustively enumerate every retaining completion at the two private gaps,
    # at smallest width. Other regions do not affect these gap inventories.
    cur=family(6);R,C,T,M=cur;P={v for e in M for v in e}
    domain={(r,c) for r in (4,5,6,7) for c in range(8,12)}
    candidates=sorted(v for v in domain-T if not set(neighbors(v))&P)
    least=100
    for bits in range(1<<len(candidates)):
        final=(R,C,T|{v for i,v in enumerate(candidates) if bits>>i&1},M)
        try:direct_check(*final)
        except AssertionError:continue
        d,_,*_=compile_gaps(final,[rectangle(0,R,0,C)]);_,A,_,_=owner_data(*d[:2])
        least=min(least,len(d[3][next(iter(A))]));totals['exhaustive_private_gap_completions_w6']+=1
    assert least==4
    for name,cur in [('sealed_star',star_copies(1,True)),('open_star',star_copies(1))]+[
        (name+str(w),f(w)[0]) for w in (6,8,10,14) for name,f in [('corner',corner_join),('occupied',occupied_bands)]]:
        R,C=cur[:2]
        variants=[('uniform',[rectangle(0,R,0,C)])]
        for cut in (2,4,8,16):
            if cut<R:
                for direction in (False,True):
                    variants.append((str((cut,direction)),[rectangle(0,cut,0,C,direction),rectangle(cut,R,0,C,not direction)]))
        for tag,regions in variants:
            direct_check(*cur);data,closed,reserves,credits,counts=compile_gaps(cur,regions)
            _,A,B,_=owner_data(*data[:2]);old=(guard_witnesses(cur)[1] if tag=='uniform' else mixed_guard_witnesses(cur,regions)[1])
            full=A and min(map(len,reserves.values()))>=2
            if full:assert len(matching(reserves))==len(A)
            small={a:set(sorted(U)[:2]) for a,U in reserves.items()}
            if len(A)<=4:
                assert brute(small)==len(matching(small));totals['independent_exhaustive_reserve_matchings']+=1
            G=sum(map(len,reserves.values()));assert G<=2*len(data[4])
            if G+2*len(B)>=2*len(A)-1:
                assert cur[0]*cur[1]//2-len(cur[2])-len(cur[3])>=0
                totals['global_numerical_criteria']+=1
            improved=[a for a in A if len(old[a])<2<=len(reserves[a])]
            if tag!='uniform':
                independent,_=compile_partition(cur,regions)
                assert independent['alpha']==len(A) and independent['beta']==len(B)
                totals['independent_mixed_ledger_comparisons']+=1
            totals['strict_two_resource_source_improvements']+=len(improved)
            totals['general_partition_models']+=1;totals.update(counts)
            if improved:mixed.append(dict(name=name,partition=tag,old_counts=sorted(len(old[a]) for a in A),
                new_counts=sorted(len(reserves[a]) for a in A),all_alpha_two_reserves=bool(full)))
    out=dict(status='PASS',counts=dict(totals),family=records,strict_improvements=mixed,
        theorem='Internal gap with a blank row has at least floor(length/3) original units; internal gap of even length with BB at both ends has at least two different units. Retaining occupied-bands family has sharp minimum floor(w/3)+2 private units per alpha for all even w>=6 and all separated copies; direct deficit<=floor(r/(floor(w/3)+2)) after r unit withdrawals; full value remains q at exact link cost equal to direct deficit, using different dedicated whole beta owners.',
        scope='General geometry and arbitrary-width completion proof written. Exact sharpness concerns direct alpha-body support, not full fork deficit. Actual saturated controls can pay all sources with one link each after withdrawing every direct private unit. Mixed global identities retain all actual M edges; no newP, removed oldT or changed P degrees in retaining class.')
    args.output.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(dict(status='PASS',counts=dict(totals))))

if __name__=='__main__':main()
