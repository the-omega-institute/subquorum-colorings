"""Fixed-P selection saturation does not repair whole-support compensation.

Independent even-width BB/TT forest compiler includes balanced boundary
chains. General proofs: SELECTION_MAXIMUM_SINGLETON_OBSTRUCTION.md.
"""
import argparse
from collections import Counter, defaultdict
import itertools
import json
from pathlib import Path
import random

from check_compensation_flow_normal_form import owner_data
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_frozen_tip_slot_obstruction import independent_strands
from check_full_pool_singleton_obstruction import fixture, compile_no_tt
from check_interval_connector_cycles_and_missing_ports import whole_bands
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_whole_support_fork_flow import fork_flow

if not __debug__:
    raise RuntimeError('Assertions required; no -O.')


def cropped(w):
    cur=fixture(w)
    return w+2,22,{(r-4,c) for r,c in cur[2]},[tuple((r-4,c) for r,c in e) for e in cur[3]]


def fixed_p_maximum(w):
 base=cropped(w)
 T={(0,c) for c in range(1,22,2)}|{(1,c) for c in (0,2,10,12,20)}
 T|={(2,c) for c in (0,8,11,18,21)}|{(3,c) for c in (1,3,7,9,11,13,17,19,21)}
 for r in range(4,w-2,2):
  T|={(r,c) for c in (0,2,8,10,12,18,20)}
  T|={(r+1,c) for c in ((0,2,7,9,11,13,17,19,21) if r==w-4 else (1,3,7,9,11,13,17,19,21))}
 T|={(w-2,c) for c in (1,3,8,10,12,18,20)}|{(w-1,c) for c in (0,11,21)}
 T|={(w,c) for c in (0,2,10,12,20)}|{(w+1,c) for c in range(1,22,2)}
 return (*base[:2],T,base[3])


def reduced_serial_certificate(w,cur):
    """Uniform all-height proof schedule, not a peeling-generated witness.

    Replay original direct cores after outer TP seeds. Postpone right lower
    side endpoint and BP until the PP seals have frozen. All coordinates
    below are first written in the preceding uncropped convention.
    """
    R=w+4;events=[]
    for shift in (0,10):
        for row,sign in ((5,-1),(R,1)):
            events.append(((row,3+shift),((row+sign,3+shift),(row,2+shift))))
    core=[((5,3),((4,3),(5,2))),((5,7),((4,7),(5,8))),
          ((R,3),((R,2),(R+1,3))),((R,7),((R,8),(R+1,7))),
          ((5,5),((4,5),(5,6))),((R,5),((R+1,5),(R,6))),
          ((R-1,6),((R-2,6),(R,6))),((R-1,4),((R-1,3),(R-1,5)))]
    for row in range(6,R-1,2):
        core.extend([((row,4),((row-1,4),(row,3))),((row+1,3),((row,3),(row+1,4)))])
    for row in range(R-2,5,-2):
        core.extend([((row,3),((row+1,3),(row,4))),((row-1,4),((row-1,3),(row,4)))])
    core.append(((5,6),((6,6),(5,5))))
    core.extend([((R,4),((R,3),(R-1,4))),((R-1,5),((R-1,4),(R,5))),
                 ((R,6),((R,5),(R-1,6)))])
    for shift in (2,12):
        events.extend(((v[0],v[1]+shift),tuple((u[0],u[1]+shift) for u in witnesses)) for v,witnesses in core)
    for shift in (0,10):
        for row,sign in ((5,-1),(R,1)):
            events.append(((row-sign,4+shift),((row,4+shift),(row-sign,5+shift))))
            if shift==10 and sign==1:continue
            events.append(((row-2*sign,4+shift),((row-2*sign,3+shift),(row-2*sign,5+shift))))
            events.append(((row,4+shift),((row,5+shift),(row-sign,4+shift))))
    for col in (4,14):
        for row in range(8,w+1,2):
            events.append(((row,col),((row-1,col),(row,col+1))))
        for row in range(w+1,8,-2):
            events.append(((row,col),((row+1,col),(row,col+1))))
    events.extend([((w+2,14),((w+1,14),(w+2,15))),
                   ((R,14),((R,15),(R-1,14)))])
    mate={a:b for e in cur[3] for a,b in (e,e[::-1])};frozen=set();layers=[]
    for point,witnesses in events:
        v=(point[0]-4,point[1]);ws=[(u[0]-4,u[1]) for u in witnesses]
        assert v in mate and v not in frozen and len(set(ws))==2
        assert all(sum(abs(a-b) for a,b in zip(v,u))==1 and u!=mate[v] for u in ws)
        assert all(u in cur[2] or (u in mate and mate[u] in frozen) for u in ws)
        frozen.add(v);layers.append([v])
    assert frozen==set(mate)
    check_rank_certificate(cur,layers)
    return layers


def feasible(cur,extra):
    try:
        direct_check(*cur[:2],cur[2]|set(extra),cur[3]);return True
    except AssertionError:return False


def candidates(cur):
    occupied=cur[2]|{v for e in cur[3] for v in e}
    return {(r,c) for r in range(cur[0]) for c in range(cur[1]) if (r,c) not in occupied and feasible(cur,{(r,c)})}


def compile_even_width(cur):
    """All whole-board aligned bands; arbitrary TT and boundary BT/TT.

    Feasibility forces each internal TT neighbour column to be BB. The
    BB/TT forest components have BB-TT difference one (an original resource)
    or zero (balanced chain touching a TT board boundary). Odd-width
    negative boundary components are excluded by the explicit width check.
    """
    direct_check(*cur);assert cur[0]%2==cur[1]%2==0
    bands=whole_bands(cur);P={v for e in cur[3] for v in e}
    kinds,comps=independent_strands(cur,bands)
    pairs=[tuple(sorted(tips)) for tips,_ in comps if tips]
    own,A,B,M=owner_data(kinds,pairs)
    body_owner={v:own[next(iter(tips))] for tips,body in comps if tips for v in body}
    nodes={};labels=[]
    for b,cols in enumerate(bands):
        row=[]
        for c,col in enumerate(cols):
            row.append(tuple(sorted('T' if v in cur[2] else 'P' if v in P else 'B' for v in col)))
            users={body_owner[v] for v in col if v in body_owner};assert len(users)<=1
            if users:nodes[b,c]=next(iter(users))
        labels.append(row)
    Q=set();forest=[];balanced=[]
    for b,row in enumerate(labels):
        for c,label in enumerate(row):
            if label==('T','T'):
                assert all(row[k]==('B','B') for k in (c-1,c+1) if 0<=k<len(row))
        unseen={c for c,label in enumerate(row) if label in (('B','B'),('T','T'))}
        while unseen:
            first=min(unseen);body={first};todo=[first];unseen.remove(first)
            while todo:
                v=todo.pop()
                for u in (v-1,v+1):
                    if u in unseen and (row[v]==('T','T') or row[u]==('T','T')):
                        unseen.remove(u);body.add(u);todo.append(u)
            first,last=min(body),max(body);assert body==set(range(first,last+1))
            bb=sum(row[c]==('B','B') for c in body);tt=len(body)-bb
            assert bb-tt in (0,1)
            if bb==tt:
                assert (first==0 and row[first]==('T','T')) or (last==len(row)-1 and row[last]==('T','T'))
                balanced.append((b,first,last))
            else:
                assert row[first]==row[last]==('B','B')
                j=(b,first,last);Q.add(j);forest.append((j,body))
    W={o:set() for o in range(len(pairs))};gaps=[]
    for b,row in enumerate(labels):
        c=0
        while c<len(row):
            if 'P' in row[c]:c+=1;continue
            first=c
            while c<len(row) and 'P' not in row[c]:c+=1
            units={j for j,body in forest if j[0]==b and first<=j[1]<=j[2]<c}
            capacity=c-first-sum(v in cur[2] for col in bands[b][first:c] for v in col)
            assert capacity==len(units)
            for boundary in (first-1,c):
                if (b,boundary) in nodes:W[nodes[b,boundary]]|=units
            gap_owners={nodes[b,k] for k in (first-1,c) if (b,k) in nodes}
            gaps.append(dict(band=b,first=first,last=c-1,capacity=capacity,owners=sorted(gap_owners)))
    links=[]
    for cols in bands:
        for left,right in zip(cols,cols[1:]):
            for a,b in zip(left,right):
                if kinds.get(a)=='TP' and kinds.get(b)=='BP':links.append((a,b))
                if kinds.get(b)=='TP' and kinds.get(a)=='BP':links.append((b,a))
    assert all(sum(j in js for js in W.values())<=2 for j in Q)
    slack=cur[0]*cur[1]//2-len(cur[2])-len(cur[3]);assert slack==len(Q)+len(B)-len(A)
    return (kinds,pairs,links,W,Q),dict(raw=len(Q),balanced_chains=balanced,labels=labels,gaps=gaps,slack=slack)


def closure(data):
    own,A,B,_=owner_data(*data[:2]);assert not B
    seen=set(A);todo=list(A)
    while todo:
        v=todo.pop()
        for a,b in data[2]:
            if own[a]==v and own[b] not in seen:seen.add(own[b]);todo.append(own[b])
    return seen,set().union(set(),*(data[3][o] for o in seen))


def tile_bounds(cur,C):
    caps=[]
    for r in range(0,cur[0],2):
        row=[]
        for c in range(0,cur[1],2):
            cells={(r+i,c+j) for i in (0,1) for j in (0,1)};xs=sorted(C&cells)
            row.append(max(len(S) for k in range(len(xs)+1) for S in itertools.combinations(xs,k) if feasible(cur,S)))
        caps.append(row)
    return caps


def inspect(base,cur,totals):
    direct_check(*cur);assert cur[:2]==base[:2] and cur[3]==base[3] and base[2]<=cur[2]
    P={v for e in cur[3] for v in e};frozen,layers=frozen_certificate(cur);assert frozen==P
    check_rank_certificate(cur,[[v['endpoint'] for v in layer] for layer in layers])
    data,meta=compile_even_width(cur);baseline,_=compile_even_width(base)
    assert data[:3]==baseline[:3]
    own,A,B,M=owner_data(*data[:2]);assert (len(A),len(B),len(M))==(2,0,14)
    _,reachable=closure(data);x=(base[0]-1,11);j=(base[0]//2-1,11,11)
    assert reachable== (set() if x in cur[2] else {j})
    flow=fork_flow(*data);assert (flow['value'],flow['cost'],flow['deficit'])==((0,0,2) if x in cur[2] else (1,1,1))
    assert meta['slack']>=4 and meta['raw']==meta['slack']+2
    totals['selected_extension_boards']+=1
    totals['boards_with_balanced_TT_boundary_chains']+=bool(meta['balanced_chains'])
    return dict(shape=cur[:2],selected=len(cur[2]),matching=len(cur[3]),slack=meta['slack'],raw_intervals=meta['raw'],
        balanced_boundary_chains=len(meta['balanced_chains']),value=flow['value'],cost=flow['cost'],deficit=flow['deficit'])


def exact_w8(base,C):
    """Finite witness discovery only. The size upper bound is the written
    disjoint-tile/shifted-patch proof, independently recomputed below.
    """
    conflict=[set(e) for e in itertools.combinations(C,2) if not feasible(base,e)]
    for v in C:
        N={u for u in C if sum(abs(a-b) for a,b in zip(v,u))==1}
        for a,b in itertools.combinations(N,2):
            e={v,a,b}
            if not any(f<=e for f in conflict) and not feasible(base,e):conflict.append(e)
    adj={v:set() for v in C}
    for e in conflict:
        for v in e:adj[v]|=e-{v}
    unseen=set(C);components=[];optimum=[]
    while unseen:
        v=min(unseen);body={v};todo=[v]
        while todo:
            v=todo.pop()
            for u in adj[v]-body:body.add(u);todo.append(u)
        unseen-=body;g=sorted(body);components.append(g);ids={v:i for i,v in enumerate(g)}
        masks=[sum(1<<ids[v] for v in e) for e in conflict if e<=body];best=[]
        def visit(i,mask,chosen):
            if len(chosen)+len(g)-i<=len(best):return
            if i==len(g):best[:]=chosen;return
            m=mask|1<<i
            if not any(m&e==e for e in masks):visit(i+1,m,chosen+[g[i]])
            visit(i+1,mask,chosen)
        visit(0,0,[]);optimum+=best
    assert len(optimum)==30 and feasible(base,optimum)
    return optimum,list(map(len,components))


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();rng=random.Random(20261025101);records=[]
    for w in list(range(8,42,2))+[64,128]:
        base=cropped(w);C=candidates(base);P={v for e in base[3] for v in e};x=(w+1,11)
        assert x in C and all(sum(abs(a-b) for a,b in zip(x,y))!=1 for y in C-{x})
        assert not any((r^1,c) in P for r,c in C)
        caps=tile_bounds(base,C)
        expected=[[0]*11,[2,0,0,0,1,2,0,0,0,1,2]]+[[2,2,0,1,2,2,2,0,1,2,2]]*(w//2-3)+[[2,0,0,0,0,2,0,0,0,0,2],[0,0,0,0,0,1,0,0,0,0,0]]
        assert caps==expected and sum(map(sum,caps))==8*w-33
        # Every new selection is individually selectable at the baseline;
        # only x lies in a no-P gap adjacent to any reachable original owner.
        d,m=compile_even_width(base);seen,_=closure(d)
        reachable_cells={(2*g['band']+i,c) for g in m['gaps'] if set(g['owners'])&seen
                         for i in (0,1) for c in range(g['first'],g['last']+1)}
        assert C&reachable_cells=={x}
        from check_full_pool_singleton_obstruction import compile_no_tt
        old,_=compile_no_tt(base,whole_bands(base));assert old[:3]==d[:3]
        assert {(b,c,c) for b,c in old[4]}==d[4]
        assert all({(b,c,c) for b,c in js}==d[3][o] for o,js in old[3].items())
        totals['exact_noTT_adapter_comparisons']+=1
        inspect(base,base,totals)
        inspect(base,(*base[:2],base[2]|{x},base[3]),totals)
        tested = sorted(C) if w<=12 else rng.sample(sorted(C),12)
        for v in tested:
            inspect(base,(*base[:2],base[2]|{v},base[3]),totals)
            totals['single_selection_extensions']+=1
        for trial in range(12):
            cur=base;order=sorted(C);rng.shuffle(order)
            for v in order:
                if trial%3==0 and v==x:continue
                if feasible(cur,{v}):cur=(*cur[:2],cur[2]|{v},cur[3])
            info=inspect(base,cur,totals)
            if trial%3:
                assert x in cur[2] and not candidates(cur)
                totals['inclusion_maximal_extensions']+=1
            else:
                # x remains addable independently of every other choice.
                assert feasible(cur,{x})
            if trial==1:records.append(dict(w=w,**info))
        # A stronger maximum over ALL selections with these endpoints, with
        # no retention hypothesis. Four disjoint 4x2 patches improve the
        # P-only aligned tile bound by four; each patch has three forbidden
        # adjacent pairs of candidates.
        empty=(*base[:2],set(),base[3]);allC=candidates(empty)
        allcaps=tile_bounds(empty,allC)
        assert allcaps==[[2,2,1,1,1,2,2,1,1,1,2]]+[[2,2,0,1,2,2,2,0,1,2,2]]*(w//2-2)+[[2,2,0,0,1,2,2,0,0,1,2],[2,2,1,1,1,2,2,1,1,1,2]]
        assert sum(map(sum,allcaps))==8*w+12
        covered=set()
        for r,c in itertools.product((0,w-2),(2,12)):
            cells={(r+i,c+j) for i in range(4) for j in (0,1)}
            assert not cells&covered;covered|=cells
            assert allC&cells=={(r,c),(r,c+1),(r+1,c),(r+2,c),(r+3,c),(r+3,c+1)}
            pairs=[((r,c),(r,c+1)),((r+1,c),(r+2,c)),((r+3,c),(r+3,c+1))]
            assert all(not feasible(empty,pair) for pair in pairs)
            assert sum(allcaps[i//2][c//2] for i in (r,r+2))==4
        maximum=fixed_p_maximum(w);direct_check(*maximum)
        data,meta=compile_even_width(maximum);flow=fork_flow(*data)
        assert len(maximum[2])==8*w+8 and meta['slack']==4 and meta['raw']==6
        assert (flow['value'],flow['deficit'])==(0,2) and not closure(data)[1]
        assert base[2]-maximum[2]=={(w-2,13)}
        # Even the reduced original configuration is frozen; the written
        # relay certificate postpones precisely the two affected events.
        reduced=(*base[:2],base[2]-{(w-2,13)},base[3])
        reduced_serial_certificate(w,reduced)
        assert frozen_certificate(reduced)[0]==P
        frozen,layers=frozen_certificate(maximum);assert frozen==P
        check_rank_certificate(maximum,[[v['endpoint'] for v in layer] for layer in layers])
        totals['all_selection_fixed_P_exact_maxima']+=1
        records.append(dict(w=w,kind='all-selection fixed-P maximum',selected=len(maximum[2]),matching=len(maximum[3]),slack=4,raw_intervals=6,value=0,deficit=2))
        if w==8:
            global_fixture=dict(shape=maximum[:2],selected=sorted(maximum[2]),matching=maximum[3],
                fixed_P_selection_maximum=72,upper_bound='POnlyAlignedTileCaps76_FourDisjoint4x2PatchesEachThreeForbiddenPairs_Save4',
                retained_original_selections=40,removed_original_selection=(6,13),
                inventory=dict(selected=72,matching=34,slack=4,raw_intervals=6,value=0,deficit=2),
                freezing_layers=[[v['endpoint'] for v in layer] for layer in layers])
            (Path(__file__).parent/'fixtures'/'fixed_P_selection_maximum_zero_payment.json').write_text(json.dumps(global_fixture,indent=2)+'\n')
        if w==8:
            optimum,parts=exact_w8(base,C);cur=(*base[:2],base[2]|set(optimum),base[3]);info=inspect(base,cur,totals)
            assert info['selected']==71 and info['slack']==5 and info['raw_intervals']==7 and info['value']==0
            # Shifted cover of the three original tiles rows4,5 columns8..13:
            # one singleton, two 2x2 squares, and three individually blocked cells.
            region={(r,c) for r in (4,5) for c in range(8,14)}
            assert C&region=={(4,8)}|{(r,c) for r in (4,5) for c in range(9,13)}
            assert sum(map(sum,caps))-6+5==30
            frozen,layers=frozen_certificate(cur)
            saved=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],added_selected=sorted(optimum),
                base_selected=sorted(base[2]),fixed_endpoint_retained_selection_maximum=71,upper_bound='Disjoint2x2TileCaps31_ReplaceThreeTilesBySingletonAndTwoShiftedSquaresCap5InsteadOf6',
                discovery_component_sizes=parts,inventory=info,freezing_layers=[[v['endpoint'] for v in layer] for layer in layers])
            (Path(__file__).parent/'fixtures'/'selection_maximum_singleton_obstruction.json').write_text(json.dumps(saved,indent=2)+'\n')
    # Independent complete finite even-board forest census, no P needed. TT
    # boundary chains must have zero rather than spurious positive resource.
    for h,w in ((2,2),(2,4),(4,2)):
        points=list(itertools.product(range(h),range(w)))
        for bits in range(1<<len(points)):
            T={v for i,v in enumerate(points) if bits>>i&1};cur=h,w,T,[]
            if not feasible(cur,[]):continue
            compile_even_width(cur);totals['small_even_forest_census']+=1
    args.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),records=records,
        scope='Written all-W fixed-P arbitrary selected-extension theorem and constant positive slack; '
              'All-W exact maximum over ALL selections with fixed P is8W+8, fully frozen zero payment, margin4; retained W8 maximum71.',
        limits=['Exact maximum permits all T with fixed P; no maximum over changing P, no global Omega extremizer claim.',
                'Unchanged band phase; alternative phases can remove this particular obstruction.',
                'General target and universal5over6 improvement remain open.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals)),indent=2))

if __name__=='__main__':main()
