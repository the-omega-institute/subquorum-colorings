"""All-T frozen repair frontier: disjoint cover charges and physical flow checks.
General proof: docs/FROZEN_SELECTION_REPAIR_FRONTIER.md. No solver needed.
"""
import argparse
from collections import Counter
import itertools
import json
from pathlib import Path
import random

from check_cooperative_promotion import neighbors
from check_compensation_flow_normal_form import owner_data
from check_crossing_matching_ports import rectangle, band_resources
from check_degree_changing_bent_completions import compile_model, add_selections
from check_forced_mates_and_adjacent_maxima import configuration, upper_certificate
from check_frozen_shared_mixed_gate import check_rank_certificate
from check_monotone_completion_deficit import schedule
from check_promotion_cores import frozen_certificate
from check_residual_corridors import direct_check
from check_selection_maximum_singleton import candidates, tile_bounds
from check_whole_support_fork_flow import fork_flow
from check_whole_support_fork_normal_form import optimize

if not __debug__: raise RuntimeError('Assertions required; no -O.')


def seals(w,k):
    return {(r,10*i+c) for i in range(k) for r,c in ((0,3),(1,2),(w,2),(w+1,3))}


def cover(w,k,cur):
    """Reconstruct the old disjoint ALL-T cap certificate, including replacements."""
    R,C,T,M=cur; empty=(R,C,set(),M)
    caps=tile_bounds(empty,candidates(empty)); members={}
    replaced={(r,c) for i in range(k) for c in (10*i+2,) for r in (0,2,w-2,w)}
    for r in range(0,R,2):
        for c in range(0,C,2):
            if (r,c) not in replaced:
                members[r,c]=(caps[r//2][c//2],{(r+a,c+b) for a in (0,1) for b in (0,1)})
    for i in range(k):
        for r in (0,w-2):
            c=10*i+2
            members['patch',r,c]=(3,{(r+a,c+b) for a in range(4) for b in (0,1)})
    seen=set();loss={}
    for key,(cap,cells) in members.items():
        assert not seen&cells;seen|=cells
        loss[key]=cap-len(T&cells);assert loss[key]>=0
    assert seen==set(itertools.product(range(R),range(C)))
    tau=(7*k+2)*(w//2)+3*k+2
    assert sum(cap for cap,cells in members.values())==tau
    assert sum(loss.values())==tau-len(T)
    return loss


def inspect(w,k,cur,totals,independent=False):
    direct_check(*cur);R,C,T,M=cur;P={v for e in M for v in e};assert seals(w,k)<=T
    reg=rectangle(0,R,0,C);data,closed,N=compile_model(cur,[reg]);own,A,B,X=owner_data(*data[:2])
    central={own[1,10*i+5] for i in range(k)}
    terminal={own[r,10*i+c] for i in range(k) for r in (1,w) for c in (3,6,8)}
    penultimate={own[w-1,10*i+7] for i in range(k)}
    assert len(central)==k and len(terminal)==6*k and len(penultimate)==k
    assert central|terminal|penultimate==set(range(len(closed)))
    assert A<=central and not (central&terminal or central&penultimate or terminal&penultimate)
    for i in range(k):
        c=10*i; o=own[1,c+5]
        assert closed[o]['body']=={(r,c+5) for r in range(1,w+1)} and not data[3][o]
        for r in (1,w):
            leaf=(r,c+3);blocked=(2 if r==1 else w-1,c+3)
            assert len(set(neighbors(blocked))&P)>=2 and blocked not in T
            assert (set(neighbors(leaf))&P)=={(r,c+4)}
            assert len(set(neighbors(leaf))&T)==2
        for r in (1,w):
            for c0 in (3,6,8):
                assert closed[own[r,c+c0]]['body']=={(r,c+c0),(r,c+c0+1)}
        assert closed[own[w-1,c+7]]['body']=={(w-1,c+7),(w-1,c+8)}
    # Test the stronger structural closure of EVERY inter-owner link.
    for p,q in data[2]:
        if own[p]==own[q]: continue
        assert p[0]==q[0] and p[0] in (1,w) and (p[1]-3)//10==(q[1]-3)//10
        assert own[p] in central|terminal and own[q] in central|terminal
    reached=set(A)
    while True:
        nxt=reached|{own[q] for p,q in data[2] if own[p] in reached}
        if nxt==reached: break
        reached=nxt
    assert reached<=central|terminal
    _,gaps,_=band_resources(P,T,reg['bands'])
    term_units=set().union(*(units for b,first,after,units in gaps if b in (0,w//2)))
    assert set().union(*(data[3][o] for o in reached))<=term_units
    loss=cover(w,k,cur);source_keys={(r,10*i+4) for i in range(k) for r in (0,w)}
    missing=sum(N[p] not in T for o in central for p in data[1][o]);a=len(A);b=len(B&central)
    assert missing==k-a+b and sum(loss[key] for key in source_keys)==missing
    beta_keys=set()
    for o in B&terminal:
        p=min(closed[o]['body']);r,c=p; assert c%10 in (6,8)
        key=(0 if r==1 else w,c);assert loss[key]==1;beta_keys.add(key)
    assert len(beta_keys)==len(B&terminal)
    gap_keys={(r,10*i) for i in range(k+1) for r in (0,w)}
    assert sum(loss[key] for key in gap_keys)==len(term_units)
    assert not (source_keys&beta_keys or source_keys&gap_keys or beta_keys&gap_keys)
    ell=sum(loss.values());budget=missing+len(beta_keys)+len(term_units)
    assert ell>=budget
    f=fork_flow(*data);assert f['value']<=len(beta_keys)+len(term_units)
    assert ell+f['deficit']>=k+b
    S=R*C//2-len(M)-len(T);assert S==2*k+ell
    assert S+f['deficit']>=3*k+b
    if independent:
        z=optimize(*data);assert (z['value'],z['cost'])==(f['value'],f['cost'])
        totals['independent_primitive_optima']+=1
    totals['sealed_arbitrary_T_boards']+=1
    totals['central_beta_boards']+=bool(b)
    totals['positive_terminal_beta_boards']+=bool(beta_keys)
    totals['positive_terminal_interval_boards']+=bool(term_units)
    totals['strict_strengthening_boards']+=bool(b)
    return dict(w=w,k=k,size=len(T),ell=ell,alpha=a,central_beta=b,terminal_beta=len(beta_keys),terminal_units=len(term_units),value=f['value'],deficit=f['deficit'],links=f['cost'])


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',required=True,type=Path);args=p.parse_args()
    totals=Counter();rng=random.Random(2026102609);attainers=[];fixture=None
    for w,k in itertools.product((8,10,14,32,64),(1,2,3,5,9)):
        base=configuration(w,k);upper_certificate(w,k,base)
        for d in range(k+1):
            # Every subset on small k; nested representatives for larger k.
            subsets=list(itertools.combinations(range(k),k-d)) if k<=3 else [tuple(range(k-d)),tuple(range(d,k))]
            for subset in subsets:
                cur=(*base[:2],base[2]-{(w+1,10*i+7) for i in subset},base[3])
                ranks=check_rank_certificate(cur,schedule(w,k));totals['sharp_strict_freezing_events']+=len(ranks)
                assert frozen_certificate(cur)[0]=={p for e in cur[3] for p in e}
                z=inspect(w,k,cur,totals,k<=2)
                assert (z['ell'],z['alpha'],z['value'],z['deficit'],z['links'])==(k-d,k,k-d,d,k-d)
                totals['sharp_frozen_attainers']+=1
                if w==8 and subset==tuple(range(k-d)):attainers.append(z)
                if (w,k,d)==(8,3,1) and fixture is None:
                    fixture=dict(shape=cur[:2],selected=sorted(cur[2]),matching=cur[3],freezing_layers=schedule(w,k),expected=z)
        # Rebuild T from only seals, with arbitrary subsets and greedy extensions.
        for repeat in range(24):
            bare=(*base[:2],seals(w,k),base[3]);full=add_selections(bare,rng)
            if repeat%3==0: cur=bare
            elif repeat%3==1: cur=full
            else: cur=(*base[:2],{v for v in sorted(full[2]) if v in seals(w,k) or rng.randrange(2)},base[3])
            inspect(w,k,cur,totals,k==1 and repeat<6)
            totals['rebuilt_from_only_seals']+=1
        # Arbitrary exchanges that retain full freezing (explicitly recheck).
        for repeat in range(12):
            T=set(base[2]);pool=sorted(T-seals(w,k));rng.shuffle(pool)
            for v in pool[:len(pool)//2]:
                test=(*base[:2],T-{v},base[3])
                if frozen_certificate(test)[0]=={p for e in base[3] for p in e}:T.remove(v)
            cur=add_selections((*base[:2],T,base[3]),rng)
            assert frozen_certificate(cur)[0]=={p for e in base[3] for p in e}
            inspect(w,k,cur,totals,k==1 and repeat<3);totals['fully_frozen_arbitrary_exchanges']+=1
        print(f'Checked W={w}, k={k}',flush=True)
    fp=Path(__file__).parent/'fixtures/frozen_selection_frontier_w8_k3.json'
    fp.write_text(json.dumps(fixture,indent=2)+'\n')
    saved=json.loads(fp.read_text());cur=(*saved['shape'],set(map(tuple,saved['selected'])),[tuple(map(tuple,e)) for e in saved['matching']])
    assert inspect(8,3,cur,totals,True)==saved['expected']
    check_rank_certificate(cur,[[tuple(v) for v in layer] for layer in saved['freezing_layers']])
    # An explicit feasible maximum without frozen leaves defeats an unsealed claim.
    ex=json.loads((fp.parent/'nonfrozen_zero_loss_selection_repair.json').read_text())
    cur=(*ex['shape'],set(map(tuple,ex['selected'])),[tuple(map(tuple,e)) for e in ex['matching']]);direct_check(*cur)
    data,_,_=compile_model(cur,[rectangle(0,cur[0],0,cur[1])]);f=fork_flow(*data)
    frozen,_=frozen_certificate(cur);assert len(cur[2])==41 and f['deficit']==0 and len(frozen)==1
    assert not seals(8,1)<=cur[2];totals['excluded_nonfrozen_same_size_repairs']+=1
    args.output.write_text(json.dumps(dict(status='PASS',counts=dict(totals),sharp_attainers=attainers,
        theorem='All even W>=8, k>=1; ANY feasible T with four seals per module (implied by freezing the two column3 leaves); fixed unique actual M and uniform horizontal N; ell+D>=k+central_beta. Fully frozen optimum under D<=d is tau-k+d for integer0<=d<=k; all fixed-P maxima that freeze those leaves have D=k.',
        proof='Written disjoint cover/sink injection; finite checks test adapters and sharpness only.',
        limits=['Other P or N not covered; vertical direction repairs the maximum at no point loss.', 'No universal5/6 improvement; geometry and freezing adapter not end-to-end Lean.']),indent=2)+'\n')
    print(json.dumps(dict(status='PASS',counts=dict(totals)),indent=2))

if __name__=='__main__': main()
