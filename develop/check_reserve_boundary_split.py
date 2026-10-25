"""Actual reserve ownership migration and exact all-reservation compensation.

The proof is a general two-source/single-shared-unit projection and lift.
Finite tests audit the geometric adapter and independent original flow.
"""
import argparse
from collections import Counter, deque
import itertools
import json
from pathlib import Path
import random

from check_merger_completion_reserves import (
    STATES,complete,feasible,frozen,frozen_certificate,load,neighbors,
    owner_data,whole_bands,whole_support_data,
)
from check_frozen_beta_support_fork import restrict
from check_rematching_receiver_flux import canonical
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__:
    raise RuntimeError('Run without -O.')

FIXTURE=Path(__file__).parent/'fixtures/frozen_reserve_boundary_split.json'
CHAIN=[((5,6),(5,7)),((5,8),(5,9)),((5,10),(5,11))]


def rematch(base):
    f=json.loads(FIXTURE.read_text())
    removed={tuple(map(tuple,e)) for e in f['removed']}
    added=[tuple(map(tuple,e)) for e in f['added']]
    assert removed<=canonical(base[3])
    return (*base[:2],base[2]|{(9,15)},
            [e for e in base[3] if tuple(sorted(e)) not in removed]+added)


def clipped(d,resources):
    return (*d[:3],{o:js&resources for o,js in d[3].items()},set(resources))


def distance(d,source):
    owners,_,_,_=owner_data(*d[:2]);out={i:set() for i in range(len(d[1]))}
    for u,v in d[2]:
        if owners[u]!=owners[v]:
            out[owners[u]].add(owners[v])
    dist={source:0};queue=deque([source])
    while queue:
        u=queue.popleft()
        for v in out[u]:
            if v not in dist:
                dist[v]=dist[u]+1;queue.append(v)
    return dist


def model(current):
    assert feasible(current) and frozen(current)
    d,meta,_=whole_support_data(current,whole_bands(current))
    o,aa,bb,mm=owner_data(*d[:2]);left,right=o[5,6],o[3,15]
    assert aa=={left,right} and o[5,12] in mm
    assert d[1][right]==((3,15),(10,9))
    j,k=meta['owner'][2,13],meta['owner'][5,10]
    assert j in d[4] and k in d[4]
    assert {a for a,s in d[3].items() if j in s}=={right,o[5,12]}
    assert {a for a,s in d[3].items() if k in s}=={right}
    groups=[d[3][left],d[3][o[3,2]],d[3][right]-{j},d[3][o[10,8]]]
    assert list(map(len,groups))[1:]==[2,10,5]
    units=[u for group in groups for u in group]+[j]
    assert len(units)==len(set(units))
    filled=(5,5) in o
    beta=o[5,5] if filled else None
    dl,dr=distance(d,left),distance(d,right)
    assert set(dl)&bb==({beta} if filled else set())
    assert not set(dr)&bb
    assert set(dl)&set(dr)==set(), 'No shared intermediate owner is hidden by interval projection.'
    for unit in d[4]:
        actual=[min((dist[a] for a,s in d[3].items() if unit in s and a in dist),default=None) for dist in (dl,dr)]
        expected=([3,0] if unit==j else [0,None] if unit in groups[0] else
                  [1,None] if unit in groups[1] else [None,0] if unit in groups[2] else
                  [None,1] if unit in groups[3] else [None,None])
        assert actual==expected
    assert all(e in d[2] for e in CHAIN)
    return d,meta,groups,j,k,filled


def predicted(groups,j,filled,available):
    inf=1000
    lp=0 if groups[0]&available else 1 if filled or groups[1]&available else inf
    rp=0 if groups[2]&available else 1 if groups[3]&available else inf
    candidates=[(0,0)]
    if lp<inf:candidates.append((1,lp))
    if rp<inf:candidates.append((1,rp))
    if j in available:candidates.append((1,0))
    if lp<inf and rp<inf:candidates.append((2,lp+rp))
    if j in available and lp<inf:candidates.append((2,lp))
    if j in available and rp<inf:candidates.append((2,3+rp))
    return max(candidates,key=lambda x:(x[0],-x[1]))


def check_available(d,groups,j,filled,A,totals,independent=True):
    data=clipped(d,A);answer=fork_flow(*data);expected=predicted(groups,j,filled,A)
    assert (answer['value'],answer['cost'])==expected
    if independent:
        for forks in (False,True):
            brute=optimize(*data,allow_forks=forks)
            assert (brute['value'],brute['cost'])==expected
            totals['independent_primitive_packs']+=1
    totals['reservation_checks']+=1
    return expected


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path,required=True);a=ap.parse_args()
    _,base=load();totals=Counter();records={};good=[];rng=random.Random(2026102503)
    f=json.loads(FIXTURE.read_text());saved=(*f['shape'],set(map(tuple,f['selected'])),[tuple(map(tuple,e)) for e in f['matching']])
    assert saved[:3]==rematch(base)[:3] and canonical(saved[3])==canonical(rematch(base)[3])
    rho={tuple(w['endpoint']):w['rank'] for w in f['strict_witnesses']}
    mate={v:w for e in saved[3] for v,w in (e,e[::-1])}
    assert set(rho)==set(mate)
    for record in f['strict_witnesses']:
        v=tuple(record['endpoint']);kept=list(map(tuple,record['kept_neighbors']))
        assert len(set(kept))==len(kept)==2
        assert all(w in set(neighbors(v)) and (w in saved[2] or
                   (w in mate and rho[mate[w]]<rho[v])) for w in kept)
    totals['saved_actual_strict_freezing_certificates']=1
    for state in STATES:
        if state[0] in ('inner_beta','outer_beta'):continue
        before=complete(base,state);cur=rematch(before);d,meta,groups,j,k,filled=model(cur)
        old,oldmeta,_=whole_support_data(before,whole_bands(before));oo,oa,ob,om=owner_data(*old[:2])
        oldj=oldmeta['owner'][2,13]
        assert {a for a,js in old[3].items() if oldj in js}=={oo[5,12]}
        assert len(d[4])==len(old[4])-3 and len(oa)==2 and len(ob)==len(owner_data(*d[:2])[2])
        identities=lambda data,info:{(info['intervals'][u]['band'],info['intervals'][u]['first'],info['intervals'][u]['last']) for u in data[4]}
        old_units,new_units=identities(old,oldmeta),identities(d,meta)
        assert old_units-new_units=={(4,13,13),(4,14,14),(4,15,15)}
        assert not new_units-old_units
        full=check_available(d,groups,j,filled,d[4],totals)
        one=check_available(d,groups,j,filled,{j},totals)
        release=check_available(d,groups,j,filled,{j,k},totals)
        assert full==(2,int(filled)) and one==((2,1) if filled else (1,0))
        assert release==((2,1) if filled else (2,3))
        if not filled:
            for source in (owner_data(*d[:2])[0][5,6],owner_data(*d[:2])[0][3,15]):
                owners,aa,_,_=owner_data(*d[:2])
                one_source=restrict(d,set(range(len(d[1])))-(aa-{source}),{j})
                assert fork_flow(*one_source)['value']==1
                totals['individual_shared_unit_controls']+=1
        # Every availability of the five behavior classes, both a single
        # representative and the entire chosen class. These are tests, not
        # the proof of all arbitrary original-resource subsets.
        classes=groups+[{j}]
        for flags in itertools.product((False,True),repeat=5):
            chosen=[g for g,flag in zip(classes,flags) if flag and g]
            for A in (set().union(*chosen),{min(g) for g in chosen}):
                check_available(d,groups,j,filled,A,totals)
                totals['class_availability_controls']+=1
        # All original singleton/pair identities, including inaccessible ones.
        for size in (0,1,2):
            for subset in itertools.combinations(sorted(d[4]),size):
                check_available(d,groups,j,filled,set(subset),totals)
                totals['all_singleton_pair_reservations']+=1
        for _ in range(128):
            A={unit for unit in d[4] if rng.randrange(2)}
            check_available(d,groups,j,filled,A,totals)
            totals['random_large_reservations']+=1
        records[state[0]]=dict(available_intervals=len(d[4]),group_sizes=list(map(len,groups)),shared_identity=meta['intervals'][j],replacement_private_identity=meta['intervals'][k],full=full,only_shared=one,shared_plus_private=release)
        good.append((state,cur,j,k,filled))
    # q copies with cap/release choices. No original owners/links/betas are
    # removed; only original interval availability is restricted to J and
    # optionally K. Formula handles simultaneous, overlapping repairs.
    options=list(itertools.product(range(4),(False,True)))
    for q in range(1,4):
        for choice in itertools.product(options,repeat=q):
            T=set();M=[];wanted=set();fill=release=overlap=0
            for i,(s,opened) in enumerate(choice):
                state,cur,j,k,filled=good[s];move=lambda v:(v[0]+14*i,v[1])
                T|={move(v) for v in cur[2]};M.extend(tuple(move(v) for v in e) for e in cur[3])
                wanted.add((7*i+2,13,13))
                if opened:wanted.add((7*i+5,10,10))
                fill+=filled;release+=opened;overlap+=filled and opened
            current=(14*q,18,T,M);assert feasible(current) and frozen(current)
            d,meta,_=whole_support_data(current,whole_bands(current))
            A={u for u in d[4] if (meta['intervals'][u]['band'],meta['intervals'][u]['first'],meta['intervals'][u]['last']) in wanted}
            assert len(A)==q+release
            answer=fork_flow(*clipped(d,A))
            assert (answer['value'],answer['cost'])==(q+fill+release-overlap,fill+3*(release-overlap))
            if q<=2:
                result=optimize(*clipped(d,A));assert (result['value'],result['cost'])==(answer['value'],answer['cost'])
                totals['independent_copy_packs']+=1
            totals['copy_cap_release_models']+=1
    a.output.write_text(json.dumps(dict(status='PASS',totals=dict(totals),models=records,
        scope='Actual monotone old-T/P extension with original singleton changing from private alpha support to alpha+mixed support; two sources reach same unit. General exact two-source shared-unit projection/lift and all-original-reservation formula; physical full pools still V2c0/1. All-q overlap-correct repair V=q+|F union E|,c=|F|+3|E minus F|. Arbitrary further geometric extensions not asserted; universal compensation and5/6 OPEN.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',totals=dict(totals))))


if __name__=='__main__':main()
