"""Mixed-direction alpha terminal defects and injective crossing-edge tax.

General proofs: docs/MIXED_TERMINAL_DEFECT_AND_FROZEN_OBSTRUCTION.md.
Finite checks test the geometric adapter, exact allocations and sharp family.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors, occupied_degrees
from check_compensation_flow_normal_form import owner_data
from check_crossing_matching_ports import rectangle, band_resources
from check_degree_changing_bent_completions import compile_model, add_selections
from check_forced_mates_and_adjacent_maxima import configuration
from check_frozen_inventory_frontier import inventory_schedule
from check_frozen_selection_frontier import cover, seals
from check_opposed_direction_interfaces import fast_rank_certificate
from check_residual_corridors import direct_check
from check_terminal_defect_port_compensation import components, deficit, matching
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:raise RuntimeError('Assertions required; no -O.')


def port_graph(cur,regions):
    R,C,T,M=cur;direct_check(*cur);P={v for e in M for v in e};O=P|T
    mate={v:u for e in M for v,u in (e,e[::-1])}
    data,closed,N=compile_model(cur,regions);own,A,B,X=owner_data(*data[:2])
    bands=[];which={};locations={};directions={}
    for rid,region in enumerate(regions):
        assert all(x%2==0 for x in region['bounds'])
        which.update({v:rid for v in region['cells']})
        for band in region['bands']:
            b=len(bands);bands.append(band);directions[b]=region['vertical']
            for c,pair in enumerate(band):
                for v in pair:locations[v]=(b,c)
    # Independent extraction of EVERY BB/TT forest, balanced or positive.
    capacity={};forest_at={};original={};unit_cells={}
    for b,cols in enumerate(bands):
        word=[tuple(sorted('P' if v in P else 'T' if v in T else 'B' for v in pair)) for pair in cols]
        unseen={c for c,x in enumerate(word) if x in (('B','B'),('T','T'))}
        while unseen:
            first=min(unseen);body={first};todo=[first];unseen.remove(first)
            while todo:
                c=todo.pop()
                for q in (c-1,c+1):
                    if q in unseen and (word[c]==('T','T') or word[q]==('T','T')):
                        unseen.remove(q);body.add(q);todo.append(q)
            first,last=min(body),max(body);assert body==set(range(first,last+1))
            cap=sum(1 if word[c]==('B','B') else -1 for c in body);assert cap in (0,1)
            if cap==0:assert (first==0 and word[first]==('T','T')) or (last==len(cols)-1 and word[last]==('T','T'))
            key=('forest',b,first,last);capacity[key]=cap
            unit_cells[key]=tuple(sorted(v for c in body for v in cols[c]))
            if cap:original[key]=(b,first,last)
            for c in body:forest_at[b,c]=key
    assert set(original.values())==data[4] and len(original)==len(data[4])
    physical_used=set()
    for key in original:
        cells=set(unit_cells[key]);assert not physical_used&cells;physical_used|=cells
    edges={};counts=Counter();tip_records=[];charged={};cross_direction={frozenset(e) for e in M if which[e[0]]!=which[e[1]] and regions[which[e[0]]]['vertical']!=regions[which[e[1]]]['vertical']}
    for a in sorted(A):
        ends=[]
        for v in data[1][a]:
            b,c=locations[v];cols=bands[b];degree=len(set(neighbors(v))&O)
            assert degree in (3,4),'Only alpha terminals need occupied degree>=3.'
            assert N[v] in T
            w=tuple(2*x-y for x,y in zip(v,N[v]));ports=[]
            for q in (c-1,c+1):
                if 0<=q<len(cols) and not set(cols[q])&O:ports.append(forest_at[b,q])
            assert len(ports)<=1
            seam=False
            if degree==4:
                counts['d4']+=1;assert not ports
            elif w not in O:
                counts['seam']+=1;seam=True;assert not ports
                assert which[v]!=which[mate[v]] and regions[which[v]]['vertical']!=regions[which[mate[v]]]['vertical']
                e=frozenset((v,mate[v]));assert e in cross_direction and e not in charged;charged[e]=v
                # The opposite endpoint's N axis IS parallel to this M edge,
                # hence its non-selected normal neighbour is its actual mate.
                other=mate[v];other_w=tuple(2*x-y for x,y in zip(other,N[other]));assert other_w==v
            elif ports:
                if not capacity[ports[0]]:counts['balanced_boundary']+=1
            else:counts['missing_local_axis_port']+=1
            if ports:node=ports[0]
            else:
                node=('dummy',v[0],v[1]);assert node not in capacity;capacity[node]=0
            if capacity[node]:assert original[node] in data[3][a]
            ends.append(node)
            tip_records.append(dict(owner=a,tip=v,degree=degree,opposite_normal=w,seam_defect=seam,node=node))
        edges[a]=tuple(ends)
    parts=components(capacity,edges);D0=deficit(parts,set());choices={a:{v for v in pair if capacity[v]} for a,pair in edges.items()}
    assignment=matching(choices);assert len(assignment)==len(A)-D0
    zeros=sum(not capacity[v] for pair in edges.values() for v in pair)
    boundary=counts['balanced_boundary']+counts['missing_local_axis_port'];tax=counts['d4']+boundary+counts['seam']
    assert zeros==tax and 2*D0<=tax and counts['seam']==len(charged)<=len(cross_direction)
    f=fork_flow(*data);assert f['deficit']<=D0 and f['value']>=len(assignment)
    S=R*C//2-len(T)-len(M);assert S==len(data[4])+len(B)-len(A)
    assert S>=len(B)-D0
    if tax<=2*len(B)+1:assert S>=0
    return dict(alpha=len(A),beta=len(B),mixed=len(X),raw=len(data[4]),slack=S,d4=counts['d4'],
        boundary=boundary,seam=counts['seam'],cross_direction_M=len(cross_direction),tax=tax,
        port_value=len(assignment),port_deficit=D0,value=f['value'],deficit=f['deficit'],cost=f['cost']),dict(
            data=data,closed=closed,partner=N,parts=parts,positive=set(original),original=original,
            edges=edges,choices=choices,assignment=assignment,tip_records=tip_records,charged=charged)


def mixed_regions(w,k):
    R=w+2;C=10*k+2;regions=[]
    for i in range(k):regions += [rectangle(0,R,10*i,10*i+4),rectangle(0,R,10*i+4,10*i+10,True)]
    regions.append(rectangle(0,R,10*k,C))
    return regions


def profile(w,k,cur,totals,rank=False,independent=False):
    R,C,T,M=cur;assert seals(w,k)<=T
    rec,cert=port_graph(cur,mixed_regions(w,k));data=cert['data'];own,A,B,X=owner_data(*data[:2]);N=cert['partner']
    assert A=={own[1,10*i+3] for i in range(k)}
    losses=cover(w,k,cur);h=[];all_supported=set()
    for i in range(k):
        c=10*i;a=own[1,c+3]
        assert set(data[1][a])=={(1,c+3),(w,c+3)}
        assert all(occupied_degrees(cur)[p]==3 for p in data[1][a])
        assert not any(own[p]==a and own[q]!=a for p,q in data[2])
        z=sum(losses[r,c+d] for r in (0,w) for d in (0,4));h.append(z)
        assert len(data[3][a])==z
        assert not all_supported&data[3][a];all_supported|=data[3][a]
        for j in data[3][a]:assert {o for o,W in data[3].items() if j in W}=={a}
    ell=sum(losses.values());assert ell>=sum(h)
    assert rec['value']==sum(z>0 for z in h) and rec['deficit']==sum(z==0 for z in h) and rec['cost']==0
    assert (rec['d4'],rec['boundary'],rec['seam'],rec['cross_direction_M'],rec['port_deficit'])==(0,0,2*k,2*k,k)
    assert ell+rec['deficit']>=k
    if rank:
        ranks=fast_rank_certificate(cur,inventory_schedule(w,k));totals['sharp_strict_freezing_events']+=len(ranks)
    if independent:
        z=optimize(*data);assert (z['value'],z['cost'])==(rec['value'],rec['cost']);totals['independent_primitive_optima']+=1
    totals['all_T_mixed_family_models']+=1
    return dict(w=w,k=k,size=len(T),ell=ell,private_support_sizes=h,**rec),cert


def check_withdrawals(rec,cert,rng,totals):
    positive=cert['positive'];Q=sorted(positive)
    sets=[set(),set(Q)]
    if len(Q)<=5:sets += [{q for i,q in enumerate(Q) if mask>>i&1} for mask in range(1<<len(Q))]
    else:sets += [{q for q in Q if rng.randrange(2)} for _ in range(3)]
    for removed in sets:
        pred=deficit(cert['parts'],removed);choices={a:W-removed for a,W in cert['choices'].items()}
        assert len(matching(choices))==rec['alpha']-pred
        withdrawn={cert['original'][q] for q in removed};data=cert['data']
        reduced=(*data[:3],{o:W-withdrawn for o,W in data[3].items()},data[4]-withdrawn)
        assert fork_flow(*reduced)['deficit']<=pred
        totals['joint_original_unit_withdrawals']+=1


def main():
    from check_adjacent_band_boundary_repair import copies
    from check_degree_changing_bent_completions import family
    from degree_three_fusion import four_way,corner_join
    from rotor_networks import chain
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    totals=Counter();rng=random.Random(2026102612);records=[];fixture=None
    boards=[configuration(8,1),family(8),copies(1),chain(1)[0],four_way(8)[0],corner_join(8)[0]]
    for bi,cur in enumerate(boards):
        R,C=cur[:2];partitions=[]
        for axis,stop in [('row',R),('col',C)]:
            for cut in range(2,stop,2):
                for vertical in (False,True):
                    partitions.append([rectangle(0,cut,0,C,vertical),rectangle(cut,R,0,C,not vertical)] if axis=='row' else [rectangle(0,R,0,cut,vertical),rectangle(0,R,cut,C,not vertical)])
        r=R//4*2;c=C//4*2
        for mask in range(16):
            boxes=[(0,r,0,c),(0,r,c,C),(r,R,0,c),(r,R,c,C)]
            partitions.append([rectangle(*box,bool(mask>>j&1)) for j,box in enumerate(boxes)])
        for repeat in range(4):
            partitions.append([rectangle(r,r+2,c,c+2,bool(rng.randrange(2))) for r in range(0,R,2) for c in range(0,C,2)])
        for j,regions in enumerate(partitions):
            rec,cert=port_graph(cur,regions);totals['general_physical_partitions']+=1
            totals['positive_seam_defect_models']+=rec['seam']>0
            totals['nonvacuous_zero_link_full_payment_certificates']+=rec['alpha']>0 and rec['port_deficit']==0
            totals['nonvacuous_coefficient_one_certificates']+=rec['alpha']>0 and rec['tax']<=2*rec['beta']+1
            if j%17==0:check_withdrawals(rec,cert,rng,totals)
        records.append(dict(base=bi,shape=cur[:2],partitions=len(partitions)))
    sharp=[]
    for w,k in itertools.product((8,10,14,32,64),(1,2,3,7)):
        base=configuration(w,k)
        for d in range(k+1):
            cur=(*base[:2],base[2]-{(0,10*i+5) for i in range(k-d)},base[3])
            rec,cert=profile(w,k,cur,totals,True,k<=2)
            assert (rec['ell'],rec['alpha'],rec['beta'],rec['mixed'],rec['raw'],rec['value'],rec['deficit'])==(k-d,k,k,k*(w//2-2),3*k-d,k-d,d)
            totals['sharp_frozen_repair_attainers']+=1
            if d==k:
                assert not any(rec['private_support_sizes']);totals['sharp_frozen_full_pool_obstructions']+=1
                assert 2*rec['deficit']==rec['seam']==rec['cross_direction_M']
            if w==8:sharp.append(rec)
            if (w,k,d)==(8,2,2):fixture=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],regions=[dict(bounds=x['bounds'],vertical=x['vertical']) for x in mixed_regions(w,k)],freezing_layers=inventory_schedule(w,k),expected=rec)
        for repeat in range(12):
            bare=(*base[:2],seals(w,k),base[3]);cur=add_selections(bare,rng)
            if repeat%2:cur=(*cur[:2],{v for v in sorted(cur[2]) if v in seals(w,k) or rng.randrange(2)},cur[3])
            rec,cert=profile(w,k,cur,totals,False,k==1 and repeat<2)
            totals['arbitrary_T_from_only_leaf_seals']+=1
    fp=Path(__file__).parent/'fixtures/mixed_degree_three_terminal_obstruction_w8_k2.json';fp.write_text(json.dumps(fixture,indent=2)+'\n')
    saved=json.loads(fp.read_text());cur=(*saved['shape'],set(map(tuple,saved['selected'])),[tuple(map(tuple,e)) for e in saved['matching']])
    rec,_=profile(8,2,cur,totals,True,True);assert rec==saved['expected']
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(totals),general_boards=records,sharp_family_records=sharp,
        theorem='Every disjoint even-rectangle mixed H/V partition, actual M restored, every alpha terminal degree>=3: exact zero-port incidences=d4+local_axis_boundary_defects+seam_defects; each seam defect injects into a different crossing actual M edge between opposite directions. 2Dport<=d4+b+s<=d4+b+eHV; full deficit<=Dport; if tax<=2beta+1 then slack>=0. Exact old path/cycle joint-withdrawal formula extends.',
        sharp_family='All even W>=8,k>=1: existing unique-M fully frozen ALL-T maximum under H width4/V width6 module partition has k alpha terminals pairs all degree3, beta k, raw2k, seam2k=eHV, boundary=d4=0, full value0,Dk; coefficient1 on eHV in 2D bound is sharp. For ANY feasible final T with column3 leaf seals: every source has private support h_i equal to four disjoint tile losses; full D=number h_i0, minlinks0, ell+D>=k. Fully frozen optimum under D<=d equals tau-k+d.',
        limits=['The numerical target and universal5/6 remain open outside the stated coefficient-one criterion.', 'The same P admits vertical zero-loss full compensation; this is not an obstruction after optimizing N.', 'General proof written; finite checks do not prove all-size geometry; Lean scope recorded separately.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals)),indent=2))

if __name__=='__main__':main()
