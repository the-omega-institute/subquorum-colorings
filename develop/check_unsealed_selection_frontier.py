"""Arbitrary-T frontier with an exact physical boundary-seal defect term.
General proof: FROZEN_SELECTION_REPAIR_FRONTIER.md, Section5.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_frozen_selection_frontier import (configuration,cover,rectangle,compile_model,
    owner_data,band_resources,fork_flow,direct_check,neighbors,add_selections,frozen_certificate)
from check_whole_support_fork_normal_form import optimize

if not __debug__:raise RuntimeError('Assertions required; no -O.')


def inspect(w,k,cur,totals,independent=False):
    R,C,T,M=cur;direct_check(*cur);reg=rectangle(0,R,0,C)
    data,closed,N=compile_model(cur,[reg]);own,A,B,X=owner_data(*data[:2]);P={p for edge in M for p in edge}
    central={own[1,10*i+5] for i in range(k)}
    terminal={own[r,10*i+c] for i in range(k) for r in (1,w) for c in (3,6,8)}
    assert A<=central
    reached=set(A)
    while True:
        nxt=reached|{own[q] for p,q in data[2] if own[p] in reached}
        if nxt==reached:break
        reached=nxt
    for p,q in data[2]:
        if own[p]!=own[q]:
            assert p[0]==q[0] and p[0] in (1,w) and (p[1]-3)//10==(q[1]-3)//10
    assert reached<=central|terminal and reached&central<=A
    _,gaps,_=band_resources(P,T,reg['bands'])
    units=set().union(*(Q for j,first,after,Q in gaps if j in (0,w//2)))
    assert set().union(*(data[3][o] for o in reached))<=units
    loss=cover(w,k,cur);source_keys={(r,10*i+4) for i in range(k) for r in (0,w)}
    gap_keys={(r,10*i) for i in range(k+1) for r in (0,w)}
    missing=sum(N[p] not in T for o in central for p in data[1][o]);a=len(A);b=len(B&central)
    assert missing==k-a+b
    outer4=sum((r,10*i+4) in T for i in range(k) for r in (0,w+1))
    outer3absent=sum((r,10*i+3) not in T for i in range(k) for r in (0,w+1))
    left_beta={own[r,10*i+3] for i in range(k) for r in (1,w)}&B
    right_beta=(B&terminal)-left_beta
    beta_keys={(0 if min(closed[o]['body'])[0]==1 else w,min(v[1] for v in closed[o]['body'])) for o in right_beta}
    assert len(beta_keys)==len(right_beta) and all(loss[x]==1 for x in beta_keys)
    assert sum(loss[x] for x in source_keys)==missing-outer4
    assert outer4+len(left_beta)==outer3absent
    empty2=sum(not ({(r,10*i+2),(r+1,10*i+2)}&T) for i in range(k) for r in (0,w))
    assert sum(loss[x] for x in gap_keys)==len(units)-empty2
    assert not(source_keys&gap_keys or source_keys&beta_keys or gap_keys&beta_keys)
    ell=sum(loss.values());assert ell>=missing-outer4+len(right_beta)+len(units)-empty2
    f=fork_flow(*data);assert f['value']<=len(B&terminal)+len(units)
    E=outer3absent+empty2;assert ell+f['deficit']+E>=k+b
    frozen,_=frozen_certificate(cur)
    leaves={(r,10*i+3) for i in range(k) for r in (1,w)}
    unfrozen=len(leaves-frozen);assert unfrozen<=E<=2*unfrozen
    assert ell+f['deficit']+2*unfrozen>=k+b
    if independent:
        q=optimize(*data);assert (q['value'],q['cost'])==(f['value'],f['cost']);totals['independent_primitive_optima']+=1
    totals['arbitrary_unsealed_T_boards']+=1
    totals['positive_seal_defect_boards']+=E>0
    totals['positive_central_beta_boards']+=b>0
    return dict(w=w,k=k,ell=ell,alpha=a,central_beta=b,deficit=f['deficit'],seal_defect=E,unfrozen_designated_leaves=unfrozen)


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    rng=random.Random(2026102611);totals=Counter();records=[]
    for w,k in itertools.product((8,10,14),(1,2,3,5)):
        base=configuration(w,k)
        for repeat in range(30):
            bare=(*base[:2],set(),base[3]);cur=add_selections(bare,rng)
            if repeat%2:cur=(*cur[:2],{v for v in sorted(cur[2]) if rng.randrange(2)},cur[3])
            z=inspect(w,k,cur,totals,k==1 and repeat<6)
            if repeat==0:records.append(z)
    pth=Path(__file__).parent/'fixtures/nonfrozen_zero_loss_selection_repair.json';j=json.loads(pth.read_text())
    cur=(*j['shape'],set(map(tuple,j['selected'])),[tuple(map(tuple,e)) for e in j['matching']])
    control=inspect(8,1,cur,totals,True)
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(totals),records=records,excluded_frozen_control=control,
        theorem='All final feasible T on existing adjacent-module P,M with uniform horizontal N, with NO freezing or seal hypothesis: ell+D+E>=k+central_beta. E counts missing outer column3 partners plus terminal column2 pairs with no selection; U<=E<=2U where U is unfrozen designated column3 leaves. Thus ell+D+2U>=k+central_beta. The frozen theorem is E=0.',
        proof='Same written disjoint cover, exact source-tile and gap corrections, and complete full-network sink injection; enumeration only checks adapters.'),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals)),indent=2))

if __name__=='__main__':main()
