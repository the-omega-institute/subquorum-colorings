"""Check the general four-arm ledger and its support-only loss family.

General proofs: docs/P_FREE_PIVOT_INTERFACE.md. Enumeration is a check only.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_canonical_band_coarsening import canonical_bands, forests, tile_refinement, random_board
from check_crossing_matching_ports import rectangle
from check_degree_changing_bent_completions import compile_model
from check_compensation_flow_normal_form import owner_data
from check_fixed_P_maximum_frozen_elbow import fixture as maximum_fixture
from check_fully_frozen_elbow_withdrawal import configuration_one
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check, transformed
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize, canonical, primitive_certificates

if not __debug__:
    raise RuntimeError('Assertions required; no -O.')


def regions(cur, bits):
    return canonical_bands(*cur[:2], [rectangle(r,r+2,c,c+2,v) for (r,c),v in bits.items()])


def gap_arms(cur, regs, pivot, vertical, closed):
    """The two open arms and the first bounding P-owner on each side."""
    r,c = pivot
    region = next(x for x in regs if (r,c) in x['cells'])
    assert region['vertical'] == vertical
    band = region['bands'][0]
    P = {v for e in cur[3] for v in e}
    body_owner = {v:o for o,x in enumerate(closed) for v in x['body']}
    at = next(i for i,pair in enumerate(band) if (r,c) in pair)
    assert not P & set(band[at]+band[at+1])
    first,after = at,at+2
    while first and not P & set(band[first-1]):
        first -= 1
    while after < len(band) and not P & set(band[after]):
        after += 1
    def boundary(i):
        if not 0 <= i < len(band):
            return None
        owners = {body_owner[v] for v in band[i] if v in body_owner}
        assert len(owners) <= 1
        return next(iter(owners),None)
    return (set(v for pair in band[first:at] for v in pair),
            set(v for pair in band[at+2:after] for v in pair),
            boundary(first-1),boundary(after))


def anchored(cur, regs, pivot):
    """Common fine-positive-child IDs; local IDs paired in sorted order."""
    fine = forests(cur,tile_refinement(*cur[:2],regs))
    coarse = forests(cur,regs)
    r,c = pivot
    tile = {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}
    children = [cells for cap,cells in fine.values() if cap]
    local = sorted((cells for cells in children if cells <= tile),key=lambda s:sorted(s))
    ids = {cells:('pivot',i) for i,cells in enumerate(local)}
    ids.update({cells:('fine',tuple(sorted(cells))) for cells in children if not cells <= tile})
    mapped = {}
    for j,(cap,cells) in coarse.items():
        if cap:
            positive = [ch for ch in children if ch <= cells]
            assert len(positive) == 1
            mapped[j] = ids[positive[0]]
    assert len(mapped) == len(children) == len(set(mapped.values()))
    return mapped,{ids[ch]:ch for ch in children},coarse


def normalized(data, mapping):
    return (*data[:3],{o:{mapping[j] for j in W} for o,W in data[3].items()},set(mapping.values()))


def bound(left,right,k,left_owner,right_owner):
    owners = {o for o in (left_owner,right_owner) if o is not None}
    backed = ({left_owner} if left and left_owner is not None else set()) | (
        {right_owner} if right and right_owner is not None else set())
    return min(left+right+k,len(owners-backed))


def check_constructive_repair(old,new,pack,blocks,endpoints,totals):
    XL,XR,X0,_,_=blocks;L,R,_,_=endpoints
    affected=XL|XR|X0
    backed=({L} if XL and L is not None else set())|({R} if XR and R is not None else set())
    reserve={o:min(XL if o==L and XL else XR) for o in backed}
    candidates=primitive_certificates(*new)
    def signature(p):
        return (p['kind'],p['owners'],tuple(sorted(p['links'])),p['interval'],p['value'],p.get('witness'),p.get('beta'))
    signatures={signature(p) for p in candidates}
    retained=[];loss=0
    for p in pack['certificates']:
        q=dict(p)
        if p['interval'] in affected:
            witness=p['witness']
            if witness in backed:
                q['interval']=reserve[witness]
                totals['constructive_arm_reassignments']+=1
            else:
                loss+=1
                if p['kind']=='fork':
                    q=next(q for q in candidates if q['kind']=='beta' and q['beta']==p['beta']
                           and set(q['owners'])<=set(p['owners']) and set(q['links'])<=set(p['links']))
                    totals['constructive_forks_truncated_to_one_beta_payment']+=1
                else:
                    assert p['kind']=='interval'
                    continue
        assert signature(q) in signatures
        retained.append(q)
    used_owners=[o for p in retained for o in p['owners']]
    used_units=[p['interval'] for p in retained if p['interval'] is not None]
    used_links={e for p in retained for e in p['links']}
    assert len(used_owners)==len(set(used_owners)) and len(used_units)==len(set(used_units))
    assert used_links<=set(pack['links'])
    assert sum(p['value'] for p in retained)==pack['value']-loss
    assert loss<=bound(len(XL),len(XR),len(X0),L,R)
    _,A,_,_=owner_data(*old[:2])
    old_paid={o for p in pack['certificates'] for o in p['owners'] if o in A}
    new_paid=set(used_owners)&A
    assert new_paid<=old_paid and len(old_paid-new_paid)==loss
    totals['constructive_source_and_link_preserving_repairs']+=1


def check_pivot(cur,bits,pivot,totals,independent=False):
    """Normalize input to H->V by transposing when necessary."""
    if bits[pivot]:
        R,C,T,M=cur
        cur=(C,R,{(c,r) for r,c in T},[tuple((c,r) for r,c in e) for e in M])
        bits={(c,r):not v for (r,c),v in bits.items()}
        pivot=pivot[::-1]
    r,c=pivot
    tile={(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)}
    assert not tile & {v for e in cur[3] for v in e}
    direct_check(*cur)
    oldregs=regions(cur,bits)
    changed=dict(bits);changed[pivot]=True
    newregs=regions(cur,changed)
    old,closed,N0=compile_model(cur,oldregs)
    new,closed1,N1=compile_model(cur,newregs)
    assert old[:2]==new[:2] and set(old[2])==set(new[2])
    assert [(x['body'],x['ends']) for x in closed]==[(x['body'],x['ends']) for x in closed1]
    assert {v for v in N0 if N0[v]!=N1[v]} == tile
    left,right,L,R=gap_arms(cur,oldregs,pivot,False,closed)
    up,down,U,D=gap_arms(cur,newregs,pivot,True,closed)
    om,oc,ofs=anchored(cur,oldregs,pivot)
    nm,nc,nfs=anchored(cur,newregs,pivot)
    assert set(oc)==set(nc)
    k=2-len(tile & cur[2]);assert k in (0,1,2)
    blocks=[{j for j,ch in oc.items() if ch <= arm} for arm in (left,right,tile,up,down)]
    assert len(blocks[2])==k
    assert sum(map(len,blocks))==len(set().union(*blocks))
    owners=lambda *xs:{x for x in xs if x is not None}
    before=[owners(L,R),owners(L,R),owners(L,R),owners(U),owners(D)]
    after=[owners(L),owners(R),owners(U,D),owners(U,D),owners(U,D)]
    old=normalized(old,om);new=normalized(new,nm)
    inv=lambda data,j:{o for o,W in data[3].items() if j in W}
    affected=set().union(*blocks)
    for j in old[4]:
        if j not in affected:
            assert inv(old,j)==inv(new,j)
        else:
            i=next(i for i,B in enumerate(blocks) if j in B)
            assert inv(old,j)==before[i] and inv(new,j)==after[i], (pivot,i,j,inv(old,j),before[i],inv(new,j),after[i])
    ell,h,_,u,d=map(len,blocks)
    bh=bound(ell,h,k,L,R);bv=bound(u,d,k,U,D)
    f0,f1=fork_flow(*old),fork_flow(*new)
    check_constructive_repair(old,new,f0,blocks,(L,R,U,D),totals)
    check_constructive_repair(new,old,f1,[blocks[i] for i in (3,4,2,0,1)],(U,D,L,R),totals)
    delta=f1['value']-f0['value']
    assert -bh<=delta<=bv
    assert max(bh,bv)<=max(1,k)
    if independent:
        for data,f in ((old,f0),(new,f1)):
            alt=optimize(*data)
            assert (alt['value'],alt['cost'])==(f['value'],f['cost'])
        totals['independent_primitive_optimum_pairs']+=1
    totals['pivots']+=1;totals['kappa_'+str(k)]+=1
    totals['support_entries_checked']+=len(old[4])
    totals['coincident_boundary_pairs']+=int(L is not None and L==R)+int(U is not None and U==D)
    totals['nonzero_payment_changes']+=int(bool(delta))
    totals['both_horizontal_owners_backed']+=int(L is not None and R is not None and ell>0 and h>0)
    return dict(pivot=list(pivot),kappa=k,arms=[ell,h,u,d],owners=[L,R,U,D],
                lower=-bh,upper=bv,old_value=f0['value'],new_value=f1['value'])


def family(m):
    assert isinstance(m,int) and m>=0
    raw=json.loads((Path(__file__).parent/'fixtures/P_free_support_only_pivot.json').read_text())
    R,C=raw['shape'];T=set(map(tuple,raw['selected']));M=[tuple(map(tuple,e)) for e in raw['matching']]
    bits={(r,c):bool(v) for r,c,v in raw['tile_directions']}
    ranks=[[tuple(v) for v in layer] for layer in raw['strict_freezing_layers']]
    cur=R,C+2*m,T,M
    bits={(r,c):bits.get((r,c),False) for r in range(0,R,2) for c in range(0,C+2*m,2)}
    return cur,bits,ranks


def check_family(m,totals):
    cur,bits,ranks=family(m)
    direct_check(*cur)
    P={v for e in cur[3] for v in e}
    assert len(cur[2])==73 and len(cur[3])==35
    assert len(check_rank_certificate(cur,ranks))==70 and frozen_certificate(cur)[0]==P
    totals['strict_freezing_events']+=70
    oldregs=regions(cur,bits);changed=dict(bits);changed[2,16]=True;newregs=regions(cur,changed)
    old,closed,_=compile_model(cur,oldregs);new,newclosed,_=compile_model(cur,newregs)
    assert old[:2]==new[:2] and set(old[2])==set(new[2])
    assert [x['body'] for x in closed]==[x['body'] for x in newclosed]
    own,A,B,X=owner_data(*old[:2]);a,b,z=own[3,12],own[5,17],own[5,15]
    assert A=={a,b} and (len(A),len(B),len(X))==(2,2,5)
    assert all(len({(r+1,c),(r-1,c),(r,c+1),(r,c-1)}&(P|cur[2]))==3 for o in A for r,c in old[1][o])
    ofs,nfs=forests(cur,oldregs),forests(cur,newregs)
    cellmap=lambda data,fs:{o:{fs[j][1] for j in W} for o,W in data[3].items()}
    os,ns=cellmap(old,ofs),cellmap(new,nfs)
    assert {ofs[j][1] for j in old[4]}=={nfs[j][1] for j in new[4]}
    target={frozenset({(2,c),(3,c)}) for c in range(18,28+2*m)}
    assert os[a]==target and not ns[a] and len(target)==10+2*m
    assert all(os[o]==ns[o] for o in os if o!=a)
    assert all({o for o,W in os.items() if cells in W}=={a} for cells in target)
    assert len(old[4])==len(new[4])==116+16*m
    assert os[z]=={frozenset({(4,13),(5,13)})} and not os[b]
    external={(p,q) for p,q in old[2] if own[p]!=own[q]}
    assert {(p,q) for p,q in external if own[p] in {a,b,z}}=={((5,17),(5,16))}
    f0,f1=fork_flow(*old),fork_flow(*new)
    assert (f0['value'],f0['cost'],f1['value'],f1['cost'])==(2,1,1,1)
    for data,expected in ((old,(2,1)),(new,(1,1))):
        alt=optimize(*data)
        assert (alt['value'],alt['cost'])==expected
    row=check_pivot(cur,bits,(2,16),totals,True)
    assert row['kappa']==0 and row['lower']==-1 and row['upper']==0
    totals['support_only_family_members']+=1
    return dict(extension=m,shape=list(cur[:2]),selected=73,matching=35,frozen=70,
                raw=116+16*m,old_value=2,new_value=1,lost_supports=10+2*m,
                unchanged_all_positive_forest_cell_sets=True,ledger=row)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);args=p.parse_args()
    totals=Counter();rng=random.Random(2026102631);records=[]
    original,bits0,ranks0=configuration_one();base,bits1,ranks1=family(0)
    assert base==(*original[:2],{v for v in original[2] if not (v[0] in (2,3) and v[1]>=18)},original[3])
    assert bits0==bits1 and ranks0==ranks1
    cur,bits,_,_=maximum_fixture()
    P={v for e in cur[3] for v in e}
    for tile in sorted(bits):
        r,c=tile
        if not {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)} & P:
            records.append(check_pivot(cur,bits,tile,totals,True))
    # Independently sampled feasible configurations, several direction patterns.
    for R,C in ((4,4),(4,8),(6,6),(8,10),(12,12)):
        for _ in range(12):
            board=random_board(R,C,rng);P={v for e in board[3] for v in e}
            for pattern in range(3):
                bits={(r,c):(bool(pattern) if pattern<2 else bool(rng.randrange(2)))
                      for r in range(0,R,2) for c in range(0,C,2)}
                for tile in sorted(bits):
                    r,c=tile
                    if not {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)} & P:
                        records.append(check_pivot(board,bits,tile,totals,True))
    # Sparse matching / sparse selections produce long, positive two-sided arms.
    for _ in range(100):
        R=C=8
        board=random_board(R,C,rng)
        board=R,C,{v for v in board[2] if rng.random()<.35},[e for e in board[3] if rng.random()<.4]
        P={v for e in board[3] for v in e}
        for pattern in range(3):
            bits={(r,c):(bool(pattern) if pattern<2 else bool(rng.randrange(2)))
                  for r in range(0,R,2) for c in range(0,C,2)}
            for tile in sorted(bits):
                r,c=tile
                if not {(r+i,c+j) for i,j in itertools.product(range(2),repeat=2)} & P:
                    records.append(check_pivot(board,bits,tile,totals,True))
    # Abstract ledger checks include coincident global boundary owners, beta
    # forks, two physically separate BP gates, and unaffected resources/links.
    abstract=[]
    for _ in range(500):
        kinds,pairs,possible=canonical(rng.choice(('AAAABM','AAABMM','AAAABB')))
        links=[e for e in possible if rng.random()<.15]
        endpoints=[rng.choice([None]+list(range(len(pairs)))) for _ in range(4)]
        L,R,U,D=endpoints
        sizes=[rng.randrange(3) for _ in range(5)];ell,h,k,u,d=sizes
        ids=[];nextid=0
        for size in sizes:
            ids.append(set(range(nextid,nextid+size)));nextid+=size
        Q=set(range(nextid+2));W0={o:set() for o in range(len(pairs))};W1={o:set() for o in W0}
        owners=lambda *xs:{x for x in xs if x is not None}
        for block,before,after in zip(ids,[owners(L,R)]*3+[owners(U),owners(D)],
                                     [owners(L),owners(R)]+[owners(U,D)]*3):
            for o in before:W0[o]|=block
            for o in after:W1[o]|=block
        for j in range(nextid,nextid+2):
            for o in W0:
                if rng.random()<.2:W0[o].add(j);W1[o].add(j)
        old=kinds,pairs,links,W0,Q;new=kinds,pairs,links,W1,Q
        f0,f1=fork_flow(*old),fork_flow(*new)
        check_constructive_repair(old,new,f0,ids,endpoints,totals)
        check_constructive_repair(new,old,f1,[ids[i] for i in (3,4,2,0,1)],(U,D,L,R),totals)
        delta=f1['value']-f0['value'];bh=bound(ell,h,k,L,R);bv=bound(u,d,k,U,D)
        assert -bh<=delta<=bv and max(bh,bv)<=max(1,k)
        for data,f in ((old,f0),(new,f1)):
            alt=optimize(*data);assert (alt['value'],alt['cost'])==(f['value'],f['cost'])
        totals['abstract_ledger_independent_pairs']+=1
        totals['abstract_beta_fork_certificates']+=sum(p['kind']=='fork' for f in (f0,f1) for p in f['certificates'])
        totals['abstract_coincident_boundary_pairs']+=int(L is not None and L==R)+int(U is not None and U==D)
        abstract.append(dict(sizes=sizes,owners=endpoints,lower=-bh,upper=bv,delta=delta))
    family_records=[check_family(m,totals) for m in (0,1,2,4,16,64)]
    # Every dihedral image tests the same physical obstruction.
    cur,bits,ranks=family(0);R,C=cur[:2]
    for tr,fr,fc in itertools.product((False,True),repeat=3):
        shape,T,M=transformed(*cur,tr,fr,fc)
        def point(v):
            r,c=v
            if fr:r=R-1-r
            if fc:c=C-1-c
            return (c,r) if tr else (r,c)
        bb={}
        for (r,c),v in bits.items():
            cells=[point((r+i,c+j)) for i,j in itertools.product(range(2),repeat=2)]
            bb[min(r for r,c in cells),min(c for r,c in cells)]=v!=tr
        image=(*shape,T,M)
        check_rank_certificate(image,[[point(v) for v in layer] for layer in ranks])
        pp=[point((r,c)) for r,c in ((2,16),(3,17))]
        tile=min(r for r,c in pp),min(c for r,c in pp)
        row=check_pivot(image,bb,tile,totals,True)
        assert abs(row['new_value']-row['old_value'])==1 and row['kappa']==0
        totals['dihedral_support_only_obstructions']+=1
    assert totals['both_horizontal_owners_backed']>0 and totals['abstract_beta_fork_certificates']>0
    assert totals['abstract_coincident_boundary_pairs']>0
    kinds,pairs,_=canonical('AA')
    old=kinds,pairs,[],{0:{0,1},1:{0,1}},{0,1}
    new=kinds,pairs,[],{0:set(),1:set()},{0,1}
    assert fork_flow(*old)['value']==optimize(*old)['value']==2
    assert fork_flow(*new)['value']==optimize(*new)['value']==0
    totals['abstract_kappa_two_sharp_loss_controls']+=1
    result=dict(status='PASS',scope='Finite checks of separately proved general four-arm and payment bounds; no universal 5/6 claim.',
                totals=dict(totals),pivots=records,abstract_ledgers=abstract,support_only_family=family_records)
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(totals,sort_keys=True))


if __name__=='__main__':
    main()
